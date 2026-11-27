"""T2b - follow-up of the single colouring of W6, K=3, ensemble 0 (seed 2102) that fell below the
pre-set LM threshold 1e-6 in logs/t2_W6_K3_run1.log (LM residual 7.9e-07, exact defect 2.3e-06).
Question: is the LM residual a converged positive minimum, or slow convergence to a true zero?
Reproduces the ensemble with the same generator and draw order as t2_chimera_search.py."""
import numpy as np
from r21_common import *

name, K, seed = "W6", 3, 2102
rng = np.random.default_rng(seed)
N, E = graph_table()[name]
m = len(E)
R = Realiser(N, E)
C = Constructor(name, N, E)
X = rng.standard_normal((K, N, 2))            # ensemble 0: first draw of the run
Tc = sqlen(X, E)
col = all_colourings(K, m)
col = col[nonconstant(col)]
T = splice_targets(Tc, col)
ex, _ = C.defect(T)
i = int(np.argmin(ex))
print("T2b start", now())
print("colouring with the smallest exact defect: #%d  %s   exact defect %.6e" % (i, ''.join(map(str, col[i])), ex[i]))
print("conformer squared lengths used:", np.array2string(T[i], precision=6))
t = T[i:i + 1]
# (1) LM from many starts, increasing iteration counts
r2 = np.random.default_rng(1)
for iters in (120, 1000, 5000):
    Z0 = 1.5 * r2.standard_normal((400, R.n))
    Z, res = R.solve(np.repeat(t, 400, axis=0), Z0, iters=iters)
    k = int(np.argmin(res))
    r, J = R.res_jac(Z[k:k + 1], t)
    g = np.einsum('bmn,bm->bn', J, r)[0]
    sv = np.linalg.svd(J[0], compute_uv=False)
    print("LM iters=%5d, 400 starts: min residual %.10e ; #starts within 1%% of it: %d ; grad norm at it %.2e ; "
          "singular values of J: max %.3e min %.3e" % (iters, res[k], int(np.sum(res < 1.01 * res[k])), np.linalg.norm(g), sv[0], sv[-1]))
Zbest = Z[k:k + 1].copy()
# (2) polish the best point with plain Gauss-Newton steps and report the residual sequence
z = Zbest.copy()
seq = []
for it in range(60):
    r, J = R.res_jac(z, t)
    seq.append(float(np.linalg.norm(r)))
    step = np.linalg.lstsq(J[0], -r[0], rcond=None)[0]
    z = z + step[None]
print("Gauss-Newton polish, residual every 10 steps:", ["%.10e" % s for s in seq[::10]])
r, J = R.res_jac(z, t)
print("final residual vector (per edge):", np.array2string(r[0], precision=3))
# (3) the same test on the three conformers themselves (must go to rounding level)
for c in range(K):
    Z0 = 1.5 * r2.standard_normal((400, R.n))
    Zc, resc = R.solve(np.repeat(Tc[c:c + 1], 400, axis=0), Z0, iters=1000)
    print("control: conformer %d, 400 starts, 1000 iters: min residual %.3e, starts reaching <1e-9: %d/400" % (c, resc.min(), int(np.sum(resc < 1e-9))))
print("DONE t2b_w6_followup", now())
