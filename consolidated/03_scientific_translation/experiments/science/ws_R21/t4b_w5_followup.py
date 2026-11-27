"""T4b - follow-up of logs/t4_W5_K1_run1.log, instance 0: a positive local minimum f = 5.9e-09 of the K = 1
certificate f(p) = sum_e (t_e(p) - t_e(x))^2 at shape distance D = 0.635 from x.  Converged positive minimum,
or an unconverged second realisation of the same eight lengths?  Same generator/draw order as t4_certificate.py."""
import numpy as np
from r21_common import *
name, K, seed = "W5", 1, 2104
rng = np.random.default_rng(seed)
N, E = graph_table()[name]
EF = complete(N)
R = Realiser(N, E)
X = rng.standard_normal((K, N, 2))
w = rng.dirichlet(np.ones(K) * 3.0)
x = X[0]
t = sqlen(x, E)[None]
print("T4b start", now())
print("x =", np.array2string(x, precision=4).replace("\n", ""))
sv = np.linalg.svd(rigidity_matrix(x, E), compute_uv=False)
print("singular values of the rigidity matrix at x:", np.array2string(sv, precision=4), " stress rank test:", stress_rank(x, E, np.random.default_rng(0)))
# hub triangles: signed areas (a flat triangle = nearly degenerate framework)
for (i, j) in [(1, 2), (2, 3), (3, 4), (1, 4)]:
    u_, v_ = x[i] - x[0], x[j] - x[0]
    a = 0.5 * (u_[0] * v_[1] - u_[1] * v_[0])
    print("   area of hub triangle (0,%d,%d) = %.4e" % (i, j, a))
C = Constructor(name, N, E)
# all realisations of the spanning subgraph, check-edge deviation for each flip pattern
for bits, (P, feas) in enumerate(C.realisations(t)):
    dev = sqlen(P, C.check)[0] - t[0, [C.idx[e] for e in C.check]]
    Dfull = np.linalg.norm(sqlen(P, EF)[0] - sqlen(x, EF))
    print("   flip pattern %d: feasible %s, check-edge deviation %s, distance D to x %.4f" % (bits, bool(feas[0]), np.array2string(dev, precision=3), Dfull))
r2 = np.random.default_rng(3)
for iters in (300, 3000):
    Z, res = R.solve(np.repeat(t, 3000, axis=0), 1.5 * r2.standard_normal((3000, R.n)), iters=iters)
    Dz = np.linalg.norm(sqlen(embed(Z, N), EF) - sqlen(x, EF)[None], axis=1)
    near = Dz < 1e-5
    other = (~near) & (res < 1e-3)
    print("LM on ||t(p)-t(x)||, 3000 starts, %d iters: reach x (D<1e-5, res<1e-9): %d ; other points with residual < 1e-3: %d"
          % (iters, int(np.sum(near & (res < 1e-9))), int(other.sum())))
    if other.any():
        k = np.where(other)[0][np.argmin(res[other])]
        vals = np.unique(np.round(res[other], 9))
        r, J = R.res_jac(Z[k:k + 1], t)
        g = np.einsum('bmn,bm->bn', J, r)[0]
        svj = np.linalg.svd(J[0], compute_uv=False)
        print("    distinct residual values among them:", np.array2string(vals[:6], precision=6),
              "; best: residual %.10e (f = %.4e), D = %.4f, grad %.1e, J singular values min %.3e max %.3e" % (res[k], res[k] ** 2, Dz[k], np.linalg.norm(g), svj[-1], svj[0]))
print("DONE t4b_w5_followup", now())
