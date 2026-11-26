#!/usr/bin/env python3
"""Shape reconnaissance only: for each line containing a tag token, print line number,
enclosing '## ' / '### ' header index, the first 22 characters, and which tags occur.
No mathematical content is displayed beyond the first 22 characters of a line."""
import re, sys
THY="/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_fc3f5d9"
tagre=re.compile(r"\{([EPCQXF?])\}")
for rep in ("AA1","AA2"):
    path=f"{THY}/docs/audit/{rep}_REPORT.md"
    h2=h3=""
    shapes={}
    rows=[]
    for i,line in enumerate(open(path,encoding="utf-8"),1):
        if line.startswith("## "): h2=line[3:9].strip(); h3=""
        if line.startswith("### "): h3=line[4:9].strip()
        tags=tagre.findall(line)
        if tags:
            shape=re.sub(r"[A-Za-z0-9]","a",line[:6])
            shapes.setdefault((h2,shape),0); shapes[(h2,shape)]+=len(tags)
            rows.append((i,h2,h3,line[:22].rstrip("\n"),"".join(tags)))
    print("=====",rep,"lines with tags:",len(rows))
    for k,v in sorted(shapes.items()): print("   h2=%r shape=%r -> %d tag tokens"%(k[0],k[1],v))
    if "-v" in sys.argv:
        for r in rows: print("  ",r)
