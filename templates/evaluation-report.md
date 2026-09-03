# Evaluation Report

- Skill/mode: `{{name and Design|Optimize}}`
- Version(s): `{{V1/V2 or generated version}}`
- Benchmark: `{{path or description}}`
- Model/harness: `{{...}}`
- Clean context: `{{yes|no|unavailable}}`
- Date: `{{date}}`

## Cases

| Case ID | Expected | V1 result | V2/result | Output valid | Errors/retries | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `{{happy-path}}` | `{{...}}` | `{{PASS/FAIL/UNRUN}}` | `{{...}}` | `{{...}}` | `{{...}}` | `{{...}}` |
| `{{missing-dependency}}` | `{{clear recovery}}` | `{{...}}` | `{{...}}` | `{{...}}` | `{{...}}` | `{{...}}` |
| `{{invalid-input}}` | `{{clear error}}` | `{{...}}` | `{{...}}` | `{{...}}` | `{{...}}` | `{{...}}` |

## Objective metrics

| Metric | V1 | V2 | Direction | Interpretation |
| --- | ---: | ---: | --- | --- |
| Execution success | `{{...}}` | `{{...}}` | higher | `{{...}}` |
| Output validity | `{{...}}` | `{{...}}` | higher | `{{...}}` |
| Errors | `{{...}}` | `{{...}}` | lower | `{{...}}` |
| Retries | `{{...}}` | `{{...}}` | lower | `{{...}}` |

## Subjective review

- Reviewer: `{{...}}`
- Artifacts: `{{paths}}`
- Findings: `{{...}}`
- Review status: `{{complete|pending|not applicable}}`

## Comparison and gate

- Improvements: `{{...}}`
- Regressions: `{{...}}`
- Missing evidence: `{{...}}`
- Gate: `{{PASS|CONDITIONAL PASS|FAIL}}`
- Decision: `{{keep V1 / adopt V2 / adopt with conditions}}`

## Remaining work

- `{{bounded follow-up item}}`
