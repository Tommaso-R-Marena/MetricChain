#!/usr/bin/env python3
"""Workstream R27, Item 3 -- Theorem L+ (the first-order constant in a certified range).  REPLICATION from the statement:

   A = half-Jacobian of the squared distances (pairs of separation <= 4), mu = its (3n-6)-th singular value,
   Lambda = largest Laplacian eigenvalue of the band graph (claimed < 11.04), C_L a constant of Theorem L.
   For every Y with ||eta||_2 <= mu/(Lambda C_L):
        d_P <= ||eta|| / (mu + sqrt(mu^2 - Lambda ||eta||))   if ||eta|| <= mu^2/Lambda,     and  d_P <= ||eta||/mu  in any case.
   "As ||eta|| -> 0 the constant tends to 1/(2mu), attained along the softest mode; at finite amplitude 1/(2mu) alone is not a bound."

What is done: (1) Lambda: the symbol 8 - 2 sum_{s<=4} cos(s theta) and Lambda_n for many n; (2) for several chains: mu, the ranges,
random / softest-mode / adversarial (constrained maximisation of d_P at given ||eta||) Y inside the range, the ratio d_P/bound, the limit along
the softest mode; (3) controls: the first-order constant used as a bound; mu replaced by 1.01 mu; and, just outside the hypotheses, a chain with
a thin interior window and its reflected tail (||eta|| <= mu^2/Lambda but > mu/(Lambda C_L)).

Run:  OMP_NUM_THREADS=1 python3 -B item3_Lplus.py > item3_Lplus_<stamp>.log
"""
import os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize, brentq
from r27lib import (cap_memory, peak_mb, now, KAPPA, helix, angle_chain, chain_consts, pair_arrays, eta_vec, procrustes,
                    local_weights, uniform_constant, half_jacobian, mu_and_mode, band_laplacian_max)

cap_memory(2.0)
t0 = time.time()
rng = np.random.default_rng(27114)
print(f"R27 item3_Lplus.py started {now()}")

# ---- (1) Lambda ---------------------------------------------------------------------------------------------------------
th = np.linspace(0, np.pi, 2_000_001)
sym = 8 - 2 * sum(np.cos(s_ * th) for s_ in range(1, 5))
k = sym.argmax()
print(f"\n(1) symbol 8 - 2 sum_(s<=4) cos(s theta): maximum {sym[k]:.9f} at theta = {np.degrees(th[k]):.4f} deg  (claimed: at most 11.04 -> {sym[k] <= 11.04})")
lam = {}
for n in (5, 6, 7, 8, 9, 10, 12, 20, 50, 100, 200, 400, 1000):
    lam[n] = band_laplacian_max(n)
print("    Lambda_n: " + ", ".join(f"{n}: {v:.6f}" for n, v in lam.items()))
print(f"    Lambda_n < 11.04 for all n computed: {all(v < 11.04 for v in lam.values())};  increasing in n: {all(np.diff(list(lam.values())) > -1e-12)};"
      f"  Lambda_n <= sup of the symbol: {all(v <= sym[k] + 1e-9 for v in lam.values())}")
print(f"    for n = 5 the graph is complete (K_5): Lambda_5 = {lam[5]:.6f} (= 5)")


def trivial_basis(X):
    n = len(X)
    T = []
    for a in range(3):
        v = np.zeros((n, 3)); v[:, a] = 1; T.append(v.ravel())
    Xc = X - X.mean(0)
    for a in range(3):
        e = np.zeros(3); e[a] = 1
        T.append(np.cross(e, Xc).ravel())
    Q, _ = np.linalg.qr(np.array(T).T)
    return Q                       # 3n x 6, orthonormal


def thin_window_chain(n, rng, pos, height):
    X = angle_chain(n, rng)
    a, b_, c_ = X[pos + 1], X[pos + 2], X[pos + 3]
    nrm = np.cross(b_ - a, c_ - a); nrm /= np.linalg.norm(nrm)
    h = (X[pos + 4] - a) @ nrm
    X[pos + 4:] += (height - h) * nrm
    return X


def reflect_tail(X, i):
    nrm = np.cross(X[i + 2] - X[i + 1], X[i + 3] - X[i + 1]); nrm /= np.linalg.norm(nrm)
    Y = X.copy()
    Y[i + 4:] = X[i + 4:] - 2 * ((X[i + 4:] - X[i + 1]) @ nrm)[:, None] * nrm[None, :]
    hm = (X[i] - X[i + 1]) @ nrm; hp = (X[i + 4] - X[i + 1]) @ nrm
    return Y, hm, hp


class Chain:
    def __init__(self, X):
        self.X = X; self.n = n = len(X)
        self.J, self.K = pair_arrays(n)
        self.tau, self.s, self.b = chain_consts(X)
        self.mu, self.nxt, self.V, self.S = mu_and_mode(X, self.J, self.K)
        self.Lam = band_laplacian_max(n)
        self.C = uniform_constant(X, (self.tau, self.s, self.b))
        self.Cloc = 2 * np.linalg.svd(local_weights(X, self.tau, self.s), compute_uv=False)[0]
        self.T = trivial_basis(X)

    def eta(self, Y):
        return eta_vec(self.X, Y, self.J, self.K)

    def dp(self, Y):
        return np.linalg.norm(procrustes(self.X, Y)[2])

    def bounds(self, rho):
        mu, L = self.mu, self.Lam
        b1 = rho / (mu + np.sqrt(mu * mu - L * rho)) if rho <= mu * mu / L else np.inf
        return b1, rho / mu

    def scale_to(self, V, rho):
        """t > 0 (smallest) with ||eta(X + t V)|| = rho"""
        V = V / np.linalg.norm(V)
        g = lambda t: np.linalg.norm(self.eta(self.X + t * V)) - rho
        hi = rho / self.mu
        it = 0
        while g(hi) < 0 and it < 60:
            hi *= 2; it += 1
        return brentq(g, 0.0, hi, xtol=1e-15 * hi, rtol=1e-14)


chains = [("helix-like n=12", helix(12, 2.3, 1.5, 100.0)), ("helix-like n=20", helix(20, 2.3, 1.5, 100.0)),
          ("strand-like 160 n=12", helix(12, 0.94, 3.3, 160.0)), ("angle-constrained random chain n=10", angle_chain(10, rng)),
          ("angle-constrained random chain n=16", angle_chain(16, rng))]
a4 = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
chains.append(("double regular tetrahedron n=5", np.vstack([a4[0], a4[1], a4[2], a4[3], 2 * a4[1:].mean(0) - a4[0]])))

print("\n(2) inside the certified range ||eta|| <= mu/(Lambda_n C_L)  [C_L = uniform constant 1.2 b (n+2)^2/(s* tau*); Lambda_n the exact eigenvalue]")
tot = dict(pairs=0, viol=0, first_order_alone_violated=0, mu101_violated=0, maxratio=0.0)
for name, X in chains:
    ch = Chain(X)
    n = ch.n
    rho_cert = ch.mu / (ch.Lam * ch.C)
    rho_cert_loc = ch.mu / (ch.Lam * ch.Cloc)
    rho_first = ch.mu ** 2 / ch.Lam
    print(f"\n  {name}: mu = {ch.mu:.6g} (next singular value {ch.nxt:.1e}; the six after it must vanish), Lambda_n = {ch.Lam:.5f}, C_L = {ch.C:.5g}, C_loc = {ch.Cloc:.5g}, 1/(2mu) = {1 / (2 * ch.mu):.5g}")
    print(f"     certified range mu/(Lambda C_L) = {rho_cert:.3e}   [with C_loc: {rho_cert_loc:.3e}];  mu^2/Lambda = {rho_first:.3e};  1/mu <= C_L needed for the root formula: {1 / ch.mu <= ch.C};"
          f"  Cor. L.3(b): mu >= 1/(2 C_L): {ch.mu >= 1 / (2 * ch.C)} (mu C_L = {ch.mu * ch.C:.1f})")
    maxr = 0.0; nviol = 0; nfo = 0; n101 = 0; npairs = 0
    worst_kind = None
    P_perp = np.eye(3 * n) - ch.T @ ch.T.T
    soft3 = np.linalg.svd(half_jacobian(X, ch.J, ch.K), full_matrices=True)[2][3 * n - 9:3 * n - 6]      # three softest non-trivial modes

    def test(Y, kind):
        rho = np.linalg.norm(ch.eta(Y)); d = ch.dp(Y)
        b1, b2 = ch.bounds(rho)
        return rho, d, b1, b2

    for frac in (1.0, 0.3, 0.1, 1e-2, 1e-4):
        rho = frac * rho_cert
        cands = []
        for sg in (1, -1):
            cands.append(("softest mode", sg * ch.V))
        for _ in range(20):
            v = (P_perp @ rng.normal(size=3 * n)).reshape(n, 3)
            cands.append(("random direction (orthogonal to the trivial motions)", v))
        for _ in range(10):
            cands.append(("random direction (not projected)", rng.normal(size=(n, 3))))
        for _ in range(10):
            c = rng.normal(size=3) * np.array([0.2, 0.5, 1.0])
            cands.append(("mixture of the three softest modes", (c @ soft3).reshape(n, 3)))
        Ys = []
        for kind, v in cands:
            t = ch.scale_to(v, rho)
            Ys.append((kind, X + t * v / np.linalg.norm(v)))
        # adversarial: maximise d_P^2 subject to ||eta||^2 <= rho^2, variables scaled by a = rho/(2 mu)
        a = rho / (2 * ch.mu)

        def negd2(z):
            Y = X + a * z.reshape(n, 3)
            res = procrustes(X, Y)[2]
            return -(res * res).sum() / a ** 2, (-2 * res / a).ravel()

        def con(z):
            Y = X + a * z.reshape(n, 3)
            et = ch.eta(Y)
            return 1.0 - (et @ et) / rho ** 2

        def con_jac(z):
            Y = X + a * z.reshape(n, 3)
            et = ch.eta(Y)
            v = 2 * (2 * et)[:, None] * (Y[ch.J] - Y[ch.K])
            G = np.zeros((n, 3)); np.add.at(G, ch.J, v); np.add.at(G, ch.K, -v)
            return (-G * a / rho ** 2).ravel()

        for q in range(6):
            z0 = (ch.V * (1 if q % 2 == 0 else -1)).ravel() * 0.9 + (0.0 if q < 2 else 0.3) * rng.normal(size=3 * n)
            res = minimize(negd2, z0, jac=True, method="SLSQP", constraints=[dict(type="ineq", fun=con, jac=con_jac)],
                           options=dict(maxiter=300, ftol=1e-14))
            Y = X + a * res.x.reshape(n, 3)
            if np.linalg.norm(ch.eta(Y)) <= rho * (1 + 1e-7):
                Ys.append(("adversarial (max d_P at given ||eta||, SLSQP)", Y))
        for kind, Y in Ys:
            rho_y, d, b1, b2 = test(Y, kind)
            npairs += 1
            if d > b1 * (1 + 1e-7) or d > b2 * (1 + 1e-7):
                nviol += 1
            if d / b1 > maxr:
                maxr = d / b1; worst_kind = (kind, frac)
            if d > rho_y / (2 * ch.mu) * (1 + 1e-9):
                nfo += 1
            mu2 = 1.01 * ch.mu
            b1_wrong = rho_y / (mu2 + np.sqrt(mu2 * mu2 - ch.Lam * rho_y))
            if d > b1_wrong * (1 + 1e-9):
                n101 += 1
    print(f"     pairs inside the range: {npairs}   violations of either bound: {nviol}   max d_P/bound = {maxr:.9f} at {worst_kind}")
    print(f"     CONTROLS: 'd_P <= ||eta||/(2 mu)' (first-order constant alone) violated by {nfo} pairs;  the bound with 1.01 mu in place of mu violated by {n101} pairs")
    # the limit along the softest mode
    line = []
    for expo in (0, -1, -2, -3, -4):
        best = 0
        for sg in (1, -1):
            rho = 10.0 ** expo * rho_first * 0.999
            t = ch.scale_to(sg * ch.V, rho)
            Y = X + sg * t * ch.V
            d = ch.dp(Y); b1, b2 = ch.bounds(np.linalg.norm(ch.eta(Y)))
            best = max(best, d / b1)
        line.append(f"{10.0 ** expo:g}: {1 - best:.2e}")
    print("     along the softest mode (better sign), 1 - d_P/bound at ||eta|| = f * mu^2/Lambda (NOT necessarily inside the certified range), f: " + ", ".join(line))
    tot["pairs"] += npairs; tot["viol"] += nviol; tot["first_order_alone_violated"] += nfo; tot["mu101_violated"] += n101
    tot["maxratio"] = max(tot["maxratio"], maxr)
    sys.stdout.flush()

print(f"\n  TOTAL inside the certified ranges: pairs {tot['pairs']}, violations {tot['viol']}, max d_P/bound {tot['maxratio']:.9f};"
      f"  controls: first-order constant alone violated {tot['first_order_alone_violated']} times, 1.01 mu violated {tot['mu101_violated']} times")

# ---- (3) just outside the hypotheses ------------------------------------------------------------------------------------
print("\n(3) just outside the hypotheses: a chain with ONE thin interior four-point window (x_{p+4} at height h over the plane of the three points before it);")
print("    Y = the tail reflected in that plane.  The conclusions of Theorem L+ are evaluated although ||eta|| > mu/(Lambda C_L):")
print("    columns: h | tau*  mu  1/(2mu)  C_L | ||eta|| = 4|h- h+| | mu/(Lambda C_L)  mu^2/Lambda | d_P | ||eta||/mu | smaller-root bound | conclusion violated? | Theorem L (uniform) holds?")
seed_state = rng.bit_generator.state
nfail = 0
for h in (0.3, 1e-1, 3e-2, 1e-2, 1e-3, 1e-4):
    rng.bit_generator.state = seed_state                     # the same base chain for every h
    X = thin_window_chain(10, rng, 3, h)
    ch = Chain(X)
    Y, hm, hp = reflect_tail(X, 3)
    rho = np.linalg.norm(ch.eta(Y)); d = ch.dp(Y)
    b1, b2 = ch.bounds(rho)
    inside_first = rho <= ch.mu ** 2 / ch.Lam
    viol = d > min(b1, b2) * (1 + 1e-9)
    nfail += int(viol and inside_first)
    print(f"    {h:7.0e} | {ch.tau.min():.3e} {ch.mu:.4f} {1 / (2 * ch.mu):.4f} {ch.C:.3e} | {rho:.4e} (4|h-h+| = {4 * abs(hm * hp):.4e}) | {ch.mu / (ch.Lam * ch.C):.2e} {ch.mu ** 2 / ch.Lam:.3e} | {d:.4f} | {b2:.3e} | "
          f"{b1:.3e} | {'YES' if viol else 'no'}{' (and ||eta|| <= mu^2/Lambda)' if inside_first else ' (||eta|| > mu^2/Lambda)'} | {d <= ch.C * rho}  (d_P/(C_L ||eta||) = {d / (ch.C * rho):.2e}; d_P/||eta|| = {d / rho:.3g})")
print(f"    -> the control fails as it should in {nfail} cases with ||eta|| <= mu^2/Lambda: there the hypothesis ||eta|| <= mu/(Lambda C_L) cannot be replaced by ||eta|| <= mu^2/Lambda,")
print("       and 1/(2 mu) stays bounded while sup_Y d_P/||eta|| grows like 1/h: the factor 1/tau of Theorem L is necessary in kind.")
print(f"ALL DONE {now()}  {time.time() - t0:.1f} s  peak memory {peak_mb():.0f} MB")
