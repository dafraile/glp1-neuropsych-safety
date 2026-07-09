"""
faers_tool.py — FAERS / openFDA spontaneous-report extraction & disproportionality
================================================================================
Stream B of the GLP-1 neuropsychiatric-safety triangulation project.

Pulls spontaneous adverse-event reports from the openFDA drug/event endpoint,
standardizes neuropsychiatric outcomes to the MedDRA SMQ "Suicide/self-injury"
term set (plus depression / anxiety), and computes disproportionality signals
(PRR, ROR, IC) against either the full-database background or a custom
active-comparator background (SGLT2 / DPP-4) to probe confounding by indication.

This stream is kept SEPARATE from the designed-study pooled estimate (Stream A);
its output exists for comparison only.

openFDA drug/event field map (verified against live API):
  patient.drug.openfda.generic_name        drug identity (INN)
  patient.drug.openfda.brand_name          brand identity
  patient.drug.drugcharacterization        1=suspect 2=concomitant 3=interacting
  patient.reaction.reactionmeddrapt        MedDRA Preferred Term (outcome)
  receivedate                              YYYYMMDD (FDA receipt date)
  primarysource.qualification              1=physician 2=pharmacist 3=other HP
                                           4=lawyer 5=consumer/non-HP
  serious, seriousnessdeath, ...           seriousness flags

No API key required for modest volumes; set OPENFDA_API_KEY env var to raise
rate limits (240->120000 req/day). All calls retry with backoff; a 404 from
openFDA means zero matching records (handled as count 0).
"""
from __future__ import annotations
import os, time, math, json, urllib.request, urllib.parse, urllib.error

BASE = "https://api.fda.gov/drug/event.json"
API_KEY = os.environ.get("OPENFDA_API_KEY")

# ---------------------------------------------------------------------------
# Controlled vocabularies
# ---------------------------------------------------------------------------

# GLP-1 receptor agonists (PICO intervention) + comparators.
# Each entry: list of openFDA generic_name tokens to OR together.
# 'brands' documents the aliases; generic_name search already resolves brands
# via openfda normalization, but brands are kept for transparency / reporting.
DRUGS = {
    # --- GLP-1 receptor agonists (intervention) ---
    "semaglutide":   {"class": "GLP-1 RA", "generic": ["semaglutide"],
                      "brands": ["Ozempic", "Wegovy", "Rybelsus"]},
    "liraglutide":   {"class": "GLP-1 RA", "generic": ["liraglutide"],
                      "brands": ["Victoza", "Saxenda"]},
    "tirzepatide":   {"class": "GIP/GLP-1 RA", "generic": ["tirzepatide"],
                      "brands": ["Mounjaro", "Zepbound"]},
    "dulaglutide":   {"class": "GLP-1 RA", "generic": ["dulaglutide"],
                      "brands": ["Trulicity"]},
    "exenatide":     {"class": "GLP-1 RA", "generic": ["exenatide"],
                      "brands": ["Byetta", "Bydureon"]},
    "lixisenatide":  {"class": "GLP-1 RA", "generic": ["lixisenatide"],
                      "brands": ["Adlyxin", "Lyxumia"]},
    "albiglutide":   {"class": "GLP-1 RA", "generic": ["albiglutide"],
                      "brands": ["Tanzeum", "Eperzan"]},
    "efpeglenatide": {"class": "GLP-1 RA", "generic": ["efpeglenatide"],
                      "brands": []},
    # --- comparators ---
    "empagliflozin": {"class": "SGLT2i", "generic": ["empagliflozin"],
                      "brands": ["Jardiance"]},
    "dapagliflozin": {"class": "SGLT2i", "generic": ["dapagliflozin"],
                      "brands": ["Farxiga", "Forxiga"]},
    "canagliflozin": {"class": "SGLT2i", "generic": ["canagliflozin"],
                      "brands": ["Invokana"]},
    "sitagliptin":   {"class": "DPP-4i", "generic": ["sitagliptin"],
                      "brands": ["Januvia"]},
    "linagliptin":   {"class": "DPP-4i", "generic": ["linagliptin"],
                      "brands": ["Tradjenta"]},
    "saxagliptin":   {"class": "DPP-4i", "generic": ["saxagliptin"],
                      "brands": ["Onglyza"]},
}

GLP1_RAS = [k for k, v in DRUGS.items() if "GLP-1" in v["class"]]
SGLT2 = [k for k, v in DRUGS.items() if v["class"] == "SGLT2i"]
DPP4 = [k for k, v in DRUGS.items() if v["class"] == "DPP-4i"]

# MedDRA SMQ "Suicide/self-injury" (narrow) — Preferred Terms present in FAERS.
SMQ_SUICIDE = [
    "Suicidal ideation", "Suicide attempt", "Completed suicide",
    "Suicidal behaviour", "Suicidal depression", "Depression suicidal",
    "Intentional self-injury", "Self-injurious behaviour",
    "Self-injurious ideation", "Intentional overdose",
    "Multiple drug overdose intentional", "Poisoning deliberate",
    "Self-mutilation",
]
# Broader mood/anxiety outcomes (kept separate from the suicide SMQ).
DEPRESSION_PTS = [
    "Depression", "Major depression", "Depressed mood",
    "Depressive symptom", "Persistent depressive disorder",
]
ANXIETY_PTS = [
    "Anxiety", "Anxiety disorder", "Generalised anxiety disorder",
    "Panic attack", "Panic disorder", "Nervousness",
]
OUTCOMES = {
    "suicide_selfinjury": SMQ_SUICIDE,   # primary SMQ-aligned composite
    "depression": DEPRESSION_PTS,
    "anxiety": ANXIETY_PTS,
}

QUALIFICATION = {"1": "physician", "2": "pharmacist", "3": "other_HP",
                 "4": "lawyer", "5": "consumer_non_HP"}

# Co-medication classes for confounding-by-indication probing.
# Matched on generic_name substrings against co-reported drugs.
COMED_CLASSES = {
    "antidepressant": ["sertraline", "fluoxetine", "escitalopram", "citalopram",
                       "paroxetine", "venlafaxine", "duloxetine", "bupropion",
                       "mirtazapine", "amitriptyline", "trazodone"],
    "benzodiazepine": ["alprazolam", "lorazepam", "diazepam", "clonazepam",
                       "temazepam", "midazolam"],
}

# ---------------------------------------------------------------------------
# Low-level query layer (retry + optional on-disk cache)
# ---------------------------------------------------------------------------
_CACHE: dict = {}

def _get(params: dict, retries: int = 4, pause: float = 1.0) -> dict:
    """Raw GET against openFDA. Returns parsed JSON; {'_zero': True} on 404."""
    if API_KEY:
        params = {**params, "api_key": API_KEY}
    key = urllib.parse.urlencode(sorted(params.items()))
    if key in _CACHE:
        return _CACHE[key]
    url = BASE + "?" + urllib.parse.urlencode(params)
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=45) as r:
                out = json.loads(r.read())
            _CACHE[key] = out
            return out
        except urllib.error.HTTPError as e:
            if e.code == 404:                 # openFDA: no matching records
                out = {"_zero": True}
                _CACHE[key] = out
                return out
            last = e
            time.sleep(pause * (2 ** i))      # 429/5xx -> exponential backoff
        except urllib.error.URLError as e:
            last = e
            time.sleep(pause * (2 ** i))
    raise RuntimeError(f"openFDA query failed after {retries} tries: {last}")

def _or(field: str, values) -> str:
    """('generic_name', ['a','b']) -> 'field:("a" OR "b")'."""
    vals = " OR ".join(f'"{v}"' for v in values)
    return f'{field}:({vals})'

def count_total(search: str) -> int:
    """Total report count for a Lucene search string ('' = whole DB)."""
    j = _get({"search": search, "limit": 1} if search else {"limit": 1})
    if j.get("_zero"):
        return 0
    return j["meta"]["results"]["total"]

# ---------------------------------------------------------------------------
# Query builders
# ---------------------------------------------------------------------------

def drug_clause(drug: str, suspect_only: bool = False) -> str:
    """Lucene clause matching any generic token for a drug key (or raw token)."""
    generics = DRUGS.get(drug, {}).get("generic", [drug])
    clause = _or("patient.drug.openfda.generic_name", generics)
    if suspect_only:
        clause = f'({clause}) AND patient.drug.drugcharacterization:1'
    return clause

def outcome_clause(outcome: str) -> str:
    """Lucene clause for a named outcome set (key of OUTCOMES) or single PT."""
    pts = OUTCOMES.get(outcome, [outcome])
    return _or("patient.reaction.reactionmeddrapt.exact", pts)

def build_search(drug=None, outcome=None, date_range=None, suspect_only=False,
                 extra=None) -> str:
    """Compose a full Lucene search string from components."""
    parts = []
    if drug:
        parts.append(f"({drug_clause(drug, suspect_only)})")
    if outcome:
        parts.append(f"({outcome_clause(outcome)})")
    if date_range:
        parts.append(f"receivedate:[{date_range[0]} TO {date_range[1]}]")
    if extra:
        parts.append(f"({extra})")
    return " AND ".join(parts)

# ---------------------------------------------------------------------------
# Disproportionality
# ---------------------------------------------------------------------------

def _z(p): return 1.959963984540054  # 95% normal quantile

def disproportionality(drug, outcome, background="full", date_range=None,
                       suspect_only=False):
    """
    2x2 disproportionality for drug x outcome.

    background:
      "full"                -> whole-DB background (classic FAERS)
      list of drug keys     -> restrict background to those drugs (e.g. SGLT2+DPP4)
                               => confounding-by-indication-controlled signal

    Returns dict with a,b,c,d, PRR, ROR (+95% CI), IC (+IC025), chi2_yates,
    and a signal flag (Evans: PRR>=2, chi2>=4, a>=3).
    """
    drug_s = f"({drug_clause(drug, suspect_only)})"
    out_s = f"({outcome_clause(outcome)})"
    date_s = f"receivedate:[{date_range[0]} TO {date_range[1]}]" if date_range else None

    def AND(*cl): return " AND ".join(c for c in cl if c)

    if background == "full":
        bg_s = None
    else:                                   # comparator-restricted background
        toks = []
        for dk in background:
            toks += DRUGS.get(dk, {}).get("generic", [dk])
        bg_drug = f'({_or("patient.drug.openfda.generic_name", toks)})'
        # universe = drug-of-interest OR comparator set
        bg_s = f'({drug_s} OR {bg_drug})'

    universe = bg_s if bg_s else None
    a = count_total(AND(drug_s, out_s, date_s))
    a_b = count_total(AND(drug_s, date_s))
    if universe:
        a_c = count_total(AND(universe, out_s, date_s))
        n = count_total(AND(universe, date_s))
    else:
        a_c = count_total(AND(out_s, date_s)) if (out_s or date_s) else count_total("")
        n = count_total(date_s) if date_s else count_total("")

    b = a_b - a
    c = a_c - a
    d = n - a - b - c
    res = {"drug": drug, "outcome": outcome,
           "background": "full-DB" if background == "full" else "+".join(background),
           "date_range": date_range, "suspect_only": suspect_only,
           "a": a, "b": b, "c": c, "d": d, "n": n}

    if min(a, b, c, d) <= 0:
        res.update({"PRR": None, "ROR": None, "note": "empty cell; estimates unstable"})
        # Haldane-Anscombe 0.5 correction for CI stability
        aa, bb, cc, dd = a + .5, b + .5, c + .5, d + .5
    else:
        aa, bb, cc, dd = a, b, c, d

    prr = (aa / (aa + bb)) / (cc / (cc + dd))
    ror = (aa * dd) / (bb * cc)
    se_ln_ror = math.sqrt(1/aa + 1/bb + 1/cc + 1/dd)
    ror_lo = math.exp(math.log(ror) - _z(.95) * se_ln_ror)
    ror_hi = math.exp(math.log(ror) + _z(.95) * se_ln_ror)
    # PRR CI (Gravel): SE(ln PRR) = sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d))
    se_ln_prr = math.sqrt(1/aa - 1/(aa+bb) + 1/cc - 1/(cc+dd))
    prr_lo = math.exp(math.log(prr) - _z(.95) * se_ln_prr)
    prr_hi = math.exp(math.log(prr) + _z(.95) * se_ln_prr)
    # Information Component (BCPNN-style, MGPS-lite)
    expected = (aa + bb) * (aa + cc) / (aa + bb + cc + dd)
    ic = math.log2(aa / expected)
    se_ic = math.sqrt((1/aa) / (math.log(2) ** 2))
    ic025 = ic - _z(.95) * se_ic
    # chi-square with Yates continuity correction
    N = aa + bb + cc + dd
    chi2 = (N * (abs(aa*dd - bb*cc) - N/2) ** 2) / ((aa+bb)*(cc+dd)*(aa+cc)*(bb+dd))

    res.update({
        "PRR": round(prr, 3), "PRR_lo": round(prr_lo, 3), "PRR_hi": round(prr_hi, 3),
        "ROR": round(ror, 3), "ROR_lo": round(ror_lo, 3), "ROR_hi": round(ror_hi, 3),
        "IC": round(ic, 3), "IC025": round(ic025, 3),
        "chi2_yates": round(chi2, 2),
        "signal_evans": bool(prr >= 2 and chi2 >= 4 and a >= 3),
        "signal_ror": bool(ror_lo > 1 and a >= 3),
        "signal_ic": bool(ic025 > 0),
    })
    return res

# ---------------------------------------------------------------------------
# Time trend (notoriety-bias probe)
# ---------------------------------------------------------------------------

def time_trend(drug, outcome=None, start="20180101", end="20251231",
               interval="month"):
    """
    Report counts over time via openFDA count on receivedate.
    Returns list of {date, count}. Use to visualize the post-July-2023 surge.
    """
    search = build_search(drug=drug, outcome=outcome, date_range=(start, end))
    field = "receivedate" if interval == "day" else f"receivedate"
    j = _get({"search": search, "count": field})
    if j.get("_zero"):
        return []
    rows = j["results"]  # each {time:'YYYYMMDD', count:n}
    if interval == "month":
        agg = {}
        for r in rows:
            ym = r["time"][:6]
            agg[ym] = agg.get(ym, 0) + r["count"]
        return [{"date": k, "count": v} for k, v in sorted(agg.items())]
    if interval == "year":
        agg = {}
        for r in rows:
            y = r["time"][:4]
            agg[y] = agg.get(y, 0) + r["count"]
        return [{"date": k, "count": v} for k, v in sorted(agg.items())]
    return [{"date": r["time"], "count": r["count"]} for r in rows]

# ---------------------------------------------------------------------------
# Report-source & co-medication profiling (confounder probes)
# ---------------------------------------------------------------------------

def source_qualification(drug, outcome=None, date_range=None):
    """Consumer vs clinician split (primarysource.qualification)."""
    search = build_search(drug=drug, outcome=outcome, date_range=date_range)
    j = _get({"search": search, "count": "primarysource.qualification"})
    if j.get("_zero"):
        return {}
    return {QUALIFICATION.get(str(r["term"]), str(r["term"])): r["count"]
            for r in j["results"]}

# ---------------------------------------------------------------------------
# Case-level retrieval + LLM-adjudication substrate
# ---------------------------------------------------------------------------

def fetch_cases(drug, outcome=None, date_range=None, max_cases=1000,
                page=100, suspect_only=False):
    """
    Page through full case objects for drug (x outcome x date). openFDA caps
    skip at 25000 and limit at 1000/page (we use <=100). Returns list of raw
    report dicts.
    """
    search = build_search(drug=drug, outcome=outcome, date_range=date_range,
                          suspect_only=suspect_only)
    out, skip = [], 0
    while len(out) < max_cases:
        j = _get({"search": search, "limit": min(page, max_cases - len(out)),
                  "skip": skip})
        if j.get("_zero"):
            break
        res = j.get("results", [])
        if not res:
            break
        out.extend(res)
        skip += len(res)
        if skip >= j["meta"]["results"]["total"] or skip >= 25000:
            break
    return out[:max_cases]

def _first(x):
    return x[0] if isinstance(x, list) and x else (x if isinstance(x, str) else None)

def case_substrate(report, drug):
    """
    Distill one raw FAERS report into the structured fields that inform causal
    adjudication — the signal the flat PT-count discards. Returns a compact
    dict suitable for LLM review.

    Fields:
      indication     why the GLP-1 drug was given (drugindication) -> confounding-by-indication
      action_taken   actiondrug (1 withdrawn,2 dose-reduced,... ) -> dechallenge
      dose_text      free dosage string
      reactions      list of MedDRA PTs on the case
      outcome_codes  reaction outcomes (1 recovered..5 fatal)
      comeds         co-reported generic names (psych meds flagged)
      age / sex      demographics
      source         reporter qualification (consumer vs clinician)
      country        primary source country
      serious        seriousness flag + death flag
      received       receipt date (notoriety window)
      report_id      safetyreportid (duplicate tracing)
    """
    generics = set(g.lower() for g in DRUGS.get(drug, {}).get("generic", [drug]))
    p = report.get("patient", {})
    drugs = p.get("drug", [])
    # locate the GLP-1 drug entry (for indication / action / dose)
    idx = None
    for i, d in enumerate(drugs):
        gn = d.get("openfda", {}).get("generic_name", [])
        gn = [g.lower() for g in (gn if isinstance(gn, list) else [gn])]
        if generics & set(gn) or any(g in (d.get("medicinalproduct","").lower()) for g in generics):
            idx = i; break
    dd = drugs[idx] if idx is not None else (drugs[0] if drugs else {})
    action_map = {"1":"drug withdrawn","2":"dose reduced","3":"dose increased",
                  "4":"dose not changed","5":"unknown","6":"not applicable"}
    psych = set(sum(COMED_CLASSES.values(), []))
    comeds = []
    for i, d in enumerate(drugs):
        if i == idx:
            continue
        gn = d.get("openfda", {}).get("generic_name") or [d.get("medicinalproduct","")]
        gn = gn if isinstance(gn, list) else [gn]
        for g in gn:
            gl = (g or "").lower().strip()
            if gl:
                flag = next((cls for cls, toks in COMED_CLASSES.items()
                             if any(t in gl for t in toks)), None)
                comeds.append({"drug": g, "psych_class": flag})
    return {
        "report_id": report.get("safetyreportid"),
        "received": report.get("receivedate"),
        "country": report.get("primarysourcecountry"),
        "source": QUALIFICATION.get(str(report.get("primarysource", {}).get("qualification")), "unknown"),
        "serious": report.get("serious"),
        "death": report.get("seriousnessdeath"),
        "age": p.get("patientonsetage"),
        "sex": {"1":"male","2":"female"}.get(str(p.get("patientsex")), "unknown"),
        "indication": _first(dd.get("drugindication")),
        "action_taken": action_map.get(str(dd.get("actiondrug")), None),
        "dose_text": dd.get("drugdosagetext"),
        "reactions": [r.get("reactionmeddrapt") for r in p.get("reaction", [])],
        "comeds": comeds,
        "n_comeds": len(comeds),
        "n_psych_comeds": sum(1 for c in comeds if c["psych_class"]),
    }

# Categories for LLM causal adjudication of a spontaneous report.
ADJUDICATION_CATEGORIES = [
    "plausible_drug_attributed",     # temporal + dechallenge + no dominant confounder
    "confounded_by_indication",      # prescribed for obesity/depression-linked indication
    "confounded_by_comedication",    # antidepressant/benzo co-reported, psych history implied
    "notoriety_or_legal_sourced",    # consumer/lawyer report in post-Jul-2023 window, thin clinical detail
    "duplicate_suspect",             # fields suggest overlap with another case
    "uninterpretable",               # too little structured information to judge
]

ADJUDICATION_SYSTEM = (
    "You are a pharmacovigilance reviewer adjudicating a single FAERS spontaneous "
    "adverse-event report for a GLP-1 receptor agonist and a suicide/self-injury "
    "outcome. You are given ONLY the structured case fields (no free-text narrative "
    "exists in the public data). Judge causal interpretability, not truth. "
    "Assign the SINGLE best-fitting category and a 0-1 confidence. Weigh: temporal "
    "information (drug start/end vs event), dechallenge (action_taken), the "
    "prescribing indication (confounding by indication if psychiatric or obesity-"
    "with-known-mood-link), psychiatric co-medication, reporter type and receipt "
    "date (consumer/lawyer reports in the post-July-2023 notoriety window with thin "
    "clinical detail lean toward notoriety_or_legal_sourced), and sparsity. "
    "Return STRICT JSON only: "
    '{{"category":"<one of {cats}>","confidence":<0-1>,"rationale":"<=25 words"}}'
).format(cats="|".join(ADJUDICATION_CATEGORIES))

def adjudicate_cases(substrates, model=None, max_concurrency=8, host=None):
    """
    LLM-adjudicate a list of case substrates. Requires the kernel `host` object
    (pass host=host). Returns list of {**substrate, category, confidence, rationale}.
    Uses host.llm list fan-out for parallelism.
    """
    if host is None:
        raise ValueError("pass host=host (the kernel singleton) for host.llm access")
    import json as _json
    prompts = []
    for s in substrates:
        compact = {k: s[k] for k in ("received","source","country","age","sex",
                   "indication","action_taken","dose_text","reactions",
                   "n_comeds","n_psych_comeds")}
        compact["psych_comeds"] = [c["drug"] for c in s["comeds"] if c["psych_class"]]
        prompts.append("Adjudicate this case. Fields:\n" + _json.dumps(compact, default=str))
    reqs = [{"prompt": p, "system": ADJUDICATION_SYSTEM,
             **({"model": model} if model else {})} for p in prompts]
    results = host.llm(reqs, max_concurrency=max_concurrency)
    out = []
    for s, r in zip(substrates, results):
        rec = dict(s)
        if isinstance(r, dict) and "error" in r:
            # Do NOT mask an LLM failure as a content judgment — a token-ceiling
            # or rate-limit error is not an "uninterpretable" case. Tag it
            # distinctly (category=None) so a caller can detect and re-run it.
            rec.update({"category": None, "confidence": None,
                        "rationale": "llm_error"})
        else:
            txt = (r.get("text") if isinstance(r, dict) else str(r)) or ""
            try:
                start, end = txt.find("{"), txt.rfind("}")
                parsed = _json.loads(txt[start:end+1])
                rec.update({"category": parsed.get("category", "uninterpretable"),
                            "confidence": parsed.get("confidence"),
                            "rationale": parsed.get("rationale", "")})
            except Exception:
                rec.update({"category": None, "confidence": None,
                            "rationale": "parse_error"})
        out.append(rec)
    return out

def adjudicate_with_retry(substrates, host=None, chunk=90, model=None,
                          max_concurrency=8, max_rounds=4):
    """
    Adjudicate in chunks and automatically re-run any cases that came back with
    rationale in {'llm_error','parse_error'} (category is None for those).
    Chunking keeps each host.llm batch under the 512 cap; re-running across
    rounds works around the per-frame token ceiling within a single session's
    budget. Returns (results, n_failed_final). If n_failed_final > 0, the frame
    budget is exhausted — finish the remainder in a fresh session or a delegated
    worker (each gets its own token budget).
    """
    def _run(items):
        out = []
        for i in range(0, len(items), chunk):
            out += adjudicate_cases(items[i:i+chunk], model=model,
                                    max_concurrency=max_concurrency, host=host)
        return out
    results = _run(substrates)
    by_id = {str(r["report_id"]): r for r in results}
    for _ in range(max_rounds - 1):
        failed = [s for s in substrates
                  if by_id[str(s["report_id"])]["rationale"] in ("llm_error", "parse_error")]
        if not failed:
            break
        for r in _run(failed):
            by_id[str(r["report_id"])] = r
    final = list(by_id.values())
    n_failed = sum(1 for r in final if r["rationale"] in ("llm_error", "parse_error"))
    return final, n_failed

def comedication(drug, outcome, comed_class, date_range=None):
    """
    Count of drug+outcome reports that ALSO mention a co-medication class,
    vs total drug+outcome reports. Probes confounding by co-prescription.
    """
    base = build_search(drug=drug, outcome=outcome, date_range=date_range)
    total = count_total(base)
    toks = COMED_CLASSES[comed_class]
    comed_clause = _or("patient.drug.openfda.generic_name", toks)
    with_comed = count_total(f"({base}) AND ({comed_clause})")
    return {"outcome_reports": total, f"with_{comed_class}": with_comed,
            "pct": round(100 * with_comed / total, 1) if total else None}
