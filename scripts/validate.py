#!/usr/bin/env python3
"""Validate methodology resources and optional Slim structure, never release approval."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
SEVERITIES = {'red', 'orange', 'yellow'}
REQUIREMENTS = {'required', 'light', 'implicit', 'merged', 'skipped', 'post_mortem', 'informal'}


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently accepting an overwritten policy."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_yaml(path):
    return yaml.load(path.read_text(encoding='utf-8'), Loader=UniqueLoader)


def frontmatter(path):
    text = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        raise ValueError(f'{path.name}: missing YAML frontmatter')
    data = yaml.load(match[1], Loader=UniqueLoader)
    if not isinstance(data, dict):
        raise ValueError(f'{path.name}: frontmatter must be a mapping')
    return data


def headings(path):
    # Fenced examples are not document headings.
    text = re.sub(r'^```.*?^```[^\n]*$', '', path.read_text(encoding='utf-8'), flags=re.M | re.S)
    return set(re.findall(r'^## (.+?)\s*$', text, re.M))


def validate(root=ROOT, project=None, tier=None):
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    def ids(rows, label):
        values = [row['id'] for row in rows]
        check(len(values) == len(set(values)), f'{label}: duplicate IDs')
        return set(values)

    def resource(relative):
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError(f'resource escapes repository: {relative}')
        check(path.is_file(), f'missing resource: {relative}')
        return path

    try:
        data = load_yaml(root / 'methodology.v4.yaml')
        check(data['version'] == 4, 'unsupported manifest schema version')
        policy = data['policy']
        check(policy['red_overridable'] is False, 'red blockers must not be overridable')
        check(data['override']['red_overridable'] is False, 'override policy permits red blockers')
        check(policy['decision_log_check'] == 'presence', 'Decision Log must be presence-based')
        check(policy['review_cap'] == 2, 'default review cap must be 2')
        check(policy['evidence_revision_required'] is True, 'evidence must name its revision')
        doc = resource(data['methodology_doc'])
        if doc.is_file():
            meta = frontmatter(doc)
            check(meta.get('release') == data['release'], 'document/manifest release mismatch')
            check(meta.get('policy') == policy, 'document/manifest policy mismatch')
        tiers = ids(data['tiers'], 'tiers')
        check(tiers == {'spike', 'slim', 'serious', 'mission_critical'}, 'unexpected tier set')
        stages = ids(data['stages'], 'stages')
        orders = [s['order'] for s in data['stages']]
        check(orders == list(range(1, len(orders) + 1)), 'stages must have consecutive order')
        for stage in data['stages']:
            check(set(stage['per_tier']) == tiers, f'{stage["id"]}: incomplete tier requirements')
            check(set(stage['per_tier'].values()) <= REQUIREMENTS, f'{stage["id"]}: invalid requirement')
            check(stage.get('next') in stages | {'iteration', None}, f'{stage["id"]}: unknown next stage')
            check(stage.get('backtrack') in stages | {None}, f'{stage["id"]}: unknown backtrack stage')
        artifacts = ids(data['artifacts'], 'artifacts')
        for artifact in data['artifacts']:
            label = artifact['id']
            check(artifact['stage'] in stages | {'cross_cutting'}, f'{label}: unknown stage')
            check(artifact['gate_severity'] in SEVERITIES, f'{label}: invalid severity')
            check(set(artifact.get('applies_to', tiers)) <= tiers, f'{label}: unknown applies_to tier')
            check(set(artifact.get('min_count_tiers', [])) <= tiers, f'{label}: unknown count tier')
            check(artifact.get('conditional') in {None, 'agent_workers', 'loops'}, f'{label}: unknown capability')
            destination = Path(artifact['destination'])
            check(not destination.is_absolute() and '..' not in destination.parts, f'{label}: unsafe destination')
            if artifact.get('template'):
                path = resource(str(Path(data['templates_dir']) / artifact['template']))
                if path.is_file():
                    missing = set(artifact.get('required_headings', [])) - headings(path)
                    check(not missing, f'{label}: missing template headings {sorted(missing)}')
            else:
                check(artifact.get('generated') is True, f'{label}: no template or generator declaration')
        gate_ids = []
        for stage, gates in data['gates'].items():
            check(stage in stages, f'gate group: unknown stage {stage}')
            for gate in gates:
                gate_ids.append(gate['id'])
                check(bool(re.fullmatch(r'[a-z_]+-\d{2}', gate['id'])), f'invalid gate ID: {gate["id"]}')
                check(gate['severity'] in SEVERITIES, f'{gate["id"]}: invalid severity')
                check(set(gate.get('applies_to', tiers)) <= tiers, f'{gate["id"]}: unknown gate tier')
                overrides = gate.get('override_severity', {})
                check(set(overrides) <= tiers, f'{gate["id"]}: unknown severity tier')
                check(set(overrides.values()) <= SEVERITIES, f'{gate["id"]}: invalid tier severity')
        check(len(gate_ids) == len(set(gate_ids)), 'duplicate gate IDs')
        planning = data['planning_validation_gate']['checks']
        ids(planning, 'planning checks')
        decisions = [c for c in planning if c['id'] == 'decision_log_presence']
        check(len(decisions) == 1, 'missing Decision Log presence check')
        check(all('min_decisions' not in c for c in planning), 'Decision Log entry quotas are forbidden')
        for c in planning:
            check(c['severity'] in SEVERITIES, f'{c["id"]}: invalid planning severity')
        for target in data['backtrack_rules'].values():
            check(target in stages | {'current_stage'}, f'unknown backtrack target: {target}')
        roster = load_yaml(resource('agents/agents.v4.yaml'))
        check(roster['release'] == data['release'], 'agent roster release mismatch')
        roles = ids(roster['agents'], 'agents')
        prompts = {}
        for path in sorted((root / 'prompts').glob('*.md')):
            if path.name == 'README.md':
                continue
            prompt = frontmatter(path)
            check(prompt['id'] not in prompts, f'duplicate prompt ID: {prompt["id"]}')
            prompts[prompt['id']] = prompt
            check(prompt['id'] == path.stem, f'{path.name}: prompt ID/filename mismatch')
            check(prompt['stage'] in stages, f'{path.name}: unknown stage')
            check(prompt['agent'] in roles, f'{path.name}: unknown agent')
            check(set(prompt['inputs']) <= artifacts, f'{path.name}: unknown input artifact')
            check(prompt['output'] in artifacts, f'{path.name}: unknown output artifact')
        for agent in roster['agents']:
            check(set(agent['stages']) <= stages, f'{agent["id"]}: unknown stage')
            check(set(agent['inputs'] + agent['outputs']) <= artifacts, f'{agent["id"]}: unknown artifact')
            check(bool(agent['must_not']), f'{agent["id"]}: missing boundaries')
            check(set(agent['prompts']) <= set(prompts), f'{agent["id"]}: missing prompt')
        slim_files = data['slim_profile']['files']
        check(set(slim_files) == {'brief.md', 'checks.md', 'log.md'}, 'Slim profile must define all three files')
        for filename, required in slim_files.items():
            path = resource(f'templates/slim/{filename}')
            if path.is_file():
                check(set(required) <= headings(path), f'Slim template {filename}: missing headings')
            if project is not None:
                candidate = project / 'docs' / filename
                check(candidate.is_file(), f'project: missing docs/{filename}')
                if candidate.is_file():
                    check(set(required) <= headings(candidate), f'project: {filename} missing headings')
        # Check local Markdown destinations, excluding external URLs and anchor-only links.
        for path in root.rglob('*.md'):
            if any(part.startswith('.') for part in path.relative_to(root).parts):
                continue
            for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^\s)]+)\)', path.read_text(encoding='utf-8')):
                if re.match(r'^[a-z]+:', target, re.I) or target.startswith('#'):
                    continue
                target_path = target.split('#', 1)[0]
                check((path.parent / target_path).exists(), f'{path.relative_to(root)}: broken link {target}')
        check(project is None or tier == 'slim', 'project validation supports only --tier slim')
    except (OSError, ValueError, TypeError, KeyError, AttributeError, yaml.YAMLError) as exc:
        errors.append(f'invalid resource: {exc}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, help='project root containing docs/')
    parser.add_argument('--tier', choices=['slim'])
    args = parser.parse_args()
    if bool(args.project) != bool(args.tier):
        parser.error('--project and --tier slim must be used together')
    errors = validate(project=args.project, tier=args.tier)
    for error in errors:
        print(f'ERROR: {error}', file=sys.stderr)
    if errors:
        return 1
    print('PASS: structural checks only; human gate and release review still required.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
