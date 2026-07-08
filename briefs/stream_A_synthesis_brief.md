# Stream A Synthesis Brief — Designed-Study Evidence on GLP-1 RA Neuropsychiatric Safety

**Project:** Triangulating the GLP-1 neuropsychiatric safety signal
**Stream A scope:** RCTs + observational pharmacoepidemiology (cohort, case-control, self-controlled)
of GLP-1 receptor agonists and neuropsychiatric outcomes (suicidal ideation, suicide attempt/self-harm,
completed suicide, depression, anxiety). Disproportionality/FAERS studies were tagged OUT (Stream B);
preclinical work routed to Stream C.

---

## 1. Headline

**Designed studies do not reproduce the spontaneous-report suicidality signal.** Across both the
randomized and the observational strata — analysed strictly separately — the pooled association between
GLP-1 RA exposure and neuropsychiatric harm is null-to-protective. The one large positive association in
the observational literature is a single high-confounding TriNetX cohort whose removal collapses the
depression estimate to the null.

| Stratum | Method | Outcome | Pooled estimate | I² | GRADE |
|---|---|---|---|---|---|
| **RCT** (k=23) | M-H random, RR on counts | suicidal behaviour (composite) | **0.84 (0.54–1.32)** | 0% | Low |
| **Observational** (k=3) | IV random, adj. log-effects | suicidal ideation | 0.74 (0.37–1.48) | 90% | Very low |
| **Observational** (k=2) | IV random | suicidality (composite) | 0.94 (0.82–1.09) | 23% | Low |
| **Observational** (k=4) | IV random | suicide attempt/self-harm | **0.71 (0.58–0.87)** | 10% | Low |
| **Observational** (k=1) | single study | completed suicide | 1.25 (0.83–1.88) | – | Very low |
| **Observational** (k=3) | IV random | depression | 1.53 (0.74–3.16) → **1.10 (0.95–1.28) excl. outlier** | 100%→92% | Very low |
| **Observational** (k=2) | IV random | anxiety | 0.54 (0.33–0.87) | 74% | Very low |

*(The "suicidality (composite)" bucket holds two studies — CPRD 2025 and a psychiatric-worsening cohort —
whose pre-specified primary outcome is a suicidal-ideation + self-harm + suicide composite, kept distinct
from the ideation-specific studies.)*

Strata are **never pooled together**. The RCT estimate is the credibility anchor; the observational
estimates are directionally concordant but carry higher risk of bias.

---

## 2. Anchor reproduction (trust check)

The pipeline was validated against **Chen et al., *J Diabetes* 2025;17(9):e70151** (25-RCT meta-analysis
of suicidal behaviour). Rebuilding from the published forest-plot 2×2 counts recovered every statistic to
reported precision:

| Statistic | Published | Reproduced |
|---|---|---|
| Pooled RR (random) | 0.84 | 0.844 |
| 95% CI | 0.54–1.32 | 0.541–1.316 |
| Q (χ²), df | 11.24, 22 | 11.24, 22 |
| I² | 0% | 0.0% |
| Events (GLP-1 vs placebo) | 35 vs 36 | 35 vs 36 |

**Verdict: PASS.** The extended synthesis is built on a validated computational base. (A second anchor —
JAMA Psychiatry 2025, rate-ratio 0.76 on person-time — is reserved for the person-time pipeline.)

---

## 3. Evidence base

- **Search:** PubMed (435 raw query hits — 102 suicidality + 333 broad neuropsychiatric — of which 374
  records had retrievable metadata) + OpenAlex (593 retrieved) = **967 records** carried into de-duplication.
  Drug block × outcome block across all 8 molecules and brand names.
- **Screening:** 967 raw → 794 unique after de-duplication → 98 included at title/abstract → confirmed
  strata of **25 RCTs** + **36 observational studies** (15 with poolable adjusted estimates for a core
  outcome; 21 non-poolable — substance-use, overdose, cognitive, healthcare-utilization, or single-arm —
  retained in the study table for transparency). Every record's decision, reason, method (LLM vs
  rule-based), and design tag is in the screening ledger.

---

## 4. What the two strata say, and where they diverge

**RCT stratum (highest credibility).** RR 0.84 (0.54–1.32), I²=0%. The trials are *precise about the
absence of a large effect* and completely consistent, but they are built on only 71 total events across
>80,000 participants. They are **underpowered for rare-event subgroups** — which is exactly the gap where
a spontaneous-report signal can appear without contradicting the trials. RoB2: all "some concerns"
because suicidality was captured via spontaneous adverse-event reporting rather than systematic
instruments (C-SSRS) and was rarely pre-specified.

**Observational stratum.** Directionally concordant with the RCTs and, for suicide attempt/self-harm,
statistically protective (0.71, p=0.001, low heterogeneity). The overall observational pool is *not*
interpretable (I²=99%) because it mixes outcomes and comparators — hence per-outcome pooling. The single
positive outlier (TriNetX obesity cohort, depression HR 2.95) has **Serious** ROBINS-I risk of bias (no
active comparator → confounding by indication / channeling). A sensitivity analysis excluding all
Serious-RoB studies moves the pooled estimate to 0.99 (0.89–1.09).

**Convergence:** two independent designs, kept methodologically separate, both land at null-to-protective.
This is the pattern expected when a spontaneous-report signal is an **artifact** rather than a causal
effect.

---

## 5. Confounders that inflate the spontaneous-report signal (ranked)

Ranked by likely contribution to the Stream A ↔ Stream B discordance:

1. **Notoriety / stimulated reporting (post-July 2023).** The Icelandic Medicines Agency reports and
   ensuing media coverage triggered a reporting surge. Spontaneous systems have no denominator, so a
   publicity-driven rise in reporting *looks* like a rise in risk. Biases Stream B **upward**; absent by
   construction from designed studies.
2. **Confounding by indication.** Depression, anxiety, and prior suicidality are more common in obesity
   and T2D — the treated population. Any database without an active comparator inherits this. It is
   precisely the mechanism behind the one positive observational outlier, and it does not operate in RCTs.
3. **Channeling.** Newer/heavily-marketed agents (semaglutide) are preferentially prescribed to
   higher-BMI, more-comorbid patients, concentrating baseline psychiatric risk in the exposed arm.
4. **Co-medication.** Antidepressant (ROR ~4.5) and benzodiazepine (ROR ~4.1) co-prescription flags
   underlying psychiatric morbidity; in spontaneous data this rides along with exposure.
5. **Consumer- vs clinician-sourced reports.** Direct-to-consumer reporting for these consumer-branded
   drugs raises the share of unvetted, causally-unassessed reports relative to older drug classes.

Active-comparator, new-user observational designs (SGLT2i / DPP-4i / sulfonylurea comparators) neutralize
#2–#4 and land at the null — consistent with the RCTs.

---

## 6. Mechanistic plausibility (one-paragraph verdict)

GLP-1 receptors are expressed in mesolimbic reward circuitry (VTA, nucleus accumbens), and GLP-1 signaling
dampens dopaminergic reward — the same pathway underlying emerging efficacy for craving/addiction
reduction. Mechanistically this makes a **reduction** in reward-driven and impulsive behaviours more
plausible than an increase, and provides a coherent biological route for the *protective* self-harm/anxiety
signals seen in the observational stratum. There is no established mechanism by which GLP-1R agonism would
specifically *generate* suicidal ideation; anhedonia/appetite-suppression concerns remain theoretical and
are not borne out in the designed-study effect sizes. **Verdict: mechanism favors NEITHER harm nor is it
silent — it modestly favors benefit**, and is at minimum fully compatible with the null-to-protective
designed-study synthesis.

---

## 7. Bottom line for triangulation

- Stream A (designed) = **null-to-protective, consistent across two separate designs, anchored to a
  validated reproduction.**
- The spontaneous-report signal (Stream B) is best explained as **notoriety bias + confounding by
  indication**, not causation.
- Mechanism is compatible with benefit, not harm.
- **Caveat preserved:** RCTs are underpowered for rare subgroups (specific molecules, baseline
  psychiatric history, adolescents). Absence of a *large* effect is well established; a small
  subgroup-specific effect cannot be excluded and is the legitimate residual question for Stream B's
  molecule/indication-stratified analysis.

---

## Artifacts

- `search_raw.csv` — 967 raw records (PubMed + OpenAlex)
- `dedup_pool.csv` — 794 unique records
- `screening_ledger.csv` — every record: source, IDs, include/exclude + reason, design tag, method
- `study_table.csv` — master study table (25 RCT + 36 observational)
- `pooled_estimates.csv` — design-stratified pooled estimates
- `risk_of_bias_summary.png`, `risk_of_bias_rct.csv`, `risk_of_bias_observational.csv` — RoB2 + ROBINS-I
- `forest_reproduction.png` (RCT stratum / anchor), `forest_observational.png`, `forest_by_outcome.png`
- `prisma_evidence_map.png`, `prisma_counts.csv`
- `grade_summary.png`, `grade_certainty.csv`
- `anchor_reproduction_brief.md` — the trust-check detail

*Method note: title/abstract screening combined an LLM rubric (418 records) with a transparent
rule-based classifier (376 records; every rule traces to explicit keyword logic). Design and outcome
were confirmed at full-text/abstract for every study entering the meta-analysis. Two extraction errors
were caught and corrected during QC: PMID 40010803 (adjusted HR 1.02, not the crude 2.08) and
PMID 40897378 (0.56 was all-cause mortality, not a neuropsychiatric outcome — study excluded from pooling).*
