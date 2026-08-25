# Current task

- **Task:** M130 - add confined asset build-plan verification.
- **Status:** Primary-source direction, exact M129 base, corrected focused
  baseline, both governance baselines, deliberate-red contract, implementation,
  installed verifier, RFC, public documentation, corrected focused proof, and
  documentation-inclusive validation, complete source/runtime/graphics gates,
  profiles, deterministic vertical slices, initial package/release gates,
  final review, hygiene, record-inclusive package/release gates are complete.
  History/hosted-state, bounded cleanup, and final clean-scratch metadata gates
  are complete. The local DCO commit and postcommit proof remain.
- **Base:** Fully locally validated M129 DCO commit
  `ae1b2bf01a001ea157e170626544a2d487055d09`, tree
  `ea7b58efafa29cb5af4ee40617636dce34176e5c`, with sole parent exact M128.
  The stack remains unpublished under the existing public-review identity
  hold.
- **Branch:** `release/m130-asset-build-plan-verification`.

## Acceptance boundary

- Add exact, content-silent verification between one saved M129 plan and a
  freshly recomputed current plan.
- Compare plan protocol/loader invariants through construction, then source-
  lock identity, asset-manifest identity, roots, exact entry URI sequence, and
  each entry field in stable order.
- Add `HeadlessProject.load_asset_build_plan()` through the established
  project-confined regular-file reader and the plan's 8 MiB decode bound.
- Add read-only `ludoweave source asset-plan-verify PROJECT --manifest FILE
  --assets FILE --lock FILE --plan FILE`.
- Load and structurally validate the saved plan, recompute and verify current
  M128 inputs, regenerate the M129 plan, and compare before emitting success.
- Success reports only versioned protocol/status and aggregate root/entry
  counts; mismatch errors expose only the first stable field and optional
  logical URI, never compared hashes, sizes, keys, paths, or settings.
- Prove confinement, descriptor closure, stale-plan rejection, no success
  output on failure, read-only project behavior, and installed-wheel use.
- Keep workflows, allocations, permissions, credentials, dependencies, lock,
  metadata, version, engine root API, existing protocols/reports, release
  authority, and remote state unchanged.

## Direction and baseline evidence

- Primary sources accessed 2026-08-26: current Bazel remote-caching, Gradle
  build/configuration-cache, stable Godot import-process, and Python 3.14 path
  documentation. Bazel declares action inputs before cache lookup/execution;
  Gradle revalidates recorded fingerprints and separates configuration from
  output caches; Godot separates committed import configuration from generated
  imports; Python distinguishes pure path manipulation from filesystem I/O.
- These sources support exact saved-plan/current-input verification as a
  prerequisite boundary. They do not justify decoder execution, build, cache
  lookup/write, artifact creation, automatic import/reimport, scheduler,
  discovery, watcher, or remote cache behavior.
- Exact M129 commit/tree/sole-parent, clean branch, and `0 30` divergence pass.
  M129 postcommit proof records exact identity, one DCO sign-off, 23 paths,
  clean worktree, zero scratch, and zero critical Git finding.
- The first focused baseline named a nonexistent generic asset-manifest test
  and stopped before collection. The corrected exact filename passes 168 tests
  with one established Windows capability skip in 5.00 seconds.
- Static governance passes. Dated governance was cache-denied before execution;
  its approved offline rerun returns zero findings.
- Deliberate red produced four expected behavior failures and four expected
  boundary failures with the protected-surface assertion passing.
- After one test-only Pyright annotation, all statics and 14 focused behavior
  assertions pass in 3.32 seconds. Three M130 boundaries pass; only the then-
  absent installed verifier and documentation assertions fail.
- After one mechanical verifier reflow and one retained governance cache
  denial, all statics, 177 focused assertions with one established skip,
  strict docs, approved dated governance, and whitespace pass. Strengthened
  limit/load-order cases bring the focused result to 178 passes with one skip.
- The isolated no-dependency wheel generates and verifies one saved plan under
  the exact protocols and creates no cache.
- The complete source separator passes all 414 formatted files, Ruff, strict
  Pyright, 1,662 architecture assertions with one established skip, strict
  docs, both governance modes, and whitespace after one retained cache denial.
- Supported suites pass on direct tracked runs: 3.12.13 graphics has 3,387
  passes/16 skips; 3.13.13 and 3.14.5 base each have 3,377 passes/17 skips.
  One earlier 3.12 session-loss attempt is retained as incomplete.
- Real-wgpu, fresh base/graphics profiles, Clockwork Arena, and Agent World
  Builder all pass and reproduce their established deterministic identities.
- Two reproducible builds, all 13 isolated consumers, two byte-identical
  release stages, both release smokes, and archive hygiene pass.
- Findings-first review has no remaining actionable issue. Exactly 21 intended
  paths and all protected/identity/credential/runtime-scope checks pass.

## Explicit non-scope

- No asset payload read beyond M128 verification, decoder execution, build,
  import, cache lookup, cache write, artifact creation, activation, reimport,
  watcher, or live update.
- No plan execution, scheduler, worker, thread, process, partial execution,
  resume, rollback, atomic filesystem snapshot, provenance, authenticity, or
  signature.
- No directory discovery, glob, default plan/manifest, component-reference
  inference, unused-asset rejection, or build-inclusion policy beyond the exact
  explicit M127 closure.
- No source/project write, world/session, command, transaction, world mutation,
  receipt, dependency, native/backend surface, metadata, version, workflow,
  allocation, permission, credential, release, publication, push, PR, or remote
  change.

## Remaining acceptance work

- Create the local DCO commit and prove it postcommit.
