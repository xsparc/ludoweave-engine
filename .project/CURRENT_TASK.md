# Current Task

- **Task:** M70 - sample-archive checksum binding
- **Status:** Implementation, documentation, full local qualification, and
  findings-first review are complete; hosted exact-head qualification remains.
- **Started:** 2026-08-13
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact synchronized M69 closeout
  `55b409d40c32c9268ee62b8c2a14aa036bcc935f`, tree
  `51b5bdfad0a139d141ea4ea2c0195fa8ece72d6c`.
- **Base qualification:** M69 feature PR #159, integration-record PR #160,
  and no-run closeout PR #161 were squash-integrated with exact reviewed trees,
  valid GitHub signatures, and exact DCO trailers. All milestone branches and
  generated outputs were pruned; synchronized `main` was the only branch.
- **Outcome:** Bind sample-archive parsing and staged-root publication to the
  sample digest already admitted from `SHA256SUMS`.
- **Acceptance:** Complete release smoke passes `checksums[bundle.name]` into
  extraction; the same opened handle is hashed and rewound before ZIP parsing
  and after member reads/completeness but before publication; either mismatch
  uses one stable content-silent category; second-check failure cleans owned
  staging; the current deterministic producer remains admitted.
- **Boundary:** Private project release smoke only. No snapshot, copy, lock,
  raw ZIP parser, filesystem isolation, race-free or immutable-input guarantee,
  defense against change-and-restore, signature, general archive sandbox,
  workflow, dependency, sample producer, runtime API, release authority, tag,
  release, publication, or real public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Research:** Python 3.12 documents seekable file-object ZIP input and binary
  hashing primitives; CWE-367 describes resource changes between check and
  use; SLSA treats artifact verification as a consumer responsibility.
- **Invalid setup attempt:** The first focused command used a nonexistent
  `D:\LudoWeaveValidation\m70` parent and produced 5 setup errors, 2 failures,
  and 1 pass. It is an environment failure, not a behavioral baseline.
- **Failing baseline:** After creating the exact disposable parent, unchanged
  M69 code produced 7 failures and 1 passing protected-surface guard in 0.28
  seconds. The helper, checksum argument, two comparisons, ordering contract,
  RFC, and documentation were absent.
- **Implementation checkpoint:** Runtime/test implementation produced 7 passes
  and only the intentionally absent documentation assertion failed in 0.30
  seconds. After documentation, the M70 file passes 8 assertions in 0.26
  seconds and inherited M64-M70 passes 84 with 1 local capability skip in 0.71
  seconds. Both changed Python files are format/Ruff clean, strict Pyright is
  clean, strict docs build in 1.22 seconds, and whitespace passes.
- **Local candidate:** An initial full-gate launch was denied access to the
  existing user uv cache and is recorded as an environment failure. The
  approved identical launch passes the unchanged 46-package lock, restored
  45-package CPython 3.12 graphics environment, formatting for 313 files,
  Ruff, strict Pyright, and strict docs.
- **Supported Python:** CPython 3.12 passes 2,303 non-wgpu tests with 15 skips;
  CPython 3.13.13 and 3.14.5 each pass 2,303 tests with 16 skips. All 773
  architecture assertions pass with 1 local capability skip.
- **Graphics and examples:** All 10 real-wgpu tests pass. Five-repeat base and
  graphics profiles validate; Clockwork Arena and Agent World Builder reproduce
  their established state/capture/replay evidence.
- **Diagnostics:** M1 accepts 7 workloads with 1 of 2 historical targets
  observed, M2 accepts 4 informational workloads, M3 accepts 6 workloads with
  0 of 2 targets met, and M4 accepts 3 with its baseline target observed.
- **Artifacts:** Two builds reproduce a pure 273,388-byte wheel at
  `865d6a8275886ecb3dab9e407c6401ab3eccf2e63a25a07ace91c4a641406f11`
  and a 1,216,959-byte source archive at
  `892b2cefdf9300f87d504dca89cf1a4cf654f46e77cea0c3b9366c6717372dc6`.
  Installed-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. The wheel has 94 entries, the sdist 506 including the
  M70 test/RFC, the sample has 50 entries, and no archive has native/WASM
  content.
- **Review:** Findings-first review identified that the first implementation
  read until EOF after descriptor admission, allowing a concurrently growing
  source to exceed M68's 16 MiB work bound. The sample-specific hash now reads
  at most the limit plus one rejection byte and rewinds. An unbounded-stream
  regression protects this correction.
- **Review gate:** M70 passes 9 assertions in 0.32 seconds; M64-M70 passes 85
  with 1 capability skip in 0.78 seconds; Ruff, strict Pyright, strict docs,
  and whitespace pass. The complete corrected CPython 3.12 suite passes 2,304
  non-wgpu tests with 15 skips in 110.05 seconds, and the corrected archive
  chain passes on 3.13/3.14 with 85 passes and 1 skip.
- **Record-inclusive gate:** The unchanged lock, all 313 formatted files, Ruff,
  strict Pyright, 774 architecture assertions with 1 capability skip, strict
  docs, whitespace, and full Git-object checking pass. Two reviewed builds
  reproduce the same pure 273,388-byte wheel and a 1,219,320-byte source
  archive at
  `acb09696c3f920423262c81fdacd1d072eb00491a7028c0b48b3124e6f3aafb2`;
  wheel, staging, and complete release smoke pass.
- **Scope and hygiene:** The exact 15-path candidate changes only the private
  release verifier, its M70 regression/RFC, public release/security/architecture
  docs, and neutral project records. CI/release workflows, runtime package,
  producer, benchmarks, dependencies, package metadata, and lock are unchanged.
  Added/current changed content has no credential/private-key or explicit
  development-tool identity match.
- **Record-frozen gate:** The unchanged lock, formatting for 313 files, Ruff,
  strict Pyright, 774 architecture assertions with 1 capability skip, strict
  docs, whitespace, and full Git-object checking pass on the exact candidate.
- **Next gate:** DCO-commit the exact candidate, push its neutral branch, and
  open the quota-bounded ready PR for Linux-first hosted qualification.
