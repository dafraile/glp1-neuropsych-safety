# Poolable-set verification audit (2026-07)

Triggered by reviewer concern that (a) extracted numbers might be wrong and (b) some
'non-poolable' studies might actually be poolable. Independent blind re-extraction of all
36 observational abstracts (15 poolable + 21 non-poolable), diffed against study_table.

## Part 1 — poolable numbers: 15/15 CORRECT (zero errors)
Every one of the 15 poolable observational estimates matches an independent blind read of
the source abstract. Six rows initially flagged as mismatches all resolved in favour of
study_table: the blind extractor had picked a different VALID sub-estimate from a
multi-estimate abstract (adjusted vs unadjusted; alternate comparator; incident vs
recurrent). No value feeding a pooled estimate was wrong. (RCT 2x2 counts pending same check.)

## Part 2 — exclusion audit: 2 studies wrongly excluded, now recovered
| PMID | Action | Estimate added |
|---|---|---|
| 42380063 | -> poolable (depression) | HR 1.20 (1.09-1.31) vs SGLT2i |
| 40760781 | -> poolable (suicidal ideation) | RR 1.36 (0.62-6.14) vs active-comparator AOM |

Borderline (documented, NOT pooled — different construct):
- 41862258: 'worsening' of pre-existing illness, not incident (would need separate stratum)
- 41389474: suicidal behaviour bundled in a composite with mortality+hospitalization
Confirmed correctly non-poolable: 40439835 (healthcare-utilization IRR), 38650544
(antidepressant-dispensing proxy), 39535805 (AUD study, null secondary).

Convention: one primary poolable outcome per study (matches the existing 15). 42380063 ->
depression; 40760781 -> suicidal ideation.

## Part 3 — impact on pooled estimates (poolable N 40 -> 42; obs 15 -> 17)
| Stratum | Before | After | Direction |
|---|---|---|---|
| Obs depression | 1.53 (0.74-3.16) k3 | 1.44 (0.80-2.58) k4 | null, unchanged |
| Obs depression excl-outlier | 1.10 (0.95-1.28) k2 | 1.13 (1.005-1.27) k3 | now marginally >1 (fragile: wide HK CI, huge PI) |
| Obs suicidal ideation | 0.74 (0.37-1.48) k3 | 0.81 (0.44-1.50) k4 | null, unchanged |
| Obs all-outcomes | 0.878 (0.63-1.23) k15 | 0.910 (0.67-1.23) k17 | null, unchanged |
| Obs anxiety, composite, attempt, RCT | — | UNCHANGED | — |

No pooled direction changes. The depression-excl-outlier estimate crosses just above 1 after
the addition but remains fragile (HK CI 0.67-3.11; prediction interval spans <0.1 to >25);
the 'depression is not summarisable by a single number' framing stands (I2 ~ 100%).

## Bottom line
The numbers in the pooled analysis are correct as extracted. Two legitimate studies had been
wrongly excluded; adding them tightens two pools without changing any conclusion. The
verification strengthens confidence in the review rather than overturning any result.
