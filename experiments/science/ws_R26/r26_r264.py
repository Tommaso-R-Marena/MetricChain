#!/usr/bin/env python3
"""r26_r264.py -- workstream R26: numerical check of Proposition R26.4 on the 16-point outer space of r26_hub.py
(3 free binary sites x 1 boundary site with P(boundary = 1) = pi_h): the Lemma N.0 upper tail function of the
envelope u*Hamming + iota*[boundary site differs], for several iota, below and above the least boundary-state
probability; and the mixture bound sup{ sum_beta mu(beta) Xi_slice(q_beta) : sum_beta mu(beta) q_beta <= q }.
Checks (each can fail): nondecreasing in iota; below the least boundary-state probability no dependence on iota
once iota >= 3u (the diameter of a slice) and at most the mixture bound; above it, growth with iota.
Usage: python3 -B r26_r264.py"""
import resource
import sys

import numpy as np

import r26_alg as A

c, u = 4, 1.0
pts = np.arange(1 << c)
bits = (pts[:, None] >> np.arange(c)[None, :]) & 1
ac = bits[:, c - 1]
ham = np.array([[bin(int(x) ^ int(z)).count("1") for z in pts] for x in pts], dtype=float)
hot = (ac[:, None] != ac[None, :]).astype(float)
viol = 0
for pi_h in (0.2, 0.02):
    mu = np.where(ac == 1, pi_h, 1 - pi_h) / (1 << (c - 1))
    p3 = np.arange(8)
    ham3 = np.array([[bin(int(x) ^ int(z)).count("1") for z in p3] for x in p3], dtype=float)
    S3 = A.EnumeratedEnvelope(np.full(8, 1 / 8), u * ham3)

    def mix(q):
        best = 0.0
        for q1 in np.linspace(0, min(1.0, q / pi_h), 801):          # q_1 = relative measure in the rare slice
            q0 = (q - pi_h * q1) / (1 - pi_h)
            if q0 < 0 or q0 >= 1 - 1e-12 or q1 >= 1 - 1e-12:
                continue
            best = max(best, pi_h * S3.Xi(q1) + (1 - pi_h) * S3.Xi(q0))
        return best
    tabs = {iota: A.EnumeratedEnvelope(mu, u * ham + iota * hot) for iota in (0.0, 1.0, 3.0, 8.0, 11.45, 40.0)}
    print(f"pi_h = {pi_h}: least boundary-state probability {min(pi_h, 1 - pi_h)}")
    print("      q     " + "".join(f"iota={i:<8g}" for i in tabs) + "  mixture bound")
    for q in (0.2 * pi_h, 0.5 * pi_h, 0.9 * pi_h, 0.999 * pi_h, 1.001 * pi_h, 2 * pi_h, 0.5):
        vals = [tabs[i].Xi(q) for i in tabs]
        m_ = mix(q) if q < min(pi_h, 1 - pi_h) else float("nan")
        print(f"  {q:8.5f}  " + "".join(f"{v:<13.5g}" for v in vals) + f"  {m_:.5g}")
        v = np.array(vals)
        if (np.diff(v) < -1e-12).any():
            viol += 1
        if q < min(pi_h, 1 - pi_h):
            if abs(v[-1] - v[-2]) > 1e-12 * max(1, v[-1]) or abs(v[-2] - v[-3]) > 1e-12 * max(1, v[-1]):
                viol += 1
            if v[-1] > m_ * (1 + 1e-9) + 1e-15:
                viol += 1
        else:
            if not (v[-1] > 10 * v[-3]):
                viol += 1
print(f"violations: {viol}")
print(f"peak memory {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")
sys.exit(1 if viol else 0)
