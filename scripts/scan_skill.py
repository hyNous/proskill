"""Run mechanical inventory checks on a Skill folder."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List

from _skill_utils import (
    iter_files,
    json_text,
    local_links,
    parse_frontmatter,
    read_text,
    relative_path,
)


DEPENDENCY_PATTERNS = (
    r"\bpip(?:3)?\s+install\b",
    r"\bnpm\s+(?:install|ci)\b",
    r"\b(?:brew|apt(?:-get)?|winget|choco|cargo|go)\s+install\b",
)


def scan(root: Path, large_file_bytes: int = 100 * 1024) -> Dict[str, object]:
    files = list(iter_files(root))
    large_files: List[Dict[str, object]] = []
    missing_paths: List[Dict[str, str]] = []
    dependency_hints: List[Dict[str, object]] = []
    total_bytes = 0
    text_files = 0
    for path in files:
        size = path.stat().st_size
        total_bytes += size
        relative = relative_path(root, path)
        if size >= large_file_bytes:
            large_files.append({"path": relative, "bytes": size})
        text = read_text(path)
        if text is None:
            continue
        text_files += 1
        if path.suffix.lower() in {".md", ".markdown"}:
            for target in local_links(text):
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    missing_paths.append({"source": relative, "target": target})
        for line_number, line in enumerate(text.splitlines(), 1):
            if any(re.search(pattern, line, re.IGNORECASE) for pattern in DEPENDENCY_PATTERNS):
                dependency_hints.append(
                    {"path": relative, "line": line_number, "text": line.strip()}
                )
    skill_path = root / "SKILL.md"
    skill_text = read_text(skill_path) if skill_path.is_file() else None
    _, metadata = parse_frontmatter(skill_text or "")
    return {
        "root": str(root.resolve()),
        "total_files": len(files),
        "text_files": text_files,
        "total_bytes": total_bytes,
        "skill_md": {
            "exists": skill_path.is_file(),
            "lines": len(skill_text.splitlines()) if skill_text else 0,
            "characters": len(skill_text) if skill_text else 0,
            "metadata": metadata,
        },
        "reference_count": sum(
            1 for path in files if relative_path(root, path).startswith("references/")
        ),
        "script_count": sum(
            1 for path in files if relative_path(root, path).startswith("scripts/")
        ),
        "large_files": large_files,
        "missing_local_paths": missing_paths,
        "dependency_hints": dependency_hints,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", type=Path)
    parser.add_argument("--large-file-bytes", type=int, default=100 * 1024)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = args.skill_path.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"Skill path is not a directory: {root}")
    result = scan(root, args.large_file_bytes)
    if args.as_json:
        print(json_text(result))
        return 0
    print(f"Skill: {result['root']}")
    print(f"Files: {result['total_files']}; text files: {result['text_files']}")
    print(f"SKILL.md: {result['skill_md']['lines']} lines, {result['skill_md']['characters']} characters")
    print(f"References: {result['reference_count']}; scripts: {result['script_count']}")
    print(f"Large files: {len(result['large_files'])}")
    print(f"Missing local paths: {len(result['missing_local_paths'])}")
    print(f"Dependency hints: {len(result['dependency_hints'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
