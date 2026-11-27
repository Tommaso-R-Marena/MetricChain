#!/usr/bin/env python3
"""r26_n1.py -- workstream R26, Item 3: attempts to break Theorem N1 and Theorem N1' (N_REPORT 2.3, 2.5).

Usage: python3 -B r26_n1.py <block> [runs]
  S    Theorem N1 (cap) on finite outer spaces with adversarial integrands -- an atom at the maximum, a gap, a
       heavy lower tail, two values, ties on the level grid, a flat integrand -- each run with the SHARPEST valid
       tail functions of that integrand (anything smaller violates (TU) or (TL)), random parameters, three bracket
       placements.  Every claim of the theorem that can be checked on a run is checked.  Mutations at the end.
  U    Theorem N1' (no cap) on two unbounded integrands with closed forms: e^{Lx} on the Gaussian line (class tail
       functions of Theorem N9) and e^{ux} on the Laplace line (Pareto tails, sharpest tail functions), including
       parameter sets in which levels are left as NEGLIGIBLE (the branch that N_REPORT 9 says was not exercised).
  Q1   Lemma N.0 evaluated literally at q = 1 (the "D != X" in its formula): a deterministic false certificate.
"""
import math
import sys
import time

import numpy as np
from scipy.special import log_ndtr, ndtr, ndtri

import r26_alg as A


# ------------------------------------------------------------------------------------------ block S

def integrands(rng):
    out = {}
    n = 400
    mu = rng.dirichlet(np.ones(n) * 0.7)
    mu = np.maximum(mu, 2e-5)
    mu /= mu.sum()
    base = np.exp(rng.normal(0, 1.0, n))
    for mass in (0.3, 0.02, 0.002):                       # an atom at the maximum
        V = base.copy()
        order = np.argsort(mu)
        acc, sel = 0.0, []
        for i in order:
            if acc >= mass:
                break
            sel.append(i)
            acc += mu[i]
        V[sel] = base.max() * 30.0
        out[f"atom at the maximum, mass {acc:.4f}"] = (mu, V)
    for (ratio, mass) in ((1e3, 0.01), (1e5, 0.001), (30.0, 0.2)):   # a gap
        V = np.exp(rng.normal(0, 0.3, n))
        order = rng.permutation(n)
        acc, sel = 0.0, []
        for i in order:
            if acc >= mass:
                break
            sel.append(i)
            acc += mu[i]
        V[sel] *= ratio
        out[f"gap: a cluster of mass {acc:.4f} higher by {ratio:g}"] = (mu, V)
    X = rng.pareto(0.6, n)                                 # heavy lower tail: V = e^{-X}, X Pareto(0.6)
    out["heavy lower tail: V = exp(-Pareto(0.6))"] = (mu, np.exp(-np.minimum(X, 60.0)))
    X = rng.exponential(1.0, n) ** 3
    out["heavy lower tail: V = exp(-Exp^3)"] = (mu, np.exp(-np.minimum(X, 80.0)))
    V = np.where(rng.random(n) < 0.03, 500.0, 1.0)
    out["two values {1, 500}"] = (mu, V)
    out["flat"] = (mu, np.full(n, 3.0))
    out["lognormal, sd 3"] = (mu, np.exp(rng.normal(0, 3.0, n)))
    return out


def block_S(runs):
    rng0 = np.random.default_rng(777)
    inst = integrands(rng0)
    print(f"instances from default_rng(777); run r of cell c uses default_rng(1000000 + 1000*c + r), r < {runs}")
    viol, cell, nruns, limited = 0, 0, 0, 0
    keys = ("valid", "width", "cert_q", "cert_p", "cert_ell", "cert_tail", "closing", "sizes", "levels")
    tot_neg = tot_pop = tot_c0 = 0
    for name, (mu, V) in inst.items():
        S = A.SharpestTails(mu, V)
        Atot = float((mu * V).sum())
        atom = float(mu.min())
        bad = {k: 0 for k in keys}
        ch_fail = 0
        nrun_inst = 0
        for pset in range(6):
            prng = np.random.default_rng(31337 + 17 * cell)
            lam = float(prng.choice([0.25, 1.0]))
            eta = float(prng.choice([0.2, 0.5]))
            etap = float(prng.choice([0.3, 1.0, 20.0]))
            theta = float(prng.choice([0.3, 1.0, 5.0]))
            b = float(prng.choice([0.3, 1.0]))
            kappa0 = float(prng.choice([1.0, 0.1]))
            x0 = float(prng.choice([4.0, 12.0]))
            r0 = float(prng.choice([0.0, 1.0, 4.0]))
            vcap = float(prng.choice([1.0, math.e ** 2]))
            theta_fn = S.Theta if pset % 2 == 0 else (lambda p_: p_)
            P = A.Params(lam=lam, eta=eta, etap=etap, theta=theta, nu1=1.0, b=b, delta=0.05, kappa0=kappa0,
                         x=(x0, (x0 + b) / 2, b), C=(1.0, 5.0, 25.0))
            ell0 = Atot * math.exp(-r0)
            Vmax = float(V.max()) * vcap
            cdf = np.cumsum(mu)
            for placement in ("random", "top", "bottom"):
                for r in range(runs):
                    rng = np.random.default_rng(1000000 + 1000 * cell + r)
                    rec = A.run_A(P, V, lambda m_: np.minimum(np.searchsorted(cdf, rng.random(m_)), len(V) - 1),
                                  S.Xi, theta_fn, ell0, atom, rng, Vmax=Vmax, placement=placement,
                                  max_points=3_000_000)
                    if rec["stop"] == "abort" and rec["abort"].startswith("max_points"):
                        limited += 1
                        continue
                    chk = A.check_run(rec, P, mu, V)
                    nruns += 1
                    nrun_inst += 1
                    for k in keys:
                        bad[k] += not chk[k]
                    ch_fail += not chk["chernoff"]
                    if chk["stop"] == "abort":
                        bad["valid"] += 0          # an abort returns the trivial bracket, counted through 'valid'
                    tot_neg += chk["n_neg"]
                    tot_pop += chk["n_pop"]
                    tot_c0 += chk["stop"] == "c0"
                cell += 1
        nb = sum(bad.values())
        viol += nb
        print(f"  {name:48s} A = {Atot:9.3e}: runs {nrun_inst}; violations by claim "
              f"{ {k: v for k, v in bad.items() if v} if nb else 0}; Chernoff events failed in {ch_fail} runs")
    print(f"block S: {nruns} runs checked ({limited} more stopped by the harness limit of 3e6 points and not "
          f"counted); levels left as populated {tot_pop}, as negligible {tot_neg}; stops by rule (c0): {tot_c0}")
    print(f"block S violations of any claim of Theorem N1: {viol}")
    # mutations: the checks must be able to fail
    print("mutations (each must produce failures):")
    mfail_total = 0
    for name in ("gap: a cluster of mass 0.0105 higher by 1000", "two values {1, 500}", "lognormal, sd 3"):
        cand = [k for k in inst if k.startswith(name[:12])]
        mu, V = inst[cand[0]] if name not in inst else inst[name]
        S = A.SharpestTails(mu, V)
        Atot = float((mu * V).sum())
        cdf = np.cumsum(mu)
        for label, kw, xi in (("Xi/20", {}, lambda q_: S.Xi(q_) / 20.0), ("K = 2", dict(K_override=2), S.Xi),
                              ("Theta x 5", {}, S.Xi)):
            P = A.Params(lam=1.0, eta=0.5, etap=1.0, theta=1.0, nu1=1.0, b=0.5, delta=0.05, kappa0=1.0,
                         x=(8.0, 2.0, 0.5), C=(1.0, 5.0, 25.0), **kw)
            th = (lambda p_: min(1.0, 5.0 * S.Theta(p_))) if label == "Theta x 5" else S.Theta
            nbad = 0
            for r in range(max(runs, 20)):
                rng = np.random.default_rng(2000000 + 1000 * cell + r)
                rec = A.run_A(P, V, lambda m_: np.minimum(np.searchsorted(cdf, rng.random(m_)), len(V) - 1), xi, th,
                              Atot * math.exp(-1.0), float(mu.min()), rng, Vmax=float(V.max()),
                              max_points=3_000_000)
                chk = A.check_run(rec, P, mu, V)
                nbad += (not chk["valid"]) or (not chk["cert_q"]) or (not chk["cert_p"]) or (not chk["cert_tail"]) \
                    or (not chk["cert_ell"])
            cell += 1
            mfail_total += nbad
            print(f"   '{cand[0] if name not in inst else name}', {label}: runs with a false certificate or an invalid "
                  f"bracket: {nbad} of {max(runs, 20)}")
    print(f"mutations: failures detected {mfail_total}")
    return viol + (0 if mfail_total > 0 else 1)


# ------------------------------------------------------------------------------------------ block U

class GaussLine:
    """V = e^{L x}, x ~ N(0,1).  Tail functions of the class Lip_L (Theorem N9), exact for this V."""

    def __init__(self, L):
        self.L = L
        self.A = math.exp(L * L / 2)
        self.ell0 = 2 * math.exp(L * L / 2) * ndtr(-L)            # E e^{-L|x|}
        self.u0 = 2 * math.exp(L * L / 2) * ndtr(L)               # E e^{+L|x|}

    def Xi(self, q):
        if q >= 1 - 1e-15:
            return math.inf
        t = -ndtri(q)
        L = self.L
        return math.exp(L * L / 2 - L * t + log_ndtr(L - t)) - math.exp(log_ndtr(-t))

    def Theta(self, p):
        if p >= 1 - 1e-15:
            return 1.0
        c = ndtri(p)
        L = self.L
        return min(1.0, p + math.exp(L * c + L * L / 2 + log_ndtr(-c - L)))

    def sample(self, rng, n):
        return rng.standard_normal(n)

    def V(self, x):
        return np.exp(self.L * x)

    def p_gt(self, s):
        return float(ndtr(-math.log(s) / self.L))

    def excess(self, s):
        t = math.log(s) / self.L
        return float(self.A * ndtr(self.L - t) - s * ndtr(-t))


class LaplaceLine:
    """V = e^{u x}, x two-sided exponential (density e^{-|x|}/2), 0 < u < 1: P(V > s) = s^{-1/u}/2 for s >= 1 (a
    Pareto tail).  Sharpest tail functions of V in closed form; Xi(q) = q u/(1-u) for q <= 1/2."""

    def __init__(self, u):
        self.u = u
        self.A = 1.0 / (1 - u * u)
        self.ell0 = 1.0 / (1 + u)             # E e^{-u|x|}
        self.u0 = 1.0 / (1 - u)               # E e^{+u|x|}

    def p_gt(self, s):
        t = math.log(s) / self.u
        return 0.5 * math.exp(-t) if t >= 0 else 1 - 0.5 * math.exp(t)

    def excess(self, s):
        u = self.u
        t = math.log(s) / u
        if t >= 0:
            return 0.5 * math.exp(-(1 - u) * t) * u / (1 - u)
        return 0.5 * ((1 - math.exp((1 + u) * t)) / (1 + u) - math.exp(u * t) * (1 - math.exp(t))) \
            + 0.5 * (1 / (1 - u) - math.exp(u * t))

    def quantile(self, q):                    # s with P(V > s) = q
        t = -math.log(2 * q) if q <= 0.5 else math.log(2 * (1 - q))
        return math.exp(self.u * t)

    def Xi(self, q):
        if q >= 1 - 1e-15:
            return math.inf
        s = self.quantile(q)
        return self.excess(s) / s

    def Theta(self, p):
        if p >= 1 - 1e-15:
            return 1.0
        s = self.quantile(p)
        return min(1.0, (self.A - self.excess(s)) / s)

    def sample(self, rng, n):
        return rng.laplace(0.0, 1.0, n)

    def V(self, x):
        return np.exp(self.u * x)


def closing_level_numeric(Xi, Theta, theta, eta, nu1):
    """Largest pi on a grid such that Xi(q) <= theta nu1 q and Xi(q) <= theta max(c q, Theta(c q)) for all grid
    points q < pi (the J-free conditions of Theorem N1'); q from 1e-300 upward, 4000 log-spaced points."""
    c = (1 - eta) / (1 + eta)
    qs = np.exp(np.linspace(math.log(1e-300), math.log(0.999), 4000))
    ok_until = None
    for q in qs:
        xi = Xi(q)
        if xi <= theta * nu1 * q and xi <= theta * max(c * q, Theta(c * q)):
            ok_until = q
        else:
            break
    return ok_until


def block_U(runs):
    viol, cell, nruns = 0, 0, 0
    keys = ("valid", "width", "cert_q", "cert_p", "cert_ell", "cert_tail", "closing", "sizes", "levels")
    print(f"seeds: run r of cell c uses default_rng(3000000 + 1000*c + r), r < {runs}")
    cases = []
    for L in (1.5, 2.5):
        cases.append((f"Gauss line, V = e^(L x), L = {L}", GaussLine(L)))
    for u in (0.5, 0.8):
        cases.append((f"Laplace line, V = e^(u x), u = {u} (Pareto index {1 / u:.2f})", LaplaceLine(u)))
    for name, G in cases:
        # self-check of the tail functions on a grid (TU), (TL) with exact p and excess
        worst = 0.0
        for s in np.exp(np.linspace(-6, 12, 400)):
            p = G.p_gt(s)
            if 1e-250 < p < 1 - 1e-12:
                worst = max(worst, G.excess(s) / (s * G.Xi(p)) - 1, s * max(p, G.Theta(p)) / (G.A - G.excess(s)) - 1)
        print(f" {name}: A = {G.A:.4f}, ell0 = {G.ell0:.4f}, u0 = {G.u0:.4f}; (TU), (TL) on 400 levels: largest "
              f"excess over equality {worst:.1e}")
        viol += worst > 1e-8
        for (theta, etap, nu1, label) in ((1.0, 1.0, 1.0, "standard"), (0.5, 1.0, 1.0, "small theta"),
                                          (1.0, 60.0, 1.0, "large eta' (nu0 small: negligible levels)"),
                                          (0.3, 200.0, 1.0, "large eta', small theta")):
            if isinstance(G, LaplaceLine):
                nu1 = max(1.0, 1.05 * G.u / ((1 - G.u) * theta))      # [N'] needs theta nu1 >= u/(1-u)
            P = A.Params(lam=1.0, eta=0.5, etap=etap, theta=theta, nu1=nu1, b=0.5, delta=0.05, kappa0=1.0,
                         x=(6.0, 2.0, 0.5), C=(1.0, 5.0, 25.0))
            pi_star = closing_level_numeric(G.Xi, G.Theta, theta, P.eta, nu1)
            if pi_star is None:
                print(f"   {label}: theta = {theta}, nu1 = {nu1:.2f}: NO positive closing level on the grid -> "
                      f"Theorem N1' gives no bound; not run")
                continue
            cst = A.constants(P, G.ell0, pi_star, u0=G.u0)
            bad = {k: 0 for k in keys}
            negs = pops = 0
            maxj, maxM, ch = 0, 0, 0
            nr = 0
            for r in range(runs):
                rng = np.random.default_rng(3000000 + 1000 * cell + r)
                rec = A.run_A(P, G.V, lambda m_: G.sample(rng, m_), G.Xi, G.Theta, G.ell0, pi_star, rng, u0=G.u0,
                              max_points=4_000_000)
                if rec["stop"] == "abort" and rec["abort"].startswith("max_points"):
                    continue
                chk = A.check_core(rec, P, G.A, G.p_gt, G.excess, G.V(rec["idx"]))
                nr += 1
                for k in keys:
                    bad[k] += not chk[k]
                if chk["stop"] == "abort":
                    bad["levels"] += 1                     # on the good event no abort may occur
                negs += chk["n_neg"]
                pops += chk["n_pop"]
                ch += not chk["chernoff"]
                maxj = max(maxj, rec["close"]["j"] if rec["close"] else 0)
                maxM = max(maxM, chk["maxM"])
            cell += 1
            nruns += nr
            nb = sum(bad.values())
            viol += nb
            print(f"   {label}: theta = {theta}, eta' = {etap}, nu1 = {nu1:.2f}: pi* = {pi_star:.3e}, J = {cst['J']}, "
                  f"K = {cst['K']}, Mbar = {cst['Mbar']:.2e}; runs {nr}; violations "
                  f"{ {k: v for k, v in bad.items() if v} if nb else 0}; Chernoff failed {ch}; levels left populated "
                  f"{pops}, NEGLIGIBLE {negs}; highest closing level {maxj} (J = {cst['J']}); largest sample {maxM}")
    # where N1' gives nothing: the closing level as a function of theta for the Laplace line with nu1 = 1
    print(" Laplace line, nu1 = 1: Xi(q)/q = u/(1-u) for all q <= 1/2, so [N'] holds iff theta >= u/(1-u):")
    for u in (0.5, 0.8, 0.95):
        G = LaplaceLine(u)
        row = []
        for theta in (0.3, 1.0, 3.0, 10.0, 30.0):
            pi = closing_level_numeric(G.Xi, G.Theta, theta, 0.5, 1.0)
            row.append(f"theta={theta:g}: {'none' if pi is None else f'{pi:.2e}'}")
        print(f"   u = {u}: u/(1-u) = {u / (1 - u):.2f}; one evaluation certifies the ratio (1+u)/(1-u) = "
              f"{(1 + u) / (1 - u):.1f}; closing level: " + "; ".join(row))
    print(f"block U: {nruns} runs; violations of any claim of Theorem N1': {viol}")
    return viol


# ------------------------------------------------------------------------------------------ block Q1

def block_Q1(runs):
    m, u = 4, 1.0
    pts = np.arange(1 << m)
    ham = np.array([[bin(int(a) ^ int(c)).count("1") for c in pts] for a in pts], dtype=float)
    mu = np.full(1 << m, 1.0 / (1 << m))
    V = np.exp(u * ham[:, 0])                         # V(a) = e^{u d(a, 0)}: a member, minimum 1 at a = 0
    Atot = float((mu * V).sum())
    ell0 = Atot / 10.0
    Vmax = float(V.max())
    print(f"Q_4, u = 1, V(a) = e^(u d(a,0)) (a member of the class), A = {Atot:.4f}, ell0 = A/10, kappa0 = 0.3 "
          f"(s0 = {0.3 * ell0:.4f} < min V = 1), theta = 2.5")
    out = 0
    for literal in (True, False):
        T = A.EnumeratedEnvelope(mu, u * ham, literal_q1=literal)
        P = A.Params(lam=1.0, eta=0.5, etap=1.0, theta=2.5, nu1=1.0, b=0.5, delta=0.05, kappa0=0.3,
                     x=(8.0, 2.0, 0.5), C=(1.0, 5.0, 25.0))
        inval = 0
        Us = []
        for r in range(runs):
            rng = np.random.default_rng(4000000 + r)
            rec = A.run_A(P, V, lambda m_: rng.integers(0, 1 << m, m_), T.Xi, T.Theta, ell0, 1.0 / (1 << m), rng,
                          Vmax=Vmax)
            chk = A.check_run(rec, P, mu, V)
            inval += not chk["valid"]
            Us.append(rec["U"] / Atot)
        print(f"  Xi(1) {'= the finite value of the formula with D != X (' + format(T.Xi(1.0), '.3f') + ')' if literal else '= +infinity'}"
              f": invalid brackets {inval} of {runs}; U/A median {np.median(Us):.3f}")
        if literal:
            out += 0 if inval == runs else 1          # the literal formula must fail (that is the finding)
        else:
            out += inval                              # the corrected one must not
    return out


if __name__ == "__main__":
    t0 = time.time()
    block = sys.argv[1] if len(sys.argv) > 1 else "S"
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    print(f"r26_n1.py block {block} runs {runs}; started {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    v = dict(S=block_S, U=block_U, Q1=block_Q1)[block](runs)
    print(f"exit violations: {v}")
    print(f"finished {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}; elapsed {time.time() - t0:.1f} s; "
          f"peak memory {A.peak_mb():.0f} MB")
    sys.exit(1 if v else 0)
