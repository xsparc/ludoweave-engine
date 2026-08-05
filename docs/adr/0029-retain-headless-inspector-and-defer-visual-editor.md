# ADR-0029: retain the headless inspector and defer a visual editor

- Status: Accepted
- Date: 2026-08-06

## Context

The post-alpha plan permits considering a visual editor only after the command
protocol and semantic inspector prove stable. LudoWeave now has versioned
commands, transactions, receipts, agent tools, local MCP, and inspector event
envelopes. The M10 inspector owns an isolated local child, defaults to read-only
access, and observes receipted safe-point mutations with exact hash continuity.

Protocol revision labels alone are not a stability promise. All public agent
symbols remain experimental, `ludoweave.tools` is internal, and the inspector
is a finite composition with one built-in sample. Current contracts do not
define the document, identity, selection, undo, property, viewport, asset,
recovery, accessibility, packaging, or performance behavior a usable editor
must own.

Introducing a GUI before those semantics exist would make toolkit state an
accidental second world model and push product decisions into widgets. It
would also create cross-platform packaging and long-lived support obligations
without user evidence or resource budgets.

## Decision

Retain the headless semantic inspector and defer visual-editor implementation.
M15 adds deterministic installed-surface evidence, exact artifact validation,
architecture guards, and product documentation only. It changes no runtime
package, public export, persistent format, dependency, lock, version, or CI
topology.

`examples/visual_editor_decision.py` emits one deterministic
`ludoweave.evaluation.visual-editor/1` document. It confirms the existing
versioned command/receipt and typed-tool foundation by running one bounded
ephemeral transaction through the installed agent service and checking its
committed receipt, command outcomes, pre/post authority hashes, tick continuity,
and resulting entity count. It derives the exact public export/stability map
and records that the agent surface remains entirely experimental and the
inspector is not public. Source, isolated-wheel, and release-bundle smoke
require the exact document and a deferred decision.

A future assigned proposal must supersede this ADR and satisfy the complete
gate documented in [the M15 decision](../visual-editor-decision.md): public
compatibility and editor command profiles; document/scene round trips;
selection and hierarchy; receipt-preserving undo/conflicts; property metadata;
backend-neutral viewport/picking/gizmos; asset workflows; dirty-state and crash
recovery; accessibility and observed usability; cross-platform installed-app
packaging; measured resource budgets; and named maintenance ownership.

## Consequences

- Human and agent mutations continue to share the existing typed command and
  receipt boundary; no privileged widget-side mutation path is introduced.
- The headless inspector remains internal, finite, local, and read-only by
  default. M15 does not promote it to a public compatibility surface.
- Engine-source architecture checks reject standard-library GUI/TUI/browser
  launch roots, while the existing closed dependency policy rejects external
  GUI frameworks. Editor-named runtime modules and root exports remain absent.
- No GUI toolkit is selected. A future admission proposal must justify its
  application boundary, supply-chain and packaging cost after product and
  protocol gates pass.
- The decision is not a claim that graphical authoring has no value. It records
  that the current evidence is necessary but insufficient for a supportable
  editor.

## References

- [Visual-editor admission decision](../visual-editor-decision.md)
- [Live semantic inspector](../inspector.md)
- [API status](../api-status.md)
- [ADR-0025: owned local semantic inspector](0025-owned-local-semantic-inspector.md)
