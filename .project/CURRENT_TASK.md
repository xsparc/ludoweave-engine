# Current Task

- **Task:** M59 - repository metadata hygiene
- **Status:** Complete. Feature PR #129 and integration-record PR #130 are
  fully validated, review-clean, squash-integrated, and branch-clean;
  publishing the exact three-file closeout on `records/m59-closeout`.
- **Started:** 2026-08-11
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M58 closeout
  `d4487565d4fda57ec05437dfcadc687d2507dafa`, with only `main` present and no
  open pull request, tag, release, closeout run/check, or post-closeout `main`
  run.
- **Outcome:** Make current tracked repository metadata tool-neutral without
  weakening maintenance guards or altering immutable provenance.
- **Acceptance:** Current tracked and non-ignored working-tree text contains no
  retired tooling-identity marker. Retired root control paths remain absent.
  The one legacy actor fixture is neutral, three duplicated checks defer to one
  centralized architecture guard, and current project records use descriptive
  redactions while retaining exact commit, PR, workflow, artifact, test, and
  timing evidence.
- **Boundary:** No Git-history rewrite, attribution or DCO change, Git-object
  deletion, runtime source, product-facing agent terminology, public API,
  protocol, workflow, dependency, lock, version, tag, release, publication, or
  release-authority change. The working-tree guard is not a forensic erasure
  claim for immutable history or external systems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Local evidence:** The initial tracked-tree scan found 107 matching
  lines across the two current project-record files and four tests. The new
  central guard then failed one assertion and passed its absent-root control,
  naming all six affected files. After neutralizing those files, 56 focused
  inherited and new assertions passed; focused Pyright was clean. The first
  documentation-contract run passed both hygiene assertions and failed only
  because the M59 contract had not yet been added. After implementation and
  review corrections, whole-tree formatting, Ruff, strict Pyright, 637
  architecture assertions, strict docs, graphics-enabled complete suites on
  CPython 3.12-3.14, real-wgpu tests, five-repeat profiles, both vertical
  slices, M1-M4 benchmark validators, reproducible pure distributions,
  isolated-wheel smoke, complete release smoke, archive review, whitespace,
  credential-pattern, protected-surface, and Git-object checks pass. The
  immutable history retains expected unreachable development objects. Review
  then identified that `Path.exists()` alone misses a dangling retired root
  symlink. The reviewer-derived regression failed before the lexical check was
  added; the correction treats existence or symlink identity as a violation,
  and all five focused assertions now pass with format, Ruff, and strict
  Pyright clean.
- **Hosted gate:** This test/documentation maintenance slice is substantive and
  requires exactly three Linux-first allocations; desktop jobs may begin only
  after Linux qualification succeeds.
- **Hosted evidence:** Corrected exact head
  `28e80e66eb16656a998353627ef78a8fe6e4c80b` passed run `31484028669` in
  exactly three Linux-first allocations. Linux passed in 6m05s before macOS
  and Windows began; they passed in 2m53s and 4m08s. Baseline and compatibility
  suites passed 2,182 tests, with one expected skip outside baseline. Every
  platform passed ten real-graphics tests, profile smoke, and both vertical
  slices; reproducible build, installed-wheel smoke, and release smoke passed.
- **Integration:** The valid P2 was corrected, answered, and resolved. Two
  delayed audits found no unresolved or later review activity. Head-pinned,
  GitHub-verified squash
  `f12f65ab7c1f8426b0232bb4b414e48276bbad56` has the exact corrected tree,
  sole parent M58 closeout, and standalone DCO. Integration PR #130 exact head
  `f142ceae1381c5c8c6cb15001229cfd4679ff028` passed run `31485465637` in one
  42-second Linux allocation; all 638 architecture assertions, strict docs,
  reproducible builds, installed-wheel smoke, and complete release smoke
  passed, while desktop umbrella `93759917789` skipped with no runner and zero
  steps. Two delayed integration audits found no comment, review, or thread.
  GitHub-verified squash `f6b734878738ca6408afeabb793c5cd591c0d607`
  reproduces the reviewed record tree with the feature squash as sole parent,
  valid signature, and standalone DCO. Both M59 working branches are deleted
  locally/remotely. Synchronized `main` has no post-merge run or non-main
  branch.
- **Closeout gate:** The exact three-file `.project/**` record must allocate
  zero hosted runs or checks.
