"""exact finite-n sums (own code, r10fin.py):
 A. Theorem T3(a) at n = 60, 120, 240 for 2- and 3-block profiles: both inequalities.
 B. one entry each of the tables of Section 6.3: dips of H at eps = 1 (n = 250, 1000) and the
    truncated shell-cone at eps = 0.0251012 n (n = 250).
usage: python3 t11_finite.py [A|B]"""
import time, sys, math
import numpy as np
from scipy.special import logsumexp
from r10lib import *
from r10fin import *
t0 = time.time()
which = sys.argv[1] if len(sys.argv) > 1 else "AB"
bJ, u = 1.5, 1.0
phi = lambda k: -(bJ / 2.0) * (2 * k - 1) ** 2
M = Model(bJ=bJ, bB=0.0, u=u)

if "A" in which:
    print("# A. Theorem T3(a): D = union of the classes c' with u*l1(c',c)/n + v(type/n) < B around the class c of a lattice profile")
    print("#    n  blocks  profile  B   ln(1+Phi)  bound n(B-alpha_n)-ln2-lnZ   ok   -ln(maxdens)/n   V(mu,B;v) - k ln(n+1)/n   ok")
    for n in (60, 120, 240):
        for sizes, counts in (((n // 2, n // 2), (round(0.70 * n / 2), round(0.30 * n / 2))),
                              ((n // 2, n // 2), (round(0.73 * n / 2), round(0.27 * n / 2))),
                              ((n // 3, n // 3, n // 3), (round(0.72 * n / 3), round(0.5 * n / 3), round(0.28 * n / 3))),
                              ((n // 4, n // 2, n // 4), (round(0.8 * n / 4), round(0.45 * n / 2), round(0.2 * n / 4)))):
            fb = FinBlocks(sizes, phi, u)
            nn = fb.n
            lam = np.array(sizes) / nn
            mu = np.array(counts) / np.array(sizes)
            Lam = nn * M.v(np.arange(nn + 1) / nn)                 # the instance psi_n = -n v(|x|/n)
            lZ = float(logsumexp(-fb.J + Lam))                      # ln A(psi_n)
            l1 = sum(np.abs(c - c0) for c, c0 in zip(fb.cnt, counts))
            cell = tuple(counts)
            alpha_n = -fb.lpi[cell] / nn
            for de in (0.0, -0.02, -0.05, 0.02):
                B = alpha_n + de
                if B <= float(M.v(counts_type := sum(counts) / nn)) + math.log(2) / nn:
                    continue
                mask = (u * l1 / nn + Lam[fb.t] / nn) < B
                if mask.all():
                    continue
                r = fb.dip(mask, Lam)
                bound = nn * (B - alpha_n) - math.log(2) - lZ
                theta = -fb.lmaxdens(mask) / nn
                V = inner_clip(M, lam, mu, B, G=400, zooms=5, ncand=6, nz=41, rounds=8)[0]
                ok1 = r['eff'] >= bound - 1e-9
                ok2 = theta >= V - len(sizes) * math.log(nn + 1) / nn - 1e-12
                print(f"   {nn:4d} {sizes} {tuple(np.round(mu,3))} B={B:.4f}  {r['eff']:.4f} >= {bound:.4f} {ok1}   theta={theta:.5f} >= {V - len(sizes)*math.log(nn+1)/nn:.5f} (V={V:.5f}) {ok2}", flush=True)

if "B" in which:
    print("# B. Section 6.3, exact sums around a centre of type n/2")

    def grid_ij(n, k):
        """two-block grid in the coordinates (i, j): i = zeros of x on the ones of the centre,
        j = ones of x on its zeros; type t = k - i + j; l1 distance of (i, j) = Hamming distance of classes"""
        ii, jj = np.meshgrid(np.arange(k + 1), np.arange(n - k + 1), indexing='ij')
        f2 = FinBlocks((k, n - k), phi, u)
        f2.t = k - ii + jj
        f2.lmult = lbinom(k, ii) + lbinom(n - k, jj)
        f2.ldens = f2.lmult - f2.lCn[f2.t]
        f2.lpi = f2.ldens - f2.J[f2.t]
        f2.cnt = [ii, jj]
        return f2, ii, jj

    def capped(f2, k, n, q):
        """in every type class the classes on the side of the centre (i/k + j/(n-k) < 1), rarest
        first (increasing i), as long as their cumulative density stays <= q"""
        m = n - k
        mask = np.zeros(f2.t.shape, bool)
        dens = np.exp(f2.ldens)
        for t in range(n + 1):
            ii = np.arange(max(0, k - t), min(k, n - t) + 1)
            jj = t - k + ii
            sel = (ii * m + jj * k) < k * m
            ii, jj = ii[sel], jj[sel]
            if len(ii) == 0:
                continue
            ok = np.cumsum(dens[ii, jj]) <= q
            mask[ii[ok], jj[ok]] = True
        return mask

    for n, ref in ((250, 0.025153), (1000, 0.025092)):
        k = n // 2
        f2, ii, jj = grid_ij(n, k)
        eps = 1.0
        lo, hi = -n * math.log(2.0) - 5.0, 0.0
        best = None
        for _ in range(44):
            mid = 0.5 * (lo + hi)
            mask = capped(f2, k, n, math.exp(mid))
            ok = False
            if mask.any():
                r = f2.dip(mask, f2.Vn)
                ok = r['eff'] > eps
            if ok:
                hi, best = mid, (f2.lmaxdens(mask), r['eff'])
            else:
                lo = mid
        print(f"   dips of H, eps = 1, n = {n}: theta_n = -ln(maxdens)/n = {-best[0]/n:.6f}   (report {ref});  ln(1/q)/n = {-hi/n:.6f}, ln(1+Phi) = {best[1]:.4f}   t={time.time()-t0:.0f}", flush=True)
    # truncated shell-cone around the class x = 0.298 at eps = 0.0251012 n, n = 250 (report 0.031466) and n = 1000 (0.027977)
    for n, ref in ((250, 0.031466), (1000, 0.027977)):
        k = n // 2
        ii, jj = np.meshgrid(np.arange(k + 1), np.arange(n - k + 1), indexing='ij')
        J = exchangeable(n, phi)
        lCn = lbinom(n, np.arange(n + 1))
        t = (k - ii + jj)
        ldens = lbinom(k, ii) + lbinom(n - k, jj) - lCn[t]
        i0 = int(round(0.298 * k)); j0 = int(round(0.298 * (n - k)))
        Ld = (np.abs(ii - i0) + np.abs(jj - j0))                   # distance to the class
        base = ldens - J[t]
        lA = float(logsumexp(base - u * Ld))
        eps = 0.0251012 * n
        # per type: levels of w = exp(-u L); t_t(q) = smallest value tau of w with dens{w > tau} <= q
        types = [np.nonzero(t.ravel() == tt)[0] for tt in range(n + 1)]
        Lr, dr, br = Ld.ravel(), np.exp(ldens.ravel()), base.ravel()
        per = []
        for idx in types:
            L_ = Lr[idx]; d_ = dr[idx]
            lev = np.unique(L_)                                   # increasing distance = decreasing weight
            below = np.array([d_[L_ < l].sum() for l in lev])     # dens{w > exp(-u l)} = dens{L < l}
            per.append((idx, L_, lev, below))
        def ratio(q):
            parts = []
            for idx, L_, lev, below in per:
                okl = lev[below <= q * (1 + 1e-12)]
                Lstar = okl.max()                                  # largest level with dens{L < level} <= q, i.e. smallest tau
                parts.append(br[idx] - u * np.maximum(L_, Lstar))
            return lA - float(logsumexp(np.concatenate(parts)))
        lo, hi = -n * math.log(2.0) - 5.0, 0.0
        for _ in range(44):
            mid = 0.5 * (lo + hi)
            if ratio(math.exp(mid)) > eps:
                hi = mid
            else:
                lo = mid
        print(f"   truncated shell-cone x = 0.298, eps = 0.0251012 n, n = {n}: theta_n = ln(1/q)/n = {-hi/n:.6f}   (report {ref})   t={time.time()-t0:.0f}", flush=True)
print("time", time.time() - t0)
