# Prior-work positioning and the decision this informs

## The existing literature (named, with what each contributes)

The GLP-1 / suicidality question is not new. The closest prior work falls in
three groups:

**FAERS / spontaneous-report disproportionality studies**
- Schoretsanitis et al., *BMC Medicine* 2024 (PMID 38355513) — early FAERS
  disproportionality; reported a semaglutide signal.
- *Postmarket safety profile of suicide/self-injury for GLP-1 RA*, Eur
  Psychiatry 2023 (PMID 38031404) — the first-wave FAERS signal report.
- *Psychiatric Safety Signals of GLP-1 RAs: A FAERS-Based Pharmacovigilance
  Study*, Pharmaceuticals 2026 (PMID 42356570); *Comparative pharmacovigilance
  analysis of suicidality-related AEs among GLP-1*, Int J Clin Pharm 2026 (PMID
  41739406) — later, more molecule-resolved FAERS analyses.

**Designed-study meta-analyses / large cohorts**
- *Impact of GLP-1 RAs on Suicide Behavior: A Meta-Analysis Based on RCTs*, J
  Diabetes 2025 (PMID 40887719) — **the anchor this project reproduces** (RR
  0.84).
- *Association of GLP-1 RAs With Risk of Suicidal Ideation and Behaviour: A
  Systematic Review*, Diabetes Metab Res Rev 2025 (PMID 39945396).
- *Suicide and Self-Harm Events With GLP-1 RAs in Adults With Diabetes or
  Obesity*, JAMA Psychiatry 2025 (PMID 40105856) — large cohort, null-to-
  protective; the observational counterpart.

**Integrative / narrative reviews** (the "McIntyre-style" benefit–harm framing)
- A targeted PubMed query for integrative reviews explicitly tying the
  reward-pathway/addiction literature to the suicidality signal
  ("semaglutide suicidality neuropsychiatric review McIntyre") **returned zero
  hits** in this search. The adjacent literature that does surface is
  generic obesity-management or safety narrative reviews (e.g. PMID 42025961,
  *Semaglutide for obesity management: efficacy, safety, and future
  directions*) that mention neuropsychiatric safety but do **not** execute a
  benefit–harm triangulation. This is itself informative: the integrative
  benefit–harm framing exists in commentary (e.g. McIntyre and colleagues have
  argued for it in editorial venues) but a **quantitative multi-stream execution
  of it is not present in the indexed primary literature** we retrieved.
  *(Note: this is based on the PubMed/OpenAlex search in this project; a full
  Embase/PsycINFO sweep was not performed and could surface additional reviews.)*

## What is genuinely new here

Every prior entry does **one** of: a FAERS signal, a designed-study pool, or a
narrative synthesis. None does all three quantitatively and holds them apart.
This project's novel contributions:

1. **Four-stream benefit–harm symmetry, never pooled.** The same FAERS database,
   read against the same comparator background, shows a harm signal that
   *dissolves* (only post-notoriety, only the news-named brands) and a benefit
   footprint that *survives* (specific across four substance classes, passing a
   crowding-out control). One database, symmetric treatment, opposite fates —
   this is the argument no prior paper makes.
2. **Validated, calibrated tooling as the reproducibility backbone.** Prior FAERS
   papers assert their disproportionality; this one **calibrates the instrument**
   against the OMOP/Ryan reference set — **AUROC 0.76 on 355/399 estimable
   drug–event pairs** (`docs/omop_calibration_report.md`) — and **measures its own
   error rate** (screening precision 0.77 with ~10 estimated missed studies [95% CI
   3–35]; extraction 0% sign errors; RoB quote-verification 86%; adjudication
   self-consistency κ≈0.48, reported honestly as reproducibility not accuracy).
   Being the entry that quantifies its own error rate is the separation from the
   pile. (An earlier n=40 hand-built control set scored AUC 0.995 but was an easy,
   label-warned-positive-vs-OMOP-negative smoke test; it is retained only as
   `docs/faers_calibration_report.md`, marked superseded — the OMOP 0.76 is the
   figure that stands.)
3. **A registry adverse-event arm** (483 trials screened, 59 with suicide AEs)
   whose crude across-trial aggregation gives RR 0.86, consistent in direction
   with the RCT null, from safety-table data the bibliographic search cannot
   reach. NB: this is currently a **crude summed 2×2**, not a trial-stratified
   Mantel–Haenszel/Peto pool — so it corroborates *direction* only. A proper
   stratified registry pool (with anchor de-duplication and molecule
   stratification) is the highest-value remaining analysis; see the handover
   note. Do not let the crude number carry more than "consistent direction."
4. **The notoriety mechanism made quantitative and falsifiable:** within-
   comparator time-split + the tirzepatide pharmacological falsifier, not a
   hand-wave about media attention.

## The decision this informs (one sentence)

**The designed, mechanistic, and validated-spontaneous-report evidence together
support regulators' no-causal-harm conclusion, support advancing the GLP-1
addiction/craving repurposing program, and argue against adding a class-wide
suicidality warning — while leaving molecule-, subgroup-, and age-specific
questions open for targeted study.**

## Headline track

**Research finding**, headlined. The reusable tools —
`faers-pharmacovigilance`, `dual-reviewer-rob`, `grade-hybrid` — are presented as
the *reproducibility backbone of the finding*, not as a separate Build
submission. The live triangulation demo (a judge typing a new drug–event pair
and watching the pipeline run) is the proof of reusability.
