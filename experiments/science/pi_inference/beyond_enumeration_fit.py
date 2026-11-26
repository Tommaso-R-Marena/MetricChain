#!/usr/bin/env python3
"""Addendum A17 (10), second part: the chain model FITTED on samples -- coordinator's script.

The model of beyond_enumeration_chain.py takes its solvent tables from an anchored expansion at one reference
assignment.  Any chain model is admissible (the choice of m is free; only the floor and the variance of the remainder
under pi_m matter), so the tables can be improved by regression: draw assignments from the current model, evaluate the
remainder r = beta (g - m), fit it by least squares with one-body and windowed pair tables (the same chain form), add
the fit to the model, repeat.  The final statistics are taken on FRESH samples of the final model.

usage: python3 beyond_enumeration_fit.py SEQLETTER BACKBONE W n_small n_large [...]  [--fit N_FIT] [--iters K]
"""
import os, sys, math, json, time
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import lsqr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beyond_enumeration_chain as bec

def design(x, ch):
    N = x.shape[0]; cols = []; rows = []; ncol = 0; index = []
    for i in range(ch.n):
        cols.append(ncol + x[:, i]); rows.append(np.arange(N)); index.append(("u", i, ncol)); ncol += ch.k[i]
    for (i, j) in sorted(ch.v):
        cols.append(ncol + x[:, i] * ch.k[j] + x[:, j]); rows.append(np.arange(N)); index.append(("v", (i, j), ncol)); ncol += ch.k[i] * ch.k[j]
    A = sp.csr_matrix((np.ones(sum(len(r) for r in rows)), (np.concatenate(rows), np.concatenate(cols))), shape=(N, ncol))
    return A, index, ncol

def refit(ch, g_of, n_fit, rng):
    ch.solve()
    x = ch.sample(n_fit, rng)
    r = g_of(x) - ch.energy(x)
    A, index, ncol = design(x, ch)
    mu = float(r.mean())
    theta = lsqr(A, r - mu, damp=1e-3, atol=1e-10, btol=1e-10, iter_lim=20000)[0]
    for kind, key, off in index:
        if kind == "u":
            ch.u[key] = ch.u[key] + theta[off:off + ch.k[key]]
        else:
            i, j = key
            ch.v[key] = ch.v[key] + theta[off:off + ch.k[i] * ch.k[j]].reshape(ch.k[i], ch.k[j])
    ch.const += mu
    return float(r.std()), n_fit

if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    n_fit = 30000; iters = 3
    if "--fit" in args: k = args.index("--fit"); n_fit = int(args[k + 1]); del args[k:k + 2]
    if "--iters" in args: k = args.index("--iters"); iters = int(args[k + 1]); del args[k:k + 2]
    aa, bb, W = args[0], args[1], int(args[2]); n_small = int(args[3]); larges = [int(v) for v in args[4:]]
    def log(s): print(s, flush=True)
    rng = np.random.default_rng(20261127)
    out = []
    log(f"# {aa} homopeptide on backbone {bb}, chain model with window W = {W}, tables refitted on samples ({iters} rounds of {n_fit}); k_BT at 300 K")
    for n in [n_small] + larges:
        ch, g_of, dom = bec.build(aa * n, bb, W, log)
        sds = []
        for it in range(iters):
            sd_before, _ = refit(ch, g_of, n_fit, rng)
            sds.append(sd_before)
        log(f"      standard deviation of the remainder under the model before each refit: " + ", ".join(f"{s:.4f}" for s in sds))
        exact = bec.exact_values(ch, g_of) if n == n_small else None
        res = bec.report(f"{aa}{n}_{bb} fitted" + (" (validation)" if n == n_small else ""), ch, g_of, 4000, rng, log, exact=exact)
        res["evaluations_for_fit"] = iters * n_fit
        out.append(res)
        if n != n_small: log(f"      (number of rotamer assignments: about 10^{sum(math.log10(len(d)) for d in dom):.1f}; evaluations used for the fit: {iters * n_fit})")
    json.dump(out, open(os.path.join(HERE, f"beyond_enumeration_fit_{aa}_{bb}_W{W}.json"), "w"), indent=1)
