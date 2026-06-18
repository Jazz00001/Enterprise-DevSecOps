# Security Exception Process

## Purpose

A security exception is used only when a finding cannot be remediated immediately and must be temporarily accepted with compensating controls.

## Exception record

| Field | Required value |
|---|---|
| Exception ID | EXC-YYYY-### |
| Finding ID | Linked finding |
| Owner | Named person/team |
| Risk | What remains exposed |
| Business justification | Why remediation is delayed |
| Compensating controls | What reduces risk temporarily |
| Expiry date | Date exception must be reviewed |
| Approval | Security owner approval |

## Example

| Field | Value |
|---|---|
| Exception ID | EXC-2026-001 |
| Finding ID | DEP-001 outdated dependency |
| Risk | Vulnerable package remains in lab mode |
| Justification | Kept intentionally vulnerable for educational exploitation evidence |
| Compensating control | Hardened dependency baseline documented in `requirements-secure.txt` |
| Expiry date | 30 days after public portfolio release |
| Approval | Project owner |
