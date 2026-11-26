#!/usr/bin/env python3
"""R23 Item 3(c): which numbered statements of the theory report (at fc3f5d9) are named in neither audit report.
A list, not a judgement.  Method (mechanical):
  1. statements = bold headers at the start of a line  **Theorem|Lemma|Proposition|Corollary|Conjecture <number>
     (number = digits/letters with dots, e.g. 2.1, 11.18a, 11.58a, R4.1), plus the same pattern anywhere in a line
     for 'Corollary' (corollaries of section 2 are introduced inline); each with its line and its section (## / ###).
  2. a statement counts as 'named' in an audit if '<number>' occurs in AA1_REPORT.md or AA2_REPORT.md as a token
     (not followed by a digit or a letter, and not preceded by a digit or a dot), or lies inside a range 'A-B' / 'A–B'
     that the audits write (e.g. 'Theorems 11.3–11.5').
Output: the list of statements not named, by section, and the counts.
Run: python3 -I -B item3c_coverage.py
"""
import re, collections
THY="/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_fc3f5d9"
rep=open(f"{THY}/docs/THEORY_REPORT.md",encoding="utf-8").read().split("\n")
aa=open(f"{THY}/docs/audit/AA1_REPORT.md",encoding="utf-8").read()+"\n"+open(f"{THY}/docs/audit/AA2_REPORT.md",encoding="utf-8").read()
hdr=re.compile(r"^\*\*(Theorem|Lemma|Proposition|Corollary|Conjecture)s? ([0-9R][0-9A-Za-z]*\.[0-9]+[a-z]?(?:′)?)")
sec2=sec3=""
stmts=[]
seen=set()
for i,l in enumerate(rep,1):
    if l.startswith("## "): sec2=l[3:].strip(); sec3=""
    elif l.startswith("### "): sec3=l[4:].strip()
    m=hdr.match(l)
    if m:
        key=(m.group(1),m.group(2))
        if key not in seen:
            seen.add(key); stmts.append((i,m.group(1),m.group(2),sec2,sec3))
# numbers written in the audits, with ranges expanded
def num_key(s):
    m=re.match(r"^([0-9R]+)\.([0-9]+)([a-z]?)$",s)
    return (m.group(1),int(m.group(2)),m.group(3)) if m else None
named=set(re.findall(r"(?<![0-9.])([0-9R][0-9]*\.[0-9]+[a-z]?)(?![0-9A-Za-z])",aa))
ranges=re.findall(r"(?<![0-9.])([0-9]+)\.([0-9]+)[a-z]?\s?[–-]\s?([0-9]+)\.([0-9]+)[a-z]?(?![0-9])",aa)
rng=set()
for a,b,c,d in ranges:
    if a==c and int(b)<int(d) and int(d)-int(b)<60:
        for k in range(int(b),int(d)+1): rng.add((a,k))
def is_named(num):
    if num in named: return True
    k=num_key(num)
    if k and (k[0],k[1]) in rng and k[2]=="": return True
    return False
out=collections.OrderedDict()
cnt_all=collections.Counter(); cnt_missing=collections.Counter()
for (i,kind,num,s2,s3) in stmts:
    top=s2.split(" ")[0].rstrip(".")
    cnt_all[top]+=1
    if not is_named(num):
        cnt_missing[top]+=1
        out.setdefault((s2,s3),[]).append(f"{kind} {num} (l.{i})")
print(f"numbered statements with a bold header in the theory report: {len(stmts)}")
print("by top-level section (all / not named in either audit):")
for k in sorted(cnt_all,key=lambda x:int(x) if x.isdigit() else 99): print(f"   section {k}: {cnt_all[k]} / {cnt_missing[k]}")
print("\nNOT NAMED in AA1_REPORT.md or AA2_REPORT.md:")
for (s2,s3),v in out.items():
    print(f"  [{s2[:60]} | {s3[:70]}]")
    for x in v: print("      "+x)
print("\nstatements per top-level section, first and last line:")
bysec=collections.defaultdict(list)
for (i,kind,num,s2,s3) in stmts: bysec[s2[:40]].append((i,num))
for k,v in bysec.items(): print(f"   {k}: {len(v)} statements, l.{v[0][0]}–l.{v[-1][0]} ({v[0][1]} … {v[-1][1]})")
print("END item3c_coverage")
