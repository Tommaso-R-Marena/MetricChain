#!/usr/bin/env python3
"""Print the LaTeX alt-text of the displayed equations carrying given numbers in an arXiv HTML (LaTeXML) page.
usage: python3 -I eqdump.py <file.html> '(2.30)' '(2.33)' ...
Reads the file as text only (untrusted data); nothing from the file is executed."""
import re, sys, html
src = open(sys.argv[1], encoding="utf-8", errors="replace").read()
for tag in sys.argv[2:]:
    for m in re.finditer(re.escape(tag), src):
        lo = max(0, m.start() - 6000)
        chunk = src[lo:m.start()]
        alts = re.findall(r'alttext="([^"]*)"', chunk)
        print("==", tag, "at", m.start(), "last alttexts before the tag:")
        for a in alts[-3:]:
            print("   ", html.unescape(a)[:900])
        break
