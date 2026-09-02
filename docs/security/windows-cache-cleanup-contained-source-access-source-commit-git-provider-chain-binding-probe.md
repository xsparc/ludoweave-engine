# Windows contained source-access source-commit Git provider-chain binding probe

**Status:** Accepted M228 current-repository test evidence; portable chain
semantics, signer policy, revocation freshness, timestamp/countersigner
authentication, source/build provenance, cross-principal proof, independent-
host proof, cleanup authority, and Windows admission have not occurred.

M228 composes a Windows-only, test-only complete ordered provider-certificate
sequence observation around M227. It performs no cache-fixture operation and
issues no cleanup.

## Live ordered provider sequence

The probe repeats M227's exact retained path and readable handle with no user
interface, cache-only URL retrieval, and explicit no-revocation policy. After
successful `WINTRUST_ACTION_GENERIC_VERIFY_V2` evaluation and before state
close, it resolves live provider data, the primary signer, and every provider
certificate by zero-based provider index order.

The signer must report the existing positive bounded chain length. Each
provider certificate must expose positive bounded DER bytes, and the complete
sequence must stay within a separate bounded aggregate DER bytes limit. Every
DER value is copied while provider state is live. The probe computes each
certificate's SHA-256 plus one domain-separated aggregate SHA-256 over the
chain length and each exact index, length, and DER value. Length prefixes and
indexes make the aggregate encoding unambiguous.

The probe also records the provider's nonzero raw verification time. Every
observation closes provider state through `WTD_STATEACTION_CLOSE` in a
`finally` boundary. Missing state, signer, chain, indexed certificate, DER,
aggregate capacity, or verification time fails closed and still closes
provider state. A close failure is reported when extraction otherwise
succeeds.

The exact chain length, encoded-size tuple, per-certificate hash tuple,
aggregate chain hash, and verification time must match before and after the
complete M227 boundary. M227 in turn binds its primary signer certificate
around the complete M226 trust/source-commit/48-child boundary.

## Evidence and authority boundary

The ordering is the provider index order observed within one live trust state.
This evidence does not define portable chain semantics and does not infer that
an index is a leaf, intermediate, or root role on another provider or host.

The probe does not authorize a signer or publisher and does not persist the
observed chain identity in project policy, fixtures, documentation output, or
diagnostics. Its hashes compare only two observations within one execution.
They are not certificate pins, publisher allowlists, rotation policy, future-
file authority, or independent certificate validation.

Revocation freshness remains unproved. Certificate expiry, timestamp and
countersigner authenticity, key custody, provider confidence/error fields,
trust-store/cache administration, and recovery remain separate decisions.
Native DLL and loader identity remain outside. Repository acquisition and the
local Git object store remain outside the trust boundary. This is not source
or build provenance, an attestation, or an independent rebuild.

Distinct-principal behavior, hostile or privileged bypass, independent-host
evidence, debugger/kernel resistance, and criteria 6 and 7 remain unresolved.
Windows is not admitted, and cleanup remains unimplemented and unauthorized.

M228 adds no runtime source, public API, CLI or MCP command, production
harness, collector, credential lifecycle, filesystem mutation, network
listener, dependency, package payload, version, workflow, permission, secret,
hosted allocation, cleanup action, or admission decision.

## Primary references

- [Microsoft: `CRYPT_PROVIDER_SGNR`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_sgnr)
- [Microsoft: `CRYPT_PROVIDER_CERT`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-crypt_provider_cert)
- [Microsoft: `WTHelperGetProvCertFromChain`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelpergetprovcertfromchain)
- [Microsoft: `WTHelperProvDataFromStateData`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-wthelperprovdatafromstatedata)
- [Git for Windows](https://gitforwindows.org/)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
