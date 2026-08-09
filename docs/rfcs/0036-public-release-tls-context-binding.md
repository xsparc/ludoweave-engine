# RFC-0036: Bind the public release socket to its exact TLS context

- **Status:** Accepted
- **Date:** 2026-08-10
- **Owners:** LudoWeave maintainers
- **Milestone:** M53

## Context

M50 creates an explicit verified client `SSLContext` for every public release
hop. M49, M52, and M51 then inspect the connected peer, service identity, and
negotiated session. The verifier did not yet observe that the actual socket was
bound to that exact context or remained client-side after the handshake.

Python documents `SSLSocket.context` as the `SSLContext` to which a socket is
bound and `SSLSocket.server_side` as the socket role. It also documents that an
`HTTPSConnection(context=...)` uses the supplied context for its HTTPS
connection. Because changing an `SSLContext` after use can produce surprising
behavior, the complete M50 context policy also needs revalidation after the
connection handshake and before later TLS observations.

## Decision

After M49 connected-peer confinement and before M52 service-identity evidence,
M51 session inspection, or HTTP transmission, every fixed API and redirected
asset hop must:

1. require the actual socket's `context` to be the exact context object passed
   to that hop's `HTTPSConnection`;
2. require the socket's `server_side` value to be exactly `False`; and
3. revalidate after the handshake that the exact context still uses
   `PROTOCOL_TLS_CLIENT`, `CERT_REQUIRED`, hostname checking, a TLSv1.2 minimum,
   strict and partial-chain verification flags, and no key-log file.

Object identity is intentional. An equivalent or substitute context does not
prove that the socket retained the context whose policy the verifier reviewed.
Every redirect owns a new exact context, connection, binding observation, and
close path.

## Ordering, failure, and ownership

Each hop creates and prevalidates its context, connects, validates its actual
globally reachable port-443 peer, validates exact context binding and the
client-side role after the handshake, revalidates the context policy, observes
service identity, validates the negotiated session, and only then sends an
HTTP method, path, or header.

A missing socket or accessor, unsupported inspection, substituted context,
non-client role, changed policy, or inspection exception fails before HTTP
with the stable, content-silent `public_release.tls_failed` code. Public output
exposes no context value, hostname, certificate, peer, URL, session value,
response, or credential. An available local cause remains chained, and the
connection remains owned and closed by the existing per-hop `finally` path.

## Authority and non-scope

M53 changes no workflow, runner allocation, action, permission, trigger,
credential, release mutation, publication, retry, rollback, cleanup,
dependency, lock, version, runtime package, or public API. It adds no custom
trust, pinning, certificate or chain parsing, revocation, TLS-session reuse,
channel binding, proxy policy, network sandbox, or external monitor.

Fixture and pull-request conformance are not a real public release observation,
independent or external verification, every TLS/CDN/geographic path, future-
availability proof, immutability proof, artifact-security result, PyPI
availability, or a supported release channel. No real M53 signed-tag execution
is performed or claimed.

## Alternatives rejected

- Trust only `HTTPSConnection(context=...)`. Rejected because M53's narrow
  purpose is to observe the binding on the actual connected socket.
- Accept an equivalent context. Rejected because equality of selected fields
  does not prove which context owns the socket or preserve per-hop ownership.
- Check only before connecting. Rejected because the contract specifically
  protects the context used after the handshake and before HTTP transmission.
- Add a wrapper or third-party TLS stack. Rejected because Python exposes the
  required portable observations on every supported CPython version.
- Add another workflow or runner. Rejected because the shared portable
  verifier owns the behavior on the existing supported-platform matrix.

## Sources

- [Python 3.14 `SSLSocket.context`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.context)
- [Python 3.14 `SSLSocket.server_side`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.server_side)
- [Python 3.14 `SSLContext`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLContext)
- [Python 3.14 `HTTPSConnection`](https://docs.python.org/3.14/library/http.client.html#http.client.HTTPSConnection)
