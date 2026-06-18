# Compliance Crosswalk

This project is not claiming formal certification. It maps lab controls to common enterprise frameworks so reviewers can see the governance thinking behind the technical work.

## Source references

- NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- CIS Kubernetes Benchmark: https://www.cisecurity.org/benchmark/kubernetes
- SLSA: https://slsa.dev/
- SOC 2 trust services criteria are commonly used for security, availability, processing integrity, confidentiality, and privacy control programs.
- ISO/IEC 27001 is an information security management system standard. This repo maps evidence in an ISO-style way but does not claim certification.
- PCI DSS/HIPAA mappings are contextual examples only; this private lab does not process cardholder data or protected health information.

## Mapping table

| Project control | NIST SSDF | OWASP ASVS | CIS Kubernetes | SLSA | SOC 2 style | ISO 27001 style | PCI/HIPAA style evidence |
|---|---|---|---|---|---|---|---|
| Threat model and attack path | PW.1, PW.2 | V1 Architecture | N/A | Threat awareness | Risk assessment | Risk management | Security risk analysis |
| SAST with Bandit | PW.7, RV.1 | V5 Validation, V14 Config | N/A | Source review support | Change control | Secure development | Secure SDLC evidence |
| Dependency scanning | PW.4, RV.1 | V14.2 Dependency | N/A | Dependency integrity | Vulnerability management | Technical vulnerability management | Vulnerability management |
| Secret scanning | PS.2, PW.6 | V2/V6 secrets | N/A | Source integrity | Access/security controls | Secure configuration | Credential protection |
| Security headers | PW.5 | V14 HTTP security config | N/A | N/A | Security baseline | Secure configuration | Secure transmission support |
| SQL injection remediation | PW.5, RV.3 | V5 Input Validation | N/A | N/A | Application controls | Secure coding | Application security evidence |
| Command injection remediation | PW.5, RV.3 | V5/V14 | N/A | N/A | Application controls | Secure coding | Application security evidence |
| Docker non-root user | PW.8 | V14 Configuration | Container runtime hardening | N/A | Secure configuration | System hardening | Platform security |
| Trivy image scan | RV.1, RV.2 | V14 Dependency/config | Container image hygiene | Artifact verification support | Vulnerability management | Vulnerability management | Vulnerability management |
| Kubernetes restricted namespace | PO/PW hardening | N/A | Pod Security / workload hardening | N/A | Infrastructure security | Secure operations | Platform security |
| RBAC least privilege | PO.5 | V4 Access control concept | RBAC controls | N/A | Logical access | Access control | Access authorization |
| NetworkPolicy default deny | PO.5 | N/A | Network segmentation | N/A | Network security | Network controls | Segmentation |
| Gatekeeper/Kyverno policies | PW.8 | N/A | Admission control | Deployment policy | Change enforcement | Configuration management | Preventive control |
| SBOM generation | PS.3 | V14 Components | N/A | Package metadata | Vendor/component risk | Asset inventory | Software inventory |
| Cosign signature verification | PS.2, PS.3 | N/A | N/A | Build/artifact integrity | Change integrity | Cryptographic controls | Integrity verification |
| SLSA-style provenance | PS.3 | N/A | N/A | Provenance | Change traceability | Supplier/security evidence | Audit trail |
| Falco runtime detections | RV.1, RV.2 | Logging/monitoring | Runtime monitoring | N/A | Monitoring | Event logging | Security monitoring |
| Retest proof | RV.3 | Verification | Control validation | N/A | Corrective action | Continual improvement | Remediation evidence |

## Reviewer note

For public GitHub, phrase compliance like this:

> This lab maps security controls to NIST SSDF, OWASP ASVS, CIS Kubernetes Benchmark, SLSA, and SOC 2/ISO-style control families for educational portfolio purposes. It is not a certification or audit attestation.
