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
