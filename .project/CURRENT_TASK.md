# Current task

- **Task:** M111 - retain sample-member permission compatibility.
- **Status:** M110 commit/cleanup verification, primary-source research,
  supported-runtime/producer probing, corrected deliberate-red contract,
  RFC-0094, aligned documentation, focused/architecture/static/complete
  supported-Python, graphics/profile/vertical, and initial artifact/release
  validation are complete. Findings-first review and review-inclusive artifact/
  release validation, final source separators, and the precommit history/
  hosted-state audit are also complete. The 15-path diff is qualified and ready
  for standalone commit closeout.
- **Base:** Fully locally validated M110 DCO commit
  `e7730664c4486cdf1fa0f171bf057cb146db7aa3`, tree
  `d88e6ca2c85012b8fdb785ea7547224c46af87a5`, with sole parent exact M109.
  The stack remains unpublished under the existing automated-review identity
  hold.

## Acceptance boundary

- Retain missing-type and regular-file permission variants when M65's symlink/
  non-regular file-type policy and all later checks pass.
- Keep the fixed producer's UNIX regular-file mode `0100644` reproducibility
  contract without turning it into verifier admission policy.
- Add RFC-0094, one focused architecture compatibility contract, and aligned
  public, security, architecture, release, roadmap, maintainer, and factual
  project records.
- Keep workflows, runner allocation, actions, permissions, credentials,
  dependencies, lock, version, verifier/runtime scripts, sample producer,
  runtime package/API, release authority, tags, releases, publication, and
  public branch state unchanged.

## Evidence so far

- M110 is exact standalone DCO commit `e7730664c4486cdf1fa0f171bf057cb146db7aa3`
  with tree `d88e6ca2c85012b8fdb785ea7547224c46af87a5`, sole parent M109,
  exact maintainer identity, one sign-off, and 15 intended paths.
- The first M110 cleanup guard rejected a directory-property mismatch before
  deletion. The corrected absolute-parent/no-reparse guard removed exactly eight
  audited ignored targets and left zero M110 scratch plus a clean worktree.
- PKWARE defines external attributes relative to the encoded creating host.
  Python exposes public `ZipInfo.external_attr`; M65 already uses only its upper
  file-type bits to reject symlinks and encoded non-regular members.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 expose/read five UNIX regular-file
  permission variants and missing-type mode `0600`. The fixed producer's 50
  members expose only create system `3`, external attribute `2175008768`, and
  mode `0100644`.
- The first red contract correctly revealed that CPython normalizes an all-zero
  external attribute to mode `0600`; that synthetic preservation case was
  removed. The corrected exact 3.12.13 contract passes 15 existing behavior,
  file-type, inventory, producer, source, and protected-surface assertions and
  fails only the intended missing-documentation assertion in 0.51 seconds.
- `scripts/smoke_release.py` remains byte-identical to M110/M109. The decision
  adds no runtime classifier or permission restoration.

## Explicit non-scope

- No exact external-attribute profile, host-semantics expansion, permission
  allowlist/normalization, chmod, umask/ACL/ownership/special-bit policy, raw ZIP
  parsing, payload inspection, repair, or general archive-security claim.
- No workflow, allocation, dependency, producer, runtime package/API, native/
  WASM, version, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Create and verify the standalone DCO commit, then perform bounded scratch
  cleanup.
