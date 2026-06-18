# PDF Regeneration Plan

## Why this matters

The current repository includes PDF reports that contain an old author name. This is a credibility blocker for public GitHub and job applications.

## Safe approach

Do not try to binary-edit the PDFs. PDF text replacement can corrupt layout, leave hidden metadata unchanged, or create inconsistent evidence.

Use this process instead:

1. Keep source reports in Markdown under `docs/professional/`.
2. Regenerate PDFs from the source Markdown with the correct owner name.
3. Run `python scripts/name_audit.py`.
4. Only publish PDFs when the audit returns no old author references.
5. Keep old PDFs in a private archive if you still need them for reference.

## Minimum public PDF set

For recruiters, you do not need 40+ PDFs. Publish only these final PDFs after regeneration:

| PDF | Purpose |
|---|---|
| Executive Project Summary | 5-minute recruiter review |
| Findings and Remediation Report | Shows AppSec/VAPT ability |
| Control Validation Matrix | Shows enterprise control thinking |
| Compliance Crosswalk | Shows audit/GRC communication |
| Evidence Index | Shows proof and traceability |
| Retest Report | Shows professional closure |
| Architecture/Threat Model | Shows design and risk thinking |

## Keep source Markdown beside every PDF

Example:

```text
docs/professional/executive_project_summary.md
docs/professional/executive_project_summary.pdf
```
