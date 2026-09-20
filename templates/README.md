# Artifact templates

For the full profile, copy each applicable template to its manifest destination. For
`multiple: true`, choose a stable unique filename within the destination directory.
Loop specs use `<loop>.md` and runlogs `<loop>.runlog.md`. Never copy sample claims as
real evidence. For Slim, use the [three-file profile](slim); conditional worker/loop
records remain separate when those capabilities are used.

| Template | Destination | Applicability |
|---|---|---|
| [capture.md](capture.md) | `docs/00_meta/capture.md` | Per tier/stage requirements |
| [problem_brief.md](problem_brief.md) | `docs/01_problem/problem.md` | Per tier/stage requirements |
| [product_spec.md](product_spec.md) | `docs/02_spec/spec.md` | Per tier/stage requirements |
| [use_case.md](use_case.md) | `docs/02_spec/use-cases/` | Per tier/stage requirements |
| [architecture_note.md](architecture_note.md) | `docs/03_architecture/architecture.md` | Per tier/stage requirements |
| [adr.md](adr.md) | `docs/03_architecture/decisions/` | Per tier/stage requirements |
| [module_contract.md](module_contract.md) | `docs/04_modules/` | serious, mission_critical |
| [vertical_slice.md](vertical_slice.md) | `docs/05_vertical_slice/slice.md` | Per tier/stage requirements |
| [GO_CRITERIA.md](GO_CRITERIA.md) | `docs/00_meta/go-criteria.md` | Per tier/stage requirements |
| [premortem.md](premortem.md) | `docs/00_meta/premortem.md` | serious, mission_critical |
| [planning_validation_report.md](planning_validation_report.md) | `docs/00_meta/` | Per tier/stage requirements |
| [task.md](task.md) | `docs/00_meta/tasks/` | Per tier/stage requirements |
| [test_plan.md](test_plan.md) | `docs/06_verification/test-plan.md` | Per tier/stage requirements |
| [production_readiness.md](production_readiness.md) | `docs/06_verification/production-readiness.md` | Per tier/stage requirements |
| [release_notes.md](release_notes.md) | `docs/07_release/release-notes.md` | Per tier/stage requirements |
| [known_limitations.md](known_limitations.md) | `docs/07_release/known-limitations.md` | Per tier/stage requirements |
| [retro.md](retro.md) | `docs/00_meta/retro.md` | Per tier/stage requirements |
| [observation_entry.md](observation_entry.md) | `docs/08_observation/` | Per tier/stage requirements |
| [decision_log_entry.md](decision_log_entry.md) | `docs/decisions.md` | Per tier/stage requirements |
| [failure_log_entry.md](failure_log_entry.md) | `docs/failures.md` | Per tier/stage requirements |
| [risk_entry.md](risk_entry.md) | `docs/risks.md` | Per tier/stage requirements |
| [ai_session.md](ai_session.md) | `docs/99_ai-sessions/` | Per tier/stage requirements |
| [infrastructure_note.md](infrastructure_note.md) | `docs/03_architecture/infrastructure.md` | slim, serious, mission_critical |
| [agent_run.md](agent_run.md) | `docs/09_agents/runs/` | Only when using agent_workers |
| [loop_spec.md](loop_spec.md) | `docs/09_agents/loops/` | Only when using loops |
| [threat_model.md](threat_model.md) | `docs/00_meta/threat_model.md` | mission_critical |
| [privacy_review.md](privacy_review.md) | `docs/00_meta/privacy_review.md` | mission_critical |
| [independent_review.md](independent_review.md) | `docs/00_meta/independent_review.md` | mission_critical |
| [incident_response.md](incident_response.md) | `docs/00_meta/incident_response.md` | mission_critical |
| [loop_runlog.md](loop_runlog.md) | `docs/09_agents/loops/` | Only when using loops |
