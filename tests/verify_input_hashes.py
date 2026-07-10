#!/usr/bin/env python3
"""verify_input_hashes.py — confirm every backing data file still matches the
SHA256 recorded in analysis_manifest.json. Detects silent data drift.

Exit 0 = all hashes match (or file intentionally regenerated & manifest rebuilt);
exit 1 = a tracked file changed without the manifest being regenerated.
"""
import json, os, hashlib, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256(relpath):
    p = os.path.join(ROOT, relpath)
    if not os.path.exists(p):
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    man = json.load(open(os.path.join(ROOT, "analysis_manifest.json")))
    recorded = man.get("input_file_sha256", {})
    mismatches, missing = [], []
    for rel, want in recorded.items():
        got = sha256(rel)
        if got is None:
            missing.append(rel)
        elif got != want:
            mismatches.append((rel, want[:12], got[:12]))
    if missing:
        print("MISSING backing files (in manifest, not on disk):")
        for r in missing:
            print(f"  {r}")
    if mismatches:
        print("HASH MISMATCH (file changed since manifest build — rerun build_manifest.py):")
        for rel, w, g in mismatches:
            print(f"  {rel}: manifest {w}... != disk {g}...")
    if missing or mismatches:
        return 1
    print(f"OK: all {len(recorded)} backing-file hashes match analysis_manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
