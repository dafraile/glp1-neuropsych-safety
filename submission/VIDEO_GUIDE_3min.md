# 3-minute video script & shot guide

A hackathon judge watches dozens of these. **Win the first 20 seconds** with the paradox, then
show the one figure that resolves it, then prove you were rigorous. Total budget ≈ 480 words at a
calm 160 wpm. Times are cumulative.

Each beat below gives you: **[what to say]** (script you can read close to verbatim) and
**[what's on screen]** (the slide/figure for your website-as-slides).

---

### BEAT 1 — The hook (0:00–0:30) · ~75 words
**[on screen]** Title slide → then the **triangulation forest plot**
(`figures/triangulation_forest.png`).

> "GLP-1 drugs like Ozempic are taken by tens of millions of people. In 2023, both the FDA and
> the EMA opened investigations because adverse-event databases were filling up with reports of
> suicidal thoughts and self-harm. But here's the paradox: the *randomised trials* show no such
> risk. So which do you believe — the spontaneous reports, or the trials? We built a system to
> answer that, and the answer is more interesting than either 'safe' or 'dangerous'."

*Pause on the forest plot: point at the blue/green points near 1.0 (trials & cohorts) vs the red
point at 2.08 (spontaneous reports). "Same drug. Same outcome. Opposite signals."*

---

### BEAT 2 — The design (0:30–1:05) · ~90 words
**[on screen]** The four-stream table (Stream A/B/C/D) — build this as a simple 4-box slide.

> "The mistake most reviews make is pooling everything together. We did the opposite. We built
> four evidence streams and kept them strictly separate. Stream A: the designed studies — trials
> and cohorts — pooled properly with risk-of-bias and GRADE. Stream B: the FAERS spontaneous
> reports, for comparison only, never mixed in. Stream C: the biological mechanism. And Stream D,
> exploratory: does this same drug pathway actually *reduce* addiction? Four streams, four
> methods, compared at the end — not blended into one misleading average."

---

### BEAT 3 — The novel result (1:05–2:00) · ~140 words — THIS IS THE CORE, GIVE IT THE MOST TIME
**[on screen]** The **notoriety ITS panel** (`figures/faers_notoriety_its.png`) — the two-panel
figure with the red semaglutide line spiking after July 2023 while control lines stay flat.

> "Here's what we found in the spontaneous reports, and it's the heart of the project. That
> suicide signal for semaglutide? It isn't stable. Compare semaglutide to metformin and the
> reporting ratio is 0.51 — *protective*. Compare it to other GLP-1 drugs and it's 3.29 — a
> strong signal. Same drug, same outcome; the answer flips entirely based on what you compare it
> to. And look at the timing" — *[point to the red spike]* — "the signal is basically absent
> before July 2023, then it jumps — but *only* for semaglutide, the drug that was in the news.
> Control outcomes like headache, and control drugs, show no such jump. That's the fingerprint
> of notoriety bias and confounding — not a real drug effect. We're not saying the drug is safe.
> We're showing the alarm signal isn't trustworthy."

---

### BEAT 4 — Why trust us / the build (2:00–2:35) · ~85 words
**[on screen]** Split slide: left = OMOP calibration ROC (`figures/omop_calibration_roc.png`) with
"AUROC 0.76"; right = the three reusable tools (dual-reviewer-rob, grade-hybrid, faers_tool).

> "Two things make this credible. First, we didn't just assert our tool works — we calibrated it
> against a reference set of known drug-safety associations: AUROC 0.76, an honest number, not a
> cherry-picked 0.99. Second, everything is reusable. The risk-of-bias engine runs the official
> signalling questions through two different AI models that cross-check each other. The GRADE
> harness, the FAERS client — all published as skills. And one command reproduces every headline
> number in the repo from the raw data."

---

### BEAT 5 — Close (2:35–3:00) · ~55 words
**[on screen]** The headline-result slide: "No detected increase — not proof of safety" + the
benefit-symmetry teaser.

> "So: the designed evidence shows no increased risk, but we're careful to say 'no detected
> increase,' not 'safe.' The spontaneous alarm is explained by comparison and calendar, not
> biology. And the same pathway may even *reduce* addiction. That's what triangulation gives you
> that a single pooled number never could. Thanks for watching."

---

## Delivery notes
- **Practice the timing.** At 160 wpm this is ~440 spoken words plus pauses — right at 3:00. If
  you run long, cut Beat 4 first (the tooling detail), never Beat 3.
- **The number that sticks is 0.51 → 3.29.** Say it slowly. It's the whole thesis in two numbers.
- **Never say "we proved it's safe."** Say "no detected increase" / "the alarm signal isn't
  trustworthy." Judges with a stats background will reward the calibration and punish overclaiming.
- **If asked in Q&A "so is it safe?"** → "Designed studies don't show harm, but they can't rule
  out a modest or subgroup effect — and that's exactly the point: we quantified what we can and
  can't say, instead of picking a side."

## Recommended slide → figure mapping (for the website)
| Slide | File |
|---|---|
| 1. Hook / paradox | `figures/triangulation_forest.png` |
| 2. Four streams | *(make a 4-box graphic; content in SUBMISSION_README §2)* |
| 3. The novel result | `figures/faers_notoriety_its.png` (+ optionally the comparator grid) |
| 4a. Calibration | `figures/omop_calibration_roc.png` |
| 4b. Reusable tools | *(logos/names of the 3 tools)* |
| 5. Close | `figures/benefit_harm_symmetry.png` |
