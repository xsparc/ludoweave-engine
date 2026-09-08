"""Versioned replay-owned action history, composed above world replay contracts."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from hashlib import sha256
from typing import cast

from ludoweave.app.errors import InputError
from ludoweave.app.input import InputAction, InputSnapshot, InputSource
from ludoweave.core.errors import LudoWeaveError
from ludoweave.world.canonical import JsonLimits, JsonValue, canonical_dumps, canonical_loads
from ludoweave.world.errors import IncompatibleReplayError
from ludoweave.world.replay import ReplayResult, ReplayRunner, ReplayTimeline
from ludoweave.world.state import TickExecutor

__all__ = ["InputReplay"]
__stability__ = {"InputReplay": "experimental"}

_PROTOCOL = "ludoweave.input-replay/1"
_MAX_TICKS = 60_000
_MAX_ACTIONS = 256
_MAX_NAME = 128
_MAX_ENTRIES = 250_000
_LIMITS = JsonLimits(
    max_bytes=67_108_864,
    max_depth=100,
    max_nodes=4_000_000,
    max_collection_items=100_000,
    max_string_bytes=1_048_576,
)


@dataclass(frozen=True, slots=True)
class InputReplay:
    """Detached timeline and complete inputs for its half-open tick interval.

    Input lookup outside the recorded interval refuses; no missing tick becomes
    an empty input. Playback uses an explicitly supplied trusted executor factory,
    not names or executable code from the document. Instances own no resources.
    """

    timeline: ReplayTimeline
    snapshots: tuple[InputSnapshot, ...]

    def __post_init__(self) -> None:
        if type(self.timeline) is not ReplayTimeline or type(self.snapshots) is not tuple:
            raise _error("timeline and snapshots must be exact immutable values")
        count = self.timeline.final_tick - self.timeline.header.initial_tick
        if not 0 <= count <= _MAX_TICKS or len(self.snapshots) != count:
            raise _error("input history must cover every replay tick within the tick limit")
        entries = 0
        for offset, snapshot in enumerate(self.snapshots):
            if type(snapshot) is not InputSnapshot:
                raise _error("input history entries must be exact snapshots")
            if snapshot.tick != self.timeline.header.initial_tick + offset:
                raise _error("input history ticks must be contiguous and ordered")
            sizes = (
                len(snapshot.actions),
                len(snapshot.just_pressed_actions),
                len(snapshot.just_released_actions),
            )
            entries += sum(sizes)
            if max(sizes) > _MAX_ACTIONS or entries > _MAX_ENTRIES:
                raise _error("input snapshot or history exceeds the action limit")
            groups = (
                tuple(action.name for action in snapshot.actions),
                snapshot.just_pressed_actions,
                snapshot.just_released_actions,
            )
            if any(len(name) > _MAX_NAME for group in groups for name in group):
                raise _error("input action name exceeds the length limit")
        # Apply the same whole-artifact budget to direct and decoded construction.
        self.canonical_bytes()

    def snapshot_for_tick(self, tick: int) -> InputSnapshot:
        """Return one owned immutable snapshot; refuse absent or malformed ticks."""

        start = self.timeline.header.initial_tick
        if type(tick) is not int or not start <= tick < self.timeline.final_tick:
            raise _error("requested tick is outside the recorded input history")
        return self.snapshots[tick - start]

    def canonical_bytes(self) -> bytes:
        """Encode the complete artifact with the existing canonical JSON policy."""

        try:
            return canonical_dumps(
                {
                    "protocol": _PROTOCOL,
                    "timeline": self.timeline.as_dict(),
                    "inputs": [_snapshot_document(item) for item in self.snapshots],
                },
                limits=_LIMITS,
            )
        except LudoWeaveError as error:
            raise _error("input replay cannot be encoded within its limits") from error

    def artifact_hash(self) -> str:
        """Bind input history and timeline together; not an authenticity signature."""

        return "sha256:" + sha256(self.canonical_bytes()).hexdigest()

    @classmethod
    def from_json(cls, document: str | bytes) -> InputReplay:
        """Admit bounded data only, rejecting unknown fields and incomplete inputs."""

        try:
            root = _object(
                canonical_loads(document, limits=_LIMITS), {"protocol", "timeline", "inputs"}
            )
            if root["protocol"] != _PROTOCOL:
                raise _error("input replay protocol is incompatible")
            values = root["inputs"]
            if type(values) is not list or len(values) > _MAX_TICKS:
                raise _error("input history exceeds the tick limit or is not an array")
            timeline = ReplayTimeline.from_json(canonical_dumps(root["timeline"], limits=_LIMITS))
            count = timeline.final_tick - timeline.header.initial_tick
            if not 0 <= count <= _MAX_TICKS or len(values) != count:
                raise _error("input history must cover every replay tick within the tick limit")
            snapshots: list[InputSnapshot] = []
            entries = 0
            for item in values:
                snapshot = _decode_snapshot(item)
                entries += (
                    len(snapshot.actions)
                    + len(snapshot.just_pressed_actions)
                    + len(snapshot.just_released_actions)
                )
                if entries > _MAX_ENTRIES:
                    raise _error("input history exceeds the aggregate action limit")
                snapshots.append(snapshot)
            return cls(timeline, tuple(snapshots))
        except (InputError, IncompatibleReplayError):
            raise
        except LudoWeaveError as error:
            raise _error("input replay contains an invalid nested value") from error

    def replay(
        self,
        runner: ReplayRunner,
        executor_factory: Callable[[InputSource], TickExecutor],
    ) -> ReplayResult:
        """Verify composition first, then replay exclusively with embedded inputs.

        The caller owns the trusted factory and any resources it creates. Playback
        is synchronous and single-owner, just like ReplayRunner. All legacy state
        and checkpoint verification remains enabled.
        """

        checked = runner.decode(self.timeline.canonical_bytes())
        return runner.replay(checked, tick_executor=executor_factory(self))


def _snapshot_document(snapshot: InputSnapshot) -> dict[str, JsonValue]:
    return {
        "tick": snapshot.tick,
        "actions": {action.name: action.value for action in snapshot.actions},
        "just_pressed": list(snapshot.just_pressed_actions),
        "just_released": list(snapshot.just_released_actions),
    }


def _object(value: JsonValue, keys: set[str]) -> dict[str, JsonValue]:
    if type(value) is not dict or set(value) != keys:
        raise _error("input replay object has missing or unknown fields")
    return value


def _decode_snapshot(value: JsonValue) -> InputSnapshot:
    item = _object(value, {"tick", "actions", "just_pressed", "just_released"})
    tick = item["tick"]
    actions = item["actions"]
    if type(tick) is not int or type(actions) is not dict or len(actions) > _MAX_ACTIONS:
        raise _error("input snapshot tick or actions are invalid")
    entries: list[InputAction] = []
    for name, action in actions.items():
        if len(name) > _MAX_NAME or type(action) not in (bool, float):
            raise _error("input action name or value is invalid")
        entries.append(InputAction(name, cast(bool | float, action)))
    transitions: list[tuple[str, ...]] = []
    for key in ("just_pressed", "just_released"):
        names = item[key]
        if type(names) is not list or len(names) > _MAX_ACTIONS:
            raise _error("input transitions exceed their limit or are not an array")
        if any(type(name) is not str or len(name) > _MAX_NAME for name in names):
            raise _error("input transition name is invalid")
        transitions.append(tuple(cast(list[str], names)))
    return InputSnapshot(tick, entries, just_pressed=transitions[0], just_released=transitions[1])


def _error(message: str) -> InputError:
    return InputError(
        message,
        code="app.invalid_input_replay",
        subsystem="app",
        phase="input_replay",
    )
