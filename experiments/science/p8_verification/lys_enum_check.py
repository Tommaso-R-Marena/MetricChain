#!/usr/bin/env python3
"""Coordinator's check of workstream P8's constants on ENUMERATED instances, with code that is not P8's for everything
except the constants themselves.

For SEQ on the helix (P2's pruned product domain, as the workstreams use it) and every order m = 3 .. n:
  left side   R(x) = | g(x) - I_{m-1} g(x) |  at EVERY state, from my own evaluation of g at every state (P3's bulk
              evaluator, called here) and my own anchored expansion (successive differences on the grid);
  right side  B(x) = sum_{T subset S(x), |T| = m} chat_T  with P8's per-subset constants, variants 'Sb' (P3's theorem,
              state-wise maximum) and 'SAb' (P8's Theorem AH), read from ws_P8/out/bc_<tag>.json.
The certificate pipeline needs exactly R <= B at every state.  Also printed: how loose the bound is where it matters
(Boltzmann-weighted means under the true ensemble E = f + g), and P8's stored enumeration of g against mine.

Run: python3 -B lys_enum_check.py K5 0.70 > lys_enum_check_K5.log
"""
import os, sys, json, math, time, itertools, importlib, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "ws_P6"))
import p6lib as L
pw = L.pw; BETA = L.BETA
CACHE = os.path.join(SCI, "pi_inference", "serine_helix_reach_cache")
L.encl.CACHE = CACHE; L.MYCACHE = CACHE


def log(s): print(s, flush=True)


def remainder(F, x0, m):
    """F - I_{m-1} F on the whole grid: sum over U, |U| >= m, of the anchored component d_U (zero unless U is inside
    the changed set)."""
    n = F.ndim; R = np.zeros_like(F)
    for r in range(m, n + 1):
        for U in itertools.combinations(range(n), r):
            d = F
            for i in range(n):
                a = np.take(d, [x0[i]], axis=i)
                d = (d - a) if i in U else a
            R = R + d
    return R


def main():
    seq, tau = sys.argv[1], float(sys.argv[2]); bb = "H"; t0 = time.time()
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
    log(f"=== {seq} on {bb}, tau {tau}: {G.nat} atoms, {n} sites, states per site {k}, {int(np.prod(k))} states; anchor {x0}")
    grid = np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, n)
    g = np.empty(len(grid))
    for s in range(0, len(grid), 256): g[s:s + 256] = G.bulk_energy(grid[s:s + 256])
    f = pw.f_energy(grid, c0, h, J)
    log(f"(0) g evaluated at every state with P3's bulk evaluator [{time.time() - t0:.0f}s]")
    fm = os.path.join(SCI, "ws_P8", "out", f"m1_{tag}.npz")
    if os.path.exists(fm):
        Z = np.load(fm)
        if "g" in Z.files and Z["g"].shape == g.shape:
            log(f"    P8's stored enumeration of g (ws_P8/out/m1_{tag}.npz) against mine: largest deviation {float(np.abs(Z['g'] - g).max()):.2e} kcal/mol; "
                f"its anchor equals mine: {[int(v) for v in Z['anchor']] == x0}")
    E = f + g; wB = np.exp(-BETA * (E - E.min())); lnZ = float(-BETA * E.min() + math.log(wB.sum())); wB /= wB.sum()
    Sx = (grid != np.array(x0)[None])
    log(f"    exact ln Z = {lnZ:.6f}; mean number of sites off the anchor in the true ensemble: {float((wB * Sx.sum(1)).sum()):.3f}")
    Jd = json.load(open(os.path.join(SCI, "ws_P8", "out", f"bc_{tag}.json")))
    F = g.reshape(k)
    log("| m | variant | subsets | sum of constants (kT) | states with >= m sites off the anchor | violations R > B | largest R (kcal/mol) | smallest B/R (R > 1e-9) | "
        "Boltzmann mean of beta R | Boltzmann mean of beta B | ratio |")
    log("|---|---|---|---|---|---|---|---|---|---|---|")
    out = {}
    for m in range(3, n + 1):
        R = np.abs(remainder(F, x0, m)).reshape(-1)
        for var in ("Sb", "SAb"):
            chat = {tuple(int(v) for v in s_.split("-")): float(c_) for s_, c_ in Jd["per_subset"][var].items() if len(s_.split("-")) == m}
            assert len(chat) == math.comb(n, m)
            B = np.zeros(len(grid))
            for T, v in chat.items(): B += v * Sx[:, list(T)].all(axis=1)
            viol = int((R > B * (1 + 1e-12) + 1e-10).sum()); nz = R > 1e-9
            out[f"{m}_{var}"] = dict(viol=viol, maxR=float(R.max()), min_ratio=float((B[nz] / R[nz]).min()), mean_bR=float(BETA * (wB * R).sum()), mean_bB=float(BETA * (wB * B).sum()))
            log(f"| {m} | {var} | {len(chat)} | {BETA * sum(chat.values()):.4g} | {int((Sx.sum(1) >= m).sum())} | {viol} | {R.max():.4g} | {(B[nz] / R[nz]).min():.3f} | "
                f"{BETA * (wB * R).sum():.3e} | {BETA * (wB * B).sum():.3e} | {(wB * B).sum() / max((wB * R).sum(), 1e-300):.1f} |")
    json.dump(dict(seq=seq, tau=tau, lnZ=lnZ, res=out), open(os.path.join(HERE, f"lys_enum_check_{seq.replace(':', 'c')}.json"), "w"), indent=1)
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
