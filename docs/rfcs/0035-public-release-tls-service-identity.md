# RFC-0035: Bind public release TLS service identity

- **Status:** Accepted
- **Date:** 2026-08-09
- **Owners:** LudoWeave maintainers
- **Milestone:** M52

## Context

M50 configures mandatory certificate-path and hostname verification, and M51
validates the negotiated session. The portable verifier still does not observe
that the resulting TLS socket retained the URL-derived reference hostname or
that the verified peer certificate remains available before HTTP transmission.

Python documents that `SSLContext.check_hostname` matches the peer certificate
during the handshake only when a `server_hostname` is passed to the client
socket. `SSLSocket.server_hostname` exposes that expected name in ASCII A-label
form for an internationalized domain name, while
`SSLSocket.getpeercert(binary_form=True)` returns the peer certificate in DER
form. RFC 9525 defines the corresponding client reference identity and server-
presented certificate relationship for TLS service authentication.

## Decision

Before opening every fixed API or bounded redirected asset hop, the verifier
must normalize the current URL hostname to its built-in IDNA ASCII A-label and
use that reference hostname for the connection. After M49 connected-peer
confinement and before the M51 negotiated-session check, it must:

1. require the connected TLS socket's observed `server_hostname` to be a non-
   empty string equal to that reference hostname under case-insensitive
   comparison; and
2. require `getpeercert(binary_form=True)` to return non-empty immutable bytes.

The existing M50 `PROTOCOL_TLS_CLIENT`, `CERT_REQUIRED`, system trust,
`check_hostname`, strict X.509, and per-hop context remain authoritative for
certificate-path, validity, and hostname matching. M52 observes the reference-
identity binding and certificate presence; it does not parse or independently
reimplement certificate validation.

## Ordering, failure, and ownership

Each hop connects, validates its actual globally reachable port-443 peer,
validates the URL-derived TLS service identity, validates the negotiated
session, and only then sends an HTTP method, path, or header. Every redirect
owns a new context, connection, peer observation, service-identity observation,
session observation, and close path.

A missing socket or accessor, unsupported inspection, invalid IDNA reference,
malformed or mismatched observed hostname, missing or non-byte peer
certificate, or inspection exception fails with the stable, content-silent
`public_release.tls_failed` code. Public output exposes no hostname,
certificate, peer, URL, session value, response, or credential. An available
local cause remains chained, and the connection remains closed exactly once by
the existing owner.

## Authority and non-scope

M52 changes no workflow, runner allocation, action, permission, trigger,
credential, release mutation, publication, retry, rollback, cleanup,
dependency, lock, version, runtime package, or public API. It adds no custom CA
bundle, certificate or SPKI pin, certificate-chain parser/export, fingerprint
allowlist, client certificate, revocation, OCSP, CRL, certificate-transparency,
DNSSEC, TLS-session, proxy, or new network policy.

Fixture and pull-request conformance are not a real public release observation,
independent or external verification, every TLS/CDN/geographic path, future-
availability proof, immutability proof, artifact-security result, PyPI
availability, or a supported release channel. No real M52 signed-tag execution
is performed or claimed.

## Alternatives rejected

- Rely only on the configured context. Rejected because M52's narrow purpose is
  to prove that the actual socket retained the expected reference hostname and
  peer certificate before request transmission.
- Reparse and match certificate identities in project code. Rejected because
  OpenSSL already performs the authoritative hostname/path validation and a
  second partial implementation would create divergent security semantics.
- Pin a leaf certificate, SPKI digest, issuer, or fingerprint. Rejected because
  GitHub/CDN certificate rotation requires a separately governed pin lifecycle
  that this milestone does not establish.
- Require Python 3.13 chain-inspection APIs. Rejected because CPython 3.12
  remains supported and the leaf-presence observation is portable across the
  complete supported range.
- Add another workflow or runner. Rejected because the shared standard-library
  verifier owns the behavior on all supported platforms.

## Sources

- [Python 3.14 `SSLContext.check_hostname`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLContext.check_hostname)
- [Python 3.14 `SSLSocket.server_hostname`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.server_hostname)
- [Python 3.14 `SSLSocket.getpeercert`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLSocket.getpeercert)
- [Python 3.14 `HTTPSConnection`](https://docs.python.org/3.14/library/http.client.html#http.client.HTTPSConnection)
- [RFC 9525: Service Identity in TLS](https://www.rfc-editor.org/rfc/rfc9525.html)
