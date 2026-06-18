# Supply Chain Security Backlog

| Backlog ID | Item | Why it matters | Target evidence |
|---|---|---|---|
| SC-BL-001 | Pin GitHub Actions by commit SHA | Reduces action supply-chain tampering risk | Workflow diff with pinned SHA |
| SC-BL-002 | Use keyless signing demo | Better enterprise story than local private keys | Cosign keyless/Rekor evidence or documented limitation |
| SC-BL-003 | Verify image signature before deploy | Connects signing to deployment enforcement | Admission policy or verification job |
| SC-BL-004 | Attach SBOM to image digest | Ties SBOM to immutable artifact | SBOM attestation verification output |
| SC-BL-005 | Add dependency review on PR | Catches risky dependency changes | GitHub dependency-review workflow evidence |
| SC-BL-006 | Add release provenance | Shows source-to-artifact traceability | SLSA provenance artifact and verification output |
| SC-BL-007 | Add VEX for accepted vulnerabilities | Explains why some vulns are not exploitable/applicable | VEX document linked to Trivy result |
