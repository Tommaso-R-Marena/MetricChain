"""
T7 — a chain-molecule landscape: rotational-isomeric-state (RIS) chain on the diamond lattice.

n torsions with states (t, g+, g-); X = {0,1,2}^n minus self-overlapping conformations; single-site move =
change of one torsion state (a 120-degree bond rotation, the tail follows: the natural move of the
programme's torsion-space setting).  Energy:
    E = e_g * #gauche  -  eps * #contacts,   contact = pair of atoms >= 3 bonds apart at squared
    lattice distance <= S_c;  overlaps are forbidden (removed from the state space).
The energy is NOT pairwise in the torsion coordinates (lever arm), so this tests the theorems and the
cut families on a landscape of the kind the programme cares about, not the kernels.

 (1) landscape statistics: feasible states, strict local minima, depths (exact merge-tree quantities);
 (2) fraction of each depth certified by box / sphere / count cuts (as T4), and by the natural
     chain coordinate q = number of contacts (wall = slab, because a move changes q by more than 1);
 (3) rates for the deepest non-global trap: lambda_A, TST cut bound, gap bound, capacity bracket;
 (4) robust height interval under a per-torsion weighted Hamming envelope vs sup-norm stability.

Run:  OMP_NUM_THREADS=1 python3 t7_chain.py
"""
import itertools
import numpy as np
from kcore import (barrier_from, component_below, outer_boundary, generator, gibbs, conductances,
                   spectral_gap, dirichlet_eig, capacity, minimax_path, local_minima)

A4 = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])


def build_chain(states):
    """positions of the atoms for a tuple of torsion states (0=t,1=g+,2=g-)."""
    n = len(states)
    ks = [0, 1]
    bonds = [A4[0], -A4[1]]
    for i, s in enumerate(states):
        j = i + 2
        sign = 1 if j % 2 == 0 else -1
        if s == 0:
            k = ks[j - 2]
        else:
            cands = sorted({0, 1, 2, 3} - {ks[j - 1], ks[j - 2]})
            dets = [np.linalg.det(np.array([bonds[j - 2], bonds[j - 1], sign * A4[c]])) for c in cands]
            plus = cands[0] if dets[0] > 0 else cands[1]
            minus = cands[1] if dets[0] > 0 else cands[0]
            k = plus if s == 1 else minus
        ks.append(k)
        bonds.append(sign * A4[k])
    pos = np.zeros((len(bonds) + 1, 3), dtype=np.int64)
    for j, b in enumerate(bonds):
        pos[j + 1] = pos[j] + b
    return pos


class ChainSpace:
    """feasible RIS conformations with the single-torsion move graph (duck-types kcore.Space)."""

    def __init__(self, n, e_g=0.5, eps=1.0, s_cut=8):
        self.n = n
        self.ks = [3] * n
        allcfg = list(itertools.product(range(3), repeat=n))
        index = {}
        cfg, E, ncont = [], [], []
        for x in allcfg:
            pos = build_chain(x)
            d2 = ((pos[:, None, :] - pos[None, :, :]) ** 2).sum(axis=2)
            m = len(pos)
            iu = np.triu_indices(m, 3)
            dd = d2[iu]
            if (dd == 0).any():
                continue
            c = int((dd <= s_cut).sum())
            index[x] = len(cfg)
            cfg.append(x)
            ncont.append(c)
            E.append(e_g * sum(1 for s in x if s != 0) - eps * c)
        self.cfg = np.array(cfg, dtype=np.int64)
        self.N = len(cfg)
        self.E = np.array(E)
        self.ncont = np.array(ncont)
        self.nbrs, self.nbr_site = [], []
        for u, x in enumerate(cfg):
            l, ls = [], []
            for i in range(n):
                for s in range(3):
                    if s != x[i]:
                        y = x[:i] + (s,) + x[i + 1:]
                        if y in index:
                            l.append(index[y])
                            ls.append(i)
            self.nbrs.append(np.array(l, dtype=np.int64))
            self.nbr_site.append(np.array(ls, dtype=np.int64))
        self.nfull = 3 ** n

    def hamming_env(self, c):
        c = np.asarray(c, dtype=float)
        D = np.zeros((self.N, self.N))
        for i in range(self.n):
            col = self.cfg[:, i]
            D += c[i] * (col[:, None] != col[None, :])
        return D


def exit_target(S, E, a):
    Ba = barrier_from(S, E, a)
    lower = np.nonzero(E < E[a])[0]
    if len(lower) == 0:
        return None, None
    best = Ba[lower].min()
    cands = lower[Ba[lower] <= best + 1e-12]
    return int(cands[np.argmin(E[cands])]), best


def cut_families(S, E, a, b, B):
    H = B - E[a]
    diff = S.cfg[a] != S.cfg[b]
    neq = S.cfg != S.cfg[a][None, :]
    best = dict(box=0.0, sphere=0.0, count=0.0)
    for Imask in range(1, 2 ** S.n):
        I = np.array([(Imask >> i) & 1 for i in range(S.n)], dtype=bool)
        if not (I & diff).any():
            continue
        q = neq[:, I].sum(axis=1)
        qb = int((I & diff).sum())
        for r in range(1, qb + 1):
            lev = q == r
            # wall = level set {q_I = r} within the feasible space (a path must still cross it)
            val = (E[lev].min() - E[a]) if lev.any() else np.inf
            val = min(val, H) if np.isinf(val) else val
            best["count"] = max(best["count"], val)
            if r == 1:
                best["box"] = max(best["box"], val)
            if I.all():
                best["sphere"] = max(best["sphere"], val)
    # contact-number coordinate: S = {x : ncont(x) > theta} (a has more contacts than the wall), exact outer boundary
    best["contacts"] = 0.0
    for theta in range(int(S.ncont.min()), int(S.ncont[a])):
        mask = S.ncont > theta
        if not mask[a] or mask[b]:
            continue
        ob = outer_boundary(S, mask)
        if ob.any():
            best["contacts"] = max(best["contacts"], E[ob].min() - E[a])
    # the same with the component of a inside {ncont > theta} (a connected piece of the level set)
    best["contacts_comp"] = 0.0
    for theta in range(int(S.ncont.min()), int(S.ncont[a])):
        mask = S.ncont > theta
        comp = np.zeros(S.N, dtype=bool)
        comp[a] = True
        stack = [a]
        while stack:
            u = stack.pop()
            for v in S.nbrs[u]:
                if mask[v] and not comp[v]:
                    comp[v] = True
                    stack.append(int(v))
        if comp[b]:
            continue
        ob = outer_boundary(S, comp)
        if ob.any():
            best["contacts_comp"] = max(best["contacts_comp"], E[ob].min() - E[a])
    return H, best


def main():
    rng = np.random.default_rng(1)
    for n in (6, 7, 8):
        S = ChainSpace(n)
        E = S.E
        mins = local_minima(S, E, strict=False)
        # strict minima in the sense "no neighbour with lower or equal energy" are rare on a lattice
        # (degenerate energies); use non-strict minima and depths w.r.t. strictly lower states
        print(f"T7 RIS diamond chain, n={n} torsions ({n+3} atoms): {S.N} feasible of {S.nfull} conformations; "
              f"E in [{E.min():.1f}, {E.max():.1f}]; {len(mins)} (non-strict) local minima; "
              f"ground-state degeneracy {(E == E.min()).sum()}")
        rows = []
        for a in mins:
            b, B = exit_target(S, E, a)
            if b is None:
                continue
            if B - E[a] <= 1e-9:
                continue
            H, best = cut_families(S, E, a, b, B)
            rows.append((H, a, b, best))
        if not rows:
            print("   no trap with positive depth")
            continue
        Hs = np.array([r[0] for r in rows])
        print(f"   traps with positive depth: {len(rows)}; depths: min {Hs.min():.2f} median {np.median(Hs):.2f} "
              f"max {Hs.max():.2f}")
        for fam in ("box", "sphere", "count", "contacts", "contacts_comp"):
            v = np.array([max(min(r[3][fam], r[0]), 0.0) for r in rows]) / Hs
            print(f"   {fam:14s}: mean fraction of depth certified {v.mean():.2f}; exact in {np.mean(v > 1 - 1e-9):.0%}")
        # ---- (3) rates for the deepest trap
        H, a, b, best = max(rows, key=lambda r: r[0])
        lab = lambda u: "".join("tpm"[int(s)] for s in S.cfg[u])     # t, g+ (p), g- (m)
        print(f"   deepest trap: a={lab(a)} E={E[a]:.1f} contacts={S.ncont[a]}  ->  b={lab(b)} "
              f"E={E[b]:.1f}; depth {H:.2f}; d_H(a,b)={(S.cfg[a] != S.cfg[b]).sum()}")
        if S.N <= 2500:
            for beta in (1.0, 2.0, 4.0):
                Q = generator(S, E, beta)
                pi = gibbs(E, beta)
                C = conductances(Q, pi)
                A = component_below(S, E, a, E[a] + H, strict=True)
                piA = pi[A].sum()
                Qf = C[np.ix_(A, ~A)].sum()
                lam = dirichlet_eig(Q, pi, A)[0]
                gap, _ = spectral_gap(Q, pi)
                ma = np.zeros(S.N, dtype=bool); ma[a] = True
                mb = np.zeros(S.N, dtype=bool); mb[b] = True
                cap, h = capacity(Q, pi, ma, mb)
                P, _ = minimax_path(S, E, a, b)
                R = sum(1.0 / C[u, v] for u, v in zip(P[:-1], P[1:]))
                print(f"     beta={beta}: |A|={A.sum()} pi(A)={piA:.2e} lambda_A={lam:.3e} lam/k_cut={lam / (Qf / piA):.3f} "
                      f"gap/gap_cut={gap / (Qf / (piA * (1 - piA))):.3f} cap/cut={cap / Qf:.3f} "
                      f"1path/cap={(1 / R) / cap:.3f}  -(1/beta)ln lambda_A={-np.log(lam) / beta:.2f}")
        # ---- (4) robust interval for this trap under a per-torsion envelope
        for cval in (0.1, 0.3):
            c = np.full(S.n, cval)
            D = S.hamming_env(c)
            lo = barrier_from(S, E - D[a, :], a)[b] - E[a]
            hi = barrier_from(S, E + D[:, a], a)[b] - E[a]
            print(f"   robust height of the deepest trap, envelope c_i={cval}: [{lo:.2f}, {hi:.2f}] around {H:.2f}; "
                  f"sup-norm stability interval [{H - c.sum():.2f}, {H + c.sum():.2f}]")


if __name__ == "__main__":
    main()
