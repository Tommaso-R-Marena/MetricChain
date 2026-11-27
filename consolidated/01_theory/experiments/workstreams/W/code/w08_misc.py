"""w08: smaller checks.

 (i)   Lemma T' (inherently typical subsets for a fixed sequence of site types and alphabets of different sizes):
       brute force on a chain with 3 ternary and 3 binary sites, random and structured sets, m = 1, 2, 3, 5;
 (ii)  W6: a binary site with an asymmetric envelope (u1, u2) has the game function of the symmetric site with
       u = (u1 + u2)/2 and the site law tilted by kappa = (u2 - u1)/2 (normal form);
 (iii) is F* concave for binary sites? (second differences on a grid of fields and constants);
 (iv)  the label switch of the triangle site: the two tangency points, e_c, both label structures; for the chain
       mix2: the gap between R^max and the best split of the accuracy (strict near the switch);
 (v)   which site law is hardest for a given envelope? three states, Hamming envelope: h = R^max(0), E, a over a
       grid of site laws (numerical observation behind W7, Proposition W7.3);
 (vi)  the dictionary with channel coding: theta_na(x) = max_rho (E_0(rho) - x)/rho, R(e) = max_rho (E_0(rho) - e)/(1+rho),
       E_0(rho) = rho * C_{1/(1+rho)}; x_na(theta) = E_sp(theta) = max_rho [E_0(rho) - rho theta], checked on the path site.
"""
import itertools
import math
import sys
import time

import numpy as np
from scipy.optimize import brentq, minimize_scalar

from wlib import *
from wsites import *

t00 = time.time()
rng = np.random.default_rng(11)
np.set_printoptions(precision=5, suppress=True, linewidth=160)
which = sys.argv[1] if len(sys.argv) > 1 else "all"

# ------------------------------------------------------------------------------------------------------------
if which in ("all", "i"):
    print("=== (i) Lemma T' by brute force ===")
    sa, sb = asym_site(), Site([0.65, 0.35], [[0, 1.2], [0.4, 0]], "bin-asym")
    seq = [sa, sb, sa, sb, sb, sa]
    typ = [0, 1, 0, 1, 1, 0]
    n = len(seq)
    X = np.array(list(itertools.product(*[range(s.q) for s in seq])), dtype=np.int64)
    lpi = sum(np.log(s.pi)[X[:, i]] for i, s in enumerate(seq))
    pi = np.exp(lpi)
    N = len(X)
    qmax = 3

    def check(mask, m):
        PA = np.where(mask, pi, 0.0)
        PA = PA / PA.sum()
        # conditional laws p_i(. | x^{i-1}) of pi(.|A), labels u_i = rounded-up quantisation
        labels = np.zeros((N, n), dtype=object)
        for i in range(n):
            s = seq[i]
            # group by prefix
            pref = [tuple(x[:i]) for x in X]
            mass = {}
            for k in range(N):
                if PA[k] > 0:
                    key = pref[k]
                    mass.setdefault(key, np.zeros(s.q))[X[k, i]] += PA[k]
            for k in range(N):
                if PA[k] > 0:
                    p = mass[pref[k]]
                    p = p / p.sum()
                    labels[k, i] = (typ[i],) + tuple(int(math.ceil(m * v - 1e-12)) for v in p)
        # joint type of ((label, letter))_i
        jt = {}
        for k in range(N):
            if PA[k] > 0:
                key = tuple(sorted((labels[k, i], int(X[k, i])) for i in range(n)))
                jt.setdefault(key, []).append(k)
        best = max(jt.values(), key=lambda ks: PA[ks].sum())
        At = np.array(best)
        alpha_A = -math.log(pi[mask].sum()) / n
        alpha_At = -math.log(pi[At].sum()) / n
        # alpha = D(P_{X|UT} || pi_T | P_{UT}) from the joint type of the class
        k0 = At[0]
        cnt = {}
        for i in range(n):
            cnt.setdefault(labels[k0, i], np.zeros(seq[i].q))[X[k0, i]] += 1
        alpha = 0.0
        for lab, c in cnt.items():
            s = sa if lab[0] == 0 else sb
            mu = c / c.sum()
            alpha += (c.sum() / n) * sum(mu[a] * math.log(mu[a] / s.pi[a]) for a in range(s.q) if mu[a] > 0)
        # (4): I(X_I; V | U_I, T_I) under pi(.|At) by direct enumeration: = H(X_I | U_I, T_I) - (1/n) H(X^n)
        PAt = pi[At] / pi[At].sum()
        Hn = -float(np.sum(PAt * np.log(PAt)))
        HXU = 0.0
        for lab, c in cnt.items():
            mu = c / c.sum()
            HXU += (c.sum() / n) * (-sum(mu[a] * math.log(mu[a]) for a in range(len(mu)) if mu[a] > 0))
        Icond = HXU - Hn / n
        # identity alpha_At = alpha + I(X_I;V|U_I,T_I) requires D(P_{X^n}||pi) = -ln pi(At) (true) and the chain rule
        ok2 = pi[At].sum() >= pi[mask].sum() / len(jt) - 1e-15
        ok3 = (alpha_A - qmax / m <= alpha + 1e-12) and (alpha <= alpha_At + 1e-12)
        ok4 = abs((alpha_At - alpha) - Icond) < 1e-10 and Icond > -1e-12
        return ok2, ok3, ok4, len(jt), alpha_A, alpha, alpha_At

    fails = [0, 0, 0]
    cnt = 0
    worst_gap = 0.0
    for it in range(120):
        kind = it % 4
        if kind == 0:
            mask = rng.random(N) < rng.choice([0.02, 0.1, 0.4])
        elif kind == 1:                                   # a ball for the envelope around a random point
            c = X[rng.integers(N)]
            dist = sum(seq[i].d[X[:, i], c[i]] for i in range(n))
            mask = dist <= rng.choice([1.0, 2.0, 3.5])
        elif kind == 2:                                   # a joint-type class, thinned
            key = (X[:, [0, 2, 5]] == 1).sum(axis=1) * 10 + (X[:, [1, 3, 4]] == 1).sum(axis=1)
            mask = (key == rng.choice(key)) & (rng.random(N) < 0.7)
        else:                                             # a cylinder
            mask = (X[:, 0] == rng.integers(3)) & (X[:, 3] == rng.integers(2))
        if mask.sum() == 0:
            continue
        for m in (1, 2, 3, 5):
            ok2, ok3, ok4, ncls, aA, al, aAt = check(mask, m)
            fails[0] += not ok2
            fails[1] += not ok3
            fails[2] += not ok4
            worst_gap = max(worst_gap, aA - al)
            cnt += 1
    print(f"  {cnt} cases (sets of four kinds x m = 1, 2, 3, 5) on a chain of 3 ternary + 3 binary sites ({N} points):")
    print(f"  violations of (2) pi(A~) >= pi(A)/#classes: {fails[0]}; of (3) alpha_A - q/m <= alpha <= alpha_A~: {fails[1]};"
          f" of (4) alpha_A~ - alpha = I(X_I; V | U_I, T_I) >= 0: {fails[2]}; largest alpha_A - alpha = {worst_gap:.4f}")

# ------------------------------------------------------------------------------------------------------------
if which in ("all", "ii"):
    print("\n=== (ii) asymmetric binary envelope = symmetric envelope + field ===")
    worst = 0.0
    for p, u1, u2 in ((0.3, 1.5, 0.5), (0.5, 2.0, 0.2), (0.1, 0.4, 1.8), (0.7, 1.0, 0.0)):
        s1 = Site([1 - p, p], [[0, u1], [u2, 0]], "asym-bin")       # gamma(0)-gamma(1) <= u1, gamma(1)-gamma(0) <= u2
        kap = (u2 - u1) / 2
        w = np.array([1 - p, p * math.exp(-kap)])
        s2 = Site(w / w.sum(), [[0, (u1 + u2) / 2], [(u1 + u2) / 2, 0]], "sym-bin")
        for t in np.linspace(0.05, 0.95, 19):
            worst = max(worst, abs(s1.Fstar(t) - s2.Fstar(t)))
        print(f"  p = {p}, (u1, u2) = ({u1}, {u2}): E = {s1.Estar():.6f} / {s2.Estar():.6f}; a = {s1.capacity():.6f} / {s2.capacity():.6f}")
    print(f"  max |F*_asym(t) - F*_sym+field(t)| over 4 sites x 19 values of t: {worst:.1e}")

# ------------------------------------------------------------------------------------------------------------
if which in ("all", "iii"):
    print("\n=== (iii) concavity of F* for binary sites ===")
    ts = np.linspace(0.0, 1.0, 201)
    worst = -np.inf
    arg = None
    for u in (0.3, 1.0, 2.0, 4.0):
        for theta in np.linspace(0.0, 6.0, 25):
            p = 1 / (1 + math.exp(theta))
            s = binary_site(p, u)
            F = np.array([s.Fstar(t) for t in ts])
            d2 = (F[:-2] - 2 * F[1:-1] + F[2:]).max()
            if d2 > worst:
                worst, arg = d2, (u, theta)
    print(f"  100 binary sites (u in {{0.3,1,2,4}}, 25 fields in [0,6]), 201 values of t: largest second difference of F*: {worst:.2e} at (u, theta) = {arg}"
          f"  -> {'concave in all cases' if worst < 1e-9 else 'NOT concave'}")

# ------------------------------------------------------------------------------------------------------------
if which in ("all", "iv"):
    print("\n=== (iv) the label switch of the triangle site ===")
    C = chains()
    for name in ("tri", "mix2"):
        ch = C[name]
        E = ch.E()
        ts, Fs = ch.table(2001)
        d2 = Fs[:-2] - 2 * Fs[1:-1] + Fs[2:]
        kc = int(np.argmax(d2)) + 1
        tc = ts[kc]

        def branch(e, lo, hi):
            res = minimize_scalar(lambda t: -(ch.Fstar(t) - t * e), bounds=(lo, hi), method="bounded", options={"xatol": 1e-11})
            return -res.fun, res.x

        g = lambda e: branch(e, tc, 0.999)[0] - branch(e, 0.001, tc)[0]
        ec = brentq(g, 0.0, 0.5 * E, xtol=1e-12)
        Rp, tp = branch(ec, tc, 0.999)
        Rm, tm = branch(ec, 0.001, tc)
        print(f"  chain {ch.name}: kink of F* at t_c = {tc:.4f} (slope jump {((Fs[kc+1]-Fs[kc]) - (Fs[kc]-Fs[kc-1]))*2000:+.5f});"
              f" the two branches tie at e_c = {ec:.6f} = {ec/E:.4f} E, R^max(e_c) = {Rp:.7f} = {Rm:.7f}")
        print(f"     e < e_c: t* = {tp:.4f}, label weights " + "; ".join(str(np.round(m, 3)) for m in ch.Ms(tp)))
        print(f"     e > e_c: t* = {tm:.4f}, label weights " + "; ".join(str(np.round(m, 3)) for m in ch.Ms(tm)))
        print(f"     gamma* (last type): {np.round(ch.gammas(tp)[-1], 4)} / {np.round(ch.gammas(tm)[-1], 4)};  R^max has a corner: slope {-tp:.4f} -> {-tm:.4f}")
        if name == "tri":
            tri_bridge = (tm, tp, ch.Fstar(tm), ch.Fstar(tp))
    # mix2: R^max against the best split = transform of sum_j lam_j conc(F*_j)
    ch = C["mix2"]
    E = ch.E()
    t1, t2, F1, F2 = tri_bridge
    sb_, st_ = ch.sites
    lb, lt = ch.lam

    def conc_tri(t):
        if t1 < t < t2:
            return F1 + (F2 - F1) * (t - t1) / (t2 - t1)
        return st_.Fstar(t) if 0 < t < 1 else 0.0

    tsf = np.linspace(0.3, 0.46, 3201)
    Fmix = np.array([lb * sb_.Fstar(t) + lt * st_.Fstar(t) for t in tsf])
    Fhull = np.array([lb * sb_.Fstar(t) + lt * conc_tri(t) for t in tsf])
    best = (0.0, None)
    for e in np.linspace(0.19 * E, 0.22 * E, 301):
        r1 = float(np.max(Fmix - tsf * e))
        r2 = float(np.max(Fhull - tsf * e))
        if r2 - r1 > best[0]:
            best = (r2 - r1, e, r1, r2)
    print(f"  chain mix2: bridge of F*_tri: [{t1:.4f}, {t2:.4f}]; largest gap between the best split of the accuracy and R^max:"
          f" {best[0]:.2e} at e = {best[1]:.6f} = {best[1]/E:.4f} E (R^max = {best[2]:.7f}, best split = {best[3]:.7f}, relative {best[0]/best[2]:.1e})")

# ------------------------------------------------------------------------------------------------------------
if which in ("all", "v"):
    print("\n=== (v) which site law is hardest? three states, Hamming envelope ===")
    for u in (1.0, 2.0):
        d = u * (1 - np.eye(3))
        rows = []
        step = 0.05
        for i in range(1, 20):
            for j in range(1, 20 - i):
                p = np.array([i * step, j * step, 1 - (i + j) * step])
                if p[2] < step - 1e-9:
                    continue
                s = Site(p, d)
                ch = Chain([s], [1.0])
                rows.append((ch.R(0.0, nt=101), s.Estar(), s.capacity(), p))
        s = Site(np.ones(3) / 3, d)
        ch = Chain([s], [1.0])
        hu, Eu, au = ch.R(0.0, nt=101), s.Estar(), s.capacity()
        bh = max(rows, key=lambda r: r[0])
        bE = max(rows, key=lambda r: r[1])
        ba = max(rows, key=lambda r: r[2])
        print(f"  u = {u}: uniform law: h = {hu:.6f}, E = {Eu:.6f}, a = {au:.6f};  over {len(rows)} laws on a grid of step {step}:")
        print(f"     largest h = {bh[0]:.6f} at pi = {np.round(bh[3], 3)}; largest E = {bE[1]:.6f} at {np.round(bE[3], 3)}; largest a = {ba[2]:.6f} at {np.round(ba[3], 3)}")
        # pointwise in t: is F*(t; pi) <= F*(t; uniform)?
        worst = -np.inf
        for t in (0.1, 0.3, 0.5, 0.7, 0.9):
            fu = s.Fstar(t)
            for r in rows[:: 3]:
                worst = max(worst, Site(r[3], d).Fstar(t) - fu)
        print(f"     largest F*(t; pi) - F*(t; uniform) over a third of the laws and t in {{.1,.3,.5,.7,.9}}: {worst:+.2e}")

# ------------------------------------------------------------------------------------------------------------
if which in ("all", "vi"):
    print("\n=== (vi) dictionary with channel coding (path site) ===")
    ch = chains()["path"]
    s = ch.sites[0]
    E, a = ch.E(), ch.a()[0]
    E0 = lambda rho: rho * s.Fstar(1 / (1 + rho)) / (1 - 1 / (1 + rho)) if rho > 0 else 0.0     # rho * C_{1/(1+rho)}
    rhos = np.concatenate([np.linspace(1e-3, 5, 400), np.geomspace(5, 400, 200)])
    E0s = np.array([E0(r) for r in rhos])
    for fr in (0.1, 0.3, 0.6):
        x = fr * E
        th1 = ch.theta_na_direct(x)[0]
        th2 = float(np.max((E0s - x) / rhos))
        R1 = ch.R(x)
        R2 = float(np.max((E0s - x) / (1 + rhos)))
        Esp = float(np.max(E0s - rhos * th1))
        print(f"  x = {fr} E: theta_na(x) = {th1:.6f} = max_rho (E_0 - x)/rho = {th2:.6f};  E_sp(theta_na(x)) = {Esp:.6f} (x = {x:.6f});"
              f"  R(x) = {R1:.6f} = max_rho (E_0 - x)/(1+rho) = {R2:.6f}")
    print(f"  E_0(rho -> infinity) = {E0s[-1]:.5f} (E = {E:.5f});  E_0(rho)/rho at rho -> 0: {E0s[0]/rhos[0]:.5f} (a = {a:.5f})")
print(f"time {time.time()-t00:.0f} s")
