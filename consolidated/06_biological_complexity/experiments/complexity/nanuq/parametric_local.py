"""Local terms of the split weights for the parametric family rho = (c, s, a, o), as linear forms, over all
systems of the class C on 4, 5, 6 leaves and all placements.

  alpha/2 = T4 + sum_z T5(z) + sum_{z,w same side} T6(z,w) + sum_{z in U, w in V} TM(z,w)      (non-trivial split)
  alpha/2 = n - 2 + sum_{z,w} TP(z,w)                                                          (trivial split)

Each term is a sum of values rho_xy(q) in {c, s, a, o} with signs; forms are vectors (c, s, a, o)."""
from itertools import combinations
from splitsys import *
from localcrit import dihedral_images
from twin_trees import closure_systems

def val(sigma, x, y, z, w):
    """vector (c,s,a,o) of rho_xy on the 4-set {x,y,z,w}"""
    pts = sorted([x, y, z, w])
    ix, iy = pts.index(x), pts.index(y)
    adjacent = (ix - iy) % 4 in (1, 3)
    a_, b_, c_, d_ = pts
    P = any(separates(m, (1 << a_) | (1 << b_), (1 << c_) | (1 << d_)) for m in sigma)   # ab|cd
    Q = any(separates(m, (1 << a_) | (1 << d_), (1 << b_) | (1 << c_)) for m in sigma)   # ad|bc
    assert P or Q
    if P and Q:
        return (0, 0, 1, 0) if adjacent else (0, 0, 0, 1)
    if not adjacent:
        return (0, 1, 0, 0)
    # adjacent pair: cherry iff the displayed quartet has {x,y} as a block
    cher = ({a_, b_}, {c_, d_}) if P else ({a_, d_}, {b_, c_})
    return (1, 0, 0, 0) if {x, y} in cher else (0, 1, 0, 0)

def comb(*terms):
    out = [0, 0, 0, 0]
    for sign, v in terms:
        for k in range(4):
            out[k] += sign * v[k]
    return tuple(out)

def T(sigma, u1, up, v1, vq, z, w):
    """the generic local term for the pair {z,w} of extra points (or z only if w is None, or none)"""
    def r(x, y, others):
        return val(sigma, x, y, *others)
    if z is None:
        Y = [u1, up, v1, vq]
        return comb((1, r(vq, up, [u1, v1])), (1, r(u1, v1, [up, vq])), (-1, r(vq, v1, [u1, up])), (-1, r(u1, up, [v1, vq])))
    if w is None:
        terms = []
        # 4-sets Y minus one point, plus z
        for (x, y, sign) in ((vq, up, 1), (u1, v1, 1), (vq, v1, -1), (u1, up, -1)):
            for third in (u1, up, v1, vq):
                if third in (x, y):
                    continue
                terms.append((sign, r(x, y, [third, z])))
        return comb(*terms)
    return comb((1, r(vq, up, [z, w])), (1, r(u1, v1, [z, w])), (-1, r(vq, v1, [z, w])), (-1, r(u1, up, [z, w])))

def TP(sigma, a, u, b, z, w):
    return comb((1, val(sigma, a, u, z, w)), (1, val(sigma, u, b, z, w)), (-1, val(sigma, a, b, z, w)))

def displayed(sigma, u1, up, v1, vq):
    return any(separates(m, (1 << u1) | (1 << up), (1 << v1) | (1 << vq)) for m in sigma)

if __name__ == "__main__":
    forms = {"T4": {}, "T5": {}, "T6": {}, "TM": {}, "TP": {}}
    def rec(kind, disp, v):
        forms[kind].setdefault(disp, set()).add(v)
    for n in (4, 5, 6):
        for s0 in closure_systems(n):
            for img in dihedral_images(n, s0):
                s = set(img)
                if n == 4:
                    rec("T4", displayed(s, 0, 1, 2, 3), T(s, 0, 1, 2, 3, None, None))
                if n == 5:
                    # u1=0, z=1, up=2, v1=3, vq=4
                    rec("T5", displayed(s, 0, 2, 3, 4), T(s, 0, 2, 3, 4, 1, None))
                    rec("TP", True, TP(s, 0, 1, 2, 3, 4))
                if n == 6:
                    # same side: u1=0, z=1, w=2, up=3, v1=4, vq=5
                    rec("T6", displayed(s, 0, 3, 4, 5), T(s, 0, 3, 4, 5, 1, 2))
                    # mixed: u1=0, z=1, up=2, v1=3, w=4, vq=5
                    rec("TM", displayed(s, 0, 2, 3, 5), T(s, 0, 2, 3, 5, 1, 4))
    for kind in ("T4", "T5", "T6", "TM", "TP"):
        for disp in sorted(forms[kind], reverse=True):
            print(f"{kind} (split quartet displayed: {disp}): forms (c,s,a,o) =", sorted(forms[kind][disp]))
