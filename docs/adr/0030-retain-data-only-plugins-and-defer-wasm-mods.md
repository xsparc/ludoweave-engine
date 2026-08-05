# ADR-0030: retain data-only plugins and defer WASM mods

- Status: Accepted
- Date: 2026-08-06

## Context

The post-alpha plan identifies WebAssembly mods as a separate security
workstream. The M12 plugin contract is deliberately inert: exact-schema
compatibility metadata can describe engine, Python, platform, capability,
determinism, native, and plugin requirements, but cannot select or execute an
artifact, module, entry point, import, or hook.

WebAssembly core gives guests no ambient host access; the embedder chooses all
imported capabilities and remains responsible for security policy. LudoWeave
has not yet defined the guest ABI, resource limits, deterministic profile,
trap atomicity, persistent guest state, package trust, runtime supply chain,
isolation boundary, conformance suite, or security-maintenance ownership that
an untrusted-mod feature requires.

Adding a runtime first would create a native security boundary and pressure
the project to expose authority through ad hoc host functions. Core memory
safety would not by itself preserve commands/receipts, determinism,
availability, project confinement, or safe lifecycle behavior.

## Decision

Retain the M12 data-only plugin boundary and defer executable WASM mods. M16
adds only a threat model, deterministic installed-surface evidence, exact
artifact validation, architecture guards, and documentation. It adds no
runtime source, dependency, public API, persistent format, executable manifest
field, compiler, WASI context, host call, loader, lock change, version change,
or CI job.

`examples/wasm_mod_security_decision.py` emits one deterministic
`ludoweave.evaluation.wasm-mod-security/1` document. It derives installed
public/plugin exports, stability, manifest fields and capabilities, and
distribution requirements. It proves that representative executable fields
are rejected through typed structured errors, that no WASM runtime requirement
is present, and that all admission gates remain false. Source, isolated-wheel,
and release-bundle smoke require the exact document.

A future proposal must supersede this ADR and satisfy the complete gate in the
[M16 security decision](../wasm-mod-security-decision.md): runtime provenance
and support; package identity/distribution; default-deny copied capabilities;
command/receipt-only world mutation; deterministic and independent execution
limits; atomic traps and lifecycle; deterministic replay; guest-state
migrations; justified isolation; adversarial testing; cross-platform installed
conformance; and named security/update ownership.

## Consequences

- Plugin manifests remain compatibility metadata, not a discovery or execution
  format. Unknown executable fields continue to fail closed.
- Untrusted Python and untrusted WASM are not executed by LudoWeave. Trusted
  applications may still explicitly compose adapters in ordinary Python under
  the existing adapter guide; that is not a sandbox claim.
- No WASI capability is ambient or implied by a manifest capability label.
- Every future guest-requested mutation must cross the existing typed
  command/transaction boundary and produce a receipt. Runtime/guest objects may
  not enter public APIs, ECS records, snapshots, receipts, or replay artifacts.
- Explicit architecture fixtures reject common WASM runtime imports. Changing
  the guard requires an assigned superseding milestone and the complete gate,
  not only a successful runtime prototype.
- The ordinary pure-Python wheel and optional graphics extra remain unchanged.

## References

- [WASM-mod security admission decision](../wasm-mod-security-decision.md)
- [Plugin manifests and compatibility](../plugins.md)
- [Security policy](https://github.com/xsparc/ludoweave-engine/blob/main/SECURITY.md)
- [WebAssembly core security considerations](https://webassembly.github.io/spec/core/intro/introduction.html#security-considerations)
- [Wasmtime security](https://docs.wasmtime.dev/security.html)
- [WASI interface inventory](https://wasi.dev/releases)
- [RFC-0002: data-only plugin manifests](../rfcs/0002-data-only-plugin-manifest-compatibility.md)
