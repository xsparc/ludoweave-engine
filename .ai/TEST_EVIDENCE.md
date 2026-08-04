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
