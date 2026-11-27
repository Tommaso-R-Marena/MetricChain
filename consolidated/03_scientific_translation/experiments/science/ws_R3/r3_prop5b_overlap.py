#!/usr/bin/env python3
"""R3 — numerical check of the referee's proof of Proposition 5b for overlapping supports
(any u > 0): with integer r1 and s in [-1, 1],
   (i)  dominance:  W/2^n >= 2 e^u r1,   W = sum_{d<r1} C(n,d) e^{u(r1-d)};
   (ii) overlap:    omega(s)/W_twin(s) <= e^{-u}/(4(r1+1)),  omega = twin weight inside supp(g0);
   =>  U'(+1) < U0 < U'(-1), hence a root s* in (-1,1); ln Z' - ln Z0 >= ln(1+e^-u) - o(1).
Also the Hoeffding bound used for (ii):
   omega/W_twin <= max_j P(d(x,a0) < r1 | x uniform on the sphere S(a',j)) <= exp(-2 lam^2/r1),
   lam = min(D - r1, D(1 - 2 r1/n))/2.
"""
import math, warnings
import numpy as np
from scipy.special import logsumexp
from r3_prop5b import Twin, lbinom
warnings.filterwarnings("ignore")

for u in (0.5, 1.0, 2.0):
    rho0 = math.log(2 / (1 + math.exp(-u))) / u
    for n, dr in ((2000, 0.02), (4000, 0.01)):
        r1 = float(round((rho0 + dr) * n))
        d = np.arange(int(r1))
        lW = logsumexp(lbinom(n, d) + u * (r1 - d)) - n * math.log(2)
        dom = lW >= math.log(2 * math.exp(u) * r1)
        for frac in (0.45, 0.5, 0.55):
            D = int(frac * n)
            tw = Twin(n, u, r1, D)
            out = []
            for s in (-1.0, 1.0):
                T = -u * np.maximum(r1 + s - tw.d1, 0.0)
                inO = (tw.g0 < 0) & (T < 0)
                lw_tw = logsumexp((tw.lc - T)[T < 0])
                lom = logsumexp((tw.lc - T)[inO]) if inO.any() else -np.inf
                out.append(lom - lw_tw)
            lam = min(D - r1, D * (1 - 2 * r1 / n)) / 2
            hoeff = -2 * lam * lam / r1
            fp, fm = tw.dU(1.0 - 1e-12), tw.dU(-1.0 + 1e-12)
            s_, _, _ = tw.root()
            E, _ = tw.excess(s_) if s_ is not None else (float('nan'), 0)
            print(f"u={u} n={n} r1={r1:.0f} D={D}: ln(W/2^n)={lW:7.2f} (dominance {dom}); ln(omega/W_twin) at s=-1,+1: "
                  f"{out[0]:8.1f}, {out[1]:8.1f} <= Hoeffding {hoeff:8.1f}: {max(out) <= hoeff + 1e-9}; needed <= {math.log(math.exp(-u) / (4 * (r1 + 1))):6.1f}; "
                  f"U'(+1)-U0={fp:+.3e}, U'(-1)-U0={fm:+.3e}; root {None if s_ is None else round(s_, 6)}; "
                  f"lnZ'-lnZ0={math.log1p(E):.4f} (>= {math.log(1 + math.exp(-u)):.4f})", flush=True)
            if dom and max(out) <= math.log(math.exp(-u) / (4 * (r1 + 1))):
                assert fp < 0 < fm and s_ is not None
