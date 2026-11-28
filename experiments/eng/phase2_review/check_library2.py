"""Step 4, second part: edge cases of src/metricchain_eng/certinf (the library is imported here).

1. Non-finite numbers in a sample: which status does certify_upper report?
2. Ellipsoid regions: the descent optimiser against an independent multi-start minimisation (quality, not soundness).
3. sequential_upper (the note's Proposition 9.6) on sites with three ordered states: the docstring says 'exact for
   ... coordinatewise monotone functions'.
4. additive_interval (Corollary 9.3) against a brute-force programme with three-state sites.
5. Wall time of s3_interval when the draws repeat a few states (the solver is not given lumped points).
6. Model-free problems (l = 0) on an ellipsoid: the descent route against an independent minimisation.

Run:  python check_library2.py
"""
from __future__ import annotations

import itertools
import math
import sys
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from metricchain_eng import certinf as ci  # noqa: E402

import ref  # noqa: E402
from check_sec9 import cone_extreme, hamming_edges, product_space  # noqa: E402

rng = np.random.default_rng(777)
warnings.simplefilter("ignore")


def nonfinite():
    N = 6
    pi = rng.dirichlet(np.ones(N) * 2)
    f = rng.uniform(-1, 1, N)
    phi = rng.uniform(-1, 1, (N, 1))
    box = ci.Box(pi @ phi, 0.05)
    d = ci.Declared(-1.0, 1.0, [-1.0], [1.0], 2.0)
    x = rng.choice(N, size=600, p=pi)
    base = ci.Sample(f[x], phi[x], np.ones(600), np.full(600, 2.0))
    clean = ci.certify_upper(base.part(slice(0, 300)), base.part(slice(300, None)), box, d, 0.1)
    print(f"[lib2] clean sample: status = {clean.status!r}, value = {clean.value:.6f}")
    for label, field, val in (("NaN in one validation target value", "f", math.nan),
                              ("NaN in one validation observable", "phi", math.nan),
                              ("NaN in one validation U", "U", math.nan)):
        s = ci.Sample(base.f.copy(), base.phi.copy(), base.L.copy(), base.U.copy())
        arr = getattr(s, field)
        if arr.ndim == 2:
            arr[450, 0] = val
        else:
            arr[450] = val
        try:
            b = ci.certify_upper(s.part(slice(0, 300)), s.part(slice(300, None)), box, d, 0.1)
            print(f"   {label:38s}: status = {b.status!r}, value = {b.value}   (declared f_hi = {d.f_hi})")
        except Exception as exc:  # noqa: BLE001
            print(f"   {label:38s}: raises {type(exc).__name__}")


def ellipsoid_quality():
    worst_gap = 0.0
    unsound = 0
    for _ in range(25):
        N = 40
        u = rng.uniform(0.2, 1.0, N)
        l = u * rng.uniform(0.2, 0.9, N)
        f = rng.uniform(-1, 1, N)
        phi = rng.uniform(-1, 1, (N, 2))
        w = rng.uniform(l, u)
        y = (w @ phi) / w.sum()
        A = rng.normal(size=(2, 2)) * 0.05
        cov = A @ A.T + 1e-4 * np.eye(2)
        ell = ci.Ellipsoid(y, cov, 1.0)
        lib = ci.interval(ci.box_problem(l, u, f, phi, ell))
        hR = lambda e: float(e @ y + math.sqrt(max(float(e @ cov @ e), 0.0)))
        hi_ref, _ = ref.dual_upper(l, u, phi, f, hR, 2, seed=int(rng.integers(1 << 30)))
        lo_ref, _ = ref.dual_upper(l, u, phi, -f, hR, 2, seed=int(rng.integers(1 << 30)))
        lo_ref = -lo_ref
        # both are values of tau*(eta) at some eta, hence upper bounds of the true end; the smaller is the better
        worst_gap = max(worst_gap, lib["hi"] - hi_ref, lo_ref - lib["lo"])
        if lib["hi"] < hi_ref - 1e-6 or lib["lo"] > lo_ref + 1e-6:
            unsound += 1          # would mean the reference minimiser is worse, not that the library is unsound
    print(f"[lib2] ellipsoid regions (m = 2, 40 states, 25 instances): library end minus the best value found by an independent"
          f" multi-start minimisation: at most {worst_gap:.2e}; cases where the library found a better optimum: {unsound}")


def seq_three_states():
    sizes = [3, 3]
    site_pi = [[0.0401, 0.5001, 0.4598], [0.3815, 0.4694, 0.1491]]
    slopes = [1.0038, 1.0722]
    g = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 1.0]])       # 1{x_1 + x_2 >= 3}: coordinatewise monotone
    # statistic S = x_1 + x_2 in {0..4}; terminal[S] = 1{S >= 3}
    stats = [[[0], [1], [2]], [[0], [1], [2]]]
    terminal = (np.arange(5) >= 3).astype(float)
    seq = ci.sequential_upper(site_pi, slopes, stats, terminal)
    states = product_space(sizes)
    pi = np.array([site_pi[0][a] * site_pi[1][b] for a, b in states])
    edges, C = hamming_edges(states, slopes)
    exact = cone_extreme(pi, edges, C, np.array([g[s] for s in states]), sense=+1)
    print(f"[lib2] sequential_upper on two three-state sites, target 1{{x_1 + x_2 >= 3}} (coordinatewise monotone):"
          f" library {seq:.6f}, exact sup over the class {exact:.6f}  -> the bound is sound but NOT exact here")


def additive_three_states():
    worst = 0.0
    for _ in range(30):
        sizes = [int(rng.integers(2, 4)) for _ in range(3)]
        states = product_space(sizes)
        pis = [rng.dirichlet(np.ones(k) * 2) for k in sizes]
        pi = np.array([np.prod([pis[i][s[i]] for i in range(3)]) for s in states])
        slopes = rng.uniform(0.0, 1.5, 3)
        edges, C = hamming_edges(states, slopes)
        fi = [rng.uniform(-1, 1, k) / 3 for k in sizes]
        phii = [rng.uniform(-1, 1, (k, 1)) / 3 for k in sizes]
        f = np.array([sum(fi[i][s[i]] for i in range(3)) for s in states])
        phi = np.array([sum(phii[i][s[i]] for i in range(3)) for s in states])
        y0 = pi @ phi
        box = ci.Box(y0 + 0.02, 0.03)
        A, c = ref.box_region(y0 + 0.02 - 0.03, y0 + 0.02 + 0.03)
        hi = cone_extreme(pi, edges, C, f, phi, A, c, +1)
        lo = cone_extreme(pi, edges, C, f, phi, A, c, -1)
        out = ci.additive_interval(pis, slopes, fi, phii, box)
        if hi is None:
            continue
        worst = max(worst, abs(out["hi"] - hi), abs(out["lo"] - lo))
    print(f"[lib2] additive_interval (Corollary 9.3) vs brute-force programme, sites with 2-3 states, one observable:"
          f" max abs diff = {worst:.2e}")


def model_free_ellipsoid():
    worst = 0.0
    unsound = 0
    nanfree = True
    for _ in range(15):
        N = 30
        u = np.ones(N)
        l = np.zeros(N)
        f = rng.uniform(-1, 1, N)
        phi = rng.uniform(-1, 1, (N, 2))
        w = rng.dirichlet(np.ones(N))
        y = w @ phi
        cov = 0.01 * np.eye(2)
        lib = ci.interval(ci.Problem(f, phi, Lw=0.0, Gw=1.0, region=ci.Ellipsoid(y, cov, 1.0)))
        hR = lambda e: float(e @ y + math.sqrt(max(float(e @ cov @ e), 0.0)))
        hi_ref, _ = ref.dual_upper(l, u, phi, f, hR, 2, seed=int(rng.integers(1 << 30)))
        lo_ref = -ref.dual_upper(l, u, phi, -f, hR, 2, seed=int(rng.integers(1 << 30)))[0]
        g = ci.tau_grad(ci.Problem(f, phi, Lw=0.0, Gw=1.0, region=ci.Ellipsoid(y, cov, 1.0)), np.array([0.3, -0.2]))
        nanfree = nanfree and not np.any(np.isnan(g))
        # inner polygon bracket of the primal: the disc contains its inscribed 64-gon, so that primal value is a lower bound of V+
        ang = np.linspace(0, 2 * np.pi, 64, endpoint=False)
        normals = np.column_stack([np.cos(ang), np.sin(ang)])
        apothem = 0.1 * np.cos(np.pi / 64)
        A, c = normals, normals @ y + apothem
        inner = ref.primal_interval(u * 0, u, phi, f, A, c)
        if inner is not None and (lib["hi"] < inner[1] - 1e-9 or lib["lo"] > inner[0] + 1e-9):
            unsound += 1
        worst = max(worst, lib["hi"] - hi_ref, lo_ref - lib["lo"])
    print(f"[lib2] model-free (l = 0), disc region, 15 instances: library end minus the best independent dual value: at most"
          f" {worst:.2e}; ends inside an inner primal bracket (unsound): {unsound}; tau_grad free of NaN: {nanfree}")


def s3_timing():
    import time
    N, Gam = 8, 2.0
    pi = rng.dirichlet(np.ones(N) * 2)
    f = rng.uniform(-1, 1, N)
    phi = rng.uniform(-1, 1, (N, 1))
    l, u = pi, Gam * pi
    g = u - l
    G = g.sum()
    b = l @ np.column_stack([np.ones(N), phi, f])
    box = ci.Box(pi @ phi, 0.03)
    for n in (2000, 5000, 20000):
        x = rng.choice(N, size=n, p=g / G)
        t0 = time.perf_counter()
        ci.s3_interval(b, G, f[x], phi[x], box, 0.05, "net")
        t1 = time.perf_counter()
        P = ci.Problem(f[x], phi[x], Lw=0.0, Gw=G, region=box.enlarged(0.1), wt=np.full(n, 1.0 / n), b=b)
        t2 = time.perf_counter()
        a = ci.solve_upper(ci.lump(P))[0]
        t3 = time.perf_counter()
        print(f"[lib2] s3_interval, {n:6d} draws from {N} states: {t1 - t0:6.1f} s;  one end after lump(): {t3 - t2:.3f} s"
              f"  (value {a:.6f})")


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    nonfinite()
    seq_three_states()
    additive_three_states()
    ellipsoid_quality()
    model_free_ellipsoid()
    s3_timing()
