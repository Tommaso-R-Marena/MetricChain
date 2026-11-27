# validation of rn.kalmanson_search: (a) random circular-decomposable metrics with scrambled labels must be
# recognised; (b) agreement with brute force over all (n-1)!/2 orders on random integer matrices near Kalmanson.
import random, itertools
import numpy as np
from rn import kalmanson_search, brute_kalmanson, is_kalmanson

rng = random.Random(5)
okA = okB = 0
nA = nB = 0
yes = no = 0
for trial in range(400):
    n = rng.randint(5, 12)
    # random circular split metric for the identity order, random support
    D = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.5:
                w = rng.randint(1, 5)
                U = set(range(i + 1, j + 1))
                for a in range(n):
                    for b in range(n):
                        if (a in U) != (b in U):
                            D[a, b] += w
    perm = list(range(n)); rng.shuffle(perm)
    D2 = D[np.ix_(perm, perm)]
    r = kalmanson_search(D2)
    nA += 1
    okA += (r is not None and is_kalmanson(D2, r))
for trial in range(300):
    n = rng.randint(5, 8)
    D = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.6:
                w = rng.randint(1, 3)
                U = set(range(i + 1, j + 1))
                for a in range(n):
                    for b in range(n):
                        if (a in U) != (b in U):
                            D[a, b] += w
    # perturb a few entries
    for _ in range(rng.randint(0, 3)):
        a, b = rng.sample(range(n), 2)
        e = rng.choice([-1, 1])
        D[a, b] += e; D[b, a] += e
    perm = list(range(n)); rng.shuffle(perm)
    D2 = D[np.ix_(perm, perm)]
    r = kalmanson_search(D2)
    bf = brute_kalmanson(D2)
    nB += 1
    okB += ((r is None) == (len(bf) == 0)) and (r is None or is_kalmanson(D2, r))
    yes += r is not None; no += r is None
print(f"(a) scrambled circular-decomposable metrics recognised: {okA}/{nA}")
print(f"(b) agreement with brute force on perturbed matrices: {okB}/{nB}  (orders exist in {yes}, none in {no})")
