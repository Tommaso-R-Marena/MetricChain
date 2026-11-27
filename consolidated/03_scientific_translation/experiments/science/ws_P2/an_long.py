"""
Chains too long for exact enumeration: what can be said exactly, and what only as a lower bound.

usage: python3 -B an_long.py SEQ BB TAU [--grid R3] [--tag NAME]

Domain: the pruned PRODUCT domain X' (states whose one-site clash score exceeds TAU, minus a
greedy set of states involved in two-site clashes; the same rule as an_main.pruned_product).

(1) Pair-additive residuals (ff03 - ff14SB, ff15ipq - ff14SB, and the known part f): the tables
    h_i, J_ij are exact, so on X
        c_ij = max over state quadruples of |J_ij(a,b) - J_ij(a',b) - J_ij(a,b') + J_ij(a',b')|
        c_i  = max_{a,b} [ h_i(a) - h_i(b) + sum_{j != i} max_t (J_ij(a,t) - J_ij(b,t)) ]
    are EXACT for every chain length (the maximum over the other sites decomposes).
(2) GBn2 (not pair-additive): the anchored order-2 expansion at a reference assignment x0
    (GB at x0, at all single flips and all double flips: 1 + sum(k_i - 1) + sum_{i<j}(k_i-1)(k_j-1)
    exact evaluations) gives
      * c_ij^LB = max mixed second difference with all other sites at x0  <= c_ij(GB)   [rigorous lower bound]
      * the same formula as in (1) applied to the expansion: c_i^(2) (exact for the pairwise
        surrogate), together with the assignment pair that realises it; the TRUE GB difference at
        that pair is a rigorous lower bound c_i^LB <= c_i(GB), and |c_i^(2) - c_i^LB| measures the
        non-pairwise part there;
      * third-order mixed differences for the triples among the five central sites (other sites
        at x0): lower bounds on c_ijk.
Output: out/long_<tag>.json
"""
import sys, os, json, time, math, itertools
import numpy as np
from anlib import HERE, KT300, BETA
from fbmodel import FBModel, BACKBONES
from enum_fb import expand_seq

np.set_printoptions(precision=3, suppress=True, linewidth=250)


def mixed2(T):
    """max |T[a,b] - T[a',b] - T[a,b'] + T[a',b']| over all a, a', b, b'."""
    ka, kb = T.shape
    ia, ja = np.triu_indices(ka, 1)
    ib, jb = np.triu_indices(kb, 1)
    if len(ia) == 0 or len(ib) == 0:
        return 0.0
    D = T[ia] - T[ja]                      # (Pa, kb)
    return float(np.abs(D[:, ib] - D[:, jb]).max())


def pairwise_constants(h, J, ns):
    """exact c_i and c_ij of the function sum h_i + sum J_ij on the product domain; also the
    maximising (i, a, b, x_rest)."""
    Jm = {}
    for (i, j), T in J.items():
        Jm[(i, j)] = T; Jm[(j, i)] = T.T
    C = np.zeros((ns, ns))
    for (i, j), T in J.items():
        C[i, j] = C[j, i] = mixed2(T)
    c = np.zeros(ns); arg = []
    for i in range(ns):
        ki = len(h[i])
        best = (-1.0, None)
        for a in range(ki):
            for b in range(ki):
                if a == b:
                    continue
                val = h[i][a] - h[i][b]
                rest = {}
                for j in range(ns):
                    if j == i:
                        continue
                    dlt = Jm[(i, j)][a] - Jm[(i, j)][b]
                    t = int(np.argmax(dlt)); val += dlt[t]; rest[j] = t
                if val > best[0]:
                    best = (val, (a, b, rest))
        c[i] = max(best[0], 0.0); arg.append(best[1])
    return c, C, arg


def icm(c0, h, J, ns, k, rng, restarts=30):
    Jm = {}
    for (i, j), T in J.items():
        Jm[(i, j)] = T; Jm[(j, i)] = T.T
    def energy(x):
        e = c0 + sum(h[i][x[i]] for i in range(ns))
        for (i, j), T in J.items():
            e += T[x[i], x[j]]
        return e
    best = None
    for r in range(restarts):
        x = [int(np.argmin(h[i])) for i in range(ns)] if r == 0 else [int(rng.integers(0, k[i])) for i in range(ns)]
        changed = True
        while changed:
            changed = False
            for i in range(ns):
                loc = h[i].copy()
                for j in range(ns):
                    if j != i:
                        loc += Jm[(i, j)][:, x[j]]
                s = int(np.argmin(loc))
                if loc[s] < loc[x[i]] - 1e-12:
                    x[i] = s; changed = True
        e = energy(x)
        if best is None or e < best[0] - 1e-12:
            best = (e, list(x))
    return best


def main():
    a = sys.argv[1:]
    seqarg, bb, tau = a[0], a[1], float(a[2])
    grid = a[a.index("--grid") + 1] if "--grid" in a else "R3"
    tag = a[a.index("--tag") + 1] if "--tag" in a else f"{seqarg.replace(':', 'c').replace('*', 'x')}_{bb}_{grid}_t{tau:.2f}"
    do_gb = "--nogb" not in a
    seq = expand_seq(seqarg)
    t0 = time.time()
    Mdl = FBModel(seq, bb, grid=grid, extra_ffs=("ff03", "ff15ipq"))
    dom = Mdl.domain(tau)
    ns = Mdl.ns; k_raw = [len(dm) for dm in dom]
    # prune to a pair-clash-free product (same greedy rule as an_main.pruned_product)
    bad = {key: (tab[np.ix_(dom[key[0]], dom[key[1]])] <= tau) for key, tab in Mdl.s2.items()}
    bad = {key: b for key, b in bad.items() if b.any()}
    keep = [np.ones(len(dm), dtype=bool) for dm in dom]
    while bad:
        deg = [np.zeros(len(dm)) for dm in dom]
        for (i, j), b in bad.items():
            bb_ = b & keep[i][:, None] & keep[j][None, :]
            deg[i] += bb_.sum(1); deg[j] += bb_.sum(0)
        best = None
        for i in range(ns):
            for s_ in np.flatnonzero(deg[i] > 0):
                key = (-deg[i][s_], Mdl.s1[i][dom[i][s_]], i, s_)
                if best is None or key < best:
                    best = key
        if best is None:
            break
        keep[best[2]][best[3]] = False
    dom = [dm[kp] for dm, kp in zip(dom, keep)]
    k = [len(dm) for dm in dom]
    print(f"=== {seqarg} = {seq} on {bb}, grid {grid}, tau {tau}: atoms {Mdl.P.natoms}, sites {ns}, one-site domain sizes {k_raw}; "
          f"pruned pair-clash-free product X': {k}", flush=True)
    out = dict(seq=seq, bb=bb, grid=grid, tau=tau, k=k, k_raw=k_raw, natoms=Mdl.P.natoms)
    if min(k) == 0:
        print("EMPTY domain"); return
    P = Mdl.P
    cb = np.array([Mdl.X0[P.idx[(kk, "CB")]] for kk in Mdl.sites])
    out["cb_dist"] = np.sqrt(((cb[:, None] - cb[None]) ** 2).sum(-1)).tolist()

    def sub(tabs):
        c0, h, J = tabs
        return c0, [h[i][dom[i]] for i in range(ns)], {(i, j): T[np.ix_(dom[i], dom[j])] for (i, j), T in J.items()}

    f_t = sub(Mdl.site_tables("ff14SB"))
    rng = np.random.default_rng(7)
    # pair-clash statistics of the product domain
    npc = {key: float((tab[np.ix_(dom[key[0]], dom[key[1]])] <= tau).mean()) for key, tab in Mdl.s2.items()}
    out["pair_clash_fraction_max"] = max(npc.values()) if npc else 0.0
    # ---- (1) exact constants of the pair-additive functions
    for name in ("f", "ff03-ff14SB", "ff15ipq-ff14SB"):
        if name == "f":
            c0, h, J = f_t
        else:
            ff = name.split("-")[0]
            g_t = sub(Mdl.site_tables(ff))
            c0 = g_t[0] - f_t[0]
            h = [g_t[1][i] - f_t[1][i] for i in range(ns)]
            J = {key: g_t[2][key] - f_t[2][key] for key in f_t[2]}
        c, C, arg = pairwise_constants(h, J, ns)
        half = 0.5 * C.sum(1); dob = np.tanh(BETA * C / 4).sum(1)
        bysep = [float(max(C[i, i + s] for i in range(ns - s))) for s in range(1, ns)]
        out[name] = dict(c=c.tolist(), half_rowsum=half.tolist(), dobrushin=dob.tolist(), bysep=bysep, C=C.tolist() if ns <= 24 else None)
        print(f"--- {name} (pair-additive: EXACT on the product domain)\n    c_i = {c}\n    max c_i {c.max():.3f} kcal/mol = {c.max()*BETA:.1f} kT; "
              f"half row sums: max {half.max():.3f}, min {half.min():.3f}; Dobrushin-type sums max {dob.max():.3f}\n    max c_ij by separation: {np.array(bysep)}", flush=True)
    # candidate minimiser of f (ICM, 30 restarts; not certified)
    ef, xf = icm(f_t[0], f_t[1], f_t[2], ns, k, rng)
    out["x_icm_f"] = xf
    if not do_gb:
        json.dump(out, open(os.path.join(HERE, "out", f"long_{tag}.json"), "w"), indent=0); return
    # ---- (2) GB: anchored order-2 expansion at x0 = ICM minimiser of f
    x0 = np.array([dom[i][xf[i]] for i in range(ns)])
    nev = 0
    g0 = float(Mdl.gb_energy(x0[None])[0]); nev += 1
    a1 = []
    for i in range(ns):
        st = np.repeat(x0[None], k[i], 0); st[:, i] = dom[i]
        a1.append(Mdl.gb_energy(st) - g0); nev += k[i]
    A2 = {}
    t1 = time.time()
    for i in range(ns):
        for j in range(i + 1, ns):
            st = np.repeat(x0[None], k[i] * k[j], 0)
            st[:, i] = np.repeat(dom[i], k[j]); st[:, j] = np.tile(dom[j], k[i])
            A2[(i, j)] = Mdl.gb_energy(st).reshape(k[i], k[j]) - g0 - a1[i][:, None] - a1[j][None, :]
            nev += k[i] * k[j]
        if i % 4 == 0:
            print(f"    GB double flips: site {i + 1}/{ns}  {time.time() - t1:.0f}s", flush=True)
    c2, C, arg = pairwise_constants(a1, A2, ns)
    half = 0.5 * C.sum(1); dob = np.tanh(BETA * C / 4).sum(1)
    bysep = [float(max(C[i, i + s] for i in range(ns - s))) for s in range(1, ns)]
    # true GB differences at the maximising pairs: rigorous lower bounds on c_i
    lb = np.zeros(ns); star = np.zeros(ns); clash_ok = []
    for i in range(ns):
        a_, b_, rest = arg[i]
        xa = x0.copy(); xb = x0.copy()
        for j, t in rest.items():
            xa[j] = dom[j][t]; xb[j] = dom[j][t]
        xa[i] = dom[i][a_]; xb[i] = dom[i][b_]
        ga, gb_ = Mdl.gb_energy(np.stack([xa, xb]))
        lb[i] = abs(ga - gb_); nev += 2
        star[i] = float(a1[i].max() - a1[i].min())
        clash_ok.append(bool(min(Mdl.clash_of(np.stack([xa, xb]))) > tau))
    out["GB"] = dict(c_pairwise_surrogate=c2.tolist(), c_lower_bound=lb.tolist(), c_at_reference=star.tolist(),
                     C_lower_bound=C.tolist() if ns <= 24 else None, half_rowsum_lb=half.tolist(), dobrushin_lb=dob.tolist(),
                     bysep_lb=bysep, evaluations=nev, maximiser_pairclashfree=clash_ok, x0=[int(v) for v in xf])
    print(f"--- GB: anchored order-2 expansion at the ICM minimiser of f ({nev} exact GB evaluations, {time.time()-t0:.0f}s)")
    print(f"    c_i at the reference background (star)      = {star}")
    print(f"    c_i of the pairwise surrogate (exact for it) = {c2}")
    print(f"    TRUE GB difference at the surrogate's maximising pair = rigorous lower bound on c_i(GB) = {lb}")
    print(f"    max: surrogate {c2.max():.3f}, lower bound {lb.max():.3f} kcal/mol ({lb.max()*BETA:.1f} kT); max |surrogate - true| at these pairs {np.abs(c2-lb).max():.4f}; "
          f"maximising pairs free of pair clashes: {sum(clash_ok)} of {ns}")
    print(f"    lower bounds on c_ij (others at x0): max by separation = {np.array(bysep)}")
    print(f"    half row sums of these lower bounds: max {half.max():.3f}, min {half.min():.3f}, by site {half}; Dobrushin-type sums max {dob.max():.3f}", flush=True)
    # excitation energies of E = f + GB at the ICM minimiser of the surrogate energy f + g2
    hE = [f_t[1][i] + a1[i] for i in range(ns)]
    JE = {key: f_t[2][key] + A2[key] for key in A2}
    eE, xE = icm(f_t[0] + g0, hE, JE, ns, k, rng)
    Jm = {}
    for (i, j), T in JE.items():
        Jm[(i, j)] = T; Jm[(j, i)] = T.T
    exc = []
    for i in range(ns):
        loc = hE[i].copy()
        for j in range(ns):
            if j != i:
                loc += Jm[(i, j)][:, xE[j]]
        d_ = np.delete(loc - loc[xE[i]], xE[i])
        exc.append(float(d_.min()) if d_.size else float("inf"))
    exc = np.array(exc)
    out["GB"].update(x_icm_E=[int(v) for v in xE], excitation_surrogate=exc.tolist(),
                     rowsum_fails_at=int((half > exc + 1e-12).sum()))
    print(f"    candidate minimiser of f + (pairwise surrogate of GB) by ICM: single-site excitation energies {exc}")
    print(f"    row-sum condition with the LOWER BOUNDS on c_ij: violated at {int((half > exc + 1e-12).sum())} of {ns} sites "
          f"(a violation with lower bounds is a violation with the true constants); ratio half-row-sum/excitation: max {np.max(half/np.maximum(exc,1e-9)):.2f}, median {np.median(half/np.maximum(exc,1e-9)):.2f}")
    # third-order lower bounds for the triples among the five central sites
    mid = ns // 2
    win = [s for s in range(mid - 2, mid + 3) if 0 <= s < ns]
    c3 = {}
    for (i, j, l) in itertools.combinations(win, 3):
        if k[i] * k[j] * k[l] > 30000:
            continue
        st = np.repeat(x0[None], k[i] * k[j] * k[l], 0)
        gi, gj, gl = np.meshgrid(dom[i], dom[j], dom[l], indexing="ij")
        st[:, i] = gi.ravel(); st[:, j] = gj.ravel(); st[:, l] = gl.ravel()
        G = Mdl.gb_energy(st).reshape(k[i], k[j], k[l]); nev += st.shape[0]
        best = 0.0
        ii, ij = np.triu_indices(k[i], 1); ji, jj = np.triu_indices(k[j], 1); li, lj = np.triu_indices(k[l], 1)
        if len(ii) and len(ji) and len(li):
            D = G[ii] - G[ij]; D = D[:, ji] - D[:, jj]; D = D[:, :, li] - D[:, :, lj]
            best = float(np.abs(D).max())
        c3[f"{i},{j},{l}"] = best
    out["GB"]["c3_central_lb"] = c3
    if c3:
        print(f"    third-order mixed differences, triples among the central sites {win} (others at x0), lower bounds on c_ijk: max {max(c3.values()):.4f} kcal/mol; "
              + " ".join(f"({kk}): {v:.4f}" for kk, v in c3.items()))
    out["seconds"] = time.time() - t0
    json.dump(out, open(os.path.join(HERE, "out", f"long_{tag}.json"), "w"), indent=0)
    print(f"    [{time.time()-t0:.0f}s] -> out/long_{tag}.json")


if __name__ == "__main__":
    main()
