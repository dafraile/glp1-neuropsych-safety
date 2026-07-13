# GLP-1 RA neuropsychiatric safety — evidence triangulation

Triangulating the GLP-1 receptor agonist neuropsychiatric safety signal.
**Primary question:** In adults on GLP-1 RAs, does designed-study and mechanistic
evidence support, refute, or fail to explain the neuropsychiatric safety signal
(suicidality, self-harm, depression) seen in spontaneous adverse-event reports?

Four evidence streams, kept **strictly separate and never pooled together**:
- **Stream A** — designed-study synthesis of the neuropsychiatric **harm** question
  (RCTs + observational pharmacoepidemiology).
- **Stream B** — FAERS spontaneous-report disproportionality (openFDA), **comparison
  only**. Scope: **semaglutide × SMQ suicide/self-injury** (not class-level).
- **Stream C** — mechanistic plausibility, as a structured bidirectional evidence map.
- **Stream D** — **exploratory** designed-study synthesis of the addiction/reward
  **benefit** question, separate from the primary safety question.

Every headline number below is generated from
[`analysis_manifest.json`](analysis_manifest.json) (machine-built from the data files;
run `./reproduce.sh` to regenerate and verify). See
[`TRIANGULATION_SYNTHESIS.md`](TRIANGULATION_SYNTHESIS.md) for the integrated reading and
[`VALIDATION_PROTOCOL.md`](VALIDATION_PROTOCOL.md) for measured pipeline error rates.

## Headline result (calibrated)

Designed studies and current regulatory assessments **do not show an increased average
risk** of suicidal ideation or behaviour with GLP-1 RAs. The study-level evidence is
**not precise enough to exclude** a modest relative effect or effects in underrepresented
subgroups, and the depression outcome is **too heterogeneous to summarise** with a single
pooled effect. This is "no detected increase," not proof of safety or equivalence.

| Stratum | Outcome | Pooled estimate | I² | GRADE |
|---|---|---|---|---|
| RCT (k=23, M-H) | suicidal behaviour (composite) | 0.84 (0.54–1.32) | 0% | Low |
| Observational (k=4, IV) | suicidal ideation | 0.81 (0.44–1.50) | 86% | Very low |
| Observational (k=2, IV) | suicidality (composite) | 0.94 (0.82–1.09) | 23% | Very low |
| Observational (k=4, IV) | suicide attempt/self-harm | 0.71 (0.58–0.87) | 10% | Very low |
| Observational (k=1) | completed suicide | 1.25 (0.83–1.88) | – | Very low |
| Observational (k=4) | depression | not summarisable (I² ≈ 100%) | ≈100% | Very low |
| Observational (k=2, IV) | anxiety | 0.54 (0.33–0.87) | 74% | Very low |

**A null test is not proof of safety.** The RCT upper CI (1.37) does **not** exclude a
prespecified harm margin of RR 1.20/1.25; the stratum can only detect RR ≥ ~1.9 at 80%
power (71 events). Absolute risk difference −0.86 per 10,000 treated (95% CI −4.94 to
+3.22). The pooled RCT estimate is stable across Mantel–Haenszel (no continuity
correction), Peto, logistic, and GLMM specifications — so it is not a continuity-correction
artifact. GRADE ratings are the cross-model **hybrid** ratings
(`results/grade_certainty_hybrid.csv`), which supersede the earlier rules-based first pass
(`results/grade_certainty.csv`, retained for provenance). Anchored to Chen et al.,
*J Diabetes* 2025, reproduced to RR 0.84 (0.54–1.32), I²=0%.

## Stream B — the spontaneous signal is comparator- and calendar-dependent

FAERS disproportionality for **semaglutide × SMQ suicide/self-injury** (a = 912;
openFDA snapshot `2026-04-28`) does not converge across comparators — the reporting OR
ranges from **0.51 (vs metformin) to 3.29 (vs other GLP-1 RAs)**, crossing the no-signal
line depending only on the comparison group (`results/faers_comparator_grid.csv`). The
conclusion that survives is **instability**, not any single ROR.

Within a fixed SGLT2i+DPP-4i comparator the signal is **absent before July 2023**
(0.85, 0.70–1.02) and present after (2.98, 2.61–3.39). A difference-in-differences vs
other GLP-1 RAs gives a semaglutide-specific jump (+0.0079, p < 0.001); control outcomes
(headache, injection-site) and control drugs do **not** show the July-2023 discontinuity
(`results/faers_notoriety_its.csv`, `faers_notoriety_did.csv`). This is **consistent with
notoriety bias** — FAERS cannot prove which bias caused the pattern, only that the pattern
is not robust to comparator and calendar time.

Obesity vs T2D: interaction test p = 0.19 → **not significantly different**, not
"approximately equal." Case adjudication over structured fields (no narrative exists) is
**triage, not an attributable fraction**: plausibly-drug-attributed share 11–27% across
three models (majority-vote 14%, cross-model κ = 0.48 — reproducibility, not accuracy).
Full detail: [`docs/stream_B_README.md`](docs/stream_B_README.md).

## Stream C — mechanism as a bidirectional evidence map

`results/stream_C_evidence_map.csv` (28 rows, 25 verified PMIDs) classifies mechanistic
evidence by level, construct, direction, and directness. GLP-1R signalling in mesolimbic
reward circuitry is compatible with reduced craving/consumption, but reward/impulsivity/
mood effects are context-dependent and some proposed harm mechanisms are unstudied.
**Mechanistic plausibility is not clinical evidence and cannot adjudicate the clinical
question in either direction; "no established mechanism for harm" is absence of explanatory
evidence, not evidence of safety.**

## Stream D — addiction/reward benefit (EXPLORATORY)

Separate from the primary safety question. Of **52** extracted studies, the 6 previously
unclassified resolve to 5 excluded + 1 no-effect → **47 direction-eligible: 28 benefit /
13 mixed / 6 no-effect / 0 harm** (`results/stream_D_reclassification.csv`). "0 harm" means
no study reported a pro-addiction direction, **not** evidence of safety. Vote-counting and
"benefit–harm symmetry" are **hypothesis-generating framing only**. Exploratory pooled
estimates (Very low certainty): alcohol RR 0.69 (0.50–0.96), nicotine RR 0.68 (0.63–0.74),
AUDIT MD −7.81 (−9.02 to −6.60, anchor-reproduced). The FAERS "footprint" is relabelled
**inverse disproportionality**, not benefit. See
[`briefs/stream_D_reframe.md`](briefs/stream_D_reframe.md).

## External concordance (method validation, not independent replication)

- **FDA (13 Jan 2026, Drug Safety Communication):** meta-analysis of **~91
  placebo-controlled trials (~107,910 patients)** and a **Sentinel cohort (~2.24M new
  users)** found no increased risk; requested removal of the suicidality warning from
  Wegovy/Saxenda/Zepbound. (Counts as reported by FDA; verify against the primary DSC.)
- **EMA/PRAC (2024):** similar no-causal-association conclusion.

Same direction as this project, and useful validation of the *method* — but **not**
independent replications: the FDA's 91-trial corpus overlaps and exceeds our
abstract-discoverable 23-trial pool, so it is the more precise trial evidence on the
average effect. Examine overlap rather than counting concordance as confirmation.

## Validation — measured error rates

`results/validation_summary.csv` + [`VALIDATION_PROTOCOL.md`](VALIDATION_PROTOCOL.md).
The disproportionality tool scores **AUROC 0.76** on the OMOP/Ryan reference set (355/399
pairs estimable) — a correctly implemented method, which is why its comparator-/time-
dependent GLP-1 reading is informative. Two-model LLM-layer metrics (cross-model
reproducibility ceilings, not accuracy): screening precision 0.77 (~10 estimated missed
studies, 95% CI 3–35); extraction 0% sign errors; RoB quote-verification 86%; adjudication
κ 0.48.
Human validation is **single-reviewer**: blinded disagreement-adjudication packets are in
`packets/`; accuracy cells stay `awaiting_adjudication` until resolved.

## Repository layout

```
analysis_manifest.json   machine-generated single source of truth for all headline counts
build_manifest.py        regenerates the manifest from the data files
reproduce.sh / Makefile  one-command reproducibility test (manifest -> hashes -> prose)
tests/                   manifest/README consistency + input-hash verification
data/      search, de-duplication, screening ledger, master study table, anchor 2x2 counts
results/   pooled estimates, rare-event + REML/HK reruns, harm-margin, FAERS grid/ITS/DiD,
           GRADE, PRISMA, risk-of-bias, calibration, validation metrics
figures/   forest plots, PRISMA, RoB, GRADE, FAERS demo/ITS, calibration ROC
briefs/    Stream A/D synthesis + hardening briefs, anchor + dual-review RoB briefs,
           Stream C evidence map
docs/      Stream B methods, FAERS task notes, calibration report, falsification, prior work
packets/   blinded disagreement-adjudication packets (one per LLM layer) + scoring key
tools/     dual-reviewer-rob + grade-hybrid harness; faers/ openFDA client (Stream B)
```

## Methods notes

- **Strata never pooled together.** RCT: Mantel-Haenszel on 2×2 counts (no continuity
  correction as primary; Peto/logistic/GLMM as sensitivity). Observational: inverse-variance
  random-effects on adjusted log-effects, with REML/Paule-Mandel + Hartung-Knapp + prediction
  intervals + leave-one-out as robustness.
- **Screening** combined an LLM rubric (418 records) with a rule-based keyword classifier
  (376 records), flagged per record in the ledger.
- **Risk of bias / GRADE** use the cross-model dual-reviewer harness (Claude + GPT-5.5,
  judge-adjudicated, full audit trail); the earlier rules-based first pass is superseded and
  retained only for provenance (see `analysis_manifest.json` → `analysis_status`).
- Two extraction errors were caught and corrected in QC (PMID 40010803 adjusted HR 1.02, not
  crude 2.08; PMID 40897378 all-cause mortality, excluded from pooling) — both confirmed
  correctly resolved in the two-model extraction re-check.

## Not included

Publisher full-text articles are **not** committed (copyright). The screening ledger and
study table carry PMIDs/DOIs to retrieve them.

---
*Generated with Claude Science. Reproduction anchors: Chen et al., J Diabetes 2025;17(9):e70151
(Stream A); Eshraghi et al., eClinicalMedicine 2025 (Stream D). openFDA snapshot 2026-04-28.*
