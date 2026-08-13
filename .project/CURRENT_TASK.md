# Current Task

- **Task:** M84 - conventional archive entry-count preflight
- **Status:** Locally qualified and independently reviewed; exact-head hosted
  qualification is pending.
- **Base:** Verified M83 closeout squash
  `1c380897fc8ee43f5885c733c1c11f87878ff2a1`, tree
  `c5bcfb19be359c828bcdd413f784ff4a9fa204e7`.
- **Branch:** `release/m84-archive-entry-preflight`

## Accepted slice

- After every established M69-M82 policy and M83 archive disk policy,
  read exactly the final conventional 22-byte end-of-central-directory record
  from the owned checksum-admitted snapshot.
- Require both conventional entry counts to equal the standard reader's parsed
  member count and restore the prior snapshot position.
- Reject any mismatch with stable content-silent error `sample bundle archive
  entry counts are inconsistent` before M77 decoded-name policy, metadata,
  exact inventory, staging, or reads.
- Preserve established error precedence and owned source/snapshot/archive
  cleanup.
- Add RFC-0067 plus aligned public, security, architecture, release, roadmap,
  maintainer, and repository evidence records.
- Add no ZIP64 end-record parser, sentinel resolution, end-record search,
  central-directory/local-header parser, neighboring-volume discovery, multi-
  volume assembler, workflow, dependency, lock, version, producer, runtime
  package/API, release authority, tag, release, or publication.

## Direction evidence

- PKWARE APPNOTE sections 4.3.16, 4.4.21, and 4.4.22 define the conventional
  EOCD current-disk and total-entry counts; `0xFFFF` defers a count to a ZIP64
  end record.
- Exact installed CPython 3.12.13, 3.13.13, and 3.14.5 source parses those
  fields but `ZipFile._RealGetContents()` does not consult them.
- Cross-version probes show zero, asymmetric, inflated, and `0xFFFF` pairs all
  preserve one parsed member and readable deflated payload.
- The fixed producer emits 50 in both fields and exposes exactly 50 members.

## Current evidence

- M83 closeout PR #203 changed only the three project records, allocated no
  workflow, passed two exact-head audits, and squash-integrated exact tree
  `c5bcfb19be359c828bcdd413f784ff4a9fa204e7` as
  `1c380897fc8ee43f5885c733c1c11f87878ff2a1` with sole integration-record
  parent, parsed DCO, and valid GitHub verification. Only clean synchronized
  `main` remained locally/remotely; no open PR, tag, release, postmerge run,
  disclosure marker, or M83 generated target remained before M84 selection.
- The static-clean authoritative red baseline passed 9 standard-library,
  established-precedence, producer, and protected-surface controls and failed
  16 missing policy, ordering, cleanup, helper/source, and documentation
  contracts in 0.50 seconds.
- The bounded runtime helper and exact call ordering make 24 assertions pass in
  0.31 seconds; only the deliberately absent RFC/public-document contract
  failed at that checkpoint. RFC-0067 and aligned documentation are now added.
- Review strengthened the helper's malformed-final-record normalization
  contract and corrected stale status wording. The corrected tree passes every
  local gate with no actionable finding remaining.

## Remaining gates

1. Publish a ready feature PR, require exact-head hosted qualification and two
   separated review audits, then squash-integrate only the qualified tree.
2. Publish and integrate bounded factual records, close out M84, remove its
   branches/generated targets, and return to clean synchronized `main` before
   selecting M85.
