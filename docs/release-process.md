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

M56/RFC-0039 validates the documented response status after M55 framing and
before comparison, redirect resolution, or body use. The status must be a non-
boolean integer from 100 through 599. Each followed `302` must expose exactly
one Location field through the documented header-pair list; its value must be a
single 1-to-8,000-octet ASCII URI-reference with valid RFC 3986 characters and
complete percent escapes. Bracket delimiters may appear only within a parsed
authority, not its path, query, or fragment. Invalid status uses content-silent
`public_release.request_failed`; invalid Location metadata or resolution uses
`public_release.redirect_failed`, and supported local causes remain chained.
Every redirect repeats the validation.

The resolved reference must still pass the bounded HTTPS URL policy before use.
Cross-host absolute references remain permitted, so every hop repeats the M49-
M55 peer, TLS, framing, deadline, byte, and exact-artifact checks; there is no
host allowlist. M56 adds no raw parser, alternate client, proxy, DNS preflight,
network sandbox, workflow, allocation, dependency, runtime API, release
authority, or general SSRF claim. Pull-request fixtures are not a real public
release observation. No real M56 pass exists until an authorized signed-tag
release run exercises the public path.

M57/RFC-0040 validates every successful response body after the existing
framing, status, and redirect gates. Each `HTTPResponse.read(amount)` result
must be immutable bytes no larger than the requested amount before EOF
interpretation, length accounting, or local output. Any validated
`Content-Length` must equal the streamed octets for both the public release
document and a final asset response. Malformed read shapes use content-silent
`public_release.request_failed`; declared-length disagreement uses
`public_release.size_mismatch`; supported local causes remain chained.

M57 retains short reads, chunked decoding through `http.client`, unframed
close-delimited bodies, and independent expected asset sizes. It adds no raw
HTTP/chunk parser, alternate client, content decoder, cleanup, workflow,
allocation, dependency, runtime API, or release authority and makes no general
response-completeness claim. Pull-request fixtures are not a real public
release observation. No real M57 pass exists until an authorized signed-tag
release run exercises the public path.

M58/RFC-0041 gives each public-release exchange explicit ordered cleanup.
Every obtained response gets one response close attempt before its created
connection gets one connection close attempt, and both close attempts occur if
the first fails. An active primary failure remains primary; a cleanup-only
ordinary failure uses content-silent `public_release.request_failed`, while a
cleanup control signal remains unwrapped.

Successful cleanup occurs before redirect continuation and before partial
publication from a separate asset partial path. M58 provides no rollback for
already written direct-target or partial bytes and adds no retry, workflow,
allocation, dependency, runtime API, release authority, or real public release
observation. No real M58 pass exists until an authorized signed-tag release run
exercises the public path.

M60/RFC-0043 treats every pre-existing final directory entry for the fresh
public document, download directory, retrieval plan, asset target, and asset
partial as a filesystem collision. The `lstat()` preflight observes the entry
itself, so files, directories, live links, and dangling links fail before
network or validator side effects. Normal output collisions keep
`public_release.output_exists`; a fresh-plan collision keeps
`public_release.plan_exists`; inspection failures use content-silent output or
plan failure codes.

The writer still relies on `x`/`xb` exclusive creation and hard-link
publication for no clobber behavior after preflight. M60 is no race-free
filesystem guarantee and adds no directory-descriptor sandbox, rollback,
cleanup, retry, workflow, allocation, dependency, runtime API, release
authority, or real public release observation. No real M60 pass exists until an
authorized signed-tag release run exercises the public path.

M61/RFC-0044 treats the expected candidate directory as read-only input. The
candidate directory and runner-owned output root are strictly resolved before
network or validator side effects. The output root cannot equal or resolve
beneath the candidate directory, including through a resolved alias; overlap
uses stable `public_release.path_overlap`. Filesystem-identity comparison across
the output ancestry also rejects differently spelled aliases on a case-
insensitive filesystem. Resolution and identity-inspection failures retain
content-silent candidate or temporary-directory codes. A separate candidate
child of the output root remains valid because fixed output entries remain its
siblings.

This is no race-free filesystem guarantee and adds no directory-descriptor or
general filesystem sandbox, rollback, cleanup, retry, workflow, allocation,
dependency, runtime API, release authority, or real public release observation.
No real M61 pass exists until an authorized signed-tag release run exercises
the public path.

M62/RFC-0045 constrains the public consumer's retrieval-plan asset names to a
deterministic portable subset: 1 through 255 allowed ASCII characters, no
trailing period, no classic Windows device stem even before an extension, and
case-insensitive uniqueness. Invalid plans use content-silent
`public_release.invalid_plan` before asset download or creation of the asset
output directory.

This is a lexical plan-consumer policy with no filesystem probing, locale,
normalization, cleanup, rollback, retry, workflow, dependency, runtime API, or
release authority. It does not change the earlier release-document download or
validator ordering. Pull-request evidence is not a real public release
observation; no real M62 pass exists until an authorized signed-tag release run
exercises the public path.

M63/RFC-0046 confines subordinate stdout and subordinate stderr while the
portable public consumer runs its in-process release-document validator and
complete release smoke. Success emits exactly one JSON document on stdout;
admitted failure emits exactly one content-silent JSON document on stderr. A
subordinate succeeds only with an exact zero integer, so boolean, float,
integer-subclass, and custom comparison results fail closed.

The Python stream redirection is process-global and is admitted only for this
single-thread standalone utility. It does not capture direct file-descriptor or
arbitrary subprocess writes. M63 adds no workflow, dependency, runtime API,
release authority, cleanup, or publication. Pull-request evidence is not a real
public release observation; no real M63 pass exists until an authorized signed-
tag release run exercises the public path.

M64/RFC-0047 bounds the staged sample bundle consumed by the complete release
smoke. Before extraction, the complete central directory must contain at most
256 members, no member may declare more than 1 MiB uncompressed, and aggregate
declared expansion may not exceed 8 MiB. Existing path and symbolic-link checks
run in that same complete preflight, before extraction creates any path. The
bundle may use only stored or deflated members; BZIP2, LZMA, and unknown methods
are rejected before extraction because their library paths do not provide the
same bounded decompressor-output behavior.

Admitted regular files then stream in 64 KiB blocks and must reproduce their
declared sizes exactly. The limits bound smoke resource use; they do not make
ZIP metadata authenticated or create a general archive sandbox. A later I/O or
decompression failure can leave partial output in the disposable runner-owned
temporary directory because cleanup and rollback are not part of M64. There is
no workflow, dependency, runtime API, or release-authority change, and pull-
request evidence is not a real public release observation.

M65/RFC-0048 adds portable sample member path identity to that same complete
preflight. Every member is a regular file beneath the exact expected root; its
relative path contains at most 255 ASCII characters and each component uses
the restricted portable ASCII grammar without a trailing period or Windows
device stem. Explicit directory entries, explicitly encoded non-regular file
types, case-insensitive duplicate paths, case-ambiguous directory ancestors,
and every file/directory prefix collision fail before extraction. A missing ZIP
file-type mode remains admitted because common producers encode permissions
without encoding a file type.

The verifier preserves admitted spellings exactly. It performs no Unicode
normalization, locale-sensitive comparison, filesystem probing, or rewriting,
and it does not guarantee every possible absolute runner path is accepted by
every filesystem. This private policy adds no workflow, dependency, sample-
producer, runtime API, cleanup guarantee, or release authority. Pull-request
evidence is not a real public release observation.

M66/RFC-0049 adds pre-publication cleanup to the same private extraction path.
The caller supplies an existing runner-owned output directory, and the final
sample root must not already exist as a file, directory, live link, or dangling
link. After complete archive preflight, admitted files stream beneath the
expected root inside a same-filesystem temporary staging directory. Required-
file completeness is validated there, and a single rename publishes only the
complete staged root.

Any pre-publication copy, decompression, write, incomplete-bundle, or rename
failure triggers owned temporary-directory cleanup and leaves the final sample
root absent. Existing entries are never replaced or removed. This is a
single-process visibility boundary, not crash-durable storage, a filesystem
transaction, or concurrent race isolation. It adds no workflow, dependency,
sample producer, runtime API, or release authority, and pull-request evidence
is not a real public release observation.

M67/RFC-0050 adds an exact source-defined sample-bundle inventory to that same
complete preflight. The 50 validated relative regular-file identities must
match exactly, independent of archive order. An unexpected member or missing
member fails with one content-silent category before extraction opens any
member or creates a staging directory. The sample producer remains unchanged;
an architecture test independently requires its current deterministic ZIP to
match the verifier expectation.

This is a project-product identity check, not content scanning, provenance, a
permission policy, or a general archive sandbox. It adds no workflow,
dependency, sample producer, runtime API, or release authority, and pull-request
evidence is not a real public release observation.

M68/RFC-0051 bounds the sample archive itself before the standard-library ZIP
parser receives it. Release smoke first rejects an obvious non-regular or
oversized source from path metadata without opening it, then opens the bundle
once and revalidates its descriptor as a regular file no larger than 16 MiB.
It gives that same opened handle to `ZipFile`. A non-regular or oversized source
fails with a stable content-silent category before central-directory parsing,
member reads, staging, or extraction output.

This input limit complements rather than replaces M64's member and expanded-
size bounds. It does not make later bytes immutable, authenticate ZIP metadata,
isolate concurrent filesystem actors, or create a general archive sandbox.
There is no workflow, dependency, sample producer, runtime API, or release-
authority change, and pull-request evidence is not a real public release
observation.

M69/RFC-0052 rejects sample members whose ZIP general-purpose bit flags
indicate traditional encryption, strong encryption, or masked header values.
The check runs during the complete central-directory preflight, before exact-
inventory validation, member reads, password handling, staging, or extraction
output. Every failure uses one content-silent category rather than a library
message containing the archive-controlled member identity.

The project sample is public deterministic evidence and has no password or key
lifecycle. M69 adds no password, decryption support, raw ZIP parser,
dependency, sample producer, runtime API, workflow, or release authority. It
does not authenticate central-directory metadata or create a general archive
sandbox, and pull-request evidence is not a real public release observation.

M70/RFC-0053 binds extraction to the sample digest already accepted from
`SHA256SUMS`. After path and descriptor checks, complete release smoke hashes
and rewinds the same opened handle before ZIP parsing. It hashes and rewinds
that handle again after all member reads and staged-completeness validation but
before publication by final rename. A persistent mismatch has one content-
silent category, and a second-check failure cleans the owned partial stage.
Each hash reads at most M68's 16 MiB limit plus one rejection byte.

This narrows the previous reopen gap but provides no immutable-input guarantee;
change-and-restore behavior between checks is outside the claim. M70 is not a
general archive sandbox and adds no workflow, dependency, sample producer,
runtime API, or release authority. Pull-request evidence is not a real public
release observation.

M71/RFC-0054 makes the checksum-admitted byte sequence itself the ZIP parser
input. After source path and descriptor admission, complete release smoke copies
at most 16 MiB into an owned binary spooled temporary file while computing the
expected digest. A mismatch or extra rejection byte clears that target and
fails content-silently before ZIP parsing or staging. Success rewinds the
snapshot, and `ZipFile` plus all member reads consume those exact bytes.

Later source mutation cannot alter the admitted parser snapshot. This creates
no persistent copy, source-immutability guarantee, filesystem lock, raw parser,
or general archive sandbox. M71 adds no workflow, dependency, sample producer,
runtime API, or release authority, and pull-request evidence is not a real
public release observation.

M72/RFC-0055 adds a content-silent outer failure boundary to that private
extractor. A documented `BadZipFile` or `LargeZipFile` from constructor,
metadata, member-open, or member-read work becomes the stable error
`sample bundle ZIP data is invalid` after owned cleanup. The original parser
exception remains programmatic context, but suppressed context prevents
archive-controlled details from appearing in normal rendered output.

The catch is deliberately narrow: verifier policy, filesystem, subprocess,
and unexpected failures keep their existing categories. M72 adds no workflow,
dependency, sample producer, runtime API, or release authority, is not a
general archive sandbox, and is not a real public release observation.

M73/RFC-0056 adds exactly `UnicodeDecodeError` to that same outer boundary.
The standard ZIP reader can raise it while decoding archive-controlled UTF-8
names in the central directory during construction or in a local header during
member open. Either path becomes the existing stable
`sample bundle ZIP data is invalid` error after owned source, snapshot,
archive, and staging cleanup.

The original decoding exception remains programmatic context; suppressed
context keeps invalid bytes, offsets, codec, and reason out of normal rendered
output. Other Unicode/value failures and verifier policy, filesystem,
subprocess, and unexpected failures remain specific. M73 adds no broad catch,
raw parser, workflow, dependency, sample producer, runtime API, or release
authority, is not a general archive sandbox, and is not a real public release
observation.

M74/RFC-0057 adds exactly `zlib.error` to that same outer boundary. A
checksum-admitted archive can carry the exact inventory and valid ZIP metadata
but contain an invalid raw-deflate payload. The standard ZIP member reader can
raise the documented decompression exception while a bounded member copy is in
progress. That path becomes the existing stable
`sample bundle ZIP data is invalid` error after owned source, snapshot,
archive, member, target, and staging cleanup.

The original decompression exception remains programmatic context; suppressed
context keeps its library- and content-determined diagnostic out of normal
rendered output. EOF, policy, filesystem, subprocess, and unexpected failures
remain specific. M74 adds no broad catch, replacement decompressor, raw parser,
workflow, dependency, sample producer, runtime API, or release authority, is
not a general archive sandbox, and is not a real public release observation.

M75/RFC-0058 rejects compressed patched data, ZIP general-purpose bit 5,
during the existing all-member flag preflight. Supported CPython versions
otherwise raise `NotImplementedError` only from member open. Complete release
smoke now emits the stable content-silent policy error before inventory
validation, staging, or member reads. Encryption retains its M69 precedence
when indicators are combined.

Other general-purpose bits remain outside this exact decision. M75 adds no
broad flag allowlist, raw parser, repair, workflow, dependency, sample
producer, runtime API, or release authority, is not a general archive sandbox,
and is not a real public release observation.

M76/RFC-0059 rejects enhanced deflating, ZIP general-purpose bit 4, only for
compression method 8 during the existing all-member preflight. Complete
release smoke emits the stable content-silent policy error before inventory
validation, staging, or member reads. Encryption and compressed-patch checks
retain their established precedence.

The check consumes central-directory flags exposed by `ZipInfo`. Stored members
carrying bit 4, local-header inconsistencies, and every other unexamined flag/
method combination remain outside this exact decision. M76 adds no broad flag
allowlist, enhanced-deflate decoder, raw parser, repair, workflow, dependency,
sample producer, runtime API, or release authority, is not a general archive
sandbox, and is not a real public release observation.

M77/RFC-0060 checks every decoded `ZipInfo.orig_filename` for an exact NUL byte
after the established flag preflight and before member metadata, inventory
validation, staging, or member reads. Complete release smoke emits the stable
content-silent policy error without rendering the archive-controlled name or
hidden suffix. Existing encryption, compressed-patch, and enhanced-deflate
categories retain precedence.

The check does not compare arbitrary original and normalized names. M77 adds no
general normalized-name comparison, no raw parser, header-consistency claim,
rewriting, repair, workflow, dependency, sample producer, runtime API, or
release authority, is not a general archive sandbox, and is not a real public
release observation.

M78/RFC-0061 rejects exact central-directory general-purpose bit 3, the data-
descriptor indicator exposed by `ZipInfo.flag_bits`, during a separate all-
member preflight before M77 name policy, member metadata, inventory validation,
member reads, or staging. Complete release smoke emits the stable content-
silent error without rendering archive-controlled content. The established
M69/M75/M76 categories retain archive-wide precedence.

The fixed sample producer continues to emit no data-descriptor flag. M78 adds
no raw descriptor parser, no broad flag allowlist, local-header consistency
claim, repair, workflow, dependency, sample producer, runtime API, or release
authority, is not a general archive sandbox, and is not a real public release
observation.

M79/RFC-0062 rejects exact Info-ZIP Unicode Path extra-field ID `0x7075`
during a separate all-member preflight before M77 decoded-name policy, member
metadata, inventory validation, member reads, or staging. A bounded extra-
field walk consumes the already decoded central-directory extra bytes exposed
by `ZipInfo`; the stable content-silent error does not render either name.
Every established M69/M75/M76/M78 category retains archive-wide precedence.

The fixed sample producer emits no extra fields. M79 adds no broad extra-field
ban, general name-difference policy, local-header comparison, repair, workflow,
dependency, runtime API, sample producer, or release authority, is not a
general archive sandbox, and is not a real public release observation.

M80/RFC-0063 rejects exact PKWARE ZIP64 extended-information extra-field ID
`0x0001` during a separate all-member preflight after M79 policy and before
M77 decoded-name policy, member metadata, inventory validation, member reads,
or staging. A bounded extra-field walk consumes the central-directory bytes
already exposed by `ZipInfo`; the stable content-silent error exposes no
archive-controlled content. Every established flag, descriptor, and Unicode
Path category retains archive-wide precedence.

The fixed sample producer continues to emit no extra fields. M80 adds no broad
extra-field ban, raw ZIP64 parser, archive-record validator, large-file
support, local-header comparison, repair, workflow, dependency, runtime API,
sample producer, or release authority, is not a general archive sandbox, and
is not a real public release observation.

M81/RFC-0064 rejects parser-exposed non-empty ZIP archive and member comments
after every established flag and exact extra-field pass. The archive comment
is checked
once before a separate all-member comment pass; both finish before decoded-
name policy, member metadata, exact inventory validation, staging, or member
reads. Complete release smoke emits stable content-silent errors `sample bundle
uses an archive comment` and `sample bundle uses a member comment` without
including comment bytes or member names.

The fixed sample producer emits neither comment surface. M81 adds no raw ZIP
parser, general comment scanner, comment decoder, rewriting, workflow,
dependency, runtime API, release authority, or producer change. It is not a
general archive sandbox and is not a real public release observation.

M82/RFC-0065 rejects every parser-exposed nonzero `ZipInfo.volume` after all
established flag, exact extra-field, and comment passes. The separate all-
member pass finishes before decoded-name policy, member metadata, exact
inventory validation, staging, or member reads. Complete release smoke emits
stable content-silent error `sample bundle uses a split-volume member` without
including a member name or archive-controlled volume value.

The fixed sample producer emits volume zero for all 50 members. M82 adds no raw
end-record parser, no multi-volume assembler, no neighboring-file discovery,
workflow, dependency, runtime API, release authority, or producer change. It
is not a general archive sandbox and is not a real public release observation.

M83/RFC-0066 requires zero current-disk and central-directory-start disk fields
in the final conventional 22-byte end-of-central-directory record. The check
runs after every established flag, exact extra-field, comment, and member-
volume pass but before decoded-name policy, metadata, exact inventory, staging,
or member reads. Either nonzero value emits stable content-silent error `sample
bundle uses unsupported archive disk fields`; the owned snapshot position is
restored and all owned resources close before control returns.

The fixed sample producer emits the record at end of file with both fields
zero. M83 adds no ZIP64 end-record parser, end-record search, neighboring-file
discovery, multi-volume assembler, workflow, dependency, runtime API, release
authority, or producer change. It does not resolve a `0xFFFF` sentinel, is not
a general archive sandbox, and is not a real public release observation.

M84/RFC-0067 requires both conventional end-of-central-directory entry counts
to equal the standard reader's parsed member count. The check runs after all
established member preflights and M83 archive disk policy but before decoded-
name policy, metadata, exact inventory, staging, or member reads. A mismatch
emits stable content-silent error `sample bundle archive entry counts are
inconsistent`; the owned snapshot position is restored and all owned resources
close before control returns.

The fixed sample producer emits 50 in both fields and exposes 50 members. M84
adds no ZIP64 end-record parser, sentinel resolution, end-record search,
neighboring-file discovery, multi-volume assembler, workflow, dependency,
runtime API, release authority, or producer change. It is not a general
archive sandbox and is not a real public release observation.

M85/RFC-0068 requires the final conventional central-directory size plus
offset to equal the absolute offset of the final end-of-central-directory
record. The check runs after M84 archive entry-count policy but before decoded-
name policy, metadata, exact inventory, staging, or member reads. A mismatch
emits stable content-silent error `sample bundle central directory placement
is inconsistent`; the shared helper restores the owned snapshot position and
all owned resources close before control returns.

The fixed sample producer starts at byte zero and satisfies the relationship
exactly. M85 adds no central-directory record parser, local-header parser,
prepended executable support, self-extracting archive support, neighboring-file
discovery, multi-volume assembler, workflow, dependency, runtime API, release
authority, or producer change. It is not a general archive sandbox and is not
a real public release observation.

M86/RFC-0069 requires the minimum parser-exposed `ZipInfo.header_offset` to be
zero. The check runs after M85 central-directory placement policy but before
decoded-name policy, metadata, exact inventory, staging, or member reads. A
nonzero value emits stable content-silent error `sample bundle first local
header placement is inconsistent`; all owned resources close before control
returns.

The fixed producer exposes 50 members and an earliest local-header offset of
zero. M86 adds no local-header parser, central-directory parser, inter-member
layout validator, prepended executable support, workflow, dependency, runtime
API, release authority, or producer change. It is not a general archive sandbox
and is not a real public release observation.

M87/RFC-0070 requires all parser-exposed local-header offsets to be distinct.
The check runs after M86 first-offset policy but before decoded-name policy,
metadata, exact inventory, staging, or member reads. A duplicate emits stable
content-silent error `sample bundle local header offsets are inconsistent`;
all owned resources close before control returns.

The fixed producer exposes 50 members and 50 distinct local-header offsets.
M87 adds no local-header parser, central-directory parser, offset ordering/
bounds rule, inter-member layout validator, workflow, dependency, runtime API,
release authority, or producer change. It is not a general archive sandbox and
is not a real public release observation.

M88/RFC-0071 requires strictly increasing local-header offsets in parser-
exposed archive order. The check runs after M87 distinctness but before decoded-
name policy, metadata, exact inventory, staging, or member reads. A non-
increasing pair emits stable content-silent error `sample bundle local header
offsets are out of order`; all owned resources close before control returns.

The fixed producer exposes 50 members in strict offset order. M88 adds no local-
header parser, central-directory record parser, offset bounds/contiguity rule,
inter-member layout validator, workflow, dependency, runtime API, release
authority, or producer change. This profile is not a general archive sandbox
and is not a real public release observation.

M89/RFC-0072 requires every parser-exposed local-header offset to remain
strictly before the conventional central directory. The check runs after M88
ordering but before decoded-name policy, metadata, exact inventory, staging, or
member reads. An offset at or after the boundary emits stable content-silent
error `sample bundle local header offsets are out of bounds`; all owned
resources close before control returns.

The fixed producer exposes all 50 member offsets below the admitted boundary.
M89 adds no local-header parser, central-directory record parser, local-record
extent, adjacency, contiguity, or physical non-overlap rule, no inter-member
layout validator, workflow, dependency, runtime API, release authority, or
producer change. This profile is not a general archive sandbox and is not a
real public release observation.

M90/RFC-0073 requires the fixed producer's four-byte local-header signature
`PK\x03\x04` at every parser-exposed offset. The signature classifier runs
after M89 bounds but before decoded-name policy, metadata, exact inventory,
staging, or member reads. A mismatch or short read emits stable content-silent
error `sample bundle local header signature is inconsistent`; all owned
resources close before control returns.

The fixed producer exposes that signature at all 50 member offsets. M90 adds no
local-header field parser, central-directory record parser, record-extent,
adjacency, contiguity, payload-bound, or physical non-overlap rule, no inter-
member layout validator, workflow, dependency, runtime API, release authority,
or producer change. This profile is not a general archive sandbox and is not a
real public release observation.

M91/RFC-0074 requires every parser-exposed offset to leave room for ZIP's
30-byte fixed local-header prefix before the conventional central directory.
The prefix-bound classifier runs after M90 signatures but before decoded-name
policy, metadata, exact inventory, staging, or member reads. Failure emits
stable content-silent error `sample bundle local header prefixes are out of
bounds`; all owned resources close before control returns.

The fixed producer leaves room for the complete prefix at all 50 offsets. M91
adds no local-header field parser, filename/extra-length interpretation,
record-extent, payload-bound, adjacency, contiguity, or physical non-overlap
rule, no inter-member layout validator, workflow, dependency, runtime API,
release authority, or producer change. This profile is not a general archive
sandbox and is not a real public release observation.

M92/RFC-0075 reads exactly the local file-name and extra-field length
declarations after M91 prefix policy. The two-field envelope-bound classifier
requires each `header_offset + 30 + file_name_length + extra_field_length` to
be no greater than the conventional central-directory offset before decoded-
name policy, metadata, exact inventory, staging, or member reads. Failure emits
stable content-silent error `sample bundle local header envelopes are out of
bounds`; all owned resources close before control returns.

The fixed producer's 50 local-header variable envelopes all end before the
directory. M92 performs no local-name comparison, extra-field parsing, next-
header or payload bound, adjacency, contiguity, physical non-overlap rule, or
inter-member layout validation, workflow, dependency, runtime API, release
authority, or producer change. This profile is not a general archive sandbox
and is not a real public release observation.

M93/RFC-0076 reads each bounded local file-name after M92 policy and requires
its bytes to equal the parser-exposed central `orig_filename` reconstructed
with UTF-8 when the central language-encoding flag is set and CP437 otherwise.
The one raw local-name consistency classifier runs before decoded-name policy,
metadata, exact inventory, staging, or member reads. Failure emits stable
content-silent error `sample bundle local header names are inconsistent`; all
owned resources close before control returns.

The fixed producer's 50 local names match their corresponding central names.
M93 performs no local-flag comparison, extra-field comparison or parsing,
field-wide local/central consistency check, next-header or payload bound,
adjacency, contiguity, physical non-overlap rule, or inter-member layout
validation, workflow, dependency, runtime API, release authority, or producer
change. This profile is not a general archive sandbox and is not a real public
release observation.

M94/RFC-0077 reads the two-byte local general-purpose flag field after M93 name
consistency and requires exact equality with the parser-exposed central
`ZipInfo.flag_bits`. The one two-byte local-flag consistency classifier runs
before decoded-name policy, metadata, exact inventory, staging, or member
reads. Failure emits stable content-silent error `sample bundle local header
flags are inconsistent`; all owned resources close before control returns.

The fixed producer's 50 local flags match their corresponding central flags.
M94 performs no local compression-method comparison, no extra-field comparison
or parsing, no version/time/CRC/size or field-wide consistency check, no next-
header or payload bound, and no inter-member layout validator, workflow,
dependency, runtime API, release authority, or producer change. This profile
is not a general archive sandbox and is not a real public release observation.

M95/RFC-0078 reads the two-byte local compression-method field after M94 flag
consistency and requires exact equality with the parser-exposed central
`ZipInfo.compress_type`. The one two-byte local-compression-method consistency
classifier runs before decoded-name policy, metadata, exact inventory, staging,
or member reads. Failure emits stable content-silent error `sample bundle local
header compression methods are inconsistent`; all owned resources close before
control returns.

The fixed producer's 50 local methods match their corresponding central
methods. M95 performs no local extra-field comparison or parsing, no
version/time/CRC/size or field-wide consistency check, no method allowlist, no
next-header or payload bound, and no inter-member layout validator, workflow,
dependency, runtime API, release authority, or producer change. This profile is
not a general archive sandbox and is not a real public release observation.

M96/RFC-0079 reads each already bounded local extra field after M95 compression-
method consistency and requires exact equality with public central
`ZipInfo.extra`. The one bounded local-extra equality classifier runs before
decoded-name policy, metadata, exact inventory, staging, or member reads.
Failure emits stable content-silent error `sample bundle local header extra
fields are inconsistent`; all owned resources close before control returns.

The fixed producer's 50 local and central extras are matching and empty. M96
adds no extra-field semantics parser, broad extra-field ban, new field-ID
policy, version/time/CRC/size or field-wide consistency check, next-header or
payload bound, inter-member layout validator, workflow, dependency, runtime
API, release authority, or producer change. This profile is not a general
archive sandbox and is not a real public release observation.

M97/RFC-0080 reads the bounded two-byte local extraction-version pair after
M96 local-extra equality and requires it to match public central
`ZipInfo.extract_version` and `ZipInfo.reserved`. This one two-byte local-
extraction-version consistency classifier runs before decoded-name policy,
metadata, exact inventory, staging, or member reads. Failure emits stable
content-silent error `sample bundle local header extraction versions are
inconsistent`; all owned resources close before control returns.

The fixed producer's 50 local and central pairs match at `(20, 0)`. M97 adds
no supported-version allowlist, time/CRC/size comparison, field-wide
consistency check, next-header or payload bound, inter-member layout validator,
workflow, dependency, runtime API, release authority, or producer change. This
profile is not a general archive sandbox and is not a real public release
observation.

M98/RFC-0081 reads the bounded four-byte local DOS timestamp after M97 and
requires it to match the bytes represented by public central
`ZipInfo.date_time`. This one four-byte local-timestamp consistency classifier
runs before decoded-name policy, metadata, exact inventory, staging, or member
reads. Failure emits stable content-silent error `sample bundle local header
timestamps are inconsistent`; all owned resources close before control
returns.

The fixed producer's 50 local and central timestamps match. M98 is no
timestamp semantics validator and adds no timezone or UTC conversion,
wall-clock comparison, calendar or reproducibility rule, extended-timestamp
interpretation, CRC/size comparison, field-wide consistency check, next-header
or payload bound, inter-member layout validator, workflow, dependency, runtime
API, release authority, or producer change. This profile is not a general
archive sandbox and is not a real public release observation.

M99/RFC-0082 reads the bounded four-byte local CRC-32 after M98 and requires it
to match public central `ZipInfo.CRC` encoded little-endian. This one four-byte
local-CRC-32 consistency classifier runs before decoded-name policy, metadata,
exact inventory, staging, or member reads. Failure emits stable content-silent
error `sample bundle local header CRC-32 values are inconsistent`; all owned
resources close before control returns.

The fixed producer's 50 local and central CRC values match. M99 performs no CRC
recomputation, payload-integrity certification, compressed/uncompressed size
comparison, field-wide consistency check, payload or next-header bound, or
inter-member layout validator, workflow, dependency, runtime API, release
authority, or producer change. This profile is not a general archive sandbox
and is not a real public release observation.

M100/RFC-0083 reads the bounded four-byte local compressed size after M99 and
requires it to match public central `ZipInfo.compress_size` encoded little-
endian. This one four-byte local-compressed-size consistency classifier runs
before decoded-name policy, metadata, exact inventory, staging, or member
reads. Failure emits stable content-silent error `sample bundle local header
compressed sizes are inconsistent`; all owned resources close before control
returns.

The fixed producer's 50 local and central compressed sizes match. M100 performs
no decompression or recompression, no uncompressed-size comparison, no
compression-ratio policy, no field-wide consistency check, no payload or next-
header bound, and no inter-member layout validator, workflow, dependency,
runtime API, release authority, or producer change. This profile is not a
general archive sandbox and is not a real public release observation.

M101/RFC-0084 reads the bounded four-byte local uncompressed size after M100
and requires it to match public central `ZipInfo.file_size` encoded little-
endian. This one four-byte local-uncompressed-size consistency classifier runs
before decoded-name policy, metadata, exact inventory, staging, or member
reads. Failure emits stable content-silent error `sample bundle local header
uncompressed sizes are inconsistent`; all owned resources close before control
returns.

The fixed producer's 50 local and central uncompressed sizes match. M101
performs no decompression or recompression, no payload-content read during
preflight, no compression-ratio policy, no field-wide consistency check, no
payload or next-header bound, and no inter-member layout validator, workflow,
dependency, runtime API, release authority, or producer change. This profile is
not a general archive sandbox and is not a real public release observation.

M102/RFC-0085 calculates each compressed payload end after M101 and requires it
not to exceed the next ordered local header or conventional central directory.
This one compressed-payload upper-bound classifier runs before decoded-name
policy, metadata, exact inventory, staging, or member reads. Failure emits
stable content-silent error `sample bundle member payloads are out of bounds`;
all owned resources close before control returns.

The fixed producer's 50 payloads end exactly at their next header or directory
limit. M102 performs no decompression or recompression, reads no payload
content, adds no exact-contiguity requirement, no gap or adjacency ban, no
compression-ratio policy, no payload-integrity certification, workflow,
dependency, runtime API, release authority, or producer change. This profile is
not a general archive sandbox and is not a real public release observation.

M103/RFC-0086 requires each compressed payload end to equal the next ordered
local header or conventional central directory. This exact compressed-payload
contiguity preflight is one compressed-payload equality classifier after M102
and before decoded-name policy, metadata, exact inventory, staging, or member
reads. Failure emits stable content-silent error `sample bundle member payloads
are not contiguous`; M102 retains overlap precedence and all owned resources
close before control returns.

The fixed producer's 50 payloads already end exactly at their next limit. M103
performs no decompression or recompression, reads no payload content, and makes
no payload-integrity certification. It adds no workflow, dependency, runtime
API, release authority, or producer change, is not a general archive sandbox,
and is not a real public release observation.

M104/RFC-0087 requires public central `ZipInfo.extra` to be empty after
established Unicode Path, ZIP64, local/central consistency, payload-bound, and
contiguity checks. This empty sample-member extra-field profile preflight is one
central-extra emptiness classifier before decoded-name policy, metadata, exact
inventory, staging, or member reads. Failure emits stable content-silent error
`sample bundle contains an unsupported extra field`; established specific and
layout errors retain precedence and all owned resources close before control
returns.

The fixed producer's 50 members already have empty extra fields. M104 adds no
extra-field semantics parser, field-ID registry, payload-content read,
decompression, recompression, or general ZIP validity claim. It adds no
workflow, dependency, runtime API, release authority, or producer change, is
not a general archive sandbox, and is not a real public release observation.

M105/RFC-0088 requires public central `ZipInfo.flag_bits` to equal zero after
established specific-flag, local/central consistency, payload-layout, and M104
extra-field checks. This zero sample-member general-purpose-flag profile
preflight is one central-flag zero-profile classifier after decoded-name and
member-metadata policy but before exact inventory, staging, or member reads.
Failure emits stable content-silent error `sample bundle contains unsupported
general-purpose flags`; established specific, codec, path, and layout errors
retain precedence and all owned resources close before control returns.

The fixed producer's 50 members already have zero general-purpose flags. M105
adds no flag-semantics parser, bit registry, payload-content read,
decompression, recompression, or general ZIP validity claim. It adds no
workflow, dependency, runtime API, release authority, or producer change, is
not a general archive sandbox, and is not a real public release observation.

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
