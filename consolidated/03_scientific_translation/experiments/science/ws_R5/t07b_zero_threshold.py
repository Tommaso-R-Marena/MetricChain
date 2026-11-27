"""t07b_zero_threshold.py -- threshold of the ZERO residual as a limit (not a finite difference):
lim_{t->0} F(0,t)/t = min_Q max_phi E_Q[ln(pi/pi_phi)]  (a matrix game: one LP).
Derived from F(0,t) = min_Q max_phi -ln sum_a Q(a) (pi_phi(a)/pi(a))^t."""
import numpy as np
from r5lib import *
from t01_identity import sites_example

if __name__ == "__main__":
    S = sites_example()
    for nm, ref in (("path", 0.394664), ("tri", 0.283427), ("asym", 0.155521)):
        s = S[nm]
        G = (np.log(s.pi)[None, :] - s.logW)          # G[phi, a] = ln(pi(a)/pi_phi(a))
        val, Q = game_value(G)                        # min over mixtures of letters of the max over vertices
        fd = [F_game(s, np.zeros(s.q), t)[0] / t for t in (1e-2, 1e-3, 1e-4)]
        print(f"{nm:5s} zero-residual threshold (limit, LP) = {val:.6f}   theirs {ref:.6f}   diff {val-ref:+.1e};"
              f"   finite differences F(0,t)/t at t = 1e-2, 1e-3, 1e-4: {fd[0]:.6f}, {fd[1]:.6f}, {fd[2]:.6f}")
