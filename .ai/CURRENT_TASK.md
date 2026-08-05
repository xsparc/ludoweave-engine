# Current Task

- **Task:** M13 - Rollback and network-snapshot readiness evaluation
- **Status:** Complete, independently accepted, DCO-signed, published as ready
  stacked PR #14, and validated by all eight essential hosted CI jobs
- **Started:** 2026-08-06
- **Base:** Exact final M12 hosted-evidence head
  `7cb834c7b5e84e1b1a945905a68b947b3a4bdd3f`; M13 will stack against
  `codex/m12-plugin-manifest-compatibility`.
- **Outcome:** Evaluate authoritative post-alpha item 7 with one bounded,
  dependency-free offline correction-branch proof and an evidence-based
  admission decision. Do not implement a transport or live rollback service.
- **Acceptance gate:**
  - A Clockwork Arena parent timeline repeats through exact checkpoints and
    canonical state hashes.
  - A child timeline branches at an exact completed-tick boundary, references
    the immutable parent hash/state, consumes a corrected future input stream,
    and repeatably reaches a different final state.
  - The proof demonstrates that current replay still requires equivalent input
    snapshots to be injected externally.
  - Evidence is versioned, sanitized, strictly fielded, work-bounded, and
    validated against inconsistent or false transport/admission claims.
  - The proof runs from source, an isolated pure wheel, and the deterministic
    release sample bundle without a new runtime dependency.
  - ADR-0027 records the deferral and measurable canonical-input, protocol,
    security, cross-platform simulation, resource, lifecycle, and ownership
    revisit gates.
  - Full local quality/artifact/provider and independent review gates pass
    before signed commit, PR, or hosted-success claims.
  - The existing eight-job essential CI topology remains unchanged.
- **Architecture:** M13 composes existing public snapshot/replay and sample
  contracts from an example. It adds no engine runtime package and leaves the
  persistent snapshot, replay, command, and input formats unchanged. The
  single `WorldSession` remains canonical.
- **Non-scope:** Sockets/listeners, network or remote-agent transports, peer
  identities, replication or prediction stores, live rollback APIs,
  authentication/encryption implementation, background mutation, protocol
  format changes, another world store, GUI/editor, 3D, Box2D/SDL3 adapters,
  real audio, WASM, Rust/PyO3, tags, releases, or package publication.
- **SemVer:** Repository evidence and documentation only; no public Python API,
  persistent runtime schema, mandatory dependency, or version change.
- **Current evidence:** The final reviewed local gate reports 793 passes and
  one existing Windows symlink-capability skip, 174 formatted files, zero
  Ruff/Pyright findings, strict docs, rebuilt pure artifacts, isolated wheel
  and fresh ten-artifact release smoke, and nine real-wgpu passes. The 120/60
  proof and strict validator pass with exact parent/child checkpoint evidence;
  independent review also passed the maximum 600/300 proof and reports no
  remaining finding. Ready stacked PR #14 targets exact M12; GitHub Actions run
  `31031590206` passed the unchanged eight-job topology on signed implementation
  commit `ba62b650191cfb982100692e7ec694da318956ae`.
