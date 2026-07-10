# Task 2 — Comparator grid + indication interaction test (Stream B FAERS)

**Scope:** semaglutide (single molecule) × MedDRA SMQ Suicide/self-injury (narrow). **Snapshot:** 2026-04-28. **API key:** none available (ran keyless). Role = all-mentioned (matches anchor); numerator a=912 throughout the grid.

## Comparator grid — 19 specifications
`results/faers_comparator_grid.csv`. Signal = ROR 95% CI excludes 1 AND a≥3.

| comparator background | ROR (95% CI) | signal |
|---|---|---|
| **T2D active comparators** | | |
| SGLT2i | 2.636 (2.380–2.919) | ✓ |
| DPP-4i | 1.646 (1.494–1.812) | ✓ |
| SGLT2i+DPP-4i (PRIMARY/anchor) | 2.075 (1.906–2.258) | ✓ |
| sulfonylurea | 0.749 (0.691–0.812) | ✗ |
| metformin | 0.514 (0.480–0.550) | ✗ |
| TZD | 1.114 (0.994–1.249) | ✗ |
| insulin | 2.094 (1.927–2.276) | ✓ |
| all non-GLP1 antidiabetics combined | 0.838 (0.783–0.897) | ✗ |
| **Obesity comparators** | | |
| orlistat | 2.429 (2.002–2.945) | ✓ |
| naltrexone–bupropion | 0.135 (0.126–0.144) | ✗ |
| phentermine | 0.466 (0.407–0.535) | ✗ |
| obesity combined | 0.160 (0.150–0.171) | ✗ |
| **Molecule / unmatched** | | |
| other GLP-1 RAs (within-class) | 3.294 (3.016–3.597) | ✓ |
| **FULL DATABASE (UNMATCHED)** | 0.774 (0.725–0.826) | ✗ |
| **Reporting-bias restrictions (vs SGLT2i+DPP-4i)** | | |
| consumer-only | 2.761 (2.393–3.185) | ✓ |
| physician-only | 2.222 (1.902–2.596) | ✓ |
| any-HCP | 2.272 (2.033–2.540) | ✓ |
| US-only | 1.890 (1.669–2.139) | ✓ |
| 2024Q1-matched | 4.310 (2.718–6.835) | ✓ |

## STABILITY VERDICT
**The disproportionality signal is NOT stable across the comparator grid — it is comparator-dependent, and the choice of denominator determines whether a signal appears at all.** The point of this analysis is that stability, not any single spec's ROR.

- **Robust within a class of comparator (reporter type, country, quarter):** once the SGLT2i+DPP-4i comparator is fixed, the signal survives every reporting-bias restriction (consumer 2.76, physician 2.22, US 1.89, 2024Q1 4.31). So it is **not** an artifact of consumer reporting or one country.
- **Flips wildly across comparator choice:** ROR spans **0.14 (vs naltrexone–bupropion) to 3.29 (vs other GLP-1 RAs)** — a >20-fold range. It signals against SGLT2i, DPP-4i, insulin, orlistat, and other GLP-1 RAs; it does NOT signal against sulfonylurea (0.75), metformin (0.51), TZD (1.11), phentermine (0.47), naltrexone–bupropion (0.13), the combined antidiabetic set (0.84), or the **full database (0.77)**.
- **The full-DB "signal" is actually inverse (ROR<1)** — semaglutide is *under*-represented for suicide relative to the entire FAERS background, because the whole-DB background is dominated by drug classes with high psychiatric/suicidality reporting. This is a textbook demonstration that the elevated comparator ROR is **driven by the low suicidality reporting of the antidiabetic comparators (confounding by indication / channeling)**, not by an absolute excess in semaglutide.
- naltrexone–bupropion and phentermine give ROR≪1 because those obesity drugs themselves carry heavy neuropsychiatric reporting (bupropion is an antidepressant with a suicidality boxed warning) — an invalid comparator direction, not evidence of semaglutide safety.

**Bottom line:** 11/19 specs signal, but the pattern is fully explained by which comparator's baseline suicidality-reporting rate you divide by. The signal is a statement about *relative reporting* between drug classes, not an absolute safety signal — consistent with confounding by indication dominating the spontaneous-report comparison.

## Indication interaction test (replaces the 1.97 vs 1.83 point comparison)
`results/faers_indication_interaction.csv`. Both strata use the **valid full-DB background, restricted by `patient.drug.drugindication`** (the SGLT2i/DPP-4i comparator is invalid for obesity — d collapses, as the existing file shows comparator_n≈14,860 with c=7).

- Obesity stratum: ROR **2.045 (1.782–2.347)**, a=299 (reproduces the doc's obesity a=298).
- T2D stratum: ROR **1.769 (1.495–2.094)**, a=152.
- Ratio of RORs (obesity/T2D) = **1.156 (0.930–1.437)**.
- **z-test on difference of log-RORs: z=1.306, p=0.192.** Cochran Q=1.705 (df=1), p=0.192, I²=41.4%.

**Conclusion:** The obesity vs T2D difference is **NOT statistically significant (p=0.192)**. The apparent gap (obesity ROR higher) is within sampling noise given the wide CIs. The signal is **statistically indication-invariant** — there is no evidence the disproportionality differs by indication. State it as "not significantly different given wide CIs," NOT as "genuinely identical" and NOT as "higher in obesity."

## Outputs
- `faers_comparator_grid.csv`
- `faers_indication_interaction.csv`
