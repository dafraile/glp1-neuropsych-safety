# FAERS adjudication — human concurrent-validity check

**Reviewer:** single expert (project PI). **Packet:** 40 cases, disagreement-enriched
(model-vs-model conflicts + a random agreement confirmation subset), NOT a random sample.

## Framing (per VALIDATION_PROTOCOL.md, Layer 4)
There is **no ground truth** for FAERS case adjudication: public FAERS carries no free-text
narrative, so adjudication runs over structured fields only. Accuracy against a true label
**cannot** be measured and is not claimed here. What is reported is **concurrent validity** —
chance-corrected agreement (Cohen's kappa) between the single human reviewer and each model,
plus a qualitative description of where they diverge. Raw percent-agreement is shown only
alongside kappa and is explicitly NOT an accuracy figure.

## Human vs model concordance (concurrent validity, n=40 disagreement-enriched)
| Model | Cohen's kappa | 95% CI (bootstrap) | raw % agreement (not accuracy) |
|---|---|---|---|
| claude-sonnet-5 | 0.16 | 0.00-0.31 | 0.35 |
| gpt-5.5 | 0.26 | 0.11-0.43 | 0.42 |

Agreement is **slight-to-fair**. Raw percent-agreement (0.35/0.42) overstates concordance
because categories are imbalanced (23/40 uninterpretable), which is exactly why the
chance-corrected kappa is the metric of record. For scale, the model-vs-model reproducibility
ceiling on the full 912 is kappa ~= 0.48; human-vs-model concurrent validity sits below that.

## Where human and models diverge (qualitative, descriptive — not an error rate)
- Human labelled 23/40 `uninterpretable`; the models called those same cases uninterpretable
  only 8 (sonnet-5) / 10 (gpt-5.5) times. On ~61% of the cases the human found unadjudicable,
  the models made a definite call.
- Human assigned **zero** `confounded_by_indication` (not identifiable at the case level — every
  case carries the obesity/T2D indication, so there is no within-case contrast). The models
  assigned it 6 / 1 times, restating a population-level fact as a case judgment.
- gpt-5.5 placed 17/40 in `notoriety_or_legal_sourced` vs the human's 0.

The consistent pattern is that the models express categorical confidence where the reviewer
abstains. This is a description of divergence, not a measurement of model error against truth.

## What the human review caught that the automated pass missed
- Two `confounded_by_comedication` cases the co-med classifier had scored 0 psychiatric
  co-meds: **vortioxetine** (FAERS_002) and **esketamine** (FAERS_037) — newer antidepressants
  absent from the original drug list. Detector expanded accordingly (clear
  antidepressants/antipsychotics added; gabapentin/pregabalin/hydroxyzine left
  flagged-but-not-counted as they are as often prescribed for pain/allergy).
- One keyboard-typo mislabel (FAERS_034, antidiabetics only) corrected to uninterpretable.

## Interpretation
Low chance-corrected concordance, combined with the models' tendency to attribute where the
reviewer abstains, is consistent with the protocol's premise: spontaneous-report case
adjudication cannot manufacture causal signal the structured fields do not contain. This
supports treating Stream B as comparison-only and resting inference on the comparator grid and
time-controlled analyses, not case counts.

## Caveats
1. n=40, disagreement-enriched -> a directional, concurrent-validity finding, not a
   corpus-wide agreement estimate.
2. Single reviewer -> concurrent validity against one expert, NOT a two-independent-reviewer
   reliability estimate, and NOT accuracy against ground truth (none exists). See
   VALIDATION_PROTOCOL.md Layer 4 and FROZEN_PROTOCOL.md.
