# b3_fixed_angle.py -- REVIEW 6, referee's own check of the Lemma of section 3 of CHAIN_GEOMETRY_HARDNESS.md
# ("free every m-th bond": for unit p, q there are unit w_0 = p, ..., w_m = q with <w_i,w_{i+1}> = cos(theta),
#  m = ceil(pi / min(theta, pi - theta))).
# Own construction, deliberately SIMPLER than the note's: for theta <= pi/2 always step by theta towards q while more
# than two steps remain (no parity rule), then close with an isosceles elbow; for theta > pi/2 the sign trick.
# Tested on random and degenerate inputs (p = q, p = -q, distance exactly 2 psi, theta = pi/2, tiny and huge theta).
# Also: (a) m is best possible: with m - 1 steps some targets are unreachable (checked through the reachable set,
# which for psi <= pi/2 is the cap of radius (m-1) psi around p or -p);
# (b) Theorem 3 end to end on a graph not used by the authors: the Heisenberg instance of Theorem 1 for the paw graph
# is embedded into a fixed-angle chain (theta = 70.53 deg, m = 3); the chain objective sum c_ij |x_i - x_j|^2 with the
# integer data c of section 1 equals 2 F(b) on random spin configurations and equals twice the Theorem-1 optimum on
# the optimal configuration.
import math, itertools, random
import numpy as np

rng = np.random.default_rng(31)


def unit(v):
    return v / np.linalg.norm(v)


def perp(p):
    a = np.array([1.0, 0, 0]) if abs(p[0]) < 0.9 else np.array([0, 1.0, 0])
    return unit(np.cross(p, a))


def sdist(a, b):
    return math.atan2(np.linalg.norm(np.cross(a, b)), float(a @ b))


def toward(c, q, ang):
    d = sdist(c, q)
    if d < 1e-13 or math.pi - d < 1e-13:
        e = perp(c)
    else:
        e = unit(q - (c @ q) * c)
    return math.cos(ang) * c + math.sin(ang) * e


def chain_small(p, q, psi, m):
    assert psi <= math.pi / 2 + 1e-15 and m * psi >= math.pi - 1e-12 and m >= 2
    w, c = [p], p
    for r in range(m, 2, -1):
        assert sdist(c, q) <= r * psi + 1e-9
        c = unit(toward(c, q, psi))
        w.append(c)
    d = sdist(c, q)
    assert d <= 2 * psi + 1e-9, (d, psi)
    if d < 1e-13:
        elbow = toward(c, perp(c), psi)
    elif math.pi - d < 1e-9:
        elbow = perp(c)
    else:
        mid = unit(c + q)
        nrm = unit(np.cross(c, q))
        cphi = min(1.0, max(-1.0, math.cos(psi) / math.cos(d / 2)))
        phi = math.acos(cphi)
        elbow = math.cos(phi) * mid + math.sin(phi) * nrm
    return w + [unit(elbow), q]


def chain(p, q, theta):
    psi = min(theta, math.pi - theta)
    m = max(2, math.ceil(math.pi / psi - 1e-9))
    if theta <= math.pi / 2:
        return chain_small(p, q, theta, m), m
    w = chain_small(p, q if m % 2 == 0 else -q, psi, m)
    return [x if i % 2 == 0 else -x for i, x in enumerate(w)], m


worst = 0.0
cases = 0
thetas = [math.radians(a) for a in (70.528779, 109.471221, 90.0, 60.0, 120.0, 45.0, 135.0, 1.0, 179.0, 89.999, 90.001, 36.0, 180.0 / 7, 100.0)]
thetas += list(rng.uniform(0.02, math.pi - 0.02, size=200))
for th in thetas:
    for trial in range(30):
        p = unit(rng.normal(size=3))
        kind = trial % 6
        psi = min(th, math.pi - th)
        if kind == 0:
            q = p.copy()
        elif kind == 1:
            q = -p
        elif kind == 2:                                   # distance exactly 2 psi (if <= pi)
            q = unit(toward(p, perp(p), min(2 * psi, math.pi)))
        elif kind == 3:                                   # distance exactly psi
            q = unit(toward(p, perp(p), psi))
        else:
            q = unit(rng.normal(size=3))
        w, m = chain(p, q, th)
        assert len(w) == m + 1 and np.allclose(w[0], p) and np.allclose(w[-1], q, atol=1e-9)
        for a, b in zip(w, w[1:]):
            worst = max(worst, abs(float(a @ b) - math.cos(th)))
            assert abs(np.linalg.norm(a) - 1) < 1e-9
        cases += 1
print(f"Lemma: {cases} cases ({len(thetas)} angles incl. degenerate targets): all chains have m+1 unit vectors with the right ends; "
      f"largest |<w_i,w_i+1> - cos(theta)| = {worst:.2e}")

# (a) m is best possible (not claimed in the note): with m-1 steps of spherical length psi <= pi/2 one stays within
# distance (m-1) psi < pi of p (resp. of (-1)^(m-1) p after the sign trick), so the antipode is out of reach.
bad = 0
for th in thetas:
    psi = min(th, math.pi - th)
    m = max(2, math.ceil(math.pi / psi - 1e-9))
    if (m - 1) * psi >= math.pi - 1e-9:
        bad += 1
print(f"(a) (m-1)*psi < pi for all tested angles (so m-1 steps cannot reach every target): {bad == 0}")


# (b) Theorem 3 end to end, paw graph
def build_Q(n, E, lam):
    pairs = [(v, n) for v in range(n)] + [(v, n + 1) for v in range(n)] + [(n, n + 1)]
    Nn = n + 2 + 2 * len(pairs)
    Q = np.zeros((Nn, Nn))
    for v, w in E:
        Q[v, w] = Q[w, v] = -1
    for g, (pp, qq) in enumerate(pairs):
        a, a2 = n + 2 + 2 * g, n + 3 + 2 * g
        Q[a, pp] = Q[pp, a] = 3 * lam; Q[a, qq] = Q[qq, a] = 4 * lam
        Q[a2, pp] = Q[pp, a2] = 3 * lam; Q[a2, qq] = Q[qq, a2] = -4 * lam
    return Q, pairs


n, E = 4, [(0, 1), (1, 2), (0, 2), (2, 3)]
lam = 4 * len(E)
Q, pairs = build_Q(n, E, lam)
Nn = Q.shape[0]
th = math.radians(70.528779)
m = 3
nb = (Nn - 1) * m + 1                      # bonds
Qt = np.zeros((nb + 2, nb + 2), dtype=np.int64)       # indices 1..nb, zero border
for a in range(Nn):
    for b in range(Nn):
        Qt[1 + a * m, 1 + b * m] = int(Q[a, b])
natoms = nb + 1
c = np.zeros((natoms + 1, natoms + 1), dtype=np.int64)
for i in range(1, natoms + 1):
    for j in range(i + 1, natoms + 1):
        # c_ij = Q~_{i,j-1} - Q~_{i-1,j-1} - Q~_{i,j} + Q~_{i-1,j}   (indices 0 or natoms give 0)
        def qv(k, l):
            return int(Qt[k, l]) if 1 <= k <= nb and 1 <= l <= nb else 0
        c[i, j] = qv(i, j - 1) - qv(i - 1, j - 1) - qv(i, j) + qv(i - 1, j)
nz = int(np.count_nonzero(c))
maxabs = int(np.abs(c).max())


def chain_value(spins):
    bonds = [spins[0]]
    for a in range(1, Nn):
        w, mm = chain(spins[a - 1], spins[a], th)
        assert mm == m
        bonds += w[1:]
    bonds = np.array(bonds)
    ang = [float(bonds[k] @ bonds[k + 1]) for k in range(len(bonds) - 1)]
    assert max(abs(x - math.cos(th)) for x in ang) < 1e-9
    x = np.vstack([np.zeros(3), np.cumsum(bonds, axis=0)])
    D2 = ((x[:, None, :] - x[None, :, :]) ** 2).sum(-1)
    return float((c[1:, 1:] * D2).sum())


ok = True
for _ in range(20):
    S = rng.normal(size=(Nn, 3)); S /= np.linalg.norm(S, axis=1, keepdims=True)
    F = 0.5 * float(np.sum(S * (Q @ S)))
    ok &= abs(chain_value(S) - 2 * F) < 1e-6 * max(1.0, abs(F))
# optimal configuration
best, sig = -1, None
for s in itertools.product((1, -1), repeat=n - 1):
    s = (1,) + s
    cut = sum(1 for v, w in E if s[v] != s[w])
    if cut > best:
        best, sig = cut, s
B = np.zeros((Nn, 3))
for v in range(n):
    B[v] = [0, 0, sig[v]]
B[n], B[n + 1] = [1, 0, 0], [0, 1, 0]
for g, (pp, qq) in enumerate(pairs):
    B[n + 2 + 2 * g] = unit(3 * B[pp] + 4 * B[qq]); B[n + 3 + 2 * g] = unit(3 * B[pp] - 4 * B[qq])
target = 10 * lam * (2 * n + 1) + 2 * best - len(E)
val = chain_value(B)
print(f"(b) paw graph: {Nn} spins -> fixed-angle chain with {natoms} atoms (theta = 70.53 deg, m = 3); integer data c: {nz} non-zero "
      f"entries, max |c| = {maxabs}; chain objective = 2 F(b) on 20 random spin configurations: {ok}; on the optimal configuration "
      f"{val:.6f} = 2 * {target} : {abs(val - 2 * target) < 1e-6}")
