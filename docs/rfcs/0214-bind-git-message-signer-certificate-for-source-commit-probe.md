# RFC-0214: Bind verified Git message signers to provider certificates

**Status:** Accepted
**Milestone:** M231
**Decision class:** Direction-preserving

## Context

M230 binds every bounded opaque encoded `SignerInfo` value exposed by the live
WinTrust cryptographic message. M227 separately binds the provider's primary
signer certificate, but the current composition does not directly show that
the message signature verifies with the same certificate bytes selected by the
provider for each signer index.

Microsoft documents `CryptMsgGetAndVerifySigner` as verifying a cryptographic
message signature and optionally returning the matching certificate context.
`CMSG_USE_SIGNER_INDEX_FLAG` restricts the operation to the exact supplied
signer index. The function can search supplied certificate stores in addition
to certificates carried by the message. A returned `CERT_CONTEXT` exposes the
encoded certificate and must be released with `CertFreeCertificateContext`.

The provider-owned `CRYPT_PROVIDER_DATA` structure exposes its message, store
array, and signer count, but Microsoft warns that this structure may change or
become unavailable. This remains suitable only for one bounded Windows
compatibility observation, not a new portable or public API.

Git for Windows continues to release new signed binaries, so observed
certificate bytes are not a durable allowlist. SLSA source provenance remains
an SCS-issued statement about a source revision and its change process; message
signature verification on the local Git executable is not source provenance.

## Decision

Correlate the verified message signer certificate with the primary WinTrust
provider certificate for every bounded exact signer index in one Windows-only,
test-only composition around complete M230.

Repeat M230's retained Git path/handle and no-UI, cache-only,
explicit-no-revocation `WINTRUST_ACTION_GENERIC_VERIFY_V2` request. While each
successful provider state remains live:

- require a compatible provider prefix, non-null message handle, positive
  bounded signer count, and a bounded provider-store count;
- require provider and message signer counts to agree;
- reject a positive provider-store count with no store array;
- invoke `CryptMsgGetAndVerifySigner` for every exact index with only
  `CMSG_USE_SIGNER_INDEX_FLAG`;
- require successful signature verification, an unchanged returned index, and
  a non-null returned certificate context;
- copy positive per-certificate and aggregate-bounded encoded DER;
- resolve the corresponding primary provider certificate for the same index;
- require the message and provider DER bytes to be exactly equal;
- retain exact lengths, both per-source SHA-256 tuples, and one domain-separated
  count/index/length/value digest; and
- release every returned certificate context before provider state closes.

Close provider state in `finally` after trust success, rejection, correlation
failure, or certificate-release failure. Preserve the primary extraction or
verification failure if context release also fails. Require the complete
immutable observation before and after M230's complete boundary.

This does not create signer or publisher authorization. It does not set
`CMSG_TRUSTED_SIGNER_FLAG`, define an allowed certificate, persist an identity,
pin a certificate, establish portable chain or timestamp semantics, independently
authorize a timestamp authority, prove revocation freshness, administer the
trust store, bind native DLL/loader state, authenticate the local object store
or repository acquisition, or establish source/build provenance. It does not
admit Windows or authorize cleanup.

## Consequences

- A message-signature failure, changed index, missing context, invalid size,
  provider lookup failure, byte mismatch, free failure, or state-close failure
  rejects the M231 observation.
- Message and provider certificate identity are correlated by exact detached
  bytes, not by a display name, serial string, saved fingerprint, or path.
- The result remains execution-local and naturally changes when a future Git
  for Windows release legitimately changes signing material.
- M221 through M230 evidence remains byte-for-byte unchanged.
- No runtime, package, API, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, admission, or hosted surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Treat WinTrust's successful provider result as sufficient correlation

Rejected for this compatibility boundary because M230 exposes the live message
and M227 exposes provider certificate bytes, so exact indexed correlation can
be tested without adding production authority.

### Mark provider stores as trusted

Rejected because `CMSG_TRUSTED_SIGNER_FLAG` would give those stores an authority
meaning that this observation does not define. WinTrust performs the existing
cached trust-policy decision; M231 verifies the message signature and compares
the returned certificate bytes.

### Persist the certificate hash as an allowlist

Rejected because normal signing and release changes require an explicit
publisher, rotation, expiry, and recovery policy that is outside this slice.

### Treat the verified local executable as source provenance

Rejected because executable signature verification does not show how the
repository revision was acquired, reviewed, or produced by its source-control
system.

### Add the live probe to hosted CI

Rejected because no public self-hosted Windows runner is authorized, and the
existing local Windows capability is enough for this compatibility observation.

## Primary references

- [Microsoft: `CryptMsgGetAndVerifySigner`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetandverifysigner)
- [Microsoft: `CERT_CONTEXT`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_context)
- [Microsoft: `CertFreeCertificateContext`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certfreecertificatecontext)
- [Microsoft: `CRYPT_PROVIDER_DATA`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_data)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
