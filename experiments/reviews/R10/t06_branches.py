"""bJ=1.5, B=0, u=1: the binary branch (symmetric shells, checked against unrestricted binary
profiles), the free-block branch S3 = {1-x, 1/2 (weight lf), x}, their crossing e0, and a table
of R2(e) for later use.  Own solvers; optima re-evaluated with S2 (dual, I)."""
import time, sys, json
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
t0 = time.time()
M = Model(bJ=1.5, bB=0.0, u=1.0)
u = 1.0

def shell(x):
    return binary(0.5, x, x)

def s3(lf, x):
    return np.array([(1 - lf) / 2, lf, (1 - lf) / 2]), np.array([1 - x, 0.5, x])

def best_shell(e, lo=0.2, hi=0.45):
    def f(x):
        v = r_mu(M, *shell(x), e)          # nan if the shell is not admissible at e (e + alpha < v(type))
        return -v if np.isfinite(v) else 1.0
    xs = np.linspace(lo, hi, 26)
    vals = [f(x) for x in xs]
    i = int(np.argmin(vals))
    res = optimize.minimize_scalar(f, bounds=(xs[max(i - 1, 0)], xs[min(i + 1, 25)]), method='bounded', options={'xatol': 1e-10})
    return -res.fun, res.x

def best_s3(e, z0=(0.14, 0.275)):
    def f(z):
        v = r_mu(M, *s3(min(max(z[0], 1e-4), 0.9), min(max(z[1], 0.01), 0.49)), e)
        return -v if np.isfinite(v) else 1.0
    res = optimize.minimize(f, z0, method='Nelder-Mead', options={'xatol': 1e-9, 'fatol': 1e-14, 'maxiter': 600})
    return -res.fun, res.x

print("# binary branch (symmetric shells) and S3 branch")
print("#   e      R2(e)        x        S3(e)        lf       x3      R_unif(e)   S2-check(binary)  S2-check(S3)")
table = []
z = (0.14, 0.275)
for e in (-0.10, -0.07, -0.05, -0.03, -0.01, 0.0, 0.001, 0.0015, 0.0018, 0.002, 0.0025, 0.004, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.064):
    r2, x = best_shell(e)
    lam, mu = shell(x)
    c2 = inner_dual(M, lam, mu, e + alpha(M, lam, mu), nk=1201, refine=5)[0]
    if e >= 0:
        r3, z = best_s3(e, z)
        lam3, mu3 = s3(*z)
        c3 = inner_dual(M, lam3, mu3, e + alpha(M, lam3, mu3), nk=1201, refine=5)[0]
        print(f"  {e:+.4f}  {r2:.9f}  {x:.5f}  {r3:.9f}  {z[0]:.4f}  {z[1]:.5f}  {R_unif(e,u):.7f}   {c2:.9f}   {c3:.9f}", flush=True)
    else:
        r3 = np.nan
        print(f"  {e:+.4f}  {r2:.9f}  {x:.5f}      -          -       -      {R_unif(e,u):.7f}   {c2:.9f}", flush=True)
    table.append((e, r2, x, r3))
# crossing
def diff(e):
    r2, _ = best_shell(e)
    r3, _ = best_s3(e, (0.14, 0.2715))
    return r3 - r2
e0 = optimize.brentq(diff, 0.001, 0.003, xtol=1e-8)
print(f"# crossing of the two branches: e0 = {e0:.6f}   (report: 0.00181)   value there {best_shell(e0)[0]:.9f}")
# unrestricted binary profiles at three accuracies (is the symmetric shell the binary optimum?)
for e in (-0.05, 0.0, 0.03):
    best = -1
    for (m, a, b) in ((0.45, 0.33, 0.27), (0.55, 0.26, 0.34), (0.4, 0.3, 0.3), (0.5, 0.2, 0.4)):
        val, l2, m2 = nm(M, e, *binary(m, a, b))
        if val > best:
            best, bl, bm = val, l2, m2
    print(f"# unrestricted binary, e={e:+.3f}: {best:.9f} [{fmt(bl, bm)}]")
json.dump(table, open('../out/t06_table.json', 'w'))
print("time", time.time() - t0)
