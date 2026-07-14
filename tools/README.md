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

## grade-hybrid

Hybrid GRADE certainty-of-evidence engine. A **deterministic** core rates the
arithmetic domains — risk-of-bias aggregation (from the resolved per-study
ratings), inconsistency from I², and imprecision from CI width / event counts /
optimal information size — with a full rule-trace, while a **dual-reviewer**
harness (Claude + OpenAI + a judge tier) rates the judgment domains
(indirectness, publication bias, magnitude/upgrade calls). RCT evidence starts
High and observational starts Low, and the two streams are kept separate.

It consumes the resolved output of `dual-reviewer-rob` and produces an
accountable, reproducible Summary-of-Findings table instead of a hand-assembled
one. Also published as a Claude Science skill; this copy is the versioned source.

- `SKILL.md` — usage, domain-by-domain logic, reviewer configuration

## faers

An openFDA / FAERS **pharmacovigilance disproportionality** client. It pulls
spontaneous adverse-event reports, standardises outcomes to a locked MedDRA SMQ
term set (suicide/self-injury), and computes the standard disproportionality
signals — **PRR, ROR, and IC** — against either the full-database background or
a **custom active-comparator** background (e.g. other GLP-1 RAs, SGLT2i, DPP-4i,
metformin), which is what lets you probe confounding by indication and
comparator sensitivity.

It also supports time-split / interrupted-time-series analyses (for notoriety
checks) and was calibrated against the OMOP/Ryan reference set (AUROC 0.76)
before use. Also published as a Claude Science skill; this copy is the versioned
source of record.

- `faers_tool.py` — the disproportionality client (backgrounds, term sets, PRR/ROR/IC)
- `SKILL.md` — usage, comparator options, calibration notes
