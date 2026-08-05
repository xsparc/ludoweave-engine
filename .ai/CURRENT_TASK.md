# Current Task

- **Task:** M3 — Null and WebGPU 2D rendering vertical slice
- **Status:** Complete; DCO-signed PR #3 is published and corrected hosted run 30993554807 passed all 14 jobs
- **Started:** 2026-08-05
- **Acceptance gate:** Backend types remain isolated; Null and wgpu consume equivalent immutable commands; clear, instanced atlas sprites, cameras, tiles, debug fixtures, resize, capture, loss, resource lifetime, graphs, examples, docs, packages, and 1k/10k evidence pass their executable checks.
- **M3-01 outcome:** Frozen backend-neutral descriptors, scoped generational handles, immutable completed-tick presentation frames, camera interpolation, deterministic texture/layer/z/entity grouping, and explicit target/camera command lists are implemented.
- **M3-02 outcome:** Null resource/command validation, logical retirement, fence-deferred physical reuse, stable render-graph compilation, and deterministic dependency/hazard/lifetime failures are implemented.
- **M3-03 outcome:** Exactly pinned optional wgpu/rendercanvas/GLFW dependencies, isolated imports, structured adapter/device/surface failures, real offscreen and Windows GLFW clear paths, and base-install optionality are implemented.
- **M3-04 outcome:** Built-in WGSL instanced quads, normalized texture-atlas UVs, 64-byte pure-Python instance packing, one draw per normal batch, and 1k/10k benchmark/validator tooling are implemented.
- **M3-05 outcome:** Translated/zoomed/rotated orthographic cameras, stable layers/z, tile batches, debug lines, and built-in 5x7 diagnostic glyphs are implemented and exercised by semantic/GPU fixtures.
- **M3-06 outcome:** Immutable normalized offscreen RGBA capture, resize/minimize/restore/destroy behavior, typed fatal device-loss injection, explicit close, deferred provider destruction, rendering documentation, and ADR-0013 through ADR-0015 are complete.
- **Local gate:** Frozen graphics validation reports 485 passed and one Windows symlink-capability skip; the graphics-free base reports 479 passed and two capability skips; strict quality/docs, pure wheel build, no-dependency installed-wheel smoke, real Windows GLFW example, scans, and the 30-sample M3 artifact/validator pass.
- **Hosted gate:** Initial run 30951328011 exposed missing optional packages in the quality type-check job and no Ubuntu graphics runtime. CI now installs the locked graphics extra for strict provider typing and Mesa Vulkan only for Ubuntu graphics smoke. Corrected run 30993554807 passed quality/docs, seven CPython/OS test jobs, three wheel smokes, and real graphics smoke on Ubuntu/Windows/macOS.
- **Known performance result:** Local 10k extraction/packing p95 is 41.9722 ms and wgpu CPU submission p95 is 6.5363 ms; neither observes the 3 ms starting target. Both keep one normal draw. This is profiling evidence, not a pass claim or native-code authorization.
- **Non-scope retained:** General project/plugin loading, asset pipelines, M4 recorded input/platform events, MCP, physics, audio, networking, editor tooling, automatic device recovery, rich text, 3D, and native acceleration.
- **SemVer:** Additive and corrective experimental `0.1.0.dev0` surface; no compatibility promise or version bump.
