"""
Third-order interface with a PAIRWISE lower model (so that the theory's pairwise kernel applies).

For a product domain, centre x0, anchored order-2 interpolant I_2 g (g on the Hamming-2 ball) and
third-order constants c_T:   |g(x) - I_2 g(x)| <= sum_{T subset S(x), |T|=3} c_T   (theory report
Thm 11.18, `higherOrder_remainder`)   <= sum_{i in S(x)} gamma_i,   gamma_i := (1/3) sum_{T contains i} c_T
(every triple inside S is counted three times a third; the other triples only add).
So  L3(x) = f(x) + I_2 g(x) - sum_i gamma_i [x_i != x0_i]  is a pairwise lower model of E, and
U3 = f + I_2 g + sum_i gamma_i [..] a pairwise upper model.  This script evaluates, by enumeration,
the accuracy eps certified by the ball with the PAIRWISE models, the free-energy bracket, and the
"third-order row-sum condition" gamma_i <= single-site excitation energies.

usage: python3 -B an_ball_pairwise.py TAG TAU [RESIDUAL]
"""
import sys, json, os
import numpy as np
from anlib import *
from an_main import pruned_product, subselect

tag, tau = sys.argv[1], sys.argv[2]
rname = sys.argv[3] if len(sys.argv) > 3 else "GB"
r = json.load(open(os.path.join(HERE, "out", f"an_{tag}_tau{float(tau):.2f}.json")))
d0 = load_fb(tag)
d = restrict(d0, float(tau)) if float(tau) > d0["tau_enum"] + 1e-12 else d0
if not (d["s2min"] > float(tau)).all():
    d = subselect(d, pruned_product(d, float(tau)))
shape = d["shape"]; n = len(shape)
assert list(shape) == r["shape_pruned"]
R = residuals(d); f = R["f"]; g = R[rname]; E = f + g
c3 = r[f"Xp|{rname}"]["c3"]
gam = np.zeros(n)
for key, v in c3.items():
    for i in key.split(","):
        gam[int(i)] += v / 3.0
x0 = tuple(int(v) for v in np.unravel_index(np.argmin(E), shape))
a2 = anchored2(g, x0)
pen = weighted_hamming(shape, x0, gam)
L3 = f + a2 - pen; U3 = f + a2 + pen
X = np.ones(shape, dtype=bool)
Hm = hamming(shape, x0)
eps = float(E[Hm <= 2].min() - L3.min())
exc = []
for i in range(n):
    idx = list(x0); idx[i] = slice(None)
    line = np.delete(E[tuple(idx)] - E[x0], x0[i])
    exc.append(float(line.min()) if line.size else float("inf"))
nball = 1 + sum(k - 1 for k in shape) + sum((shape[i] - 1) * (shape[j] - 1) for i in range(n) for j in range(i + 1, n))
print(f"{tag} tau {tau} {rname}: X' {int(np.prod(shape))}, ball {nball} evaluations; gamma_i = {np.round(gam, 4)} (sum = Gamma = {gam.sum():.4f}); "
      f"min excitation energies {np.round(exc, 3)}; third-order row-sum condition gamma_i <= excitation: {bool((gam <= np.array(exc)).all())}; "
      f"remainder max |g - I2g| = {np.abs(g - a2).max():.4f} <= max penalty {pen.max():.4f}; "
      f"pairwise lower model certifies min E to within eps = {max(eps, 0):.4f} kcal/mol; "
      f"free-energy bracket ln Z(L3) - ln Z(U3) = {lnZ(L3, X) - lnZ(U3, X):.4f} nats (<= 2 beta Gamma = {2 * BETA * gam.sum():.3f})")
