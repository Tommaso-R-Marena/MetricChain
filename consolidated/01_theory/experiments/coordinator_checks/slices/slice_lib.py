"""Uniform slices of the cube: block profiles inside one type class (coordinator's check library for theory report 11.25).

A profile in the slice of density kappa: blocks of fractions lam_j with densities mu_j, sum lam_j mu_j = kappa.
MI(mu) = sum_j lam_j KL(mu_j || kappa);  dist(nu, mu) = sum_j lam_j |nu_j - mu_j|.
r_slice(mu, e) = min{ MI(nu) : nu in the slice, u dist(nu, mu) <= e + MI(mu) }                       (hinted)
n_slice(mu, X) = min{ MI(nu) : nu in the slice, MI(nu) + u dist(nu, mu) - MI(mu) <= X }              (non-adaptive)
Binary centre of type m: F(lam) = m KL(kappa + lam/2m || kappa) + (1-m) KL(kappa - lam/(2(1-m)) || kappa),
Psi(s) = max_lam [s lam - F(lam)] = min_{th1 - th2 = 2s} [m Lam(th1) + (1-m) Lam(th2)],  Lam(th) = ln(1 - kappa + kappa e^th) - kappa th."""
import math
import numpy as np

def kl(a, b):
    a = min(max(a, 0.0), 1.0)
    t = 0.0
    if a > 0: t += a*math.log(a/b)
    if a < 1: t += (1-a)*math.log((1-a)/(1-b))
    return t

def golden(f, a, b, tol=1e-13, it=90):
    g = (math.sqrt(5) - 1)/2
    c, d = b - g*(b - a), a + g*(b - a)
    fc, fd = f(c), f(d)
    for _ in range(it):
        if b - a < tol: break
        if fc < fd: b, d, fd = d, c, fc; c = b - g*(b - a); fc = f(c)
        else: a, c, fc = c, d, fd; d = a + g*(b - a); fd = f(d)
    x = (a + b)/2
    return f(x), x

def bisect(f, a, b, it=60):
    """root of an increasing f on [a, b] (f(a) <= 0 <= f(b))"""
    for _ in range(it):
        m = (a + b)/2
        if f(m) <= 0: a = m
        else: b = m
    return (a + b)/2

# ---------- multi-block profiles: the inner problem by clipping (Lemma 11.77(a)); no duality used ----------
def klv(a, b):
    a = np.clip(np.asarray(a, float), 0.0, 1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(a > 0, a*np.log(a/b), 0.0) + np.where(a < 1, (1 - a)*np.log((1 - a)/(1 - b)), 0.0)
    return t

def MI(lam, mu, kappa): return float(np.dot(lam, klv(mu, kappa)))

def clip_profile(lam, mu, kappa, c_lo):
    """the clipping nu_j = min(max(mu_j, c_lo), c_hi) of type kappa (c_lo <= kappa); returns (nu, dist) or None"""
    lam = np.asarray(lam, float); mu = np.asarray(mu, float)
    lo = np.maximum(mu, c_lo)
    def typ(c_hi): return float(np.dot(lam, np.minimum(lo, c_hi))) - kappa
    if typ(1.0) < -1e-15: return None
    c_hi = bisect(typ, kappa, 1.0) if typ(kappa) < 0 else kappa
    nu = np.minimum(lo, c_hi)
    return nu, float(np.dot(lam, np.abs(nu - mu)))

def r_slice(lam, mu, kappa, u, e):
    """min MI(nu) over the slice subject to u dist(nu, mu) <= e + MI(mu)"""
    Bd = (e + MI(lam, mu, kappa))/u
    full = clip_profile(lam, mu, kappa, kappa)          # everything clipped to kappa: the mixed profile
    if full[1] <= Bd: return 0.0
    c = bisect(lambda c_lo: clip_profile(lam, mu, kappa, c_lo)[1] - Bd, 0.0, kappa)
    nu, d = clip_profile(lam, mu, kappa, c)
    return MI(lam, nu, kappa)

def n_slice(lam, mu, kappa, u, X):
    """min MI(nu) over the slice subject to MI(nu) + u dist(nu, mu) <= X + MI(mu)"""
    tot = X + MI(lam, mu, kappa)
    def g(c_lo):
        nu, d = clip_profile(lam, mu, kappa, c_lo)
        return MI(lam, nu, kappa) + u*d
    # along the clipping path MI decreases and dist increases; the constraint function need not be monotone: scan + bisect
    cs = np.linspace(0.0, kappa, 2001)
    best = math.inf
    vals = [g(c) for c in cs]
    for i, c in enumerate(cs):
        if vals[i] <= tot + 1e-15:
            nu, d = clip_profile(lam, mu, kappa, c)
            best = min(best, MI(lam, nu, kappa))
    # refine the last crossing
    for i in range(len(cs) - 1):
        if (vals[i] - tot)*(vals[i+1] - tot) < 0:
            a, b = cs[i], cs[i+1]
            for _ in range(80):
                m_ = (a + b)/2
                if (g(m_) - tot)*(vals[i] - tot) > 0: a = m_
                else: b = m_
            for c in (a, b):
                if g(c) <= tot + 1e-13:
                    nu, d = clip_profile(lam, mu, kappa, c)
                    best = min(best, MI(lam, nu, kappa))
    return best

# ---------- binary centres: closed forms ----------
def lam_range(m, kappa):
    """lam in (lo, hi): kappa + lam/2m in (0,1), kappa - lam/(2(1-m)) in (0,1)"""
    hi = min(2*m*(1 - kappa), 2*(1 - m)*kappa)
    lo = -min(2*m*kappa, 2*(1 - m)*(1 - kappa))
    return lo, hi

def F(m, kappa, lam): return m*kl(kappa + lam/(2*m), kappa) + (1 - m)*kl(kappa - lam/(2*(1 - m)), kappa)

def Lam(kappa, th): return np.logaddexp(math.log1p(-kappa), math.log(kappa) + th) - kappa*th

def Psi(m, kappa, s):
    """Legendre transform of F on lam >= 0 (s >= 0), computed as a maximum over lam"""
    if s <= 0: return 0.0
    hi = lam_range(m, kappa)[1]
    v, _ = golden(lambda l: -(s*l - F(m, kappa, l)), 0.0, hi*(1 - 1e-13))
    return -v

def Psi_dual(m, kappa, s):
    v, _ = golden(lambda t1: m*Lam(kappa, t1) + (1 - m)*Lam(kappa, t1 - 2*s), -60.0, 60.0 + 2*s)
    return float(v)

def V_binary(m, kappa, u, e):
    """sup over shells of the hinted value around a centre of type m: F((Psi(u) - e)_+ / u)"""
    P = Psi(m, kappa, u)
    return F(m, kappa, (P - e)/u) if P > e else 0.0

def V_binary_direct(m, kappa, u, e, grid=4001):
    hi = lam_range(m, kappa)[1]
    best = 0.0
    for l in np.linspace(0, hi*(1 - 1e-9), grid):
        x = l - (e + F(m, kappa, l))/u
        if x > 0: best = max(best, F(m, kappa, x))
    return best

def N_binary(m, kappa, u, X):
    """non-adaptive value around a centre of type m: F(lam_X), u lam_X - F(lam_X) = Psi(u) - X on the increasing branch"""
    P = Psi(m, kappa, u)
    if X >= P: return 0.0
    hi = lam_range(m, kappa)[1]
    _, lstar = golden(lambda l: -(u*l - F(m, kappa, l)), 0.0, hi*(1 - 1e-13))
    lx = bisect(lambda l: (u*l - F(m, kappa, l)) - (P - X), 0.0, lstar)
    return F(m, kappa, lx)

def Fstar(m, kappa, u, t): return t*Psi(m, kappa, u) - Psi(m, kappa, t*u)

def R_unif(u, e):
    L1 = math.log(2/(1 + math.exp(-u))); rho = (L1 + e)/u
    return kl(rho, 0.5) if rho < 0.5 else 0.0

def N_cube(u, x):
    """theta_na of the uniform cube: min{KL(rho || 1/2) : KL(rho || p_u) <= x}, p_u = 1/(1 + e^u)"""
    pu = 1/(1 + math.exp(u))
    if kl(0.5, pu) <= x: return 0.0
    rho = bisect(lambda r: kl(r, pu) - x, pu, 0.5)
    return kl(rho, 0.5)

def slice_best(kappa, u, e, ms=None):
    """sup over centre types of V_binary (golden search after a scan)"""
    ms = np.linspace(0.02, 0.98, 97) if ms is None else ms
    vals = [V_binary(m, kappa, u, e) for m in ms]
    i = int(np.argmax(vals))
    a, b = ms[max(i - 1, 0)], ms[min(i + 1, len(ms) - 1)]
    v, m = golden(lambda mm: -V_binary(mm, kappa, u, e), a, b, tol=1e-10)
    return -v, m
