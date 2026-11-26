"""The limiting best centre type on a type class (an answer to the Computational Research Division, ENG-RES-0012:
"if the limiting centre type is known to you, please say whether 0.455 and 0.405 agree with it").

On the type class of density kappa, at slope u and vanishing accuracy, the hinted exponent around a centre of type m
is V_binary(m, kappa, u, 0) of slice_lib.py (theory report Theorem 11.90, closed forms).  This script maximises it
over the centre type (a grid of 961 values, then golden section) and prints the maximiser, the maximum, the value
with the centre in the class (m = kappa), and the range of centre types within 1e-5 and 1e-4 of the maximum.

Run from the repository root:  python3 experiments/coordinator_checks/slices/centre_type.py
"""
import sys, math
sys.path.insert(0, "experiments/coordinator_checks/slices")
import numpy as np
import slice_lib as sl

u, e = 1.0, 0.0
for kappa in (0.5, 0.4, 0.3, 0.2):
    ms = np.linspace(0.02, 0.98, 961)
    vals = [sl.V_binary(m, kappa, u, e) for m in ms]
    i = int(np.argmax(vals))
    # refine by golden search around the best grid point
    a, b = ms[max(i - 2, 0)], ms[min(i + 2, len(ms) - 1)]
    _, m_star = sl.golden(lambda m: -sl.V_binary(m, kappa, u, e), a, b, tol=1e-12)
    v_star = sl.V_binary(m_star, kappa, u, e)
    v_in = sl.V_binary(kappa, kappa, u, e)
    # flatness: range of m with value within 1e-5 and 1e-4 of the maximum
    close5 = [m for m, v in zip(ms, vals) if v > v_star - 1e-5]
    close4 = [m for m, v in zip(ms, vals) if v > v_star - 1e-4]
    print(f"kappa={kappa}: m*={m_star:.5f}  V*={v_star:.6f}  V(centre in class)={v_in:.6f}  diff={v_star - v_in:.6f}"
          f"  within 1e-5: [{min(close5):.3f}, {max(close5):.3f}]  within 1e-4: [{min(close4):.3f}, {max(close4):.3f}]")
    # the complement symmetry: centre type m and 1 - m
    print("    V(1-m*) =", round(sl.V_binary(1 - m_star, kappa, u, e), 6), " V(0.5) =", round(sl.V_binary(0.5, kappa, u, e), 6))
