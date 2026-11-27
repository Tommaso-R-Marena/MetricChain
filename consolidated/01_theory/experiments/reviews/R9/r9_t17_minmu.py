# R9 test 17: the least point mass of mu_H (it governs the number of potential outer points, 4K/min mu_H, in Theorem F7):
#   -ln min_x mu_H(x) = n c_1 + ln Z_H,   c_1 = ln 2 if |theta| <= u,   c_1 = ln(1 + e^{|theta|-u}) > ln 2 if |theta| > u.
import numpy as np
from math import log, exp
from r9lib import Par
from r9prof import Grid
for (p, u) in [(0.3, 1.0), (0.2, 4.0), (0.5, 1.0), (0.1, 2.0), (0.05, 2.0), (0.01, 1.0), (0.95, 1.0)]:
    P = Par(p, u); th = P.theta
    c1 = log(2.0) if abs(th) <= u else log(1 + exp(abs(th) - u))
    for n in (50, 400):
        gr = Grid(P, (n // 2, n - n // 2)); tt = np.arange(n + 1.0)
        lnmu = tt * log(P.p) + (n - tt) * log(P.q) - gr.psiH_t - gr.lnZH      # ln mu_H(x) for x of type t
        print(f"p={p} u={u} theta={th:+.3f} n={n}: -ln(min mu_H) = {-lnmu.min():.4f};  n c_1 + ln Z_H = {n*c1 + gr.lnZH:.4f}  (c_1 = {c1:.4f}, ln 2 = {log(2):.4f}); "
              f"union bound of Theorem 11.52 void for phi > ln2/c_1 = {min(1.0, log(2)/c1):.3f}")
