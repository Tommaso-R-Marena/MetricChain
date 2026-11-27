#!/usr/bin/env python3
"""R4 -- Lemma 11.85 against the EXACT optimum over two-round algorithms with batches (1, 1).

With M1 = 1 every first batch is equivalent by translation (B1 = {0}); with M2 = 1 the best second
point for each posterior class is found exactly (arg max of the coverage).  So
   opt(1,1) = max over deterministic two-round algorithms with one point per batch of
              #{centres s : the transcripts on psi_{D,s} and psi_{S,s} differ} / 2^n
is computed exactly (randomisation cannot beat the best deterministic algorithm), and must be
<= p1 + p2 by the lemma.  For M2 = k > 1 the greedy value is a lower bound on the optimum.
"""
import numpy as np
from twins_exact import Twins
from small_cube import cube_tables, distinguisher

print("# (n1,n2,u,T) | p1 | p2 | exact optimum (1,1) | bound p1+p2 | ratio || greedy (1,k), k=2,4,8: value/bound")
for (n1, n2, u, T) in [(6, 6, 1.0, 4.0), (6, 8, 1.0, 5.5), (7, 7, 2.0, 4.8), (5, 9, 1.0, 6.0), (4, 10, 1.0, 6.5),
                       (6, 8, 3.0, 5.5), (8, 6, 0.5, 4.1)]:
    tw = Twins(n1, n2, u, T)
    n = n1 + n2
    N = 1 << n
    PsiD, PsiS, G1, d1, d2 = cube_tables(tw)
    p1 = float((~tw.W1[d1, d2]).mean())
    p2 = float((~tw.W2[d2]).mean())
    B1 = np.array([0], dtype=np.int64)
    a, b, ncl = distinguisher(PsiD, PsiS, n, B1, 1)
    opt = (a + b) / N
    extra = []
    for k in (2, 4, 8):
        a2, b2, _ = distinguisher(PsiD, PsiS, n, B1, k)
        extra.append(f"{(a2 + b2) / N:.5f}/{p1 + k * p2:.5f}")
    print(f"({n1},{n2},{u},{T}) | {p1:.5f} | {p2:.5f} | {opt:.5f} | {p1 + p2:.5f} | {opt / (p1 + p2):.3f} || "
          + "  ".join(extra) + f"   (posterior classes: {ncl}; violated: {opt > p1 + p2 + 1e-12})")
