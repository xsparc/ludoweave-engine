# Current Task

- **Task:** M75 - compressed-patch sample-member preflight
- **Status:** M75 feature and integration records are fully qualified and
  squash-integrated. The exact three-record no-CI closeout is in progress.
- **Started:** 2026-08-13
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact synchronized M74 closeout
  `674d74c8fc852846404813ab541aab3deffd8608`, tree
  `cbe1b75ae6c3174c04b0712894244918cae69010`.
- **Base qualification:** M74 feature PR #174, one-runner integration-record
  PR #175, and no-run closeout PR #176 were squash-integrated with exact
  reviewed trees, exact DCO trailers, and valid GitHub signatures. All M74
  branches and 18 generated targets were pruned; synchronized `main` was the
  only branch.
- **Gap:** ZIP general-purpose bit 5 declares compressed patched data. Exact
  supported CPython `ZipFile.open` paths reject it only at member open with
  `NotImplementedError`, after the current all-member flag preflight and after
  inventory/staging work can begin.
- **Outcome:** Reject exactly compressed patched data during M69's all-member
  flag preflight, before member metadata, inventory validation, staging, or
  member reads.
- **Acceptance:** Define exact flag `0x0020`; use a stable content-silent policy
  error; prove later-member preemption and owned cleanup; retain encryption
  precedence; leave unrelated flags out of scope; admit the current producer.
- **Boundary:** Private complete release smoke only. No broad flag allowlist,
  reserved-bit policy, `NotImplementedError` catch, patch decoder, repair, raw
  ZIP parser, scanner, workflow, dependency, sample producer, runtime API,
  release authority, tag, release, publication, or real public observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Research:** PKWARE APPNOTE 6.3.9 assigns general-purpose bit 5 to compressed
  patched data. Exact installed CPython 3.12.13, 3.13.13, and 3.14.5 all test
  that bit in `ZipFile.open` and raise the same `NotImplementedError`.
- **Failing baseline:** The statically clean M75 regression passed 3 standard-
  library/protected/out-of-scope guards and failed 7 contract assertions in
  0.34 seconds against exact M74. The actual exact-inventory path reached
  inventory/staging and escaped with CPython's raw flag-specific error; the
  constant, policy branch, producer assertion, source contract, and docs were
  absent.
- **Implementation checkpoint:** One exact constant and one ordered branch
  after encryption implement the policy. Affected formatting, Ruff, and strict
  Pyright pass. All 9 M75 behavioral/source/protected assertions plus all 9 M69
  compatibility assertions pass; only the deliberately absent RFC/docs
  assertion failed in the 19-test group.
- **Focused gate:** After correcting one exact documentation phrase, all 10
  M75 assertions pass in 0.21 seconds and inherited M64-M75 passes 126
  assertions with 1 local filesystem-capability skip in 1.18 seconds. Affected
  formatting, Ruff, and strict Pyright are clean; strict docs build in 1.22
  seconds and whitespace passes.
- **Complete local gate:** The unchanged lock resolves 46 packages and the
  locked graphics environment contains 45 packages. All 318 files are format
  clean; Ruff and strict Pyright report zero findings. CPython 3.12, 3.13, and
  3.14 each pass 2,345 tests with 15 skips; all 815 architecture assertions
  pass with 1 local capability skip.
- **Graphics/diagnostics:** All 10 real-wgpu tests pass in 7.99 seconds; both
  five-repeat profiles validate. Clockwork Arena and Agent World Builder
  reproduce their deterministic state/capture/replay identities. All four
  fresh M1-M4 diagnostic artifacts validate: M1 and M3 each observe one of two
  targets, M2 has no targets, and M4 observes its baseline target.
- **Pre-review artifacts:** Two builds reproduce a pure 274,103-byte wheel at
  `60824005e82908164ad7a6433d3647cdf011d9aa03dec884aa8d142904084784`
  and a 1,256,257-byte sdist at
  `9d33bf47e294d63a5dc6bce66d60781562676e5881158d414d849b23d785df49`.
  Installed-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. The sample remains 111,168 bytes/50 entries at
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  no inspected wheel or sample entry is native or WASM.
- **Scope:** Intended scope is exactly 16 paths: one private release-smoke
  script, one regression, one new RFC, one M69 supersession note, six public
  boundary/index/navigation documents, and four neutral project records.
  Workflows, sample producer, runtime package, dependencies, metadata, lock,
  benchmarks, version, and release authority remain unchanged.
- **Review:** No product, test, RFC, or scope defect remains. The exact bit-5
  mutation proves CPython's raw failure and the earlier content-silent policy;
  all-member ordering, cleanup, encryption precedence, unrelated flags, current
  producer, protected surfaces, and public non-claims are executable.
- **Record-inclusive gate:** The unchanged lock resolves 46 packages and the
  graphics environment checks 45 packages; all 318 files are format clean;
  Ruff and strict Pyright are clean; all 815 architecture assertions pass with
  1 local capability skip; strict docs, whitespace, and Git-object checking
  pass. Two builds reproduce the pure 274,103-byte wheel at
  `60824005e82908164ad7a6433d3647cdf011d9aa03dec884aa8d142904084784`
  and a 1,257,198-byte record-updated sdist at
  `ece63f8b3f70b3aa9600e4a64543b5a0143ba0f3c794e119d29461560936600d`;
  wheel, staging, and complete release smoke pass. Exact commit artifact
  identity remains delegated to hosted qualification because recording this
  result changes the sdist.
- **Final freeze:** The unchanged lock resolves 46 packages; all 318 files are
  format clean; Ruff and strict Pyright are clean; all 815 architecture
  assertions pass with 1 local capability skip; strict docs, whitespace, and
  Git-object checking pass. Exact 16-path scope, protected hashes, credential/
  private-key hygiene, and explicit development-tool identity hygiene pass.
- **Prepublication audit:** Feature `HEAD`, local `main`, `origin/main`, and the
  merge base are exact M74 closeout with symmetric difference `0 0`; history is
  linear. Only remote `main` exists; GitHub reports no open PR, tag, or release.
- **Exact post-record freeze:** All 318 files are format clean; Ruff and strict
  Pyright are clean; all 815 architecture assertions pass with 1 local
  capability skip; strict docs, whitespace, and exact 16-path scope pass.
- **Hosted qualification:** Exact DCO head
  `77ab1757ea52be4c5532adfe26c27bfa202504ef`, tree
  `b0aac18c83fc6e93bd5fd1e1f154100e2bc75799`, passed run
  `31633932748` in exactly three Linux-first allocations. Linux passed in
  7m21s, macOS in 3m25s, and Windows in 4m06s.
- **Hosted suites/artifacts:** All 318 files and static/docs gates passed.
  Linux CPython 3.12/3.13/3.14 and macOS/Windows 3.14 each passed 2,360
  tests, with 1 expected skip outside Linux 3.12; every OS passed 10 real-wgpu
  tests. Two builds reproduced a pure 274,089-byte wheel at
  `af0ea15e0ac4851461a93d79b11b587d2d230fc91219c2da47acee5574901d4b`
  and a 1,257,945-byte sdist at
  `7f68ef379d335c9a4b3cefb7e9409af26fb759f8ebffc28dc7a7bb11e8d43917`;
  profiles, examples, wheel, staging, and release smokes passed.
- **Hosted review/integration:** Two separated audits found zero comment,
  review, inline comment, or thread. PR #177 squash
  `b86013397d5ad5f28d9a9adfe7c7f30996cbad65` has the exact reviewed tree,
  sole parent M74 closeout, exact DCO, and a valid GitHub signature verified at
  `2026-08-12T19:55:01Z`; the feature branch is absent locally and remotely.
- **Integration local qualification:** The unchanged lock resolves 46
  packages; all 318 files are format clean; Ruff and strict Pyright are clean;
  all 815 architecture assertions pass with 1 local capability skip; strict
  docs, whitespace, and Git-object checking pass. Two builds reproduce the
  feature-identical 274,103-byte wheel at
  `60824005e82908164ad7a6433d3647cdf011d9aa03dec884aa8d142904084784`
  and a 1,259,225-byte record-updated sdist at
  `5f5051d0e2831634eb2b2bb596258a2782fa83fd5063cac3854df4e296e1d2a7`;
  wheel, staging, and release smoke pass.
- **Hosted integration:** Exact DCO head
  `26640c723b48a208301c86dacc5f53772bc745fe`, tree
  `a8ea9e89a40adaf0125623b86face642c721533e`, passed run
  `31635295952` in one 38-second Linux allocation; desktop skipped with zero
  steps. The gate passed 816 selected architecture assertions, strict docs,
  reproducible artifacts, wheel, staging, and release smokes. Hosted wheel was
  274,089 bytes at
  `af0ea15e0ac4851461a93d79b11b587d2d230fc91219c2da47acee5574901d4b`;
  sdist was 1,259,477 bytes at
  `bf99be5f80bf644173b309efb8c75950c5de718efaff8acdcea71e34361c3a1c`.
- **Integration merge:** Two audits found no review activity. PR #178 squash
  `57dc9af600a5e651bc051fb5a47b2902cb2e2403` has the exact reviewed tree,
  sole feature-squash parent, exact DCO, and valid GitHub signature verified at
  `2026-08-12T20:00:32Z`; the branch is deleted.
- **Closeout qualification:** All 318 files are format clean; Ruff and strict
  Pyright are clean; all 815 architecture assertions pass with 1 local
  capability skip; strict docs, whitespace, and Git-object checking pass. The
  diff is exactly the three neutral project records.
- **Next gate:** Qualify and publish the exact no-CI three-record closeout,
  prune M75 artifacts/branches, and return to synchronized `main`.
