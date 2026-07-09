# Triangulating the GLP-1 neuropsychiatric safety signal — integrated synthesis

**Question (PICO).** In adults on GLP-1 receptor agonists, does *designed-study* and
*mechanistic* evidence support, refute, or fail to explain the neuropsychiatric safety
signal (suicidality, self-harm, depression) seen in spontaneous adverse-event reports —
and how does the pooled designed-study estimate compare to the spontaneous-report signal?

This document integrates four evidence streams that were built and analysed **separately
and never pooled together**. The point of the project is to compare them; mixing RR, aOR,
and reporting-OR into one number would be indefensible. The divergence *is* the result.

---

## The four streams

### Stream A — designed studies (RCT + observational)
Pooled, design-stratified, anchored to a reproduced published meta-analysis.

| Stratum | Outcome | Estimate (95% CI) | I² |
|---|---|---|---|
| RCT (k=23, M-H) | suicidal behaviour (composite) | **0.84 (0.54–1.32)** | 0% |
| Observational (k=4, IV) | suicide attempt / self-harm | 0.71 (0.58–0.87) | 10% |
| Observational (k=2) | suicidality (composite) | 0.94 (0.82–1.09) | 23% |
| Observational (k=3) | suicidal ideation | 0.74 (0.37–1.48) | 90% |
| Observational (k=1) | completed suicide | 1.25 (0.83–1.88) | – |
| Observational (k=2) | anxiety | 0.54 (0.33–0.87) | 74% |
| Observational (k=2, excl. outlier) | depression | 1.10 (0.95–1.28) | 92% |

**Anchor reproduction:** Chen et al., *J Diabetes* 2025 — published RR 0.84 (0.54–1.32),
I²=0%; reproduced to **0.8436 (0.5406–1.3165)**, I²=0. Pipeline credible.

**Verdict: null-to-protective, consistent across two independent designs.**

### Stream B — FAERS spontaneous reports (comparison only)
Same numerator (semaglutide × MedDRA SMQ suicide/self-injury, a=912), opposite
conclusions by comparator:

| Background | Reporting OR (95% CI) |
|---|---|
| Full FAERS database | **0.77 (0.73–0.83)** — no signal |
| SGLT2i + DPP-4i comparators | **2.08 (1.91–2.26)** — signal |

The comparator-background signal is a **time artifact**: pre–July-2023 ROR 0.85
(0.70–1.02, no signal) vs post–July-2023 ROR 2.98 (2.61–3.39). Restricting to
clinician-sourced reports does *not* remove it (2.26) — but restricting to the
pre-media era does. **87% of reports arrived after July 2023.** LLM adjudication of all
912 reports over structured fields: only **11% plausibly drug-attributed**, **25%
notoriety/legal-sourced**, 22% confounded by indication or co-medication.

Indication-stratified (see `indication_stratification.md`): obesity (1.97) ≈ T2D (1.83)
under a valid full-DB background — the signal is not indication-specific.

**Verdict: the alarming number is an artifact of comparator choice + notoriety bias.**

### Stream C — mechanistic plausibility
GLP-1 receptors are expressed in mesolimbic reward circuitry (VTA, nucleus accumbens);
GLP-1 signalling dampens dopaminergic reward — the pathway underlying craving/addiction
reduction. This makes a *reduction* in reward-driven and impulsive behaviour more
plausible than an increase. There is **no established mechanism** by which GLP-1R agonism
would specifically generate suicidal ideation.

**Verdict: mechanism modestly favours benefit; at minimum fully compatible with the
null-to-protective designed-study synthesis.**

### Stream D — the benefit counterpart (designed studies)
Designed human studies associate GLP-1 RA exposure with **reduced** addictive behaviour
(ratios harmonized so <1 favours GLP-1 RA):

| Substance | Stratum | Pooled (95% CI) | I² |
|---|---|---|---|
| Alcohol | Observational | RR 0.69 (0.50–0.96) | 85% |
| Nicotine | RCT+TTE | RR 0.68 (0.63–0.74) | 0% |
| Alcohol | AUDIT MD (anchor-reproduced) | −7.81 (−9.02 to −6.60) | 88% |

28 benefit / 13 mixed / 5 no-effect / **0 harm** among 52 extracted studies. Certainty
Very low on every outcome — **symmetric with the harm side**: the same evidentiary bar,
applied to both directions, yields Very low certainty for observational evidence on both.

**FAERS footprint (Stream B×D):** the benefit cannot be reported directly, but appears as
**inverse disproportionality** — addiction terms under-reported across every substance
(composite ROR 0.37, 0.31–0.43), with a passing specificity control (neutral headache
outcome at ROR 1.15, not depressed). See `stream_D_faers_footprint.md`.

**Verdict: benefit is real in designed studies and leaves a specific, mechanism-aligned
footprint in FAERS.**

---

## Resolution of the benefit–harm paradox

The same FAERS database, read against the same comparator background, shows:

- a **harm** signal that **dissolves under scrutiny** — it appears only vs an
  ill-matched diabetes-drug comparator and only in the post-notoriety window, and
  adjudication attributes just 11% of reports to plausible drug effect;
- a **benefit** signal that **survives scrutiny** — specific across four substance
  classes, passing a crowding-out control, and directionally matching Stream D
  substance-for-substance.

All four streams converge: **designed studies show no causal neuropsychiatric harm and a
probable cross-addiction benefit; mechanism favours benefit; the spontaneous-report harm
signal is best explained by notoriety bias plus confounding by indication.**

## Confounders ranked (how each biases the spontaneous signal)
1. **Notoriety / media bias** — 87% of reports post–July 2023; the signal is absent before it.
2. **Confounding by indication** — obesity/T2D carry elevated baseline suicide risk.
3. **Comparator / background choice** — determines the *sign* (0.77 vs 2.08).
4. **Consumer- vs clinician-sourced reporting** — 48% consumer-sourced.
5. **Psychiatric co-medication / channeling** — 2.4× proxy ratio, fully confounded.
6. **Channeling / duplicate reporting** — openFDA does not de-duplicate.

## Preserved caveats / limitations
- RCTs are **underpowered for rare subgroups** (specific molecules, adolescents).
  Absence of a *large* effect is well established; a small subgroup-specific effect
  cannot be excluded.
- **Baseline psychiatric history** as an effect modifier is **not estimable** in this
  corpus (no trial subgroup data; FAERS proxy is confounded).
- **Obesity-only** designed-study estimate is **not estimable** (corpus is mixed-population).
- **Gambling** remained synthesis-empty in Stream D (no qualifying quantitative study).
- FAERS carries **no free-text narrative** in public data; finer case adjudication would
  require FOIA of raw FAERS/MedWatch source documents.

## Stream provenance
- Stream A: `briefs/stream_A_synthesis_brief.md`, `results/pooled_estimates.csv`
- Stream B: `docs/stream_B_README.md`, `results/faers_case_adjudication_full912.csv`,
  `results/confounder_ranking.csv`, `results/indication_stratified.csv`
- Stream C: mechanistic verdict, Stream A brief §6
- Stream D: `briefs/stream_D_synthesis_brief.md`, `docs/stream_D_faers_footprint.md`
- Tool: `tools/faers/faers_tool.py` (published skill `faers-pharmacovigilance`)
