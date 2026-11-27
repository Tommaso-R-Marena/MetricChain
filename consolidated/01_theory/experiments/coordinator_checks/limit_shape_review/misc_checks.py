#!/usr/bin/env python3
"""Assistant B — arithmetic and sanity checks for N4, N5, m4, m5, m6, Bezdek (A2.3) and A2.2's constant.
Own code (mylat.py); the harness is imported as a library only for ls_lamella (our lamella builder)."""
import sys, os, json, math, itertools, importlib.util
from fractions import Fraction as Fr
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
import mylat as ML

print("=== N4: d_H(D_N^br, K^br) >= 17.6 N^(-1/3) - 17/N  (Proposition 11.73 and (1,5,6;0) in K^br)")
f = lambda N, a=17.6, b=17.0: a * N ** (-1.0 / 3) - b / N
for thr in (0.5, 0.25):
    # largest N with f >= thr, and check that f >= thr on the whole range 3..N
    N = 3
    while f(N + 1) >= thr or N < 100:
        N += 1
    lo = min(f(n) for n in range(3, N + 1))
    print(f"  threshold {thr}: f(N) >= {thr} for every 3 <= N <= {N} (min over the range {lo:.6f}); f({N}) = {f(N):.7f}, f({N+1}) = {f(N+1):.7f}")
cex = 9 * 2 ** (-2.0 / 3) + 12
print(f"  the constant: 9*2^(-2/3) + 12 = {cex:.5f} (17.6 is rounded down); constant term 9 + 8 = 17")

print("=== Bezdek / Proposition A2.3: arithmetic")
cb = 3 * (18 * math.pi) ** (1.0 / 3) / math.pi
print(f"  3 (18 pi)^(1/3) / pi = {cb:.6f}   (claimed 3.665...)")
cw = cb * 2 ** (1.0 / 3)
print(f"  walks: 2 * {cb:.4f} * ((N-1)/2)^(2/3) = {cw:.6f} (N-1)^(2/3)   (claimed 4.617);  (2/3)*{cw:.4f} = {2*cw/3:.4f} <= 3.1")
tot = 9 * 2 ** (-2.0 / 3) + 4 * cw
tot_r = 9 * 2 ** (-2.0 / 3) + 4 * 4.617
print(f"  surface law for walks: coefficient of N^(2/3): 9*2^(-2/3) + 4*{cw:.4f} = {tot:.5f} (with the rounded 4.617: {tot_r:.5f}; claimed 24.1);")
print(f"     constant term: 9 + 4*(3.1 + 2) = {9 + 4*5.1:.1f};   k = coefficient/35 = {tot/35:.5f} (rounded 4.617: {tot_r/35:.5f}; claimed 'k >= 0.69'; first version {cex/35:.4f})")
g = lambda N: 24.1 * N ** (-1.0 / 3) - 29.4 / N
for thr in (0.5, 0.25):
    N = 100
    while g(N + 1) >= thr:
        N += 1
    print(f"  N4 with Bezdek's constant (walks: 24.1 N^(-1/3) - 29.4/N >= {thr}): for every 4 <= N <= {N}  (min over the range {min(g(n) for n in range(4, N+1)):.5f})")

print("=== sanity of e8 < 6N - 3.665 N^(2/3) (all finite site sets, N >= 2) and e8 < 6N - 4.617 N^(2/3) + 3.1 (walks)")
D8 = ML._disp()[8]
def e8_of(S):
    S = set(S)
    return sum(1 for p in S for v in D8 if (p[0] + v[0], p[1] + v[1], p[2] + v[2]) in S) // 2
worst = (1e9, None)
for R2 in range(3, 260, 4):
    r = int(math.isqrt(R2)) + 2
    S = [p for p in itertools.product(range(-r, r + 1), repeat=3) if ML.is_site(p) and p[0] ** 2 + p[1] ** 2 + p[2] ** 2 <= R2]
    N = len(S)
    if N < 2:
        continue
    e8 = e8_of(S)
    assert e8 < 6 * N - cb * N ** (2.0 / 3)
    q = (6 * N - e8) / N ** (2.0 / 3)
    if q < worst[0]:
        worst = (q, (R2, N, e8))
    # one sublattice only (an fcc ball): contact number against Bezdek directly
    SA = [p for p in S if p[0] % 2 == 0]
    nA = len(SA)
    if nA >= 2:
        cA = e8_of(SA)
        assert cA < 6 * nA - cb * nA ** (2.0 / 3)
        qa = (6 * nA - cA) / nA ** (2.0 / 3)
        if qa < worst[0]:
            worst = (qa, ("fcc ball", R2, nA, cA))
print(f"  diamond balls and fcc balls up to squared radius 259: no violation; smallest (6N - e8)/N^(2/3) = {worst[0]:.4f} at {worst[1]}  (must exceed {cb:.4f})")
mw = -1e9
cnt = 0
viol5 = 0
n5max = [-10 ** 9] * 5
for N in range(4, 15):
    for b in ML.enum_bridges(N):
        cnt += 1
        h3, h8, h11, g = ML.profile_hash(b)
        e8 = h8 + N - 2
        assert e8 == e8_of(b)
        assert e8 < 6 * N - cw * N ** (2.0 / 3) + 3.1
        mw = max(mw, e8 - (6 * N - cw * N ** (2.0 / 3) + 3.1))
        # N5 (reviewer's finite-N constants)
        v = [-3 * h3 + 2 * h8 - h11 - 2 * N - 53, -3 * h3 + 4 * h8 - 3 * h11 - 2 * N - 65,
             (2 * h11 - 5 * h3 - 8 * N - 143) - g, (2 * h11 - h8 - 7 * N - 70) - g, (h11 + h8 - 4 * h3 - 7 * N - 128) - g]
        for i in range(5):
            n5max[i] = max(n5max[i], v[i])
        viol5 += any(x > 0 for x in v)
        # m4: the three by-hand inequalities
        assert h8 >= 4 * h3 - 2 and h8 >= 6 * h3 - N - 4 and h8 <= 2 * h3 + 3 * N + 3
print(f"  all {cnt} bridges with 4..14 beads: e8 < 6N - 4.617N^(2/3) + 3.1 holds (largest lhs - rhs = {mw:.3f}); Prop 11.72(a) holds")
print(f"=== N5 (reviewer's finite-N rows): on the same bridges: violations {viol5}; largest (lhs - rhs) of the five rows: {n5max}")
ver = json.load(open(os.path.join(HERE, "wit", "verified.json")))
sys.argv = ["x"]
spec = importlib.util.spec_from_file_location("fc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "falsify_conjectures.py"))
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)
big = [(name, r["N"], tuple(r["hg"])) for name, r in ver.items()]
for (M, Q, l) in ((9, 1, 16), (33, 1, 64), (5, 5, 6), (9, 9, 10), (17, 17, 18)):
    w = fc.ls_lamella(M, Q, l)
    assert ML.check_walk(w) is None and ML.is_bridge(w)
    big.append((f"lamella {M}x{Q}x{l}", len(w), ML.profile_hash(w)))
for N in (50, 1000):
    big.append((f"helix {N}", N, (0, 0, N - 3, N - 3)))
    big.append((f"rod {N}", N, (0, 0, 0, 0)))
n5max = [-10 ** 9] * 5
for name, N, (h3, h8, h11, g) in big:
    v = [-3 * h3 + 2 * h8 - h11 - 2 * N - 53, -3 * h3 + 4 * h8 - 3 * h11 - 2 * N - 65,
         (2 * h11 - 5 * h3 - 8 * N - 143) - g, (2 * h11 - h8 - 7 * N - 70) - g, (h11 + h8 - 4 * h3 - 7 * N - 128) - g]
    assert all(x <= 0 for x in v), (name, v)
    for i in range(5):
        n5max[i] = max(n5max[i], v[i])
    e8 = h8 + N - 2
    assert e8 < 6 * N - cw * N ** (2.0 / 3) + 3.1 and 9 * h3 + 4 * h8 + h11 <= 35 * N - 24.1 * N ** (2.0 / 3) + 29.4
print(f"  on {len(big)} long walks (the ten verified bridges, five lamellae of our builder, helices, rods): no violation; largest lhs - rhs: {n5max}")
print("  (these tests have little power: the constants are loose at these sizes.  The certificates of N5 were NOT re-derived.)")

print("=== m5 / N5: volume ratios vol(U X + rho B1)/vol(rho B1), rho = eps1/(2L), own computation (Qhull, float)")
U = np.array([[5, 0, 0], [3, 3, 0], [1, 1, 1]], float)
def ratio(Vp, rho):
    Vu = Vp @ U.T
    pts = np.vstack([Vu + rho * s * np.eye(3)[k] for k in range(3) for s in (1, -1)])
    return ConvexHull(pts).volume / (4.0 / 3 * rho ** 3)
box = np.array(list(itertools.product((0, 1), (0, 5), (0, 6))), float)
K2 = np.array([(0, 0, 0), (0, 0, 2), (0, 1, 4), (0, 2, 2), (0, 2, 4.5), (0, 3, 4), (0, 3, 4.5), (.5, 2, 1.5), (.5, 2, 3), (.5, 3.5, 3.5), (.5, 4, 4.5), (1, 5, 6)], float)
print(f"  vol K2 = {ConvexHull(K2).volume:.6f} (25/8 = 3.125);  number of hull vertices {len(ConvexHull(K2).vertices)}")
cases = [("(1,1/2)", 0.25), ("(1,1/4)", 0.125), ("(1/5,1/2)", 1.25), ("(1/5,1/4)", 0.625)]
print("  bulk box:", "  ".join(f"{n}: {ratio(box, r):.2f}" for n, r in cases))
print("  K2      :", "  ".join(f"{n}: {ratio(K2, r):.2f}" for n, r in cases))
rows = [((-1, 0, 0), 0, 1), ((4, -1, 0), 0, 22), ((6, -1, 0), 1, 28), ((-2, 1, 0), 3, 8), ((-1, 1, -1), 0, 13), ((-1, 2, -1), 3, 19),
        ((-4, 2, -1), 2, 24), ((3, 4, -3), 5, 35), ((6, -2, 1), 2, 26), ((0, -1, 2), 7, 2), ((-3, 0, 2), 9, 9),
        ((-3, 2, -1), 2, 53), ((-3, 4, -3), 2, 65)]
# the eleven constants K = 4M + c3 + 2c8 of Proposition 11.72(b) (ours)
ours = {(-1, 0, 0): Fr(1, 2), (4, -1, 0): 5, (6, -1, 0): 6, (-2, 1, 0): 2, (-1, 1, -1): 3, (-1, 2, -1): 4, (-4, 2, -1): 6, (3, 4, -3): 6,
        (6, -2, 1): 6, (0, -1, 2): 1, (-3, 0, 2): 3}
for c, b, K in rows[:11]:
    assert 4 * ours[c] + c[0] + 2 * c[1] == K, (c, K)
print("  the eleven finite constants K = 4M + c3 + 2c8 of Proposition 11.72(b) agree with the reviewer's list; the two marked rows use the reviewer's 53, 65")
cen = K2.mean(0)
for N in (100, 1000, 10000, 100000, 10 ** 7):
    hs = np.array([list(c) + [-(b + K / N)] for c, b, K in rows], float)
    V = HalfspaceIntersection(hs, cen).intersections
    print(f"  K2^(N), N >= {N:>8d}:", "  ".join(f"{n}: {ratio(V, r):.1f}" for n, r in cases))
print("  reviewer: N=100: 4650.3 30352.1 110.9 486.7; 1000: 3728.7 23978.1 94.3 402.2; 10^4: 3636.7 23342.7 92.7 393.7; 10^5: 3627.5 23279.1 92.5 392.9; limit 3626.5 23272.0 92.5 392.8")

print("=== m6 and the interior of K^br in R^4")
# the four exact points lie on the hyperplane g = 9 p3 - 3 p8 + p11; a verified bridge far off it
for q in ((0, 0, 0, 0), (Fr(1, 2), 2, Fr(3, 2), 0), (1, 5, 6, 0), (0, 0, 1, 1)):
    assert q[3] == 9 * q[0] - 3 * q[1] + q[2]
name = "_0_3_4__W3_W64"
N = ver[name]["N"]; h = ver[name]["hg"]
fval = Fr(h[3], N) - 9 * Fr(h[0], N) + 3 * Fr(h[1], N) - Fr(h[2], N)
delta = Fr(168, N + 3)
# |f(dq)| <= |dg| + |12 s1 - 4 s2 + s3| <= |dg| + (12/5)(5|s1|) + (4/3)(3|s2|) + |s3| <= (12/5)(||dp||_c + |dg|)
print(f"  f(p,g) = g - 9p3 + 3p8 - p11 vanishes at the four exact points; at the verified W3 bridge f = {float(fval):.4f}, "
      f"uncertainty <= (12/5)*168/(N+3) = {float(Fr(12,5)*delta):.4f}  => a fifth, affinely independent point: K^br has interior in R^4")
print("  volume of the hull of the four exact profile points = 1/12 (inner_volume.py): the profile body has interior in R^3")

print("=== A2.2: the constant for bridges")
beta, betap, R, d = 60, 28, 36, 4
print(f"  c = 2 sqrt(beta (d+1)(beta'+R)) = {2*math.sqrt(beta*(d+1)*(betap+R)):.2f}  (claimed 277);  (d+1)(beta'+R) = {(d+1)*(betap+R)}")
for M in (10 ** 4, 10 ** 6, 10 ** 8):
    m = math.ceil(math.sqrt(beta * M / ((d + 1) * (betap + R))))
    print(f"  M = {M:.0e}: m = {m}: beta/m + (d+1)(beta'+R) m/M = {beta/m + (d+1)*(betap+R)*m/M:.5f};  c/sqrt(M) = {2*math.sqrt(beta*(d+1)*(betap+R)/M):.5f}")

print("=== m4: the three elementary inequalities on C(d,2), 0 <= d <= 4")
for dd in range(5):
    c2 = dd * (dd - 1) // 2
    print(f"  d = {dd}: C(d,2) = {c2};  2d-3 = {2*dd-3} (<= C: {2*dd-3 <= c2});  3d-6 = {3*dd-6} (<= C: {3*dd-6 <= c2});  "
          f"3d/2 = {1.5*dd} (>= C: {1.5*dd >= c2});  (5d-8)/2 = {(5*dd-8)/2} (>= C: {(5*dd-8)/2 >= c2})")
