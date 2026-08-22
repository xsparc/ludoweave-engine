# Current task

- **Task:** M96 - local-header extra-field consistency preflight
- **Status:** Implementation, full local qualification, and findings-first
  review are complete; exact-head hosted qualification and integration remain.
- **Base:** Verified M95 closeout squash
  `e770f5538660b5edea5fd8ebc4fccf717b18b272`, tree
  `0f8e47c61c1e93147f6ba19c813c836dea514962`.
- **Branch:** `release/m96-local-extra-consistency`.

## Accepted scope

- After M95 compression-method consistency, read the already bounded local name
  and extra lengths at each public `ZipInfo.header_offset + 26`.
- Read exactly the declared local extra bytes after the fixed 30-byte prefix and
  local name, then require equality with public central `ZipInfo.extra`.
- Raise stable content-silent error `sample bundle local header extra fields
  are inconsistent` before decoded-name policy, metadata, exact inventory,
  staging, or member reads.
- Preserve every established policy through M95, empty-archive inventory
  behavior, owned-resource cleanup, and caller snapshot position.
- Add RFC-0079 plus aligned public, security, architecture, release, roadmap,
  maintainer, test, and factual project records.
- Keep workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, and publication unchanged.

## Explicit non-scope

- No extra-field semantics parser, broad extra-field ban, new field-ID policy,
  nested-length/order/duplication/canonicalization rule, or claim that general
  ZIP producers must use identical local and central extra fields.
- No version/time/CRC/size or field-wide local/central comparison.
- No complete local-record or payload bound, next-header bound, gap, adjacency,
  contiguity, physical overlap rule, or inter-member layout validator.
- No archive repair, general archive sandbox, public release observation,
  workflow change, runtime feature, dependency, native/WASM work, tag, release,
  or publication.

## Direction and red evidence

- Clean M95 audit found exact local/remote closeout
  `e770f5538660b5edea5fd8ebc4fccf717b18b272`, only `main`, no open PR,
  release, tag, or M95 scratch target, valid three-squash DCO/signature chain,
  and exactly the two intended hosted runs.
- PKWARE APPNOTE 6.3.10 defines separate variable extra fields in corresponding
  local and central records. CPython exposes central bytes through public
  `ZipInfo.extra` and advances over local extra bytes without comparing them.
- A temporary valid-extra probe changed only the second local final byte from
  `feca02006f6b` to `feca02006f21`. Exact CPython 3.12.13, 3.13.13, and
  3.14.5 each retained both central extras as `feca02006f6b`, offsets
  `[0, 60]`, and read both payloads. The probe was format/Ruff clean.
- The first contract format check requested one mechanical reflow; Ruff and
  strict Pyright passed. After Ruff formatting, format, Ruff, and strict
  Pyright passed.
- The corrected 26-assertion M96 contract passed 16 supported-runtime behavior,
  inherited precedence, empty-archive, producer, and protected-surface
  controls. Ten stable-error, helper, cleanup, ordering, and documentation
  assertions failed because the M96 policy/RFC did not exist in unchanged M95.
  No complete pass is claimed from that red checkpoint.

## Remaining acceptance work

- Publish the locally qualified, independently reviewed, exact 16-path DCO
  feature commit through the existing quota-conscious three-
  allocation gate, two exact-head audits, guarded squash, bounded integration
  record, no-workflow closeout, and complete branch/generated-target cleanup.
