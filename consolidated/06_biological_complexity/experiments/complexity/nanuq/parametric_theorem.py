"""The parametric family rho = (c, s, a, o) on the class C: exact domain

      D = { o = s,  c >= 0,  c + s <= 2a,  a < s }.

(1) decomposition identity for parametric rho (global alpha = sum of local forms), on blow-ups of class systems;
(2) sufficiency: every local form occurring in C_{<=6} is >= 0 on the three extreme rays of the closure of D
    (0,2,1,2), (0,1,1,1), (1,1,1,1), the T4 forms are > 0 on D, and the forms of undisplayed splits vanish;
(3) necessity: witnesses whose split weight is m^2 * F(rho) + O(m) for F = o - s, s - o, 2a - c - s;
    the 4-cycle for a < s.
"""
import random
from fractions import Fraction as F
from itertools import combinations
from splitsys import *
from localcrit import dihedral_images, blowup
from twin_trees import A_systems, closure_systems
from parametric import param_d, param_alphas
from parametric_local import T, TP, displayed
from parametric_domain import local_forms, ev

def TQ(sig, a, u, b, z):
    """4-sets containing the three leaves a,u,b of a trivial split {u}: rho(a,u) + rho(u,b) - rho(a,b)"""
    from parametric_local import val, comb
    return comb((1, val(sig, a, u, b, z)), (1, val(sig, u, b, a, z)), (-1, val(sig, a, b, u, z)))

def local_alpha(n, sig, i, j):
    """2*alpha_ij as vector (c,s,a,o,const) from local forms"""
    U = []
    k = (i + 1) % n
    while True:
        U.append(k)
        if k == j:
            break
        k = (k + 1) % n
    V = [(j + 1 + t) % n for t in range(n - len(U))]
    def addv(acc, v, mult=1):
        return [x + mult * y for x, y in zip(acc, list(v) + [0] * (5 - len(v)))]
    if len(U) == 1 or len(V) == 1:
        if len(V) == 1:
            U, V = V, U
        u = U[0]; b, a = V[0], V[-1]
        acc = [0, 0, 0, 0, n - 2]
        for z, w in combinations(V[1:-1], 2):
            acc = addv(acc, TP(sig, a, u, b, z, w))
        for z in V[1:-1]:
            acc = addv(acc, TQ(sig, a, u, b, z))
        return tuple(2 * x for x in acc)
    u1, up, v1, vq = U[0], U[-1], V[0], V[-1]
    acc = [0, 0, 0, 0, 0]
    acc = addv(acc, T(sig, u1, up, v1, vq, None, None))
    for z in U[1:-1] + V[1:-1]:
        acc = addv(acc, T(sig, u1, up, v1, vq, z, None))
    for z, w in combinations(U[1:-1], 2):
        acc = addv(acc, T(sig, u1, up, v1, vq, z, w))
    for z, w in combinations(V[1:-1], 2):
        acc = addv(acc, T(sig, u1, up, v1, vq, z, w))
    for z in U[1:-1]:
        for w in V[1:-1]:
            acc = addv(acc, T(sig, u1, up, v1, vq, z, w))
    return tuple(2 * x for x in acc)

if __name__ == "__main__":
    rng = random.Random(3)
    C6 = sorted(closure_systems(6), key=lambda s: sorted(s))
    # (1) identity on blow-ups
    cnt = 0
    for _ in range(40):
        s0 = rng.choice(C6)
        mult = [rng.choice([1, 1, 2, 3]) for _ in range(6)]
        n, sig = blowup(6, s0, mult)
        D = param_d(n, sig)
        al = param_alphas(n, D)
        for (i, j), v in al.items():
            assert tuple(v) == local_alpha(n, sig, i, j), (n, i, j, v, local_alpha(n, sig, i, j))
            cnt += 1
    print("(1) parametric decomposition identity verified on", cnt, "split weights of 40 blow-ups (up to", 18, "leaves)")
    # (2) sufficiency
    forms, undisp = local_forms({n: closure_systems(n) for n in (4, 5, 6)})
    rays = [(0, 2, 1, 2), (0, 1, 1, 1), (1, 1, 1, 1)]
    tq = set()
    for s0 in closure_systems(5):
        for img in dihedral_images(5, s0):
            tq.add(TQ(set(img), 0, 1, 2, 3))
    for s0 in closure_systems(4):
        for img in dihedral_images(4, s0):
            tq.add(TQ(set(img), 0, 1, 2, 3))
    forms["TQ"] = tq
    print("    TQ forms (4-sets through the three leaves of a trivial split):", sorted(tq))
    ok = all(ev(v, r) >= 0 for k in forms for v in forms[k] for r in rays)
    interior = (F(1, 10), F(1), F(7, 10), F(1))          # a point of D
    t4pos = all(ev(v, interior) > 0 for v in forms["T4"])
    print("(2) all local forms of C_{<=6} are >= 0 on the extreme rays of cl(D):", ok,
          "| T4 forms:", sorted(forms["T4"]), "> 0 inside D:", t4pos,
          "| forms of undisplayed splits:", sorted(undisp))
    # (3) necessity witnesses
    def find_placement(target, kind):
        for s0 in C6:
            for img in dihedral_images(6, s0):
                s = set(img)
                if kind == "TM":
                    if displayed(s, 0, 2, 3, 5) and T(s, 0, 2, 3, 5, 1, 4) == target:
                        return s, (1, 4), (2, 5)       # z=1 in U, w=4 in V ; split U = {0,1,2} -> gaps
                else:
                    if displayed(s, 0, 3, 4, 5) and T(s, 0, 3, 4, 5, 1, 2) == target:
                        return s, (1, 2), (3, 5)
        return None
    for label, target, kind, rho in (("o > s  (form s - o)", (0, 1, 0, -1), "TM", (F(0), F(1), F(1, 2), F(11, 10))),
                                     ("o < s  (form o - s)", (0, -1, 0, 1), "TM", (F(0), F(1), F(1, 2), F(9, 10))),
                                     ("2a < c + s  (form 2a - c - s)", (-1, -1, 2, 0), "T6", (F(1, 2), F(1), F(1, 2), F(1)))):
        s, (z, w), _ = find_placement(target, kind)
        res = []
        for m in (1, 2, 3, 4, 5, 6):
            mult = [1] * 6
            mult[z] = m; mult[w] = m
            n, sig = blowup(6, s, mult)
            D = param_d(n, sig)
            al = param_alphas(n, D)
            # the split U|V of the placement after blow-up: U = image of {0..2} (TM) or {0..3} (T6)
            ucount = sum(mult[:3]) if kind == "TM" else sum(mult[:4])
            key = (n - 1, ucount - 1) if False else None
            # find the gap pair whose U side is the first `ucount` leaves
            target_mask = canon(n, (1 << ucount) - 1)
            v = None
            for (i, j), vv in al.items():
                if canon(n, split_mask(n, i, j)) == target_mask:
                    v = vv
            res.append((m, str(ev(v[:4], rho) + v[4]), v))
        print(f"(3) witness for {label}; rho = {tuple(str(x) for x in rho)}: (m, alpha, form):")
        for r in res:
            print("      ", r)
    # modified NANUQ on the witness family
    print("Modified NANUQ rho = (1/2, 1, 1/2, 1): c + s = 3/2 > 2a = 1, so it is outside D (see the third witness).")
