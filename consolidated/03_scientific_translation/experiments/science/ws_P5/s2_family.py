"""
P5 step 2 (explicit family) -- numerical check of Theorem 9 of the report.

Family: N atoms with charges +-q (N/2 of each sign), all pair distances equal to r, the same inverse
Born radius b(x) for all of them.  (N = 2: a bond; N = 4: a regular tetrahedron = two crossed neutral
dipoles; N > 4 is not realisable by points of R^3 but is inside the class of functions that a
term-by-term analysis covers, which never uses the embedding.)  Kernel matrix: b on the diagonal,
h = h(-2 ln b; r) = b psi(r^2 b^2) off it, psi(u) = (u + e^{-u/4})^{-1/2};  chi := b - h.

Claims checked here, each at every state / every sign pattern of every instance of the family:
  (F1)  0 <= (3/8) u - (1 - psi(u)) <= (27/128) u^2                       (grid of u)
  (F2)  g_s = -(kappa/2) q^2 [ N b + ((sum s)^2 - N) h ]                    for every sign pattern s
  (F3)  truth (neutral pattern)  |Delta_T g| = (kappa/2) q^2 N |Delta_T chi|
  (F4)  all-plus pattern         |Delta_T g_+| = (kappa/2) q^2 |N^2 Delta_T b - N(N-1) Delta_T chi|
  (F5)  hence  max_s |Delta_T g_s| / truth  >=  N |Delta_T b| / |Delta_T chi| - (N - 1)
  (F6)  |Delta_T chi| <= 2^(m-1) (3/8) r^2 b_max^3
Part B takes b(I) = the GBn2 rescaling of a real atom class and I = I0 + sum_i a_i x_i with I0 and a_i
read from the real descreening tables of Leu8 on the helix (one backbone carbonyl carbon).
Part C builds the N = 4 member with OpenMM's own descreening integrals (P3's GBModel._H): a tetrahedron
of four charged atoms and T_d-symmetric shells of uncharged atoms as the sites.

usage: python3 -B s2_family.py        (log: logs/s2_family.log)
"""
import sys, os, itertools, time, json
import numpy as np
from p5lib import *

log = Tee(os.path.join(HERE, "logs", "s2_family.log"))
PRE = -0.5 * KAPPA / KCAL                      # kcal nm / mol
psi = lambda u: 1.0 / np.sqrt(u + np.exp(-u / 4.0))


def hker(b, r):
    return b * psi(r * r * b * b)


nchk = nviol = 0


def check(cond, what):
    global nchk, nviol
    nchk += 1
    if not cond:
        nviol += 1
        log(f"    VIOLATION: {what}")


# ----------------------------------------------------------------------------- (F1)
u = np.linspace(0.0, 60.0, 600001)
lo = 0.375 * u - (1.0 - psi(u))
hi = (27.0 / 128.0) * u * u - lo
log(f"(F1) grid of {len(u)} points u in [0, 60]: min of (3/8)u - (1 - psi) = {lo.min():.3e} (>= 0), min of (27/128)u^2 - that = {hi.min():.3e} (>= 0)")
check(lo.min() >= -1e-15 and hi.min() >= -1e-15, "F1")

# ----------------------------------------------------------------------------- real magnitudes
G = GBModel("L8", "H", tau=0.60)
names = list(G.P.names); resid = np.asarray(G.P.resid)
x0 = (1,) * 8
pstar = [p for p in range(G.nat) if names[p] == "C" and resid[p] == 4][0]
fidx = int(np.flatnonzero(G.fixed == pstar)[0])
I0 = float(G.descreening(np.array([x0]))[0, pstar])
a_all = np.array([G.A[i][1 - x0[i], fidx] - G.A[i][x0[i], fidx] for i in range(8)])
cls = dict(orr=float(G.orr[pstar]), rad=float(G.rad[pstar]), al=float(G.al[pstar]), be=float(G.be[pstar]), ga=float(G.ga[pstar]))
log(f"atom class of the family: backbone carbonyl C (atom {pstar}): or = {cls['orr']:.4f} nm, alpha, beta, gamma = {cls['al']:.6f}, {cls['be']:.6f}, {cls['ga']:.6f}")
log(f"    I0 = {I0:.4f} nm^-1 (anchor of Leu8/H); one-site changes a_i of its descreening integral (nm^-1): {np.round(a_all, 4)}")


def ib(I):
    ps = I * cls["orr"]
    return 1.0 / cls["orr"] - np.tanh(cls["al"] * ps - cls["be"] * ps ** 2 + cls["ga"] * ps ** 3) / cls["rad"]


def mixed(vals, m):
    """mixed difference of an array indexed by (x_1..x_m) in {0,1}^m (anchor 0)."""
    D = vals
    for ax in range(m):
        D = np.take(D, [1], axis=ax) - np.take(D, [0], axis=ax)
    return float(D.reshape(-1)[0]) if D.ndim == m else D.reshape(D.shape[m:])


# ----------------------------------------------------------------------------- Part B
log("=== Part B: equidistant family with a common Born radius; q = 0.5 e; kcal/mol")
q = 0.5
order = np.argsort(-np.abs(a_all))
rows = []
for m in (3, 4, 5):
    T = order[:m]
    a = a_all[T]
    grid = np.array(list(itertools.product([0, 1], repeat=m)))
    I = I0 + grid @ a
    b = ib(I).reshape((2,) * m)
    bmax = float(b.max())
    db = mixed(b, m)
    for r in (0.05, 0.10, 0.123, 0.15, 0.20, 0.30, 0.50):
        h = hker(b, r); chi = b - h
        dchi = mixed(chi, m); dh = mixed(h, m)
        check(abs(dchi) <= 2 ** (m - 1) * 0.375 * r * r * bmax ** 3 * (1 + 1e-12), f"F6 m={m} r={r}")
        line = f"    m = {m}, r = {r:5.3f} nm: B in [{1 / bmax:.3f}, {1 / b.min():.3f}] nm, |D b| = {abs(db):.3e}, |D chi| = {abs(dchi):.3e} nm^-1 | ratio (max over signs)/truth:"
        for N in (2, 4, 8, 16, 32, 64):
            truth = abs(PRE) * q * q * N * abs(dchi)
            plus = abs(PRE) * q * q * abs(N * N * db - N * (N - 1) * dchi)
            # exact maximum over sign patterns through k = sum s (F2), and brute force for N <= 12
            ks = np.arange(-N, N + 1, 2)
            vals = np.abs(PRE * q * q * (N * db + (ks.astype(float) ** 2 - N) * dh))
            mx = float(vals.max())
            if N <= 12:
                Mst = b[..., None, None] * np.eye(N) + h[..., None, None] * (1.0 - np.eye(N))      # (2,)*m + (N, N)
                A = mixed(Mst, m)                                                                  # (N, N)
                bf = 0.0
                alt = None
                for s in itertools.product([-1.0, 1.0], repeat=N):
                    s = np.array(s)
                    v = abs(PRE * q * q * float(s @ A @ s))
                    check(abs(v - abs(PRE * q * q * (N * db + (s.sum() ** 2 - N) * dh))) <= 1e-9 * (1 + v), "F2")
                    bf = max(bf, v)
                check(abs(bf - mx) <= 1e-9 * (1 + mx), "max over signs")
                salt = np.array([1.0, -1.0] * (N // 2))
                check(abs(abs(PRE * q * q * float(salt @ A @ salt)) - truth) <= 1e-9 * (1 + truth), "F3")
                check(abs(abs(PRE * q * q * float(np.ones(N) @ A @ np.ones(N))) - plus) <= 1e-9 * (1 + plus), "F4")
            pp = abs(PRE) * q * q * (N * abs(db) + N * (N - 1) * abs(dh))
            bound = N * abs(db) / abs(dchi) - (N - 1)
            check(mx / truth >= bound * (1 - 1e-9), f"F5 m={m} r={r} N={N}")
            check(pp >= mx * (1 - 1e-12), "pair optimum >= sign-blind optimum")
            rows.append(dict(m=m, r=r, N=N, truth=truth, signblind=mx, pair=pp, ratio=mx / truth, bound=bound))
            if N in (2, 4, 16, 64):
                line += f"  N={N}: {mx / truth:8.1f} (>= {bound:7.1f})"
        log(line)

# ----------------------------------------------------------------------------- Part C
log("=== Part C: the N = 4 member built with OpenMM's GBn2 descreening integrals (tetrahedron + T_d-symmetric uncharged shells)")
ce = [p for p in range(G.nat) if names[p] == "CB" and resid[p] == 4][0]          # class of the uncharged shell atoms
vt = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], dtype=float) / np.sqrt(3.0)
octa = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], dtype=float)
cubo = np.array([p for p in itertools.product([-1, 0, 1], repeat=3) if sum(abs(c) for c in p) == 2], dtype=float) / np.sqrt(2.0)
shells = [(-vt, 0.42, 0.80), (octa, 0.45, 0.78), (vt, 0.50, 0.85), (cubo, 0.55, 0.90), (-vt, 0.60, 0.95)]   # (directions, near, far) nm
# a static T_d-symmetric bath of uncharged atoms that buries the cluster (so that B is as large as in the peptide)
bath = np.concatenate([cubo * 0.30, octa * 0.34, vt * 0.37, -vt * 0.37, cubo * 0.40], axis=0)
log(f"    static bath: {len(bath)} uncharged atoms (class of CB) at 0.30-0.40 nm; 5 sites = shells of 4, 6, 4, 12, 4 uncharged atoms moving between two radii")
for m in (3, 4, 5):
    for r in (0.10, 0.123, 0.15, 0.25):
        Xc = vt * r * np.sqrt(3.0 / 8.0)                                         # edge length r
        rcc = np.sqrt(((Xc[:, None] - Xc[None]) ** 2).sum(-1)) + np.eye(4)
        check(np.allclose(rcc[~np.eye(4, dtype=bool)], r), "tetrahedron edge")
        Icc = (G._H(rcc, [pstar] * 4, [pstar] * 4) * (1 - np.eye(4))).sum(-1)
        rcb = np.sqrt(((Xc[:, None] - bath[None]) ** 2).sum(-1))
        Icc = Icc + G._H(rcb, [pstar] * 4, [ce] * len(bath)).sum(-1)
        grid = np.array(list(itertools.product([0, 1], repeat=m)))
        Iall = np.zeros((len(grid), 4))
        for gi, x in enumerate(grid):
            I = Icc.copy()
            for i in range(5):
                d, near, far = shells[i]
                rho = near if (i < m and x[i] == 1) else far
                Xe = d * rho
                rce = np.sqrt(((Xc[:, None] - Xe[None]) ** 2).sum(-1))
                I = I + G._H(rce, [pstar] * 4, [ce] * len(Xe)).sum(-1)
            Iall[gi] = I
        sym = float(np.abs(Iall - Iall[:, :1]).max())
        check(sym < 1e-10, "the four descreening integrals are equal by symmetry")
        b = ib(Iall[:, 0]).reshape((2,) * m)
        h = hker(b, r); chi = b - h
        db, dchi = mixed(b, m), mixed(chi, m)
        Mst = b[..., None, None] * np.eye(4) + h[..., None, None] * (1.0 - np.eye(4))
        A = mixed(Mst, m)
        vals = {}
        for s in itertools.product([-1.0, 1.0], repeat=4):
            s = np.array(s)
            vals[tuple(s)] = abs(PRE * q * q * float(s @ A @ s))
        truth = vals[(1.0, -1.0, 1.0, -1.0)]
        mx = max(vals.values())
        pp = abs(PRE) * q * q * (4 * abs(db) + 12 * abs(mixed(h, m)))
        bound = 4 * abs(db) / abs(dchi) - 3
        check(abs(truth - abs(PRE) * q * q * 4 * abs(dchi)) <= 1e-9 * (1 + truth), "F3 (C)")
        check(mx / truth >= bound * (1 - 1e-9), "F5 (C)")
        check(abs(dchi) <= 2 ** (m - 1) * 0.375 * r * r * float(b.max()) ** 3, "F6 (C)")
        log(f"    m = {m}, r = {r:5.3f} nm: max deviation of the four I_p {sym:.1e}; I in [{Iall.min():.3f}, {Iall.max():.3f}] nm^-1, B in [{1 / b.max():.3f}, {1 / b.min():.3f}] nm; "
            f"truth {truth:.3e}, best sign pattern {mx:.3e}, pair-level optimum {pp:.3e} kcal/mol; ratio {mx / truth:.1f} (>= {bound:.1f})")
# ----------------------------------------------------------------------------- Part D
log("=== Part D: neutral clusters of N charges at random points with a common Born radius (the Remark after Theorem 9)")
rngD = np.random.default_rng(11)
ratios = []
for m in (3, 4, 5):
    T = order[:m]
    grid = np.array(list(itertools.product([0, 1], repeat=m)))
    b = ib(I0 + grid @ a_all[T]).reshape((2,) * m)
    bmax = float(b.max())
    db, db3 = mixed(b, m), mixed(b ** 3, m)
    for N in (4, 8, 16, 32):
        for a_rad in (0.03, 0.06, 0.12, 0.25):
            for rep in range(5):
                Xp = rngD.normal(size=(N, 3)); Xp *= a_rad / np.linalg.norm(Xp, axis=1).max()
                qv = rngD.uniform(0.1, 0.6, size=N) * rngD.choice([-1.0, 1.0], size=N)
                qv -= qv.mean()                                                    # neutral
                rpq = np.sqrt(((Xp[:, None] - Xp[None]) ** 2).sum(-1))
                off = ~np.eye(N, dtype=bool)
                Mst = b[..., None, None] * np.eye(N) + hker(b[..., None, None], rpq + np.eye(N)) * off
                A = mixed(Mst, m)
                truth = PRE * float(qv @ A @ qv)                                   # Delta_T g, kcal/mol
                mu2 = float((qv @ Xp) @ (qv @ Xp))
                lead = 0.75 * PRE * mu2 * db3                                      # -(3 kappa/8)|mu|^2 Delta(b^3)
                aq_ = np.abs(qv)
                errb = abs(PRE) * 2 ** (m - 1) * (27.0 / 128.0) * bmax ** 5 * float((np.outer(aq_, aq_) * rpq ** 4)[off].sum())
                check(abs(truth - lead) <= errb * (1 + 1e-9) + 1e-15, f"D: remainder bound m={m} N={N} a={a_rad}")
                plus = abs(PRE * float(aq_ @ A @ aq_))
                lowp = abs(PRE) * (aq_.sum() ** 2 * abs(db) - 2 ** (m - 1) * 0.375 * bmax ** 3 * float((np.outer(aq_, aq_) * rpq ** 2)[off].sum()))
                check(plus >= lowp * (1 - 1e-9) - 1e-15, f"D: all-plus lower bound m={m} N={N} a={a_rad}")
                if rep == 0 and m == 3:
                    ratios.append((N, a_rad, plus / abs(truth)))
for N in (4, 8, 16, 32):
    log("    m = 3, N = %2d: (all charges positive)/truth for cluster radius 0.03, 0.06, 0.12, 0.25 nm: " % N + ", ".join(f"{v:.0f}" for (n_, a_, v) in ratios if n_ == N))
# ----------------------------------------------------------------------------- Part E
log("=== Part E: the brief's family -- two neutral dipoles (bond d = 0.123 nm, charges +-0.5 e) at distance R, common Born radius; m = 3")
m = 3
T = order[:m]
grid = np.array(list(itertools.product([0, 1], repeat=m)))
b = ib(I0 + grid @ a_all[T]).reshape((2,) * m)
dbond = 0.123
for label, second in (("parallel", (0.5, -0.5)), ("antiparallel", (-0.5, 0.5))):
    line = f"    {label:12s}: R (nm) -> truth (kcal/mol), max over the 16 sign patterns, ratio:"
    for R in (0.2, 0.3, 0.5, 0.8, 1.2, 2.0):
        Xp = np.array([[0, 0, 0], [0, 0, dbond], [R, 0, 0], [R, 0, dbond]], dtype=float)
        qv = np.array([0.5, -0.5, second[0], second[1]])
        rpq = np.sqrt(((Xp[:, None] - Xp[None]) ** 2).sum(-1))
        off = ~np.eye(4, dtype=bool)
        Mst = b[..., None, None] * np.eye(4) + hker(b[..., None, None], rpq + np.eye(4)) * off
        A = mixed(Mst, m)
        truth = abs(PRE * float(qv @ A @ qv))
        mx = max(abs(PRE * float((np.array(sv) * np.abs(qv)) @ A @ (np.array(sv) * np.abs(qv)))) for sv in itertools.product([-1.0, 1.0], repeat=4))
        check(mx >= truth * (1 - 1e-12), "E: max over signs >= truth")
        line += f"  {R:.1f}: {truth:.2e}, {mx:.2e}, {mx / truth:.0f};"
    log(line)
log(f"checks: {nchk}, violations: {nviol}")
with open(os.path.join(HERE, "out", "s2_family.json"), "w") as fh:
    json.dump(dict(rows=rows, checks=nchk, violations=nviol), fh, indent=1)
log.done()
