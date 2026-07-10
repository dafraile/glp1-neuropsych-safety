# Frozen protocol — GLP-1 RA neuropsychiatric safety triangulation

This file pins every choice needed to reproduce the analysis. It is frozen: changing
any pinned value below requires regenerating `analysis_manifest.json` (`./reproduce.sh`)
and re-checking the headline numbers.

## 1. Data snapshots (pinned)

| Source | Snapshot / cutoff | How pinned |
|---|---|---|
| openFDA FAERS | `last_updated = 2026-04-28` | recorded in every FAERS output CSV (`snapshot` column) |
| FAERS adjudication corpus | 912 semaglutide × SMQ suicide/self-injury reports, received 2018Q3–2026Q1 | `results/faers_case_adjudication_full912.csv` |
| PubMed/OpenAlex (Stream A) | as-executed; 967 retrieved → 794 deduplicated | `data/search_raw.csv`, `data/dedup_pool.csv` |
| PubMed (Stream D) | as-executed; 246 retrieved | `data/stream_D_search_raw.csv` |
| OMOP/Ryan reference set | `OHDSI/MethodEvaluation` `omopReferenceSet.rda` (399 pairs) | `data/omop_reference_set.csv` (committed copy) |

openFDA accrues reports over time, so RORs drift; the `2026-04-28` snapshot is the
reference. Re-running FAERS analyses against a later snapshot will shift absolute counts
but the design (comparator grid, time-split, controls) is snapshot-independent.

## 2. Outcome definitions (pinned)

- **Harm outcome (Stream A & B):** MedDRA SMQ "Suicide/self-injury" (narrow). The exact
  Preferred-Term list used in FAERS is locked in `results/faers_smq_terms_locked.csv`.
  openFDA does **not** expose a MedDRA version in the public API; the PT strings are the
  contract.
- **Standardized categories:** suicidal ideation / suicide attempt–self-harm / completed
  suicide / intentional self-injury / depression / anxiety.
- **OMOP calibration outcomes (Layer 5):** acute liver failure, acute MI, acute renal
  failure, upper-GI bleed → MedDRA PT sets in `results/omop_outcome_pt_map.csv`.

## 3. Drug definitions (pinned)

- Exposure molecules and their generic/brand token maps: `tools/faers/faers_tool.py`
  (`DRUGS` dict). Stream B primary scope is **semaglutide only**.
- Comparator sets (Stream B grid): T2D — SGLT2i, DPP-4i, sulfonylurea, metformin, TZD,
  insulin; obesity — orlistat, naltrexone-bupropion, phentermine; within-class — other
  GLP-1 RAs; unmatched — full database. All enumerated in
  `results/faers_comparator_grid.csv`.

## 4. Statistical methods (pinned)

- **Strata are never pooled across designs or streams.**
- RCT stratum: Mantel–Haenszel on 2×2 counts, **no continuity correction** (primary);
  Peto OR, fixed-effect logistic, binomial-normal GLMM, and 0.5-CC as sensitivity. Double-
  zero trials contribute exposure but not the relative effect. (`rct_rare_event_sensitivity.csv`)
- Observational stratum: inverse-variance random-effects on adjusted log-effects;
  τ² via REML and Paule–Mandel; Hartung–Knapp CIs; prediction intervals (k≥3); leave-one-out.
  (`obs_reml_hk_reruns.csv`, `obs_leave_one_out.csv`)
- Harm margin: RR 1.20 and 1.25, prespecified; test = does the upper 95% CI exclude it.
- Disproportionality: PRR/ROR/IC with the tool's built-in CIs; signal at Evans default
  (PRR≥2, χ²≥4, a≥3). Calibration metric = AUROC on IC025 ranking.
- Notoriety: interruption at **July 2023** (prespecified; Jan/Oct 2023 as sensitivity);
  proportion denominator = outcome reports / all-drug reports per quarter; DiD vs other
  GLP-1 RAs; control outcomes + control drugs.

## 5. LLM steps (pinned model/prompt versions)

Recorded in `analysis_manifest.json` → `llm_steps`:
- Screening: Claude Science default + rule-based classifier (method flagged per record).
- Extraction: Claude Science default; two-model re-check = claude-sonnet-5 + claude-opus-4-8.
- FAERS adjudication: claude-haiku (production) + claude-sonnet-5 + gpt-5.5; consensus = majority vote.
- RoB / GRADE: dual-reviewer-rob harness (claude-sonnet-5 + gpt-5.5), judge-adjudicated.

## 6. Analysis status (provisional / complete / superseded)

Authoritative in `analysis_manifest.json` → `analysis_status`. Superseded artifacts are
retained for provenance: `grade_certainty.csv` (→ hybrid), rules-based RoB first pass
(→ dual-review), `faers_case_adjudication_partial800.csv` (→ full912; removed from tree).

## 7. One-command reproducibility test

```bash
./reproduce.sh          # or: make reproduce
```

Regenerates `analysis_manifest.json` from the committed data files, verifies all backing-
file SHA256 hashes, and checks that README.md / TRIANGULATION_SYNTHESIS.md headline
numbers are consistent with the manifest. Exits non-zero on any drift. This reproduces the
**provenance chain** (data → manifest → prose); it does not re-hit openFDA or re-run LLM
layers (those need the pinned snapshot + API access — see §1 and §5).

## 8. Human validation status

Single reviewer. Blinded disagreement-adjudication packets are in `packets/` (one per LLM
layer, plus `adjudication_key.csv`). Until resolved, all LLM-layer agreement figures are
**cross-model reproducibility ceilings, not accuracy**; accuracy cells in
`results/validation_summary.csv` carry `human_status = awaiting_adjudication`.
