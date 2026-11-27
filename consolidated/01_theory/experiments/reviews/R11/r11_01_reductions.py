"""R11 / 01 -- brute-force test of Theorems Y1 (U), Y2 (L), Y3 (L') on random inhomogeneous
nearest-neighbour chains (binary n = 8, 9, 10; ternary n = 6), random fields, couplings,
asymmetric envelopes, cuts, gaps and gauges.  Own code, written from the statements.

Run:  python3 r11_01_reductions.py     (about 1 minute)
"""
import itertools, time
import numpy as np

rng = np.random.default_rng(20261126)
T0 = time.time()


def all_configs(qs):
    return np.array(list(itertools.product(*[range(q) for q in qs])), dtype=np.int64)


def closure(d):
    """shortest-path closure of a matrix with zero diagonal (Floyd-Warshall)."""
    d = d.copy()
    q = d.shape[0]
    for k in range(q):
        d = np.minimum(d, d[:, [k]] + d[[k], :])
    return d


def random_envelope(q):
    d = rng.uniform(0.2, 2.0, size=(q, q))
    np.fill_diagonal(d, 0.0)
    return closure(d)


def dist_matrix(X, ds, sites=None):
    """D[x, y] = sum_i d_i(x_i, y_i)."""
    N = X.shape[0]
    D = np.zeros((N, N))
    for i in (range(X.shape[1]) if sites is None else sites):
        D += ds[i][X[:, i][:, None], X[:, i][None, :]]
    return D


def chain_weights(X, f, J):
    n = X.shape[1]
    e = np.zeros(X.shape[0])
    for i in range(n):
        e += f[i][X[:, i]]
    for i in range(n - 1):
        e += J[i][X[:, i], X[:, i + 1]]
    w = np.exp(-e)
    return w / w.sum()


def random_member(D):
    """a random member of C_d: psi(x) - psi(y) <= D[x, y].
    Mixtures (max / min / convex combinations) of inf-convolutions min_y [g(y) + D[x, y]]."""
    N = D.shape[0]
    def infconv(scale):
        g = rng.normal(0, scale, size=N)
        return (g[None, :] + D).min(axis=1)
    kind = rng.integers(0, 5)
    a, b = infconv(rng.uniform(0.5, 4.0)), infconv(rng.uniform(0.5, 4.0))
    if kind == 0:
        return a
    if kind == 1:
        return np.maximum(a, b)
    if kind == 2:
        return np.minimum(a, b)
    if kind == 3:
        lam = rng.uniform()
        return lam * a + (1 - lam) * b
    y0 = rng.integers(0, N)
    return D[:, y0].copy()            # a cone d(., y0)


def viol(psi, D):
    """largest value of psi(x) - psi(y) - D[x, y]."""
    return float((psi[:, None] - psi[None, :] - D).max())


def lnA(pi, psi):
    return float(np.log((pi * np.exp(-psi)).sum()))


stats = dict(U_id=0.0, U_adm=-np.inf, U_ctrl=0, U_n=0, U_tight=np.inf, U_pi=0.0,
             L_marg=0.0, L_two=-np.inf, L_n=0, Lp_adm=-np.inf, Lp_id=0.0, Lp_n=0, Lp_ctrl=0, Lp_skipped=0,
             L_sub=-np.inf)

chains = [([2] * 8, 9), ([2] * 9, 9), ([2] * 10, 9), ([3] * 6, 9)]
nchains = 0
for qs, reps in chains:
    n = len(qs)
    X = all_configs(qs)
    N = X.shape[0]
    for rep in range(reps):
        nchains += 1
        sd = rng.choice([0.3, 1.0, 2.5])
        f = [rng.normal(0, 1.0, size=q) for q in qs]
        J = [rng.normal(0, sd, size=(qs[i], qs[i + 1])) for i in range(n - 1)]
        ds = [random_envelope(q) for q in qs]
        pi = chain_weights(X, f, J)
        D = dist_matrix(X, ds)

        # ------------------------------------------------------------------ (U)
        ncut = rng.integers(1, n - 1)
        cuts = sorted(rng.choice(np.arange(n - 1), size=ncut, replace=False))   # cut c between sites c and c+1 (0-based)
        r = {c: rng.normal(0, 0.7, size=qs[c]) if rng.uniform() < 0.5 else np.zeros(qs[c]) for c in cuts}
        s_ = {c: rng.normal(0, 0.7, size=qs[c + 1]) if rng.uniform() < 0.5 else np.zeros(qs[c + 1]) for c in cuts}
        Jo = {c: J[c] - r[c][:, None] - s_[c][None, :] for c in cuts}
        # product over blocks of free-boundary block laws with the gauge fields
        f2 = [fi.copy() for fi in f]
        for c in cuts:
            f2[c] = f2[c] + r[c]
            f2[c + 1] = f2[c + 1] + s_[c]
        J2 = [np.zeros_like(J[i]) if i in cuts else J[i] for i in range(n - 1)]
        rho = chain_weights(X, f2, J2)
        # check that rho is a product over the blocks
        bounds = [0] + [c + 1 for c in cuts] + [n]
        blocks = [list(range(bounds[j], bounds[j + 1])) for j in range(len(bounds) - 1)]
        prod = np.ones(N)
        for B in blocks:
            key = np.zeros(N, dtype=np.int64)
            for i in B:
                key = key * qs[i] + X[:, i]
            marg = np.bincount(key, weights=rho)
            prod *= marg[key]
        stats['U_pi'] = max(stats['U_pi'], float(np.abs(prod - rho).max()))
        g = np.zeros(N)
        for c in cuts:
            g += Jo[c][X[:, c], X[:, c + 1]]
        # pi = rho e^{-g} / E_rho e^{-g}
        w = rho * np.exp(-g)
        stats['U_pi'] = max(stats['U_pi'], float(np.abs(w / w.sum() - pi).max()))
        # d+ : delta^-_c(a,a') = max_b [Jo(a,b) - Jo(a',b)] at site c,  delta^+_c(b,b') = max_a [Jo(a,b) - Jo(a,b')] at site c+1
        dplus = [d.copy() for d in ds]
        for c in cuts:
            dm = (Jo[c][:, None, :] - Jo[c][None, :, :]).max(axis=2)
            dp = (Jo[c][:, :, None] - Jo[c][:, None, :]).max(axis=0)
            dplus[c] = dplus[c] + dm
            dplus[c + 1] = dplus[c + 1] + dp
        Dp = dist_matrix(X, dplus)
        for k in range(12):
            psi = random_member(D)
            assert viol(psi, D) < 1e-9
            lhs = lnA(pi, psi)
            rhs = lnA(rho, psi + g) - lnA(rho, g)
            stats['U_id'] = max(stats['U_id'], abs(lhs - rhs))
            stats['U_adm'] = max(stats['U_adm'], viol(psi + g, Dp))
            stats['U_ctrl'] += viol(psi + g, D) > 1e-9
            stats['U_n'] += 1
        # tightness: for a cone at y0 the slack min over single-site pairs of d+ - difference
        for k in range(3):
            y0 = rng.integers(0, N)
            psi = D[:, y0] + g
            stats['U_tight'] = min(stats['U_tight'], float((Dp - (psi[:, None] - psi[None, :])).min()))

        # ------------------------------------------------------------------ (L), (L')
        # random blocks with gaps
        while True:
            marks = rng.integers(0, 2, size=n)              # 1 = block site, 0 = gap site
            marks[rng.integers(0, n)] = 1
            # blocks = maximal runs of ones; need at least two blocks for a non-trivial test
            runs = []
            i = 0
            while i < n:
                if marks[i] == 1:
                    j = i
                    while j + 1 < n and marks[j + 1] == 1:
                        j += 1
                    runs.append(list(range(i, j + 1)))
                    i = j + 1
                else:
                    i += 1
            # split long runs at random positions (gap m = 0 between the pieces)
            blocks = []
            for run in runs:
                while len(run) > 1 and rng.uniform() < 0.5:
                    cpos = rng.integers(1, len(run))
                    blocks.append(run[:cpos])
                    run = run[cpos:]
                blocks.append(run)
            if len(blocks) >= 2:
                break
        bsites = [i for B in blocks for i in B]
        # marginal of pi on the block sites
        qB = [qs[i] for i in bsites]
        XB = all_configs(qB)
        NB = XB.shape[0]
        keyB = np.zeros(N, dtype=np.int64)
        for i in bsites:
            keyB = keyB * qs[i] + X[:, i]
        piB = np.bincount(keyB, weights=pi, minlength=NB)
        # block marginals and rho_j
        pos = {site: k for k, site in enumerate(bsites)}
        prodB = np.ones(NB)
        for B in blocks:
            key = np.zeros(NB, dtype=np.int64)
            for i in B:
                key = key * qs[i] + XB[:, pos[i]]
            marg = np.bincount(key, weights=piB)
            prodB *= marg[key]
        lnrho = []
        rho_prod = np.ones(NB)
        for j in range(len(blocks) - 1):
            e, st = blocks[j][-1], blocks[j + 1][0]
            pair = np.zeros((qs[e], qs[st]))
            np.add.at(pair, (X[:, e], X[:, st]), pi)
            rj = pair / (pair.sum(1)[:, None] * pair.sum(0)[None, :])
            lnrho.append((e, st, np.log(rj)))
            rho_prod *= rj[XB[:, pos[e]], XB[:, pos[st]]]
        stats['L_marg'] = max(stats['L_marg'], float(np.abs(piB - prodB * rho_prod).max()))
        dB = [ds[i] for i in bsites]
        DB = dist_matrix(XB, dB)
        lo = sum(l.min() for _, _, l in lnrho)
        hi = sum(l.max() for _, _, l in lnrho)
        for k in range(12):
            psiB = random_member(DB)
            psi = psiB[keyB]                              # psi' o proj on the full chain
            stats['L_sub'] = max(stats['L_sub'], viol(psi, D))
            diff = lnA(pi, psi) - lnA(prodB, psiB)
            stats['L_two'] = max(stats['L_two'], lo - diff, diff - hi)
            stats['L_n'] += 1
        # (L'): reduced envelope
        dminus = [d.copy() for d in dB]
        for e, st, l in lnrho:
            em = (l[:, None, :] - l[None, :, :]).max(axis=2)       # eps^-(a,a') = max_b [l(a,b) - l(a',b)]
            ep = (l[:, :, None] - l[:, None, :]).max(axis=0)       # eps^+(b,b') = max_a [l(a,b) - l(a,b')]
            dminus[pos[e]] = dminus[pos[e]] - em
            dminus[pos[st]] = dminus[pos[st]] - ep
        dminus_c = [closure(d) for d in dminus]
        if min(d.min() for d in dminus_c) < 0 or any(np.abs(np.diag(d)).max() > 1e-12 for d in dminus_c):
            stats['Lp_skipped'] += 1
        else:
            Dm = dist_matrix(XB, dminus_c)
            corr = np.zeros(NB)
            for e, st, l in lnrho:
                corr += l[XB[:, pos[e]], XB[:, pos[st]]]
            for k in range(12):
                psiB = random_member(Dm)
                psi = (psiB + corr)[keyB]
                stats['Lp_adm'] = max(stats['Lp_adm'], viol(psi, D))
                stats['Lp_id'] = max(stats['Lp_id'], abs(lnA(pi, psi) - lnA(prodB, psiB)))
                stats['Lp_n'] += 1
                # control: psi' in the plain class instead of the reduced one
                psiB2 = random_member(DB)
                stats['Lp_ctrl'] += viol((psiB2 + corr)[keyB], D) > 1e-9

print(f"{nchains} random chains (27 binary with 8, 9, 10 sites, 9 ternary with 6 sites)")
print(f"(U)  pi = rho e^-g / Z and rho = product over blocks:  max abs deviation {stats['U_pi']:.2e}")
print(f"(U)  identity ln A_pi(psi) = ln A_rho(psi+g) - ln A_rho(g):  {stats['U_n']} residuals, max deviation {stats['U_id']:.2e}")
print(f"(U)  psi + g in C_(d+):  largest violation {stats['U_adm']:.2e}  (<= 1e-12 means admissible)")
print(f"(U)  control: psi + g violates the original envelope d in {stats['U_ctrl']} of {stats['U_n']} cases")
print(f"(U)  tightness: smallest slack of d+ left by psi = d(., y0):  {stats['U_tight']:.2e}  (0 = attained)")
print(f"(L)  marginal on blocks = prod of block marginals * prod rho_j:  max deviation {stats['L_marg']:.2e}")
print(f"(L)  psi' o proj in C_d: largest violation {stats['L_sub']:.2e};  two-sided bound: {stats['L_n']} residuals, largest violation {stats['L_two']:.2e} (<= 0 means none)")
print(f"(L') {stats['Lp_n']} residuals on chains with a nonnegative reduced envelope ({stats['Lp_skipped']} chains skipped):")
print(f"     psi = psi' o proj + sum ln rho_j in C_d: largest violation {stats['Lp_adm']:.2e};  |ln A_pi(psi) - ln A_prod(psi')| <= {stats['Lp_id']:.2e}")
print(f"     control (psi' in C_d instead of C_(d-)): psi violates d in {stats['Lp_ctrl']} of {stats['Lp_n']} cases")

# ---------------------------------------------------------------------- constants of the binary symmetric chain
print("\nbinary symmetric chain: delta^+-, rho_m, kappa_m")
for p in (0.4, 0.3, 0.2, 0.1):
    K = np.log((1 - p) / p)
    lam = 1 - 2 * p
    Jm = -K * np.eye(2)
    dm = (Jm[:, None, :] - Jm[None, :, :]).max(axis=2)
    P = np.array([[1 - p, p], [p, 1 - p]])
    kap = []
    dev = 0.0
    for m in range(6):
        Pm = np.linalg.matrix_power(P, m + 1)
        rho_m = 0.5 * Pm / 0.25
        dev = max(dev, abs(rho_m[0, 0] - (1 + lam ** (m + 1))), abs(rho_m[0, 1] - (1 - lam ** (m + 1))))
        l = np.log(rho_m)
        kap.append((l[:, None, :] - l[None, :, :]).max(axis=2)[0, 1])
    print(f"p={p}: K={K:.4f}  delta(0,1)={dm[0,1]:.4f}  max|rho_m - (1 +- lam^(m+1))| = {dev:.1e}  kappa_m (m=0..5) = " + " ".join(f"{k:.4f}" for k in kap))
print(f"{time.time()-T0:.1f} s")
