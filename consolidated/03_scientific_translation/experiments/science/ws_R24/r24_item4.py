#!/usr/bin/env python3
"""R24, item 4: a sandwich as a class of ensembles (addendum item 89; SCI-RES-0032 section 4).  Own linear programmes.

 H1  (a) the class P(sqrt(l u), d) with d(x, y) = (D(x) + D(y))/2 for x != y, d(x, x) = 0, IS the sandwich -- also when some
     states have D = 0 (then d is a pseudo-metric: d(x, y) = 0 for two distinct states of zero width).  Test: maximum of random
     functionals over the polytope (LP) = maximum over the box (threshold vertices); every LP vertex scales into the box.
     Control: the envelope D(x) + D(y) (twice the hub metric) gives a strictly larger class.
 H2  (b) a COUNTEREXAMPLE to "data pin only bang-bang members" and to the criterion without its level-set clause: four states,
     two means, a member whose weight is strictly inside the box at one state and which is nevertheless the only member with
     these two means (LP: every coordinate has range zero).  Controls: with the first mean alone the range is positive; a
     member strictly inside at every state is not identified by the same two functions, and is by three (complete data).
     The criterion as printed in item 89 (b) is satisfied by every member with f = 1 (nothing above, nothing below).
 H3  (c) stability.  The bound TV <= (t* - E f)/gamma; the BEST constant for a given sandwich and f,
            C*(f) = max_y (1 - mu_f(y)) / |f(y) - t*|   <=   1/gamma,
     attained by moving one weight (proved in the report); checked by linear-fractional programmes over every subset.
     Control: 0.98 C* is violated.  gamma -> 0: C* grows like 1/gamma (the blow-up is real).
 H4  (d) sandwich + r data, r = 2, 3: the certificate value at the LP's own multipliers = the LP value; soundness at random
     multipliers.  And the cost: on a product model with r = 3 additive integer statistics the certificate at the optimal
     multiplier needs the law of ONE real additive statistic; with that statistic rounded up to a grid eps a single counter
     gives a sound end within n eps of the exact one -- no counter per statistic.
Run: python3 -B r24_item4.py > r24_item4.log
"""
import os, sys, math, time, itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack as svstack, hstack as shstack, eye as seye
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r24_common as C
from r24_item3 import my_range


def hub_rows(u, l, factor=0.5):
    N = len(u); pi = np.sqrt(u * l); D = np.log(u / l); rows = []
    for x in range(N):
        for y in range(N):
            if x != y:
                r = np.zeros(N); r[y] = pi[x]; r[x] = -math.exp(factor * (D[x] + D[y])) * pi[y]; rows.append(r)
    return np.array(rows)


def lp(c, A, N, Aeq=None, beq=None, sense=+1):
    Ae = np.ones((1, N)) if Aeq is None else np.vstack([np.ones((1, N)), Aeq]); be = [1.0] if beq is None else [1.0] + list(beq)
    r = linprog(-sense * np.asarray(c, float), A_ub=A, b_ub=np.zeros(len(A)), A_eq=Ae, b_eq=be, bounds=[(0, None)] * N, method="highs")
    return (None, None, None) if r.status != 0 else (sense * (-r.fun), r.x, r)


def threshold(f, u, l):
    """upper end t*, threshold weights v (u where f > t*, l where f < t*; u on the level set), gap gamma"""
    t = my_range(f, u, l)[1]; v = np.where(f > t + 1e-13, u, np.where(f < t - 1e-13, l, u)); return t, v, float(np.abs(f - t).min())


def main():
    t0 = time.time(); rng = np.random.default_rng(2404)
    # ------------------------------------------------------------------ H1
    dev = 0.0; nfun = 0; scal = 0; nvert = 0; ctrl = 0; ncase = 0; pseudo = 0
    for N in (3, 4, 6, 8):
        for rep in range(12):
            l = rng.uniform(0.05, 1.0, N); u = l * np.exp(rng.uniform(0.05, 2.0, N)); nz = rep % 4                       # number of states of zero width: 0, 1, 2, 3
            for z in rng.choice(N, size=min(nz, N - 1), replace=False): u[z] = l[z]
            D = np.log(u / l); pseudo += int((D == 0).sum() >= 2); A = hub_rows(u, l); A2 = hub_rows(u, l, 1.0); ncase += 1; bigger = 0.0
            for q in range(8):
                f = rng.normal(size=N); v, x, _ = lp(f, A, N); nfun += 1; dev = max(dev, abs(v - my_range(f, u, l)[1]))
                # the vertex scales into the box: max mu/u <= min mu/l
                nvert += 1; scal += int((x / u).max() <= (x / l).min() * (1 + 1e-9))
                bigger = max(bigger, lp(f, A2, N)[0] - v)
            ctrl += int(bigger > 1e-6 or (D == 0).all())
    print(f"H1  hub class against the box, {ncase} boxes of 3 to 8 states of which {pseudo} have two or more states of zero width (d is then a pseudo-metric): LP maximum over the polytope minus the box maximum over {nfun} functionals: "
          f"largest {dev:.1e} (must be < 1e-8); LP vertices that scale into the box: {scal} of {nvert}; control, the envelope D(x) + D(y): a strictly larger class in {ctrl} of {ncase} boxes (must be all)")
    assert dev < 1e-8 and scal == nvert and ctrl == ncase
    # ------------------------------------------------------------------ H2
    l = np.array([0.5, 0.5, 2.0, 1.0]); u = np.array([1.0, 1.0, 3.0, 2.0]); w0 = np.array([1.0, 1.0, 2.0, 1.5]); mu0 = w0 / w0.sum(); A = hub_rows(u, l)
    f = np.array([2.0, 2.0, 0.0, 1.0]); g = np.array([0.0, 0.0, 0.0, 1.0]); h3 = np.array([1.0, 0.0, 0.0, 0.0])
    tstar = my_range(f, u, l)[1]

    def widths(data, mu):
        Aeq = np.array(data) if data else None; beq = [float(d @ mu) for d in data] if data else None; out = []
        for x in range(4):
            e = np.zeros(4); e[x] = 1.0; hi = lp(e, A, 4, Aeq, beq, +1)[0]; lo = lp(e, A, 4, Aeq, beq, -1)[0]; out.append(hi - lo)
        return out
    wi = widths([f, g], mu0); w1 = widths([f], mu0)
    wint = np.array([0.8, 0.7, 2.5, 1.5]); muint = wint / wint.sum(); wi2 = widths([f, g], muint); wi3 = widths([f, g, h3], muint)
    print(f"H2  four states, l = {l.tolist()}, u = {u.tolist()}; member w = {w0.tolist()} (strictly inside the box at the fourth state: 1 < 1.5 < 2); f = {f.tolist()}: upper end t* = {tstar:.6f}, E f at the member = {float(f @ mu0):.6f}; "
          f"second datum: the population of the fourth state.  Range of each mu(x) over the members with these two means: {', '.join(f'{v:.1e}' for v in wi)} (all zero: IDENTIFIED by two means on four states); "
          f"controls: with the first mean alone: {', '.join(f'{v:.3f}' for v in w1)} (positive); a member strictly inside at every state, same two functions: {', '.join(f'{v:.3f}' for v in wi2)} (positive: not identified); "
          f"the same with a third function (complete data): {', '.join(f'{v:.1e}' for v in wi3)}")
    # the printed criterion with f = 1: every member satisfies "at the floor where f > t, at the ceiling where f < t" with t = 1
    assert max(wi) < 1e-7 and min(w1[3:]) > 1e-3 and max(wi2) > 1e-3 and max(wi3) < 1e-7
    # ------------------------------------------------------------------ H3
    worst = -1e9; devC = 0.0; ctrl3 = 0; n3 = 0; ratio_g = []; pop_ratio = []
    for N in (4, 5, 6, 7):
        for rep in range(8):
            l = rng.uniform(0.05, 1.0, N); u = l * np.exp(rng.uniform(0.2, 2.0, N)); A = hub_rows(u, l)
            f = rng.normal(size=N) if rep % 2 else (rng.random(N) < 0.5).astype(float)
            if len(np.unique(f)) == 1: f[0] = 1 - f[0]
            t, v, gam = threshold(f, u, l)
            if gam < 1e-4: continue
            muf = v / v.sum(); Cstar = float(((1 - muf) / np.abs(f - t)).max()); n3 += 1; best = 0.0; worst_c = -1e9; viol98 = -1e9
            for bits in range(1, 2 ** N - 1):
                iA = np.array([(bits >> j) & 1 for j in range(N)], dtype=float)
                # sup of [mu(A) - mu_f(A)] / (t - E f): variables (y, s), y = s mu:  maximise iA.y - mu_f(A) s  s.t.  t s - f.y = 1, sum y = s
                c = np.concatenate([-iA, [float(iA @ muf)]]); Aeq = np.vstack([np.concatenate([-f, [t]]), np.concatenate([np.ones(N), [-1.0]])])
                r = linprog(c, A_ub=np.hstack([A, np.zeros((len(A), 1))]), b_ub=np.zeros(len(A)), A_eq=Aeq, b_eq=[1.0, 0.0], bounds=[(0, None)] * (N + 1), method="highs")
                if r.status == 0: best = max(best, -r.fun)
                vv = lp(iA + Cstar * f, A, N)[0]; worst_c = max(worst_c, vv - float(iA @ muf) - Cstar * t)
                vv = lp(iA + 0.98 * Cstar * f, A, N)[0]; viol98 = max(viol98, vv - float(iA @ muf) - 0.98 * Cstar * t)
            devC = max(devC, abs(best - Cstar) / Cstar); worst = max(worst, worst_c); ctrl3 += int(viol98 > 1e-7); ratio_g.append(Cstar * gam)
            if rep % 2 == 0: pop_ratio.append(Cstar * min(t, 1 - t))
    print(f"H3  stability, {n3} sandwiches of 4 to 7 states (random and indicator observables), every subset: the best constant sup TV / (t* - E f) by linear-fractional programmes against C*(f) = max_y (1 - mu_f(y))/|f(y) - t*|: "
          f"largest relative deviation {devC:.1e} (must be < 1e-6); max over the class of TV - C* (t* - E f): {worst:+.1e} (must be <= 1e-9); control, 0.98 C*: violated in {ctrl3} of {n3} (must be all); "
          f"C* gamma between {min(ratio_g):.3f} and {max(ratio_g):.3f} (<= 1: the constant 1/gamma of item 89 is valid and not attained); populations: C* min(P, 1 - P) between {min(pop_ratio):.3f} and {max(pop_ratio):.3f}")
    assert devC < 1e-6 and worst <= 1e-9 and ctrl3 == n3
    # gamma -> 0: one state whose value approaches the threshold
    l = np.array([0.3, 0.5, 0.4, 0.6, 0.2]); u = l * np.array([2.0, 3.0, 1.5, 2.5, 2.0]); line = []
    for eps in (0.3, 0.1, 0.01, 0.001):
        f = np.array([1.0, 0.8, -0.5, -1.0, 0.0]); t = my_range(f, u, l)[1]; f[4] = t - eps                                  # the fifth state sits eps below the threshold of the others
        t, v, gam = threshold(f, u, l); muf = v / v.sum(); Cs = float(((1 - muf) / np.abs(f - t)).max())
        w = v.copy(); w[4] = u[4]; mu = w / w.sum(); tv = 0.5 * float(np.abs(mu - muf).sum()); deficit = t - float(f @ mu)
        line.append(f"gap {gam:.4f}: C* = {Cs:.1f}, 1/gamma = {1 / gam:.1f}; the member with the fifth weight at its other bound: TV = {tv:.4f}, t* - E f = {deficit:.5f}, ratio {tv / deficit:.1f}")
    print("    gamma -> 0: " + "; ".join(line) + "  (the distance stays, the deficit vanishes: no stability towards mu_f; what survives is the distance to the face of maximisers)")
    # ------------------------------------------------------------------ H4
    dev4 = 0.0; unsound = 0; n4 = 0
    for N in (6, 8, 10):
        for r_ in (2, 3):
            for rep in range(8):
                l = rng.uniform(0.05, 1.0, N); u = l * np.exp(rng.uniform(0.2, 2.0, N)); A = hub_rows(u, l); psi = rng.normal(size=N); Phi = rng.normal(size=(r_, N))
                w = l + (u - l) * rng.random(N); m = Phi @ (w / w.sum()); v, x, res = lp(psi, A, N, Phi, list(m)); n4 += 1
                nu = np.asarray(res.eqlin.marginals)[1:]                                   # multipliers of the data constraints (HiGHS: of the minimisation of -psi)
                tl = lambda lam: my_range(psi - lam @ (Phi - m[:, None]), u, l)[1]
                dev4 = max(dev4, min(abs(tl(nu) - v), abs(tl(-nu) - v)))
                for _ in range(5): unsound += int(tl(rng.normal(size=r_) * 2) < v - 1e-9)
    print(f"H4  sandwich + r data (r = 2, 3; {n4} cases of 6 to 10 states): certificate value at the linear programme's own multipliers against its value: largest deviation {dev4:.1e} (must be < 1e-7); "
          f"a certificate value below the LP value at a random multiplier: {unsound} of {5 * n4} (must be 0)")
    assert dev4 < 1e-7 and unsound == 0
    # the cost: a product model, r = 3 integer additive statistics, one rounded counter
    out = []
    for rep in range(3):
        n = 7; kk = 3; r_ = 3; ui = rng.uniform(0.3, 1.0, (n, kk)); li = ui * np.exp(-rng.uniform(0.05, 0.6, (n, kk)))
        psi_i = rng.integers(0, 3, (n, kk)).astype(float); phi_i = rng.integers(0, 3, (r_, n, kk)).astype(float)
        X = np.array(list(itertools.product(range(kk), repeat=n))); N = len(X); ar = np.arange(n)
        U = np.prod(ui[ar, X], axis=1); Lw = np.prod(li[ar, X], axis=1); psi = psi_i[ar, X].sum(axis=1); Phi = np.stack([phi_i[j][ar, X].sum(axis=1) for j in range(r_)])
        w0 = np.sqrt(U * Lw); m = Phi @ (w0 / w0.sum())
        # exact end: maximise sum w psi, s.t. l s <= w <= u s, sum w = 1, sum w (Phi - m) = 0   (variables w and s; sparse)
        I = seye(N, format="csr"); Aub = svstack([shstack([I, csr_matrix(-U[:, None])]), shstack([-I, csr_matrix(Lw[:, None])])]).tocsr()
        Aeq = np.vstack([np.concatenate([np.ones(N), [0.0]])] + [np.concatenate([Phi[j] - m[j], [0.0]]) for j in range(r_)])
        res = linprog(np.concatenate([-psi, [0.0]]), A_ub=Aub, b_ub=np.zeros(2 * N), A_eq=Aeq, b_eq=[1.0] + [0.0] * r_, bounds=[(0, None)] * (N + 1), method="highs")
        assert res.status == 0; exact = -res.fun; nu = np.asarray(res.eqlin.marginals)[1:]
        best = None
        for lam in (nu, -nu):
            hfull = psi - lam @ (Phi - m[:, None]); t_enum = my_range(hfull, U, Lw)[1]
            if best is None or abs(t_enum - exact) < abs(best[1] - exact): best = (lam, t_enum)
        lam, t_enum = best; hi = psi_i - np.tensordot(lam, phi_i, axes=1); const = float(lam @ m); rowres = []
        for eps in (0.05, 0.01, 0.002):
            # one counter: the law of the rounded-up statistic sum_i ceil(h_i(x_i)/eps) under floor and ceiling, by convolution over the sites
            g = np.ceil(hi / eps - 1e-12).astype(int); gmin = int(g.min(axis=1).sum()); gmax = int(g.max(axis=1).sum()); lawU = np.zeros(gmax - gmin + 1); lawL = np.zeros(gmax - gmin + 1); lawU[0] = lawL[0] = 1.0; off = 0
            for i in range(n):
                nu_ = np.zeros_like(lawU); nl_ = np.zeros_like(lawL); base = int(g[i].min())
                for s in range(kk):
                    sh = int(g[i, s]) - base
                    nu_[sh:] += ui[i, s] * lawU[:len(lawU) - sh] if sh else ui[i, s] * lawU
                    nl_[sh:] += li[i, s] * lawL[:len(lawL) - sh] if sh else li[i, s] * lawL
                lawU, lawL = nu_, nl_
            vals = (gmin + np.arange(len(lawU))) * eps + const; keep = (lawU > 0) | (lawL > 0)
            t_cert = my_range(vals[keep], lawU[keep], lawL[keep])[1]; rowres.append((eps, t_cert, len(lawU)))
        joint = int(np.prod([int(Phi[j].max() - Phi[j].min()) + 1 for j in range(r_)]) * (int(psi.max() - psi.min()) + 1))
        out.append(f"case {rep + 1}: exact end {exact:.6f} (LP over {N} states), certificate at the LP's multiplier by enumeration {t_enum:.6f}; one rounded counter: "
                   + ", ".join(f"eps = {e:g}: {t:.6f} (sound: {t >= exact - 1e-9}; above the exact end by {t - exact:.1e} <= n eps = {n * e:g}: {t - exact <= n * e + 1e-9}; {cells} cells)" for e, t, cells in rowres)
                   + f"; a joint counter for the {r_ + 1} integer statistics has {joint} cells")
    print("    the cost of the certificate for r = 3 additive statistics on a product model (7 sites, 3 states): " + " | ".join(out))
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {C.rss():.0f} MB")


if __name__ == "__main__":
    main()
