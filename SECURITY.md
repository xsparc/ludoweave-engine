# Security Policy

## Supported versions

LudoWeave is pre-alpha and has no supported release line yet. Security fixes are applied to the default branch until a version-support policy is announced.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability.

Use the repository's **Security** tab and choose **Report a vulnerability** to create a private GitHub security advisory. Include the affected revision, impact, reproduction steps, and any suggested mitigation. Do not include unrelated secrets or personal data.

If private vulnerability reporting is unavailable, use GitHub Support to contact the repository owner rather than disclosing the report publicly.

Maintainers will acknowledge the report through the same private channel, assess impact, coordinate a fix when warranted, and credit reporters who request attribution. No response or remediation deadline is guaranteed during pre-alpha.

## Initial security boundaries

- The engine provides no remote control or network listener through M2.
- The CLI performs no arbitrary Python evaluation.
- M2 artifact paths are bounded, project-relative, resolved beneath an explicitly selected project root, and reported only by stable roles in expected diagnostics.
- Input files are read through one bounded open handle; stale size metadata cannot cause an unbounded read.
- Project confinement protects normal workflows and static symlink/traversal mistakes. It is not a sandbox against a hostile local principal concurrently replacing files, directories, junctions, or symlinks inside the selected project tree; run commands only against a locally trusted, quiescent project directory.
- The M2 CLI project manifest is data-only and cannot select Python modules, callables, components, or plugins.
- Diagnostics must not expose environment variables or credentials.
- Future agent-facing mutations must be typed, validated, capability-gated, and auditable.
