# CI/CD Workflow Separation

## Purpose

This repository separates report-only workflows from blocking security gate workflows.

## Report-Only Workflow

`ci.yml` generates reports and uploads artifacts. It may continue after scanner findings because its purpose is evidence collection.

## Blocking Gate Workflows

The following workflows are intended to block unsafe pull requests:

- `security-gates.yml`
- `gitleaks.yml`
- `trivy-container.yml`
- `zap-baseline.yml`
- `codeql.yml`

## Rule

Blocking gate workflows must not use fake gates such as:

- `|| true`
- `exit-code: "0"` for the actual blocking scan step
- unconditional success after serious findings

## Why This Matters

A professional DevSecOps project should not claim that security gates block unsafe builds unless the workflows actually fail when serious findings exist.
