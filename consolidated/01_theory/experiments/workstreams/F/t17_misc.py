"""t17: (a) the cosh form of the two-state game value; (b) mutation of the recursion: the pair of the instance g = 0
alone converges to R_0, below the lower bound R^max of the hardest additive instance; (c) the nested scheme with plain
sampling of pi: exponent theta_h^pi = max_m min{ I + KL(P_X||pi) : u P(X != S) - Lam <= e } against R^max and R_0;
(d) the second level at vanishing accuracy."""
import math, numpy as np, time
from flib import *
from recursion import Recursion
t0 = time.time()
rng = np.random.default_rng(17)

# (a)  F(t) = ln{ [sinh(t b/2) C(lam-a)^t + sinh(t a/2) C(lam+b)^t] / sinh(t(a+b)/2) } - t ln C(lam),  C(x) = 2 cosh(x/2),
#      lam = theta + gamma (total field), a = u + gamma, b = u - gamma
worst = 0.0
for _ in range(5000):
    p = rng.uniform(0.02, 0.98); u = rng.uniform(0.1, 5); g = rng.uniform(-u, u); t = rng.uniform(1e-3, 1.0)
    theta = math.log((1 - p) / p)
    lam, a, b = theta + g, u + g, u - g
    C = lambda x: 2 * math.cosh(x / 2)
    val = math.log((math.sinh(t * b / 2) * C(lam - a) ** t + math.sinh(t * a / 2) * C(lam + b) ** t) / math.sinh(t * (a + b) / 2)) - t * math.log(C(lam))
    worst = max(worst, abs(val - float(F_game(p, u, g, t))))
print("(a) cosh form vs closed game formula: max abs error", worst)

for p, u in ((0.1, 2.0), (0.3, 1.0)):
    st = Site(p, u)
    wp = WorstPair(p, u)
    w0 = WorstPair(p, u, gam_fixed=0.0)
    # (b) mutation: recursion with the pair of g = 0 alone
    r = Recursion(w0.theta_na, w0.R, w0.a, w0.h, w0.E)
    for k in range(2, 11):
        r.step()
    below = float(np.max(np.array([float(wp.R(g)) for g in r.g]) - r.T)) / wp.a
    print(f"(b) p={p} u={u}: recursion built on the pair of g = 0 alone: after 10 levels max(R^max - T_10)/a = {below:.4f} > 0"
          f"  (it falls below the lower bound of the hardest additive instance: such an accounting is refuted)")
    # (c) nested scheme with plain sampling of pi
    print(f"(c) p={p} u={u}:   e/E      R_0       R^max     theta_h^pi (hinted exponent of g=0 with the sampler pi)")
    for frac in (0.0, 0.25, 0.5, 0.75):
        e = frac * wp.E
        thpi = maxmin_J(st, "hint0", e)[0]
        print(f"                  {frac:4.2f}   {float(w0.R(e)):.6f}  {float(wp.R(e)):.6f}  {thpi:.6f}")
    # (d) second level at vanishing accuracy
    phis = np.linspace(0.01, 0.99, 981)
    t2 = min(max((1 - f) * wp.a, f * wp.a + (1 - f) * wp.theta_na(f * wp.a / (1 - f))) for f in phis)
    print(f"(d) p={p} u={u}: T_2(0+)/a = {t2 / wp.a:.4f}   (h/a = {wp.h / wp.a:.4f})")
print("time", time.time() - t0)
