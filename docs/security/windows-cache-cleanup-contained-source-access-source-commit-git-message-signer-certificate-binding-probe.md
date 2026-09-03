# Windows contained source-access source-commit Git message-signer certificate binding probe

**Status:** Accepted M231 current-repository test evidence; publisher policy,
certificate pinning, revocation freshness, provenance, Windows admission, and
cleanup authority remain unresolved.

## Boundary

M231 composes one Windows-only, test-only certificate-correlation observation
around the complete M230 boundary. It repeats the exact retained Git path and
handle plus M230's no-UI, cache-only, explicit-no-revocation
`WINTRUST_ACTION_GENERIC_VERIFY_V2` request. No network retrieval is enabled.

While each successful provider state remains live, the probe requires a
compatible provider prefix, a non-null cryptographic-message handle, a positive
bounded signer count, and a bounded provider-store count. The message and
provider signer counts must agree. A positive store count requires the live
provider store array.

For every exact message signer index, `CryptMsgGetAndVerifySigner` runs with
`CMSG_USE_SIGNER_INDEX_FLAG` and without `CMSG_TRUSTED_SIGNER_FLAG`. The call
must verify the message signature, return the same index, and return a non-null
certificate context. Its positive bounded DER bytes are copied before the
context is released.

The same provider state resolves the primary provider certificate for that
exact index. The message and provider certificate bytes must be exactly equal.
The detached observation retains the provider-store and signer counts, exact
certificate-size tuple, message and provider SHA-256 tuples, and one
domain-separated aggregate over every index, length, and both byte sequences.
The complete observation must match before and after the complete M230 boundary.

Every returned certificate context is released even when verification reports
failure after returning a context. Provider state closes in `finally` after
success, trust rejection, missing or malformed provider data, count/store
failure, message verification failure, changed index, invalid certificate,
provider lookup failure, byte mismatch, context-release failure, or another
correlation failure. A primary correlation failure is preserved if release also
fails; a release or state-close failure is reported after otherwise successful
extraction.

## What this proves

- The current host can verify every bounded exact signed-message signer index.
- The certificate returned by message verification has the same detached DER
  bytes as the primary provider certificate at that index.
- Counts, order, boundaries, bytes, and hashes remain stable across M230's
  complete retained-file interval.
- Returned certificate contexts and provider state close on every exercised
  outcome.

## What this does not prove

The observation does not authorize a signer or publisher. It defines no
certificate allowlist, persisted identity, pin, expiry, rotation, recovery, or
publisher-name policy. It does not make the provider stores independently
trusted and does not administer the Windows trust store.

It does not establish revocation freshness, portable certificate-chain or
timestamp semantics, timestamp-authority authorization, independent timestamp-
token validation, or signing-time authenticity. Cached WinTrust success remains
the only trust-policy observation.

It is not source or build provenance, repository-acquisition evidence, local-
object-store trust, native DLL/loader identity, distinct-principal or
independent-host proof, or a hostile/privileged bypass claim. Criteria 6 and 7
remain unresolved.

Windows is not admitted. Cleanup remains unimplemented and unauthorized. M231
adds no runtime source, public API, CLI or MCP command, production collector,
filesystem mutation, dependency, lock change, fixture, example, script,
benchmark, workflow, permission, public runner, or hosted allocation.

## Primary references

- [Microsoft: `CryptMsgGetAndVerifySigner`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetandverifysigner)
- [Microsoft: `CERT_CONTEXT`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_context)
- [Microsoft: `CertFreeCertificateContext`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-certfreecertificatecontext)
- [Microsoft: `CRYPT_PROVIDER_DATA`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_data)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
