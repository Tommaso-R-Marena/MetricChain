#!/usr/bin/env python3
"""R22 Item 3(c): three differing torsions -- direct check of the paper argument.
The restriction of a linear image to the first three segments is one of the 8 explicit images of the two-torsion
problem (G determined by (rho1, rho2)); it is a chain on the fourth segment iff B_4 = I + G (Q_4 - I) is orthogonal.
For each of the 6 spurious candidates the defect ||B_4^T B_4 - I||_F is printed (must be > 0: the candidate fails);
for the two states it must be ~1e-15.  Also printed: the facts used in the uniqueness proof for two torsions --
rank of {I, Q3, R1 s, s R2} (must be 4) and ||Q3 - Q3^T|| (must be > 0).
Run: OMP_NUM_THREADS=1 python3 -B t3c_three_torsion_candidates.py > t3c_three_torsion_candidates.log
"""
import time
import numpy as np
import r22lib as L
t0 = time.time(); COS = -1.0 / 3.0


def rot(axis, ang):
    a = axis / np.linalg.norm(axis); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)


print("| n | hinges | thetas | rank{I, Q3, R1 s, s R2} | ||Q3 - Q3^T|| | defect of B_4 for the two states | smallest defect of B_4 over the 6 spurious candidates | all six defects |")
print("|---|---|---|---|---|---|---|---|")
viol = 0
for i, (n, hinges, half) in enumerate(((20, [4, 9, 14], False), (26, [5, 12, 19], False), (26, [6, 11, 18], False), (32, [7, 15, 23], False),
                                        (18, [3, 7, 11], False), (26, [5, 12, 19], True))):
    rng = np.random.default_rng(2320 + i)
    t1 = rng.uniform(-np.pi, np.pi, n - 3); X1 = L.chain(t1, COS)
    th = np.array([np.pi] * 3) if half else rng.uniform(0.5, 2.6, 3) * rng.choice([-1, 1], 3)
    b = [X1[h + 2] - X1[h + 1] for h in hinges]
    R = [rot(b[j], th[j]) for j in range(3)]
    Q2, Q3, Q4 = R[0], R[0] @ R[1], R[0] @ R[1] @ R[2]
    e = np.cross(b[0], b[1]); e /= np.linalg.norm(e); s = np.eye(3) - 2 * np.outer(e, e); I3 = np.eye(3)
    pred = [(I3, I3), (R[0], R[1]), (R[0], s), (I3, s @ R[1]), (s, R[1]), (R[0] @ s, I3), (R[0] @ s, s @ R[1]), (s, s)]
    defects = []
    for (r1, r2) in pred:
        # G from B2 = r1 = I + G(Q2 - I), B3 = r1 r2 = I + G(Q3 - I): least squares on the stacked 3x6 system
        A = np.hstack([Q2 - I3, Q3 - I3])            # G @ A = [r1 - I, r1 r2 - I]
        Bm = np.hstack([r1 - I3, r1 @ r2 - I3])
        G = Bm @ np.linalg.pinv(A)
        cons = np.abs(G @ A - Bm).max()              # consistency of the candidate on the first three segments
        B4 = I3 + G @ (Q4 - I3)
        defects.append((np.linalg.norm(B4.T @ B4 - I3), cons))
    rk = np.linalg.matrix_rank(np.array([I3.ravel(), Q3.ravel(), (R[0] @ s).ravel(), (s @ R[1]).ravel()]), tol=1e-9)
    asym = np.linalg.norm(Q3 - Q3.T)
    d_true = max(defects[0][0], defects[1][0]); d_sp = [d[0] for d in defects[2:]]
    cons = max(d[1] for d in defects)
    ok = d_true < 1e-12 and min(d_sp) > 1e-3 and cons < 1e-12 and (half or (rk == 4 and asym > 1e-3))
    viol += int(not ok)
    print(f"| {n} | {hinges} | " + ", ".join(f"{t:+.3f}" for t in th) + f" | {rk} | {asym:.3f} | {d_true:.1e} | {min(d_sp):.3f} | " + ", ".join(f"{d:.3f}" for d in d_sp) + " |"
          + ("" if ok else "  <-- unexpected"))
print(f"violations: {viol}   (max inconsistency of a candidate on the first three segments must be ~1e-15)")
print(f"ALL DONE {time.time() - t0:.1f} s")
