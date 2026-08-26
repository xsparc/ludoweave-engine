# Current task

- **Task:** M131 - add bounded in-memory asset plan execution.
- **Status:** Implementation, review hardening, full supported-runtime,
  architecture, graphics, installed-wheel, documentation, governance,
  reproducibility, and local release-rehearsal validation are complete. Final
  record separator, scratch cleanup, local DCO commit, and postcommit proof
  remain.
- **Base:** Fully locally validated M130 DCO commit
  `1b69a30820d94c23272d7e1982ec80f978da8194`, tree
  `8270d4de2a49808d5a7bb7c348a4bc8152e721a2`, with sole parent exact M129.
  The stack remains unpublished under the existing public-review identity
  hold.
- **Branch:** `release/m131-bounded-asset-plan-execution`.

## Acceptance boundary

- Add frozen slotted exact `AssetBuildInput` values containing one logical URI
  and immutable source bytes in exact M129 plan order.
- Add tightening-only per-source, aggregate-source, per-artifact, and
  aggregate-artifact execution limits under fixed hard maxima.
- Preflight the complete input URI sequence, sizes, hashes, and source bounds
  before invoking any decoder.
- Execute only existing built-in PNG, JSON, WGSL, and audio transformations;
  settings remain cache-key inputs and do not become extension hooks.
- Add immutable `ludoweave.asset-build-result/1` output identities containing
  the plan hash, unchanged loader protocol, aggregate byte counts, and each
  plan-ordered URI/kind/cache-key/source-size/artifact-hash/artifact-size.
- Retain no decoded payload in the result and emit no success bytes until the
  entire execution and result construction succeed.
- Add `ludoweave source asset-build PROJECT --manifest FILE --assets FILE
  --lock FILE --plan FILE` after the exact M130 verification chain.
- Acquire exact detached source bytes through the existing project-confined
  bounded reader; executor revalidation must detect drift after lock hashing.
- Add unit, CLI, architecture, and isolated no-dependency wheel evidence.
- Document ownership, failure atomicity, determinism, limits, compatibility,
  and explicit cache/publication/plugin/worker non-scope.
- Keep workflows, allocations, permissions, credentials, dependencies, lock,
  metadata, version, engine root API, existing protocols/reports, release
  authority, and remote state unchanged.

## Direction and baseline evidence

- Primary sources accessed 2026-08-26: current Bazel remote-caching, Gradle 9.7
  build-cache/build-cache-concepts, and stable Godot import-process
  documentation. They separate declared actions, execution, cache reuse/write,
  and generated imported artifacts.
- Those sources support bounded built-in decoder execution with detached
  output identities. They do not justify cache lookup/write, persistent
  publication, worker scheduling, plugin loading, discovery, or reimport.
- Exact M130 commit/tree/parent, clean branch, and `0 31` divergence pass. The
  focused M4/M126-M130 asset/source/CLI baseline passes 88 tests in 6.73
  seconds. Static and dated governance pass; the lock check passed on an
  approved rerun after one pre-execution cache denial.
- The first deliberate-red format check requested two mechanical reflows, and
  the first architecture red exposed two guessed protected hashes. After exact
  hash correction and formatting, the protected surface passes, behavior
  stops only on absent exports, and four intended M131 boundaries fail.
- The first implementation checkpoint found one export-order lint issue, five
  test-only typing issues, and four immutable-detail assertion errors. After
  test-only corrections, formatting, Ruff, strict Pyright, and all 16 new
  execution/CLI assertions pass in 2.61 seconds.

## Explicit non-scope

- No cache lookup, cache read, cache write, persisted artifact, cache schema,
  atomic publication, collision/corruption handling, partial execution,
  resume, rollback, or artifact reader.
- No scheduler, worker, subprocess, thread, parallel execution, callback,
  plugin, decoder registration, dynamic import, arbitrary evaluation, or
  remote execution.
- No directory discovery, glob, watcher, live update, import/reimport,
  renderer upload, source/project write-back, world/session, command,
  transaction, world mutation, or receipt.
- No dependency, native/backend surface, metadata, version, workflow/job/
  allocation, permission, credential, release, publication, push, PR, or
  remote change.

## Remaining acceptance work

- Run complete source, supported-runtime, graphics, profile, vertical-slice,
  package, release, review, hygiene, history, hosted-state, cleanup, and final
  record separators.
- Create the authorized local DCO commit and prove it postcommit. Do not push or
  create a PR while the public-review identity hold remains.
