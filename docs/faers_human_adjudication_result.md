# FAERS adjudication — human validation result

**Reviewer:** single expert (project PI). **Packet:** 40 cases, disagreement-enriched
(model-vs-model conflicts + a random agreement confirmation subset), NOT a random sample.

## Headline
Model accuracy against the human reference standard is low and the error is systematic,
not random:

| Model | Accuracy vs human (n=40) | 95% CI |
|---|---|---|
| claude-sonnet-5 | 0.35 | 0.22–0.50 |
| gpt-5.5 | 0.42 | 0.29–0.58 |

The direction of disagreement is the finding: **the models over-attribute; the human
abstains.**

- Human labelled 23/40 `uninterpretable`; the models called those same cases
  uninterpretable only 8 (sonnet-5) / 10 (gpt-5.5) times. On **57–65%** of the cases the
  human found unadjudicable, the models made a confident, definite call.
- Human assigned **zero** `confounded_by_indication` (not identifiable at the case level —
  every case carries the obesity/T2D indication, so there is no within-case contrast).
  The models assigned it 6 / 1 times, restating a population-level fact as a case judgment.
- gpt-5.5 placed 17/40 in `notoriety_or_legal_sourced` vs the human's 0.

## Human reference-standard category shares (this packet)
plausible_drug_attributed 5/40 (12.5%); confounded_by_comedication 12/40; uninterpretable
23/40 (57.5%); confounded_by_indication 0; notoriety 0.

## What the human review caught that the automated pass missed
- Two `confounded_by_comedication` cases the co-med classifier had scored 0 psychiatric
  co-meds: **vortioxetine** (FAERS_002) and **esketamine** (FAERS_037) — newer
  antidepressants absent from the original drug list. Detector expanded accordingly
  (clear antidepressants/antipsychotics added; gabapentin/pregabalin/hydroxyzine left
  flagged-but-not-counted as they are as often prescribed for pain/allergy).
- One keyboard-typo mislabel (FAERS_034, antidiabetics only) corrected to uninterpretable.

## Interpretation
This is direct evidence that spontaneous-report case adjudication — by model OR human —
cannot manufacture causal signal the structured fields do not contain. It supports, rather
than undermines, the decision to treat Stream B as comparison-only and to rest the
inference on the comparator grid and time-controlled analyses, not case counts. The LLM
adjudication layer is triage with a documented tendency to false confidence; it is not a
causal-attribution instrument.

## Caveats
1. n=40, disagreement-enriched → the raw accuracy understates whole-corpus agreement; this
   is a directional finding about HOW models err, not a corpus-wide accuracy estimate.
2. Single reviewer → "agreement with one expert", not a two-independent-reviewer gold
   standard (see FROZEN_PROTOCOL.md).
