# RFC-0095: Retain sample-member creating-system compatibility

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PKWARE defines the upper byte of central-directory `version made by` as the
host system with which a member's external attributes are compatible. Host `0`
denotes the DOS family and host `3` denotes UNIX; external-attribute meaning is
host dependent. Python exposes that byte as public `ZipInfo.create_system`.

CPython intentionally initializes `ZipInfo.create_system` to `0` on Windows
and `3` elsewhere. Exact CPython 3.12.13, 3.13.13, and 3.14.5 each preserve and
read representative parser-exposed values `0`, `3`, `10`, `19`, and `255` in
otherwise admitted fixtures. The fixed 50-member LudoWeave producer explicitly
emits `(create_version, create_system) == (20, 3)`.

M108 considered coupling its exact creation-version rule to
`create_system == 3`. The complete architecture suite produced 54 established
Windows-fixture regressions, so that host restriction was removed. M111 then
confirmed that M65's existing file-type boundary admits common Windows-style
missing type bits and UNIX regular-file attributes without restoring archived
permissions.

## Decision

Retain sample-member creating-system compatibility. Complete release smoke
continues to apply no creating-system allowlist and adds no host marker
classifier after M111.

M65's existing external-attribute file-type policy remains unchanged: encoded
symbolic links and encoded non-regular types fail, while a missing type marker
or regular-file marker can continue through later policy. The creating-system
marker does not bypass that boundary and does not cause archived attributes to
be applied locally.

The fixed producer continues to emit creating system `3` for reproducible
artifacts. Producer reproducibility and verifier admission remain separate
contracts.

This is one host-marker compatibility decision. It adds no error category or
precedence change. Existing structural, metadata, file-type, inventory,
staging, read, cleanup, and content-silent diagnostics remain unchanged.

## Boundary

M112 adds no creating-system allowlist, no exact creating-system profile, no
host-specific external-attribute interpretation, no attribute normalization,
no permission restoration, no chmod operation, no ownership or ACL handling,
no raw central-record parsing, no payload-content read, no decompression,
recompression, repair, or general ZIP validity claim. It is not a general
archive sandbox and is not a real public release observation.

The decision does not assert that every host marker or external-attribute value
has equivalent meaning. It preserves the established parser-exposed admission
boundary because extraction copies bytes into newly created owned files and
does not apply archived attributes.

M112 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, verifier, sample producer,
release mutation, release authority, tag, release, or publication.

## Consequences

- Standard-library Windows and non-Windows creating-system markers remain
  admitted when every established check passes.
- Other parser-exposed host markers remain unclassified rather than being
  converted into a new allowlist.
- M65's encoded symlink/non-regular rejection remains in force independently of
  the creating-system marker.
- The fixed producer remains byte-reproducible with creating system `3`.
- Extracted files continue to receive local creation attributes rather than
  archived host-specific attributes.

## Alternatives considered

- Require exact creating system `3`. Rejected because M108 demonstrated 54
  regressions in established Windows-created compatibility fixtures.
- Allow only systems `0` and `3`. Rejected because no extraction security
  property depends on that allowlist and the verifier does not apply archived
  attributes.
- Interpret external attributes according to every host marker. Deferred
  because no release-smoke requirement needs a cross-platform attribute
  semantics engine.
- Change the deterministic producer to the local platform default. Rejected
  because explicit system `3` and mode `0100644` are part of reproducible
  artifact production, not verifier admission.

## References

- [PKWARE APPNOTE](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Python `ZipInfo` documentation](https://docs.python.org/3/library/zipfile.html#zipfile.ZipInfo)
- [CPython 3.14 `zipfile` implementation](https://github.com/python/cpython/blob/3.14/Lib/zipfile/__init__.py)
- [RFC-0091: require exact sample-member creation version](0091-require-exact-sample-member-creation-version.md)
- [RFC-0094: retain sample-member permission compatibility](0094-retain-sample-member-permission-compatibility.md)
