# FAERS adjudication — human concurrent-validity check

**Reviewer:** single expert (project PI). **Packet:** 40 cases, disagreement-enriched
(model-vs-model conflicts + a random agreement confirmation subset), NOT a random sample.

## Framing (per VALIDATION_PROTOCOL.md, Layer 4)
There is **no ground truth** for FAERS case adjudication: public FAERS carries no free-text
narrative, so adjudication runs over structured fields only. Accuracy against a true label
**cannot** be measured and is not claimed. What is reported is **concurrent validity** —
chance-corrected agreement (Cohen's kappa) between the single human reviewer and each model.
Raw percent-agreement is shown only alongside kappa and is explicitly NOT accuracy.

## PRIMARY metric: the load-bearing call (plausible drug attribution vs not)
The distinction the synthesis actually rests on is binary: is a report a plausible
drug attribution, or not? Concordance on THAT call, per model:

| Model | Cohen's kappa (plausible-vs-not) | model plausible / human plausible / overlap |
|---|---|---|
| gpt-5.5 | **0.63** (substantial) | 4 / 5 / 3 |
| claude-sonnet-5 | **0.09** (chance-level) | 11 / 5 / 2 |

The two models diverge sharply on the decision that matters: **gpt-5.5 tracks the expert**
on whether a real drug signal is present; **sonnet-5 does not** — it over-attributes
plausibility (11 plausible calls vs the reviewer's 5, overlapping on only 2). A single
blended kappa across all five categories hides this split, which is why the binary call is
reported as primary.

CIs are wide at n=40 (bootstrap lower bounds approach 0); these are directional
concurrent-validity estimates, not precise reliability coefficients.

## SECONDARY: full 5-category concordance
| Model | Cohen's kappa (5-category) | raw % agreement (NOT accuracy) |
|---|---|---|
| claude-sonnet-5 | 0.16 | 0.35 |
| gpt-5.5 | 0.26 | 0.42 |

The 5-category kappa is lower largely because of churn among the three "cannot-attribute"
sub-labels (indication / notoriety / uninterpretable), which are not cleanly separable at
the case level. Collapsing indication->uninterpretable or to a 3-way scheme does not raise
concordance materially; collapsing to the binary plausible call does (gpt-5.5 0.26->0.63),
locating the agreement in the decision that matters and the disagreement in the fuzzy
confounder sub-categories. For scale, the model-vs-model reproducibility ceiling on the
full 912 is kappa ~= 0.48.

## Where human and models diverge (qualitative, descriptive — not an error rate)
- Human labelled 23/40 `uninterpretable`; the models called those same cases uninterpretable
  only 8 (sonnet-5) / 10 (gpt-5.5) times — on ~61% of cases the human found unadjudicable,
  the models made a definite call.
- Human assigned **zero** `confounded_by_indication` (not identifiable at the case level —
  every case carries the obesity/T2D indication, so there is no within-case contrast). The
  models assigned it 6 / 1 times, restating a population-level fact as a case judgment.
- gpt-5.5 placed 17/40 in `notoriety_or_legal_sourced` vs the human's 0.

## What the human review caught that the automated pass missed
- Two `confounded_by_comedication` cases the co-med classifier scored 0 psychiatric co-meds:
  **vortioxetine** (FAERS_002) and **esketamine** (FAERS_037) — newer antidepressants absent
  from the original drug list. Detector expanded (clear antidepressants/antipsychotics added;
  gabapentin/pregabalin/hydroxyzine left flagged-but-not-counted as they are as often for
  pain/allergy).
- One keyboard-typo mislabel (FAERS_034, antidiabetics only) corrected to uninterpretable.

## Interpretation
On the binary call that carries the inference, gpt-5.5 shows substantial concurrent validity
with the expert and sonnet-5 shows essentially none — a model-specific reliability finding,
not a blanket "LLMs fail." More broadly, the reviewer's high abstention rate where the fields
do not support a call is consistent with the protocol's premise: spontaneous-report case
adjudication cannot manufacture causal signal the structured fields do not contain. This
supports treating Stream B as comparison-only and resting inference on the comparator grid
and time-controlled analyses, not case counts.

## Caveats
1. n=40, disagreement-enriched -> directional concurrent-validity estimates, not corpus-wide
   agreement; CIs are wide. A tighter estimate would need ~30-40 additional RANDOMLY drawn
   (not disagreement-enriched) cases.
2. Single reviewer -> concurrent validity against one expert, NOT a two-independent-reviewer
   reliability estimate, and NOT accuracy against ground truth (none exists). See
   VALIDATION_PROTOCOL.md Layer 4 and FROZEN_PROTOCOL.md.
3. Model rubrics were NOT retro-fitted to the reviewer's decision rules; doing so and
   re-scoring against the same reviewer would be circular. Any future rubric-clarified re-run
   is a revised plausible-fraction estimate, not independent validation.
