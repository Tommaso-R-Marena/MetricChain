"""r10_16: validation of r10_blockfield.py (the block-field lower bound used for small p): the
finite-k identity of Proposition I for the two uniform fields per block,
    G_t^(kL)(M) = k G_t^(L) + ln E[c^t] - t ln E_{Q^k}[prod rho0],
against the brute-force Renyi form (the definition) on the whole chain of n = kL sites, and the
operator value of Lambda_blk against exact increments of ln E[c^t]."""
import itertools, time
import numpy as np
from r10lib import *
from r10_blockfield import *

t0 = time.time()
u = 1.0; h = u / 2
worst = 0.0; cnt = 0
for (L, k) in ((3, 2), (4, 2), (2, 3), (5, 2)):
    n = L * k
    for p in (0.3, 0.1, 0.02):
        for t in (0.3, 0.5, 0.8):
            f = joint_first_last_m(L, p)
            val, G, Lam = blockfield_bound(p, u, L, t, f)
            pin = binary_chain_law(n, p); sn = spins(n).astype(float)
            tuples = list(itertools.product((1.0, -1.0), repeat=k))
            sigs = np.array([np.concatenate([np.full(L, s) for s in tp]) for tp in tuples])
            Wn, lnZn = gibbs(pin, -h * (sigs @ sn.T))
            piL = binary_chain_law(L, p); sL = spins(L).astype(float)
            lz = np.log((piL * np.exp(h * sL.sum(axis=1))).sum())
            c = np.exp(lnZn - k * lz)                       # c_phi = Z_phi / z^k
            Mn = c ** t; Mn /= Mn.sum()
            Gdef = -t * np.log(((Mn @ Wn ** t) ** (1 / t)).sum())
            m = np.arange(-L, L + 1).astype(float)
            Bp = (f * np.exp(h * m)[None, None, :]).sum(axis=2) / np.exp(lz)
            Bm = (f * np.exp(-h * m)[None, None, :]).sum(axis=2) / np.exp(lz)
            rho0 = 2 * np.array([[1 - p, p], [p, 1 - p]])
            cc = []
            for tp in tuples:
                v = np.ones(2) @ (Bp if tp[0] > 0 else Bm)
                for s in tp[1:]:
                    v = v @ rho0 @ (Bp if s > 0 else Bm)
                cc.append(v.sum())
            cc = np.array(cc)
            assert np.allclose(cc, c)
            lnEc = np.log((0.5 ** k * cc ** t).sum())
            wq = (1 / t) * (np.logaddexp(t * h * m, -t * h * m) - np.log(2))
            BQ = (f * np.exp(wq)[None, None, :]).sum(axis=2); BQ /= BQ.sum()
            v = np.ones(2) @ BQ
            for _ in range(k - 1):
                v = v @ rho0 @ BQ
            formula = k * (G * L) + lnEc - t * np.log(v.sum())
            worst = max(worst, abs(Gdef - formula)); cnt += 1
print("finite-k identity against the definition: %d cases, largest deviation %.2e" % (cnt, worst))
# Lambda_blk: operator against exact increments of ln E[c^t] over k = 9, 10 blocks (2 matrices)
for (p, L, t) in ((0.05, 6, 0.307), (0.02, 7, 0.256), (0.3, 4, 0.428)):
    f = joint_first_last_m(L, p)
    m = np.arange(-L, L + 1).astype(float)
    lz = np.log((f * np.exp(h * m)[None, None, :]).sum())
    Bp = (f * np.exp(h * m)[None, None, :]).sum(axis=2) / np.exp(lz)
    Bm = (f * np.exp(-h * m)[None, None, :]).sum(axis=2) / np.exp(lz)
    rho0 = 2 * np.array([[1 - p, p], [p, 1 - p]])
    A = [Bp @ rho0, Bm @ rho0]
    ex = []
    for k in (11, 12):
        tot = 0.0
        for tp in itertools.product((0, 1), repeat=k):
            x = np.ones(2)
            for i in tp:
                x = A[i] @ x
            tot += 0.5 ** k * x.sum() ** t
        ex.append(np.log(tot))
    op48 = mom_lyap2(A, [0.5, 0.5], t, 48); op96 = mom_lyap2(A, [0.5, 0.5], t, 96)
    val = blockfield_bound(p, u, L, t, f)[0]
    print("p=%.2f L=%d t=%.3f: Lambda_blk operator N=48 %.9f, N=96 %.9f; exact increment k=11->12 %.9f;  bound per site %.6f"
          % (p, L, t, op48, op96, ex[1] - ex[0], val))
print("time %.0fs" % (time.time() - t0))
