# Current Task

- **Task:** M17 - installed render-device conformance
- **Status:** Complete. PR #22 squash-integrated the exact hosted-validated
  M17 tree into `main` as GitHub-verified commit
  `610261c8450afc3d7db6ebb2b0425a1829737aec`.
- **Started:** 2026-08-06
- **Base:** Exact clean `main` commit
  `27d2ee9d1f7f75dacc17568650f00ce833ef4fce`, synchronized with
  `origin/main` before branching.
- **Outcome:** Give external render-adapter authors one small, versioned,
  installed behavioral profile over the existing engine-owned `RenderDevice`
  boundary so comparable evidence can be produced without copying private
  repository fixtures.
- **Acceptance gate:**
  - The public experimental runner accepts a bounded adapter ID and an
    explicitly supplied trusted factory; it performs no discovery, dynamic
    import, install, filesystem scan, subprocess launch, network request, or
    global registration.
  - Fixed checks cover identity/capabilities, engine-owned resource handles,
    offscreen clear submission, fence completion, capability-consistent
    capture, copied events, resize, stale-handle rejection, idempotent close,
    and use-after-close rejection.
  - Frozen reports use protocol `ludoweave.render-device-conformance/1` and
    profile `render-device-baseline/1`, with stable ordered statuses/error
    codes and no exception text, path, environment, timing, capture, or native
    values.
  - Null passes from source, an isolated dependency-free wheel, and the
    deterministic release sample bundle. The existing real wgpu adapter passes
    in the graphics suite.
  - Negative fixtures prove invalid identity, unstructured failure,
    capability mismatch, prerequisite, cleanup, immutability, and no-discovery
    behavior.
  - ADR-0031 and public guides record trust, ownership, limitations, evidence
    meaning, and the fact that accepted third-party adoption remains zero.
  - The existing eight essential CI jobs remain unchanged.
- **Non-scope:** Adapter discovery/loading/installation, manifest execution or
  new fields, sandboxing, security certification, provider admission, a new
  backend, audio/physics conformance, network, editor, 3D, WASM execution,
  native code, dependency/lock/version changes, release tag, GitHub release,
  or package publication.
- **SemVer:** Additive experimental `ludoweave.render` exports and a versioned
  report/profile; no stable API, canonical/persistent world format, runtime
  dependency, or package version change.
- **Current evidence:** The final local gate reports 895 passes and one existing
  Windows symlink-capability skip, 191 formatted Python files, no Ruff/Pyright
  findings, strict docs, a 92-entry universal wheel with no native/WASM files,
  isolated wheel and ten-artifact release smoke, and 10 real-wgpu tests. Every
  documented benchmark/profile validator passed with the existing M1/M3 target
  misses recorded. GitHub Actions run `31042903689` passed all eight unchanged
  essential jobs on DCO-signed implementation commit
  `8e592f329424719214239bf97bd85dad9c9c5928`. PR #22 then squash-integrated
  final evidence head `148600cdaf9c419fbf552c68f833e0d55655731f`
  as verified one-parent `main` commit
  `610261c8450afc3d7db6ebb2b0425a1829737aec`; its tree exactly matches the
  retained milestone branch.
