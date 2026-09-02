# Windows contained source-access source-commit Git executable file retention probe

**Status:** Accepted M224 current-repository test evidence; executable
authenticity, source/build provenance, cross-principal proof, independent-host
proof, cleanup authority, and Windows admission have not occurred.

M224 composes a Windows-only, test-only retained-file boundary around M223's
complete Git-selection observation. It performs no cache-fixture operation and
issues no cleanup.

## Git executable file retention

The probe performs exactly one real `PATH`/`PATHEXT` lookup and requires the
result to be an existing absolute canonical file. It then opens one
non-inheritable read-only handle with `FILE_SHARE_READ` as the only share mode.
Windows keeps those share constraints effective until the handle closes.

The retained file snapshot includes its normalized path, volume serial, file
identifier, positive bounded byte count, and SHA-256 digest. The same handle
must produce an identical snapshot after all 48 fixed Git object reads in the
complete M223/M222/M221 three-participant boundary.

The identical retainer is also opened on its own writable test source.
Access-only competing opens must show that write and delete/rename access is
refused with the exact sharing-violation category. Those checks neither write
nor delete the proof file. After the retained handle closes, both access
categories must settle and a fresh read snapshot must equal the retained
snapshot. The separate proof file avoids confusing host ACL denial on an
installed Git executable with the retainer's share-mode effect.

M223's existing scoped selector and subprocess observer remain mandatory. All
48 direct child commands still begin with the selected absolute path. M222's
no-lazy-fetch, no-replacement-object, sanitized-environment, no-shell,
no-input, timeout, bounded-output, and empty-standard-error rules remain in
force. The full M220 retained-source, image, Job, token, access, settlement,
and participant boundary also remains mandatory.

## Evidence and authority boundary

This is Git executable file retention only. It does not authenticate the
executable, a signer, publisher, origin, ACL, or security descriptor. It does
not prove that the created process image or every executed byte came from the
retained handle. Native DLL and loader identity remain outside, and the local
object store remains outside the trust boundary.

This is not a source provenance attestation, and build provenance remains
unproved. Repository acquisition, imported modules, distinct-principal
behavior, hostile or privileged bypass, independent-host evidence, and
debugger/kernel resistance remain unbound. Criteria 6 and 7 remain unresolved.
Windows is not admitted, cleanup remains unimplemented and unauthorized, and
no public self-hosted runner is introduced.

M224 adds no runtime source, public API, CLI or MCP command, production
harness, collector, credential lifecycle, filesystem mutation, network
listener, dependency, package payload, version, workflow, permission, secret,
hosted allocation, cleanup action, or admission decision.

## Primary references

- [CreateFileW share modes](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [GetFileInformationByHandleEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfileinformationbyhandleex)
- [FILE_ID_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [GetFileSizeEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfilesizeex)
- [ReadFile](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfile)
- [Python subprocess reliability](https://docs.python.org/3/library/subprocess.html)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
- [GitHub artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)
- [NIST SSDF publications](https://csrc.nist.gov/Projects/ssdf/publications)
