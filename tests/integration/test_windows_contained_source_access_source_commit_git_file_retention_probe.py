"""Retain the selected Git executable across the complete M223 boundary."""

from __future__ import annotations

import sys
from ctypes import wintypes
from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest

from tests.integration import (
    test_windows_contained_source_access_source_commit_binding_probe as _commit_module,
)
from tests.integration import (
    test_windows_contained_source_access_source_commit_git_selection_binding_probe as _selection_module,
)
from tests.integration.test_windows_retained_launch_source_access_refusal_probe import (
    _require_source_access_allowed,  # pyright: ignore[reportPrivateUsage]
    _require_source_access_refused,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _FILE_ATTRIBUTE_NORMAL,  # pyright: ignore[reportPrivateUsage]
    _FILE_SHARE_READ,  # pyright: ignore[reportPrivateUsage]
    _GENERIC_READ,  # pyright: ignore[reportPrivateUsage]
    _OPEN_EXISTING,  # pyright: ignore[reportPrivateUsage]
    _handle_value,  # pyright: ignore[reportPrivateUsage]
    _ImageApi,  # pyright: ignore[reportPrivateUsage]
    _normalized_name,  # pyright: ignore[reportPrivateUsage]
    _RetainedImageFile,  # pyright: ignore[reportPrivateUsage]
)
from tests.integration.test_windows_retained_process_image_binding_probe import (
    _verify_stable as _verify_image_stable,  # pyright: ignore[reportPrivateUsage]
)

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="M224 retains one Git executable file across the Windows M223 boundary",
)


class _RetainedGitExecutableFile(_RetainedImageFile):
    """Own one non-inheritable read handle that excludes write/delete sharing."""

    def __init__(self, path: str | Path) -> None:
        self._api = _ImageApi()
        self._close_handle = self._api.close_handle
        self._name = _normalized_name(path)
        raw = cast(
            wintypes.HANDLE,
            self._api.create_file(
                self._name,
                _GENERIC_READ,
                _FILE_SHARE_READ,
                None,
                _OPEN_EXISTING,
                _FILE_ATTRIBUTE_NORMAL,
                wintypes.HANDLE(),
            ),
        )
        self.handle = _handle_value(raw, "CreateFileW")

    def __enter__(self) -> _RetainedGitExecutableFile:
        return self


def test_git_file_retention_preserves_m223_boundary() -> None:
    real_which = _commit_module.shutil.which
    with patch.object(
        _commit_module.shutil,
        "which",
        side_effect=real_which,
    ) as lookup:
        git_executable = _commit_module._git_executable()  # pyright: ignore[reportPrivateUsage]
    assert lookup.call_count == 1

    with _RetainedGitExecutableFile(git_executable) as retained:
        before = retained.snapshot()
        if Path(before.normalized_name) != git_executable:
            raise RuntimeError("retained Git executable path was not canonical") from None
        with patch.object(
            _commit_module, "_git_executable", return_value=git_executable
        ) as selection:
            _selection_module._require_git_selection_bound_m222_boundary()  # pyright: ignore[reportPrivateUsage]
        assert selection.call_count == 1
        _verify_image_stable(before, retained.snapshot())

    with _RetainedImageFile(git_executable) as settled:
        _verify_image_stable(before, settled.snapshot())


def test_git_file_retainer_refuses_replacement_access_without_mutation() -> None:
    probe_file = Path(__file__).resolve(strict=True)
    with _RetainedGitExecutableFile(probe_file) as retained:
        before = retained.snapshot()
        _require_source_access_refused(probe_file, phase="retained_probe")
        _verify_image_stable(before, retained.snapshot())

    _require_source_access_allowed(probe_file)
    with _RetainedImageFile(probe_file) as settled:
        _verify_image_stable(before, settled.snapshot())
