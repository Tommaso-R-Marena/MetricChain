#!/usr/bin/env python3
"""Coordinator's checks of workstream P7 before publication -- written from the report's description of the format
(P7_REPORT.md section 5.1-5.2); none of the workstream's code is imported.

For each of the nine certificate files ws_P7/out/p7_02_cert*.json (integers in units of 2^-40 kcal/mol):
  (1) my own checker: walk the tree with the current box; at a branch every state of the current domain of the site
      must have a child; at a leaf, on the CURRENT box (not the box stored with the leaf):
          U_i <= H_i(a) + sum_j m_ij(a),   P2_ij <= J_ij(a,b) - m_ij(a) - m_ji(b),   0 <= sum U + sum P2,
      in Python integers -- additions and comparisons only;
  (2) two controls that must be REJECTED: the bound raised by one unit; the first leaf alone on the whole domain;
  (3) brute force: the published instance evaluated at every state of the domain (int64): its minimum must be 0,
      attained at the reference -- the statement the tree certifies;
  (4) the value of the pairwise (local-polytope) relaxation at the root by my own linear programme (HiGHS, floating
      point): it must be NEGATIVE (the gap: no shares at the root) and equal the report's number.
Then Proposition P7.5 at n = 4 (ring, w = 7/4, R = 10) with the same linear programme: the root and every one-site
branching must fail, a depth-two tree must succeed.
Run:  python3 -B p7_adoption_check.py > p7_adoption_check.log       (under a minute)
"""
import os, sys, json, glob, itertools, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "ws_P7", "out"))
UNIT = 2.0 ** -40


def check_leaf(cert, leaf, box, bound):
    n = len(cert["shape"]); H, J = cert["H"], cert["J"]; U, P2, m = leaf["U"], leaf["P2"], leaf["m"]
    nadd = 0
    for i in range(n):
        for a in box[i]:
            s = H[i][a]
            for j in range(n):
                if j != i: s += m[f"{i},{j}"][a]; nadd += 1
            if U[i] > s: return False, nadd
    for i in range(n):
        for j in range(i + 1, n):
            Jij = J[f"{i},{j}"]; mij, mji = m[f"{i},{j}"], m[f"{j},{i}"]; p = P2[f"{i},{j}"]
            for a in box[i]:
                for b in box[j]:
                    nadd += 2
                    if p > Jij[a][b] - mij[a] - mji[b]: return False, nadd
    return bound <= sum(U) + sum(P2.values()), nadd


def verify(cert, node, box, bound, stats):
    if "leaf" in node:
        ok, nadd = check_leaf(cert, cert["leaves"][node["leaf"]], box, bound); stats["leaf_checks"] += 1; stats["additions"] += nadd
        return ok
    i = node["site"]
    for a in box[i]:
        ch = node["children"].get(str(a))
        if ch is None: return False
        nb = list(box); nb[i] = [a]
        if not verify(cert, ch, nb, bound, stats): return False
    return True


def brute(cert):
    shape = cert["shape"]; n = len(shape)
    grids = np.meshgrid(*[np.arange(k) for k in shape], indexing="ij")
    F = np.zeros(shape, dtype=np.int64)
    for i in range(n): F += np.array(cert["H"][i], dtype=np.int64)[grids[i]]
    for i in range(n):
        for j in range(i + 1, n): F += np.array(cert["J"][f"{i},{j}"], dtype=np.int64)[grids[i], grids[j]]
    return int(F.min()), int((F == F.min()).sum()), int(F[tuple(cert["ref"])]), int(F.size)


def relaxation(shape, H, J, box=None):
    """value of the local-polytope relaxation of min sum_i H_i + sum_{i<j} J_ij over the box (floats)."""
    n = len(shape); box = box or [list(range(k)) for k in shape]
    off1 = {}; nv = 0
    for i in range(n):
        for a in box[i]: off1[(i, a)] = nv; nv += 1
    off2 = {}
    for i in range(n):
        for j in range(i + 1, n):
            for a in box[i]:
                for b in box[j]: off2[(i, j, a, b)] = nv; nv += 1
    c = np.zeros(nv)
    for (i, a), v in off1.items(): c[v] = H[i][a]
    for (i, j, a, b), v in off2.items(): c[v] = J[(i, j)][a][b]
    rows = n + sum(len(box[i]) + len(box[j]) for i in range(n) for j in range(i + 1, n))
    A = lil_matrix((rows, nv)); rhs = np.zeros(rows); r = 0
    for i in range(n):
        for a in box[i]: A[r, off1[(i, a)]] = 1.0
        rhs[r] = 1.0; r += 1
    for i in range(n):
        for j in range(i + 1, n):
            for a in box[i]:
                for b in box[j]: A[r, off2[(i, j, a, b)]] = 1.0
                A[r, off1[(i, a)]] = -1.0; r += 1
            for b in box[j]:
                for a in box[i]: A[r, off2[(i, j, a, b)]] = 1.0
                A[r, off1[(j, b)]] = -1.0; r += 1
    res = linprog(c, A_eq=A.tocsr(), b_eq=rhs, bounds=(0, None), method="highs")
    assert res.status == 0, res.message
    return float(res.fun)


t0 = time.time()
print("# file | variant | sites, states | my checker: accepted (leaf checks, additions) | controls rejected (bound + 1 unit; first leaf alone) | "
      "brute force: min, attained at, value at the reference | relaxation at the root (kcal/mol; negative = no shares)")
allok = True
for fn in sorted(glob.glob(os.path.join(OUT, "p7_02_cert*.json"))):
    cert = json.load(open(fn)); shape = cert["shape"]; n = len(shape)
    full = [list(range(k)) for k in shape]
    st = dict(leaf_checks=0, additions=0); ok = verify(cert, cert["tree"], full, 0, st)
    c1 = verify(cert, cert["tree"], full, 1, dict(leaf_checks=0, additions=0))
    c2 = verify(cert, {"leaf": 0}, full, 0, dict(leaf_checks=0, additions=0))
    mn, nmin, fref, size = brute(cert)
    Jf = {tuple(int(v) for v in key.split(",")): np.array(val, dtype=float) * UNIT for key, val in cert["J"].items()}
    Hf = [np.array(v, dtype=float) * UNIT for v in cert["H"]]
    rel = relaxation(shape, Hf, Jf)
    good = ok and (not c1) and (not c2) and mn == 0 and fref == 0 and rel < 0
    allok &= good
    print(f"{os.path.basename(fn)} | {cert['variant']} | {n} sites, {size} states | {ok} ({st['leaf_checks']}, {st['additions']}) | {not c1}; {not c2} | "
          f"min {mn}, at {nmin} state(s), reference {fref} | {rel:.6f}   [{time.time() - t0:.0f}s]", flush=True)
print(f"all nine: accepted, both controls rejected, minimum 0 at the reference, relaxation negative at the root: {allok}")

# ---- Proposition P7.5 at n = 4
n, w, R = 4, 1.75, 10.0
ring = {(0, 1), (1, 2), (2, 3), (0, 3)}
H = [np.array([0.0, 1.0]) for _ in range(n)]                       # state 1 = changed
J = {(i, j): np.array([[0.0, 0.0], [0.0, (-w if (i, j) in ring else R)]]) for i in range(n) for j in range(i + 1, n)}
F = lambda x: sum(x) + sum(J[(i, j)][x[i]][x[j]] for i in range(n) for j in range(i + 1, n))
vals = sorted((F(x), x) for x in itertools.product((0, 1), repeat=n))
print(f"ring n = 4, w = 7/4, R = 10: minimum {vals[0][0]} at {vals[0][1]}, second value {vals[1][0]} (unique minimiser: {vals[1][0] > vals[0][0]})")
root = relaxation([2] * n, H, J)
print(f"   root: relaxation value {root:.4f} (negative: no shares)")
one = []
for i in range(n):
    leafs = []
    for a in (0, 1):
        box = [[0, 1]] * n; box = [list(b) for b in box]; box[i] = [a]; leafs.append(relaxation([2] * n, H, J, box))
    one.append(min(leafs)); print(f"   branch on site {i}: leaf values (unchanged, changed) = {leafs[0]:.4f}, {leafs[1]:.4f} -> certifies: {min(leafs) >= -1e-9}")
two = []
for i, j in itertools.combinations(range(n), 2):
    b1 = [[0, 1] for _ in range(n)]; b1[i] = [1]
    b2 = [[0, 1] for _ in range(n)]; b2[i] = [0]; b2[j] = [1]
    b3 = [[0, 1] for _ in range(n)]; b3[i] = [0]; b3[j] = [0]
    v = [relaxation([2] * n, H, J, b) for b in (b1, b2, b3)]; two.append((min(v) >= -1e-9, (i, j), v))
print("   depth two, three leaves (i changed | i unchanged, j changed | both unchanged): " + "; ".join(f"sites {ij}: {'certifies' if ok else 'fails'} ({v[0]:.3f}, {v[1]:.3f}, {v[2]:.3f})" for ok, ij, v in two))
print(f"   -> no shares at the root: {root < -1e-9}; no single site certifies: {all(v < -1e-9 for v in one)}; a depth-two tree with three leaves certifies: {any(ok for ok, _, _ in two)}")
print(f"ALL DONE {time.time() - t0:.0f} s")
