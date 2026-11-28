"""Numerical check of the two repairs proposed in HIERARCHY_REVIEW.md (findings M2 and M3).

M2: bracket B(theta; D, rho) = D^2 + 2 theta D/rho + rho^2 - 2 sqrt(D^2 + (rho - sqrt(theta))^2)  >=  s (s-1)/8, s = 2 sqrt(theta),
    for D > 0, rho >= sqrt(theta), theta > 1/4.
M3: for theta > h and every y outside W_3 the hidden gain bound with the anchor at radius zeta (f(zeta) = min{a, h + delta/2})
    or the report's bound is <= - min{delta/4, h/2, u (kappa - zeta) h / (2 ln 2)},  delta = theta - h.
"""
import math
import numpy as np
from rv_common import consts, fKL, kKL, finv

rng = np.random.default_rng(3)
# ---- M2
worst = 1e300
for th in (0.2501, 0.26, 0.3, 0.5, 1.0, 2.0, 5.0):
    s = 2 * math.sqrt(th)
    D = np.concatenate([np.linspace(1e-9, 3, 3001), np.linspace(3, 60, 600)])[:, None]
    rho = (math.sqrt(th) + np.concatenate([np.linspace(0, 3, 3001), np.linspace(3, 60, 600)]))[None, :]
    B = D ** 2 + 2 * th * D / rho + rho ** 2 - 2 * np.sqrt(D ** 2 + (rho - math.sqrt(th)) ** 2)
    ratio = B.min() / (s * (s - 1) / 8)
    worst = min(worst, ratio)
    print('M2 theta=%.4f: min bracket = %.6f, claimed lower bound s(s-1)/8 = %.6f, sharp value 2 sqrt(theta)-1 = %.6f'
          % (th, B.min(), s * (s - 1) / 8, s - 1))
print('M2: min over theta of (min bracket)/(s(s-1)/8) = %.3f (must be >= 1)' % worst)

# ---- M3
LN2 = math.log(2.0)
bad = 0
cnt = 0
worst_ratio = 1e300
for trial in range(300000):
    u = float(rng.choice([0.5, 1.0, 2.0, 4.0]))
    c = consts(u)
    h, kap, a, pu = c['h'], c['kap'], c['a'], c['pu']
    nP, nQ, nT = int(rng.integers(0, 3)), int(rng.integers(0, 3)), int(rng.integers(0, 3))
    m = nP + nQ + nT
    if m == 0:
        continue
    phi = rng.dirichlet(np.ones(m))
    roles = ['P'] * nP + ['Q'] * nQ + ['T'] * nT
    theta = float(rng.choice([1.02, 1.1, 1.3, 1.8, 3.0])) * h
    delta = theta - h
    R = float(rng.choice([0.0, 0.5, 0.95, 1.05, 1.5, 3.0, 20.0])) * theta * rng.uniform(0.9, 1.1)
    mode = rng.integers(0, 3)
    if mode == 0:
        y = rng.uniform(0, 0.5, m)
    elif mode == 1:
        y = np.where(rng.random(m) < 0.5, pu, 0.5) + 0.0
    else:
        y = np.clip(np.where(rng.random(m) < 0.5, pu, 0.5) + rng.normal(0, 0.02, m), 0, 0.5)
    r = np.array([phi[j] * fKL(y[j]) for j in range(m)])
    iP = [j for j in range(m) if roles[j] == 'P']
    iQ = [j for j in range(m) if roles[j] == 'Q']
    iT = [j for j in range(m) if roles[j] == 'T']
    rP, rQ, rT = r[iP].sum(), r[iQ].sum(), r[iT].sum()
    if min(rP + rQ, R) + rT <= theta:
        continue
    # only the sub-case of the report without margin: x <= R and T not relaxed
    e = y.copy()
    for j in iP + iQ:
        e[j] = max(y[j], kap)
    x = sum(phi[j] * fKL(e[j]) for j in iP)
    rQe = sum(phi[j] * fKL(e[j]) for j in iQ)
    if not (x <= R and rT <= theta - x - rQe):
        continue
    cnt += 1
    zeta = finv(min(a, h + delta / 2))
    claimed = min(delta / 4, h / 2, u * (kap - zeta) * h / (2 * LN2))
    report_bound = -rT - sum(phi[j] * (fKL(y[j]) if y[j] >= kap else kKL(y[j], u)) for j in iP + iQ)
    if rT >= delta / 4:
        best = report_bound
    else:
        e2 = y.copy()
        for j in iP + iQ:
            e2[j] = max(y[j], zeta)
        x2 = sum(phi[j] * fKL(e2[j]) for j in iP)
        tot = sum(phi[j] * fKL(e2[j]) for j in range(m))
        assert tot <= theta + 1e-12            # anchor in W_1
        assert x2 <= R + 1e-12                 # cap is m_vis
        best = sum(phi[j] * (u * (e2[j] - y[j]) - fKL(y[j])) for j in range(m))
    worst_ratio = min(worst_ratio, -best / claimed)
    if best > -claimed + 1e-12:
        bad += 1
print('M3: %d hidden types in the sub-case "x <= R, T not relaxed" with theta > h; margin smaller than claimed: %d; min margin/claimed = %.3f'
      % (cnt, bad, worst_ratio))
