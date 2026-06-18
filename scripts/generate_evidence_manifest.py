#!/usr/bin/env python3
"""Generate SHA256 evidence manifest for screenshots, reports, SBOMs, and docs."""
from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "professional" / "evidence_manifest.csv"
INCLUDE_DIRS = ["screenshots", "security/reports", "security/sbom", "security/provenance", "reports", "docs/findings"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    rows = []
    generated_at = datetime.now(timezone.utc).isoformat()
    for dirname in INCLUDE_DIRS:
        base = ROOT / dirname
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file():
                rows.append({
                    "generated_at_utc": generated_at,
                    "relative_path": str(path.relative_to(ROOT)),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["generated_at_utc", "relative_path", "size_bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} evidence records to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
