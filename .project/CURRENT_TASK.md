# Current task

- **Task:** M142 - strictly admit and verify one saved M140 cache-fingerprint
  comparison against an exact plan and two admitted fingerprints offline.
- **Status:** Runtime, CLI, tests, architecture, documentation, complete local
  validation, reproducible distribution, all installed consumers, release
  rehearsal, findings-first review, final scope/history/hosted-state audits,
  and the authorized local DCO commit are complete. No CI change was needed.
- **Base:** Fully locally validated M141 DCO commit
  `bff0e111b40a6e4b342fe4e5b93307d770b7be95`, tree
  `bc5476e90d05ae4f2c27a2d2eebecc0821331a41`, with sole parent exact M140.
  The stack remains unpublished under the existing public-review identity hold.
- **Branch:** `release/m142-saved-cache-fingerprint-comparison-verification`.

## Acceptance boundary

- Add tightening-only 4,096-byte admission for exact canonical M140 comparison
  records; reject duplicate names, non-finite values, overlong integers,
  unknown/missing fields, invalid primitives/protocols/status, out-of-range
  signed deltas, and noncanonical bytes.
- Add a pure verifier that reruns M141 from one exact plan and two exact admitted
  fingerprints, requires exact frozen comparison equality, and performs no
  filesystem, cache, environment, clock, process, thread, or network access.
- Emit frozen path-free
  `ludoweave.asset-cache-fingerprint-comparison-verification/1` with plan,
  protocols, comparison status, and digest of the already-public canonical
  comparison report. Publish neither fingerprint observation digest nor any
  cache/object identity.
- Add `source asset-cache-fingerprint-comparison-verify`: preflight current
  inputs, independently read/decode two bounded fingerprints and one bounded
  comparison, then exit 0 for correctly derived equal or different evidence and
  2 for invalid/mismatched processing.
- Prove operation after originating caches are absent. Add isolated-wheel proof,
  RFC-0125, public docs, and architecture enforcement while preserving cache
  layout, M137-M141 protocols/bytes, workflows, dependencies, version, engine
  root, release authority, and prior evidence.
- State explicitly that verification of unsigned records is local integrity
  evidence, not chronology, authenticity, provenance, an atomic snapshot, or
  retention/deletion/cleanup authority.

## Direction and evidence so far

- Primary sources accessed 2026-08-27: RFC 8785, Python 3.12 JSON, NIST FIPS
  180-4, OpenTelemetry sensitive-data, SLSA 1.2 verification, GitHub workflow/
  billing, and repository-agent customization guidance. They support bounded
  canonical local recomputation, disclosure minimization, separate trust roots
  for authenticity, and no workflow expansion for this slice.
- Exact M141 commit/tree/parent and clean worktree were established before the
  neutral M142 branch was created; the redundant contained M141 branch was
  pruned.
- The strict decoder, pure verifier, focused exports, CLI, unit/integration
  tests, installed smoke, RFC-0125, public docs, and architecture boundary are
  additive. Findings-first review also closed structured UTF-8 encoding failure
  translation for unpaired-surrogate `str` input.
- All 460 Python files are format-clean; Ruff and strict Pyright pass; 1,722
  architecture assertions pass with one established skip; strict docs and both
  governance modes pass; exact CPython 3.12-3.14, real-wgpu, profiles, and both
  deterministic vertical slices pass.
- Two final distributions reproduce byte-for-byte; all 25 isolated installed
  consumers pass; two byte-identical ten-artifact release rehearsals pass; and
  archive, protected-surface, disclosure, identity, credential, history, and
  object-integrity audits are clean.
- Fresh fetch and hosted queries still expose only exact M99 `main`, no open PR,
  no post-M99 run, and no release. M142 therefore remains local rather than
  publishing a 43-milestone stack onto a stale public base.

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

- No local M142 acceptance work remains. Keep the commit unpublished while the
  public-review identity hold remains, then start the next approved,
  research-gated milestone from the exact committed M142 tip.
