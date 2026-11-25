"""w06: brute force on full product spaces.

Part A (W5: validation of the exact joint-type sums of wfin.py)
   A1  one ternary site type (path), n = 8 (6561 points), two label blocks;
   A2  two site types (binary + ternary path), n = 4 + 4 (1296 points), four label blocks;
   A3  one ternary site type with an ASYMMETRIC envelope, n = 7 (2187 points).
   For each: the table N[P, c] against a direct count; for the additive instance gamma* and for the flat-histogram
   instance H: Phi(y) = min_{x in C}[d(y,x) - psi(y) + psi(x)], admissibility of the generalised dip,
   its effect on ln A, the density of its support in every joint-type class, and the deepest dip on the
   same support -- against DipTable.
Part B (W1/W6: what symmetry alone gives; two site types, both envelopes asymmetric, 3 + 3 sites, 216 points)
   B1  orbits = joint types, their number; the quotient envelope is the transport cost;
   B2  truncation at orbit-wise quantiles stays in the class, orbit density <= q (random members);
   B3  dips of invariant instances: A(psi^D)/A(psi) = 1 + Phi(D), formula with the landscape; Lambda_g <= V;
       Z_g Phi_g^+(D) <= Z_H Phi_H^+(D) (random instances, random sets);
   B4  fibre averages are admissible for the outer envelope; tail lemma relative to the reference H in the
       orientation s(y -> x), and its violation with the wrong orientation (mutation).
"""
import itertools
import math
import sys
import time

import numpy as np

from wlib import *
from wfin import *
from wsites import *

t00 = time.time()
rng = np.random.default_rng(7)
np.set_printoptions(precision=5, suppress=True, linewidth=150)


def space(seq):
    X = np.array(list(itertools.product(*[range(s.q) for s in seq])), dtype=np.int64)
    lpi = sum(np.log(s.pi)[X[:, i]] for i, s in enumerate(seq))
    D = sum(s.d[X[:, i][:, None], X[:, i][None, :]] for i, s in enumerate(seq))    # D[x, y] = d(x, y)
    return X, np.exp(lpi), D


def admissible(psi, D, tol=1e-9):
    return bool(np.all(psi[:, None] - psi[None, :] <= D + tol))


def counts(X, pos, q):
    return np.stack([(X[:, pos] == a).sum(axis=1) for a in range(q)], axis=1)


# ============================================================================================================
print("=== w06 Part A: exact joint-type sums of wfin.py against brute force ===")


def partA(name, chain, sizes_per_type, e_frac, positions=None):
    """chain: Chain; sizes_per_type[j] = number of sites of type j; blocks from the generalised-dip profile at e"""
    from wprimal import dip_profile
    E = chain.E()
    e = e_frac * E
    R, ts = chain.R(e, return_t=True)
    prof, phis, Ms, gam = dip_profile(chain, ts)
    # sequence of site types: type 0 first, then type 1 (any fixed order would do)
    seq, typ = [], []
    for j, s in enumerate(chain.sites):
        seq += [s] * sizes_per_type[j]
        typ += [j] * sizes_per_type[j]
    typ = np.array(typ)
    X, pi, D = space(seq)
    n = len(seq)
    parts, blocks_pos, centre = [], [], []
    pos0 = 0
    for j, s in enumerate(chain.sites):
        nj = sizes_per_type[j]
        sz = round_counts(nj, prof.P[j])
        p = Part(s, sz, unit=0.1)
        blks = []
        pp = pos0
        for u, nu in enumerate(sz):
            m_u = round_counts(int(nu), prof.mu[j][u])
            K, c = p.transport_costs(int(nu), m_u)
            blks.append((K, c))
            blocks_pos.append((j, list(range(pp, pp + int(nu))), m_u))
            pp += int(nu)
        cmax = int(round(nj * s.d.max() / 0.1)) + 1
        p.build(blks, cmax)
        parts.append(p)
        pos0 += nj
    # the centre class C and the brute-force transport cost
    inC = np.ones(len(X), bool)
    for (j, pos, m_u) in blocks_pos:
        inC &= np.all(counts(X, pos, chain.sites[j].q) == m_u[None, :], axis=1)
    Cidx = np.nonzero(inC)[0]
    cost = D[:, Cidx].min(axis=1)                       # min_{x in C} d(y, x)
    # joint types per part
    typeidx = []
    for j, p in enumerate(parts):
        pos = np.nonzero(typ == j)[0]
        typeidx.append(counts(X, pos, p.q) @ p.stride)
    # A-i: table N against a direct count (the cost splits over the parts: recompute per part by brute force)
    worst = 0.0
    for j, p in enumerate(parts):
        pos = np.nonzero(typ == j)[0]
        sub = np.unique(X[:, pos], axis=0)
        subC = np.ones(len(sub), bool)
        off = 0
        for (jj, bpos, m_u) in blocks_pos:
            if jj != j:
                continue
            loc = [int(np.nonzero(pos == b)[0][0]) for b in bpos]
            subC &= np.all(counts(sub, loc, p.q) == m_u[None, :], axis=1)
        s = chain.sites[j]
        Dsub = sum(s.d[sub[:, i][:, None], sub[:, i][None, :]] for i in range(len(pos)))
        csub = np.rint(Dsub[:, subC].min(axis=1) / p.unit).astype(np.int64)
        tsub = counts(sub, list(range(len(pos))), p.q) @ p.stride
        Nb = np.zeros_like(p.N)
        np.add.at(Nb, (tsub, csub), 1.0)
        worst = max(worst, float(np.max(np.abs(Nb - p.N))))
    print(f"{name}: n = {n}, |X| = {len(X)}, |C| = {len(Cidx)}, e = {e_frac} E, t* = {ts:.4f}; table N[P,c] against direct count: max abs difference {worst:.1e}")
    # instances
    for inst in ("gamma*", "H"):
        deltas, lmasses = [], []
        psi = np.zeros(len(X))
        for j, p in enumerate(parts):
            if inst == "gamma*":
                g, lm = p.g_additive(gam[j])
            else:
                g, lm, lZ = p.g_flat()
            PC = sum(m_u for (jj, bpos, m_u) in blocks_pos if jj == j) @ p.stride
            deltas.append(g[PC] - g)
            lmasses.append(lm)
            psi += g[typeidx[j]]
        assert admissible(psi, D), "instance not in the class"
        w = pi * np.exp(-psi)
        A = w.sum()
        mu = w / A
        Phi = (D[:, Cidx] - psi[:, None] + psi[None, Cidx]).min(axis=1)
        assert Phi.min() > -1e-9
        dt = DipTable(parts, deltas, lmasses)
        worst_e = worst_d = 0.0
        gap_deep = []
        for r in np.linspace(0.3, 0.8 * Phi.max(), 9):
            eff_b = math.log(float(np.sum(mu * np.exp(np.maximum(r - Phi, 0.0)))))
            supp = Phi < r
            # densities per joint-type class
            key = typeidx[0] if len(parts) == 1 else typeidx[0] * parts[1].sizeP + typeidx[1]
            tot = np.bincount(key)
            ins = np.bincount(key, weights=supp.astype(float), minlength=len(tot))
            dens_b = float(np.max(ins[tot > 0] / tot[tot > 0]))
            eff_t = dt.effect(r)
            dens_t = dt.maxdens(r)[0]
            worst_e = max(worst_e, abs(eff_b - eff_t))
            worst_d = max(worst_d, abs(dens_b - dens_t))
            # the generalised dip is in the class, and the deepest dip on its support is at least as effective
            dip = psi - np.maximum(r - Phi, 0.0)
            assert admissible(dip, D)
            if supp.any() and not supp.all():
                out = ~supp
                deep = np.where(supp, np.max(psi[None, out] - D[np.ix_(out, np.arange(len(X)))].T, axis=1), psi)
                assert admissible(deep, D)
                eff_deep = math.log(float(np.sum(pi * np.exp(-deep))) / A)
                gap_deep.append(eff_deep - eff_b)
        print(f"   instance {inst:6s}: effect ln E exp((r-Phi)_+): max |brute - table| = {worst_e:.1e}; maxdens: max |brute - table| = {worst_d:.1e};"
              f" deepest dip on the same support minus generalised dip: min {min(gap_deep):+.2e}, max {max(gap_deep):+.2e} (>= 0)")


C = chains()
partA("A1", C["path"], [8], 0.0)
partA("A2", C["mix"], [4, 4], 0.2)
partA("A3", C["asym"], [7], 0.1)

# ============================================================================================================
print("\n=== w06 Part B: what symmetry alone gives (two site types, both envelopes asymmetric) ===")
sa = asym_site()
sb = Site([0.65, 0.35], [[0, 1.2], [0.4, 0]], "bin-asym")
seq = [sa, sb, sa, sb, sb, sa]                         # a fixed sequence of site types
typ = np.array([0, 1, 0, 1, 1, 0])
sites = [sa, sb]
X, pi, D = space(seq)
N = len(X)
tcounts = [counts(X, np.nonzero(typ == j)[0], sites[j].q) for j in range(2)]
key = tcounts[0] @ np.array([0, 1, 4]) * 4 + tcounts[1][:, 1]
orbs, orb = np.unique(key, return_inverse=True)
norb = len(orbs)
print(f"B1: |X| = {N}; orbits (joint types): {norb}; formula prod_j C(n_j+q_j-1, q_j-1) = {math.comb(5, 2) * math.comb(4, 1)}")
# every orbit is one orbit of the group (the multiset of letters per site type determines the orbit): by construction.
rep = [np.nonzero(orb == o)[0] for o in range(norb)]
Pj = [np.array([tcounts[j][rep[o][0]] for o in range(norb)]) for j in range(2)]
delta = np.zeros((norb, norb))
worst = 0.0
for o1 in range(norb):
    for o2 in range(norb):
        brute = D[np.ix_(rep[o1], rep[o2])].min()
        tr = sum(np.max((Pj[j][o1] - Pj[j][o2]) @ sites[j].V.T) for j in range(2))
        delta[o1, o2] = brute
        worst = max(worst, abs(brute - tr))
print(f"    quotient envelope min d(x,y) over orbits against the transport cost sum_j n_j W_dj: max abs difference {worst:.1e}"
      f" (asymmetric: max |delta - delta^T| = {np.max(np.abs(delta - delta.T)):.2f})")


def random_member():
    f = rng.normal(scale=rng.choice([0.5, 1.5, 4.0]), size=N)
    return np.min(f[None, :] + D, axis=1)               # psi(x) = min_y [f(y) + d(x,y)]


def orbit_dens(mask):
    return np.array([mask[rep[o]].mean() for o in range(norb)])


# B2: truncation at orbit-wise quantiles
viol = 0
maxd = 0.0
ntr = 0
for it in range(300):
    psi = random_member()
    assert admissible(psi, D)
    q = float(rng.choice([0.1, 0.25, 0.5, 0.8]))
    w = np.exp(-psi)
    t = np.zeros(N)
    for o in range(norb):
        vals = np.unique(w[rep[o]])
        # smallest value tau of w on the orbit with dens{w > tau} <= q
        for tau in vals:
            if np.mean(w[rep[o]] > tau) <= q + 1e-12:
                t[rep[o]] = tau
                break
    c = -np.log(t)
    ok_levels = bool(np.all(c[:, None] - c[None, :] <= D + 1e-9))
    tr = np.maximum(psi, c)
    ok_tr = admissible(tr, D)
    dd = orbit_dens(np.abs(tr - psi) > 1e-12).max()
    maxd = max(maxd, dd - q)
    viol += (not ok_levels) or (not ok_tr) or (dd > q + 1e-12)
    ntr += int(np.any(np.abs(tr - psi) > 1e-12))
print(f"B2: 300 random members: quantile levels admissible, truncation in the class, orbit density <= q: violations {viol};"
      f" (truncation non-trivial in {ntr} cases; largest density minus q: {maxd:+.3f})")

# B3: invariant instances, landscapes, the hardest invariant instance
J = np.array([-math.log(pi[rep[o]].sum()) for o in range(norb)])
Vn = np.min(J[:, None] + delta, axis=0)                 # V(P) = min_{P'} [J_{P'} + delta(P', P)]
psiH = -Vn[orb]
assert admissible(psiH, D)
ZH = float(np.sum(pi * np.exp(-psiH)) / math.exp(-0.0))
ZH = float(np.sum(np.exp(-(J - Vn))))
worst_form = 0.0
worst_c = -np.inf
worst_land = -np.inf
for it in range(200):
    f = rng.normal(scale=rng.choice([0.5, 2.0]), size=norb)
    g = np.min(f[None, :] + delta, axis=1)              # g(P) - g(P') <= delta(P, P')
    psi = g[orb]
    assert admissible(psi, D)
    cg = np.min(J + g)
    Lam = -g + cg
    worst_land = max(worst_land, float(np.max(Lam - Vn)))
    Zg = float(np.sum(np.exp(-(J - Lam))))
    A = float(np.sum(pi * np.exp(-psi)))
    mask = rng.random(N) < rng.choice([0.05, 0.2, 0.5])
    if mask.all() or not mask.any():
        continue
    out = ~mask
    deep = np.where(mask, np.max(psi[None, out] - D[np.ix_(out, np.arange(N))].T, axis=1), psi)
    assert admissible(deep, D)
    ratio = float(np.sum(pi * np.exp(-deep))) / A
    ins = np.nonzero(mask)[0]
    expo = np.min(D[np.ix_(out, ins)] + Lam[orb[out]][:, None], axis=0)      # min_{y not in D} [d(y,x) + Lam(P_y)]
    Phip_g = float(np.sum(pi[ins] * np.exp(expo))) / Zg
    mu_g = pi * np.exp(-psi) / A
    worst_form = max(worst_form, abs(ratio - (1 + Phip_g - mu_g[ins].sum())))
    expoH = np.min(D[np.ix_(out, ins)] + Vn[orb[out]][:, None], axis=0)
    Phip_H = float(np.sum(pi[ins] * np.exp(expoH))) / ZH
    worst_c = max(worst_c, Zg * Phip_g - ZH * Phip_H)
print(f"B3: 200 random invariant instances and sets: |A(psi^D)/A(psi) - (1 + Phi_g(D))| <= {worst_form:.1e};"
      f" max(Lambda_g - V) = {worst_land:+.1e} (<= 0); max[Z_g Phi_g^+(D) - Z_H Phi_H^+(D)] = {worst_c:+.1e} (<= 0); Z_H = {ZH:.3f} <= N_orb = {norb}")

# B4: fibre averages and the tail lemma relative to the reference H of the outer block
outer = [0, 1, 2, 3]                                     # outer block: types (0,1,0,1); inner: (1,0)
inner = [4, 5]
Xo, pio, Do = space([seq[i] for i in outer])
Xi, pii, Di = space([seq[i] for i in inner])
No, Ni = len(Xo), len(Xi)
# index of (a, b) in X: X is the product in site order 0..5, so index = a_index * Ni + b_index
typo = typ[outer]
tco = [counts(Xo, np.nonzero(typo == j)[0], sites[j].q) for j in range(2)]
keyo = tco[0] @ np.array([0, 1, 3]) * 3 + tco[1][:, 1]
orbso, orbo = np.unique(keyo, return_inverse=True)
repo = [np.nonzero(orbo == o)[0] for o in range(len(orbso))]
deltao = np.array([[Do[np.ix_(repo[a], repo[b])].min() for b in range(len(orbso))] for a in range(len(orbso))])
Jo = np.array([-math.log(pio[repo[o]].sum()) for o in range(len(orbso))])
Vo = np.min(Jo[:, None] + deltao, axis=0)
psiref = -Vo[orbo]
wref = np.exp(-psiref)
muref = pio * wref / np.sum(pio * wref)
S_right = Do.T - psiref[None, :] + psiref[:, None]      # S_right[x, y] = d(y, x) - psi_ref(y) + psi_ref(x)  (x inside, y outside)
S_wrong = Do - psiref[None, :] + psiref[:, None]        # the same with d(x, y): wrong orientation
viol_adm = viol_right = viol_wrong = 0
ntest = 0
for it in range(400):
    psi = random_member().reshape(No, Ni)
    Wf = (np.exp(-psi) * pii[None, :]).sum(axis=1)
    lw = -np.log(Wf)
    viol_adm += not bool(np.all(lw[:, None] - lw[None, :] <= Do + 1e-9))
    What = Wf / wref
    for t in np.unique(What)[:-1]:
        Dm = What > t
        ins, out = np.nonzero(Dm)[0], np.nonzero(~Dm)[0]
        lhs = float(np.sum(muref[ins] * (What[ins] - t)))
        rhs = t * float(np.sum(muref[ins] * (np.exp(S_right[np.ix_(ins, out)].min(axis=1)) - 1)))
        rhw = t * float(np.sum(muref[ins] * (np.exp(S_wrong[np.ix_(ins, out)].min(axis=1)) - 1)))
        viol_right += lhs > rhs * (1 + 1e-9) + 1e-12
        viol_wrong += lhs > rhw * (1 + 1e-9) + 1e-12
        ntest += 1
print(f"B4: 400 random members, outer block of 4 sites ({No} points, {len(orbso)} outer orbits), inner block of 2 sites:"
      f" fibre averages admissible for the outer envelope: violations {viol_adm};")
print(f"    tail lemma E_mu(What - t)_+ <= t Phi_ref({{What > t}}) at {ntest} levels: violations {viol_right};"
      f" with the wrong orientation of the slack (mutation): violations {viol_wrong}")
print(f"time {time.time()-t00:.1f} s")

# ============================================================================================================
print("\n=== w06 Part C: truncated generalised cones (w07) against brute force ===")
from w07_nonadaptive_finite import cone_table, xn_of_q
from wprimal import dip_profile
for cname, nC, ef in (("path", 8, 0.3), ("tri", 7, 0.1), ("asym", 8, 0.0)):
    chc = C[cname]
    sc = chc.sites[0]
    Rc, tsc = chc.R(ef * chc.E(), return_t=True)
    profc, phisc, _, _ = dip_profile(chc, tsc)
    p, sz, shift = cone_table(sc, nC, profc.P[0], phisc[0])
    f, F = p.dens_table()
    w = np.exp(-np.arange(p.C1) * p.unit)
    G = np.zeros_like(F)
    np.cumsum(f * w[None, :], axis=1, out=G[:, 1:])
    sup = np.where(f > 0, np.arange(p.C1)[None, :], -1)
    lastsup = np.maximum.accumulate(sup, axis=1)
    lpiT = p.lTP[p.Pidx] + p.Ptypes @ np.log(sc.pi)
    Xc, pic, Dc = space([sc] * nC)
    lab = np.repeat(np.arange(len(sz)), sz)
    psi = sum(phisc[0][lab[i]][Xc[:, i]] for i in range(nC))
    assert admissible(psi, Dc)
    wb = np.exp(-psi)
    keyc = counts(Xc, list(range(nC)), sc.q) @ p.stride
    worst = 0.0
    okc = True
    for q in (0.02, 0.05, 0.1, 0.2, 0.35, 0.5, 0.8):
        t = np.zeros(len(Xc))
        for k in np.unique(keyc):
            m = keyc == k
            for tau in np.unique(wb[m]):
                if np.mean(wb[m] > tau) <= q * (1 + 1e-12):
                    t[m] = tau
                    break
        tr = np.maximum(psi, -np.log(t))
        okc &= admissible(tr, Dc)
        xb = math.log(float(np.sum(pic * wb)) / float(np.sum(pic * np.exp(-tr))))
        xt, _ = xn_of_q(p, f, F, G, lastsup, w, lpiT, q)
        worst = max(worst, abs(xb - xt))
    print(f"C ({cname}, n = {nC}, {len(Xc)} points, blocks {sz.tolist()}): ln[A/A^tr] at 7 values of q: max |brute - table| = {worst:.1e}; truncations in the class: {okc}")
print(f"time {time.time()-t00:.1f} s")
