"""r10_03: exact small-n enumerations (Y_REPORT sections 4.2, 5.4(b), 7).  Own code.
Binary symmetric chain, Hamming slope u=1, ALL vertices of the Lipschitz polytope of the
n-chain (n<=4: 990; n=5: 395094), duality brackets for F*_n(t), E_n, a_n.
 A. n<=4: F*_n(t), E_n, a_n; weight of the optimum on non-additive vertices; site-wise-only values.
 B. E_n against ln Z_n(h)/Z_n(0).
 C. structure of the Renyi centre at n=4, t=0.45: I(x1;x3|x2), Walsh norms of gamma*.
 D. n=5: dual certificate of the site-wise centre over all 395094 vertices.
usage: python3 r10_03_small_n.py [A] [D]
"""
import sys
import time
import numpy as np
from r10lib import *

u = 1.0
parts = sys.argv[1:] or ["A", "D"]


def is_additive_rows(V, n):
    g = V - V[:, [0]]
    c = np.stack([g[:, 1 << i] for i in range(n)], axis=1).astype(float)
    lin = c @ bits(n).astype(float).T
    return np.all(np.abs(g - lin) < 1e-9, axis=1)


def lnZratio(n, p, h):
    """ln E_pi exp(h m), m = sum of spins, for the stationary chain."""
    P = np.array([[1 - p, p], [p, 1 - p]])
    D = np.diag([np.exp(h), np.exp(-h)])
    v = np.array([0.5, 0.5]) @ D
    for _ in range(n - 1):
        v = v @ P @ D
    return np.log(v.sum())


def cond_mi_13_2(Q, n):
    """I(x1; x3 | x2) under Q (sites 0,1,2 of the n-chain), nats."""
    q = Q.reshape((2,) * n)            # axis order: reshape of index k = sum x_i 2^i -> last axis is site 0
    q = q.transpose(tuple(range(n - 1, -1, -1)))   # now axis i = site i
    q3 = q.sum(axis=tuple(range(3, n))) if n > 3 else q
    p2 = q3.sum(axis=(0, 2))
    p12 = q3.sum(axis=2)
    p23 = q3.sum(axis=0)
    mi = 0.0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                mi += q3[a, b, c] * np.log(q3[a, b, c] * p2[b] / (p12[a, b] * p23[b, c]))
    return mi


def walsh(g, n):
    s = spins(n).astype(float)
    out = {}
    for k in range(1 << n):
        S = [i for i in range(n) if (k >> i) & 1]
        chi = np.prod(s[:, S], axis=1) if S else np.ones(1 << n)
        out[tuple(S)] = float((g * chi).mean())
    return out


if "A" in parts:
    t0 = time.time()
    print("=== A/B/C: n <= 4, all vertices ===")
    for p in (0.4, 0.3, 0.1):
        for n in (1, 2, 3, 4):
            pi = binary_chain_law(n, p)
            V = hom_vertices(n).astype(float) * u
            add = is_additive_rows(V, n)
            W, lnZ = gibbs(pi, V)
            row = "p=%.1f n=%d |V|=%d:" % (p, n, len(V))
            for t in (0.25, 0.45, 0.65):
                br = renyi_bracket(W, t, tol=1e-12)
                bs = renyi_bracket(W[add], t, tol=1e-12)
                row += "  F*(%.2f)=[%.7f,%.7f] nonadd w=%.1e sitewise-only=%.7f" % (
                    t, br["lower"], br["upper"], br["M"][~add].sum() if (~add).any() else 0.0, bs["lower"])
            print(row)
            th = threshold_bracket(W, tol=1e-12)
            ths = threshold_bracket(W[add], tol=1e-12)
            ca = capacity_bracket(W, tol=1e-12)
            cas = capacity_bracket(W[add], tol=1e-12)
            ref = lnZratio(n, p, u / 2)
            print("     E_n=[%.9f,%.9f] (nonadd w=%.1e; sitewise-only %.9f)   ln Z_n(h)/Z_n(0)=%.9f  diff=%.1e"
                  % (th["lower"], th["upper"], th["M"][~add].sum() if (~add).any() else 0.0, ths["lower"], ref, th["upper"] - ref))
            print("     a_n=[%.7f,%.7f] (nonadd w=%.4f; sitewise-only [%.7f,%.7f])"
                  % (ca["lower"], ca["upper"], ca["M"][~add].sum() if (~add).any() else 0.0, cas["lower"], cas["upper"]))
            if n == 4:
                # which non-additive vertices carry weight in the capacity optimum
                M = ca["M"]
                order = np.argsort(-M)[:6]
                x = bits(n); wt = x.sum(axis=1)
                for k in order:
                    if M[k] > 1e-6:
                        f = V[k] - V[k][0]
                        tag = "additive" if add[k] else "NON-additive"
                        isdist = np.allclose(f - f.min(), (-np.minimum(wt, n - wt)) - (-np.minimum(wt, n - wt)).min())
                        print("        weight %.4f  %s  f=%s%s" % (M[k], tag, f.astype(int).tolist(),
                                                                  "   = -min(|x|,4-|x|)+const" if isdist else ""))
                # C: structure of the Renyi centre at t = 0.45
                t = 0.45
                br = renyi_bracket(W, t, tol=1e-13)
                Q = br["Q"]; M = br["M"]
                sup = np.nonzero(M > 1e-6)[0]
                print("     C: t=0.45: support of M*: %d labels, weights %s" % (len(sup), np.round(M[sup], 4).tolist()))
                for k in sup:
                    f = V[k] - V[k][0]
                    print("        label f=%s additive=%s" % (f.astype(int).tolist(), bool(add[k])))
                gam = -np.log(Q / pi)
                gam -= gam.mean()
                m = spins(n).sum(axis=1).astype(float)
                model = -np.log(np.cosh(t * (u / 2) * m)) / t
                model -= model.mean()
                print("        max |gamma* - (-(1/t) ln cosh(t h m))| = %.2e" % np.abs(gam - model).max())
                wc = walsh(gam, n)
                norms = [np.sqrt(sum(v * v for S, v in wc.items() if len(S) == k)) for k in range(1, n + 1)]
                print("        Walsh l2-norms of gamma* by order 1..4: %s ; nn pair coefficient %.4f ; I(x1;x3|x2) under Q* = %.3e (under pi: %.1e)"
                      % (np.round(norms, 4).tolist(), wc[(0, 1)], cond_mi_13_2(Q, n), cond_mi_13_2(pi, n)))
    print("F*_n(0.45)/n at p=0.4, n=1..4:", end=" ")
    for n in (1, 2, 3, 4):
        pi = binary_chain_law(n, 0.4)
        W, _ = gibbs(pi, hom_vertices(n).astype(float) * u)
        br = renyi_bracket(W, 0.45, tol=1e-12)
        print("%.5f" % (br["upper"] / n), end=" ")
    print("\ntime A: %.1fs" % (time.time() - t0))

if "D" in parts:
    t0 = time.time()
    print("=== D: n = 5, all 395094 vertices ===")
    n = 5
    V8 = hom_vertices(n)
    addm = is_additive_rows(V8.astype(float), n)
    print("vertices %d, additive %d  (%.1fs)" % (len(V8), addm.sum(), time.time() - t0))
    V = V8.astype(float) * u
    for p in (0.3, 0.1):
        pi = binary_chain_law(n, p)
        W, lnZ = gibbs(pi, V)
        Ws = W[addm]
        lw = np.log(W)
        for t in (0.45, 0.65, 0.85):
            bs = renyi_bracket(Ws, t, tol=1e-12)
            c = (W ** t) @ (bs["Q"] ** (1 - t))
            dual_all = -np.log(c.min())
            print("p=%.1f t=%.2f: site-wise optimum [%.7f,%.7f]; dual value of the site-wise centre over ALL vertices %.7f  -> %s"
                  % (p, t, bs["lower"], bs["upper"], dual_all,
                     "certificate: site-wise optimal" if dual_all - bs["lower"] < 1e-8 else "NOT a certificate (gap %.5f)" % (dual_all - bs["lower"])))
            if dual_all - bs["lower"] > 1e-8:
                # column generation for the true F*_5(t)
                act = np.nonzero(addm)[0].tolist()
                M = None
                for rnd in range(60):
                    Wa = W[act]
                    br = renyi_bracket(Wa, t, tol=1e-11, iters=200000)
                    c = (W ** t) @ (br["Q"] ** (1 - t))
                    up = -np.log(c.min())
                    if up - br["lower"] < 1e-8:
                        break
                    new = [k for k in np.argsort(c)[:200] if k not in set(act)]
                    act += new
                Ma = br["M"]
                wna = Ma[~addm[np.array(act)]].sum()
                print("        column generation: F*_5(%.2f) in [%.7f, %.7f] with %d active labels; weight on non-additive %.4f"
                      % (t, br["lower"], up, len(act), wna))
        # E
        ths = threshold_bracket(Ws, tol=1e-12)
        kl = float(ths["Q"] @ np.log(ths["Q"])) - lw @ ths["Q"]
        ref = lnZratio(n, p, u / 2)
        print("p=%.1f E: site-wise [%.9f,%.9f]; dual over ALL vertices %.9f; ln Z_5(h)/Z_5(0)=%.9f (diff %.1e)"
              % (p, ths["lower"], ths["upper"], kl.max(), ref, kl.max() - ref))
        # a
        cas = capacity_bracket(Ws, tol=1e-12)
        klr = (W * (lw - np.log(cas["Q"])[None, :])).sum(axis=1)
        print("p=%.1f a: site-wise [%.7f,%.7f]; dual over ALL vertices %.7f -> %s"
              % (p, cas["lower"], cas["upper"], klr.max(), "certificate" if klr.max() - cas["lower"] < 1e-8 else "NOT a certificate"))
        del W, lw
    print("time D: %.1fs" % (time.time() - t0))
