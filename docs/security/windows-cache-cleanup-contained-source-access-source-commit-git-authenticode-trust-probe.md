# Windows contained source-access source-commit Git Authenticode trust probe

**Status:** Accepted M226 current-repository test evidence; signer policy,
revocation freshness, source/build provenance, cross-principal proof,
independent-host proof, cleanup authority, and Windows admission have not
occurred.

M226 composes a Windows-only, test-only retained-handle Authenticode trust
observation around M225's complete Git child-image binding. It performs no
cache-fixture operation and issues no cleanup.

## Retained-handle Authenticode trust

The probe performs one real Git lookup and keeps the resulting canonical file
open through M224's non-inheritable read handle. A `WINTRUST_FILE_INFO` passes
both that canonical path and the same readable handle to
`WINTRUST_ACTION_GENERIC_VERIFY_V2`.

Trust evaluation has no user interface and uses cache-only URL retrieval. It
sets no additional revocation checking and explicitly suppresses provider
revocation checks, so verification cannot consult the network. Exact success
therefore shows only that the file satisfies the current host's cached Windows
generic Authenticode policy; revocation freshness remains unproved.

Each call enters `WTD_STATEACTION_VERIFY` and explicitly closes provider state
with `WTD_STATEACTION_CLOSE` in a `finally` boundary. Rejected trust still
closes provider state. A close failure is reported when verification otherwise
succeeds.

The retained file must verify before and after the complete M225 boundary.
Between those checks, M225 creates all 48 fixed Git children suspended, binds
each actual process image to the retained executable before code runs, and
requires complete M223/M222/M221 settlement. M226 also rechecks the retained
file snapshot before its second trust verification.

## Evidence and authority boundary

This is a local Windows trust-policy observation for the exact retained file.
It does not allowlist a signer or publisher, pin a certificate, establish key
custody or rotation, prove current online revocation status, or authorize a
future executable. Host trust-store and cache administration remain outside.

Native DLL and loader identity remain outside. The local Git object store and
repository acquisition remain outside the trust boundary. This is not source
or build provenance, an attestation, or an independent rebuild.

Distinct-principal behavior, hostile or privileged bypass, independent-host
evidence, debugger/kernel resistance, and criteria 6 and 7 remain unresolved.
Windows is not admitted, and cleanup remains unimplemented and unauthorized.

M226 adds no runtime source, public API, CLI or MCP command, production
harness, collector, credential lifecycle, filesystem mutation, network
listener, dependency, package payload, version, workflow, permission, secret,
hosted allocation, cleanup action, or admission decision.

## Primary references

- [Microsoft: `WinVerifyTrust`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/nf-wintrust-winverifytrust)
- [Microsoft: `WINTRUST_FILE_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-wintrust_file_info)
- [Microsoft: `WINTRUST_DATA`](https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-wintrust_data)
- [Microsoft: verifying a PE signature](https://learn.microsoft.com/en-us/windows/win32/seccrypto/example-c-program--verifying-the-signature-of-a-pe-file)
- [Microsoft: `Get-AuthenticodeSignature`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-authenticodesignature)
- [Git for Windows: MinGit](https://gitforwindows.org/mingit.html)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
- [NIST SSDF publications](https://csrc.nist.gov/Projects/ssdf/publications)
