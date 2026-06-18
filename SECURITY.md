# Security Policy

## Project

**Enterprise DevSecOps Security Lab**  
**Maintainer:** Jagriti Banerjee  
**Repository Type:** Private lab / portfolio / educational DevSecOps security project

---

## 1. Security Policy Overview

This repository is an end-to-end DevSecOps and Kubernetes security lab designed to demonstrate secure software delivery, application security testing, container hardening, Kubernetes security, GitOps, software supply chain security, runtime detection, monitoring, evidence collection, and professional remediation reporting.

The project intentionally includes vulnerable components for controlled testing inside a private lab environment. These vulnerable components are used to demonstrate detection, exploitation proof, remediation, retesting, and documentation practices.

This security policy defines:

- How security issues should be reported.
- Which assets are in scope.
- Which activities are prohibited.
- Which vulnerabilities are intentionally present as part of the lab.
- How severity is assessed.
- How evidence should be submitted.
- How security controls are maintained across the repository.
- How remediation, retesting, and exceptions are handled.

This project must not be used to attack public systems, third-party systems, production infrastructure, or any environment where explicit authorization has not been granted.

---

## 2. Supported Security Scope

Security review is supported for the following project areas:

| Area | Path / Component | Security Focus |
|---|---|---|
| Application Code | `src/app/` | Flask routes, input handling, SQL usage, command execution, template rendering |
| Tests | `tests/` | Health checks, route tests, security header tests |
| Container Build | `Dockerfile`, `docker-compose.yml` | Non-root execution, image hardening, build hygiene |
| CI/CD | `.github/workflows/` | Security gates, SAST, SCA, image scanning, OpenSSF Scorecard |
| Kubernetes | `k8s/base/` | SecurityContext, RBAC, NetworkPolicy, Pod Security, service exposure |
| GitOps | `gitops/argocd/` | ArgoCD application configuration, drift correction, sync behavior |
| Supply Chain | `security/cosign/`, `security/sbom/`, `security/provenance/` | Cosign signing, Syft SBOM, provenance, attestations |
| Policy-as-Code | `security/policies/` | OPA Gatekeeper policies and admission control |
| Runtime Detection | `redteam/`, `monitoring/`, Falco artifacts | Runtime detection, attack simulation, alerting |
| Monitoring | `monitoring/dashboards/`, `monitoring/rules/` | Grafana dashboards, Prometheus rules, Falco metrics |
| Documentation | `docs/`, `SECURITY_FINDINGS_REPORT.md`, reports | Evidence, remediation, compliance mapping, retest proof |

---

## 3. Out-of-Scope Assets

The following are out of scope:

- Public websites or infrastructure not owned by this project.
- Real company infrastructure.
- GitHub accounts, cloud accounts, registries, or services not explicitly part of this private lab.
- Personal devices, home networks, employer networks, or third-party networks.
- Social engineering attacks.
- Physical security testing.
- Phishing, credential harvesting, or impersonation.
- Denial-of-service attacks against GitHub, container registries, cloud providers, or any external service.
- Attempts to access secrets, tokens, or private data outside the lab environment.
- Any testing that violates laws, terms of service, or authorization boundaries.

---

## 4. Important Lab Disclaimer

This repository contains intentionally vulnerable code and intentionally insecure configurations for learning and demonstration.

Examples include:

- SQL injection in the vulnerable Flask route.
- Command injection in the vulnerable Flask route.
- Unsafe template rendering.
- Vulnerable dependency versions for SCA testing.
- Privileged pod simulation.
- RBAC privilege escalation simulation.
- GitOps drift simulation.
- Runtime detection simulation.

These are included to demonstrate secure testing, evidence collection, remediation strategy, and security engineering workflows.

Do not expose the vulnerable application to the public internet.

Do not run the attack simulation manifests in production clusters.

Do not reuse vulnerable code patterns in real applications.

---

## 5. Reporting a Security Issue

If you identify a security issue in this project that is not already documented as an intentional lab finding, report it responsibly.

Preferred reporting method:

1. Open a **private GitHub Security Advisory**, if enabled for the repository.
2. If private advisories are unavailable, contact the maintainer privately.
3. Do not disclose the issue publicly until it has been reviewed.

### Report Title Format

Use the following format:

```text
[Security] <Short finding title> - <Affected component>
```

Example:

```text
[Security] Insecure workflow token permission - .github/workflows/security-gates.yml
```

### Required Report Details

A useful report should include:

| Field | Required Detail |
|---|---|
| Finding Title | Clear and concise vulnerability title |
| Affected Component | File, path, workflow, container, manifest, or service |
| Vulnerability Type | SAST, SCA, container, Kubernetes, RBAC, secret, CI/CD, supply chain, runtime |
| Impact | What could happen if exploited |
| Reproduction Steps | Safe steps that work inside the private lab only |
| Evidence | Logs, screenshots, commands, scanner output, or proof of concept |
| Severity Suggestion | Critical, High, Medium, Low, or Informational |
| Recommended Fix | Secure code, configuration, workflow, or policy remediation |
| Retest Method | How the fix can be validated |
| Disclosure Status | Private, internal, draft, or ready for documentation |

---

## 6. Prohibited Testing Activities

The following activities are not allowed:

- Testing against any system outside the private lab.
- Exfiltrating real secrets, credentials, or tokens.
- Publishing private keys, tokens, passwords, or environment variables.
- Running destructive payloads.
- Running denial-of-service tests.
- Attempting persistence on host machines.
- Uploading malware, ransomware, miners, or destructive scripts.
- Abusing GitHub Actions minutes, runners, or external services.
- Attacking GitHub Container Registry, GitHub APIs, or third-party registries.
- Attempting to bypass authentication on systems not owned by the lab.
- Accessing or modifying data that is not part of the lab.

---

## 7. Known Intentional Vulnerabilities

The following issues are intentionally included for controlled demonstration and should not be reported as new vulnerabilities unless the report identifies a new variant, missing remediation, or incorrect documentation.

| ID | Finding | Component | Intentional Purpose | Status |
|---|---|---|---|---|
| LAB-APP-001 | SQL Injection | `/user?id=` route | Demonstrate injection testing and remediation | Documented |
| LAB-APP-002 | Command Injection | `/ping?host=` route | Demonstrate unsafe shell execution | Documented |
| LAB-APP-003 | Unsafe Template Rendering | `/hello?name=` route | Demonstrate template injection risk | Documented |
| LAB-SCA-001 | Vulnerable Dependency | `requirements.txt` | Demonstrate pip-audit and dependency remediation | Documented |
| LAB-K8S-001 | Privileged Pod Pattern | `redteam/runtime/` | Demonstrate runtime detection and Pod Security remediation | Documented |
| LAB-RBAC-001 | Cluster-Admin Binding | `redteam/rbac/` | Demonstrate RBAC escalation and least privilege remediation | Documented |
| LAB-GITOPS-001 | Manual Drift | Kubernetes deployment | Demonstrate ArgoCD self-healing | Documented |
| LAB-SUPPLY-001 | Unsigned Image Baseline | Container image | Demonstrate Cosign signing and SBOM workflow | Remediated |

---

## 8. Severity Classification

Severity is evaluated using project impact, exploitability, affected trust boundary, remediation complexity, and whether the issue affects only the lab or could affect real-world deployments if copied.

### Critical

A finding is Critical when it may allow:

- Full cluster compromise.
- Full host compromise.
- Unauthorized administrative control.
- Secret extraction with broad impact.
- Remote command execution in a realistic deployment path.
- Supply chain compromise that allows malicious artifact deployment.

Examples:

- Privileged Kubernetes workload with hostPath access.
- Cluster-admin access granted to an application ServiceAccount.
- Hardcoded production token with write access.
- Critical container vulnerability with available exploit path.

### High

A finding is High when it may allow:

- Unauthorized data access.
- Command execution inside a container.
- Privilege escalation within an application or namespace.
- Deployment of unsafe workloads.
- Bypass of major security controls.

Examples:

- Command injection.
- SQL injection exposing sensitive records.
- Insecure CI/CD permissions.
- Missing admission control for sensitive workloads.

### Medium

A finding is Medium when it may allow:

- Security control weakness.
- Missing defense-in-depth.
- Incomplete logging or monitoring.
- Misconfiguration requiring chaining with another issue.
- Unpatched dependency without direct exploit evidence.

Examples:

- Missing security headers.
- Weak image hardening.
- Missing SBOM metadata.
- Missing NetworkPolicy for low-risk namespace.

### Low

A finding is Low when it has limited direct impact but should be improved.

Examples:

- Missing documentation.
- Minor hardening gaps.
- Informational scanner findings.
- Non-sensitive metadata exposure.

### Informational

A finding is Informational when it improves awareness but does not create a direct vulnerability.

Examples:

- Recommended version pinning.
- Suggested documentation improvement.
- Recommended dashboard enhancement.

---

## 9. Security Gates

This project uses CI/CD security gates to prevent insecure changes from being accepted without review.

The following conditions should fail a security gate:

| Gate | Fail Condition |
|---|---|
| Dependency Security | Critical dependency vulnerability found |
| Container Security | Critical container vulnerability found |
| Secret Scanning | Secret found in repository or workflow artifacts |
| Dockerfile Security | Critical Dockerfile misconfiguration found |
| Kubernetes Security | Critical Kubernetes manifest misconfiguration found |
| SAST | High or Critical unsafe code pattern detected after remediation baseline |
| Supply Chain | Missing expected SBOM, signature, or provenance artifact in protected release flow |

Security gate workflows should be placed under:

```text
.github/workflows/security-gates.yml
.github/workflows/scorecard.yml
```

---

## 10. OpenSSF Scorecard Usage

OpenSSF Scorecard is used to evaluate repository security posture.

The Scorecard workflow helps identify weaknesses related to:

- Branch protection.
- Dependency update practices.
- Token permissions.
- Dangerous workflow patterns.
- Signed releases.
- Maintained dependencies.
- Security policy presence.
- Vulnerability reporting process.

Scorecard results should be reviewed as security posture guidance. A low score does not automatically mean the repository is vulnerable, but it identifies improvement areas that should be tracked.

---

## 11. Dependency Security Policy

Dependency security is handled through:

- `pip-audit`
- Trivy filesystem scanning
- SBOM generation with Syft
- Dependency review through CI/CD
- Manual remediation and retest documentation

Dependency management expectations:

- Avoid outdated packages unless intentionally used for lab demonstration.
- Document vulnerable dependencies clearly.
- Use version pinning for reproducible builds.
- Update vulnerable packages when remediation is required.
- Maintain a vulnerability exception record when risk is accepted.
- Do not ignore dependency vulnerabilities without justification.

Dependency evidence should be stored in:

```text
security/reports/
security/sbom/
docs/
```

---

## 12. Secret Handling Policy

Secrets must never be committed to the repository.

Examples of prohibited secrets:

- GitHub personal access tokens.
- Cosign private keys.
- Cloud credentials.
- SSH private keys.
- API keys.
- Database passwords.
- Service account tokens.
- `.env` files containing credentials.

The following files must remain ignored:

```text
security/cosign/cosign.key
cosign.key
*.pem
*.key
.env
```

Before committing, run:

```bash
git status --ignored | grep cosign.key || true
grep -R "ghp_" -n . --exclude-dir=.git || true
grep -R "GITHUB_TOKEN" -n . --exclude-dir=.git || true
grep -R "COSIGN_PASSWORD" -n . --exclude-dir=.git || true
```

If a secret is committed accidentally:

1. Revoke the secret immediately.
2. Remove it from the repository.
3. Rotate any dependent credentials.
4. Document the incident.
5. Add a prevention rule or scanner update.

---

## 13. Container Security Policy

Container images should follow hardened build and runtime practices.

Expected controls:

- Multi-stage Docker build.
- Non-root runtime user.
- Fixed UID/GID.
- Minimal base image.
- No package cache in final image.
- No secrets in image layers.
- Healthcheck configured.
- Gunicorn used instead of Flask debug server.
- Image scanned with Trivy.
- Image signed with Cosign.
- SBOM generated with Syft.
- Provenance generated for build traceability.

Unsafe container practices:

- Running as root.
- Using `latest` tag for production-style deployments.
- Including build tools in runtime image unnecessarily.
- Copying secrets into the image.
- Enabling Flask debug mode in production-style runtime.
- Running with privileged mode.
- Mounting host root filesystem.

---

## 14. Kubernetes Security Policy

Kubernetes manifests should implement defense-in-depth.

Expected controls:

| Control | Expected Setting |
|---|---|
| Namespace Isolation | Dedicated namespace |
| Pod Security | Restricted labels where appropriate |
| ServiceAccount | Dedicated ServiceAccount |
| Token Mounting | `automountServiceAccountToken: false` unless required |
| User Context | `runAsNonRoot: true` |
| UID/GID | Fixed non-root UID/GID |
| Privilege Escalation | `allowPrivilegeEscalation: false` |
| Capabilities | Drop `ALL` |
| Root Filesystem | `readOnlyRootFilesystem: true` where feasible |
| Seccomp | `RuntimeDefault` |
| Resource Limits | CPU and memory requests/limits |
| Probes | Liveness and readiness probes |
| NetworkPolicy | Default-deny and explicit allow rules |
| Admission Control | Gatekeeper policies |
| Runtime Detection | Falco monitoring |

High-risk Kubernetes patterns:

- Privileged containers.
- HostPath mounts.
- Host network usage.
- Host PID usage.
- Host IPC usage.
- Cluster-admin application ServiceAccounts.
- ServiceAccount token auto-mounting by default.
- Missing NetworkPolicies.
- Missing resource limits.
- Public NodePort exposure without justification.

---

## 15. RBAC Security Policy

RBAC must follow least privilege.

Requirements:

- Avoid `cluster-admin` except for controlled administrative tasks.
- Use namespace-scoped Roles where possible.
- Use ClusterRoles only when cluster-wide access is necessary.
- Bind permissions only to required ServiceAccounts.
- Review ClusterRoleBindings regularly.
- Validate permissions using `kubectl auth can-i`.
- Document exceptions.

Expected validation commands:

```bash
kubectl auth can-i get secrets \
  --as=system:serviceaccount:devsecops:demo-app-sa \
  -n devsecops

kubectl auth can-i list nodes \
  --as=system:serviceaccount:devsecops:demo-app-sa
```

Expected secure result:

```text
no
no
```

---

## 16. Network Security Policy

Network security should follow a default-deny model where supported.

Expected controls:

- Default deny ingress.
- Default deny egress where feasible.
- Explicit allow for required service-to-service traffic.
- Explicit DNS egress.
- NetworkPolicy enforced by a compatible CNI such as Calico.
- Validation using allowed and blocked test pods.

Evidence should show:

- Trusted pod allowed.
- Untrusted pod blocked.
- DNS egress allowed if required.
- NetworkPolicies listed in the namespace.

---

## 17. Supply Chain Security Policy

Supply chain security is handled through:

- GitHub Actions security gates.
- OpenSSF Scorecard.
- Cosign image signing.
- Syft SBOM generation.
- SPDX and CycloneDX SBOM formats.
- Provenance records.
- SLSA-style evidence.
- Vulnerability exceptions.
- VEX notes.

Expected artifacts:

```text
security/cosign/cosign.pub
security/sbom/sbom-spdx.json
security/sbom/sbom-cyclonedx.json
security/provenance/slsa-provenance.json
security/reports/cosign-image-verify.txt
security/reports/sbom-attestation-verify.txt
security/reports/slsa-provenance-verify.txt
```

Private keys must never be committed.

---

## 18. Runtime Detection Policy

Runtime security is monitored using Falco, Falcosidekick, Prometheus, and Grafana.

Detection coverage includes:

- Sensitive file access.
- Shell activity inside containers.
- Privileged container behavior.
- Host filesystem access patterns.
- Suspicious Kubernetes runtime activity.
- Falco event drops.
- Falco output queue drops.

Expected evidence:

- Falco alert logs.
- Falcosidekick UI or metrics.
- Prometheus query result.
- Grafana dashboard screenshot.
- Prometheus alert rule configuration.
- Incident response runbook.

Runtime detections should include:

| Field | Required |
|---|---|
| Detection Name | Yes |
| MITRE ATT&CK Mapping | Yes |
| Log Source | Yes |
| Trigger Condition | Yes |
| False Positives | Yes |
| Severity | Yes |
| Triage Steps | Yes |
| Response Steps | Yes |
| Evidence Screenshot | Yes |

---

## 19. Evidence and Retest Policy

Every security finding should include evidence and retest proof.

Evidence should be stored in:

```text
evidence/screenshots/
security/reports/
docs/evidence/
```

Each finding should include:

- Initial vulnerable state.
- Scanner or manual test evidence.
- Impact explanation.
- Remediation applied.
- Retest command.
- Retest output.
- Final status.

Retest result statuses:

| Status | Meaning |
|---|---|
| Remediated | Fix applied and validated |
| Accepted Risk | Risk documented and approved for lab purpose |
| False Positive | Finding reviewed and not applicable |
| Open | Fix pending |
| Not Applicable | Control not relevant to project scope |

---

## 20. Vulnerability Exceptions

Exceptions are allowed only when documented.

Each exception must include:

- Vulnerability ID.
- Affected package or component.
- Reason for exception.
- Compensating controls.
- Expiry or review date.
- Owner.
- Risk level.
- Retest plan.

Example acceptable exception reasons:

- Vulnerability is intentionally included for lab demonstration.
- Vulnerable package is not reachable at runtime.
- Exploit requires unavailable configuration.
- Fix would break a controlled test scenario.
- Compensating controls reduce practical risk.

Exceptions should be documented in:

```text
exceptions/vulnerability_exceptions.md
exceptions/vex_notes.md
```

---

## 21. Secure Development Requirements

Development changes should follow these requirements:

- Validate untrusted input.
- Use parameterized SQL queries.
- Avoid `shell=True`.
- Avoid unsafe template rendering.
- Add security headers.
- Add unit tests for security behavior.
- Keep dependencies updated.
- Use least privilege.
- Avoid secrets in code.
- Keep CI/CD permissions minimal.
- Document evidence for security-relevant changes.

Recommended secure code examples:

- SQL query parameterization.
- Subprocess argument list instead of shell string.
- Template rendering with context variables.
- Security headers using Flask `after_request`.
- Strict dependency pinning.
- Test cases for dangerous payloads.

---

## 22. Responsible Disclosure Timeline

For a private portfolio lab, response timelines are best-effort. For professional structure, the following targets are used:

| Severity | Initial Review Target | Remediation Target |
|---|---:|---:|
| Critical | 2 business days | 7 business days |
| High | 3 business days | 14 business days |
| Medium | 5 business days | 30 business days |
| Low | 10 business days | 60 business days |
| Informational | Best effort | Best effort |

Intentional lab vulnerabilities may remain open if they are clearly documented and isolated.

---

## 23. Safe Local Testing Instructions

Run the application locally only inside a private lab:

```bash
docker compose up --build demo-app
```

Run security scans:

```bash
docker compose --profile security run --rm bandit-sast
docker compose --profile security run --rm pip-audit-sca
docker compose --profile security run --rm trivy-fs-scan
docker compose --profile security run --rm trivy-image-scan
```

Run tests:

```bash
python -m pytest tests/ -v
```

Run SBOM generation:

```bash
docker compose --profile sbom run --rm syft-sbom
```

Do not expose the vulnerable app publicly.

---

## 24. Branch Protection Recommendations

For enterprise-grade GitHub posture, enable:

- Protected `main` branch.
- Pull request required before merge.
- Required approvals.
- Required status checks.
- Required security gates.
- Dismiss stale approvals on new commits.
- Restrict force pushes.
- Restrict branch deletion.
- Require conversation resolution.
- Review GitHub Actions workflow permission settings.

Recommended required checks:

```text
Security Gates
OpenSSF Scorecard
CI Pipeline
```

---

## 25. Contact

For security-related discussion, use the repository security advisory process or contact the maintainer privately.

Do not disclose sensitive findings publicly before review.

---

## 26. Final Notes

This project is a controlled, private DevSecOps security lab. It is designed to demonstrate professional security engineering practices across application security, CI/CD, containers, Kubernetes, GitOps, supply chain security, runtime detection, monitoring, compliance mapping, evidence collection, and retesting.

The vulnerable components are intentionally included for learning and should remain isolated from public environments.
