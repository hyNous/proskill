"""Minimal dependency-free self-check for the ProSkill helper scripts."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from compare_versions import compare
from detect_platform_risks import find_risks
from inspect_structure import inspect
from scan_skill import scan
from validate_skill import validate


def main() -> int:
    with TemporaryDirectory() as temporary:
        root = Path(temporary) / "sample-skill"
        (root / "references").mkdir(parents=True)
        (root / "agents").mkdir()
        (root / "scripts").mkdir()
        (root / "SKILL.md").write_text(
            "---\n"
            "name: sample-skill\n"
            "description: A sample skill used for the ProSkill self-check.\n"
            "---\n\n"
            "[Rule](references/rule.md)\n",
            encoding="utf-8",
        )
        (root / "references" / "rule.md").write_text("# Rule\n", encoding="utf-8")
        (root / "agents" / "openai.yaml").write_text(
            "interface:\n  display_name: Sample\n", encoding="utf-8"
        )
        (root / "scripts" / "example.py").write_text("print('ok')\n", encoding="utf-8")
        (root / "notes.md").write_text("Fallback command: bash /tmp/work\n", encoding="utf-8")

        structure = inspect(root)
        assert structure["total_files"] == 5
        assert structure["skill_md"]["exists"] is True
        assert scan(root)["missing_local_paths"] == []
        assert validate(root)["valid"] is True
        assert any(item["category"] == "unix-shell" for item in find_risks(root))

        v1 = {
            "version": "V1",
            "cases": [{"id": "happy", "status": "FAIL", "output_valid": False}],
            "metrics": {"errors": 2},
        }
        v2 = {
            "version": "V2",
            "cases": [{"id": "happy", "status": "PASS", "output_valid": True}],
            "metrics": {"errors": 0},
        }
        assert compare(v1, v2)["gate"] == "PASS"
        supported_v1 = {
            "cases": [{"id": "core", "status": "PASS", "output_valid": True}],
            "metrics": {"errors": 0},
        }
        regressed_v2 = {
            "cases": [{"id": "core", "status": "FAIL", "output_valid": False}],
            "metrics": {"errors": 1},
        }
        assert compare(supported_v1, regressed_v2)["gate"] == "FAIL"
    print("self-test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
