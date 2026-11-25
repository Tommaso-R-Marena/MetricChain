"""Single-letter formulas for the p-biased binary cube with the Lipschitz class L_u.

Written from the statements of theory report §11.20 (Theorem 11.59) and §11.26 (Theorem 11.99),
and from R5_REPORT §4.1 (conventions for Renyi / Sibson / Augustin quantities).  Nothing imported
from the theory division's code.

Conventions
-----------
site alphabet {0,1}; reference site law pi = (q, p), p = P(x=1), theta = ln(q/p).
additive instance gamma (psi = gamma*|x|): Gibbs site law pi_gamma(1) = p e^{-gamma}/(q + p e^{-gamma})
    = 1/(1+exp(theta+gamma)).
vertex channel W: phi=0 -> pi_0 = pi_{gamma=+u} (cone centred at letter 0),
                  phi=1 -> pi_1 = pi_{gamma=-u} (cone centred at letter 1).
All logarithms natural.
"""
import numpy as np
from scipy.optimize import minimize_scalar, brentq, minimize

# ----------------------------------------------------------------------------- basics

def h2(x):
    x = np.clip(x, 1e-300, 1 - 1e-16)
    return -(x * np.log(x) + (1 - x) * np.log1p(-x))


def kl2(a, b):
    """binary KL(a||b) in nats"""
    a = min(max(a, 0.0), 1.0)
    out = 0.0
    if a > 0:
        out += a * np.log(a / b)
    if a < 1:
        out += (1 - a) * np.log((1 - a) / (1 - b))
    return out


def pgam(p, gamma):
    """pi_gamma(1)"""
    theta = np.log((1 - p) / p)
    return 1.0 / (1.0 + np.exp(theta + gamma))


def site_laws(p, u, gamma):
    """returns pi_gamma, pi_0, pi_1 as arrays [P(0), P(1)]"""
    pg = pgam(p, gamma)
    p0 = pgam(p, u)
    p1 = pgam(p, -u)
    return np.array([1 - pg, pg]), np.array([1 - p0, p0]), np.array([1 - p1, p1])


def gamma_of_density(p, c):
    """the gamma with pi_gamma(1) = c"""
    theta = np.log((1 - p) / p)
    return np.log((1 - c) / c) - theta


# ----------------------------------------------------------------------------- game function

def F_game(p, u, gamma, t):
    """F(gamma,t) = -ln val(K), K(a,phi) = (pi_phi(a)/pi_gamma(a))^t, 2x2 game solved exactly.
    Adversary mixes phi (minimises), sampler picks a (maximises)."""
    if t <= 0:
        return 0.0
    pg, p0, p1 = site_laws(p, u, gamma)
    K = np.array([[(p0[a] / pg[a]) ** t, (p1[a] / pg[a]) ** t] for a in (0, 1)])  # K[a,phi]
    # pure strategies of the adversary
    best = min(max(K[0, 0], K[1, 0]), max(K[0, 1], K[1, 1]))
    den = K[0, 0] - K[1, 0] + K[1, 1] - K[0, 1]
    m = None
    if abs(den) > 1e-300:
        mm = (K[0, 0] - K[1, 0]) / den
        if 0 <= mm <= 1:
            v = (1 - mm) * K[0, 0] + mm * K[0, 1]
            if v < best:
                best, m = v, mm
    return -np.log(best)


def game_opt_m(p, u, gamma, t):
    """optimal mixing weight m = M(phi=1) of the adversary in the game at (gamma,t)"""
    pg, p0, p1 = site_laws(p, u, gamma)
    K = np.array([[(p0[a] / pg[a]) ** t, (p1[a] / pg[a]) ** t] for a in (0, 1)])
    den = K[0, 0] - K[1, 0] + K[1, 1] - K[0, 1]
    mm = (K[0, 0] - K[1, 0]) / den
    return min(max(mm, 0.0), 1.0)


def F_closed(p, u, gamma, t):
    """closed form of Theorem 11.59(b)"""
    theta = np.log((1 - p) / p)
    lam, lp, lm = theta + gamma, theta + u, theta - u
    C = lambda x: 2 * np.cosh(x / 2)
    if t <= 0:
        return 0.0
    num = np.sinh(t * (lp - lam) / 2) * C(lm) ** t + np.sinh(t * (lam - lm) / 2) * C(lp) ** t
    return np.log(num / np.sinh(t * u)) - t * np.log(C(lam))


def sibson_G(p, u, m, t):
    """G_t(M) = -t ln sum_a (sum_phi M(phi) pi_phi(a)^t)^{1/t},  M = (1-m, m)"""
    _, p0, p1 = site_laws(p, u, 0.0)
    s = (1 - m) * p0 ** t + m * p1 ** t
    return -t * np.log(np.sum(s ** (1.0 / t)))


def Fstar(p, u, t, return_all=False):
    """F*(t) = max_M G_t(M) = max_gamma F(gamma,t); also the saddle (m*, Q*, gamma*)."""
    if t <= 0 or t >= 1:
        if return_all:
            return 0.0, None, None, None
        return 0.0
    res = minimize_scalar(lambda m: -sibson_G(p, u, m, t), bounds=(0, 1), method='bounded',
                          options={'xatol': 1e-14})
    m = res.x
    val = -res.fun
    if not return_all:
        return val
    _, p0, p1 = site_laws(p, u, 0.0)
    s = (1 - m) * p0 ** t + m * p1 ** t
    Q = s ** (1.0 / t)
    Q = Q / Q.sum()
    gstar = gamma_of_density(p, Q[1])
    return val, m, Q, gstar


def Fstar_via_gamma(p, u, t):
    res = minimize_scalar(lambda g: -F_game(p, u, g, t), bounds=(-u, u), method='bounded',
                          options={'xatol': 1e-13})
    return -res.fun, res.x


def _max_concave_1d(f, lo, hi, n=400):
    """maximise a (nearly) unimodal function on [lo,hi]: grid + golden refinement"""
    xs = np.linspace(lo, hi, n + 1)
    vals = np.array([f(x) for x in xs])
    i = int(np.argmax(vals))
    a = xs[max(i - 1, 0)]
    b = xs[min(i + 1, n)]
    res = minimize_scalar(lambda x: -f(x), bounds=(a, b), method='bounded', options={'xatol': 1e-13})
    if -res.fun >= vals[i]:
        return -res.fun, res.x
    return vals[i], xs[i]


def R_gamma(p, u, gamma, e, return_t=False):
    """hinted exponent of the additive instance gamma: max_{0<=t<=1} F(gamma,t) - t e"""
    val, t = _max_concave_1d(lambda t: F_game(p, u, gamma, t) - t * e, 0.0, 1.0)
    val = max(val, 0.0)
    return (val, t) if return_t else val


def Rmax(p, u, e, return_all=False):
    """R^max(e) = max_t F*(t) - t e ; returns also t*, and the saddle"""
    val, t = _max_concave_1d(lambda t: Fstar(p, u, t) - t * e, 1e-9, 1.0 - 1e-9)
    val = max(val, 0.0)
    if not return_all:
        return val
    _, m, Q, g = Fstar(p, u, t, return_all=True)
    return val, t, m, Q, g


def E_threshold(p, u):
    """E = sup_t F*(t)/t = lim_{t->0}"""
    t = 1e-6
    return Fstar(p, u, t) / t


def a_capacity(p, u):
    """Shannon capacity of the vertex channel = lim F*(t)/(1-t), computed directly"""
    _, p0, p1 = site_laws(p, u, 0.0)

    def mi(m):
        Q = (1 - m) * p0 + m * p1
        return (1 - m) * np.sum(p0 * np.log(p0 / Q)) + m * np.sum(p1 * np.log(p1 / Q))
    res = minimize_scalar(lambda m: -mi(m), bounds=(0, 1), method='bounded', options={'xatol': 1e-14})
    return -res.fun, res.x


def theta_na(p, u, x):
    """theta_na(x) = sup_{0<=tau<1} (F*(tau) - tau x)/(1-tau)   (R5.2(a); Prop 11.65 proof)"""
    f = lambda tau: (Fstar(p, u, tau) - tau * x) / (1 - tau)
    val, tau = _max_concave_1d(f, 1e-9, 1 - 1e-7, n=2000)
    return max(val, 0.0), tau


# ----------------------------------------------------------------------------- constant composition

def Rcc(p, u, gamma, m, e, tmax=60.0, return_all=False):
    """constant-composition exponent of plain dips with centre type m at the additive base gamma:
        min { I(M,V) : D(V||pi_phi|M) - D(V||pi_gamma|M) <= e }
      = max_{t>=0} min_Q [ - sum_phi M(phi) ln sum_a Q(a) r_phi(a)^t - t e ],  r_phi = pi_phi/pi_gamma.
    """
    pg, p0, p1 = site_laws(p, u, gamma)
    r = [p0 / pg, p1 / pg]
    Mv = [1 - m, m]

    def g(t):
        def G(y):
            out = 0.0
            for phi in (0, 1):
                if Mv[phi] > 0:
                    out -= Mv[phi] * np.log((1 - y) * r[phi][0] ** t + y * r[phi][1] ** t)
            return out
        res = minimize_scalar(G, bounds=(1e-12, 1 - 1e-12), method='bounded', options={'xatol': 1e-14})
        return res.fun, res.x

    val, t = _max_concave_1d(lambda t: g(t)[0] - t * e, 0.0, tmax, n=600)
    val = max(val, 0.0)
    if return_all:
        y = g(t)[1]
        # optimal conditional types V_phi ∝ Q r_phi^t
        V = []
        for phi in (0, 1):
            w = np.array([(1 - y) * r[phi][0] ** t, y * r[phi][1] ** t])
            V.append(w / w.sum())
        return val, t, y, V
    return val


def Rcc_primal(p, u, gamma, m, e):
    """the same by direct primal minimisation over (v0, v1) (check of the dual form)"""
    pg, p0, p1 = site_laws(p, u, gamma)
    Mv = np.array([1 - m, m])
    lr = [np.log(pg / p0), np.log(pg / p1)]   # ln(pi_gamma(a)/pi_phi(a))

    def I(v):
        y = Mv[0] * v[0] + Mv[1] * v[1]
        return Mv[0] * kl2(v[0], y) + Mv[1] * kl2(v[1], y)

    def con(v):  # e - sum M V ln(pi_gamma/pi_phi) >= 0
        s = 0.0
        for phi in (0, 1):
            s += Mv[phi] * ((1 - v[phi]) * lr[phi][0] + v[phi] * lr[phi][1])
        return e - s
    best = np.inf
    for v0 in (0.2, 0.5, 0.8):
        for v1 in (0.2, 0.5, 0.8):
            res = minimize(I, [v0, v1], constraints=[{'type': 'ineq', 'fun': con}],
                           bounds=[(1e-9, 1 - 1e-9)] * 2, method='SLSQP',
                           options={'ftol': 1e-15, 'maxiter': 500})
            if res.success and con(res.x) > -1e-9:
                best = min(best, res.fun)
    return max(best, 0.0)


def m_forced(p, u, gamma):
    """the centre type m with (MW)(1) = pi_gamma(1): the one-body matching equation for plain dips"""
    pg, p0, p1 = site_laws(p, u, gamma)
    return (pg[1] - p0[1]) / (p1[1] - p0[1])


def cone_density(p, u, m):
    _, p0, p1 = site_laws(p, u, 0.0)
    return (1 - m) * p0[1] + m * p1[1]


def R0_closed(p, u, e, return_m=False):
    """Theorem 11.59(c): R_0(e) = max_m [h(m) - h((Lambda_m + e)/u)]_+"""
    q = 1 - p
    L0 = -np.log(q + p * np.exp(-u))
    L1 = -np.log(p + q * np.exp(-u))

    def f(m):
        # rate-distortion function of a Bernoulli(m) source with Hamming distortion rho
        rho = ((1 - m) * L0 + m * L1 + e) / u
        if rho < 0:
            return h2(m)
        if rho >= min(m, 1 - m):
            return 0.0
        return h2(m) - h2(rho)
    val, m = _max_concave_1d(f, 1e-9, 1 - 1e-9, n=2000)
    return (max(val, 0.0), m) if return_m else max(val, 0.0)
