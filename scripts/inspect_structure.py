"""Inspect the shape and file inventory of a Skill folder."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Dict, List

from _skill_utils import human_bytes, iter_files, json_text, relative_path


EXPECTED_ENTRIES = ("SKILL.md", "agents", "scripts", "references", "templates", "assets")


def inspect(root: Path) -> Dict[str, object]:
    files = list(iter_files(root))
    extension_counts = Counter(
        (path.suffix.lower() or "[no extension]") for path in files
    )
    top_level_counts = Counter(
        (relative_path(root, path).split("/", 1)[0]) for path in files
    )
    total_bytes = sum(path.stat().st_size for path in files)
    entries = {
        entry: (root / entry).exists()
        for entry in EXPECTED_ENTRIES
    }
    skill_path = root / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8", errors="replace") if skill_path.is_file() else ""
    return {
        "root": str(root.resolve()),
        "exists": root.is_dir(),
        "total_files": len(files),
        "total_bytes": total_bytes,
        "total_size": human_bytes(total_bytes),
        "entries": entries,
        "skill_md": {
            "exists": skill_path.is_file(),
            "lines": len(skill_text.splitlines()) if skill_text else 0,
            "characters": len(skill_text),
        },
        "files_by_extension": dict(sorted(extension_counts.items())),
        "files_by_top_level_entry": dict(sorted(top_level_counts.items())),
        "files": [relative_path(root, path) for path in files],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = args.skill_path.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"Skill path is not a directory: {root}")
    result = inspect(root)
    if args.as_json:
        print(json_text(result))
        return 0
    print(f"Skill: {result['root']}")
    print(f"Files: {result['total_files']} ({result['total_size']})")
    print(f"SKILL.md: {result['skill_md']['lines']} lines, {result['skill_md']['characters']} characters")
    missing = [name for name, present in result["entries"].items() if not present]
    print("Missing expected entries: " + (", ".join(missing) if missing else "none"))
    print("Top-level files:")
    for name, count in result["files_by_top_level_entry"].items():
        print(f"  {name}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
