# RFC-0211: Bind retained Git WinTrust provider chain

**Status:** Accepted
**Milestone:** M228
**Decision class:** Direction-preserving

## Context

M227 proves that successful live WinTrust state exposes one bounded primary
signer certificate before and after M226. The signer structure also reports a
bounded `csCertChain` count, but M227 copies only provider-certificate index
zero. It therefore does not bind the rest of the provider's indexed
certificate sequence across the retained-file interval.

Microsoft documents `csCertChain` as the number of elements in the
`pasCertChain` array and documents zero-based provider-certificate lookup
through `WTHelperGetProvCertFromChain`. The API exposes provider state; its
documentation does not define a portable semantic ordering contract suitable
for issuer-policy decisions. Microsoft also cautions that the helper may
change and points independent certificate validation toward other APIs.

Git for Windows continues to release new versions beyond the installation
observed by M227. Persisting or allowlisting one locally observed chain would
therefore create an unapproved rotation, expiry, revocation, and recovery
policy. SLSA source provenance remains an SCS-issued statement about a source
revision, not a property conferred by the certificate chain on a local Git
executable.

## Decision

Bind the complete ordered WinTrust provider-certificate sequence around the
complete M227 boundary in one Windows-only test composition. Repeat M227's
exact retained path/handle, no-UI, cache-only, explicit no-revocation trust
request. While each successful provider state remains live:

- require provider data and the primary non-countersigner;
- require the existing positive bounded provider-chain count;
- retrieve every provider certificate by exact zero-based provider index;
- require positive per-certificate DER size and a bounded aggregate DER size;
- copy every DER value before provider state closes;
- compute a per-certificate SHA-256 and one domain-separated aggregate SHA-256
  over chain count plus each index, DER length, and DER value; and
- retain the provider's nonzero raw `sftVerifyAsOf` FILETIME value.

Close provider state in a `finally` boundary after success, trust rejection,
or extraction failure. Require the exact provider count, size tuple,
per-certificate digest tuple, aggregate digest, and verification-time value
before and after M227's complete boundary.

The ordering is only the provider-index sequence observed during one
execution. Do not label indexes as leaf, intermediate, or root, infer issuer
semantics, persist the chain identity, or compare it with a repository
allowlist. This decision does not establish signer or publisher authorization,
certificate validation policy, rotation/recovery, timestamp or countersigner
authenticity, revocation freshness, trust-store authority, native DLL/loader
identity, repository acquisition, local-object-store trust, or source/build
provenance. It does not admit Windows or authorize cleanup.

## Consequences

- Every certificate in the bounded live provider sequence must be available
  and detached before state close.
- A changed count, order, DER length, DER value, aggregate digest, or raw
  verification time fails the M228 composition.
- M221 through M227 evidence remains byte-for-byte unchanged.
- No runtime, package, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, or admission surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Infer issuer order and authorize the terminal certificate

Rejected because the provider exposes an indexed sequence, while portable
issuer semantics and authorization require an explicit validation and trust-
store policy outside this observation.

### Persist the complete chain as an allowlist

Rejected because the chain is rotation-sensitive current-host evidence. A
durable allowlist requires explicit authority, update, expiry, revocation,
recovery, and compatibility decisions.

### Replace WinTrust with independent chain validation

Rejected because M228 is a narrow extension of the successful provider-state
observation. A separate validation policy would be a different authority and
does not follow from M227.

### Treat the chain as source provenance

Rejected because authenticating a local executable is distinct from proving
how a repository revision was acquired, reviewed, or produced.

## Primary references

- [Microsoft: `CRYPT_PROVIDER_SGNR`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_sgnr)
- [Microsoft: `CRYPT_PROVIDER_CERT`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_cert)
- [Microsoft: `WTHelperGetProvCertFromChain`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovcertfromchain)
- [Microsoft: `WTHelperProvDataFromStateData`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelperprovdatafromstatedata)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
