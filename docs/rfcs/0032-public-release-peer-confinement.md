# RFC-0032: Confine public release requests to global connected peers

- **Status:** Accepted
- **Date:** 2026-08-09
- **Owners:** LudoWeave maintainers
- **Milestone:** M49

## Context

M48 constrains the shared public release client to GitHub's documented direct
`200` release response and direct `200` or bounded `302` asset responses. Every
initial URL is fixed, redirected URLs must remain verified HTTPS on the default
port, API-only headers remain on `api.github.com`, and exact post-download bytes
are revalidated.

That URL policy does not classify the address actually reached by a permitted
redirect hostname. A hostname can resolve to loopback, link-local, private,
shared, documentation, benchmarking, reserved, or other non-global space. A
separate DNS lookup would not be the request's authoritative peer because the
connection could resolve again or select a different address.

Python's socket interface exposes the remote address of the actual connected
socket through `getpeername()`. The standard-library `ipaddress` module exposes
IPv4/IPv6 global-reachability classification based on the IANA special-purpose
registries. The supported current CPython 3.12-3.14 patch releases agree on the
documented corrected special-purpose ranges used by this decision.

## Decision

Constrain the existing M48 client without changing its call sites or authority:

1. establish the normal verified TLS connection before transmitting each HTTP
   request;
2. inspect the actual connected peer through `getpeername()`;
3. require a well-formed IPv4 or IPv6 address and actual peer port 443;
4. classify IPv4-mapped IPv6 through its embedded IPv4 address;
5. require a globally reachable address and additionally reject multicast and
   unspecified addresses;
6. repeat the check for the fixed `api.github.com` request and every accepted
   `302` asset redirect; and
7. transmit no HTTP method, path, or headers until that hop passes.

Private, shared, loopback, link-local, documentation, benchmarking,
unspecified, multicast, reserved, and every other non-global connected peer
fails with `public_release.peer_forbidden`. A connect or peer-inspection
`TimeoutError` retains `public_release.request_timeout`. An unavailable socket,
malformed peer result, wrong peer port, invalid address, or other peer
inspection failure uses `public_release.request_failed`.

Public JSON remains generic and content-silent. It does not include a hostname,
address, URL, request path, response body, environment value, credential, or
local path. Internal exception chaining remains available for maintainer-side
diagnosis.

## Connection and ownership boundary

The client still creates one `HTTPSConnection` per response hop with the fixed
ten-second blocking timeout inside M48's 30-second monotonic request deadline.
Calling `connect()` performs DNS resolution and the verified TLS handshake
needed to create the socket. Peer validation occurs immediately afterward and
before HTTP request transmission. M49 does not claim to prevent DNS queries,
TCP packets, or the TLS handshake itself from reaching a rejected peer.

The actual connected socket is authoritative; M49 adds no hostname/CDN
allowlist, fixed-IP allowlist, separate DNS preflight, DNSSEC resolver, ambient
proxy, or packet-level network sandbox. Default certificate and hostname
verification remain unchanged. Every M48 response, redirect, header, timeout,
transport/output, document, plan, asset, count, byte, path, exclusive-partial,
exact-validation, and installed-smoke bound remains.

## Authority and failure behavior

M49 changes no workflow, runner allocation, action, permission, trigger,
credential, dependency, lock, version, runtime, package, public API, upload,
publication, edit, delete, unpublish, rollback, retry, cleanup, or other release
mutation. In short, M49 grants no release mutation.

The verifier still owns only its runner-temporary document, plan, download
directory, partials, and isolated smoke environment. A failed real tag run
leaves the already published prerelease for explicit maintainer review.

## Claims and non-claims

Fixture-driven tests establish deterministic connected-peer ordering,
IPv4/IPv6 classification, redirect-hop revalidation, and stable failure codes.
Pull-request CI establishes supported development-platform compatibility. This
is not a real public release observation.

An authorized signed-tag run would remain same-workflow, same-repository,
same-account, and same-provider evidence. M49 does not establish a network
sandbox, independent or external verification, a machine outside
GitHub-hosted Actions, every CDN or geographic path, future availability,
immutability, artifact security, vulnerability freedom, PyPI availability, or
a supported release channel. No real M49 signed-tag execution is performed or
claimed.

## Alternatives rejected

- Maintain only the M48 URL syntax check. Rejected because hostname syntax does
  not establish the address actually reached.
- Resolve and classify the hostname before constructing the connection.
  Rejected because a separate lookup is not the actual connected peer and adds
  a rebinding/selection gap.
- Require a CDN hostname allowlist. Rejected because GitHub documents a
  redirect location but no stable object-host list; certificate verification,
  actual global-peer confinement, exact IDs, and exact bytes are the durable
  boundaries. M49 therefore uses no hostname allowlist.
- Allow all globally classified multicast or unspecified values. Rejected
  because they are not valid remote unicast endpoints for this client.
- Retry another resolved address after a forbidden peer. Rejected because it
  changes observation semantics and timing, complicates failure evidence, and
  is unnecessary for fail-closed conformance.
- Add another workflow or runner. Rejected because the gap is in one shared
  standard-library client and fits the unchanged three-allocation substantive
  pull-request gate.

## Sources

- [GitHub: Get a release asset](https://docs.github.com/en/rest/releases/assets#get-a-release-asset)
- [Python 3.14 `http.client`](https://docs.python.org/3/library/http.client.html)
- [Python 3.14 socket `getpeername()`](https://docs.python.org/3/library/socket.html#socket.socket.getpeername)
- [Python 3.14 `ipaddress`](https://docs.python.org/3/library/ipaddress.html)
- [IANA IPv4 Special-Purpose Address Registry](https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml)
- [IANA IPv6 Special-Purpose Address Registry](https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml)
