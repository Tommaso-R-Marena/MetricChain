"""Step 1 -- brute-force checks of the reductions (U), (L), (L') on inhomogeneous nearest-neighbour chains of 8-10 binary
sites (and 6 ternary sites), random fields, couplings, asymmetric site envelopes, random cuts/gaps, random admissible residuals.

(U)  pi = rho e^{-g} / E_rho e^{-g}, rho = product over blocks, g = sum of gauged cut couplings;
     A_pi(psi) = A_rho(psi+g)/A_rho(g);  psi in C_d  =>  psi+g in C_{d+},  d+ = d + delta^-_c at the left site of a cut, + delta^+_c at the right site,
     delta^-(a,a') = max_b [J0(a,b)-J0(a',b)],  delta^+(b,b') = max_a [J0(a,b)-J0(a,b')].
(L)  blocks with gaps: marginal of pi on the blocks = prod_j pi_{B_j} * prod_j rho_j(end_j, start_{j+1});
     sum_j min ln rho_j <= ln A_pi(psi' o proj) - ln A_prod(psi') <= sum_j max ln rho_j.
(L') psi' in C_{d-}  =>  psi = psi' + sum_j ln rho_j in C_d  and  A_pi(psi) = A_prod(psi') exactly.
"""
import sys, time, itertools, math
import numpy as np

rng = np.random.default_rng(20261125)
t0 = time.time()

def closure(d):
    d = d.copy(); q = len(d)
    for k in range(q):
        d = np.minimum(d, d[:, k:k + 1] + d[k:k + 1, :])
    return d

def random_envelope(q, lo=0.3, hi=1.5):
    d = rng.uniform(lo, hi, (q, q)); np.fill_diagonal(d, 0.0)
    return closure(d)                                   # zero diagonal, triangle inequality, asymmetric

def configs(qs):
    return np.array(list(itertools.product(*[range(q) for q in qs])), dtype=int)   # N x n

def pair_env(X, ds):
    """D[x,y] = sum_i d_i(x_i, y_i)"""
    N, n = X.shape; D = np.zeros((N, N))
    for i in range(n): D += ds[i][X[:, i][:, None], X[:, i][None, :]]
    return D

def chain_weights(X, fs, Js):
    N, n = X.shape; e = np.zeros(N)
    for i in range(n): e += fs[i][X[:, i]]
    for i in range(n - 1): e += Js[i][X[:, i], X[:, i + 1]]
    w = np.exp(-(e - e.min())); return w / w.sum()

def random_member(D):
    """random psi with psi(x) - psi(y) <= D[x,y]: inf-convolutions, their maxima, minima and convex combinations"""
    N = len(D)
    def infconv():
        c = rng.uniform(0, rng.choice([0.5, 2.0, 6.0]) * D.max(), N)
        if rng.random() < 0.5: c[rng.random(N) < 0.8] = np.inf; c[rng.integers(N)] = 0.0
        return (c[None, :] + D).min(axis=1)
    k = rng.integers(4)
    if k == 0: return infconv()
    if k == 1: return np.maximum(infconv(), infconv() + rng.normal())
    if k == 2: lam = rng.random(); return lam * infconv() + (1 - lam) * infconv()
    return np.minimum(infconv(), infconv() + rng.normal())

def violation(psi, D):
    return float((psi[:, None] - psi[None, :] - D).max())

def lnA(w, psi):
    return math.log(float((w * np.exp(-psi)).sum()))

stats = dict(U_id=0.0, U_adm=-1e9, U_noslack=0, U_cases=0, L_id=0.0, L_bound=-1e9, L_cases=0, Lp_adm=-1e9, Lp_id=0.0, Lp_cases=0,
             Lp_noslack=0, U_tight=1e9)
for case in range(36):
    if case % 4 == 3: qs = [3] * 6
    else: qs = [2] * [8, 9, 10][case % 3]
    n = len(qs); X = configs(qs); N = len(X)
    fs = [rng.normal(0, 0.7, q) for q in qs]
    Js = [rng.normal(0, rng.choice([0.3, 1.0, 2.5]), (qs[i], qs[i + 1])) for i in range(n - 1)]
    ds = [random_envelope(q) for q in qs]
    w = chain_weights(X, fs, Js); D = pair_env(X, ds)
    # ---------------------------------------------------------------- (U)
    cuts = sorted(rng.choice(n - 1, size=rng.integers(1, 4), replace=False))       # cut between sites c and c+1
    fs2 = [f.copy() for f in fs]; Js2 = [J.copy() for J in Js]; ds_plus = [d.copy() for d in ds]; g = np.zeros(N)
    for c in cuts:
        r = rng.normal(0, 0.5, qs[c]) * (rng.random() < 0.5); s = rng.normal(0, 0.5, qs[c + 1]) * (rng.random() < 0.5)   # a gauge
        J0 = Js[c] - r[:, None] - s[None, :]
        fs2[c] = fs2[c] + r; fs2[c + 1] = fs2[c + 1] + s; Js2[c] = np.zeros_like(J0)       # rho: product over blocks
        g += J0[X[:, c], X[:, c + 1]]
        dm = (J0[:, None, :] - J0[None, :, :]).max(axis=2)                                # delta^-(a,a') = max_b J0(a,b)-J0(a',b)
        dp = (J0[:, :, None] - J0[:, None, :]).max(axis=0)                                # delta^+(b,b') = max_a J0(a,b)-J0(a,b')
        ds_plus[c] = ds_plus[c] + dm; ds_plus[c + 1] = ds_plus[c + 1] + dp
    rho = chain_weights(X, fs2, Js2); Dp = pair_env(X, ds_plus)
    # rho is a product over blocks: check on the first cut
    c = cuts[0]; left = X[:, :c + 1]; right = X[:, c + 1:]
    kl, kr = {}, {}
    for idx in range(N):
        kl.setdefault(tuple(left[idx]), []).append(idx); kr.setdefault(tuple(right[idx]), []).append(idx)
    ml = {k: rho[v].sum() for k, v in kl.items()}; mr = {k: rho[v].sum() for k, v in kr.items()}
    prod_err = max(abs(rho[idx] - ml[tuple(left[idx])] * mr[tuple(right[idx])]) for idx in range(0, N, 7))
    assert prod_err < 1e-13
    for rep in range(12):
        psi = random_member(D); assert violation(psi, D) < 1e-9
        stats["U_id"] = max(stats["U_id"], abs(lnA(w, psi) - (lnA(rho, psi + g) - lnA(rho, g))))
        stats["U_adm"] = max(stats["U_adm"], violation(psi + g, Dp))
        stats["U_noslack"] += violation(psi + g, D) > 1e-9          # control: without the slack psi+g is NOT admissible in general
        stats["U_cases"] += 1
    # tightness of d+: the member psi = -g + (lower d-envelope of g) is not needed; record the smallest slack left by psi = D(., y0)
    psi = D[:, rng.integers(N)]; stats["U_tight"] = min(stats["U_tight"], -violation(psi + g, Dp))
    # ---------------------------------------------------------------- (L) and (L')
    L = rng.integers(1, 3); m = rng.integers(0, 3)
    blocks = []; i = rng.integers(0, 2)
    while i + L <= n:
        blocks.append(list(range(i, i + L))); i += L + m
    if len(blocks) < 2: blocks = [[0], [n - 1]]
    bs = [s for B in blocks for s in B]
    # marginal of pi on the block sites; block marginals; rho_j
    keyB = [tuple(x[bs]) for x in X]; uniq = sorted(set(keyB)); pos = {k: i for i, k in enumerate(uniq)}
    idxB = np.array([pos[k] for k in keyB]); piB = np.bincount(idxB, weights=w, minlength=len(uniq))
    XB = np.array(uniq)
    def marg(sites):
        key = [tuple(x[sites]) for x in X]; out = {}
        for k, wt in zip(key, w): out[k] = out.get(k, 0.0) + wt
        return out
    mb = [marg(B) for B in blocks]
    prodlaw = np.array([math.prod(mb[j][tuple(x[B])] for j, B in enumerate(blocks)) for x in X[[keyB.index(k) for k in uniq]]])
    rhos = []
    for j in range(len(blocks) - 1):
        e, s = blocks[j][-1], blocks[j + 1][0]
        pe, ps, pes = marg([e]), marg([s]), marg([e, s])
        rhos.append(np.array([[pes[(a, b)] / (pe[(a,)] * ps[(b,)]) for b in range(qs[s])] for a in range(qs[e])]))
    col = {s: k for k, s in enumerate(bs)}
    dens = np.ones(len(uniq))
    for j, R in enumerate(rhos):
        dens *= R[XB[:, col[blocks[j][-1]]], XB[:, col[blocks[j + 1][0]]]]
    stats["L_id"] = max(stats["L_id"], float(np.abs(piB - prodlaw * dens).max()))
    lo = sum(math.log(R.min()) for R in rhos); hi = sum(math.log(R.max()) for R in rhos)
    DB = pair_env(XB, [ds[s] for s in bs])
    # reduced envelope for (L')
    ds_minus = {s: ds[s].copy() for s in bs}
    for j, R in enumerate(rhos):
        lr = np.log(R); e, s = blocks[j][-1], blocks[j + 1][0]
        ds_minus[e] = ds_minus[e] - (lr[:, None, :] - lr[None, :, :]).max(axis=2)
        ds_minus[s] = ds_minus[s] - (lr[:, :, None] - lr[:, None, :]).max(axis=0)
    DBm = pair_env(XB, [ds_minus[s] for s in bs])
    lnrho = np.log(dens)
    for rep in range(12):
        psiB = random_member(DB); assert violation(psiB, DB) < 1e-9
        psi = psiB[idxB]                                           # psi' o proj: does not depend on the gap letters
        assert violation(psi, D) < 1e-9                            # it is in the chain's class
        diff = lnA(w, psi) - lnA(prodlaw, psiB)
        stats["L_bound"] = max(stats["L_bound"], lo - diff, diff - hi); stats["L_cases"] += 1
    if DBm.min() >= 0:                                             # (L') needs a nonnegative reduced envelope
        DBm_c = DBm.copy()
        for k in range(len(DBm_c)): DBm_c = np.minimum(DBm_c, DBm_c[:, k:k + 1] + DBm_c[k:k + 1, :])   # shortest-path closure (same class)
        for rep in range(12):
            psiB = random_member(DBm_c); assert violation(psiB, DBm) < 1e-9
            psi = (psiB + lnrho)[idxB]
            stats["Lp_adm"] = max(stats["Lp_adm"], violation(psi, D))
            stats["Lp_id"] = max(stats["Lp_id"], abs(lnA(w, psi) - lnA(prodlaw, psiB)))
            psi_bad = (random_member(DB) + lnrho)[idxB]            # control: without the reduction of the envelope
            stats["Lp_noslack"] += violation(psi_bad, D) > 1e-9
            stats["Lp_cases"] += 1

print("(U): %d residuals on 36 chains;  max |ln A_pi(psi) - ln A_rho(psi+g) + ln A_rho(g)| = %.2e;  max violation of d+ by psi+g = %.2e (<= 0 means admissible)"
      % (stats["U_cases"], stats["U_id"], stats["U_adm"]))
print("     control: psi+g violates the ORIGINAL envelope d in %d of %d cases;  smallest slack left in d+ by cones psi = d(., y0): %.2e (d+ is attained)"
      % (stats["U_noslack"], stats["U_cases"], stats["U_tight"]))
print("(L): max |marginal on blocks - prod of block marginals * prod rho_j| = %.2e;  %d residuals: max violation of the two-sided bound = %.2e"
      % (stats["L_id"], stats["L_cases"], stats["L_bound"]))
print("(L'): %d residuals (cases with nonnegative reduced envelope): max violation of d by psi'+sum ln rho = %.2e;  max |ln A_pi - ln A_prod| = %.2e"
      % (stats["Lp_cases"], stats["Lp_adm"], stats["Lp_id"]))
print("     control: with psi' in C_d instead of C_{d-}, psi'+sum ln rho violates d in %d of %d cases" % (stats["Lp_noslack"], stats["Lp_cases"]))

# ---------------------------------------------------------------- binary symmetric chain: the constants
print("\nbinary symmetric chain: constants of the reductions")
for p in (0.4, 0.3, 0.2, 0.1):
    K = math.log((1 - p) / p); lam = 1 - 2 * p; n = 10; qs = [2] * n; X = configs(qs)
    J = np.array([[-K, 0.0], [0.0, -K]])
    w = chain_weights(X, [np.zeros(2)] * n, [J] * (n - 1))
    # stationarity of free boundary conditions; rho_m(a,b) = 1 +- lam^(m+1)
    def marg(sites):
        key = [tuple(x[sites]) for x in X]; out = {}
        for k, wt in zip(key, w): out[k] = out.get(k, 0.0) + wt
        return out
    errs = []
    for m in range(0, 5):
        pes = marg([2, 3 + m]); R = np.array([[pes[(a, b)] / 0.25 for b in range(2)] for a in range(2)])
        errs.append(max(abs(R[0, 0] - (1 + lam ** (m + 1))), abs(R[0, 1] - (1 - lam ** (m + 1)))))
    kappa = [math.log((1 + lam ** (m + 1)) / (1 - lam ** (m + 1))) for m in range(6)]
    dm = (J[:, None, :] - J[None, :, :]).max(axis=2)
    print("p=%.1f: K=%.4f  delta^-(0,1)=delta^+(0,1)=%.4f (=K)  max|rho_m - (1 +- lam^(m+1))| = %.1e   kappa_m (m=0..5) = %s"
          % (p, K, dm[0, 1], max(errs), " ".join("%.4f" % k for k in kappa)))
print("%.1f s" % (time.time() - t0))
