# Current task

- **Task:** M133 - add verified read-only asset cache lookup.
- **Status:** Implementation, documentation, complete reviewed validation,
  records, scratch cleanup, history/hosted audit, and final metadata separation
  are complete. M133 is ready for the authorized local DCO commit.
- **Base:** Fully locally validated M132 DCO commit
  `da62eda909cbf47abfd7ef1e8c83a52466d8210a`, tree
  `ad2d0e147147a430ca2738fb27448750462e2a09`, with sole parent exact M131.
  The stack remains unpublished under the existing public-review identity
  hold.
- **Branch:** `release/m133-verified-asset-cache-lookup`.

## Acceptance boundary

- Preserve M132 creating/publishing behavior by default while adding exact
  `writable=False` authority that creates nothing and rejects publication.
- Inspect only action keys from an exact current `AssetBuildPlan`; never
  enumerate unrelated cache history.
- Treat an absent action as an exact miss, including when an orphan CAS blob
  exists. Treat every present malformed, incomplete, unreadable, aliased, or
  mismatched entry as fail-closed corruption rather than a miss.
- Bound metadata before parsing; require strict UTF-8, unique object names,
  finite standard JSON, the exact field set, and exact canonical bytes.
- Reconstruct a validated result entry and match URI, kind, cache key, and
  source byte count to the current plan entry before accepting the action.
- Verify the referenced ordinary CAS payload's bounded byte count and SHA-256
  on every hit.
- Add immutable path-free plan-ordered
  `ludoweave.asset-cache-lookup/1` hit/miss evidence and focused experimental
  exports only.
- Add `ludoweave source asset-cache-check PROJECT --manifest FILE --assets FILE
  --lock FILE --plan FILE --cache DIRECTORY` after complete current lock/plan
  verification. It must not acquire decoder inputs, materialize, publish,
  repair, delete, or mutate project/cache data.
- Add unit, CLI, architecture, and isolated no-dependency wheel evidence.
- Document integrity versus authenticity, ownership, read/write authority,
  determinism, missing/corrupt behavior, compatibility, and explicit
  cache-assisted-execution/remote/mutation non-scope.
- Keep workflows, CI allocations, permissions, credentials, dependencies,
  lock, metadata, version, engine root, execution/pipeline/lock/plan contracts,
  M132 publication behavior/evidence, release authority, and remote state
  unchanged.

## Direction and baseline evidence

- Primary sources accessed 2026-08-26: current Bazel remote-cache
  documentation, Gradle 9.7 build-cache documentation, and Python JSON decoder
  documentation. They support stable action-key lookup, separate CAS payloads,
  independent read/write authority, exact misses, size-bounded parsing, and
  explicit duplicate-name rejection.
- They do not justify cache authenticity, decode bypass, mixed-hit execution,
  enumeration, remote transport, shared writers, repair, eviction, workers, or
  CI changes.
- Exact M132 commit/tree/parent, clean status, and `0 33` divergence pass. The
  unchanged lock resolves and 38 focused M132 assertions pass in 4.40 seconds.
- The deliberate-red unit contract stopped on absent lookup exports. After
  implementation, one fixture-root omission and seven strict typing issues
  were corrected; all 26 unit/retained-boundary assertions then passed.
- CLI, installed source, strict parsing, and M133 boundaries were added. Ruff
  and strict Pyright pass; all 37 pre-documentation assertions pass except the
  intentionally absent RFC/public-doc boundary.
- Documentation-inclusive validation passes all 426 Python files, Ruff,
  strict Pyright, 55 focused assertions in 8.64 seconds, strict docs in 1.72
  seconds, and whitespace. The isolated no-dependency wheel lookup smoke
  passes.
- Complete validation passes 1,675 architecture assertions, the full supported
  interpreter matrix, real wgpu, both profiles and vertical slices,
  reproducible distributions, all 16 isolated wheel consumers, two identical
  release rehearsals, archive hygiene, and protected/identity/credential
  scans. Review-hardened final suite counts are 3,453/16 on Python 3.12 and
  3,443/17 on both 3.13 and 3.14.

## Explicit non-scope

- No cache-assisted execution, decoder bypass, mixed hit/miss materialization,
  automatic publication, repair, deletion, eviction, garbage collection,
  quota, migration, or legacy-cache trust.
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

- Run the final metadata and M133 boundary separator after this factual record.
- Create the authorized local DCO commit and prove it postcommit. Do not push or
  create a PR while the public-review identity hold remains.
