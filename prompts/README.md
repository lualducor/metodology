# Task prompts

Optional briefs for the stages and worker/loop roles. Each file has YAML frontmatter
with an ID, stage, role, input artifact IDs and output artifact ID. Load the corresponding
Slim sections when using that profile. Agents return drafts and evidence; humans approve.
Runtime permission enforcement belongs to the chosen execution environment.

- [problem-interrogator](problem-interrogator.md): problem → `problem_brief`.
- [spec-writer](spec-writer.md): spec → `product_spec`.
- [architecture-options](architecture-options.md): architecture → `architecture_note`.
- [module-contractor](module-contractor.md): module_design → `module_contract`.
- [slice-cutter](slice-cutter.md): vertical_slice → `vertical_slice`.
- [verify-qa](verify-qa.md): verify → `test_plan`.
- [harden-auditor](harden-auditor.md): harden → `production_readiness`.
- [observe-synthesizer](observe-synthesizer.md): observe → `observation_entry`.
- [retro-writer](retro-writer.md): ship → `retro`.
- [orchestrator-decompose](orchestrator-decompose.md): build → `build_task`.
- [worker-task](worker-task.md): build → `agent_run`.
- [merge-reviewer](merge-reviewer.md): verify → `agent_run`.
- [loop-pass](loop-pass.md): build → `agent_run`.
- [loop-debrief](loop-debrief.md): build → `decision_log`.
