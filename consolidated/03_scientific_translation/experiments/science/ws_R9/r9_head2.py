#!/usr/bin/env python3
"""R9: the cleaned bridge 'head 2 + x + tail 3' has (h,g) = (h,g)(x) + A(x,c1) + B(x) EXACTLY (the third site below the
bridge never contributes to B), i.e. it realises qhat(x,c1) with N+5 beads.  All bridges with at most 13 beads."""
import sys
sys.dont_write_bytecode = True
import r9_lat as L
n = 0
for N in range(3, 14):
    for x in L.enum_bridges(N):
        idx = {p: i for i, p in enumerate(x)}
        h = L.profile(x); B = L.B_part(x, idx)
        s3 = L.bottom_sites(x, 3)[2]
        assert L._extra(idx, s3, -3) == [0, 0, 0]
        for c1 in L.admissible_c1(x):
            A = L.A_part(x, c1, idx)
            y = L.extend(x, c1, 2, 3)
            assert L.is_clean(y) and len(y) == N + 5
            assert L.profile(y) == tuple(h[i] + A[i] + B[i] for i in range(4))
            n += 1
print(f"{n} (bridge, c1) with 3..13 beads: head 2 + tail 3 is clean, has N+5 beads and (h,g) = (h,g) + A + B exactly; the third site below never has an extra pair")
