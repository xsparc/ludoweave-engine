# Current task

- **Task:** M102 - compressed-payload upper-bound preflight
- **Status:** M100 and M101 are fully locally validated in separate stacked DCO
  commits and remain unpushed because of the external reviewer-identity hold.
  M102 primary-source direction, deterministic supported-runtime probe,
  corrected deliberate red contract, runtime implementation, RFC-0085,
  aligned documentation, and the corrected implementation checkpoint are
  complete on a third local stacked branch. Supported-Python focused and full
  suites, repository-wide quality gate, graphics/profile/vertical slices, and
  initial reproducible distribution/release gate, and findings-first review
  record-inclusive artifact/release gate, final source separator, and stacked
  remote-history/scope/integrity audit, and final post-audit separator pass. The
  local DCO commit remains.
- **Base:** Fully locally validated M101 DCO commit
  `7b73861adc268182b6322e79c5a8651ca9c4db3d`, tree
  `b2c2348df504217315dd008d3eba083be8175c38`, with sole parent exact M100
  commit `103f84bf57f0b4ae0ca07548b453c199eec88f49`.
- **Branch:** `release/m102-compressed-payload-upper-bound`.

## Approved scope

- After M101 size-field consistency, private release smoke calculates each
  compressed payload end from the already bounded local-header envelope plus
  public central `ZipInfo.compress_size`.
- Each nonfinal payload end must be no greater than the next strictly ordered
  local-header offset; the final payload end must be no greater than the
  conventional central-directory offset.
- Overlap raises stable content-silent `sample bundle member payloads are out
  of bounds` before decoded-name policy, metadata, exact inventory, staging, or
  member reads.
- Every established policy through M101, empty-archive inventory behavior,
  owned-resource cleanup, and caller snapshot position remain intact.
- RFC-0085 and aligned public, security, architecture, release, roadmap,
  maintainer, test, and factual project records will define the boundary.
- Workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, and publication remain unchanged.

## Current evidence

- M101 commit `7b73861adc268182b6322e79c5a8651ca9c4db3d` is one commit
  ahead of M100 and two ahead of exact `origin/main`; it has the validated
  15-path tree, sole M100 parent, exact maintainer author/committer identity,
  and standalone DCO trailer. It is unpushed and has no hosted qualification
  claim.
- All 26 generated M101 scratch targets were verified under the exact workspace
  `.tmp` root, permanently removed in one approved pass, and confirmed absent.
  No tracked or recoverable file was removed.
- PKWARE APPNOTE defines local data immediately after each variable local-header
  envelope and the central directory after local records. Earlier milestones
  already provide bounded envelopes, ordered offsets, the conventional
  directory boundary, and matching compressed sizes.
- The first exact 3.12.13 runtime probe demonstrated payload byte 54 crossing
  the next header at byte 53, delayed first-member `BadZipFile`, and a readable
  second payload, while format passed; Ruff found one unused `noqa`. After that
  static-only correction, exact CPython 3.12.13, 3.13.13, and 3.14.5 reproduced
  central/local compressed sizes `[12, 11]`, the 54/53 overlap, delayed
  `BadZipFile`, and readable `payload-1`; the probe is format/Ruff clean.
- Initial M102 contract static checks passed strict Pyright but format requested
  one reflow and Ruff found one tuple-concatenation presentation issue. The
  13-assertion red run still passed five supported-runtime, M101-precedence,
  empty-archive, producer, and protected-surface controls and failed eight
  intended policy/helper/cleanup/ordering/documentation assertions. After the
  mechanical tuple and formatter corrections, the contract is format/Ruff
  clean, strict Pyright reports zero findings, and exact CPython 3.14.5 repeats
  the authoritative five-pass/eight-fail red result in 0.70 seconds. No
  complete pass is claimed.
- The first implementation checkpoint stopped when Ruff requested one
  mechanical runtime reflow. After formatting, affected-file format, Ruff, and
  strict Pyright checks passed, but the first focused command used a nonexistent
  abbreviated M101 path and collected no tests. The corrected exact path passed
  all 28 combined M101-M102 assertions in 0.36 seconds; strict docs built in
  1.45 seconds with only the known Material notice, and whitespace is clean.
- The first exact 3.12 focused invocation was blocked before pytest by sandbox
  denial of uv's user cache. With the existing cache authorized, all 13 M102
  assertions passed on exact CPython 3.12.13, 3.13.13, and 3.14.5 in 0.27,
  0.63, and 0.60 seconds. Each complete suite then passed 2,920 tests with 16
  established skips in 111.93, 102.87, and 107.01 seconds respectively.
- The unchanged lock resolves 46 packages and the exact CPython 3.12.13
  45-package graphics environment is restored. All 345 Python files are format
  clean; Ruff and strict Pyright pass; architecture passes 1,390 assertions
  with one established Windows capability skip; strict docs, 18 metadata/M102
  assertions, and whitespace pass.
- Ten real-wgpu tests, both one-repeat profiles, Clockwork Arena, and Agent
  World Builder pass with established deterministic identities. Two fresh
  builds reproduce a 276,141-byte wheel at
  `d44412d063b0cb85be358fad3849b29400fd75e08a3a4895c453840019749ae9`
  and a 1,460,394-byte source archive at
  `226fb991c517778c07f29a3d50fe35718303e820964a65bb010d9674683b113a`;
  isolated-wheel smoke, ten-artifact staging, and release smoke pass. Recording
  these facts changes the source archive afterward.
- Findings-first review found no actionable issue across exactly 15 intended
  paths. The runtime delta is one ordered call plus one position-restoring
  helper; M101 precedence, stable error, empty behavior, cleanup, exact/gap
  admission, and both overlap limits are covered. Protected workflows,
  producer, dependencies, package/API, metadata, and lock have no diff. The
  first credential scan command misparsed its leading-dash pattern; the
  corrected credential scan and identity/control-path scans found zero matches.
  The 94-entry pure wheel and 570-entry source archive contain zero native,
  WASM, bytecode, or retired control-metadata entries.
- Review-inclusive repeat builds reproduce the 276,141-byte pure wheel at
  `d44412d063b0cb85be358fad3849b29400fd75e08a3a4895c453840019749ae9`
  and a 1,462,149-byte source archive at
  `a53fb59806725ea2c1f9bd7c2b91ac89239bb11eeb362a4333e2c0a0447a435d`;
  isolated-wheel smoke, ten-artifact staging, and complete release smoke pass.
  Final factual record changes will alter only the source archive.
- The final separator's first sandboxed lock check was blocked before project
  evaluation by uv user-cache denial. The authorized lock check then resolved
  46 packages in 0.81 milliseconds; all 345 files remained format clean; Ruff
  and strict Pyright passed; architecture passed 1,390 assertions with one
  established skip; strict docs, all 18 metadata/M102 assertions, and
  whitespace passed.
- After fetch/prune, `HEAD` and the M101 branch are exact M101, M100 retains its
  exact commit, and local/remote `main` retain exact M99. Merge base is M99 and
  precommit divergence is the expected two local commits. Exactly 15 intended
  paths change; only the four necessary local stack branches and remote `main`
  exist. Authentication is valid; open PR, M102 workflow, release, and tag
  queries are empty. Exact DCO identity is configured, protected surfaces are
  unchanged, final scans are empty, Git reports 286 historical dangling-object
  lines and zero critical finding, and whitespace is clean.
- Final post-audit separator: strict docs built in 1.53 seconds; all 18
  metadata/M102 assertions passed in 0.43 seconds; credential, explicit
  service-identity, and retired-control scans remained empty; exactly 15 paths
  remained changed; and whitespace remained clean.

## Explicit non-scope

- No decompression or recompression and no payload-content read during
  preflight.
- No exact-contiguity requirement, no gap or adjacency ban, and no physical
  payload-byte inspection.
- No compression-ratio or archive-bomb policy and no payload-integrity
  certification.
- No generic field-wide comparison, archive repair, general archive sandbox,
  public release observation, workflow change, dependency, runtime feature,
  native/WASM work, tag, release, or publication.

## Remaining acceptance work

- Create one standalone local DCO commit stacked on M101.
- Publish M100-M102 ready PRs only after the automated-review identity exposure
  is resolved or the maintainer explicitly accepts that disclosure risk.
