# Current Task

- **Task:** M62 - portable public release asset names
- **Status:** M62 implementation, review, feature integration, and integration-
  record integration are complete. This exact three-file zero-allocation
  closeout record establishes the verified M63 base on `records/m62-closeout`.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M61 closeout
  `14f848c92021d54c9140e01b0333c0725c45145d`, whose tree
  `0d62fdda4864c1b4f92083bbd59ee63afc6d38aa` exactly matches the reviewed
  closeout head. GitHub reports a valid signature and parsed DCO trailer. Only
  `main` existed locally/remotely, no pull request was open, the closeout
  created no run or check, and no post-closeout `main` run exists.
- **Outcome:** Reject public-release retrieval-plan asset basenames that do not
  preserve one deterministic portable child-file identity across Windows,
  macOS, and Linux.
- **Acceptance:** Admit 1 through 255 existing ASCII basename characters;
  reject a trailing period, a case-insensitive classic Windows device stem,
  and a case-insensitive duplicate with stable content-silent
  `public_release.invalid_plan` before asset download or output-directory
  creation. Preserve representative portable release names unchanged.
- **Boundary:** No filesystem probing, locale, Unicode normalization, filename
  rewriting, path resolution, race-free filesystem claim, cleanup, rollback,
  retry, workflow, runner allocation, dependency, lock, version, runtime
  package/API, release authority, tag, release, publication, or real public
  release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Development evidence:** Against unchanged M61 production code, the initial
  16-case M62 file failed 14 assertions and passed two in 0.51 seconds. All 11
  nonportable names, including a 256-character basename, were accepted; case-
  only duplicates were accepted; the invalid existing plan reached an
  intentionally forbidden asset download; and RFC-0045 was absent. The
  portable-name sample and protected-surface guard passed. After the parser-
  only correction, all 15 non-documentation assertions pass with the docs case
  deselected in 0.22 seconds. Both changed Python files are formatted, Ruff is
  clean, and strict Pyright reports zero diagnostics. The documented 16-case
  contract, 677 architecture assertions, 56 release-draft assertions with two
  platform-capability skips, whole-tree static and strict documentation gates,
  and complete graphics-enabled CPython 3.12.13, 3.13.13, and 3.14.5 suites are
  green. Each supported interpreter passed 2,217 tests with 14 expected skips.
  Real-wgpu coverage, both five-repeat profiles, both vertical slices, and all
  four benchmark artifact validators pass. M1 observed one of two targets, M3
  observed zero of two, and M4 observed its baseline target; those measurements
  are diagnostic facts rather than release gates. Two fresh builds reproduce a
  pure wheel and source archive; isolated-wheel and complete ten-artifact smoke
  pass. Findings-first review caught and corrected a stale README completion
  boundary with a failing regression. The final post-review builds reproduce a
  pure 271,887-byte wheel and 1,142,219-byte source archive; archive inventory,
  protected-surface, credential, tool-identity, whitespace, and Git-object
  audits are clean apart from expected unreachable historical objects.
- **Hosted evidence:** Ready PR #138 exact head
  `3bb7539463e34859b5ef8a63d2ea4bc1ff4c2cb2` passed run `31501434063`
  in exactly three Linux-first allocations. Linux passed in 7m20s before macOS
  and Windows began; they passed in 3m11s and 4m18s. Baseline passed 2,221
  tests; every compatibility suite passed 2,221 with one expected skip.
  GitHub-verified squash `a96fac6b4fdd2eb3c0d65ede17f66cede2faa232`
  has the exact reviewed tree, sole parent exact M61 closeout, and parsed DCO.
  Ready integration-record PR #139 exact head
  `5252987bc6b1da546f49f09b9358a2735e6b34f1` passed run `31503119877`
  in one 41-second Linux allocation; the desktop umbrella skipped with zero
  steps. GitHub-verified squash
  `de6ead04124b889318b5ab854d25a6b5324d05aa` has the exact reviewed tree,
  sole parent the feature squash, and parsed DCO.
