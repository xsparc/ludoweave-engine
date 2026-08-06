# Current Task

- **Task:** M25 - external-consumer-feedback admission readiness
- **Status:** Implementation, local validation, publication, and the single
  necessary hosted run are complete on
  `codex/m25-external-consumer-feedback-readiness`. Delayed thread-aware review
  and squash integration remain.
- **Started:** 2026-08-07
- **Base:** Exact clean synchronized `main` commit
  `680e90dd8f9377fece23c43bd9f07ca9d76297de` after verified PR #37.
- **Outcome:** Make RFC-0003 gate-2 evidence mechanically auditable without
  treating project-owned fixtures, synthetic tests, or unreviewed submissions
  as external-consumer feedback.
- **Acceptance gate:**
  - Add one strict reviewed manifest whose current feedback-record set is empty
    and whose exact byte length and SHA-256 are pinned by architecture tests.
  - Require a manually reviewed independent consumer, public HTTPS repository,
    immutable Git revision, exact command/transaction/receipt protocol set,
    integration and feedback artifact hashes, and a bounded outcome before any
    record can count.
  - Preserve every previously mandatory reviewed record as an exact append-only
    prefix and reject duplicate consumers, malformed or project-owned records,
    unreviewed manifest bytes, unknown fields, unsafe locators, and excess
    records or bytes.
  - Emit exact sanitized `not-ready` evidence for the current empty manifest;
    never expose consumer identity, repository, revision, or artifact hashes in
    the report.
  - Prove future gate logic only with a synthetic `.invalid` consumer and state
    explicitly that the test is not external feedback or adoption evidence.
  - Exercise source, isolated wheel, and release-sample bundle paths, accept
    RFC-0008, and preserve the existing eight essential CI jobs.
- **Non-scope:** Soliciting or contacting consumers; network, telemetry,
  discovery, dynamic imports, subprocesses, provider execution, adoption or
  certification claims, stability promotion, runtime source/API/exports,
  protocol/operation/version changes, dependency/lock/workflow changes,
  release/tag/PyPI publication, or RFC-0003 gates 1/6.
- **SemVer:** No package or public-Python-surface change; version remains
  `0.1.0a1` and all command/transaction/receipt surfaces remain experimental.
- **Baseline evidence:** M24 feature PR #36 and zero-run state PR #37 are
  squash-integrated; local `main` was clean and synchronized at exact verified
  commit `680e90dd8f9377fece23c43bd9f07ca9d76297de`. `uv lock --check`
  resolves the unchanged 46-package lock, and 45 relevant M20/M24/release
  tests pass in 4.40 seconds. The new reviewed manifest is exactly 283 bytes
  with SHA-256
  `b113444f60946461ec6774e2c278b9e82e7d80e08a37450b6cc153e5c5c1500e`.
  Findings-first review corrected explicit-path symlink enforcement and
  hardened public HTTPS locators. The final local gate passes 227-file
  formatting, Ruff, strict Pyright, strict docs, 1,109 tests with two Windows
  symlink-capability skips, pure build, isolated wheel/release smoke, all
  documented benchmark/profile validators, 10 real-wgpu tests, and both
  graphics vertical slices.
- **Review and hosted evidence:** DCO-signed implementation commit
  `9667e020c2213d415072b7c7efbd880f6b58abfa` is published through ready PR
  #38 against exact assigned base
  `680e90dd8f9377fece23c43bd9f07ca9d76297de`. Sole GitHub Actions run
  `31111498136` passed all eight unchanged essential jobs. GitHub reports the
  PR `MERGEABLE` and `CLEAN`; the first thread-aware read found no issue
  comment, review, or inline review thread. Delayed automated review found one
  valid P2: numeric private/link-local IP authorities could pass the future
  locator syntax gate. The local correction requires an alphabetic DNS-style
  top-level label, adds loopback/link-local regressions, and passes 1,111 tests
  with the two existing Windows capability skips plus the complete static/docs
  and isolated wheel/release gate. DCO correction commit
  `90ed57e360765cf7f2d0973e41b8f8ec06dc4b50` passed necessary corrected run
  `31112342328` across all eight unchanged essential jobs. Final thread-aware
  reread found the original thread unresolved and non-outdated because its
  anchor persists, but the adjacent non-IP gate and exact regressions satisfy
  it; no finding remains actionable. No reply or manual resolution was
  performed. A final CI-skipping evidence commit and squash integration remain.
