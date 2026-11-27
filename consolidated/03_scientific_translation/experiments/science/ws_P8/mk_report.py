"""
P8 -- assembles docs/science/workstreams/P8_REPORT.md from report_parts/*.md (in name order) and inserts the tables of
out/tables.md (p8_09_tables.py) at the markers  <!--T:T1-->  (the block of tables.md under the heading '## T1 ...',
without its heading line).  A marker <!--T:T7:Lys₁₂--> inserts only the sub-block of T7 that starts with '**Lys₁₂**'; a marker
<!--T:T2|Lys₅,LKSE:5--> inserts the table of T2 restricted to the rows of the named instances (all rows: out/tables.md).
usage: python3 -B mk_report.py
"""
import os, re, glob, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
tab = open(os.path.join(HERE, "out", "tables.md")).read()
blocks = {}
for m in re.finditer(r"^## (T\w+)  [^\n]*\n(.*?)(?=^## T|\Z)", tab, flags=re.S | re.M):
    blocks[m.group(1)] = m.group(2).strip("\n")


def sub_block(name, key):
    b = blocks[name]
    parts = re.split(r"(?m)^(?=\*\*)", b)
    for p in parts:
        if p.startswith(f"**{key}**"):
            return p.strip("\n")
    raise KeyError((name, key))


def rows_of(name, keys):
    """the table of block `name` restricted to the rows whose first cell is one of `keys` (header lines kept)."""
    out_ = []; nrow = 0
    for ln in blocks[name].split("\n"):
        if ln.startswith("|"):
            nrow += 1
            first = ln.split("|")[1].strip()
            if nrow <= 2 or first in keys or first.split(" (")[0] in keys:
                out_.append(ln)
        else:
            out_.append(ln)
    return "\n".join(out_)


def repl(m):
    body = m.group(1)
    if "|" in body:                                    # <!--T:T2|Lys₅,LKSE:5--> : only the rows of the named instances
        name, keys = body.split("|", 1)
        return rows_of(name, [k_.strip() for k_ in keys.split(",")])
    spec = body.split(":")
    return blocks[spec[0]] if len(spec) == 1 else sub_block(spec[0], spec[1])


out = []
for fn in sorted(glob.glob(os.path.join(HERE, "report_parts", "*.md"))):
    out.append(re.sub(r"<!--T:([^>]+)-->", repl, open(fn).read()).rstrip("\n"))
dst = os.path.normpath(os.path.join(HERE, "..", "..", "..", "docs", "science", "workstreams", "P8_REPORT.md"))
open(dst, "w").write("\n\n".join(out) + "\n")
print(f"wrote {dst}: {sum(len(o) for o in out)} characters from {len(out)} parts")
