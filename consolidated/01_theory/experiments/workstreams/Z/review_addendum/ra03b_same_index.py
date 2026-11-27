#!/usr/bin/env python3
"""RA03b -- the sentence after Theorem Z' ("by Corollary A4 the envelope schedule has the smaller b_k at every k"):
the envelope tops (start b_0 = a) against the cut-curve tops of Z_REPORT (start b_0 = h + eps1; s_t = L + 0.05) AT THE SAME INDEX k.
Corollary A4 gives b_{k1+i} <= bcut_i (k1 = first level with b_k <= h + eps1), not b_k <= bcut_k.
Usage: python3 -B ra03b_same_index.py
"""
import ra_lib as R

for name, P, eps1 in (("cube u = 1", R.Cube(1.0).setup(), 0.003), ("Gaussian pair", R.Gauss().setup(), 0.02)):
    a, h, L = P.a, P.h, P.L
    S = R.EnvSeq(P, 70)
    st, b0 = L + 0.05, h + eps1
    cuts = []
    for j in range(62):
        if P.orbit_with_slope(b0, j)[0] <= st:
            cuts.append(None)
        else:
            lo, hi = h, b0
            for _ in range(100):
                mid = 0.5 * (lo + hi)
                if P.orbit_with_slope(mid, j)[0] <= st:
                    lo = mid
                else:
                    hi = mid
            cuts.append((lo, P.orbit_with_slope(lo, j)[1]))
    bc = [b0]
    for j in range(61):
        cj = cuts[j]
        bc.append(bc[j] if cj is None else min(bc[j], cj[0] + (1 - st - cj[0] / a) / (cj[1] + 1 / a)))
    k1 = next(k for k in range(71) if S.b[k] <= b0)
    print("# %s, s_t = L + 0.05, eps1 = %g:  k1 = %d" % (name, eps1, k1))
    print("#   k    (b_k - h)/h  envelope     (bcut_k - h)/h  cut curves     envelope smaller at the same k?     b_{k1+k} <= bcut_k (Corollary A4)?")
    for k in list(range(0, 13)) + [15, 20, 30, 40, 60]:
        print("  %3d      %.6f               %.6f                    %-5s                              %s"
              % (k, (S.b[k] - h) / h, (bc[k] - h) / h, S.b[k] <= bc[k], S.b[k1 + k] <= bc[k] if k1 + k <= 70 else "-"))
    bad = [k for k in range(0, 61) if S.b[k] > bc[k]]
    print("  indices k <= 60 at which the envelope top is LARGER than the cut top: %s\n" % bad)
