#!/usr/bin/env python3
"""Create seven-slide, notes-free Saturday presentation source."""
from pathlib import Path
import re
import sys

def prepare(source: Path, destination: Path) -> None:
    if source.resolve() == destination.resolve():
        raise ValueError("Never overwrite the instructor source")
    kept = []
    skipping = False
    notes = 0
    for line in source.read_text(encoding="utf-8").splitlines(keepends=True):
        s = line.strip()
        if s == "::: {.notes}":
            if skipping:
                raise ValueError("Nested note block")
            skipping = True
        elif skipping and s == ":::":
            skipping = False
            notes += 1
            kept.append("\n")
        elif not skipping:
            kept.append(line)
    public = "".join(kept)
    slides = len(re.findall(r"^## ", public, re.MULTILINE))
    if skipping or slides != 7 or notes != 7 or ".notes" in public:
        raise ValueError(f"Unexpected slides/notes: {slides}/{notes}")
    destination.write_text(public, encoding="utf-8")
    print(f"Prepared notes-free source: {slides} slides")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python prepare_student.py index.qmd student-public.qmd")
    prepare(Path(sys.argv[1]), Path(sys.argv[2]))
