#!/usr/bin/env python3
"""Mechanical re-check of the quotations in the report against the text extractions of the downloaded sources.

usage: python3 -I check_quotes.py <report.md> <dir with txt/<name>/<name>.txt> [<dir with the read-only copies>]

Every string between straight double quotes in the report (length >= 25 after trimming) is split at ellipses
("…", "[...]", "...") and each piece (>= 18 characters) is searched in every extraction after normalisation:
whitespace and hyphens removed, ligatures expanded, typographic quotes/dashes unified, case kept.
A quotation is FOUND if all its pieces occur in one and the same source.  Pieces with mathematical symbols that
the PDF text layer scrambles are expected to fail and are listed for inspection by eye, as are quotations that
are not from a downloaded source (phrases of the note under review, my own terms, fetch-tool quotations).
The extractions are read as text only; nothing in them is executed."""
import glob, os, re, sys, unicodedata

def norm(t):
    t = unicodedata.normalize("NFKC", t)
    for a, b in (("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("−", "-"), ("′", "'"),
                 ("ǫ", "ε"), ("ﬁ", "fi"), ("ﬂ", "fl")):
        t = t.replace(a, b)
    return re.sub(r"[\s\-\"]+", "", t)

rep = open(sys.argv[1], encoding="utf-8").read()
src = {}
for f in sorted(glob.glob(os.path.join(sys.argv[2], "*", "*.txt"))):
    src[os.path.basename(f)] = norm(open(f, encoding="utf-8", errors="replace").read())
if len(sys.argv) > 3:
    for f in sorted(glob.glob(os.path.join(sys.argv[3], "*.md"))):
        src["(their file) " + os.path.basename(f)] = norm(open(f, encoding="utf-8", errors="replace").read())

quotes = []
for m in re.finditer(r'"([^"\n]*(?:\n[^"\n]*){0,6}?)"', rep):
    q = re.sub(r"\n>?\s*", " ", m.group(1)).strip()
    q = re.sub(r"^[>*\s]+", "", q)
    if len(q) >= 25:
        quotes.append((rep.count("\n", 0, m.start()) + 1, q))

found = miss = 0
for line, q in quotes:
    pieces = [p.strip() for p in re.split(r"…|\[\.\.\.\]|\.\.\.", q) if len(p.strip()) >= 18]
    if not pieces:
        continue
    hits = [name for name, text in src.items() if all(norm(p) in text for p in pieces)]
    if hits:
        found += 1
        print(f"FOUND   l.{line:4d}  [{hits[0]}]  {q[:90]}")
    else:
        miss += 1
        part = [(p[:40], [n for n, t in src.items() if norm(p) in t][:1]) for p in pieces]
        print(f"MISSING l.{line:4d}  {q[:110]}\n          pieces: {part}")
print(f"\n{found} quotations found verbatim in a source; {miss} not found mechanically (to be inspected by eye).")
