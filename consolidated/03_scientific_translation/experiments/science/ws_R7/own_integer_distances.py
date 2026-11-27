"""R7 OWN: how many profile distances of the generic chain are exact integers (or integer multiples of 1/2)?
For each n: number of unordered pairs of distinct classes with |D - round(D)| < 1e-9, how many of them have
D = gmin(y) + eps for one of the integer-valued thresholds (a tie of the cover relation at L = 1), and the
distribution of the nearest non-integer."""
import sys
import numpy as np
import own_cover as oc

for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    cd = oc.class_data(n)
    D = oc.dist_matrix(cd["Srep"])
    N = n + 3
    C = cd["ncls"]
    iu = np.triu_indices(C, k=1)
    d = D[iu]
    frac = np.abs(d - np.rint(d))
    is_int = frac < 1e-9
    half = np.abs(2 * d - np.rint(2 * d)) < 1e-9
    near = frac[~is_int].min()
    # ties at L = 1: D[a,y] = gmin[y] + eps, eps in the integer-valued members of {0, 1, N/20, N/10, N/4, N/2}
    eps_int = sorted({e for e in (0, 1, N / 20, N / 10, N / 4, N / 2) if abs(e - round(e)) < 1e-12})
    ties = 0
    for e in eps_int:
        sl = np.abs(D - (cd["mingap"] + e)[None, :])
        np.fill_diagonal(sl, 1.0)
        ties += int((sl < 1e-9).sum())
    vals, cnts = np.unique(np.rint(d[is_int]).astype(int), return_counts=True)
    print(f"n={n} classes={C} pairs={len(d)} integer-valued distances: {int(is_int.sum())} ({is_int.mean():.2e} of pairs); "
          f"half-integer or integer: {int(half.sum())}; nearest non-integer to an integer: {near:.2e}; "
          f"integer eps values {eps_int}: ordered (centre, point) ties at L=1: {ties}; "
          f"most frequent integer values: {sorted(zip(cnts.tolist(), vals.tolist()), reverse=True)[:6]}", flush=True)
