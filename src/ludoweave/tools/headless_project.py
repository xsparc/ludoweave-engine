"""Safe data-only composition for M2 command/snapshot/replay CLI workflows."""

from __future__ import annotations

import os
import re
import stat
import tempfile
from contextlib import suppress
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import cast

from ludoweave.core.errors import LudoWeaveError
from ludoweave.ecs import (
    ComponentRegistry,
    ResourceRegistry,
    ResourceStore,
    World,
    WorldStore,
)
from ludoweave.scene.document import DEFAULT_SCENE_LIMITS, SceneDocument, SceneLimits
from ludoweave.world import (
    AuthorityResourceRegistry,
    RandomStreams,
    ReplayRunner,
    SnapshotBinding,
    SnapshotCodec,
    TickExecutor,
    WorldSession,
    canonical_dumps,
    canonical_loads,
)
from ludoweave.world.canonical import JsonValue

PROJECT_PROTOCOL = "ludoweave.headless-project/1"
PROJECT_MANIFEST = "ludoweave.project.json"
_STABLE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/+-]{0,127}\Z")
_WORLD_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_SHA256 = re.compile(r"sha256:[0-9a-f]{64}\Z")
_MAX_MANIFEST_BYTES = 65_536
_WINDOWS_RESERVED = frozenset(
    {
        "AUX",
        "CON",
        "CONIN$",
        "CONOUT$",
        "NUL",
        "PRN",
        *(f"COM{index}" for index in range(1, 10)),
        *(f"LPT{index}" for index in range(1, 10)),
    }
)


class NoopTickExecutor:
    """Deterministic empty-project tick kernel used by the M2 CLI adapter."""

    __slots__ = ()

    def execute_tick(
        self,
        world: WorldStore,
        resources: ResourceStore,
        random_streams: RandomStreams,
        tick: int,
    ) -> None:
        del world, resources, random_streams, tick


@dataclass(frozen=True, slots=True)
class HeadlessProject:
    """Loaded data-only project composition with no dynamic Python imports."""

    root: Path
    world_id: str
    seed: int
    platform_profile: str
    dependency_lock_hash: str
    project_schema: str
    components: ComponentRegistry
    resources: ResourceRegistry
    authority_resources: AuthorityResourceRegistry
    snapshot_codec: SnapshotCodec
    tick_executor: TickExecutor

    @classmethod
    def load(cls, root: Path) -> HeadlessProject:
        try:
            resolved_root = root.resolve(strict=True)
        except OSError as error:
            raise _tool_error(
                "project root is unavailable",
                code="tools.project_unavailable",
                phase="open_project",
                details={"role": "project"},
            ) from error
        if not resolved_root.is_dir():
            raise _tool_error(
                "project root must be a directory",
                code="tools.invalid_project",
                phase="open_project",
                details={"role": "project"},
            )
        manifest_path = _resolve_relative(
            resolved_root,
            PROJECT_MANIFEST,
            must_exist=True,
            role="project_manifest",
        )
        manifest_bytes = _read_bounded(
            manifest_path,
            max_bytes=_MAX_MANIFEST_BYTES,
            role="project_manifest",
        )
        try:
            decoded = canonical_loads(manifest_bytes)
        except LudoWeaveError as error:
            raise _tool_error(
                "project manifest is not bounded canonical JSON",
                code="tools.invalid_project",
                phase="decode_project",
                details={"cause_code": error.code},
            ) from error
        if not isinstance(decoded, dict):
            raise _invalid_project("project manifest must be an object", field="manifest")
        manifest = cast(dict[str, JsonValue], decoded)
        required = {
            "protocol",
            "world_id",
            "seed",
            "platform_profile",
            "dependency_lock_hash",
        }
        missing = sorted(required - manifest.keys())
        unexpected = sorted(manifest.keys() - required)
        if missing or unexpected:
            raise _tool_error(
                "project manifest fields do not match its schema",
                code="tools.invalid_project",
                phase="decode_project",
                details={
                    "missing": ",".join(missing),
                    "unexpected": ",".join(unexpected),
                },
            )
        if _text(manifest["protocol"], field="protocol") != PROJECT_PROTOCOL:
            raise _invalid_project("project protocol is incompatible", field="protocol")
        world_id = _world_id(manifest["world_id"])
        platform_profile = _stable_id(manifest["platform_profile"], field="platform_profile")
        dependency_lock_hash = _sha256_text(
            manifest["dependency_lock_hash"], field="dependency_lock_hash"
        )
        seed_text = _text(manifest["seed"], field="seed")
        if len(seed_text) != 16 or any(
            character not in "0123456789abcdef" for character in seed_text
        ):
            raise _invalid_project("project seed must be unsigned hexadecimal", field="seed")
        seed = int(seed_text, 16)
        canonical_manifest = canonical_dumps(manifest)
        project_schema = f"sha256:{sha256(canonical_manifest).hexdigest()}"
        components = ComponentRegistry()
        resources = ResourceRegistry()
        authority_resources = AuthorityResourceRegistry()
        snapshot_codec = SnapshotCodec(
            components,
            resources,
            authority_resources=authority_resources,
            binding=SnapshotBinding(
                project_schema,
                dependency_lock_hash,
                platform_profile,
            ),
        )
        return cls(
            resolved_root,
            world_id,
            seed,
            platform_profile,
            dependency_lock_hash,
            project_schema,
            components,
            resources,
            authority_resources,
            snapshot_codec,
            NoopTickExecutor(),
        )

    def new_session(self) -> WorldSession:
        return WorldSession(
            self.world_id,
            World(self.components),
            ResourceStore(self.resources),
            authority_resources=self.authority_resources,
            random_streams=RandomStreams(self.seed),
            tick_executor=self.tick_executor,
        )

    def load_snapshot(self, document: bytes) -> WorldSession:
        session = self.snapshot_codec.decode(document, tick_executor=self.tick_executor)
        if session.world_id != self.world_id or session.random_seed != self.seed:
            raise _tool_error(
                "snapshot identity is incompatible with the selected project",
                code="tools.project_mismatch",
                phase="load_snapshot",
                details={"field": "world_or_seed"},
            )
        return session

    def replay_runner(self) -> ReplayRunner:
        return ReplayRunner(
            self.snapshot_codec,
            project_schema=self.project_schema,
            dependency_lock_hash=self.dependency_lock_hash,
            platform_profile=self.platform_profile,
        )

    def read_relative(self, relative: str, *, max_bytes: int, role: str) -> bytes:
        path = _resolve_relative(self.root, relative, must_exist=True, role=role)
        return _read_bounded(path, max_bytes=max_bytes, role=role)

    def load_scene(
        self,
        relative: str,
        *,
        limits: SceneLimits = DEFAULT_SCENE_LIMITS,
    ) -> SceneDocument:
        """Load one detached scene document from a project-confined file."""

        if type(limits) is not SceneLimits:
            raise _tool_error(
                "scene limits must be an exact SceneLimits value",
                code="tools.invalid_scene_limits",
                phase="load_scene",
                details={"actual_type": type(limits).__name__},
            )
        document = self.read_relative(relative, max_bytes=limits.max_bytes, role="scene")
        return SceneDocument.from_json(document, limits=limits)

    def write_relative(self, relative: str, document: bytes, *, role: str) -> None:
        path = _resolve_relative(self.root, relative, must_exist=False, role=role)
        parent = path.parent
        if not parent.is_dir():
            raise _tool_error(
                "output parent directory does not exist",
                code="tools.output_unavailable",
                phase="write",
                details={"role": role},
            )
        temporary: Path | None = None
        try:
            descriptor, name = tempfile.mkstemp(prefix=".ludoweave-", dir=parent)
            temporary = Path(name)
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(document)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
            temporary = None
        except OSError as error:
            raise _tool_error(
                "output could not be written atomically",
                code="tools.output_unavailable",
                phase="write",
                details={"role": role},
            ) from error
        finally:
            if temporary is not None:
                with suppress(OSError):
                    temporary.unlink(missing_ok=True)


def _resolve_relative(root: Path, relative: str, *, must_exist: bool, role: str) -> Path:
    if type(relative) is not str or not relative or "\x00" in relative:
        raise _unsafe_path(role)
    try:
        byte_length = len(relative.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise _unsafe_path(role) from error
    if byte_length > 1_024:
        raise _unsafe_path(role)
    windows = PureWindowsPath(relative)
    posix = PurePosixPath(relative)
    if windows.is_absolute() or windows.drive or windows.root or posix.is_absolute():
        raise _unsafe_path(role)
    parts = (*windows.parts, *posix.parts)
    for part in parts:
        device_name = part.rstrip(" .").partition(".")[0].upper()
        if (
            part == ".."
            or ":" in part
            or part.endswith((" ", "."))
            or device_name in _WINDOWS_RESERVED
        ):
            raise _unsafe_path(role)
    try:
        candidate = (root / relative).resolve(strict=must_exist)
        candidate.relative_to(root)
    except (OSError, ValueError) as error:
        raise _unsafe_path(role) from error
    if must_exist and not candidate.is_file():
        raise _tool_error(
            "input must be a regular file",
            code="tools.input_unavailable",
            phase="read",
            details={"role": role},
        )
    return candidate


def _read_bounded(path: Path, *, max_bytes: int, role: str) -> bytes:
    descriptor: int | None = None
    try:
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
        status = os.fstat(descriptor)
        if not stat.S_ISREG(status.st_mode):
            raise _tool_error(
                "input must be a regular file",
                code="tools.input_unavailable",
                phase="read",
                details={"role": role},
            )
        if status.st_size > max_bytes:
            raise _tool_error(
                "input exceeds its byte limit",
                code="tools.input_oversized",
                phase="read",
                details={"role": role, "limit": max_bytes},
            )
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = None
            document = handle.read(max_bytes + 1)
    except LudoWeaveError:
        raise
    except OSError as error:
        raise _tool_error(
            "input could not be read",
            code="tools.input_unavailable",
            phase="read",
            details={"role": role},
        ) from error
    finally:
        if descriptor is not None:
            with suppress(OSError):
                os.close(descriptor)
    if len(document) > max_bytes:
        raise _tool_error(
            "input exceeds its byte limit",
            code="tools.input_oversized",
            phase="read",
            details={"role": role, "limit": max_bytes},
        )
    return document


def _text(value: object, *, field: str) -> str:
    if type(value) is not str:
        raise _invalid_project("project field must be text", field=field)
    return value


def _stable_id(value: object, *, field: str) -> str:
    text = _text(value, field=field)
    if _STABLE_ID.fullmatch(text) is None:
        raise _invalid_project("project identity must use bounded stable text", field=field)
    return text


def _world_id(value: object) -> str:
    text = _text(value, field="world_id")
    if _WORLD_ID.fullmatch(text) is None:
        raise _invalid_project("world ID must use bounded stable text", field="world_id")
    return text


def _sha256_text(value: object, *, field: str) -> str:
    text = _text(value, field=field)
    if _SHA256.fullmatch(text) is None:
        raise _invalid_project("project hash must use canonical SHA-256 text", field=field)
    return text


def _invalid_project(message: str, *, field: str) -> LudoWeaveError:
    return _tool_error(
        message,
        code="tools.invalid_project",
        phase="decode_project",
        details={"field": field},
    )


def _unsafe_path(role: str) -> LudoWeaveError:
    return _tool_error(
        "path must remain project-relative and confined",
        code="tools.unsafe_path",
        phase="resolve_path",
        details={"role": role},
    )


def _tool_error(
    message: str,
    *,
    code: str,
    phase: str,
    details: dict[str, str | int | float | bool | None],
) -> LudoWeaveError:
    return LudoWeaveError(
        message,
        code=code,
        subsystem="tools",
        phase=phase,
        details=details,
    )
