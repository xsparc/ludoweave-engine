# WASM-mod security admission decision

M16 evaluates the post-alpha question “should LudoWeave execute untrusted
WebAssembly mods?” The answer is **not yet**. LudoWeave retains the M12
data-only plugin boundary and defers any WASM runtime, loader, guest ABI, or
host-call implementation behind a complete security and determinism gate.

This is a threat model and admission decision, not a sandbox prototype. M16
adds no runtime dependency, executable manifest field, compiler, JIT, WASI
context, guest memory, host function, discovery mechanism, or mod package
format. There is currently no LudoWeave WASM execution path to exploit.

## Why the core sandbox is not the whole product boundary

The WebAssembly core specification provides memory-safe execution and no
ambient host access, but explicitly makes the embedder responsible for every
imported environmental capability. It also permits embedders to impose module
and execution limits. Those properties are valuable foundations; they do not
choose LudoWeave’s authority, resource, lifecycle, persistence, or determinism
policy. See the official [core security
considerations](https://webassembly.github.io/spec/core/intro/introduction.html#security-considerations)
and [implementation-limit
model](https://webassembly.github.io/spec/core/appendix/implementation.html).

Wasmtime’s official security guidance makes the same boundary concrete: guest
interaction is limited to explicitly linked interfaces, yet embedders must
still distrust guest values, contain denial of service, select capabilities,
and maintain the runtime. WASI can expose filesystem, socket, HTTP, CLI,
environment, clock, and random interfaces, so merely selecting “WASI” is not a
least-privilege policy. See [Wasmtime security](https://docs.wasmtime.dev/security.html),
[Wasmtime’s vulnerability model](https://docs.wasmtime.dev/security-what-is-considered-a-security-vulnerability.html),
and the official [WASI interface inventory](https://wasi.dev/releases).

## Threat model

### Assets and actors

| Area | In scope |
| --- | --- |
| Assets | Canonical ECS/world authority, commands and receipts, snapshots and replays, project assets, process confidentiality, CPU/memory/storage budgets, availability, deterministic outcomes, and release integrity |
| Trusted actors | Game authors choosing a mod, application composition roots, maintainers, and the engine-owned command service |
| Untrusted actors | Mod producers, module bytes, guest state and outputs, guest-selected identifiers, malformed packages, and compromised distribution sources |
| Entry points | Package/manifest decode, module validation/compilation, instantiation, imports/exports, tick/event callbacks, guest memory copies, persistence, diagnostics, and cache reuse |
| Privileged operations | World mutation, filesystem/network/process access, clocks/randomness, persistence, rendering/audio devices, logging, and resource allocation |

### Trust boundaries and data flow

1. Untrusted artifact bytes cross into bounded package and module parsing.
2. A validated module crosses into a selected runtime and compiler/interpreter.
3. Guest values cross linear memory into copied, validated host values.
4. Guest requests cross a default-deny capability table into engine-owned host
   functions.
5. World changes cross only the existing versioned command/transaction service
   and produce receipts; guest code never receives ECS aliases.
6. Traps, cancellation, close, and process failure cross back into atomic
   recovery and sanitized diagnostics.
7. Persistent guest state crosses a versioned snapshot/replay/migration format,
   if one is ever admitted.

None of this executable-mod flow exists in M16. The only adjacent current path
is the separately defined M12 decoder for inert compatibility metadata; it
cannot identify or carry module bytes. The flow above describes the minimum
future review surface, not implemented behavior.

## Blocking findings

These are prospective feature blockers, not vulnerabilities in the current
data-only implementation. Severity describes the impact if executable mods
were added without the stated control.

| ID | Severity | Finding and impact | Required remediation and verification |
| --- | --- | --- | --- |
| WM-01 | Critical | An imported host function could grant ambient authority or mutate ECS state outside receipts. | Define a versioned default-deny capability ABI. Copy and validate every guest value. Route every mutation through commands/transactions and assert receipt/hash continuity in adversarial conformance tests. |
| WM-02 | High | Guest execution, compilation, recursion, memory growth, tables, logs, or host calls could exhaust the engine process. | Set tested limits for artifact size/structure, compilation, fuel, cancellation, memory, tables, stack, output, calls, and cache. Fuel is the deterministic work meter; coarse epoch interruption is only a second cancellation boundary. Wasmtime documents this distinction in its [store API](https://docs.wasmtime.dev/api/wasmtime/struct.Store.html). |
| WM-03 | High | Ambient WASI or broad host imports could expose files, sockets, process arguments, environment values, clocks, or randomness. | Start with no WASI and no imports. Admit each copied capability separately with project confinement, explicit ownership, quotas, deterministic classification, and negative tests. |
| WM-04 | High | Runtime, compiler, binding, or unsafe precompiled artifacts add a native sandbox and supply-chain boundary. | Select and pin a maintained candidate only after wheel/provenance/support review; track advisories and update ownership; isolate compilation/execution as the final threat model requires. Never deserialize untrusted precompiled native artifacts—the official [Wasmtime precompile guidance](https://docs.wasmtime.dev/examples-pre-compiling-wasm.html) warns that this can permit arbitrary code execution. |
| WM-05 | High | Host clocks/randomness, nondeterministic imports, floating-point edge cases, scheduling, runtime upgrades, or platform differences could break hashes and replay. | Define a versioned deterministic guest profile, engine-owned clock/random inputs, host-call ordering, numeric rules, runtime identity, and Windows/macOS/Linux replay/hash conformance. Classify nonconforming mods D0 and exclude them from authoritative replay. |
| WM-06 | High | A trap, timeout, reentrant callback, or host failure could leave partially applied state or violate single-thread ownership. | Execute at explicit safe points against staged authority, define trap receipts and rollback, prohibit reentrancy, close resources exactly once, and test cancellation/failure at every boundary. |
| WM-07 | Medium | Guest state could become unversioned opaque save data that cannot migrate, inspect, revoke, or replay. | Specify bounded canonical state, compatibility identity, migrations, unknown-field policy, recovery, and replay semantics before persistence. |
| WM-08 | Medium | Package identity, provenance, dependencies, updates, and revocation have no policy. | Define a separate versioned mod-package contract, content identity, trust UX, dependency policy, update/revocation behavior, and maintenance owner. Signatures may establish provenance; they do not make hostile behavior safe. |

Defense in depth after those blockers includes an owned child-process boundary,
compiler/executor separation, reduced runtime features, malicious corpora,
fuzzing, differential execution, terminal-output filtering, cache quarantine,
and platform sandboxing. Those controls cannot replace the command/receipt and
least-privilege host ABI.

## Residual risk after admission controls

Even a future implementation that satisfies every gate would retain material
risk:

- a runtime, compiler, binding, or platform sandbox can contain an unknown
  escape or memory-safety vulnerability;
- embedder code can validate the wrong guest value, grant more authority than
  intended, or mishandle reentrancy and cleanup;
- fuel, memory, process, and output limits reduce but cannot eliminate denial
  of service or pathological host work;
- machine-code execution can retain hardware side-channel exposure, which the
  WebAssembly core security considerations explicitly leave to embedders; and
- runtime, compiler, dependency, operating-system, and CPU changes can alter
  both security posture and deterministic conformance.

Admission would therefore require a named security owner, private advisory
intake, supported-version and urgent-update policy, emergency disable/revocation
path, and an explicit ADR accepting the measured residual risk. Process
isolation and platform sandboxing are defense in depth, not a claim that hostile
guest execution is risk-free. Authoritative compositions must still fail closed
when the pinned runtime or deterministic profile is unsupported.

## Reproducible installed evidence

Run:

```console
python examples/wasm_mod_security_decision.py
```

It emits one deterministic `ludoweave.evaluation.wasm-mod-security/1` JSON
document. The audit derives the exact installed plugin exports, preview
stability map, manifest fields/capabilities, complete exact distribution
requirements, and
root exports. It positively proves that executable fields are rejected with a
typed `plugins.invalid_manifest` error and records no WASM runtime requirement
or public execution export.

The exact document is validated from source, an isolated universal wheel, and
the deterministic release sample bundle. Architecture fixtures explicitly
reject common WASM runtime imports and keep the runtime dependency set
unchanged.

## Complete admission gate

A future assigned proposal must supersede ADR-0030 and satisfy every item
together:

1. a selected runtime/binding with pinned provenance, CPython 3.12–3.14 wheels
   on Windows, macOS, and Linux, no mandatory compiler, and a named update owner;
2. a versioned mod package and capability manifest distinct from the inert M12
   compatibility metadata, with identity, dependency, distribution, update,
   trust, and revocation policy;
3. no ambient WASI; a default-deny host ABI with explicit copied capabilities,
   validation, quotas, redaction, ownership, and close semantics;
4. all world mutation mapped to versioned commands/transactions and receipts,
   with no guest or runtime object in public APIs or canonical state;
5. deterministic fuel plus independent cancellation, bounded compile work,
   artifact/module structure, memory/table/stack, host-call, output, diagnostic,
   and cache budgets;
6. staged atomic trap/timeout behavior, safe-point scheduling, reentrancy rules,
   thread ownership, cleanup, recovery, and typed failure receipts;
7. a deterministic profile for numeric behavior, clocks, randomness, host-call
   order, runtime identity, upgrades, and cross-platform replay hashes;
8. versioned snapshot/replay/migration semantics for any persistent guest state;
9. a justified in-process or owned-process isolation decision that accounts for
   runtime bugs, denial of service, compiler exposure, and platform sandboxing;
10. malicious module/package corpora, parser/runtime fuzzing, host-ABI property
    tests, cross-runtime differential tests where useful, and negative
    capability tests;
11. same-artifact installed conformance on every supported OS/Python target;
    and
12. an advisory intake, patch/backport policy, emergency disable/revocation
    path, measured performance/resource budget, and named maintenance owner.

Passing a “hello world” module, choosing a runtime, or demonstrating core
memory isolation does not authorize executable mods.

## Decision

Retain the data-only plugin boundary and defer WASM mods. The tradeoff is no
untrusted mod execution today in exchange for keeping canonical authority,
headless determinism, least privilege, supply-chain size, and the ordinary
CPython baseline intact.

See [ADR-0030](adr/0030-retain-data-only-plugins-and-defer-wasm-mods.md), the
[plugin guide](plugins.md), and the repository [security
policy](https://github.com/xsparc/ludoweave-engine/blob/main/SECURITY.md).
