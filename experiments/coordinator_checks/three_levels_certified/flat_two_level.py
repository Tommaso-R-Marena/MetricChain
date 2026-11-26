#!/usr/bin/env python3
"""Two levels at the flat instance against the certified three-level bound: a comparison that needs no model.

Why (SCI-REV-0016, finding m3; theory report section 11.19, remark (1b)).  The comparison "(beta)" of remark (1b)
sets the CERTIFIED cost bound of three nested levels (a theorem: no run on any member of the class makes more
evaluations) against the worst instance FOUND for two levels by the Computational Research Division, whose cost is
the cost of a MEAN RUN (every random count replaced by its mean) -- a model, and a search.  At one instance neither
is involved: on the zero function a run of the two-level algorithm with base brackets inside is deterministic, so
its number of evaluations is exact (experiments/reviews/R8/r8_flat.flat_run, the referee's routine; nothing is
re-implemented here).  If that exact number exceeds the certified three-level bound, then the two-level algorithm
as built makes, in every run on the zero function, more evaluations than three levels make in any run on any
instance.

The two-level design is the one of the table of remark (1b): b = 0.5, lam = 0.2, eta = eta' = theta = 0.05,
delta = 0.05, the ladder x_l = x_0 (b/x_0)^(l/40), certified accuracy 0.8715 at every outer block; u = 1.
Scanned: (i) the outer fractions 0.30, 0.31, ..., 0.85; (ii) EVERY outer block size n_o in a window of +-0.03 n
around the minimiser of (i), to see what the grid misses; (iii) every outer block size in the window in which the
two-level cost is not above the three-level bound (if any), to delimit it.

usage:  python3 flat_two_level.py [n,n,...]          default 4000,8000,16000,32000,64000
"""
import sys, math, time
sys.path.insert(0, __file__.rsplit('/', 1)[0] + '/../../reviews/R8')
import r8_flat as R

U = 1.0
P = 1 / (1 + math.exp(U))
A = math.log(2) + P * math.log(P) + (1 - P) * math.log(1 - P)
# certified three-level bound, ln(bound)/(n a): out_summary.txt (column "the same with more middle designs"; at n = 64000
# the outer fraction 0.275 of out_64000d.txt, which the Scientific Discovery Division found with its own code)
CERT3 = {4000: 0.6106, 8000: 0.5262, 16000: 0.4782, 32000: 0.4439, 64000: 0.4341}


def cost(n, n_o):
    r = R.flat_run(U, n, (n_o + 0.5) / n)
    assert r['n_o'] == n_o and abs(r['xout'] - 0.8715) < 1e-4, (n, n_o, r['n_o'], r['xout'])
    return r['lcost'] / (n * A), r['lCmax'] / (n * A)


def main():
    ns = [int(v) for v in sys.argv[1].split(',')] if len(sys.argv) > 1 else sorted(CERT3)
    print("two levels at the flat instance (exact, deterministic) against the certified three-level bound; u = 1, "
          "a = %.6f; all figures are ln(.)/(n a)" % A)
    for n in ns:
        t0 = time.time()
        c3 = CERT3.get(n)
        grid = [round(0.30 + 0.01 * i, 2) for i in range(56)]
        vals = {}
        for phi in grid:
            n_o = int(math.floor(phi * n + 1e-9))
            vals[n_o] = cost(n, n_o)
        best = min(vals, key=lambda k: vals[k][0])
        print("n=%d  grid of step 0.01 (0.30 ... 0.85): minimum %.4f at n_o = %d (phi = %.2f); its own certified "
              "bound there %.4f" % (n, vals[best][0], best, best / n, vals[best][1]))
        # every block size around the minimiser
        w = int(0.03 * n)
        step = max(1, n // 4000)                                   # every n_o up to n = 4000, else every (n/4000)-th
        fine = {}
        for n_o in range(max(1, best - w), min(n - 1, best + w) + 1, step):
            fine[n_o] = cost(n, n_o)
        fbest = min(fine, key=lambda k: fine[k][0])
        print("       every %s outer block size in [%d, %d]: minimum %.4f at n_o = %d (phi = %.4f)"
              % ('' if step == 1 else '%d-th' % step, min(fine), max(fine), fine[fbest][0], fbest, fbest / n))
        if c3 is not None:
            below = sorted(k for k in vals if vals[k][0] <= c3)
            allv = dict(vals); allv.update(fine)
            belowf = sorted(k for k in allv if allv[k][0] <= c3)
            print("       certified three-level bound %.4f; margin (two-level flat minimum minus the bound): %+.4f n a "
                  "= %+.0f nats" % (c3, min(fine[fbest][0], vals[best][0]) - c3,
                                    (min(fine[fbest][0], vals[best][0]) - c3) * n * A))
            if below:
                print("       grid fractions at which two levels at the flat instance cost no more than the bound: "
                      "%.2f ... %.2f (%d of %d)" % (below[0] / n, below[-1] / n, len(below), len(grid)))
            else:
                print("       grid fractions at which two levels at the flat instance cost no more than the bound: none")
            if belowf and not below:
                print("       off the grid: %d block sizes, %.4f ... %.4f" % (len(belowf), belowf[0] / n, belowf[-1] / n))
        print("       (%.0f s)" % (time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
