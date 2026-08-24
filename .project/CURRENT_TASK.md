# Current task

- **Task:** M112 - retain sample-member creating-system compatibility.
- **Status:** M111 commit/cleanup verification, primary-source research, exact
  supported-runtime/producer probing, and a deliberate-red compatibility
  contract are complete. RFC-0095, aligned records, and exact three-runtime
  focused, static, architecture, docs, and complete-suite qualification are
  complete. Graphics/profile/vertical and initial artifact/release gates also
  pass. Findings-first review corrected two weak test assertions and now has no
  actionable finding. Review-inclusive reproducibility, isolated-wheel,
  ten-artifact release, complete release-smoke, and archive-hygiene gates pass;
  the final source separator, local/hosted history audit, and post-audit record
  separator pass. The standalone commit and bounded scratch cleanup remain.
- **Base:** Fully locally validated M111 DCO commit
  `fb577c5d414653fe2a6f66841bda8d86c8f306f7`, tree
  `833039101e454e72872d203605a266bce7c9d82c`, with sole parent exact M110.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Retain parser-exposed creating-system markers when M65's symlink/non-regular
  file-type policy and every later check pass.
- Keep the fixed producer's creating system `3`, creation version `20`, and UNIX
  regular-file mode `0100644` reproducibility contract without turning the host
  marker into verifier admission policy.
- Add RFC-0095, one focused architecture compatibility contract, and aligned
  public, security, architecture, release, roadmap, maintainer, and factual
  project records.
- Keep workflows, runner allocation, actions, permissions, credentials,
  dependencies, lock, version, verifier/runtime scripts, sample producer,
  runtime package/API, release authority, tags, releases, publication, and
  public branch state unchanged.

## Evidence so far

- M111 is exact standalone DCO commit
  `fb577c5d414653fe2a6f66841bda8d86c8f306f7`, tree
  `833039101e454e72872d203605a266bce7c9d82c`, sole parent M110, exact
  maintainer identity, one sign-off, and 15 intended paths. Nine audited M111
  scratch targets were removed and zero remain.
- PKWARE defines creating-system markers as external-attribute compatibility
  hosts. CPython defaults public `ZipInfo.create_system` to `0` on Windows and
  `3` elsewhere; M108 already demonstrated 54 established regressions from an
  exact host-`3` rule.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 preserve and read representative
  markers `0`, `3`, `10`, `19`, and `255`. The fixed producer remains exact at
  creation version `20`, host `3`, and mode `0100644` for all 50 members.
- The format/Ruff-clean exact 3.12.13 red contract passes 15 existing behavior,
  file-type, inventory, producer, source, and protected-surface assertions and
  fails only the intended missing-documentation assertion in 0.50 seconds.
- `scripts/smoke_release.py` remains byte-identical to M111/M110. The decision
  adds no runtime classifier or archived-attribute application.
- The review-inclusive wheel remains 277,458 bytes at SHA-256
  `d19962155511815c3b165236af6a99f354511cca497ee5145af0b96524dfd897`;
  the reproducible 1,518,358-byte source archive is
  `be95c1d0b91ea8694bddd7071bb52ea36ac8cfc3b735722d778332a3595c1cd5`.
  The wheel/release smokes and 94/590-entry hygiene audit pass.

## Explicit non-scope

- No creating-system allowlist or exact profile, host-specific external-
  attribute interpretation, attribute normalization, permission restoration,
  chmod, ACL/ownership policy, raw ZIP parsing, payload inspection, repair, or
  general archive-security claim.
- No workflow, allocation, dependency, producer, runtime package/API, native/
  WASM, version, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Run the final post-review source separator, history/hosted-state audit,
  standalone DCO commit, and bounded scratch cleanup.
