"""The 108 systems of the substitution closure on six points, up to rotation and reflection: 17 classes.
For a representative of each class: its non-trivial splits, the size of the class, whether it lies in class A,
and the values of 2*Phi6(y1; y2,y3; y4; y5,y6) in the twelve dihedral placements, split according to whether
the quartet y1y4|y5y6 is displayed.  The six-point condition is: no negative value, and only zeros in the
"not displayed" column.  (Printed as a markdown table for Appendix B of NANUQ_LOCAL_CRITERION.md.)"""
from collections import Counter
from splitsys import *
from localcrit import dihedral_images
from local_terms import phi6, displayed
from twin_trees import closure_systems, A_systems


def name(n, m):
    return "".join(str(p + 1) for p in range(n) if (m >> p) & 1)


if __name__ == "__main__":
    n = 6
    C = set(closure_systems(n))
    A = set(A_systems(n))
    seen = set()
    classes = []
    for s in sorted(C, key=lambda s: (len(s), sorted(s))):
        if s in seen:
            continue
        orb = dihedral_images(n, s)
        assert orb <= C
        seen |= orb
        classes.append((s, orb))
    print(f"{len(C)} systems, {len(classes)} classes; in class A: {sum(len(o) for s, o in classes if s in A)} systems, "
          f"{sum(1 for s, o in classes if s in A)} classes")
    print("| # | non-trivial splits (side not containing leaf 1) | class size | in 𝒜 | 2Φ6, split displayed | 2Φ6, split not displayed |")
    print("|---|---|---|---|---|---|")
    for k, (s, orb) in enumerate(classes, 1):
        nt = sorted((m for m in s if not is_trivial(n, m)), key=lambda m: (bin(m).count("1"), m))
        disp, undisp = Counter(), Counter()
        # twelve placements = the images of s under the dihedral group, each evaluated at the fixed labelling
        for r in range(n):
            for refl in (False, True):
                y = [(r - t) % n if refl else (r + t) % n for t in range(n)]
                v = phi6(set(s), n, *y)
                (disp if displayed(set(s), y[0], y[3], y[4], y[5]) else undisp)[v] += 1
        f = lambda c: ", ".join(f"{v} (×{c[v]})" for v in sorted(c)) if c else "—"
        ok = all(v >= 0 for v in disp) and all(v == 0 for v in undisp)
        assert ok
        print(f"| {k} | {' '.join(name(n, m) for m in nt)} | {len(orb)} | {'yes' if s in A else 'no'} | {f(disp)} | {f(undisp)} |")
