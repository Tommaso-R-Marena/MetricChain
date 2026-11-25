"""Own check of the compensation lemma and of Theorem A of the science division's workstream F (SCI-RES-0006).
Exact enumeration on the cube Q_n, n <= 12.  Nothing imported from that division."""
import math, itertools, sys
import numpy as np

def cube(n):
    X = np.array(list(itertools.product((0, 1), repeat=n)), dtype=np.int8)
    return X, X.sum(axis=1)

def lip_ok(w, n, u, tol=1e-11):
    """w > 0 on the cube (index = binary number, first coordinate most significant) is in the class iff
    |ln w(x) - ln w(x^i)| <= u for all x, i."""
    lw = np.log(w).reshape((2,) * n)
    worst = 0.0
    for i in range(n):
        a = np.take(lw, 0, axis=i); b = np.take(lw, 1, axis=i)
        worst = max(worst, float(np.abs(a - b).max()))
    return worst <= u + tol, worst

def marginals(pi, w, X):
    m = pi * w
    return (m[:, None] * X).sum(axis=0) / m.sum()

def run(n, p, u, gam, k, r, verbose=True):
    X, wt = cube(n)
    q = 1 - p
    pi = p ** wt * q ** (n - wt)
    pg = lambda g: p * math.exp(-g) / (q + p * math.exp(-g))
    wtil = lambda g: np.exp(-g * wt) / (q + p * math.exp(-g)) ** n
    pm, pp = pg(u), pg(-u)                       # window
    Z0, Z1 = q + p * math.exp(-u), p + q * math.exp(-u)
    def cone(s):
        d = np.abs(X - s[None, :]).sum(axis=1)
        return np.exp(-u * d) / (Z0 ** (n - s.sum()) * Z1 ** s.sum())
    base = wtil(gam)
    s = np.array([1] * k + [0] * (n - k), dtype=np.int8)
    shifts = [np.roll(s, j) for j in range(n)]
    D = [np.maximum(math.exp(r) * cone(t) - base, 0.0) for t in shifts]
    Dbar = sum(D) / n
    E = float((pi * Dbar).sum()); c = float((pi * Dbar * wt).sum() / (n * E))
    c0 = (1 - k / n) * pm + (k / n) * pp
    out = dict(n=n, k=k, r=r, E=E, c=c, c0=c0, pgam=pg(gam))
    assert math.exp(r) - 1 - 1e-12 <= E <= math.exp(r) + 1e-12, "Lemma 2: mass"
    assert abs(c - c0) <= 1 / (math.exp(r) - 1) + 1e-12, "Lemma 2: density"
    if not (pm < c < pp):
        out["window"] = False
        return out
    p2, g2 = (pp, -u) if c > pg(gam) else (pm, u)
    b = (c - pg(gam)) / (p2 - c)
    w0 = base + b * wtil(g2); w1 = w0 + Dbar
    ok0, l0 = lip_ok(w0, n, u); ok1, l1 = lip_ok(w1, n, u)
    assert ok0 and ok1, ("membership", l0, l1)
    m0, m1 = marginals(pi, w0, X), marginals(pi, w1, X)
    out.update(b=b, marg_err=float(max(np.abs(m0 - c).max(), np.abs(m1 - c).max())))
    assert out["marg_err"] < 1e-12, "all one-body marginals equal c"
    gap = math.log((pi * w1).sum() / (pi * w0).sum())
    assert abs(gap - math.log(1 + E / (1 + b))) < 1e-12, "gap"
    # control: without the compensator the marginals differ by Phi/(1+Phi) (c - p_gamma)
    mu1 = marginals(pi, base + Dbar, X)
    assert np.abs(mu1 - (pg(gam) + E / (1 + E) * (c - pg(gam)))).max() < 1e-12, "criterion (c)"
    out.update(gap=gap, unmatched=float(E / (1 + E) * (c - pg(gam))))
    # counting: H = max_x P_{s uniform in T_k}[x in D_{s,r}], against (n+1) e^{tr} rho_t(k/n; gamma)^n
    Tk = [np.array(t, dtype=np.int8) for t in itertools.product((0, 1), repeat=n) if sum(t) == k]
    cnt = np.zeros(len(X))
    for t in Tk:
        cnt += (math.exp(r) * cone(t) > base)
    H = float(cnt.max() / len(Tk))
    pi0, pi1, pig = (1 - pm, pm), (1 - pp, pp), (1 - pg(gam), pg(gam))
    m = k / n
    best = math.inf
    for t in np.linspace(0, 3, 301):
        rho = max((1 - m) * (pi0[a] / pig[a]) ** t + m * (pi1[a] / pig[a]) ** t for a in (0, 1))
        best = min(best, (n + 1) * math.exp(t * r) * rho ** n)
    out.update(H=H, markov=best)
    assert H <= best * (1 + 1e-12), "H <= (n+1) e^{tr} rho^n"
    # a point lies in the support of Dbar_s for at most n * #{s : x in D_s} centres: check the support identity
    supp = (Dbar > 0)
    assert (supp == (sum((d > 0) for d in D) > 0)).all()
    out["lower_bound_evals"] = 1 / (n * H)
    return out

if __name__ == "__main__":
    rng = np.random.default_rng(20261125)
    worst = 0.0
    for case in range(24):
        n = int(rng.integers(6, 11)); p = float(rng.uniform(0.1, 0.9)); u = float(rng.uniform(0.5, 2.0))
        gam = float(rng.uniform(-u, u)); k = int(rng.integers(1, n)); r = float(rng.uniform(0.5, 4.0))
        o = run(n, p, u, gam, k, r)
        if o.get("window", True):
            worst = max(worst, o["marg_err"])
            print(f"n={n} p={p:.3f} u={u:.2f} gam={gam:+.2f} k={k} r={r:.2f}: c={o['c']:.4f} (c0={o['c0']:.4f}, p_gam={o['pgam']:.4f}) b={o['b']:.4f} "
                  f"gap={o['gap']:.4f} unmatched={o['unmatched']:+.2e} marg_err={o['marg_err']:.1e} H={o['H']:.3e} <= {o['markov']:.3e}")
        else:
            print(f"n={n} p={p:.3f} u={u:.2f} gam={gam:+.2f} k={k} r={r:.2f}: excess density {o['c']:.4f} outside the window (c0={o['c0']:.4f}); no compensation")
    print("worst marginal error", worst)
