# ProSkill

ProSkill is a V1 meta-skill for engineering other Agent Skills. It turns requirements, SOPs, and workflows into a Skill, or audits and improves an existing Skill with a preserved baseline and evidence-based comparison.

## Included

- `SKILL.md`: mode routing, invariants, outputs, and evaluation gate.
- `references/`: progressive-disclosure workflows and productization rules.
- `templates/`: reusable requirement, blueprint, audit, plan, and evaluation formats.
- `scripts/`: dependency-free structural inspection, validation, platform-risk detection, and V1/V2 comparison.

## Quick start

Invoke `$proskill` with either:

```text
Design a Skill from this requirement/SOP: ...
```

or:

```text
Optimize the Skill at /path/to/skill.
```

For a target Skill, run `scripts/validate_skill.py` before evaluation. For optimization, keep the original folder as V1 and evaluate both versions against the same benchmark.

## V1 boundary

Design, Optimize, Blueprint, productization, validation, and evaluation are included. Merge, Migrate, Maintain, a hosted dashboard, and continuous monitoring are intentionally deferred to V2.
