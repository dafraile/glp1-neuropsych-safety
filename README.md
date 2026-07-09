# GLP-1 RA neuropsychiatric safety — Stream A (designed-study synthesis)

Triangulating the GLP-1 receptor agonist neuropsychiatric safety signal.
**Primary question:** In adults on GLP-1 RAs, does designed-study and mechanistic
evidence support, refute, or fail to explain the neuropsychiatric safety signal
(suicidality, self-harm, depression) seen in spontaneous adverse-event reports?

This repository holds **Stream A** — the designed-study evidence synthesis (RCTs +
observational pharmacoepidemiology). Two other streams are kept strictly separate and
are **not** pooled with Stream A: Stream B (FAERS spontaneous reports, comparison only)
and Stream C (mechanistic plausibility).

## Headline result

Designed studies do **not** reproduce the spontaneous-report suicidality signal.
Analysed in two design strata kept strictly separate, the pooled association is
null-to-protective on every outcome.

| Stratum | Outcome | Pooled estimate | I² | GRADE |
|---|---|---|---|---|
| RCT (k=23, M-H) | suicidal behaviour (composite) | 0.84 (0.54–1.32) | 0% | Low |
| Observational (k=3, IV) | suicidal ideation | 0.74 (0.37–1.48) | 90% | Very low |
| Observational (k=2, IV) | suicidality (composite) | 0.94 (0.82–1.09) | 23% | Very low |
| Observational (k=4, IV) | suicide attempt/self-harm | 0.71 (0.58–0.87) | 10% | Very low |
| Observational (k=1) | completed suicide | 1.25 (0.83–1.88) | – | Very low |
| Observational (k=3, IV) | depression | 1.53 (0.74–3.16) → 1.10 excl. outlier | 100% | Very low |
| Observational (k=2, IV) | anxiety | 0.54 (0.33–0.87) | 74% | Very low |

GRADE ratings above are the **hybrid** ratings (`results/grade_certainty_hybrid.csv`):
mechanical domains computed deterministically, judgment domains via cross-model dual
review (Claude + GPT-5.5). They supersede the earlier hand-built `grade_certainty.csv`,
which under-applied the body-of-evidence risk-of-bias downgrade on two observational
outcomes (suicidality composite, suicide attempt/self-harm — both now Very low).

The pipeline is anchored to a published meta-analysis (Chen et al., *J Diabetes* 2025)
and reproduces its pooled RR of 0.84 (0.54–1.32), I²=0%, to reported precision.

## Repository layout

```
data/      search, de-duplication, screening ledger, master study table, anchor 2x2 counts
results/   pooled estimates, reproduction check, GRADE, PRISMA counts, risk-of-bias tables
figures/   forest plots, PRISMA evidence map, RoB summary, GRADE table, reproduction check
briefs/    Stream A synthesis brief + anchor reproduction brief + dual-review RoB brief
tools/     dual-reviewer-rob + grade-hybrid harness source (cross-model RoB & GRADE)
```

### Hardened risk-of-bias & GRADE layer
The observational risk-of-bias and GRADE-judgment assessments were re-run with a
two-model harness (Claude + GPT-5.5, judge-adjudicated, full audit trail):
- `results/risk_of_bias_observational_dualreview.csv` — resolved ROBINS-I ratings
- `results/rob_audit_trail.csv` — every study × domain × reviewer judgment + verbatim quotes
- `results/rob_escalation_queue.csv` — disagreements tiered for human review (0 priority gaps)
- `results/grade_certainty_hybrid.csv` — hybrid GRADE Summary of Findings
- `results/grade_judgment_audit.csv` — cross-model judgment-domain trail
- `briefs/rob_dualreview_brief.md` — narrative of the dual-review hardening
- `tools/dual-reviewer-rob/`, `tools/grade-hybrid/` — the harness source

### Key files
- `data/screening_ledger.csv` — every record (n=794): source, IDs, include/exclude + reason,
  design tag, screening method (LLM vs rule-based). Full audit trail.
- `data/study_table.csv` — master table: 25 RCTs + 36 observational studies with design, N,
  comparator, outcome, effect estimate + CI, risk-of-bias rating.
- `results/pooled_estimates.csv` — design-stratified pooled estimates (never pooled across designs).
- `briefs/stream_A_synthesis_brief.md` — full narrative, ranked confounders, mechanistic verdict.

## Methods notes

- **Strata never pooled together.** RCT stratum: Mantel-Haenszel random-effects RR on 2×2 counts.
  Observational stratum: inverse-variance random-effects on adjusted log-effects (DerSimonian-Laird).
- **Screening** combined an LLM rubric (418 records) with a transparent rule-based keyword classifier
  (376 records); the method is flagged per record in the ledger.
- **Risk of bias / GRADE in this snapshot are a rules-based first pass** (RoB2 all "some concerns";
  ROBINS-I rated primarily from confounding-control characteristics). A full-text, dual-reviewer
  (cross-model) RoB assessment is the planned hardening step; ratings here are provisional.
- Two extraction errors were caught and corrected in QC: PMID 40010803 (adjusted HR 1.02, not crude
  2.08) and PMID 40897378 (0.56 was all-cause mortality, excluded from pooling).

## Not included

Publisher full-text articles are **not** committed (copyright). The screening ledger and study table
carry the identifiers (PMID/DOI) needed to retrieve them.

---
*Generated with Claude Science. Reproduction anchor: Chen et al., J Diabetes 2025;17(9):e70151.*
