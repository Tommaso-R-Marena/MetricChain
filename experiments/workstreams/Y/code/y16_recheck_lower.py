"""Independent re-evaluation of the headline lower bounds h >= ... (label laws i.i.d. over blocks, <= 2 walls per block):
(i) the block term G_L(M_L) recomputed directly from M_L (no solver), (ii) the boundary term Lam_blk(t) by the transfer operator
with N = 40 and N = 80 nodes and by EXACT enumeration of E[c_phi^t] for k = 1, 2, 3 blocks (increments converge to Lam_blk),
(iii) the finite-k bound  [k G_L + ln E c^t - t ln E_Q R]/(k L)  which is itself a valid lower bound for F*_{kL}(t)/(kL)."""
import sys, time, math, itertools
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("y07", os.path.join(os.path.dirname(os.path.abspath(__file__)), "y07_block_labels.py"))
t0 = time.time(); u = 1.0
# import the functions of y07 without running its main part
src = open(spec.origin).read().split("# ------------------------------------------------------------------ (1) validation")[0]
ns = {}; exec(src, ns)
block_data, wall_labels, moment_lyap_general = ns["block_data"], ns["wall_labels"], ns["moment_lyap_general"]
for (p, t, L) in ((0.3, 0.434, 14), (0.4, 0.459, 12), (0.2, 0.409, 14), (0.1, 0.380, 14)):
    labels = wall_labels(L, 2)
    GL, mats, probs, lamQ, M, P, Q = block_data(L, p, labels, t)
    s = M @ P ** t; GL2 = -t * math.log(float((s ** (1 / t)).sum()))
    lam40 = moment_lyap_general(mats, probs, t, 40); lam80 = moment_lyap_general(mats, probs, t, 80)
    A = np.array(mats); pr = np.array(probs); one = np.ones(2)
    # exact E[(1' A_1 ... A_k 1)^t]: note c_phi = 1' B_1 rho0 B_2 rho0 ... B_k 1; with A = B rho0 the last factor differs by rho0 (bounded), increments are unaffected
    v1 = A @ one                                              # k = 1: vectors A_i 1
    e1 = math.log(float(pr @ (v1.sum(axis=1) ** t)))
    v2 = np.einsum("iab,jb->ija", A, v1)                      # A_i A_j 1
    e2 = math.log(float(np.einsum("i,j,ij->", pr, pr, v2.sum(axis=2) ** t)))
    keep = pr > 1e-5; A3 = A[keep]; p3 = pr[keep] / pr[keep].sum()
    v1k = A3 @ one; v2k = np.einsum("iab,jb->ija", A3, v1k); v3k = np.einsum("iab,jkb->ijka", A3, v2k)
    e2k = math.log(float(np.einsum("i,j,ij->", p3, p3, v2k.sum(axis=2) ** t)))
    e3k = math.log(float(np.einsum("i,j,k,ijk->", p3, p3, p3, v3k.sum(axis=3) ** t)))
    bound = (GL + lam80 - t * math.log(lamQ)) / L
    print("p=%.1f t=%.3f L=%d: %d labels (%d with weight > 1e-5); G_L = %.9f (recomputed %.9f); Lam_blk: N=40 %.9f, N=80 %.9f; exact increments k=1->2: %.7f, k=2->3 (support truncated at 1e-5): %.7f; ln lam_Q = %.9f;  bound = %.6f   [%.0f s]" % (
        p, t, L, len(labels), int(keep.sum()), GL, GL2, lam40, lam80, e2 - e1, e3k - e2k, math.log(lamQ), bound, time.time() - t0), flush=True)
