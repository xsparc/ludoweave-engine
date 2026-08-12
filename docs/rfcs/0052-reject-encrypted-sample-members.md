# RFC-0052: Reject encrypted sample members before extraction

- **Status:** Accepted
- **Date:** 2026-08-12
- **Owners:** LudoWeave maintainers
- **Milestone:** M69

## Context

M64 through M68 bound the project sample ZIP's parser input, member count,
declared expansion, codecs, paths, inventory, streaming copy, and publication.
M64 explicitly left encrypted-member policy unchanged. An encrypted member can
therefore pass the complete metadata preflight and reach `ZipFile.open()` only
after the verifier creates its temporary staging directory.

Python 3.12 documents that `zipfile` supports decryption but cannot create
encrypted members, accepts an optional password for member reads, and performs
decryption in Python. CPython's member-open path raises an error containing the
member identity when traditional encryption lacks a password and separately
rejects strong encryption. The PKWARE ZIP Application Note assigns general-
purpose bit 0 to traditional encryption, bit 6 to strong encryption, and bit 13
to masked local-header values associated with central-directory encryption.

The project-produced sample bundle is public, deterministic release evidence.
It has no confidentiality requirement or password-delivery protocol, so any
encryption indicator is outside the intended product shape.

## Decision

During the existing complete central-directory preflight, the private release
smoke rejects a member when any of general-purpose bit flags **0, 6, or 13** is
set. The mask is `0x2041`.

The rejection uses the stable content-silent category `sample bundle contains
an encrypted member`. It occurs before exact-inventory validation, member
reads, staging-directory creation, extraction writes, or password handling.
Every member is checked, independent of archive order.

The current producer remains unchanged and an architecture test independently
proves that it emits no admitted encryption indicator. Other ZIP flags retain
their existing behavior.

## Boundary

M69 does not add a password, key source, credential, decryption capability,
encryption algorithm parser, raw local-header parser, central-directory
decryptor, content scanner, malware detector, authenticated-metadata scheme,
or general archive sandbox. It does not claim that a malicious archive cannot
forge or contradict central-directory metadata; standard-library parsing and
the existing staged checksum remain separate boundaries.

The private rule applies only to the project sample bundle consumed by complete
release smoke. It adds no workflow, runner allocation, action, permission,
credential, dependency, lock, version, runtime package/API, sample producer,
release mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- Traditional encryption, strong encryption, and masked header values fail in
  the complete preflight before member reads and before staging.
- Failure text no longer depends on a member name supplied by the archive.
- The verifier does not need a password-distribution or secret-handling path.
- Existing unencrypted stored and deflated project bundles remain admitted.

## Alternatives considered

- Let `ZipFile.open()` reject encrypted members. Rejected because the failure
  happens after staging begins and can include the archive-controlled member
  identity.
- Supply a password. Rejected because the public deterministic sample bundle
  has no confidentiality need, credential source, or key lifecycle.
- Reject every nonzero general-purpose flag. Rejected because valid producer
  and interoperable ZIP flags unrelated to encryption are outside the evidenced
  gap.
- Parse and compare local-header flags before extraction. Deferred because it
  would introduce a raw ZIP parsing boundary; M69 makes no metadata-
  authentication claim.

## References

- [Python 3.12 `zipfile` documentation](https://docs.python.org/3.12/library/zipfile.html)
- [PKWARE ZIP Application Note](https://www.pkware.com/documents/casestudies/APPNOTE.TXT)
- [CPython 3.12 `zipfile` implementation](https://github.com/python/cpython/blob/3.12/Lib/zipfile/__init__.py)
- [RFC-0047: bound sample-bundle extraction](0047-bounded-sample-bundle-extraction.md)
- [RFC-0051: bound the sample-archive container](0051-bounded-sample-archive-container.md)
