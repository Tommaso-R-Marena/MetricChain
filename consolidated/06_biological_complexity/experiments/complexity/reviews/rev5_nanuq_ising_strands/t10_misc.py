# t10_misc.py -- REVIEWER'S OWN CODE: smaller statements of Section 7.2
import itertools, collections
from math import comb
from mybuild import bloblet_spec, build
from myblob import check_theorem12, formula12b

# (1) all bloblets N[kB,k1,k2] with 4..13 leaves: Theorem 12 / Corollary 13 from the explicit network
cnt = 0; bad = 0; neg = 0; zero = 0
for n in range(4, 14):
    s = n - 1
    for kB in range(s + 1):
        for k1 in range(s - kB + 1):
            k2 = s - kB - k1
            net = build(bloblet_spec(kB, k1, k2, src=('A',)))
            info = check_theorem12(net)
            cnt += 1
            if info['viol']: bad += 1; print("VIOLATION", (kB, k1, k2), info['viol'][:2])
            if k1 >= 1 and kB >= 2:
                pred = k1 + k2 - comb(kB - 1, 2) if k2 >= 1 else k1 + 1 - comb(kB - 2, 2)
                assert info['crit_values'] == [pred]
                neg += pred < 0; zero += pred == 0
            else:
                assert info['ncrit'] == 0
print("bloblets with 4..13 leaves:", cnt, " violations:", bad, " negative critical weight:", neg, " zero:", zero)

# (2) Remark 2 of 7.2: all size assignments with seven leaves in total (formula of Theorem 12(b))
def compositions(total, parts):
    if parts == 1:
        yield (total,); return
    for a in range(1, total - parts + 2):
        for r in compositions(total - a, parts - 1):
            yield (a,) + r
res = collections.Counter(); detail = []
for P in range(4, 8):
    for kB in range(2, P):
        for k1 in range(1, P - kB):
            k2 = P - 1 - kB - k1
            if k2 < 0: continue
            for sizes in compositions(7, P):
                beta = list(sizes[:kB]); xi = list(sizes[kB:kB + k1]); eta = sizes[kB + k1]; gamma = list(sizes[kB + k1 + 1:])
                v = formula12b(beta, xi, eta, gamma)
                if v < 0: res['negative'] += 1; detail.append(('neg', (kB, k1, k2), sizes, v))
                if v == 0: res['zero'] += 1; detail.append(('zero', (kB, k1, k2), sizes, v))
print("seven leaves: size assignments with critical weight < 0 / = 0:", dict(res))
for d in detail: print("   ", d)

# (3) Theorem 9(c) as instances of Theorem 12(b)
for s in range(0, 8):
    for t in range(0, 8):
        if s + t + 1 >= 2:
            assert formula12b([1] * (s + t + 1), [1], 1, [1]) == 2 - comb(s + t, 2)
        if s >= 1 and t >= 1:
            assert formula12b([1, t, s], [1], 1, [1]) == 2 - s * t
print("Theorem 9(c): both formulas are instances of Theorem 12(b) for 0 <= s,t <= 7")
