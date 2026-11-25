"""Assistant D's helpers.  Own code; the harness is imported read-only as a library (its st_* helpers)."""
import importlib.util, math, sys
import os
import numpy as np
from scipy.optimize import linprog, minimize

HARNESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "falsify_conjectures.py")


def load_harness():
    argv = sys.argv
    sys.argv = ["x"]
    spec = importlib.util.spec_from_file_location("fc_harness", HARNESS)
    mod = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(mod)
    sys.argv = argv
    return mod


# ---------------------------------------------------------------- own implementation (independent of st_*)
def vertices(d):
    """Vertices of {g : g[a]-g[b] <= d[a][b]} modulo constants (g[0] = 0), by enumeration of bases."""
    import itertools
    d = np.asarray(d, float)
    q = len(d)
    cons = [(a, b) for a in range(q) for b in range(q) if a != b]
    out = []
    for S in itertools.combinations(cons, q - 1):
        A = np.zeros((q - 1, q - 1)); rhs = np.zeros(q - 1)
        for i, (a, b) in enumerate(S):
            if a > 0: A[i, a - 1] += 1
            if b > 0: A[i, b - 1] -= 1
            rhs[i] = d[a, b]
        if abs(np.linalg.det(A)) < 1e-12:
            continue
        g = np.concatenate([[0.0], np.linalg.solve(A, rhs)])
        if all(g[a] - g[b] <= d[a, b] + 1e-10 for a, b in cons) and not any(np.allclose(g, h, atol=1e-9) for h in out):
            out.append(g)
    return np.array(out)


def gibbs(pi, g):
    w = np.asarray(pi, float) * np.exp(-np.asarray(g, float))
    return w / w.sum()


class Site:
    def __init__(self, pi, d):
        self.pi = np.asarray(pi, float); self.d = np.asarray(d, float)
        self.V = vertices(self.d)
        self.P = np.array([gibbs(self.pi, phi) for phi in self.V])   # rows: Gibbs laws of the vertices
        self.q = len(self.pi)


def renyi(site, t, starts=6, seed=0):
    """F*(t) = max_M -t ln sum_a (sum_phi M pi_phi^t)^(1/t); returns (primal value, dual bound, M, Q).
    Convex programme in M: exponentiated-gradient / SLSQP polish; the dual bound certifies."""
    Pt = site.P ** t
    nv = len(Pt)

    def N(M):
        return float(((M @ Pt) ** (1 / t)).sum())

    def dN(M):
        return (Pt * ((M @ Pt) ** (1 / t - 1))[None, :]).sum(axis=1) / t

    best = None
    rng = np.random.default_rng(seed)
    for s in range(starts):
        M0 = np.ones(nv) / nv if s == 0 else rng.dirichlet(np.ones(nv))
        res = minimize(N, M0, jac=dN, method="SLSQP", bounds=[(0, 1)] * nv,
                       constraints=[{"type": "eq", "fun": lambda M: M.sum() - 1, "jac": lambda M: np.ones(nv)}],
                       options={"ftol": 1e-16, "maxiter": 1000})
        M = np.clip(res.x, 0, None); M /= M.sum()
        # polish by multiplicative updates (Arimoto-type), keeps the simplex
        for _ in range(200):
            g = dN(M)
            M2 = M * np.exp(-(g - g.min()) * 0.5 / max(g.max(), 1e-300))
            M2 /= M2.sum()
            if N(M2) < N(M): M = M2
            else: break
        m = (M @ Pt) ** (1 / t)
        Q = m / m.sum()
        val = -t * math.log(N(M))
        upper = max(-math.log(float((Pt[i] * Q ** (1 - t)).sum())) for i in range(nv))
        if best is None or val > best[0]:
            best = (val, upper, M, Q)
        if upper - val < 1e-11:
            break
    return best


def Fstar(chain, t):
    if t <= 1e-13 or t >= 1 - 1e-13:
        return 0.0
    return sum(l * renyi(s, t)[0] for l, s in chain)


def golden(f, a, b, tol=1e-11):
    """maximise f on [a,b] by golden section; returns (argmax, max)."""
    gr = (math.sqrt(5) - 1) / 2
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol:
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a); fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a); fd = f(d)
    x = 0.5 * (a + b)
    return x, f(x)


def Rhat(chain, e, grid=80):
    ts = np.linspace(0, 1, grid + 1)
    vals = [Fstar(chain, t) - t * e for t in ts]
    i = int(np.argmax(vals))
    t, v = golden(lambda t: Fstar(chain, t) - t * e, ts[max(i - 1, 0)], ts[min(i + 1, grid)])
    return max(v, max(vals), 0.0), t


def theta_na(chain, x, grid=80, tmax=0.999):
    ts = np.linspace(0, tmax, grid + 1)
    vals = [(Fstar(chain, t) - t * x) / (1 - t) for t in ts]
    i = int(np.argmax(vals))
    t, v = golden(lambda t: (Fstar(chain, t) - t * x) / (1 - t), ts[max(i - 1, 0)], ts[min(i + 1, grid)])
    return max(v, max(vals), 0.0)


def E_site(site):
    lP = np.log(site.P); nv = len(lP)
    best = None
    for s in range(4):
        M0 = np.ones(nv) / nv if s == 0 else np.random.default_rng(s).dirichlet(np.ones(nv))
        res = minimize(lambda M: math.log(float(np.exp(M @ lP).sum())), M0, method="SLSQP", bounds=[(0, 1)] * nv,
                       constraints=[{"type": "eq", "fun": lambda M: M.sum() - 1}], options={"ftol": 1e-16, "maxiter": 1000})
        if best is None or -res.fun > best:
            best = -float(res.fun)
    return best


def a_site(site, iters=200000, tol=1e-15):
    """Shannon capacity by Blahut-Arimoto, with the dual bound max_phi KL(pi_phi || Q)."""
    P = site.P
    M = np.ones(len(P)) / len(P)
    for _ in range(iters):
        Q = M @ P
        D = (P * np.log(P / Q[None, :])).sum(axis=1)
        lo, hi = float(M @ D), float(D.max())
        if hi - lo < tol:
            break
        M = M * np.exp(D - D.max()); M /= M.sum()
    return lo, hi


def hamming(q, u):
    return [[0.0 if a == b else u for b in range(q)] for a in range(q)]


SITES = dict(
    bin=([0.7, 0.3], hamming(2, 1.0)),
    path=([0.5, 0.3, 0.2], [[0, 0.8, 2.4], [0.8, 0, 1.6], [2.4, 1.6, 0]]),
    tri=([0.2, 0.5, 0.3], [[0, 1.0, 2.0], [1.0, 0, 1.5], [2.0, 1.5, 0]]),
    asym=([0.5, 0.3, 0.2], [[0, 1, 2], [0.5, 0, 1.5], [1, 0.5, 0]]),
)
