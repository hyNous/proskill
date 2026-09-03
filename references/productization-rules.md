# Productization rules

Apply these rules to both Design and Optimize. They are a review checklist, not a reason to add machinery to a simple Skill.

| Rule | Required decision | Evidence to look for |
| --- | --- | --- |
| Workflow first | model trigger, steps, branches, and outputs before files | requirement/workflow/blueprint artifacts |
| Deterministic core + agentic shell | assign repeatable structured work to programs and judgment to the agent | architecture table and script boundaries |
| Progressive context | keep the entrypoint small and load detail conditionally | reference links with routing conditions |
| Weak-model clarity | make state, next action, and failure behavior explicit | short numbered routes, named inputs/outputs |
| Happy path first | make normal execution direct and move setup/recovery to the edges | one obvious success route |
| Recoverable workflow | checkpoint, resume, and isolate failures when work is long or expensive | state/checkpoint/resume contract |
| Human-in-the-loop | require review for subjective, risky, or irreversible decisions | explicit approval/review artifact |
| Portability | avoid unannounced shell, path, runtime, and credential assumptions | platform findings and documented alternatives |
| Evaluation | compare observable behavior, not self-reported quality | benchmark, results, gate, remaining risk |

## Severity guidance

- `CRITICAL`: data loss, security exposure, unsafe irreversible action, or a core supported behavior cannot run.
- `HIGH`: frequent failure, unrecoverable long work, hidden dependency, or a major route that a weaker model is likely to misinterpret.
- `MEDIUM`: unnecessary context, brittle portability, repeated manual work, or incomplete diagnostics.
- `LOW`: polish, documentation, or a minor convenience with no material behavior impact.

## Change discipline

Preserve the business goal and supported behavior unless the user explicitly changes them. Prefer deletion, routing, and local repairs over adding universal instructions. Do not force every Skill to have scripts, checkpoints, UI, or all reference categories: add each only when the workflow justifies it.
