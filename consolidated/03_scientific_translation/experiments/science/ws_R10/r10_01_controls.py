"""r10_01: controls (Y_REPORT section 2).  Own code (r10lib), written before opening theirs.
 (i) cube closed forms at u=1;  (ii) one site numerically;  (iii) 2 and 3 independent uniform
 sites as ONE super-site with all vertices of the block polytope (6, 38), additive only,
 non-additive only;  (iv) vertex counts for n=1..5;  (v) field control (0.7,0.3)."""
import time
import numpy as np
from r10lib import *

t0 = time.time()
u = 1.0
h, ts, a, E = cube_exponents(u)
print("(i) cube closed forms u=1:  h=%.7f at t*=%.4f   a=%.7f   E=%.7f" % (h, ts, a, E))


def exponents(pi, labels, per=1, name=""):
    """h (max_t F*), a, E for a label family; returns brackets divided by `per`."""
    W, _ = gibbs(pi, labels)

    def low(t):
        return renyi_bracket(W, t)["lower"]

    tbest, _ = golden_max(low, 0.05, 0.95, tol=1e-6)
    br = renyi_bracket(W, tbest)
    ca = capacity_bracket(W)
    th = threshold_bracket(W)
    print("%-46s h in [%.7f, %.7f] (t=%.4f)  a in [%.7f, %.7f]  E in [%.7f, %.7f]" % (
        name, br["lower"] / per, br["upper"] / per, tbest, ca["lower"] / per, ca["upper"] / per,
        th["lower"] / per, th["upper"] / per))
    return br, ca, th


# (ii) one site
pi1 = np.array([0.5, 0.5])
V1 = u * hom_vertices(1).astype(float)
exponents(pi1, V1, 1, "(ii) one uniform site, 2 vertices")

# (iv) counts
for n in range(1, 6):
    tt = time.time()
    V = hom_vertices(n)
    # sanity: every edge has |difference| = 1, f(0) = 0, rows distinct
    N = 1 << n
    ok = all(np.all(np.abs(V[:, v].astype(int) - V[:, v ^ (1 << i)].astype(int)) == 1)
             for v in range(N) for i in range(n))
    distinct = len(np.unique(V, axis=0)) == len(V)
    print("(iv) n=%d: %d integer height functions (all edges tight: %s, distinct: %s, f(0)=0: %s)  %.1fs"
          % (n, len(V), ok, distinct, bool(np.all(V[:, 0] == 0)), time.time() - tt))

# (iii) super-sites of independent uniform sites
for L in (2, 3):
    N = 1 << L
    piL = np.full(N, 1.0 / N)
    V = u * hom_vertices(L).astype(float)
    # additive vertices: f(x) = sum_i c_i x_i with c_i = +-1  <=> second differences vanish
    S = sitewise_labels(L) * u
    def is_additive(f):
        g = f - f[0]
        c = np.array([g[1 << i] for i in range(L)])
        lin = bits(L).astype(float) @ c
        return np.allclose(g, lin)
    add = np.array([is_additive(f) for f in V])
    print("(iii) L=%d: %d vertices, %d additive, %d non-additive" % (L, len(V), add.sum(), (~add).sum()))
    br, ca, th = exponents(piL, V, L, "      all vertices, per site")
    # weight of the optimal M on non-additive vertices
    print("      weight on non-additive vertices: Renyi %.2e, capacity %.2e, threshold %.2e"
          % (br["M"][~add].sum(), ca["M"][~add].sum(), th["M"][~add].sum()))
    exponents(piL, V[add], L, "      additive vertices only, per site")
    exponents(piL, V[~add], L, "      non-additive vertices only, per site")
    # cross-check: my sitewise_labels() gives the same family as the additive vertices
    exponents(piL, S, L, "      sitewise_labels(), per site")

# (v) field control
exponents(np.array([0.7, 0.3]), V1, 1, "(v) field control (0.7,0.3), one site")
# unequal weights: number of vertices for slopes (1.847, 1, 1.847) (Y_REPORT section 2: 120)
Vw = cube_vertices_weighted([1.847, 1.0, 1.847])
print("(vi) weighted cube slopes (1.847,1,1.847): %d vertices; (1,1,1): %d; (1.5,1): %d"
      % (len(Vw), len(cube_vertices_weighted([1.0, 1.0, 1.0])), len(cube_vertices_weighted([1.5, 1.0]))))
print("time %.1fs" % (time.time() - t0))
