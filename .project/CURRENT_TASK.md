# Current Task

- **Task:** M71 - checksum-admitted sample snapshot
- **Status:** Implementation, documentation, complete local qualification,
  findings-first review, record-inclusive qualification, and final static/docs
  freeze are complete. Ready for DCO publication and quota-bounded hosted
  qualification.
- **Started:** 2026-08-13
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact synchronized M70 closeout
  `f62631e2541f8f6a34b0ed84f489c2d7f9503747`, tree
  `f1e8ecc9b0d681a6fb4006354c8d983b2f4f119c`.
- **Base qualification:** M70 feature PR #162, one-runner integration-record PR
  #163, and no-run closeout PR #164 were squash-integrated with exact reviewed
  trees, valid GitHub signatures, and exact DCO trailers. All M70 branches and
  18 generated targets were pruned; synchronized `main` was the only branch.
- **Outcome:** Make one owned, bounded, checksum-admitted sample snapshot the
  exact byte source for ZIP parsing and extraction.
- **Acceptance:** After path/descriptor admission, copy at most 16 MiB plus one
  rejection byte into an owned binary spooled temporary file while hashing;
  clear and fail content-silently on limit/digest mismatch before ZIP parsing;
  parse the rewound admitted snapshot; prove source changes cannot alter it;
  close snapshot/source on success and failure; admit the unchanged producer.
- **Boundary:** Private complete release smoke only. No persistent copy, cache,
  recovery artifact, lock, source-immutability guarantee, raw ZIP parser,
  general archive sandbox, workflow, dependency, sample producer, runtime API,
  release authority, tag, release, publication, or real public observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Research:** Python 3.12 documents `SpooledTemporaryFile` as a file-like
  temporary object and `ZipFile` seekable file-object input; CWE-367 motivates
  reducing check/use separation; SLSA assigns digest verification to consumers.
- **Failing baseline:** Exact M70 code produced 7 failures and 2 passing
  protected/producer guards in 0.36 seconds. The snapshot helper, owned parser
  input, source-independent behavior, ordering contract, RFC, and docs were
  absent; parsing still received the source descriptor.
- **Implementation checkpoint:** After implementation, the M70/M71 pair
  produced 13 passes with only deliberately absent documentation failing in
  0.41 seconds. Strict Pyright was clean; Ruff identified only import ordering.
- **Focused gate:** Import ordering was normalized. M71 passes 9 assertions in
  0.29 seconds; inherited M64-M71 passes 90 with 1 local capability skip in
  0.90 seconds. Four affected Python files are format/Ruff clean; strict
  Pyright is clean; strict docs build in 1.20 seconds; whitespace passes. The
  M68 historical guard retains path/descriptor admission and now recognizes
  the checksum-admitted snapshot before parser construction.
- **Complete local gate:** The unchanged lock, whole-tree formatting, Ruff,
  strict Pyright/docs, all supported interpreters, architecture suite, 10
  real-wgpu tests, both profiles, both vertical slices, and all four diagnostic
  benchmark validators pass. CPython 3.12 passed 2,309 non-wgpu tests with 15
  skips; CPython 3.13 and 3.14 each passed 2,309 with 16 skips; architecture
  passed 779 assertions with 1 local capability skip.
- **Artifacts:** Two pre-review builds reproduced a pure 273,524-byte wheel at
  `791f2c909cf9b89381443f0b89d6baa79ed56f7a0bd96fa7de4d09521f597671`
  and a 1,225,504-byte sdist at
  `ef631bcdb169baa8e41036cafaaa0720edd38402db127847fb9a683e3d8e3166`.
  Installed-wheel, deterministic staging, and complete release smoke pass; no
  inspected wheel, sdist, or sample entry is native or WASM.
- **Review:** No implementation defect or overclaim remains. Review
  strengthened the runtime proof so the test observes `ZipFile` receiving the
  distinct snapshot and verifies both owned streams close after checksum
  failure; the focused file now passes 10 assertions. No workflow, runtime
  package, producer, dependency, metadata, lock, or release authority changed.
- **Record-inclusive gate:** The unchanged lock resolves 46 packages; all 314
  files are format clean; Ruff and strict Pyright are clean; all 780
  architecture assertions pass with 1 local capability skip; strict docs,
  whitespace, and full Git-object checking pass. Two builds reproduce the
  feature-identical wheel and a 1,227,248-byte record-updated sdist at
  `530ebef65bd489cf16a74760c84d4b308fc9180b62849345da4bf70b19349de0`;
  wheel, staging, and complete release smoke pass.
- **Final freeze:** The unchanged lock resolves 46 packages; all 314 files are
  format clean; Ruff and strict Pyright are clean; all 780 architecture
  assertions pass with 1 local capability skip; strict docs and whitespace
  pass. Exact commit artifact identity remains a hosted qualification fact
  because recording an sdist digest changes it.
- **Next gate:** Review exact scope and Git history, then DCO-publish for
  Linux-first hosted qualification.
