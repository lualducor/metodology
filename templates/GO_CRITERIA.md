# GO Criteria Checklist

Copy to `docs/00_meta/go-criteria.md`. Replace prompts with evidence; use `n/a: reason` only when justified.

```yaml
ai_assisted: false
ai_session_id: null
human_reviewed: false
reviewer: null
reviewed_at: null
reviewed_revision: null
```

## Problem clarity

Link the observed pain, target user, outcome, effort estimate and kill criteria.

## Behavior clarity

Link the UC/ACs, failure states, I/O and planned checks for the slice.

## Shape clarity

Link the architecture and data model; explain the critical dependency choices.

## Module clarity

Name the owner of each critical behavior and link its contract or Slim design section.

## Scope clarity

Link the smallest slice, exclusions, fallback and completion criteria.

## AI readiness

Confirm relevant context is reviewed, task boundaries are explicit and review capacity is scheduled.

## Infrastructure readiness

Link the deployment, environment, secrets, recovery and cost decisions applicable to this tier.

## Risk & failure readiness

Review risks, kill criteria and premortem when applicable. List open blockers and expiring orange overrides.
