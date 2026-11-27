#!/usr/bin/env python3
"""The theory division's question (THY-RES-0015 section 4): are our charged head-to-head pairs in the regime
rho R^2 < 1 of its sign-blind lemma?

Their lemma.  For a bilinear form t = q_a^T M q_b between two clusters a, b (M the kernel between their atoms),
w = |q|, SB = max over sign patterns of |(s_a o w_a)^T M (s_b o w_b)|, any reference value mbar != 0,
e = max |M_pq - mbar|, rho = e/|mbar|, R_a = sum|q_a| / |sum q_a|:
        SB  <=  (1 + rho) / (1 - rho R_a R_b) * R_a R_b * |t|        whenever rho R_a R_b < 1,
with equality SB = R_a R_b |t| for a constant kernel.  "rho is the relative spread of the entries of Delta_T A over
the atom pairs of the two groups."

What is computed here (Ace-Lys5-NMe on the helix; workstream P8's validation case, order 4).  For every 4-subset T:
the context and states (z, y_T) at which |Delta_T g| is largest (from workstream P8's stored enumeration of g; the
mixed difference is taken here), the mixed-difference KERNEL matrix A = Delta_T M at that point (workstream P5's
kernel, 16 evaluations), and for every pair of lysines the block of A between their ammonium groups (NZ, HZ1-3,
identified by their charges) and between their extended head groups (CE, HE2, HE3, NZ, HZ1-3): the entries'
mean and spread, rho for two references (the mean; the midrange, which minimises e), R_a R_b, the exact SB of the
block by enumeration of all sign patterns, the block's own t, and the lemma's bound where it applies.
Mine: this file.  Workstream P5's: kernel_rows.  Workstream P8's: the stored g (out/m1_K5_H_0.70.npz, not tracked;
regenerate with ws_P8/p8_01_measure.py K5 H 0.70).  Checks printed: the charges; Delta_T g re-computed from A against
the mixed difference of the stored g; the lemma's inequality on every block where rho R_a R_b < 1.
Run: python3 -B kernel_spread.py > kernel_spread_K5.log
"""
import os, sys, itertools, resource, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "ws_P8"))
import p8lib as P8L
P5, PRE = P8L.P5, P8L.PRE


def log(s): print(s, flush=True)


def main():
    t0 = time.time(); seq, bb, tau = "K5", "H", 0.70
    G = P8L.GBModel(seq, bb, tau=tau); n, N = G.ns, G.nat; shape = tuple(G.k)
    Z = np.load(os.path.join(SCI, "ws_P8", "out", f"m1_{P8L.tagname(seq, bb, tau)}.npz"))
    x0 = tuple(int(v) for v in Z["anchor"]); assert tuple(Z["shape"]) == shape
    g = np.array(Z["g"], dtype=float).reshape(shape); q = np.array(G.q, dtype=float)
    # ---- head groups by charge: the atom of each moving side chain with the most negative charge and its three most positive partners
    amm, ext = [], []
    for i in range(n):
        mv = np.array(G.mov[i]); qi = q[mv]
        nz = mv[int(np.argmin(qi))]; hz = mv[np.argsort(-qi)[:3]]
        rest = [p for p in mv if p not in set(hz) and p != nz]
        ce_he = sorted(rest, key=lambda p: -p)[:3]                       # the three movable atoms listed just before the ammonium group
        amm.append(np.array([nz, *hz])); ext.append(np.array([*sorted(ce_he), nz, *hz]))
    log(f"=== Ace-Lys5-NMe on the helix, tau {tau}: {N} atoms, {n} sites, states per site {list(shape)}, anchor {list(x0)}")
    log(f"(0) ammonium groups (atom indices; charges): " + "; ".join(f"site {i}: {list(map(int, a))} q = {np.round(q[a], 4).tolist()}" for i, a in enumerate(amm[:2])) + " ...")
    Ra = [float(np.abs(q[a]).sum() / abs(q[a].sum())) for a in amm]; Re = [float(np.abs(q[a]).sum() / abs(q[a].sum())) for a in ext]
    log(f"    R = sum|q| / |sum q|: ammonium (4 atoms) {Ra[0]:.4f} (R^2 = {Ra[0] ** 2:.3f}; net charge {q[amm[0]].sum():+.4f}); with CE, HE2, HE3 (7 atoms: charges {np.round(q[ext[0]], 4).tolist()}) "
        f"{Re[0]:.4f} (R^2 = {Re[0] ** 2:.3f}; net charge {q[ext[0]].sum():+.4f})")

    def kernel_at(states):
        return P5.kernel_rows(G, np.atleast_2d(np.array(states)), np.arange(N))

    def sb_exact(M, wa, wb):
        best = 0.0
        for sa in itertools.product((1.0, -1.0), repeat=len(wa)):
            v = (np.array(sa) * wa) @ M
            best = max(best, float(np.abs(v * wb).sum()))               # the best s_b for a given s_a aligns every term
        return best
    log("| T | point of the largest abs(Delta_T g): context; states of T | Delta_T g there (kcal/mol): from the stored g; from the kernel matrix | pair of lysines (in T?) | group | kernel block: mean; min; max (1/nm) "
        "| rho (reference: mean) | rho (midrange) | R_a R_b | rho R_a R_b (midrange) | t of the block (kcal/mol) | SB of the block / abs(t), exact | the lemma's bound on that ratio |")
    log("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    stats = dict(blocks=0, regime=0, lemma_viol=0); summary = []
    for T in itertools.combinations(range(n), 4):
        D = g
        for i in T: D = D - np.take(D, [x0[i]], axis=i)
        k = int(np.argmax(np.abs(D))); xs = list(np.unravel_index(k, shape)); dstored = float(D.reshape(-1)[k])
        sts, sg = [], []
        for r in range(5):
            for U in itertools.combinations(T, r):
                x = list(xs)
                for i in T:
                    if i not in U: x[i] = x0[i]
                sts.append(x); sg.append((-1.0) ** (4 - r))
        A = np.tensordot(np.array(sg), kernel_at(sts), axes=1)          # Delta_T M at (z, y_T), an (N, N) matrix
        dker = float(0.5 * PRE * q @ A @ q); assert abs(dker - dstored) < 1e-8, (dker, dstored)
        rest = [i for i in range(n) if i not in T]
        first = True
        for i, j in itertools.combinations(range(n), 2):
            for name, grp, R in (("ammonium", amm, Ra), ("with CE, HE", ext, Re)):
                a, b = grp[i], grp[j]; M = A[np.ix_(a, b)]; mean, mn, mx = float(M.mean()), float(M.min()), float(M.max())
                rho_mean = float(np.abs(M - mean).max() / abs(mean)) if mean != 0 else float("inf")
                mid = 0.5 * (mx + mn); rho_mid = float(0.5 * (mx - mn) / abs(mid)) if mid != 0 else float("inf")
                RR = R[i] * R[j]; t = float(PRE * q[a] @ M @ q[b]); sb = float(abs(PRE) * sb_exact(M, np.abs(q[a]), np.abs(q[b])))
                ratio = sb / abs(t) if t != 0 else float("inf"); stats["blocks"] += 1
                bound = (1 + rho_mid) / (1 - rho_mid * RR) * RR if rho_mid * RR < 1 else None
                if bound is not None:
                    stats["regime"] += 1; stats["lemma_viol"] += int(ratio > bound * (1 + 1e-9))
                summary.append((name, rho_mid, rho_mid * RR, ratio, abs(t), i in T and j in T))
                head = (f"| {T} | context site {rest[0]} at state {xs[rest[0]]}; states {[int(xs[i_]) for i_ in T]} | {dstored:+.6f}; {dker:+.6f} " if first else "| | | ")
                log(head + f"| {i}, {j} ({'both' if (i in T and j in T) else 'one'}) | {name} | {mean:+.3e}; {mn:+.3e}; {mx:+.3e} | {rho_mean:.3g} | {rho_mid:.3g} | {RR:.3f} | {rho_mid * RR:.3g} | {t:+.3e} | "
                    f"{ratio:.3g} | {'%.3g' % bound if bound is not None else 'not in the regime'} |")
                first = False
    for name in ("ammonium", "with CE, HE"):
        S = [s for s in summary if s[0] == name]; r = np.array([s[1] for s in S]); rr = np.array([s[2] for s in S]); ra = np.array([s[3] for s in S]); tt = np.array([s[4] for s in S])
        big = tt >= 0.1 * tt.max()
        log(f"(1) {name}: {len(S)} blocks (5 subsets x 10 pairs); rho (midrange): smallest {r.min():.3g}, median {np.median(r):.3g}, largest {r.max():.3g}; rho R_a R_b < 1 in {int((rr < 1).sum())} of {len(S)}; "
            f"SB/|t| of the blocks: median {np.median(ra):.3g}; among the {int(big.sum())} blocks whose |t| is at least a tenth of the largest: rho from {r[big].min():.3g} to {r[big].max():.3g}, "
            f"rho R_a R_b < 1 in {int((rr[big] < 1).sum())}, SB/|t| from {ra[big].min():.3g} to {ra[big].max():.3g}")
    log(f"(2) the lemma's inequality on the {stats['regime']} blocks in its regime: {stats['lemma_viol']} violations")
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
