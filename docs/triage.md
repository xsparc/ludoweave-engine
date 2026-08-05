# Issue triage

This is the maintainer contract for turning reports into safe, actionable work. The
checked-in [label catalog](https://github.com/xsparc/ludoweave-engine/blob/main/.github/labels.yml) is the source for project-specific
labels. Maintainers synchronize that catalog through GitHub's label settings; no
write-enabled label automation runs in pull requests.

## Intake

1. Redirect vulnerabilities to the private process in `SECURITY.md` and remove
   accidentally disclosed secrets from public discussion.
2. Reproduce bugs or record why reproduction is blocked. Ask for the exact revision,
   platform, CPython version, command, input, and sanitized result.
3. Map the report to one `area:*` label and one of `bug`, `enhancement`, or
   `documentation`.
4. Use `priority:high` only for a security response, correctness loss, or a named
   release blocker. Otherwise use `priority:normal`.
5. Set exactly one workflow label: `status:needs-design`, `status:blocked`, or
   `status:ready`. Record the missing decision or dependency when work is not ready.

Duplicates should point to the canonical issue before they close. Unsupported or
out-of-scope requests should explain the governing roadmap, ADR, or security boundary.

## Ready work

An issue is `status:ready` only when it has:

- one bounded outcome and explicit non-scope;
- observable acceptance criteria and focused validation commands;
- named compatibility, determinism, security, and dependency-boundary effects;
- enough repository pointers for a contributor to start without private context; and
- a maintainer or reviewer prepared to review it.

Compatibility, schemas, backends, security boundaries, governance, and other topics
listed in `GOVERNANCE.md` require a public RFC before implementation.

## Good-first work

Apply `good first issue` only after the ready-work checks pass and the change can be
completed in one small pull request without adding a public API, dependency, persistent
schema, native boundary, or new subsystem. Also apply `help wanted` when maintainers are
actively seeking an external contributor.

The [roadmap board](https://github.com/xsparc/ludoweave-engine/blob/main/ROADMAP.md#good-first-contribution-queue) contains maintained
starter cards. A contributor should comment on the corresponding issue before working;
a maintainer then records assignment and avoids duplicated effort. The
[first-contribution guide](first-contribution.md) covers setup, DCO sign-off, tests, and
review.

## Review cadence

Maintainers review untriaged issues before milestone planning and before an alpha
release candidate. Stale ready work is revalidated against current code and ADRs rather
than closed solely due to age. Security and conduct reports stay in their private
channels and never enter this queue.
