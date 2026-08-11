# RFC-0041: Constrain public release transport cleanup

- **Status:** Accepted
- **Date:** 2026-08-10
- **Owners:** LudoWeave maintainers
- **Milestone:** M58

## Context

M47-M57 bound the portable public-release verifier's request, connected-peer,
TLS, HTTP, redirect, and response-body behavior. Each request also creates an
`HTTPSConnection` and may obtain an `HTTPResponse`, but the existing `finally`
block called their `close()` methods directly. A response close failure could
therefore prevent the connection close attempt, and either close failure could
replace a more useful verification failure or escape through an unstable
exception surface.

The verifier also published a successfully streamed asset partial before its
response and connection were closed. A cleanup-only failure could therefore
report failure after the final asset path had become visible. Redirect
continuation similarly depended on implicit `finally` ordering rather than an
explicit successful-cleanup contract.

Python documents `HTTPConnection.close()` as closing the server connection and
`HTTPResponse` as a buffered readable object. The common I/O contract makes
`close()` idempotent and uses context-managed cleanup even when an operation
raises. M58 adopts only the public close methods; it does not inspect private
socket or response state.

## Decision

For every successfully created connection, the verifier makes one explicit
connection close attempt. If a response was obtained, it first makes one
explicit response close attempt. Both close attempts occur even when response
close fails, and the response failure wins when both attempts fail.

An already-active verification or control-flow failure remains the primary
failure: cleanup failures are suppressed after both close attempts. With no
active failure, an ordinary cleanup `Exception` becomes the stable,
content-silent `public_release.request_failed` error and retains its local cause
through exception chaining. A cleanup-only control signal outside `Exception`,
such as `KeyboardInterrupt`, remains unwrapped after the connection attempt.

Cleanup succeeds before redirect continuation for the current hop. When an
asset uses a separate partial path, cleanup also succeeds before publication
to the final path. Cleanup therefore occurs before partial publication. Direct
release-document streaming retains its existing target ownership and failure
behavior.

## Boundary

M58 adds ordered cleanup conformance only. It adds no rollback: bytes already
written to a direct target or partial file remain available for bounded runner
cleanup and diagnostic inspection after failure. It adds no retry, alternate
client, raw parser, connection pooling, cache, proxy, DNS preflight, network
sandbox, workflow, runner allocation, action, permission, trigger, credential,
release mutation, release authority, dependency, lock, version, runtime
package, or public API.

This is no general resource-leak proof for the standard library, operating
system, intermediaries, or process termination. Fixture and pull-request
evidence are not a real public release observation, independent or external
verification, proof of every delivery path, future availability, immutability,
artifact security, PyPI availability, or a supported channel. A real M58 pass
remains pending an explicitly authorized signed-tag release run.

## Consequences

- Response close precedes connection close when a response exists.
- Both close attempts occur even if the first attempt fails.
- Cleanup cannot mask the primary request, protocol, validation, output, or
  control-flow failure.
- Cleanup-only ordinary failures use one stable public error surface.
- Redirect continuation and separate partial publication require successful
  cleanup, while M58 deliberately provides no rollback guarantee.

## Alternatives considered

- Keep direct calls in `finally`. Rejected because the first failure can skip
  the second close and either cleanup failure can mask the primary failure.
- Use only a response context manager. Rejected because a connection can exist
  before a response is obtained and still requires explicit ownership cleanup.
- Suppress every cleanup failure. Rejected because a cleanup-only failure must
  fail the verifier rather than silently permit redirect or publication
  progress.
- Delete output on cleanup failure. Rejected because rollback widens local
  mutation and failure-ordering semantics beyond this conformance slice.

## References

- [Python 3.14 `http.client`](https://docs.python.org/3.14/library/http.client.html)
- [Python 3.14 I/O base classes](https://docs.python.org/3.14/library/io.html#io.IOBase)
