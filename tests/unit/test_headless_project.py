"""Data-only CLI project composition and cross-platform path confinement."""

import os
from hashlib import sha256
from pathlib import Path

import pytest

from ludoweave.core.errors import LudoWeaveError
from ludoweave.tools.headless_project import PROJECT_PROTOCOL, HeadlessProject
from ludoweave.world import canonical_dumps


def _manifest(**updates: object) -> dict[str, object]:
    document: dict[str, object] = {
        "protocol": PROJECT_PROTOCOL,
        "world_id": "tool-world",
        "seed": "0000000000000001",
        "platform_profile": "cpython-portable-empty-v1",
        "dependency_lock_hash": f"sha256:{sha256(b'lock').hexdigest()}",
    }
    document.update(updates)
    return document


def _project(root: Path, **updates: object) -> HeadlessProject:
    (root / "ludoweave.project.json").write_bytes(canonical_dumps(_manifest(**updates)))
    return HeadlessProject.load(root)


@pytest.mark.parametrize(
    "path",
    [
        "../outside.json",
        "..\\outside.json",
        "/absolute.json",
        "\\rooted.json",
        "C:\\absolute.json",
        "C:drive-relative.json",
        "state.lws:alternate",
        "NUL",
        "folder/COM1.txt",
        "folder/trailing. ",
    ],
)
def test_artifact_input_paths_must_remain_project_relative(
    tmp_path: Path,
    path: str,
) -> None:
    project = _project(tmp_path)

    with pytest.raises(LudoWeaveError) as raised:
        project.read_relative(path, max_bytes=10, role="transaction")

    assert raised.value.code == "tools.unsafe_path"
    assert raised.value.details == (("role", "transaction"),)
    assert str(tmp_path) not in str(raised.value.as_dict())


def test_output_traversal_is_rejected_before_any_external_file_is_created(
    tmp_path: Path,
) -> None:
    project = _project(tmp_path)
    escaped = tmp_path.parent / "escaped.lws"
    escaped.unlink(missing_ok=True)

    with pytest.raises(LudoWeaveError) as raised:
        project.write_relative("../escaped.lws", b"snapshot", role="snapshot")

    assert raised.value.code == "tools.unsafe_path"
    assert not escaped.exists()


def test_bounded_read_and_atomic_replacement_use_sanitized_roles(tmp_path: Path) -> None:
    project = _project(tmp_path)
    (tmp_path / "input.json").write_bytes(b"12345")
    with pytest.raises(LudoWeaveError) as raised:
        project.read_relative("input.json", max_bytes=4, role="transaction")
    assert raised.value.code == "tools.input_oversized"
    assert raised.value.details == (("limit", 4), ("role", "transaction"))

    (tmp_path / "state.lws").write_bytes(b"old")
    project.write_relative("state.lws", b"new", role="snapshot")
    assert (tmp_path / "state.lws").read_bytes() == b"new"
    assert not tuple(tmp_path.glob(".ludoweave-*"))


def test_bounded_read_caps_the_open_handle_when_size_metadata_is_stale(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project = _project(tmp_path)
    (tmp_path / "growing.json").write_bytes(b"x" * 128)
    real_fstat = os.fstat

    def stale_size(descriptor: int) -> os.stat_result:
        status = real_fstat(descriptor)
        values = list(status)
        values[6] = 0
        return os.stat_result(values)

    monkeypatch.setattr(os, "fstat", stale_size)

    with pytest.raises(LudoWeaveError) as raised:
        project.read_relative("growing.json", max_bytes=16, role="transaction")

    assert raised.value.code == "tools.input_oversized"


def test_manifest_is_exact_data_and_cannot_select_python_code(tmp_path: Path) -> None:
    (tmp_path / "ludoweave.project.json").write_bytes(
        canonical_dumps(_manifest(python_module="project.bootstrap"))
    )

    with pytest.raises(LudoWeaveError) as raised:
        HeadlessProject.load(tmp_path)

    assert raised.value.code == "tools.invalid_project"
    assert raised.value.details == (("missing", ""), ("unexpected", "python_module"))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("platform_profile", "different-portable-profile-v1"),
        ("dependency_lock_hash", f"sha256:{sha256(b'different-lock').hexdigest()}"),
        ("world_id", "different-world"),
    ],
)
def test_snapshots_are_bound_to_the_selected_project_composition(
    tmp_path: Path,
    field: str,
    value: str,
) -> None:
    source_root = tmp_path / "source"
    destination_root = tmp_path / "destination"
    source_root.mkdir()
    destination_root.mkdir()
    source = _project(source_root)
    snapshot = source.snapshot_codec.encode(source.new_session())

    destination = _project(destination_root, **{field: value})

    with pytest.raises(LudoWeaveError) as raised:
        destination.load_snapshot(snapshot)

    assert raised.value.code == "world.snapshot.incompatible"


def test_existing_symlink_escape_is_rejected_when_platform_supports_symlinks(
    tmp_path: Path,
) -> None:
    project = _project(tmp_path)
    outside = tmp_path.parent / "outside-project-input.json"
    outside.write_bytes(b"{}")
    link = tmp_path / "linked.json"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("file symlinks are unavailable for this test account")

    with pytest.raises(LudoWeaveError) as raised:
        project.read_relative("linked.json", max_bytes=10, role="transaction")

    assert raised.value.code == "tools.unsafe_path"
