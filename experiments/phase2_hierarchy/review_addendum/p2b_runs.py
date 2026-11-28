#!/usr/bin/env python3
"""Reviewer's runs of the extremal-profile attack on Theorem P (driver for p2_extremal.py, own code).

Lattice effect that had to be separated from a real violation: the lattice core starts at ceil(kappa n_c);
the anchor of the proof sits at kappa n_c.  Each class costs up to (u - |f'(kappa)|) * (ceil(kappa n_c) - kappa n_c)
nats.  "Aligned" sizes are class sizes for which kappa n_c is just below an integer; variant `Pout` uses the
smallest lattice box containing K and brackets the continuum value from the other side.

modes:  align | controls2 | scaleA1 | scaleA2 | scaleA3 | sweepA [ident] [confs] | two
"""
import sys
import numpy as np
from p2_extremal import consts, finv, run_all, summarize, fmt, f

def gapk(u, n):
    kap = consts(u)[2]
    return float(np.ceil(kap * n - 1e-9) - kap * n)

def aligned(u, target, win=4):
    best = None
    for n in range(max(2, target - win), target + win + 1):
        d = gapk(u, n)
        if best is None or d < best[0] - 1e-12 or (abs(d - best[0]) < 1e-12 and abs(n - target) < abs(best[1] - target)):
            best = (d, n)
    return best[1]

def table(res, key=lambda r: (r['args'][5], r['args'][1].__repr__(), r['args'][2].__repr__(), r['args'][3], r['args'][4])):
    """one line per (variant, G1, G2, u, Theta/nh): excess/u along the scale"""
    rows = {}
    for r in res:
        if r['empty']:
            continue
        rows.setdefault(key(r), []).append(r)
    for k in rows:
        rs = sorted(rows[k], key=lambda r: r['n'])
        print("   %-5s G1=%-18s G2=%-24s u=%g Th/nh=%-4g : " % k + " | ".join(
            "n=%d: %+.2fu (gain %+.1f, bound %+.1f)" % (r['n'], r['excess'] / r['args'][3], r['gain'], r['nh'] - r['args'][4] * r['nh'])
            for r in rs))
    sys.stdout.flush()

def scale_cases(structs, us, ths, variant='P', ident='hub', align=True):
    cases = []
    for name, base, G1, G2, scales in structs:
        for u in us:
            for th in ths:
                for s in scales:
                    sizes = tuple((aligned(u, b * s) if align else b * s) for b in base)
                    cases.append((sizes, G1, G2, u, th, variant, ident))
    return cases

S_PAIRS = ('one cell -> pairs', (1, 1, 1, 1), [[0, 1, 2, 3]], [[0, 1], [2, 3]])
S_THREE = ('one cell -> {0},{1},{2,3}', (1, 1, 1, 1), [[0, 1, 2, 3]], [[0], [1], [2, 3]])
S_3IN1 = ('three classes 1:2:3 in one cell, never split', (1, 2, 3), [[0, 1, 2]], [[0, 1, 2]])
S_TINY = ('3% class with a big one after the split', (1, 15, 16), [[0, 1, 2]], [[0, 1], [2]])
S_NEST = ('nested', (1, 1, 1, 1), [[0, 1], [2, 3]], [[0, 1], [2], [3]])
S_FIVE = ('five classes -> {0,1},{2,3},{4}', (1, 1, 1, 1, 1), [[0, 1, 2, 3, 4]], [[0, 1], [2, 3], [4]])
S_4IN1 = ('four classes in one cell, never split', (1, 1, 1, 1), [[0, 1, 2, 3]], [[0, 1, 2, 3]])
S_3HID = ('three hidden classes after split', (1, 1, 1, 1), [[0, 1, 2, 3]], [[0, 1, 2], [3]])
S_TWO = ('two classes 1:3, never split', (1, 3), [[0, 1]], [[0, 1]])

CONF = {
    'c1':  ('three classes in one cell, never split',          (40, 60, 80), [[0, 1, 2]], [[0, 1, 2]]),
    'c2':  ('class of weight ~3% in a cell of three',          (6, 84, 90), [[0, 1, 2]], [[0, 1, 2]]),
    'c3':  ('~3% class stays with a big one after split',      (6, 84, 90), [[0, 1, 2]], [[0, 1], [2]]),
    'c4':  ('cell split into three {0},{1},{2,3}',             (30, 34, 38, 42), [[0, 1, 2, 3]], [[0], [1], [2, 3]]),
    'c5':  ('five classes, split into {0,1},{2,3},{4}',        (14, 16, 18, 20, 22), [[0, 1, 2, 3, 4]], [[0, 1], [2, 3], [4]]),
    'c6':  ('nested {0,1},{2,3} -> {0,1},{2},{3}',             (30, 34, 38, 42), [[0, 1], [2, 3]], [[0, 1], [2], [3]]),
    'c7':  ('three hidden classes left in a cell after split', (24, 30, 36, 54), [[0, 1, 2, 3]], [[0, 1, 2], [3]]),
    'c8':  ('~2.5% class with one big class',                  (6, 234), [[0, 1]], [[0, 1]]),
    'c9':  ('two equal classes (tight at Theta = nh)',         (120, 120), [[0, 1]], [[0, 1]]),
    'c10': ('four classes in one cell, never split',           (30, 34, 38, 42), [[0, 1, 2, 3]], [[0, 1, 2, 3]]),
    'c11': ('two cells of G1, each hiding a pair forever',     (30, 34, 38, 42), [[0, 1], [2, 3]], [[0, 1], [2, 3]]),
    'c12': ('~2% class + 3 classes, split {0,1},{2,3}',        (5, 60, 64, 72), [[0, 1, 2, 3]], [[0, 1], [2, 3]]),
    'c13': ('pairs with classes of very unequal size',         (10, 90, 20, 60), [[0, 1, 2, 3]], [[0, 1], [2, 3]]),
}

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == 'align':
        print("ALIGNMENT EXPERIMENT (structure: one cell -> pairs {0,1},{2,3}; four equal classes of size N).")
        print("  d = ceil(kappa N) - kappa N.  If the positive excess is a lattice effect of the core boundary it follows d, not n;")
        print("  `P` = lattice points inside K (upper bound for the continuum), `Pout` = smallest lattice box containing K.")
        for u, Ns in ((2.0, (36, 46, 49, 53, 60, 67)), (4.0, (36, 41, 42, 47, 48, 53, 59, 65))):
            pu, L1, kap, h, a = consts(u)
            print("  u=%g kappa=%.5f  (u - |f'(kappa)|) = %.3f nats per unit of d and class" % (u, kap, u - abs(np.log(kap / (1 - kap)))))
            for th in (1.0, 1.2):
                cases = [((N, N, N, N), [[0, 1, 2, 3]], [[0, 1], [2, 3]], u, th, v, 'hub') for N in Ns for v in ('P', 'Pout')]
                res = run_all(cases, procs=4)
                print("   Th/nh=%g: " % th + " | ".join("N=%d d=%.2f: P %+.2fu, Pout %+.2fu" % (
                    Ns[i], gapk(u, Ns[i]), res[2 * i]['excess'] / u, res[2 * i + 1]['excess'] / u) for i in range(len(Ns))))
                sys.stdout.flush()
    elif mode == 'controls2':
        print("CONTROL (i'): variant `alg` (blind region {R <= Theta}, as in the author's script), Theta = 0.7 n h, two equal classes:")
        print("              the plain dip of Remark 4 is admissible; excess/n must be >= D(theta) - (h - theta) > 0")
        for u in (2.0, 4.0):
            pu, L1, kap, h, a = consts(u)
            pred = (u * finv(0.7 * h) - L1) - 0.3 * h
            res = run_all([((s, s), [[0, 1]], [[0, 1]], u, 0.7, 'alg', 'hub') for s in (60, 120, 240, 480)], procs=4)
            print("     u=%g plain-dip prediction per coordinate: %+.5f ;  measured excess/n: %s" % (
                u, pred, ", ".join("%+.5f" % (r['excess'] / r['n']) for r in res)))
        print("CONTROL (i''): same with Theorem P's own hypothesis ((H1) on K): for theta < h the plain dip is NOT admissible")
        print("              (its cone reaches into K), and the bound nu_K + h - theta (now positive) still holds:")
        for u in (2.0, 4.0):
            res = run_all([((s, s), [[0, 1]], [[0, 1]], u, 0.7, 'P', 'hub') for s in (60, 120, 240, 480)], procs=4)
            print("     u=%g measured excess/n: %s" % (u, ", ".join("%+.5f" % (r['excess'] / r['n']) for r in res)))
    elif mode == 'two':
        print("CONTROL (iv'): two rounds only; classes (A0,A1,B0,B1) with phi_A = 0.64, G1 = {A0},{A1},{B0,B1}; the final batch samples shells of G1.")
        print("   gain = max hidden (U - R) with the visible maximum normalised to 0.  Two rounds fail while gain >= 0.")
        print("   Archive (Theorem 11.86 / U3): threshold theta_2*/h = 1.33 at u = 2 (optimal split), 1.37 at u = 1 (phi_1 = 0.64).")
        for u, scales in ((2.0, (2, 3, 4)), (3.0, (2, 3, 4))):
            cases = [((16 * s, 16 * s, 9 * s, 9 * s), [[0], [1], [2, 3]], [[0], [1], [2, 3]], u, th, 'two', 'hub')
                     for th in (1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7) for s in scales]
            res = run_all(cases, procs=4)
            for i, th in enumerate((1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7)):
                rs = res[len(scales) * i: len(scales) * (i + 1)]
                print("     u=%g Th/nh=%.1f: gain/n = %s" % (u, th, ", ".join("n=%d: %+.5f" % (r['n'], r['gain'] / r['n']) for r in rs)))
            sys.stdout.flush()
    elif mode in ('scaleA1', 'scaleA2', 'scaleA3'):
        if mode == 'scaleA1':
            structs = [S_PAIRS + ((16, 32, 48, 64),), S_THREE + ((16, 32, 48, 64),)]
        elif mode == 'scaleA2':
            structs = [S_3IN1 + ((20, 40, 80),), S_TINY + ((6, 12, 24),), S_TWO + ((60, 120, 240, 480),),
                       S_NEST + ((16, 32, 48),), S_4IN1 + ((16, 32, 48),)]
        else:
            structs = [S_FIVE + ((10, 16, 22, 26),), S_3HID + ((16, 32, 48),)]
        print("SCALING with aligned sizes, Theorem P exactly as stated (variant P, identification by hubs).")
        print("  A violation of the theorem would show as excess/u growing linearly in n; the theorem predicts excess <= O(#classes) u.")
        cases = scale_cases(structs, (2.0, 4.0), (1.0, 1.2, 1.5))
        res = run_all(cases, procs=4)
        print("  SUMMARY (excess in lattice steps u; gain = max hidden (U-R); bound = n h - Theta):")
        table(res)
        summarize(res, mode)
    elif mode == 'sweepA':
        ident = sys.argv[2] if len(sys.argv) > 2 else 'hub'
        which = sys.argv[3].split(',') if len(sys.argv) > 3 else list(CONF)
        us = tuple(float(x) for x in sys.argv[4].split(',')) if len(sys.argv) > 4 else (1.0, 2.0, 4.0)
        ths = (1.0, 1.05, 1.2, 1.5, 2.5)
        print("BREADTH SWEEP, Theorem P exactly as stated (variant P), identification=%s, aligned sizes; excess in units of u at Theta/nh = %s"
              % (ident, ths))
        cases = []
        for c in which:
            name, sizes, G1, G2 = CONF[c]
            for u in us:
                sz = tuple(aligned(u, s, win=(1 if s < 10 else 3)) for s in sizes)
                for th in ths:
                    cases.append((sz, G1, G2, u, th, 'P', ident))
        res = run_all(cases, procs=4)
        print("  SUMMARY:")
        i = 0
        for c in which:
            name, sizes, G1, G2 = CONF[c]
            for u in us:
                rs = res[i:i + len(ths)]
                i += len(ths)
                print("   %-4s %-48s u=%g n=%-4d %-20s nh/u=%5.1f : %s" % (
                    c, name, u, rs[0]['n'], rs[0]['args'][0], rs[0]['nh'] / u,
                    " | ".join(("%+6.2f" % (r['excess'] / u)) if r['nhid'] else "  none" for r in rs)))
        summarize(res, "sweepA/" + ident)
    else:
        raise SystemExit("unknown mode")
