---
name: grade-hybrid
description: >-
  Hybrid GRADE certainty-of-evidence assessment for a systematic review. A
  DETERMINISTIC engine rates the mechanical domains (risk-of-bias aggregation
  from resolved per-study ratings, inconsistency from I2, imprecision from CI
  width / event counts / OIS) with a full rule-trace, and a DUAL-REVIEWER
  harness (Claude + GPT-5.5 + judge) rates the judgment domains (indirectness,
  publication bias, magnitude of downgrade, and the observational upgrade
  factors incl. plausible-confounding-toward-null). RCTs start High,
  observational starts Low; streams are kept separate. Consumes the output of
  dual-reviewer-rob. Use when you need an accountable, reproducible
  Summary-of-Findings table rather than a hand-assembled one.
---

# Hybrid GRADE certainty assessment

GRADE is not one kind of task. Three of its domains are **arithmetic on numbers
you already have** (risk-of-bias aggregation, inconsistency, imprecision) and
four are **judgment read from context** (indirectness, publication bias, the
-1-vs-2 magnitude calls, and the observational upgrade factors). This skill
splits them accordingly: a transparent rule engine for the first set, the
dual-reviewer + judge pattern (from `dual-reviewer-rob`) for the second.

## When to use
- You have pooled estimates per outcome (effect, CI, I2, k, event counts) and
  resolved per-study RoB ratings, and need a defensible certainty rating.
- You want the RoB->GRADE dependency **live**: a RoB reclassification flows into
  the body-of-evidence downgrade automatically instead of being hand-copied.
- You need a Summary-of-Findings row per outcome carrying BOTH the rule-trace
  (which number triggered each mechanical downgrade) and the reviewer/judge
  audit trail (for the judgment domains).

## Backends
- **Mechanical domains** — pure Python, no LLM, runs anywhere (incl. the repl
  tool). Deterministic and reproducible.
- **Judgment domains** — reviewer #1 Claude (`host.llm`), reviewer #2 **GPT-5.5**
  at `reasoning_effort="high"` (needs an OpenAI key + `api.openai.com` allowlisted).
  Set `backend2="claude"` for two independent Claude passes when no OpenAI key /
  quota is available.
- **Judge** — Claude by default; adjudicates only disagreeing judgment domains.

## Kernel helpers (auto-loaded)
Deterministic: `rob_body_downgrade`, `inconsistency_downgrade`,
`imprecision_downgrade`, `deterministic_profile`, `apply_deltas`.
Judgment (host-side; call from the repl tool): `review_grade_claude`,
`review_grade_openai`, `judge_grade_domain`, `dual_review_judgment`.
One-call per SoF row: `grade_row(...)`.

## Workflow

```python
# One SoF row, full hybrid (mechanical compute + dual-reviewer judgment):
row = grade_row(
    outcome="anxiety", stratum="Observational", is_rct=False,
    study_overalls=["Moderate","Serious"],   # resolved ROBINS-I overalls for this outcome
    I2=74, k=2, ci_low=0.33, ci_high=0.87, events=None,
    backend2="openai")                        # or "claude" for the no-OpenAI fallback
row["final_certainty"]                        # e.g. "Very low"
row["profile"]                                # per-domain deltas + reasons + subtotal
row["judgment"]["audit"]                      # reviewer/judge trail for judgment domains
```

Mechanical-only (no LLM), e.g. to sanity-check an existing table:
```python
prof = deterministic_profile(start="Low", study_overalls=[...], I2=90, k=3,
                             ci_low=0.37, ci_high=1.48)
prof["level_after_deterministic"]
```

## GRADE arithmetic
`final = start + sum(downgrades) + sum(upgrades)`, floored at Very low, capped at
High. RCT starts High, observational starts Low. **Upgrades apply to observational
evidence only** and only when no downgrade for the same concern applies; the
harness forces all upgrade deltas to 0 for RCTs. Feed **resolved** per-study RoB
overalls from `dual-reviewer-rob` into `study_overalls` so the body-of-evidence
RoB downgrade tracks the hardened ratings.

## Traceability contract
- Every mechanical downgrade carries the number that triggered it
  (`{"delta": -1, "reason": "substantial heterogeneity (I2=90%)"}`).
- Every judgment domain carries both reviewers' deltas + reasons and, on
  disagreement, the judge resolution; an unresolved judge call resolves
  conservatively (the smaller delta) and is marked for human review.
- The engine surfaces arithmetic errors in hand-built SoF tables: run it over an
  existing table and any row where `final_certainty` differs from the recorded
  value is a table error or an undocumented judgment call. (In this project it
  caught two rows where a RoB downgrade was recorded but not applied.)

## Notes
- This skill does not compute the pooled estimate or the RoB ratings — feed it
  the meta-analysis output and the `dual-reviewer-rob` resolved ratings.
- Imprecision defaults: k<=2, CI-crosses-null, events<OIS (300), or CI ratio >3x
  each trigger -1. Override `ois=` per outcome; pass `events=` when known.
