"""K = 5: orbits of type sets under the group of order 1920, decision of every orbit representative by the
full LP over all states of the type sites (exact verification), cross-check with the span-reduced algorithm,
counts of type sets, the six non-exposed orbits, four-states-with-constant-product statistics."""
import itertools, sys, json, time
from fractions import Fraction
from multiprocessing import Pool
import numpy as np
from ising_core import *

K = 5
types = [(1,) + t for t in itertools.product([1, -1], repeat=K - 1)]     # 16 types
NT = len(types)
idx = {t: i for i, t in enumerate(types)}


def canon_t(t):
    return t if t[0] == 1 else tuple(-v for v in t)


def group_perms():
    G = set()
    for perm in itertools.permutations(range(K)):
        for sg in itertools.product([1, -1], repeat=K):
            G.add(tuple(idx[canon_t(tuple(sg[i] * t[perm[i]] for i in range(K)))] for t in types))
    return sorted(G)


def orbit_data():
    G = group_perms()
    masks = np.arange(1 << NT, dtype=np.int64)
    best = masks.copy()
    lo = masks & 255
    hi = masks >> 8
    for g in G:
        L = np.zeros(256, dtype=np.int64)
        H = np.zeros(256, dtype=np.int64)
        for b in range(256):
            v = 0
            w = 0
            for i in range(8):
                if b >> i & 1:
                    v |= 1 << g[i]
                    w |= 1 << g[i + 8]
            L[b] = v
            H[b] = w
        img = L[lo] | H[hi]
        np.minimum(best, img, out=best)
    return len(G), best


def types_of(mask):
    return [types[i] for i in range(NT) if mask >> i & 1]


def nondegenerate(mask):
    ts = types_of(mask)
    for k in range(K):
        for l in range(k + 1, K):
            if len(set(t[k] * t[l] for t in ts)) < 2:
                return False
    return True


def const_product_quads(mask):
    ts = types_of(mask)
    out = []
    for Q in itertools.combinations(range(K), 4):
        if len(set(int(np.prod([t[k] for k in Q])) for t in ts)) == 1:
            out.append(Q)
    return out


def work(mask):
    ts = types_of(mask)
    V = states_from_types(ts)
    t0 = time.time()
    r1 = decide(V)
    r2 = decide_span(V)
    Y, _ = sign_vectors_in_span(V)
    extra = sorted(set(Y) - set(canon(x) for x in V))
    info = dict(mask=int(mask), ntypes=len(ts), exposed=bool(r1.exposed), exposed_span=bool(r2.exposed),
                n_extra_sign_vectors=len(extra), quads=const_product_quads(mask), time=time.time() - t0)
    if not r1.exposed:
        info["mu"] = [("".join("+" if v > 0 else "-" for v in y), str(w)) for y, w in r1.mu.items()]
        info["alpha"] = [str(a) for a in r1.alpha]
        info["states"] = ["".join("+" if v > 0 else "-" for v in x) for x in V]
    return info


if __name__ == "__main__":
    gorder, best = orbit_data()
    print("effective group order:", gorder)
    reps, counts = np.unique(best[1:], return_counts=True)
    print("orbits of non-empty type sets:", len(reps))
    nd = [bool(nondegenerate(int(r))) for r in reps]
    print("non-degenerate orbits:", sum(nd), "  non-degenerate type sets:", int(sum(c for c, f in zip(counts, nd) if f)))
    todo = [int(r) for r, f in zip(reps, nd) if f]
    with Pool(4) as pool:
        results = pool.map(work, todo, chunksize=1)
    size = {int(r): int(c) for r, c in zip(reps, counts)}
    nexp_orb = [r for r in results if not r["exposed"]]
    print("non-exposed orbits:", len(nexp_orb), "  non-exposed type sets:", sum(size[r["mask"]] for r in nexp_orb))
    print("disagreements full LP vs span-reduced LP:", sum(r["exposed"] != r["exposed_span"] for r in results))
    print("exposed orbits containing 4 states with constant product:",
          sum(1 for r in results if r["exposed"] and r["quads"]))
    print("non-exposed orbits WITHOUT 4 states of constant product:",
          sum(1 for r in results if not r["exposed"] and not r["quads"]))
    print("exposed orbits whose span contains another sign vector:",
          sum(1 for r in results if r["exposed"] and r["n_extra_sign_vectors"] > 0))
    print("non-exposed orbits whose span contains NO other sign vector (would contradict Prop. 5):",
          sum(1 for r in results if not r["exposed"] and r["n_extra_sign_vectors"] == 0))
    for r in nexp_orb:
        print("--- non-exposed orbit: rep mask", r["mask"], "types", r["ntypes"], "orbit size", size[r["mask"]],
              "const-product quads", r["quads"])
        print("    states:", r["states"])
        print("    mu:", r["mu"])
        print("    alpha:", r["alpha"])
    for r in results:
        r["orbit_size"] = size[r["mask"]]
    json.dump(results, open("k5_results.json", "w"), indent=1)
    print("max time per orbit: %.1f s" % max(r["time"] for r in results))
