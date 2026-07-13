# FAERS case adjudication — reading guide

## What you are deciding
For each report, pick the single best-fit category for whether the semaglutide->suicide/
self-injury association in THIS report is a plausible drug attribution or better explained
by something else. Categories (mutually exclusive):

- plausible_drug_attributed  : temporally/clinically coherent, no dominant alternative
- confounded_by_indication   : the obesity/T2D indication itself carries elevated suicide risk
                               (e.g. weight/eating-disorder context, no other driver)
- confounded_by_comedication : a psychiatric co-medication is present (see psych_comeds_detected)
                               -> the psychiatric comorbidity it treats is the likely driver
- notoriety_or_legal_sourced : consumer/lawyer-sourced, or media-era hallmarks (off-label,
                               product-availability, litigation phrasing), low clinical detail
- uninterpretable            : the structured fields do not let you decide  <-- VALID and COMMON

## Important limitation (answers your question directly)
Public FAERS carries NO internal causality assessment and NO free-text narrative. The only
role field openFDA exposes is `drugcharacterization` (1=suspect, 2=concomitant, 3=interacting)
= the REPORTER's designation of which drug is primary, NOT an assessment that the drug caused
the event. There is no "attributable" flag. So you often cannot establish plausibility from the
fields alone -> `uninterpretable` is the correct answer then, not a failure. This is exactly why
the synthesis treats this layer as TRIAGE, not an attributable fraction.

## Columns to lean on
- reactions        : the full MedDRA PT list for the report (look for the actual mechanism of
                     death/harm — e.g. hepatic necrosis after intentional overdose)
- psych_comeds_detected / n_psych_comeds_corrected : psychiatric co-meds now include
                     ANTIPSYCHOTICS + mood-stabilizers + antidepressants + benzodiazepines
                     (the original n_psych_comeds MISSED antipsychotics; use the *_corrected column)
- indication       : reported indication for semaglutide (weight vs T2D vs unknown)
- source           : physician / other_HP / consumer / lawyer  (consumer/lawyer -> notoriety weight)
- serious/death/age/sex, action_taken, dose_text

## Worked examples (from this packet)
- FAERS_001 (completed suicide): reactions show intentional overdose -> hepatic necrosis/lactic
  acidosis; no psychiatric co-meds; semaglutide plausibly incidental to a self-inflicted overdose.
  Reasonable label: uninterpretable (no psychiatric history to invoke indication/comed, and the
  mechanism is the overdose, not a drug effect) — or plausible only if you judge the SMQ event
  itself is the outcome regardless of mechanism. Document your reasoning.
- FAERS_000 (suicidal ideation): quetiapine + aripiprazole present (antipsychotics) ->
  confounded_by_comedication (the original packet wrongly showed n_psych_comeds=0; corrected=5).
