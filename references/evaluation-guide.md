# Evaluation guide

Evaluation answers whether a Skill works better for its intended task. It does not turn a subjective artifact into a precise score.

## Benchmark cases

Use stable case IDs and the same inputs for every version. At minimum include:

```json
{
  "id": "happy-path",
  "input": "representative input or a fixture path",
  "expected": "observable success condition",
  "risk": "normal"
}
```

Add missing dependency, invalid input, partial failure, long workflow, resume, and ambiguous request cases when the Skill claims those paths.

## Result record

The comparison script accepts one JSON result file per version. A useful shape is:

```json
{
  "version": "V1",
  "cases": [
    {
      "id": "happy-path",
      "status": "PASS",
      "output_valid": true,
      "retries": 0,
      "tool_calls": 2,
      "errors": 0,
      "workflow_steps": 4,
      "notes": ""
    }
  ],
  "metrics": {
    "execution_success": 1,
    "output_validity": 1
  },
  "subjective_review_required": false
}
```

Objective metrics may include execution success, retries, tool calls, errors, workflow steps, output validity, and—when measured consistently—tokens, latency, or cost. State the direction of improvement; fewer retries/errors/steps is generally better, while success/validity is higher-is-better.

Subjective results such as copy, UI, slides, or visual design should be shown side by side for human review. Do not let an agent's self-rating be the only acceptance evidence.

## Clean-context comparison

Run V1 and V2 with the same benchmark, comparable model/harness, and no design-stage conclusions in the execution context. Record environment differences and unavailable runs. A missing run is incomplete evidence, not a pass.

## Gate

- `PASS`: clear objective or reviewed improvement and no critical regression;
- `CONDITIONAL PASS`: improvement is plausible but evidence is incomplete, subjective review is pending, or a non-critical risk remains;
- `FAIL`: a previously supported behavior regresses, validation fails, or the result is unsafe; retain V1.

Use concrete per-case evidence and a bounded follow-up list. Scores may summarize trends but cannot replace the gate rationale.
