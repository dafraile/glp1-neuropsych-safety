# Indication stratification — obesity vs T2D (FAERS)

The project PICO tracks **obesity vs T2D as distinct indications**. This note records
where that stratification was and was not achievable, and the FAERS result.

## Stream A (designed studies): NOT cleanly estimable
The Stream A corpus is predominantly mixed-population: of 42 poolable studies,
**25 are tagged "T2D/obesity", 11 pure T2D, 3 obesity+T2D, and only 3 pure obesity.**
A clean obesity-only pooled estimate is not supportable from this corpus. This is a
data limitation of the trial/cohort literature (cardiovascular-outcome and diabetes
registries dominate), not an analysis choice. Reported here as an explicit limitation.

## Stream B (FAERS): estimable via the per-report indication field
openFDA carries `patient.drug.drugindication`. Stratifying semaglutide ×
suicide/self-injury (SMQ) by indication:

| Indication | Background | a | Reporting OR (95% CI) |
|---|---|---|---|
| Obesity | Full FAERS DB | 298 | 1.97 (1.72–2.26) |
| Obesity | SGLT2i/DPP-4i comparator | 298 | 1.58 (0.74–3.37) **← invalid** |
| T2D | Full FAERS DB | 251 | 1.83 (1.61–2.08) |
| T2D | SGLT2i/DPP-4i comparator | 251 | 2.24 (1.91–2.61) |

## Key methodological finding: the comparator background breaks for the obesity stratum
SGLT2i and DPP-4i are **diabetes** drugs. Within the obesity-indication stratum the
comparator denominator collapses (d = 511), producing the wide, unstable CI
(0.74–3.37, marked with an open marker in the figure). **Indication-stratified
disproportionality cannot use a diabetes-drug comparator for the obesity stratum** —
a full-DB background is required, or an obesity-matched comparator (e.g. naltrexone/
bupropion, orlistat, phentermine) if one wants an active comparator.

Under the valid full-DB background, **obesity (1.97) ≈ T2D (1.83)** — the suicide
reporting signal is *not* concentrated in one indication. (These full-DB RORs are
elevated because the full-DB background is itself not indication-matched; the
interpretable quantity is the obesity-vs-T2D **comparison**, which is flat, not the
absolute ROR.)

## Secondary Q1 addendum — baseline psychiatric history: NOT cleanly estimable
FAERS has no baseline-history field. The only available proxy is psychiatric
co-medication (antidepressant/benzodiazepine co-report), which conflates prior
history, current severity, indication, and the outcome itself (channeling). The raw
proxy split (suicide reported in 2.29% of psych-co-med reports vs 0.97% without,
a 2.4× ratio) is **confounded by design and must not be read as effect modification
by psychiatric history.** True subgroup analysis requires patient-level designed-study
data reporting the subgroup — absent from this corpus. Reported as an explicit
limitation, not a finding.

Reproduce: `results/indication_stratified.csv`, figure `figures/indication_stratified.png`.
