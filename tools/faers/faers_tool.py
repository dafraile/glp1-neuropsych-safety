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
