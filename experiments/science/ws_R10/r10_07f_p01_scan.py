"""r10_07f: p = 0.1, u = 1: scan of the reference flip probability q~ for the safe threshold bound
(reference Markov(q~)) and the safe capacity bound; Y used Q = pi for E and q~ <= 1.1 p for a."""
import time, numpy as np
from r10lib import E_F
from r10_tilt import Tilt
t0 = time.time()
p, u = 0.1, 1.0
def klrate(q, p):
    return q * np.log(q / p) + (1 - q) * np.log((1 - q) / (1 - p))
for G in (801, 1601):
    T = Tilt(p, u, G, "safe")
    print("G=%d  E_F=%.6f" % (G, E_F(p, u)))
    for qt in (0.100, 0.102, 0.104, 0.106, 0.108, 0.110, 0.112, 0.115, 0.120, 0.130):
        e = T.thr_rate(qt, sweeps=6000, tol=1e-10)[0]
        print("   E: q~=%.3f: safe bound %.6f ;  E_F + KL-rate(q~||p) = %.6f ;  excess %.2e   (%.0fs)" % (qt, e, E_F(p, u) + klrate(qt, p), e - E_F(p, u) - klrate(qt, p), time.time() - t0), flush=True)
    if G == 801:
        for qt in (0.14, 0.16, 0.18, 0.20, 0.22, 0.25, 0.30):
            a = T.cap_rate(qt, sweeps=6000, tol=1e-9)[0]
            print("   a: q~=%.3f: safe bound %.6f   (%.0fs)" % (qt, a, time.time() - t0), flush=True)
