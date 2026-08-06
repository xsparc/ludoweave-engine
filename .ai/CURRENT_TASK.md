# Current Task

- **Task:** M19 - installed WorldStore conformance
- **Status:** Complete, hosted-validated, and squash-integrated into `main` by
  PR #26. No M20 implementation is assigned.
- **Started:** 2026-08-06
- **Base:** Exact clean synchronized `main` commit
  `4076f3d7ac0c0a82834a1c98dcb36426ba67ac5e`.
- **Outcome:** Give authors of storage-neutral ECS world implementations one
  small installed, versioned behavioral profile over the existing public
  `WorldStore` boundary without copying repository-private tests.
- **Acceptance gate:**
  - The public experimental runner accepts a bounded adapter ID and an
    explicitly supplied trusted `factory(ComponentRegistry)`. It performs no
    discovery, dynamic import, installation, filesystem scan, subprocess,
    network request, or global registration.
  - One fixed profile exercises exactly these ordered checks:
    `factory_registry`, `empty_state`, `direct_mutation_epochs`,
    `copy_isolation`, `entity_generations`, `query_semantics`,
    `writable_query_lifecycle`, `command_buffer_atomicity`,
    `clone_independence`, and `structured_failures`.
  - The profile verifies deterministic entity IDs/generations, logical and
    structural epochs, detached component ownership, stable and changed
    queries, writable-cursor ownership, atomic retryable local command flush,
    clone/allocator independence, and structured failure atomicity.
  - Frozen reports use protocol `ludoweave.world-store-conformance/1` and
    profile `world-store-baseline/1`, with fixed status order and runner-owned
    `world_store_conformance.*` codes. Reports contain no provider message or
    code, path, environment/platform data, timing, component/entity values,
    storage layout, credential, or native object.
  - The built-in production `World` and independent `ReferenceWorld` pass from
    source, an isolated dependency-free wheel, and the deterministic release
    sample bundle.
  - Negative fixtures prove invalid factory/registry/shape, malformed values,
    mutation/epoch/query/command/clone mismatches, provider diagnostic
    sanitization, immutable report invariants, and no-discovery behavior.
  - ADR-0033 and public guides record trust, borrowed component-registry
    identity, the current no-close in-memory contract, limitations, evidence
    meaning, and independently authored storage-adapter adoption remaining
    zero.
  - The existing eight essential CI jobs remain unchanged and only one hosted
    implementation run may be created.
- **Non-scope:** A new storage backend, native/archetype/NumPy storage,
  persistence or database access, external-resource lifecycle, background
  threads, discovery/loading/installation, plugin fields or execution,
  command/snapshot/replay changes, another world authority, benchmark target
  changes, GUI/editor, 3D, WASM, networking, dependency/lock/version changes,
  release tag, GitHub release, or package publication.
- **SemVer:** Additive experimental `ludoweave.ecs` exports and a versioned
  report/profile. No stable API, root export, persistent format, runtime
  dependency, or package version change.
- **Baseline evidence:** On the exact clean base, `uv lock --check` resolved 46
  packages; storage/conformance/import/API tests passed 117 tests in 1.17
  seconds; and `uv run --frozen pytest -q` passed 925 tests with the existing
  Windows symlink-capability skip in 65.66 seconds.
- **Current local evidence:** The final hardened gate passes 955 tests with the
  existing skip, 149 focused tests, and all ten real-wgpu tests; 201 Python
  files are formatted with zero Ruff/Pyright findings; strict docs, the pure
  94-entry isolated wheel, and a complete ten-artifact release smoke pass. The
  protected workflows, lock, project metadata, version, and package root are
  unchanged. All documented benchmark/profile artifacts validate while the
  existing M1 simulation and both M3 target misses remain explicit. GitHub
  Actions run `31092244573` passed all eight unchanged essential jobs on
  DCO-signed implementation commit
  `1da692a693c1f92e10b676c2d4539354ce3ff59f`. PR #26 squash-integrated exact
  final evidence head `b93ca591f7063a1500cf105e6b0496b33573c69a` into `main` as
  GitHub-verified commit `1a7219e540d8f4cb3c1f60ff12981513c6860ef9`; both trees are
  `7fcd614fdde76daf1807f27dbe78ec306a501cc3`. No tag, release, package
  publication, certification, or independent third-party adoption is claimed.
