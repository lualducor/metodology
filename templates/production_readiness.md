# Production Readiness Checklist

Copy to `docs/06_verification/production-readiness.md`. Replace prompts with evidence; use `n/a: reason` only when justified.

```yaml
ai_assisted: false
ai_session_id: null
human_reviewed: false
reviewer: null
reviewed_at: null
reviewed_revision: null
```

## Error handling

Record checks for critical errors, safe recovery and useful user-facing messages.

## Secrets

Record scan result and credential handling. Never paste credential values into this document.

## Logging/observability

Describe how failures can be diagnosed without logging secrets or unnecessary personal data.

## Rollback plan

Record candidate/prior revision, rollback or forward-repair steps, data compatibility and walkthrough evidence.

## Env vars

List variable names, purpose, required/optional status and safe placeholders; never real secrets.

## Backup/export

Describe what is backed up, where, retention, owner and tested restore/export evidence.

## Performance budget

Define workload, environment and measurable latency/resource targets, then record the result.
