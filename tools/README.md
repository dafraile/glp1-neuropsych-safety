# tools/

Reusable analysis tooling that travels with this project.

## dual-reviewer-rob

Full-text risk-of-bias harness: two **independent, cross-model** reviewers
(Claude + OpenAI by default), per-domain disagreement detection, a judge tier
for flagged domains, and a full (study x domain x reviewer) audit trail with
verbatim quote verification. Frameworks: RoB2 (RCTs), ROBINS-I (observational).

This is the planned hardening step for the RoB/GRADE layer, which is provisional
(rules-based) in the current results snapshot. It is also published as a Claude
Science skill; this copy is the versioned source of record.

- `SKILL.md` — usage, backends, traceability contract
- `kernel.py` — helper functions (get_rubric, run_dual_review, verify_quotes,
  detect_disagreements, judge, audit_rows, ...)
