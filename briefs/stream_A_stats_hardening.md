# Stream A — Statistical methods hardening

Rerun/robustness on the existing verified dataset (61 studies: 25 RCT + 36 observational,
15 poolable). No re-search, no re-extraction. Streams kept separate; only Stream A touched.

---

## 1. Rare-event RCT rerun (suicidal-behaviour composite)

**Stratum facts.** 25 trials with 2×2 counts. Total events **35 exposed / 36 control** across
~42,000 vs ~39,000 participants — extremely sparse. **2 double-zero trials** (Ishii 2020,
Tamborlane 2022) carry zero events in both arms and contribute nothing to any relative effect;
k=23 informative. Arm-size imbalance ≥2:1 in 8 informative trials (Ahrén, Zinman, DeFronzo,
Arslanian, Seino 2012b, Umpierrez, Kaku 2019, Carydias 2022) flagged as Peto-questionable; the two
double-zero trials (Ishii, Tamborlane) are also ≥2:1 but carry no events so the Peto concern is
moot for them.

**Sensitivity panel — all methods on the same 23 informative trials:**

| Method | Estimate | 95% CI | I² |
|---|---|---|---|
| **MH RR, FE, no continuity correction (PRIMARY)** | **0.868** | 0.549–1.373 | 0% |
| MH RR, random-effects (DL) | 0.844 | 0.541–1.317 | 0% |
| MH OR, FE, no continuity correction | 0.868 | 0.546–1.382 | 0% |
| MH OR, random-effects (DL) | 0.844 | 0.540–1.318 | 0% |
| Peto OR, FE | 0.865 | 0.540–1.385 | 0% |
| Fixed-effect logistic (study fixed effects) | 0.865 | 0.540–1.385 | — |
| GLMM binomial-normal (random study intercept) | 0.845 | 0.608–1.174 | — |
| IV OR, treatment-arm 0.5 CC (sensitivity) | 0.844 | 0.540–1.318 | 0% |

**Continuity correction:** MH, Peto, logistic and the GLMM all handle zero cells natively — **no
correction applied**. The 0.5-CC row is shown only to demonstrate that adding a correction changes
nothing (0.844 vs 0.868). The exact conditional-likelihood model was infeasible (the recursion
overflows on the ~8,800-patient trials); the study-fixed-effect logistic is its asymptotic
equivalent and is reported with that caveat.

**Anchor check:** primary MH-RR 0.868 (0.549–1.373) sits directly on Chen 2025 RR 0.84
(0.54–1.32). Pipeline reproduces the anchor within CI. ✔

**What changed vs the original single pool:** the original reported one M-H number (0.844, k=23).
It is confirmed and now flanked by 7 other methods spanning **0.84–0.87**, all with CIs crossing 1
and I²=0%. The estimate is robust to method choice; the width is driven by 71 total events, not by
between-method disagreement.

---

## 2. Few-study observational rerun

Re-pooled each outcome with REML **and** Paule-Mandel τ², Hartung-Knapp CI, prediction intervals
(k≥3 only), leave-one-out and per-study estimates (`obs_reml_hk_reruns.csv`,
`obs_leave_one_out.csv`, `obs_study_level_estimates.csv`).

| Outcome | k | REML pooled | DL CI | HK CI | Prediction interval |
|---|---|---|---|---|---|
| Suicidal ideation | 3 | 0.74 | 0.40–1.37 | 0.21–2.59 | 0.00–1110 (uninformative) |
| Suicidality composite | 2 | 0.94 | 0.82–1.09 | 0.37–2.41 | n/a (k<3) |
| Suicide attempt/self-harm | 4 | 0.71 | 0.58–0.86 | 0.51–0.98 | 0.45–1.10 |
| Completed suicide | 1 | 1.25 | 0.83–1.88 | — | n/a (single study) |
| Depression | 3 | 1.53 | 0.80–2.93 | 0.37–6.37 | 0.00–6920 (uninformative) |
| Anxiety | 2 | 0.54 | 0.33–0.87 | 0.02–11.98 | n/a (k<3) |

**Key robustness signals.** τ² is nearly identical under REML and PM everywhere. **Hartung-Knapp
widens every CI dramatically** and, for suicide attempt/self-harm, pulls the upper bound to 0.98 —
i.e. the one "significant" protective observational pool is barely significant once small-k
uncertainty is honoured. Prediction intervals for the two k≥3 heterogeneous outcomes (ideation,
depression) are so wide as to be uninterpretable, which is itself the finding: with 3 discordant
studies you cannot predict a new study's result. **Leave-one-out:** suicide attempt/self-harm and
anxiety stay significant (and same-sign) on every drop; suicidal ideation and depression stay
**non-significant on every drop** — never crossing into significance — but their point estimate and
CI swing widely by which study is removed (ideation 0.57→1.02; depression 1.10→1.87), which is the
fragility here, not a significance flip.

---

## 3. Depression reframe (see `depression_reframe.md`)

Three estimates: all-study **1.53 (I²=99.8%)**; excl-outlier (PMID 39424950, HR 2.95)
**1.10 (0.95–1.28) but I²=91.8%**. **Heterogeneity stays ~92% after the exclusion**, the exclusion
was **not prespecified**, and the two surviving studies disagree (HR 1.19 elevated vs RR 1.02
null). Correct conclusion: **highly inconsistent, not meaningfully summarised by one pooled
effect** — explicitly **not** "null-to-protective". Metric check: 14/15 poolable rows are HR/aHR,
one is RR (PMID 38852027); for rare suicidality HR≈RR≈OR so pooling is defensible, but for
**non-rare depression/anxiety** mixing HR and RR is a second, independent reason not to report a
single number.

---

## 4. Absolute risk, harm margin, power, cohort overlap (`results/*.csv`)

**Absolute risk (RCT, the only stratum with counts):** exposed **8.33/10,000**, control
**9.19/10,000**, ARD **−0.86/10,000 (95% CI −4.94 to +3.22)** — crosses zero. Observational
absolute risks cannot be computed (no shared baseline); illustrative projections onto the RCT
baseline are labelled as such.

**Clinically important harm margin (RR 1.20 / 1.25):** for the RCT primary and for depression,
completed suicide, and suicidal ideation, the **upper CI does NOT exclude the harm margin** — these
analyses **cannot rule out a clinically important increase**. Only suicidality-composite, suicide
attempt/self-harm, and anxiety have upper CIs below 1.20.

**Detectable effect:** with 71 RCT events the trials are powered only to detect an RR ≥ ~1.9 at 80%
power. The RCT null is therefore **"no increase detected in an underpowered dataset," not
"equivalence."** These are different claims and are reported as such.

**Cohort overlap:** matrix over database/country/indication/molecule/comparator/outcome
(`cohort_overlap_matrix.csv`). No two studies on the **same outcome** share a documented
database+country, so no pool double-counts a population. The one shared-source cluster is the
TriNetX-type US EHR studies (39424950, 38182782, 41334076, 42373755) — but they sit in **different
outcome pools**, so they never co-contribute to a single estimate. One estimate per overlapping
population is preserved (`cohort_overlap_selection.csv`).

---

## One-line honest verdict per outcome

- **RCT suicidal-behaviour composite:** RR ≈ 0.85 (0.55–1.37), method-robust, but underpowered
  (71 events) — **no increase detected; cannot exclude RR up to ~1.37/harm margin 1.20.**
- **Obs suicidal ideation (k=3):** direction inconsistent, HK CI 0.21–2.59, flips on LOO —
  **uninformative.**
- **Obs suicidality composite (k=2):** 0.94, tight under DL but HK 0.37–2.41 — **compatible with
  no effect; small-k fragile.**
- **Obs suicide attempt/self-harm (k=4):** 0.71, lowest heterogeneity, but HK upper bound 0.98 —
  **suggestive of lower risk, only marginally significant once k is honoured.**
- **Obs completed suicide (k=1):** 1.25 (0.83–1.88) single study — **cannot rule out harm;
  not poolable.**
- **Obs depression (k=3):** **highly inconsistent (I²≈92–100%); not summarisable by one number** —
  not null-to-protective.
- **Obs anxiety (k=2):** 0.54 point estimate but HK 0.02–11.98 and flips on LOO — **direction
  suggestive of lower risk but statistically unreliable at k=2.**
