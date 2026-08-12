# Current Task

- **Task:** M73 - content-silent sample ZIP text failures
- **Status:** Implementation, documentation, complete local qualification,
  findings-first review, record-inclusive qualification, and final
  static/docs/history freeze are complete. Ready for DCO publication and
  quota-bounded hosted qualification.
- **Started:** 2026-08-13
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact synchronized M72 closeout
  `f4afb40aade2b1a59b7ceabf6f1db158b450b7cd`, tree
  `90e987138c2fa09fe62db2428e23421ec511a7a5`.
- **Base qualification:** M72 feature PR #168, one-runner integration-record PR
  #169, and no-run closeout PR #170 were squash-integrated with exact reviewed
  trees, valid GitHub signatures, and exact DCO trailers. All M72 branches and
  18 generated targets were pruned; synchronized `main` was the only branch.
- **Outcome:** Convert the standard ZIP reader's archive-controlled UTF-8 name
  decoding failures to M72's stable content-silent outer error after owned
  cleanup.
- **Acceptance:** Catch exactly `UnicodeDecodeError` alongside the existing
  `BadZipFile`/`LargeZipFile` pair; cover actual malformed central-directory
  and local-header names; suppress rendered invalid bytes/offsets while
  retaining programmatic context; close owned source/snapshot/archive/staging;
  preserve policy failures and the unchanged producer.
- **Boundary:** Private complete release smoke only. No `UnicodeError`,
  `ValueError`, or general exception catch; replacement decoder, metadata
  repair, raw parser, scanner, workflow, dependency, sample producer, runtime
  API, release authority, tag, release, publication, or real public
  observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Research:** Python documents `UnicodeDecodeError` as retaining invalid input
  and offsets. Exact installed CPython 3.12.13, 3.13.13, and 3.14.5 source
  strictly decodes UTF-8-marked central-directory and local-header names.
- **Failing baseline:** After one non-product setup failure from the absent
  external validation parent, the valid exact-M72 run produced 5 failures and
  3 passing policy/producer/protected guards in 0.41 seconds. Both real decode
  paths escaped raw; the narrow source contract and RFC/docs were absent.
- **Implementation checkpoint:** Format, Ruff, and strict Pyright pass. The
  M72/M73 implementation group passes 16 assertions with only the deliberately
  absent RFC/docs assertion failing in 0.48 seconds.
- **Focused gate:** M73 passes all 8 assertions in 0.22 seconds; inherited
  M64-M73 passes 108 with 1 local capability skip in 0.94 seconds. Affected
  Python formatting/Ruff and strict Pyright are clean; strict docs build in
  1.33 seconds; whitespace passes.
- **Complete local gate:** The unchanged lock resolves 46 packages; the locked
  graphics environment contains 45 packages; all 316 files are format clean;
  Ruff and strict Pyright are clean. CPython 3.12 passed 2,337 tests with 15
  skips; CPython 3.13 and 3.14 each passed 2,327 with 16 skips; architecture
  passed 797 assertions with 1 local capability skip.
- **Graphics/diagnostics:** All 10 real-wgpu tests pass in 7.32 seconds; both
  five-repeat profiles validate; Clockwork Arena and Agent World Builder
  reproduce their deterministic state/capture/replay hashes. All M1-M4
  diagnostic artifacts validate: M1 observed one of two targets, M2 retains no
  targets, M3 observed neither target, and M4 observed its baseline target.
- **Pre-review artifacts:** Two builds reproduce a pure 273,839-byte wheel at
  `32553b1c0bf9eea3bbd3b6ab63d51ee97ef4a2d6429054dc2049439b3175af5d`
  and a 1,240,741-byte sdist at
  `5c39589b70170715d04a1a4c83a147616f7953b53ec8f9348cb9c3c78f746877`.
  Wheel, staging, and complete release smoke pass. The sample remains 111,168
  bytes/50 entries at
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  no inspected wheel, sdist, or sample entry is native or WASM.
- **Review:** No product/RFC/scope defect remains. Review strengthened the
  local-header regression to observe archive closure and made M72's historical
  catch-boundary extraction precise. The first strengthened gate exposed an
  overly generic test recorder to strict Pyright; the exact one-stream
  signature corrected it. The corrected group passes 17 assertions, inherited
  M64-M73 passes 108 with 1 skip, and static/docs/whitespace checks pass.
- **Record-inclusive gate:** The unchanged lock resolves 46 packages; the
  45-package graphics environment, all 316 formatted files, Ruff, strict
  Pyright, 797 architecture assertions with 1 skip, strict docs, whitespace,
  and Git-object checking pass. Two builds reproduce the pure 273,839-byte
  wheel at
  `32553b1c0bf9eea3bbd3b6ab63d51ee97ef4a2d6429054dc2049439b3175af5d`
  and a 1,242,180-byte record-updated sdist at
  `5fc6b835edafdc6903b343ca038ed2b71a3f02f048536ed2e523b31ba5d82e8e`;
  wheel, staging, and complete release smoke pass.
- **Scope:** Exactly 17 intended paths. CI, release workflow, sample producer,
  package metadata, and lock hashes remain exact; no runtime package,
  dependency, benchmark, version, workflow, or release-authority surface
  changes.
- **Final freeze:** The unchanged lock resolves 46 packages; all 316 files are
  format clean; Ruff and strict Pyright are clean; all 797 architecture
  assertions pass with 1 local capability skip; strict docs, whitespace, and
  Git-object checking pass.
- **Prepublication audit:** Feature `HEAD`, local `main`, and `origin/main` are
  exact M72 closeout with symmetric difference `0 0`; history is linear. Only
  remote `main` exists; GitHub reports no open PR, tag, or release. Exact scope,
  protected surfaces, credential/private-key hygiene, and explicit
  development-tool identity hygiene pass.
- **Exact post-record freeze:** All 316 files are format clean; Ruff and strict
  Pyright are clean; all 797 architecture assertions pass with 1 local
  capability skip; strict docs, whitespace, and exact 17-path scope pass.
- **Next gate:** Run the exact post-record freeze, create the DCO feature
  commit, push the neutral branch, open the ready PR, and verify Linux-first
  hosted qualification is tied to that head.
