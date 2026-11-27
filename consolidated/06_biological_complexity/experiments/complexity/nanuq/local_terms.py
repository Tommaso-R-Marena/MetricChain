"""Local (4-, 5-, 6-point) terms of the split weights alpha_ij of the NANUQ metric.

For a non-trivial circular split U|V with U = (u_1,...,u_p), V = (v_1,...,v_q) (circular order
u_1..u_p v_1..v_q, p,q >= 2) and Y = {u_1,u_p,v_1,v_q}:

  alpha/2 = Phi4 + sum_{z in X\\Y} Phi5(z) + sum_{ {z,w} in X\\Y, same side } Phi6(z,w)

  Phi4        = 2 w(u_1 u_p | v_1 v_q)
  Phi5(z)     = w(u_1 z | v_1 v_q) + w(z u_p | v_1 v_q) - w(z u_p | v_1 u_1) - w(u_1 z | u_p v_q)     (z in U)
  Phi6(z,w)   = w(z w | v_1 v_q) + w(z w | u_1 u_p) - w(z w | v_q u_p) - w(z w | u_1 v_1)             (z,w in U)

where w(ab|cd) in {0,1/2,1} is the weight of the quartet ab|cd among the displayed quartets of {a,b,c,d}
(and symmetrically for z, w in V).  Pairs {z,w} on different sides contribute 0.
Here we evaluate 2*Phi (integers) on all systems of the network class on 4, 5, 6 points.
"""
import sys
from itertools import combinations
from splitsys import *
from multiblob import network_systems

def weight2(sigma, n, a, b, c, d):
    """2 * weight of quartet ab|cd in the system sigma (set of canonical masks) : 0, 1 or 2."""
    ab, cd = (1 << a) | (1 << b), (1 << c) | (1 << d)
    P = any(separates(m, ab, cd) for m in sigma)
    # the other planar quartet on {a,b,c,d}: determine circular order
    pts = sorted([a, b, c, d])
    # ab|cd is planar iff a,b adjacent in the circular order of the 4 points
    ia, ib = pts.index(a), pts.index(b)
    assert (ia - ib) % 4 in (1, 3), "non-planar quartet requested"
    # other planar quartet: pair each of a,b with its other neighbour
    na = pts[(ia + 1) % 4] if pts[(ia + 1) % 4] != b else pts[(ia - 1) % 4]
    nb = [x for x in pts if x not in (a, b, na)][0]
    Q = any(separates(m, (1 << a) | (1 << na), (1 << b) | (1 << nb)) for m in sigma)
    assert P or Q
    if P and Q:
        return 1
    return 2 if P else 0

def phi4(sigma, n, u1, up, v1, vq):
    return 2 * weight2(sigma, n, u1, up, v1, vq)

def phi5(sigma, n, u1, z, up, v1, vq):
    return (weight2(sigma, n, u1, z, v1, vq) + weight2(sigma, n, z, up, v1, vq)
            - weight2(sigma, n, z, up, v1, u1) - weight2(sigma, n, u1, z, up, vq))

def phi6(sigma, n, u1, z, w, up, v1, vq):
    return (weight2(sigma, n, z, w, v1, vq) + weight2(sigma, n, z, w, u1, up)
            - weight2(sigma, n, z, w, vq, up) - weight2(sigma, n, z, w, u1, v1))

def displayed(sigma, a, b, c, d):
    return any(separates(m, (1 << a) | (1 << b), (1 << c) | (1 << d)) for m in sigma)

if __name__ == "__main__":
    # 6-point systems
    for n, fn, labels in ((5, phi5, "Phi5"), (6, phi6, "Phi6")):
        systems = network_systems(n, n)
        vals = {}
        zero_viol = 0
        for s in systems:
            if n == 5:
                # u1=0,z=1,up=2,v1=3,vq=4
                v = phi5(s, n, 0, 1, 2, 3, 4)
                disp = displayed(s, 0, 2, 3, 4)
            else:
                v = phi6(s, n, 0, 1, 2, 3, 4, 5)
                disp = displayed(s, 0, 3, 4, 5)
            vals.setdefault((disp, v), 0)
            vals[(disp, v)] += 1
            if not disp and v != 0:
                zero_viol += 1
        print(n, labels, "(split quartet displayed?, 2*Phi) -> count:", dict(sorted(vals.items())), "violations of 'not displayed => 0':", zero_viol)
