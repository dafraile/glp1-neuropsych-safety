"""Kernel helpers for the grade-hybrid skill.

Deterministic engine for the mechanical GRADE domains (risk of bias aggregation,
inconsistency, imprecision) + a dual-reviewer harness (Claude + GPT-5.5 + judge)
for the judgment domains (indirectness, publication bias, magnitude of downgrade,
observational upgrade factors). RCTs start High, observational starts Low.

host.llm and the OpenAI client are host-side -> call the dual-review wrappers from
the repl tool; the deterministic engine is pure Python and runs anywhere.
"""
import json, re

GRADE_LEVELS = ["Very low", "Low", "Moderate", "High"]

# ---------------------------------------------------------------- deterministic

def clamp_level(idx):
    return GRADE_LEVELS[max(0, min(3, idx))]

def apply_deltas(start, total_delta):
    """start level + net delta (negative=downgrade), floored/capped to the scale."""
    return clamp_level(GRADE_LEVELS.index(start) + total_delta)

def rob_body_downgrade(study_overalls):
    """Body-of-evidence RoB downgrade from resolved per-study RoB ratings
    (RoB2: Low/Some concerns/High; ROBINS-I: Low/Moderate/Serious/Critical).
    Returns (delta, reason). Drives GRADE from the dual-reviewer-rob output."""
    ov = [str(x) for x in study_overalls]
    if any(x in ("Critical",) for x in ov):
        return -2, "critical RoB in the body of evidence"
    n = len(ov) or 1
    n_top = sum(x in ("Serious", "High") for x in ov)
    if n_top and n_top >= n / 2:
        return -2, f"serious/high RoB dominates ({n_top}/{n})"
    if any(x in ("Serious", "High", "Moderate", "Some concerns") for x in ov):
        return -1, "moderate-to-serious RoB present"
    return 0, "low RoB across the body"

def inconsistency_downgrade(I2, k, ci_overlap=None):
    """Statistical heterogeneity. I2 in [0,100]; k = number of studies."""
    if k is None or k < 2 or I2 is None or (isinstance(I2, float) and I2 != I2):
        return 0, "single study / not estimable"
    if I2 >= 75:
        return -1, f"substantial heterogeneity (I2={I2:.0f}%)"
    if I2 >= 50:
        return -1, f"moderate heterogeneity (I2={I2:.0f}%)"
    return 0, f"low heterogeneity (I2={I2:.0f}%)"

def imprecision_downgrade(ci_low, ci_high, k, events=None, ois=300,
                          spans_null=None, null=1.0):
    """CI width vs decision threshold, event count vs optimal information size."""
    if spans_null is None and ci_low is not None and ci_high is not None:
        spans_null = ci_low < null < ci_high
    reasons, d = [], 0
    if k is not None and k <= 2:
        d = max(d, 1); reasons.append(f"few studies (k={k})")
    if spans_null:
        d = max(d, 1); reasons.append("CI crosses the null")
    if events is not None and events < ois:
        d = max(d, 1); reasons.append(f"{events} events < OIS ({ois})")
    if ci_low and ci_high and ci_low > 0 and ci_high / ci_low > 3:
        d = max(d, 1); reasons.append("wide CI (ratio > 3x)")
    return -d, ("; ".join(reasons) if reasons else "adequate precision")

def deterministic_profile(start, study_overalls, I2, k, ci_low, ci_high,
                          events=None, ois=300, null=1.0):
    """Run the three mechanical domains. Returns a dict with per-domain
    (delta, reason) and the running subtotal off `start`."""
    rob = rob_body_downgrade(study_overalls)
    inc = inconsistency_downgrade(I2, k)
    imp = imprecision_downgrade(ci_low, ci_high, k, events=events, ois=ois, null=null)
    subtotal = rob[0] + inc[0] + imp[0]
    return {
        "start": start,
        "risk_of_bias": {"delta": rob[0], "reason": rob[1]},
        "inconsistency": {"delta": inc[0], "reason": inc[1]},
        "imprecision": {"delta": imp[0], "reason": imp[1]},
        "deterministic_subtotal": subtotal,
        "level_after_deterministic": apply_deltas(start, subtotal),
    }

# --------------------------------------------------------- judgment (reviewers)

JUDGMENT_DOMAINS = {
    "indirectness": "Do the population (obesity vs T2D), intervention, comparator, and "
        "outcome match the PICO directly? Surrogate vs hard outcome? Downgrade -1 or -2, or 0.",
    "publication_bias": "Small-study effects, search comprehensiveness, funnel/Egger "
        "(unreliable at k<10). Downgrade -1 or 0.",
    "upgrade_large_effect": "Observational only: is the effect large (RR>2 or <0.5) and "
        "unlikely to be confounding? Upgrade +1/+2 or 0. RCTs: always 0.",
    "upgrade_dose_response": "Observational only: monotonic dose-response gradient? "
        "Upgrade +1 or 0. RCTs: always 0.",
    "upgrade_opposing_confounding": "Observational only: would plausible residual confounding "
        "bias TOWARD the null, i.e. the true effect is likely larger than observed? Upgrade +1 or 0.",
}

def build_grade_reviewer_prompt(outcome, stratum, evidence_json):
    """evidence_json: a compact dict of the numeric + PICO context for one SoF row."""
    doms = "\n".join(f"  {k}: {v}" for k, v in JUDGMENT_DOMAINS.items())
    return (
        f"You are an independent GRADE methodologist rating the JUDGMENT domains for one "
        f"summary-of-findings row. Stratum: {stratum}. Outcome: {outcome}.\n\n"
        f"Rate ONLY these domains (the mechanical domains - risk of bias, inconsistency, "
        f"imprecision - are computed separately and are NOT your job):\n{doms}\n\n"
        f"Evidence context (numbers already computed; do not recompute):\n"
        f"{json.dumps(evidence_json, indent=1)}\n\n"
        f"For upgrade domains, remember upgrades apply to OBSERVATIONAL evidence only and only "
        f"when no downgrade for that concern applies. Return ONLY valid JSON:\n"
        f'{{"outcome": "{outcome}", "domains": [{{"domain": "indirectness", "delta": 0, '
        f'"quote_or_reason": "...", "rationale": "..."}}, ...]}}'
    )

def review_grade_claude(outcome, stratum, evidence_json, model=None):
    prompt = build_grade_reviewer_prompt(outcome, stratum, evidence_json)
    mdl = model or host.reasoning_model()
    last = None
    for mt in (4000, 8000):
        r = host.llm(prompt, model=mdl, max_tokens=mt)
        txt = r.get("text", "") or ""
        try:
            out = gparse_json(txt); out["_backend"] = f"claude:{mdl}"; return out
        except Exception as e:
            last = (repr(e), r.get("stop_reason"))
    raise RuntimeError(f"review_grade_claude failed: {last}")

def review_grade_openai(outcome, stratum, evidence_json, model="gpt-5.5",
                        cred_name=None, reasoning_effort="high"):
    from openai import OpenAI
    client = OpenAI(api_key=gopenai_key(cred_name))
    prompt = build_grade_reviewer_prompt(outcome, stratum, evidence_json)
    is_reasoning = model.startswith(("gpt-5", "o1", "o3", "o4"))
    last = None
    for budget in ((8000, 16000) if is_reasoning else (4000, 8000)):
        kw = dict(model=model, response_format={"type": "json_object"},
                  messages=[{"role": "user", "content": prompt}])
        if is_reasoning:
            kw["max_completion_tokens"] = budget
            if reasoning_effort:
                kw["reasoning_effort"] = reasoning_effort
        else:
            kw["temperature"] = 0; kw["max_tokens"] = budget
        resp = client.chat.completions.create(**kw)
        txt = resp.choices[0].message.content or ""
        try:
            out = gparse_json(txt); out["_backend"] = f"openai:{model}"; return out
        except Exception as e:
            last = (repr(e), resp.choices[0].finish_reason)
    raise RuntimeError(f"review_grade_openai failed: {last}")

def judge_grade_domain(outcome, domain, r1_delta, r1_reason, r2_delta, r2_reason,
                       backend="claude", model=None, cred_name=None,
                       reasoning_effort="high"):
    prompt = (
        f"Two GRADE methodologists disagree on the '{domain}' domain for outcome '{outcome}'.\n"
        f"Reviewer 1: delta={r1_delta} ({r1_reason})\nReviewer 2: delta={r2_delta} ({r2_reason})\n"
        f"Decide the correct integer delta, or ESCALATE_TO_HUMAN if the evidence given cannot "
        f'resolve it. Return ONLY JSON: {{"resolution": <int or "ESCALATE_TO_HUMAN">, "reason": "..."}}'
    )
    try:
        if backend == "claude":
            r = host.llm(prompt, model=model or host.reasoning_model(), max_tokens=2000)
            txt = r["text"]
        else:
            from openai import OpenAI
            client = OpenAI(api_key=gopenai_key(cred_name))
            m = model or "gpt-5.5"
            kw = dict(model=m, response_format={"type": "json_object"},
                      messages=[{"role": "user", "content": prompt}])
            if m.startswith(("gpt-5", "o1", "o3", "o4")):
                kw["max_completion_tokens"] = 4000; kw["reasoning_effort"] = reasoning_effort
            else:
                kw["temperature"] = 0
            txt = client.chat.completions.create(**kw).choices[0].message.content
        return gparse_json(txt)
    except Exception as e:
        return {"resolution": "ESCALATE_TO_HUMAN", "reason": f"judge unparseable ({e!r})"}

def dual_review_judgment(outcome, stratum, evidence_json, is_rct,
                         backend2="openai", judge_backend="claude", **kw):
    """Two independent reviewers on the judgment domains + judge on disagreements.
    Forces all upgrade domains to 0 for RCTs. Returns per-domain resolved deltas + audit."""
    r1 = review_grade_claude(outcome, stratum, evidence_json)
    r2 = (review_grade_openai(outcome, stratum, evidence_json, **kw)
          if backend2 == "openai" else review_grade_claude(outcome, stratum, evidence_json))
    d1 = {d["domain"]: d for d in r1.get("domains", [])}
    d2 = {d["domain"]: d for d in r2.get("domains", [])}
    resolved, audit = {}, []
    for dom in JUDGMENT_DOMAINS:
        a, b = d1.get(dom, {}), d2.get(dom, {})
        da, db = int(a.get("delta", 0) or 0), int(b.get("delta", 0) or 0)
        if is_rct and dom.startswith("upgrade_"):
            da = db = 0
        agree = da == db
        if agree:
            resolved[dom] = da; res = None
        else:
            j = judge_grade_domain(outcome, dom, da, a.get("quote_or_reason", ""),
                                   db, b.get("quote_or_reason", ""), backend=judge_backend)
            jr = j.get("resolution")
            resolved[dom] = (jr if isinstance(jr, int) else min(da, db))  # conservative on escalate
            res = j
        audit.append({"outcome": outcome, "domain": dom, "r1_delta": da, "r2_delta": db,
                      "agree": agree, "resolved_delta": resolved[dom],
                      "r1_backend": r1.get("_backend"), "r2_backend": r2.get("_backend"),
                      "r1_reason": a.get("quote_or_reason", ""), "r2_reason": b.get("quote_or_reason", ""),
                      "judge": res})
    return {"outcome": outcome, "resolved": resolved, "audit": audit, "r1": r1, "r2": r2}

def grade_row(outcome, stratum, is_rct, study_overalls, I2, k, ci_low, ci_high,
              events=None, ois=300, null=1.0, run_judgment=True, backend2="openai", **kw):
    """One full SoF row: deterministic domains + (optional) dual-reviewer judgment.
    Returns the profile, the resolved judgment deltas, and the final certainty."""
    start = "High" if is_rct else "Low"
    prof = deterministic_profile(start, study_overalls, I2, k, ci_low, ci_high,
                                 events=events, ois=ois, null=null)
    judgment = None
    jdelta = 0
    if run_judgment:
        judgment = dual_review_judgment(outcome, stratum, {
            "stratum": stratum, "k": k, "I2": I2, "ci": [ci_low, ci_high],
            "events": events, "is_rct": is_rct}, is_rct, backend2=backend2, **kw)
        jdelta = sum(judgment["resolved"].values())
    total = prof["deterministic_subtotal"] + jdelta
    prof["judgment_delta"] = jdelta
    prof["final_certainty"] = apply_deltas(start, total)
    return {"outcome": outcome, "stratum": stratum, "profile": prof, "judgment": judgment,
            "final_certainty": prof["final_certainty"]}

# ------------------------------------------------------------------- internals

def gparse_json(s):
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\n?", "", s); s = re.sub(r"\n?```$", "", s)
    i, j = s.find("{"), s.rfind("}")
    if i >= 0 and j > i:
        s = s[i:j + 1]
    return json.loads(s)

def gopenai_key(cred_name=None):
    names = [cred_name] if cred_name else [
        c["name"] for c in host.credentials.list()
        if "openai" in (c.get("provider", "") + c.get("name", "")).lower()]
    for nm in names:
        try:
            c = host.credentials.get(nm)
        except Exception:
            continue
        for k in ("api_key", "value", "token", "secret_access_key"):
            if c.get(k):
                return c[k]
    import os
    return os.environ.get("OPENAI_API_KEY")
