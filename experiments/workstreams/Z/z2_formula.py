#!/usr/bin/env python3
"""Z2: the bound of Theorem Z (docs/workstreams/Z_REPORT.md, section 6) as a formula, in numbers.

    ln N(n; eps, delta)  <=  n b_k + E_Z(n, k),      E_Z unrolled from the top as in section 6:
    k times [ chain (A_T + X + 1), level (ell_0 + X_0 + d_min ln 2 + 2) ], then the base family of Theorem A of Q2
    with M_1 epochs (B_{M_1} <= b_0).

b_j: the chain of cut orbit curves of the cube (zetalib.ChainZ; s_t = L + 0.05, b_0 = h + eps1) for j <= JEXACT;
beyond, b_j - h = rho * c_*^2 / j^2 with rho the last computed value of j^2 (b_j - h)/c_*^2  [an extrapolation:
the proof gives the limit rho -> 1, not this value].  The range condition of the chain is checked for the levels
computed; that it holds for ALL levels at this eps1 is numerical evidence, not a proof (Lemma RC of R_REPORT
gives some eps1 > 0).  So this table is an illustration of the order of magnitude, labelled [N].

Compared with:  Theorem A/B of Q2  (min over M of n B_M + E_new)  and Theorem 11.58a (min over M of n B_M + E_old),
the non-adaptive n a, and the hinted lower bound n h.
Usage: python3 z2_formula.py [u] [eps1]        (default 1.0 0.003)
"""
import math
import sys

import zetalib as Z

Q2 = Z.Q2
Q = Q2.Q
LN2 = math.log(2.0)
u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
eps1 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.003
JEXACT = 160
C = Z.ChainZ(u, 0.05, eps1, JEXACT)
cu = Q.Cube(u)
h, a = C.h, C.a
cstar2 = C.P.const
rho = JEXACT ** 2 * (C.b[JEXACT] - h) / cstar2
dm = Z.dmin(u)
assert abs(cu.h - h) < 1e-9 and abs(cu.a - a) < 1e-12


def b_of(j):
    return C.b[j] if j <= JEXACT else h + rho * cstar2 / j ** 2


seq = Q.epoch_seq(cu, 70)
M1 = next(m for m in range(60) if seq['B'][m] <= C.b0)
kM1 = seq['k'][M1] if 'k' in seq else None
print("# cube u = %g: h = %.6f, a = %.6f, c_*^2 = %.6f;  chain: s_t = L + 0.05, b_0 = h + %g = h (1 + %.3f); range condition to level %d: %s"
      % (u, h, a, cstar2, eps1, eps1 / h, JEXACT, C.range_ok))
print("# j^2 (b_j - h)/c_*^2 at j = 10, 20, 40, 80, 160: %s   (extrapolation beyond 160 with rho = %.4f)"
      % (" ".join("%.4f" % (j * j * (C.b[j] - h) / cstar2) for j in (10, 20, 40, 80, 160)), rho))
print("# base: Theorem A of Q2 with M_1 = %d epochs (B_{M_1} = h (1 + %.4f) <= b_0), k_{M_1} = %s levels" % (M1, seq['B'][M1] / h - 1, kM1))


def E_Z(n, eps, dln, k, detail=False):
    eh = min(eps, 1.0)
    Lam = dln + n * LN2
    X0n = Z.X0(u, n)
    calX = X0n + 1
    tot_chain = tot_level = 0.0
    for j in range(k, 0, -1):
        alpha = eh if j == k else 1.0
        Bp = b_of(j)
        m = Q2.Chain.design_m(cu, n, Bp, calX, alpha, Lam)
        ch = Q2.Chain(cu, n, Bp, calX, alpha, m)
        Ls = ch.Lam_sharp(n, Lam)
        tot_chain += ch.A_T(n, Ls) + ch.j(n) * ch.Delta_T(n, Ls) + calX + 1
        Lam = Ls
        tot_level += Q2.ell0(cu, n, Lam) + X0n + dm * LN2 + 2
        Lam += Q2.qSb(cu, n, Lam)
    base = Q2.E_new(cu, n, 1.0, Lam - n * LN2, M1, seq) if k >= 1 else Q2.E_new(cu, n, eps, dln, M1, seq)
    if detail:
        return tot_chain, tot_level, base, Lam
    return tot_chain + tot_level + base


def best(f, lo, hi):
    """minimise an (essentially unimodal, flat near its minimum) integer function on a geometric grid of ratio 1.08"""
    cand, k = [], float(lo)
    while k <= hi:
        cand.append(int(round(k)))
        k = max(k * 1.08, k + 1)
    return min((f(k), k) for k in sorted(set(cand)))


def best_M(f, M0):
    """the number of epochs: n (B_M - h) decreases and the error increases with M; stop after three increases"""
    bestv, bestM, up = math.inf, None, 0
    for M in range(M0, MMAX):
        v = f(M)
        if v < bestv:
            bestv, bestM, up = v, M, 0
        else:
            up += 1
            if up >= 3:
                break
    return bestv, bestM


MMAX = len(seq['B']) - 1
dln = math.log(1 / 0.05)
eps = 1.0
print("# delta = 0.05, eps = 1.  All entries are ln(evaluations) minus n h, in nats; 'n(a-h)' is where the non-adaptive bound stands.")
print("#        n    n(a-h)   | Thm 11.58a (Q)        | Theorem A of Q2       | Theorem Z: total      k   n beta_k    chains    levels     base  per level/ln n")
for ex in (5, 6, 7, 8, 9, 10, 12, 15):
    n = 10 ** ex
    vo, Mo = best_M(lambda M: n * (seq['B'][M] - h) + Q2.E_old(cu, n, eps, dln, M, seq), 1)
    vn, Mn = best_M(lambda M: n * (seq['B'][M] - h) + Q2.E_new(cu, n, eps, dln, M, seq), 0)
    kmax = int(min(n ** 0.5, 12000))
    vz, kz = best(lambda k: n * (b_of(k) - h) + E_Z(n, eps, dln, k), 1, kmax)
    tc, tl, tb, Lam = E_Z(n, eps, dln, kz, detail=True)
    flag = "" if (Mo < MMAX - 1 and Mn < MMAX - 1 and kz < kmax) else "  (a search range was exhausted)"
    print("  10^%-3d  %9.3g   | %10.4g  (M = %2d)  | %10.4g  (M = %2d)  | %10.4g  %6d  %9.4g  %8.4g  %8.4g  %7.4g   %6.2f%s"
          % (ex, n * (a - h), vo, Mo, vn, Mn, vz, kz, n * (b_of(kz) - h), tc, tl, tb, (tc + tl) / kz / math.log(n), flag))
print("# limsup constant (3/2)(2 c_*^2)^{1/3} c_Z^{2/3} with c_Z = the last column at the largest n: %.2f   (Theorem B of Q2: C_*' sqrt(n ln n))"
      % (1.5 * (2 * cstar2) ** (1 / 3.0) * ((tc + tl) / kz / math.log(n)) ** (2 / 3.0)))
