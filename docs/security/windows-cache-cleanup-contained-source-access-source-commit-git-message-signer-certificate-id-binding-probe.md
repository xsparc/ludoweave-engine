# Windows contained source-access source-commit Git message-signer certificate-ID binding probe

**Status:** Accepted M233 current-repository test evidence; signer and publisher
authorization, alternate certificate-ID support, certificate pinning,
revocation freshness, provenance, Windows admission, and cleanup authority
remain unresolved.

## Boundary

M233 composes one Windows-only, test-only certificate-ID observation around the
complete M232 boundary. It repeats the exact retained Git path and handle plus
M232's no-UI, cache-only, explicit-no-revocation
`WINTRUST_ACTION_GENERIC_VERIFY_V2` request. No network retrieval is enabled.

M232 first verifies the complete bounded message/verified/provider certificate
and issuer/serial correlation. While that same successful provider state
remains live, M233 reacquires the non-null message handle and the same positive
bounded signer count.

For every exact message signer index, a bounded two-phase
`CMSG_SIGNER_CERT_ID_PARAM` read returns a `CERT_ID`. The probe validates the
explicit certificate-ID choice before inspecting its pointer-bearing union.
This current-host profile accepts only `CERT_ID_ISSUER_SERIAL_NUMBER`; key-ID,
SHA-1 hash-ID, unknown, malformed, empty, oversized, or unavailable values
refuse. The issuer and serial-number bytes are copied while the owning native
buffer remains alive and must exactly equal M232's same-index legacy message
certificate selector.

The detached observation retains the explicit choice, exact component lengths,
a domain-separated certificate-ID hash for every index, and one domain-
separated aggregate over the signer count plus every index, choice, length, and
byte sequence. It also retains M232's complete detached observation. The whole
result must match before and after complete M232.

Provider state closes through M232's existing `finally` discipline after
success, trust rejection, malformed data, extraction or comparison failure,
context-release failure, or another observed outcome. M232 releases every
returned certificate context before M233 reads the explicit certificate ID.

## What this proves

- The current host exposes an issuer/serial `CERT_ID` for every bounded exact
  Git message signer index.
- Each explicit choice is validated before its union member is read.
- The copied certificate-ID payload exactly equals the same-index M232 message
  selector.
- Counts, order, choice, component boundaries, bytes, and hashes remain stable
  across M232's complete retained-file interval.
- Pointer-bearing message data is detached before its native buffer expires,
  and provider state closes on every exercised outcome.

## What this does not prove

The observation does not authorize a signer or publisher. It defines no
certificate allowlist, persisted identity, pin, expiry, rotation, recovery, or
publisher-name policy. It deliberately does not support or correlate the valid
key-ID and SHA-1 hash-ID representations and is not a general certificate-
identity service.

It does not establish revocation freshness, portable certificate-chain or
timestamp semantics, timestamp-authority authorization, independent timestamp-
token validation, signing-time authenticity, or Windows trust-store
administration. Cached WinTrust success remains the only trust-policy
observation.

It is not source or build provenance, repository-acquisition evidence, local-
object-store trust, native DLL/loader identity, distinct-principal or
independent-host proof, or a hostile/privileged bypass claim. Criteria 6 and 7
remain unresolved.

Windows is not admitted. Cleanup remains unimplemented and unauthorized. M233
adds no runtime source, public API, CLI or MCP command, production collector,
filesystem mutation, dependency, lock change, fixture, example, script,
benchmark, workflow, permission, public runner, or hosted allocation.

## Primary references

- [Microsoft: `CryptMsgGetParam`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetparam)
- [Microsoft: `CERT_ID`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_id)
- [Microsoft: `CERT_ISSUER_SERIAL_NUMBER`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_issuer_serial_number)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
