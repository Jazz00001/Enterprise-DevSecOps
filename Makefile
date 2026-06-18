# ==============================================================================
# Enterprise DevSecOps Security Lab - Professional Makefile
# Maintainer: Jagriti Banerjee
#
# Purpose:
#   This Makefile provides repeatable commands for local development, testing,
#   security scanning, Docker workflows, Kubernetes hardening validation,
#   GitOps operations, supply-chain evidence, runtime detection, and reporting.
#
# Usage:
#   make help
#   make setup
#   make test
#   make security-all
#   make docker-build
#   make k8s-apply
#
# Safety:
#   This project contains intentionally vulnerable lab components. Run only inside
#   your private VM / private Kind cluster. Do not expose the app publicly.
# ==============================================================================

SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

# ------------------------------------------------------------------------------
# Project Metadata
# ------------------------------------------------------------------------------

PROJECT_NAME             ?= enterprise-devsecops-lab
APP_NAME                 ?= demo-app
APP_MODULE               ?= app:app
PYTHON                   ?= python3
VENV_DIR                 ?= .venv
PIP                      ?= $(VENV_DIR)/bin/pip
PYTEST                   ?= $(VENV_DIR)/bin/pytest
BANDIT                   ?= $(VENV_DIR)/bin/bandit
PIP_AUDIT                ?= $(VENV_DIR)/bin/pip-audit

APP_DIR                  ?= src/app
TEST_DIR                 ?= tests
DOCS_DIR                 ?= docs
SECURITY_DIR             ?= security
REPORTS_DIR              ?= $(SECURITY_DIR)/reports
SBOM_DIR                 ?= $(SECURITY_DIR)/sbom
PROVENANCE_DIR           ?= $(SECURITY_DIR)/provenance
POLICIES_DIR             ?= $(SECURITY_DIR)/policies
EVIDENCE_DIR             ?= evidence/screenshots

REQUIREMENTS_FILE        ?= $(APP_DIR)/requirements.txt
DOCKERFILE               ?= Dockerfile
COMPOSE_FILE             ?= docker-compose.yml

# ------------------------------------------------------------------------------
# Container / Registry Settings
# ------------------------------------------------------------------------------

IMAGE_LOCAL              ?= devsecops-vuln-app:lab
IMAGE_NAME               ?= enterprise-devsecops-lab
IMAGE_TAG                ?= latest
GITHUB_USER              ?= YOUR_GITHUB_USERNAME
GITHUB_USER_LOWER        := $(shell echo "$(GITHUB_USER)" | tr '[:upper:]' '[:lower:]')
GHCR_IMAGE               ?= ghcr.io/$(GITHUB_USER_LOWER)/$(IMAGE_NAME):$(IMAGE_TAG)

COSIGN_PUBLIC_KEY        ?= $(SECURITY_DIR)/cosign/cosign.pub
COSIGN_PRIVATE_KEY       ?= $(SECURITY_DIR)/cosign/cosign.key

# ------------------------------------------------------------------------------
# Kubernetes Settings
# ------------------------------------------------------------------------------

KIND_CLUSTER             ?= devsecops-lab
KIND_CONFIG              ?= kind-cluster.yaml
K8S_NAMESPACE            ?= devsecops
K8S_BASE                 ?= k8s/base
K8S_APP_LABEL            ?= app=$(APP_NAME)
SERVICE_NAME             ?= demo-app-svc
SERVICE_PORT             ?= 5000
LOCAL_APP_PORT           ?= 8080

ARGOCD_NAMESPACE         ?= argocd
ARGOCD_APP               ?= demo-app
GATEKEEPER_NAMESPACE     ?= gatekeeper-system
FALCO_NAMESPACE          ?= falco
MONITORING_NAMESPACE     ?= monitoring

# ------------------------------------------------------------------------------
# Security Gate Thresholds
# ------------------------------------------------------------------------------

MAX_BANDIT_HIGH          ?= 0
MAX_BANDIT_MEDIUM        ?= 0
MAX_PIP_AUDIT_TOTAL      ?= 0
MAX_TRIVY_CRITICAL       ?= 0
MAX_TRIVY_HIGH           ?= 5

# ------------------------------------------------------------------------------
# Colors
# ------------------------------------------------------------------------------

GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
BLUE   := \033[0;34m
RESET  := \033[0m

# ------------------------------------------------------------------------------
# Help
# ------------------------------------------------------------------------------

.PHONY: help
help: ## Show all available Make targets
	@echo ""
	@echo -e "$(BLUE)Enterprise DevSecOps Security Lab - Make Targets$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z0-9_.-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;32m%-34s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Common usage:"
	@echo "  make setup"
	@echo "  make test"
	@echo "  make security-all"
	@echo "  make docker-build"
	@echo "  make k8s-apply"
	@echo "  make evidence-index"
	@echo ""

# ------------------------------------------------------------------------------
# Environment / Tooling
# ------------------------------------------------------------------------------

.PHONY: doctor
doctor: ## Check required local tools and project structure
	@echo -e "$(BLUE)[doctor] Checking tools and project structure...$(RESET)"
	@command -v $(PYTHON) >/dev/null || { echo "Missing python3"; exit 1; }
	@command -v docker >/dev/null || { echo "Missing docker"; exit 1; }
	@command -v git >/dev/null || { echo "Missing git"; exit 1; }
	@command -v curl >/dev/null || { echo "Missing curl"; exit 1; }
	@command -v jq >/dev/null || echo "Warning: jq not found"
	@command -v kubectl >/dev/null || echo "Warning: kubectl not found"
	@command -v helm >/dev/null || echo "Warning: helm not found"
	@command -v kind >/dev/null || echo "Warning: kind not found"
	@test -d "$(APP_DIR)" || { echo "Missing $(APP_DIR)"; exit 1; }
	@test -f "$(REQUIREMENTS_FILE)" || { echo "Missing $(REQUIREMENTS_FILE)"; exit 1; }
	@test -f "$(DOCKERFILE)" || { echo "Missing $(DOCKERFILE)"; exit 1; }
	@echo -e "$(GREEN)[doctor] Basic checks completed.$(RESET)"

.PHONY: prepare-dirs
prepare-dirs: ## Create project report, evidence, SBOM, provenance, and policy folders
	@echo -e "$(BLUE)[prepare-dirs] Creating project directories...$(RESET)"
	@mkdir -p "$(REPORTS_DIR)" "$(SBOM_DIR)" "$(PROVENANCE_DIR)" "$(POLICIES_DIR)" "$(EVIDENCE_DIR)"
	@mkdir -p docs/evidence docs/architecture docs/findings docs/templates redteam/runtime redteam/rbac monitoring/dashboards monitoring/rules monitoring/values
	@echo -e "$(GREEN)[prepare-dirs] Directories ready.$(RESET)"

.PHONY: venv
venv: ## Create Python virtual environment
	@echo -e "$(BLUE)[venv] Creating virtual environment...$(RESET)"
	@test -d "$(VENV_DIR)" || $(PYTHON) -m venv "$(VENV_DIR)"
	@$(PIP) install --upgrade pip setuptools wheel
	@echo -e "$(GREEN)[venv] Virtual environment ready.$(RESET)"

.PHONY: install
install: venv prepare-dirs ## Install application and security testing dependencies
	@echo -e "$(BLUE)[install] Installing Python dependencies...$(RESET)"
	@$(PIP) install -r "$(REQUIREMENTS_FILE)"
	@$(PIP) install pytest pytest-cov requests bandit pip-audit
	@echo -e "$(GREEN)[install] Dependencies installed.$(RESET)"

.PHONY: setup
setup: doctor install ## Full local setup for private VM development
	@echo -e "$(GREEN)[setup] Project setup completed.$(RESET)"

# ------------------------------------------------------------------------------
# Application Development / Testing
# ------------------------------------------------------------------------------

.PHONY: run-local
run-local: ## Run Flask app locally from src/app
	@echo -e "$(BLUE)[run-local] Starting local Flask app on 127.0.0.1:5000...$(RESET)"
	@cd "$(APP_DIR)" && ../../$(VENV_DIR)/bin/gunicorn --bind 127.0.0.1:5000 "$(APP_MODULE)"

.PHONY: test
test: install ## Run all pytest tests
	@echo -e "$(BLUE)[test] Running pytest...$(RESET)"
	@$(PYTEST) "$(TEST_DIR)" -v

.PHONY: test-cov
test-cov: install ## Run pytest with coverage output
	@echo -e "$(BLUE)[test-cov] Running pytest with coverage...$(RESET)"
	@$(PYTEST) "$(TEST_DIR)" -v --cov="$(APP_DIR)" --cov-report=term-missing --cov-report=xml:$(REPORTS_DIR)/coverage.xml

.PHONY: test-health
test-health: install ## Run health endpoint tests only
	@$(PYTEST) "$(TEST_DIR)/test_health.py" -v

.PHONY: test-routes
test-routes: install ## Run route behavior tests only
	@$(PYTEST) "$(TEST_DIR)/test_routes.py" -v

.PHONY: test-security-headers
test-security-headers: install ## Run security header tests only
	@$(PYTEST) "$(TEST_DIR)/test_security_headers.py" -v

# ------------------------------------------------------------------------------
# Static Analysis / Dependency Security
# ------------------------------------------------------------------------------

.PHONY: bandit
bandit: install prepare-dirs ## Run Bandit SAST scan and save reports
	@echo -e "$(BLUE)[bandit] Running Bandit SAST...$(RESET)"
	@$(BANDIT) -r "$(APP_DIR)" -f json -o "$(REPORTS_DIR)/bandit-report.json" || true
	@$(BANDIT) -r "$(APP_DIR)" -f txt -o "$(REPORTS_DIR)/bandit-report.txt" || true
	@echo -e "$(GREEN)[bandit] Reports saved in $(REPORTS_DIR).$(RESET)"

.PHONY: bandit-gate
bandit-gate: bandit ## Fail if Bandit High/Medium findings exceed thresholds
	@echo -e "$(BLUE)[bandit-gate] Evaluating Bandit thresholds...$(RESET)"
	@$(PYTHON) - <<'PY'
import json, sys
from pathlib import Path
report = Path("$(REPORTS_DIR)/bandit-report.json")
data = json.loads(report.read_text()) if report.exists() else {"results": []}
counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
for issue in data.get("results", []):
    sev = issue.get("issue_severity", "LOW").upper()
    counts[sev] = counts.get(sev, 0) + 1
print(f"Bandit counts: {counts}")
if counts.get("HIGH", 0) > int("$(MAX_BANDIT_HIGH)") or counts.get("MEDIUM", 0) > int("$(MAX_BANDIT_MEDIUM)"):
    print("Bandit security gate failed.")
    sys.exit(1)
print("Bandit security gate passed.")
PY

.PHONY: pip-audit
pip-audit: install prepare-dirs ## Run pip-audit dependency scan and save reports
	@echo -e "$(BLUE)[pip-audit] Running dependency audit...$(RESET)"
	@$(PIP_AUDIT) -r "$(REQUIREMENTS_FILE)" -f json -o "$(REPORTS_DIR)/pip-audit-report.json" || true
	@$(PIP_AUDIT) -r "$(REQUIREMENTS_FILE)" > "$(REPORTS_DIR)/pip-audit-report.txt" || true
	@echo -e "$(GREEN)[pip-audit] Reports saved in $(REPORTS_DIR).$(RESET)"

.PHONY: pip-audit-gate
pip-audit-gate: pip-audit ## Fail if pip-audit vulnerability count exceeds threshold
	@echo -e "$(BLUE)[pip-audit-gate] Evaluating dependency thresholds...$(RESET)"
	@$(PYTHON) - <<'PY'
import json, sys
from pathlib import Path
report = Path("$(REPORTS_DIR)/pip-audit-report.json")
data = json.loads(report.read_text()) if report.exists() else {"dependencies": []}
total = sum(len(dep.get("vulns", [])) for dep in data.get("dependencies", []))
print(f"pip-audit total vulnerabilities: {total}")
if total > int("$(MAX_PIP_AUDIT_TOTAL)"):
    print("pip-audit security gate failed.")
    sys.exit(1)
print("pip-audit security gate passed.")
PY

# ------------------------------------------------------------------------------
# Docker / Compose
# ------------------------------------------------------------------------------

.PHONY: docker-build
docker-build: prepare-dirs ## Build hardened local Docker image
	@echo -e "$(BLUE)[docker-build] Building $(IMAGE_LOCAL)...$(RESET)"
	@docker build -t "$(IMAGE_LOCAL)" .
	@echo -e "$(GREEN)[docker-build] Image built: $(IMAGE_LOCAL)$(RESET)"

.PHONY: docker-run
docker-run: docker-build ## Run application container locally on 127.0.0.1:8080
	@echo -e "$(BLUE)[docker-run] Running container on localhost:$(LOCAL_APP_PORT)...$(RESET)"
	@docker run --rm -p 127.0.0.1:$(LOCAL_APP_PORT):5000 --name "$(PROJECT_NAME)-app" "$(IMAGE_LOCAL)"

.PHONY: docker-id
docker-id: docker-build ## Verify container runs as non-root user
	@echo -e "$(BLUE)[docker-id] Checking runtime UID/GID...$(RESET)"
	@docker run --rm --entrypoint id "$(IMAGE_LOCAL)"

.PHONY: docker-health
docker-health: ## Test local container/app health endpoint
	@echo -e "$(BLUE)[docker-health] Testing health endpoint...$(RESET)"
	@curl -fsS "http://127.0.0.1:$(LOCAL_APP_PORT)/health" | jq . || curl -fsS "http://127.0.0.1:$(LOCAL_APP_PORT)/health"

.PHONY: compose-up
compose-up: ## Start app using docker compose
	@docker compose -f "$(COMPOSE_FILE)" up --build demo-app

.PHONY: compose-down
compose-down: ## Stop compose stack and remove containers
	@docker compose -f "$(COMPOSE_FILE)" down --remove-orphans

.PHONY: compose-security
compose-security: ## Run compose-based security scanners
	@docker compose -f "$(COMPOSE_FILE)" --profile security run --rm bandit-sast
	@docker compose -f "$(COMPOSE_FILE)" --profile security run --rm pip-audit-sca
	@docker compose -f "$(COMPOSE_FILE)" --profile security run --rm trivy-fs-scan
	@docker compose -f "$(COMPOSE_FILE)" --profile security run --rm trivy-image-scan

# ------------------------------------------------------------------------------
# Trivy Security Scanning
# ------------------------------------------------------------------------------

.PHONY: trivy-fs
trivy-fs: prepare-dirs ## Run Trivy filesystem scan for vulnerabilities, secrets, and misconfigurations
	@echo -e "$(BLUE)[trivy-fs] Running Trivy filesystem scan...$(RESET)"
	@trivy fs --scanners vuln,secret,misconfig --severity CRITICAL,HIGH,MEDIUM --format table . | tee "$(REPORTS_DIR)/trivy-fs-report.txt"
	@trivy fs --scanners vuln,secret,misconfig --severity CRITICAL,HIGH,MEDIUM --format json -o "$(REPORTS_DIR)/trivy-fs-report.json" . || true

.PHONY: trivy-config
trivy-config: prepare-dirs ## Run Trivy Kubernetes/IaC config scan
	@echo -e "$(BLUE)[trivy-config] Running Trivy config scan for $(K8S_BASE)...$(RESET)"
	@trivy config --severity CRITICAL,HIGH,MEDIUM --format table "$(K8S_BASE)" | tee "$(REPORTS_DIR)/trivy-config-report.txt"
	@trivy config --severity CRITICAL,HIGH,MEDIUM --format json -o "$(REPORTS_DIR)/trivy-config-report.json" "$(K8S_BASE)" || true

.PHONY: trivy-image
trivy-image: docker-build prepare-dirs ## Run Trivy image vulnerability scan
	@echo -e "$(BLUE)[trivy-image] Running Trivy image scan for $(IMAGE_LOCAL)...$(RESET)"
	@trivy image --severity CRITICAL,HIGH,MEDIUM --ignore-unfixed --format table "$(IMAGE_LOCAL)" | tee "$(REPORTS_DIR)/trivy-image-report.txt"
	@trivy image --severity CRITICAL,HIGH,MEDIUM --ignore-unfixed --format json -o "$(REPORTS_DIR)/trivy-image-report.json" "$(IMAGE_LOCAL)" || true

.PHONY: trivy-gates
trivy-gates: trivy-fs trivy-config trivy-image ## Run all Trivy scans
	@echo -e "$(GREEN)[trivy-gates] Trivy scans completed.$(RESET)"

# ------------------------------------------------------------------------------
# SBOM / Cosign / Provenance
# ------------------------------------------------------------------------------

.PHONY: syft-sbom
syft-sbom: docker-build prepare-dirs ## Generate Syft SBOM in SPDX and CycloneDX formats
	@echo -e "$(BLUE)[syft-sbom] Generating SBOMs...$(RESET)"
	@syft "$(IMAGE_LOCAL)" -o spdx-json="$(SBOM_DIR)/sbom-spdx.json"
	@syft "$(IMAGE_LOCAL)" -o cyclonedx-json="$(SBOM_DIR)/sbom-cyclonedx.json"
	@syft "$(IMAGE_LOCAL)" -o table | tee "$(REPORTS_DIR)/sbom-table-report.txt"
	@echo -e "$(GREEN)[syft-sbom] SBOMs saved in $(SBOM_DIR).$(RESET)"

.PHONY: sbom-count
sbom-count: syft-sbom ## Print SBOM package count
	@echo -e "$(BLUE)[sbom-count] SPDX package count:$(RESET)"
	@jq '.packages | length' "$(SBOM_DIR)/sbom-spdx.json"

.PHONY: cosign-generate-key
cosign-generate-key: prepare-dirs ## Generate Cosign key pair; private key must not be committed
	@mkdir -p "$(SECURITY_DIR)/cosign"
	@cd "$(SECURITY_DIR)/cosign" && cosign generate-key-pair
	@echo -e "$(YELLOW)Reminder: Never commit $(COSIGN_PRIVATE_KEY).$(RESET)"

.PHONY: cosign-sign
cosign-sign: ## Sign GHCR image with Cosign private key
	@echo -e "$(BLUE)[cosign-sign] Signing $(GHCR_IMAGE)...$(RESET)"
	@COSIGN_YES=true cosign sign --key "$(COSIGN_PRIVATE_KEY)" "$(GHCR_IMAGE)"

.PHONY: cosign-verify
cosign-verify: prepare-dirs ## Verify GHCR image signature using Cosign public key
	@echo -e "$(BLUE)[cosign-verify] Verifying $(GHCR_IMAGE)...$(RESET)"
	@cosign verify --key "$(COSIGN_PUBLIC_KEY)" "$(GHCR_IMAGE)" | tee "$(REPORTS_DIR)/cosign-image-verify.txt"

.PHONY: image-digest
image-digest: ## Print image digest for GHCR image
	@echo -e "$(BLUE)[image-digest] Inspecting image digest...$(RESET)"
	@docker buildx imagetools inspect "$(GHCR_IMAGE)" --format '{{json .Manifest.Digest}}'

.PHONY: provenance
provenance: prepare-dirs ## Generate local SLSA-style provenance evidence
	@echo -e "$(BLUE)[provenance] Creating local provenance predicate...$(RESET)"
	@GIT_COMMIT=$$(git rev-parse HEAD); \
	STARTED_ON=$$(date -u +"%Y-%m-%dT%H:%M:%SZ"); \
	FINISHED_ON=$$(date -u +"%Y-%m-%dT%H:%M:%SZ"); \
	cat > "$(PROVENANCE_DIR)/slsa-provenance.json" <<EOF; \
{ \
  "buildDefinition": { \
    "buildType": "https://example.com/private-vm/docker-build", \
    "externalParameters": { \
      "repository": "$$(git config --get remote.origin.url)", \
      "ref": "$$(git branch --show-current)", \
      "image": "$(GHCR_IMAGE)" \
    }, \
    "resolvedDependencies": [ \
      { \
        "uri": "$$(git config --get remote.origin.url)", \
        "digest": { "gitCommit": "$$GIT_COMMIT" } \
      } \
    ] \
  }, \
  "runDetails": { \
    "builder": { "id": "private-ubuntu-endpoint-vm" }, \
    "metadata": { \
      "invocationId": "local-lab-$$GIT_COMMIT", \
      "startedOn": "$$STARTED_ON", \
      "finishedOn": "$$FINISHED_ON" \
    } \
  } \
} \
EOF
	@jq . "$(PROVENANCE_DIR)/slsa-provenance.json"

# ------------------------------------------------------------------------------
# Kubernetes / Kind
# ------------------------------------------------------------------------------

.PHONY: kind-create
kind-create: ## Create Kind cluster using configured Kind config
	@echo -e "$(BLUE)[kind-create] Creating Kind cluster $(KIND_CLUSTER)...$(RESET)"
	@kind create cluster --config "$(KIND_CONFIG)"

.PHONY: kind-delete
kind-delete: ## Delete Kind cluster
	@echo -e "$(RED)[kind-delete] Deleting Kind cluster $(KIND_CLUSTER)...$(RESET)"
	@kind delete cluster --name "$(KIND_CLUSTER)"

.PHONY: kind-load-image
kind-load-image: docker-build ## Load local Docker image into Kind
	@echo -e "$(BLUE)[kind-load-image] Loading image into Kind...$(RESET)"
	@kind load docker-image "$(IMAGE_LOCAL)" --name "$(KIND_CLUSTER)"

.PHONY: k8s-dry-run
k8s-dry-run: ## Server-side dry-run Kubernetes manifests
	@echo -e "$(BLUE)[k8s-dry-run] Validating Kubernetes manifests...$(RESET)"
	@kubectl apply -k "$(K8S_BASE)" --dry-run=server

.PHONY: k8s-apply
k8s-apply: kind-load-image ## Apply Kubernetes manifests using Kustomize
	@echo -e "$(BLUE)[k8s-apply] Applying Kubernetes manifests...$(RESET)"
	@kubectl apply -k "$(K8S_BASE)"
	@kubectl wait --for=condition=Ready pod -l "$(K8S_APP_LABEL)" -n "$(K8S_NAMESPACE)" --timeout=180s

.PHONY: k8s-status
k8s-status: ## Show Kubernetes app status
	@echo -e "$(BLUE)[k8s-status] Kubernetes resources in $(K8S_NAMESPACE)...$(RESET)"
	@kubectl get all -n "$(K8S_NAMESPACE)"
	@kubectl get networkpolicy -n "$(K8S_NAMESPACE)" || true
	@kubectl get serviceaccount,role,rolebinding -n "$(K8S_NAMESPACE)" || true

.PHONY: k8s-logs
k8s-logs: ## Show app logs from Kubernetes
	@kubectl logs -n "$(K8S_NAMESPACE)" -l "$(K8S_APP_LABEL)" --tail=100

.PHONY: k8s-port-forward
k8s-port-forward: ## Port-forward Kubernetes service to localhost
	@echo -e "$(BLUE)[k8s-port-forward] Forwarding localhost:$(LOCAL_APP_PORT) to $(SERVICE_NAME):$(SERVICE_PORT)...$(RESET)"
	@kubectl -n "$(K8S_NAMESPACE)" port-forward "svc/$(SERVICE_NAME)" "$(LOCAL_APP_PORT):$(SERVICE_PORT)"

.PHONY: k8s-health
k8s-health: ## Test Kubernetes app health through localhost port-forward
	@curl -fsS "http://127.0.0.1:$(LOCAL_APP_PORT)/health" | jq . || curl -fsS "http://127.0.0.1:$(LOCAL_APP_PORT)/health"

.PHONY: k8s-security-context
k8s-security-context: ## Print pod/container securityContext evidence
	@echo -e "$(BLUE)[k8s-security-context] Pod security context:$(RESET)"
	@kubectl -n "$(K8S_NAMESPACE)" get pod -l "$(K8S_APP_LABEL)" -o jsonpath='{.items[0].spec.securityContext}{"\n"}'
	@echo -e "$(BLUE)[k8s-security-context] Container security context:$(RESET)"
	@kubectl -n "$(K8S_NAMESPACE)" get pod -l "$(K8S_APP_LABEL)" -o jsonpath='{.items[0].spec.containers[0].securityContext}{"\n"}'

.PHONY: k8s-readonly-test
k8s-readonly-test: ## Validate read-only root filesystem and writable /tmp
	@POD=$$(kubectl -n "$(K8S_NAMESPACE)" get pod -l "$(K8S_APP_LABEL)" -o jsonpath='{.items[0].metadata.name}'); \
	echo "Testing /app write should fail:"; \
	kubectl -n "$(K8S_NAMESPACE)" exec "$$POD" -- sh -c 'touch /app/test.txt' || true; \
	echo "Testing /tmp write should pass:"; \
	kubectl -n "$(K8S_NAMESPACE)" exec "$$POD" -- sh -c 'touch /tmp/test.txt && echo tmp-write-ok'

# ------------------------------------------------------------------------------
# RBAC / NetworkPolicy / Pod Security Validation
# ------------------------------------------------------------------------------

.PHONY: rbac-check
rbac-check: ## Validate app ServiceAccount least privilege
	@echo -e "$(BLUE)[rbac-check] Checking app ServiceAccount permissions...$(RESET)"
	@kubectl auth can-i list configmaps --as=system:serviceaccount:$(K8S_NAMESPACE):demo-app-sa -n "$(K8S_NAMESPACE)"
	@kubectl auth can-i get secrets --as=system:serviceaccount:$(K8S_NAMESPACE):demo-app-sa -n "$(K8S_NAMESPACE)"
	@kubectl auth can-i list nodes --as=system:serviceaccount:$(K8S_NAMESPACE):demo-app-sa

.PHONY: rbac-audit-cluster-admin
rbac-audit-cluster-admin: ## Audit ClusterRoleBindings using cluster-admin
	@kubectl get clusterrolebindings -o json | jq -r '.items[] | select(.roleRef.name=="cluster-admin") | [.metadata.name, ((.subjects // []) | map("\(.kind):\(.namespace // "-"):\(.name)") | join(","))] | @tsv'

.PHONY: networkpolicy-list
networkpolicy-list: ## List NetworkPolicy resources
	@kubectl get networkpolicy -n "$(K8S_NAMESPACE)" -o wide

.PHONY: pod-security-labels
pod-security-labels: ## Show namespace Pod Security labels
	@kubectl get ns "$(K8S_NAMESPACE)" --show-labels

.PHONY: gatekeeper-status
gatekeeper-status: ## Show OPA Gatekeeper status and constraints
	@kubectl get pods -n "$(GATEKEEPER_NAMESPACE)" || true
	@kubectl get constrainttemplates || true
	@kubectl get constraints || true

# ------------------------------------------------------------------------------
# ArgoCD GitOps
# ------------------------------------------------------------------------------

.PHONY: argocd-status
argocd-status: ## Show ArgoCD app status
	@kubectl get application "$(ARGOCD_APP)" -n "$(ARGOCD_NAMESPACE)" || true
	@kubectl describe application "$(ARGOCD_APP)" -n "$(ARGOCD_NAMESPACE)" || true

.PHONY: argocd-port-forward
argocd-port-forward: ## Port-forward ArgoCD UI to https://localhost:8080
	@kubectl port-forward svc/argocd-server -n "$(ARGOCD_NAMESPACE)" 8080:443

.PHONY: argocd-password
argocd-password: ## Print initial ArgoCD admin password
	@kubectl -n "$(ARGOCD_NAMESPACE)" get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

.PHONY: argocd-stop
argocd-stop: ## Stop ArgoCD workloads to save RAM
	@kubectl -n "$(ARGOCD_NAMESPACE)" scale deployment --all --replicas=0 || true
	@kubectl -n "$(ARGOCD_NAMESPACE)" scale statefulset --all --replicas=0 || true

.PHONY: argocd-start
argocd-start: ## Start ArgoCD workloads
	@kubectl -n "$(ARGOCD_NAMESPACE)" scale deployment --all --replicas=1 || true
	@kubectl -n "$(ARGOCD_NAMESPACE)" scale statefulset --all --replicas=1 || true

# ------------------------------------------------------------------------------
# Falco / Prometheus / Grafana
# ------------------------------------------------------------------------------

.PHONY: falco-status
falco-status: ## Show Falco pods and services
	@kubectl get pods -n "$(FALCO_NAMESPACE)" || true
	@kubectl get svc -n "$(FALCO_NAMESPACE)" || true

.PHONY: falco-logs
falco-logs: prepare-dirs ## Follow Falco logs and save local evidence
	@kubectl logs -n "$(FALCO_NAMESPACE)" -l app.kubernetes.io/name=falco -f | tee "$(REPORTS_DIR)/falco-live-alerts.txt"

.PHONY: prometheus-port-forward
prometheus-port-forward: ## Port-forward Prometheus to http://localhost:9090
	@kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n "$(MONITORING_NAMESPACE)"

.PHONY: grafana-port-forward
grafana-port-forward: ## Port-forward Grafana to http://localhost:3000
	@kubectl port-forward svc/monitoring-grafana 3000:80 -n "$(MONITORING_NAMESPACE)"

.PHONY: falcosidekick-port-forward
falcosidekick-port-forward: ## Port-forward Falcosidekick metrics to http://localhost:2801
	@kubectl -n "$(FALCO_NAMESPACE)" port-forward svc/falco-falcosidekick 2801:2801

.PHONY: falco-prometheus-query
falco-prometheus-query: prepare-dirs ## Query Prometheus for Falco detections
	@curl -sG "http://localhost:9090/api/v1/query" --data-urlencode 'query=sum(increase(falcosecurity_falco_rules_matches_total[10m]))' | tee "$(REPORTS_DIR)/falco-detection-query-result.json" | jq .

# ------------------------------------------------------------------------------
# kube-bench / CIS Kubernetes Benchmark
# ------------------------------------------------------------------------------

.PHONY: kube-bench
kube-bench: prepare-dirs ## Run kube-bench container and save CIS-style results
	@echo -e "$(BLUE)[kube-bench] Running kube-bench. Results may vary in Kind/local VM environments...$(RESET)"
	@docker run --rm --pid=host \
		-v /etc:/etc:ro \
		-v /var:/var:ro \
		-v "$(PWD)/$(REPORTS_DIR)":/reports \
		aquasec/kube-bench:latest \
		--json > "$(REPORTS_DIR)/kube-bench-results.json" || true
	@docker run --rm --pid=host \
		-v /etc:/etc:ro \
		-v /var:/var:ro \
		aquasec/kube-bench:latest | tee "$(REPORTS_DIR)/kube-bench-results.txt" || true
	@echo -e "$(GREEN)[kube-bench] Results saved in $(REPORTS_DIR).$(RESET)"

# ------------------------------------------------------------------------------
# Git / Documentation / Evidence
# ------------------------------------------------------------------------------

.PHONY: evidence-index
evidence-index: prepare-dirs ## Generate evidence index from screenshots and reports
	@echo -e "$(BLUE)[evidence-index] Generating docs/evidence/EVIDENCE_INDEX.md...$(RESET)"
	@mkdir -p docs/evidence
	@{ \
		echo "# Evidence Index"; \
		echo ""; \
		echo "This file lists collected screenshots and reports for the Enterprise DevSecOps Security Lab."; \
		echo ""; \
		echo "## Screenshots"; \
		echo ""; \
		if [ -d "$(EVIDENCE_DIR)" ]; then find "$(EVIDENCE_DIR)" -maxdepth 1 -type f | sort | sed 's#^#- #'; else echo "- No screenshot directory found."; fi; \
		echo ""; \
		echo "## Security Reports"; \
		echo ""; \
		if [ -d "$(REPORTS_DIR)" ]; then find "$(REPORTS_DIR)" -maxdepth 1 -type f | sort | sed 's#^#- #'; else echo "- No report directory found."; fi; \
	} > docs/evidence/EVIDENCE_INDEX.md
	@echo -e "$(GREEN)[evidence-index] Created docs/evidence/EVIDENCE_INDEX.md$(RESET)"

.PHONY: git-security-check
git-security-check: ## Check for common accidental secret patterns before commit
	@echo -e "$(BLUE)[git-security-check] Checking for accidental secrets...$(RESET)"
	@git status --ignored | grep cosign.key || true
	@grep -R "ghp_" -n . --exclude-dir=.git --exclude-dir=$(VENV_DIR) || true
	@grep -R "GITHUB_TOKEN" -n . --exclude-dir=.git --exclude-dir=$(VENV_DIR) || true
	@grep -R "COSIGN_PASSWORD" -n . --exclude-dir=.git --exclude-dir=$(VENV_DIR) || true
	@grep -R "PRIVATE KEY" -n . --exclude-dir=.git --exclude-dir=$(VENV_DIR) || true
	@echo -e "$(YELLOW)[git-security-check] Review output carefully before committing.$(RESET)"

.PHONY: repo-tree
repo-tree: ## Show professional repository tree
	@tree -a -I '.git|$(VENV_DIR)|__pycache__|.pytest_cache|node_modules' -L 4 || find . -maxdepth 4 -not -path './.git/*' | sort

# ------------------------------------------------------------------------------
# Full Workflows
# ------------------------------------------------------------------------------

.PHONY: security-all
security-all: bandit pip-audit trivy-gates syft-sbom ## Run all local security scans and SBOM generation
	@echo -e "$(GREEN)[security-all] Security scans and SBOM generation completed.$(RESET)"

.PHONY: quality-all
quality-all: test test-cov security-all ## Run tests, coverage, scans, and SBOM
	@echo -e "$(GREEN)[quality-all] Quality and security workflow completed.$(RESET)"

.PHONY: k8s-validate-all
k8s-validate-all: k8s-dry-run k8s-apply k8s-status k8s-security-context rbac-check networkpolicy-list pod-security-labels ## Apply and validate Kubernetes security controls
	@echo -e "$(GREEN)[k8s-validate-all] Kubernetes validation completed.$(RESET)"

.PHONY: full-lab-validation
full-lab-validation: quality-all docker-id k8s-validate-all evidence-index git-security-check ## Run broad local project validation
	@echo -e "$(GREEN)[full-lab-validation] Full lab validation completed.$(RESET)"

# ------------------------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------------------------

.PHONY: clean
clean: ## Remove local Python/test caches
	@echo -e "$(BLUE)[clean] Cleaning local caches...$(RESET)"
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -f .coverage coverage.xml
	@echo -e "$(GREEN)[clean] Local caches removed.$(RESET)"

.PHONY: clean-reports
clean-reports: ## Remove generated security reports only
	@echo -e "$(YELLOW)[clean-reports] Removing generated reports...$(RESET)"
	@rm -rf "$(REPORTS_DIR)"
	@mkdir -p "$(REPORTS_DIR)"
	@echo -e "$(GREEN)[clean-reports] Reports directory reset.$(RESET)"

.PHONY: clean-docker
clean-docker: ## Remove local lab Docker image
	@docker image rm "$(IMAGE_LOCAL)" || true

.PHONY: version
version: ## Print Makefile/project version information
	@echo "Project: $(PROJECT_NAME)"
	@echo "App: $(APP_NAME)"
	@echo "Local image: $(IMAGE_LOCAL)"
	@echo "GHCR image: $(GHCR_IMAGE)"
	@echo "Kind cluster: $(KIND_CLUSTER)"
	@echo "Kubernetes namespace: $(K8S_NAMESPACE)"
