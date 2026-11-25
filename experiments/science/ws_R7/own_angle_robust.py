"""R7 OWN: are the equalities that define the profile classes of the generic chain exact (polynomial identities in
c = -cos(theta)), or accidents of the bond angle 111 degrees?

Every squared distance is a polynomial in c with rational coefficients (R7_REPORT, Proposition G1), so two distances
that are equal as polynomials are equal at EVERY bond angle, whereas two distinct polynomials that merely coincide at
111 degrees to 1e-14 separate when the angle is changed.  Test: recompute the enumeration and the class partition at
theta = 111 + delta for several small delta (small enough that every hard-core and cutoff decision keeps its sign) and
compare (i) the accepted torsion words, (ii) the partition of the words into classes.
"""
import math, sys
import numpy as np
import own_gen as og

def partition(n, theta_deg):
    og.THETA = math.radians(theta_deg)
    # coords_from_words has theta as a default argument bound at import time: rebind
    og.coords_from_words.__defaults__ = (og.THETA, og.PHIS)
    words = og.enumerate_words(n)
    S = og.truncated_sorted_sq(words)
    cid, ncls, info = og.profile_classes(S)
    return words, cid, ncls, info

def canon(cid):
    """canonical relabelling of a partition: class id = index of first occurrence"""
    first = {}
    return np.array([first.setdefault(int(c), len(first)) for c in cid])

if __name__ == "__main__":
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        w0, c0, k0, i0 = partition(n, 111.0)
        ref = canon(c0)
        line = f"n={n} conf={len(w0)} classes={k0}:"
        for d in (-0.02, -0.007, 0.003, 0.011, 0.03):
            w, c, k, info = partition(n, 111.0 + d)
            same_words = (w.shape == w0.shape) and bool((w == w0).all())
            same_part = same_words and bool((canon(c) == ref).all())
            line += f"  [{d:+.3f} deg: words {'same' if same_words else 'DIFFERENT'}, classes {k}, partition {'same' if same_part else 'DIFFERENT'}, min gap between distinct values {info['min_gap_between_clusters']:.1e}]"
        print(line, flush=True)
    partition(5, 111.0)
