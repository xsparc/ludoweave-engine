# Current Task

- **Task:** M64 - bounded sample-bundle extraction
- **Status:** Ready PR #144 passed its first three-allocation hosted gate; the
  actionable BZIP2/LZMA review finding is corrected and fully locally validated
  for a DCO-signed follow-up commit and fresh hosted qualification.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M63 closeout
  `a92330c5d592eaeba69e75e25dd94d83b22d367f`, whose tree
  `86cf786b01eb92ff39fcdbdc5464540f4b3c8eea` exactly matches the reviewed
  closeout head. GitHub reports a valid signature and parsed DCO trailer. Only
  `main` existed locally/remotely, no pull request was open, the closeout
  created no run or check, and no post-closeout `main` run exists.
- **Outcome:** Bound staged sample-ZIP expansion and memory use before the
  installed-candidate release smoke extracts any member.
- **Acceptance:** Preflight no more than 256 members, 1 MiB declared
  uncompressed per member, and 8 MiB declared uncompressed total before the
  first filesystem write; retain path and symbolic-link validation; stream
  admitted stored/deflated members in 64 KiB blocks; reject BZIP2, LZMA, and
  unknown methods; require copied size to match metadata.
- **Boundary:** Private release-smoke limits only. No general archive sandbox,
  authentication claim, duplicate/case/Unicode filename policy, cleanup or
  rollback guarantee, workflow, runner allocation, dependency, lock, version,
  runtime package/API, release authority, tag, release, publication, or real
  public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Development evidence:** The unchanged M63 staged bundle measures 50 members,
  379,577 total declared uncompressed bytes, a 33,018-byte largest member, and
  111,168 compressed bytes. Against unchanged production code, the initial
  eight-case M64 file failed seven assertions and passed the protected-surface
  guard in 0.44 seconds: all three limits were absent, oversized fixtures wrote
  before later completeness failure, whole-member reads remained, and RFC-0047
  was absent. The implementation adds complete metadata preflight and streaming
  copies. Seven non-documentation tests now pass in 0.29 seconds. A combined
  command reported only eight strict-Pyright private-usage findings in this
  intentional test seam; its final pytest segment returned zero, so that
  invocation is not a complete static pass. The suppression is now confined to
  this architecture test. Its first form included explanatory prose that
  Pyright rejected after formatting and Ruff passed; the corrected exact
  directive passes. Both changed Python files are format/Ruff/Pyright clean,
  all eight M64 assertions pass in 0.27 seconds, and strict docs build in 1.05
  seconds with only the known upstream notice. All 699 inherited architecture
  and release-artifact assertions pass in 5.27 seconds.
- **Source gate:** The unchanged lock, locked graphics environment, whole-tree
  formatting, Ruff, strict Pyright, all 699 architecture/release-artifact
  assertions, strict docs, and whitespace pass. The candidate passes 2,237
  tests with 14 expected skips on CPython 3.12, 3.13, and 3.14. Renderer,
  profile, example, benchmark, twice-reproducible distribution, isolated-wheel,
  and complete bounded release-smoke gates also pass. Findings-first review and
  archive inspection found no scope, credential, backend/native, or payload
  leakage. It clarified the central-directory parse boundary and added direct
  short/long streamed-size mismatch regressions. After one fail-fast Ruff
  import-order correction, formatting, Ruff, strict Pyright, all ten M64 tests,
  and all 701 inherited assertions pass. Final exact-tree gates remain pending.
- **Final source gate:** The exact current records/source state is format, Ruff,
  and strict-Pyright clean; all 701 inherited assertions, strict docs, lock,
  environment, and whitespace pass. The reviewed candidate passes 2,239 tests
  with 14 expected skips on CPython 3.12, 3.13, and 3.14; final real-wgpu,
  profiles, examples, and four diagnostic benchmark validators pass. Final
  twice-reproducible artifacts, isolated-wheel smoke, and complete bounded
  release smoke pass. The final record-frozen source gate passes; only exact
  commit review and hosted qualification remain.
- **Hosted evidence:** Ready PR #144 exact initial head
  `c5813633f8ff7970311cc7ab8e1159f844c056f7` passed run `31513476270` in
  exactly three Linux-first allocations: Linux `93852742523` passed in 7m33s,
  then macOS `93854944611` passed in 2m56s and Windows `93854944488` in 4m28s.
  Linux baseline and all compatibility suites passed 2,243 tests; compatibility
  suites reported one expected skip. Hosted builds reproduced a 272,176-byte
  wheel at `80a52b31109504d23a6d4fc5c5c36c9427c3f3d11ef3a2fa83362043236aedc4`
  and a 1,160,677-byte source archive at
  `d0b61cc6b97aabdf2eeb6166385dad6c1201858b5b647aee359426a9d7e9efdf`;
  installed-wheel and complete release smoke passed. The first review audit
  then identified CPython's unbounded-output BZIP2/LZMA read path. Local source
  inspection confirmed the distinction; the reviewer-derived test failed three
  assertions and passed ten against the hosted head. The correction admits only
  stored/deflated members. Its corrected focused formatting, Ruff, strict
  Pyright, all 13 M64 assertions, 704 inherited architecture/release-artifact
  assertions, strict docs, and whitespace pass. The corrected candidate passes
  2,242 tests with 14 expected skips on every supported CPython, real-wgpu,
  profiles, vertical slices, twice-reproducible builds, installed-wheel smoke,
  and corrected complete release smoke. Final record/commit validation and a
  new hosted run remain; the final record-inclusive source gate is green.
