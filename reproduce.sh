#!/usr/bin/env bash
# reproduce.sh — one-command reproducibility test for the GLP-1 triangulation repo.
#
#   ./reproduce.sh
#
# Regenerates the machine-generated manifest from the committed data files, then
# verifies that (1) backing-file hashes are unchanged and (2) the README /
# synthesis prose is consistent with the manifest. Exits non-zero on any drift.
#
# This does NOT re-run the openFDA / LLM analyses (those depend on a live openFDA
# snapshot and API access — see FROZEN_PROTOCOL.md for the pinned snapshot date and
# how to re-run them). It reproduces the *provenance chain*: data files -> manifest
# -> headline numbers, which is what a reviewer needs to trust the counts.
set -euo pipefail
cd "$(dirname "$0")"

echo "== [1/3] regenerating analysis_manifest.json from data files =="
python build_manifest.py

echo
echo "== [2/3] verifying backing-file hashes =="
python tests/verify_input_hashes.py

echo
echo "== [3/3] checking README / synthesis consistency with manifest =="
python tests/check_readme_against_manifest.py

echo
echo "REPRODUCIBILITY CHECK PASSED"
