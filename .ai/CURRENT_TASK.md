# Current Task

- **Task:** M14 - Constrained 3D scope admission decision
- **Status:** Complete, independently accepted, hosted-validated, and
  squash-integrated with M8-M14 into `main` by PR #16. Stacked PR #15 is
  closed as superseded; its branch remains for audit history.
- **Started:** 2026-08-06
- **Base:** Exact final M13 hosted-evidence head
  `48f8f296113e3f2794bae7f4c67997d433e4dd36`; M14 will stack against
  `codex/m13-rollback-network-readiness`.
- **Outcome:** Decide authoritative post-alpha item 8 using reproducible
  installed-surface evidence. Retain the differentiated layered-2D scope and
  defer constrained 3D unless a later RFC satisfies a complete admission gate.
- **Acceptance gate:**
  - A dependency-free example audits the installed engine-owned render and
    command surfaces, emits deterministic versioned JSON, and reports no path,
    host, environment, provider, timing, or credential data.
  - Evidence distinguishes layered/z-sorted 2D from perspective, mesh,
    depth/stencil, 3D texture, material/light, agent-semantic, Null-conformance,
    product-slice, and cross-platform-budget contracts.
  - The same evidence runs from source, an isolated universal wheel, and the
    deterministic release sample bundle.
  - ADR-0028 records why WebGPU provider capability does not imply an
    engine-owned 3D feature and defines the complete revisit gate.
  - Architecture tests keep 3D provider dependencies and public 3D contracts
    out until a superseding decision intentionally changes the boundary.
  - Full local quality/artifact/provider and independent review gates pass
    before signed commit, PR, or hosted-success claims.
  - The existing eight-job essential CI topology remains unchanged.
- **Architecture:** M14 adds repository evidence, tests, and documentation
  only. It introspects existing public contracts from a composition-root
  example; `src/`, persistent formats, engine protocols, and public exports do
  not change. Provider capability remains isolated behind engine contracts.
- **Non-scope:** Perspective/3D cameras, Vec3/quaternion/3D transform types,
  meshes, models, materials, lights, depth/stencil attachments, 3D textures,
  general asset import, terrain, skeletal animation, PBR, 3D physics, picking,
  scene graphs, editor/GUI, networking, WASM, provider dependencies, native
  code, tags, releases, or package publication.
- **SemVer:** Repository decision evidence and documentation only; no public
  Python API, persistent schema, dependency, runtime version, or compatibility
  surface changes.
- **Current evidence:** The design spec explicitly limits layered 2D to
  orthographic sprites/tiles/layers and asks for a later decision rather than
  automatic expansion. Current public descriptors expose only color textures,
  a color-only pipeline, `Camera2D`, 2D device limits, and sprite/tile/debug
  records. The built-in sprite shader fixes vertex depth at zero. WebGPU itself
  supports 3D clip coordinates and optional depth/stencil state, but those
  provider capabilities are not LudoWeave contracts.
- **Final local gate:** 809 tests pass with one existing Windows
  symlink-capability skip; 178 Python files are formatted; Ruff, Pyright,
  strict docs, pure wheel/sdist build, exact installed-wheel evidence, fresh
  ten-artifact release smoke, nine real-wgpu tests, all inherited documented
  benchmark/profile validators, protected-scope/history checks, and independent
  hostile review pass. GitHub Actions run `31033924254` passed all eight
  unchanged essential jobs on signed implementation commit
  `47443046834eb423be977973775f80494161533d`.
