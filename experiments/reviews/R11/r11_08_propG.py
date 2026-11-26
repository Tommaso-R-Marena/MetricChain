"""R11 / 08 -- Proposition G (the tilt-state recursion): own derivation, own safe discretisation.

Own form of the constraint (*):  with  a(m) = ln((1-p)e^m + p),  abar(m) = a(m) - m,
c(m) = ln(p e^m + 1-p),  cbar(m) = c(m) - m,   the unique theta's are
      theta_- = lam - a(mu_+) + c(mu_-),        theta_+ = lam - abar(mu_+) + cbar(mu_-),
so (lam, mu_+, mu_-) is admissible iff both lie in [-u, u]  (and all tilts in [-u*, u*]).

(1) brute force on random members of the class: the tilts of pi_phi satisfy this, |lam| <= u*,
    and sum_x pi_phi^t Q^(1-t) = sum_x prod_i tau^t q^(1-t);
(2) finite chain n = 3: exact maximum of (1-t) D_t(pi_phi || Q) over ALL 38 vertices against
    my safe finite-horizon recursion (must be >=, and close if the relaxation is tight);
(3) safe upper bounds for F_inf(t) with W piecewise constant on a grid of G cells (any positive W
    gives a bound; every relaxation step is on the safe side: the feasible set of each cell pair is
    enlarged to the union over the cells, the stage factors are their minima over the cell);
    then h <= sup_t and E <= (reward version, reference Q = pi).

Run:  python3 r11_08_propG.py test            (parts 1, 2; < 1 min)
      python3 r11_08_propG.py h 0.3 [G]       (part 3 for one p; several minutes)
      python3 r11_08_propG.py E 0.3 [G]
      python3 r11_08_propG.py a 0.3 [G]       (capacity-type bound for a)
"""
import sys, time
import numpy as np
from r11lib import *

T0 = time.time()
u = 1.0
BIG = 1e200
TLIM = 480.0          # seconds available for the adaptive refinement in t


def ustar(p):
    g = lambda x: np.log(((1 - p) * np.exp(x) + p) / (p * np.exp(x) + 1 - p))
    x = u
    for _ in range(1000):
        x = u + g(x)
    return x


class Grid:
    """cells [e_k, e_{k+1}] of [-u*, u*];  feasible ranges of the cell of mu_+ for (cell of lam, cell of mu_-)."""

    def __init__(self, p, G, lam_cells=None):
        self.p, self.G = p, G
        us = ustar(p)
        self.us = us
        e = np.linspace(-us, us, G + 1)
        self.e = e
        D = e[1] - e[0]
        self.D = D
        a_inv = lambda y: np.where(np.exp(y) > p, np.log(np.maximum(np.exp(y) - p, 1e-300) / (1 - p)), -np.inf)
        abar_inv = lambda y: np.where(np.exp(y) > 1 - p, -np.log(np.maximum(np.exp(y) - (1 - p), 1e-300) / p), np.inf)
        c = lambda m: np.log(p * np.exp(m) + 1 - p)
        cbar = lambda m: np.log(p + (1 - p) * np.exp(-m))
        l1, l2 = e[:-1][:, None], e[1:][:, None]              # lam cell i
        m1, m2 = e[:-1][None, :], e[1:][None, :]              # mu_- cell j
        L1 = l1 + c(m1) - u
        U1 = l2 + c(m2) + u
        L2 = l1 + cbar(m2) - u
        U2 = l2 + cbar(m1) + u
        with np.errstate(divide='ignore', invalid='ignore'):
            lo = np.maximum(np.maximum(a_inv(L1), np.where(np.exp(U2) > 1 - p, abar_inv(U2), np.inf)), -us)
            hi = np.minimum(np.minimum(np.where(np.exp(U1) > p, a_inv(U1), -np.inf),
                                       np.where(np.exp(L2) > 1 - p, abar_inv(L2), np.inf)), us)
        feas = lo <= hi
        klo = np.clip(np.floor((lo + us) / D - 1e-9), 0, G - 1)
        khi = np.clip(np.floor((hi + us) / D + 1e-9), 0, G - 1)
        klo = np.where(feas, klo, 0).astype(np.int32)
        khi = np.where(feas, khi, 0).astype(np.int32)
        self.feas, self.klo, self.khi = feas, klo, khi
        ln = (khi - klo + 1).astype(np.int64)
        self.lev = np.floor(np.log2(np.maximum(ln, 1))).astype(np.int32)
        self.r2 = (khi - (1 << self.lev) + 1).astype(np.int32)
        self.nlev = int(self.lev.max()) + 1

    def rmq(self, w, mode='min'):
        """range minimum (maximum) of w over [klo, khi] for every cell pair."""
        op = np.minimum if mode == 'min' else np.maximum
        st = [w]
        for l in range(1, self.nlev):
            prev = st[-1]
            sh = 1 << (l - 1)
            cur = prev.copy()
            cur[: self.G - sh] = op(prev[: self.G - sh], prev[sh:])
            st.append(cur)
        st = np.array(st)
        return op(st[self.lev, self.klo], st[self.lev, self.r2])

    def stage_min(self, t, qt):
        """minima over the cells of A_+(lam) = tau_lam(+,+)^t (1-qt)^(1-t), A_-(lam) = tau_lam(+,-)^t qt^(1-t)."""
        p = self.p
        tp = lambda lam: (1 - p) * np.exp(lam / 2) / ((1 - p) * np.exp(lam / 2) + p * np.exp(-lam / 2))
        Ap = tp(self.e[:-1]) ** t * (1 - qt) ** (1 - t)            # increasing in lam: minimum at the left end
        Am = (1 - tp(self.e[1:])) ** t * qt ** (1 - t)            # decreasing: minimum at the right end
        return Ap, Am

    def T(self, w, Ap, Am):
        """safe lower bound of (T W)(+, lam) for lam in each cell; W(+, mu) = w, W(-, mu) = w(-mu)."""
        rm = self.rmq(w, 'min')                                    # (i, j): min of w over admissible cells of mu_+
        val = Ap[:, None] * rm + Am[:, None] * w[::-1][None, :]    # cell j of mu_- -> W(-, mu_-) = w[G-1-j]
        val = np.where(self.feas, val, BIG)
        return val.min(axis=1)

    def rate(self, t, qt, iters=4000, tol=1e-10, w0=None):
        """-ln max over iterates of min_i (T w)_i / w_i : an upper bound for F_inf(t) (any w is allowed)."""
        Ap, Am = self.stage_min(t, qt)
        w = np.ones(self.G) if w0 is None else w0.copy()
        best = 0.0
        for it in range(iters):
            Tw = self.T(w, Ap, Am)
            r = Tw / w
            cmin, cmax = r.min(), r.max()
            best = max(best, cmin)
            if cmax - cmin < tol * cmax:
                break
            w = Tw / Tw.max()
        return -np.log(best), -np.log(cmax), w, it

    # ---------------------------------------------------------------- threshold (rewards), Q = pi
    def E_rate(self, iters=20000, tol=1e-10):
        p = self.p
        tp = lambda lam: (1 - p) * np.exp(lam / 2) / ((1 - p) * np.exp(lam / 2) + p * np.exp(-lam / 2))
        k = lambda lam: (1 - p) * np.log((1 - p) / tp(lam)) + p * np.log(p / (1 - tp(lam)))
        kmax = np.maximum(k(self.e[:-1]), k(self.e[1:]))            # convex in lam: maximum over a cell at its ends
        w = np.zeros(self.G)
        best = np.inf
        for it in range(iters):
            rm = self.rmq(w, 'max')
            val = (1 - p) * rm + p * w[::-1][None, :]
            val = np.where(self.feas, val, -BIG)
            Tw = kmax + val.max(axis=1)
            d = Tw - w
            best = min(best, d.max())
            if d.max() - d.min() < tol:
                break
            w = Tw - Tw.max()
        return best, d.min(), it


def a_rate(gr, qt, iters=20000, tol=1e-10):
    """safe upper bound for the growth of  W -> KL(tau_lam(b,.) || q(b,.)) + max sum_a tau_lam(b,a) W(a, mu_a)
    (the capacity-type bound: a_inf <= growth, reference = symmetric Markov chain with flip probability qt).
    Over a cell of lam: the reward is quasi-convex in lam (maximum at an end of the cell) and the
    expectation is linear in tau_lam(+,+), which is monotone in lam (maximum at an end of the cell)."""
    p = gr.p
    tp = lambda lam: (1 - p) * np.exp(lam / 2) / ((1 - p) * np.exp(lam / 2) + p * np.exp(-lam / 2))
    kl = lambda lam: tp(lam) * np.log(tp(lam) / (1 - qt)) + (1 - tp(lam)) * np.log((1 - tp(lam)) / qt)
    kmax = np.maximum(kl(gr.e[:-1]), kl(gr.e[1:]))
    t1, t2 = tp(gr.e[:-1])[:, None], tp(gr.e[1:])[:, None]
    w = np.zeros(gr.G)
    best = np.inf
    for it in range(iters):
        rm = gr.rmq(w, 'max')
        wm = w[::-1][None, :]
        val = np.maximum(t1 * rm + (1 - t1) * wm, t2 * rm + (1 - t2) * wm)
        val = np.where(gr.feas, val, -BIG)
        Tw = kmax + val.max(axis=1)
        d = Tw - w
        best = min(best, d.max())
        if d.max() - d.min() < tol:
            break
        w = Tw - Tw.max()
    return best, d.min(), it


def a_bound(p, G):
    gr = Grid(p, G)
    f = lambda q: a_rate(gr, q)[0]
    a, b = 0.5 * p, min(3.0 * p, 0.5)
    g = (np.sqrt(5.0) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = f(c), f(d)
    while b - a > 2e-3 * p:
        if fc > fd:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
        else:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
    q = c if fc < fd else d
    v = min(fc, fd)
    vp = f(p)
    print(f"p={p} G={G}: a_inf <= {min(v, vp):.6f}  (best q~ = {q if v <= vp else p:.4f}; at q~ = p: {vp:.6f});"
          f"  cube a = {cube_constants(u)[2]:.6f};  report (G = 801): 0.121446 (0.4), 0.140860 (0.3), 0.160745 (0.2), 0.192774 (0.1)   [{time.time()-T0:.0f} s]", flush=True)


def test():
    rng = np.random.default_rng(5)
    print("== (1) the constraint (*) and the chain rule, brute force on random members ==")
    worst_th = -np.inf
    worst_lam = -np.inf
    worst_id = 0.0
    worst_star = 0.0
    for rep in range(60):
        n = int(rng.integers(3, 8))
        p = float(rng.choice([0.4, 0.3, 0.2, 0.1]))
        t = float(rng.uniform(0.1, 0.9))
        qt = float(rng.uniform(0.05, 0.5))
        us = ustar(p)
        s, pi = chain_law(n, p)
        N = 2 ** n
        idx = np.arange(N)
        ham = np.zeros((N, N))
        for i in range(n):
            ham += (s[:, i][:, None] != s[:, i][None, :])
        g = rng.normal(0, rng.uniform(0.5, 3), size=N)
        phi = (g[None, :] + u * ham).min(axis=1)
        if rng.uniform() < 0.5:                                  # a vertex-like member: cone or site-wise label
            phi = u * ham[:, rng.integers(0, N)]
        w = pi * np.exp(-phi)
        # V_i(x_{<=i}) for i = 0..n-1 (prefix of i+1 letters); prefix key = low bits
        V = []
        for i in range(n):
            key = idx & (2 ** (i + 1) - 1)
            V.append(np.bincount(key, weights=w, minlength=2 ** (i + 1)) / np.bincount(key, weights=pi, minlength=2 ** (i + 1)))
        # tilts lam_i(x_{<i}) = ln V_i(x_{<i}, +) / V_i(x_{<i}, -);  bit i = 1 means x_i = -1
        lam = [np.log(V[i][np.arange(2 ** i)] / V[i][np.arange(2 ** i) + 2 ** i]) for i in range(n)]
        for i in range(n):
            worst_lam = max(worst_lam, float(np.abs(lam[i]).max()) - (us if i < n - 1 else u))
        a = lambda m: np.log((1 - p) * np.exp(m) + p)
        c = lambda m: np.log(p * np.exp(m) + 1 - p)
        for i in range(n - 1):
            pre = np.arange(2 ** i)
            mup, mum = lam[i + 1][pre], lam[i + 1][pre + 2 ** i]     # x_i = +1 / -1
            thm = lam[i] - a(mup) + c(mum)
            thp = lam[i] - (a(mup) - mup) + (c(mum) - mum)
            worst_th = max(worst_th, float(np.abs(thm).max()) - u, float(np.abs(thp).max()) - u)
            # (*) in the report's form
            rhs = np.log((1 - p) * np.exp(thp + mum) + p * np.exp(thm)) - np.log(p * np.exp(mum) + 1 - p)
            worst_star = max(worst_star, float(np.abs(rhs - lam[i]).max()), float(np.abs(mup - mum - thp + thm).max()))
        # chain rule: sum_x pi_phi^t Q^(1-t) = sum_x prod_i tau_{lam_i}(x_{i-1}, x_i)^t q(x_{i-1}, x_i)^(1-t)
        nfl = ((s[:, :-1] * s[:, 1:]) == -1).sum(axis=1)
        Q = 0.5 * qt ** nfl * (1 - qt) ** (n - 1 - nfl)
        piphi = w / w.sum()
        lhs = float((piphi ** t * Q ** (1 - t)).sum())
        prod = np.ones(N)
        for i in range(n):
            lm = lam[i][idx & (2 ** i - 1)]
            xi = s[:, i]
            if i == 0:
                base = np.full(N, 0.5)
                same = np.ones(N, dtype=bool)
                qf = np.full(N, 0.5)
            else:
                same = s[:, i - 1] == xi
                base = np.where(same, 1 - p, p)
                qf = np.where(same, 1 - qt, qt)
            # tau(b, x_i) ~ P(b, x_i) e^{x_i lam / 2}
            num = base * np.exp(xi * lm / 2)
            other = (0.5 if i == 0 else np.where(same, p, 1 - p)) * np.exp(-xi * lm / 2)
            tau = num / (num + other)
            prod *= tau ** t * qf ** (1 - t)
        worst_id = max(worst_id, abs(lhs - float(prod.sum())))
    print(f"60 random cases (n = 3..7): |theta_+-| - u <= {worst_th:.2e};  |lam_i| - u* (last site: - u) <= {worst_lam:.2e};"
          f"  (*) residual {worst_star:.2e};  chain-rule identity {worst_id:.2e}")

    print("\n== (2) n = 3: exact maximum over all vertices against the safe finite-horizon recursion ==")
    for p in (0.4, 0.3, 0.1):
        s, pi = chain_law(3, p)
        V = lipschitz_vertices(3, [u] * 3)
        logP = gibbs_logs(np.log(pi), V)
        for t in (0.3, 0.45, 0.7):
            for qt in (p, 0.8 * p, 0.5):
                nfl = ((s[:, :-1] * s[:, 1:]) == -1).sum(axis=1)
                Q = 0.5 * qt ** nfl * (1 - qt) ** (2 - nfl)
                exact = float(renyi_div_term(logP, np.log(Q), t).max())
                out = []
                for G in (201, 801):
                    gr = Grid(p, G)
                    Ap, Am = gr.stage_min(t, qt)
                    # last site: lam in [-u, u] only
                    inside = (gr.e[1:] > -u - 1e-12) & (gr.e[:-1] < u + 1e-12)
                    S = np.where(inside, Ap + Am, BIG)
                    S = gr.T(S, Ap, Am)                               # two sites
                    # root: no previous letter, P = q = (1/2, 1/2)
                    tp = lambda lam: np.exp(lam / 2) / (np.exp(lam / 2) + np.exp(-lam / 2))
                    Rp = tp(gr.e[:-1]) ** t * 0.5 ** (1 - t)
                    Rm = (1 - tp(gr.e[1:])) ** t * 0.5 ** (1 - t)
                    root = gr.T(S, Rp, Rm)
                    out.append(-np.log(root.min()))
                print(f"p={p} t={t} q~={qt:.2f}: exact max over {V.shape[0]} vertices {exact:.6f};  safe recursion G=201: {out[0]:.6f}, G=801: {out[1]:.6f};"
                      f"  safe >= exact: {out[1] >= exact - 1e-12}")


def h_bound(p, G):
    """a bound for sup_t F_inf(t) over ALL t in (0,1):  grid values B(t) (each minimised over the flip
    probability q~ of the symmetric Markov reference) + on every grid interval [t1, t2] the rule
    F(t) <= min(B(t1) t2/t1, B(t2)(1-t1)/(1-t2))  (F/t nonincreasing, F/(1-t) nondecreasing);
    below the first and above the last grid point: F(t) <= t E_up and F(t) <= (1-t) a_up with the
    one-site bounds of Proposition F (E_up, a_up for slope u*)."""
    hc = cube_constants(u)[0]
    gr = Grid(p, G)
    print(f"p={p}: u* = {gr.us:.4f}, G = {G} cells, spacing {gr.D:.5f}   [{time.time()-T0:.0f} s]", flush=True)
    res = {}
    state = dict(w=None)

    def best_q(t, q0=None):
        f = lambda q: gr.rate(t, q, iters=3000, tol=1e-9, w0=state['w'])[0]
        if q0 is None:
            a, b = 0.55 * p, min(2.5 * p, 0.5)
        else:
            a, b = q0 - 0.03 * p, q0 + 0.03 * p
        # golden section for the minimum over q~ (any q~ gives a valid bound)
        g = (np.sqrt(5.0) - 1) / 2
        c, d = b - g * (b - a), a + g * (b - a)
        fc, fd = f(c), f(d)
        while b - a > 2e-3 * p:
            if fc > fd:
                a, c, fc = c, d, fd
                d = a + g * (b - a)
                fd = f(d)
            else:
                b, d, fd = d, c, fc
                c = b - g * (b - a)
                fc = f(c)
        q = c if fc < fd else d
        val, _, w, it = gr.rate(t, q, iters=6000, tol=1e-10, w0=state['w'])
        # the bound has a kink at q~ = p (Q = pi): try it explicitly
        valp, _, wp, _ = gr.rate(t, p, iters=6000, tol=1e-10, w0=state['w'])
        if valp < val:
            val, q, w = valp, p, wp
        state['w'] = w
        return val, q

    for t in np.round(np.arange(0.05, 0.951, 0.05), 3):
        res[float(t)] = best_q(float(t))
    print("   coarse t-grid: " + "  ".join(f"{t:.2f}: {res[t][0]:.6f}" for t in sorted(res)) + f"   [{time.time()-T0:.0f} s]", flush=True)
    # adaptive bisection of the interval with the largest certified value (q~ interpolated: any q~ is valid)
    nev = 0
    while time.time() - T0 < TLIM:
        tt = sorted(res)
        gmax = max(v[0] for v in res.values())
        bounds = [min(res[a][0] * b / a, res[b][0] * (1 - a) / (1 - b)) for a, b in zip(tt[:-1], tt[1:])]
        k = int(np.argmax(bounds))
        if bounds[k] <= gmax * (1 + 2e-3) or tt[k + 1] - tt[k] < 2e-4:
            break
        tm = 0.5 * (tt[k] + tt[k + 1])
        qm = 0.5 * (res[tt[k]][1] + res[tt[k + 1]][1])
        if res[tt[k]][1] == p or res[tt[k + 1]][1] == p:
            qm = p
        val, _, w, it = gr.rate(tm, qm, iters=6000, tol=1e-10, w0=state['w'])
        state['w'] = w
        res[tm] = (val, qm)
        nev += 1
    print(f"   adaptive refinement: {nev} more values of t   [{time.time()-T0:.0f} s]")
    tt = sorted(res)
    tb = max(tt, key=lambda t: res[t][0])
    print(f"   largest grid value: F_inf({tb:.3f}) <= {res[tb][0]:.6f} at q~ = {res[tb][1]:.4f}   (Q = pi closed form at that t: {tb*E_F(p,u)-E_F(p,tb*u):.6f})   [{time.time()-T0:.0f} s]")
    sup = 0.0
    for a, b in zip(tt[:-1], tt[1:]):
        sup = max(sup, min(res[a][0] * b / a, res[b][0] * (1 - a) / (1 - b)))
    # ends: one-site bounds of Proposition F for E and a (two-letter site with law (1-p, p), slope u*)
    hh = gr.us / 2
    logP = gibbs_logs(np.log(np.array([1 - p, p])), np.array([[-hh, hh], [hh, -hh]]))
    E_up = maximise_E_fast(logP)[1]
    a_up = maximise_a(logP)[1]
    ends = max(tt[0] * E_up, (1 - tt[-1]) * a_up)
    print(f"   certified for all t in [{tt[0]}, {tt[-1]}]: {sup:.6f};  outside: <= {ends:.6f} (t E_up, (1-t) a_up with E_up = {E_up:.5f}, a_up = {a_up:.5f})")
    print(f"   ==> h_inf = sup_t F_inf(t) <= {max(sup, ends):.6f}   (cube {hc:.6f};  report: 0.036163 (0.4), 0.044995 (0.3), 0.054353 (0.2), 0.066765 (0.1))")


def E_bound(p, G):
    gr = Grid(p, G)
    best, dmin, it = gr.E_rate()
    print(f"p={p} G={G}: E_inf <= {best:.6f} (safe; lower iterate value {dmin:.6f}, {it} sweeps);  E_F = {E_F(p,u):.6f};  excess {best-E_F(p,u):.2e}   [{time.time()-T0:.0f} s]")


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'test'
    if mode == 'test':
        test()
    elif mode == 'h':
        h_bound(float(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 401)
    elif mode == 'a':
        for G in ([int(sys.argv[3])] if len(sys.argv) > 3 else [201, 401]):
            a_bound(float(sys.argv[2]), G)
    elif mode == 'E':
        for G in ([int(sys.argv[3])] if len(sys.argv) > 3 else [201, 401, 801]):
            E_bound(float(sys.argv[2]), G)
    print(f"{time.time()-T0:.1f} s")
