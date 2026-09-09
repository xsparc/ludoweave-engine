"""Keep onboarding short while retaining accessible historical evidence."""

import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]


def test_readme_is_a_short_entry_point() -> None:
    text = (_ROOT / "README.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    assert len(lines) <= 120
    assert lines.index("## Quick start") < 40
    assert "Build worlds humans can play and agents can operate." in text
    assert "experimental" in text
    assert "docs/quality.md" in text
    assert "docs/readme-history.md" in text
    assert not re.search(r"^>? ?M\d+", text, re.MULTILINE)


def test_readme_local_destinations_exist() -> None:
    text = (_ROOT / "README.md").read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if ":" not in target and not target.startswith("#"):
            assert (_ROOT / target.split("#", 1)[0]).exists(), target


def test_history_and_quality_are_explicitly_scoped() -> None:
    history = (_ROOT / "docs/readme-history.md").read_text(encoding="utf-8")
    quality = (_ROOT / "docs/quality.md").read_text(encoding="utf-8")
    assert "historical, not current release or support claims" in history
    assert "## Quality commands" in history
    assert "uv run --frozen pytest -q" in quality
    assert "uv run --frozen mkdocs build --strict" in quality
    assert "not authorization to tag or publish" in quality
