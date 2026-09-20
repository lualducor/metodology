# Reading list — illustrative log

All entries are fictional, including human review. Never copy these as real evidence.

## Decisions

D-01, Alex, 2026-09-17: use a local JSON file instead of a database. One user, no concurrent
writers and a small list make this sufficient. Revisit if multi-process access is needed.
No decision quota applies. No warnings have been overridden.

## Risks and failures

R-01: accidental data overwrite; mitigate with invalid-data rejection and backup/restore
walkthrough. Owner Alex accepts residual single-process limitation until 2026-10-01;
reopen then if still actively used.

F-01: first draft treated corrupt JSON as an empty list. caught_by: verify-01; AC-04 check
found potential data loss. Fix: fail without writes. Sample regression SAMPLE-4 passes
on DEMO-CODE-1. Routine intermediate assertion failures remain in sample test output.

## Tasks and AI review

T-01 → UC-01 / AC-01–04. Scope: CLI, list use case and JSON adapter. Check: all four
acceptance scenarios plus diff review. Review estimate: 15 minutes, scheduled Sept 17.
AI session S-01 supplied a draft; fictional Alex reviewed planning and final code at
DEMO-SPEC-1 / DEMO-CODE-1. Verdict: accepted after F-01 fix. Actual review: 20 minutes;
queue age 30 minutes; rework 15 minutes. One work item pending at peak; session and diff
counted once. No autonomous workers or loops, so their conditional artifacts are n/a.

## Retro

Outcome: fictional release and successful first-use observation. Estimate: 4 hours;
actual: 3.5 hours. Process work: 20 minutes (9.5%); review: 20 minutes; rework: 15 minutes.
Caught: malformed storage behavior via verify-01. Missed: spec originally did not explain
the recovery message; clarified before release. No rubber-stamped gates identified.

One proposal: add a corrupt-storage check example to the template guidance. Exposure:
one applicable project, one catch, approximately five minutes to check. Consequence:
possible loss of saved URLs. Alternative: stronger persistence library plus restore tests.
This is a teaching hypothesis, not sufficient evidence to mandate a new universal rule.
