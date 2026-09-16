#!/usr/bin/env python3
"""Deterministic verification for the clean Personal AI core package."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
HASHES = ROOT / "integrity" / "foundation_hashes.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    failures = []
    expected = json.loads(HASHES.read_text())
    print("=== Personal AI Core Verification ===")
    for rel, wanted in expected.items():
        got = sha256(ROOT / rel)
        ok = got == wanted
        print(f"FOUNDATION {'PASS' if ok else 'FAIL'}: {rel}")
        if not ok:
            failures.append(rel)

    compile_targets = list((ROOT / "personal_ai").rglob("*.py"))
    for path in compile_targets:
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except Exception as exc:
            failures.append(str(path))
            print(f"SYNTAX FAIL: {path}: {exc}")
    print(f"Python source syntax: {'PASS' if not failures else 'CHECK'}")

    if failures:
        print("VERIFICATION: FAIL")
        return 1

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
        text=True,
    )
    if result.returncode != 0:
        print("PYTEST: FAIL")
        return result.returncode

    print("VERIFICATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
