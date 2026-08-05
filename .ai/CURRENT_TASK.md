# Current Task

- **Task:** M15 - Visual-editor admission decision
- **Status:** Locally complete and independently accepted on
  `codex/m15-visual-editor-admission`; ready for signed commit, ready PR, and
  the unchanged essential hosted gate.
- **Started:** 2026-08-06
- **Base:** Exact clean `main` evidence commit
  `bfea67d2d922e8c591224d18f56c14d572d7f7da`, after the validated M8-M14
  integration and repository-state evidence PRs.
- **Outcome:** Confirm the installed command/receipt, typed-tool, MCP, and
  inspector foundation while retaining the finite headless inspector and
  deferring visual-editor implementation behind a complete product and
  engineering admission gate.
- **Acceptance gate:**
  - A dependency-free example audits exact installed protocols, operations,
    tools, stability, and inspector configuration; emits deterministic
    versioned JSON; and reports no path, host, environment, process, provider,
    timing, provider-native object/selection, or credential data.
  - Evidence positively confirms receipted semantic operation and the
    read-only inspector foundation while keeping all editor-specific admission
    gates false.
  - The same exact evidence runs from source, an isolated universal wheel, and
    the deterministic release sample bundle.
  - ADR-0029 records target users/jobs, the evidence-to-decision chain,
    tradeoffs, risks, non-goals, and a complete testable revisit gate.
  - Architecture tests keep GUI/TUI imports, editor runtime modules, editor
    root exports, and GUI dependencies absent.
  - Full local quality/artifact/provider and independent review gates pass
    before signed commit, PR, hosted-success, or integration claims.
  - The existing eight-job essential CI topology remains unchanged.
- **Architecture:** M15 adds repository evidence, tests, and documentation
  only. The example is a composition root that inspects installed engine-owned
  contracts and explicitly reports the inspector as internal. `src/`, public
  APIs, persistent formats, dependencies, lock, version, and CI remain
  unchanged.
- **Non-scope:** GUI/TUI/editor implementation, toolkit choice, public
  inspector promotion, document/scene formats, selection, undo/redo, property
  panels, viewport/picking/gizmos, asset browser/import, autosave/recovery,
  editor plugins, networking, remote attach, arbitrary child commands, 3D,
  Box2D, SDL3, WASM, native code, tags, releases, or package publication.
- **SemVer:** Repository decision evidence and documentation only; no public
  Python API, persistent schema, dependency, runtime version, or compatibility
  surface changes.
- **Current evidence:** Commands, transactions, receipts, agent service,
  inspector events, and MCP all have explicit revisions; twelve typed tools
  operate the same authority; and the owned inspector defaults read-only. The
  agent surface is still experimental, `ludoweave.tools` is internal, and no
  editor-specific authoring, recovery, usability, packaging, performance, or
  support contract exists.
- **Final local gate:** 834 tests pass with one existing Windows
  symlink-capability skip; 182 Python files are formatted; Ruff, Pyright,
  strict docs, universal wheel/sdist build, exact installed-wheel evidence,
  fresh ten-artifact release smoke, nine real-wgpu tests, and every inherited
  documented benchmark/profile validator pass. Independent findings-first
  review approved after installed mutation, export/stability, dependency,
  root-export, and stale-state evidence gaps were corrected.
