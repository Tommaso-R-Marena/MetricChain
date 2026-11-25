# R9 test 15: the every-n lower bound of Theorem F1(a) (= Theorem 11.27(c) at the additive instance gamma|x| of THIS
# class), by brute force on the full cube, n = 8: for all centres b in {0,1}^n and the radius r,
#   Phi_b(x) = sum_i [u 1[x_i != b_i] - gamma x_i - Lam(b_i) - ln Z_gamma]   (so E_{pi_gamma} e^{-Phi_b + gamma|b| ...} normalised),
#   the generalised dip psi_gamma - (r - Phi_b)_+ is a member of L_u and raises ln A by at least r;
#   every point x lies in the supports {Phi_b < r} of centres of total M^n-weight <= e^{tr} val(K_t)^n.
import numpy as np, itertools, time
from math import log, exp
from scipy.optimize import linprog
from r9lib import Par
rng = np.random.default_rng(3); t0 = time.time()
n = 8; X = np.array(list(itertools.product([0, 1], repeat=n))); tX = X.sum(axis=1); N = 1 << n
dist = (X[:, None, :] != X[None, :, :]).sum(axis=2)
worst_sens = np.inf; worst_cov = -np.inf; worst_lip = -np.inf; cases = 0
for trial in range(12):
    p = rng.uniform(0.05, 0.95); u = rng.uniform(0.3, 3.0); P = Par(p, u); g = rng.uniform(-u, u); t = rng.uniform(0.05, 1.0)
    lz = float(P.lnZ(g)); Lam = np.array([P.Lam0, P.Lam1])
    psi = g * tX
    logw = tX * log(p) + (n - tX) * log(1 - p) - psi; lnA = np.log(np.exp(logw).sum())
    # Phi_b(x) for all b, x:  u d(x,b) - gamma|x| - sum_i Lam(b_i) - n ln Z_gamma
    LamB = Lam[X].sum(axis=1)                               # sum_i Lam(b_i) for centre b
    Phi = u * dist - g * tX[:, None] - LamB[None, :] - n * lz      # Phi[x, b]
    # optimal mixed strategy M of the centres' letters for the game K_t
    K = P.Kmat(g, t)
    res = linprog(c=[0, 0, 1], A_ub=np.hstack([K, -np.ones((2, 1))]), b_ub=[0, 0], A_eq=[[1, 1, 0]], b_eq=[1], bounds=[(0, None), (0, None), (None, None)], method='highs')
    M = res.x[:2]; val = res.x[2]
    wB = np.prod(np.where(X == 1, M[1], M[0]), axis=1)      # M^n(b)
    for r in (0.3, 1.0, 2.5):
        supp = Phi < r
        cov = (supp * wB[None, :]).sum(axis=1).max()
        worst_cov = max(worst_cov, cov / (exp(t * r) * val ** n))
        for b in rng.integers(0, N, 6):
            psid = psi - np.maximum(r - Phi[:, b], 0.0)
            worst_lip = max(worst_lip, float(np.max(np.abs(psid[:, None] - psid[None, :]) - u * dist)))
            gain = np.log(np.exp(tX * log(p) + (n - tX) * log(1 - p) - psid).sum()) - lnA
            worst_sens = min(worst_sens, gain - r); cases += 1
print(f"n={n}, 12 random (p, u, gamma, t), 3 radii: {cases} dips: min(ln A(dip) - ln A - r) = {worst_sens:+.2e} (>= 0: every radius r > eps is sensitive); max Lipschitz violation {worst_lip:.1e}; "
      f"max over points of [M^n-weight of the supports containing it]/(e^(tr) val^n) = {worst_cov:.4f} (<= 1)   [{time.time()-t0:.0f}s]")
