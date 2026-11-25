"""Finding M1, second half.  In the cells of the grid t07c where the uniform cube's profile
mu* = (1/2; p_u, p_u) has the value 0 at a coupling below bJ*(e,u): is there ANY profile -- binary or
with more blocks -- whose value comes near R_unif(e)?  (If yes, "R_H = R_unif for bJ <= bJ*" could
still be true for another reason; if not, the junction really is earlier.)

Outer search: alternating SLP (finite-mass moves on the law of the block types) and Nelder-Mead, from
starts adapted to the cell (the best symmetric binary shell, asymmetric binary profiles, diluted shells
with a free block, four-atom symmetric profiles, frozen coordinates, off-centre types) and from random
splittings/perturbations of them.  The best profiles are re-evaluated with S1 (fine), S2 (dual per
exit type, with I) and S3 (primal SLSQP, with I), which share no approximation.

The supremum sits on a cliff: the value of a profile drops to 0 when a constant exit near a well
(MI = 0) becomes feasible, and at the edge the three inner solvers may fall on different sides
(first run of this script: S1 = S2 = 0.36742, S3 = 0 at the edge profile).  Therefore the SEARCH is
done at the accuracy e + delta (delta = 2e-5; r_mu(e + delta) <= r_mu(e), so it only loses), and the
profiles it returns are evaluated at the accuracy e itself, where the constant exits are infeasible
by a margin and the three solvers must agree.

usage: python3 t24_junction_multi.py u etag f seed nrandom tlimit
       etag in {0, 0.3ec, 0.6ec, 0.9ec}; the coupling is bJ = 1 + f (bJ*(e,u) - 1)."""
import time, sys
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
from r10slp import *

u = float(sys.argv[1]); etag = sys.argv[2]; f = float(sys.argv[3])
seed, nrandom = int(sys.argv[4]), int(sys.argv[5]); tlimit = float(sys.argv[6])
t0 = time.time()
pu = p_u(u)
ec = -float(kl(pu, 0.5))
e = {"0": 0.0, "0.3ec": 0.3 * ec, "0.6ec": 0.6 * ec, "0.9ec": 0.9 * ec}[etag]
rho = (Lam1(u) + e) / u
c2 = 1.0 / (2 * rho * (1 - rho)) - 2.0
L = np.log((1 - rho) / rho)
bJs = 1.0 + u * c2 / (2 * L)
bJ = 1.0 + f * (bJs - 1.0)
M = Model(bJ=bJ, bB=0.0, u=u)
phip = lambda k: -2 * bJ * (2 * k - 1)
rng = np.random.default_rng(seed)
Ru = R_unif(e, u)
fine = dict(G=400, zooms=5, ncand=6, nz=41, rounds=8)
print(f"# u={u} e={e:+.6f} ({etag}) bJ*={bJs:.5f} bJ={bJ:.5f} (f={f}) p_u={pu:.6f} R_unif(e)={Ru:.9f} seed={seed}")
print(f"# contact set {[(round(float(a),4), round(float(b),4)) for a,b in M.contact()]}  I(1/2)={float(M.I(0.5)):.5f}  well at {M.kmin:.3e}", flush=True)


delta = 2e-5
es = e + delta                      # accuracy used in the search


def val(lam, mu, kw=None, acc=None):
    v = r_mu(M, np.asarray(lam, float), np.asarray(mu, float), es if acc is None else acc, **(kw or {}))
    return float(v) if np.isfinite(v) else -1.0


cgrid = np.unique(np.concatenate((np.linspace(0.0, 1.0, 20001), np.exp(np.linspace(np.log(1e-9), np.log(0.5), 4000)),
                                  1 - np.exp(np.linspace(np.log(1e-9), np.log(0.5), 4000)))))
Icg = M.I(cgrid)


def const_margin(lam, mu, acc):
    """min over constant exits (c, ..., c) of  u dist + I(c)  minus the budget acc + alpha(mu);
    positive = every exit with MI = 0 is infeasible"""
    lam = np.asarray(lam, float); mu = np.asarray(mu, float)
    cost = u * (np.abs(mu[None, :] - cgrid[:, None]) @ lam) + Icg
    j = int(np.argmin(cost))
    return float(cost[j] - (acc + alpha(M, lam, mu))), float(cgrid[j])


# the uniform cube's profile and the best symmetric binary shell (scan + golden section, S1 fine)
lam0, mu0 = binary(0.5, pu, pu)
cm, cc = const_margin(lam0, mu0, e)
print(f"# mu* at the accuracy e: r = {val(lam0, mu0, fine, acc=e):.9f}; cheapest constant exit at type {cc:.3e}, margin {cm:+.3e} (negative = feasible)")
print(f"# search accuracy e + delta, delta = {delta}")
xs = np.exp(np.linspace(np.log(pu * 0.5), np.log(0.3), 240))
vs = np.array([val(*binary(0.5, x, x)) for x in xs])
i = int(np.argmax(vs))
lo, hi = xs[max(i - 1, 0)], xs[min(i + 1, len(xs) - 1)]
res = optimize.minimize_scalar(lambda x: -val(*binary(0.5, x, x), kw=fine), bounds=(lo, hi), method='bounded',
                               options={'xatol': 1e-10})
xb, vb = float(res.x), -float(res.fun)
if vs[i] > vb:
    xb, vb = float(xs[i]), float(vs[i])
print(f"# best symmetric binary shell: x = {xb:.6f}, value {vb:.9f}; R_unif - value = {Ru - vb:+.3e}; "
      f"positive values for x in [{xs[vs > 0].min() if (vs > 0).any() else np.nan:.5f}, {xs[vs > 0].max() if (vs > 0).any() else np.nan:.5f}]", flush=True)
Kb = float(kl(xb, 0.5))


def x_with_kl(target):
    """x <= 1/2 with KL(x || 1/2) = target (target < ln 2)"""
    return float(optimize.brentq(lambda x: float(kl(x, 0.5)) - target, 1e-12, 0.5))


starts = [("binary shell", binary(0.5, xb, xb))]
starts.append(("binary asym a", binary(0.47, xb, 1.15 * xb)))
starts.append(("binary asym b", binary(0.5, 0.8 * xb, 1.3 * xb)))
for ff in (0.03, 0.08, 0.15):
    tgt = min(0.985 * Kb / (1 - ff), 0.999 * np.log(2))
    xf = x_with_kl(tgt)
    starts.append((f"diluted {ff}", (np.array([(1 - ff) / 2, ff, (1 - ff) / 2]), np.array([1 - xf, 0.5, xf]))))
for (w2, s1, s2) in ((0.1, 0.6, 3.0), (0.2, 0.5, 2.0), (0.05, 0.9, 6.0)):
    starts.append((f"four atoms {w2}", (np.array([0.5 - w2, w2, w2, 0.5 - w2]),
                                         np.array([s1 * xb, min(s2 * xb, 0.45), 1 - min(s2 * xb, 0.45), 1 - s1 * xb]))))
for wf in (0.05, 0.12):
    tgt = min(0.985 * Kb, 0.999 * np.log(2))
    # frozen coordinates carry KL = ln 2 each: (2 wf) ln 2 + (1 - 2 wf) KL(x) = tgt
    rest = (tgt - 2 * wf * np.log(2)) / (1 - 2 * wf)
    if rest > 0:
        xf = x_with_kl(rest)
        starts.append((f"frozen {wf}", (np.array([wf, 0.5 - wf, 0.5 - wf, wf]), np.array([1e-9, xf, 1 - xf, 1 - 1e-9]))))
starts.append(("off-centre", (np.array([0.5, 0.5]), np.array([1 - xb - 0.03, xb]))))
base = list(starts)
for s in range(nrandom):
    name, (lam, mu) = base[s % len(base)]
    for attempt in range(6):
        sc = 0.35 * 0.6 ** attempt
        w = rng.dirichlet(np.ones(2) * 3, size=len(mu))
        l2 = (np.asarray(lam)[:, None] * w).ravel()
        t = np.log(np.clip(np.repeat(mu, 2), 1e-9, 1 - 1e-9) / (1 - np.clip(np.repeat(mu, 2), 1e-9, 1 - 1e-9)))
        m2 = 1 / (1 + np.exp(-(t + sc * rng.standard_normal(len(t)))))
        if rng.random() < 0.5:
            wfree = rng.uniform(0.0, 0.1) * 0.6 ** attempt
            l2 = np.concatenate(((1 - wfree) * l2, [wfree])); m2 = np.concatenate((m2, [rng.uniform(0.05, 0.95)]))
        if val(l2, m2) > 0:
            starts.append((f"rand{s}({name})", (l2, m2)))
            break
print(f"# {len(starts)} starts", flush=True)

results = []
for name, (lam, mu) in starts:
    if time.time() - t0 > tlimit:
        print("# time limit: remaining starts skipped", flush=True)
        break
    lam = np.asarray(lam, float) / np.sum(lam); mu = np.asarray(mu, float)
    cur = val(lam, mu)
    v0 = cur
    cyc = 0
    for cyc in range(3):
        cand = []
        try:
            v1, l1, m1, hist = slp(M, lam, mu, es, phip, nM=801, iters=12)
            if np.isfinite(v1):
                cand.append((float(v1), l1, m1))
                l2, m2 = coarsen(l1, m1, tol=0.002)
                v2 = val(l2, m2)
                if v2 > 0:
                    cand.append((v2, l2, m2))
                    l1, m1 = l2, m2
            else:
                l1, m1 = lam, mu
        except Exception as ex:                      # the search is heuristic; a failure of a step is not a result
            print(f"   ({name}: SLP step failed: {type(ex).__name__})", flush=True)
            l1, m1 = lam, mu
        if len(m1) <= 8:
            v3, l3, m3 = nm(M, es, l1, m1, maxiter=300 * len(m1))
            cand.append((float(v3), l3, m3))
        cand.append((cur, lam, mu))
        best = max(cand, key=lambda c: c[0])
        if best[0] <= cur + 2e-9:
            break
        cur, lam, mu = best
        if time.time() - t0 > tlimit:
            break
    lam, mu = merge(lam, mu, tol=1e-5, wmin=1e-6)
    results.append((cur, lam, mu, name))
    print(f"{name:26s} v0={v0:.7f} -> {cur:.9f} ({cyc+1} cycles) [{fmt(lam, mu)}] type {float(lam@mu):.4f} MI {float(MI(lam, mu)):.5f} t={time.time()-t0:.0f}", flush=True)

results.sort(key=lambda r: -r[0])
lb, mb_ = binary(0.5, xb, xb)
print(f"# best symmetric binary shell (found at e + delta): x = {xb:.6f}; R_unif(e) = {Ru:.9f}")
print("# evaluation AT THE ACCURACY e with three inner solvers (S1 fine: clippings, v; S2: dual per exit type, I; S3: primal SLSQP, I):")
todo = [("best symmetric binary shell", lb, mb_)] + [(name, l3, m3) for v3, l3, m3, name in results[:3]]
best_three = -1.0
for name, l3, m3 in todo:
    B = e + alpha(M, l3, m3)
    if B < float(M.v(float(l3 @ m3))) - 1e-13:
        print(f"  {name}: not admissible at e")
        continue
    s1 = inner_clip(M, l3, m3, B, **fine)[0]
    s2, k2, loc = inner_dual(M, l3, m3, B, nk=1201, refine=5)
    s3 = inner_primal(M, l3, m3, B, nstart=30)[0]
    cm, cc = const_margin(l3, m3, e)
    agree = max(s1, s2, s3) - min(s1, s2, s3)
    if agree < 1e-5:
        best_three = max(best_three, min(s1, s2, s3))
    print(f"  {name}: [{fmt(l3, m3)}] type {float(l3@m3):.5f} MI {float(MI(l3, m3)):.6f}\n"
          f"     S1 {s1:.9f}  S2 {s2:.9f}  S3 {s3:.9f}  (spread {agree:.1e});  R_unif - S1 = {Ru - s1:+.4e};  "
          f"cheapest constant exit: type {cc:.3e}, margin {cm:+.3e}\n"
          f"     local minima over exit types {[(round(a,4), round(b,8)) for a,b in loc[:5]]}", flush=True)
vbs = val(lb, mb_, fine)
print(f"# search values (at e + delta): best symmetric binary shell {vbs:.9f}; starts that end above it by more than 1e-7: "
      f"{sum(1 for r in results if r[0] > vbs + 1e-7)} of {len(results)}; best search value {results[0][0]:.9f}")
print(f"# largest value at e on which the three solvers agree to 1e-5: {best_three:.9f}; R_unif(e) - it = {Ru - best_three:+.4e}")
print("# time", time.time() - t0)
