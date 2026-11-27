"""
check_tail_lemmas.py -- workstream R6: brute-force checks of the two inputs that the whole chain rests on.
(1) Harper in the form used: for every nonempty S in Q_m, |S| >= |B(m,k)|  =>  |N(S)| >= |B(m,k+1)|   (all subsets, m <= 4; random, m = 5..7)
(2) Lemma K.1(a),(b) on random u-Lipschitz W (McShane-type constructions) on Q_m, m <= 10, every threshold.
(3) Lemma K.4 (a),(b),(d) and inequality (3.0) on exact tables.
"""
import itertools, math, sys
import numpy as np
import mpmath as mp
from fractions import Fraction
import r6lib as R

def balls(m):
    b = [sum(math.comb(m, j) for j in range(r + 1)) for r in range(m + 1)]
    return b

def nbr_masks(m):
    N = 1 << m
    return [[x ^ (1 << i) for i in range(m)] for x in range(N)]

def harper_exhaustive(m):
    N = 1 << m
    nb = nbr_masks(m)
    b = balls(m)
    # closed neighbourhood as bitmask of bitmask-sets
    nmask = [(1 << x) | sum(1 << y for y in nb[x]) for x in range(N)]
    viol = 0; cnt = 0
    for S in range(1, 1 << N):
        size = bin(S).count("1")
        NS = 0
        T = S
        while T:
            x = (T & -T).bit_length() - 1
            NS |= nmask[x]
            T &= T - 1
        ns = bin(NS).count("1")
        k = max(r for r in range(m + 1) if b[r] <= size)
        need = b[min(k + 1, m)]
        cnt += 1
        if ns < need:
            viol += 1
    return cnt, viol

def harper_random(m, trials, rng):
    N = 1 << m
    b = balls(m)
    idx = np.arange(N)
    viol = 0
    for _ in range(trials):
        kind = rng.integers(0, 3)
        if kind == 0:
            S = rng.random(N) < rng.random()
        elif kind == 1:      # union of a few balls
            S = np.zeros(N, bool)
            for _ in range(rng.integers(1, 4)):
                c = rng.integers(0, N); r = rng.integers(0, m)
                S |= np.array([bin(x ^ c).count("1") <= r for x in range(N)])
        else:                # initial segment of the simplicial order with a random centre, plus noise
            c = rng.integers(0, N)
            w = np.array([bin(x ^ c).count("1") for x in range(N)]) + 0.5 * rng.random(N)
            S = w <= np.sort(w)[rng.integers(0, N)]
        if not S.any():
            continue
        NS = S.copy()
        for i in range(m):
            NS |= S[idx ^ (1 << i)]
        size = int(S.sum()); ns = int(NS.sum())
        k = max(r for r in range(m + 1) if b[r] <= size)
        if ns < b[min(k + 1, m)]:
            viol += 1
    return viol

def random_lipschitz(m, u, rng):
    """psi on Q_m that is u-Lipschitz for the Hamming distance: random combination of McShane extensions, cones, additive parts."""
    N = 1 << m
    xs = np.arange(N)
    pop = np.array([[bin(x ^ c).count("1") for x in range(N)] for c in rng.integers(0, N, size=4)])
    kind = rng.integers(0, 5)
    if kind == 0:   # lower McShane envelope of random anchors: max_c (v_c - u d(x,c))
        v = rng.normal(0, u * m / 3, size=4)
        psi = np.max(v[:, None] - u * pop, axis=0)
    elif kind == 1: # upper envelope
        v = rng.normal(0, u * m / 3, size=4)
        psi = np.min(v[:, None] + u * pop, axis=0)
    elif kind == 2: # additive with slopes in [-u,u]
        th = rng.uniform(-u, u, size=m)
        psi = np.array([sum(th[i] for i in range(m) if (x >> i) & 1) for x in range(N)])
    elif kind == 3: # radial random walk
        steps = rng.uniform(-u, u, size=m)
        f = np.concatenate([[0], np.cumsum(steps)])
        psi = f[pop[0]]
    else:           # noise smoothed by inf-convolution with u*d (largest u-Lipschitz minorant)
        z = rng.normal(0, u * m / 2, size=N)
        psi = z.copy()
        for _ in range(m):
            for i in range(m):
                psi = np.minimum(psi, psi[xs ^ (1 << i)] + u)
    # verify Lipschitz
    for i in range(m):
        assert np.all(np.abs(psi - psi[xs ^ (1 << i)]) <= u + 1e-9)
    return psi

def tail_lemmas(m, u, trials, rng):
    N = 1 << m
    tab = R.Tables(m, u)
    xs = np.arange(N)
    viol_a = viol_b = n_a = n_b = 0
    max_a = max_b = 0.0
    for _ in range(trials):
        W = np.exp(-random_lipschitz(m, u, rng))
        vals = np.unique(W)
        for t in vals:
            # (a): D = {W > t}, |D| <= |B(m,r)|, r <= m-1  =>  sum (W - t)_+ <= t E_r(m)
            D = W > t
            if D.any() and not D.all():
                r = tab.least_ball_ge(int(D.sum()))
                if r <= m - 1:
                    lhs = float(np.sum(W[D] - t)); rhs = float(t * tab.E[r])
                    n_a += 1; max_a = max(max_a, lhs / rhs)
                    if lhs > rhs * (1 + 1e-9): viol_a += 1
            # (b): S = {W >= t}, |S| >= |B(m,k)|  =>  sum min(W,t) >= t T_m(k)
            S = W >= t
            k = tab.largest_ball_le(int(S.sum()))
            lhs = float(np.sum(np.minimum(W, t))); rhs = float(t * tab.T[k])
            n_b += 1; max_b = max(max_b, rhs / lhs)
            if lhs < rhs * (1 - 1e-9): viol_b += 1
    return n_a, viol_a, max_a, n_b, viol_b, max_b

def lemma_K4(us=(0.5, 1.0, 2.0), ms=(8, 20, 50, 120, 300, 800, 2000), etas=(Fraction(1, 2), Fraction(1, 4), Fraction(1, 12), Fraction(1, 20))):
    worst = dict(a=0.0, b=0.0, eq30=0.0)
    cases = 0
    viol = 0
    for u in us:
        pu = 1 / (1 + math.exp(u))
        for m in ms:
            tab = R.Tables(m, u)
            # (a): Gamma~(r) <= 2 e^u m for 0 <= r <= p_u (m+1)
            for r in range(0, int(math.floor(pu * (m + 1))) + 1):
                if r > m - 0: break
                g = tab.gamma_tilde(r) / (2 * mp.e ** u * m)
                worst["a"] = max(worst["a"], float(g)); cases += 1
                if g > 1: viol += 1
            # (3.0): Gamma~(r) <= (m+1) e^{2u} exp(m KL((r-1)/m || p_u)) for r >= 1
            for r in range(1, m + 1):
                rho = mp.mpf(r - 1) / m
                kl = (rho * mp.log(rho / pu) if rho > 0 else 0) + ((1 - rho) * mp.log((1 - rho) / (1 - pu)) if rho < 1 else 0)
                g = tab.gamma_tilde(r) / ((m + 1) * mp.e ** (2 * u) * mp.e ** (m * kl))
                worst["eq30"] = max(worst["eq30"], float(g)); cases += 1
                if g > 1 + mp.mpf(10) ** (-20): viol += 1
            for eta in etas:
                ef = float(eta)
                c_eta = (1 - ef) / (1 + ef)
                m0 = math.ceil(math.log(1 / c_eta) / u)
                # (b): kappa(r) >= r-1-m0 for 1 <= r <= p_u(m+1)+1 ; Gamma''(r) <= 2 e^{u(m0+2)} P(Bin(m,p_u) <= r) for 0 <= r <= p_u m
                cdf = mp.mpf(0)
                pmf = [mp.mpf(math.comb(m, j)) * mp.mpf(pu) ** j * mp.mpf(1 - pu) ** (m - j) for j in range(0, int(pu * m) + 2)]
                for r in range(0, int(math.floor(pu * m)) + 1):
                    cdf += pmf[r]
                    if r >= 1 and tab.kappa(r, eta) < max(0, r - 1 - m0): viol += 1
                    g = tab.gamma_pp(r, eta) / (2 * mp.e ** (u * (m0 + 2)) * cdf)
                    worst["b"] = max(worst["b"], float(g)); cases += 1
                    if g > 1: viol += 1
    return cases, viol, worst

if __name__ == "__main__":
    rng = np.random.default_rng(2026)
    for m in (1, 2, 3, 4):
        c, v = harper_exhaustive(m)
        print("Harper (form used), all nonempty subsets of Q_%d: %d sets, %d violations" % (m, c, v))
    for m in (5, 6, 7):
        print("Harper, random/structured subsets of Q_%d: 20000 sets, %d violations" % (m, harper_random(m, 20000, rng)))
    for (m, u, tr) in [(4, 0.7, 300), (6, 1.0, 300), (8, 0.5, 150), (8, 2.0, 150), (10, 1.3, 60)]:
        na, va, ma, nb, vb, mb = tail_lemmas(m, u, tr, rng)
        print("Lemma K.1 on Q_%d, u=%.1f: (a) %d thresholds, %d violations, max lhs/rhs %.6f; (b) %d thresholds, %d violations, max rhs/lhs %.6f" % (m, u, na, va, ma, nb, vb, mb))
    c, v, w = lemma_K4()
    print("Lemma K.4(a),(b) and inequality (3.0): %d cases, %d violations; largest ratios lhs/rhs: (a) %.4f, (b) %.4f, (3.0) %.4f" % (c, v, w["a"], w["b"], w["eq30"]))
