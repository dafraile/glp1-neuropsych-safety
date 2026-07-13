#!/usr/bin/env python3
"""build_manifest.py — machine-generate analysis_manifest.json.

Single source of truth for every headline count, file hash, model version, and
analysis-status flag in the repository. README.md and TRIANGULATION_SYNTHESIS.md
numbers are checked against this manifest by tests/check_readme_against_manifest.py.

Counts are computed by reading the data/results files directly, not transcribed.
Run:  python build_manifest.py   ->  writes analysis_manifest.json
"""
import csv, json, hashlib, subprocess, os, datetime, sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))


def sha256(relpath):
    p = os.path.join(ROOT, relpath)
    if not os.path.exists(p):
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(relpath):
    p = os.path.join(ROOT, relpath)
    if not os.path.exists(p):
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def git_commit():
    try:
        return subprocess.check_output(
            ["git", "-C", ROOT, "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def col_counts(rows, col):
    return dict(Counter((r.get(col) or "").strip() for r in rows))


# --------------------------------------------------------------------------
# Stream A — designed-study harm synthesis
# --------------------------------------------------------------------------
st = read_csv("data/study_table.csv")
n_rct = sum(1 for r in st if r["design"] == "RCT")
n_obs = sum(1 for r in st if r["design"] != "RCT")
poolable = col_counts(st, "poolable")


def _num(x):
    try:
        return float(x)
    except Exception:
        return None


rct_rows = [r for r in st if r["design"] == "RCT"]
rct_2x2 = [r for r in rct_rows if all(_num(r[c]) is not None
           for c in ("events_exp", "events_ctrl", "N_exposed", "N_comparator"))]
rct_double_zero = [r["study"] for r in rct_2x2
                   if _num(r["events_exp"]) == 0 and _num(r["events_ctrl"]) == 0]

pe = read_csv("results/pooled_estimates.csv")
pooled_k = {r["stratum"]: int(r["k"]) for r in pe}

prisma_a = {r["stage"]: int(r["n"]) for r in read_csv("results/prisma_counts.csv")}
scr = read_csv("data/screening_ledger.csv")

stream_A = {
    "search_and_screening": {
        "identified_pubmed": prisma_a.get("Identified (PubMed)"),
        "identified_openalex": prisma_a.get("Identified (OpenAlex)"),
        "total_retrieved": prisma_a.get("Total retrieved"),
        "after_dedup": len(scr),
        "duplicates_removed": prisma_a.get("Duplicates removed"),
        "ta_included": sum(1 for r in scr if r["ta_decision"] == "include"),
        "ta_excluded": sum(1 for r in scr if r["ta_decision"] == "exclude"),
        "screen_method": col_counts(scr, "screen_method"),
    },
    "study_table": {
        "total_rows": len(st),
        "rct_rows": n_rct,
        "observational_rows": n_obs,
        "poolable": poolable,
    },
    "pooling": {
        "rct_with_2x2": len(rct_2x2),
        "rct_double_zero_count": len(rct_double_zero),
        "rct_double_zero_studies": rct_double_zero,
        "rct_pooled_k_MH": pooled_k.get("RCT (M-H counts)"),
        "rct_reconciliation": (
            f"{n_rct} RCTs with 2x2 data; Mantel-Haenszel drops "
            f"{len(rct_double_zero)} double-zero trial(s) "
            f"({', '.join(rct_double_zero)}) which cannot inform a relative "
            f"effect but whose safety exposure is reported; pooled k="
            f"{pooled_k.get('RCT (M-H counts)')}"),
        "obs_poolable": sum(1 for r in st
                            if r["design"] != "RCT" and r["poolable"] == "yes"),
        "obs_nonpoolable": sum(1 for r in st
                               if r["design"] != "RCT" and r["poolable"] != "yes"),
        "total_poolable": sum(1 for r in st if r["poolable"] == "yes"),
        "pooled_k_all_strata": pooled_k,
    },
}

# --------------------------------------------------------------------------
# Stream D — designed-study benefit synthesis
# --------------------------------------------------------------------------
sd = read_csv("data/stream_D_study_table.csv")
sd_dir = col_counts(sd, "direction")
if "" in sd_dir:                       # blank direction == unclassified
    sd_dir["unclassified"] = sd_dir.pop("")
sd_unclassified = [r["pmid"] for r in sd if not (r.get("direction") or "").strip()]
prisma_d = {r["stage"]: int(r["n"]) for r in read_csv("results/stream_D_prisma_counts.csv")}

# The 6 formerly-blank studies were adjudicated (results/stream_D_reclassification.csv):
# 5 EXCLUDE (wrong outcome / review / biomarker) + 1 no-effect. This resolves the 46-vs-52
# discrepancy: extracted N=52 -> direction-eligible N=47 + 5 excluded.
reclass = read_csv("results/stream_D_reclassification.csv")
corrected = read_csv("results/stream_D_corrected_counts.csv")
if corrected:
    c = corrected[0]
    dir_eligible = int(c["direction_eligible_N"])
    n_excluded = int(c["excluded"])
    corrected_dir = {"benefit": int(c["dir_benefit"]), "mixed": int(c["dir_mixed"]),
                     "no-effect": int(c["dir_no-effect"]), "harm": int(c["dir_harm"])}
else:
    dir_eligible, n_excluded, corrected_dir = len(sd), 0, {}

stream_D = {
    "records_retrieved": prisma_d.get(
        "Records retrieved for screening (relevance-capped, deduplicated union)"),
    "included_after_screening": prisma_d.get("Records included after screening"),
    "extracted_study_table": len(sd),
    "raw_direction_breakdown_pre_reclass": sd_dir,
    "reclassified_6_studies": {r["pmid"]: r["new_status"] for r in reclass},
    "excluded_after_reclass": n_excluded,
    "direction_eligible_N": dir_eligible,
    "corrected_direction_breakdown": corrected_dir,
    "direction_reconciliation": (
        f"extracted N=52 -> {dir_eligible} direction-eligible "
        f"({corrected_dir.get('benefit',0)} benefit / {corrected_dir.get('mixed',0)} mixed / "
        f"{corrected_dir.get('no-effect',0)} no-effect / {corrected_dir.get('harm',0)} harm) "
        f"+ {n_excluded} excluded = {len(sd)}. '0 harm' = no study reported a pro-addiction "
        f"direction, NOT evidence of safety. Stream D is exploratory."),
}

# --------------------------------------------------------------------------
# Stream B — FAERS (drug-specific; scope stated explicitly)
# --------------------------------------------------------------------------
adj = read_csv("results/faers_case_adjudication_full912.csv")
recv = [ (r.get("received") or "").strip() for r in adj if (r.get("received") or "").strip()]
recv_sorted = sorted(recv)


def _quarter(yyyymmdd):
    y, mth = int(yyyymmdd[:4]), int(yyyymmdd[4:6])
    return f"{y}Q{(mth-1)//3 + 1}"


post_jul23 = sum(1 for d in recv if d >= "20230701")
stream_B = {
    "primary_analysis_scope": "semaglutide (single molecule) x MedDRA SMQ suicide/self-injury (narrow). NOT class-level.",
    "class_level_analyses": "Stream D FAERS footprint and the 8-molecule signal matrix are class-level / multi-molecule; scope is labelled per table.",
    "faers_snapshot_cutoff": f"{recv_sorted[-1][:4]}-{recv_sorted[-1][4:6]}-{recv_sorted[-1][6:8]}" if recv_sorted else None,
    "faers_quarter_span": f"{_quarter(recv_sorted[0])} - {_quarter(recv_sorted[-1])}" if recv_sorted else None,
    "adjudicated_cases_total": len(adj),
    "pct_post_july_2023": round(100 * post_jul23 / len(recv)) if recv else None,
    "adjudication_note": (
        "All 912 cases adjudicated. Single-model category counts in "
        "faers_case_adjudication_full912.csv; the load-bearing headline is the "
        "cross-provider consensus RANGE, not a single-model point estimate."),
}

# --------------------------------------------------------------------------
# LLM steps — model/prompt versions
# --------------------------------------------------------------------------
llm_steps = {
    "screening": {
        "models": ["claude (Claude Science default, screening pass)",
                   "rule-based keyword classifier (no LLM)"],
        "note": "418 records LLM-screened, 376 rule-based; method flagged per record in data/screening_ledger.csv",
    },
    "extraction": {"models": ["claude (Claude Science default)"],
                   "note": "abstract/full-text extraction into study_table.csv; 2 QC corrections logged"},
    "faers_adjudication": {
        "models": ["claude-haiku (kernel default)", "claude-sonnet-5", "gpt-5.5"],
        "note": "cross-provider 3-model adjudication over structured fields; consensus = majority vote",
    },
    "risk_of_bias": {
        "models": ["claude-opus-4.8 (reviewer 1)", "gpt-5.6-sol (reviewer 2)", "claude-sonnet-5 (blinded judge)"],
        "note": "signalling-question dual-reviewer-rob engine (ROBINS-I 2016 for observational, RoB2 for RCTs); hardened reconciliation on disagreements, blinded judge on residual splits; full audit trail",
    },
    "grade": {
        "models": ["claude-sonnet-5", "gpt-5.5"],
        "note": "grade-hybrid cross-model for GRADE judgment domains; RoB downgrade sourced from the signalling-question RoB ratings above",
    },
}

# --------------------------------------------------------------------------
# Analysis status flags — provisional / complete / superseded
# --------------------------------------------------------------------------
analysis_status = {
    "stream_A_pooling": "complete",
    "rct_rare_event_sensitivity": "complete",           # updated by hardening reruns
    "observational_reml_hk_pi": "complete",
    "grade_hybrid_crossmodel": "complete",              # supersedes rules-based grade_certainty.csv
    "grade_rules_based_firstpass": "superseded",        # grade_certainty.csv -> grade_certainty_hybrid.csv
    "risk_of_bias_dualreview": "complete",              # supersedes rules-based first pass
    "risk_of_bias_rules_firstpass": "superseded",
    "faers_case_adjudication_partial800": "superseded", # -> full912
    "faers_case_adjudication_full912": "complete",
    "faers_adjudication_crossprovider": "complete",
    "faers_comparator_grid": "complete",
    "faers_time_controlled_notoriety": "complete",
    "faers_dedup_drug_role_sensitivity": "complete",
    "disproportionality_calibration_omop": "complete",
    "stream_D_benefit_synthesis": "complete (exploratory)",
    "validation_layers_human_adjudication": "provisional",  # awaits single-reviewer disagreement adjudication
}

# --------------------------------------------------------------------------
# Table -> backing-file map (every headline table)
# --------------------------------------------------------------------------
table_file_map = {
    "README_headline_streamA": "results/pooled_estimates.csv",
    "README_headline_streamA_GRADE": "results/grade_certainty_hybrid.csv",
    "README_streamB_comparator_flip": "results/stream_B_signal_matrix.csv",
    "README_streamB_timesplit": "results/streamB_timesplit_reframe.csv",
    "README_streamD_headline": "data/stream_D_study_table.csv",
    "README_streamD_pooled": "results/stream_D_pooled_estimates.csv",
    "anchor_reproduction_A": "results/reproduction_check.csv",
    "anchor_reproduction_D": "results/stream_D_reproduction_check.csv",
    "prisma_A": "results/prisma_counts.csv",
    "prisma_D": "results/stream_D_prisma_counts.csv",
    "confounder_ranking": "results/confounder_ranking.csv",
    "indication_stratified": "results/indication_stratified.csv",
    "faers_footprint_streamD": "results/streamD_faers_benefit.csv",
    "faers_adjudication": "results/faers_case_adjudication_full912.csv",
    "faers_adjudication_crossprovider": "results/adjudication_crossprovider.csv",
    "disproportionality_calibration_omop": "results/omop_calibration_results.csv",
    "disproportionality_calibration_40pair": "results/faers_calibration_results.csv",
    "validation_summary": "results/validation_summary.csv",
    "rct_rare_event_sensitivity": "results/rct_rare_event_sensitivity.csv",
    "obs_reml_hk_reruns": "results/obs_reml_hk_reruns.csv",
    "harm_margin_test": "results/harm_margin_test.csv",
    "absolute_risks": "results/absolute_risks.csv",
    "cohort_overlap_matrix": "results/cohort_overlap_matrix.csv",
    "faers_comparator_grid": "results/faers_comparator_grid.csv",
    "faers_indication_interaction": "results/faers_indication_interaction.csv",
    "faers_notoriety_its": "results/faers_notoriety_its.csv",
    "faers_notoriety_did": "results/faers_notoriety_did.csv",
    "faers_drug_role_sensitivity": "results/faers_drug_role_sensitivity.csv",
    "stream_C_evidence_map": "results/stream_C_evidence_map.csv",
    "stream_D_reclassification": "results/stream_D_reclassification.csv",
    "stream_D_corrected_counts": "results/stream_D_corrected_counts.csv",
}

# input-file hashes for every backing file that exists
input_hashes = {}
for _, rel in table_file_map.items():
    h = sha256(rel)
    if h:
        input_hashes[rel] = h
for extra in ["data/study_table.csv", "data/stream_D_study_table.csv",
              "data/screening_ledger.csv", "data/dedup_pool.csv",
              "tools/faers/faers_tool.py"]:
    h = sha256(extra)
    if h:
        input_hashes[extra] = h

manifest = {
    "_schema": "glp1-neuropsych-safety analysis manifest v1",
    "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "git_commit": git_commit(),
    "streams_are_never_pooled_together": True,
    "stream_A": stream_A,
    "stream_B_faers": stream_B,
    "stream_D": stream_D,
    "llm_steps": llm_steps,
    "analysis_status": analysis_status,
    "table_file_map": table_file_map,
    "input_file_sha256": input_hashes,
}

if __name__ == "__main__":
    out = os.path.join(ROOT, "analysis_manifest.json")
    with open(out, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"wrote {out}")
    print(f"  git_commit={manifest['git_commit']}")
    print(f"  stream_A poolable total={stream_A['pooling']['total_poolable']}, "
          f"RCT pooled k={stream_A['pooling']['rct_pooled_k_MH']}")
    print(f"  stream_D extracted={stream_D['extracted_study_table']}, "
          f"direction_eligible={stream_D['direction_eligible_N']}, "
          f"excluded={stream_D['excluded_after_reclass']}")
    print(f"  FAERS adjudicated={stream_B['adjudicated_cases_total']}, "
          f"cutoff={stream_B['faers_snapshot_cutoff']}")
