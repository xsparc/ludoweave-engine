# Quality checks

Run these commands from the repository root with the locked uv environment.
Record actual exit results and skips; no command in this guide is a claim that
it has already passed. No additional hosted CI jobs are required by this guide.

## Standard checks

```console
uv lock --check
uv sync --frozen --all-groups --extra graphics --extra audio
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen pyright
uv run --frozen pytest -q
uv run --frozen mkdocs build --strict
git diff --check
```

For documentation-only edits, start with the strict docs build and affected
architecture tests. Run broader checks when test logic or packaging changes.
Graphics tests need the optional provider and a working graphics runtime;
headless tests do not prove real-device output. Consult the existing workflow
for platform setup rather than adding hosted jobs for every documentation edit.

## Distribution checks

Use new, empty output directories for each qualification. If these names already
exist, choose fresh names consistently; do not delete unrelated artifacts.

```console
uv build --out-dir .tmp/dist-first
uv build --out-dir .tmp/dist-second
uv run --frozen python scripts/verify_distribution_reproducibility.py .tmp/dist-first .tmp/dist-second
uv run --frozen python scripts/smoke_wheel.py .tmp/dist-first
uv run --frozen python scripts/smoke_scene_wheel.py .tmp/dist-first
uv run --frozen python scripts/smoke_audio_wheel.py .tmp/dist-first
uv run --frozen python scripts/smoke_input_replay_wheel.py .tmp/dist-first
uv run --frozen python scripts/release_artifacts.py .tmp/dist-first .tmp/release-candidate
uv run --frozen python scripts/smoke_release.py .tmp/release-candidate
```

These are local packaging rehearsals, not authorization to tag or publish a
release. See the [release process](release-process.md).

## Performance and specialized probes

Benchmark/profile runs are not every edit's fast gate. Their commands are
preserved in the [historical quality reference](readme-history.md#quality-commands)
and explained by the [benchmark methodology](benchmarks.md).
Record timing misses without claiming an unmeasured speedup. The Box2D candidate
probe and unsupported-interpreter observations are evaluations, not standard
dependencies or support promises.

The [test evidence](https://github.com/xsparc/ludoweave-engine/blob/main/.project/TEST_EVIDENCE.md) records executed commands;
historical records are scoped to their original commit and environment.
