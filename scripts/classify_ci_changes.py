"""Classify a pull-request diff for LudoWeave's quota-conscious CI policy."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections.abc import Iterable, Sequence
from pathlib import Path, PurePosixPath

_REVISION = re.compile(r"[0-9a-fA-F]{40,64}\Z")
_DOCUMENTATION_FILES = frozenset(
    {
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/labels.yml",
    }
)


def is_documentation_path(value: str) -> bool:
    """Return whether *value* is confined to documentation/community state."""

    if not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        return False
    if value in _DOCUMENTATION_FILES:
        return True
    if len(path.parts) == 1 and path.suffix.casefold() == ".md":
        return True
    if path.parts[0] in {"docs", ".project"}:
        return path.suffix.casefold() == ".md"
    return path.parts[:2] == (".github", "ISSUE_TEMPLATE") and path.suffix.casefold() in {
        ".md",
        ".yaml",
        ".yml",
    }


def requires_substantive_ci(paths: Iterable[str]) -> bool:
    """Fail closed unless at least one path exists and every path is documentation."""

    changed = tuple(paths)
    return not changed or any(not is_documentation_path(path) for path in changed)


def changed_paths(base: str, head: str, *, cwd: Path) -> tuple[str, ...]:
    """Return NUL-safe three-dot diff paths for two validated Git revisions."""

    for label, revision in (("base", base), ("head", head)):
        if _REVISION.fullmatch(revision) is None:
            raise ValueError(f"{label} revision must be a full hexadecimal object id")
    result = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "--no-renames",
            "-z",
            f"{base}...{head}",
            "--",
        ],
        cwd=cwd,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git diff failed with exit {result.returncode}: {message}")
    return tuple(
        entry.decode("utf-8", errors="strict") for entry in result.stdout.split(b"\0") if entry
    )


def _append_github_output(path: Path, *, substantive: bool, count: int) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(f"substantive={'true' if substantive else 'false'}\n")
        stream.write(f"changed_count={count}\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="full pull-request base object id")
    parser.add_argument("--head", required=True, help="full pull-request head object id")
    parser.add_argument(
        "--github-output",
        required=True,
        type=Path,
        help="GitHub Actions output file to append",
    )
    args = parser.parse_args(argv)
    base = str(args.base)
    head = str(args.head)
    output = Path(args.github_output)
    paths = changed_paths(base, head, cwd=Path.cwd())
    substantive = requires_substantive_ci(paths)
    _append_github_output(output, substantive=substantive, count=len(paths))
    print(
        json.dumps(
            {
                "changed_count": len(paths),
                "classification": "substantive" if substantive else "documentation",
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
