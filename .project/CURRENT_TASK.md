# Current task

- **Task:** M118 - retain Python 3.15 prerelease outside support after one
  installed-wheel compatibility observation.
- **Status:** M117 commit/cleanup verification, current primary-source research,
  exact Windows CPython 3.15 prerelease inventory, installed-wheel probe,
  implementation, complete local validation, findings-first review,
  history/hosted-state audit, and all precommit separators are complete.
- **Base:** Fully locally validated M117 DCO commit
  `2015e8c613366996a813362a1d95edea98b42bb0`, tree
  `a031129b5a46003dbc5b588cab94c3adba704301`, with sole parent exact M116.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Retain `requires-python = ">=3.12,<3.15"`, standard CPython 3.12-3.14 as the
  supported baseline, and exact doctor rejection for Python 3.15.
- Record one exact Windows CPython 3.15.0b1 pure-wheel observation: explicit
  metadata override, version, doctor rejection, deterministic serial headless
  execution, orderly close, and exact wrong-thread rejection.
- Add RFC-0101, one focused architecture contract, and aligned public,
  security, architecture, runtime, release, roadmap, maintainer, and factual
  project records.
- Keep workflows, runner allocation, actions, permissions, credentials,
  dependencies, lock, version, metadata, installed-wheel smoke, runtime package/
  API, providers, release authority, tags, releases, publication, and public
  branch state unchanged.

## Evidence so far

- M117 is exact standalone DCO commit
  `2015e8c613366996a813362a1d95edea98b42bb0`, tree
  `a031129b5a46003dbc5b588cab94c3adba704301`, sole parent M116, exact
  maintainer identity, one sign-off, 16 intended paths, and `0 18` divergence.
  Fourteen audited M117/test scratch targets were removed and zero remain.
- PEP 790 records Python 3.15.0 candidate 1 on 2026-08-04 and schedules final
  for 2026-10-01. uv classifies Python 3.15 prereleases as Tier 2.
- No exact uv-managed Windows CPython 3.15 runtime was initially installed. An
  exact RC1 install request found no managed download; the current inventory
  exposed only CPython 3.15.0b1, which was then installed.
- A pure `0.1.0a1` wheel built and an isolated exact 3.15.0b1 environment was
  created. uv warned that the interpreter is incompatible with the declared
  `>=3.12,<3.15` range. Installation succeeded only with the explicit metadata
  override and no dependencies.
- The first install/probe orchestration used an invalid PowerShell selection
  parameter, then pip received no requirement; no product result relies on it.
  The corrected run installed the wheel and passed version before `doctor`
  correctly exited 1 for unsupported Python, stopping that sequence.
- The explicit expected-boundary rerun confirmed doctor exit 1, then completed
  120 virtual ticks and frames in exactly 2,000,000,000 nanoseconds, closed,
  and observed `engine.wrong_thread`. The installed-wheel headless example
  reproduced the deterministic summary.
- The ignored probe and new focused contract are format- and Ruff-clean. Exact
  CPython 3.12.13 passes three metadata, doctor, and protected-surface assertions
  and fails only the intended absent-RFC/docs assertion in 0.28 seconds.
- The first implementation run passed three assertions but found that Markdown
  code formatting interrupted one required prose phrase. The corrected RFC
  states the phrase plainly; all four assertions pass in 0.19 seconds. Strict
  docs built in 1.73 seconds, whitespace passes, and exactly 16 intended paths
  change.
- The unchanged 46-package lock, exact 45-package CPython 3.12.13 graphics
  environment, 361-file format check, Ruff, strict Pyright, strict docs,
  protected surfaces, whitespace, and all 1,603 architecture assertions with
  one established Windows capability skip pass. Exact standard CPython
  3.12.13, 3.13.13, and 3.14.5 each pass all four focused assertions.
- Complete suites pass 3,143 tests with 15 skips on exact CPython 3.12.13 with
  graphics and 3,133 tests with 16 skips on exact CPython 3.13.13 and 3.14.5.
  All ten real-wgpu tests, fresh base/graphics profiles, Clockwork Arena, and
  Agent World Builder pass with established deterministic identities.
- Two initial builds reproduce a 278,778-byte pure wheel at SHA-256
  `254c3da96cc0b7161425ea09a9883279ba91f030a7790d5c1ac89149acbcd9ba`
  and a 1,557,512-byte source archive at SHA-256
  `27adfcbf099b8092bcaead44e07a5afd0e8b1b51ff91000fa8e2320441ddba40`.
  Wheel smoke, twice-staged ten-artifact byte identity, complete release smoke,
  and 94/602-entry package hygiene pass.
- Findings-first review covers exactly 16 intended paths. Protected workflows,
  doctor/CLI, installed-wheel smoke, metadata, lock, runtime package/API,
  dependencies, version, providers, and release authority have zero diff.
  Public identity, high-confidence secret, package-hygiene, and whitespace scans
  are clean; no actionable finding remains.
- Review-inclusive builds reproduce the unchanged 278,778-byte pure wheel at
  SHA-256
  `254c3da96cc0b7161425ea09a9883279ba91f030a7790d5c1ac89149acbcd9ba`
  and a 1,558,615-byte source archive at SHA-256
  `ec194e05707eb847e2ca7f9d6671d04dd04c87c7f68693f0c488762ec7087051`.
  Reproducibility, isolated-wheel smoke, twice-staged ten-artifact byte
  identity, complete release smoke, and 94/602-entry package hygiene pass.
- The final source separator passes the unchanged 46-package lock, 361-file
  formatting, Ruff, strict Pyright, strict docs, protected surfaces,
  whitespace, all 1,603 architecture assertions with one established Windows
  capability skip, and all nine focused M59/M118 assertions.
- The precommit audit confirms a linear 18-commit M100-M117 unpublished stack
  with exact maintainer identity, one DCO sign-off per commit, no merges, and
  zero critical Git object-database finding. Local and remote `main` remain
  exact M99; only remote `main` exists. GitHub authentication is valid and
  M118 PR/run, releases, and remote tags are empty, so no hosted Actions
  allocation was triggered.
- The post-audit separator builds strict docs in 1.64 seconds, passes all nine
  focused assertions in 0.38 seconds, and confirms protected surfaces, exact
  16-path scope, whitespace, public identity hygiene, and high-confidence
  secret scans remain clean.
- The final precommit metadata separator passes all nine focused assertions in
  0.37 seconds and reports no whitespace error.

## Explicit non-scope

- No Python 3.15 support, final-release, later-prerelease, cross-platform,
  graphics, free-threaded, full-suite, performance, extension, or provider
  compatibility claim.
- No runtime shim, metadata relaxation, doctor relaxation, workflow, allocation,
  dependency, lock, version, runtime package/API, release authority, tag,
  release, publication, push, or PR.

## Remaining acceptance work

- Commit the exact reviewed slice and perform bounded scratch cleanup.
