# Decisions Pending

No architecture decision is currently blocked.

RFC-0092 resolves the M109 zero sample-member internal-attribute profile
preflight. PKWARE defines the central two-byte field as an advisory apparent-
text bit plus a mainframe record-control bit, with other bits reserved or
unused. Python exposes public `ZipInfo.internal_attr`; CPython initializes it to
zero. Exact CPython 3.12.13, 3.13.13, and 3.14.5 each admitted value `1` and
read the probe payload, while the fixed 50-member producer emits only zero.
Private release smoke therefore requires every public central internal-
attribute value to equal zero after M108 and before exact inventory, staging,
or reads. The stable error is `sample bundle has unsupported internal
attributes`.

This zero sample-member internal-attribute profile preflight is one central-
internal-attribute exact-profile classifier, not text/binary content
interpretation, a record-control semantics parser, supported-bit mask,
external-attribute or host policy, raw record parser, payload-content check,
archive repair, general ZIP validity claim, or general sandbox. RFC-0092 records
the accepted policy; no M109 design decision remains pending.

RFC-0091 resolves the corrected M108 exact sample-member creation-version
profile preflight. PKWARE defines the lower `version made by` byte as the ZIP
specification version supported by the encoder. Python exposes public central
`ZipInfo.create_version`; CPython defaults to `20`. Exact CPython 3.12.13,
3.13.13, and 3.14.5 each admitted public central creation version `21` and read
the probe payload, while the fixed 50-member producer emits sole version-made-
by pair `(20, 3)`. Private release smoke therefore requires every public
central `create_version` value to equal `20` after M107 and before exact
inventory, staging, or reads. The stable error is `sample bundle has an
unsupported creation version`.

This exact sample-member creation-version profile preflight is one central-
creation-version exact-profile classifier, not a general creation-version
semantics parser, supported-version range, producer-capability evaluator,
attribute-host policy, payload-content check, archive repair, general ZIP
validity claim, or general sandbox. The initially considered exact host policy
was rejected after 54 established architecture regressions. RFC-0091 records
the corrected accepted policy; no M108 design decision remains pending.

RFC-0090 resolves the M107 exact sample-member extraction-version profile
preflight. PKWARE assigns version 2.0 to Deflate, Python exposes public central
`ZipInfo.extract_version`, and CPython uses default value `20`. Exact CPython
3.12.13, 3.13.13, and 3.14.5 each exposed matching local/central pairs
`(21, 0)` and read both probe payloads, while the fixed 50-member producer emits
sole pair `(20, 0)`. Private release smoke therefore requires every public
central `ZipInfo.extract_version` value to equal `20` after established local
consistency, payload-layout, extra-field, member-metadata, M105, and M106 checks
and before exact inventory, staging, or reads. The stable error is `sample
bundle has an unsupported extraction version`.

This exact sample-member extraction-version profile preflight is one central-
extraction-version exact-profile classifier, not a general extraction-version
semantics parser, supported-version range, capability evaluator, raw record
parser, payload-content check, archive repair, general ZIP validity claim, or
general sandbox. It changes no workflow, dependency, producer, runtime API, or
release authority. RFC-0090 records the accepted policy; no M107 design
decision remains pending.

RFC-0089 resolves the M106 zero sample-member extraction-version reserved-byte
profile preflight. Python documents public central `ZipInfo.reserved` as zero,
CPython initializes and serializes zero, and PKWARE defines the enclosing two-
byte version-needed-to-extract field. Exact CPython 3.12.13, 3.13.13, and
3.14.5 each exposed matching local/central pairs `(20, 1)` and read both probe
payloads, while the fixed 50-member producer emits sole reserved value zero.
Private release smoke therefore requires every public central
`ZipInfo.reserved` value to equal zero after established local consistency,
payload-layout, extra-field, member-metadata, and M105 checks and before exact
inventory, staging, or reads. The stable error is `sample bundle has a nonzero
extraction-version reserved byte`.

This zero sample-member extraction-version reserved-byte profile preflight is
one central-reserved zero-profile classifier, not an extraction-version
semantics parser, supported-version allowlist, capability rule, raw record
parser, payload-content check, archive repair, general ZIP validity claim, or
general sandbox. It changes no workflow, dependency, producer, runtime API, or
release authority. RFC-0089 records the accepted policy; no M106 design
decision remains pending.

RFC-0088 resolves the M105 zero sample-member general-purpose-flag profile
preflight. PKWARE defines legitimate nonzero flag semantics and currently
unused bits; CPython exposes the central value through public
`ZipInfo.flag_bits`. Exact CPython 3.12.13, 3.13.13, and 3.14.5 each retained
matching unused bit 7 as value `128` and read both probe payloads, while the
fixed 50-member producer emits sole value zero. Private release smoke therefore
requires every public central `ZipInfo.flag_bits` value to equal zero after
established specific-flag, M94 consistency, M102/M103 layout, and M104 extra-
field, decoded-name, and member-metadata checks and before exact inventory,
staging, or reads.
The stable error is `sample bundle contains unsupported general-purpose flags`.

This zero sample-member general-purpose-flag profile preflight is one central-
flag zero-profile classifier, not a flag-semantics parser, bit registry, raw
record parser, payload-content check, archive repair, general ZIP validity
claim, or general sandbox. It changes no workflow, dependency, producer,
runtime API, or release authority. RFC-0088 records the accepted policy; no
M105 design decision remains pending.

RFC-0087 resolves the M104 empty sample-member extra-field profile preflight.
PKWARE defines local and central member extra fields as valid ZIP extensibility;
Python exposes central bytes through public `ZipInfo.extra`; CPython interprets
selected known fields and retains uninterpreted bytes. Exact CPython 3.12.13,
3.13.13, and 3.14.5 each retained equal local/central third-party field
`feca02006f6b` and read both probe payloads, while the fixed 50-member producer
emits empty fields.
Private release smoke therefore requires empty public central `ZipInfo.extra`
after established Unicode Path, ZIP64, M96 consistency, M102 bounds, and M103
contiguity checks and before decoded names, metadata, inventory, staging, or
reads. The stable error is `sample bundle contains an unsupported extra field`.

This empty sample-member extra-field profile preflight is one central-extra
emptiness classifier, not an extra-field semantics parser, field-ID registry,
raw central-record parser, payload-content check, archive repair, general ZIP
validity claim, or general sandbox. It changes no workflow, dependency,
producer, runtime API, or release authority. RFC-0087 records the accepted
policy; no M104 design decision remains pending.

RFC-0081 resolves the M98 local-header timestamp consistency preflight. PKWARE
duplicates a two-byte DOS modification time and two-byte DOS modification date
in corresponding local and central member records. Exact CPython 3.12.13,
3.13.13, and 3.14.5 retain both central tuples as
`(2026, 8, 23, 4, 6, 8)` and read both payloads when only the second local
time's low byte changes from `c4` to `e4`. Private release smoke therefore
reads exactly four bytes at `ZipInfo.header_offset + 10` after M97 and requires
equality with the DOS bytes represented by public central `ZipInfo.date_time`
before decoded names, metadata, inventory, staging, or reads. The stable error
is `sample bundle local header timestamps are inconsistent`.

This is one four-byte local-timestamp consistency classifier, not a timestamp
semantics validator, timezone or UTC conversion, wall-clock comparison,
calendar or reproducibility policy, extended-timestamp interpretation,
CRC/size or field-wide comparison, record/payload/next-header bound,
gap/adjacency/contiguity/non-overlap rule, inter-member layout validator,
archive repair, or general sandbox. It changes no workflow, dependency,
producer, runtime API, or release authority. RFC-0081 records the accepted
policy; no M98 design decision remains pending.

RFC-0080 resolves the M97 local-header extraction-version consistency
preflight. PKWARE duplicates a two-byte version-needed pair in corresponding
local and central member records. Exact CPython 3.12.13, 3.13.13, and 3.14.5
retain central pairs `[(20, 0), (20, 0)]` and read both payloads when only the
second local extraction-version byte changes to 21. Private release smoke
therefore reads exactly two bytes at `ZipInfo.header_offset + 4` after M96 and
requires equality with public central `ZipInfo.extract_version` and
`ZipInfo.reserved` before decoded names, metadata, inventory, staging, or
reads. The stable error is `sample bundle local header extraction versions are
inconsistent`.

This is one two-byte local-extraction-version consistency classifier, not a
supported-version allowlist, minimum extractor-capability rule, reserved-byte
policy, time/CRC/size or field-wide comparison,
record/payload/next-header bound, gap/adjacency/contiguity/non-overlap rule,
inter-member layout validator, archive repair, or general sandbox. It changes
no workflow, dependency, producer, runtime API, or release authority. RFC-0080
records the accepted policy; no M97 design decision remains pending.

RFC-0079 resolves the M96 local-header extra-field consistency preflight.
PKWARE defines separate variable extra fields in corresponding local and
central member records. Exact CPython 3.12.13, 3.13.13, and 3.14.5 retain both
central extras as `feca02006f6b` and read both payloads when only the second
same-length local extra changes to `feca02006f21`. Private release smoke
therefore reads the already bounded local bytes after M95 and requires exact
equality with public central `ZipInfo.extra` before decoded names, metadata,
inventory, staging, or reads. The stable error is `sample bundle local header
extra fields are inconsistent`.

This is one bounded local-extra equality classifier, not an extra-field
semantics parser, broad extra-field ban, new field-ID policy,
version/time/CRC/size or field-wide comparison, record/payload/next-header
bound, gap/adjacency/contiguity/non-overlap rule, inter-member layout validator,
archive repair, or general sandbox. It changes no workflow, dependency,
producer, runtime API, or release authority. RFC-0079 records the accepted
policy; no M96 design decision remains pending.

RFC-0078 resolves the M95 local-header compression-method consistency
preflight. PKWARE duplicates a two-byte compression method in corresponding
local and central member records. Exact CPython 3.12.13, 3.13.13, and 3.14.5
retain central methods `[8, 8]` and read both payloads when only the second
local method changes to stored 0. Private release smoke therefore reads exactly
two little-endian bytes at `ZipInfo.header_offset + 8` after M94 and requires
equality with central `ZipInfo.compress_type` before decoded names, metadata,
inventory, staging, or reads. The stable error is `sample bundle local header
compression methods are inconsistent`.

This is one two-byte local-compression-method consistency classifier, not a
local extra-field comparison/parser, version/time/CRC/size or field-wide
comparison, method allowlist, record/payload/next-header bound, gap/adjacency/
contiguity/non-overlap rule, inter-member layout validator, archive repair, or
general sandbox. It changes no workflow, dependency, producer, runtime API, or
release authority. RFC-0078 records the accepted policy; no M95 design decision
remains pending.

RFC-0077 resolves the M94 local-header flag-consistency preflight. PKWARE
defines a two-byte general-purpose flag in both local and central member
records, while supported CPython exposes the central value and accepts a
demonstrated local-only encryption-bit mutation through both payload reads.
The fixed sample producer emits equal values, so complete release smoke now
compares exactly the two local bytes at `ZipInfo.header_offset + 6` with public
central `ZipInfo.flag_bits` after M93 and before decoded names, metadata,
inventory, staging, or reads. The stable error is `sample bundle local header
flags are inconsistent`.

This is one two-byte local-flag consistency classifier, not a local compression-
method or extra-field comparison, broad flag allowlist, field-wide consistency
check, payload/next-header bound, inter-member layout validator, archive repair,
or general sandbox. It changes no workflow, dependency, producer, runtime API,
or release authority. RFC-0077 records the accepted policy; no M94 design
decision remains pending.

Feature PR #234 integrates the accepted RFC-0077 policy as verified squash
`7974b6fc110f995cac25f7d69d9c48b55013a764` after exact-head hosted run
`32581692977` passed the unchanged three Linux-first allocations. The squash
has exact qualified tree `96bd9000efbc473d09f0c75d83c5e1231621409e`,
sole parent M93 closeout, standalone DCO, and a valid GitHub signature. This
evidence does not widen the decision or establish a real public release
observation. Only the factual integration record and closeout remain; no M94
policy decision is pending.

RFC-0076 resolves the M93 local-header name-consistency preflight. PKWARE
requires corresponding local and central member records, places each variable
name immediately after the fixed local prefix, and specifies CP437 by default
with UTF-8 under bit 11. Python exposes the central decoded name, flags, and
header offset; exact CPython 3.12-3.14 admits a same-length local-only name
mutation and defers `BadZipFile` until member open. The selected fixed-profile
rule reconstructs the central name bytes under the central bit-11 policy and
requires exact equality with the already bounded raw local name after M92 and
before decoded-name policy, metadata, inventory, staging, or reads. It adds no
local-flag comparison, extra-field comparison, field-wide consistency,
inter-member layout validator, repair, workflow, dependency, producer,
runtime API, or release authority. RFC-0076 records the accepted policy;
implementation and exact-head qualification are integrated by feature PR
#231. The factual integration record and closeout remain active; no policy
decision is pending.

RFC-0075 resolves the M92 local-header variable-envelope bound. PKWARE defines
two 16-bit local file-name and extra-field length declarations before their
variable bytes, and Python exposes each purported header offset. Exact CPython
3.12-3.14 admits a 65,535-byte local name declaration whose fixed prefix fits
before the conventional central directory, then defers `BadZipFile` until
member open. The selected narrow fixed-profile rule reads only those two
lengths after M91 and before names, metadata, inventory, staging, or reads. It
adds no local-name comparison, extra-field parsing, next-header or payload
bound, inter-member layout validator, workflow, dependency, producer, runtime
API, or release authority. RFC-0075 records the accepted policy;
implementation and exact-head qualification are integrated by feature PR
#228. The factual integration record and closeout remain active; no policy
decision is pending.

RFC-0074 resolves the M91 fixed local-header-prefix bound. PKWARE defines 30
fixed local-header bytes before variable name and extra fields, and Python
exposes each purported header offset. Exact CPython 3.12-3.14 admits a pointer
with a valid signature but only four bytes before the conventional central
directory and defers `BadZipFile` until member open. The selected narrow fixed-
profile rule is one arithmetic prefix-bound classifier after M90 and before
names, metadata, inventory, staging, or reads. It adds no local-header field
parser, record extent, payload bound, inter-member layout validator, workflow,
dependency, producer, runtime API, or release authority. RFC-0074 records the
accepted policy. The exact corrected feature tree, factual integration record,
and closeout are squash-integrated through PRs #225-#227.

RFC-0073 resolves M90 local-header signature preflight. PKWARE defines the four-byte
local-file-header signature and Python exposes each purported header offset.
Exact CPython 3.12-3.14 admits a pointer shifted one byte into a real header as
ordered, distinct, in-bounds public metadata and defers `BadZipFile` until
member open. The selected narrow fixed-profile rule classifies only four bytes
at each public offset after M89 and before names, metadata, inventory, staging,
or reads. It adds no local-header field parser, record-extent or inter-member
layout validator, workflow, dependency, producer, runtime API, or release
authority. RFC-0073 records the accepted narrow policy. Complete local and
exact-head cross-platform qualification are green, and the exact qualified
feature tree, factual integration record, and closeout are squash-integrated
through PRs #222, #223, and #224.

RFC-0072 resolves M89 local-header-offset bounds preflight. PKWARE places local/data
records before the central-directory sequence, and Python exposes the central
pointer as the byte offset to a member's file header. Exact CPython 3.12-3.14
accepts a pointer equal to the conventional central-directory offset and defers
`BadZipFile` until member open. The selected narrow fixed-profile rule requires
every public offset to be strictly before that boundary after M88 and before
names, metadata, inventory, staging, or reads. It admits no local-header parser,
record-extent or inter-member layout validator, workflow, dependency, producer,
runtime API, or release authority. RFC-0072 records the accepted narrow policy.
Complete local and exact-head hosted qualification are green, and the exact
qualified tree, factual integration record, and closeout are squash-integrated
through PRs #219, #220, and #221.

RFC-0071 resolves M88 local-header-order preflight. PKWARE permits arbitrary
ZIP file order generally, while Python documents `ZipFile.infolist()` as archive-entry
order and the fixed LudoWeave producer emits physical local-header order.
Cross-version CPython 3.12-3.14 probes expose a central-record-only swap as
offsets `[46, 0]` and read both members successfully. The selected narrow rule
requires strictly increasing public offsets after M87 distinctness and before
names, metadata, inventory, staging, or reads. It is not a general ZIP-validity
claim and admits no raw parser, inter-member layout validator, workflow,
dependency, producer, runtime API, or release authority. Exact-head cross-
platform hosted qualification and guarded squash integration are complete.

RFC-0070 resolves M87 distinct local-header-offset preflight. PKWARE assigns a
local header and corresponding central record to each stored file, while exact
CPython 3.12-3.14 exposes duplicate central local-header pointers and defers
their consequences until member open. The selected fixed-profile response is
one aggregate distinctness check over public `ZipInfo.header_offset` values
after M86 and before names, metadata, inventory, staging, or reads. Corrected
exact-head cross-platform hosted qualification and guarded squash integration
are complete. No raw parser, ordering/bounds rule, inter-
member layout validator, workflow, dependency, producer, runtime API, or
release authority is admitted.

RFC-0069 resolves M86 first local-header placement preflight. Private complete
release smoke finishes every established policy through M85, then requires the
minimum parser-exposed `ZipInfo.header_offset` to equal zero before M77 decoded-
name policy, metadata, exact inventory, staging, or reads. The stable policy
error is content-silent; empty archives retain the established later inventory
failure. This is not a local-header parser, central-directory parser, inter-
member layout validator, field-consistency validator, signature classifier,
archive repair path, or general archive sandbox. It adds no workflow,
dependency, producer, runtime API, or release authority. A real pass remains
pending an explicitly authorized signed-tag release execution.

RFC-0068 resolves M85 conventional central-directory placement preflight.
Private complete release smoke finishes every established policy through M84,
then requires the final conventional central-directory size plus offset to
equal the absolute final end-of-central-directory record offset before M77
decoded-name policy, metadata, exact inventory, staging, or reads. The stable
policy error is content-silent and the shared helper restores the previous
snapshot position. This is not a central-directory/local-header parser, end-
record search, ZIP64 parser, executable classifier, prepended executable or
self-extracting archive support, multi-volume assembler, or general archive
sandbox. It adds no workflow, dependency, producer, runtime API, or release
authority. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0067 resolves M84 conventional archive entry-count preflight. Private
complete release smoke finishes every M69-M82 policy pass and M83 archive disk
check, then reads exactly the final conventional 22-byte end-of-central-
directory record from the owned checksum-admitted snapshot. Both entry counts
must equal the standard reader's parsed member count before M77 decoded-name
policy, metadata, exact inventory, staging, or reads. The stable policy error
is content-silent and the previous snapshot position is restored. `0xFFFF` is
rejected as outside the fixed profile, not resolved through ZIP64. This is not
a ZIP64 end-record parser, sentinel resolver, end-record search, central/local-
header parser, neighboring-volume discovery, multi-volume assembler, or
general archive sandbox. It adds no workflow, dependency, producer, runtime
API, or release authority. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0066 resolves M83 conventional archive disk-field preflight. Private
complete release smoke finishes every M69-M82 archive-wide pass, then reads
exactly the final conventional 22-byte end-of-central-directory record from
the owned checksum-admitted snapshot. It requires the signature, zero comment
length, current-disk zero, and central-directory-start disk zero before M77
decoded-name policy, metadata, exact inventory, staging, or reads. The stable
policy error is content-silent and the previous snapshot position is restored.
`0xFFFF` is rejected as outside the fixed profile, not interpreted as proof of
split-volume topology. This is not a ZIP64 end-record parser, end-record search,
central/local-header parser, neighboring-volume discovery, multi-volume
assembler, or general archive sandbox. It adds no workflow, dependency,
producer, runtime API, or release authority. A real pass remains pending an
explicitly authorized signed-tag release execution.

M80 ZIP64 extra-field preflight is resolved for implementation. PKWARE assigns
exact extra-field ID `0x0001` to ZIP64 alternate sizes, header offset, and disk-
start metadata. Current CPython applies the size and header-offset values, not
the defined disk-start value, before release smoke receives `ZipInfo`. The
fixed 50-member sample is small and emits no extra fields, so M80 rejects exact
central-directory ID `0x0001` after established M79 policy and before decoded-
name or metadata policy. Unrelated fields and malformed-extra handling remain
outside M80. No broad extra-field ban, raw ZIP64 parser, large-file support
change, workflow, dependency, producer, runtime API, or release authority is
admitted.

RFC-0062 resolves M79 Unicode Path extra-field preflight. Private complete
release smoke finishes every established archive-wide flag/descriptor pass,
then performs a bounded extra-field walk and rejects exact Info-ZIP field ID
`0x7075` before decoded-name checks, metadata, inventory, staging, or reads.
The stable policy error is content-silent and owned resources close before
control returns. This is not a broad extra-field ban, general name-difference
rule, raw ZIP header parser, repair path, scanner, or general archive sandbox.
It adds no workflow, dependency, sample producer, runtime API, or release
authority. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0061 resolves M78 data-descriptor sample-member preflight. Private complete
release smoke finishes the established archive-wide M69/M75/M76 flag pass,
then rejects exact ZIP general-purpose bit 3 in a separate all-member pass
before M77 name checks, metadata, inventory, staging, or reads. The stable
policy error is content-silent and owned resources close before control
returns. This is not a raw descriptor parser, broad flag allowlist, local-
header consistency claim, repair path, scanner, or general archive sandbox.
It adds no workflow, dependency, sample producer, runtime API, or release
authority. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0060 resolves M77 NUL-suffixed sample-member name preflight. Private
complete release smoke checks every decoded `ZipInfo.orig_filename` for an
exact NUL after established flag checks and before metadata, inventory,
staging, or reads. This prevents CPython's documented NUL truncation from
hiding an unvalidated suffix behind an otherwise exact visible sample path.
The stable policy error is content-silent; later ambiguous members preempt
earlier metadata failures and owned resources close first. This is exactly a
NUL check, not a general original-versus-normalized name comparison, raw ZIP
parser, local-header/central-directory consistency claim, repair path, scanner,
or general archive sandbox. It adds no workflow, dependency, sample producer,
runtime API, or release authority. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0059 resolves M76 enhanced-deflate sample-member preflight. Private
complete release smoke rejects exactly ZIP general-purpose bit 4 when paired
with compression method 8, after established processing checks and before
metadata, inventory, staging, or reads. The stable policy error is content-
silent; later flagged members preempt earlier metadata failures and owned
resources close first. Stored-member bit 4 and other flag/method combinations
remain outside this exact decision. The check consumes central-directory flags
exposed by `ZipInfo`; local-header inconsistencies remain outside scope. This is
not a broad flag allowlist, enhanced-deflate decoder, repair path, raw parser,
scanner, or general archive sandbox. It adds no workflow, dependency, sample
producer, runtime API, or release authority. A real pass remains pending an
explicitly authorized signed-tag release execution.

RFC-0058 resolves M75 compressed-patch sample-member preflight. Private
complete release smoke rejects exactly ZIP general-purpose bit 5 during M69's
all-member flag preflight, after encryption and before metadata, inventory,
staging, or reads. The stable policy error is content-silent; later flagged
members preempt earlier metadata failures and owned resources close first.
This is not a broad flag allowlist, reserved-bit policy, implementation-error
catch, patch decoder, repair path, raw parser, scanner, or general archive
sandbox. It adds no workflow, dependency, sample producer, runtime API, or
release authority. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0057 resolves M74 content-silent sample ZIP decompression-failure
normalization. Private complete release smoke adds exactly `zlib.error` from a
checksum-admitted invalid deflated-member payload to the existing stable outer
error after owned cleanup. Suppressed context confines the decompressor
diagnostic while retaining the original exception programmatically. EOF,
policy, filesystem, and unexpected failures remain specific. This is not a
broad compression/general catch, replacement decompressor, payload repair, raw
parser, scanner, or general archive sandbox. It adds no workflow, dependency,
sample producer, runtime API, or release authority. A real pass remains pending
an explicitly authorized signed-tag release execution.

RFC-0056 resolves M73 content-silent sample ZIP text-failure normalization.
Private complete release smoke adds exactly `UnicodeDecodeError` from strict
archive-controlled UTF-8 name decoding in the central directory or local
header to M72's existing stable outer error after owned cleanup. Suppressed
context confines invalid bytes, offsets, codec, and reason while retaining the
original exception programmatically. This is not a broad Unicode/value catch,
replacement decoder, metadata repair, raw parser, scanner, or general archive
sandbox. It adds no workflow, dependency, sample producer, runtime API, or
release authority. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0055 resolves M72 content-silent sample ZIP failure normalization. Private
complete release smoke catches exactly documented `BadZipFile` and
`LargeZipFile` around its checksum-admitted extractor, lets owned cleanup
finish, then raises one stable error with suppressed rendered context. The
original exception remains available programmatically; verifier policy and
non-parser failures retain their categories. This is not a broad catch, public
error protocol, raw parser, scanner, or general archive sandbox. It adds no
workflow, dependency, sample producer, runtime API, or release authority. A
real pass remains pending an explicitly authorized signed-tag release
execution.

RFC-0054 resolves M71 checksum-admitted sample snapshot parsing. After bounded
source admission, complete release smoke copies at most 16 MiB into one owned
binary spooled temporary file while hashing, clears/fails on mismatch, and
gives that exact rewound snapshot to `ZipFile`. Later source change-and-restore
cannot alter parser input. This creates no persistent copy, source-immutability
guarantee, lock, raw ZIP parser, or general archive sandbox. It adds no
workflow, dependency, sample producer, runtime API, or release authority. A
real pass remains pending an explicitly authorized signed-tag release execution.

RFC-0053 resolves M70 sample-archive checksum binding. Complete release smoke
passes the already admitted `SHA256SUMS` digest into extraction, hashes and
rewinds the same opened handle before ZIP parsing, and repeats the comparison
after reads/completeness but before publication. A persistent mismatch uses one
content-silent category and second-check failure cleans owned staging. This
creates no snapshot, lock, immutable-input guarantee, change-and-restore
defense, raw ZIP parser, or general archive sandbox. It adds no workflow,
dependency, sample producer, runtime API, or release authority. A real pass
remains pending an explicitly authorized signed-tag release execution.

RFC-0049 resolves M66 staged sample-root publication. The existing real output
directory owns a same-filesystem temporary staging directory; completeness is
validated there before one rename exposes the final sample root. A final entry
that already exists fails before archive reads and remains untouched. Copy,
decompression, write, incompleteness, and publication failures clean the partial
owned stage and preserve their cause. This is not crash-durable, a general
archive sandbox, a recovery journal, concurrent filesystem race isolation, or
post-publication rollback. It adds no workflow, dependency, sample producer,
runtime API, or release authority. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0048 resolves M65 portable staged sample-member paths. Every member is a
regular file beneath the exact root with at most 255 relative ASCII characters
and portable components. Complete paths are unique case-insensitively,
directory ancestors retain one exact spelling, and file/directory prefix
collisions fail before extraction. Windows device stems, trailing periods,
Unicode, empty/dot components, explicit directory entries, and explicitly
encoded non-regular file types are rejected. Missing ZIP file-type mode bits
remain common-producer compatible. This performs no Unicode normalization or
filesystem probing and is not a general archive sandbox, absolute-path
portability claim, or cleanup guarantee. It adds no workflow, dependency,
sample producer, runtime API, or release authority. A real pass remains pending
an explicitly authorized signed-tag release execution.

RFC-0047 resolves M64 bounded staged sample-bundle extraction. Complete
count/path/link/declared-size preflight admits at most 256 members, 1 MiB per
member, and 8 MiB total before extraction; admitted files stream in 64 KiB
blocks and must exactly reproduce declared sizes. Only stored and deflated
methods are admitted; BZIP2, LZMA, and unknown methods fail preflight because
their standard-library read paths do not provide the same bounded decompressor-
output behavior. This is not a general archive sandbox, metadata-authentication
claim, filename-policy expansion, or transactional cleanup guarantee. It adds
no workflow, dependency, runtime API, or release authority. A real pass remains
pending an explicitly authorized signed-tag release execution.

RFC-0046 resolves M63 public-release subordinate-output confinement. Both in-
process release-document validation and complete smoke redirect subordinate
stdout and subordinate stderr, restore the process-global streams on return or
exception, and succeed only with an exact built-in zero integer. The consumer
retains one content-silent JSON document on its designated channel. This relies
on the verifier's single-thread utility ownership and adds no descriptor or
arbitrary subprocess capture, concurrency claim, workflow, dependency, runtime
API, or release authority. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0045 resolves M62 portable public-release asset-name conformance. The plan
consumer admits 1 through 255 restricted ASCII characters, rejects a trailing
period or case-insensitive Windows device stem, and requires case-insensitive
uniqueness before asset download or output-directory creation. Violations use
content-silent `public_release.invalid_plan`. This uses no filesystem probing,
locale, normalization, rewriting, cleanup, rollback, retry, workflow,
dependency, runtime API, or release authority. A real pass remains pending an
explicitly authorized signed-tag release execution.

RFC-0044 resolves M61 public release candidate/output-root separation. The
expected candidate directory is read-only input. It and the runner-owned output
root are strictly resolved before network or validator side effects; an output
root that equals or resolves beneath the candidate fails with stable
`public_release.path_overlap`. Filesystem-identity comparison across the output
ancestry also rejects differently spelled aliases on a case-insensitive
filesystem. Resolution and identity-inspection failures retain content-silent
candidate/temporary-directory codes, while a separate candidate child of the
output root remains valid. This adds no race-free guarantee, filesystem sandbox,
rollback, cleanup, retry, workflow, dependency, runtime API, or release
authority. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0041 resolves M58 public release transport-cleanup conformance. Every
obtained response receives one response close attempt before its created
connection receives one connection close attempt, and both close attempts
occur when response close fails. Active failures remain primary. Cleanup-only
ordinary failures use content-silent `public_release.request_failed` with the
first cause chained; cleanup control signals remain unwrapped. Redirect
continuation and separate partial publication require successful cleanup. This
adds no rollback, retry, private state, alternate client, workflow, dependency,
runtime API, or release authority. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0040 resolves M57 public release response-body conformance. Every
successful `HTTPResponse.read(amount)` returns immutable bytes no larger than
the requested amount before EOF interpretation, accounting, or output. Any
validated `Content-Length` must equal the total streamed octets for the release
document and every successful response after an asset redirect. Malformed read
shapes use content-silent request failure; declared-length disagreement remains
a size mismatch. This adds no private response/socket state, raw parser,
content decoder, alternate client, workflow, dependency, runtime API, cleanup,
or release authority and makes no general completeness claim for unframed
close-delimited bodies. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0039 resolves M56 public release status and redirect-reference conformance.
Every response status is a non-boolean integer from 100 through 599. Every
followed `302` exposes exactly one Location field through the documented header-
pair list; its value is one 1-to-8,000-octet ASCII URI-reference using valid RFC
3986 characters and complete percent escapes. Bracket delimiters are accepted
only inside the parsed authority and rejected in its path, query, or fragment.
The resolved target repeats the existing bounded HTTPS and per-hop peer/TLS/HTTP
checks. This adds no host
allowlist, private parser state, raw HTTP/URI parser, alternate client,
workflow, dependency, runtime API, or release authority and makes no general
SSRF claim. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0038 resolves M55 public release HTTP response-framing conformance. Every
response must expose documented HTTP/1.1-class value `11`; this is explicitly
not exact raw status-line token evidence because CPython can normalize another
`HTTP/1.x` value. Transfer encoding is
absent or exactly `chunked` case-insensitively, cannot coexist with content
length, and any present content length is a string before existing bounded
checks. Every redirect repeats the validation before status or body use. This
adds no private response-state dependency, raw HTTP parser, alternate client,
workflow, dependency, runtime API, or release authority and makes no general
request-smuggling claim. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0037 resolves M54 public release TLS session freshness. Every fixed API or
bounded redirected asset connection must report `session_reused` as exactly
`False` after the handshake and M53 binding, before service identity,
negotiated-session inspection, or HTTP. Missing, unsupported, resumed,
malformed, and raising observations fail content-silently. This adds no session
cache, session assignment, ticket control, workflow, dependency, runtime API,
or release authority, and does not claim a reconstructed handshake or
certificate exchange. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0034 resolves M51 public release negotiated TLS-session conformance. Every
fixed API or redirected asset connection advertises only `http/1.1` and, after
actual connected-peer validation but before HTTP transmission, requires exactly
TLSv1.2 or TLSv1.3, a well-formed cipher report with at least 128 secret bits,
no TLS compression, and ALPN `http/1.1` or no negotiated ALPN. There is no
cipher-name allowlist, workflow/dependency/release mutation, or authority
change. A real pass remains pending an explicitly authorized signed-tag release
execution.

RFC-0033 resolves M50 public release TLS key-log isolation. Every public API or
asset hop receives a new explicit verified client context with system
server-auth roots, certificate/hostname validation, TLS 1.2 minimum, strict
X.509 flags, and disabled key logging. An ambient `SSLKEYLOGFILE` remains
unchanged and cannot create or receive secrets from the verifier. No custom
trust store, pin, workflow, dependency, release mutation, or authority change
is introduced. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0032 resolves M49 public release connected-peer confinement. Every fixed
API or redirected asset connection validates the actual port-443 TLS socket
peer before HTTP transmission and permits only globally reachable unicast IPv4
or IPv6, with IPv4-mapped IPv6 classified by its embedded address. A
non-global peer has one stable forbidden code; timeout and malformed/unavailable
peer inspection retain the request timeout/failure taxonomy. No hostname/IP
allowlist, separate DNS preflight, workflow, dependency, release mutation, or
authority change is introduced. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0031 resolves M48 public release HTTP response conformance. The fixed
release-document request accepts only direct `200`; asset-ID requests accept
direct `200` or at most three bounded `302` responses. API-only headers remain
on `api.github.com`; timeout, other transport/protocol, and local-output
failures have distinct stable codes. All M47 identity, TLS, path, size,
validation, smoke, workflow, allocation, and authority bounds remain. A real
pass remains pending an explicitly authorized signed-tag release execution.

RFC-0030 resolves M47 cross-platform public consumer rehearsal. One typed
standard-library Python verifier replaces the Bash-only public path and the
existing tag-only fresh-consumer job expands to Ubuntu, Windows, and macOS.
Each runner creates a bounded plan, retrieves exact public bytes without a
release credential, and runs complete installed release smoke. The result
remains same-workflow/provider rather than independent/external evidence. Two
tag-only allocations are added; pull-request allocations, release authority,
runtime, dependency, package, and public API remain unchanged. A real pass
remains pending an explicitly authorized signed-tag release execution.

RFC-0029 resolves M46 fresh-runner consumer rehearsal. After the publishing
job succeeds, one additional read-only Linux job receives only the verified
release ID/version, retrieves the exact same-workflow admitted candidate,
creates a fresh bounded plan, repeats public byte validation without a release
credential, and runs installed release smoke. This is not independent/external
or cross-platform verification and adds no release mutation, publication
authority, pull-request CI allocation, runtime, dependency, or package change.
A real fresh-runner pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0028 resolves M45 public release consumer-path integrity. The publishing
job performs bounded credential-free exact-ID public retrieval, revalidates the
downloaded candidate, and runs complete installed release smoke. This is one
same-run observation, not independent/external or cross-platform evidence,
future availability, immutability, artifact security, PyPI, or a supported
channel. A real public-path pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0027 resolves M44 published release attestation integrity. The existing
release job will verify SLSA v1 provenance for every exact M43-retrieved asset
and an SPDX 2.3 SBOM attestation for exactly one pure wheel after publication.
The verifier fixes repository, signer workflow, tag/source identity, signer
commit, GitHub OIDC issuer, hosted-runner class, predicate, bundle count,
process count, timeout, and content-silent output bounds. No authority exists
to create a tag/release, change attestation creation, retry or roll back failed
publication, enable immutability, publish to PyPI, claim artifact security,
independent builds, or predicate truth, or promote a supported release channel.
A real attestation pass remains pending an explicitly authorized signed-tag
release execution; local and pull-request validation cannot substitute for
that hosted evidence.

RFC-0026 resolves M43 published-asset retrieval integrity. Protocol `/4`
requires unique bounded numeric asset IDs and may write one exclusive
published-only retrieval plan after complete verification. The existing tag job
retrieves every exact ID through the authenticated binary API and rehashes the
downloaded directory against the same published document. Failure is observed
after publication and performs no rollback or mutation. The result is one
authenticated point-in-time byte observation, not unauthenticated/global/future
availability, immutability, consumer installation, or attestation evidence.
Jobs, runners, actions, permissions, triggers, dependencies, credentials, tags,
releases, uploads, cleanup, and publication authority remain unchanged.

RFC-0025 resolves M42 published-prerelease observation. The exact numeric
release database ID now crosses the existing publish transition, after which
one read-only authenticated request must report public prerelease state, a
valid UTC publication time, and unchanged notes/assets. Protocol `/3` makes
draft/published state explicit. Failure blocks a successful release-job result
but performs no automatic rollback, deletion, or mutation. Jobs, runners,
actions, permissions, triggers, dependencies, credentials, tags, releases,
uploads, publication authority, and immutable-release policy remain unchanged.

RFC-0024 resolves M41 release-notes body integrity. The existing bounded M40
validator now requires authenticated draft `body` text to exactly equal the
fixed staged `RELEASE_NOTES.md` supplied through `--notes-file`, while emitting
no note content. The internal protocol advances to `/2`; both workflow files,
runner allocations, actions, permissions, triggers, dependencies, credentials,
API calls, tags, releases, and publication authority remain unchanged. Rendered
Markdown, link and factual-content review, immutable-release policy, PyPI, and a
supported release channel remain separate decisions.

RFC-0023 resolves M40 draft-release asset integrity. The existing tag job makes
its final draft/upload/publish sequence explicit and publishes only when a
bounded standard-library validator confirms the authenticated GitHub draft has
the exact local asset names, complete upload state, byte sizes, and SHA-256
digests. Failed verification remains an unpublished draft and assets are never
clobbered or automatically deleted. The gate adds no runner, action, permission,
trigger, dependency, credential, tag, release, or publication authority.
Independent remote download/storage verification, immutable-release policy,
PyPI, and a supported release channel remain separate decisions.

RFC-0022 resolves M39 release-tag identity enforcement. GitHub's annotated-tag
API is the hosted signature-verification authority, while local Git independently
checks the exact tag object, checkout commit, and `origin/main` ancestry before
the existing tag job performs expensive or publishing work. The bounded gate
adds no runner, action, permission, trigger, dependency, credential, tag, or
publication authority. A local trust store, signer/key allowlist, immutable-
release policy, PyPI channel, and supported-release claim remain separate
decisions.

RFC-0021 resolves M38 distribution reproducibility enforcement. The existing
Linux pull-request and tag-release distribution jobs build twice and compare
the exact pure wheel/source pair before smoke, staging, attestation, or
publication. A same-source/same-job byte match is required; cross-platform or
hermetic reproducibility, independent rebuilding, provenance, and publication
are not claimed. A separate rebuild runner and attestation changes are rejected
for this bounded milestone.

RFC-0020 resolves M37 CI change qualification with an exact trusted-base
classifier. Documentation-only work retains one Linux quality/docs/
architecture/distribution allocation; substantive work retains all three M36
allocations and eight slices. Windows/macOS depend on successful Linux
qualification, so an early failure consumes no desktop allocation. The
accepted tradeoff is later substantive desktop feedback. Workflow-level docs
filtering is rejected because GitHub documents a required-check pending risk;
a separate filter job is rejected because it adds a fourth allocation.

RFC-0019 resolves M36 CI runner ownership by preserving all eight existing
validation slices inside three OS-owned allocations. Ubuntu runs quality/
distribution, 3.12 graphics, and sequential 3.13/3.14 compatibility. Windows
and macOS each run 3.12 graphics followed by 3.14 compatibility. The accepted
tradeoff is less per-slice parallelism and rerun granularity in exchange for
five fewer runner allocations and repeated setups. No billed-minute saving is
claimed before hosted evidence; no coverage slice is removed.

RFC-0018 resolves how third-party conformance-adoption evidence is admitted.
The offline harness counts distinct independent external implementation
identities only after a complete project-accepted submission-census review and
a passing exact installed M17-M19 profile. Project-owned and maintainer-
authored references never count. Plugin-backed evidence is limited to the
existing M12 `render.device` capability and requires both compatible inert
manifest evidence and a passing render profile. Failed and not-executed
submissions remain in complete history. The reviewed manifest is empty, so the
current passing count is zero and no ecosystem, support, certification,
security, performance, or global-discovery result exists.

RFC-0017 resolves how agent-tool recovery-rate evidence is admitted. The
offline harness requires a complete reviewed cohort of task-directed sessions
and every dispatched call, keeps known failure and manual-recovery outcomes in
the denominator, blocks publication on unobserved terminal state, and preserves
complete history. The reviewed manifest is empty, so no measured rate or
recovery-free result exists. Human review owns session/call eligibility,
manual-recovery status, outcome, provenance, validation, and census
completeness. The eight essential CI jobs now run only for substantive pull
requests, avoiding redundant post-merge and `.project/**`-only runs.

RFC-0001 resolves the M7 first-native-kernel question by deferring Rust/PyO3
until its quantified cross-platform, buffer/GIL, ownership, build, fallback,
fuzz, and maintenance-owner gate is satisfied.

ADR-0023 resolves the M8 SDL3 question by using the already-pinned GLFW gamepad
surface and deferring SDL3 until a stable Python binding, auditable offline
binary delivery, explicit lifecycle ownership, cross-platform conformance, and
maintenance owner are evidenced.

ADR-0024 resolves the M9 Box2D question by deferring the preview binding until
the complete CPython/OS wheel and provenance matrix, stable API, lifecycle and
stale-object soak, documented GIL/thread ownership, cross-platform
snapshot/replay classification, copied engine adapter conformance, and a named
maintenance owner are evidenced.

ADR-0025 resolves the M10 inspector boundary with one isolated, owned local
MCP child, detached semantic observations, explicit receipted writes, exact
hash continuity, and no arbitrary process, network, remote-attach, or editor
surface.

RFC-0002 resolves the M12 plugin boundary with canonical inert manifests,
explicit environment/policy/dependency checks, and no discovery, import,
execution, installation, or ambient global registry.

ADR-0027 resolves the M13 rollback/network-snapshot question by admitting only
a bounded offline correction-branch proof and deferring transport/live rollback
until canonical tick-input history, protocol/security, cross-platform network
simulation, resource budgets, lifecycle ownership, and maintenance gates are
complete.

ADR-0028 resolves the M14 constrained-3D question by retaining layered 2D and
deferring any 3D runtime until a bounded product slice, provider-neutral
spatial/render/asset contracts, canonical agent/replay semantics, equivalent
Null behavior, cross-platform installed conformance, measured resource
budgets, lifecycle ownership, and a named maintainer are evidenced together.

ADR-0029 resolves the M15 visual-editor question by retaining the finite
headless inspector and deferring GUI/editor implementation until public
compatibility, document/scene, selection/hierarchy, undo/conflict, property,
viewport, asset, recovery, accessibility/usability, cross-platform packaging,
resource-budget, and maintenance-owner gates are evidenced together.

ADR-0030 resolves the M16 WASM-mod question by retaining the inert M12 plugin
boundary and deferring executable guests until runtime provenance/support,
package identity/distribution, default-deny copied capabilities,
command/receipt mutation mapping, bounded execution, atomic trap/lifecycle,
deterministic replay, guest-state migration, isolation, adversarial
conformance, cross-platform installation, and named security/update ownership
are evidenced together.

ADR-0031 resolves the first external-adapter conformance boundary with one
versioned installed `RenderDevice` baseline over an explicitly supplied trusted
factory. It forbids discovery/loading/installation and records that passing
behavior is not security, provenance, cross-platform, performance, or provider
admission evidence. No independently authored adapter is counted until
external evidence is reviewed.

ADR-0032 resolves the installed agent-adapter conformance boundary with one
versioned 12-tool baseline over an explicitly supplied trusted factory. It
forbids discovery, dynamic import, installation, subprocesses, networking, and
global registration, and records that a project-owned pass is reference
behavior rather than security, provenance, external adoption, cross-platform,
performance, or manual-recovery evidence.

RFC-0003 resolves the first central API-stability candidate by retaining the
command, transaction, and receipt contracts as experimental. Same-version
canonical/atomic behavior is confirmed, but preview promotion remains gated on
a cross-version corpus, external consumer feedback, operation and receipt-field
evolution rules, a bounded public receipt reader, and a supported deprecation-
capable feature-release channel.

RFC-0004 resolves the bounded-reader gate with a strict resource-limited
decoder for the unchanged receipt/1 graph and immutable committed, dry-run,
and rejected fixtures from `0.1.0a1`. This satisfies only gate 4 of RFC-0003.
The fixture set is explicitly a single-version baseline; cross-version
compatibility, external adoption, evolution rules, a release channel, and
stability promotion remain unresolved.

RFC-0005 resolves the built-in operation-argument policy gate. Exact required
and optional fields, unknown-field rejection, and named semantic rules are
fixed per operation/version identity; a breaking change uses a new operation
version and a new identity is additive. This satisfies only gate 3 of
RFC-0003. Cross-version history, external feedback, receipt semantic-diff/
diagnostic evolution, and a supported deprecation release channel remain
unresolved.

RFC-0006 resolves the receipt semantic-diff and diagnostic-code policy gate.
Exact v1 field sets, presence, ordering, and meanings cannot change in place;
existing code meanings are fixed, new well-formed codes are additive, and
phase/message/scalar detail metadata is non-authoritative. This satisfies only
gate 5 of RFC-0003. Cross-version history, external feedback, and a supported
deprecation release channel remain unresolved.

RFC-0007 resolves how cross-version receipt-corpus evidence is admitted. The
offline harness preserves exact historical identities and requires a distinct
installed reader version plus supported-release records for every observed
version. Its current result is explicitly false because all evidence is
`0.1.0a1` and the release set is empty. Actual cross-version history, external
feedback, and a supported deprecation release channel remain unresolved.

RFC-0008 resolves how external-consumer-feedback evidence is admitted. The
offline harness requires manually reviewed independent-consumer records with
exact public repository, revision, protocol, outcome, and artifact identities;
the evaluator verifies only the frozen data contract and cannot establish
independence by itself. The reviewed manifest is empty, so actual external
feedback and adoption remain absent. Cross-version history and a supported
deprecation release channel also remain unresolved.

RFC-0009 resolves how supported deprecation-capable feature-release-channel
evidence is admitted. The offline harness requires two reviewed supported,
non-yanked final releases on distinct feature lines with exact publication
identities and append-only history. The reviewed manifest is empty, so the
actual channel remains absent. Cross-version release execution and external
consumer feedback also remain unresolved; no stability promotion is implied.

RFC-0010 resolves how the first-external-contribution documentation objective
is admitted. The offline harness requires at least one manually reviewed human
good-first contribution linked to a public project issue and merged pull
request, with exact Git/patch/feedback identities, DCO, documented validation,
no private maintainer knowledge, and no public-API, persistent-format,
dependency, or workflow change. The reviewed manifest is empty, so actual
external-contributor usability evidence remains absent. The evaluator cannot
establish independence or undisclosed assistance; human review owns those
facts, and no synthetic fixture or CI pass is an external contribution.

RFC-0011 resolves how externally authored sample games are admitted as a
longer-term adoption metric. The offline harness requires manually reviewed
independent authorship, immutable public provenance, installed-wheel headless/
command-receipt/replay evidence, distinct artifact identities, and reviewed
licensing while preserving exact complete history. The reviewed manifest is
empty, so the current external sample-game count remains zero. Project-owned
examples, maintainers, agents, CI, and synthetic fixtures are not adoption.

RFC-0012 resolves how external contributor-retention evidence is admitted. The
offline harness requires the same independently reviewed external human to
complete distinct first and later merged public contributions with exact
issue/PR/revision/artifact identities, chronology, DCO, validation, provenance,
and complete history. The reviewed manifest is empty, so retained-contributor
and return-contribution counts remain zero; popularity and synthetic fixtures
are not retention.

RFC-0013 resolves how published-wheel installation-matrix evidence is admitted.
The offline harness requires one immutable public pure-Python release wheel to
pass reviewed clean isolated installation and installed checks across the exact
practical OS/CPython matrix with complete history. The reviewed manifest is
empty, so source-checkout CI, local builds, and synthetic fixtures are not
published installation success.

RFC-0014 resolves how issue-response and pull-request-review latency evidence
is admitted. The offline harness requires a complete reviewed public cohort of
eligible external-human issues and pull requests, preserves pending items,
binds first qualifying human-maintainer actions to exact frozen evidence and
timestamp/latency agreement, and preserves complete history. The reviewed
manifest is empty, so no latency aggregate, responsiveness result, SLA, or
support claim exists. The evaluator cannot establish human roles, participant
distinctness, first-action state, or census completeness; manual review owns
those facts.

RFC-0015 resolves how CI replay-divergence-rate evidence is admitted. The
offline harness requires a complete reviewed public cohort of eligible replay
executions, preserves cancellation, early failure, skips, and missing result
evidence as non-executed, binds verified/diverged outcomes to exact workflow,
case, and frozen result identities, and preserves complete history. The
reviewed manifest is empty, so no measured rate or zero-divergence result
exists. Human review owns cohort completeness, eligibility, outcome,
provenance, and validation.

RFC-0016 resolves how benchmark-regression-rate evidence is admitted. The
offline harness requires a complete reviewed controlled cohort of paired
registered M1-M4 `perf_counter_ns` p95 comparisons, binds exact base/head
sources and frozen runner/result artifacts, requires predeclared integer
tolerances, preserves non-execution, and preserves complete history. M7
cProfile output is diagnostic and ineligible. The reviewed manifest is empty,
so no measured rate or zero-regression result exists. Human review owns runner
control, parameter equality, eligibility, comparability, tolerance
predeclaration, outcome, provenance, validation, and census completeness.

Operational follow-ups outside repository implementation:

- Verify and reserve the `ludoweave` package name before the first publication.
