# Loop runlog

Copy beside the frozen spec as `<loop>.runlog.md`. Append events; do not rewrite prior results.

## Run identity

Record run ID, spec path/version/hash, task/UC/ACs, runtime/model, owner and start time.
Do not include secrets. Link the approved file/tool/network scope and budget limits.

## Pass events

Append one event per pass: attempt number, input hashes, output revision, verifier/version,
command and exit code, evidence location, elapsed time, incurred/reserved cost, remaining
limits, next action and reason. Include errors, cancellation and checkpoint/restart events.
A pass that cannot establish its result stops for reconciliation, not blind replay.

## Termination

Append stop reason (success/limit/cancel/error/escalation), total time/cost, output revision,
remaining issues and debrief link. Record human review separately, with reviewer/date and
accepted revision; loop success does not grant permission to merge or deploy.
