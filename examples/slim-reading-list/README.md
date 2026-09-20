# Worked Slim example: personal reading list

This is a **fictional, completed teaching example**. No application, real test run,
deployment or human approval is claimed. `DEMO-CODE-1` and `DEMO-SPEC-1` below are
illustrative revision labels, not Git commits. Replace them with real revision IDs
and evidence links in a real project. Do not add this example to the evidence ledger.

The example follows one slice from observed pain through GO, build, verify, ship and
observation. It illustrates a local tool with no network service or agent workers.

1. [Brief](docs/brief.md): scope, acceptance criteria, boundaries and GO.
2. [Checks](docs/checks.md): sample acceptance results, readiness and release.
3. [Log](docs/log.md): decisions, failure/catch, review and retrospective.

From the methodology repository root, run:

```sh
python3 scripts/validate.py --project examples/slim-reading-list --tier slim
```

This checks the document shape, not the fictional results.
