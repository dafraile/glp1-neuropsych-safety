
"""Dual-reviewer + judge risk-of-bias / GRADE harness.

Full-text RoB2 (RCT) and ROBINS-I (observational) assessment with two
independent model reviewers, per-domain disagreement detection, a judge tier
for flagged domains, and a full (study x domain x reviewer) audit trail.
Every rating carries a verbatim supporting quote that is substring-verified
against the source full text.
"""
import json, re, os

RATING_SCALE = {
    "RoB2": ["Low", "Some concerns", "High"],
    "ROBINS-I": ["Low", "Moderate", "Serious", "Critical", "No information"],
}
RATING_RANK = {
    "RoB2": {"Low": 0, "Some concerns": 1, "High": 2},
    "ROBINS-I": {"Low": 0, "Moderate": 1, "Serious": 2, "Critical": 3, "No information": 1},
}


def get_rubric(framework):
    """Return {domain_id: {name, question}} for RoB2 or ROBINS-I."""
    if framework == "RoB2":
        return {
            "D1": {"name": "Randomization process",
                   "question": "Was the allocation sequence random, concealed, and were baseline groups balanced?"},
            "D2": {"name": "Deviations from intended interventions",
                   "question": "Were there deviations from intended intervention (blinding of participants/carers), and was analysis appropriate (ITT)?"},
            "D3": {"name": "Missing outcome data",
                   "question": "Were outcome data available for nearly all participants, and is missingness unlikely to bias the result?"},
            "D4": {"name": "Measurement of the outcome",
                   "question": "Was the neuropsychiatric outcome measured with a systematic, validated instrument (e.g. C-SSRS) rather than spontaneous adverse-event capture, and were assessors blinded?"},
            "D5": {"name": "Selection of the reported result",
                   "question": "Was the neuropsychiatric outcome pre-specified in a protocol/SAP, and is there no evidence of selective reporting from multiple analyses?"},
        }
    elif framework == "ROBINS-I":
        return {
            "D1": {"name": "Confounding",
                   "question": "Was confounding by indication controlled (active comparator, propensity/multivariable adjustment for baseline psychiatric history, indication, comedication)?"},
            "D2": {"name": "Selection of participants",
                   "question": "Was selection into the study unrelated to exposure or outcome (new-user design, no immortal-time or prevalent-user bias)?"},
            "D3": {"name": "Classification of interventions",
                   "question": "Was GLP-1 RA exposure defined from records before outcome and free of misclassification?"},
            "D4": {"name": "Deviations from intended interventions",
                   "question": "Were exposure switches/adherence handled without introducing bias?"},
            "D5": {"name": "Missing data",
                   "question": "Were outcome and covariate data reasonably complete for exposed and comparator groups?"},
            "D6": {"name": "Measurement of outcomes",
                   "question": "Was the neuropsychiatric outcome ascertained comparably across groups (coded diagnoses / validated definition, aligned with the SMQ) and not differentially?"},
            "D7": {"name": "Selection of the reported result",
                   "question": "Was the reported adjusted estimate pre-specified rather than selected from many analyses?"},
        }
    raise ValueError("framework must be 'RoB2' or 'ROBINS-I'")


def build_reviewer_prompt(framework, study_text, study_id, max_chars=24000):
    rub = get_rubric(framework)
    scale = RATING_SCALE[framework]
    dom_lines = "\n".join(f"  {d}: {v['name']} -- {v['question']}" for d, v in rub.items())
    text = study_text[:max_chars]
    return (
        f"You are an independent methodology reviewer performing a {framework} risk-of-bias "
        f"assessment for study {study_id}. Assess ONLY from the study text provided.\n\n"
        f"Domains:\n{dom_lines}\n\n"
        f"Allowed ratings (use EXACTLY one of these strings): {scale}\n\n"
        f"For EVERY domain return: the rating, a VERBATIM quote copied word-for-word from the "
        f"study text that justifies the rating (or \"NO EVIDENCE IN TEXT\" if the text is silent), "
        f"and a one-sentence rationale. Do not paraphrase the quote.\n\n"
        f"Return ONLY valid JSON, no prose, in this exact shape:\n"
        f'{{\"study_id\": \"{study_id}\", \"framework\": \"{framework}\", '
        f'\"domains\": [{{\"domain\": \"D1\", \"rating\": \"...\", \"quote\": \"...\", \"rationale\": \"...\"}}, ...], '
        f'\"overall\": \"...\"}}\n\n'
        f"STUDY TEXT:\n{text}"
    )


def parse_json_block(s):
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\n?", "", s); s = re.sub(r"\n?```$", "", s)
    i, j = s.find("{"), s.rfind("}")
    if i >= 0 and j > i:
        s = s[i:j + 1]
    return json.loads(s)


def review_claude(framework, study_text, study_id, model=None):
    """Reviewer backend: a Claude call via host.llm. model=None -> reasoning default."""
    prompt = build_reviewer_prompt(framework, study_text, study_id)
    mdl = model or host.reasoning_model()
    r = host.llm(prompt, model=mdl, max_tokens=4000)
    out = parse_json_block(r["text"])
    out["_backend"] = f"claude:{mdl}"
    return out


def openai_key(cred_name=None):
    names = [cred_name] if cred_name else None
    if names is None:
        names = [c["name"] for c in host.credentials.list()
                 if "openai" in (c.get("provider", "") + c.get("name", "")).lower()]
    for nm in names:
        try:
            c = host.credentials.get(nm)
        except Exception:
            continue
        for k in ("api_key", "value", "token", "secret_access_key"):
            if c.get(k):
                return c[k]
    env = os.environ.get("OPENAI_API_KEY")
    if env:
        return env
    raise RuntimeError("no OpenAI credential found -- add one via Customize -> Credentials, "
                       "or pass cred_name=")


def review_openai(framework, study_text, study_id, model="gpt-4o", cred_name=None):
    """Reviewer backend: an OpenAI call. Requires the openai package + a stored key."""
    from openai import OpenAI
    client = OpenAI(api_key=openai_key(cred_name))
    prompt = build_reviewer_prompt(framework, study_text, study_id)
    resp = client.chat.completions.create(
        model=model, temperature=0,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompt}],
    )
    out = parse_json_block(resp.choices[0].message.content)
    out["_backend"] = f"openai:{model}"
    return out


def review(backend, framework, study_text, study_id, **kw):
    """Dispatch a single reviewer. backend in {'claude','openai'}."""
    if backend == "claude":
        return review_claude(framework, study_text, study_id, model=kw.get("model"))
    if backend == "openai":
        return review_openai(framework, study_text, study_id,
                             model=kw.get("model", "gpt-4o"), cred_name=kw.get("cred_name"))
    raise ValueError("backend must be 'claude' or 'openai'")


def verify_quotes(review_dict, full_text):
    """Annotate each domain with quote_verified (verbatim substring of full text)."""
    norm = re.sub(r"\s+", " ", full_text).lower()
    for d in review_dict.get("domains", []):
        q = (d.get("quote") or "").strip()
        if not q or q.upper().startswith("NO EVIDENCE"):
            d["quote_verified"] = None
        else:
            qn = re.sub(r"\s+", " ", q).lower()
            d["quote_verified"] = qn[:120] in norm if len(qn) > 20 else qn in norm
    return review_dict


def detect_disagreements(r1, r2, framework):
    """Per-domain comparison of two reviews. Returns list of flags."""
    rank = RATING_RANK[framework]
    m1 = {d["domain"]: d for d in r1.get("domains", [])}
    m2 = {d["domain"]: d for d in r2.get("domains", [])}
    flags = []
    for dom in sorted(set(m1) | set(m2)):
        a, b = m1.get(dom, {}), m2.get(dom, {})
        ra, rb = a.get("rating"), b.get("rating")
        gap = abs(rank.get(ra, 99) - rank.get(rb, 99)) if ra in rank and rb in rank else None
        flags.append({
            "domain": dom, "r1_rating": ra, "r2_rating": rb,
            "agree": ra == rb, "gap": gap,
            "severity": "match" if ra == rb else ("adjacent" if gap == 1 else "major"),
            "r1_quote": a.get("quote"), "r2_quote": b.get("quote"),
        })
    return flags


def build_judge_prompt(framework, study_id, flag):
    rub = get_rubric(framework)
    dom = flag["domain"]; name = rub.get(dom, {}).get("name", dom)
    return (
        f"Two independent reviewers disagree on {framework} domain {dom} ({name}) for study {study_id}.\n"
        f"Reviewer 1: rating='{flag['r1_rating']}', quote=\"{flag['r1_quote']}\"\n"
        f"Reviewer 2: rating='{flag['r2_rating']}', quote=\"{flag['r2_quote']}\"\n"
        f"Allowed ratings: {RATING_SCALE[framework]}\n"
        f"Adjudicate. If the two quotes support different ratings and neither is clearly correct, "
        f"escalate to a human. Return ONLY JSON: "
        f'{{\"resolution\": \"<one allowed rating>\" or \"ESCALATE_TO_HUMAN\", \"reason\": \"...\"}}'
    )


def judge(framework, study_id, flags, backend="claude", **kw):
    """Adjudicate only the disagreeing domains. Returns {domain: {resolution, reason}}."""
    out = {}
    for f in flags:
        if f["agree"]:
            continue
        prompt = build_judge_prompt(framework, study_id, f)
        if backend == "claude":
            r = host.llm(prompt, model=kw.get("model") or host.reasoning_model(), max_tokens=800)
            txt = r["text"]
        elif backend == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=openai_key(kw.get("cred_name")))
            resp = client.chat.completions.create(
                model=kw.get("model", "gpt-4o"), temperature=0,
                response_format={"type": "json_object"},
                messages=[{"role": "user", "content": prompt}])
            txt = resp.choices[0].message.content
        else:
            raise ValueError("judge backend must be 'claude' or 'openai'")
        out[f["domain"]] = parse_json_block(txt)
    return out


def audit_rows(study_id, framework, r1, r2, flags, resolutions):
    """One row per (study, domain, reviewer) + judge resolution. For a tidy CSV."""
    rows = []
    fm = {f["domain"]: f for f in flags}
    for label, rv in (("reviewer1", r1), ("reviewer2", r2)):
        for d in rv.get("domains", []):
            dom = d["domain"]
            rows.append({
                "study_id": study_id, "framework": framework, "reviewer": label,
                "backend": rv.get("_backend"), "domain": dom,
                "domain_name": get_rubric(framework).get(dom, {}).get("name", dom),
                "rating": d.get("rating"), "quote": d.get("quote"),
                "quote_verified": d.get("quote_verified"), "rationale": d.get("rationale"),
                "agree": fm.get(dom, {}).get("agree"),
                "disagreement_severity": fm.get(dom, {}).get("severity"),
                "judge_resolution": (resolutions.get(dom) or {}).get("resolution"),
                "judge_reason": (resolutions.get(dom) or {}).get("reason"),
            })
    return rows


def run_dual_review(study_id, full_text, framework,
                    backend1="claude", backend2="openai", judge_backend="claude",
                    b1_kw=None, b2_kw=None, judge_kw=None):
    """End-to-end: two reviewers -> quote-verify -> flag -> judge -> audit rows.
    Returns {study_id, framework, r1, r2, flags, resolutions, audit}."""
    b1_kw = b1_kw or {}; b2_kw = b2_kw or {}; judge_kw = judge_kw or {}
    r1 = verify_quotes(review(backend1, framework, full_text, study_id, **b1_kw), full_text)
    r2 = verify_quotes(review(backend2, framework, full_text, study_id, **b2_kw), full_text)
    flags = detect_disagreements(r1, r2, framework)
    resolutions = judge(framework, study_id, flags, backend=judge_backend, **judge_kw)
    audit = audit_rows(study_id, framework, r1, r2, flags, resolutions)
    return {"study_id": study_id, "framework": framework, "r1": r1, "r2": r2,
            "flags": flags, "resolutions": resolutions, "audit": audit}
