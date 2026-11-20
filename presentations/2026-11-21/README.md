# Saturday AI workshop slides — 21 November 2026

Seven activity-led Quarto / Reveal.js slides for the 60-minute UDSM MATH4SDG workshop. The accepted 20 November deck under 2026-11-19 is unchanged.

## Instructor preview

From this folder using the existing Nix/direnv environment with Quarto:

```sh
quarto preview index.qmd
```

Press S for speaker notes. **Do not distribute the instructor render**, which embeds notes.

## Student version

Run the local notes-removal script and render the result:

```sh
python prepare_student.py index.qmd student-public.qmd
quarto render student-public.qmd --to revealjs --output student.html -M embed-resources:true
```

The script verifies that it removed exactly seven note blocks from seven slides.

A standalone offline notes-free browser HTML and presentation package are also supplied as separate conversation downloads. The existing Friday-only GitHub Pages workflow is **not** modified and will not automatically publish these Saturday slides.

Do not reveal the `deobfuscation(x)` function until students have explicitly chosen a model. Do not include restricted partner data in public materials.
