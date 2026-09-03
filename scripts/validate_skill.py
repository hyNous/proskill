"""Validate Skill structure, local links, metadata, and Python syntax."""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple

from _skill_utils import iter_files, json_text, local_links, parse_frontmatter, read_text, relative_path


NAME_RE = re.compile(r"^[a-z0-9-]{1,63}$")


def _inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _check_links(root: Path, source: Path, text: str) -> List[str]:
    errors: List[str] = []
    for target in local_links(text):
        candidate = (source.parent / target).resolve()
        relative_source = relative_path(root, source)
        if not _inside(root, candidate):
            errors.append(f"{relative_source}: local link escapes Skill: {target}")
        elif not candidate.exists():
            errors.append(f"{relative_source}: missing local link: {target}")
    return errors


def validate(root: Path) -> Dict[str, object]:
    errors: List[str] = []
    warnings: List[str] = []
    if not root.is_dir():
        return {"root": str(root), "valid": False, "errors": [f"not a directory: {root}"], "warnings": []}

    skill_path = root / "SKILL.md"
    skill_text = read_text(skill_path) if skill_path.is_file() else None
    if skill_text is None:
        errors.append("missing readable SKILL.md")
    else:
        frontmatter, metadata = parse_frontmatter(skill_text)
        if frontmatter is None:
            errors.append("SKILL.md is missing YAML frontmatter")
        else:
            if not metadata.get("name"):
                errors.append("SKILL.md frontmatter is missing name")
            elif not NAME_RE.fullmatch(metadata["name"]):
                errors.append("SKILL.md frontmatter name must contain only lowercase letters, digits, and hyphens")
            elif metadata["name"].startswith("-") or metadata["name"].endswith("-") or "--" in metadata["name"]:
                errors.append("SKILL.md frontmatter name cannot start/end with hyphen or contain consecutive hyphens")
            elif metadata["name"] != root.name:
                warnings.append(
                    f"frontmatter name '{metadata['name']}' differs from folder '{root.name}'"
                )
            if not metadata.get("description"):
                errors.append("SKILL.md frontmatter is missing description")
            elif "<" in metadata["description"] or ">" in metadata["description"]:
                errors.append("SKILL.md frontmatter description cannot contain angle brackets")
            elif len(metadata["description"]) > 1024:
                errors.append("SKILL.md frontmatter description exceeds 1024 characters")
            elif len(metadata["description"]) < 20:
                warnings.append("frontmatter description is very short; routing may be ambiguous")
        if len(skill_text.splitlines()) > 400:
            warnings.append("SKILL.md exceeds 400 lines; consider routing detail to references")
        if "[TODO" in skill_text or "[todo" in skill_text.lower():
            warnings.append("SKILL.md still contains a TODO scaffold marker")

    for path in iter_files(root):
        text = read_text(path)
        if text is not None and path.suffix.lower() in {".md", ".markdown"}:
            errors.extend(_check_links(root, path, text))
        if path.suffix.lower() == ".py":
            if text is None:
                errors.append(f"{relative_path(root, path)}: unreadable Python file")
            else:
                try:
                    ast.parse(text, filename=str(path))
                except SyntaxError as exc:
                    errors.append(
                        f"{relative_path(root, path)}: Python syntax error at line {exc.lineno}: {exc.msg}"
                    )

    metadata_path = root / "agents" / "openai.yaml"
    if metadata_path.exists():
        metadata_text = read_text(metadata_path)
        if metadata_text is None:
            errors.append("agents/openai.yaml is unreadable")
        else:
            if "interface:" not in metadata_text:
                warnings.append("agents/openai.yaml has no interface section")
            prompt_match = re.search(r"^\s*default_prompt:\s*[\"']?(.*?)[\"']?\s*$", metadata_text, re.MULTILINE)
            if prompt_match and "$" not in prompt_match.group(1):
                warnings.append("agents/openai.yaml default_prompt does not visibly invoke the Skill")

    return {
        "root": str(root.resolve()),
        "valid": not errors,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = args.skill_path.expanduser().resolve()
    result = validate(root)
    if args.as_json:
        print(json_text(result))
    else:
        print("Validation: " + ("PASS" if result["valid"] else "FAIL"))
        for item in result["errors"]:
            print(f"ERROR: {item}")
        for item in result["warnings"]:
            print(f"WARNING: {item}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
