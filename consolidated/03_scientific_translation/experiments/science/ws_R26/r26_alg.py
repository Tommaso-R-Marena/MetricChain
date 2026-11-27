#!/usr/bin/env python3
"""r26_alg.py -- workstream R26 (internal review by an AI agent).

An implementation of "Algorithm A" written from N_REPORT 2.2-2.3 only (setting (S), constants, steps 0-3, rule
(c0), the abort rules; Theorem N1' variant without a cap), together with

  * tail functions: Harper's functions of the uniform cube (as the table (R4) of N_REPORT 2.5 states them), the
    functions of Lemma N.0 for an envelope on a small finite space (by enumeration of all subsets), and the
    sharpest tail functions of one given integrand;
  * a simulated inner oracle: brackets of the promised ratio around the exact V(a) (placement random / top /
    bottom / middle), so that the event (V1) holds by construction -- as in N_REPORT 7.3; NOT an end-to-end run;
  * a checker of every claim of Theorem N1 that can be checked on one run with the exact integrand in hand.

Nothing here was copied from the theory division's scripts (they were not available).
"""
import math
import resource
import sys
import time
from math import comb

import numpy as np


# ------------------------------------------------------------------------------------------- tail functions

class HarperCube:
    """Uniform cube Q_m, slope u per flip.  Xi(q): 0 for q < 2^-m; 2^-m E_r(m) with r the least radius such that
    |B(m,r)| >= 2^m q; +inf if r = m.  Theta(p) = 2^-m T_m(k), k the largest radius with |B(m,k)| <= max(1, 2^m p).
    E_r = sum_{i<=r} C(m,i) (e^{u(r+1-i)} - 1),   T_k = sum_{i<=k} C(m,i) + sum_{i>k} C(m,i) e^{-u(i-k)}."""

    def __init__(self, m, u):
        self.m, self.u = m, u
        self.binom = np.array([comb(m, i) for i in range(m + 1)], dtype=float)
        self.ball = np.cumsum(self.binom)
        self.E = np.array([sum(self.binom[i] * math.expm1(u * (r + 1 - i)) for i in range(r + 1))
                           for r in range(m + 1)])
        self.T = np.array([self.ball[k] + sum(self.binom[i] * math.exp(-u * (i - k)) for i in range(k + 1, m + 1))
                           for k in range(m + 1)])
        self.size = 2.0 ** m

    def radius(self, q):
        x = self.size * q
        if x < 1.0 - 1e-12:
            return -1
        return int(np.searchsorted(self.ball, x * (1 - 1e-12), side="left"))

    def Xi(self, q):
        r = self.radius(q)
        if r < 0:
            return 0.0
        if r >= self.m:
            return math.inf
        return self.E[r] / self.size

    def Theta(self, p):
        x = max(1.0, self.size * p)
        k = int(np.searchsorted(self.ball, x * (1 + 1e-12), side="right")) - 1
        k = max(0, min(k, self.m))
        return self.T[k] / self.size

    def closing_level(self, theta, eta, nu0):
        """sup{pi : Xi(q) <= theta(1-eta)nu0 q and Xi(q) <= theta max(c q, Theta(c q)) for all q < pi}, c = c_eta.
        Xi is constant on (|B(r-1)|, |B(r)|] 2^-m and the right sides are nondecreasing and right-continuous, so
        the conditions hold on the whole step iff they hold at its left end."""
        c = (1 - eta) / (1 + eta)
        best = 1.0 / self.size                       # for q < 2^-m, Xi = 0
        for r in range(0, self.m):
            qleft = (self.ball[r - 1] if r >= 1 else 1.0) / self.size
            xi = self.E[r] / self.size
            okN = xi <= theta * (1 - eta) * nu0 * qleft
            okP = xi <= theta * max(c * qleft, self.Theta(c * qleft))
            if okN and okP:
                best = self.ball[r] / self.size
            else:
                break
        return best


class EnumeratedEnvelope:
    """Lemma N.0 on a finite space of N <= 20 points with probabilities mu and an envelope rho[x, z] (rho[x,x] = 0):
        Xi(q)   = max{ sum_{x in D} mu(x) (e^{rho(x -> D^c)} - 1) : mu(D) <= q, D != X },   Xi(1) = +inf  (*),
        Theta(p) = min{ sum_x mu(x) e^{-rho(S -> x)} : mu(S) >= p }.
    (*) the lemma's formula has "D != X" and would give a finite value at q = 1; (TU) at q = 1 forces +inf (N_REPORT
    2.1), and this class returns +inf for q >= 1 - 1e-12 unless literal_q1=True (used once, to show the difference)."""

    def __init__(self, mu, rho, literal_q1=False):
        mu = np.asarray(mu, dtype=float)
        N = len(mu)
        assert N <= 20
        self.N, self.mu, self.literal = N, mu, literal_q1
        nsub = 1 << N
        member = ((np.arange(nsub, dtype=np.int64)[:, None] >> np.arange(N)[None, :]) & 1).astype(bool)   # [D, x]
        meas = member.astype(float) @ mu
        # rho(x -> D^c) = min_{z not in D} rho[x, z];  rho(S -> x) = min_{y in S} rho[y, x]
        f_up = np.zeros(nsub)
        f_lo = np.zeros(nsub)
        chunk = 1 << 12
        for lo in range(0, nsub, chunk):
            mem = member[lo:lo + chunk]                                   # [d, x]
            big = np.where(mem[:, None, :], np.inf, rho[None, :, :])      # [d, x, z], z in D -> inf
            dist_out = big.min(axis=2)                                    # rho(x -> D^c); inf if D = X
            with np.errstate(over="ignore", invalid="ignore"):
                val = np.where(mem, mu[None, :] * np.expm1(np.where(np.isfinite(dist_out), dist_out, 0.0)), 0.0)
            f_up[lo:lo + chunk] = val.sum(axis=1)
            big2 = np.where(mem[:, :, None], rho[None, :, :], np.inf)     # [d, y, x], y not in S -> inf
            dist_in = big2.min(axis=1)                                    # rho(S -> x); inf if S empty
            f_lo[lo:lo + chunk] = (mu[None, :] * np.exp(-dist_in)).sum(axis=1)
        f_up[nsub - 1] = np.inf if not literal_q1 else -np.inf            # D = X excluded from the sup
        # upper: prefix maximum over subsets sorted by measure
        order = np.argsort(meas, kind="stable")
        self.up_meas = meas[order]
        fu = f_up[order].copy()
        if literal_q1:
            fu[np.isneginf(fu)] = 0.0
        self.up_val = np.maximum.accumulate(fu)
        # lower: suffix minimum over subsets sorted by measure (mu(S) >= p)
        self.lo_meas = meas[order]
        fl = f_lo[order]
        self.lo_val = np.minimum.accumulate(fl[::-1])[::-1]
        self.atom = mu[mu > 0].min()

    def Xi(self, q):
        if q >= 1 - 1e-12 and not self.literal:
            return math.inf
        i = int(np.searchsorted(self.up_meas, q * (1 + 1e-12), side="right")) - 1
        return float(self.up_val[i]) if i >= 0 else 0.0

    def Theta(self, p):
        i = int(np.searchsorted(self.lo_meas, p * (1 - 1e-12), side="left"))
        if i >= len(self.lo_meas):
            return float(self.lo_val[-1])
        return float(min(1.0, self.lo_val[i]))


class SharpestTails:
    """The smallest upper and the largest lower tail function of ONE integrand V on a finite space (mu, V):
        Xi_V(q) = E(V - s*)_+ / s*,  s* = min{v : mu(V > v) <= q}   (E(V-s)_+/s decreases in s);  Xi_V(1) = +inf;
        Theta_V(q) = E min(V, s0)/s0,  s0 = max{v : mu(V >= v) >= q}   (E min(V,s)/s decreases in s).
    Any smaller Xi or larger Theta violates (TU) or (TL) for this V: the most adversarial valid input."""

    def __init__(self, mu, V):
        mu = np.asarray(mu, dtype=float)
        V = np.asarray(V, dtype=float)
        order = np.argsort(V)
        v, w = V[order], mu[order]
        vals, inv = np.unique(v, return_inverse=True)
        mass = np.zeros(len(vals))
        np.add.at(mass, inv, w)
        self.vals, self.mass = vals, mass
        above = np.concatenate([np.cumsum(mass[::-1])[::-1][1:], [0.0]])       # mu(V > vals[i])
        atleast = np.cumsum(mass[::-1])[::-1]                                   # mu(V >= vals[i])
        self.above, self.atleast = above, atleast
        # E(V - vals[i])_+ and E min(V, vals[i])
        tailsum = np.concatenate([np.cumsum((mass * vals)[::-1])[::-1][1:], [0.0]])
        self.excess = tailsum - vals * above
        headsum = np.concatenate([[0.0], np.cumsum(mass * vals)[:-1]])          # sum over V < vals[i]
        self.trunc = headsum + vals * atleast

    def Xi(self, q):
        if q >= 1 - 1e-12:
            return math.inf
        # smallest i with above[i] <= q  (above is nonincreasing in i)
        i = int(np.searchsorted(-self.above, -q * (1 + 1e-12), side="left"))
        i = min(i, len(self.vals) - 1)
        return float(self.excess[i] / self.vals[i])

    def Theta(self, q):
        # largest i with atleast[i] >= q  (atleast is nonincreasing in i)
        i = int(np.searchsorted(-self.atleast, -q * (1 - 1e-12), side="right")) - 1
        i = max(0, min(i, len(self.vals) - 1))
        return float(min(1.0, self.trunc[i] / self.vals[i]))


# ------------------------------------------------------------------------------------------- the algorithm

class Params:
    def __init__(self, lam=1.0, eta=0.5, etap=1.0, theta=1.0, nu1=1.0, b=0.5, delta=0.05, kappa0=1.0,
                 x=(8.0, 2.0, 0.5), C=(1.0, 10.0, 100.0), c_ref=1.0, K_override=None):
        self.lam, self.eta, self.etap, self.theta, self.nu1 = lam, eta, etap, theta, nu1
        self.b, self.delta, self.kappa0 = b, delta, kappa0
        self.x, self.C, self.c_ref, self.K_override = tuple(x), tuple(C), c_ref, K_override
        assert self.x[-1] <= b + 1e-12 and all(self.x[i] > self.x[i + 1] for i in range(len(self.x) - 1))

    def x_out(self):
        return math.log(self.kappa0 + math.exp(self.b) * (math.exp(self.lam) * (1 + self.eta) / (1 - self.eta)
                                                           + self.etap + self.theta))


def constants(P, ell0, pi_star, Vmax=None, u0=None):
    """The constants of N_REPORT 2.2 (cap variant: Vmax given) or of Theorem N1' (no cap: u0 given)."""
    lam, eta = P.lam, P.eta
    L = len(P.x) - 1
    s0 = P.kappa0 * ell0
    if Vmax is not None:
        # "J = ceil(ln(Vmax/s0)/lam) (or any larger integer)": when Vmax lies on the level grid up to rounding,
        # s_J computed in floating point can fall one ulp below Vmax and rule (c0) then fires at level J+1; the
        # +1e-12 makes J the larger integer in that case (allowed by the statement), and the comparison
        # s_j >= Vmax in the run stays exact.  (First version had -1e-12: 18 false "level > J" flags on a flat
        # integrand, out_n1_S_1.txt.)
        J = max(0, math.ceil(math.log(Vmax / s0) / lam + 1e-12))
    else:
        J = math.floor((math.log(u0 / s0) + P.b + lam + math.log((1 + eta) / ((1 - eta) * pi_star))) / lam)
    nu0 = max((J + 1) * math.expm1(lam) / P.etap, P.nu1) / (1 - eta)
    m_max = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * nu0 / ((1 - eta) * pi_star)) - 1e-12)
    K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * (J + 1) * (m_max + 1) * (L + 2) / P.delta))
    K_theorem = K
    if P.K_override is not None:
        K = int(P.K_override)
    nu = K * nu0
    Mdag = K / ((1 - eta) * pi_star)
    Mbar = 2 * (1 + eta) * math.exp(lam) * nu0 * Mdag
    cnt = [max(K, 2 * (1 + eta) ** 2 / (1 - eta) * math.exp(lam) * nu * math.exp(xv)) for xv in P.x]
    Cmax = P.c_ref + 2 * Mbar * P.C[0] + sum(min(2 * Mbar, (J + 1) * cnt[l - 1]) * P.C[l] for l in range(1, L + 1))
    return dict(s0=s0, J=J, nu0=nu0, m_max=m_max, K=K, K_theorem=K_theorem, nu=nu, Mdag=Mdag, Mbar=Mbar, cnt=cnt,
                Cmax=Cmax, L=L, x_out=P.x_out(), pi_star=pi_star)


def run_A(P, Vtab, sampler, Xi, Theta, ell0, pi_star, rng, Vmax=None, u0=None, placement="random",
          max_points=None):
    """One run.  Vtab[a] = exact V on the outer space (used by the oracle only); sampler(n) -> n outer indices
    i.i.d. from mu_o.  Returns a record (dict).  The oracle returns, at rung l, a bracket of ratio exactly e^{x_l}
    containing V(a), intersected with the previous bracket."""
    cst = constants(P, ell0, pi_star, Vmax=Vmax, u0=u0)
    lam, eta, b, theta = P.lam, P.eta, P.b, P.theta
    s0, J, K, nu, L = cst["s0"], cst["J"], cst["K"], cst["nu"], cst["L"]
    Mcap = K * 2 ** cst["m_max"]
    cap_variant = Vmax is not None
    abort_bracket = (ell0, Vmax if cap_variant else u0)
    eb, enb = math.exp(b), math.exp(-b)

    def Thetabar(p):
        return max(p, Theta(p))

    idx = np.zeros(0, dtype=np.int64)
    Lb = np.zeros(0)
    Ub = np.zeros(0)
    rung = np.zeros(0, dtype=np.int64)
    Vi = np.zeros(0)
    queries = P.c_ref
    calls = [0] * (L + 1)
    rec = dict(cst=cst, levels=[], passes=[], stop=None, abort=None, close=None)

    def place(n):
        if placement == "random":
            return rng.random(n)
        if placement == "top":           # V at the top of its bracket
            return np.ones(n)
        if placement == "bottom":        # V at the bottom of its bracket
            return np.zeros(n)
        return np.full(n, 0.5)

    def finish(Lret, Uret, stop):
        rec.update(L=Lret, U=Uret, stop=stop, points=len(idx), queries=queries, calls=calls, idx=idx)
        return rec

    def abort(reason):
        rec["abort"] = reason
        return finish(abort_bracket[0], abort_bracket[1], "abort")

    ell, Sigma = ell0, 0.0
    upper_sum = 0.0
    j = 0
    while True:
        s = s0 * math.exp(j * lam)
        if cap_variant and s >= Vmax:
            Lret, Uret = max(ell, Sigma), s0 + upper_sum
            if Lret > Uret:
                return abort("L>U")
            rec["close"] = dict(j=j, rule="c0", tail=0.0, q=None, M=None, N=None, ell=ell, s=s)
            return finish(Lret, Uret, "c0")
        if (not cap_variant) and j > J:
            return abort("level J+1")
        ell_entry = ell
        Mneg = nu * s / (ell_entry * eb)
        M = K
        while True:
            if M > Mcap:
                return abort("M > K 2^m_max")
            if max_points is not None and M > max_points:
                return abort("max_points (harness limit, not part of the algorithm)")
            # draw new points if needed (each costs C0 for its rung-0 bracket)
            if M > len(idx):
                nnew = M - len(idx)
                if queries + nnew * P.C[0] > cst["Cmax"]:
                    return abort("C_max (point)")
                new = sampler(nnew)
                v = Vtab(new) if callable(Vtab) else Vtab[new]
                t = place(nnew)
                idx = np.concatenate([idx, new]) if len(idx) else np.asarray(new)
                Vi = np.concatenate([Vi, v])
                Lb = np.concatenate([Lb, v * np.exp(-P.x[0] * t)])
                Ub = np.concatenate([Ub, v * np.exp(P.x[0] * (1 - t))])
                rung = np.concatenate([rung, np.zeros(nnew, dtype=np.int64)])
                queries += nnew * P.C[0]
                calls[0] += nnew
            # classify a_1..a_M at level j
            while True:
                need = np.nonzero((Ub[:M] > s) & (Lb[:M] <= s * enb))[0]
                if len(need) == 0:
                    break
                if (rung[need] >= L).any():
                    return abort("unclassified at rung L")
                newr = rung[need] + 1
                cost = sum(P.C[r] for r in newr)
                if queries + cost > cst["Cmax"]:
                    return abort("C_max (inner call)")
                queries += cost
                for r in np.unique(newr):
                    calls[r] += int((newr == r).sum())
                xr = np.array([P.x[r] for r in newr])
                t = place(len(need))
                v = Vi[need]
                Lb[need] = np.maximum(Lb[need], v * np.exp(-xr * t))
                Ub[need] = np.minimum(Ub[need], v * np.exp(xr * (1 - t)))
                rung[need] = newr
            N = int((Ub[:M] > s).sum())
            q = min(1.0, max(N, K) / ((1 - eta) * M))
            populated = N >= K
            plow = None
            if populated:
                plow = N / ((1 + eta) * M)
                ell = max(ell, s * enb * Thetabar(plow))
            tail = s * Xi(q)
            rec["passes"].append((j, M, N, q))
            if tail <= theta * eb * ell:
                Lret = max(ell, Sigma + ((1 - math.exp(-lam)) * enb * s * plow if populated else 0.0))
                Uret = s0 + upper_sum + tail
                rec["close"] = dict(j=j, rule="c", tail=tail, q=q, M=M, N=N, ell=ell, s=s, populated=populated,
                                    plow=plow)
                if Lret > Uret:
                    return abort("L>U")
                return finish(Lret, Uret, "closure")
            if populated:
                rec["levels"].append(dict(j=j, s=s, kind="pop", q=q, plow=plow, M=M, N=N, ell_entry=ell_entry,
                                          Mneg=Mneg))
                Sigma += (1 - math.exp(-lam)) * enb * s * plow
                upper_sum += (s * math.exp(lam) - s) * q
                break
            if M >= Mneg:
                rec["levels"].append(dict(j=j, s=s, kind="neg", q=q, plow=None, M=M, N=N, ell_entry=ell_entry,
                                          Mneg=Mneg))
                upper_sum += (s * math.exp(lam) - s) * q
                break
            M *= 2
        j += 1


# ------------------------------------------------------------------------------------------- the checker

def check_run(rec, P, mu, Vtab, Xi=None, Theta=None, tol=1e-9):
    """Checks one run against the exact integrand on a finite space (mu, Vtab).  See check_core."""
    A = float((mu * Vtab).sum())
    order = np.argsort(Vtab)
    vs, ws = Vtab[order], mu[order]
    cum_above = np.concatenate([np.cumsum(ws[::-1])[::-1], [0.0]])       # cum_above[i] = mu(V >= vs[i])
    cumvw = np.concatenate([np.cumsum((ws * vs)[::-1])[::-1], [0.0]])

    def p_gt(s):                       # mu(V > s)
        i = int(np.searchsorted(vs, s, side="right"))
        return cum_above[i]

    def excess(s):                     # E (V - s)_+
        i = int(np.searchsorted(vs, s, side="right"))
        return cumvw[i] - s * cum_above[i]

    return check_core(rec, P, A, p_gt, excess, Vtab[rec["idx"]], tol=tol)


def check_core(rec, P, A, p_gt, excess, Vs, tol=1e-9):
    """Checks one run, given A, p(s) = mu(V > s), E(V-s)_+ and the values Vs of V at the sampled points:
      valid       L <= A <= U
      width       U <= e^{x_out} L                      (not for aborts)
      cert_q      p(s_i) <= q_i at every level left and at the closing pass     (certificates obtained by sampling)
      cert_p      p(s_i e^-b) >= plow_i at every populated level / pass
      cert_ell    final ell <= A
      cert_tail   E(V - s_j)_+ <= tail at the closing pass  (the tail bound; the only use of Xi for validity)
      chernoff    (V2) and (V3) at threshold s_j e^-b, on the realised sample, at every visited (j, M)
      closing     every level left has q_j >= pi_star
      sizes       every M <= Mbar
      levels      the run stopped at a level j <= J
    """
    cst = rec["cst"]
    out = dict(A=A, L=rec["L"], U=rec["U"], stop=rec["stop"], abort=rec["abort"])
    out["valid"] = (rec["L"] <= A * (1 + tol)) and (A <= rec["U"] * (1 + tol))
    out["width"] = True if rec["stop"] == "abort" else rec["U"] <= math.exp(cst["x_out"]) * rec["L"] * (1 + tol)
    enb = math.exp(-P.b)
    cert_q = cert_p = True
    for lev in rec["levels"]:
        if p_gt(lev["s"] * (1 + tol)) > lev["q"] * (1 + tol):
            cert_q = False
        if lev["kind"] == "pop" and p_gt(lev["s"] * enb * (1 - tol)) < lev["plow"] * (1 - tol):
            cert_p = False
    cl = rec["close"]
    cert_tail = True
    cert_ell = True
    if cl is not None:
        cert_ell = cl["ell"] <= A * (1 + tol)
        if cl["rule"] == "c":
            if p_gt(cl["s"] * (1 + tol)) > cl["q"] * (1 + tol):
                cert_q = False
            if cl.get("populated") and p_gt(cl["s"] * enb * (1 - tol)) < cl["plow"] * (1 - tol):
                cert_p = False
            cert_tail = excess(cl["s"]) <= cl["tail"] * (1 + tol) + 1e-300
            out["tail_true"] = excess(cl["s"])
            out["tail_cert"] = cl["tail"]
        else:
            cert_tail = excess(cl["s"]) <= 1e-300 + tol * A
    out.update(cert_q=cert_q, cert_p=cert_p, cert_tail=cert_tail, cert_ell=cert_ell)
    K, eta = cst["K"], P.eta
    ch = True
    for (j, M, N, q) in rec["passes"]:
        s = cst["s0"] * math.exp(j * P.lam)
        ps = p_gt(s * (1 + tol))
        X = int((Vs[:M] > s * (1 + tol)).sum())
        if not (M * ps <= K / (1 - eta) * (1 + tol) or X >= (1 - eta) * M * ps * (1 - tol)):
            ch = False
        t = s * enb
        pt = p_gt(t * (1 - tol))
        Xt = int((Vs[:M] > t * (1 - tol)).sum())
        if not (Xt < K or Xt <= (1 + eta) * M * pt * (1 + tol)):
            ch = False
    out["chernoff"] = ch
    out["closing"] = all(lev["q"] >= cst["pi_star"] * (1 - tol) for lev in rec["levels"])
    out["sizes"] = all(M <= cst["Mbar"] * (1 + tol) for (_, M, _, _) in rec["passes"])
    out["levels"] = (cl is None) or (cl["j"] <= cst["J"])
    out["points"] = rec["points"]
    out["queries"] = rec["queries"]
    out["maxM"] = max((M for (_, M, _, _) in rec["passes"]), default=0)
    out["n_neg"] = sum(lev["kind"] == "neg" for lev in rec["levels"])
    out["n_pop"] = sum(lev["kind"] == "pop" for lev in rec["levels"])
    return out


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


# ------------------------------------------------------------------------------------------- self-test

def selftest():
    viol = 0
    # Harper's functions against brute force over ALL subsets of Q_4 (Lemma N.0 with rho = u * Hamming)
    m = 4
    pts = np.arange(1 << m)
    ham = np.array([[bin(a ^ c).count("1") for c in pts] for a in pts], dtype=float)
    mu = np.full(1 << m, 1.0 / (1 << m))
    for u in (0.5, 1.0, 2.0):
        H = HarperCube(m, u)
        En = EnumeratedEnvelope(mu, u * ham)
        worst_up, worst_lo = 0.0, 0.0
        for r in range(0, m):                              # at ball sizes the two must coincide
            q = H.ball[r] / H.size
            worst_up = max(worst_up, abs(H.Xi(q) - En.Xi(q)) / H.Xi(q))
            worst_lo = max(worst_lo, abs(H.Theta(q) - En.Theta(q)) / H.Theta(q))
        between = all(En.Xi(q) <= H.Xi(q) * (1 + 1e-12) and En.Theta(q) >= H.Theta(q) * (1 - 1e-12)
                      for q in np.linspace(0.01, 0.99, 197))
        ok = worst_up < 1e-12 and worst_lo < 1e-12 and between
        viol += 0 if ok else 1
        print(f"selftest Harper vs all 65534 subsets of Q_4, u={u}: rel. diff at ball sizes up {worst_up:.1e} "
              f"lo {worst_lo:.1e}; Harper step functions dominate elsewhere: {between}")
    # sharpest tail functions of one V: (TU), (TL) hold with equality somewhere and for all levels
    rng = np.random.default_rng(1)
    for trial in range(20):
        n = 40
        mu = rng.dirichlet(np.ones(n))
        V = np.exp(rng.normal(0, 2, n))
        if trial % 3 == 0:
            V[: n // 2] = V[0]                                  # atoms / ties
        S = SharpestTails(mu, V)
        A = (mu * V).sum()
        worst = 0.0
        tight = 0.0
        for s in np.concatenate([np.unique(V), np.unique(V) * 1.0001, np.unique(V) * 0.9999]):
            p = mu[V > s].sum()
            pbar = mu[V >= s].sum()
            ex = (mu * np.maximum(V - s, 0)).sum()
            tr = (mu * np.minimum(V, s)).sum()
            if p > 0 and p < 1:
                xi = S.Xi(p)
                worst = max(worst, ex / (s * xi) - 1)
                tight = max(tight, ex / (s * xi))
            if pbar > 0:
                th = S.Theta(pbar)
                worst = max(worst, s * th / tr - 1)
        ok = worst < 1e-9 and tight > 1 - 1e-9
        viol += 0 if ok else 1
    print(f"selftest sharpest tail functions, 20 random integrands: violations so far {viol}")
    return viol


if __name__ == "__main__":
    t0 = time.time()
    v = selftest()
    print(f"selftest total violations: {v}")
    print(f"elapsed {time.time() - t0:.1f} s; peak memory {peak_mb():.0f} MB")
    sys.exit(1 if v else 0)
