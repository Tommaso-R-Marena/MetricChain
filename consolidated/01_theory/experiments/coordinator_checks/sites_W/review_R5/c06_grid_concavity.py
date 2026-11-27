"""(a) three letters, Hamming: h, a, E on the grid of 171 site laws with entries in (1/20)N, at u = 0.5 and u = 1 (R5_REPORT 6.3);
(b) a local maximisation of h over three-letter laws at u = 0.5 (where does the data point of SCI-REV-0001 come from?);
(c) concavity of F* for two letters on 500 random sites (R5-T3: record the range of the numerical evidence).  Own code."""
import sys, time, math
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import minimize
import dlib
t0 = time.time()

# closed-form box vertices for three letters with the Hamming envelope: g = u * 1_B, B a proper nonempty subset
def site3(pi, u):
    return dlib.Site(pi, dlib.hamming(3, u))

def h_of(site, grid=24):
    ts = np.linspace(0.3, 0.7, grid + 1)
    vals = [dlib.renyi(site, t)[0] for t in ts]
    i = int(np.argmax(vals))
    t, v = dlib.golden(lambda t: dlib.renyi(site, t)[0], ts[max(i - 1, 0)], ts[min(i + 1, grid)], tol=1e-8)
    return max(v, max(vals))

def cube(u):
    F = lambda t: t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))
    h = dlib.golden(F, 0.0, 1.0, tol=1e-13)[1]
    p = 1 / (1 + math.exp(u))
    return h, math.log(2) + p * math.log(p) + (1 - p) * math.log(1 - p), math.log(math.cosh(u / 2))

print("(a) grid of 171 laws (i/20, j/20, k/20), i, j, k >= 1")
for u in (0.5, 1.0):
    best = dict(h=(-1, None), a=(-1, None), E=(-1, None)); n = 0
    for i in range(1, 19):
        for j in range(i, 19):                      # symmetric under permutations: i <= j <= k
            k = 20 - i - j
            if k < j: continue
            pi = [i / 20, j / 20, k / 20]; s = site3(pi, u); n += 1
            h = h_of(s); a = dlib.a_site(s, iters=20000)[0]; E = dlib.E_site(s)
            for key, val in (("h", h), ("a", a), ("E", E)):
                if val > best[key][0]: best[key] = (val, pi)
    hc, ac, Ec = cube(u)
    su = site3([1 / 3] * 3, u)
    print("   u = %.1f: %d laws up to permutation (171 with permutations); grid maxima: h = %.9f at %s, a = %.9f at %s, E = %.9f at %s" %
          (u, n, best["h"][0], best["h"][1], best["a"][0], best["a"][1], best["E"][0], best["E"][1]))
    print("            two-letter cube: h = %.9f a = %.9f E = %.9f;   uniform three-letter law: h = %.9f a = %.9f E = %.9f" %
          (hc, ac, Ec, h_of(su), dlib.a_site(su)[0], dlib.E_site(su)))
    print("            time %.1f s" % (time.time() - t0))

print("(b) local maximisation of h over three-letter laws at u = 0.5 (Nelder-Mead in logits, four starts)")
u = 0.5
def negh(z):
    w = np.exp(np.concatenate([[0.0], z])); pi = w / w.sum()
    return -h_of(site3(pi, u), grid=12)
bestv, bestpi = -1, None
for start in ([0.05, 0.5, 0.45], [0.045, 0.457, 0.498], [0.1, 0.45, 0.45], [0.02, 0.5, 0.48]):
    z0 = np.log(np.array(start[1:]) / start[0])
    res = minimize(negh, z0, method="Nelder-Mead", options={"xatol": 1e-5, "fatol": 1e-13, "maxiter": 220})
    w = np.exp(np.concatenate([[0.0], res.x])); pi = w / w.sum()
    print("   start %s -> law (%.5f, %.5f, %.5f), h = %.10f" % (start, pi[0], pi[1], pi[2], -res.fun))
    if -res.fun > bestv: bestv, bestpi = -res.fun, pi
print("   best found: (%.5f, %.5f, %.5f), h = %.10f;  cube %.10f;  excess %.3e (%.4f %%)   [SCI-REV-0001: (0.04502, 0.45679, 0.49819), 0.0076753]" %
      (bestpi[0], bestpi[1], bestpi[2], bestv, cube(u)[0], bestv - cube(u)[0], 100 * (bestv - cube(u)[0]) / cube(u)[0]))
print("   time %.1f s" % (time.time() - t0))

print("(c) two letters: second differences of F* on t = 0.02..0.98, step 0.01, 500 random sites (law, asymmetric envelope)")
rng = np.random.default_rng(2026)
ts = np.arange(0.02, 0.9801, 0.01)
ms = None
worst = -1e9; npos = 0; worst_site = None
for trial in range(500):
    p = float(rng.uniform(0.02, 0.98)); u1, u2 = float(rng.uniform(0.05, 7.0)), float(rng.uniform(0.05, 7.0))
    # the two vertices: g = gamma(1) - gamma(0) in {-u1, +u2}; Gibbs laws (1-p, p e^{-g}) normalised
    P = np.array([[1 - p, p * math.exp(u1)], [1 - p, p * math.exp(-u2)]]); P /= P.sum(axis=1, keepdims=True)
    F = np.empty(len(ts))
    for i, t in enumerate(ts):
        Pt = P ** t
        f = lambda m: -(((m * Pt[0] + (1 - m) * Pt[1]) ** (1 / t)).sum())      # maximise -N(m): N convex in m
        m, v = dlib.golden(f, 0.0, 1.0, tol=1e-12)
        F[i] = -t * math.log(-v)
    d2 = F[:-2] - 2 * F[1:-1] + F[2:]
    if d2.max() > worst: worst, worst_site = d2.max(), (p, u1, u2)
    npos += int((d2 > 1e-12).sum())
print("   largest second difference %.3e (site p = %.3f, u1 = %.2f, u2 = %.2f); number of positive second differences (> 1e-12): %d of %d" %
      (worst, worst_site[0], worst_site[1], worst_site[2], npos, 500 * (len(ts) - 2)))
print("time %.1f s" % (time.time() - t0))
