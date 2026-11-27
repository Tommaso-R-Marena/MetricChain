#!/usr/bin/env python3
"""Assistant C -- own demonstration for finding M1 of SCI-REV-0003 (Theorem 11.84(ii)).

Written from the statement of Theorem 11.84 in docs/THEORY_REPORT.md (section 11.24) and the
constants of K_REPORT.md section 2.2; the reviewer's batched_sim.py was read before, but nothing
is imported from it.

Instance: the flat instance psi = 0 on Q_{n_o} x Q_{n_i}.  Every fibre average is W = 1, so the
candidate set C_2 is a deterministic function of the stored brackets:
  honest rung 1 : every call returns [W e^{-alpha x_1}, W e^{(1-alpha) x_1}]   (ratio e^{x_1}; valid)
  wide rung 1   : every call returns the trivial bracket [e^{-u n_i}, e^{u n_i}] (ratio e^{2 u n_i}; valid)
A bracket procedure may return a bracket wider than promised with probability delta' (section
11.18), so both are runs of the schedule.

Part 1 (arrays; small sizes): C_2 computed point by point from the display of Theorem 11.84, with
        reduced K and enlarged eta' (as in the reviewer's harness) so that N_2 < M_max.
Part 2 (closed form): when all stored brackets are equal to [Lb, Ub],
        N_L(j, M) = M [Lb > s_j],  lambda_j = max{l_0, c_eta/(1+eta) e^{-b} max{s_i' : i' < j, s_i' < Lb}},
        |C_2| = min(M_max, floor(max{Mhat_j : s_j < Ub, s_j >= Lb e^b}))  -- checked against Part 1 --
        evaluated with the UNREDUCED constants of the theorem (K with L+3 in its logarithm,
        eta' = 1) at sizes where N_2 < M_max.
"""
import math
import sys
import numpy as np
from math import comb


def constants(u, n_o, n_i, lam, eta, etap, theta, nu1, L, delta, b, K_override=None):
    n = n_o + n_i
    m = n_o
    c_eta = (1 - eta) / (1 + eta)
    binom = [comb(m, j) for j in range(m + 1)]
    ball = np.cumsum(binom).astype(float)                      # |B(m, r)|
    E = [sum(binom[j] * (math.exp(u * (r + 1 - j)) - 1.0) for j in range(r + 1)) for r in range(m + 1)]
    T = [sum(binom[j] * math.exp(-u * max(j - k, 0)) for j in range(m + 1)) for k in range(m + 1)]
    Gt = [math.exp(u) - 1.0] + [E[r] / ball[r - 1] for r in range(1, m + 1)]

    def kappa(r):
        bound = max(1.0, c_eta * (ball[r - 1] if r >= 1 else 0.0))
        return max(k for k in range(m + 1) if ball[k] <= bound * (1 + 1e-12))

    G2 = [E[r] / T[kappa(r)] for r in range(m + 1)]
    J = math.ceil((2 * u * n + b + n_o * math.log(2)) / lam)
    nu0 = max((J + 1) * (math.exp(lam) - 1) / etap, nu1) / (1 - eta)
    rdag = -1
    for r in range(m):
        if Gt[r] <= theta * (1 - eta) * nu0 and min(Gt[r] / c_eta, G2[r]) <= theta:
            rdag = r
        else:
            break
    pidag = ball[rdag] / 2.0 ** m if rdag >= 0 else 2.0 ** (-m - 1)
    m_max = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * nu0 / ((1 - eta) * pidag)))
    K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * (J + 1) * (m_max + 1) * (L + 3) / delta))
    if K_override is not None:
        K = K_override
    nu = K * nu0
    return dict(u=u, n=n, n_i=n_i, lam=lam, eta=eta, b=b, c_eta=c_eta, J=J, nu0=nu0, rdag=rdag, pidag=pidag,
                m_max=m_max, K=K, nu=nu, M_max=K * 2 ** m_max)


def N_bound(c, x_prev):
    return c["K"] + (c["J"] + 1) * max(c["K"], 4 * (1 + c["eta"]) / c["c_eta"] * math.exp(c["lam"]) * c["nu"]
                                       * math.exp(x_prev))


def levels(c):
    return np.exp(-c["u"] * c["n"] + c["lam"] * np.arange(c["J"] + 1))             # s_j, psi_0 = 0


def candidate_set_2_arrays(c, Lb, Ub):
    """C_2 = {i <= M_max : exists j <= J, i <= Mhat_j, U_i > s_j, L_i <= s_j e^{-b}}  (C_1 = everything),
    lambda_j, Mhat_j as displayed in Theorem 11.84."""
    J, K, nu, c_eta, M_max, eta, b = c["J"], c["K"], c["nu"], c["c_eta"], c["M_max"], c["eta"], c["b"]
    s = levels(c)
    ell0 = ((1 + math.exp(-c["u"])) / 2.0) ** c["n"]
    sizes = np.array([K * 2 ** mm for mm in range(c["m_max"] + 1)])
    jl = np.searchsorted(s, Lb, side="left")                      # L_i > s_j  <=>  j < jl[i]
    NL = np.zeros((J + 1, len(sizes)))
    for mi, M in enumerate(sizes):
        h = np.bincount(np.minimum(jl[:M], J + 1), minlength=J + 2)
        NL[:, mi] = np.cumsum(h[::-1])[::-1][1:J + 2]
    best = 0.0
    member = np.zeros(M_max, dtype=bool)
    idx = np.arange(1, M_max + 1)
    for j in range(J + 1):
        lam_j = max(ell0, c_eta / (1 + eta) * math.exp(-b) * best)
        Mhat = max(K, 2 * nu * s[j] / (lam_j * math.exp(b)))
        member |= (idx <= Mhat) & (Ub > s[j]) & (Lb <= s[j] * math.exp(-b))
        ok = NL[j] >= K
        if ok.any():
            best = max(best, float(np.max(s[j] * NL[j][ok] / sizes[ok])))
    return int(member.sum())


def candidate_set_2_closed(c, Lb, Ub):
    """the same when every stored bracket equals [Lb, Ub] (two numbers)."""
    J, K, nu, c_eta, M_max, eta, b = c["J"], c["K"], c["nu"], c["c_eta"], c["M_max"], c["eta"], c["b"]
    s = levels(c)
    ell0 = ((1 + math.exp(-c["u"])) / 2.0) ** c["n"]
    best = 0.0
    top = 0.0
    for j in range(J + 1):
        lam_j = max(ell0, c_eta / (1 + eta) * math.exp(-b) * best)
        Mhat = max(K, 2 * nu * s[j] / (lam_j * math.exp(b)))
        if Ub > s[j] and Lb <= s[j] * math.exp(-b):
            top = max(top, Mhat)
        if Lb > s[j]:
            best = max(best, s[j])
    return int(min(M_max, math.floor(top)))


def no_tie(c, lb, ub):
    """no bracket end (and no L e^b) lies on the level grid: the comparisons are not decided by rounding"""
    g = (np.log(np.array([lb, ub, lb * math.exp(c["b"])]))[:, None] + c["u"] * c["n"]) / c["lam"]
    return bool(np.all(np.abs(g - np.round(g)) > 1e-6))


def brackets(c, x1, kind):
    triv = (math.exp(-c["u"] * c["n_i"]), math.exp(c["u"] * c["n_i"]))
    if kind == "wide":
        return triv
    alpha = kind
    return max(triv[0], math.exp(-alpha * x1)), min(triv[1], math.exp((1 - alpha) * x1))


def main():
    lam, eta, theta, nu1, delta, L = 1 / math.sqrt(2), 0.5, 3.0, 1.0, 0.05, 2   # irrational ratio: no ties
    print("# Part 1: arrays, reduced K = 6 and eta' = 100 (the reviewer's reduction), u = 1, lambda = 1/sqrt(2), eta = 1/2,")
    print("#         theta = 3; flat instance; x_2 = b = x_1/2")
    print("# n_o n_i  x_1     M_max      N_2   |C_2| honest (alpha = 0, 1/2, 1)   |C_2| all wide   violated   closed form agrees")
    viol1 = 0
    for (n_o, n_i, x1) in [(10, 4, 1.0), (11, 4, 1.5), (10, 5, 0.8), (11, 3, 2.0), (10, 6, 1.2)]:
        c = constants(1.0, n_o, n_i, lam, eta, 100.0, theta, nu1, L, delta, 0.5 * x1, K_override=6)
        N2 = N_bound(c, x1)
        res, agree = [], True
        for kind in (0.0, 0.5, 1.0, "wide"):
            lb, ub = brackets(c, x1, kind)
            assert no_tie(c, lb, ub)
            n_arr = candidate_set_2_arrays(c, np.full(c["M_max"], lb), np.full(c["M_max"], ub))
            agree &= (n_arr == candidate_set_2_closed(c, lb, ub))
            res.append(n_arr)
        viol1 += res[3] > N2
        print(f"  {n_o}  {n_i}   {x1:.1f}  {c['M_max']:8d}  {int(N2):8d}   {res[:3]}   {res[3]:10d}   {res[3] > N2}   {agree}")
        assert max(res[:3]) <= N2 and agree
    print(f"# Part 1: |C_2| > N_2 with trivial rung-1 brackets in {viol1} of 5 rows; never with honest brackets")
    print("#")
    print("# Part 2: closed form, UNREDUCED constants of the theorem (eta' = 1, K with L+3), lambda = 1/sqrt(2), eta = 1/2,")
    print("#         theta = 3 (u = 1), 50 (u = 2, 3), nu_1 = 1, delta = 0.05; flat instance; x_2 = b = x_1/2")
    print("# u  n_o n_i  x_1     K   r_dag        M_max          N_2   |C_2| honest (alpha = 0, 1/2, 1)       |C_2| all wide   violated")
    viol2 = rows2 = 0
    for (u, n_o, n_i, x1) in [(1.0, 8, 6, 1.5), (1.0, 60, 20, 1.0), (1.0, 100, 40, 2.0), (1.0, 200, 160, 5.0),
                              (2.0, 30, 10, 1.0), (2.0, 60, 30, 3.0), (3.0, 20, 8, 1.0), (3.0, 40, 20, 4.0)]:
        c = constants(u, n_o, n_i, lam, eta, 1.0, theta if u == 1.0 else 50.0, nu1, L, delta, 0.5 * x1)
        N2 = N_bound(c, x1)
        assert all(no_tie(c, *brackets(c, x1, kind)) for kind in (0.0, 0.5, 1.0, "wide"))
        res = [candidate_set_2_closed(c, *brackets(c, x1, kind)) for kind in (0.0, 0.5, 1.0, "wide")]
        rows2 += 1
        viol2 += res[3] > N2
        print(f"  {u:.0f}  {n_o:3d} {n_i:3d}  {x1:.1f}  {c['K']:4d}  {c['rdag']:3d}  {c['M_max']:.4e}  {N2:.4e}   "
              f"{[f'{r:.3e}' for r in res[:3]]}   {res[3]:.4e}   {res[3] > N2}"
              + ("" if c["M_max"] > N2 else "   (N_2 >= M_max: Claim B is vacuous here)"))
        assert max(res[:3]) <= N2
        sys.stdout.flush()
    print(f"# Part 2: |C_2| > N_2 with trivial rung-1 brackets in {viol2} of {rows2} rows (every row with N_2 < M_max);")
    print("#         never with honest brackets of ratio e^{x_1}.")
    print("# With the rule 'before stage 2: if |C_2| > N_2, stop and return the trivial bracket' stage 2 never runs")
    print("# on more than N_2 fibres, and with honest rung-1 brackets the rule fires in no row above.")


if __name__ == "__main__":
    main()
