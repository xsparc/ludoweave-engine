# ADR-0020: Local stdio MCP adapter

- Status: Accepted
- Date: 2026-08-05

## Context

M5 requires a small local MCP interface without authorizing networking,
remote unauthenticated control, or a second agent-service implementation. The
adapter must preserve transport-independent tool schemas and exact receipt
semantics while keeping protocol dependencies and attack surface small.

## Decision

Implement the MCP `2025-11-25` initialization lifecycle, ping, `tools/list`,
and `tools/call` over newline-delimited UTF-8 JSON-RPC on standard input and
standard output. Standard output is protocol-only. Successful calls include
structured content and an equivalent canonical text block; expected service
failures are MCP tool results marked as errors.

Reject batches, duplicate JSON keys, non-finite constants, duplicate request
IDs, oversized lines, invalid lifecycle ordering, and unsupported methods. The
adapter delegates to exactly one injected `AgentCommandService` and closes it
when the transport exits.

Do not implement sockets, HTTP, discovery, authentication, or a remote
listener. Do not add an MCP SDK dependency in M5. The trusted composition root
selects the project or built-in sample and explicitly enables write/capture/test
capabilities; request data cannot select Python code.

## Consequences

- Local MCP clients discover and call the same 12 typed tools used directly by
  Python and the CLI.
- Process-launch and stdio access form the local security boundary. The adapter
  must not be presented as remotely authenticated or network-ready.
- Hand-maintaining the deliberately small protocol subset requires tests
  against the pinned revision and a future ADR before adding another transport
  or adopting an SDK.

## Alternatives considered

HTTP and socket transports were rejected because M5 does not define
authentication, authorization delegation, origin policy, or deployment
hardening. Adding a general MCP SDK was rejected because the required subset is
small and a runtime dependency would expand the initial boundary. A custom
non-MCP remote protocol was rejected as both out of scope and unnecessary.
