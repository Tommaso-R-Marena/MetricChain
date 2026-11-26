#!/usr/bin/env python3
"""Addendum A17 (10), note of 2026-11-26: a long run of the fitted chain model for Ace-Val20-NMe on PPII, to decide whether
the offset of 2.3 standard errors between the chain-model estimates and the sandwich-sampler estimates (see
sampler_precision_check.py) is a fluctuation.  One seed, tables refitted as in the production run (3 rounds of 30 000),
then 600 000 fresh samples in 60 blocks; the running estimate is printed after every block.
Run:  python3 -u beyond_enumeration_recheck_V20_long.py > beyond_enumeration_recheck_V20_long.log     (one core, about 30 min)
"""
import os, sys, math, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beyond_enumeration_chain as bec
import beyond_enumeration_fit as bef

def log(s): print(s, flush=True)
t0 = time.time(); seed = 16180339
rng = np.random.default_rng(seed)
ch, g_of, dom = bec.build("V" * 20, "P2", 2, log)
sds = [bef.refit(ch, g_of, 30000, rng)[0] for _ in range(3)]
lnZm = ch.solve()
log(f"seed {seed}: sd before each refit {', '.join(f'{s:.4f}' for s in sds)};  ln Z(m) = {lnZm:.9f}   ({time.time() - t0:.0f} s)")
B = 10000; means = []; s1 = s2 = se_ = 0.0; n = 0; sexp = 0.0; rmin = 0.0
for blk in range(60):
    x = ch.sample(B, rng); r = g_of(x) - ch.energy(x)
    means.append(float(r.mean())); s1 += float(r.sum()); s2 += float((r * r).sum()); sexp += float(np.exp(-r).sum()); n += B; rmin = min(rmin, float(r.min()))
    m = s1 / n; se = math.sqrt((s2 / n - m * m) / n)
    direct = lnZm + math.log(sexp / n)                      # ln Z(m) + ln mean(e^{-r}): the exponential average, no cumulant expansion
    if (blk + 1) % 5 == 0:
        log(f"  {n:7d} samples: mean r = {m:+.9f} +- {se:.9f};  ln Z(m) - mean + K = {lnZm - m + math.log(sexp / n) + m:.9f};  exponential average {direct:.9f} +- {se:.9f};  min r {rmin:+.4f}   ({time.time() - t0:.0f} s)")
blockse = float(np.std(means, ddof=1) / math.sqrt(len(means)))
res = dict(seed=seed, lnZ_model=lnZm, N=n, r_mean=s1 / n, se=se, se_from_blocks=blockse, estimate=direct, r_min=rmin, sds_before_refit=sds)
json.dump(res, open(os.path.join(HERE, "beyond_enumeration_recheck_V20_long.json"), "w"), indent=1)
log(f"final: ln Z(E) ~ {direct:.9f} +- {se:.9f} (from the 60 block means: +- {blockse:.9f});  sandwich sampler (workstream P6): 518.262414 +- 0.000005 and 518.262417 +- 0.000006")
log(f"ALL DONE {time.time() - t0:.0f} s")
