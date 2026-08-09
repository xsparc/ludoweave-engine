# RFC-0037: Require fresh public release TLS sessions

- **Status:** Accepted
- **Date:** 2026-08-10
- **Owners:** LudoWeave maintainers
- **Milestone:** M54

## Context

M50 creates a new verified client `SSLContext` for every public release hop,
and M53 proves that the connected socket retained that exact context after the
handshake. The verifier did not yet observe whether the TLS implementation
reported that the resulting connection resumed an earlier session.

Python exposes that post-handshake observation through
[`SSLSocket.session_reused`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.session_reused).
Python also documents that an [`SSLSocket.session`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.session)
may be assigned on a client socket before the handshake to reuse a session.
OpenSSL describes TLS 1.3 resumption as a PSK path that can avoid another
certificate exchange. Requiring the portable reported reuse state to be false
therefore strengthens the release verifier's per-hop evidence without adding a
TLS implementation, session cache, or ticket controller.

This observation does not reconstruct the handshake or independently prove
which handshake messages were exchanged. It relies on the supported
CPython/OpenSSL surface to report whether the session was reused.

## Decision

After M53 exact context binding and before M52 service identity, M51 negotiated
session inspection, or HTTP transmission, every fixed API and bounded
redirected asset hop must:

1. read the actual connected socket's `session_reused` property;
2. require the value to be exactly `False`, rejecting truthy, falsey-but-not-
   boolean, absent, unsupported, and raising observations; and
3. repeat the observation independently after the handshake on every redirect.

The existing connection remains the sole owner of the socket and closes it on
success or failure. A missing socket, unavailable accessor, resumed session,
malformed value, or inspection exception fails before later TLS evidence or
HTTP transmission under the stable, content-silent
`public_release.tls_failed` code. An available local inspection exception is
chained as the cause, while public output exposes no reuse value, host,
certificate, peer, URL, response, or credential.

## Boundary

M54 changes no workflow, runner allocation, action, permission, trigger,
credential, release mutation, release authority, dependency, lock, version,
runtime package, or public API. It adds no session cache, session object
assignment, ticket disabling, ticket-count policy, TLS implementation
introspection, custom trust, certificate or SPKI pin, certificate/chain parser,
revocation policy, channel binding, proxy, or network sandbox.

Fixture and pull-request evidence are not a real public release observation,
independent or external verification, proof of a full handshake or certificate
exchange, every TLS implementation or delivery path, future availability,
immutability, artifact security, PyPI availability, or a supported channel. A
real M54 pass remains pending an explicitly authorized signed-tag release run.

## Consequences

- A resumed TLS connection fails closed even if all later identity and
  negotiated-session observations would otherwise pass.
- An implementation that cannot expose the portable observation fails closed.
- Every redirect supplies independent freshness evidence before transmitting
  its request.
- Existing M53-M47 context, identity, session, peer, response, artifact, and
  installed-smoke boundaries remain authoritative.

## Alternatives considered

- Accept session resumption because a reused session can still provide secure
  transport. Rejected because the public verifier is an infrequent release
  evidence path and benefits from an explicit non-resumption observation.
- Disable tickets or mutate session caches. Rejected because those controls
  are implementation-specific, broaden ownership, and are unnecessary for
  rejecting the actual reported connection state.
- Inspect `SSLSession` identifiers, tickets, or context statistics. Rejected
  because those surfaces do not improve the exact per-connection decision and
  would add fragile implementation detail.
- Claim a full certificate exchange from `session_reused is False`. Rejected
  because M54 observes the implementation's reuse report; it does not parse or
  reconstruct the handshake.

## References

- [Python 3.14 `SSLSocket.session_reused`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.session_reused)
- [Python 3.14 `SSLSocket.session`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.session)
- [OpenSSL 3.6 TLS server guide](https://docs.openssl.org/3.6/man7/ossl-guide-tls-server-block/)
