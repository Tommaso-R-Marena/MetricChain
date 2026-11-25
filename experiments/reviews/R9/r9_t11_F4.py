# R9 test 11: Theorem F4.
#  (a) brute force (n <= 9): for random psi in L_u and random q: quantiles t_{kappa+-1} <= e^u t_kappa, the truncated
#      function is u-Lipschitz, differs from psi only on D = {w > t_|x|}, maxdens(D) <= q, dens{w >= t_kappa} >= q.
#  (b)(ii) the stratified estimator, simulated on a cone (n = 10): frequency of the two tail events.
#  (c) the finite-n bound  ln[A(psi_s)/A(psi_s^tr,q)] >= n F_m(theta + 3 ln(n+1)/n) - 5 ln(n+2),  q = e^{-n theta},
#      F_m(th) = min{I^cone(z) : I(z) <= th}, with exact sums (n up to 2000) -- and how far the bound is from the truth.
import numpy as np, itertools, sys, time
from math import log, exp
from scipy.optimize import minimize
from r9lib import Par, h, kl
from r9prof import Grid, lse
rng = np.random.default_rng(23); t0 = time.time()
# ---------- (a)
viol = 0; ncase = 0
for trial in range(400):
    n = int(rng.integers(3, 10)); u = rng.uniform(0.2, 3.0); N = 1 << n
    X = np.array(list(itertools.product([0, 1], repeat=n))); tX = X.sum(axis=1)
    dist = (X[:, None, :] != X[None, :, :]).sum(axis=2)
    k = int(rng.integers(1, 7)); pts = rng.integers(0, N, k); vals = rng.uniform(-3 * u, 3 * u, k)
    psi = (vals[None, :] + u * dist[:, pts]).min(axis=1)             # a member of L_u
    if trial % 3 == 0: psi = np.maximum(psi, rng.uniform(-u, u) + u * rng.uniform(0, 1) * np.abs(tX - rng.integers(0, n + 1)))
    assert np.max(np.abs(psi[:, None] - psi[None, :]) - u * dist) < 1e-9
    w = np.exp(-psi); q = rng.uniform(0.01, 0.99)
    tq = np.zeros(n + 1)
    for t in range(n + 1):
        ww = np.sort(np.unique(w[tX == t]))
        # the smallest value tau of w on T_t with dens{w > tau} <= q
        for tau in ww:
            if np.mean(w[tX == t] > tau) <= q: tq[t] = tau; break
    ok = True
    for t in range(n):
        ok &= tq[t + 1] <= exp(u) * tq[t] * (1 + 1e-12) and tq[t] <= exp(u) * tq[t + 1] * (1 + 1e-12)
    psitr = np.maximum(psi, -np.log(tq[tX]))
    ok &= np.max(np.abs(psitr[:, None] - psitr[None, :]) - u * dist) < 1e-9
    D = w > tq[tX] * (1 + 1e-14)
    ok &= np.max(np.abs(psitr[~D] - psi[~D]), initial=0.0) < 1e-12     # (-ln e^{-psi} = psi up to rounding)
    ok &= max(np.mean(D[tX == t]) for t in range(n + 1)) <= q + 1e-12
    ok &= all(np.mean(w[tX == t] >= tq[t] * (1 - 1e-14)) >= q - 1e-12 for t in range(n + 1))
    ncase += 1; viol += (not ok)
    if not ok and viol <= 3: print('   violation at trial', trial, 'n', n, 'q', q)
print(f"(a) {ncase} random (psi, q), n in 3..9: violations of [quantiles e^u-Lipschitz, psi^tr in L_u, differs only on D, maxdens(D) <= q, dens(w >= t) >= q]: {viol}   [{time.time()-t0:.0f}s]")
# ---------- (b)(ii): simulation on a cone and on a random member, n = 10
n = 10; N = 1 << n; X = np.array(list(itertools.product([0, 1], repeat=n))); tX = X.sum(axis=1)
dist_to = lambda c: (X != X[c][None, :]).sum(axis=1)
for (p, u) in [(0.2, 1.5)]:
    piX = p ** tX * (1 - p) ** (n - tX); piT = np.array([piX[tX == t].sum() for t in range(n + 1)])
    for name in ('cone', 'random'):
        if name == 'cone': psi = u * dist_to(int(rng.integers(0, N)))
        else:
            pts = rng.integers(0, N, 4); vals = rng.uniform(-2 * u, 2 * u, 4)
            psi = (vals[None, :] + u * np.array([dist_to(int(c)) for c in pts]).T).min(axis=1)
        w = np.exp(-psi); A = (piX * w).sum()
        for q, M in ((0.2, 200), (0.05, 800)):
            K = M * q
            tq = np.zeros(n + 1)
            for t in range(n + 1):
                for tau in np.sort(np.unique(w[tX == t])):
                    if np.mean(w[tX == t] > tau) <= q: tq[t] = tau; break
            Atr = (piX * np.minimum(w, tq[tX])).sum(); epstr = log(A / Atr)
            idx_by_t = [np.where(tX == t)[0] for t in range(n + 1)]
            low = high = 0; R = 2000; d2 = 0.1
            for r in range(R):
                Ahat = sum(piT[t] * w[rng.choice(idx_by_t[t], M)].mean() for t in range(n + 1))
                low += log(Ahat) < log(A) - epstr - log(2); high += log(Ahat) > log(A) + log(1 / d2)
            print(f"(b)(ii) n={n} p={p} u={u} {name}, q={q}, M={M} (K={K:.0f}): eps^tr(psi)={epstr:.3f}; lower-tail failures {low}/{R} (bound (n+1)e^(-K/8) = {(n+1)*exp(-K/8):.2e}); upper-tail failures {high}/{R} (bound {d2})")
# ---------- (c)
def Fm(P, m, th):
    """min{ I^cone(z) : I(z) <= th } for centre type m (grid + SLSQP polish)"""
    al = np.linspace(1e-4, 1 - 1e-4, 501)[:, None]; be = np.linspace(1e-4, 1 - 1e-4, 501)[None, :]
    d = P.prof(m, al, be); val = np.where(d['I'] <= th, d['Icone'], np.inf)
    k = int(np.argmin(val)); i, j = divmod(k, 501); best = float(val[i, j]); z0 = (float(al[i, 0]), float(be[0, j]))
    fI = lambda z: float(P.prof(m, z[0], z[1])['Icone']); fc = lambda z: th - float(P.prof(m, z[0], z[1])['I'])
    r = minimize(fI, z0, method='SLSQP', bounds=[(1e-9, 1 - 1e-9)] * 2, constraints=[{'type': 'ineq', 'fun': fc}], options={'ftol': 1e-14, 'maxiter': 300})
    if r.success and fc(r.x) >= -1e-10: best = min(best, float(r.fun))
    return best
print("(c) exact ln[A(cone)/A(truncated cone)] against the bound n F_m(theta + 3 ln(n+1)/n) - 5 ln(n+2) and against n F_m(theta)")
nviol = 0; tot = 0
for (p, u) in [(0.1, 2.0), (0.3, 1.0), (0.2, 4.0)]:
    P = Par(p, u)
    for n in (200, 1000, 2000):
        for m in (0.3, 0.5, 0.7):
            k = int(round(m * n)); gr = Grid(P, (k, n - k)); lncum, d = gr.density_ball_order((1, 0))
            Ic = float(P.prof(k / n, P.eta1, P.eta0)['I'])
            logw = gr.logc + gr.logpi - u * d; lnA = lse(logw)
            for f in (0.15, 0.4, 0.7, 0.9):
                th = f * Ic
                if exp(-n * th) >= 1 / (n + 1): continue
                D = lncum <= -n * th
                rho = np.full(n + 1, 10 ** 9, dtype=np.int64); np.minimum.at(rho, gr.ti[~D], d[~D])
                lw = np.where(D, gr.logc + gr.logpi - u * rho[gr.ti], logw)
                exact = lnA - lse(lw)
                bound = n * Fm(P, k / n, th + 3 * log(n + 1) / n) - 5 * log(n + 2)
                lim = n * Fm(P, k / n, th)
                tot += 1; nviol += exact < bound - 1e-9
                if f in (0.4,) and m == 0.5:
                    print(f"    p={p} u={u} n={n} m={k/n:.3f} theta={th:.4f}: exact {exact:.3f}; bound {bound:.3f}; n F_m(theta) {lim:.3f}; (exact - n F_m)/ln n = {(exact-lim)/log(n):+.2f}")
print(f"    {tot} cases (3 parameter pairs, n = 200, 1000, 2000, 3 centre types, up to 4 values of theta): violations of the bound: {nviol}   [{time.time()-t0:.0f}s]")
