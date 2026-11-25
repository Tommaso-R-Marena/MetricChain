"""R7 OWN: structure of the five exact ties at n = 11 (why is the profile distance an exact integer?)."""
import sys
import mpmath as mp
import numpy as np
import own_ties as ot

mp.mp.dps = 50
c = -mp.cos(mp.radians(111))      # cos 69 deg = b_k . b_{k+1}

def word(s): return ["t+-".index(ch) for ch in s]

PAIRS = [("tt+tt-tt---", "+t+ttt++t--"), ("tt++t-tt+t-", "+t+ttt++t--"), ("tt+tt-t++t-", "+t+t--ttt++"),
         ("tt+tt-t-t++", "+t+t+ttt+++"), ("tt+tt-t+t--", "+t+t-ttt+++")]

def labelled(w, sc=16):
    X = ot.mp_coords(w)
    N = len(X)
    out = []
    for p in range(N):
        for q in range(p + 3, N):
            s = sum((X[p][i] - X[q][i]) ** 2 for i in range(3))
            out.append((min(s, mp.mpf(sc)), p, q, s))
    return sorted(out, key=lambda t: t[0])

for wa, wy in PAIRS:
    A, Y = labelled(word(wa)), labelled(word(wy))
    diffs = [a[0] - y[0] for a, y in zip(A, Y)]
    nz = [(k, d) for k, d in enumerate(diffs) if abs(d) > mp.mpf(10) ** -40]
    pos = sum(d for k, d in nz if d > 0); neg = sum(-d for k, d in nz if d < 0)
    inA = sum(1 for a in A if a[0] < 16); inY = sum(1 for y in Y if y[0] < 16)
    print(f"\ncentre {wa} (pairs inside cutoff {inA}, gauche {sum(ch != 't' for ch in wa)})   point {wy} (inside {inY}, gauche {sum(ch != 't' for ch in wy)})")
    print(f"  positions that differ: {len(nz)} of {len(diffs)};  sum of positive differences {mp.nstr(pos, 25)}  sum of negative {mp.nstr(neg, 25)}  total |.| {mp.nstr(pos + neg, 30)}")
    print(f"  sum over ALL truncated distances: centre {mp.nstr(sum(a[0] for a in A), 30)}  point {mp.nstr(sum(y[0] for y in Y), 30)}  difference {mp.nstr(sum(a[0] for a in A) - sum(y[0] for y in Y), 30)}")
    # express each sum as alpha + beta*c  (integer relation search)
    for name, L in (("centre", A), ("point", Y)):
        tot = sum(a[0] for a in L if a[0] < 16)
        rel = mp.pslq([tot, 1, c, c ** 2, c ** 3], maxcoeff=10 ** 6, maxsteps=10 ** 5)
        print(f"  {name}: sum of the squared distances inside the cutoff = {mp.nstr(tot, 25)}; integer relation with (1, c, c^2, c^3), c = cos 69deg: {rel}")
