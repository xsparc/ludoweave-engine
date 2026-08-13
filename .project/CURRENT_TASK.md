# Current Task

- **Task:** M83 - conventional archive disk-field preflight
- **Status:** Corrected feature tree is fully locally qualified and reviewed;
  exact-head hosted qualification is next.
- **Base:** Verified M82 closeout squash
  `e0ade9928e19895d5074a40fd11fcbf6bfa6fbe0`, tree
  `fc19f02ae8af1a432d23f0ccf8e4775ef10085c7`.
- **Branch:** `release/m83-archive-disk-preflight`

## Accepted slice

- After every established M69-M82 archive-wide policy, read exactly the final
  conventional 22-byte end-of-central-directory record from the owned
  checksum-admitted snapshot.
- Require the signature, zero comment length, current-disk zero, and central-
  directory-start disk zero; restore the prior snapshot position.
- Reject either nonzero disk field with stable content-silent error `sample
  bundle uses unsupported archive disk fields` before M77 decoded-name policy,
  metadata, exact inventory, staging, or reads.
- Preserve established flag, extra-field, comment, and member-volume error
  precedence and owned source/snapshot/archive cleanup.
- Add RFC-0066 plus aligned public, security, architecture, release, roadmap,
  maintainer, and repository evidence records.
- Add no ZIP64 end-record parser, end-record search, central-directory/local-
  header parser, neighboring-volume discovery, multi-volume assembler,
  workflow, dependency, lock, version, producer, runtime package/API, release
  authority, tag, release, or publication.

## Direction evidence

- PKWARE APPNOTE sections 4.3.16, 4.4.19, and 4.4.20 define the conventional
  EOCD current-disk and central-directory-start disk fields; `0xFFFF` defers a
  value to a ZIP64 end record.
- Exact installed CPython 3.12.13, 3.13.13, and 3.14.5 source parses those
  fields but `ZipFile._RealGetContents()` does not consult them.
- Cross-version probes show `(1,0)`, `(0,1)`, `(1,1)`, and
  `(0xFFFF,0xFFFF)` all preserve a volume-zero member and readable deflated
  payload.
- The fixed producer emits one final conventional record with both disk fields
  zero, so all other conventional values are outside the intended profile.

## Current evidence

- M82 closeout PR #200 changed only the three project records, allocated no
  workflow, passed two exact-head audits, and squash-integrated exact tree
  `fc19f02ae8af1a432d23f0ccf8e4775ef10085c7` as
  `e0ade9928e19895d5074a40fd11fcbf6bfa6fbe0` with sole integration-record
  parent, parsed DCO, and valid GitHub verification. Only clean synchronized
  `main` remained locally/remotely; no open PR, tag, release, postmerge run, or
  M82 generated target remained before M83 selection.
- The static-clean authoritative red baseline passed 16 standard-library,
  established-precedence, producer, and protected-surface controls and failed
  15 missing policy, ordering, cleanup, helper/source, and documentation
  contracts in 0.52 seconds.
- The bounded runtime helper and exact call ordering make 30 assertions pass in
  0.32 seconds; only the deliberately absent RFC/public-document contract
  failed at that checkpoint. RFC-0066 and aligned documentation are now added.
- Strict docs initially caught missing RFC navigation; the omission was
  corrected. Findings-first review then found the structural-error claim lacked
  explicit regression coverage. Three test-only controls now prove signature,
  declared-comment-length, and trailing-byte shapes retain stable ZIP-data
  normalization; all 34 corrected assertions pass on CPython 3.12-3.14.
- Complete local qualification is clean: CPython 3.12 passes 2,514 tests with
  15 capability skips; initial full 3.13/3.14 suites each passed 2,501 with 16
  skips and the corrected focused contract passes on both. Static, 974-case
  architecture, 285-case M64-M83 lineage, real-wgpu, profiles, both vertical
  slices, M1-M4 diagnostics, reproducible builds, isolated-wheel smoke, ten-
  artifact staging, complete release smoke, strict docs, scope, disclosure,
  credential, artifact, whitespace, and Git-object gates pass.

## Remaining gates

1. Publish a ready feature PR, require exact-head hosted qualification and two
   separated review audits, then squash-integrate only the qualified tree.
2. Publish and integrate bounded factual records, close out M83, remove its
   branches/generated targets, and return to clean synchronized `main` before
   selecting M84.
