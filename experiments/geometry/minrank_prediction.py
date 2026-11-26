"""Generic prediction for the degree D at which the rank conditions certify and demix
(docs/geometry/ENSEMBLE_RIGIDITY.md, section 6.2; sent to the Complexity division).

The coordinate ring of the symmetric N x N matrices of rank <= 3 has Hilbert function
    HF_X(D) = sum over partitions lambda of D with at most 3 parts of dim S_{2 lambda}(C^N)
(the decomposition Sym(Sym^2 V) = sum of S_{2 lambda} V; the ideal of rank <= 3 is the sum over
lambda with more than 3 parts).  The space L is cut out of Sym(N) by 2n - 4 linear conditions
(the 2n - 3 values e^T P e / l_e^2 are equal).  If these behaved like generic linear forms on
the ring ("maximal rank"), the Hilbert function of the section would be given by the
coefficients of  HS_X(t) (1 - t)^(2n-4)  up to the first non-positive one, and zero from there
on; for a planted mixture the value K takes the place of 0.  So the PREDICTED threshold of
the degree-D certificate is

    n_D(K) = min { n : [t^d] HS_X(t) (1 - t)^(2n-4) <= 0 for some d <= D },      N = 3K,

subject to the structural obstruction n >= 6K - 1 (Proposition 6.2 (f)).  This is a heuristic,
not a theorem: the linear conditions of a chain are not generic.  It reproduces the computed
thresholds for K = 2, 3 at D = 4.  Standard library only.
"""
import sys
from fractions import Fraction
from math import comb


def partitions(D, maxparts, maxpart=None):
    maxpart = D if maxpart is None else maxpart
    if D == 0:
        yield ()
        return
    if maxparts == 0:
        return
    for first in range(min(D, maxpart), 0, -1):
        for rest in partitions(D - first, maxparts - 1, first):
            yield (first,) + rest


def schur_dim(shape, N):
    """dim S_shape(C^N) by the hook-content formula."""
    val = Fraction(1)
    cols = [sum(1 for r in shape if r > j) for j in range(shape[0])] if shape else []
    for i, row in enumerate(shape):
        for j in range(row):
            hook = (row - j - 1) + (cols[j] - i - 1) + 1
            val *= Fraction(N + j - i, hook)
    assert val.denominator == 1
    return int(val)


def HF_X(D, N):
    return sum(schur_dim(tuple(2 * p for p in lam), N) for lam in partitions(D, 3))


def coefficient(D, N, c, hf):
    return sum((-1) ** j * comb(c, j) * hf[D - j] for j in range(D + 1))


def h_vector(N):
    """h-vector of the coordinate ring (Cohen-Macaulay, dimension 3N - 3): HS_X(t) (1 - t)^(3N-3).
    Its degree is the Castelnuovo-Mumford regularity; its sum is the degree of the variety."""
    dim, Dmax = 3 * N - 3, 3 * N
    hf = [HF_X(D, N) for D in range(Dmax + 1)]
    h = [coefficient(D, N, dim, hf) for D in range(Dmax + 1)]
    while h and h[-1] == 0:
        h.pop()
    return h


def harris_tu_degree(N, r=3):
    """Degree of the symmetric N x N matrices of rank <= r (Harris-Tu)."""
    val = Fraction(1)
    for a in range(N - r):
        val *= Fraction(comb(N + a, N - r - a), comb(2 * a + 1, a))
    assert val.denominator == 1
    return int(val)


def main():
    Dmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    Kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    assert HF_X(4, 9) == comb(48, 4) - 5292 and HF_X(4, 6) == comb(24, 4) - 105
    # independent check of the Hilbert function: the h-vector sums to the Harris-Tu degree
    regs = []
    for K in range(2, min(Kmax, 6) + 1):
        h = h_vector(3 * K)
        assert all(v > 0 for v in h) and sum(h) == harris_tu_degree(3 * K), K
        regs.append((K, len(h) - 1, sum(h)))
    assert regs[0] == (2, 6, 112)
    print("regularity and degree of the symmetric 3K x 3K matrices of rank <= 3: "
          + "; ".join(f"K = {K}: {reg}, {deg}" for K, reg, deg in regs))
    print("predicted thresholds n_D(K) of the degree-D certificate (generic linear sections; heuristic)")
    print(f"{'K':>3} {'4.5K+1':>7} {'6K-1':>6} " + " ".join(f"{'D='+str(D):>7}" for D in range(4, Dmax + 1)) + f" {'conic':>7}")
    for K in range(2, Kmax + 1):
        N = 3 * K
        hf = [HF_X(D, N) for D in range(Dmax + 1)]
        conic = -(-(9 * K * K + K + 8) // 4)
        row = []
        for D in range(4, Dmax + 1):
            n = 4
            while n < conic and all(coefficient(d, N, 2 * n - 4, hf) > 0 for d in range(4, D + 1)):
                n += 1
            row.append(n)
        print(f"{K:>3} {int(4.5 * K) + 1:>7} {6 * K - 1:>6} " + " ".join(f"{n:>7}" for n in row) + f" {conic:>7}")
    print("observed (demix4.py, all minors): K = 2: 11; K = 3: 17; K = 4: h_4 = 4 at n = 34, 36, 38")


if __name__ == "__main__":
    main()
