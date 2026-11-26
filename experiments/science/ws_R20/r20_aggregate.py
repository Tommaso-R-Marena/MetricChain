#!/usr/bin/env python3
"""r20_aggregate.py -- reads the SUMMARY blocks of completed r20_theorem.py logs (only logs whose last line is
'END r20_theorem.py') and prints the totals quoted in the report.  Usage: python3 -I -B r20_aggregate.py log1 log2 ..."""
import re
import sys

tot_inst = tot_yes = tot_no = tot_struct = 0
utot = {}
mtot = {}
order = []
for path in sys.argv[1:]:
    lines = open(path).read().splitlines()
    if not lines or lines[-1].strip() != "END r20_theorem.py":
        print("SKIPPED (not complete): %s" % path)
        continue
    for i, l in enumerate(lines):
        m = re.match(r"SUMMARY  set '(\S+)': (\d+) instances \((\d+) solvable, (\d+) not\), (\d+) connected labelled structures enumerated, ([\d.]+) s", l)
        if m:
            name, ni, ny, nn, ns, sec = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), float(m.group(6))
            tot_inst += ni
            tot_yes += ny
            tot_no += nn
            tot_struct += ns
            um = dict((k, int(v)) for k, v in re.findall(r"(U\d)=(\d+)", lines[i + 1]))
            for k, v in um.items():
                utot[k] = utot.get(k, 0) + v
            print("%-34s set %-16s %3d instances (%2d solvable, %2d not) %12d structures %7.1f s  U-violations %s" % (
                path.split("/")[-1], name, ni, ny, nn, ns, sec, um))
            for l2 in lines[i + 3:]:
                m2 = re.match(r"\s+(\S+)\s+\[(\w+)\s*\] S1=(\d+) S2=(\d+) S3=(\d+) S4=(\d+) S5=(\d+) wrong decisions=(\d+)", l2)
                if not m2:
                    continue
                nm = m2.group(1)
                vals = [int(x) for x in m2.groups()[2:]]
                if nm not in mtot:
                    mtot[nm] = [m2.group(2), 0, 0, 0, 0, 0, 0, 0, 0]
                    order.append(nm)
                for j, v in enumerate(vals):
                    mtot[nm][1 + j] += v
                mtot[nm][7] += ni
                mtot[nm][8] += nn
print()
print("TOTAL over the logs above: %d instances (%d solvable, %d not), %d connected labelled structures; U totals %s" % (
    tot_inst, tot_yes, tot_no, tot_struct, utot))
print("%-30s %-5s %4s %4s %4s %4s %4s %6s  %s" % ("loop function", "class", "S1", "S2", "S3", "S4", "S5", "wrong", "instances (not solvable) it was run on"))
for nm in order:
    c = mtot[nm]
    print("%-30s %-5s %4d %4d %4d %4d %4d %6d  %d (%d)" % (nm, c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8]))
print("END r20_aggregate.py")
