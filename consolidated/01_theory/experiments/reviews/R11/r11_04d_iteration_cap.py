"""R11 / 04d -- finding m1: the report's four headline lower ends are those of an Arimoto iterate
stopped by an iteration cap.  Here: plain Arimoto from the uniform law on the labels with <= 2 walls,
stopped after 300 + int(3e8 / (labels x configurations)) iterations (the cap of y07_block_labels.py,
read after my own runs), then the bound of Proposition I.  Compare with y16_recheck_lower.txt:
G_L = 0.408732091, 0.564818823, 0.638251913, 0.669310392;  bounds 0.034026, 0.040115, 0.044599, 0.044378.

Run:  python3 r11_04d_iteration_cap.py      (about 1 minute)
"""
import numpy as np
from r11lib import *

u = 1.0
h = u / 2


def walls_labels(L, maxwalls):
    sig = configs(L)
    nw = ((sig[:, :-1] * sig[:, 1:]) == -1).sum(axis=1)
    return sig[nw <= maxwalls]


def end_matrix(s, w):
    B = np.zeros((2, 2))
    np.add.at(B, ((s[:, 0] == -1).astype(int), (s[:, -1] == -1).astype(int)), w)
    return B


for p, L, t, repG, repB in ((0.4, 12, 0.459, 0.408732091, 0.034026), (0.3, 14, 0.434, 0.564818823, 0.040115),
                            (0.2, 14, 0.409, 0.638251913, 0.044599), (0.1, 14, 0.380, 0.669310392, 0.044378)):
    labels = walls_labels(L, 2)
    s, pi = chain_law(L, p)
    logP = gibbs_logs(np.log(pi), -h * labels.astype(float) @ s.T.astype(float))
    A = np.exp(t * logP)
    nl = A.shape[0]
    cap = min(40000, 300 + int(3e8 / A.size))
    M = np.full(nl, 1.0 / nl)
    for it in range(cap):
        mt = M @ A
        m = mt ** (1.0 / t)
        S = m.sum()
        c = (A @ (m / mt)) / S ** (1 - t)             # sum_x P^t Q^(1-t)
        M = M * c ** (-t / (1.0 - t))
        M /= M.sum()
    G_L = G_of_M(logP, M, t)
    rho0 = 2 * np.array([[1 - p, p], [p, 1 - p]])
    keep = M > 1e-12
    As = [end_matrix(s, np.exp(lp)) @ rho0 for lp in logP[keep]]
    Lam = moment_lyapunov(As, M[keep] / M[keep].sum(), t, N=96)
    print(f"p={p} L={L} t={t}: {cap} Arimoto iterations from the uniform law:  G_L = {G_L:.9f} (report {repG:.9f});  Lambda_blk = {Lam:.9f};"
          f"  bound = {(G_L + Lam) / L:.6f} (report {repB:.6f});  labels with weight > 1e-5: {(M > 1e-5).sum()}")
