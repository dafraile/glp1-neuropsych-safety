---
name: dual-reviewer-rob
description: Full-text risk-of-bias assessment (RoB2 for RCTs, ROBINS-I 2016 for observational) run through the OFFICIAL signalling questions of each tool -- 22 questions across 5 RoB2 domains, 34 across 7 ROBINS-I domains -- with per-question verbatim quotes, a deterministic algorithm cross-check, TWO independent cross-model reviewers (Claude Opus 4.8 + GPT-5.6 Sol), per-domain disagreement detection, a cross-model judge tier that adjudicates on the justified quotes, and a full study x domain x signalling-question x reviewer audit trail. Use when you need accountable, traceable RoB ratings grounded in the actual instrument rather than a single-line-per-domain heuristic pass -- hardening a systematic-review RoB layer, adjudicating between a Claude and a GPT reviewer, or flagging domains for human expert review.
---

# Dual-reviewer risk-of-bias harness (signalling-question engine)

Runs a full-text RoB assessment the way the tools are actually meant to be applied:
each domain is scored through its **official signalling questions**, every answer
carries a **verbatim quote**, a **deterministic algorithm** recomputes the domain
judgement where the tool publishes a decision table, **two independent cross-model
reviewers** work the same study, disagreements are flagged per domain, and a
**judge** adjudicates the flagged domains on the quotes — escalating to a human when
the verified evidence underdetermines the rating. Nothing is a single model's final
word, and every rating traces to text.

## Why signalling questions (vs the earlier thin prompt)
A one-line-per-domain prompt asks the model to jump straight to a verdict; the bias
often lives in a sub-question that one-liner never asks (e.g. ROBINS-I 5.4 "were
missing-data proportions similar across groups?", RoB2 1.2 allocation concealment).
This engine puts the model through the same structured questions a human RoB
assessor answers, then maps them to a judgement.

## The substrate (grounded, not paraphrased)
Signalling questions, response options (Y / PY / PN / N / NI / NA), condensed
elaborations, and the mapping algorithms are taken from the official riskofbias.info
guidance (RoB2 22 Aug 2019; ROBINS-I detailed guidance 20 Oct 2016) and stored in
`rob_tool_substrate.json`. Counts: **RoB2 = 22 signalling questions / 5 domains;
ROBINS-I 2016 = 34 / 7 domains.** "No information" is scored as its own answer and is
never treated as "no problem".

## The layered reviewer prompt (per study)
1. **General RoB instructions** — assess only from text, material-bias principle, the
   response-option scale, the NI-is-not-reassurance rule, verbatim-quote requirement.
2. **Condensed study-type guidance** — the domain intros and what evidence to look
   for, specialised for RCT (RoB2) vs observational (ROBINS-I), framed to the review's
   neuropsychiatric outcome and confounding-by-indication concern.
3. **All signalling questions at once** with a permissive token budget (reviewers try
   12k->20k Claude / 24k->40k OpenAI).
4. **Per-question answer + verbatim quote + short note**, then a stated domain rating
   and overall judgement.

## Backends
- **Reviewer 1** default `claude`, model **`claude-opus-4-8`** (via `host.llm`).
- **Reviewer 2** default `openai`, model **`gpt-5.6-sol`** at `reasoning_effort="medium"`
  (needs an OpenAI credential, `pip install openai`, `api.openai.com` allowlisted).
- **Judge** default `claude` (**`claude-sonnet-5`**) — a BLINDED, distinct third model
  that is neither reviewer's. The two reviewers are presented as Reviewer A / Reviewer B
  with no model identity and in a per-domain randomized order, and the judge is instructed
  not to infer identity nor reward fluency/confidence/agreeableness. This closes both the
  style-preference channel and the same-model-reasoning channel. Choice grounded in a
  blinded 3-judge test (Opus / Sonnet-5 / GPT-5.6 Sol on the pilot's split domains): Opus,
  even blinded, sided with the Opus reviewer 7/10 (same-model reasoning correlation) and
  escalated only 1/10; Sonnet-5 showed no such correlation and escalated conservatively —
  the right disposition for a judge that only sees genuinely hard cases. Override via
  `judge_backend=` / `judge_kw` (e.g. `judge_kw={"model":"claude-opus-4-8"}`).
- If no OpenAI key: set `backend2="claude"`, `judge_backend="claude"` for two
  independent Claude passes (catches transcription/judgment slips, not architectural
  blind spots).

## Deterministic algorithm cross-check
`cross_check_algorithm` recomputes the domain judgement from each reviewer's
signalling answers. RoB2 **D1** (Table 4) and **D3** (Table 10) have clean published
decision tables and get an EXACT recompute; other domains return `algo_rating=None`
and rely on the judge's criteria check. Each domain carries `algo_rating` and
`algo_consistent` (does the model's stated rating match the algorithm?). An
inconsistency is a third signal, alongside the two reviewers, that the domain needs a
look.

## Reconciliation round (pre-escalation rebuttal)
Before the judge, every domain where the two reviewers disagree gets ONE **hardened
reconciliation round** (`reconcile=True`, default): each reviewer — on its own backend —
sees the other's rating, rationale, and signalling quotes, and may revise. It is
anti-capitulation by construction: a reviewer changes its rating ONLY on text-grounded
evidence it missed, is told not to downgrade merely to agree, and is warned that an
unreported bias source (missing adherence data, no prespecified protocol, unhandled missing
covariates) is **not reassurance**. Domains that converge are resolved by that consensus
(`resolution_source="reconciliation"`); only domains still split go to the judge, and then
to the human queue if the judge escalates.

Why hardened, not naive: in the pilot, a plain rationale-swap autoresolved more cases but its
errors were **silent under-ratings** (reviewers talking each other down via "not *shown* to be
differential"), the dangerous direction for RoB. The hardened prompt flips the error direction —
its disagreements with a human rubric were **over-ratings** (worst case: an extra study in the
review queue), consistent with the RoB convention to err toward stronger suspicion of bias when
in doubt. Set `reconcile=False` to skip the round and send all disagreements straight to the judge.

## Kernel helpers (auto-loaded)
`get_rubric(framework)`, `build_reviewer_prompt(...)`, `review(backend, ...)`,
`review_claude`, `review_openai`, `algorithm_judgement(...)`,
`cross_check_algorithm(...)`, `verify_quotes(review, full_text)`,
`reconcile_domain(...)`, `build_escalation_packet(run_results, out_path=)`,
`detect_disagreements(r1, r2, framework)`, `judge(...)`, `audit_rows(...)`, and the
one-call wrapper `run_dual_review(...)`. `framework` is `"RoB2"` (RCTs) or
`"ROBINS-I"` (observational, 2016 7-domain structure).

## Workflow
```python
# host.llm and the OpenAI client are host-side -> run from the repl tool.
texts = {...}  # {study_id: full_text}. Full text >> abstract for RoB.
results = []
for sid, txt in texts.items():
    r = run_dual_review(sid, txt, framework="ROBINS-I",
                        backend1="claude", backend2="openai", judge_backend="openai")
    results.append(r)
# then flatten in a python cell:
import pandas as pd
rows = [row for r in results for row in r["audit"]]
pd.DataFrame(rows).to_csv("rob_audit_trail.csv", index=False)
```

Each `run_dual_review` returns `{study_id, framework, r1, r2, flags, reconciliation, resolutions, audit}`:
- `r1`/`r2`: full reviews — per domain, a `signalling` list (`sq, answer, quote,
  quote_verified, note`), a `rating`, `algo_rating`, `algo_consistent`, `rationale`.
- `flags`: per-domain `{agree, gap, severity: match|adjacent|major, r1/r2_algo_consistent}`.
- `resolutions`: judge output for disagreeing domains only —
  `{resolution: <rating> | "ESCALATE_TO_HUMAN", reason}`.
- `audit`: one row per (study, domain, signalling question, reviewer) with the answer,
  verbatim quote, `quote_verified`, the domain rating, `algo_rating`/`algo_consistent`,
  disagreement severity, and judge resolution.

## Traceability contract
- Every signalling answer carries a verbatim quote; `quote_verified` marks whether it
  is actually a substring of the source. An answer whose quote does not verify is a
  fabrication flag — the judge is told to discount it.
- The human-expert queue = `major` disagreements (rating gap >= 2), any
  `ESCALATE_TO_HUMAN`, and any domain where `algo_consistent is False`. Filter the
  audit CSV to those.
- **`build_escalation_packet(run_results, out_path=)`** assembles a ready-to-review
  markdown packet for every `ESCALATE_TO_HUMAN` domain: both reviewers' original and
  post-reconciliation ratings, every signalling answer with verbatim quote and
  `verify_status`, the judge's reason (which names the deciding signalling question and
  what evidence is missing), the candidate ratings, and a blank "Your call" line. Accepts
  one result dict or a list; returns a "nothing escalated" note when the queue is empty.
  Run it after every batch so the human always gets a focused queue rather than raw JSON.
- Reviewer backends, per-question answers, quotes, algorithm recompute, and judge
  reasoning are all preserved. Nothing is silently overwritten.

## Notes
- Call `run_dual_review` from the `repl` tool; write results to `./handoff/*.json`,
  flatten to CSV in a `python` cell.
- A reviewer parse failure that survives both token-budget retries raises
  `RuntimeError` and stops that study (a reviewer with no valid ratings can't be
  scored); wrap the per-study call in try/except to skip-and-continue on a batch.
- This harness assesses; it does not compute the pooled estimate. Feed resolved
  per-study ratings into the `grade-hybrid` step (RCT starts High, observational
  starts Low).
