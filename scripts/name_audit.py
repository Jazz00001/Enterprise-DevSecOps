#!/usr/bin/env python3
"""Find old author/name references before public release.

For PDFs, the script uses pdftotext when available because PDF text may not be
visible through normal text reading. Output is capped so CI logs stay readable.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDLES = ["Jagriti", "Banerjee"]
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "docs/professional"}
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".zip"}
MAX_RESULTS = 200


def is_skipped(path: Path) -> bool:
    rel = str(path.relative_to(ROOT))
    return any(part in SKIP_DIRS for part in path.parts) or path.suffix.lower() in BINARY_SUFFIXES or rel == "scripts/name_audit.py"


def read_text_for_audit(path: Path) -> str:
    if path.suffix.lower() == ".pdf" and shutil.which("pdftotext"):
        try:
            result = subprocess.run(["pdftotext", str(path), "-"], text=True, capture_output=True, timeout=15)
            return result.stdout + result.stderr
        except Exception:
            return path.read_text(errors="ignore")
    return path.read_text(errors="ignore")


def main() -> int:
    findings = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or is_skipped(path):
            continue
        try:
            text = read_text_for_audit(path)
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if any(n in line for n in NEEDLES):
                findings.append((path.relative_to(ROOT), i, line.strip()[:180]))
                if len(findings) >= MAX_RESULTS:
                    break
        if len(findings) >= MAX_RESULTS:
            break
    if findings:
        print(f"Old author/name references found (showing up to {MAX_RESULTS}):")
        for rel, line_no, line in findings:
            print(f"{rel}:{line_no}: {line}")
        return 1
    print("No old author/name references found in public source/report files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
