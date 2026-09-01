# Windows local control token-binding probe

**Status:** Accepted M213 current-host test evidence; no cross-principal or
independent-host collection has occurred.

M213 layers one retained-token check onto the exact frozen M212 local control
channel. It is Windows-only, test-only, and fixed-purpose. It neither issues a
collection action nor operates on a cache fixture. Criteria 6 and 7 remain
unresolved, `windows_cleanup_admitted is false`, Windows is not admitted, and
cleanup remains unimplemented and unauthorized.

## Retained primary token

After M212 binds the named-pipe client to the retained participant process
handle, the controller opens that process's primary token with query-only
access. The token handle stays open across the challenge/ready barrier. Two
snapshots query and privately copy `TokenUser`, `TokenLogonSid`,
`TokenStatistics`, and `TokenSessionId` from that same retained token.

The first snapshot must identify a primary token. Its user SID, logon SID,
authentication identifier, and session identifier must equal the controller's
query-only primary-token snapshot. The participant token ID, authentication
identifier, modified ID, user SID, logon SID, session ID, and token type must
then remain byte-for-byte stable after `ready` and before `release`.

Token identity values remain private transient test memory. Raw SIDs, locally
unique identifiers, session identifiers, process identifiers, token handles,
and pipe names are not printed, serialized, or retained as evidence. Errors
name only the failed category or native operation and error code.

## Native session agreement

The controller obtains the pipe client's session through
`GetNamedPipeClientSessionId`, derives the retained process's session through
`ProcessIdToSessionId`, and reads the participant token's `TokenSessionId`.
All three must agree, and the participant token session must equal the
controller token session. This proves only the expected same-session property
of this one same-host, same-logon observation; it is not a cross-session test.

The M212 pipe DACL is also read back again using the participant token's copied
logon SID. The exact protected, non-default, single-ACE, bounded-access policy
must still hold before the challenge is released. This does not exclude a
hostile process already holding the same logon identity.

## No impersonation

Impersonation is not used. The probe does not call
`ImpersonateNamedPipeClient`, open a thread token, alter the controller's
security context, or require `RevertToSelf`. Retained process-token queries and
native session APIs establish the narrow observation without introducing a
thread-scoped privilege transition whose failed reversion would require
process termination.

Every token handle is explicitly owned and closed once. M212 continues to own
and settle the process, Job Object, named pipe, and overlapped-I/O handles.
Timeouts and protocol failures retain M212's bounded fail-closed settlement.

## Evidence and authority boundary

This is one same-host, same-logon observation. It does not prove a distinct
authenticated principal, separate logon, separate Windows session, hostile
same-logon race resistance, account or credential custody, independent-host
qualification, fixture mutation, interruption durability, collection, or
cleanup. It is not qualifying M206 or M208 evidence and cannot resolve criteria
6 or 7.

M213 adds no product runtime source, public API, CLI or MCP command, production
harness, account lifecycle, impersonation, privilege adjustment, network
listener, dependency, package payload, version, workflow, permission, secret,
hosted allocation, or admission decision. No public self-hosted runner is
introduced.

## Primary references

- [Access tokens](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-tokens)
- [GetTokenInformation](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-gettokeninformation)
- [TOKEN_INFORMATION_CLASS](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_information_class)
- [TOKEN_STATISTICS](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_statistics)
- [GetNamedPipeClientSessionId](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getnamedpipeclientsessionid)
- [ProcessIdToSessionId](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-processidtosessionid)
- [Client impersonation](https://learn.microsoft.com/en-us/windows/win32/secauthz/client-impersonation)
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
