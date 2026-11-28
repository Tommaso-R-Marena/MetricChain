"""Instance families F1-F6 of the Phase II validation protocol (docs/engineering/phase2/PROTOCOL.md section 2).

Everything here is deterministic (fixed seeds).  Every observable is scaled affinely to [-1, 1] by its minimum and
maximum over the enumerated space (or its a-priori range for F4/F5); the scaling (a, b) with scaled = a*raw + b is
recorded in ``Instance.scaling``.

The "true" ensemble behind the data is p_true = pi * exp(-R) / Z with R = rho(x) * r(x) and a fixed r: X -> [-1, 1]
(``Instance.r``); for the sensitivity run (a) R = 2 rho(x) r(x).  Data region: box of half-width 0.03 around the exact
averages of p_true (F1, F2, F4); ellipsoid with the correlated covariance ``F3_COV`` around them (F3).
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "src"))
from metricchain_eng import certinf as ci  # noqa: E402

RHOS = [0.2, 0.55, 1.15, 1.7, 2.3]          # Gamma = e^{2 rho} ~ 1.5, 3, 10, 30, 100
HALF = 0.03
F3_SD = 0.03
F3_CORR = np.array([[1.0, 0.5, 0.3], [0.5, 1.0, 0.5], [0.3, 0.5, 1.0]])
F3_COV = F3_SD ** 2 * F3_CORR


def scale(v):
    lo, hi = float(np.min(v)), float(np.max(v))
    a = 2.0 / (hi - lo)
    b = -1.0 - a * lo
    return a * v + b, (a, b, lo, hi)


@dataclass
class Instance:
    name: str
    pi: np.ndarray                 # reference law on the enumerated space (normalised)
    phi: np.ndarray                # (N, m), scaled
    targets: dict                  # name -> f (N,), scaled
    r: np.ndarray                  # the fixed shape of the residual, |r| <= 1
    region_kind: str               # 'box' | 'ellipsoid'
    scaling: dict = field(default_factory=dict)
    extra: dict = field(default_factory=dict)

    @property
    def N(self):
        return self.pi.size


# ------------------------------------------------------------------------------------------------ envelopes
def rho_vec(inst: Instance, env) -> np.ndarray:
    """rho(x) for an envelope label: a float (uniform) or 'var' (F1's state-dependent envelope)."""
    if env == "var":
        m = inst.extra["mag_raw"]
        return 0.55 * (0.5 + np.abs(m))          # in [0.275, 0.825]
    return np.full(inst.N, float(env))


def true_law(inst: Instance, env, factor: float = 1.0) -> np.ndarray:
    R = factor * rho_vec(inst, env) * inst.r
    w = inst.pi * np.exp(-R - (-R).max())
    return w / w.sum()


def region_for(inst: Instance, centre):
    if inst.region_kind == "box":
        return ci.Box(centre, HALF)
    return ci.Ellipsoid(centre, F3_COV, 1.0)


def data_region(inst: Instance, env, factor: float = 1.0):
    p = true_law(inst, env, factor)
    return region_for(inst, p @ inst.phi), p


def _r_shape(phi, rng, N):
    xi = rng.uniform(-1, 1, N)
    r = 0.6 * phi[:, 0] - 0.3 * phi[:, 1 % phi.shape[1]] + 0.4 * xi
    return np.clip(r, -1, 1)


# ------------------------------------------------------------------------------------------------ F1
def f1() -> Instance:
    n, J, h = 14, 0.4, 0.1
    idx = np.arange(1 << n)
    s = 1 - 2 * ((idx[:, None] >> np.arange(n)) & 1)          # spins +-1
    nn = (s * np.roll(s, -1, axis=1)).mean(axis=1)
    nnn = (s * np.roll(s, -2, axis=1)).mean(axis=1)
    mag = s.mean(axis=1)
    e = -(J * (s * np.roll(s, -1, axis=1)).sum(axis=1) + h * s.sum(axis=1))
    pi = np.exp(-(e - e.min()))
    pi /= pi.sum()
    sc = {}
    p1, sc["magnetisation"] = scale(mag)
    p2, sc["nn_corr"] = scale(nn)
    t1, sc["nnn_corr"] = scale(nnn)
    t2, sc["abs_mag"] = scale(np.abs(mag))
    phi = np.column_stack([p1, p2])
    r = _r_shape(phi, np.random.default_rng(101), 1 << n)
    return Instance("F1", pi, phi, {"nnn_corr": t1, "abs_mag": t2}, r, "box", sc, {"mag_raw": mag})


# ------------------------------------------------------------------------------------------------ F2
def f2() -> Instance:
    n, q = 7, 4
    rng = np.random.default_rng(202)
    h1 = rng.normal(0, 0.5, (n, q))
    J = rng.normal(0, 0.3, (n, n, q, q))
    idx = np.arange(q ** n)
    x = (idx[:, None] // q ** np.arange(n)) % q
    e = np.zeros(idx.size)
    for i in range(n):
        e += h1[i, x[:, i]]
        for j in range(i + 1, n):
            e += J[i, j, x[:, i], x[:, j]]
    pi = np.exp(-(e - e.min()))
    pi /= pi.sum()
    sc = {}
    cols = []
    for (site, st) in [(0, 0), (1, 1), (2, 2)]:
        v, sc[f"pop_x{site}={st}"] = scale((x[:, site] == st).astype(float))
        cols.append(v)
    phi = np.column_stack(cols)
    t, sc["pop_x3=0_x4=1"] = scale(((x[:, 3] == 0) & (x[:, 4] == 1)).astype(float))
    r = _r_shape(phi, np.random.default_rng(203), idx.size)
    return Instance("F2", pi, phi, {"pair_pop": t}, r, "box", sc)


# ------------------------------------------------------------------------------------------------ F3
def saws(steps: int) -> np.ndarray:
    moves = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]])
    out = []

    def rec(path, occ):
        if len(path) == steps + 1:
            out.append(np.array(path))
            return
        x = path[-1]
        for mv in moves:
            y = (x[0] + mv[0], x[1] + mv[1], x[2] + mv[2])
            if y not in occ:
                occ.add(y)
                path.append(y)
                rec(path, occ)
                path.pop()
                occ.remove(y)

    rec([(0, 0, 0)], {(0, 0, 0)})
    return np.stack(out).astype(float)


def f3() -> Instance:
    X = saws(7)                                               # (81390, 8, 3)
    d2 = ci.sq_distances(X)
    nb = X.shape[1]
    iu = [(i, j) for i in range(nb) for j in range(i + 3, nb)]
    contacts = sum((d2[:, i, j] == 1.0).astype(int) for i, j in iu)
    e = -0.5 * contacts
    pi = np.exp(-(e - e.min()))
    pi /= pi.sum()
    sc = {}
    cols = []
    for (i, j) in [(0, 7), (0, 4), (3, 7)]:
        v, sc[f"d2_{i}_{j}"] = scale(d2[:, i, j])
        cols.append(v)
    phi = np.column_stack(cols)
    k0 = int(np.argmax(contacts))                             # first lowest-energy conformation in enumeration order
    om = ci.projection_stress(X[k0])
    st = ci.stress_values(X, om)
    t1, sc["stress"] = scale(st)
    cen = X - X.mean(axis=1, keepdims=True)
    rg2 = (cen ** 2).sum(axis=2).mean(axis=1)
    t2, sc["rg2"] = scale(rg2)
    r = _r_shape(phi, np.random.default_rng(303), X.shape[0])
    return Instance("F3", pi, phi, {"stress": t1, "rg2": t2}, r, "ellipsoid", sc,
                    {"lowest_index": k0, "max_contacts": int(contacts.max())})


# ------------------------------------------------------------------------------------------------ F4
F4_SITES = 100


def f4_params():
    rng = np.random.default_rng(404)
    p = rng.uniform(0.2, 0.8, F4_SITES)
    sgn = rng.choice([-1.0, 1.0], F4_SITES)
    return p, sgn


def f4_cells(rho: float, factor: float = 1.0):
    """Level counts of (k1 = ones in sites 1-20, k2 = ones in 21-50, k3 = ones in 51-100) under the product
    reference (Proposition 8.1, ci.product_joint_law), and the scaled phi, f of each cell.  The true ensemble is the
    product with R(x) = factor * (rho/50) * sum_i sgn_i (x_i - 1/2), |R| <= factor * rho."""
    p, sgn = f4_params()
    stats = [[[0, 0, 0], [int(i < 20), int(20 <= i < 50), int(i >= 50)]] for i in range(F4_SITES)]
    law = ci.product_joint_law([[1 - q, q] for q in p], stats)
    cells, prob = ci.cells_from_law(law)
    k1, k2, k3 = cells[:, 0], cells[:, 1], cells[:, 2]
    phi = np.column_stack([2 * (k1 + k2) / 50 - 1, 2 * k3 / 50 - 1])
    f = 2 * k1 / 20 - 1
    # true product law: site logit shifted by -factor*rho/50*sgn
    lg = np.log(p / (1 - p)) - factor * rho / 50 * sgn
    pt = 1 / (1 + np.exp(-lg))
    centre = np.array([2 * pt[:50].sum() / 50 - 1, 2 * pt[50:].sum() / 50 - 1])
    true_f = 2 * pt[:20].sum() / 20 - 1
    return dict(prob=prob, phi=phi, f=f, centre=centre, true_f=true_f, p=p, pt=pt, ncells=len(prob))


def f4_draw(rng, n, chunk=20000):
    """n exact draws from the product reference, site by site; returns (phi, f) scaled."""
    p, _ = f4_params()
    phis, fs = [], []
    for s in range(0, n, chunk):
        k = min(chunk, n - s)
        x = rng.random((k, F4_SITES)) < p
        k1 = x[:, :20].sum(1)
        k2 = x[:, 20:50].sum(1)
        k3 = x[:, 50:].sum(1)
        phis.append(np.column_stack([2 * (k1 + k2) / 50 - 1, 2 * k3 / 50 - 1]))
        fs.append(2 * k1 / 20 - 1)
    return np.concatenate(phis), np.concatenate(fs).astype(float)


def get(name: str) -> Instance:
    return {"F1": f1, "F2": f2, "F3": f3}[name]()


if __name__ == "__main__":
    import json
    import time
    for nm in ("F1", "F2", "F3"):
        t = time.time()
        I = get(nm)
        print(nm, I.N, I.phi.shape, list(I.targets), round(time.time() - t, 2), json.dumps(I.scaling)[:300], I.extra.get("max_contacts"))
    t = time.time()
    c = f4_cells(0.55)
    print("F4 cells", c["ncells"], round(time.time() - t, 2), c["centre"], c["true_f"])
