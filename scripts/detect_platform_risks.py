"""Find common shell, path, API, and runtime portability hazards."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List

from _skill_utils import iter_files, json_text, read_text, relative_path


RISK_PATTERNS = (
    (
        "unix-shell",
        re.compile(r"#!/(?:usr/bin/env\s+)?(?:ba)?sh\b|\b(?:bash|zsh)\b", re.IGNORECASE),
        "Shell-specific interpreter or command may not exist on every host.",
    ),
    (
        "unix-command",
        re.compile(r"\b(?:chmod|sed\s+-i|grep\s+-P|rm\s+-rf|apt-get|brew\s+install)\b", re.IGNORECASE),
        "Unix-specific command or flag needs a host-specific alternative.",
    ),
    (
        "windows-shell",
        re.compile(
            r"\b(?:powershell|pwsh|cmd(?:\.exe)?|winget|choco)(?:\s|$|\.exe\b)",
            re.IGNORECASE,
        ),
        "Windows-specific shell or package command may not exist on every host.",
    ),
    (
        "windows-path",
        re.compile(
            r"\b[A-Za-z]:\\(?:[A-Za-z0-9_. -]+\\)+|%[A-Z_][A-Z0-9_]*%|\\Users\\",
            re.IGNORECASE,
        ),
        "Windows-specific path or environment-variable syntax is embedded.",
    ),
    (
        "unix-path",
        re.compile(r"(?:/home/|/Users/|/tmp/|~/|/var/|/opt/|/etc/)", re.IGNORECASE),
        "Absolute or Unix-style path may not be portable.",
    ),
    (
        "macos-api",
        re.compile(r"\b(?:osascript|pbcopy|pbpaste)\b|/Applications/", re.IGNORECASE),
        "macOS-specific command or path needs an alternative or documented limit.",
    ),
    (
        "os-api",
        re.compile(r"\b(?:os\.startfile|winreg|fcntl|termios|win32api|darwin)\b", re.IGNORECASE),
        "Operating-system-specific API may require a portability boundary.",
    ),
)


def find_risks(root: Path) -> List[Dict[str, object]]:
    findings: List[Dict[str, object]] = []
    for path in iter_files(root):
        if path.name == "detect_platform_risks.py" or path.name.startswith("test_"):
            continue
        text = read_text(path)
        if text is None:
            continue
        relative = relative_path(root, path)
        for line_number, line in enumerate(text.splitlines(), 1):
            for category, pattern, reason in RISK_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        {
                            "category": category,
                            "path": relative,
                            "line": line_number,
                            "reason": reason,
                            "snippet": line.strip()[:240],
                        }
                    )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = args.skill_path.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"Skill path is not a directory: {root}")
    result = {"root": str(root), "finding_count": 0, "findings": find_risks(root)}
    result["finding_count"] = len(result["findings"])
    if args.as_json:
        print(json_text(result))
        return 0
    print(f"Platform-risk findings: {result['finding_count']}")
    for finding in result["findings"]:
        print(
            f"{finding['category']} {finding['path']}:{finding['line']} — "
            f"{finding['reason']} Snippet: {finding['snippet']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
