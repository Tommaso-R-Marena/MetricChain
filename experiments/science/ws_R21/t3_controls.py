"""T3 — controls of the chimera search: cases in which chimeras MUST be found, and a case in which
identification fails WITHOUT a chimera.  Own code; same two methods as T2 (LM multistart, EXACT).

 (a) K4+deg2 (rigid, not globally rigid, rigidity matroid NOT connected), generic pairs: a splice is
     predicted realisable iff it is constant on the K4 block and the two pendant radii satisfy the
     triangle inequality with the base edge (closed form, coded independently).
 (b) K5-e (generically globally rigid, connected matroid) with two conformers that SHARE the rigid
     triangle {0,1,2} and differ in the positions of vertices 3 and 4: predicted chimeras
     (T,P3,P4') and (T,P3',P4); the two ensembles 1/2(x1+x2), 1/2(y+y') have the same edge laws.
     Same conformers on K5 (edge 34 measured): no chimera expected.
 (c) 2K4_edge and 2K4_2sum (rigid, redundantly rigid, NOT globally rigid, matroid CONNECTED),
     generic pairs: no chimera expected (E5(a)), although K = 1 already fails (flip).
 (d) K4 (generically globally rigid): an explicit rational pair of frameworks with NO common edge
     length whose two complementary splices are realisable (a switching component), and 20 random
     members of the same family in which each conformer alone is in general position.
"""
import sys
from fractions import Fraction as Fr
import numpy as np
from r21_common import *

rng = np.random.default_rng(2103)
STARTS = 30
print("T3 controls  start", now(), " LM starts =", STARTS)


def all_dist(P):
    return sqlen(P, complete(P.shape[0]))


def search(name, X, starts=STARTS):
    """All non-constant colourings for the conformers X (K,N,2).  Returns colourings, targets,
    LM residual, exact defect, and the best configurations of the exact method."""
    N, E = graph_table()[name]
    K = X.shape[0]
    Tc = sqlen(X, E)
    col = all_colourings(K, len(E))
    col = col[nonconstant(col)]
    T = splice_targets(Tc, col)
    best, _, _ = Realiser(N, E).multistart(T, starts, rng)
    ex, P = Constructor(name, N, E).defect(T)
    return col, T, Tc, best, ex, P


viol_total = 0

# ---------------------------------------------------------------- (a)
name = "K4+deg2"
N, E = graph_table()[name]
blk = [E.index(e) for e in complete(4)]
i04, i14, i01 = E.index((0, 4)), E.index((1, 4)), E.index((0, 1))
n_pairs, n_pred, n_lm, n_ex, miss_lm, miss_ex, fp_lm, fp_ex, pairs_with = 40, 0, 0, 0, 0, 0, 0, 0, 0
margin_min = np.inf
for trial in range(n_pairs):
    X = rng.standard_normal((2, N, 2))
    col, T, Tc, best, ex, _ = search(name, X)
    const_blk = np.all(col[:, blk] == col[:, blk[:1]], axis=1)
    i = col[:, blk[0]]
    base = np.sqrt(Tc[i, i01])
    r0, r1 = np.sqrt(T[:, i04]), np.sqrt(T[:, i14])
    tri = (np.abs(r0 - r1) <= base) & (base <= r0 + r1)
    margin = np.minimum(base - np.abs(r0 - r1), r0 + r1 - base)
    pred = const_blk & tri
    margin_min = min(margin_min, np.min(np.abs(margin[const_blk])))
    f_lm, f_ex = best < 1e-6, ex < 1e-9
    n_pred += pred.sum(); n_lm += f_lm.sum(); n_ex += f_ex.sum()
    miss_lm += np.sum(pred & ~f_lm); miss_ex += np.sum(pred & ~f_ex)
    fp_lm += np.sum(~pred & f_lm); fp_ex += np.sum(~pred & f_ex)
    pairs_with += int(pred.any())
print(f"(a) {name}: {n_pairs} generic pairs x 254 non-constant colourings. predicted chimeras (closed form) {n_pred}; "
      f"pairs with at least one: {pairs_with}/{n_pairs}")
print(f"    LM found {n_lm} (missed {miss_lm}, not predicted {fp_lm}); EXACT found {n_ex} (missed {miss_ex}, not predicted {fp_ex}); "
      f"smallest |triangle-inequality margin| among block-constant splices {margin_min:.2e}")
viol_total += miss_lm + miss_ex + fp_lm + fp_ex

# ---------------------------------------------------------------- (b)
for name in ("K5-e", "K5"):
    N, E = graph_table()[name]
    n_pairs = 20
    tot_pred = tot_lm = tot_ex = miss = fp = 0
    law_err = 0.0
    noncong = np.inf
    triv = 0
    for trial in range(n_pairs):
        X = rng.standard_normal((2, N, 2))
        X[1, :3] = X[0, :3]                       # shared rigid triangle {0,1,2}
        col, T, Tc, best, ex, P = search(name, X, starts=12)
        # distinct targets
        is_conf = (np.max(np.abs(T[:, None, :] - Tc[None, :, :]), axis=2) < 1e-12).any(axis=1)   # splice equals a conformer (trivial)
        star3 = [E.index((j, 3)) for j in range(3)]
        star4 = [E.index((j, 4)) for j in range(3)]
        c3 = np.all(col[:, star3] == col[:, star3[:1]], axis=1)
        c4 = np.all(col[:, star4] == col[:, star4[:1]], axis=1)
        if name == "K5-e":
            pred = c3 & c4 & (col[:, star3[0]] != col[:, star4[0]])
        else:
            pred = np.zeros(len(col), dtype=bool)
        f_lm, f_ex = (best < 1e-6) & ~is_conf, (ex < 1e-9) & ~is_conf
        triv += int(is_conf.sum())
        tot_pred += pred.sum(); tot_lm += f_lm.sum(); tot_ex += f_ex.sum()
        miss += np.sum(pred & ~f_lm) + np.sum(pred & ~f_ex)
        fp += np.sum(~pred & f_lm) + np.sum(~pred & f_ex)
        if name == "K5-e":
            Y = np.stack([np.vstack([X[0, :4], X[1, 4:]]), np.vstack([X[1, :4], X[0, 4:]])])   # (T,P3,P4'), (T,P3',P4)
            La = np.sort(sqlen(X, E), axis=0)
            Lb = np.sort(sqlen(Y, E), axis=0)
            law_err = max(law_err, np.max(np.abs(La - Lb)))
            for y in Y:
                for x in X:
                    noncong = min(noncong, np.max(np.abs(all_dist(y) - all_dist(x))))
    print(f"(b) {name}, two conformers sharing the triangle {{0,1,2}}: {n_pairs} pairs; splices equal to a conformer (trivial) {triv}; "
          f"predicted chimera colourings {tot_pred}; LM found {tot_lm}; EXACT found {tot_ex}; missed {miss}; not predicted {fp}")
    if name == "K5-e":
        print(f"    ensembles 1/2(x1+x2) and 1/2(y+y'), y=(T,P3,P4'), y'=(T,P3',P4): max difference of the sorted per-edge "
              f"squared lengths {law_err:.1e} (same laws); smallest max-difference of the full distance vectors between a "
              f"chimera and a conformer {noncong:.3f} (not congruent)")
    viol_total += miss + fp

# ---------------------------------------------------------------- (c)
for name in ("2K4_edge", "2K4_2sum"):
    N, E = graph_table()[name]
    n_pairs = 10
    found = 0
    gl, ge = [], []
    flip_err, flip_noncong = 0.0, np.inf
    for trial in range(n_pairs):
        X = rng.standard_normal((2, N, 2))
        col, T, Tc, best, ex, _ = search(name, X, starts=8)
        found += int(np.sum(best < 1e-6) + np.sum(ex < 1e-9))
        gl.append(best.min()); ge.append(ex.min())
        for x in X:                                # flip vertices 4,5 across the line through p0,p1
            u = (x[1] - x[0]) / np.linalg.norm(x[1] - x[0])
            q = x.copy()
            for v in (4, 5):
                w = x[v] - x[0]
                q[v] = x[0] + 2 * np.dot(w, u) * u - w
            flip_err = max(flip_err, np.max(np.abs(sqlen(q, E) - sqlen(x, E))))
            flip_noncong = min(flip_noncong, np.max(np.abs(all_dist(q) - all_dist(x))))
    print(f"(c) {name} (not globally rigid, connected matroid): {n_pairs} generic pairs x {len(col)} non-constant colourings: "
          f"chimeras found {found}; smallest LM residual {min(gl):.2e}, smallest exact defect {min(ge):.2e}")
    print(f"    flip of {{4,5}} about the line p0p1: max change of a measured squared length {flip_err:.1e}; smallest "
          f"max-change of an unmeasured one {flip_noncong:.3f}  => delta_x is not determined (K = 1), with no chimera")
    viol_total += found

# ---------------------------------------------------------------- (d)
name = "K4"
N, E = graph_table()[name]          # edges (0,1),(0,2),(0,3),(1,2),(1,3),(2,3); the special edge is (0,1)


def kite(s, x1, y1, dx, y2, cis):
    """vertices: 2 = (-s,0), 3 = (s,0), 0 = (x1,y1), 1 = (x1+dx, +-y2)"""
    return [(x1, y1), (x1 + dx, y2 if cis else -y2), (-s, 0), (s, 0)]


def sq_exact(P):
    return [(P[u][0] - P[v][0]) ** 2 + (P[u][1] - P[v][1]) ** 2 for (u, v) in E]


A = (Fr(1), Fr(1, 2), Fr(2), Fr(5, 2), Fr(3))
B = (Fr(2), Fr(1, 2), Fr(3, 2), Fr(1), Fr(4))
x1, x2 = kite(*A, True), kite(*B, False)
y, yp = kite(*A, False), kite(*B, True)
L = {k: sq_exact(v) for k, v in dict(x1=x1, x2=x2, y=y, yp=yp).items()}
print("(d) explicit rational example on K4 (exact arithmetic), edges", E)
for k in ("x1", "x2", "y", "yp"):
    print(f"    {k:2s} coordinates {[(str(a), str(b)) for a, b in dict(x1=x1, x2=x2, y=y, yp=yp)[k]]}  squared lengths {[str(t) for t in L[k]]}")
same_laws = all(sorted([L['x1'][e], L['x2'][e]]) == sorted([L['y'][e], L['yp'][e]]) for e in range(6))
no_common = all(L['x1'][e] != L['x2'][e] for e in range(6))
y_new = (L['y'] != L['x1']) and (L['y'] != L['x2']) and (L['yp'] != L['x1']) and (L['yp'] != L['x2'])
print(f"    exact checks: per-edge multisets of 1/2(x1+x2) and 1/2(y+y') equal: {same_laws}; x1, x2 have no common edge "
      f"length: {no_common}; y, y' are not congruent to x1 or x2 (K4 is complete): {y_new}")
viol_total += int(not (same_laws and no_common and y_new))
X = np.array([[[float(a), float(b)] for a, b in x1], [[float(a), float(b)] for a, b in x2]])
col, T, Tc, best, ex, _ = search(name, X)
pred = np.zeros(len(col), dtype=bool)
for q, c in enumerate(col):
    if (c[0] != c[1]) and np.all(c[1:] == c[1]):
        pred[q] = True
print(f"    search on (x1, x2): 62 non-constant colourings; predicted realisable 2; LM found {int(np.sum(best < 1e-6))} "
      f"(colourings {[''.join(map(str, c)) for c in col[best < 1e-6]]}); EXACT found {int(np.sum(ex < 1e-9))}; "
      f"smallest LM residual among the other 60: {np.min(best[~pred]):.3e}")
viol_total += int(np.sum(pred & ~(best < 1e-6)) + np.sum(pred & ~(ex < 1e-9)) + np.sum(~pred & (best < 1e-6)) + np.sum(~pred & (ex < 1e-9)))
# random members of the family
n_fam, ok_fam, law_fam, minlen = 20, 0, 0.0, np.inf
t = 0
while t < n_fam:
    s, xa, ya, dx, yb = rng.uniform(0.5, 2.0, 5)
    s2, xa2, ya2 = rng.uniform(0.5, 2.0, 3)
    yb2 = ya * yb / ya2
    dx2sq = dx * dx + ya * ya + yb * yb - ya2 * ya2 - yb2 * yb2
    if dx2sq <= 0.05:
        continue
    t += 1
    dx2 = np.sqrt(dx2sq)
    X = np.array([kite(s, xa, ya, dx, yb, True), kite(s2, xa2, ya2, dx2, yb2, False)])
    Y = np.array([kite(s, xa, ya, dx, yb, False), kite(s2, xa2, ya2, dx2, yb2, True)])
    col, T, Tc, best, ex, _ = search(name, X)
    pred = np.array([(c[0] != c[1]) and bool(np.all(c[1:] == c[1])) for c in col])
    good = (np.sum(pred & (best < 1e-6)) == 2) and (np.sum(pred & (ex < 1e-9)) == 2) and (np.sum(~pred & ((best < 1e-6) | (ex < 1e-9))) == 0)
    ok_fam += int(good)
    law_fam = max(law_fam, np.max(np.abs(np.sort(sqlen(X, E), axis=0) - np.sort(sqlen(Y, E), axis=0))))
    minlen = min(minlen, np.min(np.abs(Tc[0] - Tc[1])))
print(f"    family (5 + 3 free real parameters, 2 relations): {n_fam} random members; both complementary chimeras found by both "
      f"methods and nothing else: {ok_fam}/{n_fam}; max law mismatch {law_fam:.1e}; smallest |len_e(x1) - len_e(x2)| {minlen:.3f}")
viol_total += n_fam - ok_fam
print("total violations of the predictions in T3:", viol_total)
print("DONE t3_controls", now())
