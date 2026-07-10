# ClinicalTrials.gov adverse-event arm — closing the rare-event gap

**Motivation.** Step 4 showed the honest limitation of a PubMed/OpenAlex
abstract search: the large GLP-1 cardiovascular-outcome trials (SELECT, REWIND,
Harmony, EXSCEL, ELIXA, PIONEER 6) are undiscoverable by abstract terms because
suicidality is a rare buried adverse event, not an abstract topic. Trial
registries carry those counts in structured safety tables regardless of
publication. This arm queries them directly.

## What was retrieved
- **483 GLP-1 RA trials with posted results** on ClinicalTrials.gov (API v2),
  across all 7 marketed molecules.
- **194 trials** report ≥1 psychiatric adverse-event term (depression, anxiety,
  suicidality, mood).
- **59 trials** report suicide/self-injury adverse events specifically —
  including **completed suicides** — the rarest, most safety-critical events,
  the majority of which never appear in the trials' publication abstracts.

## Result: registry data independently reproduce the RCT null

Aggregating arm-level suicide/self-injury AE counts (crude, across-trial):

| Arm | Suicide/self-injury events | At risk | Rate / 10,000 |
|---|---|---|---|
| GLP-1 RA | 76 | 78,277 | 9.71 |
| Comparator | 55 | 48,828 | 11.26 |

**Crude pooled RR = 0.86 (95% CI 0.61–1.22).**

This lands almost exactly on the Stream A RCT anchor (Chen 2025: **0.84,
0.54–1.32**) — and it is **independent evidence from a source the literature
search could not reach**.

**Completed/suspected suicide (rare-event subset), stated honestly.** 16 GLP-1 vs
8 comparator events; rate-adjusted 2.04 vs 1.64/10,000, **rate ratio 1.25 (95% CI
0.53–2.91)**. The larger GLP-1 denominator (1.6×) does *not* fully explain the 2×
raw count ratio — a residual ~25% rate excess remains, **in the direction of
harm**, for this specific endpoint. It is **not statistically significant** (CI
spans 1.0 widely, 24 events total), but it is not "no excess" either, and we do
not report it as such. This is exactly the underpowered rare-event subgroup the
falsification section flags as unresolved: the any-suicide/self-injury composite
(RR 0.86) is the powered, reportable result; completed suicide alone is too rare
here to adjudicate and is carried forward as an open question, not a null.

## What this adds
1. **Directly fills the rare-event residual** flagged in Step 4 and in the
   original synthesis' caveats. The registry AE tables are the underpowered-
   subgroup gap made partly visible.
2. **Triangulates a third designed-evidence source** (registry safety data)
   onto the same null the published RCTs and observational cohorts already gave —
   convergence across *independent discovery channels*, not just independent
   studies.
3. **Addresses the Embase/CENTRAL gap** the search acknowledged: registries are a
   distinct evidence stream from bibliographic databases, and adding them
   strengthens the rare-event arm even though full Embase/CENTRAL coverage
   remains outside scope.

## Caveats (stated, not hidden)
- This is **crude arm-level aggregation across heterogeneous trials**, not a
  within-trial random-effects meta-analysis. It is a triangulation check, kept
  separate from the Stream A pooled estimate, not merged into it.
- Arm classification (GLP-1 vs comparator) is by group-title regex; mixed or
  ambiguous arms ("other", 31 rows) are excluded from the 2×2.
- Registry AE reporting is standardized but not adjudicated for causality —
  consistent with how it is used here (rate comparison, not attribution).

*Files: `ctgov_ae_table.csv` (252 per-arm suicide-AE rows, 59 trials),
`ctgov_ae_summary.csv`, `ctgov_ae_counts.png`.*
