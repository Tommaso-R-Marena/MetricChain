#!/usr/bin/env python3
"""
R1 (SCI-REV-0001) -- the remark "more than two letters" AS CORRECTED at theory checkpoint 89ac710, and the numbers of
Proposition 11.103(d), (e) that it now points to.  Own code, written from the STATEMENT of Theorem 11.99:

  site (pi, d = u*Hamming) on q letters; Lipschitz polytope L = {gamma : gamma(a) - gamma(b) <= u}; its vertices modulo
  constants are u * indicator(S), S a non-empty proper subset of the letters; pi_S ~ pi * exp(-u 1_S) ("vertex channel").
      F*(t) = max_M  -t ln sum_a ( sum_S M(S) pi_S(a)^t )^(1/t)  =  min_Q max_S  -ln sum_a pi_S(a)^t Q(a)^(1-t)
      E = lim F*(t)/t (t->0)   = max_M -ln sum_a prod_S pi_S(a)^M(S) = min_Q max_S KL(Q || pi_S)      (threshold)
      a = lim F*(t)/(1-t) (t->1) = Shannon capacity of the vertex channel
      h = max_{0<=t<=1} F*(t)   (= R-hat(0), the exponent at vanishing accuracy)
The formulas themselves (Theorems 11.98, 11.99, workstream W) are NOT reviewed here -- this script only checks that the
numbers quoted in the corrected remark and in Proposition 11.103(d),(e) follow from them, with a duality bracket
(lower value from M, upper value from the centre Q built from M) for every optimum.

Checked:
 (S1) thresholds at u = 1: uniform three letters 0.119499, pi = (0.05, 0.5, 0.45) 0.120196, two-letter cube 0.120115;
 (S2) uniform sites, q = 3, 4, u in {0.5, 1, 2, 3}: E, a, h against the values of single dips on k equal groups, k | q;
      q = 4, u = 1: h = h_2 = 0.029139, a = a_4 = 0.117993, E = E_2 = 0.120115;
 (S3) three-letter laws near (1/2, 1/2, 0): h -> h_2 = 0.007673 > h_3 = 0.007425 at u = 0.5; a_2 > a_3 iff u < 0.5194
      (0.011125 against 0.010582 at u = 0.3);
 (S4) h_k = h_{k+1} exactly at e^u = k(k-1);
 (S5) the grid of 171 three-letter laws (i, j, k)/20: is the uniform law the hardest for h at u = 1, 2 (claimed yes) and at
      u = 0.5 (claimed no)?
 (S6) referee's elementary remark: a uniform four-letter site is a pair of uniform bits, so every lower bound of the binary
      cube transfers to it (value of the pair grouping = binary value, for every u and t).
Run:  python3 remark_v2_sites.py
"""
import itertools
import math
import sys

import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar

ok_all = True


def report(name, ok, detail):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    sys.stdout.flush()


def vertex_laws(pi, u):
    """Gibbs laws pi_S ~ pi * exp(-u 1_S) of the vertices u*1_S, S non-empty proper subset"""
    q = len(pi)
    out, labels = [], []
    for r in range(1, q):
        for S in itertools.combinations(range(q), r):
            w = np.array(pi, float)
            w[list(S)] *= math.exp(-u)
            out.append(w / w.sum())
            labels.append(S)
    return np.array(out), labels


def simplex_min(fun, n, starts=4, seed=0):
    """minimise a smooth convex function over the probability simplex (SLSQP, several starts)"""
    rng = np.random.default_rng(seed)
    best = None
    cons = [{"type": "eq", "fun": lambda m: np.sum(m) - 1.0}]
    for s in range(starts):
        m0 = np.ones(n) / n if s == 0 else rng.dirichlet(np.ones(n))
        res = minimize(fun, m0, method="SLSQP", bounds=[(0.0, 1.0)] * n, constraints=cons,
                       options={"maxiter": 2000, "ftol": 1e-16})
        m = np.clip(res.x, 0, None)
        m = m / m.sum()
        v = fun(m)
        if best is None or v < best[0]:
            best = (v, m)
    return best


def Fstar(P, t):
    """returns (lower, upper) bracket of F*(t) for the vertex channel with rows P (0 < t < 1)"""
    Pt = P ** t
    g = lambda M: float(np.sum((M @ Pt) ** (1.0 / t)))
    val, M = simplex_min(g, P.shape[0])
    lower = -t * math.log(val)
    Q = (M @ Pt) ** (1.0 / t)
    Q = Q / Q.sum()
    upper = float(np.max(-np.log(Pt @ (Q ** (1.0 - t)))))
    return lower, upper, M


def threshold_E(P):
    lnP = np.log(P)
    f = lambda M: float(np.log(np.sum(np.exp(M @ lnP))))          # minimise ln sum_a prod pi_S^M
    val, M = simplex_min(f, P.shape[0])
    lower = -val
    Q = np.exp(M @ lnP)
    Q = Q / Q.sum()
    upper = float(np.max(np.sum(Q[None, :] * (np.log(Q)[None, :] - lnP), axis=1)))
    return lower, upper, M


def capacity_a(P, iters=20000, tol=1e-13):
    """Blahut-Arimoto with the standard bracket  I(M) <= C <= max_S KL(pi_S || Q_M)"""
    n = P.shape[0]
    M = np.ones(n) / n
    for _ in range(iters):
        Q = M @ P
        D = np.sum(P * (np.log(P) - np.log(Q)[None, :]), axis=1)
        lower, upper = float(M @ D), float(D.max())
        if upper - lower < tol:
            break
        M = M * np.exp(D)
        M /= M.sum()
    return lower, upper, M


def h_value(P, ngrid=120):
    """max_t F*(t): grid (F* may have kinks = label switches), then local polishing; returns (h, t*, max bracket gap)"""
    ts = np.linspace(0.02, 0.98, ngrid)
    vals, gaps = [], []
    for t in ts:
        lo, up, _ = Fstar(P, float(t))
        vals.append(lo)
        gaps.append(up - lo)
    i = int(np.argmax(vals))
    res = minimize_scalar(lambda t: -Fstar(P, float(t))[0], bounds=(ts[max(i - 1, 0)], ts[min(i + 1, ngrid - 1)]),
                          method="bounded", options={"xatol": 1e-10})
    lo, up, _ = Fstar(P, float(res.x))
    if lo >= vals[i]:
        return lo, float(res.x), max(max(gaps), up - lo)
    return vals[i], float(ts[i]), max(gaps)


# closed forms for single dips on k equally weighted groups
def Psi_k(k, s):
    return math.log((math.exp(s) + k - 1) / k) - s / k


def h_k(k, u):
    r = minimize_scalar(lambda t: -(t * Psi_k(k, u) - Psi_k(k, t * u)), bounds=(0, 1), method="bounded",
                        options={"xatol": 1e-14})
    return -r.fun


def a_k(k, u):
    Z = math.exp(u) + k - 1
    return math.log(k) - math.log(Z) + u * math.exp(u) / Z


def main():
    # ---------------- (S1) thresholds at u = 1 ----------------
    u = 1.0
    rows = []
    good = True
    for name, pi, claimed in (("uniform, 3 letters", [1 / 3] * 3, 0.119499), ("pi = (0.05, 0.5, 0.45)", [0.05, 0.5, 0.45], 0.120196),
                              ("uniform, 2 letters", [0.5, 0.5], 0.120115)):
        P, _ = vertex_laws(pi, u)
        lo, up, _ = threshold_E(P)
        good &= abs(lo - claimed) < 6e-7 and up - lo < 1e-8
        rows.append(f"{name}: E in [{lo:.9f}, {up:.9f}] (claimed {claimed})")
    report("(S1) thresholds, u=1", good, "; ".join(rows))

    # ---------------- (S2) uniform sites ----------------
    print("      uniform sites: value from the vertex channel (all 2^q - 2 vertices) | best equal grouping k | q")
    good = True
    maxgap = 0.0
    for q in (3, 4):
        ks = [k for k in range(2, q + 1) if q % k == 0]
        for u in (0.5, 1.0, 2.0, 3.0):
            P, _ = vertex_laws([1 / q] * q, u)
            Elo, Eup, _ = threshold_E(P)
            alo, aup, _ = capacity_a(P)
            h, tstar, gap = h_value(P)
            maxgap = max(maxgap, gap, Eup - Elo, aup - alo)
            Ebest = max(ks, key=lambda k: Psi_k(k, u))
            abest = max(ks, key=lambda k: a_k(k, u))
            hbest = max(ks, key=lambda k: h_k(k, u))
            okrow = abs(Elo - Psi_k(Ebest, u)) < 1e-7 and abs(alo - a_k(abest, u)) < 1e-7 and abs(h - h_k(hbest, u)) < 1e-7
            good &= okrow
            print(f"        q={q} u={u}: E = {Elo:.6f} (k={Ebest}: {Psi_k(Ebest, u):.6f})   a = {alo:.6f} (k={abest}: {a_k(abest, u):.6f})   "
                  f"h = {h:.6f} at t={tstar:.3f} (k={hbest}: {h_k(hbest, u):.6f})   {'ok' if okrow else 'MISMATCH'}")
    P, _ = vertex_laws([0.25] * 4, 1.0)
    q4 = (threshold_E(P)[0], capacity_a(P)[0], h_value(P)[0])
    good &= abs(q4[0] - 0.120115) < 6e-7 and abs(q4[1] - 0.117993) < 6e-7 and abs(q4[2] - 0.029139) < 6e-7
    report("(S2) uniform sites group their letters", good,
           f"q = 3, 4, u in (.5,1,2,3): E, a, h equal the best equal grouping in all 8 cases (largest duality bracket {maxgap:.1e}); "
           f"q=4,u=1: E={q4[0]:.6f} (=E_2, claimed 0.120115), a={q4[1]:.6f} (=a_4, claimed 0.117993), h={q4[2]:.6f} (=h_2, claimed 0.029139); "
           f"the single-dip-on-letters values quoted at 5ed4072 for k=4 were h_4(0.5)={h_k(4, 0.5):.6f}, h_4(1)={h_k(4, 1.0):.6f}")

    # ---------------- (S3) three-letter laws near (1/2, 1/2, 0) ----------------
    good = True
    u = 0.5
    line = []
    for d3 in (1 / 3, 0.1, 0.01, 0.001, 0.0001):
        pi = [(1 - d3) / 2, (1 - d3) / 2, d3]
        P, _ = vertex_laws(pi, u)
        h, tstar, gap = h_value(P, ngrid=60)
        line.append(f"pi_3={d3:.4f}: h={h:.6f}")
        last = h
    good &= abs(last - 0.007673) < 5e-6 and abs(h_k(3, u) - 0.007425) < 6e-7 and abs(h_k(2, u) - 0.007673) < 6e-7
    ucross = brentq(lambda x: a_k(2, x) - a_k(3, x), 0.2, 1.0, xtol=1e-14)
    good &= abs(a_k(2, 0.3) - 0.011125) < 6e-7 and abs(a_k(3, 0.3) - 0.010582) < 6e-7 and abs(ucross - 0.5194) < 5e-5
    report("(S3) near (1/2,1/2,0), u=0.5", good, "; ".join(line) + f"  (h_2 = {h_k(2, u):.6f}, h_3 = {h_k(3, u):.6f}); "
           f"a_2(0.3) = {a_k(2, 0.3):.6f}, a_3(0.3) = {a_k(3, 0.3):.6f}, a_2 = a_3 at u = {ucross:.6f}")

    # ---------------- (S4) exact crossings ----------------
    good = True
    line = []
    for k in (2, 3, 4, 5):
        uc = brentq(lambda x: h_k(k, x) - h_k(k + 1, x), 0.5 * math.log(k * (k - 1)) + 0.05, 2 * math.log(k * (k - 1)) + 0.5, xtol=1e-13)
        good &= abs(uc - math.log(k * (k - 1))) < 1e-8
        line.append(f"h_{k} = h_{k + 1} at u = {uc:.10f} (ln {k * (k - 1)} = {math.log(k * (k - 1)):.10f})")
    report("(S4) crossings e^u = k(k-1)", good, "; ".join(line))

    # ---------------- (S5) grid of 171 three-letter laws ----------------
    print("      grid of 171 three-letter laws (i,j,k)/20: the law with the largest h, against the uniform law")
    good = True
    for u, claim_uniform_hardest in ((1.0, True), (2.0, True), (0.5, False)):
        Pu, _ = vertex_laws([1 / 3] * 3, u)
        hu = h_value(Pu, ngrid=60)[0]
        best = (-1, None)
        for i in range(1, 19):
            for j in range(i, 19):           # symmetry: sort the first two; third free
                k3 = 20 - i - j
                if k3 < 1:
                    continue
                pi = [i / 20, j / 20, k3 / 20]
                P, _ = vertex_laws(pi, u)
                hv = h_value(P, ngrid=40)[0]
                if hv > best[0]:
                    best = (hv, pi)
        uniform_hardest = best[0] <= hu + 1e-9
        good &= (uniform_hardest == claim_uniform_hardest)
        print(f"        u={u}: h(uniform) = {hu:.6f}; largest h on the grid = {best[0]:.6f} at pi = {best[1]}  "
              f"-> uniform law hardest on the grid: {uniform_hardest} (claimed {claim_uniform_hardest})")
    report("(S5) which three-letter law is hardest", good, "uniform law hardest for h on the grid at u = 1, 2; NOT at u = 0.5 "
                                                           "(laws near (1/2,1/2,0) are harder)")

    # ---------------- (S6) four letters = two bits ----------------
    worst = 0.0
    for u in (0.3, 0.5, 1.0, 2.0, 3.0):
        P, labels = vertex_laws([0.25] * 4, u)
        for t in (0.2, 0.5, 0.8):
            lo, up, M = Fstar(P, t)
            binary = t * Psi_k(2, u) - Psi_k(2, t * u)
            worst = min(worst, lo - binary) if worst else lo - binary
            worst = min(worst, lo - binary)
    report("(S6) four letters contain the binary cube", worst >= -1e-9,
           f"F*_(uniform 4 letters)(t) - F*_(binary cube)(t) >= {worst:.2e} for u in (.3,.5,1,2,3), t in (.2,.5,.8)")
    print()
    print("SUMMARY:", "ALL PASS" if ok_all else "FAILURES")


if __name__ == "__main__":
    main()
