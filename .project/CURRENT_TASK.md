# Current task

- **Task:** M94 - local-header flag-consistency preflight
- **Status:** Implementation, complete local qualification, review, and record-
  inclusive artifacts are green; exact-head hosted qualification remains.
- **Base:** Verified M93 closeout squash
  `1b189da618d2d2ea0b3208707ba209f81d1368cc`, synchronized exactly with
  `origin/main` before branch creation.
- **Branch:** `release/m94-local-header-flag-consistency`.

## Accepted scope

- After M93 local-name consistency, read exactly two little-endian bytes at
  each parser-exposed `ZipInfo.header_offset + 6` from the owned checksum-
  admitted snapshot.
- Require the local general-purpose flag field to equal the corresponding
  central `ZipInfo.flag_bits`.
- Raise stable content-silent error `sample bundle local header flags are
  inconsistent` before decoded-name policy, metadata, exact inventory,
  staging, or member reads.
- Preserve every established policy through M93, empty-archive inventory
  behavior, owned-resource cleanup, and caller snapshot position.
- Add RFC-0077 plus aligned public, security, architecture, release, roadmap,
  maintainer, test, and factual project records.
- Keep workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, and publication unchanged.

## Explicit non-scope

- No local compression-method comparison; no extra-field comparison or
  parsing; no version/time/CRC/size or field-wide local/central comparison.
- No broad flag allowlist, complete local-record or payload bound, next-header
  bound, gap, adjacency, contiguity, physical overlap rule, or inter-member
  layout validator.
- No archive repair, general archive sandbox, public release observation,
  workflow change, runtime feature, dependency, native/WASM work, tag, release,
  or publication.

## Direction and red evidence

- Clean-history audit found local `main`, `origin/main`, and `origin/HEAD` at
  exact M93 closeout with only `main` present locally/remotely and no worktree
  changes.
- PKWARE APPNOTE 6.3.10 defines a two-byte general-purpose flag in both local
  and central member records. CPython exposes the central value through public
  `ZipInfo.flag_bits` and the local pointer through `header_offset`.
- A format/Ruff-clean temporary probe changed only the second local flag from
  zero to encryption bit 0. Exact CPython 3.12.13, 3.13.13, and 3.14.5 each
  retained central flags `[0, 0]`, offsets `[0, 54]`, and successfully read
  both payloads. Initial sandboxed runtime attempts were blocked only by uv
  cache access and are not claimed as passes; the identical approved reruns
  exited zero.
- The initial M94 contract collected 24 assertions. Against unchanged M93
  behavior, 14 controls passed and 10 missing-policy/helper/order/docs
  assertions failed. The initial format check also requested one mechanical
  reflow; Ruff lint passed and the formatter subsequently applied that reflow.
  No complete pass was claimed from that red checkpoint.

## Local qualification

- Corrected combined M93-M94 checkpoint: 46 passed; focused format, Ruff,
  strict Pyright, and strict docs passed.
- Exact focused proof: all 24 M94 assertions passed on CPython 3.12.13,
  3.13.13, and 3.14.5.
- Complete exact suites: 2,727 passed with 16 established skips on each of
  CPython 3.12.13, 3.13.13, and 3.14.5.
- Locked baseline: 46-package lock resolved; 45-package exact CPython 3.12.13
  graphics environment restored.
- Repository gate: 337 files format clean; Ruff and strict Pyright passed;
  1,197 architecture assertions passed with one established skip after a fresh-
  base correction of one inherited Windows filesystem permission denial;
  strict docs, five metadata-hygiene assertions, and whitespace passed.
- All ten real-wgpu tests, both one-repeat profile contracts, Clockwork Arena,
  and Agent World Builder passed with established deterministic identities.
- Two fresh builds reproduced the pure wheel and source archive; isolated-wheel
  smoke, ten-artifact staging, and complete release smoke passed.

## Remaining acceptance work

- Create one DCO-signed feature commit, push the neutral branch, open a ready
  PR, require the quota-conscious existing Linux-first three-allocation gate,
  audit exact head twice, and squash only after all required checks pass.
- Record integration through the bounded documentation-only PR, close the
  milestone through its no-workflow closeout PR, then delete temporary targets
  and all branches except `main`.
