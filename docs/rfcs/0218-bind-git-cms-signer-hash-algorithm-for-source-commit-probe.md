# RFC-0218: Bind the CMS signer hash algorithm

**Status:** Accepted
**Milestone:** M235
**Decision class:** Direction-preserving

## Context

M234 binds each decoded CMS SignerInfo certificate ID to the same-index
dedicated certificate ID and the complete earlier source-commit observation.
The same CMS signer record also contains a pointer-bearing `HashAlgorithm`, but
M234 deliberately leaves that field unread. Microsoft separately exposes the
same indexed value through `CMSG_SIGNER_HASH_ALGORITHM_PARAM`.

Microsoft defines `CRYPT_ALGORITHM_IDENTIFIER` as an object-identifier pointer
plus an encoded parameter blob. `CryptMsgGetParam` supports a size query
followed by a caller-owned output buffer, may report the actual size on the
second call, and assigns both parameter forms by an exact signer index. New
algorithms may be introduced, and encoded parameters are part of the algorithm
identifier even though many current algorithms use an empty parameter blob.

The current Git for Windows signature exposes a CMS hash algorithm that can be
observed locally. Its algorithm choice can legitimately change in a later
release. Selecting acceptable algorithms or interpreting their cryptographic
strength is a separate policy decision. SLSA source provenance remains an
SCS-issued statement about source revision creation and change controls; local
executable CMS metadata is not source provenance.

## Decision

Bind the CMS signer hash algorithm for every bounded exact signer index in one
Windows-only, test-only, direction-preserving composition around complete
M234.

While each inherited successful provider state remains live, the probe:

- executes M234's complete certificate and SignerInfo identifier correlation;
- reacquires the same non-null message handle and exact bounded signer count;
- performs bounded two-phase reads of `CMSG_CMS_SIGNER_INFO_PARAM` and
  `CMSG_SIGNER_HASH_ALGORITHM_PARAM` for every exact signer index;
- reads the CMS `HashAlgorithm` from the aligned signer-info prefix and the
  dedicated `CRYPT_ALGORITHM_IDENTIFIER` from parameter 8;
- confines the OID pointer and non-empty parameter blob to the actual returned
  owner buffer, requires a bounded in-buffer NUL terminator, and copies both
  values before that buffer expires;
- validates only a bounded ASCII dotted-decimal OID representation and bounded
  encoded parameter bytes;
- requires exact OID and encoded-parameter equality between both same-index
  representations;
- retains detached OIDs, parameter sizes, domain-separated per-index hashes,
  and one count/index/value sequence digest; and
- requires the complete detached observation before and after M234's complete
  retained-file boundary.

Provider state closes through M234's inherited `finally` discipline after
every outcome. The observation does not approve or reject an algorithm based
on its identity, parameter encoding, strength, age, or suitability. It does
not create an algorithm allowlist, negotiate an algorithm, interpret parameters,
or revalidate the signature.

This decision adds no signer or publisher authorization, certificate policy,
revocation freshness, portable chain or timestamp semantics, native loader or
DLL identity, local-object-store trust, repository-acquisition evidence, or
source/build provenance. It does not admit Windows or authorize cleanup.

## Consequences

- The CMS signer-info and dedicated API representations must agree at every
  exact signer index instead of being inferred from one another.
- Escaped pointers, missing in-buffer termination, malformed textual OIDs,
  oversized values, read-size changes, and representation mismatches refuse.
- Algorithm identity and opaque encoded parameters become reproducible local
  evidence without becoming algorithm-selection policy.
- M221 through M234 evidence remains byte-for-byte unchanged.
- No runtime, package, API, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, admission, or hosted surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Infer the algorithm from one representation

Rejected because either API result alone cannot prove that the separately
marshalled same-index CMS field agrees.

### Add a SHA-family allowlist

Rejected because identity correlation and cryptographic acceptability are
different decisions. An allowlist requires lifecycle, compatibility, and
failure-policy review beyond this observation slice.

### Dereference native pointers without owner bounds

Rejected because a successful native call does not justify reading outside the
actual caller-owned output buffer or after its lifetime.

### Add the live probe to hosted CI

Rejected because no public self-hosted Windows runner is authorized, and this
local compatibility observation does not justify recurring hosted allocation.

## Primary references

- [Microsoft: `CMSG_CMS_SIGNER_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cmsg_cms_signer_info)
- [Microsoft: `CRYPT_ALGORITHM_IDENTIFIER`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-crypt_algorithm_identifier)
- [Microsoft: `CryptMsgGetParam`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetparam)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
