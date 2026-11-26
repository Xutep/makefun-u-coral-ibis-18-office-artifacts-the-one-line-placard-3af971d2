#!/usr/bin/env python3
"""Office Artifacts: The One-Line Placard Contest.

Writes a single museum placard (one line, at most 180 characters) for an
ordinary office object, treated as an ancient artifact from a lost
civilisation, to /output/entry.txt.

The program holds a small curated set of candidate placards, scores each
one deterministically on label craft (catalogue date, material, provenance
or donor, dry structure, economy of length), and writes the best-scoring
one. Ties break toward the earliest candidate, so the output is identical
on every run. Standard library only; no network, no randomness, no input.
"""

import os
import re

# Candidate placards, best first. Each is one line, 1-180 characters.
CANDIDATES = [
    # Stapler: the Binding Rite. A stapler literally binds two sheets
    # together forever, so the ritual conceit writes itself; the donor
    # ("Department of Last Resorts") stays deadpan.
    "Stapler, c. 1987, pressed steel. Ritual binding implement: two "
    "sheets, once strangers, joined forever in a single decisive bite. "
    "Gift of the Department of Last Resorts.",
    # Microwave: the noon rite before the humming god.
    "Microwave oven, c. 1994, enamelled steel. Reheating vessel of the "
    "noon rite; yesterday's lunch warmed before the humming god. "
    "Bequest of the Break Room Elders.",
    # Sticky note: a prayer slip whose plea goes unanswered by Friday.
    "Adhesive note, c. 2003, paper and failing glue. A prayer slip "
    "pressed to the monitor of the gods \u2014 'call me back' \u2014 "
    "unanswered by Friday. Found beneath a keyboard, Floor 3.",
    # Lanyard: rank among the badge-bearers, opened doors by colour alone.
    "Lanyard, c. 2011, woven nylon and plastic clip. Ceremonial cord of "
    "the badge-bearers; its colour alone opened doors lesser mortals "
    "knocked upon. Donated by Human Resources.",
    # Hole punch: the Filing Cult, pierced twice that it might be bound.
    "Hole punch, c. 1979, cast iron. Perforation tool of the Filing "
    "Cult; each sheet pierced twice, that it might be bound and never "
    "lost. Gift of the Records Office.",
]

DATE_RE = re.compile(r"\bc\. \d{4}\b")
DONOR_RE = re.compile(r"\b(Gift of|Bequest of|Donated by|Found beneath)\b")


def score(text):
    """Deterministic label-craft score; higher is a better placard."""
    points = 0
    if DATE_RE.search(text):  # catalogue date sells the artifact
        points += 3
    if ", " in text.split(".")[0]:  # material named in the opening label
        points += 2
    if DONOR_RE.search(text):  # provenance or donor
        points += 2
    if text.endswith("."):
        points += 1
    if ":" in text or ";" in text:  # dry curatorial structure
        points += 1
    if 120 <= len(text) <= 175:  # economy: full but never padded
        points += 2
    elif 100 <= len(text) <= 180:
        points += 1
    if 140 <= len(text) <= 175:
        points += 1
    return points


def choose():
    """Pick the best candidate; earliest wins any tie."""
    best = None
    best_score = -1
    for text in CANDIDATES:
        if not (1 <= len(text) <= 180):
            continue
        if text != text.strip() or "\n" in text:
            continue
        s = score(text)
        if s > best_score:
            best, best_score = text, s
    if best is None:
        raise SystemExit("no valid placard candidate")
    return best


def main():
    text = choose()
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(f"{len(text)} chars: {text}")


if __name__ == "__main__":
    main()
