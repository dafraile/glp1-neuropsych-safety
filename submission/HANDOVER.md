# Handover — submission state, assets, and the one open gap

*Prepared for: the presenter building the website-as-slides + the coding agent finishing the repo.
Repo HEAD at handover: `ad6bd95` (submission-hardening commit). Everything in §1–§3 below is done
and pushed; §4 is the single remaining scientific gap.*

---

## 1. What state the repo is in

**Submission-ready.** The core science was already hardened in earlier commits (calibrated
language, harm-margin test, falsification doc, strict never-pool discipline, anchor reproduction).
This session closed the reviewer's remaining items:

| Reviewer item | Status | Where |
|---|---|---|
| RoB escalation backlog (6 pending) | ✅ resolved before this session (20/20) | `results/rob_escalation_queue.csv` |
| Stale `prior_work_positioning.md` (0.995/1.00) | ✅ fixed → 0.76 / 0.77 | commit `ad6bd95` |
| Stale `faers_calibration_report.md` (n=40, 0.995) | ✅ marked SUPERSEDED smoke test | `docs/faers_calibration_report.md` |
| Stale `VALIDATION_PROTOCOL.md` (two-rater, 87%) | ✅ fixed → single-reviewer + DiD | `VALIDATION_PROTOCOL.md` |
| `reproduce.sh` calls `python` (fails) | ✅ → `python3`, runs clean | `reproduce.sh` |
| Extraction numeric fidelity buried | ✅ surfaced (0.18/0.55) in README | `README.md` §validation |
| E-values on observational estimates | ✅ **added** | `results/obs_evalues.csv`, addendum |
| Small-study test on RCT stratum | ✅ **added** (Peters 0.50, Harbord 0.32) | `results/rct_small_study_test.csv`, `figures/rct_funnel_contour.png` |
| Registry trial-stratified pool | ❌ **still open** — see §4 | — |

`./reproduce.sh` passes end-to-end (manifest rebuild → 35 hash checks → README consistency).

## 2. The two new sensitivity analyses (added this session)

**E-values** (`docs/sensitivity_analyses_addendum.md`, `results/obs_evalues.csv`): the two
significant *protective* observational signals are fragile — self-harm 0.71 needs only an
unmeasured confounder of RR≈1.56 to explain away, anxiety 0.54 needs RR≈1.57. This applies the
same skepticism to "protective" observational reads as to harmful ones, and directly answers the
"healthy-user / confounding-by-indication" objection a reviewer will raise.

**RCT small-study test** (`figures/rct_funnel_contour.png`): Peters p=0.50, Harbord p=0.32,
symmetric contour funnel on the k=23 / 71-event stratum. We used Peters/Harbord (valid for sparse
binary data), **not** Egger. The GRADE publication-bias "no downgrade" is now test-backed rather
than asserted. Caveat stated: 71 events = low power, so "no asymmetry detected" ≠ "bias excluded."

## 3. Assets for the website / slides

**Use these figures (all in `figures/`), in this priority order:**

1. **`triangulation_forest.png`** — THE flagship. Designed-study points near 1.0 vs the FAERS
   red point at 2.08, on one log axis, explicitly labelled "ratios NOT pooled across streams."
   This is your slide 1 / hero image. It renders the entire thesis at a glance.
2. **`faers_notoriety_its.png`** — the load-bearing Stream B evidence: semaglutide suicide-report
   proportion spikes after July 2023 while control drugs (panel A) and control outcomes (panel B)
   stay flat. This is the figure for the "novel result" beat of the video.
3. **`omop_calibration_roc.png`** — the "we calibrated our tool, AUROC 0.76" credibility slide.
4. **`prisma_evidence_map.png`** — the PRISMA flow (967 → 794 → 61) if you want a "how we got
   here" slide.
5. **`benefit_harm_symmetry.png`** — the Stream D closer: harm signal dissolves, benefit footprint
   survives, same database.
6. **`grade_summary_of_findings.png`** — the GRADE Summary-of-Findings table as an image, if a
   judge wants the formal evidence grading.

**Supporting figures if you have room:** `forest_reproduction.png` (anchor reproduction),
`risk_of_bias_dualreview.png` (the RoB engine output), `stream_D_forest_by_substance.png`
(addiction benefit by substance class), `rct_funnel_contour.png` (the new small-study figure).

**Headline numbers to put on slides (all machine-verified in `analysis_manifest.json`):**
- RCT pool: **RR 0.84 (0.54–1.32), I²=0%, k=23, 71 events**
- FAERS comparator swing: **0.51 (vs metformin) → 3.29 (vs other GLP-1 RAs)**
- Notoriety: pre-July-2023 **0.85** → post **2.98** (fixed comparator); DiD **p<0.001**
- Tool calibration: **AUROC 0.76** (355/399 OMOP pairs)
- Evidence base: **967 retrieved → 794 dedup → 61 designed studies**
- External concordance: FDA meta-analysis **~91 trials / ~108k patients** — same direction

**Text sources for slide copy:** `submission/SUBMISSION_README.md` (motivation, design, findings,
deliverables) and `TRIANGULATION_SYNTHESIS.md` (the integrated reading). Don't re-derive numbers —
copy them from the manifest or these docs so the website stays consistent with the repo.

**A note on framing for the website (do this, it's the reviewer's #5 point):** lead with Stream B
(the comparator/calendar dissection) and the calibrated tooling as the *novel* contribution.
Stream A's pooled null *corroborates* the FDA's larger meta-analysis; it does not supersede it.
Distributing weight as if all four streams were equal independent proofs is the one framing error
to avoid — "convergence means consistent direction, not four proofs."

## 4. The one open scientific gap (for the coding agent)

**Build a proper trial-stratified pool of the ClinicalTrials.gov registry arm.** This is the
highest-value analysis still missing, and the data is already extracted.

- **Why it matters:** the k=23 RCT stratum *is* the Chen 2025 anchor re-run (RCT rows in
  `data/study_table.csv` have blank PMIDs, `molecule=mixed`, DOI = the anchor). So Stream A's RCT
  arm *corroborates* the anchor rather than independently confirming it. The genuinely independent
  designed-study dataset is the **registry AE arm** — `results/ctgov_ae_table.csv` (253 rows,
  ~59 NCTs, molecule + indication resolvable per trial) — but it's currently collapsed to a crude
  summed 2×2 (76/78,277 vs 55/48,828, RR≈0.86) in `results/ctgov_ae_summary.csv`. Naive summation
  across trials of wildly different size and baseline rate is a Simpson's-paradox hazard.
- **What to do:**
  1. Run a **Mantel–Haenszel / Peto** pool on the per-NCT 2×2s (same methods as the RCT stratum),
     not a summed 2×2.
  2. **Deduplicate** registry NCTs against the anchor trial list, and report the **registry-unique**
     trials as the real independent designed-study estimate.
  3. **Stratify by molecule** (semaglutide / liraglutide / dulaglutide / tirzepatide) — the
     registry arm carries molecule per NCT, so this yields a *designed-study* estimate for
     semaglutide specifically, which is the exact molecule Stream B flags. Right now there is no
     designed-study number for semaglutide alone.
  4. Add a **RoB caveat**: these are registry results-section data, not RoB-assessed full texts —
     don't let them enter at the same weight as assessed trials. Either run the dual-reviewer-rob
     engine on them or label them explicitly as "registry data, not RoB-assessed."
- **Status flag already set:** `analysis_manifest.json → analysis_status.registry_stratified_pool
  = "not_done"`, and `docs/prior_work_positioning.md` now carries the caveat. Flip the status to
  `complete` when done.

### Lower-priority, if time permits
- **Effect-measure mixing sensitivity:** HR/OR/RR are currently pooled as interchangeable
  log-ratios. For the non-rare outcomes (depression/anxiety) convert OR/HR→RR via baseline risk
  and re-pool as a one-line sensitivity — closes a flagged-but-untested gap.

## 5. Things NOT to "fix" (deliberate design choices)
- **Single-reviewer human validation** — hackathon constraint, now stated honestly everywhere.
  Not a bug.
- **PubMed + OpenAlex only** — stated as the reason we have 23 vs the FDA's 91 trials. Adding
  Embase/CENTRAL is out of scope for a hackathon.
- **The n=40 FAERS smoke test** — kept on purpose (marked superseded) because it surfaces two
  useful failure modes. Don't delete it; the pointer to OMOP 0.76 is what matters.
