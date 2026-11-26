"""Parameter domain on class A (hybrid nodes with a leaf child; contains all bloblets):
        D_A = { o = s,  0 <= c <= a,  s <= 2a,  a < s }.
Sufficiency: local forms of A_{<=6} on the extreme rays of cl(D_A).
Necessity: witnesses inside A (sunlets with a leaf hybrid, some non-hybrid leaves replaced by clades)."""
from fractions import Fraction as F
from itertools import product
from splitsys import *
from localcrit import dihedral_images, blowup
from twin_trees import A_systems
from parametric import param_d, param_alphas
from parametric_domain import local_forms, ev, cycle_with_clade_hybrid, min_alpha
from parametric_theorem import TQ

if __name__ == "__main__":
    forms, undisp = local_forms({n: A_systems(n) for n in (4, 5, 6)})
    tq = set()
    for n in (4, 5):
        for s0 in A_systems(n):
            for img in dihedral_images(n, s0):
                tq.add(TQ(set(img), 0, 1, 2, 3))
    forms["TQ"] = tq
    rays = [(0, 2, 1, 2), (0, 1, 1, 1), (1, 1, 1, 1), (1, 2, 1, 2)]
    print("local forms of A_{<=6} are >= 0 on the extreme rays of cl(D_A):",
          all(ev(v, r) >= 0 for k in forms for v in forms[k] for r in rays),
          "| undisplayed forms:", sorted(undisp))
    # witnesses: sunlet with m non-hybrid leaves (hybrid = leaf m), non-hybrid leaves blown up
    tests = [("o > s", (F(0), F(1), F(1, 2), F(11, 10))), ("o < s", (F(0), F(1), F(1, 2), F(9, 10))),
             ("c > a", (F(7, 10), F(1), F(3, 5), F(1))), ("2a < s", (F(0), F(1), F(2, 5), F(1))),
             ("Modified NANUQ (in D_A)", (F(1, 2), F(1), F(1, 2), F(1))), ("NANUQ", (F(0), F(1), F(1, 2), F(1)))]
    for label, r in tests:
        found = None
        for m in (4, 5, 6):
            n0, sig0 = cycle_with_clade_hybrid(m, 1)          # leaves 0..m-1 on the cycle, leaf m hybrid
            for mult in product((1, 3, 6), repeat=m):
                if sum(mult) > 16:
                    continue
                n, sig = blowup(n0, sig0, list(mult) + [1])
                w = min_alpha(n, sig, r)
                if w is not None:
                    if found is None or n < found[0]:
                        found = (n, m, mult, str(w[0]), w[2])
            if found:
                break
        print(f"{label}: rho = {tuple(str(x) for x in r)} ->",
              "no violation found" if found is None else
              f"violation: sunlet with {found[1]} cycle positions, clade sizes {found[2]}, hybrid leaf; n = {found[0]}; "
              f"alpha = {found[3]} on a {'displayed' if found[4] else 'undisplayed'} split")
