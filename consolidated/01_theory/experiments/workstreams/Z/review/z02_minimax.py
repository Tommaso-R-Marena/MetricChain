#!/usr/bin/env python3
"""z02: (ii) of the brief -- Proposition Z1(2) and the minimax identity behind it.

For a convex nondecreasing W : [0, b] -> [0, 1] and g > 0, with theta = theta_na of the cube:

  LHS(g) = inf_{0<phi<1} max_{(B,s) in E(W,b)} Psi_g(phi; B, s),   Psi = (1 - phi) B + (1 - s) phi theta(g/phi)
  MID(g) = sup{ B - Sigma(B, W(B)) g : 0 <= B <= b, Sigma(B, W(B)) < inf }          (right side of Proposition U)
  RHS(g) = M_{W',b'}(g) = max_{B <= b'} (B - W'(B) g)                                 (Corollary U')

Every quantity is bracketed rigorously (up to rounding) between a LOWER value (maximum over sample points of the curve)
and an UPPER value (sample points plus the intersection points of consecutive tangents; zrev.curve_points), so that
"LHS_up <= RHS_lo + tol" proves the inequality at that g up to rounding, whatever the grid.

Part A (the chain): W = W_j, b = b_j, W' = W_{j+1}, b' = b_{j+1} for the cut orbit curves of the cube,
        u in {1/2, 1, 2}, j = 0..J-1:   (T1) LHS <= RHS;   (T2) LHS = MID (both directions);   (T3) MID <= RHS.
Part B (adversarial): other convex nondecreasing W with values in [0, 1] (powers, linear, flat-then-linear, random
        piecewise-quadratic), heights b up to a and beyond the regular region; W' := min(1, Sigma(., W(.))) on [0, b'],
        b' = sup{B <= b : Sigma(B, W(B)) < inf}  (the curve of Corollary U' / remark (1) of R_REPORT section 5; it need not be
        convex -- M is a supremum of lines in any case):   (T1') LHS <= M_{W',b'};   (T2) LHS = MID.
Part C (controls, must FAIL): a concave W, a decreasing W (identity LHS = MID must break: LHS > MID).
Usage: python3 z02_minimax.py [A|B|C|all]
"""
import math
import random
import sys
import time

import numpy as np

sys.dont_write_bytecode = True
import zrev

INF = zrev.INF
which = sys.argv[1] if len(sys.argv) > 1 else 'all'
TOL = 2e-12
t00 = time.time()


def image_curve(cu, Bs, Ws, dWs, b):
    """H(B) = Sigma(B, W(B)) with derivative, on the sample points where it is finite; and b' = sup{B <= b : H < inf}."""
    sig, gB, gs = cu.sigma_grad(Bs, np.minimum(Ws, 1.0))
    fin = np.isfinite(sig) & (Ws < 1.0)
    H = np.where(fin, sig, INF)
    dH = np.where(fin, gB + gs * dWs, INF)
    return H, dH, fin


def bprime(cu, Wfun, b):
    """sup{B in [0, b] : Sigma(B, W(B)) < inf} = sup{B <= b : B < (1 - W(B)) a}  (cube: infinite slope at zero);
    B - (1 - W(B)) a is increasing, so bisection."""
    f = lambda B: B - (1.0 - float(Wfun(np.array([B]))[0][0])) * cu.a
    if f(b) < 0:
        return b, True          # finite up to and including b
    lo, hi = 0.0, b
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo, False            # the supremum is not attained (Sigma = inf at b')


def sample(Wfun, b, npts, closed=True, extra=None):
    """sample points of [0, b] (uniform, denser towards b, plus the intersections of consecutive tangents, where the
    polygonal brackets are widest) with the values and derivatives of the convex function Wfun."""
    t = np.linspace(0.0, 1.0, npts)
    Bs = np.unique(np.concatenate([b * t, b * (1 - 10.0 ** np.linspace(-1, -13, 300))] + ([extra] if extra is not None else [])))
    Bs = Bs[(Bs >= 0) & ((Bs <= b) if closed else (Bs < b))]
    for _ in range(2):          # two refinements at the tangent intersections
        Ws, dWs = Wfun(Bs)
        ok = np.isfinite(Ws) & np.isfinite(dWs)
        Bs, Ws, dWs = Bs[ok], Ws[ok], dWs[ok]
        (_, _), (uB, us) = zrev.curve_points(Bs, Ws, dWs)
        Bx = uB[len(Bs):]
        Bs = np.unique(np.concatenate([Bs, Bx]))
    Ws, dWs = Wfun(Bs)
    ok = np.isfinite(Ws) & np.isfinite(dWs)
    return Bs[ok], Ws[ok], dWs[ok]


def test_pair(cu, Wfun, b, W2fun, b2, gs, npts=1201, label=""):
    """returns dict of worst excesses.  Wfun(B) -> (W, W');  W2fun likewise or None (then W' := min(1, Sigma(., W(.))))."""
    gs = np.asarray(gs, dtype=np.float64)
    Bs, Ws, dWs = sample(Wfun, b, npts)
    (lB, ls), (uB, us) = zrev.curve_points(Bs, Ws, dWs)
    # the image curve H = Sigma(., W(.)) on [0, b') (or [0, b'] if finite there)
    bp, attained = bprime(cu, Wfun, b)

    def Hfun(B):
        W, dW = Wfun(B)
        sig, gB, gs_ = cu.sigma_grad(B, np.minimum(W, 1.0))
        fin = np.isfinite(sig) & (W < 1.0)
        with np.errstate(invalid='ignore'):
            return np.where(fin, sig, INF), np.where(fin, gB + gs_ * dW, INF)
    Bi, H, dH = sample(Hfun, bp, npts, closed=attained)
    (mlB, mls), (muB, mus) = zrev.curve_points(Bi, H, dH)
    muB = np.append(muB, bp)            # beyond the last sample point: B <= b', H >= H(last)
    mus = np.append(mus, H[-1])
    if W2fun is not None:
        B2, W2, dW2 = sample(W2fun, b2, npts)
        (rlB, rls), (ruB, rus) = zrev.curve_points(B2, W2, dW2)
    else:
        rlB, rls = Bi, np.minimum(H, 1.0)
        ruB, rus = muB, np.minimum(mus, 1.0)
    Lup, _ = zrev.inf_phi(cu, gs, uB, us)
    Llo, _ = zrev.inf_phi(cu, gs, lB, ls)
    Mlo = (mlB[None, :] - mls[None, :] * gs[:, None]).max(axis=1)
    Mup = (muB[None, :] - mus[None, :] * gs[:, None]).max(axis=1)
    Rlo = (rlB[None, :] - rls[None, :] * gs[:, None]).max(axis=1)
    Rup = (ruB[None, :] - rus[None, :] * gs[:, None]).max(axis=1)
    out = dict(T1=float(np.max(Lup - Rlo)), T1v=float(np.max(Llo - Rup)), T2a=float(np.max(Llo - Mup)), T2b=float(np.max(Mlo - Lup)),
               T2abs=float(np.max(np.abs(0.5 * (Lup + Llo) - 0.5 * (Mup + Mlo)))),
               T3=float(np.max(Mlo - Rup)), gapL=float(np.max(Lup - Llo)), gapM=float(np.max(Mup - Mlo)), gapR=float(np.max(Rup - Rlo)),
               slack=float(np.max(Rlo - Lup)), n=len(gs))
    return out


def gs_for(cu):
    return np.concatenate([10.0 ** np.linspace(-7, -3, 9), np.linspace(0.002, 1.3, 40) * cu.eps_star, [2 * cu.eps_star, cu.u, 3 * cu.u]])


KEYS = ('T1', 'T1v', 'T2a', 'T2b', 'T2abs', 'T3', 'gapL', 'gapM', 'gapR', 'slack')


def merge(w, r):
    for k in KEYS:
        w[k] = max(w.get(k, -INF), r[k])
    w['n'] = w.get('n', 0) + r['n']


def report(w):
    print("    (T1) Z1(2):  max of LHS_up - RHS_lo = %.3e  [<= tol proves LHS <= RHS];   max of LHS_lo - RHS_up = %.3e  [> 0 would be a proven violation];"
          "  largest slack RHS - LHS = %.3e" % (w['T1'], w['T1v'], w['slack']))
    print("    (T2) minimax identity:  max of LHS_lo - MID_up = %.3e,  max of MID_lo - LHS_up = %.3e,  max |LHS - MID| (midpoints) = %.3e"
          % (w['T2a'], w['T2b'], w['T2abs']))
    print("    (T3) max of MID_lo - RHS_up = %.3e;   widths of the brackets: LHS %.2e, MID %.2e, RHS %.2e" % (w['T3'], w['gapL'], w['gapM'], w['gapR']))


if which in ('A', 'all'):
    print("== Part A: the chain of cut orbit curves ==")
    tot = 0
    sets = ((1.0, 0.05, 0.003, 31), (0.5, 0.05, 0.0008, 21), (2.0, 0.05, 0.01, 21), (1.0, 0.15, 0.003, 13), (1.0, 0.05, 0.012, 9))
    if len(sys.argv) > 2:
        sets = [sets[int(k)] for k in sys.argv[2].split(',')]
    for u, dst, eps1, J in sets:
        cu = zrev.Cube(u)
        C = zrev.Chain(cu, dst, eps1, J)
        gs = gs_for(cu)
        w = {}
        for j in range(J):
            r = test_pair(cu, lambda B, j=j: C.Wd(j, B), C.b[j], lambda B, j=j: C.Wd(j + 1, B), C.b[j + 1], gs)
            merge(w, r)
        tot += w['n']
        print("u = %g, s_t = L + %g, b_0 = h + %g (range condition to level %d: %s, largest W_j(b_j) = %.4f): levels j = 0..%d, %d values of g each (%d cases)   [%.0f s]"
              % (u, dst, eps1, J, C.range_ok, max(C.Wtop), J - 1, len(gs), w['n'], time.time() - t00))
        report(w)
        sys.stdout.flush()
    print("Part A: %d cases" % tot)

if which in ('B', 'all'):
    print("== Part B: other convex nondecreasing W (adversarial) ==")
    random.seed(7)
    tot = 0
    worst = {}
    wat = {}
    for u in (0.5, 1.0, 2.0):
        cu = zrev.Cube(u)
        gs = gs_for(cu)[::3]
        fams = []
        for bfac in (0.3, 0.9, 1.0, 1.5, 3.0):                  # b as a multiple of h ... up to above a
            for b in (bfac * cu.h, min(bfac * cu.a, 0.999 * math.log(2))):
                for p in (1.0, 1.5, 2.0, 4.0, 10.0):
                    for top in (1.0, 0.6, 0.2):
                        fams.append(("top*(B/b)^%g, b=%.4f, top=%g" % (p, b, top),
                                     (lambda B, b=b, p=p, top=top: (top * (B / b) ** p, top * p * (B / b) ** (p - 1) / b)), b))
                # flat, then linear (a kink): W = max(0, c (B - B1))
                for frac, top in ((0.5, 1.0), (0.9, 1.0), (0.2, 0.7)):
                    B1 = frac * b
                    c = top / (b - B1)
                    fams.append(("kink at %.2f b, b=%.4f, top=%g" % (frac, b, top),
                                 (lambda B, B1=B1, c=c: (np.maximum(0.0, c * (B - B1)), np.where(B >= B1, c, 0.0))), b))
                # W = 0 (flat) and W = const > 0 is excluded (W(0) > 0: vacuous)
                fams.append(("zero, b=%.4f" % b, (lambda B: (np.zeros_like(B), np.zeros_like(B))), b))
                # exponential-type: W = top (e^{kB/b} - 1)/(e^k - 1)
                for k in (3.0, 12.0):
                    fams.append(("exp k=%g, b=%.4f" % (k, b),
                                 (lambda B, b=b, k=k: (np.expm1(k * B / b) / math.expm1(k), k / b * np.exp(k * B / b) / math.expm1(k))), b))
        for name, Wfun, b in fams:
            r = test_pair(cu, Wfun, b, None, None, gs, npts=801)
            tot += r['n']
            for k in KEYS:
                if r[k] > worst.get(k, -INF):
                    worst[k] = r[k]
                    wat[k] = "u=%g %s" % (u, name)
        print("u = %g: %d families x %d values of g done   [%.0f s]" % (u, len(fams), len(gs), time.time() - t00))
        sys.stdout.flush()
    print("Part B: %d cases (RHS here is M_{W',b'} with W' = min(1, Sigma(., W(.))))" % tot)
    report(worst)
    print("    worst cases: T1 at %s; T1v at %s; T2abs at %s; widest bracket at %s" % (wat.get('T1'), wat.get('T1v'), wat.get('T2abs'), wat.get('gapL')))

if which in ('C', 'all'):
    print("== Part C: controls (the identity must FAIL: LHS > MID) ==")
    cu = zrev.Cube(1.0)
    gs = gs_for(cu)[::4]
    b = 0.9 * cu.a

    def dense(Wf, g):
        Bs = np.linspace(0.0, b, 20001)
        Ws = Wf(Bs)
        L, _ = zrev.inf_phi(cu, g, Bs, Ws)
        sig = cu.sigma(Bs, np.minimum(Ws, 1.0))
        fin = np.isfinite(sig) & (Ws < 1.0)
        return float(L[0]), float(np.max(Bs[fin] - sig[fin] * g))
    for name, Wf in (("concave W = sqrt(B/b)", lambda B: np.sqrt(B / b)),
                     ("step W = 1{B > b/2}", lambda B: (B > b / 2).astype(float)),
                     ("decreasing W = 0.5 (1 - B/b)", lambda B: 0.5 * (1 - B / b))):
        ex = [(lambda t: t[0] - t[1])(dense(Wf, g)) for g in gs]
        print("   %-30s max of LHS - MID over %d values of g: %.4f (relative to a: %.3f)   -> identity fails: %s" % (name, len(gs), max(ex), max(ex) / cu.a, max(ex) > 1e-4))
print("total time %.0f s" % (time.time() - t00))
