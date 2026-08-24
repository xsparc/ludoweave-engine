# Current task

- **Task:** M110 - retain sample-member timestamp compatibility.
- **Status:** Primary-source research, supported-runtime/producer probes, the
  rejected exact-profile red and implementation checkpoint, complete-
  architecture incompatibility proof, corrected decision contract, RFC-0093,
  and aligned documentation are complete. Corrected focused, architecture,
  complete supported-Python, graphics/profile/vertical, and initial artifact/
  release validation, findings-first review, final separators, history/object/
  hosted-state audit, and post-audit validation pass. Commit and cleanup remain.
- **Base:** Fully locally validated M109 DCO commit
  `42671751f5243e52ec3db7cb6737b2ada87d5e01`, tree
  `9b799a8ef957efd93acbb8fc1cd8aad7c2cf6b68`, with sole parent exact M108.
  The stack remains unpublished under the existing automated-review identity
  hold.

## Acceptance boundary

- Retain alternate MS-DOS member timestamps when the established M98 local/
  central consistency and all later structural, metadata, profile, inventory,
  and content checks pass.
- Keep the fixed producer's `(1980, 1, 1, 0, 0, 0)` reproducibility contract
  without turning it into verifier admission policy.
- Add RFC-0093, one focused architecture compatibility contract, and aligned
  public, security, architecture, release, roadmap, maintainer, and factual
  project records.
- Keep workflows, runner allocation, actions, permissions, credentials,
  dependencies, lock, version, verifier/runtime scripts, sample producer,
  runtime package/API, release authority, tags, releases, publication, and
  public branch state unchanged.

## Evidence so far

- A nonzero-volume candidate was rejected because unchanged M109 already rejects
  it through M82's split-volume gate; no duplicate policy remains.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 expose alternate timestamp
  `(2026, 8, 25, 12, 34, 56)` and read its payload, while the fixed producer's
  50 members expose only `(1980, 1, 1, 0, 0, 0)`.
- The initial exact-profile contract failed ten targeted assertions against
  M109, then passed all 21 on exact 3.12.13/3.13.13/3.14.5 in 0.26/0.62/0.61
  seconds after implementation; strict docs and static checks also passed.
- The complete architecture gate then failed 22 established assertions with
  1,507 passes and one skip in 10.12 seconds. Regressions covered valid bounded
  extraction, portable paths, atomic staging, inventory, owned snapshots,
  decompression, and diagnostic precedence. The exact classifier and its
  contract were removed rather than rewriting historical compatibility.
- `scripts/smoke_release.py` is byte-identical to M109. The corrected contract
  requires alternate and mixed timestamp admission, preserves M98 consistency,
  and protects the unchanged workflow, producer, dependency, and runtime
  boundaries.

## Explicit non-scope

- No timezone or UTC conversion, verifier wall-clock lookup, daylight-saving
  inference, extended-timestamp parsing, normalization, raw ZIP parsing,
  payload inspection, repair, or general archive-security claim.
- No workflow, allocation, dependency, producer, runtime package/API, native/
  WASM, version, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Create the standalone local DCO commit and perform bounded M110 scratch
  cleanup. Publication remains held.
