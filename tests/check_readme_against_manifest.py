#!/usr/bin/env python3
"""check_readme_against_manifest.py — fail if a headline number in README.md or
TRIANGULATION_SYNTHESIS.md contradicts analysis_manifest.json.

This is the guard that keeps the prose honest: the manifest is machine-generated
from the data files, and every load-bearing count in the narrative must match it.
Run as part of `make reproduce` / the one-command reproducibility test.

Exit 0 = consistent; exit 1 = a contradiction (printed).
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


def main():
    mpath = os.path.join(ROOT, "analysis_manifest.json")
    if not os.path.exists(mpath):
        print("FAIL: analysis_manifest.json not found — run build_manifest.py first")
        return 1
    man = json.load(open(mpath))

    A = man["stream_A"]
    B = man["stream_B_faers"]
    D = man["stream_D"]

    checks = []

    # FAERS adjudication count: exactly 912, and NOT a stale "800"
    checks.append(("FAERS adjudicated total",
                   lambda t: str(B["adjudicated_cases_total"]) in t
                   and "800/912" not in t and "800 of 912" not in t,
                   ["README.md", "TRIANGULATION_SYNTHESIS.md"]))

    # Stream D reconciliation: the extracted N appears
    checks.append(("Stream D extracted study count",
                   lambda t: str(D["extracted_study_table"]) in t,
                   ["README.md"]))

    # RCT pooled k
    checks.append(("RCT pooled k (M-H)",
                   lambda t: str(A["pooling"]["rct_pooled_k_MH"]) in t,
                   ["README.md"]))

    # No stale file reference
    checks.append(("no stale stream_B_PENDING reference",
                   lambda t: "stream_B_PENDING" not in t,
                   ["README.md", "TRIANGULATION_SYNTHESIS.md"]))

    failures = []
    for label, fn, docs in checks:
        for doc in docs:
            if not os.path.exists(os.path.join(ROOT, doc)):
                continue
            text = load(doc)
            if not fn(text):
                failures.append(f"  [{doc}] {label}")

    if failures:
        print("MANIFEST-README CONSISTENCY FAILURES:")
        print("\n".join(failures))
        return 1
    print("OK: README/TRIANGULATION_SYNTHESIS consistent with analysis_manifest.json")
    print(f"  FAERS adjudicated = {B['adjudicated_cases_total']}")
    print(f"  Stream A RCT pooled k = {A['pooling']['rct_pooled_k_MH']}")
    print(f"  Stream D extracted = {D['extracted_study_table']} "
          f"({D['direction_reconciliation']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
