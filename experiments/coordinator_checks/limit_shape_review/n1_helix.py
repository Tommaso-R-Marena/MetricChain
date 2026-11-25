#!/usr/bin/env python3
"""Assistant B — finding N1: the all-gauche 4_1 helix (bond indices 0,1,2,3,0,...) is a bridge for every N
with h = (0,0,N-3), g = N-3.  Own code (mylat.py); cross-check with the harness helpers ls_* (imported as a
library, sys.argv = ["x"]); and, by own exhaustive enumeration of bridges, the set of gauche counts that occur
with the profile (0,0,N-3)."""
import os, sys, importlib.util, time
sys.dont_write_bytecode = True
import mylat as ML

t0 = time.time()
# 1. own code
bad = []
for N in list(range(4, 201)) + [500, 1000, 4096, 10007]:
    w = ML.helix(N)
    err = ML.check_walk(w)
    br = ML.is_bridge(w)
    up = all(w[i + 1][1] - w[i][1] == 1 for i in range(N - 1))
    hg = ML.profile_hash(w)
    hg2 = ML.profile_bruteforce(w) if N <= 200 else ML.profile_kdtree(w)
    ok = (err is None) and br and up and hg == (0, 0, N - 3, N - 3) and hg2 == hg
    if not ok:
        bad.append((N, err, br, up, hg, hg2))
print("own code: helix for N = 4..200, 500, 1000, 4096, 10007: self-avoiding lattice walk, every bond an up-bond, bridge,")
print("   (h3,h8,h11,g) = (0,0,N-3,N-3) by two own counts (hash look-up and O(N^2) definition / k-d tree): failures:", bad)
w = ML.helix(9)
print("   first nine beads:", w)
print("   bead i+4 - bead i =", tuple(w[4][k] - w[0][k] for k in range(3)), " squared 1-5 distance", ML.sq(w[0], w[4]),
      "; 1-4:", ML.sq(w[0], w[3]), "; 1-6:", ML.sq(w[0], w[5]), "; 1-7:", ML.sq(w[0], w[6]))
# smallest squared distance between beads at chain separation >= 4 in a long helix
w = ML.helix(400)
m = min(ML.sq(w[0], w[j]) for j in range(4, 400))
print("   smallest squared distance at chain separation >= 4 (N = 400):", m)

# 2. harness helpers as a library
sys.argv = ["x"]
spec = importlib.util.spec_from_file_location("fc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "falsify_conjectures.py"))
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)
bad = []
for N in list(range(4, 121)) + [1000]:
    w = ML.helix(N)
    if not (fc.ls_valid_walk(w) and fc.ls_is_bridge(w) and fc.ls_profile(w) == (0, 0, N - 3, N - 3)):
        bad.append(N)
print("harness helpers (ls_valid_walk, ls_is_bridge, ls_profile) on the same walks, N = 4..120, 1000: failures:", bad)

# 3. exhaustive: which gauche counts occur with the profile (0,0,N-3) among ALL bridges with N beads
#    (own enumerator; cross-check of the enumerator against ls_enum(bridge=True) on counts)
for N in range(4, 15):
    cnt = 0
    gs = {}
    classes = set()
    for b in ML.enum_bridges(N):
        cnt += 1
        hg = ML.profile_hash(b)
        classes.add(hg[:3])
        if hg[:3] == (0, 0, N - 3):
            gs[hg[3]] = gs.get(hg[3], 0) + 1
    ref = len(fc.ls_enum(N, bridge=True)) if N <= 11 else None
    print(f"N = {N:2d}: {cnt} bridges from the origin (harness ls_enum: {ref}), {len(classes)} profile classes; "
          f"gauche counts with h = (0,0,{N-3}): {dict(sorted(gs.items()))}", flush=True)
print("time %.1f s" % (time.time() - t0))
