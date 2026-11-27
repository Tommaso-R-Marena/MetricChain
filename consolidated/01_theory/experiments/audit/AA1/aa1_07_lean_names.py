#!/usr/bin/env python3
"""AA1 audit, script 7: do the Lean names cited in THEORY_REPORT sections 0.2, 2-6 and 11.1-11.15
exist as declarations in proofs/ ?

A text cross-check only (nothing is compiled; `lake` is not run): every back-ticked identifier of
those sections that contains an underscore is looked up among the names declared by
theorem / lemma / def / abbrev / structure / inductive / instance / class in proofs/**/*.lean
(last component of the name).  Identifiers that are not found are printed; they are expected to
be mathematical symbols or file names, not Lean names.

Run:  python3 experiments/audit/AA1/aa1_07_lean_names.py > experiments/audit/AA1/out_07_lean_names.txt
"""
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
lines = open(os.path.join(ROOT, "docs", "THEORY_REPORT.md"), encoding="utf-8").read().split("\n")


def section_bounds(start_pat, end_pat):
    a = next(i for i, l in enumerate(lines) if l.startswith(start_pat))
    b = next(i for i, l in enumerate(lines) if l.startswith(end_pat))
    return a, b


a1, b1 = section_bounds("### 0.2 ", "## 7. ")          # 0.2 ... end of section 6
a2, b2 = section_bounds("## 11. ", "### 11.16 ")       # 11.1 ... 11.15
text = "\n".join(lines[a1:b1] + lines[a2:b2])
names = set(re.findall(r"`([A-Za-z][A-Za-z0-9_\.']*_[A-Za-z0-9_\.']+)`", text))

decl = set()
for root, _, files in os.walk(os.path.join(ROOT, "proofs")):
    for fn in files:
        if fn.endswith(".lean"):
            src = open(os.path.join(root, fn), encoding="utf-8").read()
            for m in re.finditer(r"^(?:private |protected |noncomputable |@\[[^\]]*\]\s*)*"
                                 r"(?:theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+([A-Za-z0-9_\.']+)",
                                 src, re.M):
                decl.add(m.group(1))
short = {d.split(".")[-1] for d in decl} | decl
missing = sorted(n for n in names if n not in short and n.split(".")[-1] not in short)
found = len(names) - len(missing)
print(f"lines {a1+1}-{b1} and {a2+1}-{b2} of docs/THEORY_REPORT.md")
print(f"back-ticked identifiers with an underscore: {len(names)}")
print(f"found as declarations in proofs/: {found}")
print(f"not found ({len(missing)}): {missing}")
lean_like = [n for n in missing if len(n) > 8 and not n.endswith(".md") and n not in ("native_decide",)]
print("not found and long enough to be a Lean name:", lean_like)
print("ALL CITED LEAN NAMES EXIST" if not lean_like else "SOME CITED NAMES ARE MISSING")
