"""t12: the level recursion with the worst-case pair of a biased cube:
  T_k nonincreasing in k and in the accuracy; never below R^max (necessary condition of D45);
  approaches R^max; and stays strictly above R_0 (the hinted exponent of the instance g = 0)."""
import math, sys, numpy as np, time
from flib import *
from recursion import Recursion
t0 = time.time()
p, u = float(sys.argv[1]), float(sys.argv[2])
depth = int(sys.argv[3]) if len(sys.argv) > 3 else 12
wp = WorstPair(p, u)
w0 = WorstPair(p, u, gam_fixed=0.0)           # the instance g = 0 alone
print(f"p={p} u={u}: E={wp.E:.6f} h={wp.h:.6f} a={wp.a:.6f};   at g=0: threshold {w0.E:.6f}, R_0(0)={w0.h:.6f}")
r = Recursion(wp.theta_na, wp.R, wp.a, wp.h, wp.E)
rows = [("k=1 (non-adaptive)", r.T.copy())]
prev = r.T.copy()
ok_mono = ok_below = True
worst_def = 0.0
for k in range(2, depth + 1):
    r.step()
    ok_mono &= bool(np.all(r.T <= prev + 1e-12) and np.all(np.diff(r.T) <= 1e-12))
    worst_def = max(worst_def, float(np.max(r.hint - r.T)) / wp.a)
    prev = r.T.copy()
    if k in (2, 3, 4, 6, 9, 12, 16, 24):
        rows.append((f"k={k}", r.T.copy()))
idx = [int(np.argmin(np.abs(r.g - f * wp.E))) for f in (0.001, 0.02, 0.1, 0.25, 0.5, 0.75)]
print("  accuracy g/E:        " + "  ".join(f"{r.g[i]/wp.E:7.4f}" for i in idx))
for name, T in rows:
    print(f"  {name:20s} " + "  ".join(f"{T[i]/wp.a:7.4f}" for i in idx) + "   (T_k / a)")
print(f"  {'R^max / a':20s} " + "  ".join(f"{r.hint[i]/wp.a:7.4f}" for i in idx))
print(f"  {'R_0 / a (g = 0)':20s} " + "  ".join(f"{float(w0.R(r.g[i]))/wp.a:7.4f}" for i in idx))
print(f"  levels nonincreasing in k and in g: {ok_mono};  largest deficit max(R^max - T_k)/a over all levels: {worst_def:.2e};"
      f"  excess max(T_{depth} - R^max)/a = {float(np.max(r.T - r.hint))/wp.a:.4f}   [{time.time()-t0:.0f}s]")
