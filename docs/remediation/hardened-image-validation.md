# Hardened Image Validation

## Purpose

This document proves that Dockerfile.hardened runs the remediated Flask application instead of the intentionally vulnerable application.

## Key Dockerfile Fix

The hardened Dockerfile now uses:

- COPY src/app/requirements-secure.txt ./requirements.txt
- CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app_hardened:app"]

## Why This Matters

The original Flask application remains in the repository for attack simulation, scanner evidence, and remediation learning.

The hardened Docker image must run the remediated application to prove the full security lifecycle:

Vulnerable application -> exploitation proof -> secure code remediation -> hardened Dockerfile -> retest validation -> scanner evidence.

## Validation Performed

| Test | Result |
|---|---|
| Docker image CMD check | Image starts app_hardened:app |
| Health endpoint | Returned hardened-flask-app |
| SQL injection retest | Blocked with HTTP 400 |
| Command injection retest | Blocked with HTTP 400 |
| Unsafe rendering retest | Script tag escaped |
| Container user check | Runs as UID 10001 |
| Read-only filesystem test | Write blocked |
| Linux capabilities check | CapEff set to zero |
| Dockerfile config scan | 0 misconfigurations |
| Secure requirements audit | No known vulnerabilities found |

## Evidence Screenshots

- 174-dockerfile-hardened-runs-hardened-app.png
- 175-hardened-image-built-and-cmd-proof.png
- 176-hardened-app-healthcheck-running.png
- 177-hardened-app-injection-retest-blocked.png
- 178-hardened-container-security-proof.png
- 179-hardened-image-scanner-reports-saved.png

## Evidence Files

- Dockerfile.hardened
- src/app/app_hardened.py
- src/app/requirements-secure.txt
- security/reports/pip-audit-secure-requirements.txt
- security/reports/trivy-hardened-image-scan.txt
- security/reports/trivy-dockerfile-hardened-config-scan.txt

## Interview Explanation

The vulnerable app remains intentionally vulnerable for security testing evidence. The hardened Dockerfile runs a separate remediated app using app_hardened:app and a separate secure dependency file using requirements-secure.txt. This proves the project does not only find vulnerabilities, but also remediates and validates them.
