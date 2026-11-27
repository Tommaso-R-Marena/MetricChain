"""Review of ENG-RES-0016 / X-011f: what ``nested_literal.three_level_run`` reports as "the theorem's count".

The division's function returns, for a middle run, the queries it ACTUALLY made (its base enumerations shared between equal
sample points); the top level multiplies that by its own unshared calls and calls the result the theorem's accounting.
Here the same instances are run twice from the same generator state: as the division does, and with every middle run
charged its own theorem's count (``attack_nested.three_level_run_strict``).  Both are far below the nested bound; the
point is only which number the label describes.

    python experiments/eng/review_x014/nested_count_comparison.py          # writes nested_count_comparison.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "eng" / "twolevel"))
sys.path.insert(0, str(HERE))

import attack_nested as an  # noqa: E402
import nested_literal as nl  # noqa: E402
import review_sim as rs  # noqa: E402


def main() -> int:
    rs.limit_memory(1.5)
    out = []
    for sizes, slopes, b_top in (((4, 4, 4), (3.0, 0.2, 1.0), 2.5), ((3, 5, 3), (2.0, 1.0, 0.1), 2.5), ((2, 6, 3), (1.5, 0.4, 2.2), 2.5)):
        S = nl.setup(sizes, slopes, b_top=b_top)
        us = np.array([slopes[0]] * sizes[0] + [slopes[1]] * sizes[1] + [slopes[2]] * sizes[2])
        rng = np.random.default_rng(5)
        a, b = [], []
        for i in range(4):
            psi = rs.instance(rs.INSTANCE_KINDS[(3 * i) % len(rs.INSTANCE_KINDS)], us, sizes[0], rng)
            a.append(nl.three_level_run(psi, sizes, S, np.random.default_rng(100 + i))["lq_thm"])
            b.append(an.three_level_run_strict(psi, sizes, S, np.random.default_rng(100 + i))["lq_thm"])
        row = dict(sizes=list(sizes), slopes=list(slopes), ln_count_as_the_division_reports_it=[round(x, 2) for x in a],
                   ln_count_with_middle_runs_charged_their_own_count=[round(x, 2) for x in b], ln_nested_bound=round(S["lCmax"], 2))
        out.append(row)
        print(row, flush=True)
    (HERE / "nested_count_comparison.json").write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
