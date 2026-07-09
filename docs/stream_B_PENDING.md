# Stream B — pending work (next session)

## Case adjudication: 112 of 912 cases remaining
The LLM case-adjudication run completed 800/912 semaglutide x suicide/self-injury
reports before hitting this session's per-frame LLM token ceiling (2.0M) and with
delegation toggled off. The 800 done are 2018–mid-2025; the missing 112 are the
2025–2026 cases (fetch_cases pages oldest-first).

IMPORTANT: because the missing cases are the most RECENT, the notoriety_or_legal_sourced
category is UNDER-counted in the partial-800 result. The notoriety conclusion in the
confounder ranking is therefore drawn from the full-912 time trend (87% of reports
post-July-2023), NOT from the adjudication counts.

### To finish
Substrates for the 112 are saved in the workspace as handoff_missing112.json (regenerable
via ft.fetch_cases). Either enable delegation, or run in a fresh session:
    ft = load_faers_tool()
    import json; missing = json.load(open("handoff_missing112.json"))
    adj = []
    for i in range(0, len(missing), 100):
        adj += ft.adjudicate_cases(missing[i:i+100], host=host, max_concurrency=8)
Then concat with results/faers_case_adjudication_partial800.csv -> full 912, and
regenerate figures/faers_adjudication.png with the full set.

## FOIA narratives (user pursuing)
openFDA exposes no free-text narrative. Real narrative NLP needs the raw FAERS
quarterly files / MedWatch source docs via FOIA. When obtained, the narrative text
becomes a new adjudication input alongside the structured substrate — the
adjudicate_cases prompt can be extended to consume it.
