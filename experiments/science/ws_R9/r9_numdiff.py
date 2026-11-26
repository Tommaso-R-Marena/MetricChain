#!/usr/bin/env python3
"""R9, item 5: list every REMOVED token that contains a digit in the word-diff dcdfea6..658b77f of docs/THEORY_REPORT.md,
with the replacement next to it — to find numbers that changed.  Read-only git command."""
import subprocess, re, sys
lo, hi = int(sys.argv[1]), int(sys.argv[2])
out = subprocess.run(["git", "-C", "/home/user/MetricChain", "diff", "-U0", "--word-diff=plain", "--word-diff-regex=[^ ]+",
                      "dcdfea6", "658b77f", "--", "docs/THEORY_REPORT.md"], capture_output=True, text=True).stdout
cur = None
for line in out.splitlines():
    m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
    if m:
        cur = int(m.group(3)); continue
    if cur is None or not (lo <= cur <= hi):
        continue
    for mm in re.finditer(r"\[-(.*?)-\](\{\+(.*?)\+\})?", line):
        rem, add = mm.group(1), mm.group(3) or ""
        if re.search(r"\d", rem) and len(rem) < 400:
            a, b = mm.span()
            ctx = line[max(0, a - 50):a]
            print(f"[{cur}] …{ctx} [-{rem}-] -> {{+{add[:160]}+}}")
