"""Exact count of the assemblies that are linear images of the stacked configuration of two
states which share rigid segments (docs/geometry/HINGE_ENSEMBLES.md, Theorem M; the Science
division's Proposition R22-1 and its request R22-GEO-2).

Two states differ by rotations R_1, ..., R_s about the hinge bonds; segment j of the second
state is Q_j times that of the first, Q_0 = I, Q_j = R_1 ... R_j.  A competing state that is a
linear image of the stack moves segment j by  B_j = I + G (Q_j - I)  for one 3 x 3 matrix G
(the formulation of the Science division's referee), and it is a conformation iff every B_j
is orthogonal (segments with edge directions on no conic).  So the candidates are the points
of the affine scheme

        V_s = { G in A^9 :  (I + G (Q_j - I))^T (I + G (Q_j - I)) = I,   j = 1, ..., s }.

Claims checked here over Q with Singular, for rotations given by integer quaternions:
    s = 2 (generic):          dim V = 0, degree 8, reduced (the radical has degree 8), and no
                              other complex point: the eight chains of the cube are all;
    s = 2, two half-turns:    dim V = 0, degree 8 (the same eight; identifiability fails there
                              for another reason, an extra affine relation among them);
    s = 3 (generic):          dim V = 0, degree 2: only the two states.
The eight (resp. two) explicit real solutions are known, so "degree 8 (2) and reduced" proves
that there is nothing else, also over the complex numbers.

Usage: python3 exact_hinge_candidates.py      (needs Singular on the PATH; a few seconds)
"""
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F


def rot(q):
    a, b, c, d = (F(x) for x in q)
    n = a * a + b * b + c * c + d * d
    return [[(a * a + b * b - c * c - d * d) / n, 2 * (b * c - a * d) / n, 2 * (b * d + a * c) / n],
            [2 * (b * c + a * d) / n, (a * a - b * b + c * c - d * d) / n, 2 * (c * d - a * b) / n],
            [2 * (b * d - a * c) / n, 2 * (c * d + a * b) / n, (a * a - b * b - c * c + d * d) / n]]


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def singular_matrix(name, A):
    ent = ",".join(f"{x.numerator}/{x.denominator}" for row in A for x in row)
    return f"matrix {name}[3][3] = {ent};\n"


def run(quats, label, want_deg, want_reduced=True):
    Q = [[F(int(i == j)) for j in range(3)] for i in range(3)]
    Qs = []
    for q in quats:
        Q = mul(Q, rot(q))
        Qs.append(Q)
    src = "LIB \"primdec.lib\";\nring r = 0,(g(1..9)),dp;\noption(redSB);\n"
    src += "matrix G[3][3] = g(1),g(2),g(3),g(4),g(5),g(6),g(7),g(8),g(9);\n"
    src += "matrix E[3][3] = 1,0,0,0,1,0,0,0,1;\nideal I = 0;\nmatrix B[3][3];\nmatrix C[3][3];\n"
    for j, Qj in enumerate(Qs):
        src += singular_matrix(f"Q{j}", Qj)
        src += f"B = E + G*(Q{j} - E);\nC = transpose(B)*B - E;\nI = I + ideal(C);\n"
    src += ("ideal J = std(I);\nprint(\"DIM=\" + string(dim(J)));\nprint(\"DEG=\" + string(vdim(J)));\n"
            "ideal R = std(radical(J));\nprint(\"RADDEG=\" + string(vdim(R)));\nquit;\n")
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as f:
        f.write(src)
        path = f.name
    out = subprocess.run(["Singular", "-q", path], capture_output=True, text=True, timeout=3600).stdout
    vals = dict(line.split("=", 1) for line in out.splitlines() if "=" in line)
    ok = vals.get("DIM") == "0" and vals.get("DEG") == str(want_deg)
    if want_reduced:
        ok = ok and vals.get("RADDEG") == str(want_deg)
    print(f"{label}: dim = {vals.get('DIM')}, degree = {vals.get('DEG')}, degree of the radical = "
          f"{vals.get('RADDEG')}  (expected degree {want_deg}{', reduced' if want_reduced else ''})  "
          f"{'OK' if ok else 'FAIL'}", flush=True)
    return ok


def main():
    if shutil.which("Singular") is None:
        print("Singular not found on the PATH; this exact computation is skipped")
        return 2
    mutate = "--mutate" in sys.argv          # planted error: claim a single candidate pair
    ok = True
    ok &= run([(3, 1, 2, -1), (2, -1, 1, 3)], "two hinges, generic rotations      ", 2 if mutate else 8)
    ok &= run([(1, 2, 0, 1), (4, 1, -2, 2)], "two hinges, second instance        ", 8)
    ok &= run([(0, 1, 2, -1), (0, -1, 1, 3)], "two hinges, both half-turns        ", 8, want_reduced=False)
    ok &= run([(3, 1, 2, -1), (2, -1, 1, 3), (1, 2, -2, 1)], "three hinges, generic rotations    ", 2)
    ok &= run([(1, 2, 0, 1), (4, 1, -2, 2), (2, 3, 1, -1)], "three hinges, second instance      ", 2)
    print("ALL OK" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
