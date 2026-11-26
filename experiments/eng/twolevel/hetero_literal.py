"""X-014b: Algorithm 2L+ run literally on small cubes with site-dependent slopes — a test of the transfer of
Theorem K1 that ``metricchain_eng.twolevel.hetero`` relies on (its header, item (2)).

An independent, direct transcription of the algorithm of ``docs/workstreams/K_REPORT.md`` §2.2 (theory branch) with
the substitutions of ``hetero.py``: the outer block is n_o sites of one slope u_o, the inner block has any slopes.
The energy is an explicit table on the whole cube, so the fibre averages W(a) and A are known exactly (up to
rounding); the inner bracket procedures are *oracles* that return a valid bracket of ratio exactly e^{x_l} with the
fibre average placed at the bottom, at the top, or at a random place — the theorem allows any valid procedure.
Random outer sample with real fluctuations; nothing is replaced by its mean.

Checked in every run: the bracket contains A; its width is at most x_out when the run stops through the closure
test; no abort; the number of queries is at most C_max; every certificate (p(s_i) <= q_i, l <= A).
Negative controls: the same algorithm with tables for a smaller outer slope than the instance has (the outer
landscape is then outside the class the tables are for), and with the constant K divided.

    python experiments/eng/twolevel/hetero_literal.py            # writes results/x014_literal.json
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel import hetero as H  # noqa: E402
from metricchain_eng.twolevel.certified import tables  # noqa: E402
from metricchain_eng.twolevel.tables import LN2  # noqa: E402


# ---------------------------------------------------------------------------------------------
# Instances: explicit tables of psi on Q_{n_o} x Q_{n_i}, outer coordinates first
# ---------------------------------------------------------------------------------------------
def all_points(n: int) -> np.ndarray:
    return ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)       # bit i = coordinate i


def wdist(X: np.ndarray, c: np.ndarray, us: np.ndarray) -> np.ndarray:
    return np.abs(X - c[None, :]) @ us


def make_instance(kind: str, us: np.ndarray, rng) -> np.ndarray:
    """A member of the class {|psi(x) - psi(x + e_i)| <= u_i}: psi on all 2^n points."""
    n = len(us)
    X = all_points(n)
    if kind == "flat":
        return np.zeros(2 ** n)
    if kind == "cone":
        return wdist(X, X[rng.integers(2 ** n)], us)
    if kind == "cone0":                     # the cone with its apex at the reference point: the first lower bound is an equality
        return wdist(X, X[0], us)
    if kind == "dip":                       # a single dip of random depth in a flat landscape (the hard instance of the lower bound)
        rho = rng.uniform(0.2, 1.0) * us.sum() * 0.5
        return -np.maximum(rho - wdist(X, X[rng.integers(2 ** n)], us), 0.0)
    if kind == "wells":                     # lower envelope of cones with random apex heights
        k = int(rng.integers(2, 6))
        f = np.full(2 ** n, np.inf)
        for _ in range(k):
            f = np.minimum(f, rng.uniform(0, us.sum()) + wdist(X, X[rng.integers(2 ** n)], us))
        return f
    if kind == "ridges":                    # upper envelope of inverted cones
        k = int(rng.integers(2, 6))
        f = np.full(2 ** n, -np.inf)
        for _ in range(k):
            f = np.maximum(f, rng.uniform(0, us.sum()) - wdist(X, X[rng.integers(2 ** n)], us))
        return f
    if kind == "linear":                    # extreme slopes in every coordinate, random signs
        return X @ (us * rng.choice([-1.0, 1.0], size=n))
    if kind == "mixed":
        a = make_instance("wells", us, rng)
        b = make_instance("ridges", us, rng)
        return np.minimum(a, b + rng.uniform(-1, 1) * us.sum() * 0.3)
    raise ValueError(kind)


def check_class(psi: np.ndarray, us: np.ndarray) -> float:
    """The largest violation of |psi(x) - psi(x + e_i)| <= u_i (<= 0 if psi is in the class)."""
    n = len(us)
    idx = np.arange(2 ** n)
    worst = -np.inf
    for i in range(n):
        worst = max(worst, float(np.max(np.abs(psi - psi[idx ^ (1 << i)])) - us[i]))
    return worst


# ---------------------------------------------------------------------------------------------
# The algorithm (K_REPORT.md §2.2), literal
# ---------------------------------------------------------------------------------------------
def run_2l(psi: np.ndarray, n_o: int, C: H.HConstants, T, oracle: str, rng, K_scale: float = 1.0) -> dict:
    """One run on an explicit energy table over the whole cube (uniform reference measure).  ``T``: the tables of the
    outer cube used by the algorithm (normally slope C.u_o).  Everything in logs."""
    n = int(round(math.log2(len(psi))))
    n_i = n - n_o
    # exact fibre averages (the truth; the algorithm sees them only through oracle brackets)
    tab = psi.reshape(2 ** n_i, 2 ** n_o).T                    # tab[a, y]: outer coordinates are the low bits
    lW = np.logaddexp.reduce(-tab, axis=1) - n_i * LN2
    return run_2l_fibres(lW, tab[:, 0], float(psi[0]), n_o, C, T, oracle, rng, K_scale)


def run_2l_fibres(lW: np.ndarray, psi_ref: np.ndarray, psi0: float, n_o: int, C: H.HConstants, T, oracle: str, rng,
                  K_scale: float = 1.0) -> dict:
    """The same run when the instance is given by its fibre averages: ``lW[a] = ln W(a)`` for every point of the
    outer cube (uniform outer marginal), ``psi_ref[a]`` the reference value of the fibre (the centre of its trivial
    bracket) and ``psi0`` the reference value of the instance.  The inner block can then be anything -- in
    particular a block whose law depends on the outer point (``false_certificate.py``)."""
    lam, eta, etap, b = C.lam, C.eta, C.etap, C.b
    xs = C.xs
    L = len(xs) - 1
    J = C.J
    K = max(1, int(math.ceil(K_scale * C.K)))
    lnu = math.log(K) + math.log(C.nu0)
    lA = float(np.logaddexp.reduce(lW) - n_o * LN2)
    ls0 = -psi0 - C.omega
    # the first lower bound: l = e^-psi0 prod_i (1 + e^-u_i)/2, and (1 + e^-u)/2 = e^-u / (2 p_u), so ln l = -psi0 - Omega - ln prod 2 p_u
    lell = -psi0 - C.omega - C.l2p
    queries = 1
    lSigma = -np.inf
    lq_hist: list = []                                         # (level, ln q) of the levels left
    upper_terms = [ls0]
    idx = np.empty(0, dtype=np.int64)
    lL = np.empty(0)
    lU = np.empty(0)
    rung = np.empty(0, dtype=np.int16)
    calls = np.zeros(L + 1, dtype=np.int64)
    Mmax = K * 2 ** C.m_max
    status = None
    omega_i = xs[0] / 2
    certificates_ok = True

    def grow(M):
        nonlocal idx, lL, lU, rung, queries
        if M > len(idx):
            new = rng.integers(0, 2 ** n_o, size=M - len(idx))
            idx = np.concatenate([idx, new])
            lL = np.concatenate([lL, -psi_ref[new] - omega_i])
            lU = np.concatenate([lU, -psi_ref[new] + omega_i])
            rung = np.concatenate([rung, np.zeros(len(new), dtype=np.int16)])
            queries += len(new)

    def classify(M, lsj):
        """Refine the first M points until each is low (U <= s_j) or high (L > s_j e^-b).  Returns False on abort."""
        nonlocal queries
        while True:
            todo = np.flatnonzero((lU[:M] > lsj) & (lL[:M] <= lsj - b))
            if todo.size == 0:
                return True
            if np.any(rung[todo] >= L):
                return False
            rung[todo] += 1
            x = np.asarray(xs)[rung[todo]]
            w = lW[idx[todo]]
            if oracle == "bottom":
                t = np.zeros(todo.size)
            elif oracle == "top":
                t = np.ones(todo.size)
            else:
                t = rng.random(todo.size)
            lL[todo] = np.maximum(lL[todo], w - t * x)
            lU[todo] = np.minimum(lU[todo], w + (1 - t) * x)
            np.add.at(calls, rung[todo], 1)

    lball = T.lball
    for j in range(J + 1):
        lsj = ls0 + j * lam
        M = K
        lell_entry = lell
        stopped = False
        while True:
            if M > Mmax:
                status = "abort: sample size"
                break
            grow(M)
            if not classify(M, lsj):
                status = "abort: unclassified at the last rung"
                break
            high = lU[:M] > lsj
            N = int(high.sum())
            lq = min(0.0, math.log(max(N, K)) - math.log((1 - eta) * M))
            lplow = None
            if N >= K:
                lplow = math.log(N) - math.log((1 + eta) * M)
                k = max(int(np.searchsorted(lball, max(0.0, n_o * LN2 + lplow) + 1e-10, side="right")) - 1, 0)
                lell = max(lell, lsj - b + lplow, lsj - b - n_o * LN2 + float(T.lT[k]))
            # closure test
            if n_o * LN2 + lq < -1e-12:
                ltail = -np.inf
            else:
                r = T.radius(lq)
                ltail = lsj - n_o * LN2 + float(T.lE[r]) if r <= n_o - 1 else np.inf
            if ltail <= C.lth + b + lell:
                lLow = max(lell, lSigma)                 # L = max{ l, Sigma + [N >= K] (1 - e^-lam) e^-b s_j p_low }
                if N >= K:
                    lLow = max(lLow, float(np.logaddexp(lSigma, math.log(-math.expm1(-lam)) - b + lsj + lplow)))
                lUp = float(np.logaddexp.reduce(upper_terms + [ltail]))
                stopped = True
                break
            if N >= K:
                lq_hist.append((j, lq))
                upper_terms.append(lsj + math.log(math.expm1(lam)) + lq)
                lSigma = float(np.logaddexp(lSigma, math.log(-math.expm1(-lam)) - b + lsj + lplow))
                break
            if math.log(M) >= lnu + lsj - lell_entry - b:
                lq_hist.append((j, lq))
                upper_terms.append(lsj + math.log(math.expm1(lam)) + lq)
                break
            M *= 2
        if stopped or status:
            break
    else:
        status = "abort: level J left"
    cost = queries + int(calls.sum())          # every oracle call is charged one query here; C_max is checked with C_l = 1
    if not stopped:
        return dict(status=status or "abort", valid=True, width=2 * C.omega, cost=cost, level=j, lA=lA)
    # certificates: p(s_i) <= q_i at every level left
    for (i, lqi) in lq_hist:
        p = float(np.mean(lW > ls0 + i * lam + 1e-12))
        if p > math.exp(lqi) * (1 + 1e-9):
            certificates_ok = False
    if lell > lA + 1e-9:
        certificates_ok = False
    return dict(status="closed", valid=bool(lLow <= lA + 1e-9 and lA <= lUp + 1e-9), width=lUp - lLow, cost=cost, level=j, lA=lA,
                lL=lLow, lU=lUp, certificates_ok=certificates_ok, M=int(len(idx)), calls=calls.tolist())


def lcmax_unit(C: H.HConstants) -> float:
    """ln C_max with C_l = 1 for every rung (the oracle is charged one query per call)."""
    return float(np.logaddexp.reduce(np.concatenate([[0.0, LN2 + C.lM_bar], C.lmult()])))


def experiment(n_o: int, u_o: float, inner_slopes, design_kw: dict, kinds, oracles, runs: int, seed: int, table_slope: float | None = None,
               K_scale: float = 1.0, lid: float = math.log(20.0)) -> dict:
    us = np.array([u_o] * n_o + list(inner_slopes), dtype=float)
    B = H.make_block([(u_o, n_o)] + [(u, 1) for u in inner_slopes])
    j = [i for i, (u, _) in enumerate(B) if u == u_o][0]
    if B[j][1] != n_o:
        raise ValueError("the inner block must not contain the outer slope (the outer block is the whole type)")
    D = H.HDesign(j=j, k=n_o, **design_kw)
    C = H.constants(B, D, lid)
    T = tables(n_o, u_o if table_slope is None else table_slope)
    rng = np.random.default_rng(seed)
    out = dict(n_o=n_o, u_o=u_o, inner_slopes=list(inner_slopes), design=design_kw, x_out=C.x_out, K=C.K, J=C.J, lCmax_unit=lcmax_unit(C),
               table_slope=u_o if table_slope is None else table_slope, K_scale=K_scale, runs=0, closed=0, invalid=0, too_wide=0, aborted=0,
               over_budget=0, bad_certificates=0, max_width=0.0, max_lcost=0.0, class_violation=-np.inf, by_kind={})
    for kind in kinds:
        stats = dict(runs=0, invalid=0, aborted=0, too_wide=0)
        for _ in range(runs):
            psi = make_instance(kind, us, rng)
            out["class_violation"] = max(out["class_violation"], check_class(psi, us))
            for orc in oracles:
                r = run_2l(psi, n_o, C, T, orc, rng, K_scale)
                out["runs"] += 1
                stats["runs"] += 1
                if r["status"] != "closed":
                    out["aborted"] += 1
                    stats["aborted"] += 1
                else:
                    out["closed"] += 1
                    if not r["valid"]:
                        out["invalid"] += 1
                        stats["invalid"] += 1
                    if r["width"] > C.x_out + 1e-9:
                        out["too_wide"] += 1
                        stats["too_wide"] += 1
                    if not r["certificates_ok"]:
                        out["bad_certificates"] += 1
                    out["max_width"] = max(out["max_width"], r["width"])
                lc = math.log(r["cost"])
                out["max_lcost"] = max(out["max_lcost"], lc)
                if lc > out["lCmax_unit"] + 1e-9:
                    out["over_budget"] += 1
        out["by_kind"][kind] = stats
    return out


KINDS = ("flat", "cone", "cone0", "dip", "wells", "ridges", "linear", "mixed")
ORACLES = ("bottom", "top", "random")
# two parameter sets inside the range of the theorem; eta = 1/2 keeps K (hence the samples) small enough for a literal run
EXT = dict(lam=1.0, eta=0.5, etap=1.0, b=1.0, Lr=4, theta=1.0, bounded=False, name="lam=1, eta=1/2, eta'=1, theta=1, b=1")
BND = dict(lam=0.5, eta=0.25, etap=0.25, b=0.5, Lr=4, theta=0.25, bounded=True, name="lam=1/2, eta=eta'=theta=1/4, b=1/2")


def main() -> int:
    t0 = time.time()
    results = []
    cases = [  # (n_o, u_o, inner slopes)
        (8, 0.5, (2.0, 2.0, 2.0, 2.0)), (8, 2.0, (0.5, 0.5, 0.5, 0.5)), (10, 1.0, (0.4, 0.4, 2.5)), (9, 0.3, (1.0, 1.0, 3.0, 0.7)),
        (10, 1.5, (0.2, 0.2, 0.2, 0.2, 0.2, 0.2)), (7, 1.0, (1.7,))]
    for ci, (n_o, u_o, inner) in enumerate(cases):
        for design in (EXT, BND):
            r = experiment(n_o, u_o, inner, design, KINDS, ORACLES, runs=200, seed=1000 + ci)
            r["what"] = "theorem's constants"
            results.append(r)
            print(f"n_o={n_o} u_o={u_o} inner={inner} [{design['name']}]: {r['runs']} runs, closed {r['closed']}, invalid {r['invalid']}, "
                  f"too wide {r['too_wide']}, aborted {r['aborted']}, over budget {r['over_budget']}, bad certificates {r['bad_certificates']}; "
                  f"max width {r['max_width']:.3f} (x_out {r['x_out']:.3f}); class violation {r['class_violation']:.1e}  [{time.time()-t0:.0f} s]", flush=True)
    # negative controls
    for ci, (n_o, u_o, inner) in enumerate(cases[:4]):
        r = experiment(n_o, u_o, inner, EXT, ("dip", "wells", "cone"), ORACLES, runs=60, seed=2000 + ci, table_slope=u_o / 4)
        r["what"] = "negative control: outer tables for a quarter of the slope"
        results.append(r)
        print(f"CONTROL tables u_o/4: n_o={n_o} u_o={u_o}: {r['runs']} runs, invalid {r['invalid']}, aborted {r['aborted']}", flush=True)
        r = experiment(n_o, u_o, inner, EXT, ("dip", "wells", "cone"), ORACLES, runs=60, seed=3000 + ci, K_scale=1 / 64)
        r["what"] = "negative control: K divided by 64"
        results.append(r)
        print(f"CONTROL K/64: n_o={n_o} u_o={u_o}: {r['runs']} runs, invalid {r['invalid']}, aborted {r['aborted']}, bad certificates {r['bad_certificates']}", flush=True)
    path = ROOT / "experiments" / "eng" / "twolevel" / "results" / "x014_literal.json"
    path.write_text(json.dumps(dict(seconds=time.time() - t0, results=results), indent=1, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
