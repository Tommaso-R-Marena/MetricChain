"""Control 3 of the brief (run: python3 -B test_controls.py).

(a) the routines of anlib.py against brute-force loops on small random grids with random masks;
(b) a synthetic residual that is EXACTLY pairwise in the site variables: c_ijk = 0 and zero
    remainder of the two-site fit (least squares, Chebyshev LP, anchored expansion);
(c) a random residual: c_ijk and the two-site remainder are of the size of the function;
(d) pairwise + a planted third-order term of known size: recovered;
(e) the star bound of theory report Thm 11.16 and the order-3 bound of Thm 11.18 hold on these
    random instances (a check of the implementation of c_ij, c_ijk and of the expansions).
"""
import itertools, math
import numpy as np
from anlib import *

rng = np.random.default_rng(11)


def brute(g, mask, order):
    """max |mixed difference| per site subset by explicit loops."""
    n = g.ndim
    out = {}
    for S in itertools.combinations(range(n), order):
        best = 0.0
        for x in itertools.product(*[range(k) for k in g.shape]):
            for alt in itertools.product(*[range(g.shape[s]) for s in S]):
                if any(alt[t] == x[S[t]] for t in range(order)):
                    continue
                val = 0.0; ok = True
                for bits in itertools.product((0, 1), repeat=order):
                    y = list(x)
                    for t in range(order):
                        if bits[t]:
                            y[S[t]] = alt[t]
                    y = tuple(y)
                    if not mask[y]:
                        ok = False; break
                    val += (-1) ** sum(bits) * g[y]
                if ok:
                    best = max(best, abs(val))
        out[S] = best
    return out


def random_pairwise(shape, scale1=1.0, scale2=1.0):
    n = len(shape)
    g = np.zeros(shape)
    for i in range(n):
        sh = [1] * n; sh[i] = shape[i]
        g = g + scale1 * rng.normal(size=shape[i]).reshape(sh)
    for i in range(n):
        for j in range(i + 1, n):
            sh = [1] * n; sh[i] = shape[i]; sh[j] = shape[j]
            g = g + scale2 * rng.normal(size=(shape[i], shape[j])).reshape(sh)
    return g


print("(a) anlib against brute force, random grids with random masks")
for shape in ((3, 2, 4), (2, 3, 2, 3)):
    g = rng.normal(size=shape)
    mask = rng.random(shape) > 0.2
    c, _, _ = first_order(g, mask)
    b1 = brute(g, mask, 1)
    C, _ = second_order(g, mask)
    b2 = brute(g, mask, 2)
    T = third_order(g, mask)
    b3 = brute(g, mask, 3)
    d1 = max(abs(c[i] - b1[(i,)]) for i in range(len(shape)))
    d2 = max(abs(C[i, j] - b2[(i, j)]) for (i, j) in b2)
    d3 = max(abs(T[t][0] - b3[t]) for t in b3)
    print(f"   shape {shape}, {int(mask.sum())} of {mask.size} points in the domain: max deviation order 1: {d1:.1e}, order 2: {d2:.1e}, order 3: {d3:.1e}")
    assert max(d1, d2, d3) < 1e-12

print("(b)-(e) synthetic residuals")
for shape in ((3, 4, 5, 3), (9, 9, 9), (3,) * 7):
    n = len(shape)
    full = np.ones(shape, dtype=bool)
    part = rng.random(shape) > 0.25
    gp = random_pairwise(shape)
    gr = rng.normal(size=shape) * gp.std()
    plant = np.zeros(shape)
    sh = [1] * n
    v0 = np.zeros(shape[0]); v0[1] = 1.0
    v1 = np.zeros(shape[1]); v1[0] = 1.0
    v2 = np.zeros(shape[2]); v2[2] = 1.0
    plant = 0.37 * v0.reshape([shape[0]] + [1] * (n - 1)) * v1.reshape([1, shape[1]] + [1] * (n - 2)) * v2.reshape([1, 1, shape[2]] + [1] * (n - 3))
    for name, g in (("exactly pairwise", gp), ("iid random", gr), ("pairwise + 0.37*[x0=1][x1=0][x2=2]", gp + plant)):
        for dname, mask in (("full product", full), ("random 75 % sub-domain", part)):
            T = third_order(g, mask)
            c3 = max(v[0] for v in T.values())
            fit = low_order_fits(g, mask, lp_limit=3000)
            x0 = tuple(int(v) for v in np.unravel_index(np.argmax(mask), shape))
            line = (f"   shape {shape}, {name:36s} on {dname:22s}: max c_ijk = {c3:.2e}; two-site fit remainder rms {fit.get('ls2_rms', float('nan')):.2e} "
                    f"max {fit.get('ls2_max', float('nan')):.2e}" + (f" sup-optimal {fit['sup2']:.2e}" if "sup2" in fit else "")
                    + f"; one-site rms {fit['ls1_rms']:.2e}; std {fit['std']:.2f}")
            if dname == "full product":
                C, _ = second_order(g, mask)
                rem1 = np.abs(g - star_part(g, x0))
                W = pair_weight(shape, x0, C)
                rem2 = np.abs(g - anchored2(g, x0))
                ch = changed(shape, x0)
                W3 = np.zeros(shape)
                for (i, j, k), v in T.items():
                    W3 = W3 + v[0] * ch[i] * ch[j] * ch[k]
                ok16 = bool((rem1 <= W + 1e-9).all()); ok18 = bool((rem2 <= W3 + 1e-9).all())
                line += (f"; star remainder max {rem1.max():.2e} <= bound max {W.max():.2e}: {ok16}; "
                         f"anchored order-2 remainder max {rem2.max():.2e} <= sum c_ijk bound max {W3.max():.2e}: {ok18}")
                assert ok16 and ok18
            print(line)
            if name == "exactly pairwise":
                assert c3 < 1e-10 and fit["ls2_max"] < 1e-8
            if name == "iid random":
                assert c3 > 0.5 * fit["std"] and fit["ls2_rms"] > 0.2 * fit["std"]
            if name.startswith("pairwise +"):
                assert abs(c3 - 0.37) < 1e-10
print("all controls passed")
