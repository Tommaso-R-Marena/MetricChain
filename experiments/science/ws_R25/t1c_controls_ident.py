#!/usr/bin/env python3
"""R25, Item 1 -- a control for the two counting identities of the proof (l.320-322 of the note), own code.

Usage: python3 -B t1c_controls_ident.py QMAX

The identities   st + fl + L = m(B-1)   and   fl = n - 1 - z   had 0 violations on every structure (runs 22-26).
Control (must fail): the same identities with a mis-defined flush face -- "two chords, one nick between two items,
no unpaired ITEM base" (the template side ignored, so that the exterior loop over a separator, or over an unpaired
G, counts as flush) -- while st, L and z are computed from the correct definitions.
"""
import sys
import time

import nn_model as nn


def main():
    t0 = time.time()
    qmax = int(sys.argv[1])
    nstruct = v1 = v2 = ok1 = ok2 = 0
    for m in range(1, qmax + 1):
        for B in range(1, qmax + 1):
            if m * B > qmax:
                continue
            for order in nn.compositions(m * B):
                n = len(order)
                circ = nn.Circle([nn.template(m, B)] + ["C" * a for a in order])
                box = [0, 0, 0, 0, 0]

                def leaf(partner, circ=circ, box=box, m=m, B=B, n=n):
                    if not nn.is_connected(circ, partner):
                        return
                    box[0] += 1
                    st = fl = L = z = flmut = 0
                    for f in nn.faces(circ, partner):
                        typ, d = nn.classify_face(circ, partner, f)
                        if typ == "stack":
                            st += 1
                        elif typ == "flush":
                            fl += 1
                        else:
                            L += d["tGG"]
                            z += d["item_nicks"]
                        if d["nnick"] == 1 and d["k"] == 2 and d["item_nicks"] == 1:
                            unp_item = sum(1 for i in f[0]
                                           if partner[(i + 1) % circ.N] == -1 and circ.sid[(i + 1) % circ.N] != 0)
                            if unp_item == 0:
                                flmut += 1
                    if st + fl + L == m * (B - 1):
                        box[3] += 1
                    if fl == n - 1 - z:
                        box[4] += 1
                    if st + flmut + L != m * (B - 1):
                        box[1] += 1
                    if flmut != n - 1 - z:
                        box[2] += 1

                nn.enumerate_noncrossing(circ, leaf)
                nstruct += box[0]
                v1 += box[1]
                v2 += box[2]
                ok1 += box[3]
                ok2 += box[4]
    print(f"families with mB <= {qmax}: {nstruct} connected structures")
    print(f"correct definitions: st+fl+L = m(B-1) holds for {ok1}, fl = n-1-z holds for {ok2} of {nstruct}")
    print(f"control (mis-defined flush): st+fl'+L != m(B-1) for {v1} structures; fl' != n-1-z for {v2} structures")
    print(f"time {time.time() - t0:.1f} s")


if __name__ == "__main__":
    nn.limit_memory(2.0)
    main()
    print(f"peak memory {nn.peak_mb():.1f} MB")
