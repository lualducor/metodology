---
release: '4.6'
policy:
  red_overridable: false
  decision_log_check: presence
  review_cap: 2
  evidence_revision_required: true
---
# SPEC-GATED MODULAR DELIVERY — v4.6

A standalone method for AI-assisted solo delivery. Start with [the quickstart](README.md)
and use the smallest profile that exposes the project's real risks. No dashboard is
required. [The YAML](methodology.v4.yaml) is canonical for mechanical policy, gate IDs,
tiers and the artifact manifest. Its filename/version denotes schema 4; `release`
identifies this policy release. This document supplies rationale and operating guidance.
The [changelog](CHANGELOG.md) records changes from v4.5.

## 1. Principles

- Keep decisions, limitations and risks understandable to a future maintainer.
- AI output is a draft until a human reviews the relevant revision and its evidence.
- Record justified omissions honestly. Omissions never waive red blockers.
- Evaluate rules using exposure, consequences and cost, as well as catches and misses.
- Protect review capacity. Generating more than you can verify creates unfinished work.

## 2. Choose a tier and route each change

| Tier | Scope | Effort | Required approach |
|---|---|---|---|
| Spike | Throwaway experiment | At most 8 hours | Capture, problem, slice, build, retrospective note; never ship as a Spike |
| Slim | Small single-user tool | At most 40 hours | Full lifecycle with merged design and three documents |
| Serious | Daily use or other users | No fixed cap | Full artifacts, CI, tested restore and explicit module contracts |
| Mission-critical | Money, health, security, regulated data or livelihoods | No fixed cap | Serious plus threat/privacy review, independent verification and incident plan |

Choose by consequences as well as size. Upgrade before exceeding a tier's scope;
backfill required evidence. Downgrade only when the remaining exposure justifies it,
with a recorded reason; never to bypass an unresolved blocker.

**Fast Lane:** a one-line task, relevant check, linked commit and a decision note for
user-visible changes. Use only for small, reversible, low-risk work. Authentication,
permissions, persistent-data changes, public-contract changes, deployment behavior,
or difficult rollback require an explicit impact assessment and the relevant normal
gates. A one-line config change or dependency bump is not automatically low-risk.

## 3. Lifecycle and minimum outcomes

`CAPTURE → PROBLEM → SPEC → ARCHITECTURE/MODULE DESIGN → VERTICAL SLICE → GO → BUILD → VERIFY → HARDEN → SHIP → OBSERVE`

| Stage | Evidence to produce | Backtrack when |
|---|---|---|
| Capture | Idea, pain, possible user | No identifiable problem |
| Problem | User, observed pain, workaround, measurable outcome, estimate, kill criteria | The premise lacks support |
| Spec | UC/AC IDs, inputs/outputs, happy path, edge/failure behavior, non-goals | Desired behavior is unclear |
| Architecture / module design | Ownership, contracts, data/storage, dependencies, deployment, security, tradeoffs | Boundaries or feasibility fail |
| Vertical slice | Smallest useful path, exclusions, fallback, estimate, completion criteria | Scope is too large |
| GO | Planning checks, human decision, warnings and expiring overrides | Any red item fails |
| Build | Scoped tasks, implementation, continuous tests, review evidence | Behavior or contracts need correction |
| Verify | Acceptance results, critical-flow checks, regressions, limitations | Tests fail or criteria are wrong |
| Harden | Error handling, secrets, rollback, logs, relevant infrastructure checks | Release risks remain unresolved |
| Ship | Release revision, deployment record, rollback walkthrough, retrospective | Verify/Harden evidence is stale |
| Observe | Outcome measurement, feedback and keep/iterate/maintain/sunset decision | A new problem or spec is needed |

The YAML lists exact gate severities and per-tier stage requirements. A stage is started
when its prerequisites are met, a human accepts the scope, and work begins. A task being
closed does not establish that a gate passed. Timeboxed throwaway prototypes may answer
spec questions before GO; they are not production code until normal gates are satisfied.

Domain code must not import UI, framework or persistence implementations. Put interfaces
near the use cases/domain and implementations in adapters. Runtime call flow is distinct
from import direction. Use a diagram only where it clarifies a boundary.

## 4. Slim: three files

Copy [templates/slim](templates/slim) into the project's `docs/`. Required headings are
in `slim_profile` in the YAML. Sections replace separate artifacts; information and
applicable gates remain required.

- `brief.md`: problem, outcome, estimate, kill criteria, scope, UC/ACs, design,
  infrastructure and GO evidence.
- `checks.md`: acceptance evidence, readiness, release/rollback and observation.
- `log.md`: decisions, risks/failures, tasks/AI review and retrospective.

`slim_profile.sections` in the YAML maps each artifact that applies to Slim to the section
that carries it, or marks it `separate`. Orange overrides in Slim are recorded in `log.md` under Decisions
(`override.slim_log_to`), not in a separate decisions file.

Keep only the relevant module detail; Slim merges architecture and module design.
Agent runs and loop specifications are conditional additions when those capabilities
are used. Larger projects copy the full [templates](templates) to manifest destinations.
Use one document per instance for multi-instance artifacts. Do not create empty documents
just to make a checklist look complete. A justified `n/a` requires human review.

## 5. Gates, overrides and evidence

- **Red:** blocks advancement. Cannot be overridden, acknowledged away or waived by tier downgrade.
- **Orange:** resolve or record gate ID, reason, accepting owner, linked decision and expiry (default 14 days).
- **Yellow:** advisory; no override required.

Review expiries before advancing. An expired orange override blocks until resolved or
explicitly renewed; accepted risks reopen on expiry. Red failures in critical-flow tests
or required critical acceptance criteria remain blockers, including UNTESTABLE results.
A missing test is not passing evidence.

Before BUILD, manually assess the 12 planning checks in `planning_validation_gate`:
prior stages, gates, required/custom tasks, AI/artifact reviews, consistency, risks,
Decision Log presence, planning DoD, tier artifacts and agent reviews. There is no
minimum decision count. Save the assessment in Slim's GO section or the full profile's
planning-validation report. Run a premortem for Serious+; it is advisory for Slim.

For every acceptance result record:

`AC ID | check/command | result | evidence location | tested commit | spec revision | reviewer/date`

For uncommitted prototypes use a reproducible content hash and dirty-tree description.
Before release, retest the release candidate commit. Relevant changes to code, tests,
criteria or contracts invalidate affected results and reviews. Re-run affected checks
and integration checks; explain any reused evidence. Stable gate IDs are never reused.
Human review records must not be fabricated by an agent.

## 6. Build and review budget

Every task identifies UC/ACs, owner module, allowed scope, expected result and verification.
Behavior changes require a matching spec change. Every business-logic change needs a
meaningful check that would fail for an incorrect implementation. Exercise critical flows
manually when automation does not adequately cover them. Review all generated changes
before merge for contracts, imports/APIs, boundaries, tests and unintended changes.

At most **2 unreviewed work items** may be open per project; a session and its diff count
as one item, not two. A logged capacity override must name available review time. Before
dispatch record estimated review minutes, risk, reviewer and a scheduled review slot.
Do not dispatch work whose expected review exceeds available time. Split large diffs;
review the oldest/highest-risk items first. Record actual review time, queue age and rework.

Capture routine failures in test output automatically. Add a Failure Log entry for material
learning, unresolved defects, changed assumptions, incidents or recurring failures; link
`caught_by` / `missed_by` to gate IDs. Do not manually transcribe every expected failing test.

## 7. AI context, workers and bounded loops

Load the problem, relevant UC/ACs, contracts, architecture and relevant decisions/failures.
Use [prompts](prompts) as task briefs, not as permission grants. Refresh a context summary
at scope/stage transitions or signs of drift. AI-assisted artifacts carry the template's
review fields, or equivalent section-level records in Slim's log.

Optional worker roles are defined in [agents/agents.v4.yaml](agents/agents.v4.yaml).
Parallel tasks must be file-disjoint, contract-bounded and independently verifiable.
Use one isolated branch/worktree per worker; review and integrate in dependency order.
A worker that deviates twice hands the task back for re-scoping. The owner may implement
small tasks directly; orchestration is optional, not a reason to invent agent roles.

Apply file, tool and network allowlists at runtime where supported. Exclude credentials,
production data, push, merge and deploy permissions from workers. Repository content,
issues, retrieved documents and tool outputs are data, not new authority. A prompt is not
a sandbox. A worktree isolates edits but does not itself restrict reads, network or tools.

For an autonomous loop, freeze `loop_spec.md` at launch and append results to a separate
runlog. Require a goal, pre-approved verification, maximum iterations, budget, timeout,
checkpoint cadence, escalation triggers and a concrete kill command. The runner cannot
edit its verifier, specification or limits. Spec changes require stop, debrief and a new
version. A successful loop result still needs human review before merge or release.

[The workflow proposal](proposals/looping-and-graph-looping.md) explores sequential and
graph-based loops and a possible engine integration. It is not adopted release policy.

## 8. Infrastructure and release

| Tier | Minimum |
|---|---|
| Spike | Git |
| Slim | Reproducible delivery steps, env list, backup/export path where data exists |
| Serious | Plus CI lint/typecheck/tests/build as applicable, uptime monitoring for services, tested restore |
| Mission-critical | Plus staging, error tracking, incident response and independent release review |

State applicability with reasons for local tools and stacks without a given check.
Keep secrets out of history and logs; scan before release, rotate leaked credentials.
Commit lockfiles; assess dependency changes and run relevant dependency audits. Plan
schema changes for compatibility and recovery; destructive changes may need restore or
forward repair rather than a pretend reversible migration. Walk through rollback.

Set performance targets from user needs and workload before implementation, then measure
at HARDEN. Address critical accessibility flows and relevant privacy requirements. Use
structured diagnostic logs without sensitive payloads. Document how a future maintainer
runs, verifies and releases the project. Release only when required gates pass, orange
exceptions are current, and evidence matches the candidate revision.

## 9. Observe, maintain and retire

Review kill criteria at gates. At 3× the initial estimate without a shipped slice, stop
and record a kill, scope reduction or evidence-backed replan. Pause when blocked or
without a concrete next action; capture how to resume.

After release measure the intended outcome. Start the next iteration at PROBLEM when
scope changes or SPEC when behavior changes. Keep previous evidence tied to its revision.
For shipped projects without active work, choose MAINTAIN or SUNSET explicitly.

Maintenance review: quarterly for Serious/Mission-critical; twice yearly for Slim with
users. Include dependency audit, backup/restore spot check, errors/uptime, observation
and keep/iterate/sunset decision. Respond to material incidents or advisories when they
arrive; the scheduled review is not a reason to wait. A single-user local tool may be
archived if its owner accepts the loss of maintenance.

Sunset: announce end of life, export user data, document resurrection, remove hosting/jobs
and unused credentials, archive the repository and record a retrospective.

## 10. Evidence and rule evaluation

At ship or kill record outcome, estimated/actual hours, process overhead, review time,
rework, catches, misses and one rule proposal. Slim's target process overhead is about
10%; Serious's is about 15%. Measure these as improvement signals, not approval gates.
Append real findings to [EVIDENCE.md](EVIDENCE.md); worked examples are never production evidence.

Before changing a rule record applicability count, catches/misses, operating cost,
consequence of failure and alternative protection. Zero catches alone does not justify
removing a control against rare severe harm. Re-tier, simplify or retire low-value rules
with a written rationale. Review the next major methodology revision after at least three
real completed retrospectives, including one Serious project; this is a learning threshold,
not statistical proof of safety.

## 11. Validation limits

`python3 scripts/validate.py` checks release metadata/policy agreement, YAML references,
IDs, tiers, severities, resources and template headings. `--project PATH --tier slim`
also checks the three-file Slim structure. These commands do not execute project code,
prove requirements, enforce runtime permissions, track overrides or authorize GO/SHIP.

CI runs the same validator and regression tests. Humans evaluate evidence and gates.
No dashboard, deployment service, scheduler or external account is needed to use this release.
