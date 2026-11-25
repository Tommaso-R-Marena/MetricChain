"""
T10 — counting cuts at scale: level-resolved minima and partition functions by a transfer matrix with a
counter (equivalently: the chain kernel run over tropical / ordinary POLYNOMIAL weights).

Model: heterogeneous Ising chain, E = -sum_i J_i s_i s_{i+1} - sum_i h_i s_i, single-spin-flip Metropolis.
Statistic q = number of up spins.  a = all-down (metastable for small positive fields), b = all-up.

 (1) validation against brute force (n = 12): min-profile m_r = min_{q=r} E, level partition functions Z_r.
 (2) n = 200 (2^200 states): certified-in-exact-arithmetic-terms quantities (floating point here):
       barrier:   max_{1<=r<=n} m_r  <=  B(a,b)  <=  max energy along an explicit path (grow one domain)
       rate:      for A_r = {q < r}:   k_TST(A_r) <= r Z_r / Z(q<r)   (each level-r state has r neighbours below)
                  and hence P_{pi_A}(no exit before T attempts) >= 1 - T * (r Z_r / n) / Z(q<r) for the
                  discrete-time sampler with uniform site proposals (KineticsCertificates.trap_certificate_weighted)
       series:    cap(q=0 <-> q=n) <= [ sum_{m} Z / min((m+1) Z_{m+1}, (n-m) Z_m) ]^{-1}   (Nash-Williams)
 (3) the Lagrangian (convexified) profile at the top level, to exhibit the failure of T4 at scale.

Run:  python3 t10_counter_dp.py
"""
import itertools
import numpy as np
from scipy.special import logsumexp


def profiles(J, h, beta):
    """m[r] = min energy with r up spins; lnZ[r] = ln sum_{q=r} exp(-beta E).  O(n^2)."""
    n = len(h)
    INF = np.inf
    # state: (spin of current site in {0:down,1:up}, count of up spins)
    mn = np.full((2, n + 1), INF)
    lz = np.full((2, n + 1), -INF)
    for s in (0, 1):
        e = -h[0] * (2 * s - 1)
        mn[s, s] = e
        lz[s, s] = -beta * e
    for i in range(1, n):
        mn2 = np.full((2, n + 1), INF)
        lz2 = np.full((2, n + 1), -INF)
        for s in (0, 1):
            for sp in (0, 1):
                e = -J[i - 1] * (2 * s - 1) * (2 * sp - 1) - h[i] * (2 * s - 1)
                if s == 0:
                    cand_m = mn[sp, :] + e
                    cand_z = lz[sp, :] - beta * e
                else:
                    cand_m = np.concatenate([[INF], mn[sp, :-1] + e])
                    cand_z = np.concatenate([[-INF], lz[sp, :-1] - beta * e])
                mn2[s, :] = np.minimum(mn2[s, :], cand_m)
                lz2[s, :] = np.logaddexp(lz2[s, :], cand_z)
        mn, lz = mn2, lz2
    return mn.min(axis=0), np.logaddexp(lz[0], lz[1])


def energy(J, h, s):
    return -np.sum(J * s[:-1] * s[1:]) - np.sum(h * s)


def brute(J, h, beta):
    n = len(h)
    m = np.full(n + 1, np.inf)
    lz = np.full(n + 1, -np.inf)
    for x in itertools.product((0, 1), repeat=n):
        s = 2 * np.array(x) - 1
        e = energy(J, h, s)
        r = sum(x)
        m[r] = min(m[r], e)
        lz[r] = np.logaddexp(lz[r], -beta * e)
    return m, lz


def convex_envelope(vals):
    """lower convex envelope of the sequence vals[0..n] evaluated at every index."""
    n = len(vals) - 1
    hull = []
    for i in range(n + 1):
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (y2 - y1) * (i - x1) >= (vals[i] - y1) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append((i, vals[i]))
    xs = np.array([p[0] for p in hull])
    ys = np.array([p[1] for p in hull])
    return np.interp(np.arange(n + 1), xs, ys)


def main():
    rng = np.random.default_rng(42)
    # ---------- (1) validation
    n = 12
    J = rng.uniform(0.5, 1.5, n - 1)
    h = 0.2 + rng.normal(0, 0.15, n)
    beta = 1.3
    m, lz = profiles(J, h, beta)
    mb, lzb = brute(J, h, beta)
    print(f"T10(1) n={n}: max |m_r - brute| = {np.abs(m - mb).max():.2e};  max |ln Z_r - brute| = {np.abs(lz - lzb).max():.2e}")
    assert np.abs(m - mb).max() < 1e-10 and np.abs(lz - lzb).max() < 1e-9

    # ---------- (2) n = 200
    n = 200
    J = rng.uniform(0.5, 1.5, n - 1)
    h = 0.2 + rng.normal(0, 0.15, n)
    sdown = -np.ones(n)
    Ea = energy(J, h, sdown)
    Eb = energy(J, h, -sdown)
    m, _ = profiles(J, h, 1.0)
    lower = m[1:].max()                    # every path 0 -> n crosses every level 1..n
    rtop = int(np.argmax(m[1:]) + 1)
    # explicit path: grow one contiguous up-domain; choose start and direction greedily over all nuclei
    best_path = np.inf
    for start in range(n):
        s = sdown.copy()
        lo = hi = start
        s[start] = 1
        e = energy(J, h, s)
        mx = max(Ea, e)
        while lo > 0 or hi < n - 1:
            cands = []
            if lo > 0:
                s[lo - 1] = 1; cands.append((energy(J, h, s), "L")); s[lo - 1] = -1
            if hi < n - 1:
                s[hi + 1] = 1; cands.append((energy(J, h, s), "R")); s[hi + 1] = -1
            e, side = min(cands)
            if side == "L":
                lo -= 1; s[lo] = 1
            else:
                hi += 1; s[hi] = 1
            mx = max(mx, e)
        best_path = min(best_path, mx)
    print(f"T10(2) n={n}: E(a)={Ea:.3f} E(b)={Eb:.3f}")
    print(f"   barrier bracket: max_r min_(q=r) E = {lower:.4f} (level r={rtop})  <=  B(a,b)  <=  {best_path:.4f} "
          f"(best single-domain growth path);  height above a in [{lower - Ea:.4f}, {best_path - Ea:.4f}]")
    env = convex_envelope(m)
    print(f"   Lagrangian (convexified) value at the top level r={rtop}: {env[rtop]:.4f}  "
          f"(trivial bound max(E(a),E(b)) = {max(Ea, Eb):.4f}; true level minimum {m[rtop]:.4f})")
    for beta in (1.0, 2.0, 3.0):
        m, lz = profiles(J, h, beta)
        lnZ = logsumexp(lz)
        # TST bound for A_r = {q < r}: minimise over r in the first part of the profile (before the system has "escaped")
        best = None
        for r in range(1, 40):
            lnZA = logsumexp(lz[:r])
            ln_k = np.log(r) + lz[r] - lnZA           # continuous time, one proposal per neighbour per unit time
            if best is None or ln_k < best[0]:
                best = (ln_k, r, lnZA)
        ln_k, r, lnZA = best
        # Nash-Williams between level 0 and level n
        lnC = np.minimum(np.log(np.arange(1, n + 1)) + lz[1:], np.log(n - np.arange(0, n)) + lz[:-1]) - lnZ
        ln_cap = -logsumexp(-lnC)
        ln_cap_1cut = lnC.min()
        print(f"   beta={beta}: best TST cut A={{q<{r}}}: ln k_TST <= {ln_k:.3f}  => mean exit time from pi_A >= "
              f"{np.exp(-ln_k):.3e} (unit: 1/proposal rate per neighbour); sampler: P(no exit in T attempts) >= 1 - T*"
              f"{np.exp(ln_k) / n:.3e}")
        print(f"            capacity(q=0 <-> q=n): ln cap <= {ln_cap:.3f} (Nash-Williams over {n} levels) vs best single "
              f"level cut {ln_cap_1cut:.3f};  -(1/beta) ln k_TST = {-ln_k / beta:.3f} vs barrier height lower bound "
              f"{lower - Ea:.3f}")


if __name__ == "__main__":
    main()
