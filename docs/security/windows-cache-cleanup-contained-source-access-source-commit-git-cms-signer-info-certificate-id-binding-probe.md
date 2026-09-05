# Windows contained source-access source-commit Git CMS SignerInfo certificate-ID binding probe

**Status:** Accepted M234 current-repository test evidence; signer and publisher
authorization, alternate CMS representation support, certificate pinning,
revocation freshness, provenance, Windows admission, and cleanup authority
remain unresolved.

## Boundary

M234 composes one Windows-only, test-only CMS SignerInfo SignerId observation
around the complete M233 boundary. It repeats the exact retained Git path and
handle plus M233's no-UI, cache-only, explicit-no-revocation
`WINTRUST_ACTION_GENERIC_VERIFY_V2` request. No network retrieval is enabled.

M233 first verifies the complete bounded message/verified/provider certificate
correlation and explicit certificate-ID choice and payload. While that same
successful provider state remains live, M234 reacquires the non-null message
handle and the same positive bounded signer count.

For every exact message signer index, a bounded two-phase
`CMSG_CMS_SIGNER_INFO_PARAM` read returns a `CMSG_CMS_SIGNER_INFO`. The probe
reads only the aligned `dwVersion` and `SignerId` prefix, then validates the
version and certificate-ID choice before inspecting pointer-bearing union
data. This current-host profile accepts only signer-info version 1 with
`CERT_ID_ISSUER_SERIAL_NUMBER`; version 3, key-ID, SHA-1 hash-ID, unknown,
malformed, empty, oversized, or unavailable values refuse.

The issuer and serial-number bytes are copied while the owning native buffer
remains alive. They must exactly equal a second same-state, same-index dedicated
M233 certificate-ID read and M233's already-detached observation.

The detached observation retains the CMS version, explicit choice, exact
component lengths, a domain-separated per-index hash, and one domain-separated
aggregate over the signer count plus every index, version, choice, length, and
byte sequence. It also retains M233's complete detached observation. The whole
result must match before and after complete M233.

Provider state closes through M233's inherited `finally` discipline after
success, trust rejection, malformed data, extraction or comparison failure,
context-release failure, or another observed outcome. M233 releases every
returned certificate context before M234 reads the CMS SignerInfo.

## What this proves

- The current host exposes signer-info version 1 with an issuer/serial
  `SignerId` for every bounded exact Git message signer index.
- Each CMS version and explicit certificate-ID choice is validated before its
  union member is read.
- The copied CMS SignerInfo SignerId payload exactly equals the same-index
  dedicated M233 certificate ID and M233 detached observation.
- Counts, order, version, choice, component boundaries, bytes, and hashes remain
  stable across M233's complete retained-file interval.
- Pointer-bearing message data is detached before its native buffer expires,
  and provider state closes on every exercised outcome.

## What this does not prove

The observation does not authorize a signer or publisher. It defines no
certificate allowlist, persisted identity, pin, expiry, rotation, recovery, or
publisher-name policy. It deliberately does not support or correlate the valid
version 3, key-ID, or SHA-1 hash-ID representations and is not a general CMS or
certificate-identity service.

It does not inspect or bind hash/signature algorithms, the encrypted hash,
authenticated or unauthenticated attributes, or countersignatures. It does not
revalidate the signature. It does not establish revocation freshness, portable certificate-
chain or timestamp semantics, timestamp-authority authorization, independent
timestamp-token validation, signing-time authenticity, or Windows trust-store
administration. Cached WinTrust success remains the only trust-policy
observation.

It is not source or build provenance, repository-acquisition evidence, local-
object-store trust, native DLL/loader identity, distinct-principal or
independent-host proof, or a hostile/privileged bypass claim. Criteria 6 and 7
remain unresolved.

Windows is not admitted. Cleanup remains unimplemented and unauthorized. M234
adds no runtime source, public API, CLI or MCP command, production collector,
filesystem mutation, dependency, lock change, fixture, example, script,
benchmark, workflow, permission, public runner, or hosted allocation.

## Primary references

- [Microsoft: `CMSG_CMS_SIGNER_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cmsg_cms_signer_info)
- [Microsoft: `CryptMsgGetParam`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetparam)
- [Microsoft: `CERT_ID`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_id)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
