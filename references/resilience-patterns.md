# Resilience patterns

Use resilience only when the workflow is long, expensive, externally fragile, or difficult to repeat.

## Checkpoints

Persist a small, human-readable checkpoint after each meaningful stage. It should identify:

- input and output artifact paths;
- completed stage and next stage;
- configuration that is safe to record;
- failed items and their error summaries;
- version/schema if the checkpoint may be resumed later.

Never store credential values in checkpoints. Make checkpoint writes atomic when a partial write could corrupt resume state.

## Resume

Define whether resume reuses, verifies, or regenerates each prior artifact. Resume only from a known completed stage; do not infer completion from a missing or ambiguous file. A resumed run should not duplicate non-idempotent external actions.

## Failure isolation

For batches, isolate item failures and preserve successful outputs. For multi-stage work, keep intermediate artifacts so a local repair does not restart the entire workflow. Report both completed and failed units.

## Retry

Retry only transient and idempotent operations. Bound attempts, preserve the original error, and stop for authentication, malformed input, permission, or irreversible-action failures. If no safe retry exists, give a repair/resume path instead.

## Human review

Pause before irreversible, high-risk, or materially subjective decisions. Store the candidate result and the decision separately when possible so a rejected review can be repaired without recomputing unrelated stages.
