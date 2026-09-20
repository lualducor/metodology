"""Regression tests prove invalid policy/resources fail, not just that YAML parses."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate import ROOT, validate


class MethodologyValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))

    def mutate(self, edit):
        path = self.root / 'methodology.v4.yaml'
        data = yaml.safe_load(path.read_text())
        edit(data)
        path.write_text(yaml.safe_dump(data, sort_keys=False))

    def assert_error(self, fragment, **kwargs):
        errors = validate(self.root, **kwargs)
        self.assertTrue(any(fragment in e for e in errors), errors)

    def test_release_and_worked_example_pass(self):
        self.assertEqual([], validate(self.root))
        self.assertEqual([], validate(self.root, self.root / 'examples/slim-reading-list', 'slim'))

    def test_missing_template_fails(self):
        (self.root / 'templates/retro.md').unlink()
        self.assert_error('missing resource: templates/retro.md')

    def test_missing_required_heading_fails(self):
        path = self.root / 'templates/use_case.md'
        path.write_text(path.read_text().replace('## Acceptance criteria', '## Optional notes'))
        self.assert_error('missing template headings')

    def test_fenced_heading_does_not_count(self):
        path = self.root / 'templates/use_case.md'
        path.write_text(path.read_text().replace('## Acceptance criteria', '```\n## Acceptance criteria\n```'))
        self.assert_error('missing template headings')

    def test_duplicate_gate_id_fails(self):
        self.mutate(lambda d: d['gates']['spec'][0].update(id=d['gates']['problem'][0]['id']))
        self.assert_error('duplicate gate IDs')

    def test_unknown_tier_fails(self):
        self.mutate(lambda d: d['artifacts'][0].update(applies_to=['tiny']))
        self.assert_error('unknown applies_to tier')

    def test_unknown_stage_fails(self):
        self.mutate(lambda d: d['stages'][0].update(next='missing'))
        self.assert_error('unknown next stage')

    def test_unknown_gate_tier_fails(self):
        self.mutate(lambda d: d['gates']['ship'][-1].update(applies_to=['tiny']))
        self.assert_error('unknown gate tier')

    def test_missing_slim_profile_file_fails(self):
        self.mutate(lambda d: d['slim_profile']['files'].pop('checks.md'))
        self.assert_error('Slim profile must define all three files')

    def test_invalid_severity_fails(self):
        self.mutate(lambda d: d['gates']['verify'][0].update(severity='green'))
        self.assert_error('invalid severity')

    def test_red_override_fails(self):
        self.mutate(lambda d: d['override'].update(red_overridable=True))
        self.assert_error('override policy permits red')

    def test_decision_quota_fails(self):
        self.mutate(lambda d: d['planning_validation_gate']['checks'][8].update(min_decisions=3))
        self.assert_error('quotas are forbidden')

    def test_document_policy_drift_fails(self):
        path = self.root / 'SPEC-GATED-MODULAR-DELIVERY-v4.6.md'
        path.write_text(path.read_text().replace('review_cap: 2', 'review_cap: 3'))
        self.assert_error('policy mismatch')

    def test_duplicate_yaml_policy_key_fails(self):
        path = self.root / 'methodology.v4.yaml'
        path.write_text(path.read_text() + '\npolicy: {}\n')
        self.assert_error('duplicate YAML key: policy')

    def test_unknown_prompt_artifact_fails(self):
        path = self.root / 'prompts/spec-writer.md'
        path.write_text(path.read_text().replace('output: product_spec', 'output: imaginary'))
        self.assert_error('unknown output artifact')

    def test_missing_slim_project_file_fails(self):
        project = self.root / 'examples/slim-reading-list'
        (project / 'docs/checks.md').unlink()
        self.assert_error('project: missing docs/checks.md', project=project, tier='slim')

    def test_malformed_yaml_fails(self):
        (self.root / 'methodology.v4.yaml').write_text('policy: [')
        self.assert_error('invalid resource')

    def test_escaping_resource_fails(self):
        self.mutate(lambda d: d.update(methodology_doc='../outside.md'))
        self.assert_error('resource escapes repository')

    def assert_no_error(self, fragment, **kwargs):
        errors = validate(self.root, **kwargs)
        self.assertFalse(any(fragment in e for e in errors), errors)

    def append(self, relative, text):
        path = self.root / relative
        path.write_text(path.read_text() + text)

    def replace_heading(self, wrapped):
        path = self.root / 'templates/use_case.md'
        path.write_text(path.read_text().replace('## Acceptance criteria', wrapped))

    def test_link_syntax_inside_code_is_not_checked(self):
        self.append('templates/adr.md', '\nSee `[diff](../../src/x.py)` and:\n\n~~~\n[ref](nowhere.md)\n~~~\n')
        self.assertEqual([], validate(self.root))

    def test_titled_broken_link_fails(self):
        self.append('templates/adr.md', '\n[title](nowhere.md "Nowhere")\n')
        self.assert_error('templates/adr.md: broken link nowhere.md')

    def test_nested_image_broken_link_fails(self):
        self.append('templates/adr.md', '\n[![badge](../LICENSE)](nowhere.md)\n')
        self.assert_error('templates/adr.md: broken link nowhere.md')

    def test_tilde_fenced_heading_does_not_count(self):
        self.replace_heading('~~~\n## Acceptance criteria\n~~~')
        self.assert_error('missing template headings')

    def test_indented_fenced_heading_does_not_count(self):
        self.replace_heading('   ```\n## Acceptance criteria\n   ```')
        self.assert_error('missing template headings')

    def test_commented_heading_does_not_count(self):
        self.replace_heading('<!-- ## Acceptance criteria -->')
        self.assert_error('missing template headings')

    def test_malformed_prompt_names_file_and_other_checks_still_run(self):
        path = self.root / 'prompts/spec-writer.md'
        path.write_text(path.read_text().replace('inputs:\n', 'not_inputs:\n'))
        (self.root / 'templates/retro.md').unlink()
        errors = validate(self.root)
        self.assertTrue(any(e.startswith('invalid resource prompts/spec-writer.md:') for e in errors), errors)
        self.assertIn('missing resource: templates/retro.md', errors)

    def test_prompt_roster_drift_fails(self):
        path = self.root / 'prompts/loop-debrief.md'
        path.write_text(path.read_text().replace('output: decision_log', 'output: retro'))
        self.assert_error('prompts/loop-debrief.md: output outside agent orchestrator outputs')

    def test_prompt_not_listed_by_agent_fails(self):
        path = self.root / 'prompts/loop-debrief.md'
        path.write_text(path.read_text().replace('agent: orchestrator', 'agent: builder'))
        self.assert_error('prompts/loop-debrief.md: agent builder does not list this prompt')

    def test_invalid_slim_planning_severity_fails(self):
        self.mutate(lambda d: [c for c in d['planning_validation_gate']['checks']
                               if c['id'] == 'cross_stage_consistency'][0].update(slim_severity='green'))
        self.assert_error('cross_stage_consistency: invalid Slim planning severity')

    def test_roster_schema_version_fails(self):
        path = self.root / 'agents/agents.v4.yaml'
        path.write_text(path.read_text().replace('schema_version: 4', 'schema_version: 3'))
        self.assert_error('agent roster schema version mismatch')

    def test_templates_dir_moves_slim_templates_too(self):
        (self.root / 'templates').rename(self.root / 'kit')
        self.mutate(lambda d: d.update(templates_dir='kit'))
        self.assert_no_error('missing resource')

    def test_missing_project_directory_is_reported_once(self):
        errors = validate(self.root, self.root / 'nope', 'slim')
        self.assertTrue(any('project directory not found' in e for e in errors), errors)
        self.assertFalse(any('project: missing docs' in e for e in errors), errors)

    def test_spike_ship_fails(self):
        self.mutate(lambda d: [s for s in d['stages'] if s['id'] == 'ship'][0]['per_tier'].update(spike='light'))
        self.assert_error('Spikes never ship')

    def test_serious_restore_and_monitoring_are_red(self):
        gates = {g['id']: g for g in yaml.safe_load((self.root / 'methodology.v4.yaml').read_text())['gates']['harden']}
        for gate in ('harden-10', 'harden-11'):
            self.assertEqual({'serious': 'red', 'mission_critical': 'red'}, gates[gate]['override_severity'], gate)

    def test_slim_section_unknown_target_fails(self):
        self.mutate(lambda d: d['slim_profile']['sections'].update(problem_brief='brief.md#Nope'))
        self.assert_error('Slim section for problem_brief: unknown target')

    def test_slim_section_missing_artifact_fails(self):
        self.mutate(lambda d: d['slim_profile']['sections'].pop('retro'))
        self.assert_error("Slim sections must map exactly the Slim-applicable artifacts: ['retro']")

    def test_slim_override_log_drift_fails(self):
        self.mutate(lambda d: d['override'].update(slim_log_to='log.md#Retro'))
        self.assert_error('override slim_log_to must be the Slim Decision Log section')


if __name__ == '__main__':
    unittest.main()
