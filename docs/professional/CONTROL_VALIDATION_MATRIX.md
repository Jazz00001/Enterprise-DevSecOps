# Control Validation Matrix

| Control ID | Domain | Risk | Control implemented | Evidence | Status | Retest criteria |
|---|---|---|---|---|---|---|
| APP-001 | AppSec | SQL injection through string-built query | Parameterized query in hardened app | `src/app/app_hardened.py`, `tests/test_hardened_app.py` | Reference fix added | Injection payload returns zero/one row and is treated as data |
| APP-002 | AppSec | OS command injection via shell execution | `shell=False`, host validation, timeout | `src/app/app_hardened.py` | Reference fix added | Payload containing `; echo` rejected with 400 |
| APP-003 | AppSec | Unsafe template rendering/SSTI | Escape user input before template render | `src/app/app_hardened.py` | Reference fix added | `{7*7}` is rendered as text, not evaluated |
| APP-004 | Web security | Missing browser security headers | Flask `after_request` hook | `src/app/app.py`, `tests/test_security_headers.py` | Implemented | All core routes return required headers |
| CI-001 | SAST | Insecure code reaches main | Bandit gate | `.github/workflows/security-gates.yml` | Existing | High/Medium count within threshold |
| CI-002 | SCA | Known vulnerable dependencies | pip-audit gate | `.github/workflows/security-gates.yml`, `security/reports/pip-audit-report.json` | Existing | Zero unaccepted vulns or documented exception |
| CI-003 | Container security | Vulnerable image promoted | Trivy image gate | `.github/workflows/security-gates.yml` | Existing | No critical vulns; high vulns under threshold |
| CI-004 | Repository security | Secrets/misconfigs in repo | Trivy fs secret/misconfig scan + gitleaks config | `.gitleaks.toml`, security reports | Enhanced | No verified secrets in repo |
| K8S-001 | Pod hardening | Privileged/root pod | Non-root, no privilege escalation, drop caps | `k8s/base/deployment.yaml` | Existing | Insecure pod blocked; secure pod admitted |
| K8S-002 | RBAC | Excessive service account permissions | Least privilege Role/RoleBinding | `k8s/base/rbac.yaml` | Existing | Service account cannot read secrets/cluster resources |
| K8S-003 | Network isolation | Lateral movement between pods | Default deny + explicit allow | `k8s/base/network-policy.yaml` | Existing | Untrusted pod blocked; approved client allowed |
| K8S-004 | Admission control | Unsigned/unlabeled workload | Gatekeeper/Kyverno policy | `security/policies/` | Existing | Missing labels rejected |
| SC-001 | SBOM | Unknown components | Syft SPDX/CycloneDX SBOM | `security/sbom/` | Existing | SBOM generated per image digest |
| SC-002 | Image integrity | Tampered/unsigned image | Cosign signing/verification evidence | `security/reports/cosign-image-verify.txt` | Existing | Verify succeeds for signed digest |
| SC-003 | Provenance | Build origin unknown | SLSA-style provenance | `security/provenance/slsa-provenance.json` | Existing | Provenance attached and verified |
| DET-001 | Runtime detection | Privileged container activity undetected | Falco rules/events | `security/reports/falco-*.txt` | Existing | Alert generated for attack simulation |
| GOV-001 | Evidence integrity | Screenshots cannot be trusted | SHA256 evidence manifest | `docs/professional/evidence_manifest.csv` | Added | Hashes reproduce locally |
| GOV-002 | Ownership credibility | Reports contain wrong author name | Name audit and regeneration plan | `scripts/name_audit.py` | Added | No public report contains wrong author |
