#!/usr/bin/env python3
"""t05 -- brute force on full cubes (n <= 12) against the profile-grid sums of tfin.py, and the every-n statements of
section 3 of the report checked literally:
 (1) dips of symmetric instances on unions of profile classes: Phi+, mu(D), Phi, maxdens;
 (2) the dip psi^D (lower McShane extension) is in L_u and A(psi^D)/A(psi) = 1 + Phi(D);
 (3) type-wise quantile truncation of an arbitrary psi in L_u is in L_u, changes psi on a set of density <= q in every
     type class (Theorem 11.61(a) for an arbitrary exchangeable pi), and tfin's ratio for shell-cones is exact.
usage: python3 t05_bruteforce.py
"""
import itertools, math, sys, time
import numpy as np
import tlib as T
import tfin as F

rng = np.random.default_rng(12345)
t0 = time.time()
nchecks, nfail, worst = 0, 0, 0.0


def check(a, b, what, tol=1e-9):
    global nchecks, nfail, worst
    nchecks += 1
    err = abs(a - b) / max(1.0, abs(a), abs(b))
    worst = max(worst, err)
    if not err <= tol:
        nfail += 1
        print("   FAIL", what, a, b)


def cube(n):
    X = np.array(list(itertools.product([0, 1], repeat=n)), dtype=np.int8)
    Dm = (X[:, None, :] != X[None, :, :]).sum(axis=2)
    return X, Dm


cases = [(8, 4, T.phi_cw(1.5, 0.0), 1.0), (9, 3, T.phi_cw(1.5, 0.1), 0.7), (10, 5, T.phi_cw(2.0, 0.0), 0.4),
         (10, 4, T.phi_field(0.2), 2.0), (11, 5, T.phi_cw(0.5, 0.3), 1.0), (12, 6, T.phi_cw(1.5, 0.0), 1.0)]
for (n, k, phi, u) in cases:
    X, Dm = cube(n)
    wt = X.sum(axis=1)
    f = F.Fin(n, k, phi, u)
    s = np.array([1] * k + [0] * (n - k), dtype=np.int8)
    pi = np.exp(-f.J[wt] - f.lCn[wt])                      # pi(x) = p_t / C(n,t)
    check(pi.sum(), 1.0, "pi normalised")
    ii = ((s == 1) & (X == 0)).sum(axis=1)
    jj = ((s == 0) & (X == 1)).sum(axis=1)
    for (name, Lam) in (("H", f.Vn), ("zero", np.zeros(n + 1)), ("add", -0.3 * u * np.arange(n + 1.0))):
        psi = -Lam[wt]                                     # the instance (up to a constant)
        # instance is in L_u ?
        assert np.all(np.abs(psi[:, None] - psi[None, :]) <= u * Dm + 1e-9)
        w = np.exp(-psi)
        A = float((pi * w).sum())
        mu = pi * w / A
        for trial in range(6):
            # a union of profile classes: random down-set-like or random mask on the grid
            if trial < 3:
                q = [0.02, 0.1, 0.3][trial]
                mask = f.capped_family()(q)
            else:
                mask = rng.random(f.t.shape) < 0.35
            if not mask.any() or mask.all():
                continue
            inD = mask[ii, jj]
            out = ~inD
            slack = u * Dm[:, out] + psi[:, None] - psi[None, out]
            sx = slack.min(axis=1)                                  # s(x -> D^c)
            PhiP = float((mu[inD] * np.exp(sx[inD])).sum())
            Phi = float((mu[inD] * np.expm1(sx[inD])).sum())
            muD = float(mu[inD].sum())
            dens = np.array([inD[wt == t].mean() if (wt == t).any() else 0.0 for t in range(n + 1)])
            lPhiP, lmu, lPhi, md = f.dip(mask, Lam)
            check(math.exp(lPhiP), PhiP, f"Phi+ n={n} {name} trial {trial}")
            check(math.exp(lmu), muD, f"mu(D) n={n} {name} trial {trial}")
            if Phi > 1e-12:
                check(math.exp(lPhi), Phi, f"Phi n={n} {name} trial {trial}", tol=1e-8)
            check(md, dens.max(), f"maxdens n={n} {name} trial {trial}")
            # (2) the dip itself
            psiD = psi.copy()
            psiD[inD] = (psi[None, out] - u * Dm[np.ix_(inD, out)]).max(axis=1)
            assert np.all(np.abs(psiD[:, None] - psiD[None, :]) <= u * Dm + 1e-9), "dip not in L_u"
            AD = float((pi * np.exp(-psiD)).sum())
            check(AD / A, 1.0 + Phi, f"A(dip)/A n={n} {name} trial {trial}")
    # (3) truncation at type-wise quantiles: a random member of L_u, and shell-cones
    for trial in range(4):
        if trial < 2:
            g = rng.normal(size=len(X)) * 3.0
            psi = (g[None, :] + u * Dm).min(axis=1)                 # McShane: in L_u
        else:
            i0, j0 = (1, 1) if trial == 2 else (k // 2, (n - k) // 2)
            psi = u * (np.abs(ii - i0) + np.abs(jj - j0)).astype(float)
        assert np.all(np.abs(psi[:, None] - psi[None, :]) <= u * Dm + 1e-9)
        w = np.exp(-psi)
        for q in (0.05, 0.2, 0.5):
            tk = np.zeros(n + 1)
            for t in range(n + 1):
                wtc = np.sort(w[wt == t])
                # smallest value tau of w on the class with dens{w > tau} <= q
                for tau in np.unique(wtc):
                    if (wtc > tau * (1 + 1e-12)).mean() <= q:
                        tk[t] = tau
                        break
            wtr = np.minimum(w, tk[wt])
            psitr = -np.log(wtr)
            assert np.all(np.abs(psitr[:, None] - psitr[None, :]) <= u * Dm + 1e-9), "truncation not in L_u"
            D = w > tk[wt] * (1 + 1e-12)
            md = max(D[wt == t].mean() for t in range(n + 1))
            assert md <= q + 1e-12
            nchecks += 2
            ratio = math.log(float((pi * w).sum()) / float((pi * wtr).sum()))
            if trial >= 2:
                check(f.shell_cone(i0, j0)(q), ratio, f"truncation ratio n={n} shell ({i0},{j0}) q={q}")
    print(f"n={n} k={k} u={u}: ok so far ({nchecks} checks, {nfail} failures)  [{time.time()-t0:.0f}s]", flush=True)
print(f"TOTAL {nchecks} checks, {nfail} failures, worst relative error {worst:.1e}")
