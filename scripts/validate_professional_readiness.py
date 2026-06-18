#!/usr/bin/env python3
"""Lightweight portfolio readiness checks for this repository."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ("README exists", ROOT / "README.md"),
    ("SECURITY.md exists", ROOT / "SECURITY.md"),
    ("Security gates workflow exists", ROOT / ".github/workflows/security-gates.yml"),
    ("Dependabot config exists", ROOT / ".github/dependabot.yml"),
    ("CODEOWNERS exists", ROOT / ".github/CODEOWNERS"),
    ("Hardened app exists", ROOT / "src/app/app_hardened.py"),
    ("Evidence manifest exists", ROOT / "docs/professional/evidence_manifest.csv"),
]


def main() -> int:
    failed = False
    print("Portfolio readiness checks")
    for name, path in CHECKS:
        ok = path.exists()
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {path.relative_to(ROOT)}")
        failed = failed or not ok

    try:
        result = subprocess.run(["python", "-m", "pytest", "-q"], cwd=ROOT, text=True, capture_output=True, timeout=120)
        print("[PASS] pytest" if result.returncode == 0 else "[FAIL] pytest")
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
            failed = True
    except Exception as exc:
        print(f"[WARN] pytest could not be executed: {exc}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
