# Security Policy

## Supported versions

LudoWeave `0.1.0a1` is a community-alpha candidate, not a long-term support line. Security fixes are applied on a best-effort basis to the default branch and the current alpha until a version-support policy is announced. Older development snapshots are unsupported.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability.

Use the repository's **Security** tab and choose **Report a vulnerability** to create a private GitHub security advisory. Include the affected revision, impact, reproduction steps, and any suggested mitigation. Do not include unrelated secrets or personal data.

If private vulnerability reporting is unavailable, use GitHub Support to contact the repository owner rather than disclosing the report publicly.

Maintainers will acknowledge the report through the same private channel, assess impact, coordinate a fix when warranted, and credit reporters who request attribution. No response or remediation deadline is guaranteed during community alpha.

## Release supply chain

- The baseline wheel has no runtime dependencies and is built as `py3-none-any`.
- Release candidates include SHA-256 checksums, an SPDX SBOM, Apache/project notices, and a versioned manifest.
- The tag workflow uses immutable action revisions and grants write, identity-token, and attestation permissions only to the release job.
- M39 requires the exact release ref to be an annotated tag whose signature
  GitHub reports as valid, whose local/GitHub target is the checked-out commit,
  and whose commit is reachable from `origin/main`. The validator is loaded
  from fetched `origin/main`, not from the unadmitted tag checkout.
- Official tagged artifacts receive GitHub build-provenance and SBOM attestations. Consumers should verify both the local checksums and hosted attestations as documented in `docs/release-process.md`.
- M40 keeps the GitHub release as an unpublished prerelease draft while the
  workflow verifies that every authenticated API asset is fully uploaded and
  exactly matches local staging by safe name, byte size, and SHA-256 digest.
  Failed verification leaves the draft for inspection and never clobbers an
  existing asset.
- M41 also requires the authenticated draft's source `body` to exactly match
  bounded staged `RELEASE_NOTES.md` before publication. It rejects missing,
  null, substituted, truncated, or normalization-different notes without
  emitting their content.
- M42 retains the exact authenticated release database ID across publication
  and rechecks the final public prerelease state, valid UTC publication time,
  notes, and assets before the release job can succeed.
- M43 retrieves every validated numeric asset ID through the authenticated
  binary asset endpoint and rehashes the complete downloaded set against the
  same published release document before the release job can succeed.
- M44 then verifies SLSA v1 provenance for every retrieved asset and an SPDX
  2.3 SBOM attestation for the one pure wheel, constrained to the exact
  repository, tag, source/signer commit, release workflow, GitHub OIDC issuer,
  hosted runner class, and bounded candidate count.
- M45 then fetches the exact public release and asset IDs without supplying a
  GitHub credential, revalidates the bounded downloaded set, and runs complete
  isolated release smoke against those public bytes.
- M46 repeats the bounded public retrieval and installed smoke from a dependent
  fresh Linux runner with read-only contents permission. It retrieves the exact
  admitted candidate through the pinned same-workflow artifact channel and
  supplies no release credential to public HTTP requests.
- M47 replaces the Bash-only verifier with one typed standard-library Python
  program and expands that tag-only fresh rehearsal to Ubuntu, Windows, and
  macOS. Each runner creates its own bounded plan and isolated installation;
  all retain read-only contents permission and credential-free public requests.
- M48 requires a direct `200` release document and only documented `200`/`302`
  asset handling, confines the API-version header to `api.github.com`, refreshes
  socket timeouts before headers/body reads, and separates timeout,
  transport/protocol, and local-output failure codes.
- M49 explicitly connects and inspects the actual port-443 TLS peer before
  sending each fixed API or redirected asset request. Only globally reachable
  unicast IPv4/IPv6 is accepted; mapped IPv6 uses its embedded IPv4 identity.
- M50 creates an explicit verified TLS client context per hop, retains system
  server-auth trust and TLS 1.2-or-newer certificate/hostname validation, and
  prevents ambient `SSLKEYLOGFILE` from enabling session-secret logging or
  creating its target.
- M51 advertises only HTTP/1.1 and validates the actual negotiated session
  before every request: exactly TLSv1.2 or TLSv1.3, a well-formed cipher report
  with at least 128 secret bits, no TLS compression, and ALPN `http/1.1` or no
  negotiated ALPN.
- M52 validates the socket's URL-derived TLS service identity before the M51
  session check: its observed IDNA-normalized reference hostname must match and
  its verified peer certificate must be available as non-empty DER bytes.
- M53 validates after the handshake that the actual socket retains the exact
  context supplied for that hop and has an exactly client-side role, then
  revalidates the complete M50 context policy before M52, M51, or any request.
  Every redirect repeats the exact context binding check independently.
- M54 validates after the handshake and M53 binding that the actual socket's
  `session_reused` observation is exactly `False` before service identity,
  negotiated-session inspection, or any request. Every redirect repeats the
  freshness check independently.
- M55 validates documented HTTP/1.1-class response metadata on every response
  before status, redirect, or body use. The public version value must be integer
  `11`; this does not prove an exact raw status-line token because CPython may
  normalize another `HTTP/1.x` value. `Transfer-Encoding` must be absent or
  exactly `chunked` case-insensitively, cannot coexist with `Content-Length`,
  and any present content length remains a string for existing bounded checks.
- M56 requires each response status to be a non-boolean integer from 100
  through 599. Each followed `302` must expose exactly one Location field whose
  value is a single URI-reference of at most 8,000 ASCII octets with complete
  percent escapes. Bracket delimiters are accepted only within a parsed
  authority, never its path, query, or fragment; the resolved URL repeats the
  existing bounded HTTPS, peer, TLS, framing, size, and exact-byte checks before
  use.
- M57 requires every successful response body read to return immutable bytes
  no larger than the requested amount before EOF handling or local output. If
  `Content-Length` exists, the declared value must equal the streamed octets;
  malformed read shapes use a content-silent request failure and length
  disagreement remains a size mismatch.
- M58 requires response close before connection close, both close attempts even
  when the first fails, and preservation of the primary failure. Redirect
  continuation and separate partial publication occur only after successful
  cleanup. It provides no rollback and makes no workflow or release-authority
  change.
- M60 treats every pre-existing fresh-output directory entry, including a
  dangling link, as a filesystem collision before network or validator side
  effects. Path-inspection failures remain content-silent, and exclusive
  creation plus hard-link publication retain no clobber behavior. This is no
  race-free filesystem guarantee and makes no workflow or release-authority
  change.
- M61 treats the candidate directory as read-only: the strictly resolved output
  root cannot equal or descend from it, including through a resolved alias,
  before network or validator work. Filesystem-identity comparison also catches
  differently spelled aliases on a case-insensitive filesystem. Resolution and
  identity-inspection failures are content-silent. This is no race-free
  filesystem guarantee and makes no workflow or release-authority change.
- M62 admits only a deterministic portable asset name in the public-release
  retrieval plan: at most 255 ASCII characters, no trailing period or Windows
  device stem, and case-insensitive uniqueness. Invalid plans fail before asset
  download or output-directory creation. This uses no filesystem probing and
  makes no workflow or release-authority change.
- M63 confines subordinate stdout and subordinate stderr during the public
  release validator and complete smoke calls. Success emits one JSON document;
  subordinate success requires an exact zero integer, while invalid status and
  admitted failure remain content-silent. The process-global stream redirection
  is limited to this single-thread utility and makes no workflow or release-
  authority change.
- M64 preflights a staged sample bundle before extraction, rejecting more than
  256 members, any member over 1 MiB, or more than 8 MiB total declared
  expansion. Admitted members stream in 64 KiB blocks with exact copied-size
  validation. Only stored and deflated codecs are admitted because CPython's
  BZIP2/LZMA paths do not provide the same bounded-output read behavior. This
  is not a general archive sandbox, transactional cleanup guarantee, workflow
  change, or real public release observation.
- M65 admits only a portable sample member path beneath the expected bundle
  root: at most 255 ASCII characters, portable components without Windows
  device stems or trailing periods, case-insensitive uniqueness, one ancestor
  spelling, no explicit directory member, no explicitly encoded non-regular
  file type, and no file/directory prefix collision. ZIP members that omit file-
  type mode bits remain admitted for common-producer compatibility. Violations
  fail before extraction. This performs no Unicode normalization or filesystem
  probing and is not a general archive sandbox, workflow change, or real public
  release observation.
- M66 requires an existing runner-owned output directory and an absent final
  sample root. It extracts into a same-filesystem temporary staging directory,
  rejects an incomplete staged set, and uses a single rename only after
  validation. Failure cleanup removes the partial owned stage and preserves the
  final path, while any final entry that already exists remains untouched. This
  is not crash-durable, provides no concurrent filesystem race isolation, adds
  no workflow or release authority, and is not a real public release
  observation.
- M67 requires the exact sample-bundle inventory of 50 regular files after the
  complete metadata/path preflight and before extraction. An unexpected member
  or missing member fails with one content-silent category before any archive
  member is opened. The expectation is source-defined independently of the
  unchanged sample producer. This is not content scanning or a general archive
  sandbox, adds no workflow or release authority, and is not a real public
  release observation.
- M68 rejects an obvious non-regular or oversized sample archive from path
  metadata before opening it, then requires the opened descriptor to identify
  a regular file no larger than 16 MiB before `ZipFile` construction. Parsing
  uses that same handle. Invalid containers fail content-silently before
  central-directory parsing or staging. This does not
  make later bytes immutable or replace expanded-size controls, is not a
  general archive sandbox, adds no workflow or release authority, and is not a
  real public release observation.
- M69 rejects ZIP general-purpose bit flags for traditional encryption,
  strong encryption, and masked header values during complete sample-member
  preflight. The stable content-silent failure occurs before member reads,
  password handling, or staging. No password or decryption path is added; this
  is not a general archive sandbox, adds no workflow or release authority, and
  is not a real public release observation.
- M70 binds sample extraction to the sample digest already admitted from
  `SHA256SUMS`. The same opened handle is hashed before ZIP parsing and again
  before publication, with persistent mismatch failing content-silently and
  partial owned staging cleaned. This creates no immutable-input guarantee,
  is not a general archive sandbox, adds no workflow or sample producer
  change, and is not a real public release observation.
- M71 copies the bounded source into one owned checksum-admitted snapshot and
  gives that spooled temporary file to `ZipFile`. Parsing therefore consumes
  the exact bytes whose digest matched `SHA256SUMS`; later source changes cannot
  alter parser input. This adds no persistent copy or source-immutability
  guarantee, is not a general archive sandbox, adds no workflow or sample
  producer change, and is not a real public release observation.
- M72 maps documented `BadZipFile` and `LargeZipFile` failures from the private
  sample parser to one stable content-silent error. Archive-controlled detail
  remains programmatic context but suppressed context keeps it out of rendered
  output; owned cleanup completes first. Verifier policy errors remain
  specific. This is not a general archive sandbox, adds no workflow or sample
  producer change, and is not a real public release observation.
- M73 adds exactly `UnicodeDecodeError` from archive-controlled UTF-8 names in
  the ZIP central directory or local header to M72's stable content-silent
  error. Suppressed context hides invalid bytes, offsets, and codec detail from
  rendered output after owned cleanup while retaining the original exception
  programmatically. Other Unicode, value, policy, filesystem, and unexpected
  failures remain specific. This is not a general archive sandbox, adds no
  workflow or sample producer change, and is not a real public release
  observation.
- M74 adds exactly `zlib.error` from checksum-admitted deflated sample members
  to the same stable content-silent error. Suppressed context hides the
  decompressor diagnostic from rendered output after owned cleanup while
  retaining the original exception programmatically. EOF, policy, filesystem,
  and unexpected failures remain specific. This is not a general archive
  sandbox, adds no workflow or sample producer change, and is not a real public
  release observation.
- M75 rejects compressed patched data, ZIP general-purpose bit 5, during the
  all-member preflight before inventory validation, member reads, or staging.
  The stable policy error contains no archive-controlled member identity;
  M69's encryption category retains precedence. This adds no broad flag
  allowlist, workflow, or sample producer change, is not a general archive
  sandbox, and is not a real public release observation.
- M76 rejects enhanced deflating when central-directory ZIP general-purpose bit
  4 is paired with compression method 8. The stable content-silent policy error
  occurs before inventory validation, member reads, or staging; earlier
  encryption and compressed-patch categories retain precedence. Stored members
  and local-header inconsistencies remain outside this exact decision. This
  adds no broad flag allowlist, workflow, or sample producer change, is not a
  general archive sandbox, and is not a real public release observation.
- M77 inspects decoded `ZipInfo.orig_filename` and rejects an exact NUL byte
  before member metadata, inventory validation, member reads, or staging. The
  content-silent category prevents a hidden suffix from entering diagnostics;
  established flag errors retain precedence. This adds no general normalized-
  name comparison, no raw parser, workflow, or sample producer change, is not
  a general archive sandbox, and is not a real public release observation.
- M78 rejects exact ZIP general-purpose bit 3, the data-descriptor indicator,
  in a separate archive-wide preflight before member reads or staging. The
  content-silent error follows established M69/M75/M76 flag categories and
  precedes NUL-name policy. This is no raw descriptor parser or broad flag
  allowlist, changes no workflow or sample producer, is not a general archive
  sandbox, and is not a real public release observation.
- M79 rejects exact Info-ZIP Unicode Path extra-field ID `0x7075` in a
  separate archive-wide preflight before member reads or staging. The stable
  content-silent error follows every established flag category and precedes
  decoded-name policy. This bounded extra-field walk is no broad extra-field
  ban, changes no workflow or sample producer, is not a general archive
  sandbox, and is not a real public release observation.
- M80 rejects exact PKWARE ZIP64 extended-information extra-field ID `0x0001`
  in a separate archive-wide preflight after M79 policy and before decoded-
  name policy, metadata, inventory, member reads, or staging. The bounded
  extra-field walk fails content-silently. This is no broad extra-field ban or
  raw ZIP64 parser, changes no workflow or sample producer, is not a general
  archive sandbox, and is not a real public release observation.
- M81 rejects parser-exposed non-empty ZIP archive and member comments in
  separate preflights after established flag/extra-field policy and before
  decoded-name policy,
  metadata, inventory, member reads, or staging. Both errors are content-
  silent. This adds no raw ZIP parser or general comment scanner, changes no
  workflow or sample producer, is not a general archive sandbox, and is not a
  real public release observation.
- M82 rejects parser-exposed nonzero `ZipInfo.volume` values in a separate all-
  member pass after established comment policy and before decoded-name policy,
  metadata, inventory, member reads, or staging. The error `sample bundle uses
  a split-volume member` is content-silent. This adds no raw end-record parser
  and no multi-volume assembler, changes no workflow or sample producer, is
  not a general archive sandbox, and is not a real public release observation.
- M83 reads exactly the final conventional 22-byte end-of-central-directory
  record after all established flag, extra-field, comment, and member-volume
  preflights. Either nonzero disk field raises content-silent error `sample
  bundle uses unsupported archive disk fields` before decoded-name policy,
  metadata, inventory, member reads, or staging. The fixed producer emits both
  fields as zero. This adds no ZIP64 end-record parser, end-record search, or
  multi-volume assembler, changes no workflow or producer, is not a general
  archive sandbox, and is not a real public release observation.
- M84 requires both conventional end-of-central-directory entry counts to
  equal the standard reader's parsed member count after M83 disk policy and
  before decoded-name policy, metadata, inventory, member reads, or staging.
  The error `sample bundle archive entry counts are inconsistent` is content-
  silent. This adds no ZIP64 end-record parser, sentinel resolution, or multi-
  volume assembler, changes no workflow or producer, is not a general archive
  sandbox, and is not a real public release observation.
- M85 requires the final conventional central-directory size plus offset to
  equal the absolute final end-of-central-directory record offset after M84
  entry-count policy and before decoded-name policy, metadata, inventory,
  member reads, or staging. The error `sample bundle central directory
  placement is inconsistent` is content-silent. This adds no central-directory
  record parser, prepended executable support, self-extracting archive support,
  or multi-volume assembler, changes no workflow or producer, is not a general
  archive sandbox, and is not a real public release observation.
- M86 requires the minimum parser-exposed `ZipInfo.header_offset` to be zero
  after M85 placement policy and before decoded names, metadata, inventory,
  staging, or reads. The content-silent error is `sample bundle first local
  header placement is inconsistent`. This adds no local-header parser, inter-
  member layout validator, workflow, dependency, producer, runtime API, or
  release authority; it is not a general archive sandbox or a real public
  release observation.
- M87 requires all parser-exposed local-header offsets to be distinct after
  M86 first-offset policy and before decoded names, metadata, inventory,
  staging, or reads. The content-silent error is `sample bundle local header
  offsets are inconsistent`. This adds no local-header parser, offset ordering/
  bounds rule, inter-member layout validator, workflow, dependency, producer,
  runtime API, or release authority; it is not a general archive sandbox or a
  real public release observation.
- M88 requires strictly increasing local-header offsets in parser-exposed
  archive order after M87 distinctness and before decoded names, metadata,
  inventory, staging, or reads. The content-silent error is `sample bundle
  local header offsets are out of order`. This fixed-producer rule adds no
  local-header parser, central-directory record parser, bounds/contiguity rule,
  inter-member layout validator, workflow, dependency, producer, runtime API,
  or release authority; it is not a general archive sandbox and is not a real
  public release observation.
- M89 requires every parser-exposed local-header offset to remain strictly
  before the conventional central directory after M88 ordering and before
  decoded names, metadata, inventory, staging, or reads. The content-silent
  error is `sample bundle local header offsets are out of bounds`. This fixed-
  producer rule adds no local-header parser, central-directory record parser,
  local-record extent rule, inter-member layout validator, workflow,
  dependency, producer, runtime API, or release authority; it is not a general
  archive sandbox and is not a real public release observation.
- M90 requires the four-byte local-header signature at every parser-exposed
  offset after M89 bounds and before decoded names, metadata, inventory,
  staging, or reads. The content-silent error is `sample bundle local header
  signature is inconsistent`. This fixed-producer signature classifier adds
  no local-header field parser, no inter-member layout validator, workflow,
  dependency, producer, runtime API, or release authority; it is not a general
  archive sandbox and is not a real public release observation.
- M91 requires room for the 30-byte fixed local-header prefix at every parser-
  exposed offset after M90 signatures and before decoded names, metadata,
  inventory, staging, or reads. Its content-silent error is `sample bundle
  local header prefixes are out of bounds`. This prefix-bound classifier adds
  no local-header field parser, no inter-member layout validator, workflow,
  dependency, producer, runtime API, or release authority; it is not a general
  archive sandbox and is not a real public release observation.
- M92 reads exactly the local file-name and extra-field length declarations
  after M91, then requires each local-header variable envelope to end no later
  than the conventional central directory before decoded names, metadata,
  inventory, staging, or reads. Its content-silent error is `sample bundle
  local header envelopes are out of bounds`. This two-field envelope-bound
  classifier performs no local-name comparison, extra-field parsing, next-
  header or payload bound, inter-member layout validation, workflow,
  dependency, producer, runtime API, or release-authority change; it is not a
  general archive sandbox and is not a real public release observation.
- M93 reads each already bounded local file-name and requires its bytes to
  match the parser-exposed central name reconstructed with the central UTF-8
  flag or default CP437 encoding before decoded names, metadata, inventory,
  staging, or reads. Its content-silent error is `sample bundle local header
  names are inconsistent`. This one raw local-name consistency classifier
  performs no local-flag comparison, extra-field comparison, next-header or
  payload bound, inter-member layout validation, workflow, dependency,
  producer, runtime API, or release-authority change; it is not a general
  archive sandbox and is not a real public release observation.
- M94 reads each two-byte local general-purpose flag field after M93 and
  requires exact equality with the parser-exposed central `ZipInfo.flag_bits`
  before decoded names, metadata, inventory, staging, or reads. Its content-
  silent error is `sample bundle local header flags are inconsistent`. This
  one two-byte local-flag consistency classifier performs no local compression-
  method comparison, no extra-field comparison, no inter-member layout
  validator, workflow, dependency, producer, runtime API, or release-authority
  change; it is not a general archive sandbox and is not a real public release
  observation.
- M95 reads each bounded two-byte local compression method after M94 and
  requires exact equality with the parser-exposed central
  `ZipInfo.compress_type` before decoded names, metadata, inventory, staging,
  or reads. Its content-silent error is `sample bundle local header compression
  methods are inconsistent`. This one two-byte local-compression-method
  consistency classifier performs no local extra-field comparison, no
  version/time/CRC/size comparison, no inter-member layout validator, workflow,
  dependency, producer, runtime API, or release-authority change; it is not a
  general archive sandbox and is not a real public release observation.
- M96 reads each bounded local extra field after M95 and requires exact
  equality with public central `ZipInfo.extra` before decoded names, metadata,
  inventory, staging, or reads. Its content-silent error is `sample bundle
  local header extra fields are inconsistent`. This one bounded local-extra
  equality classifier adds no extra-field semantics parser, broad extra-field
  ban, version/time/CRC/size comparison, inter-member layout validator,
  workflow, dependency, producer, runtime API, or release-authority change; it
  is not a general archive sandbox and is not a real public release
  observation.
- M97 reads each bounded two-byte local extraction-version pair after M96 and
  requires exact equality with public central `ZipInfo.extract_version` and
  `ZipInfo.reserved` before decoded names, metadata, inventory, staging, or
  reads. Its content-silent error is `sample bundle local header extraction
  versions are inconsistent`. This one two-byte local-extraction-version
  consistency classifier adds no supported-version allowlist, no
  time/CRC/size comparison, no inter-member layout validator, workflow,
  dependency, producer, runtime API, or release-authority change; it is not a
  general archive sandbox and is not a real public release observation.
- M98 reads each bounded four-byte local DOS timestamp after M97 and requires
  exact equality with the bytes represented by public central
  `ZipInfo.date_time` before decoded names, metadata, inventory, staging, or
  reads. Its content-silent error is `sample bundle local header timestamps are
  inconsistent`. This one four-byte local-timestamp consistency classifier is
  no timestamp semantics validator, performs no timezone or UTC conversion,
  adds no CRC/size comparison or inter-member layout validator, and changes no
  workflow, dependency, producer, runtime API, or release authority; it is not
  a general archive sandbox and is not a real public release observation.
- M99 reads each bounded four-byte local CRC after M98 and requires exact
  equality with public central `ZipInfo.CRC` before decoded names, metadata,
  inventory, staging, or reads. Its content-silent error is `sample bundle
  local header CRC-32 values are inconsistent`. This one four-byte local-CRC-32
  consistency classifier performs no CRC recomputation, payload-integrity
  certification, compressed/uncompressed size comparison, payload or next-
  header bound, or inter-member layout validator, and changes no workflow,
  dependency, producer, runtime API, or release authority; it is not a general
  archive sandbox and is not a real public release observation.
- M100 reads each bounded four-byte local compressed size after M99 and
  requires exact equality with public central `ZipInfo.compress_size` before
  decoded names, metadata, inventory, staging, or reads. Its content-silent
  error is `sample bundle local header compressed sizes are inconsistent`.
  This one four-byte local-compressed-size consistency classifier performs no
  decompression or recompression, no uncompressed-size comparison, no payload
  or next-header bound, and no inter-member layout validator, and changes no
  workflow, dependency, producer, runtime API, or release authority; it is not
  a general archive sandbox and is not a real public release observation.
- M101 reads each bounded four-byte local uncompressed size after M100 and
  requires exact equality with public central `ZipInfo.file_size` before
  decoded names, metadata, inventory, staging, or reads. Its content-silent
  error is `sample bundle local header uncompressed sizes are inconsistent`.
  This one four-byte local-uncompressed-size consistency classifier performs no
  decompression or recompression, no compression-ratio policy, no payload or
  next-header bound, and no inter-member layout validator, and changes no
  workflow, dependency, producer, runtime API, or release authority; it is not
  a general archive sandbox and is not a real public release observation.
- M102 calculates each compressed payload end after M101 and requires it not to
  exceed the next ordered local header or conventional central directory before
  decoded names, metadata, inventory, staging, or reads. Its content-silent
  error is `sample bundle member payloads are out of bounds`. This one
  compressed-payload upper-bound classifier performs no decompression or
  recompression, adds no exact-contiguity requirement, no gap or adjacency ban,
  and no payload-integrity certification, and changes no workflow, dependency,
  producer, runtime API, or release authority; it is not a general archive
  sandbox and is not a real public release observation.
- M103 requires each compressed payload end to equal the next ordered local
  header or conventional central directory after M102 and before decoded names,
  metadata, inventory, staging, or reads. Its content-silent error is `sample
  bundle member payloads are not contiguous`. This exact compressed-payload
  contiguity preflight is one compressed-payload equality classifier with no
  decompression or recompression, no payload-content read, and no payload-
  integrity certification. It changes no workflow, dependency, producer,
  runtime API, or release authority; it is not a general archive sandbox and is
  not a real public release observation.
- M104 requires public central `ZipInfo.extra` to be empty after established
  Unicode Path, ZIP64, local/central consistency, payload-bound, and contiguity
  checks and before decoded names, metadata, inventory, staging, or reads. Its
  content-silent error is `sample bundle contains an unsupported extra field`.
  This empty sample-member extra-field profile preflight is one central-extra
  emptiness classifier with no extra-field semantics parser and no payload-
  content read. It changes no workflow, dependency, producer, runtime API, or
  release authority; it is not a general archive sandbox and is not a real
  public release observation.
- M105 requires public central `ZipInfo.flag_bits` to equal zero after
  established specific-flag, local/central consistency, payload-layout, and
  M104 extra-field checks, then after decoded names and member metadata but
  before exact inventory, staging, or reads. Its content-silent error is
  `sample bundle contains unsupported general-purpose flags`. This zero sample-
  member general-purpose-flag profile preflight is one central-flag zero-
  profile classifier with no flag-semantics parser and no payload-content read.
  It changes no workflow,
  dependency, producer, runtime API, or release authority; it is not a general
  archive sandbox and is not a real public release observation.
- M106 requires public central `ZipInfo.reserved` to equal zero after M105 and
  before exact inventory, staging, or reads. Its content-silent error is
  `sample bundle has a nonzero extraction-version reserved byte`. This zero
  sample-member extraction-version reserved-byte profile preflight is one
  central-reserved zero-profile classifier with no extraction-version semantics
  parser and no payload-content read. It changes no workflow, dependency,
  producer, runtime API, or release authority; it is not a general archive
  sandbox and is not a real public release observation.
- M107 requires public central `ZipInfo.extract_version` to equal `20` after
  M106 and before exact inventory, staging, or reads. Its content-silent error
  is `sample bundle has an unsupported extraction version`. This exact sample-
  member extraction-version profile preflight is one central-extraction-version
  exact-profile classifier with no general extraction-version semantics parser
  and no payload-content read. It changes no workflow, dependency, producer,
  runtime API, or release authority; it is not a general archive sandbox and is
  not a real public release observation.
- M108 requires public central `ZipInfo.create_version` to equal `20` after
  M107 and before exact inventory, staging, or reads. Its content-silent error
  is `sample bundle has an unsupported creation version`. This exact sample-
  member creation-version profile preflight is one central-creation-version
  exact-profile classifier with no general creation-version semantics parser
  and no payload-content read. It changes no workflow, dependency, producer,
  runtime API, or release authority; it is not a general archive sandbox and is
  not a real public release observation.
- M109 requires public central `ZipInfo.internal_attr` to equal zero after M108
  and before exact inventory, staging, or reads. Its content-silent error is
  `sample bundle has unsupported internal attributes`. This zero sample-member
  internal-attribute profile preflight is one central-internal-attribute exact-
  profile classifier with no text/binary content interpretation and no payload-
  content read. It changes no workflow, dependency, producer, runtime API, or
  release authority; it is not a general archive sandbox and is not a real
  public release observation.
- M110 retains sample-member timestamp compatibility after an exact fixed-
  producer tuple caused 22 established architecture regressions. M98 continues
  to require local/central consistency, while the verifier performs no timezone
  or UTC conversion and no payload-content read. This is one central-timestamp
  compatibility decision, with no workflow, dependency, producer, runtime API,
  or release-authority change; it is not a general archive sandbox and is not a
  real public release observation.
- M111 retains sample-member permission compatibility. M65 continues to reject
  encoded symlinks and non-regular file types while admitting missing type bits
  and regular-file permission variants. This is one permission-bit
  compatibility decision with no exact external-attribute profile, no
  permission restoration, and no payload-content read. It changes no workflow,
  dependency, producer, runtime API, or release authority; it is not a general
  archive sandbox and is not a real public release observation.
- M112 retains sample-member creating-system compatibility. Standard-library
  host markers remain admitted while M65's existing encoded file-type boundary
  remains in force and the producer stays fixed at host `3`. This is one host-
  marker compatibility decision with no creating-system allowlist, no host-
  specific external-attribute interpretation, and no payload-content read. It
  changes no workflow, dependency, producer, runtime API, or release authority;
  it is not a general archive sandbox and is not a real public release
  observation.
- M113 retains sample-member compression-method compatibility. M64's exact
  stored/deflated allowlist and M95's local/central method agreement remain in
  force, while the fixed producer remains deflated. This is one compression-
  method compatibility decision with no exact deflate-only profile, no new
  decompressor, and no payload-content read. It changes no workflow,
  dependency, producer, runtime API, or release authority; it is not a general
  archive sandbox and is not a real public release observation.
- M114 retains sample-member compression-level non-observability. Reopened
  member metadata does not establish the exact writer configuration, so the
  verifier does not infer a compressor level from attributes, compressed bytes,
  or sizes. The fixed producer remains explicit at level `9`, while M105's zero
  flags and M113's method policy remain in force. This is one compression-level
  non-observability decision with no exact level-9 verifier profile, no inferred
  compressor level, and no payload-content read. It changes no workflow,
  dependency, producer, runtime API, or release authority; it is not a general
  archive sandbox and is not a real public release observation.
- M115 scopes sample-bundle byte reproducibility to the release environment.
  Repeated production within one fixed resolved environment remains the exact
  byte-identity claim; supported runtimes receive no cross-runtime byte-
  identity promise. This is one sample-bundle reproducibility-scope decision
  with no compressor-identity manifest field. It changes no workflow,
  allocation, dependency, producer, verifier, runtime API, or release
  authority; it is not a general reproducible-build claim and is not a real
  public release observation.
- M116 separates sample-bundle semantic portability from byte identity. The
  exact supported-runtime Windows producer-consumer matrix extracted the same
  fixed 50-file tree from both observed archive identities. This is one sample-
  bundle semantic-portability decision recording cross-runtime producer-
  consumer compatibility with no alternate compression method or cross-runtime
  byte-identity claim. It changes no workflow, allocation, dependency,
  producer, verifier, runtime API, or release authority; it is not a general
  ZIP interoperability claim and is not a real public release observation.
- M117 retains standard GIL CPython as the supported baseline after one exact
  Windows CPython 3.14.5t installed-wheel serial compatibility observation.
  The GIL-disabled probe preserved deterministic headless execution, explicit
  owner-thread rejection, and orderly close. It is one free-threaded serial-
  compatibility decision, not a support promise, and makes no concurrent-
  safety claim. It adds no graphics, performance, cross-platform, extension,
  workflow, allocation, dependency, runtime API, or release-authority change
  and is not a real public release observation.
- No PyPI trusted-publishing or upload step exists in community alpha.
- M26 release-channel evidence is offline and empty; it does not publish,
  download, resolve, or establish a supported release channel.
- M27 contributor-rehearsal evidence is offline and empty. Future reviewed
  evidence may contain a public login and project references, but must exclude
  email, private correspondence, credentials, prompts, telemetry, and other
  unpublished personal data.
- M39 does not define a signer/key allowlist, local trust store, or workflow-
  file self-authentication. Repository tag rules, deployment-environment
  approval, signing-key lifecycle, and workflow governance remain operational
  controls; report suspected unauthorized tag/workflow changes privately.
- M40 does not enable or claim immutable releases, independently verify GitHub
  storage, or replace build/SBOM attestations. Release immutability and failed-
  draft cleanup remain explicit repository operations.
- M41 compares the API source body, not GitHub's rendered Markdown; it does not
  validate links or factual completeness, sanitize maintainer-authored text, or
  replace human release review.
- M42 observes the authenticated state only after publication. Failure blocks
  a successful job result but does not automatically unpublish, delete, or
  mutate evidence, prevent later edits, or claim immutable-release policy.
- M43 writes only an exclusive bounded runner-temporary retrieval plan and new
  temporary download files. It neither clobbers nor mutates release assets and
  does not prove unauthenticated availability, all CDN/cache paths, future
  bytes, immutability, consumer installation, or attestation verification.
- M44 attestation identity and subject verification does not establish
  artifact security, an independent or trusted build, predicate truth beyond
  the constrained type/identity, future availability or non-revocation,
  immutable release state, consumer installation, or a supported channel.
- M45 observes one fixed public GitHub API path on the same hosted Linux runner.
  It does not establish an independent or external consumer, a clean-machine or
  cross-platform matrix, every browser/CDN/cache/geographic path, future
  availability, immutability, artifact security, PyPI, or a supported channel.
- M46 adds workspace/runner separation but remains inside the same GitHub-hosted
  workflow and uses scoped checkout/artifact services. M46 alone is not a
  cross-platform public matrix.
- M47 supplies the three supported hosted operating-system observations but
  remains inside the same workflow, repository, account, and provider. It is
  not independent or external verification, a clean machine outside that
  provider, every delivery path, future availability, immutability, artifact
  security, PyPI, or a supported channel.
- M48 hardens fixture-driven client behavior only. It adds no real public
  release observation, host/CDN allowlist claim, retry, cleanup, mutation,
  publication authority, or supported-channel evidence.
- M49 does not provide a hostname/IP allowlist, separate DNS preflight, DNSSEC,
  packet-level network sandbox, every-CDN result, real release observation,
  independent verification, retry, cleanup, mutation, or new authority.
- M50 does not replace system trust policy, add certificate pinning, disable
  platform trust configuration, inspect every negotiated cipher/session, or
  establish a real release observation or new release authority.
- M51 adds no cipher-name allowlist, custom trust, certificate/SPKI pin,
  revocation policy, TLS fingerprint, session-ticket policy, workflow,
  dependency, or release authority. Fixture checks are not a real public
  release observation or a claim about every TLS endpoint or future protocol.
- M52 does not parse or rematch certificates, add a pin/fingerprint allowlist,
  custom trust, certificate-chain export, revocation, OCSP/CRL, certificate-
  transparency, DNSSEC, workflow, dependency, or release authority. Its
  fixture checks are not a real public release observation or proof for every
  endpoint, certificate, delivery path, or future connection.
- M53 adds no custom trust, pinning, certificate/chain parser, revocation,
  session reuse, channel binding, proxy, network sandbox, workflow, dependency,
  or release authority. Its fixture checks are not a real public release
  observation or proof for every endpoint, context implementation, delivery
  path, or future connection.
- M54 adds no session cache, session assignment, ticket policy, TLS
  implementation introspection, trust replacement, pinning, workflow,
  dependency, or release authority. Its `session_reused` fixture checks are
  not a real public release observation or proof of a full handshake,
  certificate exchange, every endpoint, or future connection.
- M55 adds no private HTTP-response introspection, raw chunk parser, alternate
  client, HTTP/2 or HTTP/3, proxy, decompression, workflow, dependency, or
  release authority. Its framing fixtures are not a real public release
  observation, exact status-line evidence, or a general intermediary/request-
  smuggling defense.

## Initial security boundaries

- The M5 agent interface is local-only and provides no network listener or remote-control claim. MCP is confined to process stdio.
- The CLI performs no arbitrary Python evaluation.
- M2 artifact paths are bounded, project-relative, resolved beneath an explicitly selected project root, and reported only by stable roles in expected diagnostics.
- Input files are read through one bounded open handle; stale size metadata cannot cause an unbounded read.
- Project confinement protects normal workflows and static symlink/traversal mistakes. It is not a sandbox against a hostile local principal concurrently replacing files, directories, junctions, or symlinks inside the selected project tree; run commands only against a locally trusted, quiescent project directory.
- The M2 CLI project manifest is data-only and cannot select Python modules, callables, components, or plugins.
- M12 plugin manifests are exact-schema inert compatibility metadata. They do
  not discover, import, install, resolve, or execute code, and unknown
  executable fields fail closed.
- M16 adds no WASM runtime, loader, guest ABI, WASI context, host call, or mod
  package. Untrusted WebAssembly is not executed. ADR-0030 requires a complete
  least-privilege, resource, determinism, lifecycle, persistence, isolation,
  conformance, supply-chain, and maintenance gate before that boundary may
  change.
- Diagnostics must not expose environment variables or credentials.
- Agent-facing mutations are typed, validated, capability-gated, caller-attributed, serialized at safe points, and return canonical receipts. Write access is disabled by default.
- Agent requests, results, transactions, ticks, queries, snapshots, captures, tests, and call rates are bounded. Credential-shaped diagnostics and telemetry values are redacted.
- The MCP adapter cannot launch a shell, evaluate Python, load a module named by request data, or open a socket. Anyone able to launch the process and access its stdio has the capabilities granted by that composition root.

## Future executable-mod reports

Treat any unexpected plugin-driven import, execution, dynamic loading, WASM
instantiation, ambient filesystem/network/process access, or world mutation
without a canonical receipt as a security report. Also report any accepted
plugin-manifest field outside its documented exact schema. Use the private
reporting route above; do not attach hostile modules or sensitive files to a
public issue.

The [M16 WASM-mod security decision](docs/wasm-mod-security-decision.md)
records the prospective assets, actors, entry points, trust boundaries,
blocking findings, verification requirements, and residual risk. Its findings
are feature-admission blockers, not claims of a current executable-mod
vulnerability.

## Asset-cache cleanup boundary

LudoWeave has no asset-cache cleanup command or background collector. Existing
inventory, fingerprint, comparison, and unreferenced-preview records are
read-only aggregate integrity evidence and grant no deletion authority.

The accepted [asset-cache cleanup threat
model](docs/security/cache-cleanup-threat-model.md) covers TOCTOU races,
symlink/junction/reparse and hard-link substitution, concurrent readers and
writers, malformed or stale evidence, trusted-time rollback, crash recovery,
quarantine, replay, rollback tampering, and path privacy. A future implementation
must fail closed unless it proves handle-relative no-follow safety and complete
retained-root/quiescence semantics on the target platform.

The accepted [platform-capability
decision](docs/security/cache-cleanup-platform-capability-decision.md) records
that current portable CPython does not supply that complete mutation chain.
No platform is admitted for cleanup, and individual flags or a successful path-
based deletion must not be treated as capability evidence.

M149's test-only [Windows capability
probe](docs/security/cache-cleanup-windows-capability-probe.md) exercises one
owned handle chain beneath pytest temporary storage. It is feasibility evidence
only. The privilege-gated reparse case, filesystem coverage, concurrent
namespace attacks, cross-process exclusion, recovery, and durable receipts
remain unresolved, so Windows is still not admitted for cache mutation.

M150's test-only [Windows directory-junction
probe](docs/security/cache-cleanup-windows-junction-probe.md) executes one NTFS
reparse refusal without elevation. The retained-handle open refuses the
junction before traversal and explicit junction removal preserves the target.
This does not resolve symbolic links, other tags/filesystems, namespace races,
recovery, or mutation authority; Windows remains unadmitted.

M151's test-only [Windows retained-parent substitution
probe](docs/security/cache-cleanup-windows-retained-parent-substitution-probe.md)
renames an opened directory, rebinds its former name to a junction, and proves
that fresh traversal refuses the junction while the retained parent remains
bound to the original file identity. This same-process fixture is not
concurrency, locking, recovery, or mutation authority; Windows remains
unadmitted.

M152's test-only [Windows cross-process substitution
probe](docs/security/cache-cleanup-windows-cross-process-substitution-probe.md)
gives the fixed rename-plus-junction operation to a non-inheriting child process
while the parent retains the original directory handle. It proves one
cross-process namespace change, fresh-name refusal, and original-object identity
on the current host. It does not prove concurrency, exclusion, quiescence,
recovery, or mutation authority; Windows remains unadmitted.

M153's test-only [Windows share-delete exclusion
probe](docs/security/cache-cleanup-windows-share-delete-exclusion-probe.md)
omits delete sharing from one retained directory handle. One fixed child rename
fails without changing the namespace, and the identical rename succeeds after
the parent closes the blocking handle. This does not establish general
cross-process exclusion, controlled interleavings, oplock behavior, quiescence,
recovery, or mutation authority; Windows remains unadmitted.

M154's test-only [Windows native sharing-violation
probe](docs/security/cache-cleanup-windows-native-sharing-violation-probe.md)
replaces localized command diagnostics with one fixed isolated child's direct
`MoveFileExW` result. It observes false/error 32 before blocker close and
true/code zero afterward. Microsoft warns that exact native errors can vary by
system or driver, so this does not establish a universal error contract,
general exclusion, recovery, or mutation authority; Windows remains unadmitted.

M155's test-only [Windows child-owned share-delete
handshake](docs/security/cache-cleanup-windows-child-owned-share-delete-handshake.md)
makes a distinct process own and acknowledge the blocking handle lifecycle. A
separate native rename child observes false/error 32 while that owner remains
alive and true/code zero only after acknowledged close. This is one ordered
current-host transition, not a concurrent race, general exclusion, recovery,
or mutation authority; Windows remains unadmitted.

M156's test-only [Windows abrupt blocker-owner termination
probe](docs/security/cache-cleanup-windows-abrupt-blocker-termination-probe.md)
reuses that distinct owner but sends no graceful release token. The parent
forces termination, waits with a fixed bound, observes no close
acknowledgement, and retries the unchanged native rename once. This is one
current-host process-termination observation, not crash or restart recovery,
general exclusion, or mutation authority; Windows remains unadmitted.

M157's test-only [Windows blocker control-pipe EOF
probe](docs/security/cache-cleanup-windows-control-pipe-eof-probe.md) instead
closes only the parent control writer after readiness. The unchanged helper
closes its native handle in `finally`, exits with its fixed invalid-control
status, and emits no close acknowledgement before one identical rename retry.
This is not arbitrary pipe failure, recovery, general exclusion, or mutation
authority; Windows remains unadmitted.

M158's test-only [Windows blocker invalid-control-token
probe](docs/security/cache-cleanup-windows-invalid-control-token-probe.md)
writes and flushes exactly one fixed non-release byte after readiness. The
unchanged helper closes its native handle in `finally`, exits with its fixed
invalid-control status, and emits no close acknowledgement before one
identical rename retry. This is not arbitrary malformed input, partial or
multiple write behavior, broken-pipe recovery, general exclusion, or mutation
authority; Windows remains unadmitted.

M159's test-only [Windows blocker broken-control-pipe
probe](docs/security/cache-cleanup-windows-broken-control-pipe-probe.md) kills
and boundedly reaps the unchanged blocker before one direct late `WriteFile`.
The current host reports false/error 232 with zero bytes, the parent writer
closes explicitly, and one identical rename succeeds. This is not a universal
Windows error result, Python exception mapping, retry or recovery contract,
general exclusion, or mutation authority; Windows remains unadmitted.

M160's test-only [Windows live-blocker wait-timeout
probe](docs/security/cache-cleanup-windows-live-wait-timeout-probe.md) performs
one zero-duration wait after the unchanged blocker is ready. The wait raises
`TimeoutExpired`; the child and false/error 32 denial remain live until the
existing graceful close orders one successful rename. This is not a timeout
recovery contract, cancellation policy, general exclusion, or mutation
authority; Windows remains unadmitted.

M161's test-only [Windows acknowledged-release timeout
probe](docs/security/cache-cleanup-windows-acknowledged-release-timeout-probe.md)
uses separate fixed release-intent and close tokens. Exact `release-held`
acknowledges intent while retaining false/error 32 denial; one immediate wait
times out before the close token orders exact `closed`, exit zero, and one
successful rename. This is not a graceful-close timeout contract, recovery
policy, general exclusion, or mutation authority; Windows remains unadmitted.

M162's test-only [Windows duplicated-handle retention
probe](docs/security/cache-cleanup-windows-duplicated-handle-probe.md) creates
one noninheritable same-process duplicate of the no-delete-share directory
handle. Closing only the original leaves false/error 32 denial in force;
closing the final duplicate permits one successful rename. This is not
inherited-handle or cross-process duplication evidence, general exclusion, or
mutation authority; Windows remains unadmitted.

M163's test-only [Windows inherited-handle retention
probe](docs/security/cache-cleanup-windows-inherited-handle-probe.md) passes
only one no-delete-share directory handle through a `STARTUPINFO` explicit
handle list, then immediately restores the parent's handle to noninheritable.
Closing the parent copy leaves false/error 32 denial in force until the fixed
child closes its inherited handle. This is not a concurrency-safe inheritance
contract, broad inheritance, leak-freedom under concurrent launches, general
exclusion, or mutation authority; Windows remains unadmitted.

M164's test-only [Windows inherited-launch failure
probe](docs/security/cache-cleanup-windows-inherited-launch-failure-probe.md)
uses one fixed missing executable to produce a real process-creation failure
after temporary explicit handle allowlisting. The parent restores
noninheritability and retains false/error 32 until explicit close. This is not
restoration-failure injection, arbitrary launch-failure coverage, concurrent-
launch safety, recovery, general exclusion, or mutation authority; Windows
remains unadmitted.

M165's test-only [Windows inherited-handle restoration-failure
probe](docs/security/cache-cleanup-windows-inherited-restore-failure-probe.md)
injects one fixed error before the native restore call after successful child
creation. The unchanged helper closes and reaps the child before propagating
the exact error; the caller then explicitly repairs the still-inheritable
parent handle and retains false/error 32 until close. This is not a real native
restoration failure, concurrent-launch safety, recovery, general exclusion, or
mutation authority; Windows remains unadmitted.

M166's test-only [Windows concurrent broad-inheritance leak
probe](docs/security/cache-cleanup-windows-concurrent-inheritance-leak-probe.md)
uses bounded events to pause M163's explicit-list launch while its exact parent
handle is temporarily inheritable, then starts the same fixed child with broad
inheritance. Native rename remains false/error 32 after the parent and intended
child close and becomes true/code zero only after the broad child closes. This
is one controlled real leak observation, not a concurrency-safe spawning
contract, general leak-freedom, recovery, general exclusion, or mutation
authority; Windows remains unadmitted.

M167's test-only [Windows concurrent explicit-list isolation
probe](docs/security/cache-cleanup-windows-concurrent-explicit-inheritance-probe.md)
holds two distinct blocker handles inheritable across two real one-handle-list
process creations. After both parent handles close, releasing either child
permits rename only for its root; both release orders prove the same pairwise
isolation. This is not a concurrency-safe process-creation contract, general
leak-freedom, recovery, general exclusion, or mutation authority; Windows
remains unadmitted.

M168's test-only [Windows concurrent explicit-list launch-failure
probe](docs/security/cache-cleanup-windows-concurrent-explicit-launch-failure-probe.md)
holds a successful fixed-child launch and a real missing-executable launch in
one shared temporary-inheritability window. After both parents close, the
failed-launch root becomes renameable while the successful child still blocks
only its own root. This is not arbitrary failure coverage, a concurrency-safe
process-creation contract, recovery, general exclusion, or mutation authority;
Windows remains unadmitted.

M169's test-only [Windows concurrent explicit-list restoration-failure
probe](docs/security/cache-cleanup-windows-concurrent-explicit-restore-failure-probe.md)
starts two real fixed children with distinct handles, then injects one restore
failure while both helpers are at restoration. The failed child is reaped
before the error escapes; after explicit parent repair and close, the failed-
restoration root releases while the survivor child still blocks only its own
root. This is not a real native restoration failure, not a concurrency-safe
process-creation contract, recovery, general exclusion, or mutation authority;
Windows remains unadmitted.

M170's test-only [Windows concurrent explicit-list abrupt-termination
probe](docs/security/cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe.md)
starts two real fixed children with distinct handles and closes both parent
copies. One child is forcibly terminated and waited for; only its root releases
while the survivor remains live and blocks its own root until graceful close.
This is not crash recovery, not a concurrency-safe process-creation contract,
recovery, general exclusion, or mutation authority; Windows remains
unadmitted.

## Unsupported interpreter observations

M118 retains Python 3.15 outside the supported range. One exact Windows CPython
3.15.0b1 pure-wheel probe used an explicit metadata override, and `doctor`
correctly rejected that interpreter even though deterministic serial headless
execution completed. This unsupported prerelease compatibility observation is
no support promise and authorizes no workflow, dependency, metadata, runtime,
provider, release-authority, or security-support change. It is not a real
public release observation.
