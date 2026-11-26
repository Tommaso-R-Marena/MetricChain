#!/usr/bin/env python3
"""R9, item 5: compact view of `git diff dcdfea6 658b77f -- docs/THEORY_REPORT.md` (read-only git command).
For every hunk in a given range of NEW line numbers prints the removed and added word segments with some context."""
import subprocess, sys, re
lo, hi = int(sys.argv[1]), int(sys.argv[2])
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 70
out = subprocess.run(["git", "-C", "/home/user/MetricChain", "diff", "-U0", "--word-diff=plain", "--word-diff-regex=[^ ]+",
                      "dcdfea6", "658b77f", "--", "docs/THEORY_REPORT.md"], capture_output=True, text=True).stdout
cur = None
for line in out.splitlines():
    m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
    if m:
        cur = int(m.group(3)); n = int(m.group(4) or 1)
        show = (cur <= hi and cur + max(n, 1) - 1 >= lo)
        if show:
            print(f"\n=== new lines {cur}-{cur + max(n,1) - 1}")
        continue
    if cur is None or not show:
        continue
    if "[-" not in line and "{+" not in line:
        continue
    # merge adjacent change marks, print with context
    pos = [mm.span() for mm in re.finditer(r"\[-.*?-\]|\{\+.*?\+\}", line)]
    segs = []
    for a, b in pos:
        if segs and a - segs[-1][1] < 2 * ctx:
            segs[-1][1] = b
        else:
            segs.append([a, b])
    for a, b in segs:
        s = line[max(0, a - ctx):min(len(line), b + ctx)]
        print("   …" + s + "…")
