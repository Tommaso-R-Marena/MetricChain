#!/usr/bin/env python3
"""R22 Item 2: 'what happens at a state where the chain is singular?'  For chains there is none: the rigidity matrix of
E0 (bonds and 1-3 pairs) has full row rank 2n-3 at EVERY conformation with bond angle in (0, pi) (each atom is attached
to its two predecessors by two non-parallel edges), so C is a smooth manifold and its tangent space is the flex space.
Check: smallest singular value of the rigidity matrix (relative) on random, planar (torsions 0/pi), helical and
nearly straight chains; dimension of the flex space = n + 3 = (n - 3) torsions + 6 isometries.
Control: with the bond angle at pi - 1e-9 (degenerate geometry) the smallest singular value must collapse.
Run: OMP_NUM_THREADS=1 python3 -B t2_rigidity_rank.py > t2_rigidity_rank.log
"""
import numpy as np, time
import r22lib as L
t0 = time.time(); rng = np.random.default_rng(2330); viol = 0


def rigidity(X):
    n = len(X); E = L.E0(n); R = np.zeros((len(E), 3 * n))
    for r, (i, j) in enumerate(E):
        R[r, 3 * i:3 * i + 3] = X[i] - X[j]; R[r, 3 * j:3 * j + 3] = X[j] - X[i]
    return R


print("| chain | n | cos(bond angle) | rows 2n-3 | rank | smallest/largest singular value | flex dimension 3n - rank | n + 3 |")
print("|---|---|---|---|---|---|---|---|")
for name, gen in (("random", lambda n: rng.uniform(-np.pi, np.pi, n - 3)), ("planar zigzag (all pi)", lambda n: np.full(n - 3, np.pi)),
                  ("planar (0/pi random)", lambda n: rng.choice([0.0, np.pi], n - 3)), ("helix (all 1.0)", lambda n: np.full(n - 3, 1.0)),
                  ("all cis (all 0)", lambda n: np.zeros(n - 3))):
    for n in (6, 14, 30):
        for cosang in (-1.0 / 3.0, -0.95, 0.5):
            if name == "all cis (all 0)" and n > 6:
                continue            # self-intersecting ring; still a point of C but skip the long ones
            X = L.chain(gen(n), cosang); s = np.linalg.svd(rigidity(X), compute_uv=False)
            rank = int((s > 1e-10 * s[0]).sum()); ok = rank == 2 * n - 3
            viol += int(not ok)
            print(f"| {name} | {n} | {cosang:+.2f} | {2 * n - 3} | {rank} | {s[-1] / s[0]:.2e} | {3 * n - rank} | {n + 3} |" + ("" if ok else "  <-- rank deficient"))
X = L.chain(rng.uniform(-np.pi, np.pi, 11), np.cos(np.pi - 1e-9)); s = np.linalg.svd(rigidity(X), compute_uv=False)
print(f"control: bond angle pi - 1e-9, n = 14: smallest/largest singular value {s[-1] / s[0]:.2e} (must collapse: degenerate geometry)")
viol += int(s[-1] / s[0] > 1e-6)
print(f"violations: {viol}")
print(f"ALL DONE {time.time() - t0:.1f} s")
