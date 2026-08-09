# Release process and artifact verification

Only maintainers publish official releases. The `release.yml` workflow runs for
an exact signed annotated `vVERSION` tag and refuses a tag that differs from
`pyproject.toml`, lacks GitHub-verified signature evidence, targets a different
checkout, or is not reachable from `origin/main`. The repository does not
publish a release from pull-request CI.

## Candidate contents

`scripts/release_artifacts.py` stages a new empty directory containing:

- the pure `py3-none-any` wheel and source distribution;
- a deterministic versioned sample ZIP;
- Apache-2.0 `LICENSE` and project `NOTICE`;
- the direct optional-dependency notice inventory;
- versioned release notes;
- an SPDX 2.3 JSON SBOM describing the baseline wheel;
- a versioned JSON release manifest with sizes and SHA-256 digests;
- `SHA256SUMS` covering every other staged file.

The baseline SBOM has one package because the wheel has no runtime dependencies
and redistributes no optional graphics providers. Locked contributor/graphics
packages are installed separately under their own distributions and notices.

Before installed-wheel smoke or staging, M38 builds the wheel and source
distribution twice in distinct directories and runs
`scripts/verify_distribution_reproducibility.py`. Both directories must contain
exactly one matching pure wheel/source-archive pair and the bytes must match.
The deterministic JSON result records exact sizes and SHA-256 identities. This
same-job check is not an independent or cross-platform rebuild claim; see
[RFC-0021](rfcs/0021-enforce-distribution-reproducibility.md).

## Maintainer gate

1. Require the milestone PR's complete local and hosted gates to pass.
2. Confirm the changelog, version, date, release notes, compatibility status,
   security policy, notices, and retrospective agree.
3. Confirm the intended release commit is integrated into `origin/main`.
4. Build twice, verify byte reproducibility, then stage/smoke the candidate
   from that clean signed commit.
5. Create and push a signed annotated `vVERSION` tag at that exact commit.
6. M39 makes the tag job fail first unless GitHub reports a valid tag
   signature and local Git confirms the same annotated object, checkout commit,
   and `origin/main` ancestry. The verifier is loaded from fetched `origin/main`,
   not the tag checkout. `--verify-tag` remains an existence check, not the
   signature gate.
7. The least-privilege tag workflow reruns quality/tests/docs, builds/stages and
   smokes artifacts, and creates GitHub build-provenance and SPDX attestations.
8. M40 creates a private prerelease draft without assets, uploads the complete
   staged set without clobbering, fetches the authenticated GitHub release
   document, and requires every uploaded name, state, size, and SHA-256 digest
   to match local staging before publishing the draft.
9. M41 additionally requires the authenticated draft's source release-notes
   body to exactly match bounded staged `RELEASE_NOTES.md`; note content is not
   emitted by the validator.
10. M42 preserves the validated numeric release ID, publishes the draft, then
    requires that exact authenticated record to report public prerelease state,
    a valid UTC publication time, and unchanged notes/assets.
11. M43 requires unique bounded numeric asset IDs, retrieves each exact ID
    through the authenticated binary asset endpoint, and rehashes the complete
    downloaded set against the same published document.
12. M44 verifies SLSA v1 provenance for every retrieved asset and an SPDX 2.3
    SBOM attestation for exactly one pure wheel under the exact repository,
    tag, source/signer commit, release workflow, issuer, and hosted-runner
    policy.
13. M45 fetches that exact public release and every exact asset ID without a
    GitHub credential, revalidates the public document and downloaded set, and
    runs the complete release smoke against those public bytes.
14. M46 waits for the publishing job to succeed, then uses one fresh read-only
    Linux runner to retrieve the same workflow's admitted candidate and the
    exact public bytes, revalidate them, install the wheel in a new isolated
    environment, and run the sample bundle.
15. M47 replaces the Bash-only public verifier and expands that tag-only fresh
    rehearsal to Ubuntu, Windows, and macOS. Every runner creates its own plan,
    revalidates exact public bytes, and runs complete installed release smoke.
16. M48 requires a direct `200` release document, only bounded `200`/`302`
    asset handling, API-only headers confined to `api.github.com`, and distinct
    timeout, transport/protocol, and local-output failure codes.
17. M49 validates the actual port-443 TLS socket peer before every fixed API or
    redirected asset HTTP request and allows only globally reachable unicast
    IPv4/IPv6.
18. M50 builds an explicit verified TLS client context per public hop and
    rejects ambient TLS session-secret logging through `SSLKEYLOGFILE`.
19. M51 advertises HTTP/1.1 and validates the actual negotiated TLS version,
    cipher report, compression, and ALPN before every HTTP request.
20. M52 validates the actual socket's IDNA-normalized reference hostname and
    non-empty DER peer certificate before the M51 session check and every HTTP
    request.
21. M53 validates after the handshake that the actual socket retains the exact
    per-hop verified context and an exactly client-side role, then revalidates
    that context before M52, M51, or every HTTP request.
22. M54 requires the actual socket's `session_reused` observation to be exactly
    `False` after the handshake and M53 binding, before service identity,
    negotiated-session inspection, or every HTTP request.
    M55 then validates every response, including every redirect, with the
    documented HTTP/1.1-class value `11`, absent or exactly `chunked`
    `Transfer-Encoding`, no
    `Transfer-Encoding`/`Content-Length` ambiguity, and a string content length
    before status, redirect, or body use.
23. Independently download the public assets, verify checksums and
    attestations, install the wheel in a clean environment, and run the sample
    bundle before announcing.

No PyPI upload is configured in community alpha. Name reservation, trusted
publishing, and a non-prerelease support policy require separate maintainer
decisions.

M39/RFC-0022 trusts GitHub's annotated-tag verification result and separately
checks local object/checkout/main ancestry. It does not install a local trust
store, define a signer or key allowlist, authorize tag creation, enable
immutable releases, or claim that a valid signature alone authorizes a release.
Repository tag rules, protected deployment environments, and workflow-file
governance remain operational controls; this workflow cannot authenticate a
replacement of its own definition by an already-authorized tag actor.

M40/RFC-0023 makes the GitHub draft boundary explicit. The standard-library
validator consumes only bounded local files and a capped strict JSON document;
network and publication remain workflow-owned. Upload or identity failure
leaves an unpublished draft for inspection, and retries never use `--clobber`.
The remote digest is GitHub's authenticated report, not independent storage
verification. M40 does not enable immutable releases, create a real release,
change attestations, or authorize automatic draft deletion.

M41/RFC-0024 advances that internal validator contract to
`ludoweave.release-draft-integrity/2`. It reads only the fixed staged
`RELEASE_NOTES.md` member, caps it at 256 KiB, requires non-empty strict UTF-8
without NUL, and compares it exactly with the authenticated release `body`.
Missing, null, substituted, truncated, or normalization-different text fails
before publication. The gate does not log note content, inspect rendered
Markdown, evaluate links or factual accuracy, or add a network call, workflow
allocation, permission, dependency, release, or publication authority.

M42/RFC-0025 advances the internal contract to
`ludoweave.release-draft-integrity/3` and makes expected draft/published state
explicit. The existing draft check now requires null `published_at`; after
publication, one read-only API request for the same numeric release ID requires
`draft=false`, `prerelease=true`, a boolean immutable field, a valid UTC
publication time, and the same notes/assets. Failure blocks a successful job
result but does not automatically unpublish, delete, or mutate an already
public release. The check neither requires nor claims immutable-release policy
and adds no runner, action, permission, dependency, trigger, tag, release,
upload, or publication authority.

M43/RFC-0026 advances the internal contract to
`ludoweave.release-draft-integrity/4`, requires unique positive 63-bit asset
IDs, and allows a fully verified published document to create one exclusive
runner-temporary `ludoweave.release-asset-retrieval-plan/1` file. The existing
tag job consumes only safe decimal IDs, expected sizes, and basenames, retrieves
each exact ID through `gh api` with `Accept: application/octet-stream`, bounds
every stream to the expected size plus one byte, rejects short/long or
over-total responses, then reruns the same validator over the downloaded
directory and same published document. The plan and downloads never clobber
existing paths. This proves one authenticated
retrieval observation, not unauthenticated availability, every CDN/cache edge,
future bytes, immutability, consumer installation, or attestation verification.
It adds no runner, action, permission, dependency, trigger, tag, release,
upload, rollback, cleanup, or publication authority.

M44/RFC-0027 consumes the canonical M43 plan and exact downloaded directory in
one standard-library verifier after byte revalidation. It runs
`gh attestation verify` once per asset for SLSA v1 provenance and once for the
single pure wheel's SPDX 2.3 SBOM. Every invocation binds repository, release
workflow, tag ref, source/signer commit, GitHub Actions OIDC issuer, hosted
runner class, predicate type, a 30-bundle limit, null child streams, and a
30-second timeout. The 32-asset plan cap limits the verifier to 33 sequential
calls. Output contains only protocol/status/counts or a stable generic failure.
This verifies subject digest and constrained GitHub identity at one observation
point; it does not prove artifact security, an independent or trusted build,
predicate truth beyond the constrained type/identity, future availability or
non-revocation, global asset access, immutability, consumer installation, or a
supported channel. Failure occurs after publication and grants no retry,
unpublish, delete, edit, rollback, or cleanup authority.

M45/RFC-0028 performs a second, credential-free retrieval after M44. It fetches
the exact public release ID and exact M43 asset IDs only from fixed HTTPS GitHub
API endpoints, with client configuration disabled, bounded redirects/connect/
request time, a 4-MiB document cap, and the inherited 32-asset, 256-MiB per-
asset, and 512-MiB total limits. The public document is validated against local
staging before retrieval; every new partial file must have the exact expected
length; the complete public directory is revalidated and passed to the existing
release smoke. The step receives no GitHub credential or authorization/cookie
header and trusts no browser download URL. It establishes one public API and
same-run installed-candidate observation only—not independent/external or
cross-platform installation, every CDN/cache/browser path, future availability,
immutability, artifact security, PyPI, or a supported release channel. Failure
occurs after publication and grants no retry, mutation, rollback, or cleanup
authority.

M46/RFC-0029 extracts that bounded retrieval into one shared shell verifier and
adds a dependent fresh-runner rehearsal. The release job exposes only its
verified numeric release ID and package version. The new Linux job uses explicit
read-only contents permission, retrieves the exact named candidate through the
pinned same-workflow artifact channel, creates a new plan exclusively, repeats
the complete public retrieval/revalidation, and runs installed release smoke in
its own workspace. Its public HTTP requests receive no release credential; the
checkout and artifact actions still use scoped workflow services. The job adds
no release mutation or publication authority.

This is a same-workflow, same-provider Linux rehearsal, not independent or
external verification, a cross-platform public matrix, a clean machine outside
GitHub-hosted Actions, every delivery path, future availability, immutability,
artifact security, PyPI, or a supported release channel. M46 by itself does not
replace maintainer gate 23. No real fresh-runner pass exists until an authorized
signed-tag release run executes.

M47/RFC-0030 replaces the shared Bash verifier with one typed standard-library
Python program and expands the existing fresh-consumer job to the exact Ubuntu,
Windows, and macOS matrix. Every execution depends on release success, uses
read-only contents permission and no dependency cache, retrieves the exact named
same-workflow candidate through the pinned artifact action, creates a fresh
exclusive M43-format plan, and repeats complete public byte validation plus
installed release smoke.

The portable client uses a verified TLS context without ambient proxy/client
configuration. Initial hosts are fixed; at most three remote redirects may
remain on HTTPS port 443. Blocking socket operations are capped at 10 seconds
inside one 30-second monotonic deadline. Existing document, plan, ID, name,
count, byte, partial, exact-set, and smoke bounds remain fail-closed. Success
reports only aggregate count/bytes; failures use stable content-silent codes.

M47 supplies same-workflow hosted observations for all three supported
operating systems, but it is still not independent/external verification, a
clean machine outside GitHub-hosted Actions, every delivery path, future
availability, immutability, artifact security, PyPI, or a supported channel.
It does not replace maintainer gate 23. No real M47 pass exists until an
authorized signed-tag release run executes.

M48/RFC-0031 narrows the shared portable client's accepted response and failure
semantics. The release document must return a direct `200`; an asset request may
return `200` or follow at most three `302` responses through the inherited
HTTPS/default-port bound. Other redirects fail. The API-version header is sent
only to `api.github.com`. Request/header/body timeouts share one stable timeout
code, other network/protocol errors remain request failures, and local
filesystem errors remain output failures.

M48 changes no workflow or release authority and does not create a real public
observation in pull-request CI. It preserves M47's cross-platform same-workflow
claim boundary and does not replace the independent consumer check in
maintainer gate 23. No real M48 pass exists until an authorized signed-tag
release run executes.

M49/RFC-0032 establishes each normal verified TLS connection before HTTP
transmission, inspects its actual `getpeername()` result, requires actual port
443, and accepts only globally reachable unicast IPv4/IPv6. IPv4-mapped IPv6 is
classified by its embedded address. The check repeats for the fixed API host
and every bounded `302` asset hop. Non-global peers have one stable forbidden
code; connect/inspection timeout and malformed/unavailable peer failures retain
M48's timeout/request taxonomy without exposing host or address values.

M49 adds no hostname/IP allowlist, separate DNS preflight, network sandbox,
workflow, allocation, dependency, retry, cleanup, mutation, or release
authority. Pull-request fixtures are not a real public release observation and
do not replace the independent consumer check in maintainer gate 23. No real
M49 pass exists until an authorized signed-tag release run executes.

M50/RFC-0033 replaces default-context construction with one explicit verified
client context per hop. It loads system server-auth roots, requires certificate
and hostname validation, sets TLS 1.2 as the minimum, retains strict and
partial-chain X.509 validation, and requires key logging to be disabled. An
ambient `SSLKEYLOGFILE` value is left unchanged and cannot create or receive
TLS session secrets from the verifier. Context failures use the stable,
content-silent `public_release.tls_failed` code.

M50 changes no workflow, allocation, dependency, package, release authority,
or independent-consumer claim. It adds no custom trust store, certificate pin,
client certificate, proxy, release mutation, retry, or cleanup. Pull-request
fixtures do not establish a real public release observation. No real M50 pass
exists until an authorized signed-tag release run executes.

M51/RFC-0034 makes the actual negotiated session a fail-closed pre-request
boundary. Each M50 context advertises only `http/1.1`. After M49 connected-peer
validation and before HTTP transmission, the verifier requires exactly
TLSv1.2 or TLSv1.3, a well-formed cipher report with at least 128 secret bits,
no TLS compression, and ALPN `http/1.1` or no negotiated ALPN. Every bounded
redirect repeats the check; malformed, unavailable, or unexpected session
state uses the stable, content-silent `public_release.tls_failed` code.

M51 changes no workflow, allocation, dependency, package, release authority,
or independent-consumer claim. It adds no cipher-name allowlist, custom trust,
certificate/SPKI pin, revocation policy, TLS fingerprint, release mutation,
retry, or cleanup. Pull-request fixtures are not a real public release
observation and do not replace the independent consumer check in maintainer
gate 23. No real M51 pass exists until an authorized signed-tag release run
executes.

M52/RFC-0035 makes the URL-derived service identity an observed pre-request
boundary. After M49 peer confinement and before M51 session inspection, the
verifier normalizes the URL hostname with built-in IDNA, requires the socket's
reference hostname to match case-insensitively, and requires a non-empty DER
peer certificate. M50's verified context remains authoritative for certificate
path, validity, and hostname matching. Every bounded redirect repeats the
complete identity observation; malformed, unavailable, mismatched, or
unsupported state uses the stable, content-silent
`public_release.tls_failed` code.

M52 changes no workflow, allocation, dependency, package, release authority,
or independent-consumer claim. It adds no certificate parser/export,
certificate/SPKI pin, fingerprint allowlist, custom trust, revocation,
OCSP/CRL/CT policy, DNSSEC, release mutation, retry, or cleanup. Pull-request
fixtures are not a real public release observation and do not replace the
independent consumer check in maintainer gate 23. No real M52 pass exists until
an authorized signed-tag release run executes.

M53/RFC-0036 makes the actual socket's TLS-context ownership an observed pre-
request boundary. After the handshake and M49 peer confinement, but before M52
service identity, M51 session inspection, or HTTP transmission, the socket
must retain the exact context supplied for that hop and an exactly client-side
role. The verifier then revalidates the complete M50 context policy. Every
redirect repeats this check with an independent context; unsupported or
changed state uses the stable, content-silent `public_release.tls_failed` code.

M53 changes no workflow, allocation, dependency, package, release authority,
or independent-consumer claim. It adds no trust replacement, pinning,
certificate/chain parser, revocation, session reuse, channel binding, proxy,
network sandbox, retry, or cleanup. Pull-request fixtures are not a real public
release observation and do not replace the independent consumer check in
maintainer gate 23. No real M53 pass exists until an authorized signed-tag
release run executes.

M54/RFC-0037 makes the actual socket's reported TLS freshness an observed pre-
request boundary. After the handshake and M53 exact context binding, but before
service identity, negotiated-session inspection, or HTTP transmission, the
socket's `session_reused` property must be exactly `False`. Every redirect
repeats the observation independently; unavailable, resumed, malformed, or
raising state uses the stable, content-silent `public_release.tls_failed` code.

M54 changes no workflow, allocation, dependency, package, release authority,
or independent-consumer claim. It adds no session cache, session assignment,
ticket control, TLS implementation introspection, trust replacement, pinning,
release mutation, retry, or cleanup. The reported state does not independently
prove a full handshake or certificate exchange. Pull-request fixtures are not
a real public release observation and do not replace the independent consumer
check in maintainer gate 23. No real M54 pass exists until an authorized
signed-tag release run executes.

M55/RFC-0038 validates response framing after every `getresponse()` and before
status, `Location`, or body use. The response version must be the documented
HTTP/1.1-class integer value `11`. CPython can normalize another raw
`HTTP/1.x` status-line token to `11`, so this is not exact wire-token evidence.
`Transfer-Encoding` is absent or exactly `chunked`
case-insensitively and cannot coexist with `Content-Length`; any present
content length remains subject to the existing string, ASCII-decimal, maximum,
and exact-size rules. Valid chunked bodies continue through the standard-
library decoder and existing bounded reader. Malformed, unsupported,
ambiguous, or raising metadata uses content-silent
`public_release.request_failed`, repeating on every redirect.

M55 changes no workflow, allocation, dependency, package, runtime API, or
release authority and adds no private response-state dependency, raw HTTP/chunk
parser, alternate client, HTTP/2 or HTTP/3, proxy, or general request-smuggling
claim or exact status-line proof. Pull-request fixtures are not a real public
release observation. No real M55 pass exists until an authorized signed-tag
release run exercises the public path.

M26/RFC-0009 adds offline admission machinery for the future supported
deprecation-capable feature-release channel. The current workflow remains
prerelease-only, no release record is admitted, and gate 6 remains false. See
the [supported release channel readiness guide](supported-release-channel-readiness.md).

M27/RFC-0010 adds the empty reviewed external-contributor rehearsal fixture and
evaluator to the deterministic sample bundle. Release smoke proves only that
the installed offline evidence path works; it is not an external contribution,
feedback artifact, or usability result. See the
[external-contributor rehearsal readiness guide](external-contributor-rehearsal-readiness.md).

M30/RFC-0013 adds the empty reviewed published-wheel installation-matrix
fixture and evaluator to the deterministic sample bundle. Release smoke proves
only that the installed offline evidence path works; it is not a public
release, independent installation, matrix result, or support claim. See the
[installation-matrix readiness guide](installation-matrix-readiness.md).

M31/RFC-0014 adds the empty reviewed response/review-latency fixture and
evaluator to the deterministic sample bundle. Release smoke proves only that
the installed offline evidence path works; it is not a human response, review,
latency measurement, service-level result, or support claim. See the
[response and review latency readiness guide](response-review-latency-readiness.md).

M32/RFC-0015 adds the empty reviewed replay-divergence-rate fixture and
evaluator to the deterministic sample bundle. Release smoke proves only that
the installed offline evidence path works; it is not a complete CI replay
cohort, measured divergence rate, reliability result, or release gate. See the
[replay-divergence-rate readiness guide](replay-divergence-rate-readiness.md).

M33/RFC-0016 adds the empty reviewed benchmark-regression-rate fixture and
evaluator to the deterministic sample bundle. Release smoke proves only that
the installed offline evidence path works; it is not a controlled paired
benchmark cohort, measured regression rate, performance result, native-code
decision, or release gate. See the
[benchmark-regression-rate readiness guide](benchmark-regression-rate-readiness.md).

M34/RFC-0017 adds the empty reviewed agent-tool recovery-rate fixture and
evaluator to the deterministic sample bundle. Release smoke proves only that
the installed offline evidence path works; it is not a task-directed
operational cohort, measured recovery-free completion rate, reliability
result, provider certification, or release gate. See the
[agent-tool recovery-rate readiness guide](agent-tool-recovery-rate-readiness.md).

M35/RFC-0018 adds the empty reviewed third-party conformance-adoption fixture
and evaluator to the deterministic sample bundle. Release smoke proves only
that the installed offline evidence path works; it is not an independently
authored adapter or plugin, passing external conformance result, provider
certification, support matrix, or adoption claim. See the
[third-party conformance-adoption readiness guide](third-party-conformance-adoption-readiness.md).

## Consumer verification

Verify local checksums using the platform's SHA-256 tool, then verify official
GitHub provenance:

```console
gh attestation verify ludoweave-VERSION-py3-none-any.whl -R xsparc/ludoweave-engine
gh attestation verify ludoweave-VERSION-py3-none-any.whl -R xsparc/ludoweave-engine --predicate-type https://spdx.dev/Document/v2.3
```

Artifact attestations are stored by GitHub and bind the subject digest to the
tag workflow. `RELEASE_MANIFEST.json` is reproducible release metadata, not a
cryptographic signature or substitute for the hosted attestation.
Matching repeat builds are also not provenance: they do not identify the
builder or prove that the environment was trustworthy.

M44 automates this check inside a real signed-tag run, but no hosted
attestation pass exists until such a run creates and verifies the attestations.
Attestation verification is an integrity and identity claim, not an artifact-
security or independent-build certification.

M45 also exercises the exact public API release and asset IDs without supplying
a GitHub credential, then runs the complete installed release smoke against
those downloaded bytes. No public-path pass exists until a real signed-tag run,
and this same-run observation is not a substitute for the independent consumer
check in maintainer gate 23.

M46 repeats that check from a dependent fresh Linux runner using the exact
candidate preserved by the publishing job. It improves runner/workspace and
isolated-install separation but remains inside the same workflow and provider,
so it is also not a substitute for the independent consumer check in gate 23.

M47 runs that same exact public-byte and installed-candidate observation from
fresh Ubuntu, Windows, and macOS runners through one portable Python verifier.
This establishes no real matrix result until an authorized tag run executes and
remains no substitute for the independent consumer check in gate 23.

M48 makes that verifier accept only the documented release/asset response set,
keeps API-only headers on the fixed API host, and reports timeout,
transport/protocol, and local-output failures distinctly. Fixture and
pull-request evidence do not substitute for an authorized tag run or the
independent consumer check in gate 23.

M49 makes every fixed API and redirected asset request prove its actual
port-443 TLS peer is globally reachable unicast before HTTP transmission. It
does not add a hostname/IP allowlist, separate DNS pass, network sandbox, real
release result, or substitute for the independent consumer check in gate 23.

M50 creates an explicit verified context for each hop and prevents ambient TLS
key logging. M51 validates the negotiated TLS version, cipher strength,
compression, and ALPN. M52 then observes that the actual socket retained the
IDNA-normalized reference hostname and a non-empty peer certificate. M53 binds
that socket to the exact verified client context after the handshake and before
M52, M51, or the request. M54 then requires `session_reused` to be exactly
`False` before those later observations or the request. These fixture and pull-
request checks do not create a real public release result or substitute for the
independent consumer check in gate 23.
