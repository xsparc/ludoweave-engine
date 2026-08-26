# Current task

- **Task:** M136 - verify saved asset-cache population evidence against the
  exact current plan and local cache.
- **Status:** Implementation, documentation, focused/complete behavior,
  supported-Python, static, architecture, governance, real-wgpu, retained
  profile, vertical-slice, findings-first, and all installed-wheel consumer
  gates pass. Record-inclusive reproducibility, release rehearsal, and final
  scope/security review, cleanup, history/hosted audit, and final metadata
  separation pass. M136 is ready for the authorized local DCO commit.
- **Base:** Fully locally validated M135 DCO commit
  `59796814ee340254c11ccfde9330184ba7ef148d`, tree
  `e0cf313f78c830c2a93c07e29bacb130b7effa18`, with sole parent exact M134.
  The stack remains unpublished under the existing public-review identity
  hold.
- **Branch:** `release/m136-saved-cache-population-verification`.

## Acceptance boundary

- Strictly reconstruct saved `ludoweave.asset-cache-population/1` bytes under
  hard 8 MiB and 4,096-entry bounds, rejecting duplicates, non-finite values,
  exact-schema/type drift, invalid identities/statuses, and inconsistent
  counts or aggregate bytes.
- Completely preflight the report against the exact current plan before cache
  construction, then open only `AssetCacheStore(..., writable=False)`.
- Require every referenced action and CAS payload to pass unchanged M133
  verification and match the complete saved result identity, with no decoder,
  fallback, cache/project mutation, repair, or creation.
- Add immutable path-free
  `ludoweave.asset-cache-population-verification/1` evidence and the additive
  `source asset-cache-population-verify` CLI composition.
- Prove bounded decoding, current-cache success, plan mismatch before reads,
  missing action, corruption, result mismatch, CLI, and isolated-wheel
  behavior.
- Document that unsigned local digest agreement is integrity evidence only,
  not provenance, authenticity, builder identity, or a trusted timestamp.
- Keep workflows, CI allocations, permissions, credentials, dependencies,
  lock, metadata, version, engine root, M131-M135 implementations, release
  authority, and remote state unchanged.

## Direction and evidence so far

- Primary sources accessed 2026-08-27: current Bazel remote-cache, Python 3.12
  JSON, and SLSA 1.2 artifact-verification documentation. They support separate
  action/CAS verification, strict duplicate rejection, and explicit trust-root
  requirements for authenticity claims.
- Exact M135 commit/tree/parent and clean baseline passed before branch
  creation. The additive reader, verifier, CLI, tests, installed smoke,
  RFC-0119, and public docs are present while protected prior surfaces,
  dependencies, metadata, and workflows remain exact.
- Focused gates pass 21, 38, and 47 assertions. All 438 Python files are
  format-clean; Ruff and strict Pyright pass; strict docs and whitespace pass;
  1,688 architecture assertions pass with one established Windows capability
  skip; both correctly targeted governance modes return zero findings.
- Accepted suites pass 3,503 tests with 16 skips on exact CPython 3.12.13 and
  3,493 tests with 17 skips on exact CPython 3.13.13 and 3.14.5.
- All ten real-wgpu tests, eight M7 profile assertions, Clockwork Arena, Agent
  World Builder, the primary wheel smoke, and all 18 focused isolated wheel
  consumers pass. The new installed verification report is exact and the
  project/cache snapshots remain unchanged.

## Explicit non-scope

- No cache publication, creation, write, repair, deletion, eviction, garbage
  collection, quota, migration, decoder, fallback, or historical-event proof.
- No remote cache, network, authentication, authorization, signature,
  attestation, trust root, provenance/authenticity claim, shared-writer or
  hostile-concurrency claim, or external provider.
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
