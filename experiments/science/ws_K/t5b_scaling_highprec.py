"""
T5b — two complements to T5.

(A) High-precision check of the potential-theoretic hitting-time identity
        E_a[tau_b] = sum_y pi(y) h_{a,b}(y) / cap(a,b)
    in a regime where float64 fails (pi(a) ~ 1e-20): mpmath, 60 digits, n=6 binary complete model.

(B) Curie–Weiss, exact lumped birth–death chain in m = number of up spins (the principal Dirichlet
    eigenfunction of a permutation-invariant set is permutation invariant, so lambda_A of the full
    2^n-state Metropolis chain equals that of the lumped chain).  For A = {m < m*} (m* = barrier top):
        k_1cut  = Q(A,A^c)/pi(A)                                    (one cut = discrete TST)
        k_mcut  = min_{m0 < m*} [ sum_{m=m0}^{m*-1} 1/C_m ]^{-1} / pi(m <= m0)   (test function of q; series law)
        lambda_A exact (tridiagonal eigenproblem)
    Scaling in n of lambda_A/k_1cut (recrossing) and lambda_A/k_mcut.

Run:  OMP_NUM_THREADS=1 python3 t5b_scaling_highprec.py
"""
import numpy as np
import mpmath as mp
from math import lgamma
from scipy.linalg import eigh_tridiagonal
from kcore import Space, random_pairwise, pairwise_energy, local_minima, barrier_from


def part_A():
    mp.mp.dps = 60
    rng = np.random.default_rng(3)
    S = Space([2] * 6)
    beta = 8.0
    # find an instance with a strict non-global local minimum of tiny Gibbs weight
    for trial in range(200):
        h, J = random_pairwise(S, rng, graph="complete", scale_h=0.5, scale_J=1.0)
        E = pairwise_energy(S, h, J)
        mins = [u for u in local_minima(S, E, strict=True) if E[u] > E.min() + 3.0]
        if mins:
            a = mins[0]
            b = int(np.argmin(E))
            break
    Em = [mp.mpf(float(e)) for e in E]
    Emin = min(Em)
    w = [mp.e ** (-beta * (e - Emin)) for e in Em]
    Z = mp.fsum(w)
    pi = [x / Z for x in w]
    N = S.N

    def rate(u, v):
        return mp.e ** (-beta * max(Em[v] - Em[u], 0))

    Q = mp.zeros(N, N)
    for u in range(N):
        tot = mp.mpf(0)
        for v in S.nbrs[u]:
            v = int(v)
            Q[u, v] = rate(u, v)
            tot += Q[u, v]
        Q[u, u] = -tot
    free = [u for u in range(N) if u not in (a, b)]
    # equilibrium potential h (1 at a, 0 at b)
    M = mp.zeros(len(free), len(free))
    rhs = mp.zeros(len(free), 1)
    for r, u in enumerate(free):
        for s, v in enumerate(free):
            M[r, s] = -Q[u, v]
        rhs[r] = Q[u, a]
    hf = mp.lu_solve(M, rhs)
    hvec = [mp.mpf(0)] * N
    hvec[a] = mp.mpf(1)
    for r, u in enumerate(free):
        hvec[u] = hf[r]
    cap = mp.mpf(0)
    for u in range(N):
        for v in S.nbrs[u]:
            v = int(v)
            if u < v:
                cap += pi[u] * Q[u, v] * (hvec[u] - hvec[v]) ** 2
    # mean hitting time of b
    nb = [u for u in range(N) if u != b]
    M2 = mp.zeros(len(nb), len(nb))
    for r, u in enumerate(nb):
        for s, v in enumerate(nb):
            M2[r, s] = -Q[u, v]
    wv = mp.lu_solve(M2, mp.ones(len(nb), 1))
    Ea = wv[nb.index(a)]
    lhs = Ea * cap
    rhs_ = mp.fsum(pi[u] * hvec[u] for u in range(N))
    rel = abs(lhs / rhs_ - 1)
    print(f"T5b(A) n=6 binary complete, beta={beta}: pi(a) = {mp.nstr(pi[a], 5)}, E_a[tau_b] = {mp.nstr(Ea, 8)}, "
          f"cap = {mp.nstr(cap, 8)}")
    print(f"        identity E_a[tau_b]*cap / sum pi h - 1 = {mp.nstr(rel, 3)}   (60-digit arithmetic)")
    # the same in float64, to exhibit the loss of precision
    Qf = np.array([[float(Q[u, v]) for v in range(N)] for u in range(N)])
    pif = np.array([float(x) for x in pi])
    idx = np.array(free)
    hff = np.zeros(N)
    hff[a] = 1.0
    hff[idx] = np.linalg.solve(-Qf[np.ix_(idx, idx)], Qf[idx, a])
    C = pif[:, None] * Qf
    np.fill_diagonal(C, 0)
    capf = 0.5 * np.sum(C * (hff[:, None] - hff[None, :]) ** 2)
    nbi = np.array(nb)
    wf = np.linalg.solve(-Qf[np.ix_(nbi, nbi)], np.ones(len(nb)))
    Eaf = wf[nb.index(a)]
    print(f"        float64: identity defect = {abs(Eaf * capf / (pif * hff).sum() - 1):.2e}")


def cw_lumped(n, beta, Jc=1.0, hfield=0.0):
    m = np.arange(n + 1)
    mag = 2 * m - n
    E = -(Jc / (2.0 * n)) * mag ** 2 - hfield * mag
    logw = np.array([lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) for k in m]) - beta * E
    logw -= logw.max()
    pi = np.exp(logw)
    pi /= pi.sum()
    up = (n - m[:-1]) * np.minimum(1.0, np.exp(-beta * (E[1:] - E[:-1])))      # m -> m+1
    C = pi[:-1] * up                                                          # conductance level m <-> m+1
    return m, E, pi, C


def part_B():
    print("T5b(B) Curie–Weiss lumped chain, J=1, h=0: A = {m < m*}, m* = top of the free-energy barrier")
    print("   n     beta  m*   pi(A)     lambda_A     lam/k_1cut  lam/k_mcut  (best m0)  F-barrier/kT")
    for beta in (1.3, 1.6):
        for n in (10, 20, 40, 80, 160, 320, 640):
            m, E, pi, C = cw_lumped(n, beta, 1.0, 0.0)
            # free energy profile: -ln pi; the barrier top is the minimum of pi between the two wells
            half = n // 2
            mstar = int(np.argmin(pi[n // 4: 3 * n // 4 + 1]) + n // 4)
            A = m < mstar
            piA = pi[A].sum()
            k1 = C[mstar - 1] / piA
            # exact Dirichlet eigenvalue: symmetric tridiagonal on levels 0..mstar-1
            down = pi[:-1] * (C / pi[:-1]) / pi[1:]          # rate m+1 -> m  = C_m / pi_{m+1}
            upr = C / pi[:-1]
            diag = np.zeros(mstar)
            for k in range(mstar):
                diag[k] = (upr[k] if k < n else 0.0) + (down[k - 1] if k > 0 else 0.0)
            off = -np.sqrt(upr[:mstar - 1] * down[:mstar - 1])
            lam = eigh_tridiagonal(diag, off, eigvals_only=True, select="i", select_range=(0, 0))[0]
            # multi-cut bound
            best = (np.inf, None)
            for m0 in range(0, mstar):
                R = np.sum(1.0 / C[m0:mstar])
                val = (1.0 / R) / pi[:m0 + 1].sum()
                if val < best[0]:
                    best = (val, m0)
            ma = int(np.argmax(pi[:mstar]))
            fb = np.log(pi[ma] / pi[mstar])
            if lam < 1e-10:
                # eigenvalue below what float64 resolves for a matrix of norm ~n: do not report ratios
                print(f"   {n:<5d} {beta:<5.2f} {mstar:<4d} {piA:<9.3e} [lambda_A < 1e-10: below float64 resolution, "
                      f"row not reported]   F-barrier/kT = {fb:.2f}")
                continue
            print(f"   {n:<5d} {beta:<5.2f} {mstar:<4d} {piA:<9.3e} {lam:<12.4e} {lam / k1:<11.4f} "
                  f"{lam / best[0]:<11.4f} m0={best[1]:<6d} {fb:.2f}")


if __name__ == "__main__":
    part_A()
    part_B()
