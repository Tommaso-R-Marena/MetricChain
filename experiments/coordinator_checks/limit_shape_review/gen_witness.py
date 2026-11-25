#!/usr/bin/env python3
"""Assistant B — regenerate the explicit bridges of S_REPORT §4.2 with OUR builder (experiments/workstreams/S/code/build.py + lat.py, witness lines parsed from
experiments/workstreams/S/out/witnesses.txt) and store the coordinates.  Nothing is verified here; verification
is in verify_witness.py with own code that imports nothing of the builder.

usage: gen_witness.py W key [key ...]      key = the label after '== ' in witnesses.txt, e.g. "(0,3,4) W3"
"""
import sys, os, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SCODE = os.path.join(HERE, "..", "..", "workstreams", "S")
sys.path.insert(0, os.path.join(SCODE, "code"))
import numpy as np
import build as B

wit = {}
lines = open(os.path.join(SCODE, "out", "witnesses.txt")).read().splitlines()
for i, l in enumerate(lines):
    if l.startswith("== ") and i + 1 < len(lines) and lines[i + 1].startswith("witness"):
        wit[l[3:].strip()] = lines[i + 1]
W = int(sys.argv[1])
for key in sys.argv[2:]:
    t0 = time.time()
    hnf, ch = B.parse(wit[key])
    strands = B.strands_in_box(hnf, ch, (W, W, W))
    walk, nlink, dropped, ns = B.link(strands)
    b = B.make_bridge(walk)
    tag = "".join(c if c.isalnum() else "_" for c in key) + "_W%d" % W
    if b is None:
        print(f"{key}: builder failed")
        continue
    np.save(os.path.join(HERE, "wit", tag + ".npy"), np.array(b, dtype=np.int32))
    print(f"{key} | box {W} | strands {ns}, linker sites {nlink}, not linked {dropped} | N = {len(b)} | file wit/{tag}.npy | {time.time()-t0:.1f} s", flush=True)
