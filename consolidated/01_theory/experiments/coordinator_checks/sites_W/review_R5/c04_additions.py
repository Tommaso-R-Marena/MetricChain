"""Additions of SCI-REV-0001 section 5 and SCI-REV-0005 section 7, and the numbers behind m1.  Harness helpers (st_*) and own code."""
import sys, time, math
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import dlib
H = dlib.load_harness()
rng = np.random.default_rng(11)
t0 = time.time()


def cube(u):
    """closed forms of the uniform two-letter cube: h, a, E, and F*(t)."""
    F = lambda t: t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))
    t, h = dlib.golden(F, 0.0, 1.0, tol=1e-13)
    p = 1 / (1 + math.exp(u))
    a = math.log(2) + p * math.log(p) + (1 - p) * math.log(1 - p)
    return h, a, math.log(math.cosh(u / 2)), F


def hae_own(pi, d):
    s = dlib.Site(pi, d)
    return dlib.Rhat([(1.0, s)], 0.0)[0], dlib.a_site(s), dlib.E_site(s)


def hae_harness(pi, d):
    s = H.st_site(pi, d)
    return H.st_R([(1.0, s)], 0.0)[0], H.st_a(s), H.st_E(s)


print("(A) the ceiling  F*(t) <= t(1-t) D^2/8,  D = max d  (Hamming envelope: D = u);  h <= D^2/32, E <= D^2/8, a <= D^2/8")
worst = dict(F=0.0, h=0.0, E=0.0, a=0.0); n = 0
sites = []
for u in (0.1, 0.3, 0.5, 1.0, 2.0, 3.0):
    sites.append(("cube u=%g" % u, [0.5, 0.5], dlib.hamming(2, u)))
    sites.append(("unif3 u=%g" % u, [1 / 3] * 3, dlib.hamming(3, u)))
    sites.append(("(0.05,0.5,0.45) u=%g" % u, [0.05, 0.5, 0.45], dlib.hamming(3, u)))
    sites.append(("unif4 u=%g" % u, [0.25] * 4, dlib.hamming(4, u)))
for name, (pi, d) in dlib.SITES.items():
    sites.append((name, pi, d))
for _ in range(12):
    q = int(rng.integers(2, 5)); dd = rng.uniform(0.2, 2.5, (q, q)); np.fill_diagonal(dd, 0.0)
    for k in range(q): dd = np.minimum(dd, dd[:, [k]] + dd[[k], :])
    sites.append(("random asym q=%d" % q, rng.dirichlet(np.ones(q) * 2), dd))
tight = []
for name, pi, d in sites:
    D = float(np.max(d)); hs = H.st_site(pi, d); so = dlib.Site(pi, d)
    rmax = 0.0
    for t in (0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95):
        vh = H.st_renyi(hs, t); vo = dlib.renyi(so, t)
        ceil = t * (1 - t) * D * D / 8
        rmax = max(rmax, vh[1] / ceil, vo[1] / ceil)          # the dual (upper) bounds against the ceiling
    h, a, E = hae_own(pi, d)
    worst["F"] = max(worst["F"], rmax); worst["h"] = max(worst["h"], h / (D * D / 32)); worst["E"] = max(worst["E"], E / (D * D / 8)); worst["a"] = max(worst["a"], a[1] / (D * D / 8))
    n += 1
    if name.startswith(("cube", "unif3")): tight.append((name, rmax, h / (D * D / 32), E / (D * D / 8), a[1] / (D * D / 8)))
print("   %d sites (cube, uniform 3 and 4 letters, (0.05,0.5,0.45), the four example sites, 12 random asymmetric): largest F*/ceiling = %.6f,"
      " h/(D^2/32) = %.6f, E/(D^2/8) = %.6f, a/(D^2/8) = %.6f   (all must be <= 1)" % (n, worst["F"], worst["h"], worst["E"], worst["a"]))
for row in tight:
    print("      %-14s  max_t F*/ceiling = %.5f   h/(u^2/32) = %.5f   E/(u^2/8) = %.5f   a/(u^2/8) = %.5f" % row)

print("(B) u = 0.5, three letters, Hamming: the data point of SCI-REV-0001 section 5 and the table of R5_REPORT 6.3   [own | harness helpers]")
u = 0.5
hc, ac, Ec, Fc = cube(u)
print("      two-letter cube (closed form)        h = %.10f  a = %.10f  E = %.10f" % (hc, ac, Ec))
for name, pi in (("uniform (1/3,1/3,1/3)", [1 / 3] * 3), ("(0.05, 0.5, 0.45)", [0.05, 0.5, 0.45]), ("(0.04502, 0.45679, 0.49819)", [0.04502, 0.45679, 0.49819]),
                 ("(0.001, 0.4995, 0.4995)", [0.001, 0.4995, 0.4995]), ("(0.02, 0.49, 0.49)", [0.02, 0.49, 0.49])):
    h, a, E = hae_own(pi, dlib.hamming(3, u)); hh, ah, Eh = hae_harness(pi, dlib.hamming(3, u))
    print("      %-30s h = %.10f  a = %.10f [bracket %.1e]  E = %.10f   | harness: h = %.10f a = %.10f E = %.10f   | h - h_cube = %+.3e (%+.4f %%), a - a_cube = %+.3e, E - E_cube = %+.3e" %
          (name, h, a[0], a[1] - a[0], E, hh, ah, Eh, h - hc, 100 * (h - hc) / hc, a[0] - ac, E - Ec))
# certified bracket for h of the data point: h = max_t F*(t); lower bound = primal value at any t, upper bound = max over a grid of the dual bound + Lipschitz slack
site = dlib.Site([0.04502, 0.45679, 0.49819], dlib.hamming(3, u))
tstar = dlib.Rhat([(1.0, site)], 0.0)[1]
v = dlib.renyi(site, tstar)
print("      data point: t* = %.6f, primal value F*(t*) = %.12f (a certified lower bound of h), dual bound at t* = %.12f; cube h = %.12f  ->  h - h_cube >= %.3e" %
      (tstar, v[0], v[1], hc, v[0] - hc))
ts = np.linspace(tstar - 0.02, tstar + 0.02, 81)
up = max(dlib.renyi(site, t)[1] for t in ts)
print("      upper bound of h from the dual values on a grid of step 5e-4 around t*: %.12f (plus second-order grid error ~ |F''| step^2/8 ~ 1e-9)" % up)

print("(C) 'a site law that gives some set of letters the weight 1/2 is at least as hard as the cube' (Hamming envelope): F*(t) - F*_cube(t) >= 0")
worst = 1.0; cnt = 0; strict = 0
for _ in range(40):
    q = int(rng.integers(3, 6)); u = float(rng.choice([0.3, 0.5, 1.0, 2.0]))
    k = int(rng.integers(1, q))                      # the set A = first k letters gets the weight 1/2
    pa = rng.dirichlet(np.ones(k)) * 0.5; pb = rng.dirichlet(np.ones(q - k)) * 0.5
    pi = np.concatenate([pa, pb])
    so = dlib.Site(pi, dlib.hamming(q, u)); hs = H.st_site(pi, dlib.hamming(q, u))
    Fc = cube(u)[3]
    for t in (0.1, 0.3, 0.5, 0.7, 0.9):
        diff = min(dlib.renyi(so, t)[0], H.st_renyi(hs, t)[0]) - Fc(t)
        worst = min(worst, diff); cnt += 1; strict += diff > 1e-9
print("   %d (law, slope) pairs, alphabets of 3-5 letters, u in {0.3, 0.5, 1, 2}: smallest F* - F*_cube = %.2e (must be >= 0 up to solver error); strictly larger in %d" % (cnt, worst, strict))
# the two box vertices alone give exactly the cube:
pi = np.array([0.2, 0.3, 0.1, 0.4]); u = 0.7; A = [0, 1]            # pi(A) = 1/2
ind = np.zeros(4); ind[A] = 1.0
P2 = np.array([dlib.gibbs(pi, u * ind), dlib.gibbs(pi, -u * ind)])
for t in (0.2, 0.5, 0.8):
    best = max(-t * math.log(float(((np.array([m, 1 - m]) @ P2 ** t) ** (1 / t)).sum())) for m in np.linspace(0, 1, 2001))
    print("      two box vertices -/+ u 1_A, pi(A) = 1/2, t = %.1f: max_M G_t = %.12f, cube F* = %.12f" % (t, best, cube(u)[3](t)))

print("(D) m1: the cube with u = 1 as a binary symmetric channel: E_sp(theta) - theta beyond h")
u = 1.0; h, a, E, F = cube(u); p = 1 / (1 + math.exp(u))
kl = lambda x, y: x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))
def Esp(theta):                      # KL(rho || p_u) at KL(rho || 1/2) = theta, p_u <= rho <= 1/2
    lo, hi = p, 0.5
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if kl(mid, 0.5) >= theta: lo = mid
        else: hi = mid
    return kl(lo, p)
def Esp_gallager(theta):             # sup_rho [E_0(rho) - rho theta], E_0(rho) = (1+rho) F(1/(1+rho))
    rr, v = dlib.golden(lambda r: (1 + r) * F(1 / (1 + r)) - r * theta, 0.0, 400.0, tol=1e-10)
    return v
print("      h = %.6f, a = %.6f, E = %.6f;  E_sp(h) - h = %.2e (fixed point)" % (h, a, E, Esp(h) - h))
for th in (0.5 * h, h, 0.3 * a, 0.5 * a, 0.9 * a):
    print("      theta = %.6f (= %.3f a = %.3f h): E_sp = %.6f [Gallager form %.6f], E_sp - theta = %+.6f" % (th, th / a, th / h, Esp(th), Esp_gallager(th), Esp(th) - th))

print("(E) m4: at a fixed label law M, Gallager's sup_rho [E_0(rho, M) - rho theta] against the Csiszar-Koerner (Augustin) form sup_rho rho [I^A - theta]; path site")
site = dlib.Site(*dlib.SITES["path"])
from scipy.optimize import minimize
def augustin(M, t):                  # min_Q sum_phi M(phi) D_t(pi_phi || Q), by SLSQP over Q (convex)
    Pt = site.P ** t
    def f(z):
        Q = np.exp(z - z.max()); Q /= Q.sum()
        return float(M @ (np.log((Pt * Q[None, :] ** (1 - t)).sum(axis=1)) / (t - 1)))
    best = min((minimize(f, np.log(M @ site.P) if s == 0 else rng.normal(0, 1, site.q), method="BFGS", options={"gtol": 1e-12}).fun for s in range(2)))
    return best
def sibson(M, t):
    return (t / (t - 1)) * math.log(float(((M @ site.P ** t) ** (1 / t)).sum()))
gapmax = 0.0; viol = 0
Estar_site = dlib.E_site(site)
rhos = np.concatenate([np.linspace(0.02, 3, 60), np.linspace(3.2, 40, 60)])
for trial in range(8):
    M = rng.dirichlet(np.ones(len(site.V)))
    theta = float(rng.uniform(0.02, 0.2))
    gal = max(r * (sibson(M, 1 / (1 + r)) - theta) for r in rhos)
    ck = max(r * (augustin(M, 1 / (1 + r)) - theta) for r in rhos)
    full = max((1 + r) * dlib.renyi(site, 1 / (1 + r))[0] - r * theta for r in rhos)      # E_sp(theta) with the maximised E_0
    gapmax = max(gapmax, ck - gal); viol += (gal > ck + 1e-9) or (ck > full + 1e-7)
print("   8 random M: Gallager(M) <= CK(M) <= E_sp violated %d times; largest CK(M) - Gallager(M) = %.2e" % (viol, gapmax))
val, upb, Mstar, Q = dlib.renyi(site, 0.4)
print("   at the optimal M* of t = 0.4: Sibson = %.12f, Augustin = %.12f (equal at the capacity-achieving law)" % (sibson(Mstar, 0.4), augustin(Mstar, 0.4)))
print("time %.1f s" % (time.time() - t0))
