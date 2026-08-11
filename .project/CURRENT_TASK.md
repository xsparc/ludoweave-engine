# Current Task

- **Task:** M61 - public release candidate/output-root separation
- **Status:** Feature and factual integration record are hosted-qualified,
  reviewed, and squash-integrated; three-file closeout is in progress on
  `records/m61-closeout`.
- **Started:** 2026-08-11
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M60 closeout
  `a8fc787a7b04b4fe8ed3766167e58258aa62c8d6`, whose tree
  `784bf3b82a3dfd51842edad622b3ae1dc0b78ea5` exactly matches the reviewed
  closeout head. GitHub reports a valid signature and parsed DCO trailer; only
  `main` existed locally/remotely, with no open pull request or closeout run.
- **Outcome:** Keep the admitted candidate directory read-only by rejecting a
  runner-owned output root that is the same directory or a resolved descendant
  before public network or validator side effects.
- **Acceptance:** Resolve both validated directories strictly and content-
  silently, use the resolved directories for later work, reject equality and
  candidate-containing-output relationships with stable
  `public_release.path_overlap`, and retain a separate candidate child of the
  output root as valid. Resolved parent aliases and filesystem-identity aliases
  whose spelling differs on a case-insensitive filesystem receive the same
  decision.
- **Boundary:** No race-free filesystem claim, directory-descriptor sandbox,
  general path sandbox, rollback, cleanup, retry, workflow, runner-allocation,
  dependency, lock, version, runtime package/API, release authority, tag,
  release, publication, or real public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Development evidence:** Against unchanged production code, the initial
  eight-assertion M61 file failed six cases and passed two. All five unsafe or
  inspection cases reached an intentionally forbidden download path; the
  documentation contract named the intentionally absent RFC. The safe sibling
  layout and protected-surface guard passed. After the focused implementation,
  all seven non-documentation assertions pass in 0.21 seconds; both changed
  Python files are format/Ruff clean and strict Pyright reports zero findings.
  The explicit documentation wording correction brings the complete M61 file
  to eight passing assertions in 0.20 seconds, and the corrected inherited
  M45-M61/release-draft group passes 346 tests with two platform-capability
  skips in 7.56 seconds. Whole-tree lock/static/docs and 656 architecture
  assertions pass. Complete graphics-enabled CPython 3.12-3.14 suites each
  pass 2,196 tests with 14 expected skips. Ten real-wgpu tests, both five-
  repeat profiles, both vertical slices, and all M1-M4 benchmark validators
  pass; timing target misses remain recorded facts rather than pass claims.
  Two pre-record builds reproduce a pure wheel and source distribution;
  isolated-wheel and complete release smoke pass. The two added resolver proof
  points bring the final focused M61 group to 11 passing assertions with
  format/Ruff/Pyright clean. The evidence-inclusive candidate passes the
  unchanged lock, 304-file formatting, Ruff, strict Pyright, 659 architecture
  assertions, strict docs, and 2,199 CPython 3.12 tests with 14 expected skips;
  all 11 final M61 assertions also pass on CPython 3.13 and 3.14. The first
  review audit found that resolved path equality alone did not promise
  canonical spelling on a case-insensitive POSIX filesystem. Both new identity-
  alias and identity-inspection regressions failed against the hosted head by
  reaching the forbidden download, while the expanded documentation contract
  also failed. After filesystem-identity ancestry comparison and aligned docs,
  all 13 M61 assertions pass; focused format, Ruff, strict Pyright, and strict
  docs are clean. The correction-inclusive whole-tree gate passes 304-file
  formatting, Ruff, strict Pyright, 661 architecture assertions, strict docs,
  and 2,201 tests with 14 expected skips on each of CPython 3.12-3.14.
- **Artifacts:** The evidence-inclusive candidate reproduces a pure wheel and
  source distribution byte-for-byte, passes isolated-wheel and complete ten-
  artifact release smoke, contains 94 wheel and 488 source entries, and has no
  native/WASM wheel member. Exact immutable candidate hashes are captured with
  commit/PR evidence rather than self-embedded into the source distribution.
- **Hosted gate:** Ready PR #135 exact initial head
  `e17476380d979e2bec891db9fdf9a8523734e8b5` passed run `31494364000` in
  exactly three Linux-first allocations. Linux `93788273122` passed in 7m09s
  before macOS `93790316767` and Windows `93790316678` began; they passed in
  3m22s and 4m11s. Every complete hosted suite passed 2,203 tests with one
  expected skip outside the baseline. This first run is superseded by the
  review correction and is not final-head qualification or integration
  authority.
- **Corrected hosted gate:** Exact corrected head
  `75d985f40bec2c073952172e53075ddadc8bc214` passed run `31496532379` in
  exactly three Linux-first allocations. Linux `93795541158` passed in 7m18s
  before macOS `93797741480` and Windows `93797741693` began; they passed in
  3m18s and 4m05s. The Linux baseline and every compatibility suite passed
  2,205 tests, with one expected skip outside the baseline. Every platform
  passed ten real-graphics tests, both profiles, and both vertical slices.
- **Review and integration:** Two delayed corrected-head audits found exact
  head/base, `MERGEABLE/CLEAN`, three successful checks, no conversation
  comment, and only the addressed/resolved P1 thread. Head-pinned GitHub-
  verified squash `7feded4ed2e37157b87a7f3bb733caf96805187e` has tree
  `3ae8059dc5a4f61a8a3b31d245b20f0373e0ffe4` exactly equal to the reviewed
  head, sole parent exact M60 closeout, and a parsed DCO trailer. The feature
  branch is deleted locally/remotely; no post-merge `main` run or open feature
  PR exists.
- **Integration record:** Ready PR #136 exact head
  `d80292ab4be734093bed52d0b0435da4d8b164e6` changed exactly four
  documentation paths and passed run `31497995187` in one 38-second Linux
  allocation. The desktop umbrella skipped with zero steps. Two delayed audits
  found no comment, review, or thread. GitHub-verified squash
  `9d1c4d4f967e97c7c77cf3b95d82c2d57367162e` has the exact reviewed tree
  `8da574c0f2642369a725e6eb32d3983176e38dac`, sole parent the feature squash,
  and a parsed DCO trailer. Both working branches are deleted locally/remotely;
  no post-integration `main` run or open PR exists.
