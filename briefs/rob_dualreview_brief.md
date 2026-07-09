# Stream A — Risk of Bias (observational): dual-reviewer hardening

**Date:** 2026-07-08  ·  **Framework:** ROBINS-I (7 domains)  ·  **Studies:** 15 observational/pharmacoepi
**Reviewers:** #1 Claude (`claude-sonnet-5`) · #2 **GPT-5.5** (`gpt-5.5`, reasoning) · judge Claude

## What this run did
The prior session produced a **provisional, rules-based** RoB pass and flagged the cross-model
dual-reviewer run as the planned hardening step. This run completes it. The corpus was staged
12/15; the 3 paywalled full texts (Chang/*Diabetes Obes Metab* PMID 42209408, *Diabetes Res Clin
Pract* PMID 41592697, *Mol Psychiatry* PMID 42000905) were supplied and extracted → **14 full
texts + 1 abstract-only (PMID 42373755)**.

Each study was assessed by **two independent reviewers on different model families**, every domain
rating tied to a **verbatim quote**; per-domain disagreements detected automatically; a Claude
**judge** adjudicated only the split domains, escalating to a human queue where the quote alone
could not resolve the split.

> **Model note.** Reviewer #2 was first run on `gpt-4o` (the harness default) and then re-run on
> **`gpt-5.5`**. The upgrade improved cross-model concordance (63%→71%) and quote verification
> (82%→86%), and removed the only priority (gap≥2) disagreement gpt-4o had produced — i.e. that
> split was a gpt-4o error, not a genuine ambiguity. All results below are the **gpt-5.5** run.

## Headline results
- **Overall RoB (resolved, n=15):** 9 Moderate, 6 Serious, 0 Low.
- **Cross-model agreement:** 75/105 domain judgments (**71%**) matched exactly across two
  independent model families.
- **Quote verification:** **86%** (181/210) of ratings carry a verbatim-substring quote. Unverified
  quotes concentrate in reviewer #2 (reviewer1: 13, reviewer2: 16); all flagged in the audit trail.
  Every headline rating is agreed or judge-adjudicated, so an unverified quote never silently sets a final rating.
- **Concordance with the gpt-4o run:** 14/15 overall ratings identical. One shifted — PMID 40010803
  Low→**Moderate** (gpt-5.5 rates D5 *missing data* and D7 *reporting* as Moderate where gpt-4o
  rated Low; D1 confounding stayed Low for this study).

## Human-expert queue
Of 30 disagreeing domains: **0 priority (gap≥2)**, 10 extraction gaps ("No information" vs a
located rating — reconcile from text), 20 adjacent threshold splits (gap=1, resolved conservatively
worse-of-two, all traceable in the audit CSV). **No domain requires human ordinal adjudication.**

## Effect on GRADE
The resolved distribution (9 Moderate, 6 Serious, no Low) **confirms and slightly strengthens** the
observational RoB downgrades in `grade_certainty.csv`; no certainty rating changes direction.
`grade_certainty_dualreview.csv` records the layer is now dual-reviewer-verified.

## Bearing on the project question
D1 (**confounding by indication**) is the most-downgraded domain — 13/15 studies rated
Moderate/Serious on D1 (Moderate=9, Serious=4, Low=2). This is precisely the bias the brief
names as the leading artifact explanation for the spontaneous-report signal, and the methodological
basis for treating Stream A as the confounding-adjusted comparator against the Stream B (FAERS)
disproportionality signal.

## Files
- `risk_of_bias_observational_dualreview.csv` — resolved 7-domain + overall ratings, escalation flags
- `rob_audit_trail.csv` — 210 rows: (study x domain x reviewer) rating, backend, quote, quote_verified, judge resolution + reason
- `rob_escalation_queue.csv` — 30 disagreeing domains, tiered (0 need human)
- `grade_certainty_dualreview.csv` — GRADE with RoB provenance
- `risk_of_bias_dualreview.png` — traffic-light grid + cross-model concordance

## Reproducibility / harness notes
- Reviewer #2 needs `api.openai.com` on the allowlist (granted) + the `openai` package.
- The published `dual-reviewer-rob` harness hardcodes `model="gpt-4o"`, `max_tokens=4000` (reviewer)
  / `800` (judge), and sends `temperature=0`. All three break on current OpenAI reasoning models:
  gpt-5.x rejects `temperature=0` (only default 1) and needs `max_completion_tokens` (not `max_tokens`),
  and 4k/800 truncate ROBINS-I's 7-domain output. This run patched reviewer→9k/14k (Claude) and a
  dedicated gpt-5.5 reviewer (no temperature, `max_completion_tokens` 16k/24k), judge→2.5k/5k, all with
  JSON-repair retry. **Recommend patching the skill** (default model → a current gpt-5.x, param fixes)
  so the run is turnkey next time.
