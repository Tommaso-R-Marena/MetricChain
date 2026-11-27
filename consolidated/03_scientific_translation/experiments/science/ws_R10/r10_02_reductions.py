"""r10_02: brute force of the three reductions of Y_REPORT section 3 on random inhomogeneous
chains (mixed binary/ternary alphabets, random fields, strong couplings, ASYMMETRIC site
envelopes, random cuts / gaps / gauges).  Own code, written from the statements of Theorems
Y1 (U), Y2 (L), Y3 (L') before opening the theory division's code.

 (U)  pi = rho e^{-g}/E_rho e^{-g};  ln A_pi(psi) = ln A_rho(psi+g) - ln A_rho(g);
      psi in C_d  =>  psi+g in C_{d+};  d+ attained;  control: psi+g in C_d fails.
 (L)  marginal of pi on the block sites = (x)_j pi_{B_j} * prod_j rho_j;
      sum_j min ln rho_j <= ln A_pi(psi' o proj) - ln A_{(x) pi_B}(psi') <= sum_j max ln rho_j.
 (L') psi := psi' o proj + sum_j ln rho_j  in C_d  and  A_pi(psi) = A_{(x) pi_B}(psi') exactly,
      for psi' in C_{d-};  control: psi' in C_{d_B} instead.
"""
import sys
import time
import numpy as np

rng = np.random.default_rng(20261125)
TOL = 1e-10


def closure(d):
    """Shortest-path closure of a matrix with zero diagonal (Floyd-Warshall)."""
    d = d.copy()
    q = d.shape[0]
    for k in range(q):
        d = np.minimum(d, d[:, [k]] + d[[k], :])
    return d


def random_envelope(q, scale):
    d = rng.uniform(0.2, 1.0, size=(q, q)) * scale
    np.fill_diagonal(d, 0.0)
    return closure(d)


class Chain:
    def __init__(self, qs, fields, Js):
        self.qs = list(qs)
        self.n = len(qs)
        self.fields = fields
        self.Js = Js
        self.shape = tuple(qs)
        self.N = int(np.prod(qs))
        self.idx = np.indices(self.shape).reshape(self.n, -1)  # idx[i, k] = letter of site i
        en = np.zeros(self.N)
        for i in range(self.n):
            en += fields[i][self.idx[i]]
        for i in range(self.n - 1):
            en += Js[i][self.idx[i], self.idx[i + 1]]
        w = np.exp(-(en - en.min()))
        self.pi = w / w.sum()

    def marginal(self, sites):
        """Marginal law on a sorted list of sites, as an array of shape (q_s for s in sites)."""
        p = self.pi.reshape(self.shape)
        other = tuple(i for i in range(self.n) if i not in sites)
        return p.sum(axis=other)


def dist_matrix(idx, ds, sites=None):
    """D[x, y] = sum_i d_i(x_i, y_i) over the given site list (idx rows correspond to it)."""
    N = idx.shape[1]
    D = np.zeros((N, N))
    for r, d in enumerate(ds):
        D += d[idx[r][:, None], idx[r][None, :]]
    return D


def random_members(D, k):
    """k random members of {psi : psi(x)-psi(y) <= D[x,y]} (D satisfies the triangle
    inequality with zero diagonal): inf-convolutions, cones, max / min / convex combinations."""
    N = D.shape[0]
    out = []
    scale = D.max()
    for j in range(k):
        kind = j % 6
        def infconv():
            r = rng.normal(size=N) * scale * rng.uniform(0.3, 2.0)
            return (r[None, :] + D).min(axis=1)
        if kind == 0:
            psi = infconv()
        elif kind == 1:
            psi = D[:, rng.integers(N)].copy()                  # cone d(., y0)
        elif kind == 2:
            psi = np.maximum(infconv(), infconv())
        elif kind == 3:
            psi = np.minimum(infconv(), infconv() + rng.normal())
        elif kind == 4:
            lam = rng.uniform()
            psi = lam * infconv() + (1 - lam) * infconv()
        else:
            psi = -D[rng.integers(N), :].copy()                 # -d(y0, .)  (also admissible)
        out.append(psi)
    return out


def violation(psi, D):
    return float((psi[:, None] - psi[None, :] - D).max())


def lnA(pi, psi):
    a = np.log(pi) - psi
    m = a.max()
    return m + np.log(np.exp(a - m).sum())


stats = dict(U_id=0.0, U_pi=0.0, U_adm=-1e9, U_ctrl_viol=0, U_cases=0, U_attain=0.0,
             L_marg=0.0, L_viol=0, L_cases=0, L_tight=1e9,
             Lp_adm=-1e9, Lp_id=0.0, Lp_cases=0, Lp_ctrl_viol=0, Lp_ctrl_cases=0, Lp_skipped=0,
             Lp_negentry_cases=0)

t0 = time.time()
chains = []
specs = [([2] * 8, 9), ([2] * 9, 9), ([2] * 10, 6), ([3] * 6, 6), ([2, 3, 2, 3, 2, 3, 2], 6), ([3, 2, 2, 3, 2, 2, 3], 4)]
for qs, reps in specs:
    for rep in range(reps):
        n = len(qs)
        sdJ = rng.choice([0.3, 1.0, 2.5])
        fields = [rng.normal(size=q) * rng.choice([0.0, 0.5, 1.5]) for q in qs]
        Js = [rng.normal(size=(qs[i], qs[i + 1])) * sdJ for i in range(n - 1)]
        ch = Chain(qs, fields, Js)
        ds = [random_envelope(q, rng.choice([0.5, 1.0, 2.0])) for q in qs]
        D = dist_matrix(ch.idx, ds)
        members = random_members(D, 12)
        for psi in members:
            assert violation(psi, D) < TOL

        # ------------------------------------------------------------------ (U)
        ncut = rng.integers(1, n)
        cuts = sorted(rng.choice(n - 1, size=ncut, replace=False))  # cut c: between c and c+1
        f2 = [f.copy() for f in fields]
        Jo = {}
        for c in cuts:
            if rng.uniform() < 0.3:
                r = np.zeros(qs[c]); s = np.zeros(qs[c + 1])
            else:
                r = rng.normal(size=qs[c]); s = rng.normal(size=qs[c + 1])
            Jo[c] = Js[c] - r[:, None] - s[None, :]
            f2[c] = f2[c] + r
            f2[c + 1] = f2[c + 1] + s
        # rho = product over blocks of free-boundary Gibbs laws: energy without the cut terms
        en = np.zeros(ch.N)
        for i in range(n):
            en += f2[i][ch.idx[i]]
        for i in range(n - 1):
            if i not in cuts:
                en += Js[i][ch.idx[i], ch.idx[i + 1]]
        rho = np.exp(-(en - en.min())); rho /= rho.sum()
        # check that rho is a product over blocks (independence across every cut)
        g = np.zeros(ch.N)
        for c in cuts:
            g += Jo[c][ch.idx[c], ch.idx[c + 1]]
        w = rho * np.exp(-g); w /= w.sum()
        stats["U_pi"] = max(stats["U_pi"], np.abs(w - ch.pi).max())
        # d+ : slack
        dplus = [d.copy() for d in ds]
        for c in cuts:
            J = Jo[c]
            dm = (J[:, None, :] - J[None, :, :]).max(axis=2)       # delta^-_c(a,a') = max_b J(a,b)-J(a',b)
            dp = (J[:, :, None] - J[:, None, :]).max(axis=0)       # delta^+_c(b,b') = max_a J(a,b)-J(a,b')
            dplus[c] = dplus[c] + dm
            dplus[c + 1] = dplus[c + 1] + dp
        Dp = dist_matrix(ch.idx, dplus)
        for psi in members:
            lhs = lnA(ch.pi, psi)
            rhs = lnA(rho, psi + g) - lnA(rho, g)
            stats["U_id"] = max(stats["U_id"], abs(lhs - rhs))
            stats["U_adm"] = max(stats["U_adm"], violation(psi + g, Dp))
            if violation(psi + g, D) > 1e-9:
                stats["U_ctrl_viol"] += 1
            stats["U_cases"] += 1
        # d+ attained: for every slack site and ordered pair of letters there are a cone and a
        # pair of configurations differing at that site only with no slack left
        worst = 0.0
        single = {}
        for i in range(n):
            # pairs (x,y) differing only at site i
            same = np.ones((ch.N, ch.N), dtype=bool)
            for j in range(n):
                if j != i:
                    same &= ch.idx[j][:, None] == ch.idx[j][None, :]
            single[i] = same
        for c in set(list(cuts) + [c + 1 for c in cuts]):
            for a in range(qs[c]):
                for a2 in range(qs[c]):
                    if a == a2:
                        continue
                    msk = single[c] & (ch.idx[c][:, None] == a) & (ch.idx[c][None, :] == a2)
                    xs, ys = np.nonzero(msk)
                    # cone psi = d(., y): psi(x) - psi(y) = d(x,y); slack left = d+ - d - (g(x)-g(y))
                    left = (Dp[xs, ys] - D[xs, ys]) - (g[xs] - g[ys])
                    worst = max(worst, left.min())
        stats["U_attain"] = max(stats["U_attain"], worst)

        # ------------------------------------------------------------------ (L), (L')
        # random blocks with gaps (possibly leading / trailing gaps, possibly zero gaps)
        while True:
            labels = []
            pos = 0
            if rng.uniform() < 0.3:
                pos += rng.integers(1, 2 + 1)
            blocks = []
            while pos < n:
                L = rng.integers(1, 4)
                blk = list(range(pos, min(n, pos + L)))
                blocks.append(blk)
                pos += L + rng.integers(0, 3)
            if len(blocks) >= 2:
                break
        bsites = [i for b in blocks for i in b]
        margB = ch.marginal(bsites)                               # array over block sites
        shapeB = margB.shape
        NB = margB.size
        idxB = np.indices(shapeB).reshape(len(bsites), -1)
        posB = {s: r for r, s in enumerate(bsites)}
        prod = np.ones(NB)
        for b in blocks:
            mb = ch.marginal(b)
            prod *= mb[tuple(idxB[posB[s]] for s in b)]
        lnrho = []
        dens = np.ones(NB)
        for j in range(len(blocks) - 1):
            e = blocks[j][-1]; s = blocks[j + 1][0]
            pe = ch.marginal([e]); ps = ch.marginal([s]); pes = ch.marginal([e, s])
            r = pes / (pe[:, None] * ps[None, :])
            lnrho.append(np.log(r))
            dens *= r[idxB[posB[e]], idxB[posB[s]]]
        stats["L_marg"] = max(stats["L_marg"], np.abs(margB.reshape(-1) - prod * dens).max())
        dsB = [ds[s] for s in bsites]
        DB = dist_matrix(idxB, dsB)
        lo = sum(l.min() for l in lnrho); hi = sum(l.max() for l in lnrho)
        # projection of the full space onto the block sites
        proj = np.ravel_multi_index(tuple(ch.idx[s] for s in bsites), shapeB)
        for psiB in random_members(DB, 12):
            psi = psiB[proj]
            assert violation(psi, D) < TOL                          # member of C_d ignoring gaps
            diff = lnA(ch.pi, psi) - lnA(prod, psiB)
            stats["L_cases"] += 1
            if diff < lo - 1e-10 or diff > hi + 1e-10:
                stats["L_viol"] += 1
            stats["L_tight"] = min(stats["L_tight"], min(diff - lo, hi - diff))
        # (L'): reduced envelope
        dminus = [d.copy() for d in dsB]
        for j in range(len(blocks) - 1):
            e = blocks[j][-1]; s = blocks[j + 1][0]
            l = lnrho[j]
            em = (l[:, None, :] - l[None, :, :]).max(axis=2)       # eps^-_j(a,a') = max_b
            ep = (l[:, :, None] - l[:, None, :]).max(axis=0)       # eps^+_j(b,b') = max_a
            dminus[posB[e]] = dminus[posB[e]] - em
            dminus[posB[s]] = dminus[posB[s]] - ep
        cl = [closure(d) for d in dminus]
        if any(np.diag(c).min() < -1e-12 for c in cl):
            stats["Lp_skipped"] += 1                                # class empty (negative cycle)
        else:
            if any(c.min() < -1e-12 for c in cl):
                stats["Lp_negentry_cases"] += 1
            Dm = dist_matrix(idxB, cl)
            corr = np.zeros(ch.N)
            for j in range(len(blocks) - 1):
                e = blocks[j][-1]; s = blocks[j + 1][0]
                corr += lnrho[j][ch.idx[e], ch.idx[s]]
            for psiB in random_members(Dm, 12):
                # members of the d- class: by construction of random_members w.r.t. Dm
                assert violation(psiB, Dm) < TOL
                psi = psiB[proj] + corr
                stats["Lp_adm"] = max(stats["Lp_adm"], violation(psi, D))
                stats["Lp_id"] = max(stats["Lp_id"], abs(lnA(ch.pi, psi) - lnA(prod, psiB)))
                stats["Lp_cases"] += 1
            for psiB in random_members(DB, 12):
                psi = psiB[proj] + corr
                stats["Lp_ctrl_cases"] += 1
                if violation(psi, D) > 1e-9:
                    stats["Lp_ctrl_viol"] += 1
        chains.append((qs, sdJ))

print("chains: %d  (alphabets: %s)" % (len(chains), sorted(set(tuple(c[0]) for c in chains))))
print("(U)  pi = rho e^-g / Z:  max abs dev %.2e" % stats["U_pi"])
print("(U)  identity ln A_pi(psi) = ln A_rho(psi+g) - ln A_rho(g):  %d cases, max dev %.2e" % (stats["U_cases"], stats["U_id"]))
print("(U)  psi+g in C_{d+}: largest violation %.2e" % stats["U_adm"])
print("(U)  d+ attained: largest slack left by the best cone over all slack sites and letter pairs %.2e" % stats["U_attain"])
print("(U)  control psi+g in C_d: violated in %d of %d" % (stats["U_ctrl_viol"], stats["U_cases"]))
print("(L)  marginal = (x) pi_B * prod rho_j: max abs dev %.2e" % stats["L_marg"])
print("(L)  two-sided bound: %d cases, %d violations, smallest margin %.3e" % (stats["L_cases"], stats["L_viol"], stats["L_tight"]))
print("(L') psi in C_d: largest violation %.2e;  A_pi(psi) = A_(x)(psi'): max dev %.2e;  %d cases (%d chains skipped: class empty; %d chains with negative entries of d- but nonempty class)"
      % (stats["Lp_adm"], stats["Lp_id"], stats["Lp_cases"], stats["Lp_skipped"], stats["Lp_negentry_cases"]))
print("(L') control psi' in C_{d_B}: violated in %d of %d" % (stats["Lp_ctrl_viol"], stats["Lp_ctrl_cases"]))
print("time %.1fs" % (time.time() - t0))
