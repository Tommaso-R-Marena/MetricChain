"""R6-T5, second pass (after SCI-RES-0012, section 1, and ENG-RES-0013, section 1.1): where does the defect of numpy's
Generator.binomial(n, p) begin?  Our first scan (t5_numpy_binomial_scan.py) jumped from n = 10^12 to n = 2^50 -- a
power of two, which both other divisions find clean -- and then to 10^15, and so reported "begins near 10^15".  This
scan fills the gap with generic numbers of trials.  4 000 000 draws per cell; z-scores of the sample mean and of the
sample variance against the exact binomial values (the variance of the sample variance from the exact fourth
central moment).  Fixed seed; standard library and numpy only."""
import math
import sys
import numpy as np

OUT = open(sys.argv[1], "w") if len(sys.argv) > 1 else None


def out(s):
    print(s)
    if OUT:
        OUT.write(s + "\n")


def cell(rng, n, mean, N=4_000_000):
    p = mean / n
    x = rng.binomial(n, p, size=N).astype(np.float64)
    var = n * p * (1 - p)
    mu4 = var * (1 + 3 * (n - 2) * p * (1 - p))                 # fourth central moment of Bin(n, p)
    zm = (x.mean() - mean) / math.sqrt(var / N)
    s2 = x.var(ddof=1)
    zv = (s2 - var) / math.sqrt((mu4 - var * var) / N)
    return zm, zv, s2 / var - 1


def main():
    rng = np.random.default_rng(20261126)
    out(f"numpy {np.__version__}: Generator.binomial(n, mean/n), 4 000 000 draws per cell; z of the mean / z of the variance (relative error of the variance)")
    ns = [(10 ** 14, "1e14"), (2 * 10 ** 14, "2e14"), (3 * 10 ** 14, "3e14"), (4 * 10 ** 14, "4e14"), (5 * 10 ** 14, "5e14"),
          (7 * 10 ** 14, "7e14"), (9 * 10 ** 14, "9e14"), (10 ** 15, "1e15"), (2 ** 50, "2^50"), (2 ** 50 + 1, "2^50+1"),
          (2 ** 52, "2^52"), (3 * 10 ** 15, "3e15"), (2 ** 53, "2^53")]
    means = [29.0, 92.0, 500.0, 5000.0]
    out(f"{'n':>8} | " + " | ".join(f"{'mean ' + str(int(m)):>26}" for m in means) + " | defective")
    first_bad = None
    for n, label in ns:
        row, bad = [], False
        for m in means:
            zm, zv, rel = cell(rng, n, m)
            flag = abs(zm) > 5 or abs(zv) > 5
            bad = bad or flag
            row.append(f"{zm:+6.1f} / {zv:+6.1f} ({100 * rel:+.2f} %)" + ("*" if flag else " "))
        if bad and first_bad is None:
            first_bad = label
        out(f"{label:>8} | " + " | ".join(f"{r:>26}" for r in row) + " | " + ("YES" if bad else ""))
    out(f"first number of trials on this grid with a z-score above 5: {first_bad}")


if __name__ == "__main__":
    main()
