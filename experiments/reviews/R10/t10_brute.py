"""brute force on full cubes (n <= 10): formula (2.3), Theorem T4, Theorem T1(a), and the block-sum
machinery of r10fin.py.  Fixed seed."""
import time, itertools
import numpy as np
from scipy.special import logsumexp
from r10fin import *
t0 = time.time()
rng = np.random.default_rng(2026)

def cw(bJ, bB):
    return lambda k: -(bJ / 2.0) * (2 * k - 1) ** 2 - bB * (2 * k - 1)

models = [("two phases", cw(1.5, 0.0)), ("field+coupling", cw(0.5, 0.3)), ("field", cw(0.0, 0.4)), ("antiferro", cw(-2.0, 0.1)), ("two phases+field", cw(1.5, 0.05))]
worst23 = 0.0; worstT4 = -np.inf; maxratio = 0.0; nchk = 0; lipfail = 0
for name, phi in models:
    for n in (5, 7, 9):
        for u in (0.3, 1.0, 2.5):
            J = exchangeable(n, phi)
            Vn = lip_minorant(J, u)
            br = Brute(n, J, u)
            ZH = np.sum(np.exp(-(J - Vn)))
            for rep in range(6):
                # random symmetric instance: u-Lipschitz g on the lattice
                steps = rng.uniform(-u, u, size=n)
                g = np.concatenate(([0.0], np.cumsum(steps)))
                if rep == 0:
                    g = np.zeros(n + 1)
                if rep == 1:
                    g = -Vn.copy()
                cg = np.min(J + g)
                Lam = -g + cg
                Zg = np.sum(np.exp(-(J - Lam)))
                psi = g[br.wt]
                psiH = -Vn[br.wt]
                # random set
                mask = rng.random(1 << n) < rng.choice([0.05, 0.3, 0.7])
                if mask.all() or not mask.any():
                    continue
                dipped = br.dip(psi, mask)
                lipfail += (not br.is_lip(dipped))
                Phi, PhiP, mu = br.phi(psi, mask)
                lhs = br.A(dipped) / br.A(psi)
                # formula (2.3)
                inner = np.min(np.where(mask[None, :], np.inf, u * br.d + Lam[br.wt][None, :]), axis=1)
                f23 = np.sum(br.pi[mask] * np.exp(inner[mask])) / Zg
                worst23 = max(worst23, abs(lhs - (1 + Phi)) / lhs, abs(f23 - PhiP) / PhiP)
                # T4
                _, PhiPH, _ = br.phi(psiH, mask)
                worstT4 = max(worstT4, Zg * PhiP / (ZH * PhiPH) - 1.0)
                maxratio = max(maxratio, PhiP / PhiPH)
                nchk += 1
print(f"(2.3) and A(dip)/A = 1+Phi: {nchk} cases, worst relative error {worst23:.2e}; dips not in L_u: {lipfail}")
print(f"T4: max of Z_g Phi_g+ / (Z_H Phi_H+) - 1 = {worstT4:.2e} (must be <= 0);  largest Phi_g+/Phi_H+ = {maxratio:.4f}")

# T4: is the factor needed?  D = complement of one point at the type of the minimum of J, g = 0
for name, phi in models[:2]:
    for n, u in ((8, 1.0), (8, 3.0), (10, 6.0)):
        J = exchangeable(n, phi); Vn = lip_minorant(J, u); br = Brute(n, J, u)
        t0_ = int(np.argmin(J))
        y = int(np.nonzero(br.wt == t0_)[0][0])
        mask = np.ones(1 << n, bool); mask[y] = False
        g = np.zeros(n + 1); Lam = -g + np.min(J + g)
        Zg = np.sum(np.exp(-(J - Lam))); ZH = np.sum(np.exp(-(J - Vn)))
        _, P0, _ = br.phi(g[br.wt], mask); _, PH, _ = br.phi(-Vn[br.wt], mask)
        print(f"   {name} n={n} u={u}: Phi_0+/Phi_H+ = {P0/PH:.4f}  Z_H/Z_0 = {ZH/Zg:.4f}  (n+1 = {n+1})")

# block machinery against brute force
worst = 0.0; nb = 0
for name, phi in models[:3]:
    for sizes in ((3, 4), (5, 4), (2, 3, 4), (3, 3, 3), (2, 2, 3, 2)):
        n = sum(sizes); u = float(rng.choice([0.4, 1.0, 2.0]))
        fb = FinBlocks(sizes, phi, u)
        br = Brute(n, fb.J, u)
        # block of each coordinate; cell index of each point
        bounds = np.cumsum((0,) + sizes)
        cell = []
        for b in range(len(sizes)):
            bits = sum(((br.pts >> c) & 1) for c in range(bounds[b], bounds[b + 1]))
            cell.append(bits)
        for rep in range(8):
            cm = rng.random(fb.t.shape) < rng.choice([0.1, 0.4])
            if cm.all() or not cm.any():
                continue
            mask = cm[tuple(cell)]
            for Lam in (fb.Vn, np.full(n + 1, fb.J.min())):
                g = -Lam
                r = fb.dip(cm, Lam)
                Phi, PhiP, mu = br.phi(g[br.wt], mask)
                worst = max(worst, abs(np.exp(r['lPhiP']) - PhiP) / PhiP, abs(np.exp(r['lmu']) - mu) / mu,
                            abs(r['maxdens'] - br.maxdens(mask)), abs(np.exp(fb.lmaxdens(cm)) - br.maxdens(mask)))
                nb += 1
print(f"block sums against brute force: {nb} cases, worst error {worst:.2e}")

# T1(a): truncation at type-wise quantiles
bad = 0; nt = 0
for name, phi in models[:3]:
    for n in (6, 8, 9):
        u = float(rng.choice([0.5, 1.0, 2.0]))
        J = exchangeable(n, phi); br = Brute(n, J, u)
        for rep in range(12):
            a = rng.normal(0, 2.0 * u, size=1 << n)
            psi = np.min(a[None, :] + u * br.d, axis=1)          # a member of L_u
            assert br.is_lip(psi)
            w = np.exp(-psi)
            q = float(rng.choice([0.05, 0.2, 0.5, 0.8]))
            thr = np.zeros(n + 1)
            ok_dens = True
            for t in range(n + 1):
                wt = w[br.wt == t]
                vals = np.unique(wt)
                tau = None
                for vv in vals:                                    # smallest value with dens{w > value} <= q
                    if np.mean(wt > vv) <= q:
                        tau = vv; break
                thr[t] = tau
                ok_dens &= (np.mean(wt >= tau) >= q - 1e-15) and (np.mean(wt > tau) <= q + 1e-15)
            tr = np.maximum(psi, -np.log(thr[br.wt]))
            Dm = w > thr[br.wt]
            okl = br.is_lip(tr)
            okq = (np.all(np.abs(np.diff(np.log(thr))) <= u + 1e-12))
            nt += 1
            bad += (not (okl and okq and ok_dens and (br.maxdens(Dm) <= q + 1e-15 if Dm.any() else True)))
print(f"T1(a): {nt} random (psi, q): violations {bad}")
print("time", time.time() - t0)
