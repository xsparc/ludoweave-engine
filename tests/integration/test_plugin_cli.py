"""CLI acceptance for explicit data-only plugin compatibility checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

from ludoweave.tools.cli import main

_ROOT = Path(__file__).resolve().parents[2]
_EXAMPLE = _ROOT / "examples" / "example.plugin.json"


def test_plugin_check_accepts_the_example_without_disclosing_path(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(["plugin", "check", str(_EXAMPLE)])

    captured = capsys.readouterr()
    report = cast(dict[str, object], json.loads(captured.out))
    assert exit_code == 0
    assert captured.err == ""
    assert report["protocol"] == "ludoweave.plugin-check/1"
    assert report["compatible"] is True
    assert report["plugin_ids"] == ["org.ludoweave.example.render-device"]
    assert str(_EXAMPLE) not in captured.out


def test_plugin_check_returns_one_for_valid_incompatibility(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    document = cast(dict[str, object], json.loads(_EXAMPLE.read_text(encoding="utf-8")))
    document["engine"] = {"minimum": "9.0.0", "maximum_exclusive": "10.0.0"}
    manifest = tmp_path / "incompatible.json"
    manifest.write_text(json.dumps(document), encoding="utf-8")

    exit_code = main(["plugin", "check", str(manifest)])

    captured = capsys.readouterr()
    report = cast(dict[str, object], json.loads(captured.out))
    assert exit_code == 1
    assert report["compatible"] is False
    assert captured.err == ""
    assert str(manifest) not in captured.out


def test_plugin_check_returns_two_for_executable_or_oversized_input(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    document = cast(dict[str, object], json.loads(_EXAMPLE.read_text(encoding="utf-8")))
    document["module"] = "untrusted.module"
    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps(document), encoding="utf-8")

    assert main(["plugin", "check", str(invalid)]) == 2
    captured = capsys.readouterr()
    error = cast(dict[str, object], json.loads(captured.err))
    assert captured.out == ""
    assert error["protocol"] == "ludoweave.cli.error/1"
    assert str(invalid) not in captured.err

    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * 65_537)
    assert main(["plugin", "check", str(oversized)]) == 2
    captured = capsys.readouterr()
    assert "plugins.manifest_too_large" in captured.err
    assert str(oversized) not in captured.err


def test_plugin_check_does_not_echo_rejected_manifest_values(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    sensitive_value = r"C:\private\credential-token.txt"
    document = cast(dict[str, object], json.loads(_EXAMPLE.read_text(encoding="utf-8")))
    document["capabilities"] = [sensitive_value]
    invalid = tmp_path / "sensitive.json"
    invalid.write_text(json.dumps(document), encoding="utf-8")

    assert main(["plugin", "check", str(invalid)]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert sensitive_value not in captured.err
    assert str(invalid) not in captured.err


def test_plugin_check_does_not_echo_invalid_determinism_argument(
    capsys: pytest.CaptureFixture[str],
) -> None:
    sensitive_value = r"C:\private\credential-token.txt"

    assert (
        main(
            [
                "plugin",
                "check",
                "--minimum-determinism",
                sensitive_value,
                str(_EXAMPLE),
            ]
        )
        == 2
    )

    captured = capsys.readouterr()
    error = cast(dict[str, object], json.loads(captured.err))
    assert captured.out == ""
    assert error["protocol"] == "ludoweave.cli.error/1"
    assert sensitive_value not in captured.err
    assert str(_EXAMPLE) not in captured.err


def test_module_invocation_checks_example_manifest() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ludoweave", "plugin", "check", str(_EXAMPLE)],
        cwd=_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["compatible"] is True
    assert str(_EXAMPLE) not in result.stdout
