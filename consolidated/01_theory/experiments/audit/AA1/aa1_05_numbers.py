#!/usr/bin/env python3
"""AA1 audit, script 5: independent recomputation of numbers quoted in THEORY_REPORT sections
11.4, 11.6, 11.10, 11.12, 11.14 (own formulas and code; nothing imported from the harness).

Each line prints the report's number, the recomputed one and OK / MISMATCH (tolerance: half a unit
of the last printed digit, plus 1e-4 for optimiser noise).

Run:  python3 experiments/audit/AA1/aa1_05_numbers.py > experiments/audit/AA1/out_05_numbers.txt
"""
import math

import numpy as np
from scipy.optimize import linprog, minimize_scalar

MISMATCH = []


def rep(label, claimed, got, tol=None):
    if tol is None:
        s = f"{claimed}"
        digits = len(s.split(".")[1]) if "." in s else 0
        tol = 0.5 * 10 ** (-digits) + 1e-4
    ok = abs(claimed - got) <= tol
    print(f"{'OK      ' if ok else 'MISMATCH'}  {label}: report {claimed}, recomputed {got:.6f}")
    if not ok:
        MISMATCH.append(label)


def h(x):
    return 0.0 if x <= 0 or x >= 1 else -x * math.log(x) - (1 - x) * math.log(1 - x)


def maximize(fn, lo, hi, grid=4001):
    xs = np.linspace(lo, hi, grid)
    vals = np.array([fn(x) for x in xs])
    i = int(vals.argmax())
    a, b = xs[max(i - 1, 0)], xs[min(i + 1, grid - 1)]
    res = minimize_scalar(lambda x: -fn(x), bounds=(a, b), method="bounded", options={"xatol": 1e-12})
    return (-res.fun, res.x) if -res.fun >= vals[i] else (vals[i], xs[i])


# ---------------------------------------------------------------- Theorem 11.9 and its cautions
print("== Theorem 11.9 (zero temperature, product landscapes)")
R, _ = maximize(lambda x: math.log1p(x) - math.log1p(x * x), 1e-9, 1 - 1e-9)
rep("R* at rho = 1/2", 0.1882, R)


def r2(t, e, c):
    return math.log1p(math.exp(-t * e)) - math.log1p(math.exp(-t * c))


per_site = maximize(lambda t: r2(t, 0.5, 1), 0, 60)[0] + maximize(lambda t: r2(t, 5, 10), 0, 6)[0]
common = maximize(lambda t: r2(t, 0.5, 1) + r2(t, 5, 10), 0, 60, grid=60001)[0]
rep("types (0.5,1),(5,10): per-site maxima added", 0.3765, per_site)
rep("types (0.5,1),(5,10): common slope (the exponent per pair)", 0.2329, common)


def lp_rate(rho, t):
    """max_v [ln sum v - ln max_a sum_s v(s) exp(-t rho(a,s))] = ln max{sum v : sum_s v(s) e^{-t rho(a,s)} <= 1}."""
    k = rho.shape[0]
    A = np.exp(-t * rho)
    res = linprog(c=-np.ones(k), A_ub=A, b_ub=np.ones(k), bounds=[(0, None)] * k, method="highs")
    return math.log(-res.fun) if res.status == 0 and -res.fun > 0 else float("-inf")


def site_rho(phi, gam, c):
    k = len(phi)
    E = np.array(phi) + np.array(gam)
    gap = E - E.min()
    rho = np.zeros((k, k))
    for a in range(k):
        for s in range(k):
            rho[a, s] = (c if a != s else 0.0) - gam[a] + gam[s] - gap[s]
    return rho, gap


rho3, gap3 = site_rho([0, 0.5, 3], [0, 0, 0], 1.0)
R3 = max(lp_rate(rho3, t) for t in np.linspace(0, 12, 2401))
B3 = maximize(lambda t: math.log(np.exp(-t * gap3).sum()) - math.log(1 + 2 * math.exp(-t)), 0, 12)[0]
rep("three-state site gaps (0,0.5,3), c=1: R*", 0.1882, R3)
rep("three-state site: Boltzmann-weight bound", 0.1066, B3)
rho2, gap2 = site_rho([0, 0.677], [0, 0.644], 1.0)
R2 = max(lp_rate(rho2, t) for t in np.linspace(0, 12, 4801))
slackmat = np.array([[0, 1 + 0.644], [1 - 0.644, 0]])
B2 = max(math.log(np.exp(-t * gap2).sum()) - math.log(max(np.exp(-t * slackmat[a]).sum() for a in range(2)))
         for t in np.linspace(0, 12, 4801))
rep("two-state site phi=(0,0.677), gamma=(0,0.644): R*", 0.0252, R2)
print(f"          Boltzmann bound for that site: max_t = {B2:.6f} (report: vacuous, i.e. <= 0)")
if B2 > 1e-9:
    MISMATCH.append("Boltzmann bound vacuous for the two-state site with residual")

# ---------------------------------------------------------------- Theorem 11.15
print("== Theorem 11.15 (finite temperature, deterministic certificates)")


def Rbeta_primal(beta, e, c):
    p1 = math.exp(-beta * e) / (1 + math.exp(-beta * e))

    def val(q):
        kl = q * math.log(q / p1) + (1 - q) * math.log((1 - q) / (1 - p1))
        D = kl / (beta * c)
        if D >= min(q, 1 - q):
            return 0.0
        return h(q) - h(D)

    return maximize(val, 1e-9, 1 - 1e-9, grid=20001)[0]


def Rbeta_dual(beta, e, c):
    p = np.array([1.0, math.exp(-beta * e)])
    p /= p.sum()
    best = 0.0
    for t in np.linspace(1e-6, 40 * max(1.0, beta), 1500):
        q = math.exp(-t * c)
        a = beta / (beta + t)

        def val(lv1):
            v1 = math.exp(lv1)
            first = ((beta + t) / beta) * math.log(p[0] ** (1 - a) * 1.0 + p[1] ** (1 - a) * v1 ** a)
            second = math.log(max(1 + v1 * q, q + v1))
            return first - second

        best = max(best, maximize(val, -40, 40, grid=801)[0])
    return best


for beta, claimed in ((1, 0.666), (4, 0.482), (40, 0.216), (0.5, 0.686), (2, 0.605)):
    rp = Rbeta_primal(beta, 0.5, 1.0)
    rep(f"R_beta, e/c = 1/2, beta = {beta} (primal form)", claimed, rp)
for beta in (1, 4):
    rp, rd = Rbeta_primal(beta, 0.5, 1.0), Rbeta_dual(beta, 0.5, 1.0)
    print(f"          single-letter identity at beta = {beta}: primal {rp:.5f}, dual {rd:.5f}, difference {abs(rp-rd):.1e}")
    if abs(rp - rd) > 2e-3:
        MISMATCH.append(f"primal/dual forms of R_beta at beta={beta}")
rep("sharp site e=2, c=1, beta=ln2: R_beta", 0.514, Rbeta_primal(math.log(2), 2.0, 1.0))
p1 = 0.25 / 1.25
rep("sharp site: entropy H(pi)", 0.500, h(p1))
rep("sharp site: single evaluation, upper ratio per site 6/5", 1.2, 0.8 + 0.2 * 2)
rep("sharp site: two-sided width per site ln(4/3)", round(math.log(4 / 3), 4), math.log((0.8 + 0.2 * 2) / (0.8 + 0.2 * 0.5)))

# ---------------------------------------------------------------- Theorems 11.24-11.26 (two-state site)
print("== Theorems 11.24-11.28 (two-state sites)")


def site(beta, e, c):
    pi = np.array([1.0, math.exp(-beta * e)])
    pi /= pi.sum()
    s = np.array([[0, c], [c, 0.0]])
    lam = np.array([-math.log(sum(pi[a] * math.exp(-beta * s[a, b]) for a in range(2))) for b in range(2)])
    return pi, s, lam


def game_value_2xk(K):
    """min over mixtures M of the two columns of max over the two rows of sum_b M(b) K[a,b] (2 x 2, exact)."""
    assert K.shape == (2, 2)
    cands = [0.0, 1.0]
    # crossing of the two rows as functions of m = M(0):  m K[a,0] + (1-m) K[a,1]
    den = (K[0, 0] - K[0, 1]) - (K[1, 0] - K[1, 1])
    if den != 0:
        m = (K[1, 1] - K[0, 1]) / den
        if 0 < m < 1:
            cands.append(m)
    return min(max(m * K[a, 0] + (1 - m) * K[a, 1] for a in range(2)) for m in cands)


def Rrand(beta, e, c, eps1=0.0, tmax=None):
    pi, s, lam = site(beta, e, c)
    tmax = tmax or 6 * beta + 6
    best, arg = 0.0, 0.0
    for t in np.linspace(0, tmax, 3001):
        K = np.array([[math.exp(-t * (s[a, b] - lam[b] / beta)) for b in range(2)] for a in range(2)])
        v = -math.log(game_value_2xk(K)) - t * eps1 / beta
        if v > best:
            best, arg = v, t
    return best, arg


for beta, e, claimed in ((1, 0.5, 0.0275), (4, 0.5, 0.154), (40, 0.5, 0.1882), (1, 2.0, 0.013)):
    val, targ = Rrand(beta, e, 1.0)
    rep(f"R^rand_beta(0), e/c = {e}, beta = {beta}  (argmax t = {targ:.2f})", claimed, val)


def Ubeta(beta, e, c):
    pi, s, lam = site(beta, e, c)
    return math.log(sum(pi[b] / sum(pi[a] * math.exp(-beta * s[a, b]) for a in range(2)) for b in range(2)))


for beta, claimed in ((0.5, 0.216), (1, 0.365), (2, 0.521), (4, 0.630)):
    rep(f"U_beta, e/c = 1/2, beta = {beta}", claimed, Ubeta(beta, 0.5, 1.0))

for u, claimed in ((0.5, 0.0077), (1.0, 0.029), (2.0, 0.097), (math.log(16), 0.156)):
    lam1 = math.log(2 / (1 + math.exp(-u)))
    rep(f"cube, third row ln2 - h(Lambda1/u), u = {u:.4f}", claimed, math.log(2) - h(lam1 / u))
u = 1.0
rep("cube: ln 2/(1+e^-u) at u = 1 (spot-check exponent)", 0.380, math.log(2 / (1 + math.exp(-u))))
rep("cube: n ln cosh(u/2) per site at u = 1", 0.120, math.log(math.cosh(0.5)), tol=6e-4)
rep("cube: 27/16 instance, ln(27/16)/4 = ln2 - h(1/4)", round(math.log(27 / 16) / 4, 4), math.log(2) - h(0.25))
rep("cube: eps < 0.2425 m, i.e. 4 ln(17/16)", 0.2425, 4 * math.log(17 / 16))

# thresholds for two-state sites (Theorem 11.24 remark, Theorem 11.28(e))
beta, e, c = 1.0, 0.5, 1.0
p = math.exp(-beta * e) / (1 + math.exp(-beta * e))
rep("eps1^crit at the zero residual, e/c=1/2, beta=1", 0.11367, 0.5 * math.log(1 + 2 * p * (1 - p) * (math.cosh(beta * c) - 1)))


def chord(theta, beta, e, c):
    P = lambda th: math.log1p(math.exp(-beta * (e + th)))
    return ((c + theta) * P(c) + (c - theta) * P(-c)) / (2 * c) - P(theta)


G0 = chord(0.0, beta, e, c)
Gmax, thstar = maximize(lambda th: chord(th, beta, e, c), -c, c, grid=20001)
rep("chord gap G(0)", 0.11367, G0)
rep("eps1* = max_theta G(theta)", 0.11383, Gmax)
rep("theta*/c", -0.037, thstar / c)
W1 = max(math.log(q * math.exp(sg * beta * c * (1 - q)) + (1 - q) * math.exp(-sg * beta * c * q))
         for q in (p,) for sg in (1, -1))
rep("untilted (passive) width W1 of the known part", 0.12246, W1)
for bb, claimed in ((4, 0.254), (40, 0.361), (400, 0.374)):
    gm, _ = maximize(lambda th: chord(th, bb, 0.5, 1.0), -1, 1, grid=40001)
    rep(f"eps1*/beta at beta = {bb} (limit (c^2-e^2)/(2c) = 0.375)", claimed, gm / bb)

# flat k-state sites, generalised dips (Theorem 11.27)
print("== Theorem 11.27 (flat k-state sites)")


def KLb(a, b):
    return a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))


def flat(k, u, m):
    rho = -math.log(m / k + (1 - m / k) * math.exp(-u)) / u
    target = 1 - m / k
    return KLb(rho, target) if rho < target else 0.0


rep("k=4, u=1: boxes of pairs", 0.02914, flat(4, 1.0, 2))
rep("k=4, u=1: single dips", 0.02841, flat(4, 1.0, 1))
rep("k=8, u=1: best box", 0.0309, max(flat(8, 1.0, m) for m in range(1, 8)))
rep("k=8, u=1: single dips", 0.0194, flat(8, 1.0, 1))

# ---------------------------------------------------------------- Theorem 11.32
print("== Theorem 11.32 (dense second-order classes, mean-field constants)")


def R2(lam):
    def val(om):
        d = math.sqrt(2 * lam * om)
        if d > min(om, 1 - om):
            return 0.0
        return h(om) - h(d)

    return maximize(val, 1e-9, 1 - 1e-9, grid=40001)[0]


for lam, claimed in ((0.02, 0.295), (0.1, 0.078), (0.2, 0.007)):
    rep(f"R_2(lambda = {lam})", claimed, R2(lam))
print(f"          R_2(0.249) = {R2(0.249):.2e}, R_2(0.251) = {R2(0.251):.2e}  (report: positive iff lambda < 1/4)")

# ---------------------------------------------------------------- Theorems 11.36, 11.38
print("== Theorems 11.36, 11.38 (chain geometry)")
rep("lever-arm limit (2/sqrt3) sin(60deg) sin(55.5deg)", 0.824, 2 / math.sqrt(3) * math.sin(math.radians(60)) * math.sin(math.radians(55.5)))
tet = math.degrees(math.acos(-1 / 3))
rep("tetrahedral angle, delta = 180deg: 2 sqrt2 / 3", 0.943, 2 / math.sqrt(3) * math.sin(math.radians(90)) * math.sin(math.radians(tet / 2)))
n, lam = 1000, 1.0
N = n + 3
for cst in (0.043, 0.0506):
    print(f"          Theorem 11.38 lower end at n = 1000, lambda = 1 with c = {cst}: exp({cst * math.sqrt(lam * N):.3f})"
          f"   (report: 'between e^1.6 and e^235', and 'the reviewer's grids support c ~ 0.043')")
for k in (2, 3, 4):
    # workstream G, Theorem G8(a): N_cov <= 1 + sum_w min{ C(n,w)(k-1)^w , 81^{ceil((N-1)/s_w)} }, s_w = floor(w e/((1+sqrt3) L b))
    logs = [0.0]
    for w in range(1, n + 1):
        a = math.lgamma(n + 1) - math.lgamma(w + 1) - math.lgamma(n - w + 1) + w * math.log(k - 1) if k > 1 else float("inf")
        sw = math.floor(w / ((1 + math.sqrt(3)) * lam))
        b = math.ceil((N - 1) / sw) * math.log(81) if sw >= 1 else float("inf")
        logs.append(min(a, b))
    mx = max(logs)
    tot = mx + math.log(sum(math.exp(x - mx) for x in logs))
    closed = 4.91 * math.sqrt(lam * N * math.log(math.e * (k - 1) * n)) + math.log(81 * (n + 1)) if k > 1 else float("nan")
    print(f"          Theorem 11.38 upper end, k = {k}: sum formula ln N_cov <= {tot:.1f};  displayed closed form = {closed:.1f}")

print()
print("ALL NUMBERS REPRODUCED" if not MISMATCH else "MISMATCHES: " + "; ".join(MISMATCH))
