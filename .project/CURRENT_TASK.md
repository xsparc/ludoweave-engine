# Current task

- **Task:** M140 - diagnose saved cache-fingerprint differences through a fixed
  path-free aggregate report.
- **Status:** Primary-source direction, implementation/hardening, supported-
  Python behavior, static/architecture/docs/governance, real-wgpu, profiles,
  vertical slices, all 23 installed-wheel consumers, reproducible distributions,
  release rehearsal, scope/security/archive review, history/hosted audit, branch
  pruning, and bounded cleanup pass. M140 is ready for the authorized local DCO
  commit. No CI change was made.
- **Base:** Fully locally validated M139 DCO commit
  `e7c01044da87004cea065fd07f379ea7ba09128f`, tree
  `c52f9af36d464d539df1bb2164a3e7b56e2741be`, with sole parent exact M138.
  The stack remains unpublished under the existing public-review identity hold.
- **Branch:** `release/m140-path-free-cache-fingerprint-comparison`.

## Acceptance boundary

- Bind the exact saved M139 fingerprint to the supplied plan before cache
  construction and reuse exactly one unchanged M138 bounded read-only
  observation.
- Return frozen canonical
  `ludoweave.asset-cache-fingerprint-comparison/1` evidence containing only
  equal/different status, fingerprint protocol, plan digest, one observation-
  equality flag, and signed deltas for the twelve existing M137 aggregates.
- Preserve identity-only change detection when all aggregate deltas are zero,
  without publishing either observation digest or any object identity.
- Add `source asset-cache-fingerprint-compare`: exit 0 for equal, exit 1 with a
  diagnostic report for different, and retain structured exit 2 for invalid or
  failed processing.
- Add isolated-wheel proof, RFC-0123, public documentation, and architecture
  enforcement while keeping cache layout, M137-M139 protocols and bytes,
  workflows, dependencies, metadata, version, engine root, release authority,
  and prior evidence unchanged.
- State explicitly that aggregate comparison is local change evidence, not
  authenticity, provenance, an atomic snapshot, or retention/deletion/cleanup
  authority.

## Direction and evidence so far

- Primary sources accessed 2026-08-27: NIST Privacy Framework, OpenTelemetry
  sensitive-data guidance, and RFC 6902. They support data minimization and
  aggregation while demonstrating that a generic JSON Patch requires paths and
  can carry values.
- Exact M139 commit/tree/parent and clean baseline were established before the
  neutral M140 branch was created.
- Core comparison, export, CLI composition, focused unit/integration coverage,
  installed-wheel source, RFC-0123, public docs, and an architecture boundary
  are additive.
- All 453 Python files are format-clean; Ruff and strict Pyright pass; 1,712
  architecture assertions pass with one established skip; exact CPython
  3.12-3.14 full suites, strict docs/governance, real-wgpu, profiles, both
  vertical slices, and all 23 isolated installed-wheel consumers pass.

## Explicit non-scope

- No per-object diff/list, JSON Patch, cache key, URI, artifact/action/blob
  identity, filename, path, payload, expected/current observation digest,
  timestamp, age, telemetry export, or redaction policy.
- No signature, key/root of trust, authenticated builder/channel, trusted
  timestamp, attestation, transparency log, provenance/authenticity claim,
  remote cache, or network.
- No atomic snapshot, hostile-concurrency guarantee, retention root, lease,
  pin, generation, cleanup policy, write, repair, deletion, eviction, garbage
  collection, quota enforcement, mutation, migration, or rollback.
- No decoder/fallback/source acquisition, watcher, scheduler, worker, process,
  thread, parallelism, plugin, dynamic import/evaluation, renderer upload,
  project/world mutation, receipt, dependency, native/backend surface,
  metadata, version, engine-root API, workflow/allocation, permission,
  credential, release, publication, push, PR, or remote change.

## Remaining acceptance work

- Create the authorized local DCO commit and prove it postcommit. Do not push or
  create a PR while the public-review identity hold remains.
