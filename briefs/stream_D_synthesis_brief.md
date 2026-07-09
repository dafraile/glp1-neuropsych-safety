# Stream D — Cross-Addiction Benefit/Reward Synthesis Brief

**GLP-1 receptor agonists and addiction/reward outcomes: the benefit counterpart to the
Stream A neuropsychiatric-harm synthesis.**

## Headline

Designed human studies consistently associate GLP-1 RA exposure with **reduced**
addictive behaviour across substances — but the certainty of that benefit signal is
**Very low on every outcome**, held down by the same methodological limits (serious
observational risk of bias, imprecision, heterogeneity) that cap the harm-side evidence.
The benefit and harm sides are therefore **symmetric in certainty**: the same evidentiary
bar, applied to both directions, yields Very low certainty for observational evidence on
both. No designed study in this corpus reported a harmful (pro-addiction) direction.

## Corpus (PubMed, as-executed)

- **246** unique records screened (title/abstract), **53 included**, **52 extracted**
  (1 narrative review excluded at extraction).
- Direction of effect among extracted studies: **28 benefit, 13 mixed, 5 no-effect,
  0 harm**.
- Substance coverage (primary tag): alcohol 25, multiple 10, nicotine 9, other/opioid/
  cannabis/stimulant/cocaine 8. **Gambling: 28 records retrieved, but none qualified as a
  designed study with a quantitative gambling outcome — gambling remains synthesis-empty.**
- Designs: secondary-analysis 21, RCT 10, cohort 9, single-arm 5, target-trial-emulation
  4, self-controlled 2, case-control 1.

*Search limits (see protocol):* PubMed only; 7-term drug block (brand names dropped for
the 20-operator API cap); 3 of 4 substance blocks truncated at the 100-hit retrieval cap
(alcohol 383, other 217, nicotine 161 total; gambling 28 full); extraction from abstracts.
This is a benefit-side **scoping** synthesis, not an exhaustive census.

## Anchor reproduction (trust check)

Reproduced the pooled AUDIT-score estimate of **Eshraghi et al., eClinicalMedicine 2025
(PMID 41324012; DOI 10.1016/j.eclinm.2025.103645)** from its Fig. 4 forest data
(4 studies). Independent DerSimonian–Laird + Hartung–Knapp recovered **I² = 87.5%
(exact)**, pooled **MD −7.81** (matches the paper's abstract exactly; Fig. 4 diamond
−7.83, an estimator/rounding difference), and **HK 95% CI [−9.02, −6.60] (exact)**.
τ² diverged (DL 0.280 vs paper 0.399, HK-REML) as expected from the estimator difference.
**Anchor reproduced within CI — the Stream D pipeline is credible.**

## Design-stratified pooled estimates (never pooled across substances or streams)

Poolable estimates mix effect metrics and outcomes, so pooling was restricted to
commensurable substance × metric × design strata (k ≥ 2). Ratio metrics were harmonized
so that **<1 favours GLP-1 RA** (OUD-remission HR and smoking-abstinence RR inverted).

| Substance | Stratum | k | Pooled | 95% CI | I² |
|---|---|---|---|---|---|
| Alcohol | Observational (risk of adverse alcohol outcome) | 4 | RR 0.69 | 0.50–0.96 | 85% |
| Nicotine | RCT + TTE (smoking abstinence / TUD) | 2 | RR 0.68 | 0.63–0.74 | 0% |
| Alcohol | Mixed (AUDIT MD, anchor-reproduced) | 4 | MD −7.81 | −9.02 to −6.60 | 88% |

Single-study strata (opioid OUD-persistence 0.57 [0.40–0.81]; cannabis CUD-incidence
HR 0.56 [0.42–0.75]; multiple-SUD composite HR 0.86 [0.83–0.88] and case-control OR 0.25
[0.22–0.30]) all point protective but are reported individually, never pooled.

## Risk of bias (dual-review, Claude + GPT-5.5, ROBINS-I / RoB2)

- Observational (n=9): **6 Serious, 3 Moderate** — worse than the Stream A observational
  set. Dominant problems: confounding by indication/channeling (who is prescribed a GLP-1
  RA), and — in EHR/registry studies — outcome ascertainment.
- RCTs (n=4): **3 High, 1 Some concerns** — small early-phase trials, short follow-up,
  self-reported outcomes.
- Quote verification 94.7% of domain judgments; 26 judge escalations (adjacent
  threshold splits), 0 priority (gap ≥ 2) disagreements.

## Hybrid GRADE certainty

**All six benefit outcomes → Very low.** Each starts Low (observational) and is
downgraded for risk of bias (−1 to −2), plus inconsistency (alcohol, multiple-SUD) or
imprecision (nicotine, cannabis, opioid). Mechanical domains computed deterministically;
indirectness / publication-bias / magnitude judged by cross-model dual review.

## Benefit–harm symmetry verdict

The project's motivating paradox — a feared neuropsychiatric **harm** signal vs an emerging
addiction-reduction **benefit**, both routed through the same GLP-1R mesolimbic reward
pathway — resolves the same way on both sides when held to designed-study evidence:

- **Harm (Stream A):** designed studies do **not** reproduce the spontaneous-report
  suicidality signal; pooled estimates null-to-protective; RCT composite Low, all
  observational harm outcomes Very low.
- **Benefit (Stream D):** designed studies **consistently** show reduced addictive
  behaviour; pooled estimates protective (RR ≈ 0.68–0.69); all outcomes Very low.

The mechanism is plausibly **real and directionally benefit-leaning** (reward-circuit
down-modulation reduces consumption), but the **certainty** on both the presence of
benefit and the absence of harm is low for the same reason: the designed-study base is
young, observational, confounded by indication, and imprecise. The honest reading is not
"GLP-1 RAs treat addiction" nor "GLP-1 RAs cause psychiatric harm," but: *the reward-
pathway hypothesis points toward benefit and away from harm, and the current designed
evidence is too low-certainty to confirm either with confidence.*

## Confounders that bias the benefit signal (ranked)

1. **Confounding by indication / channeling** — GLP-1 RAs are prescribed to people
   engaged with care (obesity/T2D clinics); treated groups differ systematically from
   comparators on health-seeking behaviour. Biases toward apparent benefit.
2. **Adherence/persistence & healthy-adherer effect** — persistent users differ from
   discontinuers; reduces measured consumption independent of drug.
3. **Outcome ascertainment** — self-reported abstinence and EHR diagnosis codes
   under-capture the outcome; differential between exposed/unexposed.
4. **Regression to the mean / single-arm designs** — before-after alcohol reductions
   partly reflect enrolment at peak use.
5. **Publication & notoriety bias** — a hyped, young literature; positive findings
   surface faster (same post-2023 attention dynamics as the harm signal).
6. **Cohort overlap** — several large-database studies (TriNetX-type) may share patients,
   inflating apparent replication.

## Limitations

PubMed-only, brand-name-trimmed, cap-truncated search; abstract-based extraction and RoB
(full-text would refine both); gambling synthesis-empty; pooling limited by metric/outcome
heterogeneity. All artifacts and audit trails are in `results/` and `data/`.
