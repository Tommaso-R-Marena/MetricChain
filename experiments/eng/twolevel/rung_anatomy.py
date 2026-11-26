"""X-011d: where the cost of a three-level run goes, rung by rung, for one design chosen at the flat fibre and one
chosen by certified cost — at the flat instance and with cone fibres (flat outer landscape, base brackets' own
answers; mean-run model).  Writes results/x011_rungs.json.

    python experiments/eng/twolevel/rung_anatomy.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import nested_bench as nb  # noqa: E402
import portfolio  # noqa: E402
from metricchain_eng.twolevel import certified as cert  # noqa: E402
from metricchain_eng.twolevel.meanrun import Instance, Law  # noqa: E402
from metricchain_eng.twolevel.tables import cube_constants  # noqa: E402


def anatomy(tree: cert.LevelBound, u: float, n: int, slope: float) -> dict:
    """The run of ``tree`` on a flat outer landscape with fibres that are cones of slope ``slope`` u (0: flat)."""
    na = n * cube_constants(u).a
    P, outer, C, ev, pos, c_in, ok = nb.level_setup(tree, u, nb.LID, slope, "k0")
    inst = Instance(Law(np.array([0.0]), np.array([0.0])), psi0=0.0, t0=u * P.n_i + c_in)
    R = ev.run(inst, "bottom", positions=pos, record=True)
    rungs = []
    for l in range(1, P.L + 1):
        s = tree.servers[l - 1]
        c, a_, b_, _ = nb.server_on_cone(s, P.n_i, P.xs[l], C.l_inv_delta_p, u, slope, "k0")
        rungs.append(dict(l=l, x=P.xs[l], server=("2L+ " + s.design.name.split("(")[0]) if isinstance(s, cert.LevelBound) else str(s),
                          cost=c / na, certified_cost=float(tree.lC[l]) / na, used=(a_ + b_) / P.xs[l], alpha=a_, beta=b_,
                          calls=float(R.lcalls[l]) / na if np.isfinite(R.lcalls[l]) else None,
                          term=(float(R.lcalls[l]) + c) / na if np.isfinite(R.lcalls[l]) else None))
    return dict(slope=slope, cost=R.lcost / na, closed=bool(R.closed and not R.violations() and ok), rungs=rungs,
                outer_sample=float(np.max(R.lM)) / na if R.lM is not None else None)


def main() -> int:
    u, n = 1.0, 4000
    out = dict(u=u, n=n, designs=[])
    for name, tree, phi in (("servers chosen at the flat fibre", portfolio.flat_tuned_tree(u, n, 0.40), 0.40),
                            ("servers chosen by certified cost", portfolio.certified_tree(u, n, 0.35, 2), 0.35)):
        na = n * cube_constants(u).a
        d = dict(name=name, phi=phi, certified=tree.lCmax / na, runs=[anatomy(tree, u, n, s) for s in (0.0, 1.0)])
        out["designs"].append(d)
        print(name, "phi", phi, "certified %.4f" % d["certified"], "flat %.4f" % d["runs"][0]["cost"], "cone fibres %.4f" % d["runs"][1]["cost"])
    (ROOT / "experiments" / "eng" / "twolevel" / "results" / "x011_rungs.json").write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
