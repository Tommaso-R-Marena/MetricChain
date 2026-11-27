#!/usr/bin/env python3
"""V9 -- regenerate the ten explicit bridges of THEORY_REPORT 11.22 (after Theorem 11.71(c)) with OUR builder
(experiments/workstreams/S/code/build.py + lat.py; keys of experiments/workstreams/S/out/witnesses.txt), exactly as
experiments/coordinator_checks/limit_shape_review/gen_witness.py does, but writing the coordinates into the scratch
directory (nothing is written into the repository; bytecode writing is off).

usage: v9_gen_witness.py OUTDIR W key [key ...]
"""
import sys, os, time
sys.dont_write_bytecode = True
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
SCODE = os.path.join(REPO, "experiments", "workstreams", "S")
sys.path.insert(0, os.path.join(SCODE, "code"))
import numpy as np
import build as B

wit = {}
lines = open(os.path.join(SCODE, "out", "witnesses.txt")).read().splitlines()
for i, l in enumerate(lines):
    if l.startswith("== ") and i + 1 < len(lines) and lines[i + 1].startswith("witness"):
        wit[l[3:].strip()] = lines[i + 1]
outdir = sys.argv[1]
W = int(sys.argv[2])
os.makedirs(outdir, exist_ok=True)
for key in sys.argv[3:]:
    t0 = time.time()
    hnf, ch = B.parse(wit[key])
    strands = B.strands_in_box(hnf, ch, (W, W, W))
    walk, nlink, dropped, ns = B.link(strands)
    b = B.make_bridge(walk)
    tag = "".join(c if c.isalnum() else "_" for c in key) + "_W%d" % W
    if b is None:
        print(f"{key}: builder failed")
        continue
    np.save(os.path.join(outdir, tag + ".npy"), np.array(b, dtype=np.int32))
    print(f"{key} | box {W} | strands {ns}, linker sites {nlink}, not linked {dropped} | N = {len(b)} | file {tag}.npy | {time.time()-t0:.1f} s", flush=True)
