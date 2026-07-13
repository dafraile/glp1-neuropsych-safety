# Validation Protocol — measuring the pipeline's error rate

**Project:** Triangulating the GLP-1 RA neuropsychiatric safety signal
**Purpose:** Convert "we automated the review" into "we automated it *and here is its
measured accuracy*." Every automated evidence-synthesis entry claims to work; almost none
reports its own error rate against a human gold standard. This protocol makes that number
the headline. It covers the three LLM-judgment layers (screening, extraction, FAERS
adjudication), the risk-of-bias layer, and a threshold-independent calibration of the
disproportionality tool against a reference set of known drug–event pairs.

The output is a single **Validation Summary** table (§7) to drop into the methods/appendix,
plus per-layer gold-set CSVs committed to the repo.

---

## 0. Global rules (apply to every layer)

- **Blind the human labels.** Raters must not see the pipeline's decision for a record
  before recording their own. Label from the source (title/abstract, full text, or FAERS
  substrate), then join to the pipeline output. Un-blinded labeling silently inflates
  agreement and is the first thing a judge will discount.
- **Human validation is single-reviewer (by design — hackathon constraint).** This
  protocol was written for a two-rater design (two team members labeling independently,
  then adjudicating to consensus, with inter-human agreement reported as the task-difficulty
  ceiling), but that second human rater **was not executed**. What actually ships is one
  human reviewer's blinded labels against the pipeline output; there is **no inter-human
  agreement number**, and the accuracy story rests on cross-model reproducibility ceilings
  plus that single reviewer. See `FROZEN_PROTOCOL.md`, which is the accurate record.
  Treat the two-rater text below as the *intended* design, not what was run.
- **Freeze inputs.** Pin the openFDA data snapshot date (FAERS accrues reports over time,
  so RORs drift), record exact model IDs/versions for every LLM layer, and commit the
  frozen gold-set label CSVs. A validation you can't re-run isn't one.
- **Pre-register the schema.** Write the label definitions (below) *before* labeling. No
  editing category definitions after seeing disagreements.
- **Report every metric with a 95% CI** (Wilson for proportions). Small gold sets have wide
  intervals; showing them is honesty, not weakness.

---

## 1. Layer 1 — Screening (title/abstract include/exclude)

**What it validates:** that the screening classifier isn't silently dropping eligible
studies (false negatives = missed evidence, the cardinal SR sin) or flooding the pool with
junk (false positives).

**Population:** the 794 de-duplicated records, split by pipeline decision (~98 include /
~696 exclude). Because includes are rare, a single random sample estimates recall poorly —
use a **two-part stratified design**:

| Part | Frame | n | Estimates |
|---|---|---|---|
| A — precision + include audit | all pipeline-**includes** (label 100% if ≤100) | ~98 | precision, include error rate |
| B — false-negative audit | random sample of pipeline-**excludes** | 150–200 | miss rate (false-omission rate) |

**Label schema (per record):** `include` / `exclude`, plus a one-word reason for excludes
(`wrong_design`, `wrong_drug`, `wrong_outcome`, `duplicate`, `not_human`). Label from
title+abstract only, matching the pipeline's information state.

**Metrics:**
- **Recall / sensitivity** (primary) = TP / (TP + FN), with the FN count estimated from
  Part B scaled to the full exclude pile. Report as an estimated *count of missed eligible
  studies* with CI — that framing is what a systematic-review methodologist reads first.
- Precision = TP / (TP + FP) from Part A.
- Specificity, F1.
- **Cohen's κ** (pipeline vs human consensus) and **inter-human κ** (ceiling).

**Interpretation:** the number that matters is the missed-study estimate. If Part B surfaces
any eligible study the pipeline excluded, name it, add it (or justify exclusion), and report
the corrected pool. A recall estimate with zero missed studies across 150–200 audited
excludes is a strong, defensible claim.

---

## 2. Layer 2 — Extraction (the pooling-critical numbers)

**What it validates:** that the numbers feeding the meta-analysis are the numbers in the
papers. This is the highest-stakes layer — an extraction error moves the pooled estimate
directly, and you already caught two in QC (PMID 40010803 crude-vs-adjusted HR; PMID
40897378 mortality mis-mapped as neuropsychiatric). Quantify how often that happens.

**Population & sampling:** re-extract **100% of the ~40 poolable studies** — it's tractable
and it's where errors are load-bearing. For the non-poolable remainder of the study table,
audit a random sample of ~20.

**Fields to re-extract (blinded, from full text / abstract):** effect estimate, both CI
bounds, events and N per arm (the RCT 2×2), outcome→standardized-category mapping,
comparator, design tag, and the **direction/sign** of the effect (the error class most
likely to flip a conclusion).

**Metrics:**
- **Per-field accuracy.** Numeric tolerance: counts exact; ratios matched to the paper's
  reported significant figures.
- **Material discrepancy rate** (headline) = share of studies with ≥1 error that would
  change a pooled estimate, its CI materially, or its direction. Report the count and list
  each one with its resolution (as you did for the two QC catches).
- Sign-error rate, reported separately (zero is the expected and required result).

**Interpretation:** report the material discrepancy rate, not raw character accuracy. "0 of
40 pooled studies had a pooling-relevant extraction error after audit" is the claim you
want; if there are any, fix them and re-run the affected pools before the submission
freezes.

---

## 3. Layer 3 — Risk of bias / GRADE judgment

**What it validates:** that the dual-reviewer RoB layer isn't fabricating justifications or
diverging in ways that would change a GRADE downgrade.

**Use what the harness already emits** (`dual-reviewer-rob`):
- **Quote-verification rate.** Every domain rating carries a verbatim quote and a
  `quote_verified` boolean. Report the share of ratings whose quote is a true substring of
  the source. This is a direct, cheap **fabrication rate** — it should be at or near 100%;
  any unverified quote is a red flag to inspect and disclose.
- **Cross-model agreement.** The harness runs two independent reviewers (Claude + GPT-5.5)
  and a judge. Report per-domain agreement, the **major-disagreement rate** (gap ≥ 2), and
  the count of `ESCALATE_TO_HUMAN` domains.

**Add a human spot-check:** have a third rater (ideally a clinician contact) independently
rate a sample of ~10–15 study×domain cells, blinded to the harness resolution, drawn
preferentially from the escalated / major-disagreement rows plus a random remainder.

**Metrics:** quote-verification rate; human-vs-harness domain agreement (κ); % escalated.

**Interpretation:** the escalation queue is a *feature* — it's where the pipeline correctly
declines to overreach. Reporting "N domains auto-escalated to human review, 0 fabricated
quotes" reads as a system that knows its own limits.

---

## 4. Layer 4 — FAERS case adjudication (reproducibility, honestly framed)

**What it validates — and what it can't.** There is **no ground truth** here: public FAERS
carries no free-text narrative, so adjudication runs over structured fields only. You cannot
measure *accuracy* against a true label. You can measure **reproducibility** (cross-model)
and **concurrent validity** (agreement with independent human raters over the same
substrate). Frame it exactly that way; claiming accuracy here is the kind of overreach a
pharmacovigilance judge will pounce on.

**Fix the headline number first.** Replace the single-model "11% plausibly drug-attributed"
with the tool's consensus path:

```python
recs, summary = ft.adjudicate_consensus(subs, host=host)
# report: plausible_consensus_both  ->  plausible_either   (a RANGE)
#         kappa_binary_plausible     (cross-model reproducibility)
```

The tool's own guidance: the plausible-attribution rate is model-dependent and spans
**~10–29%** across models — report the **range with the κ**, never one percentage.

**Human validation:** both team members independently adjudicate a **stratified sample of
~100 reports** over the same structured substrate, blinded to the model tags. Stratify by
(a) the model's assigned category and (b) **pre- vs post-July-2023** (the notoriety split is
central, so validate agreement holds on both sides of it).

**Metrics:** human-consensus vs model agreement (κ, and per-category); **inter-human κ**
(the ceiling — expect it to be modest precisely because the substrate is thin, which is
itself an important thing to report); cross-model κ from `adjudicate_consensus`.

**Interpretation:** a headline of "plausible-attribution 10–29% (cross-model κ = X); human
raters agreed with the consensus tag at κ = Y over the same fields; inter-human κ = Z"
is bulletproof *because* it refuses to claim more than the data supports. The load-bearing
notoriety conclusion does **not** rest on the raw "87% of reports post-July-2023" descriptive
(a raw share is confounded by rising GLP-1 prescribing volume). It rests on the
**time-controlled analysis** in `TRIANGULATION_SYNTHESIS.md`: within a fixed SGLT2i+DPP-4i
comparator the signal is absent before July 2023 (0.85, 0.70–1.02) and present after
(2.98, 2.61–3.39); a difference-in-differences vs other GLP-1 RAs gives a semaglutide-specific
jump (p<0.001); and control outcomes (headache, injection-site) and control drugs show **no**
July-2023 discontinuity (`results/faers_notoriety_its.csv`, `faers_notoriety_did.csv`). Keep
the DiD + clean-control design as the load-bearing evidence, not the raw share.

---

## 5. Layer 5 — Disproportionality calibration (the Build-track centerpiece)

**What it validates:** that `faers_tool`'s signal detection is *calibrated* — it flags real
associations and stays quiet on non-associations — rather than being a machine that returns
whatever ROR you point it at. This is the strongest possible answer to the field's complaint
that FAERS disproportionality papers are uncalibrated churn, and it needs no new domain,
connector, or politics.

**Reference set:** use a curated set of adjudicated **positive- and negative-control**
drug–event pairs — e.g. the **OMOP/Ryan reference set** (~399 pairs across acute liver
injury, acute kidney injury, acute MI, and upper-GI bleeding; positive controls = known
associations, negative controls = pairs with no known association). Pull the current
published version; confirm the license. (The EU-ADR reference set is a fine alternative /
supplement.)

**Procedure:**
1. Map each reference drug to the FAERS drug vocabulary and each outcome to its MedDRA PT
   set. Record **coverage** — the fraction of pairs estimable in FAERS (some will have
   `a = 0`); report it honestly, don't silently drop them.
2. For each estimable pair, run `ft.disproportionality(drug, outcome_PTs,
   background="full")` and capture the **IC lower bound (IC025)** or the ROR lower CI, plus
   the built-in signal flags.

**Metrics:**
- **AUROC (headline, threshold-independent):** rank all estimable pairs by IC025, compute
  area under the ROC against the known positive/negative labels. This is the standard
  calibration metric and doesn't depend on where you set the alert threshold.
- **At the tool's default signal threshold:** sensitivity = flagged / known-positive
  (estimable); specificity = not-flagged / known-negative (estimable).
- Coverage (§5.1 above).

**Interpretation — set expectations honestly.** FAERS disproportionality on these reference
sets typically lands around **AUROC ~0.75–0.80**. Hitting that band means your tool behaves
like a *correctly implemented* disproportionality method — it does **not** mean
disproportionality is a great causal instrument (it isn't, and your GLP-1 case study is the
proof). That distinction, stated plainly, is exactly the calibrated humility this audience
rewards. Pair the number with one line: "the same tool that scores AUROC ~0.78 on known
controls returns a *null* signal for GLP-1×suicidality once notoriety and comparator are
handled — calibrated, and unmoved by the artifact."

---

## 6. External concordance (free validation you already have)

Layer 5 shows internal calibration; the **regulatory concordance** shows external validity.
The EMA PRAC (April 2024) and FDA both concluded no causal GLP-1↔suicidality link and no
label change — the same conclusion your pipeline reaches. State it as validation of the
*method*: an automated pipeline landing where three agencies landed after multi-year reviews
with privileged data. This is your strongest single framing line; §5 makes it quantitative.

---

## 7. Validation Summary (the table for the submission)

| Layer | Metric (headline) | Value | 95% CI | Gold-set n | Ceiling (inter-human) |
|---|---|---|---|---|---|
| Screening | Missed eligible studies | ___ | ___ | 250–300 | κ = ___ |
| Screening | Precision | ___ | ___ | ~98 | — |
| Extraction | Material discrepancy rate | ___ | ___ | ~60 | — |
| RoB | Quote-verification (non-fabrication) rate | ___ | ___ | all ratings | — |
| RoB | Human vs harness agreement (κ) | ___ | — | 10–15 cells | — |
| FAERS adjudication | Plausible-attribution **range** + cross-model κ | ___–___ / κ ___ | — | all 912 | κ = ___ |
| FAERS adjudication | Human vs consensus agreement (κ) | ___ | — | ~100 | κ = ___ |
| Disproportionality | AUROC vs reference set | ___ | ___ | ~399 pairs | — |
| Disproportionality | Sensitivity / specificity @ threshold | ___ / ___ | ___ | est. pairs | — |

---

## 8. Reproducibility & provenance checklist

- [ ] openFDA snapshot date recorded; disproportionality re-runs pinned to it.
- [ ] Model IDs + versions logged for screening, extraction, adjudication, RoB (all layers).
- [ ] Reference-set version + source + license recorded; coverage reported.
- [ ] Gold-set label CSVs committed (blinded labels + consensus), one per layer.
- [ ] Labeling schemas pre-registered (committed before labeling timestamps).
- [ ] Every reported proportion carries a Wilson 95% CI.

---

## 9. Honest limitations (state these, don't hide them)

- Gold sets are **hackathon-scale**; CIs are correspondingly wide — reported, not concealed.
- Raters are the team (plus, where possible, a clinician for RoB), not an independent expert
  panel; inter-human κ is reported so readers can judge the ceiling.
- FAERS adjudication has **no ground truth** (no narrative); Layer 4 measures reproducibility
  and concurrent validity only, never accuracy.
- Reference-set drugs (Layer 5) are a **different therapeutic area** than GLP-1 — that is the
  point (it's a generalization test), but coverage gaps and vocabulary mapping introduce
  their own noise, which is reported.

---

*Hand-off note for Claude Code: build each layer as an independent script writing one
gold-set CSV + one metrics row, so §7 assembles from the row files. Do Layer 5 first — it's
self-contained (no human labeling) and it's the Build-track centerpiece.*
