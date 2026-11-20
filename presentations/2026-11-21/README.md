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

A standalone offline notes-free browser HTML and presentation package are also supplied as separate conversation downloads. The GitHub Pages workflow publishes this notes-free student deck at [Saturday's slides](https://mbr085.github.io/MATH4SDG-Industrial-Mathematics-2026/2026-11-21/) while retaining [Friday's slides](https://mbr085.github.io/MATH4SDG-Industrial-Mathematics-2026/) at the original address. Share only the Saturday link with students; the instructor source contains notes.

Do not reveal the `deobfuscation(x)` function until students have explicitly chosen a model. Do not include restricted partner data in public materials.

## Pair and group organization

Students remain in the five existing project groups and work in pairs. Each pair constructs two models, selects one using validation results **before** the final test, and tests it once. Afterwards, each group reports the two lowest final-test MAEs among the pairs' preselected models. This ranking is for description, not a second model-selection step.

**Publication status:** The accepted presentation is merged. GitHub Pages deploys the notes-free student version after the publishing workflow succeeds.
