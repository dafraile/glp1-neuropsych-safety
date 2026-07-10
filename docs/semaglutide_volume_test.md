# Does the suicide signal track pharmacology, or notoriety?

**Question.** Only semaglutide trips a suicide/self-injury signal in the earlier
Stream B matrix. Semaglutide is also the July-2023 notoriety epicenter. Is the
signal receptor-mediated GLP-1R pharmacology, or an artifact of *which brand was
in the news*? We test three competing explanations across all 8 molecules.

## Test 1 — report volume (statistical-power / stimulated-reporting artifact)
If more reports simply trip the ROR threshold more easily, the suicide ROR
should rise with total report volume.

- Spearman(ROR vs total reports) = **0.26, p=0.62** (n=6 estimable). **No
  positive relationship.** In fact the single highest-volume molecule is
  protective (see Test 2). Report volume does **not** explain the signal.

## Test 2 — GLP-1R pharmacology (the falsifier: tirzepatide)
If suicidality were mediated by GLP-1-receptor engagement, the molecule with the
*most* exposure and the *strongest* receptor pharmacology should signal most.

| Molecule | Class | Total reports | Suicide reports | ROR vs comparator | Signals? |
|---|---|---|---|---|---|
| **tirzepatide** | **dual GIP/GLP-1R** | **140,435 (highest)** | 491 | **0.65** | **No — protective** |
| semaglutide | GLP-1 RA | 82,911 | 912 | 2.08 | Yes |

**tirzepatide is the decisive falsifier.** It has the highest exposure of any
molecule, is the only *dual* GIP/GLP-1R agonist (maximal receptor engagement),
and 96.9% of its reports are post-July-2023 (same era as semaglutide) — yet it
is **protective (0.65, no signal)**. If harm were GLP-1R pharmacology,
tirzepatide should be the *worst* offender. It is among the safest. Pharmacology
is falsified.

## Test 3 — notoriety (which brands were named in the July-2023 probe)
Pre–July-2023, **no estimable molecule signals** (maximum comparator ROR across the **six molecules with reports** = **0.96**; albiglutide and efpeglenatide have zero suicide reports, so their Haldane-corrected ROR is an empty-cell artifact, not a signal). Post–July-2023, exactly two cross into signal:

| Post-Jul-2023 signal (lo>1) | Brand | In Jul-2023 EMA/FDA probe? |
|---|---|---|
| semaglutide (2.98) | Ozempic / Wegovy | **Yes — the index drug** |
| liraglutide (2.31) | Saxenda / Victoza | **Yes — named alongside** |
| tirzepatide (0.78, protective) | Mounjaro / Zepbound | No — not yet marketed for obesity at probe time |

The two molecules that signal post-notoriety are precisely the **obesity brands
named in the July-2023 regulatory investigation**. The higher-exposure,
same-era, but not-yet-in-the-news molecule (tirzepatide) does not signal. This
is the pattern notoriety bias predicts and pharmacology does not.

## Verdict
The suicide/self-injury signal **tracks brand notoriety timing, not GLP-1R
pharmacology or raw report volume.** The single most-exposed, most-receptor-
engaging molecule (tirzepatide) is protective; the signal appears only
post-July-2023 and only in the brands the regulators named. This closes the
"only semaglutide signals, and semaglutide is the epicenter" gap with a
quantitative, falsification-based argument rather than a hand-wave.

*Files: `semaglutide_volume_test.csv`, `semaglutide_volume_vs_pharmacology.png`.*
