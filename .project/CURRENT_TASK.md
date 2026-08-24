# Current task

- **Task:** M114 - retain sample-member compression-level non-observability.
- **Status:** M113 commit/cleanup verification, primary-source research, exact
  supported-runtime/producer probing, and a deliberate-red compatibility
  contract are complete. RFC-0097 and aligned public/project records are
  implemented. Focused, supported-runtime, static, architecture, docs,
  complete-suite, graphics, profile, vertical-slice, and initial artifact
  qualification pass. Findings-first review has no actionable finding. Review-
  inclusive artifacts and final reviewed-tree source qualification pass.
  History/hosted-state audit and the post-audit separator pass. Commit and
  cleanup remain.
- **Base:** Fully locally validated M113 DCO commit
  `0c1d81bea0079e2946b2ec2919c1e7fc6cfbf9b3`, tree
  `14c2b29bcc787c3c784168b5efbc726ed25a2d72`, with sole parent exact M112.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Retain verifier independence from exact writer compression-level
  configuration when every established sample-bundle check passes.
- Keep the fixed producer's explicit `compresslevel=9`, M105's zero flags, and
  M113's stored/deflated method policy without adding an exact level-9 verifier
  profile or inferred compressor level.
- Add RFC-0097, one focused architecture compatibility contract, and aligned
  public, security, architecture, release, roadmap, maintainer, and factual
  project records.
- Keep workflows, runner allocation, actions, permissions, credentials,
  dependencies, lock, version, verifier/runtime scripts, sample producer,
  runtime package/API, release authority, tags, releases, publication, and
  public branch state unchanged.

## Evidence so far

- M113 is exact standalone DCO commit
  `0c1d81bea0079e2946b2ec2919c1e7fc6cfbf9b3`, tree
  `14c2b29bcc787c3c784168b5efbc726ed25a2d72`, sole parent M112, exact
  maintainer identity, one sign-off, 15 intended paths, and `0 14` divergence.
  Nine audited M113 scratch targets were removed and zero remain.
- PKWARE assigns broad Deflate option categories to flag bits 1 and 2, not an
  exact numeric compressor level. Python's `compresslevel` controls writing;
  CPython 3.13 adds public `ZipInfo.compress_level` for that configuration.
- Exact CPython 3.12.13, 3.13.13, and 3.14.5 requested levels `0`, `1`, `6`,
  and `9`, then reopened every member with method `8`, extraction version `20`,
  zero flags, readable bytes, and no recovered exact level. Controlled levels
  `6` and `9` produced identical archive bytes on all three runtimes.
- All 50 fixed-producer members remain method `8`, version `20`, and zero flags;
  the producer source remains explicit at level `9`, while reopened metadata
  does not recover that setting.
- The ignored probe is format/Ruff clean after one recorded mechanical
  correction. The exact 3.12.13 deliberate-red contract passes 15 behavior,
  complete/mixed bundle, standard-writer, inventory, producer, source, and
  protected-surface assertions and fails only the intended missing-
  documentation assertion in 0.45 seconds.
- `scripts/smoke_release.py` and `scripts/release_artifacts.py` remain byte-
  identical to M113. The decision adds no level classifier or inference.
- All 16 focused assertions pass on exact CPython 3.12.13, 3.13.13, and 3.14.5
  in 0.41, 0.78, and 0.76 seconds. The unchanged lock, 357-file formatting,
  Ruff, strict Pyright, 1,582 architecture assertions with one established
  skip, strict docs, and whitespace pass.
- Complete exact-runtime suites pass: 3.12.13 with graphics has 3,122 passes
  and 15 skips; 3.13.13 and 3.14.5 each have 3,112 passes and 16 skips. Ten real-
  wgpu tests, both profiles, and both vertical slices pass with established
  deterministic identities.
- Two fresh builds reproduce a 277,859-byte pure wheel at
  `da01350575fe086ab26f361b6d7cd7517b1559bba857453fbe9683de645cc4db`
  and a 1,528,920-byte source archive at
  `61ed0826b9d17ff152c1fcfae70218fd162524b189b8fe64adb812d1580c3b0d`.
  Isolated-wheel smoke, ten-artifact staging, complete release smoke, and
  94/594-entry package hygiene pass.
- Findings-first review covers exactly 15 intended record, documentation, and
  test paths. Protected workflows, verifier, stager, metadata, lock, runtime
  package/API, dependencies, producer, version, and release authority have zero
  diff. Current public tool-identity, high-confidence secret, whitespace, and
  stale-current-status scans are clean; no actionable finding remains.
- Review-inclusive builds reproduce the unchanged 277,859-byte pure wheel at
  `da01350575fe086ab26f361b6d7cd7517b1559bba857453fbe9683de645cc4db`
  and a 1,530,147-byte source archive at
  `c0970acd55a1ab4c2af5e718c265b634bdea9064ac2c9b8bfaa1ce869fb35e4f`.
  Reproducibility, isolated-wheel smoke, deterministic staging, complete
  release smoke, and 94/594-entry package hygiene pass.
- The final reviewed-tree source separator passes the unchanged lock, 357-file
  format check, Ruff, strict Pyright, all 1,582 architecture assertions with one
  established skip, strict docs, all 21 metadata/compatibility assertions, and
  whitespace.
- The precommit audit confirms exact M113 head/tree/parent, exact M99 local and
  remote `main`, `0 14` divergence, the linear M100-M113 stack, 15 intended
  paths, exact maintainer identity, protected-surface integrity, no public tool
  identity or high-confidence secret, and zero critical object finding. GitHub
  reports no M114 PR/run, release, or tag. One unsupported release-list JSON
  field was corrected; the supported read-only query returned empty.
- The post-audit separator passes strict docs, all 21 metadata/compatibility
  assertions, protected-surface integrity, whitespace, exact 15-path scope,
  high-confidence secret scan, and public tool-identity scan.

## Explicit non-scope

- No exact level-9 profile, inferred compressor level, compression-ratio
  policy, recompression, raw Deflate parsing, payload inspection, repair, or
  general archive-security claim.
- No workflow, allocation, dependency, producer, runtime package/API, native/
  WASM, version, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Create the standalone DCO commit and perform bounded scratch cleanup.
