# Skill Blueprint

Use this as the canonical intermediate model for Design and Optimize. Mark unknowns as `unknown` or `not applicable`; do not silently fill them in.

## Identity

- Name: `{{lowercase-skill-name}}`
- Purpose: `{{one sentence}}`
- Description/trigger summary: `{{...}}`
- Blueprint source: `{{requirement or existing skill path}}`

## Trigger and inputs

- Conditions: `{{positive signals}}`
- Do not trigger for: `{{negative signals}}`
- Required inputs: `{{...}}`
- Optional inputs: `{{...}}`

## Outputs

- Primary: `{{...}}`
- Secondary: `{{...}}`
- Human-review artifacts: `{{... or none}}`

## Workflow

| Step | Action | Owner | Input/output | Branch, retry, or stop condition |
| --- | --- | --- | --- | --- |
| 1 | `{{...}}` | `{{agent/program/user/tool}}` | `{{...}}` | `{{...}}` |
| 2 | `{{...}}` | `{{...}}` | `{{...}}` | `{{...}}` |

## Agent/program boundary

- Agent tasks: `{{...}}`
- Program tasks: `{{...}}`
- References needed by route: `{{...}}`
- Templates/assets needed by route: `{{...}}`

## Dependencies and configuration

- CLI/runtime: `{{...}}`
- External services: `{{...}}`
- Environment variables: `{{names only}}`
- Credential setup: `{{secure setup and failure behavior}}`
- Platform assumptions: `{{...}}`

## Productization

- Happy path: `{{short sequence}}`
- Onboarding: `{{first-run setup}}`
- Recovery paths: `{{malformed input, dependency, auth, network, tool}}`
- State: `{{state representation}}`
- Checkpoints/resume: `{{... or not needed}}`
- Failure isolation: `{{... or not needed}}`
- Human review/approval: `{{... or none}}`

## Skill files

- `SKILL.md`: `{{routing and critical rules}}`
- `scripts/`: `{{script and contract}}`
- `references/`: `{{reference and conditional load trigger}}`
- `templates/`: `{{reusable output shapes}}`
- `assets/`: `{{static assets or not needed}}`

## Evaluation

- Benchmark cases: `{{case IDs}}`
- Objective metrics: `{{...}}`
- Subjective review: `{{... or none}}`
- Preservation requirements (Optimize): `{{... or not applicable}}`
- Acceptance gate: `{{PASS/CONDITIONAL PASS/FAIL criteria}}`
