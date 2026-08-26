# Current task

- **Task:** M139 - strictly decode one saved cache-observation fingerprint and
  compare it with one fresh bounded read-only observation.
- **Status:** Primary-source direction, implementation, hardening, supported-
  Python behavior, static/architecture/docs/governance, real-wgpu, profiles,
  vertical slices, reproducible distributions, the primary plus all 21 focused
  installed-wheel consumers, release rehearsal, scope/security/archive review,
  precommit history/hosted audit, final metadata separation, and bounded cleanup
  pass. M139 is ready for the authorized local DCO commit.
- **Base:** Fully locally validated M138 DCO commit
  `aeca2b3ea1c1e6122df4080641f707e36a9a43d7`, tree
  `28c6e0a5b423eb7e340d5ffa010d9997c1d408af`, with sole parent exact M137.
  The stack remains unpublished under the existing public-review identity
  hold.
- **Branch:** `release/m139-saved-cache-fingerprint-verification`.

## Acceptance boundary

- Decode one project-confined canonical `ludoweave.asset-cache-fingerprint/1`
  record under a 65,536-byte tightening-only bound with duplicate-name,
  non-finite-number, exact-schema/type/protocol/digest/aggregate, and canonical-
  byte rejection.
- Completely bind the saved nested inventory to the exact current plan before
  constructing or observing the cache.
- Reuse exactly one M138 bounded read-only observation and require exact nested
  inventory plus observation-digest equality.
- Return frozen path-free
  `ludoweave.asset-cache-fingerprint-verification/1` success without exposing
  differing cache identities or content.
- Add `source asset-cache-fingerprint-verify`, isolated-wheel proof, RFC-0122,
  public documentation, and architecture enforcement while keeping cache
  layout, M138 fingerprint bytes, workflows, dependencies, metadata, version,
  engine root, release authority, and prior evidence unchanged.
- State explicitly that agreement is local integrity equality, not
  authenticity, provenance, atomic snapshot, retention, deletion, cleanup, or
  mutation authority.

## Direction and evidence so far

- Primary sources accessed 2026-08-27: Python 3.12 JSON, NIST FIPS 180-4, and
  SLSA 1.2 artifact-verification documentation. They support bounded ambiguity-
  rejecting decode and changed-message detection while requiring separate
  signatures, roots of trust, subject binding, and expectations for
  authenticity.
- Exact M138 commit/tree/parent and clean whitespace baseline passed before the
  neutral M139 branch was created.
- The strict decoder/verifier, focused exports, CLI, unit/integration tests,
  installed smoke, RFC-0122, architecture boundary, and public docs are
  additive. An initial focused 18-test gate passed; the expanded pre-doc gate
  passed 50 assertions in 29.34 seconds with clean Ruff.
- The corrected focused gate passed strict Pyright and 45 behavior/CLI/boundary
  assertions; a whitespace-sensitive documentation assertion was normalized
  and the corrected 45-test run plus strict docs passed.
- Review independently capped every detached inventory field; all 20 hardened
  unit/boundary assertions, 449-file static gate, 1,706 architecture assertions
  with one established skip, strict docs, and both governance modes pass.
- Exact CPython 3.12.13/3.13.13/3.14.5 passed 3,562/3,552/3,552 tests with
  16/17/17 established skips. Real-wgpu, profiles, both vertical slices, and
  the primary plus all 21 focused installed consumers pass.

## Explicit non-scope

- No signature, key management, root of trust, authenticated builder/channel,
  trusted timestamp, attestation, transparency log, provenance/authenticity
  claim, or remote cache/network.
- No per-object public diff/list, retention root, pin/lease/generation,
  timestamp/age/access-time policy, atomic snapshot, or hostile-concurrency
  guarantee.
- No cache/project creation, publication, write, repair, deletion, eviction,
  garbage collection, quota enforcement, cleanup recommendation, migration, or
  rollback.
- No decoder/fallback/source acquisition, watcher, scheduler, worker, process,
  thread, parallelism, plugin, dynamic import/evaluation, renderer upload,
  project/world mutation, receipt, dependency, native/backend surface,
  metadata, version, engine-root API, workflow/allocation, permission,
  credential, release, publication, push, PR, or remote change.

## Remaining acceptance work

- Create the authorized local DCO commit and prove it
  postcommit. Do not push or create a PR while the public-review identity hold
  remains.
