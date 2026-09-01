# Windows local control-channel probe

**Status:** Accepted M212 current-host test evidence; no cross-principal or
independent-host collection has occurred.

M212 exercises the smallest local coordination primitive needed to advance one
future M205/M209 fixture barrier after M211 has contained the participant. It is
Windows-only, test-only, and fixed-purpose. It does not issue collection or
cleanup authority, operate on a cache fixture, or satisfy M205's distinct-
principal requirement. Criteria 6 and 7 remain unresolved,
`windows_cleanup_admitted is false`, Windows is not admitted, and cleanup
remains unimplemented and unauthorized.

## Protected local endpoint

The controller creates one randomized local message-mode named-pipe instance.
The server uses `FILE_FLAG_FIRST_PIPE_INSTANCE`, allows exactly one instance,
and sets `PIPE_REJECT_REMOTE_CLIENTS`. It does not use the default pipe security
descriptor. Instead, the controller derives its current logon SID from its
owned process token and supplies a protected DACL with exactly one allow ACE
for that logon SID.

The live probe reads the resulting security descriptor back from the native
pipe object. It requires a present, non-default, protected DACL containing one
allow ACE for the exact logon SID and the exact bounded read/write access mask.
The broad Windows default DACL is therefore not accepted. The pipe name and
SID remain private test coordination values and are never retained as evidence.

`GENERIC_READ | GENERIC_WRITE` is needed by the fixed message client. Windows
maps those generic rights to the exact `0x0012019f` named-pipe access mask,
which includes the API's overlapping create-instance bit. M212 contains that
property with the single logon-SID ACE, 128-bit unpredictable pipe suffix,
one-instance limit, and a live second-server refusal check. This is current-
host test evidence, not a claim that a same-logon hostile process is excluded.

## Retained process identity

The controller creates one fixed direct `pythonw.exe` participant suspended,
with handle inheritance disabled. It assigns the retained process handle to a
new no-breakaway, kill-on-last-close Job Object before resume. The exact Job
membership must contain only that participant.

After the client connects but before any challenge is sent, the controller
requires `GetNamedPipeClientProcessId` to equal both the process identifier
returned by `CreateProcessW` and the identity returned from the retained process
handle. A client-provided or participant-reported PID is never accepted. The
participant must remain live and must emit no message before the controller
releases the first barrier.

M211 separately proves fixed descendant inheritance and exact two-member tree
termination. M212 does not weaken or duplicate that boundary; it proves one
single-member control connection whose identity is retained before release.

## Bounded challenge and sequence

Every connection receives a fresh 256-bit challenge from the operating-system
random source after native client identity is verified. The challenge is not a
command-line or environment value and is never written to retained evidence.
The closed message sequence is:

1. controller `challenge`, sequence 0;
2. participant `ready`, sequence 1;
3. controller `release`, sequence 2; and
4. participant `released`, sequence 3.

Each message is one canonical JSON object under
`ludoweave.test.windows-local-control-channel/1`, bounded to 1,024 bytes, with
exact fields and no trailing data. The participant accepts only the fixed pipe
name shape and this protocol; it cannot select a program, path, operation,
fixture, account, authority, or native target.

Controller connect, read, and write operations use overlapped I/O, owned event
handles, five-second native waits, `GetOverlappedResult`, and cancellation on
timeout. Job last-close remains the fail-safe for a participant blocked in a
client read. Every native handle is controller-owned or participant-owned and
closed at settlement.

## Refusal observations

The live tests prove these fixed outcomes:

- one fresh challenge and exact release reaches `released` and exit zero;
- replaying sequence 0 after `ready` exits with the protocol-refusal category;
- a sequence-2 release carrying a different challenge exits with the
  challenge-refusal category; and
- a canonical object with a missing protocol shape exits with the protocol-
  refusal category; and
- closing the server after `ready` exits with the disconnect-refusal category.

Every refusal occurs before `released`. The controller observes settlement
through its retained process handle and requires Job accounting to reach one
total and zero active processes. A participant message, PID disappearance, or
successful API return alone cannot establish success.

## Evidence and authority boundary

This is one same-host, same-logon observation. It does not prove principal-
scoped DACL resistance against a distinct authenticated account, hostile
connection races, cross-session behavior, account or credential custody,
independent host qualification, filesystem behavior, interruption durability,
recovery, or teardown of a real fixture. It is not qualifying M206 or M208
evidence and cannot resolve criteria 6 or 7.

M212 adds no product runtime source, public API, CLI or MCP command, production
harness, arbitrary process or pipe endpoint, network listener, dependency,
package payload, version, workflow, permission, secret, credential lifecycle,
filesystem mutation, cleanup authority, hosted allocation, or admission
decision. No public self-hosted runner is introduced.

## Primary references

- [Named-pipe security and access rights](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights)
- [CreateNamedPipeW](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-createnamedpipew)
- [GetNamedPipeClientProcessId](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getnamedpipeclientprocessid)
- [GetTokenInformation](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-gettokeninformation)
- [ConvertStringSecurityDescriptorToSecurityDescriptorW](https://learn.microsoft.com/en-us/windows/win32/api/sddl/nf-sddl-convertstringsecuritydescriptortosecuritydescriptorw)
- [Named-pipe server using overlapped I/O](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-server-using-overlapped-i-o)
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
