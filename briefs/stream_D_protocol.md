# Stream D — Cross-Addiction Benefit/Reward Evidence Synthesis (Protocol)

**Project:** Triangulating the GLP-1 neuropsychiatric safety signal.
**Stream D role:** The *benefit* counterpart to Stream A's *harm* synthesis. The same
GLP-1R mesolimbic reward pathway invoked to explain a feared neuropsychiatric harm signal
also underlies emerging efficacy for addiction/craving reduction. Stream D applies the
**same designed-study machinery** (dual-review RoB + hybrid GRADE + anchor reproduction)
to the benefit outcomes, so the two sides of the paradox are held to one evidentiary bar.

> **Stream separation (hard constraint).** Stream D is never pooled with Stream A
> (neuropsychiatric harm), Stream B (FAERS spontaneous reports), or Stream C (mechanism).
> Within Stream D, estimates are never pooled across substances or across designs.

## PICO

- **P** — Adults exposed to a GLP-1 receptor agonist. Track indication where reported
  (obesity / T2D / addiction-primary). Include populations with a target addictive
  behaviour (AUD, tobacco use disorder, gambling disorder) or general populations with
  the behaviour measured as an outcome.
- **I** — Any GLP-1 RA: semaglutide (Ozempic/Wegovy), liraglutide (Saxenda/Victoza),
  tirzepatide (dual GIP/GLP-1, Mounjaro/Zepbound), dulaglutide, exenatide, lixisenatide,
  albiglutide, efpeglenatide.
- **C** — Placebo; active comparator; or none (single-arm/before-after where that is the
  only design available, flagged as such).
- **O** — Reward / craving / consumption reduction, grouped by substance:
  - **Alcohol:** drinks per drinking day, heavy-drinking days, total consumption,
    AUDIT / AUDIT-C, %days abstinent, relapse, craving (e.g. PACS/AUQ).
  - **Nicotine / tobacco:** point-prevalence / continuous abstinence, cigarettes/day,
    quit rate, craving, tobacco use disorder incidence.
  - **Gambling:** gambling frequency/severity (e.g. PGSI), craving, disorder incidence.
  - **Other:** opioid/stimulant/cannabis use, binge-eating/food-addiction reward
    endpoints where framed as addiction (not weight loss per se).

## Design tags (on every hit)
RCT / cohort / case-control / self-controlled / target-trial-emulation /
single-arm or before-after / secondary analysis of an RCT / registered-but-unreported trial.

## Search concept blocks

**Drug block** (same as project brief):
`"GLP-1 receptor agonist" OR semaglutide OR Ozempic OR Wegovy OR liraglutide OR Saxenda
OR Victoza OR tirzepatide OR Mounjaro OR Zepbound OR dulaglutide OR exenatide OR
lixisenatide OR albiglutide OR efpeglenatide`

**Benefit/reward outcome block:**
`alcohol OR drinking OR "alcohol use disorder" OR AUD OR AUDIT OR "heavy drinking"
OR nicotine OR smoking OR tobacco OR "smoking cessation" OR cigarette OR vaping
OR gambling OR "gambling disorder" OR craving OR "substance use" OR addiction
OR "reward" OR relapse OR abstinence OR consumption`

Combined: Drug AND Outcome, humans, adults, inception→present.

## Inclusion / exclusion
- **Include:** adults; GLP-1 RA vs comparator or single-arm; a reward/craving/addiction
  consumption outcome reported quantitatively.
- **Exclude:** preclinical/animal-only (route to a Stream C/mechanism side-list);
  narrative reviews (snowball references only); pure weight-loss/glycaemic outcomes with
  no addiction/reward endpoint; duplicate/overlapping cohorts (keep largest/most complete).

## Anchor (trust check)
Reproduce the pooled estimate of one **published GLP-1-RA / alcohol** systematic review
from its included-study data. Recovering its pooled estimate within CI validates the
extended cross-addiction synthesis. Anchor identifiers (PROSPERO/DOI/authorship) are
verified from the retrieved record at anchor time — not carried from prior prose.

## Outputs
PRISMA evidence map + counts; substance-tagged study table; design-stratified pooled
estimates per substance; anchor reproduction; dual-review RoB + hybrid GRADE; synthesis
brief with an explicit benefit–harm symmetry statement; symmetry comparison figure.

## Confounders/artifacts to surface
Channeling (who gets prescribed), adherence/persistence, confounding by indication
(obesity/T2D vs addiction-primary), short follow-up, outcome ascertainment (self-report
vs biochemically verified abstinence), single-arm regression-to-the-mean, small-study
effects in a young/hyped literature (publication/notoriety bias, post-2023 surge).


---

## As-executed search note (transparency)

The **executed** PubMed query used a **trimmed 7-term drug block** —
`"GLP-1 receptor agonist" OR semaglutide OR liraglutide OR tirzepatide OR dulaglutide
OR exenatide OR lixisenatide` — because the PubMed API enforces a 20-boolean-operator
cap and the full 15-term block (with brand names) exceeded it. Brand names (Ozempic,
Wegovy, Saxenda, Victoza, Mounjaro, Zepbound) and two lower-prevalence generics
(albiglutide, efpeglenatide) were dropped. In PubMed, brand-name-only records are rare
without the generic also present, so the recall loss is expected to be small, but it is
**not zero** and is disclosed here rather than hidden.

**Source coverage:** the executed search queried **PubMed only** (via the pubmed MCP
connector). Europe PMC / other databases named in the plan were **not** queried in this
pass. Retrieval was capped at 100 relevance-ranked hits per substance block. Three of the
four blocks exceeded that cap and were truncated — alcohol (383 total), other (217),
and nicotine (161); only gambling (28) was retrieved in full. The corpus is therefore a
relevance-ranked screening pool, not an exhaustive census. A future pass adding Europe
PMC + full pagination + brand-name terms (chunked to respect the operator cap) would
raise recall; the current yield is adequate for a benefit-side scoping synthesis and its
limits are stated in the Stream D brief.
