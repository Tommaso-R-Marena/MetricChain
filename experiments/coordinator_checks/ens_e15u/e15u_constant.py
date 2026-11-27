#!/usr/bin/env python3
"""Coordinator's check of the Ensemble division's Proposition E15U (ENSEMBLE-MSG-0005 §2),
written from the statement, and two additions of ours.

Setting (disagreement variables e in {0,1}^n, N = sum e_i, nu a positive measure, a member
is mu = h nu with h nondecreasing, E_nu h = 1).

(1) QUANTITATIVE FORM.  With m_U = E_nu[N | U] - E_nu[N | U^c] and c* = min over nontrivial
    up-sets U:   TV(mu, nu) <= (E_mu N - E_nu N) / c*   for every monotone density, if c* > 0,
    the constant 1/c* is attained (two-level densities), and if c* <= 0 no constant exists.
    [Proof: the layer-cake argument of E15U with "m_U >= 1" replaced by "m_U >= c*".]
(2) THE STAR.  Hub with k leaves, pi ~ exp(-J sum_j x_hub x_j), centre all-plus, slopes lam:
    m_{e_hub = 1} = 1 + k [ 1/(1+e^{2J+lam}) - 1/(1+e^{-2J+lam}) ],  negative for k J of order one:
    no constant e^{O(influence)} exists.
Exact enumeration in floating point; n <= 4 for (1) (all up-sets), k <= 10 for (2).
"""
import itertools, math, random

def upsets(n):
    pts = list(itertools.product((0, 1), repeat=n))
    idx = {p: i for i, p in enumerate(pts)}
    res = []
    for mask in range(1, 2 ** len(pts) - 1):
        ok = True
        for i, p in enumerate(pts):
            if mask >> i & 1:
                for j in range(n):
                    if p[j] == 0:
                        q = p[:j] + (1,) + p[j + 1:]
                        if not (mask >> idx[q] & 1):
                            ok = False; break
                if not ok: break
        if ok: res.append(mask)
    return pts, res

def stats(pts, nu, mask):
    q = sum(nu[i] for i in range(len(pts)) if mask >> i & 1)
    nU = sum(nu[i] * sum(pts[i]) for i in range(len(pts)) if mask >> i & 1) / q
    nC = sum(nu[i] * sum(pts[i]) for i in range(len(pts)) if not (mask >> i & 1)) / (1 - q)
    return q, nU - nC

def ratio(pts, nu, h):
    z = sum(nu[i] * h[i] for i in range(len(pts)))
    mu = [nu[i] * h[i] / z for i in range(len(pts))]
    tv = 0.5 * sum(abs(mu[i] - nu[i]) for i in range(len(pts)))
    dN = sum((mu[i] - nu[i]) * sum(pts[i]) for i in range(len(pts)))
    return tv, dN

def random_monotone(pts, rng):
    # maximum of a few additive nondecreasing log-densities (monotone by construction)
    n = len(pts[0]); k = rng.randint(1, 3)
    comps = [[rng.uniform(0, 2.0) for _ in range(n)] for _ in range(k)]
    offs = [rng.uniform(-1, 1) for _ in range(k)]
    return [math.exp(max(offs[c] + sum(comps[c][j] * p[j] for j in range(n)) for c in range(k))) for p in pts]

def main():
    rng = random.Random(20261126)
    print("(1) quantitative form: TV <= (E_mu N - E_nu N)/c*,  c* = min_U m_U")
    for n in (2, 3, 4):
        pts, ups = upsets(n)
        nmeas = {2: 300, 3: 200, 4: 40}[n]
        pos = neg = 0; worst = -1.0; attained = 0.0; viol = 0; negwit = 0
        for _ in range(nmeas):
            # pair interactions of either sign, fields
            Jm = {(i, j): rng.gauss(0, rng.choice((0.3, 1.0, 2.0))) for i in range(n) for j in range(i + 1, n)}
            f = [rng.gauss(0, 1) for _ in range(n)]
            w = [math.exp(sum(Jm[i, j] * (1 - 2 * p[i]) * (1 - 2 * p[j]) for (i, j) in Jm) - sum(f[i] * p[i] for i in range(n))) for p in pts]
            Z = sum(w); nu = [x / Z for x in w]
            ms = [stats(pts, nu, m) for m in ups]
            cstar = min(m for (_, m) in ms)
            if cstar > 1e-9:
                pos += 1
                # members: random monotone and every two-level density
                for _ in range(60):
                    tv, dN = ratio(pts, nu, random_monotone(pts, rng))
                    if tv > 1e-12:
                        r = tv * cstar / dN if dN > 0 else float('inf')
                        worst = max(worst, r)
                        if r > 1 + 1e-9: viol += 1
                for m in ups:
                    h = [1.0 + 0.7 * (m >> i & 1) for i in range(len(pts))]
                    tv, dN = ratio(pts, nu, h)
                    r = tv * cstar / dN
                    worst = max(worst, r); attained = max(attained, r)
                    if r > 1 + 1e-9: viol += 1
            else:
                neg += 1
                # the two-level member of the minimising up-set has TV > 0 and E_mu N - E_nu N <= 0
                mbest = min(range(len(ups)), key=lambda t: ms[t][1])
                h = [1.0 + 0.7 * (ups[mbest] >> i & 1) for i in range(len(pts))]
                tv, dN = ratio(pts, nu, h)
                if tv > 0 and dN <= 1e-12: negwit += 1
        print(f"  n={n}: up-sets {len(ups)}, measures {nmeas}: c*>0 in {pos} (violations of the bound with 1/c*: {viol}; "
              f"largest TV c*/(E_mu N - E_nu N) = {worst:.12f}, over two-level members {attained:.12f}); "
              f"c*<=0 in {neg}, of which the two-level member has TV>0 and no excess in {negwit}")
        assert viol == 0 and abs(attained - 1) < 1e-9 and negwit == neg
    print("(2) the star: hub with k leaves, pi ~ exp(-J sum_j x_hub x_j), centre all-plus, slope lam at every site")
    for (J, lam) in ((0.5, 1.0), (0.25, 1.0), (0.1, 1.0), (0.5, 0.2)):
        row = []
        for k in range(1, 9):
            n = k + 1
            pts = list(itertools.product((0, 1), repeat=n))
            w = [math.exp(-J * sum((1 - 2 * p[0]) * (1 - 2 * p[j]) for j in range(1, n)) - lam * sum(p)) for p in pts]
            Z = sum(w); nu = [x / Z for x in w]
            mask = sum(1 << i for i, p in enumerate(pts) if p[0] == 1)
            q, m = stats(pts, nu, mask)
            closed = 1 + k * (1 / (1 + math.exp(2 * J + lam)) - 1 / (1 + math.exp(-2 * J + lam)))
            assert abs(m - closed) < 1e-12
            row.append(m)
        kcrit = 1 / (1 / (1 + math.exp(-2 * J + lam)) - 1 / (1 + math.exp(2 * J + lam)))
        print(f"  J={J}, lam={lam}: m_U(k=1..8) = " + " ".join(f"{x:+.4f}" for x in row) + f"   (zero at k = {kcrit:.3f}; total coupling at the hub k*J = {kcrit * J:.3f})")
    # an explicit member beyond the threshold: TV > 0, sum of one-body deficits negative
    J, lam, k = 0.5, 1.0, 3
    n = k + 1
    pts = list(itertools.product((0, 1), repeat=n))
    w = [math.exp(-J * sum((1 - 2 * p[0]) * (1 - 2 * p[j]) for j in range(1, n)) - lam * sum(p)) for p in pts]
    Z = sum(w); nu = [x / Z for x in w]
    h = [math.exp(1.0 * p[0]) for p in pts]            # tilts the hub only: log-increments in [0, 2 lam]
    tv, dN = ratio(pts, nu, h)
    print(f"  member h = exp(e_hub), J={J}, lam={lam}, k={k}: TV = {tv:.6f}, sum of one-body deficits E_mu N - E_nu N = {dN:+.6f}")
    assert tv > 0 and dN < 0
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
