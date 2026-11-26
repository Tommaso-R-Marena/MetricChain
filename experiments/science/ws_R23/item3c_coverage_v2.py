#!/usr/bin/env python3
"""R23 Item 3(c), second pass (v1 = item3c_coverage.py looked at bold headers at line starts only).
Every number N.M[a] that the theory report (fc3f5d9) uses after Theorem/Lemma/Proposition/Corollary/Conjecture
(anywhere in a line, singular or plural, also in ranges and lists), by the section of its FIRST occurrence in bold
(taken as the place of the statement) or, failing that, of its first occurrence; then: is the number named in AA1/AA2?
Also: numbered objects of other kinds that are not statements with proofs but carry claims -
rows A1..E2 of section 0.2, rows G1..G40 of section 10, items of section 12, 'Dnn' excluded.
Run: python3 -I -B item3c_coverage_v2.py"""
import re, collections
THY="/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_fc3f5d9"
rep=open(f"{THY}/docs/THEORY_REPORT.md",encoding="utf-8").read().split("\n")
aa1=open(f"{THY}/docs/audit/AA1_REPORT.md",encoding="utf-8").read(); aa2=open(f"{THY}/docs/audit/AA2_REPORT.md",encoding="utf-8").read(); aa=aa1+"\n"+aa2
kindre=r"(Theorem|Lemma|Proposition|Corollary|Conjecture)s?"
numre=r"((?:[0-9]+|R[0-9]+)\.[0-9]+[a-z]?)"
occ=collections.OrderedDict()   # (kind,num) -> dict(first=(line,sec), bold=(line,sec))
sec=""
for i,l in enumerate(rep,1):
    if l.startswith("## "): sec=l[3:].split(" ")[0].rstrip(".")
    for m in re.finditer(kindre+r" "+numre,l):
        key=m.group(2)
        d=occ.setdefault(key,{"kind":m.group(1)})
        d.setdefault("first",(i,sec))
        if "**"+m.group(0) in l and "bold" not in d: d["bold"]=(i,sec)
def named(num,text):
    if re.search(r"(?<![0-9.])"+re.escape(num)+r"(?![0-9A-Za-z])",text): return True
    m=re.match(r"^([0-9]+)\.([0-9]+)$",num)
    if m:
        for a,b,c,d in re.findall(r"(?<![0-9.])([0-9]+)\.([0-9]+)[a-z]?\s?[–-]\s?([0-9]+)\.([0-9]+)[a-z]?(?![0-9])",text):
            if a==c==m.group(1) and int(b)<=int(m.group(2))<=int(d) and int(d)-int(b)<60: return True
    return False
tot=0; notnamed=[]; bysec=collections.Counter(); ext=[]
for num,d in occ.items():
    line,s=d.get("bold",d["first"])
    # numbers that belong to OTHER documents (workstream theorems like 'Theorem 13' have no dot; 'Theorem 1.3' of a cited paper etc.)
    major=num.split(".")[0]
    if major not in ("2","3","4","6","11","R4"): ext.append((num,d["kind"],line,s)); continue
    tot+=1; bysec[s]+=1
    if not named(num,aa): notnamed.append((num,d["kind"],line,s,"bold" in d))
print(f"numbers of the report's own statements (majors 2, 3, 4, 6, 11, R4): {tot}; by section of the statement: {dict(bysec)}")
print(f"not named in either audit: {len(notnamed)}")
for x in notnamed: print("   ",x)
print(f"numbers with other majors (cited from other documents or papers; not statements of this report): {len(ext)}")
for x in ext: print("   ",x)
# other numbered objects
g_rows=[re.match(r"^\| (G[0-9]+) ",l).group(1) for l in rep if re.match(r"^\| (G[0-9]+) ",l)]
g_named=[g for g in g_rows if re.search(r"\b"+g+r"\b",aa)]
print(f"rows of section 10: {g_rows[0]}..{g_rows[-1]} ({len(g_rows)}); named in the audits: {len(g_named)}; NOT named: {[g for g in g_rows if g not in g_named]}")
a_rows=[]
for l in rep[40:80]:
    m=re.match(r"^\| ([A-E][0-9]+) ",l)
    if m: a_rows.append(m.group(1))
print(f"rows of section 0.2: {a_rows}; not named in the audits: {[a for a in a_rows if not re.search(r'\b'+a+r'\b',aa)]}")
# section 12 items
items=[]
insec=False
for i,l in enumerate(rep,1):
    if l.startswith("## 12."): insec=True
    elif l.startswith("## 13."): insec=False
    if insec:
        m=re.match(r"^([0-9]+)\. \*\*",l)
        if m: items.append(int(m.group(1)))
print(f"numbered items of section 12: {items}")
for it in items:
    print(f"   item {it}: cited in AA1 as '§12 item {it}': {len(re.findall(r'§12 item '+str(it)+r'(?![0-9])',aa1))} times; in AA2: {len(re.findall(r'§12 item '+str(it)+r'(?![0-9])',aa2))} times")
print("END item3c_coverage_v2")
