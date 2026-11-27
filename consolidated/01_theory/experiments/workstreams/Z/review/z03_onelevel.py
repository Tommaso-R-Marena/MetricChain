#!/usr/bin/env python3
"""z03: (iii) of the brief -- Lemma Z2 and Proposition Z3 against an exact one-level evaluator, at parameters other than
the coordinator's (experiments/workstreams/Z/z1_onelevel.py: u = 1, N = d in {300, ..., 10^4}, delta = 0.05, E = 0, j <= 11).

Exact evaluator: the one of the referee of Q2 (Q2/review/rlib.py; tables of the outer cube, r_dagger, pi_dagger, the
constants of Theorem 11.56) -- independent of q2lib/qlib/r12lib.  Chain (W_j, b_j): own code (zrev.py).

For each case (u, horizon N, dimension d <= N, chain level j, delta, target accuracy xhat >= X = X_0(N) + 1, inner error
function E): the inner family saturates the type H^infty(grid of W_j at horizon N; E).  Checked:

 (A) the accuracy of the level L(d; n_o, y/n_o) is at most xhat                                     [every level evaluated]
 (B) (U-infinity): ln C_max <= max_lines [n_i B + (1 - sigma) n_o theta_na(e)] + ell_0(d, Lam) + E(d, 1; Lam + q(d, Lam)),
     and ln(1/delta') + n_i ln 2 <= Lam + q(d, Lam),   Lam = ln(1/delta) + d ln 2                    [every level evaluated]
 (C) min_{n_o} Pi_j(n_o) <= d max_{grid of W_{j+1}} [B - W_{j+1}(B) g] + d/N + 1 + a d_min           [all admissible n_o]
 (D) the type of Proposition Z3 at the n_o of the design (the minimiser of Pi_j):
     ln C_max <= max_{grid of W_{j+1}} [d B - sigma xhat] + E(d, 1; Lam + q) + ell_0 + X_0(d) + d_min ln 2 + 2
 Levels evaluated per case: the design's n_o, n_o = 1, 2, the largest admissible one, and a few random ones.
Controls (must fail somewhere): (D) without ell_0 and X_0(d); (C) with the curve W_{j+2}; (A) with the target lowered by 1.3.
Usage: python3 z03_onelevel.py u [seconds] [seed] [s_t - L] [b_0 - h]
"""
import math
import random
import sys
import time

import numpy as np

sys.dont_write_bytecode = True
import zrev
import zlev

RL = zlev.RL
u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
TMAX = float(sys.argv[2]) if len(sys.argv) > 2 else 200.0
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
random.seed(seed)
PAR = {0.5: (0.05, 0.0008), 1.0: (0.05, 0.003), 2.0: (0.05, 0.01), 0.25: (0.05, 0.00015), 4.0: (0.04, 0.02)}
dst, eps1 = PAR[u]
if len(sys.argv) > 5:
    dst, eps1 = float(sys.argv[4]), float(sys.argv[5])          # another chain: cut level L + dst, restart height h + eps1
JMAX = 22
cu = zrev.Cube(u)
rc = RL.Cube(u)
assert abs(rc.a - cu.a) < 1e-13 and abs(rc.h - cu.h) < 1e-13
C = zrev.Chain(cu, dst, eps1, JMAX + 2)
dm = zlev.dmin(u)
a, h = cu.a, cu.h
print("# cube u = %g: h = %.6f, a = %.6f, d_min = %d;  chain: s_t = L + %g, b_0 = h + %g; range condition to level %d: %s (largest W_j(b_j) = %.3f)"
      % (u, h, a, dm, dst, eps1, JMAX + 2, C.range_ok, max(C.Wtop)))
print("# (b_j - h)/h at j = 0, 5, 10, 20: %s" % " ".join("%.4f" % ((C.b[j] - h) / h) for j in (0, 5, 10, 20)))
assert C.range_ok

EFUNS = {"0": None, "3sqrt(d)": lambda d, x, Lam: 3 * math.sqrt(d), "Lam/7": lambda d, x, Lam: Lam / 7.0,
         "5/x+lnLam": lambda d, x, Lam: 5.0 / x + math.log(Lam)}
viol = dict(A=0, B=0, Bq=0, C=0, D=0)
worst = dict(A=-1e18, B=-1e18, Bq=-1e18, C=-1e18, D=-1e18)
where = {}
ctrl = dict(D_noX0=0, D_twolevels=0, A_theta=0)
nlev = ncase = 0
gave = 0.0
_grid = {}


def grid(j, N):
    key = (j, N)
    if key not in _grid:
        if len(_grid) > 40:
            _grid.clear()
        Bs, Ws = C.grid(j, N)
        _grid[key] = zlev.Lines(Bs, np.minimum(Ws, 1.0))
    return _grid[key]


t0 = time.time()
rows = []
while time.time() - t0 < TMAX:
    # ---- a random case
    kind = random.random()
    if kind < 0.30:
        d = dm + random.randint(1, 40)                      # dimensions near d_min
    elif kind < 0.65:
        d = random.choice([60, 100, 200, 300, 500, 800, 1300])
    else:
        d = random.choice([2000, 3000, 5000, 8000, 12000, 20000])
    N = d * random.choice([1, 1, 1, 2, 3, 10]) if d <= 3000 else d * random.choice([1, 1, 2])
    j = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 9, 12, 15, 18, 20])
    ld = random.choice([math.log(0.5), math.log(0.05), math.log(1e-3), math.log(1e-12), -float(d), -30.0 * d])
    ename = random.choice(list(EFUNS))
    Ef = EFUNS[ename]
    X0d = zlev.X0(u, d)
    calX = zlev.X0(u, N) + 1
    r = random.random()
    if r < 0.2:
        xh = calX
    elif r < 0.4:
        xh = calX + random.choice([1e-9, 0.37, 2.0, 7.3])
    elif r < 0.8:
        xh = calX + random.random() ** 2 * 1.2 * u * d
    else:
        xh = calX + random.choice([2 * u * d, 10.0 * d, cu.eps_star * d, h * d, 0.5 * h * d])
    y = xh - X0d
    g = y / d
    lines = grid(j, N)
    nxt = grid(j + 1, N)
    nxt2 = grid(j + 2, N)
    inner = zlev.Sat(lines, Ef, xmin=1.0)
    Lam = -ld + d * zlev.LN2
    qq = zlev.q(u, d, Lam)
    l0 = zlev.ell0(u, d, Lam)
    E1v = inner.E(d, 1.0, Lam + qq)
    nos, Pi = zlev.proxy_all(cu, d, y, lines)
    kbest = int(np.argmin(Pi))
    n_star = int(nos[kbest])
    # (C)
    M1 = d * float(nxt.env([g])[0])
    M2 = d * float(nxt2.env([g])[0])
    exC = Pi[kbest] - (M1 + d / N + 1 + a * dm)
    if exC > worst["C"]:
        worst["C"], where["C"] = exC, (d, N, j, xh)
    viol["C"] += exC > 1e-9
    if Pi[kbest] - (M2 + d / N + 1 + a * dm) > 1e-9:
        ctrl["D_twolevels"] += 1
    ncase += 1
    cand = {n_star, 1, min(2, len(nos)), int(nos[-1])}
    for _ in range(3):
        cand.add(random.randint(1, int(nos[-1])))
    lC_star = None
    for n_o in sorted(cand):
        res = zlev.level_Z2(cu, d, n_o, y, ld, inner.cost)
        nlev += 1
        exA = res['xout'] - xh
        if exA > worst["A"]:
            worst["A"], where["A"] = exA, (d, N, j, xh, n_o)
        viol["A"] += exA > 1e-9
        # control: the accuracy accounting has no more than about one nat to spare (a target lower by 1.3 is missed somewhere)
        if res['xout'] > xh - 1.3:
            ctrl["A_theta"] += 1
        main = float(Pi[n_o - 1])
        exB = res['lC'] - (main + l0 + E1v)
        if exB > worst["B"]:
            worst["B"], where["B"] = exB, (d, N, j, xh, n_o, ld, ename)
        viol["B"] += exB > 1e-9
        exq = (-res['ldp'] + (d - n_o) * zlev.LN2) - (Lam + qq)
        worst["Bq"] = max(worst["Bq"], exq)
        viol["Bq"] += exq > 1e-9
        if n_o == n_star:
            lC_star = res['lC']
    typ = float(nxt.major(d, [xh])[0])
    typ2 = float(nxt2.major(d, [xh])[0])
    Eplus = E1v + l0 + X0d + dm * zlev.LN2 + 2
    exD = lC_star - (typ + Eplus)
    if exD > worst["D"]:
        worst["D"], where["D"] = exD, (d, N, j, xh, n_star, ld, ename)
    viol["D"] += exD > 1e-9
    if lC_star - (typ + E1v + dm * zlev.LN2 + 2) > 1e-9:
        ctrl["D_noX0"] += 1
    if len(rows) < 14 and random.random() < 0.02:
        rows.append((d, N, j, xh, n_star, lC_star, typ, lC_star - typ - E1v, X0d + l0 + dm * zlev.LN2 + 2, ename))
print("# %d cases, %d levels evaluated exactly  [%.0f s]" % (ncase, nlev, time.time() - t0))
print("#      d       N   j        xhat    n_o*   ln C_max   type(j+1)   excess-E   allowed   E")
for r in rows:
    print("  %6d  %6d  %2d  %10.1f  %6d  %9.2f  %9.2f  %8.2f  %8.2f   %s" % r)
print("violations: (A) accuracy %d, (B) (U-infinity) %d, (B') delta' bookkeeping %d, (C) exponent %d, (D) the type %d   [each must be 0]"
      % (viol["A"], viol["B"], viol["Bq"], viol["C"], viol["D"]))
print("largest excess (negative = slack): (A) %.4f, (B) %.3f, (B') %.3f, (C) %.4f, (D) %.3f" % (worst["A"], worst["B"], worst["Bq"], worst["C"], worst["D"]))
for k in "ABCD":
    print("   worst case of (%s): %s" % (k, where.get(k)))
print("controls: (D) without ell_0 and X_0(d) fails in %d cases; (C) with W_{j+2} fails in %d cases; accuracy against a target lowered by 1.3 fails in %d levels   [each must be > 0]"
      % (ctrl["D_noX0"], ctrl["D_twolevels"], ctrl["A_theta"]))
ok = all(v == 0 for v in viol.values()) and all(v > 0 for v in ctrl.values())
print("ALL CHECKS PASS" if ok else "A CHECK FAILED")
