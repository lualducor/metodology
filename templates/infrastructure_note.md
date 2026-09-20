# Infrastructure Note

Copy to `docs/03_architecture/infrastructure.md`. Replace prompts with evidence; use `n/a: reason` only when justified.

```yaml
ai_assisted: false
ai_session_id: null
human_reviewed: false
reviewer: null
reviewed_at: null
reviewed_revision: null
```

## Deploy target

Name local/hosted runtime, owner, environments and reproducible delivery steps.

## Environments & env vars

List environments, variable names and safe placeholders; explain how credentials are injected outside model context.

## CI pipeline

List applicable lint/typecheck/test/build commands and link candidate-revision results; justify unavailable checks.

## Secrets handling

Describe storage, access, scanning and rotation without including secret values.

## Backup & restore

Name data, cadence, owner, recovery steps and latest restore evidence.

## Monitoring & alerts

Name health/error signals, endpoints, owners and response expectations, or justify n/a for a local tool.

## Cost ceiling

Set hosting/API ceilings, monitoring and the action taken before exceeding them.
