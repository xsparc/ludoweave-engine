# RFC-0213: Bind retained Git WinTrust signed-message SignerInfo values

**Status:** Accepted
**Milestone:** M230
**Decision class:** Direction-preserving

## Context

M229 binds every bounded certificate chain in the live WinTrust countersigner
sequence around M228. Those provider records describe signers derived from a
cryptographic message, but M229 does not bind that message's encoded
`SignerInfo` values.

Microsoft documents `CRYPT_PROVIDER_DATA` as mutable provider-owned state that
exposes the message encoding, an `HCRYPTMSG`, and the provider signer count.
`CryptMsgGetParam` can retrieve the signer count and each encoded
`CMSG_SIGNER_INFO` by zero-based index. It supports a size query followed by an
exact data retrieval for values of unknown length. The provider structure may
change or become unavailable on later Windows versions, so it remains suitable
only for one bounded compatibility observation rather than a new portable API.

Microsoft's Authenticode guidance explains that `SignerInfo` contains the
signature and authenticated or unauthenticated attributes, including a nested
countersignature. Merely copying the opaque encoded value does not parse,
validate, or authorize those fields. Git for Windows also continues to release
new signed binaries, making a persisted encoded value or digest an unsuitable
allowlist. SLSA source provenance remains an SCS-issued statement about a
source revision, not a property established by the local Git executable's
signature message.

## Decision

Bind the complete bounded encoded SignerInfo sequence around the complete M229
boundary in one Windows-only test composition. Repeat M229's exact retained
path/handle, no-UI, cache-only, explicit-no-revocation trust request. While each
successful provider state remains live:

- require a provider structure large enough to contain the documented message
  prefix;
- require a positive raw encoding value, a non-null `HCRYPTMSG`, and a positive
  bounded provider signer count;
- query `CMSG_SIGNER_COUNT_PARAM` and require an exact `DWORD` result equal to
  the provider signer count;
- retrieve every `CMSG_ENCODED_SIGNER` by exact zero-based index using a
  successful size query followed by an exact-size read;
- require positive per-signer and aggregate-bounded encoded lengths;
- copy each complete value before provider state closes;
- compute every encoded SignerInfo SHA-256; and
- compute one domain-separated aggregate SHA-256 over raw encoding, both
  counts, and every exact signer index, length, and encoded value.

Close provider state in a `finally` boundary after success, trust rejection, or
any provider/message extraction failure. Require the complete immutable
observation before and after M229's complete boundary.

The decision does not independently parse or validate SignerInfo. It does not
interpret algorithms, issuer/serial fields, authenticated attributes,
unauthenticated attributes, encrypted digests, countersignatures, or signing
times. It does not establish portable timestamp semantics or authorize a
signer, publisher, or timestamp authority. It creates no persisted identity,
certificate pin, rotation/recovery policy, revocation-freshness proof,
trust-store authority, native DLL/loader binding, repository-acquisition
attestation, local-object-store trust, or source/build provenance. It does not
admit Windows or authorize cleanup.

## Consequences

- Provider and message signer counts must agree within a shared explicit bound.
- A changed encoding, count, order, boundary, encoded value, or digest fails the
  M230 composition.
- A size change between the exact two retrieval phases fails closed instead of
  hashing a partial or padded value.
- M221 through M229 evidence remains byte-for-byte unchanged.
- No runtime, package, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, or admission surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Parse the encoded SignerInfo and enforce algorithms or attributes

Rejected because parsing and policy enforcement would create a new portable
cryptographic compatibility and authorization boundary. M230 only establishes
that the opaque provider message records stay stable around M229.

### Persist the encoded values or hashes as an allowlist

Rejected because normal Git for Windows signing, certificate, timestamp, and
packaging changes would require an unapproved authority, rotation, expiry, and
recovery policy.

### Treat the signed message as repository provenance

Rejected because the signed message authenticates the local executable under
the observed Windows policy; it does not show how a repository revision was
acquired, reviewed, or produced.

### Add the live probe to hosted CI

Rejected because no public self-hosted Windows runner is authorized, and a new
hosted allocation is unnecessary for this local compatibility observation.

## Primary references

- [Microsoft: `CRYPT_PROVIDER_DATA`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_data)
- [Microsoft: `CryptMsgGetParam`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetparam)
- [Microsoft: `CMSG_CMS_SIGNER_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cmsg_cms_signer_info)
- [Microsoft: time stamping Authenticode signatures](https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
