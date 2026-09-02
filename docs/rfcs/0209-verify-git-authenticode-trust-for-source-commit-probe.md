# RFC-0209: Verify retained Git Authenticode trust for the source-commit probe

**Status:** Accepted
**Milestone:** M226
**Decision class:** Direction-preserving

## Context

M225 proves that every actual Git child process image equals M224's retained
executable before child code runs. Stable identity and bytes do not show that
Windows accepts the executable under its Authenticode trust policy.

Windows `WinVerifyTrust` can apply the generic Authenticode policy to an
individual file described by both its full path and an already-open readable
handle. The provider allocates state during verification that must be released
by a subsequent close action.

## Decision

Verify retained Git Authenticode trust around the complete M225 boundary in one
Windows-only test composition. Perform one real Git lookup, retain that
canonical file through M224's existing non-inheritable read handle, and pass
both the canonical path and retained handle to
`WINTRUST_ACTION_GENERIC_VERIFY_V2`.

Set no user interface, no additional revocation checking, explicit provider
revocation-check suppression, and cache-only URL retrieval. This prevents the
probe from consulting the network and makes its result a bounded observation
of current local Windows trust state. Require exact success before executing
M225 and after M225 settles with an unchanged retained-file snapshot.

Every verification uses `WTD_STATEACTION_VERIFY` and then
`WTD_STATEACTION_CLOSE` in a `finally` boundary. A nonzero verification result
fails closed, and a close failure is reported when verification otherwise
succeeds.

This decision does not establish signer or publisher authorization. It does
not define a certificate or thumbprint allowlist, prove revocation freshness,
bind native DLLs or loader state, authenticate repository acquisition or the
local object store, or establish source/build provenance. It does not admit
Windows or authorize cleanup.

## Consequences

- The exact retained Git file used by M225 must satisfy local Windows generic
  Authenticode policy before and after all 48 child processes settle.
- The observation is deterministic with respect to network access but remains
  dependent on the current host trust store and cache.
- M221 through M225 evidence remains byte-for-byte unchanged.
- No runtime, package, dependency, lock, workflow, permission, fixture,
  example, script, benchmark, cleanup, or admission surface is added.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Invoke `Get-AuthenticodeSignature`

Rejected because it adds a second command process, does not bind the check to
the existing retained file handle, and can prefer a catalog signature over an
embedded signature.

### Require online revocation checking

Rejected because it adds network availability, mutable remote state, latency,
and credential/proxy environment to a local test observation. Revocation
freshness remains a separate admission decision.

### Pin the currently observed certificate thumbprint

Rejected because a signer allowlist is authority policy with rotation and
recovery obligations. One current-host observation does not authorize that
policy.
