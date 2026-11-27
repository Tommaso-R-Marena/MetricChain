"""Reads the six T4 logs and prints the statistics quoted in the report (no new computation)."""
import re, glob
import numpy as np
rows = []
allratio = []
for g in ("K4", "W5"):
    for K in (1, 2, 3):
        txt = open(f"logs/t4_{g}_K{K}_run1.log").read()
        assert "DONE t4_certificate" in txt
        direct = [float(x) for x in re.findall(r"mean of f under mu: direct ([0-9.e+-]+)", txt)]
        frommom = [float(x) for x in re.findall(r"from the moments sum c\*m = ([0-9.e+-]+)", txt)]
        cabs = [float(x) for x in re.findall(r"C_abs = sum \|c\| m = ([0-9.e+-]+)", txt)]
        wchg = [float(x) for x in re.findall(r"largest relative change of a moment ([0-9.]+)", txt)]
        wmean = [float(x) for x in re.findall(r"mean of f = ([0-9.e+-]+) \(blind", txt)]
        e2b = [float(x) for x in re.findall(r"fitted exponent ([0-9.]+)", txt)]
        e2c = [(float(a), float(b)) for a, b in re.findall(r"spread s ~ ([0-9.]+) \* eps\^\(1/([0-9.]+)\)", txt)]
        zeros = re.findall(r"LM runs on f: (\d+) reach f < 1e-16; of these (\d+) are NOT a conformer.*?conformers reached: (\[.*?\])", txt)
        mark = [float(x) for x in re.findall(r"r = 1.0: gamma\*\(r\) = [0-9.e+-]+ .*?for 10% of the mass: eps <= ([0-9.e+-]+)", txt)]
        lps = re.findall(r"adversary LP, r = ([0-9.]+), (\d+) candidates.*?\n", txt)
        blocks = txt.split("--- instance")[1:]
        print(f"{g} K={K}: direct mean max {max(direct):.1e}; from moments max |.| {max(abs(x) for x in frommom):.1e}; C_abs {min(cabs):.2e}..{max(cabs):.2e}; "
              f"weights: mean f max {max(wmean):.1e}, moment change max {max(wchg):.3f}; exponent(2b) {min(e2b):.3f}..{max(e2b):.3f}; "
              f"split coef {min(a for a,b in e2c):.2f}..{max(a for a,b in e2c):.2f}, exponent {min(b for a,b in e2c):.2f}..{max(b for a,b in e2c):.2f}; "
              f"Markov eps(10%, r=1) {min(mark):.2e}..{max(mark):.2e}")
        for k, blk in enumerate(blocks):
            z = re.search(r"LM runs on f: (\d+) reach f < 1e-16; of these (\d+) are NOT a conformer.*?conformers reached: (\[.*?\])", blk)
            reached = eval(z.group(3))
            flag = "" if min(reached) > 0 else "   <-- CONTROL FAILS (a conformer never reached)"
            for r in ("0.3", "1.0"):
                vals = []
                for line in blk.splitlines():
                    if line.strip().startswith("adversary LP, r = %s," % r):
                        d = {float(a): float(b) for a, b in re.findall(r"eps=([0-9.e-]+): ([0-9.e+-]+) \(achieved err", line)}
                        vals.append([d.get(e, np.nan) for e in (1e-2, 1e-3, 1e-4, 1e-5)])
                if len(vals) == 2:
                    a, b = np.array(vals[0]), np.array(vals[1])
                    with np.errstate(invalid='ignore', divide='ignore'):
                        ratio = b / a
                    allratio += [x for x in ratio if np.isfinite(x)]
                    if r == "1.0":
                        print(f"    inst {k}: zeros {z.group(1)}, non-conformer {z.group(2)}, reached {reached}{flag}; r=1 far mass small/large set at 1e-2..1e-5: "
                              f"{np.array2string(a, precision=4)} / {np.array2string(b, precision=4)}")
print("ratio (large candidate set / small) over all LP pairs: min %.3f, median %.3f, max %.3f, n = %d" % (min(allratio), np.median(allratio), max(allratio), len(allratio)))
print("LP failures:", sum(open(f).read().count("LP status") for f in glob.glob("logs/t4_*_run1.log")))
