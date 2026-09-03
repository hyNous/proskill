# Optimization workflow

Use this reference when an existing Skill folder is in scope. Optimize behavior and reliability, not wording alone.

## O0 — Preserve the baseline

Treat the supplied folder as V1. Do not overwrite it before V2 passes. Use a sibling copy such as `optimized-skill/`, a version-control branch, or the user's specified versioned layout. Record the source path and the behavior that must remain compatible.

## O1 — Reverse engineer

Build an Existing Skill Blueprint before editing. Identify:

- purpose, trigger, inputs, outputs, and actual workflow;
- scripts, references, assets, templates, configuration, and external tools;
- hidden dependencies, credentials, platform assumptions, and state;
- happy path, failure paths, retry/resume behavior, and human review;
- behavior that is intentional versus accidental or debugging-only.

Use [templates/skill-blueprint.md](../templates/skill-blueprint.md). Separate facts observed in the files from assumptions inferred by the audit.

## O2 — Static scan

Run the deterministic checks before semantic conclusions:

```text
python scripts/inspect_structure.py <v1>
python scripts/scan_skill.py <v1>
python scripts/validate_skill.py <v1>
python scripts/detect_platform_risks.py <v1>
```

Use the results to locate missing local paths, syntax errors, oversized context, hidden dependencies, and portability hazards. Do not treat a clean static scan as proof that the workflow works.

## O3 — Semantic audit

Audit only categories relevant to the observed Skill. Check:

- onboarding and recovery;
- workflow length, duplicate steps, and implicit state;
- agent/program boundary and mechanical work that should be scripted;
- `SKILL.md` size, repetition, and conditional reference loading;
- weak-model routing, explicit state, and ambiguous instructions;
- checkpoints, resume, retry, and failure isolation;
- human interaction and reusable UI/output templates;
- hard-coded paths, shell/runtime assumptions, and credential handling;
- distribution usability when the Skill is public.

Use [productization-rules.md](productization-rules.md) as the common checklist, then load [agent-program-boundary.md](agent-program-boundary.md), [context-engineering.md](context-engineering.md), [onboarding-recovery.md](onboarding-recovery.md), [resilience-patterns.md](resilience-patterns.md), or [evaluation-guide.md](evaluation-guide.md) only for relevant findings.

Classify findings as `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`. Explain the concrete failure mode and evidence; do not make a numeric score the conclusion.

## O4 — Optimization plan

For each proposed change, fill [templates/optimization-plan.md](../templates/optimization-plan.md) with:

```text
Problem → Why it matters → Proposed change → Expected benefit → Risk → Validation method
```

Use priority `P0` for functional/critical issues, `P1` for reliability/architecture, `P2` for efficiency/maintainability, and `P3` for UX/polish. Prefer local, behavior-preserving changes. Reject changes that only add more prompt reminders when a structural fix is available.

## O5 — Refactor

Implement the smallest plan that addresses the findings. Preserve supported behavior and keep V1 untouched. Move stable repeated operations into dependency-free scripts when that materially improves determinism; move detailed conditional knowledge out of `SKILL.md`; make state and recovery visible. Do not add speculative abstractions or V2 Merge/Migrate/Maintain machinery.

## O6 — Validate

Run the same structural, script, instruction, and platform checks against V2. Re-run representative V1 cases to confirm behavior preservation. Any missing dependency, invalid input, or script failure should produce a clear result rather than a guessed recovery.

## O7 — Regression evaluation

Evaluate V1 and V2 with the same benchmark and as-close-as-possible model/harness conditions. Use clean task context so design-stage knowledge does not bias either run. Capture objective metrics and side-by-side subjective artifacts. Use `scripts/compare_versions.py` to organize JSON results, then complete [templates/evaluation-report.md](../templates/evaluation-report.md).

Return one gate:

- `PASS` only when V2 clearly improves without a critical regression;
- `CONDITIONAL PASS` when evidence is incomplete or improvement still carries risk;
- `FAIL` when a supported behavior regresses; retain V1.

Default to one major optimization cycle. Report a bounded backlog instead of looping indefinitely; continue only when the user explicitly asks.
