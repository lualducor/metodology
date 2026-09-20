# Test Plan / QA Checklist

Copy to `docs/06_verification/test-plan.md`. Replace prompts with evidence; use `n/a: reason` only when justified.

```yaml
ai_assisted: false
ai_session_id: null
human_reviewed: false
reviewer: null
reviewed_at: null
reviewed_revision: null
```

## Critical flows

List UC/ACs, test data, environment, commands and expected results for the critical paths.

## Acceptance results

For each AC record result, evidence, tested commit, spec revision and reviewer/date. Missing or stale evidence is not a pass.

## Regression checklist

Name affected existing behaviors and how to re-check them after changes.

## Edge cases

List empty, invalid, boundary, duplicate and concurrent inputs that matter for this slice, and expected behavior.

Use `AC ID | check/command | result | evidence path | tested commit | spec revision | reviewer/date`. A heading or passing structure check is not a passing acceptance test.
