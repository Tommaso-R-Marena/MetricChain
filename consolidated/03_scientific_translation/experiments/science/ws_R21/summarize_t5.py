"""Collects the SUMMARY lines of the T5 logs into one table (no new computation)."""
import re, glob
rows = []
for f in sorted(glob.glob("logs/t5_*_run1.log")):
    txt = open(f).read()
    done = "DONE t5_gap_scaling" in txt
    m = re.search(r"SUMMARY graph=(\S+) m=(\d+) codim=(\d+) K=(\d+) splices=(\d+): g1 median ([0-9.e+-]+), min ([0-9.e+-]+), max ([0-9.e+-]+); "
                  r"sup-norm gap relative to the mean squared length: median ([0-9.e+-]+), min ([0-9.e+-]+)(?:; g2 median ([0-9.e+-]+), min ([0-9.e+-]+))?; heuristic splices\^\(-1/codim\) = ([0-9.e+-]+)", txt)
    if m is None:
        print('NOT FINISHED (no SUMMARY line):', f)
        continue
    n_ens = len(re.findall(r"^ens \d+:", txt, flags=re.M))
    mode = "sample" if "(sample)" in txt else "all"
    rows.append((m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), float(m.group(6)), float(m.group(7)), float(m.group(8)),
                 float(m.group(9)), float(m.group(10)), m.group(11), m.group(12), float(m.group(13)), n_ens, mode, done))
order = {"K4": 0, "W5": 1, "K5-e": 2, "K5": 3, "W6": 4, "K6": 5}
rows.sort(key=lambda r: (order[r[0]], r[3]))
print("graph  m codim K   splices  n_ens   g1 median     g1 min     g1 max  rel.sup median  rel.sup min   g2 median   heuristic  colourings  DONE")
for r in rows:
    print(f"{r[0]:5s} {r[1]:2d} {r[2]:5d} {r[3]:1d} {r[4]:9d} {r[13]:6d}   {r[5]:9.2e}  {r[6]:9.2e}  {r[7]:9.2e}   {r[8]:9.2e}    {r[9]:9.2e}   {(r[10] or '-'):>9s}   {r[12]:9.2e}  {r[14]:>6s}  {r[15]}")
