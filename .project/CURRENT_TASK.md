# Current task

- **Task:** M105 - zero sample-member general-purpose-flag profile preflight
- **Status:** Direction evidence, exact supported-runtime reproduction,
  deliberate red contract, runtime implementation, RFC-0088, aligned public
  documentation, supported-runtime/full/static/graphics/release qualification,
  diagnostic-order correction, findings-first review, reproducible artifacts,
  and final source/history audit are complete locally. The standalone DCO
  commit is next.
- **Base:** Fully locally validated M104 DCO commit
  `3c734d627c90cd9071350d5b4863711a6ba3113e`, tree
  `2b99704ee9639854af0fe6f2ee4875db527246ad`, with sole parent exact M103
  commit `19ccf5076d391924e969b57e76c25049068553a6`.
- **Branch:** `release/m105-zero-flag-profile`.

## Approved scope

- After established specific-flag, local/central consistency, local-record,
  payload-layout, and M104 extra-field checks, require every parsed member's
  public central `ZipInfo.flag_bits` to equal zero.
- Raise stable content-silent `sample bundle contains unsupported general-
  purpose flags` after decoded-name/member-metadata policy and before exact
  inventory, staging, or member reads.
- Preserve precise encryption, data-descriptor, enhanced-deflate, compressed-
  patch, local-flag consistency, payload-layout, M104, empty-inventory, current-
  producer, and owned-resource behavior.
- Add RFC-0088, one focused architecture contract, and aligned public,
  security, architecture, release, roadmap, maintainer, and factual project
  records.
- Keep workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, publication, and public branch state unchanged.

## Current evidence

- M104 is one clean standalone local DCO commit at
  `3c734d627c90cd9071350d5b4863711a6ba3113e`, tree
  `2b99704ee9639854af0fe6f2ee4875db527246ad`, with sole parent exact M103.
  It remains unpushed and has no hosted qualification claim.
- M104 cleanup targeted 28 ignored scratch paths whose immediately preceding
  read-only audit showed exact direct `.tmp` children with no reparse points.
  The removal command emitted non-terminating `DirectoryName` validation
  errors for directory entries, so its internal parent guard is not claimed as
  successful. It nevertheless reported `removed=28; remaining=0`; a separate
  follow-up confirmed zero targets and a clean tracked worktree.
- PKWARE defines legitimate nonzero general-purpose flags and currently leaves
  bits 7-10 unused. CPython exposes public central `ZipInfo.flag_bits` and
  selectively interprets known bits. The selected policy is explicitly a
  fixed-producer zero profile, not a general ZIP validity or safety claim.
- The format-clean ignored probe on exact CPython 3.12.13, 3.13.13, and 3.14.5
  preserved matching unused bit 7 as value `128`, read `first` and `second`,
  and confirmed the fixed producer emits 50 members with sole flag value zero.
  Initial Ruff found one surplus blank line; the corrected probe passes Ruff.
- The first deliberate-red run used a nested pytest base whose parent did not
  exist, so 13 setup errors make that run unusable as contract evidence. The
  corrected red run passed 11 established-boundary assertions and failed five
  targeted stable-error, cleanup, helper/order, and documentation assertions
  in 0.30 seconds against exact M104. No complete pass is claimed from either
  red run.
- The implementation is one post-M104 ordered call and one aggregate public-
  metadata zero classifier. It performs no flag-semantics parsing, raw record
  parsing, or payload-content read.
- Affected formatting and Ruff pass; strict Pyright reports zero findings; all
  16 focused assertions pass in 0.23 seconds; strict docs build in 1.47 seconds
  with only the known upstream Material notice; and whitespace passes.
- The first complete exact 3.12.13 suite exposed three established diagnostic-
  precedence regressions and exited 1 after 2,959 passes and 16 skips in 102.51
  seconds. The zero classifier moved after decoded-name/member-metadata policy;
  two focused LZMA/UTF-8 regressions and the M76 stored-bit supersession were
  added. All 64 relevant M64/M65/M76/M105 assertions, strict Pyright, affected
  Ruff, strict docs, and whitespace then pass.
- All 18 final focused M105 assertions pass on exact CPython 3.12.13, 3.13.13,
  and 3.14.5 in 0.60, 0.59, and 0.58 seconds. The corrected complete suites each
  pass 2,964 tests with 16 established skips in 100.89, 98.09, and 103.75
  seconds.
- The unchanged 46-package lock resolves in 0.80 milliseconds and the exact
  CPython 3.12.13 locked all-groups graphics environment installs 45 packages.
  All 348 Python files are format clean; Ruff and strict Pyright pass; all 1,434
  architecture assertions pass with one established Windows capability skip in
  9.32 seconds; strict docs build in 1.47 seconds; all 23 metadata/M105
  assertions pass in 0.44 seconds; and whitespace passes.
- All ten real-wgpu integration tests pass in 6.06 seconds. One-repeat base and
  graphics profiles validate with two and three workloads. Clockwork Arena and
  Agent World Builder reproduce their established state, capture, replay,
  render, query, and registered-test identities.
- Two fresh builds reproduce a 276,588-byte pure wheel at
  `07fb9037775621176dfd1736ba5bdb8b3c2ff063a1a10d714d40cc5d0147324e`
  and a 1,478,156-byte source archive at
  `54467dd8c6ea402ea134355350532235762091440541fc9d6cdcf50007caadc8`.
  Isolated-wheel smoke, ten-artifact staging, and complete release smoke pass.
  The 94-entry wheel and 576-entry source archive contain no native, WASM,
  bytecode, or retired control-metadata paths. Recording these facts changes
  the source archive afterward.
- Findings-first review covers 17 intended paths. It retained the diagnostic-
  order correction, clarified RFC/public placement and M76 supersession, and
  found no remaining actionable code, test, security, architecture, or
  documentation issue. The runtime diff is one ordered call plus one aggregate
  public central-flag classifier; the existing M76 regression is the only
  previously tracked test changed. Protected workflows, release stager,
  metadata, lock, runtime package/API, dependencies, producer, version, and
  release authority have no diff. Credential, explicit service-identity,
  backend/native, wall-clock, and retired-control scans return zero matches.
- Review-inclusive repeat builds reproduce the 276,588-byte pure wheel at
  `dd2fae65bab55e8ed87beb89028b37150b90e617099ce4ab2240c667b348a474`
  and a 1,479,641-byte source archive at
  `0596b0f5b55a4fadc3bd116f33485f87a6c6db98c92ae08ceed085b2a82cead6`;
  isolated-wheel smoke, ten-artifact staging, and complete release smoke pass.
  The 94-entry wheel and 576-entry source archive remain free of native, WASM,
  bytecode, and retired control-metadata paths. Final factual record changes
  alter the source archive afterward.
- Final source separator: the unchanged 46-package lock resolves in 0.82
  milliseconds; all 348 Python files remain format clean; Ruff and strict
  Pyright pass; all 1,434 architecture assertions pass with one established
  Windows capability skip in 8.64 seconds; strict docs build in 1.42 seconds;
  all 23 metadata/M105 assertions pass in 0.42 seconds; and whitespace passes.
- Precommit stacked-history audit: the first multi-ref command contained one
  mistyped M102 branch name and its ref result is not used. The corrected
  labeled audit establishes `HEAD`/M104 at exact
  `3c734d627c90cd9071350d5b4863711a6ba3113e`, M100-M103 at their retained
  exact commits, local/remote `main` and merge base at M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, and divergence `0 5`.
  Exactly 17 intended paths change; only `main` and required M100-M105 local
  branches exist, while only `origin/main` exists remotely. Exact DCO identity
  is configured. Authentication is valid; open PR, M105 run, release, and tag
  queries are empty. Protected hashes remain exact; Git checking reports 287
  dangling-only lines and zero critical finding; and whitespace is clean.
- Final post-audit separator: strict docs build in 1.44 seconds with only the
  known upstream Material notice; all 23 metadata/M105 assertions pass in 0.42
  seconds; high-confidence credential, explicit service-identity, runtime
  backend/native/wall-clock, and retired-control scans return zero matches;
  exactly 17 intended paths remain changed; and whitespace remains clean.

## Explicit non-scope

- No flag-semantics parser, compression-option interpreter, bit registry,
  general ZIP allowlist, raw local/central parser, or general ZIP validity or
  safety claim.
- No decompression, recompression, payload-content read, CRC recomputation,
  repair, archive-bomb policy, or payload-integrity certification.
- No workflow, allocation, dependency, producer, runtime package/API, native/
  WASM, version, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Create one standalone local DCO commit stacked on M104, verify identity,
  parent, tree, trailer, and scope, then remove only verified M105 scratch
  targets.
- Publish ready stacked milestones only after the automated-review identity
  exposure is resolved or the maintainer explicitly accepts that disclosure
  risk.
