# Current Task

- **Task:** M61 - public release candidate/output-root separation
- **Status:** Complete locally on `security/m61-release-root-separation`;
  hosted qualification and review remain pending.
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
  output root as valid. Resolved parent aliases receive the same decision.
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
  all 11 final M61 assertions also pass on CPython 3.13 and 3.14.
- **Artifacts:** The evidence-inclusive candidate reproduces a pure wheel and
  source distribution byte-for-byte, passes isolated-wheel and complete ten-
  artifact release smoke, contains 94 wheel and 488 source entries, and has no
  native/WASM wheel member. Exact immutable candidate hashes are captured with
  commit/PR evidence rather than self-embedded into the source distribution.
- **Hosted gate:** This security/documentation maintenance slice is
  substantive and requires exactly three Linux-first allocations; desktop jobs
  may begin only after Linux qualification succeeds.
