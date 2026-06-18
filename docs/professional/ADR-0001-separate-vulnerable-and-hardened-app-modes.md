# ADR-0001: Separate Vulnerable and Hardened Application Modes

## Status

Accepted

## Context

The project needs to demonstrate real vulnerabilities for learning and evidence. At the same time, a professional portfolio must prove the owner understands secure remediation.

## Decision

Maintain two modes:

1. `src/app/app.py` - intentionally vulnerable private-lab app used for exploit evidence.
2. `src/app/app_hardened.py` - secure reference implementation used for remediation and retest proof.

## Consequences

- Recruiters can see exploitation and secure coding ability.
- Security tests can validate both vulnerable behavior and hardened behavior.
- The README must clearly state that vulnerable routes are private-lab only and are not production code.
