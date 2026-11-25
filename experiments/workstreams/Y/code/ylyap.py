"""Moment Lyapunov exponents of the random-bond Ising chain in a uniform field, and the Lyapunov form of the lower bound.

Xi_{kappa,eta}(b) = sum_{tau in {+-1}^n} exp( kappa sum_i b_i tau_i tau_{i+1} + eta sum_i tau_i )      (b_i = +-1, i = 1..n-1)
L_q(kappa, eta; r) = lim (1/n) ln E[ Xi(b)^r ],   b_i i.i.d. with P(b = -1) = q.

Transfer operator on the direction z = (1/2) ln(x_+/x_-) of the partial partition vector, z in [-kappa, kappa]:
   (T f)(z) = sum_b P(b) m_b(z+eta)^r f( zeta_b(z+eta) ),
   zeta_b(y) = (1/2) ln[cosh(kappa b + y)/cosh(kappa b - y)],   m_b(y) = 2 sqrt(cosh(kappa b + y) cosh(kappa b - y)).
Discretised by Chebyshev collocation (barycentric interpolation); L = ln(spectral radius)."""
import math, itertools
import numpy as np

def _cheb(N, a, b):
    j = np.arange(N); th = np.pi * (j + 0.5) / N
    x = np.cos(th); w = (-1.0) ** j * np.sin(th)
    return 0.5 * (a + b) + 0.5 * (b - a) * x, w

def _interp(nodes, w, y):
    """matrix ell_k(y_i) of the barycentric interpolant at first-kind Chebyshev nodes"""
    d = y[:, None] - nodes[None, :]
    hit = np.abs(d) < 1e-14
    d[hit] = 1.0
    c = w[None, :] / d
    M = c / c.sum(axis=1, keepdims=True)
    rows = hit.any(axis=1)
    M[rows] = hit[rows].astype(float)
    return M

def moment_lyap(kappa, eta, q, r, N=48):
    """L_q(kappa, eta; r);  q = P(bond = -kappa)."""
    if abs(kappa) < 1e-14: return r * math.log(2 * math.cosh(eta))
    kappa = abs(kappa)
    nodes, w = _cheb(N, -kappa, kappa)
    y = nodes + eta
    T = np.zeros((N, N))
    for b, pb in ((1.0, 1.0 - q), (-1.0, q)):
        if pb <= 0: continue
        cp = np.cosh(kappa * b + y); cm = np.cosh(kappa * b - y)
        zeta = 0.5 * np.log(cp / cm); m = 2 * np.sqrt(cp * cm)
        T += pb * (m ** r)[:, None] * _interp(nodes, w, zeta)
    ev = np.linalg.eigvals(T)
    return math.log(float(np.max(ev.real)))

def moment_exact(kappa, eta, q, r, n):
    """ln E[Xi(b)^r] for a chain of n sites by enumeration of the 2^(n-1) bond patterns"""
    B = np.array(list(itertools.product((1.0, -1.0), repeat=n - 1)))
    x = np.tile(np.array([math.exp(eta), math.exp(-eta)]), (len(B), 1))            # D 1
    lw = np.zeros(len(B))
    for i in range(n - 1):
        b = B[:, n - 2 - i]
        ep = np.exp(kappa * b); em = np.exp(-kappa * b)
        xp = ep * x[:, 0] + em * x[:, 1]; xm = em * x[:, 0] + ep * x[:, 1]         # T_b x
        x = np.stack([xp * math.exp(eta), xm * math.exp(-eta)], axis=1)            # D T_b x
        lw += np.where(b > 0, math.log(1 - q) if q < 1 else -np.inf, math.log(q) if q > 0 else -np.inf)
    lx = np.log(x.sum(axis=1)) * r + lw
    mx = lx.max()
    return mx + math.log(np.exp(lx - mx).sum())

def G_inf(t, c, p, u, N=48):
    """per-site Lyapunov lower bound for site-wise labels with the Z^t-tilted symmetric Markov label law of coupling c:
       G = L_{p_c}(K', h; t) - t L_p(c, t h; 1/t) - t ln(2 cosh K') + ln(2 cosh c),   K' = K/2, h = u/2, p_c = 1/(1+e^{2c})."""
    Kp = 0.5 * math.log((1 - p) / p); h = u / 2
    pc = 1.0 / (1.0 + math.exp(2 * c))
    return (moment_lyap(Kp, h, pc, t, N) - t * moment_lyap(c, t * h, p, 1.0 / t, N)
            - t * math.log(2 * math.cosh(Kp)) + math.log(2 * math.cosh(c)))

def G_finite(t, c, p, u, n):
    """the same for a chain of n sites (exact enumeration over bond patterns):
       G_t(M_c) = ln E_{beta~p_c}[Xi_{K',h}^t] - t ln E_{b~p}[Xi_{c,th}^{1/t}] - t ln Z0(K') + ln Z0(c),  Z0(x) = 2 (2 cosh x)^(n-1)"""
    Kp = 0.5 * math.log((1 - p) / p); h = u / 2
    pc = 1.0 / (1.0 + math.exp(2 * c))
    lz = lambda x: math.log(2) + (n - 1) * math.log(2 * math.cosh(x))
    return moment_exact(Kp, h, pc, t, n) - t * moment_exact(c, t * h, p, 1.0 / t, n) - t * lz(Kp) + lz(c)

def E_F(p, u):
    """closed-form lower bound for the threshold: ln[lambda_max(K', h)/(2 cosh K')]"""
    Kp = 0.5 * math.log((1 - p) / p); h = u / 2
    lam = math.exp(Kp) * math.cosh(h) + math.sqrt(math.exp(2 * Kp) * math.sinh(h) ** 2 + math.exp(-2 * Kp))
    return math.log(lam / (2 * math.cosh(Kp)))
