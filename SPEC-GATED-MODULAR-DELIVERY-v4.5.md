# SPEC-GATED MODULAR DELIVERY — v4.5

**The single standard for AI-assisted solo software delivery at LuchoLabs.**

A lightweight shipping system that gives you enough engineering discipline to ship
maintainable software without enterprise bureaucracy. It assumes you use AI heavily,
your time is your scarcest resource, and your code will be read by a future-you who
has forgotten everything.

> This document supersedes `SPEC-GATED-MODULAR-DELIVERY-v4.md` (archived in
> `../../docs/archive/`, with v1–v3). Where they conflict, **v4.5 wins.**
> The machine-readable spec remains `methodology.v4.yaml` — v4.5 changes **no**
> stages, tiers, artifacts, gate items, or severities, so the YAML spine is
> unchanged. The YAML is **canonical for everything mechanical** (gate items,
> artifact manifest, health weights, risk list, backtrack rules, dashboard IA);
> this document no longer duplicates those tables. `test_methodology_sync.py`
> keeps doc and YAML agreeing.

---

## 0. What v4.5 changes — and why it exists

v4.5 is the **evidence-gathering release**. Its job is to run on real projects and
record what the methodology actually catches, misses, and costs — so that **v5 is
written from evidence instead of accretion** (every version so far was written from
taste). Two kinds of change:

**Subtraction (one rule, one home):**

| Change | Where it went |
|---|---|
| Gate-item tables, health weights, risk table, backtrack table removed from this doc | `methodology.v4.yaml` (canonical) |
| Anti-Spaghetti rules section deleted | unique rules already live in §5.5 (contract-first, dependency direction) and the YAML gates; the rest were duplicates |
| Definition of Done trimmed to its unique items | the rest restated the Verify/Harden gates |
| "≥3 decisions" PVG threshold dropped from doctrine | counting decisions invites padding; presence stays (see §24 — the dashboard still checks 3 until phase 2) |
| Stale-decision detection dropped from the Next Action Engine | third expiry mechanism; never fired usefully |
| Prompt-improvement-requires-Decision-Log demoted to advisory | unenforced ceremony (§24 was honest about this; now the rule is too) |

**Addition (the new axiom and its machinery):**

| Layer | What it adds | Where |
|---|---|---|
| **Review Budget** | Unreviewed AI output is inventory, not progress; a hard cap on open unreviewed work | §9 |
| **Instrumentation** | Gate-catch/miss tagging, estimate-vs-actual, overhead tracking, per-project retro, evidence ledger | §23 |
| **Rule eviction (Law 4)** | Every rule must earn its keep by v5 or die | §2, §23.3 |
| **Maintenance & Sunset** | Lifecycle for shipped-but-dormant projects — the "quietly rotting" failure mode | §12.1–12.2 |
| **Worker security model** | Prompt-injection, secrets, and permission scoping for agent workers | §10.6.1 |
| **Premortem** | A cheap adversarial pass at GO — someone finally plays red team against the plan | §6.2 |

---

## 1. Core Principles

> **Do not move from idea to code too quickly.** The system exists to stop you from
> creating future pain — not to slow you down.

> **Review bandwidth is the budgeted resource.** AI made code cheap; it did not make
> your attention cheap. A methodology that polices generation but assumes review
> "just happens" optimizes the wrong bottleneck. Gates exist to protect verification
> capacity, not to produce paperwork.

Every project moves through a lifecycle. The lifecycle adapts to project size (tier).
AI accelerates each stage but never replaces the human review at the gates. A project
may proceed with warnings — but the warnings must be **visible**.

## 2. The Four Laws

These override every other rule in this document.

- **Law 1 — Honesty over ceremony.** A skipped stage is fine if you document *why*. A skipped stage hidden under the rug is not.
- **Law 2 — AI output is a draft.** Until read, understood, contract-checked, and accepted by you, AI-generated content does not exist.
- **Law 3 — Future-you is a stranger.** Write every decision, shortcut, known issue, and "I'll fix this later" as if a different person reads it in six months. Because they will.
- **Law 4 — Evidence over accretion.** *(new in v4.5)* A rule that never catches anything is not discipline, it is drag. Every rule in this system must show a recorded catch or a named near-miss by the v5 review, or it is deleted or demoted by default. The burden of proof is on the rule, not on its removal.

---

## 3. Project Tiers

Every project (and every iteration) gets a tier at creation. The tier determines which
stages are mandatory and what the gates check.

| Tier | Typical scope | Lifecycle | Effort |
|---|---|---|---|
| **Spike** | One-off experiment / throwaway | CAPTURE → PROBLEM → VERTICAL SLICE → BUILD → retro note | hard cap < 8h |
| **Slim** | Small useful project, single-user | Full lifecycle; MODULE DESIGN merges into ARCHITECTURE; HARDEN light | hard cap < 40h |
| **Serious** | Used daily, possibly by others | Full lifecycle, all stages | typically 40h+ (no cap) |
| **Mission-critical** | Money, health, security, regulated data, others' livelihoods | Full lifecycle + mandatory security/privacy reviews; SHIP requires peer review or independent verification | typically 40h+ (no cap) |

**Tier rules:** you can downgrade or upgrade at any time (an upgrade backfills earlier
stages). A Spike that ships is renamed and re-tiered — you ship a Slim that started as
a Spike, never a "Spike."

The per-tier stage requirements (required / light / merged / skipped / implicit /
post-mortem / informal) are defined in `methodology.v4.yaml` `stages.per_tier` and
rendered by the dashboard.

---

## 4. Lifecycle

```
CAPTURE → PROBLEM → SPEC → ARCHITECTURE → MODULE DESIGN → VERTICAL SLICE
                                                               │
      ┌────────────────────────────────────────────────────────┘
      ▼
  🚦 GO / NO-GO  (GO_CRITERIA + Planning Validation Gate + premortem)
      ▼
  BUILD ⇄ continuous verification → VERIFY gate → HARDEN gate → SHIP → OBSERVE
      ▲                                                            │
      └── next iteration: → PROBLEM (scope changed) or SPEC ───────┤
                                                                   ▼
                       no active iteration → MAINTAIN (§12.1) → SUNSET (§12.2)
```

- **MODULE DESIGN merges with ARCHITECTURE** for Slim; distinct for Serious / Mission-critical.
- **Continuous verification** lives inside BUILD; the **VERIFY gate** is a checkpoint that the critical flows actually pass.
- **HARDEN is a gate**, not a phase — a production-readiness checklist run against an already-tested build.
- **OBSERVE → PROBLEM/SPEC** loops formally for the next iteration; a shipped project with no active iteration enters **MAINTAIN**, not limbo.

### 4.1 Stage task checklists

Each stage's **Minimum output** list is the stage's **pending-task checklist** in the
dashboard, filtered by tier. Mark each `done`, `n/a` (with a one-line reason that
mirrors into the Decision Log), or add custom tasks. Tasks track *work*; gates check
*outcomes* — closing a task does not auto-close its gate item.

---

## 5. Stages

Each stage has: **Goal · Question · Minimum output · Entry · Exit · Red flags · Backtrack target · Next.** Templates referenced by name live in `templates/`; each artifact's destination path and required headings are in the YAML manifest.

### 5.1 CAPTURE
- **Goal:** capture the raw idea before it disappears.
- **Question:** what is the idea, and what triggered it?
- **Minimum output:** raw idea note (`capture.md`), rough name, pain one-liner, possible target user, why it caught you.
- **Entry:** an idea exists. **Exit:** you can explain it in one paragraph; the pain is visible.
- **Red flags:** you wrote a feature, not a problem; no user; excited by the tool, not the pain.
- **Backtrack:** N/A. **Next:** PROBLEM.

### 5.2 PROBLEM
- **Goal:** define the real problem before defining the app.
- **Question:** what pain, for whom, why does it matter?
- **Minimum output:** `problem_brief.md` — target user, pain, current workaround, desired outcome, success definition, non-goals, **effort estimate**, **kill criteria**.
- **Entry:** CAPTURE complete. **Exit:** user/pain/outcome/non-goals clear; you can defend why this should exist.
- **Red flags:** "I want to build an app that…"; no user; no pain; no outcome; scope already wide.
- **Backtrack:** CAPTURE. **Next:** SPEC.

### 5.3 SPEC
- **Goal:** define what the software must do.
- **Question:** what behavior must the system have?
- **Minimum output:** `product_spec.md` + `use_case.md` files — use cases, acceptance criteria, functional + non-functional requirements, edge cases, failure states, inputs, outputs.
- **Preferred format:** Use Cases + Acceptance Criteria (not bare user stories).
- **Spec-Driven Development:** the spec is the *executable source of truth* for AI generation, not just a document:
  - **Generation contract** — every AI build task cites the UC-ID + acceptance criteria it implements. AI generates only from spec artifacts (problem brief, use cases, contracts, architecture note), never from chat memory.
  - **Machine-checkable acceptance criteria** — Given/When/Then wherever possible, so each criterion maps to a test or a scripted check.
  - **Spec-delta rule** — a code change that alters behavior without a matching spec update raises an 🟠 item at the VERIFY gate. Code never silently outruns the spec.
  - **UC-IDs** — `UC-<NN>`, allocated sequentially per project, never reused after deletion, referenced in tasks, commits, and tests.
- **Entry:** PROBLEM gate green/orange. **Exit:** main use cases clear; acceptance criteria exist; failure states named; I/O known; behavior verifiable.
- **Red flags:** no acceptance criteria; happy-path only; AI wrote it unreviewed; vague requirements; code merged whose behavior the spec doesn't describe.
- **Backtrack:** PROBLEM. **Next:** ARCHITECTURE.

### 5.4 ARCHITECTURE
- **Goal:** define system shape before the codebase grows.
- **Question:** what are the main parts and how do they interact?
- **Minimum output:** `architecture_note.md`, data model, storage decision, external deps, deployment target, security/privacy notes, ≥1 ADR (`adr.md`), known tradeoffs, `infrastructure_note.md` (§11.1).
- **Diagrams:** UML-lite only — diagram only what would confuse or break.
- **Entry:** SPEC gate green/orange. **Exit:** components named; data model exists; externals identified; deploy target known; major decisions in the ADR log; tradeoffs visible.
- **Red flags:** no data model; no deploy target; external APIs not isolated; stack chosen without reasoning; over- or under-built.
- **Backtrack:** SPEC. **Next:** MODULE DESIGN (Serious+) or VERTICAL SLICE (Slim).

### 5.5 MODULE DESIGN
- **Goal:** prevent spaghetti.
- **Question:** what modules exist, what are they responsible for, what are their contracts?
- **Minimum output:** module map, `module_contract.md` per critical module, dependency map, failure behavior per module, test responsibilities.
- **Default layers:** UI → Use Case → Domain → Infrastructure/Adapters → Persistence.
- **Contract-first rule:** for critical modules, the contract is written *before* implementation — it is the prompt boundary handed to worker agents (§10.6). No critical-module code generation without its contract.
- **Dependency direction rule:** imports point inward toward domain. UI and adapters are never imported by domain; domain imports nothing above it. Checked at the VERIFY gate ("no new cross-layer imports").
- **Entry:** ARCHITECTURE gate green. **Exit:** modules named; single responsibility each; I/O declared; dependencies visible; critical modules have contracts; layers separated.
- **Red flags:** module does everything; feature has no owning module; business logic in UI; DB calls scattered; shared types missing; no per-module test strategy.
- **Backtrack:** ARCHITECTURE. **Next:** VERTICAL SLICE.

### 5.6 VERTICAL SLICE
- **Goal:** choose the smallest useful version — one thin end-to-end path through all layers.
- **Question:** what is the smallest thing I can ship that proves value?
- **Minimum output:** `vertical_slice.md` — scope, out-of-scope, must/should/could/won't, critical path, manual fallback, definition of done, first user/tester, release target, **effort estimate**.
- **Prototype-as-evidence (v4.5):** when a spec question can be answered faster by a
  one-hour throwaway prototype than by another planning page, build the prototype —
  it is spec *input*, logged as a Spike-tier probe, and it never graduates to
  production code without passing GO like everything else.
- **Entry:** ARCHITECTURE (and MODULE DESIGN for Serious+) green. **Exit:** slice small; out-of-scope generous; DoD clear; critical path known; manual fallback defined.
- **Red flags:** too many features; building infra before proving value; no out-of-scope list; nice-to-haves treated as core; first version untestable.
- **Backtrack:** PROBLEM. **Next:** 🚦 GO / NO-GO, then BUILD.

### 5.7 🚦 GO / NO-GO GATE
Before opening the editor, complete `GO_CRITERIA.md` (every box checked or explicitly
justified), pass the Planning Validation Gate, and — Serious+ — run the premortem. See §6.

### 5.8 BUILD (with continuous verification)
- **Goal:** implement the slice with traceability and proof as you go.
- **Question:** am I building the specified slice, in the planned modules, proving it works?
- **Minimum output:** build tasks (`task.md`) linked to requirements/use-cases/modules, implementation notes, known issues, AI session logs (`ai_session.md`), continuous test results, commit notes.
- **Continuous verification means:** every business-logic task gets a test in the same session; every AI implementation gets a manual run-through before commit; acceptance criteria checked at task close; failures land in the Failure Log the moment they happen.
- **Build rules:** one task verifiable in one sitting; every task connects to a use case/module/stage; every AI output reviewed before merge; every shortcut becomes a Known Issue or Decision Log entry; every commit references the task; **the review budget (§9) is respected — no new generation while at the unreviewed-work cap.**
- **Entry:** GO gate passed. **Exit:** slice tasks implemented; code maps to requirements; module boundaries mostly respected; known issues documented; AI code reviewed.
- **Red flags:** tasks not linked to spec; AI output pasted unreviewed; one file ballooning; duplicate logic; UI holding business rules; DB calls everywhere; no error/loading/empty states; **a queue of unreviewed diffs growing while you dispatch more work.**
- **Backtrack:** MODULE DESIGN (boundaries crumble) or SPEC (behavior misunderstood). **Next:** VERIFY gate.

### 5.9 VERIFY GATE
- **Goal:** prove the software behaves correctly against the spec.
- **Question:** does it work according to the acceptance criteria?
- **Minimum output:** test plan (`test_plan.md`), manual QA checklist, acceptance results, regression checklist, bug reports, failed-task recovery notes, edge-case results.
- **Testing pyramid (solo):** unit (pure domain), integration (adapters touching real systems), one or two e2e on the critical path, manual QA against a written checklist for the rest.
- **Exit:** critical flows tested; acceptance criteria checked; edge cases reviewed; failed tasks resolved or accepted; limitations recorded.
- **Red flags:** happy-path only; no acceptance check; failed tasks unresolved; no regression after changes; "seems to work"; never tested with production-like data.
- **Backtrack:** BUILD (fix) or SPEC (criteria were wrong). **Next:** HARDEN gate.

### 5.10 HARDEN GATE
- **Goal:** confirm readiness for production reality. A checklist against an already-tested build, not a dev phase.
- **Minimum output:** production readiness checklist (`production_readiness.md`) — error handling, logging/observability, security review, privacy review, performance budget, backup/export, rollback, env vars, deployment. Concrete minimums in §11.
- **Exit:** errors handled; logs debuggable; sensitive data protected; env vars documented; deploy process known; rollback exists; critical risks accepted or resolved.
- **Red flags:** no rollback; no logs; no error states; exposed secrets; no env checklist; no backup; no privacy review; no production-like deploy test.
- **Backtrack:** BUILD (each unchecked item is a build task). **Next:** SHIP.

### 5.11 SHIP
- **Goal:** release a usable version.
- **Minimum output:** `release_notes.md`, deployment record, version tag, known limitations (`known_limitations.md`), post-ship checklist, rollback instructions, **retro (§23.2)**.
- **Exit:** deployed/published; release documented; limitations visible; rollback exists; observation tasks created; retro written.
- **Red flags:** no release notes or rollback; unresolved critical failures; no deployment record; no observation plan.
- **Backtrack:** HARDEN. **Next:** OBSERVE.

### 5.12 OBSERVE
- **Goal:** learn from the shipped product.
- **Minimum output:** `observation_entry.md` files — feedback log, bug log, usage notes, monitoring notes, refactor candidates, next-iteration backlog, lessons learned.
- **Exit:** feedback captured; bugs tracked; refactor needs identified; next iteration planned from evidence; lessons recorded; kill/pause/continue decision logged.
- **Red flags:** no feedback; bugs in memory only; no monitoring; refactor debt ignored; next features picked from excitement.
- **Backtrack:** none. **Next:** new iteration (→ PROBLEM or SPEC), MAINTAIN (§12.1), or archive.

---

## 6. Quality Gates

A gate is checked at the end of a stage. Severities:

- 🔴 **RED (blocker):** cannot advance. Resolve before the next stage.
- 🟠 **ORANGE (warning):** advance with an explicit override note in the Decision Log; visible until resolved; expires.
- 🟡 **YELLOW (advisory):** surfaced for awareness; does not block.

**The authoritative per-stage gate-item lists live in `methodology.v4.yaml` under
`gates:`** — the dashboard renders them; this document no longer duplicates them.
Two framing rules apply to all of them:

- **Evidence, not assertion.** Gate items are phrased as *evidence to record* ("CI run
  link recorded"), not states to assert. Where the dashboard can't verify the evidence
  (§24), pasting it is still on you — Law 1.
- **Catches get logged.** When a gate or checklist item surfaces a real defect, log it
  (§23.1). That's how the item earns its keep under Law 4.

### 6.1 GO CRITERIA (the human gate)

`GO_CRITERIA.md` is the one-page hard checklist you complete before opening the editor:
problem clarity, behavior clarity, shape clarity, module clarity, scope clarity, AI
readiness, infrastructure readiness, risk & failure readiness. Every box checked, or a
documented reason for proceeding without it. It ends with the harsh-rule sentence read
aloud (§21).

### 6.2 Premortem (Serious+, advisory for Slim) — *new in v4.5*

The gates check that planning artifacts are complete and consistent. Nothing checks
that they are *true* — a beautifully complete wrong spec sails through. So before GO,
run one adversarial pass: **"It is three months from now and this project failed.
Write the post-mortem."** Ten minutes, AI-assisted is fine (it's good at this — §10.2).
Any failure mode the plan can't answer becomes a risk entry or a spec fix. This is
the only gate that argues *against* the plan.

### 6.3 Planning Validation Gate (the automated gate)

A **meta-gate** at the planning → execution boundary, validating that every prior
stage is complete *and* internally consistent. Fires when the user attempts BUILD;
can be run manually anytime. Its 12 checks (definitions in `methodology.v4.yaml`
`planning_validation_gate:`): stage-completion roll-up · gate roll-up · skeleton-task
roll-up · custom-task roll-up · AI-session review roll-up · artifact review roll-up ·
cross-stage consistency (every use case has an owning module, every criterion belongs
to a use case, no orphans) · risk check · Decision Log presence · planning DoD
composed · tier-specific artifacts · agent-run review roll-up.

**Outcome:** all 🔴 pass → **GO**. Any 🔴 fails → **NO-GO** until resolved. Only 🟠/🟡
fail → GO with logged override. The report saves to
`docs/00_meta/planning-validation-<date>.md`. Re-run when a planning stage is re-entered.

*(v4.5: the Decision Log check is presence-based in doctrine — a log with honest
entries, not a count. The dashboard still enforces ≥3 until phase 2; see §24.)*

### 6.4 Override mechanics

To advance past an 🟠 item, record an override (`override` entry in the Decision Log):
`Override · Stage · Reason · Acceptance (who acknowledges) · Expiry (default +14 days) · Linked decision`.
Overrides expire and re-block. 🔴 items cannot be overridden, only resolved.
Overrides are also instrumentation: at retro, items overridden every project are
eviction candidates (Law 4) — or the tier calibration is wrong.

---

## 7. Risk Radar

The 18-risk catalog with default severities lives in `methodology.v4.yaml`
`risk_radar:`. Record risks with `risk_entry.md`. **Accepted risks must have an
expiry**; when it passes, the risk re-opens automatically.

---

## 8. Failure Log + Backtrack Rules

Every failed task, test, AI output, assumption, integration, deployment, or
architecture decision is logged with `failure_log_entry.md` **the moment it happens**.
The dashboard suggests a backtrack target by failure category (mapping in
`methodology.v4.yaml` `backtrack_rules:`); the user can override.

*(v4.5)* Each failure entry also records, when known: `caught_by:` (the gate/checklist
item or test that caught it) or `missed_by:` (the stage that should have). One line.
This is the raw material for §23.

---

## 9. Review Budget — *new in v4.5*

Law 2 says unreviewed AI output does not exist. Then treat it like what it is:
**inventory, not progress.** Generation that outruns review is negative work — it
piles up risk you will misjudge later under time pressure.

1. **The cap.** At most **2 unreviewed worker diffs / agent runs** open per project at
   any time (pending `ai_session` reviews count toward it). At the cap, the next
   action is *review*, not dispatch. The cap is a per-project property; raise it only
   with a logged override — and if you keep raising it, the finding is that you are
   the bottleneck, which is the point.
2. **Don't generate what you can't verify this week.** Before dispatching a task, name
   how and when its output gets verified (the task's verify command / checklist slot).
   No named verification = not ready to dispatch.
3. **Review is scheduled work.** The daily loop (§18) starts with the review queue,
   not with new generation. Review time is a first-class task, not a gap-filler.
4. **The PVG already enforces the floor:** pending AI-session and agent-run reviews
   block GO. The cap extends the same principle into BUILD, where the pile actually
   grows.

---

## 10. AI Stage Layer

AI is a participant at every stage. Treat it as a junior developer with infinite energy,
perfect recall of the wrong things, and zero context unless you provide it.

### 10.1 Context-Loading Protocol
Before any non-trivial AI generation, the AI must have read, in order: (1) Problem Brief, (2) relevant Use Case + Acceptance Criteria, (3) relevant Module Contract, (4) Architecture Note, (5) current Decision Log, (6) relevant Failure Log entries. If you cannot point the AI at these, you are not ready to generate code.

### 10.2 AI usage per stage (good at / dangerous at)
Capture: reformulating / inventing scope. Problem: pushing back on vague problems / accepting your framing. Spec: generating use & edge cases / inventing plausible requirements. Architecture: options + tradeoffs / picking shiny tech. Module Design: drafting contracts / coupling silently. Vertical Slice: cutting scope / "while we're at it" features. Premortem: imagining failure modes / inventing implausible ones. Build: boilerplate, adapters, tests / business logic without verification. Verify: edge-case tests / tests that always pass. Harden: checklists, security review / hallucinating compliance. Ship: release notes / overstating changes. Observe: pattern recognition / inventing sentiment from one comment.

### 10.3 Validation rules for AI output
Before merging: (1) contract check, (2) boundary check (no silent cross-layer calls), (3) hallucination check (imports/APIs exist), (4) test check (a test that would fail if the AI got it wrong), (5) trace check (link to a use case/requirement), (6) diff check (no unrequested changes). Any "I'm not sure" = **no**, don't merge.

### 10.4 Anti context-rot
For long sessions (>30 min or >10 turns): pause and ask the AI to summarize state, decisions, open questions. If the summary surprises you, it has drifted — restart with fresh context. Never let a session cross a stage boundary without a checkpoint. Log every tool call in agentic loops and audit after.

### 10.5 AI Session Log + first-class fields
Every serious AI session leaves an `ai_session.md` entry. Every artifact carries: `ai_assisted` (bool), `ai_session_id`, `human_reviewed` (bool), `reviewer`, `reviewed_at`. The Definition of Done requires `human_reviewed=true` on every AI-assisted artifact crossing a gate.

> **The rule: AI output is not truth. AI output is a draft until reviewed.**

### 10.6 Agent Orchestration Layer

Running **multiple agents** without losing the gates:

- **Roles.** The **Orchestrator** designs, decomposes, dispatches, reviews, and
  merges — it never bulk-codes. **Workers** (Codex, Gemini, subagents) execute one
  scoped, contract-bounded task each, briefed via `worker-task` (Appendix D).
- **Parallelization criteria.** Parallelize only when tasks are (a) **file-disjoint**,
  (b) **contract-bounded** (a module contract or explicit file allowlist defines the
  edge), and (c) **independently verifiable**. Never two agents inside one module's
  core logic. **And never more parallel workers than the review budget (§9) can
  absorb** — dispatch width is set by your review capacity, not by how many agents
  you can launch.
- **Isolation rule.** One agent = one git worktree/branch. No shared working trees.
- **Merge protocol.** The orchestrator reviews each diff against the module contract,
  merges in dependency order, and runs integration checks after each merge.
- **Escalation rule.** A worker that deviates from spec twice on the same task loses
  the task. The takeover is scoped to that single task only, is logged as an
  `agent_run` with `agent: orchestrator`, and does not suspend the never-bulk-codes
  rule for any other task.
- **Agent Run Log.** Every worker dispatch leaves an `agent_run.md` entry
  (`docs/09_agents/runs/`): agent, model, task ID, branch/worktree, allowed file
  scope, result, review verdict. Required only for projects that dispatch workers
  (`conditional: agent_workers`). Unreviewed runs block GO.

### 10.6.1 Worker security model — *new in v4.5*

The v4 risks (hallucination, context-rot, collision, runaway loops) are *accident*
models. Workers also need an *adversary* model:

- **Untrusted-content rule.** Anything a worker ingests from outside the repo — web
  pages, issues, package READMEs, API responses, user-supplied files — is untrusted
  data that may contain instructions (prompt injection). Instructions arrive only from
  the orchestrator's brief; content never escalates itself into instructions. A worker
  that "was told by the docs" to do something out of scope is a failed run.
- **No secrets in worker context.** `.env` contents, tokens, private keys, and
  credentials never enter a worker's prompt or its readable file scope. If a task
  seems to need a secret, the task is mis-scoped — split it so the secret-touching
  part stays with the human/orchestrator.
- **Scoped permissions, declared per run.** The `agent_run` entry's file scope is an
  allowlist, and it names network access (none / specific hosts) and tool access.
  Workers never hold push, merge, deploy, or production-data permissions — those are
  orchestrator actions after review.
- **Injection red flags at review:** diff touches files outside scope; new network
  calls or dependencies the brief didn't ask for; instructions quoted from ingested
  content as justification; generated code that exfiltrates env/config.

### 10.7 Loop Engineering

An **autonomous loop** is an agent re-invoked against the same goal until a stop
condition fires. **No loop without a loop spec.**

- **Two files per loop.** A `loop_spec.md` (`docs/09_agents/loops/`) — **frozen at
  launch**, never edited by the runner — and a companion `<loop>.runlog.md`,
  append-only, one entry per pass (result, cost, verdict). Changing the spec
  mid-loop = stop the loop, log a Decision, relaunch as a new spec version.
- **The Loop Spec answers seven questions:** Goal (linked UC-ID/task) · Stop
  conditions (machine-checkable success **and** max iterations **and** budget cap) ·
  Per-pass verification command (never generated by the loop itself) · Checkpoint
  cadence · Context strategy (fresh-per-pass vs accumulated, with a rot-reset rule)
  · Escalation triggers · Kill switch (a command, not a hope).
- **Required only for projects that run loops** (`conditional: loops`).
- **Red flags:** no verifiable stop condition; the loop grading its own homework;
  unbounded budget; a loop crossing a stage boundary without a checkpoint; the runner
  editing its own spec or budget.

---

## 11. DevOps & Infrastructure Layer

### 11.1 Infrastructure Note

Every Slim+ project writes an **Infrastructure Note** (`infrastructure_note.md` →
`docs/03_architecture/infrastructure.md`) at ARCHITECTURE: Deploy target ·
Environments & env vars · CI pipeline · Secrets handling · Backup & restore ·
Monitoring & alerts · Cost ceiling. Slim may mark non-applicable headings `n/a`
with a one-line reason. Checked at the Architecture Gate (🟠, 🔴 Serious+).

### 11.2 Tier-scaled infrastructure minimums

This table is the **authoritative minimum**. The practices in §11.3 are the default
expectation for Serious and Mission-critical; for Spike and Slim this table governs
and the practices are advisory.

| Tier | Infrastructure minimum |
|---|---|
| **Spike** | Git. Nothing else. |
| **Slim** | Deploy script/steps documented · env var list · a backup path |
| **Serious** | + CI on every PR (lint, typecheck, tests, build) · uptime check · restore tested at least once |
| **Mission-critical** | + staging environment · error tracking · incident-response note |

### 11.3 Engineering practices

- **VCS hygiene:** `main` always deployable; short-lived branches; PR even when solo; conventional commits referencing the task; one logical change per commit; AI-assisted commits tagged in the body; `.gitignore` covers `.env`, build dirs, IDE/OS files.
- **Secrets:** never in git history, ever. `.env.example` with placeholders committed; real `.env` gitignored; pre-commit secret scanner (`gitleaks`/`trufflehog`); rotation plan; on leak — rotate, purge history, audit access.
- **Dependencies:** lockfiles committed; security audit before each release (`npm audit`, `pip-audit`); pin majors; a new dependency = a Decision Log entry.
- **CI/CD (minimal):** every PR runs lint, typecheck, tests, build (+ optional secret scan); CD is a documented scripted path ("run `vercel --prod`" counts; "I remember the steps" does not).
- **Migrations:** every schema change is a committed, reversible migration; never edit an applied migration; back up before migrating production.
- **Performance budgets (concrete):** set numbers at HARDEN. Defaults — API p95 < 300 ms; page LCP (4G) < 2.5 s; initial bundle < 200 KB gzipped; < 5 DB queries on the critical path.
- **Observability minimum:** structured logs with severity + request IDs; error tracking (Sentry/Logfire); ≥1 uptime/health check; one key business metric.
- **Accessibility & i18n:** keyboard nav on critical flows; WCAG AA contrast; labelled fields; locale decided and written down; locale-aware date/number formatting.
- **Docs that survive you:** `README.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, and `docs/`. A future-you (or client) can run the project and understand its shape in one hour.

---

## 12. Kill / Pause / Continue / Maintain

Every project has explicit abort criteria (in the Problem Brief), reviewed at every gate.

- **Kill if:** the original problem no longer exists; you've spent **3× the original effort estimate** and the slice still hasn't shipped; the core assumption was wrong; a blocking dependency disappeared.
- **Pause if:** no clear next action for >1 week; a higher-priority project demands your attention; you're blocked on something you can't get yet (legal, partner, data).
- **Continue if:** the problem is still real; you can name the next concrete action; overrun is <3× and trending down.

Log the decision in the Decision Log. Killing a project is not failure — keeping a
dead project on the active list is. **A kill still gets a retro (§23.2)** — killed
projects are the cheapest methodology evidence you will ever collect.

### 12.1 MAINTAIN mode — *new in v4.5*

Kill/Pause/Continue covers pre-ship. The real solo failure mode is post-ship:
**shipped and quietly rotting** — a project with users, stale dependencies, and no
owner attention. A shipped project with no active iteration is explicitly in
**MAINTAIN**, and MAINTAIN has a pulse:

- **Cadence:** Serious & Mission-critical — quarterly. Slim with users — twice a year.
  Slim single-user / Spike — none (archive instead).
- **The pulse (≤1h):** dependency security audit (`npm audit`/`pip-audit`) · backup
  still runs + spot-restore · uptime/error check · one line in the project's
  observation log · **keep / iterate / sunset decision.**
- A pulse that keeps getting skipped *is* the sunset decision — make it honestly (Law 1).

### 12.2 Sunset procedure — *new in v4.5*

Retiring a shipped project is a first-class outcome, not abandonment:
final release note (announces end-of-life, points to alternatives) · data export path
for any user · archive README (what it was, why retired, how to resurrect) · teardown
checklist (domains, hosting, cron jobs, API keys — rotated/cancelled) · repo archived ·
retro written. A sunset done in an afternoon beats a zombie maintained by guilt.

---

## 13. Health Score (stage-aware)

A 0–100 score per project; category scores 0–10, weighted by current stage so the
score reflects what matters *now*. **The weight matrix lives in `methodology.v4.yaml`
`health_weights:`** (dashboard implementation detail — it doesn't belong in your head).

What belongs in your head is the **warnings** the score exists to surface: "high
missing-spec risk" (spec < 4 at SPEC+) · "building before architecture is clear"
(BUILD with arch < 5) · "shipping before verification complete" (SHIP with verify < 7)
· "unresolved failed tasks" (recovery < 5) · "no rollback plan" (HARDEN/SHIP) · "no
module contracts for critical logic" (BUILD, Serious+).

Agent and loop work needs no new categories: it scores through **task execution**
(dispatched tasks completing against their briefs) and **failed-task recovery**
(rejected runs and stopped loops logged and resolved).

---

## 14. Next Action Engine

One "what should I do next?" string per project, by priority: (1) review queue at or
over the budget cap (§9), (2) open gate items (🔴 first, then 🟠 expiring soonest),
(3) open failed tasks (with backtrack), (4) AI sessions with `human_reviewed=false`,
(5) accepted risks past expiry, (6) tasks blocked >7 days.

---

## 15. Fast Lane

For trivial work that doesn't deserve the full lifecycle — single-file bug fix,
copy/typo, dependency bump, config tweak, doc-only change. Requires only: a one-line
task with reason; a Decision Log note if user-visible; a test or manual check that the
fix doesn't regress the critical flow; a commit linked to the task. The Fast Lane is a
per-project property; early-stage projects may have none.

---

## 16. Iteration Loop

After SHIP + OBSERVE a project enters its next numbered iteration (v1.0 → v1.1 → v2.0).
Each iteration has its own current stage (PROBLEM if scope changed, SPEC if only
behavior changed), inherits artifacts but can supersede them, and has its own health
score. The dashboard shows the active iteration; previous iterations are read-only.

---

## 17. Definition of Started + Done

**Started:** entry criteria met (or overrides logged) + user explicitly starts the
stage + first task `In Progress`. Prevents auto-advance.

**Feature done** *(items not already covered by the Verify/Harden gates)*: maps to a
use case with passing acceptance criteria and an owning module; no `TODO/FIXME/XXX`
without a linked Known Issue; no secrets in the diff; no AI code merged without a
logged session; known limitations documented.

**Release done:** Verify + Harden gates green or overridden; release notes exist;
rollback path *walked through*, not just written; observation tasks created; version
tagged; deployment reproducible from docs; retro written; (Mission-critical) peer
review recorded.

---

## 18. Operating Loops

**Daily:** open Mission Control → pick one active project → **work the review queue
first (§9)** → read current stage + next action → check blockers/failed tasks/expiring
overrides → work one small task → log AI use → update task status → record failures
immediately → update next action. Don't end a session without updating status, logging
blockers, recording decisions, noting next action.

**Weekly:** review all active projects → pause anything without a clear next action →
archive dead Spikes → check unresolved failed tasks → check high-severity risks →
reduce scope where needed → resolve/extend expiring overrides → pick one project to
advance toward shipping.

**Per ship or kill:** write the retro (§23.2), append its findings to the evidence
ledger (§23.3).

**Quarterly:** run the MAINTAIN pulse (§12.1) over every shipped, non-iterating project.

---

## 19. Folder Structure

Canonical per-project layout (the dashboard reads these paths):

```
/<project>
├── README.md  ARCHITECTURE.md  CHANGELOG.md  .env.example  .gitignore
└── /docs
    ├── 00_meta/            planning-validation-<date>.md, go-criteria.md, retro.md
    ├── 01_problem/         problem.md
    ├── 02_spec/            spec.md, use-cases/*.md
    ├── 03_architecture/    architecture.md, infrastructure.md, decisions/*.md (ADRs)
    ├── 04_modules/         *.md (module contracts)
    ├── 05_vertical_slice/  slice.md
    ├── 06_verification/    test-plan.md, qa-checklist.md, acceptance.md
    ├── 07_release/         release-notes.md, known-limitations.md
    ├── 08_observation/     *.md
    ├── 09_agents/          runs/*.md (agent runs), loops/*.md (loop specs + runlogs)
    ├── decisions.md  failures.md  risks.md
    └── 99_ai-sessions/     *.md (one per session)
```

`/src` layout per stack — see appendices.

---

## 20. Minimum Artifact Set per Tier

- **Spike:** raw idea note · problem one-liner · vertical slice (one paragraph) · informal module notes · **retro note** (the post-mortem, §23.2 — same thing).
- **Slim:** Problem Brief · light Product Spec (≤3 use cases w/ acceptance criteria) · Architecture Note (merged module map) · Infrastructure Note (n/a headings allowed) · Vertical Slice · test checklist · Release Notes (one page) · project logs · AI Session Log · **retro**.
  - *(v4.5)* Slim may keep Decision + Risk + Failure logs as **one** `docs/log.md`
    with typed entries (`decision:` / `risk:` / `failure:`) instead of three files —
    same information, less ceremony. Serious+ keeps them separate. (Dashboard
    scaffolds still create three files until phase 2 — §24.)
- **Serious:** all of Slim (separate logs), plus use cases for every critical flow · module contracts for every domain module · ADRs for every major choice · production readiness checklist · backup/rollback plan · observation plan · performance budgets.
- **Mission-critical:** all of Serious, plus threat model · privacy review document · peer review / independent verification record · on-call / incident response plan · audit log of who reviewed each gate.
- **Conditional (any tier):** projects that dispatch worker agents add Agent Run Logs; projects that run autonomous loops add Loop Specs + runlogs (§10.6–10.7).

---

## 21. The Harsh Rule

If you cannot explain — what problem it solves, what behavior it must have, what module
owns it, how it fails, how to verify it, how to ship it safely, and what would make you
kill it — then you are not ready to build that feature yet. You can still prototype. But
do not pretend it is production-ready software.

---

## 22. What this system is NOT

Not Jira. Not fake-Agile theater. Not documentation-for-its-own-sake. Not a hard-block
system (warnings are visible, overrides are logged, the human owns the call). Not
opinionated about your stack (the folder structure is a suggestion). Not a substitute
for code review (AI session logging complements, never replaces, reviewing AI code).
And not metrics theater: the instrumentation in §23 is a handful of one-line tags and
a one-page retro — if it ever needs a spreadsheet, it has failed its own test.

---

## 23. Instrumentation — the road to v5 *(new in v4.5; the point of this release)*

The methodology has an OBSERVE stage for products but, until now, none for itself.
Every version so far was written from taste. v5 will be written from the evidence
this section collects. The cost budget for all of it: **one-line tags during work +
one page per project at the end.**

### 23.1 What gets recorded (reusing existing logs — no new ritual)

1. **Catches.** A gate/checklist item surfaces a real defect → the Failure Log entry
   gets `caught_by: <stage>/<item>` (§8).
2. **Misses.** A defect reaches VERIFY or production that an earlier stage should have
   caught → `missed_by: <stage>`.
3. **Overrides.** Already in the Decision Log (§6.4). At retro, count them per item.
4. **Estimate vs actual.** The estimate already exists (Problem Brief, Vertical
   Slice). Record actual hours at ship/kill. The kill criterion (3×, §12) already
   depends on this number — now it also feeds calibration.
5. **Process overhead.** Rough hours spent on methodology artifacts and rituals,
   recorded once at retro. Targets, measured not enforced: **Slim ≤ ~10% of project
   hours, Serious ≤ ~15%.** Over budget = the methodology owes you a cut, not the
   other way around.

### 23.2 The Retro (per project, at SHIP or kill)

One page, `docs/00_meta/retro.md` (template: `retro.md`, prompt:
`prompts/retro-writer.md`): outcome · estimate vs actual · what the process caught ·
what it missed · what was rubber-stamped (checked without thought) · process overhead
· **the one rule to change.** A Spike's post-mortem note *is* its retro — same
artifact, smaller.

### 23.3 The Evidence Ledger (cross-project)

Retro findings append to **`methodology/EVIDENCE.md`** — the accumulating v5 problem
brief. Lessons stop dying inside per-project folders.

**Rule-eviction mechanics (Law 4):** at the v5 review, every gate item and every rule
in this document must show, in the ledger, **at least one catch or one named
near-miss**. A rule with zero evidence across all retros is deleted or demoted to 🟡
by default — keeping it requires the same thing removing it used to: an argument.
Items overridden in nearly every project get re-tiered or deleted. This is the only
mechanism preventing v5 from being v4.5 plus more layers.

### 23.4 Definition of v5-ready

v5 gets written when the ledger holds **≥3 completed retros** (any mix of shipped and
killed, at least one Serious). Not before — a rewrite earlier than that is taste again.

---

## 24. Enforcement status (honesty table)

Law 1 applied to the methodology itself — what the dashboard enforces by code today
vs. what remains a manual or document-level contract:

| Mechanism | Today | Phase 2 |
|---|---|---|
| Artifact presence + required headings | ✅ enforced | — |
| Tier filtering of stages/gates | ✅ enforced, including `applies_to` and `min_count_tiers` | — |
| Verify gate red items ("critical flows tested", "acceptance criteria checked") | ✅ evidence-backed by the merge gate (verify command + per-criterion conformance trace) | — |
| Other v4 gate items | ⚠️ manual checklist items (heading/token matching, not instrumented) | optionally instrument (CI status, restore evidence) |
| `conditional:` artifacts (agent runs, loop specs) | ✅ enforced; `n_a` until the capability is used | — |
| PVG check 12 (`agent_run_review_rollup`) | ✅ enforced as blocking | — |
| PVG check 9 — doctrine is presence-based (v4.5) | ⚠️ dashboard still checks ≥3 decisions | relax to presence |
| Review budget cap (§9) | ❌ discipline | count open unreviewed runs/sessions; block dispatch at cap |
| `caught_by:`/`missed_by:` failure tags (§23.1) | ❌ discipline (free-text fields in the template) | parse + aggregate into the ledger |
| Retro artifact (§23.2) | ⚠️ template ships; not in the YAML manifest — dashboard doesn't scaffold or track it | add to manifest + Ship gate 🟠 |
| Evidence ledger (§23.3) | ❌ manual append | auto-append from parsed retros |
| Slim merged project log (§20) | ❌ dashboard scaffolds three logs | merged-log support |
| MAINTAIN pulse (§12.1) | ❌ discipline (calendar reminder) | dashboard surfaces due pulses |
| Worker security scopes in `agent_run` (§10.6.1) | ⚠️ recorded free-text in the template | validate scope fields |
| Prompt frontmatter (`inputs` preload) | ❌ orchestrator discipline | parsed validation |
| Agent Ops dashboard section | ✅ views and manifest-driven scaffolds built | — |

---

## APPENDIX A — Next.js stack `/src`

```
/src
├── /app          routes & pages (App Router)
├── /components   reusable presentational components
├── /features     feature-scoped UI + orchestration
├── /domain       entities, rules, validation (pure, zero framework imports)
├── /use-cases    application workflows
├── /server       server actions, API routes
├── /adapters     external API wrappers, parsers, DB clients
├── /db           schema, migrations, queries
├── /lib  /types  shared utilities & types
└── /tests        /unit /integration /e2e
```
Server actions in `/server` (never `/components`); DB queries in `/db`/`/adapters`; `/domain` pure TS; Zod at trust boundaries; `strict: true`, no `any` without a comment. Tooling: ESLint + Prettier, Vitest/Jest, Playwright, Husky + lint-staged.

## APPENDIX B — FastAPI stack `/src`

```
/src
├── /api          routers, request/response models (thin)
├── /use_cases    application workflows
├── /domain       entities, value objects (zero FastAPI/SQLAlchemy imports)
├── /adapters     external clients, parsers, gateways
├── /repositories persistence (returns domain entities, not ORM rows)
├── /db           SQLAlchemy models, Alembic migrations
├── /core         config, logging, deps, security
├── /schemas      Pydantic DTOs
└── /tests        /unit /integration /e2e
```
Routers validate → call a use case → return; domain is framework-free; Alembic from day one (even SQLite); env loaded only in `/core`. For LLM/agentic projects: wrap every LLM call behind `/adapters/llm/`; log prompt + response (PII-redacted); explicit timeouts/retries; hard token cap per request.

## APPENDIX C — Template index

All templates live in `templates/`, designed to be copied into a project's `docs/`.
Destination paths and required headings per artifact are in `methodology.v4.yaml`.

| File | Purpose / stage |
|---|---|
| `GO_CRITERIA.md` | The GO / NO-GO one-page gate |
| `capture.md` | CAPTURE — raw idea note |
| `problem_brief.md` | PROBLEM |
| `product_spec.md` | SPEC |
| `use_case.md` | SPEC — one use case + acceptance criteria |
| `architecture_note.md` | ARCHITECTURE |
| `infrastructure_note.md` | ARCHITECTURE — infra layer |
| `adr.md` | ARCHITECTURE — decision record |
| `module_contract.md` | MODULE DESIGN |
| `vertical_slice.md` | VERTICAL SLICE |
| `task.md` | BUILD — traceable task |
| `test_plan.md` | VERIFY — test plan / QA checklist |
| `production_readiness.md` | HARDEN — readiness checklist |
| `ai_session.md` | AI session log entry (cross-cutting) |
| `agent_run.md` | Agent run log entry (cross-cutting) |
| `loop_spec.md` | Loop spec + companion runlog (cross-cutting) |
| `decision_log_entry.md` | Decision Log entry (cross-cutting) |
| `failure_log_entry.md` | Failure Log entry (cross-cutting) |
| `risk_entry.md` | Risk Radar entry (cross-cutting) |
| `release_notes.md` | SHIP |
| `known_limitations.md` | SHIP — honest limitations list |
| `observation_entry.md` | OBSERVE |
| `retro.md` | SHIP / kill — methodology retro *(v4.5)* |

---

## APPENDIX D — Prompt library index

Reusable prompts live in `prompts/`, one file each, with frontmatter: `id`, `stage`,
`agent` (who fires it), `inputs` (artifacts that MUST be loaded first — the
Context-Loading Protocol §10.1, made mechanical), `output` (artifact produced).

> Prompts are part of the methodology. Logging a prompt improvement as a Decision is
> **advisory** (v4.5): nothing parses or enforces it (§24), and pretending otherwise
> violated Law 1. Meaningful prompt changes that alter what an artifact contains are
> still worth a Decision line.

| Prompt | Stage / layer | Produces |
|---|---|---|
| `problem-interrogator.md` | PROBLEM | problem brief draft — pushes back on vague problems |
| `spec-writer.md` | SPEC | product spec + use cases with Given/When/Then ACs and UC-IDs |
| `architecture-options.md` | ARCHITECTURE | 2–3 options w/ tradeoffs, data model, ADR drafts |
| `module-contractor.md` | MODULE DESIGN | module map + per-module contracts |
| `slice-cutter.md` | VERTICAL SLICE | smallest end-to-end slice, generous out-of-scope, DoD |
| `verify-qa.md` | VERIFY | test plan + edge cases derived from acceptance criteria |
| `harden-auditor.md` | HARDEN | production-readiness review against the checklist |
| `observe-synthesizer.md` | OBSERVE | feedback synthesis → next-iteration backlog |
| `retro-writer.md` | SHIP / kill | the one-page methodology retro (§23.2) |
| `orchestrator-decompose.md` | Agent Orchestration | slice → file-disjoint, contract-bounded worker tasks |
| `worker-task.md` | Agent Orchestration | the standard worker briefing |
| `merge-reviewer.md` | Agent Orchestration | diff verdict vs module contract + spec-delta check |
| `loop-pass.md` | Loop Engineering | one loop pass: increment → verify → runlog → stop-check |

---

## APPENDIX E — Agent roster (definitions only)

Defined in `agents/agents.v4.yaml` — superficial cards to be implemented later as
Claude Code subagents, Codex profiles, or dashboard-driven dispatch. Schema:
`id · role · default_runtime (claude|codex|gemini|haiku|any) · fallback_runtimes ·
stages · inputs · outputs · prompts · must_not · escalates_to`.

| id | Role | Runtime | Must not |
|---|---|---|---|
| `orchestrator` | Decomposes, dispatches, reviews, merges; owns gates + Decision Log | claude | bulk-code; merge unreviewed diffs; skip gates |
| `spec-writer` | Idea → problem brief + spec + use cases | claude | invent untraceable requirements |
| `architect` | Architecture/infra notes, ADRs, module contracts | claude | pick stack without tradeoffs |
| `builder` | ONE scoped task in an isolated worktree | codex | touch files outside scope; change specs/contracts; merge to main |
| `verifier` | Test plan, acceptance criteria, spec-delta check | claude | verify its own code; weaken criteria |
| `devops` | CI, deploys, backup/restore, monitoring | codex | secrets in repo; deploy without rollback |
| `loop-runner` | One loop pass per invocation, honors stop conditions | codex | run without loop spec; alter own stop conditions/budget |
| `librarian` | Keeps the logs honest and headings current | haiku | rewrite history; close gate items |

Three binding rules: (1) every agent run is logged as an `agent_run.md`; (2) `must_not`
lists are copied **verbatim** into any implementation's system prompt — boundaries are
never re-derived per project; (3) every implementation inherits the worker security
model (§10.6.1).
