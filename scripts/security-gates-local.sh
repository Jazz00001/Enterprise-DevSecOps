#!/usr/bin/env bash
set -euo pipefail

mkdir -p security/reports

echo "[1/5] Bandit high severity gate"
bandit -r src/app --severity-level high --confidence-level medium -f json -o security/reports/bandit-local-gate.json

echo "[2/5] pip-audit secure requirements gate"
python3 -m pip_audit -r src/app/requirements-secure.txt > security/reports/pip-audit-local-gate.txt

echo "[3/5] Trivy config gate"
trivy config --severity HIGH,CRITICAL --exit-code 1 . > security/reports/trivy-config-local-gate.txt

echo "[4/5] Build hardened image"
docker build -f Dockerfile.hardened -t devsecops-app:hardened .

echo "[5/5] Trivy hardened image gate"
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 devsecops-app:hardened > security/reports/trivy-image-local-gate.txt

echo "All local security gates passed."
