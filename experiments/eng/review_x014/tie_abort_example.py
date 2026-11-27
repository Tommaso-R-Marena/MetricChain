"""Review of ENG-RES-0016 §6 ("no abort"): a reproducible abort of ``hetero_literal.run_2l`` with the constants of the
statement, a valid oracle and the good event intact.

It is the floating-point tie of K_REPORT's erratum (m10): with x_L = b exactly, a fibre average that lies on the level
grid, and the oracle that puts the truth at the top of its bracket, the bracket [W e^-b, W] has U = s_j and
L = s_j e^-b up to rounding, and the classification rule "U > s_j and L <= s_j e^-b" can hold for it.  In exact
arithmetic it cannot.  The instances are deterministic (a cone on the outer block, flat fibres, the sum of all slopes a
multiple of lambda); only the outer sample is random.  Nothing here contradicts the theorem; it contradicts reading
"no abort in 57,600 runs" as a property of the simulator rather than of the instances that were drawn.

    python experiments/eng/review_x014/tie_abort_example.py          # writes tie_abort_example.json  (a few seconds)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "twolevel"))
sys.path.insert(0, str(HERE))

import hetero_literal as hl  # noqa: E402
from review_sim import limit_memory  # noqa: E402
from metricchain_eng.twolevel import hetero as H  # noqa: E402
from metricchain_eng.twolevel.certified import tables  # noqa: E402

LID = math.log(20.0)
CASES = [  # (n_o, u_o, inner (slope, count), design)
    (6, 0.5, [(2.0, 3)], dict(lam=0.2, eta=1 / 3, etap=1.0, b=1.3, Lr=1, theta=0.1, bounded=False)),
    (6, 0.5, [(2.0, 3)], dict(lam=0.5, eta=0.25, etap=0.25, b=0.5, Lr=4, theta=0.25, bounded=True)),      # the division's set "BND"
    (8, 0.5, [(2.0, 4)], dict(lam=0.5, eta=0.25, etap=0.25, b=0.5, Lr=4, theta=0.25, bounded=True)),      # the division's first shape, "BND"
    (8, 0.5, [(2.0, 4)], dict(lam=1.0, eta=0.5, etap=1.0, b=1.0, Lr=4, theta=1.0, bounded=False)),        # the division's first shape, "EXT"
    (8, 2.0, [(0.5, 4)], dict(lam=1.0, eta=0.5, etap=1.0, b=1.0, Lr=4, theta=1.0, bounded=False)),
    (5, 1.0, [(1.0, 2), (2.0, 1)], dict(lam=1.0, eta=0.5, etap=1.0, b=1.0, Lr=4, theta=1.0, bounded=False)),
]


def main() -> int:
    limit_memory(2.0)
    out = []
    for n_o, u_o, inner, kw in CASES:
        B = H.make_block([(u_o, n_o)] + inner)
        j = [i for i, (u, _) in enumerate(B) if u == u_o][0]
        C = H.constants(B, H.HDesign(j=j, k=n_o, **kw), LID)
        us = np.array([u_o] * n_o + [u for u, k in inner for _ in range(k)])
        n = len(us)
        X = ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1)
        row = dict(n_o=n_o, u_o=u_o, inner=inner, design=kw, omega_over_lambda=C.omega / kw["lam"], K=C.K, J=C.J, instances=[])
        for name, psi in (("cone on the outer block, apex at the reference point, flat fibres", u_o * X[:, :n_o].sum(axis=1).astype(float)),
                          ("inverted cone on the outer block, flat fibres", -u_o * X[:, :n_o].sum(axis=1).astype(float)),
                          ("flat", np.zeros(2 ** n))):
            assert hl.check_class(psi, us) <= 1e-12
            for orc in ("top", "bottom"):
                aborted, runs, first = 0, 40, None
                for seed in range(runs):
                    r = hl.run_2l(psi, n_o, C, tables(n_o, u_o), orc, np.random.default_rng(seed))
                    if r["status"] != "closed":
                        aborted += 1
                        first = first or dict(seed=seed, status=r["status"], level=r["level"])
                row["instances"].append(dict(instance=name, oracle=orc, runs=runs, aborted=aborted, first=first))
        out.append(row)
        print(f"n_o={n_o} u_o={u_o} inner={inner} lam={kw['lam']} b={kw['b']}: Omega/lam = {row['omega_over_lambda']:.6g}; "
              + "; ".join(f"{x['instance'][:12]}/{x['oracle']}: {x['aborted']}/{x['runs']}" for x in row["instances"]))
    (HERE / "tie_abort_example.json").write_text(json.dumps(out, indent=1, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
