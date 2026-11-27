#!/usr/bin/env python3
"""R19: the first-order cost of the evaluation allowance attached term by term, 2 beta <A_M>, A_M(x) = eps_g (1 + sum_{j=1}^{M} C(t, j) 2^j),
t = number of sites off the anchor, under exact samples of the floor and of the ceiling of a stored case (they bracket the true ensemble's
occupancies).  Used only to say how much of a corrected bracket the allowance can be.  Run: python3 -B r19_allowance_first_order.py case.pkl N"""
import os, sys, math, pickle, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
SCI = "/home/user/MetricChain/experiments/science"
sys.path.insert(0, os.path.join(SCI, "ws_P3")); sys.path.insert(0, os.path.join(SCI, "pi_inference"))
import numpy as np
import pwmodel as pw, window_model
WindowModel, _b, _d = window_model.make(pw)
C = pickle.load(open(sys.argv[1], "rb")); N = int(sys.argv[2]); n, k, w, beta = C["n"], C["k"], C["w"], C["beta"]; x0 = np.array(C["x0"]); EPS = 1e-7
def build(T):
    mdl = WindowModel(k, w); mdl.const = T["const"]; mdl.one = [np.array(v) for v in T["one"]]
    for (i, j), tab in T["pair"].items(): mdl.add_pair(i, j, tab)
    for U, tab in T["multi"].items(): mdl.add_multi(U, tab)
    return mdl
for name, T, seed in (("ceiling", C["up"], 71), ("floor", C["lo"], 72)):
    X = build(T).sample(N, np.random.default_rng(seed)); t = (X != x0[None]).sum(1); cnt = np.bincount(t, minlength=n + 1) / N
    out = []
    for M in (2, 3, 4):
        A = EPS * np.array([1.0 + sum(math.comb(tt, j) * 2 ** j for j in range(1, M + 1)) for tt in range(n + 1)])
        out.append(f"order {M + 1}: 2 beta <A> = {2 * beta * float(cnt @ A):.3g} nats")
    print(f"case {C['args']}, {N} exact samples of the {name}: mean number of sites off the anchor {float(t.mean()):.3f}; distribution {np.round(cnt[:7], 4).tolist()}; " + "; ".join(out))
print(f"ALL DONE; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
