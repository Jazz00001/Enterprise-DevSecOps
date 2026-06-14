# Enterprise DevSecOps Security Lab

## Overview

This project is a private DevSecOps security lab that demonstrates secure software delivery concepts using a deliberately vulnerable Flask application, Docker image hardening, SAST, dependency scanning, container scanning, and CI/CD security automation.

## Lab Environment

- Ubuntu private VM
- Docker Engine
- Python Flask application
- GitHub Actions CI/CD
- Bandit SAST
- pip-audit SCA
- Trivy filesystem and image scanning
- GitHub Container Registry

## Application Vulnerabilities

| Route | Vulnerability Type | Purpose |
|---|---|---|
| `/user?id=1` | SQL Injection | Demonstrate insecure query construction |
| `/ping?host=127.0.0.1` | Command Injection | Demonstrate unsafe shell execution |
| `/hello?name=test` | Unsafe Template Rendering | Demonstrate template injection risk |

## Docker Security Controls

- Multi-stage build
- Non-root user
- No pip cache
- Healthcheck
- Gunicorn runtime server

## CI/CD Security Pipeline

1. Bandit SAST scan
2. pip-audit dependency scan
3. Trivy filesystem scan
4. Docker image build
5. Trivy image vulnerability scan
6. SARIF upload to GitHub code scanning
7. Push to GitHub Container Registry

## Evidence

Screenshots and reports are stored in:

- `evidence/screenshots/`
- `security/reports/`

## Disclaimer

This project is for private lab and educational purposes only. The vulnerable application must not be exposed to the public internet.
