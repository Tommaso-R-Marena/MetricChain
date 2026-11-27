"""Search heuristics for GEOMETRY-REQ-0006 (floating point and non-rigorous high precision).

NOT TRUSTED.  Nothing here concludes an inequality of a certificate: these functions only propose
the objects that the trusted code then checks (couplings, approximate maximisers, approximate
four-dimensional realisations, control instances).
"""
from __future__ import annotations

from fractions import Fraction as Fr

import numpy as np
from flint import arb, arb_mat

from gr6_kernel import ma_eval, point, to_fraction
from gr6_model import derivative, nerf_chain, statewise_pairs


# ------------------------------------------------------------------ stress and couplings
def rigidity_matrix(X, edges):
    n, dim = X.shape
    R = np.zeros((len(edges), n * dim))
    for e, (i, j) in enumerate(edges):
        R[e, dim * i:dim * i + dim] = X[i] - X[j]
        R[e, dim * j:dim * j + dim] = X[j] - X[i]
    return R


def stress(X, edges):
    """(omega, Omega, singular values): a unit left null vector of the rigidity matrix (the
    equilibrium stress when the last singular value is the only vanishing one), its stress
    matrix, and the singular values of the transposed rigidity matrix."""
    n = X.shape[0]
    R = rigidity_matrix(X, edges)
    _, s, Vt = np.linalg.svd(R.T)
    om = Vt[-1]
    Om = np.zeros((n, n))
    for w, (i, j) in zip(om, edges):
        Om[i, i] += w
        Om[j, j] += w
        Om[i, j] -= w
        Om[j, i] -= w
    return om, Om, s


def energy_float(tors, pairs, c):
    X = nerf_chain(tors)
    return float(sum(ci * ((X[i] - X[j]) ** 2).sum() for (i, j), ci in zip(pairs, c)))


def hessian_float(fun, x, h=1e-4):
    x = np.asarray(x, float)
    m = len(x)
    H = np.zeros((m, m))
    for a in range(m):
        for b in range(m):
            ea, eb = np.eye(m)[a] * h, np.eye(m)[b] * h
            H[a, b] = (fun(x + ea + eb) - fun(x + ea - eb) - fun(x - ea + eb) + fun(x - ea - eb)) / (4 * h * h)
    return (H + H.T) / 2


def couplings(tors, pairs):
    """c = s * omega|_F for the unit stress omega of (F u E0, X(tors)), the sign s chosen so that
    the Hessian of H_c in the torsions is negative definite at tors (the convention of the
    request).  Returns (c, info); c is None if the Hessian is not definite."""
    X = nerf_chain(tors)
    n = X.shape[0]
    E0 = statewise_pairs(n)
    om, Om, sv = stress(X, E0 + list(pairs))
    c = om[len(E0):]
    hv = np.linalg.eigvalsh(hessian_float(lambda t: energy_float(t, pairs, c), tors))
    ev = np.linalg.eigvalsh(Om)
    info = dict(stress_singular_values_tail=sv[-2:].tolist(), stress_eigenvalues=ev.tolist())
    if hv.max() < 0:
        s = 1.0
    elif hv.min() > 0:
        s = -1.0
    else:
        return None, info
    info["hessian_eigenvalues"] = sorted((s * hv).tolist())
    info["stress_eigenvalues_signed"] = sorted((s * ev).tolist())
    return s * c, info


def round_couplings(c, digits=6):
    return [Fr(int(round(float(x) * 10 ** digits)), 10 ** digits) for x in c]


# ------------------------------------------------------------------ approximate critical points
def refine_critical(form, tors, iterations=60):
    """Newton iteration for grad H = 0 in ball arithmetic at the working precision, started at the
    torsions `tors` (radians).  Returns the centre as exact dyadic rationals in units of pi and
    the size of the last step.  (Approximation only: the trusted Krawczyk test certifies.)"""
    nv = len(tors)
    grad = [derivative(form, k) for k in range(nv)]
    hess = [[derivative(grad[k], l) for l in range(nv)] for k in range(nv)]
    tau = [(arb(float(t)) / arb.pi()).mid() for t in tors]
    last = None
    for _ in range(iterations):
        P = [point(t) for t in tau]
        g = arb_mat(nv, 1, [ma_eval(gk, P).mid() for gk in grad])
        Hm = arb_mat(nv, nv, [ma_eval(hess[k][l], P).mid() for k in range(nv) for l in range(nv)])
        step = Hm.solve(g)
        tau = [(tau[k] - step[k, 0] / arb.pi()).mid() for k in range(nv)]
        size = max(float(abs(step[k, 0]).mid()) for k in range(nv))
        if last is not None and size >= last and size < 1e-30:
            break
        last = size
    return [to_fraction(t) for t in tau], last


def form_float(form):
    """A numpy evaluator t -> form(t) (radians) and the coefficient tensor of a form."""
    nv = len(next(iter(form)))
    h = np.zeros((3,) * nv)
    for alpha, v in form.items():
        h[alpha] = float(v.mid())

    def fun(t):
        out = h
        for x in t:
            out = np.tensordot(np.array([1.0, np.cos(x), np.sin(x)]), out, axes=(0, 0))
        return float(out)

    return fun, h


def local_maxima(form, starts=400, seed=0):
    """Distinct local maxima of a form found by BFGS from random starts: [(value, torsions)],
    by decreasing value, one representative of each pair +-theta."""
    from scipy.optimize import minimize

    fun, _ = form_float(form)
    nv = len(next(iter(form)))
    rng = np.random.default_rng(seed)
    found = []
    for _ in range(starts):
        r = minimize(lambda t: -fun(t), rng.uniform(-np.pi, np.pi, nv), method="BFGS", options=dict(gtol=1e-11))
        t = (r.x + np.pi) % (2 * np.pi) - np.pi
        if t[np.argmax(np.abs(t) > 1e-6)] < 0:
            t = -t
        if not any(abs(v - (-r.fun)) < 1e-8 and np.abs(np.angle(np.exp(1j * (t - u)))).max() < 1e-4 for v, u in found):
            found.append((-r.fun, t))
    found.sort(key=lambda p: -p[0])
    return found


# ------------------------------------------------------------------ four-dimensional realisations
def _unknowns(n):
    from gr6_qb_proof import gauge_unknowns

    return gauge_unknowns(n)


def residual_jacobian(Y, edges, unknowns, target):
    f = np.array([((Y[i] - Y[j]) ** 2).sum() - t for (i, j), t in zip(edges, target)])
    J = np.zeros((len(edges), len(unknowns)))
    col = {u: k for k, u in enumerate(unknowns)}
    for e, (i, j) in enumerate(edges):
        for a in range(Y.shape[1]):
            if (i, a) in col:
                J[e, col[(i, a)]] += 2 * (Y[i, a] - Y[j, a])
            if (j, a) in col:
                J[e, col[(j, a)]] -= 2 * (Y[i, a] - Y[j, a])
    return f, J


def realise_4d(X, edges, Om, trials=300, seed=0, tol=1e-12, iterations=60):
    """Candidate realisations in R^4 with the lengths of X (n x 3, in the chain gauge) on `edges`.

    Start from X with a fourth coordinate h q, q an isotropic vector of the stress matrix
    (q^T Omega q = 0: the second-order condition for a flex out of the hyperplane; a random
    vector if the stress is semidefinite) made to vanish on the atoms 0..3, and run minimum-norm
    Gauss-Newton with step control on the gauged system.  Returns [(sigma_4, Y)] for the runs
    that converged to a solution of the length equations (possibly a flat one), by decreasing
    sigma_4."""
    n = X.shape[0]
    rng = np.random.default_rng(seed)
    unknowns = _unknowns(n)
    target = np.array([((X[i] - X[j]) ** 2).sum() for (i, j) in edges])
    lam, vec = np.linalg.eigh(Om)
    scale = np.abs(lam).max()
    pos, neg = vec[:, lam > 1e-9 * scale], vec[:, lam < -1e-9 * scale]
    aff = np.hstack([np.ones((4, 1)), X[:4]])                 # affine functions on the atoms 0..3
    out = []
    for _ in range(trials):
        if pos.shape[1] and neg.shape[1]:
            a, b = rng.normal(size=pos.shape[1]), rng.normal(size=neg.shape[1])
            qp, qn = pos @ a, neg @ b
            q = qp / np.sqrt(qp @ Om @ qp) + qn / np.sqrt(-(qn @ Om @ qn))
        else:
            q = rng.normal(size=n)
        q = q - np.hstack([np.ones((n, 1)), X]) @ np.linalg.solve(aff, q[:4])
        q /= np.abs(q).max()
        Y = np.hstack([X, rng.uniform(0.05, 0.9) * q[:, None]])
        ok = False
        for _ in range(iterations):
            f, J = residual_jacobian(Y, edges, unknowns, target)
            if np.abs(f).max() < tol:
                ok = True
                break
            step = np.linalg.lstsq(J, -f, rcond=None)[0]
            t = 1.0
            while True:
                Z = Y.copy()
                for k, (i, a_) in enumerate(unknowns):
                    Z[i, a_] += t * step[k]
                if np.linalg.norm(residual_jacobian(Z, edges, unknowns, target)[0]) < np.linalg.norm(f) or t < 1e-4:
                    break
                t /= 2
            Y = Z
        if ok:
            out.append((float(np.linalg.svd(Y - Y.mean(0), compute_uv=False)[3]), Y))
    out.sort(key=lambda p: -p[0])
    return out


def newton_float(Y, edges, free, target, iterations=50):
    """Floating-point Newton iteration on the square system in the unknowns `free`; returns
    (Y, max residual) (inf if the iteration breaks down)."""
    Y = Y.copy()
    for _ in range(iterations):
        f, J = residual_jacobian(Y, edges, free, target)
        if np.abs(f).max() < 1e-15:
            break
        try:
            step = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return Y, float("inf")
        if not np.all(np.isfinite(step)) or np.abs(step).max() > 1.0:
            return Y, float("inf")
        for k, (i, a) in enumerate(free):
            Y[i, a] += step[k]
    return Y, float(np.abs(residual_jacobian(Y, edges, free, target)[0]).max())


def choose_pins(Y, edges):
    """The unknown coordinates to pin so that the gauged length system becomes square with the
    best-conditioned Jacobian at Y.  Returns (pins, condition number)."""
    from itertools import combinations

    unknowns = _unknowns(Y.shape[0])
    extra = len(unknowns) - len(edges)
    assert extra >= 0
    _, J = residual_jacobian(Y, edges, unknowns, np.zeros(len(edges)))
    best = None
    for pins in combinations(range(len(unknowns)), extra):
        keep = [k for k in range(len(unknowns)) if k not in pins]
        s = np.linalg.svd(J[:, keep], compute_uv=False)
        cond = s[0] / s[-1] if s[-1] > 0 else np.inf
        if best is None or cond < best[1]:
            best = ([unknowns[k] for k in pins], float(cond))
    return best


def refine_square(free, f, jac, z0, iterations=60):
    """Newton iteration in ball arithmetic (midpoints) for a square system given by the trusted
    f and jac of qb_proof.length_system, started at the floats z0.  Returns (centre as exact
    balls, max |f| at the centre as a float).  Approximation only."""
    m = len(free)
    z = [arb(float(x)) for x in z0]
    for _ in range(iterations):
        fz = [v.mid() for v in f(z)]
        J = jac(z)
        try:
            step = arb_mat(m, m, [J[i][j].mid() for i in range(m) for j in range(m)]).solve(arb_mat(m, 1, fz))
        except ZeroDivisionError:
            break
        z = [(z[k] - step[k, 0]).mid() for k in range(m)]
        if max(float(abs(step[k, 0]).mid()) for k in range(m)) < 2.0 ** -170:
            break
    return z, max(float(abs(v).mid()) for v in f(z))
