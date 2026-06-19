# Security Gates

## Blocking Conditions

| Gate | Tool | Failure Condition |
|---|---|---|
| SAST | Bandit | High severity Python finding |
| Dependency Scan | pip-audit | Vulnerable secure dependency |
| Secret Scan | Gitleaks | Secret detected |
| Config Scan | Trivy config | HIGH or CRITICAL misconfiguration |
| Container Scan | Trivy image | HIGH or CRITICAL vulnerability |
| Code Scanning | CodeQL | CodeQL security finding |
| DAST | ZAP Baseline | Baseline alerts above accepted threshold |

## Report-Only vs Blocking

Report-only workflows create evidence.

Blocking workflows enforce policy and fail pull requests when serious issues are found.
