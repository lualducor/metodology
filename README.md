# LuchoLabs Methodology

A standalone method for shipping small, maintainable software with AI assistance.
Write the behavior, build a narrow slice, verify the result and review before release.

Current release: **4.6**. No dashboard or external service is required.

## Start a Slim project

1. Read the [tier and risk guidance](SPEC-GATED-MODULAR-DELIVERY-v4.6.md#2-choose-a-tier-and-route-each-change).
2. Copy `templates/slim/brief.md`, `checks.md` and `log.md` into your project's `docs/`.
3. Fill the brief, including acceptance criteria and the human GO decision.
4. Implement one small task; record checks and review evidence on the exact revision.
5. Complete release/rollback checks, observe the outcome and write the retrospective.

The [worked reading-list example](examples/slim-reading-list/README.md) shows the full
three-file flow. It is a fictional teaching example, not a claim of shipped software.
For Serious/Mission-critical projects use the full [artifact templates](templates)
and [methodology](SPEC-GATED-MODULAR-DELIVERY-v4.6.md).

## Validate locally

Requires Python 3.10+ and PyYAML. From this repository:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/validate.py --project examples/slim-reading-list --tier slim
```

To check your project's three files, replace the example path with your project root.
Validation checks structure and policy/resource consistency. It does **not** approve
release, execute your tests, or establish that an acceptance criterion is met.

## Resources

- [Canonical manifest and policy](methodology.v4.yaml): schema 4, policy release 4.6.
- [Reusable task prompts](prompts/README.md) and [optional agent roles](agents/agents.v4.yaml).
- [Looping and graph-looping proposal](proposals/looping-and-graph-looping.md), including engine evaluation.
- [Changelog and migration](CHANGELOG.md) and [real-project evidence ledger](EVIDENCE.md).

Licensed under [MIT](LICENSE).
