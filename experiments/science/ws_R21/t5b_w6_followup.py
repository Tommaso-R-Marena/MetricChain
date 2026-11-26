"""T5b - follow-up of logs/t5_W6_K3_run1.log, ensemble 2: g1 = 1.190e-09 (LM), min exact defect 5.4e-07.
A residual of 1e-9 is three orders above what realisable targets reach (<= 1e-12) and three orders below the
other ensembles: converged positive minimum (near-chimera), true zero (a chimera - would contradict E5(a) for a
random ensemble), or an artefact of a degenerate configuration?  The random stream of t5_gap_scaling.py is
replayed exactly (same seed, same sequence of calls) up to ensemble 2."""
import numpy as np
import mpmath as mp
from r21_common import *

name, K, starts, seed = "W6", 3, 12, 2105
rng = np.random.default_rng(seed)
N, E = graph_table()[name]
m = len(E)
R = Realiser(N, E)
C = Constructor(name, N, E)
CAP = 1000
print("T5b start", now())
for ens in range(3):
    X = rng.standard_normal((K, N, 2))
    Tc = sqlen(X, E)
    col = all_colourings(K, m)
    col = col[nonconstant(col)]
    T = splice_targets(Tc, col)
    ex, _ = C.defect(T)
    sel = np.unique(np.concatenate([np.argsort(ex)[:CAP], rng.choice(len(col), CAP, replace=False)]))
    best, bestZ, _ = R.multistart(T[sel], starts, rng)
    i = int(np.argmin(best))
    print("replay ens %d: g1 = %.3e, min exact defect %.3e" % (ens, best[i], ex.min()))
ci = sel[i]
t = T[ci:ci + 1]
print("ensemble 2: colouring #%d %s ; LM residual %.6e ; exact defect of this colouring %.6e ; rank of this colouring by exact defect: %d"
      % (ci, ''.join(map(str, col[ci])), best[i], ex[ci], int(np.sum(ex < ex[ci]))))
print("target squared lengths:", np.array2string(t[0], precision=6))
print("conformer squared lengths (rows = conformers):"); print(np.array2string(Tc, precision=4))
print("differences |t_e(x_i) - t_e(x_j)| smallest three:", np.array2string(np.sort(np.abs(Tc[:, None] - Tc[None])[np.triu_indices(K, 1)].ravel())[:3], precision=5))
# how many edges does the colouring take from each conformer; distance of the target to each conformer's vector
print("edges per conformer:", [int(np.sum(col[ci] == c)) for c in range(K)], "; ||target - t(x_c)||_2 for c = 0,1,2:",
      np.array2string(np.linalg.norm(t - Tc, axis=1), precision=4))
z0 = bestZ[i:i + 1].copy()
P0 = embed(z0, N)[0]
print("LM minimiser, coordinates:", np.array2string(P0, precision=5).replace("\n", ""))
for (a, b) in [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5)]:
    u_, v_ = P0[a] - P0[0], P0[b] - P0[0]
    print("   hub triangle (0,%d,%d): signed area %.4e" % (a, b, 0.5 * (u_[0] * v_[1] - u_[1] * v_[0])))
r, J = R.res_jac(z0, t)
sv = np.linalg.svd(J[0], compute_uv=False)
print("at the LM minimiser: residual %.10e, gradient norm %.2e, singular values of J: %s" % (np.linalg.norm(r), np.linalg.norm(np.einsum('bmn,bm->bn', J, r)), np.array2string(sv, precision=3)))
# (1) more iterations from the minimiser and from 400 random starts
r2 = np.random.default_rng(11)
for iters in (1000, 10000):
    Zs = np.vstack([z0, 1.5 * r2.standard_normal((400, R.n))])
    Z, res = R.solve(np.repeat(t, len(Zs), axis=0), Zs, iters=iters)
    k = int(np.argmin(res))
    print("LM %5d iterations: from the minimiser -> %.10e ; best of 400 random starts -> %.10e ; number of starts below 1e-7: %d"
          % (iters, res[0], res[1:].min(), int(np.sum(res[1:] < 1e-7))))
zbest = Z[0:1].copy() if res[0] <= res[1:].min() else Z[k:k + 1].copy()
# (2) exact enumeration: check-edge deviation for every flip pattern
for bits, (P, feas) in enumerate(C.realisations(t)):
    dev = sqlen(P, C.check)[0] - t[0, [C.idx[e] for e in C.check]]
    if feas[0] and abs(dev[0]) < 1e-2:
        print("   flip pattern %2d: feasible, check-edge deviation %.6e" % (bits, dev[0]))
# (3) 40-digit arithmetic: least-squares stationarity by Newton on the gradient of ||F(z) - t||^2 from the float minimiser
mp.mp.dps = 40
I = [e[0] for e in E]; Jx = [e[1] for e in E]
tt = [mp.mpf(float(v)) for v in t[0]]            # the float64 targets, taken as exact rational data
def emb(z):
    P = [[mp.mpf(0), mp.mpf(0)], [z[0], mp.mpf(0)]]
    for k in range(2, N):
        P.append([z[2 * k - 3], z[2 * k - 2]])
    return P
def resid(z):
    P = emb(z)
    return [(P[a][0] - P[b][0]) ** 2 + (P[a][1] - P[b][1]) ** 2 - tt[q] for q, (a, b) in enumerate(E)]
def grad(*z):
    z = list(z)
    h = mp.mpf(10) ** (-18)
    g = []
    for k in range(len(z)):
        zp = z[:]; zp[k] += h
        zm = z[:]; zm[k] -= h
        g.append((sum(x * x for x in resid(zp)) - sum(x * x for x in resid(zm))) / (2 * h))
    return g
zf = [mp.mpf(float(v)) for v in zbest[0]]
print("40-digit evaluation at the float minimiser: residual 2-norm = %s" % mp.nstr(mp.sqrt(sum(x * x for x in resid(zf))), 15))
try:
    sol = mp.findroot(grad, zf, tol=1e-30, maxsteps=50)
    zs = [sol[k] for k in range(len(zf))]
    rs = resid(zs)
    print("40-digit stationary point of ||F - t||^2 (Newton from the float minimiser): residual 2-norm = %s ; moved by %s"
          % (mp.nstr(mp.sqrt(sum(x * x for x in rs)), 15), mp.nstr(max(abs(a - b) for a, b in zip(zs, zf)), 5)))
    print("   residual per edge:", [mp.nstr(x, 4) for x in rs])
except Exception as exc:
    print("mpmath findroot failed:", repr(exc))
print("DONE t5b_w6_followup", now())
