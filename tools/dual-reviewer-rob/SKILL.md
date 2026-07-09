---
name: dual-reviewer-rob
description: Full-text risk-of-bias (RoB2 for RCTs, ROBINS-I for observational) and GRADE-input assessment with TWO independent model reviewers, per-domain disagreement detection, a judge tier for flagged domains, and a full study x domain x reviewer audit trail with verbatim quote verification. Use when you need accountable, traceable RoB ratings rather than a single-reviewer heuristic pass -- e.g. hardening a systematic-review RoB layer, adjudicating between a Claude and a GPT reviewer, or flagging domains for human expert review. Cross-model by default (Claude + OpenAI); falls back to two independent Claude passes if no OpenAI key.
---

# Dual-reviewer risk-of-bias / GRADE harness

Runs a full-text RoB assessment as **two independent reviewers + a judge**, so
no single model's judgment is the final word and every rating is traceable to a
verbatim quote. Built for systematic-review accountability: one model does
reviewer #1, a *different* model does reviewer #2, disagreements are detected
per domain, and a third judge call resolves flagged domains or escalates them to
a human.

## When to use
- You have full texts (or substantial abstracts) and need defensible RoB2 /
  ROBINS-I ratings, not a rules-based first pass.
- You want cross-model review (Claude + GPT) with disagreement flagging.
- You need a per-(study x domain x reviewer) audit trail for a methods appendix.

## Backends
- **Reviewer 1** default `claude` (via `host.llm`, no key needed).
- **Reviewer 2** default `openai`, model **`gpt-5.5`** at `reasoning_effort="high"`
  (needs an OpenAI credential via Customize -> Credentials, `pip install openai`,
  and `api.openai.com` on the network allowlist). Override the model with
  `b2_kw={"model": "..."}`; `review_openai` auto-detects reasoning models
  (`gpt-5.x` / `o`-series) and switches to `max_completion_tokens` + `reasoning_effort`
  (no `temperature`), falling back to `temperature=0` + `max_tokens` for classic
  chat models like `gpt-4o`. If no OpenAI key is available, set `backend2="claude"`
  for two independent same-family passes (catches transcription/judgment slips but
  not architectural blind spots).
- **Judge** default `claude`; adjudicates only the domains where the two reviewers
  disagree. When run on `openai`, defaults to `gpt-5.5` at high effort with the same
  reasoning-model handling.
- **Token budgets** auto-retry from a normal to a large ceiling: a 7-domain ROBINS-I
  assessment overruns a small `max_tokens`, so reviewers try 8k->14k/16k->24k and the
  judge uses 4k (Claude) / 8k (OpenAI). If the **judge** still returns unparseable
  output for a domain, that domain degrades to `ESCALATE_TO_HUMAN`. A **reviewer**
  parse failure that survives both retries raises `RuntimeError` and stops that
  study (by design — a reviewer with no valid ratings can't be scored); wrap the
  per-study call in try/except if you want the batch to skip and continue.

## Kernel helpers (auto-loaded)
`get_rubric(framework)`, `build_reviewer_prompt(...)`, `review(backend, ...)`,
`review_claude`, `review_openai`, `verify_quotes(review, full_text)`,
`detect_disagreements(r1, r2, framework)`, `judge(...)`, `audit_rows(...)`,
and the one-call wrapper `run_dual_review(...)`.
`framework` is `"RoB2"` (RCTs) or `"ROBINS-I"` (observational).

## Workflow

```python
# 1. Load full texts as {study_id: text}. Full text >> abstract for RoB.
texts = {...}

# 2. Run the dual review per study (one repl cell; host.llm/openai are host-side)
results = []
for sid, txt in texts.items():
    r = run_dual_review(sid, txt, framework="ROBINS-I",
                        backend1="claude", backend2="openai", judge_backend="claude")
    results.append(r)

# 3. Flatten the audit trail to a tidy CSV (in a python cell, from handoff JSON)
import pandas as pd
rows = [row for r in results for row in r["audit"]]
pd.DataFrame(rows).to_csv("rob_audit_trail.csv", index=False)
```

Each `run_dual_review` returns `{study_id, framework, r1, r2, flags,
resolutions, audit}`:
- `flags`: per-domain `{agree, gap, severity: match|adjacent|major, quotes}`.
- `resolutions`: judge output for disagreeing domains only —
  `{resolution: <rating> | "ESCALATE_TO_HUMAN", reason}`.
- `audit`: one row per (study, domain, reviewer) with rating, quote,
  `quote_verified` (bool — is the quote a verbatim substring of the source?),
  disagreement severity, and judge resolution.

## Traceability contract
- Every domain rating carries a **verbatim quote**; `verify_quotes` marks
  whether it is actually present in the source text (`quote_verified`). A
  rating whose quote does not verify is a fabrication flag — treat as unreliable.
- **Major** disagreements (rating gap >= 2) and any `ESCALATE_TO_HUMAN`
  resolution are the human-expert queue. Filter the audit CSV to those rows.
- The audit CSV is the record: reviewer backends, quotes, judge reasoning, all
  preserved. Nothing is silently overwritten.

## Notes
- `host.llm` and the OpenAI client are **host-side** — call `run_dual_review`
  from the `repl` tool (control-plane kernel), write results to
  `./handoff/*.json`, then flatten to CSV in a `python` cell.
- Per-frame `host.llm` token budget is finite: for large corpora, chunk studies
  across sessions or route reviewer #1 to OpenAI too.
- This harness assesses; it does not compute the pooled estimate. Feed the
  resolved per-study ratings into your GRADE step (RCT starts High, observational
  starts Low; downgrade for the resolved RoB, measured I2, and imprecision).
