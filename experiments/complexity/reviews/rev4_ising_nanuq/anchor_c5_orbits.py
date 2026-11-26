"""The representatives of the 7-face orbits of c_5 as written in LIENS-95-1 (Section 3.2.1), evaluated."""
import itertools, numpy as np, sympy
from ising_core import all_states, Pmat
S = all_states(5)                       # states; cut coordinate x_ij = 1 if s_i != s_j
n = 5
def cutvec(s): return {(i, j): int(s[i] != s[j]) for i in range(n) for j in range(i + 1, n)}
X = [cutvec(s) for s in S]
g = lambda x, i, j: x[(min(i, j), max(i, j))]
def Tr3(i, j, k):   # x_ij + x_ik + x_jk <= 2
    return frozenset(t for t, x in enumerate(X) if g(x, i, j) + g(x, i, k) + g(x, j, k) == 2)
def Tr(i, j, k):    # x_ij - x_ik - x_jk <= 0     (Tr_{ij,k})
    return frozenset(t for t, x in enumerate(X) if g(x, i, j) - g(x, i, k) - g(x, j, k) == 0)
eq = frozenset(t for t, x in enumerate(X) if sum(x.values()) == 6)
def dim(f):
    R = Pmat(S[sorted(f)])
    return sympy.Matrix((R[1:] - R[0:1]).tolist()).rank()
# group: switchings and permutations acting on states
def orbit_size(f):
    seen = set()
    states = [tuple(int(v) for v in s) for s in S]
    idx = {s: t for t, s in enumerate(states)}
    for perm in itertools.permutations(range(n)):
        for sw in itertools.product([1, -1], repeat=n):
            img = []
            for t in f:
                s = states[t]
                u = tuple(s[perm[i]] * sw[i] for i in range(n))
                if u[0] == -1: u = tuple(-v for v in u)
                img.append(idx[u])
            seen.add(frozenset(img))
    return len(seen)
T = lambda *a: Tr3(*[i - 1 for i in a])
Tm = lambda i, j, k: Tr(i - 1, j - 1, k - 1)
f81 = T(1, 2, 3) & T(1, 2, 4)
f82 = T(1, 2, 3) & T(1, 4, 5)
f83 = T(1, 2, 3) & eq
reps = {
 "f8^1 = Tr123 ^ Tr124": f81, "f8^2 = Tr123 ^ Tr145": f82, "f8^3 = Tr123 ^ f9^2": f83,
 "f7^1 = f8^1 ^ Tr24,3 ^ Tr13,4": f81 & Tm(2, 4, 3) & Tm(1, 3, 4),
 "f7^2 = f8^2 ^ Tr23,4": f82 & Tm(2, 3, 4),
 "f7^3 = f8^3 ^ Tr125": f83 & T(1, 2, 5),
 "f7^4 = f8^2 ^ f9^2": f82 & eq,
 "f7^5 = f8^1 ^ Tr134": f81 & T(1, 3, 4),
 "f7^6 = f8^1 ^ Tr125": f81 & T(1, 2, 5),
 "f7^7 = f8^1 ^ Tr135": f81 & T(1, 3, 5),
}
tot = 0
for name, f in reps.items():
    d, o = dim(f), orbit_size(f)
    print("%-32s vertices %2d  dim %d  orbit size %d" % (name, len(f), d, o))
