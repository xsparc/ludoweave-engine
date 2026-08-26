# Current task

- **Task:** M141 - compare two canonical saved cache fingerprints offline
  through the fixed M140 path-free report.
- **Status:** Runtime, CLI, tests, architecture, documentation, complete local
  validation, reproducible distribution, installed-consumer proof, release
  rehearsal, evidence normalization, and generated-output cleanup pass. The
  authorized local DCO commit remains. No CI change is needed.
- **Base:** Fully locally validated M140 DCO commit
  `81d55ac7b531d5782aec8723a8df9b0be18b49ca`, tree
  `710867b3c6229c4c3bb86f0e1b80b1c1ce9cc2b3`, with sole parent exact M139.
  The stack remains unpublished under the existing public-review identity hold.
- **Branch:** `release/m141-offline-cache-fingerprint-comparison`.

## Acceptance boundary

- Add a pure function that requires one exact plan and two exact admitted M138
  fingerprint values, binds both nested plan digests, and performs no cache or
  filesystem access.
- Reuse frozen canonical
  `ludoweave.asset-cache-fingerprint-comparison/1` unchanged, with twelve
  signed `current - expected` M137 aggregate deltas and one exact-observation
  equality flag.
- Preserve identity-only change detection with all-zero aggregate deltas and
  publish neither saved observation digest nor any cache/object identity.
- Add `source asset-cache-fingerprint-record-compare`: verify current inputs,
  read/decode exactly two bounded project-confined canonical records, then exit
  0 for equal, 1 for diagnostic different, or 2 for invalid processing.
- Prove the CLI works after the originating cache is absent. Add isolated-wheel
  proof, RFC-0124, public docs, and architecture enforcement while preserving
  cache layout, M137-M140 protocols/bytes, workflows, dependencies, version,
  engine root, release authority, and prior evidence.
- State explicitly that comparison of two unsigned records is local integrity
  evidence, not chronology, authenticity, provenance, an atomic snapshot, or
  retention/deletion/cleanup authority.

## Direction and evidence so far

- Primary sources accessed 2026-08-27: NIST FIPS 180-4, OpenTelemetry
  sensitive-data guidance, SLSA 1.2 artifact verification, and GitHub workflow/
  attestation guidance. They support aggregate change detection while requiring
  separate trust roots/signatures/expectations for authenticity and avoiding
  hosted signing of frequent test builds.
- Exact M140 commit/tree/parent and clean worktree were established before the
  neutral M141 branch was created; the redundant contained M140 branch was
  pruned.
- The pure record comparison, export, CLI, unit/integration tests, installed
  smoke, RFC-0124, public docs, and architecture boundary are additive.
- All 456 Python files are format-clean; Ruff and strict Pyright pass; 1,717
  architecture assertions pass with one established skip; strict docs and both
  governance modes pass; exact CPython 3.12-3.14, real-wgpu, profiles, and both
  deterministic vertical slices pass.
- The final pure wheel and source archive reproduce byte-for-byte; all 24
  isolated installed-wheel consumers pass; two byte-identical ten-artifact
  release rehearsals pass; archive, protected-surface, disclosure, identity,
  credential, history, and object-integrity audits are clean.
- Fresh fetch and hosted queries still expose only exact M99 `main`, no open PR,
  no post-M99 run, and no release. M141 therefore remains local rather than
  publishing a 42-milestone stack onto a stale public base.

## Explicit non-scope

- No cache argument, construction, access, fresh observation, source-payload
  acquisition, record storage, write-back, per-object diff/list, JSON Patch,
  cache key, URI, artifact/action/blob identity, filename/path, payload, or
  expected/current observation digest disclosure.
- No signature, key/root of trust, authenticated builder/channel, trusted
  timestamp, attestation, transparency log, provenance/authenticity claim,
  remote cache, network, telemetry export, or redaction policy.
- No atomic snapshot, hostile-concurrency guarantee, retention root, lease,
  pin, generation, cleanup policy, write, repair, deletion, eviction, garbage
  collection, quota enforcement, mutation, migration, or rollback.
- No watcher, scheduler, worker, process, thread, parallelism, plugin, dynamic
  import/evaluation, renderer upload, project/world mutation, receipt,
  dependency, native/backend surface, metadata, version, engine-root API,
  workflow/allocation, permission, credential, release, publication, push, PR,
  or remote change.

## Remaining acceptance work

- Create the authorized local DCO commit and prove it postcommit. Do not push or
  create a PR while the public-review identity hold remains.
