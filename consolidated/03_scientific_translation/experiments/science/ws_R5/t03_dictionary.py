"""
t03_dictionary.py -- the dictionary of Theorem 11.99 with exact conventions.

(A) uniform cube = binary symmetric channel with crossover p_u = 1/(1+e^u):
      a = ln 2 - h(p_u),  E = ln cosh(u/2),  E_sp(theta) = KL(rho||p_u) at KL(rho||1/2) = theta,
      F*(t) = Lambda(tu) - t Lambda(u), R^(e) = KL((Lambda_1+e)/u || 1/2)   (the formulas of section 11.16/11.18)
(B) E_sp(theta) := sup_{rho>=0} [E_0(rho) - rho theta],  E_0(rho) = sum_j lambda_j max_M E_0^{(j)}(rho, M)  (Gallager, raw)
      against  x_na(theta) := S(R^^{-1}(theta))  from the site functions  (the claim "theta_na = E_sp^{-1}"),
      and  e_hint(theta) := R^^{-1}(theta) = E_sp(theta) - theta   (shear law)
(C) fixed composition M: Gallager's sup_rho[E_0(rho,M) - rho theta]  <=  Csiszar-Koerner min{D(V||W|M): I(M,V)<=theta}
      <= E_sp(theta), with equality in both at the optimal M   (Sibson vs Augustin: which form is the 'cone' formula)
"""
import time
import numpy as np
from scipy.optimize import minimize, brentq, minimize_scalar
from r5lib import *
from t01_identity import sites_example

np.set_printoptions(precision=6, suppress=True, linewidth=150)


def klb(a, b):
    return a * np.log(a / b) + (1 - a) * np.log((1 - a) / (1 - b))


def hb(p):
    return -p * np.log(p) - (1 - p) * np.log(1 - p)


def E0_chain_raw(chain, rho):
    """sum_j lambda_j max_M E_0(rho, M) with Gallager's raw formula; the maximiser M from the primal solver."""
    tot = 0.0
    for l, s in chain.parts:
        t = 1.0 / (1.0 + rho)
        lo, M, hi = renyi_primal(s, t)
        tot += l * E0_gallager_raw(s, rho, M)
    return tot


def Esp_raw(chain, theta, rho_max=400.0):
    """sup_{rho >= 0} [E_0(rho) - rho*theta] by a grid in t = 1/(1+rho) and Brent refinement."""
    f = lambda t: E0_chain_raw(chain, (1 - t) / t) - (1 - t) / t * theta if 0 < t < 1 else (0.0 if t >= 1 else -np.inf)
    ts = np.linspace(1.0 / (1 + rho_max), 1.0, 300)
    vals = np.array([f(t) for t in ts])
    i = int(vals.argmax())
    l, r = ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)]
    res = minimize_scalar(lambda t: -f(t), bounds=(l, r), method="bounded", options=dict(xatol=1e-12))
    return max(vals.max(), -res.fun)


def Rhat_inverse(Fstar, theta, E):
    """the e with R^(e) = theta (0 < theta), by bisection; R^ is strictly decreasing where positive."""
    return brentq(lambda e: Rhat(Fstar, e, ngrid=300)[0] - theta, -3.0, E, xtol=1e-13)


def ck_fixed_M(site, M, theta):
    """Csiszar-Koerner form for ONE site type and a fixed label law M, by a PRIMAL solver over the
    exit laws nu[phi, a]:  min { sum_phi M(phi) KL(nu_phi || pi_phi) : sum_phi M(phi) KL(nu_phi || nubar) <= theta }."""
    idx = [k for k in range(len(M)) if M[k] > 1e-9]
    Mi = M[idx] / M[idx].sum()
    W = site.W[idx]
    nv, q = W.shape

    def unpack(x):
        nu = np.maximum(x.reshape(nv, q), 1e-300)
        return nu

    def Dfun(x):
        nu = unpack(x)
        return float(np.sum(Mi[:, None] * nu * (np.log(nu) - np.log(W))))

    def MIfun(x):
        nu = unpack(x)
        bar = Mi @ nu
        return float(np.sum(Mi[:, None] * nu * (np.log(nu) - np.log(bar)[None, :])))

    cons = [dict(type="eq", fun=lambda x: unpack(x).sum(axis=1) - 1.0),
            dict(type="ineq", fun=lambda x: theta - MIfun(x))]
    best = np.inf
    # start from the mixture (MI = 0, feasible) and from a point between the mixture and the channel
    Wbar = Mi @ W
    for lam in (0.0, 0.3, 0.6):
        x0 = ((1 - lam) * np.tile(Wbar, (nv, 1)) + lam * W).ravel()
        res = minimize(Dfun, x0, method="SLSQP", bounds=[(1e-10, 1)] * (nv * q), constraints=cons,
                       options=dict(ftol=1e-14, maxiter=2000))
        if res.success and MIfun(res.x) <= theta + 1e-9:
            best = min(best, res.fun)
    return best


if __name__ == "__main__":
    t0 = time.time()
    print("== (A) the uniform cube is the binary symmetric channel with crossover 1/(1+e^u) ==")
    for u in (0.5, 1.0, 2.0):
        s = Site([0.5, 0.5], [[0, u], [u, 0]], "cube")
        ch = Chain([(1.0, s)])
        pu = 1 / (1 + np.exp(u))
        print(f"u={u}: vertex channel rows {np.round(s.W, 6).tolist()}  (crossover p_u = {pu:.6f})")
        a_lo, a_hi, _ = capacity_a(s)
        E_lo, E_hi, _ = threshold_E(s)
        print(f"   a = {a_lo:.9f}  vs ln2 - h(p_u) = {np.log(2) - hb(pu):.9f};   E = {E_lo:.9f}  vs ln cosh(u/2) = {np.log(np.cosh(u/2)):.9f}")
        Lam = lambda x: np.log(2 / (1 + np.exp(-x)))
        dF = max(abs(Fstar_site(s, t) - (Lam(t * u) - t * Lam(u))) for t in np.linspace(0.05, 0.95, 19))
        h, _ = Rhat(ch.Fstar, 0.0)
        print(f"   max_t |F*(t) - [Lambda(tu) - t Lambda(u)]| = {dF:.1e};   h = {h:.9f}  vs KL(Lambda_1/u || 1/2) = {klb(Lam(u)/u, 0.5):.9f}")
        for frac in (0.1, 0.3, 0.6, 0.9):
            theta = frac * a_lo
            rho_star = brentq(lambda r: klb(r, 0.5) - theta, pu, 0.5 - 1e-12)     # KL(rho||1/2) = theta on [p_u, 1/2]
            closed = klb(rho_star, pu)
            esp = Esp_raw(ch, theta)
            xna = theta + Rhat_inverse(ch.Fstar, theta, E_lo)
            print(f"   theta = {frac:.1f}a: E_sp (Gallager sup) = {esp:.9f} | S(R^^-1(theta)) = {xna:.9f} | KL(rho||p_u) at KL(rho||1/2)=theta: {closed:.9f}"
                  f" | adaptive/hinted accuracy E_sp - theta = {esp - theta:.9f} vs u*rho - Lambda_1 = {u*rho_star - Lam(u):.9f}")
    print()
    S = sites_example()
    chains = {"path": Chain([(1.0, S["path"])]), "asym": Chain([(1.0, S["asym"])]),
              "mix": Chain([(0.5, S["bin"]), (0.5, S["path"])]), "mix2": Chain([(0.4, S["bin"]), (0.6, S["tri"])])}
    print("== (B) E_sp(theta) = sup_rho[E_0(rho) - rho theta] (raw Gallager, common rho for all site types)  vs  S(R^^-1(theta)) ==")
    worst = 0
    for nm, ch in chains.items():
        E, a = ch.E(), ch.a()
        for frac in (0.05, 0.2, 0.5, 0.8, 0.95):
            theta = frac * a
            esp = Esp_raw(ch, theta)
            e_hint = Rhat_inverse(ch.Fstar, theta, E)
            xna = theta + e_hint
            th_back = theta_na_direct(ch.Fstar, esp)[0]
            worst = max(worst, abs(esp - xna), abs(th_back - theta))
            print(f"{nm:5s} theta={frac:.2f}a={theta:.6f}: E_sp={esp:.9f}  S(R^^-1)={xna:.9f}  diff={esp-xna:+.1e};  "
                  f"theta_na(E_sp(theta)) - theta = {th_back-theta:+.1e};  E_sp - theta = {esp-theta:.6f}")
        print(f"{nm:5s} E_sp(0+) = lim E_0(rho): E_0(400) = {E0_chain_raw(ch, 400.0):.6f}, E_0(4000) = {E0_chain_raw(ch, 4000.0):.6f}; E = {E:.6f};"
              f"   E_0(rho)/rho at rho=1e-4: {E0_chain_raw(ch, 1e-4)/1e-4:.6f}; a = {a:.6f};  fixed point E_sp(h)=h: h = {Rhat(ch.Fstar,0.0)[0]:.9f},"
              f" E_sp(h) = {Esp_raw(ch, Rhat(ch.Fstar,0.0)[0]):.9f}")
    print(f"largest deviation in (B): {worst:.1e}")
    print()
    print("== (C) fixed label law M (one site type, 'path' and 'asym'): Gallager(M) <= Csiszar-Koerner(M) <= E_sp ==")
    rng = np.random.default_rng(7)
    for nm in ("path", "asym"):
        s = S[nm]
        ch = chains[nm]
        a = ch.a()
        for frac in (0.2, 0.6):
            theta = frac * a
            esp = Esp_raw(ch, theta)
            # optimal M at the optimal rho
            tau = theta_na_direct(ch.Fstar, esp)[1]
            Mstar = renyi_primal(s, tau)[1]

            def gallager_M(M):
                f = lambda t: E0_gallager_raw(s, (1 - t) / t, M) - (1 - t) / t * theta
                ts = np.linspace(0.003, 1.0, 400)
                v = [f(t) for t in ts]
                i = int(np.argmax(v))
                res = minimize_scalar(lambda t: -f(t), bounds=(ts[max(i-1, 0)], ts[min(i+1, 399)]), method="bounded",
                                      options=dict(xatol=1e-12))
                return max(max(v), -res.fun)

            ck_star = ck_fixed_M(s, Mstar, theta)
            print(f"{nm:5s} theta={frac}a: E_sp = {esp:.9f};  at M*: Gallager(M*) = {gallager_M(Mstar):.9f}, CK(M*) = {ck_star:.9f}"
                  f"  (CK - E_sp = {ck_star-esp:+.1e})")
            viol_low, viol_up, strict = 0, 0, 0
            gaps = []
            for rep in range(12):
                M = rng.dirichlet(np.ones(len(s.V)))
                g = gallager_M(M)
                c = ck_fixed_M(s, M, theta)
                viol_low += (g > c + 1e-7)
                viol_up += (c > esp + 1e-7)
                strict += (c > g + 1e-6)
                gaps.append((c - g, esp - c))
            gaps = np.array(gaps)
            print(f"        12 random M: violations of Gallager(M) <= CK(M): {viol_low}; of CK(M) <= E_sp: {viol_up}; "
                  f"CK(M) > Gallager(M) strictly in {strict} cases (largest gap {gaps[:,0].max():.2e}); "
                  f"smallest E_sp - CK(M) = {gaps[:,1].min():.2e}")
    print(f"[{time.time()-t0:.1f} s]")
