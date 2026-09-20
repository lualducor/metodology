#!/usr/bin/env python3
"""Validate methodology resources and optional Slim structure, never release approval."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'methodology.v4.yaml'
ROSTER = 'agents/agents.v4.yaml'
SEVERITIES = {'red', 'orange', 'yellow'}
REQUIREMENTS = {'required', 'light', 'implicit', 'merged', 'skipped', 'post_mortem'}
SLIM_FILES = {'brief.md', 'checks.md', 'log.md'}
SLIM_SEPARATE = 'separate'
FAILURES = (OSError, ValueError, TypeError, KeyError, AttributeError, yaml.YAMLError)
# Markdown links: [text](target), [text](target "title"), [![alt](img)](target), [text](<a b>).
LINK = re.compile(
    r'(?<!!)\[(?:[^\[\]]|!\[[^\]]*\]\([^)]*\))+\]'
    r'\(\s*(?:<([^>]*)>|((?:[^\s()<>]|\([^\s()]*\))+))'
    r'(?:\s+(?:"[^"]*"|\'[^\']*\'|\([^)]*\)))?\s*\)'
)
FENCE = re.compile(r'(`{3,}|~{3,})')


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
        raise ValueError('missing YAML frontmatter')
    data = yaml.load(match[1], Loader=UniqueLoader)
    if not isinstance(data, dict):
        raise ValueError('frontmatter must be a mapping')
    return data


def prose(text):
    """Drop fenced code, inline code and HTML comments: examples are not document structure."""
    kept = []
    fence = None
    for line in text.split('\n'):
        stripped = line.lstrip(' ')
        match = FENCE.match(stripped) if len(line) - len(stripped) <= 3 else None
        if fence is None:
            if match:
                fence = match[1]
            else:
                kept.append(line)
        elif match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not stripped[len(match[1]):].strip():
            fence = None
    text = re.sub(r'<!--.*?-->', '', '\n'.join(kept), flags=re.S)
    return re.sub(r'(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)', '', text)


def headings(path):
    return set(re.findall(r'^## (.+?)\s*$', prose(path.read_text(encoding='utf-8')), re.M))


def links(text):
    for match in LINK.finditer(prose(text)):
        yield match[1] if match[1] is not None else match[2]


class Validator:
    def __init__(self, root=ROOT, project=None, tier=None):
        self.root = Path(root)
        self.project = None if project is None else Path(project)
        self.tier = tier
        self.errors = []
        self.data = {}
        self.tiers = set()
        self.stages = set()
        self.artifacts = {}
        self.roles = {}
        self.prompts = {}

    def check(self, condition, message):
        if not condition:
            self.errors.append(message)

    def guard(self, label, fn, *args):
        """Run one check group; a malformed resource names itself and lets the other groups run."""
        try:
            return fn(*args)
        except FAILURES as exc:
            self.errors.append(f'invalid resource {label}: {exc}')
            return None

    def ids(self, rows, label):
        values = [row['id'] for row in rows]
        self.check(len(values) == len(set(values)), f'{label}: duplicate IDs')
        return set(values)

    def resource(self, relative):
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root.resolve()):
            raise ValueError(f'resource escapes repository: {relative}')
        self.check(path.is_file(), f'missing resource: {relative}')
        return path

    def run(self):
        self.check(self.project is None or self.tier == 'slim', 'project validation supports only --tier slim')
        if self.project is not None and not self.project.is_dir():
            self.errors.append(f'project directory not found: {self.project}')
            self.project = None
        data = self.guard(MANIFEST, load_yaml, self.root / MANIFEST)
        if data is None:
            return self.errors
        if not isinstance(data, dict):
            self.errors.append(f'invalid resource {MANIFEST}: manifest must be a mapping')
            return self.errors
        self.data = data
        groups = (
            (MANIFEST, self.policy),
            (str(data.get('methodology_doc')), self.document),
            (MANIFEST, self.lifecycle),
            (MANIFEST, self.artifact_manifest),
            (MANIFEST, self.gate_manifest),
            (MANIFEST, self.planning),
            (ROSTER, self.roster),
            (MANIFEST, self.slim_profile),
            (MANIFEST, self.project_files),
            ('links', self.links),
        )
        for label, group in groups:
            self.guard(label, group)
        return self.errors

    def policy(self):
        data = self.data
        self.check(data['version'] == 4, 'unsupported manifest schema version')
        policy = data['policy']
        self.check(policy['red_overridable'] is False, 'red blockers must not be overridable')
        self.check(data['override']['red_overridable'] is False, 'override policy permits red blockers')
        self.check(policy['decision_log_check'] == 'presence', 'Decision Log must be presence-based')
        self.check(policy['review_cap'] == 2, 'default review cap must be 2')
        self.check(policy['evidence_revision_required'] is True, 'evidence must name its revision')

    def document(self):
        doc = self.resource(self.data['methodology_doc'])
        if doc.is_file():
            meta = frontmatter(doc)
            self.check(meta.get('release') == self.data['release'], 'document/manifest release mismatch')
            self.check(meta.get('policy') == self.data['policy'], 'document/manifest policy mismatch')

    def lifecycle(self):
        data = self.data
        self.tiers = self.ids(data['tiers'], 'tiers')
        self.check(self.tiers == {'spike', 'slim', 'serious', 'mission_critical'}, 'unexpected tier set')
        self.stages = self.ids(data['stages'], 'stages')
        orders = [s['order'] for s in data['stages']]
        self.check(orders == list(range(1, len(orders) + 1)), 'stages must have consecutive order')
        for stage in data['stages']:
            label = stage['id']
            self.check(set(stage['per_tier']) == self.tiers, f'{label}: incomplete tier requirements')
            self.check(set(stage['per_tier'].values()) <= REQUIREMENTS, f'{label}: invalid requirement')
            self.check(stage.get('next') in self.stages | {'iteration', None}, f'{label}: unknown next stage')
            self.check(stage.get('backtrack') in self.stages | {None}, f'{label}: unknown backtrack stage')
            if label == 'ship':
                # Doc §2: a Spike is never shipped as a Spike; the manifest must not permit it.
                self.check(stage['per_tier'].get('spike') == 'skipped', 'ship: Spikes never ship')
        for target in data['backtrack_rules'].values():
            self.check(target in self.stages | {'current_stage'}, f'unknown backtrack target: {target}')

    def artifact_manifest(self):
        rows = self.data['artifacts']
        self.ids(rows, 'artifacts')
        self.artifacts = {row['id']: row for row in rows}
        for artifact in rows:
            self.guard(f'artifact {artifact.get("id")}', self.artifact, artifact)

    def artifact(self, artifact):
        label = artifact['id']
        tiers = self.tiers
        self.check(artifact['stage'] in self.stages | {'cross_cutting'}, f'{label}: unknown stage')
        self.check(artifact['gate_severity'] in SEVERITIES, f'{label}: invalid severity')
        self.check(set(artifact.get('applies_to', tiers)) <= tiers, f'{label}: unknown applies_to tier')
        self.check(set(artifact.get('min_count_tiers', [])) <= tiers, f'{label}: unknown count tier')
        self.check(artifact.get('conditional') in {None, 'agent_workers', 'loops'}, f'{label}: unknown capability')
        destination = Path(artifact['destination'])
        self.check(not destination.is_absolute() and '..' not in destination.parts, f'{label}: unsafe destination')
        if artifact.get('template'):
            path = self.resource(str(Path(self.data['templates_dir']) / artifact['template']))
            if path.is_file():
                missing = set(artifact.get('required_headings', [])) - headings(path)
                self.check(not missing, f'{label}: missing template headings {sorted(missing)}')
        else:
            self.check(artifact.get('generated') is True, f'{label}: no template or generator declaration')

    def gate_manifest(self):
        gate_ids = []
        for stage, gates in self.data['gates'].items():
            self.check(stage in self.stages, f'gate group: unknown stage {stage}')
            for gate in gates:
                gate_ids.append(gate.get('id'))
                self.guard(f'gate {gate.get("id")}', self.gate, gate)
        self.check(len(gate_ids) == len(set(gate_ids)), 'duplicate gate IDs')

    def gate(self, gate):
        label = gate['id']
        tiers = self.tiers
        self.check(bool(re.fullmatch(r'[a-z_]+-\d{2}', label)), f'invalid gate ID: {label}')
        self.check(gate['severity'] in SEVERITIES, f'{label}: invalid severity')
        self.check(set(gate.get('applies_to', tiers)) <= tiers, f'{label}: unknown gate tier')
        overrides = gate.get('override_severity', {})
        self.check(set(overrides) <= tiers, f'{label}: unknown severity tier')
        self.check(set(overrides.values()) <= SEVERITIES, f'{label}: invalid tier severity')

    def planning(self):
        planning = self.data['planning_validation_gate']['checks']
        self.ids(planning, 'planning checks')
        decisions = [c for c in planning if c['id'] == 'decision_log_presence']
        self.check(len(decisions) == 1, 'missing Decision Log presence check')
        self.check(all('min_decisions' not in c for c in planning), 'Decision Log entry quotas are forbidden')
        for c in planning:
            self.check(c['severity'] in SEVERITIES, f'{c["id"]}: invalid planning severity')
            self.check(c.get('slim_severity', c['severity']) in SEVERITIES, f'{c["id"]}: invalid Slim planning severity')

    def roster(self):
        roster = load_yaml(self.resource(ROSTER))
        self.check(roster['schema_version'] == self.data['version'], 'agent roster schema version mismatch')
        self.check(roster['release'] == self.data['release'], 'agent roster release mismatch')
        self.ids(roster['agents'], 'agents')
        self.roles = {agent['id']: agent for agent in roster['agents']}
        for path in sorted((self.root / 'prompts').glob('*.md')):
            if path.name != 'README.md':
                self.guard(str(path.relative_to(self.root)), self.prompt, path)
        for agent in roster['agents']:
            self.guard(f'agent {agent.get("id")}', self.agent, agent)

    def prompt(self, path):
        name = path.relative_to(self.root)
        prompt = frontmatter(path)
        self.check(prompt['id'] not in self.prompts, f'duplicate prompt ID: {prompt["id"]}')
        self.prompts[prompt['id']] = prompt
        self.check(prompt['id'] == path.stem, f'{name}: prompt ID/filename mismatch')
        self.check(prompt['stage'] in self.stages, f'{name}: unknown stage')
        self.check(set(prompt['inputs']) <= set(self.artifacts), f'{name}: unknown input artifact')
        self.check(prompt['output'] in self.artifacts, f'{name}: unknown output artifact')
        agent = self.roles.get(prompt['agent'])
        self.check(agent is not None, f'{name}: unknown agent')
        if agent is not None:
            # The roster restates stage/inputs/outputs; they must agree with every prompt that names the agent.
            label = agent['id']
            self.check(prompt['id'] in agent['prompts'], f'{name}: agent {label} does not list this prompt')
            self.check(prompt['stage'] in agent['stages'], f'{name}: stage outside agent {label} stages')
            self.check(set(prompt['inputs']) <= set(agent['inputs']), f'{name}: inputs outside agent {label} inputs')
            self.check(prompt['output'] in agent['outputs'], f'{name}: output outside agent {label} outputs')

    def agent(self, agent):
        label = agent['id']
        self.check(set(agent['stages']) <= self.stages, f'{label}: unknown stage')
        self.check(set(agent['inputs'] + agent['outputs']) <= set(self.artifacts), f'{label}: unknown artifact')
        self.check(bool(agent['must_not']), f'{label}: missing boundaries')
        self.check(set(agent['prompts']) <= set(self.prompts), f'{label}: missing prompt')

    def slim_profile(self):
        data = self.data
        slim = data['slim_profile']
        files = slim['files']
        self.check(set(files) == SLIM_FILES, 'Slim profile must define all three files')
        for filename, required in files.items():
            path = self.resource(str(Path(data['templates_dir']) / 'slim' / filename))
            if path.is_file():
                self.check(set(required) <= headings(path), f'Slim template {filename}: missing headings')
        # Every artifact a Slim project owes must say which Slim section carries it (or that it stays separate).
        sections = slim['sections']
        applicable = {aid for aid, row in self.artifacts.items() if 'slim' in row.get('applies_to', self.tiers)}
        drift = sorted(set(sections) ^ applicable)
        self.check(not drift, f'Slim sections must map exactly the Slim-applicable artifacts: {drift}')
        for artifact, target in sections.items():
            if target == SLIM_SEPARATE:
                continue
            filename, _, heading = str(target).partition('#')
            self.check(heading in files.get(filename, []), f'Slim section for {artifact}: unknown target {target}')
        decision_log = self.artifacts.get('decision_log', {})
        self.check(data['override']['log_to'] == decision_log.get('destination'),
                   'override log_to must be the Decision Log destination')
        self.check(data['override']['slim_log_to'] == sections.get('decision_log'),
                   'override slim_log_to must be the Slim Decision Log section')

    def project_files(self):
        if self.project is None:
            return
        for filename, required in self.data['slim_profile']['files'].items():
            candidate = self.project / 'docs' / filename
            self.check(candidate.is_file(), f'project: missing docs/{filename}')
            if candidate.is_file():
                self.check(set(required) <= headings(candidate), f'project: {filename} missing headings')

    def links(self):
        # Local Markdown destinations only; external URLs and anchor-only links are skipped.
        for path in sorted(self.root.rglob('*.md')):
            relative = path.relative_to(self.root)
            if any(part.startswith('.') for part in relative.parts):
                continue
            for target in links(path.read_text(encoding='utf-8')):
                if re.match(r'^[a-z][a-z0-9+.-]*:', target, re.I) or target.startswith('#'):
                    continue
                target_path = unquote(target.split('#', 1)[0])
                self.check((path.parent / target_path).exists(), f'{relative}: broken link {target}')


def validate(root=ROOT, project=None, tier=None):
    return Validator(root, project, tier).run()


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
