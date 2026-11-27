#!/usr/bin/env python3
"""Workstream A1, addendum (questions B1, B2 of THY-REQ-0011) -- numerical checks with own code.

 Q1  The dictionary of theory Theorem 11.99 on the uniform cube, from the textbook formulas:
     F*_c(t) = t ln cosh(u/2) - ln cosh(tu/2) = (1-t) C_t(BSC(p_u));
     E_sp(theta) = sup_{a in (0,1)} ((1-a)/a)(C_a - theta) (Nakiboglu's Definition 13) = KL(rho_theta || p_u), KL(rho_theta||1/2) = theta
     (= the Suarez-Silbey-Oppenheim bias curve = D(delta_GV(R)||p) = Merhav's F_g - (ln 2 - R));
     Hoeffding's bound (Tomamichel-Hayashi eq. (3)) for P = Bern(p_u) [the cone's letter law], Q = Bern(1/2), type-II rate theta:
     sup_s ((1-s)/s)(D_s(P||Q) - theta) = the same curve;   hinted accuracy = E_sp(theta) - theta = u rho_theta - Lambda_1.
 Q2  (B2)  k equal groups of letters, pairwise likelihood ratio L = e^u: the k-ary symmetric 'vertex channel' with
     p_k = L/(L+k-1).  F*_k(t) = t Psi_k(u) - Psi_k(tu) = (1-t) C_t(k);  cutoff rate R_0(k) = C_{1/2}(k) = 2 F*_k(1/2).
     (a) R_0(k) is maximal over real k at k = sqrt(L) + 1;
     (b) at L = k(k-1):  F*_k(t) = F*_{k+1}(1-t) for all t  (so h_k = h_{k+1} and R_0(k) = R_0(k+1) there);
     (c) the Shannon capacity a_k = ln k - H(p_k, ...) is maximal over real k at k = (L-1)^2/(L ln L - L + 1)  (~ L/ln L).
 Q3  (generalised Proposition A1.1, report sect. 9.3)  Heteropolymer product landscapes: sites of several types, three
     letters, asymmetric envelopes d_j (triangle inequality), product known part.  For every admissible psi:
     (i)  every conditional law of nu_psi lies in the window polytope  P(L_j) = {p : pi(a) p(b) <= e^{d(a,b)} pi(b) p(a)};
     (ii) the vertices of P(L_j) are Gibbs laws of vertices of the Lipschitz polytope, and
          KL(nu_psi || prod_i Q*_{tau(i)}) <= sum_i a_{tau(i)},  a_j = min_Q max_{vertices} KL(. || Q)  (information radius = capacity),
          with equality for an additive instance built from capacity-achieving vertices.
 Q4  (report sect. 9.2(d))  The adaptive law against Burnashev's law.  On the cube the adaptive / hinted accuracy rate is
     e(theta) = E_sp(theta) - theta = u rho_theta - Lambda_1.  For the same channel BSC(p_u) the reliability function of
     variable-length codes with feedback is Burnashev's line E_B(R) = C_1 (1 - R/C), C_1 = max_{x,x'} D(W(.|x)||W(.|x'))
     (formula (4) of Berlin-Nakiboglu-Rimoldi-Telatar, arXiv:cs/0610145).  Checked: C_1 = u tanh(u/2); e(0+) = ln cosh(u/2);
     e vanishes at the fixed point h of E_sp (h = KL(Lambda_1/u || 1/2) < a = C); e is strictly convex in theta, hence not a line.
     (The two are different quantities -- an accuracy rate and an error exponent; the check only shows that the laws differ.)
Run: python3 addendum_checks.py     (about 10 s)
"""
import itertools
import math
import sys

import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar

rng = np.random.default_rng(99)
fails = 0
LN2 = math.log(2)


def check(name, ok, info=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + ("   " + info if info else ""))
    fails += (not ok)


def kl2(a, b):
    o = 0.0
    if a > 0:
        o += a * math.log(a / b)
    if a < 1:
        o += (1 - a) * math.log((1 - a) / (1 - b))
    return o


def kl(p, q):
    p, q = np.asarray(p, float), np.asarray(q, float)
    m = p > 0
    return float((p[m] * np.log(p[m] / q[m])).sum())


# ------------------------------------------------------------------ Q1
ok, worst = True, 0.0
for u in (0.5, 1.0, 2.0, 3.0):
    pu = 1 / (1 + math.exp(u))
    Lam = math.log(2 / (1 + math.exp(-u)))
    a = kl2(pu, 0.5)

    def C(al):  # Renyi capacity of order al of BSC(pu) = D_al(Bern(pu)||Bern(1/2))
        return LN2 + math.log(pu ** al + (1 - pu) ** al) / (al - 1)

    for t in np.linspace(0.02, 0.98, 49):
        Fc = t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2))
        worst = max(worst, abs(Fc - (1 - t) * C(t)))
    for frac in (0.1, 0.3, 0.5, 0.7, 0.9):
        theta = frac * a
        rho = brentq(lambda r: kl2(r, 0.5) - theta, 1e-12, 0.5)
        target = kl2(rho, pu)
        f = lambda al: -((1 - al) / al) * (C(al) - theta)
        res = minimize_scalar(f, bounds=(1e-4, 1 - 1e-6), method="bounded", options={"xatol": 1e-12})
        Esp = -res.fun
        worst = max(worst, abs(Esp - target))
        # Hoeffding's bound for P = Bern(pu), Q = Bern(1/2): identical expression (C_al = D_al(P||Q) for the BSC)
        hinted = u * rho - Lam
        worst = max(worst, abs((Esp - theta) - hinted))
        # Merhav's glassy free energy: F_g - (ln2 - R) = D(delta_GV(R)||p)
        Fg = rho * math.log(1 / pu) + (1 - rho) * math.log(1 / (1 - pu))
        worst = max(worst, abs(Fg - (LN2 - theta) - target))
check("Q1  cube dictionary: F*_c = (1-t)C_t; E_sp = sup_a ((1-a)/a)(C_a - theta) = KL(rho_theta||p_u) = F_g - (ln2 - R); E_sp - theta = u rho_theta - Lambda_1",
      worst < 1e-7, "max deviation %.1e" % worst)


# ------------------------------------------------------------------ Q2
def Psi(k, s):
    return math.log((math.exp(s) + k - 1) / k) - s / k


def Fk(k, u, t):
    return t * Psi(k, u) - Psi(k, t * u)


def renyi_cap_sym(k, L, al):
    """Renyi capacity of order al of the k-ary symmetric channel with correct prob p = L/(L+k-1) (uniform centre)"""
    p = L / (L + k - 1)
    w = (1 - p) / (k - 1)
    return math.log(k) + math.log(p ** al + (k - 1) * w ** al) / (al - 1)


dev = 0.0
for k in (2, 3, 4, 5):
    for u in (0.5, 1.3, 2.4):
        L = math.exp(u)
        for t in (0.2, 0.5, 0.8):
            dev = max(dev, abs(Fk(k, u, t) - (1 - t) * renyi_cap_sym(k, L, t)))
check("Q2  F*_k(t) = t Psi_k(u) - Psi_k(tu) = (1-t) C_t of the k-ary symmetric channel with p_k = e^u/(e^u+k-1)", dev < 1e-12,
      "max deviation %.1e" % dev)

# (a) cutoff rate maximal at k = sqrt(L) + 1
ok_a, rows = True, []
for u in (1.0, 2.0, 3.0, 5.0):
    L = math.exp(u)
    R0 = lambda k: 2 * Fk(k, u, 0.5)
    res = minimize_scalar(lambda k: -R0(k), bounds=(1.0001, 500.0), method="bounded", options={"xatol": 1e-10})
    ok_a &= abs(res.x - (math.sqrt(L) + 1)) < 1e-5
    rows.append("u=%.0f: argmax k = %.4f, sqrt(L)+1 = %.4f" % (u, res.x, math.sqrt(L) + 1))
check("Q2a cutoff rate R_0(k) = C_{1/2} is maximal over real k at k = e^{u/2} + 1", ok_a, "; ".join(rows))

# (b) symmetry at L = k(k-1)
dev_b, dev_h, dev_off = 0.0, 0.0, 0.0
for k in (2, 3, 4, 5, 6):
    u = math.log(k * (k - 1))
    for t in np.linspace(0.05, 0.95, 19):
        dev_b = max(dev_b, abs(Fk(k, u, t) - Fk(k + 1, u, 1 - t)))
    hk = -minimize_scalar(lambda t: -Fk(k, u, t), bounds=(0, 1), method="bounded", options={"xatol": 1e-13}).fun
    hk1 = -minimize_scalar(lambda t: -Fk(k + 1, u, t), bounds=(0, 1), method="bounded", options={"xatol": 1e-13}).fun
    dev_h = max(dev_h, abs(hk - hk1))
    # off the crossing the identity must fail (mutation)
    u2 = u + 0.2
    dev_off = max(dev_off, abs(Fk(k, u2, 0.3) - Fk(k + 1, u2, 0.7)))
check("Q2b at e^u = k(k-1):  F*_k(t) = F*_{k+1}(1-t) for all t, hence h_k = h_{k+1} and R_0(k) = R_0(k+1)   (k = 2..6)",
      dev_b < 1e-13 and dev_h < 1e-10 and dev_off > 1e-4,
      "max |F_k(t) - F_{k+1}(1-t)| = %.1e; max |h_k - h_{k+1}| = %.1e; off the crossing the identity fails by %.1e" % (dev_b, dev_h, dev_off))
vals = {u: [(-minimize_scalar(lambda t: -Fk(k, u, t), bounds=(0, 1), method="bounded").fun) for k in (2, 3, 4)] for u in (0.5, 1.0)}
check("Q2b' replication of the theory report's values h_2, h_3, h_4 at u = 0.5 (0.007673, 0.007425, 0.006552) and u = 1 (0.029139, 0.030654, 0.028405)",
      max(abs(x - y) for x, y in zip(vals[0.5], (0.007673, 0.007425, 0.006552))) < 6e-7
      and max(abs(x - y) for x, y in zip(vals[1.0], (0.029139, 0.030654, 0.028405))) < 6e-7,
      "mine: %s ; %s" % (", ".join("%.6f" % v for v in vals[0.5]), ", ".join("%.6f" % v for v in vals[1.0])))

# (d) integer optima: for (k-1)(k-2) < L < k(k-1) the integer maximiser of R_0 and of h is k
ok_d, cnt = True, 0
for k in range(2, 13):
    lo, hi = (k - 1) * (k - 2), k * (k - 1)
    for frac in (0.1, 0.5, 0.9):
        L = lo + frac * (hi - lo)
        if L <= 1.0:
            continue
        u = math.log(L)
        r0 = [2 * Fk(j, u, 0.5) for j in range(2, 20)]
        hh = [-minimize_scalar(lambda t, j=j: -Fk(j, u, t), bounds=(0, 1), method="bounded", options={"xatol": 1e-12}).fun for j in range(2, 20)]
        ok_d &= (2 + int(np.argmax(r0)) == k) and (2 + int(np.argmax(hh)) == k)
        cnt += 1
check("Q2d for (k-1)(k-2) < e^u < k(k-1) the integer maximiser of the cutoff rate and of h over the number of groups is k  (k = 2..12)",
      ok_d, "%d slopes" % cnt)

# (c) Shannon capacity maximal at k* = (L-1)^2/(L ln L - L + 1)
ok_c, rows = True, []
for u in (1.0, 2.0, 3.0, 5.0):
    L = math.exp(u)
    cap = lambda k: math.log(k / (L + k - 1)) + L * math.log(L) / (L + k - 1)
    res = minimize_scalar(lambda k: -cap(k), bounds=(1.0001, 5000.0), method="bounded", options={"xatol": 1e-10})
    kstar = (L - 1) ** 2 / (L * math.log(L) - L + 1)
    ok_c &= abs(res.x - kstar) < 1e-4 * kstar
    rows.append("u=%.0f: argmax k = %.3f (formula %.3f; e^{u/2}+1 = %.3f)" % (u, res.x, kstar, math.sqrt(L) + 1))
check("Q2c Shannon capacity a_k maximal at k = (L-1)^2/(L ln L - L + 1), L = e^u  -- a different law from the cutoff rate's", ok_c,
      "; ".join(rows))
# the report's a_2 > a_3 iff u < 0.5194
f = lambda u: (math.log(2 / (math.exp(u) + 1)) + math.exp(u) * u / (math.exp(u) + 1)) - (math.log(3 / (math.exp(u) + 2)) + math.exp(u) * u / (math.exp(u) + 2))
ucross = brentq(f, 0.1, 1.5)
check("Q2c' crossing a_2 = a_3 at u = 0.5194 (theory report)", abs(ucross - 0.5194) < 2e-4, "mine: %.5f" % ucross)


# ------------------------------------------------------------------ Q3  heteropolymer chain rule
def random_envelope(q, lo=0.4, hi=1.6):
    """random asymmetric d >= 0 with zero diagonal satisfying the triangle inequality (shortest-path closure)"""
    d = rng.uniform(lo, hi, size=(q, q))
    np.fill_diagonal(d, 0.0)
    for k in range(q):
        for i in range(q):
            for j in range(q):
                d[i, j] = min(d[i, j], d[i, k] + d[k, j])
    return d


def window_vertices(pi, d):
    """vertices of P(L) = {p in simplex: pi(a) p(b) <= e^{d(a,b)} pi(b) p(a)}  by enumerating tight constraint sets (small q)"""
    q = len(pi)
    cons = [(a, b) for a in range(q) for b in range(q) if a != b]
    verts = []
    for combo in itertools.combinations(cons, q - 1):
        A = np.zeros((q, q))
        rhs = np.zeros(q)
        for r, (a, b) in enumerate(combo):
            # pi(a) p(b) - e^{d(a,b)} pi(b) p(a) = 0
            A[r, b] += pi[a]
            A[r, a] -= math.exp(d[a, b]) * pi[b]
        A[q - 1, :] = 1.0
        rhs[q - 1] = 1.0
        if abs(np.linalg.det(A)) < 1e-12:
            continue
        p = np.linalg.solve(A, rhs)
        if p.min() <= 1e-12:
            continue
        feas = all(pi[a] * p[b] <= math.exp(d[a, b]) * pi[b] * p[a] * (1 + 1e-9) for (a, b) in cons)
        if feas and not any(np.allclose(p, v, atol=1e-9) for v in verts):
            verts.append(p)
    return verts


def info_radius(points):
    """min_Q max_k KL(p_k||Q) by Blahut-Arimoto on the channel whose rows are the points; returns (C, Q*, input law)"""
    W = np.array(points)
    m = len(W)
    w = np.ones(m) / m
    for _ in range(20000):
        Q = w @ W
        dv = np.array([kl(W[i], Q) for i in range(m)])
        wn = w * np.exp(dv)
        wn /= wn.sum()
        if np.abs(wn - w).max() < 1e-14:
            w = wn
            break
        w = wn
    Q = w @ W
    dv = np.array([kl(W[i], Q) for i in range(m)])
    return float(dv.max()), Q, w, dv


def admissible_regularise(phi, shape, ds):
    """psi(x) = min_y [phi(y) + d(x,y)], d(x,y) = sum_i d_i(x_i,y_i): admissible (psi(x) - psi(y) <= d(x,y)) by the triangle inequality."""
    psi = phi.copy()
    n = len(shape)
    for _ in range(n + 1):
        for ax in range(n):
            q = shape[ax]
            moved = np.moveaxis(psi, ax, 0)
            new = moved.copy()
            for a in range(q):
                for b in range(q):
                    if a != b:
                        new[a] = np.minimum(new[a], moved[b] + ds[ax][a, b])
            psi = np.moveaxis(new, 0, ax)
    return psi


def is_admissible(psi, shape, ds):
    n = len(shape)
    for ax in range(n):
        moved = np.moveaxis(psi, ax, 0)
        for a in range(shape[ax]):
            for b in range(shape[ax]):
                if a != b and (moved[a] - moved[b]).max() > ds[ax][a, b] + 1e-9:
                    return False
    return True


all_adm = True
ok_i = ok_ii = True
max_ratio, eq_gap, viol = 0.0, 1.0, 0.0
ninst = 0
for trial in range(6):
    # two site types: type 0 with 3 letters, type 1 with 2 or 3 letters
    q_types = [3, int(rng.integers(2, 4))]
    pis = [rng.dirichlet(np.ones(q) * 3) for q in q_types]
    dts = [random_envelope(q) for q in q_types]
    seq = [0, 1, 0, 1, 0, 1, 0][: (7 if max(q_types) == 3 and q_types[1] == 2 else 6)]
    shape = tuple(q_types[t] for t in seq)
    n = len(seq)
    ds = [dts[t] for t in seq]
    verts = [window_vertices(pis[t], dts[t]) for t in range(2)]
    radii = [info_radius(v) for v in verts]
    a_types = [r[0] for r in radii]
    Qs = [r[1] for r in radii]
    a_total = sum(a_types[t] for t in seq)
    # reference log-weights of pi and of the product proposal
    logpi = np.zeros(shape)
    logq = np.zeros(shape)
    for i, t in enumerate(seq):
        sh = [1] * n
        sh[i] = shape[i]
        logpi = logpi + np.log(pis[t]).reshape(sh)
        logq = logq + np.log(Qs[t]).reshape(sh)
    instances = []
    for scale in (0.5, 2.0, 8.0):
        instances.append(admissible_regularise(rng.normal(0, scale, size=shape), shape, ds))
    wells = np.zeros(shape)
    idx = tuple(int(rng.integers(0, s)) for s in shape)
    wells[idx] = -10.0
    instances.append(admissible_regularise(wells, shape, ds))
    instances.append(np.zeros(shape))
    # additive instance from capacity-achieving vertices (support of the optimal input law): equality case
    add = np.zeros(shape)
    for i, t in enumerate(seq):
        k = int(np.argmax(radii[t][2]))                    # a vertex in the support of the capacity-achieving input
        gam = -np.log(verts[t][k] / pis[t])                # pi_gamma = vertex law
        sh = [1] * n
        sh[i] = shape[i]
        add = add + gam.reshape(sh)
    instances.append(add)
    for j, psi in enumerate(instances):
        ninst += 1
        all_adm &= is_admissible(psi, shape, ds)
        lw = logpi - psi
        nu = np.exp(lw - lw.max())
        nu /= nu.sum()
        # (i) conditional laws along the natural order lie in the window polytope of the site
        for i, t in enumerate(seq):
            marg = nu.sum(axis=tuple(range(i + 1, n))) if i + 1 < n else nu
            den = marg.sum(axis=i, keepdims=True)
            cond = np.moveaxis(marg / np.maximum(den, 1e-300), i, -1).reshape(-1, shape[i])
            keep = np.moveaxis(den, i, -1).reshape(-1) > 1e-250
            cond = cond[keep]
            for a in range(shape[i]):
                for b in range(shape[i]):
                    if a != b:
                        lhs = pis[t][a] * cond[:, b]
                        rhs = math.exp(dts[t][a, b]) * pis[t][b] * cond[:, a]
                        viol = max(viol, float(((lhs - rhs) / np.maximum(rhs, 1e-300)).max()))
        # (ii) KL to the product of capacity-achieving output laws
        KLv = float((nu * (np.log(np.maximum(nu, 1e-300)) - logq))[nu > 0].sum())
        max_ratio = max(max_ratio, KLv / a_total)
        ok_ii &= KLv <= a_total * (1 + 1e-9)
        if j == len(instances) - 1:
            eq_gap = min(eq_gap, KLv / a_total)
ok_i = viol < 1e-8
check("Q3  generators produce admissible instances (asymmetric envelopes, two site types, 2-3 letters)", all_adm, "%d instances" % ninst)
check("Q3i every conditional law of nu_psi lies in the window polytope of its site", ok_i, "largest relative violation %.1e" % viol)
check("Q3ii KL(nu_psi || product of capacity-achieving site laws) <= sum_i a_tau(i); equality for additive instances on capacity-achieving vertices",
      ok_ii and eq_gap > 1 - 1e-6, "max KL/(sum a) = %.6f; additive vertex instances: min ratio %.6f" % (max_ratio, eq_gap))
# vertex laws are Gibbs laws of vertices of the Lipschitz polytope: check gamma = -ln(p/pi) is admissible and has q-1 tight constraints
okv = True
for t in range(2):
    for p in verts[t]:
        gam = -np.log(p / pis[t])
        q = len(p)
        tight = sum(1 for a in range(q) for b in range(q) if a != b and abs(gam[a] - gam[b] - dts[t][a, b]) < 1e-7)
        adm = all(gam[a] - gam[b] <= dts[t][a, b] + 1e-7 for a in range(q) for b in range(q) if a != b)
        okv &= adm and tight >= q - 1
check("Q3iii the vertices of the window are Gibbs laws of vertices of the site's Lipschitz polytope (>= q-1 tight constraints)", okv)
# mutation: a psi that violates the envelope must be able to leave the window
shape = (3, 3, 3)
d = random_envelope(3)
pi = rng.dirichlet(np.ones(3) * 3)
psi_bad = 5.0 * rng.normal(size=shape)
lw = sum(np.log(pi).reshape([3 if k == i else 1 for k in range(3)]) for i in range(3)) - psi_bad
nu = np.exp(lw - lw.max()); nu /= nu.sum()
m0 = nu.sum(axis=(1, 2))
bad = max((pi[a] * m0[b]) / (math.exp(d[a, b]) * pi[b] * m0[a]) for a in range(3) for b in range(3) if a != b)
check("Q3m mutation: a non-admissible psi leaves the window", bad > 1.0 + 1e-6, "ratio %.3f" % bad)

# ------------------------------------------------------------------ Q4  the adaptive law against Burnashev's line
ok4, rows = True, []
for u in (0.5, 1.0, 2.0, 3.0):
    pu = 1 / (1 + math.exp(u))
    Lam = math.log(2 / (1 + math.exp(-u)))
    a = kl2(pu, 0.5)
    C1 = kl2(pu, 1 - pu)                               # the two input letters of BSC(p_u): Bern(p_u) against Bern(1 - p_u)
    ok4 &= abs(C1 - u * math.tanh(u / 2)) < 1e-12

    def rho_of(th):
        return brentq(lambda r: kl2(r, 0.5) - th, 1e-14, 0.5, xtol=1e-15)

    def e(th):                                          # E_sp(theta) - theta = u rho_theta - Lambda_1  (checked in Q1)
        return u * rho_of(th) - Lam

    e0 = u * 0.5 - Lam                                  # theta -> 0+
    ok4 &= abs(e0 - math.log(math.cosh(u / 2))) < 1e-12 and e0 < C1
    h = brentq(e, 1e-12, a, xtol=1e-15)                 # E_sp(h) = h  <=>  e(h) = 0
    ok4 &= abs(kl2(rho_of(h), pu) - h) < 1e-9 and h < a
    ok4 &= abs(h - kl2(Lam / u, 0.5)) < 1e-9            # the theory report's h = KL(Lambda_1/u || 1/2)
    ths = np.linspace(0.05 * h, 0.95 * h, 19)
    ev = np.array([e(t) for t in ths])
    ok4 &= bool(((ev[2:] - 2 * ev[1:-1] + ev[:-2]) > 0).all())   # strictly convex on (0, h): not a line
    rows.append("u=%.1f: C_1 = %.4f, e(0+) = %.4f, h = %.5f < a = %.5f, e(h/2) = %.4f against the chord's %.4f"
                % (u, C1, e0, h, a, e(0.5 * h), 0.5 * e0))
check("Q4  adaptive law e(theta) = E_sp(theta) - theta on the cube against Burnashev's line C_1(1 - R/C) for BSC(p_u): "
      "C_1 = u tanh(u/2); e(0+) = ln cosh(u/2); e vanishes at h < a; e strictly convex (not a line)", ok4,
      "\n      " + "\n      ".join(rows))

# mutation for Q4: a line through (0, e(0+)) and (h, 0) is NOT e  (the convexity check has power)
u = 2.0
pu = 1 / (1 + math.exp(u)); Lam = math.log(2 / (1 + math.exp(-u)))
h = kl2(Lam / u, 0.5); e0 = math.log(math.cosh(u / 2))
rho_mid = brentq(lambda r: kl2(r, 0.5) - 0.5 * h, 1e-14, 0.5, xtol=1e-15)
gap = 0.5 * e0 - (u * rho_mid - Lam)
check("Q4m mutation: the straight line between the two endpoints differs from e at theta = h/2", gap > 1e-3, "chord - e = %.4f at u = 2" % gap)

print("\nfailures: %d" % fails)
sys.exit(1 if fails else 0)
