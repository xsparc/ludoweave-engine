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
