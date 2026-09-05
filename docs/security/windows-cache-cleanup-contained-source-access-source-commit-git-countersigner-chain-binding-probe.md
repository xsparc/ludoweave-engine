# Windows contained source-access source-commit Git countersigner-chain binding probe

**Status:** Accepted M229 current-repository test evidence; portable timestamp
semantics, timestamp-authority policy, signer policy, revocation freshness,
provenance, Windows admission, and cleanup authority remain unresolved.

## Boundary

M229 composes a Windows-only, test-only complete indexed countersigner sequence
around M228. It repeats the exact retained Git path/handle and M228's no-UI,
cache-only, explicit-no-revocation `WINTRUST_ACTION_GENERIC_VERIFY_V2` request.
No network retrieval is enabled.

While each successful provider state is live, the probe requires provider data
and the primary signer. It reads the positive bounded `csCounterSigners` count
and retrieves every countersigner with
`WTHelperGetProvSignerFromChain(provider_data, 0, TRUE, index)`. The index is an
execution-local provider index, not a portable timestamp-authority ordering.

Every countersigner must expose zero provider error, a nonzero raw
`sftVerifyAsOf` FILETIME, and a positive bounded provider-certificate count. The
probe retrieves each certificate by its countersigner provider-chain order,
copies positive bounded DER bytes before state close, and enforces both per-chain
and bounded aggregate DER bytes across the complete countersigner sequence.

The detached observation retains countersigner count, raw signer type, provider
error, verification time, chain count, DER-size tuple, per-certificate hashes,
per-chain hash, and one domain-separated aggregate over every exact index,
length, metadata field, and DER value. The complete observation must match
before and after the complete M228 boundary.

Provider state closes in `finally` after success, trust rejection, missing
state, missing primary signer, missing indexed countersigner, provider error,
invalid verification time, invalid chain, certificate extraction failure, DER
rejection, or aggregate-bound rejection. A close failure is reported when
extraction otherwise succeeds.

## What this proves

- The current host exposes one complete bounded provider-index countersigner
  sequence for the retained Git executable.
- Every bounded countersigner certificate is detached while provider state is
  live.
- Count, order, raw metadata, certificate boundaries, values, and hashes remain
  stable across M228's complete test boundary.
- Provider state closes after every exercised outcome.

## What this does not prove

This evidence does not establish portable timestamp semantics and does not
authorize a signer, publisher, or timestamp authority. It does not persist the
observed countersigner identity or create a certificate allowlist, pin,
rotation, expiry, revocation, or recovery policy.

Raw signer type and FILETIME values are bound as provider metadata. The probe
does not independently parse an RFC 3161 token, validate a PKCS #7 signing-time
attribute, establish a trusted time source, or prove that one timestamp policy
is portable across Windows versions or trust stores. Revocation freshness
remains unproved.

It is not source or build provenance, repository-acquisition evidence,
local-object-store trust, native DLL/loader identity, trust-store authority,
distinct-principal or independent-host proof, or a hostile/privileged bypass
claim. Criteria 6 and 7 remain unresolved.

Windows is not admitted. Cleanup remains unimplemented and unauthorized. M229
adds no runtime source, public API, CLI or MCP command, production collector,
filesystem mutation, dependency, lock change, fixture, example, script,
benchmark, workflow, permission, public runner, or hosted allocation.

## Primary references

- [Microsoft: `CRYPT_PROVIDER_SGNR`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_sgnr)
- [Microsoft: `WTHelperGetProvSignerFromChain`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovsignerfromchain)
- [Microsoft: `WTHelperGetProvCertFromChain`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovcertfromchain)
- [Microsoft: time stamping Authenticode signatures](https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
