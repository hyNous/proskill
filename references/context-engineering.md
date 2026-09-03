# Context engineering

The context budget is part of the Skill's product quality. Put information at the narrowest layer that still makes execution reliable.

| Layer | Put here |
| --- | --- |
| `SKILL.md` | trigger, mode router, critical invariants, next action, conditional reference/script routes |
| `references/` | detailed domain rules, audit checklists, platform notes, advanced procedures loaded on demand |
| `scripts/` | stable transformations, file operations, validation, comparison, and other deterministic mechanics |
| `templates/` / `assets/` | reusable output shapes and static material |
| user input/state | task-specific values, decisions, checkpoints, and results |

## Review questions

- Can a new agent identify the route and next action without reading every file?
- Are the same rules repeated across the entrypoint and references?
- Does the entrypoint load references unconditionally when only one branch needs them?
- Is a long instruction compensating for a missing state file, script, or output contract?
- Are names and paths exact enough for a weaker model to follow?
- Does each failure route say whether to retry, repair locally, resume, ask the user, or stop?

Shorten context by deleting repetition and moving conditional detail, not by removing a safety or output contract. A reference link must say when to read it; an unlinked reference is hidden context debt.
