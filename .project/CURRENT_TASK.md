# Current task

## M216 Windows retained launch-source access-refusal probe

- **Task:** Exercise one fixed, access-only Windows share-refusal probe around
  the exact frozen M212-M215 launch-source boundary without writing, deleting,
  collecting, cleaning, or admitting Windows cleanup.
- **Status:** Implementation, complete local validation, record-state
  packaging, findings-first review, guarded cleanup, final closeout, and the
  local DCO commit are finished. Publication is withheld because hosted
  `main` lacks the M100-M215 prerequisite stack.
- **Base:** exact fully locally validated M215 DCO commit
  `b1cc04bdc0dc93c0a757e2cf2e6ae655efd05e7f`, tree
  `7da8fcc38bf90ed59449aea466f11383808bf737`, with sole parent exact M214.
- **Branch:**
  `release/m216-windows-retained-launch-source-access-refusal-probe`; exact
  containment made the local M215 branch name redundant, so only local `main`
  and active M216 remain.

### M216 acceptance boundary

- Retain the fixed M215 participant source read-only with only read sharing.
- Request access-only `GENERIC_WRITE` and `DELETE` opens using the competing
  read/write/delete share mode and `OPEN_EXISTING`; require exact native error
  32 before launch, after connection, and after `ready`.
- After child settlement and closure of the retained source handle, require
  both access opens to succeed and close without exercising either right.
- Prove the bounded source snapshot is unchanged after every observation.
- Exclude `WriteFile`, truncation, replacement, rename, move, and delete APIs;
  protect the exact M215 boundary and every runtime, package, fixture, example,
  script, benchmark, workflow, dependency, lock, and version surface.
- Keep source provenance, hostile filesystem races, distinct-principal and
  independent-host proof, collection, cleanup, criteria 6/7, and Windows
  admission unresolved. Add zero GitHub Actions jobs or hosted allocation.

### Validation evidence so far

- The exact M215 handoff passed 34 tests; static and dated-strict governance
  checks passed with zero findings before implementation.
- The intentional red failed only because the selected M216 probe and decision
  files were absent. Development corrected one architecture-audit expression,
  one native invalid-handle representation, and one exact documentation phrase.
  Final focused formatting, Ruff, strict Pyright, strict docs, whitespace, and
  all 24 M216 architecture/live tests pass.
- All 618 Python files are format-clean; Ruff and strict Pyright report zero
  findings; architecture plus the live M216 probe passes 2,287 tests with one
  inherited capability skip.
- Complete isolated all-group graphics suites pass 4,434 tests with 19 skips
  on each CPython 3.12, 3.13, and 3.14.
- Ten real-wgpu tests, both one-repeat profile contracts, eight profile tests,
  two Null Clockwork repeats, wgpu Clockwork, and Agent World Builder pass.
- Two builds reproduce a 364,763-byte pure wheel at SHA-256
  `d4f6d66bf7d786ead6fe0b8186df5509f89fdd17272f2c8f10e8f308ef79d0d1`
  and 2,562,119-byte source archive at SHA-256
  `f94d7f43cd5e0f62a807e9997f97ca3718ea21f77c8dab61f827e2aa4a3e2077`.
  Installed wheel/scene smokes and two byte-identical ten-artifact release
  rehearsals pass. The 114-entry wheel contains no M216 file; the integration
  probe, architecture guard, RFC, and security guide occur once in the
  1,030-entry source archive.
- Record-inclusive static/type/architecture/docs/governance/whitespace gates
  pass. Two record-state builds reproduce the unchanged wheel and identical
  2,564,768-byte source archives at SHA-256
  `3d92c7e824135282cd0f618ef7920efe0cca11f68b71e941356da60719922c7b`;
  installed smokes and both exact release rehearsals pass.
- Findings-first review confirms exactly 16 intended paths, no protected
  product/tooling/fixture/CI/dependency/lock change, no mutation operation or
  authority increase, correct handle closure and exact-error behavior, and no
  actionable finding. Commit-object audit and hosted publication-safety review
  remain to be completed.
- An access-enabled audit proved all 23 M216 scratch/documentation targets and
  45,944 descendants repository-confined, ignored, untracked, and recursively
  reparse-free before exact removal. Zero target remains; older generated
  outputs and all inaccessible M212 roots were untouched.
- The post-cleanup 618-file static/type gate, exact 24-test M216 boundary,
  strict docs, dated-strict governance, and whitespace pass. The regenerated
  ignored documentation directory and its 756 descendants were separately
  proven confined, untracked, and reparse-free before exact removal; no M216
  scratch remains.
- Pre-commit audit confirms exact M215 history/tree/parent, exactly 16 intended
  paths, only local `main` plus active neutral M216, expected `0 116`
  divergence, configured maintainer identity, zero protected-surface change,
  zero M216 scratch, absent retired root metadata, zero added identity-
  disclosure match, clean whitespace, and connected Git objects.
- Initial DCO commit `3eb4bf6de41b372d0c4cab6a6bf1a0b30896241f`, tree
  `ac36a4224d4a04ac841ac2622834533bcba7b876`, has sole parent exact M215,
  exactly 16 paths, one matching sign-off, consistent maintainer identity,
  clean revision/worktree/connectivity, and expected `0 117` divergence. This
  factual record is incorporated by the closeout amendments.
- Fresh pruned fetch and direct remote-head lookup leave public `origin/main`
  at exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; M215 is absent,
  M99 is present, only remote `main` exists, and divergence is `0 117`.
  Authentication is valid; the repository is public, unarchived, and defaults
  to `main`; PR #251 remains latest. Publishing M216 would expose absent
  M100-M215 prerequisites, so no push, PR, hosted allocation, tag, release, or
  package publication occurs.

## M215 Windows retained launch-source binding probe

- **Task:** Exercise one fixed, test-only retained participant-source check on
  the exact frozen M212-M214 process, control, token, session, and executable
  boundary without collection, cleanup authority, or Windows admission.
- **Status:** Fully locally validated, findings-first reviewed, and locally
  DCO-committed; record-state packaging and guarded scratch cleanup pass.
  Publication is withheld because hosted `main` lacks the M100-M214
  prerequisite stack.
- **Base:** exact fully locally validated M214 DCO commit
  `8da9809a9505437175c09e439e43caca84e7333a`, tree
  `6b06cdd6e404cde29bc705054ff3d5bad8dd9838`, with sole parent exact M213.
- **Branch:** `release/m215-windows-retained-launch-source-binding-probe`;
  exact containment made the local M214 branch name redundant, so only local
  `main` and active M215 remain.

### M215 acceptance boundary

- Open the fixed participant source read-only before launch, retain it through
  settlement, and privately snapshot normalized name, volume/file ID, bounded
  size, and SHA-256 before child creation.
- Rewind the source and launch fixed direct `pythonw.exe -I -B -` so Python
  consumes the retained bytes from inherited standard input rather than
  reopening a script pathname.
- Use `STARTUPINFOEXW` with an exact three-handle allowlist containing only the
  source and distinct write-only `NUL` output/error handles.
- After exact M212-M214 bindings and challenge/ready, recheck source, retained
  token, expected image, and observed image before release; retain native
  client/session/DACL checks as pre-challenge prerequisites, fail closed on
  drift, and close every new handle once.
- Protect all runtime, package, example, script, benchmark, workflow,
  dependency, lock, version, fixture, and M214 surfaces.
- Keep imported-module bytes, interpreter state, source-commit provenance,
  hostile ABA resistance, distinct-principal and independent-host proof,
  collection, cleanup, criteria 6/7, and Windows admission unresolved.
- Add zero GitHub Actions jobs or hosted allocation.

### Validation evidence so far

- The exact M214 handoff passed 23 tests; static and dated-strict governance
  each passed with zero findings before the branch was created.
- The intentional red failed only because the probe and decision files were
  absent. The first code-only guard then found two audit-expression mismatches;
  explicit source-bound aliases and a correctly scoped fixed-command check
  corrected them. Focused formatting, Ruff, strict Pyright, strict docs, and all
  34 M215 architecture/live tests pass.
- All 616 Python files pass formatting and Ruff; strict Pyright reports zero
  findings; architecture plus the live M215 probe passes 2,284 tests with one
  inherited capability skip.
- Complete isolated all-group graphics suites pass 4,410 tests with 19 skips
  on each CPython 3.12, 3.13, and 3.14.
- Ten real-wgpu tests, both one-repeat profile contracts, eight profile tests,
  two Null Clockwork repeats, wgpu Clockwork, and Agent World Builder pass.
- Two builds reproduce a 364,667-byte pure wheel at SHA-256
  `2e6b684275653afcfa6c2d413ec06c3f6988d8fd74a9aa006d26ca3330bd7cdb`
  and 2,551,937-byte source archive at SHA-256
  `85653a8e7d72ffbe210708ffbdfea36a4c970b787c32025ad4a12916ecbc41b3`.
  Installed wheel/scene smokes and two byte-identical ten-artifact release
  rehearsals pass. The 114-entry wheel contains no M215 file; all four new
  implementation/decision files occur once in the 1,026-entry source archive.
- Record-inclusive static, type, architecture/live, strict docs, governance,
  and whitespace gates pass. Two record-state builds reproduce the unchanged
  wheel and identical 2,554,519-byte source archives at SHA-256
  `274409936034d9d5b54f30ca0a8d8624d3b28db9f324ada10b8475af952ec947`;
  installed smokes and both byte-identical release stages pass.
- Findings-first review corrected one documentation overclaim so native
  client/session/DACL checks are described as pre-challenge prerequisites,
  while only the source, retained token, and expected/observed image handles
  are claimed as rechecked after `ready`. One unused native constant was
  removed. The corrected 34-test focused boundary and all static/docs gates
  pass; no actionable finding remains.
- All 25 M215 generated targets and 47,425 descendants were proven
  repository-confined, ignored, untracked, and reparse-free before exact
  removal across the primary and regenerated-documentation cleanup. Zero M215
  target remains; older output and all inaccessible M212 roots were untouched.
- Pre-commit audit confirms exact M214 history/tree/parent, exactly 16 intended
  paths, only local `main` plus active M215, configured maintainer identity,
  expected `0 115` pre-commit divergence, zero protected-surface change, zero
  M215 scratch, absent retired root metadata, clean whitespace, and connected
  Git objects.
- Initial DCO commit `6903bab3fe9fad9310365aa05ef3482e7a0a21c5`,
  tree `c56b4b071f11037bd9730af1193780a7b1158f21`, has sole parent exact
  M214, exactly 16 paths, one matching sign-off, consistent maintainer
  identity, expected `0 116` divergence, a clean worktree/revision, and
  connected objects. This factual record is incorporated by the closeout
  amendments.
- Fresh pruned fetch and direct remote-head lookup leave public `origin/main`
  at exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; M214 is absent,
  M99 is present, and only remote `main` exists. Divergence is `0 116`.
  Authentication is valid; the repository is public, unarchived, and defaults
  to `main`; PR #251 remains latest. No push, PR, or hosted allocation occurs.

## M214 Windows retained process-image binding probe

- **Task:** Exercise one fixed, test-only retained executable-image check on
  the exact frozen M212/M213 process, control, token, and session boundary
  without collection, cleanup authority, or Windows admission.
- **Status:** Fully locally validated, reviewed, and DCO-committed; record-state
  packaging and guarded scratch cleanup are complete. Publication is withheld
  because hosted `main` lacks the M100-M213 prerequisite stack.
- **Base:** exact fully locally validated M213 DCO commit
  `217d29d07fddf0d123d6c6c903b4133806f226fc`, tree
  `5f5ac6b6cb9ac7073b37ac9d0aeac469b08fa6bb`, with sole parent exact M212.
- **Branch:** `release/m214-windows-retained-process-image-binding-probe`;
  exact containment made the local M213 branch name redundant, so only local
  `main` and active M214 remain.

### M214 acceptance boundary

- Retain a read-only handle to the fixed direct `pythonw.exe` before launch.
- After exact M212 process/pipe and M213 token/session binding, query the image
  through the retained process handle and retain a read-only handle to it.
- Compare private filesystem-target-normalized name, volume serial, 128-bit
  file ID, size bounded to 64 MiB, and SHA-256 from fixed 64 KiB reads.
- Recheck both retained handles after `ready` and before `release`; fail closed
  on any drift and close every new handle exactly once.
- Protect the exact M213 boundary and all runtime, package, example, script,
  benchmark, workflow, dependency, lock, and version surfaces.
- Keep script/import bytes, hostile ABA resistance, distinct-principal and
  independent-host proof, collection, cleanup, criteria 6/7, and Windows
  admission explicitly unresolved.
- Add zero GitHub Actions jobs or hosted allocation.

### Current evidence

- The exact M213 handoff passed 25 tests; static and dated-strict governance
  each passed with zero findings before the branch was created.
- The intentional red failed only because the new probe and decision files
  were absent. Focused implementation and decision coverage now passes all 23
  tests; all 614 Python files pass formatting and Ruff, strict Pyright reports
  zero findings, and architecture plus the live M214 probe passes 2,262 tests
  with one inherited capability skip.
- Complete isolated all-group graphics suites pass 4,376 tests with 19 skips
  on each CPython 3.12, 3.13, and 3.14.
- Ten real-wgpu tests, both one-repeat profile contracts and eight profile
  tests, Null/wgpu Clockwork Arena, and Agent World Builder pass.
- Two initial and two record-state builds reproduce a 364,573-byte pure wheel
  at SHA-256
  `4b45de86d48bb02879b9b336de24c055616071555a94b9bac6353b0803f23dd6`
  and the record-state 2,543,397-byte source archive at SHA-256
  `011df8367b00f77c93ad81bdeac4d37ee0e84da8026b6be029fcc5469bcf4143`.
  Installed wheel/scene smokes and two byte-identical ten-artifact release
  rehearsals pass. The 114-entry wheel contains no M214 file; all four new
  implementation/decision files occur once in the 1,022-entry source archive.
- Final review confirms exactly 16 intended paths, no protected product,
  tooling, CI, metadata, dependency, or lock change, no sensitive disclosure,
  and no authority increase. Twenty exact M214 generated targets were proven
  confined, ignored, untracked, and recursively reparse-free immediately
  before removal. The one documentation directory regenerated by the closeout
  gate received the same audit and exact removal; zero remains and the
  inaccessible M212 roots were untouched.
- Initial DCO commit `1adc5e98a7316d0d01ee2d8ecdec636ee69af5f5`,
  tree `6fe399c064519dbdaa972af1213135c950427cde`, has sole parent exact
  M213, exactly 16 intended paths, one matching sign-off, consistent maintainer
  identity, clean worktree/revision/connectivity, and expected `0 115`
  local-main divergence. This closeout record is incorporated by one amendment.
- A fresh pruned fetch and direct remote-head query leave public `origin/main`
  at exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; M213 is absent,
  only remote `main` exists, and hosted divergence is `0 115`. Authentication
  is valid, the repository is public and unarchived with `main` as default,
  and PR #251 remains latest. No push, PR, or hosted allocation occurs.

## M213 Windows local control token-binding probe

- **Task:** Exercise one fixed, test-only retained client-token and native
  session-binding check on the exact frozen M212 local control channel without
  impersonation, collection, cleanup authority, or Windows admission.
- **Status:** Fully locally validated and DCO-committed; project-record
  closeout, guarded scratch cleanup, and publication-safety review are
  complete. Publication is withheld because hosted `main` lacks the M100-M212
  prerequisite stack.
- **Base:** fully locally validated M212 DCO commit
  `98500e9fbe0eda9997d54d729200ba7acdbf05ef`, tree
  `7c26481ed145ed912fb7e6acb819ec17448c8f1a`, with sole parent exact M211.
- **Branch:** `release/m213-windows-local-control-token-binding-probe`; exact
  containment made the local M212 branch name redundant, so only local `main`
  and active M213 remain.

### M213 acceptance boundary

- Open and retain the M212 participant process's primary token with query-only
  access across challenge/ready; privately copy user SID, logon SID,
  authentication ID, token ID, modified ID, session ID, and token type.
- Require the participant to use a primary token and match the controller's
  user, logon, authentication, and session identity.
- Require native pipe-client, retained-process, and participant-token session
  identifiers to agree; revalidate M212's exact DACL against the copied
  participant logon SID.
- Re-query the same retained token after `ready` and before `release`; fail
  closed on any identity drift and explicitly close every token handle.
- Use no impersonation, alternate-account launch, credential lifecycle,
  privilege adjustment, runtime/package surface, fixture mutation, cleanup
  authority, workflow, public runner, or hosted allocation.

### Validation evidence so far

- Exact M212 handoff passed 17 tests; static and dated-strict governance each
  report zero findings. The intentional architecture red recorded 9 expected
  missing-artifact/registration failures and 2 protected-boundary passes.
- Focused formatting, Ruff, strict Pyright, and all 25 M213 architecture/live
  tests pass. The complete architecture plus live M213 group passes 2,253 tests
  with one supported-capability skip.
- All 612 Python files are format-clean; Ruff and strict Pyright report zero
  findings. Strict docs, both governance modes, and whitespace pass.
- Complete isolated suites pass identical totals of 4,353 tests with 19 skips
  on CPython 3.12, 3.13, and 3.14.
- Ten real-wgpu tests, fresh base/graphics profiles, all eight profile-schema
  tests, Null/wgpu Clockwork Arena, and Agent World Builder pass. Fresh repeated
  Clockwork observations agree at state `sha256:c4a5bbedca3a9eb40dbf20745207aeade4e7254e5a5bdd801e64b767a1cce0a0`
  and 15 sprites; this supersedes the stale M212 narrative for the same current
  three-tick invocation without changing frozen runtime code.
- Final record-state distributions are byte-identical: the 364,461-byte pure wheel is SHA-256
  `906099ccbb2351cd40e6959b35b9ea47ebf9151b6da08e6839905e00cff3a83d`
  and the 2,534,018-byte source archive is SHA-256
  `0c43685178018c0bced374a2749978630f55891fdce6f99f22ef114d4379141e`.
  Installed wheel/scene smokes and two ten-artifact release rehearsals pass;
  exact release inventories have zero difference. The wheel has 114 entries
  and no M213 file; all four M213 implementation/decision files occur once in
  the 1,018-entry source archive.
- Findings-first review confirms 12 pre-record intended paths, zero runtime,
  package, example, script, benchmark, workflow, metadata, dependency, or lock
  diff, and no actionable correctness, authority, security, architecture,
  documentation, compatibility, package-boundary, or CI-allocation finding.
- A read-only audit proved all 15 M213 scratch targets repository-confined,
  ignored, untracked, and recursively reparse-free. Immediate exact
  revalidation removed all 15; zero M213 scratch target remains. Previously
  disclosed inaccessible M212 roots were not touched.
- The record-inclusive separator keeps all 612-file static gates, 2,253/one-
  skipped architecture/live tests, strict docs, current-date strict governance,
  and whitespace green. Record-state installed smokes and both byte-identical
  release rehearsals pass with the final distribution identities above.

### Explicit non-scope

- No distinct-principal, separate-logon, separate-session, hostile connection-
  race, independent-host, credential-custody, fixture-mutation, interruption,
  collection, or cleanup evidence.
- Criteria 6 and 7 remain unresolved. Windows remains unadmitted, and cleanup
  remains unimplemented and unauthorized.
- No runtime API, CLI/MCP command, package payload, dependency, workflow,
  permission, secret, hosted job, tag, release, or package publication.

### Publication boundary

- Initial DCO commit `0b32bb265811b50b91bc1e0862ad5ca50e2828b5`, tree
  `5ae8220f769e2417f74f9083fa991f49e490d786`, has sole parent exact M212,
  exactly 16 intended paths, one matching sign-off, consistent maintainer
  identity, clean revision/worktree/connectivity, and expected `0 114`
  local-main divergence. This factual record is incorporated by one closeout
  amendment.
- A fresh pruned fetch and direct remote-head query leave public `origin/main`
  at exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; M212 is absent, M99 is
  present, and only remote `main` exists. Hosted divergence is `0 114`.
  GitHub authentication is valid, the repository is public and unarchived with
  `main` as default, and PR #251 remains the latest merged PR. Publishing M213
  would expose the absent M100-M212 stack, so no push, PR, hosted allocation,
  tag, release, or package publication occurs.
- Automatic publication remains authorized only when a later fresh gate proves
  the complete prerequisite stack reachable from hosted `main`.

## M212 Windows local control-channel probe

- **Task:** Exercise one fixed, test-only Windows named-pipe coordination
  primitive after M211 containment without implementing a collector, issuing
  cleanup authority, or admitting Windows cleanup.
- **Status:** Fully locally validated and DCO-committed; project-record
  closeout, guarded scratch cleanup, and publication-safety review are
  complete. Publication is withheld because hosted `main` lacks the M100-M211
  prerequisite stack and authentication is unavailable.
- **Base:** fully locally validated M211 DCO commit
  `ff78fb674f3c5b18437e1164557e139933d0d424`, tree
  `4ca126e17fa65609bbe5cad1975fa206262e9e7d`, with sole parent exact M210.
- **Branch:** `release/m212-windows-local-control-channel-probe`; exact
  containment made the local M211 branch name redundant, so only local `main`
  and active M212 remain.

### M212 acceptance boundary

- Create one randomized, one-instance, local-only duplex named pipe under an
  explicit protected DACL containing exactly one current-logon-SID allow ACE;
  read the native DACL back and prove second-server refusal.
- Create the fixed participant suspended with inheritance disabled, assign its
  retained process handle to a no-breakaway kill-on-close Job Object before
  resume, and require exact one-process membership.
- Bind the connected native pipe-client process identifier to both the
  `CreateProcessW` result and retained process handle before sending a fresh
  challenge.
- Accept only the bounded canonical sequence challenge 0, ready 1, release 2,
  released 3; prove replay, wrong-challenge, malformed-shape, and disconnect
  refusal with bounded overlapped controller I/O and settled native handles.
- Keep the result Windows-only, same-host, same-logon, offline, test-only, and
  outside product runtime, package payload, collection/cleanup authority,
  admission, credentials, filesystem mutation, and CI allocation.

### Validation evidence so far

- Exact M211 history, branch containment, and the 14-test M211 handoff were
  confirmed. Static and current-date strict governance checks pass with zero
  findings. The intentional M212 red failed only because the selected probe
  artifacts were absent.
- Current Microsoft named-pipe security, logon-SID, client-process identity,
  security-descriptor, and overlapped-I/O guidance supports this smallest
  same-logon coordination probe while retaining the public-runner exclusion.
- Development corrected native generic-rights mapping to the exact observed
  `0x0012019f` pipe mask and then added live first-instance refusal plus
  cancellation settlement. The final focused architecture/live group passes
  all 17 tests.
- All 610 Python files are format-clean; Ruff and strict Pyright report zero
  findings. Complete architecture passes 2,228 tests with one supported-
  capability skip; strict docs and whitespace pass.
- Complete isolated all-group graphics suites pass identical totals of 4,328
  tests with 19 skips on CPython 3.12.13, 3.13.13, and 3.14.5.
- Ten real-wgpu tests, fresh two-/three-workload base and graphics profiles,
  all eight profile-schema tests, Null/wgpu Clockwork Arena, and Agent World
  Builder pass with their established deterministic identities.
- Two initial distributions are byte-identical: the 364,404-byte pure wheel is
  SHA-256 `a157884268ed30ec9a7a275d2ea9e40d865e8fd5de0c5b56bdceeab70eb98d13`
  and the 2,516,609-byte source archive is SHA-256
  `37bce1a2c7718cb7255204778e82fc3e8f68126e442d443a322c1f63c5f407e6`.
  Installed-wheel and scene smokes pass; two ten-artifact release rehearsals
  pass with zero difference. The wheel has 114 entries and none of the five
  M212 implementation/decision files; each occurs once in the 1,014-entry
  source archive.
- The record-inclusive separator keeps all 610-file static gates clean,
  complete architecture at 2,228 passes/one skip, strict docs, both governance
  modes, and whitespace passing. Two record-state builds reproduce a
  364,390-byte pure wheel at SHA-256
  `0d671cea6ee9f0def17268c126411f7661a853bfbb3f5f6257f60371082370e6`
  and 2,519,609-byte source archive at SHA-256
  `d0dabb8fb4db883338a70cbac8cfe7ea169758417820db0c64e914de42d5f2cb`;
  installed smokes and both byte-identical release rehearsals pass. Recording
  this evidence necessarily changes only the source archive afterward.
- Findings-first review corrected one diagnostic edge so a failed native wait
  retains its Windows error category after safe cancellation instead of being
  mislabeled as a timeout. Focused formatting, Ruff, strict Pyright, whitespace,
  and all 17 M212 tests pass after the correction.
- Complete corrected-tree suites again pass 4,328 tests with 19 skips on
  CPython 3.12.13, 3.13.13, and 3.14.5. These replace the earlier candidate
  matrix as final supported-version behavioral evidence.
- Final corrected-record builds reproduce the unchanged 364,390-byte wheel at
  SHA-256
  `0d671cea6ee9f0def17268c126411f7661a853bfbb3f5f6257f60371082370e6`
  and identical 2,520,789-byte source archives at SHA-256
  `3d85c259b30c2742cf6fbb5f4f912397cc09c63cb9c2d4709579c67aa9bb8e9e`.
  Installed smokes and two ten-artifact release stages pass with zero byte
  difference; recording this row changes only the source archive afterward.
- Findings-first scope/security review confirms the exact 17-path allowlist,
  zero protected runtime/package/example/script/benchmark/workflow/metadata/
  dependency/lock diff, absent retired root control metadata, and zero added
  development-tool identity, credential, machine-path, debug-marker, backend,
  network, arbitrary-evaluation, shell, breakaway, privilege, or account-launch
  match. Git whitespace and object connectivity are clean; no actionable
  correctness, authority, security, architecture, compatibility,
  documentation, package-boundary, or CI-allocation finding remains.
- Scratch cleanup stopped without mutation on its first access-denied audit.
  The access-enabled audit proved 35 targets repository-confined, ignored,
  untracked, and recursively reparse-free; immediate revalidation removed
  exactly those 35. Three final supported-version pytest roots remain ignored
  and untracked because their isolated sandbox identity denies traversal. A
  top-level inherited-access reset failed, and no ownership/ACL bypass was
  attempted. Their cleanup requires separate explicit authority.
- Post-cleanup, all 610-file static gates remain clean; all 17 M212 tests,
  strict docs, both governance modes, and whitespace pass. The test root was
  absent after pytest settlement and the sole regenerated docs target was
  independently audited and removed; only the same three inaccessible ignored
  roots remain.
- Pre-commit audit confirms exact M211 HEAD/tree/parent, the exact 17-path
  allowlist, zero protected diff, only local `main` plus neutral M212,
  configured maintainer identity, expected `0 112` local-main divergence,
  three disclosed ignored/untracked inaccessible roots, zero sensitive added-
  content match, clean whitespace, and clean Git object connectivity.

### Explicit non-scope

- No distinct-principal or independent-host evidence, hostile same-logon
  exclusion, privileged collector, production fixture, credential lifecycle,
  VM/physical power action, qualifying collection, filesystem cleanup,
  runtime/package API, dependency, workflow, hosted allocation, tag, release,
  or package publication.
- Criteria 6 and 7 remain unresolved. Windows remains unadmitted, and cleanup
  remains unimplemented and unauthorized.

### Publication boundary

- Initial DCO commit `5ee787e277553d73e58672364708abc7c33be0a1`,
  tree `c312d44c3861383a5f004d0a9d7e1e7bda633c1f`, has sole parent exact
  M211, exactly 17 intended paths, one matching sign-off, consistent
  author/committer identity, clean revision whitespace, expected `0 113`
  divergence, clean worktree and Git connectivity, and the three disclosed
  ignored/untracked residual roots. This factual record is incorporated by one
  closeout amendment.
- Closeout commit `e1e8d5b6b9d1f1ff3812d13240b572080d6b6383`,
  tree `f613a700b96c35c968995ea4c154a2939275cea8`, retains exact M211 as sole
  parent, exact 17-path scope, one matching sign-off, consistent identity,
  clean worktree/revision/connectivity, expected `0 113` divergence, and the
  three disclosed ignored/untracked residual roots. This hosted-safety record
  is incorporated by one final evidence-only amendment.
- A fresh pruned fetch leaves public `origin/main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; M211 is absent, M99 is
  present, and only remote `main` exists. Hosted divergence is `0 113` and the
  configured GitHub authentication is invalid. Publishing M212 would expose
  absent M100-M211 prerequisites, so no push, PR, hosted allocation, tag,
  release, or package publication occurs.
- Automatic publication remains authorized only if a fresh hosted ancestry
  gate proves the complete prerequisite stack is already reachable from
  hosted `main`. Otherwise the validated DCO commit remains local.

## M211 Windows independent-host process-containment probe

- **Task:** Exercise one test-only, offline Windows suspended-launch and Job
  Object containment sequence for M209's future fixed participant tree without
  implementing a privileged collector or admitting Windows cleanup.
- **Status:** Fully locally validated and DCO-committed; publication is withheld
  because hosted `main` lacks the M100-M210 prerequisite stack.
- **Base:** fully locally validated M210 DCO commit
  `2aa04dd2c6c259e2d8c5295f7ac1ca65df04f6b4`, tree
  `73983d6e0c17f4ccd5605e59f220058007fe5fae`, with sole parent exact M209.
- **Branch:**
  `release/m211-windows-independent-host-process-containment-probe`; exact
  containment made the local M210 branch name redundant, so only local `main`
  and active M211 remain.

### M211 acceptance boundary

- Create one unnamed Job Object with kill-on-last-close and no breakaway;
  create the fixed root suspended, assign its retained handle before any
  fixture instruction, then resume and close the retained thread handle.
- Admit exactly one private inherited output handle, accept only two bounded
  canonical readiness records, retain and verify root and descendant process
  handles, and require exact two-process Job membership.
- Prove both fixed Job-scoped termination with settled accounting and
  last-handle-close fail-safe settlement under bounded native waits.
- Treat access-denied nested Job assignment as an explicit unsupported-host
  skip; add no PID-only, unsuspended, shell, breakaway, or widened-membership
  fallback.
- Keep the probe Windows-only, test-only, offline, fixed-purpose, and outside
  the product runtime, CLI, package payload, cleanup authority, collection
  authority, admission decision, and CI allocation.

### Development evidence so far

- Exact M210 history and clean containment were confirmed. The focused M210
  handoff passed 29 tests with one supported-symlink skip; both governance
  modes passed with zero findings.
- Current Microsoft and GitHub primary guidance supports suspended creation,
  retained process/thread identity, inherited no-breakaway Job containment,
  kill-on-last-close, bounded process waits, and exclusion of public
  self-hosted collection. The current controller is already Job-contained, so
  incompatible nested assignment remains an explicit skip rather than a
  weaker fallback.
- Neutral M211 starts from exact M210. The redundant local M210 branch name was
  removed while its commit remains the exact parent. The intentional red
  failed its single selected check only because the five probe/RFC/security
  artifacts and public registrations were absent.
- The final focused architecture and live integration group passes 14 tests.
  Development corrected native integer-handle normalization, text-mode CRLF,
  virtual-environment launcher identity, and unexpected console-host
  membership; the final direct `pythonw.exe` tree contains exactly the retained
  root and descendant.
- Initial whole-tree gates are clean across 607 Python files. Ruff and strict
  Pyright report zero findings; the architecture suite passes 2,216 tests with
  one supported-symlink skip; strict docs and whitespace pass.
- Complete isolated all-group graphics suites pass identical totals of 4,311
  tests with 19 skips on CPython 3.12.13, 3.13.13, and 3.14.5.
- Ten real-wgpu tests, fresh two-/three-workload base and graphics profiles,
  all eight profile-schema tests, Null/wgpu Clockwork Arena, and Agent World
  Builder pass and reproduce their established deterministic identities.
- Two distributions are byte-identical. Installed-wheel and scene smokes pass;
  two complete ten-artifact release stages pass with zero difference. The
  114-entry wheel contains no M211 material; all five M211 implementation and
  decision files are source-only in the 1,009-entry source archive.
- The record-inclusive separator leaves the unchanged lock and 45-package
  graphics environment clean, all 607-file static gates clean, 2,216
  architecture tests with one skip, strict docs, both governance modes, and
  whitespace passing.
- Record-state builds reproduce the unchanged 364,279-byte wheel and identical
  2,500,060-byte source archives. Installed smokes and two complete
  ten-artifact release stages pass with zero byte difference; inventory remains
  114 wheel/1,009 source entries with the five M211 files source-only.
- Findings-first review leaves exactly 17 intended paths, zero protected
  runtime/package/example/script/benchmark/workflow/metadata/dependency/lock
  diff, and zero added development-tool identity, credential, machine-path,
  debug-marker, or retired-control-path match. No actionable correctness,
  containment, architecture, security, compatibility, documentation, package,
  or CI-allocation finding remains.
- The first recursive scratch audit was access-denied inside pytest-owned
  directories and made no deletion decision. Its exact access-enabled rerun
  proved all 25 M211 scratch targets repository-confined, ignored, untracked,
  and reparse-free. Guarded removal revalidated the unchanged set immediately
  before removing it and left zero M211 scratch target.
- The post-cleanup separator leaves all 607-file static gates clean, the exact
  metadata/M210/M211 group at 48 passes with one supported-symlink skip, strict
  docs, both governance modes, and whitespace passing. Its two regenerated
  scratch directories were independently revalidated and removed; zero M211
  scratch remains.
- The pre-commit audit proves exact M210 HEAD/tree/parent, the exact 17-path
  allowlist, zero protected diff, only local `main` plus neutral M211,
  configured maintainer identity, expected `0 111` local-main divergence,
  zero sensitive added-line or scratch match, clean whitespace, and clean Git
  object connectivity.

### Explicit non-scope

- No privileged or independent-host collector, production fixture, external
  host action, cross-principal execution, VM or physical power action,
  credential lifecycle, evidence admission, filesystem cleanup, runtime or
  package API, command, dependency, workflow, hosted allocation, tag, release,
  or package publication.
- Criteria 6 and 7 remain unresolved. Windows remains unadmitted, and cleanup
  remains unimplemented and unauthorized.

### Publication boundary

- Initial DCO commit `798f397675a441c05af746f05cb561714c2e3f34`,
  tree `ffd1520e6e4f889c9897ae322a0b08871d45bd23`, has sole parent exact
  M210, exactly 17 intended paths, one matching sign-off, clean revision
  whitespace, expected `0 112` local-main divergence, clean worktree, zero
  scratch, and clean Git connectivity. This factual record is incorporated by
  one closeout amendment.
- Closeout commit `ef5fe47191dabc95bd9ffca94a5f071e8832eebc`,
  tree `b516b68e46799cdf5bf6e64eb6567d462527e6f1`, retains exact M210 as
  sole parent, one matching sign-off, exact 17-path scope, clean worktree,
  zero scratch, clean revision whitespace, expected `0 112` local-main
  divergence, and clean object connectivity. This hosted-safety record is
  incorporated by one final evidence-only amendment.
- A fresh pruned fetch and direct hosted-head query leave public `main` at exact
  M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; M210 is absent, M99 is
  present, only remote `main` exists, and hosted divergence is `0 112`.
  Authentication is valid; the repository is public, unarchived, defaults to
  `main`, and PR #251 remains latest and merged.
- Publishing M211 would expose absent M100-M210 prerequisites. No push, PR,
  hosted allocation, tag, release, or package publication occurs. Automatic
  publication remains authorized only after hosted `main` gains the complete
  prerequisite ancestry and a fresh safety gate passes.

## M210 Windows independent-host collection-plan validator

- **Task:** Add one offline, read-only source validator and reviewed incomplete
  fixture for a sanitized structural companion to M209's future private run
  manifest, without implementing a privileged harness or admitting Windows
  cleanup.
- **Status:** Fully locally validated and DCO-committed; publication is withheld
  because hosted `main` lacks the M100-M209 prerequisite stack.
- **Base:** fully locally validated M209 DCO commit
  `03f3848a3bf52945ab4d1b0af4065219568a5b1a`, tree
  `f82a3b12edfe5a3765580837327d4373671373d6`, sole parent exact M208.
- **Branch:**
  `release/m210-windows-independent-host-collection-plan-validator`; exact
  containment made the local M209 branch name redundant, so only local `main`
  and active M210 remain.

### M210 acceptance boundary

- Read one stable regular non-symlink plan bounded to 1,048,576 bytes and one
  exact canonical JSON line; emit only stable path-free validation results.
- Require the exact M207 profile, barrier, and interruption matrices, M209's
  closed eight-operation sequence, bounded sanitized host classifications,
  typed identity syntax, exact requirement declarations, and derived totals.
- Derive structural `plan_complete`; keep collection status `not_run` and
  authority, criteria 6 and 7, and Windows admission false in every accepted
  document.
- Treat a complete plan as neither the private manifest nor authentication,
  executable authority, provenance, qualifying evidence, or admission.
- Keep stable machine/storage/process/principal/session/operator identities,
  paths, credentials, native handles, and controller objects outside the
  schema and engine API.
- Add no runtime/package API, CLI command, privileged harness, native call,
  process or power control, account or credential lifecycle, filesystem
  mutation, network access, cleanup authority, dependency, version, workflow,
  permission, secret, qualifying run, or hosted allocation.

### Development evidence so far

- Exact M209 history and clean containment were confirmed. The focused M209
  handoff passed 12 tests.
- Static and current-date strict external governance checks passed with zero
  findings. One sandboxed strict attempt was denied existing-cache access
  before checking; the access-enabled exact rerun passed.
- Current Microsoft, GitHub, and NIST primary guidance supports retained
  process identity, Job Object process-tree containment, external power
  separation, separately retained evidence digests, and exclusion of public
  self-hosted collection. DirectionBriefV1 recommended this source-only
  prerequisite rather than a privileged collector.
- Neutral M210 starts from exact M209. The redundant local M209 branch name was
  removed while its commit remains the exact parent.
- The intentional red failed its one selected check only because the four M210
  validator, fixture, RFC, and security artifacts were absent.
- The first combined core run passed 19 tests with one supported-symlink skip
  and failed only the still-absent RFC/security check. Two exact wording issues
  and then one Markdown-format wording issue were corrected. The final focused
  integration/architecture group passes 29 tests with one supported-symlink
  skip.
- Initial whole-tree static gates are clean across 604 Python files after Ruff
  mechanically formatted two new files. Ruff and strict Pyright report zero
  findings; the complete architecture suite passes 2,204 tests with one
  supported-symlink skip; strict docs and whitespace pass.
- Complete isolated all-group graphics suites pass identical totals of 4,297
  tests with 19 skips on CPython 3.12.13, 3.13.13, and 3.14.5. The 3.13 run's
  isolated interpreter was directly verified after uv warned that the project
  default remained 3.12.
- Ten real-wgpu tests, fresh two-/three-workload base and graphics profiles,
  all eight profile-schema tests, Null/wgpu Clockwork Arena, and Agent World
  Builder pass and reproduce their established identities.
- Two pre-record distributions are byte-identical. Installed-wheel and scene
  smokes pass; two complete ten-artifact release stages pass with zero
  difference. The 114-entry wheel contains no M210 payload; all six M210
  implementation files are source-only in the 1,004-entry source archive.
- Findings-first review added the M207-compatible `other_supported` Windows
  release class and corrected the noncanonical regression to exercise actual
  formatting drift. Exactly 18 intended paths remain, protected runtime/
  package/workflow/dependency/lock surfaces have zero diff, and the added-line
  credential, machine-path, and tooling-identity scan has zero match.
- The record-inclusive separator rechecks the unchanged lock and graphics
  environment, all 604-file static gates, 2,204 architecture tests with one
  skip, strict docs, both governance modes, and whitespace successfully.
- Record-state builds reproduce the unchanged 364,159-byte wheel and a
  2,482,598-byte source archive. Installed-wheel and scene smokes pass; two
  complete ten-artifact release stages are byte-identical. Inventory remains
  114 wheel/1,004 source entries with all six M210 files source-only.
- The first recursive scratch audit was access-denied inside pytest-owned
  directories and therefore did not authorize deletion. Its exact access-
  enabled rerun proved all 31 M210 scratch targets repository-confined,
  ignored, untracked, and reparse-free. Guarded removal revalidated the same
  set and left zero M210 scratch target.
- The post-cleanup separator leaves all 604 Python files format-clean, Ruff and
  strict Pyright clean, the exact metadata/M209/M210 group at 27 passes, both
  governance modes at zero findings, whitespace clean, and M210 scratch zero.
- The pre-commit audit proves exact M209 HEAD/tree/parent, the exact 18-path
  allowlist, zero protected diff, only local `main` plus neutral M210,
  configured maintainer identity, expected `0 110` local-main divergence,
  zero sensitive added-line or scratch match, clean whitespace, and clean Git
  object connectivity.

### Explicit non-scope

- No privileged harness, independent-host execution, real host or credential
  provisioning, native process/power/filesystem implementation, qualifying
  M206 or M208 artifact, criterion 6 or 7 resolution, Windows admission,
  cleanup, production cache access, runtime/package change, dependency,
  workflow, CI allocation, release, or publication.

### Publication boundary

- Initial DCO commit `ee20a6e73e6c6cd6bb833368b7f597634a7d4848`,
  tree `fb01371982666a8683148a2715b4365ee0acc6c1`, has sole parent exact
  M209, exactly 18 intended paths, one matching sign-off, clean revision
  whitespace, expected `0 111` local-main divergence, and a clean worktree.
  This factual record is incorporated by one closeout amendment.
- A fresh pruned fetch and direct hosted-head query leave public `main` at exact
  M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; M209 is absent, M99 is
  present, only remote `main` exists, and hosted divergence is `0 111`.
  Authentication is valid; the renamed repository is public, unarchived,
  defaults to `main`, and PR #251 remains latest and merged.
- Publishing M210 would expose absent M100-M209 prerequisites. No push, PR,
  hosted allocation, tag, release, or package publication occurs. Automatic
  publication remains authorized only after hosted `main` gains the complete
  prerequisite ancestry and a fresh safety gate passes.

## M209 Windows independent-host collection-authority policy

- **Task:** Define the least-authority, offline, operator-controlled boundary
  for a future M207/M208 evidence collector without implementing or running the
  privileged harness or admitting Windows cleanup.
- **Status:** Policy, RFC, architecture guard, and registrations are fully
  locally validated; record, commit, and publication-safety closeout are in
  progress.
- **Base:** fully locally validated M208 DCO commit
  `b30892e35b6dfcb2f0c11a209f04260228738db6`, tree
  `5478be6d27e81f54f1b6ebae0a616249ee930892`, sole parent exact M207.
- **Branch:**
  `release/m209-windows-independent-host-collection-authority-policy`; exact
  containment made the local M208 branch name redundant, so only local `main`
  and active M209 remain.

### M209 acceptance boundary

- Bind a future private non-serializable single-run, single-use collection
  action to one host, fixture, lane, trial, barrier, interruption, exact input
  identities, and closed operation.
- Keep collection authority separate from M201 cleanup authority, product
  commands, canonical world state, production cache access, and Windows
  admission.
- Require an offline disposable-host environment with networking, clipboard,
  writable live shares, public self-hosted runners, repository credentials,
  and participant self-attestation excluded.
- Keep process termination bound to exact fixture participants; require VM
  power cut against current storage without guest shutdown or checkpoint
  restore; keep physical-host power loss operator-only.
- Require a private pre-run manifest, chronological custody, atomic same-volume
  staging, separately retained digest, post-settlement sanitization, authority
  expiry, and fail-closed teardown before M208 validation.
- Add no privileged harness, qualifying run, runtime/package API, command,
  native call, process or power control, credential lifecycle, filesystem
  mutation, dependency, version, workflow, permission, secret, or hosted
  allocation.

### Development evidence so far

- Exact M208 history and the DCO-signed M201 ancestry were confirmed. The
  worktree was clean, retired root control metadata remained absent, and the
  focused M208 handoff passed 45 tests with one supported-symlink skip.
- Both required external governance modes passed after the sandboxed first
  launch was rerun with read-only access to the existing uv cache.
- Current GitHub, Microsoft, and NIST primary guidance supports offline custody,
  no public self-hosted runner, deny-by-default Sandbox channels, real VM turn-
  off without checkpoint restoration, and separately retained evidence
  digests. The resulting DirectionBriefV1 recommended this policy-only slice.
- Neutral M209 starts from exact M208. The redundant local M208 branch name was
  removed while its commit remains the exact parent.
- The intentional red failed one selected check only because the M209 policy
  and RFC were absent. The first complete guard run then exposed seven exact-
  wording mismatches and the second exposed two; the policy language was made
  explicit. The final focused guard passes all 12 tests, strict docs builds,
  and whitespace is clean.
- The initial whole-tree separator passes the unchanged lock and graphics sync,
  all 601-file static gates, 2,194 architecture tests with one supported-
  symlink skip, strict docs, and whitespace.
- Complete isolated suites pass 4,268 tests with 18 skips on each of CPython
  3.12.13, 3.13.13, and 3.14.5. All ten real-wgpu tests and eight profile-
  schema tests pass; fresh base and graphics profiles contain two and three
  workloads.
- Null and wgpu Clockwork Arena reproduce the established state, 600 draws,
  and 2,213 sprites; wgpu reproduces its capture. Agent World Builder
  reproduces established state, capture, replay, query, and batch results.
- Two pre-record distributions are byte-identical, installed-wheel smoke
  passes, and two complete ten-artifact release stages pass with zero
  difference. The 114-entry wheel contains no M209 or project-control payload;
  all three M209 implementation files are source-only.
- Findings-first review confirms exactly 15 intended paths, zero protected
  runtime/package/workflow/dependency/lock difference, zero added credential,
  machine-local path, or retired tooling identity, and no unresolved security,
  authority, correctness, compatibility, package, documentation, or CI-
  allocation finding at this stage.
- The first record-inclusive architecture run caught one literal disclosure of
  retired metadata names in the evidence record. Neutral wording replaced it;
  the corrected complete separator passes all 601-file static gates, 2,194
  architecture tests with one skip, strict docs, both governance modes, and
  whitespace.
- Record-state builds reproduce the unchanged 364,078-byte wheel and a
  2,468,345-byte source archive. Installed-wheel smoke and two complete,
  byte-identical ten-artifact release stages pass; inventory remains 114 wheel
  and 998 source entries with exactly the three M209 implementation files
  source-only.
- The final record-inclusive static, metadata-hygiene/M209, strict-docs,
  governance, and whitespace separator passes. All 26 M209 scratch targets were
  proven repository-confined, ignored, untracked, and reparse-free immediately
  before guarded removal; the postcondition found zero remaining target.
- The corrected pre-commit audit proves exact M208 HEAD/tree/parent, exactly 15
  intended paths, zero protected diff, only local `main` plus neutral M209,
  configured maintainer identity, expected `0 109` local-main divergence, zero
  M209 scratch, clean whitespace, and clean Git object connectivity.

### Explicit non-scope

- No privileged harness, independent-host execution, account or credential
  handling, native process/power/filesystem implementation, qualifying M206 or
  M208 artifact, criterion 6 or 7 resolution, Windows admission, cleanup,
  production cache access, runtime/package change, dependency, workflow, CI
  allocation, release, or publication.

### Commit and publication result

- Initial DCO commit `185df0d4cf599e4bceb26da5bd4312d25474a5f2`,
  tree `99255ff861cb7f0d9743bbc2d5bc72aab11b8fed`, has sole parent exact
  M208, exactly 15 intended paths, matching author/committer/sign-off identity,
  clean revision whitespace, expected `0 110` local-main divergence, clean
  worktree, zero scratch, and clean object connectivity. This factual record is
  incorporated by one closeout amendment.
- A fresh pruned fetch and direct remote-head query leave hosted `main` at exact
  M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; M208 is absent, M99 is
  present, only remote `main` exists, and hosted divergence is `0 110`.
  Authentication is valid; the repository is public, unarchived, defaults to
  `main`, and PR #251 remains the latest merged PR.
- Publishing M209 would expose absent M100-M208 prerequisites. No push, PR,
  hosted allocation, tag, release, or package publication occurs.

### Publication boundary

- Publication remains authorized only after hosted `main` gains the complete
  prerequisite ancestry and a fresh safety gate passes.

## M208 Windows independent-host evidence validator

- **Task:** Add one offline, read-only validator and reviewed incomplete
  fixture for the M207 evidence envelope, bound to a separately validated M206
  companion, without running a privileged fixture or admitting Windows cleanup.
- **Status:** Fully locally validated; pre-commit and publication-safety
  closeout in progress.
- **Base:** fully locally validated M207 DCO commit
  `1b3af35a6b4c2382199e0cdad540b258e0008866`, tree
  `8e1d5cb86b70e7e4da42f69d044940543fda9c7f`, sole parent exact M206.
- **Branch:** `release/m208-windows-independent-host-evidence-validator`;
  exact containment made the local M207 branch name redundant, so only local
  `main` and active M208 remain.

### M208 acceptance boundary

- Accept exactly one stable bounded canonical independent-host artifact and
  one separate M206 cross-principal artifact.
- Validate the M206 companion independently, recompute its digest, and derive
  criterion 6; never trust a copied criterion claim or unverified binding.
- Validate at most 32 host records, 128 profile/host results, 4,096 trials,
  65,536 observations, all eight M207 profile lanes, and all three
  interruption classes through exact classifications, statuses, totals, and
  sanitized outcomes.
- Require at least two passed independent hosts per passed profile, complete
  physical-persistence interruption evidence for local fixed NTFS, actual
  engine refusal for refusal lanes, and observed identity reuse plus stale-
  authorization rejection for the ABA lane.
- Keep the reviewed fixture all `not_run`, criterion 7 false, and Windows
  admission false. A complete synthetic validation proves claim relationships
  only and is not execution evidence.
- Preserve runtime, package, workflow, dependency, version, native, process,
  account, credential, network, filesystem-mutation, and hosted-allocation
  boundaries.

### Development evidence so far

- Exact M207 history, clean worktree, two-branch inventory, absent retired
  control metadata, current test state, and both external governance modes
  were audited before branching.
- Current RFC 8259/RFC 8785, Python stable-file primitives, and Microsoft
  host-scoped file-identity guidance were reviewed. They support strict
  canonical/schema validation, M206 companion binding, and sanitized scoped
  identities without a new format or authority.
- Neutral M208 starts from exact M207. The redundant local M207 branch name was
  removed while its commit remains the exact parent.
- The intentional red failed only because the M208 validator and fixture were
  absent. The source-only validator, canonical all-`not_run` fixture,
  integration coverage, architecture guard, RFC-0191, security guide, and
  eight public registrations are now implemented.
- Focused Ruff and strict Pyright pass. The corrected M208 integration and
  architecture group passes 45 tests with one environment-dependent symlink
  skip on each supported interpreter, including a synthetic complete pair,
  invalid companion and digest substitution, exact classification/claim
  mutations, canonical and oversized input, path-free errors, protected
  surfaces, and no-authority checks.
- Complete post-review suites pass 4,254 tests with 17 skips on CPython 3.12.13
  plus graphics and 4,244 tests with 18 skips on CPython 3.13.13 and 3.14.5.
  Ten real-wgpu tests, fresh profiles, Clockwork Arena, and Agent World Builder
  reproduce their established identities.
- Findings-first review tightened the ABA lane to the admitted local fixed
  NTFS stable 128-bit host/volume-scoped capability profile. Oversized-file,
  host-count, symlink, and ABA-scope regressions now cover the corrected
  boundary. No runtime, workflow, dependency, or hosted allocation changed.
- The record-inclusive 45-package graphics environment, all 600-file static
  gates, 181 architecture/evidence tests with one supported-symlink skip,
  strict docs, both governance modes, and whitespace pass.
- Two record-state distributions reproduce a 363,972-byte pure wheel and a
  2,454,719-byte source archive. Installed wheel/scene and two complete ten-
  artifact release stages pass; both stages are byte-identical. Inventory is
  114 wheel and 995 source entries with all six M208 implementation artifacts
  source-only and zero forbidden wheel or retired-control entry.
- The corrected scope audit confirms exactly 18 intended paths, zero protected
  runtime/workflow/metadata/lock difference, no service identity, credential
  assignment, machine-local path, or retired root metadata, and clean
  whitespace.
- A read-only audit proved all 41 M208 scratch targets repository-confined,
  ignored, untracked, and recursively reparse-free. Exact guarded removal
  revalidated the unchanged target set; a separate postcondition confirms zero
  M208 scratch remains.
- The final post-cleanup separator keeps all 600 Python files format-clean;
  Ruff and strict Pyright pass; 181 architecture/evidence tests pass with one
  supported-symlink skip; strict docs, both governance modes, and whitespace
  pass. Its two regenerated scratch directories were independently revalidated
  and removed; zero M208 scratch remains.
- The corrected pre-commit audit confirms exact M207 HEAD/tree/parent, the
  18-path allowlist, zero protected diff, only local `main` plus neutral M208,
  configured maintainer identity, expected `0 108` local-main divergence,
  absent retired root metadata, zero scratch, clean whitespace, and clean Git
  object connectivity.

### Commit and publication result

- Initial DCO commit `ac95e0aaf67188a19ff759811600b8a85a58bf35`, tree
  `9cef3daa1562fc1b65f2e95de3c9fa90772d7909`, has exact M207 as its sole
  parent, exactly 18 intended paths, one matching sign-off, consistent
  maintainer identity, clean revision whitespace, expected `0 109` local-main
  divergence, a clean worktree, zero scratch, and clean Git connectivity. This
  factual record is incorporated by one closeout amendment.
- A fresh pruned fetch and direct hosted-head query leave public `main` at exact
  M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`. M207 is absent, M99 is
  present, only remote `main` exists, and hosted divergence is `0 109`.
  GitHub authentication is valid; the repository is public, unarchived,
  defaults to `main`, and PR #251 remains the latest merged PR.
- Publishing M208 would expose absent M100-M207 prerequisites. No push, PR,
  hosted allocation, tag, release, or package publication occurs.

### Publication boundary

- Publication remains authorized only after hosted `main` gains the complete
  prerequisite ancestry and a fresh safety gate passes.

### Explicit non-scope

- No qualifying Windows run, independent-host collection, physical power-loss
  execution, criterion 6 or 7 resolution, Windows admission, privileged
  harness, coordinator, process launch, native API, cleanup implementation,
  account or credential management, network access, dependency, version,
  workflow, permission, hosted allocation, release, or publication.

## M207 Windows independent-host validation contract

- **Task:** Define the exact independent-host, capability-profile,
  safe-refusal, interruption, recovery, and sanitized-evidence contract
  required by M199 Windows cleanup admission criterion 7.
- **Status:** Locally complete; publication withheld by hosted ancestry.
- **Base:** fully locally validated M206 DCO commit
  `5ae957ffcfb1523e980ce6ff95841f685e05ea27`, tree
  `52b47c015b184390618b7ea387b430135894b326`, sole parent exact M205.
- **Branch:** `release/m207-windows-independent-host-validation-contract`;
  exact containment made the local M206 branch name redundant, so only local
  `main` and active M207 remain.

### M207 acceptance boundary

- Require at least two independently provisioned Windows hosts for every
  admitted profile, with distinct operating-system, boot, and storage
  instances; processes, sessions, containers, reboots, and same-snapshot
  clones are not substitutes.
- Observe filesystem family/version, local/remote state, exact volume
  capabilities, same-volume relationships, file-ID scope, and persistence
  class rather than inferring them from paths or platform labels.
- Require the complete local-NTFS positive lane and observed fail-closed lanes
  for ReFS, SMB, CsvFS, cross-volume, unknown/missing capabilities, and file-ID
  reuse/ABA pressure.
- Separate forced-process termination, VM power cut, and physical-host power
  loss; require restart reconciliation and forbid stronger durability claims
  from graceful close, VM-only interruption, or one successful flush call.
- Reserve one bounded canonical sanitized evidence envelope without adding a
  harness or validator. Unsupported, not-run, failed, incomplete, or shared-
  ancestry evidence keeps criterion 7 unresolved.
- Keep collection offline on operator-controlled disposable fixtures. Add no
  public self-hosted runner, credential, account lifecycle, network access,
  hosted allocation, or workflow change.
- Preserve exact M206, runtime, examples, scripts, dependencies, metadata,
  version, package, and vital-CI boundaries. Windows remains unadmitted and
  cleanup remains unimplemented and unauthorized.

### Development evidence so far

- Exact M206 commit/tree/parent, clean worktree, two-branch inventory, and
  retained maintainer identity were audited before work.
- Static and current-date strict external governance checks pass with zero
  findings. A corrected `python -m pytest` focused baseline passes all 59
  M205/M206/evidence tests; the direct pytest entry point first exposed a local
  namespace-path ambiguity without repository change.
- Current Microsoft filesystem capability, file-identity, cross-volume move,
  flush, NTFS/ReFS, and GitHub runner guidance was reviewed before branching.
  It supports observed capability profiles, explicit copy/delete refusal,
  separated durability claims, and offline operator-controlled collection.
- Neutral M207 starts from exact M206. The redundant local M206 branch name was
  removed while its commit remains the exact parent.
- The intentional architecture-red run passed both preservation/no-runtime
  checks and failed only nine absent decision/RFC/registration checks.
- RFC-0190, the security contract, one architecture guard, and eight public
  registrations are implemented. One Markdown code-span mismatch was
  normalized; the focused M205-M207/evidence group passes all 70 tests.
- The unchanged lock resolves 46 packages. All 597 Python files are format-
  clean; Ruff passes; strict Pyright passes after restoring the existing
  graphics extra removed by the base all-groups sync; the exact repository-
  hygiene/M199-M207 group passes 108 tests; strict docs, governance, and
  whitespace pass.
- Complete isolated suites pass 4,211 tests with 17 skips on CPython 3.12.13
  plus graphics and 4,201 tests with 18 skips on CPython 3.13.13 and 3.14.5.
- Ten real-wgpu tests, fresh one-repeat base/graphics profiles, all eight
  profile-schema tests, Clockwork Arena, and Agent World Builder reproduce
  their established identities.
- Two pre-review distributions are byte-identical; installed wheel and scene
  smokes pass; two byte-identical ten-artifact release stages pass complete
  smoke. Inventory is 114 wheel and 989 source entries with all three M207
  implementation artifacts source-only and zero forbidden wheel entry.
- Findings-first review found no authority, runtime, package, CI, secret,
  local-path, or repository-identity leak. It tightened the ABA lane so
  allocation pressure without actual file-ID reuse remains unsupported, and
  normalized one test name. The corrected focused group passes 70 tests.
- The record-inclusive 45-package graphics environment, all 597-file static
  gates, 108 architecture tests, strict docs, both governance modes, and
  whitespace pass.
- Two record-state builds reproduce a 363,886-byte pure wheel and a
  2,436,889-byte source archive. Installed wheel/scene and two complete
  ten-artifact release smokes pass; both stages are byte-identical. Inventory
  remains 114 wheel/989 source entries with all three M207 implementation
  artifacts source-only.
- A read-only audit proved all 23 M207 test, environment, profile,
  documentation, distribution, and release targets repository-confined,
  ignored, untracked, and recursively reparse-free. Exact guarded removal
  revalidated the unchanged set and removed all 23; zero remains.
- The final post-cleanup separator keeps all 597 Python files format-clean;
  Ruff and strict Pyright pass; 108 architecture tests, strict docs, both
  governance modes, and whitespace pass. Its sole regenerated documentation
  directory was independently audited and removed; zero M207 scratch remains.
- The pre-commit audit confirms exact M206 HEAD/tree/parent, exactly 15
  intended paths, zero protected diff, only local `main` plus neutral M207,
  configured maintainer identity, expected `0 107` local-main divergence,
  absent retired root metadata, zero hygiene findings, zero scratch, clean
  whitespace/static/architecture gates, and clean Git connectivity.

### Commit and publication result

- Initial DCO commit `e4b09b803ee4d64b46460f27ab62f18020da4abd`,
  tree `a697c0132d826da5caf4c476307ce37ecdc7ecea`, has exact M206 as its
  sole parent, exactly 15 intended paths, one matching sign-off, consistent
  maintainer identity, clean revision whitespace, expected `0 108`
  local-main divergence, a clean worktree, zero scratch, and clean Git
  connectivity. This hosted-safety record is incorporated by one closeout
  amendment.
- A fresh pruned fetch and direct hosted-head query leave public `main` at
  exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, with only remote
  `main`. M206 is absent, M99 is present, and hosted divergence is `0 108`.
- GitHub authentication is valid. A public read-only API check confirms the
  repository is public, unarchived, defaults to `main`, and PR #251 remains
  the latest closed merged PR.
- Publishing M207 would expose the absent M100-M206 prerequisite stack. No
  push, PR, hosted allocation, tag, release, or package publication occurs.

### Publication boundary

- Publication remains authorized only after hosted `main` gains the complete
  prerequisite ancestry. The current safety gate withholds it.
- Publication remains authorized only after complete validation and a fresh
  hosted-ancestry safety gate. No push, PR, tag, release, package publication,
  or hosted allocation has occurred for M207.

### Explicit non-scope

- No independent-host run, physical power-loss run, criterion 6 or 7
  resolution, Windows cleanup admission, privileged harness, offline
  validator, process launcher, filesystem adapter, native call, runtime
  cleanup, account or credential management, dependency, version, workflow,
  permission, or hosted allocation.

## M206 Windows cross-principal evidence validator

- **Task:** Add one offline, read-only validator and reviewed incomplete fixture
  for the M205 evidence envelope without running a privileged fixture or
  admitting Windows cleanup.
- **Status:** Locally complete; publication withheld by hosted ancestry.
- **Base:** fully locally validated M205 DCO commit
  `b678ca04de153f1908b7af73f15a471c93e9a486`, tree
  `5e28c9ea5dfa380af3ba8980af97320d156357c0`, sole parent exact M204.
- **Branch:** `release/m206-windows-cross-principal-evidence-validator`; exact
  containment made the local M205 branch name redundant, so only local `main`
  and active M206 remain.

### M206 acceptance boundary

- Read exactly one stable regular non-symlink file and require exact bounded
  canonical JSON with duplicate and unknown fields rejected.
- Enforce all 13 M205 lanes, all eight barrier identities, bounded
  trial/event totals, exact sanitized qualification/control/outcome fields,
  and exact source/executable digest syntax for attempted evidence.
- Cross-check every criterion claim. Only an all-passed complete document may
  set `criterion_6_satisfied` true; `windows_cleanup_admitted` remains false.
- Emit only path-free canonical validation output and retain no raw principal,
  token, account, credential, pathname, handle, ACL, environment, or platform
  error value.
- Ship a reviewed canonical fixture in which all lanes are `not_run`; describe
  it as incomplete schema evidence, never as a qualifying execution.
- Add integration and architecture coverage while preserving runtime,
  dependency, package, release, and vital-CI boundaries.
- Keep criteria 6 and 7 unresolved. Add no launcher, account lifecycle, native
  call, cleanup mutation, workflow, permission, or hosted allocation.

### Development evidence so far

- Exact M205 commit/tree/parent, clean worktree, protected hashes, maintainer
  identity, local/remote branch inventory, M99 hosted ancestry, and absent
  retired root control metadata were re-audited before work.
- The focused M205/canonical/rollback baseline passed 73 tests. Static and
  current-date strict governance checks passed with zero findings.
- Current RFC JSON guidance, Microsoft token-statistics documentation, and
  GitHub-hosted-runner documentation were reviewed before branching. The
  evidence supports one bounded canonical artifact, sanitized token-derived
  booleans, and no new hosted allocation.
- Neutral M206 starts from exact M205. The redundant local M205 branch name was
  removed while its commit remains the exact parent.
- The intentional architecture-red run passed two preservation checks and
  failed only the ten expected absent validator, fixture, decision/RFC, and
  registration checks.
- The source-only test validator, reviewed fixture, integration coverage,
  RFC-0189, security decision, and eight public registrations are implemented.
- Whole-tree format, Ruff, strict Pyright, the corrected 97-test architecture
  group, strict docs, static/current-date governance, and whitespace pass.
- Post-review complete suites pass on CPython 3.12, 3.13, and 3.14. Real wgpu,
  both profiles, profile-schema tests, Null/wgpu Clockwork Arena, and World
  Builder reproduce established results.
- Two initial distributions and two ten-artifact release stages are
  byte-identical; installed wheel/scene and complete release smokes pass. The
  114-entry wheel has zero forbidden payload and all six M206 artifacts are
  source-only within the 986-entry source archive.
- Findings-first review corrected negative barrier-order handling so failed and
  unsupported evidence remains structurally reviewable but criterion-false.
  The expanded focused group passes 73 tests.
- The record-inclusive locked environment, all static gates, 97 architecture
  tests, strict docs, static/current-date governance, and whitespace pass.
- Two final record-state builds reproduce a 363,790-byte pure wheel and a
  2,423,882-byte source archive; installed smokes and two byte-identical
  ten-artifact release stages pass. Inventory remains 114 wheel/986 source
  entries with all six M206 artifacts source-only.
- Terminating review confirms exactly 18 intended paths, no protected-surface,
  credential, private-key, root-metadata, or package-boundary finding. One
  pre-existing historical retired-tooling phrase was neutrally restated. All
  34 audited ignored/untracked/reparse-free M206 scratch targets were removed;
  zero remains.
- The final post-cleanup separator passes all 596-file static gates, 97
  architecture tests, strict docs, both governance modes, and whitespace. Its
  sole regenerated documentation directory was audited and removed; zero M206
  scratch remains.
- The pre-commit audit confirms exact M205 HEAD/tree/parent, exactly 18 intended
  paths, zero protected diff, only `main` plus neutral M206, configured
  maintainer identity, expected `0 106` local-main divergence, clean
  whitespace/static/architecture gates, zero scratch, and clean Git
  connectivity.

### Publication result

- Initial DCO commit `c1f90dd5d31a6b5b5938706e7fbed69051a76b0a`,
  tree `48fe26e1349876c5afa197033879917fc649a279`, has exact M205 as
  its sole parent, exactly 18 paths, one matching sign-off, consistent
  maintainer identity, clean revision whitespace, and a clean worktree.
- A fresh pruned fetch and direct hosted query leave public `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, tree
  `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`.
- M205 is absent from hosted `main`, M99 is present, only remote `main` exists,
  and divergence is `0 107`. A public API fallback confirmed an unarchived
  public repository, default branch `main`, and latest closed PR #251 after the
  local GitHub CLI credential was found invalid.
- Publishing M206 would expose the absent M100-M205 prerequisite stack. No
  push, PR, hosted allocation, tag, release, or package publication occurs.

### Publication boundary

- Publication remains authorized only after hosted `main` gains the complete
  prerequisite ancestry. The current safety gate withholds it.

### Explicit non-scope

- No qualifying cross-principal run, criterion 6 resolution, independent-host
  criterion 7 evidence, Windows cleanup admission, process launcher, account or
  credential management, native adapter, production cleanup, runtime command,
  dependency, version, workflow, permission, or hosted allocation.

## M205 Windows cross-principal validation contract

- **Task:** Define the exact adversarial evidence, principal qualification,
  credential-custody, process/session, ACL, handle, alias/reparse, and teardown
  contract required by M199 Windows cleanup admission criterion 6.
- **Status:** Locally complete; publication withheld by hosted ancestry.
- **Base:** fully locally validated M204 DCO commit
  `c4b670aab7305c4b1c34a88d5e0725dc1e9b57ce`, tree
  `382928168f7ba9000bee4fe3225c529582624925`, sole parent exact M203.
- **Branch:** `release/m205-windows-cross-principal-validation-contract`;
  exact containment made the local M204 branch name redundant, so only local
  `main` and active M205 remain.

### M205 acceptance boundary

- Require a genuinely distinct untrusted local principal with a different
  TOKEN_USER SID and independently authenticated logon context. Same-user
  restricted tokens, integrity changes, AppContainers, impersonation, and
  hosted administrator accounts do not qualify.
- Keep accounts and credentials operator-provisioned and outside repository
  inputs, files, environment, commands, logs, evidence, and CI secrets. Add no
  account or local-security-policy mutation.
- Require a trusted coordinator, trusted engine, and unrelated hostile process
  across separate process-tree, authenticated-logon, and Windows-session lanes.
- Require explicit handle inventories, allowlisted control-channel inheritance,
  zero cleanup-handle leakage, and cross-process duplication pressure.
- Exercise mandatory ACL, hard-link, reparse, rename, recreation, recovery,
  and channel-failure lanes with deterministic barriers rather than timing
  overlap.
- Emit one bounded canonical sanitized evidence document. Identity is derived
  by the coordinator from owned process/token handles, never participant
  self-report.
- Keep criteria 6 and 7 unresolved: M205 defines the contract but performs no
  qualifying cross-principal run and admits no Windows cleanup.
- Add no runtime, launcher, adapter, native call, integration fixture,
  dependency, metadata, version, workflow, permission, or hosted allocation.

### Development evidence so far

- Exact M204 commit/tree/parent, clean worktree, protected hashes, maintainer
  identity, local/remote branch inventory, M99 hosted ancestry, and absent
  retired root control metadata were re-audited before work.
- The frozen M204 guard passed 15 tests. Static and current-date strict external
  governance checks passed with zero findings.
- Current Microsoft access-token, process-launch, logon, ACL propagation,
  inheritance, hard-link, reparse, and GitHub-hosted-runner documentation was
  reviewed before branching. It supports an independent-principal contract and
  shows that the ordinary hosted administrator topology is not qualifying.
- Neutral M205 starts from exact M204. The redundant local M204 branch name was
  removed while its commit remains the exact parent.
- The intentional architecture-red run passed the two protected/no-runtime
  checks and failed the 17 absent contract/registration checks as expected.
- RFC-0188, the security contract, and eight public registrations now define
  the source-only boundary. After normalizing Markdown-interrupted guarded
  phrases, all 19 focused architecture tests pass; focused Ruff and strict
  Pyright are clean.
- Whole-tree format, Ruff, strict Pyright, the corrected 85-test architecture
  group, strict docs, static/current-date governance, and whitespace pass.
- Complete suites pass on CPython 3.12, 3.13, and 3.14. Real wgpu, both M7
  profiles, eight profile tests, Null/wgpu Clockwork Arena, and World Builder
  reproduce their established results.
- Two distributions are byte-identical; installed wheel and scene smokes pass;
  two byte-identical ten-artifact release stages pass complete smoke. Inventory
  is 114 wheel and 980 source entries, with all three M205 files source-only.
- Findings-first review restored the historical current-task record that an
  initial replacement had removed and normalized one restored retired metadata
  reference. Exactly 15 intended paths remain, with zero protected-surface,
  credential, machine-path, private-key, native-import, or package-boundary
  finding.
- The record-inclusive lock/environment, static quality, 85-test architecture,
  strict-docs, governance, and whitespace separator passes. Two fresh
  record-state builds reproduce the unchanged wheel and a 2,405,791-byte source
  archive; installed smokes and two byte-identical ten-artifact release stages
  pass, with the 114/980 inventory unchanged.
- A final static/docs/governance/whitespace separator passes. Twenty initial
  scratch targets and the one documentation directory regenerated by the final
  separator were each proven repository-confined, ignored, untracked, and
  reparse-free before exact guarded removal. Zero M205 scratch remains.
- The terminating pre-commit audit confirms exact M204 HEAD/tree/parent,
  exactly 15 intended paths, only local `main` plus neutral M205, configured
  maintainer identity, expected `0 105` local-main divergence, zero protected
  diff, zero scratch, clean whitespace/static/architecture gates, clean added-
  content hygiene, and clean Git connectivity apart from historical dangling
  objects.
- The first local DCO commit has exact M204 as its sole parent and the 15-path
  scope, but the staged whitespace check surfaced two Markdown hard-break spaces
  and one final blank line in RFC-0188. PowerShell continued to the commit after
  reporting them. Those three whitespace defects are corrected for the
  closeout amendment; no public state changed.
- The corrected amended DCO commit
  `c38ea2d148f8f68d4e5afc7e69990c0397e17230`, tree
  `8d3509a97f55e4051d2a078151a2ca84f25dc0e7`, has sole parent exact M204,
  exactly 15 paths, one matching sign-off, consistent maintainer identity,
  clean revision whitespace, `0 106` local-main divergence, a clean worktree,
  zero scratch, and dangling-only Git object output.

### Publication result

- A fresh pruned fetch and direct hosted query leave public `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, tree
  `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`.
- M204 is absent from hosted `main`, M99 is present, only remote `main` exists,
  divergence is `0 106`, and PR #251 remains latest.
- Publishing M205 would expose the absent M100-M204 prerequisite stack. No
  push, PR, hosted allocation, tag, release, or package publication occurs.

## M204 Windows cleanup durable recovery policy

- **Task:** Resolve M199 Windows cleanup admission criterion 5 as an exact,
  bounded durable-intent, same-filesystem quarantine, restart-reconciliation,
  and rollback-tamper policy without admitting cleanup or adding runtime or CI
  surface.
- **Status:** Locally complete; publication withheld. Exact M203 baseline, current primary-source research,
  neutral branch containment, intentional architecture red, accepted RFC and
  security decision, public registrations, focused and whole-project quality,
  supported-Python suites, rendering/profile/examples, initial reproducible
  package/release rehearsal, archive inventory, and findings-first review are
  complete. Record-inclusive validation/package rehearsal is also complete.
  Final separators, guarded cleanup, pre-commit audit, local DCO commit, and
  hosted publication-safety reconciliation are complete. Publication is
  withheld because hosted `main` remains exact M99 and does not contain M203
  or the M100-M203 prerequisite stack.
- **Base:** Fully locally validated M203 DCO commit
  `14bcd3be32bbec92538d4f92d223115d57a9e6aa`, tree
  `5083ee04bdcb879ffa20a2bbad4afe7412b9fe28`, sole parent exact M202.
- **Branch:** `release/m204-windows-cleanup-durable-recovery-policy`; the
  redundant local M203 branch name was removed after exact M204 branch creation
  retained its object.

### M204 acceptance boundary

- Keep one private, same-volume, root-confined recovery store and at most one
  active operation per trusted root and generation; records remain evidence,
  not world state or authority.
- Reserve a bounded immutable canonical hash-chain policy with write-ahead
  staging, flush, no-replace publication, parent settlement, retained-handle
  reopen, and exact verification before a phase is durable.
- Require durable intent and replay lookup before accepted acknowledgement;
  bind public receipt phase/outcome to the last durable state without claiming
  exactly-once effects or delivery.
- Quarantine the same admitted object through retained handles on the same
  volume, into an absent engine-generated slot, with no replacement or
  copy/delete fallback.
- On restart, reacquire fresh private authority, replay the bounded chain,
  reconcile exact original/quarantine observations, and append only the unique
  justified next transition without repeating an observed effect.
- Allow no-replace restoration only before the durable deletion commitment.
  After that boundary, never guess rollback or infer successful deletion from
  absence alone.
- Block the complete root and generation on invalid chains, unknown entries,
  security/generation mismatch, object mismatch, or ambiguous physical state;
  preserve evidence and perform no automatic repair, deletion, or restoration.
- Resolve criterion 5 as policy, retain criteria 1 through 4 as policy, and
  leave criteria 6 and 7 unresolved. Windows remains unadmitted and cleanup
  remains unimplemented and unauthorized.
- Preserve exact M203, runtime, fixtures, examples, scripts, dependencies,
  metadata, workflows, permissions, version, and package surface. Add no
  command, public constant/type, recovery store implementation, native adapter,
  mutation, or hosted check.

### M204 development evidence so far

- Exact M203 commit/tree/parent, clean worktree, protected hashes, maintainer
  identity, and two-branch inventory were reverified. The exact M203
  architecture module passed all 12 tests in 0.57 seconds.
- Static and current-date strict external governance each returned pass with
  zero findings across three objectives, seven requirements, and four work
  items.
- Current Microsoft primary documentation was reviewed for TxF alternatives,
  rename/replace behavior, cross-volume fallback, caching, flushing, and
  handle-relative metadata updates. It supports a policy-only application
  recovery protocol while retaining criteria 6 and 7 for hostile and
  independent power-loss proof.
- Neutral M204 starts from exact M203. Exact containment made the local M203
  branch name redundant, so only local `main` and active M204 remain.
- The intentional architecture-red run passed the protected-boundary and no-
  runtime checks and failed only the 13 absent RFC, security-decision, and
  registration contracts in 0.85 seconds.
- RFC-0187, the security decision, and eight public registrations define the
  complete no-authority-increase policy. The first focused run passed eight
  checks and exposed seven Markdown-format wording mismatches; factual wording
  was normalized without weakening policy. All 15 checks then passed in 0.56
  seconds.
- Initial whole-project format, Ruff, strict Pyright, 66-test architecture,
  strict docs, static/current-date governance, and whitespace gates pass. The
  first lock/sync attempts were cache-denied before checking; their exact
  access-enabled reruns pass. Strict docs first caught four incorrect ADR
  filenames; corrected links pass the exact rerun.
- Complete isolated CPython 3.12, 3.13, and 3.14 suites each pass 4,131 tests
  with 18 skips. Ten real-wgpu tests, fresh base/graphics profile validation,
  eight profile tests, both 600-tick Clockwork renderers, and Agent World
  Builder reproduce their established identities.
- Two initial distributions are byte-identical; installed wheel/scene smoke
  passes; two byte-identical ten-artifact release stages pass complete smoke.
  Inventory is 114 wheel and 977 source entries, with all three M204 evidence
  files source-only and zero forbidden wheel entry.
- Findings-first review corrected stale ADR filenames, clarified bound
  exhaustion and immutable-chain wording, normalized one protocol status, and
  made the phase graph unambiguous. Exactly 15 intended paths remain, protected
  runtime/package/CI surfaces have zero diff, and 1,013 inspected added lines
  contain no development-tool identity, credential assignment, or machine-
  local path. The corrected focused review gate passes all 15 checks.
- The record-inclusive lock/sync, format, Ruff, strict Pyright, 66-test
  architecture, strict docs, static/current-date governance, and whitespace
  separator passes. Two record-state builds reproduce the 363,517-byte wheel
  and a 2,390,949-byte source archive; installed wheel/scene and both complete
  release smokes pass. Both ten-artifact stages are byte-identical and the
  114-wheel/977-source package boundary remains exact.
- The final pre-cleanup and post-cleanup format/Ruff/Pyright, 66-test
  architecture, strict-docs, static/current-date governance, and whitespace
  separators pass. A terminating audit proved 21 initial M204 scratch targets
  repository-confined, ignored, untracked, and reparse-free before guarded
  removal. The post-cleanup separator regenerated only one docs directory;
  its corrected exact audit and revalidated removal leave zero M204 scratch.
- Pre-commit audit confirms exact M203 ancestry, exactly 15 intended paths,
  only local `main` plus neutral M204, configured maintainer identity, zero
  protected-surface diff, clean static/focused/whitespace gates, zero M204
  scratch, absent retired root control metadata, clean added-content hygiene,
  and clean Git connectivity
  apart from historical dangling objects.
- Initial DCO commit `2411d1519cc25dcb54556cbe7af8a7bd0b7459e9`,
  tree `933e46fb37af67943efad57447bf3ae3de862f6f`, has sole parent exact M203,
  exactly 15 files, one matching sign-off, consistent configured maintainer
  identity, a clean worktree, and `0 105` divergence from local M99 `main`.
- Fresh fetch/prune, direct hosted-head query, local hosted-ref/tree/ancestry,
  authenticated repository/default-branch query, and recent PR history prove
  hosted `main` is exact M99, M203 is absent, only remote `main` exists, and PR
  #251 remains latest. No push, PR, hosted allocation, tag, release, or package
  publication occurs.

## M203 Windows cleanup protocol and receipt policy

- **Task:** Resolve M199 Windows cleanup admission criterion 4 as an exact,
  bounded request/acknowledgement/receipt policy without admitting cleanup or
  adding runtime or CI surface.
- **Status:** Locally complete; publication withheld. Exact M202 baseline, current primary-source
  research, neutral branch containment, intentional architecture red, accepted
  RFC/security decision, eight public registrations, focused and whole-project
  quality, supported-Python suites, rendering/profile/examples, reproducible
  package/release rehearsal, findings-first review, record-inclusive package/
  quality separators, guarded scratch cleanup, and final post-cleanup separator
  are complete. The local DCO commit/object audits and fresh hosted publication-
  safety gate pass. Publication is withheld because hosted `main` remains exact
  M99 and does not contain M202 or the M100-M202 prerequisite stack.
- **Base:** Fully locally validated M202 DCO commit
  `e95be9726f8b00c5aef81192c6fba23813602e1f`, tree
  `e08c7aa0b143d7b8c46c14362dcb0c6ad8d97e6f`, sole parent exact M201.
- **Branch:** `release/m203-windows-cleanup-protocol-receipt-policy`; the
  redundant local M202 branch name was removed after exact M203 branch creation
  retained its object.

### M203 acceptance boundary

- Reserve distinct versioned cleanup request, acknowledgement, and receipt
  document identities outside world command/transaction/receipt v1.
- Require one complete bounded canonical UTF-8 JSON object per call; reject
  notifications, batches, sequences, partial parsing, trailing bytes,
  duplicate/unknown fields, and limit violations.
- Keep requests path/candidate/native-data-free and make actor attribution,
  dry-run, and caller intent explicitly non-authorizing.
- Bind acknowledgement to request/operation IDs and canonical request digest;
  acceptance means bounded admission only, never mutation or success.
- Bind receipts to request and acknowledgement digests; expose only bounded,
  path-free, operation-local typed outcomes and retain evidence-not-authority
  semantics.
- Bind retry identity without claiming exactly-once behavior; leave durable
  lookup, recovery transitions, and delivery-loss reconciliation to criterion
  5.
- Resolve criterion 4 as policy, retain criteria 1 through 3 as policy, and
  leave criteria 5 through 7 unresolved. Windows remains unadmitted and cleanup
  remains unimplemented and unauthorized.
- Preserve exact M202, runtime, fixtures, examples, scripts, dependencies,
  metadata, workflows, permissions, version, and package surface. Add no
  decoder, command, protocol constant, public type, receipt store, adapter,
  mutation/recovery code, or hosted check.

### M203 development evidence so far

- Exact M202 history/tree/parent, clean worktree, and branch inventory were
  reverified. The M202 architecture guard passed all ten tests in 0.56 seconds.
- Static governance returned pass with zero findings. The first current-date
  strict invocation was denied managed-cache access before checking; its exact
  access-enabled rerun passed with zero findings across three objectives, seven
  requirements, and four work items.
- Current RFC, JSON-RPC, and NIST primary guidance supports one bounded complete
  canonical document, mandatory correlation, and typed evidence while rejecting
  notification/batch/stream-recovery and authenticity/durability overclaims.
- Neutral M203 starts from exact M202. Exact containment made the local M202
  branch name redundant, so only local `main` and active M203 remain.
- The intentional architecture-red run passed two protected containment/no-
  implementation checks and failed only ten absent RFC, decision, and public-
  registration contracts in 0.85 seconds.
- RFC-0186, the security decision, and eight public registrations define the
  complete no-authority-increase policy. The first focused run passed ten
  checks and exposed two markdown wording mismatches; the factual phrases were
  normalized without weakening policy. All twelve checks then passed in 0.56
  seconds, and focused format, Ruff, and strict Pyright are clean.
- Whole-project format, Ruff, strict Pyright, architecture, strict docs,
  governance, and whitespace gates pass. Complete CPython 3.12, 3.13, and 3.14
  suites each pass 4,126 tests with 17 skips; the 3.13 suite was repeated to
  capture an authoritative exit code after its first output channel was lost.
- Ten real-wgpu tests, both fresh M7 profiles and validators, eight profile
  tests, Null/wgpu Clockwork Arena, and Agent World Builder reproduce their
  established deterministic identities.
- Two distributions are byte-reproducible; installed wheel/scene smoke passes;
  two byte-identical ten-artifact release stages pass complete smoke. Inventory
  is 114 wheel and 974 source entries, with all three M203 evidence files
  source-only and zero forbidden wheel entry.
- Findings-first review corrected one RFC spelling of the exact
  `recovery_required` status. Exactly 15 intended paths remain, protected
  runtime/package/CI surfaces have zero diff, and added M203 content contains
  no development-tool identity, credential assignment, or machine-local path.
- Record-inclusive quality/governance passes. Two final record-state builds
  reproduce the unchanged pure wheel and one source archive; installed wheel/
  scene smoke and both byte-identical ten-artifact release smokes pass.
- A read-only exact audit proved 21 M203 scratch targets repository-confined,
  ignored, untracked, and reparse-free. Guarded deletion removed exactly those
  generated targets and proved none remains.
- The post-cleanup format/Ruff/Pyright, 51-test architecture, strict-docs,
  static/dated-governance, and whitespace separator passes. Its sole regenerated
  docs directory was independently audited and removed; no M203 scratch remains.
- Initial DCO commit `f11e5b5ed5e0c2ba3739bb630e50ca0c5ad0a023`
  has tree `c55b1eb833626da07c154b0e31faa0ed8508054b`, sole parent exact M202,
  exactly 15 files, one matching sign-off, configured maintainer identity, a
  clean worktree, and clean connectivity apart from historical dangling objects.
- Fresh fetch/prune, direct hosted-head query, local hosted-ref/tree/ancestry,
  authenticated repository/default-branch query, and recent PR history prove
  hosted `main` is exact M99, M202 is absent, only remote `main` exists, and PR
  #251 remains latest. No push, PR, hosted allocation, tag, release, or package
  publication occurs.

## M202 Windows use-time revalidation policy

- **Task:** Resolve M199 Windows cleanup admission criterion 3 as an exact,
  fail-closed use-time revalidation policy without admitting cleanup or adding
  runtime or CI surface.
- **Status:** Locally complete; publication withheld.
  Explicit approval, current primary-source direction research, exact M201
  baseline, neutral branch containment, intentional architecture red, accepted
  RFC/security decision, public registration, focused and whole-tree gates,
  supported-Python coverage, graphics/profile/examples, reproducible package
  and release rehearsal, inventory, findings-first review, and record-inclusive
  separator, final record-state distribution, guarded cleanup, and post-cleanup
  validation, pre-commit audit, local DCO object verification, factual closeout,
  and final publication-safety reconciliation are complete. Publication is
  withheld because hosted `main` remains at M99 and lacks the M100-M201
  prerequisite chain.
- **Base:** Fully locally validated M201 DCO commit
  `df54db0fa4b188048cfcb1075a9f5dc7934e6749`, tree
  `dd9c65821a294ddbbb8dced43a4867d0a976e1d1`, sole parent exact M200.
- **Branch:** `release/m202-windows-use-time-revalidation-policy`; the redundant
  local M201 branch name was removed after exact M202 branch creation retained
  its object.

### M202 acceptance boundary

- Retain the exact admitted effective-token, trusted-root, durable-generation,
  acquisition-lineage, and candidate objects through use-time revalidation.
- Freshly compare the complete token/root/generation/lineage/candidate tuple
  with admission immediately before every mutation boundary.
- Refresh exact least-privilege token and root-security decisions plus handle-
  derived identity/type/link/delete/reparse/root/generation facts.
- Hold the non-reentrant single-owner gate and retained references without an
  application-introduced gap into the same-handle mutation.
- Leave the candidate untouched on failure before the first mutation; after a
  completed transition, stop before deletion and require deferred recovery.
- Resolve criterion 3 as policy, retain criteria 1 and 2 as policy, and leave
  criteria 4 through 7 unresolved. Windows remains unadmitted and cleanup
  remains unimplemented and unauthorized.
- Preserve exact M201, runtime, fixtures, examples, scripts, dependencies,
  metadata, workflows, permissions, version, and package surface. Add no
  adapter, command, protocol, receipt, mutation/recovery code, or hosted check.

### M202 development evidence so far

- Exact M201 history/tree/parent, maintainer identity, hosted-main divergence,
  and branch inventory were rechecked before work. The M201 architecture guard
  passed all nine tests in 0.26 seconds.
- Static and current-date strict external governance gates each returned pass
  with zero findings across three objectives, seven requirements, and four
  work items.
- Current Microsoft primary sources support exact handle-derived identity,
  type/link state, effective-token/security queries, least-privilege access
  checking, and same-handle mutation. They also explicitly preserve the
  non-atomic race boundary, so M202 adds policy only and no hosted allocation.
- Neutral M202 starts from exact M201. Exact containment made the local M201
  branch name redundant, so only local `main` and active M202 remain.
- The intentional architecture-red run passed two protected containment/no-
  implementation checks and failed only eight absent RFC, decision, and public-
  registration contracts in 0.51 seconds.
- RFC-0185, the security decision, and eight public registrations define the
  complete no-authority-increase policy. The first focused run passed nine
  checks and exposed one markdown-format mismatch in the guarded Microsoft
  race-limit phrase; the factual text was normalized, and all ten checks then
  passed in 0.25 seconds. Focused format, Ruff, and strict Pyright are clean.
- Whole-tree static/docs/governance gates and the 39-check architecture review
  group are clean. Complete CPython 3.12, 3.13, and 3.14 suites each pass 4,114
  tests with 17 skips.
- Real-wgpu, fresh profile contracts, and both deterministic vertical slices
  reproduce established results. Two distribution builds and two complete
  release stages are byte-identical; installed wheel/scene/release smokes and
  the 114-wheel/971-source package boundary pass.
- Findings-first review confirms exactly 15 intended paths, zero protected-
  surface diff, zero new hosted allocation, and no actionable finding.
- The record-inclusive separator remains clean across all 590 Python files,
  the 39-check architecture group, strict docs, static/current-date governance,
  and whitespace.
- Two exact record-state builds reproduce a 363,290-byte pure wheel and
  2,361,437-byte source archive. Installed-wheel/scene and both complete
  release-stage smokes pass; the stages are byte-identical and the 114/971
  package boundary remains exact.
- A terminating audit proved all 18 exact generated targets confined, ignored,
  untracked, and recursively reparse-free. Revalidating removal deleted all 18
  and proved the zero-target postcondition without a tracked-path or ACL change.
- The final post-cleanup separator passes all static, 39 architecture, strict-
  docs, governance, and whitespace gates. Its sole regenerated ignored docs
  target was revalidated, removed, and proved absent.
- Pre-commit audit confirms exact M201 ancestry, exactly 15 intended paths,
  only local `main` plus neutral M202, correct maintainer identity, zero
  protected-surface diff, clean static/architecture/whitespace gates, zero
  scratch, and clean Git connectivity apart from historical dangling objects.
- Initial local commit `2cbde10cf04701dedaa128d78c2f48f39d4a54b2` has
  the exact 15-path tree, sole parent M201, consistent maintainer identity, one
  matching DCO trailer, clean worktree, and expected `0 103` divergence. This
  factual object record is folded into one closeout amendment.
- A fresh pruned fetch and direct hosted-head query leave public default
  `origin/main` at exact M99 with PR #251 latest, only remote `main`, and M201
  absent from hosted ancestry. Publishing would expose M100-M201, so no push,
  PR, hosted allocation, tag, release, or package publication occurs.

## M201 Windows cleanup-authority admission policy

- **Task:** Resolve M199 Windows cleanup admission criterion 1 as an exact,
  fail-closed authority policy without admitting cleanup or adding runtime or
  CI surface.
- **Status:** Locally complete. Explicit approval, current primary-source
  direction research, exact M200 baseline, neutral branch containment,
  governance correction, intentional architecture red, accepted RFC/security
  decision, public registration, focused and whole-project validation,
  supported-Python coverage, rendering/profile/vertical-slice checks,
  reproducible package/release rehearsal, findings-first review, record-
  inclusive closeout, guarded scratch cleanup, post-cleanup validation, pre-
  commit audit, local DCO commit, and publication-safety reconciliation pass.
  Publication is withheld because hosted `main` remains at M99 and lacks the
  M100-M200 prerequisite chain.
- **Base:** Fully locally validated M200 DCO commit
  `42428005cbf2b3fbcd47c787504bab5e0a235804`, tree
  `cd2429fa610a414ca35bee3df6f29447661d3528`, sole parent exact M199.
- **Branch:** `release/m201-windows-cleanup-authority-admission-policy`; the
  redundant local M200 branch name was removed after exact M201 branch creation
  retained its object.

### M201 acceptance boundary

- Accept RFC-0184 and one public Windows cleanup-authority admission policy.
- Permit future issuance only from the trusted composition root after exact
  effective-token, retained identity/security-bound root, and separate durable-
  generation bindings all pass.
- Bind `TOKEN_USER` user SID plus `TOKEN_STATISTICS` token ID, authentication
  ID, modified ID, token type, and impersonation level; reject anonymous,
  identification-only, missing, malformed, changed, or unsupported context.
- Require a retained root handle, `FILE_ID_INFO` identity, ordinary non-reparse
  directory type, owner match, non-null trusted DACL, and a versioned least-
  privilege access profile. Paths and handle-open success supply no authority.
- Require a separate immutable, root-confined, versioned durable generation
  record bound to project/cache, root, policy, record identity, and canonical
  SHA-256. Token/logon/process/path values cannot substitute for generation.
- Keep the future capability private, engine-owned, non-serializable,
  operation-scoped, single-use, cleanup-only, and silent about raw security
  material. World-write capability, request data, and saved evidence cannot
  mint or widen it.
- Resolve criterion 1 as policy only, retain criterion 2, and keep criteria 3
  through 7 unresolved. Windows cleanup remains unimplemented and unauthorized.
- Preserve exact M200, runtime, fixtures, examples, scripts, dependencies,
  metadata, workflows, permissions, version, and package surface. Add no
  production adapter, public authority, generation state, command, cache
  access, mutation, native code, workflow, job/allocation, or hosted check.

### M201 development evidence so far

- Maintainer approval named the exact M201 policy milestone after two current
  primary-source scans distinguished world-write capability from Windows
  principal/root/generation authority.
- Exact M200 HEAD/tree/parent and configured maintainer identity were
  reverified. The eight-assertion M200 architecture guard passed in 0.85
  seconds before edits.
- The first dated strict governance attempt was denied access to the managed uv
  cache before checking. Its access-enabled exact rerun returned pass with zero
  findings across three objectives, seven requirements, and four work items.
- One exploratory invocation pointed the external governance checker at
  LudoWeave and returned `registry.unreadable`; that checker owns a separate
  project registry and is not LudoWeave's traceability format. The prescribed
  checker-package static invocation returned pass with zero findings.
- Neutral M201 starts from exact M200. Exact containment made the local M200
  branch name redundant, so only local `main` and active M201 remain.
- The intentional architecture-red run passed exact protected-boundary and no-
  implementation checks and failed only seven absent RFC, decision, and public-
  registration contracts.
- RFC-0184, the security decision, and eight public registrations define the
  complete no-authority-increase policy. The corrected focused gate passes all
  nine checks; focused format, lint, and strict typing are clean; and the exact
  repository-hygiene/M199/M200/M201 group passes all 29 checks.
- The complete CPython 3.12, 3.13, and 3.14 suites pass with respective totals
  of 4,104/17, 4,094/18, and 4,094/18 passed/skipped tests. The 3.14 result is a
  clean solo monolithic run, so no shard fallback is claimed.
- The restored 45-package CPython 3.12 graphics environment passes ten real-
  wgpu tests, fresh two- and three-workload profile validation, both 600-draw
  Clockwork Arena modes, and Agent World Builder with established state,
  capture, and replay identities.
- Two initial builds are byte-identical; installed wheel/scene and both ten-
  artifact release smokes pass. Inventory is 114 wheel and 968 source entries,
  with all three M201 evidence files source-only and zero forbidden wheel entry.
- Findings-first review covers exactly 15 intended paths with no protected
  runtime, integration, dependency, workflow, package, identity, machine-path,
  credential-assignment, scope, correctness, security, or documentation issue.
- The record-inclusive separator remains clean, and two fresh builds reproduce
  the 114-entry pure wheel and 968-entry source archive. Installed-wheel,
  installed-scene, both complete ten-artifact release stages, byte comparison,
  and source-only M201 evidence inventory all pass.
- A terminating-error audit proved 41 exact generated targets repository-
  confined, ignored, untracked, and recursively reparse-free. Revalidating
  deletion removed those targets and reached a verified zero-target
  postcondition without changing a tracked path or ACL.
- The final post-cleanup separator passes; its only two regenerated ignored
  cache targets were separately revalidated, removed, and verified absent.
- Pre-commit audit confirms exact M200 ancestry, 15 intended paths, zero
  protected-surface diff, only local `main` plus neutral M201, configured
  maintainer identity, clean static/architecture/whitespace gates, zero scratch,
  clean object connectivity apart from historical dangling objects, and no
  development-identity, machine-path, or credential-assignment match.
- Initial local DCO commit `fe8295e6572bd9be2e6830b541a5a8d80ce07902`
  has tree `967739c36af24a372662fed2afccc7c48eaf6232`, sole parent exact
  M200, exactly 15 paths, matching configured author/committer identity, one
  matching sign-off, a clean worktree, and `0 102` divergence from local M99
  `main`. This factual record is incorporated by one closeout amendment.
- Fresh pruned and direct hosted checks leave only remote `main` at exact M99;
  M200 is not its ancestor and PR #251 remains latest. Publishing M201 would
  expose 101 unpublished prerequisite milestones, so no push, PR, hosted check,
  tag, release, or package publication occurs.

## M200 Windows singleton-link refusal policy

- **Task:** Resolve M199 Windows cleanup admission criterion 2 as a strict
  singleton-link refusal policy without admitting cleanup or adding runtime or
  CI surface.
- **Status:** Exact M199 baseline, governance, neutral branch containment,
  intentional architecture red, accepted RFC/security decision, public
  registration, focused and whole-tree static gates, supported-Python coverage,
  rendering/examples, reproducible packaging/release rehearsal, findings-first
  review, record-inclusive closeout, guarded cleanup, post-cleanup validation,
  pre-commit audit, initial DCO object verification, and hosted publication-
  safety reconciliation pass. The closeout amendment remains; publication is
  withheld because hosted `main` lacks M100-M199.
- **Base:** Fully locally validated M199 DCO commit
  `31d786f203de0e51b08f13f72a0340ff8c44e27a`, tree
  `d1a62006d7c116b2859bca50687be022d40b665c`, sole parent exact M198.
- **Branch:** `release/m200-windows-singleton-link-refusal-policy`; the
  redundant local M199 branch name was removed after exact M200 branch creation
  retained its object.

### M200 acceptance boundary

- Accept RFC-0183 and one public singleton-link refusal decision.
- Require the same retained opened object to report a handle-derived link count
  of exactly one at admission and immediately before mutation.
- Refuse before mutation for zero, multiple, changed, unavailable, invalid, or
  unsupported counts. Do not use saved/pathname observations as fallback.
- Do not enumerate hard-link names for admission or authority. Treat any future
  enumeration only as separately approved, bounded, non-authoritative evidence.
- Resolve criterion 2 as policy only. Keep criterion 1 and criteria 3 through 7
  unresolved, including production use-time enforcement.
- Keep Windows cleanup unimplemented and unauthorized. Preserve exact M199,
  runtime, fixtures, examples, scripts, dependencies, metadata, workflows,
  permissions, version, and package surface.
- Add no production adapter, command, public capability, cache access,
  quarantine, mutation, native code, dependency, workflow job/allocation,
  permission, credential, release effect, or hosted check.

### M200 development evidence so far

- The clean exact M199 baseline retained only local `main` and M199. Its seven-
  assertion architecture guard passed in 1.98 seconds.
- Static governance returned pass with zero findings across three objectives,
  seven requirements, and four work items.
- Neutral M200 starts from exact M199. Exact containment made the local M199
  branch name redundant, so only local `main` and active M200 remain.
- The intentional architecture-red run passed three containment/inventory/no-
  implementation checks and failed only five absent RFC, decision, and public-
  registration contracts.
- RFC-0183, the security decision, and eight public registrations define the
  fail-closed policy. All eight focused architecture assertions pass in 1.24
  seconds.
- Focused Ruff lint and strict Pyright pass. The first Ruff format check
  requested one mechanical reformat; that formatting has been applied.
- The first three-interpreter complete run correctly exposed that the original
  M200 decision filename entered M199's protected 50-record glob. Renaming only
  that decision outside the historical probe namespace preserved exact M199;
  the combined M199/M200 guard now passes 15 checks.
- Exact CPython 3.12.13 and 3.13.13 complete suites each pass 4,095 tests with
  17 skips. Two CPython 3.14.5 monolithic attempts each pass 4,094 tests with 17
  skips but encounter different unchanged 15-second subprocess-fixture
  timeouts. Disjoint 3.14 core, non-cache integration, and Windows cache-
  cleanup shards cover the complete inventory and pass 4,095 tests with 17
  skips; the two timed-out tests pass in the accepted shards.
- Ten real-wgpu tests, fresh base/graphics profiles, eight profile tests, Null
  and wgpu Clockwork Arena, and Agent World Builder pass with established
  identities.
- Two distributions and two ten-artifact release stages are byte-identical;
  installed wheel/scene and both complete release smokes pass. Inventory is 114
  pure wheel and 965 source entries with all three M200 files source-only.
- Findings-first review retains exactly 15 intended paths, zero protected
  runtime/fixture/dependency/workflow diff, 20 passing hygiene/M199/M200 tests,
  and zero development-identity, credential-assignment, or machine-local-path
  match across 654 added lines. No actionable M200 finding remains.
- Record-inclusive lock/environment, whole-tree static checks, 20 review tests,
  strict docs, both governance modes, whitespace, reproducible distributions,
  installed smokes, and both byte-identical ten-artifact release rehearsals
  pass.
- Final pre-cleanup validation passes. An access-enabled audit proved 36 exact
  `.tmp/m200*` targets confined, ignored, untracked, direct-child, and recursively
  reparse-free. The deletion wrapper returned before its process exit, so an
  intermediate check found seven targets; the continuing bounded deletion then
  reached a verified zero-target postcondition. Final post-cleanup validation
  passes, and the sole regenerated docs target was separately audited and
  removed. Zero M200 scratch remains.
- Pre-commit audit confirms exact M199 HEAD/tree and sole-parent shape, exactly
  15 intended paths, zero protected runtime/fixture/package/CI diff, only local
  `main` and neutral M200, expected `0 100` divergence, configured maintainer
  identity, zero scratch, clean whitespace/object connectivity, 20 passing
  review checks, strict governance, and zero public-hygiene match across 732
  added lines.
- Initial DCO commit `2d0fd45633f69aa29ba74d60305976bd033bd8cf`,
  tree `f25ce04801feaaa4a79c27b88e1a5baeafe6e976`, has sole parent exact
  M199, exactly 15 paths, one matching sign-off trailer, consistent configured
  identity, no merge, expected `0 101` divergence, clean whitespace and object
  connectivity, a clean worktree, and zero scratch.
- A fresh pruned fetch and hosted inspection leave only remote `main` at exact
  M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; M198 and M199 are not
  ancestors, and PR #251 remains latest. Publishing M200 would expose the
  absent M100-M199 stack, so no push, PR, hosted allocation, tag, release, or
  package publication occurs.

## M199 Windows cache-cleanup readiness refresh

- **Task:** Consolidate M149-M198 as a complete Windows cleanup threat-model
  evidence set, retain the cleanup deferral, close standalone method-level
  closed-stream probing, and require future work to resolve a named admission
  criterion.
- **Status:** Direction research, exact M198 baseline, governance, neutral
  branch containment, intentional architecture red, public decision
  documentation, focused/static validation, supported-Python regression,
  rendering, reproducible distribution/release rehearsal, and findings-first
  review, record-inclusive validation, cleanup, initial local DCO object audit,
  and hosted publication-safety gates pass. The closeout amendment remains;
  publication is withheld because hosted `main` lacks M100-M198.
- **Base:** Fully locally validated M198 DCO commit
  `36f2778c1924409e9916611f49996c513d4c7185`, tree
  `1a849f5ee00012f01ed0056520dfc8e06746637b`, sole parent exact M197.
- **Branch:** `release/m199-windows-cache-cleanup-readiness-refresh`; the
  redundant local M198 branch name was removed after exact M199 branch creation
  retained its object.

### M199 acceptance boundary

- Accept RFC-0182 and one public Windows cache-cleanup readiness decision.
- Treat M149-M198 as exactly 50 current-host, test-only milestones with 50
  corresponding Windows integration probes and 50 pre-M199 security records.
- Keep Windows cleanup unimplemented and unauthorized. Require authenticated
  trusted-root authority, complete hard-link policy, use-time identity and
  link-count revalidation, acknowledged typed receipts, durable intent and
  idempotent recovery, cross-principal adversarial evidence, and independent-
  host proof before admission.
- Close standalone method-by-method closed-stream probing after M198. Require a
  future Windows cleanup milestone to resolve a named admission criterion.
- Preserve exact M198, runtime, examples, scripts, dependencies, metadata,
  workflows, permissions, fixtures, and package surface.
- Add no cleanup command, public probe, adapter, cache access, native code,
  dependency, workflow, job/allocation, permission, version, release authority,
  tag, or publication.

### M199 development evidence so far

- Exact M198 architecture/live baseline passed nine tests in 0.53 seconds.
- Static strict governance returned zero findings. The first current-date
  invocation was denied managed-cache access before checking; its exact access-
  enabled rerun returned zero findings across three objectives, seven
  requirements, and four work items.
- Current Microsoft file identity, hard-link, and access-control documentation;
  Python closed-stream semantics; GitHub Actions security/billing guidance;
  NIST SSDF 1.2 draft; and SLSA 1.2 support a no-authority-increase readiness
  refresh and reject more standalone closed-stream method probes as admission
  evidence.
- Neutral M199 starts from exact M198. Exact containment made the local M198
  branch name redundant, so only local `main` and active M199 remain.
- The intentional architecture-red phase passed three containment/inventory
  checks and failed only four absent decision, RFC, and public-registration
  boundaries.
- RFC-0182, the readiness decision, and eight public registrations now state
  the deferred outcome. The first public-integrated run passed six checks and
  found one missing exact stopping-rule phrase; after adding it, all seven
  checks pass.
- Focused Ruff lint passed before formatting. Ruff requested one mechanical
  reformat. One first Pyright command named a nonexistent duplicated-suffix
  path and therefore performed no type validation. The corrected file is now
  format- and lint-clean, strict Pyright returns zero findings, and all seven
  focused checks pass in 0.27 seconds.
- The unchanged lock and 45-package graphics environment pass. All 587 Python
  files are format-clean; Ruff and strict Pyright return zero findings; strict
  docs, static and current-date governance, and whitespace pass.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 complete suites each pass 4,087
  tests with 17 skips in 267.45, 268.74, and 280.10 seconds. The isolated 3.13
  and 3.14 environments each install the same 45-package graphics set.
- Ten real-wgpu tests pass. Fresh base and graphics M7 profiles validate two
  and three workloads; a first profile-test command named one nonexistent file
  and is excluded, while the corrected eight-test module passes. Null and wgpu
  Clockwork Arena plus Agent World Builder reproduce established identities.
- Two distribution builds reproduce a 362,959-byte pure wheel at SHA-256
  `115e1470a084d99230a1eba1406271a5ecb0fae215fd42bec114be698fa53fae`
  and a 2,322,347-byte source archive at SHA-256
  `3d63fad47c970ba3bc5d29ff52ce0cb605cb724ed82156c66a43a636fb63eb32`.
  Installed-wheel and scene-wheel smoke pass; two identical ten-artifact
  release stages pass complete release smoke.
- Package inventory remains 114 pure wheel entries and advances to 962 source
  entries. All three new M199 files are source-only and the wheel contains no
  tests, project records, docs, native payload, or cache content.
- Findings-first review retains exactly 15 intended paths, zero protected
  runtime, fixture, dependency, workflow, and M198 diff, 12 passing hygiene and
  M199 checks, and zero development-identity, credential-assignment, or
  machine-local-path match across 598 added lines. No actionable finding
  remains.
- The public status now records M199 as locally validated. Record-inclusive
  validation and rebuild/release rehearsal pass. At that status change, guarded
  cleanup, DCO, and hosted reconciliation remained.
- The record-inclusive separator resolves the unchanged lock, checks the exact
  graphics environment, keeps all 587 Python files static-clean, passes the
  12-test hygiene/M199 group, strict docs, both governance modes, and
  whitespace.
- Two record-state builds reproduce a 362,956-byte pure wheel at SHA-256
  `ab8875fa0a8cdc4f07ce70217ef822d9156a3efc7ee5a24999cbf6aea032d9cb`
  and a 2,323,423-byte source archive at SHA-256
  `166cef1e1d40f2ab85e42b98219d2f48f772538c37b6fe52be2321d3ec2a75e1`.
  Installed-wheel and scene-wheel smoke pass; two byte-identical ten-artifact
  release stages pass complete release smoke. Inventory remains 114/962 with
  exact source-only M199 confinement. At that rehearsal, final pre-cleanup
  validation, guarded cleanup, DCO, and hosted reconciliation remained.
- The final pre-cleanup separator keeps all 587 Python files static-clean,
  passes 12 review checks, strict docs, static and current-date governance, and
  whitespace.
- Guarded cleanup found exactly 21 top-level `.tmp/m199*` test, JUnit, profile,
  docs, distribution, and release targets. Each was proven repository-confined,
  ignored, untracked, direct-child, and top-level plus recursively reparse-free;
  each was revalidated immediately before exact removal. Zero M199 target
  remains, and no ACL was changed. At that cleanup gate, final post-cleanup
  validation, DCO, and hosted reconciliation remained.
- The final post-cleanup separator keeps all 587 Python files static-clean,
  passes 12 review checks in 0.75 seconds, builds strict docs in 3.19 seconds,
  passes both governance modes and whitespace. Pytest created no persistent
  target because these architecture tests need no temporary fixture. A first
  cleanup guard expected two regenerated targets, found one, and stopped before
  deletion; its corrected exact audit removed the sole docs target. Zero M199
  scratch remains. At that separator, DCO and hosted reconciliation remained.
- Read-only pre-commit readiness proves exact M198 HEAD/tree, exactly 15
  intended paths, zero protected runtime, fixture, package, dependency,
  workflow, and M198 diff, only local `main` and neutral M199, expected `0 99`
  divergence, configured maintainer identity, zero M199 scratch, clean
  whitespace, and clean object connectivity. A current 781-line added-content
  scan finds zero development-identity, credential-assignment, or machine-
  local-path match. That audit preceded the initial DCO object and final hosted
  reconciliation recorded below.
- Initial DCO commit `4f6b3d52ac2444ee72e97ae0a6597725f478b990`, tree
  `578de20f3d9b8f0e0c53cc69d99b37ca16271289`, has sole parent exact M198,
  exactly 15 intended paths, one matching `Signed-off-by` trailer, consistent
  configured author and committer identity, no merge, expected `0 100`
  divergence from local M99 `main`, a clean worktree, zero M199 scratch, clean
  revision whitespace, and clean object connectivity. This factual record is
  incorporated by one closeout amendment.
- A final fresh pruned fetch leaves remote `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e` and tree
  `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`; only remote `main` exists,
  divergence is `0 100`, and neither exact M198 nor the initial M199 object is
  an ancestor. Publishing M199 would expose the absent M100-M198 prerequisite
  stack, so no push, PR, hosted allocation, tag, release, or package
  publication occurs.

### M199 explicit non-scope

- Any cleanup implementation or authority; candidate enumeration; retention,
  grace, quota, lease, pin, quarantine, rollback, or recovery implementation;
  trusted-root construction; authentication; hard-link enumeration; ACL
  mutation; cross-principal fixture; independent-host execution; or Windows
  admission.
- Any new closed-stream inquiry, argument, message assertion, native-call
  trace, portability claim, subprocess fixture, runtime API, CLI command,
  adapter, dependency, native extension, compiler requirement, workflow,
  permission, hosted allocation, credential, version, release, tag, or package
  publication.

## M198 Windows hard-link alias mutator closed-stream write boundary

- **Task:** Determine the concrete parent-stream result of one `write(b"!")`
  after M197's protected failed-close, repeated-close, closed-flush, and retained
  closed-state sequence.
- **Status:** Local implementation, supported-Python regression, rendering,
  distribution, release rehearsal, findings-first review, exact scratch
  cleanup, final post-cleanup validation, initial local DCO object audit, and
  hosted publication-safety gates pass. The closeout amendment remains;
  publication is withheld because hosted `main` lacks M100-M197.
- **Base:** Fully locally validated M197 DCO commit
  `7a317300b01f6c02a959d1e3018f94aee178d603`, tree
  `96bcfc262ec0f4c73b057b01234eb354d86b655b`, sole parent exact M196.
- **Branch:**
  `release/m198-windows-alias-mutator-closed-stream-write-after-delivery-failure-boundary`;
  the redundant local M197 branch name was removed after exact M198 branch
  creation retained its object.

### M198 acceptance boundary

- Accept RFC-0181 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, M186's unchanged
  bounded-output mutator child, and M197's byte-for-byte closed-flush helper.
- Require M195's first `close()` to raise generic `OSError`, M196's second
  `close()` to return `None`, M197's `flush()` to raise generic `ValueError`,
  and the stream closed. Call `write(b"!")` exactly once, require generic
  `ValueError` without message or numeric assertion, and require the stream
  still closed.
- While the guardian remains live, require alias presence, shared identity and
  bytes, link count two, range availability through both names, and continued
  exact-name rename refusal. Close the guardian exactly, rename, and require
  complete process, stream, native, and range cleanup.
- State the result narrowly as one concrete closed-stream write disposition.
  Do not claim native-call suppression, a second native write, delivery retry,
  acknowledgement, portability, durable recovery, Windows admission, or
  cleanup authority.
- Add no runtime API, fixture, dependency, workflow, job or allocation,
  permission, release authority, version, or CI change.

### M198 development evidence so far

- Exact M197 focused baseline passed nine tests in 0.58 seconds.
- Static strict governance returned zero findings. The first dated invocation
  was denied managed-cache access before checking; its exact access-enabled
  `2026-08-30` rerun returned zero findings across three objectives, seven
  requirements, and four work items.
- Current Python buffered-I/O and CPython implementation, Microsoft
  `WriteFile`, GitHub least-privilege/billing, NIST SSDF, and SLSA 1.2 sources
  support one bounded closed-write observation, its strict non-claims, and no
  hosted allocation.
- Neutral M198 was created from exact M197, and the redundant local M197 branch
  name was removed without deleting its retained object.
- The first live M198 probe passed one test in 0.51 seconds. The intentional
  architecture-red phase passed six behavior and containment checks and failed
  only the three absent RFC, security, and public-registration contracts.
- RFC-0181, the security record, and eight public registrations now describe
  the selected boundary. Ruff requested only mechanical formatting; both new
  Python files are now format-, lint-, and strict-Pyright clean, and all nine
  focused checks pass.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 complete suites each pass 4,080
  tests with 17 skips. The exact 100-file Windows boundary passes 387 tests
  with one established skip, and 20 independent M198 live invocations pass.
- Ten real-wgpu tests, fresh two- and three-workload M7 profiles, eight profile-
  schema tests, Null and wgpu Clockwork Arena, and Agent World Builder pass
  with their established deterministic identities.
- Two builds are byte-identical; installed-wheel and scene-wheel smoke pass;
  two identical ten-artifact release stages pass complete release smoke. The
  wheel has 114 pure entries, the source archive has 959 entries, and all four
  M198 evidence files are source-only.
- Findings-first review retains exactly 16 intended paths, zero protected-
  surface diff, 14 passing hygiene and M198 checks, zero forbidden wheel
  payload, and zero development-identity, credential-assignment, or machine-
  local-path match across 892 added lines. No actionable finding remains.
- The public status now records M198 as locally validated. Record-inclusive
  static, documentation, governance, distribution, release, cleanup, and
  hosted reconciliation gates pass. At that separator, final post-cleanup
  validation and the DCO commit remained.
- The record-inclusive separator resolves the unchanged lock, keeps all 586
  Python files static-clean, passes 14 review checks, strict docs, static and
  current-date strict governance, and whitespace.
- Two record-state builds reproduce a 362,840-byte pure wheel at SHA-256
  `811a9fb8b83e68fe8b5d974dcb7a1936a1f8f51e7969bff06fe822a44834b142`
  and a 2,309,053-byte source archive at SHA-256
  `19598ff4c00590f04316ede1e277e845a16e5d0be33b7bdc25a901a839456e73`.
  Installed-wheel and scene-wheel smoke pass; two byte-identical ten-artifact
  release stages pass complete release smoke. Inventory remains 114/959 with
  exact source-only confinement and zero forbidden wheel entry. Final
  pre-cleanup validation, guarded cleanup, and hosted reconciliation now pass;
  at that rehearsal, final post-cleanup validation and the DCO commit remained.
- The final pre-cleanup separator keeps all 586 Python files static-clean,
  passes 14 review checks, strict docs, static and current-date strict
  governance, and whitespace. Guarded cleanup and hosted reconciliation now
  pass; at that separator, final post-cleanup validation and the DCO commit
  remained.
- Guarded cleanup found 52 exact top-level `.tmp/m198*` targets. All were
  repository-confined, ignored, untracked, and top-level non-reparse. Forty-one
  recursively auditable, reparse-free targets were removed first. An exact
  complementary access-enabled read-only audit then proved the remaining 11
  pytest roots recursively reparse-free; exact guarded removal revalidated and
  removed them. Zero `.tmp/m198*` target remains, and no ACL was changed.
- Read-only pre-commit readiness proves exact M197 HEAD and tree, exactly 16
  intended paths, zero protected runtime, package, fixture, CI, and M197 diff,
  only local `main` and neutral M198, expected `0 98` divergence, configured
  maintainer identity, clean whitespace, and clean object connectivity. That
  audit preceded the completed complementary cleanup, final post-cleanup gate,
  and initial DCO object.
- A fresh pruned fetch, local hosted-ref and ancestry inspection, authenticated
  public-repository/default-branch query, and recent PR history leave remote
  `main` at exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`
  with tree `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`, prove M196 and
  M197 absent, show only remote `main`, and report PR #251 as latest. Publishing
  M198 would expose the absent M100-M197 stack, so no push, PR, hosted
  allocation, tag, release, or package publication occurs.
- The post-hosted-readiness separator keeps all 586 Python files format-clean,
  returns zero Ruff and strict-Pyright findings, builds strict docs, returns
  zero static and dated governance findings, and passes whitespace. Its exact
  generated docs target was recursively audited and removed. The subsequent
  complementary audit and guarded delete completed the remaining scratch
  cleanup without changing ACLs.
- The final post-cleanup separator keeps all 586 Python files format-clean,
  returns zero Ruff and strict-Pyright findings, passes the exact 14-test
  hygiene/M198 group in 0.97 seconds, builds strict docs in 3.19 seconds,
  returns zero static and corrected current-date strict governance findings,
  and passes whitespace. Its exact test and docs targets were guarded, removed,
  and leave zero `.tmp/m198*` target.
- Initial DCO commit `f40e17844c861e408d7ef53314659f93b3f04bb1`, tree
  `c034e90791840f2efc822ed947bcd0e5d7cf77be`, has sole parent exact M197,
  exactly 16 intended paths, one matching `Signed-off-by` trailer, consistent
  configured author and committer identity, no merge, expected `0 99`
  divergence from local M99 `main`, a clean worktree, zero M198 scratch, clean
  revision whitespace, and clean object connectivity. This factual record is
  incorporated by one closeout amendment.
- A final fresh pruned fetch leaves remote `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e` and tree
  `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`; only remote `main` exists,
  divergence is `0 99`, and neither exact M197 nor the initial M198 object is
  an ancestor. Publication remains withheld with zero hosted allocation.

### M198 explicit non-scope

- Any closed-stream operation other than one `write(b"!")`; other arguments;
  exact exception text; native-call tracing; pre-settlement or concurrent late
  commands; arbitrary buffered, partial, repeated, or larger input;
  duplicated or inherited writers; cross-principal or unrelated-process
  behavior; hostile simultaneous racing; authenticated framing or
  acknowledgement; crash or power loss; durable intent, rollback,
  reconciliation, typed recovery receipts; ReFS, SMB, or other-host evidence;
  Windows admission; and cleanup authority.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M197 Windows hard-link alias mutator closed-stream flush boundary

- **Task:** Determine the concrete parent-stream result of one `flush()` after
  M196's failed first close, repeated-close no-op, and retained closed state.
- **Status:** Local implementation and validation complete through authority,
  direction, exact M196 baseline, governance, branch containment, test-first
  implementation, supported-Python regression, concentrated/repeated Windows
  behavior, graphics/product checks, reproducible distribution/release,
  findings-first review, final separators, guarded cleanup, and DCO audit.
  Hosted publication is withheld because remote `main` remains at M99 and does
  not contain M196.
- **Base:** Fully locally validated M196 DCO commit
  `b4a7623541767c191750cc404781e11f370be133`, tree
  `49257842225afc0a7d304e011a9e601a918c19de`, sole parent exact M195.
- **Branch:**
  `release/m197-windows-alias-mutator-buffered-flush-after-close-delivery-failure-boundary`;
  the redundant local M196 branch name was removed after exact M197 branch
  creation retained its object.

### M197 acceptance boundary

- Accept RFC-0180 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, M186's unchanged
  bounded-output mutator child, and M196's byte-for-byte repeated-close helper.
- Require M195's first `close()` to raise generic `OSError`, M196's second
  `close()` to return `None`, and the stream closed. Call `flush()` exactly
  once, require generic `ValueError` without message or numeric assertion, and
  require the stream still closed.
- While the guardian remains live, require alias presence, shared identity and
  bytes, link count two, range availability through both names, and continued
  exact-name rename refusal. Close the guardian exactly, rename, and require
  complete process/stream/native/range cleanup.
- State the result narrowly as one concrete closed-stream flush disposition.
  Do not claim a second native write, delivery retry, acknowledgement,
  portability, durable recovery, Windows admission, or cleanup authority.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, version, or CI change.

### M197 development evidence so far

- Exact M196 focused baseline passed nine tests in 2.35 seconds.
- Static strict governance returned zero findings. The first dated invocation
  was denied managed-cache access before checking; its exact access-enabled
  `2026-08-30` rerun returned zero findings across three objectives, seven
  requirements, and four work items.
- Current Python buffered-I/O and CPython implementation, Microsoft
  `WriteFile`, GitHub least-privilege/billing, NIST SSDF, and SLSA 1.2 sources
  support one bounded closed-flush observation, its strict non-claims, and no
  hosted allocation.
- Neutral M197 was created from exact M196, and the redundant local M196 branch
  name was removed without deleting its retained object.
- The first live M197 probe passed one test in 0.48 seconds. The intentional
  architecture-red phase passed six behavior/containment checks and failed
  only the three absent RFC/security/public-registration contracts.
- RFC-0180, the security record, and eight public registrations now describe
  the selected boundary. Ruff requested only mechanical formatting; both new
  Python files then became format-, lint-, and strict-Pyright clean, and all
  nine focused checks passed.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 complete suites each pass 4,071
  tests with 17 skips. The exact 98-file Windows boundary passes 378 tests with
  one established skip, and 20 independent M197 live invocations pass.
- Ten real-wgpu tests, fresh two-/three-workload M7 profiles, eight profile-
  schema tests, null/wgpu Clockwork Arena, and Agent World Builder pass with
  their established deterministic identities.
- Two builds are byte-identical; installed-wheel and scene-wheel smoke pass;
  two identical ten-artifact release stages pass complete release smoke. The
  wheel has 114 pure entries, the source archive has 955 entries, and all four
  M197 evidence files are source-only.
- Findings-first review retains exactly 16 intended paths, zero protected-
  surface diff, 14 passing hygiene/M197 checks, zero forbidden wheel payload,
  and zero development-identity, credential-assignment, or machine-local-path
  match across 874 added lines. No actionable finding remains.
- The record-inclusive separator resolves the unchanged lock, keeps all 584
  Python files static-clean, passes 14 review checks, strict docs, static and
  current-date strict governance, and whitespace. Record-inclusive artifacts,
  guarded cleanup, DCO, and hosted reconciliation remain.
- Two record-state builds reproduce a 362,790-byte pure wheel at SHA-256
  `63f4574a3ceda02023dc4580ab9da463ce457964296e59bcdd03a7ccca97a935`
  and a 2,303,731-byte source archive at SHA-256
  `e7c59a35a3dc05cd0434672ed5746782ab3061f8f6e0f2cc6a9e21adb1c453a5`.
  Installed-wheel and scene-wheel smoke pass; two byte-identical ten-artifact
  release stages pass complete release smoke. Inventory remains 114/955 with
  exact source-only confinement and zero forbidden wheel entry.
- The final pre-cleanup separator keeps all 584 Python files static-clean,
  passes 14 review checks, strict docs, current-date strict governance, and
  whitespace. Guarded cleanup, DCO, and hosted reconciliation remain.
- Guarded cleanup proved all 49 exact `.tmp/m197*` targets repository-
  confined, ignored, untracked, and top-level plus recursively reparse-free,
  removed them exactly, and confirmed zero remains. Final post-cleanup
  separator, DCO, and hosted reconciliation remain.
- Final post-cleanup validation keeps both M197 Python files static-clean,
  passes all 14 review checks, strict docs, current-date strict governance, and
  whitespace. The two exact regenerated review/docs directories were
  revalidated, removed, and zero M197 scratch remains. DCO and hosted-
  publication reconciliation are the remaining closeout gates.
- Pre-commit audit proves exact M196 HEAD/tree, exactly 16 intended paths,
  zero protected-surface diff, only local `main` and neutral M197, expected
  `0 97` divergence, configured maintainer identity, zero M197 scratch, clean
  whitespace, and clean object connectivity.
- Initial DCO commit `18615c8d17ad51452a6ca7d73c140fe2be2f7fc6`, tree
  `610aa576ad204a3dc44264641b7c7281cc6f5a59`, has sole parent exact M196,
  exactly 16 intended paths, one matching sign-off, consistent configured
  author/committer identity, no merge, expected `0 98` divergence, a clean
  worktree, zero M197 scratch, clean whitespace, and clean object connectivity.
  This factual record is folded into one closeout amendment.
- A fresh pruned fetch and authenticated hosted audit leave `origin/main` at
  exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, prove M196 absent and
  not an ancestor, show only remote `main`, and report PR #251 as latest.
  Publishing M197 would expose the absent M100-M196 stack, so no push, PR,
  hosted allocation, tag, release, or package publication occurs.

### M197 explicit non-scope

- Any closed-stream operation other than one `flush()`; exact exception text;
  native-call tracing; pre-settlement or concurrent late commands; arbitrary
  buffered, partial, repeated, or larger input; duplicated/inherited writers;
  cross-principal or unrelated-process behavior; hostile simultaneous racing;
  authenticated framing/acknowledgement; crash/power loss; durable intent,
  rollback, reconciliation, typed recovery receipts; ReFS/SMB/other-host
  evidence; Windows admission; and cleanup authority.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M196 Windows hard-link alias mutator repeated buffered-close boundary

- **Task:** Determine whether a second parent-side `close()` is a no-op after
  M195's first buffered close reports delivery failure but leaves the stream
  closed.
- **Status:** Local implementation and validation complete through authority,
  direction, exact M195 baseline, governance, branch containment, test-first
  implementation, supported-Python regression, concentrated/repeated Windows
  behavior, graphics/product checks, reproducible distribution/release,
  findings-first review, final separators, guarded cleanup, and DCO audit.
  Hosted publication is withheld because remote `main` remains at M99 and does
  not contain M195.
- **Base:** Fully locally validated M195 DCO commit
  `496e47d534bea27f387be15702504a6bb75efdb9`, tree
  `53c62d76e6f79a7fa30bfdb1ec03e05e3909f264`, sole parent exact M194.
- **Branch:**
  `release/m196-windows-alias-mutator-repeated-buffered-close-after-delivery-failure-boundary`;
  the redundant local M195 branch name was removed after exact M196 branch
  creation retained its object.

### M196 acceptance boundary

- Accept RFC-0179 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, M186's unchanged
  bounded-output mutator child, and M195's byte-for-byte first-close helper.
- Require M195's first `close()` to raise generic `OSError` and leave the
  stream closed. Call `close()` exactly once more, require it to return `None`
  without another exception, and require the stream still closed.
- While the guardian remains live, require alias presence, shared identity and
  bytes, link count two, range availability through both names, and continued
  exact-name rename refusal. Close the guardian exactly, rename, and require
  complete process/stream/native/range cleanup.
- State the result narrowly as repeated-close disposition evidence for one
  fixed stream and fixture. Do not claim delivery retry, acknowledgement,
  portable exception behavior, durable recovery, Windows admission, or
  cleanup authority.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, version, or CI change.

### M196 development evidence so far

- Exact M195 focused baseline passed nine tests.
- Static strict governance passed. The first dated strict governance launch
  was denied managed-cache access before checking; its exact access-enabled
  rerun returned zero findings across three objectives, seven requirements,
  and four work items.
- Current Python buffered-I/O, Microsoft `WriteFile`, GitHub least-privilege
  and billing, NIST SSDF, and SLSA 1.2 sources support the bounded repeated-
  close observation and no hosted allocation.
- Neutral M196 was created from exact M195, and the redundant local M195 branch
  name was removed without deleting its retained object.
- The first live M196 probe passed. The intentional architecture red passed
  five behavior/containment guards and failed only the three absent
  RFC/security/public-registration contracts.
- RFC-0179, the security record, and eight public registrations now describe
  the selected boundary. Ruff requested only mechanical formatting; both new
  Python files then became format-, lint-, and strict-Pyright clean, and all
  nine focused checks passed.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 complete suites each pass 4,062
  tests with 17 skips. The exact 96-file Windows boundary passes 369 tests with
  one established skip, and 20 independent M196 live invocations pass.
- Ten real-wgpu tests, fresh two-/three-workload M7 profiles, eight profile-
  schema tests, null/wgpu Clockwork Arena, and Agent World Builder pass with
  their established deterministic identities.
- Two builds are byte-identical; installed-wheel and scene-wheel smoke pass;
  two identical ten-artifact release stages pass complete release smoke. The
  wheel retains 114 pure entries, the source archive has 951 entries, and all
  four M196 evidence files are source-only.
- The record-inclusive separator remains clean. Its two fresh builds reproduce
  the unchanged 362,709-byte wheel at SHA-256
  `fac8fd367e910ebe7b121ed8d74a2c43211396bda41285ded887e8f89211c737`
  and a 2,296,404-byte source archive at SHA-256
  `5d823da03301da046190dd9e1df940c12a01460510c9de81207ceebf61502ad6`.
  Installed-wheel and scene-wheel smoke pass; the corrected exact comparator
  proves two byte-identical ten-artifact release stages, and both complete
  release smokes pass. Inventory remains 114/951 with exact source-only
  confinement and zero forbidden wheel entry.
- The final pre-cleanup separator passes whole-tree formatting, Ruff, strict
  Pyright, 14 hygiene/M196 checks, strict docs, current-date strict governance,
  and whitespace. A first governance invocation used the wrong evidence root
  and a first dated invocation was cache-denied; corrected exact invocations
  return zero findings.
- Guarded scratch cleanup's first recursive audit was sandbox-denied before
  deletion. Its access-enabled rerun proved all 48 exact `.tmp/m196*` targets
  repository-confined, ignored, untracked, and top-level plus recursively
  reparse-free, removed them exactly, and confirmed zero remains.
- Final post-cleanup validation keeps both M196 Python files static-clean,
  passes all 14 review checks, strict docs, current-date strict governance,
  and whitespace. The two exact regenerated review/docs directories were
  revalidated, removed, and zero M196 scratch remains. DCO and hosted-
  publication reconciliation are the remaining closeout gates.
- Pre-commit audit proves exact M195 HEAD/tree, exactly 16 intended paths,
  zero protected-surface diff, only local `main` and neutral M196, expected
  `0 96` divergence, configured maintainer identity, zero M196 scratch, clean
  whitespace, and clean object connectivity.
- Initial DCO commit `0b1a57729c3b8e038b4365cc6769381e310af551`, tree
  `b7c2064ebde0e34c8a425228d6c40dba28c313c4`, has sole parent exact M195,
  exactly 16 intended paths, one matching sign-off, consistent configured
  author/committer identity, no merge, expected `0 97` divergence, a clean
  worktree, zero M196 scratch, clean whitespace, and clean object connectivity.
  This factual record is folded into one closeout amendment.
- A fresh pruned fetch and authenticated hosted audit leave `origin/main` at
  exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, prove M195 absent and
  not an ancestor, show only remote `main`, and report PR #251 as latest.
  Publishing M196 would expose the absent M100-M195 stack, so no push, PR,
  hosted allocation, tag, release, or package publication occurs.
- Findings-first review retains exactly 16 intended paths, zero protected-
  surface diff, 14 passing hygiene/M196 checks, zero forbidden wheel payload,
  and zero development-identity, credential-assignment, or machine-local-path
  match across 875 added lines. No actionable finding remains.

### M196 explicit non-scope

- Any closed-stream operation other than repeated `close()`; pre-settlement or
  concurrent late commands; arbitrary buffered, partial, repeated, or larger
  input; exact exception subtype/code; duplicated/inherited writers; cross-
  principal or unrelated-process behavior; hostile simultaneous racing;
  authenticated framing/acknowledgement; crash/power loss; durable intent,
  rollback, reconciliation, typed recovery receipts; ReFS/SMB/other-host
  evidence; Windows admission; and cleanup authority.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M195 Windows hard-link alias mutator buffered-close delivery-failure boundary

- **Task:** Determine what the parent-side buffered writer reports when direct
  `close()` is the first delivery attempt for M194's accepted late byte.
- **Status:** Local implementation and validation complete through direction,
  test-first behavior, supported-Python regression, repeated Windows behavior,
  graphics/examples, reproducible distribution/release rehearsal, governance,
  findings-first review, final separators, guarded cleanup, and DCO audit.
  Hosted publication is withheld because remote `main` remains at M99 and does
  not contain M194.
- **Base:** Fully locally validated M194 DCO commit
  `4b1314d58095a93963df2ded846b7b2bf77ed27e`, tree
  `131de175d73ade7ac9fceb926984ccefe284d0d4`, sole parent exact M193.
- **Branch:**
  `release/m195-windows-alias-mutator-buffered-close-delivery-failure-boundary`;
  the redundant local M194 branch name was removed after exact M195 branch
  creation retained its object.

### M195 acceptance boundary

- Accept RFC-0178 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, and M186's
  unchanged bounded-output mutator child.
- Reproduce M194 through exact child exit 5, terminal output, and one-byte late
  buffer acceptance. Perform no late `flush()`. Require direct `close()` to
  raise generic `OSError` and require the stream closed afterward, without
  freezing a subtype or numeric code.
- While the guardian remains live, require alias presence, shared identity and
  bytes, link count two, range availability through both names, and continued
  exact-name rename refusal. Close the guardian exactly, rename, and require
  complete process/stream/native/range cleanup.
- State the result narrowly as close-triggered delivery evidence for one fixed
  late byte and fixture. Do not claim arbitrary buffering, portable exception
  translation, acknowledgement, durable recovery, Windows admission, or
  cleanup authority.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, version, or CI change.

### M195 development evidence so far

- Exact M194 focused baseline passed nine tests. Static and dated strict
  governance each returned zero findings across three objectives, seven
  requirements, and four work items.
- Current Microsoft `WriteFile`, Python buffered-I/O, automation-safety, GitHub
  least-privilege and billing, NIST SSDF, and SLSA 1.2 sources support the
  bounded close observation and no hosted allocation.
- The first live M195 probe passed. The initial contract-red run passed six
  checks and failed only the absent RFC/security/public-registration
  contracts. After RFC-0178 and the security record, only registration remained
  red. After eight registrations, all nine architecture/live checks passed.
- Ruff requested one mechanical architecture-test reformat. Both new Python
  files are now format-, lint-, and strict-Pyright clean; all nine focused
  checks pass in 0.48 seconds.
- An initial 3.12 full run exposed one project-record reference that violated
  the established tool-neutral metadata contract: 1 failed and 1,343 passed
  before the stop. Neutral wording corrected only that record; the exact
  five-test hygiene contract then passed.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 complete suites each pass 4,053
  tests with 17 skips. The exact 94-file Windows boundary passes 360 tests with
  one established skip, and 20 independent M195 live invocations pass.
- Ten real-wgpu tests, fresh two-/three-workload M7 profiles, eight profile-
  schema tests, null/wgpu Clockwork Arena, and Agent World Builder pass with
  their established deterministic identities.
- Two builds are byte-identical; installed-wheel smoke passes; two identical
  ten-artifact release stages pass complete release smoke. Inventory retains a
  114-entry pure wheel and a 947-entry source archive, with all four M195 files
  source-only.
- Findings-first review retains exactly 16 intended paths, zero protected-
  surface diff, 14 passing hygiene/M195 checks, zero forbidden wheel payload,
  and zero credential-assignment or machine-local-path match across 931 added
  lines. No actionable correctness, security, architecture, documentation,
  compatibility, package-boundary, allocation, or public-hygiene finding
  remains.
- The first record-inclusive review command counted only tracked diffs and
  stopped at 12 before testing. Its corrected tracked-plus-untracked inventory
  proved the exact 16-path scope. Whole-tree static checks, strict docs, both
  governance modes, and whitespace then passed from the recorded state.
- Two record-inclusive builds preserve the exact wheel bytes/hash and reproduce
  identical 2,288,447-byte source archives at SHA-256
  `08224ecda9b1b11a6a8f094d6b8ab2b5d73fabcca86fb9bb74b30aa222a8d057`.
  Installed-wheel smoke and both identical ten-artifact release stages pass.
- The final record-state separator keeps all 580 Python files static-clean;
  the 14-test review group, strict docs, dated governance, and whitespace pass.
  Two final 2,288,781-byte source archives reproduce at SHA-256
  `0819cfe055960862800ce7fbe2ec5ae5f5c2bbf991a10d45290f51f69c01d034`;
  the wheel is unchanged, installed-wheel smoke passes, and both identical
  ten-artifact release stages pass. Recording cleanup/object facts later changes
  only the source archive.
- Guarded cleanup verified all 59 exact M195 test, environment, profile,
  distribution, release, and generated-docs targets as repository-confined,
  ignored, untracked, and top-level plus recursively reparse-free before
  removing them. Zero M195 target remains; older milestone scratch and the
  managed environment were not selected.
- After recording cleanup, both Python files remained format-, Ruff-, and strict-
  Pyright clean; the 14-test review group passed in 1.14 seconds; strict docs,
  dated governance, and whitespace passed. The two regenerated test/docs targets
  were revalidated and removed; zero M195 scratch remains.
- The first pre-commit audit used PowerShell-sensitive `HEAD^{tree}` syntax and
  stopped on the misparsed tree query. Its corrected `git show --format=%T`
  rerun retains exactly 16 intended paths, only local `main` and neutral M195,
  exact M194 base/tree, expected `0 95` divergence, zero protected-surface
  diff, zero scratch, configured maintainer identity, clean whitespace, and
  clean repository object connectivity.
- Initial signed DCO commit `31563f13616403d75e621bf70da2d9b12e93416a`,
  tree `987202c629abb8c7f1eba41b53876b223cc19a1a`, has sole parent exact
  M194, exactly 16 paths, one matching sign-off, consistent configured
  identity, expected `0 96` divergence, a clean worktree, zero scratch, clean
  whitespace, and clean connectivity. The first object-audit whitespace query
  contained an invalid Unicode revision separator and stopped; its corrected
  rerun passed. This closeout record is incorporated by amendment.
- A fresh pruned fetch and direct hosted/PR inspection leave remote `main` at
  exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, tree
  `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`, with only remote `main`, M194
  absent from its ancestry, and PR #251 still latest. Publishing M195 would
  expose the absent M100-M194 stack, so no push, PR, or hosted allocation is
  created.

### M195 explicit non-scope

- Pre-settlement or concurrent late commands; arbitrary buffered, partial,
  repeated, or larger input; exact exception subtype/code; duplicated/inherited
  writers; cross-principal or unrelated-process behavior; hostile simultaneous
  racing; authenticated framing/acknowledgement; crash/power loss; durable
  intent, rollback, reconciliation, typed recovery receipts; ReFS/SMB/other-
  host evidence; Windows admission; and cleanup authority.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M194 Windows hard-link alias mutator late valid-close delivery-failure boundary

- **Task:** Determine what the parent-side buffered writer reports when one
  late valid `!` byte is attempted after M193's exact invalid settlement.
- **Status:** Local implementation and validation complete. Direction, test-first
  implementation, accepted RFC/security boundary, public registration,
  supported-Python regression, repeated Windows behavior, graphics/examples,
  reproducible distribution/release rehearsal, governance, and findings-first
  review, record-inclusive rebuild, and source/governance separators pass.
  Guarded scratch cleanup, the final pre-commit separator, exact scope/history
  audit, and DCO object audit pass. Hosted publication is withheld because
  remote `main` remains at M99 and does not contain M193.
- **Base:** Fully locally validated M193 DCO commit
  `71e5ae471fc6e63b26a8e31e40389e3342aa8491`, tree
  `3aaef65cd46db0bf4ae16426da56d50cab9044e3`, sole parent exact M192.
- **Branch:** `release/m194-windows-alias-mutator-late-close-delivery-failure-boundary`;
  the redundant local M193 branch name was removed after exact M194 branch
  creation retained its object.

### M194 acceptance boundary

- Accept RFC-0177 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, and M186's
  unchanged bounded-output mutator child.
- Require initial shared identity/link count two, guardian `ready`, exact-name
  rename error 32, child-owned deletion/recreation, and exact `deleted` then
  `recreated` events.
- Reproduce M193's exact accepted/flushed `?!`, parent-writer openness, bounded
  exit 5, no `closed` event, stdout EOF, and empty stderr. Only after the child
  has settled, write one late valid `!` byte, require the buffer to accept one
  byte, and require generic `OSError` on `flush()` without freezing a subtype
  or numeric code. Close the writer best-effort and require it closed.
- While the guardian remains live, require alias presence, shared identity and
  bytes, link count two, range availability through both names, and continued
  exact-name rename refusal. Close the guardian exactly, rename, and require
  complete process/stream/native/range cleanup.
- State the result narrowly as buffered acceptance-versus-delivery evidence for
  one fixed late byte and fixture. Do not claim arbitrary buffering, portable
  exception translation, acknowledgement, durable recovery, Windows admission,
  or cleanup authority.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, version, or CI change.

### M194 development evidence so far

- The exact M193 focused baseline passed nine tests. Static and dated strict
  governance each returned zero findings across three objectives, seven
  requirements, and four work items.
- Current Microsoft pipe/`WriteFile` documentation, Python buffered-I/O,
  subprocess and exception contracts, GitHub Actions billing guidance, NIST
  SSDF, and SLSA 1.2 support the bounded observation and no hosted allocation.
- A first disposable direct-write probe had an inline diagnostic syntax error
  and produced no behavior evidence. Its corrected run observed an open writer
  followed by generic `OSError` after peer exit. A separate buffered probe
  observed one-byte local acceptance, generic flush and close errors, and final
  stream closure. M194 deliberately asserts no exact subtype or code.
- The live M194 probe passed first execution. The first architecture red found
  the intended three absent decision/registration contracts plus one incorrect
  writer-open count. After correcting only that guard, the red phase failed
  only the three intended contracts. After RFC/security records, only public
  registration remained red; after registration, all nine checks passed.
- Ruff requested one mechanical architecture-test reformat. Both new Python
  files then passed focused formatting, Ruff, and strict Pyright; all nine
  focused checks pass in 0.44 seconds.
- The unchanged 46-package lock and 45-package graphics environment pass.
  Formatting covers 578 Python files; Ruff, strict Pyright, strict docs,
  whitespace, and static plus dated strict governance pass. The first dated
  governance closeout attempt was denied access to the managed uv cache before
  checking; its access-enabled rerun returned zero findings.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 each pass 4,044 tests with 17
  skips. The 92-file M149-M194 Windows boundary passes 351 tests with one
  established skip, and 20 independent M194 live invocations pass.
- Ten real-wgpu tests, fresh two-/three-workload M7 profiles, eight profile
  schema tests, null/wgpu Clockwork Arena, and Agent World Builder pass with
  their established deterministic hashes.
- Two builds are byte-identical; installed-wheel smoke passes; two identical
  ten-artifact release stages pass complete release smoke. Inventory retains a
  114-entry pure wheel and a 943-entry source archive, with all four M194 files
  source-only.
- Findings-first review retains exactly 16 intended paths, zero protected-
  surface diff, 14 passing hygiene/M194 checks, zero forbidden wheel payload,
  and zero credential-assignment or machine-local-path match across 926 added
  lines. No actionable correctness, security, architecture, documentation,
  compatibility, package-boundary, allocation, or public-hygiene finding
  remains.
- The record-inclusive final pair preserves the exact wheel bytes/hash,
  reproduces identical 2,282,185-byte source archives at SHA-256
  `45d7cc9f29ecf144eb35841215daba45ba1e646781f0bee26dcf5b44c2d2cfec`,
  passes installed-wheel smoke, and produces two identical ten-artifact stages
  that both pass complete release smoke.
- Guarded cleanup verified all 46 exact M194 test, profile, distribution,
  release, and generated-docs targets as repository-confined, ignored,
  untracked, and reparse-free before removing all 46; zero target remains.
- After the cleanup record, both Python files remained format-, Ruff-, and
  strict-Pyright clean; the 14-test hygiene/M194 group passed in 0.76 seconds;
  strict docs, dated governance, and whitespace passed.
- The pre-commit audit retains exactly 16 intended paths, only local `main` and
  neutral M194, exact M193 base/tree, expected `0 94` divergence, zero
  protected-surface diff, zero scratch, configured maintainer identity, clean
  whitespace, and clean repository object connectivity.
- Initial DCO commit `6c667470a8f1cf64c1f4acfc3d4d6eee5e2b407e`, tree
  `fc777bc94403433a7b6baded8f6226d74a3c0e32`, has sole parent exact M193,
  exactly 16 paths, one matching sign-off, consistent configured identity,
  expected `0 95` divergence, a clean worktree, zero scratch, and clean object
  connectivity. This closeout record is incorporated by amendment.
- A fresh pruned fetch and direct hosted/PR inspection leave remote `main` at
  exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, tree
  `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`, with only remote `main`, M193
  absent from its ancestry, and PR #251 still latest. Publishing M194 would
  expose the absent M100-M193 stack, so no push, PR, or hosted allocation is
  created.

### M194 explicit non-scope

- Pre-settlement or concurrent late commands; arbitrary buffered, partial,
  repeated, or larger input; exact exception subtype/code; duplicated/inherited
  writers; cross-principal or unrelated-process behavior; hostile simultaneous
  racing; authenticated framing/acknowledgement; crash/power loss; durable
  intent, rollback, reconciliation, typed recovery receipts; ReFS/SMB/other-
  host evidence; Windows admission; and cleanup authority.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M193 Windows hard-link alias mutator open-writer invalid-prefix settlement boundary

- **Task:** Determine whether M186's unchanged mutator child settles on fixed
  `?!` after exact `recreated` while the parent control writer remains open.
- **Status:** Locally complete through direction, test-first implementation,
  accepted RFC/security boundary, public registration, supported-Python
  regression, concentrated and repeated Windows behavior, graphics/product
  checks, distribution/release rehearsal, governance, findings-first review,
  separators, cleanup, DCO, and fresh hosted reconciliation. Publication is
  withheld because hosted `main` lacks M100-M192.
- **Base:** Fully locally validated M192 DCO commit
  `3b9c7e43c3deac47b040c837844945e07514ba69`, tree
  `7edd933e7bd4da487d9f2079a5e86b408b3fd161`, sole parent exact M191.
- **Branch:**
  `release/m193-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate-boundary`;
  the redundant local M192 branch name was removed after exact M193 branch
  creation retained its object.

### M193 acceptance boundary

- Accept RFC-0176 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, and M186's
  unchanged bounded-output mutator child.
- Require initial shared identity/link count two, guardian `ready`, exact-name
  rename error 32, child-owned deletion/recreation, and exact `deleted` then
  `recreated` events.
- Write fixed `?!` exactly once, require both bytes accepted and flushed, keep
  the parent writer open across a bounded wait, and require exit 5 while the
  writer is still open, no `closed` event, stdout EOF, and empty stderr. Close
  the parent writer only after those observations.
- While the guardian remains live, require alias presence, shared identity and
  bytes, link count two, range availability through both names, and continued
  exact-name rename refusal. Close the guardian exactly, rename, and require
  complete process/stream/native/range cleanup.
- State the result narrowly as open-writer settlement evidence for one fixed
  sequence and bounded-output fixture. Do not claim arbitrary malformed-input
  or unbounded-output handling, general framing, durable recovery, Windows
  admission, or cleanup authority.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, version, or CI change.

### M193 development evidence so far

- The exact M192 focused baseline passed nine tests. Static and dated strict
  governance each returned zero findings across three objectives, seven
  requirements, and four work items.
- Current Microsoft pipe documentation, Python buffered-I/O and subprocess
  contracts, GitHub Actions billing guidance, NIST SSDF, and SLSA 1.2 support
  the bounded observation and no additional hosted allocation.
- The live probe passed its first execution. The intended architecture red
  passed behavior and non-documentation guards while identifying three absent
  decision/registration records. After both decisions, only public
  registration remained red; after registration, all nine checks passed.
- Ruff requested one mechanical architecture-test reformat. Both new Python
  files then passed focused Ruff and strict Pyright; all nine focused checks
  pass in 0.45 seconds.
- Exact CPython 3.12.13, isolated 3.13.13, and isolated 3.14.5 each pass 4,035
  tests with 17 skips in 254.72, 257.68, and 265.02 seconds. The 45 M149-M193
  architecture modules plus all 45 Windows cleanup integrations pass 342
  tests with one established skip. Twenty live repetitions pass in 0.35-0.42
  seconds each.
- Ten real-wgpu tests pass. Fresh two- and three-workload profiles validate;
  all eight profile-schema tests pass. Clockwork Arena and Agent World Builder
  reproduce established state, capture, replay, draw, sprite, match, and batch
  identities.
- The unchanged 46-package lock and exact 45-package graphics environment
  resolve. All 576 Python files are format-clean; Ruff, strict Pyright, strict
  docs, static and dated governance, and whitespace pass.
- Two builds reproduce a 362,492-byte pure wheel at SHA-256
  `75b9bfc69b4d54ee00e48784ed96e9c9a03b456bf165a7fca8b57c107ea7bd48`
  and a 2,271,984-byte source archive at SHA-256
  `e461731453e04cf061e4c119d5ec8baf7f3d3a92b80b6ecb970f892c62ecd710`.
  Installed-wheel smoke and two identical ten-artifact release smokes pass.
  Inventory is 114 wheel/939 source entries; all M193 evidence is source-only.
- Findings-first review confirms exactly 16 intended paths, zero protected-
  surface diff, 14 passing hygiene/architecture/live checks, no forbidden
  wheel payload, and zero retired-identity, credential-assignment, or local-
  path match across 907 added lines. No actionable finding remains before the
  record-state gates.
- The first record-state review found one retired identity term in three
  evidence summaries while all other checks passed. Neutral wording corrected
  those summaries; all 576 Python files then remained static-clean, the exact
  14-test review group passed, strict docs and whitespace passed, and dated
  governance returned zero findings.
- Two final builds reproduce the unchanged 362,492-byte wheel and identical
  2,273,075-byte source archives at SHA-256
  `4f21e5a177cd7447ba3c7a2252224e28819845027798a493890bb012d780a77b`.
  Complete installed-wheel smoke passes; two final ten-artifact release stages
  are byte-identical and both complete release smokes pass.
- The post-record separator keeps both Python files static-clean; 14 exact
  review tests, strict docs, dated governance, and whitespace pass.
- The first scratch audit was denied access to pytest-owned directories before
  deletion. Its exact access-enabled rerun verified 46 M193 targets as
  repository-confined, ignored, and top-level plus recursively reparse-free;
  guarded removal completed with zero M193 target remaining.
- Initial DCO commit `2b3cf8273d2aa5bed0fa888ae7ea02e7419b9bac`, tree
  `0b3ae83543db3bacbe55604d11ee0e96dce6847a`, has sole parent exact M192,
  exactly 16 intended paths, one matching sign-off, truthful configured
  author/committer identity, no merge, expected `0 94` divergence, a clean
  worktree, and zero M193 scratch. This factual record is folded into the
  closeout amendment; the successor milestone will record the amended hash
  without self-reference.

### M193 publication boundary

- Pre-publication amended DCO object
  `607bf9802cbf1abca6be90f892db536712b0ba57`, tree
  `d25cdd2fc1343de8e7a16a30f17dfcca580c56fe`, has sole parent exact M192,
  exactly 16 paths, one matching sign-off, truthful identity, no merge, clean
  worktree, expected `0 94` divergence, and zero M193 scratch.
- A fresh pruned fetch, direct hosted-ref query, local ancestry and branch
  inventory, authenticated account check, and recent PR history leave hosted
  `main` at exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`,
  tree `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`. M192 is absent and not an
  ancestor, PR #251 remains latest, and no milestone branch is hosted.
  Publication is withheld: no push, PR, hosted allocation, tag, release, or
  package publication occurs.
- This reconciliation record is folded into the final closeout amendment; the
  successor milestone records the ultimate M193 hash without self-reference.

### M193 explicit non-scope

- Arbitrary malformed, partial, separate, repeated, or longer input; arbitrary
  or unbounded child output; duplicated/inherited writers; cross-principal or
  unrelated-process behavior; hostile simultaneous racing; authenticated
  framing; crash/power loss; durable intent, rollback, reconciliation, typed
  recovery receipts; ReFS/SMB/other-host evidence; Windows admission; and
  cleanup authority.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M192 Windows hard-link alias mutator invalid-prefix valid-close-suffix boundary

- **Task:** Determine how M186's unchanged mutator child settles when one
  flushed write contains a fixed invalid byte followed by the valid close byte
  after exact `recreated`.
- **Status:** Locally complete through direction, test-first implementation,
  public documentation, supported-Python regression, concentrated and repeated
  Windows behavior, rendering/profiles, initial and record-state distribution/
  release rehearsal, governance, findings-first review, and separators.
  Guarded cleanup, the post-record separator, DCO, and fresh hosted
  reconciliation are complete. Publication is withheld because hosted `main`
  lacks M100-M191.
- **Base:** Fully locally validated M191 DCO commit
  `882d8827aee17cca4d4acf3fdc4da43d185a8856`, tree
  `0f57ff5c0207ea26c000959a7a0ff3697a5fd2ce`, sole parent exact M190.
- **Branch:**
  `release/m192-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate-boundary`;
  the redundant local M191 branch name was removed after exact M192 branch
  creation retained its object.

### M192 acceptance boundary

- Accept RFC-0175 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, and M186's
  unchanged fixed mutator child.
- Require initial shared identity/link count two, guardian `ready`, exact-name
  rename error 32, child-owned alias deletion/recreation, and exact `deleted`
  then `recreated` events.
- Write fixed `?!` exactly once, require both bytes accepted and flushed, close
  the parent writer, and require bounded exit 5, no `closed` event, stdout EOF,
  and empty stderr.
- While the guardian remains live, require alias presence, shared identity and
  bytes, link count two, range availability through both names, and continued
  exact-name rename refusal. Close the guardian exactly, rename, and require
  complete process/stream/native/range cleanup.
- State the result narrowly as leading-byte rejection for one fixture and one
  fixed sequence. Do not claim arbitrary malformed-input handling, general
  message framing, durable commit, recovery, Windows admission, or cleanup
  authority.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, version, or CI change.

### M192 development evidence so far

- The exact M191 architecture/live baseline passed nine tests. Static and dated
  strict governance each returned zero findings across three objectives, seven
  requirements, and four work items after correcting the initial restricted
  cache access.
- Current Microsoft byte-stream and write documentation, Python buffered-I/O
  contracts, and GitHub workflow/billing guidance support one narrow fixed
  prefix observation and no additional hosted allocation.
- The live probe passed its first execution. The intended architecture red
  passed behavior and non-documentation guards while identifying only the
  missing decision/registration records. After both decisions, only public
  registrations remained red; after those registrations, all nine checks
  passed.
- Mechanical formatting changed one Python file. Both Python files then passed
  Ruff and strict Pyright, and all nine focused checks pass in 0.44 seconds.
- Exact CPython 3.12.13, isolated 3.13.13, and isolated 3.14.5 each pass
  4,026 tests with 17 skips in 261.12, 231.00, and 240.08 seconds.
- The 44 M149-M192 architecture modules plus all 44 Windows cache-cleanup
  integration modules pass 333 tests with one established skip. Twenty
  independent live observations pass in 0.35-0.38 seconds each.
- Ten real-wgpu tests pass. Fresh two- and three-workload profiles validate;
  all eight profile-schema tests pass. Clockwork Arena and Agent World Builder
  reproduce their established state, capture, replay, draw, sprite, match, and
  batch identities.
- The unchanged 46-package lock and exact 45-package graphics environment
  resolve. All 574 Python files are format-clean; Ruff, strict Pyright, strict
  docs, static and dated governance, and whitespace pass.
- Two builds reproduce a 362,408-byte pure wheel at SHA-256
  `58ba23dc880407426b3b24b88732bd7d7fe90ad073c0a712a8cb00fd977e2a67`
  and a 2,264,718-byte source archive at SHA-256
  `8aff71208ca31320aba05cdbd6e5428ed6171bd8294454d4eed1cce2261622c2`.
  Complete installed-wheel smoke passes. Two ten-artifact release stages are
  byte-identical and both complete release smokes pass. Inventory is 114 wheel/
  935 source entries; all four M192 files are source-only.
- Findings-first review confirms exactly 16 intended paths, no runtime/package/
  fixture/dependency/workflow/CI diff, no added development-tool identity,
  credential assignment, or local-path material, and no test/native/WASM/
  bytecode wheel payload. Fourteen exact hygiene/architecture/live checks pass;
  no actionable finding remains before record-state gates.
- Record-inclusive static checks keep all 574 Python files clean; 14 exact
  review tests, strict docs, dated governance, and whitespace pass. Two final
  builds reproduce the unchanged wheel and a 2,265,482-byte source archive at
  SHA-256
  `1ac927e641d39dc82896628dd450ceaf85fa868b9ae419445dacd6498036c087`.
  Complete installed-wheel smoke passes; two final ten-artifact release stages
  are byte-identical and both complete release smokes pass.
- Cleanup audit corrected directory/file parent-property assumptions before any
  deletion. Its final type-aware pass verified 49 exact M192 scratch targets as
  repository-confined, ignored, and top-level plus recursively reparse-free;
  guarded removal completed with zero M192 target remaining.
- The post-record separator keeps both Python files static-clean; 14 exact
  review tests, strict docs, dated governance, and whitespace pass. Its two
  regenerated targets were revalidated, removed, and confirmed absent with
  zero M192 scratch remaining.
- Initial DCO commit `4ff6e8442736c3e240afc7e1f0f940776156757c`, tree
  `0a8642e432b890961536e790b3066d71ce8368fd`, has sole parent exact M191,
  exactly 16 intended paths, one matching sign-off, truthful configured
  author/committer identity, no merge, expected `0 93` divergence, a clean
  worktree, zero M192 scratch, and clean connectivity apart from ordinary
  dangling records. This factual record is folded into the closeout amendment;
  the successor milestone will record the amended hash without self-reference.

### M192 publication boundary

- Pre-publication amended DCO object
  `060f1e2c9e6cd2befc9bad9b204ffc2b360adf47`, tree
  `194941a19d838c7df9af5c69bd9e993899db1155`, has sole parent exact M191,
  exactly 16 paths, one matching sign-off, truthful identity, no merge, clean
  worktree, expected `0 93` divergence, and zero M192 scratch.
- A fresh pruned fetch, direct hosted-ref query, local ancestry and branch
  inventory, authenticated account check, and recent PR history leave hosted
  `main` at exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`,
  tree `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`. M191 is absent and not an
  ancestor, PR #251 remains latest, and no milestone branch is hosted.
  Publication is withheld: no push, PR, hosted allocation, tag, release, or
  package publication occurs.
- This reconciliation record is folded into the final closeout amendment; the
  successor milestone records the ultimate M192 hash without self-reference.

### M192 explicit non-scope

- Arbitrary malformed, partial, separate, repeated, or longer input;
  duplicated/inherited writers; cross-principal or unrelated-process behavior;
  hostile simultaneous racing; explicit authenticated framing; crash/power
  loss; durable intent, rollback, reconciliation, typed recovery receipts;
  ReFS/SMB/other-host evidence; Windows admission; and cleanup authority.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M191 Windows hard-link alias mutator valid-close prefix with trailing byte boundary

- **Task:** Determine how M186's unchanged mutator child settles when one
  flushed write contains the valid close byte followed by one fixed invalid
  byte after exact `recreated`.
- **Status:** Locally complete through direction, test-first implementation,
  public documentation, supported-Python regression, concentrated and repeated
  Windows behavior, rendering/profiles, distribution/release rehearsal,
  governance, findings-first review, separators, cleanup, DCO audit, and fresh
  hosted reconciliation. Publication is withheld because hosted `main` lacks
  M100-M190.
- **Base:** Fully locally validated M190 DCO commit
  `3d84bda9e41caf82a683e359210b7b9e74e9f8cc`, tree
  `6d49c1eeb2b383a6bf267fb05a44e8a4326e4bb8`, sole parent exact M189.
- **Branch:**
  `release/m191-windows-hard-link-alias-mutator-valid-close-prefix-trailing-byte-after-recreate-boundary`;
  the redundant local M190 branch name was removed after exact M191 branch
  creation retained its object.

### M191 acceptance boundary

- Accept RFC-0174 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, and M186's
  unchanged fixed mutator child.
- Require initial shared identity/link count two, guardian `ready`, exact-name
  rename error 32, child-owned alias deletion/recreation, and exact `deleted`
  then `recreated` events.
- Write the fixed sequence `!?` exactly once, require both bytes accepted and
  flushed, then require exact `closed` while the parent writer remains open.
  Close that writer and require bounded exit 0, stdout EOF, and empty stderr.
- While the guardian remains live, require alias presence, shared identity and
  bytes, link count two, range availability through both names, and continued
  exact-name rename refusal. Close the guardian exactly, rename, and require
  complete process/stream/native/range cleanup.
- State the result narrowly as byte-prefix acceptance for one fixture and one
  fixed sequence. Do not claim arbitrary malformed-input handling, general
  message framing, durable commit, recovery, Windows admission, or cleanup
  authority.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, version, or CI change.

### M191 development evidence so far

- Current Microsoft anonymous-pipe and byte-mode pipe documentation, Python
  buffered-I/O contracts, GitHub matrix and billing guidance, NIST SSDF, SLSA,
  and bounded-execution safety guidance support one narrow trailing-input
  observation and no hosted allocation.
- The exact M190 architecture/live baseline passed nine tests. Static and
  dated strict governance each returned zero findings across three objectives,
  seven requirements, and four work items.
- The live probe passed its first execution. The intended architecture red
  passed behavior and non-documentation guards while identifying only the
  missing decision/registration records. After those records, all nine focused
  checks passed.
- Ruff requested mechanical formatting of both Python files. That formatting
  exposed three line-wrap-sensitive architecture assertions; their narrow
  correction left both files format-, Ruff-, and strict-Pyright clean, and all
  nine focused checks pass in 0.45 seconds. Strict docs also pass with only the
  known Material notice.
- The first complete CPython 3.12.13 run passed 4,016 tests before one
  repository-neutrality failure identified a source publisher named in a new
  evidence row. After retaining only the source category, the five-case
  hygiene guard passed and exact CPython 3.12.13, isolated 3.13.13, and
  isolated 3.14.5 each pass 4,017 tests with 17 skips in 280.32, 234.21, and
  244.89 seconds.
- The 43 M149-M191 architecture modules plus 43 Windows cache-cleanup
  integration modules pass 324 tests with one established skip. Twenty
  independent live observations pass in 0.35-0.39 seconds each.
- Ten real-wgpu tests pass. Fresh two- and three-workload profiles validate;
  all eight profile-schema tests pass. Clockwork Arena and Agent World Builder
  reproduce their established state, capture, replay, draw, sprite, match, and
  batch identities.
- The unchanged 46-package lock and exact 45-package graphics environment
  resolve. All 572 Python files are format-clean; Ruff, strict Pyright, strict
  docs, static and dated governance, and whitespace pass.
- Two builds reproduce a 362,338-byte pure wheel at SHA-256
  `301aee0997a554793462edcadd63081ee8b4ee85f75c51706466a6a408d57bc6`
  and a 2,257,594-byte source archive at SHA-256
  `55b2c01d16800c959207bb925a5b7cbf2ad9fbb6c7b610de3cea64b0002fa0e5`.
  Complete installed-wheel smoke passes. Two ten-artifact release stages are
  byte-identical and both complete release smokes pass. Inventory is 114
  wheel/931 source entries; all four M191 files are source-only.
- Findings-first review confirms exactly 16 intended paths, no runtime/package/
  fixture/dependency/workflow/CI diff, no added credential or local-path
  material, a tool-neutral repository, and no test/native/WASM/bytecode wheel
  payload. No actionable finding remains before the final record-state gates.
- Record-inclusive builds reproduce the unchanged wheel and a 2,258,812-byte
  source archive at SHA-256
  `4cc112204d1f18df5727ced8a84e6ec85e5e076c4ca3c78d059280419a510292`.
  Complete installed-wheel smoke passes; two final ten-artifact release stages
  are byte-identical and both complete release smokes pass.
- The final pre-commit separator keeps both Python files format-, Ruff-, and
  strict-Pyright clean; 14 exact hygiene/architecture/live checks, strict docs,
  dated governance, and whitespace pass.
- Guarded cleanup verified all 49 exact M191 scratch/generated-docs targets as
  repository-confined, ignored, and top-level plus recursively reparse-free,
  removed them, and confirmed zero M191 target and no generated site remains.
- The final post-record separator again keeps both Python files static-clean;
  14 exact checks, strict docs, dated governance, and whitespace pass. Its two
  exact generated targets were revalidated, removed, and confirmed absent.
- Initial DCO commit `7313bae15ab1f830891c521dc6ec5ef9b69f990f`, tree
  `1dd6beb3c0dd6205ca8f16c6dc9c8588fee22790`, has sole parent exact M190,
  exactly 16 intended paths, one matching sign-off, truthful configured
  author/committer identity, no merge, expected `0 92` divergence, a clean
  worktree, zero M191 scratch, and clean connectivity apart from ordinary
  dangling records. This factual record is folded into the closeout amendment;
  the successor milestone will record the amended hash without self-reference.

### M191 publication boundary and explicit non-scope

- A fresh pruned fetch, direct hosted-ref/tree query, local ancestry and branch
  inventory, authenticated account check, and recent PR history leave hosted
  `main` at exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`,
  tree `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`. M190 is absent and
  not an ancestor, PR #251 remains latest, and no milestone branch is hosted.
  Publication is withheld: no push, PR, hosted allocation, tag, release, or
  package publication occurs.
- Arbitrary malformed, partial, separate, repeated, or longer input;
  duplicated/inherited writers; cross-principal or unrelated-process behavior;
  hostile simultaneous racing; explicit authenticated framing; crash/power
  loss; durable intent, rollback, reconciliation, typed recovery receipts;
  ReFS/SMB/other-host evidence; Windows admission; and cleanup authority.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

Pre-publication amended DCO object
`a4da22845a844d934ae5b5e3914ebbd989de0f00`, tree
`cd9da89a59bbcf4338c558ebdad88c4aa2c718d4`, has sole parent exact M190,
exactly 16 paths, one matching sign-off, truthful identity, no merge, expected
`0 92` divergence, clean worktree, zero M191 scratch, and clean connectivity.
This hosted-reconciliation record is folded into the final closeout amendment;
the successor milestone records the ultimate hash without self-reference.

## M190 Windows hard-link alias mutator invalid-control after recreation boundary

- **Task:** Determine the residual namespace state when M186's independent
  mutator child receives one fixed invalid control byte after exact
  `recreated` and before the close token.
- **Status:** Locally complete at final DCO commit
  `3d84bda9e41caf82a683e359210b7b9e74e9f8cc`, tree
  `6d49c1eeb2b383a6bf267fb05a44e8a4326e4bb8`; publication is withheld because
  hosted `main` lacks M100-M189.
- **Base:** Fully locally validated M189 DCO commit
  `2f7c61379ccd608a869c866e4937e7937906a64c`, tree
  `641b6e8fae20947e92fd5b87f58ca07d958757ee`, sole parent exact M188.
- **Branch:** The M190 branch name was retired after exact M191 branch creation;
  its final object remains M191's base.

### M190 acceptance boundary

- Accept RFC-0173 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, and M186's
  unchanged fixed mutator child.
- Require initial shared identity/link count two, guardian `ready`, exact-name
  rename error 32, child-owned alias deletion/recreation, and exact `deleted`
  then `recreated` events.
- Write exactly one repository-fixed invalid `?` byte, require an exact
  one-byte buffered write, flush and close the parent writer, and wait with
  M186's fixed bound. Require exact exit 5, no `closed` event, stdout EOF, and
  empty stderr.
- While the guardian remains live, require alias presence, shared identity and
  bytes, link count two, range availability through both names, and continued
  exact-name rename refusal. Close the guardian exactly, rename, and require
  complete process/stream/native/range cleanup.
- State the result narrowly: the fixed invalid token after recreation leaves
  the peer alias present and does not automatically roll back to one link.
  This is distinct from control-pipe EOF and abrupt termination and is not
  durable commit, recovery, Windows admission, or cleanup authority.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, version, or CI change.

### M190 development evidence so far

- Current Microsoft pipe and hard-link documentation, Python stream and
  subprocess contracts, GitHub matrix semantics, and NIST SSDF guidance
  support one bounded invalid-byte observation and no hosted allocation.
- The exact M189 architecture/live baseline passed nine tests. Static and
  dated strict governance returned zero findings; the first dated invocation
  was cache-denied before checking and its exact access-enabled rerun passed.
- The live probe passed first execution. The first combined architecture/live
  run passed behavior and seven guards but exposed one formatter-sensitive
  guard. After narrow correction and mechanical formatting, eight guards plus
  the live behavior pass nine tests; targeted Ruff and strict Pyright pass;
  strict docs pass.
- Exact CPython 3.12.13, isolated 3.13.13, and isolated 3.14.5 complete
  45-package graphics environments each pass 4,008 tests with 17 skips in
  301.23, 266.76, and 277.50 seconds.
- The 42 M149-M190 architecture modules plus 42 Windows cache-cleanup
  integration modules pass 315 tests with one established skip. The first
  repetition wrapper supplied an empty base-temp and pytest rejected it before
  collection; the corrected wrapper passes 20 independent live observations
  in 0.36-0.43 seconds each.
- Ten real-wgpu tests pass. Fresh two- and three-workload profiles validate;
  all eight profile-schema tests pass. Clockwork Arena and Agent World Builder
  reproduce their established state, capture, replay, draw, sprite, match, and
  batch identities.
- The unchanged 46-package lock and exact 45-package graphics environment
  resolve. All 570 Python files are format-clean; Ruff, strict Pyright, strict
  docs, and whitespace pass. The first sandboxed lock/sync calls were denied
  external uv-cache access; their exact access-enabled rerun passed.
- Two builds reproduce a 362,252-byte pure wheel at SHA-256
  `275738ae405af226003a2884951afa3ad379e32e397d5cdc2f966750ced5d43f`
  and a 2,247,477-byte source archive at SHA-256
  `d35b7b4f4f15265f4a48fa43ecaf84dca19c1b9f0affca744c7731af7470c3ac`.
  The complete installed-wheel smoke passes. Two ten-artifact release stages
  are byte-identical and both complete release smokes pass. Inventory is 114
  wheel/927 source entries; all four M190 files are source-only and the wheel
  contains no test, project-record, native, WASM, or bytecode payload.
- Record-inclusive source, Windows, docs, governance, scope, security, and
  package-boundary gates pass. Final record-state builds reproduce the
  unchanged wheel and a 2,250,591-byte source archive at SHA-256
  `4ecc42087b2a458e7b8c0c1da96f5a51907dcad264edf78d19065e901274dcf3`;
  installed-wheel and dual release smokes pass.
- The final source separator corrected one documentation/guard wording
  mismatch; both Python files, all nine focused checks, strict docs, dated
  governance, and whitespace pass after correction.
- Guarded cleanup verified and removed all 56 exact repository-confined,
  untracked, reparse-free M190 scratch targets; zero M190 target remains.
- The final post-record separator passes both Python files, all nine focused
  checks, strict docs, dated governance, and whitespace; its two exact
  generated targets were revalidated, removed, and confirmed absent.
- Initial DCO commit `e30a6e8f9b3351a197f96e3ed05314355288b7af`,
  tree `42881b058857857678abc2839f34d2144a594b99`, has sole parent exact
  M189, exactly 16 intended paths, one matching sign-off, truthful configured
  author/committer identity, no merge, expected `0 91` divergence, a clean
  worktree, zero M190 scratch, and clean connectivity apart from ordinary
  dangling records. This factual record is folded into the closeout object.

### M190 publication boundary and explicit non-scope

- A final fresh pruned fetch, direct hosted-ref query, local hosted tree and
  ancestry checks, authenticated recent PR history, and branch inventory leave
  hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, without M189; PR #251 is
  latest and no milestone branch is hosted. Publication is withheld: no push,
  PR, hosted allocation, tag, release, or package publication occurs.
- Cross-principal or unrelated-process behavior, duplicated/inherited control
  writers, arbitrary malformed or partial/multiple input, hostile simultaneous
  racing, crash or power-loss consistency, trusted root ownership, link
  enumeration, ReFS/SMB/driver variation, durable intent, rollback/
  reconciliation policy, typed recovery receipts, Windows admission, cleanup
  authority, or independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M189 Windows hard-link alias mutator control-pipe EOF after recreation boundary

- **Task:** Determine the residual namespace state when M186's independent
  mutator child receives control-pipe EOF after exact `recreated` and before the
  close token.
- **Status:** Locally complete at final DCO commit
  `2f7c61379ccd608a869c866e4937e7937906a64c`; publication is withheld because
  hosted `main` lacks M100-M188.
- **Base:** Fully locally validated M188 DCO commit
  `137442543d50f6795308372230c6677f34eec087`, tree
  `a12e0c5139c9ce60cf85a62f5a087cce5ae5a032`, sole parent exact M187.
- **Branch:** The M189 branch name was retired after exact M190 branch creation;
  its exact final object remains M190's base.

### M189 acceptance boundary

- Accept RFC-0172 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, and M186's
  unchanged fixed mutator child.
- Require initial shared identity/link count two, guardian `ready`, exact-name
  rename error 32, child-owned alias deletion/recreation, and exact `deleted`
  then `recreated` events.
- Send no close token. Close only the parent `Popen.stdin`, wait with M186's
  fixed bound, and require exact exit 5, no `closed` event, stdout EOF, and
  empty stderr.
- While the guardian remains live, require alias presence, shared identity and
  bytes, link count two, range availability through both names, and continued
  exact-name rename refusal. Close the guardian exactly, rename, and require
  complete process/stream/native/range cleanup.
- State the result narrowly: control-pipe EOF after recreation leaves the peer
  alias present and does not automatically roll back to one link. This is not
  abrupt termination, durable commit, recovery, Windows admission, or cleanup
  authority.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, version, or CI change.

### M189 development evidence so far

- Current official pipe, subprocess, hard-link, GitHub matrix, and NIST
  verification guidance supports the bounded EOF observation and no CI change.
- The exact M188 architecture/live baseline passed nine tests. Static and
  dated strict governance returned zero findings; one dated and one
  concentrated uv invocation were cache-denied before execution and their
  exact access-enabled reruns passed.
- The new live probe passed first execution. The first combined run exposed
  one over-broad architecture substring and the intended missing public
  registrations. After narrow correction, both Python files pass focused
  formatting, Ruff, and strict Pyright; eight guards plus live behavior pass
  nine tests; strict docs and whitespace pass.
- Exact CPython 3.12.13, isolated 3.13.13, and isolated 3.14.5 complete
  45-package graphics environments each pass 3,999 tests with 17 skips in
  252.98, 254.39, and 270.40 seconds.
- The 41 M149-M189 architecture modules plus 41 Windows cache-cleanup
  integration modules pass 306 tests with one established skip. Twenty
  independent live repetitions pass in 0.35-0.38 seconds.
- Ten real-wgpu tests, fresh two/three-workload profiles, eight profile tests,
  Clockwork Arena, and Agent World Builder reproduce their established
  deterministic identities.
- The unchanged 46-package lock and exact 45-package graphics environment
  resolve. All 568 Python files are format-clean; Ruff, strict Pyright, strict
  docs, static/dated governance, and whitespace pass.
- Two builds reproduce a 362,208-byte pure wheel at SHA-256
  `0265b8f0b004d4a9f9db39cba7a149feddc6521417859944499bd7c09d2b37e5`
  and a 2,241,034-byte source archive at SHA-256
  `7b691bfb273df0ae6bac0ebd0d66acd768b35800f43b272cf143308b4e092cba`.
  Primary plus 27 additional installed-wheel consumers pass. Two ten-artifact
  release stages are byte-identical and both complete release smokes pass.
  Inventory is 114 wheel/923 source entries; all four M189 files are
  source-only.
- The record-inclusive separator keeps the unchanged lock/environment, all 568
  Python files, nine focused checks, the 306-pass/one-skip Windows boundary,
  strict docs, both governance modes, and whitespace clean.
- Two record-inclusive builds reproduce a 362,195-byte pure wheel at SHA-256
  `5673fc31242a65ec10ceecc614806fd81357564fb3edcce8bbbab6f804d8173d`
  and identical 2,243,024-byte source archives at SHA-256
  `07e2c5c9108d9548e33d738aace9d410ec068ad5c2fddca6c8ddfbfd60a0aa05`.
  Primary plus all 27 additional installed-wheel consumers pass against the
  final wheel. Both final ten-artifact release stages are byte-identical and
  pass complete release smoke.
- Findings-first review confirms exactly 16 intended paths: four new
  source-only evidence files, eight public registrations, and four project
  records. Runtime/package code, fixtures, examples, scripts, workflows,
  metadata, dependencies, lock, version, and root exports have zero diff. New
  additions contain no development-tool identity, credential assignment, or
  local path; the wheel has no native/WASM payload. No actionable correctness,
  architecture, security, documentation, compatibility, package, or
  CI-allocation finding remains.
- Guarded cleanup removed all 45 exact M189 scratch targets. Two initial
  confinement-property corrections stopped before deletion; a sandboxed
  traversal then removed 13 accessible artifact/file targets but could not
  traverse 32 pytest-owned directories despite returning a misleading zero.
  The terminating access-enabled rerun revalidated repository confinement and
  zero reparse points, removed the remaining 32, and confirmed zero exact
  M189 target remains.
- The final pre-commit separator keeps both M189 Python files format-, Ruff-,
  and strict-Pyright clean; nine focused checks, strict docs, dated governance,
  and whitespace pass. Its two exact regenerated targets were revalidated,
  removed, and confirmed absent.
- Final DCO commit `2f7c61379ccd608a869c866e4937e7937906a64c`, tree
  `641b6e8fae20947e92fd5b87f58ca07d958757ee`, has sole parent exact M188,
  exactly 16 intended paths, one matching sign-off, truthful configured
  author/committer identity, no merge, expected `0 90` divergence from
  hosted/local M99 `main`, a clean worktree, zero exact M189 scratch, and clean
  connectivity apart from ordinary dangling records.

### M189 publication boundary and explicit non-scope

- A final pruned fetch, direct hosted-ref query, local hosted tree/ancestry
  check, remote-branch inventory, and authenticated recent PR history leave
  hosted `main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, tree
  `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`; M188 is absent, only remote
  `main` exists, and PR #251 remains the latest hosted PR.
- Publication is withheld. No push, PR, hosted workflow allocation, tag,
  release, or package publication occurs.
- Cross-principal or unrelated-process behavior, duplicated/inherited control
  writers, hostile simultaneous racing, crash or power-loss consistency,
  trusted root ownership, link enumeration, ReFS/SMB/driver variation,
  durable intent, rollback/reconciliation policy, typed recovery receipts,
  Windows admission, cleanup authority, or independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M188 Windows hard-link alias mutator abrupt-loss-after-recreate boundary

- **Task:** Determine the residual namespace state when M186's independent
  mutator child is terminated after exact `recreated` and before the close
  token.
- **Status:** Locally complete at final DCO commit
  `137442543d50f6795308372230c6677f34eec087`; publication is withheld because
  hosted `main` lacks M100-M187.
- **Base:** Fully locally validated M187 DCO commit
  `2f0869c3aeb632daa68a2e460f2b2cb3d34a1e7e`, tree
  `9efa5bcdf44ca8cd47831f9eacabe207383587a1`, sole parent exact M186.
- **Branch:** The M188 branch name was retired by M189's in-place rename; its
  exact final object remains M189's base.

### M188 acceptance boundary

- Accept RFC-0171 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, and M186's
  unchanged fixed mutator child.
- Require initial shared identity/link count two, guardian `ready`, exact-name
  rename error 32, child-owned alias deletion and recreation, and exact
  `deleted` then `recreated` events.
- Before any close token, terminate and reap the mutator through the existing
  bounded helper; require a nonzero exit and empty remaining output.
- While the guardian remains live, require alias presence, shared original and
  alias identity/bytes, link count two, range availability through both names,
  and continued exact-name rename refusal.
- Close the guardian exactly, rename the original, and require displaced and
  alias identities, two-link counts, bytes, processes, streams, native handles,
  and ranges to settle completely.
- State the evidence precisely: abrupt process loss after recreation leaves the
  alias present and does not automatically roll back to one link. This is not
  durable commit, recovery, crash consistency, Windows admission, or cleanup
  authority.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, version, or CI change.

### M188 development evidence so far

- Current Microsoft process and hard-link documentation plus Python's
  subprocess contract support a bounded terminate/wait observation and reject
  rollback or durability claims. GitHub matrix and NIST SSDF status justify no
  CI or conformance change.
- The exact M187 architecture/live baseline passes nine tests. Static and dated
  strict governance pass; one dated invocation was sandbox-denied before the
  checker and its exact access-enabled rerun passed.
- The first combined implementation run passed the live observation and seven
  guards; one public-registration guard failed as intended. After eight narrow
  public registrations, both Python files pass format, Ruff, and strict
  Pyright, eight guards plus the live probe pass nine tests, strict docs pass,
  and whitespace is clean.
- Exact CPython 3.12.13, isolated 3.13.13, and isolated 3.14.5 complete frozen
  45-package graphics environments each pass 3,990 tests with 17 skips in
  299.97, 286.40, and 303.36 seconds.
- The exact 40 M149-M188 architecture modules plus 40 Windows cache-cleanup
  integration modules pass 297 tests with one established skip. Twenty
  independent live repetitions pass in 0.36-0.45 seconds.
- Ten real-wgpu tests, two/three-workload profiles, eight profile-schema tests,
  Clockwork Arena, and Agent World Builder reproduce their established
  identities.
- The unchanged 46-package lock and exact 45-package graphics environment
  resolve. All 566 Python files are format-clean; Ruff and strict Pyright pass.
- Two builds reproduce a 362,127-byte pure wheel at SHA-256
  `228066129979b3eceb3c766e66d7ed2577172998e76e309635a324a24a4f1660`
  and a 2,234,521-byte source archive at SHA-256
  `40f19af2899390a323bdb6e4398b15c898498f281b17921178be71055b30d0e5`.
  Primary plus 27 additional installed-wheel consumers pass. Two ten-artifact
  release stages are byte-identical and both complete release smokes pass.
  Inventory is 114 wheel/919 source entries; all four M188 files are
  source-only.
- The record-inclusive separator keeps the unchanged lock/environment, all 566
  Python files, nine focused checks, the 297-pass/one-skip Windows boundary,
  strict docs, both governance modes, and whitespace clean.
- Two record-inclusive builds reproduce the unchanged 362,127-byte wheel and
  identical 2,236,761-byte source archives at SHA-256
  `5cd21d6a7a1bc6e0c670d96fc907facc6328a8852006eb519c219b184a00277c`.
  Primary wheel smoke and both final ten-artifact release smokes pass; the 27
  earlier consumer results apply byte-for-byte to the unchanged wheel.
- Findings-first review confirms exactly 16 intended paths: four new
  source-only evidence files, eight public registrations, and four project
  records. Runtime/package code, fixtures, examples, scripts, workflows,
  metadata, dependencies, lock, version, and root exports have zero diff. No
  public development-tool identity, credential assignment, or local path was
  added, and no actionable correctness, architecture, security, documentation,
  compatibility, package, or CI-allocation finding remains.
- Exact guarded cleanup revalidated and removed 42 repository-confined M188
  test, profile, docs, distribution, and release targets. The selected trees
  contained expected test hard links but no reparse points. Zero exact M188
  scratch target remains.
- The final pre-commit separator keeps both M188 Python files format-, Ruff-,
  and strict-Pyright clean; nine focused checks, strict docs, dated governance,
  and whitespace pass. Its two exact regenerated targets were revalidated,
  removed, and confirmed absent.
- Final DCO commit `137442543d50f6795308372230c6677f34eec087`, tree
  `a12e0c5139c9ce60cf85a62f5a087cce5ae5a032`, has sole parent exact M187,
  exactly 16 intended paths, one matching sign-off, truthful configured
  author/committer identity, no merge, expected `0 89` divergence from
  hosted/local M99 `main`, a clean worktree, zero exact M188 scratch, and clean
  connectivity apart from 325 ordinary dangling records.
- The post-record separator passes nine focused checks, strict docs, dated
  governance, and whitespace. Its two exact regenerated targets were
  revalidated, removed, and confirmed absent.

### M188 publication boundary

- A final fresh pruned fetch, direct hosted-ref/tree query, ancestry test,
  remote-branch inventory, and authenticated recent PR history still leave
  hosted `origin/main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; M187's prerequisite stack is
  absent, only remote `main` exists, and PR #251 is the latest merged PR.
- Publication is withheld. No push, PR, hosted workflow allocation, tag,
  release, or package publication occurs.

### M188 explicit non-scope

- Cross-principal or unrelated-process behavior, hostile simultaneous racing,
  crash or power-loss consistency, trusted root ownership, link enumeration,
  ReFS/SMB/driver variation, file-ID reuse, durable intent, quarantine,
  rollback/reconciliation policy, typed recovery receipts, Windows admission,
  cleanup authority, or independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M187 Windows hard-link alias mutator abrupt-loss boundary

- **Task:** Determine the residual namespace state when M186's independent
  mutator child is terminated after its exact `deleted` event and before the
  recreate token.
- **Status:** Locally complete. Direction, implementation, supported-Python
  regression, concentrated/repeated Windows behavior, rendering/profiles,
  record-inclusive distribution/release rehearsal, governance, review,
  cleanup, DCO object audit, and publication-safety recheck pass. Publication
  is withheld because hosted `main` lacks M100-M186.
- **Base:** Fully locally validated M186 DCO commit
  `3357f1e38de6b25ecdf15502ae46124bebcb3597`, tree
  `6fc99f5496b39cf3304cf1713db9f93e20452322`, sole parent exact M185.
- **Branch:**
  `release/m187-windows-hard-link-alias-mutator-abrupt-loss-boundary`; exact
  containment removed the redundant local M186 branch name.

### M187 acceptance boundary

- Accept RFC-0170 and retain one current-host Windows-only, test-only NTFS
  observation over M173's coordination file, M181's guardian, and M186's
  unchanged fixed mutator child.
- Require initial shared identity/link count two, guardian `ready`, exact-name
  rename error 32, child-owned alias deletion, and exact `deleted`.
- Send no recreate token. Terminate and reap the mutator through the existing
  bounded helper; require a nonzero exit and empty remaining output.
- While the guardian remains live, require alias absence, unchanged original
  identity and bytes, link count one, range availability, and continued
  exact-name rename refusal.
- Close the guardian exactly, rename the original, and require the displaced
  one-link identity, bytes, processes, streams, native handles, and ranges to
  settle completely.
- State the evidence precisely: abrupt process loss leaves the alias absent;
  there is no automatic rollback or recovery. This remains a three-process,
  same-principal, parent-owned-tree observation, not cleanup admission.
- Add no runtime API, fixture, dependency, workflow, job/allocation,
  permission, release authority, or CI change.

### M187 development evidence so far

- Current Microsoft process, hard-link, and file documentation plus Python's
  subprocess contract support a bounded terminate/reap observation and reject
  a recovery claim. GitHub matrix and NIST SSDF status justify no CI or
  conformance change.
- The exact M186 focused pair passes nine tests. Static and dated strict
  governance pass after access-enabled reruns of cache-denied invocations.
- The new live probe passed on its first run. The first public-boundary run
  found one exact no-hosted-check wording mismatch; after correction and one
  mechanical format, eight guards plus the live probe pass nine tests.
- Exact CPython 3.12.13, isolated 3.13.13, and isolated 3.14.5 complete frozen
  graphics environments each pass 3,981 tests with 17 skips. The first 3.12
  launch was sandbox-denied before pytest and is not counted.
- The 78-file M149-M187 Windows boundary passes 288 tests with one established
  skip. Twenty independent live repetitions pass after one sandbox-denied
  pre-execution attempt.
- Ten real-wgpu tests, fresh one-repeat two/three-workload profiles, eight
  profile-schema tests, Clockwork Arena, and Agent World Builder pass with
  established identities.
- The unchanged 46-package lock and exact 45-package graphics environment
  resolve. All 564 Python files are format-clean; Ruff, strict Pyright, strict
  docs, both governance modes, and whitespace pass.
- Two builds reproduce a 362,058-byte pure wheel at SHA-256
  `5792c7c9206f318cacc65d468a8419a0ef54450c12fbccdb51a0acb3bf6b5080`
  and a 2,227,485-byte source archive at SHA-256
  `e6bf579a9bc04f05c2ed1bb2013727b3a265f2109378809b0d31b1ac60d659db`.
  Primary plus 27 additional installed-wheel consumers pass. Two ten-artifact
  release stages are byte-identical and both complete smokes pass. Inventory
  finds 114 wheel and 915 source entries; all four M187 files are source-only.
- The record-inclusive separator retains the unchanged lock/environment, all
  564 Python files, nine focused checks, the 288-pass/one-skip Windows boundary,
  strict docs, both governance modes, and whitespace.
- Two final builds reproduce the unchanged 362,058-byte wheel and identical
  2,230,290-byte source archives at SHA-256
  `32bf32c2a1ccd251e173bf30714b4e5cc9a38f96f465c448bdcb9fbecb03cf49`.
  Primary wheel smoke and both final ten-artifact release smokes pass; the 27
  earlier consumers apply byte-for-byte to the unchanged wheel.
- Findings-first review confirms exactly 16 intended paths: four new
  source-only evidence files, eight public registrations, and four project
  records. Runtime/package code, fixtures, examples, scripts, workflows,
  metadata, dependencies, lock, version, and root exports have zero diff. No
  actionable correctness, architecture, security, documentation,
  compatibility, package-boundary, allocation, public-identity, credential,
  or newly introduced local-path finding remains.
- Exact guarded cleanup revalidated and removed 45 repository-confined,
  ignored, untracked, top-level and nested reparse-free M187 scratch targets.
  Zero exact M187 target remains; older scratch and the managed environment
  were not selected.
- The final pre-commit separator keeps both M187 Python files format-, Ruff-,
  and strict-Pyright clean; nine focused checks, strict docs, dated governance,
  and whitespace pass. Its exact two regenerated scratch targets were
  revalidated, removed, and confirmed absent.
- Initial DCO commit `b8ff0fe3663983bc6a39274bd754306d34ab5a0e`,
  tree `77cd50b714162df5b311096c3b6f412d037174e6`, has sole parent exact M186,
  exactly 16 intended paths, one matching sign-off, truthful configured
  author/committer identity, no merge, expected `0 88` divergence from
  hosted/local M99 `main`, a clean worktree, zero exact M187 scratch, and clean
  connectivity apart from 323 ordinary dangling records. This factual record
  will be folded into the closeout object.
- The post-record separator passes nine focused checks, strict docs, dated
  governance, and whitespace. Its two exact regenerated targets were
  revalidated, removed, and confirmed absent.

### M187 publication boundary

- A final fresh pruned fetch and direct hosted-ref query leave `origin/main` at
  exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e` with tree
  `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`; M186 is not its ancestor.
- GitHub reports PR #251 as the latest merged pull request and only remote
  `main` exists. The reported squash merge is still not reflected here.
- No push, PR, hosted workflow allocation, tag, release, or package
  publication occurs. Publication may be reconsidered only after the missing
  prerequisite stack is integrated or an explicit ancestry-safe integration
  plan is supplied.

### M187 explicit non-scope

- Cross-principal or unrelated-process behavior, hostile simultaneous racing,
  crash or power-loss consistency, trusted root ownership, link enumeration,
  other failure phases, ReFS/SMB/driver variation, file-ID reuse, durable
  intent, quarantine, rollback, reconciliation, typed recovery receipts,
  Windows admission, cleanup authority, or independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M186 Windows independent hard-link alias mutator ABA boundary

- **Task:** Determine whether M185's hard-link alias delete/recreate ABA remains
  observable when a distinct child process, rather than the parent
  coordinator, owns both namespace mutations.
- **Status:** Locally complete. Direction, implementation, supported-Python
  regression, concentrated/repeated Windows behavior, rendering/profiles,
  record-inclusive distribution/release rehearsal, governance, review,
  cleanup, DCO object audit, and publication-safety recheck pass. Publication
  is withheld because hosted `main` lacks M100-M185.
- **Base:** Fully locally validated M185 DCO commit
  `4dd880402a8e6f6f1e74bd69be1cd3ad0366b513`, tree
  `418e75176693f0ea30f43dac80bf0c8451f5a29e`, sole parent exact M184.
- **Branch:**
  `release/m186-windows-independent-hard-link-alias-mutator-aba-boundary`;
  exact containment removed the redundant local M185 branch name.

### M186 acceptance boundary

- Accept RFC-0169 and retain one current-host Windows-only, test-only NTFS
  observation over M173's exact coordination file and M181's unchanged
  expected-identity guardian child.
- Begin with one peer alias and shared identity/link count two. Admit the
  matching guardian, require exact `ready`, and preserve exact-name rename
  error 32.
- Launch a distinct sibling mutator child with a fixed fixture, no arguments,
  `sys.executable -I -B`, `close_fds=True`, `shell=False`, and bounded pipes.
- Require child-owned alias deletion, exact `deleted`, both children live,
  alias absence, unchanged identity/bytes, link count one, and range
  availability.
- Send one exact recreate byte; require child-owned `os.link`, exact
  `recreated`, both children live, identity/count/bytes restored through both
  names, range availability, and persistent guardian rename refusal.
- Close the mutator exactly before the guardian; require the guardian still
  live and protective, then close it exactly and verify post-close rename,
  identity, count, bytes, processes, pipes, native handles, and ranges.
- State the evidence precisely: three processes under one principal and one
  parent-owned process tree. Do not claim cross-principal, unrelated-session,
  hostile-process, simultaneous-race, or cleanup-admission evidence.
- Add no runtime API, dependency, workflow, job/allocation, permission,
  release authority, or CI change.

### M186 direction and development evidence so far

- Current Microsoft documentation retains per-file sharing across process
  contexts, multiple directory entries per hard-linked file, and deletion in
  any creation order. Current Python documentation supports the fixed,
  shell-free, close-fds child protocol used here.
- GitHub still documents one job per matrix combination; no new hosted
  allocation is justified. NIST still lists SSDF 1.2 as draft, so no
  conformance target changes.
- Exact M185 was clean. Its focused architecture/live pair passed eight tests
  in 0.51 seconds. Static governance passed; the dated check passed after an
  access-only rerun because the sandbox denied uv cache initialization before
  the first attempt reached the checker.
- The new live probe passed immediately in 0.38 seconds. The first architecture
  run correctly exposed two assertion/documentation mismatches; after narrow
  corrections, eight guards plus the live probe pass nine tests in 0.48
  seconds. All three Python files are format-, Ruff-, and strict-Pyright clean;
  strict docs pass with only the known Material notice.
- Exact CPython 3.12.13, isolated 3.13.13, and isolated 3.14.5 complete frozen
  graphics environments each pass 3,972 tests with 17 skips in 255.73, 234.74,
  and 243.61 seconds.
- The 76-file M149-M186 Windows boundary passes 279 tests with one established
  skip. A first repetition-loop expression produced no test run; the corrected
  explicit-root loop passes 20 independent M186 live invocations.
- Ten real-wgpu tests pass. Fresh one-repeat base and graphics profiles emit
  and validate two and three workloads; all eight profile-schema tests pass.
  Clockwork Arena and Agent World Builder reproduce their established state,
  capture, replay, query, and batch identities.
- The unchanged 46-package lock and exact 45-package graphics environment
  resolve. All 562 Python files are format-clean; Ruff and strict Pyright
  report zero findings; strict docs, both governance modes, and whitespace
  pass.
- Two initial builds reproduce a 361,987-byte pure wheel and 2,217,745-byte
  source archive. Primary plus 27 additional installed-wheel consumers pass.
  Two ten-artifact release stages are byte-identical and both complete smokes
  pass. Inventory finds 114 wheel and 911 source entries, no test/native
  payload in the wheel, and all five M186 source-only files once in the sdist.
- The record-inclusive separator keeps the unchanged lock/environment, all 562
  Python files, nine focused assertions, the 279-pass/one-skip Windows
  boundary, strict docs, both governance modes, and whitespace clean.
- Two final builds reproduce the unchanged 361,987-byte wheel at SHA-256
  `45b977971af0e3340b8ca3fcd3be10b84d5b6359cb3ff4d7ba9b201d9f0a11df`
  and identical 2,220,908-byte source archives at SHA-256
  `77228bd4bbb19331ffd5c422db5413c49208377c402d396a225f5ab25f1e5f45`.
  Primary wheel smoke passes; the 27 earlier consumers apply byte-for-byte.
  Two final ten-artifact stages are identical and both release smokes pass.
- Findings-first review confirms exactly 17 intended paths; unchanged runtime,
  package code, examples, scripts, workflows, metadata, dependencies, lock,
  and version; no public development-tool identity, credential assignment, or
  local path; no actionable correctness, architecture, security,
  documentation, compatibility, package, or CI-allocation finding remains.
- Exact guarded cleanup revalidated and removed 41 repository-confined,
  ignored, top-level and nested reparse-free M186 targets. Zero exact M186
  scratch target remains; older scratch and the managed environment were not
  selected.
- The final pre-commit separator keeps all three Python files static-clean,
  passes nine focused assertions, dated strict governance, and whitespace. Its
  exact regenerated test root was revalidated, removed, and confirmed absent.
- Initial DCO commit `279d135db74565dd10c4eb8e2a61727ebf16e893`, tree
  `accededba4eb41d2394ef7d7cb2104c0c75ffc66`, has sole parent exact M185,
  exactly 17 paths, one matching sign-off, truthful configured
  author/committer identity, no merge, expected `0 87` divergence, a clean
  worktree, zero exact M186 scratch, and clean connectivity apart from ordinary
  dangling objects. This factual record will be folded into the closeout
  object.
- The post-record separator passes nine focused assertions, dated strict
  governance, and whitespace; its exact test root was revalidated, removed,
  and confirmed absent.
- The pre-publication amended object `3aae3959e2dcf966cda26aa627fef65301c6470b`,
  tree `cb8edf9f9aa3f40affb2fb9ca6f07266cf91e587`, retains sole parent exact M185,
  exactly 17 paths, one matching DCO sign-off, truthful author/committer
  identity, no merge, expected `0 87` divergence, clean worktree, zero exact
  M186 scratch, and clean connectivity apart from 322 ordinary dangling
  objects. The immutable final revision is reported at closeout rather than
  embedded self-referentially here.

### M186 publication boundary

- A final fresh pruned fetch and direct hosted-ref query leave
  `origin/main` at exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e` with tree
  `c52ea4bfe80ffa3aa5883414b5ab0fd1af9d1b70`; M185 is not its ancestor.
- GitHub reports PR #251 as the latest merged pull request and no newer M186
  prerequisite integration. Only remote `main` exists.
- No push, PR, hosted workflow allocation, tag, release, or package
  publication occurs. Publication may be reconsidered only after the missing
  prerequisite stack is integrated or an explicit ancestry-safe integration
  plan is supplied.

### M186 explicit non-scope

- Cross-principal behavior, unrelated process trees or sessions, hostile or
  simultaneous racing, root authentication, link enumeration, POSIX-delete
  flags, cross-volume behavior, ReFS/SMB/driver variation, file-ID reuse,
  trusted generation provenance, failed launch, simultaneous loss, recovery,
  link-count policy, typed receipts, Windows admission, cleanup authority, or
  independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, tag,
  release, publication, or version changes.
## M185 Windows hard-link alias delete/recreate ABA boundary

- **Task:** Determine whether the same peer hard-link pathname can be deleted
  and recreated while M181's matching expected-identity guardian remains live.
- **Status:** Locally complete. Direction, implementation, supported-Python regression,
  concentrated and repeated Windows behavior, rendering/profiles/product
  slices, record-inclusive reproducible distribution/release rehearsal,
  governance, findings-first review, guarded cleanup, DCO object audit, and
  the final publication-safety recheck pass. Publication is withheld because
  hosted `main` lacks M100-M184.
- **Base:** Fully locally validated M184 DCO commit
  `5f4d1863984063fe3bc53951424a7b2b606f8f03`, tree
  `59c2cc1580d227354cdc1c902ab5be1a8dfc6847`, sole parent exact M183.
- **Branch:**
  `release/m185-windows-hard-link-alias-delete-recreate-aba-boundary`; exact
  containment removed the redundant local M184 branch name.

### M185 acceptance boundary

- Accept RFC-0168 and retain one Windows-only, test-only current-host NTFS
  observation over M173's exact coordination file and M181's unchanged
  expected-identity guardian child.
- Begin with one peer alias and link count two; require shared identity before
  guardian launch and exact-name rename error 32 after exact `ready`.
- Delete the peer alias while the guardian remains live; require absence,
  unchanged identity and bytes, link count one, and range availability.
- Recreate the same alias pathname with `os.link`; require identity and bytes
  unchanged, link count restored to two through both names, range availability,
  guardian liveness, and persistent exact-name rename refusal.
- After exact guardian close, require exact-name rename success, retained
  identity/link count/bytes through the displaced name and alias, and complete
  cleanup.
- Correct the M184 evidence classification: the mutation actor and guardian
  are separate parent and child processes under one principal. Do not claim
  cross-principal behavior or an independent third actor.
- Add no runtime API, dependency, workflow, job/allocation, permission,
  release authority, or CI change.

### M185 direction and development evidence so far

- Microsoft documents multiple directory entries per hard-linked file,
  deletion in any link-creation order, and per-file CreateFile sharing which
  remains in effect across process contexts. Python exposes standard
  `os.link` and `os.unlink`; a controlled observation was still required for
  this exact guardian interleaving.
- GitHub still documents one job per matrix combination; M185 adds no hosted
  allocation. NIST still lists SSDF 1.2 as draft, so no conformance claim
  changes.
- Exact M184 was clean. Its eight focused assertions passed in 0.65 seconds;
  static and 2026-08-29 dated strict governance returned zero findings.
- The new live probe passed immediately in 0.46 seconds. Both Python files are
  format-, Ruff-, and strict-Pyright clean; seven architecture guards plus the
  live observation pass eight tests; strict docs build passes with only the
  known Material notice.
- Exact CPython 3.12.13, isolated 3.13.13, and isolated 3.14.5 complete frozen
  graphics environments each pass 3,963 tests with 17 skips. An initial 3.13
  run without the graphics extra passed its smaller 3,953-test collection with
  18 skips and is not used for parity.
- The 74-file M149-M185 Windows boundary passes 270 tests with one established
  skip; 20 independent M185 live repetitions pass.
- Ten real-wgpu tests, fresh base/graphics profiles, eight profile-schema
  tests, Clockwork Arena, and Agent World Builder pass.
- Two builds reproduce a 361,907-byte pure wheel and 2,206,707-byte source
  archive. Primary plus 27 additional installed-wheel consumers pass. Two
  ten-artifact release stages are byte-identical and both complete smokes pass.
  Inventory finds 114 wheel and 906 source entries, no native/test/project
  payload in the wheel, and all four M185 source-only files once in the sdist.
- The record-inclusive separator passes the unchanged lock/environment, all
  static checks, eight focused assertions, the 270-pass/one-skip Windows
  boundary, strict docs, both governance modes, and whitespace.
- Two final builds reproduce the unchanged 361,907-byte wheel and identical
  2,209,784-byte source archives. Primary wheel smoke passes; the 27 earlier
  consumers apply byte-for-byte. Two final ten-artifact stages are identical
  and both complete release smokes pass.
- Findings-first review confirms exactly 18 intended paths, unchanged runtime,
  examples, scripts, fixtures, workflows, metadata, dependencies, and lock;
  no actionable code, architecture, security, documentation, compatibility,
  package, allocation, public-identity, credential, or local-path finding
  remains.
- Exact guarded cleanup revalidated and removed 42 repository-confined,
  untracked/ignored, reparse-free M185 targets. Zero exact M185 target or
  generated docs site remains; older scratch and the managed environment were
  not selected.
- The final pre-commit separator keeps both Python files static-clean, passes
  eight focused assertions, dated strict governance, and whitespace. Its exact
  regenerated test root was revalidated, removed, and confirmed absent.
- Initial DCO commit `0a9c8e224f4a30c1bbe8070435fe707a0577d84d`,
  tree `a72bd1e243921ada161322ab202ea588055349bb`, has sole parent exact M184,
  exactly 18 paths, one matching sign-off, truthful configured author/committer
  identity, no merge, expected `0 86` divergence, clean worktree, and clean
  connectivity apart from ordinary dangling objects. This factual record is
  folded into the closeout object.
- The post-record separator passes eight focused assertions, dated strict
  governance, and whitespace; its exact test root was revalidated, removed,
  and confirmed absent.
- The amended closeout object retains sole parent exact M184, exactly 18 paths,
  one matching DCO sign-off, truthful author/committer identity, no merge,
  expected `0 86` divergence, a clean worktree, zero exact M185 scratch,
  protected runtime/package/CI surfaces, and clean connectivity apart from
  ordinary dangling objects. The immutable final revision is reported at
  closeout rather than embedded self-referentially here.

### M185 publication boundary

- A fresh pruned fetch and direct remote-ref query leave hosted `origin/main`
  at exact M99 `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; it does not contain M184.
- GitHub reports PR #251 as the latest merge and no newer M185 prerequisite
  integration. The user's squash-merge notice is not reflected in this hosted
  repository.
- The final fresh pruned fetch, direct remote-ref query, merge-base check, and
  authenticated PR history again leave hosted `main` at exact M99 and confirm
  M184 is not its ancestor. PR #251 remains the latest merge and only remote
  `main` exists.
- No push, PR, hosted workflow allocation, tag, release, or package publication
  occurs. Publication may be reconsidered only after the missing prerequisite
  stack is integrated or an explicit ancestry-safe integration plan is supplied.

### M185 explicit non-scope

- Cross-principal behavior, an independent third mutation actor, unrelated
  process trees, controlled concurrent racing, root authentication, link
  enumeration, POSIX-delete flags, cross-volume behavior, ReFS/SMB/driver
  variation, file-ID reuse, trusted generation provenance, failed launch,
  simultaneous loss, recovery, link-count policy, typed receipts, Windows
  admission, cleanup authority, or independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M184 Windows hard-link alias deletion non-exclusion boundary

- **Task:** Determine whether M181's matching expected-identity guardian
  excludes deletion of a preexisting peer hard-link entry.
- **Status:** Direction, corrected implementation, supported-Python regression,
  concentrated and repeated Windows behavior, rendering/profiles/product
  slices, reproducible distribution/release rehearsal, governance, and
  findings-first review pass. Record-inclusive closure, guarded cleanup, and
  final post-record separators pass. The DCO object and fresh publication-
  safety gate pass. Publication is withheld because hosted `main` lacks
  M100-M183; one final amended-object audit remains.
- **Base:** Fully locally validated M183 DCO commit
  `e44ce6a12d61a5c1b857b88e81c45015a986df77`, tree
  `6c2a7a69ec36328182fda066b946272c4eb0a227`, sole parent exact M182.
- **Branch:**
  `release/m184-windows-hard-link-alias-deletion-boundary`; exact containment
  allowed the redundant local M183 branch name to be pruned.

### M184 acceptance boundary

- Accept RFC-0167 and retain one Windows-only, test-only current-host NTFS
  observation over M173's exact coordination file and M181's unchanged
  expected-identity guardian.
- Create one peer hard-link alias before launch; require shared identity and
  link count two before starting the matching guardian.
- Require exact-name rename error 32, then delete the peer alias with
  `Path.unlink` while the guardian remains live.
- Require alias absence, exact link-count reduction to one, retained identity
  and bytes, range availability, and persistent exact-name rename refusal.
- After exact guardian close, require exact-name rename success, retained
  identity/link count/bytes, and complete cleanup.
- Preserve the first failed all-links deletion-exclusion hypothesis as factual
  negative evidence, not root-confined ownership, link policy, recovery,
  admission, or cleanup authority.
- Add no runtime API, dependency, workflow, job/allocation, permission,
  release authority, or CI change.

### M184 direction and development evidence so far

- Microsoft documents `DeleteFileW` sharing restrictions, independent
  hard-link names, and deletion through any hard-link order. Python documents
  Windows in-use removal behavior. The broad language did not determine this
  alias-entry case, so the current-host observation remains narrow.
- GitHub still documents one job per matrix combination; M184 adds no hosted
  allocation. NIST still lists SSDF 1.2 as draft material, so no conformance
  claim changes.
- Exact M183 was clean. Its eight focused assertions passed in 0.37 seconds;
  static and 2026-08-29 dated strict governance returned zero findings.
- The first live implementation expected alias `unlink` to raise sharing
  error 32 and failed because deletion succeeded. The corrected probe retains
  that observation and passes.
- Both Python files pass Ruff format/lint and strict Pyright. Seven
  architecture guards plus the corrected live observation pass eight tests;
  strict docs build with only the known Material notice.
- Exact CPython 3.12.13 plus fresh isolated 3.13.13 and 3.14.5 each pass 3,955
  tests with 17 skips. The 72-file M149-M184 Windows boundary passes 262 tests
  with one skip; 20 corrected live repetitions pass.
- Ten real-wgpu tests, fresh base/graphics profiles, eight profile-schema
  tests, Clockwork Arena, and Agent World Builder pass with established
  deterministic identities.
- Two builds reproduce a 361,819-byte pure wheel and 2,200,431-byte source
  archive. Primary plus 27 additional installed-wheel consumers pass. Two
  ten-artifact release stages are byte-identical and both complete smokes pass.
- Findings-first review finds no actionable defect, credential-shaped content,
  public development-tool identity, protected-surface drift, allocation
  expansion, or package-boundary issue across exactly 16 intended paths.
- The record-inclusive separator passes the unchanged lock/environment, all
  static checks, 13 focused assertions, the 262-pass/one-skip Windows boundary,
  strict docs, both governance modes, and whitespace.
- Two final builds reproduce the same fully consumed wheel and a 2,201,207-byte
  source archive. Primary wheel smoke passes; the earlier 27 consumer results
  apply byte-for-byte. Two final ten-artifact stages are identical and both
  complete release smokes pass.
- Exact guarded cleanup removed 35 generated targets under the ordinary
  identity and revalidated/removed the 13 complementary-ACL targets under the
  elevated identity. Zero exact M184 target remains.
- The final separator keeps both Python files static-clean, passes 13 focused
  assertions, strict docs, dated strict governance, and whitespace. Its exact
  two outputs were revalidated and removed at the complementary ACL boundary.
- The final post-record metadata separator passes 13 assertions, dated strict
  governance, and whitespace; its exact test root was guarded and removed.
- Final pre-commit audit confirms exactly 16 intended paths, unchanged
  protected M183/runtime/package/CI surfaces, zero public-identity/path/
  credential match, zero exact scratch, neutral branch hygiene, truthful Git
  identity, exact M183 ancestry, and clean object connectivity.
- Initial DCO commit `426ccd31707461a1c4cf8ccfeb29780ac56a3dd0`,
  tree `6666e414a80aa863705e6c9612153f416329fa16`, has sole parent exact M183,
  exactly 16 paths, one sign-off, matching configured author/committer
  identity, no merge, expected `0 85` divergence, clean worktree, and clean
  object connectivity. This factual record is folded into the closeout object.

### M184 publication boundary

- A fresh pruned fetch leaves hosted `origin/main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; it does not contain M183.
- GitHub reports no open PR, PR #251 as the latest merge, and only remote
  `main`. Publishing M184 would expose the absent M100-M183 prerequisite stack.
- No push, PR, hosted workflow allocation, tag, release, or package publication
  occurs. Publication may be reconsidered after the missing prerequisite stack
  is integrated or an explicit ancestry-safe integration plan is supplied.

### M184 explicit non-scope

- Cross-principal behavior, an independent third mutation actor, unrelated
  process trees, root authentication, link enumeration,
  POSIX-delete flags, cross-volume behavior, ReFS/SMB/driver variation,
  file-ID reuse, trusted generation provenance, failed launch, simultaneous
  loss, recovery, link-count policy, typed receipts, Windows admission,
  cleanup authority, or independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M183 Windows post-admission hard-link creation boundary

- **Task:** Determine whether M181's matching expected-identity guardian
  prevents the file from gaining a new hard-link entry after admission.
- **Status:** Direction, implementation, supported-Python regression,
  concentrated Windows behavior, repeated live behavior, graphics/profiles,
  vertical slices, reproducible package/release rehearsal, strict governance,
  record-inclusive separators, findings-first review, and guarded cleanup pass.
  The DCO object, fresh publication-safety gate, and final amended-object shape
  and connectivity pass. Publication is withheld because hosted `main` lacks
  M100-M182.
- **Base:** Fully locally validated M182 DCO commit
  `b9d02dbdfbb13f290079970305e2e1c5c6cd783f`, tree
  `e27c14aa60b7ac9fa63af769e51d5344e5cca72a`, sole parent exact M181.
- **Branch:** `release/m183-windows-post-admission-hard-link-creation-boundary`;
  exact containment allowed the redundant local M182 branch name to be pruned.

### M183 acceptance boundary

- Accept RFC-0166 and retain one Windows-only, test-only current-host NTFS
  observation over M173's exact coordination file and M181's unchanged
  expected-identity guardian.
- Begin with no peer alias and require link count one before guardian launch.
- Admit the matching guardian, require exact-name rename error 32, then create
  one peer alias with standard-library `os.link` while the guardian remains
  live.
- Require the same identity through both handles, exact link-count growth to
  two, exact bytes, range availability through both names, and persistent
  exact-name rename refusal.
- After exact guardian close, require exact-name rename success, retained
  identity/link count/bytes through both names, and complete cleanup.
- Interpret the result as post-admission link-set non-exclusion, not
  root-confined ownership, link policy, recovery, admission, or cleanup
  authority.
- Add no runtime API, dependency, workflow, job/allocation, permission,
  release authority, or CI change.

### M183 direction and development evidence so far

- Microsoft documents hard links as same-volume directory entries,
  `CreateHardLinkW` as adding an entry, `FILE_LINK_INFORMATION` as requiring no
  specific file access right, and `BY_HANDLE_FILE_INFORMATION` as exposing
  the current link count. Python exposes `os.link` directly.
- GitHub still documents one job per matrix combination; M183 adds no hosted
  allocation. NIST still lists SSDF 1.2 as draft material, so no conformance
  claim changes.
- Exact M182 is clean. Its eight focused assertions pass in 0.40 seconds;
  static and 2026-08-29 dated strict governance return zero findings.
- The first live M183 observation passes: link count grows from one to two
  while the guardian remains live and continues protecting its exact name.
- Ruff and strict Pyright pass both new Python files. Eight combined
  architecture/live assertions pass, and strict docs build with only the known
  Material notice. One mechanical architecture wrap was applied.
- Exact CPython 3.12.13, fresh isolated 3.13.13, and fresh isolated 3.14.5 each
  pass 3,947 tests with 17 skips. The 70-file M149-M183 Windows boundary passes
  254 tests with one skip, and 20 repeated live observations pass.
- Ten real-wgpu tests, base/graphics profiles, eight profile-schema tests,
  Clockwork Arena, and Agent World Builder pass with established identities.
- Two builds reproduce a 361,753-byte pure wheel and 2,191,922-byte source
  archive. The primary and all 27 additional installed-wheel consumers pass;
  two ten-artifact release stages are byte-identical and both release smokes
  pass.
- Findings-first review finds no actionable defect, high-confidence
  credential-shaped content, protected-surface change, allocation expansion,
  or package-boundary issue across exactly 16 intended paths.
- The record-inclusive separator passes. Two final builds reproduce the same
  fully consumed pure wheel and a 2,192,904-byte source archive. Both final
  ten-artifact release stages are byte-identical and pass complete smoke.
- Forty-three exact generated M183/site targets were guarded. The ordinary
  pass removed 32; an elevated revalidation removed the 11 pytest-owned roots
  at the complementary ACL boundary. Zero exact target remains.
- The final pre-commit separator keeps both Python files static-clean, passes
  13 focused assertions, strict docs, dated strict governance, and whitespace.
  Its regenerated site and one pytest-owned root were revalidated, removed,
  and confirmed absent.
- Initial DCO commit `271cb353d1497e81c069c594c807122ba5636e1c`, tree
  `b4ece8c1f47cc6815bb3d9f43a190bca0b6f1f23`, has sole parent exact M182,
  exactly 16 paths, one sign-off, matching configured author/committer identity,
  no merge, a clean worktree, and clean object connectivity.
- A fresh pruned fetch leaves hosted `origin/main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; it does not contain M182.
  There is no open PR and no remote branch besides `main`, so M183 is not
  pushed and no PR or hosted allocation is created.

### M183 publication boundary

- Automatic publication is authorized only when the hosted base contains the
  prerequisite local stack. That condition is false for M183.
- Publishing the current head would expose M100-M183 as one unrelated stack
  over hosted M99, defeating the milestone and review boundary.
- No push, PR, hosted workflow allocation, tag, release, or package publication
  occurs. Publication may be reconsidered after the missing prerequisite stack
  is integrated or an explicit ancestry-safe integration plan is supplied.

### M183 explicit non-scope

- Another process or principal, root authentication, link enumeration, alias
  deletion, cross-volume behavior, ReFS/SMB/driver variation, file-ID reuse,
  trusted generation provenance, failed launch, simultaneous loss, recovery,
  link-count policy, typed receipts, Windows admission, cleanup authority, or
  independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## M182 Windows hard-link alias non-exclusion boundary

- **Task:** Determine whether M181's matching expected-identity guardian also
  excludes namespace mutation through a preexisting hard-link alias.
- **Status:** Direction, implementation, supported-Python regression,
  concentrated Windows behavior, graphics/profiles/vertical slices,
  reproducible distribution/release rehearsal, strict governance, and
  findings-first review pass. The first live run falsified the proposed
  all-names protection guarantee; the corrected negative boundary passes.
  Record-inclusive separators, guarded cleanup, initial DCO commit, and the
  publication-safety gate pass. Publication is withheld because hosted
  `main` lacks M100-M181. Final amended-object shape and connectivity pass.
- **Base:** Fully locally validated M181 DCO commit
  `d808b94102acd576c7ac8e458fe119692d614c4e`, tree
  `109ed76a0c95d80b3f0cf8c002ef543d077d4b3f`, sole parent exact M180.
- **Branch:** `release/m182-windows-hard-link-alias-non-exclusion-boundary`;
  renaming the active branch removed the inaccurate protection claim and left
  no redundant local predecessor branch.

### M182 acceptance boundary

- Accept RFC-0165 and retain one Windows-only, test-only current-host NTFS
  observation over M173's exact coordination file and M181's unchanged
  expected-identity guardian.
- Create one preexisting peer hard link; require equal `FILE_ID_INFO` and link
  counts of at least two before guardian launch.
- Require the exact opened coordination name to reject rename with sharing
  error 32 while the preexisting alias rename succeeds and the guardian stays
  live.
- Require the moved alias to retain identity and link count, byte-range
  ownership to remain available through both names, and a second exact-name
  rename to remain refused.
- After exact guardian close, require exact-name rename success, retained
  identity/link count/bytes through both remaining names, and complete cleanup.
- Interpret the result as hard-link alias non-exclusion, not root-confined
  ownership, link policy, recovery, admission, or cleanup authority.
- Add no runtime API, dependency, workflow, job/allocation, permission,
  release authority, or CI change.

### M182 direction and development evidence so far

- Microsoft documents hard links as multiple same-volume directory entries
  for one file, per-file CreateFile sharing, handle link counts, and pathname
  rename/delete operations. GitHub matrix and NIST SSDF status were also
  checked on 2026-08-29; neither supports a new CI allocation or conformance
  claim.
- Exact M181 was clean. Its ten focused assertions passed; static and dated
  strict governance returned zero findings across three objectives, seven
  requirements, and four work items.
- The first live M182 run failed because the preexisting alias rename did not
  raise the expected error. The correction preserved that result as the
  boundary and renamed the branch, source, tests, and decision language.
- The corrected live probe passes. Ruff and strict Pyright pass both new
  Python files. Eight combined architecture/live assertions pass, and strict
  documentation builds with only the known Material notice.
- Exact CPython 3.12.13, fresh isolated 3.13.13, and fresh isolated 3.14.5
  each pass 3,939 tests with 17 skips. A retained older 3.13 environment passed
  its collected 3,929 tests with 18 skips but is diagnostic only; the fresh
  frozen run is the accepted compatibility result.
- The 34-file M149-M182 architecture selection plus 34 Windows cache-cleanup
  integration modules passes 246 tests with one established skip. Twenty
  independent M182 live invocations pass in 0.601 to 0.675 seconds.
- Ten real-wgpu tests, fresh base/graphics profiles, all eight profile-schema
  tests, Clockwork Arena, and Agent World Builder pass with established
  deterministic identities.
- Two builds reproduce a 361,686-byte pure wheel at SHA-256
  `46418eb0a65e35b9fbcd3ce09207bc4985ecefa02bde7e9ab014f87367a09938`
  and a 2,182,678-byte source archive at SHA-256
  `7c166b609b2547106d835b6ef00fc98d93c0ea26850ddc53e1c9e69908839e16`.
  Primary smoke, all 27 additional installed-wheel consumers, two
  byte-identical ten-artifact release stages, and both release smokes pass.
- The wheel has 114 entries and no native, WASM, bytecode, hidden project
  record, or M182 test source. The 894-entry source archive contains all four
  new M182 source records exactly once.
- Static and dated strict governance pass with zero findings. The focused
  metadata/security review passes 13 assertions and finds no public
  development-tool identity, credential assignment, local path, protected
  runtime/package/CI change, or remaining actionable finding.

### M182 explicit non-scope

- Root authentication, link enumeration, post-admission link creation, alias
  deletion, cross-volume behavior, ReFS/SMB/driver variation, file-ID reuse,
  trusted generation provenance, failed launch, simultaneous loss, recovery,
  link-count policy, typed receipts, Windows admission, cleanup authority, or
  independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

### M182 publication boundary

- Initial DCO commit `f70689b623a7ec432351864e06f2db468761c135`, tree
  `c3c6080b732a33a8dc903e379839d4e19ad13a26`, has sole parent exact M181,
  exactly 16 intended paths, one sign-off, matching configured maintainer
  identity, no merge, expected `0 83` divergence from local M99 `main`, a
  clean worktree, and clean object connectivity. This factual record is
  incorporated by one final amendment.
- A fresh pruned fetch leaves hosted `origin/main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; it does not contain M181.
  GitHub reports no open PR, PR #251 as the latest merge, and only remote
  `main`. M182 is not pushed and no PR or hosted allocation is created while
  M100-M181 remain unpublished prerequisites.
- Publication must not create a workflow, job, matrix allocation, redundant
  predecessor branch, tag, release, or package publication.

## M181 Windows expected-identity guardian admission

- **Task:** Determine whether a Windows guardian can admit the intended
  coordination object and reject a preexisting pathname replacement by
  comparing a caller-supplied expected identity on the same protecting handle.
- **Status:** Direction, implementation, supported-Python regression,
  concentrated Windows behavior, rendering, profiles, vertical slices,
  reproducible distribution/release rehearsal, governance, findings-first
  review, record-inclusive separators, guarded cleanup, initial DCO commit,
  and publication-safety gates pass. Publication is withheld because hosted
  `main` lacks M100-M180; one factual amendment and final object audit remain.
- **Base:** Fully locally validated M180 DCO commit
  `d19e03ec9f83134d72086b93ebd988a5cade8f0d`, tree
  `bffe676c2da214b77c757f914372ba351712da18`, sole parent exact M179.
- **Branch:** `release/m181-windows-expected-identity-guardian-admission`;
  exact containment allowed the redundant local M180 branch to be pruned.

### M181 acceptance boundary

- Accept RFC-0164 and retain one Windows-only, test-only child fixture plus two
  current-host observations over M173's exact ordinary coordination file.
- Open with no delete sharing, reject an inheritable or reparse handle, and
  compare `FILE_ID_INFO` on that same already protecting handle before
  emitting `ready`.
- Admit an exact match, require direct rename error 32 and exact exclusive
  range availability, then require exact close, successful rename, retained
  identity and bytes, and complete cleanup.
- After M174 pre-launch substitution, reject the replacement with exact
  `identity_mismatch`, close before reporting it, settle boundedly, then
  require rename and range availability plus both retained identities and
  exact bytes.
- Interpret the result only as same-handle expected-identity admission
  evidence. It is not trusted identity provenance, durable storage,
  generation authority, authenticated launch, recovery, Windows admission,
  or cleanup authority.
- Add no runtime API, dependency, workflow, job/allocation, permission,
  release authority, or CI change.

### M181 direction evidence

- Microsoft documents `FILE_ID_INFO` as a volume serial plus 128-bit identifier
  for identifying a file on one computer, and documents querying it through
  `GetFileInformationByHandleEx`.
- Microsoft documents that `CreateFileW` sharing modes remain in force until
  the owning handle closes. Denying delete sharing before identity comparison
  protects the same handle that may be admitted.
- GitHub documents matrix expansion behavior. M181 uses only the existing
  Windows suite and creates no hosted allocation.
- NIST still lists SSDF 1.2 as draft material. M181 makes no new conformance
  claim.

### M181 local validation evidence so far

- Exact M180 was clean. Its nine focused assertions passed in 0.99 seconds;
  static and 2026-08-29 dated strict governance returned zero findings.
- Eight architecture guards plus the two live cases pass ten assertions. An
  initial unused import finding and one mechanical architecture format request
  were corrected; all three new Python files then passed Ruff and strict
  Pyright.
- The unchanged 46-package lock and 45-package graphics environment validate.
  All 551 Python files pass formatting, Ruff, and strict Pyright.
- An initial full baseline run passed 3,930 tests with 17 skips and exposed one
  inherited M180 metadata-neutrality failure. Three historical evidence
  phrases were neutralized; the exact 15-case regression group then passed.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 each pass 3,931 tests with 17
  skips. Twenty independent two-case M181 invocations pass all 40 cases in
  0.45 to 0.49 seconds per invocation.
- Ten real-wgpu tests, fresh base/graphics profiles, Clockwork Arena, and Agent
  World Builder pass with their established deterministic outputs.
- Two initial builds reproduce a 361,611-byte pure wheel at SHA-256
  `e1ec8690060d7c3fc5711a42f7a72a31643b0900c76ee215790f8e1f78cfb0fd`
  and a 2,169,797-byte source archive at SHA-256
  `52a598705cd832db2aa76fa91eb12a21164588f76501430fe9417412a6e9f848`.
  Wheel smoke, two byte-identical ten-artifact release stages, and both release
  smokes pass. Inventory has 114 wheel and 890 source entries, no native,
  WASM, or bytecode entry, no M181 test source in the wheel, and all five new
  M181 sources exactly once in the source archive.
- Strict docs built in 2.61 seconds with only the known Material notice.
  Static and dated strict governance each return zero findings across three
  objectives, seven requirements, and four work items.
- Findings-first review found no remaining runtime, architecture, security,
  documentation, compatibility, package-boundary, or allocation defect.
  Runtime, examples, scripts, workflows, metadata, dependencies, lock, and
  the exact M180 boundary remain protected.

### M181 publication boundary

- Initial DCO commit `70cd29751405b6cbc7b23b446216d258d043009d`, tree
  `4069c350a3bd8dee1110ce12b191cf1f95aae91c`, has sole parent exact M180,
  exactly 17 paths, one sign-off, matching configured maintainer identity, no
  merge, expected `0 82` divergence, and a clean worktree. This factual record
  is incorporated by one final amendment.
- A fresh pruned fetch leaves hosted `origin/main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; it does not contain M180.
  GitHub reports no open PR, PR #251 as the latest merge, and only remote
  `main`. M181 is not pushed and no PR or hosted allocation is created while
  M100-M180 remain unpublished prerequisites.
- Publication must not create a workflow, job, matrix allocation, redundant
  predecessor branch, tag, release, or package publication.

### M181 explicit non-scope

- Trusted expected-identity provenance or storage, durable generation state,
  guardian discovery/election/authentication, failed launch, simultaneous
  loss, hostile handles, arbitrary process trees, mapped views, filesystem
  variation, use-time revalidation, policy, receipts, cleanup authority,
  complete Windows admission, or independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, tag,
  release, publication, or version changes.

## Earlier task: M180 Windows zero-owner guardian restart boundary

- **Task:** Distinguish benign guardian restart over an unchanged coordination
  identity from restart after pathname substitution during a zero-owner
  interval.
- **Status:** Direction, implementation, supported-Python regression,
  concentrated/repeated Windows behavior, rendering, profiles, vertical
  slices, reproducible distribution/release rehearsal, governance,
  findings-first review, record-inclusive source closure, and scope/hygiene
  gates pass. Guarded cleanup, final factual separators, initial DCO commit,
  and publication-safety gates pass. Publication is withheld because hosted
  `main` lacks M100-M179; one factual amendment and object audit remain.
- **Base:** Fully locally validated M179 DCO commit
  `2d6312fbc59358f8ef080f5b335a815c6ffe2d15`, tree
  `9246c860dd6b18c4615c761fbeff0f5b619dd03c`, sole parent exact M178.
- **Branch:** `release/m180-windows-zero-owner-guardian-restart-boundary`;
  exact containment allowed the redundant local M179 branch to be pruned.

### M180 acceptance boundary

- Accept RFC-0163 and retain two Windows-only, test-only current-host
  observations after M178's unchanged guardian is abruptly killed and reaped.
- In the mutation-free case, require the exposed pathname to retain the
  original `FILE_ID_INFO`; require a later guardian to reacquire that identity,
  refuse substitution, and leave the cooperative range available.
- In the mutation case, require M174 substitution during the zero-owner
  interval; require the later guardian to attach to the replacement identity,
  refuse a second direct rename with error 32, and leave the range available.
- After exact close, require rename/substitution success, original and
  replacement identity separation, exact bytes, and complete process, stream,
  handle, and range cleanup without retry or sleep.
- Interpret the result only as a restart-boundary observation. It is not crash
  recovery, generation authority, election, trusted placement, startup
  authentication, continuity, Windows admission, or cleanup authority.
- Add no fixture, runtime adapter, guardian/lock API, dependency, workflow,
  job/allocation, permission, release authority, or CI change.

### M180 direction evidence

- Microsoft documents that `CreateFileW` share modes persist only while the
  owning handle remains open and that `MoveFileExW` acts on pathnames.
- Microsoft documents `TerminateProcess` as asynchronous, so each zero-owner
  observation begins only after M176's bounded wait completes.
- GitHub documents that each matrix combination creates a job. M180 uses only
  the existing Windows suite and creates no hosted allocation.
- NIST still lists SSDF 1.2 as draft material. M180 retains the existing
  governance posture without a new conformance claim.

### M180 local validation evidence so far

- Exact M179 is clean. Its seven focused assertions pass in 1.00 seconds;
  static and 2026-08-29 dated strict governance return zero findings.
- Two new live cases and seven architecture guards pass nine assertions. The
  first documentation registration gate correctly found the missing security
  navigation entry; after adding it, the focused group passed in 1.03 seconds.
- The unchanged 46-package lock and 45-package graphics environment validate.
  All 548 Python files pass formatting, Ruff, and strict Pyright.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 each pass 3,921 tests with 17
  skips. A first 3.13 run encountered only inherited shared scratch ACL errors
  and was stopped; the accepted 3.13/3.14 runs use distinct confined roots.
- The 64-module M149-M180 boundary passes 228 tests with one established skip.
  Twenty independent two-case central probes pass 40 cases in 0.89 to 0.95
  seconds per invocation.
- Ten real-wgpu tests, fresh base/graphics profiles, eight profile-validator
  tests, Clockwork Arena, and Agent World Builder pass with established
  deterministic identities.
- Two initial builds reproduce a 361,539-byte pure wheel and a 2,158,613-byte
  source archive. Isolated wheel smoke, two byte-identical ten-artifact release
  stages, and both release smokes pass. Inventory has 114 wheel and 885 source
  entries, no native/WASM/bytecode or hidden development root, no M180 wheel
  source, and all four new M180 sources in the archive.
- Findings-first review found no runtime defect and strengthened the
  architecture guard to hash every reused historical helper. The corrected
  nine-case group passes in 0.98 seconds; strict docs build in 2.70 seconds.
- Static and 2026-08-29 dated strict governance each return zero findings
  across three objectives, seven requirements, and four work items.
- The record-inclusive separator keeps the 46-package lock current, all 548
  Python files static-clean, all nine focused assertions passing in 0.98
  seconds, the M149-M180 boundary at 228 passes/one skip in 14.88 seconds,
  strict docs and whitespace passing, and both governance modes at zero
  findings.
- Two final record-inclusive builds reproduce the unchanged 361,539-byte wheel
  and an identical 2,161,961-byte source archive. Primary wheel smoke, two
  byte-identical ten-artifact release stages, and both release smokes pass.
- Exact scope is 16 intended paths. Protected runtime/package/CI/M179/helper
  surfaces have zero diff; corrected added/new-content public-identity,
  local-path, and credential-assignment scans return zero matches. The retired
  retired hidden development roots and their root guidance file remain absent.
- Fifty-one exact generated M180/pytest/docs targets were independently
  confined and checked for tracked content, ignore status, and recursive
  reparse points. Ordinary cleanup removed 37; an approved, fully revalidated
  retry removed the 14 split-ACL targets. No exact target remains.
- After recording cleanup, both Python files remain static-clean; nine focused
  assertions pass in 1.03 seconds; strict docs build in 2.72 seconds; dated
  governance and whitespace pass. The regenerated docs site and exact test
  root were independently revalidated, removed, and confirmed absent.

### M180 publication boundary

- Initial DCO commit `a9ff96c7265872b149cfb09cc89500b8ad8d52d7`, tree
  `217559d9a39475210572c9aadcd4d862716eead6`, has sole parent exact M179,
  exactly 16 paths, one sign-off, matching configured maintainer identity, no
  merge, expected `0 81` divergence, and a clean worktree. This factual record
  is incorporated by one final amendment.
- A fresh pruned fetch leaves hosted `origin/main` at exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; it does not contain M179.
  GitHub reports no open PR, PR #251 as the latest merge, and only remote
  `main`. M180 is not pushed and no PR or hosted allocation is created while
  M100-M179 remain unpublished prerequisites.
- Publication must not create a workflow, job, matrix allocation, redundant
  predecessor branch, tag, release, or package publication.

### M180 explicit non-scope

- Crash recovery, durable identity/generation state, guardian election or
  authentication, failed restart launch, simultaneous loss, trusted root
  placement, complete participant admission, hostile prior handles, arbitrary
  process trees, mapped views, filesystem variation, use-time revalidation,
  policy, receipts, cleanup authority, or independent-host proof.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, fixture,
  dependency, native-extension, compiler, workflow, permission, CI-allocation,
  tag, release, publication, or version changes.

## Earlier task: M179 Windows overlapping guardian rotation

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
