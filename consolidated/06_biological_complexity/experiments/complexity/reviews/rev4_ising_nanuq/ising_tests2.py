"""Theorem 2, second test: instances with twins AND true anti-twins, biased towards non-exposed type sets;
the unreduced problem is solved over all 2^(n-1) states (no gauge applied before solving)."""
import itertools, random, json, time
from fractions import Fraction
import numpy as np
from ising_core import *

rng = random.Random(31337)
K5 = json.load(open("k5_results.json"))
types5 = [(1,) + t for t in itertools.product([1, -1], repeat=4)]
types4 = [(1,) + t for t in itertools.product([1, -1], repeat=3)]
bad5 = [[types5[i] for i in range(16) if r["mask"] >> i & 1] for r in K5 if not r["exposed"]]
good5 = [[types5[i] for i in range(16) if r["mask"] >> i & 1] for r in K5 if r["exposed"] and r["ntypes"] <= 7]
bad4 = [[t for t in types4 if t[1] * t[2] * t[3] == s] for s in (1, -1)]

def random_group_image(ts, K):
    perm = rng.sample(range(K), K)
    sg = [rng.choice([1, -1]) for _ in range(K)]
    return [tuple(sg[i] * t[perm[i]] for i in range(K)) for t in ts]

st = dict(total=0, exposed=0, notexp=0, mismatch=0, antitwin_pairs=0, maxn=0, cert_fail=0)
t0 = time.time()
for it in range(700):
    r = rng.random()
    if r < 0.3:
        ts, K = rng.choice(bad4), 4
    elif r < 0.75:
        ts, K = rng.choice(bad5), 5
    else:
        ts, K = rng.choice(good5), 5
    ts = random_group_image(ts, K)
    mt = len(ts)
    n = rng.randint(mt + 1, min(12, mt + 5))
    cols = list(ts) + [rng.choice(ts) for _ in range(n - mt)]
    rng.shuffle(cols)
    signs = [rng.choice([1, -1]) for _ in cols]
    cols = [tuple(v * s for v in c) for c, s in zip(cols, signs)]
    V = states_from_types(cols)
    assert distinct_states(V)
    # count anti-twin pairs actually present
    for i in range(n):
        for j in range(i + 1, n):
            if all(x[i] == -x[j] for x in V):
                st["antitwin_pairs"] += 1
    Vr, T = twin_reduce(V)
    assert len(Vr[0]) == mt and distinct_states(Vr)
    full = decide(V)
    red = decide(Vr)
    st["total"] += 1
    st["maxn"] = max(st["maxn"], n)
    st["exposed"] += full.exposed
    st["notexp"] += (not full.exposed)
    if full.exposed != red.exposed:
        st["mismatch"] += 1
    if not full.exposed:
        # Theorem 1 bound on the support and Proposition 5 for the unreduced system
        if len(full.mu) > n * (n - 1) // 2 + 1:
            st["cert_fail"] += 1
        Y, _ = sign_vectors_in_span(V)
        if any(y not in set(Y) for y in full.mu):
            st["cert_fail"] += 1
print("Theorem 2, biased test:", st, "time %.0f s" % (time.time() - t0))
