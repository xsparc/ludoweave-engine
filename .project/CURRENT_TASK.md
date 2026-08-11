# Current Task

- **Task:** M59 - repository metadata hygiene
- **Status:** The initial exact head passed hosted validation. One valid P2
  review finding now has a tests-first, fully locally qualified correction on
  `maintenance/m59-repository-hygiene`; corrected exact-head validation is
  pending.
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
- **Integration:** Pending complete local qualification, findings-first review,
  exact-head hosted validation, delayed review, verified squash integration,
  bounded integration record, and zero-run closeout.
