# Current task

- **Task:** M106 - zero sample-member extraction-version reserved-byte profile
  preflight.
- **Status:** Direction research, exact supported-runtime/producer probe,
  deliberate red, runtime implementation, RFC-0089, aligned documentation, and
  full local qualification are complete. Findings-first review corrected one
  documentation-contract omission; review-inclusive artifacts, final source,
  and history/integrity audits pass. The standalone DCO commit is next.
- **Base:** Fully locally validated M105 DCO commit
  `6155e125968c92dfbae44da6c6f13f9684f11fcd`, tree
  `ae77b746a5ed9491da14aa2f6ad69f0663e92bfd`, with sole parent exact M104
  `3c734d627c90cd9071350d5b4863711a6ba3113e`.
- **Branch:** `release/m106-zero-reserved-byte-profile`.

## Approved scope

- After M97 local/central extraction-version-pair equality and established
  payload-layout, extra-field, member-metadata, and M105 flag-profile checks,
  require every public central `ZipInfo.reserved` value to equal zero.
- Raise stable content-silent `sample bundle has a nonzero extraction-version
  reserved byte` before exact inventory, staging, or member reads.
- Preserve precise local mismatch, layout, extra-field, codec, path, flag,
  empty-inventory, producer, and owned-resource behavior.
- Add RFC-0089, one focused architecture contract, and aligned public,
  security, architecture, release, roadmap, maintainer, and factual project
  records.
- Keep workflow, runner allocation, action, permission, credential,
  dependency/lock/version, producer, runtime package/API, release authority,
  tag, release, publication, and public branch state unchanged.

## Current evidence

- Official Python 3.14 documentation says `ZipInfo.reserved` must be zero;
  CPython initializes and serializes it as zero; PKWARE defines its enclosing
  two-byte version-needed-to-extract field. The response is one fixed-producer
  zero classifier, not general extraction-version semantics or ZIP security.
- An initial sandboxed three-runtime probe could not read uv's external cache
  and exited 1 on each invocation. The approved rerun on exact CPython 3.12.13,
  3.13.13, and 3.14.5 exposed matching local/central pairs `(20, 1)`, read both
  payloads, and found all 50 fixed-producer reserved values equal zero.
- The deliberate-red CPython 3.12.13 regression exited 1 with one intended
  failure in 0.22 seconds: the unchanged verifier reached exact inventory
  rather than rejecting the matching nonzero byte.
- The implementation is one post-M105 ordered call plus one aggregate
  `info.reserved != 0` classifier. It reads no payload and uses no private ZIP
  API. The first 15-assertion CPython 3.12.13 checkpoint passes in 0.25 seconds.
- All 15 focused assertions pass on exact CPython 3.12.13, 3.13.13, and 3.14.5
  in 0.25, 0.65, and 0.62 seconds. Complete suites pass 2,989/15 skipped,
  2,979/16 skipped, and 2,979/16 skipped in 114.15, 101.92, and 107.77
  seconds; the 3.12 environment included ten optional graphics tests.
- The first grouped static checkpoint ran after the 3.14 focused environment
  replacement and Pyright reported 17 missing/unknown optional-wgpu diagnostics;
  formatting, Ruff, docs, and whitespace passed. Restoring the exact locked
  CPython 3.12.13 graphics environment made strict Pyright pass with zero
  diagnostics. The complete corrected gate has 349 format-clean files, clean
  Ruff/Pyright, 1,449 architecture passes with one skip, strict docs, 20
  metadata/M106 passes, and clean whitespace.
- All ten real-wgpu tests pass in 5.87 seconds; one-repeat two-workload base and
  three-workload graphics profiles validate; Clockwork Arena and Agent World
  Builder reproduce their established deterministic identities.
- Two builds reproduce a 276,680-byte pure wheel at
  `613d1d72ea8583f03dfc7ecb941d40df23522a19b877ee1fcbf5ab908db9216e`
  and a 1,483,265-byte source archive at
  `596219c8ed041afd918a488a6a574379da23b7ce6ee5b4d2f0715a4110a7eca2`.
  Isolated-wheel smoke, ten-artifact staging, and complete release smoke pass;
  the 94-entry wheel and 578-entry source archive contain no native, WASM,
  bytecode, or retired control-metadata paths. Later factual record changes
  will alter only the source archive.
- Findings-first review covers exactly 16 intended paths. It found no runtime,
  security, architecture, diagnostic-order, ownership, or scope defect. It
  tightened the documentation contract to require every listed file and include
  the changed roadmap; affected Ruff/Pyright, all 20 metadata/M106 assertions,
  strict docs, and whitespace pass. Protected workflows, stager, metadata,
  lock, runtime package/API, dependencies, producer, version, and release
  authority have no diff. Explicit service-identity and high-confidence secret
  scans return zero matches.
- Review-inclusive builds reproduce the same 276,680-byte pure wheel at
  `613d1d72ea8583f03dfc7ecb941d40df23522a19b877ee1fcbf5ab908db9216e`
  and a 1,485,135-byte source archive at
  `ba60a0813bfc32a75184a43275ea84d8f89d3be98d7839014ee567f0a2c8e786`;
  isolated-wheel smoke, ten-artifact staging, and complete release smoke pass.
  The 94/578-entry inventories remain free of native, WASM, bytecode, and
  retired control-metadata paths. Final factual records alter the source archive
  afterward.
- Final source separator: the unchanged 46-package lock resolves in 0.86
  milliseconds; all 349 files remain format clean; Ruff and strict Pyright
  pass; all 1,449 architecture assertions pass with one established skip in
  8.75 seconds; strict docs build in 1.48 seconds; all 20 metadata/M106
  assertions pass in 0.81 seconds; and whitespace passes.
- Precommit audit: an initial branch-ref command mistyped the M104 and M102
  branch names, so its two affected fields are discarded. The fully corrected
  audit establishes the exact M100-M105 stack, local/remote M99 main and merge
  base, and expected `0 6` divergence. Exactly 16 intended paths change; only
  main and required M100-M106 local branches exist, while only `origin/main`
  exists remotely. Exact DCO identity is configured. Authentication is valid;
  open PR, M106 run, release, and tag queries are empty. Git checking reports
  287 dangling-only lines and zero critical finding. Final runtime backend/
  native/wall-clock, explicit service-identity, high-confidence secret, and
  protected-surface scans return zero findings.
- Final post-audit separator: strict docs build in 1.49 seconds; all 20
  metadata/M106 assertions pass in 0.40 seconds; exactly 16 intended paths
  remain; explicit service-identity and high-confidence secret scans return
  zero matches; and whitespace remains clean.
- M105 postcommit cleanup removed exactly 17 pre-audited ignored, direct,
  non-reparse `.tmp` children and independently confirmed zero remaining
  targets and a clean worktree.
- Publication remains held because a public no-finding automated review on the
  M99 closeout exposed the configured review service's identity. No ready local
  stacked milestone will be pushed until the risk is resolved or explicitly
  accepted.

## Explicit non-scope

- No extraction-version semantics parser, supported-version allowlist,
  capability rule, raw record parser, or general ZIP validity/security claim.
- No decompression, recompression, payload-content read, CRC recomputation,
  repair, archive-bomb policy, or payload-integrity certification.
- No workflow, allocation, dependency, producer, runtime package/API, native/
  WASM, version, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Create one standalone local DCO commit, verify identity/parent/tree/trailer/
  scope, and remove only verified M106 scratch targets.
