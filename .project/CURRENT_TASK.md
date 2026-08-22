# Current task

- **Task:** M95 - local-header compression-method consistency preflight
- **Status:** Implementation, local qualification, and precommit review are
  complete; exact-head hosted qualification and integration remain.
- **Base:** Verified M94 closeout squash
  `a19db05c096c6d22e5871373bc738d282516635c`, tree
  `82b7378fd5634202cf3d21e3fe8aa4590faea4d4`.
- **Branch:** `release/m95-local-header-compression-consistency`.

## Accepted scope

- After M94 local-flag consistency, read exactly two little-endian bytes at
  each parser-exposed `ZipInfo.header_offset + 8` from the owned checksum-
  admitted snapshot.
- Require the local compression method to equal the corresponding central
  `ZipInfo.compress_type`.
- Raise stable content-silent error `sample bundle local header compression
  methods are inconsistent` before decoded-name policy, metadata, exact
  inventory, staging, or member reads.
- Preserve every established policy through M94, empty-archive inventory
  behavior, owned-resource cleanup, and caller snapshot position.
- Add RFC-0078 plus aligned public, security, architecture, release, roadmap,
  maintainer, test, and factual project records.
- Keep workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, and publication unchanged.

## Explicit non-scope

- No local extra-field comparison or parsing; no version/time/CRC/size or
  field-wide local/central comparison; no new compression-method allowlist.
- No complete local-record or payload bound, next-header bound, gap, adjacency,
  contiguity, physical overlap rule, or inter-member layout validator.
- No archive repair, general archive sandbox, public release observation,
  workflow change, runtime feature, dependency, native/WASM work, tag, release,
  or publication.

## Direction and red evidence

- Clean M94 audit found exact local/remote closeout
  `a19db05c096c6d22e5871373bc738d282516635c`, only `main`, no open PR, exact-
  squash run, tag, or release, valid DCO/signatures, and no M94 scratch targets.
- PKWARE APPNOTE 6.3.10 defines a two-byte compression method in corresponding
  local and central records. CPython exposes the central value through public
  `ZipInfo.compress_type` and the local pointer through `header_offset`.
- A temporary probe changed only the second local method from deflate 8 to
  stored 0. Exact CPython 3.12.13, 3.13.13, and 3.14.5 each retained central
  methods `[8, 8]`, local methods `[8, 0]`, offsets `[0, 54]`, and read both
  payloads. Its first format check required one mechanical wrap; Ruff passed,
  then the corrected format/Ruff gate passed.
- The first contract static checkpoint required formatting and strict Pyright
  reported 17 unknown lambda-parameter findings; Ruff passed. Typed named
  mutators and one formatter pass corrected it, after which format, Ruff, and
  strict Pyright passed.
- The corrected 25-assertion M95 contract passed 15 standard-library behavior,
  inherited precedence, empty-archive, producer, and protected-surface
  controls. Ten stable-error, helper, cleanup, ordering, and documentation
  assertions failed because the M95 policy/RFC did not exist. No complete pass
  is claimed from that red checkpoint.

## Local acceptance evidence

- The implementation is exactly one constant, one ordered call, and one
  position-restoring equality helper plus RFC/public/project records. All 49
  combined M94-M95 assertions pass.
- All 25 focused assertions pass on exact CPython 3.12.13, 3.13.13, and 3.14.5.
  Each complete suite passes 2,752 tests with 16 established skips.
- Static, docs, all 1,222 architecture assertions with one established Windows
  capability skip, metadata, real-wgpu, profiles, vertical slices,
  reproducible artifacts, wheel/staging/release smoke, and the findings-first
  scope/security/archive/integrity review pass after the recorded graphics-
  environment correction.

## Remaining acceptance work

- Publish one DCO feature commit through the existing quota-conscious three-
  allocation gate, two exact-head audits, guarded squash, bounded integration
  record, no-workflow closeout, and complete branch/generated-target cleanup.
