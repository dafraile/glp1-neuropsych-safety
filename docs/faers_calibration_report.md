# FAERS tool calibration against known controls

> ⚠️ **SUPERSEDED — smoke test only. Do not cite these numbers.**
> This report uses a small (n=40), **hand-built** control set of label-warned
> positives versus OMOP-style negatives. That is an *easy* discrimination task,
> so the AUC 0.995 / sensitivity 1.00 / specificity 0.95 reported below **overstate**
> real-world performance and must not be quoted as the tool's calibration.
> The calibration figure of record is **AUROC 0.76 on the full OMOP/Ryan reference
> set (355/399 estimable pairs)** — see [`omop_calibration_report.md`](omop_calibration_report.md).
> This document is retained only to show the initial smoke test and the two
> informative failure modes it surfaced (over-sensitive single-threshold rules;
> confounding-by-indication false positive). Every headline number in the
> README, synthesis, and manifest uses the OMOP 0.76, not the figures here.

**Purpose.** The strongest objection to any disproportionality analysis is "the
tool produces whatever ROR you point it at." This calibration answers it: run
the *same* `faers_tool` used for the GLP-1 analysis across a reference set of
drug–event pairs with **known ground truth**, and measure whether it recovers
the truth. If it separates established positives from negatives, its GLP-1
verdict is a measurement, not an artifact.

## Reference set (n=40, balanced)
- **20 positive controls** — established, label-warned causal drug–ADR
  associations of the type used as true positives in OMOP / EU-ADR / Ryan et al.
  reference sets: statin–rhabdomyolysis, ACEi–angioedema, clozapine–
  agranulocytosis, allopurinol/carbamazepine/phenytoin–SJS, amiodarone–pulmonary
  fibrosis, metformin–lactic acidosis, ciprofloxacin–tendon rupture,
  infliximab–TB reactivation, warfarin/heparin bleeding & HIT, etc.
- **20 negative controls** — drug–outcome pairs with no known pharmacological
  association (OMOP-style negative controls used to estimate the null), e.g.
  statin–SJS, antihistamine–agranulocytosis, PPI–tendon rupture, aspirin–TB.

Full labeled list with source notes: `faers_reference_set.csv`.

## Results

| Signal rule | Sensitivity | Specificity | PPV | Youden J |
|---|---|---|---|---|
| **Evans (PRR≥2 & χ²≥4 & a≥3) — tool's primary rule** | **1.00** | **0.95** | **0.95** | **0.95** |
| ROR lower-CI > 1 & a≥3 | 1.00 | 0.45 | 0.65 | 0.45 |
| IC025 > 0 | 1.00 | 0.45 | 0.65 | 0.45 |

**Continuous discrimination: AUC = 0.995** (IC025 or ln-ROR as the score).

The Evans multi-criterion rule — the tool's stated primary signal definition —
recovers ground truth almost perfectly: it flags 20/20 known positives and 19/20
known negatives.

## Two informative "errors"
1. **The single-threshold rules are deliberately over-sensitive** (specificity
   0.45). A bare "ROR lower-CI > 1" fires on 11/20 negatives. **This is the
   central methodological lesson for the GLP-1 case:** a lone ROR > 1 is weak
   evidence; the reason the GLP-1 harm reading is defensible is that it rests on
   the *within-comparator time-split* and the multi-criterion gate, not a single
   crossing of ROR = 1.
2. **The one Evans false positive is a "hard" negative:** levothyroxine ×
   pulmonary fibrosis (ROR 3.5). This is confounding by indication —
   hypothyroidism is comorbid with idiopathic pulmonary fibrosis — the *same*
   confounding-by-indication mechanism this project attributes to the GLP-1
   signal. The tool's one miss is itself an instance of the bias we name, not a
   random failure.

## Transparency note
One reference pair required a MedDRA PT correction: digoxin's arrhythmia
association was initially coded as the PT "Cardiac arrhythmia" (unpopulated in
FAERS, a=0); the FAERS-populated PT is "Arrhythmia" (a=1016, Evans=True). This
was a coding choice on our side, corrected before the final metrics — logged
here rather than hidden.

## Bottom line (of this smoke test — superseded)
Against 40 hand-built pairs, the FAERS tool's primary signal rule separated
positives from negatives nearly perfectly. This confirmed the tool was not
emitting arbitrary RORs, but the task was too easy to serve as the calibration
of record. **The trustworthy calibration is AUROC 0.76 on the full OMOP/Ryan
reference set** ([`omop_calibration_report.md`](omop_calibration_report.md)),
which is what the GLP-1 reading actually rests on.

*Files: `faers_reference_set.csv`, `faers_calibration_results.csv`,
`faers_calibration_detail.csv`, `faers_calibration_roc.png`.*
