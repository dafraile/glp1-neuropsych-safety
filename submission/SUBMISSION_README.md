# Triangulating the GLP-1 neuropsychiatric safety signal
### Hackathon submission — what we built, why, and what you can reuse

**One sentence:** We reconciled the biggest open contradiction in GLP-1 drug safety —
regulators' spontaneous-report databases scream "suicide signal" while trials and cohorts
say "no" — by rebuilding the whole evidence base as four strictly-separated streams with
error-rate-reporting, calibrated tooling, and showing *why* the spontaneous signal is an
artifact of comparator choice and calendar time rather than a real drug effect.

---

## 1. Why this matters (motivation)

GLP-1 receptor agonists (semaglutide/Ozempic/Wegovy, liraglutide, tirzepatide, …) are among
the most-prescribed drugs in the world. In 2023 the EMA and FDA opened investigations into
post-marketing reports of **suicidal ideation and self-harm**. This created a genuine
benefit–harm paradox:

- **Spontaneous-report databases (FAERS)** show a disproportionate suicide signal.
- **Randomised trials and cohort studies** largely do **not** — and sometimes suggest *lower* risk.
- The **same GLP-1R mesolimbic reward pathway** is showing early promise for *reducing*
  addiction and craving.

The question is not just "is it safe?" but **"why do the evidence sources disagree, and which
one should a regulator believe?"** That is a meta-science problem, and it is exactly the kind
of problem where careless pooling produces confidently wrong answers.

## 2. What we did (the design)

We built **four evidence streams and never pooled across them** — the single most important
methodological choice in the project:

| Stream | Question | Evidence | Role |
|---|---|---|---|
| **A** | Do *designed studies* show neuropsychiatric harm? | RCTs + observational pharmacoepi | Pooled estimate + risk-of-bias + GRADE |
| **B** | Is the *spontaneous* signal real? | FAERS / openFDA disproportionality | Comparison only — never pooled with A |
| **C** | Is harm/benefit *biologically plausible*? | Mechanistic literature | Plausibility, not effect size |
| **D** | *(Exploratory)* Does it *reduce* addiction? | Designed studies on craving/use | Quarantined from the safety question |

Each stream has its own PRISMA flow, its own study table, its own pooled estimate, and its own
GRADE certainty. The streams are compared at the end (triangulation), not merged.

## 3. The headline findings

**Stream A — designed studies do not show increased average risk.**
RCT pool (k=23, Mantel–Haenszel): **RR 0.84 (0.54–1.32), I²=0%**. Observational pools sit at
or below the null. But we state this as **"no detected increase," not "proof of safety"**: the
RCT upper CI (1.37) does *not* exclude a prespecified harm margin of RR 1.20/1.25, and with 71
events the stratum can only detect RR ≥ ~1.9 at 80% power.

**Stream B — the spontaneous signal is an artifact of *what you compare against and when*.**
This is the novel result. For semaglutide × SMQ suicide/self-injury, the reporting odds ratio
**swings from 0.51 (vs metformin) to 3.29 (vs other GLP-1 RAs)** — it crosses the no-signal
line depending only on the comparison group. Within a fixed active comparator, the signal is
**absent before July 2023 (0.85) and present after (2.98)**, a semaglutide-specific
difference-in-differences jump (p<0.001), while control outcomes (headache, injection-site
reactions) and control drugs show **no** July-2023 discontinuity. The conclusion that survives
is **instability consistent with notoriety bias + confounding by indication** — not a real
drug effect, and not a "debunk" either.

**Stream C — mechanism can't adjudicate the clinical question.** GLP-1R signalling in reward
circuitry is compatible with *reduced* craving, but proposed harm mechanisms are largely
unstudied. "No established mechanism for harm" is absence of explanatory evidence, not evidence
of safety.

**Stream D (exploratory) — a benefit footprint that survives the same scrutiny that dissolves
the harm signal.** In the *same* FAERS database, read against the *same* comparator, the harm
signal dissolves (only post-notoriety, only news-named brands) while an addiction-reduction
footprint survives across four substance classes. One database, symmetric treatment, opposite
fates.

**The honest framing:** the persuasive force comes from the **Stream B comparator/calendar
dissection** and the **calibrated tooling**, *not* from the pooled RCT number (which the FDA's
larger 91-trial meta-analysis supersedes on the average-effect question). We lead with the new
thing, not the corroboration.

## 4. Deliverables

### 4a. Research outputs
- **[`../TRIANGULATION_SYNTHESIS.md`](../TRIANGULATION_SYNTHESIS.md)** — the integrated reading across all four streams.
- **[`../README.md`](../README.md)** — full methods, headline table, external concordance, measured error rates.
- **Study table + PRISMA** (`data/study_table.csv`, `figures/prisma_evidence_map.png`): 967 records retrieved → 794 after dedup → 61 designed studies (25 RCT rows, 36 observational).
- **Pooled estimates, stratified by design** (`results/pooled_estimates.csv`) with forest plots, rare-event sensitivity, REML/Hartung-Knapp reruns, leave-one-out.
- **Risk of bias** via a dual-reviewer signalling-question engine (RoB2 + ROBINS-I), full audit trail.
- **GRADE** Summary-of-Findings via a hybrid deterministic + dual-reviewer harness.
- **FAERS analysis** (`results/faers_*`): comparator grid, time-controlled ITS/DiD, dedup/drug-role sensitivity, case adjudication.
- **Anchor reproduction** (`docs/anchor_reproduction_VERIFIED.md`): we reproduce Chen et al. 2025's pooled estimate to RR 0.84 (0.54–1.32), I²=0% — source-verified against the full text.
- **Sensitivity analyses** (`docs/sensitivity_analyses_addendum.md`): E-values on observational estimates; small-study test on the RCT stratum.

### 4b. Reusable skills & tooling (the "build track")
These travel with the project as versioned source and are usable on *any* systematic review:
- **`tools/dual-reviewer-rob/`** — a full-text risk-of-bias harness that runs the **official
  signalling questions** (RoB2: 22 Qs / 5 domains; ROBINS-I 2016: 34 Qs / 7 domains) through
  **two independent cross-model reviewers** (Claude + GPT), a judge tier for disagreements, and
  a full study×domain×question×reviewer audit trail with verbatim quote verification. Also
  published as a Claude Science skill.
- **`tools/grade-hybrid/`** — hybrid GRADE: a *deterministic* engine for the arithmetic domains
  (RoB aggregation, inconsistency from I², imprecision from CI/events/OIS) + a *dual-reviewer*
  harness for the judgment domains. Consumes the dual-reviewer-rob output.
- **`tools/faers/faers_tool.py`** — an openFDA disproportionality client that standardises
  outcomes to the MedDRA SMQ suicide/self-injury term set and computes PRR/ROR/IC against
  either the full-database background or custom active-comparator backgrounds.

### 4c. Reproducibility infrastructure
- **`analysis_manifest.json`** — machine-generated single source of truth for every headline
  number, built from the data files by `build_manifest.py`.
- **`./reproduce.sh`** — one command that regenerates the manifest, verifies 35 backing-file
  hashes, and checks that the README/synthesis prose is consistent with the manifest. (It
  reproduces the *provenance chain* data→manifest→prose, not the live openFDA/LLM analyses —
  see `FROZEN_PROTOCOL.md` for the pinned snapshot and how to re-run those.)
- **`VALIDATION_PROTOCOL.md` + `results/validation_summary.csv`** — measured pipeline error
  rates for every LLM layer.

## 5. What makes this credible (the meta-science)

- **Calibrated tooling, not asserted.** The disproportionality tool scores **AUROC 0.76** on
  the OMOP/Ryan reference set (355/399 estimable pairs) — a real, imperfect number, not a
  hand-picked 0.99.
- **We measure and report our own error rates**, including the unflattering ones (extraction
  numeric exact-match 0.18–0.55; RoB quote-verification 86%).
- **A falsification doc** (`docs/falsification_and_limits.md`) states "what would flip this"
  for every conclusion.
- **Calibrated language throughout:** "no detected increase," never "safe."

## 6. Honest limitations (stated, not hidden)

- **Human validation is single-reviewer** (hackathon constraint, by design) — the accuracy
  story is cross-model reproducibility ceilings plus one reviewer.
- **Search was PubMed + OpenAlex only** (no Embase/CENTRAL/PsycINFO/ICTRP) — which is why we
  have 23 abstract-discoverable trials and the FDA has 91. Our RCT pool corroborates rather
  than supersedes.
- **The registry adverse-event arm** is currently a crude summed 2×2 (RR 0.86); a proper
  trial-stratified Mantel–Haenszel/Peto pool is the one high-value analysis still open (see
  the handover note).

---

*Anchors: Chen et al., J Diabetes 2025 (Stream A); Eshraghi et al., eClinicalMedicine 2025
(Stream D). openFDA snapshot 2026-04-28. Generated with Claude Science.*
