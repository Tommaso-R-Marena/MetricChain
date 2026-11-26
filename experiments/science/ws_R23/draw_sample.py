#!/usr/bin/env python3
"""R23 sampler.  Implements the rule pre-registered in NOTES.md (2026-11-26T17:25Z / 17:31Z).
Run:  python3 -I -B draw_sample.py   (reads <THY> only; writes sample.json next to this script)."""
import re, json, hashlib, random, os, sys, datetime
THY="/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_fc3f5d9"
HERE=os.path.dirname(os.path.abspath(__file__))
SIZES={"P":6,"F":5,"Q":3,"?":2}
ENTRY_RE={"AA1":re.compile(r"^### (E\d+)\."), "AA2":re.compile(r"^### (Entry \d+)")}
END_RE={"AA1":re.compile(r"^## 4\."), "AA2":re.compile(r"^## A\. ")}
tagre=re.compile(r"\{([EPCQXF?])\}")

def seed_of(s): return int(hashlib.sha256(s.encode()).hexdigest(),16) % 2**32

def population(rep):
    path=f"{THY}/docs/audit/{rep}_REPORT.md"
    entry=None; started=False; ended=False
    pop=[]  # (line, col, tag, entry)
    for i,line in enumerate(open(path,encoding="utf-8"),1):
        if END_RE[rep].match(line): ended=True
        m=ENTRY_RE[rep].match(line)
        if m and not ended: entry=m.group(1); started=True
        if started and not ended:
            for mm in tagre.finditer(line):
                pop.append((i,mm.start(),mm.group(1),entry))
    return pop

out={"rule":"NOTES.md 2026-11-26T17:25Z","samples":{}, "population_counts":{}}
lines=[]
allpops={}
for rep in ("AA1","AA2"):
    pop=population(rep); allpops[rep]=pop
    counts={t:sum(1 for p in pop if p[2]==t) for t in "EPCQXF?"}
    out["population_counts"][rep]=counts
    lines.append(f"{rep}: population tokens inside entries: {counts} total {len(pop)}")
    for T,m in SIZES.items():
        sub=[p for p in pop if p[2]==T]
        N=len(sub)
        if N<=m:
            idx=list(range(N)); s=None; k=None
        else:
            k=N//m; seed=seed_of(f"R23|{rep}|{T}"); rng=random.Random(seed); s=rng.randrange(k)
            idx=[s+j*k for j in range(m)]
        sel=[{"index":j,"line":sub[j][0],"col":sub[j][1],"entry":sub[j][3]} for j in idx]
        out["samples"][f"{rep}|{T}"]={"N":N,"m":m,"k":k,"start":s,"selected":sel}
        lines.append(f"{rep} {{{T}}}: N={N} m={m} k={k} start={s} -> "+", ".join(f"#{d['index']} l.{d['line']} ({d['entry']})" for d in sel))
# rebuild order for the ten F
tenF=[("AA1",d) for d in out["samples"]["AA1|F"]["selected"]]+[("AA2",d) for d in out["samples"]["AA2|F"]["selected"]]
rng=random.Random(seed_of("R23|rebuild")); order=list(range(len(tenF))); rng.shuffle(order)
out["rebuild_order"]=[{"rep":tenF[j][0],"line":tenF[j][1]["line"],"entry":tenF[j][1]["entry"]} for j in order]
lines.append("rebuild order (take the first two that are finite computable objects): "+", ".join(f"{d['rep']} l.{d['line']}" for d in out["rebuild_order"]))
# citations
citre=re.compile(r"SCI-(REV|RES)-[0-9]+")
cits=[]
for fn,lab in ((f"{THY}/docs/audit/AA1_REPORT.md","AA1"),(f"{THY}/docs/audit/AA2_REPORT.md","AA2"),(f"{THY}/docs/ASSUMPTION_AUDIT.md","SYN")):
    for i,line in enumerate(open(fn,encoding="utf-8"),1):
        for mm in citre.finditer(line): cits.append((lab,i,mm.start(),mm.group(0)))
N=len(cits); m=5
lines.append(f"citations of our messages: N={N}; distinct messages: {sorted(set(c[3] for c in cits))}")
if N>m:
    k=N//m; rng=random.Random(seed_of("R23|citations")); s=rng.randrange(k); idx=[s+j*k for j in range(m)]
else:
    k=None; s=None; idx=list(range(N))
chosen=[]; seen=set()
for j in idx:
    jj=j; steps=0
    while cits[jj%N][3] in seen and steps<N: jj+=1; steps+=1
    c=cits[jj%N]; seen.add(c[3]); chosen.append({"drawn_index":j,"used_index":jj%N,"file":c[0],"line":c[1],"msg":c[3]})
out["citations"]={"N":N,"k":k,"start":s,"selected":chosen}
lines.append("citation sample: "+", ".join(f"{d['file']} l.{d['line']} {d['msg']}"+("" if d['drawn_index']==d['used_index'] else f" (moved from #{d['drawn_index']})") for d in chosen))
stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
lines.append(f"clock (UTC): {stamp}")
lines.append("END draw_sample")
json.dump(out,open(os.path.join(HERE,"sample.json"),"w"),indent=1)
log=os.path.join(HERE,"logs",f"draw_sample_{stamp}.log")
open(log,"w").write("\n".join(lines)+"\n")
print("\n".join(lines)); print("log:",log)
