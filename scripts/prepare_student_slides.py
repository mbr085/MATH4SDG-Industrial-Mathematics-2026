#!/usr/bin/env python3
"""Prepare a notes-free copy of the nine-slide MATH4SDG Reveal.js presentation.

Do not publish or distribute the locally rendered instructor presentation:
it embeds speaker notes, including discussion and facilitator cues.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def prepare(source: Path, destination: Path) -> None:
    if source.resolve() == destination.resolve():
        raise ValueError("The student output must not overwrite the instructor source")

    original = source.read_text(encoding="utf-8")
    output_lines: list[str] = []
    inside_notes = False
    removed_notes = 0

    for line in original.splitlines(keepends=True):
        marker = line.strip()
        if marker == "::: {.notes}":
            if inside_notes:
                raise ValueError("Nested speaker-note blocks are not supported")
            inside_notes = True
            continue
        if inside_notes:
            if marker.startswith(":::") and marker != ":::":
                raise ValueError("Nested div inside speaker notes: inspect manually")
            if marker == ":::":
                inside_notes = False
                removed_notes += 1
                output_lines.append("\n")
            continue
        output_lines.append(line)

    if inside_notes:
        raise ValueError("Unclosed speaker-note block")

    public = "".join(output_lines)
    slides = len(re.findall(r"^## ", public, flags=re.MULTILINE))

    # Fail closed if the structure changes: publishing must be reviewed again.
    if slides != 9 or removed_notes != 9:
        raise ValueError(
            f"Unexpected slide or note count: {slides} slides, "
            f"{removed_notes} speaker-note blocks. Expected nine of each."
        )
    if ".notes" in public or "Gaussian" in public:
        raise ValueError("A possible private note or activity reveal remains")
    if "clustering_investigation.ipynb" not in public:
        raise ValueError("The Part 1 notebook instructions are missing")
    if "clustering_validation.ipynb" not in public:
        raise ValueError("The Part 2 notebook instructions are missing")

    destination.write_text(public, encoding="utf-8")
    print(f"Prepared {destination}: {slides} slides; removed {removed_notes} note blocks")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: prepare_student_slides.py INPUT.qmd OUTPUT.qmd")
    prepare(Path(sys.argv[1]), Path(sys.argv[2]))
