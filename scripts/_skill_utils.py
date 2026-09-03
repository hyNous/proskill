"""Small standard-library helpers shared by ProSkill inspection scripts."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple
from urllib.parse import urlparse


IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    ".next",
}

_FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
_LINK_RE = re.compile(r"\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")


def iter_files(root: Path) -> Iterator[Path]:
    """Yield regular files below root in deterministic order."""

    if not root.is_dir():
        return
    for base, directories, filenames in os.walk(root, followlinks=False):
        directories[:] = sorted(
            name for name in directories if name not in IGNORED_DIRS
        )
        for name in sorted(filenames):
            path = Path(base) / name
            if path.is_file() and not path.is_symlink():
                yield path


def read_text(path: Path) -> Optional[str]:
    """Read a likely text file without making binary scans fail."""

    try:
        with path.open("rb") as handle:
            sample = handle.read(4096)
        if b"\x00" in sample:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeError):
        return None


def parse_frontmatter(text: str) -> Tuple[Optional[str], Dict[str, str]]:
    """Return the raw YAML block and simple top-level key/value pairs."""

    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None, {}
    block = match.group(1)
    values: Dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", key.strip()):
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return block, values


def local_links(text: str) -> List[str]:
    """Extract relative Markdown link targets, excluding URLs and anchors."""

    targets: List[str] = []
    for match in _LINK_RE.finditer(text):
        target = (match.group(1) or match.group(2) or "").strip()
        parsed = urlparse(target)
        if not target or target.startswith("#") or parsed.scheme or parsed.netloc:
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if target:
            targets.append(target)
    return targets


def relative_path(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def human_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KiB"
    return f"{size / (1024 * 1024):.1f} MiB"
