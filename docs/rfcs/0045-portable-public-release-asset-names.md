# RFC-0045: Constrain public release asset names portably

- **Status:** Accepted
- **Date:** 2026-08-12
- **Owners:** LudoWeave maintainers
- **Milestone:** M62

## Context

The public-release consumer parses a bounded asset retrieval plan before it
creates the asset output directory or starts any asset download. Its existing
ASCII basename grammar allowed 256-character names, a trailing period, classic
Windows device stems such as `CON` or `NUL.txt`, and distinct records whose
names differed only by ASCII case. Those spellings do not provide one portable
child-file identity across the supported Windows, macOS, and Linux hosts.

Microsoft documents the classic device stems as reserved even when followed by
an extension and advises against a trailing period. The current release assets
need neither platform-specific spellings nor more than 255 ASCII characters.
The consumer can therefore enforce a deterministic lexical subset without
probing the runner filesystem.

## Decision

One portable asset name:

- is 1 through 255 ASCII characters;
- begins with an ASCII alphanumeric character;
- otherwise contains only ASCII alphanumerics, period, underscore, plus, or
  hyphen;
- does not end with a trailing period; and
- has no case-insensitive first period-delimited stem equal to `CON`, `PRN`,
  `AUX`, `NUL`, `COM1` through `COM9`, or `LPT1` through `LPT9`.

Asset names in one plan must also be unique under ASCII case-insensitive
comparison. Any violation uses existing content-silent
`public_release.invalid_plan`. An invalid existing or freshly generated plan is
rejected before asset download and before creating the asset output directory.
The release document retrieval and validator work that produces a fresh plan
necessarily precede this parser.

## Boundary

M62 performs no filesystem probing, locale-sensitive comparison, Unicode
normalization, case-preservation inference, reserved-name API call, path
resolution, or race isolation. The admitted grammar is an intentionally narrow
portable policy, not a claim that every possible filesystem accepts every
admitted name or that every rejected name is invalid on every host.

M62 adds no cleanup, rollback, retry, workflow, runner allocation, action,
permission, trigger, credential, dependency, lock, version, runtime package/API,
release mutation, release authority, tag, release, or publication. Fixture and
pull-request evidence are not a real public release observation, independent
verification, future availability, immutability, artifact security, PyPI
availability, or a supported channel.

## Consequences

- Platform-sensitive device and trailing-period spellings fail before asset
  output or transport.
- Case-insensitive filename collisions fail during plan parsing.
- The maximum admitted basename is 255 ASCII characters.
- Existing portable release artifact names remain valid.
- The decision is deterministic and independent of the host filesystem.

## Alternatives considered

- Use `Path.is_reserved()` or `os.path.isreserved()`. Rejected because M62 needs
  one version-stable cross-platform policy rather than host-dependent probing.
- Accept case-only pairs and depend on exclusive output creation. Rejected
  because that would begin asset work before discovering a known cross-platform
  collision.
- Permit 256-character or trailing-period names where one host accepts them.
  Rejected because public release artifacts must have one portable identity.
- Normalize or rewrite names. Rejected because downloaded asset names are exact
  authenticated release identities and must never be silently changed.

## References

- [Microsoft: Naming Files, Paths, and Namespaces](https://learn.microsoft.com/windows/win32/fileio/naming-a-file)
- [Python 3.14 `pathlib` documentation](https://docs.python.org/3.14/library/pathlib.html)
- [RFC-0044: separate the public release candidate and output root](0044-public-release-root-separation.md)
