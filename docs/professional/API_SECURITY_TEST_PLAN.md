# API Security Test Plan

## Scope

The Flask lab app exposes `/health`, `/`, `/user`, `/ping`, and `/hello`. The vulnerable version is used for exploitation evidence. The hardened version is used for remediation proof.

## Test categories

| Category | Test | Evidence |
|---|---|---|
| Authentication/authorization | Validate sensitive routes do not expose privileged data without auth | Future improvement |
| Input validation | SQLi payloads against `/user` | `screenshots/035-sql-injection-proof.png` |
| Command injection | Shell metacharacters against `/ping` | `screenshots/036-command-injection-proof.png` |
| Template injection | Template expressions against `/hello` | Finding report |
| Security headers | CSP, XFO, XCTO, Referrer-Policy, Permissions-Policy | `tests/test_security_headers.py` |
| Error handling | Invalid inputs return 400 without stack traces | `tests/test_hardened_app.py` |
| Dependency risk | pip-audit | `security/reports/pip-audit-report.json` |
| SAST | Bandit | `security/reports/bandit-report.json` |

## Recommended negative tests

```bash
curl "http://localhost:5000/user?id=1'%20OR%20'1'='1"
curl "http://localhost:5000/ping?host=127.0.0.1;%20echo%20DEVSECOPS_CMD_INJECTION_TEST"
curl "http://localhost:5000/hello?name={{7*7}}"
```

## Recommended hardened behavior

| Payload | Hardened response |
|---|---|
| SQLi string | Treated as data or rejected |
| `; echo test` | HTTP 400 invalid host |
| `{{7*7}}` | Rendered as escaped text, not evaluated |
