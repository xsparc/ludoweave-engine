# ADR-0025: Owned local semantic inspector over typed stdio tools

- Status: Accepted
- Date: 2026-08-06

## Context

The post-alpha sequence calls for a live semantic inspector, likely as a
separate process using the command/query protocol. A general process launcher,
remote attach protocol, or editor would expand the trust boundary before the
engine has authentication, discovery, deployment, or UI ownership contracts.
Reading storage internals directly would also give human tooling a privileged
view unavailable to software agents and could turn detached diagnostics into a
second mutable state model.

The existing local MCP adapter already exposes bounded world description,
stable query, snapshots, semantic diff, telemetry, transactions, and receipted
ticks. M10 can therefore prove the separate-process ownership and semantic
stream without adding another transport or authority.

## Decision

Add `ludoweave inspect` as a finite headless client. It may launch only
`sys.executable -I -m ludoweave mcp` for one explicitly selected data-only project
or the built-in Agent World Builder sample. It uses pipes with no shell and
accepts no arbitrary executable, Python module, command, URL, host, port,
process identifier, or remote endpoint. Isolated mode prevents the working
directory, `PYTHONPATH`, and user site from shadowing the installed package;
project paths follow an option terminator so their names cannot become flags.

The default child is read-only. Sample bootstrap and bounded tick advancement
require `--write`; they call only the existing `transaction_apply` and
`world_tick` tools, use optimistic state hashes, and retain the returned
receipts. The inspector does not add a mutation operation.

Emit newline-delimited `ludoweave.inspector.event/1` observations containing
detached world description, stable bounded query results, telemetry, the
optional transition/receipt, and the semantic diff from the preceding state.
Keep the prior canonical snapshot only inside the parent long enough to request
the next diff. Never emit the snapshot, paths, environment values, process IDs,
provider objects, or mutable aliases.

Verify MCP initialization and required tools, JSON and message bounds,
response identity, transition commitment, completed ticks, and exact
snapshot/world/query/telemetry/diff hash continuity. The parent owns all child
pipes and closes the child on success and failure with a bounded forced-close
fallback. Architecture tests forbid network imports and Python evaluation in
both local stdio modules.

## Consequences

- Humans and agents inspect the same engine-owned semantic documents instead
  of receiving storage- or provider-specific access.
- The installed pure-Python wheel gains an exercised local process composition
  without a runtime dependency, compiler, network listener, or global daemon.
- Sessions are finite and caller-driven. They do not observe mutations from an
  unrelated live process and do not provide a visual editor or wall-clock
  watch loop.
- Large authority snapshots can exceed the inspector's deliberately smaller
  protocol bounds and fail closed. This is preferable to incomplete or
  unverified observations in the first slice.

## Alternatives considered

A GUI/TUI inspector was rejected because M10 does not define editor state,
interaction, accessibility, rendering ownership, or packaging. Network and
remote-process attachment were rejected because no authentication,
authorization, discovery, origin, or deployment contract exists. An arbitrary
child command was rejected because it would create a shell/process-launch API.
Direct in-process ECS inspection was rejected because it would bypass the
shared typed command/query surface and would not exercise child ownership.
