"""Data-only plugin manifest and compatibility contract tests."""

from __future__ import annotations

import json
import sys
from collections.abc import Iterable
from dataclasses import replace
from itertools import cycle, repeat
from typing import cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave.plugins import (
    PLUGIN_CHECK_PROTOCOL,
    PLUGIN_MANIFEST_PROTOCOL,
    PluginCapability,
    PluginCompatibilityContext,
    PluginCompatibilityError,
    PluginCompatibilityIssue,
    PluginCompatibilityReport,
    PluginDeterminism,
    PluginManifest,
    PluginManifestError,
    PluginPlatform,
    PluginRequirement,
    PythonVersionRange,
    VersionRange,
    check_plugin_compatibility,
    current_plugin_context,
)


class _AlwaysEqual:
    def __eq__(self, other: object) -> bool:
        return True


class _ProtocolText(str):
    pass


def _manifest(
    plugin_id: str = "org.example.render",
    *,
    plugin_version: str = "1.2.3",
    engine: VersionRange | None = None,
    python: PythonVersionRange | None = None,
    platforms: Iterable[PluginPlatform] = tuple(PluginPlatform),
    capabilities: Iterable[PluginCapability] = (PluginCapability.RENDER_DEVICE,),
    determinism: PluginDeterminism = PluginDeterminism.D0,
    native: bool = False,
    requires: Iterable[PluginRequirement] = (),
) -> PluginManifest:
    return PluginManifest(
        plugin_id=plugin_id,
        plugin_version=plugin_version,
        engine=engine or VersionRange("0.1.0a1", "0.2.0"),
        python=python or PythonVersionRange("3.12", "3.15"),
        platforms=cast(tuple[PluginPlatform, ...], platforms),
        capabilities=cast(tuple[PluginCapability, ...], capabilities),
        determinism=determinism,
        native=native,
        requires=cast(tuple[PluginRequirement, ...], requires),
    )


def _context(
    *,
    engine_version: str = "0.1.0a1",
    python_version: str = "3.12",
    python_implementation: str = "cpython",
    platform: PluginPlatform = PluginPlatform.LINUX,
    minimum_determinism: PluginDeterminism = PluginDeterminism.D0,
    allow_native: bool = False,
    supported_capabilities: Iterable[PluginCapability] = tuple(PluginCapability),
) -> PluginCompatibilityContext:
    return PluginCompatibilityContext(
        engine_version=engine_version,
        python_version=python_version,
        python_implementation=python_implementation,
        platform=platform,
        minimum_determinism=minimum_determinism,
        allow_native=allow_native,
        supported_capabilities=cast(tuple[PluginCapability, ...], supported_capabilities),
    )


def test_manifest_round_trip_is_canonical_and_order_independent() -> None:
    dependency = PluginRequirement("org.example.base", VersionRange("1.0.0", "2.0.0"))
    manifest = _manifest(
        platforms=(PluginPlatform.WINDOWS, PluginPlatform.LINUX, PluginPlatform.MACOS),
        capabilities=(PluginCapability.RENDER_DEVICE, PluginCapability.AGENT_CAPTURE),
        requires=(dependency,),
    )

    decoded = PluginManifest.from_json(manifest.canonical_bytes())

    assert decoded == manifest
    assert decoded.canonical_bytes() == manifest.canonical_bytes()
    assert decoded.fingerprint == manifest.fingerprint
    assert decoded.protocol == PLUGIN_MANIFEST_PROTOCOL
    assert decoded.platforms == tuple(PluginPlatform)
    assert decoded.capabilities == (
        PluginCapability.AGENT_CAPTURE,
        PluginCapability.RENDER_DEVICE,
    )
    assert b"module" not in decoded.canonical_bytes()


@pytest.mark.parametrize(
    "protocol",
    [
        _ProtocolText(PLUGIN_MANIFEST_PROTOCOL),
        _AlwaysEqual(),
    ],
    ids=["str-subclass", "hostile-equality"],
)
def test_persistent_protocols_require_exact_strings(protocol: object) -> None:
    with pytest.raises(PluginManifestError) as manifest_error:
        replace(_manifest(), protocol=cast(str, protocol))
    assert dict(manifest_error.value.details) == {"field": "protocol"}

    with pytest.raises(PluginCompatibilityError) as report_error:
        PluginCompatibilityReport(
            context=_context(),
            plugin_ids=("org.example.plugin",),
            manifest_fingerprint=f"sha256:{'0' * 64}",
            issues=(),
            protocol=cast(str, protocol),
        )
    assert dict(report_error.value.details) == {"field": "protocol"}


def test_release_and_python_ranges_use_half_open_ordering() -> None:
    alpha = VersionRange("0.1.0a1", "0.1.0")
    assert alpha.contains("0.1.0a1")
    assert alpha.contains("0.1.0rc1")
    assert not alpha.contains("0.1.0")
    python = PythonVersionRange("3.12", "3.15")
    assert python.contains("3.12")
    assert python.contains("3.14")
    assert not python.contains("3.15")


@pytest.mark.parametrize(
    "value",
    ["1", "1.2", "1.2.3.4", "v1.2.3", "1.2.3-dev", "01.2.3", "1.02.3"],
)
def test_invalid_release_versions_are_rejected(value: str) -> None:
    with pytest.raises(PluginManifestError):
        VersionRange(value, "2.0.0")


@given(st.text(max_size=80))
def test_version_parser_never_leaks_unstructured_failures(value: str) -> None:
    try:
        VersionRange(value, "999.0.0")
    except PluginManifestError as error:
        assert error.code == "plugins.invalid_manifest"


def test_manifest_rejects_extra_executable_fields_and_unknown_values() -> None:
    document = _manifest().as_dict()
    document["module"] = "malicious.module"
    with pytest.raises(PluginManifestError, match="fields"):
        PluginManifest.from_mapping(document)

    document = _manifest().as_dict()
    document["capabilities"] = ["physics.backend"]
    with pytest.raises(PluginManifestError, match="unsupported"):
        PluginManifest.from_mapping(document)

    document = _manifest().as_dict()
    document["protocol"] = "ludoweave.plugin-manifest/999"
    with pytest.raises(PluginManifestError, match="incompatible"):
        PluginManifest.from_mapping(document)


def test_invalid_manifest_diagnostics_do_not_echo_untrusted_text() -> None:
    document = _manifest().as_dict()
    document["credential_super_secret"] = "do-not-echo"
    with pytest.raises(PluginManifestError) as extra:
        PluginManifest.from_mapping(document)
    rendered = json.dumps(extra.value.as_dict())
    assert "credential_super_secret" not in rendered
    assert "do-not-echo" not in rendered

    document = _manifest().as_dict()
    document["capabilities"] = ["credential.secret-value"]
    with pytest.raises(PluginManifestError) as capability:
        PluginManifest.from_mapping(document)
    assert "credential.secret-value" not in json.dumps(capability.value.as_dict())

    document = _manifest().as_dict()
    document["protocol"] = "credential-secret-protocol"
    with pytest.raises(PluginManifestError) as protocol:
        PluginManifest.from_mapping(document)
    assert "credential-secret-protocol" not in json.dumps(protocol.value.as_dict())


def test_manifest_rejects_mixed_key_types_with_a_structured_error() -> None:
    document = cast(dict[object, object], _manifest().as_dict())
    document[1] = "untrusted"
    document["unexpected"] = "untrusted"

    with pytest.raises(PluginManifestError) as raised:
        PluginManifest.from_mapping(document)

    assert raised.value.code == "plugins.invalid_manifest"
    assert raised.value.phase == "decode"


@pytest.mark.parametrize(
    ("field", "count", "item"),
    [
        ("platforms", 4, "linux"),
        ("capabilities", 17, "render.device"),
        ("requires", 65, {}),
    ],
)
def test_direct_manifest_mappings_bound_arrays_before_decoding(
    field: str, count: int, item: object
) -> None:
    document = cast(dict[str, object], _manifest().as_dict())
    document[field] = [item] * count

    with pytest.raises(PluginManifestError, match="item limit") as raised:
        PluginManifest.from_mapping(document)

    assert dict(raised.value.details)["actual"] == count


@pytest.mark.parametrize(
    "plugin_id",
    ["example", "Org.Example.Plugin", "org..plugin", ".org.plugin", "org.plugin_unsafe"],
)
def test_plugin_identity_is_strict(plugin_id: str) -> None:
    with pytest.raises(PluginManifestError):
        _manifest(plugin_id)


def test_manifest_collections_are_bounded_before_complete_materialization() -> None:
    with pytest.raises(PluginManifestError, match="item limit"):
        _manifest(capabilities=cycle((PluginCapability.RENDER_DEVICE,)))
    with pytest.raises(PluginManifestError, match="item limit"):
        _manifest(
            requires=repeat(PluginRequirement("org.example.base", VersionRange("1.0.0", "2.0.0")))
        )


def test_requirements_are_unique_and_cannot_be_self_referential() -> None:
    requirement = PluginRequirement("org.example.base", VersionRange("1.0.0", "2.0.0"))
    with pytest.raises(PluginManifestError, match="unique"):
        _manifest(requires=(requirement, requirement))
    with pytest.raises(PluginManifestError, match="require itself"):
        _manifest(
            requires=(PluginRequirement("org.example.render", VersionRange("1.0.0", "2.0.0")),)
        )


def test_malformed_and_oversized_json_are_structured() -> None:
    with pytest.raises(PluginManifestError) as malformed:
        PluginManifest.from_json(b"{")
    assert malformed.value.code == "plugins.invalid_manifest"
    with pytest.raises(PluginManifestError) as oversized:
        PluginManifest.from_json(b" " * 65_537)
    assert oversized.value.code == "plugins.invalid_manifest"


def test_compatible_dependency_set_has_repeatable_report() -> None:
    base = _manifest(
        "org.example.base",
        plugin_version="1.5.0",
        capabilities=(PluginCapability.RESOURCE_ADAPTER,),
        determinism=PluginDeterminism.D2,
    )
    dependent = _manifest(
        requires=(PluginRequirement(base.plugin_id, VersionRange("1.0.0", "2.0.0")),),
    )
    context = _context()

    forward = check_plugin_compatibility((base, dependent), context)
    reverse = check_plugin_compatibility((dependent, base), context)

    assert forward.compatible
    assert forward.protocol == PLUGIN_CHECK_PROTOCOL
    assert forward.plugin_ids == ("org.example.base", "org.example.render")
    assert forward.canonical_bytes() == reverse.canonical_bytes()
    assert forward.manifest_fingerprint == reverse.manifest_fingerprint


def test_environment_and_policy_incompatibilities_are_complete() -> None:
    manifest = _manifest(
        engine=VersionRange("0.2.0", "0.3.0"),
        python=PythonVersionRange("3.12", "3.13"),
        platforms=(PluginPlatform.LINUX,),
        capabilities=(PluginCapability.RENDER_DEVICE,),
        determinism=PluginDeterminism.D0,
        native=True,
    )
    context = _context(
        python_version="3.14",
        python_implementation="pypy",
        platform=PluginPlatform.WINDOWS,
        minimum_determinism=PluginDeterminism.D2,
        supported_capabilities=(PluginCapability.AUDIO_BACKEND,),
    )

    report = check_plugin_compatibility((manifest,), context)

    assert not report.compatible
    assert {issue.code for issue in report.issues} == {
        "plugins.compatibility.capability",
        "plugins.compatibility.determinism",
        "plugins.compatibility.engine_version",
        "plugins.compatibility.native_forbidden",
        "plugins.compatibility.platform",
        "plugins.compatibility.python_implementation",
        "plugins.compatibility.python_version",
    }


def test_missing_wrong_version_duplicate_and_ambiguous_dependencies_are_reported() -> None:
    requirement = PluginRequirement("org.example.base", VersionRange("2.0.0", "3.0.0"))
    dependent = _manifest(requires=(requirement,))
    missing = check_plugin_compatibility((dependent,), _context())
    assert [issue.code for issue in missing.issues] == ["plugins.compatibility.dependency_missing"]

    base = _manifest(
        "org.example.base",
        plugin_version="1.0.0",
        capabilities=(PluginCapability.RESOURCE_ADAPTER,),
    )
    wrong = check_plugin_compatibility((base, dependent), _context())
    assert "plugins.compatibility.dependency_version" in {issue.code for issue in wrong.issues}

    duplicate = replace(base, plugin_version="1.1.0")
    ambiguous = check_plugin_compatibility((base, duplicate, dependent), _context())
    assert {issue.code for issue in ambiguous.issues} == {
        "plugins.compatibility.dependency_ambiguous",
        "plugins.compatibility.duplicate_id",
    }


def test_dependency_cycles_are_reported_for_every_member() -> None:
    left = _manifest(
        "org.example.left",
        requires=(PluginRequirement("org.example.right", VersionRange("1.0.0", "2.0.0")),),
    )
    right = _manifest(
        "org.example.right",
        requires=(PluginRequirement("org.example.left", VersionRange("1.0.0", "2.0.0")),),
    )

    report = check_plugin_compatibility((right, left), _context())

    cycle_issues = [
        issue for issue in report.issues if issue.code == "plugins.compatibility.dependency_cycle"
    ]
    assert [issue.plugin_id for issue in cycle_issues] == [
        "org.example.left",
        "org.example.right",
    ]
    details = [dict(issue.details) for issue in cycle_issues]
    assert {item["cycle_size"] for item in details} == {2}
    assert len({item["cycle_fingerprint"] for item in details}) == 1
    assert str(details[0]["cycle_fingerprint"]).startswith("sha256:")


def test_maximum_dependency_cycle_returns_a_bounded_report() -> None:
    plugin_ids = tuple(f"org.example.plugin-{index:02d}" for index in range(64))
    manifests = tuple(
        _manifest(
            plugin_id,
            requires=(
                PluginRequirement(
                    plugin_ids[(index + 1) % len(plugin_ids)],
                    VersionRange("1.0.0", "2.0.0"),
                ),
            ),
        )
        for index, plugin_id in enumerate(plugin_ids)
    )

    report = check_plugin_compatibility(manifests, _context())

    cycle_issues = tuple(
        issue for issue in report.issues if issue.code == "plugins.compatibility.dependency_cycle"
    )
    assert len(cycle_issues) == 64
    assert {dict(issue.details)["cycle_size"] for issue in cycle_issues} == {64}
    assert len({dict(issue.details)["cycle_fingerprint"] for issue in cycle_issues}) == 1
    assert report.canonical_bytes()


def test_compatibility_inputs_are_bounded_and_exact() -> None:
    with pytest.raises(PluginCompatibilityError, match="item limit"):
        check_plugin_compatibility(repeat(_manifest()), _context())
    with pytest.raises(PluginCompatibilityError, match="wrong value type"):
        check_plugin_compatibility(cast(Iterable[PluginManifest], (object(),)), _context())
    with pytest.raises(PluginCompatibilityError, match="exact compatibility context"):
        check_plugin_compatibility((_manifest(),), cast(PluginCompatibilityContext, object()))


@pytest.mark.parametrize(
    ("field", "value"),
    [("engine_version", "bad"), ("python_version", "bad")],
)
def test_invalid_context_versions_raise_compatibility_errors(field: str, value: str) -> None:
    with pytest.raises(PluginCompatibilityError) as raised:
        if field == "engine_version":
            _context(engine_version=value)
        else:
            _context(python_version=value)

    assert raised.value.code == "plugins.invalid_compatibility_request"
    assert raised.value.phase == "configure"
    assert dict(raised.value.details) == {"field": field}
    assert isinstance(raised.value.__cause__, PluginManifestError)


@pytest.mark.parametrize("value", [2**100, chr(233) * 512, "\ud800"])
def test_issue_details_reject_values_outside_canonical_json_limits(value: str | int) -> None:
    with pytest.raises(PluginCompatibilityError):
        PluginCompatibilityIssue(
            "plugins.compatibility.test",
            "org.example.plugin",
            (("value", value),),
        )


def test_report_and_issue_reject_non_exact_or_sensitive_plugin_identities() -> None:
    with pytest.raises(PluginCompatibilityError):
        PluginCompatibilityIssue(
            "plugins.compatibility.test",
            r"C:\secret\manifest.json",
        )

    with pytest.raises(PluginCompatibilityError):
        PluginCompatibilityReport(
            context=_context(),
            plugin_ids=cast(tuple[str, ...], "abc"),
            manifest_fingerprint=f"sha256:{'0' * 64}",
            issues=(),
        )


def test_compatibility_collections_reject_text_instead_of_coercing_it() -> None:
    with pytest.raises(PluginCompatibilityError):
        PluginCompatibilityIssue(
            "plugins.compatibility.test",
            "org.example.plugin",
            cast(tuple[tuple[str, str], ...], ""),
        )

    with pytest.raises(PluginCompatibilityError):
        PluginCompatibilityReport(
            context=_context(),
            plugin_ids=("org.example.plugin",),
            manifest_fingerprint=f"sha256:{'0' * 64}",
            issues=cast(tuple[PluginCompatibilityIssue, ...], ""),
        )


def test_report_construction_enforces_aggregate_canonical_limits() -> None:
    details = tuple((f"value_{index}", "x" * 512) for index in range(16))
    issue = PluginCompatibilityIssue(
        "plugins.compatibility.test",
        "org.example.plugin",
        details,
    )

    with pytest.raises(PluginCompatibilityError, match="canonically serializable") as raised:
        PluginCompatibilityReport(
            context=_context(),
            plugin_ids=("org.example.plugin",),
            manifest_fingerprint=f"sha256:{'0' * 64}",
            issues=(issue,) * 6_000,
        )

    assert raised.value.phase == "report"
    assert raised.value.__cause__ is not None


@pytest.mark.parametrize(
    "protocol",
    ["x" * 100_000, b"not-json"],
    ids=["oversized-text", "non-json-bytes"],
)
def test_report_rejects_protocol_without_echoing_untrusted_value(protocol: object) -> None:
    with pytest.raises(PluginCompatibilityError) as raised:
        PluginCompatibilityReport(
            context=_context(),
            plugin_ids=("org.example.plugin",),
            manifest_fingerprint=f"sha256:{'0' * 64}",
            issues=(),
            protocol=cast(str, protocol),
        )

    assert dict(raised.value.details) == {"field": "protocol"}
    assert protocol not in raised.value.details


def test_maximum_dependency_work_produces_a_bounded_serializable_report() -> None:
    requirements = tuple(
        PluginRequirement(f"org.missing.dep-{index}", VersionRange("1.0.0", "2.0.0"))
        for index in range(64)
    )
    manifests = tuple(
        _manifest(f"org.example.plugin-{index}", requires=requirements) for index in range(64)
    )

    report = check_plugin_compatibility(manifests, _context())

    assert not report.compatible
    assert len(report.issues) == 4_096
    assert len(report.canonical_bytes()) < 4_194_304


def test_current_context_contains_only_normalized_supported_facts() -> None:
    context = current_plugin_context()
    document = context.as_dict()
    assert context.python_implementation == "cpython"
    assert context.platform in tuple(PluginPlatform)
    assert document["engine_version"] == "0.1.0a1"
    assert set(document) == {
        "allow_native",
        "engine_version",
        "minimum_determinism",
        "platform",
        "python_implementation",
        "python_version",
        "supported_capabilities",
    }


def test_current_context_does_not_echo_an_unsupported_platform(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sensitive_platform = r"C:\private\credential-token.txt"
    monkeypatch.setattr(sys, "platform", sensitive_platform)

    with pytest.raises(PluginCompatibilityError) as raised:
        current_plugin_context()

    assert dict(raised.value.details) == {"field": "platform"}
    assert sensitive_platform not in str(raised.value.as_dict())


def test_manifest_json_has_exact_expected_fields() -> None:
    document = cast(dict[str, object], json.loads(_manifest().canonical_bytes()))
    assert set(document) == {
        "capabilities",
        "determinism",
        "engine",
        "native",
        "platforms",
        "plugin_id",
        "plugin_version",
        "protocol",
        "python",
        "requires",
    }
