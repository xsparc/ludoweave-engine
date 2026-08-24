# Current task

- **Task:** M107 - exact sample-member extraction-version profile preflight.
- **Status:** Direction research, exact supported-runtime/producer probe,
  deliberate red, runtime implementation, RFC-0090, aligned documentation, and
  complete qualification, findings-first review, and review-inclusive artifact
  verification are complete. Final source/history separators and the local DCO
  commit remain.
- **Base:** Fully locally validated M106 DCO commit
  `630f794cd1e3609f9e0b20d2f7f16e4d1fb27ef5`, tree
  `708753da831b9a3942affa128f4ac9dc4fb6dbca`, with sole parent exact M105
  `6155e125968c92dfbae44da6c6f13f9684f11fcd`.
- **Branch:** `release/m107-extraction-version-profile`.

## Approved scope

- After M97 local/central extraction-version-pair equality and established
  payload-layout, extra-field, member-metadata, M105 flag, and M106 reserved-
  byte checks, require every public central `ZipInfo.extract_version` value to
  equal `20`.
- Raise stable content-silent `sample bundle has an unsupported extraction
  version` before exact inventory, staging, or member reads.
- Preserve precise local mismatch, layout, extra-field, codec, path, flag,
  reserved-byte, empty-inventory, producer, and owned-resource behavior.
- Add RFC-0090, one focused architecture contract, and aligned public,
  security, architecture, release, roadmap, maintainer, and factual project
  records.
- Keep workflow, runner allocation, action, permission, credential,
  dependency/lock/version, producer, runtime package/API, release authority,
  tag, release, publication, and public branch state unchanged.

## Current evidence

- PKWARE assigns extraction version 2.0 to Deflate; Python exposes public
  `ZipInfo.extract_version`; CPython uses default value `20` and recognizes
  features through 6.3. The response is one fixed-producer exact classifier,
  not a general capability parser or universal ZIP rule.
- The ignored probe first required one mechanical Ruff-format reflow, then
  passed Ruff. Exact CPython 3.12.13, 3.13.13, and 3.14.5 exposed matching
  local/central `(21, 0)` pairs, read both payloads, and found all 50 fixed-
  producer pairs equal `(20, 0)`.
- The deliberate-red exact CPython 3.12.13 contract passed 11 established
  behavior/protected-surface assertions and failed nine targeted stable-error,
  cleanup, exact-value, helper/order, and documentation assertions in 0.37
  seconds against unchanged M106.
- The implementation is one post-M106 ordered call plus one aggregate
  `info.extract_version != 20` classifier. It reads no payload and uses no
  private ZIP API.
- The first implementation checkpoint passed 19 assertions but failed the docs
  contract because line wrapping split the exact classifier phrase. RFC-0090
  was reflowed; all 20 focused assertions then pass on exact CPython 3.12.13 in
  0.25 seconds, strict docs build in 1.44 seconds, and whitespace passes.
- All 20 focused assertions pass on exact CPython 3.12.13, 3.13.13, and 3.14.5
  in 0.25, 0.63, and 0.62 seconds. Complete suites pass 3,009/15 skipped,
  2,999/16 skipped, and 2,999/16 skipped in 106.98, 102.12, and 108.06
  seconds; the 3.12 environment included the optional graphics tests.
- The unchanged 46-package lock resolves in 0.78 milliseconds and the exact
  locked CPython 3.12.13 graphics environment installs 45 packages. All 350
  files are format clean; Ruff and strict Pyright pass; all 1,469 architecture
  assertions pass with one established skip in 9.47 seconds; strict docs build
  in 1.58 seconds; all 25 metadata/M107 assertions pass in 0.82 seconds; and
  whitespace passes.
- All ten real-wgpu tests pass in 6.66 seconds; one-repeat two-workload base and
  three-workload graphics profiles validate; Clockwork Arena and Agent World
  Builder reproduce their established deterministic identities.
- Two builds reproduce a 276,812-byte pure wheel at
  `aa46f3ab81e92efc04e04655323eb97f553c077eb5ccb77472aee4cde9657a3c`
  and a 1,488,822-byte source archive at
  `0edc1ecc0980f506fd830d644aa8f228f43ad94f5575ac3f54ffe0f2c12ab6db`.
  Isolated-wheel smoke, ten-artifact staging, and complete release smoke pass;
  the 94-entry wheel and 580-entry source archive contain no native, WASM,
  bytecode, or retired control-metadata paths. Later factual record changes
  alter only the source archive.
- Findings-first review covers exactly 16 intended paths and found no runtime,
  security, architecture, diagnostic-order, ownership, documentation, or scope
  defect. Protected workflows, stager, metadata, lock, runtime package/API,
  dependencies, producer, version, and release authority have no diff. Narrow
  service-identity and high-confidence secret scans return zero matches.
- Review-inclusive builds reproduce the same 276,812-byte pure wheel at
  `aa46f3ab81e92efc04e04655323eb97f553c077eb5ccb77472aee4cde9657a3c`
  and a 1,489,494-byte source archive at
  `c65fc7ec2130bed55168e9d4aaa3f8d12724c47881c63ae3f3f2ab3fff3e20b6`.
  Isolated-wheel smoke, ten-artifact staging, complete release smoke, and
  94/580-entry native/WASM/bytecode/retired-metadata hygiene pass. Final factual
  records alter the source archive afterward.
- Final source separator: the unchanged lock resolves 46 packages in 0.87
  milliseconds after an approved rerun of a sandbox-only cache denial; all 350
  files remain format clean; Ruff and strict Pyright pass; all 1,469
  architecture assertions pass with one established skip in 9.69 seconds;
  strict docs build in 1.53 seconds; all 25 metadata/M107 assertions pass in
  0.82 seconds; and whitespace passes.
- Corrected precommit audit establishes exact M100-M106 ancestry, M106 head and
  tree, local/remote M99 main and merge base, and expected `0 7` divergence.
  Exactly 16 intended paths change; only main and required M100-M107 local
  branches exist, while only `origin/main` exists remotely. Exact DCO identity
  is configured. Authentication is valid; approved read-only reruns report no
  open PR, M107 run, release, or tag. Git checking reports 44 dangling-only
  objects and zero defect. The earlier unquoted tree-expression field and
  dangling-as-critical classifier are discarded.
- Post-audit records pass strict docs in 1.56 seconds and all 25 metadata/M107
  assertions in 0.42 seconds. Exactly 16 paths remain, protected hashes and
  zero protected diff are unchanged, narrow service-identity and corrected
  boundary-aware secret scans return zero, and whitespace passes. An initial
  unbounded `sk-` pattern matched six established `task-directed` product-test
  strings; those false positives are discarded.
- M106 is exact commit `630f794cd1e3609f9e0b20d2f7f16e4d1fb27ef5`,
  tree `708753da831b9a3942affa128f4ac9dc4fb6dbca`, with sole parent
  M105, exact maintainer identity, one DCO trailer, and 16 intended paths.
- M106 postcommit cleanup removed exactly ten pre-audited ignored, direct,
  non-reparse `.tmp` children and independently confirmed zero remaining
  targets and a clean worktree.
- Publication remains held because a public no-finding automated review on the
  M99 closeout exposed the configured review service's identity. No ready local
  stacked milestone will be pushed until the risk is resolved or explicitly
  accepted.

## Explicit non-scope

- No general extraction-version semantics parser, supported-version range,
  feature/capability evaluator, raw record parser, or general ZIP validity/
  security claim.
- No decompression, recompression, payload-content read, CRC recomputation,
  repair, archive-bomb policy, or payload-integrity certification.
- No workflow, allocation, dependency, producer, runtime package/API, native/
  WASM, version, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Create one standalone local DCO commit, verify identity/parent/tree/trailer/
  scope, and remove only verified M107 scratch targets.
