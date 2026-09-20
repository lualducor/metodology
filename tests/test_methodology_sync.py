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


if __name__ == '__main__':
    unittest.main()
