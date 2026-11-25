"""
t06_bruteforce_orientation.py -- brute force on a full product space with TWO site types and TWO ASYMMETRIC envelopes:
the finite-n statements that the transfer (Theorem 11.101, W_REPORT section 5) uses, in the orientation
   psi(x) - psi(y) <= d(x, y),      slack s0(y, x) = d(y, x) - psi0(y) + psi0(x)   (y outside the dip, x inside).

Chain: 2 sites of type A ('asym', 3 letters) + 2 sites of type B (2 letters, asymmetric envelope (0.7, 0.2)): 36 points.

 (1) quotient envelope = oriented transport cost (Lemma W1.0)
 (2) deepest dip, the dip formula, minimality
 (3) fibre averages are admissible for the outer envelope (F2)
 (4) tail lemma relative to a reference (flat-histogram instance of the lattice), and its failure when the slack is transposed
 (5) truncation at orbit-wise quantiles stays in the class and changes psi on orbit density <= q  (Theorem 11.95(a))
 (6) Z_g Phi_g^+(D) <= Z_H Phi_H^+(D) for invariant instances (Theorem 11.95, 'hardest invariant instance')
 (7) generalised dips with independent vertex labels (Proposition W4.0 = Theorem 11.101(a)): admissible, effect >= r,
     and  max_x P_labels(x in support) <= e^{tr} prod_j rho_t(M_j)^{n_j}
"""
import itertools, time
import numpy as np
from scipy.optimize import linprog
from r5lib import *

rng = np.random.default_rng(2026)
TOL = 1e-10

A = Site([0.5, 0.3, 0.2], [[0, 1, 2], [0.5, 0, 1.5], [1, 0.5, 0]], "asym")
B = Site([0.6, 0.4], [[0, 0.7], [0.2, 0]], "bin_asym")
types = [A, A, B, B]            # site i has type types[i]
tindex = [0, 0, 1, 1]
sites = [A, B]
n = len(types)
X = list(itertools.product(*[range(s.q) for s in types]))
N = len(X)
pi = np.array([np.prod([types[i].pi[x[i]] for i in range(n)]) for x in X])
D = np.array([[sum(types[i].d[x[i], y[i]] for i in range(n)) for y in X] for x in X])     # D[x, y] = d(x, y)


def jtype(x):
    return (tuple(sorted(x[:2])), tuple(sorted(x[2:])))


orbits = {}
for k, x in enumerate(X):
    orbits.setdefault(jtype(x), []).append(k)
orb_of = np.array([list(orbits).index(jtype(x)) for x in X])
orb_list = [np.array(v) for v in orbits.values()]
n_orb = len(orb_list)


def random_member():
    """psi(x) = min_y [c(y) + d(x, y)]  is in the class (triangle inequality of d)."""
    c = rng.uniform(0, 4.5, size=N) * rng.choice([0.3, 1.0, 2.0])
    return np.min(c[None, :] + D, axis=1)


def in_class(psi, tol=1e-9):
    return bool(np.all(psi[:, None] - psi[None, :] <= D + tol))


def A_of(psi):
    return float(pi @ np.exp(-psi))


def emp(x, j):
    idx = [i for i in range(n) if tindex[i] == j]
    q = sites[j].q
    p = np.zeros(q)
    for i in idx:
        p[x[i]] += 1.0 / len(idx)
    return p


def transport(site, Pp, P):
    """primal LP: min sum kappa(a,b) d(a,b), first marginal Pp, second marginal P."""
    q = site.q
    c = site.d.ravel()
    Aeq = np.zeros((2 * q, q * q))
    for a in range(q):
        Aeq[a, a * q:(a + 1) * q] = 1
    for b in range(q):
        Aeq[q + b, b::q] = 1
    res = linprog(c, A_eq=Aeq, b_eq=np.concatenate([Pp, P]), bounds=[(0, None)] * (q * q), method="highs")
    return res.fun


if __name__ == "__main__":
    t0 = time.time()
    print(f"space: {N} points, {n_orb} joint types; envelopes asymmetric: A {not np.allclose(A.d, A.d.T)}, B {not np.allclose(B.d, B.d.T)}")
    # ---------------------------------------------------------------- (1)
    worst = 0.0
    reps = [o[0] for o in orb_list]
    delta = np.zeros((n_orb, n_orb))
    for a_, oa in enumerate(orb_list):
        for b_, ob in enumerate(orb_list):
            delta[a_, b_] = D[np.ix_(oa, ob)].min()
            xa, xb = X[oa[0]], X[ob[0]]
            w = sum(2 * transport(sites[j], emp(xa, j), emp(xb, j)) for j in range(2))
            worst = max(worst, abs(delta[a_, b_] - w))
    print(f"(1) quotient envelope min d(x,y) over T_P x T_P' against sum_j n_j W_j(P_j,P'_j) [primal LP]: max deviation {worst:.1e};"
          f" delta asymmetric: {not np.allclose(delta, delta.T)}")
    # also Kantorovich duality over the vertices (the form used everywhere)
    wd = 0.0
    for _ in range(300):
        j = int(rng.integers(2))
        s = sites[j]
        P1, P2 = rng.dirichlet(np.ones(s.q)), rng.dirichlet(np.ones(s.q))
        wd = max(wd, abs(transport(s, P1, P2) - np.max(s.V @ (P1 - P2))))
    print(f"    Kantorovich: primal LP against max over the vertices of L of E_P' phi - E_P phi, 300 random pairs: {wd:.1e}")
    # ---------------------------------------------------------------- (2), (3), (4), (5)
    J = np.array([-np.log(pi[o].sum()) for o in orb_list])
    Vn = np.array([min(J[b_] + delta[b_, a_] for b_ in range(n_orb)) for a_ in range(n_orb)])      # V_n(P) = min_P' [J_P' + delta(P', P)]
    psiH = -Vn[orb_of]
    print(f"    flat-histogram instance of the lattice psi_H = -V_n(P_x) in the class: {in_class(psiH)};"
          f" its transpose-built variant min_P'[J_P' + delta(P, P')] in the class: "
          f"{in_class(-np.array([min(J[b_] + delta[a_, b_] for b_ in range(n_orb)) for a_ in range(n_orb)])[orb_of])}")
    muH = pi * np.exp(-psiH)
    ZH = muH.sum()
    muH /= ZH
    print(f"    Z_H = {ZH:.4f} (1 <= Z_H <= N_orb = {n_orb})")
    v_dip = v_min = v_tail = v_tail_T = n_tail = v_q_class = v_q_dens = v_q_lev = v_f2 = 0
    worst_dip = 0.0
    for rep in range(400):
        psi0 = random_member()
        assert in_class(psi0)
        # (2) deepest dip on a random set
        mask = rng.random(N) < rng.choice([0.1, 0.3, 0.6])
        if mask.all() or not mask.any():
            continue
        out = ~mask
        dip = psi0.copy()
        dip[mask] = np.max(psi0[out][:, None] - D[np.ix_(out, mask)], axis=0)           # max_{y notin D} [psi0(y) - d(y, x)]
        v_dip += (not in_class(dip))
        slack = D - psi0[:, None] + psi0[None, :]                                       # slack[y, x] = d(y,x) - psi0(y) + psi0(x)
        mu0 = pi * np.exp(-psi0)
        mu0 /= mu0.sum()
        Phi = float(np.sum(mu0[mask] * (np.exp(np.min(slack[np.ix_(out, mask)], axis=0)) - 1)))
        worst_dip = max(worst_dip, abs(A_of(dip) / A_of(psi0) - 1 - Phi))
        # minimality: any member that agrees with psi0 off D is >= dip
        other = random_member()
        cand = np.where(mask, np.maximum(dip, np.minimum(other, psi0)), psi0)
        if in_class(cand):
            v_min += bool(np.any(cand < dip - 1e-9))
        # (3) fibre averages: outer block = sites 0 and 2 (one of each type), inner = sites 1 and 3
        outer_pts = list(itertools.product(range(3), range(2)))
        Wf = {}
        for (a0, a2) in outer_pts:
            tot = 0.0
            for b1 in range(3):
                for b3 in range(2):
                    k = X.index((a0, b1, a2, b3))
                    tot += A.pi[b1] * B.pi[b3] * np.exp(-psi0[k])
            Wf[(a0, a2)] = tot
        for p1 in outer_pts:
            for p2 in outer_pts:
                do = A.d[p1[0], p2[0]] + B.d[p1[1], p2[1]]
                # (-ln W)(p1) - (-ln W)(p2) <= d_o(p1, p2)
                v_f2 += (np.log(Wf[p2]) - np.log(Wf[p1]) > do + 1e-9)
        # (4) tail lemma relative to the reference H, for psi := psi0 (any member), all levels
        w_hat = np.exp(-psi0) / np.exp(-psiH)
        sref = D - psiH[:, None] + psiH[None, :]                                        # s_ref[y, x] = d(y,x) - psiH(y) + psiH(x)
        for s_level in np.unique(w_hat)[:-1]:
            Dset = w_hat > s_level
            oth = ~Dset
            lhs = float(np.sum(muH[Dset] * (w_hat[Dset] - s_level)))
            rhs = s_level * float(np.sum(muH[Dset] * (np.exp(np.min(sref[np.ix_(oth, Dset)], axis=0)) - 1)))
            rhs_T = s_level * float(np.sum(muH[Dset] * (np.exp(np.min(sref.T[np.ix_(oth, Dset)], axis=0)) - 1)))
            n_tail += 1
            v_tail += (lhs > rhs * (1 + 1e-9) + 1e-12)
            v_tail_T += (lhs > rhs_T * (1 + 1e-9) + 1e-12)
        # (5) orbit-wise quantile truncation
        qq = rng.choice([0.1, 0.25, 0.5])
        w = np.exp(-psi0)
        tlev = np.zeros(n_orb)
        for a_, o in enumerate(orb_list):
            vals = np.unique(w[o])
            ok = [tau for tau in vals if np.mean(w[o] > tau) <= qq]
            tlev[a_] = min(ok)
        trunc = np.maximum(psi0, -np.log(tlev[orb_of]))
        # compare with a tolerance: w = t_P exactly gives -ln(exp(-psi0)) != psi0 by one ulp (my first version counted these
        # as changed points and reported 330 spurious 'violations')
        dens = max(np.mean((trunc > psi0 + 1e-12)[o]) for o in orb_list)
        v_q_class += (not in_class(trunc))
        v_q_dens += (dens > qq + 1e-12)
        # the levels themselves: t_{P_y} <= t_{P_x} e^{d(x,y)}  for all x, y
        lev = tlev[orb_of]
        v_q_lev += bool(np.any(lev[None, :] > lev[:, None] * np.exp(D) * (1 + 1e-12)))
    print(f"(2) deepest dips: not in the class {v_dip}; dip formula max error {worst_dip:.1e}; minimality violations {v_min}")
    print(f"(3) fibre averages (-ln W in the class of the outer block): violations {v_f2}")
    print(f"(4) tail lemma relative to H: {n_tail} levels, violations {v_tail};  with the TRANSPOSED slack: {v_tail_T} violations")
    print(f"(5) truncation at orbit-wise q-quantiles: levels not admissible {v_q_lev}; truncation not in the class {v_q_class};"
          f" changed on orbit density > q {v_q_dens}")
    # ---------------------------------------------------------------- (6)
    v6 = 0
    for rep in range(300):
        # invariant instance g(P): admissible iff g(P) - g(P') <= delta(P, P'); build one as a lower envelope
        c = rng.uniform(0, 5, size=n_orb)
        g = np.array([min(c[b_] + delta[a_, b_] for b_ in range(n_orb)) for a_ in range(n_orb)])
        psig = g[orb_of]
        if not in_class(psig):
            v6 += 1
            continue
        mask = rng.random(N) < rng.choice([0.1, 0.3, 0.6])
        if mask.all() or not mask.any():
            continue
        out = ~mask
        def phi_plus(psi):
            mu = pi * np.exp(-psi)
            Z = mu.sum()
            sl = D - psi[:, None] + psi[None, :]
            return float(np.sum(mu[mask] / Z * np.exp(np.min(sl[np.ix_(out, mask)], axis=0)))), Z
        Lam = -g + np.min(J + g)
        Zg = float(np.sum(np.exp(-(J - Lam))))
        ZHn = float(np.sum(np.exp(-(J - Vn))))
        pg, _ = phi_plus(psig)
        pH, _ = phi_plus(psiH)
        v6 += (Zg * pg > ZHn * pH * (1 + 1e-9)) + bool(np.any(Lam > Vn + 1e-9))
    print(f"(6) Z_g Phi_g^+(D) <= Z_H Phi_H^+(D) and Lambda_g <= V_n on 300 random invariant instances and sets: violations {v6}")
    # ---------------------------------------------------------------- (7)
    v7 = 0
    worst_ratio = 0.0
    for rep in range(40):
        gam = [rng.dirichlet(np.ones(len(s.V))) @ s.V for s in sites]           # gamma_j in L_j
        psig = np.array([sum(gam[tindex[i]][x[i]] for i in range(n)) for x in X])
        assert in_class(psig)
        mug = pi * np.exp(-psig)
        mug /= mug.sum()
        t = rng.uniform(0.15, 0.9)
        r = rng.uniform(0.05, 1.0)
        Ms, sig, rho = [], [], []
        for j, s in enumerate(sites):
            pg = gibbs(s.pi, gam[j])[0]
            K = np.exp(t * (s.logW - np.log(pg)[None, :])).T
            val, M = game_value(K)
            Ms.append(M)
            rho.append(val)
            sig.append(-(s.logW - np.log(pg)[None, :]))       # sigma_phi(a) = phi~(a) - gamma~(a) = -ln(pi_phi(a)/pi_gamma(a))
        prob = np.zeros(N)
        for labels in itertools.product(*[range(len(sites[tindex[i]].V)) for i in range(n)]):
            wgt = np.prod([Ms[tindex[i]][labels[i]] for i in range(n)])
            if wgt == 0:
                continue
            Phi = np.array([sum(sig[tindex[i]][labels[i]][x[i]] for i in range(n)) for x in X])
            alt = psig - np.maximum(r - Phi, 0.0)
            if not in_class(alt):
                v7 += 1
            if np.log(A_of(alt)) - np.log(A_of(psig)) < r - 1e-9:
                v7 += 1
            if abs(float(mug @ np.exp(-Phi)) - 1) > 1e-9:
                v7 += 1
            prob += wgt * (Phi < r)
        bound = np.exp(t * r) * np.prod([rho[tindex[i]] for i in range(n)])
        worst_ratio = max(worst_ratio, prob.max() / bound)
        v7 += (prob.max() > bound * (1 + 1e-9))
    print(f"(7) generalised dips with independent vertex labels, 40 random (gamma, t, r): violations {v7};"
          f" largest [max_x P(x in support)] / [e^(tr) prod rho^(n_j)] = {worst_ratio:.4f} (must be <= 1)")
    print(f"[{time.time()-t0:.1f} s]")
