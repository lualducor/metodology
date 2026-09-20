# Failure Log

Copy to `docs/failures.md`. Replace prompts with evidence; use `n/a: reason` only when justified.

```yaml
ai_assisted: false
ai_session_id: null
human_reviewed: false
reviewer: null
reviewed_at: null
reviewed_revision: null
```

## Failure

Describe expected/actual behavior, reproduction and affected revision.

## Impact and recovery

State affected data/users, containment, fix and recovery verification.

## Caught by or missed by

Name the stable gate/test ID that caught this, or the gate that should have caught it.

## Follow-up

Assign unresolved work, owner and next action; link the issue or task.

Use stable IDs: `caught_by: verify-01` or `missed_by: spec-03`. Routine test output may remain in test logs; summarize material learning and unresolved failures here.
