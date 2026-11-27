"""Referee R11 -- own helper library, written from the statements of Y_REPORT.md
(no code of the workstream or of the repository is imported or copied).

Conventions (as in the report, section 1):
  spins s in {+1,-1}^n ; binary symmetric chain pi(s) = (1/2) prod_i P(s_i, s_{i+1}),
  P(a,a) = 1-p, P(a,-a) = p ;  K = ln((1-p)/p), K' = K/2 ;  slope u per site, h = u/2.
  class C_d = { psi : |psi(x)-psi(y)| <= u * Hamming(x,y) } (symmetric Hamming envelope).
  Gibbs law pi_phi ~ pi e^{-phi};  G_t(M) = -t ln sum_x ( sum_phi M(phi) pi_phi(x)^t )^(1/t).
"""
import numpy as np


# ----------------------------------------------------------------------------- basic objects
def configs(n):
    """all s in {+1,-1}^n, shape (2^n, n); row index = integer whose bit i is 1 iff s_i = -1."""
    idx = np.arange(2 ** n, dtype=np.int64)
    bits = (idx[:, None] >> np.arange(n)[None, :]) & 1
    return (1 - 2 * bits).astype(np.int8)


def chain_law(n, p):
    """stationary binary symmetric chain of n sites with flip probability p."""
    s = configs(n).astype(np.int64)
    nflip = ((s[:, :-1] * s[:, 1:]) == -1).sum(axis=1) if n > 1 else np.zeros(2 ** n, dtype=int)
    pi = 0.5 * p ** nflip * (1.0 - p) ** (n - 1 - nflip)
    return s, pi


def logsumexp(a, axis=None):
    a = np.asarray(a, dtype=float)
    m = np.max(a, axis=axis, keepdims=True)
    out = m + np.log(np.sum(np.exp(a - m), axis=axis, keepdims=True))
    if axis is None:
        return float(out.reshape(()))
    return np.squeeze(out, axis=axis)


def gibbs_logs(logpi, phis):
    """rows: log pi_phi for each label phi (array labels x configs)."""
    a = logpi[None, :] - phis
    return a - logsumexp(a, axis=1)[:, None]


def is_lipschitz(psi, n, slopes, tol=1e-10):
    """largest violation of |psi(x) - psi(x^i)| <= slopes[i] over all edges of the cube
    (for a sum-of-sites envelope checking single flips is equivalent to checking all pairs).
    Returns max over edges of |diff| - slope  (<= tol means admissible)."""
    idx = np.arange(2 ** n)
    worst = -np.inf
    for i in range(n):
        d = np.abs(psi[idx] - psi[idx ^ (1 << i)]) - slopes[i]
        worst = max(worst, float(d.max()))
    return worst


# ----------------------------------------------------------------------------- game function
def G_of_M(logP, M, t):
    """G_t(M) = -t ln sum_x ( sum_phi M(phi) P_phi(x)^t )^(1/t);  logP: labels x configs."""
    sup = M > 0
    a = t * logP[sup] + np.log(M[sup])[:, None]
    lm = logsumexp(a, axis=0) / t          # ln m(x)
    return -t * logsumexp(lm)


def centre_of_M(logP, M, t):
    """ln Q, Q the Renyi centre ~ (sum_phi M pi_phi^t)^(1/t)."""
    sup = M > 0
    a = t * logP[sup] + np.log(M[sup])[:, None]
    lm = logsumexp(a, axis=0) / t
    return lm - logsumexp(lm)


def renyi_div_term(logP, logQ, t):
    """(1-t) D_t(P_phi || Q) = -ln sum_x P_phi^t Q^(1-t), for every row."""
    return -logsumexp(t * logP + (1.0 - t) * logQ[None, :], axis=1)


def maximise_G(logP, t, M0=None, iters=200000, tol=1e-11, verbose=False):
    """Arimoto-type multiplicative iteration for max_M G_t(M) with the duality bracket
    [G_t(M), max_phi (1-t) D_t(pi_phi || Q_M)] (weak duality = Hoelder, checked by hand).
    Returns (lower, upper, M)."""
    nl = logP.shape[0]
    M = np.full(nl, 1.0 / nl) if M0 is None else M0.copy()
    lo = up = None
    for it in range(iters):
        logQ = centre_of_M(logP, M, t)
        dv = renyi_div_term(logP, logQ, t)          # (1-t) D_t(P_phi||Q)
        lo = G_of_M(logP, M, t)
        up = float(dv.max())
        if up - lo < tol:
            break
        # Arimoto step: M <- M * c_phi^(-t/(1-t)),  c_phi = sum_x P^t Q^(1-t) = exp(-dv)
        w = np.log(np.maximum(M, 1e-300)) + (t / (1.0 - t)) * dv
        w -= w.max()
        M = np.exp(w)
        M /= M.sum()
        if verbose and it % 1000 == 0:
            print(it, lo, up)
    return lo, up, M


def _support(M, prune, cap=200):
    """indices kept for the SLSQP polish: weights above prune * max, at most `cap` of them."""
    keep = M > prune * M.max()
    if keep.sum() > cap:
        thr = np.sort(M)[-cap]
        keep = M >= thr
    return keep


def maximise_G_fast(logP, t, M0=None, n_arimoto=400, polish=True, prune=1e-9):
    """max_M G_t(M) by an over-relaxed Arimoto iteration (step halved whenever the objective
    does not improve, so the iteration is monotone) followed by an SLSQP polish on the support.
    Returns (lower, upper, M): lower = G_t(M) evaluated from scratch, upper = the dual value
    max_phi (1-t) D_t(pi_phi || Q_M) over ALL rows of logP (weak duality)."""
    from scipy.optimize import minimize
    A = np.exp(t * logP)
    nl = A.shape[0]

    def fg(M, AA):
        mt = M @ AA
        m = mt ** (1.0 / t)
        S = m.sum()
        return np.log(S), (AA @ (m / mt)) / (t * S)

    M = np.full(nl, 1.0 / nl) if M0 is None else M0 / M0.sum()
    val, g = fg(M, A)
    eta = 1.0
    for it in range(n_arimoto):
        dv = -np.log(g * t) - t * val                 # (1-t) D_t(P_phi || Q_M)
        while True:
            w = np.log(np.maximum(M, 1e-300)) + eta * (t / (1.0 - t)) * dv
            Mn = np.exp(w - w.max())
            Mn /= Mn.sum()
            vn, gn = fg(Mn, A)
            if vn <= val + 1e-15 or eta <= 1.0:
                break
            eta = max(1.0, eta / 2)
        M, val, g = Mn, vn, gn
        eta = min(eta * 1.3, 64.0)
    if polish:
        keep = _support(M, prune)
        A2 = A[keep]
        x0 = M[keep] / M[keep].sum()
        res = minimize(lambda x: fg(x, A2), x0, jac=True, method='SLSQP', bounds=[(0.0, 1.0)] * x0.size,
                       constraints=[dict(type='eq', fun=lambda x: x.sum() - 1.0, jac=lambda x: np.ones_like(x))],
                       options=dict(maxiter=1000, ftol=1e-15))
        Mp = np.zeros(nl)
        Mp[keep] = np.maximum(res.x, 0.0)
        Mp /= Mp.sum()
        if G_of_M(logP, Mp, t) >= G_of_M(logP, M, t):
            M = Mp
    lo = G_of_M(logP, M, t)
    up = float(renyi_div_term(logP, centre_of_M(logP, M, t), t).max())
    return lo, up, M


def maximise_E(logP, iters=200000, tol=1e-11):
    """E = min_Q max_phi KL(Q||pi_phi) = max_M -ln sum_x prod_phi pi_phi(x)^M(phi).
    Exponentiated gradient with the duality bracket.  Returns (lower, upper, M)."""
    nl = logP.shape[0]
    M = np.full(nl, 1.0 / nl)
    step = 1.0
    best = (-np.inf, np.inf, M)
    for it in range(iters):
        lg = M @ logP                                  # ln geometric mean (unnormalised)
        lz = logsumexp(lg)
        lo = -lz
        logQ = lg - lz
        Q = np.exp(logQ)
        kl = (Q * logQ).sum() - logP @ Q               # KL(Q||pi_phi)
        up = float(kl.max())
        if lo > best[0]:
            best = (lo, min(up, best[1]), M.copy())
        if up - lo < tol:
            break
        w = np.log(np.maximum(M, 1e-300)) + step * (kl - kl.max())
        M = np.exp(w - w.max())
        M /= M.sum()
    return best


def maximise_E_fast(logP, prune=1e-9):
    """E = max_M -ln sum_x prod_phi pi_phi(x)^M(phi) = min_Q max_phi KL(Q||pi_phi):
    exponentiated gradient followed by an SLSQP polish on the support; returns (lower, upper, M)
    with upper = max_phi KL(Q_M || pi_phi) over ALL rows (weak duality)."""
    from scipy.optimize import minimize
    lo0, up0, M = maximise_E(logP, iters=3000, tol=1e-12)
    nl = logP.shape[0]
    keep = _support(M, prune)
    lPk = logP[keep]

    def fg(x):
        lg = x @ lPk
        mx = lg.max()
        w = np.exp(lg - mx)
        S = w.sum()
        return mx + np.log(S), lPk @ (w / S)

    x0 = M[keep] / M[keep].sum()
    res = minimize(fg, x0, jac=True, method='SLSQP', bounds=[(0.0, 1.0)] * x0.size,
                   constraints=[dict(type='eq', fun=lambda x: x.sum() - 1.0, jac=lambda x: np.ones_like(x))],
                   options=dict(maxiter=2000, ftol=1e-15))
    Mp = np.zeros(nl)
    Mp[keep] = np.maximum(res.x, 0.0)
    Mp /= Mp.sum()

    def bracket(Mx):
        lg = Mx @ logP
        lz = logsumexp(lg)
        logQ = lg - lz
        Q = np.exp(logQ)
        kl = (Q * logQ).sum() - logP @ Q
        return -lz, float(kl.max())
    b1, b2 = bracket(M), bracket(Mp)
    if b2[1] - b2[0] < b1[1] - b1[0]:
        return b2[0], b2[1], Mp
    return b1[0], b1[1], M


def maximise_a(logP, iters=200000, tol=1e-11):
    """a = min_Q max_phi KL(pi_phi||Q) = Shannon capacity; Blahut-Arimoto with bracket."""
    nl = logP.shape[0]
    P = np.exp(logP)
    M = np.full(nl, 1.0 / nl)
    for it in range(iters):
        Q = M @ P
        logQ = np.log(Q)
        kl = (P * (logP - logQ[None, :])).sum(axis=1)
        lo = float(M @ kl)
        up = float(kl.max())
        if up - lo < tol:
            break
        w = np.log(np.maximum(M, 1e-300)) + kl - kl.max()
        M = np.exp(w)
        M /= M.sum()
    return lo, up, M


# ----------------------------------------------------------------------------- scalar optimisation
def golden_max(f, a, b, tol=1e-9):
    g = (np.sqrt(5.0) - 1.0) / 2.0
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol:
        if fc < fd:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
        else:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
    x = 0.5 * (a + b)
    return x, f(x)


# ----------------------------------------------------------------------------- closed forms
def cube_F(t, u=1.0):
    """game function of the uniform cube per site: t ln cosh(u/2) - ln cosh(t u/2)."""
    h = u / 2.0
    return t * np.log(np.cosh(h)) - np.log(np.cosh(t * h))


def cube_constants(u=1.0):
    h = u / 2.0
    ts, hval = golden_max(lambda t: cube_F(t, u), 1e-6, 1 - 1e-6)
    E = np.log(np.cosh(h))
    a = h * np.tanh(h) - np.log(np.cosh(h))
    return hval, ts, a, E


def E_F(p, u=1.0):
    h = u / 2.0
    return np.log((1 - p) * np.cosh(h) + np.sqrt((1 - p) ** 2 * np.sinh(h) ** 2 + p ** 2))


# ----------------------------------------------------------------------------- moment Lyapunov exponents
def moment_lyapunov(mats, probs, r, N=64, side='left', return_fun=False):
    """ln of the growth rate of E[ (1^T A_1 A_2 ... A_k 1)^r ] for i.i.d. positive 2x2 matrices
    A_j drawn from `mats` with probabilities `probs`.
    Transfer operator on the direction x in (0,1) of the positive row vector v = (x, 1-x):
        (T f)(x) = sum_a probs[a] * |v A_a|_1^r * f( dir(v A_a) ),
    discretised by Chebyshev collocation on the smallest interval that contains the images of
    the simplex under all maps (so the operator maps functions on that interval to itself)."""
    mats = [np.asarray(A, dtype=float) for A in mats]
    probs = np.asarray(probs, dtype=float)

    def image(A, x):
        w0 = x * A[0, 0] + (1 - x) * A[1, 0]
        w1 = x * A[0, 1] + (1 - x) * A[1, 1]
        s = w0 + w1
        return s, w0 / s

    # invariant interval: images of the end points 0 and 1 (maps are monotone Moebius maps)
    lo, hi = 1.0, 0.0
    for A in mats:
        for x in (0.0, 1.0):
            _, y = image(A, x)
            lo, hi = min(lo, y), max(hi, y)
    if hi - lo < 1e-13:              # all matrices of rank one in the same direction
        lo, hi = lo - 1e-6, hi + 1e-6
    # Chebyshev nodes on [lo, hi]
    k = np.arange(N)
    z = np.cos(np.pi * (k + 0.5) / N)                 # nodes in (-1, 1)
    x = 0.5 * (lo + hi) + 0.5 * (hi - lo) * z

    def cheb_eval_matrix(y):
        """matrix E with f(y_i) = sum_j E[i, j] f(x_j) for the interpolant through the nodes."""
        zy = (2 * y - (lo + hi)) / (hi - lo)
        zy = np.clip(zy, -1.0, 1.0)
        Ty = np.cos(np.outer(np.arccos(zy), np.arange(N)))          # T_m(zy)
        Tx = np.cos(np.outer(np.arccos(z), np.arange(N)))           # T_m(z_j)
        c = np.full(N, 2.0 / N)
        c[0] = 1.0 / N
        # f ~ sum_m a_m T_m, a_m = c_m sum_j f(x_j) T_m(z_j)
        return Ty @ (c[:, None] * Tx.T)

    Top = np.zeros((N, N))
    for A, pa in zip(mats, probs):
        if pa == 0:
            continue
        s, y = image(A, x)
        Top += pa * (s ** r)[:, None] * cheb_eval_matrix(y)
    ev = np.linalg.eigvals(Top)
    lam = float(np.max(ev.real))
    if return_fun:
        return np.log(lam), (x, Top)
    return np.log(lam)


def exact_moment(mats, probs, r, k, left=None, right=None):
    """E[(left^T A_1 ... A_k right)^r] by a full enumeration of the product (|mats|^k terms),
    organised as a list of (probability, row vector)."""
    left = np.ones(2) if left is None else left
    right = np.ones(2) if right is None else right
    vecs = np.array([left], dtype=float)
    pr = np.array([1.0])
    for _ in range(k):
        newv = []
        newp = []
        for A, pa in zip(mats, probs):
            if pa == 0:
                continue
            newv.append(vecs @ A)
            newp.append(pr * pa)
        vecs = np.concatenate(newv, axis=0)
        pr = np.concatenate(newp, axis=0)
    return float((pr * (vecs @ right) ** r).sum())


# ----------------------------------------------------------------------------- Ising-chain pieces
def Xi_matrices(kappa, eta):
    """transfer matrices of Xi_{kappa,eta}(b) = sum_tau exp(kappa sum b_i tau_i tau_{i+1} + eta sum tau_i):
    row vector v_i(tau_i) (partial sums including the field of site i), v_{i+1} = v_i T(b),
    T(b)[tau, tau'] = exp(kappa b tau tau' + eta tau'), tau in (+1, -1)."""
    tau = np.array([1.0, -1.0])
    out = {}
    for b in (1, -1):
        out[b] = np.exp(kappa * b * np.outer(tau, tau) + eta * tau[None, :])
    return out


def L_moment(q, kappa, eta, r, N=64):
    """L_q(kappa, eta; r) = lim n^-1 ln E[Xi_{kappa,eta}(b)^r], bonds i.i.d., P(b=-1) = q."""
    T = Xi_matrices(kappa, eta)
    return moment_lyapunov([T[1], T[-1]], [1 - q, q], r, N=N)


def Xi_exact_moment(q, kappa, eta, r, n):
    """E[Xi_{kappa,eta}(b)^r] for a chain of n sites (n-1 bonds), exact enumeration of bonds."""
    T = Xi_matrices(kappa, eta)
    left = np.exp(eta * np.array([1.0, -1.0]))
    return exact_moment([T[1], T[-1]], [1 - q, q], r, n - 1, left=left, right=np.ones(2))


# ----------------------------------------------------------------------------- vertices of a Lipschitz polytope of a small cube
def lipschitz_vertices(L, slopes, tol=1e-9):
    """all vertices (modulo constants; normalised f(0) = 0, index 0 = all +1) of
    { f on {+-1}^L : |f(x) - f(x^i)| <= slopes[i] }.
    A point of this polytope is a vertex iff its tight edges connect the cube; so every vertex is
    obtained from a spanning tree of the cube graph with a sign on every tree edge.  L <= 3."""
    import itertools
    N = 2 ** L
    edges = [(x, x ^ (1 << i), i) for x in range(N) for i in range(L) if x < x ^ (1 << i)]
    verts = {}
    for tree in itertools.combinations(range(len(edges)), N - 1):
        # connectivity by union-find
        parent = list(range(N))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a
        ok = True
        for e in tree:
            a, b, _ = edges[e]
            ra, rb = find(a), find(b)
            if ra == rb:
                ok = False
                break
            parent[ra] = rb
        if not ok:
            continue
        adj = {x: [] for x in range(N)}
        for e in tree:
            a, b, i = edges[e]
            adj[a].append((b, e))
            adj[b].append((a, e))
        for signs in itertools.product((1.0, -1.0), repeat=N - 1):
            sg = dict(zip(tree, signs))
            f = np.full(N, np.nan)
            f[0] = 0.0
            stack = [0]
            while stack:
                a = stack.pop()
                for b, e in adj[a]:
                    if np.isnan(f[b]):
                        ea, eb, i = edges[e]
                        # f(eb) - f(ea) = sign * slope
                        f[b] = f[a] + (sg[e] * slopes[i] if a == ea else -sg[e] * slopes[i])
                        stack.append(b)
            if all(abs(f[a] - f[b]) <= slopes[i] + tol for a, b, i in edges):
                verts[tuple(np.round(f, 9))] = f
    return np.array(list(verts.values()))


def maximise_a_fast(logP, n_ba=3000, prune=1e-10):
    """Shannon capacity max_M I(M) = min_Q max_phi KL(pi_phi||Q): Blahut-Arimoto, then an SLSQP polish
    on the support; bracket [I(M), max_phi KL(pi_phi||Q_M)] over all rows (weak duality)."""
    from scipy.optimize import minimize
    lo, up, M = maximise_a(logP, iters=n_ba, tol=1e-13)
    P = np.exp(logP)
    nl = P.shape[0]
    keep = _support(M, prune)
    Pk, lPk = P[keep], logP[keep]

    def fg(x):
        Q = x @ Pk
        kl = (Pk * (lPk - np.log(Q)[None, :])).sum(axis=1)
        return -float(x @ kl), -(kl - 1.0)

    x0 = M[keep] / M[keep].sum()
    res = minimize(fg, x0, jac=True, method='SLSQP', bounds=[(0.0, 1.0)] * x0.size,
                   constraints=[dict(type='eq', fun=lambda x: x.sum() - 1.0, jac=lambda x: np.ones_like(x))],
                   options=dict(maxiter=2000, ftol=1e-15))
    Mp = np.zeros(nl)
    Mp[keep] = np.maximum(res.x, 0.0)
    Mp /= Mp.sum()

    def bracket(Mx):
        Q = Mx @ P
        kl = (P * (logP - np.log(Q)[None, :])).sum(axis=1)
        return float(Mx @ kl), float(kl.max())
    b1, b2 = bracket(M), bracket(Mp)
    if b2[1] - b2[0] < b1[1] - b1[0]:
        return b2[0], b2[1], Mp
    return b1[0], b1[1], M
