# Current Task

- **Task:** M43 - published asset retrieval integrity
- **Status:** Feature implementation is squash-integrated through PR #80;
  publishing the documentation-only integration record on
  `records/m43-integration`.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79`. Only `main` existed locally
  and remotely, no pull request, local/remote tag, or GitHub release was
  present, and `git fsck --full --no-dangling` passed.
- **Outcome:** Require the exact published asset database identities already
  admitted by M42 to return the same complete byte set as local staging before
  the release job can succeed.
- **Acceptance gate:**
  - Advance the internal release validator from `/3` to `/4` and require one
    unique positive 63-bit ID for every bounded remote asset.
  - After complete published-state verification, create one exclusive
    `ludoweave.release-asset-retrieval-plan/1` file containing only canonical
    decimal ID, expected-size, and safe-basename tuples.
  - Reject draft plans, malformed/duplicate/out-of-range IDs, existing plan
    targets, unavailable parents, incomplete validation, and all asset drift.
  - Consume the plan inside the existing tag job with quoted bounded tokens,
    no clobber, bounded response streams, and exact `releases/assets/ID`
    authenticated API requests.
  - Reuse the same published document and validator to hash every downloaded
    byte against the already matched local staging identities.
  - Add no job, runner, action, permission, trigger, dependency, credential,
    cache key, tag, release, upload, rollback, cleanup, or publication authority.
  - Document the one-point authenticated retrieval claim and all public,
    global, future, immutability, consumer-installation, and attestation
    non-claims.
  - Run the complete local gate and one substantive hosted pull-request gate.
- **Non-scope:** Creating/pushing a tag, draft, or release; uploading or
  publishing; automatic unpublish/delete/rollback; enabling or requiring
  immutable releases; unauthenticated/browser downloads; global CDN/cache
  verification; future-byte monitoring; public installed-wheel matrix;
  attestation verification; rendered Markdown/link/factual review; signer/key
  policy; deployment environments or tag rules; PyPI; supported release
  channel; runtime/public API; package version/dependency/lock; deferred
  subsystems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** M42 zero-run closeout PR #79 exact head
  `8407499326f2c55118c7a28735224c9e4cd18723` changed only three `.project`
  paths and had no run, check, review, comment, or thread. Squash
  `2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79` has sole parent the M42
  integration squash, preserves reviewed tree
  `664d67c43daa42eb8bd02ab0c52d04bad294ff6b`, has a valid GitHub signature and
  standalone DCO trailer, and allocated no post-merge run. Official GitHub API
  documentation confirms exact numeric asset-ID binary retrieval with the
  existing contents access. Protocol `/4`, exclusive published-only plan
  output, exact-ID authenticated retrieval, same-document byte revalidation,
  and fail-closed state/ID/drift behavior are implemented. Findings-first
  review tightened the shell boundary to canonical positive 63-bit IDs and at
  most 32 requests and added an exact-ID success round trip. Hosted run
  `31273727767` passed the exact initial feature head in three allocations, but
  one P2 review correctly found that an oversized response was not bounded
  during transfer. The plan now carries verified expected sizes; each transfer
  is capped at expected size plus one byte, short/long responses fail, and the
  512-MiB expected-total cap is enforced before materialization. The corrected
  workflow SHA-256 is
  `a5c7ff3f80010cad2712592daf32327b80122b8473cee720fe066bbb3eb06e06`.
  Whole-tree format/lint/type/docs, 361 architecture tests, the final 1,870-test
  CPython 3.12 suite, CPython 3.13/3.14 compatibility, real graphics, profiles,
  deterministic samples, fresh reproducible distributions, installed-wheel
  smoke, complete release smoke, YAML, scope, credential, archive, identity,
  whitespace, and Git-object checks all pass locally for the initial head. The
  focused correction, shell-stream semantics, complete architecture, static,
  docs, YAML, final 1,870-test suite, reproducible distribution, installed-wheel,
  complete release smoke, protected-surface, credential, whitespace, and
  Git-object gates pass. Corrected head
  `3a5004217598c82eca5b8286442e7d8a502642b1` passed run `31274622529` in
  exactly three allocations: Linux 7m13s, macOS 1m48s, and Windows 3m53s.
  Linux and every compatibility platform passed 1,873 tests; compatibility
  suites had one expected skip, and all three platforms passed ten real-wgpu
  tests. The P2 thread was answered with correction evidence and resolved;
  no unresolved thread remains. PR #80 squash
  `8b7038cc203cead16d1dd88c746b584b6d0c37ca` has sole parent the exact M42
  closeout, preserves reviewed tree
  `6c5ed36a8454a3ab16fec82152df13038c41ce84`, has a valid GitHub signature and
  standalone DCO trailer, and allocated no post-merge `main` run. The feature
  branch is deleted locally and remotely. Only the documentation-only
  integration record and zero-run closeout record remain.
