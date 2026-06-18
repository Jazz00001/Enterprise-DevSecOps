# Kubernetes Hardening Backlog

| Backlog ID | Item | Current state | Target state | Priority |
|---|---|---|---|---|
| K8S-BL-001 | Replace `project: default` in Argo CD | Uses default project | Restricted AppProject with repo/destination allowlist | High |
| K8S-BL-002 | Add image digest pinning | Image tag used in local lab | Use immutable digest in production-like manifest | High |
| K8S-BL-003 | Add admission policy for non-root/read-only FS | Partially covered | Kyverno/Gatekeeper policy blocks non-compliant pod | High |
| K8S-BL-004 | Add PodDisruptionBudget | Missing | PDB for production-style resilience | Medium |
| K8S-BL-005 | Add ResourceQuota and LimitRange | Not visible in base | Namespace-level quotas and defaults | Medium |
| K8S-BL-006 | Add AppArmor profile note | Not present | Document runtime profile options | Low |
| K8S-BL-007 | Add external-secrets/sealed-secrets concept | Not present | No plaintext secrets in Git | High |
| K8S-BL-008 | Add audit logging evidence | Partial | kube-apiserver audit policy evidence or kind simulation | Medium |
