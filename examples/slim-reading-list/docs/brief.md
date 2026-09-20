# Reading list — illustrative brief

All dates, outcomes, reviewers and results in this example are fictional.
Spec revision: DEMO-SPEC-1.

## Problem

User: one researcher saving article URLs. Pain: links disappear among browser tabs.
Current workaround: paste URLs into a text file. Desired outcome: save and find a URL
within 30 seconds. Estimate: 4 hours including 20 minutes of process work. Kill if the
local JSON approach cannot support the slice within 8 hours; re-scope before continuing.
Tier: Slim. No accounts, sharing, sensitive records or external requests.

## Scope and acceptance criteria

UC-01: save a URL and list saved URLs. Inputs: URL string and local file path. Output:
ordered titles/URLs in the terminal, or a clear error. Non-goals: scraping, syncing,
search, tags, cloud hosting and multiple users.

- AC-01: Given an empty list, when a valid HTTPS URL is added, listing shows it once.
- AC-02: Given a saved URL, adding the exact same URL leaves one entry and reports a duplicate.
- AC-03: Given an invalid URL, adding it exits unsuccessfully and leaves storage unchanged.
- AC-04: Given malformed JSON, listing reports the invalid file and does not overwrite it.

## Architecture and infrastructure

CLI parses input → use case validates/adds/lists → JSON adapter reads/writes. Domain
validation has no filesystem imports. File writes use a temporary file and rename;
only one process is supported. Critical contract: invalid input never modifies storage.
Use Python's standard library. Keep the data file outside the source checkout.
Delivery: local source checkout with documented CLI steps. Env vars: none. Secrets:
none required. Backup: copy the JSON file before upgrades; restore by replacing it.
Cost ceiling: no hosting or API cost. Diagnostics: clear stderr messages and exit codes;
request IDs/uptime monitoring are n/a because this is a local single-process tool.

## GO decision

Illustrative owner/reviewer: Alex, 2026-09-17; reviewed spec DEMO-SPEC-1.
Prior planning stages, gate checklist, required tasks, reviewed draft artifacts, UC/module
mapping, risk review and planning DoD assessed. Decision Log exists (one entry is enough).
Custom tasks: none. Agent runs: n/a, no workers. AI session draft reviewed in log.
Premortem is advisory for Slim: likely failure is accidental storage loss; mitigate with
invalid-data rejection and backup. No open red items; no orange overrides. GO for UC-01
only. The owner must re-open planning if sharing or cloud storage is requested.
