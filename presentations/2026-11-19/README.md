# MATH4SDG presentation — Quarto + Reveal.js

Editable source for the nine-slide Friday 20 November 2026 presentation.

## Contents

- `index.qmd` — **primary presentation source**, text and equations in Quarto Markdown, plus speaker notes.
- `math4sdg.css` — global slide typography, spacing, panels, tables, and colors.
- `assets/install_guide_qr.png` — QR code linking directly to `INSTALL.md` on the setup slide.
- The two clustering slides give **local JupyterLab instructions and filenames**, without GitHub links or QR codes. The earlier clustering QR assets remain in `assets/` but are not displayed.
- Reveal the ninth slide only after students have recorded and discussed their predictions.
- Private facilitator reveal and discussion notes are **kept outside this public repository**. Do not share them with students in advance.

## Preview and render

From this directory, with [Quarto](https://quarto.org/) installed:

```bash
quarto preview index.qmd
quarto render index.qmd --to revealjs
```

The render command produces `index.html` and any support assets needed by your local Quarto version. Copy the output and support directory together if the render is not embedded into one HTML file.

Press **S** in the Reveal.js presentation to open the presenter view, including the slide's `.notes` content. (For this reason, do not distribute full presenter notes in advance.)

The YAML deliberately **does not contain a title field**, preventing Quarto from inserting an automatic extra title slide. The first `##` heading is the visual title slide. A ninth slide introduces the independent clustering sample after students have recorded their predictions.

The staged clustering notebooks, the independent feature-selection investigation and their public CSV datasets are in the main [MATH4SDG repository](https://github.com/mbr085/MATH4SDG-Industrial-Mathematics-2026). Students open the clustering notebooks **locally in JupyterLab** using the filenames shown on slides 8 and 9; the slides do not execute Python code while rendering.

## Editing tips

- Each `##` heading begins a new slide; there are nine slides.
- Slide text, equations, and tables are ordinary Markdown or LaTeX.
- `::: {.columns}` and `::: {.column width="..."}` create multi-column layouts.
- `::: {.notes}` contains speaker notes that appear in the presenter view, not the projected slide.
- Edit `math4sdg.css` for fonts, sizes, panel styles, and colors, rather than editing individual slides repeatedly.
- Keep the public presentation free of the Gaussian-data reveal until the student investigation is complete.

## Environment status

The source has been checked with Pandoc's Markdown parser. Preview it using the project's Nix/direnv environment, then inspect the rendered slides locally before presenting.
## Student version for GitHub Pages

The **instructor** file `index.qmd` contains speaker notes. Do **not** publish its ordinary `index.html` output: Reveal.js speaker view can display those notes.

The workflow [`publish-student-slides.yml`](../../.github/workflows/publish-student-slides.yml) instead:

1. Builds a temporary `student-public.qmd` from `index.qmd`, removing all nine `.notes` sections with [`prepare_student_slides.py`](../../scripts/prepare_student_slides.py).
2. Refuses to publish if the number of slides or notes differs from nine or if the activity reveal appears in the public source.
3. Renders a **self-contained**, notes-free Reveal.js `index.html` and deploys **only that HTML file** to GitHub Pages.

The two clustering notebooks are named on slides 8–9, but the Gaussian data-generating mechanism and instructor discussion prompts are excluded. Reveal the second notebook only after students have recorded their prediction; a publicly accessible slide deck cannot enforce that staging.

To activate GitHub Pages, select **Settings → Pages → Build and deployment → Source: GitHub Actions**. The workflow runs on relevant changes to `main` and can also be run manually under **Actions → Publish student presentation (without notes) → Run workflow**.

Expected Pages address after successful deployment: `https://mbr085.github.io/MATH4SDG-Industrial-Mathematics-2026/`. Verify that it actually loads before sharing it.
