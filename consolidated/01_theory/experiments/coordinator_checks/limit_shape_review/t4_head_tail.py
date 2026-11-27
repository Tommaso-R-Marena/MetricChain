"""Theory report Proposition 11.69b(b): how short may the zigzag head and tail be that make a bridge clean?
The proposition proves that three beads suffice; this script tries one to four beads on every bridge with 3..10 beads
(own lattice code `mylat.py`, concatenation helpers of `concat_check.py`).  Run from this directory: about 20 s."""
import sys, random, time, itertools
sys.dont_write_bytecode = True
import mylat as ML
import concat_check as C

def head(x, k):
    u1 = C.sub(x[1], x[0]); u2 = C.sub(x[2], x[1])
    out = []; p = x[0]
    for j in range(k):
        p = C.sub(p, u2 if j % 2 == 0 else u1)
        out.append(p)
    return out[::-1]

def in_S(x):
    cs, b, dg = C.c1_choices(x)
    if dg != 0:
        return False
    S = set(x)
    return C.A_part(x, S, cs[0], b, dg) == (0, 0, 0, 0) and C.B_part(x, S) == (0, 0, 0, 0)

for k in (1, 2, 3, 4):
    bad = 0; tot = 0; mx = [0, 0, 0, 0]
    for N in range(3, 11):
        for x in ML.enum_bridges(N):
            cs, b, dg = C.c1_choices(x)
            for c1 in cs:
                y = head(x, k) + x + C.zigzag(x, c1, b, k)
                assert ML.check_walk(y) is None and ML.is_bridge(y)
                tot += 1
                if not in_S(y):
                    bad += 1
                else:
                    h0 = ML.profile_hash(x); h1 = ML.profile_hash(y)
                    for i in range(4):
                        mx[i] = max(mx[i], h1[i] - h0[i])
    print(f"head and tail of {k} zigzag beads: {tot - bad} of {tot} extended bridges (3..10 beads, every admissible c1) are in S; largest change of (h, g) among those: {mx}")
