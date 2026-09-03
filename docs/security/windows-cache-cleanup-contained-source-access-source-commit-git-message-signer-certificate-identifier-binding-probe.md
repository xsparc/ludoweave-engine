# Windows contained source-access source-commit Git message-signer certificate-identifier binding probe

**Status:** Accepted M232 current-repository test evidence; signer and publisher
authorization, certificate pinning, revocation freshness, provenance, Windows
admission, and cleanup authority remain unresolved.

## Boundary

M232 composes one Windows-only, test-only certificate-identifier observation
around the complete M231 boundary. It repeats the exact retained Git path and
handle plus M231's no-UI, cache-only, explicit-no-revocation
`WINTRUST_ACTION_GENERIC_VERIFY_V2` request. No network retrieval is enabled.

While each successful provider state remains live, the probe requires a
compatible provider prefix, a non-null cryptographic-message handle, a
positive bounded signer count, and a bounded provider-store count. The message
and provider signer counts must agree. A positive store count requires the live
provider store array.

For every exact message signer index, a bounded two-phase
`CMSG_SIGNER_CERT_INFO_PARAM` read copies only the returned `CERT_INFO` issuer
and serial-number blobs. Microsoft documents only these two fields as valid for
that parameter and describes them together as identifying the signer
certificate for retrieval.

The probe then verifies that exact message signer, copies the issuer and serial
number from its live returned certificate context, and releases the context.
It resolves the same-index primary provider certificate and copies the same
fields. M231's exact verified/provider certificate-DER equality is retained.
The message, verified-certificate, and provider-certificate identifier values
must be exactly equal.

The detached observation retains provider-store and signer counts, exact
issuer/serial component lengths, a domain-separated identifier hash for each
source and index, and one domain-separated aggregate over every source,
boundary, index, length, and byte sequence. The complete observation must match
before and after the complete M231 boundary.

Every returned certificate context is released even when verification reports
failure after returning a context. Provider state closes in `finally` after
success, trust rejection, malformed data, extraction or comparison failure,
context-release failure, or another observed outcome. A primary failure is
preserved if certificate release also fails; a release or state-close failure
is reported after otherwise successful extraction.

## What this proves

- The current host can retrieve the certificate selector for every bounded
  exact message signer index.
- Exact issuer and serial-number blobs agree across the message selector, the
  verified message certificate, and the same-index primary provider
  certificate.
- Counts, order, component boundaries, bytes, and hashes remain stable across
  M231's complete retained-file interval.
- Returned certificate contexts and provider state close on every exercised
  outcome.

## What this does not prove

The observation does not authorize a signer or publisher. It defines no
certificate allowlist, persisted identity, pin, expiry, rotation, recovery, or
publisher-name policy. It does not establish general semantic certificate-name
or integer equivalence and does not administer the Windows trust store.

It does not establish revocation freshness, portable certificate-chain or
timestamp semantics, timestamp-authority authorization, independent timestamp-
token validation, signing-time authenticity, or durable identity across Git
for Windows releases. Cached WinTrust success remains the only trust-policy
observation.

It is not source or build provenance, repository-acquisition evidence, local-
object-store trust, native DLL/loader identity, distinct-principal or
independent-host proof, or a hostile/privileged bypass claim. Criteria 6 and 7
remain unresolved.

Windows is not admitted. Cleanup remains unimplemented and unauthorized. M232
adds no runtime source, public API, CLI or MCP command, production collector,
filesystem mutation, dependency, lock change, fixture, example, script,
benchmark, workflow, permission, public runner, or hosted allocation.

## Primary references

- [Microsoft: `CryptMsgGetParam`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetparam)
- [Microsoft: `CERT_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_info)
- [Microsoft: `CERT_CONTEXT`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_context)
- [Microsoft: `CertCompareCertificateName`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certcomparecertificatename)
- [Microsoft: `CertCompareIntegerBlob`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certcompareintegerblob)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
