# Inverse-ROR relabeling — Stream D FAERS footprint (EXPLORATORY consistency check only)

**Snapshot:** 2026-04-28. **Comparator:** SGLT2i+DPP-4i. **API key:** none available (ran keyless). **Reproduces** `streamD_faers_benefit.csv` `any_addiction_composite` exactly: class-level a=222, ROR 0.368 (0.311–0.435).

This note produces corrected numbers and framing for the Stream D FAERS footprint. It does **not** edit the doc (another track owns docs) — it supplies what that track needs to make the doc consistent. Output table: `results/faers_inverse_disproportionality_relabel.csv`.

## Correction 1 — an ROR<1 is "inverse disproportionality", NOT "protective" / "benefit"
The existing `streamD_faers_benefit.csv` labels every ROR<1 row `direction=protective`. This is a **causal overclaim** and must be relabeled. In a spontaneous-report system:
- ROR<1 means the drug–event pair is **reported less often than expected relative to the comparator** — i.e. *inverse disproportionality* / *under-reporting relative to comparator*.
- It is **not** evidence of a protective or therapeutic effect. Addiction-reduction benefits cannot be reported as adverse events, so under-reporting is expected regardless of any true effect; it is equally consistent with reporting behaviour, indication differences, and channeling. Use "inverse disproportionality (ROR<1)"; never "protective" or "benefit".

## Correction 2 — class-level vs semaglutide-only scope inconsistency
The benefit table is **class-level** (all 8 GLP-1 RAs — confirmed: `any_addiction_composite` a=222 matches only the class-level pull, not semaglutide's a=71). If any reproduce snippet queries `semaglutide` alone it will NOT match the table. The doc must pick one scope and label it. Both are provided so it can be made consistent:

| substance | class-level GLP-1 (a, ROR, CI) | semaglutide-only (a, ROR, CI) |
|---|---|---|
| alcohol | 35, 0.512 (0.324–0.808) — inverse | 14, 1.085 (0.589–1.998) — **null** |
| nicotine/tobacco | 8, 0.268 (0.116–0.622) — inverse | 3, 0.533 (0.156–1.820) — **null** |
| substance/drug | 158, 0.357 (0.293–0.436) — inverse | 50, 0.568 (0.420–0.768) — inverse |
| behavioural | 25, 0.356 (0.216–0.587) — inverse | 6, 0.432 (0.183–1.015) — **null** |
| any-addiction composite | 222, 0.368 (0.311–0.435) — inverse | 71, 0.596 (0.462–0.768) — inverse |
| reward/appetite (on-target control) | 22044, 3.408 (3.292–3.528) — over-reported | 6444, 4.536 (4.363–4.715) — over-reported |
| headache (neutral control) | 12218, 1.101 (1.067–1.135) | 3568, 1.605 (1.540–1.672) |

Two rows differ from `streamD_faers_benefit.csv` on counts because of PT term-set / query-date differences, though directionally identical: (a) nicotine/tobacco was a=14 there, a=8 here; (b) CONTROL_headache was n=13407 (ROR 1.15) there, a=12218 (ROR 1.101) here (~9% count difference, same near-neutral direction). Reconcile both when aligning the doc; neither changes any conclusion.

**Scope-sensitivity finding:** at semaglutide-only scope, the alcohol, nicotine, and behavioural inverse signals **lose significance (CIs span 1)**. Only the substance/drug and overall composite remain inverse in both scopes, and even those attenuate toward the null (0.36→0.60). The class-level "benefit footprint" is therefore substantially weaker when narrowed to the primary-analysis molecule — another reason to treat it as exploratory only.

## Correction 3 — frame the WHOLE Stream D FAERS footprint as exploratory
Even the reward/appetite over-reporting (ROR>1) and the headache control (~1.1, near-neutral) confirm the pathway is *engaged* and the method behaves, but none of this is a designed-study benefit estimate. The Stream D FAERS footprint is an **exploratory consistency check** that the spontaneous-report direction is not contradicted by the designed-study benefit signal (Stream D proper) — it is not a benefit effect size and must never be pooled with, or presented as, the designed-study result.

## Outputs
- `results/faers_inverse_disproportionality_relabel.csv`
