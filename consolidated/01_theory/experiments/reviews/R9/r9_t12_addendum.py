# R9 test 12: the coordinator's addendum (monotonicity of F*(t; theta) in |theta|), step by step, own code.
# Independent ingredients: F from the closed form of Theorem F2(b) (r9lib.Par.F, not the cosh form), F* by direct
# maximisation over gamma, derivatives by finite differences.
import numpy as np, sys, time
from math import log, exp, sinh, cosh, tanh
from scipy.optimize import minimize_scalar
from scipy.integrate import quad
from r9lib import Par
rng = np.random.default_rng(31); t0 = time.time()
C = lambda x: 2 * np.cosh(x / 2)
def I_th(x, th, u, t): return (np.sinh(t * (th + u - x) / 2) * C(th - u) ** t + np.sinh(t * (x - th + u) / 2) * C(th + u) ** t) / np.sinh(t * u)
def rho(x, th, u, t): return I_th(x, th, u, t) / C(x) ** t
def par(th, u): return Par(1 / (1 + exp(th)), u)          # theta = ln(q/p)
# (0) F(gamma,t) = ln rho_theta(theta+gamma): closed form (b) against the cosh form
d0 = 0.0
for _ in range(3000):
    th = rng.uniform(-5, 5); u = rng.uniform(0.1, 5); t = rng.uniform(0.02, 0.98); g = rng.uniform(-u, u)
    d0 = max(d0, abs(float(par(th, u).F(g, t)) - log(rho(th + g, th, u, t))))
print(f"(0) |F closed form (b) - ln rho_theta(theta+gamma)| <= {d0:.1e}  (3000 random points)")
# (i) the ODE for rho, and unimodality
d1 = 0.0; nbad = 0
for _ in range(2000):
    th = rng.uniform(-5, 5); u = rng.uniform(0.1, 5); t = rng.uniform(0.02, 0.98); x = th + rng.uniform(-0.95, 0.95) * u; hh = 1e-4
    r0, rp, rm = rho(x, th, u, t), rho(x + hh, th, u, t), rho(x - hh, th, u, t)
    res = (rp - 2 * r0 + rm) / hh ** 2 + t * tanh(x / 2) * (rp - rm) / (2 * hh) + t * (1 - t) / 4 / cosh(x / 2) ** 2 * r0
    d1 = max(d1, abs(res))
    xs = th + np.linspace(-u, u, 4001); dr = np.diff(rho(xs, th, u, t))
    sc = int(np.sum(np.sign(dr[1:]) != np.sign(dr[:-1])))
    nbad += (sc != 1) or not (dr[0] > 0 and dr[-1] < 0)
print(f"(i) residual of rho'' + t tanh(x/2) rho' + (t(1-t)/4) sech^2(x/2) rho = 0 (finite differences): <= {d1:.1e}; cases in which rho is not increasing-then-decreasing on the window: {nbad} of 2000")
# (ii) the derivative at gamma = 0
d2 = 0.0; nsign = 0; nmono = 0
for _ in range(3000):
    th = rng.uniform(0.01, 6); u = rng.uniform(0.1, 5); t = rng.uniform(0.02, 0.98); P = par(th, u); eps = 1e-5
    fd = (float(P.F(eps, t)) - float(P.F(-eps, t))) / (2 * eps)
    A = (log(cosh((th + u) / 2)) - log(cosh((th - u) / 2))) / u
    form = (t / 2) * (tanh(t * u * A / 2) / tanh(t * u / 2) - tanh(th / 2))
    d2 = max(d2, abs(fd - form)); nsign += not (form < 0)
    tt = np.linspace(0.01, 1.0, 200); qq = np.tanh(tt * u * A / 2) / np.tanh(tt * u / 2)
    nmono += not (np.all(np.diff(qq) > -1e-13) and abs(qq[-1] - tanh(th / 2)) < 1e-12 and 0 < A < 1)
print(f"(ii) |d/dgamma F(0,t) - (t/2)[tanh(t u A/2)/tanh(t u/2) - tanh(theta/2)]| <= {d2:.1e}; not negative (theta > 0): {nsign} of 3000; quotient not increasing in t, or != tanh(theta/2) at t = 1, or A not in (0,1): {nmono}")
# (iii), (iv): envelope formula and the comparison of the two averages
d3 = 0.0; nineq = 0; ngam = 0; ncont = 0; ndec = 0; margin = np.inf
for _ in range(1500):
    th = rng.uniform(0.02, 6); u = rng.uniform(0.1, 5); t = rng.uniform(0.03, 0.97)
    def Fst(thv):
        Pv = par(thv, u)
        gs = np.linspace(-u, u, 4001); v = Pv.F(gs, t); i = int(np.argmax(v))
        r = minimize_scalar(lambda g: -float(Pv.F(g, t)), bounds=(gs[max(i - 1, 0)], gs[min(i + 1, 4000)]), method='bounded', options={'xatol': 1e-14})
        return -r.fun, r.x
    F0, gst = Fst(th); hh = 1e-4
    fd = (Fst(th + hh)[0] - Fst(th - hh)[0]) / (2 * hh)
    Pq = (th - u) / 2 + t * (u - gst) / 2; Qq = (th + u) / 2 - t * (u + gst) / 2
    xst = th + gst
    form = (t / 2) * 2 ** t * (cosh((th - u) / 2) ** (t - 1) * cosh(Pq) - cosh((th + u) / 2) ** (t - 1) * cosh(Qq)) / (I_th(xst, th, u, t) * sinh(t * u))
    d3 = max(d3, abs(fd - form))
    lhs = log(cosh(Qq)) - log(cosh(Pq)); rhs = (1 - t) * (log(cosh((th + u) / 2)) - log(cosh((th - u) / 2)))
    nineq += not (lhs >= rhs - 1e-13); margin = min(margin, (lhs - rhs) / ((1 - t) * u))
    ngam += not (gst < 0)
    ncont += not ((th - u) / 2 - 1e-12 <= Pq and Qq <= (th + u) / 2 + 1e-12 and abs((Qq - Pq) - (1 - t) * u) < 1e-12 and (Pq + Qq) / 2 > th / 2)
    ndec += not (fd < 0)
print(f"(iii) |dF*/dtheta (finite differences of the maximum) - envelope formula| <= {d3:.1e}; gamma* >= 0: {ngam}; [P,Q] not inside the window / wrong length / centre not to the right: {ncont}; dF*/dtheta >= 0: {ndec}  (1500 random (theta > 0, u, t))")
print(f"      inequality ln cosh Q - ln cosh P >= (1-t)[ln cosh((theta+u)/2) - ln cosh((theta-u)/2)]: violated {nineq} times; least (avg over [P,Q] - avg over the window) = {margin:.2e}")
# (iv) the lemma for random odd increasing functions that are concave on [0, inf)
fams = [lambda x, a: np.tanh(a * x), lambda x, a: 1 - np.exp(-a * x), lambda x, a: x / (1 + a * x), lambda x, a: np.log1p(a * x),
        lambda x, a: np.minimum(x, a), lambda x, a: np.sqrt(x) * a, lambda x, a: np.minimum(2 * x, x + a)]
nb = 0; ntest = 0; worst = 0.0
for _ in range(3000):
    f0 = fams[rng.integers(0, len(fams))]; aa = rng.uniform(0.2, 5)
    f = lambda x: np.sign(x) * f0(np.abs(x), aa)
    c = rng.uniform(0, 4) * rng.choice([0.0, 1.0, 1.0, 1.0])
    rs = np.sort(rng.uniform(0.01, 8, 6))
    xs = np.linspace(-1, 1, 20001)
    av = [float(np.mean(f(c + r * xs))) for r in rs]             # midpoint-type average on a fine grid
    dv = np.diff(av); ntest += 1; nb += np.any(dv > 2e-6); worst = max(worst, float(dv.max()))
print(f"(iv) lemma: average of f over [c-r, c+r] nonincreasing in r (c >= 0): {nb} violations in {ntest} random (f, c, radii); largest increase {worst:.1e} (quadrature error ~1e-6)")
# necessity of the hypothesis c >= 0 / oddness: a mutation
f = lambda x: np.tanh(x); xs = np.linspace(-1, 1, 20001)
print(f"      (mutation: c = -1 < 0: averages over r = 0.5, 2 are {np.mean(f(-1 + 0.5 * xs)):.4f}, {np.mean(f(-1 + 2 * xs)):.4f} -- increasing, as it should be for c < 0)")
# consequences: F*, R^max, E, a, theta_na nonincreasing in |theta|, even in theta
nv = 0
for u in (0.3, 1.0, 2.0, 4.0):
    prev = None
    for th in np.linspace(0, 6, 25):
        P = par(th, u); ts, Fs, Gs = P.table(nt=1001, ng=801)
        Em = P.E()[0]; a = -P.ec(); Pm = par(-th, u); tsm, Fsm, Gsm = Pm.table(nt=1001, ng=801)
        even = float(np.max(np.abs(Fs - Fsm)))
        cur = (Fs.copy(), Em, a, max(float(np.max(Fs - ts * 0.02)), 0.0))
        sign_ok = (th == 0) or np.all(Gs[5:-5] < 0)
        if prev is not None:
            nv += not (np.all(cur[0] <= prev[0] + 1e-12) and cur[1] <= prev[1] + 1e-12 and cur[2] <= prev[2] + 1e-9 and cur[3] <= prev[3] + 1e-12)
        nv += (even > 1e-10) or (not sign_ok)
        prev = cur
print(f"consequences on a grid (u in {{0.3,1,2,4}}, theta = 0, 0.25, ..., 6, 1001 values of t): violations of [F* even in theta, F*, E, a, R^max(0.02) nonincreasing in theta, gamma*(t) < 0 for theta > 0]: {nv}   [{time.time()-t0:.0f}s]")
