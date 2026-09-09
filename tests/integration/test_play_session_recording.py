"""Actual play-loop inputs survive headless replay without device dependencies."""

import json
import subprocess
import sys
from collections.abc import Callable, Sequence
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import cast

import pytest

from ludoweave.app import InputSnapshot, InputSource
from ludoweave.app.replay import InputReplay
from ludoweave.audio import NullAudioBackend
from ludoweave.platform import (
    CloseEvent,
    FocusEvent,
    GamepadAxis,
    GamepadAxisEvent,
    GamepadConnectionEvent,
    GamepadEvent,
    KeyEvent,
    MouseButtonEvent,
    PlatformEvent,
)
from ludoweave.render import NullRenderDevice, RenderDevice, SurfaceHandle

_ROOT = Path(__file__).resolve().parents[2]


def _example() -> ModuleType:
    spec = spec_from_file_location("play_recording_example", _ROOT / "examples/clockwork_arena.py")
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _main(module: ModuleType, arguments: Sequence[str]) -> int:
    return cast(Callable[[Sequence[str]], int], module.main)(arguments)


def _use_device(device: RenderDevice) -> Callable[[str], RenderDevice]:
    def create(name: str) -> RenderDevice:
        return device

    return create


def _no_device(name: str) -> RenderDevice:
    pytest.fail("device opened")


def _verify(path: Path) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(_ROOT / "examples/input_replay.py"), "replay", str(path)],
        cwd=path.parent,
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )
    return cast(dict[str, object], json.loads(result.stdout))


@pytest.mark.parametrize("ticks,stress", [(0, 1), (30, 1), (12, 16)])
def test_play_recording_matches_normal_play_and_fresh_process(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], ticks: int, stress: int
) -> None:
    module = _example()
    arguments = ["--ticks", str(ticks), "--stress", str(stress), "--render-every", "7"]
    assert _main(module, arguments) == 0
    ordinary = capsys.readouterr().out
    path = tmp_path / "play.json"
    assert _main(module, [*arguments, "--record", str(path)]) == 0
    recorded = capsys.readouterr().out
    assert recorded == ordinary
    artifact = InputReplay.from_json(path.read_bytes())
    assert len(artifact.snapshots) == ticks
    verified = _verify(path)
    assert verified["ticks"] == ticks
    assert verified["state_hash"] == json.loads(recorded)["arena"]["state_hash"]
    assert verified["artifact_hash"] == artifact.artifact_hash()


class _EventDevice(NullRenderDevice):
    def __init__(self, *, immediate_close: bool = False) -> None:
        super().__init__()
        self.polls = 0
        self.closes = 0
        self.immediate_close = immediate_close

    def drain_surface_events(self, handle: SurfaceHandle) -> tuple[PlatformEvent, ...]:
        super().drain_surface_events(handle)
        self.polls += 1
        if self.immediate_close or self.polls == 3:
            return (CloseEvent(),)
        if self.polls == 1:
            return (KeyEvent("w", True), MouseButtonEvent("primary", True))
        return (FocusEvent(False),)

    def poll_gamepads(self) -> tuple[GamepadEvent, ...]:
        if self.polls == 1:
            return (
                GamepadConnectionEvent(0, True),
                GamepadAxisEvent(0, GamepadAxis.LEFT_X, 0.625),
            )
        return ()

    def close(self) -> None:
        self.closes += 1
        super().close()


@pytest.mark.parametrize("immediate_close", [False, True])
def test_interactive_recording_owns_consumed_events_and_early_close(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    immediate_close: bool,
) -> None:
    module = _example()
    device = _EventDevice(immediate_close=immediate_close)
    monkeypatch.setattr(module, "_device", _use_device(device))
    path = tmp_path / "interactive.json"
    assert (
        _main(
            module,
            [
                "--renderer",
                "wgpu",
                "--window",
                "--interactive",
                "--ticks",
                "10",
                "--record",
                str(path),
            ],
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    artifact = InputReplay.from_json(path.read_bytes())
    ticks = 0 if immediate_close else 2
    assert len(artifact.snapshots) == payload["arena"]["ticks"] == ticks
    assert device.closes == 1
    if not immediate_close:
        first, second = artifact.snapshots
        assert first.pressed("fire") and first.just_pressed("fire")
        assert first.value("move.x") == (0.625 - 0.15) / (1.0 - 0.15)
        assert first.value("move.y") == 1.0
        assert not second.pressed("fire") and second.just_released("fire")
    assert _verify(path)["state_hash"] == payload["arena"]["state_hash"]


@pytest.mark.parametrize("arguments", [["--ticks", "3601"], ["--ticks", "-1"]])
def test_recording_limits_precede_device_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, arguments: list[str]
) -> None:
    module = _example()
    monkeypatch.setattr(module, "_device", _no_device)
    path = tmp_path / "refused.json"
    with pytest.raises(SystemExit) as error:
        _main(module, [*arguments, "--record", str(path)])
    assert error.value.code == 2
    assert not path.exists()


def test_existing_destination_is_preserved_before_devices(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "existing.json"
    path.write_bytes(b"preserve")
    module = _example()
    monkeypatch.setattr(module, "_device", _no_device)
    with pytest.raises(SystemExit):
        _main(module, ["--record", str(path)])
    assert path.read_bytes() == b"preserve"


@pytest.mark.parametrize("failure", ["initialize", "close", "race"])
def test_failure_closes_resources_and_never_publishes_success(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    path = tmp_path / "failure.json"
    device = _EventDevice()

    class Audio(NullAudioBackend):
        closes = 0

        def __init__(self) -> None:
            super().__init__()
            instances.append(self)

        def initialize(self) -> None:
            if failure == "initialize":
                raise RuntimeError("injected initialization failure")
            super().initialize()

        def close(self) -> None:
            self.closes += 1
            super().close()
            if failure == "close":
                raise RuntimeError("injected close failure")
            if failure == "race":
                path.write_bytes(b"concurrent destination")

    instances: list[Audio] = []
    module = _example()
    monkeypatch.setattr(module, "_device", _use_device(device))
    monkeypatch.setattr(module, "NullAudioBackend", Audio)
    with pytest.raises((RuntimeError, FileExistsError)):
        _main(module, ["--ticks", "1", "--record", str(path)])
    assert len(instances) == 1
    assert device.closes == instances[0].closes == 1
    if failure == "race":
        assert path.read_bytes() == b"concurrent destination"
    else:
        assert not path.exists()


def test_rejected_tick_does_not_publish_recording(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class BrokenInput:
        def snapshot_for_tick(self, tick: int) -> InputSnapshot:
            raise RuntimeError("injected input failure")

    def source(ticks: int) -> InputSource:
        return BrokenInput()

    module = _example()
    device = _EventDevice()
    monkeypatch.setattr(module, "clockwork_input", source)
    monkeypatch.setattr(module, "_device", _use_device(device))
    path = tmp_path / "rejected.json"
    with pytest.raises(RuntimeError, match="transaction was rejected"):
        _main(module, ["--ticks", "1", "--record", str(path)])
    assert device.closes == 1
    assert not path.exists()
