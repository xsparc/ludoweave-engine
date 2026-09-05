# RFC-0210: Bind retained Git Authenticode signer certificate

**Status:** Accepted
**Milestone:** M227
**Decision class:** Direction-preserving

## Context

M226 proves that the exact retained Git executable satisfies the current
host's cached Windows Authenticode policy before and after M225. It does not
inspect which certificate the successful provider state associated with the
primary signer.

Windows exposes live trust-provider state through
`WTHelperProvDataFromStateData`. The corresponding primary signer and first
provider certificate can be obtained through
`WTHelperGetProvSignerFromChain` and `WTHelperGetProvCertFromChain`. The
certificate context contains bounded encoded DER bytes that can be copied
before provider state closes.

The current Git installation is accepted by Windows even though its observed
leaf certificate is past its ordinary validity end, consistent with a
timestamped signature. A fixed leaf thumbprint or subject therefore would be a
rotation-sensitive authorization policy, not a direction-neutral observation.
No stable upstream signer-rotation contract was found for that policy.

## Decision

Bind retained Git Authenticode signer certificate evidence around the complete
M226 boundary in one Windows-only test composition. Repeat M226's exact
retained path/handle, no-UI, cache-only, explicit no-revocation verification.
While the successful provider state remains live:

- require provider data and the primary non-countersigner;
- require a positive bounded signer certificate-chain length;
- require the first provider certificate and a positive bounded DER length;
- copy the DER bytes before provider state closes;
- compute SHA-256 over the detached copy; and
- retain the provider's nonzero raw `sftVerifyAsOf` FILETIME value.

Close provider state in a `finally` boundary after success, trust rejection,
or extraction failure. Require the exact detached certificate size, DER hash,
and verification-time observation before and after M226's complete boundary.

Do not persist the host's observed certificate identity or compare it with a
repository allowlist. This decision does not establish signer or publisher
authorization, certificate rotation or recovery policy, timestamp or
countersigner authenticity, or revocation freshness. It does not bind native
DLLs or loader state, authenticate repository acquisition or the local object
store, establish source/build provenance, admit Windows, or authorize cleanup.

## Consequences

- Every accepted local trust result used by this composition must expose one
  bounded primary signer certificate while provider state is live.
- The detached certificate observation must remain exact across all inherited
  M226/M225 source-commit and child-image checks.
- M221 through M226 evidence remains byte-for-byte unchanged.
- No runtime, package, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, or admission surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Pin the observed leaf certificate thumbprint

Rejected because the observed leaf is rotation-sensitive and already outside
its ordinary validity interval. A pin requires an explicit authority,
rotation, expiry, revocation, and recovery policy that this test cannot infer.

### Allowlist the certificate subject string

Rejected because a display name is not a cryptographic identity and no
authoritative upstream policy commits future Git for Windows releases to one
unchanging subject.

### Export the observation as project policy

Rejected because current-host diagnostics do not authorize a future signer.
The hash stays inside one test execution and is compared only across its
retained-file interval.

## Primary references

- [Microsoft: `WTHelperProvDataFromStateData`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelperprovdatafromstatedata)
- [Microsoft: `WTHelperGetProvSignerFromChain`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovsignerfromchain)
- [Microsoft: `WTHelperGetProvCertFromChain`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovcertfromchain)
- [Microsoft: `CRYPT_PROVIDER_SGNR`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_sgnr)
- [Microsoft: `CRYPT_PROVIDER_CERT`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_cert)
- [Microsoft: `CERT_CONTEXT`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_context)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
- [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final)
