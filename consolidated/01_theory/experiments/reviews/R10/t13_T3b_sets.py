"""Theorem T3(b) on sets that are NOT unions of profile classes around one centre: exact sums on a
4-block grid (n = 4s), flat-histogram instance H (lattice landscape V_n).  For each set D:
   e_D = ln(Phi_H^+(D))/n,  theta_D = -ln(maxdens(D))/n,
   omega(D) = least omega >= 0 with theta_D <= Rbar(e_D - omega) + omega,
once with Rbar = max(R_ref, -e), R_ref = the best LOWER bound of R_H that I know (binary shells and
the free-block family S3; computed here), once with the PROVED upper bound Rbar_unif (ferromagnet).
T3(b) says omega -> 0 with the true R_H >= R_ref; a set with omega (w.r.t. R_ref) bounded away from 0
would be a profile-free view of R_H > R_ref; with respect to R_unif it would contradict T3(b)+T9(e).
usage: python3 t13_T3b_sets.py u s seed"""
import time, sys, math, json
import numpy as np
from scipy import optimize
from r10lib import *
from r10fin import *
t0 = time.time()
u = float(sys.argv[1]); s = int(sys.argv[2]); seed = int(sys.argv[3])
bJ = 1.5
phi = lambda k: -(bJ / 2.0) * (2 * k - 1) ** 2
M = Model(bJ=bJ, bB=0.0, u=u)
rng = np.random.default_rng(seed)
n = 4 * s
# ---- reference curve
sh = lambda x: binary(0.5, x, x)
def best_shell(e):
    f = lambda x: -(lambda v: v if np.isfinite(v) else -1.0)(r_mu(M, *sh(x), e))
    xs = np.linspace(max(p_u(u) * 0.6, 0.01), 0.499, 40)
    vals = [f(x) for x in xs]
    i = int(np.argmin(vals))
    res = optimize.minimize_scalar(f, bounds=(xs[max(i - 1, 0)], xs[min(i + 1, 39)]), method='bounded', options={'xatol': 1e-9})
    return max(-res.fun, -vals[i]), res.x
def s3p(lf, x):
    return np.array([(1 - lf) / 2, lf, (1 - lf) / 2]), np.array([1 - x, 0.5, x])
Eu = float(np.log(np.cosh(u / 2)))
ec = -float(kl(p_u(u), 0.5))
egrid = np.concatenate((np.linspace(1.15 * ec, 0, 24)[:-1], np.linspace(0, 1.02 * Eu, 28)))
Rref = []
z = np.array([0.14, max(p_u(u) + 0.005, 0.02)])
for e in egrid:
    r2, x = best_shell(e)
    r = r2
    if e > 0:
        f = lambda zz: -(lambda v: v if np.isfinite(v) else -1.0)(r_mu(M, *s3p(min(max(zz[0], 1e-4), 0.9), min(max(zz[1], 0.005), 0.495)), e))
        res = optimize.minimize(f, z, method='Nelder-Mead', options={'xatol': 1e-7, 'fatol': 1e-12, 'maxiter': 300})
        if -res.fun > r2:
            z = res.x
        r = max(r2, -res.fun)
    Rref.append(max(r, 0.0))
Rref = np.maximum.accumulate(np.array(Rref)[::-1])[::-1]          # nonincreasing envelope (R_H is nonincreasing)
print(f"# u={u} n={n}: reference curve at e=0: {np.interp(0.0, egrid, Rref):.7f}; R_unif(0) = {R_unif(0.0,u):.7f}; E_unif = {Eu:.5f}; table time {time.time()-t0:.0f}s", flush=True)
def Rbar_ref(e):
    if e <= egrid[0]:
        return -e
    if e >= egrid[-1]:
        return 0.0
    return max(float(np.interp(e, egrid, Rref)), -e)
def Rbar_unif(e):
    return max(R_unif(e, u), -e)
def omega(eD, thD, Rb):
    if thD <= Rb(eD):
        return 0.0
    lo, hi = 0.0, 2.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if thD <= Rb(eD - mid) + mid:
            hi = mid
        else:
            lo = mid
    return hi
# ---- grid
fb = FinBlocks((s, s, s, s), phi, u)
i1, i2, i3, i4 = fb.cnt
Vt = fb.Vn[fb.t] / n
lnn = math.log(n) / n
def dshell(pairA, pairB, x):
    a = sum(fb.cnt[j] for j in pairA); b = sum(fb.cnt[j] for j in pairB)
    a0 = round((1 - x) * 2 * s); b0 = round(x * 2 * s)
    return np.abs(a - a0) + np.abs(b - b0), (a0, b0)
def alpha_shell(x):
    a0 = round((1 - x) * 2 * s); b0 = round(x * 2 * s)
    return -(lbinom(2 * s, a0) + lbinom(2 * s, b0) - lbinom(n, a0 + b0) - fb.J[a0 + b0]) / n
centres = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
results = {}
def record(fam, mask, note=""):
    if mask.all() or not mask.any():
        return
    r = fb.dip(mask, fb.Vn)
    if r['maxdens'] <= 0:
        return
    eD = r['lPhiP'] / n
    thD = -math.log(r['maxdens']) / n
    o1 = omega(eD, thD, Rbar_ref); o2 = omega(eD, thD, Rbar_unif)
    results.setdefault(fam, []).append((o1, o2, eD, thD, note))
xs = [max(p_u(u) + 0.01, 0.02), p_u(u) + 0.03, p_u(u) + 0.06]
es = [0.4 * ec, 0.0, 0.15 * Eu, 0.35 * Eu]
for x in xs:
    d = [dshell(A, B_, x)[0] for A, B_ in centres]
    al = alpha_shell(x)
    for e in es:
        B = al + e
        N = [(u * dd / n + Vt) < B for dd in d]
        record("1 one shell-neighbourhood (control)", N[0], f"x={x:.3f} e={e:+.4f}")
        record("2 union of two shell-neighbourhoods (centres at distance n/2)", N[0] | N[1], f"x={x:.3f} e={e:+.4f}")
        record("3 union of three", N[0] | N[1] | N[2], f"x={x:.3f} e={e:+.4f}")
        record("4 intersection of two", N[0] & N[1], f"x={x:.3f} e={e:+.4f}")
        record("5 symmetric difference of two", N[0] ^ N[1], f"x={x:.3f} e={e:+.4f}")
        record("6 sum of the two distances", (u * (d[0] + d[1]) / (2 * n) + Vt) < B, f"x={x:.3f} e={e:+.4f}")
        N1b = (u * d[1] / n + Vt) < (B + 0.5 * abs(e) + 0.01)
        record("7 union with unequal budgets", N[0] | N1b, f"x={x:.3f} e={e:+.4f}")
    print(f"#   shells x={x:.3f} done t={time.time()-t0:.0f}", flush=True)
# neighbourhoods of single 4-block cells, unions of two, cylinders, half-spaces
for rep in range(14):
    mu = np.clip(np.array([1 - xs[1], 1 - xs[1], xs[1], xs[1]]) + 0.12 * rng.standard_normal(4), 0.03, 0.97)
    c = np.round(mu * s).astype(int)
    l1 = sum(np.abs(fb.cnt[j] - c[j]) for j in range(4))
    al = -fb.lpi[tuple(c)] / n
    mu2 = np.clip(np.array([1 - xs[1], xs[1], 1 - xs[1], xs[1]]) + 0.12 * rng.standard_normal(4), 0.03, 0.97)
    c2 = np.round(mu2 * s).astype(int)
    l1b = sum(np.abs(fb.cnt[j] - c2[j]) for j in range(4))
    alb = -fb.lpi[tuple(c2)] / n
    for e in (0.0, 0.25 * Eu):
        A_ = (u * l1 / n + Vt) < al + e
        B_ = (u * l1b / n + Vt) < alb + e
        record("8 neighbourhood of a random 4-block class", A_, f"c={tuple(c)} e={e:+.4f}")
        record("9 union of two such", A_ | B_, f"c={tuple(c)},{tuple(c2)} e={e:+.4f}")
        l1c = sum(np.abs(fb.cnt[j] - c[j]) for j in range(3))
        # cylinder: block 4 free; its class has pi-exponent of the 3-block marginal
        cyl_cells = (fb.cnt[0] == c[0]) & (fb.cnt[1] == c[1]) & (fb.cnt[2] == c[2])
        from scipy.special import logsumexp
        alc = -float(logsumexp(fb.lpi[cyl_cells])) / n
        record("10 cylinder (block 4 free)", (u * l1c / n + Vt) < alc + e, f"c={tuple(c[:3])} e={e:+.4f}")
    w = rng.standard_normal(4)
    lin = sum(w[j] * fb.cnt[j] for j in range(4))
    for qv in (0.02, 0.1, 0.3):
        tau = np.quantile(lin.ravel()[::97], qv)
        record("11 half-space in the counts", lin < tau, f"w={np.round(w,2)} q={qv}")
    if time.time() - t0 > 400:
        break
print(f"# family: sets | max omega w.r.t. R_ref (in units ln n/n) | max omega w.r.t. R_unif (units ln n/n) | where the first maximum is attained")
for fam in sorted(results, key=lambda f: int(f.split()[0])):
    rr = results[fam]
    o1 = max(rr, key=lambda r: r[0]); o2 = max(r[1] for r in rr)
    print(f"  {fam}: {len(rr)} | {o1[0]:.5f} ({o1[0]/lnn:.3f}) | {o2:.5f} ({o2/lnn:.3f}) | e_D={o1[2]:+.4f} theta_D={o1[3]:.4f} {o1[4]}")
print("time", time.time() - t0)
