# AGENTS.md

This file is the operating contract for human and automated contributors to LudoWeave Engine.

## Read first

1. The assigned issue or milestone acceptance criteria.
2. `docs/architecture.md` and relevant accepted ADRs.
3. `.ai/PROJECT_STATE.md`, `.ai/CURRENT_TASK.md`, and `.ai/TEST_EVIDENCE.md`.
4. Current code, tests, CI, and `git status`.

## Authoritative rules

1. Canonical runtime state belongs to the ECS/world store as it is introduced through M1.
2. Headless execution is first-class.
3. Every externally initiated world mutation must eventually be a versioned command that produces a receipt.
4. Public APIs must not expose wgpu, GLFW, NumPy storage, or native extension objects.
5. No arbitrary Python evaluation or unauthenticated remote control.
6. Normal CPython 3.12-3.14 is the baseline; free-threaded builds are optional experiments.
7. Apache-2.0 and DCO sign-off govern contributions.
8. Never claim a check passed unless it was executed and its result was recorded.
9. Do not create empty speculative packages or abstractions without an exercised test or example.
10. Stop at the assigned milestone; do not opportunistically implement adjacent roadmap items.

## Dependency direction

Contracts and core code do not import application, tool, or concrete-backend modules. Application code depends on engine-owned protocols. Concrete adapters implement those protocols. CLI and examples are composition roots and may choose a concrete adapter. See ADR-0002 and the architecture tests.

## Working method

- Keep one task in progress and map changes to acceptance criteria.
- Preserve unrelated user changes and never use destructive Git commands to discard work.
- Add focused tests and public documentation with behavior changes.
- Run focused checks first, then every command in the README quality suite.
- Review the diff for scope growth, secrets, dependency violations, backend leakage, nondeterminism, packaging effects, and stale documentation.
- Update `.ai/PROJECT_STATE.md` and `.ai/TEST_EVIDENCE.md` with reproducible facts only.

## Current boundary

M0 through M20 are complete, independently accepted, hosted-CI validated, and
integrated into `main`.
M1-M7 are integrated into `main` by PR #8; M8-M14 are squash-integrated by PR
#16 as verified commit `2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa` with the
exact final M14 tree. Superseded stacked PRs #9 through #15 are closed and
their branches remain for audit history. M13 is only a bounded offline rollback/network-snapshot
readiness evaluation. M9 defers the Box2D v3 plugin. M10 adds only the headless
owned-child semantic inspector. M11 adds bounded headless 2D audio-mix,
bitmap-text, tick-animation, tilemap, and particle authoring through existing
backend-neutral extraction. M12 adds only strict data-only preview plugin
manifests, deterministic compatibility checks, and an explicitly invoked local
validation CLI. M13 proves immutable local correction branches and records the
external tick-input limitation; it may not add a transport or live
rollback service. M14 is only the installed-surface constrained-3D decision.
It retains layered 2D and adds evidence, tests, and documentation, but no
runtime package, public 3D contract, persistent format, provider, or dependency.
Repository-state evidence is integrated in `main` by PR #18 at
`bfea67d2d922e8c591224d18f56c14d572d7f7da`.
M15 retains the headless inspector and defers visual-editor implementation
under ADR-0029. Its evidence-only implementation is published through ready PR
#19 and validated by hosted run `31036925179`; it adds no runtime source,
public API, persistent format, dependency, lock, version, or CI change.
PR #19 squash-integrates the exact M15 tree as verified `main` commit
`c013dad38b1b64f0f4ccddc19681d643f6414427`. M16 is assigned only to a
WASM-mod security admission decision. It must retain data-only plugins and add
threat-model, installed evidence, tests, and documentation without selecting or
adding a runtime, loader, executable manifest field, guest ABI, WASI, host
function, public API, persistent format, dependency, lock, version, or CI job.
Its implementation is complete and independently accepted on
`codex/m16-wasm-mod-security-decision`. Ready PR #20 and GitHub Actions run
`31039403209` validate all eight unchanged essential jobs on DCO-signed
implementation commit `bcaf78fbc78bda8a13a95e397ab15d003dd4a6ce`.
PR #20 squash-integrates exact final head
`808e48a5cb2727c8e1f4d7e896c4f8c7d41bfe1a` into `main` as GitHub-verified
commit `e2bd57c057c0c16861953c0702b2012c4cabfe90` with the exact final tree.
M17 is assigned only to an installed `RenderDevice` baseline conformance
profile derived from the design plan's third-party-adoption metric. It accepts
an explicitly supplied trusted factory, returns sanitized versioned evidence,
and passes against Null plus the existing optional wgpu adapter through the
unchanged essential CI topology. Ready PR #22 and GitHub Actions run
`31042903689` validate all eight jobs on DCO-signed implementation commit
`8e592f329424719214239bf97bd85dad9c9c5928`. PR #22 squash-integrates final
evidence head `148600cdaf9c419fbf552c68f833e0d55655731f` into `main` as
GitHub-verified commit `610261c8450afc3d7db6ebb2b0425a1829737aec`
with the exact final tree.
It may not discover, dynamically import,
install, sandbox, certify, or admit provider code, change plugin manifests, or
add a concrete provider, dependency, lock, version, persistent world format,
canonical state, or package-root export. Do not add discovery, imports, hook execution,
installation/resolution, a global plugin registry, GUI/editor, sockets,
networking or remote attach, arbitrary child commands, another world store, a
Box2D adapter,
release tag, GitHub release, or PyPI publication. Real audio playback, font
parsing/shaping, network agent transports, editor work, constrained/general 3D,
SDL3, executable WASM, and native code remain out of scope.
RFC-0001 records the evidence-based native-code deferral; local performance
misses are not automatic authorization for acceleration.

M18 adds only an installed baseline conformance profile over the existing
12-tool transport-independent agent service. M19 is assigned only to an
installed baseline conformance profile over the existing public `WorldStore`
contract. It must accept an explicit trusted `factory(ComponentRegistry)`,
return sanitized versioned evidence, pass production and reference worlds
through isolated wheel/release smoke, and add no CI job. It may not discover,
import, install, or launch provider code; add a storage backend, database,
external-resource lifecycle, native/archetype/NumPy storage, format, plugin
field, dependency, lock, version, or package-root export; or claim project-
owned evidence as third-party adoption or certification.
Ready PR #26 and GitHub Actions run `31092244573` validate all eight unchanged
essential jobs on DCO-signed M19 implementation commit
`1da692a693c1f92e10b676c2d4539354ce3ff59f`. PR #26 squash-integrates exact
final evidence head `b93ca591f7063a1500cf105e6b0496b33573c69a` into `main` as
GitHub-verified commit `1a7219e540d8f4cb3c1f60ff12981513c6860ef9`; both trees are
`7fcd614fdde76daf1807f27dbe78ec306a501cc3`. M19 is complete; no M20 work was
included in it.

M20 adds only an installed command/receipt preview-readiness decision. It
confirms the current same-version canonical and atomic behavior, reuses the
existing M18 agent-tool profile, defines the complete compatibility gate, and
records the result under RFC-0003 through source, isolated-wheel, and release-
bundle evidence. It does not add or reinterpret a
command, operation, receipt field/reader, schema, migration, public runtime
symbol, stability label, root export, dependency, lock, package version, or CI
job. No external adoption, cross-version compatibility, tag, release,
publication, or certification may be claimed without direct evidence.
Ready PR #28 and GitHub Actions run `31095009029` validate all eight unchanged
essential jobs on DCO-signed M20 implementation commit
`d96d132da5ee847d6e86645be5e87a1e4aa5e89e`. PR #28 squash-integrates exact
final evidence head `d04561184996fac507071ad9e7dd0ef9c5e3cb7c` into `main` as
GitHub-verified commit `d166ef86bf25526d9d7715f63263d3cac6db78d4`; both trees are
`c3e2dc1224f530fb483d1b9684ff55329bf9557b`. M20 is complete; no M21 work is
included or assigned here.
