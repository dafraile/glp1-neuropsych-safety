# Presentation site

Two self-contained views of the GLP-1 neuropsychiatric-safety triangulation project — no build
step, no external dependencies, all figures local, all CSS/JS inlined:

- **[`index.html`](index.html)** — the full scroll-driven walkthrough (consult for the complete narrative and results).
- **[`video.html`](video.html)** — a **3-minute, 5-beat slide deck** built for screen-recording the video presentation.

## The 3-minute deck (`video.html`)

Six full-screen slides timed to a 3-minute narration, matching the beats in the video guide.
Keyboard/click driven, so the presenter controls pacing while narrating:

| Key | Action |
|---|---|
| `→` `Space` · click stage | next slide |
| `←` | previous slide |
| `S` · **☰ Script** button | toggle speaker notes (the narration script, per slide) |
| `F` | fullscreen (for a clean recording) |
| `1`–`6` | jump to a slide |

The comparator swing (0.51 → 3.29) auto-animates when its slide opens; press **▶ replay** to run it
again. Speaker notes are hidden by default so recordings stay clean — open them on a second
monitor, or read and hide with `S`. Dark stage by default; **◐** toggles light.

## Narrative arc

1. **The paradox** — GLP-1 drugs and the 2023 suicide-signal investigations; trials vs. reports.
2. **Four streams, never pooled** — the core methodological choice (A/B/C/D).
3. **Stream A — validating the pipeline** — anchor reproduction (RR 0.84), calibration (AUROC 0.76),
   small-study & E-value sensitivity; "no detected increase," not "safe."
4. **Stream B — the FAERS connection** — the reporting OR swinging 0.51 → 3.29 across comparators
   (scroll-driven), and the July-2023 notoriety spike (DiD p<0.001).
5. **Stream D — the exploratory benefit signal** — same database, opposite fate; addiction-reduction
   footprint across four substance classes; 0 harm ≠ safety.
6. **Why it generalises** — living meta-research, comparator-aware monitoring, repurposing discovery.
7. **The toolkit** — three reusable tools, released under Apache 2.0.

## Run it

Open `index.html` directly in a browser, or serve the folder:

```bash
cd site && python3 -m http.server 8787   # then open http://localhost:8787
```

## Deploy on GitHub Pages

GitHub Pages serves from the repository root or `/docs` (not `/site`). To publish this page:

- **Simplest:** copy `site/` to `docs/` (`cp -r site docs`) and, in the repo's
  **Settings → Pages**, set the source to *Deploy from a branch* → `main` / `/docs`. The site
  will be at `https://dafraile.github.io/glp1-neuropsych-safety/`.
- **Or** use a Pages GitHub Action that publishes the `site/` directory as the artifact.

The page is theme-aware (light/dark), responsive, and passes with no console errors and no
horizontal overflow.
