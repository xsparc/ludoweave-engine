"""Stage deterministic community-alpha artifacts, SPDX SBOM, and checksums."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tomllib
import zipfile
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import cast

_SAMPLE_FILES = (
    "README.md",
    "agent_tool_recovery_rate_readiness.py",
    "agent_tool_conformance.py",
    "agent_world_builder.py",
    "alpha_acceptance.py",
    "benchmark_regression_rate_readiness.py",
    "clockwork_arena.assets.json",
    "clockwork_arena.py",
    "command_receipt_stability_decision.py",
    "constrained_3d_decision.py",
    "cross_version_corpus_readiness.py",
    "example.plugin.json",
    "external_contributor_rehearsal_readiness.py",
    "external_contributor_retention_readiness.py",
    "external_consumer_feedback_readiness.py",
    "external_sample_game_adoption_readiness.py",
    "fixed_step_world.py",
    "hello_headless.py",
    "hello_sprite.py",
    "installation_matrix_readiness.py",
    "operation_argument_compatibility.py",
    "render_device_conformance.py",
    "receipt_reader.py",
    "receipt_semantic_compatibility.py",
    "replay_divergence_rate_readiness.py",
    "response_review_latency_readiness.py",
    "rich_2d_showcase.py",
    "rollback_readiness.py",
    "supported_release_channel_readiness.py",
    "visual_editor_decision.py",
    "wasm_mod_security_decision.py",
    "world_store_conformance.py",
)
_COPY_FILES = ("LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md")
_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist", type=Path, help="directory containing one wheel and one sdist")
    parser.add_argument("output", type=Path, help="new empty release staging directory")
    parser.add_argument("--tag", help="optional exact vVERSION release tag to verify")
    args = parser.parse_args(argv)
    dist = _path_argument(args, "dist").resolve()
    output = _path_argument(args, "output").resolve()
    tag = _optional_text_argument(args, "tag")
    root = Path(__file__).resolve().parents[1]
    project = _object(tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8")))[
        "project"
    ]
    project_table = _object(project)
    version = _text(project_table["version"], field="project.version")
    release = _object(
        _object(tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8")))["tool"]
    )["ludoweave"]
    release_table = _object(_object(release)["release"])
    release_date = _text(release_table["date"], field="tool.ludoweave.release.date")
    if tag is not None and tag != f"v{version}":
        parser.error(f"release tag {tag!r} does not match package version v{version}")
    if output.exists() and any(output.iterdir()):
        parser.error("output directory must be empty")
    output.mkdir(parents=True, exist_ok=True)

    wheel = _one(dist.glob(f"ludoweave-{version}-*.whl"), "wheel")
    sdist = _one(dist.glob(f"ludoweave-{version}.tar.gz"), "source distribution")
    if f"-{version}-" not in wheel.name or f"-{version}." not in sdist.name:
        parser.error("built distribution filenames do not match project version")
    if not wheel.name.endswith("-py3-none-any.whl"):
        parser.error("community-alpha baseline wheel must remain pure Python")

    staged: list[Path] = []
    for source in (wheel, sdist):
        target = output / source.name
        shutil.copyfile(source, target)
        staged.append(target)
    for name in _COPY_FILES:
        target = output / name
        shutil.copyfile(root / name, target)
        staged.append(target)
    notes = output / "RELEASE_NOTES.md"
    shutil.copyfile(root / "docs" / "releases" / f"{version}.md", notes)
    staged.append(notes)

    sample_bundle = output / f"ludoweave-samples-{version}.zip"
    _write_sample_bundle(root, sample_bundle, version)
    staged.append(sample_bundle)

    sbom = output / f"ludoweave-{version}.spdx.json"
    _write_sbom(sbom, wheel=output / wheel.name, version=version, release_date=release_date)
    staged.append(sbom)

    manifest = output / "RELEASE_MANIFEST.json"
    manifest_document = {
        "protocol": "ludoweave.release-manifest/1",
        "version": version,
        "release_date": release_date,
        "artifacts": [_artifact(path) for path in sorted(staged, key=lambda path: path.name)],
    }
    manifest.write_text(_json(manifest_document), encoding="utf-8", newline="\n")

    checksums = output / "SHA256SUMS"
    checksum_subjects = sorted(
        (path for path in output.iterdir() if path.is_file() and path != checksums),
        key=lambda path: path.name,
    )
    checksums.write_text(
        "".join(f"{_sha256(path)}  {path.name}\n" for path in checksum_subjects),
        encoding="ascii",
        newline="\n",
    )
    print(
        _json(
            {
                "protocol": "ludoweave.release-stage/1",
                "version": version,
                "artifacts": len(checksum_subjects) + 1,
                "sample_bundle": sample_bundle.name,
                "sbom": sbom.name,
            }
        ).strip()
    )
    return 0


def _write_sample_bundle(root: Path, output: Path, version: str) -> None:
    sample_root = root / "examples"
    sources = [(sample_root / name, Path(name)) for name in _SAMPLE_FILES]
    sources.extend(
        (source, source.relative_to(sample_root))
        for source in sorted((sample_root / "assets").rglob("*"))
    )
    fixture_root = root / "tests" / "fixtures"
    sources.append(
        (
            fixture_root / "agent_tool_recovery_rate.json",
            Path("assets/agent_tool_recovery_rate.json"),
        )
    )
    sources.append(
        (
            fixture_root / "benchmark_regression_rate.json",
            Path("assets/benchmark_regression_rate.json"),
        )
    )
    sources.append(
        (
            fixture_root / "cross_version_receipt_corpus.json",
            Path("assets/cross_version_receipt_corpus.json"),
        )
    )
    sources.append(
        (
            fixture_root / "external_contributor_rehearsal.json",
            Path("assets/external_contributor_rehearsal.json"),
        )
    )
    sources.append(
        (
            fixture_root / "external_contributor_retention.json",
            Path("assets/external_contributor_retention.json"),
        )
    )
    sources.append(
        (
            fixture_root / "external_consumer_feedback.json",
            Path("assets/external_consumer_feedback.json"),
        )
    )
    sources.append(
        (
            fixture_root / "external_sample_game_adoption.json",
            Path("assets/external_sample_game_adoption.json"),
        )
    )
    sources.append(
        (
            fixture_root / "installation_matrix.json",
            Path("assets/installation_matrix.json"),
        )
    )
    sources.append(
        (
            fixture_root / "replay_divergence_rate.json",
            Path("assets/replay_divergence_rate.json"),
        )
    )
    sources.append(
        (
            fixture_root / "response_review_latency.json",
            Path("assets/response_review_latency.json"),
        )
    )
    sources.append(
        (
            fixture_root / "supported_release_channel.json",
            Path("assets/supported_release_channel.json"),
        )
    )
    sources.extend(
        (source, Path("assets/receipt_v1") / source.relative_to(fixture_root / "receipt_v1"))
        for source in sorted((fixture_root / "receipt_v1").rglob("*"))
    )
    prefix = f"ludoweave-samples-{version}"
    with zipfile.ZipFile(output, "w") as archive:
        for source, relative_path in sources:
            if not source.is_file():
                continue
            relative = relative_path.as_posix()
            info = zipfile.ZipInfo(f"{prefix}/{relative}", _ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, source.read_bytes(), compresslevel=9)


def _write_sbom(output: Path, *, wheel: Path, version: str, release_date: str) -> None:
    wheel_hash = _sha256(wheel)
    package_id = "SPDXRef-Package-ludoweave"
    file_id = "SPDXRef-File-wheel"
    document = {
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"ludoweave-{version}",
        "documentNamespace": (
            f"https://github.com/xsparc/ludoweave-engine/sbom/{version}/{wheel_hash}"
        ),
        "creationInfo": {
            "created": f"{release_date}T00:00:00Z",
            "creators": [
                "Organization: LudoWeave Engine contributors",
                "Tool: scripts/release_artifacts.py",
            ],
        },
        "packages": [
            {
                "name": "ludoweave",
                "SPDXID": package_id,
                "versionInfo": version,
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": True,
                "licenseConcluded": "Apache-2.0",
                "licenseDeclared": "Apache-2.0",
                "copyrightText": "Copyright 2026 LudoWeave Engine contributors",
                "checksums": [{"algorithm": "SHA256", "checksumValue": wheel_hash}],
                "externalRefs": [
                    {
                        "referenceCategory": "PACKAGE-MANAGER",
                        "referenceType": "purl",
                        "referenceLocator": f"pkg:pypi/ludoweave@{version}",
                    }
                ],
            }
        ],
        "files": [
            {
                "fileName": wheel.name,
                "SPDXID": file_id,
                "checksums": [{"algorithm": "SHA256", "checksumValue": wheel_hash}],
                "licenseConcluded": "Apache-2.0",
                "copyrightText": "Copyright 2026 LudoWeave Engine contributors",
            }
        ],
        "relationships": [
            {
                "spdxElementId": "SPDXRef-DOCUMENT",
                "relationshipType": "DESCRIBES",
                "relatedSpdxElement": package_id,
            },
            {
                "spdxElementId": package_id,
                "relationshipType": "CONTAINS",
                "relatedSpdxElement": file_id,
            },
        ],
    }
    output.write_text(_json(document), encoding="utf-8", newline="\n")


def _artifact(path: Path) -> dict[str, object]:
    return {"name": path.name, "bytes": path.stat().st_size, "sha256": _sha256(path)}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, indent=2) + "\n"


def _one(values: Iterable[Path], role: str) -> Path:
    paths = tuple(values)
    if len(paths) != 1:
        raise ValueError(f"expected exactly one {role}")
    return paths[0]


def _path_argument(args: argparse.Namespace, name: str) -> Path:
    value: object = getattr(args, name, None)
    if not isinstance(value, Path):
        raise TypeError(f"{name} must be a path")
    return value


def _optional_text_argument(args: argparse.Namespace, name: str) -> str | None:
    value: object = getattr(args, name, None)
    if value is None or isinstance(value, str):
        return value
    raise TypeError(f"{name} must be text")


def _object(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError("release configuration entry must be a table")
    return cast(dict[str, object], value)


def _text(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise TypeError(f"{field} must be non-empty text")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
