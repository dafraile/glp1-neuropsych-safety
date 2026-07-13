# Triangulating the GLP-1 neuropsychiatric safety signal — integrated synthesis

**Question (PICO).** In adults on GLP-1 receptor agonists, does *designed-study* and
*mechanistic* evidence support, refute, or fail to explain the neuropsychiatric safety
signal (suicidality, self-harm, depression) seen in spontaneous adverse-event reports —
and how does the pooled designed-study estimate compare to the spontaneous-report signal?

This document integrates four evidence streams built and analysed **separately and never
pooled together**. Mixing RR, adjusted OR/HR, and reporting-OR into one number would be
indefensible; the *comparison* across streams is the result. All headline counts here are
generated from [`analysis_manifest.json`](analysis_manifest.json) (machine-built from the
data files), not entered by hand.

> **One-paragraph bottom line (calibrated).** Designed studies and current regulatory
> assessments do not show an increased *average* risk of suicidal ideation or behaviour
> with GLP-1 receptor agonists. The available study-level evidence remains insufficient to
> *exclude* modest relative effects or effects in underrepresented subgroups: the pooled
> RCT confidence interval still admits up to a ~37% relative increase, and the corpus is
> underpowered for molecule-, indication-, and age-specific questions. The FAERS signal is
> highly sensitive to comparator and calendar period and is therefore compatible with
> reporting and selection biases — but FAERS alone cannot determine which bias produced the
> pattern. Evidence of addiction-related benefit (Stream D) is promising but very uncertain
> and is treated here as exploratory. The defensible synthesis is: *a concerning
> spontaneous-report pattern does not reproduce consistently across comparators, calendar
> periods, designed studies, or regulatory analyses, so it is not persuasive evidence of a
> causal class-level risk — while modest effects and vulnerable subgroups remain
> incompletely characterised.*

---

## The four streams

### Stream A — designed studies (RCT + observational)
Pooled, design-stratified, anchored to a reproduced published meta-analysis. Strata are
never pooled together.

| Stratum | Outcome | Estimate (95% CI) | I² | GRADE |
|---|---|---|---|---|
| RCT (k=23, M-H) | suicidal behaviour (composite) | 0.84 (0.54–1.32) | 0% | Low |
| Observational (k=4, IV) | suicide attempt / self-harm | 0.71 (0.58–0.87) | 10% | Very low |
| Observational (k=2, IV) | suicidality (composite) | 0.94 (0.82–1.09) | 23% | Very low |
| Observational (k=4, IV) | suicidal ideation | 0.81 (0.44–1.50) | 86% | Very low |
| Observational (k=1) | completed suicide | 1.25 (0.83–1.88) | – | Very low |
| Observational (k=2, IV) | anxiety | 0.54 (0.33–0.87) | 74% | Very low |
| Observational | depression | **not summarised by one effect** (see below) | ≥92% | Very low |

*Certainty basis (signalling-question RoB engine — ROBINS-I 2016 for observational, RoB2 for
RCTs; R1 Claude Opus 4.8, R2 GPT-5.6-sol, blinded Sonnet-5 judge): the core poolable
observational pool is 13 Serious / 3 Moderate, driven by confounding by indication (D1) — as
the PICO anticipated — so every observational stratum starts Low and is downgraded to Very
low. RCTs are 18 High / 2 Some concerns (D4 outcome measurement: psychiatric events captured
through spontaneous adverse-event reporting rather than a systematic instrument), so the RCT
composite starts High and lands at Low. No low-RoB observational subset exists to pool, so an
"exclude Serious-RoB" sensitivity estimate is not estimable (`results/grade_certainty_hybrid.csv`).*

**A null test is not proof of safety.** The RCT composite (0.84, 0.54–1.32) is reassuring
but its upper bound permits a ~32–37% relative increase. Against a prespecified clinically
important harm margin of RR 1.20/1.25, the RCT upper CI (1.37) **does not exclude** that
margin — so the correct statement is "no detected increase," not "harm excluded" or
"equivalence demonstrated." Detectable-effect analysis: the RCT stratum can only detect
RR ≥ ~1.9 at 80% power (71 total events), i.e. it is underpowered for a small effect.
Observational strata that *do* exclude the 1.20 margin: suicidality composite, suicide
attempt/self-harm, anxiety. (`harm_margin_test.csv`, `detectable_effect.csv`,
`absolute_risks.csv`.)

**Absolute risks (RCT):** 8.33 vs 9.19 events per 10,000 treated; absolute risk difference
−0.86 per 10,000 (95% CI −4.94 to +3.22 — crosses zero).

**Rare-event robustness.** Suicidality is sparse (35 vs 36 events; 2 double-zero trials).
I²=0% does not demonstrate homogeneity at this event count. The pooled estimate is stable
across Mantel–Haenszel without continuity correction (0.87), Peto (0.87), fixed-effect
logistic (0.87), a binomial-normal GLMM (0.85), and a 0.5-CC sensitivity (0.84) — continuity
correction is not driving the result. Peto assumptions are questionable in 8 arm-imbalanced
trials (reported, minimal impact given event scarcity). (`rct_rare_event_sensitivity.csv`,
`rct_arm_imbalance_and_zeros.csv`.)

**Depression — not headlined as null-to-protective.** The all-study estimate is 1.44
(0.80–2.58, k=4) with I²≈100%; excluding the large TriNetX outlier (PMID 39424950, HR 2.95)
gives 1.13 (1.005–1.27, k=3) but heterogeneity **remains ~88%**, and the exclusion was not
prespecified. Although that excl-outlier interval now sits marginally above 1, it is
fragile — the Hartung-Knapp CI (0.67–3.11) and the prediction interval (spanning <0.1 to
>25) both cross 1 freely — so it is **not** evidence of a depression signal. The correct
conclusion is **"highly inconsistent and not meaningfully summarised by a single pooled
effect."** HR/OR/RR were treated as interchangeable
log-ratios; defensible for very rare suicidality, more questionable for depression/anxiety —
flagged. (`obs_reml_hk_reruns.csv`, `depression_reframe.md`.)

**Few-study robustness.** Observational outcomes re-pooled with REML and Paule–Mandel τ²,
Hartung–Knapp CIs, prediction intervals (k≥3), and leave-one-out. No LOO drop flips
significance for ideation or depression; point estimates shift materially, underscoring
fragility at k=2–4. (`obs_reml_hk_reruns.csv`, `obs_leave_one_out.csv`.)

**Overlapping populations.** Four studies draw on a shared TriNetX-type US EHR network
(including the depression outlier); they inform *different* outcomes so are not double-counted
within any single pool, but shared-population dependence is a limitation.
(`cohort_overlap_matrix.csv`.)

**Anchor reproduction:** Chen et al., *J Diabetes* 2025 — published RR 0.84 (0.54–1.32),
I²=0%; reproduced to 0.8436 (0.5406–1.3165), I²=0. Pipeline recovers the anchor within CI.

**Verdict (calibrated): no increased average risk detected across two designs; the evidence
does not have the precision to exclude a modest effect, and depression is too heterogeneous
to summarise.**

### Stream B — FAERS spontaneous reports (comparison only)
**Scope: semaglutide (single molecule) × MedDRA SMQ suicide/self-injury (narrow),
a = 912.** openFDA snapshot pinned at `last_updated = 2026-04-28`. This is *not* a
class-level analysis; class/multi-molecule analyses are labelled separately.

**Comparator sensitivity is a finding, not proof of artifact.** The reporting OR spans the
full comparator grid without converging (`faers_comparator_grid.csv`):

| Background | Reporting OR (95% CI) | Signal @ tool default |
|---|---|---|
| SGLT2i | 2.64 (2.38–2.92) | yes |
| SGLT2i + DPP-4i (primary anchor) | 2.08 (1.91–2.26) | yes |
| DPP-4i | 1.65 (1.49–1.81) | yes |
| Other GLP-1 RAs (within class) | 3.29 (3.02–3.60) | yes |
| Sulfonylurea | 0.75 (0.69–0.81) | no |
| Metformin | 0.51 (0.48–0.55) | no |
| Combined non-GLP-1 antidiabetics | 0.84 (0.78–0.90) | no |
| Full database (unmatched) | 0.77 (0.73–0.83) | no |

The estimate is **background-dependent**: it does not, by itself, establish which value is
"true." SGLT2i/DPP-4i comparators are appropriate mainly for a *T2D* estimand, not the mixed
obesity/T2D semaglutide population; the full database is not an indication-matched control,
just another reporting background. The conclusion that survives is **instability across
specifications**, not any single ROR.

**Time-controlled notoriety analysis (replaces the "87% post-2023" claim).** Within the
fixed SGLT2i+DPP-4i comparator, pre–July-2023 ROR 0.85 (0.70–1.02, no signal) vs post 2.98
(2.61–3.39). Because semaglutide use and total reporting also grew, we test the *proportion*
(semaglutide-suicide / all-semaglutide reports) per quarter and controls:
- **Difference-in-differences**, semaglutide vs other GLP-1 RAs, around July-2023:
  DiD = +0.0079 (z = 11.3, p < 0.001) — the jump is specific to semaglutide, not class-wide.
- **Control outcomes** (headache, injection-site) and **control drugs** (other GLP-1 RAs,
  empagliflozin) do **not** show the July-2023 discontinuity (`faers_notoriety_its.*`).
- Interrupted time series at the prespecified July-2023 breakpoint shows a level/slope change;
  alternative breakpoints (Jan/Oct 2023) are reported as sensitivity.

This is **consistent with notoriety bias** — not "proven time artifact." FAERS cannot
identify which bias caused the pattern; it shows the pattern is not stable to the variables
(comparator, calendar time) a causal signal should be robust to.

**Obesity vs T2D — formal interaction test (not point-estimate comparison).** Obesity ROR
2.05 (1.78–2.35) vs T2D 1.77 (1.50–2.09), full-DB background (the diabetes-drug comparator
is invalid for the obesity stratum). Interaction z-test p = 0.19 → the two are **not
significantly different given wide CIs** — the signal is not demonstrably indication-specific,
which is different from "approximately equal." (`faers_indication_interaction.csv`.)

**De-duplication & drug-role sensitivity.** Primary-suspect-only, all-suspect, and
all-mentioned drug-role definitions were run; the exact narrow-SMQ PT list is locked
(`faers_smq_terms_locked.csv`; openFDA does not version MedDRA in the public API).
(`faers_drug_role_sensitivity.csv`, `faers_dedup_analysis.csv`.)

**Case adjudication is corroboration only, framed as triage.** Public FAERS has no
narrative, so a model cannot estimate an attributable fraction from structured fields. Across
three models the "plausibly drug-attributed" share is **11–27%** (majority-vote consensus 14%,
95% CI 11.9–16.4%); cross-model κ = 0.48 (reproducibility, not accuracy). Reproducibility is
**weaker before July-2023** (Fleiss κ 0.30 pre vs 0.49 post) — the pre-notoriety slice is
small and harder to classify. The load-bearing notoriety evidence is the time-controlled
analysis above, **not** the adjudication.

**Verdict (calibrated): the semaglutide suicide reporting signal is comparator- and
calendar-dependent and is compatible with reporting/selection bias; FAERS cannot adjudicate
causation.**

### Stream C — mechanistic plausibility (structured evidence map)
Rebuilt as a **bidirectional evidence map** (`stream_C_evidence_map.csv`, 28 rows, 25
verified PMIDs), classified by evidence level (human/animal/cellular), construct (target
engagement vs behavioural consequence), direction supported, and directness to the clinical
outcome — **not** a directional argument. GLP-1 receptors are expressed in mesolimbic reward
circuitry (VTA, NAc) and GLP-1 signalling can dampen dopaminergic reward, which is compatible
with reduced craving/consumption. But reward, impulsivity, anhedonia, and mood effects are
context-dependent, and at least one line of evidence is bidirectional (acute anxiogenic vs
chronic antidepressant effects). Several proposed harm mechanisms are simply **unstudied**.

**Verdict (calibrated): mechanism is compatible with a reward/craving reduction and offers
no established pathway to suicidality, but mechanistic plausibility is not clinical evidence
and cannot adjudicate the clinical question in either direction. "No established mechanism
for harm" is absence of explanatory evidence, not evidence that harm is absent.**

### Stream D — addiction/reward benefit (designed studies, EXPLORATORY)
Separate from the primary safety question and treated as exploratory. Of 52 extracted
studies, a blind direction + inclusion audit (`docs/stream_D_audit_2026-07.md`) resolves the
6 previously unclassified (5 excluded — wrong outcome / review / biomarker — + 1 no-effect)
and corrects 2 further benefit calls (40577093 a systematic review; 38264360 a weight-outcome
record), giving **45 direction-eligible: 26 benefit / 13 mixed / 6 no-effect / 0 harm**, with
7 excluded (`stream_D_corrected_counts.csv`). "0 harm" was confirmed by an independent blind
pass across all 52 and means **no study reported a pro-addiction direction**, not evidence of
safety.

Design-stratified pooled estimates (harmonised so <1 favours GLP-1 RA), all Very low
certainty and labelled exploratory: alcohol RR 0.69 (0.50–0.96); nicotine RR 0.68
(0.63–0.74); AUDIT MD −7.81 (−9.02 to −6.60, anchor-reproduced from Eshraghi et al.,
eClinicalMedicine 2025). **Vote-counting and "benefit–harm symmetry" are demoted to
hypothesis-generating framing** — they are vulnerable to study size, selective reporting,
and publication bias, and symmetry is a narrative, not a statistical property.

The FAERS "footprint" (addiction terms at ROR < 1) is relabelled **inverse
disproportionality**, NOT "protective/benefit," and is an exploratory consistency check only.
(`inverse_ror_note.md`, `stream_D_reframe.md`.)

---

## External concordance (validation of the method, not independent replication)

- **FDA, 13 January 2026** (Drug Safety Communication). A meta-analysis of **91
  placebo-controlled trials (~107,910 patients)** and a **Sentinel cohort of ~2.24 million
  new users** found no increased risk of suicidal ideation/behaviour; FDA requested removal
  of the suicidality warning from Wegovy/Saxenda/Zepbound labels. (Figures as reported in
  the FDA communication; verify exact trial/patient/cohort counts against the primary DSC
  before citing downstream.)
- **EMA/PRAC, 2024.** Reached a similar no-causal-association conclusion.

These land in the same direction as this project and are useful external validation of the
*method*. They are **not independent replications**: the FDA trial corpus overlaps our RCT
corpus (both draw on the sponsor development programs), and its 91-trial base is larger and
more precise than our abstract-discoverable 23-trial pool — a reason to defer to it on the
average-effect question, not to treat concordance as two independent confirmations.

---

## Resolution of the benefit–harm framing (calibrated)

The same FAERS database, read against the same comparator, shows a **harm** signal that does
not survive comparator/time sensitivity and a **benefit-direction footprint** that is
exploratory and confounded in the opposite direction. This is a *hypothesis-generating*
juxtaposition routed through a shared mesolimbic mechanism — **not** a demonstrated
symmetry and not an inferential argument. The streams converge in *direction* (no persuasive
designed-study harm; exploratory benefit) via independent discovery channels (published
RCTs, observational cohorts, a trial-registry AE arm), but "convergence" here means
consistent direction under separate methods, not four readings that each prove the same
causal claim.

## The decision this informs (one sentence)
The designed, mechanistic, and validated spontaneous-report evidence together are
**consistent with regulators' no-causal-harm conclusion** and **support continued (targeted)
investigation of the GLP-1 addiction/craving repurposing program**, while **not excluding**
molecule-, subgroup-, and age-specific effects that remain incompletely characterised.

## Confounders ranked (how each biases the spontaneous signal)
1. **Notoriety / media bias** — the semaglutide-specific July-2023 discontinuity survives a
   proportion denominator and control outcomes/drugs (DiD p<0.001).
2. **Confounding by indication** — obesity/T2D carry elevated baseline suicide risk.
3. **Comparator / background choice** — determines the *sign* of the ROR (0.51 → 3.29).
4. **Consumer- vs clinician-sourced reporting** — ~48% consumer-sourced.
5. **Psychiatric co-medication / channeling** — fully confounded proxy.
6. **Duplicate reporting** — openFDA does not de-duplicate.

## Preserved caveats / limitations
- RCTs are **underpowered for rare subgroups and a small average effect**; absence of a
  *large* effect is established, a modest or subgroup-specific effect is not excluded.
- **Baseline psychiatric history** as effect modifier is **not estimable** here.
- **Obesity-only** designed-study estimate is **not estimable** (mixed-population corpus).
- Depression is **too heterogeneous to summarise** with one pooled effect.
- FAERS carries **no free-text narrative** in public data; adjudication is triage, not accuracy.
- Human validation is **single-reviewer** (disagreement-adjudication packets prepared); all
  LLM-layer agreement figures are cross-model reproducibility ceilings, not accuracy.
- Stream D is **exploratory**; the FAERS footprint is inverse disproportionality, not benefit.

## Validation (measured pipeline error rates)
See [`VALIDATION_PROTOCOL.md`](VALIDATION_PROTOCOL.md) and `results/validation_summary.csv`.
Headlines: disproportionality tool AUROC **0.76** on the OMOP/Ryan reference set (355/399
pairs estimable) — a *correctly implemented* method, which is exactly why its comparator-/
time-dependent GLP-1 reading is informative; screening precision 0.77 with an estimated
an estimated ~10 missed eligible studies (95% CI 3–35); extraction 0% sign errors
(material-discrepancy 29% genuine,
mostly multi-outcome studies for the human to adjudicate); RoB quote-verification 86%.
Accuracy cells await single-reviewer adjudication of the blinded packets.

## Stream provenance
- Manifest: [`analysis_manifest.json`](analysis_manifest.json) — all headline counts,
  file hashes, model versions, per-analysis status.
- Stream A: `briefs/stream_A_synthesis_brief.md`, `briefs/stream_A_stats_hardening.md`,
  `results/pooled_estimates.csv`, `results/rct_rare_event_sensitivity.csv`,
  `results/obs_reml_hk_reruns.csv`, `results/harm_margin_test.csv`.
- Stream B: `docs/stream_B_README.md`, `docs/faers_task{1,2,3}_*notes.md`,
  `results/faers_comparator_grid.csv`, `results/faers_notoriety_{its,did}.csv`,
  `results/faers_case_adjudication_full912.csv`, `results/adjudication_crossprovider.csv`.
- Stream C: `briefs/stream_C_evidence_map.md`, `results/stream_C_evidence_map.csv`.
- Stream D: `briefs/stream_D_synthesis_brief.md`, `briefs/stream_D_reframe.md`,
  `docs/stream_D_faers_footprint.md`, `results/stream_D_reclassification.csv`.
- Validation: `VALIDATION_PROTOCOL.md`, `results/validation_summary.csv`,
  `results/omop_calibration_results.csv`, `packets/adjudicate_*.csv`.
- Tool: `tools/faers/faers_tool.py`.
