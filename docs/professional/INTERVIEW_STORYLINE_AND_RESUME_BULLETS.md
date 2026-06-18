# Interview Storyline and Resume Bullets

## 60-second explanation

I built an enterprise-style DevSecOps security assessment lab that follows the full lifecycle: build, break, detect, harden, retest, and report. The lab starts with a vulnerable Flask API and then moves through CI/CD security gates, dependency scanning, container image scanning, Kubernetes hardening, GitOps with Argo CD, policy-as-code with Gatekeeper/Kyverno concepts, SBOM generation, Cosign signing evidence, SLSA-style provenance, runtime detection using Falco, and PTaaS-style findings and retest reports.

## 5-minute demo flow

1. Show architecture diagram and assessment scope.
2. Run the vulnerable API locally.
3. Demonstrate SQL injection / command injection / unsafe rendering in the private lab.
4. Show Bandit, pip-audit, Trivy, and CI security gate output.
5. Show hardened Kubernetes deployment: non-root, no privilege escalation, read-only filesystem, resource limits.
6. Show NetworkPolicy and RBAC validation.
7. Show Argo CD sync and drift self-heal evidence.
8. Show SBOM, Cosign verification, and provenance evidence.
9. Show Falco runtime alert evidence.
10. Close with retest report and what you would improve next.

## Resume bullets

- Built an enterprise DevSecOps security lab covering AppSec, CI/CD security, Kubernetes hardening, GitOps, supply-chain security, runtime detection, evidence collection, and PTaaS-style reporting.
- Implemented security gates using Bandit, pip-audit, Trivy filesystem/config/image scans, SARIF upload, artifact retention, and threshold-based CI enforcement.
- Demonstrated exploitation and remediation of SQL injection, command injection, unsafe template rendering, vulnerable dependencies, insecure container images, and Kubernetes privilege misconfigurations.
- Hardened Kubernetes workloads using non-root execution, dropped capabilities, read-only root filesystem, resource limits, Pod Security labels, NetworkPolicies, and least-privilege RBAC.
- Generated SBOM and signing/provenance evidence using Syft/Cosign/SLSA-style artifacts and mapped controls to NIST SSDF, OWASP ASVS, CIS Kubernetes, SLSA, SOC 2, and ISO-style frameworks.
- Produced professional evidence packages including screenshots, scanner outputs, risk register, compliance matrix, retest proof, and executive summaries.

## Interview weakness to avoid

Do not say: “I ran tools and copied reports.”  
Say: “I used scanners as evidence sources, manually validated the finding, explained root cause and business impact, implemented remediation, and retested the control.”
