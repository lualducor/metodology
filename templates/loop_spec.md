# Loop Spec

Copy to `docs/09_agents/loops/`. Replace prompts with evidence; use `n/a: reason` only when justified.

```yaml
ai_assisted: false
ai_session_id: null
human_reviewed: false
reviewer: null
reviewed_at: null
reviewed_revision: null
```

## Goal

Name the task and UC/ACs, expected outcome, spec version and owner. Freeze the approved scope.

## Stop conditions

Specify machine-checkable success, maximum iterations, wall-clock deadline, per-call timeout and budget ceiling. Freeze this file before starting.

## Per-pass verification

Use a pre-approved command the runner cannot edit; record exit code and revision each pass.

## Checkpoint cadence

Set when to persist progress and review it; record input/output revisions and consumed budget each pass.

## Context strategy

Choose fresh-per-pass or accumulated context, required inputs and the rule for resetting drift.

## Escalation triggers

Stop on changed requirements, scope drift, repeated no-progress, ambiguous verifier results or a limit. Name the human owner.

## Kill switch

Provide a concrete stop command. Keep the companion runlog append-only.

## Permissions

List allowed files, tools and network hosts. Protect this spec and the verifier from
worker writes. Declare how the runtime enforces restrictions; a prompt is not a sandbox.

## Runlog and recovery

Name the separate append-only runlog. Per pass record spec/input hashes, output revision,
verifier/result/evidence, time/cost and stop reason. State how to reconcile in-flight work
on restart; do not retry an uncertain external side effect blindly. Stop and debrief before
changing this spec or verifier. A successful run still requires human review.
