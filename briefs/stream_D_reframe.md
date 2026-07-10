# Stream D — Reframe as EXPLORATORY Addiction/Reward-Benefit Analysis

**Response to methodologist review.** This document (a) resolves the 6 unclassified studies
the reviewer flagged (the "46 vs 52" discrepancy), (b) reports a corrected direction tally
that sums correctly, and (c) demotes vote-counting and the "benefit–harm symmetry" narrative
to hypothesis-generating status, explicitly separating this exploratory benefit analysis from
the primary safety question (Streams A/B).

## 1. Resolution of the 6 unclassified studies

The extracted table held 52 studies; 6 carried a BLANK direction. On verification against
each record's own abstract quote:

| PMID | Verified reason | Final status |
|---|---|---|
| 41384608 | FGF21 biomarker on cessation; not a GLP-1 effect on an addiction outcome | **EXCLUDE** |
| 41696398 | Systematic review counting ClinicalTrials.gov records; not a primary designed study | **EXCLUDE** |
| 40980971 | Target-trial emulation of adverse **liver** outcomes; no addiction/reward outcome | **EXCLUDE** |
| 40506208 | COaST RCT (semaglutide in schizophrenia+clozapine): reports **weight**, not addiction; a psychiatric-population **safety** RCT → route to Stream A | **EXCLUDE** |
| 40037282 | Dulaglutide smoking-cessation RCT, but this record reports **blood pressure**, not the cessation outcome | **no-effect** |
| 39246719 | Tirzepatide vs semaglutide cohort; explicitly **no** addiction/reward outcome (T2D incidence) | **EXCLUDE** |

**Outcome: 5 excluded (wrong outcome / review), 1 reclassified as no-effect.** Full detail
in `results/stream_D_reclassification.csv`. PMID 40506208 is flagged to the Stream A owners as
a psychiatric-population safety RCT; Stream D does not claim it.

## 2. Corrected counts that sum correctly

The reviewer's core complaint — a tally that did not reconcile to the denominator — is fixed
by reporting **both** the extracted-table N and the direction-eligible N:

- **Extracted-table N = 52** (all records that passed extraction).
- **Excluded from the direction tally = 5** (wrong outcome or review; see above).
- **Direction-eligible N = 47.**

Corrected direction tally (over the 47 eligible):

> **28 benefit / 13 mixed / 6 no-effect / 0 harm** (= 47), **+ 5 excluded = 52.**

The arithmetic now closes: 28 + 13 + 6 + 0 = 47 eligible, and 47 + 5 = 52 extracted.

**The "0 harm" cell means: no study in this corpus reported a pro-addiction (harmful)
direction of effect.** It is **not** evidence that GLP-1 RAs are safe with respect to
addiction, and still less with respect to the primary neuropsychiatric-safety question. Zero
harm-direction studies in a benefit-oriented, non-exhaustive scoping corpus is a property of
*what was searched and reported*, not a demonstrated absence of risk.

## 3. Vote-counting is demoted to hypothesis-generating context

The "28 benefit / 13 mixed / 6 no-effect / 0 harm" tally is **vote-counting**: it treats each
study as one equally-weighted ballot regardless of sample size, design, precision, or outcome.
Vote-counting is a well-known low-validity synthesis method — it is vulnerable to:
- **study size** (a 54-patient RCT and a 100k-record cohort count the same);
- **selective reporting / outcome-switching** (a study can be counted "benefit" on a
  secondary endpoint);
- **publication and retrieval bias** (a benefit-oriented search with capped retrieval —
  3 of 4 substance blocks truncated at 100 hits — over-samples positive findings);
- **outcome and substance heterogeneity** (alcohol, nicotine, opioid, stimulant, and
  composite SUD endpoints are not commensurable).

**Therefore the tally is retained ONLY as hypothesis-generating context** describing the shape
of the retrieved literature. It is **not** inferential evidence of benefit and must never be
reported as such. The inferential content of Stream D is limited to the pre-specified,
design-stratified pooled estimates in §5, each carried at **Very low** certainty.

## 4. "Benefit–harm symmetry" is demoted to a narrative, not a statistical property

The brief's framing that the benefit and harm sides are "symmetric in certainty" is an
**attractive narrative, not a statistical property.** The benefit side (Stream D) and the
harm side (Streams A/B) differ in outcomes (addiction/reward vs suicidality/depression),
populations (SUD/obesity vs broad GLP-1 RA users), designs, exposure definitions, and the
specific biases at play (benefit-side retrieval/publication bias vs harm-side notoriety bias
and confounding by indication). That both happen to land at "Very low certainty" under GRADE
is a **coincidence of a shared evidentiary bar applied to two different questions**, not a
symmetry that licenses any cross-inference. **The symmetry claim is hypothesis-generating
framing only and is removed from the inferential argument.**

## 5. Separation of questions; exploratory labelling

- The **primary question** of this project is neuropsychiatric **safety/harm** (Streams A and
  B). That is where the confirmatory inference lives.
- The **addiction/reward-benefit question (Stream D) is EXPLORATORY.** Per the project brief
  it is "the benefit counterpart" to the harm synthesis and was framed as a scoping analysis
  around the safety question; because it was not the pre-registered primary question, it must
  be labelled **exploratory** to avoid the appearance of a post-hoc positive-spin analysis.
- The pooled Stream D estimates below **stay exactly as reported** but are explicitly labelled
  **exploratory / Very low certainty**:

  | Substance | Stratum | k | Pooled | 95% CI | I² | Certainty |
  |---|---|---|---|---|---|---|
  | Alcohol | Observational (risk of adverse alcohol outcome) | 4 | RR 0.69 | 0.50–0.96 | 85% | Very low (exploratory) |
  | Nicotine | RCT+TTE (smoking abstinence/TUD, harmonized) | 2 | RR 0.68 | 0.63–0.74 | 0% | Very low (exploratory) |
  | Alcohol | AUDIT score (anchor-reproduced) | 4 | MD −7.81 | −9.02 to −6.60 | 88% | Very low (exploratory) |

  Directionally these favour GLP-1 RAs, but at Very low certainty and with the retrieval/
  publication-bias caveats above, they are **hypothesis-generating** and cannot be pooled with
  or set against the Stream A/B safety evidence.

## Bottom line

The 6 unclassified records resolve to **5 exclusions and 1 no-effect**, giving a
direction-eligible denominator of **47** with a corrected, self-consistent tally of
**28 benefit / 13 mixed / 6 no-effect / 0 harm (+5 excluded = 52)**. The direction tally and
the benefit–harm-symmetry framing are **hypothesis-generating only**; the exploratory pooled
estimates stand as reported at **Very low certainty**. "0 harm" means **no study reported a
pro-addiction direction**, not that GLP-1 RAs are safe.
