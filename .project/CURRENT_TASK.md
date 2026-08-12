# Current Task

- **Task:** M68 - bounded sample-archive container admission
- **Status:** Feature PR #156 and integration-record PR #157 are fully
  validated, twice audited, squash-integrated, and verified. This exact three-
  record closeout establishes the clean M69 selection base without requesting
  hosted CI.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact synchronized M67 closeout
  `ea3de73f5ef1792df729c1f271b3d84a28db1028`, tree
  `feed6f892798f0030974c957fa6b5f1352c8b53c`.
- **Outcome:** Bound the sample ZIP container before standard-library archive
  parsing while retaining the existing M64-M67 extraction policies.
- **Acceptance:** Reject an obvious non-regular or over-16-MiB source before
  opening; revalidate the opened descriptor before `ZipFile`; parse through
  that same handle; fail content-silently before parser or staging side effects;
  close the handle on success and failure; and preserve the unchanged producer,
  workflows, runtime, dependencies, version, and public package surface.
- **Boundary:** Private project release smoke only. No raw ZIP parser, general
  archive sandbox, immutable-input guarantee, concurrent filesystem isolation,
  content scanning, workflow, dependency, producer, runtime API, release
  authority, tag, release, publication, or real public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Research:** Focused primary-source review of Python 3.12 `zipfile` and the
  OWASP File Upload Cheat Sheet supports complementary compressed-input and
  expanded-output limits plus one seekable file-handle identity. The 16 MiB
  private cap is over 150 times the exact 111,168-byte project sample bundle.
- **Failing baseline:** The new M68 architecture file produced 6 failures and 2
  passing guards in 0.34 seconds against exact M67 code. The cap/helper were
  absent, invalid sources reached the parser, valid parsing reopened the path,
  and source ordering was absent.
- **Local candidate:** The unchanged 46-package lock and restored 45-package
  CPython 3.12 graphics environment pass whole-tree formatting for 311 files,
  Ruff, strict Pyright, strict docs, and whitespace. The pre-review complete
  suites passed 2,295 tests with 15 skips on CPython 3.12 and 2,285 with 16
  skips on CPython 3.13/3.14. Ten real-wgpu tests, both five-repeat profiles,
  both vertical slices, and all four diagnostic benchmark validators pass.
- **Review:** Findings-first review identified that descriptor-only admission
  could block while opening a FIFO or surface a directory-open failure before
  the stable non-regular category. A pre-open path-metadata check now rejects
  obvious invalid sources; descriptor revalidation remains authoritative after
  open. The strengthened M64-M68 contract passes 67 assertions with 1 local
  symlink-capability skip on CPython 3.12, 3.13, and 3.14. The corrected full
  CPython 3.12 suite passes 2,296 tests with 15 skips.
- **Pre-review artifacts:** Two builds reproduced a pure 273,082-byte wheel at
  `089c787bd156e3af5f36fa20dbab1a69e953cc913b9367d9b023e1ccb18977fe`
  and a 1,198,756-byte source archive at
  `f135564122dacca5e3cd3c10e20005a7d40e4a9eda774b00a2771bb036d23f68`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke
  passed. The sample ZIP is exactly 111,168 bytes, contains 50 files, and has
  SHA-256 `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`.
  A record-inclusive rebuild also reproduced a pure 273,106-byte wheel at
  `685c3baaa66ed325c471b5deb5f3f44590eb1bbc2c177ebdd53bc39366119c22`
  and a 1,200,373-byte source archive at
  `5d1bcb8424c13145977d53484a164457911ddfeb7d0e6e972e27399708afeaeb`;
  installed-wheel and complete release smoke passed again. This factual update
  changes the source archive afterward, so exact commit-tree artifact identity
  remains delegated to hosted qualification.
- **Hosted evidence:** Ready PR #156 exact DCO head
  `0fbccca248e6a00a79631ca12c2afa6e7b9acdac`, tree
  `7e03726ebea72d074e0404f6c8073f96e0e8cce5`, passed run `31585838550`
  in exactly three Linux-first allocations. Linux passed in 7m34s; only then
  macOS and Windows began and passed in 2m58s and 4m13s. Baseline and every
  compatibility suite passed 2,301 tests with one compatibility skip; all
  real-wgpu, profile, vertical-slice, reproducibility, installed-wheel, staging,
  and complete release-smoke gates passed.
- **Hosted artifacts:** Two exact-head builds reproduced a pure 273,092-byte
  wheel at
  `85378f6485a06a8e1496e775fa8f71b122a899bdd0731ba3d67e1eda0f06db58`
  and a 1,200,886-byte source archive at
  `d1ac76ec6d3e62be894e894a862fbde09fa0aca07b58a8277b2ea33f96fdc977`.
- **Hosted review:** Two delayed exact-head audits found no comment, review, or
  unresolved thread. PR #156 remained clean, mergeable, exact-head, and exact-
  base before integration.
- **Feature integration:** PR #156 squash
  `5bd0196128aeffcf21094d0a0c6d78b624aaf49b` has the exact reviewed tree,
  sole parent M67 closeout, valid GitHub signature verified at
  `2026-08-12T10:19:22Z`, and exact DCO trailer. The feature branch is deleted
  remotely and locally.
- **Integration gate:** Change exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`;
  request only the existing documentation-qualified Linux allocation and a
  skipped zero-step desktop umbrella; then create a three-record closeout that
  requests no hosted runner. Delete every remaining M68 branch and generated
  output after verified integration.
- **Integration local evidence:** The exact four-file record passes the
  unchanged lock, formatting for 311 files, Ruff, strict Pyright, all 758
  selected architecture/release-artifact assertions with 1 local capability
  skip, strict docs, whitespace, full Git-object checking, two-build
  reproducibility, installed-wheel smoke, ten-artifact staging, and complete
  M68 release smoke. The pure 273,106-byte wheel remains feature-identical;
  exact integration-commit sdist identity is delegated to the hosted gate.
- **Integration hosted evidence:** Exact four-file head
  `cd65d1345b2725eb3be4daeb899535eacb740dee`, tree
  `83e765ba0fa92038aeefaaf2dcf9d2fb85eec052`, passed run `31587335592`
  in one 43-second Linux allocation; the desktop umbrella skipped with zero
  steps. Hosted formatting, Ruff, strict docs, 757 documentation-selected
  architecture assertions, reproducibility, installed-wheel smoke, staging,
  and complete M68 release smoke passed.
- **Integration hosted artifacts:** Two builds reproduced the feature-identical
  pure 273,092-byte wheel at
  `85378f6485a06a8e1496e775fa8f71b122a899bdd0731ba3d67e1eda0f06db58`
  and a record-updated 1,202,598-byte source archive at
  `32d390922dbfc9a62eb19fdf0ea4f35f6817a2da7c676534d6849bafbee3cc6e`.
- **Integration review:** Two delayed exact-head audits found no comment,
  review, or unresolved thread. PR #157 remained clean, mergeable, exact-head,
  and exact-base before squash integration.
- **Integration squash:** PR #157 squash
  `69fe032bfa0af6513d46e7c7492ffa3a5720d163` has the exact reviewed tree,
  sole parent feature squash, valid GitHub signature verified at
  `2026-08-12T10:28:06Z`, and exact DCO trailer. The integration branch is
  deleted remotely and locally.
- **Closeout gate:** Change exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`; run architecture,
  strict docs, scope, Git-object, and whitespace checks; create a DCO-signed
  ready PR that requests no hosted runner; verify its squash; delete every M68
  branch locally/remotely; remove only verified generated outputs; and leave
  synchronized clean `main` before selecting M69.
- **Closeout local evidence:** The exact three-file record passes all 756
  architecture assertions with 1 local capability skip, strict docs,
  whitespace, full Git-object checking, and exact scope. It changes no
  workflow, runtime, verifier, producer, dependency, package, test, public-doc,
  or roadmap surface and is excluded from CI by the existing path policy.
