"""Source-tree agent-tool conformance example acceptance."""

import json
import subprocess
import sys
from pathlib import Path
from typing import cast


def test_direct_agent_conformance_example_emits_path_free_success() -> None:
    example = Path(__file__).parents[2] / "examples" / "agent_tool_conformance.py"
    result = subprocess.run(
        (sys.executable, str(example)),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    report = cast(dict[str, object], json.loads(result.stdout))
    assert report["protocol"] == "ludoweave.agent-tool-conformance/1"
    assert report["profile"] == "agent-tool-baseline/1"
    assert report["adapter_id"] == "org.ludoweave.agent-service"
    assert report["status"] == "pass"
    checks = cast(list[dict[str, object]], report["checks"])
    assert len(checks) == 12
    assert all(check["status"] == "pass" for check in checks)
    assert str(example.parent) not in result.stdout


def test_agent_conformance_example_rejects_arguments_without_loading_an_adapter() -> None:
    example = Path(__file__).parents[2] / "examples" / "agent_tool_conformance.py"
    result = subprocess.run(
        (sys.executable, str(example), "--adapter", "arbitrary.module"),
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr
