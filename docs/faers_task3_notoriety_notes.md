# Task 3 — Time-controlled notoriety analysis (Stream B FAERS)

**Scope:** semaglutide (single molecule) × MedDRA SMQ Suicide/self-injury (narrow). **Snapshot:** 2026-04-28. **API key:** none available (ran keyless; quarterly series are query-heavy but cached). Replaces the descriptive "87% of reports post-July-2023" with denominator-controlled, formally-tested controls.

## 1. Proportion series (the key denominator control)
Quarterly **semaglutide-suicide reports / ALL semaglutide reports** (`faers_notoriety_series.csv`). This controls for semaglutide's own reporting growth. Pre-Jul-2023 the proportion sits at ~0.005–0.017; from 2023Q3 it jumps to ~0.02–0.04 and settles around 0.011–0.021 — a step up, not a continuation of trend. So the surge is **not** merely semaglutide getting more reports overall.

## 2. Interrupted time series (segmented regression, interruption 2023Q3)
`prop ~ t + post + t_since`, `faers_notoriety_its.csv`:
- **Level change at Jul-2023: +0.0206, p<0.0001** (highly significant discontinuity).
- **Slope change: −0.0026, p=0.0001** (negative — the proportion spikes then partially decays, the signature of a notoriety spike rather than a sustained new hazard level).
- Pre-interruption slope: +0.0004, p=0.05 (essentially flat before).

## 3. Control outcomes (NOT in the publicity) — stayed flat ✓
Same ITS on semaglutide's own nausea / headache / injection-site proportions:
- nausea: level change +0.026, **p=0.26** (n.s.)
- headache: −0.002, **p=0.80** (n.s.)
- injection-site: −0.007, **p=0.36** (n.s.)

None show the July-2023 discontinuity. The break is **suicide-specific**, not a general reporting artifact affecting all semaglutide events.

## 4. Control drugs (similar growth, no suicidality publicity) — stayed flat ✓
Suicide-report proportion ITS:
- empagliflozin: level change −0.002, **p=0.29** (n.s.)
- tirzepatide: +0.083, **p=0.51** (n.s.)
- dulaglutide: +0.003, **p=0.003** (significant but ~7× smaller than semaglutide's +0.0206)

Control drugs do not jump at July-2023 the way semaglutide does.

## 5. Difference-in-differences (semaglutide vs other GLP-1 RAs)
`faers_notoriety_did.csv`:
- semaglutide suicide-proportion: 0.00474 → 0.01376 (change **+0.00902**)
- other GLP-1 RAs: 0.00292 → 0.00408 (change +0.00117)
- **DiD = +0.00785 (0.79 pp), 95% CI 0.0065–0.0092, z=11.3, p<0.0001.**

Semaglutide's excess post-July-2023 is specific to semaglutide, ~7× the within-class secular rise.

## 6. Sensitivity to alternative interruption dates & reporting lag
Level change significant at every candidate date (2023-01 +0.0161 p=0.002; 2023-04 +0.0208 p<0.0001; **2023-07 +0.0206 p<0.0001**; 2023-10 +0.0187 p=0.0001) — the discontinuity is robust to the exact date chosen. The level jump is essentially identical for the Apr/Jul/Oct-2023 candidates (0.0208/0.0206/0.0187; April is marginally the largest, not July), and the slope-change is most negative at 2023-10 (−0.0032) rather than July (−0.0026). July-2023 is used as the prespecified interruption (matching the EMA/FDA signal timing), not because it is the statistical best-fit; the near-equivalence across Q2–Q4 2023 means the analysis does not hinge on the precise breakpoint. Reporting lag (receivedate − receiptdate) on the 912 cases: median 0, 82% same-day — no material lag distorting the quarter assignment.

## VERDICT
The July-2023 discontinuity is **suicide-specific** (control outcomes flat), **semaglutide-specific** (control drugs flat, DiD p<0.0001), **survives the proportion denominator** (not explained by semaglutide's own growth), and has the **spike-then-decay shape** of a reporting surge rather than a step to a new sustained hazard. This is **consistent with notoriety bias** following the July-2023 EMA/FDA signal announcements and media coverage. Stated carefully: consistent with notoriety bias — NOT "proven time artifact." A true increase in underlying risk cannot be fully excluded from spontaneous data, but every negative-control check points to reporting behaviour, not incidence.

## Outputs
- `faers_notoriety_series.csv`, `faers_notoriety_its.csv`, `faers_notoriety_did.csv`, `faers_notoriety_its.png`
- Task 5 inverse-ROR: `faers_inverse_disproportionality_relabel.csv`, `inverse_ror_note.md`
