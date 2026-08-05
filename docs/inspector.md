# Live semantic inspector

M10 adds a headless client that owns one local LudoWeave child process and
observes its canonical world through the existing typed MCP tools. It does not
attach to an arbitrary process and does not create another world store.

## Start a bounded session

Inspect the built-in Agent World Builder composition without mutation:

```console
ludoweave inspect --sample agent-world-builder
```

Inspect a trusted data-only project, optionally from a project-relative
snapshot:

```console
ludoweave inspect PROJECT
ludoweave inspect PROJECT --state world.lws
```

The parent launches exactly the current interpreter as
`python -I -m ludoweave mcp` with the selected project or built-in sample.
Isolated mode prevents the working directory, `PYTHONPATH`, and user site from
redirecting the child to a shadow package. The command has no executable,
shell, module, URL, host, port, discovery, or remote attach option.

The default session is read-only. The built-in sample can be created and then
advanced only with an explicit write grant:

```console
ludoweave inspect --sample agent-world-builder --write --bootstrap --ticks 2
```

`--bootstrap` submits the sample's existing versioned transaction. Every
`--ticks` step calls `world_tick` for exactly one tick. Both paths return
ordinary receipts, use the latest expected world hash, and observe only after
the mutation safe point has completed. Bootstrap is intentionally available
only for the named built-in sample.

## Observation stream

Standard output is newline-delimited JSON. Every line is one
`ludoweave.inspector.event/1` document with:

- a zero-based `sequence`, `event: "observation"`, and cause of `initial`,
  `bootstrap`, or `tick`;
- the detached result of `world_describe`;
- a stable bounded `world_query` result;
- detached non-authoritative telemetry;
- the typed transition result and receipt, or `null` for the initial read; and
- a semantic diff from the prior authority image, or `null` for the initial
  read.

The inspector obtains a snapshot to establish the exact authority hash and to
request the next semantic diff, but it never emits that base64 snapshot. It
requires the world, query, telemetry, transition, and diff hashes to describe
one continuous state chain. A disagreement is a structured protocol failure,
not a partial success claim.

The stream contains no filesystem path, environment value, process ID,
provider-native object, or mutable world alias. Output order and JSON key order
are stable for identical observations, but telemetry call counts are
diagnostic and do not enter canonical state.

## Bounds and failures

One session accepts at most 600 requested ticks and a query limit from 1 to
1,000. Requests are limited to 1 MiB and child responses/events to 16 MiB.
Oversized worlds therefore fail closed instead of silently truncating the
authority or diff. Use `--query-limit` to reduce entity detail; this does not
change the world.

The parent verifies MCP revision `2025-11-25`, initialization ordering,
required tool discovery, response IDs, JSON shapes, typed tool errors,
transition status, tick count, and hash continuity. Expected failures are
reported on standard error as `ludoweave.cli.error/1` with stable
`tools.inspector_*` codes. Standard output contains only complete observation
lines emitted before the failure.

The parent owns stdin, stdout, stderr, and the child lifetime. It closes child
input and waits after success; after an exception it still closes the process,
and a child that does not exit within the bounded close interval is killed.
The inspector creates no listener, background thread, polling timer, retained
daemon, or orphan by design.

## Deliberate limitations

This is a finite headless protocol session, not a GUI, TUI, visual editor,
wall-clock watcher, process browser, debugger, or network agent transport. It
does not accept arbitrary commands and cannot invoke capture or registered
test tools. Rich visual inspection and remote attachment require separate
future security, ownership, and product decisions.
