# Security Policy

## Supported versions

LudoWeave is pre-alpha and has no supported release line yet. Security fixes are applied to the default branch until a version-support policy is announced.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability.

Use the repository's **Security** tab and choose **Report a vulnerability** to create a private GitHub security advisory. Include the affected revision, impact, reproduction steps, and any suggested mitigation. Do not include unrelated secrets or personal data.

If private vulnerability reporting is unavailable, use GitHub Support to contact the repository owner rather than disclosing the report publicly.

Maintainers will acknowledge the report through the same private channel, assess impact, coordinate a fix when warranted, and credit reporters who request attribution. No response or remediation deadline is guaranteed during pre-alpha.

## Initial security boundaries

- The engine provides no remote control or network listener in M0.
- The CLI performs no arbitrary Python evaluation.
- Diagnostics must not expose environment variables or credentials.
- Future agent-facing mutations must be typed, validated, capability-gated, and auditable.
