# Current task

- **Task:** M125 - add bounded source-integrity lock verification.
- **Status:** Fresh direction research, exact-base/governance proof, deliberate
  red, immutable lock implementation, project-confined loading, read-only lock
  generation and verification, retained M124 behavior, focused static/behavior
  proof, initial isolated-wheel proof, RFC-0108, and public documentation are
  complete. The documentation-inclusive focused gate also passes. Complete
  source/architecture/governance validation passes. Supported-runtime,
  validation across exact CPython 3.12-3.14 passes. Graphics/vertical, artifact,
  profile and deterministic vertical validation also passes. Artifact, final
  deterministic distribution/release and findings-first review are complete.
  Final record-inclusive artifacts, cleanup, history, and local DCO-commit
  evidence remain.
- **Base:** Fully locally validated M124 DCO commit
  `c73242b29325977484df271a107287d688fbdb54`, tree
  `f703877a9516af679c338dfcd002619bb18b668e`, with sole parent exact M123.
  The stack remains unpublished under the existing public-review identity hold.
- **Branch:** `release/m125-source-lock-verification`.

## Acceptance boundary

- Add exact bounded `ludoweave.source-lock/1` values in the focused
  `ludoweave.scene` package; keep the engine root unchanged.
- Bind one normalized M124 manifest ID/hash plus 1-256 entry-ID-ordered source
  protocol, stable ID, and lowercase SHA-256 identities.
- Require prefab entries to bind the explicit instance protocol/ID/hash and
  forbid those fields for scenes.
- Use immutable slotted values, exact fields, unique IDs, canonical bytes,
  limits that may tighten only, and content-silent structured failures.
- Add internal confined bounded `HeadlessProject.load_source_lock()` ownership.
- Add read-only `ludoweave source lock PROJECT --manifest FILE` that emits the
  lock only to stdout.
- Add `ludoweave source verify PROJECT --manifest FILE --lock LOCK` that
  compares exact current identities and emits
  `ludoweave.cli.source-lock-verify/1` only after success.
- Retain M123/M124 check output exactly; on mismatch emit no success document,
  disclose no path/hash values, leave the project unchanged, and return exit 2.
- Add unit, integration, architecture, installed-wheel, RFC, and public-doc
  evidence.
- Keep workflows/allocations, permissions, credentials, dependencies, lock,
  metadata, version, engine root, existing scene/prefab/manifest contracts,
  planners, release authority, tags, releases, publication, and remote state
  unchanged.

## Evidence so far

- Primary sources accessed 2026-08-26 support stable path-independent resource
  identities, checksum-based change detection, versioned deterministic lock
  documents, and pre-use hash verification. They do not justify importing,
  discovery, a cache, automatic reimport, live update, signatures, or trust.
- Exact M124 commit/tree/sole-parent and `0 25` divergence pass from a clean
  worktree. Static and dated strict governance each return zero findings.
- Deliberate red produced five intended absent contract/loader/CLI/verifier/docs
  failures and one protected-surface pass in 0.21 seconds.
- The first implementation checkpoint stopped at one sorted-export lint issue.
  The corrected run reached strict typing and found one redundant literal cast
  plus two test-only decoded-list typing gaps. After correction, statics passed;
  23 behavior cases passed and one expectation incorrectly hashed raw rather
  than normalized manifest bytes. The corrected canonical expectation yields
  all 24 M125 plus retained M124 behavior cases passing in 2.68 seconds.
- Twelve M124/M125 implementation and protection assertions pass; only the
  intentionally absent documentation assertion failed before docs.
- The first pure package build succeeds. The isolated no-dependency wheel
  verifier checks the four focused experimental exports, emits a two-entry
  source lock, and verifies it with the expected protocols and identities.
- RFC-0108 and public docs define the exact schema, limits, ownership, mismatch
  behavior, compatibility, deterministic ordering, sequential-read limitation,
  integrity-only hash semantics, and explicit non-scope.
- The documentation-inclusive focused gate passes formatting, Ruff, strict
  Pyright, all 37 behavior/boundary assertions, strict docs, dated strict
  governance, and whitespace.
- Findings-first review added missing deterministic precedence coverage for
  manifest/entry-set mismatches plus end-to-end manifest drift. No runtime
  change was needed; all 42 corrected focused assertions pass with statics and
  whitespace.
- The complete source separator passes the unchanged lock, all 393 Python
  files, Ruff, strict Pyright, 1,637 architecture assertions with one
  established skip, strict docs, both governance modes, and whitespace.
- Exact CPython 3.12.13 with graphics passes 3,307 tests with 16 skips; exact
  3.13.13 and 3.14.5 base environments each pass 3,297 with 17 skips. The first
  3.13 harness accidentally reselected the repository's 3.12 default and was
  interrupted; the corrected commands explicitly selected 3.13 on every uv
  invocation before any 3.13 pass was claimed.
- The restored exact 45-package 3.12.13 graphics environment passes all ten
  real-wgpu tests. Fresh base/graphics profiles validate with two/three
  workloads, and both vertical samples reproduce their established deterministic
  identities and passing acceptance fields.
- Two independent distributions are byte-identical, all eight isolated wheel
  paths pass, two ten-artifact release stages are byte-identical with complete
  release smoke, and package/repository hygiene reports zero forbidden,
  public development-tool identity, or high-confidence credential match.
- Findings-first review covers exactly 23 intended paths, confirms exact
  mismatch ordering, content-silent failures, confined read ownership, and
  unchanged protected surfaces, and finds no remaining actionable defect.
- The review-record source separator passes lock, all 393-file formatting,
  Ruff, strict Pyright, 1,637 architecture assertions with one established
  skip, strict docs, corrected static and dated strict governance, and
  whitespace. One mispointed governance invocation is retained as a factual
  harness correction rather than a project failure.
- Final review-record-inclusive distributions reproduce byte-for-byte; all
  eight isolated-wheel paths pass; both byte-identical ten-artifact release
  candidates pass; and final package/repository hygiene is clean.
- Corrected precommit history and hosted-state audit passes: exact M99 main,
  exact M124 head/tree/parent, `0 25` divergence, 25 linear exact-identity
  singly signed-off stack commits, only remote main, zero critical Git finding,
  and no M125 remote branch, PR, run, tag, or release.
- The final factual source/architecture/docs/governance separator passes, and
  all 13 exact generated M125/docs/pytest targets are now absent after bounded
  cleanup.
- The final metadata/scope separator passes selected formatting, Ruff, strict
  Pyright, all 11 M59/M125 assertions, dated strict governance, protected
  surfaces, whitespace, exact 23-path scope, zero scratch, and disclosure scans.

## Explicit non-scope

- No directory discovery, recursion, glob, suffix routing, implicit pairing,
  asset database, import graph, or project-manifest source registry.
- No import, compile, application component registration/resolution, asset or
  dependency load, world/session, command, transaction, mutation, or receipt.
- No atomic filesystem snapshot, cache, watcher, automatic reimport, live
  update, source write-back, arbitrary script/import/evaluation, file URI, or
  remote access.
- No signature, provenance, authenticity, authorization, freshness, artifact-
  security, or hostile-filesystem claim.
- No dependency, lock, metadata, version, engine-root API, workflow job or
  allocation, hosted runner, release authority, tag, release, publication,
  push, PR, or remote change.

## Remaining acceptance work

- Run the post-record metadata/scope separator, stage exactly 23 paths, create
  the local DCO commit, and verify its exact tree, parent, identity, scope, and
  clean worktree.
- Create the standalone local DCO commit and verify exact tree, parent, identity,
  scope, and clean worktree. Publication remains held.
