#!/usr/bin/env python3
"""More NO-instances for Lemma A2 (random 3DM instances that cover all elements but have no perfect matching)."""
import random, itertools, time
from eth_chain_test import build_4partition, exact_packing_exists, pm_3dm_index
rng = random.Random(77)
done = 0; t0 = time.time(); tried = 0
dist = {}
while done < 300:
    tried += 1
    q = rng.choice([2, 2, 3, 3, 3, 4])
    allt = [(i, j, k) for i in range(1, q + 1) for j in range(1, q + 1) for k in range(1, q + 1)]
    nt = rng.randint(q, min(8, len(allt)))
    T = sorted(rng.sample(allt, nt))
    cover = {('w', t[0]) for t in T} | {('x', t[1]) for t in T} | {('y', t[2]) for t in T}
    if len(cover) < 3 * q:
        continue
    if pm_3dm_index(q, T):
        continue
    items, B = build_4partition(q, T)
    sizes = [s for _, s in items]
    assert sum(sizes) == len(T) * B and all(5 * s > B and 3 * s < B for s in sizes)
    assert not exact_packing_exists(sizes, B, len(T)), ('LEMMA A2 FAILS (no-instance packs)', q, T)
    done += 1
    dist[(q, nt)] = dist.get((q, nt), 0) + 1
print('Lemma A2: 300 NO-instances (no perfect matching, all elements covered): no exact packing in any; (q,|T|) distribution', dict(sorted(dist.items())), '[%.0fs]' % (time.time() - t0))
