# RFC-0033: Isolate public release TLS key logging

- **Status:** Accepted
- **Date:** 2026-08-09
- **Owners:** LudoWeave maintainers
- **Milestone:** M50

## Context

M49 validates the actual connected peer before transmitting each fixed API or
redirected asset HTTP request. The portable client creates its verified TLS
context through `ssl.create_default_context()`.

Supported CPython documents an ambient behavior at that boundary: when
`SSLKEYLOGFILE` is present, `create_default_context()` enables TLS key logging.
The key-log file is a debugging facility that receives TLS session secrets and
is opened for append. A release verifier must not silently inherit that
diagnostic side effect or write secrets to an environment-selected path.

Python also documents that `PROTOCOL_TLS_CLIENT` enables mandatory certificate
verification and hostname checking. An explicit context can load default
server-auth roots and select its minimum TLS version without involving the
default-context helper's key-log hook.

## Decision

For every fixed API or bounded asset-redirect hop, the portable verifier must:

1. construct a new `SSLContext(PROTOCOL_TLS_CLIENT)` directly;
2. load system default certificates for `SERVER_AUTH`;
3. require `CERT_REQUIRED` and hostname checking;
4. set TLS 1.2 as the minimum protocol version;
5. enable `VERIFY_X509_PARTIAL_CHAIN` and `VERIFY_X509_STRICT`;
6. require `keylog_filename` to remain disabled before handing the context to
   `HTTPSConnection`; and
7. fail with `public_release.tls_failed` when construction, root loading, or
   invariant validation fails.

The verifier does not read, remove, rewrite, or disclose `SSLKEYLOGFILE`.
Fixture tests set the variable to a controlled nonexistent path and prove that
the value remains intact while no target is created. Redirects receive a
different context object and repeat all existing URL, peer, timeout, response,
size, path, and exact-byte checks.

## Failure and ownership

Context construction happens before a connection object exists. A TLS-context
failure therefore has no connection or response to close and writes no release
document, asset, partial, or key-log target. Its public error contains only the
stable code and generic message; internal exception chaining retains the cause
for local diagnosis.

Each context is owned by its one `HTTPSConnection` hop. The existing connection
close path remains authoritative on success, redirect, and failure. M50 does
not share or mutate a context after use.

## Authority and non-scope

M50 changes no workflow, runner allocation, action, permission, trigger,
credential, release mutation, publication, retry, rollback, cleanup,
dependency, lock, version, runtime package, or public API. It adds no proxy,
custom CA bundle, certificate/SPKI pin, client certificate, external verifier,
or negotiated-session reporting. System and OpenSSL default trust locations
remain the trust boundary.

Fixture and pull-request validation are not a real public release observation,
independent or external verification, every CDN/geographic path, a complete
environment-isolation proof, future-availability proof, immutability proof,
artifact-security result, PyPI availability, or a supported release channel.
No real M50 signed-tag execution is performed or claimed.

## Alternatives rejected

- Continue using `create_default_context()`. Rejected because documented
  ambient key-log behavior is the gap being closed.
- Clear `context.keylog_filename` after default-context creation. Rejected
  because context creation can already open the environment-selected file.
- Temporarily remove `SSLKEYLOGFILE` from `os.environ`. Rejected because the
  environment is process-global and mutating it would introduce a concurrency
  and restoration boundary not needed by an explicit context.
- Disable system trust and pin GitHub certificates or keys. Rejected because
  certificate rotation would add operational fragility and GitHub does not
  publish a stable pin contract for this client.
- Add another workflow or runner. Rejected because one shared standard-library
  verifier owns the behavior on all supported platforms.

## Sources

- [Python 3.14 `ssl.create_default_context`](https://docs.python.org/3.14/library/ssl.html#ssl.create_default_context)
- [Python 3.14 `SSLContext.keylog_filename`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLContext.keylog_filename)
- [Python 3.14 `PROTOCOL_TLS_CLIENT`](https://docs.python.org/3.14/library/ssl.html#ssl.PROTOCOL_TLS_CLIENT)
- [Python 3.14 `SSLContext.minimum_version`](https://docs.python.org/3.14/library/ssl.html#ssl.SSLContext.minimum_version)
