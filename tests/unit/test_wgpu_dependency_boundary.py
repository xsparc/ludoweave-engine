"""The optional graphics adapter fails through engine-owned diagnostics."""

from __future__ import annotations

import pytest

from ludoweave.core.errors import RenderError
from ludoweave.render.backends.wgpu import WgpuRenderDevice


def test_missing_graphics_extra_is_structured_and_chains_import_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    missing = ModuleNotFoundError("private provider detail")
    monkeypatch.setattr(
        "ludoweave.render.backends.wgpu._dependency_import_error",
        missing,
    )
    with pytest.raises(RenderError) as raised:
        WgpuRenderDevice()
    assert raised.value.code == "render.backend_dependency_missing"
    assert raised.value.phase == "initialize"
    assert raised.value.__cause__ is missing
    assert dict(raised.value.details) == {"install": "pip install ludoweave[graphics]"}
    assert "private provider detail" not in str(raised.value)
