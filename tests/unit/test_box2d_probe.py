"""Tests for the isolated M9 Box2D admission probe."""

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).parents[2] / "scripts" / "probe_box2d_candidate.py"
_FAKE_MODULE = """
previous_world = None

class Body:
    def __init__(self):
        self.step_count = 0

    @property
    def position(self):
        return 0.0, 5.0 - self.step_count / 60.0

class Builder:
    def __init__(self, world):
        self.world = world

    def dynamic(self):
        return self

    def static(self):
        return self

    def position(self, x, y):
        return self

    def box(self, half_width, half_height):
        return self

    def build(self):
        body = Body()
        self.world.bodies.append(body)
        return body

class World:
    def __init__(self, *, gravity, threads):
        global previous_world
        assert gravity == (0.0, -10.0)
        assert threads == 1
        if previous_world is not None:
            assert previous_world.destroy_count == 2
        previous_world = self
        self.bodies = []
        self.destroy_count = 0

    def new_body(self):
        return Builder(self)

    def step(self, time_step, substep_count):
        assert time_step.hex() == (1.0 / 60.0).hex()
        assert substep_count == 4
        for body in self.bodies:
            body.step_count += 1

    def destroy(self):
        self.destroy_count += 1
        assert self.destroy_count <= 2
"""


def _run(*arguments: str, fake_sites: tuple[Path, ...] = ()) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    if not fake_sites:
        environment.pop("PYTHONPATH", None)
    else:
        environment["PYTHONPATH"] = os.pathsep.join(str(path) for path in fake_sites)
    return subprocess.run(
        (sys.executable, "-S", str(_SCRIPT), *arguments),
        check=False,
        capture_output=True,
        env=environment,
        text=True,
    )


def _write_fake_candidate(root: Path) -> None:
    (root / "box2d.py").write_text(textwrap.dedent(_FAKE_MODULE), encoding="utf-8")
    _write_fake_metadata(root)


def _write_fake_metadata(root: Path) -> None:
    metadata = root / "box2d_python-0.1.2.dist-info"
    metadata.mkdir()
    (metadata / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: box2d-python\nVersion: 0.1.2\n",
        encoding="utf-8",
    )
    (metadata / "RECORD").write_text(
        "box2d.py,,\n"
        "box2d_python-0.1.2.dist-info/METADATA,,\n"
        "box2d_python-0.1.2.dist-info/RECORD,,\n",
        encoding="utf-8",
    )


def test_probe_emits_repeatable_sanitized_evidence(tmp_path: Path) -> None:
    _write_fake_candidate(tmp_path)

    result = _run("--iterations", "3", "--steps", "4", fake_sites=(tmp_path,))

    assert result.returncode == 0, result.stderr
    document = json.loads(result.stdout)
    assert document["schema"] == "ludoweave.evaluation.box2d/1"
    assert document["status"] == "ok"
    assert document["candidate"] == {
        "distribution": "box2d-python",
        "version": "0.1.2",
    }
    assert document["probe"]["repeat_equal"] is True
    assert len(document["probe"]["trace_sha256"]) == 64
    assert not ({"path", "environment_variables"} & document.keys())


def test_probe_reports_missing_candidate_without_a_trace() -> None:
    result = _run("--iterations", "2", "--steps", "1")

    assert result.returncode == 2, result.stderr
    document = json.loads(result.stdout)
    assert document["status"] == "unavailable"
    assert document["candidate"] == {"distribution": "box2d-python"}
    assert "trace_sha256" not in document["probe"]


def test_probe_distinguishes_broken_installed_candidate(tmp_path: Path) -> None:
    _write_fake_metadata(tmp_path)

    result = _run("--iterations", "2", "--steps", "1", fake_sites=(tmp_path,))

    assert result.returncode == 1
    document = json.loads(result.stdout)
    assert document["status"] == "failed"
    assert document["candidate"]["version"] == "0.1.2"
    assert document["probe"]["error_type"] == "_CandidateOwnershipError"


def test_probe_rejects_shadow_module_before_import(tmp_path: Path) -> None:
    candidate_site = tmp_path / "candidate"
    shadow_site = tmp_path / "shadow"
    candidate_site.mkdir()
    shadow_site.mkdir()
    _write_fake_candidate(candidate_site)
    (shadow_site / "box2d.py").write_text(
        "raise RuntimeError('shadow module executed')\n", encoding="utf-8"
    )

    result = _run(
        "--iterations",
        "2",
        "--steps",
        "1",
        fake_sites=(shadow_site, candidate_site),
    )

    assert result.returncode == 1
    document = json.loads(result.stdout)
    assert document["status"] == "failed"
    assert document["candidate"]["version"] == "0.1.2"
    assert document["probe"]["error_type"] == "_CandidateOwnershipError"
    assert "shadow module executed" not in result.stderr


@pytest.mark.parametrize(
    "arguments",
    [
        ("--iterations", "1"),
        ("--iterations", "101"),
        ("--steps", "0"),
        ("--steps", "10001"),
        ("--iterations", "100", "--steps", "1001"),
    ],
)
def test_probe_rejects_unbounded_work(arguments: tuple[str, ...]) -> None:
    result = _run(*arguments)

    assert result.returncode == 2
    assert "error:" in result.stderr
