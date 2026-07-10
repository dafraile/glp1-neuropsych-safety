# Depression outcome — reframe (Stream A, observational)

## The three estimates on the table

| Analysis | k | Pooled | 95% CI | I² |
|---|---|---|---|---|
| All studies | 3 | **1.53** | 0.74–3.16 (DL) / 0.80–2.93 (REML) | **99.8%** |
| Excluding outlier PMID 39424950 (HR 2.95) | 2 | **1.10** | 0.95–1.28 | **91.8%** |
| The outlier itself | 1 | 2.95 | 2.82–3.08 | — |

## What the numbers actually say

**Heterogeneity remains ~92% even after excluding the outlier.** Dropping PMID 39424950
moves the point estimate from 1.53 to 1.10, but I² only falls from 99.8% to 91.8%. The two
"agreeing" studies do not agree: PMID 41592697 reports **HR 1.19 (1.11–1.28)** — a clearly
elevated, tightly-bounded increase — while PMID 38852027 reports **RR 1.02 (0.97–1.07)** — a
clearly null, tightly-bounded result. Their confidence intervals barely overlap. A pooled 1.10
is a mathematical average of two incompatible, individually-precise estimates, not a summary of
a coherent effect.

**The outlier exclusion was not prespecified.** Removing PMID 39424950 was a post-hoc decision
driven by its influence, not a protocol rule. Post-hoc outlier removal that changes the headline
conclusion is exactly the kind of analytic degree-of-freedom a methodologist flags. It is
reported here as a sensitivity analysis, not as the primary estimate.

**Correct conclusion:** the depression evidence in Stream A is **highly inconsistent and not
meaningfully summarised by a single pooled effect.** With I² ≈ 92–100% and component estimates
running from RR 1.02 to HR 2.95, no single number — neither 1.53 nor 1.10 — represents the body
of evidence. It is specifically **NOT** correct to describe the excl-outlier 1.10 (0.95–1.28) as
"null-to-protective"; that reading (a) launders a post-hoc exclusion into the headline and (b)
ignores that one of the two surviving studies (HR 1.19) is itself significantly elevated.

## HR / OR / RR interchangeability check (the metric problem)

Across the whole observational stratum, effect_type is HR/aHR for 14 of 15 poolable rows and RR
for exactly one — **PMID 38852027 (depression, RR 1.02)**. They were pooled as interchangeable
log-ratios. This is worth stating explicitly:

- **For rare suicidality outcomes** (attempt/self-harm, completed suicide, ideation), HR ≈ RR ≈ OR
  because the outcome is rare; treating them as one log-ratio metric introduces negligible bias.
- **For depression and anxiety — NON-rare outcomes — this is more questionable.** When the
  cumulative incidence is high, a hazard ratio and a risk ratio diverge (HR is further from 1 than
  RR for a harmful exposure; the two answer different questions — instantaneous rate vs cumulative
  risk over the window). The depression pool mixes an HR (1.19), an HR (2.95), and an RR (1.02) as
  if they were the same quantity. They are not. This metric mismatch is a *second*, independent
  reason — on top of the ~92% statistical heterogeneity — not to report a single pooled depression
  effect.
- **Anxiety** (k=2) is HR + HR, so the metric is at least internally consistent, but I² ≈ 74% and
  k<3 (no interpretable prediction interval) still make a single pooled anxiety effect fragile; it
  flips on leave-one-out (0.41 vs 0.67 individually).

**Bottom line:** the depression signal should be presented as its component estimates
(HR 1.19; HR 2.95; RR 1.02), described as highly inconsistent, with the pooled numbers shown only
to demonstrate their own instability — not summarised as a single protective or null effect.
