# Test Evidence

Only commands actually executed in the current repository are recorded here.

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

GitHub-hosted Windows/macOS/Linux and Python 3.13/3.14 jobs have not run for these changes. No hosted or cross-platform pass claim is made.

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
