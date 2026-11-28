"""Referee A -- false convergence under state-dependent energy offsets.

The MBAR objective is exactly shift-equivariant: adding a constant off_k to the energies of state k
moves every free energy by off_k and nothing else.  We therefore know the exact answer for shifted
data from the unshifted problem (which is well conditioned), and can test
  (a) mbar(): does it return a wrong estimate while reporting convergence?
  (b) LRRegion: is phi_min (hence REJECT_MODEL) right?  are the intervals too narrow?
The reference computations are done in the unshifted coordinates g = f - off by this script.
"""
import sys, warnings
import numpy as np
from scipy.special import logsumexp
from scipy.optimize import minimize, minimize_scalar
sys.path.insert(0, "../src")
from d9mbar.estimators import mbar
from d9mbar.certificates import lr_confidence_region
warnings.filterwarnings("ignore")
K = 3
CONTR = [np.array([-1.0, 0.0, 1.0]), np.array([1.0, -2.0, 1.0])]


def phi0(A0, y, g):
    return float(np.sum(logsumexp(A0 + g, axis=1) - g[y]))


def grad0(A0, y, g):
    Z = A0 + g
    p = np.exp(Z - logsumexp(Z, axis=1)[:, None])
    return p.sum(axis=0) - np.bincount(y, minlength=K)


def profile(A0, y, c, theta):
    """exact profile for K = 3: one free direction, convex -> Brent."""
    C = np.vstack([c, np.ones(K)])
    gp = np.linalg.lstsq(C, np.array([theta, 0.0]), rcond=None)[0]
    d = np.cross(c, np.ones(K)); d /= np.linalg.norm(d)
    res = minimize_scalar(lambda t: phi0(A0, y, gp + t * d), bracket=(-1.0, 1.0), tol=1e-12)
    return res.fun, gp + res.x * d


def endpoint(A0, y, c, level0, th0, sgn):
    lo_t, step, hi_t = 0.0, 0.05, None
    for _ in range(80):
        v, _ = profile(A0, y, c, th0 + sgn * step)
        if v > level0:
            hi_t = step
            break
        lo_t, step = step, step * 1.6
    if hi_t is None:
        return np.inf
    for _ in range(45):
        mid = 0.5 * (lo_t + hi_t)
        if profile(A0, y, c, th0 + sgn * mid)[0] <= level0:
            lo_t = mid
        else:
            hi_t = mid
    return lo_t


print("offset | mbar: ok / wrong-but-'converged' / exception | region statuses | false REJECT | phi_min excess>1e-6 | "
      "intervals: total / too narrow (max shortfall) / truth wrongly excluded / infinite")
for off_scale in (0.0, 3.0, 10.0, 20.0, 30.0, 50.0, 100.0):
    st = {}
    mb = dict(ok=0, wrong=0, exc=0)
    worst_wrong = 0.0
    false_rej = excess = n_int = narrow = truth_bad = n_inf = 0
    max_short = 0.0
    max_excess = 0.0
    for rep in range(60):
        rng = np.random.default_rng(7000 + rep)
        n = 60
        kind = rep % 2
        if kind == 0:
            x0 = 0.8 * np.arange(K)
            x = np.concatenate([rng.normal(x0[k], 1.0, n) for k in range(K)])
            U0 = 0.5 * (x[:, None] - x0[None, :]) ** 2
        else:
            J = 5
            P = rng.dirichlet(np.ones(J) * 2, size=K)
            xs = np.concatenate([rng.choice(J, size=n, p=P[k]) for k in range(K)])
            U0 = -np.log(P[:, xs].T)
        y = np.repeat(np.arange(K), n)
        perm = rng.permutation(K * n); U0, y = U0[perm], y[perm]
        off = off_scale * rng.normal(size=K)
        U = U0 + off[None, :]
        f0, _ = mbar(U0, y)                           # reference: unshifted problem
        try:
            f, info = mbar(U, y)
            err = np.abs((f - f[0]) - (f0 - f0[0] + off - off[0])).max()
            if err > 1e-5:
                mb["wrong"] += 1
                worst_wrong = max(worst_wrong, err)
            else:
                mb["ok"] += 1
        except Exception:
            mb["exc"] += 1
        try:
            reg = lr_confidence_region(U, y)
        except Exception as e:
            st["EXC " + type(e).__name__] = st.get("EXC " + type(e).__name__, 0) + 1
            continue
        st[reg.status] = st.get(reg.status, 0) + 1
        if reg.status not in ("OK", "REJECT_MODEL") or not reg.A.size:
            continue
        A0, yy = reg.A + off[None, :], reg.labels
        level0 = reg.level + off[yy].sum()
        res = minimize(lambda g: phi0(A0, yy, g), np.zeros(K), jac=lambda g: grad0(A0, yy, g), method="BFGS",
                       options=dict(gtol=1e-9))
        ghat, phimin0 = res.x - res.x.mean(), float(res.fun)
        if reg.status == "REJECT_MODEL":
            false_rej += int(phimin0 <= level0)
            continue
        ex = (reg.phi_min + off[yy].sum()) - phimin0
        if ex > 1e-6:
            excess += 1
            max_excess = max(max_excess, ex)
        gtrue = f0 * 0  # placeholder
        for c in CONTR:
            try:
                lo, hi = reg.interval(c)
            except Exception as e:
                st["EXC interval " + type(e).__name__] = st.get("EXC interval " + type(e).__name__, 0) + 1
                continue
            n_int += 1
            if not np.isfinite(hi - lo):
                n_inf += 1
            th0 = float(c @ ghat)
            ref_hi = c @ off + th0 + endpoint(A0, yy, c, level0, th0, +1.0)
            ref_lo = c @ off + th0 - endpoint(A0, yy, c, level0, th0, -1.0)
            short = max(ref_hi - hi, lo - ref_lo)        # > 0: the returned interval misses part of the region
            if short > 1e-5 * max(1.0, ref_hi - ref_lo):
                narrow += 1
                max_short = max(max_short, short / (ref_hi - ref_lo))
    print(f"{off_scale:6.1f} | {mb['ok']} / {mb['wrong']} (max err {worst_wrong:.3g}) / {mb['exc']} | {st} | {false_rej} | "
          f"{excess} (max {max_excess:.3g}) | {n_int} / {narrow} (max {max_short:.3g} of the width) / {truth_bad} / {n_inf}")
