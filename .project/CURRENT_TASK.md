# Current Task

- **Task:** M87 - distinct local-header-offset preflight
- **Status:** Locally qualified after findings-first review; ready for exact-head
  publication and hosted validation.
- **Base:** Verified M86 closeout squash
  `ba9464e59678766dd23953c1ea71acf010103903`, tree
  `eb75ce1a1ebc675dd5c9eb34fde5ffd8619587e1`.
- **Branch:** `release/m87-distinct-local-header-offsets`

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
- On all three versions, reading the first entry succeeds with an overlapped-
  entry warning and reading the aliased second entry later raises a local/
  central filename mismatch. The fixed profile can reject the public offset
  alias before staging without relying on CPython's private `_end_offset`.
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

## Remaining gates

1. Publish, exact-head qualify, audit, squash-integrate, record, close out, and
   clean M87 before selecting the next bounded milestone.
