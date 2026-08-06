"""Keep M24 corpus admission evidence strict, local, and outside runtime source."""

import ast
import hashlib
import json
import tomllib
from pathlib import Path
from typing import cast

import pytest

import ludoweave

_ROOT = Path(__file__).parents[2]
_CORPUS = _ROOT / "tests" / "fixtures" / "cross_version_receipt_corpus.json"
_SOURCE_MANIFEST = _ROOT / "tests" / "fixtures" / "receipt_v1" / "manifest.json"
_EVIDENCE_FILES = (
    _ROOT / "examples" / "cross_version_corpus_readiness.py",
    _ROOT / "scripts" / "cross_version_corpus_evidence.py",
)
_FORBIDDEN_IMPORTS = {
    "http",
    "importlib",
    "multiprocessing",
    "numpy",
    "os",
    "requests",
    "socket",
    "sqlite3",
    "subprocess",
    "time",
    "urllib",
    "webbrowser",
    "ludoweave.plugins",
    "ludoweave.render.backends",
    "ludoweave.tools",
}
_GRAPHICS_DEPENDENCIES = [
    "glfw==2.10.2",
    "rendercanvas[glfw]==2.7.2",
    "wgpu==0.32.0",
]


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.add(node.module)
    return imports


def _forbidden(imports: set[str]) -> set[str]:
    return {
        imported
        for imported in imports
        if any(imported == name or imported.startswith(f"{name}.") for name in _FORBIDDEN_IMPORTS)
    }


def _literal(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for statement in tree.body:
        if isinstance(statement, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in statement.targets
        ):
            return ast.literal_eval(statement.value)
        if (
            isinstance(statement, ast.AnnAssign)
            and isinstance(statement.target, ast.Name)
            and statement.target.id == name
            and statement.value is not None
        ):
            return ast.literal_eval(statement.value)
    raise AssertionError(f"{name} was not a literal assignment")


def test_admission_manifest_is_exact_and_preserves_m21_identity() -> None:
    payload = _CORPUS.read_bytes()
    document = cast(dict[str, object], json.loads(payload))
    source_payload = _SOURCE_MANIFEST.read_bytes()

    assert len(payload) == 434
    assert hashlib.sha256(payload).hexdigest() == (
        "0b1d7b9f68b49ad1f6ab21cff4f744140cf3a16b52c6cdebd691b28b375a72ae"
    )
    assert _literal(_EVIDENCE_FILES[0], "_REVIEWED_CORPUS_SHA256") == (
        "0b1d7b9f68b49ad1f6ab21cff4f744140cf3a16b52c6cdebd691b28b375a72ae"
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_SOURCE_PREFIX") == (
        (
            "receipt_v1",
            "0.1.0a1",
            762,
            "ed3f1040294376fafce523e129897ce756d785b2f6d90c54335ad5f8abb84ac3",
        ),
    )
    assert _literal(_EVIDENCE_FILES[0], "_MANDATORY_RELEASE_PREFIX") == ()
    assert document == {
        "schema": "ludoweave.compatibility.cross-version-receipt-corpus/1",
        "source_package": "ludoweave",
        "receipt_protocol": "ludoweave.receipt/1",
        "minimum_distinct_observed_versions": 2,
        "source_manifests": [
            {
                "directory": "receipt_v1",
                "source_version": "0.1.0a1",
                "bytes": 762,
                "sha256": ("ed3f1040294376fafce523e129897ce756d785b2f6d90c54335ad5f8abb84ac3"),
            }
        ],
        "supported_releases": [],
    }
    assert len(source_payload) == 762
    assert hashlib.sha256(source_payload).hexdigest() == (
        "ed3f1040294376fafce523e129897ce756d785b2f6d90c54335ad5f8abb84ac3"
    )


def test_evidence_files_have_no_ambient_execution_or_provider_dependency() -> None:
    for path in _EVIDENCE_FILES:
        assert _forbidden(_imports(path)) == set()


@pytest.mark.parametrize(
    "source",
    [
        "def nested() -> None:\n    import socket\n",
        "if True:\n    from importlib import import_module\n",
        "try:\n    import subprocess\nexcept ImportError:\n    pass\n",
        "from ludoweave.tools import cli\n",
        "from ludoweave.render.backends.wgpu import WgpuRenderDevice\n",
    ],
)
def test_import_scan_detects_nested_forbidden_fixtures(tmp_path: Path, source: str) -> None:
    fixture = tmp_path / "invalid_evidence.py"
    fixture.write_text(source, encoding="utf-8")

    assert _forbidden(_imports(fixture))


def test_m24_adds_no_runtime_export_dependency_version_or_provider() -> None:
    document = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = cast(dict[str, object], document["project"])

    assert project["version"] == "0.1.0a1"
    assert project["dependencies"] == []
    assert project["optional-dependencies"] == {"graphics": _GRAPHICS_DEPENDENCIES}
    assert "CrossVersionCorpus" not in ludoweave.__all__
