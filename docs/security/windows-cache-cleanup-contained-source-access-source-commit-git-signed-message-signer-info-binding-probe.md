# Windows contained source-access source-commit Git signed-message SignerInfo binding probe

**Status:** Accepted M230 current-repository test evidence; SignerInfo parsing,
portable timestamp semantics, signer or timestamp-authority policy, revocation
freshness, provenance, Windows admission, and cleanup authority remain
unresolved.

## Boundary

M230 composes a Windows-only, test-only complete bounded encoded SignerInfo
sequence around M229. It repeats the exact retained Git path/handle and M229's
no-UI, cache-only, explicit-no-revocation
`WINTRUST_ACTION_GENERIC_VERIFY_V2` request. No network retrieval is enabled.

While each successful provider state is live, the probe requires a provider
structure large enough to contain the documented message prefix. It retains
the positive raw `dwEncoding`, requires a non-null `hMsg`, and requires a
positive bounded `csSigners` count. It uses two-phase CryptMsgGetParam queries
to retrieve `CMSG_SIGNER_COUNT_PARAM` and every `CMSG_ENCODED_SIGNER` by exact
zero-based message index.

The message count must occupy exactly one `DWORD`, remain within the shared
bound, and equal the provider count. Each size query must return a positive
bounded value. The exact-size read must succeed without changing that size.
Per-signer and complete-sequence limits are enforced before all bytes are
copied from provider-owned state.

The detached observation retains the raw encoding, provider and message signer
counts, encoded-size tuple, every encoded SignerInfo SHA-256, and one
domain-separated aggregate over both counts plus every exact index, length, and
value. The complete observation must match before and after the complete M229
boundary.

Provider state closes in `finally` after success, trust rejection, missing
state, missing or short provider data, invalid encoding, missing message,
invalid or inconsistent counts, size-query failure, invalid capacity, read
failure, or retrieval-size change. A close failure is reported when extraction
otherwise succeeds.

## What this proves

- The current host exposes one bounded live WinTrust message whose provider and
  message signer counts agree.
- Every encoded signer record is copied through an exact two-phase retrieval
  while provider state remains live.
- Raw encoding, counts, order, boundaries, values, and hashes remain stable
  across M229's complete test boundary.
- Provider state closes after every exercised outcome.

## What this does not prove

The probe does not parse SignerInfo. It treats every encoded value as opaque and
does not independently validate algorithms, issuer or serial fields,
authenticated or unauthenticated attributes, encrypted digests,
countersignatures, timestamp tokens, or signing times.

It does not establish portable timestamp semantics and does not authorize a
signer, publisher, or timestamp authority. It does not persist the observed
message or create an allowlist, identity, certificate pin, rotation, expiry,
revocation, or recovery policy. Revocation freshness and trust-store authority
remain unproved.

It is not source or build provenance, repository-acquisition evidence,
local-object-store trust, native DLL/loader identity, distinct-principal or
independent-host proof, or a hostile/privileged bypass claim. Criteria 6 and 7
remain unresolved.

Windows is not admitted. Cleanup remains unimplemented and unauthorized. M230
adds no runtime source, public API, CLI or MCP command, production collector,
filesystem mutation, dependency, lock change, fixture, example, script,
benchmark, workflow, permission, public runner, or hosted allocation.

## Primary references

- [Microsoft: `CRYPT_PROVIDER_DATA`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_data)
- [Microsoft: `CryptMsgGetParam`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetparam)
- [Microsoft: `CMSG_CMS_SIGNER_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cmsg_cms_signer_info)
- [Microsoft: time stamping Authenticode signatures](https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
