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
| Done | M15 visual-editor admission decision | Hosted-validated installed semantic-mutation evidence, retained headless inspector, complete authoring/support gate, and no GUI/editor implementation |
| Done | M16 WASM-mod security admission decision | Hosted-validated installed inert-boundary evidence, prospective threat model, complete security/determinism gate, and no runtime or guest execution |
| Done | M17 installed render-device conformance | Versioned explicit-factory baseline, Null/wgpu evidence, isolated artifact smoke, and unchanged essential CI topology |
| Done | M18 installed agent-tool conformance | Hosted-validated explicit-factory 12-tool baseline, direct-service artifact evidence, and unchanged essential CI topology |
| Done | M19 installed WorldStore conformance | Hosted-validated versioned explicit-factory storage baseline, production/reference artifact evidence, and unchanged essential CI topology |
| In progress | M20 command/receipt stability decision | Installed same-version evidence, complete preview gate, RFC-0003 decision, and unchanged runtime/CI topology |

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
PR #16 squash-integrated the exact validated M8-M14 tree into `main` as
verified commit `2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`. Stacked PRs
#9-#15 are closed as superseded; their branches remain as audit history.
PR #18 integrated the repository-state evidence as verified main commit
`bfea67d2d922e8c591224d18f56c14d572d7f7da`; M15 starts from that exact base.
M15 ready PR #19 passed the unchanged eight-job hosted matrix as run
`31036925179` on implementation commit
`7e85570056dde3678aaeee13eee4036067876d8c`.
PR #19 squash-integrated the exact final M15 tree into `main` as verified
commit `c013dad38b1b64f0f4ccddc19681d643f6414427`. M16 starts from that
exact clean base and treats WASM mods as a separate security decision, not a
runtime implementation.
M16 ready PR #20 passed the unchanged eight-job hosted matrix as run
`31039403209` on implementation commit
`bcaf78fbc78bda8a13a95e397ab15d003dd4a6ce`.
PR #20 squash-integrated exact final M16 head
`808e48a5cb2727c8e1f4d7e896c4f8c7d41bfe1a` into `main` as verified commit
`e2bd57c057c0c16861953c0702b2012c4cabfe90`; both trees are
`05367be9bd85014fe6c70995ac1a69a39f90ef1e`.
M17 starts from integrated `main` commit
`27d2ee9d1f7f75dacc17568650f00ce833ef4fce`. It turns the existing
`RenderDevice` checklist into one installed baseline profile. The profile
executes only an explicitly supplied trusted factory and does not discover,
load, install, sandbox, or certify third-party code. Project-owned Null/wgpu
passes do not count as independent third-party adoption.
Ready PR #22 passed the unchanged eight-job hosted matrix as run
`31042903689` on DCO-signed implementation commit
`8e592f329424719214239bf97bd85dad9c9c5928`. PR #22 squash-integrated exact
final evidence head `148600cdaf9c419fbf552c68f833e0d55655731f` into
`main` as GitHub-verified commit
`610261c8450afc3d7db6ebb2b0425a1829737aec`; both trees are
`1e82568a463c62d0a1cf988b67eea09885ec50e3`.
M18 starts from integrated `main` commit
`ed65b12fa02f672113eac5939a0f616079fee44a`. It turns the existing internal
agent-service acceptance loop into one installed baseline for an explicitly
supplied trusted adapter factory. It does not discover, load, install, launch,
connect to, sandbox, certify, or admit third-party code, and project-owned
direct-service evidence does not count as independent adoption.
Ready PR #24 passed the unchanged eight-job hosted matrix as run
`31046172544` on DCO-signed implementation commit
`c4dde705393eebb7c99af428745e9383750f6b4d`.
PR #24 squash-integrated exact final evidence head
`cb617be0f678528fadc82877ec6910e42c6daf6b` into `main` as GitHub-verified
commit `1000d362432f19c912edf51c67e29c79bf444443`; both trees are
`1b6676ca7c1a6aaa223057a35e0c95242f4e9462`.
M19 starts from integrated `main` commit
`4076f3d7ac0c0a82834a1c98dcb36426ba67ac5e`. It turns existing private
production/reference storage conformance into one installed profile for an
explicitly supplied trusted `factory(ComponentRegistry)`. It does not discover,
load, install, sandbox, certify, or admit code and adds no backend or storage
format. Ready PR #26 passed the unchanged eight-job hosted matrix as run
`31092244573` on DCO-signed implementation commit
`1da692a693c1f92e10b676c2d4539354ce3ff59f`.
PR #26 squash-integrated exact final evidence head
`b93ca591f7063a1500cf105e6b0496b33573c69a` into `main` as GitHub-verified
commit `1a7219e540d8f4cb3c1f60ff12981513c6860ef9`; both trees are
`7fcd614fdde76daf1807f27dbe78ec306a501cc3`.
M20 starts from integrated `main` commit
`2fdeccd697f09f3e165130eb8564a6c585d472d2`. It evaluates whether the
installed command/transaction/receipt contracts are ready for preview without
changing their runtime or wire formats. RFC-0003 retains experimental status
until the complete cross-version, external-feedback, operation/receipt
evolution, bounded-reader, and supported-release-channel gate is evidenced.

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
rigid-body physics, network transports, international text shaping, automatic GPU
recovery. Constrained and general 3D are deferred under
[ADR-0028](docs/adr/0028-retain-layered-2d-and-defer-constrained-3d.md).
Visual-editor implementation is deferred under
[ADR-0029](docs/adr/0029-retain-headless-inspector-and-defer-visual-editor.md).
Executable WASM mods are deferred under
[ADR-0030](docs/adr/0030-retain-data-only-plugins-and-defer-wasm-mods.md).
Native acceleration is deferred under
[RFC-0001](docs/rfcs/0001-defer-first-native-kernel.md); its complete admission
and quantified revisit gate applies before another proposal.
