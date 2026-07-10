.PHONY: reproduce manifest test clean

# One-command reproducibility test (data files -> manifest -> headline numbers).
reproduce:
	bash reproduce.sh

# Just regenerate the machine-generated manifest.
manifest:
	python build_manifest.py

# Run the consistency + hash tests without rebuilding.
test:
	python tests/verify_input_hashes.py
	python tests/check_readme_against_manifest.py
