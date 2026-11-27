"""r10_09b: smallest explicit example (cones psi = d_H(., y0), u = 1) in which the TRUNCATED residual
max(psi, t) -- not only the level function t -- violates admissibility for Markov-type classes."""
import numpy as np
import importlib.util, sys
spec = importlib.util.spec_from_file_location("m9", "r10_09_markov_types.py")
# re-implement the three helpers here to avoid running the brute force on import
def bits(n):
    k = np.arange(1 << n)
    return ((k[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)
def markov_classes(n):
    x = bits(n); a, b = x[:, :-1].astype(int), x[:, 1:].astype(int)
    key = x[:, 0].astype(int)
    for (i, j) in ((0, 0), (0, 1), (1, 0), (1, 1)):
        key = key * (n + 1) + ((a == i) & (b == j)).sum(axis=1)
    return np.unique(key, return_inverse=True)[1]
def levels(psi, cls, q):
    t = np.empty_like(psi)
    for c in np.unique(cls):
        idx = np.nonzero(cls == c)[0]; v = np.sort(psi[idx])
        t[idx] = v[int(np.floor(q * len(idx) + 1e-12))]
    return t
found = False
for n in range(3, 8):
    X = bits(n); cls = markov_classes(n); N = 1 << n
    for y0 in range(N):
        psi = (X != X[y0][None, :]).sum(axis=1).astype(float)
        for q in (0.34, 0.5, 0.67):
            t = levels(psi, cls, q); tr = np.maximum(psi, t)
            for i in range(n):
                nb = np.arange(N) ^ (1 << i)
                viol = tr - tr[nb] - 1.0
                k = int(np.argmax(viol))
                if viol[k] > 1e-9:
                    a, b = k, nb[k]
                    s = lambda v: "".join(str(c) for c in X[v])
                    print("n=%d  y0=%s  q=%.2f:  a=%s (class %s, psi=%g, level %g, truncated %g)   b=%s (class %s, psi=%g, level %g, truncated %g)   d(a,b)=1,  psi^tr(a)-psi^tr(b) = %g > 1"
                          % (n, s(y0), q, s(a), [s(v) for v in np.nonzero(cls == cls[a])[0]], psi[a], t[a], tr[a],
                             s(b), [s(v) for v in np.nonzero(cls == cls[b])[0]], psi[b], t[b], tr[b], tr[a] - tr[b]))
                    print("        psi on class(a): %s ; psi on class(b): %s" % (psi[cls == cls[a]].tolist(), psi[cls == cls[b]].tolist()))
                    found = True
                    break
            if found: break
        if found: break
    if found: break
