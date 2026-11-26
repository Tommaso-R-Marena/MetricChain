#!/usr/bin/env python3
"""r26_band.py -- workstream R26 (internal review by an AI agent).

Band (transfer-matrix) models on a chain of n sites with q states per site and pair interactions up to sequence
separation r (the "bandwidth").  For a cut after site c (outer block = sites 0..c-1, inner block = sites c..n-1)
this library computes, with code written from the definitions of N_REPORT 2.7 (Theorem N4) and nothing else:

  * the conditional laws mu(b | a) of the inner block, by brute-force enumeration AND by transfer matrices
    (two independent paths; they are compared in the self-test);
  * the pointwise influence        iota_pt(a,a')  = max_b ln[ mu(b|a) / mu(b|a') ];
  * the box-class influence        iota_box(a,a') = sup{ ln[ <w>_a / <w>_a' ] : 1 <= w <= e^D }   (level-set formula
    and, as a check, a linear programme on the whole inner block);
  * the Lipschitz-class influence  iota_L(a,a')   = sup{ ln[ <w>_a / <w>_a' ] : w(x) <= e^u w(y) for Hamming
    neighbours x, y of the inner block }   (a linear programme on the whole inner block; exact);
  * a polynomial-time upper bound of iota_L for nearest-neighbour chains (pairwise recursion through the block).

Conventions: energies in kT; mu(x) proportional to exp(-E(x)); a "boundary state" alpha is the state of the last
min(r,c) outer sites; beta is the state of the first min(r, n-c) inner sites (the "inner boundary layer").
"""
import itertools
import resource
import sys
import time

import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from scipy.special import logsumexp


# ----------------------------------------------------------------------------------------------- models

def make_base(n, q, r, rng, clash_frac=0.0):
    """Random numbers of a band model, independent of the scales J and C (so that one seed can be re-scaled)."""
    G, mask = {}, {}
    for i in range(n):
        for j in range(i + 1, min(n, i + r + 1)):
            G[(i, j)] = rng.standard_normal((q, q))
            mask[(i, j)] = rng.random((q, q)) < clash_frac
    hG = rng.standard_normal((n, q))
    return dict(n=n, q=q, r=r, G=G, mask=mask, hG=hG)


def energies(base, J, C=None, field=0.0):
    """Pair energies J*G, with the masked entries replaced by the clash energy C (if C is not None)."""
    pair = {}
    for key, g in base["G"].items():
        e = J * g
        if C is not None:
            e = np.where(base["mask"][key], C, e)
        pair[key] = e
    h = field * base["hG"]
    return dict(n=base["n"], q=base["q"], r=base["r"], pair=pair, h=h)


def configs(q, k):
    """All q^k configurations of k sites, shape (q^k, k); the first site is the most significant digit."""
    if k == 0:
        return np.zeros((1, 0), dtype=np.int64)
    return np.array(list(itertools.product(range(q), repeat=k)), dtype=np.int64)


# ----------------------------------------------------------------------------- brute force across a cut

def brute_conditionals(model, c):
    """Enumerate the inner block.  Returns (alphas, bconf, logmu) with logmu[alpha_index, b_index] =
    ln mu(b | alpha), alphas = states of the last min(r,c) outer sites, bconf = all inner configurations."""
    n, q, r = model["n"], model["q"], model["r"]
    k = n - c
    rb = min(r, c)
    bconf = configs(q, k)
    Ei = np.zeros(len(bconf))
    for j in range(c, n):
        Ei += model["h"][j][bconf[:, j - c]]
    for (i, j), e in model["pair"].items():
        if i >= c:
            Ei += e[bconf[:, i - c], bconf[:, j - c]]
    alphas = configs(q, rb)
    Ex = np.zeros((len(alphas), len(bconf)))
    for (i, j), e in model["pair"].items():
        if i < c <= j:
            ia = i - (c - rb)
            assert 0 <= ia < rb
            Ex += e[alphas[:, ia][:, None], bconf[:, j - c][None, :]]
    logw = -Ex - Ei[None, :]
    logmu = logw - logsumexp(logw, axis=1, keepdims=True)
    return alphas, bconf, logmu


# ----------------------------------------------------------------------------- transfer matrices (super-sites)

def inner_groups(model, c):
    n, r = model["n"], model["r"]
    groups, lo = [], c
    while lo < n:
        groups.append(list(range(lo, min(lo + r, n))))
        lo += r
    return groups


def group_energy(model, sites, conf):
    e = np.zeros(len(conf))
    for t, j in enumerate(sites):
        e += model["h"][j][conf[:, t]]
    for t1, i in enumerate(sites):
        for t2, j in enumerate(sites):
            if i < j and (i, j) in model["pair"]:
                e += model["pair"][(i, j)][conf[:, t1], conf[:, t2]]
    return e


def cross_energy(model, sitesA, confA, sitesB, confB):
    e = np.zeros((len(confA), len(confB)))
    for t1, i in enumerate(sitesA):
        for t2, j in enumerate(sitesB):
            if (i, j) in model["pair"]:
                e += model["pair"][(i, j)][confA[:, t1][:, None], confB[:, t2][None, :]]
    return e


def boundary_layer(model, c):
    """Transfer-matrix path.  Returns (alphas, betas, Ex, logR, logpi):
    Ex[alpha, beta] = cross-cut energy (it involves the last r outer and the first r inner sites only),
    logR[beta] = ln of the partition sum of the inner block with its first group fixed to beta (backward message),
    logpi[alpha, beta] = ln mu(first inner group = beta | alpha)."""
    q, r = model["q"], model["r"]
    rb = min(r, c)
    groups = inner_groups(model, c)
    confs = [configs(q, len(g)) for g in groups]
    logR = -group_energy(model, groups[-1], confs[-1])
    for t in range(len(groups) - 2, -1, -1):
        X = cross_energy(model, groups[t], confs[t], groups[t + 1], confs[t + 1])
        logR = -group_energy(model, groups[t], confs[t]) + logsumexp(-X + logR[None, :], axis=1)
    outer_sites = list(range(c - rb, c))
    alphas = configs(q, rb)
    Ex = cross_energy(model, outer_sites, alphas, groups[0], confs[0])
    logw = -Ex + logR[None, :]
    logpi = logw - logsumexp(logw, axis=1, keepdims=True)
    return alphas, confs[0], Ex, logR, logpi


# ----------------------------------------------------------------------------- influences

def iota_pointwise_brute(logmu):
    """iota_pt[alpha, alpha'] = max_b ( ln mu(b|alpha) - ln mu(b|alpha') ), from the enumeration."""
    return (logmu[:, None, :] - logmu[None, :, :]).max(axis=2)


def iota_pointwise_formula(Ex, logpi):
    """The boundary formula: iota_pt(a,a') = max_beta Delta(beta) - ln sum_beta pi_{a'}(beta) e^{Delta(beta)},
    Delta(beta) = Ex(a',beta) - Ex(a,beta).  Also returns osc(Delta) = max - min (the bound that uses the cross-cut
    interaction only)."""
    Delta = Ex[None, :, :] - Ex[:, None, :]                 # [a, a', beta]
    mx = Delta.max(axis=2)
    lme = logsumexp(logpi[None, :, :] + Delta, axis=2)
    return mx - lme, mx - Delta.min(axis=2)


def iota_box_levelset(logpi, D):
    """sup over 1 <= w <= e^D of ln(<w>_a / <w>_a') = ln max_S (1 + (e^D-1) pi_a(S)) / (1 + (e^D-1) pi_a'(S)), S a
    super-level set of the likelihood ratio pi_a/pi_a' on the inner boundary layer."""
    nA = logpi.shape[0]
    out = np.zeros((nA, nA))
    g = np.expm1(D)
    for a in range(nA):
        for a2 in range(nA):
            if a == a2:
                continue
            order = np.argsort(-(logpi[a] - logpi[a2]), kind="stable")
            Pa = np.cumsum(np.exp(logpi[a][order]))
            Pb = np.cumsum(np.exp(logpi[a2][order]))
            ratio = (1.0 + g * Pa) / (1.0 + g * Pb)
            out[a, a2] = np.log(max(1.0, ratio.max()))
    return out


def lipschitz_constraints(q, k, u):
    """Rows w(x) - e^u w(y) <= 0 for all ordered pairs of inner configurations that differ in exactly one site."""
    N = q ** k
    conf = configs(q, k)
    idx = np.arange(N)
    rows, cols, vals = [], [], []
    nrow = 0
    eu = np.exp(u)
    for site in range(k):
        stride = q ** (k - 1 - site)
        for delta in range(1, q):
            y = idx + (((conf[:, site] + delta) % q) - conf[:, site]) * stride
            r_ = np.arange(nrow, nrow + N)
            rows += [r_, r_]
            cols += [idx, y]
            vals += [np.ones(N), -eu * np.ones(N)]
            nrow += N
    A = sparse.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(nrow, N))
    return A


LP_FALLBACKS = {"highs": 0, "highs-ds": 0, "highs-ipm": 0, "failed": 0}


def lp_ratio(mu_num, mu_den, A_ub, trunc=1e-15):
    """max <mu_num, w> subject to <mu_den, w> = 1, A_ub w <= 0, w >= 0.  Returns the optimal value.
    Coefficients below `trunc` times the largest one are set to zero before the solve: in clash models the
    probabilities span 60 decades and HiGHS then sometimes returns "Status 0: Not Set" (seen in
    out_infl_T4_1.txt).  Because every feasible w has max w <= e^{u k} min w, the truncation changes the optimum
    by a relative amount of at most N * trunc * e^{2 u k} (< 1e-8 in every use here).  If the default solver
    fails, the dual simplex and then the interior-point solver are tried; the counts are kept in LP_FALLBACKS."""
    N = len(mu_num)
    num = np.where(mu_num < trunc * mu_num.max(), 0.0, mu_num)
    den = np.where(mu_den < trunc * mu_den.max(), 0.0, mu_den)
    for method in ("highs", "highs-ds", "highs-ipm"):
        res = linprog(-num, A_ub=A_ub, b_ub=np.zeros(A_ub.shape[0]), A_eq=den[None, :], b_eq=[1.0],
                      bounds=[(0, None)] * N, method=method)
        if res.status == 0:
            LP_FALLBACKS[method] += 1
            return -res.fun
    LP_FALLBACKS["failed"] += 1
    raise RuntimeError("LP failed with all three HiGHS methods: " + res.message)


def iota_lipschitz_lp(logmu, A_ub, pairs=None):
    """Exact Lipschitz-class influence by LP on the whole inner block, for the listed ordered pairs (default all)."""
    nA = logmu.shape[0]
    mu = np.exp(logmu)
    out = np.full((nA, nA), np.nan)
    np.fill_diagonal(out, 0.0)
    if pairs is None:
        pairs = [(a, a2) for a in range(nA) for a2 in range(nA) if a != a2]
    for a, a2 in pairs:
        out[a, a2] = np.log(lp_ratio(mu[a], mu[a2], A_ub))
    return out


def box_lp(mu_num, mu_den, D):
    """Check of the level-set formula: Charnes-Cooper LP for sup <mu_num,w>/<mu_den,w> over 1 <= w <= e^D.
    Variables (y, t): y = t w.  max <mu_num,y> s.t. <mu_den,y> = 1, t <= y <= e^D t."""
    N = len(mu_num)
    c = np.concatenate([-mu_num, [0.0]])
    I = sparse.identity(N, format="csr")
    one = sparse.csr_matrix(np.ones((N, 1)))
    A1 = sparse.hstack([-I, one])                    # t - y <= 0
    A2 = sparse.hstack([I, -np.exp(D) * one])        # y - e^D t <= 0
    A_ub = sparse.vstack([A1, A2]).tocsr()
    A_eq = np.concatenate([mu_den, [0.0]])[None, :]
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(2 * N), A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)] * (N + 1),
                  method="highs")
    if res.status != 0:
        raise RuntimeError("box LP failed: " + res.message)
    return -res.fun


# ------------------------------------------------------- pairwise recursion (nearest-neighbour chains only)

def small_cone_lp(pnum, pden, v):
    """sup <pnum,W>/<pden,W> over W > 0 on q points with W(z) <= e^{v[z,z']} W(z') for all z != z'."""
    q = len(pnum)
    rows, b = [], []
    for z in range(q):
        for z2 in range(q):
            if z != z2 and np.isfinite(v[z, z2]):
                row = np.zeros(q)
                row[z] = 1.0
                row[z2] = -np.exp(v[z, z2])
                rows.append(row)
    res = linprog(-pnum, A_ub=np.array(rows), b_ub=np.zeros(len(rows)), A_eq=pden[None, :], b_eq=[1.0],
                  bounds=[(0, None)] * q, method="highs")
    if res.status != 0:
        raise RuntimeError("small LP failed: " + res.message)
    return -res.fun


def recursion_bound_nn(model, c, u):
    """Upper bound of iota_L across the cut of a nearest-neighbour chain (r = 1), in polynomial time.
    v_j[x,y] bounds ln( W_j(x)/W_j(y) ), W_j(x) = E[w | b_j = x], w log-u-Lipschitz on the sites j..n-1:
        v_{n-1} = u (x != y);   v_j[x,y] = u + ln sup{ <P_j(.|x),W>/<P_j(.|y),W> : W in cone(v_{j+1}) },
    P_j(z|x) = law of site j+1 given site j = x in the inner chain.  At the cut the same programme with the two
    conditional laws of the first inner site."""
    assert model["r"] == 1
    n, q = model["n"], model["q"]
    # backward messages logR_j[x] = ln sum over sites > j of exp(-energy of the terms on sites >= j), site j = x
    logR = [None] * n
    logR[n - 1] = -model["h"][n - 1]
    for j in range(n - 2, c - 1, -1):
        logR[j] = -model["h"][j] + logsumexp(-model["pair"][(j, j + 1)] + logR[j + 1][None, :], axis=1)
    v = u * (1.0 - np.eye(q))
    for j in range(n - 2, c - 1, -1):
        lw = -model["pair"][(j, j + 1)] + logR[j + 1][None, :]
        P = np.exp(lw - logsumexp(lw, axis=1, keepdims=True))          # P[x, z]
        vnew = np.zeros((q, q))
        for x in range(q):
            for y in range(q):
                if x != y:
                    vnew[x, y] = u + np.log(small_cone_lp(P[x], P[y], v))
        v = vnew
    lw = -model["pair"][(c - 1, c)] + logR[c][None, :]
    P = np.exp(lw - logsumexp(lw, axis=1, keepdims=True))              # P[alpha, beta]
    out = np.zeros((q, q))
    for a in range(q):
        for a2 in range(q):
            if a != a2:
                out[a, a2] = np.log(small_cone_lp(P[a], P[a2], v))
    return out, v


# ----------------------------------------------------------------------------- self-test

def selftest():
    rng = np.random.default_rng(20261126)
    viol = 0
    worst = 0.0
    # (1) brute force against transfer matrices and the boundary formula, 24 random models
    for trial in range(24):
        q = int(rng.integers(2, 5))
        r = int(rng.integers(1, 4))
        n = int(rng.integers(max(2 * r, 4), 9))
        c = int(rng.integers(1, n))
        if q ** (n - c) > 5000:
            c = n - 4
        base = make_base(n, q, r, rng, clash_frac=0.2)
        model = energies(base, J=float(rng.choice([0.5, 1.0, 3.0])), C=float(rng.choice([10.0, 25.0])), field=0.5)
        alphas, bconf, logmu = brute_conditionals(model, c)
        al2, betas, Ex, logR, logpi = boundary_layer(model, c)
        assert np.array_equal(alphas, al2)
        ipt_b = iota_pointwise_brute(logmu)
        ipt_f, osc = iota_pointwise_formula(Ex, logpi)
        d = np.abs(ipt_b - ipt_f).max()
        worst = max(worst, d)
        if d > 1e-9 or (ipt_b > osc + 1e-9).any() or (ipt_b < -1e-9).any():
            viol += 1
        # marginal of the inner boundary layer from the enumeration against the transfer matrices
        kb = betas.shape[1]
        key = (bconf[:, :kb] * (q ** np.arange(kb - 1, -1, -1))[None, :]).sum(axis=1)
        marg = np.zeros((len(alphas), len(betas)))
        for a in range(len(alphas)):
            np.add.at(marg[a], key, np.exp(logmu[a]))
        d2 = np.abs(marg - np.exp(logpi)).max()
        worst = max(worst, d2)
        if d2 > 1e-10:
            viol += 1
    print(f"selftest 1: brute force vs transfer matrices vs boundary formula, 24 models: violations {viol}, "
          f"largest difference {worst:.2e}")
    # (2) box influence: the level-set formula on the inner boundary layer against
    #     (a) the maximum over ALL 2^(q^r) vertex weights W in {1, e^D}^(boundary layer) (exhaustive; the ratio
    #         depends on w only through W = E[w | beta], and a linear-fractional function on a box is maximal at a
    #         vertex);
    #     (b) the Charnes-Cooper LP on the WHOLE inner block (no use of the boundary reduction), for D <= 3 only.
    #     Own errors on the way (kept in the logs): for D = 12 the LP variables are of size e^-12 and HiGHS'
    #     absolute feasibility tolerance inflates the optimum by up to 8e-4 (out_band_selftest_1.txt); a residual
    #     F(t*) with cancellation, and an "optimality condition" that ignored configurations of mass below 1e-17,
    #     reported false violations (out_band_selftest_2.txt, _3.txt).  None was a defect of the formula.
    v2, w2, w2b, n2, n2b = 0, 0.0, 0.0, 0, 0
    for trial in range(8):
        q, r, n, c = 3, int(rng.integers(1, 3)), 7, 3
        base = make_base(n, q, r, rng, clash_frac=0.2)
        model = energies(base, J=1.0, C=15.0)
        alphas, bconf, logmu = brute_conditionals(model, c)
        _, betas, Ex, logR, logpi = boundary_layer(model, c)
        mu = np.exp(logmu)
        pi = np.exp(logpi)
        nb = pi.shape[1]
        subsets = ((np.arange(2 ** nb)[:, None] >> np.arange(nb)[None, :]) & 1).astype(float)   # all vertices
        for D in (0.5, 3.0, 12.0, 30.0):
            lev = iota_box_levelset(logpi, D)
            g = np.expm1(D)
            PA = subsets @ pi.T                                   # [subset, alpha]
            for a in range(len(alphas)):
                for a2 in range(len(alphas)):
                    if a == a2:
                        continue
                    best = np.log(((1 + g * PA[:, a]) / (1 + g * PA[:, a2])).max())
                    n2 += 1
                    w2 = max(w2, abs(best - lev[a, a2]))
                    if abs(best - lev[a, a2]) > 1e-10:
                        v2 += 1
            if D <= 3.0:
                for (a, a2) in [(0, 1), (1, 0), (0, len(alphas) - 1)]:
                    val = np.log(box_lp(mu[a], mu[a2], D))
                    n2b += 1
                    w2b = max(w2b, abs(val - lev[a, a2]))
                    if abs(val - lev[a, a2]) > 1e-6:
                        v2 += 1
    print(f"selftest 2: box influence, level-set formula vs all 2^(q^r) vertex weights on the boundary layer, "
          f"{n2} cases, largest difference {w2:.2e}; vs LP on the whole block for D <= 3, {n2b} cases, largest "
          f"difference {w2b:.2e}; violations {v2}")
    # (3) Lipschitz LP against the closed form for product conditional laws Bernoulli(p)^k (N_REPORT 2.7)
    v3, w3 = 0, 0.0
    k = 6
    conf = configs(2, k)
    wt = conf.sum(axis=1)
    for (p, p2, u) in [(0.3, 0.6, 1.0), (0.9, 0.2, 0.5), (0.05, 0.5, 2.0), (0.5, 0.45, 1.5)]:
        A = lipschitz_constraints(2, k, u)
        mu1 = p ** wt * (1 - p) ** (k - wt)
        mu2 = p2 ** wt * (1 - p2) ** (k - wt)
        val = np.log(lp_ratio(mu1, mu2, A))
        closed = k * max(np.log((1 + p * (np.exp(s * u) - 1)) / (1 + p2 * (np.exp(s * u) - 1))) for s in (1, -1))
        w3 = max(w3, abs(val - closed))
        if abs(val - closed) > 1e-6:
            v3 += 1
    print(f"selftest 3: Lipschitz LP vs k*max ln[(1+p(e^(+-u)-1))/(1+p'(e^(+-u)-1))], 4 cases: violations {v3}, "
          f"largest difference {w3:.2e}")
    # (4) symmetric binary chain: LP against the recursion v -> u + g(v), g(v) = ln[((1-p)e^v + p)/(p e^v + 1-p)]
    v4, w4 = 0, 0.0
    lines = []
    for (p, u, kin) in [(0.3, 1.0, 6), (0.1, 1.0, 6), (0.2, 0.5, 6), (0.3, 2.35, 6), (0.1, 1.0, 8)]:
        n, c = kin + 2, 2
        Jc = 0.5 * np.log((1 - p) / p)            # e(x,y) = -Jc if x == y, +Jc otherwise  => P(flip) = p
        pair = {(i, i + 1): np.array([[-Jc, Jc], [Jc, -Jc]]) for i in range(n - 1)}
        model = dict(n=n, q=2, r=1, pair=pair, h=np.zeros((n, 2)))
        alphas, bconf, logmu = brute_conditionals(model, c)
        A = lipschitz_constraints(2, kin, u)
        lp = iota_lipschitz_lp(logmu, A)
        rec, _ = recursion_bound_nn(model, c, u)
        v = u
        for _ in range(kin - 1):
            v = u + np.log(((1 - p) * np.exp(v) + p) / (p * np.exp(v) + 1 - p))
        g = np.log(((1 - p) * np.exp(v) + p) / (p * np.exp(v) + 1 - p))
        d = max(abs(lp[0, 1] - g), abs(lp[1, 0] - g), abs(rec[0, 1] - g))
        w4 = max(w4, d)
        if d > 1e-6:
            v4 += 1
        lines.append(f"    p={p} u={u} k={kin}: u+iota: LP {u + lp[0, 1]:.6f}  recursion {u + rec[0, 1]:.6f}  "
                     f"closed form u+g(v^(k)) {u + g:.6f}   pointwise u+K {u + np.log((1 - p) / p):.4f}")
    print(f"selftest 4: symmetric binary chain, LP vs own recursion vs closed form, 5 cases: violations {v4}, "
          f"largest difference {w4:.2e}")
    for ln_ in lines:
        print(ln_)
    total = viol + v2 + v3 + v4
    print(f"selftest total violations: {total}")
    return total


if __name__ == "__main__":
    t0 = time.time()
    tot = selftest()
    print(f"elapsed {time.time() - t0:.1f} s; peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
    sys.exit(1 if tot else 0)
