#!/usr/bin/env python3
"""R22 Item 3(b): Theorem G (ENSEMBLE_RIGIDITY.md l.487-532) numerically, own code.

Pair of generic chains (K = 2), n = 12, 13, 14 (and 16, 20 for the trend), unit bonds, cos(bond angle) = -1/3,
weights (0.4, 0.6).  phi(X) = ||Pi_perp X||_F^2, Pi_perp = projector of R^n off span(1, columns of z).
 (a) phi >= 0; phi = -1/2 <Pi_perp, D(X)>; phi(X_k) = 0.
 (b) kappa = inf_C phi(X) / min_k d_P(X, X_k)^2:
     local value at X_k = smallest generalised eigenvalue of Pi_perp on (flex space minus infinitesimal isometries),
     validated by the ratio on a short step along the eigen-direction;
     global: random conformations and local minimisation (L-BFGS-B, finite-difference gradients) from the best samples
     and from perturbations of the states.  Reported: the smallest value found and where.
 (c) the inequality  int min_k d_P^2 dnu <= sqrt(n-1-6) / (2 kappa) ||M(nu) - M(mu)||_F  with kappa replaced by the
     smallest ratio found (an UPPER estimate of kappa, so a violation would only mean kappa is smaller): slack on
     random ensembles and on symmetric broadenings; the size of ||dM|| below which the bound beats the trivial bound.
 (d) infinitesimal identifiability: smallest singular value of (a, tau) -> sum a_k D(X_k) + sum L_k(tau_k).
 (e) broadening of one state: exponents of ||dM|| and W_2^2 in eps; control: a one-sided shift.
 (w) the hypotheses actually used by the proof of (a)-(b) -- (H1) the only linear images of z that are chains are
     the states, (H2) no flex of the form z B^T + 1 t^T -- on pairs where (CC) FAILS: two and three differing torsions.
Controls: a random ensemble must have int phi dnu = -1/2 <Pi_perp, M(nu) - M(mu)> to rounding; the local value must be
reproduced by the ratio along the eigen-direction; phi of a random conformation must be > 0.
Run: OMP_NUM_THREADS=1 python3 -B t3b_theorem_G.py > t3b_theorem_G.log        (about 6 minutes)
"""
import time
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize
import r22lib as L

t0 = time.time()
COS = -1.0 / 3.0
W = (0.4, 0.6)
viol = 0


def flex_basis(tors, X):
    """torsion tangents with the infinitesimal isometries projected out; rows = flattened fields"""
    T = L.torsion_tangents(tors, COS).reshape(len(tors), -1)
    Q = L.iso_basis(X)
    return T - (T @ Q.T) @ Q, T


def local_kappa(tors, X, Pp):
    Tp, T = flex_basis(tors, X)
    n = len(X)
    PT = np.einsum("ij,ajk->aik", Pp, Tp.reshape(len(tors), n, 3)).reshape(len(tors), -1)
    Nmat = Tp @ PT.T
    G = Tp @ Tp.T
    lam, V = eigh((Nmat + Nmat.T) / 2, (G + G.T) / 2)
    return lam, V, Tp


def analyse(n, seed, nsamp, nstart, hinges=None, label="generic pair"):
    global viol
    rng = np.random.default_rng(seed)
    t1 = rng.uniform(-np.pi, np.pi, n - 3)
    if hinges is None:
        t2 = rng.uniform(-np.pi, np.pi, n - 3)
    else:
        t2 = t1.copy()
        for h in hinges:
            t2[h] += rng.uniform(0.6, 2.5) * rng.choice([-1, 1])
    X = [L.chain(t1, COS), L.chain(t2, COS)]
    tt = [t1, t2]
    z = L.stack(X, W)
    dimN = L.conic_nullity(z)[0]
    Pp, r = L.perp_projector(z)
    D = [L.sqdist(Xk) for Xk in X]
    M = W[0] * D[0] + W[1] * D[1]

    def phi(Y):
        return float(((Pp @ Y) ** 2).sum())

    def dmin2(Y):
        return min(L.procrustes2(Y, X[0]), L.procrustes2(Y, X[1]))

    # (a)
    a1 = max(phi(X[0]), phi(X[1]))
    a2 = 0.0
    a3 = np.inf
    for _ in range(200):
        Y = L.chain(rng.uniform(-np.pi, np.pi, n - 3), COS)
        a2 = max(a2, abs(phi(Y) + 0.5 * (Pp * L.sqdist(Y)).sum()))
        a3 = min(a3, phi(Y))
    viol += int(a1 > 1e-20 or a2 > 1e-10 or a3 <= 0)
    # (b) local
    loc = []
    for k in range(2):
        lam, V, Tp = local_kappa(tt[k], X[k], Pp)
        v = V[:, 0]
        # validation: ratio on a short step along the softest direction (in torsion space)
        eps = 1e-4
        Y = L.chain(tt[k] + eps * v, COS)
        ratio = phi(Y) / L.procrustes2(Y, X[k])
        loc.append((lam[0], lam[1], lam[-1], ratio))
        viol += int(abs(ratio - lam[0]) > 2e-2 * max(lam[0], 1e-12) + 1e-9)
    kloc = min(l[0] for l in loc)

    # (b) global
    def ratio_fn(t):
        Y = L.chain(t, COS)
        d2 = dmin2(Y)
        if d2 < 1e-12:
            return kloc
        return phi(Y) / d2

    samples = rng.uniform(-np.pi, np.pi, (nsamp, n - 3))
    vals = np.array([ratio_fn(t) for t in samples])
    best_sample = float(vals.min())
    order = np.argsort(vals)[: nstart // 2]
    starts = [samples[i] for i in order]
    for k in range(2):
        for _ in range(nstart // 4):
            starts.append(tt[k] + rng.normal(size=n - 3) * rng.choice([0.05, 0.3, 1.0]))
    best, best_t, best_d = np.inf, None, None
    nloc_min = []
    for s in starts:
        res = minimize(ratio_fn, s, method="L-BFGS-B", options={"maxiter": 300, "ftol": 1e-13, "gtol": 1e-10})
        d2 = dmin2(L.chain(res.x, COS))
        nloc_min.append((res.fun, d2))
        if res.fun < best:
            best, best_t, best_d = float(res.fun), res.x.copy(), d2
    away = [f for f, d2 in nloc_min if d2 > 1e-4]
    best_away = min(away) if away else float("nan")
    kap = min(best, kloc)
    diam2 = max(dmin2(L.chain(t, COS)) for t in samples[:2000])
    # (c) slack
    sl_rand, sl_broad = [], []
    c_id = 0.0
    for _ in range(200):
        J = int(rng.integers(1, 6))
        Ys = [L.chain(rng.uniform(-np.pi, np.pi, n - 3), COS) for _ in range(J)]
        wv = rng.dirichlet(np.ones(J))
        Mn = sum(wj * L.sqdist(Yj) for wj, Yj in zip(wv, Ys))
        lhs = sum(wj * dmin2(Yj) for wj, Yj in zip(wv, Ys))
        eta = np.linalg.norm(Mn - M)
        c_id = max(c_id, abs(sum(wj * phi(Yj) for wj, Yj in zip(wv, Ys)) + 0.5 * (Pp * (Mn - M)).sum()))
        rhs = np.sqrt(r) / (2 * kap) * eta
        sl_rand.append(lhs / rhs)
    viol += int(c_id > 1e-9)
    lam, V, Tp = local_kappa(tt[0], X[0], Pp)
    for eps in (1e-1, 1e-2, 1e-3):
        v = V[:, 0] / np.linalg.norm(V[:, 0])
        Yp, Ym = L.chain(t1 + eps * v, COS), L.chain(t1 - eps * v, COS)
        Mn = W[0] * 0.5 * (L.sqdist(Yp) + L.sqdist(Ym)) + W[1] * D[1]
        lhs = W[0] * 0.5 * (dmin2(Yp) + dmin2(Ym))
        rhs = np.sqrt(r) / (2 * kap) * np.linalg.norm(Mn - M)
        sl_broad.append(lhs / rhs)
    # (d) infinitesimal identifiability
    iu = [(i, j) for i in range(n) for j in range(i + 3, n)]
    cols = [np.array([D[0][i, j] - D[1][i, j] for i, j in iu])]
    for k in range(2):
        T = L.torsion_tangents(tt[k], COS)
        for j in range(n - 3):
            dD = 2.0 * ((X[k][:, None, :] - X[k][None, :, :]) * (T[j][:, None, :] - T[j][None, :, :])).sum(-1)
            cols.append(np.array([dD[a, b] for a, b in iu]))
    Jm = np.array(cols).T
    Jn = Jm / np.linalg.norm(Jm, axis=0)
    sv = np.linalg.svd(Jn, compute_uv=False)
    return dict(n=n, label=label, dimN=dimN, r=r, a=(a1, a2, a3), loc=loc, best_sample=best_sample, best=best, best_d=best_d,
                best_away=best_away, kap=kap, diam2=diam2, sl_rand=(min(sl_rand), float(np.median(sl_rand)), max(sl_rand)),
                sl_broad=sl_broad, sv=(sv[-1], sv[0], Jm.shape), Mnorm=float(np.linalg.norm(M)), c_id=c_id,
                X=X, tt=tt, Pp=Pp, D=D, M=M)


print("=== R22 3(b): Theorem G numerically (own code); K = 2, weights 0.4/0.6, cos(bond angle) = -1/3")
print("\n--- (a), (b): the certificate phi and its growth")
print("| pair | n | dim N(z) | rank Pi_perp | phi at the states | max |phi + <Pi,D>/2| | min phi on 200 random chains | "
      "local value at X_1 (softest, next; stiffest) | check along the soft direction | local value at X_2 | check | "
      "smallest ratio among random chains | smallest ratio after local minimisation (d_P^2 of the minimiser to the nearer state) | "
      "smallest local minimum with d_P^2 > 1e-4 | kappa estimate = min(local values, global search) |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
R = []
for (n, seed, nsamp, nstart) in ((12, 2281, 20000, 48), (12, 2282, 20000, 48), (13, 2283, 20000, 48), (14, 2284, 20000, 48),
                                 (14, 2285, 20000, 48), (16, 2286, 10000, 32), (20, 2287, 10000, 32)):
    d = analyse(n, seed, nsamp, nstart)
    R.append(d)
    l1, l2 = d["loc"]
    print(f"| generic, seed {seed} | {n} | {d['dimN']} | {d['r']} | {d['a'][0]:.1e} | {d['a'][1]:.1e} | {d['a'][2]:.3f} | "
          f"{l1[0]:.3e}, {l1[1]:.3e}; {l1[2]:.3f} | {l1[3]:.3e} | {l2[0]:.3e} | {l2[3]:.3e} | {d['best_sample']:.3e} | "
          f"{d['best']:.3e} ({d['best_d']:.2e}) | {d['best_away']:.3e} | {d['kap']:.3e} |", flush=True)

print("\n--- (c): what the inequality gives with the kappa estimate (an upper estimate of kappa)")
print("| n | seed | kappa est. | constant sqrt(n-7)/(2 kappa) | ||M(mu)||_F | largest min_k d_P^2 on 2000 random chains ('diam^2') | "
      "||dM||_F below which the bound beats the trivial bound diam^2 | the same relative to ||M(mu)||_F | "
      "slack LHS/RHS on 200 random ensembles (min, median, max) | LHS/RHS for a symmetric broadening of X_1 along its softest flex, eps = 1e-1, 1e-2, 1e-3 | "
      "max |int phi dnu + <Pi, dM>/2| |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for d in R:
    C = np.sqrt(d["r"]) / (2 * d["kap"])
    eta_star = d["diam2"] / C
    print(f"| {d['n']} | | {d['kap']:.3e} | {C:.3e} | {d['Mnorm']:.2f} | {d['diam2']:.2f} | {eta_star:.3e} | {eta_star / d['Mnorm']:.2e} | "
          f"{d['sl_rand'][0]:.2e}, {d['sl_rand'][1]:.2e}, {d['sl_rand'][2]:.2e} | " + ", ".join(f"{s:.3f}" for s in d["sl_broad"]) + f" | {d['c_id']:.1e} |")
    viol += int(d["sl_rand"][2] > 1.0 + 1e-9 or max(d["sl_broad"]) > 1.0 + 1e-6)

print("\n--- (d): infinitesimal identifiability: smallest / largest singular value of the column-normalised map (a, tau) -> dM")
for d in R:
    print(f"    n = {d['n']}: matrix {d['sv'][2][0]} x {d['sv'][2][1]}, singular values {d['sv'][0]:.3e} ... {d['sv'][1]:.3f}  (injective iff the smallest is > 0)")
    viol += int(d["sv"][0] < 1e-9)

print("\n--- (e): broadening X_1 -> X(theta +- eps v) with weights w_1/2 (v a random unit direction in torsion space); control: one-sided shift")
print("| n | eps | ||dM||_F two-sided | W_2^2 two-sided | W_2^2/||dM|| | ||dM||_F one-sided | W_2^2 one-sided | W_2^2/||dM|| |")
print("|---|---|---|---|---|---|---|---|")
d = R[3]
rng = np.random.default_rng(99)
v = rng.normal(size=d["n"] - 3)
v /= np.linalg.norm(v)
e_two, e_one = [], []
for eps in (1e-1, 3e-2, 1e-2, 3e-3, 1e-3):
    Yp, Ym = L.chain(d["tt"][0] + eps * v, COS), L.chain(d["tt"][0] - eps * v, COS)
    dM2 = np.linalg.norm(W[0] * 0.5 * (L.sqdist(Yp) + L.sqdist(Ym)) - W[0] * d["D"][0])
    w2 = W[0] * 0.5 * (L.procrustes2(Yp, d["X"][0]) + L.procrustes2(Ym, d["X"][0]))
    dM1 = np.linalg.norm(W[0] * (L.sqdist(Yp) - d["D"][0]))
    w1 = W[0] * L.procrustes2(Yp, d["X"][0])
    e_two.append((eps, dM2, w2))
    e_one.append((eps, dM1, w1))
    print(f"| {d['n']} | {eps:.0e} | {dM2:.3e} | {w2:.3e} | {w2 / dM2:.4f} | {dM1:.3e} | {w1:.3e} | {w1 / dM1:.2e} |")
p2 = np.polyfit(np.log([e[0] for e in e_two]), np.log([e[1] for e in e_two]), 1)[0]
pw = np.polyfit(np.log([e[0] for e in e_two]), np.log([e[2] for e in e_two]), 1)[0]
p1 = np.polyfit(np.log([e[0] for e in e_one]), np.log([e[1] for e in e_one]), 1)[0]
print(f"    fitted exponents in eps: ||dM|| two-sided {p2:.3f} (2 expected), W_2^2 {pw:.3f} (2), ||dM|| one-sided {p1:.3f} (1): "
      f"W_2^2/||dM|| tends to a positive constant for the symmetric broadening and to 0 for the shift")
viol += int(abs(p2 - 2) > 0.05 or abs(pw - 2) > 0.05 or abs(p1 - 1) > 0.05)

print("\n--- (w): pairs on which (CC) FAILS -- two and three differing torsions (long segments)")
print("| pair | n | dim N(z) | local value at X_1 (softest) | local value at X_2 | smallest ratio among 10000 random chains | smallest ratio after minimisation (d_P^2 to nearer state) |")
print("|---|---|---|---|---|---|---|")
for (n, seed, hinges, lab) in ((20, 2291, [5, 12], "two torsions [5, 12]"), (26, 2292, [5, 12, 19], "three torsions [5, 12, 19]"), (26, 2293, [6, 12, 18], "three torsions [6, 12, 18]")):
    d = analyse(n, seed, 10000, 32, hinges=hinges, label=lab)
    l1, l2 = d["loc"]
    print(f"| {lab} | {n} | {d['dimN']} | {l1[0]:.3e} | {l2[0]:.3e} | {d['best_sample']:.3e} | {d['best']:.3e} ({d['best_d']:.2e}) |", flush=True)
print("    (two torsions: phi vanishes on the six mirrored linear images found in t3c_linear_images.py, so the infimum is 0 although the mixture is identifiable;")
print("     three torsions: only the two states are linear images, and the local values are positive: Theorem G(a)-(c) would hold there without (CC).)")

print(f"\ncontrol/consistency violations: {viol}")
print(f"ALL DONE {time.time() - t0:.1f} s")
