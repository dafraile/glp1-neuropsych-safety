# Stream D direction + inclusion audit (2026-07)

Proportionate check for the EXPLORATORY, non-pooled addiction/reward stream. Because Stream D
rests on DIRECTION vote-counting (not pooled effect sizes), the audit re-verified direction
classification and inclusion — NOT numeric magnitudes (which feed no pooled estimate).

Method: blind LLM re-classification of all 52 abstracts (direction + in-scope, no knowledge
of the existing label), diffed against the current table with the 6-study reclassification
folded in.

## Headline check: "0 harm" CONFIRMED (51/52 blind-classified)
The blind pass returned a parseable classification for 51 of 52 abstracts and found ZERO
studies reporting a pro-addiction / worsening direction among them. The 52nd (PMID 42355949,
alcohol) has no abstract in PubMed (title only). A retry parsed but was based solely on the
110-char title (it returned "benefit"); judged unreliable on title alone, it was discarded
and the record retains its prior "mixed" label. Either way it was NOT coded harm. No study in the corpus — pre- or
post-audit — is classified harm, so the load-bearing "0 harm" cell holds, with the explicit
caveat that one record was verified only against its pre-existing (non-harm) label rather than
by independent blind read.

## Corrections applied (benefit over-count guarded)
| PMID | Was | Now | Why |
|---|---|---|---|
| 40577093 | benefit | EXCLUDED | Systematic review (37 studies) — snowball-only, not a primary tally row |
| 38264360 | benefit | no-effect | This record's outcome is weight gain during cessation, not the abstinence/addiction endpoint (sister record holds the cessation result) |
| 41036780 | no-effect | EXCLUDED | Prescription-trend/utilization study; no GLP-1->addiction effect |
| 36655300 | benefit | benefit (kept) | Blind flagged out-of-scope, but Control-of-Eating craving domains ARE a food-reward outcome — legitimately in scope |

Plus the 6 previously-unclassified studies resolved earlier (5 EXCLUDE + 1 no-effect;
41384608 FGF21 biomarker, 41696398 registry count, 40980971 liver TTE, 40506208 schizophrenia
weight RCT->Stream A, 39246719 T2D/CV cohort; 40037282 smoking-BP record -> no-effect).

## Corrected tally
| | before | after audit |
|---|---|---|
| benefit | 28 | **26** |
| mixed | 13 | 13 |
| no-effect | 6 | 6 |
| harm | 0 | **0** |
| excluded | 5 | **7** |
| direction-eligible | 47 | **45** |

## Interpretation (unchanged framing)
Still a directional vote-count of an exploratory literature, NOT an inferential estimate. The
benefit direction predominates (26/45) with zero harm signals, but this is descriptive: no
pooled effect, designs are heterogeneous (secondary-analyses, single-arm, RCTs), and
publication/outcome-reporting bias toward positive addiction findings is likely. The audit
slightly reduces the benefit count and confirms no harm — it does not change the exploratory
status or licence any causal benefit claim.

## Scope note
Numeric effect estimates (effect_est/CI) were NOT re-verified — they feed no pooled result.
This is deliberate proportionality, not an omission: Stream D's conclusion depends on
direction and inclusion, both of which were checked.
