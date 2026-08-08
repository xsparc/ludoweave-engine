# RFC-0020: CI change qualification

- **Status:** Accepted
- **Date:** 2026-08-08

## Context

M36 preserved eight validation slices in three OS-owned hosted allocations.
That is the minimum allocation count for a substantive change that must retain
real Windows, macOS, and Linux evidence. It is unnecessary for a
documentation-only change to repeat full cross-platform runtime, graphics, and
compatibility suites when source, tests, dependencies, packaging inputs, and
automation are unchanged.

Removing the workflow trigger for documentation paths is not a safe substitute.
GitHub documents that a workflow skipped by path filtering can leave associated
required checks pending, while a job skipped by a conditional reports success.
GitHub also documents that jobs named by `needs` wait for and depend on their
prerequisite job. M37 therefore keeps one visible workflow and performs strict
qualification inside its existing Linux allocation.

References:

- [Using conditions to control job execution](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions?apiVersion=2022-11-28)
- [Using jobs in a workflow](https://docs.github.com/en/enterprise-cloud%40latest/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs)
- [Skipping workflow runs](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs)

## Decision

The Linux job classifies the pull-request three-dot diff before expensive work.
It executes the classifier stored at the exact base revision, not the pull-
request copy. A pull request therefore cannot weaken qualification merely by
editing the classifier. The first pull request that introduces the classifier,
a missing base classifier, an empty diff, invalid revision, diff failure,
undecodable path, ambiguous path, or any unrecognized path fails closed to the
substantive policy or fails the Linux job.

Documentation-only admission is deliberately narrow:

- Markdown files at the repository root;
- Markdown files below `docs/` and `.project/`;
- `.github/labels.yml`, the pull-request template, and issue forms.

Everything else is substantive, including non-Markdown files below `docs/` or
`.project/`, `mkdocs.yml`, runtime, tests, scripts, dependencies, lockfiles,
licenses/notices, packaging configuration, workflows, release policy, and
executable repository security/governance controls. This prevents a candidate
from adding a documentation hook or changing documentation execution policy
under the smaller gate.

A documentation-only pull request uses one hosted allocation. The Linux job
still verifies the lock, installs the locked documentation environment, checks
Python formatting and lint, builds strict documentation, runs all architecture
tests, builds the sdist/wheel, smoke-tests the isolated wheel, stages the release
candidate, and smoke-tests the release candidate. Distribution checks remain
because the root README and documentation enter package or release artifacts.
Type checking, complete runtime tests, profiling, and graphics tests are skipped
only because their inputs cannot be changed by the admitted path set.

A substantive pull request uses the same three hosted allocations and all eight
M36 validation slices. The Linux job emits the qualification result after
checkout and setup, performs its complete quality/distribution/graphics/
compatibility gate, and the Windows/macOS matrix runs only after Linux succeeds
with `substantive=true`. A failed or indeterminate Linux job blocks the pull
request and prevents the two desktop allocations from consuming quota.

The existing workflow remains pull-request only, ignores `.project/**`-only
changes entirely, cancels superseded runs, and retains least privilege, exact
action and uv pins, disabled checkout credentials, lock-based caching, bounded
timeouts, and desktop fail-fast isolation.

## Consequences

- Documentation-only changes require one hosted allocation instead of three.
- Substantive changes retain three hosted allocations and every M36 slice.
- A Linux qualification failure avoids two desktop allocations, but substantive
  desktop feedback begins only after Linux completes.
- The Linux checkout includes history so the exact base and head revisions can
  be compared and the trusted base classifier can be loaded.
- The policy does not claim a billed-minute reduction, documentation-only hosted
  success, or future required-check configuration until exact hosted evidence
  exists.
- No runtime, public API, protocol, format, dependency, lockfile, package
  version, release workflow, tag, publication, or support-policy change occurs.

## Alternatives considered

A separate change-filter job was rejected because every substantive pull
request would allocate a fourth runner. Workflow-level documentation path
filtering was rejected because it can leave required checks pending and would
provide no documentation validation. Trusting the pull-request copy of the
classifier was rejected because the code deciding whether tests run must not be
replaceable by the same diff it classifies. Removing desktop or compatibility
slices was rejected because it would weaken the supported platform contract.
