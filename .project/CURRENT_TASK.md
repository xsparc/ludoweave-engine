# Current task

- **Task:** M135 - add explicit post-realization asset-cache population.
- **Status:** Implementation, documentation, findings-first review, complete
  validation, record-inclusive reproducibility, release rehearsal, and scope
  review are complete. Cleanup and history/hosted audit are complete. Final
  metadata separation is complete. M135 is ready for the authorized local DCO
  commit.
- **Base:** Fully locally validated M134 DCO commit
  `a6263a2e7d0df18ff1a34d32f02f88be29ee006c`, tree
  `de0284fc44a825ead61440ad231b2fb6de559950`, with sole parent exact M133.
  The stack remains unpublished under the existing public-review identity
  hold.
- **Branch:** `release/m135-post-realization-cache-population`.

## Acceptance boundary

- Accept one exact current build plan, detached input tuple, explicit local
  cache path, optional project root, and existing tightening-only limits.
- Open the cache without write authority, complete all M134 source/cache/
  decoder/limit work, and only then acquire write authority for the same
  resolved root.
- Reuse the unchanged M132 publisher and retain atomic per-entry visibility,
  content verification, structured failures, and the documented possibility
  of an earlier valid entry or valid orphan CAS blob after later failure.
- Add immutable path-free `ludoweave.asset-cache-population/1` evidence that
  combines plan-ordered `hit`/`decoded` with `published`/`reused` status.
- Add `ludoweave source asset-cache-populate PROJECT --manifest FILE --assets
  FILE --lock FILE --plan FILE --cache DIRECTORY` only after current lock/plan
  verification and complete project-confined source acquisition.
- Prove cold, warm, mixed, stale-source, corrupt-cache, decoder-failure,
  limit-failure, publication-failure, CLI, and isolated-wheel behavior.
- Document read/write authority, determinism, trust, non-transactional failure,
  compatibility, and explicit remote/shared-writer/repair non-scope.
- Keep workflows, CI allocations, permissions, credentials, dependencies,
  lock, metadata, version, engine root, M131-M134 implementations, release
  authority, and remote state unchanged.

## Direction and evidence so far

- Primary sources accessed 2026-08-27: current Bazel remote-cache and Gradle
  build-cache documentation. They support declared input/output identity,
  cache lookup, execution of misses, later upload/store, and separately
  controlled read/write authority. They do not establish an all-plan
  transaction, rollback, hostile-concurrency safety, remote trust, repair,
  eviction, or new CI work.
- Exact M134 commit/tree/parent and clean baseline passed before branch
  creation. The additive source, CLI, unit/integration/architecture evidence,
  installed smoke, RFC-0118, and public docs are present while protected
  M131-M134 modules, dependencies, metadata, and workflows remain exact.
- Focused gates passed 39, 61, and 26 assertions. All 434 Python files are
  format-clean; Ruff and strict Pyright pass; strict docs and whitespace pass;
  1,683 architecture assertions pass with one established Windows capability
  skip; both governance modes return zero findings.
- Accepted suites pass 3,482 tests with 16 skips on exact CPython 3.12.13 and
  3,472 tests with 17 skips on exact CPython 3.13.13 and 3.14.5.
- All ten real-wgpu tests, both M7 profile contracts, Clockwork Arena, Agent
  World Builder, the primary wheel smoke, and all 17 focused isolated wheel
  consumers pass. The new cold/warm installed population report is exact.

## Explicit non-scope

- No implicit publication in `asset-realize`, all-plan transaction, rollback,
  repair, deletion, eviction, garbage collection, quota, migration, or legacy-
  cache trust.
- No remote cache, network, authentication, authorization, shared-writer or
  hostile-concurrency claim, upload/download protocol, retry transport, or
  external provider.
- No discovery/enumeration, watcher, reimport, scheduler, worker, process,
  thread, parallelism, callback, plugin, decoder registration, dynamic import,
  or arbitrary evaluation.
- No renderer upload, source/project write-back, world/session mutation,
  receipt, dependency, native/backend surface, metadata, version, engine-root
  API, workflow/job/allocation, permission, credential, release, publication,
  push, PR, or remote change.

## Remaining acceptance work

- Create the authorized local DCO commit and prove it postcommit. Do not push or
  create a PR while the public-review identity hold remains.
