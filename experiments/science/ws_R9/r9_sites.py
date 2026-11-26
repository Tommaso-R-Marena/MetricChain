#!/usr/bin/env python3
"""R9 — own code for the single-site functions of theory report §11.26 (written from the statements of Theorems
11.97-11.99 and Proposition 11.103 in the export at 658b77f; neither R5's r5lib.py nor the theory division's
wv_lib.py / harness helpers were opened before this file was written).

Site: letters 0..q-1, site law pi, envelope d (d[a][b] >= 0, zero diagonal, triangle inequality, maybe asymmetric).
L = {gamma : gamma(a) - gamma(b) <= d(a,b)};  vertices of L modulo constants;  pi_phi ∝ pi e^{-phi}.
F*(t) = max_M -t ln sum_a (sum_phi M(phi) pi_phi(a)^t)^{1/t} = min_Q max_phi (1-t) D_t(pi_phi||Q)   (0<t<1)
h = max_t F*(t);  E = min_Q max_phi KL(Q||pi_phi) = max_M -ln sum_a prod_phi pi_phi(a)^M(phi);  a = Shannon capacity.
Every optimum is returned with a duality bracket (primal value, dual value).

Items of the R9 brief served here:
 2(c)(c) the data point (0.02, 0.49, 0.49) at u = 0.5 against the two-letter cube; the other data points of Prop. 11.103(d);
 2(c)(b) the ceiling F*(t) <= t(1-t) D^2/8 for every envelope (random asymmetric sites);
 3(a)    the chi^2 bound that replaces uniform continuity in Theorem 11.97(c):  (I - v)(P) = min_{gamma in L} KL(P||pi_gamma)
         <= chi^2(P||Q) for every Q in the window, and (I - v) <= omega' on the set G of the proof.
"""
import itertools, math, sys
import numpy as np
from scipy.optimize import minimize, linprog

np.seterr(all="ignore")


# ---------------------------------------------------------------- vertices of the Lipschitz polytope
def vertices(d, tol=1e-9):
    q = len(d)
    cons = [(a, b) for a in range(q) for b in range(q) if a != b]          # gamma_a - gamma_b <= d[a][b]
    V = []
    for S in itertools.combinations(cons, q - 1):
        A = np.zeros((q, q)); rhs = np.zeros(q)
        for r, (a, b) in enumerate(S):
            A[r, a] = 1; A[r, b] = -1; rhs[r] = d[a][b]
        A[q - 1, 0] = 1                                                      # normalisation gamma_0 = 0
        if abs(np.linalg.det(A)) < 1e-12:
            continue
        g = np.linalg.solve(A, rhs)
        if all(g[a] - g[b] <= d[a][b] + tol for (a, b) in cons):
            if not any(np.allclose(g, v, atol=1e-8) for v in V):
                V.append(g)
    return np.array(V)


def check_envelope(d, tol=1e-12):
    q = len(d)
    assert all(abs(d[a][a]) < tol for a in range(q)) and all(d[a][b] >= -tol for a in range(q) for b in range(q))
    assert all(d[a][c] <= d[a][b] + d[b][c] + tol for a in range(q) for b in range(q) for c in range(q))


class Site:
    def __init__(self, pi, d):
        self.pi = np.array(pi, float); self.pi /= self.pi.sum()
        self.d = np.array(d, float); check_envelope(self.d)
        self.V = vertices(self.d)
        W = self.pi[None, :] * np.exp(-self.V)
        self.P = W / W.sum(axis=1, keepdims=True)                           # P[phi, a] = pi_phi(a)
        self.D = float(self.d.max())

    # ---- F*(t) with a duality bracket
    def Fstar(self, t, M0=None):
        P = self.P; k = len(P)
        Pt = P ** t

        def lnG(M):
            m = M @ Pt
            return math.log(np.sum(m ** (1 / t)))

        def grad(M):
            m = M @ Pt
            G = np.sum(m ** (1 / t))
            return (Pt @ (m ** (1 / t - 1))) / (t * G)

        best = None
        starts = [np.full(k, 1 / k)] + ([M0] if M0 is not None else [])
        for s in starts:
            res = minimize(lnG, s, jac=grad, method="SLSQP", bounds=[(0, 1)] * k,
                           constraints=[{"type": "eq", "fun": lambda M: M.sum() - 1, "jac": lambda M: np.ones(k)}],
                           options={"ftol": 1e-16, "maxiter": 2000})
            M = np.clip(res.x, 0, None); M /= M.sum()
            # multiplicative polishing: r_phi = t * dG/dM_phi / G; at the optimum r = 1 on the support, >= 1 off it
            for _ in range(20000):
                m = M @ Pt
                G = np.sum(m ** (1 / t))
                r = (Pt @ (m ** (1 / t - 1))) / G
                if 1 - r.min() < 1e-13:
                    break
                M = M * r ** (-0.5 * t / (1 - t) if t < 0.5 else -0.5)
                M /= M.sum()
            m = M @ Pt
            G = np.sum(m ** (1 / t))
            r = (Pt @ (m ** (1 / t - 1))) / G
            primal = -t * math.log(G)
            dual = primal - math.log(r.min())                               # max_phi (1-t) D_t(pi_phi || Q*), Q* ∝ m^{1/t}
            if best is None or dual - primal < best[1] - best[0]:
                best = (primal, dual, M)
        return best

    def h(self, ngrid=199):
        ts = np.linspace(0.005, 0.995, ngrid)
        vals = [self.Fstar(t)[0] for t in ts]
        i = int(np.argmax(vals))
        lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, ngrid - 1)]
        gr = (math.sqrt(5) - 1) / 2
        c, dd = hi - gr * (hi - lo), lo + gr * (hi - lo)
        fc, fd = self.Fstar(c)[0], self.Fstar(dd)[0]
        for _ in range(60):
            if fc < fd:
                lo, c, fc = c, dd, fd; dd = lo + gr * (hi - lo); fd = self.Fstar(dd)[0]
            else:
                hi, dd, fd = dd, c, fc; c = hi - gr * (hi - lo); fc = self.Fstar(c)[0]
        t = 0.5 * (lo + hi)
        p, du, _ = self.Fstar(t)
        return t, p, du

    def E(self):
        """E = max_M -ln sum_a prod_phi pi_phi(a)^M(phi);  dual: Q* ∝ prod pi_phi^M, value max_phi KL(Q*||pi_phi)"""
        lnP = np.log(self.P); k = len(lnP)

        def f(M):
            z = M @ lnP
            mx = z.max()
            return mx + math.log(np.exp(z - mx).sum())

        def g(M):
            z = M @ lnP
            w = np.exp(z - z.max()); w /= w.sum()
            return lnP @ w

        res = minimize(f, np.full(k, 1 / k), jac=g, method="SLSQP", bounds=[(0, 1)] * k,
                       constraints=[{"type": "eq", "fun": lambda M: M.sum() - 1, "jac": lambda M: np.ones(k)}],
                       options={"ftol": 1e-16, "maxiter": 5000})
        M = np.clip(res.x, 0, None); M /= M.sum()
        for _ in range(200000):                                             # polishing: equalise KL(Q||pi_phi) on the support
            z = M @ lnP
            Q = np.exp(z - z.max()); Q /= Q.sum()
            kl = np.array([np.sum(Q * (np.log(Q) - lnP[i])) for i in range(k)])
            primal = -f(M)
            if kl.max() - primal < 1e-13:
                break
            M = M * np.exp(0.5 * (kl - kl.max())) ; M /= M.sum()
        z = M @ lnP
        Q = np.exp(z - z.max()); Q /= Q.sum()
        kl = np.array([np.sum(Q * (np.log(Q) - lnP[i])) for i in range(k)])
        return -f(M), float(kl.max())

    def a(self):
        """Shannon capacity of the vertex channel by Blahut-Arimoto; bracket (I(M), max_phi KL(pi_phi||Q_M))"""
        P = self.P; k = len(P)
        M = np.full(k, 1 / k)
        for _ in range(500000):
            Q = M @ P
            kl = np.sum(P * (np.log(P) - np.log(Q)[None, :]), axis=1)
            lo, hi = float(M @ kl), float(kl.max())
            if hi - lo < 1e-14:
                break
            M = M * np.exp(kl); M /= M.sum()
        return lo, hi


def hamming(q, u):
    return [[0.0 if a == b else u for b in range(q)] for a in range(q)]


def cube_values(u):
    h_t = lambda t: t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))
    ts = np.linspace(0, 1, 200001)
    hv = max(h_t(t) for t in ts)
    p = 1 / (1 + math.exp(u))
    a = math.log(2) + p * math.log(p) + (1 - p) * math.log(1 - p)
    return hv, a, math.log(math.cosh(u / 2))


if __name__ == "__main__":
    out = []
    P = lambda *a: (print(*a), sys.stdout.flush())
    # ------------------------------------------------------------------ sanity: the two-letter cube as a site
    for u in (0.5, 1.0, 2.0):
        s = Site([0.5, 0.5], hamming(2, u))
        t, hp, hd = s.h(); Ep, Ed = s.E(); ap, ad = s.a()
        hc, ac, Ec = cube_values(u)
        P(f"cube as a 2-letter site, u = {u}: h = [{hp:.10f}, {hd:.10f}] (closed form {hc:.10f});  a = [{ap:.10f}, {ad:.10f}] ({ac:.10f});"
          f"  E = [{Ep:.10f}, {Ed:.10f}] ({Ec:.10f});  #vertices {len(s.V)}")
    # ------------------------------------------------------------------ 2(c)(c): three letters, Hamming, u = 0.5
    u = 0.5
    hc, ac, Ec = cube_values(u)
    P(f"\nu = {u}: two-letter cube  h = {hc:.7f}  a = {ac:.7f}  E = {Ec:.7f}   (report: 0.0076729, 0.0302999, 0.0309298)")
    for pi in ((0.02, 0.49, 0.49), (0.05, 0.5, 0.45), (0.04502, 0.45679, 0.49819), (1 / 3, 1 / 3, 1 / 3), (0.001, 0.4995, 0.4995)):
        s = Site(pi, hamming(3, u))
        t, hp, hd = s.h(); Ep, Ed = s.E(); ap, ad = s.a()
        P(f"  pi = {tuple(round(x, 5) for x in pi)}: h in [{hp:.9f}, {hd:.9f}] (t* = {t:.4f})  a in [{ap:.9f}, {ad:.9f}]  E in [{Ep:.9f}, {Ed:.9f}]"
          f"   vs cube: h {'above' if hp > hc else ('below' if hd < hc else 'undecided')} ({(hp/hc-1)*100:+.4f} %), "
          f"a {'above' if ap > ac else ('below' if ad < ac else 'undecided')}, E {'above' if Ep > Ec else ('below' if Ed < Ec else 'undecided')}"
          f"   #vertices {len(s.V)}")
    P("  report (Prop. 11.103(d)): (0.02,0.49,0.49): h = 0.0076722, E = 0.0309220, a above the cube;  (0.05,0.5,0.45): h = 0.0076752,")
    P("          a = 0.0303217, E = 0.0309316;  (0.04502,0.45679,0.49819): h = 0.0076753;  uniform: h = 0.007425")
    # u = 1: the numbers of 11.103(d) at the threshold
    u = 1.0
    hc, ac, Ec = cube_values(u)
    P(f"\nu = {u}: two-letter cube  h = {hc:.6f}  a = {ac:.6f}  E = {Ec:.6f}   (report: E = 0.120115, h = 0.029139)")
    for pi in ((1 / 3, 1 / 3, 1 / 3), (0.05, 0.5, 0.45), (0.3, 0.35, 0.35)):
        s = Site(pi, hamming(3, u))
        t, hp, hd = s.h(); Ep, Ed = s.E(); ap, ad = s.a()
        P(f"  pi = {tuple(round(x, 5) for x in pi)}: h in [{hp:.7f}, {hd:.7f}]  a in [{ap:.7f}, {ad:.7f}]  E in [{Ep:.7f}, {Ed:.7f}]")
    P("  report: uniform E = 0.119499, h = 0.030654, a = 0.123284;  (0.05,0.5,0.45): E = 0.120196;  (0.3,0.35,0.35): h = 0.030572, a = 0.122951")
    # ------------------------------------------------------------------ 2(c)(b): the ceiling for every envelope
    rng = np.random.default_rng(20261126)
    worst = 0.0; ncase = 0; worst_h = 0.0
    for trial in range(60):
        q = int(rng.integers(2, 5))
        while True:                                                         # random asymmetric envelope with the triangle inequality
            d = rng.uniform(0.1, 2.5, size=(q, q)); np.fill_diagonal(d, 0)
            for _ in range(q):                                              # shortest-path closure
                for b in range(q):
                    d = np.minimum(d, d[:, [b]] + d[[b], :])
            np.fill_diagonal(d, 0)
            if d.max() > 0:
                break
        pi = rng.dirichlet(np.ones(q))
        s = Site(pi, d)
        for t in (0.05, 0.2, 0.35, 0.5, 0.65, 0.8, 0.95):
            p, du, _ = s.Fstar(t)
            ratio = du / (t * (1 - t) * s.D ** 2 / 8)
            worst = max(worst, ratio); ncase += 1
        worst_h = max(worst_h, s.h()[2] / (s.D ** 2 / 32))
    P(f"\nceiling F*(t) <= t(1-t) D^2/8, D = max d: {ncase} (site, t) pairs on 60 random sites with asymmetric envelopes, q = 2..4:"
      f" largest ratio (dual value/ceiling) = {worst:.4f};  largest h/(D^2/32) = {worst_h:.4f}")
    for u in (0.1, 0.5, 1.0, 2.0):
        hc, ac, Ec = cube_values(u)
        s3 = Site([1 / 3] * 3, hamming(3, u))
        t, hp, hd = s3.h()
        P(f"  u = {u}: cube h/(u^2/32) = {hc/(u*u/32):.4f};  uniform three-letter site h/(u^2/32) = {hp/(u*u/32):.4f}  (below the ceiling by {100*(1-hp/(u*u/32)):.1f} %)")
    # weight 1/2 on a set of letters  =>  F* >= F*_cube
    bad = 0; n = 0
    for trial in range(40):
        q = int(rng.integers(3, 5)); u = float(rng.uniform(0.2, 2.5))
        w = rng.dirichlet(np.ones(q - 1)) * 0.5
        k = int(rng.integers(1, q - 1))
        a_ = rng.dirichlet(np.ones(k)) * 0.5; b_ = rng.dirichlet(np.ones(q - k)) * 0.5
        pi = np.concatenate([a_, b_])
        s = Site(pi, hamming(q, u))
        for t in (0.1, 0.3, 0.5, 0.7, 0.9):
            fc = t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))
            p, du, _ = s.Fstar(t); n += 1
            if du < fc - 1e-10: bad += 1
    P(f"site laws with weight 1/2 on a set of letters (Hamming, q = 3, 4, random u): F* >= F*_cube in {n - bad} of {n} (site, t) pairs")

    # ------------------------------------------------------------------ 3(a): the chi^2 bound
    P("\n3(a): (I - v)(P) = min_{gamma in L} KL(P||pi_gamma) <= KL(P||Q) <= chi^2(P||Q) for Q = pi_gamma0 in the window")

    def v_primal(s, Pm):
        """v(P) = min_{P'} [KL(P'||pi) + W(P',P)], W(P',P) = min E d(X',X) over couplings: a convex programme in the coupling K[a',a]"""
        q = len(s.pi)

        def obj(k):
            K = k.reshape(q, q)
            Pp = K.sum(axis=1)
            return float(np.sum(Pp * (np.log(np.maximum(Pp, 1e-300)) - np.log(s.pi))) + np.sum(K * s.d))
        cons = [{"type": "eq", "fun": (lambda k, a=a: k.reshape(q, q)[:, a].sum() - Pm[a])} for a in range(q)]
        best = 1e9
        for start in range(4):
            if start == 0:
                k0 = np.diag(Pm).ravel()
            else:
                R = rng.dirichlet(np.ones(q), size=q).T * Pm[None, :]
                k0 = R.ravel()
            res = minimize(obj, k0, method="SLSQP", bounds=[(0, 1)] * (q * q), constraints=cons, options={"ftol": 1e-15, "maxiter": 3000})
            if res.success or res.status in (0, 9):
                best = min(best, obj(np.clip(res.x, 0, None)))
        return best

    def v_dual(s, Pm):
        """max_{gamma in L} [ -ln E_pi e^{-gamma} - E_P gamma ]  (concave in gamma)"""
        q = len(s.pi)
        cons = [{"type": "ineq", "fun": (lambda g, a=a, b=b: s.d[a][b] - g[a] + g[b])} for a in range(q) for b in range(q) if a != b]

        def obj(g):
            return math.log(np.sum(s.pi * np.exp(-g))) + float(Pm @ g)
        best = (1e9, None)
        for g0 in [np.zeros(q)] + list(s.V):
            res = minimize(obj, g0, method="SLSQP", constraints=cons, options={"ftol": 1e-15, "maxiter": 3000})
            if obj(res.x) < best[0] and all(c["fun"](res.x) >= -1e-9 for c in cons):
                best = (obj(res.x), res.x)
        return -best[0], best[1]

    nt = 0; maxgap = 0.0; worst_ratio = 0.0; viol = 0
    for trial in range(120):
        q = int(rng.integers(2, 5))
        d = rng.uniform(0.1, 2.0, size=(q, q)); np.fill_diagonal(d, 0)
        for _ in range(q):
            for b in range(q):
                d = np.minimum(d, d[:, [b]] + d[[b], :])
        np.fill_diagonal(d, 0)
        pi = rng.dirichlet(np.ones(q) * 2)
        s = Site(pi, d)
        # a window point Q = pi_gamma0 with gamma0 a random point of L (convex combination of vertices), and P near Q
        lam = rng.dirichlet(np.ones(len(s.V)))
        g0 = lam @ s.V
        Q = pi * np.exp(-g0); Q /= Q.sum()
        scale = 10 ** rng.uniform(-3, -0.3)
        Pm = np.clip(Q + scale * rng.normal(size=q) * Q, 1e-9, None); Pm /= Pm.sum()
        I = float(np.sum(Pm * (np.log(Pm) - np.log(pi))))
        vp = v_primal(s, Pm); vd, gopt = v_dual(s, Pm)
        maxgap = max(maxgap, abs(vp - vd))
        ImV = I - vd
        chi2 = float(np.sum((Pm - Q) ** 2 / Q))
        klPQ = float(np.sum(Pm * (np.log(Pm) - np.log(Q))))
        nt += 1
        if ImV > chi2 + 1e-9 or ImV > klPQ + 1e-9 or ImV < -1e-9:
            viol += 1
        if chi2 > 1e-12:
            worst_ratio = max(worst_ratio, ImV / chi2)
        # letter probabilities in the window are at least pi_min e^{-D}
        assert Q.min() >= pi.min() * math.exp(-s.D) - 1e-12
    P(f"  {nt} random (site, window point Q, nearby P), q = 2..4, asymmetric envelopes: |v_primal - v_dual| <= {maxgap:.2e};"
      f" violations of 0 <= I - v <= KL(P||Q) <= chi^2(P||Q): {viol};  largest (I - v)/chi^2 = {worst_ratio:.4f}")

    # the bound on the set G of the proof: |P_j(a) - Q_j(a)| <= kappa2/lambda_j  =>  (I - v)(P) <= omega'
    P("  the bound on G: sum_j lambda_j (I-v)_j(P_j) <= omega' = m kappa2 [q_max e^{D_max}/pi_min + ln(1/pi_min)]")
    worst = 0.0; nt = 0
    for trial in range(300):
        m = int(rng.integers(1, 4))
        sites = []
        for j in range(m):
            q = int(rng.integers(2, 4))
            d = rng.uniform(0.1, 1.5, size=(q, q)); np.fill_diagonal(d, 0)
            for _ in range(q):
                for b in range(q):
                    d = np.minimum(d, d[:, [b]] + d[[b], :])
            np.fill_diagonal(d, 0)
            sites.append(Site(rng.dirichlet(np.ones(q) * 2), d))
        lam = rng.dirichlet(np.ones(m) * rng.choice([0.05, 0.3, 1.0]))
        kappa2 = 10 ** rng.uniform(-3.5, -1)
        qmax = max(len(s.pi) for s in sites); Dmax = max(s.D for s in sites); pmin = min(s.pi.min() for s in sites)
        omega = m * kappa2 * (qmax * math.exp(Dmax) / pmin + math.log(1 / pmin))
        tot = 0.0
        for j, s in enumerate(sites):
            q = len(s.pi)
            g0 = rng.dirichlet(np.ones(len(s.V))) @ s.V
            Q = s.pi * np.exp(-g0); Q /= Q.sum()
            # an adversarial P in the box |P - Q| <= kappa2/lambda_j: move mass between two letters by the full amount allowed
            r = min(kappa2 / lam[j], 1.0)
            a, b = rng.choice(q, 2, replace=False)
            dlt = min(r, Q[a] - 1e-9 if Q[a] > 1e-9 else 0.0, 1 - Q[b])
            Pm = Q.copy(); Pm[a] -= dlt; Pm[b] += dlt
            Pm = np.clip(Pm, 1e-12, None); Pm /= Pm.sum()
            I = float(np.sum(Pm * (np.log(Pm) - np.log(s.pi))))
            vd, _ = v_dual(s, Pm)
            tot += lam[j] * (I - vd)
        nt += 1
        worst = max(worst, tot / omega)
    P(f"  {nt} random chains (m = 1..3 site types, compositions with small fractions, kappa2 in [3e-4, 0.1]): largest (I - v)/omega' = {worst:.4f}  (must be <= 1)")
