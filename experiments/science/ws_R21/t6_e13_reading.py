"""T6 — Corollary E1.3(b) and its reading (own code).

 (a) replication of E1.3(b) on the free configuration space (R^2)^N: nu = law of R*p with R^2 in {0,2},
     and the general mechanism (random affine images p*A with E[A A^T] = I): same mean squared length
     of every pair, different ensemble.
 (b) the same trick for any single power: observables r^alpha (alpha = -6): R^alpha in {1-s, 1+s}.
 (c) chains with fixed bond lengths (planar, unit bonds, all pairs measured): the function
         f(p) = || P_perp b(p) ||_F^2 ,  b = bond vectors, P = projector on the column space of b(x),
     is a linear function of the squared distances of all pairs on the chain space, is >= 0, and
     vanishes exactly on the affine images of x that are chains; Proposition A (R21 report) says these
     are the congruent copies iff the bond directions are not on a conic at infinity.  Checked: zeros of
     f found by minimisation over the chain space; the degenerate case (two parallel bonds) with the
     explicit two-point mixture that has the mean squared distances of x.
 (d) two generic chain conformers: all solutions S = M M^T (M = [A1; A2], 4x2) of
         c_u S c_u^T = 1  for every bond u,  c_u = (b_u(x1), b_u(x2)) in R^4,  S psd of rank <= 2,
     i.e. all chains of the form x1*A1 + x2*A2 (the only ones an ensemble with the mean squared
     distances of w1*x1 + w2*x2 can charge).  Counted as a function of the number of bonds.
"""
import numpy as np
from r21_common import *

rng = np.random.default_rng(2106)
print("T6 E1.3 and its reading  start", now())

# ---------------------------------------------------------------- (a)
N = 5
EF = complete(N)
X = rng.standard_normal((2, N, 2))
w = np.array([0.3, 0.7])
m_mu = w @ sqlen(X, EF)
# nu = law of R p, R^2 in {0, 2} with probability 1/2 each
conf_nu = np.concatenate([0.0 * X, np.sqrt(2.0) * X])
w_nu = np.concatenate([0.5 * w, 0.5 * w])
m_nu = w_nu @ sqlen(conf_nu, EF)
Q_mu = np.sum(sqlen(X, EF), axis=1)
print(f"(a) E1.3(b), N=5, K=2, all 10 pairs: max |mean sq. length under nu - under mu| = {np.max(np.abs(m_nu - m_mu)):.1e}; "
      f"P_mu(Q=0) = {float(np.sum(w[Q_mu == 0])):.2f}, P_nu(Q=0) = {float(np.sum(w_nu[np.sum(sqlen(conf_nu, EF), axis=1) == 0])):.2f}")
# general mechanism: affine images with E[A A^T] = I  (points are rows: p -> p A)
B1 = rng.standard_normal((2, 2)) * 0.4 + np.eye(2)
S1 = B1 @ B1.T
t = 0.5 / np.linalg.eigvalsh(S1).max()          # weight of A1 so that I - t*S1 stays positive definite
S2 = (np.eye(2) - t * S1) / (1 - t)
A2 = np.linalg.cholesky(S2)
confs = np.concatenate([X @ B1, X @ A2])
w_aff = np.concatenate([t * w, (1 - t) * w])
m_aff = w_aff @ sqlen(confs, EF)
d_cong = min(np.max(np.abs(sqlen(c, EF) - sqlen(x, EF))) for c in confs for x in X)
print(f"    affine mechanism (A1 with weight {t:.3f}, A2 with weight {1-t:.3f}, t*A1A1^T + (1-t)*A2A2^T = I): "
      f"max |difference of mean sq. lengths| = {np.max(np.abs(m_aff - m_mu)):.1e}; smallest max-difference of the "
      f"distance vectors between a conformer of nu and one of mu = {d_cong:.3f}")

# ---------------------------------------------------------------- (b)
alpha = -6.0
s = 0.5
Rs = np.array([(1 - s) ** (1 / alpha), (1 + s) ** (1 / alpha)])
r_mu = w @ (sqlen(X, EF) ** (alpha / 2))
confs = np.concatenate([Rs[0] * X, Rs[1] * X])
r_nu = np.concatenate([0.5 * w, 0.5 * w]) @ (sqlen(confs, EF) ** (alpha / 2))
print(f"(b) observables r^-6 on all pairs: scaling by R with R^-6 in {{0.5, 1.5}} (R = {Rs[0]:.4f}, {Rs[1]:.4f}): "
      f"max relative difference of <r^-6> = {np.max(np.abs(r_nu / r_mu - 1)):.1e}")

# ---------------------------------------------------------------- (c)


def chain(phi):
    """phi: (B, nb) bond directions -> bond vectors (B, nb, 2)"""
    return np.stack([np.cos(phi), np.sin(phi)], axis=-1)


def chain_points(phi):
    b = chain(phi)
    return np.concatenate([np.zeros((phi.shape[0], 1, 2)), np.cumsum(b, axis=1)], axis=1)


def lm_free(resfun, Z0, iters=300):
    """batched LM with a finite-difference Jacobian (small problems)."""
    def fun(Z, want_jac):
        r = resfun(Z)
        if not want_jac:
            return r, None
        h = 1e-6
        J = np.zeros((Z.shape[0], r.shape[1], Z.shape[1]))
        for k in range(Z.shape[1]):
            Zp = Z.copy(); Zp[:, k] += h
            Zm = Z.copy(); Zm[:, k] -= h
            J[:, :, k] = (resfun(Zp) - resfun(Zm)) / (2 * h)
        return r, J
    return batched_lm(fun, Z0, iters=iters)


print("(c) planar chains with unit bonds; observables: mean squared distance of every pair of chain atoms")
for nb, label in ((2, "2 bonds (directions always on a conic)"), (3, "3 bonds"), (4, "4 bonds"), (6, "6 bonds")):
    viol = 0
    gaps = []
    n_inst = 20
    extra_zero = 0
    cong_zero = 0
    for inst in range(n_inst):
        phi_x = rng.uniform(0, 2 * np.pi, nb)
        bx = chain(phi_x[None])[0]                         # (nb, 2)
        Qm, _ = np.linalg.qr(bx)                           # orthonormal basis of col(b(x))
        Pperp = np.eye(nb) - Qm @ Qm.T
        # f is linear in the squared distances of all pairs: check on random chains
        if inst == 0:
            Np = nb + 1
            EFc = complete(Np)
            ph = rng.uniform(0, 2 * np.pi, (400, nb))
            Tall = sqlen(chain_points(ph), EFc)
            fv = np.einsum('uv,bud,bvd->b', Pperp, chain(ph), chain(ph))
            Afit = np.hstack([Tall, np.ones((400, 1))])
            coef, res, rk, sv = np.linalg.lstsq(Afit, fv, rcond=None)
            lin_err = np.max(np.abs(Afit @ coef - fv))

        def resfun(Z):
            b = chain(Z)                                   # (B, nb, 2)
            return np.einsum('uv,bvd->bud', Pperp, b).reshape(Z.shape[0], -1)

        Z0 = rng.uniform(0, 2 * np.pi, (400, nb))
        Z, cost, gn = lm_free(resfun, Z0)
        zero = cost < 1e-18
        # congruence class: compare all pair distances
        Np = nb + 1
        EFc = complete(Np)
        Tx = sqlen(chain_points(phi_x[None]), EFc)[0]
        dT = np.max(np.abs(sqlen(chain_points(Z), EFc) - Tx[None]), axis=1)
        noncong_zero = zero & (dT > 1e-6)
        extra_zero += int(noncong_zero.sum())
        cong_zero += int((zero & (dT <= 1e-6)).sum())
        pos = cost[(~zero) & (gn < 1e-6)]
        if len(pos):
            gaps.append(pos.min())
    print(f"    {label}: {n_inst} random conformations x 400 minimisations of f over the chain space; zeros of f that are NOT "
          f"congruent to x: {extra_zero} (control: minimisations that reach a zero congruent to x: {cong_zero}/{400*n_inst})" + (f"; f is an affine function of the pair squared distances on the chain space to {lin_err:.1e}" if nb >= 2 else "")
          + (f"; smallest positive local minimum of f: {min(gaps):.3e}" if gaps else ""))
# degenerate case with explicit mixture: 3 bonds, bonds 1 and 3 parallel
phi_x = np.array([0.3, 1.7, 0.3])
x = chain_points(phi_x[None])[0]
bx = chain(phi_x[None])[0]
# S symmetric with b S b^T = 0 for the two distinct directions
Mat = np.array([[b[0] * b[0], 2 * b[0] * b[1], b[1] * b[1]] for b in bx[:2]])
ns = np.linalg.svd(Mat)[2][-1]
S = np.array([[ns[0], ns[1]], [ns[1], ns[2]]])
S /= np.abs(np.linalg.eigvalsh(S)).max()
tt = 0.4
out = []
for sign in (+1, -1):
    ev, U = np.linalg.eigh(np.eye(2) + sign * tt * S)
    A = U @ np.diag(np.sqrt(ev)) @ U.T
    out.append(x @ A)
out = np.array(out)
EFc = complete(4)
bond_err = np.max(np.abs(sqlen(out, [(0, 1), (1, 2), (2, 3)]) - 1.0))
mean_err = np.max(np.abs(0.5 * (sqlen(out[0], EFc) + sqlen(out[1], EFc)) - sqlen(x, EFc)))
noncong = np.max(np.abs(sqlen(out[0], EFc) - sqlen(x, EFc)))
print(f"    degenerate conformation (3 bonds, bonds 1 and 3 parallel): two chains p(+t), p(-t) = x (I +- tS)^(1/2), t = {tt}: "
      f"max |bond length^2 - 1| = {bond_err:.1e}; max |mean sq. distance of the 50/50 mixture - that of x| over all pairs = {mean_err:.1e}; "
      f"max |sq. distance of p(+t) - that of x| = {noncong:.3f}  => delta_x NOT determined")

print("DONE t6_e13_reading", now())
