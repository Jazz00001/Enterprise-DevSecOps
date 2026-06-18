# Security Exception Request Template

> Use this template when a vulnerability, misconfiguration, policy violation, dependency finding, container issue, Kubernetes risk, CI/CD weakness, or supply-chain finding cannot be remediated immediately and requires a time-bound, documented risk exception.

---

## 1. Exception Summary

| Field | Details |
|---|---|
| Exception Title | `<Short title of the exception>` |
| Exception ID | `EXC-YYYY-###` |
| Project | `Enterprise DevSecOps Security Lab` |
| Requested By | `<Name / role>` |
| Owner | `<Responsible owner>` |
| Reviewer | `<Security reviewer / maintainer>` |
| Approval Status | `Draft / Pending Review / Approved / Rejected / Expired / Closed` |
| Request Date | `<YYYY-MM-DD>` |
| Expiry Date | `<YYYY-MM-DD>` |
| Review Frequency | `Weekly / Monthly / Before release / Before merge` |
| Related Finding ID | `<Finding ID, CVE, advisory ID, scanner ID, or report reference>` |
| Related Evidence | `<Screenshot, report path, workflow run, scanner output, or issue link>` |

---

## 2. Exception Type

Select all that apply.

- [ ] Application security finding
- [ ] Dependency vulnerability
- [ ] Container image vulnerability
- [ ] Dockerfile misconfiguration
- [ ] Kubernetes manifest misconfiguration
- [ ] RBAC exception
- [ ] NetworkPolicy exception
- [ ] Pod Security exception
- [ ] CI/CD workflow exception
- [ ] Secret scanning exception
- [ ] Supply-chain exception
- [ ] SBOM / provenance exception
- [ ] Runtime detection exception
- [ ] Compliance mapping exception
- [ ] False positive
- [ ] Accepted lab risk
- [ ] Other: `<Describe>`

---

## 3. Affected Asset

| Field | Details |
|---|---|
| Repository Path | `<Example: src/app/app.py, Dockerfile, k8s/base/deployment.yaml>` |
| Component | `<Application / Docker / Kubernetes / CI/CD / Supply Chain / Monitoring>` |
| Environment | `Private lab / Local VM / Kind cluster / GitHub Actions / GHCR` |
| Image Name | `<Example: ghcr.io/<user>/enterprise-devsecops-lab:latest>` |
| Image Digest | `<sha256 digest if applicable>` |
| Kubernetes Namespace | `<Namespace if applicable>` |
| Workload / Service | `<Deployment, ServiceAccount, Service, NetworkPolicy, etc.>` |
| Workflow Name | `<GitHub Actions workflow if applicable>` |
| Scanner / Tool | `<Bandit / pip-audit / Trivy / kube-bench / Scorecard / Falco / Gatekeeper>` |

---

## 4. Finding Description

### 4.1 Finding Title

`<Write a clear title for the risk being accepted temporarily.>`

### 4.2 Finding Details

Describe the issue in plain language.

Example:

```text
The dependency scan identified a vulnerable package version in requirements.txt. The issue is currently retained because the vulnerable package is intentionally included in the lab to demonstrate SCA detection, report generation, remediation planning, and retest proof.
```

### 4.3 Technical Evidence

Add evidence references.

| Evidence Type | Location |
|---|---|
| Screenshot | `evidence/screenshots/<filename>.png` |
| Scanner Report | `security/reports/<report-name>.json` |
| CI/CD Workflow | `.github/workflows/<workflow>.yml` |
| SBOM | `security/sbom/<file>.json` |
| Kubernetes Manifest | `k8s/base/<file>.yaml` |
| Documentation | `docs/<document>.md` |
| PDF Report | `docs/reports/<report>.pdf` |

---

## 5. Severity and Risk Rating

| Field | Value |
|---|---|
| Severity | `Critical / High / Medium / Low / Informational` |
| Likelihood | `High / Medium / Low` |
| Impact | `High / Medium / Low` |
| Exploitability | `High / Medium / Low` |
| Exposure | `Private lab only / Internal / Public / Unknown` |
| Data Sensitivity | `None / Test data / Sensitive / Secrets / Unknown` |
| Business Risk | `High / Medium / Low` |
| Technical Risk | `High / Medium / Low` |
| Residual Risk | `High / Medium / Low` |
| Risk Decision | `Accept / Mitigate Later / False Positive / Not Applicable / Transfer / Avoid` |

### 5.1 Risk Rating Rationale

Explain why this rating was chosen.

```text
This issue is rated Medium because the vulnerable component exists only inside a private lab and is not exposed to the public internet. However, the same pattern would be High or Critical in production because it could allow unauthorized access, command execution, privilege escalation, or supply-chain compromise.
```

---

## 6. Root Cause

Select all that apply.

- [ ] Intentional vulnerable lab scenario
- [ ] Insecure code pattern
- [ ] Outdated dependency
- [ ] Missing input validation
- [ ] Unsafe command execution
- [ ] Missing security header
- [ ] Insecure Dockerfile setting
- [ ] Missing container hardening
- [ ] Kubernetes default configuration
- [ ] Excessive RBAC permission
- [ ] Missing NetworkPolicy
- [ ] Missing Pod Security enforcement
- [ ] Missing admission-control policy
- [ ] Missing security gate
- [ ] Missing artifact signing
- [ ] Missing SBOM / provenance
- [ ] Scanner false positive
- [ ] Tool limitation
- [ ] Documentation gap
- [ ] Other: `<Describe>`

### Root Cause Explanation

```text
<Explain why the issue exists, how it was introduced, and whether it is intentional for lab demonstration or an actual gap requiring remediation.>
```

---

## 7. Justification for Exception

Explain why remediation is not being completed immediately.

Valid reasons may include:

- The vulnerable pattern is intentionally included for educational lab evidence.
- The finding is required to demonstrate detection and remediation workflow.
- The fix is planned but requires compatibility testing.
- The scanner finding is not exploitable in the current configuration.
- A compensating control reduces the practical risk.
- The vulnerable package is not reachable at runtime.
- The issue exists only in a controlled private VM environment.
- The issue has no public exposure.
- The issue is a false positive requiring documented review.
- The issue will be remediated in a future milestone.

### Exception Justification

```text
<Write the specific reason this exception is being requested. Avoid vague statements such as "will fix later" without a clear plan.>
```

---

## 8. Compensating Controls

Document the controls that reduce risk while the exception remains open.

| Control Area | Compensating Control | Evidence |
|---|---|---|
| Exposure Control | Application runs only inside private VM / local Kind cluster | `<Evidence path>` |
| CI/CD Control | Security gates detect and report the issue | `<Workflow/report>` |
| Runtime Control | Falco detects suspicious runtime activity | `<Falco evidence>` |
| Kubernetes Control | Pod Security / RBAC / NetworkPolicy reduce blast radius | `<Manifest/evidence>` |
| Supply Chain Control | Image signing, SBOM, provenance available | `<Cosign/Syft evidence>` |
| Documentation Control | Finding documented with remediation and retest plan | `<Report path>` |
| Monitoring Control | Prometheus/Grafana dashboards track detections | `<Dashboard evidence>` |

### Additional Compensating Controls

```text
<List any extra controls used to reduce likelihood or impact.>
```

---

## 9. Remediation Plan

| Step | Remediation Action | Owner | Target Date | Status |
|---|---|---|---|---|
| 1 | `<Example: Replace vulnerable SQL query with parameterized query>` | `<Owner>` | `<YYYY-MM-DD>` | `Open` |
| 2 | `<Example: Replace shell=True with safe subprocess argument list>` | `<Owner>` | `<YYYY-MM-DD>` | `Open` |
| 3 | `<Example: Upgrade vulnerable dependency>` | `<Owner>` | `<YYYY-MM-DD>` | `Open` |
| 4 | `<Example: Re-run security gates and attach results>` | `<Owner>` | `<YYYY-MM-DD>` | `Open` |
| 5 | `<Example: Update retest proof documentation>` | `<Owner>` | `<YYYY-MM-DD>` | `Open` |

### Secure Remediation Requirements

The final remediation should include, where applicable:

- Secure code change.
- Dependency upgrade.
- Dockerfile hardening.
- Kubernetes manifest hardening.
- CI/CD security gate validation.
- Retest proof.
- Evidence screenshot.
- Updated documentation.
- Updated risk register entry.
- Closure approval.

---

## 10. Retest Plan

### 10.1 Retest Commands

Add the exact commands that will be used to validate closure.

```bash
# Run application tests
python -m pytest tests/ -v

# Run SAST
bandit -r src/app -f json -o security/reports/bandit-report.json

# Run dependency audit
pip-audit -r src/app/requirements.txt -f json -o security/reports/pip-audit-report.json

# Run container scan
trivy image devsecops-vuln-app:lab

# Run Kubernetes manifest scan
trivy config k8s/base

# Validate RBAC
kubectl auth can-i get secrets --as=system:serviceaccount:devsecops:demo-app-sa -n devsecops

# Validate NetworkPolicy
kubectl -n devsecops exec blocked-curl -- curl --max-time 5 http://demo-app-svc:5000/health

# Validate Pod Security
kubectl apply -f redteam/runtime/privileged-hostpath-pod.yaml

# Validate Cosign signature
cosign verify --key security/cosign/cosign.pub <IMAGE>

# Validate SBOM attestation
cosign verify-attestation --key security/cosign/cosign.pub --type spdxjson <IMAGE>
```

### 10.2 Retest Success Criteria

| Control | Success Criteria |
|---|---|
| Application Security | Exploit payload no longer succeeds |
| SAST | No High/Critical insecure code pattern remains, unless documented |
| Dependency Security | Critical dependency findings are remediated or excepted |
| Container Security | Critical image vulnerabilities are remediated or excepted |
| Dockerfile | Critical misconfigurations are resolved |
| Kubernetes | Critical manifest misconfigurations are resolved |
| RBAC | ServiceAccount cannot access secrets or cluster-admin actions |
| NetworkPolicy | Untrusted pod traffic is blocked |
| Pod Security | Privileged pod is rejected |
| Supply Chain | Signature, SBOM, and provenance validation succeeds |
| Runtime Detection | Falco/Prometheus evidence remains available |
| Documentation | Findings and retest proof are updated |

---

## 11. Expiry and Review

Security exceptions must be time-bound.

| Field | Value |
|---|---|
| Exception Expiry Date | `<YYYY-MM-DD>` |
| Maximum Exception Duration | `30 / 60 / 90 days` |
| Review Cadence | `Weekly / Monthly / Release-based` |
| Auto-Expire? | `Yes / No` |
| Renewal Allowed? | `Yes / No` |
| Renewal Requires Approval? | `Yes` |

### Expiry Rule

If the expiry date is reached and the exception has not been renewed or remediated, the exception should be marked as:

```text
Expired - Requires immediate review
```

---

## 12. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Requester | `<Name>` | `Submitted` | `<YYYY-MM-DD>` |
| Security Reviewer | `<Name>` | `Approved / Rejected / Needs Changes` | `<YYYY-MM-DD>` |
| Technical Owner | `<Name>` | `Approved / Rejected / Needs Changes` | `<YYYY-MM-DD>` |
| Final Approver | `<Name>` | `Approved / Rejected` | `<YYYY-MM-DD>` |

### Approval Notes

```text
<Add reviewer comments, approval conditions, or required follow-up actions.>
```

---

## 13. Closure

Complete this section only after the issue is fixed, expired, or formally accepted.

| Field | Value |
|---|---|
| Closure Status | `Remediated / Accepted Risk / False Positive / Not Applicable / Expired` |
| Closure Date | `<YYYY-MM-DD>` |
| Closed By | `<Name>` |
| Retest Evidence | `<Path to retest screenshot/report>` |
| Pull Request | `<PR link>` |
| Commit Hash | `<Commit SHA>` |
| Final Risk | `None / Low / Medium / High` |

### Closure Summary

```text
<Explain what changed, what evidence proves closure, and whether any residual risk remains.>
```

---

## 14. Example Completed Exception

### Exception Summary

| Field | Details |
|---|---|
| Exception Title | Intentional vulnerable Flask dependency retained for SCA demonstration |
| Exception ID | `EXC-2026-001` |
| Project | `Enterprise DevSecOps Security Lab` |
| Owner | `Jagriti Banerjee` |
| Approval Status | `Approved for lab demonstration` |
| Related Finding ID | `LAB-SCA-001` |
| Expiry Date | `2026-12-31` |

### Finding Description

The dependency scan identifies a vulnerable package version in the Flask application requirements file. The vulnerable package is intentionally retained in the lab branch to demonstrate dependency scanning, pip-audit output, security gate behavior, remediation planning, vulnerability exception documentation, and retest proof.

### Risk Rating

| Field | Value |
|---|---|
| Severity | Medium |
| Likelihood | Low |
| Impact | Medium |
| Exposure | Private lab only |
| Risk Decision | Accepted lab risk |

### Justification

The dependency exists only in a controlled private lab environment. It is not deployed to production or exposed publicly. The finding is documented, detected by CI/CD security gates, included in reports, and tracked for remediation demonstration.

### Compensating Controls

- Private VM only.
- Not internet exposed.
- pip-audit detects the issue.
- Trivy detects vulnerable dependencies.
- SBOM documents the package inventory.
- Vulnerability exception is documented.
- Retest plan exists.

### Closure Condition

The exception can be closed once the dependency is upgraded, tests pass, pip-audit returns no unresolved critical findings, and the retest proof document is updated.

---

## 15. GitHub Labels

Recommended labels for GitHub issues:

```text
security-exception
risk-accepted
needs-review
needs-retest
dependency-security
container-security
kubernetes-security
ci-cd-security
supply-chain-security
false-positive
lab-intentional
expires-soon
```

---

## 16. GitHub Issue Title Examples

```text
[Security Exception] Intentional vulnerable dependency retained for SCA lab evidence
[Security Exception] Privileged pod manifest retained for runtime detection demo
[Security Exception] Critical image vulnerability accepted pending base image upgrade
[Security Exception] Scanner false positive in Kubernetes manifest
[Security Exception] Missing security header accepted pending Flask middleware update
```

---

## 17. Repository Placement

Recommended placement:

```text
docs/templates/SECURITY_EXCEPTION_TEMPLATE.md
```

Optional GitHub issue template placement:

```text
.github/ISSUE_TEMPLATE/security_exception_request.md
```

---

## 18. Notes

This exception template is designed for a private Enterprise DevSecOps lab. It supports professional documentation of risk acceptance, false positives, accepted lab vulnerabilities, remediation deferrals, and compensating controls.

It should not be used to hide unresolved production risk. In real enterprise environments, every exception should have an owner, expiry date, review cadence, compensating controls, and formal approval.
