"""Protect the M35 third-party conformance-adoption evidence boundary."""

import ast
import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_EXAMPLE = _ROOT / "examples" / "third_party_conformance_adoption_readiness.py"
_VALIDATOR = _ROOT / "scripts" / "third_party_conformance_adoption_evidence.py"
_MANIFEST = _ROOT / "tests" / "fixtures" / "third_party_conformance_adoption.json"
_GUIDE = _ROOT / "docs" / "third-party-conformance-adoption-readiness.md"
_RFC = _ROOT / "docs" / "rfcs" / "0018-third-party-conformance-adoption-readiness.md"
_BANNED_IMPORT_ROOTS = {
    "http",
    "importlib",
    "os",
    "requests",
    "socket",
    "subprocess",
    "urllib.request",
}


def _import_roots(path: Path) -> set[str]:
    roots: set[str] = set()
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            roots.add(node.module)
    return roots


def _banned_imports(source: str) -> set[str]:
    tree = ast.parse(source)
    found: set[str] = set()
    for node in ast.walk(tree):
        names: tuple[str, ...] = ()
        if isinstance(node, ast.Import):
            names = tuple(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            names = (node.module,)
        for name in names:
            if any(
                name == banned or name.startswith(f"{banned}.") for banned in _BANNED_IMPORT_ROOTS
            ):
                found.add(name)
    return found


def test_m35_evaluator_is_offline_and_synthetic_guard_proves_itself() -> None:
    source = _EXAMPLE.read_text(encoding="utf-8")

    assert _banned_imports(source) == set()
    assert _banned_imports("import requests\n") == {"requests"}
    assert _banned_imports("from urllib.request import urlopen\n") == {"urllib.request"}
    for forbidden in (
        "entry_points",
        "import_module",
        "urlopen",
        "Popen",
        "run(",
        "environ",
        "getenv",
        "site-packages",
    ):
        assert forbidden not in source


def test_m35_evaluator_imports_only_version_from_engine() -> None:
    roots = _import_roots(_EXAMPLE)

    assert (
        roots
        & {
            "ludoweave.agent",
            "ludoweave.ecs",
            "ludoweave.plugins",
            "ludoweave.render",
            "ludoweave.tools",
        }
        == set()
    )
    tree = ast.parse(_EXAMPLE.read_text(encoding="utf-8"))
    engine_imports = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "ludoweave"
    ]
    assert len(engine_imports) == 1
    assert [alias.name for alias in engine_imports[0].names] == ["__version__"]


def test_m35_fixes_only_existing_installed_profiles_and_reference_counts() -> None:
    source = _EXAMPLE.read_text(encoding="utf-8")

    for identity in (
        "ludoweave.render-device-conformance/1",
        "render-device-baseline/1",
        "ludoweave.agent-tool-conformance/1",
        "agent-tool-baseline/1",
        "ludoweave.world-store-conformance/1",
        "world-store-baseline/1",
    ):
        assert identity in source
    for count in (
        '"agent-tool-baseline/1",\n        12',
        '"render-device-baseline/1",\n        9',
        '"world-store-baseline/1",\n        10',
    ):
        assert count in source
    assert '"render-device-plugin"' in source
    assert '"agent-tool-plugin"' not in source
    assert '"world-store-plugin"' not in source


def test_m35_excludes_project_and_maintainer_evidence_before_outcome() -> None:
    source = _EXAMPLE.read_text(encoding="utf-8")
    relationship = source.index('record["relationship"]')
    project_owned = source.index('record["project_owned"]')
    maintainer_authored = source.index('record["maintainer_authored"]')
    outcome = source.index('record["outcome"]')

    assert relationship < outcome
    assert project_owned < outcome
    assert maintainer_authored < outcome
    assert "project-owned implementations are not third-party evidence" in source
    assert "maintainer-authored implementations are not third-party evidence" in source


def test_m35_preserves_nonpasses_history_and_sanitizes_output() -> None:
    source = _EXAMPLE.read_text(encoding="utf-8")

    for outcome in ("passed", "failed", "not-executed"):
        assert f'outcome == "{outcome}"' in source
    assert "_MANDATORY_SUBMISSION_PREFIX" in source
    assert "historical_submissions_preserved" in source
    return_block = source[
        source.index("    return {", source.index("def evaluate")) : source.index(
            "\n\n\ndef _parse_manifest"
        )
    ]
    for private_field in (
        "implementation_id",
        "package_id",
        "repository_url",
        "revision",
        "adapter_id",
        "review_url",
        "platform",
        "python_version",
    ):
        assert f'"{private_field}"' not in return_block


def test_m35_manifest_is_exact_empty_reviewed_evidence() -> None:
    payload = _MANIFEST.read_bytes()

    assert len(payload) == 250
    assert hashlib.sha256(payload).hexdigest() == (
        "adee8c68b5d89923ee2682162eb24cd9542a4601b1ff6fb901709ebcc0066767"
    )
    assert payload.endswith(b"\n")
    assert b'"submission_census_complete_reviewed":true' in payload
    assert b'"submissions":[]' in payload


def test_m35_changes_no_runtime_or_public_export_surface() -> None:
    runtime_files = tuple((_ROOT / "src" / "ludoweave").rglob("*.py"))
    for path in runtime_files:
        text = path.read_text(encoding="utf-8")
        assert "third_party_conformance" not in text
        assert "ThirdPartyConformance" not in text


def test_m35_release_artifacts_include_exact_evaluator_and_manifest() -> None:
    release = (_ROOT / "scripts" / "release_artifacts.py").read_text(encoding="utf-8")
    wheel_smoke = (_ROOT / "scripts" / "smoke_wheel.py").read_text(encoding="utf-8")
    release_smoke = (_ROOT / "scripts" / "smoke_release.py").read_text(encoding="utf-8")
    release_test = (_ROOT / "tests" / "unit" / "test_release_artifacts.py").read_text(
        encoding="utf-8"
    )

    for text in (release, wheel_smoke, release_smoke, release_test):
        assert "third_party_conformance_adoption" in text
    assert "validate_third_party_conformance_adoption_evidence" in wheel_smoke
    assert "validate_third_party_conformance_adoption_evidence" in release_smoke


def test_m35_public_docs_fix_zero_result_and_noncertification_boundary() -> None:
    guide = _GUIDE.read_text(encoding="utf-8")
    rfc = _RFC.read_text(encoding="utf-8")
    architecture = (_ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    readme = (_ROOT / "README.md").read_text(encoding="utf-8")
    roadmap = (_ROOT / "ROADMAP.md").read_text(encoding="utf-8")

    for text in (guide, rfc, architecture, readme, roadmap):
        assert "M35" in text
        assert "third-party" in text.casefold()
        assert "zero" in text.casefold()
    assert "does not discover packages" in guide
    assert "compatible manifest by itself" in guide
    assert "does not establish a complete support matrix" in guide
    assert "no runtime source" in guide
    assert "RFC-0018" in rfc


def test_m35_rfc_is_accepted_and_registered() -> None:
    rfc = _RFC.read_text(encoding="utf-8")
    index = (_ROOT / "docs" / "rfcs" / "index.md").read_text(encoding="utf-8")
    nav = (_ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    assert "**Status:** Accepted" in rfc
    assert "0018-third-party-conformance-adoption-readiness.md" in index
    assert "0018-third-party-conformance-adoption-readiness.md" in nav


def test_m35_uses_existing_ci_topology_and_records_only_filter() -> None:
    workflow = (_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "push:" not in workflow
    assert '      - ".project/**"' in workflow
    assert workflow.count("runs-on:") == 3
    assert "matrix.os" in workflow
    assert "matrix.python" in workflow
    assert "graphics" in workflow.casefold()


def test_m35_validator_has_no_engine_or_provider_dependency() -> None:
    roots = _import_roots(_VALIDATOR)

    assert all(not root.startswith("ludoweave") for root in roots)
    assert _banned_imports(_VALIDATOR.read_text(encoding="utf-8")) == set()
