# Current task

- **Task:** M132 - add verified local asset cache publication.
- **Status:** Implementation, documentation, findings-first review, complete
  validation, factual records, scratch cleanup, and history/hosted audit are
  complete. M132 is ready for the authorized local DCO commit.
- **Base:** Fully locally validated M131 DCO commit
  `ea472476ee5cfca05afeda90fa888bf5557a3128`, tree
  `7de987430ac34cf22071cfcb58644b65b32f8d21`, with sole parent exact M130.
  The stack remains unpublished under the existing public-review identity
  hold.
- **Branch:** `release/m132-verified-local-asset-cache`.

## Acceptance boundary

- Add frozen exact materialization values that pair every retained payload
  with the corresponding M131 result entry after the unchanged complete
  preflight, decoder, and resource-limit chain.
- Preserve identity-only `execute_asset_build_plan()` behavior; payload
  retention requires the separate explicit materialization function.
- Add one caller-authorized local `AssetCacheStore`; project composition must
  reject cache roots equal to, inside, or containing the project root.
- Separate `cas/` payloads addressed by artifact SHA-256 from `actions/`
  canonical `ludoweave.asset-cache-entry/1` metadata addressed by the existing
  M4/M129 cache key.
- Verify exact metadata bytes, ordinary-file layout, payload byte count, and
  payload SHA-256 on every hit or collision. Missing actions are misses;
  corruption fails closed without overwrite, repair, or deletion.
- Stage blobs and action directories beside their destinations, flush owned
  file content, publish with same-filesystem replacement, and remove every
  still-owned staging path on success or failure.
- Publish CAS content before atomic per-entry action visibility. Document that
  valid orphan blobs or earlier valid entries may remain after a later storage
  failure without becoming partial cache hits.
- Add `ludoweave source asset-cache PROJECT --manifest FILE --assets FILE
  --lock FILE --plan FILE --cache DIRECTORY` only after complete M130/M131
  verification, acquisition, and materialization.
- Emit path-free deterministic `ludoweave.asset-cache-publish/1` summaries with
  exact plan/artifact identities and `published` or `reused` status.
- Add unit, CLI, architecture, and isolated no-dependency wheel evidence.
- Document ownership, atomicity, corruption, cleanup, determinism,
  compatibility, and explicit remote/eviction/worker/project-write non-scope.
- Keep workflows, CI allocations, permissions, credentials, dependencies,
  lock, metadata, version, engine root, legacy pipeline/protocols, release
  authority, and remote state unchanged.

## Direction and baseline evidence

- Primary sources accessed 2026-08-26: current Bazel remote-cache
  documentation, the Remote Execution API, Gradle 9.7 build-cache concepts,
  and Python 3.14 `os.replace()` documentation. They support separate CAS and
  action identities, digest verification, repeatable/non-overlapping outputs,
  payload-before-action ordering, and destination-filesystem replacement.
- They do not justify remote transport, shared cache writers, authentication,
  automatic eviction, background maintenance, parallel execution, or CI
  changes.
- Exact M131 commit/tree/parent, clean status, and `0 32` divergence pass. The
  focused M131 execution/import/API baseline passes 126 tests in 6.13 seconds;
  the unchanged 46-package lock and static governance pass.
- Four new contract files were formatted mechanically. Behavior collection
  then stopped only on absent materialization/cache exports. After correcting
  one guessed M131 smoke hash, the protected-surface assertion passed and
  three intended implementation/CLI/installed-docs boundaries failed.
- The first implementation checkpoint found two deterministic ordering lint
  issues, one exception-chaining lint issue, and three strict typing issues.
  After corrections, strict typing passes and 40 focused behavior/historical
  assertions pass; only installed/docs evidence remains intentionally absent.
- Review corrected the initial combined action/payload layout to the adopted
  distinct artifact-digest CAS and cache-key action index before documentation.

## Explicit non-scope

- No remote cache, HTTP/gRPC, network, authentication, authorization, shared
  service, upload/download protocol, retry transport, or external provider.
- No cache eviction, garbage collection, quota, deletion API, repair,
  overwrite-on-corruption, migration, or legacy-cache trust.
- No all-plan transaction, rollback of valid content-addressed entries,
  scheduler, worker, process, thread, parallel execution, callback, plugin,
  decoder registration, dynamic import, or arbitrary evaluation.
- No discovery, glob, watcher, live update, import/reimport, renderer upload,
  source/project write-back, world/session, command, transaction, mutation, or
  receipt.
- No dependency, native/backend surface, metadata, version, engine-root API,
  workflow/job/allocation, permission, credential, release, publication, push,
  PR, or remote change.

## Remaining acceptance work

- Create the authorized local DCO commit and prove it postcommit. Do not push or
  create a PR while the public-review identity hold remains.
