#!/usr/bin/env python3
"""
r16_cert.py -- workstream R16: replication of the certified two- and three-level bounds of THY-RES-0013 section 4 /
theory report section 11.19 remark (1b), with own code (r16lib.py; nothing of the theory division imported).

usage:  python3 r16_cert.py <n> <phi1,phi1,...> [modes: two,tuned,searched] [--terms]
output: ln(bound)/(n a) per outer fraction; with --terms the server of every rung (to compare with out_terms_*.txt).
u = 1.
"""
import sys
import time
import math
import r16lib as R


def ranges(ls):
    if not ls:
        return "-"
    out, start, prev = [], ls[0], ls[0]
    for v in ls[1:] + [None]:
        if v is None or v != prev + 1:
            out.append("%d" % start if start == prev else "%d-%d" % (start, prev))
            start = v
        prev = v
    return ", ".join(out)


def main():
    u = 1.0
    a = R.a_of(u)
    n = int(sys.argv[1])
    phis = [float(v) for v in sys.argv[2].split(",")]
    modes = sys.argv[3].split(",") if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else ["two", "tuned", "searched"]
    terms = "--terms" in sys.argv
    na = n * a
    t0 = time.time()
    print("# R16 replication (own code r16lib.py). u = %g, a = %.6f, n = %d, n a = %.4f" % (u, a, n, na))
    print("# started %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    best = {m: (None, None) for m in modes}
    for phi in phis:
        R.clear_tabs()
        R._mid.clear()
        line = "n=%d phi_1=%.3f:" % (n, phi)
        vals = {}
        for mode in modes:
            lev, lcm, rows = R.three_level_bound(u, n, phi, mode, a)
            vals[mode] = lcm / na
            if best[mode][0] is None or lcm / na < best[mode][0]:
                best[mode] = (lcm / na, phi)
            two = [l for l in range(1, lev.L + 1) if rows[l]["kind"] == "2L+"]
            # admissibility facts recorded for the review (Item 1):
            #   max over the chosen two-level servers of (certified accuracy - rung accuracy); must be <= 0
            exc = max([rows[l]["best"]["xout"] - lev.xs[l] for l in two], default=float("nan"))
            line += " %s %.4f [2L+ rungs: %d of %d (%s); max(xout - x_l) over them %.3g] |" % (
                mode, lcm / na, len(two), lev.L, ranges(two), exc)
            if terms:
                cap = R.LN2 + lev.lMbar
                tl = sorted(((lev.lmult(l)[0] + rows[l]["lC"], l) for l in range(1, lev.L + 1)), reverse=True)
                print("n=%d phi_1=%.3f mode %s: ln(C_max)/(na) = %.4f; cap 2 Mbar %.4f; fibre dimension %d; n_o = %d; J = %d; K = %d;"
                      " r-dagger = %d; ln(delta') = %.3f; x_out = %.6f; rungs served by a two-level run: %d of %d (rungs %s)"
                      % (n, phi, mode, lcm / na, cap / na, lev.n_i, lev.n_o, lev.J, lev.K, lev.rdag, lev.ldeltap, lev.xout,
                         len(two), lev.L, ranges(two)))
                for t, l in tl[:4]:
                    print("    term %.4f: rung %2d, server %-4s, accuracy x_l = %.4g (x_{l-1} = %.4g), multiplier: %s %.4f,"
                          " cost charged %.4f" % (t / na, l, rows[l]["kind"], lev.xs[l], lev.xs[l - 1], lev.lmult(l)[1],
                                                  lev.lmult(l)[0] / na, rows[l]["lC"] / na))
                print("    rung   accuracy   multiplier   base bracket   best two-level candidate: certified bound, certified"
                      " accuracy, design   -> server, term")
                for l in range(1, lev.L + 1):
                    r = rows[l]
                    mult, mk = lev.lmult(l)
                    bst = r["best"]
                    print("    %4d %10.4g   %-5s %.4f   %12.4f   %s   -> %s, %.4f"
                          % (l, lev.xs[l], mk, mult / na, r["c0"] / na,
                             ("%.4f, %.6g, %s" % (bst["lCmax"] / na, bst["xout"], bst["name"])) if bst is not None
                             else "(none tried)", r["kind"], (mult + r["lC"]) / na))
        line += "   [%.0f s]" % (time.time() - t0)
        print(line, flush=True)
    print("n=%d best over these outer fractions: " % n + "; ".join(
        "%s %.4f (phi_1 = %g)" % (m, best[m][0], best[m][1]) for m in modes))
    print("# finished %s; elapsed %.0f s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), time.time() - t0))
    print("peak RSS MB", R.peak_rss_mb())


if __name__ == "__main__":
    main()
