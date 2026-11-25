#!/usr/bin/env python3
"""Assistant A, SCI-REV-0001, finding M2: Theorem 11.90(a) at negative accuracies.  Own code (numpy/scipy only),
nothing imported from the repository or from the reviewer's scripts.

Slice of density kappa.  A profile is a finitely supported law rho of block densities with mean kappa;
MI = E_rho KL(x || kappa);  r(e) = min{MI(nu) : type(nu) = kappa, u dist(nu, mu) <= e + MI(mu)}.
Claim to test: for -h(kappa) <= e < 0 the supremum of r over ALL feasible profiles equals the supremum over
two-block profiles.

Three independent computations:
 (A) two blocks: semi-analytic value of a centre (root of F' = u) + brute force over shells; sup over centre types;
 (B) all profiles supported on a grid of densities, any number of blocks: for fixed multipliers (t, xi) the dual
     function is linear in rho, so  sup_rho [E_rho g_{t,xi} - t e]  over the feasible laws is a linear programme
     (3 constraints); by weak duality every such value is <= r of a feasible profile, by strong duality the
     supremum over (t, xi) is the supremum of r over grid laws.  Global in rho, 2-dimensional search in (t, xi);
 (C) explicit profiles with 3-5 blocks, feasible at e < 0: inner value bracketed between a dual value (lower)
     and the MI of an exactly feasible exit (upper); random profiles and Nelder-Mead from random starts.
"""
import math, sys, time
import numpy as np
from scipy.optimize import linprog, minimize

rng = np.random.default_rng(20261125)


def kl(a, b):
    a = np.clip(np.asarray(a, float), 0.0, 1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(a > 0, a * np.log(a / b), 0.0) + np.where(a < 1, (1 - a) * np.log((1 - a) / (1 - b)), 0.0)


def hb(k):
    return -k * math.log(k) - (1 - k) * math.log(1 - k)


def logit(p):
    return math.log(p / (1 - p))


def sig(z):
    return 1.0 / (1.0 + np.exp(-z))


# ---------------------------------------------------------------- (A) two blocks
def lmax(m, k):
    return min(2 * m * (1 - k), 2 * (1 - m) * k)


def F(m, k, l):
    return float(m * kl(k + l / (2 * m), k) + (1 - m) * kl(k - l / (2 * (1 - m)), k))


def Fp(m, k, l):
    return 0.5 * (logit(k + l / (2 * m)) - logit(k - l / (2 * (1 - m))))


def lstar(m, k, u):
    a, b = 0.0, lmax(m, k) * (1 - 1e-15)
    for _ in range(200):
        mid = 0.5 * (a + b)
        if Fp(m, k, mid) < u:
            a = mid
        else:
            b = mid
    return 0.5 * (a + b)


def V_centre(m, k, u, e):
    """sup over the FEASIBLE shells l >= 0 of the centre m of F((l - (e + F(l))/u)_+); -inf if none is feasible."""
    ls = lstar(m, k, u)
    Fs = F(m, k, ls)
    if e + Fs >= 0:
        x = ls - (e + Fs) / u
        return F(m, k, x) if x > 0 else 0.0
    if -e <= F(m, k, lmax(m, k)):
        return -e
    return -math.inf


def V_centre_brute(m, k, u, e, n=200001):
    l = np.linspace(0.0, lmax(m, k), n)
    Fl = m * kl(k + l / (2 * m), k) + (1 - m) * kl(k - l / (2 * (1 - m)), k)
    ok = Fl >= -e
    if not ok.any():
        return -math.inf
    x = np.maximum(l - (e + Fl) / u, 0.0)[ok]
    return float((m * kl(k + x / (2 * m), k) + (1 - m) * kl(k - x / (2 * (1 - m)), k)).max())


def golden(f, a, b, tol=1e-12):
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol:
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
    x = 0.5 * (a + b)
    return f(x), x


def R2(k, u, e):
    ms = np.linspace(0.002, 0.998, 499)
    vals = np.array([V_centre(m, k, u, e) for m in ms])
    i = int(np.argmax(vals))
    v, m = golden(lambda mm: V_centre(mm, k, u, e), ms[max(i - 1, 0)], ms[min(i + 1, len(ms) - 1)])
    if vals[i] > v:
        v, m = float(vals[i]), float(ms[i])
    return v, m


def game_cube(u, e):
    f = lambda t: t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2)) - t * e
    v, t = golden(f, 0.0, 1.0)
    return max(v, f(0.0), f(1.0))


# ---------------------------------------------------------------- (B) all grid laws by linear programming
def gfun(x, t, xi, k, u):
    a = logit(k) - xi
    y = np.clip(x, sig(a - t * u), sig(a + t * u))
    return kl(y, k) + t * u * np.abs(y - x) + xi * (y - k) - t * kl(x, k)


def lp_value(x, klx, t, xi, k, u, e, want_rho=False):
    g = gfun(x, t, xi, k, u)
    res = linprog(-g, A_ub=[-klx], b_ub=[e], A_eq=[np.ones_like(x), x], b_eq=[1.0, k], bounds=(0, None), method="highs")
    if res.status != 0:
        return (-math.inf, None) if want_rho else -math.inf
    val = -res.fun - t * e
    return (val, res.x) if want_rho else val


def lp_sup(k, u, e, N=1201):
    x = np.linspace(0.0, 1.0, N)
    klx = kl(x, k)
    ts = np.concatenate([np.linspace(0.0, 1.5, 25), np.linspace(1.7, 4.0, 8), [5, 6, 8, 12, 20]])
    xis = np.linspace(-6, 6, 37)
    best = []
    for t in ts:
        for xi in xis:
            best.append((lp_value(x, klx, t, xi, k, u, e), t, xi))
    best.sort(reverse=True)
    top = best[0]
    seen = []
    for v0, t0, xi0 in best[:60]:
        if any(abs(t0 - a) < 0.2 and abs(xi0 - b) < 0.5 for a, b in seen):
            continue
        seen.append((t0, xi0))
        if len(seen) > 3:
            break
        res = minimize(lambda z: -lp_value(x, klx, abs(z[0]), z[1], k, u, e), [t0, xi0], method="Nelder-Mead",
                       options={"xatol": 1e-7, "fatol": 1e-13, "maxiter": 300})
        if -res.fun > top[0]:
            top = (-res.fun, abs(res.x[0]), res.x[1])
    val, rho = lp_value(x, klx, top[1], top[2], k, u, e, want_rho=True)
    atoms = [(float(x[i]), float(rho[i])) for i in np.nonzero(rho > 1e-9)[0]]
    mi = float(np.dot(rho, klx))
    return top[0], top[1], top[2], atoms, mi, len(best)


# ---------------------------------------------------------------- (C) explicit multi-block profiles
def r_lower(lam, mu, k, u, e):
    """the dual function at a (numerically) optimal (t, xi): a lower bound for r by weak duality, whatever (t >= 0, xi)."""
    lam, mu = np.asarray(lam, float), np.asarray(mu, float)
    dual = lambda z: float(np.dot(lam, gfun(mu, abs(z[0]), z[1], k, u))) - abs(z[0]) * e
    best = -math.inf
    for z0 in ([0.5, 0.0], [1.0, 0.0], [2.0, 0.5], [0.2, -0.5], [5.0, 0.0]):
        res = minimize(lambda z: -dual(z), z0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-15, "maxiter": 2000})
        best = max(best, -res.fun)
    return best


def r_upper(lam, mu, k, u, e):
    """MI of an exactly feasible exit (an upper bound for r): a clipping nu = clip(mu, c_lo, c_hi) of type k with
    u dist(nu, mu) <= e + MI(mu).  None if the profile is infeasible (e + MI(mu) < 0)."""
    lam, mu = np.asarray(lam, float), np.asarray(mu, float)
    B = e + float(np.dot(lam, kl(mu, k)))
    if B < 0:
        return None

    def clip_type(c_lo):
        lo = np.maximum(mu, c_lo)
        if float(np.dot(lam, np.minimum(lo, k))) >= k:
            c_hi = k
        else:
            a, b = k, 1.0
            for _ in range(60):
                mid = 0.5 * (a + b)
                if float(np.dot(lam, np.minimum(lo, mid))) <= k:
                    a = mid
                else:
                    b = mid
            c_hi = b
        nu = np.minimum(lo, c_hi)
        nu = nu + (k - float(np.dot(lam, nu)))            # restore the type exactly (a shift of order 1e-16)
        return nu, float(np.dot(lam, np.abs(nu - mu)))
    if u * clip_type(k)[1] <= B:
        return 0.0
    a, b = 0.0, k
    for _ in range(60):
        mid = 0.5 * (a + b)
        if u * clip_type(mid)[1] <= B:
            a = mid
        else:
            b = mid
    nu, d = clip_type(a)
    assert u * d <= B + 1e-15
    return float(np.dot(lam, kl(np.clip(nu, 0, 1), k)))


def r_bracket(lam, mu, k, u, e):
    up = r_upper(lam, mu, k, u, e)
    return None if up is None else (r_lower(lam, mu, k, u, e), up)


def random_profile(k, nb, e):
    for _ in range(200):
        lam = rng.dirichlet(np.ones(nb) * float(rng.choice([0.5, 1, 3])))
        mu = rng.beta(0.4, 0.4, nb)
        t = float(np.dot(lam, mu))
        mu = mu * k / t if t > k else 1 - (1 - mu) * (1 - k) / (1 - t)
        if float(np.dot(lam, kl(mu, k))) >= -e and mu.min() >= 0 and mu.max() <= 1:
            return lam, mu
    return None


def multi_search(k, u, e, r2, nrand=40, nstart=4):
    worst_rand, gap = -math.inf, 0.0
    for _ in range(nrand):
        nb = int(rng.integers(3, 6))
        pr = random_profile(k, nb, e)
        if pr is None:
            continue
        lo, up = r_bracket(pr[0], pr[1], k, u, e)
        worst_rand = max(worst_rand, up - r2)
        gap = max(gap, up - lo)

    def neg(z):                                             # three blocks: (l1, l2, a, b); the third density from the type
        l1, l2, a, b = z
        l3 = 1 - l1 - l2
        if min(l1, l2, l3) < 1e-4 or not (0 <= a <= 1 and 0 <= b <= 1):
            return 1.0
        c = (k - l1 * a - l2 * b) / l3
        if not (0 <= c <= 1):
            return 1.0
        out = r_upper([l1, l2, l3], [a, b, c], k, u, e)
        return 1.0 if out is None else -out                 # the upper end of the bracket: can only favour a violation
    best = -math.inf
    for s in range(nstart):
        pr = random_profile(k, 3, e)
        if pr is None:
            continue
        z0 = [pr[0][0], pr[0][1], pr[1][0], pr[1][1]]
        res = minimize(neg, z0, method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-12, "maxiter": 500})
        best = max(best, -res.fun)
    return worst_rand, gap, best - r2


if __name__ == "__main__":
    t00 = time.time()
    allcases = [(0.5, 1.0, -0.05), (0.5, 1.0, -0.15), (0.3, 1.0, -0.03), (0.3, 1.0, -0.2), (0.3, 2.0, -0.1),
                (0.2, 0.5, -0.02), (0.7, 3.0, -0.3), (0.1, 1.0, -0.05), (0.3, 1.0, -0.55), (0.3, 1.0, 0.0)]
    part = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    cases = allcases[:5] if part == 1 else allcases[5:] if part == 2 else allcases
    print("(A) two-block supremum (semi-analytic, sup over 499 centre types + golden section) and brute force over shells at the best centre")
    print("(B) LP over all laws on a grid of 1201 densities, sup over (t, xi): value, multipliers, atoms of the optimal law, its MI")
    print("(C) explicit profiles with 3-5 blocks: random feasible profiles and Nelder-Mead over 3-block profiles")
    print()
    worst = dict(lp=-math.inf, rand=-math.inf, nm=-math.inf, gap=0.0)
    for (k, u, e) in cases:
        t0 = time.time()
        r2, mb = R2(k, u, e)
        brute = V_centre_brute(mb, k, u, e)
        cube = game_cube(u, e)
        lpv, tt, xi, atoms, mi, nlp = lp_sup(k, u, e)
        wr, gap, nm = multi_search(k, u, e, r2)
        worst["lp"] = max(worst["lp"], lpv - r2)
        worst["rand"] = max(worst["rand"], wr)
        worst["nm"] = max(worst["nm"], nm)
        worst["gap"] = max(worst["gap"], gap)
        print(f"kappa={k}, u={u}, e={e}  (h(kappa) = {hb(k):.6f}, -e = {-e})")
        print(f"   (A) R2 = {r2:.10f} at m = {mb:.5f}; brute force over shells of that centre: {brute:.10f};  max(R2, -e) = {max(r2, -e):.10f};  cube game form {cube:.10f}")
        print(f"   (B) sup_(t,xi) [LP - te] = {lpv:.10f} at t = {tt:.4f}, xi = {xi:.4f} ({nlp} grid LPs + polishing);  LP - R2 = {lpv - r2:+.2e};")
        print(f"       optimal law: {len(atoms)} atoms " + ", ".join(f"({a:.4f}: {w:.4f})" for a, w in atoms) + f";  its MI = {mi:.8f} (budget e + MI = {e + mi:+.2e})")
        print(f"   (C) random 3-5-block profiles: max (r_upper - R2) = {wr:+.3e}; largest inner bracket width {gap:.1e};  Nelder-Mead over 3 blocks: best - R2 = {nm:+.3e}")
        print(f"       [{time.time() - t0:.0f} s]")
        sys.stdout.flush()
    print()
    print(f"SUMMARY: largest (LP sup - R2) = {worst['lp']:+.3e};  largest random multi-block excess = {worst['rand']:+.3e};  "
          f"largest Nelder-Mead excess = {worst['nm']:+.3e};  largest inner bracket width = {worst['gap']:.1e}")
    print(f"total {time.time() - t00:.0f} s")
