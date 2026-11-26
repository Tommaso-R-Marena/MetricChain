"""Single-line epochs with optimised outer rates (coordinator's exploration).
State of an epoch: T(x) <= B - s x for 0 < x <= R (s <= 1); start (B, 0, inf).
Slope step at outer rate e:  s' = [B - (1-s) theta_na(e)]/e,  R' = R e/(theta_na(e) + R)   (capped s' <= 1).
Drop:  B' = B - R (B - (1-s) a)/(a + R).
Policy: regular steps with e = argmax s' subject to e >= emin while s' < 1; then choose the stopping level of the
epoch (with one final push step chosen to maximise the drop) that maximises ln(delta/delta')/levels.
"""
import math, sys
import numpy as np
sys.path.insert(0, ".")
from pairs import Gauss, Cube

def run(P, K, emin_frac=0.05, verbose=False):
    a, h = P.a, P.h
    E = np.exp(np.linspace(math.log(emin_frac * h), math.log(P.estar), 20001))
    TNA = P.theta_na(E)
    B, k = a, 1                       # T_1 <= a
    hist = [(k, B)]
    while k < K:
        s, R = 0.0, float("inf")
        delta = B - h
        best = None                   # (rate, levels, Bnew)
        j = 0
        traj = []
        while j < 100000:
            # candidates for the final push from (s, R): choose e maximising the drop after one step
            sp = np.minimum((B - (1 - s) * TNA) / E, 1.0)
            Rp = E if math.isinf(R) else R * E / (TNA + R)
            dropB = B - Rp * (B - (1 - sp) * a) / (a + Rp)
            i = int(np.argmin(dropB))
            Bnew = float(dropB[i])
            levels = j + 2                                   # j regular steps + push + drop
            if Bnew < B and Bnew > h:
                rate = math.log(delta / (Bnew - h)) / levels
                if best is None or rate > best[0]:
                    best = (rate, levels, Bnew, s, R, float(E[i]))
            # regular step: maximise the slope
            i2 = int(np.argmax(sp))
            s2, R2 = float(sp[i2]), float(Rp[i2])
            traj.append((s, R, float(E[i2])))
            if s2 >= 1.0 - 1e-12 or s2 <= s:
                break
            s, R = s2, R2
            j += 1
            if best is not None and j > 3 * best[1] + 20:
                break
        rate, levels, Bnew, s_stop, R_stop, e_push = best
        k += levels
        B = Bnew
        hist.append((k, B))
        if verbose:
            print("   epoch: delta=%.3e levels=%d  delta'/delta=%.4f  (push from s=%.4f R=%.3e with e=%.4f)" % (delta, levels, (B - h) / delta, s_stop, R_stop, e_push))
    return hist

for P in [Gauss(), Cube(1.0), Cube(0.5), Cube(2.0)]:
    C = 2 * math.pi ** 2 * P.h ** 2 * P.hint2
    hist = run(P, 3000, verbose=(P.name == "gauss"))
    print("# %s: a=%.5f h=%.5f; sharp constant 2 pi^2 h^2 H2 = %.5f" % (P.name, P.a, P.h, C))
    print("#  k   B_k - h   k^2 (B_k - h)   ratio to sharp constant")
    for (k, B) in hist:
        if k in (1,) or k > 3:
            print("  %5d  %.4e  %.4f  %.2f" % (k, B - P.h, k * k * (B - P.h), k * k * (B - P.h) / C))
