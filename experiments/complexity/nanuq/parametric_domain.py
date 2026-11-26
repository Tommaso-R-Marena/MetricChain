"""Parameter domain of the family rho = (c, s, a, o) on the class C (all galled outer-labeled planar networks)
and on the class A (hybrids with a leaf child).

(1) local forms on A_n and C_n, n <= 6;
(2) explicit networks showing that each inequality of the domain is necessary."""
from fractions import Fraction as F
from itertools import combinations
from splitsys import *
from localcrit import dihedral_images
from twin_trees import A_systems, closure_systems
from parametric import param_d, param_alphas
from parametric_local import T, TP, displayed

def local_forms(systems_by_n):
    forms = {"T4": set(), "T5": set(), "T6": set(), "TM": set(), "TP": set()}
    undisp = set()
    for n, systems in systems_by_n.items():
        for s0 in systems:
            for img in dihedral_images(n, s0):
                s = set(img)
                if n == 4:
                    v, dsp = T(s, 0, 1, 2, 3, None, None), displayed(s, 0, 1, 2, 3)
                    (forms["T4"] if dsp else undisp).add(v)
                if n == 5:
                    v, dsp = T(s, 0, 2, 3, 4, 1, None), displayed(s, 0, 2, 3, 4)
                    (forms["T5"] if dsp else undisp).add(v)
                    forms["TP"].add(TP(s, 0, 1, 2, 3, 4))
                if n == 6:
                    v, dsp = T(s, 0, 3, 4, 5, 1, 2), displayed(s, 0, 3, 4, 5)
                    (forms["T6"] if dsp else undisp).add(v)
                    v, dsp = T(s, 0, 2, 3, 5, 1, 4), displayed(s, 0, 2, 3, 5)
                    (forms["TM"] if dsp else undisp).add(v)
    return forms, undisp

def ev(v, r):
    return sum(x * y for x, y in zip(v, r))

def cycle_with_clade_hybrid(m, hyb_size):
    """level-1 cycle with m non-hybrid leaves 0..m-1 along the cycle and a hybrid whose child is a caterpillar
    clade on hyb_size leaves (hyb_size = 1: a sunlet).  Circular order 0..m-1, then the clade."""
    n = m + hyb_size
    X = list(range(m, n))
    full = (1 << n) - 1
    sig = set(canon(n, 1 << p) for p in range(n))
    Xm = 0
    for x in X:
        Xm |= 1 << x
    for size in range(2, hyb_size):          # caterpillar clade clusters
        mm = 0
        for x in X[:size]:
            mm |= 1 << x
        sig.add(canon(n, mm))
    if hyb_size >= 2:
        sig.add(canon(n, Xm))
    # tree L: clade attached before leaf 0: clusters X+{0}, X+{0,1}, ...
    mm = Xm
    for p in range(m - 2):
        mm |= 1 << p
        sig.add(canon(n, mm))
    # tree R: clade attached after leaf m-1: clusters {0,1}, {0,1,2}, ..., {0..m-1}
    mm = 1
    for p in range(1, m):
        mm |= 1 << p
        if mm != full:
            sig.add(canon(n, mm))
    return n, sig

def min_alpha(n, sig, r):
    D = param_d(n, sig)
    al = param_alphas(n, D)
    worst = None
    for (i, j), v in al.items():
        val = ev(v[:4], r) + v[4]
        m = canon(n, split_mask(n, i, j))
        ok = (val > 0) if m in sig else (val == 0)
        if not ok and (worst is None or val < worst[0]):
            worst = (val, (i, j), m in sig)
    return worst

if __name__ == "__main__":
    for name, fam in (("A", {n: A_systems(n) for n in (4, 5, 6)}), ("C", {n: closure_systems(n) for n in (4, 5, 6)})):
        forms, undisp = local_forms(fam)
        print(f"class {name}: undisplayed-split forms: {sorted(undisp)}")
        for k in ("T4", "T5", "T6", "TM", "TP"):
            print(f"   {k}: {sorted(forms[k])}")
    print()
    tests = [("NANUQ", (F(0), F(1), F(1, 2), F(1))),
             ("c=0.3, a=0.5 (c <= a but 2a < c+s)", (F(3, 10), F(1), F(1, 2), F(1))),
             ("c=0.3, a=0.65 (2a = c+s)", (F(3, 10), F(1), F(13, 20), F(1))),
             ("c=0.2, a=0.8", (F(1, 5), F(1), F(4, 5), F(1))),
             ("a=0.4 < s/2", (F(0), F(1), F(2, 5), F(1))),
             ("o = 1.1 > s", (F(0), F(1), F(1, 2), F(11, 10))),
             ("o = 0.9 < s", (F(0), F(1), F(1, 2), F(9, 10))),
             ("a = s", (F(0), F(1), F(1), F(1)))]
    for label, r in tests:
        print(label, "rho =", tuple(str(x) for x in r))
        for hs in (1, 2):
            res = []
            for m in (4, 5, 6, 8, 10, 12):
                n, sig = cycle_with_clade_hybrid(m, hs)
                w = min_alpha(n, sig, r)
                res.append((m, None if w is None else (str(w[0]), w[2])))
            print(f"   cycle, hybrid clade size {hs}: first violations (m, (alpha, displayed?)):", res)
