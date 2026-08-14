# Current Task

- **Task:** M87 - distinct local-header-offset preflight
- **Status:** Feature and integration records are verified and squash-
  integrated; exact three-record closeout is locally qualified for publication.
- **Base:** Verified M86 closeout squash
  `ba9464e59678766dd23953c1ea71acf010103903`, tree
  `eb75ce1a1ebc675dd5c9eb34fde5ffd8619587e1`.
- **Branch:** `release/m87-closeout`

## Accepted slice

- After every established policy through M86, require every parser-exposed
  `ZipInfo.header_offset` to be distinct.
- Reject two or more central entries that expose the same offset with stable
  content-silent error `sample bundle local header offsets are inconsistent`
  before M77 decoded-name policy, metadata, exact inventory, staging, or reads.
- Preserve empty/single-member admission, M84 entry-count and M86 first-offset
  precedence, every later failure category, and owned-resource close rules.
- Add RFC-0070 plus aligned public, security, architecture, release, roadmap,
  maintainer, and repository evidence records.
- Add no local-header parser, central-directory parser, offset ordering/bounds
  rule, inter-member layout validator, field-consistency validator, signature
  classifier, archive repair, workflow, dependency, lock, version, producer,
  runtime package/API, release authority, tag, release, or publication.

## Direction evidence

- PKWARE APPNOTE sections 4.3.2 and 4.3.6 require each stored file to have a
  preceding local header and a corresponding central header, then repeat the
  local-header/data sequence for each file.
- Exact installed CPython 3.12.13, 3.13.13, and 3.14.5 expose two central
  entries that point at one local header as offsets `[0, 0]`.
- On all three local Windows versions, reading the first entry succeeds with an
  overlap warning and reading the aliased second entry later raises a local/
  central filename mismatch. Hosted Linux omitted the warning. The fixed
  profile depends only on the public offsets and deferred read failure, not
  warning emission or CPython's private `_end_offset`.
- The fixed producer exposes 50 members and 50 distinct local-header offsets.

## Current evidence

- M86 feature PR #210 passed exact three-allocation hosted qualification and
  guarded squash integration. Documentation-only integration PR #211 used one
  48-second Linux allocation while the desktop umbrella skipped with zero
  steps. Three-record closeout PR #212 allocated no workflow and squash-merged
  as exact base `ba9464e59678766dd23953c1ea71acf010103903`. Exact synchronized
  `main` was the sole local/remote branch; no open PR, tag, release, postmerge
  run, disclosure marker, or M86 generated target remained before M87.
- Cross-version alias probes on CPython 3.12.13, 3.13.13, and 3.14.5 each
  exposed offsets `[0, 0]`, read the first payload with an overlap warning,
  and deferred the second-entry filename mismatch until member open.
- The new regression contract is format/Ruff clean and strict Pyright reports
  zero findings. Against unchanged M86 runtime/docs, its authoritative red
  run passes 6 behavior, precedence, empty/archive, producer, and protected-
  surface controls while 10 missing runtime, helper, ordering, cleanup, and
  documentation contracts fail in 0.42 seconds.
- The aggregate helper now runs immediately after M86. Combined M86-M87
  runtime/source/precedence coverage passes 32 cases; the sole remaining
  checkpoint failure was the deliberately absent RFC/public-document contract.
- RFC-0070 and aligned public records are present. The initial documentation-
  integrated gate passes all 33 combined M86-M87 assertions; affected format,
  Ruff, strict Pyright, strict docs, and whitespace gates are clean.
- The 16-case M87 contract passes on supported CPython 3.12.13, 3.13.13, and
  3.14.5. A concurrent first 3.12 invocation lost Hypothesis during pytest's
  terminal hook when parallel uv processes replaced the shared `.venv`; the
  isolated serial correction passes all 16 cases.
- Findings-first review corrected two stale project-record statements and found
  no runtime, test, or scope defect. The unchanged lock, all 330 Python files,
  Ruff, strict Pyright, 1,055 architecture assertions, exact 366-case M64-M87
  lineage, strict docs, and whitespace pass with one established Windows
  capability skip in each applicable architecture gate.
- Complete non-wgpu suites pass 2,585 tests with 15 established skips on each
  of CPython 3.12.13, 3.13.13, and 3.14.5. Ten real-wgpu tests, both one-repeat
  profiles, Clockwork Arena, and Agent World Builder pass after restoring the
  locked 45-package CPython 3.12 graphics environment.
- Two fresh builds reproduce a 275,673-byte wheel at
  `3659480bf9c924758529f34ce312f903a1bd652a5820284bfa11549fe9b428e7`
  and a 1,349,517-byte source archive at
  `936973c9dbf7dc0abd209705e35bccc4d2800a805128609ab65e3f5939d0a01b`.
  Installed-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass.
- Final local audit contains exactly 16 intended paths. CI, release workflow,
  producer, project metadata, and lock retain protected hashes; identity and
  credential scans are empty; the wheel exposes no backend/native object at
  its root; Git object checking reports no corruption.
- The record-inclusive rerun retains all 1,055 architecture assertions with one
  capability skip; all 330 files remain format/Ruff clean, strict Pyright and
  docs pass, and whitespace is clean.
- Precommit remote history verification resolves branch head, `main`,
  `origin/main`, and merge base to exact M86 closeout `ba9464e5967...`, with
  symmetric difference `0 0`; only `main` and the necessary neutral M87 branch
  exist, authentication is valid, and no open PR competes with publication.
- Initial ready PR #213 exact DCO head `769bcb04d3b60114b5c29ea31bce8a15e85471f0`
  reached 2,599 hosted Linux passes before one M87 test-only assertion failed:
  Linux did not emit the overlap warning seen by local Windows probes. The
  duplicate offsets, successful first read, and deferred second-read mismatch
  remained present. Desktop qualification stayed guarded. The correction drops
  only the incidental warning assertion and narrows RFC/architecture wording;
  production code and policy are unchanged.
- The corrected 16-case contract passes without warning dependence on CPython
  3.12.13, 3.13.13, and 3.14.5. All 330 files remain format/Ruff clean, strict
  Pyright and docs pass, all 1,055 architecture assertions pass with one
  established capability skip, whitespace is clean, and the corrected complete
  CPython 3.12 baseline passes 2,585 tests with 15 established skips.
- Corrected ready PR #213 exact DCO head
  `b98aa8365b6d3742c91871a820170d6b73330f25`, tree
  `2c4aff1985fa6e820a967323114ad6a3d73f9875`, passed run `31794063270`
  in exactly three Linux-first allocations. Linux passed in 7m16s, macOS in
  3m05s, and Windows in 3m52s. Linux CPython 3.12 passed 2,600 tests; Linux
  3.13/3.14 and both desktop 3.14 suites passed 2,600 with one capability skip.
  Each OS passed ten real-wgpu tests, its profile and both vertical slices.
- Hosted static/docs, byte-reproducible distribution, isolated-wheel, ten-
  artifact staging, and complete release smoke passed. The hosted wheel was
  275,661 bytes at
  `a0ef617c4ce29f59130155b143c457ceda740ba7950a2f1e01b4893f35ed2263`;
  the source archive was 1,352,531 bytes at
  `51d595e22e172cbdf74cddf7628db710d94a59c239edd4a90da34eeb40aa3fa3`.
- Two separated audits retained the exact base/head, three successful checks,
  `MERGEABLE/CLEAN`, DCO history, protected scope, and zero feedback. Guarded
  squash `dff483e120d607105120d8c004838e609540a14d` has the exact qualified
  tree, sole M86-closeout parent, standalone DCO, and valid GitHub signature.
  No postmerge run was allocated; feature branches were removed locally and
  remotely before this record branch.
- Integration-record scope is exactly four project records plus roadmap. The
  unchanged lock, all 330 files, Ruff, strict Pyright, 1,055 architecture
  assertions, strict docs, whitespace, protected hashes, identity/credential
  scans, and Git-object integrity pass with one established capability skip.
  A pre-record pair of fresh builds reproduces a 275,673-byte wheel at
  `3659480bf9c924758529f34ce312f903a1bd652a5820284bfa11549fe9b428e7`
  and a 1,353,993-byte source archive at
  `e58694e30441bc79b16d3842da647a95be2144015fd5bf4b5c28c2baa4bfc005`;
  installed-wheel, ten-artifact staging, and complete release smoke pass. The
  subsequent factual project-record lines differ only in the source archive;
  exact record-tree artifact evidence remains a hosted gate.
- Integration-record PR #214 exact DCO head
  `6a99381dbe9ce88c4912f0976d4503a86ab4493d`, tree
  `0b7b6f03d4ad7ce032d7fdb2b9aa43397bd47e2f`, passed run `31795436154`
  in one 45-second Linux allocation; the desktop umbrella skipped with zero
  steps. Hosted documentation architecture passed 1,056 assertions. Exact-head
  byte reproducibility, isolated-wheel, ten-artifact staging, and complete
  release smoke passed; the 275,661-byte wheel hash was
  `a0ef617c4ce29f59130155b143c457ceda740ba7950a2f1e01b4893f35ed2263`
  and the 1,354,599-byte source archive hash was
  `36b3ebff00339a36214830ac243ff0f64f34ec77ae71bdfffb57acdcf755821d`.
- Two separated integration-record audits retained exact scope, base/head,
  DCO, successful/skipped checks, `MERGEABLE/CLEAN`, and zero feedback. Squash
  `857633ad70e21c7c590dafd5c274263ac3184d37` has the exact record tree,
  sole feature-squash parent, standalone DCO, and valid GitHub signature at
  `2026-08-14T11:17:23Z`. No postmerge run was allocated; only synchronized
  `main` remained before this closeout branch.
- Closeout changes exactly the three project records. Metadata hygiene passes
  five assertions; whitespace and identity/credential scans are clean. No
  public, runtime, test, workflow, build, dependency, release, or generated
  surface is present.

## Remaining gates

1. Validate, publish, audit, and squash-integrate the exact three-record
   closeout without allocating CI.
2. Remove all M87 branches and generated targets and return to clean
   synchronized `main` before selecting M88.
