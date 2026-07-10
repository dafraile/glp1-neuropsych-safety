# Task 1 — De-duplication + drug-role sensitivity (Stream B FAERS)

**Primary analysis scope:** semaglutide (single molecule) × MedDRA SMQ Suicide/self-injury (narrow PT set).
**openFDA snapshot (PINNED):** 2026-04-28 (`meta.last_updated`).
**API key:** NONE available this run — no handoff file (`handoff/openfda_key.json` absent), no `OPENFDA_API_KEY` env var, no stored openFDA credential. Ran keyless (≤1000 req/day/IP) with one process + aggressive `_CACHE` reuse. This does not affect result values, only throughput. **Flag for re-run: supply the key to raise the limit if larger sweeps are needed.**

## Sanity anchors — ALL reproduced
| spec | expected | observed |
|---|---|---|
| all-dates comparator ROR (vs SGLT2i+DPP-4i) | ~2.08 (1.91–2.26) | **2.075 (1.906–2.258)**, a=912 |
| pre-Jul-2023 | ~0.85 | **0.848 (0.702–1.025)**, a=120 |
| post-Jul-2023 | ~2.98 | **2.976 (2.609–3.394)**, a=792 |

Pipeline validated. a=912 matches the adjudication set exactly.

## De-duplication
openFDA returns **one row per `safetyreportid`, already the latest version** — it does not serve superseded versions. Therefore **case-level count = report-version-level count = 912**; there is no separate "collapse older versions" step to perform on the returned data. `safetyreportversion` IS exposed (range 1–18; 746/912 are v1) and confirms each returned row is a single current version. There were **0** `safetyreportid` collisions in the pull.

What de-dup IS possible on the returned data:
- **Self-declared duplicate flag** (`duplicate=1`): 251/912 records.
- **`reportduplicate` block** (`duplicatesource` + `duplicatenumb`, cross-source linkage): 252 records carry it; 40 `duplicatenumb` values are shared by ≥2 records within the 912 (102 "extra" linked rows — but these are legitimately distinct safety reports that manufacturers cross-reference, not identical resubmissions).
- **`companynumb` (manufacturer control number):** 494 unique non-null, 404 null. Collapsing exact `companynumb` matches (null → own `safetyreportid`) yields **898 case families** (14 near-duplicate rows collapsed).

**Dedup impact on the anchor:** replacing the numerator a=912 → 898 moves the comparator ROR from **2.075 (1.906–2.258)** to **2.043 (1.876–2.224)** — a 0.032 shift, well within the CI. The conclusion (signal present) is unchanged. The 912 count is retained as primary (matches published adjudication set); 898 reported as the conservative de-duplicated alternative.

## Drug-role sensitivity (primary comparator: semaglutide × suicide vs SGLT2i+DPP-4i)
Role filter applied consistently to BOTH the drug and the comparator background.

| drug role | a | ROR (95% CI) | signal |
|---|---|---|---|
| primary-suspect only (`drugcharacterization:1`) | 908 | **2.090 (1.920–2.275)** | yes |
| all-suspect (1 or 2) | 909 | **2.078 (1.909–2.262)** | yes |
| all-mentioned (any role) | 912 | **2.075 (1.906–2.258)** | yes |

**ROR range across roles: 2.075–2.090.** The signal is essentially role-invariant — 908/912 reports already list semaglutide as primary suspect, so relaxing the role definition adds almost nothing. No spec flips.

## MedDRA version lock
openFDA's public drug/event API **does not expose or version MedDRA**. We therefore lock the analysis by the **verbatim PT string list** (`patient.reaction.reactionmeddrapt.exact`), saved to `faers_smq_terms_locked.csv` (13 narrow Suicide/self-injury PTs). Reproducibility depends on these exact strings, not a MedDRA version number.

## Generic/brand mapping validation (semaglutide)
`generic:["semaglutide"]`, `brands:[Ozempic, Wegovy, Rybelsus]`. openFDA `generic_name` normalization captures **all** brand reports: brand-name reports NOT covered by the generic search = **0**. Generic search = 82,911 reports; Ozempic 62,885 / Wegovy 19,958 / Rybelsus 6,782. Mapping validated — the generic token alone is sufficient and correct.

## Outputs
- `faers_drug_role_sensitivity.csv`
- `faers_smq_terms_locked.csv`
- `faers_dedup_analysis.csv`
