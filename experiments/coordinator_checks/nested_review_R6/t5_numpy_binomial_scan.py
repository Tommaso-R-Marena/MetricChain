"""R6-T5: where is numpy's Generator.binomial(n, p) wrong?  (numpy 2.5.3; the finding of SCI-REV-0007, section 4,
re-measured and extended.)

For Bin(n, mu/n) with n huge the exact mean and variance are mu and mu (1 - mu/n).  Reported per cell: the bias of the
sample mean, its z-score, the relative error of the sample variance and its z-score (the variance of the squared
deviation of a near-Poisson law is 2 mu^2 + mu).  |z| > 4 is a detection.

 Section A   the regime of the review: n from 1e12 to 2^62, means 20 ... 1e5            (400 000 draws per cell)
 Section B   where does it start?  n from 2^31 to 6e15, means 92, 500, 5000             (2 000 000 draws per cell)
 Section C   large means at n >= 1e16                                                   (4 000 000 draws per cell)
 Section D   the counts and conditional probabilities that actually occurred in the published run of
             experiments/workstreams/K/sim_grouped.py (see t5_trace_old_runs.py)        (8 000 000 draws per cell)
 Section E   the cells of referee R8's check behind its erratum m6 (n = 2^59, p = 1e-15 ... 1e-20; R8 used 4000
             draws); means below 30 go through numpy's inversion branch                 (2 000 000 draws per cell)
 Section F   numpy's Poisson sampler, for comparison (the review found no defect there) (2 000 000 draws per cell)
 Section G   the lower end of the window of means, n = 1e17 and 2^61: sharp at n p = 44   (4 000 000 draws per cell)
             (as we remember numpy's source, the last acceptance test of the rejection branch is reached only for
             20 < |y - m| < n p q / 2 - 1, which is possible only for n p q > 44; this section is the measurement)

Usage: python3 t5_numpy_binomial_scan.py          (about one minute)
"""
import sys, os, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def outfile(name):
    """Where an output goes: ../out/<name> in the scratch layout (scripts in code/, outputs in out/), and
    out_<name> next to the script in the repository (experiments/coordinator_checks/nested_review_R6/)."""
    d = os.path.join(HERE, os.pardir, "out")
    if os.path.basename(HERE) == "code" and os.path.isdir(d):
        return os.path.join(d, name)
    return os.path.join(HERE, "out_" + name)


lines = []
def out(s=""):
    print(s); lines.append(s); sys.stdout.flush()


def cell(rng, n, p, N):
    mu = n * p
    var = mu * (1 - p)
    x = rng.binomial(n, p, size=N).astype(np.float64)
    d = x - mu
    zm = d.mean() / math.sqrt(var / N)
    vr = (d * d).mean() / var
    zv = (vr - 1) / math.sqrt((2 + 1 / var) / N)
    return d.mean(), zm, vr - 1, zv


def table(title, rng, cells, N):
    out(title)
    out(f"  {'n':>22} {'n p':>12} | {'mean - n p':>11} {'z':>8} | {'var/exact - 1':>13} {'z':>8} | detected")
    ndet = 0
    for (n, p) in cells:
        b, zm, v, zv = cell(rng, n, p, N)
        det = abs(zm) > 4 or abs(zv) > 4
        ndet += det
        out(f"  {n:22d} {n * p:12.1f} | {b:11.4f} {zm:8.2f} | {v:13.5f} {zv:8.2f} | {'YES' if det else ''}")
    return ndet


def main():
    t0 = time.time()
    out(f"numpy {np.__version__}: Generator.binomial(n, p) against the exact mean and variance")
    rng = np.random.default_rng(20261126)
    A = [(n, mu / n) for n in (10 ** 12, 2 ** 50, 10 ** 15, 2 ** 53, 10 ** 16, 2 ** 54 + 12345, 10 ** 17, 10 ** 18, 2 ** 61, 2 ** 62 - 1)
         for mu in (20.0, 31.0, 45.0, 92.0, 500.0, 5000.0, 1e5)]
    table("Section A: 400 000 draws per cell", rng, A, 400000)
    B = [(n, mu / n) for n in (2 ** 31, 10 ** 10, 10 ** 11, 10 ** 12, 2 ** 40 + 7, 10 ** 13, 3 * 10 ** 13, 10 ** 14, 3 * 10 ** 14, 10 ** 15, 3 * 10 ** 15,
                               2 ** 52, 2 ** 52 + 1, 6 * 10 ** 15) for mu in (92.0, 500.0, 5000.0)]
    table("Section B: 2 000 000 draws per cell", rng, B, 2000000)
    C = [(n, mu / n) for n in (10 ** 16, 10 ** 18, 2 ** 61, 2 ** 62 - 1) for mu in (2e4, 1e5, 1e6, 1e7, 1e9)]
    table("Section C: 4 000 000 draws per cell", rng, C, 4000000)
    D = [(124 * 10 ** 12, 3.729e-11), (527 * 10 ** 12, 3.729e-11), (622 * 10 ** 12, 1.141e-10), (10 ** 15, 3.729e-11), (5049 * 10 ** 12, 3.729e-11),
         (10100 * 10 ** 12, 3.729e-11), (8761 * 10 ** 12, 1.141e-10), (1030 * 10 ** 12, 1.23e-7)]
    table("Section D: the published run's own (n, p); 8 000 000 draws per cell", rng, D, 8000000)
    E = [(2 ** 59, p) for p in (1e-15, 1e-16, 9e-17, 3e-17, 1e-17, 1e-18, 1e-20)]
    table("Section E: the cells of referee R8 (n = 2^59); 2 000 000 draws per cell", rng, E, 2000000)
    out("Section F: Generator.poisson(mu), 2 000 000 draws per cell")
    out(f"  {'mu':>12} | {'mean - mu':>11} {'z':>8} | {'var/mu - 1':>13} {'z':>8} | detected")
    for mu in (20.0, 45.0, 92.0, 500.0, 5000.0, 1e5, 1e7):
        x = rng.poisson(mu, size=2000000).astype(np.float64)
        d = x - mu
        zm = d.mean() / math.sqrt(mu / 2000000)
        vr = (d * d).mean() / mu
        zv = (vr - 1) / math.sqrt((2 + 1 / mu) / 2000000)
        out(f"  {mu:12.1f} | {d.mean():11.4f} {zm:8.2f} | {vr - 1:13.5f} {zv:8.2f} | {'YES' if abs(zm) > 4 or abs(zv) > 4 else ''}")
    G = [(n, mu / n) for n in (10 ** 17, 2 ** 61) for mu in (36.0, 40.0, 42.0, 43.0, 43.9, 44.1, 45.0, 46.0, 48.0, 52.0)]
    table("Section G: the lower end of the window of means; 4 000 000 draws per cell", rng, G, 4000000)
    out(f"({time.time() - t0:.0f} s)")
    open(outfile("t5_numpy_binomial_scan.txt"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
