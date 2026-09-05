# Windows contained source-access source-commit Git signer-certificate binding probe

**Status:** Accepted M227 current-repository test evidence; signer policy,
revocation freshness, timestamp/countersigner authentication, source/build
provenance, cross-principal proof, independent-host proof, cleanup authority,
and Windows admission have not occurred.

M227 composes a Windows-only, test-only primary signer-certificate observation
around M226's complete retained-handle Authenticode boundary. It performs no
cache-fixture operation and issues no cleanup.

## Live WinTrust provider state

The probe repeats M226's exact retained path and readable handle with no user
interface, cache-only URL retrieval, and explicit no-revocation policy. After
successful `WINTRUST_ACTION_GENERIC_VERIFY_V2` evaluation and before state
close, it resolves the live WinTrust provider state, primary signer, and first
provider certificate.

The signer must report a positive bounded certificate-chain length. Its first
certificate context must expose positive bounded DER bytes. Those bytes are
copied while provider state is live and hashed with SHA-256 after detachment.
The probe also records the provider's nonzero raw verification time; Windows
documents this as the current time or timestamp, so this field is not treated
as independent timestamp or countersigner proof.

Every observation closes provider state through `WTD_STATEACTION_CLOSE` in a
`finally` boundary. Missing state, signer, chain, certificate, DER bytes, or
verification time fails closed and still closes provider state. A close
failure is reported when extraction otherwise succeeds.

The detached certificate size, DER hash, and verification time must match
before and after the complete M226 boundary. M226 in turn requires its two
cached trust decisions around all 48 M225 child-image bindings and the full
retained source-commit settlement.

## Evidence and authority boundary

This binds one primary signer certificate observation to the exact retained
Git file and live successful trust state. It does not authorize a signer or
publisher and does not persist the observed certificate identity in project
policy, fixtures, documentation, or output.

The DER hash is compared only within one execution. It is not a certificate
pin, publisher allowlist, rotation policy, revocation decision, or future-file
authorization. Revocation freshness remains unproved. Certificate expiry,
timestamp validation, countersigner identity, key custody, trust-store/cache
administration, and recovery remain separate authority decisions.

Native DLL and loader identity remain outside. The local Git object store and
repository acquisition remain outside the trust boundary. This is not source
or build provenance, an attestation, or an independent rebuild.

Distinct-principal behavior, hostile or privileged bypass, independent-host
evidence, debugger/kernel resistance, and criteria 6 and 7 remain unresolved.
Windows is not admitted, and cleanup remains unimplemented and unauthorized.

M227 adds no runtime source, public API, CLI or MCP command, production
harness, collector, credential lifecycle, filesystem mutation, network
listener, dependency, package payload, version, workflow, permission, secret,
hosted allocation, cleanup action, or admission decision.

## Primary references

- [Microsoft: `WTHelperProvDataFromStateData`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelperprovdatafromstatedata)
- [Microsoft: `WTHelperGetProvSignerFromChain`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovsignerfromchain)
- [Microsoft: `WTHelperGetProvCertFromChain`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovcertfromchain)
- [Microsoft: `CRYPT_PROVIDER_SGNR`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_sgnr)
- [Microsoft: `CRYPT_PROVIDER_CERT`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_cert)
- [Microsoft: `CERT_CONTEXT`](https://learn.microsoft.com/en-us/windows/win32/api/wincrypt/ns-wincrypt-cert_context)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
- [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final)
