# Current Task

- **Task:** M21 - bounded public receipt reader and v1 compatibility-fixture
  baseline
- **Status:** Complete. Implementation, local review, publication, the sole
  hosted run, and exact squash integration are complete. PR #30 produced
  GitHub-verified `main` commit
  `6bfb56555cafc93a7312f64465ea15cd7c450e79`; the milestone branch remains
  for audit history.
- **Started:** 2026-08-06
- **Base:** Exact clean synchronized `main` commit
  `feed793e94c345fac4b146c358a68264ef6e5f62` on
  `codex/m21-receipt-reader-baseline`.
- **Outcome:** Add a strict resource-bounded reader for the existing exact
  `ludoweave.receipt/1` document and preserve immutable same-version fixture
  inputs for later cross-version compatibility work.
- **Acceptance gate:**
  - `TransactionReceipt.from_mapping()` and `.from_json()` detach caller data,
    enforce exact fields/types/protocol/invariants, and return the existing
    immutable receipt graph.
  - Frozen/slotted `ReceiptLimits` bounds UTF-8 bytes, JSON depth/nodes,
    collections, strings, outcomes, diagnostics/details, aliases, and semantic
    diff records before unbounded domain construction.
  - Structured receipt decode and incompatibility errors retain stable codes,
    contextual details, and causes without leaking input documents.
  - Exact committed, dry-run, and rejected `0.1.0a1` fixtures have a manifest
    containing their byte sizes and SHA-256 digests and explicitly declare
    `single-version-baseline` evidence.
  - A deterministic installed example and strict validator run from source,
    an isolated dependency-free wheel, and the release sample bundle.
  - M20 living readiness evidence advances to schema `/2`, marks only the
    public-reader gate true, and retains the overall experimental decision.
  - RFC-0004, public docs, and architecture tests document and enforce the
    bounded trust boundary, dependency direction, ownership, failure,
    determinism, and compatibility non-claims.
  - The existing eight essential CI jobs remain unchanged and at most one
    hosted implementation run is created.
- **Non-scope:** Receipt protocol/field reinterpretation, cross-version or
  external-adoption claims, stability promotion, a new command/operation,
  migration framework, provider discovery/import/installation, filesystem or
  network reader, package-root export, dependency, lock, package version,
  workflow/job, backend, database, native/WASM code, tag, release, or package
  publication.
- **SemVer:** Experimental additive `ludoweave.world` surface only. The exact
  wire protocol remains `ludoweave.receipt/1`; package version remains
  `0.1.0a1`.
- **Baseline evidence:** `uv lock --check` resolved 46 packages in 0.71 ms;
  138 focused receipt/canonical/API/artifact tests passed in 1.70 seconds; the
  inherited full suite passed 972 tests with one existing Windows symlink-
  capability skip in 69.25 seconds.
- **Current local evidence:** Corrected reader tests pass 26 tests in 0.41
  seconds. Fixture/reader tests pass 24 tests in 0.39 seconds. Installed and
  release integration tests pass 34 tests in 2.22 seconds. The combined M20/
  M21 group passed 58 tests in 3.46 seconds before one static-test helper
  correction; the corrected combined gate passes Ruff, Pyright, and 60 tests
  in 4.10 seconds. Review hardening then raised the focused result to 62 tests
  in 4.13 seconds. The final gate passes 1,015 tests with one existing Windows
  symlink-capability skip, 211-file formatting, Ruff, Pyright, strict MkDocs,
  pure-wheel and fresh release smoke, 255 expanded tests, ten real-wgpu tests,
  and every inherited benchmark/profile validator. M1 simulation and both M3
  targets remain observed misses. Exact results and corrected first attempts
  are recorded in `.ai/TEST_EVIDENCE.md`. DCO-signed implementation commit
  `cec339be07318a7c1586bb3405e8f9b1904859f5` is published through ready PR
  #30. GitHub Actions run `31098563810` passed all eight essential jobs and is
  the branch's only run. PR #30 squash-integrated final evidence head
  `4e378756b2a1733de28e7160ac2d6d72921f3e4a` as verified `main` commit
  `6bfb56555cafc93a7312f64465ea15cd7c450e79`; both trees are
  `ea3f410fac31d7a32faee4e697c4fb0941b657df`. No tag, release, publication,
  stability promotion, external adoption, certification, or cross-version
  compatibility is claimed.
  Early failures and their corrections remain recorded in
  `.ai/TEST_EVIDENCE.md`.
