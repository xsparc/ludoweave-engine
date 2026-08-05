# First contribution

This walkthrough is deliberately complete enough to use without private
maintainer knowledge. A documentation or focused test correction is the best
first change; select an item labelled `good first issue` whose acceptance notes
name the expected file and verification command.

## 1. Prepare the checkout

Fork and clone the repository, then create one task branch:

```console
git switch -c docs/your-focused-change
uv sync --frozen --all-groups --extra graphics
```

Read `AGENTS.md`, `.ai/PROJECT_STATE.md`, `.ai/CURRENT_TASK.md`, the relevant
guide/ADR, and `git status`. Do not discard unrelated changes.

## 2. Reproduce the baseline

Run the smallest check named by the issue. For a guide/link correction:

```console
uv run --frozen mkdocs build --strict
```

For Python behavior, run the focused test file first. Record the exact command,
exit status, and result; a failure is evidence, not a pass.

## 3. Make one coherent change

- Preserve canonical ECS/world ownership and headless operation.
- Do not leak provider objects or add arbitrary evaluation/network control.
- Add/update tests and docs with behavior.
- Update `CHANGELOG.md` for user-visible work.
- If adding a supported export, update `__all__` and `__stability__` together.
- Stop if the task needs a new compatibility, persistent-schema, backend,
  security, governance, networking, editor, 3D, or native-code decision.

## 4. Run the complete gate

```console
uv lock --check
uv sync --frozen --all-groups --extra graphics
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen pyright
uv run --frozen pytest -q
uv run --frozen mkdocs build --strict
uv build
uv run --frozen python scripts/smoke_wheel.py dist
uv run --frozen python scripts/release_artifacts.py dist .tmp/release-candidate
uv run --frozen python scripts/smoke_release.py .tmp/release-candidate
git diff --check
```

Use a new empty release staging directory if `.tmp/release-candidate` already
exists. Milestone benchmark commands are required only when performance is
affected or claimed.

## 5. Review and submit

Review the diff for scope growth, credentials, personal paths, backend/native
leakage, unsafe paths, nondeterministic authority inputs, packaging changes,
and stale documentation. Commit with DCO sign-off:

```console
git commit -s
```

Open a pull request using the repository template. Map the result to the issue's
acceptance criteria, list exact executed commands, identify API/schema,
determinism, security, dependency, and platform effects, and state explicit
non-goals. A maintainer may request a focused correction or a design discussion;
that is normal review, not a request to expand the task.

## Rehearsal definition

The community-alpha CI rehearses this public path from a clean checkout on
Windows, macOS, and Linux: locked setup, quality/docs, complete tests, pure-wheel
build, isolated installed-wheel smoke, release staging, checksum/SBOM validation,
and bundled headless samples. No external-contributor usability study has yet
been recorded; report unclear or missing steps as documentation bugs.
