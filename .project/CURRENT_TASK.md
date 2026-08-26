# Current task

- **Task:** M138 - add a deterministic path-free fingerprint over one exact
  bounded sequential local-cache observation.
- **Status:** Primary-source direction, implementation, focused/complete
  behavior, supported-Python, static, architecture, strict typing/docs,
  governance, real-wgpu, retained profiles, vertical slices, findings-first
  review, record-inclusive reproducibility, all installed-wheel consumers,
  release rehearsal, final scope/security/archive review, bounded cleanup, and
  history/hosted audit, and final metadata separation pass. M138 is ready for
  the authorized local DCO commit.
- **Base:** Fully locally validated M137 DCO commit
  `b5b904b22303991474ed99a8ed4473738070dd45`, tree
  `5fe36bb63ec751406e690d279776a0bf5d97ebff`, with sole parent exact M136.
  The stack remains unpublished under the existing public-review identity
  hold.
- **Branch:** `release/m138-deterministic-cache-observation-fingerprint`.

## Acceptance boundary

- Reuse exactly one M137 bounded no-follow read-only storage observation so the
  aggregate inventory and fingerprint derive from the same verified action/CAS
  identities without a second enumeration.
- Hash a protocol domain plus sorted typed length-framed records: exact
  canonical action metadata by cache key, then raw CAS SHA-256 and byte count by
  artifact digest.
- Return frozen path-free `ludoweave.asset-cache-fingerprint/1` evidence nesting
  the unchanged M137 inventory and one plan-independent
  `observation_sha256`.
- Keep current-plan classification distinct from storage identity; an equal
  cache observation may accompany a different plan-relative inventory.
- Add `source asset-cache-fingerprint`, isolated-wheel proof, RFC-0121, public
  documentation, and architecture enforcement while keeping cache layout,
  workflows, dependencies, metadata, version, engine root, release authority,
  and prior evidence unchanged.
- State explicitly that a fingerprint is one sequential observation, not an
  atomic snapshot, diff, retention root, last-use record, provenance statement,
  deletion eligibility, or cleanup authorization.

## Direction and evidence so far

- Primary sources accessed 2026-08-27: current Bazel remote-cache, Gradle 9.7.1
  cache-directory/cleanup, and Git garbage-collection documentation. They
  associate cleanup with explicit age/size and idle/managed policy or
  reachability/grace, while warning about concurrent writers. M137 lacks those
  deletion preconditions.
- Exact M137 commit/tree/parent and clean baseline passed before branch
  creation. The additive fingerprint contract, single-pass refactor, CLI,
  tests, installed smoke, RFC-0121, and public docs are present while protected
  workflows, dependencies, metadata, cache layout, M137 evidence, release
  scripts, and CI allocations remain exact.
- Ruff formatting/linting and strict Pyright pass. Strict docs build in 2.09
  seconds. After one whitespace-sensitive architecture assertion was
  corrected, all 53 focused M137-M138 unit/CLI/boundary assertions pass in
  29.03 seconds.
- The new isolated no-dependency consumer passes against an initial
  343,300-byte pure wheel at SHA-256
  `f6841676cd19ef6a8485de61fb3e7cc2dd3d50e6e754c63ac5b4413761b6a390`.
- Accepted suites pass 3,539 tests with 16 skips on exact CPython 3.12.13 and
  3,529 tests with 17 skips on exact CPython 3.13.13 and 3.14.5. All 445 Python
  files, 1,700 architecture assertions with one established skip, strict docs,
  governance, real-wgpu, profiles, and both deterministic vertical slices pass.

## Explicit non-scope

- No saved-fingerprint decoder/verifier, per-object public inventory, diff,
  retention root, pin/lease/generation, timestamp/age/access-time policy,
  atomic snapshot, or hostile-concurrency guarantee.
- No cache creation, publication, write, repair, deletion, eviction, garbage
  collection, quota enforcement, cleanup recommendation, migration, or rollback.
- No remote cache, network, authentication, authorization, signature,
  attestation, provenance/authenticity claim, shared writer, or external
  provider.
- No decoder, fallback, source acquisition, watcher, scheduler, worker,
  process, thread, parallelism, plugin, dynamic import/evaluation, renderer
  upload, project/world mutation, receipt, dependency, native/backend surface,
  metadata, version, engine-root API, workflow/allocation, permission,
  credential, release, publication, push, PR, or remote change.

## Remaining acceptance work

- Create the authorized local DCO commit and prove it postcommit. Do not push or
  create a PR while the public-review identity hold remains.
