# Stream B — FAERS spontaneous-report disproportionality

**Kept strictly separate from Stream A. Not pooled with designed studies.**
Spontaneous reporting proportions are hypothesis-generating signals, not
incidence or risk. This stream exists to *compare* the spontaneous signal
against the designed-study estimate, and to quantify how much of it is an
artifact of comparator choice, notoriety, and confounding by indication.

## Tool

`tools/faers/faers_tool.py` — a self-contained openFDA `drug/event` client
(stdlib only, no API key required). Provides:

- Controlled vocabularies: 8 GLP-1 RAs + SGLT2i / DPP-4i comparators; outcomes
  standardized to the MedDRA SMQ "Suicide/self-injury" narrow PT set, plus
  depression and anxiety composites (aligned with Stream A outcome defs).
- `disproportionality(drug, outcome, background=...)` — 2x2 with PRR, ROR, IC
  (all 95% CI), Yates chi-square, and Evans/ROR/IC signal flags. `background`
  is either `"full"` (whole-DB) **or a comparator drug list** — the latter
  gives a confounding-by-indication-controlled signal.
- Confounder probes: `time_trend()` (notoriety), `source_qualification()`
  (consumer vs clinician), `comedication()` (antidepressant/benzodiazepine).

The tool is disease/event-agnostic: any drug list x any MedDRA PT set works,
so it is reusable beyond this project.

## Headline result — the signal is a function of the comparator

Semaglutide x suicide/self-injury SMQ (a = 912 reports):

| Background | ROR (95% CI) | Signal? |
|---|---|---|
| Full FAERS database | 0.77 (0.73-0.83) | No (null-to-protective) |
| SGLT2i + DPP-4i comparators | 2.08 (1.91-2.26) | Yes |

Same numerator, opposite conclusion. Among all GLP-1 RAs, **only semaglutide**
crosses into signal territory under the comparator background; liraglutide,
tirzepatide, dulaglutide, and exenatide do not (see `results/stream_B_signal_matrix.csv`).

The monthly report trend peaks in **August 2023**, immediately after the
July 2023 EMA/FDA review announcements — consistent with notoriety bias.
Consumer-sourced reports (441) outnumber physician reports (231) for the
suicide outcome, and 16.8% co-report an antidepressant.

## Triangulation vs Stream A

`figures/triangulation_forest.png` co-displays Stream A pooled estimates and
Stream B spontaneous signals on **one shared log-ratio axis but in separate,
unpooled bands**. Designed studies (RCT RR 0.84; observational adjusted ratios
0.71-0.94) are null-to-protective; the FAERS signal is positive *only* under
the comparator background. The divergence — not a single pooled number — is
the result.

## Files
```
tools/faers/faers_tool.py          the extraction / disproportionality client
results/stream_B_signal_matrix.csv 8 drugs x 3 outcomes x 2 backgrounds, RORs + flags
figures/faers_demo.png             semaglutide signal flip + notoriety time trend
figures/triangulation_forest.png   Stream A vs Stream B co-display (unpooled bands)
```

## Caveats
openFDA returns FAERS in normalized public form; it does **not** de-duplicate
overlapping case versions the way a full quarterly-file pipeline would, and
drug matching inherits openFDA SPL normalization. Absolute counts are for
signal comparison, not incidence. Disproportionality cannot establish causation.
