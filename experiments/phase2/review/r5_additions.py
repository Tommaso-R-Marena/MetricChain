#!/usr/bin/env python3
"""Referee replication 5: material added to the report while the review was running
(section 5.1, Lemma 5.1 'attenuated bias'; section 2.5, Proposition 2.7 'absorption').  Independent code.

Part A  Lemma 5.1 by brute force on a cube of 10 sites.
Part B  |nu~(s) - tanh(u/2)^|s|| at the critical radius (normalised Krawtchouk values by the three-term recurrence, floats).
Part C  Proposition 2.7: the two maps on a cube of 9 sites; the numbers h(u -+ kappa).
Part D  absorption against the flat family for a field (product reference).
Run: python3 -B r5_additions.py
"""
import math
import numpy as np

rng = np.random.default_rng(11)


def wht(a):
    a = a.astype(float).copy()
    N = a.shape[0]
    h = 1
    while h < N:
        a = a.reshape(N // (2 * h), 2, h)
        a = np.stack([a[:, 0, :] + a[:, 1, :], a[:, 0, :] - a[:, 1, :]], axis=1).reshape(N)
        h *= 2
    return a


def kl(x, y):
    return x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))


def consts(u):
    pu = 1 / (1 + math.exp(u))
    rho0 = math.log(2 / (1 + math.exp(-u))) / u
    return pu, kl(pu, 0.5), rho0, kl(rho0, 0.5)


print("== Part A: Lemma 5.1 (n = 10) ==")
n, u, r = 10, 1.0, 3
N = 1 << n
x = np.arange(N)
PC = np.zeros(N, dtype=np.int64)
for i in range(n):
    PC += (x >> i) & 1
er = np.maximum(np.exp(u * (r - PC)) - 1.0, 0.0)
nu = er / er.sum()
ok = True
for trial in range(5):
    Gam = rng.choice(N, size=int(rng.integers(1, 9)), replace=False)
    phi = rng.uniform(-1, 1, size=N)
    # left side: brute force over all shifts a
    lhs = 0.0
    for a in range(N):
        nu_shift = np.zeros(N)
        for c in Gam:
            nu_shift += nu[x ^ int(c) ^ a]
        nu_shift /= len(Gam)
        lhs += ((nu_shift * phi).sum() - phi.mean()) ** 2
    lhs /= N
    phih = wht(phi) / N                                   # phi^(s) = E_pi phi chi_s
    rho = np.zeros(N)
    rho[Gam] = 1.0 / len(Gam)
    rhot = wht(rho)                                       # rho~(s) = sum_c rho(c) chi_s(c)
    nut = wht(nu)
    rhs = float(((phih ** 2) * (rhot ** 2) * (nut ** 2))[1:].sum())
    bound = (phi ** 2).mean() * float(((np.abs(rhot) * np.abs(nut))[1:] ** 2).max())
    ok = ok and abs(lhs - rhs) < 1e-12 and rhs <= bound + 1e-15
    print(f"   |Gamma|={len(Gam)}: E_a(dev^2) = {lhs:.6e} = sum_s phi^2 rho~^2 nu~^2 = {rhs:.6e} <= {bound:.6e}")
print("   Lemma 5.1 identity and inequality:", ok)

print("== Part B: |nu~(s) - t^|s|| at the critical radius, t = tanh(u/2) (Krawtchouk recurrence, float64, orders j <= 60) ==")


def nu_tilde_dev(n, u, r):
    """max_j |S_j/S_0 - t^j| with S_j = sum_{d<r} C(n,d)(e^{u(r-d)}-1) kappa_j(d), kappa_j(d)=K_j(d)/C(n,j).
    kappa_j(d) is computed through the symmetric three-term recurrence in j (floats, long doubles)."""
    t = math.tanh(u / 2)
    ds = np.arange(0, r)
    wts = np.array([math.exp(math.lgamma(n + 1) - math.lgamma(d + 1) - math.lgamma(n - d + 1) + math.log(math.expm1(u * (r - d)))) for d in ds])
    # normalised Krawtchouk: (n-j) k_{j+1}(d) = (n-2d) k_j(d) - j k_{j-1}(d),  k_0 = 1, k_1 = 1 - 2d/n
    kprev = np.ones(len(ds))
    kcur = 1 - 2 * ds / n
    S0 = wts.sum()
    worst = abs((wts * kcur).sum() / S0 - t)
    for j in range(1, min(n, 60)):                     # orders up to 60 (t^60 is below every tolerance of interest)
        knext = ((n - 2 * ds) * kcur - j * kprev) / (n - j)
        kprev, kcur = kcur, knext
        worst = max(worst, abs((wts * kcur).sum() / S0 - t ** (j + 1)))
    return worst


for u in (1.0,):
    pu, a, rho0, h = consts(u)
    for n in (100, 200, 400, 800):
        # critical radius: least r with m_r > e^eps - 1 for eps = 0.5 (bounded accuracy)
        def m_r(r):
            return sum(math.exp(math.lgamma(n + 1) - math.lgamma(d + 1) - math.lgamma(n - d + 1) - n * math.log(2)) * math.expm1(u * (r - d)) for d in range(r))
        r = 1
        while m_r(r) <= math.expm1(0.5):
            r += 1
        print(f"   u={u} n={n}: r={r} (rho0 n = {rho0*n:.1f}); max_(j<=60) |nu~ - t^j| = {nu_tilde_dev(n, u, r):.3e}"
              f"   (archive A10 quotes its bound tau_0 = 1.9e-2, 1.3e-3, 2.7e-6, 1.7e-11 at n = 100..800; true deviation 5-10 times smaller)")

print("== Part C: Proposition 2.7 (absorption) ==")
n, u, kap = 9, 1.0, 0.4
N = 1 << n
x = np.arange(N)
PC = np.zeros(N, dtype=np.int64)
for i in range(n):
    PC += (x >> i) & 1


def lipschitz_const(g):
    """max over neighbours of |g(x) - g(y)| (the Lipschitz constant for the Hamming distance)."""
    return max(np.abs(g - g[x ^ (1 << i)]).max() for i in range(n))


# a known energy with single-site moves of cost at most kap: field + pair interaction on 0/1 variables
theta = rng.uniform(-1, 1, size=n)
J = np.triu(rng.uniform(-1, 1, size=(n, n)), 1)
bits = ((x[:, None] >> np.arange(n)[None, :]) & 1).astype(float)
f = bits @ theta + np.einsum('xi,ij,xj->x', bits, J, bits)
f *= kap / lipschitz_const(f)
okC = abs(lipschitz_const(f) - kap) < 1e-12
for trial in range(20):
    # w in W_u: maximum / sum of cones;  v in W_{u-kap}
    def member(slope):
        g = np.full(N, rng.uniform(0.3, 2.0))
        for _ in range(5):
            c = int(rng.integers(N))
            cone = rng.uniform(0.5, 20) * np.exp(-slope * PC[x ^ c])
            g = np.maximum(g, cone) if rng.random() < 0.5 else g + cone
        return g
    w = member(u)
    v = member(u - kap)
    pi0 = np.full(N, 1.0 / N)
    Zf = (pi0 * np.exp(-f)).sum()
    pi = pi0 * np.exp(-f) / Zf
    w1 = w * np.exp(-f)                                  # in W_{u+kap}, same ensemble under pi0, target + ln Zf
    v1 = v * np.exp(f)                                   # in W_u, same ensemble under pi, target - ln Zf
    okC = okC and lipschitz_const(np.log(w)) <= u + 1e-12 and lipschitz_const(np.log(w1)) <= u + kap + 1e-12
    okC = okC and lipschitz_const(np.log(v)) <= u - kap + 1e-12 and lipschitz_const(np.log(v1)) <= u + 1e-12
    okC = okC and np.allclose(w * pi / (w * pi).sum(), w1 * pi0 / (w1 * pi0).sum())
    okC = okC and np.allclose(v * pi0 / (v * pi0).sum(), v1 * pi / (v1 * pi).sum())
    okC = okC and abs(math.log((pi0 * w1).sum()) - (math.log((pi * w).sum()) + math.log(Zf))) < 1e-10
    okC = okC and abs(math.log((pi * v1).sum()) - (math.log((pi0 * v).sum()) - math.log(Zf))) < 1e-10
print("   the two maps, the equal ensembles and the shifted targets (n = 9, field + pair interaction):", okC)
for (uu, kk) in [(1.0, 0.25)]:
    print(f"   u={uu}, kappa={kk}: h(u-kappa) = {consts(uu-kk)[3]:.5f}, h(u) = {consts(uu)[3]:.5f}, h(u+kappa) = {consts(uu+kk)[3]:.5f};"
          f"  a(u-kappa) = {consts(uu-kk)[1]:.5f}, a(u) = {consts(uu)[1]:.5f}, a(u+kappa) = {consts(uu+kk)[1]:.5f}")
us = np.linspace(0.05, 6, 400)
print("   h and a increasing in u on [0.05, 6]:", bool(np.all(np.diff([consts(v)[3] for v in us]) > 0) and np.all(np.diff([consts(v)[1] for v in us]) > 0)))

print("== Part D: a field (product reference Bernoulli(p)^n): absorption against the flat family ==")
for (p, uu, flat0, flatbest) in [(0.3, 1.0, 0.010881, 0.01220), (0.1, 2.0, 0.005562, 0.01064)]:
    kk = abs(math.log(p / (1 - p)))                      # f = kk |x| : pi = e^{-f} uniform / Z
    if kk < uu:
        print(f"   p={p}, u={uu}: field strength kappa = ln((1-p)/p) = {kk:.4f} < u: absorption lower bound h(u-kappa) = {consts(uu-kk)[3]:.6f};"
              f" flat family (Theorem A''): {flat0:.6f} at the constant baseline, {flatbest:.5f} at the best tilt  [values from r3_field.py]")
    else:
        print(f"   p={p}, u={uu}: field strength kappa = {kk:.4f} >= u: Proposition 2.7 does not apply;"
              f" flat family (Theorem A''): {flat0:.6f} at the constant baseline, {flatbest:.5f} at the best tilt  [values from r3_field.py]")
