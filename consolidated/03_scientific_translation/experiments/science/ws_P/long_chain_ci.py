"""
Lower bounds on per-torsion bounded-difference constants c_i for chains too long to enumerate:
random sampling + greedy local search (multi-start coordinate ascent over the other torsions)
of   D_i(x) = max_a g(x^{i->a}) - min_a g(x^{i->a})   over clash-free states a (>= 2 of them).
Every reported value is attained by an explicit pair of clash-free grid conformations, so it
is a rigorous lower bound on the exact constant of that grid; it is NOT an upper bound.

usage: python3 long_chain_ci.py <n> <alphabet> <residual> [--sites a,b,...] [--starts S] [--sweeps W]
residual in {GB, ff03, coulGB}
"""
import sys, time, os, json, math
import numpy as np
from pepbuild import Peptide
from fastff import FastFF
from enumerate_grid import ALPHABETS

TAU = 0.7


def main():
    n = int(sys.argv[1]); alphabet = sys.argv[2]; resid = sys.argv[3]
    S = int(sys.argv[sys.argv.index("--starts") + 1]) if "--starts" in sys.argv else 8
    W = int(sys.argv[sys.argv.index("--sweeps") + 1]) if "--sweeps" in sys.argv else 6
    m = 2 * n
    sites = list(range(m))
    if "--sites" in sys.argv:
        sites = [int(v) for v in sys.argv[sys.argv.index("--sites") + 1].split(",")]
    ph, ps = ALPHABETS[alphabet]; k = len(ph)
    PH = np.deg2rad(np.array(ph)); PS = np.deg2rad(np.array(ps))
    extra = ("ff03",) if resid == "ff03" else ()
    P = Peptide(n, extra_ffs=extra, solvent=True, platform="CPU")
    F = FastFF(P, threads=1)
    rng = np.random.default_rng(99 + n)

    def evaluate(st):
        """st: (B, m) int states -> (g, ok)"""
        X = P.coords(PH[st[:, 0::2]], PS[st[:, 1::2]])
        E = F.energies(X, gb=("gbn2",), extra=extra if extra else False)
        if resid == "GB":
            g = E["gbn2"]
        elif resid == "coulGB":
            g = E["gbn2"] + E["coul"]
        else:
            g = (E["ff03_tors"] + E["ff03_lj"] + E["ff03_coul"]) - (E["tors"] + E["lj"] + E["coul"])
        return g, E["clash"] > TAU

    def objective(base, i):
        """base: (B, m).  D_i for each row: spread of g over the clash-free states of site i."""
        B = base.shape[0]
        st = np.repeat(base, k, axis=0)
        st[:, i] = np.tile(np.arange(k), B)
        g, ok = evaluate(st)
        g = g.reshape(B, k); ok = ok.reshape(B, k)
        hi = np.where(ok, g, -np.inf).max(axis=1); lo = np.where(ok, g, np.inf).min(axis=1)
        D = np.where(ok.sum(axis=1) >= 2, hi - lo, -1.0)
        return D

    out = {}
    t0 = time.time()
    # random sampling stage (shared pool)
    R = 400
    pool = rng.integers(0, k, (R, m))
    for i in sites:
        D = objective(pool, i)
        best_idx = np.argsort(-D)[:S]
        cur = pool[best_idx].copy(); curD = D[best_idx].copy()
        samp_max = float(D.max()); samp_med = float(np.median(D[D >= 0])) if (D >= 0).any() else float("nan")
        for sweep in range(W):
            improved = False
            for j in rng.permutation(m):
                if j == i:
                    continue
                cand = np.repeat(cur, k, axis=0)
                cand[:, j] = np.tile(np.arange(k), S)
                Dc = objective(cand, i).reshape(S, k)
                bj = Dc.argmax(axis=1); bD = Dc[np.arange(S), bj]
                upd = bD > curD + 1e-9
                if upd.any():
                    cur[upd, j] = bj[upd]; curD[upd] = bD[upd]; improved = True
            if not improved:
                break
        b = int(curD.argmax())
        out[i] = dict(lower_bound=float(curD.max()), sampled_max=samp_max, sampled_median=samp_med,
                      state=cur[b].tolist(), sweeps=sweep + 1)
        print(f"n={n} {alphabet} {resid} site {i:3d} (dist to end {min(i + 1, m - i)}): sampled median {samp_med:6.2f} max {samp_max:6.2f} "
              f"-> local search {curD.max():6.2f} kcal/mol   [{time.time() - t0:.0f}s]", flush=True)
    os.makedirs("out", exist_ok=True)
    path = f"out/long_ci_{alphabet}_n{n}_{resid}.json"
    json.dump(dict(n=n, alphabet=alphabet, residual=resid, starts=S, sweeps=W, pool=R, sites={str(i): v for i, v in out.items()}),
              open(path, "w"), indent=0)


if __name__ == "__main__":
    main()
