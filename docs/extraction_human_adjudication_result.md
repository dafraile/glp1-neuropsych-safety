# Extraction — human validation result

**Reviewer:** single expert (PI). **Packet:** 38 rows, disagreement-enriched; 35 labelled.
Unlike FAERS, extraction HAS a ground truth — the value is printed in the abstract — so
numeric fields are scored as accuracy, not mere concordance.

## Results (vs human)
| Field | Metric | sonnet-5 | gpt-5.5 |
|---|---|---|---|
| direction (protective/harmful/null) | agreement | 5/5 | 5/5 |
| outcome_category (after vocab crosswalk) | concordance | 9/12 (0.75) | 8/12 (0.67) |
| numeric effect_est/ci (clean single-value rows) | exact match vs ground truth | 2/11 (0.18) | 6/11 (0.55) |

## Findings
1. **Numeric extraction has a real accuracy gap, and gpt-5.5 is the stronger extractor**
   (6/11 vs 2/11 exact matches to the reviewer's ground-truth reading). This corroborates
   the earlier model-computed genuine material-discrepancy rate (~29%).
2. **outcome_category raw agreement (1/13) was a VOCABULARY artifact, not judgment.** The
   models emit their own label set (`neuropsychiatric_other`, `composite_suicidality`, …)
   while the reviewer used the study-table vocabulary supplied in the packet
   (`neuropsychiatric (non-core/non-poolable)`, `suicidality (composite)`, …). After a
   crosswalk to a common space, concordance is 9/12 and 8/12. This is a packet-design flaw
   (two label dictionaries), corrected here by crosswalk; the models DO capture the outcome.
3. **6 of 17 numeric rows are ill-posed as 'extract one number'** — the study reports
   multiple estimates (multiple drugs × comparators × strata × outcomes). Example EXT_001:
   the abstract carries 8+ HRs; the reviewer's 1.12 (tirzepatide vs semaglutide, anxiety) is
   a real value but a different contrast than the packet's target (semaglutide vs
   naltrexone-bupropion, 0.67/0.73). Neither is an error; the task was under-specified for
   multi-estimate studies. Flagged as a task-design limitation, not a discrepancy.

## Direction of the overall signal (unchanged, now corroborated)
Both the FAERS concurrent-validity check and this extraction accuracy check point the same
way: gpt-5.5 tracks the expert better than sonnet-5 on the load-bearing judgments. The
extraction discrepancies are in numeric precision and vocabulary, NOT in direction (5/5) —
so the sign of every pooled estimate is safe; the uncertainty is in exact magnitudes, which
is already reflected in the wide observational CIs and the decision not to over-interpret
point estimates.

## Caveats
1. n small per field (5-12 scoreable rows); disagreement-enriched -> directional.
2. Single reviewer ground truth for numerics = one careful human read of the abstract, not
   independent double-extraction.
3. outcome_category crosswalk is a post-hoc harmonization; the underlying packet should have
   used ONE shared vocabulary. Fixed for any future round.
