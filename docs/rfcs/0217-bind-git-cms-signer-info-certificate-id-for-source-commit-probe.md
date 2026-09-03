# RFC-0217: Bind the CMS SignerInfo certificate ID

**Status:** Accepted
**Milestone:** M234
**Decision class:** Direction-preserving

## Context

M233 correlates the explicit `CERT_ID` returned by
`CMSG_SIGNER_CERT_ID_PARAM` with the legacy message selector and the verified
certificate for every exact signer index. That dedicated parameter does not
prove that the separately decoded CMS signer record carries the same signer
identifier.

Microsoft documents `CMSG_CMS_SIGNER_INFO_PARAM` as returning a
`CMSG_CMS_SIGNER_INFO` for an exact signer index. The structure begins with a
version and a `CERT_ID SignerId`, followed by algorithm, encrypted-hash, and
attribute fields. Its pointer-bearing identifier must be copied while the
returned native buffer remains alive. The installed Windows SDK defines the
parameter as 39 and signer-info versions 1 and 3.

The current Git for Windows signature uses version 1 plus the issuer/serial
certificate-ID choice already admitted by M233's narrow compatibility probe.
A different version or identifier choice can be valid CMS, but accepting it
would require separately reviewed comparison and policy semantics. Reading
algorithm or attribute fields would likewise expand this slice beyond the
identity-representation gap.

Git for Windows signing material and CMS representation can legitimately
change between releases. SLSA source provenance remains an SCS-issued
statement about source-revision creation and change controls; local executable
CMS metadata is not source provenance.

## Decision

Bind the CMS SignerInfo certificate-ID version, choice, and payload for every
bounded exact signer index in one Windows-only, test-only composition around
complete M233.

Repeat M233's retained Git path/handle and no-UI, cache-only,
explicit-no-revocation `WINTRUST_ACTION_GENERIC_VERIFY_V2` request. While each
successful provider state remains live:

- execute M233's complete message/verified/provider and explicit-certificate-ID
  correlation first;
- reacquire the same live provider message and exact bounded signer count;
- retrieve `CMSG_CMS_SIGNER_INFO_PARAM` for every exact signer index through a
  bounded two-phase read;
- read only the aligned prefix containing `dwVersion` and `SignerId`;
- require signer-info version 1 and inspect `SignerId.dwIdChoice` before reading
  its union;
- require `CERT_ID_ISSUER_SERIAL_NUMBER` and refuse version 3, key-ID, hash-ID,
  unknown, malformed, or unavailable forms in this current-host profile;
- copy positive bounded issuer and serial-number blobs while the owning native
  buffer remains alive;
- require exact equality with a same-state, same-index dedicated M233
  certificate-ID read and M233's detached observation;
- retain the version, choice, component lengths, a domain-separated per-index
  hash, and one count/index/version/choice/length/value sequence digest; and
- require the complete detached observation before and after M233's complete
  boundary.

Close provider state through M233's inherited `finally` discipline after every
outcome. Returned certificate contexts remain governed by M233 and are freed
before this extension runs.

This does not create signer or publisher authorization. It defines no
allowlist, persisted identity, certificate pin, expiry, rotation, recovery, or
publisher-name rule. It does not claim general support for version 3, key-ID,
or hash-ID signer forms. It does not inspect or bind the hash algorithm,
signature algorithm, encrypted hash, authenticated attributes, or
unauthenticated attributes. It does not revalidate the signature, establish
revocation freshness, portable chain or timestamp semantics, trust-store
administration, native DLL/loader identity, local object-store trust,
repository-acquisition evidence, or source/build provenance. It does not admit
Windows or authorize cleanup.

## Consequences

- The decoded CMS signer identifier is correlated with the complete M233
  evidence chain instead of inferred from a separate API result.
- A valid but different CMS version or identifier choice refuses this narrow
  current-host probe until a later decision defines its semantics.
- Pointer-bearing `SignerId` data is copied before its native buffer leaves
  scope.
- M221 through M233 evidence remains byte-for-byte unchanged.
- No runtime, package, API, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, admission, or hosted surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Infer CMS `SignerId` from M233

Rejected because M233 reads a different parameter and cannot prove the CMS
structure version, identifier discriminant, union payload, or index was
marshalled correctly.

### Parse the entire CMS signer-info structure

Rejected because algorithm and attribute interpretation adds unrelated policy,
encoding, and validation obligations. The minimal aligned prefix closes the
identified representation gap.

### Accept every version and `CERT_ID` choice

Rejected because successful parsing alone would not bind alternate identifiers
to the verified certificate. Silent fallback would weaken the fail-closed
boundary.

### Add the live probe to hosted CI

Rejected because no public self-hosted Windows runner is authorized, and the
existing local Windows capability is sufficient for this compatibility
observation.

## Primary references

- [Microsoft: `CMSG_CMS_SIGNER_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cmsg_cms_signer_info)
- [Microsoft: `CryptMsgGetParam`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/nf-wincrypt-cryptmsggetparam)
- [Microsoft: `CERT_ID`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_id)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
