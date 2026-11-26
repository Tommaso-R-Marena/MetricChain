#!/usr/bin/env python3
"""Referee's finite checks for N_REPORT -- own code, nothing imported from the workstream.

 F-A  Lemma N.0 on random finite quasi-metric spaces: the enumerated functions are tail functions of the envelope
      class, are attained by dips, and are NOT valid at q = 1 unless Xi(1) = +infinity
 F-B  Q_4, all 65 534 subsets: exact tail functions against Harper's E_r, T_k at ball sizes; the largest ratio of
      Harper's step function to the exact function between ball sizes (N_REPORT 2.5 (R3))
 F-C  Theorem N4: the class-relative influence of Bernoulli(p)^k against Bernoulli(p')^k over u-Lipschitz fibres:
      formula, attainment, and no violation by random members; the slope of -ln V on a small dependent instance
 F-D  the nearest-neighbour chain of section 4(f): the one-sided slack u + g(v^(k)), attainment by the uniform field
 F-E  Proposition N2 (base bracket) on (R, N(0,1)), V = e^{-psi} with psi random L-Lipschitz, exact A: coverage, ratio
 F-F  Proposition N7(a): the identity for the cube's and the Gaussian profile; failure for the transport profile
 F-G  Proposition N8(a) on random splits of two-kind families
 F-H  Proposition N10(b), qualifier: outer points against queries when rung 0 may use the reference query only
"""
import itertools
import math
import sys
import time

import numpy as np
from scipy import special, stats

INF = float("inf")
bad = 0
rng = np.random.default_rng(11)


def popcount(x):
    return bin(x).count("1")


# ------------------------------------------------------------------------------------------------------------------
def FA():
    global bad
    print("F-A  Lemma N.0 on random finite spaces (7 points, random quasi-metric = shortest-path closure, random mu)")
    worstU, worstL, att = 0.0, INF, 0.0
    viol_q1 = 0
    for trial in range(12):
        n = 7
        d = rng.uniform(0.2, 3.0, (n, n))
        np.fill_diagonal(d, 0.0)
        for k_ in range(n):                      # Floyd-Warshall: triangle inequality, not symmetric
            d = np.minimum(d, d[:, [k_]] + d[[k_], :])
        mu = rng.dirichlet(np.ones(n))
        # rho(x, z) = d[x, z];  class: V(x) <= V(z) e^{rho(x,z)}
        subsets = range(1, 2 ** n - 1)
        F, G, meas = {}, {}, {}
        for D in range(0, 2 ** n):
            ins = [i for i in range(n) if D >> i & 1]
            outs = [i for i in range(n) if not D >> i & 1]
            meas[D] = sum(mu[i] for i in ins)
            if outs and ins:
                F[D] = sum(mu[x] * math.expm1(min(d[x, z] for z in outs)) for x in ins)
            if ins:
                G[D] = sum(mu[x] * math.exp(-min(d[y, x] for y in ins)) for x in range(n))

        def Xi(q):
            if q >= 1 - 1e-15:
                return INF
            c = [F[D] for D in F if meas[D] <= q + 1e-15]
            return max(c) if c else 0.0

        def Xi_literal(q):                       # the formula of Lemma N.0 read literally (sup over D != X)
            c = [F[D] for D in F if meas[D] <= q + 1e-15]
            return max(c) if c else 0.0

        def Th(p):
            return min(G[D] for D in G if meas[D] >= p - 1e-15)

        # random members: V = exp(-psi), psi(x) = max_i (c_i - d[i... ]) forms; member iff V(x) <= V(z) e^{d[x,z]}
        for rep in range(60):
            kind = rep % 3
            c = rng.normal(0, 2.0, n)
            if kind == 0:      # lnV(x) = min_z (c_z + d[x,z])   -> lnV(x) - lnV(z) <= d[x,z]
                lnV = np.array([min(c[z] + d[x, z] for z in range(n)) for x in range(n)])
            elif kind == 1:    # lnV(x) = max_y (c_y - d[y,x])
                lnV = np.array([max(c[y] - d[y, x] for y in range(n)) for x in range(n)])
            else:
                a_ = np.array([min(c[z] + d[x, z] for z in range(n)) for x in range(n)])
                c2 = rng.normal(0, 2.0, n)
                b_ = np.array([max(c2[y] - d[y, x] for y in range(n)) for x in range(n)])
                lnV = np.maximum(a_, b_)
            assert all(lnV[x] - lnV[z] <= d[x, z] + 1e-12 for x in range(n) for z in range(n))
            V = np.exp(lnV)
            for s in list(V) + list(V * 0.999) + list(V * 1.001) + [V.min() * 0.5]:
                pgt = float(mu[V > s].sum())
                pge = float(mu[V >= s].sum())
                exc = float((mu * np.maximum(V - s, 0)).sum())
                emin = float((mu * np.minimum(V, s)).sum())
                if pgt > 0:
                    x = Xi(pgt)
                    if x < INF:
                        worstU = max(worstU, exc / (s * x) if x > 0 else INF)
                    xl = Xi_literal(pgt)
                    if pgt >= 1 - 1e-15 and exc > s * xl * (1 + 1e-12):
                        viol_q1 += 1
                if pge > 0:
                    worstL = min(worstL, emin / (s * Th(pge)))
        # attainment by dips
        for D in list(F)[::7]:
            outs = [i for i in range(n) if not D >> i & 1]
            V = np.array([math.exp(min(d[x, z] for z in outs)) if D >> x & 1 else 1.0 for x in range(n)])
            assert all(V[x] <= V[z] * math.exp(d[x, z]) * (1 + 1e-12) for x in range(n) for z in range(n))
            att = max(att, abs(float((mu * np.maximum(V - 1, 0)).sum()) - F[D]))
    print("     largest E(V-s)+/(s Xi(p(s))) = %.10f; smallest E min(V,s)/(s Theta(pbar(s))) = %.10f; dips attain F(D) to %.1e"
          % (worstU, worstL, att))
    print("     with the formula read literally at q = 1 (sup over D != X, finite): (TU) violated in %d cases (s below min V)" % viol_q1)
    bad += (worstU > 1 + 1e-9) + (worstL < 1 - 1e-9) + (att > 1e-12)


# ------------------------------------------------------------------------------------------------------------------
def FB():
    global bad
    print("F-B  Q_4, all subsets: exact tail functions against Harper")
    m = 4
    N = 16
    dist = [[popcount(x ^ y) for y in range(N)] for x in range(N)]
    for u in (0.5, 1.0, 2.0):
        ball = [sum(math.comb(m, j) for j in range(r + 1)) for r in range(m + 1)]
        E = [sum(math.comb(m, j) * math.expm1(u * (r + 1 - j)) for j in range(r + 1)) for r in range(m + 1)]
        T = [sum(math.comb(m, j) * math.exp(-u * max(j - k, 0)) for j in range(m + 1)) for k in range(m + 1)]
        bestF = [0.0] * (N + 1)      # by cardinality: max of sum_{x in D}(e^{u dist(x, D^c)} - 1)
        bestG = [INF] * (N + 1)      # min of sum_x e^{-u dist(x, S)}
        for D in range(1, 2 ** N):
            ins = [x for x in range(N) if D >> x & 1]
            c = len(ins)
            if c < N:
                outs = [x for x in range(N) if not D >> x & 1]
                f = sum(math.expm1(u * min(dist[x][z] for z in outs)) for x in ins)
                bestF[c] = max(bestF[c], f)
            g = sum(math.exp(-u * min(dist[x][y] for y in ins)) for x in range(N))
            bestG[c] = min(bestG[c], g)
        exactXi = [max(bestF[1:c + 1]) for c in range(1, N)]            # |D| <= c
        exactTh = [min(bestG[c:]) for c in range(1, N + 1)]            # |S| >= c
        okb = all(abs(exactXi[ball[r] - 1] / E[r] - 1) < 1e-12 for r in range(m)) and all(abs(exactTh[ball[k] - 1] / T[k] - 1) < 1e-12 for k in range(m + 1))
        worst_step = 0.0
        valid = True
        for c in range(1, N):
            r = next(r for r in range(m + 1) if ball[r] >= c)
            if r <= m - 1:
                worst_step = max(worst_step, E[r] / exactXi[c - 1])
                valid &= E[r] >= exactXi[c - 1] * (1 - 1e-12)
        for c in range(1, N + 1):
            k = max(k for k in range(m + 1) if ball[k] <= max(1, c))
            valid &= T[k] <= exactTh[c - 1] * (1 + 1e-12)
        print("     u = %-4g exact = Harper at ball sizes: %s; Harper's step functions valid at all cardinalities: %s; largest step/exact (upper) %.3f"
              % (u, okb, valid, worst_step))
        bad += (not okb) + (not valid)


# ------------------------------------------------------------------------------------------------------------------
def lipschitz_random(k, u, kind):
    """a random u-Lipschitz function on Q_k (Hamming), as an array of length 2^k"""
    N = 1 << k
    pts = np.arange(N)
    if kind == 0:        # additive
        c = rng.uniform(-u, u, k)
        return np.array([sum(c[i] for i in range(k) if x >> i & 1) for x in pts])
    if kind == 1:        # cone / dip mixtures
        z = rng.integers(0, N, 3)
        c = rng.normal(0, u * k / 2, 3)
        return np.array([max(c[i] - u * popcount(x ^ int(z[i])) for i in range(3)) for x in pts])
    if kind == 2:
        z = rng.integers(0, N, 3)
        c = rng.normal(0, u * k / 2, 3)
        return np.array([min(c[i] + u * popcount(x ^ int(z[i])) for i in range(3)) for x in pts])
    f = rng.normal(0, u * k, N)          # McShane extension of random data: Lipschitz envelope
    return np.array([min(f[y] + u * popcount(x ^ y) for y in pts) for x in pts])


def FC():
    global bad
    print("F-C  Theorem N4: class-relative influence of product Bernoulli laws over u-Lipschitz fibres")
    worst = -INF
    att = 0.0
    for trial in range(40):
        k = int(rng.integers(2, 6))
        u = float(rng.uniform(0.2, 2.5))
        p, pp = rng.uniform(0.02, 0.98, 2)
        N = 1 << k
        wt = np.array([popcount(x) for x in range(N)])
        P = p ** wt * (1 - p) ** (k - wt)
        PP = pp ** wt * (1 - pp) ** (k - wt)
        iota = k * max(math.log((1 + p * math.expm1(s * u)) / (1 + pp * math.expm1(s * u))) for s in (1, -1))
        for s in (1, -1):                # the uniform fields f = -s u |b|
            att = max(att, math.log((P * np.exp(s * u * wt)).sum() / (PP * np.exp(s * u * wt)).sum()) - iota) if True else att
        for rep in range(200):
            f = lipschitz_random(k, u, rep % 4)
            w = np.exp(-(f - f.min()))
            worst = max(worst, math.log((P * w).sum() / (PP * w).sum()) - iota)
    print("     40 triples (k, u, p, p'), 8 000 random fibres: largest ln[E_p w / E_p' w] - iota = %.3e (must be <= 0);"
          " uniform field: %.1e (attained)" % (worst, att))
    bad += (worst > 1e-12) + (abs(att) > 1e-12)
    # the slope of -ln V on a small dependent instance: outer Q_3, inner Q_3, p(a) depends on |a|
    m, k = 3, 3
    worstslope, attained = -INF, -INF
    for trial in range(30):
        u = float(rng.uniform(0.3, 1.5))
        pa = rng.uniform(0.05, 0.95, m + 1)                # p as a function of |a|
        n = m + k
        iota1 = max(k * max(math.log((1 + pa[w] * math.expm1(s * u)) / (1 + pa[w2] * math.expm1(s * u))) for s in (1, -1))
                    for w in range(m + 1) for w2 in (w - 1, w + 1) if 0 <= w2 <= m)
        for rep in range(40):
            psi = lipschitz_random(n, u, rep % 4) if rep < 36 else None
            if psi is None:                               # additive extremal candidates: -+u on outer letters, uniform field on b
                s_o = rng.choice([-1, 1], m)
                s_b = rng.choice([-1, 1])
                psi = np.array([sum(s_o[i] * u for i in range(m) if x >> i & 1) + s_b * u * popcount(x >> m) for x in range(1 << n)])
            V = np.zeros(1 << m)
            for a in range(1 << m):
                p = pa[popcount(a)]
                for b in range(1 << k):
                    wb = popcount(b)
                    V[a] += p ** wb * (1 - p) ** (k - wb) * math.exp(-psi[a | (b << m)])
            for a in range(1 << m):
                for i in range(m):
                    a2 = a ^ (1 << i)
                    w, w2 = popcount(a), popcount(a2)
                    io = k * max(math.log((1 + pa[w] * math.expm1(s * u)) / (1 + pa[w2] * math.expm1(s * u))) for s in (1, -1))
                    sl = math.log(V[a] / V[a2]) - (u + io)
                    worstslope = max(worstslope, sl)
                    if rep >= 36:
                        attained = max(attained, sl)
    print("     outer Q_3 x inner Q_3, p = p(|a|): largest ln[V(a)/V(a')] - (u + iota(a,a')) over 1 200 members = %.3e (must be <= 0);"
          " additive candidates reach %.1e" % (worstslope, attained))
    bad += worstslope > 1e-12


# ------------------------------------------------------------------------------------------------------------------
def FD():
    global bad
    print("F-D  nearest-neighbour chain (symmetric binary, flip p): outer sites 1..c, inner sites c+1..c+k")
    c, k = 3, 5
    n = c + k
    for (p, u) in [(0.3, 1.0), (0.1, 1.0), (0.2, 0.5), (0.4, 2.0)]:
        g = lambda v: math.log(((1 - p) * math.exp(v) + p) / (p * math.exp(v) + 1 - p))
        v = u
        for _ in range(k - 1):
            v = u + g(v)
        vb = u + g(v)
        # conditional law of the inner block given a_c
        def condprob(ac, b):
            pr, prev = 1.0, ac
            for i in range(k):
                bi = b >> i & 1
                pr *= (1 - p) if bi == prev else p
                prev = bi
            return pr
        cp = [[condprob(ac, b) for b in range(1 << k)] for ac in (0, 1)]
        worst_b, worst_nb, att = -INF, -INF, -INF
        for rep in range(44):
            if rep < 40:
                psi = lipschitz_random(n, u, rep % 4)
            else:                                        # uniform fields
                sgn = 1 if rep % 2 else -1
                psi = np.array([sgn * u * popcount(x) for x in range(1 << n)])
            V = np.zeros(1 << c)
            for a in range(1 << c):
                ac = a >> (c - 1) & 1
                V[a] = sum(cp[ac][b] * math.exp(-psi[a | (b << c)]) for b in range(1 << k))
            for a in range(1 << c):
                for i in range(c):
                    sl = abs(math.log(V[a] / V[a ^ (1 << i)]))
                    if i == c - 1:
                        worst_b = max(worst_b, sl)
                        if rep >= 40:
                            att = max(att, sl)
                    else:
                        worst_nb = max(worst_nb, sl)
        print("     p=%.1f u=%.1f: slope in a non-boundary letter <= %.6f (u = %.1f); in the boundary letter <= %.6f, formula u+g(v^(k)) = %.6f, uniform field %.6f"
              % (p, u, worst_nb, u, worst_b, vb, att))
        bad += (worst_nb > u + 1e-9) + (worst_b > vb + 1e-9) + (abs(att - vb) > 1e-9)


# ------------------------------------------------------------------------------------------------------------------
def FE():
    global bad
    print("F-E  Proposition N2 on (R, N(0,1)): V = e^{-psi}, psi piecewise linear with slopes +-L; exact A; Xi_L, Theta_L")
    Phi, Phinv = stats.norm.cdf, stats.norm.ppf

    def Xi(L, q):
        t = -Phinv(q)
        return math.exp(L * L / 2 - L * t + special.log_ndtr(L - t)) - q

    def Th(L, p_):
        c_ = Phinv(p_)
        return max(p_, p_ + math.exp(L * c_ + L * L / 2 + special.log_ndtr(-c_ - L)))

    tot, miss, ratio_bad = 0, 0, 0
    for (L, kind) in [(1.0, 'lin'), (2.0, 'lin'), (2.0, 'abs'), (1.5, 'tent')]:
        if kind == 'lin':                      # psi = -L x: A = e^{L^2/2}
            f = lambda x: L * x
            A = math.exp(L * L / 2)
        elif kind == 'abs':                    # psi = -L|x|: A = 2 e^{L^2/2} Phi(L)
            f = lambda x: L * np.abs(x)
            A = 2 * math.exp(L * L / 2) * Phi(L)
        else:                                  # psi = L|x|: A = 2 e^{L^2/2} Phi(-L)
            f = lambda x: -L * np.abs(x)
            A = 2 * math.exp(L * L / 2) * Phi(-L)
        for (eta, K, M) in [(0.5, 60, 4000), (0.25, 200, 20000), (0.5, 40, 200000)]:
            qp, qm = K / ((1 - eta) * M), K / ((1 + eta) * M)
            pfail = 4 * math.exp(-eta ** 2 * K / (3 * (1 + eta)))
            bound = (1 + eta) / (1 - eta) * (1 + Xi(L, qp) / Th(L, qm))
            nrep = 300
            m_ = r_ = 0
            for _ in range(nrep):
                v1 = np.exp(f(rng.standard_normal(M)))
                that = np.partition(v1, M - K)[M - K]
                v2 = np.exp(f(rng.standard_normal(M)))
                Ahat = np.minimum(v2, that).mean()
                Lb = Ahat / (1 + eta)
                Ub = Ahat / (1 - eta) + that * Xi(L, qp)
                m_ += not (Lb <= A <= Ub)
                r_ += Ub / Lb > bound * (1 + 1e-12)
            tot += nrep
            miss += m_
            ratio_bad += r_
            print("     L=%.1f %-4s eta=%.2f K=%d M=%d: misses %d/%d (bound on the failure probability %.3g), ratio bound %.3f exceeded %d times"
                  % (L, kind, eta, K, M, m_, nrep, min(pfail, 1.0), bound, r_))
            bad += (m_ / nrep > min(pfail, 1.0) + 0.05)
    print("     total: %d brackets, %d misses, %d above the ratio bound" % (tot, miss, ratio_bad))


# ------------------------------------------------------------------------------------------------------------------
def FF():
    global bad
    print("F-F  Proposition N7(a): theta_na(e + theta_hint(e)) = theta_hint(e)")

    def check(wfun, theta_bar, name):
        th = np.linspace(0, theta_bar, 200001)
        w = wfun(th)
        x = w + th
        mono = bool(np.all(np.diff(x) <= 1e-12))
        # theta_hint = w^{-1} (w decreasing where (P1) holds); theta_na(X) = min{theta : x(theta) <= X}
        worst = 0.0
        E = w[0]
        for e in np.linspace(0.02 * E, 0.98 * E, 49):
            i = int(np.argmax(w <= e))                 # first index with w <= e
            thh = th[i]
            X = e + thh
            jj = int(np.argmax(x <= X + 1e-12))
            worst = max(worst, abs(th[jj] - thh))
        print("     %-34s w + id nonincreasing: %-5s  largest |theta_na(e+theta_hint(e)) - theta_hint(e)| = %.4f" % (name, mono, worst))
        return mono, worst

    c = 1.3
    mono, worst = check(lambda t: np.where(t <= c * c / 2, c * c / 2 - c * np.sqrt(2 * t), -t), 2.0, "Gaussian profile, c = 1.3")
    bad += (not mono) + (worst > 1e-3)
    u = 1.0
    pu = 1 / (1 + math.exp(u))
    # cube: theta = KL(rho||1/2), w = u rho + ln((1+e^-u)/2) for rho >= p_u; w = -theta ... param by rho in [p_u, 1/2]
    rho = np.linspace(pu, 0.5, 200001)[::-1]                    # theta increasing <=> rho decreasing
    th_c = np.log(2) + rho * np.log(rho) + (1 - rho) * np.log(1 - rho)
    w_c = u * rho + math.log((1 + math.exp(-u)) / 2)
    xc = w_c + th_c
    worst = 0.0
    for e in np.linspace(0.02 * w_c[0], 0.98 * w_c[0], 49):
        i = int(np.argmax(w_c <= e))
        X = e + th_c[i]
        jj = int(np.argmax(xc <= X + 1e-12))
        worst = max(worst, abs(th_c[jj] - th_c[i]))
    print("     %-34s w + id nonincreasing: %-5s  largest deviation = %.4f   (E = %.5f, a = %.5f, h = %.5f)"
          % ("cube profile, u = 1", bool(np.all(np.diff(xc) <= 1e-12)), worst, w_c[0], th_c[-1], th_c[int(np.argmax(w_c <= 0))]))
    bad += worst > 1e-3
    mono, worst = check(lambda t: np.where(t <= u * u / 8, u * u / 8, u * np.sqrt(t / 2) - t), math.log(2), "transport profile, u = 1 (N_REPORT 3.1)")
    print("     (for the transport profile the hypothesis (P1) fails and so does the identity, as the report says)")
    bad += mono or worst < 1e-3


# ------------------------------------------------------------------------------------------------------------------
def FG():
    global bad
    print("F-G  Proposition N8(a): min(gamma0, mu) + Rhat_beta(gamma0) >= Rhat_nu(G) on random splits, two kinds of binary sites")
    Lam = lambda v: math.log(2) - np.log1p(np.exp(-v))
    ts = np.linspace(0, 1, 4001)
    worst = INF
    for trial in range(400):
        u1, u2 = rng.uniform(0.2, 4.0, 2)
        nu = rng.dirichlet([1, 1])
        J1 = Lam(ts * u1) - ts * Lam(u1)
        J2 = Lam(ts * u2) - ts * Lam(u2)
        al = nu * rng.uniform(0, 1, 2)
        be = nu - al
        Jn, Ja, Jb = nu[0] * J1 + nu[1] * J2, al[0] * J1 + al[1] * J2, be[0] * J1 + be[1] * J2
        Rhat = lambda Jv, e: float(np.max(Jv - ts * e))
        Tna = lambda Jv, x: float(np.max((Jv[:-1] - ts[:-1] * x) / (1 - ts[:-1])))
        G = rng.uniform(0.01, 1.0) * float(np.max(Jn[1:] / ts[1:]))
        B = rng.uniform(0.01, 0.99) * G
        mu_ = Tna(Ja, G - B)
        g0 = max(B, mu_)
        worst = min(worst, min(g0, mu_) + Rhat(Jb, g0) - Rhat(Jn, G))
    print("     400 random (slopes, composition, split, G, B): smallest margin %.3e (must be >= 0 up to the grid in t)" % worst)
    bad += worst < -1e-6


# ------------------------------------------------------------------------------------------------------------------
def FH():
    global bad
    print("F-H  outer points against queries on V = e^{La}, a ~ N(0,1), n_i = 0, when rung 0 uses the reference query only")
    print("     rung 0: [e^{-L|a|}, e^{L|a|}] without a query if |a| <= 6 (x_0 = 12 L), else one query; rung 1: one query, exact value")
    Phi, Phinv = stats.norm.cdf, stats.norm.ppf

    def Xi(L, q):
        if q >= 1:
            return INF
        t = -Phinv(q)
        return math.exp(L * L / 2 - L * t + special.log_ndtr(L - t)) - q

    def ThB(L, p_):
        c_ = Phinv(p_)
        return max(p_, p_ + math.exp(L * c_ + L * L / 2 + special.log_ndtr(-c_ - L)))

    for (L, theta) in [(3.0, 2.0), (3.5, 2.0), (4.0, 20.0), (4.0, 3.0)]:
        lam, eta, etap, nu1, b, delta = 0.5, 0.5, 0.5, max(1.0, 2 * L / theta), 0.25, 0.05
        ceta = (1 - eta) / (1 + eta)
        A = math.exp(L * L / 2)
        ell0, u0 = 2 * A * Phi(-L), 2 * A * Phi(L)
        qs = np.exp(np.linspace(math.log(1e-14), 0, 3001))[:-1]
        pi_star = None
        for q in qs:
            if Xi(L, q) <= theta * nu1 * q and Xi(L, q) <= theta * ThB(L, ceta * q):
                pi_star = q
            else:
                break
        pi_star *= 0.999
        J = math.floor((math.log(u0 / ell0) + b + lam + math.log((1 + eta) / ((1 - eta) * pi_star))) / lam)
        nu0 = max((J + 1) * math.expm1(lam) / etap, nu1) / (1 - eta)
        m_max = math.ceil(math.log2(2 * (1 + eta) * math.exp(lam) * nu0 / ((1 - eta) * pi_star)))
        K = math.ceil(3 * (1 + eta) / eta ** 2 * math.log(2 * (J + 1) * (m_max + 1) * 3 / delta))
        nu = K * nu0
        x_out = math.log(1 + math.exp(b) * (math.exp(lam) * (1 + eta) / (1 - eta) + etap + theta))
        bound = 2 * K / (1 + eta) * math.exp((L - math.sqrt(2 * x_out)) ** 2 / 2) if x_out < L * L / 2 else float('nan')
        out = []
        for rep in range(3):
            a = np.empty(0); Lo = np.empty(0); Up = np.empty(0); queried = np.empty(0, dtype=bool)
            ell, Sig, usum, j, Mmax, done = ell0, 0.0, 0.0, 0, 0, False
            while not done and j <= J:
                sj = ell0 * math.exp(j * lam)
                Mneg = nu * sj / (ell * math.exp(b))
                M = K
                while True:
                    if M > 4e7:
                        done = True
                        Lret = Uret = float('nan')
                        break
                    if len(a) < M:
                        na = rng.standard_normal(M - len(a))
                        far = np.abs(na) > 6
                        a = np.concatenate([a, na])
                        Lo = np.concatenate([Lo, np.where(far, np.exp(L * na), np.exp(-L * np.abs(na)))])
                        Up = np.concatenate([Up, np.where(far, np.exp(L * na), np.exp(L * np.abs(na)))])
                        queried = np.concatenate([queried, far])
                    Mmax = max(Mmax, M)
                    idx = np.nonzero((Up[:M] > sj) & (Lo[:M] <= sj * math.exp(-b)))[0]
                    if len(idx):
                        Lo[idx] = Up[idx] = np.exp(L * a[idx])
                        queried[idx] = True
                    Nh = int(np.count_nonzero(Up[:M] > sj))
                    q = min(1.0, max(Nh, K) / ((1 - eta) * M))
                    pop = Nh >= K
                    if pop:
                        plow = Nh / ((1 + eta) * M)
                        ell = max(ell, sj * math.exp(-b) * ThB(L, plow))
                    tl = sj * Xi(L, q)
                    if tl <= theta * math.exp(b) * ell:
                        Lret = max(ell, Sig + ((1 - math.exp(-lam)) * math.exp(-b) * sj * plow if pop else 0.0))
                        Uret = ell0 + usum + tl
                        done = True
                        break
                    if pop:
                        Sig += (1 - math.exp(-lam)) * math.exp(-b) * sj * plow
                        usum += sj * math.expm1(lam) * q
                        break
                    if M >= Mneg:
                        usum += sj * math.expm1(lam) * q
                        break
                    M *= 2
                j += 1
            out.append((Mmax, int(queried.sum()), bool(Lret <= A <= Uret), Uret / Lret <= math.exp(x_out) * (1 + 1e-12)))
        print("     L=%.1f theta=%g nu1=%.1f: K=%d x_out=%.3f, N10(b) bound on M_max %.4g | runs (M_max, queries, valid, width ok): %s"
              % (L, theta, nu1, K, x_out, bound, "  ".join(str(o) for o in out)))
        bad += sum((not o[2]) or (not o[3]) for o in out)


if __name__ == "__main__":
    t0 = time.time()
    which = sys.argv[1:] or ["A", "B", "C", "D", "E", "F", "G", "H"]
    for w in which:
        {"A": FA, "B": FB, "C": FC, "D": FD, "E": FE, "F": FF, "G": FG, "H": FH}[w]()
    print("violations: %d   (%.1f s)" % (bad, time.time() - t0))
    sys.exit(1 if bad else 0)
