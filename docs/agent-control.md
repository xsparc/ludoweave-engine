# Agent control interface

M5 adds a transport-independent, typed control surface over the same
`WorldSession`, `TransactionService`, snapshots, receipts, replay records, and
presentation extraction used by Python applications and the CLI. It does not
add another authority store. The live ECS/world record remains canonical, and
every accepted mutation reaches an existing versioned transaction safe point.

The interface is experimental protocol `ludoweave.agent.service/1`. It is
designed for local humans, tests, and software agents to observe and operate the
same world without arbitrary Python evaluation, shell access, dynamic imports,
or provider-native objects.

## Tools

`AgentCommandService.tools()` returns immutable JSON Schema 2020-12
descriptions for exactly these tools:

| Tool | Capability | Behavior |
| --- | --- | --- |
| `project_describe` | read | Project identity, schemas, limits, tools, and enabled capabilities. |
| `world_describe` | read | Current tick, authority hash, and entity/component/resource counts. |
| `world_query` | read | Stable entity query by included/excluded component UUID. |
| `entity_get` | read | One live entity and its detached canonical component values. |
| `transaction_validate` | read | Dry-run a canonical transaction and return its proposed receipt/diff. |
| `transaction_apply` | write | Atomically apply one canonical transaction and record its receipt. |
| `world_tick` | write | Advance bounded ticks as individually receipted transactions. |
| `world_snapshot` | read | Return a complete canonical snapshot as bounded base64. |
| `world_diff` | read | Compare a supplied snapshot with another snapshot or current authority. |
| `render_capture` | capture | Return bounded provider-neutral RGBA8 capture metadata and optional pixels. |
| `telemetry_get` | read | Return bounded non-authoritative service/application telemetry. |
| `test_run` | tests | Run only explicitly registered, in-process checks by stable name. |

Read capability is always available. Write, capture, and test capabilities are
independent and disabled unless the trusted composition root enables them.
Validation remains available when writes are disabled because it cannot adopt
the staged result.

`world_tick` returns one receipt for every committed tick. Each tick is an
atomic, replayable branch boundary; a multi-tick request is deliberately not
one all-or-nothing transaction. The service stops at the first rejection and
never describes rejected work as committed.

## Python composition

Applications construct `AgentCommandService` with explicit project metadata,
an owned `WorldSession`, an actor, capabilities, limits, and optional capture,
test, and telemetry providers. The service owns and closes the capture provider.
It does not own the clock, session, test provider, or telemetry provider.

The service is single-thread-owned by its constructing thread. Mutation calls
are serialized through a non-blocking gate: concurrent, wrong-thread, and
reentrant mutations fail with structured errors instead of waiting or racing.
Read calls return detached documents and cannot mutate authority.

The built-in data-only project composition is exposed through the CLI. A
typical read-only call uses a project-relative canonical request file:

```console
ludoweave agent PROJECT world_describe empty-request.json
ludoweave agent PROJECT transaction_validate transaction-request.json
```

Mutation requires an explicit capability grant:

```console
ludoweave agent PROJECT transaction_apply transaction-request.json --write
```

`--state SNAPSHOT` loads a project-relative input snapshot. `--actor-kind` and
`--actor-id` bind the caller recorded on accepted transaction work. Inputs use
the same project confinement and bounded-handle reads as the M2 workflow.

## Local MCP adapter

`ludoweave mcp` is a small local standard-input/standard-output adapter over
`AgentCommandService`:

```console
ludoweave mcp PROJECT
ludoweave mcp PROJECT --write --actor-id local-builder
ludoweave mcp --sample agent-world-builder --write
ludoweave mcp --sample agent-world-builder --write --renderer wgpu
```

Configure any MCP client that supports local stdio by supplying an executable
and arguments equivalent to this vendor-neutral description (individual client
configuration field names differ):

```json
{
  "transport": "stdio",
  "command": "ludoweave",
  "args": ["mcp", "/absolute/path/to/trusted/project"]
}
```

Install the wheel in the client's environment or replace `command`/`args` with
the environment manager invocation used by that trusted project. Add `--write`
only for a client that should mutate the world; do not put credentials in the
arguments because this local transport defines no authentication protocol.

It implements MCP revision `2025-11-25` initialization, ping, tool discovery,
and tool calls using newline-delimited UTF-8 JSON-RPC messages. Standard output
contains protocol messages only. Tool success returns both `structuredContent`
and a canonical JSON text block; expected LudoWeave errors are tool results with
`isError: true`. Duplicate JSON keys, batches, non-finite constants, oversized
messages, duplicate request IDs, calls before initialization, and unsupported
methods are rejected.

The adapter intentionally has no socket, HTTP, authentication, discovery, or
remote listener. Stdio process access is the security boundary. The current
wire behavior follows the official [MCP transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports),
[lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle),
and [tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
contracts without adding an MCP runtime dependency.

## Owned semantic inspector

`ludoweave inspect` is an M10 client of this same local MCP surface. It starts
only the built-in `python -I -m ludoweave mcp` child, observes through typed tools,
and emits a versioned newline-delimited stream of world descriptions, stable
queries, telemetry, transition receipts, and semantic diffs. It does not read
ECS storage directly or keep another world model.

The inspector is read-only unless `--write` is present. Its optional sample
bootstrap and tick advancement use `transaction_apply` and one-tick
`world_tick` calls with exact hash chaining. It cannot select an arbitrary
child command, capture provider, registered test, network endpoint, or remote
process. See the [live semantic inspector guide](inspector.md) and ADR-0025 for
the complete stream, ownership, failure, and non-scope contract.

## Limits and data handling

Default service bounds include a 1 MiB request, 8 MiB result, 256 commands per
transaction, 600 ticks per request, 1,000 query entities, 64 MiB decoded
snapshot, 2,073,600 capture pixels, 32 selected tests, and 120 calls per
60-second monotonic window. A composition root may inject different positive
limits. The outer result bound can be lower than a domain artifact bound; in
that case callers must use a smaller artifact or another trusted local workflow.

Diagnostics and telemetry recursively redact values whose keys indicate a
secret, password, or token. Results never include filesystem paths, environment
values, provider objects, world-storage aliases, or render-native handles.
Capture bytes are immutable tightly packed RGBA8 and can be omitted while still
returning dimensions and a SHA-256 digest.

The rate window uses an injected monotonic clock and is not authoritative game
state. Telemetry, capture pixels, request counts, and wall-clock behavior never
enter world hashes.

## Agent World Builder acceptance loop

`examples/agent_world_builder.py` composes an ECS-authoritative room, player,
light, props, and effect through ordinary typed transactions. It describes the
project and world, snapshots the baseline, validates and applies the build,
ticks three individually receipted frames, captures a 320x180 offscreen image,
queries and adjusts the player, computes a semantic diff, runs four registered
acceptance checks, reads telemetry, and emits replay evidence.

Run it with the real optional renderer:

```console
uv run --frozen --extra graphics python examples/agent_world_builder.py
```

The example has no editor, remote control, scene importer, arbitrary code
execution, or parallel authority. It is an acceptance composition for the M5
protocol boundary, not a general project/plugin format.

## Installed adapter conformance

M18 turns the exact 12-tool service path into protocol
`ludoweave.agent-tool-conformance/1`, profile `agent-tool-baseline/1`. A caller
explicitly imports a trusted local adapter factory and passes it to
`run_agent_tool_conformance()`. The runner owns one fresh adapter, exercises
detached reads, command validation/application and receipts, stale-hash
atomicity, ticks, query/diff/provider result shapes, and close semantics, then
emits a deterministic sanitized report.

The profile performs no discovery, dynamic import, installation, filesystem
scan, subprocess launch, network connection, or global registration. It is
behavioral evidence rather than trust, transport security, provenance,
performance, cross-platform, or real-agent recovery evidence. See the
[agent-tool conformance guide](agent-tool-conformance.md).
