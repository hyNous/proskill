# Agent/program boundary

Choose the owner of each workflow step by its semantic shape, not by a blanket preference for code or prompts.

## Decision test

Ask:

1. Is the input structured?
2. Is the output structured?
3. Is the operation repeated or batchable?
4. Does the same input usually require the same execution logic?
5. Does the step require open-ended interpretation or subjective judgment?

Prefer a program when answers 1–4 are mostly yes and 5 is no. Keep the step with the agent when the value is interpretation, planning, routing, exception judgment, or creative synthesis. Use a human when approval or subjective acceptance is part of correctness.

## Good program candidates

- deterministic file reads/writes and format conversion;
- JSON/CSV transformation and schema validation;
- batch rename, merge, split, or packaging;
- fixed API sequences with explicit inputs and outputs;
- repeatable checks, summaries, and comparison calculations;
- checkpoint persistence and resume bookkeeping.

## Keep judgment with the agent or user

- extracting the real business goal from ambiguous prose;
- choosing a workflow branch from incomplete context;
- deciding whether a result is persuasive, safe, or aesthetically acceptable;
- adapting to an undocumented environment change;
- approving an irreversible external action.

## Script contract

Every script should have:

- a narrow purpose and explicit CLI inputs;
- deterministic, inspectable output;
- standard-library dependencies where practical;
- clear nonzero failure exits and actionable messages;
- no credential values in logs;
- a small runnable check when it contains nontrivial logic.

Do not turn an entire workflow into one opaque script. Let the agent choose and explain the semantic steps around small deterministic helpers.
