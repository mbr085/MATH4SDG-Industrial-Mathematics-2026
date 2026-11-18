# MATH4SDG presentation — Quarto + Reveal.js

Editable source for the nine-slide Friday 20 November 2026 presentation.

## Contents

- `index.qmd` — **primary presentation source**, text and equations in Quarto Markdown, plus speaker notes.
- `math4sdg.css` — global slide typography, spacing, panels, tables, and colors.
- `assets/repo_qr.svg` and `assets/clustering_qr.svg` — existing QR codes for the repository and first activity.
- `assets/clustering_validation_qr.png` — QR code for the second activity; reveal the ninth slide only after the prediction checkpoint.
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

The staged clustering notebooks, the independent feature-selection investigation and their public CSV datasets are in the main [MATH4SDG repository](https://github.com/mbr085/MATH4SDG-Industrial-Mathematics-2026). The slides only link to those resources; they do not run any Python code while rendering.

## Editing tips

- Each `##` heading begins a new slide; there are nine slides.
- Slide text, equations, and tables are ordinary Markdown or LaTeX.
- `::: {.columns}` and `::: {.column width="..."}` create multi-column layouts.
- `::: {.notes}` contains speaker notes that appear in the presenter view, not the projected slide.
- Edit `math4sdg.css` for fonts, sizes, panel styles, and colors, rather than editing individual slides repeatedly.
- Keep the public presentation free of the Gaussian-data reveal until the student investigation is complete.

## Environment status

The source has been checked with Pandoc's Markdown parser. Preview it using the project's Nix/direnv environment, then inspect the rendered slides locally before presenting.