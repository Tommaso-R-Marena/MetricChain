#!/usr/bin/env python3
"""Workstream A1 -- a class-wide KL bound by the chain rule, and what it gives at bounded accuracy.

Setting: X = {0,1}^n, reference pi = Bern(p)^n, psi u-Lipschitz for the Hamming distance,
nu_psi ~ pi e^{-psi},  A(psi) = E_pi e^{-psi}.   a0 = p e^{-u}/(q + p e^{-u}),  a1 = p e^{u}/(q + p e^{u})
(the letter marginals of the cones around 0^n and 1^n; logit a1 - logit a0 = 2u for every p).

Proposition A1.1 (report, sect. 2.6).
 (i)   For every u-Lipschitz psi, every order of the coordinates, every prefix:  nu_psi(y_i = 1 | y_<i) in [a0, a1].
 (ii)  Hence for every r in (0,1):  KL(nu_psi || Bern(r)^n) <= n * R(r),  R(r) = max(KL(a0||r), KL(a1||r)),
       with equality for the cone around 0^n or 1^n;  min_r R(r) = a(p,u) = capacity of the binary channel (a0, a1).
 (iii) Under nu_psi, for r in [a0, a1]:  P( log(d nu_psi / d Bern(r)^n) > n R(r) + s ) <= exp(-s^2 / (2 n u^2))
       (Azuma-Hoeffding: each log-likelihood increment takes two values that differ by |logit kappa - logit r| <= 2u).
 (iv)  For M i.i.d. points from Q^n = Bern(r)^n and any tau > 0:
       E | A_hat/A - 1 | <= sqrt(tau/M) + 2 P_nu( d nu/dQ^n > tau ).
 So M = exp(n a + t) points from the PRODUCT measure Bern(r*)^n give E|A_hat/A - 1| <= e^{-t/4} + 2 exp(-t^2/(8 n u^2))
 for EVERY member of the class and every n -- no isoperimetric input.
 (v)   a(p,u) <= a(1/2,u) = ln 2 - h(p_u), with equality iff p = 1/2: the odds-ratio lemma in capacity form.

Checks: exact enumeration on cubes n = 8..14 with several families of Lipschitz functions (cones, flattened cones,
dips, McShane regularisations of random functions, minima/maxima of cones, block-radial functions); Monte Carlo for (iv);
mutations.   Run: python3 chain_rule_check.py   (about 1-2 min)
"""
import math
import sys

import numpy as np
from scipy.optimize import minimize_scalar

rng = np.random.default_rng(2026)
fails = 0


def check(name, ok, info=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ("   " + info if info else ""))
    fails += (not ok)


def kl(a, b):
    out = 0.0
    if a > 0:
        out += a * math.log(a / b)
    if a < 1:
        out += (1 - a) * math.log((1 - a) / (1 - b))
    return out


def h(p):
    return 0.0 if p <= 0 or p >= 1 else -p * math.log(p) - (1 - p) * math.log1p(-p)


def ends(p, u):
    q = 1 - p
    return p * math.exp(-u) / (q + p * math.exp(-u)), p * math.exp(u) / (q + p * math.exp(u))


def radius(p, u):
    a0, a1 = ends(p, u)
    res = minimize_scalar(lambda r: max(kl(a0, r), kl(a1, r)), bounds=(a0 + 1e-12, a1 - 1e-12), method="bounded",
                          options={"xatol": 1e-13})
    return res.fun, res.x


# ---------- the cube as arrays of shape (2,)*n, axis i = coordinate i ----------
def popcount_array(n):
    idx = np.arange(1 << n)
    pc = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        pc += (idx >> i) & 1
    return pc


def hamming_to(n, s):
    idx = np.arange(1 << n)
    x = idx ^ s
    d = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        d += (x >> i) & 1
    return d


def lipschitz_regularise(phi, n, u):
    """largest u-Lipschitz minorant: psi(x) = min_y phi(y) + u d(x,y)  (min-plus relaxation along edges)"""
    psi = phi.copy().reshape((2,) * n)
    for _ in range(n):
        for ax in range(n):
            flipped = np.flip(psi, axis=ax)
            psi = np.minimum(psi, flipped + u)
    return psi.reshape(-1)


def is_lipschitz(psi, n, u):
    a = psi.reshape((2,) * n)
    return all(np.abs(a - np.flip(a, axis=ax)).max() <= u + 1e-9 for ax in range(n))


def families(n, u):
    N = 1 << n
    out = []
    s = int(rng.integers(0, N))
    d = hamming_to(n, s)
    out.append(("cone(random centre)", u * d))
    out.append(("cone(0^n)", u * hamming_to(n, 0)))
    out.append(("cone(1^n)", u * hamming_to(n, N - 1)))
    R = int(rng.integers(1, n))
    out.append(("flattened cone", u * np.maximum(d, R)))
    out.append(("dip", np.minimum(0.0, u * (d - R))))
    out.append(("zero", np.zeros(N)))
    # minima / maxima of several cones with offsets
    cs = [int(rng.integers(0, N)) for _ in range(5)]
    offs = rng.uniform(0, u * n / 3, size=5)
    out.append(("min of 5 cones", np.min([o + u * hamming_to(n, c) for o, c in zip(offs, cs)], axis=0)))
    out.append(("max of 5 anti-cones", np.max([o - u * hamming_to(n, c) for o, c in zip(offs, cs)], axis=0)))
    # McShane regularisation of rough random functions (several roughness scales)
    for scale in (0.3, 1.0, 3.0, 10.0):
        out.append(("regularised random (scale %.1f)" % scale, lipschitz_regularise(rng.normal(0, scale * u, size=N), n, u)))
    # sparse deep wells
    phi = np.full(N, 0.0)
    wells = rng.integers(0, N, size=6)
    phi[wells] = -rng.uniform(0, u * n, size=6)
    out.append(("six wells", lipschitz_regularise(phi, n, u)))
    # block-radial function of two blocks
    n1 = n // 2
    mask1 = (1 << n1) - 1
    idx = np.arange(N)
    d1 = hamming_to(n1, int(rng.integers(0, 1 << n1)))[idx & mask1]
    d2 = hamming_to(n - n1, int(rng.integers(0, 1 << (n - n1))))[idx >> n1]
    # (each of d1, d2 changes by one when a coordinate is flipped, and only one of them changes)
    out.append(("block-radial |d1-d2|", u * np.abs(d1 - d2)))
    out.append(("block-radial min(d1, d2+2)", u * np.minimum(d1, d2 + 2)))
    # additive with slopes in [-u, u]
    gam = rng.uniform(-u, u, size=n)
    add = np.zeros(N)
    for i in range(n):
        add += gam[i] * ((idx >> i) & 1)
    out.append(("additive", add))
    return out


def analyse(n, p, u, psi, r):
    """returns (min kappa, max kappa over all prefixes for 3 coordinate orders, KL(nu||Bern(r)^n), log-density array, nu)"""
    N = 1 << n
    pc = popcount_array(n)
    logpi = pc * math.log(p) + (n - pc) * math.log(1 - p)
    lw = logpi - psi
    lw -= lw.max()
    w = np.exp(lw)
    nu = w / w.sum()
    kmin, kmax = 1.0, 0.0
    arr = nu.reshape((2,) * n)          # axis k <-> bit (n-1-k)
    for trial in range(3):
        perm = np.arange(n) if trial == 0 else rng.permutation(n)
        a = np.transpose(arr, perm)
        for i in range(n):
            m = a.sum(axis=tuple(range(i + 1, n))) if i + 1 < n else a
            num = np.take(m, 1, axis=i)
            den = num + np.take(m, 0, axis=i)
            ok = den > 1e-290
            kap = num[ok] / den[ok]
            kmin, kmax = min(kmin, float(kap.min())), max(kmax, float(kap.max()))
    logq = pc * math.log(r) + (n - pc) * math.log(1 - r)
    logrho = np.log(np.maximum(nu, 1e-300)) - logq
    KL = float((nu * logrho)[nu > 0].sum())
    return kmin, kmax, KL, logrho, nu


# ------------------------------------------------------------------ main loop
all_ok_i = all_ok_ii = all_ok_iii = all_lip = True
worst_ratio = 0.0
cone_ratio = []
tested = 0
bad_names = []
slack_kappa = 0.0
for (n, p, u) in ((8, 0.5, 1.0), (10, 0.5, 2.0), (12, 0.5, 0.5), (10, 0.2, 1.0), (12, 0.1, 2.0), (14, 0.3, 1.0), (11, 0.7, 1.5)):
    a0, a1 = ends(p, u)
    a, rstar = radius(p, u)
    c = max(abs(math.log(k / rstar)) for k in (a0, a1)) + max(abs(math.log((1 - k) / (1 - rstar))) for k in (a0, a1))
    for name, psi in families(n, u):
        if not is_lipschitz(psi, n, u):
            all_lip = False
            bad_names.append(name)
        kmin, kmax, KL, logrho, nu = analyse(n, p, u, psi, rstar)
        tested += 1
        all_ok_i &= (kmin >= a0 - 1e-9) and (kmax <= a1 + 1e-9)
        slack_kappa = max(slack_kappa, a0 - kmin, kmax - a1)
        all_ok_ii &= KL <= n * a + 1e-9
        worst_ratio = max(worst_ratio, KL / (n * a))
        if name in ("cone(0^n)", "cone(1^n)"):
            cone_ratio.append(KL / (n * a))
        # (iii) exact tail against the Azuma bound
        for s in (0.25 * u * math.sqrt(n), 0.5 * u * math.sqrt(n), 1.0 * u * math.sqrt(n), 2.0 * u * math.sqrt(n), 3.0 * u * math.sqrt(n)):
            tail = float(nu[logrho > n * a + s].sum())
            # sharp form: each log-likelihood increment takes two values that differ by |logit kappa - logit r*| <= 2u
            all_ok_iii &= tail <= math.exp(-s * s / (2 * n * u * u)) + 1e-12
check("A1  every instance generated is u-Lipschitz (sanity of the generators)", all_lip, "%d instances%s" % (tested, "" if all_lip else "; NOT Lipschitz: " + ", ".join(sorted(set(bad_names)))))
check("A2  (i) all conditional means nu(y_i = 1 | prefix) lie in [a0, a1] (3 coordinate orders, all prefixes)", all_ok_i,
      "largest excursion outside the interval: %.1e" % slack_kappa)
check("A3  (ii) KL(nu_psi || Bern(r*)^n) <= n a for every instance; equality at one of the cones around 0^n, 1^n",
      all_ok_ii and max(cone_ratio) > 1 - 1e-9, "max KL/(n a) = %.6f; max over the two constant cones = %.6f" % (worst_ratio, max(cone_ratio)))
check("A4  (iii) exact upper tail of the log-density under nu_psi is below exp(-s^2/(2 n u^2))", all_ok_iii)

# ------------------------------------------------------------------ (iv) Monte Carlo
ok_iv = True
rows = []
for (n, p, u, t) in ((12, 0.5, 1.0, 3.0), (12, 0.2, 1.5, 3.0), (10, 0.5, 2.0, 4.0)):
    a, rstar = radius(p, u)
    N = 1 << n
    pc = popcount_array(n)
    q = np.exp(pc * math.log(rstar) + (n - pc) * math.log(1 - rstar))
    q /= q.sum()
    M = int(math.ceil(math.exp(n * a + t)))
    tau = math.exp(n * a + t / 2)
    for name, psi in families(n, u)[:9]:
        _, _, KL, logrho, nu = analyse(n, p, u, psi, rstar)
        rho = np.exp(logrho)
        bound = math.sqrt(tau / M) + 2 * float(nu[rho > tau].sum())
        reps = 300
        draws = rng.choice(N, size=(reps, M), p=q)
        est = rho[draws].mean(axis=1)
        err = float(np.abs(est - 1).mean())
        se = float(np.abs(est - 1).std() / math.sqrt(reps))
        ok_iv &= err <= bound + 3 * se
        rows.append((n, p, u, name, M, err, bound))
worst = max(rows, key=lambda r: r[5] / r[6])
check("A5  (iv) E|A_hat/A - 1| <= sqrt(tau/M) + 2 P_nu(rho > tau) with M = e^{na+t}, tau = e^{na+t/2} (27 instances, 300 runs each)",
      ok_iv, "tightest case: n=%d p=%.1f u=%.1f %s: M=%d, measured %.3f, bound %.3f" % worst)

# ------------------------------------------------------------------ (v)
u = 1.0
vals = [(p, radius(p, u)[0]) for p in np.linspace(0.02, 0.98, 97)]
top = max(vals, key=lambda v: v[1])
a_half = math.log(2) - h(1 / (1 + math.exp(u)))
check("A6  (v) a(p,u) <= a(1/2,u) = ln2 - h(p_u), maximal at p = 1/2  (odds-ratio lemma in capacity form; logit a1 - logit a0 = 2u)",
      abs(top[0] - 0.5) < 1e-9 and abs(top[1] - a_half) < 1e-9 and all(v[1] <= a_half + 1e-12 for v in vals),
      "argmax p = %.2f, a = %.6f; a(0.3) = %.6f, a(0.1) = %.6f" % (top[0], top[1], radius(0.3, u)[0], radius(0.1, u)[0]))
ok = all(abs((math.log(a1 / (1 - a1)) - math.log(a0 / (1 - a0))) - 2 * uu) < 1e-12
         for pp in (0.1, 0.4, 0.8) for uu in (0.5, 2.0) for (a0, a1) in [ends(pp, uu)])
check("A6b the cone channel has log odds ratio exactly 2u for every p", ok)

# ------------------------------------------------------------------ mutations
n, p, u = 10, 0.3, 1.0
a0, a1 = ends(p, u)
a, rstar = radius(p, u)
# (m1) a function that is NOT u-Lipschitz must be able to violate (i)
psi_bad = 3.0 * u * hamming_to(n, 0)
kmin, kmax, KL, _, _ = analyse(n, p, u, psi_bad, rstar)
m1 = (kmin < a0 - 1e-6) or (kmax > a1 + 1e-6)
# (m2) with the proposal pi itself (r = p) the bound n*a must fail for a cone
_, _, KLp, _, _ = analyse(n, p, u, u * hamming_to(n, (1 << n) - 1), p)
m2 = KLp > n * a * 1.05
# (m3) a tighter interval for the conditional means must fail
kmin, kmax, _, _, _ = analyse(n, p, u, u * hamming_to(n, 0), rstar)
m3 = kmin < a0 + 1e-3
check("A7  mutations detected (3u-Lipschitz function leaves the interval; proposal r = p exceeds n a; interval is tight)",
      m1 and m2 and m3, "KL(cone||pi)/(n a) = %.3f" % (KLp / (n * a)))

print("\nfailures: %d" % fails)
sys.exit(1 if fails else 0)
