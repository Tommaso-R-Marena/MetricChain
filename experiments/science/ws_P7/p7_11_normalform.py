"""
P7, a numerical check of Proposition P7.1(c): "shares with allowances" is the normal form of a leaf certificate.

For every leaf box B of the smallest tree of each gap analysis (out/p7_02_branch.json: the working site with the
fewest states, or for Leu16 the depth-two tree), with the anchor y = the reference with the branching states of
the leaf inserted, the linear programme of the normal form is solved:

    minimise  sum_j e_j + sum_{j<k} e_jk     over shares s_jk(b) (b != y_j; any sign) and allowances e >= 0  with
        sum_{k != j} s_jk(b) <= A^y_j(b) + e_j ,   s_jk(b) >= -e_jk ,   s_jk(b) + s_kj(c) >= -M^y_jk(b, c) - e_jk

(A^y, M^y: excitation energies and second differences of F at y, free sites of the leaf only).  P7.1(c) says:
a certificate for the bound lambda exists iff the least total allowance is <= F(y) - lambda, i.e.

    least total allowance  =  F(y) - (value of the pairwise relaxation of the leaf) .

The right side is computed independently by the dual programme in the kernel's variables (p7lib.dual_lp).

usage: python3 -B p7_11_normalform.py > logs/p7_11_normalform.log   (last line "DONE p7_11_normalform")
"""
import sys, os, json, time
sys.dont_write_bytecode = True
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog
import p7lib as L7
from p7lib import PM, L4

t00 = time.time()
print(f"p7_11_normalform  started {L7.now()}")
five = json.load(open(os.path.join(L7.HERE, "out", "p7_01_five.json")))["gaps"]
branch = {(r["instance"], r["tau"]): r for r in json.load(open(os.path.join(L7.HERE, "out", "p7_02_branch.json")))}


def least_allowance(pmy, B):
    """the normal-form programme at the anchor pmy.r on the box B (which contains the anchor)."""
    n = pmy.n
    free = [j for j in range(n) if len(B[j]) >= 2]
    off = {}; nv = 0
    for j in free:
        for k in free:
            if j != k:
                off[(j, k)] = nv; nv += pmy.shape[j]
    ej = {j: nv + q for q, j in enumerate(free)}; nv += len(free)
    ejk = {}
    for a_, j in enumerate(free):
        for k in free[a_ + 1:]:
            ejk[(j, k)] = nv; nv += 1
    lb = np.full(nv, -np.inf); ub = np.full(nv, np.inf)
    for (j, k), o in off.items():                       # shares exist for changed states of the box only
        for b in range(pmy.shape[j]):
            if b == pmy.r[j] or b not in B[j]:
                lb[o + b] = ub[o + b] = 0.0
    for v in list(ej.values()) + list(ejk.values()):
        lb[v] = 0.0
    rows, cols, vals, rhs = [], [], [], []
    nr = 0

    def add(cs, vs, r):
        global_rows.append((cs, vs, r))
    global_rows = []
    for j in free:
        for b in B[j]:
            if b == pmy.r[j]:
                continue
            cs = [off[(j, k)] + b for k in free if k != j] + [ej[j]]
            add(cs, [1.0] * (len(cs) - 1) + [-1.0], pmy.A[j][b])                      # load
    for (j, k), e in ejk.items():
        for b in B[j]:
            if b != pmy.r[j]:
                add([off[(j, k)] + b, e], [-1.0, -1.0], 0.0)                         # sign: s_jk(b) >= -e_jk
        for c in B[k]:
            if c != pmy.r[k]:
                add([off[(k, j)] + c, e], [-1.0, -1.0], 0.0)
        T = pmy.M[(j, k)]
        for b in B[j]:
            if b == pmy.r[j]:
                continue
            for c in B[k]:
                if c != pmy.r[k]:
                    add([off[(j, k)] + b, off[(k, j)] + c, e], [-1.0, -1.0, -1.0], T[b, c])   # cover
    for q, (cs, vs, r) in enumerate(global_rows):
        rows += [q] * len(cs); cols += cs; vals += vs; rhs.append(r)
    Aub = sp.csr_matrix((vals, (rows, cols)), shape=(len(global_rows), nv))
    cost = np.zeros(nv)
    for v in list(ej.values()) + list(ejk.values()):
        cost[v] = 1.0
    res = linprog(cost, A_ub=Aub, b_ub=np.array(rhs), bounds=np.c_[lb, ub], method="highs")
    return float(res.fun), nv, len(global_rows)


nleaf = 0; worst = 0.0
for g in five:
    iname = f"{g['family']}{g['nres']}/{g['bb']}"
    br = branch[(iname, g["tau"])]
    inst = L4.load_instance(g["tag"], float(g["tau"]))
    Lmod, x0, E, C = L7.second_order_grid(inst, g["split"])
    pm = PM.from_grid(Lmod, x0)
    G = pm.grid()                                        # F = L - L(x0) as an exactly pairwise grid
    D = pm.full_domain()
    boxes = []
    if br["working"]:
        i = br["tree_site"]
        boxes = [(L7.fix(D, i, a), {i: int(a)}) for a in pm.dom[i]]
    else:                                                # Leu16: the three leaves of the depth-two tree (branch on 1, then on 6)
        boxes = [(L7.fix(D, 1, 1 - x0[1]), {1: 1 - x0[1]}), (L7.fix(L7.fix(D, 1, x0[1]), 6, 1 - x0[6]), {1: x0[1], 6: 1 - x0[6]}),
                 (L7.fix(L7.fix(D, 1, x0[1]), 6, x0[6]), {1: x0[1], 6: x0[6]})]
    dmax = 0.0
    for B, fx in boxes:
        y = list(x0)
        for i_, a in fx.items():
            y[i_] = int(a)
        y = tuple(y)
        pmy = PM.from_grid(G, y)                          # difference form at the anchor
        tot, nv, nrow = least_allowance(pmy, B)
        relax = L7.dual_lp(pm, B)["val"]                  # value of the leaf's relaxation, relative to F(x0) = 0
        Fy = float(G[y])
        d = abs(tot - (Fy - relax))
        dmax = max(dmax, d); worst = max(worst, d); nleaf += 1
    print(f"{iname} tau {g['tau']} split {g['split']}: {len(boxes)} leaves; largest |least total allowance - (F(anchor) - relaxation value)| = {dmax:.2e}")
print(f"\n{nleaf} leaves; largest difference {worst:.2e} kcal/mol (floating point; P7.1(c) predicts 0)")
assert worst < 1e-7
print(f"[{time.time() - t00:.0f}s] finished {L7.now()}")
print("DONE p7_11_normalform")
