# Current Task

- **Task:** M88 - local-header-order preflight
- **Status:** Runtime, regression contract, RFC, and aligned public records are
  implemented; supported-version and complete qualification are active.
- **Base:** Verified M87 closeout squash
  `aba849aceec15342141a29fc105b85720a5e48ba`, tree
  `d61bce3093e6a497bc40ff57f34dbca957f9a4de`.
- **Branch:** `release/m88-local-header-order`

## Accepted slice

- After every established policy through M87, require parser-exposed members to
  have strictly increasing `ZipInfo.header_offset` values.
- Reject central-directory order that disagrees with physical local-header
  order using stable content-silent error `sample bundle local header offsets
  are out of order` before decoded-name policy, metadata, exact inventory,
  staging, or reads.
- Preserve empty/single-member admission, M84 entry-count, M86 first-offset,
  and M87 distinct-offset precedence, every later failure category, and owned-
  resource close rules.
- Add RFC-0071 plus aligned public, security, architecture, release, roadmap,
  maintainer, and repository evidence records.
- Add no local-header parser, central-directory record parser, bounds or
  physical-contiguity rule, inter-member layout validator, archive repair,
  workflow, dependency, lock, version, producer, runtime package/API, release
  authority, tag, release, or publication.

## Direction evidence

- PKWARE APPNOTE 6.3.10 permits arbitrary file ordering generally and depicts
  corresponding local/data and central records. Python documents that
  `ZipFile.infolist()` returns entries in their actual archive order.
- A fixture that swaps only two central-directory records preserves both local
  records and payloads. Exact installed CPython 3.12.13, 3.13.13, and 3.14.5
  each expose names `second.txt`, `first.txt`, offsets `[46, 0]`, and readable
  payloads `second`, `first` in reordered central-directory order.
- This is a fixed LudoWeave producer-profile rule, not a claim that such ZIP
  archives are invalid generally. The producer exposes 50 strictly increasing
  offsets.

## Current evidence

- M87 feature PR #213, integration-record PR #214, and closeout PR #215 are
  squash-integrated. Exact synchronized `main` is closeout
  `aba849aceec15342141a29fc105b85720a5e48ba`; only `main` remained, with no
  open PR, tag, release, postmerge run, disclosure marker, or M87 generated
  target before M88 selection.
- The new 17-case regression contract is format/Ruff clean and strict Pyright
  reports zero findings. Against unchanged M87 runtime/docs, its authoritative
  red run passed 7 controls while 10 missing implementation and documentation
  contracts failed in 0.29 seconds. No pass is claimed.
- The new aggregate ordering helper runs immediately after M87 distinctness.
  All 33 combined M87-M88 runtime, precedence, cleanup, source-order, producer,
  protected-surface, and documentation assertions pass in 0.42 seconds.
- Affected formatting and Ruff checks pass, strict Pyright reports zero
  findings, and strict documentation builds in 1.56 seconds with only the known
  upstream Material notice.
- The 17-case M88 contract passes on installed CPython 3.12.13 in 0.29 seconds,
  3.13.13 in 1.37 seconds, and 3.14.5 in 1.69 seconds.
- Findings-first review found no runtime, test, documentation, or scope defect.
  The rule remains one public-parser aggregate check with established
  precedence, content-silent failure, and owned cleanup.
- The unchanged lock resolves 46 packages. All 331 Python files are format/Ruff
  clean, strict Pyright reports zero findings, all 1,072 architecture
  assertions pass with one established Windows capability skip, strict docs
  and whitespace pass, and protected workflow/producer/metadata/lock hashes are
  unchanged.
- Complete non-wgpu suites pass 2,602 tests with 15 established skips on each
  of CPython 3.12.13, 3.13.13, and 3.14.5.
- After restoring the locked 45-package CPython 3.12 graphics environment, all
  ten real-wgpu tests, both one-repeat profiles, Clockwork Arena, and Agent
  World Builder pass with their established deterministic identities.
- Two fresh builds reproduce a 275,794-byte pure wheel SHA-256
  `982da69788bbb475c58e73f6b4b09f1f424ebd064693a5923cfee07613152f9c`
  and 1,358,324-byte source archive SHA-256
  `7c05d0b4832d30be3186baeca5c897c44b3dab3cc9de0837a02a3e4d88c98cda`.
  Installed-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass.
- Final local audit contains exactly 16 intended paths. CI, release workflow,
  sample producer, project metadata, and lock retain protected hashes; added-
  content identity and credential scans are empty; the 94-entry wheel and 542-
  entry source archive contain no native/WASM/bytecode or retired control
  metadata; Git object checking reports no corruption.
- After fetch/prune, branch head, `main`, `origin/main`, and merge base remain
  exact M87 closeout `aba849aceec15342141a29fc105b85720a5e48ba` with symmetric
  difference `0 0`. Only `main` and the necessary neutral M88 branch exist,
  GitHub authentication is valid, and no open PR competes with publication.

## Remaining acceptance

- Publish one ready feature PR, qualify its exact head through the existing
  quota-conscious hosted topology, perform two separated clean readiness
  audits, and squash-integrate only the exact qualified tree.
- Publish and integrate factual project-record and closeout PRs, clean all M88
  branches/generated targets, and select the next bounded milestone.
