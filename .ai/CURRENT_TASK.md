# Current Task

- **Task:** M24 - cross-version receipt-corpus admission readiness
- **Status:** Implementation is complete, locally validated, DCO-signed, and
  published through ready PR #36 on
  `codex/m24-cross-version-corpus-readiness`. Sole GitHub Actions run
  `31107800179` passed all eight unchanged essential jobs. Delayed automated
  review found one valid append-only-history gap. The correction freezes
  mandatory source/release prefixes and passes the complete local/artifact
  gate; DCO correction commit, one necessary hosted run, final thread reread,
  and squash integration remain.
- **Started:** 2026-08-06
- **Base:** Exact clean synchronized `main` commit
  `55c7a72337913303b6b1f6bd31edbca7ff28683b` after verified PR #35.
- **Outcome:** Make RFC-0003 gate-1 evidence mechanically auditable without
  relabeling the current single-version fixtures as cross-version history.
- **Acceptance gate:**
  - Add one strict repository manifest that references preserved M21 source
    manifests by safe name, exact byte length, and SHA-256.
  - Decode every declared receipt through the installed bounded public reader
    and require exact status/canonical-byte preservation.
  - Require a reader version different from a source version, at least two
    observed versions, and supported-release records for every observed
    version before the cross-version gate can become true.
  - Emit exact sanitized `not-ready` evidence for the current `0.1.0a1` corpus
    and empty supported-release set.
  - Prove future gate logic synthetically while explicitly refusing to count
    that regression as history or release evidence.
  - Exercise source, isolated wheel, and release-sample bundle paths, accept
    RFC-0007, and preserve the existing eight essential CI jobs.
- **Non-scope:** Changing historical receipt bytes, runtime source/API/exports,
  command/receipt/operation semantics, package version, stability labels,
  dependency/lock/workflow topology, external-adoption claims, actual release
  records, tag/release/PyPI publication, provider discovery, networking,
  subprocesses, storage/backend/native/WASM/editor work, or RFC-0003 gates 2/6.
- **SemVer:** No package or public-Python-surface change; version remains
  `0.1.0a1` and all command/transaction/receipt surfaces remain experimental.
- **Baseline evidence:** The exact M21 source manifest remains 762 bytes with
  SHA-256 `ed3f1040294376fafce523e129897ce756d785b2f6d90c54335ad5f8abb84ac3`.
  The lock resolves 46 packages, and 71 relevant reader/corpus/policy/
  architecture tests pass in 4.05 seconds. The final reviewed gate passes 223-
  file formatting, Ruff, strict Pyright, strict docs, 1,074 tests with one
  existing Windows symlink skip, pure build, isolated wheel/release smoke, 10
  real-wgpu tests, both graphics vertical slices, and base/graphics profile
  contract smokes. Findings-first review added bounded streaming and path
  confinement, pinned reviewed-corpus identity, exact release coverage, and
  source/release/fixture/receipt resource caps; 26 focused post-hardening tests
  pass and no finding remains.
