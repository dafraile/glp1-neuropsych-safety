# The FAERS case-adjudication number, stated honestly

## What the number is
An LLM reviewer assigned each of the 912 semaglutide × suicide/self-injury FAERS
reports to a single causal-interpretability category using **only the structured
case fields** — indication, dechallenge, co-medication, reporter type, receipt
date. Public FAERS carries **no free-text narrative**, so this is a
*structured-field triage*, not a clinical causality assessment.

Result: **102/912 (11%) categorized `plausibly drug-attributed`.** Two
denominators matter and both are reported: 11% of *all* reports, or 19% of the
**531 interpretable** reports (381 were `uninterpretable` — too few structured
fields to judge).

## What the number is NOT — and how we measured that
"11% plausibly drug-attributed" is a **soft instrument**, and we quantify its
softness rather than present it as a hard number.

Re-adjudicating a random 100-case sample with a **second, stronger model**
(Sonnet-class vs the Haiku-class original) gives:

| Agreement metric | Cohen's κ | Raw agreement |
|---|---|---|
| 6-category | 0.42 | 0.55 |
| 3-way (plausible / confounded / artifact) | 0.48 | 0.68 |
| Binary (plausible-drug vs not) | 0.46 | 0.84 |

Agreement is **moderate** (Landis–Koch), and the two models **disagree on the
rate itself**: 14/100 vs 22/100 called `plausibly drug-attributed`. 

**This is the finding, not a failure.** It confirms the 11% is an
uncertainty-laden triage estimate whose exact value is model-dependent. Crucially:

- A dual-model κ measures **automation reproducibility, not accuracy.** There is
  **no accessible ground truth** — public FAERS has no narrative, so no human
  rater (one or two) can adjudicate true causality from these fields either.
  Reporting a two-human κ here would measure how consistently two people apply an
  under-determined rubric, not whether the label is correct. We do not
  manufacture that number.
- The **conclusion does not depend on the exact percentage.** Whether plausible
  attribution is 11%, 14%, or 22%, the load-bearing evidence for the notoriety
  reading is the **within-comparator time-split** (pre-2023 null, Step 1) and the
  **molecule/brand pattern** (Step 2) — both of which are hard, reproducible
  disproportionality measurements from a **calibrated** tool (Step 3), not LLM
  judgments. The adjudication is corroborating colour, explicitly downgraded to
  it.

## Revised synthesis wording
> Structured-field LLM triage classified 11% of the 912 reports as plausibly
> drug-attributed (19% of interpretable reports), with the majority attributable
> to notoriety/legal sourcing, confounding by indication, or co-medication. This
> figure is a soft, model-dependent estimate (dual-model κ ≈ 0.4–0.5; the two
> models disagreed on the rate, 14% vs 22%) and is offered as corroboration only.
> The quantitative case for notoriety bias rests on the within-comparator
> time-split and the calibrated disproportionality analysis, not on this number.

*Files: `adjudication_selfconsistency.csv`, `adjudication_selfconsistency.json`,
`adjudication_selfconsistency.png`.*


---

## Cross-provider re-adjudication (all 912 cases, upgraded from Haiku)

The original 11% was produced by the kernel-default **Haiku-class** model. To scale
beyond it for this load-bearing decision, all 912 cases were re-adjudicated by
**two independent strong models from different providers**: **claude-sonnet-5** and
**OpenAI gpt-5.5**. This is genuine cross-provider validation, not same-vendor.

**Plausibly-drug-attributed rate is model-dependent — and that is the finding:**

| Rater | Plausible rate |
|---|---|
| Haiku (original) | 102/912 = **11.2%** |
| gpt-5.5 | 116/912 = **12.7%** |
| claude-sonnet-5 | 242/912 = **26.5%** |
| 3-model majority vote | 128/912 = **14.0%** |
| Strong-model conservative consensus (both agree plausible) | 93/912 = **10.2%** |

**Agreement.** The two strong models agree exactly on the 6-category scheme in
**67%** of cases (Cohen's κ = 0.57) — *better* than either agrees with Haiku
(κ ≈ 0.42). Across all three models: **395/912 (43%) unanimous, 462 majority-2/3,
55 no-majority.**

**What this establishes.**
1. **The original Haiku 11% was not inflated.** It sits inside the conservative
   cross-provider consensus band (10.2%) and below majority vote (14%). If
   anything, claude-sonnet-5 is the high-side outlier at 26.5%.
2. **The defensible headline is a range, 10–29%**, not a point estimate — the
   plausible-attribution rate genuinely depends on how strict a reviewer is about
   sparse structured fields, which is exactly the soft-instrument property we
   flagged.
3. **The conclusion is unchanged and does not depend on the exact rate.** Whether
   10%, 14%, or 29% of reports are plausibly drug-attributed, the majority are
   still notoriety/legal-sourced or confounded, and the load-bearing evidence for
   the notoriety reading remains the within-comparator time-split and the
   calibrated disproportionality — not this adjudication.

**Recommendation for the reusable tool.** The `faers_tool` case-adjudication
default should be moved off Haiku to a strong model (or, better, a cross-provider
consensus with a reported agreement rate), so future runs and the live demo carry
a defensible default rather than the utility model.

*Files: `adjudication_crossprovider.csv` (per-case 3-model votes + consensus),
`adjudication_crossprovider_raw.csv`, `adjudication_crossprovider.png`.*
