# Current Task

- **Task:** M16 - WASM-mod security admission decision
- **Status:** Complete, independently accepted, and hosted-validated through
  ready PR #20 on `codex/m16-wasm-mod-security-decision`; integration uses the
  user-authorized squash-PR flow.
- **Started:** 2026-08-06
- **Base:** Exact clean, verified `main` integration commit
  `c013dad38b1b64f0f4ccddc19681d643f6414427` from squash PR #19. Its tree
  exactly matches the final M15 evidence head.
- **Outcome:** Treat executable WebAssembly mods as a separate security
  workstream, retain the M12 data-only plugin boundary, and defer runtime or
  guest execution until a complete least-privilege, resource, determinism,
  lifecycle, persistence, isolation, conformance, supply-chain, and ownership
  gate is satisfied.
- **Acceptance gate:**
  - A dependency-free example audits exact installed root/plugin exports,
    preview stability, manifest fields/capabilities, and distribution
    requirements; positively proves representative executable manifest fields
    fail closed; emits deterministic versioned JSON; and records no credential,
    environment, secret, or token data.
  - The exact evidence runs from source, an isolated universal wheel, and the
    deterministic release sample bundle.
  - A prospective threat model identifies assets, actors, entry points, trust
    boundaries, privileged operations, blocking severity, remediation,
    verification, defense in depth, and residual risk.
  - ADR-0030 records the evidence-to-decision chain, tradeoffs, non-goals, and
    complete testable admission gate.
  - Architecture tests keep common WASM runtime imports, runtime modules,
    public execution exports, and dependencies absent and prove the import
    guard with synthetic invalid fixtures.
  - Full local quality/artifact/provider and independent security review gates
    pass before signed commit, PR, hosted-success, or integration claims.
  - The existing eight-job essential CI topology remains unchanged.
- **Architecture:** M16 adds repository evidence, tests, and documentation
  only. The example is a composition root over installed inert metadata. It
  compiles or executes no guest and adds no runtime source, public API,
  persistent format, dependency, lock, version, or CI change.
- **Non-scope:** WASM runtime selection or dependency, compilation/JIT/AOT,
  instantiation, WASI, host functions, guest ABI/memory/state, mod package or
  loader, discovery/import/hook execution, executable Python plugins, network,
  GUI/editor, 3D, Box2D, SDL3, Rust/native code, release tag, GitHub release,
  or package publication.
- **SemVer:** Repository decision evidence and documentation only; no public
  Python API, persistent schema, dependency, runtime version, or compatibility
  surface changes.
- **Current evidence:** No executable mod path or WASM runtime dependency is
  present. M12 manifests are exact-schema inert metadata and reject unknown
  executable fields. WebAssembly core host authority belongs to the embedder,
  so memory isolation alone cannot establish LudoWeave's command/receipt,
  determinism, resource, lifecycle, persistence, or supply-chain contract.
- **Final local gate:** 870 tests pass with one existing Windows
  symlink-capability skip; 186 Python files are formatted; Ruff, Pyright,
  strict docs, universal wheel/sdist build, exact installed-wheel evidence,
  fresh ten-artifact release smoke, nine real-wgpu tests, and every inherited
  documented benchmark/profile validator pass. Independent review first found
  four evidence/threat-model gaps; after exact full-requirement validation,
  WebAssembly module/dynamic-load fixtures, explicit residual risk, and
  corrected current-flow wording, repeat review approved with no finding.
- **Hosted gate:** GitHub Actions run `31039403209` passed all eight unchanged
  essential jobs on DCO-signed implementation commit
  `bcaf78fbc78bda8a13a95e397ab15d003dd4a6ce` through ready PR #20 against
  exact base `c013dad38b1b64f0f4ccddc19681d643f6414427`.
