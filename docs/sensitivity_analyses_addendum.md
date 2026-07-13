# Sensitivity analyses addendum — E-values & RCT small-study test

*Added in the submission-hardening pass. Two reviewer-expected, low-cost sensitivity
analyses that were previously absent. Neither changes any headline conclusion; both make
the existing conclusions test-backed rather than asserted.*

---

## 1. E-values on the observational estimates (confounding sensitivity)

The observational strata are all rated **Very low** GRADE, dominated by confounding by
indication (ROBINS-I D1). GRADE flags the uncertainty but does not *bound* it. The E-value
answers the standard reviewer objection directly: **how strong would an unmeasured
confounder have to be — on both the exposure and the outcome, above the measured
covariates — to explain the estimate away?**

`results/obs_evalues.csv`. E-value for the point estimate and for the confidence-interval
bound nearest the null (a CI that crosses 1 needs no confounder, so its CI-bound E-value is 1.00).

| Outcome | k | Estimate (95% CI) | Significant | E-value (point) | E-value (CI bound) |
|---|---|---|---|---|---|
| suicidal ideation | 4 | 0.81 (0.44–1.50) | no | 1.76 | 1.00 |
| suicidality (composite) | 2 | 0.94 (0.82–1.09) | no | 1.31 | 1.00 |
| suicide attempt / self-harm | 4 | **0.71 (0.58–0.87)** | yes | 2.18 | **1.56** |
| completed suicide | 1 | 1.25 (0.83–1.88) | no | 1.81 | 1.00 |
| depression (excl. TriNetX outlier) | 3 | 1.13 (1.01–1.27) | yes | 1.51 | **1.08** |
| anxiety | 2 | **0.54 (0.33–0.87)** | yes | 3.13 | **1.57** |

**Reading.** For the two significant *protective* observational signals — self-harm 0.71
and anxiety 0.54 — an unmeasured confounder associated with both GLP-1 exposure and the
outcome by a risk ratio of **≥1.56** (self-harm) or **≥1.57** (anxiety), beyond all measured
covariates, would suffice to move the CI to include the null. Healthy-user, prevalent-user,
and confounding-by-indication effects of that magnitude are entirely plausible in these
designs, so the "protective" observational readings are **not robust** and should not be
over-read as "GLP-1 protects against self-harm / anxiety." This is the same skepticism the
project applies to harm-direction signals, applied symmetrically. The one significant
harm-direction row (depression, excl. outlier) is even more fragile: a confounder of RR
≥1.08 explains it away.

*Method: E-value = RR + √(RR·(RR−1)), reflecting protective estimates to the ≥1 scale
(VanderWeele & Ding 2017). HR/OR treated as approximate RR, appropriate here because the
outcomes are rare.*

---

## 2. Small-study / publication-bias test on the RCT stratum (k=23)

Previously the GRADE publication-bias domain for the RCT stratum was set to "no downgrade"
by narrative assertion ("k=23 > threshold, nothing noted"). For k=23 that claim should be
backed by a test. It now is.

`results/rct_small_study_test.csv`, `figures/rct_funnel_contour.png`.

| Test | Statistic | p-value | Interpretation |
|---|---|---|---|
| **Peters (primary)** | slope of lnOR on 1/N (WLS) | **0.50** | No significant small-study effect |
| Harbord (secondary) | intercept of Z/√V on √V | **0.32** | No significant small-study effect |

- **k = 23 event-contributing trials, 71 total events** (2 double-zero trials — Ishii 2020,
  Tamborlane 2022 — contribute no information and are excluded, as in the primary pool).
- **Peters' and Harbord's tests were used, not Egger's on log-RR.** Egger's test is invalid
  on sparse binary data (its false-positive rate inflates when events are rare and arms are
  imbalanced); Peters' and Harbord's are the recommended small-study tests for binary
  outcomes with few events.
- The **contour-enhanced funnel** (significance contours around the null) is visually
  symmetric — points fall on both sides of the pooled center and there is no "missing"
  wedge in the non-significant region that would signal selective non-publication of null
  trials.
- The **size-adjusted (Peters intercept) estimate is OR ≈ 0.93**, close to the pooled
  M-H estimate (RR 0.84 / OR ≈ 0.87 — the two coincide to 2 dp for this rare outcome) —
  i.e. no evidence the small trials are pulling the estimate. (The headline pool is reported as
  RR 0.84 elsewhere; the Peters intercept is on the OR scale, so it is compared to the MH-OR here.)

**Caveat (stated explicitly).** With only 71 events, power to *detect* funnel asymmetry is
low, so "no asymmetry detected" is not "publication bias excluded." The GRADE non-downgrade
is now consistent with a run test rather than an unbacked assertion, but the low-power caveat
stands.

**Scope.** This test is run **only on the RCT stratum (k=23)**. For Stream D and the
observational strata (k=1–4) the existing "too few studies to test reliably (k<10)" narrative
is correct and unchanged — a funnel/Peters test at k≤4 is uninformative and was not run.

---

## What this does and does not change

- **No headline estimate changes.** The RCT pool, observational pools, and GRADE ratings
  are unchanged.
- **What improves:** the observational "protective" signals now carry an explicit,
  quantified robustness bound (they are fragile to plausible unmeasured confounding), and
  the RCT publication-bias GRADE domain is now test-backed. Both were reviewer-flagged gaps.
- **Still open (out of scope for this pass, see handover):** the trial-stratified
  Mantel–Haenszel/Peto pool of the ClinicalTrials.gov registry arm with anchor
  de-duplication and molecule stratification — the one genuinely independent designed-study
  estimate, currently only a crude summed 2×2.
