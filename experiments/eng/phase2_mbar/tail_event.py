#!/usr/bin/env python
"""Supplementary and post hoc (not in PREDICTIONS.md): what the largest density ratio on the event does.

Found while writing a unit test: the pooled certificate of Theorem M1 was hardly better than target-only
sampling on the tail event {x > 0.68} of a Gaussian target, although the windows reach the event.  Cause: the
sample size needed is set by sup over the event of p_0/m (m the sampling mixture), and harmonic windows decay
faster than the target beyond the last window, so that sup sits in the far tail.  Three configurations:

  tail-6    the event {x > 0.68}, target and five windows (centres 0.4 .. 0.8)
  slice-6   the thin slice {0.68 < x <= 0.70}, same states
  tail-8    the event {x > 0.68}, two more windows (centres 0.9, 1.0) that cover the far tail

    PYTHONPATH=src python experiments/eng/phase2_mbar/tail_event.py
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

import multistate_certificate as E

HERE = os.path.dirname(os.path.abspath(__file__))
SEED, N, REPS, GAMMA = 20261128, 18000, 60, 3.0


def states(centres):
    x = (np.arange(E.M) + 0.5) / E.M
    base = -80.0 * (x - 0.3) ** 2
    lq = np.stack([base] + [base - 200.0 * (x - c) ** 2 for c in centres], axis=1)
    P = np.exp(lq - lq.max(axis=0))
    P /= P.sum(axis=0)
    return x, lq, P


def main():
    eps = 0.5 * math.log(GAMMA)
    lam, ups = math.exp(-eps), math.exp(eps)
    five, seven = (0.4, 0.5, 0.6, 0.7, 0.8), (0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
    configs = {"tail-6": (five, lambda x: (x > 0.68).astype(float)),
               "slice-6": (five, lambda x: ((x > 0.68) & (x <= 0.70)).astype(float)),
               "tail-8": (seven, lambda x: (x > 0.68).astype(float))}
    out = {}
    for ci, (name, (centres, obs)) in enumerate(configs.items()):
        x, lq, P = states(centres)
        f = obs(x)
        p = float(P[:, 0] @ f)
        truth = ups * p / (ups * p + lam * (1 - p))
        m = P.mean(axis=1)
        ratio = P[:, 0] / m
        sup, avg = float(np.max(ratio * f)), p / float(m @ f)
        vals, stats = {}, {}
        for child in np.random.SeedSequence([SEED, 100 + ci]).spawn(REPS):
            rng = np.random.default_rng(child)
            res = E.run_target(rng, P, f, lam, ups, N, True)
            res.update(E.run_pooled(rng, lq, P, f, lam, ups, N, True)[0])
            for k, (v, st) in res.items():
                vals.setdefault(k, []).append(float(v))
                stats.setdefault(k, []).append(st)
        row = dict(states=1 + len(centres), p0_event=p, truth=truth, mixture_mass_of_event=float(m @ f),
                   sup_ratio_on_event=sup, sup_over_average_ratio=sup / avg, methods={})
        for k in vals:
            v = np.array(vals[k])
            cert = np.array([s == "certified" for s in stats[k]])
            row["methods"][k] = dict(median_ratio=float(np.median(v) / truth), wrong=int(np.sum(v[cert] < truth * (1 - 1e-9))),
                                     certified=int(cert.sum()), abstain=int(sum(s.startswith("abstain") for s in stats[k])))
        out[name] = row
        print(f"{name:8s} K={row['states']} p0(event)={p:.3e} sup/avg of p0/m on the event={sup / avg:8.1f} | "
              + " | ".join(f"{k} x{d['median_ratio']:.1f} w{d['wrong']} a{d['abstain']}" for k, d in row["methods"].items()))
    with open(os.path.join(HERE, "results", "tail_event.json"), "w") as fh:
        json.dump(dict(seed=SEED, N=N, reps=REPS, gamma=GAMMA, configs=out), fh, indent=1)


if __name__ == "__main__":
    main()
