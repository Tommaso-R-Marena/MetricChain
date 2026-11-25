"""Run an_main.analyse on every enumerated model of one backbone and both thresholds.
usage: python3 -B an_batch.py BB [GRID] [--only PREFIX]     (logs to stdout; JSON to out/)"""
import sys, os, json, re, time
import numpy as np
from anlib import HERE
from an_main import analyse

bb = sys.argv[1]
grid = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "R3"
only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
tags = sorted(fn[:-4] for fn in os.listdir(os.path.join(HERE, "data")) if re.fullmatch(rf"fb_.+_{bb}_{grid}_t0\.60\.npz", fn))


def order(t):
    m = re.match(r"fb_([A-Z]+)c?(\d*)", t)
    return (m.group(1), int(m.group(2) or 0))


for tag in sorted(tags, key=order):
    if only and not tag.startswith("fb_" + only):
        continue
    z = np.load(os.path.join(HERE, "data", tag + ".npz"))
    shape0 = [int(v) for v in z["shape"]]
    for tau in (0.70, 0.60):
        outp = os.path.join(HERE, "out", f"an_{tag}_tau{tau:.2f}.json")
        if os.path.exists(outp):
            continue
        big = max(shape0) > 9
        r = analyse(tag, tau, third_names=["GB", "f", "ff03-ff14SB"] if big else None)
        json.dump(r, open(outp, "w"), indent=0)
        print(f"   [{r.get('seconds', 0):.0f}s] -> out/an_{tag}_tau{tau:.2f}.json", flush=True)
