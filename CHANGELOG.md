# Changelog

## 4.6 — 2026-09-19

- Ship all artifact templates, reusable prompts, optional agent role definitions and a worked Slim example.
- Add a three-file Slim profile and local/CI structural validation.
- Make Decision Log validation presence-based; make red blockers consistently non-overridable.
- Register stable gate IDs and revision-specific verification/review evidence.
- Route small changes by risk, budget review time, and evaluate rules by exposure and consequences.
- Remove dashboard metadata, health scores and claims of unavailable automatic enforcement.
- Add an optional workflow proposal; proposals do not change adopted policy.

Migration: use `SPEC-GATED-MODULAR-DELIVERY-v4.6.md`. The YAML filename remains
`methodology.v4.yaml` for schema continuity, with `release: '4.6'`. Consumers of removed
`dashboard`, `health_weights` or artifact `section` fields must adapt. Gate IDs are new;
retain old label references in historical evidence and map new entries to IDs. Slim
projects may consolidate existing artifacts into the three files without discarding
history. Existing legitimate reviews remain tied to their original revisions.

## 4.5-a1 — 2026-07-23

Registered premortem and retrospective artifacts in the YAML manifest.
