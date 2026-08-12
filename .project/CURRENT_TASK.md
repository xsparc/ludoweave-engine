# Current Task

- **Task:** M71 - checksum-admitted sample snapshot
- **Status:** M71 feature and integration evidence are hosted-qualified,
  review-clean, squash-integrated, and fully verified. The current three-file
  closeout records only completion facts and requests no hosted allocation.
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
- **Hosted qualification:** Exact DCO head
  `fd124202e95288f305fd57a74c918550c8104804`, tree
  `e144b20a8ec372defd7766c9d81dd943342f6adf`, passed run `31616197801`
  in exactly three Linux-first allocations. Linux completed in 7m21s, macOS
  in 3m10s, and Windows in 4m12s.
- **Hosted suites:** Linux CPython 3.12 and all hosted 3.13/3.14 suites passed
  2,325 tests with 1 expected compatibility skip where applicable. Each OS
  passed 10 real-wgpu tests, its graphics profile, Clockwork Arena, and Agent
  World Builder; Linux also passed formatting, Ruff, strict Pyright/docs, the
  base profile, reproducible builds, wheel smoke, staging, and release smoke.
- **Hosted artifacts:** Two exact-head builds reproduced a pure 273,509-byte
  wheel at
  `06c2501eb5fcc999ff2d59716bd47bc5ecafb0a25473d485d314327a57867e82`
  and a 1,227,996-byte sdist at
  `50dc7061ace2bbf1a4947246062aa355594cd95fbff44c250fe10ff8e15be678`.
- **Hosted review:** Two separated exact-head audits found no issue comment,
  review, inline comment, or review thread; the PR remained clean and
  mergeable.
- **Feature integration:** PR #165 squash
  `a408198b2a3ce9e59d50372095dde2afb6ac9fe5` has the exact reviewed tree,
  sole parent M70 closeout `f62631e2541f8f6a34b0ed84f489c2d7f9503747`,
  valid GitHub signature verified at `2026-08-12T16:23:48Z`, and exact DCO.
  The feature branch is absent remotely and locally.
- **Integration local qualification:** The exact four-file record passes the
  unchanged lock, whole-tree formatting/Ruff/strict-Pyright, all 780
  architecture assertions with 1 capability skip, strict docs, whitespace,
  full Git-object checking, two-build reproducibility, installed-wheel smoke,
  deterministic staging, and complete release smoke. The feature-identical
  pure wheel is 273,524 bytes at
  `791f2c909cf9b89381443f0b89d6baa79ed56f7a0bd96fa7de4d09521f597671`;
  the record-updated sdist is 1,229,599 bytes at
  `88e50fabed0299caa603166043967123997b8ecb686d10c3953fd2fc3cca24d7`.
- **Integration hosted qualification:** Exact DCO head
  `f4bb6ef2fac3d4e8d58203c7028aee0f9aa5a73a`, tree
  `ac55309b8a9a31a4706849f5954504e5292f81bf`, passed run `31617678812`
  in one 44-second Linux allocation. The desktop umbrella skipped with zero
  steps. All 314 files were format clean; Ruff and strict docs passed; 781
  selected architecture assertions passed in 9.50 seconds; wheel/staging/
  release smoke passed.
- **Integration hosted artifacts:** The feature-identical pure wheel is
  273,509 bytes at
  `06c2501eb5fcc999ff2d59716bd47bc5ecafb0a25473d485d314327a57867e82`;
  the exact integration-head sdist is 1,229,985 bytes at
  `5b7a5d3d1de4de06ea83a4274c8d67fe449d7c0b24c665919acd5a2e1d348d8a`.
- **Integration review/integration:** Two separated audits were clean. PR #166
  squash `9ce08e520c97ddb06de446718fbdc8ada90060ad` has the exact reviewed tree,
  sole parent feature squash `a408198b2a3ce9e59d50372095dde2afb6ac9fe5`,
  valid GitHub signature verified at `2026-08-12T16:30:25Z`, and exact DCO.
  The integration branch is absent remotely and locally.
- **Closeout local qualification:** Exactly the three `.project` records pass
  all 780 architecture assertions with 1 local capability skip, strict docs,
  whitespace, full Git-object checking, exact scope, and credential/metadata-
  identity hygiene. No workflow, runtime, verifier, producer, dependency,
  package, test, public documentation, or roadmap surface changes.
- **Next gate:** DCO-publish and squash-integrate this exact no-run closeout;
  prune generated M71 targets and leave only a clean synchronized `main`
  before selecting M72.
