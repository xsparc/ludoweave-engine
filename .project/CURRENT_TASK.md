# Current task

- **Task:** M113 - retain sample-member compression-method compatibility.
- **Status:** M112 commit/cleanup verification, primary-source research, exact
  supported-runtime/producer probing, and a deliberate-red compatibility
  contract are complete. RFC-0096, aligned public/project records, and the
  focused implementation checkpoint pass. Supported-runtime focused, static,
  architecture, docs, complete-suite, graphics, profile, and vertical-slice
  qualification pass. Initial artifacts pass; findings-first review corrected
  one weak fixture and now has no actionable finding. Review-inclusive
  artifacts, the final source separator, and history/hosted-state audit pass.
  The post-audit separator passes. The standalone commit and cleanup remain.
- **Base:** Fully locally validated M112 DCO commit
  `b3c9406c382dc91802a424e308801be2ef1b100e`, tree
  `2cfd7f3bb027736cc6a0b755a182e8300bcfb68d`, with sole parent exact M111.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Retain M64's exact stored/deflated sample-member allowlist when every
  established check passes, including M95 local/central method agreement.
- Keep the fixed producer's deflate method `8`, version `20`, and zero flags
  reproducibility contract without adding an exact deflate-only verifier
  profile.
- Add RFC-0096, one focused architecture compatibility contract, and aligned
  public, security, architecture, release, roadmap, maintainer, and factual
  project records.
- Keep workflows, runner allocation, actions, permissions, credentials,
  dependencies, lock, version, verifier/runtime scripts, sample producer,
  runtime package/API, release authority, tags, releases, publication, and
  public branch state unchanged.

## Evidence so far

- M112 is exact standalone DCO commit
  `b3c9406c382dc91802a424e308801be2ef1b100e`, tree
  `2cfd7f3bb027736cc6a0b755a182e8300bcfb68d`, sole parent M111, exact
  maintainer identity, one sign-off, 15 intended paths, and `0 13` divergence.
  Nine audited M112 scratch targets were removed and zero remain.
- PKWARE defines compression as optional, method `0` as stored, and method `8`
  as deflated. Python exposes and reads both, and defaults new archives to
  stored; M64 already admits exactly those two methods and M95 requires local/
  central agreement.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 preserve/read methods `0` and `8`
  with versions `20`, flags `0`, and payload `payload`. The fixed producer
  remains exact at method `8`, versions `20`, and flags `0` for all 50 members.
- The corrected format/Ruff-clean exact 3.12.13 red contract passes 13 existing
  behavior, complete/mixed bundle, standard-writer, file-type, unsupported-
  method, inventory, producer, source, and protected-surface assertions and
  fails only the intended missing-documentation assertion in 0.76 seconds.
- `scripts/smoke_release.py` and `scripts/release_artifacts.py` remain byte-
  identical to M112. The decision adds no exact deflate-only classifier or new
  decompressor.

## Explicit non-scope

- No exact deflate-only profile, additional compression method, new
  decompressor, compression-level or ratio policy, recompression, raw stream
  parsing, payload inspection, repair, or general archive-security claim.
- No workflow, allocation, dependency, producer, runtime package/API, native/
  WASM, version, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Run the implementation checkpoint, supported-Python focused proof, static/
  architecture/docs/full-suite/graphics/profile/vertical/artifact validation,
  findings-first review, history/hosted-state audit, final separators,
  standalone DCO commit, and bounded scratch cleanup.
