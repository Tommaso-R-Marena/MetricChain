# R9 test 5: exact finite-n sums on balls with type-dependent radii ("density balls") around one centre s.
#   hint:  the smallest density ball D_q(s) (largest type density q) whose deepest dip changes ln A by more than eps
#          at the instance g = 0, at gamma*|x| and at H  ->  every algorithm needs (1-2 delta)/q evaluations there
#          (Theorem 11.22(c) with a random permutation); reported n^-1 ln(1/q), maximised over 5 centre types.
#   non-adaptive: the smallest q for which truncating the cone u d(.,s) at the type-wise q-quantiles lowers ln A by more
#          than eps  ->  (1-2 delta)/q evaluations for non-adaptive algorithms (Theorem F4(b)(i)).
# usage: python3 r9_t5_finite.py p u frac n1,n2,...
import numpy as np, sys, time
from math import log, exp
from r9lib import Par
from r9prof import Grid, lse
p, u, frac = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
ns = [int(x) for x in sys.argv[4].split(',')]
t0 = time.time()
P = Par(p, u); E, gE, E0 = P.E(); e1 = frac * E
R0 = P.R0(e1); Rm, tst, gst = P.Rmax(e1, True); Rg = P.Rg(gst, e1); tna = P.theta_na(e1)
_, m0 = P.maxmin('R0', e1); _, mg = P.maxmin('Rg', e1, g=gst); _, mH = P.maxmin('Rmax', e1); _, mna = P.maxmin('na', e1)
print(f"p={p} u={u} eps1={frac}E={e1:.6f}: R0={R0:.6f} (m*={m0:.4f}); R^max={Rm:.6f} at gamma*={gst:+.4f} (centre types: gamma* {mg:.4f}, H {mH:.4f}); theta_na={tna:.6f} (m*={mna:.4f})   [{time.time()-t0:.0f}s]")
sys.stdout.flush()

def smallest_q(cumsorted, test):
    """smallest index i such that test(threshold = cumsorted[i]) holds (test is monotone)"""
    lo, hi = 0, len(cumsorted) - 1
    if not test(cumsorted[hi]): return None
    while lo < hi:
        mid = (lo + hi) // 2
        if test(cumsorted[mid]): hi = mid
        else: lo = mid + 1
    return cumsorted[lo]

res = {}
for n in ns:
    eps = e1 * n
    out = {}
    for name, mstar in (('g=0', m0), ('gamma*', mg), ('H', mH), ('nonadaptive', mna)):
        best = -1.0; bk = None
        for dm in (-0.04, -0.02, 0.0, 0.02, 0.04):
            k = int(round((mstar + dm) * n))
            if k < 1 or k > n - 1: continue
            gr = Grid(P, (k, n - k))
            lncum, d = gr.density_ball_order((1, 0))
            cs = np.unique(lncum[np.isfinite(lncum)])
            cs = cs[cs < -1e-12]                      # D must not contain a whole type class ... (q < 1)
            if name == 'nonadaptive':
                logw_cone = gr.logc + gr.logpi - u * d
                lnA_cone = lse(logw_cone)
                def test(thr):
                    D = lncum <= thr
                    # rho_t = least distance of a cell of type t outside D
                    rho = np.full(n + 1, 10 ** 9, dtype=np.int64)
                    np.minimum.at(rho, gr.ti[~D], d[~D])
                    lw = np.where(D, gr.logc + gr.logpi - u * rho[gr.ti], logw_cone)
                    return lnA_cone - lse(lw) > eps
            else:
                psi_t = {'g=0': np.zeros(n + 1), 'gamma*': gst * np.arange(n + 1.0), 'H': gr.psiH_t}[name]
                def test(thr):
                    D = lncum <= thr
                    if not D.any(): return False
                    ln_mu, ln_pp, ln_phi, ln_md = gr.stats(D, psi_t)
                    return np.logaddexp(0.0, ln_phi) > eps
            thr = smallest_q(cs, test)
            if thr is None: continue
            val = -thr / n
            if val > best: best, bk = val, k
        out[name] = (best, bk)
    res[n] = out
    print(f"n={n}: " + "; ".join(f"{nm}: {out[nm][0]:.6f} (k/n={out[nm][1]/n:.3f})" for nm in out) + f"   [{time.time()-t0:.0f}s]")
    sys.stdout.flush()
print("limits claimed:   g=0: R0 = %.6f; gamma*: R^max = %.6f; H: R^max = %.6f; non-adaptive: theta_na = %.6f" % (R0, Rm, Rm, tna))
if len(ns) >= 3:
    # least-squares fit  value = A + B ln(n)/n + C/n  through the last three sizes
    for nm, lim in (('g=0', R0), ('gamma*', Rm), ('H', Rm), ('nonadaptive', tna)):
        nn = np.array(ns[-3:], dtype=float); y = np.array([res[int(x)][nm][0] for x in nn])
        M = np.stack([np.ones(3), np.log(nn) / nn, 1 / nn], axis=1); A, B, C = np.linalg.solve(M, y)
        print(f"  {nm}: extrapolated {A:.6f} (coefficient of ln n/n: {B:+.2f}); formula {lim:.6f}; excess at the largest n: {(y[-1]-lim)*nn[-1]/log(nn[-1]):+.2f} ln n/n")
print(f"[{time.time()-t0:.0f}s]")
