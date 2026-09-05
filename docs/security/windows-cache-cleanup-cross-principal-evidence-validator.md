# Windows cache-cleanup cross-principal evidence validator

**Status:** Accepted for M206 source validation; qualifying evidence has not
been produced.

M206 adds one offline, read-only validator for the evidence envelope defined by
the [M205 cross-principal validation
contract](windows-cache-cleanup-cross-principal-validation-contract.md).
Structurally valid does not mean criterion 6 satisfied. M206 does not resolve
criterion 6, no qualifying cross-principal run has occurred, and criterion 6
remains unresolved. Windows is not admitted. Cleanup remains unimplemented and
unauthorized.

## Input boundary

The validator accepts one exact canonical JSON object with schema
`ludoweave.windows-cleanup-cross-principal-evidence/1`. It uses LudoWeave's
existing bounded canonical JSON contract. Duplicate fields, unknown fields,
noncanonical bytes, and non-finite numbers are rejected. The artifact is capped
at 4,194,304 bytes, 2,048 JSON nodes, eight levels, 256 members per collection,
and 256 UTF-8 bytes per string.

Input must be a regular non-symbolic-link file. The validator compares before
and after open identity and size, including device, file identity, and file
length from the opened descriptor. It also compares the descriptor after the
bounded read and the pathname after close. Any difference refuses validation.
The validator never writes the artifact, follows no symlink, starts no process,
uses no network, and performs no cleanup.

## Exact evidence shape

Every document contains all 13 mandatory lanes in canonical order:

1. `baseline_denial`
2. `acl_flip`
3. `owner_dacl_takeover_denial`
4. `hard_link_alias`
5. `reparse_substitution`
6. `rename_substitution`
7. `delete_recreate`
8. `inherited_handle`
9. `duplicate_handle`
10. `unrelated_open`
11. `cross_session`
12. `recovery_tamper`
13. `control_channel_failure`

The document is capped at 32 lanes, 512 trials, and 32,768 events. An attempted
run binds a lower-case `git-sha1:` source identity and `sha256:` executable
identity. An all-`not_run` document omits both identities.

A passed lane contains all eight barrier identities in canonical order:

1. `before_authority_admission`
2. `after_authority_before_intent`
3. `after_intent_before_pending`
4. `after_quarantine_pending_before_quarantine`
5. `after_quarantine_before_quarantined`
6. `after_delete_pending_before_deletion`
7. `after_deletion_before_deleted`
8. `during_recovery_reconciliation`

Every applicable barrier records passed authority-first and mutation-first
release orders. Every inapplicable barrier records `not_applicable` for both
orders. Across lane and barrier records the closed status vocabulary is passed,
failed, unsupported, not_run, and not_applicable. A passed lane has at least one
applicable barrier, positive observations, and every safety outcome set true.

## Sanitization and claims

Principal qualification is limited to four observer-derived booleans:
`principal_sid_distinct`, `authentication_context_distinct`,
`administrator_membership_absent`, and `bypass_privileges_absent`. The control
record contains only `observer_derived`, `control_channel_authenticated`,
`fixture_confined`, and `teardown_settled`.

Each lane contains only counts, fixed identifiers and statuses, barrier results,
and these outcomes:

- `no_out_of_root_mutation`
- `no_unauthorized_deletion_or_restoration`
- `no_canonical_world_state_change`
- `no_leaked_handle`
- `no_live_participant_or_descendant`

Evidence contains no account name, SID value, domain, token or authentication
identifier, session identifier, process identifier, pathname, handle value, ACL
bytes, environment value, credential, secret, or platform error text.

Only an all-passed complete document can set criterion_6_satisfied true: all
four qualification booleans, all four control booleans, and all 13 lane statuses
must pass. Counts and summary totals must agree. Failed, unsupported, incomplete,
or not-run evidence is structurally reviewable but cannot satisfy criterion 6.
windows_cleanup_admitted must remain false because independent-host criterion
7 is still absent.

## Output and reviewed fixture

Success prints one path-free canonical JSON summary with the evidence SHA-256,
criterion result, fixed lane-status counts, and the false Windows-admission
claim. Failure prints one path-free typed validation error. Operating-system
error text and input locations are never echoed.

The reviewed fixture is intentionally all not_run. It proves that the schema,
canonical decoder, sanitizer, and incomplete-result handling are reviewable; it
is not execution evidence. M206 supplies no credential or account lifecycle,
launcher, native adapter, or production authority. It adds no new hosted
allocation. The
executable validator is source-only test tooling, not part of the frozen public
script or wheel surface.

## Primary references

- [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange
  Format](https://www.rfc-editor.org/rfc/rfc8259)
- [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785)
- [Microsoft `TOKEN_STATISTICS`](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-token_statistics)
- [GitHub-hosted runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
