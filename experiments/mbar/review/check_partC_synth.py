"""Referee A -- independent checks of Part C (C1, C2), SYNTHESIS (S1, S1', S1'', S2, S3), the stored
A11 counterexample, and the sqrt(R_c/V_c) numbers of B4.  No import of d9mbar.
"""
import json
import numpy as np
import cvxpy as cp

rng = np.random.default_rng(31415)
E_ = np.e


def rand_model(K, J, zero_prob=0.0, alpha=1.0):
    while True:
        P = rng.dirichlet(np.ones(J) * alpha, size=K)
        P = np.where(rng.random((K, J)) < zero_prob, 0.0, P)
        if np.all(P.sum(axis=1) > 0):
            return P / P.sum(axis=1, keepdims=True)


def V_direct(P, s, nu):
    """sup_h 2 nu.h - sum_k s_k Var_k(h), computed in L2(m) coordinates (I - T has spectrum in [0,1])."""
    m = s @ P
    supp = m > 0
    if np.any(np.abs(nu[~supp]) > 1e-12 * max(np.abs(nu).max(), 1e-300)):
        return np.inf, None
    d = np.sqrt(m[supp])
    Pa = P[:, supp]
    Mt = ((Pa / d).T * s) @ (Pa / d)
    Qt = np.eye(supp.sum()) - (Mt + Mt.T) / 2
    w, E = np.linalg.eigh(Qt)
    pos = w > 1e-9
    coef = E.T @ (nu[supp] / d)
    if np.any(np.abs(coef[~pos]) > 1e-7 * max(np.abs(coef).max(), 1e-300)):
        return np.inf, None
    h = np.zeros(P.shape[1])
    h[supp] = (E[:, pos] @ (coef[pos] / w[pos])) / d
    return float(np.sum(coef[pos] ** 2 / w[pos])), h


def lap(P, s):
    m = s @ P
    pi = s[:, None] * P / np.where(m > 0, m, 1.0)
    return np.diag(s) - (pi * m) @ pi.T, pi


def kl(p, q):
    msk = p > 0
    return float(np.sum(p[msk] * np.log(p[msk] / q[msk])))


# ------------------------------------------------------------------ C1
print("== C1: constants at N = N0 (the smallest admitted N), tau in {1, 1/2, 0.1}")
worst_dens, worst_sep, worst_kl, worst_D, worst_sep_ratio = 0.0, np.inf, 0.0, -np.inf, np.inf
cnt = 0
for trial in range(3000):
    K, J = int(rng.integers(2, 6)), int(rng.integers(2, 9))
    P = rand_model(K, J, zero_prob=rng.choice([0.0, 0.3]), alpha=rng.choice([0.2, 1.0, 5.0]))
    s = rng.dirichlet(np.ones(K) * rng.choice([0.3, 1, 5]))
    pair = rng.random() < 0.5
    if pair:
        i, j = rng.choice(K, 2, replace=False)
        c = np.zeros(K); c[i], c[j] = 1.0, -1.0
    else:
        c = rng.normal(size=K); c -= c.mean()
    L, pi = lap(P, s)
    w = np.linalg.eigvalsh(L)
    if w[1] < 1e-9 * w[-1]:
        continue                                   # disconnected: outside the hypotheses
    v = np.linalg.pinv(L, rcond=1e-10, hermitian=True) @ c
    Rc = c @ v
    V, h = V_direct(P, s, c @ P)                   # stable route; h = dual maximiser (unique up to a constant)
    if not np.isfinite(V) or V < 1e-6 * Rc:
        continue
    supp = (s @ P) > 0
    h = np.where(supp, h, 0.0)
    zz = v @ pi
    if w[1] < 1e-6 * w[-1] or np.abs((h - zz)[supp] - (h - zz)[supp].mean()).max() > 1e-5 * max(1.0, np.abs(zz).max()):
        continue                                   # numerically unresolved (near-disconnected) instance: skipped
    D = h[supp].max() - h[supp].min()
    if pair:
        worst_D = max(worst_D, D / Rc)             # claim: D <= R_c
    # sanity: l_c(h) = V = Q(s,h)
    Eh = P @ h
    if abs(c @ Eh - V) > 1e-6 * V:
        continue
    Q = s @ (P @ h ** 2 - Eh ** 2)
    if abs(Q - V) > 1e-6 * V:
        continue
    for tau in (1.0, 0.5, 0.1):
        N0 = max(4 * tau ** 2 * D ** 2 / V, tau ** 2 * np.abs(c).sum() ** 2 * D ** 4 / V ** 3)
        N = N0
        t = tau / np.sqrt(N * V)
        hbar = 0.5 * (h[supp].max() + h[supp].min())
        dens = 1 + t * (h - hbar)
        worst_dens = max(worst_dens, np.abs(dens[supp] - 1).max())
        u = t * (Eh - hbar)
        sep = abs(-np.sum(c * np.log(1 + u)))
        worst_sep = min(worst_sep, sep / ((tau / 2) * np.sqrt(V / N)))
        worst_sep_ratio = min(worst_sep_ratio, sep / (t * V))
        KL = 0.0
        for k in range(K):
            dl = (t * (h - hbar) - u[k]) / (1 + u[k])          # p_{k,t}/p_k - 1, computed without cancellation
            KL += N * s[k] * float(np.sum(P[k] * ((1 + dl) * np.log1p(dl) - dl)))   # KL(p_{k,t} || p_k), stable
        if KL / ((16 / 9) * tau ** 2) > worst_kl:
            worst_kl = KL / ((16 / 9) * tau ** 2)
            worst_info = dict(K=K, J=J, V=V, Rc=Rc, D=D, N0=N0, tau=tau, t=t, Q=Q, umax=float(np.abs(u).max()))
        cnt += 1
print(f"  {cnt} cases: max |dG_t/dG - 1| = {worst_dens:.4f} (claim <= 1/4); "
      f"min separation/((tau/2)sqrt(V/N)) = {worst_sep:.4f} (claim >= 1); "
      f"max KL/((16/9)tau^2) = {worst_kl:.4f} (claim <= 1); max D/R_c for pair contrasts = {worst_D:.6f} (claim <= 1)")
print("  worst KL case:", worst_info)
for tau in (1.0, 0.5):
    print(f"  Le Cam/Pinsker arithmetic tau={tau}: 0.5*(1 - sqrt((16/9)tau^2/2)) = {0.5 * (1 - np.sqrt(16 / 9 * tau ** 2 / 2)):.4f}"
          f"   vs 0.5*(1-(2 sqrt2/3) tau) = {0.5 * (1 - 2 * np.sqrt(2) / 3 * tau):.4f}")

# ------------------------------------------------------------------ C2
print("== C2: least-favourable direction of the design problem; per-state divergence and separation")
worst_c2_kl, worst_c2_sep, worst_eta = 0.0, np.inf, 0.0
cnt = 0
for trial in range(40):
    K, J = int(rng.integers(2, 6)), int(rng.integers(3, 8))
    P = rand_model(K, J, zero_prob=rng.choice([0.0, 0.2]))
    if np.linalg.eigvalsh(lap(P, np.ones(K) / K)[0])[1] < 1e-9:
        continue
    c = rng.normal(size=K); c -= c.mean()
    a = rng.uniform(0.3, 4, K)
    hv = cp.Variable(J)
    sq = np.sqrt(P)
    cons = [cp.norm(cp.multiply(sq[k], hv - P[k] @ hv), 2) <= np.sqrt(a[k]) for k in range(K)]
    pr = cp.Problem(cp.Maximize((c @ P) @ hv), cons)
    pr.solve(solver=cp.CLARABEL)
    h = hv.value
    Eh = P @ h
    var = P @ h ** 2 - Eh ** 2
    M = np.max(var / a)
    ell = c @ Eh
    D = h.max() - h.min()
    for tau in (1.0, 0.5):
        # smallest budget admitted by the two side conditions
        t = min(0.5 / D, abs(ell) / (np.abs(c).sum() * D ** 2))
        B = tau ** 2 / (t ** 2 * M)
        Vstar = ell ** 2 / (B * M)                 # = V*(B) when h is the exact maximiser (eta = 0)
        hbar = 0.5 * (h.max() + h.min())
        u = t * (Eh - hbar)
        dens = 1 + t * (h - hbar)
        for k in range(K):
            dl = (t * (h - hbar) - u[k]) / (1 + u[k])
            klk = float(np.sum(P[k] * (dl - np.log1p(dl))))      # KL(p_k || p_{k,t}), stable
            worst_c2_kl = max(worst_c2_kl, klk / ((16 / 9) * t ** 2 * max(var[k], 1e-300)))
        sep = abs(np.sum(c * np.log(1 + u)))
        worst_c2_sep = min(worst_c2_sep, sep / ((tau / 2) * np.sqrt(Vstar)))
        # information of ANY allocation of cost B: sum_k n_k Var_k <= B M
        for rep in range(20):
            nvec = rng.dirichlet(np.ones(K) * 0.3); nvec *= B / (a @ nvec)
            worst_eta = max(worst_eta, (nvec @ var) / (B * M))
        cnt += 1
print(f"  {cnt} cases: max KL(p_k||p_k,t)/((16/9)t^2 Var_k) = {worst_c2_kl:.4f} (claim <= 1); "
      f"min separation/((tau/2)sqrt(V*)) = {worst_c2_sep:.4f} (claim >= 1); max information ratio = {worst_eta:.6f}")

# ------------------------------------------------------------------ S1 path bound
print("== S1: path bound (random models with common support, random paths incl. repeated states)")
worst_path, worst_len = 0.0, 0.0
cnt = 0
for trial in range(3000):
    K, J = int(rng.integers(2, 7)), int(rng.integers(2, 8))
    P = 0.97 * rand_model(K, J, alpha=rng.choice([0.3, 1.0, 4.0])) + 0.03 / J
    Lp = int(rng.integers(1, K + 2))
    path = [int(rng.integers(K))]
    for _ in range(Lp):
        path.append(int(rng.integers(K)))
    if not rng.random() < 0.3:
        path = list(dict.fromkeys(path))            # distinct states
    if len(path) < 2 or path[0] == path[-1]:
        continue
    c = np.zeros(K); c[path[0]] += 1; c[path[-1]] -= 1
    s = rng.dirichlet(np.ones(K))
    if rng.random() < 0.4:                           # only the sources of the steps are sampled
        s = np.where(np.isin(np.arange(K), path[:-1]), s, 0.0)
    chi = [np.sum(P[path[j + 1]] ** 2 / P[path[j]]) - 1 for j in range(len(path) - 1)]
    if any(s[path[j]] == 0 for j in range(len(path) - 1)):
        continue
    bound = sum(chi[j] / s[path[j]] for j in range(len(path) - 1))
    V = V_direct(P, s, c @ P)[0]
    worst_path = max(worst_path, V / bound)
    cnt += 1
print(f"  {cnt} cases: max V/bound = {worst_path:.6f} (claim <= 1)")

# ------------------------------------------------------------------ S1' Bhatia-Davis
a_grid = np.linspace(1 / E_, 1, 200001)
bd = (E_ * a_grid - 1) * (1 - a_grid)
print(f"== S1': sup of (ea-1)(1-a) over a in [1/e,1] = {bd.max():.6f};  (e-1)^2/(4e) = {(E_ - 1) ** 2 / (4 * E_):.6f}")
# brute force: chi2 between consecutive rungs of a random tempering ladder with oscillation Omega
worst_chi, worst_lad = 0.0, 0.0
for trial in range(300):
    J = int(rng.integers(2, 40))
    Om = rng.uniform(0.2, 12)
    psi = rng.random(J) ** rng.choice([0.2, 1, 5]); psi = (psi - psi.min()) / (psi.max() - psi.min()) * Om
    ref = rng.dirichlet(np.ones(J) * rng.choice([0.2, 1.0]))
    Kp = int(np.ceil(Om))
    Pl = np.array([ref * np.exp(-(j / Kp) * psi) for j in range(Kp + 1)])
    Pl /= Pl.sum(axis=1, keepdims=True)
    chis = [np.sum(Pl[j + 1] ** 2 / Pl[j]) - 1 for j in range(Kp)]
    worst_chi = max(worst_chi, max(chis))
    s = np.zeros(Kp + 1); s[:Kp] = 1.0 / Kp           # uniform on the K' sampled states, target unsampled
    c = np.zeros(Kp + 1); c[0], c[Kp] = 1.0, -1.0
    worst_lad = max(worst_lad, V_direct(Pl, s, c @ Pl)[0] / (0.272 * Kp ** 2))
print(f"  random ladders: max step chi2 = {worst_chi:.5f} (claim <= 0.27154); max V_uniform/(0.272 K'^2) = {worst_lad:.4f} (claim <= 1)")

# S1'' arithmetic
for Kp, eps, delta in ((5, 0.1, 0.05), (40, 0.5, 0.01), (1, 1.0, 0.3)):
    n1 = int(np.ceil(8 * (E_ - 1) ** 2 * Kp ** 2 * np.log(4 * Kp / delta) / eps ** 2))
    eta = eps / (4 * Kp)
    fail = Kp * 2 * np.exp(-2 * n1 * eta ** 2 / (E_ - 1) ** 2)
    print(f"== S1'': K'={Kp}, eps={eps}, delta={delta}: n1={n1}, union failure = {fail:.5f} (claim <= delta/2 = {delta / 2}); "
          f"log error <= K'*max|log(1+-eta)| = {Kp * max(np.log(1 + eta), -np.log(1 - eta)):.5f} (claim <= eps/2 = {eps / 2})")

# ------------------------------------------------------------------ S2 bridge instance, and K = 2
print("== S2: bridge instance (K >= 3) and the nested instance (K = 2)")
for K in (3, 4, 6):
    nb = 3
    P = np.zeros((K, 2 * nb))
    P[0, :nb] = 1 / nb                 # a
    P[1, nb:] = 1 / nb                 # b
    P[2, :] = 1 / (2 * nb)             # m (bridge)
    for k in range(3, K):
        P[k, :nb] = 1 / nb             # copies of a
    c = np.zeros(K); c[1], c[0] = 1.0, -1.0
    worst = 0.0
    for rep in range(200):
        s = rng.dirichlet(np.ones(K) * rng.choice([0.2, 1.0]))
        if rep % 3 == 0:
            s[rng.integers(K)] = 0.0
            if s[2] == 0:
                continue
            s /= s.sum()
        V = V_direct(P, s, c @ P)[0]
        worst = max(worst, abs(4 / V - s[2]))
    print(f"  K={K}: max |V*/V(s) - s_m| = {worst:.2e}  (V* = 4)")
# K = 2: P_1 uniform on A, P_2 uniform on A u B  (|A| = a, |B| = b)
for (na, nbb) in ((3, 3), (1, 5), (4, 1)):
    P = np.zeros((2, na + nbb)); P[0, :na] = 1 / na; P[1, :] = 1 / (na + nbb)
    c = np.array([-1.0, 1.0])
    worst = 0.0
    Vst = V_direct(P, np.array([0.0, 1.0]), c @ P)[0]
    for rep in range(100):
        s = rng.dirichlet(np.ones(2))
        worst = max(worst, abs(Vst / V_direct(P, s, c @ P)[0] - s[1]))
    print(f"  K=2 nested (|A|={na},|B|={nbb}): V(e_2) = {Vst:.4f}, max |eff(s) - s_2| = {worst:.2e}")
# the bridge instance needs three distinct states: what does the proof's instance give for K = 2? (not defined)

# ------------------------------------------------------------------ S3 two-point instance
print("== S3: two-point instance pi(1)=1/Gamma, weights (1, Gamma)")
for G in (4.0, 16.0, 64.0, 256.0, 1024.0):
    pi_ = np.array([1 - 1 / G, 1 / G]); wgt = np.array([1.0, G])
    p = pi_ * wgt; p /= p.sum()
    P = np.vstack([pi_, p])
    f = np.array([0.0, 1.0])
    nu = (f - p @ f) * p
    Vavg_ref = V_direct(P, np.array([1.0, 0.0]), nu)[0]
    Vavg_tgt = V_direct(P, np.array([0.0, 1.0]), nu)[0]
    Vfe_ref = V_direct(P, np.array([1.0, 0.0]), np.array([1.0, -1.0]) @ P)[0]
    print(f"  Gamma={G:6.0f}: V_avg(ref only)/Gamma = {Vavg_ref / G:.5f}; V_avg(target) = {Vavg_tgt:.5f}; "
          f"V_free-energy(ref only)/Gamma = {Vfe_ref / G:.5f}")

# ------------------------------------------------------------------ A11 stored counterexample
print("== A11: stored counterexample (results/lower_bounds_and_chains.json)")
ex = json.load(open("../results/lower_bounds_and_chains.json"))["correlated"]["example"]
P, T = np.array(ex["P"]), np.array(ex["T"])
s0, u0, lam = np.array(ex["s"]), np.array(ex["u"]), ex["lam"]
K, J = P.shape
c = None
print("  P shape", P.shape, "T shape", T.shape, "rows of T sum to 1:", np.allclose(T.sum(axis=2), 1),
      "stationary:", [bool(np.allclose(P[k] @ T[k], P[k], atol=1e-10)) for k in range(K)],
      "reversible:", [bool(np.allclose(P[k][:, None] * T[k], (P[k][:, None] * T[k]).T, atol=1e-10)) for k in range(K)])


def Vcorr(P, T, s, c):
    L, pi = lap(P, s)
    v = np.linalg.pinv(L, rcond=1e-10, hermitian=True) @ c
    z = v @ pi
    tot = 0.0
    for k in range(P.shape[0]):
        r = s[k] * (P[k] @ z - z)                      # r*_k, centred under P_k
        Zf = np.linalg.inv(np.eye(P.shape[1]) - T[k] + np.outer(np.ones(P.shape[1]), P[k]))
        gam = 2 * (P[k] * r) @ (Zf @ r) - (P[k] * r) @ r   # long-run variance
        tot += gam / s[k]
    return tot


found = False
for i in range(K):
    for j in range(K):
        if i == j:
            continue
        c = np.zeros(K); c[i], c[j] = 1.0, -1.0
        vals = [Vcorr(P, T, s0, c), Vcorr(P, T, u0, c)]
        for l in (lam, 1 - lam):
            mid = Vcorr(P, T, l * s0 + (1 - l) * u0, c)
            if np.allclose(sorted(vals + [mid]), sorted(ex["values"]), rtol=1e-6):
                chord = l * vals[0] + (1 - l) * vals[1]
                print(f"  contrast e{i}-e{j}, weight {l:.4f}: V(s)={vals[0]:.4f} V(u)={vals[1]:.4f} V(mix)={mid:.4f} "
                      f"chord={chord:.4f}; (mix-chord)/mix = {(mid - chord) / mid:.4f}, (mix-chord)/chord = {(mid - chord) / chord:.4f}")
                found = True
if not found:
    c = np.zeros(K); c[0], c[-1] = 1.0, -1.0
    print("  could not reproduce stored values with a pair contrast; e0-eK:", Vcorr(P, T, s0, c), Vcorr(P, T, u0, c),
          Vcorr(P, T, lam * s0 + (1 - lam) * u0, c), "stored", ex["values"])

# ------------------------------------------------------------------ B4: sqrt(R_c/V_c) in the benchmark models
print("== B4: sqrt(R_c/V_c), uniform allocation, end-to-end contrast and adjacent contrast")


def ratio(P, c):
    K = P.shape[0]
    s = np.ones(K) / K
    L, _ = lap(P, s)
    R = c @ np.linalg.pinv(L, rcond=1e-12, hermitian=True) @ c
    return np.sqrt(R / (R - np.sum(c ** 2 / s)))


for ov in (0.05, 0.35):
    K = 4
    P = np.full((K, K), ov / (K - 1)); np.fill_diagonal(P, 1 - ov)
    c = np.zeros(K); c[0], c[-1] = -1, 1
    print(f"  discrete overlap {ov}: {ratio(P, c):.3f}")
for K, spread in ((5, 0.5), (2, 1.0), (10, 0.25)):
    ks = 2.0 ** np.arange(K); x0 = spread * np.arange(K)
    x = np.linspace(-12, x0[-1] + 12, 400001)
    P = np.exp(-0.5 * ks[:, None] * (x[None, :] - x0[:, None]) ** 2)
    P /= P.sum(axis=1, keepdims=True)
    c = np.zeros(K); c[0], c[-1] = -1, 1
    c2 = np.zeros(K); c2[0], c2[1] = -1, 1
    print(f"  harmonic K={K} spread={spread}: end-to-end {ratio(P, c):.3f}; adjacent(0,1) {ratio(P, c2):.3f}")
