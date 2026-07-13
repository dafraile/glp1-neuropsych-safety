# Chen 2025 anchor reproduction — VERIFIED AGAINST SOURCE (trust check)

**Status: PASS — verified against the primary source, not merely self-consistent.**

## What this check is
The project's protocol requires reproducing a *published* GLP-1-RA/suicidality pooled
estimate from our own per-study data before trusting the extended Stream A synthesis. The
anchor is **Chen et al., J Diabetes 2025;17(9):e70151** (DOI 10.1111/1753-0407.70151,
PMID 40887719, PMC12399406, CC-BY), a meta-analysis of 25 RCTs of GLP-1 RA vs control for
suicidal behaviour.

## Two-layer verification (2026-07)
An earlier brief reported an exact reproduction, but its "Published" targets and per-study
2x2 were transcribed from the Figure 2 forest plot. A transcribe-then-pool match proves the
pooling code is self-consistent; it does NOT prove fidelity to Chen 2025. This pass adds the
missing layer.

**Layer 1 — pooling reproducibility (recomputed from committed `data/anchor_jdiabetes_2x2.csv`):**
Mantel-Haenszel random-effects (DerSimonian-Laird tau2, 0.5 continuity correction for
single-zero, double-zero dropped), 23/25 studies estimable.
- RR 0.844 (95% CI 0.541-1.317), Q=11.24, df=22, I2=0%, Z=0.747, p=0.455, tau2=0.

**Layer 2 — fidelity to the source (fetched full text from PMC, 2025):**
Every published statistic matches, and every input trial is confirmed present in the paper.

| Statistic | Chen 2025 (source) | Reproduced | Match |
|---|---|---|---|
| Pooled RR (random) | 0.84 | 0.844 | exact |
| 95% CI | 0.54-1.32 | 0.541-1.317 | exact |
| I2 | 0% | 0.0% | exact |
| p (overall) | 0.46 | 0.455 | exact |
| Total events (exp vs ctrl) | 35 vs 36 | 35 vs 36 | exact |
| N (exp vs ctrl) | 42 172 vs 39 223 | 42 172 vs 39 223 | exact |
| k pooled / df | 23 / 22 | 23 / 22 | exact |

- **Study-set fidelity:** all 25 trials in `anchor_jdiabetes_2x2.csv` (24 unique first
  authors incl. Pi-Sunyer 2015) are named in the Chen 2025 full text — zero phantom studies,
  none missing.
- **Double-zero handling matches:** Ishii 2020 and Tamborlane 2022 are double-zero and dropped
  by M-H (23 estimable), consistent with the anchor's df=22.

## Source subgroup RRs (for context; NOT re-pooled here)
Chen 2025 reports outcome-type subgroups all null, I2=0%: suicidal ideation RR 1.04,
suicide attempts 0.68, depression-related 0.65, completed suicide 1.06; and by indication
T2DM 0.74 vs obesity 1.07. These are the RCT-side analogues of our own observational pools
(different data) and are directionally consistent with Stream A.

## Verdict
The Stream A pooling machinery recovers the anchor **to reported precision on every
statistic**, from inputs confirmed faithful to the source paper. The pipeline is validated
for the extended synthesis; no divergence to flag. This closes the project's anchor trust-check
deliverable.

## Artifacts
- `data/anchor_jdiabetes_2x2.csv` — reproducible per-study 2x2 input
- `results/reproduction_check.csv` — statistic-by-statistic concordance
- `figures/forest_reproduction.png`, `figures/reproduction_check.png`
- `articles/` — Chen 2025 full text (PMC), used for Layer-2 verification
