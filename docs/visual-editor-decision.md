# Visual-editor admission decision

M15 evaluates the post-alpha question “is LudoWeave ready for a visual
editor?” The answer is **not yet**. LudoWeave retains the finite headless
semantic inspector and defers editor implementation behind a complete,
testable admission gate.

This is a product and architecture decision, not an editor prototype. M15 adds
no window, GUI/TUI framework, viewport, project format, runtime module, public
API, dependency, or background process.

## Users and jobs

A future visual editor would need to serve three linked user groups:

- game authors need to navigate a project, select stable world objects, edit
  validated properties, preview changes, undo mistakes, and save or recover
  without corrupting canonical state;
- tool-building agents need the same semantic operations, validation results,
  receipts, and observations as humans, without a second privileged mutation
  path; and
- maintainers need one supportable cross-platform application with bounded
  startup, memory, project-size, long-session, recovery, accessibility, and
  packaging behavior.

The primary job is therefore not merely “show a viewport.” It is “make
authoring safe, understandable, reversible, and equivalent across human and
agent workflows.”

## Evidence and decision chain

The installed engine confirms useful foundations:

1. externally initiated world changes use versioned command/transaction
   envelopes and return versioned receipts;
2. twelve typed agent tools expose bounded observation, validation, mutation,
   capture, telemetry, and registered tests;
3. local MCP and inspector event revisions are explicit;
4. the inspector owns one isolated local child, defaults to read-only access,
   and verifies safe-point receipts and state-hash continuity; and
5. Null/headless execution remains the baseline.

Those facts prove semantic operability, not editor readiness. The entire agent
Python surface is still experimental, `ludoweave.tools` is internal, and the
inspector is a finite one-shot composition with one built-in sample. There is
no stable document or scene model, selection/hierarchy identity, undo/redo
grouping, property metadata, viewport picking, asset-authoring workflow,
dirty-state recovery, desktop packaging, usability evidence, or operational
budget.

Building a GUI now would force those missing contracts to emerge through
widget and toolkit choices. That would risk a second state model and accidental
compatibility promises. M15 therefore keeps the headless inspector as the
supported evaluation path and defers the editor.

## Reproducible evidence

Run the dependency-free installed-surface audit:

```console
python examples/visual_editor_decision.py
```

It emits one deterministic
`ludoweave.evaluation.visual-editor/1` JSON document. The document records the
exact protocol revisions, operation/tool names, inspector configuration fields,
read-only default, exact experimental agent status, one actual committed
receipt/hash transition, positive foundation result, and the false state of
every editor-admission gate. It emits no path, host, environment, process,
provider-native object/selection, timing, or credential data.

The exact document is validated from source, an isolated pure wheel, and the
deterministic release sample bundle. Architecture tests prohibit GUI/TUI
standard-library imports as well as third-party dependencies and keep
editor-named runtime modules and root exports absent.

## Complete revisit gate

A future assigned proposal must supersede ADR-0029 and satisfy every item
together:

1. a versioned, installed public inspector/editor compatibility profile with
   a stated deprecation policy;
2. a stable subset of command, receipt, query, diff, and observation semantics
   explicitly supported for authoring workflows;
3. canonical project/document/scene serialization with lossless round trips,
   migrations, unknown-field policy, and failure recovery;
4. stable selection, focus, hierarchy, object identity, and deletion semantics;
5. transaction grouping, undo/redo, stale-state conflict, external-change, and
   crash-recovery rules that never bypass receipts;
6. schema-driven property metadata, validation diagnostics, defaults, ranges,
   units, references, and multi-selection behavior;
7. backend-neutral viewport, camera, picking, overlay, and gizmo contracts that
   preserve a headless Null conformance path;
8. project-confined asset browse/import/reload/save workflows with content
   identity and path safety;
9. explicit dirty-state, autosave, backup, atomic save, reopening, and recovery
   behavior for multiple documents;
10. accessible keyboard-only and screen-reader workflows plus observed
    usability evidence for representative author and agent-assisted tasks;
11. same-build Windows, macOS, and Linux installed-application packaging,
    update, close, crash-isolation, and support ownership; and
12. measured startup, idle CPU, memory, large-project interaction, long-session,
    save/recovery, and artifact-size budgets with named maintainers.

Passing only one gate, choosing a GUI toolkit, or demonstrating a viewport does
not authorize implementation.

## Non-goals and tradeoffs

M15 does not select Qt, GTK, Tk, a browser shell, or another toolkit. It does
not make inspector internals public, promote experimental protocols, add scene
graphs, or define editor plugins. It also does not prohibit a future editor;
it makes the prerequisites observable before the project accepts the ongoing
compatibility and support cost.

The tradeoff is slower arrival of a graphical authoring experience in exchange
for preserving one canonical state model, human/agent parity, headless
conformance, deterministic artifacts, and a small public API.

See [ADR-0029](adr/0029-retain-headless-inspector-and-defer-visual-editor.md)
for the normative decision and [the inspector guide](inspector.md) for the
current bounded tool.
