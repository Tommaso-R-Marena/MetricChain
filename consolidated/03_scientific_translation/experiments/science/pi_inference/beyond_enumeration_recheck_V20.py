#!/usr/bin/env python3
"""Addendum A17 (10): re-check of the coordinator's uncertified estimate of ln Z for Ace-Val20-NMe on PPII
(fitted chain model, window 2) with two new seeds and ten times more fresh samples.

Reason: workstream P6 ran the theory division's sandwich sampler (their Proposition 11.113) on workstream P3's certified
sandwich and obtained a bracket whose upper end lies below the earlier estimate 518.262562 +- 0.000075 (seed 20261127,
4 000 fresh samples) by about one standard error.  A fluctuation or a bias?  Each replication below refits the chain
tables from scratch (3 rounds of 30 000 evaluations, its own seed) and then takes 40 000 fresh samples.
Run:  python3 -u beyond_enumeration_recheck_V20.py > beyond_enumeration_recheck_V20.log     (one core)
"""
import os, sys, math, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beyond_enumeration_chain as bec
import beyond_enumeration_fit as bef

def log(s): print(s, flush=True)
t0 = time.time(); out = []
for seed in (31415926, 27182818):
    rng = np.random.default_rng(seed)
    ch, g_of, dom = bec.build("V" * 20, "P2", 2, log)
    sds = [bef.refit(ch, g_of, 30000, rng)[0] for _ in range(3)]
    lnZm = ch.solve()
    means = []
    for blk in range(10):                                   # 10 blocks of 4 000 fresh samples
        x = ch.sample(4000, rng); r = g_of(x) - ch.energy(x); means.append((float(r.mean()), float(r.var(ddof=1)), float(r.min()), float(np.mean(np.exp(-(r - r.mean()))))))
    m = float(np.mean([a for a, _, _, _ in means])); v = float(np.mean([b for _, b, _, _ in means])); se = math.sqrt(v / 40000)
    blockse = float(np.std([a for a, _, _, _ in means], ddof=1) / math.sqrt(10))
    Kexp = float(np.log(np.mean([c for _, _, _, c in means])))
    res = dict(seed=seed, lnZ_model=lnZm, r_mean=m, se=se, se_from_blocks=blockse, first_order=lnZm - m, K_exp=Kexp, r_min=min(c for _, _, c, _ in means), sd=math.sqrt(v), sds_before_refit=sds)
    out.append(res)
    log(f"seed {seed}: sd before each refit {', '.join(f'{s:.4f}' for s in sds)};  ln Z(m) = {lnZm:.6f};  40 000 fresh samples: mean r = {m:+.6f} +- {se:.6f} (from 10 block means: +- {blockse:.6f}), sd {math.sqrt(v):.5f}, min {res['r_min']:+.4f};"
        f"  first-order estimate ln Z(g) ~ {lnZm - m:.6f} +- {se:.6f};  exponential-average estimate of K = {Kexp:.2e}   ({time.time() - t0:.0f} s)")
json.dump(out, open(os.path.join(HERE, "beyond_enumeration_recheck_V20.json"), "w"), indent=1)
a, b = out
log(f"two replications: {a['first_order']:.6f} +- {a['se']:.6f} and {b['first_order']:.6f} +- {b['se']:.6f};  difference {a['first_order'] - b['first_order']:+.6f} ({abs(a['first_order'] - b['first_order']) / math.hypot(a['se'], b['se']):.2f} combined standard errors);  earlier run (seed 20261127, 4 000 samples): 518.262562 +- 0.000075")
log(f"ALL DONE {time.time() - t0:.0f} s")
