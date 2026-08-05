# Current Task

- **Task:** M7 — Post-alpha performance and first-native-kernel decision
- **Status:** Complete; DCO-signed PR #7 is published and hosted run `31005165849` passed all 14 jobs
- **Started:** 2026-08-05
- **Acceptance gate:** Profile the exact recorded M1/M3 misses, exhaust ordinary
  Python/algorithm work justified by the evidence, assess every native-code
  admission field in a public RFC, preserve deterministic and backend-isolated
  semantics, and validate the decision across the normal platform matrix.
- **Profiling outcome:** Schema `ludoweave.profile.m7/1` records exact
  10,000-entity simulation, 10,000-sprite extraction/packing, and optional
  10,000-sprite wgpu submission profiles with sanitized module identities,
  exact invariants, and a strict tamper-tested validator.
- **Implementation outcome:** Query metadata/signature work is reduced without
  weakening detached ownership or production/reference parity. Extraction
  reuses validated immutable source fields while checking interpolated
  finiteness. Sprite packing uses fixed 64-byte standard-library records and
  retains exact provider-neutral bytes and structured overflow errors.
- **Decision outcome:** Accepted RFC-0001 and ADR-0022 defer Rust/PyO3. Current
  ECS/extraction inputs are Python object graphs rather than a GIL-releasable
  contiguous buffer; no native build matrix or maintenance owner exists. The
  RFC gives quantified evidence and an exact revisit gate.
- **Local performance evidence:** Official 30-sample local p95 is 144.0474 ms
  for the representative simulation tick, 30.6902 ms for extraction/packing,
  and 5.1918 ms for wgpu CPU submission. All remain honest target misses. The
  same-machine reductions from prior recorded evidence are 26.83%, 26.88%, and
  20.57%, respectively.
- **Local quality gate:** Windows, uv-managed CPython 3.12.13 reports 564 passed
  and one existing symlink-capability skip, 148 formatted Python files, zero
  Ruff/Pyright findings, strict docs success, pure wheel/sdist, installed-wheel
  smoke, complete release-candidate smoke, six real wgpu integration passes,
  and successful Clockwork Arena/Agent World Builder runs.
- **Hosted gate:** PR #7 is mergeable with clean merge state against
  `codex/m6-release-hardening`. Run `31005165849` passed strict quality/docs,
  all seven CPython/OS test jobs, all three installed release-candidate smokes,
  and all three real graphics/profile smokes.
- **Non-scope retained:** No Rust, PyO3, Maturin, NumPy storage, native artifact,
  public storage-layout exposure, release publication, networking, editor, 3D,
  rigid-body physics, production audio, or remote agent transport.
- **SemVer:** No public API or persistent-protocol addition; version remains
  `0.1.0a1` and all current supported exports remain experimental.
