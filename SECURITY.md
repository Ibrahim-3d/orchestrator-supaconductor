# Security Policy

## Supported versions

Security fixes target the latest published SupaConductor release and the current `master` branch.

## Reporting a vulnerability

Do **not** open a public issue containing vulnerability details, exploit steps, credentials, or sensitive logs.

Preferred route:

1. Open the repository's **Security** tab.
2. Use **Report a vulnerability** / private vulnerability reporting when available.
3. Include affected versions, reproduction steps, impact, and any suggested mitigation.

If private vulnerability reporting is not available, start a GitHub Discussion asking the maintainer for a private contact channel **without posting the vulnerability details publicly**.

## Scope

Useful reports include vulnerabilities in:

- hooks and shell execution
- agent/tool permission declarations
- unsafe command construction
- path traversal or arbitrary file writes
- credential or secret exposure
- release/update mechanisms
- third-party integrations bundled or invoked by SupaConductor

Please allow reasonable time for triage and remediation before public disclosure.
