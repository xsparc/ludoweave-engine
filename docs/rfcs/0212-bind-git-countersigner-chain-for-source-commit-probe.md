# RFC-0212: Bind retained Git WinTrust countersigner chains

**Status:** Accepted
**Milestone:** M229
**Decision class:** Direction-preserving

## Context

M228 binds the complete provider-index certificate sequence of the primary
WinTrust signer around M227. The complete signer structure also exposes a
`csCounterSigners` count, and the provider helper supports retrieving each
countersigner by a zero-based index. M228 neither enumerates those
countersigners nor binds their provider-certificate chains.

Microsoft documents countersigners as provider data associated with a primary
signer. It also documents Authenticode time stamps as PKCS #7 countersignatures
that depend on a trusted time source. Those facts support observing the complete
provider-index sequence, but they do not make a raw countersigner structure a
portable timestamp-validation or authorization policy. Microsoft separately
cautions that the provider helper may change and points independent certificate
validation toward other APIs.

Git for Windows continues to release new versions beyond the local installation
used by this evidence. Persisting a locally observed timestamp identity or chain
would therefore create an unapproved authority, rotation, expiry, revocation,
and recovery policy. SLSA source provenance remains an SCS-issued statement
about a source revision, not a property conferred by a local executable's
countersigner.

## Decision

Bind the complete indexed WinTrust countersigner sequence around the complete
M228 boundary in one Windows-only test composition. Repeat M228's exact retained
path/handle, no-UI, cache-only, explicit no-revocation trust request. While each
successful provider state remains live:

- require provider data and the primary signer;
- require a positive bounded primary countersigner count;
- retrieve every countersigner by exact zero-based provider index;
- require zero provider error, a positive raw verification time, and a positive
  bounded certificate-chain count for each countersigner;
- retrieve every countersigner certificate by exact zero-based provider index;
- copy positive per-certificate and aggregate-bounded DER before provider state
  closes;
- compute per-certificate and per-chain SHA-256 values; and
- compute one domain-separated aggregate SHA-256 over countersigner count plus
  every exact countersigner index, raw signer type, provider error, verification
  time, chain count, certificate index, DER length, and DER value.

Close provider state in a `finally` boundary after success, trust rejection, or
any countersigner extraction failure. Require the complete immutable observation
before and after M228's complete boundary.

The ordering is only the provider-index sequence observed during one execution.
Retain the raw signer type and verification-time values without interpreting
them as a portable timestamp policy. This decision does not establish
timestamp-authority authorization, signer or publisher authorization,
certificate pinning, rotation/recovery, timestamp token or signing-time
validation, revocation freshness, trust-store authority, native DLL/loader
identity, repository acquisition, local-object-store trust, or source/build
provenance. It does not admit Windows or authorize cleanup.

## Consequences

- Every countersigner and certificate in the bounded live provider sequence
  must be available and detached before state close.
- A changed count, order, raw metadata value, certificate boundary, DER value,
  or digest fails the M229 composition.
- M221 through M228 evidence remains byte-for-byte unchanged.
- No runtime, package, dependency, lock, workflow, permission, fixture, example,
  script, benchmark, cleanup, or admission surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Authorize the observed timestamp authority

Rejected because one provider observation does not define authority ownership,
rotation, expiry, revocation, recovery, or compatibility policy.

### Parse and independently validate the timestamp token

Rejected because M229 is a narrow extension of the successful WinTrust provider
state. An independent RFC 3161 or PKCS #7 policy would be a different trust
boundary and does not follow from M228.

### Persist the countersigner sequence as an allowlist

Rejected because the sequence is rotation-sensitive current-host evidence. A
durable allowlist requires separately approved authority and recovery rules.

### Treat the countersigner as source provenance

Rejected because authenticating time or a local executable remains distinct
from proving how a repository revision was acquired, reviewed, or produced.

## Primary references

- [Microsoft: `CRYPT_PROVIDER_SGNR`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_sgnr)
- [Microsoft: `WTHelperGetProvSignerFromChain`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovsignerfromchain)
- [Microsoft: `WTHelperGetProvCertFromChain`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovcertfromchain)
- [Microsoft: time stamping Authenticode signatures](https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
