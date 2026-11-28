"""Step 4 of the review: does src/metricchain_eng/certinf implement the statements soundly?

Written only after the mathematical review (ref.py and the check_*.py scripts do not import the library).
Here the library IS imported, and compared with the independent reference in ref.py.

Run:  python check_library.py
"""
from __future__ import annotations

import math
import sys
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from metricchain_eng import certinf as ci  # noqa: E402

import ref  # noqa: E402

rng = np.random.default_rng(424242)
warnings.simplefilter("ignore")          # library warnings carry local paths; the cases that matter are caught explicitly below


# ------------------------------------------------------------------ exact side
def check_tau_root():
    worst = 0.0
    for _ in range(2000):
        N = int(rng.integers(1, 9))
        m = int(rng.integers(0, 3))
        u = rng.uniform(0.0, 1.0, N) * (rng.random(N) < 0.9)
        kind = rng.integers(0, 4)
        l = u * rng.uniform(0, 1, N) if kind == 0 else (np.zeros(N) if kind == 1 else (u.copy() if kind == 2 else u * (rng.random(N) < 0.5)))
        f = rng.choice([-1.0, 0.0, 0.5, 1.0], N) if rng.random() < 0.5 else rng.uniform(-1, 1, N)    # ties
        phi = rng.uniform(-1, 1, (N, m))
        y, half = rng.uniform(-0.3, 0.3, m), rng.uniform(0, 0.2, m)
        box = ci.Box(y, half)
        eta = rng.normal(size=m) * rng.choice([0.0, 1.0, 10.0])
        if u.sum() == 0:
            continue
        P = ci.box_problem(l, u, f, phi, box)
        a = ci.tau_root(P, eta)
        b = ref.tau_star(eta, l, u, phi, f, lambda e: ref.h_box(e, y - half, y + half))
        if math.isfinite(a) or math.isfinite(b):
            worst = max(worst, abs(a - b))
    print(f"[lib] tau_root vs independent exact root (2000 random problems incl. l=0, l=u, ties, zero weights):"
          f" max abs diff = {worst:.2e}")


def check_interval():
    worst = 0.0
    unsound = 0
    empty_mismatch = 0
    cases = 0
    for _ in range(400):
        N = int(rng.integers(3, 10))
        m = int(rng.integers(0, 3))
        u = rng.uniform(0.2, 1.0, N)
        kind = rng.integers(0, 4)
        l = u * rng.uniform(0.05, 0.9, N) if kind == 0 else (np.zeros(N) if kind == 1 else (u.copy() if kind == 2 else u * (rng.random(N) < 0.5)))
        f = rng.uniform(-1, 1, N)
        phi = rng.uniform(-1, 1, (N, m))
        w = rng.uniform(l, u) if l.sum() > 0 else u
        y = (w @ phi) / w.sum() + (rng.uniform(-0.6, 0.6, m) if rng.random() < 0.3 else 0.0)
        half = rng.uniform(0, 0.1, m) * (rng.random() < 0.8)
        box = ci.Box(y, half)
        out = ci.interval(ci.box_problem(l, u, f, phi, box))
        A, c = ref.box_region(y - half, y + half) if m else (None, None)
        true = ref.primal_interval(l, u, phi, f, A, c)
        cases += 1
        if true is None:
            empty_mismatch += int(not out["empty"])
            continue
        if out["empty"]:
            empty_mismatch += 1
            continue
        if out["hi"] < true[1] - 1e-7 or out["lo"] > true[0] + 1e-7:
            unsound += 1
        worst = max(worst, abs(out["hi"] - true[1]), abs(out["lo"] - true[0]))
    print(f"[lib] interval() vs independent primal LP, {cases} instances (box regions; l=0, l=u, displaced regions):"
          f" unsound = {unsound}, emptiness verdict differs = {empty_mismatch}, max abs diff = {worst:.2e}")


def check_inconsistency_model_free():
    u = np.array([1.0, 1.0, 1.0])
    l = np.zeros(3)
    phi = np.array([[0.0], [0.5], [1.0]])
    f = np.array([0.0, 1.0, 0.0])
    far = ci.Box([2.5], 0.5)
    P = ci.box_problem(l, u, f, phi, far)
    val, eta = ci.find_inconsistency(P)
    out = ci.interval(P)
    print(f"[lib] model-free (l = 0), phi in [0,1], R = [2,3] (no ensemble compatible): find_inconsistency -> {val:.3g}"
          f" (never > 0);  interval() -> empty = {out['empty']} (hi = {out['hi']}, lo = {out['lo']})")
    # sampled version
    x = rng.integers(0, 3, 4000)
    s = ci.Sample(f[x], phi[x], np.zeros(4000), np.full(4000, 3.0))
    d = ci.Declared(0.0, 1.0, [0.0], [1.0], 3.0)
    b = ci.certify_inconsistent(s.part(slice(0, 2000)), s.part(slice(2000, None)), far, d, 0.05)
    print(f"      certify_inconsistent on 4000 draws: status = {b.status!r}  (the declared range [0,1] of phi alone excludes R:"
          " a deterministic certificate exists and is not used)")


# ------------------------------------------------------------------ sampled certificates
def two_point(Gam, a, v0, n, delta, reps, eps_tv=0.0, beta=1.0, sampler_a=None):
    """f in {v0, 1}; nominal reference pi(1) = a; draws from pi'(1) = sampler_a."""
    pa = a if sampler_a is None else sampler_a
    vplus = (Gam * a + (1 - a) * v0) / (Gam * a + 1 - a)
    d = ci.Declared(v0, 1.0, [], [], Gam, eps_tv=eps_tv, beta=beta)
    region = ci.Box()
    miss = cert = 0
    for _ in range(reps):
        x = rng.random(n) < pa
        f = np.where(x, 1.0, v0)
        s = ci.Sample(f, np.zeros((n, 0)), np.ones(n), np.full(n, Gam))
        b = ci.certify_upper(s.part(slice(0, 1)), s, region, d, delta)
        cert += b.status == "certified"
        miss += b.value < vplus - 1e-12
    return miss / reps, cert / reps, vplus


def check_certify_upper():
    print("[lib] certify_upper, m = 0, two states f in {v0, 1}, declared range [v0, 1], U_max = Gamma (exact), delta = 0.05")
    print("   Gamma     a      v0      n     V+        miss rate   certified rate")
    for Gam, a, v0, n, reps in ((10.0, 0.05, 0.0, 60, 20000), (10.0, 0.05, 0.0, 600, 10000), (1000.0, 0.002, 0.0, 1500, 5000),
                                (1000.0, 0.002, 0.0, 15000, 1000), (100.0, 0.0005, 0.9, 12800, 1000)):
        miss, cert, vplus = two_point(Gam, a, v0, n, 0.05, reps)
        print(f"   {Gam:7.0f}  {a:7.5f}  {v0:4.2f}  {n:6d}  {vplus:.5f}   {miss:.4f}      {cert:.3f}")
    print("   sampler different from the nominal reference (the up-weighted state under-sampled):")
    print("   case                                     miss rate   certified rate")
    Gam, a, n = 5.0, 0.1, 4000
    for label, kw in (("TV 0.02, declared eps_tv = 0 (wrong)", dict(sampler_a=a - 0.02)),
                      ("TV 0.02, declared eps_tv = 0.02", dict(sampler_a=a - 0.02, eps_tv=0.02)),
                      ("ratio 1/1.5, declared beta = 1 (wrong)", dict(sampler_a=a / 1.5)),
                      ("ratio 1/1.5, declared beta = 1.5", dict(sampler_a=a / 1.5, beta=1.5))):
        miss, cert, vplus = two_point(Gam, a, 0.0, n, 0.05, 1000, **kw)
        print(f"   {label:40s} {miss:.4f}      {cert:.3f}")

    print("[lib] certified_interval, 6 states, m = 1, n = 1000 (500 + 500), delta = 0.1: miss rate of either end")
    for Gam in (3.0, 30.0):
        N = 6
        pi = rng.dirichlet(np.ones(N) * 2)
        f = rng.uniform(-1, 1, N)
        phi = rng.uniform(-1, 1, (N, 1))
        r = rng.uniform(1, Gam, N)
        y = (pi * r) @ phi / (pi * r).sum()
        box = ci.Box(y, 0.03)
        A, c = ref.box_region(y - 0.03, y + 0.03)
        true = ref.primal_interval(pi, Gam * pi, phi, f, A, c)
        d = ci.Declared(-1.0, 1.0, [-1.0], [1.0], Gam)
        miss = 0
        widths = []
        reps = 1500
        for _ in range(reps):
            x = rng.choice(N, size=1000, p=pi)
            out = ci.certified_interval(ci.Sample(f[x], phi[x], np.ones(1000), np.full(1000, Gam)), box, d, 0.1)
            miss += (out["hi"] < true[1] - 1e-9) or (out["lo"] > true[0] + 1e-9)
            widths.append(out["hi"] - out["lo"])
        print(f"   Gamma = {Gam:4.0f}: true interval [{true[0]:.4f}, {true[1]:.4f}], miss rate = {miss / reps:.4f},"
              f" median certified width = {np.median(widths):.4f}")


def check_rigorous():
    N = 6
    pi = rng.dirichlet(np.ones(N) * 2)
    f = rng.uniform(-1, 1, N)
    phi = rng.uniform(-1, 1, (N, 1))
    y = pi @ phi
    for region, name in ((ci.Box(y, 0.05), "box"), (ci.Ellipsoid(y, [[0.0025]], 1.0), "ellipsoid"),
                         (ci.Ellipsoid(y, [[0.0025]], 1.0).enlarged(0.01), "ellipsoid + box")):
        x = rng.choice(N, size=600, p=pi)
        s = ci.Sample(f[x], phi[x], np.ones(600), np.full(600, 2.0))
        d = ci.Declared(-1.0, 1.0, [-1.0], [1.0], 2.0)
        a = ci.certify_upper(s.part(slice(0, 300)), s.part(slice(300, None)), region, d, 0.1)
        b = ci.certify_upper(s.part(slice(0, 300)), s.part(slice(300, None)), region, d, 0.1, rigorous=True)
        print(f"[lib] rigorous=True, region {name:15s}: plain {a.status} {a.value:.12f}, interval-arithmetic {b.status} {b.value:.12f}")


def check_inconsistent_false_alarm():
    N, Gam = 6, 4.0
    pi = rng.dirichlet(np.ones(N) * 2)
    f = rng.uniform(-1, 1, N)
    phi = rng.uniform(-1, 1, (N, 1))
    lo = ref.primal_extreme(pi, Gam * pi, phi, phi[:, 0], None, None, -1)
    hi = ref.primal_extreme(pi, Gam * pi, phi, phi[:, 0], None, None, +1)
    d = ci.Declared(-1.0, 1.0, [-1.0], [1.0], Gam)
    print(f"[lib] certify_inconsistent, 6 states, Gamma = 4, reachable range of E phi = [{lo:.4f}, {hi:.4f}], n = 400+400, delta = 0.05")
    for label, centre in (("region tangent to the reachable set from outside (consistent)", hi + 0.02),
                          ("region displaced by 0.02 (inconsistent)", hi + 0.04),
                          ("region displaced by 0.2 (inconsistent)", hi + 0.22)):
        box = ci.Box([centre], 0.02)
        fires = 0
        reps = 1500
        for _ in range(reps):
            x = rng.choice(N, size=800, p=pi)
            s = ci.Sample(f[x], phi[x], np.ones(800), np.full(800, Gam))
            fires += ci.certify_inconsistent(s.part(slice(0, 400)), s.part(slice(400, None)), box, d, 0.05).status == "certified"
        print(f"   {label:62s}: fires in {fires / reps:.4f}")


def check_gap():
    N, Gam = 8, 5.0
    pi = rng.dirichlet(np.ones(N) * 2)
    f = rng.uniform(-1, 1, N)
    phi = rng.uniform(-1, 1, (N, 1))
    l, u = pi, Gam * pi
    g = u - l
    G = g.sum()
    v = np.column_stack([np.ones(N), phi, f])
    b = l @ v
    r = rng.uniform(1, Gam, N)
    y = (pi * r) @ phi / (pi * r).sum()
    box = ci.Box(y, 0.03)
    A, c = ref.box_region(y - 0.03, y + 0.03)
    true = ref.primal_interval(l, u, phi, f, A, c)
    d = ci.Declared(-1.0, 1.0, [-1.0], [1.0], Gam)
    miss = 0
    vals = []
    reps = 1500
    for _ in range(reps):
        x = rng.choice(N, size=1000, p=g / G)
        out = ci.certify_upper_gap(b, G, f[x[:500]], phi[x[:500]], f[x[500:]], phi[x[500:]], box, d, 0.05)
        miss += out.value < true[1] - 1e-9
        vals.append(out.value)
    print(f"[lib] certify_upper_gap, 8 states, m = 1, n = 500+500, delta = 0.05: V+ = {true[1]:.4f}, miss rate = {miss / reps:.4f},"
          f" median bound = {np.median(vals):.4f}")
    x = rng.choice(N, size=1000, p=g / G)
    for label, dd in (("iid=False", ci.Declared(-1.0, 1.0, [-1.0], [1.0], Gam, iid=False)),
                      ("eps_tv=0.2", ci.Declared(-1.0, 1.0, [-1.0], [1.0], Gam, eps_tv=0.2)),
                      ("beta=3", ci.Declared(-1.0, 1.0, [-1.0], [1.0], Gam, beta=3.0)),
                      ("f_err=0.1, phi_err=0.1", ci.Declared(-1.0, 1.0, [-1.0], [1.0], Gam, f_err=0.1, phi_err=0.1)),
                      ("declared f range [-0.2, 0.2] (violated by the draws)", ci.Declared(-0.2, 0.2, [-1.0], [1.0], Gam))):
        ref_b = ci.certify_upper_gap(b, G, f[x[:500]], phi[x[:500]], f[x[500:]], phi[x[500:]], box, d, 0.05)
        out = ci.certify_upper_gap(b, G, f[x[:500]], phi[x[:500]], f[x[500:]], phi[x[500:]], box, dd, 0.05)
        print(f"   Declared({label}): status = {out.status!r}, value = {out.value:.6f}   (plain declaration: {ref_b.value:.6f})")
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            out = ci.certify_upper_gap(b, 0.0, f[x[:500]], phi[x[:500]], f[x[500:]], phi[x[500:]], box, d, 0.05)
        kinds = sorted({f"{w.category.__name__}: {w.message}" for w in caught})
        print(f"   G = 0: status = {out.status!r}, value = {out.value}; warnings emitted: {kinds}")
    except Exception as exc:  # noqa: BLE001
        print(f"   G = 0: raises {type(exc).__name__}: {exc}")


def check_s3():
    N, Gam = 8, 2.0
    pi = rng.dirichlet(np.ones(N) * 2)
    f = rng.uniform(-1, 1, N)
    phi = rng.uniform(-1, 1, (N, 1))
    l, u = pi, Gam * pi
    g = u - l
    G = g.sum()
    v = np.column_stack([np.ones(N), phi, f])
    b = l @ v
    r = rng.uniform(1, Gam, N)
    y = (pi * r) @ phi / (pi * r).sum()
    box = ci.Box(y, 0.03)
    A, c = ref.box_region(y - 0.03, y + 0.03)
    true = ref.primal_interval(l, u, phi, f, A, c)
    for bound in ("net", "rademacher"):
        miss = 0
        widths = []
        for _ in range(40):
            x = rng.choice(N, size=5000, p=g / G)
            out = ci.s3_interval(b, G, f[x], phi[x], box, 0.05, bound)
            miss += (out["status"] != "certified") or out["hi"] < true[1] - 1e-9 or out["lo"] > true[0] + 1e-9
            widths.append(out["hi"] - out["lo"])
        print(f"[lib] s3_interval ({bound}), n = 5000, Gamma = 2: true width {true[1] - true[0]:.4f}, median S3 width"
              f" {np.median(widths):.4f}, kappa = {out['kappa']:.4f}, misses = {miss}/40")
    far = ci.Box(y + 1.5, 0.03)
    x = rng.choice(N, size=5000, p=g / G)
    out = ci.s3_interval(b, G, f[x], phi[x], far, 0.05, "rademacher")
    print(f"   region displaced by 1.5 (no ensemble compatible): status = {out['status']!r}")
    out = ci.s3_interval(np.zeros(3), G, f[x], phi[x], box, 0.05)
    print(f"   Z_l = 0: status = {out['status']!r}, kappa = {out['kappa']}")
    try:
        out = ci.s3_interval(b, 0.0, np.zeros(0), np.zeros((0, 1)), box, 0.05)
        print(f"   G = 0 (no draws possible): status = {out['status']!r}")
    except Exception as exc:  # noqa: BLE001
        print(f"   G = 0 (no draws possible): raises {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    check_tau_root()
    check_interval()
    check_inconsistency_model_free()
    check_rigorous()
    check_gap()
    check_s3()
    check_inconsistent_false_alarm()
    check_certify_upper()
