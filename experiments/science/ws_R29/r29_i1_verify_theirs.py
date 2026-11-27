#!/usr/bin/env python3
"""r29_i1_verify_theirs.py u J K [script.py]  --  an independent exact verification of the sequence that
z6_certified_tops.py (the theory division's script, imported UNMODIFIED from the read-only export, or a copy given
as the fourth argument) actually builds.

How.  The module is imported without running its main().  Its own step() is called to produce the curves.  In
parallel a *shadow* of step() -- the same statements, calling the module's own next_top, best_rho, certified_pair,
down, upw and Curve -- records for every generated line the data its validity rests on: the rate rho, the pair
(e', th), the parent line.  The shadow curve must equal the module's curve bit for bit (else the run stops).  Then,
with code that shares nothing with theirs (r29lib: my integer interval arithmetic, my exact hull, my checker):
  (a) every pair is re-certified:  e' >= KL(rho||p_u)  and  th >= KL(rho||1/2)  against my rigorous enclosures;
  (b) every stored image line is compared EXACTLY with its image line:  alpha <= (1 + th a0)/e',  beta >= th (1 + b0)/e';
  (c) the parent is a stored line of the previous curve (or the zero line);
  (d) the cap line is below the maximum of two certified image lines that straddle its slope (a certificate that
      does not use their hull or their vertices);
  (e) their stored lines are exactly the upper hull of themselves (my hull routine) -- a test of their hull;
  (f) the top: c' = c or c' + ABAR V(c') >= ABAR exactly, with ABAR >= a by my enclosure of a;  V'(c') <= 1;
  (g) the tops against the semi-analytic envelope tops (necessary: c_j >= b_j) and against the committed output.
"""
import importlib.util
import math
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

import r29lib as R
import r29env as E

R.cap_memory()
R.DI.P = 160                                   # enclosures of width 1e-46: far finer than the doubles under test

EXPORT = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_07cde81/experiments/workstreams/Z"
u_str = sys.argv[1] if len(sys.argv) > 1 else "1"
JMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 6
K = int(sys.argv[3]) if len(sys.argv) > 3 else 400
script = sys.argv[4] if len(sys.argv) > 4 else os.path.join(EXPORT, "z6_certified_tops.py")


def load(path, argv):
    old = sys.argv
    sys.argv = argv
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("z6_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.argv = old
    return mod


z6 = load(script, [script, u_str, str(JMAX), str(K), "nocompare"])
ufr = Fr(u_str)
cube = R.CubeDI(ufr)
ABAR = Fr(z6.ABAR)
print("# independent verification of %s  (u = %s, J = %d, K = %d)" % (os.path.basename(script), u_str, JMAX, K))
print("# their ABAR = %.17g; my enclosure of a: [%.17g, %.17g]; ABAR >= a rigorously: %s;  ABAR - a <= %.2e (%.1f ulp)"
      % (z6.ABAR, float(cube.A.lo_fr()), float(cube.A.hi_fr()), ABAR >= cube.A.hi_fr(), float(ABAR - cube.A.lo_fr()),
         float(ABAR - cube.A.lo_fr()) / math.ulp(z6.ABAR)))


def shadow_step(V):
    """the statements of their step(), with a record per generated line"""
    c = z6.next_top(V)
    Bs = np.unique(np.concatenate([np.linspace(0.0, c, z6.K + 1)[1:], c * (1.0 - np.geomspace(1e-9, 0.25, z6.K // 4))]))
    s, idx = V.val(Bs)
    keep = s < 1.0
    Bs, s, idx = Bs[keep], s[keep], idx[keep]
    rho, Fv = z6.best_rho(Bs, s)
    good = (Fv > 0) & np.isfinite(Fv) & (Fv < 50.0)
    recs = []
    cache = {}
    for B_, r_, i_ in zip(Bs[good], rho[good], idx[good]):
        r_ = float(r_)
        if r_ not in cache:
            cache[r_] = z6.certified_pair(r_)
        e_, th_ = cache[r_]
        a0 = float(V.al[i_]) if i_ >= 0 else 0.0
        b0 = float(V.be[i_]) if i_ >= 0 else 0.0
        al = float(z6.down(np.float64((1.0 + th_ * a0) / e_)))
        be = float(z6.upw(np.float64(th_ * (1.0 + b0) / e_)))
        recs.append((al, be, r_, e_, th_, a0, b0))
    H = z6.Curve([r[0] for r in recs], [r[1] for r in recs], c)
    C = Fr(c)
    capline = None
    if len(H.al) and Fr(float(H.al[-1])) * C - Fr(float(H.be[-1])) > 1:
        vs = H.vertices()
        mstar = max((1 - Vx) / (C - X) for X, Vx in vs[:-1])
        m = float(mstar)
        while Fr(m) < mstar:
            m = math.nextafter(m, z6.INF)
        bL = float(Fr(m) * C - 1)
        while Fr(bL) < Fr(m) * C - 1:
            bL = math.nextafter(bL, z6.INF)
        kal = [float(a_) for a_, b_ in zip(H.al, H.be) if Fr(float(a_)) * C - Fr(float(b_)) <= 1]
        kbe = [float(b_) for a_, b_ in zip(H.al, H.be) if Fr(float(a_)) * C - Fr(float(b_)) <= 1]
        H = z6.Curve(kal + [m], kbe + [bL], c)
        capline = (m, bL)
    return H, recs, capline


def to_PL(V):
    return R.PL([(Fr(float(a_)), Fr(float(b_))) for a_, b_ in zip(V.al, V.be)], Fr(V.c))


def certificates(Vn_pl, recs, capline):
    """certificates for my checker from the shadow records"""
    img = {}
    for al, be, r_, e_, th_, a0, b0 in recs:
        key = (Fr(al), Fr(be))
        if key not in img:
            img[key] = ("img", (Fr(a0), Fr(b0)), Fr(r_), Fr(e_), Fr(th_))
    certs = {}
    capkey = (Fr(capline[0]), Fr(capline[1])) if capline else None
    for ln in Vn_pl.lines():
        if capline and ln == capkey and ln not in img:
            # witnesses: in MY hull of all image lines, the two neighbours whose slopes straddle the cap slope
            Hfull = R.PL(list(img.keys()), Vn_pl.c)
            hl = Hfull.hull
            j = 1
            while j + 1 < len(hl) and hl[j][0] < ln[0]:
                j += 1
            l1, l2 = (hl[j - 1][0], hl[j - 1][1]), (hl[j][0], hl[j][1])
            certs[ln] = ("cap", (l1, img.get(l1)), (l2, img.get(l2)))
        elif ln in img:
            certs[ln] = img[ln]
    return certs


def margins(recs):
    """smallest margins of the pairs and of the line rounding, in ulps of the stored doubles (>= 0 means valid)"""
    mE = mT = mA = mB = math.inf
    for al, be, r_, e_, th_, a0, b0 in recs:
        Eh, Th = cube.pair_enclosures(Fr(r_))
        mE = min(mE, float(Fr(e_) - Eh.hi_fr()) / math.ulp(e_))
        if th_ > 0:
            mT = min(mT, float(Fr(th_) - Th.hi_fr()) / math.ulp(th_))
        ia, ib = R.image_line((Fr(a0), Fr(b0)), Fr(e_), Fr(th_))
        mA = min(mA, float(ia - Fr(al)) / math.ulp(al))
        if be > 0 and ib > 0:
            mB = min(mB, float(Fr(be) - ib) / math.ulp(be))
    return mE, mT, mA, mB


J0 = int(os.environ.get("R29_J0", "1"))                   # chunked runs: levels J0 .. JMAX, state carried in npz files
if J0 > 1:
    st_in = np.load(os.environ["R29_STATE_IN"])
    V = z6.Curve(list(st_in["al"]), list(st_in["be"]), float(st_in["c"]))
    assert len(V.al) == len(st_in["al"]) and bool(np.all(V.al == st_in["al"])) and bool(np.all(V.be == st_in["be"]))
    print("# chunk: continuing after level %d from %s (%d lines, top %.15f)" % (J0 - 1, os.path.basename(os.environ["R29_STATE_IN"]), len(V.al), V.c))
else:
    V = z6.Curve([], [], z6.ABAR)
Vpl = to_PL(V)
tops = []
tot_viol = 0
tot_lines = tot_recs = 0
hull_mismatch = 0
worst = [math.inf] * 4
t0 = time.time()
print("# columns: j | their c_j | stored lines | records | shadow == their step | their lines == my hull of them | checker violations | least margins in ulp: e', th, slope, beta")
for j in range(J0, JMAX + 1):
    Vn = z6.step(V)
    Hs, recs, capline = shadow_step(V)
    same = (Hs.c == Vn.c and len(Hs.al) == len(Vn.al) and bool(np.all(Hs.al == Vn.al)) and bool(np.all(Hs.be == Vn.be)))
    if not same:
        print("STOP: the shadow of step() does not reproduce their step() at level %d" % j)
        R.finish("r29_i1_verify_theirs (stopped)")
        sys.exit(1)
    Vn_pl = to_PL(Vn)
    mine = Vn_pl.lines()
    stored = [(Fr(float(a_)), Fr(float(b_))) for a_, b_ in zip(Vn.al, Vn.be)]
    hull_same = (mine == stored)
    hull_mismatch += (not hull_same)
    certs = certificates(Vn_pl, recs, capline)
    bad = R.check_step(Vpl, Vn_pl, certs, cube, ABAR)
    mg = margins(recs)
    worst = [min(w, m) for w, m in zip(worst, mg)]
    tot_viol += len(bad)
    tot_lines += len(stored)
    tot_recs += len(recs)
    tops.append(Vn.c)
    if j <= 12 or j % 10 == 0 or bad or not hull_same or j == JMAX:
        print("%4d | %.15f | %5d | %5d | %s | %s | %d | %.2f %.2f %.2f %.2f" % (j, Vn.c, len(stored), len(recs), same, hull_same, len(bad), mg[0], mg[1], mg[2], mg[3]), flush=True)
        for b in bad[:5]:
            print("        violation:", b)
    V, Vpl = Vn, Vn_pl
print("# steps %d (levels %d..%d); stored lines %d; generated lines (records) %d; checker violations %d; hull mismatches %d; time %.0f s"
      % (JMAX - J0 + 1, J0, JMAX, tot_lines, tot_recs, tot_viol, hull_mismatch, time.time() - t0))
if os.environ.get("R29_STATE_OUT"):
    np.savez(os.environ["R29_STATE_OUT"], al=V.al, be=V.be, c=V.c)
    print("# state after level %d saved to %s" % (JMAX, os.path.basename(os.environ["R29_STATE_OUT"])))
print("# least margins over the run, in ulp of the stored double (all must be >= 0): e' %.2f, th %.2f, slope %.2f, beta %.2f" % tuple(worst))

# (g) against the semi-analytic envelope and the committed output
envf = E.EnvSA(E.CubeF(float(ufr)), JMAX)
below = [(J0 + i, tops[i] - envf.b[J0 + i]) for i in range(len(tops)) if tops[i] < envf.b[J0 + i] - 1e-12]
print("# largest and smallest (c_j - b_j)/(b_j - h) over the levels of this run: %.3e, %.3e" % (
    max((tops[i] - envf.b[J0 + i]) / (envf.b[J0 + i] - envf.P.h) for i in range(len(tops))),
    min((tops[i] - envf.b[J0 + i]) / (envf.b[J0 + i] - envf.P.h) for i in range(len(tops)))))
print("# tops below the semi-analytic envelope tops (doubles, tolerance 1e-12): %d   [must be 0]" % len(below))
name = {"1": "out_z6_certified_u1.txt", "2": "out_z6_certified_u2.txt", "1/2": "out_z6_certified_u0.5.txt", "0.5": "out_z6_certified_u0.5.txt"}.get(u_str)
if u_str == "1" and K == 4000:
    name = "out_z6_certified_u1_J400.txt"
committed_K = None
if name and os.path.exists(os.path.join(EXPORT, name)):
    com = {}
    for line in open(os.path.join(EXPORT, name)):
        if line.startswith("#"):
            if "K =" in line:
                committed_K = int(line.split("K =")[1].split(";")[0])
            continue
        f = [x.strip() for x in line.split("|")]
        if len(f) > 2:
            try:
                com[int(f[0])] = f[1]
            except ValueError:
                pass
    if committed_K == K:
        diff = [J0 + i for i in range(len(tops)) if (J0 + i) in com and ("%.12f" % tops[i]) != com[J0 + i]]
        ncmp = len([1 for i in range(len(tops)) if (J0 + i) in com])
        print("# committed output %s (K = %d): %d of %d tops differ in the 12 printed decimals" % (name, committed_K, len(diff), ncmp))
    else:
        print("# committed output %s has K = %s: not compared digit by digit" % (name, committed_K))
ok = (tot_viol == 0 and hull_mismatch == 0 and not below and min(worst) >= 0)
print("VERIFY-THEIRS: %s" % ("ALL CHECKS PASS" if ok else "CHECK FAILED"))
R.finish("r29_i1_verify_theirs u=%s J=%d K=%d" % (u_str, JMAX, K))
