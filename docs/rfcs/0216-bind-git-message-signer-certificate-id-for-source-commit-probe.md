# RFC-0216: Bind the explicit Git message signer certificate ID

**Status:** Accepted
**Milestone:** M233
**Decision class:** Direction-preserving

## Context

M232 correlates the issuer and serial-number selector returned by
`CMSG_SIGNER_CERT_INFO_PARAM` with the exact verified message certificate and
same-index provider certificate. That legacy parameter does not expose which
identifier representation the signed message selected.

Microsoft documents `CMSG_SIGNER_CERT_ID_PARAM` as returning a `CERT_ID` that
identifies the signer's public key. Its `dwIdChoice` discriminant selects
exactly one union member: issuer and serial number, key identifier, or SHA-1
certificate hash. The installed Windows SDK defines the parameter as 38 and
the three choices as 1, 2, and 3.

An implementation that reads union storage without first validating the
discriminant can misinterpret pointer-bearing native data. A current-host
compatibility probe can instead require the issuer/serial choice and compare
its copied payload with M232's already correlated selector. Other choices are
valid Windows representations, but supporting and correlating them requires a
separate reviewed policy and evidence slice.

Git for Windows signing material and identifier form can legitimately change
between releases. SLSA source provenance remains an SCS-issued statement about
the creation and change controls of a source revision; local executable
certificate correlation is not source provenance.

## Decision

Bind the explicit message signer certificate-ID choice and payload for every
bounded exact signer index in one Windows-only, test-only composition around
complete M232.

Repeat M232's retained Git path/handle and no-UI, cache-only, explicit-no-
revocation `WINTRUST_ACTION_GENERIC_VERIFY_V2` request. While each successful
provider state remains live:

- execute M232's complete message/verified/provider certificate-identifier
  correlation first;
- reacquire the same live provider message and exact bounded signer count;
- retrieve `CMSG_SIGNER_CERT_ID_PARAM` for every exact signer index through a
  bounded two-phase read;
- inspect `dwIdChoice` before reading any union member;
- require `CERT_ID_ISSUER_SERIAL_NUMBER` for this current-host profile and
  refuse key-ID, hash-ID, unknown, malformed, or unavailable choices;
- copy the positive bounded issuer and serial-number blobs while the returned
  native buffer remains alive;
- require exact equality with the same-index M232 legacy message selector;
- retain the choice, component lengths, a domain-separated per-index hash, and
  one count/index/choice/length/value sequence digest; and
- require the complete detached observation before and after M232's complete
  boundary.

Close provider state through M232's existing `finally` discipline after every
outcome. Returned certificate contexts remain governed by M232 and are freed
before the certificate-ID extension runs.

This does not create signer or publisher authorization. It defines no
allowlist, persisted identity, certificate pin, expiry, rotation, recovery, or
publisher-name rule. It does not claim support for key-ID or hash-ID signer
forms. It does not establish revocation freshness, portable chain or timestamp
semantics, trust-store administration, native DLL/loader identity, local
object-store trust, repository-acquisition evidence, or source/build
provenance. It does not admit Windows or authorize cleanup.

## Consequences

- The explicit message identifier representation is bound to M232 instead of
  being inferred from equal certificate bytes or the legacy selector.
- A valid but different identifier choice refuses this narrow current-host
  probe until a later decision defines its comparison semantics.
- Pointer-bearing union data is copied before its native buffer leaves scope.
- M221 through M232 evidence remains byte-for-byte unchanged.
- No runtime, package, API, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, admission, or hosted surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Infer the choice from M232

Rejected because M232 observes a different API surface and cannot prove the
`CERT_ID` discriminant or union payload was correctly marshalled.

### Accept all `CERT_ID` choices without correlation

Rejected because successful parsing alone would not bind a key or hash
identifier to the verified certificate. Silent fallback would weaken the
fail-closed boundary.

### Persist the certificate ID as an allowlist

Rejected because persistence would create authorization, rotation, expiry,
recovery, and trust-distribution obligations outside this slice.

### Add the live probe to hosted CI

Rejected because no public self-hosted Windows runner is authorized, and the
existing local Windows capability is sufficient for this compatibility
observation.

## Primary references

- [Microsoft: `CryptMsgGetParam`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetparam)
- [Microsoft: `CERT_ID`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_id)
- [Microsoft: `CERT_ISSUER_SERIAL_NUMBER`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_issuer_serial_number)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
