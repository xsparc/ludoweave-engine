# Current Task

- **Task:** M74 - content-silent sample ZIP decompression failures
- **Status:** Direction research, failing regression, minimal implementation,
  and corrected implementation checkpoint are complete. RFC and public
  boundary documentation are in progress.
- **Started:** 2026-08-13
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact synchronized M73 closeout
  `7ecb584e71a375d1ab63ee8134e7493e418dedff`, tree
  `fafa86abb05929711e38f34b4d219bcfc7161637`.
- **Base qualification:** M73 feature PR #171, one-runner integration-record
  PR #172, and no-run closeout PR #173 were squash-integrated with exact
  reviewed trees, valid GitHub signatures, and exact DCO trailers. All M73
  branches and 18 generated targets were pruned; synchronized `main` was the
  only branch.
- **Outcome:** Convert the standard decompressor's exact `zlib.error` from a
  checksum-admitted deflated sample member to the existing stable content-
  silent ZIP-data error after owned cleanup.
- **Acceptance:** Catch exactly `zlib.error` alongside M72/M73's established
  exceptions; exercise a real invalid raw-deflate block behind valid inventory
  and checksum admission; suppress rendered decompressor detail while retaining
  programmatic context; close owned source/snapshot/archive/staging; preserve
  EOF, policy, filesystem, and producer behavior.
- **Boundary:** Private complete release smoke only. No `EOFError`, `OSError`,
  broad compression/general catch, replacement decompressor, repair, raw ZIP
  parser, scanner, workflow, dependency, sample producer, runtime API, release
  authority, tag, release, publication, or real public observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Research:** Official Python documentation defines `zlib.error` for
  compression/decompression failures. Exact installed CPython 3.12.13 and
  3.13.13 with zlib 1.3.1 and CPython 3.14.5 with zlib-ng 1.3.1 all route
  deflated ZIP member bytes through the decompressor without recategorizing
  that exception.
- **Failing baseline:** Exact M73 passed 4 policy/producer/protected guards and
  failed 4 assertions in 0.38 seconds. Two actual checksum-admitted invalid-
  deflate paths escaped as raw `zlib.error`; the exact source catch and
  RFC/docs were absent.
- **Implementation checkpoint:** The two-line runtime change imports stdlib
  `zlib` and adds exactly `zlib.error` to the existing outer tuple. The first
  checkpoint exposed M73's historical whole-tuple assertion; its guard was
  narrowed to M73's required members. The corrected M73/M74 group passes 15
  assertions with only the deliberately absent M74 RFC/docs assertion failing
  in 0.43 seconds. Affected formatting, Ruff, and strict Pyright are clean.
- **Focused gate:** All 8 M74 assertions pass in 0.22 seconds; inherited
  M64-M74 passes 116 assertions with 1 local filesystem-capability skip in
  1.02 seconds. Affected formatting, Ruff, and strict Pyright are clean;
  strict docs build in 1.44 seconds; whitespace passes.
- **Complete local gate:** The unchanged lock resolves 46 packages; the locked
  graphics environment contains 45 packages; all 317 files are format clean;
  Ruff and strict Pyright are clean. CPython 3.12 passes 2,335 tests with 15
  skips; CPython 3.13 and 3.14 each pass 2,335 with 16 skips; architecture
  passes 805 assertions with 1 local capability skip.
- **Graphics/diagnostics:** All 10 real-wgpu tests pass in 7.64 seconds; both
  five-repeat profiles validate; Clockwork Arena and Agent World Builder
  reproduce their deterministic state/capture/replay hashes. All M1-M4
  diagnostic artifacts validate: M1 observes one of two targets, M2 has no
  targets, M3 observes one of two targets, and M4 observes its baseline target.
- **Pre-review artifacts:** Two builds reproduce a pure 273,952-byte wheel at
  `ada989ae548bdf51f124d39080a83580711e58e5148b149b28a72dbaf59c8bcf`
  and a 1,247,726-byte sdist at
  `f06f525fda77ddd9d618ac92a4c7bbfb2f33cc4c29d6358c1310106a71951988`.
  Wheel, staging, and complete release smoke pass. The sample remains 111,168
  bytes/50 entries at
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  no inspected wheel, sdist, or sample entry is native or WASM.
- **Scope:** Exactly 17 intended paths, including the two new RFC/test paths.
  CI, release workflow, sample producer, package metadata, and lock hashes
  remain exact; no runtime package, dependency, benchmark, version, workflow,
  or release-authority surface changes.
- **Review:** No product, test, RFC, or scope defect remains. The exact invalid-
  block fixture retains valid metadata, inventory, and matching checksum;
  cleanup and rendered-context checks cover the staged failure; EOF and policy
  categories remain distinct. M73's inherited source guard now preserves its
  exact required members while permitting later narrow additions and still
  excluding broad catches. The M72-M74 group passes 25 assertions in 0.40
  seconds; whole-tree static checks, strict docs, and whitespace pass.
- **Record-inclusive gate:** The unchanged lock, 45-package graphics
  environment, all 317 formatted files, Ruff, strict Pyright, 805 architecture
  assertions with 1 skip, strict docs, whitespace, and Git-object checking
  pass. Two builds reproduce the pure 273,952-byte wheel at
  `ada989ae548bdf51f124d39080a83580711e58e5148b149b28a72dbaf59c8bcf`
  and a 1,249,215-byte record-updated sdist at
  `ab78ce123bb24d9bee5e70871f13238745e31ded5da826e0a2969b2db03212a5`;
  wheel, staging, and complete release smoke pass. Exact commit artifact
  identity remains delegated to hosted qualification because recording this
  result changes the sdist.
- **Final freeze:** The unchanged lock resolves 46 packages; all 317 files are
  format clean; Ruff and strict Pyright are clean; all 805 architecture
  assertions pass with 1 local capability skip; strict docs, whitespace, and
  Git-object checking pass.
- **Prepublication audit:** Feature `HEAD`, local `main`, and `origin/main` are
  exact M73 closeout with symmetric difference `0 0`; history is linear. Only
  remote `main` exists; GitHub reports no open PR, tag, or release. Exact
  17-path scope, protected surfaces, credential/private-key hygiene, and
  explicit development-tool identity hygiene pass.
- **Exact post-record freeze:** All 317 files are format clean; Ruff and strict
  Pyright are clean; all 805 architecture assertions pass with 1 local
  capability skip; strict docs, whitespace, and exact 17-path scope pass.
- **Next gate:** Create the DCO feature commit, push the neutral branch, open
  the ready PR, and verify Linux-first hosted qualification is tied to that
  exact head.
