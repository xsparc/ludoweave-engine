# Current task

- **Task:** M117 - retain the standard CPython baseline after a free-threaded
  serial-compatibility evaluation.
- **Status:** M116 commit/cleanup verification, current primary-source research,
  exact CPython 3.14.5t installed-wheel probing, implementation, complete local
  validation, findings-first review, history/hosted-state audit, and all
  precommit separators are complete.
- **Base:** Fully locally validated M116 DCO commit
  `34bad8a0fa304a2e0a96f5cc177483d09abd7acd`, tree
  `26be29b19d1b91e3e3b889d6a3337541290739b9`, with sole parent exact M115.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Retain standard GIL CPython as the supported baseline for CPython 3.12-3.14.
- Record exact Windows CPython 3.14.5 free-threaded installed-wheel serial
  compatibility with the GIL disabled: version, doctor, deterministic headless
  execution, orderly close, and exact wrong-thread rejection.
- Keep lifecycle ownership explicit and independent of the GIL. Do not add
  locking, concurrent mutation, runtime build branches, or a support promise.
- Add RFC-0100, one focused architecture contract, and aligned public,
  security, architecture, runtime, release, roadmap, maintainer, and factual
  project records.
- Keep workflows, runner allocation, actions, permissions, credentials,
  dependencies, lock, version, metadata, installed-wheel smoke, runtime package/
  API, graphics, release authority, tags, releases, publication, and public
  branch state unchanged.

## Evidence so far

- M116 is exact standalone DCO commit
  `34bad8a0fa304a2e0a96f5cc177483d09abd7acd`, tree
  `26be29b19d1b91e3e3b889d6a3337541290739b9`, sole parent M115, exact
  maintainer identity, one sign-off, 15 intended paths, and `0 17` divergence.
  Thirteen audited M116/test scratch targets were removed and zero remain.
- PEP 779 makes free-threaded CPython officially supported but still optional
  in Python 3.14. Python documents that shared iterators and other objects are
  not generally safe merely because the GIL is disabled. uv documents explicit
  `3.14t` discovery and selection.
- Exact CPython 3.14.5 free-threaded was installed through uv. The ignored probe
  is format- and Ruff-clean. A pure local wheel installed without dependencies
  into an isolated 3.14.5t environment.
- With `Py_GIL_DISABLED == 1` and `sys._is_gil_enabled() is False`, module
  version and doctor passed. The installed wheel completed 120 virtual ticks
  and frames in exactly 2,000,000,000 nanoseconds, closed normally, and rejected
  a worker-thread initialize call with `engine.wrong_thread`. The installed-
  wheel headless example reproduced the same deterministic summary.
- The new focused contract needed one mechanical Ruff reformat, then was
  format- and lint-clean. Exact CPython 3.12.13 passed three protected baseline,
  ownership, and scope assertions and failed only the intended absent-RFC/docs
  assertion in 0.23 seconds.
- The first post-implementation run found that one prose assertion was
  unintentionally case-sensitive. The corrected case-normalized contract is
  format/Ruff-clean and all four assertions pass in 0.20 seconds. Strict docs
  build in 1.64 seconds with only the known Material notice; whitespace passes;
  exactly 16 intended paths change.
- Exact standard-GIL CPython 3.12.13, 3.13.13, and 3.14.5 each pass all four
  focused assertions. The unchanged lock, 360-file format check, Ruff, strict
  Pyright, 1,599 architecture assertions with one established Windows
  capability skip, strict docs, protected surfaces, and whitespace pass.
- Complete suites pass 3,139 tests with 15 skips on exact CPython 3.12.13 with
  graphics and 3,129 tests with 16 skips on exact CPython 3.13.13 and 3.14.5
  standard-GIL base environments.
- All ten real-wgpu tests, fresh base/graphics profiles, Clockwork Arena, and
  Agent World Builder pass with the established deterministic identities.
- Two initial builds reproduce a 278,576-byte pure wheel at SHA-256
  `5161d89bb35aaf7b8a5af78912cbd5858c0ec67364002b44ed4f92c05021095d`
  and a 1,551,612-byte source archive at SHA-256
  `286306db276e076688abc92bfb8c16c374a60b64579ea6789fb6d8116233fb12`.
  Wheel smoke, twice-staged ten-artifact byte identity, complete release smoke,
  and 94/600-entry package hygiene pass.
- Findings-first review covers exactly 16 intended paths. Protected workflows,
  runtime lifecycle, installed-wheel smoke, metadata, lock, runtime package/API,
  dependencies, version, graphics, and release authority have zero diff. Public
  tool-identity, high-confidence secret, package-hygiene, and whitespace scans
  are clean; no actionable finding remains.
- Review-inclusive builds reproduce the unchanged 278,576-byte pure wheel at
  SHA-256
  `5161d89bb35aaf7b8a5af78912cbd5858c0ec67364002b44ed4f92c05021095d`
  and a 1,551,972-byte source archive at SHA-256
  `9ea05239d408bbead73a774790da1fe273b8cf2252b1fd4cdbae462e817333d6`.
  Reproducibility, isolated-wheel smoke, twice-staged ten-artifact byte
  identity, complete release smoke, and 94/600-entry package hygiene pass.
- The final source separator passes the unchanged 46-package lock, 360-file
  formatting, Ruff, strict Pyright, strict docs, protected surfaces,
  whitespace, all 1,599 architecture assertions with one established Windows
  capability skip, and all nine focused M59/M117 assertions.
- The precommit audit confirms a linear 17-commit M100-M116 unpublished stack
  with exact maintainer identity, one DCO sign-off per commit, no merges, and
  zero critical Git object-database finding. Local and remote `main` remain
  exact M99; only remote `main` exists. GitHub authentication is valid and
  M117 PR/run, releases, and remote tags are empty, so no hosted Actions
  allocation was triggered.
- The first post-audit documentation and focused-test launches were blocked
  before project execution by sandbox denial of the existing uv cache. The
  approved rerun built strict docs in 1.70 seconds and passed all nine focused
  assertions in 0.39 seconds. Protected surfaces, exact 16-path scope,
  whitespace, public identity hygiene, and high-confidence secret scans pass.
- The final precommit metadata separator passes all nine focused assertions in
  0.38 seconds and reports no whitespace error.

## Explicit non-scope

- No concurrent-safety claim, parallel speedup, performance result, graphics/
  wgpu evidence, cross-platform free-threaded evidence, extension compatibility,
  new lock, runtime branch, or support promotion.
- No workflow, allocation, dependency, metadata, version, runtime package/API,
  release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Commit the exact reviewed slice and perform bounded scratch cleanup.
