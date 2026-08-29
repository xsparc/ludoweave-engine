# Current task

## M179 Windows overlapping guardian rotation

- **Task:** Prove one already-live second guardian retains namespace protection
  after the first overlapping guardian is abruptly reaped and the protected
  range participant later closes.
- **Status:** Fully locally validated at the initial DCO commit; publication is
  withheld because hosted `main` lacks M100-M178. One factual amendment and
  final object audit remain.
- **Base:** Fully locally validated M178 DCO commit
  `e77068a9a2150e6820c979a4b809e76f21d36bc0`, tree
  `2a823e2c312a93e89cf18dcfd8e687001a03bed8`, sole parent exact M177.
- **Branch:** `release/m179-windows-overlapping-guardian-rotation`; exact
  containment allowed the redundant local M178 branch to be pruned.

### M179 acceptance boundary

- Accept RFC-0162 and retain one Windows-only, test-only, current-host NTFS
  observation over M173's exact coordination file, two unchanged M178
  guardians, and M175's unchanged protected participant.
- Require the first guardian to retain original identity, substitution error
  32, and exact exclusive range availability before the participant joins.
- Start the participant and second guardian while the first remains live;
  require original identity, substitution error 32, and exclusive-range error
  33 throughout the three-owner overlap.
- Kill and boundedly wait for the first guardian through M176's helper, then
  require the second guardian and participant still live with both protections.
- Close the participant exactly. With only the second guardian live, require
  original identity and substitution error 32 while exact exclusive range
  acquire/release succeeds.
- Close the second guardian exactly, then require substitution success,
  retained original/displaced identity, distinct replacement identity, exact
  bytes, and complete cleanup without retry or sleep.
- Interpret this only as overlapping rotation. It is not guardian restart,
  crash recovery, election, generation authority, trusted placement, complete
  admission, Windows admission, or cleanup authority.
- Add no fixture, runtime adapter, guardian/lock API, dependency, workflow,
  job/allocation, permission, release authority, or CI change.

### M179 direction evidence

- Microsoft documents that compatible `CreateFileW` requests may coexist and
  that each handle's sharing options remain effective until that handle closes
  regardless of process context.
- Microsoft documents `TerminateProcess` as asynchronous, so survivor
  assertions begin only after M176's bounded process wait completes.
- GitHub documents that every matrix combination creates a job. M179 uses only
  the existing Windows suite and creates no hosted allocation.
- NIST still lists SSDF 1.2 as an Initial Public Draft. M179 retains existing
  governance without a new standards-conformance claim.

### M179 local validation evidence

- Exact M178 is clean; its nine focused assertions pass in 1.08 seconds.
  Static and 2026-08-29 dated strict governance each pass with zero findings
  across three objectives, seven requirements, and four work items.
- Neutral M179 starts from exact M178. Exact containment made local M178
  redundant, so only local `main` and active M179 remain.
- One new integration probe reuses the unchanged M178 guardian twice, the
  unchanged M175 participant, and M176's bounded abrupt-wait helper. One new
  architecture guard protects all prerequisite/runtime/package/CI boundaries.
- Ruff requested one mechanical architecture wrap. After formatting, both new
  Python files are format-clean, Ruff-clean, and strict-Pyright clean. Six
  architecture guards plus the live observation pass seven assertions in 1.02
  seconds; strict docs build in 2.59 seconds and whitespace passes.
- Exactly 12 implementation/public paths currently differ from M178. Public
  identity, high-confidence credential, and local-user-path scans return zero
  findings. No hidden development root is present.
- The unchanged lock resolves 46 packages and the baseline graphics environment
  checks 45 packages. All 546 Python files pass Ruff formatting, Ruff lint, and
  strict Pyright.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 each pass 3,912 tests with 17
  established skips. An initial active-environment sync accidentally replaced
  both intended compatibility environments with 3.12; no test used them. They
  were rebuilt, installed from the frozen export, and their exact interpreter
  versions were verified before the accepted runs.
- The complete 62-module M149-M179 boundary passes 219 tests with one
  established capability skip. Twenty independent central M179 probes pass in
  1.210 to 1.283 seconds wall time. A first read-only PowerShell selection
  wrapper had a parser error and produced no test result; the corrected exact
  31-plus-31 selection is the accepted evidence.
- Ten real-wgpu tests, fresh base and graphics profile schemas, all eight
  profile-validator tests, Clockwork Arena, and Agent World Builder pass with
  their established deterministic identities.
- Strict docs build in 2.69 seconds with only the known Material notice. Static
  and 2026-08-29 dated strict governance return zero findings across three
  objectives, seven requirements, and four work items; whitespace passes.
- Two final record-inclusive builds reproduce a 361,461-byte pure wheel at
  SHA-256
  `b84f692e595f53ce6d6651ecfc2240b5797dfd0b32bc760d9a36c73aca446b2d`
  and a 2,152,246-byte source archive at SHA-256
  `8528e9998243524515a47b3435f0b4a567fb2ed3d740ba2a5ebb05514588e13f`.
  Primary smoke and all 27 additional installed-wheel consumers pass. Two
  ten-artifact release stages are byte-identical and both release smokes pass;
  inventory finds 114 wheel and 881 source entries, no native/WASM/bytecode or
  hidden development root, no M179 wheel entry, and all four exact M179 sources
  in the source archive. Recording this final row changes only the source
  archive afterward.
- Findings-first review has no remaining actionable code, architecture,
  security, documentation, compatibility, scope, or public-hygiene finding.
  Exactly 16 intended paths differ from M178; runtime, examples, scripts,
  workflows, metadata, dependencies, lock, fixture, and M178 remain protected.
- The evidence-inclusive source separator keeps the 46-package lock current,
  all 546 Python files static-clean, all seven focused assertions passing in
  0.99 seconds, the 62-module boundary at 219 passes and one skip, strict docs
  and whitespace passing, and both governance modes at zero findings.
- The final record-only separator keeps both M179 Python files format-, lint-,
  and type-clean; all seven focused assertions pass in 1.06 seconds; strict
  docs build in 2.76 seconds; whitespace and both governance modes pass.
- Forty-six exact ignored M179/test/docs targets were repository-confined and
  checked for tracked content and reparse points. The ordinary identity removed
  39; a separately revalidated approved retry removed the seven ACL-protected
  roots. No exact target remains.
- The pre-commit gate confirms exactly 16 intended paths, unchanged protected
  runtime/package/CI/M178 surfaces, only local `main` and neutral M179,
  configured maintainer identity, whitespace, and zero added/new development-
  identity, local-path, or high-confidence credential-assignment match.
- After the cleanup record, seven focused assertions, strict docs, dated strict
  governance, and whitespace pass once more. The two regenerated ignored
  outputs were independently revalidated, removed, and confirmed absent.

### M179 publication boundary

- Initial DCO commit `186ae451dac6e0a07d2f2001b90ff7ae9a11ba77`, tree
  `26a572cdaedf5da302d9dedfc212bc6a3d163add`, has sole parent exact M178,
  exactly 16 intended paths, one sign-off, matching configured maintainer
  identity, no merge, expected `0 80` divergence, a clean worktree, and
  successful full object checking. This factual record is incorporated by one
  final amendment.
- A fresh pruned fetch leaves hosted `origin/main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, which does not contain M178.
  GitHub reports no open PR, PR #251 as the latest merge, and only remote
  `main`. M179 is not pushed and no PR or hosted workflow allocation is created
  while M100-M178 remain unpublished prerequisites.
- No push, PR, hosted workflow allocation, tag, release, or package publication
  is claimed.
- Publication must not create a new workflow, job, matrix allocation, or
  redundant predecessor branch.

### M179 explicit non-scope

- Guardian discovery, election, restart after failure, zero-owner intervals,
  simultaneous loss, trusted root placement, startup recovery, complete
  admission, hostile prior handles, mapped views, filesystem variation,
  generation, policy, receipts, cleanup authority, or independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, tag,
  release, publication, or version changes.

## Prior task: M178

- **Task:** M178 - prove a protected participant retains its independent
  coordination protections after an overlapping guardian is abruptly
  terminated and reaped.
- **Status:** Fully locally validated at the final DCO commit produced by the
  factual amendment to initial commit
  `c52b38cd4b9923bfe5c750cecb0ddf7c579e2a69`. Publication is withheld because
  hosted `main` lacks M100-M177.
- **Base:** Fully locally validated M177 DCO commit
  `afa5aed0862c4a560a262a61a395b228d56afc3e`, tree
  `cb96284e742a966e6724ae569463171df2d22f25`, sole parent exact M176.
- **Branch:** `release/m178-windows-guardian-abrupt-handoff`; exact containment
  allowed the redundant local M177 branch to be pruned.

### M178 acceptance boundary

- Accept RFC-0161 and retain one Windows-only, test-only, current-host NTFS
  observation over M173's exact coordination file and M175's fixed participant.
- Add one fixed isolated guardian child which accepts no caller-selected path,
  argument, or environment value; opens the final component without following
  a reparse point; rejects reparse identity; proves its handle noninheritable;
  omits delete sharing; and owns no byte-range lock.
- With only the guardian live, require M174 substitution error 32 and exact
  M173 exclusive range acquire/release success.
- Admit M175's unchanged participant on the retained identity and require
  substitution error 32 plus exclusive-range error 33.
- Kill and boundedly wait for the guardian through M176's helper, then require
  the participant still live on the original identity with both refusals intact.
- After exact participant close, require exclusive acquire/release and M174
  substitution success with retained original identity, distinct replacement
  identity, exact bytes, and complete cleanup.
- Interpret this only as one current-host overlapping ownership chain. It is
  not crash recovery, generation authority, trusted placement, complete
  admission, Windows admission, or cleanup authority.
- Add no runtime adapter, guardian/lock API, dependency, workflow,
  job/allocation, permission, release authority, or CI change.

### M178 direction evidence

- Microsoft documents that `CreateFileW` sharing options remain effective
  until each handle closes regardless of process context.
- Microsoft documents that `TerminateProcess` is asynchronous and requires a
  process-object wait before termination can be treated as complete.
- Microsoft documents `LockFileEx` range ownership separately; M178 asserts
  survivor protection only after bounded wait and makes no portable immediate-
  release claim.
- GitHub documents that every matrix combination creates a job. M178 uses only
  the existing Windows suite and creates no hosted allocation.
- NIST still lists SSDF 1.2 as draft. M178 retains existing governance and
  makes no new standard-conformance claim.

### M178 development evidence so far

- Exact M177 is clean with expected `0 78` divergence from local M99 main. Its
  seven focused assertions pass in 0.83 seconds.
- Static and 2026-08-29 dated strict governance each pass with zero findings
  across three objectives, seven requirements, and four work items.
- Neutral M178 starts from exact M177. Exact containment made local M177
  redundant, so only local `main` and active M178 remain.
- Ruff mechanically reformatted one new integration file. Findings-first
  review then added an acknowledged-close observation, pinned exact null-
  security/no-follow construction, explicitly forbade delete sharing, and
  narrowed one documentation claim to the construction actually exercised.
- All 544 Python files are format-clean, Ruff-clean, and strict-Pyright clean.
  The corrected M178 group passes nine assertions on exact CPython 3.12.13,
  3.13.13, and 3.14.5; the exact 60-module M149-M178 boundary passes 212 tests
  with one established skip.
- Before that test-only review correction, the complete suite passed 3,904
  tests with 17 skips on each supported interpreter. Twenty central abrupt-
  handoff repetitions, real-wgpu, both profiles, Clockwork Arena, Agent World
  Builder, all 28 wheel consumers, and two reproducible release stages pass.
- Strict docs, static and dated strict governance, whitespace, exact 17-path
  scope, protected surfaces, and public identity/credential/local-path scans
  pass. No workflow or dependency changed.
- Two evidence-inclusive builds reproduce the unchanged 361,396-byte pure
  wheel and identical 2,143,429-byte source archives. Primary installed-wheel
  smoke, two byte-identical ten-artifact release stages, both release smokes,
  and archive inventory pass.
- The record-only separator keeps all three M178 modules clean and passes nine
  focused assertions, strict docs, whitespace, and both governance modes.
  Guarded cleanup removed all 47 exact M178/pytest/docs scratch targets after
  repository confinement, tracked-content, and recursive reparse checks.
- Pre-commit audit confirms exactly 17 intended paths, zero protected-surface
  diff, zero public identity/credential/local-path finding, zero scratch, only
  local `main` plus neutral M178, and configured maintainer identity.

### M178 publication boundary

- Fresh hosted audit leaves `origin/main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; it does not contain M177. No PR
  is open, PR #251 remains the latest merge, and `main` is the only remote
  branch. No M178 push, PR, hosted workflow allocation, tag, or release occurs.
- Publication must not create a new workflow, job, matrix allocation, or
  redundant predecessor branch.

### M178 explicit non-scope

- Guardian restart, a zero-owner interval, multiple guardians, trusted root
  placement, startup recovery, complete participant admission, hostile prior
  handles, mapped views, filesystem variation, generation, policy, receipts,
  cleanup authority, or independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, tag,
  release, publication, or version changes.

## Earlier task: M177

- **Task:** Prove one protected guardian can bridge a participant-free
  coordination interval and hand namespace protection to a later participant.
- **Status:** Fully locally validated at DCO commit
  `afa5aed0862c4a560a262a61a395b228d56afc3e`; publication was withheld because
  hosted `main` lacks M100-M176.

## Earlier task: M176

- **Task:** M176 - prove bounded abrupt settlement of M175 protected
  coordination participants while preserving survivor ownership.
- **Status:** Direction, implementation, supported-Python regression,
  rendering, distribution, release rehearsal, documentation, governance,
  findings-first review, evidence-inclusive closure, record-only separator,
  exact scratch cleanup, pre-commit audit, initial local DCO commit, and
  publication-safety gates pass. Publication is correctly withheld because
  hosted `main` lacks M100-M175; the final amended-object audit follows this
  factual record.
- **Base:** Fully locally validated M175 DCO commit
  `9e5d440b9c16687c7291c6abdf63b806b2cd33cf`, tree
  `630dfc51f599a5bf1298e6538441da589d77e9f0`, sole parent exact M174.
- **Branch:** `release/m176-windows-protected-lock-abrupt-settlement`; exact
  containment allowed the redundant local M175 branch to be pruned.

## Acceptance boundary

- Accept RFC-0159 and retain one Windows-only, test-only, current-host NTFS
  observation over two M175 protected coordination participants.
- Require both participants to refuse pathname substitution/error 32 and
  exclusive range ownership/error 33 before termination.
- Kill and boundedly wait for the first participant. Require nonzero status,
  stdout EOF after `ready`, empty stderr, no graceful `closed`, and both
  refusals to persist through the survivor.
- Kill and boundedly wait for the survivor. Without retry or sleep, require
  exact exclusive acquire/release and then M174 substitution success with
  retained original identity, distinct replacement identity, and exact bytes.
- Interpret this only as current-host abrupt settlement after completed process
  wait. It is not a portable immediate-release guarantee, crash recovery,
  generation authority, Windows admission, or cleanup authority.
- Add no fixture, runtime adapter, lock API, cleanup authority, dependency,
  workflow, job/allocation, permission, release authority, or CI change.

## Direction evidence

- Microsoft documents `TerminateProcess` as asynchronous and requires a wait
  when completed termination matters. Python documents that Windows
  `Popen.kill()` uses that termination path.
- Microsoft documents that the operating system unlocks outstanding
  `LockFileEx` ranges after process termination or file close, while warning
  that settlement time depends on available system resources.
- GitHub documents that each matrix combination creates another job. M176 uses
  only the existing Windows suite and creates no hosted allocation.
- NIST SSDF 1.2 remains a draft. The bounded observation is adopted without
  claiming a newer final standard or promoting runtime authority.

## Development evidence so far

- Exact M175 was clean with expected `0 76` divergence from local M99 main.
  Its seven focused assertions pass in 0.58 seconds. Static and dated strict
  governance each return zero findings.
- The first M176 live observation passes in 0.53 seconds with strict Pyright
  and Ruff clean. The first complete gate found only one mechanical architecture
  format request and one correctly detected split `zero-participant` phrase.
  After both corrections, all seven architecture/live assertions pass in 0.61
  seconds; strict docs build in 2.53 seconds; whitespace passes.
- All 539 Python files pass static checks. Exact CPython 3.12.13 passes 3,889
  tests/17 skips; exact 3.13.13 and 3.14.5 pass 3,879 tests/18 skips each.
- The M149-M176 boundary passes 196 tests with one established skip; twenty
  consecutive live probes pass. Ten real-wgpu tests, both profiles, Clockwork
  Arena, and Agent World Builder pass.
- Two pre-review development builds and two ten-artifact release stages are
  byte-identical; all 28 installed-wheel consumers and both release smokes
  pass. Static and dated strict governance each return zero findings.
- Findings-first review found no code defect and corrected one overly broad
  claim from wheel contents to the actual wheel package boundary. Scope,
  protected-surface, public-identity, credential, and local-path scans pass.
- Evidence-inclusive builds reproduce the unchanged wheel and identical
  2,125,029-byte source archives; installed-wheel smoke and two identical
  ten-artifact release stages pass. The record-only separator keeps both M176
  Python files format-clean, Ruff-clean, and strict-Pyright clean; all seven
  focused assertions, strict docs, whitespace, and both strict governance
  modes pass. Guarded cleanup removed all 46 repository-confined, untracked,
  non-reparse M176/pytest scratch targets. Commit and hosted publication-safety
  evidence pass. The pre-commit audit confirms exact 16-path scope, zero
  protected-surface or public-hygiene finding, zero scratch, only local `main`
  plus active M176, and the configured maintainer identity.
- Initial DCO commit `cbe6ea913c1707262b195741b580b9123adf706c`
  has tree `313400db57958c708b407efede620ba5578a755d`, sole parent exact
  M175, exactly 16 paths, truthful configured identity, one sign-off, expected
  `0 77` divergence, a clean worktree, and successful full object check.

## Publication boundary

- Fresh hosted `main` is exact M99, no PR is open, PR #251 is the latest merge,
  and no remote topic branch exists. M176 is 77 commits ahead and contains the
  unpublished M100-M175 prerequisite stack. No branch was pushed, no PR was
  opened, and no hosted workflow allocation was started.
- Publication must not create a new workflow, job, matrix allocation, or
  redundant predecessor branch.

## Explicit non-scope

- A portable operating-system unlock deadline, arbitrary termination timing,
  process trees, startup/crash recovery, job objects, mapped views, filesystem
  variation, trusted-root placement, complete participant admission,
  generation issuance/retention, policy, receipts, or independent-host proof.
- Zero-participant substitution exclusion, cache-root integration, candidate
  policy, cleanup authority, Windows admission, or a production adapter.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, tag,
  release, publication, or version changes.

## Prior task

- **Task:** M175 - prove whether cooperative participants that deny delete
  sharing exclude M174 pathname substitution throughout the live-ownership
  interval.
- **Status:** Direction, implementation, findings-first correction,
  supported-Python regression, rendering, distribution, release rehearsal,
  documentation, governance, evidence-inclusive closure, record-only
  separator, exact scratch cleanup, local DCO commit, and publication-safety
  gates pass. Publication is correctly withheld because hosted `main` still
  lacks M100-M174; the final amended-object audit follows this factual record.
- **Base:** Fully locally validated M174 DCO commit
  `f4aa920fa3b6cbcb8a9711111aaeb102f60902d4`, tree
  `3fe906267b6c89708d8f2a6fa5926a4e4184404a`, sole parent exact M173.
- **Branch:** `release/m175-windows-live-substitution-exclusion`; exact
  containment allowed the redundant local M174 branch to be pruned.

## Acceptance boundary

- Accept RFC-0158 and retain one Windows-only, test-only, current-host NTFS
  observation over two simultaneous shared-range participants that omit
  `FILE_SHARE_DELETE` on one fixed coordination file.
- Require pathname substitution to fail with native sharing error 32 and an
  exclusive range owner to fail with native lock error 33 while two, then one,
  cooperative participant remains live.
- After the final participant closes, require exact exclusive acquire/release,
  then successful M174 substitution with the displaced identity equal to the
  original and different from the replacement.
- Preserve exact file bytes, noninheritable handles, bounded canonical child
  output, deterministic settlement, and all M174/runtime/package/CI surfaces.
- Interpret this only as a continuous cooperative live-ownership boundary. It
  does not cover the zero-participant gap, uncooperative actors, admission, or
  cleanup authority.
- Add no runtime adapter, lock API, cleanup authority, dependency, workflow,
  job/allocation, permission, release authority, or CI change.

## Direction evidence

- Microsoft documents that `CreateFileW` share modes remain effective until
  handle close, and that omitting delete sharing prevents later delete-access
  opens, including rename access.
- Microsoft documents `LockFileEx` as a cooperative handle/range primitive,
  `MoveFileExW` as a native move operation, and `FILE_ID_INFO` as stable volume
  and file identity for same-computer comparisons.
- GitHub documents that each matrix combination creates another job. M175 uses
  only the existing Windows suite and creates no hosted allocation.
- NIST SSDF 1.2 remains a draft. The bounded observation is adopted without
  claiming a newer final standard or promoting runtime authority.

## Development evidence so far

- Exact M174 was clean, its seven focused assertions passed in 0.50 seconds,
  and both static and dated strict governance returned zero findings.
- The fixed protected participant, live integration test, and six architecture
  guards pass strict Pyright and Ruff. Ruff requested only mechanical format
  corrections. The corrected focused set passes seven assertions in 0.57
  seconds; strict docs build in 2.67 seconds with only the known Material
  notice; whitespace passes.
- Findings-first review identified and corrected one participant-startup
  cleanup gap. The reviewed tree passes all 537-file static checks, exact
  CPython 3.12.13 with 3,882 tests/17 skips, and exact 3.13.13 and 3.14.5 with
  3,872 tests/18 skips each.
- The reviewed M149-M175 boundary passes 189 tests with one established skip;
  twenty consecutive corrected live probes pass. Ten real-wgpu tests, both
  profiles, Clockwork Arena, and Agent World Builder pass.
- Two pre-review development builds and two ten-artifact release stages are
  byte-identical; all 28 installed-wheel consumers and both release smokes
  pass. Static and dated strict governance each return zero findings.
- Evidence-inclusive builds reproduce the unchanged wheel and identical
  2,116,472-byte source archives; installed-wheel smoke and two identical
  ten-artifact release stages pass. The final source, governance, scope, and
  public-hygiene separator passes.
- The record-only separator keeps all three M175 files format-clean,
  Ruff-clean, and strict-Pyright clean; seven assertions, strict docs,
  whitespace, and both strict governance modes pass.
- Exact guarded cleanup removed 68 M175 scratch targets and the generated
  pytest root; all are confirmed absent.
- Initial DCO commit `81a97157914d7f6be236c8f5a7e4bfda03fd362d`
  has tree `7effa8279d5a641d8f5cc602f888c354d531efe5`, sole parent exact
  M174, exactly 17 paths, truthful configured identity, one sign-off, expected
  `0 76` divergence, a clean worktree, and successful full object check.

## Publication boundary

- Fresh hosted `main` is exact M99, no PR is open, and PR #251 is the latest
  merge. M175 is 76 commits ahead and contains the unpublished M100-M174
  prerequisite stack. No branch was pushed, no PR was opened, and no hosted
  workflow allocation was started.
- Publication must not create a new workflow, job, matrix allocation, or
  redundant predecessor branch.

## Explicit non-scope

- A production identity/generation protocol, trusted-root placement,
  uncooperative actors, complete participant admission, zero-participant
  substitution exclusion, mapped views, multiple ranges, wait/fairness policy,
  cancellation, abrupt exit, delayed operating-system unlock, native close or
  unlock failure, filesystem variation, recovery, policy, receipts, or
  independent-host proof.
- Cache-root integration, candidate policy, cleanup authority, Windows
  admission, or a private production adapter.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, tag,
  release, publication, or version changes.

## Prior task

- **Task:** M174 - prove whether pathname substitution splits M173's
  cooperative Windows coordination barrier across file identities.
- **Status:** Direction, implementation, supported-Python regression,
  rendering, distribution, release rehearsal, documentation, and governance
  gates pass. Evidence-inclusive closure and findings-first review pass; final
  record separator and exact scratch cleanup pass. Commit and publication-
  safety gates pass. The exact 17-path pre-commit scope and hygiene gate passes.
  Publication is correctly withheld because hosted `main` still lacks
  M100-M173; the final amended-object audit follows this factual record.
- **Base:** Fully locally validated M173 DCO commit
  `767337f7ea8138bdc14455296c54d0261cd20e9e`, tree
  `114a874eb76a920b334fbf26190efc4cf63a0f97`, sole parent exact M172.
- **Branch:** `release/m174-windows-lock-substitution`; exact containment
  allowed the redundant local M173 branch to be pruned.

## Acceptance boundary

- Accept RFC-0157 and retain one Windows-only, test-only, current-host NTFS
  observation that renaming and replacing `live/coordination.lock` splits old
  and new M173 participants across independent file identities and lock
  generations.
- Preserve M173, runtime, examples, scripts, dependencies, workflows,
  metadata, and lock byte-for-byte.
- Use one fixed isolated namespace child with no argument or environment
  behavior. Require exact `MoveFileExW` rename, ordinary replacement creation,
  exact bytes, a noninheritable handle, bounded canonical output, and
  deterministic close.
- Prove retained-original identity equals displaced identity and differs from
  replacement identity using `FILE_ID_INFO`.
- Keep unchanged M173 participants live on both identities. Require independent
  exclusive refusal, then prove replacement exclusive ownership succeeds while
  the original participant remains live and the displaced original still
  refuses ownership.
- Record the result as negative capability evidence. It is not participant
  completeness, substitution resistance, Windows admission, or cleanup
  authority.
- Add no runtime adapter, lock API, cleanup authority, dependency, workflow,
  job/allocation, permission, release authority, or CI change.

## Direction evidence

- Microsoft documents `LockFileEx` as a handle/file-range primitive and
  `FILE_ID_INFO` as the volume/file identity for same-computer comparisons.
- Microsoft documents that `FILE_SHARE_DELETE` permits later rename/delete
  access and `MoveFileExW` moves an existing object to another name.
- GitHub documents that each matrix combination creates another job. M174 uses
  only the existing Windows suite and creates no hosted allocation.
- NIST SSDF remains outcome- and risk-oriented; version 1.2 is still a draft.
  The bounded substitution observation is adopted without claiming a newer
  final standard or promoting runtime authority.

## Development evidence so far

- Exact M173 was clean with expected `0 74` divergence from hosted/local M99
  main. Its ten focused architecture/live assertions pass in 0.45 seconds.
  Static and dated strict governance each return zero findings.
- The fixed namespace child and parent integration probe pass strict Pyright.
  The first Ruff run identified only mechanical import ordering; the exact
  correction passes Ruff. The first live observation passes in 0.37 seconds.
- Six new architecture guards plus the live observation pass seven assertions
  in 0.49 seconds. Strict documentation builds in 2.70 seconds with only the
  known Material notice. Ruff formatting requested one mechanical architecture
  wrap; the corrected focused gate passes seven assertions in 0.46 seconds and
  strict docs in 2.47 seconds.
- All 534 Python files pass Ruff formatting, Ruff, and strict Pyright. Exact
  CPython 3.12.13 passes 3,875 tests with 17 skips; exact CPython 3.13.13 and
  3.14.5 each pass 3,865 tests with 18 skips.
- The complete M149-M174 Windows boundary passes 182 tests with one established
  skip. Twenty consecutive live substitutions pass. Ten real-wgpu tests, both
  one-repeat profiles, Clockwork Arena, and Agent World Builder pass.
- Two development builds are byte-identical: a 361,088-byte pure wheel at
  SHA-256 `b6a6f5e75861d3b483533b0abbb110aa058b7b1d9c880948cbdd4f6e96d47acc`
  and a 2,105,817-byte source archive at SHA-256
  `b7d6ea6be098cd0ce3257c99c732a42f6f455232bdb08c218abe5a37c54dc777`.
  Installed-wheel smoke passes; two ten-artifact release stages are identical
  and both complete release smokes pass.
- Final static and dated strict governance checks return zero findings. The
  evidence-inclusive reproduction retains the exact wheel and produces two
  identical 2,107,218-byte source archives at SHA-256
  `8e68012e170376d26657e5d0b0f47568b094bf24fa920123da7041ccf6ca89a9`.
  Installed-wheel smoke, two identical ten-artifact release stages, and both
  release smokes pass.
- Findings-first review found no remaining actionable defect. Public identity,
  added credential/local-path, protected-surface, package-boundary, and scope
  scans pass after replacing two unnecessarily explicit control-pattern names
  with neutral wording.

## Publication boundary

- Fresh hosted `main` is exact M99, no PR is open, and PR #251 is the latest
  merge. M174 is 75 commits ahead and contains the unpublished M100-M173
  prerequisite stack. No branch was pushed, no PR was opened, and no hosted
  workflow allocation was started.
- Publication must not create a new workflow, job, matrix allocation, or
  redundant predecessor branch.

## Explicit non-scope

- A production identity/generation protocol, trusted-root placement,
  uncooperative actors, complete participant admission, mapped views,
  multiple ranges, wait/fairness policy, cancellation, abrupt exit, delayed
  operating-system unlock, native close/unlock failure, filesystem variation,
  recovery, policy, receipts, or independent-host proof.
- Cache-root integration, candidate policy, cleanup authority, Windows
  admission, or a private production adapter.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, tag,
  release, publication, or version changes.
