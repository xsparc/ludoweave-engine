# RFC-0215: Bind Git message signer certificate identifiers

**Status:** Accepted
**Milestone:** M232
**Decision class:** Direction-preserving

## Context

M231 verifies every bounded exact signer in the live WinTrust cryptographic
message and requires the returned certificate DER to equal the same-index
primary provider certificate. The composition does not separately observe the
issuer and serial number carried by the message's signer-certificate selector.

Microsoft documents `CMSG_SIGNER_CERT_INFO_PARAM` as returning the certificate
information needed to identify a message signer's certificate. Only the
`Issuer` and `SerialNumber` fields are valid in that returned `CERT_INFO`.
Microsoft describes those fields together as uniquely identifying a
certificate for retrieval. The installed Windows SDK defines the parameter as
value 7.

`CERT_CONTEXT.pCertInfo` exposes the complete parsed certificate information
while the certificate context remains live. Therefore one execution-local
probe can copy and compare the exact identifier blobs from the message, the
verified certificate, and the same-index provider certificate without adding
an identity registry or certificate policy.

Exact raw equality is intentionally narrower than a general certificate-name
or integer equivalence service. The values compared here originate from one
live WinTrust message and its already byte-equal certificates. A future
portable identity policy would need explicit normalization, authority,
rotation, expiry, and recovery rules.

Git for Windows signing material can legitimately change between releases.
SLSA source provenance remains an SCS-issued statement about the creation and
change controls of a source revision; local executable certificate correlation
is not source provenance.

## Decision

Bind the message signer certificate identifier to the exact verified and
provider certificates for every bounded exact signer index in one Windows-
only, test-only composition around complete M231.

Repeat M231's retained Git path/handle and no-UI, cache-only, explicit-no-
revocation `WINTRUST_ACTION_GENERIC_VERIFY_V2` request. While each successful
provider state remains live:

- require a compatible provider prefix, non-null message handle, positive
  bounded signer count, and bounded provider-store count;
- require provider and message signer counts to agree;
- retrieve `CMSG_SIGNER_CERT_INFO_PARAM` for every exact signer index through a
  bounded two-phase read;
- copy only its positive bounded issuer and serial-number blobs;
- verify the exact message signer and copy the same two fields from its live
  certificate context before releasing it;
- resolve the same-index primary provider certificate and copy the same two
  fields;
- retain M231's exact verified/provider DER equality;
- require exact issuer and serial-number equality across message, verified,
  and provider sources;
- retain exact component lengths, domain-separated per-source hashes, and one
  count/index/length/value sequence digest; and
- require the complete detached observation before and after M231's complete
  boundary.

Close provider state in `finally` after success, rejection, extraction failure,
or certificate-release failure. Preserve the primary extraction or comparison
failure if certificate release also fails.

This does not create signer or publisher authorization. It defines no
allowlist, persisted identity, certificate pin, expiry, rotation, recovery, or
publisher-name rule. It does not establish revocation freshness, portable
chain or timestamp semantics, timestamp-authority authorization, signing-time
authenticity, trust-store administration, native DLL/loader identity, local
object-store trust, repository-acquisition evidence, or source/build
provenance. It does not admit Windows or authorize cleanup.

## Consequences

- A missing or malformed message selector, parsed certificate identifier,
  index, certificate, store, provider record, or native resource rejects the
  M232 observation.
- Exact message, verified-certificate, and provider-certificate identifier
  boundaries are explicit and detached before native lifetimes end.
- The observation changes naturally when a future Git for Windows release
  legitimately changes its signing certificate.
- M221 through M231 evidence remains byte-for-byte unchanged.
- No runtime, package, API, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, admission, or hosted surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Infer the identifier from equal certificate DER

Rejected for this compatibility boundary because the message directly exposes
its signer-certificate selector and an exact comparison can detect indexing or
marshalling mistakes independently of DER equality.

### Compare display names or formatted serial strings

Rejected because formatting introduces locale, display, normalization, and
ambiguity concerns. This probe copies the encoded issuer and integer blobs.

### Persist the identifier as an allowlist

Rejected because persistence would create authorization, rotation, expiry,
recovery, and trust-distribution obligations outside this slice.

### Treat the result as source provenance

Rejected because executable certificate correlation does not show how the
repository revision was acquired, reviewed, or produced by its source-control
system.

### Add the live probe to hosted CI

Rejected because no public self-hosted Windows runner is authorized, and the
existing local Windows capability is sufficient for this compatibility
observation.

## Primary references

- [Microsoft: `CryptMsgGetParam`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetparam)
- [Microsoft: `CERT_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_info)
- [Microsoft: `CERT_CONTEXT`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_context)
- [Microsoft: `CertCompareCertificateName`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certcomparecertificatename)
- [Microsoft: `CertCompareIntegerBlob`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certcompareintegerblob)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
