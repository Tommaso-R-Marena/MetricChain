#!/usr/bin/env python3
"""Which term of the certified bound C_max of the outer level dominates, and which procedure serves which rung.

Companion of cert3.py (same directory; read its header first).  Theorem 11.56:

    C_max = 1 + 2 Mbar + sum_{l=1}^{L} min{ 2 Mbar , (J+1) cnt(x_{l-1}) } * C_l ,

C_l the cost bound of the procedure that serves rung l.  For one size and one outer fraction this script prints, for
each mode of cert3.py asked for, the bound, the term 2 Mbar ("cap": the largest outer sample), the four largest terms
of the sum, and a table of the rungs: the cost of the base bracket, the best two-level candidate, its certified bound
and its cost at the flat fibre, and which of the two serves the rung.  The multiplier of a rung is the cap for coarse
rungs (every point of the outer sample may need them) and the count (J+1) cnt(x_{l-1}) for fine ones.

usage:  python3 terms.py <n> <phi_1> [modes, default cert,tuned,searched]
        (u = 1; the outer level has the parameters of the report's section 6.4: the defaults of r8_flat.flat_run)
"""
import math
import sys

import cert3

F = cert3.F


def main():
    u = 1.0
    pu = 1 / (1 + math.exp(u))
    a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
    n = int(sys.argv[1])
    phi = float(sys.argv[2])
    modes = sys.argv[3].split(',') if len(sys.argv) > 3 else ['cert', 'tuned', 'searched']
    lam, eta, etap, theta, Lr = 0.2, 0.05, 0.05, 0.05, 40      # the defaults of r8_flat.flat_run
    na = n * a
    for mode in modes:
        chosen = []
        r = F.flat_run(u, n, phi, inner=cert3.make_inner(u, mode, chosen))
        assert len(chosen) == Lr
        lK = math.log(r['K'])
        J, lMbar, xs, lc, kinds, n_o = r['J'], r['lMbar'], r['xs'], r['lcosts'], r['kinds'], r['n_o']
        nu1 = 2 * math.exp(u) * n_o / theta
        nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
        lnu = lK + math.log(nu0)

        def lcnt(x):
            return max(lK, math.log(2 * (1 + eta) ** 2 / (1 - eta)) + lam + lnu + x)

        cap = math.log(2) + lMbar
        terms = []
        total = [0.0, cap]
        mults = {}
        for l in range(1, Lr + 1):
            mult = min(cap, math.log(J + 1) + lcnt(xs[l - 1]))
            mults[l] = (mult, 'cap' if mult == cap else 'count')
            total.append(mult + lc[l])
            terms.append((mult + lc[l], l))
        m = max(total)
        lsum = m + math.log(sum(math.exp(t - m) for t in total))
        assert abs(lsum - r['lCmax']) < 1e-9 * max(1.0, abs(lsum)), (lsum, r['lCmax'])    # the terms are those of flat_run
        terms.sort(reverse=True)
        two = [l for l in range(1, Lr + 1) if kinds[l] == '2L+']
        print("n=%d phi_1=%.3f mode %s: ln(C_max)/(na) = %.4f; cap 2 Mbar %.4f; fibre dimension %d; rungs served by a"
              " two-level run: %d of %d%s"
              % (n, phi, mode, r['lCmax'] / na, cap / na, r['n_i'], len(two), Lr,
                 (" (rungs %s)" % ranges(two)) if two else ""))
        for t, l in terms[:4]:
            print("    term %.4f: rung %2d, server %-4s, accuracy x_l = %.4g (x_{l-1} = %.4g), multiplier: %s %.4f, cost charged"
                  " %.4f" % (t / na, l, kinds[l], xs[l], xs[l - 1], mults[l][1], mults[l][0] / na, lc[l] / na))
        print("    rung   accuracy   multiplier   base bracket   best two-level candidate: certified bound, flat cost, design"
              "   -> server, term")
        for l in range(1, Lr + 1):
            x, c0, design, lcm, lfl, use = chosen[l - 1]
            assert abs(x - xs[l]) < 1e-9 * max(1.0, x)
            print("    %4d %10.4g   %-5s %.4f   %12.4f   %s   -> %s, %.4f"
                  % (l, x, mults[l][1], mults[l][0] / na, c0 / na,
                     ("%.4f, %.4f, %s" % (lcm / na, lfl / na, design)) if design is not None else "(none tried)",
                     kinds[l], (mults[l][0] + lc[l]) / na))


def ranges(ls):
    out, start, prev = [], ls[0], ls[0]
    for v in ls[1:] + [None]:
        if v is None or v != prev + 1:
            out.append("%d" % start if start == prev else "%d-%d" % (start, prev))
            start = v
        prev = v
    return ", ".join(out)


if __name__ == '__main__':
    main()
