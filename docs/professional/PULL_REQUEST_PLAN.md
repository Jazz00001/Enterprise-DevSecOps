# Pull Request Plan

Use these PRs to make the project look like an enterprise team workflow.

| PR | Title | Files | Purpose |
|---|---|---|---|
| PR-001 | Fix baseline security headers and make tests pass | `src/app/app.py`, `tests/` | Shows quality gate discipline |
| PR-002 | Add hardened reference implementation | `src/app/app_hardened.py`, `tests/test_hardened_app.py` | Shows remediation ability |
| PR-003 | Add evidence chain-of-custody | `scripts/generate_evidence_manifest.py`, `docs/professional/evidence_manifest.csv` | Shows audit readiness |
| PR-004 | Add governance templates | `.github/`, `SECURITY_EXCEPTION_TEMPLATE.md` | Shows enterprise repo maturity |
| PR-005 | Add compliance/control mapping source docs | `docs/professional/` | Shows reporting maturity |
| PR-006 | Clean author metadata in public reports | `docs/` | Fixes credibility risk |
