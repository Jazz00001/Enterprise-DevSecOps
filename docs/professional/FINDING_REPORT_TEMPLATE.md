# Security Finding Report Template

## Finding ID

`FINDING-AREA-###`

## Title

Concise vulnerability title.

## Severity

Critical / High / Medium / Low

## Affected component

Application route, source file, pipeline job, container image, Kubernetes manifest, cloud/IaC file, or runtime control.

## Executive summary

Explain the issue in business language.

## Technical description

Explain the vulnerability, root cause, affected code/configuration, and exploit path.

## Evidence

| Evidence ID | File path | Description |
|---|---|---|
| EVD-001 | screenshots/example.png | Proof of vulnerable behavior |
| EVD-002 | security/reports/example.json | Tool output |

## Reproduction steps

```bash
# Put safe private-lab reproduction steps here.
```

## Impact

Describe confidentiality, integrity, availability, privilege escalation, lateral movement, compliance, and operational impact.

## Remediation

Give exact code/configuration remediation.

## Retest proof

Describe how the fix was verified.

## Status

Open / In Remediation / Retest Passed / Risk Accepted
