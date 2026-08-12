# Current Task

- **Task:** M69 - encrypted sample-member preflight rejection
- **Status:** Initial feature head passed hosted qualification; one hosted P2
  ordering finding is corrected and locally revalidated for head update.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact synchronized M68 closeout
  `fec3df4d490d363a9ab538f6b99ec86859e7acdc`, tree
  `519955303ba8638ed9847df6b0d9cb62ded25436`.
- **Outcome:** Reject encryption-indicating sample ZIP members during the
  complete metadata preflight rather than discovering them after staging
  begins.
- **Acceptance:** Reject general-purpose bit 0, 6, or 13 with one stable
  content-silent category before exact-inventory validation, member reads,
  password handling, staging, or extraction output; retain valid unencrypted
  stored/deflated samples and the unchanged producer.
- **Boundary:** Private project release smoke only. No password, key source,
  decryption, raw ZIP parser, local-header comparison, metadata-authentication
  guarantee, content scanning, general archive sandbox, workflow, dependency,
  producer, runtime API, release authority, tag, release, publication, or real
  public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Research:** Python 3.12 documents ZIP decryption and password-bearing
  member reads; CPython's member-open path can reveal an encrypted member name
  and rejects strong encryption only at read time. The PKWARE ZIP Application
  Note assigns traditional encryption, strong encryption, and masked header
  values to general-purpose bits 0, 6, and 13.
- **Failing baseline:** The new M69 architecture file produced 7 failures and
  1 passing protected-surface guard in 0.52 seconds against exact M68 code.
  All three indicators reached staging, while the mask, validator, producer
  assertion, source ordering, decision, and docs were absent.
- **Local candidate:** The unchanged 46-package lock and restored 45-package
  CPython 3.12 graphics environment pass formatting for 312 files, Ruff,
  strict Pyright, strict docs, whitespace, 766 architecture/release assertions
  with 1 capability skip, 10 real-wgpu tests, both five-repeat profiles, both
  vertical slices, all four diagnostic benchmark validators, and complete
  package/release smoke.
- **Supported Python:** CPython 3.12.13 passes 2,304 tests with 15 skips;
  CPython 3.13.13 and 3.14.5 each pass 2,294 with 16 skips. Two initial 3.14
  attempts were not counted because environment/cache writes exhausted
  storage; pruning only disposable validation outputs and disabling pytest's
  nonessential cache produced the clean final result.
- **Artifacts:** Two builds reproduce a pure 273,229-byte wheel at
  `bba4773ecedf1b2c749daa7e8d930da482ed040df8e7d4e25a68e4a8127d66de`
  and a 1,206,202-byte source archive at
  `22420057c1c8d7c6283666501a05f596461a3505c2ac4425bee07463caeaa3bd`.
  Installed-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. The wheel has 94 entries, the sdist 504 including one
  M69 test/RFC, and the 50-member sample has no encryption indicator; no
  inspected archive contains native/WASM content.
- **Review:** The pre-publication findings-first review strengthened fail-
  before-inventory proof. Hosted review then correctly found that encryption
  validation shared the per-member metadata loop, so an unsafe earlier member
  could mask an encrypted later member. A dedicated all-member flag pass now
  precedes every per-member metadata check, and an order-adversarial regression
  requires the stable encrypted-member category.
- **Reviewed artifacts:** Two record-inclusive builds reproduce the same pure
  273,229-byte wheel and a 1,207,763-byte source archive at
  `54cc3fd021dfc120cf51fc7d3db31a3a3054b345c7a09547d7e6982298a9a671`;
  installed-wheel and release smoke pass. This factual update changes the
  source archive afterward, so exact commit-tree identity remains delegated to
  hosted qualification.
- **Initial hosted gate:** PR #159 exact initial head `c4b7729` passed run
  `31590079286` in three Linux-first allocations. Linux passed in 7m10s,
  macOS in 2m31s, and Windows in 4m07s. All supported-Python, real-wgpu,
  profile, vertical-slice, reproducibility, wheel, staging, and release-smoke
  gates passed. This head is superseded by the review correction and is not a
  merge candidate.
- **Corrected local gate:** The unchanged lock, all 312 formatted files, Ruff,
  strict Pyright, 76 focused M64-M69 assertions with 1 capability skip, 2,305
  complete CPython 3.12 tests with 15 skips, 767 architecture/release
  assertions with 1 skip, strict docs, whitespace, two-build reproducibility,
  installed-wheel smoke, deterministic staging, and complete release smoke
  pass. The corrected build retains the 273,229-byte wheel and produces a
  1,208,657-byte source archive at
  `85d8cc5f2d9cb9ecedc763176abb428726c8eab76e4c59e3b885e03b6df3ff6f`.
- **Next gate:** Commit and push the DCO-signed correction, qualify the exact
  updated head through the existing three-allocation Linux-first hosted gate,
  then answer and resolve the review thread only with exact passing evidence.
