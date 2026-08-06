# Current Task

- **Task:** M26 - supported deprecation release-channel admission readiness
- **Status:** In progress on
  `codex/m26-supported-release-channel-readiness`.
- **Started:** 2026-08-07
- **Base:** Exact clean synchronized `main` commit
  `0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62` after verified PR #39.
- **Outcome:** Make RFC-0003 gate-6 evidence mechanically auditable without
  treating the prerelease workflow, local candidates, CI, tags, or synthetic
  records as a supported deprecation-capable feature-release channel.
- **Acceptance gate:**
  - Add one strict reviewed manifest whose current release-record set is empty
    and whose exact byte length and SHA-256 are pinned by architecture tests.
  - Require at least two reviewed, supported, non-yanked final
    `MAJOR.MINOR.PATCH` releases on distinct feature lines before the gate can
    become true.
  - Require exact version/tag/commit, public non-IP HTTPS release URL,
    artifact/notes SHA-256, and publication-channel identities for every
    record; preserve accepted history as an exact append-only prefix.
  - Preserve the one-supported-feature-release deprecation window and reject
    prereleases, patch-only cadence, duplicates, out-of-order records,
    unsupported/yanked releases, unreviewed bytes, and excess records/bytes.
  - Emit exact sanitized `not-ready` evidence for the current empty manifest;
    never expose release URLs, commits, or artifact/notes hashes in the report.
  - Prove future gate mechanics synthetically while explicitly refusing to
    count that regression as a release, support promise, or publication.
  - Exercise source, isolated wheel, and release-sample bundle paths, accept
    RFC-0009, and preserve the existing workflows and eight essential CI jobs.
- **Non-scope:** Creating/pushing a tag; publishing a GitHub release or PyPI
  package; configuring trusted publishing; changing the release workflow,
  package version, runtime source/API/exports, protocol/operation, dependency,
  lock, stability metadata, or support policy; network/telemetry/discovery/
  subprocess/provider execution; or claiming RFC-0003 gates 1/2 complete.
- **SemVer:** No package or public-Python-surface change; version remains
  `0.1.0a1` and all command/transaction/receipt surfaces remain experimental.
- **Baseline evidence:** M25 feature PR #38 and zero-run state PR #39 are
  squash-integrated; local `main` is clean and synchronized at exact verified
  commit `0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62`. The unchanged lock resolves
  46 packages, and 61 relevant release/stability tests pass with one Windows
  symlink-capability skip in 5.90 seconds. The new reviewed manifest is exactly
  278 bytes with SHA-256
  `f23b4314696384ad288b86c63bc101606f1aa9f323c4fb186486d8c74915ec41`.
  Findings-first review hardened exact project-tag URLs, final-release state,
  and publication identity. The complete local gate passes 231-file formatting,
  Ruff, strict Pyright, strict docs, 1,152 tests with three Windows symlink-
  capability skips, pure build, isolated wheel/release smoke, all documented
  benchmark/profile validators, 10 real-wgpu tests, and both graphics vertical
  slices. The post-documentation full gate passes on the exact final local tree;
  ready PR #40 targets the exact assigned base from DCO-signed implementation
  commit `835ac2b2f3dd8bfe5a31fe9f880a43555e86fd34`. Sole hosted run
  `31115252696` passes all eight unchanged essential jobs. GitHub reports the PR
  `MERGEABLE` and `CLEAN`; the first thread-aware read found no comment, review,
  or inline thread. Delayed review and squash integration remain pending.
