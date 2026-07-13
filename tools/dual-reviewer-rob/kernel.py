"""Dual-reviewer + judge risk-of-bias harness, grounded in the official RoB2 and
ROBINS-I signalling questions, elaborations, and mapping algorithms.

Redesign notes (vs the earlier thin-prompt version):
- Each domain is scored via its OFFICIAL SIGNALLING QUESTIONS (RoB2: 22 across 5
  domains; ROBINS-I 2016: 34 across 7 domains), not a single one-line question.
- The reviewer prompt is layered: (1) general RoB instructions, (2) condensed
  study-type-specific guidance, (3) all signalling questions at once (permissive
  token budget), (4) a verbatim quote per signalling question, then a stated
  domain judgement.
- A deterministic engine recomputes the domain judgement from the signalling
  answers where the tool publishes a clean decision table (RoB2 D1, D3) and
  criteria-checks the rest, giving a machine-checkable consistency signal on top
  of the two reviewers + judge.
- Reviewer 1 defaults to Claude Opus (claude-opus-4-8), reviewer 2 and judge to
  GPT-5.6 Sol (gpt-5.6-sol), both at medium reasoning effort.

Substrate source: riskofbias.info official guidance (RoB2 22 Aug 2019;
ROBINS-I detailed guidance 20 Oct 2016). See rob_tool_substrate.json.
"""
import json, re, os, unicodedata

RATING_SCALE = {"RoB2": ["Low", "Some concerns", "High"], "ROBINS-I": ["Low", "Moderate", "Serious", "Critical", "No information"]}
RATING_RANK = {"RoB2": {"Low": 0, "Some concerns": 1, "High": 2}, "ROBINS-I": {"Low": 0, "Moderate": 1, "Serious": 2, "Critical": 3, "No information": 1}}
RESPONSE_LEGEND = {"Y": "Yes", "PY": "Probably yes", "PN": "Probably no", "N": "No", "NI": "No information", "NA": "Not applicable"}

ROB2_SQ = {
"D1": {
"name": "Bias arising from the randomization process",
"sq": {
"1.1": "Was the allocation sequence random?",
"1.2": "Was the allocation sequence concealed until participants were enrolled and assigned to interventions?",
"1.3": "Did baseline differences between intervention groups suggest a problem with the randomization process?"
}
},
"D2": {
"name": "Bias due to deviations from intended interventions (effect of assignment to intervention)",
"sq": {
"2.1": "Were participants aware of their assigned intervention during the trial?",
"2.2": "Were carers and people delivering the interventions aware of participants' assigned intervention during the trial?",
"2.3": "If Y/PY/NI to 2.1 or 2.2: Were there deviations from the intended intervention that arose because of the trial context?",
"2.4": "If Y/PY to 2.3: Were these deviations likely to have affected the outcome?",
"2.5": "If Y/PY to 2.4: Were these deviations from intended intervention balanced between groups?",
"2.6": "Was an appropriate analysis used to estimate the effect of assignment to intervention?",
"2.7": "If N/PN/NI to 2.6: Was there potential for a substantial impact (on the result) of the failure to analyse participants in the group to which they were randomized?"
}
},
"D3": {
"name": "Bias due to missing outcome data",
"sq": {
"3.1": "Were data for this outcome available for all, or nearly all, participants randomized?",
"3.2": "If N/PN/NI to 3.1: Is there evidence that the result was not biased by missing outcome data?",
"3.3": "If N/PN to 3.2: Could missingness in the outcome depend on its true value?",
"3.4": "If Y/PY/NI to 3.3: Is it likely that missingness in the outcome depended on its true value?"
}
},
"D4": {
"name": "Bias in measurement of the outcome",
"sq": {
"4.1": "Was the method of measuring the outcome inappropriate?",
"4.2": "Could measurement or ascertainment of the outcome have differed between intervention groups?",
"4.3": "If N/PN/NI to 4.1 and 4.2: Were outcome assessors aware of the intervention received by study participants?",
"4.4": "If Y/PY/NI to 4.3: Could assessment of the outcome have been influenced by knowledge of intervention received?",
"4.5": "If Y/PY/NI to 4.4: Is it likely that assessment of the outcome was influenced by knowledge of intervention received?"
}
},
"D5": {
"name": "Bias in selection of the reported result",
"sq": {
"5.1": "Were the data that produced this result analysed in accordance with a pre-specified analysis plan that was finalized before unblinded outcome data were available for analysis?",
"5.2": "Is the numerical result being assessed likely to have been selected, on the basis of the results, from multiple eligible outcome measurements within the outcome domain?",
"5.3": "Is the numerical result being assessed likely to have been selected, on the basis of the results, from multiple eligible analyses of the data?"
}
}
}

ROBINS_SQ = {
"D1": {
"name": "Bias due to confounding",
"sq": {
"1.1": "Is there potential for confounding of the effect of intervention in this study?",
"1.2": "Was the analysis based on splitting participants' follow-up time according to intervention received?",
"1.3": "Were intervention discontinuations or switches likely to be related to factors that are prognostic for the outcome?",
"1.4": "Did the authors use an appropriate analysis method that controlled for all the important confounding domains?",
"1.5": "If Y/PY to 1.4: Were confounding domains that were controlled for measured validly and reliably by the variables available in this study?",
"1.6": "Did the authors control for any post-intervention variables that could have been affected by the intervention?",
"1.7": "Did the authors use an appropriate analysis method that controlled for all the important confounding domains and for time-varying confounding?",
"1.8": "If Y/PY to 1.7: Were confounding domains that were controlled for measured validly and reliably by the variables available in this study?"
}
},
"D2": {
"name": "Bias in selection of participants into the study",
"sq": {
"2.1": "Was selection of participants into the study (or into the analysis) based on participant characteristics observed after the start of intervention?",
"2.2": "If Y/PY to 2.1: Were the post-intervention variables that influenced selection likely to be associated with intervention?",
"2.3": "If Y/PY to 2.2: Were the post-intervention variables that influenced selection likely to be influenced by the outcome or a cause of the outcome?",
"2.4": "Do start of follow-up and start of intervention coincide for most participants?",
"2.5": "If Y/PY to 2.2 and 2.3, or N/PN to 2.4: Were adjustment techniques used that are likely to correct for the presence of selection biases?"
}
},
"D3": {
"name": "Bias in classification of interventions",
"sq": {
"3.1": "Were intervention groups clearly defined?",
"3.2": "Was the information used to define intervention groups recorded at the start of the intervention?",
"3.3": "Could classification of intervention status have been affected by knowledge of the outcome or risk of the outcome?"
}
},
"D4": {
"name": "Bias due to deviations from intended interventions",
"sq": {
"4.1": "Were there deviations from the intended intervention beyond what would be expected in usual practice?",
"4.2": "If Y/PY to 4.1: Were these deviations from intended intervention unbalanced between groups and likely to have affected the outcome?",
"4.3": "Were important co-interventions balanced across intervention groups?",
"4.4": "Was the intervention implemented successfully for most participants?",
"4.5": "Did study participants adhere to the assigned intervention regimen?",
"4.6": "If N/PN to 4.3, 4.4 or 4.5: Was an appropriate analysis used to estimate the effect of starting and adhering to the intervention?"
}
},
"D5": {
"name": "Bias due to missing data",
"sq": {
"5.1": "Were outcome data available for all, or nearly all, participants?",
"5.2": "Were participants excluded due to missing data on intervention status?",
"5.3": "Were participants excluded due to missing data on other variables needed for the analysis?",
"5.4": "If PN/N to 5.1, or Y/PY to 5.2 or 5.3: Are the proportion of participants and reasons for missing data similar across interventions?",
"5.5": "If PN/N to 5.1, or Y/PY to 5.2 or 5.3: Is there evidence that results were robust to the presence of missing data?"
}
},
"D6": {
"name": "Bias in measurement of outcomes",
"sq": {
"6.1": "Could the outcome measure have been influenced by knowledge of the intervention received?",
"6.2": "Were outcome assessors aware of the intervention received by study participants?",
"6.3": "Were the methods of outcome assessment comparable across intervention groups?",
"6.4": "Were any systematic errors in measurement of the outcome related to intervention received, or associated with a factor related to intervention?"
}
},
"D7": {
"name": "Bias in selection of the reported result",
"sq": {
"7.1": "Is the reported effect estimate likely to be selected, on the basis of the results, from multiple outcome measurements within the outcome domain?",
"7.2": "Is the reported effect estimate likely to be selected, on the basis of the results, from multiple analyses of the intervention-outcome relationship?",
"7.3": "Is the reported effect estimate likely to be selected, on the basis of the results, from different subgroups?"
}
}
}

ROB2_ALGO = {
"D1": [
[
{
"1.1": "Y/PY/NI",
"1.2": "Y/PY",
"1.3": "NI/N/PN"
},
"Low"
],
[
{
"1.1": "Y/PY",
"1.2": "Y/PY",
"1.3": "Y/PY"
},
"Some concerns"
],
[
{
"1.1": "N/PN/NI",
"1.2": "Y/PY",
"1.3": "Y/PY"
},
"Some concerns"
],
[
{
"1.1": "Any",
"1.2": "NI",
"1.3": "N/PN/NI"
},
"Some concerns"
],
[
{
"1.1": "Any",
"1.2": "NI",
"1.3": "Y/PY"
},
"High"
],
[
{
"1.1": "Any",
"1.2": "N/PN",
"1.3": "Any"
},
"High"
]
],
"D3": [
[
{
"3.1": "Y/PY",
"3.2": "NA",
"3.3": "NA",
"3.4": "NA"
},
"Low"
],
[
{
"3.1": "N/PN/NI",
"3.2": "Y/PY",
"3.3": "NA",
"3.4": "NA"
},
"Low"
],
[
{
"3.1": "N/PN/NI",
"3.2": "N/PN",
"3.3": "N/PN",
"3.4": "NA"
},
"Low"
],
[
{
"3.1": "N/PN/NI",
"3.2": "N/PN",
"3.3": "Y/PY/NI",
"3.4": "N/PN"
},
"Some concerns"
],
[
{
"3.1": "N/PN/NI",
"3.2": "N/PN",
"3.3": "Y/PY/NI",
"3.4": "Y/PY/NI"
},
"High"
]
]
}

ROB2_CRITERIA = {
"D1": "See Table 4 decision tree (encoded in ROB2_ALGO['D1']).",
"D2": "Low: (blinded) OR (aware AND no trial-context deviations) AND appropriate ITT-type analysis. Some concerns: aware AND (no info on deviations OR deviations not likely to affect outcome / balanced) OR analysis inappropriate but limited impact. High: deviations likely affected outcome and unbalanced, OR inappropriate analysis with substantial impact.",
"D3": "See Table 10 decision tree (encoded in ROB2_ALGO['D3']).",
"D4": "Low: measurement not inappropriate AND did not differ between groups AND (assessors blinded OR could not be influenced). Some concerns: not inappropriate, no differential, but assessors aware though influence unlikely; OR no info on differential with blinding. High: method inappropriate OR ascertainment could differ; OR assessors aware and assessment likely influenced.",
"D5": "Low: analysed per pre-specified plan AND result not selected from multiple eligible measurements AND not from multiple eligible analyses. Some concerns: no pre-specified plan but no evidence of selection, OR no information. High: result likely selected from multiple measurements or analyses on the basis of results."
}

ROBINS_CRITERIA = {
"D1": "Low: comparable to a well-performed RCT \u2014 no confounding expected (rare in observational drug-safety). Moderate: confounding expected but ALL known important confounders appropriately measured and controlled, measured validly/reliably (no serious residual confounding expected). Serious: at least one known important confounding domain not appropriately measured or not controlled, OR measurement of a key confounder too poor (serious residual confounding). Critical: confounding inherently uncontrollable, or negative controls strongly suggest unmeasured confounding.",
"D2": "Low: all participants who would have been eligible for the target trial were included. Moderate/Serious depending on whether selection was based on post-intervention characteristics associated with intervention and outcome, whether start of follow-up and intervention coincide, and whether adjustment corrected for it.",
"D3": "Low: intervention status well defined and recorded at start of intervention, classification could not be affected by knowledge of the outcome. Serious if classification could have been influenced by outcome knowledge or is substantially misclassified.",
"D4": "Low: no deviations beyond usual practice, or deviations balanced and analysis appropriate for the effect of interest. Serious if deviations were unbalanced and likely affected the outcome, or co-interventions differed and analysis did not account for it.",
"D5": "Low: outcome data available for all/nearly all participants; no exclusions for missing intervention/covariate data, or missingness similar across groups and results robust. Serious if substantial differential missingness without evidence of robustness.",
"D6": "Low: outcome measure could not be influenced by intervention knowledge, assessors blinded or methods comparable across groups, no differential systematic error. Serious if ascertainment differed by exposure (e.g. differential surveillance) or systematic error related to intervention.",
"D7": "Low: reported estimate is the pre-specified one, not selected from multiple measurements/analyses/subgroups on the basis of results. Serious if strong indication of selective reporting from many analyses."
}

GENERAL_INSTRUCTIONS = "You are an experienced systematic-review methodologist performing a formal risk-of-bias assessment. You and a second independent reviewer are appraising the same study; a judge will later reconcile any domains where the two of you differ, using the quotes each of us provides. Work as a careful peer would: read closely, reason from the text, and be explicit about what the study does and does not report.\n\nCore principles (from the official tool guidance):\n- Assess risk of bias ONLY from the study text provided. Do not use outside knowledge of the study, the authors, or the drug class to fill gaps.\n- 'Risk of bias' means risk of MATERIAL bias: raise concern only about issues likely to affect the reliability of this study's result for the outcome being assessed.\n- The response options for each signalling question are: Yes (Y), Probably yes (PY), Probably no (PN), No (N), No information (NI), and Not applicable (NA). Use PY/PN when the text points clearly in a direction without stating it outright; use NI only when the text is genuinely silent. Critically: 'No information' is NOT the same as 'no problem' \u2014 silence is not reassurance.\n- Every signalling-question answer must be justified by a VERBATIM quote copied word-for-word from the study text. If the text is silent on that question, write exactly \"NO EVIDENCE IN TEXT\" as the quote. Never paraphrase a quote, and never invent text that is not present.\n- After answering all signalling questions for a domain, state the domain-level risk-of-bias judgement. The tool's algorithm maps signalling answers to a suggested judgement, but you may override it \u2014 if you do, say why."

STUDY_TYPE_GUIDANCE = {"RoB2": "This is a RANDOMIZED trial, assessed with the Cochrane RoB2 tool (5 domains). Frame every judgement around the specific result being assessed (here, a neuropsychiatric outcome: suicidal ideation, suicide attempt/self-harm, completed suicide, depression, or anxiety).\n- D1 Randomization: look for the sequence-generation method, allocation concealment, and baseline balance.\n- D2 Deviations (effect of assignment / ITT): look for blinding of participants and carers, trial-context deviations, and whether the analysis was intention-to-treat.\n- D3 Missing outcome data: for rare psychiatric AEs, consider differential loss to follow-up and whether spontaneous AE capture undercounts events.\n- D4 Measurement of outcome: a systematic, validated instrument (e.g. C-SSRS) applied to all participants is low-risk; reliance on spontaneous/unsolicited adverse-event reporting is a common source of bias for psychiatric outcomes. Consider assessor blinding.\n- D5 Selection of reported result: was the neuropsychiatric outcome pre-specified in a protocol/SAP, or is it a post-hoc pooled safety analysis selected from many possible analyses?", "ROBINS-I": "This is a NON-RANDOMIZED (observational) study, assessed with ROBINS-I (7 domains, 2016 structure). ROBINS-I asks how this study compares to the 'target trial' it emulates. Frame every judgement around the specific neuropsychiatric result being assessed.\n- D1 Confounding: the dominant concern is confounding by indication \u2014 patients prescribed GLP-1 RAs differ systematically (BMI, diabetes severity, baseline psychiatric history, antidepressant/benzodiazepine co-medication). Look for an active comparator (e.g. SGLT2/DPP-4 inhibitors), new-user design, and propensity/multivariable adjustment for baseline psychiatric history and comedication. Unadjusted or non-active-comparator designs are typically Serious.\n- D2 Selection of participants: prevalent-user or immortal-time bias, and selection based on post-intervention characteristics.\n- D3 Classification of interventions: was GLP-1 RA exposure defined from records BEFORE the outcome and free of misclassification (e.g. prescription vs dispensing vs adherence)?\n- D4 Deviations from intended intervention: switching/adherence and co-interventions.\n- D5 Missing data: completeness of outcome and covariate data across exposed and comparator groups; coded psychiatric diagnoses often undercount events.\n- D6 Measurement of outcomes: was the outcome ascertained comparably across groups (coded diagnoses / validated definition aligned with the MedDRA SMQ 'Suicide/self-injury'), and not differentially by exposure?\n- D7 Selection of reported result: was the reported adjusted estimate pre-specified, or selected from many analyses/subgroups?"}


# ----------------------------------------------------------------------------
# Rubric access
# ----------------------------------------------------------------------------
def get_rubric(framework):
    """Return {domain_id: {name, sq: {sq_id: text}}} for RoB2 or ROBINS-I."""
    if framework == "RoB2":
        return ROB2_SQ
    if framework in ("ROBINS-I", "ROBINS-I-2016"):
        return ROBINS_SQ
    raise ValueError("framework must be 'RoB2' or 'ROBINS-I'")


def framework_key(framework):
    return "RoB2" if framework == "RoB2" else "ROBINS-I"


# ----------------------------------------------------------------------------
# Layered reviewer prompt
# ----------------------------------------------------------------------------
def build_reviewer_prompt(framework, study_text, study_id, max_chars=48000):
    rub = get_rubric(framework)
    fk = framework_key(framework)
    scale = RATING_SCALE[fk]
    guide = STUDY_TYPE_GUIDANCE[fk]
    # Build the signalling-question block, grouped by domain
    dom_blocks = []
    schema_domains = []
    for dom, dv in rub.items():
        sq_lines = "\n".join(f"    {sid}: {stext}" for sid, stext in dv["sq"].items())
        dom_blocks.append(f"  {dom} - {dv['name']}:\n{sq_lines}")
        sq_schema = ", ".join(
            f'{{"sq": "{sid}", "answer": "<Y|PY|PN|N|NI|NA>", "quote": "<verbatim or NO EVIDENCE IN TEXT>", "note": "<=1 sentence"}}'
            for sid in dv["sq"]
        )
        schema_domains.append(
            f'{{"domain": "{dom}", "signalling": [{sq_schema}], "rating": "<one of {scale}>", "rationale": "<=2 sentences"}}'
        )
    dom_text = "\n".join(dom_blocks)
    schema = (
        '{"study_id": "%s", "framework": "%s", "domains": [%s], "overall": "<one of %s>"}'
        % (study_id, fk, ", ".join(schema_domains), scale)
    )
    text = study_text[:max_chars]
    return (
        f"{GENERAL_INSTRUCTIONS}\n\n"
        f"=== STUDY TYPE ===\n{guide}\n\n"
        f"=== TASK ===\n"
        f"Assess study '{study_id}' using the {fk} tool. Answer EVERY signalling question below "
        f"(answers: Y, PY, PN, N, NI, NA), each with a verbatim supporting quote (or 'NO EVIDENCE IN TEXT'). "
        f"Then give each domain a rating from {scale}, and an overall judgement.\n\n"
        f"=== SIGNALLING QUESTIONS ===\n{dom_text}\n\n"
        f"=== OUTPUT ===\n"
        f"Return ONLY valid JSON (no prose, no markdown fences) in EXACTLY this shape:\n{schema}\n\n"
        f"=== STUDY TEXT ===\n{text}"
    )


def parse_json_block(s):
    s = (s or "").strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\n?", "", s)
        s = re.sub(r"\n?```$", "", s)
    i = s.find("{")
    if i < 0:
        return json.loads(s)
    # Walk braces to the matching close so trailing prose after the object is ignored.
    depth = 0
    for k in range(i, len(s)):
        if s[k] == "{":
            depth += 1
        elif s[k] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(s[i:k + 1])
    return json.loads(s[i:])


# ----------------------------------------------------------------------------
# Reviewer backends
# ----------------------------------------------------------------------------
def review_claude(framework, study_text, study_id, model="claude-opus-4-8"):
    prompt = build_reviewer_prompt(framework, study_text, study_id)
    last = None
    for mt in (12000, 20000):  # full SQ output needs headroom
        r = host.llm(prompt, model=model, max_tokens=mt)
        txt = r.get("text", "") or ""
        try:
            out = parse_json_block(txt)
            out["_backend"] = f"claude:{model}"
            return out
        except Exception as e:
            last = (repr(e), r.get("stop_reason"), len(txt))
    raise RuntimeError(f"review_claude failed after retries: {last}")


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
    raise RuntimeError("no OpenAI credential found -- add one via Customize -> Credentials, or pass cred_name=")


def review_openai(framework, study_text, study_id, model="gpt-5.6-sol", cred_name=None,
                  reasoning_effort="medium"):
    """Reviewer backend: an OpenAI reasoning-model call. Default GPT-5.6 Sol at medium effort."""
    from openai import OpenAI
    client = OpenAI(api_key=openai_key(cred_name))
    prompt = build_reviewer_prompt(framework, study_text, study_id)
    is_reasoning = model.startswith(("gpt-5", "gpt-6", "o1", "o3", "o4"))
    last = None
    for budget in ((24000, 40000) if is_reasoning else (12000, 20000)):
        kw = dict(model=model, response_format={"type": "json_object"},
                  messages=[{"role": "user", "content": prompt}])
        if is_reasoning:
            kw["max_completion_tokens"] = budget
            if reasoning_effort:
                kw["reasoning_effort"] = reasoning_effort
        else:
            kw["temperature"] = 0
            kw["max_tokens"] = budget
        resp = client.chat.completions.create(**kw)
        txt = resp.choices[0].message.content or ""
        try:
            out = parse_json_block(txt)
            out["_backend"] = f"openai:{model}"
            return out
        except Exception as e:
            last = (repr(e), resp.choices[0].finish_reason, len(txt))
    raise RuntimeError(f"review_openai failed after retries: {last}")


def review(backend, framework, study_text, study_id, **kw):
    if backend == "claude":
        return review_claude(framework, study_text, study_id, model=kw.get("model", "claude-opus-4-8"))
    if backend == "openai":
        return review_openai(framework, study_text, study_id,
                             model=kw.get("model", "gpt-5.6-sol"), cred_name=kw.get("cred_name"),
                             reasoning_effort=kw.get("reasoning_effort", "medium"))
    raise ValueError("backend must be 'claude' or 'openai'")


# ----------------------------------------------------------------------------
# Deterministic algorithm recompute (RoB2 D1/D3 exact; else None)
# ----------------------------------------------------------------------------
def algo_expand(code):
    if code == "Any":
        return {"Y", "PY", "N", "PN", "NI", "NA"}
    return set(code.replace(" ", "").split("/"))


def algo_rule_match(ans, rule):
    for sq, code in rule.items():
        a = ans.get(sq)
        allowed = algo_expand(code)
        if a is None:
            if "NA" in allowed:
                continue
            return False
        if a not in allowed:
            return False
    return True


def algorithm_judgement(framework, domain, sq_answers):
    """Recompute the suggested domain judgement from signalling answers.

    Returns (judgement|None, matched_rule_index|None). Only RoB2 D1 and D3 have a
    published clean decision table; others return (None, None) and rely on the
    criteria-based judge check instead.
    """
    if framework != "RoB2":
        return (None, None)
    algo = ROB2_ALGO.get(domain)
    if not algo:
        return (None, None)
    for i, (rule, judg) in enumerate(algo):
        if algo_rule_match(sq_answers, rule):
            return (judg, i)
    return (None, None)


def cross_check_algorithm(framework, review_dict):
    """Annotate each domain with algo_rating and algo_consistent (vs the model's stated rating)."""
    for d in review_dict.get("domains", []):
        ans = {s.get("sq"): (s.get("answer") or "").strip().upper().replace("PROBABLY YES", "PY")
               for s in d.get("signalling", [])}
        # normalise common spellings
        norm = {}
        for k, v in ans.items():
            v = {"YES": "Y", "NO": "N", "PROBABLY YES": "PY", "PROBABLY NO": "PN",
                 "NO INFORMATION": "NI", "NOT APPLICABLE": "NA"}.get(v, v)
            norm[k] = v
        algo, idx = algorithm_judgement(framework, d.get("domain"), norm)
        d["algo_rating"] = algo
        d["algo_rule_index"] = idx
        d["algo_consistent"] = (algo == d.get("rating")) if algo is not None else None
    return review_dict


# ----------------------------------------------------------------------------
# Quote verification (per signalling question)
# ----------------------------------------------------------------------------
def rob_normalize_text(s):
    """Normalize text for quote matching: drop format/control chars (soft hyphens,
    zero-width spaces) and undefined codepoints that PDF extraction injects, fold
    unicode dashes to '-', NFKC-normalize, collapse whitespace, lowercase. Without
    this, faithful quotes from PDF-sourced full texts fail a naive substring check."""
    s = "".join(ch for ch in s if unicodedata.category(ch) not in ("Cf", "Cc", "Cn"))
    for d in ("\u2010", "\u2011", "\u2012", "\u2013", "\u2014"):
        s = s.replace(d, "-")
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).lower().strip()


def verify_quotes(review_dict, full_text):
    """Mark each signalling quote with quote_verified (bool|None) and verify_status
    ('verbatim' | 'ellipsis_verified' | 'unverified' | 'no_evidence').

    Verified if (a) first 120 normalized chars are a substring of the normalized
    source (verbatim), or (b) it is an ellipsis-joined quote whose every fragment
    (>15 chars) is individually verbatim. rob_normalize_text strips PDF artifacts so
    faithful quotes are not falsely flagged. 'No evidence' answers verify as None."""
    src = rob_normalize_text(full_text)
    for d in review_dict.get("domains", []):
        for s in d.get("signalling", []):
            q = (s.get("quote") or "").strip()
            if not q or q.upper().startswith("NO EVIDENCE"):
                s["quote_verified"] = None
                s["verify_status"] = "no_evidence"
                continue
            qn = rob_normalize_text(q)
            probe = qn[:120] if len(qn) > 20 else qn
            if probe in src:
                s["quote_verified"] = True
                s["verify_status"] = "verbatim"
            else:
                frags = [f for f in re.split(r"\.\.\.|\u2026", q) if len(f.strip()) > 15]
                if frags and all(rob_normalize_text(f)[:80] in src for f in frags):
                    s["quote_verified"] = True
                    s["verify_status"] = "ellipsis_verified"
                else:
                    s["quote_verified"] = False
                    s["verify_status"] = "unverified"
    return review_dict
def detect_disagreements(r1, r2, framework):
    fk = framework_key(framework)
    rank = RATING_RANK[fk]
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
            "r1_algo_consistent": a.get("algo_consistent"),
            "r2_algo_consistent": b.get("algo_consistent"),
        })
    return flags


# ----------------------------------------------------------------------------
# Judge (cross-model), on the justified signalling quotes
# ----------------------------------------------------------------------------
def domain_signalling_digest(review_dict, domain):
    for d in review_dict.get("domains", []):
        if d.get("domain") == domain:
            lines = []
            for s in d.get("signalling", []):
                vq = s.get("quote_verified")
                tag = "" if vq is None else (" [quote verified]" if vq else " [QUOTE NOT FOUND IN TEXT]")
                lines.append(f"      {s.get('sq')}: {s.get('answer')} -- \"{s.get('quote')}\"{tag}")
            return f"    rating={d.get('rating')} (algo={d.get('algo_rating')})\n" + "\n".join(lines)
    return "    (domain not rated)"


def build_judge_prompt(framework, study_id, flag, r1, r2, blind_order=None):
    """Blinded adjudication prompt. The two reviewers are presented as Reviewer A and
    Reviewer B with NO model/tool identity, in an order fixed by blind_order (a tuple
    like ('r1','r2') or ('r2','r1')); if None, defaults to (r1, r2). The judge is told
    not to infer identity and not to reward fluency/confidence/agreeableness — closing
    both the style-preference channel and (as far as possible) the identity channel."""
    fk = framework_key(framework)
    rub = get_rubric(framework)
    dom = flag["domain"]
    name = rub.get(dom, {}).get("name", dom)
    order = blind_order or ("r1", "r2")
    revmap = {"r1": r1, "r2": r2}
    revA, revB = revmap[order[0]], revmap[order[1]]
    return (
        f"You are a senior methodology adjudicator. Two independent reviewers assessed {fk} domain "
        f"{dom} ({name}) for study {study_id} and reached different domain ratings. Their assessments "
        f"appear below as Reviewer A and Reviewer B. You are NOT told which tool, model, or person "
        f"produced each, and you must not try to infer it. Decide the correct domain rating ONLY on "
        f"which rating the verbatim quotes actually support. Do not favour a reviewer for being more "
        f"fluent, more confident, more detailed, or more agreeable in style; writing quality is not "
        f"evidence. A quote flagged [QUOTE NOT FOUND IN TEXT] is unverified -- discount it. If the "
        f"verified evidence genuinely underdetermines the rating, escalate to a human.\n\n"
        f"Reviewer A:\n{domain_signalling_digest(revA, dom)}\n\n"
        f"Reviewer B:\n{domain_signalling_digest(revB, dom)}\n\n"
        f"Allowed ratings: {RATING_SCALE[fk]}\n"
        f'Return ONLY JSON: {{"resolution": "<one allowed rating> or ESCALATE_TO_HUMAN", '
        f'"reason": "<=2 sentences citing the deciding signalling question(s)>"}}'
    )


def judge(framework, study_id, flags, r1, r2, backend="claude", **kw):
    """Adjudicate disagreeing domains on the blinded, quote-grounded evidence.

    Default backend 'claude' with model 'claude-sonnet-5': a distinct third model that
    is neither reviewer's, chosen after a blinded 3-judge test showed Opus (Reviewer 1's
    model) sided with the Reviewer-1 rating 7/10 even without labels (same-model reasoning
    correlation) and escalated only 1/10, while Sonnet-5 showed no such correlation and
    escalated conservatively. The A/B presentation order is randomised per domain so the
    judge cannot even use position as a proxy for identity."""
    import random as _rnd
    out = {}
    for f in flags:
        if f["agree"]:
            continue
        order = ("r1", "r2") if _rnd.random() < 0.5 else ("r2", "r1")
        prompt = build_judge_prompt(framework, study_id, f, r1, r2, blind_order=order)
        if backend == "claude":
            r = host.llm(prompt, model=kw.get("model", "claude-sonnet-5"), max_tokens=4000)
            txt = r["text"]
        elif backend == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=openai_key(kw.get("cred_name")))
            jmodel = kw.get("model", "gpt-5.6-sol")
            jkw = dict(model=jmodel, response_format={"type": "json_object"},
                       messages=[{"role": "user", "content": prompt}])
            if jmodel.startswith(("gpt-5", "gpt-6", "o1", "o3", "o4")):
                jkw["max_completion_tokens"] = 8000
                jkw["reasoning_effort"] = kw.get("reasoning_effort", "medium")
            else:
                jkw["temperature"] = 0
            resp = client.chat.completions.create(**jkw)
            txt = resp.choices[0].message.content
        else:
            raise ValueError("judge backend must be 'claude' or 'openai'")
        try:
            out[f["domain"]] = parse_json_block(txt)
        except Exception as e:
            out[f["domain"]] = {"resolution": "ESCALATE_TO_HUMAN",
                                 "reason": f"judge output unparseable ({e!r})"}
    return out


# ----------------------------------------------------------------------------
# Audit rows: one per (study, domain, signalling question, reviewer)
# ----------------------------------------------------------------------------
def audit_rows(study_id, framework, r1, r2, flags, resolutions):
    rows = []
    fm = {f["domain"]: f for f in flags}
    rub = get_rubric(framework)
    for label, rv in (("reviewer1", r1), ("reviewer2", r2)):
        for d in rv.get("domains", []):
            dom = d["domain"]
            dname = rub.get(dom, {}).get("name", dom)
            fl = fm.get(dom, {})
            res = resolutions.get(dom) or {}
            for s in d.get("signalling", []):
                rows.append({
                    "study_id": study_id, "framework": framework, "reviewer": label,
                    "backend": rv.get("_backend"), "domain": dom, "domain_name": dname,
                    "sq": s.get("sq"), "sq_text": rub.get(dom, {}).get("sq", {}).get(s.get("sq"), ""),
                    "answer": s.get("answer"), "quote": s.get("quote"),
                    "quote_verified": s.get("quote_verified"), "verify_status": s.get("verify_status"), "sq_note": s.get("note"),
                    "domain_rating": d.get("rating"), "domain_rationale": d.get("rationale"),
                    "algo_rating": d.get("algo_rating"), "algo_consistent": d.get("algo_consistent"),
                    "agree_with_other_reviewer": fl.get("agree"),
                    "disagreement_severity": fl.get("severity"),
                    "judge_resolution": res.get("resolution"), "judge_reason": res.get("reason"),
                    "resolution_source": res.get("source", "judge" if res.get("resolution") else None),
                    "reconciled": fl.get("reconciled"), "reconcile_converged": fl.get("reconcile_converged"),
                    "overall": rv.get("overall"),
                })
    return rows




# ----------------------------------------------------------------------------
# Reconciliation round (pre-escalation rebuttal) -- hardened, anti-capitulation
# ----------------------------------------------------------------------------
def build_reconcile_prompt(framework, study_id, domain, own_review, other_review, own_label, other_label):
    """Show a reviewer the other reviewer's take on the SAME domain and invite a
    text-grounded reconsideration. Hardened against consensus-seeking leniency:
    revise only on missed evidence, and never treat unreported bias sources as
    reassurance."""
    fk = framework_key(framework)
    rub = get_rubric(framework)
    name = rub.get(domain, {}).get("name", domain)

    def digest(rev):
        d = next((x for x in rev.get("domains", []) if x.get("domain") == domain), None)
        if not d:
            return "(no rating)"
        lines = [f"    rating: {d.get('rating')}", f"    rationale: {d.get('rationale')}"]
        for s in d.get("signalling", []):
            lines.append(f"      {s.get('sq')} [{s.get('answer')}]: \"{s.get('quote')}\"")
        return "\n".join(lines)

    return (
        f"You previously assessed {fk} domain {domain} ({name}) for study {study_id}. A second, equally "
        f"experienced reviewer reached a different rating. Reconsider your rating in light of theirs.\n\n"
        f"This is a reconciliation step, NOT a negotiation. Two rules govern it:\n"
        f"1. Change your rating ONLY if the other reviewer cites text-grounded evidence you overlooked or "
        f"misread. Do NOT lower (or raise) your rating merely to reach agreement -- an unresolved genuine "
        f"disagreement is a valid outcome and is better than a false consensus.\n"
        f"2. Guard against the 'absence of evidence' fallacy in BOTH directions. A potential source of bias "
        f"the study does not report (adherence, differential co-interventions, missing-covariate handling, a "
        f"prespecified protocol) is NOT reassurance -- 'not shown to be differential' or 'not shown to be "
        f"biased' does not justify a lower rating. Unreported detail that could materially bias the result "
        f"keeps the domain at the more cautious rating, not the lenient one. Do not talk each other down.\n\n"
        f"YOUR assessment ({own_label}):\n{digest(own_review)}\n\n"
        f"COLLEAGUE's assessment ({other_label}):\n{digest(other_review)}\n\n"
        f"Allowed ratings: {RATING_SCALE[fk]}\n"
        f'Return ONLY JSON: {{"domain": "{domain}", "revised_rating": "<one allowed rating>", '
        f'"changed": <true|false>, "reason": "<=2 sentences>"}}'
    )


def reconcile_domain(framework, study_id, domain, r1, r2,
                     b1_backend="claude", b2_backend="openai", b1_kw=None, b2_kw=None):
    """One hardened rebuttal round for a disagreeing domain. Each reviewer, on its
    own backend, reconsiders given the other's rating/rationale/quotes. Returns
    {r1_revised, r2_revised, converged, resolved_to}."""
    b1_kw = b1_kw or {}; b2_kw = b2_kw or {}
    l1, l2 = r1.get("_backend", "reviewer1"), r2.get("_backend", "reviewer2")

    # Reviewer 1 reconsiders on its backend
    p1 = build_reconcile_prompt(framework, study_id, domain, r1, r2, l1, l2)
    if b1_backend == "claude":
        resp = host.llm(p1, model=b1_kw.get("model", "claude-opus-4-8"), max_tokens=2500)
        rev1 = parse_json_block(resp["text"])
    else:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key(b1_kw.get("cred_name")))
        m = b1_kw.get("model", "gpt-5.6-sol")
        kw = dict(model=m, response_format={"type": "json_object"},
                  messages=[{"role": "user", "content": p1}])
        if m.startswith(("gpt-5", "gpt-6", "o1", "o3", "o4")):
            kw["max_completion_tokens"] = 6000; kw["reasoning_effort"] = b1_kw.get("reasoning_effort", "medium")
        else:
            kw["temperature"] = 0
        rev1 = parse_json_block(client.chat.completions.create(**kw).choices[0].message.content)

    # Reviewer 2 reconsiders on its backend
    p2 = build_reconcile_prompt(framework, study_id, domain, r2, r1, l2, l1)
    if b2_backend == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=openai_key(b2_kw.get("cred_name")))
        m = b2_kw.get("model", "gpt-5.6-sol")
        kw = dict(model=m, response_format={"type": "json_object"},
                  messages=[{"role": "user", "content": p2}])
        if m.startswith(("gpt-5", "gpt-6", "o1", "o3", "o4")):
            kw["max_completion_tokens"] = 6000; kw["reasoning_effort"] = b2_kw.get("reasoning_effort", "medium")
        else:
            kw["temperature"] = 0
        rev2 = parse_json_block(client.chat.completions.create(**kw).choices[0].message.content)
    else:
        resp = host.llm(p2, model=b2_kw.get("model", "claude-opus-4-8"), max_tokens=2500)
        rev2 = parse_json_block(resp["text"])

    conv = rev1.get("revised_rating") == rev2.get("revised_rating")
    return {"r1_revised": rev1, "r2_revised": rev2, "converged": conv,
            "resolved_to": rev1.get("revised_rating") if conv else None}


# ----------------------------------------------------------------------------
# Orchestrator
# ----------------------------------------------------------------------------
def run_dual_review(study_id, full_text, framework,
                    backend1="claude", backend2="openai", judge_backend="claude",
                    reconcile=True, b1_kw=None, b2_kw=None, judge_kw=None):
    """End-to-end: two signalling-question reviewers -> quote-verify + algorithm
    cross-check -> flag disagreements -> (optional) hardened reconciliation round
    -> cross-model judge on the domains still disagreeing -> audit rows.

    reconcile=True (default): before the judge, each disagreeing domain gets ONE
    hardened rebuttal round (reconcile_domain) where each reviewer sees the other's
    rating/rationale/quotes and may revise on text-grounded evidence only. Domains
    that converge are resolved by that consensus; only domains still split go to the
    judge. The reconciliation is anti-capitulation (never downgrade to reach
    agreement, unreported bias is not reassurance), so its errors run conservative.

    Returns {study_id, framework, r1, r2, flags, reconciliation, resolutions, audit}."""
    b1_kw = b1_kw or {}; b2_kw = b2_kw or {}; judge_kw = judge_kw or {}
    r1 = cross_check_algorithm(framework, verify_quotes(
        review(backend1, framework, full_text, study_id, **b1_kw), full_text))
    r2 = cross_check_algorithm(framework, verify_quotes(
        review(backend2, framework, full_text, study_id, **b2_kw), full_text))
    flags = detect_disagreements(r1, r2, framework)

    reconciliation = {}
    if reconcile:
        for f in flags:
            if f["agree"]:
                continue
            rec = reconcile_domain(framework, study_id, f["domain"], r1, r2,
                                   b1_backend=backend1, b2_backend=backend2,
                                   b1_kw=b1_kw, b2_kw=b2_kw)
            reconciliation[f["domain"]] = rec
            f["reconciled"] = True
            f["reconcile_converged"] = rec["converged"]
            f["reconcile_resolved_to"] = rec["resolved_to"]

    # Judge only the domains still disagreeing AFTER reconciliation.
    to_judge = [f for f in flags
                if (not f["agree"]) and not reconciliation.get(f["domain"], {}).get("converged")]
    resolutions = judge(framework, study_id, to_judge, r1, r2, backend=judge_backend, **judge_kw)
    # Fold reconciliation consensus into resolutions so the audit has one resolved column.
    for dom, rec in reconciliation.items():
        if rec["converged"]:
            resolutions[dom] = {"resolution": rec["resolved_to"],
                                "reason": "Resolved by reconciliation round (both reviewers converged): "
                                          + (rec["r1_revised"].get("reason") or ""),
                                "source": "reconciliation"}
    audit = audit_rows(study_id, framework, r1, r2, flags, resolutions)
    return {"study_id": study_id, "framework": framework, "r1": r1, "r2": r2,
            "flags": flags, "reconciliation": reconciliation,
            "resolutions": resolutions, "audit": audit}


# ----------------------------------------------------------------------------
# Escalation packet (human-review queue) -- assembled from the judge's output
# ----------------------------------------------------------------------------
def build_escalation_packet(run_results, out_path=None):
    """Build a human-review packet for every domain a run sent to ESCALATE_TO_HUMAN.

    Accepts a single run_dual_review result dict or a list of them. For each escalated
    (study, domain) it emits: both reviewers' ORIGINAL and post-reconciliation ratings,
    every signalling-question answer with its verbatim quote and verify_status, the
    judge's reason (which names the deciding signalling question and what evidence is
    missing), the candidate ratings to choose between, and a blank 'Your call' line.
    The judge crafts the focus of each entry; this function lays it out.

    Returns the markdown string; also writes it to out_path if given. Returns a short
    note instead of an empty file when nothing escalated."""
    if isinstance(run_results, dict):
        run_results = [run_results]

    def dblock(rev, dom):
        return next((d for d in rev.get("domains", []) if d.get("domain") == dom), None)

    def sq_lines(d):
        out = []
        for s in d.get("signalling", []):
            st = s.get("verify_status")
            tag = {"verbatim": " [verbatim]", "ellipsis_verified": " [verbatim, ellipsis-joined]",
                   "unverified": " [NOT VERIFIED IN TEXT]", "no_evidence": ""}.get(st, "")
            q = (s.get("quote") or "").replace("\n", " ")
            out.append(f'    - **{s.get("sq")}** `[{s.get("answer")}]`{tag}: "{q}"')
        return "\n".join(out)

    blocks = []
    n = 0
    for r in run_results:
        sid = r.get("study_id"); fw = r.get("framework")
        rub = get_rubric(fw)
        recon = r.get("reconciliation", {})
        for dom, res in (r.get("resolutions") or {}).items():
            if (res or {}).get("resolution") != "ESCALATE_TO_HUMAN":
                continue
            n += 1
            name = rub.get(dom, {}).get("name", dom)
            d1 = dblock(r.get("r1", {}), dom) or {}
            d2 = dblock(r.get("r2", {}), dom) or {}
            rc = recon.get(dom, {})
            r1_rev = (rc.get("r1_revised") or {}).get("revised_rating")
            r2_rev = (rc.get("r2_revised") or {}).get("revised_rating")
            cands = sorted({x for x in (d1.get("rating"), d2.get("rating"), r1_rev, r2_rev) if x})
            blocks.append("\n".join([
                f"## {sid} - {dom} ({name})",
                "",
                f"- **Reviewer 1 ({r.get('r1', {}).get('_backend','')})**: {d1.get('rating')}"
                + (f"  ->(after reconciliation) {r1_rev}" if r1_rev and r1_rev != d1.get('rating') else ""),
                f"- **Reviewer 2 ({r.get('r2', {}).get('_backend','')})**: {d2.get('rating')}"
                + (f"  ->(after reconciliation) {r2_rev}" if r2_rev and r2_rev != d2.get('rating') else ""),
                f"- **Reconciliation**: did not converge",
                "",
                f"**Why the judge escalated (deciding question + missing evidence):**",
                f"> {res.get('reason','')}",
                "",
                f"**Reviewer 1 rationale.** {d1.get('rationale','')}",
                "",
                "Reviewer 1 signalling answers:",
                sq_lines(d1),
                "",
                f"**Reviewer 2 rationale.** {d2.get('rationale','')}",
                "",
                "Reviewer 2 signalling answers:",
                sq_lines(d2),
                "",
                f"**Candidate ratings:** {' | '.join(cands) if cands else '(see above)'}",
                f"**Your call:** ____________   **Note:** ____________",
                "",
                "---",
                "",
            ]))

    if n == 0:
        md = "# Escalation packet\n\nNo domains were escalated to human review in this run.\n"
    else:
        header = (
            "# Escalation packet - human review queue\n\n"
            f"{n} domain-cell(s) where the two reviewers disagreed, the reconciliation round "
            "failed to converge, and the blinded judge declined to resolve on the verified evidence. "
            "For each, the judge names the deciding signalling question and what evidence is missing; "
            "choose among the candidate ratings and fill in 'Your call'.\n\n"
        )
        md = header + "\n".join(blocks)
    if out_path:
        with open(out_path, "w") as fh:
            fh.write(md)
    return md
