"""Step 0 -- controls.  (1) the uniform cube from the site function; (2) a block of L = 2, 3 INDEPENDENT uniform sites as
one super-site (alphabet {0,1}^L, envelope = Hamming distance times u): per-site values must be the cube's;
(3) vertex counts 2, 6, 38, 990 and agreement of three enumerations; (4) field control 'bin' of theory report 11.26."""
import sys, time, math
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *

t0 = time.time()
u = 1.0
REF = dict(h=0.029139, a=0.110944, E=0.120115)
print("closed forms (cube, u=1): h=%.6f a=%.6f E=%.6f" % cube_numbers(u))

def report(name, pi, V, L):
    P = gibbs_rows(pi, V)
    G = GameFunction(P, scale=L)
    tst, hlo, hup = G.Rhat(0.0)
    Elo, Eup, ME, QE = E_threshold(P)
    alo, aup, Ma, Qa = capacity(P)
    # independent inner solvers at the optimum t*: SLSQP primal, and the game LP at the Renyi centre
    lo, up, M, Q = renyi_F(P, tst)
    sl = renyi_F_slsqp(P, tst) if P.shape[0] <= 60 else float("nan")
    gm, _ = F_game(P, Q, tst)
    print("%-28s |V|=%4d  h=[%.7f, %.7f] at t*=%.4f | SLSQP %.7f | game-LP at centre %.7f | a=[%.7f, %.7f] | E=[%.7f, %.7f]" % (
        name, len(V), hlo, hup, tst, sl / L, gm / L, alo / L, aup / L, Elo / L, Eup / L))
    return dict(h=hlo, a=alo / L, E=Elo / L, M=M, Mh=M, Ma=Ma, ME=ME, t=tst)

# (1) one binary site
V1 = lip_vertices_trees([u])
r1 = report("cube, one site", [0.5, 0.5], V1, 1)
for k in REF: assert abs(r1[k] - REF[k]) < 6e-7, (k, r1[k])
# (2) blocks of independent uniform sites
for L in (2, 3):
    VT = lip_vertices_trees([u] * L)
    VH = height_functions(L) * u
    assert len(VT) == len(VH) and all(any(np.allclose(f, g) for g in VH) for f in VT)
    add = sitewise_labels([u] * L); add = add - add[:, :1]
    is_add = np.array([any(np.allclose(f, g) for g in add) for f in VT])
    r = report("block of %d independent sites" % L, np.full(2 ** L, 2.0 ** -L), VT, L)
    for k in REF: assert abs(r[k] - REF[k]) < 6e-7, (k, r[k])
    for nm in ("Mh", "Ma", "ME"):
        print("    weight of the %d non-additive vertices in the optimal M for %s: %.3e (the solver's M; any M with the same value is optimal)" % (
            (~is_add).sum(), nm[1:], r[nm][~is_add].sum()))
    # restricted to additive vertices only: same values?
    ra = report("  same, additive labels only", np.full(2 ** L, 2.0 ** -L), [f for f, s in zip(VT, is_add) if s], L)
    for k in REF: assert abs(ra[k] - REF[k]) < 6e-7
    # restricted to NON-additive vertices only (what do they give alone?)
    rn = report("  same, non-additive only", np.full(2 ** L, 2.0 ** -L), [f for f, s in zip(VT, is_add) if not s], L)
# (3) counts
for L in (1, 2, 3, 4):
    H = height_functions(L)
    print("L=%d: %d height functions; all are vertices: %s" % (L, len(H), all(is_vertex(f, [1.0] * L) for f in H)))
# general weights, L = 2, 3: tree enumeration against the brute force of the reference file wv_lib.py (reused ONLY here, as an independent check)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "coordinator_checks", "sites_W"))
import wv_lib
for wts in ([1.0, 1.7], [1.847, 1.847], [0.6, 1.0]):
    d = [[sum(wts[i] for i in range(2) if ((x >> i) & 1) != ((y >> i) & 1)) for y in range(4)] for x in range(4)]
    A = lip_vertices_trees(wts); B = wv_lib.vertices(d)
    print("weights", wts, ": trees", len(A), "wv_lib", len(B), "same set:", len(A) == len(B) and all(any(np.allclose(f, g, atol=1e-7) for g in B) for f in A))
for wts in ([1.847, 1.0, 1.847], [0.677, 1.0, 0.677], [1.0, 1.0, 1.526]):
    A = lip_vertices_trees(wts)
    print("weights", wts, ": %d vertices (tree enumeration); all pass the vertex test: %s" % (len(A), all(is_vertex(f, wts) for f in A)))
# (4) control with a field: 'bin' of the worked example: pi = (0.7, 0.3), u = 1: E = 0.103131, a = 0.095301, h = 0.025034
rb = report("field control bin (0.7,0.3)", [0.7, 0.3], V1, 1)
for k, v in dict(h=0.025034, a=0.095301, E=0.103131).items(): assert abs(rb[k] - v) < 6e-7, (k, rb[k])
print("all controls passed; %.1f s" % (time.time() - t0))
