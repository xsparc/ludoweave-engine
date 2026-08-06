# Test Evidence

Only commands actually executed in the current repository are recorded here.

## M22 development evidence — 2026-08-06, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Baseline lock remained current; 46 packages resolved in 0.75 ms. |
| Inherited focused command/transaction/stability/API/release tests | 0 | 165 tests passed in 3.43 seconds. |
| `uv run --frozen pytest -q` | 0 | Inherited full suite passed 1,015 tests in 80.65 seconds with one existing Windows symlink-capability skip. |
| `uv run --frozen python examples/operation_argument_compatibility.py` | 0 | All seven valid built-in v1 operations committed; missing-required and unexpected-field cases rejected with `world.transaction.validation_failed`; one sanitized schema `/1` report printed. |
| `uv run --frozen pytest -q tests/integration/test_operation_argument_compatibility.py` | 0 | 7 installed evidence and tamper tests passed in 1.49 seconds. |
| M22 integration plus architecture tests | 0 | 15 tests passed in 1.63 seconds. |
| Focused M22/M20/release test group after artifact wiring | 0 | 34 tests passed in 3.50 seconds. |
| First repository-wide Ruff check | 1 | Three simplification findings in the new example/architecture test were reported and corrected; no lint pass is claimed for this attempt. |
| First repository-wide Pyright run | 0 | 0 errors, 0 warnings, 0 information messages. |
| First M22 strict MkDocs build | 0 | Documentation built successfully in 0.66 seconds with Material's upstream MkDocs 2.0 informational warning. |

The first sandboxed uv invocation after adding M22 evidence exited 1 before
pytest ran because the managed sandbox denied access to uv's user cache. The
same test commands were rerun with approved cache access and passed; no test
pass is claimed for the failed attempt. Final full-suite, docs, build, wheel,
release, graphics, benchmark/profile, and diff evidence follows. Hosted
hosted evidence is recorded below.

## M22 final local validation — 2026-08-06, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current; 46 packages resolved in 1 ms. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Locked baseline plus graphics environment checked 45 packages in 2 ms. |
| `uv run --frozen ruff format --check .` | 0 | All 215 Python files were formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed after the recorded first-pass corrections. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 1,030 tests passed in 71.59 seconds; one existing Windows symlink-capability test skipped. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.64 seconds with Material's upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built pure `ludoweave-0.1.0a1-py3-none-any.whl` and source distribution. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated installed-wheel smoke passed, including exact M22 operation-argument evidence. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/release-candidate-m22-final` | 0 | Staged the complete deterministic 10-artifact release candidate with sample bundle and SPDX SBOM. |
| `uv run --frozen python scripts/smoke_release.py .tmp/release-candidate-m22-final` | 0 | Isolated release smoke passed for `0.1.0a1`, including bundled M22 evidence. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | 10 real-wgpu integration tests passed in 5.79 seconds. |
| Hosted graphics vertical-slice commands | 0 | Thirty-tick wgpu Clockwork Arena and Agent World Builder completed with their expected structured summaries. |
| M1 benchmark plus validator | 0 | Seven workloads validated; fixed-tick target observed, simulation-tick target not observed. |
| M2 benchmark plus validator | 0 | Four informational workloads validated with no timing targets. |
| M3 benchmark plus validator | 0 | Six workloads validated; neither of two recorded targets was met. |
| M4 benchmark plus validator | 0 | Three workloads validated; baseline target observed. |
| M7 base and graphics profile runners plus validators | 0 | Two-workload base and three-workload graphics artifacts validated. |
| `git diff --check` | 0 | No whitespace errors. |
| First sandboxed `git add --all` | 128 | The filesystem sandbox denied creation of `.git/index.lock`; no path was staged. The operation was rerun with approved repository-metadata access. |

The M1 simulation and both M3 target misses are recorded without a performance
pass claim. They do not authorize native acceleration. Repository review found
no change under `src/`, `.github/`, `pyproject.toml`, or `uv.lock`; no credential
assignment matched; and the M22 evidence import scan found no ambient,
provider, filesystem, process, or network dependency.

## M22 hosted validation — PR #32

Ready PR #32 targets `main` from `codex/m22-operation-argument-policy` at
DCO-signed implementation commit
`f1a89ad460467039f966ed37955144840cd96a12`. GitHub Actions run
`31100821087`, triggered once by that pull request, completed successfully on
2026-08-06. It is the only workflow run listed for the branch.

| Hosted job | Result |
| --- | --- |
| Quality, tests, and distribution — Ubuntu, Python 3.12 | Passed lock, formatting, Ruff, strict Pyright, strict docs, baseline tests, base profile smoke, pure build, isolated wheel smoke, release staging, and isolated release smoke. |
| Compatibility — Ubuntu, Python 3.13 | Passed. |
| Compatibility — Ubuntu, Python 3.14 | Passed. |
| Compatibility — Windows, Python 3.14 | Passed. |
| Compatibility — macOS, Python 3.14 | Passed. |
| Graphics smoke — Ubuntu | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke — Windows | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke — macOS | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |

No additional CI job or workflow change was introduced. No cross-version,
external-adoption, stability-promotion, release, or publication claim is made.

## Baseline — 2026-08-04

| Command | Exit | Result |
| --- | ---: | --- |
| `git status --short --branch` | 0 | Clean `main` tracking `origin/main`; only the initial README and LICENSE were tracked. |
| `uv run --no-project python --version` | 0 | CPython 3.14.5 executed through uv; no project existed. |
| `uv run --no-project python -m pytest -q` | 1 | Baseline could not run because pytest was not installed. |
| `uv run --no-project python scripts/agent_workflow.py status` | 1 | Optional workflow helper was absent from the initial repository. |

## Development feedback retained

The first focused quality pass was not clean and was not reported as passing:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 1 | One file required formatting. |
| `uv run --frozen ruff check .` | 1 | Three lint findings were reported and corrected. |
| `uv run --frozen pyright` | 1 | Nineteen strict-type findings were reported and corrected. |
| `uv run --frozen pytest -q` | 1 | 38 tests passed; one setup error came from denied access to pytest's user temp directory. Test temporaries were moved to the workspace. |

The independent review later reproduced two relative-import forms that bypassed the architecture checker. Relative parent imports and sibling-alias imports are now resolved to absolute module names, regression fixtures cover both forms, and all affected checks were rerun.

## Final local validation — Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile is current; 39 packages resolved. |
| `uv sync --frozen --all-groups` | 0 | Locked environment checked successfully with 39 packages. |
| `uv run --frozen ruff format --check .` | 0 | 26 Python files already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 44 tests passed in 0.96 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel install passed console version, JSON doctor, and three-tick headless example checks. |
| `git diff --check` | 0 | No whitespace errors after LF normalization. |

## Executable acceptance evidence

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ludoweave --version` | 0 | Printed `ludoweave 0.1.0.dev0`. |
| `uv run --frozen ludoweave doctor` | 0 | JSON schema `ludoweave.doctor/1`; Python, monotonic clock, and null renderer all reported `ok`. |
| `uv run --frozen python examples/hello_headless.py --ticks 120` | 0 | Printed JSON with 120 ticks, 120 frames, null renderer, closed final state, and 2,000,000,000 virtual nanoseconds. |
| GitHub YAML parse check | 0 | Parsed all four workflow/template YAML files. |
| Banned-import source scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` imports matched; ripgrep uses exit 1 for no matches. |
| Credential-pattern scan | 1 | No key/password/secret/private-key assignment patterns matched; ripgrep uses exit 1 for no matches. |

## Review evidence

- Wheel contents contain only `ludoweave`, `py.typed`, distribution metadata, CLI entry point, LICENSE, and NOTICE.
- Package metadata reports Apache-2.0, Python `>=3.12,<3.15`, and no runtime `Requires-Dist` entries.
- CI actions use full commit SHAs, workflow permissions are `contents: read`, and checkout credential persistence is disabled.
- Independent review found relative parent/sibling import checker bypasses and stale state files as blockers. Both bypass forms have regression coverage; these state files now reflect executed evidence.
- No GitHub-hosted matrix job has run yet, so cross-platform CI is not claimed as passing.

## M1-01 final local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current with 39 packages resolved. |
| `uv sync --frozen --all-groups` | 0 | Existing locked environment checked successfully with 39 packages. |
| `uv run --frozen pytest -q tests/unit/test_entity_allocator.py tests/architecture/test_import_boundaries.py` | 0 | 21 focused allocator and architecture tests passed. |
| `uv run --frozen ruff format --check .` | 0 | 30 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 61 tests passed in 1.64 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel checks passed version, doctor, entity generation/staleness, and the headless example. |
| `git diff --check` | 0 | No whitespace errors. |

Independent review found that plain prefix matching allowed `ludoweave.ecs_tools` through the ECS dependency rule. All package-boundary checks now require exact module names or dot-delimited children, a synthetic near-prefix regression is present, and the reviewer independently reran the 21 focused tests with no remaining blocker.

## M1-02 final local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current with 39 packages resolved. |
| `uv sync --frozen --all-groups` | 0 | Existing locked environment checked successfully with 39 packages. |
| `uv run --frozen pytest -q tests/unit/test_component_schema.py tests/property/test_component_migrations.py tests/architecture/test_import_boundaries.py` | 0 | 48 focused component, migration, property, and architecture tests passed. |
| `uv run --frozen ruff format --check .` | 0 | 33 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 103 tests passed in 1.75 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel checks passed version, doctor, entity generations, explicit component registration, forward migration, and the headless example. |
| `git diff --check` | 0 | No whitespace errors. |
| Banned-import source scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` import matched; ripgrep uses exit 1 for no matches. |
| Credential-pattern scan | 1 | No credential-assignment pattern matched; ripgrep uses exit 1 for no matches. |
| Global-registry source scan | 1 | No `ComponentRegistry` instance exists in package source; ripgrep uses exit 1 for no matches. |

Independent architecture and quality design reviews recommended explicit UUID identity, no global registration, immutable registries, a narrow canonical scalar domain, and complete adjacent migrations; ADR-0003 records the decision. Independent code review found no runtime/API defect. Its state-drift blockers were the stale derived-ID wording and missing completion evidence; both are corrected here.

## M1-03 final local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current with 39 packages resolved. |
| `uv sync --frozen --all-groups` | 0 | Frozen environment checked successfully with 39 packages. |
| `uv run --frozen ruff format --check .` | 0 | 39 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q tests\unit\test_world_storage.py tests\conformance\test_world_conformance.py tests\property\test_world_model.py tests\architecture\test_import_boundaries.py` | 0 | 47 focused storage, conformance, state-machine property, and architecture tests passed in 1.13 seconds. |
| `uv run --frozen pytest -q` | 0 | 144 tests passed in 2.53 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts\smoke_wheel.py dist` | 0 | Isolated wheel passed version, doctor, allocator, schema migration, copy-safe world add/patch/get/remove, destroy/reuse, stale-handle, and headless example checks. |
| `git diff --check` | 0 | No whitespace errors. |
| Banned-import source scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` import matched source, tests, or scripts; ripgrep uses exit 1 for no matches. |
| Credential-pattern scan | 1 | No credential-assignment pattern matched outside excluded generated/dependency paths; ripgrep uses exit 1 for no matches. |
| ECS wall-clock/random scan | 1 | No wall-clock or random source matched `src/ludoweave/ecs`; ripgrep uses exit 1 for no matches. |
| Dynamic-evaluation scan | 1 | No `eval()` or `exec()` call matched package source; ripgrep uses exit 1 for no matches. |
| ECS backend-leakage scan | 1 | No render, wgpu, GLFW, or NumPy reference matched ECS source; ripgrep uses exit 1 for no matches. |
| `uv run --frozen python -m zipfile -l dist\ludoweave-0.1.0.dev0-py3-none-any.whl` | 0 | Wheel contains the typed `ludoweave` package including ECS modules, distribution metadata, CLI entry point, LICENSE, and NOTICE. |

Independent architecture and quality reviews established the copy boundary, epoch contract, swap-removal checks, and independent dictionary oracle before implementation. Findings-first code review then reproduced raw missing-slot errors, a side-effecting getter time-of-check/time-of-use alias defect, an omitted protocol clone declaration, incomplete clone coverage, and a bypassable reference-import guard. All were corrected with regressions. The reviewer reran 47 focused tests with clean Ruff and strict Pyright and accepted M1-03 with no implementation blocker.

GitHub-hosted Windows/macOS/Linux and Python 3.13/3.14 jobs have not run for these changes. No cross-platform pass claim is made.

## M1-06 and complete-M1 final local validation — 2026-08-05, Windows, CPython 3.12.13 GIL build

The first sandboxed `uv lock --check` invocation exited 1 because the managed sandbox denied access to uv's user cache. The same command was rerun with approved cache access and exited successfully; this was an environment permission failure, not a lockfile failure.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current; 39 packages resolved in 0.72 milliseconds. |
| `uv sync --frozen --all-groups` | 0 | Frozen environment checked successfully with 39 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | 60 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 303 tests passed in 2.78 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.31 seconds; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel smoke passed version, doctor, M1 ECS/resource/schedule operations, the M0 headless example, and the fixed-step world example. |
| `uv run --frozen python benchmarks/benchmark_m1.py --samples 30 --seed 1 --json-out .tmp/m1-benchmark.json` | 0 | Recorded 30 raw samples for all seven versioned M1 workloads with sanitized Windows/AMD64/CPython 3.12.13 release-GIL metadata and a dirty-worktree commit reference. |
| `uv run --frozen python benchmarks/validate_m1_results.py .tmp/m1-benchmark.json` | 0 | Exact artifact schema, parameters, distributions, metadata, and both target records validated; one of two local engineering targets was observed. |
| `git diff --check` | 0 | No whitespace errors. |
| Banned native/backend import scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` import matched source, tests, examples, scripts, or benchmarks; ripgrep uses exit 1 for no matches. |
| Credential-assignment scan | 1 | No API key, access token, client secret, password, or private-key assignment pattern matched outside excluded generated/dependency/artifact paths; ripgrep uses exit 1 for no matches. |
| ECS wall-clock/random scan | 1 | No wall-clock, performance timer, or global random use matched `src/ludoweave/ecs`; ripgrep uses exit 1 for no matches. |
| Dynamic-evaluation scan | 1 | No `eval()` or `exec()` call matched package source; ripgrep uses exit 1 for no matches. |
| Application/core concrete-backend scan | 1 | No concrete render backend, wgpu, GLFW, or NumPy reference matched application, ECS, or core source; ripgrep uses exit 1 for no matches. |
| `uv run --frozen python -m zipfile -l dist\ludoweave-0.1.0.dev0-py3-none-any.whl` | 0 | Wheel contains only the typed `ludoweave` package, distribution/entry-point metadata, LICENSE, and NOTICE; benchmarks, tests, docs, credentials, and native artifacts are absent. |

### Final M1 benchmark observations

All durations are nearest-rank distributions from the final 30 retained samples; setup is excluded as documented for operation-specific workloads.

| Workload | p50 | p95 | p99 | Local target observation |
| --- | ---: | ---: | ---: | --- |
| Entity create/destroy/reuse, 10,000 entities | 28.3294 ms | 36.3653 ms | 37.1018 ms | No target assigned. |
| Read query, 10,000 entities/two components | 96.8505 ms | 129.7374 ms | 132.6638 ms | No target assigned. |
| Writable query, 10,000 entities/two components | 148.5815 ms | 194.5107 ms | 202.5685 ms | No target assigned. |
| Scheduler plan, seeded 100-system DAG | 4.1550 ms | 4.6828 ms | 4.8285 ms | No target assigned. |
| Staged flush, 1,000 two-component spawn commands | 41.0282 ms | 56.0997 ms | 60.7698 ms | No target assigned. |
| Fixed-step headless run, 3,600 ticks | 22.7571 ms | 26.8523 ms | 29.0085 ms | Observed p95 ≤ 12 seconds (at least 5× simulated real time). |
| Representative application tick, 10,000 entities | 166.5203 ms | 196.8800 ms | 217.7976 ms | **Not observed:** p95 < 4 ms. |

The benchmark miss is recorded without a performance pass claim. It authorizes profiling and pure-Python algorithm work only; no Rust, PyO3, Cython, NumPy storage, or native build requirement was added.

### Independent review closure

Findings-first review reproduced and drove regressions for forged schedule execution, incomplete flush diagnostics, noncanonical resource failure ordering, hostile input objects/mappings, BaseException query-lease leakage, unmodeled entity-set reads/writes, writable engine-owned input, exact bool/float and signed-zero equality, protocol/runtime surface mismatch, and underspecified benchmark validation/metadata. Canonical plan revalidation, exact input signatures, BaseException-safe cleanup, restricted M1 structural operations, exact public protocols, hostile-source wrapping, exact benchmark schemas, tamper tests, and GIL/free-threaded metadata resolve those findings. The reviewer independently reran 130 focused tests, the 303-test full suite, Ruff format/lint, strict Pyright, a minimal benchmark, and the official 30-sample artifact validator, then accepted M1-06 with no remaining blocking or non-blocking code finding.

### Hosted CI — PR #1

The first PR run (`30936335552`) failed before checkout on every job because the planned `actions/checkout` v6.0.2 SHA `de0fac2e4500dabe0009e8f65f754d05d2b0f7a6` does not exist upstream. The official tag API resolved v6.0.2 to `de0fac2e4500dabe0009e67214ff5f5447ce83dd`; `astral-sh/setup-uv` v8.1.0 independently resolved to the already configured `08807647e7069bb48b6ef5acd8ec9567f424441b`. The three checkout references were corrected without changing workflow privileges or credential persistence.

GitHub Actions run `30936533105` then completed successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed formatting, lint, strict Pyright, lock verification, and strict MkDocs build. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three matrix jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both matrix jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both matrix jobs passed. |
| Installed wheel — Ubuntu/Windows/macOS, Python 3.12 | All three build and isolated-wheel smoke jobs passed. |

Some successful jobs emitted non-fatal setup-uv cache-reservation annotations because another matrix job created the same cache first. No test, build, documentation, or wheel-smoke step failed in the corrected run.

## M1-05 final local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current; 39 packages resolved in 0.80 milliseconds. |
| `uv sync --frozen --all-groups` | 0 | Frozen environment checked successfully with 39 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | 49 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q tests/unit/test_resources.py tests/unit/test_schedule.py tests/property/test_schedule_graph.py tests/architecture/test_import_boundaries.py` | 0 | 47 focused resource, scheduler, generated graph property, and architecture tests passed in 0.45 seconds. |
| `uv run --frozen pytest -q` | 0 | 219 tests passed in 2.26 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.28 seconds; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel passed version, doctor, allocator/schema/world/query/command checks, copy-owned typed resource isolation, deterministic scheduled ordering, and the headless example. |
| `git diff --check` | 0 | No whitespace errors. |
| Banned-import source scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` import matched source, tests, or scripts; ripgrep uses exit 1 for no matches. |
| Credential-pattern scan | 1 | No credential-assignment pattern matched outside excluded generated/dependency paths; ripgrep uses exit 1 for no matches. |
| ECS wall-clock/random scan | 1 | No wall-clock or random source matched `src/ludoweave/ecs`; ripgrep uses exit 1 for no matches. |
| Dynamic-evaluation scan | 1 | No `eval()` or `exec()` call matched package source; ripgrep uses exit 1 for no matches. |
| ECS backend-leakage scan | 1 | No render, wgpu, GLFW, or NumPy import matched ECS source; ripgrep uses exit 1 for no matches. |

Independent architecture and quality reviews established the explicit resource identity/copy boundary, fixed phases, same-phase conflict ambiguity rule, serial-only planner, and deterministic graph diagnostics before implementation. Findings-first code review reproduced a canonical-state mutation risk from misbehaving resource adapters, D0 component eligibility bypass, raw signature-inspection exception, class-member declaration ambiguity, stale public/state documentation, and missing after-only/write-write regressions. The accepted contract now explicitly trusts adapters that treat input as read-only, deterministic plans reject D0 components, signature failures are structured and chained, only strict module-level functions are accepted, and focused regressions cover the ordering relationships. The reviewer independently reran focused tests, Ruff, and strict Pyright and accepted M1-05 with no remaining runtime, API, architecture, test, or scope blocker.

GitHub-hosted Windows/macOS/Linux and Python 3.13/3.14 jobs have not run for these changes. No cross-platform pass claim is made.

## M1-04 final local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current with 39 packages resolved. |
| `uv sync --frozen --all-groups` | 0 | Frozen environment checked successfully with 39 packages. |
| `uv run --frozen ruff format --check .` | 0 | 44 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q tests/unit/test_query.py tests/unit/test_commands.py tests/conformance/test_query_commands_conformance.py tests/property/test_world_model.py tests/architecture/test_import_boundaries.py` | 0 | 52 focused query, command, conformance, state-machine property, and architecture tests passed in 1.12 seconds. |
| `uv run --frozen pytest -q` | 0 | 185 tests passed in 2.16 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel passed version, doctor, allocator/schema/world checks, stable include/exclude/changed query, writable query close, buffered-operation invisibility, atomic flush, deferred-token resolution, and the headless example. |
| `git diff --check` | 0 | No whitespace errors. |
| Banned-import source scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` import matched source, tests, or scripts; ripgrep uses exit 1 for no matches. |
| Credential-pattern scan | 1 | No credential-assignment pattern matched outside excluded generated/dependency paths; ripgrep uses exit 1 for no matches. |
| ECS wall-clock/random scan | 1 | No wall-clock or random source matched `src/ludoweave/ecs`; ripgrep uses exit 1 for no matches. |
| Dynamic-evaluation scan | 1 | No `eval()` or `exec()` call matched package source; ripgrep uses exit 1 for no matches. |
| ECS backend-leakage scan | 1 | No render, wgpu, GLFW, or NumPy import matched ECS source; ripgrep uses exit 1 for no matches. |
| `uv run --frozen python -m zipfile -l dist\ludoweave-0.1.0.dev0-py3-none-any.whl` | 0 | Wheel contains the typed package including query/command modules, distribution metadata, CLI entry point, LICENSE, and NOTICE; no generated docs, tests, backend-native objects, or credentials are packaged. |

Independent architecture and quality reviews established cursor ownership, row-atomic writeback, mutation-guard precedence, buffer rollback, exact token identity, reference independence, and the M2 boundary before implementation. Findings-first code review then reproduced a value-equal deferred-token forgery and signed-zero change-detection loss, and identified five-plus query typing, frozen-write documentation, plan-driver coverage, and failed-queue wording gaps. Identity-only tokens, float-hex signatures, variadic fallback typing, focused regressions, and corrected documentation resolve every finding. The reviewer independently reran all gates and reported no remaining runtime, API, or architecture blocker.

GitHub-hosted Windows/macOS/Linux and Python 3.13/3.14 jobs have not run for these changes. No cross-platform pass claim is made.
## M2-01 full local validation — 2026-08-05, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 0 | 66 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 334 tests passed in 3.16 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.30 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |

The new focused canonical-command/architecture suite reported 45 passing tests
in 0.50 seconds before the full gate. This evidence establishes M2-01 only; no
atomic apply, receipt, snapshot, replay, or CLI pass claim is made yet.

## M2-02 full local validation — 2026-08-05, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 0 | 73 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 351 tests passed in 3.44 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.31 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |

Focused M2-02 transaction and generated reference-model tests passed before the
full gate. They cover stale-hash rejection, invalid-middle rollback, dry-run,
resource and tick staging, BaseException escape, allocator churn, limits,
thread ownership, and production/reference authority hashes. This is not yet a
receipt, snapshot, replay, CLI, package-build, or hosted-platform pass claim.

## M2-03 full local validation — 2026-08-05, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 0 | 76 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 357 tests passed in 3.36 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.31 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |

Focused receipt/diff tests passed before the full gate. They cover exact net
created/destroyed/changed entities, component field and row-epoch changes,
spawn-then-destroy audit behavior, dry-run/commit equivalence, canonical
rejected receipts, resource/tick changes, and pre-adoption receipt/diff limits.
This is not yet snapshot, replay, CLI, package-build, or hosted-platform
evidence.

## M2-04 full local validation — 2026-08-05, Windows, CPython 3.12

The first sandboxed combined gate could not initialize uv's user cache and did
not execute the uv-managed checks. The rerun used approved cache access. Its
first full pytest execution found a missing reference-model error whitelist
entry; that architecture-test defect was corrected, and the complete gate was
rerun from the beginning.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current; 39 packages resolved in 0.70 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | 80 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 373 tests passed in 3.64 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.33 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |

Focused random/snapshot tests reported 16 passes before the final full gate.
Coverage includes independent repeatable named streams, exact random
checkpoint continuation, allocator churn and future allocation, change epochs,
byte-identical round trips, resource/component migrations, malformed and
hash-mismatched payloads, semantic limits, invalid resource/random state, and
active-query atomic-load rejection. This is not yet replay, branch, CLI,
package-build, wheel-smoke, or hosted-platform evidence.

## M2-05 local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 0 | 82 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 381 tests passed in 3.74 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.33 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |

This evidence covers self-contained replay, checkpoints, hash divergence,
immutable parent-bound branches, and repeated replay. Later independent review
required additional one-tick branch-boundary and composition corrections, so
the final M2 evidence supersedes this slice result.

## M2 final review-candidate source gate — 2026-08-05, Windows, CPython 3.12.13

Review-driven fixes added exact command equality and operation dispatch,
exhaustive resource roles, detached session views, project-bound snapshots,
excluded-resource preservation, strict checkpoint/schema invariants, one-tick
replay boundaries, bounded handle reads, and stronger architecture guards.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 0 | 88 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 430 tests passed, 1 skipped in 8.46 seconds. The skip is the Windows symlink-capability test for an account that cannot create file symlinks. |

This is source-gate evidence for the review candidate, not the final M2
artifact/benchmark/hosted-platform claim. Documentation, build, wheel smoke,
benchmark validation, scans, independent resnapshot, and hosted CI remain to be
recorded after they execute on the final cut.

## M2 final local validation — 2026-08-05, Windows, CPython 3.12.13

The first full pytest attempt on the final review cut reported six failures
because an established component-version error-message regex no longer matched.
The signed-64 validation behavior was correct; stable wording was restored and
the complete gate below was rerun. No pass is claimed for that failed attempt.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current; 39 packages resolved in 0.74 milliseconds. |
| `uv sync --frozen --all-groups` | 0 | Frozen environment checked 39 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | 88 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 444 tests passed and one Windows symlink-capability test skipped in 8.15 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built in 0.36 seconds; Material printed its documented upstream MkDocs 2.0 warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated installed-wheel version, doctor, headless, command, receipt, snapshot, replay, branch, and diff workflow smoke passed. |
| `uv run --frozen python benchmarks/benchmark_m2.py --samples 30 --seed 1 --json-out .tmp/m2-benchmark.json` | 0 | Recorded 30 retained samples after three warmups for all four versioned informational workloads. |
| `uv run --frozen python benchmarks/validate_m2_results.py .tmp/m2-benchmark.json` | 0 | Validated four informational M2 workloads with no timing targets. |
| `git diff --check` | 0 | No whitespace errors. |
| `git diff --cached --check` | 0 | The complete staged 61-file milestone diff has no whitespace errors. |
| Credential-pattern scan | 1 | No private-key, AWS key, GitHub token, or Slack token pattern matched project files; ripgrep uses exit 1 for no matches. |
| Backend/native import scan | 1 | No wgpu, GLFW, NumPy, Rust, Box2D, or MCP import matched source, tests, examples, benchmarks, or scripts; ripgrep uses exit 1 for no matches. |
| Wheel content listing | 0 | Pure-Python wheel contains only the typed `ludoweave` package, distribution metadata, entry point, LICENSE, and NOTICE; no tests, generated docs, native objects, or credentials are packaged. |

The final 30-sample local duration p50/p95 values were 30.2751/33.7076 ms
for canonical 100-command round trips, 13.9896/16.9751 ms for atomic
100-command apply, 17.1209/18.0412 ms for 1,000-entity snapshot round trips,
and 216.5521/271.2240 ms for verified 100-batch replay. These are local
profiling observations, not timing targets or cross-platform performance claims.

Independent final code/security review reran Ruff, Pyright, the complete test
suite, strict documentation, a minimal benchmark/validator, and diff checks. It
reported no remaining P0, P1, or P2 actionable finding. Trusted author codecs,
migrations, and tick executors plus a trusted/quiescent local project tree remain
documented boundaries. Hosted M2 CI has not yet run, so no new hosted-platform
claim is made.

## M2 hosted validation — GitHub Actions run 30947073913

The DCO-signed M2 commit `6bf3f99e94e30e4204af221064331e4b01c487dc`
was pushed to `codex/m2-command-transaction-replay` and published as stacked
pull request #2 against the open M1 branch. The resulting least-privilege CI
run completed successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright, and strict MkDocs gates. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three matrix jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both matrix jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both matrix jobs passed. |
| Installed wheel — Ubuntu/Windows/macOS, Python 3.12 | All three build and isolated installed-wheel workflow smoke jobs passed. |

All 11 jobs in run `30947073913` passed. This supplies the cross-platform M2
evidence that was deliberately not claimed by the local gate.

## M3 local validation — 2026-08-05, Windows, CPython 3.12.13

Development-focused renderer checks reached 51 passes, then the graphics-enabled
full suite reached 484 passes and one existing Windows symlink-capability skip.
The final cut added the rotated-camera regression and produced the complete gate
below. An earlier real offscreen clear exposed wgpu-py 0.32's Windows queue
callback ABI mismatch; the exact adapter now contains and documents the native
device-poll workaround. The failing attempt raised typed
`render.device_lost`; no pass was claimed for it.

The first graphics-free `uv sync` attempt could not open uv's managed user cache
inside the filesystem sandbox and did not execute tests. The approved rerun
completed and removed `cffi`, `glfw`, `numpy`, `pycparser`, `rendercanvas`, and
`wgpu`, proving the optional dependency boundary:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv sync --frozen --all-groups` | 0 | Removed six graphics/provider packages from the base environment. |
| `uv run --frozen pytest -q` | 0 | 479 tests passed and two tests skipped: the Windows symlink capability and graphics-extra module capability. |

The real window composition was also executed outside the sandbox:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen --extra graphics python examples/hello_sprite.py --width 16 --height 8 --window` | 0 | Created the rendercanvas/GLFW surface, submitted one draw with two sprite instances, completed the fence, emitted the versioned JSON summary, and closed. |

The final local gate used the locked graphics extra:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile resolved 46 packages in 0.70 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Frozen environment checked 45 packages in 2 milliseconds. |
| `uv run --frozen --extra graphics ruff format --check .` | 0 | 105 Python files were already formatted. |
| `uv run --frozen --extra graphics ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen --extra graphics pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen --extra graphics pytest -q` | 0 | 485 tests passed and one Windows symlink-capability test skipped in 13.72 seconds. This includes five real offscreen wgpu/example tests. |
| `uv run --frozen --extra graphics mkdocs build --strict` | 0 | Documentation built in 0.36 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and pure `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen --extra graphics python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency wheel smoke passed version, doctor, M0-M2 workflows, package/render imports, and structured missing-graphics diagnostics. |
| `uv run --frozen --extra graphics python benchmarks/benchmark_m3.py --samples 30 --output .tmp/m3-benchmark-final.json` | 0 | Recorded 30 retained samples after three warmups for all six M3 workloads. |
| `uv run --frozen --extra graphics python benchmarks/validate_m3_results.py .tmp/m3-benchmark-final.json` | 0 | Validated all workload schemas, distributions, exact dependency versions, sanitized metadata, one-draw invariants, and two target observations; zero targets were met. |
| `git diff --check` | 0 | No whitespace errors in the tracked diff. |

The final Windows/CPython 3.12.13 local duration observations were:

| Workload | p50 | p95 | p99 | Draws | 3 ms target |
| --- | ---: | ---: | ---: | ---: | --- |
| Extraction/packing, 1,000 sprites | 3.2777 ms | 3.6115 ms | 4.1763 ms | 1 | Not assigned |
| Extraction/packing, 10,000 sprites | 35.4460 ms | 41.9722 ms | 51.8362 ms | 1 | Not observed |
| Null submission, 1,000 sprites | 0.0081 ms | 0.0124 ms | 0.0465 ms | 1 | Not assigned |
| Null submission, 10,000 sprites | 0.0077 ms | 0.0084 ms | 0.0085 ms | 1 | Not assigned |
| wgpu CPU submission, 1,000 sprites | 0.5095 ms | 0.8001 ms | 0.8055 ms | 1 | Not assigned |
| wgpu CPU submission, 10,000 sprites | 5.3753 ms | 6.5363 ms | 6.9215 ms | 1 | Not observed |

The misses are recorded performance risks, not compatibility failures, target
passes, cross-platform claims, or authorization for native acceleration.

A separate final audit found no credential/private-key pattern. The backend
import scan found only the three expected wgpu/rendercanvas imports inside
`ludoweave.render.backends.wgpu`; no NumPy, MCP, Box2D, Rust/PyO3, or arbitrary
evaluation import/call entered source/examples/benchmarks/scripts. The wheel
listing contains only the typed package, metadata, entry point, LICENSE, and
NOTICE; it contains no native objects, tests, generated docs, or credentials.
## M3 hosted validation — GitHub Actions runs 30951328011 and 30993554807

The DCO-signed M3 implementation commit
`230687b16dfc02a8d2762af66f6bf2db4ef87f21` was pushed to
`codex/m3-rendering-vertical-slice` and published as stacked PR #3 against the
M2 branch. Initial run `30951328011` was not green and is not reported as a
pass: all base test and wheel jobs plus Windows/macOS graphics passed, while
strict Pyright failed because the quality job had not installed optional
provider packages and Ubuntu graphics failed with the typed
`render.adapter_unavailable` outcome because the runner had no usable graphics
driver.

Correction commit `6e6cea0bd80450a4d5b59cc1ff2e9f27a4195a92`
installs the already locked `graphics` extra in the quality job and installs
`libvulkan1` plus `mesa-vulkan-drivers` only on the Ubuntu graphics runner.
Local strict Pyright remained green before publication. Corrected run
`30993554807` then completed successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright with the optional adapter installed, and strict MkDocs. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three base jobs passed without the graphics extra. |
| Tests — Windows, Python 3.12/3.14 | Both base jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both base jobs passed. |
| Installed wheel — Ubuntu/Windows/macOS, Python 3.12 | All three pure-wheel/no-dependency workflow smokes passed. |
| Graphics smoke — Ubuntu/Windows/macOS, Python 3.12 | All three real clear, instanced sprite, capture, resize/minimize, and loss fixtures passed; Ubuntu used the explicitly provisioned Mesa Vulkan software runtime. |

All 14 jobs in run `30993554807` passed. This supplies the cross-platform M3
evidence that was deliberately not claimed by the local gate.

## M4 final local validation — 2026-08-05, Windows, CPython 3.12.13

Focused input, asset, audio, collision, and architecture tests passed 73 tests.
The Clockwork Arena integration suite passed four tests in 28.70 seconds,
including the exact 3,600-tick fixture, an independently recorded 3,600-tick
input replay with the same state hash, replay checkpoints, and presentation
nonmutation.

The real renderer compositions were executed with the locked graphics extra:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu submitted three draws containing 16 total sprite instances. The capture SHA-256 was `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; the exact final state hash was `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 10 --renderer wgpu --window --interactive` | 0 | The GLFW window path processed platform input, submitted 10 draws containing 40 total sprite instances, and closed with state hash `sha256:8dec596fd7492b86e30a4c00409ce447c515548b79005a544ef8a2af8bd39fa6`. |

The complete local quality and package gate then passed:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile resolved 46 packages in 0.72 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Frozen environment checked 45 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | 125 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 516 tests passed and one existing Windows symlink-capability test skipped in 45.39 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.44 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and pure `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installed-wheel smoke passed version, doctor, existing workflows, and M4 Arena/audio/collision checks outside the source tree. |
| `uv run --frozen python benchmarks/benchmark_m4.py --samples 300 --warmups 60 --output .tmp/m4-benchmark.json` | 0 | Recorded 300 retained samples after 60 warmups at stress levels 1, 4, and 8 with fixed seed, raw durations, final metrics, and state hashes. |
| `uv run --frozen python benchmarks/validate_m4_results.py .tmp/m4-benchmark.json` | 0 | Validated artifact schema, sample distributions, metadata, workload integrity, and all three final summaries; the baseline target observation was true. |
| `git diff --check` | 0 | No whitespace errors in the complete tracked diff. |

The final M4 benchmark retained 300 samples after 60 warmups for each workload.
Its artifact validator returned
`{"baseline_target_observed":true,"schema":"ludoweave.benchmark.m4/1","valid":true,"workloads":3}`.

| Workload | p50 | p95 | p99 | Target |
| --- | ---: | ---: | ---: | --- |
| Clockwork Arena, stress 1 | 1.5228 ms | 2.1228 ms | 2.5898 ms | p95 < 16.666667 ms observed |
| Clockwork Arena, stress 4 | 2.1822 ms | 3.5029 ms | 4.3358 ms | Not assigned |
| Clockwork Arena, stress 8 | 2.6362 ms | 4.8371 ms | 5.7986 ms | Not assigned |

The exact 3,600-tick fixture records 35 enemies spawned, three destroyed, 300
score, 360 shots, 12 waves, 12 remaining player health, and state hash
`sha256:4243defe548ba6e36b6bec93b45f266d2ad48e74c24efc2856d3f7c6197a3b6e`.
Architecture, credential, dynamic-evaluation, native/backend, Box2D, MCP,
network, and editor scans found no unapproved dependency or capability. Wheel
inspection found the new assets, audio, collision, platform, and sample modules
as pure Python, with no provider objects, tests, docs, or native artifacts.
M4 hosted CI has not yet run, so no cross-platform M4 pass is claimed here.

## M4 hosted validation — GitHub Actions run 30996905660

The DCO-signed M4 implementation commit
`e46bceec62fb20886fbb705149b07d083f4a46de` was pushed to
`codex/m4-clockwork-arena` and published as stacked pull request #4 against the
validated M3 branch. The resulting least-privilege CI run completed
successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright with the optional graphics adapter installed, and strict MkDocs gates. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three base matrix jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both base matrix jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both base matrix jobs passed. |
| Installed wheel — Ubuntu/Windows/macOS, Python 3.12 | All three pure-wheel/no-dependency workflow smokes passed, including the installed M4 Arena/audio/collision checks. |
| Graphics smoke — Ubuntu/Windows/macOS, Python 3.12 | All three real graphics fixtures and the Clockwork Arena wgpu vertical-slice command passed; Ubuntu used the explicitly provisioned Mesa Vulkan software runtime. |

All 14 jobs in run `30996905660` passed. This supplies the cross-platform M4
evidence that was deliberately not claimed by the local gate.

## M5 final local validation — 2026-08-05, Windows, CPython 3.12.13

Focused service, MCP, CLI, architecture, and real graphics tests were run while
the slice was developed. One initial rate-window assertion exposed an incorrect
zero-time threshold and one initial sample composition exposed postponed
component annotations; both attempts failed and were corrected before any pass
was claimed. The final audit also found that successful-result redaction covered
tokens/passwords but not API-key and authorization-shaped fields explicitly;
the redactor and regression test were strengthened, then the entire gate was
rerun on the exact final tree.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile resolved 46 packages in 0.76 milliseconds. No dependency change was required. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Frozen environment checked 45 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 137 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 545 tests passed and one existing Windows symlink-capability test skipped in 51.70 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Final documentation built successfully in 0.47 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and pure `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency wheel smoke passed existing workflows plus installed `agent` receipt equivalence, MCP stdio lifecycle/discovery, and the full Agent World Builder loop with a provider-neutral fake capture. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The real wgpu composition created six entities, committed create/adjust transactions and three ticks, captured 320x180 RGBA8, passed all registered checks, and recorded five replay batches. Final state hash: `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`; replay hash: `sha256:95d9c87ecd826c1bf33b72ded0779fff02488c08c169735f6c3083638eb45893`. |
| `git diff --check` | 0 | No whitespace errors in the complete tracked diff. |

The final source scan found no credential/private-key literal; matches were
policy text, redaction fixtures, or existing token terminology. Agent source
contains no evaluation primitive. The MCP adapter contains no socket, HTTP, or
network-framework import. Provider imports remain confined to
`ludoweave.render.backends.wgpu`; the sample selects that adapter only at its
composition root. Wheel inspection found only pure Python package files,
metadata, the console entry point, LICENSE, and NOTICE—no native objects, tests,
generated docs, credentials, or mandatory graphics dependency.

Hosted M5 CI had not yet run at the time of the local gate, so that section made
no cross-platform claim.

## M5 hosted validation — GitHub Actions run 30999777517

The DCO-signed M5 implementation commit
`b85bfcd13c56d6ffcfc292823c6e0be33c78f945` was pushed to
`codex/m5-agent-control` and published as stacked pull request #5 against the
validated M4 branch. The resulting least-privilege CI run completed
successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright with the optional graphics adapter installed, and strict MkDocs gates. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three base matrix jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both base matrix jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both base matrix jobs passed. |
| Installed wheel — Ubuntu/Windows/macOS, Python 3.12 | All three pure-wheel/no-dependency smokes passed, including installed agent receipt, MCP stdio, and Agent World Builder checks. |
| Graphics smoke — Ubuntu/Windows/macOS, Python 3.12 | All three real graphics fixtures and the Agent World Builder wgpu composition passed; Ubuntu used the explicitly provisioned Mesa Vulkan software runtime. |

All 14 jobs in run `30999777517` passed. This supplies the cross-platform M5
evidence that was deliberately not claimed by the local gate.

## M6 final local validation — 2026-08-05, Windows, CPython 3.12.13

Focused development checks first passed the deterministic artifact, API
metadata, and release-workflow contracts: five release/workflow tests passed,
two API-stability tests passed, strict Pyright reported no findings, and the
dependency-free `examples/alpha_acceptance.py` returned status `ok` with four
engine ticks, 120 Arena ticks, three agent ticks, five replay batches, and all
registered agent tests passing.

The first default-sandbox invocations of `uv lock --check`, `uv sync`, and
`uv build` each exited 1 because the sandbox could not open uv's managed user
cache. The exact commands were rerun with access to that existing cache and
passed. This was an execution-environment restriction, not recorded as a
project pass.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Final rerun resolved 46 packages in 0.77 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Final frozen rerun checked 45 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 143 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 552 tests passed and one existing Windows symlink-capability test skipped in 45.79 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.44 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and pure `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installed-wheel version, doctor, M0-M5 workflow, agent, MCP, and sample checks passed outside the source tree. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/release-candidate-final --tag v0.1.0a1` | 0 | Staged ten files: wheel, sdist, fixed-timestamp sample ZIP, LICENSE, NOTICE, optional-dependency notices, release notes, manifest, SPDX SBOM, and exact checksum inventory. |
| `uv run --frozen python scripts/smoke_release.py .tmp/release-candidate-final` | 0 | Exact checksum and manifest coverage, SBOM identity, required notices, safe sample extraction, isolated wheel install, CLI/doctor, and bundled headless examples passed for `0.1.0a1`. |
| `git diff --check` | 0 | No whitespace errors in the complete tracked diff before the factual evidence update. |

Wheel inspection found only the typed pure-Python `ludoweave` package,
distribution metadata, console entry point, LICENSE, and NOTICE. The sample ZIP
contains the eight documented example files plus the Clockwork Arena asset,
all beneath one versioned directory with fixed timestamps. A credential-prefix
scan found no key/token/private-key material. Provider imports remain confined
to `ludoweave.render.backends.wgpu`; no Rust, PyO3, Box2D, new networking,
editor, native object, or mandatory runtime dependency was introduced.

No M6 benchmark was run because the milestone changes distribution,
compatibility metadata, documentation, and community workflow rather than a
performance-sensitive runtime path. No new timing claim is made. At the time
of this local section, hosted M6 CI had not run, so no cross-platform result was
claimed there.

## M6 hosted validation — GitHub Actions run 31002365370

The DCO-signed M6 implementation commit
`84cc318c7c14ccbd2efbda6b61e19cec7c375612` was pushed to
`codex/m6-release-hardening` and published as stacked pull request #6 against
the validated M5 branch. The least-privilege CI run completed successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright with the optional adapter installed, and strict MkDocs. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both jobs passed. |
| Installed release candidate — Ubuntu/Windows/macOS, Python 3.12 | All three built the pure wheel/sdist, passed installed-wheel smoke, staged the 10-file candidate, and passed checksum/manifest/SBOM/notice/bundled-sample smoke. |
| Graphics smoke — Ubuntu/Windows/macOS, Python 3.12 | All three real graphics fixtures, Clockwork Arena wgpu run, and Agent World Builder loop passed; Ubuntu used the explicitly provisioned Mesa Vulkan software runtime. |

All 14 jobs passed. Six jobs printed non-failing setup-uv annotations because a
parallel job had already reserved the same cache key; no validation step or
job failed. This supplies the cross-platform M6 artifact evidence deliberately
not claimed by the local-only section.

## M7 final local validation — 2026-08-05, Windows, CPython 3.12.13

M7 profiles the inherited M1/M3 target misses and decides whether the first
Rust/PyO3 kernel satisfies the project admission gate. The decision is a
deferral: no native source, build tool, artifact, dependency, storage object,
or public API was added.

Development feedback was retained rather than reported as a pass:

- The initial profiler quality check exited 1: two new files required Ruff
  formatting and strict Pyright reported 11 `pstats`/unknown-container findings.
  A typed protocol view and explicit container narrowing resolved them.
- The first base-profile command in the default sandbox exited 1 because uv
  could not open its existing user cache. The authorized rerun generated the
  artifact, but its validator exited 1 on the profiler's `python.~` built-in
  record. Built-ins and raw memory-address text are now normalized; the exact
  base and graphics artifacts then validated.
- The first new extraction regressions had two incorrect detail-container
  assertions and four corresponding Pyright findings; they were corrected to
  inspect the immutable detail pairs as a mapping before the focused pass.
- One focused pytest invocation named a nonexistent property-test path and
  exited before collection; the corrected real query/reference/property set
  passed 20 tests.
- The first sprite-packer quality command reported one Ruff import-order
  finding. The mechanical import fix was applied before the final gate.

The final executed command evidence is:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the existing 46-package lock in 0.76 milliseconds; no dependency changed. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked the locked 45-package environment in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 148 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 564 tests passed and one existing Windows symlink-capability test skipped in 46.11 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.45 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv run --frozen python -m benchmarks.profile_m7 --repeats 5 --output .tmp/m7-profile-base-final.json` | 0 | Recorded the exact 10,000-entity simulation and 10,000-sprite extraction/packing profiles under `ludoweave.profile.m7/1`. |
| `uv run --frozen python -m benchmarks.validate_m7_profile .tmp/m7-profile-base-final.json` | 0 | Validated both base workload identities, parameters, invariants, calls, sanitized metadata, and canonical hotspot order. |
| `uv run --frozen --extra graphics python -m benchmarks.profile_m7 --repeats 5 --include-wgpu --output .tmp/m7-profile-graphics-final.json` | 0 | Recorded the two base workloads plus exact 10,000-sprite wgpu CPU submission with engine-owned capabilities. |
| `uv run --frozen python -m benchmarks.validate_m7_profile .tmp/m7-profile-graphics-final.json` | 0 | Validated all three graphics-profile workloads and sanitization contracts. |
| `uv run --frozen python benchmarks/benchmark_m1.py --samples 30 --seed 1 --json-out .tmp/m7-m1-benchmark-final.json` | 0 | Recorded 30 retained samples for all seven M1 workloads after three warmups. |
| `uv run --frozen python benchmarks/validate_m1_results.py .tmp/m7-m1-benchmark-final.json` | 0 | Validated seven workloads and two target records; only the 3,600-tick headless target was observed. |
| `uv run --frozen --extra graphics python benchmarks/benchmark_m3.py --samples 30 --output .tmp/m7-m3-benchmark-final.json` | 0 | Recorded 30 retained samples for all six M3 workloads after three warmups. |
| `uv run --frozen --extra graphics python benchmarks/validate_m3_results.py .tmp/m7-m3-benchmark-final.json` | 0 | Validated six workloads and two target records; neither 10,000-sprite target was observed. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and pure `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installed-wheel smoke passed outside the source tree. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m7-release-candidate-final` | 0 | Staged the complete 10-file alpha candidate with deterministic sample ZIP, manifest, SPDX SBOM, notices, and checksums. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m7-release-candidate-final` | 0 | Release checksum/manifest/SBOM/notices/sample extraction, isolated install, CLI, doctor, and bundled M0-M5 scenario smoke passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Six real wgpu clear/sprite/capture/resize/loss tests passed in 5.56 seconds. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu run completed 30 ticks with three draws and 16 submitted sprite instances. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320×180 RGBA8, passed registered tests, and recorded five replay batches. |
| `git diff --check` | 0 | No whitespace errors remained after the factual state update. |

### M7 final local performance observations

| Workload | p50 | p95 | p99 | Target observation |
| --- | ---: | ---: | ---: | --- |
| 10,000-entity simulation tick | 130.1806 ms | 144.0474 ms | 150.6699 ms | `< 4 ms`: not observed |
| 10,000-sprite extraction/packing | 20.8641 ms | 30.6902 ms | 31.4777 ms | `< 3 ms`: not observed |
| 10,000-sprite wgpu CPU submission | 2.8678 ms | 5.1918 ms | 5.2584 ms | `< 3 ms`: not observed |

Against the earlier same-machine records, those p95 values are lower by
26.83%, 26.88%, and 20.57%, respectively. They remain local observations and
are not cross-platform timing claims. Profiler totals include instrumentation
overhead and are not benchmark/frame durations.

The five-repeat graphics profile attributes overlapping cumulative time as
follows: simulation `_open_query` about 55% and component preparation about
47%; extraction interpolation/record construction about 42% and packing about
8%; wgpu submission packing about 86%. The strongest narrow-looking candidate
still reads nested Python objects and cannot release the GIL without a prior
scalar-buffer conversion. RFC-0001 records the missing build, owner, buffer,
GIL, cross-platform, and conformance fields and defers native acceleration.

The final repository/wheel audit found no Cargo manifest, Rust source, direct
NumPy/PyO3/Rust import, credential/private-key literal, native artifact, or new
mandatory dependency. Provider imports remain confined to the existing exact
wgpu adapter. The wheel contains only the typed pure-Python package,
distribution metadata/entry point, LICENSE, and NOTICE. Hosted M7 CI had not
run at the time of this local section, so no cross-platform result is claimed.

## M7 hosted validation — GitHub Actions run 31005165849

The DCO-signed M7 implementation commit
`b14e6c5581e2ca797adc9d71e46d460b941005b8` was pushed to
`codex/m7-performance-decision` and published as stacked pull request #7
against the validated M6 branch. The least-privilege pull-request run completed
successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright, strict MkDocs, and the exact base profiling-contract smoke. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three base matrix jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both base matrix jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both base matrix jobs passed. |
| Installed release candidate — Ubuntu/Windows/macOS, Python 3.12 | All three built the pure wheel/sdist, passed installed-wheel smoke, staged the complete candidate, and passed release smoke. |
| Graphics smoke — Ubuntu/Windows/macOS, Python 3.12 | All three passed real clear/sprite/capture/resize/loss tests, exact wgpu profiling-contract smoke, Clockwork Arena, and Agent World Builder; Ubuntu used Mesa Vulkan. |

All 14 jobs passed. Run `31005165849` completed with conclusion `success` for
head `b14e6c5581e2ca797adc9d71e46d460b941005b8`. GitHub reports PR #7 open,
mergeable, and `CLEAN` against `codex/m6-release-hardening`. The hosted
profiling steps validate portable execution and artifact contracts only; they
do not create uncontrolled cross-platform timing claims.

Before the hosted-evidence commit, `uv run --frozen mkdocs build --strict` and
`git diff --check` both exited 0; documentation built in 0.55 seconds with only
the already-recorded upstream Material/MkDocs 2.0 informational warning.

## M8 final local validation — 2026-08-05, Windows, CPython 3.12.13

This executed gate was superseded after independent review found three
blocking adapter defects: production window focus was not translated, a GLFW
C-level query error could be mistaken for disconnection, and an unavailable
trigger axis could become a false half press. Its results remain factual
historical evidence but are not the final M8 acceptance evidence.

M8 adds provider-neutral standardized gamepad input and decides whether an
SDL3 adapter is mature enough for the supported alpha baseline. ADR-0023
defers SDL3: the current SDL-listed Python binding is Beta and downloads native
binaries on first use by default, while the already-pinned GLFW dependency
supplies bounded standardized state without a new dependency.

Development feedback was retained rather than reported as a pass:

- The first focused Ruff invocation exited 1 on one export ordering and one
  import ordering finding; Ruff's deterministic fixes resolved both.
- The first focused gamepad test run reported 47 passes and one failure because
  structured error details are immutable pairs rather than a mapping; the
  assertion now copies them through `dict()`.
- The first strict Pyright run after that correction reported two protocol
  return-variance findings in the fake provider; exact `Sequence` annotations
  resolved them.
- A later format check exited 1 on one architecture-test layout and the file
  was formatted before the final gate.
- The first default-sandbox `uv lock --check` and `uv build` invocations each
  exited 1 because the sandbox could not open uv's existing user cache. The
  exact commands were rerun with access to that cache and passed. This was an
  execution-environment restriction, not a project failure.

The final executed command evidence is:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Authorized rerun resolved the unchanged 46-package lock in 1 millisecond. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked all 45 locked environment packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 149 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 589 tests passed and one existing Windows symlink-capability test skipped in 48.24 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.53 seconds with only the already-recorded upstream Material/MkDocs 2.0 informational warning. |
| `uv build` | 0 | Authorized rerun built `ludoweave-0.1.0a1.tar.gz` and pure `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency installed-wheel smoke passed, including typed gamepad events, deadzone mapping, and Null-provider lifecycle. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m8-release-candidate-local` | 0 | Staged the complete 10-file `ludoweave.release-stage/1` alpha candidate. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m8-release-candidate-local` | 0 | Checksum, manifest, SPDX SBOM, notice, sample, isolated install, CLI, doctor, and bundled workflow smoke passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Eight real wgpu tests passed, including the provider-free device result and a real GLFW null-platform gamepad poll. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu completed 30 ticks, three draws, 16 sprite instances, and deterministic state/capture hashes. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320×180 RGBA8, passed registered tests, and recorded five replay batches. |
| `uv run --frozen python examples/alpha_acceptance.py` | 0 | The dependency-free acceptance composition returned `status: ok` with four engine ticks, 120 Arena ticks, three agent ticks, and five replay batches. |
| `git diff --check` | 0 | No whitespace errors existed before the factual state/evidence update. |

The final source scan found no introduced credential value, SDL/PySDL3 import,
native artifact, or new dependency. The only provider imports remain inside
`ludoweave.render.backends.wgpu`; architecture fixtures now reject SDL and
PySDL3 imports as well as the existing banned roots. Gamepad events carry only
bounded slots, engine enums, booleans, and normalized floats. Provider names,
GUIDs, timestamps, native objects, and hardware capabilities remain outside
canonical state and public values.

No M8 benchmark was run because polling is bounded to 16 logical slots and the
milestone adds input contracts/adapter translation rather than a frame-scale
simulation or extraction workload. No timing claim is made. Hosted M8 CI has
not run, so no cross-platform M8 pass is claimed here.

## M8 corrected final local validation — 2026-08-05, Windows, CPython 3.12.13

The review-blocking focus, provider-error, and trigger-neutrality defects were
corrected before publication. GLFW focus transitions are prepended during
production surface draining, gamepad and focus queries clear and check the
calling-thread GLFW error state, and GLFW emits only its unambiguous buttons
and four stick axes. The public provider contract retains trigger events for a
future provider that can distinguish capability and neutral state safely.

Development feedback in the corrected pass was retained:

- The first focused Ruff check exited 1 for an import-order finding and one
  stale internal protocol name. Ruff organized the imports and the cast now
  uses `_GlfwGamepadApi`.
- The first strict Pyright pass after adding the focus fake exited 1 with five
  invariant protocol-constant findings. Explicit `ClassVar[int]` annotations
  resolved them.
- The default-sandbox `uv lock --check` and
  `uv sync --frozen --all-groups --extra graphics` commands exited 1 because
  uv's existing user cache was inaccessible. The exact commands passed when
  rerun with authorized cache access; no lock or dependency changed.

The corrected final executed command evidence is:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Authorized rerun resolved the unchanged 46-package lock in 0.72 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Authorized rerun checked all 45 locked environment packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 149 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 594 tests passed and one existing Windows symlink-capability test skipped in 45.16 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.53 seconds with only the already-recorded upstream Material/MkDocs 2.0 informational warning. |
| `uv build` | 0 | Authorized run built `ludoweave-0.1.0a1.tar.gz` and `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency installed-wheel smoke passed, including the M8 gamepad contract. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m8-release-candidate-corrected` | 0 | Staged the complete 10-file `ludoweave.release-stage/1` candidate. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m8-release-candidate-corrected` | 0 | Checksum, manifest, SPDX SBOM, notice, sample, isolated install, CLI, doctor, and bundled workflow smoke passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Eight real wgpu tests passed, including provider-free and real GLFW null-platform gamepad polling. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu completed 30 ticks, three draws, 16 sprite instances, and deterministic state/capture hashes. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320×180 RGBA8, passed registered tests, and recorded five replay batches. |
| `uv run --frozen python examples/alpha_acceptance.py` | 0 | The dependency-free acceptance composition returned `status: ok` with four engine ticks, 120 Arena ticks, three agent ticks, and five replay batches. |
| PowerShell wheel ZIP inventory | 0 | The built wheel contained 79 entries and zero `.pyd`, `.so`, `.dll`, or `.dylib` entries. |
| `git diff --check` | 0 | No whitespace errors existed after final evidence reconciliation. |

Repeat independent review executed 113 focused unit/architecture tests, two
real gamepad integration selections, Ruff formatting/linting, Pyright, and
`git diff --check`; all passed. It also reproduced an uninitialized pinned
GLFW query becoming structured `platform.gamepad_provider_failure` code 65537.
The reviewer found no remaining blocker, provider/native leakage, credential
exposure, authority violation, dependency drift, or lifecycle/concurrency
regression and recommended M8 for commit and PR.

No M8 benchmark was run and no performance statement is made.

## M8 hosted validation — 2026-08-05

Commit `2a654e03005481d61c6cbeb054b31e260b960659` was pushed to
`codex/m8-gamepad-sdl3-evaluation` and published as ready PR #9 against
`main`. GitHub reported the PR mergeable. Actions run `31012696753` completed
successfully with all 14 jobs passing:

- quality and strict documentation;
- Ubuntu CPython 3.12, 3.13, and 3.14;
- Windows CPython 3.12 and 3.14;
- macOS CPython 3.12 and 3.14;
- isolated installed-wheel smoke on Ubuntu, Windows, and macOS; and
- real graphics/gamepad smoke on Ubuntu, Windows, and macOS.

The hosted result validates execution and artifact contracts, not controller
hardware coverage or a performance target. PR #9 remains open and no merge,
tag, release, or package publication is claimed.

## M9 local validation — 2026-08-06, Windows, CPython 3.12.13

M9 evaluates `box2d-python==0.1.2` as an isolated candidate and does not add it
to project metadata, the uv lock, the package, or release dependencies. Primary
package evidence shows an early-development CFFI preview with partial Box2D
v3.0 functionality, no source distribution, CPython 3.12/3.13 wheels only,
macOS ARM64 wheels only, and no Trusted Publishing upload. Official Box2D is
now 3.1.0 and documents cross-platform determinism beginning in 3.1; that claim
is not attributed to this partial v3.0 community binding.

Development feedback is retained rather than reported as a pass:

- An initial CPython 3.12 candidate command used the tuple-position call shown
  on the PyPI example and exited 1 because the installed wheel required two
  position arguments. The corrected isolated call stepped successfully and
  also tolerated repeated `destroy()`.
- The first focused Ruff check found import ordering, a mutable test class
  attribute, and a missing exception import. These were corrected.
- The first focused pytest collection failed because the repository's
  `scripts` directory is not an import package. The test now invokes the real
  script in an isolated subprocess with a fake distribution instead of changing
  project import behavior.
- The first focused Pyright pass found two unsafe `object`-to-float conversions.
  The probe now explicitly validates finite numeric position values.
- A default-sandbox base-environment probe could not open uv's existing cache.
  The authorized exact rerun produced the expected structured `unavailable`
  document with child exit 2 and did not install the candidate.
- Independent review found that distribution metadata and the imported module
  were not yet linked, allowing a shadow `box2d.py` to be misattributed to
  version 0.1.2. The probe now matches the resolved module to the
  distribution's installed-file inventory before import, checks identity again
  after import, fails closed without paths, and has a shadow-module regression.
  It also requires at least one observed position change.

Candidate probe evidence:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --no-project --python 3.12 --with box2d-python==0.1.2 python scripts/probe_box2d_candidate.py --iterations 25 --steps 120` | 0 | Windows CPython 3.12.13 completed 25 single-thread create/step/double-destroy repetitions; exact traces matched with SHA-256 `c9e299e715c5f7a3654d7c5794d75347d765cc029b7991d4c8066dfaf7abdfc5`. |
| `uv run --no-project --python 3.13 --with box2d-python==0.1.2 python scripts/probe_box2d_candidate.py --iterations 25 --steps 120` | 0 | Windows CPython 3.13.13 produced the same exact bounded trace digest. |
| `uv run --no-project --python 3.14 --with box2d-python==0.1.2 python scripts/probe_box2d_candidate.py --iterations 25 --steps 120` | 1 | Resolution failed: the release has no matching `cp314` wheel and publishes only `cp312`/`cp313` ABI wheels. The probe did not run. |
| `uv run --frozen python scripts/probe_box2d_candidate.py --iterations 2 --steps 1` | 2 | The locked base environment emitted sanitized schema `ludoweave.evaluation.box2d/1` with status `unavailable`, confirming Box2D is not installed. |

The full executed repository gate is:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the unchanged 46-package lock in 0.73 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked all 45 locked environment packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 151 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | The ownership-corrected final run reported 606 tests passed and one existing Windows symlink-capability test skipped in 46.57 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.55 seconds with only the known upstream Material/MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and the pure `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installed-wheel smoke passed. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m9-release-candidate-reviewed-20260806` | 0 | The final post-review build staged the complete 10-file `ludoweave.release-stage/1` candidate. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m9-release-candidate-reviewed-20260806` | 0 | The final post-review checksum, manifest, SPDX SBOM, notice, sample, isolated install, CLI, doctor, and bundled workflow smoke passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Eight real wgpu/GLFW integration tests passed. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu completed 30 ticks, three draws, 16 sprite instances, and deterministic state/capture hashes. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320×180 RGBA8, passed registered tests, and recorded five replay batches. |
| `uv run --frozen python examples/alpha_acceptance.py` | 0 | The dependency-free acceptance composition returned `status: ok` with four engine ticks, 120 Arena ticks, three agent ticks, and five replay batches. |
| PowerShell wheel ZIP inventory | 0 | The built wheel contained 79 entries and zero `.pyd`, `.so`, `.dll`, or `.dylib` entries. |
| Runtime dependency scan | 1 | No case-insensitive Box2D name matched `src`, `pyproject.toml`, or `uv.lock`; ripgrep exit 1 means no matches. |
| Credential-pattern scan | 1 | No private-key header or simple credential assignment matched the reviewed M9 repository surfaces; ripgrep exit 1 means no matches. |
| `git diff --check` | 0 | No whitespace errors existed before factual evidence reconciliation. |

The Windows traces establish only bounded same-binary headless/lifecycle smoke.
No performance benchmark, cross-platform determinism, rollback, snapshot,
contact-order, GIL-release, thread-safety, free-threaded, or provider-support
claim is made.

Independent review initially blocked sign-off because metadata identity did not
prove ownership of the imported top-level module. After correction, repeat
review ran 54 focused tests, Ruff formatting/linting, strict Pyright,
`git diff --check`, the runtime/dependency scan, and an actual CPython 3.12
candidate probe. It verified the pre-import installed-file ownership check,
post-import identity check, structured broken-install behavior, and
non-executing shadow-module regression; no blocker remained and the reviewer
recommended M9 for final sign-off. Hosted M9 CI had not run at that point.

## M9 hosted validation — 2026-08-06

DCO-signed implementation commit
`8b429aaf07684651f6d538419701c049ee55fc4f` was pushed to
`codex/m9-box2d-plugin-evaluation` and published as ready stacked PR #10 against
the hosted-validated M8 branch. GitHub Actions run `31015885190` completed with
conclusion `success`; all 14 jobs passed:

- quality, lock, formatting, lint, strict Pyright, strict documentation, and
  base profiling-contract smoke on Ubuntu CPython 3.12;
- tests on Ubuntu CPython 3.12, 3.13, and 3.14;
- tests on Windows and macOS CPython 3.12 and 3.14;
- pure build, isolated wheel smoke, complete release staging, and release smoke
  on Ubuntu, Windows, and macOS; and
- real graphics/gamepad, profiling-contract, Clockwork Arena, and Agent World
  Builder smoke on Ubuntu, Windows, and macOS.

GitHub reports PR #10 open, ready, mergeable, and `CLEAN` against
`codex/m8-gamepad-sdl3-evaluation`, whose exact base is
`187ad4503a40325a1e334da3cb4078969e2e043b`. The hosted result validates project
execution and artifact contracts; it does not install the deferred candidate,
exercise controller hardware, or create Box2D performance/cross-platform
determinism claims. No merge, tag, release, or package publication occurred.

## M10 final local validation - 2026-08-06, Windows, CPython 3.12.13

M10 adds one finite headless semantic inspector over an owned local MCP child.
It introduces no runtime dependency, listener, arbitrary process command,
editor, second world store, native code, or release publication.

Development and review feedback is retained rather than reported as a pass:

- The first focused Ruff run found one set-comparison simplification and the
  first focused Pyright run found 19 strict typing issues in decoded JSON.
  Both were corrected before focused tests.
- After the CI job consolidation, the existing release-workflow architecture
  test failed because it still required three redundant wheel jobs. The test
  now asserts one complete distribution gate, the reduced compatibility
  matrix, and retained three-OS graphics coverage.
- Independent review blocked publication on four trust-boundary defects:
  inherited cwd/`PYTHONPATH` could shadow the child package, dash-prefixed
  project names could become child options, a top-level tick result could omit
  a valid receipt, and stream decode/read errors escaped structured handling.
  The child now uses `-I`, binds variable options with `=`, places the project
  after `--`, requires exactly one committed receipt with exact hash/tick
  continuity, and translates Unicode/I/O/closed-stream failures. Source and
  installed-wheel adversarial regressions cover every correction.
- During the adversarial correction pass, one import-order finding and three
  strict typing findings were corrected. The repeat focused gate then passed.
- Final CI review found that the consolidated baseline would duplicate real
  wgpu execution without the dedicated Linux job's Mesa/Vulkan installation.
  Baseline pytest now excludes exactly `test_wgpu_render.py`; the three-OS
  graphics matrix remains its sole gate. Architecture assertions now protect
  least privilege, pins, timeouts, caching, no credential persistence,
  fail-fast policy, cancellation, matrix size, and distribution commands.
- A default-sandbox `uv lock --check` attempt exited 1 because access to uv's
  existing user cache was denied. The approved exact rerun exited 0; this was
  an environment permission failure, not a lock failure.

Final executed repository gate:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | The unchanged lock resolved 46 packages in 0.79 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | The locked environment checked 45 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 154 Python files were formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 642 tests passed and one existing Windows symlink-capability test skipped in 49.09 seconds. |
| `uv run --frozen pytest -q --ignore=tests/integration/test_wgpu_render.py` | 0 | The exact consolidated baseline command passed 634 non-provider tests with one skip in 52.39 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | The final documentation build completed in 0.48 seconds with only the known Material/MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installation passed all inherited smoke plus M10 bootstrap/tick receipts and proved a cwd-shadowed `ludoweave` package was not executed. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m10-release-candidate-final-reviewed-20260806` | 0 | Staged the complete 10-file `ludoweave.release-stage/1` candidate. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m10-release-candidate-final-reviewed-20260806` | 0 | Checksum, manifest, SPDX SBOM, notices, sample bundle, isolated install, CLI, doctor, and bundled workflow smoke passed. |
| `uv run --frozen python -m benchmarks.profile_m7 --repeats 1 --output .tmp/m10-profile-base.json` plus validator | 0 | The retained two-workload base profiling contract validated. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Eight real wgpu/GLFW integration tests passed in 5.51 seconds. |
| `uv run --frozen --extra graphics python -m benchmarks.profile_m7 --repeats 1 --include-wgpu --output .tmp/m10-profile-graphics.json` plus validator | 0 | The retained three-workload graphics profiling contract validated. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu completed 30 ticks, three draws, 16 sprites, and the expected deterministic state/capture hashes. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320x180 RGBA8, passed registered tests, and recorded five replay batches. |
| `uv run --frozen python examples/alpha_acceptance.py` | 0 | Dependency-free acceptance returned `status: ok` with four engine ticks, 120 Arena ticks, three agent ticks, and five replay batches. |
| CI workflow YAML parse and quota contract | 0 | The workflow parsed with exactly eight jobs: one complete baseline, four compatibility, and three graphics jobs. Five focused release/workflow tests passed. |
| Wheel ZIP/metadata inventory | 0 | The wheel contains 80 entries, zero native entries, no mandatory runtime dependency, and only the three exact optional graphics requirements. |
| Local stdio network-import scan | 1 | No network-module import matched the inspector or MCP adapter; ripgrep exit 1 means no matches. |
| Local stdio dynamic-evaluation scan | 1 | No `eval`, `exec`, or `__import__` call matched the inspector or MCP adapter; ripgrep exit 1 means no matches. |
| Deferred-provider scan | 1 | No Box2D or SDL3 binding name matched package source, project metadata, or the lock; ripgrep exit 1 means no matches. |
| Credential-assignment scan | 1 | No credential assignment matched the reviewed M10 source, tests, scripts, docs, or workflow; ripgrep exit 1 means no matches. |
| `git diff --check` | 0 | No whitespace errors. |

The final focused inspector, architecture, and trust-boundary suite reported 81
passes. Repeat independent review reran that suite, Ruff, strict Pyright, and
diff checks, found no remaining implementation blocker, and approved the
corrected M10 head. The exact quota-conscious baseline and separately gated
graphics commands were then executed locally after CI review.

M10 has no benchmark or performance threshold. The retained M7 profiling
commands validate artifact behavior only; no timing result or performance pass
is claimed. Before PR publication, hosted M10 CI had not run and no M10
cross-platform or hosted pass was claimed.

## M10 hosted validation - 2026-08-06

DCO-signed implementation commit
`2e60b3f1c4884dba71df5f23b779bc49187d68c6` was pushed to
`codex/m10-live-semantic-inspector` and published as ready stacked PR #11
against exact final M9 head
`22bc2de9f8450f60fe483bd4fea10a86702d2f0f`. GitHub Actions run
`31020096463` completed with conclusion `success`; all eight jobs passed:

- the Ubuntu CPython 3.12 quality/test/distribution job passed lock,
  formatting, lint, strict Pyright, strict docs, 634-test baseline, base profile
  contract, pure build, isolated wheel smoke, release staging, and release
  smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profile contract, Clockwork Arena, and Agent World
  Builder passed on Ubuntu software Vulkan, Windows, and macOS.

GitHub reports PR #11 open, ready, mergeable, and `CLEAN` against
`codex/m9-box2d-plugin-evaluation`. This is the first run of the consolidated
eight-job topology; it replaces the former 14-job topology without dropping a
supported Python version, desktop operating system, complete distribution
gate, or real three-OS graphics gate. No merge, tag, release, or package
publication occurred.

## M11 focused development validation - 2026-08-06

Environment: Windows, uv-managed CPython 3.12.13. M11 is based on exact M10
evidence head `bae799900671481cfd6f03fe502dea95b2c7f96c` and is not yet
published. No hosted or milestone-complete claim is made.

- `uv run --frozen ruff format src/ludoweave/presentation src/ludoweave/audio examples/rich_2d_showcase.py scripts/smoke_wheel.py scripts/release_artifacts.py scripts/smoke_release.py tests`
  exited 0; 76 files were already formatted.
- `uv run --frozen ruff check src/ludoweave/presentation src/ludoweave/audio examples/rich_2d_showcase.py scripts/smoke_wheel.py scripts/release_artifacts.py scripts/smoke_release.py tests/unit/test_presentation.py tests/unit/test_audio.py tests/integration/test_rich_2d_showcase.py tests/architecture`
  exited 0 with `All checks passed!`.
- `uv run --frozen pyright src/ludoweave/presentation src/ludoweave/audio examples/rich_2d_showcase.py scripts/smoke_wheel.py scripts/release_artifacts.py scripts/smoke_release.py tests/unit/test_presentation.py tests/unit/test_audio.py tests/integration/test_rich_2d_showcase.py`
  exited 0 with zero errors, warnings, or information diagnostics.
- `uv run --frozen pytest -q tests/unit/test_presentation.py tests/unit/test_audio.py tests/integration/test_rich_2d_showcase.py tests/architecture`
  exited 0 with 76 passing tests in 1.40 seconds.

An earlier focused run exposed three lint defaults, one tuple return-type
annotation, and an incorrect newly authored particle digest fixture; a second
integration run corrected its expected lifetime count from eight to ten. Those
development failures are not pass evidence. The corrected commands above are
the current focused evidence. Full suite, strict docs, distribution/release,
graphics, independent review, and hosted validation remain pending.

## M11 final reviewed local validation - 2026-08-06

Environment: Windows, uv-managed CPython 3.12.13 with the exact locked graphics
extra. Base: `bae799900671481cfd6f03fe502dea95b2c7f96c`. Branch:
`codex/m11-rich-2d-modules`.

The final independently reviewed command sequence produced these results:

- `uv lock --check` exited 0; the 46-package lock was unchanged.
- `uv sync --frozen --all-groups --extra graphics` exited 0; 45 packages were
  checked.
- `uv run --frozen ruff format --check .` exited 0; 164 Python files were
  already formatted.
- `uv run --frozen ruff check .` exited 0 with `All checks passed!`.
- `uv run --frozen pyright` exited 0 with zero errors, warnings, or information
  diagnostics.
- `uv run --frozen pytest -q` exited 0 with 663 passing tests and one existing
  Windows symlink-capability skip in 46.37 seconds.
- `uv run --frozen mkdocs build --strict` exited 0 in 0.47 seconds. Material for
  MkDocs emitted its existing upstream MkDocs 2.0 informational warning.
- `uv build` exited 0 and rebuilt
  `dist/ludoweave-0.1.0a1.tar.gz` plus the universal
  `dist/ludoweave-0.1.0a1-py3-none-any.whl` from the sdist.
- `uv run --frozen python scripts/smoke_wheel.py dist` exited 0 with
  `wheel smoke passed: ludoweave-0.1.0a1-py3-none-any.whl`. The isolated
  no-dependency environment ran CLI/doctor, inherited scenarios, inspector,
  agent builder, and the M11 rich-2D example.
- `uv run --frozen python scripts/release_artifacts.py dist .tmp/m11-release-candidate-reviewed-20260806`
  exited 0 with protocol `ludoweave.release-stage/1`, version `0.1.0a1`, ten
  artifacts, the sample bundle, and SPDX SBOM.
- `uv run --frozen python scripts/smoke_release.py .tmp/m11-release-candidate-reviewed-20260806`
  exited 0 with `release smoke passed: ludoweave 0.1.0a1`; the extracted
  versioned bundle ran `rich_2d_showcase.py` from the installed wheel.
- `git diff --check` exited 0.

Additional retained-gate execution:

- `uv run --frozen python -m benchmarks.profile_m7 --repeats 1 --output .tmp/m11-profile-base.json`
  and its validator exited 0 with schema `ludoweave.profile.m7/1`, two valid
  workloads.
- `uv run --frozen --extra graphics python -m benchmarks.profile_m7 --repeats 1 --include-wgpu --output .tmp/m11-profile-graphics.json`
  and its validator exited 0 with the same schema and three valid workloads.
  These validate inherited artifact contracts only; M11 assigns no timing
  target and makes no performance claim.
- `uv run --frozen pytest -q tests/integration/test_wgpu_render.py` exited 0
  with nine passes in 5.52 seconds, including M11 animation/text/tile/particle
  extraction through the real provider.
- `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10`
  exited 0 with 30 ticks, three draws, 16 sprites, and capture SHA-256
  `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`.
- `uv run --frozen --extra graphics python examples/agent_world_builder.py`
  exited 0 with committed apply/adjust status, six query matches, three ticks,
  five replay batches, and passing registered tests.
- `uv run --frozen python examples/alpha_acceptance.py` exited 0 with protocol
  `ludoweave.sample.alpha_acceptance/1` and status `ok`.
- `uv run --frozen python examples/rich_2d_showcase.py --ticks 6` exited 0 with
  schema `ludoweave.example.rich_2d/1`, animation frame 0, audio gain 0.2, nine
  glyphs, ten particles, 20 sprite instances, eight tile instances, two draw
  calls, and particle digest
  `d3bb0b7050ec5f841de9f0b12997c9e9f4bdeb88f6a14024cd4554103beaa546`.

Artifact and scope audit:

- the wheel contains 87 entries, including all seven
  `ludoweave/presentation` files and zero `.pyd`, `.so`, `.dll`, `.dylib`,
  `.a`, or `.lib` entries;
- metadata has no mandatory `Requires-Dist`; only the unchanged exact graphics
  extra (`glfw`, `rendercanvas[glfw]`, `wgpu`) is present;
- the final release sample ZIP contains `rich_2d_showcase.py`;
- `.github/workflows/ci.yml` is unchanged, so the eight-job essential topology
  remains the only pull-request gate;
- focused scans found no M11 native/provider imports, presentation clock/global
  RNG/thread/network imports, high-confidence credentials, or new-file trailing
  whitespace; and architecture tests passed.

Independent findings-first review initially identified unreachable maximum
tile coordinates, unbounded/quadratic layer traversal, unbounded public
sequence freezing, missing runtime parent-bus fader propagation, particle
work/state bounds, and Ruff generic syntax. The fixes add edge, infinite-
iterator, work-budget, state-lifetime, canonical-order, and nested-gain
regressions. Final re-review reported no blocking, non-blocking, or open finding:
format and Ruff passed, Pyright reported zero, 78 focused tests and 58
architecture/API tests passed, provider isolation and deterministic showcase
passed, and diff/credential checks were clean. One parallel review invocation
collided with the root process on shared `.pytest-tmp` and produced 55 setup
errors; the isolated rerun passed all 78, so that collision is not pass
evidence.

An initial sandboxed full-gate attempt could not read the existing uv user
cache and therefore produced no check evidence. The exact approved reruns above
completed successfully. At this local-gate stage no M11 hosted, cross-platform,
merge, tag, release, or package-publication claim was made.

## M11 hosted validation - 2026-08-06

Ready stacked PR #12 targets `codex/m10-live-semantic-inspector` from
`codex/m11-rich-2d-modules`. GitHub Actions pull-request run `31024155710`
executed signed implementation commit
`aca6d93165a52d88451e8e06d5f1aa8d2e323f1d` and completed successfully from
`2026-08-05T16:12:36Z` through `2026-08-05T16:14:40Z`.

All eight essential jobs concluded `success`:

- `Quality, tests, and distribution` on Ubuntu with CPython 3.12 ran the
  lockfile, formatting, Ruff, Pyright, strict documentation, baseline tests,
  base profiling-contract smoke, sdist/wheel build, isolated-wheel smoke,
  release staging, and release smoke gates.
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14;
- real graphics smoke passed on Ubuntu, Windows, and macOS, including inherited
  clear/sprite/capture/resize/loss/gamepad coverage, graphics profiling,
  Clockwork Arena, and Agent World Builder.

The workflow file was unchanged by M11. This run is the only hosted run created
for the implementation commit. It validates the supported cross-platform
matrix and distribution/provider contracts; it does not merge PR #12, publish
a package, create a tag or release, or admit any deferred provider/native work.

## M12 final reviewed local validation - 2026-08-06

Environment: Windows 11, uv-managed CPython 3.12.13 with the exact locked
graphics extra. Base and current pre-commit `HEAD`:
`840a8b06d461fa1d5e649911b22f5995154728a7`. Branch:
`codex/m12-plugin-manifest-compatibility`.

The complete independently reviewed command sequence produced these results:

- The first sandboxed `uv lock --check` attempt exited 1 because the workspace
  sandbox denied access to uv's existing user cache. The approved exact rerun
  exited 0 and resolved the unchanged 46-package lock.
- `uv sync --frozen --all-groups --extra graphics` exited 0 and checked 45
  packages.
- `uv run --frozen ruff format --check .` exited 0; 170 Python files were
  already formatted.
- `uv run --frozen ruff check .` exited 0 with `All checks passed!`.
- `uv run --frozen pyright` exited 0 with zero errors, warnings, or information
  diagnostics.
- `uv run --frozen pytest -q` exited 0 with 741 passing tests and one existing
  Windows symlink-capability skip in 47.87 seconds.
- `uv run --frozen mkdocs build --strict` exited 0 in 0.50 seconds. Material for
  MkDocs emitted its existing upstream MkDocs 2.0 informational warning.
- `uv build` exited 0 and rebuilt
  `dist/ludoweave-0.1.0a1.tar.gz` plus the universal
  `dist/ludoweave-0.1.0a1-py3-none-any.whl` from the sdist.
- `uv run --frozen python scripts/smoke_wheel.py dist` exited 0 with
  `wheel smoke passed: ludoweave-0.1.0a1-py3-none-any.whl`; the isolated wheel
  check included the explicit M12 manifest and path-free compatible report.
- `uv run --frozen python scripts/release_artifacts.py dist .tmp/m12-release-candidate-final-reviewed-20260806`
  exited 0 with protocol `ludoweave.release-stage/1`, version `0.1.0a1`, ten
  artifacts, the versioned sample bundle, and SPDX SBOM.
- `uv run --frozen python scripts/smoke_release.py .tmp/m12-release-candidate-final-reviewed-20260806`
  exited 0 with `release smoke passed: ludoweave 0.1.0a1`; the extracted bundle
  checked `example.plugin.json` through the isolated installed wheel.
- `git diff --check` exited 0.

Provider and example acceptance:

- `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py`
  exited 0 with nine passes in 5.53 seconds.
- Null and real-wgpu `examples/clockwork_arena.py --ticks 600` runs both exited
  0 with the same authoritative state hash
  `sha256:b7a77c7fa0f0bab668245723719a4e57c00f5f821b4df8cf013dcf9aaaf34c70`;
  the wgpu run completed 600 draws and produced an offscreen capture.
- `uv run --frozen --extra graphics python examples/agent_world_builder.py`
  exited 0 with committed apply/adjust status, six query matches, three ticks,
  five replay batches, and passing registered tests.
- `uv run --frozen python examples/alpha_acceptance.py` exited 0 with protocol
  `ludoweave.sample.alpha_acceptance/1` and status `ok`.
- `uv run --frozen python examples/rich_2d_showcase.py --ticks 6` exited 0 with
  schema `ludoweave.example.rich_2d/1`, nine glyphs, ten particles, 20 sprite
  instances, eight tile instances, and two draw calls.
- `uv run --frozen ludoweave plugin check examples/example.plugin.json` exited
  0 with canonical protocol `ludoweave.plugin-check/1`, one compatible plugin,
  no issues or path, and manifest-set fingerprint
  `sha256:c2ed00ea4153e92aec46c5e80d22324656fe4009903c638544faa48cba9d24a2`.

Every benchmark/profile command in the README quality suite was also rerun
against uniquely named M12 artifacts and its validator exited 0:

- M1 recorded seven workloads. The fixed 3,600-tick p95 was 35,648,600 ns and
  observed its headless target; the 10,000-entity simulation p95 was
  118,236,300 ns and did not observe its inherited 4 ms target. The validator
  reported one of two recorded targets observed.
- M2 validated four informational workloads with no timing targets.
- M3 validated six workloads with zero of its two inherited timing targets
  observed.
- M4 validated three workloads; the baseline p95 was 1,824,800 ns and observed
  its 16,666,667 ns target.
- The five-repeat M7 base and real-wgpu profile artifacts validated with two
  and three workloads respectively. Profile timing is diagnostic only.

Artifact, scope, and history audit:

- the wheel contains 91 entries, including four `ludoweave/plugins` files and
  zero `.pyd`, `.so`, `.dll`, `.dylib`, `.a`, or `.lib` entries;
- wheel metadata has no mandatory dependency; its only `Requires-Dist` entries
  are the unchanged exact `graphics` extra for GLFW, rendercanvas, and wgpu;
- credential-assignment and plugin backend/discovery/evaluation/filesystem
  scans found no matches; ripgrep exit 1 means no matches;
- the CI workflow, `pyproject.toml`, and `uv.lock` are unchanged, retaining the
  eight essential hosted jobs and pure-Python package contract; and
- `HEAD`, local M11, and remote-tracking M11 all resolved to
  `840a8b06d461fa1d5e649911b22f5995154728a7` before the M12 commit. Merge-base
  matched exactly and the pre-commit left/right count was `0 0`, so the stack
  contains no missing or unrelated commit.

Independent findings-first review reproduced and drove regressions for bounded
cycle diagnostics, canonical detail/report limits, exact error types and
protocol values, mixed-key and pre-bound mapping validation, exact plugin
identities, deterministic immutable decision state, path-free diagnostics,
explicit import/global-state/I/O/evaluation architecture rules, and sanitized
CLI parsing before file I/O. Final re-review reported no blocking or
non-blocking finding; its corrected focused plugin/CLI/architecture/API/release
suite passed 138 tests, with clean Ruff, Pyright, strict docs, diff, and
isolated CLI checks.

At this stage no M12 hosted or cross-platform pass, merge, tag, release, package
publication, discovery/loading/execution, provider admission, networking,
editor/GUI, deferred Box2D/SDL3 adapter, or native-code claim is made.

## M12 hosted validation - 2026-08-06

Ready stacked PR #13 targets `codex/m11-rich-2d-modules` from
`codex/m12-plugin-manifest-compatibility`. Its one DCO-signed implementation
commit is `e1f6e3cd8572d20a4f0a5c62a96b9aa52a986b38`; GitHub reports the PR open,
ready, mergeable, and `CLEAN` against exact final M11 evidence head
`840a8b06d461fa1d5e649911b22f5995154728a7`.

GitHub Actions pull-request run `31028863469` executed the implementation
commit from `2026-08-05T17:11:37Z` through `2026-08-05T17:13:23Z` and concluded
`success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profiling
  contract, sdist/wheel build, isolated-wheel smoke including the explicit
  plugin manifest, release staging, and complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file was unchanged by M12. This is the only hosted run created for
the implementation commit. It validates the supported cross-platform,
distribution, and provider contracts; it does not merge PR #13, publish a
package, create a tag or release, load plugin code, admit a provider, or
authorize any deferred networking/editor/native work.

## M13 final reviewed local validation - 2026-08-06

Environment: Windows 11, uv-managed CPython 3.12.13 with the exact locked
graphics extra. Base and current pre-commit `HEAD`:
`7cb834c7b5e84e1b1a945905a68b947b3a4bdd3f`. Branch:
`codex/m13-rollback-network-readiness`.

The complete post-review command sequence produced these results:

- The first sandboxed `uv lock --check` / `uv sync --frozen --all-groups
  --extra graphics` attempt exited 1 because the workspace sandbox denied
  access to uv's existing user cache. The approved exact rerun exited 0:
  `uv lock --check` resolved the unchanged 46-package lock and sync checked 45
  packages. An initial sandboxed `uv build` had the same cache denial; its
  approved exact rerun and final post-review rebuild both exited 0.
- `uv run --frozen ruff format --check .` exited 0; all 174 Python files were
  already formatted.
- `uv run --frozen ruff check .` exited 0 with `All checks passed!`.
- `uv run --frozen pyright` exited 0 with zero errors, warnings, or information
  diagnostics.
- `uv run --frozen mkdocs build --strict` exited 0 in 0.51 seconds. Material
  for MkDocs emitted its existing upstream MkDocs 2.0 informational warning.
- `uv run --frozen pytest -q` exited 0 with 793 passing tests and one existing
  Windows symlink-capability skip in 60.05 seconds.
- `uv build` exited 0 and rebuilt
  `dist/ludoweave-0.1.0a1.tar.gz` plus the universal
  `dist/ludoweave-0.1.0a1-py3-none-any.whl` from the sdist.
- `uv run --frozen python scripts/smoke_wheel.py dist` exited 0 with
  `wheel smoke passed: ludoweave-0.1.0a1-py3-none-any.whl`; the isolated wheel
  ran the M13 24/12 readiness proof and required deferred/no-transport gates.
- `uv run --frozen python scripts/release_artifacts.py dist
  .tmp/m13-release-candidate-final-20260806` exited 0 with protocol
  `ludoweave.release-stage/1`, version `0.1.0a1`, ten artifacts, the versioned
  sample bundle, and SPDX SBOM.
- `uv run --frozen python scripts/smoke_release.py
  .tmp/m13-release-candidate-final-20260806` exited 0 with
  `release smoke passed: ludoweave 0.1.0a1`; the isolated installed wheel ran
  the bundled readiness example.
- `git diff --check` exited 0.

M13 evidence and provider acceptance:

- `uv run --frozen python examples/rollback_readiness.py --ticks 120
  --branch-tick 60 --output .tmp/m13-readiness-final.json` exited 0 with schema
  `ludoweave.evaluation.rollback-readiness/1`, status `deferred`, no transport,
  120 parent batches/121 verified checkpoints, 60 child batches/61 verified
  checkpoints, immutable parent timeline hash
  `sha256:c4650d3173a0b62eb9e65e1a49f8e90fa90c9268b56ab9000fb75b096ec0e515`,
  parent final hash
  `sha256:9d4b4f5e81ed1ac487f83ae742ce41cfb27f2a0da652a43c33c74e5571cd3026`,
  and repeatable corrected final hash
  `sha256:2708c1bb1df45adaca0eb095242f12b96837493e2bd06cd8a3c78b45742af7b2`.
  The informational canonical sizes were 2,793 snapshot bytes, 95,118 parent
  timeline bytes, and 51,160 child timeline bytes; M13 defines no timing or
  bandwidth target.
- `uv run --frozen python scripts/validate_rollback_readiness.py
  .tmp/m13-readiness-final.json` exited 0 with
  `rollback readiness evidence valid`.
- The final hostile integration/architecture/release focus exited 0 with 54
  passes in 13.01 seconds. It covers direct-call work bounds, exact checkpoint
  counts, root/nested duplicate JSON, non-finite numbers, non-regular and
  oversized files, exact root types/version, Boolean/integer ambiguity,
  hashes/counts/metrics, false admission, and closed import/member aliases.
- `uv run --frozen --extra graphics pytest -q
  tests/integration/test_wgpu_render.py` exited 0 with nine passes in 5.65
  seconds.
- Clockwork Arena wgpu, Agent World Builder, alpha acceptance, rich-2D
  showcase, and the path-free compatible example plugin check all exited 0.

Every benchmark/profile command in the README quality suite was also rerun
against uniquely named M13 artifacts and its validator exited 0:

- M1 recorded seven workloads. The fixed 3,600-tick p95 was 35,707,100 ns and
  observed its headless target; the 10,000-entity simulation p95 was
  136,388,500 ns and did not observe its inherited 4 ms target. The validator
  reported one of two recorded targets observed.
- M2 validated four informational workloads with no timing targets.
- M3 validated six workloads. The 10,000-sprite extraction p95 was 24,154,400
  ns and missed its inherited target; the wgpu submit p95 was 2,747,400 ns and
  observed its target. One of two recorded targets was observed.
- M4 validated three workloads; the baseline p95 was 1,840,000 ns and observed
  its 16,666,667 ns target.
- The five-repeat M7 base and real-wgpu profile artifacts validated with two
  and three workloads respectively. Profile timing is diagnostic only.

Artifact, scope, and history audit:

- the wheel contains 91 entries and zero `.pyd`, `.so`, `.dll`, or `.dylib`
  entries;
- wheel metadata has no mandatory dependency; its only `Requires-Dist` entries
  are the unchanged exact `graphics` extra for GLFW, rendercanvas, and wgpu;
- `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, and all `src/` files
  are unchanged from the exact M12 base, retaining the eight essential jobs,
  persistent formats, public Python surfaces, and pure-Python package contract;
- focused secret-assignment and network/provider import scans found no match;
  ripgrep exit 1 means no matches; and
- merge-base equals exact M12 head
  `7cb834c7b5e84e1b1a945905a68b947b3a4bdd3f` and the pre-commit left/right
  count was `0 0`, so no unrelated commit entered the stack.

Independent hostile review reproduced and drove fixes for pre-read byte caps,
regular-file pre/post-open checks, canonical duplicate/non-finite JSON,
version/path spoofing, exact Boolean/integer/count types, direct-call work
bounds, complete parent/child checkpoint verification, closed exact
module/member import allowlists, and dynamic-builtin aliases. Final review
reported no blocking or non-blocking finding. It independently passed Ruff,
Pyright, strict docs, 54 focused tests, a generated/validated 24/12 artifact,
and the advertised maximum 600/300 proof in 19.1 seconds with deferred and
no-transport gates. Diff and secret scans were clean.

At this stage no M13 hosted or cross-platform pass, merge, tag, release,
package publication, socket/listener, peer authority, live rollback service,
network protocol, persistent-format change, editor/GUI, 3D, provider adapter,
or native-code claim is made.

## M13 hosted validation - 2026-08-06

Ready stacked PR #14 targets `codex/m12-plugin-manifest-compatibility` from
`codex/m13-rollback-network-readiness`. Its one DCO-signed implementation
commit is `ba62b650191cfb982100692e7ec694da318956ae`; GitHub reports the PR open,
ready, mergeable, and `CLEAN` against exact final M12 evidence head
`7cb834c7b5e84e1b1a945905a68b947b3a4bdd3f`.

GitHub Actions pull-request run `31031590206` executed the implementation
commit from `2026-08-05T17:46:38Z` through `2026-08-05T17:48:41Z` and concluded
`success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profiling
  contract, sdist/wheel build, isolated-wheel smoke including the M13
  readiness proof, release staging, and complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file was unchanged by M13. This is the only hosted run created for
the implementation commit. It validates the supported cross-platform,
distribution, and provider contracts; it does not merge PR #14, publish a
package, create a tag or release, or authorize sockets, remote authority, live
rollback, a network protocol, editor/GUI, 3D, provider/native work, or a
persistent-format change.

## M14 final local validation - 2026-08-06

M14 was evaluated on Windows 11 with uv-managed CPython 3.12.13. It changes
repository evidence, tests, and documentation only. Its installed JSON confirms
the exact 47-name public render export list, orthographic `Camera2D` fields and
matrix, canonical sprite `(layer, z, entity)` ordering, the tile layer field,
color-only descriptors, 2D limits, and the seven existing world operations.
All nine constrained-3D admission gates are false.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | The existing lock resolved 46 packages and remained current. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | The existing frozen environment checked 45 packages. |
| `uv run --frozen ruff format --check .` | 0 | All 178 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 809 tests passed and one existing Windows symlink-capability test skipped in 69.68 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built in 0.51 seconds; Material emitted its documented upstream MkDocs 2.0 warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and the universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency wheel install passed the exact M14 installed-surface document plus the inherited public smokes. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m14-release-candidate-r2` | 0 | Staged the complete deterministic ten-artifact candidate including the M14 sample. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m14-release-candidate-r2` | 0 | Checksums, manifest, SBOM, installed wheel, and every bundled sample including exact M14 evidence passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Nine real-wgpu integration tests passed in 5.51 seconds. |
| `git diff --check` | 0 | No whitespace errors. |

Every inherited benchmark/profile command in the README quality suite ran
against uniquely named M14 artifacts and its validator exited 0:

- M1 validated seven workloads. Fixed 3,600-tick p95 was 35,706,500 ns and
  observed its target; 10,000-entity simulation p95 was 128,658,700 ns and did
  not observe the inherited 4 ms target. One of two targets was observed.
- M2 validated four informational workloads with no timing targets.
- M3 validated six workloads. The 10,000-sprite extraction p95 was 28,468,500
  ns and missed its inherited target; real-wgpu 10,000-instance submission p95
  was 2,835,700 ns and observed its target. One of two targets was observed.
- M4 validated three workloads; baseline p95 was 1,877,900 ns and observed its
  16,666,667 ns target.
- Five-repeat M7 base and real-wgpu profile artifacts validated with two and
  three workloads respectively. Profile timing remains diagnostic only.

Artifact, scope, history, and independent-review evidence:

- the wheel contains 91 entries and zero `.pyd`, `.so`, `.dll`, or `.dylib`
  entries; metadata retains Apache-2.0, Python `>=3.12,<3.15`, no mandatory
  dependency, and only the unchanged exact `graphics` extra;
- `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, and all `src/` files
  are byte-unchanged from exact M13 evidence head
  `48f8f296113e3f2794bae7f4c67997d433e4dd36`;
- merge-base equals that exact M13 head and the pre-commit left/right count was
  `0 0`; focused credential assignment scanning returned no matches (ripgrep
  exit 1); and
- independent hostile review first blocked positive layered-2D evidence,
  exact artifact validation, and closed import/export guards. After correction,
  it independently reproduced lock/static/full-test/docs/build/wheel/release
  success, rejected tampered sorting/version/export/gate documents, found no
  credential match, and approved with no remaining finding.

At this stage no M14 hosted/cross-platform pass, merge, tag, release, package
publication, runtime/public/persistent-format change, 3D feature, provider
dependency, or new performance-target claim is made.

## M14 hosted validation - 2026-08-06

Ready stacked PR #15 targets `codex/m13-rollback-network-readiness` from
`codex/m14-constrained-3d-decision`. Its DCO-signed implementation commit is
`47443046834eb423be977973775f80494161533d`. GitHub reports the PR open,
ready, mergeable, and `CLEAN` against exact final M13 evidence head
`48f8f296113e3f2794bae7f4c67997d433e4dd36`.

GitHub Actions pull-request run `31033924254` executed the implementation
commit from `2026-08-05T18:16:06Z` through `2026-08-05T18:18:37Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, exact isolated-wheel M14 evidence, release staging, and
  complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file was unchanged by M14, and the branch has exactly this one
pull-request CI run for the implementation commit. Hosted evidence confirms
the supported installed/cross-platform/provider contracts; it does not merge
PR #15, publish a package, create a tag or release, add 3D runtime behavior,
change a public/persistent contract, or admit a new dependency/provider.

## M8-M14 main integration - 2026-08-06

Direct-main integration PR #16 used exact base
`0237b2bfb11c6032d030dada639c7dbe439e5089` and final M14 evidence head
`02426805a11712030b3082ec349696d6d94aca50`. The pre-merge audit found 14
linear commits, zero merge commits, and DCO sign-off in all 14. The M8-M14
implementation runs `31012696753`, `31015885190`, `31020096463`,
`31024155710`, `31028863469`, `31031590206`, and `31033924254` were all
re-queried from GitHub and reported completed `success`.

PR #16 was open, ready, `MERGEABLE`, and `CLEAN`. Its final evidence head
contained `[skip ci]`, so opening the integration PR created no redundant
matrix. The user-authorized squash merge completed at
`2026-08-05T18:22:37Z` as GitHub-verified main commit
`2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`. Its tree
`137a1870b0dd9034ad935b253a13186f6c7cc913` exactly equals the validated M14
head tree. The squash message includes the DCO sign-off and all seven hosted
run IDs.

Stacked PRs #9-#15 were closed as superseded after the exact-tree check;
branches were retained. The integration creates no tag, release, package
publication, new runtime/provider behavior, or additional Actions run.

## M15 final local validation - 2026-08-06

M15 was evaluated on Windows 11 with uv-managed CPython 3.12.13. It changes
repository evidence, tests, and documentation only. Its deterministic installed
document derives the exact four-name root export surface, empty tools exports,
the exact 20-name all-experimental agent surface, twelve tools, seven world
operations, command/transaction/receipt/agent/inspector/MCP revisions, and
inspector configuration/read-only facts. It also executes one ephemeral
six-command write-enabled agent transaction and verifies a committed v1
receipt, six committed outcomes, pre/post/authority hash continuity, unchanged
tick count, and six resulting entities. All twelve editor-admission gates
remain false.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | The existing lock resolved 46 packages and remained current. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | The existing frozen environment checked 45 packages. |
| `uv run --frozen ruff format --check .` | 0 | All 182 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 834 tests passed and one existing Windows symlink-capability test skipped in 62.59 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built in 0.52 seconds; Material emitted its documented upstream MkDocs 2.0 warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and the universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency wheel install passed the exact M15 installed document plus inherited public smokes. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m15-release-candidate-r2` | 0 | Staged the complete deterministic ten-artifact candidate including the M15 sample. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m15-release-candidate-r2` | 0 | Checksums, manifest, SBOM, installed wheel, and every bundled sample including exact M15 evidence passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Nine real-wgpu integration tests passed in 5.59 seconds. |
| `git diff --check` | 0 | No whitespace errors. |

The first sandboxed attempt to start the complete uv gate could not access the
user-managed uv cache and therefore ran no check; the authorized rerun above
completed successfully. The corrected focused review suite reported 120 passes,
clean Ruff/Pyright, and strict docs before the final full gate.

Every inherited README benchmark/profile command ran against uniquely named
M15 artifacts and its validator exited 0:

- M1 validated seven workloads. Fixed 3,600-tick p95 was 35,317,100 ns and
  observed its target; 10,000-entity simulation p95 was 158,073,300 ns and did
  not observe the inherited 4 ms target. One of two targets was observed.
- M2 validated four informational workloads with no timing targets.
- M3 validated six workloads. The 10,000-sprite extraction p95 was 24,263,200
  ns and real-wgpu 10,000-instance submission p95 was 3,057,200 ns; neither
  observed its inherited target in this local run. Zero of two targets was
  observed.
- M4 validated three workloads; baseline p95 was 1,885,700 ns and observed its
  16,666,667 ns target.
- Five-repeat M7 base and real-wgpu profile artifacts validated with two and
  three workloads respectively. Profile timing remains diagnostic only.

Artifact, scope, history, and independent-review evidence:

- the exact alpha wheel contains 91 entries and zero `.pyd`, `.so`, `.dll`, or
  `.dylib` entries;
- `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, and all `src/` files
  are byte-unchanged from exact base
  `bfea67d2d922e8c591224d18f56c14d572d7f7da`;
- merge-base equals that exact base and the pre-commit left/right count is
  `0 0`; deferred-interface import and credential-assignment scans found no
  match; and
- independent review initially blocked hard-coded inspector-public status,
  shallow agent stability evidence, non-executed receipt claims, narrow root
  export/dependency guards, formatting, and stale roadmap/state text. After
  correction, the reviewer independently reproduced 120 focused and 834 full
  passes, static/docs/build/wheel/release success, protected scope, history,
  and credential scans and approved with no remaining finding.

At this stage no M15 commit, hosted/cross-platform pass, PR, merge, tag,
release, package publication, runtime/public/persistent-format change,
GUI/editor implementation, toolkit/dependency, or new performance-target claim
is made.

## M15 hosted validation - 2026-08-06

Ready PR #19 targets `main` from `codex/m15-visual-editor-admission`. Before
the evidence-only follow-up, GitHub reported exact base
`bfea67d2d922e8c591224d18f56c14d572d7f7da`, implementation head
`7e85570056dde3678aaeee13eee4036067876d8c`, `MERGEABLE`, and `CLEAN`. The
implementation history contains one DCO-signed commit.

GitHub Actions pull-request run `31036925179` executed that implementation
commit from `2026-08-05T18:54:18Z` through `2026-08-05T18:56:30Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, exact isolated-wheel M15 evidence, release staging, and
  complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and this is the only hosted run created for
the implementation commit. Hosted evidence confirms the supported installed,
cross-platform, and provider contracts; it does not publish a package, create
a tag or release, add a GUI/editor/runtime API, promote the experimental agent
surface, change a persistent format, or admit a new dependency/provider.

## M16 final local validation - 2026-08-06

M16 was evaluated on Windows 11 with uv-managed CPython 3.12.13. It changes
repository evidence, tests, release-sample composition, and documentation only.
The deterministic installed document records the complete exact three-entry
optional-graphics `Requires-Dist` set, exact root/plugin exports and preview
stability, ten inert manifest fields, eight capability labels, typed rejection
of six representative executable fields, no WASM runtime requirement, no
public guest-execution export, and fifteen false admission gates. It compiles
or executes no guest.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | The existing lock resolved 46 packages and remained current. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | The existing frozen environment checked 45 packages. |
| `uv run --frozen ruff format --check .` | 0 | All 186 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 870 tests passed and one existing Windows symlink-capability test skipped in 65.04 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built in 0.55 seconds; Material emitted its documented upstream MkDocs 2.0 warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and the universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency wheel install passed the exact M16 installed document plus inherited public smokes. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m16-release-candidate-reviewed-20260806` | 0 | Staged the complete deterministic ten-artifact candidate including the M16 sample. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m16-release-candidate-reviewed-20260806` | 0 | Checksums, manifest, SBOM, installed wheel, and every bundled sample including exact M16 evidence passed. |
| `uv run --frozen pytest -q tests/integration/test_wgpu_render.py` | 0 | Nine real-wgpu integration tests passed in 5.62 seconds. |
| `uv run --frozen python examples/wasm_mod_security_decision.py` | 0 | Emitted the exact deferred `ludoweave.evaluation.wasm-mod-security/1` document. |
| `git diff --check` | 0 | No whitespace errors. |

The first sandboxed `uv lock --check` and two sandboxed `uv build` attempts
could not open the user-managed uv cache and exited 1 before completing those
checks. Their explicitly authorized reruns above exited 0. The first strict
docs attempt found two links outside the documentation tree; the links were
corrected and both final and independent strict builds passed.

Every inherited README benchmark/profile command ran against uniquely named
M16 artifacts and its validator exited 0:

- M1 validated seven workloads. Fixed 3,600-tick p95 was 36,551,800 ns and
  observed its target; 10,000-entity simulation p95 was 123,939,400 ns and did
  not observe the inherited 4 ms target. One of two targets was observed.
- M2 validated four informational workloads with no timing targets.
- M3 validated six workloads. The 10,000-sprite extraction p95 was 24,013,300
  ns and real-wgpu 10,000-instance submission p95 was 3,172,000 ns; neither
  observed its inherited target in this local run. Zero of two targets was
  observed.
- M4 validated three workloads; baseline p95 was 1,817,500 ns and observed its
  16,666,667 ns target.
- Five-repeat M7 base and real-wgpu profile artifacts validated with two and
  three workloads respectively. Profile timing remains diagnostic only.

Artifact, scope, history, and independent-review evidence:

- the exact alpha wheel contains 91 entries and zero `.pyd`, `.so`, `.dll`,
  `.dylib`, WASM runtime, or WASI entries;
- `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, the version, and all
  `src/` files are byte-unchanged from exact base
  `c013dad38b1b64f0f4ccddc19681d643f6414427`; the eight-job CI topology is
  unchanged;
- explicit, dynamic, and named-module fixtures prove the WASM runtime guard,
  including the reproduced `webassembly_runtime.py` bypass; unknown and
  malformed installed requirement fixtures fail before evidence success; and
- independent review initially blocked blacklist-only requirement evidence,
  the named-module bypass, missing residual risk, and inaccurate current-flow
  wording. After correction, the reviewer ran
  `uv run --frozen pytest -q tests/architecture/test_import_boundaries.py tests/architecture/test_m16_wasm_boundary.py tests/integration/test_wasm_mod_security_decision.py tests/unit/test_release_artifacts.py tests/architecture/test_release_workflow.py`
  with 140 passes in 3.30 seconds, independently reproduced clean focused
  Ruff/Pyright, strict docs, offline build, wheel/release smoke, exact evidence,
  protected scope, and diff checks, and approved with no remaining finding.

At this stage no M16 commit, hosted/cross-platform pass, PR, merge, tag,
release, package publication, runtime/public/persistent-format change,
executable mod, WASI/host-call surface, dependency, or new performance-target
claim is made.

## M16 hosted validation - 2026-08-06

Ready PR #20 targets `main` from
`codex/m16-wasm-mod-security-decision`. Before the evidence-only follow-up,
GitHub reported exact base `c013dad38b1b64f0f4ccddc19681d643f6414427`,
implementation head `bcaf78fbc78bda8a13a95e397ab15d003dd4a6ce`,
`MERGEABLE`, and `CLEAN`. The implementation history contains one DCO-signed
commit.

GitHub Actions pull-request run `31039403209` executed that implementation
commit from `2026-08-05T19:26:18Z` through `2026-08-05T19:28:52Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, exact isolated-wheel M16 evidence, release staging, and
  complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and this is the only hosted run created for
the implementation commit. Hosted evidence confirms the supported installed,
cross-platform, and provider contracts; it does not publish a package, create
a tag or release, add an executable mod/runtime/WASI/host-call surface, change
a public or persistent contract, or admit a new dependency/provider.

## M16 main integration - 2026-08-06

PR #20 used exact base `c013dad38b1b64f0f4ccddc19681d643f6414427`
and final evidence head `808e48a5cb2727c8e1f4d7e896c4f8c7d41bfe1a`.
The two-commit branch history contains a DCO trailer on both commits. The final
evidence commit contains `[skip ci]`, and GitHub lists only implementation run
`31039403209` for the branch.

The user-authorized squash merge completed at `2026-08-05T19:31:34Z` as
GitHub-verified main commit `e2bd57c057c0c16861953c0702b2012c4cabfe90`
with verification reason `valid`. Its sole parent is the exact base, its DCO
trailer is a real commit-message trailer, and tree
`05367be9bd85014fe6c70995ac1a69a39f90ef1e` exactly equals the final M16
branch tree. The milestone branch is retained.

The integration creates no tag, release, package publication, executable mod,
runtime/provider/dependency behavior, or additional Actions run. The
authoritative post-alpha sequence ends with M16 item 10; no M17 milestone or
acceptance criteria are assigned by the current plan.

## M17 installed render-device conformance - local final gate - 2026-08-06

M17 was subsequently assigned from the design plan's longer-term metric for
third-party adapters/plugins passing conformance. Branch
`codex/m17-render-device-conformance` started from exact clean synchronized
`main` commit `27d2ee9d1f7f75dacc17568650f00ce833ef4fce` (`main...origin/main`
left/right count `0 0`). The bounded slice is one experimental installed
`RenderDevice` baseline over an explicitly supplied trusted factory. It adds
no adapter discovery/loading/installation, provider dependency, plugin field,
canonical/persistent world state, version change, or CI job.

Final Windows local gate used uv-managed CPython 3.12.13:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the unchanged 46-package lock. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked the locked 45-package environment. |
| `uv run --frozen ruff format --check .` | 0 | All 191 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen pytest -q` | 0 | 895 passed and one existing Windows symlink-capability test skipped in 64.75 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built; the upstream Material MkDocs-2 warning remained informational. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency wheel passed all inherited flows plus the nine-check Null render-device profile. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m17-release-candidate-final-reviewed` | 0 | Staged the complete deterministic ten-artifact candidate including the updated sample bundle. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m17-release-candidate-final-reviewed` | 0 | Exact checksums/manifest/SBOM/notices, safe extraction, isolated install, inherited samples, and bundled Null conformance passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All 10 real-wgpu tests passed in 5.87 seconds, including the shared baseline. |
| `uv run --frozen --extra graphics python examples/render_device_conformance.py --backend wgpu` | 0 | Protocol `ludoweave.render-device-conformance/1`, profile `render-device-baseline/1`, adapter `wgpu`, all nine checks `pass`. |
| `uv run --frozen pytest -q tests/unit/test_render_device_conformance.py tests/architecture/test_m17_conformance_boundary.py tests/architecture/test_import_boundaries.py` | 0 | 121 focused success, failure-sanitization, lifecycle, explicit-factory, and dependency-boundary tests passed. |

Artifact inspection found 92 wheel entries, including
`ludoweave/render/conformance.py`, and zero `.pyd`, `.so`, `.dll`, `.dylib`,
or `.wasm` entries. Installed metadata retains no mandatory requirement and
the exact existing graphics extra only:

- `glfw==2.10.2; extra == 'graphics'`;
- `rendercanvas[glfw]==2.7.2; extra == 'graphics'`; and
- `wgpu==0.32.0; extra == 'graphics'`.

The protected `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, package
version, and package-root exports are unchanged. M14's installed render-export
fingerprint was updated from 47 to the exact 53-name surface by adding only the
two conformance constants, status enum, two frozen report records, and runner;
its layered-2D facts and every 3D admission gate remain unchanged.

All documented benchmark/profile validation contracts were executed on the
dirty M17 working tree and validated:

- M1: seven workloads; fixed-step p95 `54,750,000 ns` observed its target,
  while 10,000-entity simulation p95 `126,505,000 ns` missed; 1 of 2 recorded
  targets observed.
- M2: four informational workloads validated with no timing threshold.
- M3: six workloads; 10,000-sprite extraction p95 `24,179,800 ns` and wgpu
  submission p95 `3,735,200 ns` both missed; 0 of 2 targets observed.
- M4: baseline p95 `1,863,200 ns` observed its target; two stress workloads
  remained informational.
- M7: five-repeat base profile with two workloads and graphics profile with
  three workloads both validated under `ludoweave.profile.m7/1`.

Two sandboxed command attempts failed before executing project code because
the managed sandbox denied uv cache access at
`C:\Users\louij\AppData\Local\uv\cache`; the same commands were rerun with
approved cache access and passed as recorded above. One earlier wheel smoke
correctly failed after the additive public render exports changed M14's exact
installed-surface fixture. The fixture was updated to the six exact M17 names,
then focused M14/M15/M16 tests, final wheel smoke, and final release smoke all
passed. No product failure remains unresolved.

## M17 hosted validation - 2026-08-06

Ready PR #22 targets `main` from
`codex/m17-render-device-conformance`. GitHub reported exact base
`27d2ee9d1f7f75dacc17568650f00ce833ef4fce`, implementation head
`8e592f329424719214239bf97bd85dad9c9c5928`, `MERGEABLE`, and `CLEAN`. The
implementation history contains one DCO-signed commit.

GitHub Actions pull-request run `31042903689` executed that implementation
commit from `2026-08-05T20:11:26Z` through `2026-08-05T20:13:48Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, installed-wheel smoke, release staging, and complete
  release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and this is the only hosted run created for
the implementation commit. Hosted evidence validates supported installed,
cross-platform, and existing-provider behavior; it does not certify or admit
third-party code, count project-owned adapters as independent adoption,
publish a package, create a tag or release, add discovery/loading/install
behavior, change a public or persistent format, or claim the locally missed
M1/M3 performance targets passed.

After recording these hosted facts, `uv run --frozen mkdocs build --strict`
exited 0 in 0.58 seconds with only the documented upstream Material MkDocs-2
warning, and `git diff --check` exited 0.

## M17 main integration - 2026-08-06

PR #22 used exact base `27d2ee9d1f7f75dacc17568650f00ce833ef4fce`
and final evidence head `148600cdaf9c419fbf552c68f833e0d55655731f`.
The two-commit branch history contains a DCO trailer on both commits. The final
evidence commit contains `[skip ci]`; GitHub lists only implementation run
`31042903689` for the branch.

The user-authorized squash merge completed at `2026-08-05T20:17:17Z` as
GitHub-verified `main` commit
`610261c8450afc3d7db6ebb2b0425a1829737aec` with verification reason `valid`.
Its sole parent is the exact base, its DCO trailer is a real commit-message
trailer, and tree `1e82568a463c62d0a1cf988b67eea09885ec50e3`
exactly equals the final M17 branch tree. The milestone branch is retained.

The first local tree comparison used unquoted PowerShell revision braces and
failed before comparing with an encoded-argument parsing error. The corrected
quoted `git rev-parse "HEAD^{tree}"` and
`git rev-parse "origin/main^{tree}"` commands both returned the exact tree
above, and `git diff --exit-code HEAD origin/main` exited 0.

The integration creates no tag, release, package publication, adapter
discovery/loading/installation, provider admission, dependency, workflow
change, or additional Actions run. Project-owned Null/wgpu conformance remains
reference evidence and does not increase independent third-party adoption.

On the integration-evidence branch,
`uv run --frozen mkdocs build --strict` exited 0 in 0.56 seconds with only the
documented upstream Material MkDocs-2 warning, and `git diff --check` exited 0.

PR #23 then squash-integrated the M17 repository-state evidence into `main` as
GitHub-verified commit `ed65b12fa02f672113eac5939a0f616079fee44a` without a
new Actions run. The retained M18 branch starts from that exact synchronized
commit.

## M18 installed agent-tool conformance - local final gate - 2026-08-06

Branch `codex/m18-agent-tool-conformance` started from exact clean synchronized
`main` commit `ed65b12fa02f672113eac5939a0f616079fee44a`. The bounded slice is
one experimental installed 12-tool agent-service baseline over an explicitly
supplied trusted factory. It adds no discovery, dynamic import, installation,
subprocess, network transport, provider, plugin field, dependency, lock,
version, persistent format, canonical state, package-root export, or CI job.

Final Windows local gate used uv-managed CPython 3.12.13:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the unchanged 46-package lock. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked the locked 45-package environment. |
| `uv run --frozen ruff format --check .` | 0 | All 196 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen pytest -q` | 0 | 925 tests passed and one existing Windows symlink-capability test skipped in 66.24 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built; the upstream Material MkDocs-2 warning remained informational. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency wheel passed inherited flows plus the exact 12-check direct agent-service profile. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m18-release-candidate-final-20260806-b` | 0 | Staged the complete deterministic ten-artifact candidate including the M18 sample. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m18-release-candidate-final-20260806-b` | 0 | Checksums, manifest, SBOM, notices, safe extraction, isolated install, inherited samples, and bundled agent conformance passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All 10 existing real-wgpu integration tests passed in 5.80 seconds. |
| `uv run --frozen pytest -q tests/unit/test_agent_tool_conformance.py tests/architecture/test_m18_agent_conformance_boundary.py tests/integration/test_agent_tool_conformance_example.py tests/unit/test_release_artifacts.py tests/integration/test_visual_editor_decision.py tests/architecture/test_release_workflow.py tests/architecture/test_import_boundaries.py` | 0 | 145 focused success, adversarial-sanitization, receipt/atomicity, lifecycle, explicit-factory, release, and dependency-boundary tests passed in 3.91 seconds. |
| `git diff --check` | 0 | No whitespace errors. |
| `git fsck --no-dangling` | 0 | Repository object/connectivity check reported no issue. |

Artifact inspection found 93 wheel entries, including
`ludoweave/agent/conformance.py`, and no `.pyd`, `.so`, `.dll`, `.dylib`, or
`.wasm` entry. Metadata retains Python `>=3.12,<3.15`, no mandatory
requirement, and only the exact existing optional graphics requirements:

- `glfw==2.10.2; extra == 'graphics'`;
- `rendercanvas[glfw]==2.7.2; extra == 'graphics'`; and
- `wgpu==0.32.0; extra == 'graphics'`.

The protected `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, package
version, and package-root exports are unchanged. Source scans found no
credential assignment, discovery/process/network import or call, or backend/
native dependency in the conformance runtime/example. The M15 exact installed
agent-export fingerprint was updated only with the seven experimental M18
names; its visual-editor decision and admission gates are unchanged.

All documented benchmark/profile validation contracts were executed on the
dirty M18 working tree and validated:

- M1: seven workloads; fixed-step p95 `39,482,100 ns` observed its target,
  while 10,000-entity simulation p95 `122,772,500 ns` missed; 1 of 2 recorded
  targets observed.
- M2: four informational workloads validated with no timing threshold.
- M3: six workloads; 10,000-sprite extraction p95 `23,673,400 ns` and wgpu
  submission p95 `3,437,400 ns` both missed; 0 of 2 targets observed.
- M4: baseline p95 `1,821,000 ns` observed its target; two stress workloads
  remained informational.
- M7: five-repeat base profile with two workloads and graphics profile with
  three workloads both validated under `ludoweave.profile.m7/1`.

Development checks first exposed import/export sorting, one unnecessary cast,
and one unknown-result type issue; all were corrected and the focused/full
static gates were rerun clean. Skeptical review then strengthened exact receipt
identity/outcome validation, invalid-factory cleanup, control-flow cleanup
during close, and nested forbidden-import fixtures before the final gate.
One sandboxed `uv build` attempt exited 1 before project execution because
access to uv's user cache was denied; the approved rerun and all final artifact
commands above exited 0. No product failure remains unresolved.

History review before publication reports `HEAD`, local `main`, `origin/main`,
and the merge base at exact commit
`ed65b12fa02f672113eac5939a0f616079fee44a`, with left/right count `0 0` and
the intended linear squash-integrated milestone history. At this stage no M18
commit, hosted/cross-platform pass, PR, merge, tag, release, or package
publication is claimed.

## M18 hosted validation - 2026-08-06

Ready PR #24 targets `main` from
`codex/m18-agent-tool-conformance`. GitHub reported exact base
`ed65b12fa02f672113eac5939a0f616079fee44a`, DCO-signed implementation head
`c4dde705393eebb7c99af428745e9383750f6b4d`, `MERGEABLE`, and `CLEAN` after
checks completed.

GitHub Actions pull-request run `31046172544` executed that implementation
commit from `2026-08-05T20:52:57Z` through `2026-08-05T20:55:24Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, installed-wheel smoke, release staging, and complete
  release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and this is the only hosted run created for
the implementation commit. Hosted evidence validates the supported installed,
cross-platform, and existing-provider contracts. It does not discover, admit,
certify, or count third-party adapter code; establish real-agent manual-
recovery rates; publish a package; create a tag or release; add a transport,
listener, provider, dependency, or CI job; or claim the locally missed M1/M3
performance targets passed.

## M18 main integration - 2026-08-06

PR #24 used exact base `ed65b12fa02f672113eac5939a0f616079fee44a`
and final evidence head `cb617be0f678528fadc82877ec6910e42c6daf6b`.
The two-commit branch history contains a DCO trailer on both commits. The final
evidence commit contains `[skip ci]`, and GitHub lists only implementation run
`31046172544` for the branch.

The user-authorized squash merge completed at `2026-08-05T20:57:29Z` as
GitHub-verified `main` commit
`1000d362432f19c912edf51c67e29c79bf444443` with verification reason `valid`.
Its sole parent is the exact base, its DCO trailer is a real commit-message
trailer, and tree `1b6676ca7c1a6aaa223057a35e0c95242f4e9462`
exactly equals the final M18 branch tree. The milestone branch is retained.

The integration creates no tag, release, package publication, adapter
discovery/loading/installation, transport, provider admission, dependency,
workflow change, or additional Actions run. Project-owned direct-service
conformance remains reference evidence and does not increase independently
authored adapter adoption or establish real-agent manual-recovery rates.

## M19 installed WorldStore conformance - local final gate - 2026-08-06

Branch `codex/m19-world-store-conformance` starts from exact clean synchronized
`main` commit `4076f3d7ac0c0a82834a1c98dcb36426ba67ac5e`, with local `main`,
`origin/main`, both merge bases, and `HEAD` initially equal and left/right count
`0 0`. The bounded slice adds one experimental installed ten-check profile over
an explicit trusted `factory(ComponentRegistry)`. It adds no discovery, dynamic
import, installation, subprocess, network operation, backend, database,
external-resource lifecycle, native/archetype/NumPy storage, persistent format,
plugin field, dependency, lock, version, package-root export, or CI job.

Final hardened Windows gate used uv-managed CPython 3.12.13:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the unchanged 46-package lock. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked the locked 45-package environment. |
| `uv run --frozen ruff format --check .` | 0 | All 201 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen pytest -q` | 0 | 955 tests passed and one existing Windows symlink-capability test skipped in 73.37 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built in 0.80 seconds; the upstream Material MkDocs-2 warning remained informational. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency wheel passed all inherited flows plus both ten-check built-in WorldStore profiles. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/release-candidate` | 0 | Staged the complete deterministic ten-artifact candidate including `world_store_conformance.py`. |
| `uv run --frozen python scripts/smoke_release.py .tmp/release-candidate` | 0 | Checksums, manifest, SBOM, notices, safe extraction, isolated install, inherited samples, and bundled production/reference WorldStore conformance passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All ten existing real-wgpu integration tests passed in 7.05 seconds. |
| `uv run --frozen pytest -q tests/unit/test_world_store_conformance.py tests/architecture/test_m19_world_store_conformance_boundary.py tests/integration/test_world_store_conformance_example.py tests/unit/test_release_artifacts.py tests/conformance tests/architecture/test_import_boundaries.py tests/architecture/test_api_stability.py` | 0 | 149 focused success, adversarial-sanitization, epoch/copy/query/command/clone, explicit-factory, release, API, and dependency-boundary tests passed in 2.02 seconds. |
| `git diff --check` | 0 | No whitespace errors. |
| `git fsck --no-dangling` | 0 | Repository object/connectivity check reported no issue. |

The final wheel contains 94 entries including exactly one
`ludoweave/ecs/conformance.py`, and no `.pyd`, `.so`, `.dll`, `.dylib`, or
`.wasm` entry. Metadata retains Python `>=3.12,<3.15`, no mandatory
requirement, and only the exact existing optional graphics requirements:

- `glfw==2.10.2; extra == 'graphics'`;
- `rendercanvas[glfw]==2.7.2; extra == 'graphics'`; and
- `wgpu==0.32.0; extra == 'graphics'`.

The protected `.github/workflows`, `pyproject.toml`, `uv.lock`, package version,
and package-root exports are unchanged from the exact base. The sample bundle
contains one project-owned `world_store_conformance.py`. Source scans found no
credential assignment or wall-clock/random use; the only broad discovery/
process/network scan match was the runtime docstring explicitly stating that
subprocess and network operations are absent. AST tests reject discovery,
private storage, concrete reference, filesystem, process, network, NumPy, and
SQLite imports and prove nested forbidden imports are detected.

All documented benchmark/profile contracts were executed on the dirty M19
working tree and validated:

- M1: seven workloads; fixed-step p95 `36,282,500 ns` observed its target,
  while 10,000-entity simulation p95 `164,496,800 ns` missed; one of two
  recorded targets observed.
- M2: four informational workloads validated with no timing threshold.
- M3: six workloads; 10,000-sprite extraction p95 `26,171,800 ns` and wgpu
  submission p95 `3,465,100 ns` both missed; zero of two targets observed.
- M4: baseline p95 `2,019,400 ns` observed its target; two stress workloads
  remained informational.
- M7: five-repeat base profile with two workloads and graphics profile with
  three workloads both validated under `ludoweave.profile.m7/1`.

Development validation first exposed postponed component annotations in the
fixture, import/export ordering, one unnecessary cast, and two incorrect
adversarial-test assumptions; all were corrected before the complete gate.
Findings-first final review then added exact property-shape checks, adapter-stage
control-flow propagation coverage, and precise direct-import architecture
wording. The complete static, 955-test, installed-wheel, and release gates were
rerun on that hardened tree with no remaining finding.

Initial sandboxed `uv lock --check`, `uv sync`, and `uv build` invocations each
exited 1 before project execution because access to uv's existing user cache
was denied. Approved cache-access reruns and every final command above exited
0; these were environment-permission failures, not lock, sync, or build
failures. No M19 hosted/cross-platform pass, PR, merge, tag, release, package
publication, certification, or independently authored adapter adoption is
claimed at this stage.

## M19 hosted validation - 2026-08-06

Ready PR #26 targets `main` from
`codex/m19-world-store-conformance`. GitHub reported exact base
`4076f3d7ac0c0a82834a1c98dcb36426ba67ac5e`, DCO-signed implementation head
`1da692a693c1f92e10b676c2d4539354ce3ff59f`, `MERGEABLE`, and `CLEAN` after
checks completed.

GitHub Actions pull-request run `31092244573` executed that implementation
commit from `2026-08-06T10:11:30Z` through `2026-08-06T10:14:03Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, installed-wheel smoke, release staging, and complete
  release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and GitHub lists this as the only hosted run
for the M19 branch. Hosted evidence validates supported installed,
cross-platform, and existing-provider contracts. It does not discover, admit,
certify, or count third-party storage implementations; establish persistence,
external-resource lifecycle, free-threaded safety, or maintenance readiness;
publish a package; create a tag or release; add a backend, dependency, format,
or CI job; or claim the locally missed M1/M3 performance targets passed.

## M19 main integration - 2026-08-06

Ready PR #26 was squash-merged at `2026-08-06T10:17:52Z`. GitHub reports
merged commit `1a7219e540d8f4cb3c1f60ff12981513c6860ef9` with sole parent
`4076f3d7ac0c0a82834a1c98dcb36426ba67ac5e`, exact tree
`7fcd614fdde76daf1807f27dbe78ec306a501cc3`, a valid GitHub signature, and the
DCO trailer. The tree exactly matches final evidence head
`b93ca591f7063a1500cf105e6b0496b33573c69a` on retained branch
`codex/m19-world-store-conformance`; `git diff --exit-code` reported no
difference between those trees.

GitHub still lists only successful run `31092244573` for the milestone branch;
the documentation-only hosted-evidence commit used `[skip ci]` and created no
second run. Integration changes no runtime, public API, workflow, dependency,
lock, package version, benchmark target, format, or release artifact. No tag,
GitHub release, PyPI publication, provider discovery/admission/certification,
or independently authored WorldStore adoption is claimed.

## M20 baseline and initial evidence - 2026-08-06

M20 starts from exact clean synchronized `main` commit
`2fdeccd697f09f3e165130eb8564a6c585d472d2` on branch
`codex/m20-command-receipt-stability-decision`.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Approved cache-access rerun resolved 46 packages in 0.84 ms. |
| `uv run --frozen pytest -q tests/unit/test_canonical_json.py tests/unit/test_persistent_command_schema.py tests/unit/test_transactions.py tests/unit/test_receipts.py tests/unit/test_agent_tool_conformance.py tests/integration/test_agent_cli.py tests/architecture/test_api_stability.py` | 0 | 91 focused baseline tests passed in 1.52 seconds. |
| `uv run --frozen pytest -q` | 0 | 955 tests passed with one existing Windows symlink-capability skip in 72.22 seconds. |
| `uv run --frozen python examples/command_receipt_stability_decision.py` | 0 | The initial versioned installed evidence confirmed the current boundary and returned deferred `retain-experimental-command-receipt`. |
| `uv run --frozen pytest -q tests/integration/test_command_receipt_stability_decision.py tests/architecture/test_m20_command_receipt_stability_boundary.py` | 0 | 16 exact-evidence, tamper, stability-drift, argument, dependency, and nested-import boundary tests passed in 2.05 seconds. |

The first sandboxed `uv lock --check` attempt exited 1 before project execution
because uv could not access its existing user cache. The approved cache-access
rerun above is the project result. At this stage the complete static, full,
documentation, build, isolated-wheel, release, provider, benchmark/profile, and
findings-first review gates remain pending. No hosted M20 run, PR, merge, tag,
release, package publication, stability promotion, cross-version compatibility,
or external consumer/adoption evidence is claimed.

## M20 final local validation and review - 2026-08-06

The final reviewed tree remains based on exact `main` commit
`2fdeccd697f09f3e165130eb8564a6c585d472d2`. M20 changes no file under
`.github`, `src/ludoweave`, `pyproject.toml`, or `uv.lock`.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Approved cache-access rerun checked 45 packages. |
| `uv run --frozen ruff format --check .` | 0 | All 205 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built; only the upstream MkDocs Material/MkDocs 2.0 informational warning was emitted. |
| `uv run --frozen pytest -q tests/integration/test_command_receipt_stability_decision.py tests/architecture/test_m20_command_receipt_stability_boundary.py tests/unit/test_release_artifacts.py tests/unit/test_canonical_json.py tests/unit/test_persistent_command_schema.py tests/unit/test_transactions.py tests/unit/test_receipts.py tests/unit/test_agent_tool_conformance.py tests/integration/test_agent_cli.py tests/architecture/test_api_stability.py tests/architecture/test_import_boundaries.py tests/architecture/test_release_workflow.py` | 0 | 211 expanded evidence, canonical transaction/receipt, agent, artifact, and architecture tests passed in 4.24 seconds. |
| `uv run --frozen pytest -q` | 0 | 972 tests passed with one existing Windows symlink-capability skip in 73.99 seconds. |
| `uv build` | 0 | Approved cache-access final build produced `ludoweave-0.1.0a1.tar.gz` and the universal pure-Python wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency installed-wheel workflow, including M20 evidence validation, passed. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m20-release-final` | 0 | A fresh complete ten-artifact release directory was staged. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m20-release-final` | 0 | Checksums, manifest, SPDX SBOM, installed wheel, and all sample-bundle evidence passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Ten real-wgpu integration tests passed in 6.29 seconds. |
| `git diff --check` | 0 | No whitespace errors. |
| `git diff --exit-code main -- .github pyproject.toml uv.lock src/ludoweave` | 0 | Workflow, metadata, lock, and runtime package trees are unchanged. |
| `git fsck --no-dangling` | 0 | Repository object connectivity is clean with no dangling objects reported. |

The M20 evidence runs twice byte-for-byte identically in its integration test.
Its exact validator rejects value and JSON-type drift, arguments, and an
unrecorded stability promotion. The source, isolated wheel, and deterministic
sample-bundle paths all return deferred
`retain-experimental-command-receipt`. The final wheel contains 94 entries,
declares only the existing optional graphics extra, contains no native/WASM
file, and the release sample ZIP contains
`command_receipt_stability_decision.py`.

All inherited documented performance artifacts validate:

- M1's 3,600-tick p95 was 42.0198 ms and observed its 12-second target; the
  10,000-entity simulation p95 was 125.6192 ms and missed the 4 ms target.
- M2's four target-free informational p50/p95 observations were
  31.8993/35.7171 ms for canonical 100-command round trips,
  14.2993/15.8356 ms for atomic 100-command apply, 18.0485/19.5923 ms for
  1,000-entity snapshot round trips, and 210.5091/229.5513 ms for verified
  100-batch replay.
- M3's 10,000-sprite extraction p95 was 26.2983 ms and real-wgpu submission
  p95 was 3.1636 ms; both missed their 3 ms starting targets.
- M4's baseline Clockwork Arena p95 was 2.1096 ms and observed its 16.666667
  ms target. Stress 4/8 p95 values were 3.0000/4.4796 ms with no targets.
- Five-repeat M7 base and graphics profiling artifacts validated with two and
  three workloads respectively. These are call-profile contracts, not timing
  targets.

Development evidence is retained rather than rewritten as a false clean first
attempt. Initial sandboxed `uv lock --check`, `uv sync`, and `uv build` calls
exited 1 before project execution because uv's existing user cache was denied;
approved cache-access reruns exited 0. The first evidence composition omitted
the explicit capture provider required by the M18 profile and was corrected.
The first Ruff pass found two smoke-script import-order issues and passed after
correction. Findings-first review identified that exact-name import checks
would miss forbidden submodules; prefix matching and a nested wgpu fixture now
cover that case, and the focused boundary suite passes 17 tests in 2.05
seconds.

The final scope/credential/backend review found no new credential assignment,
ambient time/random/environment/path input, native/WASM/backend leakage,
runtime/public API change, dependency change, workflow change, stale link, or
unsupported pass claim. No hosted M20 run, PR, merge, tag, release, package
publication, cross-version compatibility, external adoption, or stability
promotion is claimed at this stage.

After recording the final evidence, one post-record gate reran `uv lock
--check`, Ruff format/check, Pyright, strict MkDocs, the 17 M20 integration and
architecture tests, and `git diff --check` in sequence. Every command exited 0;
the focused tests passed in 2.07 seconds. A fresh `git fetch --prune origin`
then confirmed local `main`, `origin/main`, the M20 merge base, and branch HEAD
all share exact base `2fdeccd697f09f3e165130eb8564a6c585d472d2`; the reviewed
history is linear and GitHub reports `main` as the default branch.

## M20 hosted validation - 2026-08-06

Ready PR #28 targets `main` from
`codex/m20-command-receipt-stability-decision`. GitHub reports exact base
`2fdeccd697f09f3e165130eb8564a6c585d472d2`, DCO-signed implementation head
`d96d132da5ee847d6e86645be5e87a1e4aa5e89e`, `MERGEABLE`, and `CLEAN` after
checks completed.

GitHub Actions pull-request run `31095009029` executed that implementation
commit from `2026-08-06T10:52:55Z` through `2026-08-06T10:55:33Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, installed-wheel smoke, release staging, and complete
  release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and GitHub lists this as the only hosted run
for the M20 branch. Hosted evidence confirms supported installed and cross-
platform same-version behavior. It does not establish cross-version
compatibility, external consumer adoption, a public receipt reader, a
deprecation-capable release channel, stability promotion, certification, tag,
release, or package publication; add a runtime/API/schema/dependency/version/CI
change; or claim the locally missed M1/M3 performance targets passed. PR #28
has not yet been merged at this stage.

## M21 main integration - 2026-08-06

Ready PR #30 was squash-merged at `2026-08-06T11:50:27Z`. GitHub reports
merged commit `6bfb56555cafc93a7312f64465ea15cd7c450e79` with sole parent
`feed793e94c345fac4b146c358a68264ef6e5f62`, exact tree
`ea3f410fac31d7a32faee4e697c4fb0941b657df`, a valid GitHub signature verified
at `2026-08-06T11:50:31Z`, and the DCO trailer. The tree exactly matches final
evidence head `4e378756b2a1733de28e7160ac2d6d72921f3e4a` on retained branch
`codex/m21-receipt-reader-baseline`; literal tree comparison reported no
difference.

GitHub still lists only successful run `31098563810` for the milestone branch;
the documentation-only hosted-evidence commit used `[skip ci]` and created no
second run. Integration changes no receipt protocol/field, command, operation,
stability label, workflow, dependency, lock, package version, backend, storage,
benchmark target, root export, or release artifact. No tag, GitHub release,
PyPI publication, cross-version compatibility, receipt authenticity, external
consumer adoption, certification, or stability promotion is claimed.

After `git fetch --prune origin`, local `main` fast-forwarded to the verified
squash commit and matched `origin/main` with a clean worktree. The retained M21
branch remains available for audit history.

After adding this hosted record, `uv run --frozen mkdocs build --strict` and
`git diff --check` both exited 0; the documentation build emitted only the
recorded upstream MkDocs Material/MkDocs 2.0 informational warning.

## M20 main integration - 2026-08-06

Ready PR #28 was squash-merged at `2026-08-06T10:58:12Z`. GitHub reports
merged commit `d166ef86bf25526d9d7715f63263d3cac6db78d4` with sole parent
`2fdeccd697f09f3e165130eb8564a6c585d472d2`, exact tree
`c3e2dc1224f530fb483d1b9684ff55329bf9557b`, a valid GitHub signature verified
at `2026-08-06T10:58:16Z`, and the DCO trailer. The tree exactly matches final
evidence head `d04561184996fac507071ad9e7dd0ef9c5e3cb7c` on retained branch
`codex/m20-command-receipt-stability-decision`; corrected literal-revision
`git rev-parse` checks and `git diff --exit-code` reported equal trees and no
difference.

GitHub still lists only successful run `31095009029` for the milestone branch;
the documentation-only hosted-evidence commit used `[skip ci]` and created no
second run. The first read-only tree query left PowerShell revision braces
unquoted and was parsed incorrectly, producing fatal ambiguous-revision output;
the quoted rerun above exited 0 and is the recorded result. Integration changes
no runtime, public API, protocol, stability label, workflow, dependency, lock,
package version, benchmark target, format, or release artifact. No tag, GitHub
release, PyPI publication, cross-version compatibility, external consumer
adoption, public receipt reader, or stability promotion is claimed.

The documentation-only integration record passes `uv run --frozen mkdocs
build --strict`, `git diff --check`, and the protected-surface comparison
`git diff --exit-code origin/main -- .github pyproject.toml uv.lock
src/ludoweave`; all exited 0. The docs build emitted only the recorded upstream
MkDocs Material/MkDocs 2.0 informational warning.

## M21 baseline and development evidence - 2026-08-06

M21 starts from exact clean synchronized `main` commit
`feed793e94c345fac4b146c358a68264ef6e5f62` on branch
`codex/m21-receipt-reader-baseline`. The branch was created before any M21
change and the initial history inspection showed that commit as local `main`,
`origin/main`, `origin/HEAD`, and the feature-branch base.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the unchanged 46-package lock in 0.71 ms. |
| `uv run --frozen pytest -q tests/unit/test_receipts.py tests/unit/test_persistent_command_schema.py tests/unit/test_canonical_json.py tests/architecture/test_api_stability.py tests/architecture/test_import_boundaries.py tests/unit/test_release_artifacts.py` | 0 | 138 focused baseline tests passed in 1.70 seconds. |
| `uv run --frozen pytest -q` | 0 | The inherited suite passed 972 tests with one existing Windows symlink-capability skip in 69.25 seconds. |
| Corrected reader unit/static group | 0 | 26 reader tests passed in 0.41 seconds; Ruff and Pyright reported no finding for the group. |
| Corrected fixture/reader group | 0 | 24 exact corpus, round-trip, limit, and compatibility tests passed in 0.39 seconds; focused Ruff and Pyright reported no finding. |
| Corrected installed/release group | 0 | 34 deterministic example, validator, isolated-artifact integration, and release-registration tests passed in 2.22 seconds; focused static checks were clean. |
| Combined M20/M21 focused group | 0 | 58 tests passed in 3.46 seconds. Ruff was clean after one mechanical import-order correction; Pyright then identified one frozen-value mutation in a test helper, which was corrected. The combined post-correction gate remains pending. |
| `uv run --frozen ruff check <M20/M21 changed Python files>` | 0 | Corrected focused files passed all Ruff checks. |
| `uv run --frozen pyright` | 0 | Corrected complete project reported zero errors, warnings, or information findings. |
| `uv run --frozen pytest -q tests/unit/test_receipt_reader.py tests/integration/test_receipt_v1_compatibility_corpus.py tests/integration/test_receipt_reader_example.py tests/integration/test_command_receipt_stability_decision.py tests/architecture/test_m21_receipt_reader_boundary.py tests/architecture/test_m20_command_receipt_stability_boundary.py tests/unit/test_release_artifacts.py` | 0 | 60 corrected M20/M21 reader, fixture, evidence, release, and architecture tests passed in 4.10 seconds. |

Development evidence is retained rather than rewritten as a clean first pass.
The first reader unit run had one failing noncanonical-input test because the
test used Python `False` inside handwritten JSON; replacing it with
`json.dumps()` corrected the fixture. Early Ruff findings were import/export
ordering only. Early Pyright findings identified one generic uniqueness helper
type and one inferred example-report return type; both received explicit types.
The installed example emitted the intended deterministic sanitized report
before its static report annotation was corrected. The final helper correction
routes the attempted frozen-field mutation through `setattr` so Pyright can
type-check the architecture test while runtime immutability remains exercised.

At this stage no complete M21 static/full/docs/distribution/graphics/benchmark
gate, final findings-first review, hosted run, PR, merge, tag, release, package
publication, stability promotion, external adoption, or cross-version
compatibility result is claimed.

## M21 final local validation and review - 2026-08-06

The final reviewed tree remains based on exact synchronized `main` commit
`feed793e94c345fac4b146c358a68264ef6e5f62`. M21 changes no file under
`.github`, `pyproject.toml`, `uv.lock`, or `src/ludoweave/__init__.py`.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Approved cache-access rerun resolved the unchanged 46-package lock in 0.76 ms. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Approved cache-access rerun checked 45 packages. |
| `uv run --frozen ruff format --check .` | 0 | All 211 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built after correcting one out-of-tree RFC link; only the upstream MkDocs Material/MkDocs 2.0 informational warning remained. |
| `uv run --frozen pytest -q tests/unit/test_receipt_reader.py tests/integration/test_receipt_v1_compatibility_corpus.py tests/integration/test_receipt_reader_example.py tests/integration/test_command_receipt_stability_decision.py tests/architecture/test_m21_receipt_reader_boundary.py tests/architecture/test_m20_command_receipt_stability_boundary.py tests/unit/test_release_artifacts.py tests/unit/test_canonical_json.py tests/unit/test_persistent_command_schema.py tests/unit/test_transactions.py tests/unit/test_receipts.py tests/unit/test_agent_tool_conformance.py tests/integration/test_agent_cli.py tests/architecture/test_api_stability.py tests/architecture/test_import_boundaries.py tests/architecture/test_release_workflow.py` | 0 | 255 expanded reader, compatibility-fixture, canonical transaction/receipt, agent, release, and architecture tests passed in 5.60 seconds. |
| `uv run --frozen pytest -q` | 0 | 1,015 tests passed with one existing Windows symlink-capability skip in 69.87 seconds. |
| `uv build` | 0 | Approved cache-access rerun built `ludoweave-0.1.0a1.tar.gz` and the universal pure-Python wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installation passed all inherited smoke plus both M20 `/2` and M21 receipt-reader evidence. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m21-release-final` | 0 | Staged a fresh complete ten-artifact candidate with a 20-file sample bundle. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m21-release-final` | 0 | Checksums, manifest, SPDX SBOM, safe extraction, isolated installation, and all bundled evidence including `receipt_reader.py` passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Ten unchanged real-wgpu integration tests passed in 5.83 seconds. |
| `git diff --check` | 0 | No whitespace errors. |
| `git diff --exit-code main -- .github pyproject.toml uv.lock src/ludoweave/__init__.py` | 0 | Workflow, metadata, lock, package version, and root package exports are unchanged. |
| `git fsck --no-dangling` | 0 | Repository object connectivity is clean with no dangling objects reported. |

The inherited performance evidence was regenerated and validated on dirty
Windows/uv-managed CPython 3.12.13 without changing any target. M1's 3,600-tick
p95 was 36.1046 ms and observed its 12-second target; the 10,000-entity
simulation p95 was 118.5788 ms and missed its 4 ms target. M2's four
target-free p50/p95 observations were 29.9931/32.9317 ms for canonical
100-command round trips, 13.8005/16.0934 ms for atomic apply, 17.7123/19.1362
ms for 1,000-entity snapshot round trips, and 199.1210/223.4890 ms for verified
100-batch replay. M3's 10,000-sprite extraction p95 was 25.6030 ms and real-
wgpu submission p95 was 3.0072 ms; both missed their 3 ms starting targets.
M4's baseline p95 was 1.8156 ms and observed its 16.666667 ms target; stress
4/8 p95 values were 2.9891/4.2398 ms with no targets. Five-repeat M7 base and
graphics profiles validated with two and three workloads. No local miss
authorizes native, WASM, dependency, or scope expansion.

Findings-first review corrected four reader-boundary defects before the final
gate: mapping input now enforces encoded `max_bytes`; canonical limit failures
retain causes and map to the typed oversized code; very long numeric entity
identities cannot escape through CPython integer-conversion limits; and changed
component epochs must advance. Nested allocator/epoch objects now fail exact-
field checks before member decoding. New regressions exercise every correction.
The review also confirmed detached inputs, exact status/hash/tick/diff
relationships, experimental-only focused exports, no world mutation or
provider access, and deterministic sanitized evidence.

Development failures remain factual: initial sandboxed lock, sync, and build
attempts exited 1 before project execution because uv's existing user cache was
inaccessible; approved cache-access reruns passed. The first full strict-docs
run exited 1 for an RFC link outside the MkDocs tree and passed after the link
targeted the in-site API-status page. A read-only PowerShell tree query again
interpreted unquoted revision braces, produced ambiguous-revision output, and
passed when the revisions were quoted.

The final scope/security/package review found no new credential assignment,
ambient time/random/environment/path input, backend/native/WASM leakage,
workflow/dependency/lock/version/root-export change, stale link, or unsupported
pass claim. The wheel has 94 entries, only the existing optional exact graphics
requirements, and no native or WASM file. The frozen fixtures and manifest have
exact checked byte sizes/hashes and explicitly claim only
`single-version-baseline`. No hosted M21 run, PR, merge, tag, GitHub release,
PyPI publication, stability promotion, external adoption, certification, or
cross-version compatibility is claimed at this stage.

## M21 hosted validation - 2026-08-06

Ready PR #30 targets `main` from `codex/m21-receipt-reader-baseline`. GitHub
reports exact base `feed793e94c345fac4b146c358a68264ef6e5f62`, DCO-signed
implementation head `cec339be07318a7c1586bb3405e8f9b1904859f5`, `MERGEABLE`,
and `CLEAN` after checks completed.

GitHub Actions pull-request run `31098563810` executed that implementation
commit from `2026-08-06T11:45:38Z` through `2026-08-06T11:48:05Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` passed lock verification, formatting,
  Ruff, Pyright, strict docs, baseline tests, base profile smoke, sdist/wheel
  build, isolated-wheel smoke, release staging, and complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and `gh run list` returned only run
`31098563810` for the M21 branch. Hosted evidence confirms the supported
installed same-version reader behavior and packaging paths. It does not prove
cross-version compatibility, authenticate receipt provenance, establish
external consumer adoption, promote stability, certify a provider, authorize
native acceleration, or create a tag, release, or package publication. PR #30
has not yet been merged at this stage.
