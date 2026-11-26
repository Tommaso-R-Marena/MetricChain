#!/usr/bin/env python3
"""ER3 review, E19(e): an independent replicate of the n = 12 four-body face frequencies near the quoted threshold
233, with the division's own decision procedure (kbody_capacity.is_face, validated in er3_kbody.py) on supports
drawn from the reviewer's random stream.  usage: er3_kbody_n12.py K trials seed"""
import os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "experiments", "ensemble")))
sys.dont_write_bytecode = True
import kbody_capacity as KB                                   # noqa: E402

K, trials, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = np.random.default_rng(seed)
Z = KB.zstates(11); G = KB.monomials(Z, 4); N = G.shape[0]
t0 = time.time(); face = und = 0
for _ in range(trials):
    ans, it = KB.is_face(G, rng.choice(N, size=K, replace=False))
    if ans is None:
        und += 1
    else:
        face += bool(ans)
print(f"n = 12, four-body data, K = {K}: face in {face} of {trials} supports (undecided {und}); frequency {face / trials:.3f}   ({time.time() - t0:.0f} s)", flush=True)
