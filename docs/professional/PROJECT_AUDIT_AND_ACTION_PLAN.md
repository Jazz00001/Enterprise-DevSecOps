# MNC-Ready Project Audit and Action Plan

**Project:** Enterprise DevSecOps Red Team Lab  
**Owner:** Jagriti Banerjee  
**Audit date:** 2026-06-18  
**Assessment lens:** MNC hiring manager, DevSecOps engineer, AppSec analyst, cloud security analyst, and security consultant portfolio review.

## Executive verdict

This is already a strong portfolio project because it demonstrates more than scanner execution. It includes application vulnerabilities, CI/CD gates, Kubernetes hardening, GitOps, supply-chain evidence, runtime detection, screenshots, and formal reports. The project currently looks like a **7.6/10** security portfolio. With the fixes below, it can become a **9/10+ interview-grade project**.

The strongest parts are:

| Area | Current strength |
|---|---|
| Evidence volume | 159 screenshots, security reports, SBOM files, Trivy/Bandit/pip-audit outputs, Falco evidence |
| Security breadth | AppSec, SAST, SCA, container, Kubernetes, RBAC, network policy, GitOps, SBOM, signing, runtime detection |
| Hiring relevance | Maps well to DevSecOps, Cloud Security, AppSec, VAPT, Security Consultant, and PTaaS-style roles |
| Practical realism | Shows vulnerable state, control implementation, retest proof, and reporting lifecycle |

## Critical issues to fix before sharing publicly

| Priority | Issue | Why it matters to MNC recruiters | Fix |
|---|---|---|---|
| P0 | Many PDF reports contain another author's name, **Jagriti Banerjee** | This is the biggest credibility risk. Recruiters may think the project is copied. | Regenerate all public reports with your name or remove them from the public repo until regenerated. Use source Markdown going forward. |
| P0 | Tests were failing because the app lacked baseline security headers | Failing tests make the repo look unfinished unless clearly explained. | `src/app/app.py` now has a baseline `after_request` header hook. Re-run pytest and commit the passing result. |
| P0 | Vulnerable and remediated code are mixed conceptually | In a lab, intentional vulnerabilities are fine, but the repo must prove you know both exploitation and remediation. | Keep vulnerable demo routes, but add hardened reference implementation and remediation tests. |
| P1 | Many documents are PDF-only | PDFs look nice but are hard to diff, review, and maintain. | Keep PDFs as final exports, but store source reports as Markdown in `docs/professional/`. |
| P1 | Dependency versions are intentionally vulnerable | This is okay for evidence, but the repo also needs a secure dependency track. | Add `requirements-secure.txt` and a documented vulnerable-vs-secure mode. |
| P1 | Evidence lacks hash manifest and chain-of-custody | Professional reports need evidence integrity. | Add generated `evidence_manifest.csv` with SHA256, file size, and path. |
| P2 | CI uses some moving third-party actions | Enterprise pipelines prefer pinned versions or commit SHAs. | Document pinning as a hardening backlog item and pin critical actions before final portfolio push. |
| P2 | Argo CD uses `project: default` | GitOps governance looks more mature with AppProject restrictions. | Add restricted AppProject manifest and document sync boundaries. |

## Scorecard

| Category | Score | Reason |
|---|---:|---|
| AppSec depth | 8/10 | SQLi, command injection, template injection, Bandit, tests, finding cards |
| DevSecOps automation | 8/10 | CI gates, artifact upload, Trivy, pip-audit, Bandit, Scorecard |
| Kubernetes security | 8/10 | securityContext, RBAC, network policy, Pod Security labels, kube-bench evidence |
| Supply chain | 7.5/10 | SBOM, Cosign, SLSA-style provenance; needs stronger verification flow and keyless signing story |
| Evidence quality | 7/10 | Many screenshots/reports; needs hash manifest and author cleanup |
| Professional presentation | 6.5/10 | Very detailed README, but too long and old author names are serious |
| Interview readiness | 8/10 | Strong story if you can explain every stage clearly |

## Recommended final repo structure

```text
Enterprise-DevSecOps/
├── README.md
├── SECURITY.md
├── LICENSE
├── Dockerfile
├── docker-compose.yml
├── src/app/
│   ├── app.py                    # intentionally vulnerable lab app
│   ├── app_hardened.py            # secure reference implementation
│   ├── init_db.py
│   ├── requirements.txt           # vulnerable lab dependencies
│   └── requirements-secure.txt    # hardened dependency baseline
├── tests/
├── k8s/base/
├── gitops/argocd/
├── security/
│   ├── reports/
│   ├── sbom/
│   ├── provenance/
│   └── policies/
├── monitoring/
├── screenshots/
├── docs/
│   ├── professional/              # source Markdown docs for recruiters
│   └── findings/                  # PDF exports only after author cleanup
├── scripts/
│   ├── generate_evidence_manifest.py
│   ├── validate_professional_readiness.py
│   └── name_audit.py
└── .github/
    ├── workflows/
    ├── ISSUE_TEMPLATE/
    ├── pull_request_template.md
    ├── dependabot.yml
    └── CODEOWNERS
```

## 30-60-90 minute action plan before pushing to GitHub

### First 30 minutes: credibility cleanup

1. Remove or regenerate every PDF containing the wrong author name.
2. Run `python scripts/name_audit.py` and save the output as proof.
3. Commit the passing test result after adding baseline security headers.
4. Add `docs/professional/MNC_PROJECT_AUDIT_AND_ACTION_PLAN.md` as your public roadmap.

### Next 60 minutes: technical maturity

1. Add `src/app/app_hardened.py` and `tests/test_hardened_app.py`.
2. Add `requirements-secure.txt`.
3. Add Dependabot, CODEOWNERS, PR template, security finding issue template.
4. Generate `docs/professional/evidence_manifest.csv`.

### Next 90 minutes: recruiter polish

1. Rewrite the top of README to be shorter and sharper.
2. Add a **5-minute demo path** section: clone, run, exploit, scan, harden, retest.
3. Add a **What I learned** section.
4. Add a **Limitations** section so the project sounds honest.
5. Add a **Video PoC storyboard** with timestamped sections.

## What to say in interviews

Use this story:

> I built a private enterprise-style DevSecOps lab that follows a consulting lifecycle: build, break, detect, harden, retest, and report. The project starts with a vulnerable Flask banking-style API, validates issues like SQL injection, command injection, insecure rendering, vulnerable dependencies, insecure container/Kubernetes configuration, and then adds CI/CD gates, SBOM, signing evidence, GitOps deployment, Kubernetes hardening, policy-as-code, runtime Falco detection, and PTaaS-style reports. I also maintained evidence screenshots, scan outputs, retest proof, and compliance mappings so the project can be reviewed like a real client assessment.

## Final quality target

Your final public GitHub should prove five things:

1. You can find vulnerabilities manually and with tools.
2. You can explain business risk, not just technical output.
3. You can remediate and retest.
4. You understand enterprise controls: CI/CD, SBOM, policy-as-code, Kubernetes hardening, evidence, and compliance.
5. You can communicate like a professional security consultant.
