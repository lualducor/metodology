# Reading list — illustrative evidence

These are sample results, not executed tests. Code revision DEMO-CODE-1;
spec revision DEMO-SPEC-1; fictional human reviewer Alex on 2026-09-17.

## Verification evidence

| AC | Check | Sample result | Sample evidence | Code/spec revision | Reviewer/date |
|---|---|---|---|---|---|
| AC-01 | Add then list in a temporary directory | MET | Run SAMPLE-1: expected URL once, exit 0 | DEMO-CODE-1 / DEMO-SPEC-1 | Alex / 2026-09-17 |
| AC-02 | Add the same URL twice | MET | Run SAMPLE-2: one entry, duplicate notice | DEMO-CODE-1 / DEMO-SPEC-1 | Alex / 2026-09-17 |
| AC-03 | Add an invalid URL; compare data hashes | MET | Run SAMPLE-3: nonzero exit, same data hash | DEMO-CODE-1 / DEMO-SPEC-1 | Alex / 2026-09-17 |
| AC-04 | List malformed JSON; compare file hashes | MET | Run SAMPLE-4: readable error, unchanged file | DEMO-CODE-1 / DEMO-SPEC-1 | Alex / 2026-09-17 |

Regression: re-run all four scenarios after the malformed-JSON fix; manually inspect the
diff for scope and boundary changes. Replacing code or spec invalidates affected results.
A real record would link captured output and the actual tested commit/spec hash.

## Production readiness

Illustrative walkthrough: errors include recovery instructions and nonzero exit status;
invalid input and malformed files preserve data. No secrets or network calls. Backup a
sample JSON file, replace it with a modified copy, restore and compare entries: sample pass.
Performance target: list 1,000 records in under one second on the owner's laptop; sample
measurement 0.1 seconds. No service uptime or browser accessibility checks apply.
No red failures or orange overrides remain in this scenario.

## Release and rollback

Illustrative release 0.1.0: deliver DEMO-CODE-1 with CLI usage instructions, preserving the
separate data file. Before upgrade, copy data; run the acceptance scenarios against a
fixture. Known limitations: exact-string duplicate matching and one process at a time.
Rollback walkthrough: switch to prior source version, restore sample backup, list entries;
expected fixture restored. Initial installation can be removed while preserving the data.
This paragraph demonstrates the record; it does not deploy or tag anything.

## Observation

Fictional next-day feedback: five URLs saved and found in under 30 seconds each. Success
measure met. No request for additional features. Decision: keep as a local single-user
tool and archive active development; owner accepts manual maintenance. If shared with
others, re-tier and establish a maintenance cadence before release to them.
