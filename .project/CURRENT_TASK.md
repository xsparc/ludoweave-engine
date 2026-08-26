# Current task

- **Task:** M134 - add read-only cache-assisted asset realization.
- **Status:** Implementation, documentation, findings-first review, complete
  validation, record-inclusive packaging, and final artifact rehearsal are
  complete. Scratch cleanup, history/hosted audit, and final metadata
  separation are complete. M134 is ready for the authorized local DCO commit.
- **Base:** Fully locally validated M133 DCO commit
  `e3f79339bc5765ec8f11a0dee6b6e8cb3e687845`, tree
  `9c38e2115e04443dd8c2a61a5acea1b0cfd03d02`, with sole parent exact M132.
  The stack remains unpublished under the existing public-review identity
  hold.
- **Branch:** `release/m134-cache-assisted-asset-realization`.

## Acceptance boundary

- Preflight every exact detached source for order, byte count, SHA-256, and
  existing tightening-only limits before the first cache action read.
- Resolve and verify every exact M133 cache candidate before any miss decoder
  runs. Present corruption and cached-hit limit failures remain fail-closed.
- Decode only exact misses with the unchanged M131 built-in decoder kernel;
  merge hits and decoded artifacts in canonical plan order.
- Apply the existing per-entry and aggregate artifact limits while retaining
  plan-order failure identity parity with uncached materialization.
- Add immutable path-free `ludoweave.asset-build-realization/1` evidence with
  exact `hit` or `decoded` status and no payload in its report.
- Add `ludoweave source asset-realize PROJECT --manifest FILE --assets FILE
  --lock FILE --plan FILE --cache DIRECTORY` after current lock/plan
  verification and complete project-confined source acquisition.
- Keep the operation read-only: a missing cache remains absent and neither
  project nor cache is changed on hit, miss, corruption, limit, or decode paths.
- Add unit, CLI, architecture, and isolated no-dependency wheel evidence.
- Document ownership, determinism, verification/decode ordering, failure
  behavior, compatibility, and explicit automatic-publication/remote non-scope.
- Keep workflows, CI allocations, permissions, credentials, dependencies,
  lock, metadata, version, engine root, execution/cache/pipeline/lock/plan
  contracts, M133 lookup evidence, release authority, and remote state unchanged.

## Direction and baseline evidence

- Primary sources accessed 2026-08-26: current Bazel remote-cache and Gradle
  build-cache documentation. They support declared actions, complete stable
  inputs, verified cache reuse, decode/execute misses, and independently
  disabled writes. They do not justify automatic publication, remote
  transport, shared writers, repair, eviction, discovery, plugins, or CI work.
- Exact M133 commit/tree/parent, clean status, and `0 34` divergence pass.
  The unchanged lock resolves; 49 focused M133 behavior tests and 112 retained
  architecture assertions pass. The deliberate-red contract stopped only on
  absent realization exports.
- Additive implementation, CLI, installed source, RFC, and architecture guard
  pass formatting, Ruff, strict Pyright, 75 focused assertions, strict docs,
  and whitespace while the M131 execution and M133 cache files remain exact.
- Complete static validation passes all 430 Python files and 1,679 architecture
  assertions with one established Windows capability skip. Both governance
  modes return zero findings.
- Findings-first review corrected mixed-hit aggregate-limit attribution by
  separating cache-phase safety accounting from canonical plan-order
  accounting. The strengthened focused gate passes 39 assertions.
- Accepted post-review suites pass 3,467 tests with 16 skips on CPython 3.12.13
  and 3,457 tests with 17 skips on exact 3.13.13 and 3.14.5.
- All ten real-wgpu tests, both M7 profile contracts, both deterministic
  vertical slices, two initial byte-identical distributions, all 17 isolated
  wheel consumers, and two byte-identical ten-artifact release stages pass.
  Record-inclusive packaging remains to run after this evidence update.

## Explicit non-scope

- No automatic cache publication, repair, deletion, eviction, garbage
  collection, quota, migration, or legacy-cache trust.
- No remote cache, network, authentication, authorization, shared service,
  upload/download protocol, retry transport, or external provider.
- No discovery/enumeration, glob, watcher, reimport, scheduler, worker,
  process, thread, parallelism, callback, plugin, decoder registration,
  dynamic import, or arbitrary evaluation.
- No renderer upload, source/project write-back, world/session, command,
  transaction, mutation, receipt, dependency, native/backend surface,
  metadata, version, engine-root API, workflow/job/allocation, permission,
  credential, release, publication, push, PR, or remote change.

## Remaining acceptance work

- Create the authorized local DCO commit and prove it postcommit. Do not push or
  create a PR while the public-review identity hold remains.
