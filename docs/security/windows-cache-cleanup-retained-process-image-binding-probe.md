# Windows retained process-image binding probe

**Status:** Accepted M214 current-host test evidence; no cross-principal or
independent-host collection has occurred.

M214 composes one current-host process-image observation with the exact frozen
M212/M213 control, process, and token boundary. The probe is Windows-only,
test-only, offline, and fixed-purpose. It neither issues a collection action
nor operates on a cache fixture. Criteria 6 and 7 remain unresolved, Windows
is not admitted, and cleanup remains unimplemented and unauthorized.

## Retained executable identity

Before participant launch, the controller opens the fixed direct
`pythonw.exe` through a retained expected-image handle with read-only access.
After M212 binds the connected pipe client to the retained participant process
and M213 binds its primary token and session, `QueryFullProcessImageNameW`
obtains the process image name from that same process handle. The controller
opens that observed image and retains its read-only file handle through the
challenge/ready barrier.

Each handle snapshot obtains `FILE_ID_INFO`, file size, and SHA-256 from the
same retained file object. Reads begin at offset zero, use fixed 64 KiB chunks,
and reject empty images or images larger than 64 MiB. File identity and size
are checked again after the bounded read. Private names are normalized through
their filesystem targets so a junction alias and its target compare as the
same file spelling.

The expected and observed normalized names, volume serials, 128-bit file IDs,
sizes, and digests must agree before the challenge. The expected and observed
handle snapshots must remain unchanged after `ready` and before `release`.
Image identity values remain private transient test memory: names, IDs, sizes,
digests, process identifiers, and handles are not printed or retained as
evidence.

## Ownership and failure behavior

Every image file handle is explicitly owned and closed once. M212 continues
to own and settle the process, Job Object, pipe, and overlapped-I/O handles;
M213 continues to own the query-only token handles. A query, bound, read,
identity, digest, or stability mismatch fails closed before the protocol
release. Opening the image with delete sharing avoids granting this observation
authority over filesystem mutation or cleanup.

This observation binds the executable file opened for the retained process. It
does not bind the loaded Python script bytes, imported module bytes,
environment, working directory, command line, or interpreter state. The
retained handles reduce path-only replacement ambiguity, but this one
cooperative current-host test does not prove hostile ABA resistance.

## Evidence and authority boundary

This is one same-host, same-logon, same-session observation. It does not prove
a distinct authenticated principal, independent host, hostile filesystem,
source-commit provenance, account or credential custody, fixture mutation,
interruption durability, collection, or cleanup. It is not qualifying M206 or
M208 evidence and cannot resolve criteria 6 or 7.

M214 adds no runtime source, public API, CLI or MCP command, production
harness, collector, account lifecycle, privilege transition, filesystem
mutation, network listener, dependency, package payload, version, workflow,
permission, secret, hosted allocation, or admission decision. No public
self-hosted runner is introduced.

## Primary references

- [QueryFullProcessImageNameW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-queryfullprocessimagenamew)
- [CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [GetFileInformationByHandleEx](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex)
- [FILE_ID_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [GetFileSizeEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfilesizeex)
- [SetFilePointerEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfilepointerex)
- [ReadFile](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-readfile)
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
