# Current Task

- **Task:** M12 - Preview plugin manifests and deterministic compatibility checks
- **Status:** Final local gate and independent review complete; publication pending
- **Started:** 2026-08-06
- **Base:** Exact final M11 evidence head
  `840a8b06d461fa1d5e649911b22f5995154728a7`; M12 will stack against
  `codex/m11-rich-2d-modules`.
- **Outcome:** Implement authoritative post-alpha item 6 as one data-only,
  headless plugin-manifest protocol plus deterministic compatibility evaluator
  that trusted composition roots and local tooling can use before injection.
- **Acceptance gate:**
  - `ludoweave.plugins` exports frozen, slotted preview values for an exact
    versioned manifest, dependency requirements, compatibility context,
    issues, reports, and evaluation.
  - Manifest JSON is canonical, strictly fielded, size/count bounded, and
    contains no Python module, callable, entry-point, path, URL, environment,
    credential, or provider object.
  - Compatibility checks cover engine release ranges, CPython minor ranges,
    desktop platform families, known engine-owned capability IDs, explicit
    native-code policy, minimum determinism tier, duplicate identities,
    dependency presence/ranges, and dependency cycles.
  - Results and issue order are repeatable across manifest input order and
    expose stable machine-readable codes plus a content fingerprint.
  - `ludoweave plugin check` reads only explicitly named bounded JSON files,
    emits one versioned JSON report without paths/environment values, returns
    0 for compatible, 1 for valid-but-incompatible, and 2 for invalid input.
  - A checked example manifest runs from source, isolated wheel, and the
    deterministic release sample bundle.
  - An accepted RFC records the persistent schema and preview compatibility
    promise; architecture tests reject discovery, imports, execution, package
    installation, networking, subprocesses, or global mutable registration.
  - Full local quality, package, release, example, provider, and independent
    review gates pass before signed commit, PR, or hosted-success claims.
  - The existing eight-job essential CI topology remains unchanged.
- **Architecture:** The plugin package is a pure data/contracts layer. It may
  depend on core version/errors and canonical JSON helpers but owns no world,
  runtime lifecycle, filesystem policy, provider, imported implementation, or
  mutable registry. CLI file access remains in `ludoweave.tools`.
- **Non-scope:** Entry-point discovery, module imports, hook execution, package
  installation/resolution, hot reload, sandboxing, plugin workers, arbitrary
  Python evaluation, project-authored module names, runtime global registries,
  provider admission, another world store, networking/rollback, GUI/editor,
  Box2D/SDL3 adapters, real audio, font shaping, 3D, WASM, Rust/PyO3, tags,
  releases, or package publication.
- **SemVer:** Additive preview Python surface and persistent
  `ludoweave.plugin-manifest/1` schema under RFC governance; runtime version
  remains `0.1.0a1` and no mandatory dependency is added.
- **Current evidence:** RFC-0002 is accepted and final independent review found
  no remaining finding. The complete local gate reports 741 passes and one
  existing Windows symlink-capability skip, 170 formatted files, zero
  Ruff/Pyright findings, strict docs, rebuilt pure artifacts, isolated wheel
  and fresh ten-artifact release smoke, nine real-wgpu integration passes,
  deterministic source examples, a compatible path-free manifest report, and
  valid inherited benchmark/profile artifacts. Hosted CI, PR status, and any
  cross-platform M12 pass remain unclaimed until publication and observation.
