# RFC-0094: Retain sample-member permission compatibility

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE defines external file attributes relative to the host system encoded by
`version made by`. Python exposes the complete public central value as
`ZipInfo.external_attr`. CPython's convenience writer on Windows emits upper-
half mode `0600` without file-type bits. The fixed 50-member LudoWeave producer
emits UNIX regular-file mode `0100644` for every member.

Exact CPython 3.12.13, 3.13.13, and 3.14.5 each expose and read fixtures with
regular-file modes `0100400`, `0100600`, `0100644`, `0100755`, and `0100777`,
as well as missing-type mode `0600`. The payload is unaffected.

M65 already establishes the relevant safety boundary. Release smoke reads the
upper 16 external-attribute bits, rejects an encoded symbolic link, and rejects
any other encoded non-regular file type. A missing file-type marker remains
admitted for compatibility with common producers. Extraction streams bytes into
new owned files and does not apply the archived permission bits.

## Decision

Retain sample-member permission compatibility. Keep the M65 file-type policy
without adding an exact permission value, permission mask, or complete external-
attribute equality rule after M110.

The fixed producer continues to emit UNIX regular-file mode `0100644` for
reproducible artifacts. Producer reproducibility and verifier admission remain
separate contracts.

This is one permission-bit compatibility decision. It adds no error category
or precedence change. Existing path, file-type, inventory, staging, read,
cleanup, and content-silent diagnostics remain unchanged.

## Boundary

M111 adds no exact external-attribute profile, host-system semantics expansion,
permission allowlist, permission normalization, chmod call, umask policy, ACL
interpretation, ownership restoration, special-bit interpretation, raw central
record parsing, payload-content read, decompression, recompression, repair, or
general ZIP validity claim. Extraction performs no permission restoration. It
is not a general archive sandbox and is not a real public release observation.

The decision does not assert that archived permission bits are trustworthy,
portable, or suitable for application to the local filesystem. They are not
canonical runtime state or release authority.

M111 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, verifier, sample producer,
release mutation, release authority, tag, release, or publication.

## Consequences

- Missing-type and regular-file permission variants remain admitted when all
  established structural, metadata, profile, inventory, and content checks pass.
- Encoded symbolic links and other encoded non-regular types remain rejected.
- The fixed producer remains byte-reproducible with UNIX mode `0100644`.
- Extracted permissions continue to be determined by local file creation, not
  archive metadata.

## Alternatives considered

- Require exact mode `0100644`. Rejected because standard-library-produced and
  otherwise admitted archives use missing type bits or other regular modes.
- Admit every external attribute without file-type checks. Rejected because it
  would remove M65's established symlink/non-regular boundary.
- Restore archived permissions. Rejected because those bits are host-relative,
  untrusted input and no release-smoke requirement needs local mode mutation.
- Interpret the lower DOS attribute bits. Deferred because M111 concerns only
  the existing upper-half file-type/permission boundary.

## References

- [PKWARE APPNOTE](https://support.pkware.com/pkzip/appnote)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0048: portable sample member paths](0048-portable-sample-member-paths.md)
- [RFC-0093: retain sample-member timestamp compatibility](0093-retain-sample-member-timestamp-compatibility.md)
