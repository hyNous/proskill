"""Compare objective evaluation results for two Skill versions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

from _skill_utils import json_text


PASS_STATUSES = {"PASS", "PASSED", "SUCCESS", "SUCCEEDED", "OK"}
METRIC_DIRECTIONS = {
    "execution_success": "higher",
    "success_rate": "higher",
    "output_validity": "higher",
    "output_valid": "higher",
    "retries": "lower",
    "errors": "lower",
    "tool_calls": "lower",
    "workflow_steps": "lower",
    "tokens": "lower",
    "latency_ms": "lower",
    "cost": "lower",
}


def load_result(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"evaluation result must be a JSON object: {path}")
    cases = value.get("cases", [])
    if not isinstance(cases, list) or any(not isinstance(case, dict) for case in cases):
        raise ValueError(f"'cases' must be a list of objects: {path}")
    metrics = value.get("metrics", {})
    if not isinstance(metrics, dict):
        raise ValueError(f"'metrics' must be an object: {path}")
    return value


def _case_status(case: Mapping[str, Any]) -> Optional[bool]:
    if isinstance(case.get("success"), bool):
        return case["success"]
    status = str(case.get("status", "")).strip().upper()
    if status in PASS_STATUSES:
        return True
    if status:
        return False
    return None


def _case_valid(case: Mapping[str, Any]) -> Optional[bool]:
    for key in ("output_valid", "valid"):
        if isinstance(case.get(key), bool):
            return case[key]
    return None


def _number(value: Any) -> Optional[float]:
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None


def _metric_comparisons(
    v1: Mapping[str, Any], v2: Mapping[str, Any]
) -> Tuple[List[Dict[str, Any]], List[str]]:
    metrics1 = v1.get("metrics", {})
    metrics2 = v2.get("metrics", {})
    names = sorted(set(metrics1) | set(metrics2))
    comparisons: List[Dict[str, Any]] = []
    missing: List[str] = []
    for name in names:
        before = _number(metrics1.get(name))
        after = _number(metrics2.get(name))
        direction = METRIC_DIRECTIONS.get(name)
        if before is None or after is None or direction is None:
            missing.append(name)
            comparisons.append(
                {
                    "metric": name,
                    "v1": metrics1.get(name),
                    "v2": metrics2.get(name),
                    "direction": direction or "unknown",
                    "result": "unknown",
                }
            )
            continue
        delta = after - before
        if delta == 0:
            result = "unchanged"
        elif (direction == "higher" and delta > 0) or (direction == "lower" and delta < 0):
            result = "improved"
        else:
            result = "regressed"
        comparisons.append(
            {
                "metric": name,
                "v1": before,
                "v2": after,
                "delta": delta,
                "direction": direction,
                "result": result,
            }
        )
    return comparisons, missing


def compare(v1: Mapping[str, Any], v2: Mapping[str, Any]) -> Dict[str, Any]:
    cases1 = {
        str(case.get("id")): case
        for case in v1.get("cases", [])
        if case.get("id") is not None
    }
    cases2 = {
        str(case.get("id")): case
        for case in v2.get("cases", [])
        if case.get("id") is not None
    }
    common_ids = sorted(set(cases1) & set(cases2))
    regressions: List[str] = []
    improvements: List[str] = []
    case_results: List[Dict[str, Any]] = []
    for case_id in common_ids:
        before = cases1[case_id]
        after = cases2[case_id]
        before_status = _case_status(before)
        after_status = _case_status(after)
        before_valid = _case_valid(before)
        after_valid = _case_valid(after)
        if before_status is True and after_status is not True:
            regressions.append(f"{case_id}: supported success no longer passes")
        elif before_status is not True and after_status is True:
            improvements.append(f"{case_id}: now passes")
        if before_valid is True and after_valid is False:
            regressions.append(f"{case_id}: output validity regressed")
        case_results.append(
            {
                "id": case_id,
                "v1_status": before.get("status", "UNRECORDED"),
                "v2_status": after.get("status", "UNRECORDED"),
                "v1_success": before_status,
                "v2_success": after_status,
                "v1_output_valid": before_valid,
                "v2_output_valid": after_valid,
            }
        )
    added_cases = sorted(set(cases2) - set(cases1))
    removed_cases = sorted(set(cases1) - set(cases2))
    metric_comparisons, unknown_metrics = _metric_comparisons(v1, v2)
    metric_improvements = [
        item["metric"] for item in metric_comparisons if item["result"] == "improved"
    ]
    metric_regressions = [
        item["metric"] for item in metric_comparisons if item["result"] == "regressed"
    ]
    regressions.extend(f"metric {name}: worsened" for name in metric_regressions)
    improvements.extend(f"metric {name}: improved" for name in metric_improvements)
    subjective_review = bool(
        v1.get("subjective_review_required") or v2.get("subjective_review_required")
    )
    has_improvement = bool(improvements)
    if regressions:
        gate = "FAIL"
    elif has_improvement and not (unknown_metrics or subjective_review):
        gate = "PASS"
    elif has_improvement or unknown_metrics or subjective_review or not common_ids:
        gate = "CONDITIONAL PASS"
    else:
        gate = "CONDITIONAL PASS"
    return {
        "gate": gate,
        "v1_label": v1.get("version", "V1"),
        "v2_label": v2.get("version", "V2"),
        "common_case_count": len(common_ids),
        "added_cases": added_cases,
        "removed_cases": removed_cases,
        "case_results": case_results,
        "regressions": regressions,
        "improvements": improvements,
        "metric_comparisons": metric_comparisons,
        "unknown_metrics": unknown_metrics,
        "subjective_review_required": subjective_review,
    }


def render_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Skill Version Comparison",
        "",
        f"- V1: {result['v1_label']}",
        f"- V2: {result['v2_label']}",
        f"- Gate: **{result['gate']}**",
        f"- Common cases: {result['common_case_count']}",
        "",
        "## Case comparison",
        "",
        "| Case | V1 | V2 | V1 valid | V2 valid |",
        "| --- | --- | --- | --- | --- |",
    ]
    for case in result["case_results"]:
        lines.append(
            f"| {case['id']} | {case['v1_status']} | {case['v2_status']} | "
            f"{case['v1_output_valid']} | {case['v2_output_valid']} |"
        )
    if not result["case_results"]:
        lines.append("| (none) | — | — | — | — |")
    lines.extend(["", "## Improvements", ""])
    if result["improvements"]:
        lines.extend(f"- {item}" for item in result["improvements"])
    else:
        lines.append("- None recorded")
    lines.extend(["", "## Regressions", ""])
    if result["regressions"]:
        lines.extend(f"- {item}" for item in result["regressions"])
    else:
        lines.append("- None recorded")
    lines.extend(["", "## Metric comparison", ""])
    if result["metric_comparisons"]:
        lines.extend(
            f"- {item['metric']}: {item['v1']} → {item['v2']} ({item['result']})"
            for item in result["metric_comparisons"]
        )
    else:
        lines.append("- None recorded")
    if result["unknown_metrics"]:
        lines.extend(["", "Unknown or incomplete metrics: " + ", ".join(result["unknown_metrics"])])
    if result["subjective_review_required"]:
        lines.extend(["", "Subjective review is required before treating the result as final."])
    if result["added_cases"]:
        lines.extend(["", "Added cases: " + ", ".join(result["added_cases"])])
    if result["removed_cases"]:
        lines.extend(["", "Removed cases: " + ", ".join(result["removed_cases"])])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v1", required=True, type=Path, help="V1 evaluation JSON")
    parser.add_argument("--v2", required=True, type=Path, help="V2 evaluation JSON")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = compare(load_result(args.v1), load_result(args.v2))
    except ValueError as exc:
        parser.error(str(exc))
    content = json_text(result) if args.format == "json" else render_markdown(result)
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
