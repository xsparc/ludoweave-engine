# Current task

- **Task:** M115 - scope sample-bundle byte reproducibility to the release
  environment.
- **Status:** M114 commit/cleanup verification, primary-source research, exact
  supported-runtime producer probing, and the deliberate-red contract are
  complete. RFC-0098 and aligned public/project records are implemented.
  Focused, supported-runtime, static, architecture, docs, complete-suite,
  graphics, profile, vertical-slice, and initial artifact qualification pass.
  Findings-first review has no actionable finding. Review-inclusive artifacts
  and the corrected sequential final source separator pass. History audit,
  hosted-state audit, object-integrity checks, and the post-audit separator
  pass. The final precommit metadata separator passes. Commit and cleanup
  remain.
- **Base:** Fully locally validated M114 DCO commit
  `0d365baf584fd4074e6b46128a6b4a1016ca296f`, tree
  `2b3e8d8d173ed9a99978a92f072ff385422b9334`, with sole parent exact M113.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Scope sample-bundle byte reproducibility to repeated production within one
  fixed resolved release environment.
- Keep baseline CPython 3.12 as the official release producer while CPython
  3.12-3.14 remain compatible consumers, verifiers, and local staging
  environments without a cross-runtime byte-identity promise.
- Keep the fixed producer's explicit `compresslevel=9`, complete release smoke,
  RFC-0021's separate wheel/sdist boundary, and public manifest shape
  unchanged.
- Add RFC-0098, one focused architecture contract, and aligned public,
  security, architecture, release, roadmap, maintainer, and factual project
  records.
- Keep workflows, runner allocation, actions, permissions, credentials,
  dependencies, lock, version, verifier/runtime scripts, sample producer,
  runtime package/API, release authority, tags, releases, publication, and
  public branch state unchanged.

## Evidence so far

- M114 is exact standalone DCO commit
  `0d365baf584fd4074e6b46128a6b4a1016ca296f`, tree
  `2b3e8d8d173ed9a99978a92f072ff385422b9334`, sole parent M113, exact
  maintainer identity, one sign-off, 15 intended paths, and `0 15` divergence.
  Nine audited M114 scratch targets were removed and zero remain.
- Python 3.14.0 released on 2025-10-07. Official Python documentation records
  that default Windows binaries changed the `zlib` implementation to zlib-ng
  and exposes build/runtime implementation constants.
- The ignored probe is format- and Ruff-clean. Initial exact-runtime launches
  were blocked before project execution because the sandbox could not access
  uv's existing user cache; approved cache-access reruns passed.
- Exact Windows CPython 3.12.13, 3.13.13, and 3.14.5 each produced two
  byte-identical fixed sample bundles within its resolved environment. CPython
  3.12/3.13 used zlib 1.3.1 and emitted a 111,168-byte archive at SHA-256
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  CPython 3.14 used zlib-ng 2.2.4 and emitted a 111,413-byte archive at SHA-256
  `d592e99c8c3a65ae63f0cf89ed7eff6094365ca98ba58d08c2099fac4316834b`.
- The first focused test format check found one mechanical formatting change;
  Ruff formatting corrected it and lint passed.
- The exact CPython 3.12.13 deliberate-red contract passed six behavior,
  producer, workflow-order, distribution-scope, and protected-surface
  assertions and failed only the intended absent-documentation assertion in
  0.32 seconds.
- RFC-0098 now records one sample-bundle reproducibility-scope decision. No
  runtime, workflow, producer, verifier, manifest, dependency, lock, or public
  API change is introduced.
- All seven focused assertions pass on exact CPython 3.12.13, 3.13.13, and
  3.14.5. The unchanged lock, 358-file formatting, Ruff, corrected strict
  Pyright with the locked graphics extra, 1,589 architecture assertions with
  one established skip, strict docs, and whitespace pass.
- Complete exact-runtime suites pass: 3.12.13 with graphics has 3,129 passes
  and 15 skips; 3.13.13 and 3.14.5 each have 3,119 passes and 16 skips. Ten
  real-wgpu tests, both profiles, and both vertical slices pass with unchanged
  deterministic identities.
- Two fresh builds reproduce a 278,133-byte pure wheel at
  `1c60a9d05b6180649c7cb975c0394eda198df3061769de7956a5b3112a1b970a`
  and a 1,536,034-byte source archive at
  `bb04237c4ac401e5c1044c4c36f1dc4c3e044b1aed3760c023a10eb6d8f96aa0`.
  Isolated wheel smoke, twice-staged byte identity, complete release smoke, and
  94/596-entry package hygiene pass.
- Findings-first review covers exactly 15 intended paths. Protected workflows,
  producer, verifier, reproducibility script, metadata, lock, runtime package/
  API, dependencies, version, and release authority have zero diff. Public
  tool-identity, high-confidence secret, whitespace, and current-status scans
  are clean; no actionable finding remains.
- Review-inclusive builds reproduce the unchanged 278,133-byte pure wheel at
  `1c60a9d05b6180649c7cb975c0394eda198df3061769de7956a5b3112a1b970a`
  and a 1,537,594-byte source archive at
  `93a6b2df81e8b229c4dc2e89453d4477426925b41a967eed893c6b3a994d6aca`.
  Reproducibility, isolated-wheel smoke, twice-staged byte identity, complete
  release smoke, and 94/596-entry package hygiene pass.
- The final source separator passes the unchanged lock, 358-file format check,
  Ruff, strict Pyright, strict docs, protected surfaces, whitespace, all 1,589
  architecture assertions with one established skip, and all 12 focused
  metadata/M115 assertions. An initial parallel pytest pair collided only on
  the shared temp root; exact cleanup and sequential reruns passed.
- The precommit audit confirms exact M114 head/tree/parent, exact M99 local and
  remote `main`, `0 15` divergence, the linear M100-M114 stack, 15 intended
  paths, exact maintainer identity and DCO sign-off, protected-surface
  integrity, required-only branch inventory, and zero critical object finding.
  GitHub reports no M115 PR/run, release, or tag; no hosted Actions allocation
  was triggered.
- The post-audit separator passes strict docs, all 12 focused metadata/M115
  assertions, protected-surface integrity, whitespace, exact 15-path scope,
  and public tool-identity/high-confidence secret scans.
- The final precommit metadata separator passes all 12 focused assertions and
  whitespace after the final task-state wording update.

## Explicit non-scope

- No cross-runtime byte-identity claim, compressor allowlist or pin,
  compressor-identity manifest field, runtime rejection, recompression, new
  sample-byte verifier, or general reproducible-build claim.
- No workflow, allocation, dependency, producer, runtime package/API, native/
  WASM, version, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Create the standalone DCO commit and perform bounded scratch cleanup.
