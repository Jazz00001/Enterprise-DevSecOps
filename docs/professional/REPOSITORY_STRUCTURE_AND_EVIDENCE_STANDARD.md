# Repository Structure and Evidence Standard

## Purpose

This document defines where every project artifact should live so the GitHub repository looks like a real enterprise security assessment rather than a collection of screenshots.

## Golden rule

Every vulnerability or control claim in the README must map to one of these evidence types:

| Claim type | Required evidence |
|---|---|
| Vulnerability found | Finding report, screenshot, vulnerable request/response, tool output, affected file/line |
| Control implemented | Code diff, configuration file, CI job, policy file, test result |
| Control validated | Retest screenshot, passing test, blocked deployment proof, scan output after fix |
| Compliance mapped | Control matrix row with framework/control/evidence path |
| Runtime detected | Falco log, Prometheus metric, dashboard screenshot, alert rule |

## Recommended naming convention

```text
screenshots/035-sql-injection-proof.png
security/reports/bandit-report.json
docs/professional/findings/FINDING-APP-001-sql-injection.md
docs/professional/retest/RETEST-APP-001-sql-injection.md
docs/professional/evidence_manifest.csv
```

## Evidence minimum fields

Each evidence item should have:

| Field | Example |
|---|---|
| Evidence ID | EVD-APP-001 |
| File path | screenshots/035-sql-injection-proof.png |
| Control/finding | FINDING-APP-001 SQL injection |
| Tool/source | Browser/curl/Bandit/Trivy/Falco/kubectl |
| Date collected | 2026-06-18 |
| Expected result | Injection returns multiple rows |
| Actual result | Multiple rows returned |
| Integrity | SHA256 in evidence manifest |

## Public README evidence rule

Do not paste every screenshot in the README. Use 8-12 high-value screenshots only:

1. Architecture diagram
2. API running
3. SQL injection proof
4. Command injection proof
5. Bandit finding
6. Trivy dependency/image finding
7. Kyverno/Gatekeeper blocked insecure deployment
8. Secure deployment running
9. Argo CD synced/healthy
10. Cosign verify/SBOM proof
11. Falco runtime alert
12. Final passing pipeline/security gate summary

## What should not be public

Remove or redact:

- Real credentials, tokens, cookies, API keys, cloud account IDs
- Real private IPs if tied to personal infrastructure
- Personal emails in screenshots
- Private keys such as `cosign.key`
- Any report carrying another author's name
