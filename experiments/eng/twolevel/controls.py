"""Controls for the engineering implementation of Algorithm 2L+ (X-005).

The implementation in ``src/metricchain_eng/twolevel`` was written from the text of the theory
branch (K_REPORT §2).  Here it is compared with numbers the theory division published:

  radial   every deterministic and random-walk row of ``out_radial_trajectory.txt`` of workstream K
           (outer loop in expectation on 17 radial landscapes, u in {1/2, 1, 2},
           n_o in {1000, 4000, 16000}; variants with and without the Harper term)
  flat     ``out_flat_cost_bounded.txt`` (number of evaluations at the flat instance)

The stored outputs are read from a checkout of the theory branch given by --theory (they are
theory-owned files and are not copied into this branch).

    python experiments/eng/twolevel/controls.py --theory ../MetricChain-theory-63efc69 [--only radial|flat]
"""
from __future__ import annotations

import argparse
import math
import re
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel.alg2l import Params, constants, inner_costs  # noqa: E402
from metricchain_eng.twolevel.meanrun import Instance, Law, mean_run, radial_law  # noqa: E402
from metricchain_eng.twolevel.ckernel import Evaluator  # noqa: E402
from metricchain_eng.twolevel.tables import TIE, CubeTables, cube_constants  # noqa: E402


# ------------------------------------------------------------------------------------------------
# the 17 radial landscapes of K_REPORT 6.6, from their description (the three random walks use the
# generator call sequence of the workstream's script: default_rng(11), u in (0.5, 1, 2), n_o in
# (1000, 4000, 16000), three draws of uniform(-u, u, n_o) per case)
# ------------------------------------------------------------------------------------------------
def k_profiles(n_o: int, u: float, rng, tables: CubeTables) -> dict[str, np.ndarray]:
    c = cube_constants(u)
    d = np.arange(n_o + 1, dtype=float)
    out = {"flat": np.zeros(n_o + 1), "cone": u * d, "cone slope u/2": 0.5 * u * d, "anti-cone": -u * d}
    for frac in (0.5, 1.0, 1.5):
        R = int(frac * c.p_u * n_o)
        out[f"flattened bottom R={frac:.1f} p_u n_o"] = u * np.maximum(d, R)
        out[f"mesa R={frac:.1f} p_u n_o"] = u * np.minimum(d, R)
    for frac in (0.8, 1.0, 1.2):
        R = int(frac * c.Lambda1 / u * n_o)
        out[f"dip R={frac:.1f} Lambda1 n_o/u"] = -u * np.maximum(R - d, 0)
    F = np.zeros(n_o + 1)
    F[1:] = np.cumsum(np.minimum(u, np.diff(tables.lball)))            # "staircase": W ~ 1/|B(d)| where the slope allows
    out["staircase W ~ 1/|B(d)|"] = F
    for i in range(3):
        out[f"random walk {i}"] = np.concatenate([[0.0], np.cumsum(rng.uniform(-u, u, size=n_o))])
    out["2-periodic"] = (u / 2) * (-1.0) ** d
    return out


ROW = re.compile(r"^(?P<name>.+?)\s*\|\s*(?P<variant>harper|plain)\s+(?P<tz>[01])\s*\|\s*(?P<kind>populated|unpopulated)\s+(?P<r>-?\d+)\s*\|"
                 r"\s*(?P<lm>[-\d.]+)\s*\|\s*(?P<width>[-\d.]+)\s*\((?P<bound>[-\d.]+)\)\s*\|\s*(?P<npop>\d+)/(?P<nneg>\d+)")
HEAD = re.compile(r"^=== u = (?P<u>[\d.]+), n_o = (?P<n>\d+):")


def control_radial(theory: Path) -> bool:
    text = (theory / "experiments/workstreams/K/out_radial_trajectory.txt").read_text().splitlines()
    want: dict = {}
    cur = None
    for line in text:
        m = HEAD.match(line)
        if m:
            cur = (float(m["u"]), int(m["n"]))
            continue
        m = ROW.match(line)
        if m and cur and not m["name"].startswith("additive"):
            want[(cur, m["name"].strip(), m["variant"])] = (m["kind"], int(m["r"]), float(m["lm"]), float(m["width"]),
                                                            int(m["npop"]), int(m["nneg"]))
    rng = np.random.default_rng(11)
    n_rows = n_bad = 0
    tie_rows = []
    t0 = time.time()
    for u in (0.5, 1.0, 2.0):
        c = cube_constants(u)
        for n_o in (1000, 4000, 16000):
            tabs = CubeTables(n_o, u)
            P = Params(n=n_o, n_o=n_o, u=u, lam=0.5, eta=0.25, etap=0.1, theta=0.1, nu1=2 * math.exp(u) * n_o / 0.1,
                       b=0.5, delta=0.05, xs=(0.0,) * 7)
            C = constants(P, tabs)
            evs = {(variant, tie): Evaluator(P, tabs, harper=(variant == "harper"), enforce_abort=(variant == "harper"),
                                             count_grid=(0.5, 2.0, 8.0, 32.0), tie=tie)       # the published "plain" rows have no abort rule
                   for variant in ("harper", "plain") for tie in (0.0, TIE)}
            for name, F in k_profiles(n_o, u, rng, tabs).items():
                inst = Instance(radial_law(F, tabs), psi0=float(F[n_o // 2]))
                for variant in ("harper", "plain"):
                    key = ((u, n_o), name, variant)
                    if key not in want:
                        continue
                    w = want[key]
                    got = {}
                    for tie in (0.0, TIE):
                        R = evs[(variant, tie)].run(inst, "bottom")
                        got[tie] = (R.status.replace("closed-", ""), R.r_close, round(R.lM_last / (n_o * c.a), 4), round(R.width, 3),
                                    R.npop, R.nneg)
                        if variant == "harper" and R.violations():
                            print(f"  CLAIM VIOLATED {key} (tie = {tie}): {R.violations()}")
                            n_bad += 1

                    def same(g):
                        return (g[0] == w[0] and g[1] == w[1] and abs(g[2] - w[2]) <= 1.5e-4 and abs(g[3] - w[3]) <= 1.5e-3
                                and g[4] == w[4] and g[5] == w[5])
                    n_rows += 1
                    if not same(got[0.0]):                       # plain floating-point comparisons, as in the published script
                        n_bad += 1
                        print(f"  DIFFERENT {key}: published {w}, here {got[0.0]}")
                    if not same(got[TIE]):
                        tie_rows.append((key, w, got[TIE]))
                    if n_o == 1000 and variant == "harper":      # the Python reference gives the same record as the kernel
                        Rp = mean_run(P, tabs, inst, "bottom", C=C, count_grid=(0.5, 2.0, 8.0, 32.0))
                        Rc = evs[("harper", TIE)].run(inst, "bottom")
                        if (Rp.status, Rp.r_close, Rp.npop, Rp.nneg) != (Rc.status, Rc.r_close, Rc.npop, Rc.nneg) or abs(Rp.lM_last - Rc.lM_last) > 1e-9:
                            n_bad += 1
                            print(f"  KERNEL != REFERENCE {key}")
    print(f"radial control: {n_rows} published rows compared; with plain floating-point comparisons {n_bad} differ; "
          f"with the tie rule {len(tie_rows)} differ:   ({time.time() - t0:.0f} s)")
    for key, w, g in tie_rows:
        print(f"  tie row {key}: published {w}, with ties treated exactly {g}")
    return n_bad == 0 and n_rows > 0 and len(tie_rows) <= 4


FLAT_HEAD = re.compile(r"^=== u = (?P<u>[\d.]+):")
FLAT_ROW = re.compile(r"^\s*(?P<n>\d+)\s*\|\s*(?P<c>[\d.]+)\s*\|\s*[\d.]+\s*\|\s*(?P<phi>[\d.]+)\s*\|\s*(?P<width>[\d.]+)\s*\|.*\|\s*r = (?P<r>-?\d+) \((?P<rdag>-?\d+)\), (?P<npop>\d+)/(?P<nneg>\d+), (?P<lm>[\d.]+)\s*$")


def k_flat_params(n: int, u: float, phi: float) -> Params:
    c = cube_constants(u)
    n_o = max(1, min(n - 1, int(math.floor(phi * n))))
    n_i = n - n_o
    b = 0.5
    rates = [c.eps_star * 0.85 ** i for i in range(40)]
    xs = [2 * u * n_i] + [r * n_i for r in rates if b < r * n_i < 2 * u * n_i] + [b]
    return Params(n=n, n_o=n_o, u=u, lam=0.2, eta=0.05, etap=0.05, theta=0.05, nu1=2 * math.exp(u) * n_o / 0.05, b=b,
                  delta=0.05, xs=tuple(xs))


def control_flat(theory: Path, n_max: int) -> bool:
    text = (theory / "experiments/workstreams/K/out_flat_cost_bounded.txt").read_text().splitlines()
    u = None
    ok = True
    n_rows = 0
    t0 = time.time()
    print(f"{'u':>4} {'n':>6} {'phi':>5} | published ln(cost)/n | here: bottom  top | traj. (r, r_dag, pop/neg, lnM/n) published | here")
    for line in text:
        m = FLAT_HEAD.match(line)
        if m:
            u = float(m["u"])
            continue
        m = FLAT_ROW.match(line)
        if not m or u is None or int(m["n"]) > n_max:
            continue
        n, phi = int(m["n"]), float(m["phi"])
        P = k_flat_params(n, u, phi)
        tabs = CubeTables(P.n_o, u)
        C = constants(P, tabs)
        lC = inner_costs(P, C)
        inst = Instance(Law(np.array([0.0]), np.array([0.0])), psi0=0.0, t0=u * P.n_i)
        ev = Evaluator(P, tabs, lC=lC)
        Rb = ev.run(inst, "bottom")
        Rt = ev.run(inst, "top")
        pub = (int(m["r"]), int(m["rdag"]), int(m["npop"]), int(m["nneg"]), float(m["lm"]))
        here = (Rb.r_close, C.r_dag, Rb.npop, Rb.nneg, round(Rb.lM_last / n, 5))
        same_traj = pub[:4] == here[:4] and abs(pub[4] - here[4]) < 1.5e-5
        dc = Rb.lcost / n - float(m["c"])
        n_rows += 1
        flag = "" if same_traj else "   <-- trajectory differs"
        if not same_traj or abs(dc) > 2e-3 or Rb.violations() or Rt.violations():
            ok = False
        print(f"{u:4.1f} {n:6d} {phi:5.2f} | {float(m['c']):20.5f} | {Rb.lcost / n:8.5f} {Rt.lcost / n:8.5f} | {pub} | {here}{flag}"
              f"  viol: {Rb.violations() + Rt.violations()}")
    print(f"flat control: {n_rows} published rows compared, all within tolerance: {ok}   ({time.time() - t0:.0f} s)")
    return ok and n_rows > 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--theory", type=Path, required=True, help="checkout of the theory branch (read only)")
    ap.add_argument("--only", choices=("radial", "flat"))
    ap.add_argument("--flat-nmax", type=int, default=64000)
    args = ap.parse_args()
    ok = True
    if args.only in (None, "radial"):
        ok &= control_radial(args.theory)
    if args.only in (None, "flat"):
        ok &= control_flat(args.theory, args.flat_nmax)
    print("CONTROLS", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
