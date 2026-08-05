# LudoWeave roadmap board

This repository-native board states outcomes and readiness; it is not a delivery-date
promise. Accepted ADRs and milestone acceptance evidence override an older card. Public
issues become the discussion and assignment record once a card is opened.

## Community-alpha release candidate

| Lane | Outcome | Evidence gate |
| --- | --- | --- |
| Done | M0 repository/runtime walking skeleton | Installed pure wheel and cross-platform CI |
| Done | M1 deterministic world core | Reference-model properties and benchmark evidence |
| Done | M2 command/snapshot/replay workflow | Artifact and installed-wheel scenario tests |
| Done | M3 isolated 2D presentation | Null/wgpu vertical slice and graphics CI |
| Done | M4 Clockwork Arena gameplay slice | 3,600-tick replay plus stress evidence |
| Done | M5 local typed agent interface | Agent World Builder and local stdio acceptance |
| Done | M6 community alpha | Release artifact, docs, API, security, and contribution gates |
| Done | M7 performance/native decision | Versioned profiles, ordinary Python optimization, RFC admission decision, and cross-platform smoke |
| Done | M8 gamepad/SDL3 evaluation | Provider-neutral gamepad mapping, pinned GLFW smoke, SDL3 maturity ADR, and cross-platform validation |
| Done | M9 Box2D v3 plugin evaluation | Binding/wheel/lifecycle/headless/API/threading/determinism/conformance admission evidence, ADR, and hosted validation |
| Done | M10 live semantic inspector | Separate local process, versioned semantic stream, command/query reuse, explicit write receipts, lifecycle/security bounds, and quota-conscious essential CI |
| Done | M11 rich 2D authoring | Headless tick animation, bitmap text, immutable tilemaps, fixed-point particles, Null-audio mixing, installed showcase, and hosted validation |
| Done | M12 plugin manifest compatibility | Canonical data-only manifests, deterministic environment/dependency checks, preview compatibility policy, installed CLI smoke, and hosted validation |
| Done | M13 rollback/network-snapshot readiness | Hosted-validated bounded correction-branch evidence, explicit input-history gap, network deferral ADR, and no transport implementation |
| Done | M14 constrained 3D decision | Hosted-validated installed-surface evidence, retained layered-2D scope, complete admission gate, and no 3D runtime implementation |

M6's implementation head passed hosted Windows, macOS, and Linux CI. Creating
or publishing the `v0.1.0a1` tag remains a separate maintainer release action.
M7's implementation head passed the same 14-job hosted matrix, including base
and real-wgpu profiling-contract smokes on all three operating systems.
M8 PR #9 passed the same 14-job hosted matrix, including standardized gamepad
contract and real GLFW smoke on all three operating systems. Haptics, sensors,
raw joysticks, remapping UI, and SDL windows remain future proposals.
M9 evaluates the external rigid-body candidate only. The dependency, adapter,
and canonical-physics integration remain absent unless every admission gate is
evidenced.
M9 PR #10 passed the same 14-job hosted matrix against the validated M8 branch.
The binding remains deferred and no dependency changed.
M10 is a headless protocol client, not a visual editor. It may spawn only the
built-in local stdio composition and cannot listen on a network interface.
M10 PR #11 passed its consolidated eight-job hosted matrix: one complete
quality/test/distribution gate, four compatibility jobs, and real graphics on
all three operating systems.
M11 is a bounded authoring and extraction slice, not a new world store. Real
audio playback, font parsing/shaping, editor-scale tile import, particle DSLs,
and provider objects remain deferred.
M11 PR #12 passed the consolidated eight-job hosted matrix on implementation
commit `aca6d93165a52d88451e8e06d5f1aa8d2e323f1d`.
M14 PR #15 passed the unchanged eight-job hosted matrix on implementation
commit `47443046834eb423be977973775f80494161533d`; layered 2D remains the
accepted scope and no runtime or dependency was added.

## Good-first contribution queue

These are issue-ready cards, not assigned work. A maintainer opens one with the
`good first issue`, `help wanted`, `status:ready`, and listed area labels before a
contributor starts.

| Card | Outcome | Scope | Acceptance |
| --- | --- | --- | --- |
| GF-01 glossary | Add a concise glossary for authority, canonical state, composition root, receipt, deterministic, presentation, and adapter | `docs/glossary.md`, `mkdocs.yml`; documentation only | Terms link to their defining guide/ADR; `uv run --frozen mkdocs build --strict` passes |
| GF-02 expected sample output | Add sanitized example JSON and explain stable versus diagnostic fields | `examples/README.md`; do not change sample behavior or protocols | Run the documented null examples and record matching output; docs build passes |
| GF-03 release checksum negative test | Add one focused test for an extra unlisted staged artifact | `tests/unit/test_release_artifacts.py`; no script/API change unless a demonstrated defect exists | Test fails against the intentional invalid fixture and full pytest passes |

Use the [good-first task form](.github/ISSUE_TEMPLATE/good_first_issue.yml) to propose
another card. The [triage contract](docs/triage.md) defines when it is ready.

## Proposal backlog

These areas remain uncommitted proposals and require milestone assignment plus the
design process in `GOVERNANCE.md`: general scene importers, production audio,
rigid-body physics, network transports, visual editor tooling, international text shaping, automatic GPU
recovery. Constrained and general 3D are deferred under
[ADR-0028](docs/adr/0028-retain-layered-2d-and-defer-constrained-3d.md).
Native acceleration is deferred under
[RFC-0001](docs/rfcs/0001-defer-first-native-kernel.md); its complete admission
and quantified revisit gate applies before another proposal.
