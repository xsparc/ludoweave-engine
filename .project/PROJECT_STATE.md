# Project State

## M99 local-header CRC-32 consistency preflight - feature integrated; integration record active

- Base: exact verified M98 closeout squash
  `6d4529efb0476f3e3e45f78204d2b0aa192da018`, tree
  `7e3ffae0423fd2b4da1725db48864b9c04f8ad35`; local branch, local `main`, and
  `origin/main` were exact with divergence `0 0`, a clean worktree, only
  `main` present, and no open PR before M99.
- Selected policy: after M98, read exactly four bytes at each public
  `ZipInfo.header_offset + 14` and require equality with public central
  `ZipInfo.CRC` encoded unsigned little-endian before decoded names, metadata,
  exact inventory, staging, or reads. The stable content-silent error is
  `sample bundle local header CRC-32 values are inconsistent`.
- Primary-source basis: PKWARE APPNOTE 6.3.10 sections 4.1.5, 4.3.7, 4.3.12,
  and 4.4.7 define CRC-32 integrity and the duplicated four-byte field. Python
  documents public `ZipInfo.CRC` and `ZipInfo.header_offset`; CPython member
  reads use the central value as their expected CRC.
- Runtime gap: exact CPython 3.12.13, 3.13.13, and 3.14.5 each retained central
  CRCs `[3724039362, 2868864084]` and read both payloads after only the second
  local CRC changed from `2868864084` to `2868864085`.
- Red contract: the 29-assertion M99 contract is format/Ruff clean and strict
  Pyright reports zero findings. Exact CPython 3.14.5 passed 19 established
  runtime, precedence, producer, empty-archive, and protected-surface controls;
  ten stable-error, helper, cleanup, ordering, and documentation assertions
  failed because closed M98 has no M99 policy/helper/RFC. No complete pass is
  claimed.
- Implementation scope: one four-byte equality classifier after M98 plus
  RFC-0082 and aligned records. No CRC recomputation, size comparison, payload
  or next-header bound, inter-member layout policy, workflow, dependency,
  producer, runtime API, version, release authority, tag, release, or
  publication is added.
- First checkpoint correction: the implementation was Ruff-clean and strict
  Pyright-clean, but format check requested one mechanical reflow. Combined
  M98-M99 tests passed 55 of 57 because the helper used an equivalent named
  four-byte constant while the contract required the literal encoding and the
  non-scope phrase omitted a repeated `no`; strict docs also required RFC-0082
  navigation. The corrected presentation changes no runtime policy.
- Supported-runtime proof: all 57 combined M98-M99 assertions and strict docs
  pass. All 29 M99 assertions pass on exact CPython 3.12.13, 3.13.13, and
  3.14.5. Each complete suite passes 2,862 tests with 16 established skips in
  109.49, 106.57, and 112.30 seconds respectively.
- Local gate: the unchanged 46-package lock resolves in 0.90 milliseconds and
  the exact CPython 3.12.13 locked 45-package graphics environment installs.
  All 342 Python files are format clean; Ruff and strict Pyright pass; all
  1,332 architecture assertions pass with one established Windows capability
  skip in 10.89 seconds; strict docs build; the five metadata-hygiene plus 29
  focused M99 assertions pass; and whitespace is clean.
- Graphics/release proof: all ten real-wgpu tests pass in 6.31 seconds; both
  one-repeat profiles validate; Clockwork Arena and Agent World Builder retain
  canonical state/replay identities. Two fresh builds reproduce a 277,172-byte
  pure wheel at
  `99b11fdff73c87131b958abb41443b7c119dd3e6c2061df502c5965a647be29e`
  and a 1,438,223-byte source archive at
  `7c28281efdd4d9ab9f0da20479da1ae4fbfa1e60d7a73f2312ac4052e6286462`;
  isolated-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. Recording changes the source archive afterward.
- Findings-first review: exactly 15 intended paths change. The runtime diff is
  one two-constant/call/helper slice using public `ZipInfo.header_offset` and
  `ZipInfo.CRC`, with M98 precedence, stable content-silent error, snapshot
  restoration, and owned cleanup preserved. No workflow/release-workflow,
  lock, metadata, runtime package/API, sample producer, dependency, version,
  release authority, credential, backend/native/WASM, or development-tool-
  identity change was found. The 94-entry wheel is pure `py3-none-any`; it and
  the 564-entry source archive contain no banned native/WASM/bytecode/control
  metadata. No remaining actionable review finding exists.
- Review-inclusive artifacts: two fresh builds reproduce the 277,172-byte pure
  wheel at
  `99b11fdff73c87131b958abb41443b7c119dd3e6c2061df502c5965a647be29e`
  and the 1,439,136-byte source archive at
  `5171bd97e5f80c2906c88d075595a9dcf6c1be2bf5fd1e1ec79cf4d50dbf3c29`;
  isolated-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. Hosted exact-head artifacts will remain authoritative
  after factual record updates change the source archive.
- Post-record separator correction: lock, all static checks, strict docs, the
  34 metadata/M99 assertions, and whitespace passed, but the architecture run
  reported 1,331 passes, one established skip, and one M67 staging-directory
  rename `WinError 5`; no clean separator is claimed from that invocation. The
  exact assertion immediately passed in 0.21 seconds, then all 1,332
  architecture assertions passed with one skip in 9.20 seconds. No source
  correction was required.
- Final source separator: the unchanged lock resolved in 1 millisecond; all 342
  files remained format clean; Ruff and strict Pyright passed; all 1,332
  architecture assertions passed with one established skip in 9.59 seconds;
  strict docs built in 1.47 seconds; all 34 metadata/M99 assertions passed in
  0.88 seconds; and whitespace remained clean.
- Precommit audit: after fetch/prune, branch base, local `main`, `origin/main`,
  and merge base remain exact M98 closeout with divergence `0 0`. Exactly 15
  intended paths change; only `main` plus the neutral M99 branch exist locally
  and only `origin/main` remotely. Authentication is valid; open PR, M99 run,
  release, and tag queries are empty. Protected workflow, metadata, lock,
  runtime package, and producer surfaces have no diff; credential and explicit
  development-tool-identity scans are empty; Git has no corruption; and the
  M98 three-squash chain retains exact parents, trees, and valid signatures.
- Hosted feature proof: ready PR #249 exact DCO head
  `b3e1bc994e57fac2277e86b552d760f9ae9c90a1`, tree
  `77c40e7a27f70bc89e273225a8bb81966fc8dfa0`, passed run `32596930304`
  in exactly three allocations: Linux job `97089296631` in 7m20s, macOS job
  `97090165770` in 2m00s, and Windows job `97090165820` in 4m10s. Linux
  CPython 3.12 passed 2,877 tests; Linux 3.13/3.14 and macOS/Windows 3.14 each
  passed 2,877 with one established capability skip. All hosted graphics,
  profiles, vertical slices, and Linux static/build/release gates passed.
- Hosted repeat builds reproduced a 277,158-byte pure wheel at
  `232eaa8b23bbe6c5e0cf0fa5510521dadb175fae17baf893ff208695c061b76e`
  and a 1,439,905-byte source archive at
  `abaa619ce80968b3f49b3f0b25de6b9c075baf3d6de142e663e56f59c09701ae`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke
  passed.
- Two separated readiness audits around 34 passing local assertions retained
  exact head/tree/base, one DCO commit, 15 paths, three successful checks from
  one exact-head run, `MERGEABLE/CLEAN`, and zero feedback. Guarded squash
  `909b7568fe98da9a77d226df57eb17a7571a68e5` has the exact qualified tree,
  sole parent M98 closeout, standalone DCO, and a valid GitHub signature
  verified at `2026-08-22T20:44:55Z`. The feature branch is deleted remotely.
- The integration record changes exactly five factual project/roadmap files;
  no runtime, public API, test, workflow, build, dependency, version,
  release-authority, tag, release, or publication surface changes.
- Integration-record environment correction: the first full gate used
  `uv sync --all-groups` without the optional graphics extra, which removed six
  locked graphics packages and caused 17 expected unresolved-import/type
  findings. Architecture still passed 1,332 assertions with one established
  skip; docs, metadata, and whitespace passed. No clean complete-gate claim is
  made from that invocation and no source correction was required.
- Corrected integration-record proof: restoring the unchanged locked graphics
  extra installed the six packages. All 342 Python files remained format
  clean; Ruff passed; strict Pyright reported zero findings; all 1,332
  architecture assertions passed with one established skip in 9.92 seconds;
  strict docs built in 1.47 seconds; all five metadata assertions passed in
  0.33 seconds; and whitespace passed.
- Two fresh integration-record builds reproduce a 277,190-byte pure wheel at
  `868c9abf5e7137142fe4d9072d0c6639481025bfd8fc55a38800fb11662a914f`
  and a 1,440,146-byte source archive at
  `d7a8e21cd7ad116eb109dc69da7425de16d0bb291ba6a5b03d17078961c1669e`;
  isolated-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. Recording this evidence changes the source archive;
  hosted integration-head identities will remain authoritative.
- Final integration-record source separator: all 342 Python files remained
  format clean; Ruff passed; strict Pyright reported zero findings; all 1,332
  architecture assertions passed with one established skip in 9.79 seconds;
  strict docs built in 1.45 seconds; all five metadata assertions passed in
  0.34 seconds; and whitespace passed.
- Integration-record precommit audit: branch base, local and remote `main`, and
  merge base are exact feature squash
  `909b7568fe98da9a77d226df57eb17a7571a68e5` with divergence `0 0`.
  Exactly five factual paths change; only `main` and the neutral integration
  branch exist locally and only `origin/main` remotely. Open PR, branch-run,
  feature-squash postmerge-run, release, and tag queries are empty. Protected
  code/workflow/dependency surfaces have no diff; credential and explicit
  development-tool-identity scans are empty; no retired control path is
  tracked; Git has no corruption and only expected historical dangling
  objects; the feature squash retains exact tree, parent, DCO, and valid
  signature; and whitespace is clean.
- Final integration post-audit separator: strict docs built in 1.49 seconds;
  all five metadata assertions passed in 0.33 seconds; exactly five paths
  remain changed; and whitespace is clean.

## M98 local-header timestamp consistency preflight - complete and closed

- Base: exact verified M97 closeout squash
  `9f4a3b915df40fe86a0fc5c759763186899ea1fe`, tree
  `678b6ff58513952a23041e6594fc621e71e9537b`; local branch, local `main`, and
  `origin/main` were exact with divergence `0 0`, a clean worktree, and no open
  PR before M98 edits.
- Accepted policy: after M97, read exactly four bytes at each public
  `ZipInfo.header_offset + 10` and require equality with the DOS time/date bytes
  represented by public central `ZipInfo.date_time` before decoded names,
  metadata, exact inventory, staging, or reads. The stable content-silent error
  is `sample bundle local header timestamps are inconsistent`.
- Primary-source basis: PKWARE APPNOTE 6.3.10 sections 4.3.7, 4.3.12, and 4.4.6
  define the duplicated two-byte DOS time and two-byte DOS date fields. Python
  documents `ZipInfo.date_time` as the central-directory result and
  `ZipInfo.header_offset` as the local-header byte offset; the documented tuple
  represents local time rather than UTC and has two-second precision.
- Runtime gap: exact CPython 3.12.13, 3.13.13, and 3.14.5 each retained central
  tuples `[(2026, 8, 23, 4, 6, 8), (2026, 8, 23, 4, 6, 8)]`, observed local
  timestamp hex `c420175d` and mutated `e420175d`, and read both payloads after
  only the second local time's low byte changed.
- Probe correction: the first sandboxed uv invocations were blocked before
  execution by user-cache access, and the first formatter check requested one
  mechanical reflow while Ruff lint passed. Corrected escalated exact-runtime
  probes passed, then the formatted probe passed both static checks.
- Red contract: the first static gate requested one mechanical reflow while
  Ruff and strict Pyright passed. After formatting, all three static gates
  passed. Exact CPython 3.14.5 then collected 28 assertions: 18 inherited
  precedence, behavior, producer, empty-archive, and protected-surface controls
  passed; ten stable-error, helper, cleanup, ordering, and documentation
  assertions failed because unchanged M97 had no M98 policy/helper/RFC. No
  complete or hosted pass is claimed.
- Implementation scope: one four-byte classifier after M97 plus RFC-0081 and
  aligned records. No timestamp semantics, timezone/UTC conversion, CRC/size
  comparison, inter-member layout policy, workflow, dependency, producer,
  runtime API, version, release authority, tag, release, or publication is
  added.
- Review correction: findings-first review closed the stale historical M97
  state with its already verified closeout facts and made RFC-0081 explicitly
  place APPNOTE's bit-13 masked-local-header exception outside the admitted
  profile because established encryption policy rejects that bit before M98.
  Runtime policy is unchanged.
- Local proof: all 28 M98 assertions pass on exact CPython 3.12.13, 3.13.13,
  and 3.14.5. Each complete suite passes 2,833 tests with 16 established skips.
  The unchanged lock and exact 45-package graphics environment, all 341-file
  format/Ruff checks, strict Pyright, 1,303 architecture assertions with one
  established Windows skip, strict docs, metadata hygiene, ten real-wgpu
  tests, both profiles, Clockwork Arena, Agent World Builder, and whitespace
  gates pass.
- Artifact proof: two review-inclusive fresh builds reproduce the 277,048-byte
  pure wheel at
  `2f69ece3b54e5fe6daccb1bcc3a4e75e0944e09a5fb7adc7d894d9fda4620c5c`
  and the 1,430,987-byte source archive at
  `4e8183c04fb637e4cfad3bfc96868cbfdf82607281fb24262bd5753ccc581822`;
  isolated-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass. Hosted exact-head artifacts will remain authoritative
  after recording changes the source archive.
- Precommit audit: remote refresh retains exact M97 closeout branch/main/
  origin/merge-base identity with divergence `0 0`; exactly 16 intended paths
  change. Only `main` plus the neutral M98 branch exist locally and only
  `origin/main` remotely; open PR, branch-run, release, and tag queries are
  empty. The M97 three-squash sole-parent/tree/signature chain is exact;
  protected surfaces, credential/identity scans, repository integrity, and
  whitespace are clean.
- Hosted feature proof: ready PR #246 exact DCO head
  `403c050224262563f5a7e77d17d7cbfa62732420`, tree
  `65e83878ffb50e5c654ba3b4e7e53fb60458b9dd`, passed run `32593756442`
  in exactly three allocations: Linux job `97081449858` in 7m27s, macOS job
  `97082337246` in 2m01s, and Windows job `97082337331` in 3m58s. Linux
  CPython 3.12 passed 2,848 tests; Linux 3.13/3.14 and macOS/Windows 3.14 each
  passed 2,848 with one established capability skip. All hosted graphics,
  profiles, vertical slices, and Linux static/build/release gates passed.
- Hosted repeat builds reproduced a 277,044-byte wheel at
  `02fe38271e0f0b450f4fe6a63d0fd759ac3bdb04b662d0283ab7d5cf81dad6d3`
  and a 1,431,495-byte source archive at
  `4ea71905c2a49a6de6898209f75e83f0560ee25d192cb98ce18b3c6813ce28cb`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke
  passed.
- Two separated readiness audits around 33 passing local assertions retained
  exact head/tree/base, one DCO commit, 16 paths, three successful checks from
  one exact-head run, `MERGEABLE/CLEAN`, and zero feedback. Guarded squash
  `f89fdbb733925344b8d362b60db035d7df575687` has the exact qualified tree,
  sole parent M97 closeout, standalone DCO, and a valid GitHub signature
  verified at `2026-08-22T19:40:48Z`. The feature branch is gone remotely and
  locally.
- The integration record changes exactly five factual project/roadmap files;
  no runtime, public API, test, workflow, build, dependency, version, release-
  authority, tag, release, or publication surface changes.
- Integration-record local proof: the unchanged 46-package lock and all 45
  locked graphics packages check; repository-wide format, Ruff, strict
  Pyright, all 1,303 architecture assertions with one established skip, strict
  docs, metadata hygiene, and whitespace pass. Two fresh builds reproduce a
  277,048-byte pure wheel at
  `34c85047b916137edd24feea97d3c393f1f253007e5041a9bd69da1c2aa66855`
  and a 1,432,079-byte source archive at
  `83b810345e63f66925bebacd651c4a6fc8d0057a30d1def4bc5e81d23df5d830`;
  isolated-wheel, staging, and complete release smoke pass.
- Integration-record precommit audit: branch base, local and remote `main`,
  and merge base are the exact feature squash with divergence `0 0`. Exactly
  five factual paths change; open PR, branch-run, postmerge-run, release, and
  tag queries are empty. Protected code/workflow/dependency surfaces have no
  diff, credential/identity scans are empty, Git has no corruption, and
  whitespace is clean.
- Integration-record review correction: the first exact-head hosted run passed
  its one Linux documentation-class allocation, but review found the handoff
  status still said its already recorded precommit audit remained. The status
  now distinguishes completed local/precommit/initial-hosted proof from the
  amended-head requalification still required. Runtime policy and public
  documentation are unchanged.
- Corrected integration-record hosted proof: ready PR #247 exact DCO head
  `ab7378aae45e620afeedf737f16b3c65af8a0ef8`, tree
  `1ab4b10f8665fb7edb376d8bd45315735d980ec2`, passed exact-head run
  `32595002867` in one 44-second Linux allocation; the desktop placeholder
  skipped without allocating a runner. Strict docs built in 2.01 seconds; all
  1,304 architecture assertions, reproducible distribution, isolated-wheel
  smoke, deterministic ten-artifact staging, and complete release smoke passed.
- Hosted repeat builds reproduced a 277,034-byte wheel at
  `eca01f9e9ed31a6d625583348e902adb55b6110f48a67cd82042c8313c415378`
  and a 1,432,942-byte source archive at
  `194fe3349cfc19b8aa5c576f5999631dc5754bbe9ebd2e2baee6710d80bf9f35`.
- Two separated corrected-head audits retained exact head/tree/base, one DCO
  commit, five paths, one exact-head successful run, and `MERGEABLE/CLEAN`.
  The one corrected review thread was resolved and outdated; there were zero
  unresolved threads or issue comments.
- Integration-record PR #247 merged at `2026-08-22T19:54:44Z` as verified
  squash `0225660c0b24ca4a5831adf96b20b0cb922d2754`. It has the exact
  qualified tree, sole M98 feature-squash parent, standalone DCO trailer, and a
  valid GitHub signature verified at `2026-08-22T19:54:43Z`. The integration
  branch is deleted remotely and locally; only `main` plus the closeout branch
  exist locally and only `origin/main` remotely.
- Closeout precommit proof: exactly three factual `.project` paths change; all
  five metadata-hygiene assertions and whitespace pass. Branch base, local
  `main`, `origin/main`, and merge base are exact integration squash with
  divergence `0 0`. Open PR, closeout-branch run, integration-squash run,
  release, and tag queries are empty. Protected source, tests, scripts, docs,
  workflows, dependencies, README, and roadmap have no diff; Git integrity and
  the integration squash's parent/tree/DCO/signature remain exact.
- Closeout proof: ready PR #248 exact DCO head
  `7e06f6897a5c58431b278a9ed7f9a1ac6e1b1960`, tree
  `7e3ffae0423fd2b4da1725db48864b9c04f8ad35`, allocated no workflow and passed
  two separated readiness audits around five metadata-hygiene assertions with
  zero feedback. It squash-merged at `2026-08-22T19:59:48Z` as
  `6d4529efb0476f3e3e45f78204d2b0aa192da018`, with exact tree, sole
  integration-record parent, standalone DCO, and valid GitHub signature.
- Final audit: local `main` and `origin/main` are exact with only `main`
  locally/remotely; open PR, closeout run, closeout-squash run, release, and tag
  queries are empty. The M98 feature/integration/closeout squash chain retains
  exact parents, trees, DCO, and valid signatures. All 12 M98 `.tmp` targets
  and ten exact M98 pytest directories were descendant-verified inside their
  intended workspace roots and removed; none remain. Metadata hygiene passes.

## M97 local-header extraction-version consistency preflight - complete and closed

- Base: exact verified M96 closeout squash
  `bb1867f8cc2cd1e7a5cb56cc596761284e7dea42`, tree
  `27b7b4968c64816dcc39a20e01c0410d4e11c78e`; local and remote `main` were
  exact with only `main` present before creating the neutral M97 branch.
- Accepted policy: after M96, read exactly two bytes at each public
  `ZipInfo.header_offset + 4` and require equality with public central
  `bytes((info.extract_version, info.reserved))`. Mismatch raises stable
  content-silent `sample bundle local header extraction versions are
  inconsistent` before decoded-name policy, metadata, exact inventory,
  staging, or reads. The helper restores position and existing ownership
  closes resources.
- Direction evidence: PKWARE defines the duplicated two-byte extraction-
  version pair. A corrected temporary probe on exact CPython 3.12.13, 3.13.13,
  and 3.14.5 showed local pairs `[(20, 0), (21, 0)]` can differ while central
  pairs remain `[(20, 0), (20, 0)]`, offsets remain `[0, 54]`, and both
  payload reads succeed.
- Red evidence: the 27-assertion M97 contract is format/Ruff clean and strict
  Pyright reports zero findings. On exact CPython 3.14.5 it passed 17
  established controls and failed ten expected missing-policy/helper/order/
  docs assertions. No M97 implementation or complete-suite pass is claimed
  from the red invocation.
- Implementation boundary: one two-byte local-extraction-version consistency
  classifier after M96 plus RFC-0080 and aligned records. No supported-version
  allowlist, minimum capability or reserved-byte policy, time/CRC/size or
  field-wide comparison, record/payload/next-header bound, inter-member layout
  validator, workflow, dependency, producer, runtime API, release authority,
  tag, release, or publication is admitted.
- Implementation checkpoint: after correcting one Markdown line wrap exposed
  by the focused contract, both affected Python files are format/Ruff clean,
  strict Pyright reports zero findings, all 53 combined M96-M97 assertions
  pass, and strict docs build. The 27-case M97 contract passes on exact CPython
  3.12.13, 3.13.13, and 3.14.5.
- Complete supported-Python proof: exact CPython 3.12.13, 3.13.13, and 3.14.5
  each pass 2,805 tests with 16 established skips. Repository-wide graphics,
  artifact, release, and findings-first qualification are complete.
- Local proof: the unchanged 46-package lock resolves and the exact CPython
  3.12.13 locked 45-package graphics environment is installed. Repository-wide
  formatting, Ruff, strict Pyright, all 1,275 architecture assertions with one
  established Windows skip, strict docs, metadata hygiene, real-wgpu, both
  profiles, Clockwork Arena, and Agent World Builder pass.
- Initial artifact proof: two fresh builds reproduced the 276,943-byte pure
  wheel at
  `23daeee5cbf95a9dd6c9232b8c35abfc7b42200dc9f6c3d5db3f1775aa6eafbc`
  and the 1,421,917-byte source archive at
  `724d9336e1b37c992f1465be03758d040a3f496dfa084a8ef2d0a98c165a452c`;
  wheel, staging, and complete release smoke pass. Later record/review
  corrections make this pre-final source-archive identity non-authoritative.
- Review correction: findings-first review moved the misplaced README M97
  paragraph after M96 and corrected "originating-system byte" to PKWARE's and
  `ZipInfo.reserved`'s reserved-byte meaning. Strict docs and all 58 affected
  metadata/M96/M97 assertions pass afterward. Corrected scope, credential,
  identity, protected-boundary, and archive-content scans have no finding
  across exactly 16 intended paths; the 94-entry wheel and 560-entry source
  archive contain no prohibited format or retired control metadata.
- Record-inclusive proof: repository-wide format, Ruff, strict Pyright, all
  1,275 architecture assertions with one established skip, strict docs,
  focused metadata/M97, and whitespace gates pass. Two fresh builds reproduce
  a 276,947-byte pure wheel at
  `5e0ace7e888b2bfe505ce82e8f10b47265f9a4e79232d8b038d29b2842d0c04a`
  and a 1,422,803-byte source archive at
  `75bbc3a6016c44e4a2adc9f46f3503cd9e05137db84c489adc62a7680a0fafbf`;
  isolated-wheel, ten-artifact staging, and complete release smoke pass.
  Hosted exact-head builds remain authoritative after this factual row changes
  the source archive.
- Precommit audit: after remote refresh, branch base, local and remote `main`,
  and merge base are exact M96 closeout with divergence `0 0`. Exactly 16
  intended paths change; only `main` and the neutral M97 branch exist locally
  and only `origin/main` remotely. Open PR, branch-run, release, and tag queries
  are empty. The M96 three-squash sole-parent/tree/DCO/signature chain is exact;
  workflow, dependency, producer, runtime package/API, and release-authority
  boundaries remain unchanged; credential and explicit development-tool-
  identity scans are empty; Git has no corruption; and whitespace is clean.
- Hosted feature proof: ready PR #243 exact DCO head
  `aa37212f4ec50c040fa39bfc98457133ab2744dd`, tree
  `8abe71ab97716a767517d211106281f25d20bb25`, passed run `32590870976`
  in exactly three allocations: Linux job `97074392026` in 7m26s, macOS job
  `97075313835` in 2m35s, and Windows job `97075313836` in 3m20s. Linux
  CPython 3.12 passed 2,820 tests; Linux 3.13/3.14 and macOS/Windows 3.14 each
  passed 2,820 with one established capability skip. All hosted graphics,
  profiles, vertical slices, and Linux static/build/release gates passed.
- Hosted repeat builds reproduced a 276,933-byte wheel at
  `39a2c02643778e823e119072a8c718cebb32f3bb3c7cc58a90981074b75e0326`
  and a 1,423,352-byte source archive at
  `e8a3ab4cb2c03b3ebb22ea284c50ca63d31e6ffe1e57fdeba96324c163d72090`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke
  passed.
- Two separated readiness audits around 32 passing local assertions retained
  exact head/tree/base, one DCO commit, 16 paths, three successful checks from
  one exact-head run, `MERGEABLE/CLEAN`, and zero feedback. Guarded squash
  `0f519c72c12d21e0a0001c21868bd0748c7d7b8c` has the exact qualified tree,
  sole parent M96 closeout, standalone DCO, and a valid GitHub signature
  verified at `2026-08-22T18:41:22Z`. The feature branch is gone remotely and
  locally.
- The integration record changes exactly five factual project/roadmap files;
  no runtime, public API, test, workflow, build, dependency, version, release-
  authority, tag, release, or publication surface changes.
- Integration-record local proof: the unchanged 46-package lock and all 45
  locked graphics packages check; repository-wide format, Ruff, strict
  Pyright, all 1,275 architecture assertions with one established skip, strict
  docs, metadata hygiene, and whitespace pass. Two fresh builds reproduce a
  276,935-byte pure wheel at
  `c98a6986f43db21cfddd645a976a4cade653f6c7adca1b0b319d99307cae60c1`
  and a 1,424,078-byte source archive at
  `c63339f89974c8f1be859d5f1958fcc5d7f780cb3efc842fc99db949c277e22c`;
  isolated-wheel, staging, and complete release smoke pass.
- Integration-record precommit audit: branch base, local and remote `main`,
  and merge base are the exact feature squash with divergence `0 0`. Exactly
  five intended factual paths change; only `main` plus the neutral record
  branch exist locally and only `origin/main` remotely. Open PR, branch-run,
  feature-squash postmerge-run, release, and tag queries are empty. Protected
  code/workflow/dependency surfaces have no diff, credential and explicit
  development-tool-identity scans are empty, Git has no corruption, and
  whitespace is clean.
- Hosted integration record: ready PR #244 exact DCO head
  `cd590e88befe44d4dbcfcdf8a700b4e4c0efd90b`, tree
  `881cf2cde38c5e833b2898b9fc652f0f116c08a7`, passed run `32591861207` in
  one 45-second Linux job `97076836696`; desktop umbrella job `97076933484`
  skipped with zero steps. Formatting, Ruff, strict docs, all 1,276 hosted
  documentation-architecture assertions, reproducible builds, installed-wheel
  smoke, ten-artifact staging, and complete release smoke passed.
- Hosted record artifacts: the 276,921-byte wheel SHA-256 is
  `cd857473dbe32729fe26ca30d6eb4f7ceac3431f927fe389c129af82e3d573d2`;
  the 1,424,470-byte source archive SHA-256 is
  `26d5de3ad8ddec68096e146c93db9f9c315af5f9b05efb2cf86592b2be755309`.
- Integration-record readiness/integration: two separated audits around five
  passing metadata assertions retained exact head/tree/base, one DCO commit,
  five paths, the successful bounded Linux gate, zero-step skipped desktop
  umbrella, `MERGEABLE/CLEAN`, and zero feedback. Guarded squash
  `e64264e2084b718b4f85338831ed806b088eb322` has the exact reviewed tree,
  sole parent the verified feature squash, standalone DCO, and a valid GitHub
  signature verified at `2026-08-22T18:51:16Z`. The branch is deleted locally
  and remotely.
- Closeout changes exactly three project records and adds no product, policy,
  workflow, dependency, build, version, release-authority, tag, release, or
  publication surface.
- Closeout local proof: all five metadata-hygiene assertions pass in 0.33
  seconds and whitespace is clean. Remote refresh retains exact integration-
  squash branch/main/origin/merge-base identity with `0 0` divergence, only
  `main` plus the necessary closeout branch locally and only `origin/main`
  remotely, and empty open-PR, branch-run, postmerge-run, release, and tag
  queries. The integration squash retains its exact tree/parent/DCO/signature;
  full Git checking reports no corruption and only historical dangling
  objects.
- Closeout integration: ready PR #245 exact DCO head
  `107f42537702bfd42e709c44b89ee6104211cdd9`, tree
  `678b6ff58513952a23041e6594fc621e71e9537b`, allocated no workflow. Guarded
  squash `9f4a3b915df40fe86a0fc5c759763186899ea1fe` has that exact reviewed tree,
  sole parent the verified integration-record squash, standalone DCO, and a
  valid GitHub signature verified at `2026-08-22T18:56:21Z`.
- Final M97 audit: local `main`, `origin/main`, and merge base were exact
  closeout with divergence `0 0`; only `main` remained locally/remotely, with
  no open PR, tag, release, or unexpected run. The feature/integration/closeout
  three-squash chain retained exact sole parents, trees, DCO trailers, and
  valid GitHub signatures. All 34 verified M97 scratch targets were removed,
  and five metadata-hygiene assertions passed in 0.34 seconds.

## M96 local-header extra-field consistency preflight - complete and closed

- Base: exact verified M95 closeout squash
  `e770f5538660b5edea5fd8ebc4fccf717b18b272`, tree
  `0f8e47c61c1e93147f6ba19c813c836dea514962`; local and remote `main` were
  exact with only `main` present before creating the neutral M96 branch.
- M95 final audit: closeout PR #239 exact DCO head
  `b595277463ac2303fa77d3b28bc8adac7ae38247`, tree
  `0f8e47c61c1e93147f6ba19c813c836dea514962`, allocated no workflow and
  squash-integrated as `e770f5538660b5edea5fd8ebc4fccf717b18b272` with sole
  integration-record parent, standalone DCO, and a valid GitHub signature.
  The feature/integration/closeout chain is exact and verified; only `main`
  remains, the worktree is clean, and all 35 verified M95 scratch targets are
  permanently removed.
- Accepted policy: after M95, use the already bounded local name and extra
  lengths to read each local extra field and require exact equality with public
  central `ZipInfo.extra`. Mismatch raises stable content-silent `sample bundle
  local header extra fields are inconsistent` before decoded-name policy,
  metadata, exact inventory, staging, or reads. The helper restores position
  and existing ownership closes resources.
- Direction evidence: PKWARE defines separate local and central extra fields.
  A clean temporary probe on exact CPython 3.12.13, 3.13.13, and 3.14.5 showed
  a second local extra `feca02006f21` can differ from central
  `feca02006f6b` while offsets remain `[0, 60]` and both payload reads succeed.
- Red evidence: after one mechanical format correction, the 26-assertion M96
  contract passed 16 established controls and failed ten expected missing-
  policy/helper/order/docs assertions. Ruff and strict Pyright were already
  clean; corrected formatting, Ruff, and strict Pyright pass. No M96
  implementation or complete-suite pass is claimed from the red invocation.
- Implementation boundary: one bounded local-extra equality classifier after
  M95 plus RFC-0079 and aligned records. No extra-field semantics parser, broad
  extra-field ban, new field-ID policy, version/time/CRC/size or field-wide
  comparison, record/payload/next-header bound, inter-member layout validator,
  workflow, dependency, producer, runtime API, release authority, tag, release,
  or publication is admitted.
- Implementation checkpoint: both affected Python files are format/Ruff clean,
  strict Pyright reports zero findings, all 51 combined M95-M96 assertions pass,
  and strict docs build. The 26-case M96 contract passes on exact CPython
  3.12.13, 3.13.13, and 3.14.5; all three complete suites pass 2,778 tests with
  16 established skips. Repository-wide and artifact qualification are
  complete.
- Local proof: repository-wide static/docs/architecture/metadata gates pass,
  including all 1,248 architecture assertions with one established Windows
  capability skip. Real-wgpu, both profiles, Clockwork Arena, Agent World
  Builder, reproducible builds, installed-wheel smoke, ten-artifact staging,
  and complete release smoke pass. Findings-first review found no actionable
  defect across exactly 16 intended paths.
- Artifact proof before record inclusion: two fresh builds reproduced the
  276,866-byte pure wheel at
  `c3da2a0d2171c15be3bb6b605c3a2e179d43cc4289db0abf9a4d7f14f5ff9237`
  and the 1,416,021-byte source archive at
  `5038283415a3ec49531ccccf7a99b596dbbb0dafcb4199ac6bc9390979d58b21`;
  wheel, staging, and complete release smoke passed. Archive review found 94
  wheel entries, 558 source entries, and zero prohibited identities or formats.
- Hosted feature proof: ready PR #240 exact DCO head
  `b876a27c099a03439b87710036ba05ec92627a84`, tree
  `23b0cd47d9e764fab09361d75e412a7a91517bbe`, passed run `32587635235`
  in exactly three allocations: Linux job `97066338343` in 7m04s, macOS job
  `97067195975` in 2m18s, and Windows job `97067196001` in 4m14s. Linux
  CPython 3.12 passed 2,793 tests; Linux 3.13/3.14 and macOS/Windows 3.14 each
  passed 2,793 with one established capability skip. All hosted graphics,
  profiles, vertical slices, and Linux static/build/release gates passed.
- Hosted repeat builds reproduced a 276,851-byte wheel at
  `525392485408079a242c42ce4be35c37ee2e43989f155abed566375ae36db66d`
  and a 1,416,453-byte source archive at
  `5275bbd6014c398eaf29910da1713d960beb1fb71e236361b1a4e324197a7f8e`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke
  passed.
- Two separated readiness audits around 31 passing local assertions retained
  exact head/tree/base, one DCO commit, 16 paths, three successful checks from
  one exact-head run, `MERGEABLE/CLEAN`, and zero feedback. Guarded squash
  `70ef2f635fd1f9b3c25a3b044a031a422280c57e` has the exact qualified tree,
  sole parent M95 closeout, standalone DCO, and a valid GitHub signature
  verified at `2026-08-22T17:37:48Z`. The feature branch is gone remotely and
  locally.
- The integration record changes exactly five factual project/roadmap files;
  no runtime, public API, test, workflow, build, dependency, version, release-
  authority, tag, release, or publication surface changes.
- Hosted integration record: ready PR #241 exact DCO head
  `cb857973e691f1ebeb3033f85e3cbc19f38286da`, tree
  `f7733170103bbecd3b0d2197bcca1590727de1d9`, passed run `32588669372` in
  one 44-second Linux job `97068888823`; desktop umbrella job `97068996000`
  skipped with zero steps. Formatting, Ruff, strict docs, all 1,249 hosted
  documentation-architecture assertions, reproducible builds, installed-wheel
  smoke, ten-artifact staging, and complete release smoke passed.
- Hosted record artifacts: the 276,833-byte wheel SHA-256 is
  `3f1954f30ea6f1e491d545634a531c0f378b9afb86a93c8bf665b5c4f2454e79`;
  the 1,417,175-byte source archive SHA-256 is
  `b890420fc7370d96c4333d6fedbbaa5613c815d705ab8f0175a50b22db9fe2f1`.
- Integration-record readiness/integration: two separated audits around five
  passing metadata assertions retained exact head/tree/base, one DCO commit,
  five paths, the successful bounded Linux gate, zero-step skipped desktop
  umbrella, `MERGEABLE/CLEAN`, and zero feedback. Guarded squash
  `74c3707f01b70348a4d47b2e9fccbd71da30fdf6` has the exact reviewed tree,
  sole parent the verified feature squash, standalone DCO, and a valid GitHub
  signature verified at `2026-08-22T17:47:12Z`. The branch is deleted locally/
  remotely.
- Closeout changes exactly three project records and adds no product, policy,
  workflow, dependency, build, version, release-authority, tag, release, or
  publication surface.
- Closeout local proof: all five metadata-hygiene assertions pass in 0.33
  seconds and whitespace is clean. Remote refresh retains exact integration-
  squash branch/main/origin/merge-base identity with `0 0` divergence, only
  `main` plus the necessary closeout branch locally and only `origin/main`
  remotely, and empty open-PR, branch-run, postmerge-run, release, and tag
  queries. Full Git checking reports no corruption and only historical dangling
  objects.
- Closeout integration: ready PR #242 exact DCO head
  `3fd9a45da4908365f57a08be4ab0ac05de073ee6`, tree
  `27b7b4968c64816dcc39a20e01c0410d4e11c78e`, allocated no workflow and
  squash-integrated as `bb1867f8cc2cd1e7a5cb56cc596761284e7dea42` with sole
  integration-record parent, standalone DCO, and a valid GitHub signature
  verified at `2026-08-22T17:52:05Z`. Local `main`, `origin/main`, and merge
  base are exact with divergence `0 0`; only `main` exists locally/remotely,
  no PR remains open, exactly the intended feature and integration-record runs
  exist, and all 33 verified M96 scratch targets are permanently removed.

## M95 local-header compression-method consistency preflight - complete and closed

- Base: exact verified M94 closeout squash
  `a19db05c096c6d22e5871373bc738d282516635c`, tree
  `82b7378fd5634202cf3d21e3fe8aa4590faea4d4`; local and remote `main` were
  exact with only `main` present before creating the neutral M95 branch.
- Accepted policy: after M94, compare each two-byte little-endian local
  compression method at `ZipInfo.header_offset + 8` with central
  `ZipInfo.compress_type`. Mismatch raises stable content-silent `sample bundle
  local header compression methods are inconsistent` before decoded-name
  policy, metadata, exact inventory, staging, or reads. The helper restores
  position and existing ownership closes resources.
- Direction evidence: PKWARE defines the duplicated two-byte fields. A clean
  temporary probe on exact CPython 3.12.13, 3.13.13, and 3.14.5 showed local
  method 0 can differ while central methods remain `[8, 8]`, offsets remain
  `[0, 54]`, and both payload reads succeed.
- Red evidence: after correcting one formatter request and 17 strict-Pyright
  findings from untyped parameter lambdas, the 25-assertion M95 contract passed
  15 established controls and failed ten expected missing-policy/helper/order/
  docs assertions. No M95 implementation or complete-suite pass is claimed
  from that red invocation.
- Implementation boundary: one fixed two-byte equality classifier after M94
  plus RFC-0078 and aligned records. No local extra-field comparison or parsing,
  version/time/CRC/size or field-wide comparison, method allowlist, record/
  payload/next-header bound, inter-member layout validator, workflow,
  dependency, producer, runtime API, release authority, tag, release, or
  publication is admitted.
- Local proof: all 49 combined M94-M95 assertions pass; the 25-case M95
  contract passes on exact CPython 3.12.13, 3.13.13, and 3.14.5; all three
  complete suites pass 2,752 tests with 16 established skips. Repository-wide
  static/docs/architecture/metadata, real-wgpu, profile, vertical-slice,
  reproducible-build, wheel, staging, and release gates pass after the recorded
  environment correction.
- Artifact proof before record inclusion: two fresh builds reproduced the
  276,765-byte pure wheel at
  `6b62c8e03a71304b1782b33d124dda9494019997364574a3c4ded19f881dbe8c`
  and the 1,409,347-byte source archive at
  `bd30131119d32fcfd4b9eb8f3e1d8bc16cb9a6e8d46b6b0b35730e5dd3df1601`;
  wheel, staging, and complete release smoke passed. Archive review found 94
  wheel entries, 556 source entries, and zero prohibited identities or formats.
- Hosted feature proof: ready PR #237 exact DCO head
  `311f4c4e141525f25b8cc64edd37b6413df2875b`, tree
  `a0a68132d1f3ca78e810cb79efd41659758b5339`, passed run `32584858990`
  in exactly three allocations: Linux job `97059599006` in 7m53s, macOS job
  `97060564461` in 2m02s, and Windows job `97060564405` in 3m13s. Linux
  CPython 3.12 passed 2,767 tests; Linux 3.13/3.14 and macOS/Windows 3.14 each
  passed 2,767 with one established capability skip. All hosted graphics,
  profiles, vertical slices, and Linux static/build/release gates passed.
- Hosted repeat builds reproduced a 276,751-byte wheel at
  `81db4ef5768dee617027ef04a8da5f725f1df00aa811353f9a9992cbaf7159b1`
  and a 1,410,436-byte source archive at
  `3bf0138f9aadd5bf0d5330f3337877e586504885858a91ee7ad17eea60597f93`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke
  passed.
- Two separated readiness audits around 30 passing local assertions retained
  exact head/tree/base, one DCO commit, 16 paths, three successful checks from
  one exact-head run, `MERGEABLE/CLEAN`, and zero feedback. Guarded squash
  `d0e4f1f59ba4347bbd9a403c4f0594e2243bf7c1` has the exact qualified tree,
  sole parent M94 closeout, standalone DCO, and a valid GitHub signature
  verified at `2026-08-22T16:42:14Z`. The feature branch is gone, synchronized
  `main` has `0 0` divergence, and no postmerge workflow ran.
- The integration record changes exactly five factual project/roadmap files;
  no runtime, public API, test, workflow, build, dependency, version, release-
  authority, tag, release, or publication surface changes.
- Hosted integration record: ready PR #238 exact DCO head
  `72e5da098c67f0cbf8a1bc6b6667cadb6e9a9d6e`, tree
  `4acdfa06f2a47656205e832b25cf5181b592a1b7`, passed run `32585810955` in
  one 49-second Linux job `97061881376`; desktop umbrella job `97061981113`
  skipped with zero steps. Formatting, Ruff, strict docs, all 1,223 hosted
  documentation-architecture assertions, reproducible builds, installed-wheel
  smoke, ten-artifact staging, and complete release smoke passed.
- Hosted record artifacts: the 276,737-byte wheel SHA-256 is
  `e4f104220bc5a7e247eaa2db2bb3eb701049a5a5fe1eb91ea1de68237051e329`;
  the 1,411,281-byte source archive SHA-256 is
  `6f63cd8ffc9050a7d1c2921619cb4e81b236d183ef28ee3a9d69503aeb16d8fa`.
- Integration-record readiness/integration: two separated audits around five
  passing metadata assertions retained exact head/tree/base, one DCO commit,
  five paths, the successful bounded Linux gate, zero-step skipped desktop
  umbrella, `MERGEABLE/CLEAN`, and zero feedback. Guarded squash
  `ddbeca5041dbac82e5e2004ed9fe3ee06371078b` has the exact reviewed tree,
  sole parent the verified feature squash, standalone DCO, and a valid GitHub
  signature verified at `2026-08-22T16:50:25Z`. The branch is deleted locally/
  remotely, synchronized `main` has `0 0` divergence, and no postmerge workflow
  ran.
- Closeout changes exactly three project records and adds no product, policy,
  workflow, dependency, build, version, release-authority, tag, release, or
  publication surface.
- Closeout local proof: all five metadata-hygiene assertions pass in 0.33
  seconds and whitespace is clean. Remote refresh retains exact integration-
  squash branch/main/origin/merge-base identity with `0 0` divergence, only
  `main` plus the necessary closeout branch locally and only `origin/main`
  remotely, and empty open-PR, branch-run, release, and tag queries. Full Git
  checking reports no corruption and only historical dangling objects.

## M94 local-header flag-consistency preflight - complete and closed

- Base: verified M93 closeout squash
  `1b189da618d2d2ea0b3208707ba209f81d1368cc`; local and remote `main` were
  exact with only `main` present before creating the neutral M94 branch.
- Accepted policy: after M93, compare each two-byte little-endian local general-
  purpose flag at `ZipInfo.header_offset + 6` with central `ZipInfo.flag_bits`.
  Mismatch raises stable content-silent `sample bundle local header flags are
  inconsistent` before decoded-name policy, metadata, exact inventory,
  staging, or reads. The helper restores position and existing ownership closes
  resources.
- Direction evidence: PKWARE defines the duplicated two-byte fields. A clean
  temporary probe on exact CPython 3.12.13, 3.13.13, and 3.14.5 showed local
  bit 0 can differ while central flags remain `[0, 0]`, offsets remain
  `[0, 54]`, and both payload reads succeed.
- Red evidence: the 24-assertion M94 contract passed 14 established controls
  and failed 10 expected missing-policy/helper/order/docs assertions. One
  mechanical format correction was then applied. No M94 implementation or
  complete-suite pass is claimed from that red invocation.
- Implementation adds only one two-byte comparison after M93 and RFC-0077 plus
  aligned records. All 46 combined M93-M94 assertions pass; the 24-case M94
  contract passes on all three exact supported interpreters; all three complete
  suites pass 2,727 tests with 16 established skips. Repository-wide static/
  docs/architecture/metadata, real-wgpu, profile, vertical-slice,
  reproducible-build, wheel, staging, and release gates pass. Exact-head hosted
  feature qualification and the bounded integration record are verified and
  squash-integrated, closed out, and cleaned.
  Findings-first review found no actionable defect; the record-inclusive wheel
  retained its exact byte identity and complete release smoke passed.
- Hosted feature proof: ready PR #234 exact DCO head
  `23ad66250455aab68e7478903b7f2238983406aa`, tree
  `96bd9000efbc473d09f0c75d83c5e1231621409e`, passed run `32581692977`
  in Linux 5m32s, macOS 2m59s, and Windows 4m22s. Hosted Linux CPython 3.12
  passed 2,742 tests; Linux 3.13/3.14 and macOS/Windows 3.14 each passed 2,742
  with one established skip. All real graphics/profile/vertical slices and
  Linux build/wheel/release smoke passed. Hosted repeat builds reproduced a
  276,592-byte wheel at `6167497499b5e87fac82007b9db3f2e30912229e64e9ca518e6e5a8d19b6d04d`
  and a 1,404,176-byte sdist at
  `57e87b11f0c5f6b16eb1c6351ca5770896a479e1585eccda268d01ca40f6cf36`.
- Two separated readiness audits found no comment, review, or thread and
  retained exact head/tree/base plus three successful checks. Guarded squash
  `7974b6fc110f995cac25f7d69d9c48b55013a764` has the exact qualified tree,
  sole parent M93 closeout, standalone DCO, and a valid GitHub signature. The
  feature branch is gone, main is exact, and no postmerge workflow ran.
- The integration record changes exactly five factual project/roadmap files;
  no runtime, public API, test, workflow, build, dependency, version, release-
  authority, tag, release, or publication surface changes.
- Hosted integration record: ready PR #235 exact DCO head
  `77e14ca27eb8cf28fb19787647f7580f5488a4e9`, tree
  `3023d335b15b2e9f6839365551c10d4a8c9b988d`, passed run `32582755728` in
  one 49-second Linux job `97054488280`; desktop job `97054590470` skipped
  with zero steps. Formatting, Ruff, strict docs, all 1,198 hosted
  documentation-architecture assertions, reproducible builds, installed-wheel
  smoke, ten-artifact staging, and complete release smoke passed.
- Hosted record artifacts: the 276,592-byte wheel retained feature SHA-256
  `6167497499b5e87fac82007b9db3f2e30912229e64e9ca518e6e5a8d19b6d04d`;
  the 1,404,994-byte source archive SHA-256 is
  `e6ee886bee2ab5cfbd41019ac48264fe95b9008ad547bc494393075fb33cb4af`.
- Integration-record readiness/integration: two separated audits around five
  passing metadata assertions retained exact head/tree/base, one DCO commit,
  five paths, the successful bounded Linux gate, zero-step skipped desktop
  umbrella, `MERGEABLE/CLEAN`, and zero feedback. Guarded squash
  `f2c5c7865ba1cad42f8dc625f8da0895ca8f0b90` has the exact reviewed tree,
  sole parent the verified feature squash, standalone DCO, and a valid GitHub
  signature. The branch is deleted locally/remotely, synchronized `main` has
  `0 0` divergence, and no postmerge workflow ran.
- Closeout changes exactly three project records and adds no product, policy,
  workflow, dependency, build, version, release-authority, tag, release, or
  publication surface.
- Closeout local proof: all five metadata-hygiene assertions pass in 0.34
  seconds; whitespace passes; and full Git checking reports no corruption with
  only expected squash-era dangling objects. Remote refresh retains exact
  integration-squash branch/main/origin/merge-base identity, `0 0` divergence,
  only `main` plus the necessary local closeout branch, only remote `main`, and
  empty open-PR, exact-branch-run, release, and tag queries.
- Boundary: no local compression-method or extra-field comparison, broad flag
  allowlist, version/time/CRC/size or field-wide comparison, payload/next-header
  bound, inter-member layout validator, archive repair, general archive
  sandbox, workflow/dependency/producer/runtime/release-authority change, tag,
  release, or publication.

## M93 local-header name-consistency preflight - complete and closed

- Base: exact verified M92 closeout squash
  `74972042525041e9251ce245a1fd4ea75add6047`, tree
  `d8c44c6639914c8a833e364d8600eb0ae7fedc8e`. Synchronized `main` was the
  only local/remote branch; there was no open PR, current-head run, tag,
  release, tracked identity-control path, or M92 generated target. Thirty-eight
  verified M92 temporary targets were removed, and full Git checking reported
  no corruption.
- Gap: changing only the second local name from `second.txt` to the same-length
  `second.txu` leaves central names `first.txt`/`second.txt` and offsets
  `[0, 46]` visible. Exact CPython 3.12.13, 3.13.13, and 3.14.5 read the first
  payload and defer public `BadZipFile` until the malformed second member
  opens.
- Decision: after every policy through M92, private complete release smoke
  reconstructs each parser-exposed central `orig_filename` as UTF-8 under
  central bit 11 and CP437 otherwise, then requires exact equality with the
  already bounded raw local name. The stable error is
  `sample bundle local header names are inconsistent`.
- Boundary: one raw local-name consistency classifier only. It performs no
  local-flag comparison, extra-field comparison or parsing, field-wide
  local/central consistency, next-header or payload bound, complete record
  extent, gap/adjacency/contiguity/non-overlap policy, inter-member layout
  validation, archive repair, workflow, dependency, producer, runtime API, or
  release authority. It is not a general archive sandbox or a real public
  release observation.
- Direction proof: PKWARE APPNOTE 6.3.10 sections 4.3.2 and 4.3.7 require
  corresponding local/central records and place the variable name after the
  fixed local prefix; Appendix D specifies CP437 by default and UTF-8 under bit
  11. Python documents the same metadata encoding precedence and public
  `flag_bits`/`header_offset`. CPython 3.14 defers its decoded local/central
  name comparison until member open; M93 uses no private names.
- Probe: the format/Ruff-clean temporary behavior probe produced the same
  structural result on exact supported CPython 3.12.13, 3.13.13, and 3.14.5.
- Red baseline: the first static-clean contract estimate named 22 cases but
  collected 21, passing 13 controls and failing eight missing-policy
  assertions in 0.32 seconds; no authoritative claim is made from it. An
  explicit UTF-8 mismatch corrects the contract to 22 cases. The corrected
  format/Ruff/Pyright-clean contract passes 13 inherited controls and fails
  nine missing stable-error, helper, cleanup, source-order, and documentation
  assertions in 0.35 seconds. No complete pass is claimed.
- Implementation: release smoke now compares raw local names immediately after
  M92. RFC-0076 and aligned public records define the narrow rule and explicit
  nonclaims. The corrected combined checkpoint passes all 44 M92-M93
  assertions; affected Python is format/Ruff clean, strict Pyright reports zero
  findings, and strict docs build.
- Supported proof: the 22-case M93 contract passes on exact CPython 3.12.13,
  3.13.13, and 3.14.5. Corrected complete suites pass 2,703 tests with 16
  established skips on each runtime. The first 3.12 suite correctly exposed a
  retired-marker record phrase and two stale M72/M73 error-precedence
  assertions; narrow corrections preserve the older parser/decoder categories
  while asserting M93's earlier raw-name precedence.
- Static/architecture proof: the unchanged 46-package lock resolves and the
  locked 45-package graphics environment is restored. All 336 Python files are
  format/Ruff clean; strict Pyright reports zero findings; all 1,173
  architecture assertions pass with one established Windows capability skip;
  strict docs, five metadata assertions, and whitespace pass.
- Graphics/slices proof: all ten real-wgpu tests pass in 6.37 seconds; one-
  repeat two- and three-workload profiles validate. Clockwork Arena and Agent
  World Builder reproduce their established state, capture, and replay
  identities.
- Distribution proof: two fresh builds reproduce a 276,467-byte pure wheel at
  `ca8d9bd9a94270f7b0a63b4e0bee173d47cddd88fb7fda46c5abec1e4ec3b1d7`
  and a 1,395,653-byte source archive at
  `e8d276fb2da5151a16182175004e8b1c8e32e82ce69dab9109ef039d6304a92a`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Review: no actionable issue is present across exactly 18 intended paths.
  Workflows, producer, project metadata, lock, and runtime package remain
  unchanged. Five protected hashes match, credential and backend-leakage scans
  find zero hits, and the 94-entry wheel plus 552-entry source archive contain
  no native/WASM/bytecode or retired control metadata.
- Record-inclusive proof retains 336-file format/Ruff cleanliness, strict
  Pyright zero findings, 1,173 passing architecture assertions with one skip,
  strict docs, five metadata assertions, and clean whitespace. Two final fresh
  builds retain the exact wheel and reproduce a 1,396,981-byte source archive
  at `d26b4d1e71caf70384aefb7493d1f28738d6e46bce094556b4aecc12e64ffc4e`;
  installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
  Precommit history confirms exact M92 base/main/origin/merge-base identity,
  `0 0` divergence, only the necessary local branch plus `main`, only remote
  `main`, valid authentication, no open PR/current-branch run/release/tag, and
  no Git corruption. Those prepublication observations are superseded by the
  exact-head qualification and guarded integration below.
- Hosted qualification: ready PR #231 exact DCO head
  `a0e160f4248cf8de88ee318960ee9bef41242f55`, tree
  `5eb11bd7dbdb62d61bafdd94d2c94ec0ae4355aa`, passed run `32578695971` in
  exactly three Linux-first allocations. Linux completed in 7m21s, macOS in
  2m04s, and Windows in 4m14s. Every hosted supported-Python suite passed 2,718
  tests; 3.13/3.14 retained one established capability skip.
- Hosted graphics/distribution: every OS passed ten real-wgpu tests, the
  three-workload graphics profile, Clockwork Arena, and Agent World Builder.
  Linux also passed 336-file formatting, Ruff, strict Pyright, strict docs,
  the two-workload base profile, reproducible builds, wheel smoke, ten-artifact
  staging, and complete release smoke. Builds reproduced a 276,453-byte wheel
  at `d30047cb6671e83592009410c9d75449084c80bfcafb6f828431150cbcd93b9a`
  and a 1,397,392-byte source archive at
  `e63abf65b518a4eb36a7753b1f93f7168bc26e5e498ad62f5a319003107914ad`.
- Readiness/integration: two separated audits retained exact head/tree/base,
  three successful checks, one exact-head run, `MERGEABLE`/`CLEAN`, and zero
  comments, reviews, review comments, or threads. The intervening 27-case
  separator passed with protected hashes and whitespace clean. Guarded squash
  `64dbd6495ebeb0f8460340d84662a218498f9f03` has the exact qualified tree,
  sole parent exact M92 closeout, standalone DCO, and a valid GitHub signature.
  The feature branch is deleted locally/remotely, synchronized `main` has `0 0`
  divergence, and no postmerge workflow ran. Factual integration-record and
  closeout PRs remain active.
- Integration-record local proof: exactly five factual records change. All 336
  Python files remain format/Ruff clean, strict Pyright reports zero findings,
  all 1,173 architecture assertions pass with one established Windows skip,
  strict docs, five metadata assertions, and whitespace pass. Two fresh builds
  retain the 276,467-byte feature wheel at
  `ca8d9bd9a94270f7b0a63b4e0bee173d47cddd88fb7fda46c5abec1e4ec3b1d7`
  and reproduce a 1,398,640-byte source archive at
  `4236d5f574d13cfddb7c6728aa68607552c8a93dfbad08deb307a9d109a386e2`;
  installed-wheel, ten-artifact staging, and complete release smoke pass.
- Final integration-record proof retains 336-file format/Ruff cleanliness,
  strict Pyright zero findings, 1,173 passing architecture assertions with one
  skip, strict docs, five metadata assertions, and clean whitespace. Remote
  refresh confirms exact feature-squash head/main/origin/merge-base identity,
  `0 0` divergence, only the necessary local branch plus `main`, only remote
  `main`, and empty open-PR, branch-run, release, and tag queries.
- Hosted integration record: ready PR #232 exact DCO head
  `2daefe6cc8aabb006c66def446489a4cdfd90770`, tree
  `5aa94c16099a809510afd483c2735e2921154873`, passed run `32579739538` in one
  49-second Linux allocation. Its desktop umbrella skipped with zero steps.
  Formatting, Ruff, strict docs, all 1,174 hosted documentation-architecture
  assertions, reproducible builds, installed-wheel smoke, ten-artifact staging,
  and complete release smoke passed.
- Hosted record artifacts: the 276,453-byte wheel retained feature SHA-256
  `d30047cb6671e83592009410c9d75449084c80bfcafb6f828431150cbcd93b9a`;
  the 1,399,230-byte record-inclusive source archive SHA-256 is
  `d979978f28ad233d149838c67302cbba6b4543a619111d319636aeea33f94567`.
- Integration-record readiness/integration: two separated audits around five
  passing metadata assertions retained exact head/tree/base, one DCO commit,
  five paths, the successful bounded Linux gate, zero-step skipped desktop
  umbrella, `MERGEABLE`/`CLEAN`, and zero feedback. Guarded squash
  `e40078cfafc2369f8c4a106d20e45d75dd07e94b` has the exact reviewed tree,
  sole parent the verified feature squash, standalone DCO, and a valid GitHub
  signature. The branch is deleted locally/remotely, synchronized `main` has
  `0 0` divergence, and no postmerge workflow ran. Only the closeout record and
  final cleanup remain.
- Closeout local proof: exactly three project records change. Five metadata-
  hygiene assertions and whitespace pass; full Git checking reports no
  corruption with expected squash-era dangling objects. Remote refresh retains
  exact integration-squash head/main/origin/merge-base identity, `0 0`
  divergence, only the necessary local closeout branch plus `main`, only remote
  `main`, and empty open-PR, branch-run, release, and tag queries.

## M92 local-header variable-envelope bounds preflight - complete

- Base: exact verified M91 closeout squash
  `0d89517265ffbca931c5fa9d76f666900371e23c`, tree
  `5e9b52d47d7d9b71ab5e803c30828bed53d8c94e`. Synchronized `main` was the
  only local/remote branch; there was no open PR, current-head run, tag,
  release, tracked identity-control path, or M91 generated target.
- Gap: changing only the second local file-name length to 65,535 leaves parser-
  exposed offsets `[0, 46]`, both signatures, and fixed-prefix end 76 before
  conventional directory offset 94, but makes the declared envelope end at
  65,611. Exact CPython 3.12.13, 3.13.13, and 3.14.5 read the first payload and
  defer public `BadZipFile` until the malformed member opens.
- Decision: after every policy through M91, private complete release smoke
  reads exactly the two little-endian local name/extra length declarations and
  requires each resulting header envelope to end no later than the
  conventional central directory before names, metadata, inventory, staging,
  or reads. The stable error is `sample bundle local header envelopes are out
  of bounds`.
- Boundary: one two-field envelope-bound classifier only. It performs no
  local-name comparison, extra-field parsing, field consistency check, next-
  header or payload bound, complete local-record extent, gap/adjacency/
  contiguity/non-overlap policy, inter-member layout validation, archive
  repair, workflow, producer, dependency, runtime API, or release authority.
- Direction proof: PKWARE APPNOTE 6.3.10 section 4.3.7 defines the two fields
  and their following variable regions; Python documents `header_offset`.
  CPython 3.14 reads and skips those local regions before its later checks, but
  M92 depends only on public offsets and owned snapshot bytes.
- Red baseline: the static-clean 22-case contract passes 12 controls and fails
  10 missing policy, helper, cleanup, source-order, and documentation contracts
  in 0.30 seconds against exact M91 code. No pass is claimed.
- Implementation: release smoke now reads four length bytes and applies the
  arithmetic envelope bound after M91 prefix policy. RFC-0075 and aligned
  public, security, architecture, release, maintainer, navigation, roadmap,
  and repository records define the fixed-profile rule.
- Focused/supported proof: all 42 combined M91-M92 assertions pass on CPython
  3.12. The 22-case M92 contract passes on exact CPython 3.12.13, 3.13.13, and
  3.14.5. Complete suites pass 2,681 tests with 16 established skips on each
  interpreter. A first concurrent focused attempt raced the shared uv
  environment; no combined pass is claimed from that attempt.
- Static/architecture proof: the unchanged 46-package lock resolves and the
  45-package graphics environment is restored. All 335 Python files are
  format/Ruff clean; strict Pyright reports zero findings; all 1,151
  architecture assertions pass with one established Windows capability skip;
  strict docs and whitespace pass. A transient Windows directory-replace
  denial in the first architecture run passed focused and complete fresh-root
  corrections.
- Graphics/slices proof: all ten real-wgpu tests pass in 7.54 seconds; one-
  repeat two- and three-workload profiles validate. Clockwork Arena and Agent
  World Builder reproduce their established state, capture, and replay
  identities.
- Distribution proof: two fresh builds reproduce a 276,310-byte pure wheel at
  `142f42c79a44b23ef94836127cb011cce361354ce1758ce7e3784a0a464d72f3`
  and a 1,387,194-byte source archive at
  `3324e96e552134eee8151cb1e23598d8bad8c6ecea6f7ba2b2dae5acebde4c0c`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Review: no actionable finding is present. Exactly 17 intended paths change;
  workflows, producer, project metadata, lock, and runtime package remain
  protected. Metadata hygiene passes five checks; high-confidence credential
  and backend-import scans find zero files; the 94-entry wheel and 550-entry
  source archive contain no native/WASM/bytecode/retired-control payload; and
  whitespace is clean.
- Record-inclusive proof: all 335 Python files remain format/Ruff clean, strict
  Pyright reports zero findings, all 1,151 architecture assertions pass with
  one established skip, strict docs, five metadata checks, and whitespace
  pass. Two fresh builds retain the exact wheel and reproduce a 1,388,803-byte
  source archive at
  `9a5594a7c13d0ad3fa4fc34986b1845aadac5e58cf5f350d69fb880b0dc67952`;
  installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Final record-tree proof retains 335-file format/Ruff cleanliness, strict
  Pyright zero findings, 1,151 passing architecture assertions with one skip
  in 10.18 seconds, strict docs in 1.55 seconds, five metadata assertions in
  0.43 seconds, and clean whitespace.
- Prepublication history: after fetch/prune, branch head, `main`, `origin/main`,
  and merge base are exact M91 closeout
  `0d89517265ffbca931c5fa9d76f666900371e23c`, with symmetric difference
  `0 0`. Only `main` and the necessary M92 feature branch exist locally and
  only `origin/main` remotely; authentication is valid, the last three
  integrated commits retain DCO, full Git checking reports no corruption, and
  open PR, current-branch workflow, tag, and release queries are empty.
- Hosted qualification: ready PR #228 exact DCO head
  `379e5f74d8b40a36bcc1124a8a173113171a836e`, tree
  `803cafd5b8e8e3d7d5d8484137a4d0ab531c2db9`, passed run `32575646939` in
  exactly three Linux-first allocations. Linux completed in 7m22s, macOS in
  2m29s, and Windows in 4m42s. Every hosted supported-Python suite passed 2,696
  tests; the 3.13/3.14 suites retained one established capability skip.
- Hosted graphics/distribution: every OS passed ten real-wgpu tests, the
  three-workload graphics profile, Clockwork Arena, and Agent World Builder.
  Linux also passed 335-file formatting, Ruff, strict Pyright, strict docs,
  the two-workload base profile, reproducible builds, wheel smoke, ten-artifact
  staging, and complete release smoke. The builds reproduced a 276,297-byte
  wheel at `fdcb1dfcad52c6dd833b00e570d83cd1639f6eb16137ae8c6b2ef856df180858`
  and a 1,389,514-byte source archive at
  `c220e7ddffe34fd0418fdab3c00e4771e40a0f70fea3df21da45c723f2176f83`.
- Readiness/integration: two separated audits retained exact head/tree/base,
  three successful checks, `MERGEABLE`/`CLEAN`, and zero feedback or review
  threads. The corrected separator passed five metadata assertions in 0.33
  seconds with protected hashes and whitespace clean. Guarded squash
  `22e26cd732dcc4b0523e6cdb7d89ac7d3946b8ed` has the exact qualified tree,
  sole parent exact M91 closeout, standalone DCO, and a valid GitHub signature.
  No postmerge workflow ran.
- Integration record: PR #229 exact DCO head
  `ec9f48ac7eb04f988e25cf3c555616823aebc752`, tree
  `3f06198b329aa5984be91ff21b2044ec1f94bb21`, passed run `32576516035` in one
  44-second Linux allocation while the desktop matrix skipped with zero steps.
  It passed formatting, Ruff, strict docs, 1,152 Linux documentation-
  architecture assertions, reproducible builds, installed-wheel smoke,
  staging, and complete release smoke. The 276,297-byte wheel retained its
  feature identity; the 1,390,777-byte source archive was
  `0c4bfe7238b5d3ee60a2d44ad879a9d14552df13bd02a79a500a5282b71312b3`.
- Integration-record readiness: two separated audits retained exact
  head/tree/base, one successful Linux check, one zero-step skipped matrix
  check, `MERGEABLE`/`CLEAN`, and zero feedback. The separator passed five
  metadata assertions in 0.33 seconds. Guarded squash
  `eb0b91697de00bd1bddbbb3b70b8362135c5accb` has the exact record tree, sole
  parent the verified feature squash, standalone DCO, and a valid GitHub
  signature. No postmerge workflow ran.

## M91 fixed local-header-prefix bounds preflight - complete

- Base: exact verified M90 closeout squash
  `152a083c2965bf99d54ed5aaba222e6bde1e841f`, tree
  `11a2be31ff96d55cb5f0ac035a2c226000eaf22c`. Synchronized `main` was the
  only local/remote branch; there was no open PR, current-head run, tag,
  release, identity-control path, or M90 generated target. Full Git checking
  reported no corruption.
- Gap: a central pointer can identify `PK\x03\x04` only four bytes before the
  conventional central directory. Exact CPython 3.12.13, 3.13.13, and 3.14.5
  expose offsets `[0, 90]` below directory offset `94`, read the first payload,
  and defer public `BadZipFile` until the malformed second member is opened.
- Decision: after every policy through M90, private complete release smoke
  requires each parser-exposed offset plus ZIP's 30-byte fixed local-header
  prefix to be no greater than the conventional central-directory offset
  before decoded names, metadata, inventory, staging, or reads. The stable
  error is `sample bundle local header prefixes are out of bounds`.
- Boundary: one arithmetic prefix-bound classifier only. It adds no local-
  header field parser, filename/extra-length interpretation, complete record
  extent, payload bound, or inter-member layout validator, archive repair,
  workflow, producer, dependency, runtime API, or release authority.
- Red baseline: the static-clean 20-case contract passes 11 controls and fails
  9 missing runtime, helper, cleanup, source-order, and documentation contracts
  in 0.35 seconds against exact M90 code. No pass is claimed.
- Implementation: release smoke now applies the 30-byte arithmetic bound after
  M90 signatures and before names. RFC-0074 and aligned public, security,
  architecture, release, maintainer, navigation, roadmap, and repository
  records define the fixed-profile rule.
- Focused/supported proof: all 39 combined M90-M91 assertions pass on CPython
  3.12. The 20-case M91 contract passes on exact CPython 3.12.13, 3.13.13, and
  3.14.5. Complete suites pass 2,659 tests on each interpreter, with 15
  established skips on 3.12 and 16 on 3.13/3.14.
- Static/architecture proof: the unchanged 46-package lock resolves and the
  45-package graphics environment is restored. All 334 Python files are
  format/Ruff clean; strict Pyright reports zero findings; all 1,129
  architecture assertions pass with one established Windows capability skip;
  strict docs and whitespace pass.
- Graphics/slices proof: all ten real-wgpu tests pass; two- and three-workload
  profiles validate. Clockwork Arena and Agent World Builder reproduce their
  established state, capture, and replay identities.
- Distribution proof: two fresh builds reproduce a 276,152-byte pure wheel at
  `007272e5a687d66ccca7ae1a324b7274dd8b5464f2ae46e909c1303eaeb24750`
  and a 1,377,835-byte source archive at
  `c2b0f8e9dbd34625dc4d92158af6d9a379ca6fa84baefa0fd6a2f596b91c4ef3`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Review: no actionable finding remains. Exactly 16 intended paths change;
  workflows, producer, project metadata, lock, and runtime package remain
  protected. Metadata hygiene passes five checks; corrected credential and
  explicit-identity scans find zero matches; the 94-entry wheel and 548-entry
  source archive contain no native/WASM/bytecode/retired-control payload;
  whitespace passes and Git object checking reports no corruption. One first
  credential regex was malformed and performed no scan; no pass is claimed.
- Record-inclusive proof: all 334 Python files remain format/Ruff clean,
  strict Pyright reports zero findings, all 1,129 architecture assertions pass
  with one established skip, strict docs and whitespace pass. Two fresh builds
  retain the exact wheel and reproduce a 1,379,095-byte source archive at
  `3ee670767c914049d48226cd245e83fbfe7e4891b6ef12cf71cae436cf880f3d`;
  installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Prepublication history: after fetch/prune, branch head, `main`, `origin/main`,
  and merge base are exact M90 closeout
  `152a083c2965bf99d54ed5aaba222e6bde1e841f`, with symmetric difference
  `0 0`. Only `main` and the necessary M91 feature branch exist locally and
  only `origin/main` remotely; authentication is valid, the last three
  integrated commits retain DCO, and open PR, current-branch workflow, tag,
  and release queries are empty.
- Initial hosted qualification: ready PR #225 exact DCO head
  `0af7816ad989c9e66f7c90748df2f85cb2578861`, tree
  `18eea0ceaa75a8afe47ce2977247ada6d5c2de89`, passed run
  `31811384356` in exactly three Linux-first allocations: Linux in 7m22s,
  macOS in 3m16s, and Windows in 4m12s. Linux passed 2,674 tests on CPython
  3.12 and 2,674 with one skip on 3.13/3.14; macOS and Windows CPython 3.14
  each passed 2,674 with one skip. Every OS passed ten real-wgpu tests,
  graphics profiling, Clockwork Arena, and Agent World Builder.
- Initial hosted artifacts: the 276,138-byte pure wheel SHA-256 is
  `cb1ef8ded74d441df6c85c4f482a0142e7bd822d774562b203c6c368a5d4cf7a`;
  the 1,379,557-byte source archive SHA-256 is
  `6f8e54b385e96135f16262c66b955923d4c63d808e4a3d58d0f963f3aaace2af`.
  Installed-wheel, staging, and complete release smoke passed.
- Review correction: the first readiness audit found one actionable P2: the
  detailed README status still named M0-M89 while the banner named M0-M90.
  The tree was not merged. The sentence now names M0-M90 and the M91 test
  protects both status statements. Twenty-five focused M91/metadata assertions,
  strict Pyright, Ruff, strict docs, and whitespace pass. One initial local
  tree query used PowerShell-sensitive braces and failed; a portable query is
  required. One review-fix format check mistakenly targeted Markdown and Ruff
  rejected that unsupported target; the corrected Python-only check passes.
- Complete correction gate: the first attempt was intentionally interrupted
  before a complete result, so no pass is claimed. A fresh rerun from separate
  absent temporary roots found all 334 Python files format/Ruff clean, strict
  Pyright zero findings, all 1,129 architecture assertions passing with one
  established Windows capability skip in 8.81 seconds, strict docs passing in
  1.44 seconds with only the known Material notice, and clean whitespace.
- Corrected hosted qualification: amended DCO head
  `1e4da54e94525a77d087ad76ad069c5aacacb2a3`, tree
  `6268e4a71ba1dc64c2be5eb3b460b97c979e1f4b`, passed run
  `32572856843` in exactly three Linux-first allocations: Linux job
  `97030804585` in 5m23s, macOS `97031385370` in 2m39s, and Windows
  `97031385385` in 4m33s.
- Corrected hosted suites: Linux passed 2,674 tests on CPython 3.12 and 2,674
  with one skip on 3.13/3.14. macOS and Windows CPython 3.14 each passed 2,674
  with one skip. Every OS passed ten real-wgpu tests, graphics profiling,
  Clockwork Arena, and Agent World Builder; Linux also passed static/docs,
  base profiling, installed-wheel, staging, and complete release smoke.
- Corrected hosted artifacts: the 276,136-byte pure wheel SHA-256 is
  `a497834b481b073b9e31558745f6d42f53cb0c53b6e542331da55d85b0129222`;
  the 1,381,396-byte source archive SHA-256 is
  `5777fbf69ad83964a787eca90a8c28ff4d60c9ad07c8e83fdaf89beab4b3a0c3`.
- Corrected readiness/integration: two separated audits retained exact
  head/tree/base, one DCO commit, 16 paths, three successful checks,
  `MERGEABLE`/`CLEAN`, one exact-head run, no issue comments, and the sole
  historical review thread resolved. The separator passed 25 M91/metadata
  assertions in 0.46 seconds.
- Guarded squash `33b9ed5ba0ed5503db82de0ce8ebb8537f67dc2b` has exact
  qualified tree, sole parent exact M90 closeout, standalone DCO trailer, and
  valid GitHub signature at `2026-08-22T12:35:24Z`. The feature branch is
  deleted remotely and locally; exact synchronized `main` has divergence
  `0 0`, and no postmerge workflow ran.
- Integration-record local gate: all 334 Python files are format clean; Ruff
  and strict Pyright report zero findings; all 1,129 architecture assertions
  pass with one established Windows capability skip in 8.09 seconds; strict
  docs build in 1.36 seconds with only the known Material notice; all five
  metadata-hygiene assertions pass in 0.34 seconds; and whitespace is clean.
  Two fresh builds reproduce a 276,150-byte pure wheel at SHA-256
  `3df5bb9a259229645b05e20661bea30d41dc15541671ff84f204ff8a4c280ca8`
  and a 1,382,764-byte source archive at SHA-256
  `2b76156a210dc80955c339a4f445111957e2f91a26b9844e6d6a8b56c512202d`;
  installed-wheel smoke, ten-artifact staging, and complete release smoke
  pass.
- Integration-record publication: ready PR #226 exact DCO head
  `c78ffa68563951e38a770491ace112b77e8463e6`, tree
  `276aa74b790300e5128b6243cf7c42277aa1dda5`, passed run
  `32573846472` in one 49-second Linux job `97033170709`; desktop umbrella
  `97033267512` skipped with zero steps. Hosted documentation architecture
  passed 1,130 assertions; installed-wheel, ten-artifact staging, and complete
  release smoke passed.
- Hosted record artifacts: the 276,136-byte wheel remains
  `a497834b481b073b9e31558745f6d42f53cb0c53b6e542331da55d85b0129222`;
  the 1,383,520-byte source archive is
  `b34bb2144f7aa7ca3bd69f021d05210cebe4e8b7eb804a401813b0a82eec351d`.
- Integration readiness/squash: two separated audits retained exact
  head/tree/base, one DCO commit, five paths, bounded Linux success, zero-step
  desktop, and zero feedback. PR #226 squash
  `9d4a0025e4e5a57a8946bb3a2ed887ca081c9955` has exact reviewed tree,
  sole parent feature squash, standalone DCO trailer, and valid GitHub
  signature at `2026-08-22T12:47:17Z`. The record branch is deleted remotely
  and locally.
- Closeout local proof: exactly three project records change; repository
  metadata hygiene passes five assertions in 0.35 seconds, whitespace passes,
  and full Git object checking reports no corruption. Fetch/prune leaves branch
  head, `main`, `origin/main`, and merge base at exact integration-record
  squash with divergence `0 0`; only `main` and the closeout branch exist
  locally and only `origin/main` remotely, with no open PR, exact-head
  postmerge run, tag, release, or tracked identity-control path.

## M90 local-header signature preflight - complete

- Base: exact verified M89 closeout squash
  `92b3e2c351fe92ea0789b46636e0d0a08d29281a`, tree
  `46fa37f60b603ffa79b5ed7354b55fa2da13b953`. Synchronized `main` is the
  only local/remote branch; there is no open PR, current-head run, tag, release,
  identity-control path, or M89 generated target. Full Git checking reports no
  corruption.
- Gap: shifting only the second central pointer by one byte leaves offsets
  ordered, distinct, and in bounds as `[0, 47]` below directory offset `94`.
  Exact CPython 3.12.13, 3.13.13, and 3.14.5 expose signature bytes
  `504b0304`, `4b030414`, read the first payload, and defer `BadZipFile` until
  the malformed second member is opened.
- Decision: after every policy through M89, private complete release smoke
  requires the four bytes at every parser-exposed offset to equal local-file-
  header signature `PK\x03\x04` before decoded-name policy, metadata,
  inventory, staging, or reads. The stable error is `sample bundle local header
  signature is inconsistent`.
- Boundary: one snapshot-backed four-byte signature classifier only. It adds
  no local-header field parser, central-directory parser, record extent,
  adjacency, contiguity, or inter-member layout validator, archive repair,
  workflow, producer, dependency, runtime API, or release authority.
- Red baseline: the static-clean 19-case contract passes 10 controls and fails
  9 missing runtime, helper, cleanup, source-order, and documentation contracts
  in 0.48 seconds against exact M89 code. No pass is claimed.
- Implementation: release smoke reads exactly four bytes at each public offset
  from the owned snapshot after M89 and restores the snapshot position.
  RFC-0073 and aligned public, security, architecture, release, maintainer,
  navigation, roadmap, and repository records state the fixed-profile rule.
- Focused checkpoint: all 37 combined M89-M90 assertions pass on CPython 3.12
  in 0.38 seconds. The two affected Python files are format/Ruff clean, strict
  Pyright reports zero findings, and strict docs build in 1.52 seconds with
  only the known upstream Material notice. A preceding command used a
  nonexistent historical M89 filename, exited 1, and ran no tests; it is not
  claimed as a pass.
- Supported/local proof: the 19-case contract passes on exact CPython 3.12.13,
  3.13.13, and 3.14.5. Complete non-wgpu suites pass 2,639 tests on each
  interpreter with 15 established skips. The locked CPython 3.12 graphics
  environment is restored.
- Static/docs proof: the unchanged 46-package lock resolves and the 45-package
  graphics environment is installed. All 333 Python files are format/Ruff
  clean; strict Pyright reports zero findings; all 1,109 architecture
  assertions pass with one established Windows capability skip; strict docs
  and whitespace pass.
- Graphics/slices proof: all ten real-wgpu tests pass in 8.81 seconds; two- and
  three-workload profiles validate. Clockwork Arena and Agent World Builder
  reproduce their established state, capture, and replay identities.
- Distribution proof: two fresh builds reproduce a 276,061-byte pure wheel at
  `c2b71f657baaaad330c9076a2cef25c13644874196005be74b8a436bcabc8cc2`
  and a 1,371,380-byte source archive at
  `807966575bc9b2141fefda88ef0ea4395dc8fc34e8307b9879ad5adb9883e262`.
  Isolated-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Review: no actionable finding remains. Exactly 16 intended paths change;
  workflows, producer, project metadata, lock, and runtime package remain
  protected. Metadata hygiene passes five checks, credential scanning finds
  zero matches, the 94-entry wheel and 546-entry source archive contain no
  native/WASM/bytecode/retired-control payload, whitespace passes, and Git
  object checking reports no corruption.
- Record-inclusive proof: all 333 Python files remain format/Ruff clean,
  strict Pyright reports zero findings, all 1,109 architecture assertions pass
  with one established skip, strict docs and whitespace pass. Two fresh builds
  retain the exact wheel and reproduce a 1,372,739-byte source archive at
  `d3dacd616f590977116ee126a777c448654e78f24f4f5387cdcdb926a7d2215c`;
  isolated-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Prepublication history: after fetch/prune, branch head, `main`,
  `origin/main`, and merge base are exact M89 closeout
  `92b3e2c351fe92ea0789b46636e0d0a08d29281a`, with symmetric difference
  `0 0`. Only `main` and the necessary M90 feature branch exist locally, only
  `origin/main` remotely, authentication is valid, and open PR, current-branch
  workflow, tag, and release queries are empty.
- Hosted qualification: ready PR #222 exact DCO head
  `e2fa04c4230756042bde239cfdcd2c6c2b1cfc5c`, tree
  `4acdecef4265e972e15e4ce838cb91e530101cda`, passed run
  `31806688540` in exactly three Linux-first allocations: Linux
  `94787208676` in 7m30s, macOS `94789151633` in 3m15s, and Windows
  `94789151556` in 4m05s.
- Hosted suites: Linux passed 2,654 tests on CPython 3.12 and 2,654 with one
  skip on 3.13/3.14. macOS and Windows CPython 3.14 each passed 2,654 with one
  skip. Every OS passed ten real-wgpu tests, graphics profiling, Clockwork
  Arena, and Agent World Builder; Linux also passed static/docs, base
  profiling, isolated-wheel, staging, and complete release smoke.
- Hosted artifacts: the 276,046-byte pure wheel SHA-256 is
  `2b7b53ea14b1beef2d6ba1409e1c5a25920460d676672a8a41df227ba9a4a8a4`;
  the 1,373,598-byte source archive SHA-256 is
  `5b31e083331b030fabf8fd34353e850efd7e3b7830e30b5eb5f305a7fdda8ad9`.
- Readiness/integration: two separated audits retained exact head/tree/base,
  one DCO commit, 16 paths, three successful checks, `MERGEABLE`/`CLEAN`, one
  hosted run, and zero feedback. The separator passed 24 focused and metadata
  assertions in 0.48 seconds.
- Guarded squash `b35b2de7725f2a5367cc48e2acd22835220560ca` has exact
  qualified tree, sole parent exact M89 closeout, standalone DCO trailer, and
  valid GitHub signature at `2026-08-14T14:05:47Z`. The feature branch is
  deleted remotely and locally.
- Integration-record local proof: exactly five repository records change.
  All 333 Python files are format/Ruff clean, strict Pyright reports zero
  findings, all 1,109 architecture assertions pass with one established skip,
  strict docs and whitespace pass. Two fresh builds retain the exact local
  feature wheel and reproduce a 1,374,693-byte source archive at
  `1f637955f3878f088aa13c24b2e77553c537466d1460afc6f8c23c66efb3eb67`;
  isolated-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Final integration-record proof: all 333 Python files remain format/Ruff
  clean, strict Pyright reports zero findings, all 1,109 architecture
  assertions pass with one established skip, strict docs and whitespace pass,
  and the five-case metadata separator passes. Fetch/prune leaves branch head,
  `main`, `origin/main`, and merge base at exact feature squash with divergence
  `0 0`; only `main` and the record branch exist, with no open PR, exact-head
  postmerge run, tag, or release.
- Hosted integration record: ready PR #223 exact DCO head
  `ba9d19a503cb748adcb05ad179d44c1047d2a5ae`, tree
  `e821498016a867fe4811a83ddafbebc6e5b5f641`, passed run
  `31808445884` in one 50-second Linux job `94792942983`; desktop umbrella
  `94793181074` skipped with zero steps. Hosted documentation architecture
  passed 1,110 assertions; isolated-wheel, ten-artifact staging, and complete
  release smoke passed.
- Hosted record artifacts: the 276,046-byte wheel remains
  `2b7b53ea14b1beef2d6ba1409e1c5a25920460d676672a8a41df227ba9a4a8a4`;
  the 1,375,288-byte source archive is
  `f6e9d306808c04f1c80233294578dc3304c4df4c5cb062f826f2279ee9ca2ee2`.
- Integration readiness/squash: two separated audits retained exact
  head/tree/base, one DCO commit, five paths, bounded Linux success, zero-step
  desktop, and zero feedback. PR #223 squash
  `808dff848f04f9ed7f665ad3a6f36047db4053b4` has exact reviewed tree,
  sole parent feature squash, standalone DCO trailer, and valid GitHub
  signature at `2026-08-14T14:16:01Z`. The record branch is deleted remotely
  and locally.
- Closeout local proof: exactly three project records change; repository
  metadata hygiene passes five assertions, whitespace passes, and Git object
  checking reports no corruption. Fetch/prune leaves branch head, `main`,
  `origin/main`, and merge base at exact integration-record squash with
  divergence `0 0`; only `main` and the closeout branch exist, with no open PR,
  exact-head postmerge run, tag, or release.
- Closeout readiness/squash: two separated audits retained exact head/tree/base,
  one standalone DCO commit, exactly three project records, zero hosted
  allocation, and zero feedback. PR #224 squash
  `152a083c2965bf99d54ed5aaba222e6bde1e841f` has exact reviewed tree, sole
  parent integration-record squash, standalone DCO trailer, and a valid GitHub
  signature at `2026-08-14T14:22:27Z`.
- Final cleanup: 25 verified generated M90 targets were removed. Exact
  synchronized `main` is the closeout squash with divergence `0 0`; only
  `main` exists locally and remotely, with no open PR, current-head workflow,
  tag, release, retired control path, or M90 generated target. Git object
  checking reports no corruption.

## M89 local-header-offset bounds preflight - complete

- Base: exact verified M88 closeout squash
  `03f3723bf7365701c78a0fde072392b9f51da66b`, tree
  `141fe396a5313eccc1c706b2af114a021537ac90`. Synchronized `main` was the
  only local/remote branch; no open PR, tag, release, postmerge run, identity-
  control directory, or M88 generated target remained before M89 selection.
- Gap: changing only one central pointer makes public `ZipInfo.header_offset`
  equal the conventional central-directory offset. Exact CPython 3.12.13,
  3.13.13, and 3.14.5 expose offsets `[0, 94]`, read the first payload, and
  defer `BadZipFile` until the malformed second member is opened.
- Decision: after every policy through M88, private complete release smoke
  requires every parser-exposed local-header offset to be strictly before the
  conventional central-directory offset before decoded-name policy, metadata,
  inventory, staging, or reads. The stable error is `sample bundle local header
  offsets are out of bounds`.
- Boundary: one aggregate public-parser upper bound only. It adds no local-
  header parser, central-directory record parser, local-record extent or
  physical-contiguity rule, inter-member layout validator, archive repair,
  workflow, producer, dependency, runtime API, or release authority.
- Red baseline: the static-clean 18-case contract passes 9 controls and fails 9
  missing runtime, helper, cleanup, source-order, and documentation contracts
  in 0.35 seconds against exact M88 code. No pass is claimed.
- Implementation: release smoke now reads the conventional central-directory
  boundary from the already-admitted final end record and rejects any public
  offset at or after it immediately after M88. RFC-0072 and the aligned public,
  security, architecture, release, maintainer, roadmap, and repository records
  state the rule and explicit nonclaims.
- Focused checkpoint: all 35 combined M88-M89 assertions pass on CPython 3.12
  in 0.41 seconds. The two affected Python files are format/Ruff clean, strict
  Pyright reports zero findings, and strict docs build in 1.38 seconds with
  only the known upstream Material notice.
- Supported/local proof: the 18-case M89 contract passes on CPython 3.12.13,
  3.13.13, and 3.14.5. Complete suites pass 2,620 tests on each interpreter
  with 15/16/16 established skips. All 1,090 architecture assertions pass with
  one established Windows capability skip; all 332 Python files are format/
  Ruff clean, strict Pyright reports zero findings, and strict docs pass.
- Graphics and slices: all ten real-wgpu tests pass; two- and three-workload
  one-repeat profiles validate. Clockwork Arena and Agent World Builder retain
  their established state, capture, and replay identities.
- Distribution: two fresh builds reproduce a 275,910-byte pure wheel at
  `eca489c14cee629bf5f3403a78b3efc6670ffea56113b09981e6a34176bef0d4`
  and a 1,364,259-byte source archive at
  `02e7801303a3465188750eedc95e2e957bb5d469b464a8da6b0a472c74b0d190`.
  Isolated-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Review: findings-first review found no defect. The exact 16-path scope keeps
  all protected hashes unchanged; metadata hygiene and credential scans are
  clean; the 94-entry wheel and 544-entry source archive contain no native,
  WASM, bytecode, or retired control metadata; Git object checking reports no
  corruption.
- Record-inclusive gate: all 332 Python files remain format/Ruff clean, strict
  Pyright reports zero findings, all 1,090 architecture assertions pass with
  one established skip, strict docs build, and whitespace passes.
- Prepublication history: fetch/prune leaves branch head, `main`, `origin/main`,
  and merge base at exact M88 closeout with symmetric difference `0 0`. Only
  `main` and the required M89 feature branch exist; authentication is valid and
  there is no open PR, tag, or release.
- Hosted qualification: ready PR #219 exact DCO head
  `60559fd6ba5e3bc4583dc86c9b185f1175ac8f3d`, tree
  `0eba3e7b2407d08a6b030746bd73e7af57211b77`, passed run `31801893736` in
  exactly three Linux-first allocations. Linux `94771566336` passed in 7m33s,
  macOS `94773345967` in 2m02s, and Windows `94773345983` in 4m12s.
- Hosted suites: Linux passed 2,635 tests on CPython 3.12, 3.13, and 3.14,
  with one capability skip on 3.13/3.14. macOS and Windows CPython 3.14 each
  passed 2,635 with one skip. Every OS passed ten real-wgpu tests, graphics
  profiling, Clockwork Arena, and Agent World Builder; Linux also passed base
  profiling, static/docs, installed-wheel, staging, and release smoke.
- Hosted artifacts: the 275,896-byte pure wheel SHA-256 is
  `22a14f43b4cdc2afaee7c4f39bc04e9baaebea557b070d3131fa8820a256c3ee`;
  the 1,365,606-byte source archive SHA-256 is
  `6ae3d9d8f5e6190342ea0e588a6340cd2676e30da8a99fe2e2c07193452c09d5`.
- Readiness/integration: two separated audits retained exact head/tree/base,
  one DCO commit, 16 paths, three successful checks, `MERGEABLE`/`CLEAN`, one
  hosted run, and zero feedback. Guarded squash
  `61e5db38aef45a00788980227edf69663c82ce7b` has exact qualified tree, sole
  parent exact M88 closeout, standalone DCO trailer, and valid GitHub signature
  at `2026-08-14T13:03:08Z`. The feature branch is deleted remotely/locally.
- Integration-record proof: exactly five repository records change. All 332
  Python files are format/Ruff clean, strict Pyright reports zero findings,
  all 1,090 architecture assertions pass with one established skip, strict
  docs and whitespace pass. Two builds reproduce the unchanged 275,910-byte
  local pure wheel and a 1,367,109-byte source archive at
  `7081b7c9661fb27ff4046c85d2b891e61dfaa6252c31d57284a08c88fe831803`;
  wheel, ten-artifact staging, and complete release smoke pass.
- Final integration-record repeat remains 332-file format/Ruff clean, strict
  Pyright at zero findings, architecture at 1,090 passed with one established
  skip, strict docs green, and whitespace clean.
- Precommit audit: the five-case metadata separator passes after one sandbox-
  only external uv-cache denial. Branch head, `main`, `origin/main`, and merge
  base remain exact feature squash with divergence `0 0`; only `main` and the
  required integration-record branch exist, with no open PR, current-head
  postmerge workflow, tag, or release.
- Integration-record hosted gate: ready PR #220 exact DCO head
  `27b0f1e2b15e368b76704c6ec0ef0d46e22df759`, tree
  `b7bdeed2c716f4016e5feac18c002a871d111cce`, passed run `31803536737` in
  one 46-second Linux job `94776890212`; desktop umbrella job `94777088248`
  skipped with zero steps. Hosted architecture passed 1,091 assertions;
  installed-wheel, staging, and complete release smoke passed.
- Hosted record-tree artifacts reproduce the feature wheel exactly at 275,896
  bytes and `22a14f43b4cdc2afaee7c4f39bc04e9baaebea557b070d3131fa8820a256c3ee`;
  the 1,367,929-byte source archive SHA-256 is
  `a3328be13d9046151b6dec5a30866280d6dc894de693e749ea0996fbad0819ef`.
- Two integration-record audits retained exact head/tree/base, one DCO commit,
  five paths, one successful bounded run, skipped desktop umbrella, and zero
  feedback. Guarded squash `96b6a2d40816aa94363cde67bb49f1943c7556f3`
  has sole parent the feature squash, exact reviewed tree, standalone DCO
  trailer, and valid GitHub signature at `2026-08-14T13:12:58Z`. Its branch is
  deleted remotely and locally.
- Closeout proof: exactly three project records change. Repository metadata
  hygiene passes five assertions and whitespace is clean. Branch head, `main`,
  `origin/main`, and merge base remain exact integration-record squash with
  divergence `0 0`; only `main` and the necessary closeout branch exist, with
  no open PR, current-head postmerge run, tag, or release.

## M88 local-header-order preflight - closeout active

- Base: exact verified M87 closeout squash
  `aba849aceec15342141a29fc105b85720a5e48ba`, tree
  `d61bce3093e6a497bc40ff57f34dbca957f9a4de`. Synchronized `main` was the
  only local/remote branch; no open PR, tag, release, postmerge run, disclosure
  marker, or M87 generated target remained before M88 selection.
- Gap: a central-directory record swap leaves local records and payloads
  unchanged but changes the public order returned by `ZipFile.infolist()`.
  Exact CPython 3.12.13, 3.13.13, and 3.14.5 expose offsets `[46, 0]` and read
  both payloads successfully. The established verifier did not reject this
  deviation from the fixed producer profile before staging.
- Decision: after every policy through M87, private complete release smoke
  requires strictly increasing parser-exposed `ZipInfo.header_offset` values
  before decoded-name policy, metadata, inventory, staging, or reads. The
  stable error is `sample bundle local header offsets are out of order`.
- Boundary: ZIP permits arbitrary file order generally; M88 is one fixed-
  producer profile rule. It adds no local-header parser, central-directory
  record parser, bounds/contiguity rule, inter-member layout validator,
  archive repair, workflow, producer, dependency, runtime API, or release
  authority.
- Red baseline: the static-clean 17-case contract passes 7 controls and fails
  10 missing runtime, helper, ordering, cleanup, and documentation contracts in
  0.29 seconds against exact M87 code. No pass is claimed.
- Runtime/documentation checkpoint: the strict-order helper runs immediately
  after M87 distinctness. All 33 combined M87-M88 assertions pass in 0.42
  seconds; affected format/Ruff and strict Pyright gates pass, and strict docs
  build in 1.56 seconds with only the known upstream Material notice.
- Supported-Python checkpoint: all 17 M88 assertions pass on exact installed
  CPython 3.12.13, 3.13.13, and 3.14.5.
- Findings-first review found no runtime, test, documentation, or scope defect.
  The unchanged lock, 331-file format/Ruff checks, strict Pyright, 1,072
  architecture assertions, strict docs, and whitespace pass; one established
  Windows architecture capability skip remains.
- Complete supported-Python suites each pass 2,602 non-wgpu tests with 15
  established skips on CPython 3.12.13, 3.13.13, and 3.14.5.
- Graphics/examples: ten real-wgpu tests, two- and three-workload one-repeat
  profiles, Clockwork Arena, and Agent World Builder pass in the restored
  locked 45-package CPython 3.12 graphics environment with established state,
  capture, and replay identities.
- Distribution/release: two fresh builds reproduce a 275,794-byte pure wheel
  SHA-256 `982da69788bbb475c58e73f6b4b09f1f424ebd064693a5923cfee07613152f9c`
  and 1,358,324-byte source archive SHA-256
  `7c05d0b4832d30be3186baeca5c897c44b3dab3cc9de0837a02a3e4d88c98cda`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Scope/security: exactly 16 intended paths differ. CI, release workflow,
  producer, project metadata, and lock retain protected hashes. Added-content
  identity/credential scans are empty; the 94-entry wheel and 542-entry source
  archive contain no native/WASM/bytecode or retired control metadata; object
  checking reports only unreachable squash-era objects and no corruption.
- Record-inclusive gate: all 331 files remain format/Ruff clean; strict Pyright
  reports zero findings; all 1,072 architecture assertions pass with one
  established capability skip; strict docs and whitespace pass.
- Precommit history: after fetch/prune, local head, `main`, `origin/main`, and
  merge base remain exact M87 closeout `aba849aceec1...` with symmetric
  difference `0 0`. Only `main` and the necessary neutral M88 feature branch
  exist; GitHub authentication is valid and no open PR competes with it.
- Exact-head hosted qualification: ready PR #216 DCO head
  `81b9d469623d5b656db747df6add7ed7dc7e5de6`, tree
  `8cc30da90115fab18798e0001e21797e5b60d6ce`, passed run `31797986973` in
  exactly three Linux-first allocations: Linux 7m22s, macOS 2m29s, and Windows
  4m25s. Linux passed 2,617 tests per supported interpreter; macOS/Windows 3.14
  passed 2,617 with one capability skip. Every OS passed ten real-wgpu tests,
  profiles, and both vertical slices.
- Hosted artifacts: exact-head builds reproduced a 275,781-byte pure wheel
  SHA-256 `b68262c68a20aec3a9f8859648ff64a345d414dc2f8c5b55366fecdc4d4069a2`
  and 1,359,270-byte source archive SHA-256
  `79dd47608abd1c528118c3c0a7c96f06617081ffe4f9fcd1d6ad249f08061e17`;
  installed-wheel smoke, ten-artifact staging, and release smoke passed.
- Integration: two separated audits were clean with zero feedback. Squash
  `b49d27fc15453be24021873a45bbe46f491a26bb` has sole parent exact M87
  closeout, exact qualified tree, standalone DCO trailer, and valid GitHub
  signature at `2026-08-14T12:06:55Z`. The feature branch is deleted remotely
  and locally; integration-record publication is active.
- Integration-record local gate: exactly four project records plus roadmap
  differ from the verified feature squash. All 331 files are format/Ruff clean,
  strict Pyright reports zero findings, 1,072 architecture assertions pass with
  one established skip, and strict docs/whitespace pass. Two pre-record builds
  reproduce the 275,794-byte wheel and 1,360,308-byte source archive SHA-256
  `73aa02c5ee1f720c28ecbd6f9b611eb01930a0361b98397e98f2ba5ff3e7507d`;
  installed-wheel, staging, and release smoke pass.
- Hosted integration record: ready PR #217 exact DCO head
  `c07c51f9f2a9ea8a54b130c4753f05ca6c50c63e`, tree
  `9df9c5f39f89759de7958ca2870ca77433d3d3ae`, passed run `31799359383` in
  one 48-second Linux allocation. Documentation architecture passed 1,073
  assertions; exact-head build, wheel smoke, staging, and release smoke passed.
  Desktop umbrella job `94763618393` skipped with zero steps.
- Integration-record artifacts: 275,781-byte wheel SHA-256
  `b68262c68a20aec3a9f8859648ff64a345d414dc2f8c5b55366fecdc4d4069a2`
  and 1,360,637-byte source archive SHA-256
  `00a235058a3dacb35561053aaebaadf1aea9ef0736d964d1723ab7f0fdec0c5f`.
- Record integration: both audits were clean after a corrected metadata-
  hygiene separator. Squash `7285f5125b170239283f46483b22655a7e598a76`
  has sole parent the feature squash, exact reviewed tree, standalone DCO
  trailer, and valid GitHub signature at `2026-08-14T12:14:53Z`. The branch is
  deleted locally/remotely; no open PR or postmerge main run remains. Exact
  three-record closeout is active.
- Closeout local gate: exact scope is three project records. Repository
  metadata hygiene passes five assertions; whitespace and added-content
  identity/credential scans are clean, with no product/runtime/workflow/build
  or generated-artifact surface.

## M87 distinct local-header-offset preflight - closeout active

- Base: exact verified M86 closeout squash
  `ba9464e59678766dd23953c1ea71acf010103903`, tree
  `eb75ce1a1ebc675dd5c9eb34fde5ffd8619587e1`. Clean synchronized `main` was
  the only local/remote branch; no open PR, tag, release, postmerge run,
  disclosure marker, or M86 generated target remained before M87 selection.
- Gap: exact installed CPython 3.12.13, 3.13.13, and 3.14.5 accept two central
  records that expose the same local-header offset. The first member read
  succeeds and the second alias fails later on local/central filename
  comparison, after the current verifier creates staging. Warning emission is
  implementation-dependent and outside the policy.
- Decision: after every policy through M86, private complete release smoke
  requires all parser-exposed `ZipInfo.header_offset` values to be distinct
  before M77 name policy, metadata, inventory, staging, or reads. The stable
  content-silent error is `sample bundle local header offsets are inconsistent`.
- Boundary: one aggregate public-parser property only. No local-header parser,
  central-directory parser, offset ordering/bounds rule, inter-member layout
  validator, field-consistency validator, signature classifier, archive repair,
  workflow, producer, dependency, runtime API, or release authority is added.
- Red baseline: the static-clean 16-case contract passes 6 controls and fails
  10 missing runtime, helper, ordering, cleanup, and documentation contracts in
  0.42 seconds against exact M86 code.
- Runtime checkpoint: the distinctness helper and exact call ordering make 32
  combined M86-M87 runtime/source/precedence assertions pass. Only the
  deliberately absent RFC/public-document contract failed before documentation
  was added.
- Documentation checkpoint: RFC-0070 and aligned public records complete the
  contract. All 33 combined M86-M87 assertions pass; affected format, Ruff,
  strict Pyright, strict docs, and whitespace gates are clean.
- Supported-Python checkpoint: the 16-case M87 contract passes on CPython
  3.12.13, 3.13.13, and 3.14.5. One concurrent 3.12 harness invocation exited
  1 after its test bodies because parallel uv processes replaced the shared
  `.venv`; a serial isolated correction passes all 16 cases.
- Findings-first review found no runtime, test, or scope defect. It corrected
  stale task and decision records that still described the completed
  implementation and accepted RFC as pending.
- Full local gate: the unchanged lock, 330-file format/Ruff checks, strict
  Pyright, 1,055 architecture assertions, exact 366-case M64-M87 lineage,
  strict docs, whitespace, and complete 2,585-test supported-Python suites pass;
  established Windows capability skips remain 1 in each applicable
  architecture gate and 15 in each complete interpreter suite.
- Graphics/examples: ten real-wgpu tests, the two- and three-workload one-
  repeat profiles, Clockwork Arena, and Agent World Builder pass in the locked
  45-package CPython 3.12 graphics environment with established deterministic
  state, capture, and replay identities.
- Distribution/release: two fresh builds reproduce a 275,673-byte wheel SHA-
  256 `3659480bf9c924758529f34ce312f903a1bd652a5820284bfa11549fe9b428e7`
  and 1,349,517-byte source archive SHA-256
  `936973c9dbf7dc0abd209705e35bccc4d2800a805128609ab65e3f5939d0a01b`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Scope/security: exactly 16 intended paths differ. CI, release workflow,
  producer, project metadata, and lock retain protected hashes. Identity and
  credential scans are empty; wheel contents remain pure Python; object
  checking reports only unreachable squash-era objects and no corruption.
- Record-inclusive gate: all 1,055 architecture assertions pass again with one
  capability skip; all 330 files remain format/Ruff clean, strict Pyright and
  docs pass, and whitespace is clean.
- Precommit history: local head, `main`, `origin/main`, and merge base are exact
  M86 closeout `ba9464e5967...` with symmetric difference `0 0`. Only `main`
  and the necessary neutral M87 branch exist; no open PR competes with it.
- Initial hosted head `769bcb04d3b60114b5c29ea31bce8a15e85471f0`
  failed one test-only assertion after 2,599 Linux passes. Linux preserved the
  duplicate offsets, successful first read, and deferred second-read mismatch,
  but did not emit the overlap warning seen by local Windows probes. The
  warning is implementation-dependent and outside the policy. The correction
  removes only that assertion and narrows public wording; runtime code,
  workflow, dependency, producer, and release authority remain unchanged.
- Corrected local gate: the 16-case contract passes on CPython 3.12.13,
  3.13.13, and 3.14.5 without depending on warning emission. All 330 files are
  format/Ruff clean, strict Pyright and docs pass, all 1,055 architecture
  assertions pass with one established capability skip, whitespace is clean,
  and the complete corrected CPython 3.12 baseline passes 2,585 tests with 15
  established skips.
- Hosted qualification: corrected PR #213 head
  `b98aa8365b6d3742c91871a820170d6b73330f25`, tree
  `2c4aff1985fa6e820a967323114ad6a3d73f9875`, passed run `31794063270`
  in exactly three Linux-first allocations. Linux finished in 7m16s, macOS in
  3m05s, and Windows in 3m52s. Linux CPython 3.12 passed 2,600 tests; Linux
  3.13/3.14 and both desktop 3.14 suites passed 2,600 with one capability skip.
  Each OS passed ten real-wgpu tests, graphics profiling, Clockwork Arena, and
  Agent World Builder; static/docs, artifacts, wheel, staging, and release
  smoke passed.
- Hosted artifacts: byte reproducibility reported a 275,661-byte pure wheel at
  `a0ef617c4ce29f59130155b143c457ceda740ba7950a2f1e01b4893f35ed2263`
  and a 1,352,531-byte source archive at
  `51d595e22e172cbdf74cddf7628db710d94a59c239edd4a90da34eeb40aa3fa3`.
- Integration: two separated audits were clean. Squash
  `dff483e120d607105120d8c004838e609540a14d` has the exact qualified
  tree, sole M86-closeout parent, standalone DCO, and valid GitHub signature at
  `2026-08-14T11:07:28Z`. No postmerge run was allocated; feature branches were
  removed locally and remotely before this integration-record branch.
- Integration-record local gate: scope is exactly four project records plus
  roadmap. The unchanged lock, all 330 files, Ruff, strict Pyright, 1,055
  architecture assertions, strict docs, whitespace, protected hashes,
  identity/credential scans, and Git-object integrity pass with one established
  capability skip. A pre-record pair of fresh builds reproduces a 275,673-byte
  wheel at
  `3659480bf9c924758529f34ce312f903a1bd652a5820284bfa11549fe9b428e7`
  and a 1,353,993-byte source archive at
  `e58694e30441bc79b16d3842da647a95be2144015fd5bf4b5c28c2baa4bfc005`;
  installed-wheel, ten-artifact staging, and complete release smoke pass. The
  subsequent factual project-record lines differ only in the source archive;
  exact record-tree artifact evidence remains a hosted gate.
- Hosted integration record: PR #214 exact DCO head
  `6a99381dbe9ce88c4912f0976d4503a86ab4493d`, tree
  `0b7b6f03d4ad7ce032d7fdb2b9aa43397bd47e2f`, passed run `31795436154`
  in one 45-second Linux allocation; the desktop umbrella skipped with zero
  steps. Documentation architecture passed 1,056 assertions. Reproducibility
  reported a 275,661-byte wheel at
  `a0ef617c4ce29f59130155b143c457ceda740ba7950a2f1e01b4893f35ed2263`
  and 1,354,599-byte source archive at
  `36b3ebff00339a36214830ac243ff0f64f34ec77ae71bdfffb57acdcf755821d`;
  wheel, staging, and release smoke passed.
- Integration-record squash: two audits were clean. Squash
  `857633ad70e21c7c590dafd5c274263ac3184d37` has sole parent
  `dff483e120d607105120d8c004838e609540a14d`, exact tree
  `0b7b6f03d4ad7ce032d7fdb2b9aa43397bd47e2f`, standalone DCO, and valid
  GitHub signature at `2026-08-14T11:17:23Z`. No postmerge run was allocated;
  only synchronized `main` remained before the closeout branch.
- Closeout local gate: exact scope is the three project records. Metadata
  hygiene passes five assertions; whitespace and identity/credential scans are
  clean. No public, runtime, test, workflow, build, dependency, release, or
  generated surface is present.

## M86 first local-header placement preflight - closed

- Base: exact verified M85 closeout squash
  `3eb38c5e591f0d73687293f130254d8c8b3256c7`, tree
  `2425b4bbe9fbdb302797fdc4618be9c34662f196`. Clean synchronized `main` was
  the only local/remote branch; no open PR, tag, release, postmerge run,
  disclosure marker, or M85 generated target remained before M86 selection.
- Gap: exact installed CPython 3.12.13, 3.13.13, and 3.14.5 reads archives with
  one or eleven bytes before the first local header when the central relative
  local-header offset and final central-directory offset are updated. M85
  concatenation adjustment remains zero while the earliest parser-exposed
  `header_offset` moves by exactly the gap length.
- Decision: after every policy through M85, private complete release smoke
  requires the minimum parser-exposed local-header offset to equal zero before
  M77 name policy, metadata, inventory, staging, or reads. The stable content-
  silent error is `sample bundle first local header placement is inconsistent`.
- Boundary: one aggregate public-parser property only. No local-header parser,
  central-directory parser, inter-member layout validator, field-consistency
  validator, signature classifier, archive repair, workflow, producer,
  dependency, runtime API, or release authority is added.
- Red-to-green: the static-clean authoritative baseline passed 6 controls and
  failed 10 missing contracts in 0.67 seconds. The runtime implementation makes
  35 M85-M86 assertions pass in 0.37 seconds; only the deliberately absent
  public/RFC contract remained before documentation was added.
- Review: no production defect was found. One evidence gap was corrected with
  an end-to-end empty-archive regression that proves the established exact-
  inventory error still precedes staging and member reads. The strengthened
  17-case contract passes on CPython 3.12-3.14.
- Pre-record qualification: the corrected CPython 3.12 suite passes 2,579
  tests with 15 capability skips; the prior complete 3.13 and 3.14 suites plus
  the strengthened 17-case cross-version proof remain green. All 1,039
  architecture assertions and the 350-case M64-M86 lineage pass with one
  Windows capability skip each. Static/type/docs, real wgpu, profiles, both
  sample applications, M1-M4 diagnostics, reproducible distributions,
  isolated-wheel smoke, deterministic staging, and complete release smoke
  pass. Exact recorded-tree qualification and publication remain active.
- Hosted qualification: ready PR #210 exact DCO head
  `9ddf5a8852dfc127819eb4809d1aae142ed58625`, tree
  `99ce8b240ef1403f0a2475bb844cfc045a0139c6`, passed exact-head run
  `31789378596`, classified substantive with 16 paths, in exactly three
  allocations. Linux completed in 7m28s, macOS in 1m57s, and Windows in 4m24s.
- Hosted tests: Linux CPython 3.12/3.13/3.14 and both desktop CPython 3.14
  suites passed 2,584 tests, with one capability skip outside Linux baseline.
  Every OS passed 10 real-wgpu tests, graphics profiling, Clockwork Arena, and
  Agent World Builder. Static/docs, reproducibility, isolated-wheel smoke,
  deterministic ten-artifact staging, and complete release smoke passed.
- Hosted artifacts: exact-head reproducibility produced a pure 275,547-byte
  wheel at
  `2c7a6c8df143bc0f84c9ee4ba3cfe3f19f78e89310bd6e10b26224638a1c85ae`
  and 1,343,247-byte source distribution at
  `eb99650bf5555b09634fe0a1f026c1531acd29cabb66a6a212162de2f37fd879`.
- Review/integration: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, three successful checks, matching DCO identity, and zero
  feedback. Exact-head-guarded squash
  `1f8368c915c9f414ec51ea8af835241d7c3efea5` has the exact qualified tree,
  sole M85-closeout parent `3eb38c5e591f0d73687293f130254d8c8b3256c7`,
  parsed DCO, and valid GitHub verification at `2026-08-14T09:58:53Z`. No
  postmerge run was allocated; the feature branch is deleted locally/remotely.
- Integration-local evidence: exactly the three project records plus roadmap
  change. The unchanged 46-package lock resolves; all 329 files are format/
  Ruff clean; strict Pyright has zero findings; all 1,039 architecture
  assertions pass with 1 Windows capability skip; strict docs, whitespace,
  and Git-object checks pass. Two builds reproduce a 275,560-byte wheel at
  `808078f5ccf8c60f3ae282ff2be5663a0c6d46e08ea8a539b2d83fe5cd75b58c`
  and 1,344,302-byte source distribution at
  `f8c2afa5cbef2fdb0dec95bb088e050234f47e4c14e4cf6317bc146663474f75`;
  isolated-wheel, staging, and release smoke pass.
- Hosted integration: ready PR #211 exact DCO head
  `53cef7f8d37b27e85afe06aecc7fcb5c297b47ff`, tree
  `0304c87018f6e2a31d2037c0b859a63fec0f9e76`, passed run `31790820557`.
  Classification was documentation-only with four paths. The sole Linux job
  passed in 48 seconds; the desktop umbrella skipped with zero steps. Strict
  docs, 1,040 architecture assertions, reproducibility, isolated-wheel,
  staging, and complete release smoke passed.
- Hosted integration artifacts: the feature-identical 275,547-byte wheel is
  `2c7a6c8df143bc0f84c9ee4ba3cfe3f19f78e89310bd6e10b26224638a1c85ae`;
  the 1,344,678-byte record-updated source distribution is
  `9332b54152eb5deae3abf12cdba07ebd360f5d9982d02ad5caa866049e578b7a`.
- Integration review/squash: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, one successful Linux check, one skipped zero-step
  desktop umbrella, matching DCO identity, and zero feedback. Guarded squash
  `cfc71a3e010e79652d450e1284a37c19e74df4f2` has the exact reviewed tree,
  sole feature-squash parent `1f8368c915c9f414ec51ea8af835241d7c3efea5`,
  parsed DCO, and valid GitHub verification at `2026-08-14T10:08:28Z`. No
  postmerge run was allocated; the integration branch is deleted locally and
  remotely.
- Closeout scope: exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` change. No
  workflow-classified, public, runtime, test, build, dependency, release,
  credential, identity, native, WASM, bytecode, or generated-artifact surface
  is added.

## M85 conventional central-directory placement preflight - closeout active

- Base: exact verified M84 closeout squash
  `5b21c4798c16fb69b8ef08d40b02a2662677227a`, tree
  `eb1e76fb5ccf1fb151acbfb4bb149c55c31ba06b`. Clean synchronized `main` was
  the only local/remote branch; no open PR, tag, release, postmerge run,
  disclosure marker, or M84 generated target remained before M85 selection.
- Gap: PKWARE defines conventional central-directory size and offset. Exact
  installed CPython 3.12.13, 3.13.13, and 3.14.5 accepts arbitrary prepended
  bytes by computing a concatenation adjustment: one- and eleven-byte prefixes
  preserve the same readable payload and shift the parsed header offset by the
  prefix length. The fixed producer starts at byte zero.
- Decision: after every policy through M84, private complete release smoke
  requires declared central-directory size plus offset to equal the absolute
  final-record offset before M77 name policy, metadata, inventory, staging, or
  reads. The stable content-silent error is `sample bundle central directory
  placement is inconsistent`.
- Boundary: one arithmetic relationship only. No central-directory/local-
  header parser, end-record search, ZIP64 parser, executable classifier,
  prepended executable or self-extracting archive support, multi-volume
  assembler, workflow, producer, dependency, runtime API, or release authority
  is added.
- Red-to-green: the static-clean authoritative baseline passed 6 controls and
  failed 13 missing contracts in 0.71 seconds. The placement implementation and
  shared structural helper make 80 M83-M85 runtime assertions pass in 0.51
  seconds; only the deliberately absent public/RFC contract remained before
  documentation was added.
- Qualification: review corrected an evidence overclaim without finding a
  production defect and added a negative-adjustment extraction-path control.
  The 20-case contract passes on CPython 3.12-3.14; the corrected CPython 3.12
  suite passes 2,562 tests with 15 skips; all 1,022 architecture assertions and
  the 333-case M64-M85 lineage pass with one Windows capability skip each.
  Static/type/docs, real wgpu, profiles, both sample applications, M1-M4
  diagnostics, reproducible distributions, isolated-wheel smoke,
  deterministic staging, and complete release smoke pass.
- Hosted qualification: ready PR #207 exact DCO head
  `6b1d7ef2c712c4d80a6bc4538e7ded3aec3ee5d5`, tree
  `b3cab8d267fa26954b7ef2fe36d9dba530f3d393`, passed exact-head run
  `31739467587`, classified substantive with 16 paths, in exactly three
  allocations. Linux completed in 7m22s, macOS in 2m24s, and Windows in 4m14s.
- Hosted tests: Linux CPython 3.12/3.13/3.14 and both desktop CPython 3.14
  suites passed 2,567 tests, with one capability skip outside Linux baseline.
  Every OS passed 10 real-wgpu tests, graphics profiling, Clockwork Arena, and
  Agent World Builder. Static/docs, reproducibility, isolated-wheel smoke,
  deterministic ten-artifact staging, and complete release smoke passed.
- Hosted artifacts: exact-head reproducibility produced a pure 275,471-byte
  wheel at
  `1043613c43be614ef21ca34f56bf6da98323d380d47fc90a3d9997dc5a785ef5`
  and 1,336,967-byte sdist at
  `cfa907e23b9d74ae6168c9b40592d6dfc244a3700e12a9ef23e89c65a95bbb8f`.
- Review/integration: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, three successful checks, matching DCO identity, and zero
  feedback. Exact-head-guarded squash
  `c9bb569fc1476d1aaf92c4fb01bfd9210d0398ed` has the exact qualified tree,
  sole M84-closeout parent `5b21c4798c16fb69b8ef08d40b02a2662677227a`,
  parsed DCO, and valid GitHub verification at `2026-08-13T20:23:29Z`. No
  postmerge run was allocated; the feature branch is deleted locally/remotely.
- Integration-local evidence: exactly the three project records plus roadmap
  change. The unchanged 46-package lock resolves; all 328 files are format/
  Ruff clean; strict Pyright has zero findings; all 1,022 architecture
  assertions pass with 1 Windows capability skip; strict docs, whitespace,
  and Git-object checks pass. Two builds reproduce a 275,486-byte wheel at
  `d290ade15c82ba8dc652b13fa7c14d63f90a87b6bdfa7991ce2cca680818c5f6`
  and 1,337,914-byte sdist at
  `0de7a63cbb7f36172926689e33b8cf6434ca9682f9a7df61972c1e28a313b03c`;
  isolated-wheel, staging, and release smoke pass.
- Hosted integration: ready PR #208 exact DCO head
  `a44e540c282673064535aa3ab8f63454886894a3`, tree
  `7db97bfbfbcf5b1e480c143c8b339a6ba69f9fba`, passed run `31741059247`.
  Classification was `documentation` with four paths. The sole Linux job
  passed in 42 seconds; the desktop umbrella skipped with zero steps. Strict
  docs, 1,023 architecture assertions, reproducibility, isolated-wheel,
  staging, and complete release smoke passed.
- Hosted integration artifacts: the feature-identical 275,471-byte wheel is
  `1043613c43be614ef21ca34f56bf6da98323d380d47fc90a3d9997dc5a785ef5`;
  the 1,338,272-byte record-updated sdist is
  `837eb2bddb871fd64bf0d9d4ae5c331ee4632ec8e4ad1687c4c5515233b5dbfd`.
- Integration review/squash: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, one successful Linux check, one skipped zero-step
  desktop umbrella, matching DCO identity, and zero feedback. Guarded squash
  `c83a25012c7a0b3520852d35c55a4fc362a9e559` has the exact reviewed tree,
  sole feature-squash parent `c9bb569fc1476d1aaf92c4fb01bfd9210d0398ed`,
  parsed DCO, and valid GitHub verification at `2026-08-13T20:31:01Z`. No
  postmerge run was allocated; the integration branch is deleted locally and
  remotely.
- Closeout scope: exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` change. No
  workflow-classified, public, runtime, test, build, dependency, release,
  credential, identity, native, WASM, bytecode, or generated-artifact surface
  is added.

## M84 conventional archive entry-count preflight - closeout active

- Base: exact verified M83 closeout squash
  `1c380897fc8ee43f5885c733c1c11f87878ff2a1`, tree
  `c5bcfb19be359c828bcdd413f784ff4a9fa204e7`. Clean synchronized `main` was
  the only local/remote branch; no open PR, tag, release, postmerge run,
  disclosure marker, or M83 generated target remained before M84 selection.
- Gap: PKWARE defines two conventional EOCD entry counts. Exact installed
  CPython 3.12.13, 3.13.13, and 3.14.5 parses but ignores them for ordinary
  archives: zero, asymmetric, inflated, and `0xFFFF` pairs preserve one parsed
  member and readable deflated payload. The fixed producer emits 50 in both
  fields and exposes 50 members.
- Decision: after every M69-M82 policy pass and M83 archive disk check, private
  complete release smoke reads exactly the final conventional record from its
  owned checksum-admitted snapshot. It requires both entry counts to equal the
  parsed member count before M77 name policy, metadata, inventory, staging, or
  reads. The stable content-silent error is `sample bundle archive entry counts
  are inconsistent`.
- Boundary: `0xFFFF` is rejected as outside the fixed conventional profile,
  not resolved through a ZIP64 end record. No new record grammar, end-record
  search, local/central-header parser, neighboring-volume discovery, multi-
  volume assembler, workflow, producer, dependency, runtime API, or release
  authority is added.
- Red-to-green: the static-clean authoritative baseline passed 9 controls and
  failed 16 missing contracts in 0.50 seconds. The runtime implementation made
  24 assertions pass in 0.31 seconds; only the deliberately absent public/RFC
  contract remained before documentation was added.
- Qualification: review found no production defect and added direct malformed-
  final-record normalization controls while correcting stale status wording.
  The strengthened contract passes on CPython 3.12-3.14; the corrected 3.12
  suite passes 2,542 tests with 15 skips; 1,002 architecture assertions and
  the 313-case M64-M84 lineage pass with one Windows capability skip each.
  Static/docs, real wgpu, profiles, samples, diagnostic validators,
  reproducible builds, isolated-wheel smoke, deterministic staging, and
  complete release smoke pass.
- Hosted qualification: ready PR #204 exact DCO head
  `5c9d4cffb1392b4c7de960544ad13971c6db512b`, tree
  `1a2bc67118919a6c6090f6bdf14794859f6bc452`, passed exact-head run
  `31734854012`, classified substantive with 16 paths, in exactly three
  allocations. Linux completed in 7m17s, Windows in 4m09s, and macOS in 2m21s.
- Hosted tests: Linux CPython 3.12/3.13/3.14 and both desktop CPython 3.14
  suites passed 2,547 tests, with one skip outside baseline. Every OS passed
  10 real-wgpu tests, graphics profiling, Clockwork Arena, and Agent World
  Builder. Static/docs, reproducibility, isolated-wheel smoke, deterministic
  ten-artifact staging, and complete release smoke passed.
- Hosted artifacts: exact-head reproducibility produced a pure 275,344-byte
  wheel at
  `25a99abc2bd6f73ee15ccf1ebf524ad29854b34303321b087e8a53f2ab3858d9`
  and 1,329,869-byte sdist at
  `9e1b4ff35c3b6ddcd95c5e442f30ff0e627cce91b89b6ee60f85c237a42b4560`.
- Review/integration: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, three successful checks, matching DCO identity, and zero
  comments, reviews, inline comments, or review threads. Exact-head-guarded
  squash `1ec97d0e5003dd92f21be6f49b528765de19506a` has the exact qualified
  tree, sole M83-closeout parent `1c380897fc8ee43f5885c733c1c11f87878ff2a1`,
  parsed DCO, and valid GitHub verification at `2026-08-13T19:27:56Z`. No
  postmerge run was allocated; the feature branch is deleted locally/remotely.
- Integration-local evidence: exactly the three project records plus roadmap
  change. The unchanged 46-package lock resolves; all 327 files are format/
  Ruff clean; strict Pyright has zero findings; all 1,002 architecture
  assertions pass with 1 Windows capability skip; strict docs, whitespace,
  and Git-object checks pass. Two builds reproduce a 275,358-byte wheel at
  `93750692bd8fddc37c9043c0fdfff46c3cce99f9bf15d0dec17189e530d40d20`
  and 1,331,078-byte sdist at
  `7e47faca5ebd49b5e688019c66deb2f465e1f7b74de455926989813e87c8324e`;
  isolated-wheel, staging, and release smoke pass.
- Hosted integration: ready PR #205 exact DCO head
  `80e3ab0fd5f367f98a8e645adbd7b825faf37e87`, tree
  `f2041834401bd363e893c2363631d150819dc7df`, passed run `31736409489`.
  Classification was `documentation` with four paths. The sole Linux job
  passed in 30 seconds; the desktop umbrella skipped with zero steps. Strict
  docs, 1,003 architecture assertions, reproducibility, isolated-wheel,
  staging, and complete release smoke passed.
- Hosted integration artifacts: the feature-identical 275,344-byte wheel is
  `25a99abc2bd6f73ee15ccf1ebf524ad29854b34303321b087e8a53f2ab3858d9`;
  the 1,331,514-byte record-updated sdist is
  `59083d42a9f22fe2da878889d686ffcc0f9ae54ff32c28f3f4281d60df900da5`.
- Integration review/squash: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, one successful Linux check, one skipped zero-step
  desktop umbrella, matching DCO identity, and zero feedback. Guarded squash
  `55657872aac9e9f7b29df99b14a2bee4d8f67397` has the exact reviewed tree,
  sole feature-squash parent `1ec97d0e5003dd92f21be6f49b528765de19506a`,
  parsed DCO, and valid GitHub verification at `2026-08-13T19:34:56Z`. No
  postmerge run was allocated; the integration branch is deleted locally and
  remotely.
- Closeout-local evidence: exactly the three project records change. The
  unchanged lock resolves; all 327 files remain format/Ruff clean with zero
  Pyright findings; all 1,002 architecture assertions pass with 1 Windows
  capability skip; strict docs, whitespace, and Git-object checking pass.

## M83 conventional archive disk-field preflight - closeout active

- Base: exact verified M82 closeout squash
  `e0ade9928e19895d5074a40fd11fcbf6bfa6fbe0`, tree
  `fc19f02ae8af1a432d23f0ccf8e4775ef10085c7`. Clean synchronized `main` was
  the only local/remote branch; no open PR, tag, release, postmerge run, or M82
  generated target remained before M83 selection.
- Gap: PKWARE defines two conventional EOCD disk fields. Exact installed
  CPython 3.12.13, 3.13.13, and 3.14.5 parses but ignores them for ordinary
  archives: asymmetric one values, matching one values, and matching `0xFFFF`
  sentinels preserve a volume-zero member and readable deflated payload. The
  fixed producer emits both fields as zero.
- Decision: after all M69-M82 archive-wide passes, private complete release
  smoke reads exactly the final 22-byte conventional record from its owned
  checksum-admitted snapshot. It requires the signature, zero comment length,
  and both disk fields zero before M77 name policy, metadata, inventory,
  staging, or reads. The stable content-silent error is `sample bundle uses
  unsupported archive disk fields`.
- Boundary: `0xFFFF` is rejected as outside the fixed conventional profile,
  not classified as a split archive. No ZIP64 end-record parser, end-record
  search, local/central-header parser, neighboring-volume discovery, multi-
  volume assembler, workflow, producer, dependency, runtime API, or release
  authority is added.
- Red-to-green: the static-clean authoritative baseline passed 16 controls and
  failed 15 missing contracts in 0.52 seconds. The runtime implementation made
  30 assertions pass in 0.32 seconds; only the deliberately absent public/RFC
  contract remained before documentation was added.
- Qualification: after review strengthening, all 34 focused assertions pass on
  CPython 3.12.13, 3.13.13, and 3.14.5. The complete corrected 3.12 graphics-
  baseline suite passes 2,514 tests with 15 capability skips; initial complete
  3.13/3.14 suites each passed 2,501 with 16 skips before the test-only review
  strengthening. All 974 architecture assertions pass with 1 Windows skip;
  the M64-M83 lineage passes 285 with 1 skip. Static checks, strict docs, real-
  wgpu, profiles, both vertical slices, M1-M4 diagnostics, byte-reproducible
  builds, isolated-wheel smoke, staging, and complete release smoke pass.
- Review: documentation navigation was corrected after its first strict-build
  failure. Findings-first review found no production defect but added three
  controls proving malformed final-record signature/comment-length/trailing-
  byte shapes retain the existing stable ZIP-data error. Exactly 16 intended
  paths change; protected hashes, disclosure/credential scans, artifact
  inventories, whitespace, and Git-object checks are clean.
- Local artifacts: the corrected tree reproduces a pure 275,238-byte wheel at
  `2c7b187266cebac06a3478ea3f5a0c515e38175ee74bda809a09f07eb2acc788`
  and a 1,322,725-byte sdist at
  `6e01c1f0f3a68fb3ddcadaf1ec7232082217c3aee6e57d47094b0801dbf06cdf`;
  the evidence-record update changes the future sdist, so hosted exact-head
  identities remain authoritative.
- Hosted qualification: ready PR #201 exact DCO head
  `66045e4cebfcd857f332a511bd16286ea0a109d0`, tree
  `7ee06883ce29e75e9f8d6d972f00c4bde85f119e`, passed exact-head run
  `31730269653`, classified substantive with 16 paths, in exactly three
  allocations. Linux completed in 8m02s, Windows in 4m00s, and macOS in 2m40s.
- Hosted tests: Linux CPython 3.12/3.13/3.14 and both desktop CPython 3.14
  suites passed 2,519 tests, with one skip outside baseline. Every OS passed
  10 real-wgpu tests, graphics profiling, Clockwork Arena, and Agent World
  Builder. Static/docs, reproducibility, isolated-wheel smoke, deterministic
  ten-artifact staging, and complete release smoke passed.
- Hosted artifacts: exact-head reproducibility produced a pure 275,225-byte
  wheel at
  `e6e219f4f6d3c0a5d128f0374a47c9004a239b56acd42b24eb509f660a5cefb8`
  and 1,323,928-byte sdist at
  `ff931882e9b83e77084951ac235c8f9ad47eaa4c93e983d7146887f35281fd08`.
- Review/integration: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, three successful checks, matching DCO identity, and zero
  comments, reviews, inline comments, or review threads. Exact-head-guarded
  squash `870141014c540984420933122028ed870fa22119` has the exact qualified
  tree, sole M82-closeout parent `e0ade9928e19895d5074a40fd11fcbf6bfa6fbe0`,
  parsed DCO, and valid GitHub verification at `2026-08-13T18:35:45Z`. No
  postmerge run was allocated; the feature branch is deleted locally/remotely.
- Integration-local evidence: exactly the three project records plus roadmap
  change. The unchanged 46-package lock resolves; all 326 files are format/
  Ruff clean; strict Pyright has zero findings; all 974 architecture assertions
  pass with 1 Windows capability skip; strict docs, whitespace, and Git-object
  checks pass. Two builds reproduce a 275,238-byte wheel at
  `2c7b187266cebac06a3478ea3f5a0c515e38175ee74bda809a09f07eb2acc788`
  and 1,325,277-byte sdist at
  `9bf9d818c94d4eeeb53008d5fa41a49481a0a841741e9a8922f2818866838788`;
  isolated-wheel, staging, and release smoke pass. Protected and added-content
  hygiene remains clean.
- Hosted integration record: ready PR #202 exact DCO head
  `e2ebc31e1de15dd8486e8927627645593c43785b`, tree
  `f65121dcc2c5945e41517666d1307860da831f9c`, classified documentation with
  four paths. Run `31731878660` used only 48-second Linux job `94554071714`;
  desktop umbrella `94554309063` skipped with zero steps. All 326 files were
  format/Ruff clean; strict docs built in 1.85 seconds; all 975 hosted
  architecture assertions passed in 10.95 seconds. Installed-wheel, staging,
  and complete release smoke passed.
- Hosted integration artifacts: same-head reproducibility produced a 275,225-
  byte pure wheel at
  `e6e219f4f6d3c0a5d128f0374a47c9004a239b56acd42b24eb509f660a5cefb8`
  and 1,325,644-byte sdist at
  `d3568d29a44f46c6dcefd381a46ba463bd44331c7d1c9a6dc8c08041cd89984`.
- Integration audit: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, one successful bounded Linux check, one skipped zero-
  step desktop umbrella, and zero comments, reviews, or threads. Exact-head-
  guarded squash `de334e3ea93aeed299ae2913ed80d05ec1fa7575` has exact reviewed
  tree, sole feature-squash parent `870141014c540984420933122028ed870fa22119`,
  parsed DCO, and valid GitHub verification at `2026-08-13T18:42:09Z`. No
  postmerge run was allocated; the integration branch is deleted locally/
  remotely.
- Closeout scope: exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` change. No
  workflow, runtime, verifier, producer, dependency, package, test, public
  documentation, roadmap, or release-authority surface changes.

## M82 split-volume sample-member preflight - closeout active

- Base: exact verified M81 closeout squash
  `ba90021304760284550e3c458901feb0e3e29dbc`, tree
  `63a1caf2bc270a6500466e24c800f4e6f454ddda`. Clean synchronized `main` was the
  only local/remote branch; no open PR, tag, release, postmerge run, or M81
  generated target remained before M82 selection.
- Gap: PKWARE APPNOTE section 4.4.13 defines central-directory disk number
  start as the disk on which a file begins. CPython assigns the parsed field to
  `ZipInfo.volume`. Installed CPython 3.12.13, 3.13.13, and 3.14.5 each exposed
  patched value one, no extra field, no general-purpose flag, and still read
  the same deflated payload. The fixed producer emits 50 volume-zero members.
- Decision: private complete release smoke retains every established flag,
  descriptor, Unicode Path, ZIP64, archive-comment, and member-comment pass,
  then rejects every nonzero parser-exposed `ZipInfo.volume` in a separate all-
  member pass before M77 decoded-name policy, metadata, exact inventory,
  staging, or reads. The stable content-silent error is `sample bundle uses a
  split-volume member`.
- Ownership: the existing `ExitStack` closes the caller-opened source, owned
  checksum-admitted snapshot, and `ZipFile` before the error returns. No member
  is opened and no staging directory or final sample root is created.
- Red-to-green: the static-clean authoritative baseline passed 12 controls and
  failed 8 missing policy, ordering, cleanup, helper/source, and documentation
  contracts in 0.42 seconds. One separate pass and typed validator make 19
  assertions pass in 0.29 seconds; only the deliberately absent documentation
  contract remained at the runtime checkpoint. RFC-0065 and aligned public
  docs are now implemented.
- Qualification: all 325 Python files are format clean; Ruff and strict
  Pyright report zero findings; all 940 architecture assertions pass with 1
  Windows capability skip; the exact M64-M82 lineage passes 251 assertions
  with 1 skip. The corrected CPython 3.12 suite passes 2,480 tests with 15
  skips. Pre-correction complete 3.13/3.14 suites each passed 2,470 with 16
  skips, and the corrected 20-case sentinel/precedence contract passes on
  3.12.13, 3.13.13, and 3.14.5. Ten real-wgpu tests, both profiles, Clockwork
  Arena, Agent World Builder, M1-M4 diagnostic validators, two-build byte
  reproducibility, isolated-wheel smoke, deterministic ten-artifact staging,
  complete release smoke, and strict docs pass.
- Review: the first findings-first pass found the ZIP64-precedence fixture used
  volume one rather than the documented `0xFFFF` sentinel and RFC-0065 split
  the stable error inside its code span. Both are corrected. Exact nonzero-
  volume policy, archive-wide ordering, content-silent failure, ownership,
  producer compatibility, public nonclaims, and protected surfaces now have no
  remaining actionable finding. Exactly 15 intended paths change; identity,
  credential, native/WASM/bytecode, and retired-control-metadata scans are
  empty.
- Initial hosted qualification: ready PR #198 exact DCO head `d7e1eef7e857ef82a26af5ae27f2418592bfa745`
  passed run `31723899463` in exactly three allocations: Linux 7m13s, Windows
  4m07s, and macOS 3m08s. Linux CPython 3.12/3.13/3.14 and both desktop 3.14
  suites passed 2,485 tests, with one compatibility skip on non-baseline runs;
  every OS passed 10 real-wgpu tests, graphics profiles, and both vertical
  slices. Static/docs, reproducibility, installed-wheel, staging, and release
  smoke passed. The classifier reported substantive with 15 paths.
- Hosted review correction: audit found the central disk-start sentinel
  `0xFFFF` was combined with a ZIP64 field containing only the three 64-bit
  values, not the format-defined following 32-bit disk-start value. The
  production policy is unchanged. The test helper now conditionally appends
  that value and the precedence case observes the well-formed field, parser-
  exposed sentinel, and readable payload. Initial-head CI is retained only as
  superseded evidence; a fresh exact-head run is required.
- Corrected local evidence: all 20 focused assertions pass on CPython 3.12.13,
  3.13.13, and 3.14.5 in 0.27/0.61/0.62 seconds. Affected format, Ruff, strict
  Pyright, strict docs, and whitespace pass. The complete corrected 3.12
  graphics-baseline suite passes 2,480 tests with 15 capability skips in
  109.01 seconds.
- Corrected hosted qualification: exact DCO head
  `9edbe5e5bf706bd11b31546bd26fcb8421f1f5d9`, tree
  `63677710315e48d32d83115bef5046476e669dd1`, passed run `31725451119`,
  classified substantive with 15 paths, in exactly three allocations. Linux
  job `94532583017` completed in 7m12s, Windows `94534595607` in 4m17s, and
  macOS `94534595665` in 2m16s. Linux CPython 3.12/3.13/3.14 and both desktop
  3.14 suites passed 2,485 tests, with one skip outside baseline. Every OS
  passed 10 real-wgpu tests, graphics profiling, Clockwork Arena, and Agent
  World Builder; static/docs, installed-wheel, staging, and release smoke pass.
- Hosted artifacts: the exact corrected head reproduced a 275,086-byte pure
  wheel at `fff5a33caafb89572e74cb41dd308611cae896e1c5a62630058f157e17214b99`
  and 1,315,802-byte sdist at
  `d16eb754e00e01d59aff425fedb0bd74db318c1b7e9ab044af3343c9a9db2a46`.
- Review/integration: the valid P2 thread has a concrete correction response and
  is resolved/outdated. Two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, three successful checks, zero issue comments, and no
  unresolved or later finding. Exact-head-guarded squash
  `f34b42f1ac9813ec2c46063774e8e86087dd67cf` has the exact reviewed tree,
  sole M81-closeout parent `ba90021304760284550e3c458901feb0e3e29dbc`,
  parsed DCO, and valid GitHub verification at `2026-08-13T17:37:04Z`.
  No postmerge run was allocated; the feature branch is deleted locally/
  remotely and synchronized `main` was the only branch before this record.
- Integration-local evidence: exactly the three project records plus roadmap
  change. The unchanged 46-package lock resolves; all 325 files are format/
  Ruff clean; strict Pyright has zero findings; all 940 architecture assertions
  pass with 1 Windows capability skip; strict docs, whitespace, and Git-object
  checks pass. Two builds reproduce a 275,100-byte wheel at
  `b0fb35139e5c6bc47beb133d3602bd83b050ff282e78465a9708e3b996e01da5`
  and 1,317,216-byte sdist at
  `b668144e40744981c7b2e5b03dbeb885f31b2394c2a44996d1a4084e7e50ed96`;
  isolated-wheel, staging, and release smoke pass. Protected hashes and added-
  content identity/credential scans remain clean.
- Hosted integration record: ready PR #199 exact DCO head
  `78e440e87a3af11fa7123f40596bead906ef5786`, tree
  `53295683df88430e6731fb75a794836ccafdc9f9`, classified documentation with
  four paths. Run `31727082001` used only 43-second Linux job `94538032073`;
  desktop umbrella `94538237840` skipped with zero steps. All 325 files were
  format/Ruff clean; strict docs built in 1.71 seconds; all 941 hosted
  architecture assertions passed in 10.40 seconds. Installed-wheel, staging,
  and complete release smoke passed.
- Hosted integration artifacts: same-head reproducibility produced a 275,086-
  byte pure wheel at
  `fff5a33caafb89572e74cb41dd308611cae896e1c5a62630058f157e17214b99`
  and 1,317,719-byte sdist at
  `030ba0cc1a60452af81c260771c7ade982f576fc8753602e867766a5b8a40833`.
- Integration audit: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, one successful bounded Linux check, one skipped zero-
  step desktop umbrella, and zero comments, reviews, or threads. Exact-head-
  guarded squash `f0558e4e3864e54d8bf81c46c656becc505c7f80` has exact reviewed tree,
  sole feature-squash parent `f34b42f1ac9813ec2c46063774e8e86087dd67cf`,
  parsed DCO, and valid GitHub verification at `2026-08-13T17:44:59Z`. No
  postmerge run was allocated; the integration branch is deleted locally/
  remotely.
- Closeout-local evidence: exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` change. All 325
  files are format/Ruff clean; strict Pyright has zero findings; all 940
  architecture assertions pass with 1 Windows capability skip; strict docs,
  whitespace, and Git-object checks pass. Protected hashes and added-content
  identity/credential scans are unchanged/empty. No workflow, runtime,
  verifier, producer, dependency, package, test, public documentation, roadmap,
  or release-authority surface changes.
- Boundary: no raw end-record parser, local-header parser, multi-volume
  assembler, neighboring-volume discovery, broad flag/extra-field rule,
  workflow, allocation, dependency, lock, version, producer, runtime package/
  API, release mutation, release authority, tag, release, or publication is
  added. This is not a general archive sandbox or real public release
  observation.
- Branch: `release/m82-closeout`.
- Remaining: hosted-excluded three-record closeout and branch/generated-target
  cleanup before clean-main M83 selection.

## M81 ZIP comment preflight - closed

- Base: exact verified M80 closeout squash
  `3241a348a75c24a764f167ade48798ed3ac06af1`, tree
  `f5a1375cff72dfbbffa8ba755210815dac1bdfd7`. PR #194 merged the exact
  reviewed closeout tree with sole integration parent, matching DCO identity,
  and valid GitHub verification. Its false-positive DCO review thread was
  answered from the published Git object and resolved. Only synchronized
  `main` remained locally/remotely; no open PR, tag, release, or M80 generated
  target remained before M81 selection.
- Gap: PKWARE defines an end-of-central-directory archive comment and a per-
  member central-directory file comment. Installed CPython 3.12.13, 3.13.13,
  and 3.14.5 preserve both exact byte strings while reading the same deflated
  payload; the probe exposed no member extra field or general-purpose flag.
  The fixed producer emits 50 members with neither comment surface.
- Decision: private complete release smoke retains every established
  M69/M75/M76/M78/M79/M80 archive-wide category, then rejects a parser-exposed
  non-empty archive comment, rejects every non-empty member comment in a
  separate pass, and only then begins M77 decoded-name policy, metadata, exact
  inventory, staging, or reads. Stable content-silent errors are `sample bundle
  uses an archive comment` and `sample bundle uses a member comment`.
- Ownership: the existing `ExitStack` closes the caller-opened source, owned
  checksum-admitted snapshot, and `ZipFile` before either error returns. No
  member is opened and no staging directory or final sample root is created.
- Contract: 26 M81 assertions cover actual CPython behavior, archive/member
  policy, exact errors, no-read/no-staging/no-inventory ordering, cleanup,
  every established flag category, Unicode Path/ZIP64 precedence, archive-
  before-member precedence, comment-before-NUL ordering, direct validator
  behavior, the 50-member producer invariant, source ordering, protected
  hashes, runtime-package absence, and public nonclaims.
- Documentation: RFC-0064 and README, changelog, security, maintainer,
  architecture, release-process, RFC-index, MkDocs navigation, roadmap, and
  repository evidence records define the exact private boundary. One focused
  documentation regression initially failed because the RFC did not contain
  exact phrase `no general comment scanner`; the wording was corrected and all
  26 focused assertions plus strict docs then passed.
- Qualification: all 324 Python files are format clean; Ruff and strict
  Pyright report zero findings; 920 architecture assertions pass with 1
  Windows capability skip; the exact M64-M81 lineage passes 231 assertions
  with 1 skip. CPython 3.12.13, 3.13.13, and 3.14.5 each pass 2,450 tests with
  15/16/16 capability skips. Ten real-wgpu tests, both profiling contracts,
  Clockwork Arena, Agent World Builder, M1-M4 diagnostic validators, two-build
  reproducibility, isolated-wheel smoke, deterministic ten-artifact staging,
  complete release smoke, strict docs, whitespace, and Git-object checks pass.
- Review: findings-first review tightened all public claims to parser-exposed
  comments because malformed raw records can fail earlier through the existing
  stable ZIP-data boundary. The corrected exact contract passes 26 assertions
  and strict docs. Exactly 15 intended paths change; protected workflow,
  producer, package, and lock hashes are unchanged; added-line identity and
  credential scans are empty; the 94-entry wheel and 528-entry sdist contain
  no native, WASM, bytecode, or retired control metadata. No remaining
  actionable finding was identified.
- Hosted feature gate: ready PR #195 exact DCO head
  `fbff420391675c6519c606a251cc4a697efe9d62` passed run `31718815561` in
  exactly three allocations. Linux job `94510280379` completed in 7m08s;
  macOS `94512364384` in 2m30s; Windows `94512364395` in 4m10s. Linux CPython
  3.12 passed 2,465 tests; Linux 3.13/3.14 and both desktop 3.14 suites passed
  2,465 with one capability skip. Every OS passed 10 real-wgpu tests, graphics
  profiling, Clockwork Arena, and Agent World Builder. Static/docs, installed-
  wheel, deterministic staging, and complete release smoke passed.
- Hosted artifacts: same-head reproducibility produced a pure 274,962-byte
  wheel at `71faae79b33898e5ed417445bdb14793b934efb01c464db73e0f40eec173342e`
  and 1,306,054-byte sdist at
  `6d257296b8595e76cc1f1fdb73cdfea31d5152013c63ca1d69859e9ea40ef27f`.
- Review/integration: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, three successful checks, and zero issue comments,
  reviews, inline comments, or threads. Exact-head-guarded squash
  `8a3a156d08a7c40c9b34ae726311776c0e2f8611` has tree
  `30d6bf6db4272279c3f32dc3c9901399018e55bc` exactly equal to the qualified
  head, sole M80-closeout parent
  `3241a348a75c24a764f167ade48798ed3ac06af1`, standalone DCO, and valid
  GitHub verification at `2026-08-13T16:18:01Z`. No postmerge run was
  allocated; the feature branch is deleted locally/remotely.
- Integration record: exact DCO head
  `ab5cf860fcd82bce71dde458d8e0653c8415adf6`, tree
  `9a5d794198dddf925d4a52a91327f33c4352e2e3`, changed exactly four intended
  record paths. Trusted-base classification reported `documentation` with
  `changed_count: 4`. Run `31720707293` used one 42-second Linux job
  `94516687882`; desktop umbrella `94516893920` skipped with zero steps. All
  324 files were format/Ruff clean; strict docs built in 1.69 seconds; all 921
  hosted architecture assertions passed in 10.15 seconds; two universal builds,
  isolated-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke passed. Reproducibility produced a 274,962-byte wheel at
  `71faae79b33898e5ed417445bdb14793b934efb01c464db73e0f40eec173342e`
  and a 1,307,844-byte sdist at
  `2d6fe8b8fb4f97595c52addcadfe2f5c47831f631e220437885c775ddfb1d2c1`.
- Integration audit: two separated audits retained exact base/head,
  `MERGEABLE`/`CLEAN`, one successful bounded Linux check, one skipped zero-step
  desktop umbrella, and zero issue comments, reviews, inline comments, or
  threads. Exact-head-guarded squash
  `2054fda66c1dafb7c0594eada4cc01a3649209cd` has the exact reviewed tree, sole
  feature-squash parent `8a3a156d08a7c40c9b34ae726311776c0e2f8611`,
  exact author identity, and valid GitHub verification at
  `2026-08-13T16:29:37Z`. The reviewed source commit has a parsed DCO trailer;
  PowerShell passed the merge body's newline escapes literally, so the
  generated squash message itself has no parsed trailer. The process defect is
  retained factually and public history is not rewritten. No postmerge run was
  allocated; the integration branch is deleted locally/remotely.
- Scope: no raw ZIP parser, general comment scanner, comment decoder, raw end-
  record validator, broad extra-field rule, workflow, runner allocation,
  action, permission, credential, dependency, lock, version, sample producer,
  runtime package/API, release mutation, release authority, tag, release, or
  publication is added. Passing pull-request evidence is not a real public
  release observation and M81 is not a general archive sandbox.
- Branch: `release/m81-closeout`.
- Status: feature, bounded integration record, and closeout are integrated;
  branch and generated-target cleanup is complete.
- Closeout: exact DCO head `36e1ce3cf8a05aaf684074a0557cbb63a1aae95a`,
  tree `63a1caf2bc270a6500466e24c800f4e6f454ddda`, changed only the three project
  records in ready PR #197. It allocated no workflow run. Two separated audits
  retained exact integration base/head, `MERGEABLE`/`CLEAN`, no checks, and
  zero review activity. Exact-head-guarded squash
  `ba90021304760284550e3c458901feb0e3e29dbc` has the exact reviewed tree, sole
  integration-record parent `2054fda66c1dafb7c0594eada4cc01a3649209cd`,
  parsed DCO, and valid GitHub verification at `2026-08-13T16:35:36Z`.
- Final cleanup: no postmerge run was allocated; remote/local closeout branches
  were deleted. A first guarded cleanup removed 33 M81 targets and the sandbox
  denied 15 test directories; the approved identical-path retry removed all 15.
  Local/remote refs then contained only exact synchronized `main`; open PR,
  release, tag, and M81-target queries were empty. Full Git-object checking
  reported only historical unreachable objects and no corruption.

## M80 ZIP64 extra-field preflight - closeout active

- Base: exact clean synchronized M79 closeout
  `892f17fce99d218905c6f624c730f735d21a794f`, tree
  `1fca519b95832978516a22c3c6bd19ff93955afd`.
- Gap: PKWARE defines extra-field ID `0x0001` as ZIP64 alternate 64-bit size,
  compressed-size, local-header-offset, and disk-start metadata. Current
  CPython applies the size and header-offset values to `ZipInfo` when central-
  directory fields use sentinels; it does not consume the defined disk-start
  value. The fixed small sample producer emits no extra fields and has no need
  for this alternate metadata representation.
- Runtime evidence: corrected sequential stdlib-only probes on installed
  CPython 3.12.13, 3.13.13, and 3.14.5 each applied genuine central-directory
  ZIP64 values for a 13-byte payload, exposed the 28-byte `0x0001` field, and
  read the payload. A first concurrent probe attempt is invalid setup evidence:
  three uv processes raced over the shared `.venv` and none reached the probe.
  The locked CPython 3.12 graphics environment was restored afterward.
- Decision: add exact `0x0001` preflight through a bounded extra-field walk in
  a separate all-member pass after M79 Unicode Path policy and before M77
  names, metadata, inventory, staging, or reads.
- Boundary: no broad extra-field ban, raw ZIP64 parser, ZIP64 archive-record
  validator, large-file support change, repair, workflow, dependency, sample-
  producer, runtime-API, or release-authority change; this is not a general
  archive sandbox or real public release observation.
- Red-to-green: the authoritative test-only baseline passed 13 controls and
  failed the 7 missing policy, ordering, cleanup, helper/source, and docs
  contracts. The exact constant/helper and separate all-member pass reduced
  that to one deliberately absent docs contract. RFC-0063 and aligned public
  docs make all 20 focused assertions pass; focused format, Ruff, strict
  Pyright, strict docs, and whitespace gates are clean.
- Setup note: the first strict-docs checkpoint exposed the earlier concurrent
  probe race as a damaged local MkDocs install. A sandboxed repair attempt
  could not access the shared uv cache; an approved locked-package reinstall
  restored MkDocs 1.6.1, after which strict docs passed. Neither failed setup
  attempt is product-test evidence.
- Complete local qualification: the unchanged 46-package lock and restored
  45-package graphics environment resolve; all 323 files are format clean;
  Ruff and strict Pyright report zero findings; all 894 architecture tests
  pass with 1 capability skip; the exact M64-M80 lineage passes 205 tests with
  1 skip. Supported CPython 3.12/3.13/3.14 each pass 2,424 tests with
  15/16/16 capability skips.
- Graphics/diagnostics: all 10 real-wgpu tests, both one-repeat profiles,
  Clockwork Arena, Agent World Builder, and all four M1-M4 diagnostic
  validators pass. M1 observes 1 of 2 targets, M2 has no targets, M3 meets 0
  of 2 observed targets, and M4 observes its baseline target.
- Reproducible release gate: two fresh builds reproduce a pure 274,845-byte
  wheel at
  `018f4cb0bc3d231a3fdd3479027bb7e0a483851516273f7a7609ed610edb3c84`
  and 1,295,107-byte sdist at
  `557235f0735245ebf82b7945ca77c7e183fb34af2237e613e0428ce9b8140de8`;
  isolated-wheel, deterministic ten-artifact staging, and complete release
  smoke pass.
- Findings-first review identifies no actionable defect. The exact field-ID
  check honors TLV boundaries, retains established archive-wide precedence,
  fails before names/metadata/inventory/staging/reads, renders no controlled
  content, and closes owned resources. Unrelated IDs and incomplete trailing
  bytes remain accepted; malformed declared fields remain CPython policy.
- Exact-scope audit: exactly 16 intended paths change. Protected CI, release
  workflow, sample producer, package metadata, and lock hashes remain exact;
  no runtime-package file changes. Explicit development-tool identity and
  credential/private-key scans identify no added marker. The 94-entry wheel
  and 526-entry sdist contain no native, WASM, bytecode, or retired control
  metadata.
- Final local gate: the record-inclusive tree retains the unchanged lock, 323
  format-clean files, zero Ruff/Pyright findings, 894 passing architecture
  tests with 1 capability skip, strict docs, whitespace, and Git-object
  integrity.
- History/remote: feature `HEAD`, local `main`, `origin/main`, and merge base
  are exact M79 closeout `892f17fce99d218905c6f624c730f735d21a794f`;
  symmetric difference is `0 0` and history is linear. Only `origin/main`
  exists remotely; GitHub reports no open PR, tag, or release.
- Initial hosted gate: exact DCO head
  `30793a758fc57b8a23d92b84cd911c5b979f977d` passed all three allocations in
  run `31711574308`, but review correctly found that public records blurred
  PKWARE's defined disk-start capacity with the narrower values CPython
  actually applies. The runtime policy remains sound; documentation now
  distinguishes the specification from observed parser behavior.
- Review correction checkpoint: RFC/project records now state that current
  CPython applies uncompressed size, compressed size, and local-header offset
  but does not consume the defined disk-start value. The genuine fixture is
  explicitly limited to its three 64-bit values. The strengthened docs
  regression, all 20 focused assertions, all 894 architecture tests with 1
  skip, strict static checks, strict docs, and whitespace pass.
- Final correction gate: the record-inclusive tree retains the unchanged lock,
  323 format-clean files, zero Ruff/Pyright findings, 894 passing architecture
  tests with 1 skip, strict docs, whitespace, and Git-object integrity.
- Corrected hosted qualification: exact DCO head
  `0a42620d3771bde90978a697b672d51bf66273a5`, tree
  `c7703140e53afe5cdd8a7cf61ee7e97b71737a60`, passed run `31713078940` in
  exactly three allocations. Linux job `94490785476` passed in 7m24s, macOS
  `94493098093` in 2m42s, and Windows `94493098213` in 4m28s. Every hosted
  Python suite passed 2,439 tests, with 1 capability skip on 3.13/3.14; all
  static/docs, graphics, profiles, examples, artifacts, and smokes passed.
- Corrected hosted artifacts: the pure 274,831-byte wheel is
  `149e02344b1ca8fc779f7c7e410a6f497c99da4d372ae4b76e70865a6eac9255`;
  the 1,297,189-byte sdist is
  `0bea646a029b214de2152cbddba6c4353a63be6a24bb1d82c1b55314bcc2f3d7`.
- Review/integration: two corrected-head audits found no new finding. The one
  valid initial thread has two comments, is resolved, and is outdated. PR #192
  was `MERGEABLE`/`CLEAN` with three successful checks. GitHub-verified squash
  `13439d41551cd9c842b3e7a0a55e7ba72e540582` has the exact corrected tree,
  sole M79-closeout parent, standalone DCO, and valid verification at
  `2026-08-13T15:14:33Z`.
- Branch/release state: the feature branch is deleted locally/remotely; local
  `main` and `origin/main` are exact feature squash. No open PR, tag, release,
  or publication exists.
- Integration-record local gate: exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`
  change. The unchanged lock resolves; all 323 files are format clean; Ruff
  and strict Pyright report zero findings; all 894 architecture tests pass
  with 1 capability skip; strict docs, whitespace, and Git-object integrity
  pass.
- Integration-record reproducibility: two builds reproduce a pure 274,845-byte
  wheel at
  `018f4cb0bc3d231a3fdd3479027bb7e0a483851516273f7a7609ed610edb3c84`
  and 1,298,516-byte sdist at
  `ba5af9cde94f2cff5a619e31afd4550b4e9d1074ea16a2d91923dee60280c53c`;
  isolated-wheel, deterministic ten-artifact staging, and complete release
  smoke pass. Recording these facts changes the sdist, so hosted record-head
  identities remain authoritative.
- Integration-record audit: protected CI/release/producer/package/lock hashes
  remain exact; added/current changed content contains no explicit development-
  tool identity or credential/private-key marker. Only synchronized `main`
  plus the intended integration branch exist locally; only `origin/main`
  exists remotely.
- Final record-frozen gate: the unchanged lock resolves; all 323 files remain
  format clean; Ruff and strict Pyright report zero findings; all 894
  architecture tests pass with 1 skip; strict docs, whitespace, and full Git-
  object checking pass.
- Integration hosted gate: exact four-file DCO head
  `b1e8f77da1ab73865cf08d959d7c242875bc3679`, tree
  `debee0bfa348af18509f8f5f0d7d4e01c4a8a30d`, classified as documentation in
  successful run `31714883660`. Linux job `94496955617` passed in 42 seconds
  with 895 architecture assertions, strict docs, two reproducible builds,
  installed-wheel smoke, staging, and release smoke. Desktop umbrella job
  `94497186984` skipped with zero steps.
- Integration hosted artifacts: the pure 274,831-byte wheel is
  `149e02344b1ca8fc779f7c7e410a6f497c99da4d372ae4b76e70865a6eac9255`;
  the 1,299,075-byte sdist is
  `404f5921afb71915d57c735237dc1c71b00319c0425f94c3f9da53c39489ca6f`.
- Integration audit: two separated audits found zero reviews, issue comments,
  inline comments, or threads. PR #193 was `MERGEABLE`/`CLEAN`. Verified squash
  `218c761c55e71d0367823bdac5ff2c92f4c5adf6` has exact reviewed tree, sole
  feature-squash parent, standalone DCO, and valid GitHub verification at
  `2026-08-13T15:22:59Z`.
- Branch state: feature and integration branches are deleted locally/remotely;
  synchronized `main` plus intended closeout exist locally and only
  `origin/main` remotely. No open PR, tag, release, or publication exists.
- Closeout local gate: exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` change. All 323
  files remain format clean; Ruff and strict Pyright report zero findings; all
  894 architecture tests pass with 1 capability skip; strict docs, whitespace,
  and full Git-object checking pass.
- Final closeout-record gate retains the same 323-file/static, 894-test,
  strict-docs, whitespace, exact-scope, and Git-object result.
- Remaining: publish and integrate the exact three-record closeout, remove M80
  generated targets, return to clean `main`, and select M81.

## M79 Unicode Path extra-field preflight - closed

- Base: exact clean synchronized M78 closeout
  `5fe3134bf5a56e5cbf986ed33db698c830aa9219`, tree
  `1e1da7d8062433c2297d170643626413dfbd457f`.
- Gap: CPython honors Info-ZIP central-directory extra-field ID `0x7075` by
  substituting its valid UTF-8 path into `ZipInfo.filename` while retaining the
  decoded legacy name in `orig_filename`. The fixed sample producer emits no
  extra fields and has no need for this alternate-name representation.
- Runtime evidence: installed CPython 3.12.13, 3.13.13, and 3.14.5 each exposed
  the replacement path, retained the legacy name, and read the payload from the
  same genuine archive. Current producer output has 50 members with empty
  `ZipInfo.extra` values.
- Decision: RFC-0062 adds an exact `0x7075` check through a bounded extra-field
  walk in a separate all-member pass after M69/M75/M76/M78 policy and before
  M77 names, metadata, inventory, staging, or reads. The stable error renders
  no archive-controlled content.
- Boundary: no broad extra-field ban, general original-versus-normalized name
  comparison, raw ZIP header parser, arbitrary extra-field validator, repair,
  workflow, dependency, sample-producer, runtime-API, or release-authority
  change; this is not a general archive sandbox or real public release
  observation.
- First regression invocation was invalid baseline evidence because the new
  test required formatting and contained one unused helper. After test-only
  correction, formatting, Ruff, and strict Pyright pass; 11 compatibility,
  precedence, producer, and protected-surface guards pass while 7 policy,
  ordering, cleanup, helper/source, and docs contracts fail in 0.37 seconds
  against unchanged M78.
- Runtime checkpoint: one exact private constant/helper and one separate all-
  member pass make 17 assertions pass; only the deliberately absent RFC/public-
  document assertion fails in 0.31 seconds.
- Focused gate: both affected Python files are format/Ruff/Pyright clean; all
  18 M79 assertions pass in 0.24 seconds; strict docs build in 1.22 seconds and
  whitespace passes.
- Complete suites: the unchanged 46-package lock and restored 45-package
  graphics environment resolve; all 322 files are format clean; Ruff and
  strict Pyright report zero findings. The M64-M79 lineage passes 185
  assertions with 1 capability skip; all 874 architecture assertions pass
  with 1 skip. CPython 3.12, 3.13, and 3.14 each pass 2,404 tests with
  15/16/16 capability skips.
- Graphics/diagnostics: all 10 real-wgpu tests, both one-repeat profiles,
  Clockwork Arena, Agent World Builder, and all four M1-M4 diagnostic
  validators pass. M1 observes 1 of 2 targets, M2 has no targets, M3 meets 0
  of 2 current targets, and M4 observes its baseline target.
- Reproducible release gate: two builds reproduce a pure 274,734-byte wheel at
  `014e443b6bc0094c74521ba3211940cfc8db7c8c932212d4c1eea742a5c3f566`
  and 1,287,732-byte sdist at
  `fadce6c20313cb04ae83e71195b8fd7713e338e8c99b570473cc70635d2d226a`;
  isolated-wheel, deterministic ten-artifact staging, and complete release
  smoke pass. The unchanged sample remains 111,168 bytes at
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`.
- Findings-first review found no actionable defect. The helper honors field
  boundaries, rejects exact `0x7075`, ignores unrelated IDs and incomplete
  trailing bytes, and relies on CPython for malformed-field rejection before
  preflight. Ordering, cleanup, stable error, and protected surfaces are sound.
- Final audit: exactly 16 intended paths change. Protected CI, release
  workflow, sample producer, package metadata, and lock hashes are unchanged;
  no `src/ludoweave` file changes. Explicit development-tool identity and
  credential/private-key scans return zero matches. The 94-entry wheel and
  524-entry sdist contain no native, WASM, bytecode, or retired control
  metadata.
- History/remote: feature `HEAD`, local `main`, `origin/main`, and merge base
  are exact M78 closeout `5fe3134bf5a56e5cbf986ed33db698c830aa9219`
  with symmetric difference `0 0`. Only `origin/main` exists remotely and
  GitHub reports no open PR, tag, or release.
- Record-inclusive gate: the unchanged lock resolves 46 packages; all 322
  files are format clean; Ruff and strict Pyright report zero findings; all
  874 architecture assertions pass with 1 capability skip; strict docs,
  whitespace, and full Git-object checking pass. Two builds reproduce the pure
  274,734-byte wheel
  `014e443b6bc0094c74521ba3211940cfc8db7c8c932212d4c1eea742a5c3f566`
  and 1,288,301-byte sdist
  `d8d7182eade2052978ea7c65f0178014f6b69ced9fbcac97ae63851d26787087`;
  installed-wheel, staging, and complete release smokes pass.
- Evidence-inclusive post-record gate: all 322 files are format clean; Ruff
  and strict Pyright report zero findings; all 874 architecture assertions
  pass with 1 capability skip; strict docs, whitespace, and exact 16-path scope
  pass.
- Hosted qualification: exact DCO head
  `13b0134e2fb215701468b05edc9b278642f79a02` passed run
  `31705986777`. Linux job `94466553453` passed in 7m13s; guarded macOS job
  `94468726505` passed in 3m15s and Windows job `94468726689` in 4m10s. Linux
  CPython 3.12/3.13/3.14 and desktop CPython 3.14 each passed 2,419 tests;
  compatibility suites recorded one capability skip. Static/docs, 10 real-
  wgpu tests per OS, profiles, examples, reproducible distribution, installed-
  wheel, staging, and complete release smoke all passed.
- Hosted artifacts: the pure 274,721-byte wheel is
  `3a3785fd9da167d4ad966dd51cae0293d10cd3e9d1da870a414f750c52d42898`;
  the 1,288,417-byte sdist is
  `089908bfc7637f070cab69232294c00412155bc30f9133684d791a48a942d5b1`.
- Review state: two separated audits found no conversation comment, review,
  inline comment, or review thread. The PR remained ready, mergeable, exact-
  head, exact-base, and successful. GitHub briefly retained the completed
  Linux check as in-progress after the parent run succeeded and all Linux
  steps completed; it finalized green before merge without a rerun.
- Feature integration: PR #189 squash
  `9bc8e3813a9e25bbb977d74201fceeed3db31be2` has exact qualified tree
  `c6a4894b2d8306d814e3cd5087f21e73c9014a80`, sole M78-closeout parent,
  parseable DCO trailer, exact identity, and valid GitHub verification at
  `2026-08-13T13:57:18Z`. Its feature branch is deleted locally/remotely.
- Integration-record local gate: the first frozen-lock command was invalid
  setup evidence because the managed sandbox denied access to the existing uv
  cache before project evaluation. The identical cache-enabled run resolved
  the unchanged 46-package lock; all 322 files are format clean; Ruff and
  strict Pyright report zero findings; all 874 architecture assertions pass
  with 1 capability skip; strict docs, whitespace, exact four-path scope,
  linear history, and full Git-object checking pass.
- Integration-record release gate: two builds reproduce the pure 274,734-byte
  wheel `014e443b6bc0094c74521ba3211940cfc8db7c8c932212d4c1eea742a5c3f566`
  and 1,289,550-byte sdist
  `a6132131a6970508b55175622751d39cef99b2ac47d228cc8afe7b300f8c8583`;
  installed-wheel, deterministic ten-artifact staging, and complete release
  smokes pass.
- Post-record gate: the unchanged lock resolves 46 packages; all 322 files are
  format clean; Ruff and strict Pyright report zero findings; all 874
  architecture assertions pass with 1 capability skip; strict docs,
  whitespace, and exact four-path scope pass.
- Integration hosted gate: exact DCO head
  `31169c0b90bea95277397e86f40a33f5fcd22287`, tree
  `761c2a6007ad8f3be340a0f6796ffe5983ea06a5`, passed run
  `31708261506`. The trusted classifier identified exactly four documentation
  paths; Linux job `94474232250` passed in 47 seconds and desktop umbrella
  `94474491443` skipped with zero steps. Hosted architecture passed 875
  assertions; distribution, installed-wheel, staging, and complete release
  smokes passed.
- Integration hosted artifacts: the pure 274,721-byte wheel remains
  `3a3785fd9da167d4ad966dd51cae0293d10cd3e9d1da870a414f750c52d42898`;
  the 1,289,953-byte sdist is
  `dccb332e1e2faebe6c738a493deac55db3a1b13e7f1a1aac144e21fecf65545e`.
- Integration review: two separated audits found no comment, review, inline
  comment, or review thread. PR #190 remained ready, clean, mergeable, exact-
  head, exact-base, and successful with the expected desktop skip.
- Integration squash: `2de20b719d0c79d87187fea95b8a58f31491dad4`
  has exact reviewed tree, sole feature-squash parent, parseable DCO trailer,
  exact identity, and valid GitHub verification at
  `2026-08-13T14:07:36Z`. Its obsolete branch is deleted locally/remotely.
- Closeout local gate: exactly three project records change. The unchanged
  lock resolves 46 packages; all 322 files are format clean; Ruff and strict
  Pyright report zero findings; all 874 architecture assertions pass with 1
  capability skip; strict docs, whitespace, exact base/HEAD history, and full
  Git-object checking pass.
- Closeout post-record gate: the unchanged lock resolves 46 packages; all 322
  files are format clean; Ruff and strict Pyright report zero findings; all
  874 architecture assertions pass with 1 capability skip; strict docs,
  whitespace, and exact three-path scope pass.
- Remaining: publish the exact three-record closeout.

## M78 data-descriptor sample-member preflight - integrated and closed

- Base: exact clean synchronized M77 closeout
  `4bca618578f29629a7270ab5d9d308fd34363a06`, tree
  `a47d36363bdc48a91ef55feae8e8f3b53077907a`.
- Gap: PKWARE assigns ZIP general-purpose bit 3 to the deferred-size data-
  descriptor representation. CPython exposes and accepts the flag, while the
  fixed LudoWeave sample producer does not need or emit that representation.
- Runtime evidence: installed CPython 3.12.13, 3.13.13, and 3.14.5 each
  produced and read a genuine bit-3 descriptor-backed member from an
  unseekable output stream; the equivalent seekable producer shape emitted
  bit 3 clear.
- Decision: RFC-0061 adds exact bit-3 rejection in a separate all-member pass
  after all established M69/M75/M76 checks and before M77 names, metadata,
  inventory, staging, or reads. The stable error renders no archive-controlled
  content.
- Boundary: no raw descriptor parser, broad flag allowlist, local-header
  comparison, decoder, repair, scanner, workflow, dependency, sample-producer,
  runtime-API, or release-authority change; this is not a general archive
  sandbox or a real public release observation.
- Regression baseline: the format/Ruff/Pyright-clean 16-case M78 regression
  passed 9 compatibility, precedence, producer, and protected-surface guards
  while 7 policy, ordering, cleanup, helper/source, and documentation contracts
  failed in 0.37 seconds against unchanged M77.
- Runtime checkpoint: one exact private constant/helper and one separate all-
  member pass made 15 cases pass; only the deliberately absent RFC/public-doc
  contract failed in 0.30 seconds.
- Focused gate: after RFC-0061 and aligned public docs, both affected Python
  files are format/Ruff/Pyright clean, all 16 M78 assertions pass in 0.23
  seconds, strict docs build in 1.20 seconds with only the known upstream
  notice, and whitespace passes.
- Complete suites: the unchanged 46-package lock and restored 45-package
  graphics environment resolve; all 321 files are format clean; Ruff and
  strict Pyright report zero findings. The M64-M78 lineage passes 167
  assertions with 1 capability skip; all 856 architecture assertions pass
  with 1 skip. CPython 3.12, 3.13, and 3.14 each pass 2,386 tests with
  15/16/16 capability skips.
- Graphics/diagnostics: all 10 real-wgpu tests, both one-repeat profiles,
  Clockwork Arena, Agent World Builder, and all four M1-M4 diagnostic
  validators pass. M1 observes 1 of 2 targets, M2 has no targets, M3 meets 0
  of 2 current targets, and M4 observes its baseline target.
- Reproducible release gate: two builds reproduce a pure 274,573-byte wheel at
  `dcf1cce4641069365c6e572f5189aee237ba2b7ff7f9e3fde17cf89ecdbbab68`
  and 1,280,223-byte sdist at
  `5c9e860c7790f60af40f5155b2b2626149e688b9cd5ceed53caf65997bff7d18`;
  isolated-wheel, deterministic ten-artifact staging, and complete release
  smoke pass. The unchanged 111,168-byte sample remains
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`.
- Findings-first review removed a raw descriptor-signature absence assertion
  from the producer guard because ordinary compressed payload bytes can match
  that signature. Canonical `ZipInfo.flag_bits` evidence remains exact. The
  corrected 16 focused and 856 architecture assertions, affected static gate,
  strict docs, and whitespace pass.
- Final audit: exactly 16 intended paths change. Protected CI, release
  workflow, sample producer, package metadata, and lock hashes are unchanged;
  no `src/ludoweave` file changes. Explicit development-tool identity scans
  return zero matches. The credential scan finds only a historical literal
  negative-test URI, not secret material. The 94-entry wheel and 522-entry
  sdist contain no native, WASM, bytecode, or retired control metadata.
- History/remote: feature `HEAD`, local `main`, `origin/main`, and merge base
  are exact M77 closeout `4bca618578f29629a7270ab5d9d308fd34363a06`
  with symmetric difference `0 0`. Only `origin/main` exists remotely and
  GitHub reports no open PR, tag, or release.
- Record-inclusive gate: the unchanged lock resolves 46 packages; all 321
  files are format clean; Ruff and strict Pyright report zero findings; all
  856 architecture assertions pass with 1 capability skip; strict docs and
  whitespace pass. Two builds reproduce the pure 274,573-byte wheel
  `dcf1cce4641069365c6e572f5189aee237ba2b7ff7f9e3fde17cf89ecdbbab68`
  and 1,281,118-byte sdist
  `2bbdb0167965d332b2d0f1e7b33065cc63915b92fdfdbd2fbd3a712cf30b015f`;
  isolated-wheel, staging, and complete release smokes pass.
- Evidence-inclusive post-record gate: the unchanged lock, all 321 formatted
  files, Ruff, strict Pyright, all 856 architecture assertions with 1
  capability skip, strict docs, whitespace, and exact 16-path scope pass.
- Hosted qualification: exact DCO head
  `e897a2277b6c150ec77b88022e2f52a165ea978a` passed run
  `31701501926`. Linux completed in 7m26s; guarded macOS and Windows passed in
  3m07s and 3m52s. Each hosted suite passed 2,401 tests; compatibility suites
  recorded one capability skip. Static/docs, 10 real-wgpu tests per OS,
  profiles, examples, reproducible distribution, installed-wheel, staging,
  and complete release smoke all passed.
- Hosted artifacts: the pure 274,559-byte wheel is
  `ccbe8d92ed51ac31c4fc0e0ca1e52fbf697d20e4b7dc9250a15ad718944a8b5b`;
  the 1,281,259-byte sdist is
  `13e5518654d192a646a08586b382967050c73a20fc36e51244148e7cb8a54309`.
- Review state: two separated audits found no conversation comment, review,
  inline comment, or review thread. The PR remained ready, `CLEAN`,
  `MERGEABLE`, exact-head, exact-base, and successful.
- Feature integration: PR #186 squash
  `180d93dbe6984fff43af07021efd000150b76132` has exact qualified tree
  `820e1a861fe4e84154515629ba43e98cc8024df3`, sole M77-closeout parent,
  parseable DCO trailer, exact identity, and valid GitHub verification at
  `2026-08-13T12:58:28Z`. Its feature branch is deleted locally/remotely.
- Integration-record local gate: exactly four record paths change. The
  unchanged lock resolves 46 packages; all 321 files are format clean; Ruff
  and strict Pyright report zero findings; all 856 architecture assertions
  pass with 1 capability skip; strict docs, whitespace, and full Git-object
  checks pass. Two builds reproduce the pure 274,573-byte wheel
  `dcf1cce4641069365c6e572f5189aee237ba2b7ff7f9e3fde17cf89ecdbbab68`
  and 1,282,286-byte sdist
  `daf0cf1f4f3d131be1a10095afc2bb1a32f349b13153b60ba23e986d45f95bae`;
  wheel, staging, and complete release smokes pass.
- Post-record gate: the unchanged lock, all 321 formatted files, Ruff, strict
  Pyright, all 856 architecture assertions with 1 capability skip, strict
  docs, whitespace, and exact four-path scope pass.
- Integration hosted gate: exact DCO head
  `a542979555916edc1fb585bbe64eb9116c8beb85`, tree
  `c807cd3f72edc81c37597ec3744661bafd41d36f`, passed run
  `31703080076`. The trusted classifier identified exactly four documentation
  paths; Linux passed in 44 seconds and the desktop umbrella skipped with zero
  steps. Hosted architecture passed 857 assertions; distribution, installed-
  wheel, staging, and complete release smokes passed.
- Integration hosted artifacts: the pure 274,559-byte wheel remains
  `ccbe8d92ed51ac31c4fc0e0ca1e52fbf697d20e4b7dc9250a15ad718944a8b5b`;
  the 1,282,392-byte sdist is
  `c3f58daeb5d7a4c307149b22358402abab390b738f33011453c335347a880e93`.
- Integration review: two separated audits found no comment, review, inline
  comment, or review thread. PR #187 remained ready, clean, mergeable, exact-
  head, exact-base, and successful.
- Integration squash: `905d40a8091dd6b4e5cf8e4e72d8c7873b7aadb9`
  has exact reviewed tree, sole feature-squash parent, parseable DCO trailer,
  exact identity, and valid GitHub verification at
  `2026-08-13T13:06:46Z`. Its obsolete branch is deleted locally/remotely.
- Closeout local gate: exactly three project records change. The unchanged
  lock resolves 46 packages; all 321 files are format clean; Ruff and strict
  Pyright report zero findings; all 856 architecture assertions pass with 1
  capability skip; strict docs, whitespace, and full Git-object checking pass.
- Closeout post-record gate: all 321 files are format clean; Ruff and strict
  Pyright report zero findings; all 856 architecture assertions pass with 1
  capability skip; strict docs, whitespace, and exact three-path scope pass.
- Remaining: publish the exact three-record closeout.

## M77 NUL-suffixed sample-member name preflight - integrated and closed

- Base: exact clean synchronized M76 closeout
  `701637f99447f4d64c84047e64ec5edfa0c6889f`, tree
  `27cfc273accb3190d0c50e6a344685875cce541b`.
- Gap: CPython preserves the decoded central-directory filename used to
  construct `ZipInfo` in `orig_filename`, then truncates `filename` at the
  first NUL. The verifier currently validates only the truncated visible name,
  allowing an exact-inventory path to carry an unvalidated hidden suffix.
- Runtime evidence: installed CPython 3.12.13, 3.13.13, and 3.14.5 each expose
  `root/README.md\0hidden` as the original name, expose `root/README.md` as the
  normalized name, and read the payload successfully.
- Decision: RFC-0060 adds one exact NUL check on `orig_filename` to the existing
  all-member preflight after flag policy and before metadata, inventory,
  staging, or reads. The stable error renders no archive-controlled content.
- Boundary: no general normalized-name comparison, raw parser, header
  consistency claim, rewriting, repair, scanner, workflow, dependency,
  producer, runtime API, or release authority. Existing flag errors retain
  precedence.
- Regression baseline: on exact M76, the format/Ruff/Pyright-clean 12-case
  regression passes 6 standard-library/precedence/producer/protected guards
  and fails 6 early-policy/ordering/cleanup/helper/source/docs contracts in
  0.91 seconds.
- Runtime checkpoint: one exact private helper checks the decoded original name
  after established flag validation. The corrected M69/M75/M76/M77 group
  passed 40 assertions; only the deliberately absent RFC/docs assertion
  failed. A prior checkpoint named a nonexistent inherited test and collected
  nothing; it is invalid setup evidence.
- Focused/inherited gate: after RFC-0060 and aligned records, all 12 M77
  assertions pass in 0.89 seconds. The exact M64-M77 extraction lineage passes
  148 assertions with 1 local capability skip in 1.68 seconds. Affected
  format/Ruff/Pyright, strict docs, and whitespace pass.
- Complete suites: the unchanged lock resolves 46 packages and the restored
  graphics environment contains 45 packages. All 320 files are format clean;
  Ruff and strict Pyright report zero findings. CPython 3.12, 3.13, and 3.14
  each pass 2,367 tests with 15 skips; all 837 architecture assertions pass
  with 1 local capability skip.
- Graphics/diagnostics: all 10 real-wgpu tests, both five-repeat profiles,
  Clockwork Arena, Agent World Builder, and all four M1-M4 diagnostic
  validators pass. M1 observes 1 of 2 targets, M2 has no targets, M3 meets 0 of
  2 current targets, and M4 observes its baseline target.
- Pre-review artifacts: two builds reproduce a pure 274,448-byte wheel at
  `ecf37cf1a420433cdc0b5a3ff07fefff5450e5d7ae0b6cdff1e2d3e88639dea9`
  and 1,272,210-byte sdist at
  `932b43823605e870598b08f0b54c98fd1bc491a38769e2440ea1aec8ab094892`;
  wheel, staging, and complete release smokes pass. The unchanged 111,168-byte
  50-entry sample is
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`.
- Local review corrected public wording that treated `orig_filename` as a
  universal name record; it is specifically the decoded central-directory
  filename used to construct `ZipInfo`. The first hosted review then found an
  archive-wide precedence gap: an earlier NUL name could mask a prohibited
  flag on a later member. The correction completes all-member flag validation
  before a separate all-member name pass. Three cross-member regressions cover
  M69, M75, and M76; all 15 focused cases and affected static/docs gates pass.
- Record-inclusive artifacts: two builds reproduce the pure 274,448-byte wheel
  `ecf37cf1a420433cdc0b5a3ff07fefff5450e5d7ae0b6cdff1e2d3e88639dea9`
  and 1,273,541-byte sdist
  `11f7a22829654db4dd855bf771bfd8d8cf391136872b7152d1ff5a817ddd765f`;
  installed-wheel, deterministic staging, and complete release smokes pass.
- Final audit: the candidate is exactly 16 intended paths. Protected CI,
  release workflow, sample producer, package metadata, and lock hashes are
  unchanged. Explicit development-tool identity and credential/private-key
  scans return zero matches; inspected archives contain no native, WASM,
  bytecode, or retired control metadata. Static, architecture, strict docs,
  whitespace, and full Git-object checking pass.
- History/remote: feature `HEAD`, local `main`, `origin/main`, and merge base
  are exact M76 closeout `701637f99447f4d64c84047e64ec5edfa0c6889f`
  with symmetric difference `0 0`. Only `origin/main` exists remotely and
  GitHub reports no open PR, tag, or release.
- Post-record gate: the unchanged lock, all 320 formatted files, Ruff, strict
  Pyright, all 837 architecture assertions with 1 local capability skip,
  strict docs, whitespace, and exact 16-path scope pass.
- First hosted head: exact DCO head
  `bd338004fc44d441b7190223645a8ad9802b7819` passed run `31695444362` on
  Linux, macOS, and Windows before the precedence finding. The corrected head
  still requires full local and hosted qualification.
- Corrected local qualification: all 15 focused assertions and all 840
  architecture assertions pass with 1 local capability skip. CPython 3.12
  passes 2,380 tests with 15 skips; CPython 3.13/3.14 each pass 2,370 with 16
  skips. Real-wgpu, profiles, examples, reproducible distribution, isolated
  wheel, deterministic staging, and complete release smoke all pass.
- Corrected hosted qualification: exact DCO head
  `482aa76c68c1ab3d17f22f4fa1d286c7ab03ed9a` passed run `31697316773`.
  Linux completed first in 7m33s; guarded macOS and Windows passed in 3m07s
  and 3m57s. Each of the five hosted suites passed 2,385 tests; all but Linux
  3.12 recorded one capability skip. All static/docs, real-wgpu, profile,
  example, distribution, installed-wheel, staging, and release checks passed.
- Review state: two separated post-correction audits found no new review input.
  The original P2 thread remains unresolved because no resolution write was
  authorized, but exact corrected head contains its requested separate
  archive-wide passes and all three cross-member regressions. GitHub reported
  the PR clean and mergeable before squash.
- Feature integration: PR #183 squash
  `0c3c407c1e5d86541570c665fd305fa95e32e07a` has exact reviewed tree
  `923efabb7b6968a53db2035c107baa80b89119cc`, sole parent M76 closeout,
  exact author identity, and valid GitHub verification at
  `2026-08-13T12:04:14Z`. Both source commits have parseable DCO trailers.
- Process note: the squash body contains literal `\n\n` characters before its
  sign-off text, not real blank lines, so the squash message itself has no
  parseable DCO trailer. This is retained as factual process evidence; future
  squash messages use a body file. No history rewrite is authorized or made.
- Integration record: exact DCO head
  `ed1eb024cc4098d03a02c06c5c5dda6e3df8792a` passed documentation-classified
  run `31698788838`. One 47-second Linux job passed 841 hosted architecture
  assertions, reproducible distribution, installed-wheel smoke, deterministic
  staging, and complete release smoke; desktop skipped with zero steps.
- Integration audits/squash: two separated audits found no review input. PR
  #184 squash `9c37857cb8d0cc68fa63128091d6c116f84ef66d` has exact reviewed tree
  `baffa85b731086ba71a247411cfbca51c4bdbc72`, sole feature-squash parent,
  exact identity, a parseable DCO trailer, and valid GitHub verification at
  `2026-08-13T12:13:08Z`.
- Remaining: exact three-record closeout, branch/artifact cleanup, and
  selection of M78 from clean synchronized `main`.

## M76 enhanced-deflate sample-member preflight - complete

- Base: exact clean synchronized M75 closeout
  `ddf262dff7a8c93defad5a205adbaec460563439`, tree
  `c124cb2573a4329c8032d1d4eeb416e2e1556d24`.
- Gap: PKWARE reserves ZIP general-purpose bit 4 for enhanced deflating with
  compression method 8. Supported CPython does not inspect that indicator and
  reads otherwise normal deflate bytes carrying it.
- Decision: RFC-0059 adds exact flag `0x0010` and one separate method-scoped
  validator to the all-member preflight. The stable content-silent error occurs
  before metadata, inventory, staging, or reads. Existing encryption and
  compressed-patch errors retain precedence.
- Boundary: bit 4 on stored members remains out of scope. No broad flag
  allowlist, enhanced-deflate decoder, repair, raw parser, scanner, workflow,
  dependency, producer, runtime API, or release authority is added. The check
  consumes central-directory flags exposed by `ZipInfo`; local-header
  inconsistencies remain outside scope.
- Baseline: after one invalid missing-parent basetemp launch, exact unchanged
  M75 passed 3 standard-library/precedence/protected guards and failed 7 M76
  contract assertions in 0.41 seconds. The constant, validator, early policy,
  producer/source contract, and RFC/docs were absent.
- Implementation checkpoint: the M69/M75/M76 group passed 28 behavioral,
  source, and protected assertions; only the deliberately absent RFC/docs
  assertion failed. Lint and strict Pyright were clean; Ruff requested and
  applied one mechanical verifier formatting change.
- Focused gate: all 10 M76 assertions pass in 0.25 seconds; exact M64-M76 passes
  136 assertions with 1 local filesystem-capability skip in 1.66 seconds.
  Affected formatting, Ruff, and strict Pyright are clean; strict docs build in
  1.26 seconds with only the known upstream notice; whitespace passes.
- Complete suite: after removing workspace-local generated pytest basetemps,
  the unchanged 46-package lock, 45-package graphics environment, all 319
  formatted files, Ruff, and strict Pyright pass. CPython 3.12 passes 2,355
  tests with 15 skips; CPython 3.13 and 3.14 each pass 2,355 with 16 skips; all
  825 architecture assertions pass with 1 local capability skip.
- Graphics/diagnostics: all 10 real-wgpu tests, both five-repeat profiles,
  Clockwork Arena, Agent World Builder, and all four M1-M4 diagnostic
  validators pass. M1/M3 each observe one of two targets, M2 has no targets,
  and M4 observes its baseline target.
- Pre-review artifacts: two builds reproduce a pure 274,258-byte wheel at
  `7ced651e7231f4308c9b092c2f4a6b6447fff7277095bd1b2f252167f0d4dff1`
  and a 1,262,791-byte sdist at
  `dfb4ee65626ac2c4d7f00137421cda4b71397feec2507bd78f6407a25a22c729`;
  wheel, staging, and complete release smoke pass. The unchanged sample is
  111,168 bytes/50 entries at
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  no inspected archive entry is native, WASM, bytecode, or retired metadata.
- Review: the runtime/test design is sound. Review corrected one documentation
  overclaim by stating that the policy observes central-directory flags exposed
  by `ZipInfo`; local-header inconsistencies remain outside scope because M76
  adds no raw parser. Corrected focused/architecture/static/docs/whitespace
  gates pass.
- Record-inclusive artifacts: two builds reproduce a 274,273-byte wheel at
  `373dbe9ad78c4c2ba6ff96e7533a84cc812057f2a985aea06c491706112fe40f`
  and a 1,264,049-byte sdist at
  `d11c63366f4e44405f8b4b02442ef6cca9db952c3068ac82202017fc1191e96a`;
  wheel, staging, and complete release smokes pass. Exact commit artifact
  identity remains delegated to hosted qualification because recording this
  result changes the sdist.
- Final audit: the candidate is exactly 16 intended paths. Protected CI,
  release workflow, sample producer, metadata, and lock hashes are unchanged;
  archive/content boundaries, credential/private-key hygiene, explicit
  development-tool identity hygiene, and retired repository-control metadata
  absence pass. Feature `HEAD`, `main`, `origin/main`, and merge base are exact
  M75 closeout with symmetric difference `0 0`; history is linear. Only
  `origin/main` exists remotely, and GitHub reports no open PR, tag, or release.
- Hosted feature qualification: PR #180 exact head
  `2f93c32926dfb2aec4798fa5f4c13a2b096495c9` passed run `31638620625` in
  three bounded allocations. Linux CPython 3.12 passed 2,370 tests; Linux
  3.13/3.14, macOS 3.14, and Windows 3.14 each passed 2,370 with 1 expected
  capability skip. Static, docs, real-wgpu, profiles, examples, installed
  wheel, staging, and complete release smokes passed.
- Hosted artifacts: the pure 274,260-byte wheel is
  `74d28148c78151f56d366db8b64212e91ae409f722931dd0a1bc6a67150482ba`;
  the 1,265,082-byte sdist is
  `75db0570cdb93a3e7c317237712c7c717b275e8ae6417186b4119523ecb294238`.
  Ten staged artifacts passed deterministic and release validation.
- Review/integration: two separated audits found no issue comment, review,
  inline comment, or unresolved thread. PR #180 remained clean, mergeable, and
  exact. Its verified DCO squash
  `425ed21ab99d91bf4661b304bea00137117a5d27` has the exact qualified tree
  `8b7f50a2efba456f1015276f1b6345466d9fa5cb` and sole parent M75 closeout.
- Integration-record local gate: exactly the four neutral project/roadmap
  records change. The unchanged lock resolves 46 packages; all 319 Python
  files are format clean; Ruff and strict Pyright report zero findings; all
  825 architecture assertions pass with 1 capability skip; strict docs,
  whitespace, and Git-object checking pass. Two fresh builds reproduce the
  pure 274,273-byte wheel
  `373dbe9ad78c4c2ba6ff96e7533a84cc812057f2a985aea06c491706112fe40f`
  and 1,265,304-byte sdist
  `1d55265954454f788d2a48adb6d5d7c8077272820f85b6185a7b5a4bbc094f0e`;
  isolated-wheel, deterministic staging, and complete release smokes pass.
- Hosted integration record: PR #181 exact head
  `3ea7f503c9f8ce4e315bf6e119f23242c0e00c22` passed run `31640417965`.
  Exactly four paths classified as documentation; one 42-second Linux job
  passed and the desktop umbrella skipped with zero steps. All 319 files were
  format clean; Ruff and strict docs passed; all 826 hosted architecture
  assertions passed; reproducible distributions, installed-wheel smoke,
  deterministic staging, and complete release smoke passed.
- Hosted integration artifacts: the pure 274,260-byte wheel is
  `74d28148c78151f56d366db8b64212e91ae409f722931dd0a1bc6a67150482ba`;
  the 1,266,053-byte sdist is
  `5a7352408529da88ffe29d8f0e1bec752c5e8a2359fe0b0088c5c4482b7af31d`.
- Integration review/squash: two separated audits found no issue comment,
  review, inline comment, or unresolved thread. PR #181 remained clean,
  mergeable, and exact. Its GitHub-verified DCO squash
  `224b595f185fdd16fb5ab733e60f78a61ab19f5a` has exact reviewed tree
  `f626382619a628a961bbf34dbb146c1bdea6099f` and sole parent M76 feature
  squash `425ed21ab99d91bf4661b304bea00137117a5d27`.
- Closeout local gate: exactly three neutral project records change. The
  unchanged lock resolves 46 packages; all 319 files are format clean; Ruff and
  strict Pyright report zero findings; all 825 architecture assertions pass
  with 1 local capability skip; strict docs, whitespace, and full Git-object
  checking pass.
- Closeout integration: path-filtered PR #182 started no workflow. Two
  separated audits were clean. Its verified DCO squash
  `701637f99447f4d64c84047e64ec5edfa0c6889f` has exact reviewed tree
  `27cfc273accb3190d0c50e6a344685875cce541b` and sole parent the M76
  integration-record squash.
- Cleanup: 32 verified workspace-local M76 validation targets were removed.
  Only synchronized `main` remains locally/remotely with symmetric difference
  `0 0`; no PR, tag, or release remains open or published.
- Post-record correction: M59 caught three project-record references that
  literally named a retired control directory. They were neutralized, after
  which all 825 architecture assertions pass with 1 capability skip; static,
  strict docs, whitespace, and exact 16-path scope also pass.

## M75 compressed-patch sample-member preflight - complete

- Base: exact clean synchronized M74 closeout
  `674d74c8fc852846404813ab541aab3deffd8608`, tree
  `cbe1b75ae6c3174c04b0712894244918cae69010`.
- Gap: ZIP general-purpose bit 5 declares compressed patched data. Supported
  CPython versions reject it only from `ZipFile.open`, after the existing
  all-member flag preflight and after inventory/staging work can begin.
- Decision: RFC-0058 adds exact flag `0x0020` to M69's all-member preflight,
  after encryption so that established category retains precedence. The new
  stable content-silent policy error occurs before metadata, inventory,
  staging, or reads.
- Boundary: no broad flag allowlist, reserved-bit policy, implementation-error
  catch, patch decoder, repair, raw parser, scanner, workflow, dependency,
  producer, runtime API, or release authority.
- Research: PKWARE APPNOTE 6.3.9 assigns bit 5 to compressed patched data;
  exact installed CPython 3.12.13, 3.13.13, and 3.14.5 all reject it at member
  open with the same `NotImplementedError`.
- Baseline: exact M74 passed 3 standard-library/protected/out-of-scope guards
  and failed 7 M75 contract assertions in 0.34 seconds. The actual exact-
  inventory archive progressed beyond flag preflight; the constant, early
  policy branch, producer assertion, source contract, and docs were absent.
- Implementation checkpoint: one exact constant and ordered policy branch are
  implemented. Affected formatting, Ruff, and strict Pyright pass. All 9 M75
  behavioral/source/protected assertions and all 9 M69 compatibility
  assertions pass; only the deliberately absent RFC/docs assertion failed.
- Focused gate: after correcting one exact documentation phrase, all 10 M75
  assertions pass in 0.21 seconds; inherited M64-M75 passes 126 assertions with
  1 local filesystem-capability skip in 1.18 seconds. Affected formatting,
  Ruff, and strict Pyright are clean; strict docs and whitespace pass.
- Complete local candidate: the unchanged lock resolves 46 packages and the
  restored graphics environment contains 45 packages. All 318 files are
  format clean; Ruff and strict Pyright report zero findings. CPython 3.12,
  3.13, and 3.14 each pass 2,345 tests with 15 skips; all 815 architecture
  assertions pass with 1 local capability skip.
- Graphics/diagnostics: all 10 real-wgpu tests, both five-repeat profiles,
  Clockwork Arena, Agent World Builder, and all four M1-M4 diagnostic
  validators pass. M1/M3 each observe one of two targets, M2 has no targets,
  and M4 observes its baseline target.
- Pre-review artifacts: two builds reproduce a pure 274,103-byte wheel at
  `60824005e82908164ad7a6433d3647cdf011d9aa03dec884aa8d142904084784`
  and a 1,256,257-byte sdist at
  `9d33bf47e294d63a5dc6bce66d60781562676e5881158d414d849b23d785df49`;
  wheel, staging, and complete release smoke pass. The unchanged sample is
  111,168 bytes/50 entries at
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  no inspected wheel or sample entry is native or WASM.
- Review: no product, test, RFC, or scope defect remains. Exact bit mutation,
  all-member ordering, cleanup, encryption precedence, unrelated-flag non-
  expansion, producer compatibility, protected surfaces, and documentation
  non-claims are covered.
- Record-inclusive qualification: the unchanged lock and 45-package graphics
  environment, all 318 formatted files, Ruff, strict Pyright, 815 architecture
  assertions with 1 local capability skip, strict docs, whitespace, and full
  Git-object checking pass. Two builds reproduce the pure 274,103-byte wheel at
  `60824005e82908164ad7a6433d3647cdf011d9aa03dec884aa8d142904084784`
  and a 1,257,198-byte record-updated sdist at
  `ece63f8b3f70b3aa9600e4a64543b5a0143ba0f3c794e119d29461560936600d`;
  wheel, staging, and complete release smoke pass. Exact commit artifact
  identity remains delegated to hosted qualification because recording this
  result changes the sdist.
- Final frozen gate: the unchanged lock resolves 46 packages; all 318 files are
  format clean; Ruff and strict Pyright are clean; all 815 architecture
  assertions pass with 1 local capability skip; strict docs, whitespace, and
  Git-object checking pass. Exact 16-path scope, protected hashes, credential/
  private-key hygiene, and explicit development-tool identity hygiene pass.
- Prepublication audit: feature `HEAD`, local `main`, `origin/main`, and merge
  base are exact M74 closeout `674d74c8fc852846404813ab541aab3deffd8608`
  with symmetric difference `0 0`; history is linear. Only remote `main`
  exists; GitHub reports no open PR, tag, or release.
- Exact post-record freeze: all 318 files are format clean; Ruff and strict
  Pyright are clean; all 815 architecture assertions pass with 1 local
  capability skip; strict docs, whitespace, and exact 16-path scope pass.
- Hosted qualification: exact DCO head
  `77ab1757ea52be4c5532adfe26c27bfa202504ef`, tree
  `b0aac18c83fc6e93bd5fd1e1f154100e2bc75799`, passed run
  `31633932748` in exactly three Linux-first allocations: Linux 7m21s, macOS
  3m25s, and Windows 4m06s. Every hosted suite, graphics/profile/example, and
  distribution/release smoke passed.
- Hosted artifacts: pure 274,089-byte wheel
  `af0ea15e0ac4851461a93d79b11b587d2d230fc91219c2da47acee5574901d4b`
  and 1,257,945-byte sdist
  `7f68ef379d335c9a4b3cefb7e9409af26fb759f8ebffc28dc7a7bb11e8d43917`.
- Hosted review/integration: two audits found no review activity. GitHub-
  verified squash `b86013397d5ad5f28d9a9adfe7c7f30996cbad65` has the exact
  reviewed tree, sole M74-closeout parent, exact DCO, and a valid signature
  verified at `2026-08-12T19:55:01Z`. The feature branch is deleted.
- Integration local qualification: the unchanged lock resolves 46 packages;
  all 318 files are format clean; Ruff and strict Pyright are clean; all 815
  architecture assertions pass with 1 local capability skip; strict docs,
  whitespace, and Git-object checking pass. Two builds reproduce the feature-
  identical 274,103-byte wheel
  `60824005e82908164ad7a6433d3647cdf011d9aa03dec884aa8d142904084784`
  and 1,259,225-byte record-updated sdist
  `5f5051d0e2831634eb2b2bb596258a2782fa83fd5063cac3854df4e296e1d2a7`;
  wheel, staging, and release smoke pass.
- Hosted integration: exact DCO head
  `26640c723b48a208301c86dacc5f53772bc745fe` passed run `31635295952`
  in one 38-second Linux allocation; desktop skipped with zero steps. It passed
  816 selected architecture assertions, strict docs, reproducible artifacts,
  and all smokes. Hosted wheel `af0ea15e...` was feature-identical; sdist was
  `bf99be5f80bf644173b309efb8c75950c5de718efaff8acdcea71e34361c3a1c`.
- Integration merge: two audits were clean. GitHub-verified squash
  `57dc9af600a5e651bc051fb5a47b2902cb2e2403` has the exact reviewed tree,
  sole feature-squash parent, exact DCO, and valid signature verified at
  `2026-08-12T20:00:32Z`. Only the closeout record remains.
- Closeout qualification: all 318 files are format clean; Ruff and strict
  Pyright are clean; all 815 architecture assertions pass with 1 local
  capability skip; strict docs, whitespace, and Git-object checking pass. The
  diff is exactly the three neutral project records.
- Intended scope: exactly 16 paths, with no workflow, producer, runtime-package,
  dependency, metadata, lock, benchmark, version, or release-authority change.

## M74 content-silent sample ZIP decompression failures - complete

- Base: exact clean synchronized M73 closeout
  `7ecb584e71a375d1ab63ee8134e7493e418dedff`, tree
  `fafa86abb05929711e38f34b4d219bcfc7161637`.
- Gap: checksum and exact-inventory admission do not validate raw-deflate
  payload syntax. The standard ZIP member reader can raise `zlib.error` during
  bounded extraction, bypassing M72/M73's stable content-silent boundary.
- Decision: RFC-0057 adds exactly `zlib.error` to the private outer catch,
  reuses the stable ZIP-data error after owned cleanup, suppresses its rendered
  context, and retains the original exception programmatically.
- Boundary: no EOF/filesystem/broad compression/general catch, replacement
  decompressor, payload repair, raw parser, scanner, workflow, dependency,
  producer, runtime API, or release authority.
- Research: official Python documentation defines `zlib.error` for compression
  and decompression failures. Exact installed CPython 3.12.13 and 3.13.13 with
  zlib 1.3.1 and CPython 3.14.5 with zlib-ng 1.3.1 directly decompress
  deflated ZIP member bytes without recategorizing that exception.
- Baseline: exact M73 produced 4 failures and 4 passing policy/producer/
  protected guards in 0.38 seconds. Both actual checksum-admitted invalid-
  deflate paths escaped raw; the catch contract and RFC/docs were absent.
- Implementation checkpoint: the two-line runtime change imports stdlib
  `zlib` and catches exactly `zlib.error`. The first M73/M74 run exposed M73's
  historical whole-tuple assertion; narrowing that inherited guard to its
  required exception members left only the deliberately absent M74 RFC/docs
  assertion failing. The corrected group passes 15 assertions in 0.43 seconds;
  affected formatting, Ruff, and strict Pyright are clean.
- Focused gate: all 8 M74 assertions pass in 0.22 seconds; inherited M64-M74
  passes 116 assertions with 1 local filesystem-capability skip in 1.02
  seconds. Affected formatting, Ruff, and strict Pyright are clean; strict docs
  and whitespace pass.
- Complete local candidate: the unchanged lock resolves 46 packages and the
  locked graphics environment contains 45 packages. All 317 files are format
  clean; Ruff and strict Pyright report zero findings. CPython 3.12 passes
  2,335 tests with 15 skips; CPython 3.13/3.14 each pass 2,335 with 16 skips;
  all 805 architecture assertions pass with 1 local capability skip.
- Graphics/diagnostics: all 10 real-wgpu tests, both five-repeat profiles,
  Clockwork Arena, Agent World Builder, and all four M1-M4 diagnostic
  validators pass. M1 observes one of two engineering targets, M2 has no
  targets, M3 observes one of two graphics targets, and M4 observes its
  baseline target.
- Pre-review artifacts: two builds reproduce a pure 273,952-byte wheel at
  `ada989ae548bdf51f124d39080a83580711e58e5148b149b28a72dbaf59c8bcf`
  and a 1,247,726-byte sdist at
  `f06f525fda77ddd9d618ac92a4c7bbfb2f33cc4c29d6358c1310106a71951988`;
  wheel, staging, and complete release smoke pass. The unchanged 111,168-byte
  50-entry sample remains at
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  no inspected archive contains native/WASM entries.
- Scope: exactly 17 intended paths including the two new RFC/test paths.
  Protected CI/release workflow, producer, package metadata, and lock hashes
  remain exact; no runtime package, dependency, benchmark, version, workflow,
  or release-authority change.
- Review: no product, test, RFC, or scope defect remains. The real invalid-
  block fixture retains valid ZIP metadata, exact inventory, and matching
  checksum; cleanup and rendered-context checks cover the staged failure; EOF
  and policy categories remain distinct. M73's inherited source guard now
  preserves its exact required members while permitting later narrow
  additions and still excludes broad catches. The M72-M74 group, whole-tree
  static checks, strict docs, and whitespace pass.
- Record-inclusive qualification: the unchanged lock and 45-package graphics
  environment, all 317 formatted files, Ruff, strict Pyright, 805 architecture
  assertions with 1 local capability skip, strict docs, whitespace, and full
  Git-object checking pass. Two builds reproduce the pure 273,952-byte wheel at
  `ada989ae548bdf51f124d39080a83580711e58e5148b149b28a72dbaf59c8bcf`
  and a 1,249,215-byte record-updated sdist at
  `ab78ce123bb24d9bee5e70871f13238745e31ded5da826e0a2969b2db03212a5`;
  wheel, staging, and complete release smoke pass. Exact commit artifact
  identity remains delegated to hosted qualification because recording this
  result changes the sdist.
- Final frozen gate: the unchanged lock resolves 46 packages; all 317 files are
  format clean; Ruff and strict Pyright are clean; all 805 architecture
  assertions pass with 1 local capability skip; strict docs, whitespace, and
  full Git-object checking pass.
- Prepublication audit: feature `HEAD`, local `main`, and `origin/main` are
  exact M73 closeout `7ecb584e71a375d1ab63ee8134e7493e418dedff` with
  symmetric difference `0 0`; history is linear and the candidate remains
  exactly 17 paths. GitHub reports only remote `main`, no open PR, no tag, and
  no release. Protected hashes, credential/private-key hygiene, and explicit
  development-tool identity hygiene pass.
- Exact post-record freeze: all 317 files are format clean; Ruff and strict
  Pyright are clean; all 805 architecture assertions pass with 1 local
  capability skip; strict docs, whitespace, and exact 17-path scope pass.
- Hosted qualification: exact DCO head
  `49f38b841d497c4bc84666d64674185290adb836`, tree
  `5bf17270a8bf9f84314bff38c93c7aeb0502b347`, passed run
  `31629156916` in exactly three Linux-first allocations. Linux passed in
  7m19s; macOS passed in 2m50s and Windows in 4m17s after Linux completed.
- Hosted suites: all 317 files were format clean; Ruff, strict Pyright, strict
  docs, every supported Python gate, real graphics, both profiles, both
  vertical slices, reproducible builds, installed-wheel smoke, staging, and
  complete release smoke passed. Each hosted Python suite passed 2,350 tests;
  all but Linux 3.12 had 1 expected skip.
- Hosted artifacts: two exact-head builds reproduced a pure 273,938-byte wheel
  at `711a4379ef59c4c2cd2bf1b3d11ce6a84de805d2d7c7ab97f5c4bab4ee841238`
  and a 1,249,974-byte sdist at
  `6b7e7c90247251c0922eb895a3ded86b1ca785587f4e5505a6425380c0e507b6`.
- Hosted review: two separated audits found no issue comment, review, inline
  comment, or review thread. PR #174 remained ready, clean, mergeable, and at
  the exact qualified head.
- Feature integration: GitHub-verified squash
  `88960cccf31458a0d654062876b46eea616374dc` has the exact reviewed tree,
  sole parent M73 closeout `7ecb584e71a375d1ab63ee8134e7493e418dedff`,
  exact DCO, and a valid signature verified at `2026-08-12T18:59:26Z`. The
  feature branch is deleted locally and remotely. The current four-file
  integration record changes no substantive M74 surface.
- Integration local qualification: the unchanged lock resolves 46 packages;
  all 317 files are format clean; Ruff and strict Pyright are clean; all 805
  architecture assertions pass with 1 local capability skip; strict docs,
  whitespace, and Git-object checking pass. Two builds reproduce the feature-
  identical pure 273,952-byte wheel at
  `ada989ae548bdf51f124d39080a83580711e58e5148b149b28a72dbaf59c8bcf`
  and a 1,251,607-byte record-updated sdist at
  `53a335c20066cc5b7f004ebb66f41ec14aecefec45dbcbecd898ffc7f110ccfa`;
  wheel, staging, and complete release smoke pass. Exact integration-commit
  artifact identity remains delegated to hosted qualification because this
  record changes the sdist.
- Integration record freeze: all 317 files remain format clean; Ruff and
  strict Pyright are clean; all 805 architecture assertions pass with 1 local
  capability skip; strict docs, whitespace, and Git-object checking pass. The
  diff remains exactly four record/roadmap files with clean credential/private-
  key and explicit development-tool identity scans.
- Hosted integration qualification: exact DCO head
  `fd3185ab0213ffdecb2225877145ebf865199513`, tree
  `f3cc51c38ce0c3682449225e84426b722e04724d`, passed run
  `31630962285` in one 38-second Linux allocation; the desktop umbrella
  skipped with zero steps. The gate resolved 46 packages, found all 317 files
  format clean, passed Ruff and strict docs, passed 806 documentation-selected
  architecture assertions, reproduced artifacts, and passed installed-wheel,
  staging, and complete release smokes.
- Hosted integration artifacts: two exact-head builds reproduced the feature-
  identical pure 273,938-byte wheel at
  `711a4379ef59c4c2cd2bf1b3d11ce6a84de805d2d7c7ab97f5c4bab4ee841238`
  and a 1,252,100-byte sdist at
  `4b974e44eed847474d621ebfc4065b9011b177986374287de7dbe50f6076e5e8`.
- Integration review: two separated audits found no issue comment, review,
  inline comment, or review thread. PR #175 remained clean, mergeable, and on
  its exact qualified head.
- Integration squash: GitHub-verified commit
  `01d79609c81f13ea637addd9c41bd019d0bdebb0` has the exact reviewed tree,
  sole parent M74 feature squash `88960cccf31458a0d654062876b46eea616374dc`,
  exact DCO, and a valid signature verified at `2026-08-12T19:07:49Z`. The
  integration branch is deleted locally and remotely. M74 is substantively
  complete; only its exact three-record closeout remains.
- Closeout qualification: the unchanged lock resolves 46 packages; all 317
  files are format clean; Ruff and strict Pyright are clean; all 805
  architecture assertions pass with 1 local capability skip; strict docs,
  whitespace, and Git-object checking pass. The diff is exactly the three
  neutral project records, with no workflow, substantive, public-documentation,
  or roadmap change and clean credential/private-key and explicit development-
  tool identity scans.

## M73 content-silent sample ZIP text failures - complete

- Base: exact clean synchronized M72 closeout
  `f4afb40aade2b1a59b7ceabf6f1db158b450b7cd`, tree
  `90e987138c2fa09fe62db2428e23421ec511a7a5`.
- Gap: CPython's standard ZIP reader strictly decodes UTF-8-marked archive-
  controlled central-directory and local-header names. Malformed bytes raise
  `UnicodeDecodeError`, bypassing M72's exact parser-exception pair and
  exposing decode details.
- Decision: RFC-0056 adds exactly `UnicodeDecodeError` to M72's private outer
  catch, reuses the stable ZIP-data error after owned cleanup, suppresses its
  rendered context, and retains the original exception programmatically.
- Boundary: no broad Unicode/value/general catch, replacement decoder,
  metadata repair, raw parser, scanner, workflow, dependency, producer,
  runtime API, or release authority.
- Research: Python documents invalid input and offset state on decoding errors;
  exact installed CPython 3.12.13, 3.13.13, and 3.14.5 source confirms strict
  UTF-8 decoding in both central-directory and local-header paths.
- Baseline: after correcting an external test-parent setup failure, exact M72
  produced 5 failures and 3 passing guards in 0.41 seconds. Both actual decode
  paths escaped raw; the catch contract and RFC/docs were absent.
- Implementation checkpoint: format, Ruff, and strict Pyright pass; 16 M72/M73
  assertions pass with only the deliberately absent RFC/docs assertion failing
  in 0.48 seconds.
- Focused gate: all 8 M73 assertions pass; inherited M64-M73 passes 108 with 1
  local capability skip; affected static checks, strict docs, and whitespace
  pass.
- Complete local candidate: the unchanged lock resolved 46 packages and the
  locked graphics environment contains 45 packages. All 316 files were format
  clean; Ruff and strict Pyright reported zero findings. CPython 3.12 passed
  2,337 tests with 15 skips; CPython 3.13/3.14 each passed 2,327 with 16 skips;
  all 797 architecture assertions passed with 1 local capability skip.
- Graphics/diagnostics: all 10 real-wgpu tests, both five-repeat profiles,
  Clockwork Arena, Agent World Builder, and all four M1-M4 diagnostic validators
  passed. M1 observed one of two engineering targets, M2 retained no targets,
  M3 observed neither graphics target, and M4 observed its baseline target.
- Pre-review artifacts: two builds reproduced a pure 273,839-byte wheel at
  `32553b1c0bf9eea3bbd3b6ab63d51ee97ef4a2d6429054dc2049439b3175af5d`
  and a 1,240,741-byte sdist at
  `5c39589b70170715d04a1a4c83a147616f7953b53ec8f9348cb9c3c78f746877`;
  wheel, staging, and complete release smoke passed. The unchanged 111,168-byte
  50-entry sample remains at
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  no inspected archive contains native/WASM entries.
- Review: no product, RFC, or scope defect remains. The local-header regression
  now observes archive closure, and the M72 catch guard uses a precise range.
  The first strengthened static gate exposed and corrected an overly generic
  test-recorder signature. The corrected focused/inherited/static/docs gate
  passes.
- Record-inclusive qualification: the unchanged lock and 45-package graphics
  environment, all 316 formatted files, Ruff, strict Pyright, 797 architecture
  assertions with 1 local capability skip, strict docs, whitespace, and full
  Git-object checking pass. Two builds reproduce the pure 273,839-byte wheel at
  `32553b1c0bf9eea3bbd3b6ab63d51ee97ef4a2d6429054dc2049439b3175af5d`
  and a 1,242,180-byte record-updated sdist at
  `5fc6b835edafdc6903b343ca038ed2b71a3f02f048536ed2e523b31ba5d82e8e`;
  wheel, staging, and complete release smoke pass. Exact commit artifact
  identity remains delegated to hosted qualification because recording this
  result changes the sdist.
- Scope: exactly 17 intended paths. Protected CI/release workflow, producer,
  package metadata, and lock hashes remain exact; no runtime package,
  dependency, benchmark, version, workflow, or release-authority change.
- Final frozen gate: the unchanged lock resolves 46 packages; all 316 files are
  format clean; Ruff and strict Pyright are clean; all 797 architecture
  assertions pass with 1 local capability skip; strict docs, whitespace, and
  full Git-object checking pass.
- Prepublication audit: feature `HEAD`, local `main`, and `origin/main` are
  exact M72 closeout `f4afb40aade2b1a59b7ceabf6f1db158b450b7cd` with
  symmetric difference `0 0`; history is linear and the candidate remains
  exactly 17 paths. GitHub reports only remote `main`, no open PR, no tag, and
  no release. Credential/private-key and explicit development-tool identity
  hygiene pass.
- Exact post-record freeze: all 316 files are format clean; Ruff and strict
  Pyright are clean; all 797 architecture assertions pass with 1 local
  capability skip; strict docs, whitespace, and exact 17-path scope pass.
- Hosted qualification: exact DCO head
  `a927c23b0e6751bd4a7876dc74a7b89f09d698be`, tree
  `562cd0a49c641270c5989e38055d8539eef2e3ca`, passed run
  `31624395783` in exactly three Linux-first allocations. Linux passed in
  5m57s, macOS in 2m13s, and Windows in 4m1s.
- Hosted suites: Linux CPython 3.12 passed 2,342 tests; Linux 3.13/3.14 and
  macOS/Windows 3.14 each passed 2,342 tests with 1 expected skip. Every OS
  passed 10 real-wgpu tests, its graphics profile, Clockwork Arena, and Agent
  World Builder. Linux also passed the base profile, static/docs,
  reproducible artifacts, installed-wheel smoke, staging, and release smoke.
- Hosted artifacts: two exact-head builds reproduced a pure 273,827-byte
  wheel at
  `b959f2ef31753f1a4514fbdcdc29695d25f3d82f71203df01f6208c24ea76afd`
  and a 1,243,346-byte sdist at
  `81631ddc7dcc79155b1e53b36d276e934ac62526f49749b78a7ab3b954ae7510`.
- Hosted review: two separated audits found no issue comment, review, inline
  comment, or review thread. PR #171 stayed clean, mergeable, and on the exact
  qualified head.
- Feature integration: PR #171 squash
  `5b9d42fba4cfc1a990bce70c1d4ea4f2e7ab04e4` has the exact reviewed tree,
  sole parent M72 closeout `f4afb40aade2b1a59b7ceabf6f1db158b450b7cd`,
  exact DCO, and a valid GitHub signature verified at
  `2026-08-12T17:59:03Z`. The feature branch is absent remotely and locally.
  The current four-file integration record changes no substantive M73
  surface.
- Integration local qualification: the exact four-file record passes the
  unchanged lock, whole-tree formatting/Ruff/strict-Pyright, all 797
  architecture assertions with 1 capability skip, strict docs, whitespace,
  full Git-object checking, two-build reproducibility, installed-wheel smoke,
  deterministic staging, and complete release smoke. The feature-identical
  pure wheel is 273,839 bytes at
  `32553b1c0bf9eea3bbd3b6ab63d51ee97ef4a2d6429054dc2049439b3175af5d`;
  the record-updated sdist is 1,244,658 bytes at
  `037d02277b58a7dc5c23cc820216deee675b8bf3fddb7d1d7cc22d1aa1dabc86`.
  Exact integration-commit artifact identity remains delegated to the bounded
  hosted documentation gate because recording this result changes the sdist.
- Integration freeze: all 316 files are format clean; Ruff and strict Pyright
  are clean; all 797 architecture assertions pass with 1 local capability
  skip; strict docs, whitespace, and exact four-file scope pass.
- Integration hosted qualification: exact DCO head
  `ddee71f4a4a9ed84679092c5734e282975004bcd`, tree
  `b1c99b4cc173e82bd35592ed59406198e935b461`, passed run
  `31626186623` in one 46-second Linux allocation; the desktop umbrella
  skipped with zero steps. The gate resolved 46 packages, found all 316 files
  format clean, passed Ruff, strict docs in 1.67 seconds, 798 selected
  architecture assertions in 9.66 seconds, reproducible artifacts,
  installed-wheel smoke, staging, and complete release smoke.
- Integration hosted artifacts: two exact-head builds reproduced the pure
  273,827-byte wheel at
  `b959f2ef31753f1a4514fbdcdc29695d25f3d82f71203df01f6208c24ea76afd`
  and a 1,245,053-byte sdist at
  `59e8a080bdc3e3e1b6680f52c17de7c903d91c68eb6dc4001232d7240f7634dd`.
- Integration hosted review: two separated audits found no issue comment,
  review, inline comment, or review thread. PR #172 stayed clean, mergeable,
  and on the exact qualified head.
- Integration record: PR #172 squash
  `bb7ca9da09d36fb166057b73e4db4d0fc806cdd0` has the exact reviewed tree,
  sole parent M73 feature squash
  `5b9d42fba4cfc1a990bce70c1d4ea4f2e7ab04e4`, exact DCO, and a valid GitHub
  signature verified at `2026-08-12T18:11:17Z`. The integration branch is
  absent remotely and locally. M73 is complete subject only to this factual
  no-run closeout record and generated-artifact pruning.
- Closeout local qualification: the unchanged lock resolves 46 packages; all
  316 files are format clean; Ruff and strict Pyright are clean; all 797
  architecture assertions pass with 1 local capability skip; strict docs,
  whitespace, full Git-object checking, and exact three-file scope pass.
- Closeout freeze: all 316 files remain format clean; Ruff and strict Pyright
  are clean; all 797 architecture assertions pass with 1 local capability
  skip; strict docs, whitespace, protected-surface isolation,
  credential/private-key hygiene, explicit development-tool identity hygiene,
  and exact three-file scope pass.

## M72 content-silent sample ZIP failures - complete

- Base: exact clean synchronized M71 closeout
  `de510b5cb44a011264a4b28f6fbbf0b59e0339e8`, tree
  `498e6e8f06509075b05d58e2be72f94c1d0818cb`.
- Gap: `BadZipFile` diagnostics can embed archive-controlled member names, and
  private complete release smoke rendered those parser exceptions directly
  despite its content-silent policy failures.
- Decision: RFC-0055 catches exactly documented `BadZipFile` and
  `LargeZipFile` outside the checksum-admitted extractor, performs owned
  cleanup first, then raises one stable error with suppressed rendered context
  while retaining the original exception programmatically.
- Boundary: private complete release smoke only. No broad catch, public error
  protocol, raw parser, scanner, telemetry, recovery, workflow, dependency,
  producer, runtime API, or release authority.
- Research: Python documents the two ZIP exceptions; local exact CPython
  3.12-3.14 source confirms archive-controlled filenames in CRC,
  central/local-name mismatch, and overlap diagnostics.
- Failing baseline: exact M71 produced 6 failures and 3 passing guards in 0.41
  seconds; raw constructor/member/ZIP64 errors escaped and docs were absent.
- Implementation checkpoint: 8 behavioral/source/protected assertions pass
  with only the deliberately absent docs/RFC assertion failing in 0.29
  seconds. Both affected Python files are format/Ruff clean and strict Pyright
  is clean.
- Focused gate: M72 passes all 9 assertions; inherited M64-M72 passes 100 with
  1 local capability skip; formatting, Ruff, strict Pyright, strict docs, and
  whitespace pass.
- Full local candidate: the unchanged lock resolved 46 packages; all 315
  Python files were format clean; Ruff and strict Pyright reported zero
  findings. CPython 3.12 passed 2,329 non-wgpu tests with 15 skips; CPython
  3.13/3.14 each passed 2,319 with 16 skips; all 789 architecture assertions
  passed with 1 local capability skip.
- Graphics/diagnostics: all 10 real-wgpu tests, both five-repeat profiles,
  Clockwork Arena, Agent World Builder, and all four M1-M4 diagnostic validators
  passed. M1 observed one of two engineering targets, M2 retained no targets,
  M3 observed neither graphics target, and M4 observed its baseline target.
- Pre-review artifacts: two builds reproduced a pure 273,687-byte wheel at
  `c2a2ea16e22be7151b0944096a96305d161d935d57e15ad94932d9721ca4e759`
  and a 1,234,046-byte sdist at
  `b9a318bc9f8b1aaa684d96f8bad56a10de74656b7c16a636908160403005b151`;
  installed-wheel, deterministic staging, and complete release smoke passed.
  The 111,168-byte 50-entry sample ZIP remains
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  no inspected wheel, sdist, or sample entry is native or WASM.
- Review: no implementation, test, or RFC defect remains. The stale legacy
  README detail that ended at M70 was corrected to M0-M71 and now names M71's
  snapshot. The corrected M64-M72 chain, affected static checks, strict docs,
  and whitespace pass.
- Record-inclusive qualification: the unchanged lock, whole-tree formatting,
  Ruff, strict Pyright, all 789 architecture assertions with 1 local capability
  skip, strict docs, whitespace, and full Git-object checking pass. Two builds
  reproduce a pure 273,704-byte review-corrected wheel at
  `11e929dbab9214c48bc621878de553a030589b39967abc87f43fab40bf4cd77e`
  and a 1,235,263-byte record-updated sdist at
  `b0372c2b5efbc486fef9cc52dd63fd515f3d095c205d1e32aa6103e1c9735a3a`;
  wheel, staging, and complete release smoke pass. Final static/docs freeze
  remains before publication.
- Final frozen gate: the unchanged lock resolves 46 packages; all 315 files are
  format clean; Ruff and strict Pyright are clean; all 789 architecture
  assertions pass with 1 local capability skip; strict docs and whitespace
  pass. The candidate is ready for exact-scope/history review and DCO
  publication.
- Prepublication audit: exact feature base, local `main`, and `origin/main` are
  M71 closeout `de510b5cb44a011264a4b28f6fbbf0b59e0339e8` with symmetric
  difference `0 0`; history is linear; the candidate is exactly 16 paths.
  Protected hashes remain exact; GitHub reports no open PR, only remote `main`,
  no tag, and no release. Credential/private-key and explicit development-tool
  identity hygiene pass.
- Exact post-record freeze: all 315 files are format clean; Ruff and strict
  Pyright are clean; all 789 architecture assertions pass with 1 local
  capability skip; strict docs and whitespace pass. The exact candidate is
  ready for DCO publication and Linux-first hosted qualification.
- Hosted qualification: exact DCO head
  `a8af08274f9e4f8cc686ee0782ef2e2fbb27e4d2`, tree
  `df4fd81c99f16b0e95f00eb485509079be73ac55`, passed run `31620403869`
  in exactly three Linux-first allocations. Linux passed in 4m59s, macOS in
  3m6s, and Windows in 3m57s.
- Hosted suites: Linux CPython 3.12, 3.13, and 3.14 passed 2,334 tests, with 1
  expected compatibility skip on 3.13/3.14. macOS and Windows CPython 3.14
  each passed 2,334 tests with 1 expected skip. Each OS passed 10 real-wgpu
  tests, its graphics profile, Clockwork Arena, and Agent World Builder;
  Linux also passed formatting, Ruff, strict Pyright/docs, the base profile,
  reproducible builds, wheel smoke, staging, and release smoke.
- Hosted artifacts: two exact-head builds reproduced a pure 273,690-byte wheel
  at `4deb9529de9a328e2d9c6f422527c21b6faf47d1c7f726865a10dffb6a26e4a9`
  and a 1,236,335-byte sdist at
  `602a9380711ecc9fe7856af6489ef10fd8b5e66edec31b3f672d737586fcf6fe`.
- Hosted review: two separated audits found no issue comment, review, inline
  comment, or review thread; the PR stayed clean, mergeable, and on the exact
  qualified head.
- Feature integration: PR #168 squash
  `65a1e90901964f40f3ef9ace63d7700f0fccd796` has the exact reviewed tree,
  sole parent M71 closeout `de510b5cb44a011264a4b28f6fbbf0b59e0339e8`,
  valid GitHub signature verified at `2026-08-12T17:10:27Z`, and exact DCO.
  The feature branch is absent remotely and locally. The current four-file
  integration record changes no substantive M72 surface.
- Integration local qualification: the exact four-file record passes the
  unchanged lock, whole-tree formatting/Ruff/strict-Pyright, all 789
  architecture assertions with 1 capability skip, strict docs, whitespace,
  full Git-object checking, two-build reproducibility, installed-wheel smoke,
  deterministic staging, and complete release smoke. The feature-identical
  pure wheel is 273,704 bytes at
  `11e929dbab9214c48bc621878de553a030589b39967abc87f43fab40bf4cd77e`;
  the record-updated sdist is 1,237,546 bytes at
  `981ad66a21e308ca29cd14abade30c4e8a80228425b479fd2645557d15607ac8`.
  Exact integration-commit artifact identity remains delegated to the bounded
  hosted documentation gate because recording this result changes the sdist.
- Integration freeze: the unchanged lock resolves 46 packages; all 315 files
  are format clean; Ruff and strict Pyright are clean; all 789 architecture
  assertions pass with 1 local capability skip; strict docs, whitespace, and
  exact four-file scope pass.
- Integration hosted qualification: exact DCO head
  `f4131213e2221e7316414448331decc09a6a2900`, tree
  `d5533287cdc618391afb15d5ebeb73b2c109becb`, passed run `31621804212`
  in one 44-second Linux allocation; the desktop umbrella skipped with zero
  steps. All 315 files were format clean; Ruff and strict docs passed; 790
  selected architecture assertions passed in 9.75 seconds; reproducible
  artifacts, wheel smoke, staging, and complete release smoke passed.
- Integration hosted artifacts: the feature-identical pure wheel is 273,690
  bytes at `4deb9529de9a328e2d9c6f422527c21b6faf47d1c7f726865a10dffb6a26e4a9`;
  the exact integration-head sdist is 1,238,037 bytes at
  `b04518bab12b29d148eab9d6a76178c99320300472adfad38cdbd9cdd0c98b89`.
- Integration review: two separated exact-head audits found no issue comment,
  review, inline comment, or review thread.
- Integration squash: PR #169 head `f413121`, tree `d553328`, squash-integrated
  as `aaa2d762bc55681a5cada448ae6ec148413370de` with the exact same tree,
  sole parent feature squash `65a1e90901964f40f3ef9ace63d7700f0fccd796`,
  valid GitHub signature verified at `2026-08-12T17:18:48Z`, and exact DCO.
  The integration branch is absent remotely and locally. The current exact
  three-record closeout changes no substantive or public project surface and
  is excluded from hosted CI.
- Closeout local qualification: exactly the three `.project` records pass all
  789 architecture assertions with 1 local capability skip, strict docs,
  whitespace, full Git-object checking, exact scope, and credential/metadata-
  identity hygiene. No workflow, runtime, verifier, producer, dependency,
  package, test, public documentation, or roadmap surface changes. The
  closeout is ready for a no-run ready PR.

## M71 checksum-admitted sample snapshot - complete

- Base: exact clean synchronized M70 closeout
  `f62631e2541f8f6a34b0ed84f489c2d7f9503747`, tree
  `f1e8ecc9b0d681a6fb4006354c8d983b2f4f119c`.
- Gap: M70 compared the source descriptor before parsing and publication, but
  `ZipFile` still consumed externally mutable bytes between those checks. A
  capable local actor could change and restore bytes without altering either
  observed digest.
- Decision: RFC-0054 copies at most 16 MiB into an owned binary spooled
  temporary file while hashing, admits only the expected digest, and gives that
  exact rewound snapshot to `ZipFile`.
- Boundary: private complete release smoke only. No persistent copy, cache,
  lock, source-immutability guarantee, raw parser, general archive sandbox,
  workflow, dependency, producer, runtime API, or release authority.
- Failing baseline: exact M70 code produced 7 failures and 2 passing guards in
  0.36 seconds; the helper, owned parser input, source independence, ordering,
  RFC, and docs were absent.
- Implementation checkpoint: M70/M71 produced 13 passes with only the absent
  documentation assertion failing in 0.41 seconds. Strict Pyright was clean;
  import ordering remained before documentation/static completion.
- Focused gate: after import normalization and the M68 historical test update,
  M71 passes 9 assertions; inherited M64-M71 passes 90 with 1 local capability
  skip; formatting, Ruff, strict Pyright, strict docs, and whitespace pass.
  Full qualification remains.
- Full local candidate: the unchanged lock resolved 46 packages; all 314
  Python files were format clean; Ruff and strict Pyright reported zero
  findings; strict docs and whitespace passed. CPython 3.12 passed 2,309
  non-wgpu tests with 15 skips, all 779 architecture assertions passed with 1
  local capability skip, and CPython 3.13/3.14 each passed 2,309 tests with 16
  skips.
- Graphics/diagnostics: all 10 real-wgpu tests, both five-repeat profiles,
  Clockwork Arena, Agent World Builder, and all four M1-M4 diagnostic validators
  passed. M1 observed one of two engineering targets, M2 retained no targets,
  M3 observed neither graphics target, and M4 observed its baseline target.
- Pre-review artifacts: two builds reproduced a pure 273,524-byte wheel at
  `791f2c909cf9b89381443f0b89d6baa79ed56f7a0bd96fa7de4d09521f597671`
  and a 1,225,504-byte sdist at
  `ef631bcdb169baa8e41036cafaaa0720edd38402db127847fb9a683e3d8e3166`;
  installed-wheel, deterministic ten-artifact staging, and complete release
  smoke passed. The 111,168-byte 50-entry sample ZIP has SHA-256
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  no inspected wheel, sdist, or sample entry is native or WASM.
- Review: no implementation defect, stale contract, or overclaim remains.
  Runtime proof was strengthened to observe `ZipFile` receiving the distinct
  snapshot and to verify source/snapshot closure after mismatch; M71 now passes
  10 assertions. Exact scope remains 18 paths with no workflow, runtime package,
  producer, benchmark, dependency, metadata, lock, or release-authority change.
  Record-inclusive qualification remains before DCO publication.
- Record-inclusive qualification: the unchanged lock, whole-tree formatting,
  Ruff, strict Pyright, all 780 architecture assertions with 1 local capability
  skip, strict docs, whitespace, and full Git-object checking pass. Two builds
  reproduce the feature-identical pure 273,524-byte wheel and a 1,227,248-byte
  record-updated sdist at
  `530ebef65bd489cf16a74760c84d4b308fc9180b62849345da4bf70b19349de0`;
  installed-wheel, deterministic staging, and complete release smoke pass.
  Recording this fact changes the sdist, so exact commit artifact identity is
  delegated to quota-bounded hosted qualification.
- Final frozen gate: the unchanged lock resolves 46 packages; all 314 files are
  format clean; Ruff and strict Pyright are clean; all 780 architecture
  assertions pass with 1 local capability skip; strict docs and whitespace
  pass. The candidate is ready for exact-scope/history review and DCO
  publication.
- Hosted qualification: exact DCO head
  `fd124202e95288f305fd57a74c918550c8104804`, tree
  `e144b20a8ec372defd7766c9d81dd943342f6adf`, passed run `31616197801`
  in exactly three Linux-first allocations. Linux passed in 7m21s, macOS in
  3m10s, and Windows in 4m12s.
- Hosted suites: Linux CPython 3.12 and every hosted 3.13/3.14 suite passed
  2,325 tests with 1 expected compatibility skip where applicable. Each OS
  passed 10 real-wgpu tests, its graphics profile, Clockwork Arena, and Agent
  World Builder; Linux also passed formatting, Ruff, strict Pyright/docs, the
  base profile, reproducible builds, wheel smoke, staging, and release smoke.
- Hosted artifacts: two exact-head builds reproduced a pure 273,509-byte wheel
  at `06c2501eb5fcc999ff2d59716bd47bc5ecafb0a25473d485d314327a57867e82`
  and a 1,227,996-byte sdist at
  `50dc7061ace2bbf1a4947246062aa355594cd95fbff44c250fe10ff8e15be678`.
- Hosted review: two separated audits found no issue comment, review, inline
  comment, or review thread; the PR stayed clean, mergeable, and on the exact
  qualified head.
- Feature integration: PR #165 squash
  `a408198b2a3ce9e59d50372095dde2afb6ac9fe5` has the exact reviewed tree,
  sole parent M70 closeout `f62631e2541f8f6a34b0ed84f489c2d7f9503747`,
  valid GitHub signature verified at `2026-08-12T16:23:48Z`, and exact DCO.
  The feature branch is absent remotely and locally. The current four-file
  integration record changes no substantive M71 surface.
- Integration local qualification: the exact four-file record passes the
  unchanged lock, whole-tree formatting/Ruff/strict-Pyright, all 780
  architecture assertions with 1 capability skip, strict docs, whitespace,
  full Git-object checking, two-build reproducibility, installed-wheel smoke,
  deterministic staging, and complete release smoke. The feature-identical
  pure wheel is 273,524 bytes at
  `791f2c909cf9b89381443f0b89d6baa79ed56f7a0bd96fa7de4d09521f597671`;
  the record-updated sdist is 1,229,599 bytes at
  `88e50fabed0299caa603166043967123997b8ecb686d10c3953fd2fc3cca24d7`.
  Exact integration-commit artifact identity remains delegated to the bounded
  hosted documentation gate because recording this result changes the sdist.
- Integration hosted qualification: exact DCO head
  `f4bb6ef2fac3d4e8d58203c7028aee0f9aa5a73a`, tree
  `ac55309b8a9a31a4706849f5954504e5292f81bf`, passed run `31617678812`
  in one 44-second Linux allocation; the desktop umbrella skipped with zero
  steps. All 314 files were format clean; Ruff and strict docs passed; 781
  selected architecture assertions passed in 9.50 seconds; reproducible
  artifacts, wheel smoke, staging, and complete release smoke passed.
- Integration hosted artifacts: the feature-identical pure wheel is 273,509
  bytes at `06c2501eb5fcc999ff2d59716bd47bc5ecafb0a25473d485d314327a57867e82`;
  the exact integration-head sdist is 1,229,985 bytes at
  `5b7a5d3d1de4de06ea83a4274c8d67fe449d7c0b24c665919acd5a2e1d348d8a`.
- Integration review: two separated exact-head audits found no issue comment,
  review, inline comment, or review thread.
- Integration squash: PR #166 head `f4bb6ef`, tree `ac55309`, squash-integrated
  as `9ce08e520c97ddb06de446718fbdc8ada90060ad` with the exact same tree,
  sole parent feature squash `a408198b2a3ce9e59d50372095dde2afb6ac9fe5`,
  valid GitHub signature verified at `2026-08-12T16:30:25Z`, and exact DCO.
  The integration branch is absent remotely and locally. The current exact
  three-record closeout changes no substantive or public project surface and
  is excluded from hosted CI.
- Closeout local qualification: exactly the three `.project` records pass all
  780 architecture assertions with 1 local capability skip, strict docs,
  whitespace, full Git-object checking, exact scope, and credential/metadata-
  identity hygiene. No workflow, runtime, verifier, producer, dependency,
  package, test, public documentation, or roadmap surface changes. The
  closeout is ready for a no-run ready PR.

## M70 sample-archive checksum binding - feature integrated

- Base: exact clean synchronized M69 closeout
  `55b409d40c32c9268ee62b8c2a14aa036bcc935f`, tree
  `51b5bdfad0a139d141ea4ea2c0195fa8ece72d6c`.
- Gap: complete release smoke validated the staged sample artifact against
  `SHA256SUMS`, then later reopened that path for extraction. M68 bound parsing
  to the new descriptor's type and size but not to the already admitted bytes.
- Decision: RFC-0053 passes the admitted sample digest to extraction, hashes
  and rewinds the same opened handle before ZIP parsing, and repeats that check
  after reads/completeness but before publication. Either mismatch uses one
  stable content-silent category.
- Boundary: private release smoke only. No snapshot, lock, immutable-input or
  race-free guarantee, change-and-restore defense, raw ZIP parser, general
  archive sandbox, workflow, dependency, sample producer, runtime API, release
  authority, or real public release observation.
- Research: Python 3.12 documents seekable file-object ZIP input and binary
  hashing; CWE-367 describes resource changes between check and use; SLSA
  identifies artifact verification as a consumer responsibility.
- Invalid setup attempt: the first focused run used a nonexistent disposable
  parent and produced 5 setup errors, 2 failures, and 1 pass. It is recorded as
  an environment failure rather than a behavioral baseline.
- Failing baseline: after creating the exact parent, unchanged M69 code
  produced 7 failures and 1 passing protected-surface guard in 0.28 seconds.
- Implementation checkpoint: the verifier and regression file produced 7
  passes with only the deliberately absent documentation assertion failing in
  0.30 seconds. After documentation, M70 passes 8 assertions in 0.26 seconds;
  M64-M70 passes 84 with 1 local capability skip in 0.71 seconds; formatting,
  Ruff, strict Pyright, strict docs, and whitespace pass. Full qualification
  remains.
- Full local candidate: after one sandbox cache-access denial, the identical
  approved gate passes the unchanged lock, 313-file formatting, Ruff, strict
  Pyright, strict docs, 2,303 non-wgpu CPython 3.12 tests with 15 skips, and
  2,303 tests with 16 skips on each of CPython 3.13.13 and 3.14.5. All 773
  architecture assertions pass with 1 local capability skip.
- Graphics/diagnostics: all 10 real-wgpu tests, both five-repeat profiles,
  both vertical slices, and all four diagnostic M1-M4 validators pass without
  changing their established evidence interpretation.
- Artifacts: two builds reproduce a pure 273,388-byte wheel at
  `865d6a8275886ecb3dab9e407c6401ab3eccf2e63a25a07ace91c4a641406f11`
  and a 1,216,959-byte source archive at
  `892b2cefdf9300f87d504dca89cf1a4cf654f46e77cea0c3b9366c6717372dc6`;
  wheel/release smoke pass.
- Review correction: the first checksum implementation read until EOF after
  descriptor admission, so a concurrently growing source could exceed M68's
  16 MiB work bound. The sample-only hasher now consumes at most that limit
  plus one rejection byte and rewinds; an unbounded-stream regression proves
  the limit.
- Corrected local gate: M70 passes 9 assertions; M64-M70 passes 85 with 1
  capability skip; Ruff, strict Pyright, strict docs, and whitespace pass. The
  complete corrected CPython 3.12 suite passes 2,304 non-wgpu tests with 15
  skips; the corrected chain passes on CPython 3.13 and 3.14 with 85 passes and
  1 skip.
- Record-inclusive qualification: the unchanged lock, whole-tree formatting,
  Ruff, strict Pyright, all 774 architecture assertions with 1 capability skip,
  strict docs, whitespace, and full Git-object checking pass. Two builds
  reproduce the feature-identical pure 273,388-byte wheel and a 1,219,320-byte
  source archive at
  `acb09696c3f920423262c81fdacd1d072eb00491a7028c0b48b3124e6f3aafb2`;
  wheel/staging/release smoke pass.
- Scope/review: no finding remains after the bounded-hash correction. The
  exact 15-path scope changes no workflow, runtime package, producer,
  benchmark, dependency, package metadata, or lock. Protected hashes remain
  exact; changed content contains no credential/private-key or explicit
  development-tool identity marker. The candidate is ready for record freeze
  and hosted feature qualification.
- Record-frozen qualification: the unchanged lock resolved 46 packages; all
  313 files were format clean; Ruff and strict Pyright were clean; all 774
  architecture assertions passed with 1 capability skip; strict docs,
  whitespace, and full Git-object checking passed. The exact candidate is
  ready for DCO publication and Linux-first hosted qualification.
- Hosted qualification: exact DCO head `7dfadaf72e74ee29d5fc0c98ef6484f6fec423a8`,
  tree `7a3ac1bb2ef9f89934325fb44228d770881c0528`, passed run
  `31611083245` in exactly three Linux-first allocations. Linux passed in
  7m12s, then macOS in 3m08s and Windows in 4m08s.
- Hosted suites: Linux CPython 3.12 and every hosted 3.13/3.14 suite passed
  2,319 tests with one expected compatibility skip. Each OS passed 10
  real-wgpu tests, its graphics profile, Clockwork Arena, and Agent World
  Builder; Linux also passed formatting, Ruff, strict Pyright/docs, the base
  profile, reproducible builds, wheel smoke, staging, and release smoke.
- Hosted artifacts: two exact-head builds reproduced a pure 273,374-byte wheel
  at `18390d39f6c267fedb832e41a0b030a03838a04c9c574fc159b45e263d67e91a`
  and a 1,220,441-byte source archive at
  `f3c9705985eb8bc3a12d71147269c181149c3dcbb77d3aa47c183b4236310790`.
- Hosted review: two separated audits found no issue comment, review, inline
  comment, or review thread; the PR remained clean and exact.
- Feature integration: PR #162 squash
  `cae3454089b4f0453859360de00129399533e2d7` has the exact reviewed tree,
  sole parent M69 closeout `55b409d40c32c9268ee62b8c2a14aa036bcc935f`,
  valid GitHub signature verified at `2026-08-12T15:26:46Z`, and exact DCO.
  The feature branch is absent remotely and locally. The current four-file
  integration record changes no substantive M70 surface.
- Integration local qualification: the exact four-file record passes the
  unchanged lock, whole-tree formatting/Ruff/strict-Pyright, all 774
  architecture assertions with 1 capability skip, strict docs, whitespace,
  full Git-object checking, two-build reproducibility, installed-wheel smoke,
  deterministic staging, and complete release smoke. The feature-identical
  pure wheel remains 273,388 bytes at
  `865d6a8275886ecb3dab9e407c6401ab3eccf2e63a25a07ace91c4a641406f11`;
  the record-updated source archive is 1,221,890 bytes at
  `af404f69f25311480130913367a1459deb21437cd0b9a800963a886bde0cee6a`.
  Recording this fact changes the sdist, so exact integration-commit artifact
  identity remains delegated to the quota-bounded hosted documentation gate.
- Integration frozen gate: the exact four files pass the unchanged lock,
  formatting, Ruff, strict Pyright, 774 architecture assertions with 1
  capability skip, strict docs, whitespace, full Git-object checking, scope,
  and credential/metadata-identity hygiene. The record is ready for bounded
  hosted documentation qualification.
- Integration hosted qualification: exact head `dda00757d1ee9365f2f3fbeddc0b89183585c9d2`,
  tree `29673a50d7bf46c7f56850117e4edd0c6f99eab8`, passed run
  `31612786971` in one 36-second Linux allocation; the desktop umbrella skipped
  with zero steps. No compatibility, graphics, profile, example, or full-suite
  runner executed.
- Integration hosted evidence: all 313 files were format clean; Ruff and
  strict docs passed; 775 selected architecture assertions passed in 7.19
  seconds. Reproducible artifacts were the feature-identical 273,374-byte
  wheel at `18390d39f6c267fedb832e41a0b030a03838a04c9c574fc159b45e263d67e91a`
  and record-updated 1,222,477-byte sdist at
  `aa903ca95706abac5f31b7f27ee0f8855e7b19162074c4a0fe422388f3e17c38`;
  wheel/staging/release smoke passed.
- Integration review: two separated exact-head audits found no issue comment,
  review, inline comment, or review thread.
- Integration squash: PR #163 head `dda0075`, tree `29673a5`, squash-integrated
  as `504d5bbe7c3ee46c71023d77748d27abd3484c74` with the exact same tree,
  sole parent feature squash `cae3454089b4f0453859360de00129399533e2d7`,
  valid GitHub signature verified at `2026-08-12T15:34:14Z`, and exact DCO.
  The integration branch is absent remotely and locally. The current exact
  three-record closeout changes no substantive or public project surface and
  is excluded from hosted CI.
- Closeout local qualification: exactly the three `.project` records pass all
  774 architecture assertions with 1 local capability skip, strict docs,
  whitespace, full Git-object checking, exact scope, and credential/metadata-
  identity hygiene. No workflow, runtime, verifier, producer, dependency,
  package, test, public documentation, or roadmap surface changes. The
  closeout is ready for a no-run ready PR.

## M69 encrypted sample-member preflight rejection - feature integrated

- Base: exact clean synchronized M68 closeout
  `fec3df4d490d363a9ab538f6b99ec86859e7acdc`, tree
  `519955303ba8638ed9847df6b0d9cb62ded25436`.
- Gap: M64 explicitly left encrypted members unchanged, so exact-inventory
  members with encryption-indicating ZIP flags reached member-open only after
  staging began and could produce an archive-controlled library message.
- Decision: RFC-0052 rejects general-purpose bits 0, 6, or 13 during the
  complete metadata preflight with one content-silent category before member
  reads or staging. The unchanged producer must emit none of those flags.
- Boundary: private project release smoke only. No password, decryption, raw
  ZIP parser, metadata-authentication guarantee, workflow, dependency,
  producer, runtime API, release authority, or real public release observation.
- Research: Python 3.12 documents ZIP decryption and password-bearing member
  reads; CPython performs traditional/strong encryption handling during
  member-open. PKWARE assigns the admitted encryption indicators to general-
  purpose bits 0, 6, and 13.
- Failing baseline: 7 failures and 1 passing boundary guard in 0.52 seconds
  proved the missing mask/helper, fail-before-staging behavior, producer
  assertion, ordering contract, RFC, and documentation.
- Local candidate: the unchanged lock and restored CPython 3.12 graphics
  environment pass whole-tree formatting/Ruff/strict-Pyright, 766 selected
  architecture/release assertions with 1 capability skip, strict docs,
  whitespace, real graphics, both profiles, both vertical slices, all four
  diagnostic validators, reproducible builds, installed-wheel smoke,
  deterministic staging, and complete release smoke.
- Supported Python: 3.12 passes 2,304 tests with 15 skips; 3.13 and the clean
  final 3.14 rerun each pass 2,294 with 16 skips. Storage-exhausted 3.14 setup
  and cache-finalization attempts are recorded as environment failures, not
  passes.
- Artifacts: two builds reproduce a pure 273,229-byte wheel at
  `bba4773ecedf1b2c749daa7e8d930da482ed040df8e7d4e25a68e4a8127d66de`
  and a 1,206,202-byte source archive at
  `22420057c1c8d7c6283666501a05f596461a3505c2ac4425bee07463caeaa3bd`;
  wheel/release smoke pass.
- Pre-publication review: no implementation defect was identified. The runtime
  regression was strengthened to forbid exact-inventory evaluation and to
  require every expected member identity to remain absent from the error.
- Reviewed artifacts: two record-inclusive builds reproduce the feature-
  identical pure 273,229-byte wheel and a 1,207,763-byte source archive at
  `54cc3fd021dfc120cf51fc7d3db31a3a3054b345c7a09547d7e6982298a9a671`.
  The factual record changes the sdist afterward; exact commit-tree artifacts
  remain delegated to hosted qualification.
- Final local gate: the unchanged lock, whole-tree static checks, 766 selected
  assertions with 1 capability skip, strict docs, whitespace, full Git-object
  checking, all protected hashes, exact 14-path scope, and added-content
  credential/identity hygiene pass. The candidate is ready for hosted feature
  qualification.
- Initial hosted qualification: PR #159 head `c4b7729` passed run
  `31590079286` in three Linux-first allocations: Linux 7m10s, macOS 2m31s,
  and Windows 4m07s. Linux baseline and every compatibility suite passed 2,309
  tests, with one expected compatibility skip. Every operating system passed
  10 real-wgpu tests, its graphics profile, Clockwork Arena, and Agent World
  Builder; Linux also passed the base profile. Reproducibility, wheel smoke,
  ten-artifact staging, and release smoke passed.
- Hosted review correction: the sole P2 thread correctly identified that
  encryption validation shared the per-member metadata loop. An unsafe member
  earlier in archive order could therefore mask a later encrypted member. The
  verifier now completes a dedicated all-member encryption-flag pass before
  any path or other member metadata validation; an order-adversarial regression
  protects that precedence.
- Corrected local qualification: all 312 Python files are format clean; Ruff
  and strict Pyright are clean; M64-M69 pass 76 assertions with 1 capability
  skip; the complete CPython 3.12 suite passes 2,305 tests with 15 skips; all
  767 architecture/release assertions pass with 1 skip; strict docs and
  whitespace pass. Two builds reproduce the unchanged pure 273,229-byte wheel
  at `bba4773ecedf1b2c749daa7e8d930da482ed040df8e7d4e25a68e4a8127d66de`
  and a 1,208,657-byte source archive at
  `85d8cc5f2d9cb9ecedc763176abb428726c8eab76e4c59e3b885e03b6df3ff6f`;
  installed-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke pass.
- Corrected hosted qualification: exact head `cea31f5`, tree `9652eded`, passed
  run `31591830264` in exactly three Linux-first allocations. Linux passed in
  7m11s, then macOS in 2m02s and Windows in 3m59s. Linux baseline and every
  hosted compatibility suite passed 2,310 tests with one expected compatibility
  skip. Each OS passed 10 real-wgpu tests, its graphics profile, Clockwork
  Arena, and Agent World Builder; Linux also passed the base profile.
- Hosted artifacts: two exact-head builds reproduced a pure 273,216-byte wheel
  at `805a0348c76a45a302a271c0386057eaa545594bf254818a5be2d6745f062d32`
  and a 1,210,777-byte source archive at
  `9783a01b07a22423e71414b6edfa64ea922ed3bc04df31f5018244206cd74dfc`;
  installed-wheel smoke, deterministic ten-artifact staging, and complete
  release smoke passed.
- Hosted review: the sole P2 was answered with exact correction evidence and
  resolved after the corrected head passed. Two separated delayed audits found
  no issue comment, new actionable review, or unresolved thread.
- Feature integration: PR #159 corrected head
  `cea31f5e6b52ff8c6ba0858425266723924726a3`, tree
  `9652eded10bb48251bd67393f93cd90ca307d1d8`, squash-integrated as
  `9d298f800964b4237f204ea4acc366d224bcf76f` with the exact same tree, sole
  parent M68 closeout `fec3df4d490d363a9ab538f6b99ec86859e7acdc`,
  valid GitHub signature verified at `2026-08-12T14:23:14Z`, and exact DCO.
  The feature branch is absent remotely and locally. The current four-file
  integration record changes no substantive M69 surface.
- Integration local qualification: exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`
  pass the unchanged lock, whole-tree formatting/Ruff/strict-Pyright, all 767
  architecture/release assertions with 1 capability skip, strict docs,
  whitespace, full Git-object checking, two-build reproducibility,
  installed-wheel smoke, deterministic staging, and complete release smoke.
  The feature-identical pure wheel remains 273,229 bytes at
  `bba4773ecedf1b2c749daa7e8d930da482ed040df8e7d4e25a68e4a8127d66de`;
  the record-updated source archive is 1,212,288 bytes at
  `6eaf97ad765abf4e28ca4107231cdb0861adcef05e2ab24b942bc56961922b13`.
  Recording this fact changes the sdist, so exact integration-commit artifact
  identity remains delegated to the quota-bounded hosted documentation gate.
- Integration hosted qualification: exact head `7a19c9d`, tree `c5ebdd4`,
  passed run `31607127000` in one 41-second Linux allocation; the desktop
  umbrella skipped with zero steps. The run did not allocate compatibility,
  software-rendering, full-suite, profile, graphics, example, or desktop work.
- Integration hosted evidence: formatting, Ruff, strict docs, 766 selected
  architecture assertions, two-build reproducibility, installed-wheel smoke,
  deterministic staging, and complete release smoke passed. The pure wheel is
  feature-identical at 273,216 bytes and
  `805a0348c76a45a302a271c0386057eaa545594bf254818a5be2d6745f062d32`;
  the record-updated source archive is 1,212,886 bytes at
  `a262564238b30683cedc5ff7e07005318f2590c0804f9bacd96fd3f765ff8de9`.
- Integration review: two separated exact-head audits found no issue comment,
  review, or thread.
- Integration squash: PR #160 head
  `7a19c9d4005992afbb4f3ee738f2d26f93515d65`, tree
  `c5ebdd4769118ed86fb7c50f557dcdd42be87597`, squash-integrated as
  `9fcd61d1a3b93801b1bfd5a56392007fa15c6e03` with the exact same tree, sole
  parent feature squash `9d298f800964b4237f204ea4acc366d224bcf76f`,
  valid GitHub signature verified at `2026-08-12T14:32:43Z`, and exact DCO.
  The integration branch is absent remotely and locally. The current exact
  three-record closeout changes no substantive or public project surface and
  is excluded from hosted CI.
- Closeout local qualification: exactly the three `.project` records pass all
  765 architecture assertions with 1 local capability skip, strict docs,
  whitespace, full Git-object checking, exact scope, and added-content
  credential/identity hygiene. No workflow, runtime, verifier, producer,
  dependency, package, test, public documentation, or roadmap surface changes.
  PR #161 squash `55b409d40c32c9268ee62b8c2a14aa036bcc935f` has exact tree
  `51b5bdfad0a139d141ea4ea2c0195fa8ece72d6c`, sole parent M69 integration
  squash `9fcd61d1a3b93801b1bfd5a56392007fa15c6e03`, a valid GitHub
  signature verified at `2026-08-12T14:38:30Z`, and exact DCO. No hosted run
  was created. Every M69 branch and generated output is absent; synchronized
  clean `main` is the M70 base.

## M68 bounded sample-archive container admission - feature integrated

- Base: exact clean synchronized M67 closeout
  `ea3de73f5ef1792df729c1f271b3d84a28db1028`, tree
  `feed6f892798f0030974c957fa6b5f1352c8b53c`.
- Gap: M64-M67 bound admitted extraction work only after `zipfile` receives an
  unbounded archive path and parses its central directory.
- Decision: RFC-0051 adds a private 16 MiB container limit. Path metadata
  rejects obvious non-regular or oversized inputs before open; descriptor
  metadata revalidates the opened source; that same handle is passed to
  `ZipFile` and closed after the archive.
- Boundary: private project release smoke only. No raw parser, general archive
  sandbox, immutable-input or concurrent-race guarantee, workflow, dependency,
  producer, runtime API, release authority, or real public release observation.
- Research: Python documents seekable file-object input and archive resource
  limits; OWASP recommends stored-file and post-decompression size limits. The
  exact project sample is 111,168 bytes, giving the 16 MiB cap over 150-fold
  current headroom while complementing the unchanged 8 MiB expansion cap.
- Failing baseline: 6 failures and 2 passing guards in 0.34 seconds proved the
  missing limit/helper, fail-before-parser behavior, same-handle identity, and
  ordering contract.
- Local candidate: all 311 Python files are format clean; Ruff and strict
  Pyright report zero findings; strict docs and whitespace pass. Pre-review
  complete suites passed 2,295 tests with 15 skips on CPython 3.12 and 2,285
  with 16 skips on CPython 3.13/3.14. Real-wgpu, profiles, vertical slices, and
  all M1-M4 diagnostic validators pass.
- Review correction: descriptor-only validation could block while opening a
  FIFO and could miss the intended stable category for a directory. Pre-open
  path metadata now rejects obvious special sources, while authoritative
  descriptor revalidation catches replacement. The reviewed M64-M68 contract
  passes 67 assertions with 1 local capability skip on every supported Python;
  corrected CPython 3.12 passes 2,296 tests with 15 skips.
- Pre-review artifacts: two builds reproduced a pure 273,082-byte wheel at
  `089c787bd156e3af5f36fa20dbab1a69e953cc913b9367d9b023e1ccb18977fe`
  and a 1,198,756-byte source archive at
  `f135564122dacca5e3cd3c10e20005a7d40e4a9eda774b00a2771bb036d23f68`.
  Installed-wheel and complete release smoke passed. A later record-inclusive
  rebuild reproduced a pure 273,106-byte wheel at
  `685c3baaa66ed325c471b5deb5f3f44590eb1bbc2c177ebdd53bc39366119c22`
  and a 1,200,373-byte source archive at
  `5d1bcb8424c13145977d53484a164457911ddfeb7d0e6e972e27399708afeaeb`;
  both smoke paths passed again. Those factual local records changed the sdist;
  exact commit-tree artifacts are recorded below from hosted qualification.
- Feature integration: PR #156 reviewed head
  `0fbccca248e6a00a79631ca12c2afa6e7b9acdac`, tree
  `7e03726ebea72d074e0404f6c8073f96e0e8cce5`, squash-integrated as
  `5bd0196128aeffcf21094d0a0c6d78b624aaf49b` with the exact same tree, sole
  parent M67 closeout, valid GitHub signature, and exact DCO trailer.
- Hosted qualification: exact head `0fbccca` passed run `31585838550` in
  exactly three Linux-first allocations. Linux passed in 7m34s; macOS passed
  in 2m58s; Windows passed in 4m13s. Baseline and every compatibility suite
  passed 2,301 tests with one compatibility skip. All real-wgpu, profile,
  vertical-slice, reproducibility, wheel, staging, and release-smoke gates
  passed.
- Hosted artifacts: two builds reproduced a pure 273,092-byte wheel at
  `85378f6485a06a8e1496e775fa8f71b122a899bdd0731ba3d67e1eda0f06db58`
  and a 1,200,886-byte source archive at
  `d1ac76ec6d3e62be894e894a862fbde09fa0aca07b58a8277b2ea33f96fdc977`.
- Hosted review: two delayed exact-head audits found no comment, review, or
  unresolved thread. The feature branch is absent remotely and locally.
- Integration record: exactly the three `.project` records and `ROADMAP.md`
  pass the unchanged lock, whole-tree formatting/Ruff/strict-Pyright, all 758
  selected architecture/release-artifact assertions with 1 local capability
  skip, strict docs, whitespace, full Git-object checking, two-build
  reproducibility, installed-wheel smoke, deterministic staging, and complete
  M68 release smoke. The pure 273,106-byte wheel remains unchanged; exact
  integration-commit sdist identity is delegated to hosted qualification.
- Integration hosted qualification: exact head `cd65d13` passed run
  `31587335592` in one 43-second Linux allocation. The desktop compatibility
  umbrella skipped with zero steps. Hosted formatting, Ruff, strict docs, all
  757 documentation-selected architecture assertions, two-build
  reproducibility, isolated-wheel smoke, deterministic staging, and complete
  M68 release smoke passed.
- Integration hosted artifacts: two builds reproduced the feature-identical
  273,092-byte wheel at
  `85378f6485a06a8e1496e775fa8f71b122a899bdd0731ba3d67e1eda0f06db58`
  and a record-updated 1,202,598-byte source archive at
  `32d390922dbfc9a62eb19fdf0ea4f35f6817a2da7c676534d6849bafbee3cc6e`.
- Integration review: two delayed exact-head audits found no comment, review,
  or unresolved thread.
- Integration squash: PR #157 head
  `cd65d1345b2725eb3be4daeb899535eacb740dee`, tree
  `83e765ba0fa92038aeefaaf2dcf9d2fb85eec052`, squash-integrated as
  `69fe032bfa0af6513d46e7c7492ffa3a5720d163` with the exact same tree, sole
  parent feature squash, valid GitHub signature, and exact DCO trailer. The
  integration branch is absent remotely and locally.
- Closeout state: PR #158 squash
  `fec3df4d490d363a9ab538f6b99ec86859e7acdc` has the exact three-record tree
  `519955303ba8638ed9847df6b0d9cb62ded25436`, sole parent M68 integration
  squash, valid GitHub signature, and exact DCO trailer. It requested no hosted
  runner. Every M68 branch and generated output is absent; synchronized clean
  `main` is the M69 base.

## M67 exact sample-bundle inventory conformance - fully integrated

- Base: exact clean synchronized M66 closeout
  `995fdda097a418a7a0e570bb6b492d3f5609d471`, tree
  `54da91c867211007156d5006512a426815a8374b`.
- Feature integration: PR #153 reviewed head
  `3cb44d412d71a930f84a1545e59f893643d68666`, tree
  `cd8833bbd93e11c7e7e678ee324711503a921d97`, squash-integrated as
  `bc8a3d9a24bab5860e48af919dbeab4ca4c913f2` with the exact same tree, sole
  parent M66 closeout, valid GitHub signature, and exact DCO trailer.
- Integration record: PR #154 exact four-file head
  `565053e8cf0f3961f8bfbc1a54df04a604240183`, tree
  `eb532eddbd368efaaa1a896efd930727cc5b3059`, squash-integrated as
  `5025877d31a2bc8a9a0a1b7bb2e106869f76066f` with the exact same tree, sole
  parent feature squash, valid GitHub signature, and exact DCO trailer.
- Current branch: `docs/m67-closeout`.
- Gap: M64-M66 validate bounded portable transactional extraction, but the
  final completeness check covers only a root-level subset. Extra portable
  files and missing nested assets are not rejected as an exact product-shape
  mismatch before extraction.
- Decision: RFC-0050 adds an independent source-defined expectation for the 50
  regular files currently emitted by the unchanged sample producer. The
  complete preflighted identity set must match exactly before member reads or
  staging; either mismatch uses one content-silent category.
- Boundary: private project sample verification only. No content scanning,
  general archive sandbox, workflow, dependency, producer, runtime API,
  release authority, or real public release observation.
- Research: Python requires archive inspection before untrusted extraction;
  OWASP recommends allowlist and pre-extraction checks; SLSA 1.2 recommends
  comparing artifacts to source-defined expectations and rejecting unrecognized
  inputs. M67 adopts only the narrow exact-inventory consequence.
- Failing baseline: 5 failures and 3 passing guards in 0.33 seconds proved the
  missing expectation, pre-read mismatch rejection, source-ordering contract,
  and documentation gap while preserving producer and boundary guards.
- Local candidate: the unchanged lock and restored graphics environment pass
  whole-tree static checks, 747 reviewed architecture assertions with 1
  capability skip, strict docs, release-artifact tests, and whitespace. CPython 3.12 passes 2,286
  tests with 15 skips; 3.13/3.14 each pass 2,276 with 16 skips. Ten real-wgpu
  tests, both profiles, both vertical slices, four diagnostic benchmark
  validators, reproducible distributions, isolated-wheel smoke, deterministic
  staging, and complete release smoke pass.
- Artifacts: two builds reproduced a pure 272,880-byte wheel at
  `dba45ae505702b2bb04e1666adce518f87239158f2e5ba3cafd19ee82c50016b`
  and a 1,190,493-byte source archive at
  `962068fd8537e13639efc0d528179911e2beeab8a0a8ccce1776a641c09ade12`.
  The wheel contains 94 entries, the sdist 500 including the M67 test and RFC,
  and the staged sample ZIP exactly 50 files; no inspected archive contains a
  native library or WASM file.
- Review: separate 49/51-member fixtures left a count-only test loophole. The
  strengthened test uses a 50-member substitution and rejects staging creation
  directly. This changed tests only; M64-M67 now pass 58 assertions with 1
  capability skip. No remaining finding was identified.
- Hosted qualification: exact feature head `3cb44d4` passed run `31534773135`
  in exactly three Linux-first allocations. Linux passed in 7m44s; only then
  macOS and Windows began, passing in 3m22s and 4m15s. Every baseline and
  compatibility suite passed 2,292 tests with one compatibility skip; all
  real-wgpu, profile, vertical-slice, reproducibility, wheel, staging, and
  release-smoke gates passed.
- Hosted artifacts: two builds reproduced a pure 272,867-byte wheel at
  `5b67653c5f4374ffc52f55eadc9d2e29fc72e8281969d6c891da3b56042475a8`
  and a 1,191,892-byte source archive at
  `79bf91855560aa26b4a2a8c6082b08b164eb22e7baece36b05397191f171bdb1`.
- Hosted review: two delayed exact-head audits found no review, comment, or
  unresolved thread. The feature branch is absent locally and remotely.
- Integration record: exactly the three `.project` records and `ROADMAP.md`
  pass the unchanged lock, whole-tree formatting/Ruff/strict-Pyright, all 747
  architecture assertions with 1 capability skip, both release-artifact tests,
  strict docs, whitespace, full Git-object checking, two-build reproducibility,
  installed-wheel smoke, deterministic staging, and complete release smoke.
- Integration hosted qualification: exact head `565053e` passed run
  `31536520514` in one 41-second Linux allocation. The desktop compatibility
  umbrella skipped with zero steps. Hosted formatting, Ruff, strict docs, all
  748 documentation-selected architecture assertions, two-build
  reproducibility, isolated-wheel smoke, deterministic staging, and complete
  M67 release smoke passed.
- Integration hosted artifacts: two builds reproduced the feature-identical
  272,867-byte wheel at
  `5b67653c5f4374ffc52f55eadc9d2e29fc72e8281969d6c891da3b56042475a8`
  and a 1,193,131-byte record-updated source archive at
  `ca246f1f23225cf43e5f81a5eda1b60629f6ff47dc389d4700e7a53b97606389`.
- Integration review resolution: delayed review comment `3761750291`
  incorrectly claimed the sole integration commit lacked DCO. GitHub and local
  trailer parsing proved the exact authorized trailer; evidence reply
  `3765169173` was posted, thread `PRRT_kwDOTtqoGs6YYOGq` resolved, and two
  post-resolution audits found no later activity.
- Closeout state: feature and integration branches are absent locally and
  remotely; the three-file closeout records the verified integration squash and
  requests no hosted runner. Its exact three-file tree passes all 747
  architecture assertions with 1 capability skip, strict docs, whitespace,
  full Git-object checking, and scope validation.

## M66 staged sample-root publication - feature integrated

- Base: exact clean synchronized M65 closeout
  `0892f4b234be5ea06d6a91f3b1f0b50a1f44eb1f`, tree
  `a8e028df3db9b6eb0293cd9177cedcda3367666a`.
- Current branch: `docs/m66-integration-record`.
- Gap: after complete M64/M65 preflight, release smoke writes directly beneath
  the final versioned sample root. A later streamed-size, decompression, I/O, or
  completeness failure can leave a partial tree at the complete-tree identity.
- Decision: RFC-0049 requires an existing real output directory and absent final
  entry. Extraction uses an owned same-filesystem temporary staging directory;
  required files are validated there; one rename publishes the complete root;
  and context-owned cleanup removes partial staging after any pre-publication
  failure while preserving the cause and unowned paths.
- Boundary: private single-process release smoke only. No crash durability,
  `fsync`, journal, general archive sandbox, concurrent filesystem race
  isolation, post-publication rollback, workflow, dependency, producer,
  runtime API, release authority, or real public release observation.
- Failing baseline: 8 failures, 2 passing guards, and 1 Windows symbolic-link
  capability skip in 0.36 seconds proved surviving partial roots, unstable
  existing-entry handling, silent output-parent creation, and the absence of a
  staged publication boundary and RFC.
- Local candidate: whole-tree format/Ruff/strict-Pyright, 736 architecture
  assertions, strict docs, and whitespace pass. Supported CPython suites each
  pass 2,266 tests; 3.12 has 15 expected skips and 3.13/3.14 each have 16. Ten
  real-wgpu tests, both profiles, both vertical slices, and all four diagnostic
  benchmark validators pass. Final reviewed builds reproduce a pure 272,709-
  byte wheel and 1,183,308-byte sdist; installed-wheel and complete staged-
  release smoke pass.
- Review: a tests-first review correction added `Path.is_junction()` to the
  real-directory admission check. Review also added direct proof of mid-stream
  I/O cleanup and preservation of a final-root collision created after initial
  preflight. The final focused file passes 13 assertions with 1 local symbolic-
  link capability skip. No further blocker or non-blocking finding remains.
- Environment: two earlier full-suite attempts were invalidated by a full
  system drive. The first produced no valid summary; the second passed 2,265
  tests before its only fixture write failed. Moving only pytest temporary
  repositories to `D:` produced the complete passing matrix above.
- Hosted qualification: exact DCO head `facda31545cd490187e7679d613cd9bb5149028d`
  passed run `31529725573` in exactly three Linux-first allocations. Linux
  passed in 7m17s, macOS in 2m07s, and Windows in 3m21s. Linux baseline and
  Ubuntu 3.13/3.14 each passed 2,283 tests, with one expected compatibility
  skip; macOS and Windows 3.14 each passed 2,283 with one skip. Real-wgpu
  passed 10 tests on every operating system; profiles, vertical slices,
  reproducibility, installed-wheel smoke, staging, and release smoke passed.
- Hosted artifacts: two builds reproduced a pure 272,695-byte wheel at
  `d72a13dcecdcaa1cef53392b0c2fb6d7eba10b817894985588e3524f8f2a2874` and a
  1,183,498-byte source archive at
  `89f1e1cd845445c3a55030c32af2f1c247d43639cd2c0eb18a47b7a8994ec360`.
- Review and integration: one review comment cited an absent commit as missing
  DCO. Exact GitHub/local commit-list and trailer evidence disproved it; the
  response is attached, the thread resolved, and two delayed audits found no
  later activity. GitHub-verified squash `79593b01d670dd07fb761e493382685765d13d7a`
  has the exact reviewed tree, sole parent exact M65 closeout, valid signature,
  and parsed DCO. The feature branch is absent locally/remotely. This four-file
  record requests one Linux documentation/distribution allocation and a skipped
  zero-step desktop umbrella; the following three-record closeout requests none.
- Integration-record local gate: the exact four-file scope passes the unchanged
  lock, formatting for 309 files, Ruff, strict Pyright, all 738 architecture
  assertions with 1 local capability skip, strict docs, and whitespace. Two
  builds reproduce the unchanged 272,709-byte wheel and a 1,185,006-byte
  record-updated sdist; installed-wheel and complete release smoke pass. This
  evidence edit changes the source archive again, so exact commit-tree artifact
  identity remains delegated to the one-allocation hosted gate.
- Integration evidence: ready PR #151 exact four-document head
  `595eb77c42de31211c4d164e949cf0fa4d5db3c3` passed run `31531603994` in
  one 43-second Linux allocation; the desktop umbrella skipped with zero steps.
  Hosted formatting for 309 files, Ruff, strict docs in 1.66 seconds, 739
  documentation-selected architecture assertions in 8.91 seconds, two-build
  reproducibility, installed-wheel smoke, staging, and complete release smoke
  passed. The hosted wheel remained 272,695 bytes at
  `d72a13dcecdcaa1cef53392b0c2fb6d7eba10b817894985588e3524f8f2a2874`;
  the record-updated 1,185,305-byte sdist was
  `d9ebe95fe0a30777e0138ce1434e9c31ac21bbfb6ba4b6856740310a1b087c5f`.
  Two delayed audits found no review, issue comment, or review comment.
- Integration squash: GitHub-verified
  `bcc91aa97d3157971eb4ba52f2430b8bb65c4ab6` has exact reviewed tree
  `8ed42b87e04ed93fb205f06878bc5f85cf26b8b5`, sole parent the feature
  squash, valid signature verified at `2026-08-11T20:14:33Z`, and parsed DCO.
  The integration branch is absent locally/remotely. This pending exact three-
  record closeout requests no hosted runner and establishes the M67 base.

## M65 portable sample member paths - feature integrated

- Base: exact clean synchronized M64 closeout
  `92e706961e2ecd4e2c187a205cc045a8c6506ab9`, tree
  `8df4aaa8222517d729234792d162dfc115674767`.
- Current branch: `docs/m65-integration-record`.
- Gap: M64 confines and resource-bounds sample extraction but admits duplicate,
  case-only, case-ambiguous-ancestor, explicit-directory, Windows-device,
  trailing-period, non-ASCII, overlong, and file/directory prefix-collision
  member paths as well as explicitly encoded non-regular types. Host behavior
  can overwrite, merge, reinterpret, or fail after earlier writes.
- Decision: RFC-0048 admits only regular files beneath the exact root. Relative
  paths contain at most 255 ASCII characters; each component follows the
  portable grammar, has no trailing period or Windows device stem, and is not
  rewritten. Complete paths are case-insensitively unique, directory ancestors
  retain one spelling, and no file path prefixes another file. Explicit non-
  regular mode types fail; omitted type bits remain common-producer compatible.
- Boundary: private release tooling only. No Unicode normalization, filesystem
  probing, general archive sandbox, cleanup, workflow, dependency, producer,
  runtime API, release authority, or real public release observation.
- Development state: the new 18-case file initially failed 16 assertions and
  passed two guards in 0.56 seconds against unchanged M64 code. The first
  implementation gate stopped on one Ruff formatting change. After formatting,
  both changed Python files are format/Ruff/strict-Pyright clean and all 17
  non-documentation assertions pass in 0.26 seconds. The complete contract
  passes all 18 assertions in 0.23 seconds; strict docs build in 1.11 seconds;
  all 720 architecture assertions and both release-artifact tests pass. Full
  candidate validation and review remain pending.
- Pre-hosted candidate state: the graphics-enabled candidate passes 2,260 tests with 14
  expected skips on each supported CPython version. Real-wgpu, both five-repeat
  profiles, both vertical slices, and all four diagnostic benchmark validators
  pass. Two builds reproduce a 272,430-byte wheel and 1,169,917-byte source
  archive; isolated-wheel and complete release smoke pass.
- Review: local review strengthened the exact upper boundary with direct proof
  that a 255-ASCII-character relative path is admitted. Hosted review then
  found that FIFO, socket, and device modes without a trailing slash passed the
  filename-based directory and symlink checks. Four reviewer-derived fixtures
  reproduced the defect before the correction and now pass. The implementation
  accepts absent type bits, explicit regular files, and rejects every explicit
  non-regular file type before extraction.
- Pre-hosted reviewed source/matrix state: the unchanged lock and restored 45-package
  graphics environment pass whole-tree formatting, Ruff, strict Pyright, all
  721 architecture assertions, strict docs, and whitespace. The reviewed
  candidate passes 2,261 tests with 14 expected skips on every supported
  CPython version. Earlier real-wgpu, profiles, vertical slices, and diagnostic
  benchmark results remain applicable because review changed only tests and
  records. Two final builds reproduce a 272,430-byte wheel and 1,171,921-byte
  source archive; installed-wheel, staging, and complete release smoke pass.
  This evidence edit changes the source archive again, so exact commit-tree
  artifact identity remains delegated to hosted qualification. The final
  record-frozen source gate passes.
- Initial hosted state: ready PR #147 exact head
  `fce4140dd2d1b2982a1e90091dd2b157b00e861c` passed run `31521633593`
  in the unchanged three Linux-first allocations. Linux `93879809651` passed
  in 5m24s, macOS `93881371543` in 2m50s, and Windows `93881371674` in 4m05s.
  Review comment `3760580215` is valid and blocks merging that initial head.
- Corrected candidate state: whole-tree static/docs and all 727 architecture/
  release assertions pass. Each graphics-enabled local supported-Python suite
  passes 2,265 tests with 14 expected skips; real-wgpu, profiles, and vertical
  slices pass. Two builds reproduce a 272,430-byte wheel at
  `f563d5a7f2ab11c28404462de33454108d74e68528c65742d9417dc9736a3020`
  and a 1,172,451-byte source archive at
  `fabf9855670bef2801fa7951a5f9c38cb737fc89a1ad037548b922ca254ea154`;
  isolated-wheel and complete release smoke pass. Exact commit-tree artifact
  identity was then delegated to the corrected hosted gate recorded below.
- Hosted correction: exact amended head
  `9de1e2e6ea11b4058bb61b4102043273715875ee` passed run `31523863615` in
  the unchanged three Linux-first allocations. Linux `93887270228` passed in
  7m32s, macOS `93889429991` in 2m09s, and Windows `93889429975` in 4m11s.
  Baseline and every compatibility suite passed 2,269 tests, with one expected
  compatibility skip; real-wgpu, profiles, vertical slices, reproducibility,
  installed-wheel smoke, staging, and complete release smoke passed.
- Hosted artifacts: two builds reproduced a pure 272,473-byte wheel at
  `4bb773ae13a5b8f4a132ef7488b783cb0249f6e4ff7e3640016c7207872c5c87`
  and a 1,174,818-byte source archive at
  `123f08b48bf2c0eef3058024182cc1389544fd70eb361c00b30b1fba73530738`.
- Review and integration: the one valid review finding was answered and its
  thread resolved after the corrected hosted pass. Two delayed audits found no
  later activity. GitHub-verified squash
  `b01335592d0e984c6b3eb6a35d31294081cff0d5` has the exact reviewed tree,
  sole parent exact M64 closeout, valid signature, and parsed DCO trailer. The
  feature branch is absent remotely and deleted locally. This four-document
  record requests one Linux documentation/distribution allocation and a
  skipped zero-step desktop umbrella; the following three-record closeout will
  request none.
- Integration evidence: ready PR #148 exact four-document head
  `1401a2423bdbd001c359735a365f4be14a010d60` passed run `31525664897` in
  one 43-second Linux allocation. The desktop umbrella skipped with zero steps.
  Hosted formatting, Ruff, strict docs, 725 architecture assertions, two-build
  reproducibility, installed-wheel smoke, staging, and complete release smoke
  passed. The hosted wheel remained 272,473 bytes at
  `4bb773ae13a5b8f4a132ef7488b783cb0249f6e4ff7e3640016c7207872c5c87`;
  the record-updated 1,176,061-byte source archive was
  `d148c700f4b09a35518cb3a61e3116088f28c4549137de85ac73b7c82d799b85`.
  Two delayed audits found no review, issue comment, review comment, or thread.
  GitHub-verified squash `b88090a78fdd6cb4978863e0792d7741cd07efb3`
  has exact reviewed tree `2c24ce9d68e7068d745f794a423b6d6d60d971b2`,
  sole parent the feature squash, valid signature, and parsed DCO trailer. The
  integration branch is absent remotely and deleted locally. This pending exact
  three-record closeout requests no hosted runner and will establish the M66
  selection base.

## M64 bounded sample-bundle extraction - complete

- Base: exact clean synchronized M63 closeout
  `a92330c5d592eaeba69e75e25dd94d83b22d367f`, tree
  `86cf786b01eb92ff39fcdbdc5464540f4b3c8eea`.
- Gap: the release smoke trusted unbounded member count and declared expansion,
  wrote earlier members before discovering a later metadata violation, and
  allocated each complete expanded member through `ZipFile.read()`.
- Decision: RFC-0047 admits at most 256 members, 1 MiB declared uncompressed per
  member, and 8 MiB declared uncompressed total. Complete path, link, codec,
  count, and size preflight precedes extraction; stored and deflated files
  stream in 64 KiB blocks and must exactly reproduce declared size. BZIP2,
  LZMA, and unknown methods fail before extraction.
- Boundary: private release tooling only. No general archive sandbox,
  transactional cleanup, filename-policy expansion, workflow, dependency,
  runtime API, release authority, or real public release observation.
- Local evidence: the final corrected candidate is format/Ruff/strict-Pyright
  clean. All 13 focused M64 assertions and 704 inherited architecture/release-
  artifact assertions pass. Every supported graphics-enabled CPython suite
  passes 2,242 tests with 14 expected skips; real-wgpu, profiles, vertical
  slices, and all four diagnostic benchmark validators pass. Two fresh builds
  reproduce a 272,239-byte wheel and 1,163,429-byte source archive; isolated-
  wheel and complete bounded release smoke pass.
- Hosted correction: initial head `c5813633f8ff7970311cc7ab8e1159f844c056f7`
  passed its three allocations but was not merged because review found that
  BZIP2/LZMA reads could decompress without a maximum-output argument before
  truncating to forged declared size. The corrected stored/deflated-only
  admission and regressions pass, the response was accepted, and the sole
  thread is resolved.
- Hosted evidence: corrected exact head
  `8b6861df891f12d194bc9b7e98b41ac8ab81f7d1` passed run `31515782370` in
  exactly three Linux-first allocations. Linux `93860439338` passed in 7m13s,
  macOS `93862476671` in 2m55s, and Windows `93862476577` in 4m06s. Baseline
  passed 2,246 tests; each compatibility suite passed 2,246 with one expected
  skip. Real-wgpu, profiles, both vertical slices, reproducible builds,
  installed-wheel smoke, and complete release smoke passed. Hosted artifacts
  were a 272,227-byte wheel at
  `4eb1cb0b2524f188056c619c7e5757b41c739ff3d889f49982c026dba7a60a3b` and
  a 1,163,806-byte source archive at
  `718d719b0c0c40cf1af93aa5e5aa398fbfbdd5439de1067003deb6dba40c69b2`.
- Review and integration: two delayed corrected-head audits found no later
  review or comment. GitHub-verified PR #144 squash
  `8399e0f94838f455ead604eceee0a17e1b2c9a91` has exact reviewed tree
  `3f46ec8c23a044a20823a7d9132906cc2efdb3fa`, sole parent exact M63 closeout,
  and a valid signature. Both source commits carry exact DCO sign-offs; the
  generated squash message contains escaped line-break text, so no standalone
  trailer claim is made for that merge commit. The feature branch is deleted
  remotely. This four-document integration record requests one Linux
  documentation/distribution allocation and a skipped zero-step desktop
  umbrella; the subsequent three-record closeout requests none.
- Integration-record local gate: the exact four-file scope passes the unchanged
  lock, formatting for 307 files, Ruff, strict Pyright, all 702 architecture
  assertions, strict docs, and whitespace. Two pre-final-record builds
  reproduced the unchanged 272,239-byte wheel and a 1,163,698-byte record-
  updated source archive; installed-wheel and complete release smoke pass. The
  final evidence edit changes the source archive again, so exact commit-tree
  artifact identity remains delegated to the one-allocation hosted gate.
- Integration evidence: ready PR #145 exact head
  `49857245d37aaf8ea1b8a0cf702897a17b3f79ab` passed run `31517725574` in one
  42-second Linux allocation. The desktop umbrella skipped with zero steps.
  Hosted formatting, Ruff, strict docs, all 702 architecture assertions,
  reproducible distribution, installed-wheel smoke, staging, and complete
  release smoke passed. The exact hosted wheel remained 272,227 bytes at
  `4eb1cb0b2524f188056c619c7e5757b41c739ff3d889f49982c026dba7a60a3b`;
  the record-updated source archive was 1,163,996 bytes at
  `d6ed5eef92c48c40f97749ad95d69b718551bafbd1024b8ee69e8dd517bbd077`.
  Two delayed audits found no review, issue comment, review comment, or thread.
  GitHub-verified squash `6f3c0352420d39f9c4666101f7de3c23a52ac2d2`
  has exact reviewed tree `7fec531dd168a8ae96a074177d72c9589975264c`,
  sole parent the feature squash, a valid signature, and exact parsed DCO.
  This three-record closeout establishes the exact M65 selection base without
  requesting a hosted runner.

## M63 public release subordinate-output confinement - complete

- Base: exact clean synchronized M62 closeout
  `1cdc1b452cbe79c9e4f082acb4dd1205f4b3648f`, with tree
  `03abc8d3a45b568e98eebcd9a492e6f96ff71049` exactly matching the reviewed
  closeout candidate. GitHub reports a valid signature and parsed DCO trailer.
  Only `main` existed locally/remotely after pruning, with no open pull request,
  closeout run/check, or post-closeout `main` run.
- Gap: the real complete release smoke prints a success line before the public
  consumer's JSON. Nested smoke output could also prefix a stable failure, and
  numeric inequality admitted `False`, `0.0`, or custom comparison behavior as
  a process success status.
- Scope: both in-process subordinate types now redirect stdout and stderr to
  private text sinks. Success is exact built-in integer zero, checked without
  invoking comparison or truth hooks. Invalid validator/smoke status retains
  content-silent document/smoke failure; consumer payloads and codes are
  unchanged.
- Decision: RFC-0046 records one-document output ownership, exact status
  conformance, restoration on exception, and the single-thread boundary. There
  is no direct descriptor or arbitrary subprocess capture, thread-safe library
  claim, subprocess wrapper, cleanup, rollback, retry, workflow, dependency,
  lock, version, runtime API, release authority, tag, release, or publication.
- Development evidence: the initial 11-case M63 file failed ten assertions and
  passed its protected-surface guard in 0.46 seconds against unchanged M62
  production code. After the minimal correction, all ten non-documentation
  assertions pass with docs deselected in 0.69 seconds. The first focused static
  gate exposed a non-public pytest capture-result annotation; after replacing it
  with plain strings, both changed Python files are format clean, Ruff clean,
  and strict-Pyright clean. The complete documented contract passes all 11
  assertions in 0.24 seconds and strict docs build in 1.14 seconds. The first
  inherited architecture run passed 685 assertions and exposed three stale
  literal guards; the first correction passed 687 and exposed one remaining
  order guard. After strengthening all inherited guards, 688 architecture
  assertions pass in 4.81 seconds and the release-draft suite passes 56 tests
  with two expected skips in 5.15 seconds.
- Candidate evidence: each graphics-enabled CPython 3.12.13, 3.13.13, and
  3.14.5 suite passes 2,228 tests with 14 expected skips. The locked baseline
  was restored; ten real-wgpu tests, five-repeat base/graphics profiles,
  Clockwork Arena, Agent World Builder, and all four diagnostic benchmark
  artifact validators pass. Two pre-review builds reproduced a pure 272,051-
  byte wheel and 1,149,252-byte source archive; isolated-wheel and complete
  ten-artifact release smoke pass.
- Review: findings-first review found one evidence gap and no production defect:
  the contract did not directly prove validator stream restoration on
  exception. The added regression passes, taking the M63 file to 12 tests and
  architecture to 689 assertions. A subsequent chained command used a
  nonexistent release-draft test path after those passes; the corrected actual
  suite passes 56 tests with two skips. The retired metadata directory is
  absent, no automation-identity or credential patterns were found, protected
  workflows/dependencies/runtime source remain byte-unchanged, and artifact/
  native/backend boundaries remain intact.
- Final local candidate: the record-inclusive source gate passes 689
  architecture assertions, all 12 M63 assertions, 56 release-draft tests with
  two skips, strict docs, static analysis, and whitespace. Each supported
  graphics-enabled CPython suite passes 2,229 tests with 14 skips. Final
  renderer/profile/examples and diagnostic benchmarks pass. Two fresh builds
  reproduced a pure 272,051-byte wheel and 1,150,415-byte source archive;
  installed-wheel, ten-artifact release smoke, and archive inspection pass.
  This evidence record changes the source archive afterward, so exact commit-
  tree artifact identity remains delegated to the hosted gate.
- Hosted evidence: ready PR #141 exact head `8fe7518efb1855c69f3f093eba921721421072ce`
  passed run `31507526704` in exactly three Linux-first allocations. Linux
  `93832810911` passed in 7m07s before macOS `93835048148` and Windows
  `93835048154` began; they passed in 2m59s and 3m11s. Baseline passed 2,233
  tests; Ubuntu 3.13/3.14 and desktop 3.14 suites each passed 2,233 with one
  expected skip. Exact hosted wheel/sdist identities, installed-wheel smoke,
  complete release smoke, profiles, real-wgpu checks, and both vertical slices
  passed. Two delayed review audits were empty. GitHub-verified squash
  `e0f1dc683d5e38b69d01d342f843074470a8418a` has the exact reviewed tree, sole
  parent exact M62 closeout, and parsed DCO. The bounded integration record is
  locally validated with 689 architecture assertions, strict docs/static/
  whitespace gates, and reproducible artifact smoke.
- Integration evidence: ready four-document PR #142 exact head
  `88ec556325bfbb278232dbfafb546a066e266b63` passed run `31509382982` in one
  41-second Linux allocation; the desktop umbrella skipped with zero steps.
  Hosted formatting, Ruff, strict docs, all 689 architecture assertions,
  reproducible distribution, installed-wheel smoke, and complete release smoke
  passed. Two delayed review audits were empty. GitHub-verified squash
  `abc51243e5e4612f5e7f1ca20cb5eeedb6dc0a8a` has exact reviewed tree
  `86c4cbd8d24dfa3c0e81dc115d2765a273bfdb7c`, sole parent the feature squash,
  valid signature, and parsed DCO. This three-record closeout establishes the
  exact M64 base without requesting a hosted runner.

## M62 portable public release asset names - complete

- Base: exact clean synchronized M61 closeout
  `14f848c92021d54c9140e01b0333c0725c45145d`, with tree
  `0d62fdda4864c1b4f92083bbd59ee63afc6d38aa` exactly matching the reviewed
  closeout candidate. GitHub reports a valid signature and parsed DCO trailer.
  Only `main` existed locally/remotely after pruning, with no open pull request,
  closeout run/check, or post-closeout `main` run.
- Gap: the public-release plan grammar admitted 256-character basenames,
  trailing periods, classic Windows device stems with or without extensions,
  and case-only pairs. Those spellings do not preserve one portable child-file
  identity across supported hosts.
- Scope: plan parsing now admits at most 255 existing restricted ASCII
  characters, rejects a trailing period or case-insensitive Windows device
  stem, and tracks case-insensitive uniqueness. Violations retain stable
  content-silent `public_release.invalid_plan` before asset download and before
  creation of the asset output directory. Existing portable names are unchanged.
- Decision: RFC-0045 records the lexical portable policy, failure ordering, and
  nonclaim boundary. There is no filesystem probing, host-dependent reserved-
  name API, locale, normalization, rewriting, path resolution, race-free claim,
  cleanup, rollback, retry, workflow, dependency, lock, version, runtime API,
  release authority, tag, release, or publication.
- Development evidence: the initial 16-case M62 file failed 14 assertions and
  passed two in 0.51 seconds against unchanged production code. Every invalid
  name and case-only duplicate was accepted, the end-to-end existing-plan case
  reached an intentionally forbidden asset download, and the RFC was absent.
  The portable-name sample and protected-surface guard passed. After the parser-
  only correction, all 15 non-documentation assertions pass with the docs case
  deselected in 0.22 seconds; both changed Python files are formatted, Ruff
  clean, and strict-Pyright clean. The full documented M62 group passes 16
  assertions. A mistakenly parallel architecture/release-draft invocation
  caused one real stale M45 literal-guard failure plus one shared temporary-root
  setup error; after strengthening the guard and rerunning sequentially, all
  677 architecture assertions pass, while the independently completed release-
  draft run passes 56 tests with two platform-capability skips. Whole-tree
  formatting for 305 files, Ruff, strict Pyright, and strict docs pass. The
  complete graphics-enabled candidate passes 2,217 tests with 14 expected skips
  on each of CPython 3.12.13, 3.13.13, and 3.14.5. Ten real-wgpu tests, both
  five-repeat profiles, Clockwork Arena, Agent World Builder, and every M1-M4
  artifact validator pass. M1 observed one of two targets, M3 observed zero of
  two, and M4 observed its baseline target; those local measurements remain
  diagnostic only. Two confirmed-absent builds reproduced a pure 271,854-byte
  wheel and 1,141,325-byte source archive; isolated-wheel and complete ten-
  artifact smoke pass. The wheel has 94 entries and the source archive 490,
  with no native, WASM, bytecode, cache, site, or dist payload. Findings-first
  review identified the inherited README's stale M0-M59 completion boundary.
  A new assertion failed against it, then all 16 M62 assertions and strict docs
  passed after aligning the status to completed M61 and repairing the stale M61
  internal closeout sentence. The final post-review lock/static/docs gate,
  whitespace, protected-surface, credential, tool-identity, and Git-object
  audits pass. Two new builds reproduce a pure 271,887-byte wheel and
  1,142,219-byte source archive; isolated-wheel and ten-artifact release smoke
  pass, and the 94/490-entry archive inventory has no native, WASM, bytecode,
  cache, site, or dist payload.
- Hosted evidence: ready PR #138 exact head
  `3bb7539463e34859b5ef8a63d2ea4bc1ff4c2cb2` passed run `31501434063`
  in exactly three allocations. Linux job `93812142249` passed in 7m20s before
  macOS `93814459679` and Windows `93814459742` began; they passed in 3m11s and
  4m18s. Linux baseline passed 2,221 tests, while Ubuntu 3.13/3.14 and both
  desktop 3.14 suites passed 2,221 with one expected skip. All platforms passed
  ten real-wgpu tests, profiles, Clockwork Arena, and Agent World Builder.
  Hosted same-source builds reproduced a pure 271,874-byte wheel at
  `00c026e3800aa4ab4f46adc55bc91e21a0d09a9bfecf22a0b882a3b2349f306a`
  and 1,142,880-byte source distribution at
  `efe8f58254a38949d9ae3b170d4b8d6f369c55fe65fc6616d48011bf06b7bcde`;
  installed-wheel and ten-artifact release smoke passed. Two delayed audits
  found no comment, review, or thread. Head-pinned GitHub-verified squash
  `a96fac6b4fdd2eb3c0d65ede17f66cede2faa232` has tree
  `0bbacc706be88a4aab7ed13a444f1657db90fdb6` exactly equal to the reviewed
  head, sole parent exact M61 closeout, and parsed DCO. The feature branch is
  deleted locally/remotely; only `main` remained before the bounded integration
  record branch was created. Ready integration-record PR #139 exact head
  `5252987bc6b1da546f49f09b9358a2735e6b34f1` changed exactly four
  documentation paths and passed run `31503119877` in one 41-second Linux
  allocation. All 305 Python files were format clean, Ruff passed, strict docs
  built, all 677 documentation architecture assertions passed, and reproducible
  build plus installed-wheel and ten-artifact release smoke passed. The desktop
  umbrella `93818148618` skipped with zero steps. Two delayed audits found no
  comment, review, or thread. Head-pinned GitHub-verified squash
  `de6ead04124b889318b5ab854d25a6b5324d05aa` has tree
  `baa594eb17a548482b81ef11e868ce0d4175051b` exactly equal to the reviewed
  integration head, sole parent the feature squash, and parsed DCO. Both merged
  branches are deleted locally/remotely; only synchronized `main` remained
  before this exact three-file closeout branch was created.

## M61 public release candidate/output-root separation - complete

- Base: exact clean synchronized M60 closeout
  `a8fc787a7b04b4fe8ed3766167e58258aa62c8d6`, with tree
  `784bf3b82a3dfd51842edad622b3ae1dc0b78ea5` exactly matching the reviewed
  closeout candidate. GitHub reports a valid signature and parsed DCO trailer.
  Only `main` existed locally/remotely after pruning, with no open pull request,
  closeout run/check, or post-closeout `main` run.
- Gap: the verifier independently accepted an existing non-symlink candidate
  directory and runner output root but did not compare their resolved
  identities. If the output root equalled or resolved beneath the candidate,
  the fresh document, plan, or downloads could mutate the candidate before its
  validation.
- Scope: both validated roots now use strict `Path.resolve()`. Resolution
  failures preserve the existing content-silent candidate/temporary-directory
  codes. Equality or an output root beneath the candidate fails with stable
  `public_release.path_overlap`; the resolved paths become the context-owned
  roots. Filesystem-identity comparison across the output ancestry also rejects
  an equivalent alias whose resolved spelling differs on a case-insensitive
  filesystem; inspection failure maps content-silently to the temporary-root
  code. A separate candidate child of the output root remains valid because its
  sibling outputs do not enter the candidate.
- Decision: RFC-0044 records read-only candidate ownership, resolved-alias
  comparison, failure ordering, and the nonclaim boundary. This remains no
  race-free filesystem guarantee and adds no descriptor-confined or general
  filesystem sandbox, rollback, cleanup, retry, workflow, dependency, lock,
  version, runtime/API, release authority, tag, release, or publication.
- Development evidence: all five unsafe/inspection cases in the initial M61
  run reached an intentionally forbidden download path, the absent-RFC case
  failed, and the safe sibling/protected-surface assertions passed. After the
  focused implementation, all seven non-documentation assertions pass in 0.21
  seconds; both changed Python files are format clean, Ruff clean, and strict-
  Pyright clean. The first documentation-integrated run required an explicit
  `before validator` phrase; after correction, all eight M61 assertions pass in
  0.20 seconds and strict docs build. The first inherited-boundary command used
  a nonexistent test filename and collected nothing. Its corrected invocation
  passes 346 M45-M61/release-draft tests with two platform-capability skips in
  7.56 seconds. The unchanged 46-package lock and 45-package graphics
  environment pass whole-tree formatting for 304 files, Ruff, strict Pyright,
  all 656 architecture assertions, and strict docs. Complete graphics-enabled
  CPython 3.12.13, 3.13.13, and 3.14.5 suites each pass 2,196 tests with 14
  expected skips. Ten real-wgpu tests, both five-repeat profiles, Clockwork
  Arena, Agent World Builder, and every M1-M4 validator pass. M1 observed one
  of two targets, M3 observed zero of two, and M4 observed its baseline target;
  target misses are retained as facts. Two pre-record builds reproduce a pure
  271,671-byte wheel and 1,132,009-byte source distribution; isolated-wheel and
  complete ten-artifact release smoke pass. Archive review finds 94 wheel and
  488 source entries with no native/WASM wheel member or cache output. Added
  RuntimeError and resolved-root-use proof points bring the final focused M61
  group to 11 passing assertions with static checks clean. Final record-
  inclusive lock/static/docs and 659 architecture assertions pass. The final
  graphics-enabled CPython 3.12 candidate passes 2,199 tests with 14 expected
  skips, and all 11 final M61 assertions pass on CPython 3.13 and 3.14. Exact
  pre-review builds reproduce a pure 271,671-byte wheel and 1,132,688-byte
  source distribution; isolated-wheel and complete release smoke pass. The
  wheel has 94 entries, the source distribution has 488, and no native/WASM
  wheel member or cache/build output is present. Protected workflow, metadata,
  lock, and runtime package surfaces are unchanged. Exact immutable final
  artifact identities are delegated to commit/PR evidence because this record
  is part of the source archive. Ready PR #135 initial head
  `e17476380d979e2bec891db9fdf9a8523734e8b5` passed run `31494364000` in
  exactly three Linux-first jobs: Linux passed in 7m09s before macOS and Windows
  began, and they passed in 3m22s and 4m11s. Every complete hosted suite passed
  2,203 tests with one expected skip outside the baseline; all platforms passed
  ten real-graphics tests and both vertical slices. The first review audit then
  identified that `Path.resolve()` alone does not promise canonical case on a
  case-insensitive POSIX filesystem. Two test-first identity regressions and
  the expanded documentation contract failed against the hosted head. The
  correction compares every resolved output ancestor to the candidate with
  `Path.samefile()` and fails identity-inspection errors content-silently. All
  12 corrected non-documentation assertions pass in 0.23 seconds; after aligned
  RFC/public documentation, all 13 M61 assertions pass in 0.23 seconds with
  focused formatting, Ruff, strict Pyright, and strict docs clean. The complete
  correction-inclusive gate passes 304-file formatting, Ruff, strict Pyright,
  661 architecture assertions, strict docs, and 2,201 tests with 14 expected
  skips on CPython 3.12.13 in 113.87 seconds, CPython 3.13.13 in 110.05
  seconds, and CPython 3.14.5 in 114.92 seconds. Exact corrected-head hosted
  qualification passed ready PR #135 run `31496532379` in exactly three Linux-
  first jobs. Linux `93795541158` passed in 7m18s before macOS `93797741480`
  and Windows `93797741693` began; they passed in 3m18s and 4m05s. The Linux
  baseline and every compatibility suite passed 2,205 tests, with one expected
  skip outside the baseline. Hosted artifacts reproduced a 271,706-byte wheel
  at `88e5b70b34896ed136ee80e268adec8e60c439c9ad3e02d38493fc3933ce27ad`
  and 1,135,916-byte source distribution at
  `db036d8e628c5ab061ae38bcf07f3635f06c98096b86fbe9b5444644f31ded5c`;
  installed-wheel and complete release smoke passed. Two delayed audits found
  no new actionable review item: the sole P1 thread was addressed and resolved.
  Head-pinned GitHub-verified squash
  `7feded4ed2e37157b87a7f3bb733caf96805187e` has the exact reviewed tree
  `3ae8059dc5a4f61a8a3b31d245b20f0373e0ffe4`, sole parent exact M60 closeout,
  and a parsed DCO trailer. The feature branch is deleted locally/remotely;
  there is no open feature PR or post-feature `main` run. Ready integration-
  record PR #136 exact head `d80292ab4be734093bed52d0b0435da4d8b164e6`
  changed exactly four documentation paths and passed run `31497995187` in one
  38-second Linux allocation. Formatting, Ruff, strict docs, 661 documentation-
  architecture assertions, distribution build, installed-wheel smoke, staging,
  and release smoke passed. The desktop umbrella skipped with zero steps. Two
  delayed audits found no comment, review, or thread. GitHub-verified squash
  `9d1c4d4f967e97c7c77cf3b95d82c2d57367162e` has the exact reviewed tree
  `8da574c0f2642369a725e6eb32d3983176e38dac`, sole parent the feature squash,
  and a parsed DCO trailer. Zero-allocation closeout PR #137 was then squash-
  merged as `14f848c92021d54c9140e01b0333c0725c45145d`; both working branches were
  deleted locally/remotely, no open PR or post-closeout `main` run exists, and
  M61 is complete.

## M60 public release filesystem collision conformance - complete

- Base: exact clean synchronized M59 closeout
  `9ba74e55b5c47d5f0bd030b53ad6a35a361c5735`, with tree
  `426ee37f3a3c7b19cab70d9f20b4be590c2cd4b5` exactly matching the reviewed
  closeout candidate. GitHub reports a valid signature and standalone DCO.
  Only `main` existed locally/remotely after pruning, with no open pull request,
  closeout run/check, or post-closeout `main` run.
- Gap: the portable public-release verifier used following `Path.exists()`
  preflight for its fresh release document, output directory, plan, target, and
  partial paths. A dangling link was therefore reported absent and could allow
  network or validator work to begin before the existing exclusive writer or
  hard-link publisher rejected the collision.
- Scope: a private helper now uses final-entry `Path.lstat()`. Files,
  directories, live links, dangling links, and other existing directory entries
  block fresh output before side effects. Non-absence inspection failures map
  to stable, content-silent output/plan failures. A late output-directory
  `FileExistsError` maps to `public_release.output_exists`.
- Ownership: direct and partial file creation remains `x`/`xb` exclusive, and
  asset publication remains hard-link creation followed by owned-partial
  removal. These retain no clobber behavior after preflight.
- Decision: accepted RFC-0043 records the collision, error, ordering,
  ownership, and nonclaim boundary. This is no race-free filesystem guarantee;
  there is no descriptor-confined sandbox, rollback, cleanup, retry, workflow,
  dependency, lock, version, runtime/API, release-authority, tag, release, or
  publication change. Pull-request fixtures are not a real public release
  observation.
- Development evidence: the inherited M45-M58/release-draft boundary first
  passed 317 tests with two platform-capability skips. All eight initial M60
  assertions then failed against unchanged code: six reached intentionally
  forbidden download/connection paths, one scope fixture held a stale workflow
  hash, and the documentation contract named the intentionally absent RFC. The
  fixture hash was corrected. The implementation then passed seven behavior
  and scope assertions; documentation initially missed one exact phrase and
  passed after correction. A late-directory-collision regression and a
  content-silent fresh-plan inspection regression were added, bringing the M60
  group to ten passing assertions. Focused formatting, Ruff, and strict Pyright
  are clean.
- Compatibility corrections: the first complete architecture run found two
  stale inherited contracts. M46 required literal `plan.exists()` and now
  requires the stronger non-following plan check and stable failure code. M59
  required its disclosure wording in maintainer/public docs; that historical
  boundary was restored without weakening the new M60 contract. The corrected
  architecture suite passed 647 assertions before the final M60 test addition;
  the record-inclusive suite passes 648 assertions.
- Broad local evidence: before the final test addition, graphics-enabled
  CPython 3.12.13, 3.13.13, and 3.14.5 complete suites each passed 2,187 tests
  with 14 expected skips. Ten real-wgpu tests, both five-repeat M7 profiles,
  Clockwork Arena, Agent World Builder, and every M1-M4 benchmark validator
  pass. M1 observed one of two targets; M3 observed one of two targets; M4
  observed its baseline target. Target misses remain recorded facts. The final
  record-inclusive CPython 3.12 suite passes 2,188 tests with 14 expected skips;
  the final ten M60 assertions pass on CPython 3.13 and 3.14.
- Pre-record distributions: two builds reproduced a 271,507-byte pure wheel at
  `03115989c614f5627ece94d4d794364510f0b88e1dcb65a5ddec2489a23e83a6`
  and a 1,121,988-byte source distribution at
  `ed6904e06a882742017a63e26d4b23a8b5beb2a6a9a9a96778b3c7edd228b2fc`.
  Isolated-wheel smoke and the complete ten-artifact release smoke pass. The
  record-inclusive candidate also reproduces twice, passes both smokes, contains
  94 pure-wheel and 486 source-distribution entries, and contains no native or
  WASM wheel member. Exact immutable candidate hashes are captured with the
  commit/PR evidence rather than self-embedded into the source distribution.
- Hosted evidence: ready PR #132 exact head
  `836c1e14bbfe0e9bb94dbe1fc84df600279e0b23` passed run `31488972656` in
  exactly three Linux-first allocations. Linux job `93770741704` passed in
  7m25s before macOS job `93772531511` and Windows job `93772531611` began;
  they passed in 2m28s and 3m17s. Linux baseline passed 2,192 tests; Ubuntu
  CPython 3.13/3.14 and both desktop CPython 3.14 suites passed 2,192 tests with
  one expected skip. All platforms passed ten real-graphics tests, valid
  three-workload graphics profiles, Clockwork Arena, and Agent World Builder.
- Hosted artifacts: same-source reproducibility produced a pure 271,493-byte
  wheel at
  `ed79ae64bbda70b105fea3eaf61fedfa175998ea55191a7127d764063579f784`
  and a 1,125,477-byte source distribution at
  `462b6659990f222fe2c06c1deca5e124fdc897ec08d4d75cde3020f919ba2aab`.
  Installed-wheel and complete ten-artifact release smoke passed.
- Integration: two audits found PR #132 ready, exact-head/exact-base,
  `MERGEABLE/CLEAN`, with exactly three successful checks and no issue comment,
  review comment, review, or thread. Head-pinned GitHub-verified squash
  `8967bd8cfc11f1b29caadbf01da9255bd6eb4584` has tree
  `e17d11565f30e58b6eb705926702e257026f9b3b` exactly equal to reviewed head
  `836c1e14bbfe0e9bb94dbe1fc84df600279e0b23`, and sole parent exact M59
  closeout `9ba74e55b5c47d5f0bd030b53ad6a35a361c5735`. The source commit has the
  required DCO trailer and remains attached to PR #132. The generated squash
  body retained literal escaped newline text before its displayed sign-off, so
  this record does not claim that generated commit has a parsed trailer and
  does not rewrite public history. The feature branch is deleted locally and
  remotely. Synchronized `main` has no post-merge run or open pull request.
  No tag, release, publication, or real public release observation exists.
- Integration record: exact four-path documentation head
  `f4a41d848a9e9bfa85da2c34d09e705ad7493c87` passed ready PR #133 run
  `31490571527` in one 43-second Linux allocation. All 303 Python files were
  format clean, Ruff passed, strict docs built in 1.53 seconds, all 648
  documentation architecture assertions passed in 8.51 seconds, same-source
  distributions reproduced, and installed-wheel plus complete release smoke
  passed. Desktop umbrella `93776026071` skipped with zero steps and no runner
  allocation. The exact-head wheel was 271,493 bytes at
  `ed79ae64bbda70b105fea3eaf61fedfa175998ea55191a7127d764063579f784`;
  the 1,127,269-byte source distribution was
  `02d7bc6c928068e4c562b3674cfd76fbec204ab0c31cc33933d1acf0254d2a6a`.
- Integration-record merge: two delayed audits found exact head/base,
  `MERGEABLE/CLEAN`, one successful Linux check, one zero-step skipped
  umbrella, and no issue comment, review comment, review, or thread. Head-
  pinned GitHub-verified squash
  `6861198cf32d04f1e802525c2327335ca1c8be86` has tree
  `280d9e41e4f04d73f99dc5d324ede72f8fc7a472` exactly equal to the reviewed
  record head, sole parent feature squash
  `8967bd8cfc11f1b29caadbf01da9255bd6eb4584`, and a parsed DCO trailer. No
  post-integration `main` run was allocated; both M60 working branches are
  deleted locally/remotely, and no open pull request exists. The exact three-
  file `.project/**` closeout must allocate zero hosted runs or checks.

## M59 repository metadata hygiene - complete

- Base: exact clean synchronized M58 closeout
  `d4487565d4fda57ec05437dfcadc687d2507dafa`, with only `main` present and no
  open pull request, tag, release, closeout run/check, or post-closeout `main`
  run.
- Scope: current tracked and non-ignored working-tree text uses tool-neutral
  role, purpose, product, and milestone names. Current project records replace
  obsolete tooling-specific labels with descriptive redactions while exact
  commit, tree, PR, workflow, artifact, test, and timing evidence remains.
- Guard: one architecture test owns the encoded retired-marker set, scans
  tracked plus non-ignored working-tree text, and separately proves retired
  root control paths remain absent. Three older duplicated absence loops now
  retain only their milestone-specific neutral-convention assertions.
- Fixture: the persistent-command schema test uses a neutral client identity;
  command behavior, canonical bytes, public protocols, and runtime source are
  unchanged.
- Decision: accepted RFC-0042 records the current-tree convention, descriptive
  redaction, central enforcement, product-terminology distinction, immutable-
  history boundary, and nonclaims.
- Boundary: no Git-history rewrite, attribution/DCO change, Git-object
  deletion, runtime source, product-facing agent terminology, public API,
  protocol, workflow, dependency, lock, version, tag, release, publication, or
  release-authority change. The guard does not claim forensic erasure from
  immutable history, clones, forks, logs, external databases, or caches.
- Development evidence: the initial tracked-tree scan found 107 matching lines
  across the two current project-record files and four tests. Against the
  unchanged tree, the new guard failed one assertion and passed its absent-root
  control in 0.28 seconds, identifying all six affected files. After the
  implementation, 56 focused inherited and new assertions passed in 0.70
  seconds and focused strict Pyright reported zero diagnostics. The new test
  initially required one formatter rewrite and one import-order correction;
  both were applied. A subsequent three-assertion documentation gate passed
  both hygiene checks and failed only on the intentionally absent M59 contract.
  The documented contract then required one README wording correction before
  all 57 selected assertions passed. Whole-tree lock, synchronization,
  formatting, Ruff, strict Pyright, 636 architecture assertions, and strict
  docs pass. Complete graphics-enabled CPython 3.12-3.14 suites each pass
  2,176 tests with 14 expected skips. Ten real-wgpu tests, both five-repeat
  profiles, both vertical slices, and every documented M1-M4 benchmark
  validator pass. Two pre-record builds reproduced the pure wheel and source
  distribution; isolated-wheel and complete release smoke pass. Findings-first
  review found and corrected two uppercase legacy instruction-name remnants,
  expanded the marker set to cover direct automation-attribution wording, and
  hardened the guard to inspect path names and symlink targets without
  following links outside the repository. All four final focused assertions
  pass with formatting, Ruff, and strict Pyright clean. The record-inclusive
  candidate passes lock/sync, whole-tree formatting, Ruff, strict Pyright, 637
  architecture assertions, strict docs, reproducible pure distributions,
  isolated-wheel smoke, complete release smoke, and archive-content review.
  Final evidence-inclusive review was clean before hosted qualification.
- Initial hosted evidence: exact head
  `3d7329311d326692dd725024d312b73bb420ef16` passed run `31482750494` in
  exactly three Linux-first allocations. Linux job `93751196748` passed in
  7m27s before macOS `93752915784` and Windows `93752915830` began; they
  passed in 2m21s and 4m20s. Linux baseline and every compatibility suite
  passed 2,181 tests, with one expected skip outside the baseline. Every
  platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and
  Agent World Builder. Hosted reproducibility produced a pure 271,281-byte
  wheel at
  `90d0e8daed42c217ae3fd5795feea821744c2e154f361112dbb5c6135998e28a`
  and a 1,114,755-byte source distribution at
  `1801d4c777f60c77366cabbb52eca38ca141253014387b5b3ffd4b10671ea124`;
  installed-wheel and complete release smoke passed.
- Review correction: one valid P2 found that `Path.exists()` follows a
  dangling retired root symlink and may report the forbidden directory entry
  absent. The platform-independent regression failed tests-first. The guard
  now treats ordinary existence or symlink identity as a violation. After
  replacing initially untyped monkeypatch lambdas rejected by strict Pyright,
  all five focused assertions pass in 0.28 seconds with format, Ruff, and
  strict Pyright clean. The corrected whole-tree candidate passes lock,
  formatting, Ruff, strict Pyright, 638 architecture assertions, strict docs,
  and whitespace. The initial hosted pass was not sufficient to merge.
- Corrected hosted evidence: exact head
  `28e80e66eb16656a998353627ef78a8fe6e4c80b` passed run `31484028669` in
  exactly three Linux-first allocations. Linux job `93755205753` passed in
  6m05s before macOS `93756589084` and Windows `93756589057` began; they
  passed in 2m53s and 4m08s. Linux baseline and every compatibility suite
  passed 2,182 tests, with one expected skip outside the baseline. Every
  platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and
  Agent World Builder.
- Corrected hosted artifacts: exact-head reproducibility produced a pure
  271,281-byte wheel at
  `90d0e8daed42c217ae3fd5795feea821744c2e154f361112dbb5c6135998e28a`
  and a 1,116,015-byte source distribution at
  `5650d9a3df594799e09969f305419829b4345d6e85b8682b130b78fe926be987`;
  installed-wheel and complete ten-artifact release smoke passed.
- Integration: the valid P2 was answered with the correction evidence and its
  sole thread resolved. Two delayed audits found exact corrected head/base,
  `MERGEABLE/CLEAN`, exactly three successful checks, zero issue comments, and
  no unresolved or later review activity. Head-pinned squash
  `f12f65ab7c1f8426b0232bb4b414e48276bbad56` has tree
  `759107195ba7094fb78cbc25b62a5d6011dd637d` exactly equal to the corrected
  reviewed head, sole parent M58 closeout
  `d4487565d4fda57ec05437dfcadc687d2507dafa`, a valid GitHub signature, and
  standalone DCO. The feature branch is deleted locally/remotely. Synchronized
  `main` has no post-merge run or non-main remote branch. Its local integration-
  record gate passes exact four-file scope,
  lock/sync, whole-tree formatting, Ruff, strict Pyright, 638 architecture
  assertions, strict docs, reproducible pure distributions, isolated-wheel
  smoke, complete release smoke, and whitespace.
- Integration record: exact head
  `f142ceae1381c5c8c6cb15001229cfd4679ff028` passed run `31485465637` in one
  42-second Linux allocation. All 302 Python files were format clean, Ruff and
  strict docs passed, 638 documentation architecture assertions passed,
  reproducible distributions plus installed-wheel and complete release smoke
  passed, and desktop umbrella `93759917789` skipped with no runner and zero
  steps. The exact-head 271,281-byte wheel was
  `90d0e8daed42c217ae3fd5795feea821744c2e154f361112dbb5c6135998e28a`;
  the 1,117,495-byte source distribution was
  `b8c4a21345ff809e7bb078ded52daae5993f863e6f54379345cc0683a92f86be`.
  Two delayed audits found no comment, review, or thread. Head-pinned GitHub-
  verified squash `f6b734878738ca6408afeabb793c5cd591c0d607` has tree
  `da5e3b4404a9385990685467d920806b290de282` exactly equal to the reviewed
  record head, sole parent feature squash
  `f12f65ab7c1f8426b0232bb4b414e48276bbad56`, valid signature, and standalone
  DCO. Both M59 working branches are deleted locally/remotely. No post-
  integration `main` run or non-main remote branch exists. The exact three-
  file `.project/**` closeout must allocate zero hosted runs or checks.

## M58 public release transport-cleanup conformance - complete

- Base: exact clean synchronized M57 closeout
  `26826822547d6d8df6ce1bfc05d8cf728a32d505`, with only `main` present and no
  open pull request, tag, release, closeout run/check, or post-closeout `main`
  run.
- Scope: every obtained response receives one close attempt before its created
  connection receives one close attempt. Both attempts occur if response close
  fails. Active request, protocol, validation, output, and control-flow
  failures remain primary. Cleanup-only ordinary failures use stable,
  content-silent `public_release.request_failed`; cleanup control signals remain
  unwrapped.
- Ordering: redirect continuation and separate asset partial publication occur
  only after successful response/connection cleanup. The release-document
  direct target and partial bytes retain their existing no-rollback behavior.
- Decision: accepted RFC-0041 records public close-method ownership, failure
  priority, ordering, and the no-rollback/non-claim boundary.
- Boundary: no retry, private response/socket state, raw parser, alternate
  client, pooling, cache, proxy, DNS preflight, network sandbox, workflow,
  runner allocation, action, permission, trigger, credential, release mutation,
  dependency, lock, version, runtime package, public API, or release authority.
  Fixture and pull-request evidence are not a real public release observation.
- Development evidence: the clean M47-M57 baseline passed 243 assertions.
  Official Python 3.14 documentation review established the public close
  surface. Against unchanged production code, all nine focused behavior and
  boundary assertions failed as expected. After correcting six Ruff findings
  and seven Pyright findings in the test harness, the implementation passes all
  ten focused behavior/boundary/documentation assertions with Ruff and strict
  Pyright clean. All 253 inherited M47-M58 assertions and strict docs pass.
  Whole-tree lock, formatting, Ruff, strict Pyright, 631 architecture
  assertions, and strict docs pass. Complete graphics-enabled CPython
  3.12-3.14 suites each pass 2,171 tests with 14 expected skips. Ten real-wgpu
  tests, both five-repeat profiles, both vertical slices, and every documented
  M1-M4 benchmark validator pass. Findings-first review then demonstrated that
  `close_error or error` invoked attacker-defined truthiness while selecting
  the first cleanup failure. The regression failed tests-first; explicit
  identity selection corrects it. All 11 focused M58, 254 inherited M47-M58,
  and 632 architecture assertions now pass with static/docs clean. Corrected
  complete graphics-enabled CPython 3.12-3.14 suites each pass 2,172 tests with
  14 expected skips. Corrected real-wgpu, both five-repeat profiles, both
  vertical slices, and every documented M1-M4 benchmark validator pass. A
  second findings-first regression then proved ambient `sys.exception()` could
  suppress cleanup failure when a caller was handling an unrelated exception.
  An explicit exchange-local primary-failure flag corrects the defect. The
  final candidate passes all 12 focused M58, 255 inherited M47-M58, and 633
  architecture assertions; whole-tree static/docs; graphics-enabled complete
  suites on CPython 3.12-3.14 with 2,173 passes and 14 expected skips each; ten
  real-wgpu tests; both five-repeat profiles; both vertical slices; and every
  documented M1-M4 benchmark validator. Two final-record builds reproduce the
  pure wheel and source distribution; isolated-wheel and complete release
  smoke pass. Findings-first scope, archive, credential, identity, history,
  and integrity review found no actionable M58 issue. Final record-inclusive
  lock/static/633-assertion/docs/integrity validation passes.
- Hosted evidence: exact head
  `8bd11f0ab6575edee6a5e7b5c78e36af59e55088` passed run `31478254138` in
  exactly three Linux-first allocations. Linux job `93736984444` passed in
  7m48s before macOS `93738860983` and Windows `93738860996` began; they
  passed in 2m00s and 4m01s. Linux baseline passed 2,177 tests; Ubuntu CPython
  3.13/3.14 and both desktop CPython 3.14 suites passed 2,177 tests with one
  expected skip. Every platform passed ten real-graphics tests, profile smoke,
  Clockwork Arena, and Agent World Builder.
- Hosted artifacts: exact-head reproducibility produced a pure 271,274-byte
  wheel at
  `04147c9b56fa5caf3c012172c043e4f0d1580257a0be513e8a274d0fe60d0f98`
  and a 1,108,291-byte source distribution at
  `30f98c24226d4cc588f122d0623d13a6e575e5abc8396c2a428cf22509134500`;
  installed-wheel and complete ten-artifact release smoke passed.
- Integration: two delayed audits found no issue comment, review comment,
  review, or thread. PR #126 was ready, `MERGEABLE/CLEAN`, exact-head/exact-
  base, and had exactly three successful checks. Head-pinned squash
  `17ea7354c80b9d140350b88cd0ae3e615f700e45` has tree
  `feea8788e3a1c0e34505be6e752aa7d0e721b693` exactly equal to the reviewed
  head, sole parent M57 closeout
  `26826822547d6d8df6ce1bfc05d8cf728a32d505`, a valid GitHub signature, and
  standalone DCO. The feature branch is deleted locally/remotely. Synchronized
  `main` has no post-merge run or non-main remote branch.
- Integration record: exact head
  `4a72ae994714a4c2040547c568c5d625ee4a7ab9` passed run `31479930394` in one
  40-second Linux allocation. All 301 Python files were format clean, Ruff and
  strict docs passed, 633 documentation architecture assertions passed,
  reproducible distributions plus installed-wheel and complete release smoke
  passed, and desktop umbrella `93742463489` skipped with no runner and zero
  steps. The exact-head 271,274-byte wheel was
  `04147c9b56fa5caf3c012172c043e4f0d1580257a0be513e8a274d0fe60d0f98`;
  the 1,109,741-byte source distribution was
  `bbe2929eefcc98486065667902b36c8100b93cdf2c623d66d9e8888c20348257`.
  Two delayed audits found no comment, review, or thread. Head-pinned GitHub-
  verified squash `26ec103a2ff3da55c4f2c4a8dca506f92ca3195e` has tree
  `ebff30df07c5797d3f85956ea9bb3a95ba833e66` exactly equal to the reviewed
  record head, sole parent feature squash
  `17ea7354c80b9d140350b88cd0ae3e615f700e45`, valid signature, and standalone
  DCO. Both M58 working branches are deleted locally/remotely. No post-
  integration `main` run or non-main remote branch exists. The exact three-
  file `.project/**` closeout must allocate zero hosted runs or checks.

## M57 public release response-body conformance - complete

- Base: exact clean synchronized M56 closeout
  `187cbfb1c857e62594e49d1cf8e7591024aff8c9`, with only `main` present and no
  open pull request, tag, release, or post-closeout `main` run.
- Scope: after M55 framing and M56 status/redirect checks, every successful
  response-body read returns immutable bytes no larger than the requested
  amount before EOF handling, accounting, or output. Any valid
  `Content-Length` must equal the total streamed octets for the release
  document and every successful final asset response. Pre-known asset sizes
  remain independently enforced.
- Failure: malformed block shapes and supported read/access failures use stable
  content-silent `public_release.request_failed`; declared-versus-streamed
  disagreement uses `public_release.size_mismatch`. Supported causes remain
  chained and existing timeout/transport/output/byte-limit/artifact ordering is
  unchanged.
- Boundary: no private response/socket state, raw HTTP/chunk parser, content
  decoder, alternate client, new required header, cleanup, retry, proxy, DNS
  preflight, network sandbox, workflow, allocation, dependency, package,
  runtime API, or release authority. There is no general completeness claim
  for an unframed close-delimited body and no real release observation.
- Decision: accepted RFC-0040 records the exact block-shape, requested-amount,
  declared-length, failure, ownership, and non-claim boundaries.
- Development evidence: the clean M47-M56 baseline passed 226 assertions.
  Official Python 3.14 and RFC 9112 review defined the binary-read and declared-
  length boundary. The first tests-first run exposed intended failures but had
  one invalid exception-class comparison because a helper reloaded the
  verifier. The corrected unchanged-verifier run failed 12 cases and passed
  two controls. Focused format, Ruff, and strict Pyright pass; all 14 initial
  M57 behavior assertions and all 240 inherited M47-M57 behavior assertions
  passed. One explicit `no alternate client` wording mismatch was corrected;
  all 242 focused implementation, compatibility, boundary, and documentation
  assertions and strict docs then passed. Findings-first review reproduced an
  unwrapped exception from a hostile bytes subclass: the new regression failed
  while 16 controls passed. Requiring exact built-in bytes closes that gap; all
  243 focused assertions now pass. All 300 Python files are format clean; Ruff
  and strict Pyright report zero findings; all 621 architecture assertions and
  strict docs pass. Complete graphics-enabled CPython 3.12-3.14 suites each
  pass 2,161 tests with 14 expected skips. Ten real-wgpu tests, three-repeat
  base/graphics profiles, Clockwork Arena, Agent World Builder, and every
  documented M1-M4 benchmark validator pass. Two pre-record builds reproduce
  byte-for-byte; installed-wheel and complete release smoke pass. Findings-
  first scope, archive, credential, identity, history, and integrity review
  reports no remaining actionable issue. Final record-inclusive static,
  documentation, reproducible-build, installed-wheel, and complete release-
  smoke gates pass.
- Hosted evidence: exact head
  `f7347965d7e9a78218fa08a34f76aed7d32ba67d` passed run `31332655171` in
  exactly three Linux-first allocations. Linux job `93293248918` passed in
  5m37s before macOS `93293864546` and Windows `93293864554` began; they passed
  in 1m51s and 3m48s. Linux baseline passed 2,165 tests; Ubuntu CPython
  3.13/3.14 and both desktop CPython 3.14 suites passed 2,165 tests with one
  expected skip. Every platform passed ten real-graphics tests, profile smoke,
  Clockwork Arena, and Agent World Builder.
- Hosted artifacts: exact-head reproducibility produced a pure 271,119-byte
  wheel at
  `a24b3d068c351370dca59d320a15dc8148ea64bfbcf6f8540591c4aeed96be61`
  and a 1,099,375-byte source distribution at
  `61add34b6732f399d772a556bf59d06816c30c794f1bd1c6a0d09905f2645602`;
  installed-wheel and complete release smoke passed.
- Integration: two delayed audits found no issue comment, review comment,
  review, or thread. PR #123 was ready, `MERGEABLE/CLEAN`, exact-head/exact-
  base, and had exactly three successful checks. Head-pinned squash
  `800050c74530d74a72338b5d444ee4751c5ad155` has tree
  `44b379cdcc510ee55bbaf35dce0bc826ffadb3ab` exactly equal to the reviewed
  head, sole parent M56 closeout
  `187cbfb1c857e62594e49d1cf8e7591024aff8c9`, a valid GitHub signature, and
  standalone DCO. The feature branch is deleted locally/remotely. Synchronized
  `main` has no post-merge run, open pull request, non-main remote branch, tag,
  or release.
- Integration record: exact head
  `b959cad56d0c9e9b3b34d02d313ce4a6b67a9fa9` passed run `31333440409` in one
  36-second Linux allocation. All 300 Python files were format clean, Ruff and
  strict docs passed, 621 documentation architecture assertions passed,
  reproducible distributions plus installed-wheel and complete release smoke
  passed, and desktop umbrella `93295290611` skipped with zero steps. The exact-
  head 271,119-byte wheel was
  `a24b3d068c351370dca59d320a15dc8148ea64bfbcf6f8540591c4aeed96be61`;
  the 1,100,675-byte source distribution was
  `b1c10ecfd5b3dedcf2cf2bf0a25f5277d1d40f76ef3da4e79292810a80a6c603`.
  Two delayed audits found no comment, review, or thread. Head-pinned GitHub-
  verified squash `f28d5ee6e9b1e3d65b1ff47c4574e8525cb6c85e` has tree
  `f8dcbfab5044a58bcfe9e1f0600ac82661d1dc8a` exactly equal to the reviewed
  record head, sole parent feature squash
  `800050c74530d74a72338b5d444ee4751c5ad155`, valid signature, and standalone
  DCO. Both M57 working branches are deleted locally/remotely. No post-
  integration `main` run, open pull request, non-main remote branch, tag, or
  release exists. The exact three-file `.project/**` closeout must allocate
  zero hosted runs or checks.

## M56 public release status and redirect-reference conformance - complete

- Base: exact clean synchronized M55 closeout
  `e7f700454adf1c11c80cb1ba684ed3318f7876e4`, with only `main` present and no
  open pull request, tag, release, or post-closeout `main` run.
- Scope: after M55 framing and before comparison, redirect resolution, or body
  use, require a non-boolean integer status from 100 through 599. A followed
  `302` must expose exactly one Location field through the documented header-
  pair list. Its value is one 1-to-8,000-octet ASCII URI-reference using RFC
  3986 characters and complete percent escapes. Bracket delimiters are valid
  only inside the parsed authority, not its path, query, or fragment.
  Revalidate the resolved HTTPS URL before another request.
- Failure: malformed, unavailable, unsupported, out-of-range, and raising
  status uses stable, content-silent `public_release.request_failed`. Missing,
  duplicate, malformed, oversized, and raising Location metadata or invalid
  resolution uses `public_release.redirect_failed`; a supported local cause is
  chained.
- Boundary: relative and cross-host absolute references remain supported, with
  M49-M55 peer, TLS, framing, deadline, size, and exact-byte checks repeated on
  every hop. No host allowlist, private response state, raw HTTP/URI parser,
  alternate client, proxy, DNS preflight, network sandbox, workflow,
  allocation, dependency, package, runtime API, release authority, or general
  SSRF claim. Fixture/PR evidence is not a real public release observation.
- Decision: accepted RFC-0039 records the exact status, header occurrence,
  syntax, resolution, failure, ownership, and non-claim boundaries.
- Development evidence: the clean M47-M55 baseline passed 189 assertions.
  Official Python 3.14 and RFC 9110/3986 review defined the public metadata and
  URI boundary. A tests-first probe failed 25 of 31 executed behavior cases and
  confirmed the status-shape, raw-failure, joined-Location, and permissive-
  recovery gaps. The implementation passes all 34 M56 behavior, boundary, and
  documentation cases; all 223 focused M47-M56 assertions pass together. All
  299 Python files are format clean; Ruff and strict Pyright report zero
  findings; all 601 architecture assertions and strict docs pass. Complete
  graphics-enabled CPython 3.12-3.14 suites each pass 2,141 tests with 14
  expected skips. Real-wgpu, profiles, both vertical slices, every documented
  benchmark validator, reproducible builds, installed-wheel smoke, and
  complete release smoke pass.
- Review: findings-first correctness, failure-ordering, scope, documentation,
  archive, credential, identity, history, and integrity review corrected one
  RFC consequence that could imply a general URI syntax validator. All 223
  focused assertions and strict docs passed after the narrower wording; no
  local issue was found at that point. Initial exact head
  `86b2d4eaf404b15100bfc7d083fe119adc3e9f11` then passed hosted run
  `31328303442` in exactly three Linux-first allocations. Delayed review found
  a valid P2: the global character set allowed bracket delimiters in path and
  query components even though RFC 3986 reserves them for IP-literal authority
  syntax. Two reviewer-derived regressions failed tests-first while 14 controls
  passed. The component-aware correction now rejects path/query/fragment
  brackets while retaining a valid bracketed IPv6 authority; its targeted 16-
  case gate passes. All 226 focused M47-M56 assertions, 604 architecture
  assertions, strict static/docs gates, and complete graphics-enabled CPython
  3.12-3.14 suites pass on the correction. Real-wgpu, profiles, both vertical
  slices, reproducible builds, isolated-wheel smoke, complete release smoke,
  archive/scope/integrity checks, and repeat findings-first review pass.
- Local status: the final exact-tree lock and 45-package graphics environment
  check; formatting; Ruff; strict Pyright; 601 architecture assertions; strict
  docs; whitespace; and full Git-object gates pass. Two fresh builds reproduce
  the pure wheel and source distribution; isolated-wheel and complete ten-
  artifact release smoke passed for the initial head. Corrected pre-record
  reproducibility and smokes also pass. The final corrected record-inclusive
  lock/static/604-assertion/docs/integrity gate, two-build reproducibility,
  isolated-wheel smoke, and complete release smoke pass.
- Hosted evidence: corrected exact head
  `35b94a42b10cbd8f75048d3200e95a4aca81fa5d` passed run `31329613114` in
  exactly three Linux-first allocations. Linux job `93285627958` passed in
  7m22s before macOS `93286456923` and Windows `93286456914` began; they passed
  in 2m19s and 4m00s. Linux baseline passed 2,148 tests; Ubuntu CPython
  3.13/3.14 and both desktop CPython 3.14 suites passed 2,148 tests with one
  expected skip. Every platform passed ten real-graphics tests, profile smoke,
  Clockwork Arena, and Agent World Builder.
- Hosted artifacts: exact corrected-head reproducibility produced a pure
  270,869-byte wheel at
  `c09dfe4f799ecad4860d088588a547786c0a9ed8cf3cc8045f8f1eb417c31cf2`
  and a 1,090,506-byte source distribution at
  `7de047cbe0b6dc5b8120795e6c1207db8a66a3f0a4372d8a69fad510a7116368`;
  installed-wheel and complete release smoke passed.
- Integration: the sole valid P2 was answered with correction evidence and its
  thread resolved. Two delayed audits found no new issue comment, review
  activity, or unresolved thread. Head-pinned GitHub-verified squash
  `22c432310fae2f9ac372062cbd465cc2617fb95c` has tree
  `a891364113a439c08e985c925fc81a507053fb2c` exactly equal to the corrected
  feature head, sole parent M55 closeout
  `e7f700454adf1c11c80cb1ba684ed3318f7876e4`, a valid signature, and
  standalone DCO. The feature branch is deleted locally/remotely; no
  post-merge `main` run, open PR, non-main remote branch, tag, or release
  exists.
- Integration record: exact head
  `db7c50009243fa7cf3bf9cd8f57afb4589dec7e7` passed run `31330464522` in one
  38-second Linux allocation. All 299 Python files were format clean, Ruff and
  strict docs passed, 604 documentation architecture assertions passed,
  reproducible distributions plus installed-wheel and complete release smoke
  passed, and desktop umbrella `93287863357` skipped with zero steps. Two
  delayed audits found no comment, review, or thread. Head-pinned GitHub-
  verified squash `acc6893ef4cadf9a17c87cd578e38b7802a3ed77` has tree
  `69ed3d44d8eab6cfa98cb646f897a9cb295296f8` exactly equal to the record
  head, sole parent feature squash
  `22c432310fae2f9ac372062cbd465cc2617fb95c`, a valid signature, and
  standalone DCO. No post-merge `main` run was allocated; both working
  branches are deleted locally/remotely, and no open PR, non-main remote
  branch, tag, or release exists. The remaining three-file `.project/**`
  closeout must allocate zero hosted runs or checks.

## M55 public release HTTP response framing - complete

- Base: exact clean synchronized M54 closeout
  `aab15d601eb4402213f2e058f270237b964f1000`, with only `main` present and no
  open pull request, tag, release, or post-closeout `main` run.
- Scope: after all connected-peer/TLS checks and `getresponse()`, validate
  documented response version and framing before status, redirect, or body
  use. Require the HTTP/1.1-class integer value `11` without claiming exact raw
  status-line identity; allow absent or case-insensitive
  exact `chunked` transfer encoding; reject transfer encoding plus content
  length; require any content length to be a string before existing bounds.
- Failure: malformed, unsupported, ambiguous, missing, and raising metadata
  uses stable, content-silent `public_release.request_failed`; a supported
  local inspection exception remains chained. Every redirect repeats the
  validation independently.
- Boundary: no workflow, allocation, dependency, package, public API, release
  authority, private response state, raw HTTP/chunk parser, alternate client,
  HTTP/2 or HTTP/3, proxy, decompression, retry, cache, or network sandbox.
  Fixture/PR evidence is not a real public release observation or general
  request-smuggling protection, and public value `11` is not exact status-line
  token evidence because CPython can normalize another raw `HTTP/1.x` value.
- Decision: accepted RFC-0038 records the exact metadata, ordering, ownership,
  failure, non-claim, and authority boundaries.
- Development evidence: after the hosted review correction, all 189 focused
  M47-M55 assertions pass. All 298 Python files are format clean; Ruff and
  strict Pyright report zero findings; 567 architecture assertions and strict
  docs pass. Complete graphics-enabled CPython 3.12-3.14 suites each pass 2,107
  tests with 14 expected skips. Real-wgpu, profiles, both vertical slices,
  documented benchmark validators, reproducible builds, isolated-wheel smoke,
  and complete release smoke pass.
- Review: a first credential expression overmatched the legitimate `ghp-import`
  lock entry and was corrected to actual token lengths. Repeat findings-first
  correctness, security, scope, history, archive, credential, identity, and
  integrity review found no actionable issue. The 24-path candidate changes no
  workflow, runtime package, benchmark, project metadata, or lock.
- Local status: final fail-fast lock, format, lint, type, architecture, strict-
  docs, reproducible-build, installed-wheel, complete release-smoke,
  whitespace, and Git-object gates pass. The final evidence-inclusive static
  gate and corrected exact-head hosted validation also pass.
- Hosted review correction: initial exact head
  `77812ae6b25635a9831b43088bd4397645fb4adf` passed run `31324078779` in
  exactly three Linux-first allocations. Delayed review then correctly found
  that CPython maps other raw `HTTP/1.x` status-line tokens to public value
  `11`, invalidating the original exact-token implication. M55 now treats `11`
  as the documented compatibility bucket and explicitly disclaims exact raw
  token evidence. Corrected focused/static/docs and complete graphics-enabled
  CPython 3.12-3.14 suites, real-wgpu, profiles, both vertical slices,
  reproducible builds, isolated-wheel smoke, and complete release smoke pass.
  Corrected findings-first review and final evidence-inclusive static gate have
  no remaining local issue.
- Hosted evidence: corrected exact head
  `f57c28b9cc3a05ef1da830c8ad478d85d46b4a3a` passed run `31325192734` in
  exactly three Linux-first allocations. Linux passed in 7m26s before macOS and
  Windows began; macOS passed in 2m44s and Windows in 2m57s. Baseline and every
  compatibility suite passed 2,111 tests, with one expected skip outside the
  baseline; all three platforms passed real graphics, profiles, Clockwork
  Arena, and Agent World Builder.
- Hosted artifacts: exact corrected-head reproducibility produced a pure
  270,593-byte wheel at
  `4b6917302282746f301e082003a4474cef230bc77bda7a0b19d90b59a7f566af`
  and a 1,077,996-byte source distribution at
  `bd8378618ca43f52ea4049ecde33eed5a8a33a40228e891a3073710221df9e26`;
  installed-wheel and complete release smoke passed.
- Integration: the sole P2 was answered with the correction evidence and its
  thread resolved. Two delayed audits found no new review, issue comment, or
  unresolved thread. GitHub-verified squash
  `879de01c5e1869c6493b59f4fbd904e361f9ddb6` has the exact corrected feature
  tree, sole parent M54 closeout, valid signature, and standalone DCO. The
  feature branch is deleted locally/remotely; no post-merge `main` run, tag, or
  release exists.
- Integration record: the exact four-file record passed local lock, format,
  lint, 567-test architecture, strict-docs, reproducible-build,
  installed-wheel, release-smoke, whitespace, and Git-object gates. Initial
  hosted run `31325924046` passed the bounded documentation lane, but review
  correctly found one stale pending-validation sentence. The corrected exact
  head `ff71acdadbee98043f3d9f06fa1bb08371f89bfc` passed replacement run
  `31326132049` in one 38-second Linux allocation; the desktop umbrella skipped
  with zero steps. The sole thread was answered and resolved, and the delayed
  audit found no new issue.
- Record integration: head-pinned GitHub-verified squash
  `d0a230e2329daecf4e248350289351c1e81827f6` has tree
  `c079de60da5e3b24e8e9b11507f012ad9fbae13e` exactly equal to the corrected
  record head, sole parent feature squash
  `879de01c5e1869c6493b59f4fbd904e361f9ddb6`, a valid signature, and standalone
  DCO. No post-merge `main` run was allocated; both M55 working branches are
  deleted locally/remotely, and no tag or release exists. The remaining
  three-file `.project/**` closeout must allocate zero hosted runs or checks.

## M54 public release TLS session freshness - complete

- Base: exact clean synchronized M53 closeout
  `fe585f8bd2313feac39b70cadf088c57bbb1960e`, with only `main` present and no
  open pull request, tag, release, or post-closeout `main` run.
- Scope: after the handshake, M49 peer confinement, and M53 exact context
  binding, require the actual socket's `session_reused` observation to be
  exactly `False` before M52 identity, M51 session inspection, or HTTP. Repeat
  independently on every redirect.
- Failure: a missing socket/accessor, unsupported observation, resumed session,
  malformed value, or inspection exception uses stable, content-silent
  `public_release.tls_failed`; an available local exception remains chained.
- Boundary: no workflow, allocation, dependency, package, public API, release
  authority, session cache, session assignment, ticket control, custom TLS
  implementation, trust replacement, pinning, parser, revocation, channel
  binding, proxy, or network sandbox. Reported non-reuse does not independently
  prove a full handshake or certificate exchange. Fixture/PR evidence is not a
  real public release observation.
- Decision: accepted RFC-0037 records the exact observation, ordering,
  ownership, failure, non-claim, and authority boundaries.
- Development evidence: all 157 focused M47-M54 assertions pass. All 297
  Python files are format clean; Ruff and strict Pyright report zero findings;
  535 architecture assertions and strict docs pass. Complete graphics-enabled
  CPython 3.12-3.14 suites each pass 2,075 tests with 14 expected skips. Real-
  wgpu, profiles, both vertical slices, documented benchmarks, reproducible
  build, isolated wheel, and release smoke pass. Exact commands, counts,
  hashes, and the sandbox-blocked attempt are recorded in test evidence.
- Review: an initial documentation review found that the RFC index ended at
  RFC-0034 and the changelog ended at M51; both are corrected through M54. A
  first post-record guard was overly broad and is corrected. Repeat findings-
  first correctness, security, scope, history, archive, credential, identity,
  and integrity review found no actionable issue. The 23-path candidate changes
  no workflow, runtime package, benchmark, metadata, or lock.
- Local status: final fail-fast static, architecture, docs, reproducible build,
  installed-wheel, release-smoke, archive, whitespace, and Git-object gates
  pass.
- Hosted evidence: exact feature head
  `d5d02a38ea302c0e314f966376e267c45508d14b` passed run `31321661693` in
  exactly three Linux-first allocations. Linux passed in 6m23s before macOS
  and Windows began; macOS passed in 2m10s and Windows in 4m11s. Every static,
  supported-Python, real-graphics, profile, sample, reproducible-build,
  isolated-wheel, and release-smoke step passed.
- Hosted artifacts: exact-head reproducibility produced a pure 270,321-byte
  wheel at SHA-256
  `009b51c9ddb4606968f195a5543288c7e98114ebaec85111347addf00a5eceee`
  and a 1,068,001-byte source distribution at
  `b26ff481a608d9d9777e65650f9556c2d880d7ab28c01a7a38b7c6ed7c1b17f1`.
- Integration: delayed review found no review, issue comment, inline comment,
  or thread. GitHub-verified squash
  `c333f2b9aad98b9a55d986076fe8b09153d30762` has the exact reviewed feature
  tree, sole parent M53 closeout, valid signature, and standalone DCO. The
  feature branch is deleted locally/remotely; no post-merge `main` run, tag, or
  release was created. The remaining integration record changes exactly four
  documentation/project paths.
- Integration record: exact head
  `baec3a2bac0c0bdd8dd4bceb66cdb6e26973538b` passed run `31322470238` in one
  37-second Linux documentation allocation. All 297 files were format clean,
  Ruff passed, strict docs built, 535 architecture assertions passed,
  reproducible build plus wheel/release smoke passed, and desktop umbrella
  `93267534507` skipped with zero steps. No review, comment, or thread existed.
- Record integration: GitHub-verified squash
  `50a14e0674c4e7468faf1c8ec4490846255558ce` has the exact reviewed record
  tree, sole parent feature squash, valid signature, and standalone DCO. Both
  working branches are deleted locally/remotely; no post-merge `main` run, tag,
  or release exists. The remaining closeout is exactly three `.project/**`
  files and must allocate zero hosted runs/checks.

## M53 public release TLS context binding - complete

- Base: exact clean synchronized M52 closeout
  `8d69f5b265277edb95ae47ea3a0af001217a4575`, with only `main` present and no
  open pull request, tag, release, or post-closeout `main` run.
- Scope: after the handshake and M49 peer confinement, require the actual
  socket to retain the exact M50 context object supplied to that hop and an
  exactly client-side role. Revalidate the complete context policy before M52
  service identity, M51 negotiated session, or HTTP transmission. Repeat on
  every redirect with an independent context.
- Failure: missing/unsupported accessors, context substitution, wrong role,
  post-handshake policy mutation, and inspection failures use the stable,
  content-silent `public_release.tls_failed` code before later TLS evidence or
  request transmission. Available local inspection causes remain chained.
- Boundary: no workflow, runner allocation, dependency, lock, version, runtime
  package, public API, credential, release mutation, or release-authority
  change. No trust replacement, pinning, certificate/chain parsing, revocation,
  session reuse, channel binding, proxy, network sandbox, or external monitor.
- Decision: accepted RFC-0036 records exact object binding, post-handshake
  policy revalidation, ordering, ownership, failure, authority, and non-claim
  boundaries.
- Development evidence: focused M47-M53 behavior passes 144 assertions. All
  296 Python files are format clean; Ruff and strict Pyright report zero
  findings; 522 architecture assertions and strict docs pass. Complete
  graphics-enabled CPython 3.12-3.14 suites each pass 2,062 tests with 14
  expected skips. Real-wgpu, profiles, both vertical slices, documented
  benchmarks, reproducible build, isolated wheel, and release smoke pass.
  Exact commands, counts, hashes, and corrected attempts are recorded in test
  evidence.
- Review: findings-first diff, scope, history, integrity, credential, identity,
  backend/native leakage, and public-boundary review found no actionable
  finding. The 19-path candidate changes no workflow, runtime package,
  benchmark, metadata, or lock. Final record-inclusive static, architecture,
  docs, reproducible build, installed wheel, and release smoke pass.
- Hosted evidence: exact feature head
  `0b3eaad213a149fb96c138cd4eabc1d861d053e9` passed run `31319422736` in
  exactly three Linux-first allocations. Linux passed in 7m05s before macOS
  and Windows began; macOS passed in 2m08s and Windows in 4m01s. Every static,
  supported-Python, real-graphics, profile, sample, reproducible-build,
  isolated-wheel, and release-smoke step passed.
- Integration: delayed review found no review, issue comment, inline comment,
  or thread. GitHub-verified squash
  `66f9d84eea57c270e9b18326348eb1ea5c4ebfa4` has the exact reviewed feature
  tree, sole parent M52 closeout, valid signature, and standalone DCO. The
  feature branch is deleted locally/remotely; no post-merge `main` run, tag, or
  release was created.
- Integration record: exact head
  `de488d1e305026f724a155bf692653cd5f8cb454` passed run `31320201771` in one
  36-second Linux documentation allocation. All 296 files were format clean,
  Ruff passed, strict docs built, 522 architecture assertions passed,
  reproducible build plus wheel/release smoke passed, and desktop umbrella
  `93261877229` skipped with zero steps. No review, comment, or thread existed.
- Record integration: GitHub-verified squash
  `9217862df30d51efa7754cc8a9300c4b05fb2426` has the exact reviewed record
  tree, sole parent feature squash, valid signature, and standalone DCO. Both
  working branches are deleted locally/remotely; no post-merge `main` run, tag,
  or release exists. The remaining closeout is exactly three `.project/**`
  files and must allocate zero hosted runs/checks.

## M52 public release TLS service-identity evidence - complete

- Base: clean synchronized M51 closeout
  `047478d0c7fb873ae94aaa6e322b5b08903ed354`, with only `main` present
  locally/remotely and no open pull request, tag, GitHub release, or post-
  closeout `main` run.
- Outcome: observe the URL-derived reference hostname and peer certificate on
  every fixed API or bounded redirected asset TLS socket before negotiated-
  session inspection or HTTP transmission.
- Identity boundary: normalize the URL hostname through built-in IDNA; require
  the socket's non-empty `server_hostname` to match case-insensitively and
  require `getpeercert(binary_form=True)` to return non-empty immutable DER
  bytes.
- Ordering and ownership: every hop connects, validates its actual global
  port-443 peer, validates service identity, validates its M51 session, and
  only then transmits HTTP. The existing connection owns and closes the socket
  on success or failure; every redirect repeats the complete sequence.
- Failure: unavailable or unsupported access, invalid IDNA, malformed or
  mismatched reference state, missing/non-byte certificate, or inspection
  failure uses content-silent `public_release.tls_failed` without revealing a
  host, certificate, peer, URL, session value, response, or credential.
- Preserved: M51 session conformance, M50 explicit context/key-log isolation,
  M49 connected-peer confinement, M48 response/header/failure conformance, and
  every M47 identity, deadline, size, path, exact-validation, and installed-
  smoke bound.
- No scope growth: no certificate parser or independent matcher, custom trust,
  certificate/SPKI/fingerprint pin, chain export, revocation/OCSP/CRL/CT,
  DNSSEC, workflow, runner, action, permission, trigger, credential, release
  mutation, retry, cleanup, dependency, lock, version, runtime package, or
  public API change.
- Decision: accepted RFC-0035 records the service-identity observation,
  ownership, failure, authority, and non-claim boundary. M50/OpenSSL remains
  authoritative for certificate-path, validity, and hostname verification.
- Development evidence: official Python 3.14.7 and RFC 9525 review supports the
  selected surfaces and terminology. Findings-first review corrected a Unicode
  case-fold confusable and added missing-accessor/invalid-IDNA coverage. The
  focused M52 suite, final static/architecture/docs and supported-Python
  suites, real-wgpu, profiles, both vertical slices, benchmark validation,
  reproducible build, isolated wheel, and release smoke pass. Exact commands,
  counts, hashes, and corrected attempts are recorded in
  `.project/TEST_EVIDENCE.md`. Each final CPython 3.12-3.14 graphics-enabled
  suite passed 2,044 tests with 14 expected skips. Record-inclusive
  reproducible build, isolated-wheel, and complete ten-artifact release smoke
  also pass. Exact review, hosted, and integration evidence follows below.
- Review correction: the first invalid-IDNA regression supplied an already
  connected fake socket, while a real connection could attempt its own IDNA
  conversion first and escape as a generic request failure. The corrected
  candidate derives and uses the ASCII reference before constructing the
  connection; actual socket comparison and certificate observation remain
  after peer confinement. The corrected focused Ruff, strict-Pyright, docs,
  and 126-assertion M47-M52 behavior gate passes. Corrected complete CPython
  3.12-3.14 suites each pass 2,044 tests with 14 expected skips. Corrected
  reproducible build, isolated-wheel, complete release smoke, post-record
  static/architecture/docs, archive/scope scans, and repeat findings-first
  review pass with no remaining finding.
- Hosted evidence: exact head
  `170db846112e27b9d11377da69784c69a6565bb4` passed run `31316474864` in
  exactly three Linux-first allocations. Linux job `93252443745` passed in
  7m02s before macOS `93253220602` and Windows `93253220599` began; they
  passed in 2m16s and 3m59s. Linux baseline passed 2,048 tests; Ubuntu
  CPython 3.13/3.14 and both desktop CPython 3.14 suites passed 2,048 tests
  with one expected skip. All platforms passed ten graphics tests, profiles,
  Clockwork Arena, and Agent World Builder. Reproducibility passed for the
  269,957-byte wheel
  `0bbdcc263fa1b28b7c0b8e29559b45b47df28b7d61a43eb23feb941d6e1e3386`
  and 1,053,252-byte sdist
  `ec58993d27bdfdfe06f16bd963651fb68cd04c842a50649f1e8ed675f1af4581`;
  installed-wheel and complete release smoke passed.
- Feature integration: PR #108 remained `MERGEABLE/CLEAN` at its exact
  reviewed head/base after a delayed audit found zero reviews, issue comments,
  inline comments, or threads. GitHub-verified squash
  `eb083089bfff774c0df2b115428901357c9084b2` has tree
  `ab92b60f4e05faccc2b0059d3d9cfad6b0e0eaef` exactly equal to the reviewed
  feature tree, sole parent M51 closeout
  `047478d0c7fb873ae94aaa6e322b5b08903ed354`, and standalone DCO. No post-
  merge `main` run was allocated; the feature branch is deleted locally and
  remotely. No real tag or release was created.
- Integration-record review correction: initial PR #109 head
  `92427931151106f7b1ce9c77c4809bf794d1f7f9` passed docs-only run
  `31317421319` in one Linux allocation with a zero-step skipped desktop
  umbrella. External review then found the stale pending-gates sentence above,
  which contradicted the exact hosted and integration evidence. The corrected
  record removed that sentence; the initial otherwise-green head was not
  merged.
- Integration-record hosted evidence: corrected exact head
  `6e36c1a77e5ca9c1ca50b272c184fab63495299c` passed run `31317666409`.
  Linux job `93255421358` passed in 42 seconds with formatting, lint, strict
  docs, 504 documentation architecture assertions, reproducible build,
  isolated-wheel smoke, and complete release smoke. The 269,957-byte wheel was
  `0bbdcc263fa1b28b7c0b8e29559b45b47df28b7d61a43eb23feb941d6e1e3386`;
  the 1,055,033-byte sdist was
  `ca9a361a96c899eff198421fc8fc015385011b0ac89110ccdd35a3d629c357de`.
  Desktop umbrella job `93255511671` skipped with zero steps and no runner
  allocation.
- Integration-record squash: the sole actionable PR #109 thread is resolved
  after its stale sentence was removed. The PR was `MERGEABLE/CLEAN` at the
  exact corrected head/base. GitHub-verified squash
  `cd697ef150861c405b9e104db009a15a9db78e47` has tree
  `0dd8456b491f5a8f783407b1c2f237a0e7604407` exactly equal to the corrected
  record tree, sole parent feature squash
  `eb083089bfff774c0df2b115428901357c9084b2`, and standalone DCO. No post-
  merge `main` run was allocated; both feature and record branches are deleted
  locally/remotely. Synchronized `main`, `origin/main`, and `origin/HEAD` now
  resolve to that squash; no open PR, tag, or GitHub release exists and full
  Git-object checking passes.
- Non-claim: fixture and pull-request conformance are not a real public release
  observation, independent/external verification, every TLS/CDN/geographic
  path, future availability, immutability, artifact security, PyPI, or a
  supported release channel.

## M51 public release negotiated TLS-session conformance - complete

- Base: clean synchronized M50 closeout
  `53f3804010f1556ecaff21a61b1e9c405a26e203`, with only `main` present
  locally/remotely and no open pull request, tag, or GitHub release.
- Outcome: advertise only HTTP/1.1 and validate the actual negotiated TLS
  session on every fixed API or bounded redirected asset hop after connected-
  peer confinement and before HTTP transmission.
- Session boundary: require exactly TLSv1.2 or TLSv1.3, a well-formed three-
  field cipher report with at least 128 integer secret bits, no TLS
  compression, and ALPN `http/1.1` or no negotiated ALPN.
- Ordering and failure: each hop connects, validates its actual global port-443
  peer, validates the session, and only then sends the request. Missing,
  unsupported, malformed, or unexpected session state uses content-silent
  `public_release.tls_failed`; the existing connection close path is retained.
- Preserved: M50 explicit context/key-log isolation, M49 connected-peer
  confinement, M48 response/header/failure conformance, and every M47 identity,
  deadline, size, path, exact-validation, and installed-smoke bound.
- No scope growth: no cipher-name allowlist, custom trust, certificate/SPKI pin,
  revocation or ticket policy, TLS fingerprint, workflow, runner, action,
  permission, trigger, credential, release mutation, retry, cleanup,
  dependency, lock, package version, runtime package, or public API change.
- Decision: accepted RFC-0034 records the exact session, ownership, failure,
  authority, and non-claim boundary. A future protocol label requires another
  reviewed decision rather than implicit acceptance.
- Local evidence: all 294 Python files format cleanly; Ruff and strict Pyright
  report zero findings; all 485 architecture assertions pass; strict docs
  build passes. Complete graphics-enabled CPython 3.12.13, 3.13.13, and 3.14.5
  suites each pass 2,025 tests with 14 expected skips. Ten real-wgpu tests,
  both three-repeat profile contracts, Clockwork Arena, Agent World Builder,
  and all documented M1-M4 benchmark validators pass. Candidate-tree
  reproducible-distribution, isolated-wheel, and release-smoke identities are
  recorded in `.project/TEST_EVIDENCE.md`; the matching exact-head hosted
  evidence follows below.
- Review correction: initial PR #105 head `cdd3cc8fd943861072efafed593462fac7ffc3f4`
  passed its exact three-allocation hosted gate, but pre-merge review found that
  an unhashable malformed negotiated-version value could escape the stable
  failure boundary. The corrected candidate first type-checks the version and
  adds sequence/mapping regressions; the initial head will not be merged.
- Hosted evidence: corrected head `a0612236aa13c2892fd95e55c2a77286d21572d4`
  passed run `31312987430` in exactly three allocations. Linux job
  `93243602979` passed in 7m16s before macOS `93244384980` and Windows
  `93244384979` began; they passed in 2m02s and 3m55s. Linux baseline and every
  hosted compatibility suite passed 2,029 tests; each nonbaseline suite had one
  expected skip. All platforms passed ten graphics tests, profile smoke,
  Clockwork Arena, and Agent World Builder. Exact-head reproducibility passed
  for wheel `9539b42da0143fb893e107eeb554dfe0229125439627f361b3b7507b9f3df989`
  and sdist `27c0604758c1d9eb391bf26a093c9c5f85396e33a6a84e4af49004bf0f1bbc5f`.
- Feature integration: the sole prior review thread is outdated and resolved
  after the correction; no issue comment or unresolved thread remains. PR #105 was
  `MERGEABLE/CLEAN` at the exact corrected head/base. GitHub-verified squash
  `ce4184b4ecedd9163a654cc96ae6c96086683760` has tree
  `c331ea93e5332b47a3df20906dfb6f6e77c6cdb3` exactly equal to the reviewed
  head, sole parent M50 closeout
  `53f3804010f1556ecaff21a61b1e9c405a26e203`, and standalone DCO. No post-
  merge `main` run was allocated; the feature branch is deleted locally and
  remotely.
- Integration-record review: four-file record PR #106 initially passed exact-
  head docs-only run `31313663654` at
  `bea144e9d0444237c08a3be6a56905f6d66b2c65` in one Linux allocation, but
  review found a stale sentence claiming hosted validation remained pending.
  The sentence was corrected; its one thread is resolved and no issue comment
  remains.
- Integration-record hosted evidence: corrected exact head
  `aa94d62a06d51f635a6dce1dcbfd686a8c0ac2dd` passed run `31313847857`.
  Linux job `93245782842` passed in 38 seconds with formatting, lint, strict
  docs, 485 documentation architecture assertions, reproducible build,
  isolated-wheel smoke, and complete release smoke. The 269,728-byte wheel was
  `9539b42da0143fb893e107eeb554dfe0229125439627f361b3b7507b9f3df989`;
  the 1,043,265-byte sdist was
  `5b66b95d6976c88943afccf1731ee359cd82e08b9bb0d46bb779b46fc3378b40`.
  Desktop umbrella job `93245857571` skipped with zero steps and no runner
  allocation.
- Integration-record squash: PR #106 was `MERGEABLE/CLEAN` at the exact
  corrected head/base with its sole thread resolved. GitHub-verified squash
  `d2cc5d630b15351289008976d192232cde184afc` has tree
  `706324da08b466e14f77fe34eb2f1cad727eecca` exactly equal to the reviewed
  record head, sole parent feature squash
  `ce4184b4ecedd9163a654cc96ae6c96086683760`, and standalone DCO. No post-
  merge `main` run was allocated; both merged record branches are deleted
  locally/remotely. Synchronized `main`, `origin/main`, and `origin/HEAD` now
  resolve to that squash; no open PR, tag, or GitHub release exists and full
  Git-object checking passes.
- Non-claim: no real signed tag or release was created or exercised. Fixture
  and pull-request evidence are not a real public release observation,
  independent/external verification, every delivery path, future-availability
  or immutability proof, artifact-security result, PyPI availability, or a
  supported release channel.

## M50 public release TLS key-log isolation - complete

- Base: clean synchronized M49 closeout
  `f6214992b02a9ef0bc44d6a9e4e6d72dc9d33de0`, with only `main` present
  locally/remotely and no open pull request, tag, or GitHub release.
- Outcome: replace `ssl.create_default_context()` in the portable public
  release verifier with one explicit `PROTOCOL_TLS_CLIENT` context per fixed
  API or bounded redirected asset hop.
- TLS boundary: load system server-auth roots; require `CERT_REQUIRED`, hostname
  checking, TLS 1.2 minimum, and strict/partial-chain X.509 verification; reject
  any context with active key logging.
- Ambient boundary: leave `SSLKEYLOGFILE` untouched and prove a controlled
  nonexistent target is neither created nor used by successful fixed and
  redirected fixture requests.
- Failure boundary: context construction, root loading, or invariant failure
  uses content-silent `public_release.tls_failed` with internal cause chaining.
- Preserved: M49 connected-peer validation, M48 response/header/failure
  conformance, and every M47 identity, deadline, size, path, exact-byte,
  partial, validation, and installed-smoke bound.
- No scope growth: no workflow, runner, action, permission, trigger,
  credential, proxy, custom trust store, certificate/SPKI pin, client
  certificate, release mutation, retry, cleanup, dependency, lock, package
  version, runtime package, or public API change.
- Decision: accepted RFC-0033 records the ownership, failure, authority, and
  non-claim boundary. System/OpenSSL default trust remains authoritative.
- Local evidence: all 293 Python files format cleanly; Ruff and strict Pyright
  report zero findings; all 464 architecture assertions pass; strict docs
  build passes. Complete graphics-enabled CPython 3.12.13, 3.13.13, and 3.14.5
  suites each pass 2,004 tests with 14 expected skips. Ten real-wgpu tests,
  both three-repeat profile contracts, Clockwork Arena, Agent World Builder,
  reproducible distributions, isolated-wheel smoke, and complete release smoke
  pass.
- Hosted evidence: ready PR #102 exact head
  `99134b6be68bb7978431710228e788250561659e` passed run `31309759226` in
  exactly three allocations. Linux job `93235618328` passed in 7m43s before
  macOS `93236421634` and Windows `93236421636` began; they passed in 2m08s
  and 3m01s. Linux baseline and every hosted compatibility suite passed 2,008
  tests; each nonbaseline suite had one expected skip. All platforms passed ten
  graphics tests, both profiles, Clockwork Arena, and Agent World Builder.
- Integration: PR #102 was `MERGEABLE/CLEAN` at the exact head/base with zero
  submitted reviews, issue comments, review comments, or review threads.
  GitHub-verified squash `5fb56120e1a96a0a25db96baa3836699e435611c`
  has tree `2ec52b638069d23aabd68af04f3ada426aab803d` exactly equal to the reviewed
  head, sole parent M49 closeout
  `f6214992b02a9ef0bc44d6a9e4e6d72dc9d33de0`, and standalone DCO. No
  post-merge `main` run was allocated. The feature branch is deleted
  locally/remotely and only synchronized `main` remains.
- Non-claim: no real signed tag or release was created or exercised. Fixture
  and pull-request evidence are not a real public release observation,
  negotiated-session audit, independent/external verification, every delivery
  path, future-availability/immutability proof, artifact-security result, PyPI
  availability, or a supported release channel.
- Integration record: four-Markdown PR #103 exact head
  `7441e9fae142a67a9d30075ac4c28127978cc750` passed documentation-only run
  `31310482277` in one 40-second Linux allocation. All 464 architecture tests,
  strict docs, reproducible build, wheel smoke, and release smoke passed; the
  desktop umbrella had zero steps and was skipped. The PR had zero reviews,
  comments, or threads. Verified squash
  `7764ea32645c3455fb08bfbd5a3c4e2d8cabbd47` has exact reviewed tree
  `d2ea7fe46d4a807c17f896ba0cfaa87e2f499a44`, sole parent the M50 feature
  squash, valid signature, and standalone DCO. No post-merge `main` run was
  allocated and the branch is deleted locally/remotely.
- Closeout boundary: only `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` may change. The
  final PR must trigger zero runs/checks and contain no review/comment/thread
  before exact-tree squash integration. M50 is otherwise complete.

## M49 public release connected-peer confinement - complete

- Base: exact verified M48 closeout
  `049cdbcf2769a1c2359593f642e37697d5bf7400`; clean synchronized `main`
  only, no open PR, tag, or release, and healthy Git objects.
- Outcome: connect and validate the actual TLS peer before every fixed API or
  redirected asset HTTP request, allowing only globally reachable unicast IPv4
  or IPv6 at port 443.
- Bounds: actual `getpeername()` rather than a separate DNS preflight; mapped
  IPv4 normalization; stable forbidden/timeout/request codes; no hostname/IP
  allowlist; all M48 identity, response, TLS, timeout, byte, path, validation,
  and smoke bounds retained.
- Authority unchanged: no workflow, runner allocation, action, permission,
  trigger, credential, release mutation, retry, cleanup, dependency, lock,
  version, runtime, package, or public API.
- Non-claim: fixture/pull-request conformance is not a real public release
  observation, independent/external verification, network sandbox, every CDN
  path, future availability, immutability, artifact security, PyPI, or a
  supported channel. No real pass exists without an authorized signed-tag run.
- Current evidence: official GitHub, Python, and IANA sources support the
  retained redirect and connected-peer/global-reachability boundaries. Strict
  Ruff/Pyright and all 74 non-documentation M47-M49 assertions pass after two
  factual fixture corrections. CPython 3.12-3.14 classify the probed corrected
  special-purpose ranges identically. The documentation-integrated focus, all
  457 architecture tests, complete graphics-enabled CPython 3.12-3.14 suites,
  ten real-wgpu tests, profiles, both deterministic vertical slices,
  reproducible distribution, isolated-wheel smoke, and complete release smoke
  pass. Final record-inclusive static/docs/architecture/distribution, scope,
  credential, identity, package-content, and initial findings-first review
  pass. Feature PR #98 exact head
  `c19d37f24516bbdc8bea71b521936ac7daf1f8e9` passed its exact three hosted
  allocations. Hosted review then identified that CPython can report
  deprecated IPv6 site-local and reserved ranges as globally classified. PR
  #98 will remain unmerged. The corrected tree explicitly rejects
  `is_site_local` and `is_reserved`, adds `fec0::1` and `5f00::1` regressions,
  and passes formatting, Ruff, strict Pyright, 31 focused assertions, complete
  graphics-enabled CPython 3.12-3.14 suites with 1,997 passes and 14 expected
  skips each, ten real-wgpu tests, both profiles, both deterministic vertical
  slices, reproducible distribution, isolated-wheel smoke, and complete
  release smoke.
- Hosted evidence: replacement PR #99 exact head
  `01c955f0256c0c6e3a34afaf317c828e439b87ca` passed run `31307775820` in
  exactly three allocations. Linux qualified first in 422 seconds; macOS then
  passed in 143 seconds and Windows in 230 seconds. Linux passed 2,001 baseline
  tests and Ubuntu CPython 3.13/3.14 each passed 2,001 with one skip. Each
  desktop passed ten real-wgpu tests, both vertical slices, profiling, and
  2,001 CPython 3.14 tests with one skip. Reproducible exact-head artifacts
  were a 269,300-byte wheel at
  `4d0c8951410d181730ade2103b5c19720a568eee004169de10d86659377baa1c` and a
  1,023,424-byte sdist at
  `ba42cc14a628a95ef928bd9fa7e974af61b2650fd18667b3a853cd9c9a1ef374`.
- Integration: PR #99 was clean and mergeable with no review, comment, or
  thread. GitHub-verified squash
  `842aedc67a7ae4584821c4d8bc96a4ed8cb334c3` has exact reviewed tree
  `a9755cbf65dfeba5087f5037f73bc6027c408444`, sole parent the M48 closeout,
  and standalone DCO. No post-merge run was allocated, and the feature branch
  is deleted locally/remotely. No signed-tag release rehearsal ran.
- Record: documentation-only PR #100 exact head
  `6d04bbf9f77382b5df3c4d1a7f5d0b70496751f9` passed run `31308454299` in
  one 31-second Linux allocation; its desktop umbrella was skipped with zero
  steps. The PR had no review, comment, or thread. Verified squash
  `d6ef4fef7f42a8bd961ea549eb3deb618a0c073f` has exact reviewed tree
  `55048621e219b915879736730011393b14caf49e`, sole parent the M49 feature
  squash, valid GitHub signature, and standalone DCO. No post-merge run was
  allocated, and the record branch is deleted locally/remotely.

## M48 public release HTTP response conformance - complete

- Base: exact verified M47 closeout
  `8d8d9e4a5790d7b74ec06139d314ffdf30a4ef41`; clean synchronized `main`
  only, no open PR, tag, or release, and healthy Git objects.
- Outcome: constrain the portable public release client to the documented
  direct-`200` release response and `200`/bounded-`302` asset responses, while
  separating timeout, transport/protocol, and local-output failure codes.
- Bounds: fixed repository/IDs and initial host, verified HTTPS/default port,
  three asset `302` responses, API-version header only on `api.github.com`,
  10/30-second time limits, bounded document/plan/assets, exact revalidation,
  complete installed release smoke, and content-silent structured results.
- Authority unchanged: no workflow, runner allocation, action, permission,
  trigger, credential, release mutation, retry, cleanup, dependency, lock,
  version, runtime, package, or public API.
- Non-claim: fixture/pull-request conformance is not a real public release
  observation, independent/external verification, every CDN/geographic path,
  future availability, immutability, artifact security, PyPI, or a supported
  release channel. No real pass exists without an authorized signed-tag run.
- Current evidence: official GitHub endpoint documentation defines the bounded
  response set; Python documents blocking timeout behavior and the
  `TimeoutError`/`OSError` relationship. Strict Ruff/Pyright and all 54 focused
  M45/M47/M48 assertions pass. Complete graphics-enabled CPython 3.12-3.14 runs
  each pass 1,966 tests with 14 expected skips. Ten real-wgpu tests, both M7
  profiles, both deterministic vertical slices, reproducible distribution,
  isolated-wheel smoke, and complete release smoke pass locally. The final
  static gate covers 291 Python files, zero Ruff/Pyright findings, 426
  architecture assertions, strict docs, whitespace, and healthy Git objects.
  The final commit-candidate distributions matched byte-for-byte and passed
  isolated-wheel plus complete release smoke.
- Hosted evidence: ready PR #95 exact head
  `9b5c533d1e73ee985945fa0feb7e876417ee0126` passed run `31288303182` in
  exactly three allocations. Linux qualified first in 415 seconds; macOS then
  passed in 118 seconds and Windows in 228 seconds. Linux passed 1,970 baseline
  tests and Ubuntu CPython 3.13/3.14 each passed 1,970 with one skip. Each
  desktop passed ten real-wgpu tests, both vertical slices, profiling, and
  1,970 CPython 3.14 tests with one skip.
- Integration: PR #95 was clean and mergeable with no review, comment, or
  thread. GitHub-verified squash
  `c32ff1bf71b53278ef2ff616c2fc3cfce5cf20a3` has exact reviewed tree
  `1986f691633d94a5b980c2be0b7e1d0b364de37e`, sole parent the M47 closeout,
  and standalone DCO. No post-merge run was allocated, and the feature branch
  is deleted locally/remotely. No signed-tag release rehearsal ran.
- Record: documentation-only PR #96 exact head
  `609e0977ba879be84270c2d4fd47a8b9ad23b4c5` passed run `31288912878` in
  one 33-second Linux allocation; its desktop umbrella was skipped with zero
  steps. The PR had no review, comment, or thread. Verified squash
  `ee98b591abb8e8ecd37b8fa32c01acb0ce279b52` has exact reviewed tree
  `bf4dc989ae014f33b89f81ef67246eb22401ea36`, sole parent the M48 feature
  squash, valid GitHub signature, and standalone DCO. No post-merge run was
  allocated, and the record branch is deleted locally/remotely.

## M47 cross-platform public consumer rehearsal - complete

- Base: exact verified M46 closeout
  `2d27b139c6bf4a130ca97e7f0b518f6ebfe191c5`; clean synchronized `main`
  only, no open PR, tag, or release, and healthy Git objects.
- Outcome: replace the internal Bash public-release verifier with one typed
  standard-library Python program and expand the existing tag-only fresh
  consumer to Ubuntu, Windows, and macOS.
- Bounds: fixed repository/IDs, verified HTTPS, three redirects, 10/30-second
  time limits, 4-MiB document, 16-KiB plan, 32 assets, 256 MiB each, 512 MiB
  total, safe unique names, exclusive partials, exact-set validation, complete
  installed release smoke, content-silent structured results, and no public
  request credential.
- Authority unchanged: two additional tag-only fresh allocations; no
  pull-request allocation, trigger, release mutation, publication command,
  credential, dependency, lock, version, runtime, package, or public API.
- Non-claim: same-workflow hosted cross-platform rehearsal is not independent
  or external verification, a clean machine outside GitHub-hosted Actions,
  every delivery path, future availability, immutability, artifact security,
  PyPI, or a supported release channel. No real pass exists without an
  authorized signed-tag run.
- Local evidence: all 39 focused M45-M47 assertions, the 405-test architecture
  suite, strict static/docs/YAML, ten real-wgpu tests, profiles, both vertical
  slices, and complete graphics-enabled CPython 3.12-3.14 suites pass. Each
  supported interpreter passed 1,945 tests with 14 expected skips. Final
  reproducible distribution, isolated-wheel smoke, and complete release smoke
  pass.
- Hosted evidence: ready PR #92 head
  `fdddaa986b647e68a0a027445c11547b878ad246` passed run `31286321895` in
  exactly three allocations. Linux qualified first in 440 seconds; macOS then
  passed in 160 seconds and Windows in 235 seconds. Linux passed 1,949 baseline
  tests and Ubuntu CPython 3.13/3.14 each passed 1,949 with one skip. Each
  desktop passed ten real-wgpu tests, both vertical slices, profiling, and
  1,949 CPython 3.14 tests with one skip.
- Integration: PR #92 was clean and mergeable with no review, comment, or
  thread. GitHub-verified squash
  `c3f5d9c4b9f21315b7ae8f113cc643f978d75746` has exact reviewed tree
  `e222ebff0655b9d86548bab6e8d19fb79ba3afc5`, sole parent the M46 closeout,
  and standalone DCO. No post-merge run was allocated, and the feature branch
  is deleted locally/remotely. No signed-tag release rehearsal ran.
- Record: documentation-only PR #93 exact head
  `19d0c9f21701acd4fa731c567d3927177374dbce` passed run `31286982718` in
  one 37-second Linux allocation; its desktop umbrella was skipped with zero
  steps. The PR had no review, comment, or thread. Verified squash
  `7bea262210afd5b22265fede596d2d5117b14854` has exact reviewed tree
  `6ebbe7af4071ce2d7a3f7539f9ef84413ed23be8`, sole parent the M47 feature
  squash, valid GitHub signature, and standalone DCO. No post-merge run was
  allocated, and the record branch is deleted locally/remotely.

## M46 fresh-runner public consumer rehearsal - complete

- Base: exact verified M45 closeout commit
  `086f1ceb3974583ce7a2c386c67f516299c2f1dd`.
- Outcome: after successful publication validation, use one separate read-only
  Linux runner to retrieve the same workflow's admitted candidate, fetch and
  revalidate public bytes without a release credential, and run complete
  installed release smoke in a fresh workspace.
- Ownership: the publishing job exports only release ID/version and reuses its
  M43 plan. The dependent job owns its downloaded workflow artifact and must
  exclusively create a fresh plan. One shared script owns fixed public request,
  byte, plan, and smoke bounds but no mutation authority.
- Topology: exactly one additional tag-only Ubuntu job, explicit read-only
  contents permission, 25-minute timeout, duplicated pinned checkout/setup,
  and download-artifact v8.0.1 pinned to verified commit
  `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c`. Pull-request CI is unchanged.
- Claim: a real pass may establish separate same-workflow GitHub-hosted runner
  and isolated-install evidence. It cannot establish independent/external or
  cross-platform verification, a clean machine outside the provider, every
  delivery path, future availability, immutability, artifact security, PyPI,
  or a supported channel.
- Current validation: release-workflow YAML and shared Bash syntax parse; all
  383 architecture assertions pass. Complete graphics-enabled CPython
  3.12-3.14 runs each pass 1,923 tests with 14 capability skips. Static/docs,
  real wgpu, both M7 profiles, deterministic samples, all retained benchmark
  validators, reproducible distribution, isolated-wheel smoke, and complete
  release smoke pass. Review caught a nonexistent plan option before commit;
  the corrected shell uses the established exclusive `--asset-plan` contract,
  and the regression executes the real verifier on all three Python versions.
  Hosted validation and integration remain.
- First hosted run `31282550237` correctly allocated exactly three runners.
  Linux and Windows passed; macOS exposed one Bash 3.2 portability failure in
  existing-plan mode after 1,926 test passes and one skip. The blocked head is
  not mergeable by policy. The correction replaces empty-array expansion under
  `set -u` with a shared verifier function and safe positional arguments while
  retaining exactly two verifier call sites. Focused tests pass on CPython
  3.12-3.14; the corrected complete 3.12 graphics and static/docs/architecture
  gates pass. Corrected hosted evidence passed as recorded below.
- Corrected run `31283211266` passed exact head
  `7f7f865880a415bec2f1fdaffbc35426399fb0fd` in exactly three allocations:
  Linux 7m07s, macOS 2m31s, and Windows 4m24s. Linux passed 1,927 baseline
  tests and Ubuntu 3.13/3.14 each passed 1,927 with one skip; both desktops
  passed 1,927 with one skip. Every platform passed ten real-wgpu tests,
  profiles, Clockwork Arena, and Agent World Builder.
- PR #89 had no review, comment, or thread. GitHub-verified squash
  `d4cb4410d1dd9f684d3b169932ea3251801d3884` has sole parent exact M45
  closeout, tree `a3774ff0846a099c2b821500a93fb3b387db2210` exactly equal to the
  corrected head, and standalone DCO. No post-merge run was allocated; the
  feature branch is deleted locally/remotely. No real tag/release rehearsal ran.
- Record: documentation-only PR #90 exact head
  `4a74380f3011cbb841b89a7778cf676163cc1c28` passed run `31283922258` in
  one 36-second Linux allocation; the desktop umbrella skipped with zero
  steps. It had no review/comment/thread. Verified squash
  `f6a15655b9bfe5657f15baea89d36206743a3468` has exact reviewed tree,
  sole feature-squash parent, valid signature, standalone DCO, and no main
  run. Its branch is deleted. This three-file closeout is the only remaining
  M46 work.

## M45 public release consumer-path integrity - complete

- Base: exact verified M44 closeout commit
  `2c5e312a97028d0b835fc174b8abb51df22ea314`.
- Outcome: after M44, fetch the exact public release and every exact asset ID
  without a GitHub credential, revalidate public metadata/bytes, and execute
  complete installed release smoke against that public directory.
- Boundary: fixed HTTPS GitHub API numeric-ID endpoints, disabled client
  configuration, no authorization/cookie/browser URL, bounded redirects and
  time, a 4-MiB document cap, and inherited M43 ID/name/count/byte/no-clobber
  limits.
- Scope: the existing tag job's postpublication tail, focused architecture
  tests, RFC/docs, and factual records only. No job/action/permission/trigger,
  dependency/lock/version, runtime/public API, tag/release/upload/publication,
  immutability setting, rollback, or cleanup authority.
- Claim: one real tag run may establish a same-run public API and installed-
  candidate observation. It cannot establish independent/external or cross-
  platform consumer evidence, every delivery path, future availability,
  immutability, artifact security, PyPI, or a supported channel.
- Local validation: the corrected focused release chain passes 106 tests
  with three capability skips; the final recorded tree passes all 373
  architecture tests and the seven exact extracted-shell regressions pass on
  CPython 3.12-3.14. The complete CPython 3.12 graphics suite passes 1,913
  tests with 14 expected skips; CPython 3.13/3.14 each pass 1,902 tests with 15
  skips. Real wgpu, profiles,
  deterministic samples, documented benchmark validators, reproducible
  distributions, isolated-wheel smoke, complete release smoke, static checks,
  strict docs, workflow YAML, Bash syntax, whitespace, scope/credential review,
  and full Git object checking pass.
- Hosted validation: ready PR #86 exact head
  `51e5a600c89fbecf09a9addb47e8e2a1729b0081` classified 29 paths as
  substantive and passed run `31279830471` in exactly three allocations. Linux
  passed in 6m58s before macOS and Windows were allocated; macOS passed in
  2m07s and Windows in 4m01s. Every platform passed graphics, profiles, both
  vertical slices, and CPython 3.14 compatibility; Linux also passed complete
  quality, CPython 3.12/3.13, reproducibility, wheel, and release smoke.
- Integration: PR #86 had no review, comment, or thread. GitHub-verified squash
  `471da6efe908463ed8f6744272bd372548cb3345` has sole parent exact M44
  closeout, tree `5f9368d215038b76cc8afb104cf6bcb444a04801` exactly equal to the
  reviewed head, and a standalone DCO trailer. No post-merge `main` run was
  allocated, and the feature branch is deleted locally/remotely.
- Record: documentation-only PR #87 exact head
  `13dcd951226430cb660ddf98ad0bd9c66f4633a5` classified four Markdown
  paths as documentation. Run `31280561142` passed in one 38-second Linux
  allocation with 373 architecture tests, universal build, installed-wheel
  smoke, and complete release smoke; desktop umbrella job `93161106180`
  skipped with zero steps. No review, comment, or thread existed. Verified
  squash `01241e2e1eadff959d13530e1118b0ad6b686dad` has sole parent the
  feature squash, exact reviewed tree, valid signature, standalone DCO, and no
  post-merge run. Its branch is deleted locally/remotely. Only this three-file
  zero-run closeout remains. No real tag, release, or public consumer-path pass
  exists or is claimed.

## M44 published release attestation integrity - complete

- Base: exact verified M43 closeout commit
  `0b3b9eb982a67eee1833f3a8f920671f8ffd006b`.
- Feature: ready PR #83 exact head
  `494ae4f32209c8e679633d528bb63cf4b1093800`; squash-integrated as
  `781ca0d1692b309ca3dd7ea9ca8dc6af88f77b09`.
- Contract: after M43 exact-ID retrieval and byte revalidation, verify SLSA v1
  provenance for every bounded asset and SPDX 2.3 SBOM attestation for exactly
  one pure wheel under exact repository, workflow, tag, source/signer commit,
  GitHub OIDC issuer, hosted-runner, timeout, and bundle-count policy.
- Ownership: the existing tag job owns credentials/network/temp files; the
  standard-library verifier owns bounded local validation and content-silent
  child execution only. Failure after publication performs no mutation,
  cleanup, retry, or rollback.
- Scope: one verifier script, the existing release workflow tail, focused
  tests, RFC/docs, historical workflow-hash guards, and factual project
  records. No job/action/permission/trigger/dependency/lock/runtime/public API,
  tag/release/upload/publication, or version change.
- Validation: complete local 3.12-3.14, graphics, profiles, samples,
  benchmarks, reproducibility, package/release smoke, static, architecture,
  docs, and security/scope gates passed. Hosted run `31277236908` passed the
  exact feature head in three allocations. Its sole review thread was resolved
  from primary evidence without a code change.
- Integration: the GitHub-verified squash has the exact reviewed tree and sole
  parent the M43 closeout; no post-merge `main` run occurred and the feature
  branch is deleted. Documentation-only PR #84 exact head
  `66c58256790127db727c8cc87741d95f6c9a5612` classified four Markdown paths
  as documentation and passed run `31278008212` in one 30-second Linux
  allocation; its desktop umbrella skipped with zero steps. With no feedback,
  it squash-integrated as `792a2e702a8331566ddc5c5bf07e449c66f30f9e`,
  preserving its reviewed tree, exact feature-squash parent, valid signature,
  standalone DCO, and zero post-merge run. Its branch is deleted locally and
  remotely. Only this final `.project/**` closeout record remains. No real
  signed-tag release or hosted attestation pass exists or is claimed.

## M43 complete

M43 starts from exact clean synchronized M42 closeout commit
`2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79`. It closes the remaining gap
between the authenticated published release document and the bytes returned by
GitHub's release-asset endpoint.

The internal validator advances to `ludoweave.release-draft-integrity/4` and
requires each remote asset to carry a unique positive 63-bit ID. A completely
verified published document may write one exclusive runner-temporary
`ludoweave.release-asset-retrieval-plan/1` containing only canonical decimal
IDs, expected byte sizes, and safe basenames. Draft plans, unsafe IDs, existing
targets, missing parents, and incomplete validation fail with structured codes.

The existing tag job consumes that plan, retrieves each exact asset ID through
the authenticated versioned binary endpoint, and reruns the same verifier over
the downloaded directory and same published document. No tag lookup, browser
URL, clobber, mutation, rollback, or cleanup is introduced. This observes one
authenticated retrieval point and does not claim unauthenticated/global/future
availability, immutability, consumer installation, or attestation verification.
M43 adds no job, runner, action, permission, trigger, dependency, credential,
runtime/public API, tag, release, upload, or publication authority.

Complete local validation passed the initial head. Hosted run `31273727767`
also passed in exactly three allocations, but one P2 review found that an
oversized asset response could fill runner storage before post-download
validation. The correction carries each already verified expected size in the
plan, caps each response stream at expected size plus one byte, rejects short
and long responses, and enforces the 512-MiB expected-total boundary during
retrieval. Focused behavior, Git Bash stream semantics, all 361 architecture
tests, the complete 1,870-test suite, static typing, docs, YAML, reproducible
distributions, wheel/release smoke, scope, credential, whitespace, and Git
objects pass on the correction. No remaining local finding was identified.
Corrected release-workflow SHA-256 is
`a5c7ff3f80010cad2712592daf32327b80122b8473cee720fe066bbb3eb06e06`.
Corrected head `3a5004217598c82eca5b8286442e7d8a502642b1` passed hosted run
`31274622529` in exactly three allocations. Linux passed in 7m13s before the
desktop jobs were allocated; macOS passed in 1m48s and Windows in 3m53s. The
Linux baseline and Ubuntu 3.13/3.14 plus both desktop 3.14 suites each passed
1,873 tests, with one expected skip in each compatibility suite. All three
platforms passed ten real-wgpu tests, profiling contracts, Clockwork Arena, and
Agent World Builder. The Linux build reproducibly produced a 267,906-byte wheel
at SHA-256 `b36bf6eebeb8173d04c9dba1c96d166f0294aab0d36804c07523be2cb2fd71c1`
and a 956,605-byte sdist at SHA-256
`2064aa70d5b8cdfef41f9a36b49689cd38e89e0b3a5780000a9d742e8b8a2982`, then
passed installed-wheel and complete ten-artifact release smoke.

The sole P2 thread was answered with the bounded-transfer correction and exact
local/hosted evidence, then resolved. GitHub reported PR #80 `MERGEABLE` and
`CLEAN` with all checks successful. Squash
`8b7038cc203cead16d1dd88c746b584b6d0c37ca` has sole parent exact M42 closeout
`2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79`, tree
`6c5ed36a8454a3ab16fec82152df13038c41ce84` exactly equal to the reviewed
corrected head, a valid GitHub signature, and a standalone DCO trailer. No
post-merge `main` run was allocated. The feature branch is deleted locally and
remotely; synchronized `main` was the sole branch before this record branch.
Documentation-only integration-record PR #81 exact head
`3350a8eb59fae09cd0764a400540d0d51722866e` classified four paths as
documentation. Run `31275425828` allocated only Linux job `93148087116`, which
passed in 33 seconds with the unchanged lock, static/docs gate, all 361
architecture tests, universal build, isolated-wheel smoke, and complete release
smoke. Desktop umbrella job `93148143924` skipped with zero steps and no runner.
No review, comment, or thread was present. Squash
`deab03fd1f01c3baea8c55494ec1205f53495417` has sole parent the feature squash,
tree `0725d4a05a2033b868e44b050d58023b4cdb61e3` exactly equal to the reviewed
record head, a valid GitHub signature, and a standalone DCO trailer. No post-
merge `main` run was allocated. The record branch is deleted locally and
remotely; only the final `.project/**` closeout record remains.

## M42 complete

M42 starts from exact clean synchronized M41 closeout commit
`0dec2254a9d9483b27d158aaad108340e9c94e28`. It closes the final-state
observation gap after the verified private draft is published. The exact
numeric release database ID now crosses the existing CLI transition and is
fetched once more through the pinned authenticated API.

The internal validator advances to `ludoweave.release-draft-integrity/3` and
requires explicit `draft` or `published` state. Drafts require mutable
prerelease state and null `published_at`; published records require public
prerelease state, a boolean immutable field, and a valid UTC publication time.
Both states retain exact tag, title, bounded notes, and asset verification.

One new read-only postpublication request runs inside the existing tag job.
M42 adds no job, runner, action, permission, trigger, dependency, credential,
tag, release, upload, publication, automatic rollback, or immutable-release
policy. RFC-0025 and the release/security/architecture surfaces document the
boundary. Findings-first review strengthened content-silent published drift and
non-mutation coverage. The complete corrected Python 3.12 suite passes 1,850
tests with 13 expected skips; Python 3.13/3.14 each pass 1,840 with 14 expected
skips. Real wgpu, profiles, vertical slices, reproducible distributions,
installed-wheel smoke, complete release smoke, and exact mutable/immutable
synthetic release states pass. CI, runtime, metadata, dependency, lock,
permission, action, and runner boundaries remain unchanged.

Ready PR #77 exact head `45cd04e627f44400e8bd3adcbeeaf1756160f745`
passed run `31271273535` in exactly three allocations: Linux 6m54s, Windows
3m39s, and macOS 1m59s. No review, issue comment, review comment, or thread was
present. Squash `28dd9d7e282ec85c06b71ed340f3cfcea379d6be` has sole parent the exact
M41 closeout, preserves reviewed tree
`7e65795a6b44de7b3ff393128274eda207c58dc3`, has a valid GitHub signature and
standalone DCO trailer, and allocated no post-merge `main` run. The feature
branch is deleted locally and remotely. Documentation-only PR #78 exact head
`b08c4ff57c2d995fdce73f2e835f2ca3a8075a70` classified four paths as
documentation and passed run `31271986168` in one 33-second Linux allocation;
the desktop umbrella skipped with zero steps and no runner. With no feedback,
it squash-integrated as `35aa6c46f0d128f66535d75dff342f0b7f6bcdeb`, preserving its reviewed tree,
exact feature-squash parent, valid signature, standalone DCO, and zero post-
merge run. Its branch is deleted locally and remotely. Only the zero-run
closeout record remains.

## M41 complete

M41 starts from exact clean synchronized M40 closeout commit
`9983e0da88b6aef999d26498cc6438f0b3c5927b`. It closes the remaining private-
draft metadata gap: the staged release notes already feed
`gh release create --notes-file`, but M40 did not compare the authenticated
release `body` with that source before publication.

The internal validator advances to `ludoweave.release-draft-integrity/2`. It
reads only the fixed staged `RELEASE_NOTES.md` regular non-symlink file, caps it
at 256 KiB, requires non-empty strict UTF-8 without NUL, and rejects any remote
body difference. Missing, null, substituted, truncated, newline-, whitespace-,
or Unicode-different text fails with a stable structured code; note content is
never emitted.

Official GitHub CLI and REST documentation confirms `--notes-file` supplies the
release notes and the authenticated release document exposes them as `body`.
The existing M40 API document and verifier invocation are therefore sufficient:
M41 changes neither workflow file and adds no runner, action, permission,
trigger, dependency, credential, API call, tag, release, or publication
authority. RFC-0024 and the release/security/architecture surfaces now document
the boundary. Focused static checks and 26 behavior/adversarial tests pass with
one Windows symlink-capability skip after correcting a Windows-only byte-fixture
and pytest case-ID defect. Findings-first review then made notes validation
precede asset scanning so a symlinked notes member uses the notes-specific code;
the complete corrected Python 3.12 suite passes 1,830 tests with 13 expected
skips, and Python 3.13/3.14 each pass 1,820 with 13 expected skips. Real wgpu,
profiles, vertical slices, reproducible distributions, installed-wheel smoke,
complete release smoke, and exact synthetic draft verification pass. Workflow,
runtime, metadata, dependency, lock, permission, and runner boundaries remain
unchanged.

Ready PR #74 exact head `ec051d4fd2da80235da1a94642158ebe384cb2b0`
passed run `31269399211` in exactly three allocations: Linux 6m55s,
Windows 2m44s, and macOS 2m12s. No review, comment, or thread was present.
Squash `89a641559c246e971869a3ae06a878de81bffcee` has sole parent the exact M40
closeout, preserves reviewed tree `6446826ee0b35c02dcebc78b9fad3f55caaca0c5`,
has a valid GitHub signature and standalone DCO trailer, and allocated no
post-merge `main` run. The feature branch is deleted locally and remotely.
Documentation-only PR #75 exact head
`d967624c618e433beda1052a7715872b0f256540` classified four paths as
documentation and passed run `31270041957` in one 33-second Linux allocation;
the desktop umbrella skipped with zero steps and no runner. With no feedback,
it squash-integrated as `b05dbda471edf2ac14c5e0b6bf4bd75aaf23f252`,
preserving its reviewed tree, exact feature-squash parent, valid signature,
standalone DCO, and zero post-merge run. Its branch is deleted locally and
remotely. Only the zero-run closeout record remains.

## M40 complete

M40 starts from exact clean synchronized M39 closeout commit
`49fba13477890bf6bf1c9e6a645e669b3a69492f`. It makes the existing GitHub
release CLI's internal draft/upload/publish sequence explicit. The tag job will
create an asset-free prerelease draft, upload the staged set without clobbering,
fetch the draft with REST API version `2026-03-10`, validate it, and only then
publish.

The standard-library validator caps duplicate-free strict JSON, local asset
count, individual and total bytes, safe basenames, and identity fields. It
requires exact tag/title/draft state, a complete duplicate-free remote set,
`state=uploaded`, and exact local/remote names, sizes, and SHA-256 digests.
Success emits only sorted safe identities; failures are structured and leave an
unpublished draft for inspection. The validator owns no network, token, shell,
dynamic import, release mutation, clobber, or cleanup authority.

Focused format/lint/strict-type and 18 behavior/adversarial tests pass with one
Windows symlink-capability skip after one typing/order correction. The explicit
workflow and M38-M40 architecture focus pass 33 tests with the same skip after
one mechanical format correction. Findings-first review then corrected the
draft lookup: GitHub documents the tag-name REST route for published releases,
so the workflow now resolves the authenticated draft's numeric database ID,
validates it, and fetches that exact release by ID.

The complete Python 3.12 suite passes 1,818 tests with 12 expected skips;
Python 3.13 and 3.14 each pass 1,808 with 13 expected skips. Real-wgpu,
base/graphics profiles, Clockwork Arena, Agent World Builder, deterministic
two-build comparison, installed-wheel smoke, ten-artifact release smoke, and a
real-staging synthetic-draft verification all pass. Review found no credential,
archive, native-object, runtime, dependency, lock, or CI drift after the exact
draft-route correction. M40 changes no pull-request CI workflow,
runner/job/matrix count, action, permission, trigger, dependency, lock, package
version, runtime/public API, attestation, tag, release, credential, immutable-
release setting, PyPI configuration, supported release policy, or deferred
subsystem. Final recorded-tree static, architecture, docs, and complete Python
3.12 validation passes. The initial exact implementation head passed all three
hosted allocations, but review correctly found that pathological JSON nesting
and overlong integers could escape as unstructured parser exceptions. No merge
is claimed for that head. The parser correction and both pathological-input
regressions pass focused static/behavior checks, the complete architecture gate,
strict docs, and all 1,818 Python 3.12 tests.

Corrected head `967147b3bbc83414d0ce303845975dea0c4e9d26` passed exact run
`31267396755` in three allocations: Linux 6m43s, macOS 2m51s, and Windows
3m35s. The resolved review thread is outdated and no unresolved thread remains.
Squash `e9d9850e11f572a1d4ddc78d06c79b23a5584f87` has sole parent the exact M39
closeout, tree `974b790ab2d925562185c2c18707f3878b0e7bdd` exactly equal to the
reviewed head, a valid GitHub signature, and standalone DCO trailer. It
allocated no `main` run. The feature branch is deleted locally/remotely; clean
synchronized `main` is the sole branch, no PR, tag, or release is open/present,
and full Git object checking passes.

Documentation-only integration record PR #72 changed four paths and passed run
`31268048294` in one 35-second Linux allocation; the desktop umbrella skipped
with zero steps and no runner. It had no review, comment, or thread. Squash
`67d03d41430dc24bf81a894752b3641de8e521ed` has sole parent the M40 feature
integration, tree `896461bbfd43975ca1ee49962409d9b38695c10f` exactly equal to the
reviewed head, a valid GitHub signature, and standalone DCO trailer. It
allocated no `main` run. The record branch is deleted locally/remotely; before
this closeout branch, clean synchronized `main` was the sole branch, no PR was
open, and full Git object checking passed. Zero-run closeout PR #73 exact head
`e1b07f781096370fa3b6f820bc80dc1d4c585279` changed only three `.project`
paths and had no run, check, review, comment, or thread. Squash
`9983e0da88b6aef999d26498cc6438f0b3c5927b` has sole parent the record
integration, tree `d76b9a348690d6a35af774755cdc4a836240069a` exactly equal to the
reviewed head, a valid GitHub signature, and standalone DCO trailer. It
allocated no `main` run. The closeout branch is deleted locally/remotely; clean
synchronized `main` is the sole branch, no PR, tag, or release is present, and
full Git object checking passes.

## M39 complete

M39 starts from exact clean synchronized M38 closeout commit
`185e206d6b9c1e97512e289bcba84701dc29c147`. It closes the existing gap between
remote tag existence and release identity. The standard-library verifier
requires strict bounded GitHub ref/tag documents, an exact annotated tag whose
signature GitHub reports as valid, matching local/GitHub tag and target commit,
an exact event checkout, and reachability from fetched `origin/main`. Success
emits only safe tag/object/commit/ref identities; signature and payload content
remain private. Structured failures cover malformed/duplicate/oversized input,
identity drift, unsigned/lightweight tags, detached checkout, missing Git state,
and non-main commits.

The existing tag workflow fetches full history/tags, reads the version, obtains
the two read-only GitHub API documents, materializes the verifier from fetched
`origin/main`, and runs it with setup Python before system-package installation,
dependency sync, tests, builds, M38 comparison, staging, attestation, or
publication. GitHub is the signature-verification authority; local Git checks
exact object, checkout, and ancestry identity without a signing-key trust store.
RFC-0022 rejects treating `gh release create --verify-tag` as a signature check
and records the absence of a signer/key allowlist. It also records that the
workflow cannot authenticate replacement of its own definition by an already-
authorized tag actor; tag and environment rules remain operational controls.

Focused behavior, adversarial, static, workflow, and YAML gates passed after one
strict-typing correction, one helper-specificity correction, and two findings-
first workflow trust corrections. Exact head
`f71d8ddbf816873cf9af8ea6538112ff0e75553e` passed hosted run `31264314307`
in exactly three allocations: Linux in 6m43s before macOS and Windows began,
then macOS in 2m33s and Windows in 3m30s. The Linux job passed the full quality,
graphics, sample, distribution, installed-wheel, release-candidate, and CPython
3.13/3.14 gates. No review, comment, or review thread was present.

PR #68 squash `4e30b4bf3b911270ab4e1bd117d49ca0d090a0a7` has sole parent exact M38
closeout, tree `e08a1956e1b6ec9005b1455c5020ee716f6fbdef` exactly equal to the
reviewed feature head, a valid GitHub signature, and a standalone DCO trailer.
No post-merge `main` run was allocated, and the feature branch is deleted
locally and remotely. Public integration-record PR #69 changed exactly four
Markdown paths. Run `31265044941` classified them as documentation and allocated
only Linux job `93121720961`, which passed in 33 seconds; desktop umbrella
`93121781802` skipped with no runner steps. No review, comment, or review thread
was present. Record squash `166dcb2dc619dbc721207eece273c0fd9437f9ff` has sole
parent the implementation squash, tree
`1071165a0bf41397dfbeee38b09eee606299686e` exactly equal to the reviewed
record head, a valid GitHub signature, and a standalone DCO trailer. It
allocated no post-merge `main` run, and the record branch is deleted locally and
remotely.

M39 changes no CI workflow, runner/job/matrix count, action, permission,
trigger, dependency, lock, package version, runtime/public API, attestation,
tag, release, PyPI configuration, supported release policy, or deferred
subsystem. Zero-run closeout PR #70 changed only three `.project` paths, had no
run, review, comment, or thread, and squash-integrated exact head
`4d31f46008bf5efd7475a9b432226748e484d891` as
`49fba13477890bf6bf1c9e6a645e669b3a69492f`. The squash has sole parent the
record integration, tree `46df243de9b6f9f773723412af2580fe8682f27a` exactly equal to the reviewed
head, a valid GitHub signature, and standalone DCO trailer. It allocated no
`main` run. The closeout branch is deleted locally/remotely; clean synchronized
`main` is the sole branch, no PR is open, and full Git object checking passes.

## M38 complete

M38 starts from exact clean synchronized M37 closeout commit
`3578da64b2686cd8d63340aeb1eed30f5c4cb761`. It adds a standard-library,
fail-closed comparison for two distinct wheel/sdist build directories and
wires one repeat build into each existing Linux pull-request and tag-release
distribution step. The verifier requires one matching pure wheel/source pair,
ordinary files, exact bytes, and deterministic JSON identities. Invalid entry
types, missing/extra artifacts, inconsistent or platform-specific names,
unreadable data, and byte divergence fail nonzero.

The existing same-source build probe produces exact matching wheel and sdist
bytes on Windows. Corrected focused tests cover valid output and adversarial
directory, name, artifact-set, byte, unreadable-directory, and symlink-cycle
cases. CI/release architecture tests preserve the M37 two-job/three-allocation
pull-request topology, one-job tag workflow, exact action pins, existing
permissions, and triggers. RFC-0021 and public release/architecture
documentation define the narrow same-source/same-job guarantee.

PR #65 review identified that `Path.resolve(strict=True)` raises
`RuntimeError`, rather than `OSError`, for a symlink loop. DCO-signed correction
`4f3db7446c842df4f36d7cc8f8321a89bbe5997f` returns the promised structured
invalid-directory failure and adds a capability-aware regression. Replacement
run `31261807768` passed exact corrected head in exactly three allocations:
Linux in 6m50s, macOS in 1m59s, and Windows in 3m44s. Linux passed before either
desktop allocation began. Its same-source rebuild comparison reported a
266,797-byte wheel at SHA-256
`6c43bb79ed5de115ee645f1c8a9b4e8338f364c5bb1f53e08cde58e82e9afe06`
and an 892,185-byte sdist at SHA-256
`8f21585819f76f289887a6194e44bcf06b72497d70d13451326cc778e48e4f8a`.
All expected steps passed; the sole review thread is resolved and outdated.

PR #65 squash `9f6ca61ccb1f9b7e0796e5cc60c7dd38e6af99d7` has sole parent exact M37
closeout, tree `1a96d02b8b23410732fc7ac746179459a14d3f44` exactly equal to the reviewed
feature head, a valid GitHub signature, and a parsed DCO trailer. The feature
branch is deleted locally and remotely, synchronized main contains the squash,
and no post-merge main run was allocated.

Public record PR #66 changed exactly four Markdown paths. Its exact committed
classifier result was `classification=documentation`, `substantive=false`, and
`changed_count=4`. Hosted run `31262609814` allocated only Linux, which passed
the complete bounded documentation gate in 32 seconds. GitHub skipped the
desktop matrix before expansion in zero seconds; its umbrella check had no
runner steps. Record squash `42046d521242147cc5ed56874238d25de9870316`
has exact sole parent the feature squash, tree
`0776afee4c20884240cd4828095ac3b03ae46423` exactly equal to the reviewed
record head, a valid GitHub signature, and a parsed DCO trailer. PR #66 had no
comment, review, or review thread. The record branch is deleted locally and
remotely, synchronized main contains both M38 squashes, and no post-merge main
run was allocated.

M38 changes no runtime, public API, dependency, lock, version, supported
platform/Python contract, attestation action/permission, tag, publication, or
deferred subsystem. Its guarantee remains same-source/same-job byte equality,
not cross-platform, hermetic, independent-rebuilder, provenance, certification,
or publication evidence.

## M37 complete

M37 starts from exact clean synchronized M36 integration-record commit
`46ef98447706c94763a236841a38c2dbb5b444ca`. Its bounded outcome is fail-closed
change qualification inside the existing Linux CI allocation. A classifier
loaded from the exact base revision admits only a narrow documentation/community
path set; empty, mixed, ambiguous, invalid, unknown, or indeterminate input is
substantive or blocks the Linux gate. Documentation-only work retains one Linux
lock/static/docs/architecture/build/wheel/release allocation. Substantive work
retains all eight M36 slices and three allocations, with Windows/macOS gated on
successful Linux `substantive=true` output.

RFC-0020 and the public architecture, maintenance, roadmap, changelog, and
README contracts describe the policy and tradeoff. Findings-first review
closed one valid executable-documentation bypass by restricting `docs/` and
`.project/` to Markdown and making `mkdocs.yml` substantive. PR #62 review then
identified that the pull-request-template allowlist used the wrong filename
case; signed correction `8214227c99831310546147977bf354b5ae956bce` aligned it
with the tracked lowercase path and updated the regression fixture. The only
review thread is outdated and resolved.

Corrected substantive run `31259200818` passed exact head
`8214227c99831310546147977bf354b5ae956bce` in three allocations. Linux passed
all qualification, quality, compatibility, graphics, vertical-slice, and
distribution steps in 6m48s; only then did Windows and macOS start, passing in
3m40s and 2m45s. Feature squash
`407226beae36182d237e32866a86ce19bb93c691` has the exact reviewed tree, exact
M36-record parent, a valid GitHub signature, and a parsed DCO trailer. PR #62
and its feature branch are closed/deleted, synchronized main contains the
feature squash, and no main-branch run was allocated.

Public record PR #63 changed exactly four admitted Markdown paths. Its exact
committed classifier result was `classification=documentation`,
`substantive=false`, and `changed_count=4`. Hosted run `31259908552` allocated
only Linux, which passed the complete bounded documentation gate in 32 seconds.
GitHub evaluated the desktop job condition before matrix expansion and emitted
one skipped matrix-umbrella check with no steps and no Windows/macOS runner
allocation. Record squash `7434f310c86dd9acf6c61ff01c1a5f2dfcdffe31`
has exact reviewed tree `9dc7f0bc50b7b5b8309405ce491978f3ef39cbe4`, sole feature-squash parent, a
valid GitHub signature, and a parsed DCO trailer. The PR and branch are deleted,
main is synchronized, and no main-branch run was allocated.

M37 changes no runtime, test behavior, dependency, lock, package version,
release workflow, supported platform/version, tag, publication, provider,
certification, or support policy.

## M36 complete

M36 starts from exact clean synchronized M35 integration-record commit
`ba9125389ab2b2b760ca7115b5b1b03c447f4190`. It changes CI orchestration only:
the same eight validation slices move from eight runner allocations to three
OS-owned allocations. One Ubuntu runner owns CPython 3.12 quality,
distribution, base/graphics profiling, real graphics, and the sequential 3.13/
3.14 compatibility slices. A two-entry desktop matrix gives Windows and macOS
one runner each for 3.12 graphics followed by 3.14 compatibility.

The structural target is five fewer runner allocations and five fewer repeated
checkout/setup sequences, not removal of coverage. PR-only and `.project/**`
filters, least privilege, disabled credential persistence, exact pins, frozen
lock, caching, timeouts, desktop failure isolation, and superseded-run
cancellation remain. Runtime, tests, dependencies, lock, package version,
release workflow, public contracts, supported platforms/versions, tag,
publication, and support policy remain unchanged. Workflow implementation,
architecture regressions, RFC-0019, and documentation are integrated. Exact
sequential 3.13 and 3.14
transitions pass complete 1,714-test suites on Windows; restored 3.12 passes
1,724 tests. Static/docs/YAML, distribution, isolated wheel/release, real-
wgpu/profile, vertical-slice, and focused workflow/release gates pass.
Findings-first review moved compatibility-interpreter installation before
expensive work. Scope/security and final implementation-tree 1,724-test gates
pass; only factual `.project/**` rows followed.

Ready PR #60 used exact base
`ba9125389ab2b2b760ca7115b5b1b03c447f4190` and DCO-signed final head
`38589bbe6b4c688b581bc972f0ba1e4e39d5cd93`. Pull-request run `31232803658`
passed exactly three hosted allocations: Linux in 6m36s, Windows in 3m32s, and
macOS in 2m16s. Its step-level evidence covers every retained quality,
distribution, compatibility, real-graphics, profiling, and vertical-slice
gate. GitHub reported the PR mergeable and clean, with no comment, review, or
review thread. PR #60 squash-integrated the exact feature tree
`39d29fa863fee46665bf02856f4d9657068b573f` as GitHub-verified commit
`0b8b39052d79ee9c8a2f909f8ac70045adf5a785`, with sole parent exact base and a
valid DCO trailer. The feature branch is deleted locally and remotely. The
PR-only workflow scheduled no post-merge `main` run; the latest listed main run
remains pre-M34 run `31226750474`.

## M35 complete

M35 starts from exact clean synchronized M34 integration-record commit
`277de9052e768a5f70d32f1a2f67ec9f93353723`. Its bounded outcome is strict
offline admission readiness for the design plan's final ordered longer-term
metric: independently authored third-party adapters or plugin-backed adapters
passing existing installed conformance. The exact reviewed 250-byte manifest
has SHA-256
`adee8c68b5d89923ee2682162eb24cd9542a4601b1ff6fb901709ebcc0066767`,
explicitly asserts complete review of the project-accepted submission census,
and contains no submissions. The current passing count is therefore zero; no
global package census, ecosystem adoption, support matrix, security,
performance, provider certification, or release gate is claimed.

Future admission is limited to distinct independent external implementation
identities using the exact installed M17 render-device, M18 agent-tool, or M19
WorldStore baseline and fixed check count. Project-owned and maintainer-
authored implementations are excluded before outcome. A plugin-backed record
is possible only for the existing M12 `render.device` capability and requires
both compatible reviewed inert-manifest evidence and a passing installed
render-device result. Passed, failed, and not-executed submissions remain in
complete accepted history; only passes count. Public immutable wheels,
revisions, reports, reviews, supported CPython/platform evidence, and explicit
authorship/independence/license/eligibility/outcome/provenance/validation/
privacy/consent review are required.

The evaluator is an explicitly invoked bounded offline reader outside the
runtime package. It performs no discovery, import, install, provider execution,
network request, sandboxing, or telemetry and emits only sanitized aggregates.
M35 changes no runtime source, public API/export, protocol/profile, plugin
field, format, dependency, lock, version, CI topology, release workflow, tag,
publication, certification, or support policy. Implementation and focused
evaluator tests exist on `evidence/m35-third-party-conformance`. Findings-first
review hardened public evidence against reserved non-public domains and non-
wheel paths. The complete local gate passes 1,716 tests with nine skips, strict
static/docs checks, universal build, installed wheel/release smoke, real-wgpu/
profile and vertical-slice checks, and scope/security/artifact audits. Hosted
run `31231040437` passed all eight essential jobs on the initial head, but
automated review found that its generic identifier grammar disagreed with the
exact shared M17-M19 adapter grammar. The correction uses the installed runner
grammar for equal implementation/adapter identities; 100 focused tests, the
complete 1,718-test suite, strict static/docs gates, real-wgpu, rebuilt wheel,
isolated-wheel smoke, and fresh release smoke pass. Corrected hosted validation
run `31231410432` passed all eight essential jobs on exact final head
`fb0d887eed80a2d96c4b3348d950df371e58db56`. The correction evidence was
posted and the sole review thread resolved. PR #58 squash-integrated the exact
final tree as GitHub-verified commit
`603403967e333342c5ff72222ea3567d3252fd6f`, with sole parent exact base
`277de9052e768a5f70d32f1a2f67ec9f93353723`, tree
`59c049ebdb957818aba2252c74d5b5f8ef9cb72f`, and a valid standalone DCO
trailer. Local and remote feature branches are deleted. The PR-only workflow
created no post-merge `main` run; the latest listed main run remains pre-M34
run `31226750474`.

## M34 complete

M34 starts from exact clean synchronized M33 integration-record commit
`d12c30a02782c0ebf892e27c5daf6e9fec1c93ee`. Its bounded outcome is strict
offline admission readiness for the percentage of agent tool calls that
complete without manual recovery, plus the directly authorized elimination of
redundant CI runs. The reviewed 195-byte manifest contains no evaluation
windows and has SHA-256
`e952c045b039055e8439069cf88176b6ac1d2ad7de49a94d39b2737e5d06e1d5`, so
no call count, manual-recovery count, recovery-free completion rate,
reliability result, certification, or release gate is claimed.

Future admission requires every dispatched call from a complete reviewed
cohort of eligible task-directed sessions. It freezes the exact 12 product
tools and `ludoweave.agent.service/1`, immutable service/dispatch/result/
recovery evidence, sequential per-session indices, canonical order, complete
history, and explicit privacy/consent plus behavioral reviews. Known non-
completions and calls completed after
manual recovery remain in the denominator; `terminal-unobserved` remains
counted and blocks publication. Synthetic fixtures, conformance, tests,
benchmarks, maintainer-driven calls, and unreviewed/private sessions are
ineligible. Aggregate output omits raw sessions, tools, prompts, arguments,
results, errors, and evidence locations.

The eight existing CI jobs remain the substantive supported Python/OS/
graphics/distribution gate. M34 changes only their trigger: substantive pull
requests run the gate once; the same tree is not rerun after merging to
unprotected `main`, and `.project/**`-only factual record pull requests use no
hosted runner. Runtime, agent tools/protocols, public APIs, formats,
dependencies, lock, version, release workflow, providers, telemetry, and
native/WASM surfaces remain unchanged. Implementation, the 1,624-test complete
suite, strict static/docs gates, universal build, isolated wheel/release smoke,
real-wgpu/vertical-slice checks, scope/security audits, and findings-first
review pass on `evidence/m34-agent-tool-recovery`. Initial hosted run
`31228373123` failed one missing-manifest regression on Ubuntu and macOS because
the uncaught chained traceback disclosed the test path; the Windows
compatibility and all three graphics jobs passed. Delayed review also found
that sufficiently deep JSON could escape through `RecursionError`. The CLI now
prints only its sanitized outer error, and both parser and recursive depth-walk
exhaustion normalize to the documented validation error. Regressions cover no
traceback and excessive nesting. The corrected local gate passes 1,625 tests
with nine skips, strict static/docs checks, a universal build, isolated wheel
smoke, and a fresh ten-artifact release smoke. Corrected hosted run
`31229138742` passed all eight jobs on exact head
`600f71a416f0df46af68e63d28a2711893ec4675`: quality/tests/distribution;
Ubuntu CPython 3.13 and 3.14; Windows and macOS CPython 3.14; and real graphics
on Ubuntu, Windows, and macOS. The sole review finding was acknowledged and its
thread resolved; GitHub reported PR #56 mergeable and clean. PR #56
squash-integrated the exact validated tree as GitHub-verified commit
`a0d80851821b569156979d8d2ae0e473cea768f9` with sole parent exact base
`d12c30a02782c0ebf892e27c5daf6e9fec1c93ee`. Both source commits are
DCO-signed and remain attached to the PR. GitHub's squash body retained literal
escaped newline text before its displayed sign-off, so this record does not
claim the generated squash commit has a parsed DCO trailer and does not rewrite
public history. The remote and local feature branches are deleted. The new
PR-only trigger created no redundant post-merge `main` run; the latest listed
main run remains pre-M34 run `31226750474`.

## M33 complete

M33 starts from exact clean synchronized M32 integration-record commit
`60ddf57216d1054ac44df8d834756312c3864e3e`. Its bounded outcome is strict
offline admission readiness for benchmark-regression rate. The reviewed
manifest contains no evaluation windows, so no comparison count, regression
count, rate, zero-regression result, performance verdict, native decision, or
release gate is claimed. Future admission is restricted to registered M1-M4
`time.perf_counter_ns` p95 workload pairs on reviewed comparable controlled
runner profiles with distinct base/head revisions, exact sources/artifacts,
and predeclared integer tolerances. M7 cProfile output is diagnostic and
ineligible. Stable, regressed, and not-executed outcomes are preserved;
non-execution blocks rate publication. No runtime/benchmark source, API,
protocol, format, dependency, lock, version, workflow, provider, telemetry, or
native/WASM boundary changes. The exact 199-byte manifest SHA-256 is
`720ae794e2a4ba76303196cd43d6ba0f3b21f81cffd4fa8584f526e2a0d48dca`.
Implementation, adversarial tests, distribution wiring, RFC-0016, and public
documentation exist on `evidence/m33-benchmark-regression-rate`. Complete local
static/docs/test/build/wheel/release/benchmark/profile/graphics validation and
findings-first review pass. Protected-surface, archive, credential-pattern,
neutral-metadata, and object-integrity audits pass. Ready PR #54 exact head
`3bd7e17eed26028592cb39d37e77e15c6f4371f1` passed all eight essential jobs in
hosted run `31225942698`; no comment, review, or review thread existed and
GitHub reported the PR mergeable/clean. PR #54 squash-integrated the exact
validated tree as GitHub-verified `main` commit
`0993c73b3290809ef4e0c36d64d39e5ee5891a9b` with sole parent exact M33 base
`60ddf57216d1054ac44df8d834756312c3864e3e` and DCO trailer. The feature branch
was deleted locally and remotely. Synchronized `main` remains at the verified
feature squash while this documentation-only `records/m33-integration` branch
and PR #55 await their own hosted gate. M33 feature work is complete; no
measured rate, release, publication, performance guarantee, or native-code
authorization is claimed.

## Current milestone

M32 is complete, hosted-validated, reviewed, squash-integrated, and cleaned up.
It started from exact clean synchronized verified `main` commit
`b4de1d115ddb620ecddccab84637c0e66cfad9fd`. Its bounded outcome is a strict
offline admission harness for the design plan's next longer-term metric:
replay-divergence rate in CI. The reviewed manifest contains no evaluation
windows, so no execution count, divergence count, rate, reliability result, or
release gate is claimed. A future admitted window requires a complete reviewed
public cohort of eligible CI replay executions started during a bounded
interval and preserves verified, diverged, and not-executed cases. Cancellation,
pre-replay failure, skips, and unavailable result evidence cannot disappear
from the cohort. Each execution binds canonical project workflow run/job
locations, exact head/workflow/case sources, UTC time, and frozen result
evidence. Verified outcomes require equal expected/actual hashes; divergences
require distinct hashes, first divergent tick, and the stable divergence code;
non-execution claims no replay hashes or tick. Public census and review
artifacts share one immutable project revision. Manual review owns cohort
completeness, eligibility, outcome, provenance, and validation. Only exact
reviewed whole-manifest identity and complete mandatory history expose admitted
counts; an exact numerator/denominator rate additionally requires a non-empty
cohort with no non-executed case. `ready` means reportable, not that any
threshold, quality target, release gate, reliability promise, SLA, or support
promise is met. M32 changes no runtime source, replay behavior, public API/
export, persistent format, protocol, operation, dependency, lock, package
version, stability label, workflow, CI topology, tag, release, publication,
certification, reliability target, SLA, or support policy. The manifest is
exactly 175 bytes with SHA-256
`cff8a32428ac8dcd18029be4f70e9d359b4c9d70fd411ffe2f36d35704d68aa7`.
The evaluator, exact validator, adversarial future/non-execution/history
regressions, source/wheel/release artifact wiring, RFC-0015, and public
documentation are complete. Findings-first review corrected noncanonical case-
source URL acceptance and fixed eligibility before outcomes to exclude
intentionally divergent negative fixtures and verification-disabled diagnostic
runs. The reviewed tree passes the unchanged 46-package lock, 255-file
formatting, Ruff, strict Pyright, strict docs, 1,498 tests with nine platform-
capability skips, pure build, isolated wheel/release smoke, ten real-wgpu tests,
and both graphics vertical slices. The 94-entry wheel remains universal pure
Python with no native/WASM file; the 44-entry sample bundle contains the exact
evaluator and manifest. Protected runtime/workflow/metadata/lock scope remains
unchanged. Ready PR #52 is published. Initial exact PR head
`7046e59eb4840e6df492c886ce78baf4ad51cd95` passed all eight hosted jobs, but
hosted review correctly found the evaluator required nonexistent diagnostic
`world.replay.divergence` instead of the runtime's `world.replay.diverged`.
Evaluator, fixture, docs, and an architecture regression are corrected. The
post-review gate passes 80 focused tests with one skip, 1,499 complete-suite
tests with nine skips, 255-file formatting, Ruff, strict Pyright, strict docs,
the unchanged lock, protected-surface and whitespace checks, pure build,
isolated-wheel smoke, and a fresh ten-artifact release smoke. Corrected hosted
head `f6f574c2e9b54341e77d1b9ba2d9268bffe5439a` passed all eight essential jobs
in run `31195402467`, and the sole hosted-review thread is resolved and
outdated. PR #52 squash-integrated exact tree
`e185e24861b74fe11325b7188026af29a9618926` as GitHub-verified commit
`36e8d9ed65a619569f3620b2431d977a1fb80a58` with sole parent
`b4de1d115ddb620ecddccab84637c0e66cfad9fd` and its DCO trailer. The temporary
feature branch is deleted locally and remotely. No benchmark was rerun because
M32 changes no runtime or performance path and defines no performance target.

M31 is complete, hosted-validated, reviewed, squash-integrated, and cleaned up.
It started from exact clean synchronized verified `main` commit
`22dc58df8b0c4d17c3619d83e37c6d0ee6184441`. Its bounded outcome is a strict
offline admission harness for the design plan's next longer-term metric:
issue-response and pull-request-review time. The reviewed manifest contains no
measurement windows, so no cohort, response/review count, latency aggregate,
responsiveness result, or SLA is claimed. A future admitted window requires a
complete reviewed public cohort of eligible external-human issues and pull
requests opened during a bounded interval, preserves both observed and pending
items, and binds first qualifying public human-maintainer actions to exact
resource/action locations, UTC timestamp/latency agreement, frozen source and
review identities, and reviewed eligibility, role, distinctness, provenance,
and validation. Public census and review artifacts must share one immutable
project revision. Only exact reviewed whole-manifest identity and complete
mandatory history expose aggregate eligible/observed/pending counts and
deterministic median/nearest-rank-p95 seconds. `ready` means reportable, not
that any threshold, quality target, release gate, SLA, or support promise is
met. M31 changes no runtime source, public API/export, persistent format,
protocol, operation, dependency, lock, package version, stability label,
workflow, CI topology, tag, release, publication, certification, SLA, or
support policy. The manifest is exactly 199 bytes with SHA-256
`bc40bbcc1636229fa2c78aed5f71854d1221fd3c0d33169edc1321dd07e69d4f`.
The evaluator, exact validator, adversarial future/pending/history regressions,
source/wheel/release artifact wiring, RFC-0014, and public documentation are
complete. The corrected focused evaluator gate passes 49 tests with one Windows
symlink-capability skip; the evaluator/artifact group passes 51 tests with the
same skip; and the corrected architecture/evaluator/artifact gate passes 62
tests with one skip and strict docs. The final complete gate passes the
unchanged lock/sync, 251-file formatting, Ruff, strict Pyright, strict docs,
1,435 tests with eight skips, pure build, isolated wheel/release smoke, ten
real-wgpu tests, and both graphics vertical slices. Protected runtime/workflow/
metadata/lock scope is unchanged; the unchanged 94-entry wheel has no native/
WASM file and the 42-entry sample bundle contains both exact M31 evidence
files. Findings-first local review found no issue. Ready PR #50's initial exact
head passed all eight hosted jobs in run `31189729885`, but the hosted review
correctly found that equality between the observation cutoff and the opening-
window close was admitted. The evaluator now requires a strictly later cutoff,
equality has an explicit regression, and the public admission text is aligned.
The post-review gate passes 60 focused tests with one skip, formatting, Ruff,
strict Pyright, strict docs, 1,435 complete-suite tests with eight skips, pure
build, installed-wheel smoke, and fresh ten-artifact release smoke. No
benchmark was run because M31 changes no runtime/performance path and defines
no timing target. Corrected exact head
`dd4058b71439b5bade9d091831ba5453a51db35c` passed all eight essential jobs in
run `31190559197`. The sole review thread is resolved and outdated, no
unresolved thread or top-level comment remains, and PR #50 was `MERGEABLE` and
`CLEAN`. PR #50 squash-integrated exact tree
`2ec80742556e62b34dc9275fd0b268a484e9eace` as GitHub-verified commit
`8adb8d46d0ce13ea3687856ae53e899e98dc42a6` with sole parent
`22dc58df8b0c4d17c3619d83e37c6d0ee6184441`. Literal tree comparison and object
integrity passed. The temporary feature branch is deleted locally and remotely;
no feature PR remains open. M0-M31 are complete; select the next bounded slice
from current authoritative project goals before changing runtime scope.

M30 is complete, hosted-validated, reviewed, and squash-integrated by PR #48 as
GitHub-verified `main` commit
`675713d15a20a38233b80580e5aa773dc7a8684c`. It started from exact clean
synchronized verified `main` commit
`c88b166a39a793c91741bfa762af5627a87c53b4`. Its bounded outcome is a strict
offline admission harness for the design plan's next longer-term metric:
installation success across the supported OS/CPython matrix. The reviewed
manifest contains zero records, so the successful-environment count remains
zero and the sanitized result is deterministically `not-ready`; source-checkout
CI, local builds, automation, downloads, and synthetic fixtures do not
establish clean installation of one immutable public release wheel. A future
true result requires the same canonical public pure-Python wheel to pass fresh
isolated installs on Ubuntu CPython 3.12/3.13/3.14 and macOS/Windows CPython
3.12/3.14, with no dependencies or native compiler, all four installed checks,
distinct log identities, canonical provenance, and reviewed validation. The
complete reviewed identity sequence must equal the executable mandatory
prefix. Candidate or history-incomplete manifests expose no record-derived
environment or release aggregates. M30 changes no runtime source, public
API/export, persistent format, protocol, dependency, lock, package version,
stability label, workflow, CI topology, tag, release, publication, or support
policy. The manifest is exactly 462 bytes with SHA-256
`7c05813a7304e8ff44a009ada37c8e60ff545baec633852fc332e46bdfe03c90`.
The evaluator, exact validator, initial fail-closed regressions, source/wheel/
release artifact wiring, RFC-0013, and public documentation are complete.
Findings-first review corrected the canonical GitHub asset download path,
required unique public validation-job locators, enforced canonical environment
order, and added real calendar validation. The corrected focused gate passes
56 evaluator/architecture/artifact tests with one Windows symlink-capability
skip. The final complete gate passes the unchanged lock/sync, 247-file
formatting, Ruff, strict Pyright, strict docs, 1,375 tests with seven skips,
pure build, isolated wheel/release smoke, ten real-wgpu tests, and both graphics
vertical slices. Protected runtime/workflow/metadata/lock scope is unchanged;
the 94-entry wheel has no native/WASM file and the 40-entry sample bundle
contains both exact M30 evidence files. No benchmark was run because M30
changes no runtime/performance path and makes no performance claim. Ready PR
#48 contained single DCO-signed feature commit
`576dd070b547bef853ee47ece4c928b4e9962a7d`; hosted run `31186083454` passed
all eight essential jobs on that exact head. The final GitHub audit found zero
reviews, zero review threads, and eight successful checks. PR #48
squash-integrated exact feature tree
`6c421ece852d822270f3de1e9ece9c7cc1568678` as verified commit
`675713d15a20a38233b80580e5aa773dc7a8684c` with sole parent
`c88b166a39a793c91741bfa762af5627a87c53b4`; the feature branch is deleted
locally and remotely.

M29 is complete, hosted-validated, and squash-integrated. It started from exact
clean synchronized verified `main` commit
`e4125bf31a751473d2af4fecc05a9744d551063c`. Its bounded outcome is a strict
offline admission harness for the design plan's next longer-term metric:
contributor retention rather than raw stars. The reviewed manifest contains
zero records, so retained-contributor and return-contribution counts remain
zero and the sanitized result is deterministically `not-ready`; maintainers,
non-human automation, CI, stars, forks, downloads, and synthetic fixtures do not
establish retention. A future true result requires the same independently
reviewed external human to complete a first and later return contribution with
distinct public issues and merged pull requests, exact Git and artifact
identities, canonical chronology, valid DCO, complete validation, reviewed
provenance, and explicit human review of identity, independence, same-person
continuity, chronology, and retention. The complete reviewed identity sequence
must equal the executable mandatory prefix. Candidate or history-incomplete
manifests expose no record-derived counts or scopes. M29 changes no runtime
source, public API/export, persistent format, protocol, dependency, lock,
package version, stability label, workflow, or CI topology. The manifest is
exactly 274 bytes with SHA-256
`61785ec165e9f9a7c1025c37f7b714d6fa42b2c7081145a0f843395a325b36ee`.
The evaluator, exact validator, initial fail-closed regressions, artifact
wiring, RFC-0012, and public documentation are complete. They are accompanied
by the user-authorized neutral
repository convention: maintenance guidance now lives in `MAINTAINERS.md`, and
current state, decisions, templates, and reproducible evidence live under
`.project/`. This path migration changes no authorship or historical fact.
Findings-first review
closed case-variant double counting, made popularity-field rejection explicit,
required ASCII canonical timestamps, and made excessive JSON nesting fail
closed. Ready PR #46's initial hosted run `31181308306` passed five essential
jobs but exposed one CPython 3.14 decoder-behavior assumption in all three
compatibility jobs. The corrected evaluator now applies an explicit,
parser-independent 16-level structural nesting limit while ignoring JSON
string contents and escapes. Focused CPython 3.12 and 3.14 suites each pass 56
tests with one Windows capability skip. Complete local CPython 3.12 and 3.14
suites pass 1,321 tests with six skips and 1,311 tests with seven skips,
respectively. The complete local gate also passes 243-file formatting, Ruff,
strict Pyright, strict docs, pure build, isolated wheel/release smoke, all retained
benchmark/profile validators, ten real-wgpu tests, and both graphics vertical
slices. Protected runtime/workflow/metadata/lock scope is unchanged; the
94-entry wheel has no native library and the 38-entry sample bundle contains
both exact M29 evidence files. Correction run `31183032073` passed all eight
essential jobs on DCO-signed head
`897a3db5b0901835c6929eda5f94ed1774afac16`. The final audit found no review
thread or actionable finding, and GitHub reported PR #46 `MERGEABLE` and
`CLEAN`. PR #46 squash-integrated the exact corrected tree as GitHub-verified
commit `fc969a981ecdbbf842477f46486e29277119e05b`; its sole parent is the
assigned base and its tree is
`d98c25f156aaeee863ff8dc88b00355daa921d2e`. The obsolete feature branch is
deleted locally and remotely.

M28 is complete, independently reviewed, hosted-validated, and squash-
integrated. It started from exact clean synchronized GitHub-verified `main` commit
`17401eb32be30862496bbe02366d886a60752fb3`. Its bounded outcome is a strict
offline admission harness for the design plan's longer-term metric counting
externally authored sample games. The reviewed manifest contains zero records,
so the current count remains zero and the sanitized result is deterministically
`not-ready`; project examples, maintainers, project-controlled automation, CI,
and synthetic fixtures do not establish adoption. A future true result requires manually
reviewed independent authorship, a public repository and immutable revision,
an installed-wheel 2D/layered-2D game, exact headless fixed-tick, typed command-
receipt, and verified-replay capability evidence, distinct source/execution/
review artifact identities, a validated outcome, and reviewed public licensing.
The complete reviewed identity sequence must equal the executable mandatory
prefix. M28 changes no runtime source, public API/export, persistent format,
protocol, dependency, lock, package version, stability label, workflow, or CI
topology. The initial baseline resolves the unchanged 46-package lock and
passes 94 related tests with two Windows symlink-capability skips. The reviewed
manifest is exactly 280 bytes with SHA-256
`ecdd0be75e42f047037c6799205786079274eb6d73d788f81e1061acc82008dd`.
The evaluator, exact validator, synthetic regressions, source/wheel/release
artifact paths, RFC-0011, and public documentation are complete. Findings-
first review added explicit independence/provenance/outcome attestations,
cross-role artifact and locator uniqueness, duplicate-field rejection,
resource bounds, and complete mandatory-prefix enforcement. Corrected focused
validation initially passed 56 tests with one Windows symlink-capability skip.
Ready PR #44 and run `31175906134` passed all eight unchanged essential jobs on
DCO-signed head `a1898a81218ae5674fd0347018c6062a5537f359`. Thread-aware
review then found two valid P2 issues: unreviewed manifests could publish
candidate game/author aggregates, and HTTPS evidence locators were not bound
to an immutable record identity. The corrected evaluator exposes aggregates
only after exact digest and complete-history admission and requires the
locator path to contain the revision or one source/execution/review digest.
Post-correction formatting, Ruff, strict Pyright, strict docs, 57 focused
tests with one skip, 1,265 full tests with five skips, pure build, isolated
wheel smoke, and fresh ten-artifact release smoke pass. Correction run
`31176729893` also passes all eight unchanged essential jobs on exact head
`36130c8a3d0923a7330ee2c9e287c11c2a52594c`. GitHub reports PR #44
`MERGEABLE` and `CLEAN`; both original P2 threads are outdated, and the final
thread-aware reread found no new finding. The factual `[skip ci]` final head
`c383a4f143fd8682059a89ff6b645104a6b4332d` created no third workflow run.
PR #44 squash-integrated that exact head as GitHub-verified commit
`90d58a4567e7c7eaff90a28a7c59f2453b6d4538`; both trees are
`2f5ebf96af70741deb8d2b7d18ffa6d84effc494`, its sole parent is the assigned
base, and the squash message retains DCO sign-off.

M27 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on
`[historical branch name redacted]` from exact clean
synchronized GitHub-verified `main` commit
`c1c3be08f7f75d90e7d1b517adbc30d56902ece4`. Its bounded outcome is a strict
offline admission harness for the design-plan objective that documentation
enable a first external contribution without private maintainer knowledge.
The reviewed manifest contains zero records, so the sanitized result is
deterministically `not-ready`; project documentation, hosted CI, maintainers,
non-human automation and synthetic fixtures do not establish an independent
human contribution rehearsal. A future true result requires at least one manually
reviewed human good-first contribution linked to a public project issue and
merged pull request, exact base/head/merge objects, patch/feedback hashes,
valid DCO, the clean/focused/complete validation sequence, and explicit review
that no private maintainer knowledge or protected API/format/dependency/workflow
change was involved. The complete reviewed identity sequence must equal the
executable mandatory prefix. M27 changes no runtime source, public API/export,
persistent format, protocol, dependency, lock, package version, stability
label, workflow, or CI topology. The manifest is exactly 270 bytes with
SHA-256 `ecb959e90a0033b4dbe3dcfe8a48db1c1eea915e0ef2840510969b9e25cdb9c7`.
The core focused suite passed 51 tests with one Windows symlink-capability skip
in 1.74 seconds; source/wheel/release artifact wiring then passed 53 tests with
one skip in 2.02 seconds, Ruff passed after import ordering was corrected, and
Pyright reported zero diagnostics. Findings-first review then closed cross-role
revision/artifact reuse and duplicate-JSON-field ambiguity; 59 corrected
focused tests pass with one skip. The complete local gate passes 235-file
formatting, Ruff, strict Pyright, strict docs, 1,210 tests with four Windows
symlink-capability skips, pure build, isolated wheel/release smoke, all retained
benchmark/profile validators, ten real-wgpu tests, and both graphics vertical
slices. Protected runtime/workflow/metadata/lock scope is unchanged; the
94-entry wheel has no native library and the 34-entry sample bundle contains
both M27 evidence files. Initial hosted run `31118834216` found that the M27
architecture test spelled the tracked lowercase pull-request template with an
uppercase filename; both Ubuntu compatibility jobs failed that same case-
sensitive lookup. The local correction uses the exact tracked path. Windows
graphics separately failed during GitHub action-download resolution before
checkout with `Service Unavailable`; macOS graphics passed. The already-failed
run was cancelled rather than spending its remaining queued jobs. Corrected
run `31119640551` first preserved three successful jobs while four jobs failed
before checkout and macOS graphics remained unassigned during GitHub's
subsequently resolved Actions outage. One failed-job-only rerun then executed
only the five affected jobs. The resulting effective eight-job matrix is fully
successful on exact corrected head
`f9e779d83a82795ad68cff22c424b6e94ef13703`: quality/distribution, Ubuntu
3.13/3.14, Windows 3.14, macOS 3.14, and graphics on Ubuntu, Windows, and
macOS all pass.

The final evidence commit used `[skip ci]` and created no additional workflow
run. The final thread-aware reread found one unresolved bot comment that
mistook GitHub's ephemeral PR test-merge commit for a branch commit; every
branch commit has the required DCO trailer, so the finding is not actionable
and was neither answered nor resolved. PR #42 squash-integrated exact final
evidence head `349dc3b78dcae2b1c725ed3dc8e5e646ca3d3ac1` as GitHub-verified
`main` commit `ff1c81f8aaa96245706586096f400a5fb03bdd04`. Both trees are
`f957c2e40eec5bd2d70cc274079ea334d6a34cc3`; the squash commit has exact
assigned base `c1c3be08f7f75d90e7d1b517adbc30d56902ece4` as its sole parent
and carries the DCO sign-off. The milestone branch remains the audit trail.

M26 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on `[historical branch name redacted]` from exact clean
synchronized `main` commit
`0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62`. Its bounded outcome is a strict
offline admission harness for RFC-0003 gate 6. The current reviewed manifest is
empty, so the sanitized result is deterministically `not-ready`: the tag-only
prerelease workflow, local candidates, CI, and synthetic records do not establish
a supported deprecation-capable feature-release channel. A future gate requires
at least two reviewed supported non-yanked final releases on distinct feature
lines, exact publication identities, the one-feature-release deprecation window,
and append-only history. M26 changes no runtime source, public API/export,
protocol, dependency, lock, package version, stability label, release workflow,
or CI topology. The manifest is exactly 278 bytes with SHA-256
`f23b4314696384ad288b86c63bc101606f1aa9f323c4fb186486d8c74915ec41`;
findings-first review hardened exact project-tag URLs, final-release state, and
publication identity. The complete local gate passes 231-file formatting,
Ruff, strict Pyright, strict docs, 1,152 tests with three Windows symlink-
capability skips, pure build, isolated wheel/release smoke, all documented
benchmark/profile validators, 10 real-wgpu tests, and both graphics vertical
slices. The post-documentation full gate passes on the exact final local tree;
ready PR #40 targets the exact assigned base from DCO-signed implementation
commit `835ac2b2f3dd8bfe5a31fe9f880a43555e86fd34`. Initial hosted run
`31115252696` passes all eight unchanged essential jobs. GitHub reports the PR
`MERGEABLE` and `CLEAN`; the first thread-aware read found no comment, review,
or inline thread. Delayed review found one valid P2: a reviewed nonempty
manifest could be admitted without a matching complete mandatory prefix. The
local correction binds the reviewed digest to the entire prefix and passes
1,153 tests with the same three Windows capability skips plus complete
static/docs and isolated wheel/release validation. Corrected run `31116147333`
is successful across all eight checks after a failed-job-only rerun recovered a
GitHub action-download setup outage. Final thread-aware review finds the
original P2 outdated and no actionable finding. PR #40 squash-integrated exact
final evidence head `ac8dd43e6b93bc89af1f5dd1821948e4860ac88b` as GitHub-verified
`main` commit `a62d28e8c36d9a590e7ad7e7a9e8b49266dcbdde`; both trees are
`e1f39a9c5d2bc81f76b45288225b27a7c782bf50`, the squash commit has the exact
assigned base as its sole parent, and the milestone branch remains the audit
trail.

M25 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on `[historical branch name redacted]` from
exact clean synchronized `main` commit
`680e90dd8f9377fece23c43bd9f07ca9d76297de`. Its bounded outcome is a strict
offline admission harness for RFC-0003 gate 2. A record can count only after
manual review establishes an independent consumer and freezes a public HTTPS
repository, immutable revision, exact protocol set, bounded outcome, and exact
integration/feedback artifact identities. The evaluator verifies those frozen
facts but cannot establish independence itself. The reviewed manifest is empty,
so the current sanitized result is deterministically `not-ready` and makes no
external-adoption claim. M25 changes no runtime source, public API/export,
protocol, dependency, lock, package version, stability label, workflow, or CI
topology. The manifest is exactly 283 bytes with SHA-256
`b113444f60946461ec6774e2c278b9e82e7d80e08a37450b6cc153e5c5c1500e`;
focused formatting, Ruff, strict Pyright, report execution, and 29 tests pass.
Findings-first review corrected explicit-path symlink enforcement and rejected
credential-bearing, local-host, Unicode, and backslash HTTPS locators. The
final local gate passes 227-file formatting, Ruff, strict Pyright, strict docs,
1,109 tests with two Windows symlink-capability skips, pure build, isolated
wheel/release smoke, all documented benchmark/profile validators, 10 real-wgpu
tests, and both graphics vertical slices.
The DCO-signed implementation is published as ready PR #38 at exact head
`9667e020c2213d415072b7c7efbd880f6b58abfa` against assigned base
`680e90dd8f9377fece23c43bd9f07ca9d76297de`. Sole GitHub Actions run
`31111498136` passed all eight unchanged essential jobs. GitHub reports the PR
`MERGEABLE` and `CLEAN`; the first thread-aware read found no issue comment,
review, or inline review thread. Delayed automated review found one valid P2:
numeric loopback/private/link-local IP authorities could pass the future
locator syntax gate. The local correction requires a non-IP DNS-style
authority, adds exact loopback/link-local regressions, and passes 1,111 tests
with the two Windows capability skips plus the complete static/docs and
isolated wheel/release gate. DCO correction commit
`90ed57e360765cf7f2d0973e41b8f8ec06dc4b50` passed necessary GitHub Actions
run `31112342328` across all eight unchanged essential jobs. PR #38 is
`MERGEABLE` and `CLEAN`. The original thread remains unresolved and non-outdated
because its anchor persists, but the adjacent non-IP gate and exact loopback/
link-local regressions directly satisfy it; no finding remains actionable, and
no reply or manual resolution was performed. A final CI-skipping evidence
head `d0866967832fe80a49942184e1ab81d3c426a478` was squash-integrated by PR
#38 as GitHub-verified `main` commit
`9ec6eeaaed40fefeb64d738d4eaaf3f7a9c4009b`. Both trees are
`fcaa7b11a4aa8d1c87e57a810db16682cf9f00e6`; the squash commit's sole parent
is assigned base `680e90dd8f9377fece23c43bd9f07ca9d76297de`, and its message contains the
DCO sign-off. The milestone branch remains the audit trail.

M24 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on `[historical branch name redacted]` from exact clean
synchronized `main` commit
`55c7a72337913303b6b1f6bd31edbca7ff28683b`. Its bounded outcome is a strict
offline admission harness over the immutable M21 receipt corpus. Gate 1 can
become true only when an installed reader differs from a preserved source
version, at least two versions are observed, every receipt remains canonically
readable, and supported-release records cover every observed version. The
current `0.1.0a1`/empty-release report is deterministically `not-ready` and
does not claim history. M24 changes no runtime source, API/export, protocol,
dependency, lock, package version, stability label, workflow, or CI topology.
The exact manifest/reader baseline passes 71 tests. The final reviewed gate
passes 223-file formatting, Ruff, strict Pyright, strict docs, 1,074 tests with
one existing Windows symlink skip, pure build, isolated wheel/release smoke, 10
real-wgpu tests, both graphics vertical slices, and base/graphics profile
contract smokes. Review hardened bounded streaming/path confinement, reviewed-
manifest identity, exact release coverage, and child/per-receipt resource caps;
26 focused post-hardening tests pass with no remaining finding. DCO-signed
implementation commit `e590d482246d122120c011969b47f79f9680efa2` is published
through ready PR #36. Sole GitHub Actions run `31107800179` passed all eight
unchanged essential jobs. GitHub reports the PR `MERGEABLE` and `CLEAN`; the
first thread-aware read found no comment, review, or inline thread. Delayed
automated review then found one valid P1: a newly pinned future corpus could
replace the current source list instead of retaining the M21 audit trail. The
local correction freezes executable mandatory source/release prefixes, adds an
explicit history-preservation gate and regression, and passes 28 focused tests,
1,076 full-suite tests with the existing skip, the complete static/docs gate,
pure build, isolated wheel smoke, and a fresh ten-artifact release smoke. DCO
correction commit `b393d6857f0a60c5d124fdeb25b3779c8f9dab86` passed necessary
GitHub Actions run `31108924069` across all eight unchanged essential jobs. PR
#36 is `MERGEABLE` and `CLEAN`. The original thread remains unresolved and non-
outdated because its loop anchor persists, but the adjacent frozen-prefix gate
and replacement-corpus regression directly satisfy it; no finding remains
actionable, and no reply or manual resolution was performed. CI-skipping final
evidence head `1a8bd6f19f656eb5c4a0d6bd90f057a69bddbc34` was squash-integrated
by PR #36 as GitHub-verified `main` commit
`b7b16697d28410567cbddf8eb962c7e6c9e664b8`. Both trees are
`fa3c455ccd9722c666cc07cae325f1b50e37ddc7`; the sole parent is assigned base
`55c7a72337913303b6b1f6bd31edbca7ff28683b`, and the commit contains the DCO
sign-off. The milestone branch remains the audit trail.

M23 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on
`[historical branch name redacted]` from exact clean
synchronized `main` commit
`415859e19d9d29caa1168fabc96def509897b056`. Its bounded result is an exact
machine-readable receipt-v1 semantic-diff and diagnostic-code evolution policy,
deterministic installed evidence, RFC-0006, and RFC-0003 schema `/4`
bookkeeping. It changes no runtime package, public API, receipt field, operation,
diagnostic behavior, dependency, lock, version, or CI topology. The complete
local gate passes lock/sync,
219-file formatting, Ruff, strict Pyright,
1,048 tests with one existing Windows symlink skip, strict docs, pure build,
isolated wheel/release smoke, 10 real-wgpu tests, both graphics vertical slices,
and every documented M1-M4/M7 benchmark/profile validator. M1 simulation and
both M3 timing targets remain observed misses rather than pass claims.
The optional `[retired control directory]` task/ledger files expected by the review role
are absent, so the authoritative `[retired control directory]` task, accepted RFCs, `[retired control file]` boundary,
call sites, tests, and executed evidence were used as the review baseline.
DCO-signed implementation commit
`a6dc30ec62d91b1f6640db2c23797967f2aefefe` is published through ready PR
#34. GitHub Actions run `31104052702` passed all eight unchanged essential jobs.
Delayed automated review produced two valid P1 findings: diagnostic identities
were not bound to exact meanings, and the installed evidence did not compare
every generated diff value and declared order. The local correction now freezes
all six code/meaning/scenario triples and an exact full complex-diff oracle. It
passes 20 focused tests, 1,050 full-suite tests with one existing skip, static
and strict-doc gates, pure build, isolated wheel smoke, and a fresh 10-artifact
release smoke. DCO-signed correction commit
`4eb61cd49542b0a4753629f31ebe80229c7d45b8` is published, and follow-up
GitHub Actions run `31105197045` passed all eight unchanged essential jobs.
Thread-aware reread shows both original discussions still unresolved and
non-outdated because their anchors remain in the diff; current adjacent code
directly supplies the requested definitions and full-diff assertion, so no
finding remains actionable. No reply or manual resolution was performed. Final
`[skip ci]` evidence head
`eacb0153d8ac6e5f65d4d52f02c493bf9a891219` was squash-integrated by PR
#34 as GitHub-verified `main` commit
`2f7152565d369225dbf69055b7d42a4c80f46d1a`. Both trees are
`6ba709c29688041992bef75a2a83831275ff32db`; the sole parent is exact assigned
base `415859e19d9d29caa1168fabc96def509897b056`, and the commit contains the
DCO sign-off. The milestone branch remains the audit trail.

M22 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on
`[historical branch name redacted]` from exact clean
synchronized `main` commit
`291dfb3fd6895a2fdac7a2f0016bb181f0e5bca4`. Its bounded result is an exact
machine-readable policy for all seven built-in operation-v1 argument shapes,
deterministic installed valid/missing/unknown-field evidence, RFC-0005, and
RFC-0003 gate bookkeeping. It changes no runtime package, public API,
operation, persistent format, dependency, lock, version, or CI topology.
DCO-signed implementation commit
`f1a89ad460467039f966ed37955144840cd96a12` is published through ready PR
#32. GitHub Actions run `31100821087` passed all eight unchanged essential
jobs. Automated review then requested an explicit defaulted-component-field
omission rule. The contract clarification, installed behavioral regression,
full local gate, wheel, and release smoke pass in DCO-signed correction commit
`cf3ae540e71cda128837ea698f5f175a7abf2fc4`. Follow-up GitHub Actions run
`31101607485` passed all eight unchanged essential jobs. Thread-aware review
now reports the sole review thread outdated and no actionable thread remains.
PR #32 squash-integrated exact final evidence head
`a5a49dcca277f28bb3e6097f37d5418d5d3c2c9d` into `main` as
GitHub-verified commit `8a4d288c4edf55d0299828b8edee1bd1885884d9`;
both trees are `f513bec716d1735cc47a6aab862bca0f5f770af9`, and the sole
parent is the assigned base. The milestone branch remains the audit trail.

M21 is complete, independently reviewed, hosted-validated, and squash-
integrated. It started on `[historical branch name redacted]` from exact clean
synchronized `main` commit `feed793e94c345fac4b146c358a68264ef6e5f62`.
Its bounded result is a public resource-limited reader for the unchanged
`ludoweave.receipt/1` graph plus exact single-version fixtures, installed
evidence, RFC-0004, and compatibility-gate bookkeeping. Implementation is
findings-first reviewed. Ready PR #30 published DCO-signed
implementation commit `cec339be07318a7c1586bb3405e8f9b1904859f5`; sole hosted
run `31098563810` passed all eight unchanged essential jobs. PR #30 squash-
integrated exact final evidence head `4e378756b2a1733de28e7160ac2d6d72921f3e4a`
as GitHub-verified `main` commit
`6bfb56555cafc93a7312f64465ea15cd7c450e79`; both trees are
`ea3f410fac31d7a32faee4e697c4fb0941b657df`.

M0 through M7 are complete, independently accepted, integrated into `main`,
and validated by hosted CI. M8 gamepad/SDL3 evaluation is complete,
independently accepted, published as PR #9 from
`[historical branch name redacted]`, and validated across all 14 hosted jobs.
M9 Box2D v3 plugin admission evaluation is locally complete on
`[historical branch name redacted]`, stacked from the exact M8 head. ADR-0024
defers the plugin; repeat independent review accepted the ownership correction
with no remaining blockers. It is published as ready stacked PR #10 and GitHub
Actions run `31015885190` passed all 14 hosted jobs.
M10's headless semantic inspector is complete, independently accepted, and
published as ready stacked PR #11 from `[historical branch name redacted]`,
based on exact M9 final head
`22bc2de9f8450f60fe483bd4fea10a86702d2f0f`. ADR-0025 accepts one isolated,
owned local MCP child with detached observations and receipted writes. GitHub
Actions run `31020096463` passed all eight essential hosted jobs.
M11 is complete and independently accepted on
`[historical branch name redacted]`, based on exact M10
evidence head `bae799900671481cfd6f03fe502dea95b2c7f96c`. ADR-0026 bounds it
to dependency-free headless audio mixing, bitmap text, tick animation,
immutable tilemaps, and fixed-point particles through existing render records.
It is published as ready stacked PR #12; GitHub Actions run `31024155710`
passed all eight essential hosted jobs on signed implementation commit
`aca6d93165a52d88451e8e06d5f1aa8d2e323f1d`.
M12 is assigned on `[historical branch name redacted]`, based on exact
M11 evidence head `840a8b06d461fa1d5e649911b22f5995154728a7`. Its bounded contract is a
data-only preview plugin-manifest schema and deterministic compatibility
evaluator. RFC-0002 is accepted and implementation plus focused review
hardening are complete. Independent hostile review approved the corrected tree
with no remaining finding, and the complete local/artifact/provider gate
passed. It is published as ready stacked PR #13; GitHub Actions run
`31028863469` passed all eight essential hosted jobs on signed implementation
commit `e1f6e3cd8572d20a4f0a5c62a96b9aa52a986b38`.
M13 is complete and independently accepted on
`[historical branch name redacted]`, based on exact
M12 hosted-evidence head
`7cb834c7b5e84e1b1a945905a68b947b3a4bdd3f`. Its bounded contract is an
offline Clockwork Arena correction-branch proof plus an evidence-based network
rollback admission decision. ADR-0027 defers networking/live rollback because
canonical tick input is not replay-owned and protocol, security, simulation,
resource, lifecycle, and maintenance gates remain incomplete. No runtime
package, persistent format, listener, transport, or dependency is added. The
final complete local/artifact/provider gate passes and independent review
reports no remaining finding. It is published as ready stacked PR #14; GitHub
Actions run `31031590206` passed all eight essential hosted jobs on signed
implementation commit `ba62b650191cfb982100692e7ec694da318956ae`.
M14 is complete and independently accepted on
`[historical branch name redacted]`, based on exact M13
hosted-evidence head
`48f8f296113e3f2794bae7f4c67997d433e4dd36`. Its bounded contract is an
installed-surface audit and product-scope decision only. ADR-0028 retains
layered 2D and defers constrained 3D behind a complete product, engine-contract,
agent-semantic, headless-conformance, cross-platform, resource-budget,
lifecycle, and maintenance gate. Exact source, isolated-wheel, and release
bundle evidence confirms the current orthographic camera and canonical
layer/z ordering while every 3D admission gate remains false. The final local
gate reports 809 passes and one existing Windows symlink-capability skip;
independent hostile review reports no remaining finding. M14 changes no
runtime package, public Python API, persistent format, dependency, version, or
CI topology. GitHub Actions run `31033924254` passed all eight essential jobs
on signed implementation commit
`47443046834eb423be977973775f80494161533d`. M8-M14 were then
squash-integrated into `main` by PR #16 as verified commit
`2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`; its tree exactly matches final
M14 evidence head `02426805a11712030b3082ec349696d6d94aca50` at tree
`137a1870b0dd9034ad935b253a13186f6c7cc913`. Stacked PRs #9-#15 are closed as
superseded, with branches retained for audit history.

Repository-state evidence was then integrated through PR #18 as verified main
commit `bfea67d2d922e8c591224d18f56c14d572d7f7da`. M15 is locally complete and
independently accepted from that exact clean base on
`[historical branch name redacted]`. Its bounded contract is
an installed-surface product decision only: confirm the versioned
command/receipt, typed-tool, local MCP, and read-only inspector foundation;
retain the headless inspector; and defer visual-editor implementation until
the complete ADR-0029 compatibility, authoring, recovery, usability,
cross-platform packaging, resource-budget, and maintenance gate is satisfied.
The final local gate reports 834 passes and one existing Windows
symlink-capability skip, clean static/docs/build/artifact/provider checks, and
successful validation of every inherited documented benchmark/profile. No
GUI/TUI, runtime package, public API, persistent format, dependency, lock,
version, or CI change is introduced. It is published through ready PR #19;
GitHub Actions run `31036925179` passed all eight unchanged essential jobs on
DCO-signed implementation commit `7e85570056dde3678aaeee13eee4036067876d8c`.

PR #19 squash-integrated the exact final M15 tree into `main` as verified
commit `c013dad38b1b64f0f4ccddc19681d643f6414427`. M16 is assigned on
`[historical branch name redacted]` from that exact clean base. Its bounded
contract is an executable-WASM-mod security admission decision only: preserve
the M12 data-only plugin boundary, document the prospective threat surface and
complete gate, and add deterministic source/wheel/release evidence plus
architecture guards. It does not add a runtime, loader, guest ABI, WASI, host
call, public API, persistent format, dependency, lock, version, or CI job.
The implementation is complete and independently accepted. The final
post-review gate reports 870 passes and one existing Windows symlink-capability
skip, clean static/docs/build/artifact/provider checks, and successful
validation of every inherited documented benchmark/profile. It is published
through ready PR #20; GitHub Actions run `31039403209` passed all eight
unchanged essential jobs on DCO-signed implementation commit
`bcaf78fbc78bda8a13a95e397ab15d003dd4a6ce`.
PR #20 then squash-integrated exact final M16 head
`808e48a5cb2727c8e1f4d7e896c4f8c7d41bfe1a` into `main` as GitHub-verified
commit `e2bd57c057c0c16861953c0702b2012c4cabfe90`. Both trees are
`05367be9bd85014fe6c70995ac1a69a39f90ef1e`; the milestone branch remains the
audit trail.

M16 integration evidence was then squash-integrated through PR #21 as verified
`main` commit `27d2ee9d1f7f75dacc17568650f00ce833ef4fce`. M17 is assigned on
`[historical branch name redacted]` from that exact clean base. Its bounded
contract is one installed experimental `RenderDevice` baseline profile over an
explicit trusted factory. It adds sanitized versioned reports, Null/wgpu
evidence, artifact smoke, architecture guards, ADR-0031, and public guidance.
It adds no discovery, dynamic import, installation, provider adapter,
dependency, lock, version, canonical/persistent world format, or CI job. The
complete local quality/artifact/provider gate passes with 895 tests and one
existing symlink skip. Ready PR #22 targets `main` from DCO-signed
implementation commit `8e592f329424719214239bf97bd85dad9c9c5928`; GitHub
Actions run `31042903689` passed all eight unchanged essential jobs. PR #22
then squash-integrated exact final evidence head
`148600cdaf9c419fbf552c68f833e0d55655731f` into `main` as GitHub-verified
commit `610261c8450afc3d7db6ebb2b0425a1829737aec`; both trees are
`1e82568a463c62d0a1cf988b67eea09885ec50e3`, and the milestone branch is
retained.

M17 integration evidence was then squash-integrated through PR #23 as verified
`main` commit `ed65b12fa02f672113eac5939a0f616079fee44a`. M18 is assigned on
`[historical branch name redacted]` from that exact clean base. Its bounded
contract is one installed experimental 12-tool agent-service profile over an
explicit trusted factory, with sanitized reports, source/wheel/release smoke,
architecture guards, ADR-0032, and public guidance. It adds no discovery,
dynamic import, installation, subprocess, network transport, provider,
dependency, lock, version, persistent format, canonical state, or CI job.
The final local gate passes, ready PR #24 targets `main` from DCO-signed
implementation commit `c4dde705393eebb7c99af428745e9383750f6b4d`, and GitHub
Actions run `31046172544` passed all eight unchanged essential jobs.
PR #24 then squash-integrated exact final evidence head
`cb617be0f678528fadc82877ec6910e42c6daf6b` into `main` as GitHub-verified
commit `1000d362432f19c912edf51c67e29c79bf444443`; both trees are
`1b6676ca7c1a6aaa223057a35e0c95242f4e9462`, and the milestone branch is
retained.

## Repository identity

M3 rendering is complete on `[historical branch name redacted]`, published as
stacked PR #3, and validated by corrected hosted run `30993554807` across the
14-job quality, CPython/OS, wheel, and graphics matrix. M4 is complete on
`[historical branch name redacted]`, published as stacked PR #4, and validated by hosted
run `30996905660` across the same 14-job matrix.
M5 agent control is complete on `[historical branch name redacted]`, published as stacked
PR #5, and validated by hosted run `30999777517` across the same 14-job matrix.
M6 community-alpha hardening is complete on `[historical branch name redacted]`,
published as stacked PR #6, and validated by hosted run `31002365370` across the
same 14-job matrix, including complete candidate smoke on all three platforms.
M7 performance/native decision is complete on
`[historical branch name redacted]`, published as stacked PR #7, and validated by
hosted run `31005165849` across all 14 jobs, including the new base and
real-wgpu profiling-contract smokes.
The validated M1-M7 tree was squash-integrated to `main` by PR #8 as commit
`0237b2bfb11c6032d030dada639c7dbe439e5089`. The validated M8-M14 tree was
squash-integrated by PR #16 as commit
`2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`. The milestone branches and
hosted-run records remain the audit trail; superseded stacked PRs are closed.
Repository-state evidence is integrated by PR #18 as main commit
`bfea67d2d922e8c591224d18f56c14d572d7f7da`.

- Canonical repository: `xsparc/ludoweave-engine`.
- Package and CLI: `ludoweave`.
- Alpha candidate version: `0.1.0a1`.
- License and contribution model: Apache-2.0 with DCO sign-off.
- Supported baseline: standard CPython 3.12-3.14 on Windows, macOS, and Linux; no mandatory native compiler.

## Implemented

- Public README, governance, contribution, conduct, security, changelog, NOTICE, issue/PR templates, and agent guidance.
- PEP 621 pure-Python package, uv lockfile, Ruff, strict Pyright, pytest, Hypothesis, MkDocs Material, and typed-package marker.
- Immutable engine configuration and run summary; monotonic and deterministic virtual clocks.
- Explicit single-owner engine lifecycle with initialization, fixed-tick run, shutdown, failure cleanup, idempotent close, and structured exceptions.
- Engine-owned render protocol, backend-neutral descriptor, and lifecycle-validating null renderer.
- `ludoweave --version`, structured `ludoweave doctor`, and deterministic headless example.
- Architecture overview, runtime contract, accepted ADR-0001 through ADR-0007, and AST import rules that test absolute, relative, near-prefix, and reference-model independence constraints.
- Least-privilege GitHub Actions matrices for the supported operating systems/Python versions and installed-wheel smoke tests.
- Immutable two-field entity IDs, deterministic generational allocation, structured stale-handle failures, and installed-wheel ECS smoke coverage.
- Explicit component UUIDs, frozen schemas, immutable UUID-sorted registries, scalar validation metadata, and complete adjacent forward migration chains.
- Storage-neutral `WorldStore`, canonical `World`, private pure-Python dense/sparse component tables, deterministic inspection, change epochs, and independent in-memory cloning.
- Deliberately simple dictionary `ReferenceWorld` with separately implemented allocation, value, epoch, patch, and clone logic, exercised as a Hypothesis state-machine oracle.
- Structured duplicate/missing/malformed-value failures, copy-in/copy-out ownership, generation-safe swap removal, and installed-wheel world lifecycle coverage.
- Storage-neutral typed query builders with include/exclude/changed filters, opt-in stable ordering, detached row values, explicit writable cursor ownership, row-atomic validated writeback, and private structurally invalidated plan caching.
- World-bound reusable `Commands` buffers with copy-on-enqueue values, identity-only deferred entity tokens, clone-staged atomic flush, deterministic direct-operation epochs, retry/clear failure behavior, and local non-receipt `FlushResult` values.
- Production/reference query and flush conformance, extended Hypothesis state-machine coverage, exact reference-import whitelisting, and installed-wheel query/command smoke coverage.
- Explicit identity-owned typed resource keys, immutable registries, copy-owned singleton stores with a trusted read-only-input adapter contract, exact generic return typing, and structured copy failures.
- Immutable module-level Python system declarations, fixed simulation phases, component/resource access metadata, deterministic-eligibility gates, same-phase conflict ambiguity rejection, canonical cycle diagnostics, and input-order-independent serial schedule planning.
- ADR-0006 documentation, generated DAG/property coverage, D0 component rejection in deterministic plans, and installed-wheel resource/scheduler smoke coverage.
- Exact integer-unit fixed-step accumulation, retained catch-up backlog, absolute virtual deadlines, immutable exact-value input snapshots, virtual/recorded input sources, and application-owned input publication.
- Declaration-enforcing invocation contexts, canonical schedule revalidation, serial PRE/SIMULATE/flush/POST execution, structured failure attribution, BaseException-safe cleanup, and an additive installed-wheel fixed-step example.
- Versioned M1 benchmark tooling for seven workloads with raw samples, nearest-rank p50/p95/p99, sanitized CPython/GIL/environment/commit metadata, exact artifact validation, and tamper regressions.
- Bounded canonical JSON with exact finite-float tags, duplicate/Unicode/size validation, immutable command/transaction envelopes, and an explicit versioned operation registry with a compatibility fingerprint.
- Single-owner authoritative world sessions, complete allocator/epoch logical images, explicit persistent resource schemas/codecs, SHA-256 state hashes, clone-staged entity/component/resource/tick transactions, optimistic pre-hash checks, dry-run, deterministic limits, and atomic pointer-swap adoption.
- Canonical committed/dry-run/rejected transaction receipts with sanitized diagnostics, command outcomes, exact alias resolutions, and independent semantic diffs covering net entity/component/resource changes plus allocator, epoch, and tick behavior.
- Canonical complete-authority snapshots with SHA-256 verification, bounded atomic restore, registered component/resource migrations, allocator/epoch preservation, and independently named deterministic PCG32 random streams.
- Self-contained canonical replay timelines with compatibility headers, exact transaction/tick/hash batches, verified checkpoints, one-tick branch boundaries, and immutable parent-referenced branches.
- Data-only project composition plus project-confined `apply`, `snapshot`, `replay`, and `diff` CLI workflows with project-bound snapshots, handle-bounded input, and atomic output replacement.
- Informational M2 benchmark/validator tooling for canonical transactions, atomic application, snapshot round trips, and replay verification.
- Frozen backend-neutral render descriptors, explicit target/camera command lists, scoped generational resource handles, deterministic presentation extraction, and graph dependency/lifetime validation.
- A validation-only `NullRenderDevice` with fence-deferred physical reuse and an optional exact wgpu/rendercanvas/GLFW adapter isolated from package roots and canonical world state.
- An installed experimental `RenderDevice` baseline conformance profile that
  exercises explicit trusted factories and emits deterministic sanitized
  evidence without discovery, loading, installation, or provider admission.
- Instanced atlas sprites, translated/zoomed/rotated orthographic cameras, stable layer/z/entity ordering, tile batches, debug lines, built-in diagnostic glyphs, resize/minimize behavior, immutable offscreen RGBA capture, and typed device-loss diagnostics.
- M3 renderer benchmark/validator tooling for 1k/10k extraction, Null submission, and wgpu CPU submission with raw p50/p95/p99 evidence and exact draw counts.
- Frozen provider-neutral platform events, immutable action snapshots with transition metadata, deterministic recorded input, and isolated render-surface event draining.
- Strict project-root-confined asset manifests, transitive content-addressed cache keys, bounded pure-Python PNG decoding, and explicitly retired immutable texture revisions.
- Deterministic AABB/circle overlap, stable exact-filter spatial grids, bounded axis-ordered kinematic movement, and a minimal engine-owned null audio backend.
- Clockwork Arena canonical world/resource gameplay, fixed-seed waves, projectiles, collision, score/restart behavior, immutable presentation extraction, and deterministic headless/offscreen/window examples.
- Exact 3,600-tick Clockwork Arena fixture and independently recorded-input replay hash, plus M4 benchmark/validator tooling for baseline and informational stress workloads.
- Transport-independent typed agent command/query service with 12 immutable tool schemas over canonical transactions, receipts, snapshots, diffs, replay, capture, telemetry, and registered tests.
- An installed experimental 12-tool agent-service baseline conformance profile
  that exercises explicit trusted factories and emits deterministic sanitized
  evidence without discovery, loading, installation, transport selection, or
  provider admission.
- An installed experimental `WorldStore` baseline conformance profile that
  exercises explicit trusted `factory(ComponentRegistry)` implementations and
  emits deterministic sanitized evidence without discovery, concrete storage,
  persistence, external-resource lifecycle, or provider admission.
- Default read-only capabilities, explicit write/capture/test grants, bounded requests/results/work, monotonic rate limiting, caller binding, recursive credential redaction, and non-blocking single-thread mutation safe points.
- Project-confined `ludoweave agent` composition and local-only stdio MCP `2025-11-25` initialization, discovery, and tool calls without networking, shell access, arbitrary evaluation, dynamic project imports, or a new runtime dependency.
- Agent World Builder acceptance composition with six typed ECS entities, real offscreen wgpu capture, exact query/adjust/diff/test/telemetry/replay coverage, and installed-wheel execution.
- Deterministic community-alpha release staging with a pure wheel, sdist, fixed-timestamp sample bundle, SHA-256 inventory, versioned manifest, SPDX 2.3 SBOM, and notice set.
- Isolated release smoke that validates exact checksum coverage, SBOM/wheel identity, safe ZIP members, installed CLI/doctor, and bundled headless M0-M5 scenarios before success.
- Explicit `__all__`/`__stability__` policy and architecture coverage for every
  supported Python export. Earlier `0.1.0a1` symbols remain experimental;
  `ludoweave.plugins` is the first preview surface with a documented
  deprecation promise.
- Pinned tag-only provenance/prerelease workflow plus one complete baseline
  release-candidate smoke, compatibility coverage for every supported Python
  version/OS, and real graphics smoke on all three operating systems.
- Community-alpha user, architecture, adapter, release, first-contribution, API, triage, release-note, roadmap, and retrospective material with declarative labels and issue-ready starter cards.
- Versioned M7 base/graphics `cProfile` tooling with exact workload invariants,
  sanitized module/function records, strict validation, and tamper regressions.
- Query metadata/signature traversal reductions mirrored independently in the
  production and reference worlds, validated presentation reconstruction, and
  fixed-record provider-neutral sprite packing.
- Accepted RFC-0001 and ADR-0022: no native kernel is admitted; measurable
  cross-platform, contiguous-buffer, GIL, owner, build, fuzz, fallback, and
  improvement gates govern any future proposal.
- Frozen standardized gamepad connection/button/axis records, bounded logical
  slots, normalized stick/trigger domains, and an engine-owned provider
  protocol implemented by Null and the optional render device.
- Gamepad action bindings with explicit analog scale/deadzone semantics,
  supported-control focus recovery, hotplug cleanup, stable GLFW polling, and
  installed-wheel/Clockwork Arena coverage without provider-object leakage.
- Accepted ADR-0023: the existing pinned GLFW adapter supplies M8 input while
  SDL3 is deferred until its Python binding, binary delivery, ownership,
  cross-platform conformance, and maintenance gates are satisfied.
- A bounded isolated Box2D-candidate probe with versioned sanitized JSON,
  exact single-thread fixed-step traces, repeated lifecycle churn, double
  destruction, strict workload bounds, and no LudoWeave/runtime import.
- Accepted ADR-0024: `box2d-python==0.1.2` is deferred after failing the complete
  CPython/platform wheel and stable-API gates and lacking sufficient
  ownership, GIL/thread, replay, adapter-conformance, and maintenance evidence.
- Architecture fixtures reject case-insensitive Box2D/native-binding imports
  from engine source; the base project metadata, uv lock, wheel, and runtime
  remain unchanged and pure Python.
- `ludoweave inspect` owns one isolated `python -I -m ludoweave mcp` child,
  defaults to read-only, emits bounded `ludoweave.inspector.event/1` semantic
  observations, and verifies MCP identity, typed tools, receipts, completed
  ticks, and exact snapshot/diff/world/query/telemetry hash continuity.
- Inspector sample bootstrap and ticks require explicit write capability and
  reuse existing versioned transaction/tick tools. Child commands, module
  shadowing, option injection, network listeners, remote attach, parallel
  authority, paths, environment values, process IDs, and provider objects are
  excluded and covered by adversarial tests.
- Pull-request CI is consolidated from 14 to eight essential jobs: one complete
  Ubuntu 3.12 quality/test/distribution gate, four compatibility jobs spanning
  CPython 3.13/3.14 and Windows/macOS, and three real cross-platform graphics
  jobs. Superseded runs remain cancelled.
- `ludoweave.presentation` frozen animation, bitmap-glyph, tilemap, and
  fixed-point particle records with exact-tick sampling, integer layout/culling,
  stable seeded stepping/digests, and existing render extraction.
- A bounded acyclic audio mix graph rooted at `master`, enforced by the
  lifecycle-validating Null backend with category and effective-gain checks.
- A dependency-free rich 2D showcase registered in source, isolated-wheel, and
  deterministic release sample-bundle validation paths.
- Accepted RFC-0002 plus strict canonical plugin manifests, frozen explicit
  compatibility contexts/reports, bounded dependency checks, a path-free local
  CLI check, and source/wheel/release example coverage. The package owns no
  discovery, import, execution, filesystem, networking, or mutable registry.
- Bounded M13 parent/correction replay evidence with exact parent lineage,
  repeatable divergent resimulation, explicit external input rehydration, a
  strict sanitized validator, and source/wheel/release-bundle composition.
- Accepted ADR-0027 deferring network rollback and remote authority until the
  complete canonical-input, protocol, security, cross-platform simulation,
  resource-budget, lifecycle, artifact, and maintenance gate is met.

## Next slice

- M0 through M32 are complete, hosted-validated, reviewed, and squash-
  integrated.
- Select the next bounded slice from current authoritative project goals; no
  subsequent milestone is assigned by this factual integration record.
- Actual cross-version package history, external consumer feedback, and a
  supported deprecation-capable feature-release channel remain absent. Do not
  promote the experimental command/receipt surface by inference.

## Validation state

- The exact M21 base resolves 46 locked packages. Its focused receipt,
  persistent-schema, canonical-JSON, API/import-boundary, and artifact baseline
  passes 138 tests in 1.70 seconds; its inherited full suite passes 972 tests
  with one existing Windows symlink-capability skip in 69.25 seconds. The final
  reviewed M21 gate passes 1,015 tests with the same single skip in 69.87
  seconds, 211-file formatting, zero Ruff/Pyright findings, strict docs, a pure
  94-entry wheel, isolated-wheel smoke, a fresh complete ten-artifact release
  smoke, 255 expanded receipt/transaction/agent/release/architecture tests, and
  ten real-wgpu tests. Every inherited benchmark/profile artifact validates;
  M1 simulation and both M3 targets remain observed misses and authorize no
  acceleration. Workflow, metadata, lock, version, and root exports are
  unchanged. Ready PR #30 is mergeable and clean after sole hosted run
  `31098563810` passed all eight essential jobs on the DCO-signed implementation
  commit. PR #30 squash-integrated the exact final branch tree as verified
  `main` commit `6bfb56555cafc93a7312f64465ea15cd7c450e79`.

- The exact M20 base resolves 46 locked packages. Its focused canonical
  command/transaction/receipt/agent/API baseline passes 91 tests in 1.52
  seconds, and its full suite passes 955 tests with the existing Windows
  symlink-capability skip in 72.22 seconds. The final M20 Windows/uv-managed
  CPython 3.12.13 gate passes 972 tests with that one skip in 73.99 seconds,
  205-file formatting, zero Ruff/Pyright findings, strict documentation, a pure
  94-entry wheel with no mandatory dependency or native/WASM file, isolated-
  wheel smoke, a fresh complete ten-artifact release smoke, 211 expanded
  focused passes, and ten real-wgpu passes. All inherited benchmark/profile
  artifacts validate; the M1 simulation and both M3 targets remain observed
  misses and authorize no acceleration. Review hardened forbidden-import
  prefix detection and reports no remaining finding. Workflows, runtime source,
  project metadata, lock, version, protocol, stability labels, and package-root
  exports are unchanged. Ready PR #28's sole hosted run `31095009029` passed
  all eight unchanged essential jobs. The exact final head is squash-integrated
  as verified `main` commit `d166ef86bf25526d9d7715f63263d3cac6db78d4`
  with matching tree `c3e2dc1224f530fb483d1b9684ff55329bf9557b`.
- The final hardened M19 local gate on Windows/uv-managed CPython 3.12.13
  reports 955 passing tests and one existing symlink-capability skip, 201
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 94-entry wheel with no mandatory dependency or native/WASM file,
  isolated-wheel smoke, fresh complete ten-artifact release smoke, 149 focused
  conformance/release/architecture passes, and ten real-wgpu passes. All
  inherited benchmark/profile artifacts validate; the existing M1 simulation
  and both M3 targets still miss and authorize no native work. Workflows,
  project metadata, lock, version, and package-root exports are unchanged.
- The final reviewed M18 local gate on Windows/uv-managed CPython 3.12.13
  reports 925 passing tests and one existing symlink-capability skip, 196
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 93-entry wheel with no mandatory dependency or native/WASM file,
  isolated-wheel smoke, fresh complete ten-artifact release smoke, 145 focused
  conformance/release/architecture passes, and ten real-wgpu integration
  passes. All inherited benchmark/profile artifacts validate; the existing M1
  simulation and both M3 targets still miss and authorize no native work.
- The final reviewed M16 local gate on Windows/uv-managed CPython 3.12.13
  reports 870 passing tests and one existing symlink-capability skip, 186
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 91-entry wheel with no mandatory dependency or native/WASM file,
  isolated-wheel smoke, and fresh complete ten-artifact release smoke.
- Nine real-wgpu integration tests and every inherited benchmark/profile
  artifact validator passed. Current M1 and M3 target misses remain recorded
  engineering evidence and do not authorize native or WASM acceleration.
  Repeat independent security review approved after exact distribution-
  requirement evidence, named/dynamic runtime guards, residual-risk ownership,
  and current-flow accuracy corrections, with no remaining finding.
- The final reviewed M13 local gate on Windows/uv-managed CPython 3.12.13
  reports 793 passing tests and one existing symlink-capability skip, 174
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 91-entry wheel with zero native files and no mandatory dependency,
  isolated-wheel smoke, and fresh complete ten-artifact release smoke.
- Nine real-wgpu integration tests, the versioned 120/60 correction proof,
  strict evidence validation, Clockwork Arena, Agent World Builder, alpha
  acceptance, rich-2D showcase, and plugin compatibility passed. Every
  inherited README benchmark/profile artifact validated; the existing M1 and
  M3 target misses remain recorded and do not authorize acceleration.
- Independent hostile review drove pre/post-open file bounds, canonical JSON,
  exact types/counts/checkpoints, direct-call work limits, closed import/member
  allowlists, and alias/tamper regressions. Final review ran 54 focused tests,
  the maximum 600/300 proof, strict docs/static/diff/secret checks, and reported
  no blocking or non-blocking finding.
- GitHub Actions run `31031590206` passed the unchanged essential eight-job
  topology on M13 implementation commit
  `ba62b650191cfb982100692e7ec694da318956ae`: the complete Ubuntu 3.12
  quality/test/distribution job, Ubuntu 3.13/3.14 plus Windows/macOS 3.14
  compatibility jobs, and real graphics jobs on Ubuntu, Windows, and macOS.
- The final reviewed M12 local gate on Windows/uv-managed CPython 3.12.13
  reports 741 passing tests and one existing symlink-capability skip, 170
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 91-entry wheel with four plugin-contract entries and zero native files,
  isolated-wheel smoke, and fresh complete ten-artifact release smoke.
- Nine real-wgpu integration tests, Null/wgpu Clockwork Arena, Agent World
  Builder, alpha acceptance, rich-2D showcase, and the canonical example plugin
  check passed. Every inherited README benchmark/profile artifact validated;
  the existing M1 simulation and M3 renderer target misses remain recorded and
  do not authorize native work.
- Independent hostile review drove boundedness, exact-type, canonical-report,
  sanitized-diagnostic, immutable-decision, import/global-state, I/O/eval, and
  CLI regressions. Final re-review ran 138 focused tests with clean static,
  docs, diff, and isolated CLI checks and reported no remaining finding.
- GitHub Actions run `31028863469` passed the unchanged essential eight-job
  topology on M12 implementation commit
  `e1f6e3cd8572d20a4f0a5c62a96b9aa52a986b38`: the complete Ubuntu 3.12
  quality/test/distribution job, Ubuntu 3.13/3.14 plus Windows/macOS 3.14
  compatibility jobs, and real graphics jobs on Ubuntu, Windows, and macOS.
- The final reviewed M11 local gate on Windows/uv-managed CPython 3.12.13
  reports 663 passing tests and one existing symlink-capability skip, 164
  formatted Python files, zero Ruff/Pyright findings, strict documentation,
  a pure 87-entry wheel with seven presentation entries and zero native files,
  isolated-wheel smoke, and complete ten-artifact release smoke.
- Nine real-wgpu integration tests, base/graphics one-repeat profiling-contract
  smokes, Clockwork Arena, Agent World Builder, alpha acceptance, and the
  repeatable rich-2D showcase passed. M11 defines no timing target and makes no
  performance claim.
- Independent review found exclusive tile-bound, pre-bound traversal, runtime
  parent-fader, bounded-sequence, particle-work/state, and generic-style issues
  during development. The corrected edge/work/iterator/gain regressions passed;
  final re-review ran 78 focused tests plus 58 architecture/API tests with clean
  Ruff/Pyright/provider/diff/credential checks and reported no remaining
  finding.
- GitHub Actions run `31024155710` passed the unchanged essential eight-job
  topology on M11 implementation commit
  `aca6d93165a52d88451e8e06d5f1aa8d2e323f1d`: the complete Ubuntu 3.12
  quality/test/distribution job, Ubuntu 3.13/3.14 plus Windows/macOS 3.14
  compatibility jobs, and real graphics jobs on Ubuntu, Windows, and macOS.
- The final reviewed M10 local gate on Windows/uv-managed CPython 3.12.13
  reports 642 passing tests and one existing symlink-capability skip, 154
  formatted Python files, zero Ruff/Pyright findings, strict documentation
  success, a pure 80-entry wheel with no native entries or mandatory runtime
  dependency, installed-wheel shadow-isolation smoke, and complete 10-artifact
  release smoke.
- Eight real wgpu/GLFW integration tests, base/graphics one-repeat profiling
  contract smokes, Clockwork Arena, Agent World Builder, and alpha acceptance
  passed. M10 defines no performance target and makes no timing claim.
- Independent review first blocked publication on child import shadowing,
  dash-prefixed project option injection, incomplete tick receipt validation,
  and unstructured stream failures. `-I`, option termination/binding, exact
  receipt/hash/tick validation, structured read errors, and adversarial source
  and installed-wheel regressions resolved all findings. Repeat review ran 81
  focused tests with clean Ruff/Pyright/diff checks and approved publication.
- The consolidated eight-job CI workflow parses and its architecture contract
  passes locally. Its exact baseline test command excludes the separately
  gated wgpu integration file and passed 634 tests with one skip; real provider
  execution remains confined to the three jobs that install platform runtime
  prerequisites. GitHub Actions run `31020096463` passed that exact topology on
  implementation commit `2e60b3f1c4884dba71df5f23b779bc49187d68c6`.
- The corrected M9 local gate on Windows/uv-managed CPython 3.12.13 reports 606 passing
  tests and one existing symlink-capability skip, 151 formatted Python files,
  zero Ruff/Pyright findings, strict documentation success, a 79-entry pure
  wheel with zero native entries, installed-wheel and complete 10-artifact
  release smoke, eight real wgpu integration passes, and successful Clockwork
  Arena, Agent World Builder, and alpha-acceptance executions.
- Isolated `box2d-python==0.1.2` probes on Windows CPython 3.12.13 and 3.13.13
  each created/stepped/destroyed 25 worlds, repeated their exact traces, and
  produced trace digest
  `c9e299e715c5f7a3654d7c5794d75347d765cc029b7991d4c8066dfaf7abdfc5`.
  CPython 3.14 resolution failed because the release has only `cp312` and
  `cp313` wheels. These are candidate-admission facts, not performance,
  cross-platform determinism, or runtime-support claims.
- Independent review initially blocked sign-off because the metadata version
  was not linked to the imported module. The corrected probe validates the
  resolved module against the distribution's installed-file inventory before
  import and again afterward. Repeat review ran 54 focused tests, Ruff,
  Pyright, diff checks, and a real CPython 3.12 probe, found no remaining
  blocker, and recommended final sign-off.
- GitHub Actions run `31015885190` passed all 14 M9 jobs for implementation
  commit `8b429aaf07684651f6d538419701c049ee55fc4f`: strict quality/docs; Ubuntu
  CPython 3.12/3.13/3.14; Windows and macOS CPython 3.12/3.14; complete
  installed release-candidate smoke on Ubuntu/Windows/macOS; and real graphics
  smoke on all three systems. PR #10 is open, ready, mergeable, and clean
  against the exact validated M8 head.
- A pre-review M8 gate completed on Windows with uv-managed CPython 3.12.13,
  but an independent review then found production focus propagation, GLFW
  error-disambiguation, and trigger-neutrality defects. Its 589-pass result is
  retained as historical evidence, not accepted as the final M8 gate.
- The corrected final M8 gate reports 594 passing tests and one existing
  Windows symlink-capability skip, 149 formatted Python files, zero
  Ruff/Pyright findings, strict documentation success, a 79-entry pure wheel
  with zero native entries, installed-wheel and complete release-candidate
  smoke, eight real wgpu/GLFW integration passes, and successful Clockwork
  Arena, Agent World Builder, and alpha-acceptance executions. Repeat
  independent review found no blocking findings and recommended PR
  publication. M8 adds no dependency or benchmark; no timing result is
  claimed.
- GitHub Actions run `31012696753` passed all 14 M8 jobs: strict quality/docs;
  Ubuntu CPython 3.12/3.13/3.14; Windows and macOS CPython 3.12/3.14;
  installed-wheel smoke on Ubuntu, Windows, and macOS; and real graphics/GLFW
  gamepad smoke on all three operating systems.
- The complete M1 final local suite reports 303 passing tests, zero Ruff/Pyright findings, a strict documentation build, successful sdist/wheel build, and successful isolated installed-wheel smoke covering both M0 and M1 examples.
- The final 30-sample Windows/CPython 3.12.13 GIL-build benchmark artifact validates all seven versioned workloads. The 3,600-tick headless p95 was 26.8523 ms and observed the local 5×-real-time target. The representative 10,000-entity simulation-tick p95 was 196.8800 ms and did not observe the 4 ms engineering target. These are local observations, not cross-platform claims.
- GitHub Actions run `30936533105` passed quality/documentation, Ubuntu Python 3.12/3.13/3.14, Windows Python 3.12/3.14, macOS Python 3.12/3.14, and installed-wheel smoke on all three operating systems after correcting the invalid planned `actions/checkout` v6.0.2 SHA.
- MkDocs Material emits its upstream informational warning about the future MkDocs 2.0 project; the strict documentation build exits successfully.
- The final M2 local gate on Windows/uv-managed CPython 3.12.13 reports 444 passing tests and one Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, successful sdist/wheel build, and successful isolated installed-wheel workflow smoke.
- The final 30-sample M2 informational benchmark validated four workloads with no timing targets. Local p50/p95 durations were 30.2751/33.7076 ms for canonical 100-command round trips, 13.9896/16.9751 ms for atomic 100-command apply, 17.1209/18.0412 ms for 1,000-entity snapshot round trips, and 216.5521/271.2240 ms for verified 100-batch replay.
- Independent final M2 code/security and quality reviews found no remaining actionable findings and independently reproduced the 444-pass/one-skip suite.
- GitHub Actions run `30947073913` passed all 11 M2 jobs: quality/documentation; Ubuntu tests on Python 3.12/3.13/3.14; Windows and macOS tests on Python 3.12/3.14; and isolated installed-wheel smoke on Ubuntu, Windows, and macOS.
- The final local M3 graphics gate on Windows/uv-managed CPython 3.12.13 reports 485 passing tests and one Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, a pure wheel, and a successful no-dependency installed-wheel smoke. A separate frozen base sync removed all graphics packages and reported 479 passes with the symlink and graphics capability skips.
- The real Windows GLFW example and the offscreen clear/sprite/capture fixtures completed. The 30-sample M3 artifact validated six workloads with one draw each. Local 10k extraction/packing p50/p95/p99 was 35.4460/41.9722/51.8362 ms; wgpu CPU submission was 5.3753/6.5363/6.9215 ms. Neither observed the 3 ms starting target; no target pass is claimed.
- Initial M3 hosted run `30951328011` passed all base test and wheel jobs plus Windows/macOS graphics, but failed the quality type check because optional providers were not installed and failed Ubuntu graphics because no driver was present. The correction installs the exact graphics extra for quality and Mesa Vulkan only for the Ubuntu graphics job.
- Corrected GitHub Actions run `30993554807` passed all 14 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; isolated wheel smoke on all three operating systems; and real clear/sprite/capture/resize/loss graphics smoke on Ubuntu software Vulkan, Windows, and macOS.
- The final local M4 gate on Windows/uv-managed CPython 3.12.13 reports 516 passing tests and one existing Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, a pure wheel, successful no-dependency installed-wheel smoke, real offscreen and GLFW Clockwork Arena runs, exact 3,600-tick deterministic fixture/replay agreement, and a valid 300-sample three-workload benchmark artifact.
- The local baseline Clockwork Arena benchmark p50/p95/p99 was 1.5228/2.1228/2.5898 ms and observed its 16.666667 ms p95 target. Stress 4 and 8 p95 values were 3.5029 ms and 4.8371 ms and have no assigned target. These are local observations, not cross-platform claims.
- GitHub Actions run `30996905660` passed all 14 M4 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; isolated wheel smoke on all three operating systems; and real graphics smoke, including Clockwork Arena wgpu execution, on Ubuntu software Vulkan, Windows, and macOS.
- The final local M5 gate on Windows/uv-managed CPython 3.12.13 reports 545 passing tests and one existing Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, a pure wheel, successful no-dependency installed-wheel smoke, and a real offscreen wgpu Agent World Builder run.
- Direct Python, the actual `ludoweave agent` subprocess, and MCP return equivalent canonical transaction results/receipts. MCP lifecycle, malformed input, duplicate IDs/keys, capability denial, limits, atomic stale-hash rejection, reentrant/wrong-thread mutation rejection, redaction, provider close, and architecture bans are covered.
- GitHub Actions run `30999777517` passed all 14 M5 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; isolated wheel smoke on all three operating systems; and real graphics smoke, including the Agent World Builder typed-tool loop, on Ubuntu software Vulkan, Windows, and macOS.
- The final local M6 gate on Windows/uv-managed CPython 3.12.13 reports 552 passing tests and one existing Windows symlink-capability skip, 143 formatted Python files, zero Ruff/Pyright findings, strict documentation success, a pure `0.1.0a1` wheel, successful no-dependency installed-wheel smoke, and a complete 10-file staged candidate whose checksum/manifest/SBOM/sample smoke passed.
- M6 changes release/community surfaces rather than simulation performance. No new benchmark or performance pass is claimed; inherited M1/M3 misses and M4 observation remain unchanged.
- GitHub Actions run `31002365370` passed all 14 M6 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; complete installed release-candidate smoke on all three operating systems; and real graphics smoke, including Clockwork Arena and Agent World Builder, on Ubuntu software Vulkan, Windows, and macOS.
- The final local M7 gate on Windows/uv-managed CPython 3.12.13 reports 564
  passing tests and one existing Windows symlink-capability skip, 148 formatted
  Python files, zero Ruff/Pyright findings, strict documentation success, a
  pure wheel/sdist, successful no-dependency wheel smoke, complete 10-file
  release smoke, six real wgpu integration passes, and successful wgpu sample
  compositions.
- Final valid 30-sample M7 observations are 130.1806/144.0474/150.6699 ms
  p50/p95/p99 for the 10,000-entity simulation tick, 20.8641/30.6902/31.4777 ms
  for 10,000-sprite extraction/packing, and 2.8678/5.1918/5.2584 ms for wgpu
  CPU submission. None observed its starting target; these are local, not
  cross-platform, timing claims.
- Five-repeat `ludoweave.profile.m7/1` base and graphics artifacts validate.
  Remaining simulation cost spans detached query copy/writeback; presentation
  cost spans immutable record construction; packing consumes Python objects
  even where it dominates submission. RFC-0001 therefore defers native code.
- GitHub Actions run `31005165849` passed all 14 M7 jobs: strict
  quality/documentation plus base profile validation; Ubuntu Python
  3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; complete installed
  release-candidate smoke on Ubuntu/Windows/macOS; and real graphics plus wgpu
  profile smoke on all three operating systems. PR #7 is open, mergeable, and
  reports clean merge state against the validated M6 branch.

## External follow-ups

- Verify and reserve the `ludoweave` name before publishing to PyPI.
- Apply `.github/labels.yml` through GitHub settings and open the issue-ready
  starter cards when maintainers are ready to review community contributions.

## Deferred roadmap

Remote/network agent transport, real audio playback, Box2D/rigid-body physics,
networking, visual-editor implementation, automatic device recovery,
international text shaping, 3D, and
native acceleration remain unimplemented. RFC-0001 records that the improved
M1/M3 workloads still miss their targets and defines the complete quantified
admission gate before a native proposal may return.
