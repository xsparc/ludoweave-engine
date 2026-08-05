"""M15 evidence is deterministic and keeps the visual editor deferred."""

import json
import subprocess
import sys
from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import pytest

from ludoweave import __version__

_ROOT = Path(__file__).parents[2]
_EXAMPLE = _ROOT / "examples" / "visual_editor_decision.py"
_VALIDATOR = _ROOT / "scripts" / "visual_editor_evidence.py"


class _Validate(Protocol):
    def __call__(self, document: dict[str, object], *, version: str) -> None: ...


def _validator() -> _Validate:
    spec = spec_from_file_location("visual_editor_evidence_validator", _VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("visual-editor evidence validator could not be loaded")
    module: ModuleType = module_from_spec(spec)
    spec.loader.exec_module(module)
    return cast(_Validate, module.validate_visual_editor_evidence)


def _run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        (sys.executable, str(_EXAMPLE), *arguments),
        check=False,
        capture_output=True,
        text=True,
    )


def test_visual_editor_evidence_is_repeatable_and_deferred() -> None:
    first = _run()
    second = _run()

    assert first.returncode == second.returncode == 0, first.stderr or second.stderr
    assert first.stdout == second.stdout
    document = json.loads(first.stdout)
    assert set(document) == {
        "admission_ready",
        "decision",
        "foundation_confirmed",
        "foundations",
        "gates",
        "ludoweave_version",
        "schema",
        "status",
    }
    assert document["schema"] == "ludoweave.evaluation.visual-editor/1"
    assert document["status"] == "deferred"
    assert document["decision"] == "retain-headless-inspector"
    assert document["foundation_confirmed"] is True
    assert document["admission_ready"] is False
    assert document["ludoweave_version"] == __version__
    assert all(value is False for value in document["gates"].values())
    foundations = document["foundations"]
    assert foundations["agent_all_experimental"] is True
    assert set(foundations["agent_stability"].values()) == {"experimental"}
    assert set(foundations["agent_stability"]) == set(foundations["agent_exports"])
    assert foundations["inspector_public_exported"] is False
    assert foundations["read_only_default"] is True
    assert len(foundations["agent_tools"]) == 12
    assert foundations["mutating_tools"] == ["transaction_apply", "world_tick"]
    assert foundations["root_exports"] == [
        "Engine",
        "EngineConfig",
        "LifecycleState",
        "__version__",
    ]
    assert foundations["tools_exports"] == []
    assert foundations["semantic_mutation"] == {
        "authority_hash_matched": True,
        "command_count": 6,
        "completed_ticks_unchanged": True,
        "entity_count_after": 6,
        "outcomes_committed": True,
        "post_hash_changed": True,
        "pre_hash_matched": True,
        "receipt_protocol": "ludoweave.receipt/1",
        "status": "committed",
    }
    for forbidden in (
        "credential",
        "environment",
        "host",
        "path",
        "process",
        "timing",
    ):
        assert forbidden not in first.stdout.casefold()


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("root", "admission_ready", True),
        ("root", "foundation_confirmed", 1),
        ("foundations", "agent_stability", "stable"),
        ("foundations", "agent_all_experimental", False),
        ("foundations", "inspector_public_exported", True),
        ("foundations", "read_only_default", 1),
        ("foundations", "root_exports", ["SceneEditor"]),
        ("foundations", "semantic_mutation", {"status": "committed"}),
        ("gates", "document_scene_roundtrip", True),
    ],
)
def test_exact_validator_rejects_decision_and_type_drift(
    section: str, key: str, value: object
) -> None:
    result = _run()
    document = cast(dict[str, object], json.loads(result.stdout))
    tampered = deepcopy(document)
    if section == "root":
        tampered[key] = value
    else:
        nested = cast(dict[str, object], tampered[section])
        nested[key] = value

    with pytest.raises(RuntimeError, match="visual-editor installed-surface evidence drifted"):
        _validator()(tampered, version=__version__)


def test_visual_editor_decision_rejects_arguments() -> None:
    result = _run("--build-editor")

    assert result.returncode == 1
    assert "accepts no arguments" in result.stderr
