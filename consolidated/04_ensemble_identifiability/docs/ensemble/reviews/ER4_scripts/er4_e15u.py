#!/usr/bin/env python3
"""ER4 (internal AI review) -- Proposition E15U beyond its main statement (report b654396, lines 1537-1642).
Own code, from the statement.

STATUS: WRITTEN, NEVER RUN.  The review was wound down (controlled consolidation of the programme) before this
script was executed.  It has no output file, it may contain errors, and nothing in the review report rests on it.
It is kept only so that the author or a later reviewer can run it.

Setting: binary sites, disagreement variables e in {0,1}^n, reference pi > 0, slopes b_i > 0, class
  P = { mu = w pi :  w(y) <= exp(b_i) w(x)  for all pairs x, y differing in one site i },
nu = mu*_a proportional to pi exp(-sum b_i e_i).

1. (A), (B), (C), (C') against exact optimisation over the class polytope (n = 2, 3; random references with
   couplings of both signs; random slopes):
     (A)  every member dominates nu stochastically     <=>  Cov(1_U, 1_W) >= 0 for all up-sets
     (B)  mu(e_i = 1) >= nu(e_i = 1) for all members    <=>  Cov(1_U, e_i) >= 0 for all up-sets, all i
     (C)  TV(mu, nu) <= E_mu N - E_nu N                 <=>  Var 1_U <= Cov(1_U, N)
     (C') TV(mu, nu) <= E_mu[N - A]  (A the compensator of N for the given order of the sites)
                                                       <=>  Var 1_U <= Cov(1_U, N - A)
   The left sides are decided by linear programmes over the class (for the total variation: one programme per
   sign pattern, 2^(2^n) of them); the right sides by enumeration of the up-sets.
2. The parity example on three sites, nu = (1 - lambda (-1)^N)/8: the slacks in closed form (sympy), the threshold.
3. The four-site instance of consequence 3, recomputed (fractions are not available for exponentials: mpmath, 40
   digits): (D) for every site, the least E[N|U] - E[N|U^c] over all 166 non-trivial up-sets, the violating member.
4. The weak-coupling rule of consequence 1 on random four-site instances at eps = 0.02, 0.005.
"""
import itertools
import sys

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.optimize import linprog

rng = np.random.default_rng(1511)


def configs(n):
    return list(itertools.product((0, 1), repeat=n))


def upsets(n):
    """all up-sets of {0,1}^n as boolean vectors over configs(n) (including the empty set and everything)"""
    C = configs(n)
    idx = {c: i for i, c in enumerate(C)}
    ups = []
    covers = []
    for i, c in enumerate(C):
        for k in range(n):
            if c[k] == 0:
                d = list(c)
                d[k] = 1
                covers.append((i, idx[tuple(d)]))
    for mask in range(1 << len(C)):
        ok = True
        for lo, hi in covers:
            if (mask >> lo) & 1 and not (mask >> hi) & 1:
                ok = False
                break
        if ok:
            ups.append(np.array([(mask >> i) & 1 for i in range(len(C))], dtype=float))
    return ups


def class_constraints(n, pi, b):
    """A_ub, b_ub for mu in the class (variables mu(x)); pairs differing in one site, both directions"""
    C = configs(n)
    idx = {c: i for i, c in enumerate(C)}
    rows = []
    for i, c in enumerate(C):
        for k in range(n):
            d = list(c)
            d[k] = 1 - d[k]
            j = idx[tuple(d)]
            # w(j) <= exp(b_k) w(i):  mu(j)/pi(j) - exp(b_k) mu(i)/pi(i) <= 0
            row = np.zeros(len(C))
            row[j] = 1.0 / pi[j]
            row[i] = -np.exp(b[k]) / pi[i]
            rows.append(row)
    return np.array(rows), np.zeros(len(rows))


def lp_max(c, A_ub, b_ub, m):
    res = linprog(-np.asarray(c), A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, m)), b_eq=[1.0], bounds=[(0, None)] * m,
                  method="highs")
    assert res.status == 0
    return -res.fun


def part1():
    print("1. (A), (B), (C), (C') against exact optimisation over the class polytope")
    tally = {"A": [0, 0, 0], "B": [0, 0, 0], "C": [0, 0, 0], "C'": [0, 0, 0]}      # agree, holds, total
    margin = 1e-7
    skipped = 0
    for n, cases in ((2, 150), (3, 90)):
        C = configs(n)
        m = len(C)
        E = np.array(C, dtype=float)                      # m x n
        N = E.sum(1)
        ups = upsets(n)
        signs = [np.array(s, dtype=float) for s in itertools.product((1.0, -1.0), repeat=m)]
        for case in range(cases):
            K = rng.normal(scale=rng.choice((0.3, 1.0, 2.0)), size=(n, n))
            K = np.triu(K, 1)
            l = rng.normal(scale=0.7, size=n)
            K3 = rng.normal(scale=rng.choice((0.0, 1.0))) if n == 3 else 0.0
            logpi = np.array([e @ K @ e + l @ e + K3 * np.prod(e) for e in E])
            pi = np.exp(logpi - logpi.max())
            pi /= pi.sum()
            b = rng.uniform(0.2, 1.5, size=n)
            nu = pi * np.exp(-E @ b)
            nu /= nu.sum()
            A_ub, b_ub = class_constraints(n, pi, b)
            # compensator A(e) = sum_i nu(e_i = 1 | e_<i)
            comp = np.zeros(m)
            for i in range(n):
                for x in range(m):
                    same = np.all(E[:, :i] == E[x, :i], axis=1)
                    comp[x] += nu[same & (E[:, i] == 1)].sum() / nu[same].sum()
            # ---------------- right sides (up-sets)
            slackA = min(nu @ (U * W) - (nu @ U) * (nu @ W) for U in ups for W in ups)
            slackB = min(nu @ (U * E[:, i]) - (nu @ U) * (nu @ E[:, i]) for U in ups for i in range(n))
            slackC = min((nu @ (U * N) - (nu @ U) * (nu @ N)) - (nu @ U) * (1 - nu @ U) for U in ups)
            NA = N - comp
            slackCp = min((nu @ (U * NA) - (nu @ U) * (nu @ NA)) - (nu @ U) * (1 - nu @ U) for U in ups)
            # ---------------- left sides (linear programmes over the class)
            # (A): min over members of mu(W) - nu(W), over all up-sets W
            worstA = max(lp_max(-W, A_ub, b_ub, m) + nu @ W for W in ups)          # max of nu(W) - mu(W)
            worstB = max(lp_max(-E[:, i], A_ub, b_ub, m) + nu @ E[:, i] for i in range(n))
            # (C), (C'): max over members of TV - L, L(mu) = E_mu[N] - E_nu[N]  resp.  E_mu[N - A]
            worstC = max(lp_max(0.5 * s - N, A_ub, b_ub, m) - 0.5 * s @ nu + nu @ N for s in signs)
            worstCp = max(lp_max(0.5 * s - NA, A_ub, b_ub, m) - 0.5 * s @ nu for s in signs)
            for key, slack, worst in (("A", slackA, worstA), ("B", slackB, worstB), ("C", slackC, worstC),
                                      ("C'", slackCp, worstCp)):
                if abs(slack) < margin or abs(worst) < margin and slack < -margin:
                    # borderline; (when the condition holds the exact maximum is 0, attained at nu itself)
                    pass
                holds_cond = slack > -1e-10
                holds_class = worst < 1e-9
                tally[key][2] += 1
                tally[key][0] += int(holds_cond == holds_class)
                tally[key][1] += int(holds_cond)
                if holds_cond != holds_class:
                    print(f"      DISAGREEMENT n = {n} case {case} {key}: least slack over up-sets {slack:.3e}, largest "
                          f"excess over the class {worst:.3e}")
    for key in ("A", "B", "C", "C'"):
        a, h, t = tally[key]
        print(f"    ({key}): criterion on up-sets and exact optimisation over the class agree in {a}/{t} "
              f"(the statement holds in {h})")
    return all(tally[k][0] == tally[k][2] for k in tally)


def part2():
    print("2. the parity example nu = (1 - lambda (-1)^N)/8 on three sites: slack Cov(1_U, N) - Var(1_U) for all 20 up-sets")
    lam = sp.symbols("lambda", positive=True)
    C = configs(3)
    nu = [sp.Rational(1, 8) * (1 - lam * (-1) ** sum(c)) for c in C]
    N = [sum(c) for c in C]
    ups = upsets(3)
    found = {}
    for U in ups:
        pU = sum(nu[i] for i in range(8) if U[i])
        if pU == 0 or sp.simplify(pU - 1) == 0:
            continue
        cov = sum(nu[i] * N[i] for i in range(8) if U[i]) - pU * sum(nu[i] * N[i] for i in range(8))
        slack = sp.factor(sp.simplify(cov - pU * (1 - pU)))
        members = tuple(int(x) for x in U)
        found.setdefault(str(slack), []).append(int(sum(members)))
    for k, v in sorted(found.items(), key=lambda kv: kv[1]):
        print(f"    slack {k:36s} for {len(v)} up-sets with {sorted(set(v))} elements")
    # pair covariances
    cov12 = sp.simplify(sum(nu[i] * C[i][0] * C[i][1] for i in range(8)) - sum(nu[i] * C[i][0] for i in range(8))
                        * sum(nu[i] * C[i][1] for i in range(8)))
    print(f"    pair covariance Cov(e_1, e_2) = {cov12};  the only slack that can be negative on 0 < lambda < 1 is "
          f"(1 - 2 lambda)/16: the bound holds iff lambda <= 1/2")
    exprs = [sp.sympify(k) for k in found]
    neg = [e for e in exprs if sp.solve(sp.And(e < 0, lam < 1, lam > 0), lam) != sp.false
           and sp.reduce_inequalities([e < 0, lam < 1, lam > 0], lam) != sp.false]
    return len(neg) == 1 and sp.simplify(neg[0] - (1 - 2 * lam) / 16) == 0


def part3():
    print("3. the four-site instance of consequence 3 (40-digit arithmetic)")
    mp.mp.dps = 40
    n = 4
    C = configs(n)
    Kd = {(0, 1): mp.mpf("-1.4"), (0, 2): mp.mpf(6), (0, 3): mp.mpf("-2.6"), (1, 2): mp.mpf("-0.5"),
          (1, 3): mp.mpf("3.3"), (2, 3): mp.mpf(0)}
    l = [mp.mpf("0.1"), mp.mpf("0.5"), mp.mpf(-1), mp.mpf("1.4")]
    wts = []
    for c in C:
        v = sum(Kd[(i, j)] * c[i] * c[j] for (i, j) in Kd) + sum(l[i] * c[i] for i in range(n))
        wts.append(mp.e ** v)
    Z = sum(wts)
    nu = [w / Z for w in wts]
    N = [sum(c) for c in C]

    def E(f):
        return sum(nu[i] * f[i] for i in range(len(C)))

    covD = []
    for i in range(n):
        ei = [c[i] for c in C]
        rest = [N[k] - ei[k] for k in range(len(C))]
        covD.append(E([ei[k] * rest[k] for k in range(len(C))]) - E(ei) * E(rest))
    print("    Cov(e_i, N - e_i), i = 1..4:", ", ".join(mp.nstr(x, 6) for x in covD), "  (report: every one at least 0.0105)")
    ups = upsets(n)
    best = (mp.inf, None)
    for U in ups:
        pU = sum(nu[i] for i in range(len(C)) if U[i])
        if U.sum() == 0 or U.sum() == len(C):
            continue
        d = sum(nu[i] * N[i] for i in range(len(C)) if U[i]) / pU - sum(nu[i] * N[i] for i in range(len(C)) if not U[i]) / (1 - pU)
        if d < best[0]:
            best = (d, U)
    Ustar = [C[i] for i in range(len(C)) if best[1][i]]
    print(f"    number of up-sets (with the two trivial ones): {len(ups)}; least E[N|U] - E[N|U^c] = {mp.nstr(best[0], 6)} "
          f"at U = {Ustar}")
    U24 = [1 if (c[1] == 1 and c[3] == 1) else 0 for c in C]
    pU = E(U24)
    d24 = E([U24[k] * N[k] for k in range(len(C))]) / pU - E([(1 - U24[k]) * N[k] for k in range(len(C))]) / (1 - pU)
    print(f"    U = {{e_2 = e_4 = 1}}: E[N|U] - E[N|U^c] = {mp.nstr(d24, 6)}  (report: 0.9634)")
    # the member with density proportional to 1 + (e^2 - 1) 1_U, slopes 1
    t = mp.e ** 2 - 1
    dens = [(1 + t * U24[k]) / (1 + t * pU) for k in range(len(C))]
    mu = [nu[k] * dens[k] for k in range(len(C))]
    tv = sum(abs(mu[k] - nu[k]) for k in range(len(C))) / 2
    ssum = sum(mu[k] * N[k] for k in range(len(C))) - E(N)
    print(f"    member with density prop. to 1 + (e^2 - 1) 1_U: TV = {mp.nstr(tv, 6)}, sum of the bound = {mp.nstr(ssum, 6)}  "
          f"(report: 0.2621 against 0.2525)")
    # membership: w = mu/pi with pi = nu exp(+sum e_i) (slopes 1): w(y) <= e w(x) for neighbours
    w = [dens[k] * mp.e ** (-N[k]) for k in range(len(C))]
    idx = {c: i for i, c in enumerate(C)}
    worst = mp.mpf(0)
    for i, c in enumerate(C):
        for k in range(n):
            dcfg = list(c)
            dcfg[k] = 1 - dcfg[k]
            j = idx[tuple(dcfg)]
            worst = max(worst, w[j] / w[i] / mp.e)
    print(f"    membership of that member: largest w(y)/(e w(x)) over neighbouring pairs = {mp.nstr(worst, 8)} (must be <= 1)")
    ok = (min(covD) >= mp.mpf("0.0105") and abs(d24 - mp.mpf("0.9634")) < mp.mpf("5e-5") and abs(tv - mp.mpf("0.2621")) < mp.mpf("5e-5")
          and abs(ssum - mp.mpf("0.2525")) < mp.mpf("5e-5") and worst <= 1 + mp.mpf("1e-30"))
    return bool(ok)


def part4():
    print("4. the weak-coupling rule (consequence 1), four sites: sign of min_i sum_j J_ij a_i a_j v_j against (C)")
    n = 4
    C = configs(n)
    E = np.array(C, dtype=float)
    N = E.sum(1)
    ups = [U for U in upsets(n) if 0 < U.sum() < len(C)]
    out = {}
    for eps in (0.02, 0.005):
        agree = total = holds = aside = 0
        for case in range(300):
            J = np.triu(rng.normal(size=(n, n)), 1)
            J = J + J.T
            h0 = rng.normal(scale=0.8, size=n)                 # product part, in the variables e
            b = rng.uniform(0.3, 1.5, size=n)
            # centre a = (+,...,+): x_i = 1 - 2 e_i
            Xs = 1 - 2 * E
            lognu0 = E @ (h0 - b)
            pair = np.array([0.5 * x @ J @ x for x in Xs])     # sum_{i<j} J_ij x_i x_j
            nu = np.exp(lognu0 + eps * pair)
            nu /= nu.sum()
            p = 1 / (1 + np.exp(-(h0 - b)))
            v = p * (1 - p)
            s = J @ v                                          # a_i a_j = 1
            if np.min(np.abs(s)) < 0.05:
                aside += 1
                continue
            slack = min((nu @ (U * N) - (nu @ U) * (nu @ N)) - (nu @ U) * (1 - nu @ U) for U in ups)
            total += 1
            agree += int((slack >= 0) == (s.min() > 0))
            holds += int(slack >= 0)
        out[eps] = (agree, total, holds, aside)
        print(f"    eps = {eps}: the sign of min_i sum_j J_ij v_j decides (C) in {agree}/{total} instances "
              f"({aside} with some |sum_j J_ij v_j| < 0.05 set aside; (C) holds in {holds})")
    return out[0.005][0] == out[0.005][1]


def main():
    ok = True
    for fn in (part1, part2, part3, part4):
        r = fn()
        print(f"  -> {'ok' if r else 'CHECK FAILED'}", flush=True)
        ok &= bool(r)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
