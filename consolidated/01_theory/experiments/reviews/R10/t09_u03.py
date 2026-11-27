"""bJ = 1.5, B = 0, u = 0.30 (narrow contact piece at the top of the barrier): binary barrier
shells, R2(e) near e = 0 and its slopes, the pair identity through n_mu, the best shell-cone at
the accuracy S(0), a direct grid evaluation of n_mu, and the PROVED upper end of the bracket.
usage: python3 t09_u03.py [u]"""
import time, sys
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
from r10tab import *
t0 = time.time()
u = float(sys.argv[1]) if len(sys.argv) > 1 else 0.30
M = Model(bJ=1.5, bB=0.0, u=u)
print(f"# u={u}: contact set {[(round(a,5), round(b,5)) for a,b in M.contact()]};  R_unif(0) = {R_unif(0.0,u):.8f}, p_u = {p_u(u):.5f}")
sh = lambda x: binary(0.5, x, x)
fine = dict(G=400, zooms=5, ncand=6, nz=41, rounds=8)

def best_shell(e, lo=0.40, hi=0.4995, npts=400):
    xs = np.linspace(lo, hi, npts)
    vs = np.array([r_mu(M, *sh(x), e) for x in xs])
    vs = np.where(np.isfinite(vs), vs, -1)
    j = int(np.argmax(vs))
    # refine on the right-continuous side: local scan
    xl, xr = xs[max(j - 1, 0)], xs[min(j + 1, npts - 1)]
    for _ in range(4):
        xx = np.linspace(xl, xr, 41)
        vv = np.array([r_mu(M, *sh(x), e) for x in xx])
        vv = np.where(np.isfinite(vv), vv, -1)
        jj = int(np.argmax(vv))
        xl, xr = xx[max(jj - 1, 0)], xx[min(jj + 1, 40)]
    return float(vv[jj]), float(xx[jj])

print("# binary barrier shells: R2(e), optimal x")
es = [-0.002, -0.001, -0.0005, 0.0, 0.0001, 0.0003, 0.0006, 0.001, 0.002]
Rs = []
for e in es:
    r, x = best_shell(e)
    lam, mu = sh(x)
    s2 = inner_dual(M, lam, mu, e + alpha(M, lam, mu), nk=2001, refine=5)[0]
    Rs.append(r)
    print(f"   e={e:+.4f}  R2={r:.8f}  x={x:.5f}  S2(dual, I)={s2:.8f}   t={time.time()-t0:.0f}", flush=True)
print("#   slopes between consecutive accuracies:", np.round(np.diff(Rs) / np.diff(es), 3))
R0, x0 = best_shell(0.0)
X = R0
print(f"# S(0) = R2(0) = {X:.8f} at x = {x0:.5f}")
lam, mu = sh(x0)
print(f"#   n_mu(S(0)) at the optimal shell: {n_mu(M, lam, mu, X)[0]:.8f}")
# profile of e + r_mu(e) for the optimal shell and for x = 0.4514
for x in (x0, 0.4514):
    lam, mu = sh(x)
    al = alpha(M, lam, mu)
    row = []
    for e in (-0.002, -0.001, 0.0, 0.0002, 0.0005, 0.001, 0.0015, 0.002):
        r = inner_clip(M, lam, mu, e + al, **fine)[0]
        row.append(f"{e:+.4f}:{r:.6f}")
    print(f"#   r_mu(e) for the shell x={x:.4f}: " + "  ".join(row))
# best symmetric shell for the non-adaptive bound at X
xs = np.linspace(0.435, 0.49, 56)
nv = [n_mu_grid(M, *sh(x), X) for x in xs]
j = int(np.argmax(nv))
res = optimize.minimize_scalar(lambda x: -n_mu_grid(M, *sh(x), X), bounds=(xs[max(j - 1, 0)], xs[min(j + 1, 55)]), method='bounded', options={'xatol': 1e-6})
xb = res.x if -res.fun > nv[j] else xs[j]
nb = max(-res.fun, nv[j])
nb_scan = n_mu(M, *sh(xb), X, ne=400)[0]
print(f"# sup over symmetric shells of n_mu(S(0)) = {nb:.8f} (two-parameter grid) = {nb_scan:.8f} (through r_mu, T8(b)) at x = {xb:.5f}  ( = {nb / R0:.3f} R2(0); report 0.0018400 at x = 0.4514)   t={time.time()-t0:.0f}", flush=True)
# direct evaluation of n_mu at that shell on a full grid of exit profiles (nu1, nu0), with I in the constraint
lam, mu = sh(xb)
al = alpha(M, lam, mu)
best = np.inf
lo1, hi1, lo0, hi0 = 0.0, 1.0, 0.0, 1.0
for it in range(4):
    g1 = np.linspace(lo1, hi1, 1201); g0 = np.linspace(lo0, hi0, 1201)
    N1, N0 = np.meshgrid(g1, g0, indexing='ij')
    nb_ = 0.5 * N1 + 0.5 * N0
    mi = h(nb_) - 0.5 * h(N1) - 0.5 * h(N0)
    con = mi + u * (0.5 * np.abs(N1 - mu[0]) + 0.5 * np.abs(N0 - mu[1])) + M.I(nb_) - al
    mi_f = np.where(con <= X, mi, np.inf)
    k_ = int(np.argmin(mi_f))
    i1, i0 = np.unravel_index(k_, mi_f.shape)
    best = min(best, float(mi_f[i1, i0]))
    w1, w0 = (hi1 - lo1) / 40, (hi0 - lo0) / 40
    lo1, hi1 = max(g1[i1] - w1, 0), min(g1[i1] + w1, 1)
    lo0, hi0 = max(g0[i0] - w0, 0), min(g0[i0] + w0, 1)
print(f"#   the same n_mu by a full grid over exit profiles with I in the constraint (upper bound of the minimum): {best:.8f} at nu = ({g1[i1]:.5f}, {g0[i0]:.5f})")
# general binary profiles
f = lambda th: -n_mu_grid(M, *prof(th, 2), X)
bestg = (nb, None)
for st in ((0.5, xb, xb), (0.48, xb + 0.005, xb - 0.005), (0.52, xb - 0.004, xb + 0.006)):
    r_ = optimize.minimize(f, unprof(*binary(*st)), method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-11, 'maxiter': 300})
    if -r_.fun > bestg[0]:
        bestg = (-r_.fun, prof(r_.x, 2))
print(f"# sup over general binary profiles of n_mu(S(0)) (3 Nelder-Mead starts): {bestg[0]:.8f} {'' if bestg[1] is None else fmt(*bestg[1])}   t={time.time()-t0:.0f}", flush=True)
# proved upper end: theta_na <= theta_na of the uniform cube (R_H <= R_unif for all e)
def S_unif(e):
    return e + R_unif(e, u)
ec = -float(kl(p_u(u), 0.5))
if X < S_unif(0.0):
    es_ = optimize.brentq(lambda e: S_unif(e) - X, ec, 0.0)
else:
    es_ = optimize.brentq(lambda e: S_unif(e) - X, 0.0, float(np.log(np.cosh(u / 2))))
print(f"# proved upper end of the bracket for theta_na(S(0)): R_unif(S_unif^-1({X:.7f})) = {R_unif(es_, u):.8f}  (the report's upper end {R0:.8f} is the binary value, a LOWER bound of R_H(0))")
print("time", time.time() - t0)
