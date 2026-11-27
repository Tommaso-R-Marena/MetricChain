#!/usr/bin/env python3
"""r29_i35_onelevel.py [u] [sizes ...]  --  one level of Lemma Z2 / Proposition Z3 evaluated exactly with MY evaluator
(r29level.py, written from the statement of Theorem 11.56), over inner families that SATURATE their type, "line by line".

Part 1 (replication against their evaluators).  The same levels with their Q2.level_U (qlib + r12lib, imported from the
read-only export): ln C_max, the accuracy and ln delta' must agree.
Part 2 (the claims, with my evaluator).  For a family (W, b), its envelope step (W', b') (my own, r29fam.Fam), the grid
families with spacing 1/N (N = d), target accuracies x-hat >= X_0(d) + 1, y = x-hat - X_0(d), g = y/d, and every
admissible outer block n_o (a stride at large d):
  (A) accuracy of the level <= x-hat;
  (B) (U-infinity):  ln C_max(n_o) <= max_lines [n_i B + (1 - sigma) n_o theta_na(y/n_o)] + ell_0(d, Lambda)   (E = 0);
  (C) min_{n_o} max_lines [n_i B + (1 - sigma) n_o theta_na(y/n_o)] <= d M_{W',b'}(g) + 1 + a d_min  (+ stride a);
  (D) the type: ln C_max at the proxy block <= max_{grid of W'} [d B - sigma x-hat] + X_0(d) + d_min ln 2 + 2 + ell_0.
Families: my envelope curves W_0, W_1, W_2, W_3, W_5; and families chosen to break the step: the chord (slope at the
cap at the top), zero-then-one-line-to-the-cap, two lines, two lines crossing at the top, flat families with low tops.
Controls (must fail): (D) without its losses; (C) with the second envelope step W'' in place of W';
(C) for families that are NOT convex (the line-by-line value of a non-convex family in place of M_{W',b'}).
"""
import math
import os
import sys
import time

import numpy as np

import r29lib as R
import r29env as E
import r29fam as FM
import r29level as LV

R.cap_memory()
u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
SIZES = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else [300, 1000, 3000]
P = E.CubeF(u)
FM.setup(P)
a, h, es = P.a, P.h, P.estar
dm = LV.dmin(u)
ld = math.log(0.05)
t0 = time.time()

# ------------------------------------------------------------------------------------------------ families
env = E.EnvSA(P, 8)


def env_fam(j):
    if j == 0:
        return FM.Fam([0.0, env.b[0]], [0.0, 0.0], "envelope W_0")
    xs = np.unique(np.concatenate([np.linspace(0, env.Bt[j], 1200), [env.b[j]]]))
    return FM.Fam(xs, np.clip([float(env.W(j, float(x))) for x in xs], 0, 1), "envelope W_%d" % j)


fams = [env_fam(j) for j in (0, 1, 2, 3, 5)]
for b in (a, 0.6 * a, 1.2 * h):
    fams.append(FM.Fam([0.0, b], [0.0, 1.0], "chord to the cap, b = %.3f a" % (b / a)))
    fams.append(FM.Fam([0.0, 0.6 * b, b], [0.0, 0.0, 1.0], "zero, then one line to the cap, b = %.3f a" % (b / a)))
    fams.append(FM.Fam([0.0, 0.5 * b, b], [0.0, 0.1, 0.7], "two lines, b = %.3f a" % (b / a)))
    fams.append(FM.Fam([0.0, 0.999999 * b, b], [0.0, 0.3 * 0.999999, 0.3], "two lines crossing at the top, b = %.3f a" % (b / a)))
fams.append(FM.Fam([0.0, 1.05 * h], [0.0, 0.0], "flat, b = 1.05 h"))
nexts = [F.envelope_step(n=1500) for F in fams]
nexts2 = [F.envelope_step(n=800) for F in nexts]


def grid_lines(F, N):
    Bs = [i / N for i in range(int(math.floor(N * F.b + 1e-12)) + 1)]
    if Bs[-1] < F.b:
        Bs.append(F.b)
    return [(B, min(1.0, max(0.0, F.W(B)))) for B in Bs]


def accuracies(d):
    X0 = LV.X0(u, d)
    return [X0 + 1, X0 + 3, X0 + 10, X0 + 0.01 * d, X0 + 0.1 * d, X0 + 0.3 * d, X0 + u * d]


def blocks(d):
    stride = max(1, (d - dm) // 300)
    return sorted(set(list(range(1, d - dm + 2, stride)) + [1, 2, 3, d - dm + 1])), stride


# ------------------------------------------------------------------------------------------------ part 1
Z = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_07cde81/experiments/workstreams/Z"
sys.path.insert(0, Z)
sys.dont_write_bytecode = True
import zetalib as ZL  # noqa: E402  (theirs; read-only, in place)

Q2 = ZL.Q2
ev = Q2.Ev(u, both=True)
n1 = 0
w1 = 0.0
const_diff = 0
for d in [s for s in SIZES if s <= 1000]:
    for F in fams[:4]:
        lines = grid_lines(F, d)
        inner = Q2.SatLines(lines)
        for xh in accuracies(d):
            y = xh - LV.X0(u, d)
            for n_o in blocks(d)[0][::7]:
                mine = LV.level_Z2(u, d, n_o, y, P.theta, lines, ld)
                lth = math.log(3.0 * (n_o + 1)) + 2 * u + math.exp(u) + y
                r = Q2.level_U(ev, d, n_o, lth, n_o * mine["th"], ld, inner)
                c = r["c"]
                w1 = max(w1, abs(mine["lC"] - r["lC"]), abs(mine["xout"] - c["xout"]), abs(mine["ldeltap"] - c["ldeltap"]))
                if not (mine["J"] == c["J"] and mine["K"] == c["K"] and mine["rdag"] == c["rdag"] and mine["m_max"] == c["m_max"]):
                    const_diff += 1
                n1 += 1
print("# one level exactly, cube u = %g, sizes %s" % (u, SIZES))
print("Part 1: %d levels by my evaluator and by theirs (qlib + r12lib): largest difference of ln C_max, accuracy, ln delta' = %.2e;" % (n1, w1))
print("        levels on which an integer constant (J, K, r_dagger, m_max) differs: %d;  their two evaluators differ by at most %.1e" % (const_diff, ev.maxdiff), flush=True)

# ------------------------------------------------------------------------------------------------ part 2
viol = {k: 0 for k in "ABCD"}
slack = {k: math.inf for k in "BCD"}
ctrl = {"D_no_losses": 0, "C_two_steps": 0}
nlev = ncase = 0
worst_rows = []
for d in SIZES:
    N = d
    X0 = LV.X0(u, d)
    Lam = -ld + d * math.log(2)
    ell0 = LV.ell0(u, d, Lam)
    bl, stride = blocks(d)
    for F, Fn, Fnn in zip(fams, nexts, nexts2):
        lines = grid_lines(F, N)
        nxt = grid_lines(Fn, N)
        for xh in accuracies(d):
            y = xh - X0
            g = y / d
            best_main, lC_at_proxy, best_no = math.inf, None, None
            for n_o in bl:
                r = LV.level_Z2(u, d, n_o, y, P.theta, lines, ld)
                nlev += 1
                if r["xout"] > xh + 1e-9:
                    viol["A"] += 1
                sB = r["main"] + ell0 - r["lC"]
                slack["B"] = min(slack["B"], sB)
                if sB < -1e-9:
                    viol["B"] += 1
                if r["main"] < best_main:
                    best_main, lC_at_proxy, best_no = r["main"], r["lC"], n_o
            ncase += 1
            M1 = d * Fn.M(g)
            M2 = d * Fnn.M(g)
            sC = M1 + 1 + a * dm + stride * a - best_main
            slack["C"] = min(slack["C"], sC)
            if sC < -1e-6:
                viol["C"] += 1
                worst_rows.append(("C", d, F.name, xh, best_no, best_main, M1))
            if best_main - (M2 + 1 + a * dm + stride * a) > 1e-9:
                ctrl["C_two_steps"] += 1
            typ = max(d * B - s * xh for (B, s) in nxt)
            sD = typ + X0 + dm * math.log(2) + 2 + ell0 + stride * a - lC_at_proxy
            slack["D"] = min(slack["D"], sD)
            if sD < -1e-9:
                viol["D"] += 1
                worst_rows.append(("D", d, F.name, xh, best_no, lC_at_proxy, typ))
            if lC_at_proxy - typ > 1e-9:
                ctrl["D_no_losses"] += 1
    print("        d = %d done (%d levels so far, %.0f s)" % (d, nlev, time.time() - t0), flush=True)
print("Part 2: %d families x %d accuracies x sizes = %d cases, %d levels evaluated exactly with my evaluator" % (len(fams), 7, ncase, nlev))
print("        violations: (A) accuracy %d, (B) (U-infinity) %d, (C) exponent step %d, (D) the type %d   [each must be 0]" % (viol["A"], viol["B"], viol["C"], viol["D"]))
print("        least slack in nats: (B) %.3f, (C) %.3f, (D) %.3f" % (slack["B"], slack["C"], slack["D"]))
for r_ in worst_rows[:6]:
    print("        VIOLATION %s: d = %d, %s, x-hat = %.2f, n_o = %s: %.4f against %.4f" % r_)
print("        controls: (D) without its losses fails in %d cases; (C) with the second envelope step fails in %d cases   [each must be > 0]" % (ctrl["D_no_losses"], ctrl["C_two_steps"]))

# control: non-convex families -- the line-by-line value of the family itself in place of the next majorant
rng = np.random.default_rng(29)
nc = failc = 0
d = SIZES[0]
X0 = LV.X0(u, d)
bl, stride = blocks(d)
for _ in range(12):
    b = h + (a - h) * rng.random()
    x1 = b * (0.2 + 0.5 * rng.random())
    w1_ = 0.3 + 0.6 * rng.random()
    Fnc = FM.Fam([0.0, x1, b], [0.0, w1_, w1_ + (1 - w1_) * 0.3 * rng.random()], "non-convex")
    lines = grid_lines(Fnc, d)
    for xh in (X0 + 0.01 * d, X0 + 0.1 * d):
        y = xh - X0
        g = y / d
        best_main = min(LV.level_Z2(u, d, n_o, y, P.theta, lines, ld)["main"] for n_o in bl)
        # line-by-line value of the non-convex family on a dense grid
        bp = Fnc.bplus()
        lbl = max([0.0] + [float(B) - Fnc.H(float(B)) * g for B in np.linspace(0, bp * (1 - 1e-12), 2001) if Fnc.H(float(B)) < math.inf])
        nc += 1
        if best_main > d * lbl + 1 + a * dm + stride * a:
            failc += 1
print("        control (families that are NOT convex, d = %d): the claim (C) with the line-by-line value fails in %d of %d cases   [must be > 0]" % (d, failc, nc))
ok = (all(v == 0 for v in viol.values()) and all(v > 0 for v in ctrl.values()) and failc > 0 and w1 < 1e-8 and const_diff == 0)
print("ONELEVEL: %s" % ("no violation; all controls fail as they must" if ok else "CHECK FAILED"))
R.finish("r29_i35_onelevel u=%g sizes=%s" % (u, SIZES))
