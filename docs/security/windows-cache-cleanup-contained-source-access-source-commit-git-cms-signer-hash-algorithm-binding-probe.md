# Windows contained source-access source-commit Git CMS signer hash-algorithm binding probe

**Status:** Accepted M235 current-repository test evidence; cryptographic
algorithm policy, signature revalidation, signer or publisher authorization,
revocation freshness, provenance, Windows admission, and cleanup authority
remain unresolved.

## Boundary

M235 composes one Windows-only, test-only hash-algorithm observation around the
complete M234 boundary. It repeats the exact retained Git path and handle plus
M234's no-UI, cache-only, explicit-no-revocation
`WINTRUST_ACTION_GENERIC_VERIFY_V2` request. No network retrieval is enabled.

M234 first verifies the complete bounded message, verified certificate,
provider certificate, explicit certificate ID, and decoded CMS SignerInfo
certificate-ID correlation. While that same successful provider state remains
live, M235 reacquires the non-null message handle and the same positive bounded
signer count.

For every exact message signer index, bounded two-phase reads retrieve both the
`HashAlgorithm` inside `CMSG_CMS_SIGNER_INFO_PARAM` and the dedicated
`CMSG_SIGNER_HASH_ALGORITHM_PARAM`. Each representation is a
`CRYPT_ALGORITHM_IDENTIFIER`: a pointer to a textual OID plus an opaque encoded
parameter blob.

The CMS HashAlgorithm value is treated as evidence, not as an authorization
decision.

The probe accepts a representation only when the OID pointer lies inside its
actual returned owner buffer, a non-empty bounded ASCII dotted-decimal OID is
NUL-terminated inside that buffer, and any positive bounded parameter range is
also wholly contained there. It copies the OID and parameter bytes before the
owner buffer expires. Query failures, read failures, invalid or changed sizes,
escaped pointers, absent termination, malformed OIDs, oversized parameters,
and cross-representation differences refuse.

The two detached values must be exactly equal at the same signer index. The
immutable result retains every OID, parameter size, domain-separated per-index
hash from both native representations, and one domain-separated aggregate over
the signer count, indexes, OIDs, and encoded parameters. The complete result
must match before and after complete M234.

Provider state closes through M234's inherited `finally` discipline after
success, trust rejection, malformed data, extraction or comparison failure,
context-release failure, or another observed outcome.

## What this proves

- The current host returns the same detached CMS `HashAlgorithm` OID and
  encoded parameters through both exact-index native representations.
- Both native results are size-bounded, pointer-confined, copied during owner
  lifetime, and detached before comparison or retention.
- Counts, order, indexes, OIDs, parameter boundaries, bytes, and hashes remain
  stable across M234's complete retained-file interval.
- Provider state closes on every exercised success and failure outcome.

## What this does not prove

The observation does not approve or reject an algorithm. It defines no
cryptographic algorithm allowlist, minimum strength, deprecation schedule,
parameter semantics, negotiation, agility, or upgrade policy. Equality of two
native representations is not evidence that the selected algorithm is secure
or suitable.

It does not revalidate the signature. It does not authorize a signer or
publisher, define a certificate allowlist or pin, establish revocation
freshness, portable certificate-chain or timestamp semantics, timestamp-
authority authorization, independent timestamp-token validation, or Windows
trust-store administration. Cached WinTrust success remains the only trust-
policy observation.

It is not source or build provenance, repository-acquisition evidence, local-
object-store trust, native DLL/loader identity, distinct-principal or
independent-host proof, or a hostile/privileged bypass claim. Criteria 6 and 7
remain unresolved.

Windows is not admitted. Cleanup remains unimplemented and unauthorized. M235
adds no runtime source, public API, CLI or MCP command, production collector,
filesystem mutation, dependency, lock change, fixture, example, script,
benchmark, workflow, permission, public runner, or hosted allocation.

## Primary references

- [Microsoft: `CMSG_CMS_SIGNER_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cmsg_cms_signer_info)
- [Microsoft: `CRYPT_ALGORITHM_IDENTIFIER`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-crypt_algorithm_identifier)
- [Microsoft: `CryptMsgGetParam`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetparam)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
