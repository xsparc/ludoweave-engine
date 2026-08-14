# Current Task

- **Task:** M89 - local-header-offset bounds preflight
- **Status:** Feature exact-head qualification, two readiness audits, and
  guarded squash integration are complete; factual integration records are
  active.
- **Base:** Verified M89 feature squash
  `61e5db38aef45a00788980227edf69663c82ce7b`, tree
  `0eba3e7b2407d08a6b030746bd73e7af57211b77`.
- **Branch:** `release/m89-integration-record`

## Accepted slice

- After every established policy through M88, require every parser-exposed
  `ZipInfo.header_offset` to be strictly before the conventional central-
  directory offset from the already-admitted final end record.
- Reject an offset at or after that boundary with stable content-silent error
  `sample bundle local header offsets are out of bounds` before decoded-name
  policy, metadata, exact inventory, staging, or reads.
- Preserve empty-archive admission, M84 entry-count, M85 placement, M86 first-
  offset, M87 distinctness, and M88 ordering precedence, every later failure
  category, snapshot-position restoration, and owned-resource close rules.
- Add RFC-0072 plus aligned public, security, architecture, release, roadmap,
  maintainer, and repository evidence records.
- Add no local-header parser, central-directory record parser, local-record
  extent or physical-contiguity rule, inter-member layout validator, archive
  repair, workflow, dependency, lock, version, producer, runtime package/API,
  release authority, tag, release, or publication.

## Direction evidence

- PKWARE APPNOTE 6.3.10 places the local-header/data sequence before the
  central-directory sequence and assigns each central record a relative local-
  header offset. Python documents `ZipInfo.header_offset` as the byte offset to
  the file header.
- A fixture that changes only the second central pointer exposes offsets
  `[0, 94]` where `94` is the conventional central-directory offset. Exact
  installed CPython 3.12.13, 3.13.13, and 3.14.5 each read the first payload and
  defer public `BadZipFile` until the malformed second member is read.
- The fixed 50-member producer exposes every local-header offset strictly
  before its conventional central directory.

## Current evidence

- M88 feature PR #216, integration-record PR #217, and closeout PR #218 are
  squash-integrated. Exact synchronized `main` is closeout
  `03f3723bf7365701c78a0fde072392b9f51da66b`; only `main` remained, with no
  open PR, tag, release, postmerge run, identity-control directory, or M88
  generated target before M89 selection. Git object checking found no
  corruption.
- All 35 combined M88-M89 behavior, precedence, cleanup, source-order, and
  documentation assertions pass on CPython 3.12. The affected Python files are
  format/Ruff clean, strict Pyright reports zero findings, and strict MkDocs
  builds with only the known upstream Material notice.
- Cross-version probes on CPython 3.12.13, 3.13.13, and 3.14.5 each exposed
  directory offset `94`, member offsets `[0, 94]`, readable first payload, and
  deferred `BadZipFile` on the second member.
- The new 18-case regression contract is format/Ruff clean and strict Pyright
  reports zero findings. Against unchanged M88 runtime/docs, its authoritative
  red run passes 9 standard-library behavior, established precedence, empty-
  archive, producer, and protected-surface controls while 9 missing runtime,
  helper, cleanup, source-order, and documentation contracts fail in 0.35
  seconds. No pass is claimed.
- The implemented 18-case contract passes on CPython 3.12.13, 3.13.13, and
  3.14.5. Complete suites pass 2,620 tests on every supported interpreter with
  15/16/16 established skips; 1,090 architecture assertions pass with one
  established Windows capability skip.
- All 332 Python files are format clean, Ruff passes, strict Pyright reports
  zero findings, and strict docs build with only the known upstream Material
  notice. The unchanged lock resolves 46 packages.
- All ten real-wgpu tests, both one-repeat profiles, Clockwork Arena, and Agent
  World Builder pass with their established deterministic identities.
- Two builds reproduce a 275,910-byte pure wheel at SHA-256
  `eca489c14cee629bf5f3403a78b3efc6670ffea56113b09981e6a34176bef0d4`
  and a 1,364,259-byte source archive at SHA-256
  `02e7801303a3465188750eedc95e2e957bb5d469b464a8da6b0a472c74b0d190`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Findings-first review found no defect. Exact scope is 16 intended paths;
  protected workflow, producer, metadata, and lock hashes remain unchanged;
  metadata hygiene, whitespace, credential scanning, package-content, and full
  Git-integrity checks are clean apart from expected squash-era unreachable
  objects.
- The final record-inclusive gate keeps all 332 Python files format/Ruff clean,
  strict Pyright at zero findings, architecture at 1,090 passed with one skip,
  strict docs green, and whitespace clean.
- After fetch/prune, branch head, `main`, `origin/main`, and merge base remain
  exact M88 closeout with symmetric difference `0 0`. Only `main` and the
  necessary neutral M89 branch exist; authentication is valid and open-PR,
  tag, and release queries are empty.
- Ready PR #219 exact DCO head
  `60559fd6ba5e3bc4583dc86c9b185f1175ac8f3d`, tree
  `0eba3e7b2407d08a6b030746bd73e7af57211b77`, passed exact three-allocation
  hosted run `31801893736`: Linux `94771566336` in 7m33s, macOS
  `94773345967` in 2m02s, and Windows `94773345983` in 4m12s.
- Hosted Linux passed 2,635 tests on every supported interpreter, with one
  capability skip on 3.13 and 3.14. macOS and Windows 3.14 each passed 2,635
  with one skip. Every OS passed ten real-wgpu tests, graphics profiling, and
  both vertical slices; Linux also passed the base profile and all distribution
  and release gates.
- Hosted builds reproduced a 275,896-byte pure wheel at SHA-256
  `22a14f43b4cdc2afaee7c4f39bc04e9baaebea557b070d3131fa8820a256c3ee`
  and a 1,365,606-byte source archive at SHA-256
  `6ae3d9d8f5e6190342ea0e588a6340cd2676e30da8a99fe2e2c07193452c09d5`.
- Two separated readiness audits retained exact head/tree/base, one standalone
  DCO commit, 16 paths, three successful checks, `MERGEABLE`/`CLEAN`, one
  hosted run, and zero comments, reviews, or review threads.
- Guarded squash `61e5db38aef45a00788980227edf69663c82ce7b` has sole
  parent exact M88 closeout, exact qualified tree, standalone DCO trailer, and
  valid GitHub signature at `2026-08-14T13:03:08Z`. The feature branch is
  deleted remotely and locally.
- The exact five-path integration record keeps all 332 Python files format/
  Ruff clean, strict Pyright at zero findings, architecture at 1,090 passed
  with one skip, strict docs green, and whitespace clean. Two builds reproduce
  the unchanged 275,910-byte local pure wheel and a 1,367,109-byte source
  archive at SHA-256
  `7081b7c9661fb27ff4046c85d2b891e61dfaa6252c31d57284a08c88fe831803`;
  wheel, staging, and complete release smoke pass.
- Its final record-inclusive repeat remains 332-file format/Ruff clean, strict
  Pyright zero, 1,090 architecture passes with one skip, strict docs green, and
  whitespace clean.
- The final metadata separator passed five assertions after one sandbox-only
  uv-cache denial. Fetch/prune leaves branch head, `main`, `origin/main`, and
  merge base at exact feature squash with divergence `0 0`; only `main` and the
  necessary integration-record branch exist, with no open PR, current-head
  postmerge run, tag, or release.

## Remaining acceptance

- Validate, publish, audit, and squash-integrate the exact factual integration
  record without allocating substantive desktop work.
- Publish and integrate the exact closeout record, clean all M89 generated
  targets and branches, and select the next bounded milestone.
