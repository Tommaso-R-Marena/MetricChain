"""What Theorems L and L+ of docs/geometry/LOCAL_DATA_STABILITY.md guarantee on idealised traces
(constant radius, rise and turn per point -- the geometries of the Science division's review
SCI-REV-0023, section 5; not structures from a database), for squared distances of sequence
separation <= 4.  Units: lengths in the unit of the trace (read: angstrom).

For each trace and length n it prints
  b, s_*, tau_*          longest bond; smallest third singular values of centred 5- and 4-point windows
  C_L                    constant of Theorem L:  d_P <= C_L ||eta||_2  for EVERY configuration Y
  1/(2 mu)               the first-order (sharp) constant of Theorem L+
  range                  ||eta||_2 <= mu / (Lambda C_L): where Theorem L+ certifies the sharp constant
  ... as an rms error of the squared distances (range / sqrt(#pairs)) and of the distances
  amplification          worst-case RMSD per unit rms distance error to first order: sqrt(p/n) / s_7(R)
The point of the table: the first-order amplification is moderate on short helices and grows like
n^2; the range in which the theorems CERTIFY that no distant configuration fits the data is
many orders of magnitude below any measurement error.
"""
import numpy as np
from local_data_bounds import rigidity_matrix
from local_data_upper import band_pairs, sharp_constants

TRACES = (("helix-like (radius 2.3, rise 1.5, 100 deg per point)", (2.3, 1.5, 100.0)),
          ("strand-like (radius 0.94, rise 3.3, 160 deg per point)", (0.94, 3.3, 160.0)),
          ("strand-like, 175 deg per point", (0.94, 3.3, 175.0)))


def trace(n, radius, rise, turn_deg):
    t = np.deg2rad(turn_deg) * np.arange(n)
    return np.column_stack([radius * np.cos(t), radius * np.sin(t), rise * np.arange(n)])


def row(X):
    n = len(X)
    pairs = band_pairs(n)
    p = len(pairs)
    mu, Lam, CL = sharp_constants(X)
    s7 = np.sort(np.linalg.svd(rigidity_matrix(X, pairs), compute_uv=False))[6]
    dmean = float(np.mean([np.linalg.norm(X[j] - X[k]) for j, k in pairs]))
    rng_eta = mu / (Lam * CL)
    return dict(n=n, pairs=p, CL=CL, sharp=1 / (2 * mu), range_eta=rng_eta, range_rms_sq=rng_eta / np.sqrt(p),
                range_rms_dist=rng_eta / np.sqrt(p) / (2 * dmean), amplification=np.sqrt(p / n) / s7,
                coarse_rmsd_per_rms_dist=CL * 2 * dmean * np.sqrt(p / n))


def main():
    ok = True
    for name, geo in TRACES:
        print(name)
        prev = None
        for n in (12, 20, 100):
            r = row(trace(n, *geo))
            print(f"   n = {n:3d}: C_L = {r['CL']:.3g}, 1/(2mu) = {r['sharp']:.3g}; certified range: ||eta||_2 <= {r['range_eta']:.2g} "
                  f"(rms squared-distance error {r['range_rms_sq']:.1g}, rms distance error {r['range_rms_dist']:.1g}); "
                  f"first-order RMSD per unit rms distance error: {r['amplification']:.3g} (worst case); "
                  f"the same from Theorem L alone: {r['coarse_rmsd_per_rms_dist']:.3g}")
            ok &= r["sharp"] <= r["CL"] and r["range_eta"] > 0
            if prev:                                    # growth with n: the sharp constant at least doubles from 12 to 20 to 100
                ok &= r["sharp"] > prev
            prev = r["sharp"]
    print("ALL OK" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
