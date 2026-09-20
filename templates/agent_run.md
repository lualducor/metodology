# Agent Run Log

Copy to `docs/09_agents/runs/`. Replace prompts with evidence; use `n/a: reason` only when justified.

```yaml
ai_assisted: false
ai_session_id: null
human_reviewed: false
reviewer: null
reviewed_at: null
reviewed_revision: null
```

## Agent

Record runtime/model version, agent identity, session/run ID and reviewer.

## Task

Link the task, UC/ACs, frozen input revisions and branch/worktree.

## Scope

List allowed files, tools and network hosts (default none); exclude secrets, push, merge, deploy and production data.

## Result

Record changed files, output revision, verifier result, evidence links, elapsed time/cost and unresolved issues.

## Review verdict

Record pending/accepted/rejected, human reviewer, tested commit, spec revision and evidence links. Re-review after relevant changes.
