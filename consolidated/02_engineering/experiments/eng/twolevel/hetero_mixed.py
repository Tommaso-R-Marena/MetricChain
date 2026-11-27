"""X-014d: outer blocks of one site type against mixed outer blocks with the sorted-slope tail bound (Lemma N14 of
the theory division's workstream N), in the same certified recursion.

Per mixture of two site types (n = 4000) and for two and three levels: the certified bound per site of
  homogeneous   the uniform cube with the larger slope (inclusion),
  aligned       outer blocks of one type, exact tables of the uniform cube,
  mixed         outer blocks with the same fraction of every type, sorted-slope tables,
  both          the union of the two families.

    python experiments/eng/twolevel/hetero_mixed.py        # writes results/x014_mixed.json
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from metricchain_eng.twolevel import certified as cert  # noqa: E402
from metricchain_eng.twolevel import hetero as H  # noqa: E402

LID = math.log(20.0)
PHIS = (0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10)
MIXTURES = [(2.0, 0.5, 0.1), (2.0, 0.5, 0.25), (2.0, 0.5, 0.5), (2.0, 0.5, 0.75), (2.0, 0.5, 0.9),
            (1.0, 0.5, 0.25), (1.0, 0.5, 0.75), (4.0, 1.0, 0.25), (4.0, 1.0, 0.75)]


def best(B, blocks: str, depth: int):
    S = H.HSearch(PHIS, blocks=blocks)
    b = None
    for j, k, c in H.top_choices(B, PHIS, blocks=blocks):
        hb = S.top(B, H.top_design(j, k, comp=c), LID, depth, cutoff=b.lCmax if b else math.inf)
        if hb is not None:
            b = hb
    return b


def main() -> int:
    n = 4000
    out = []
    for uH, uL, frac in MIXTURES:
        nH = int(round(frac * n))
        B = H.make_block([(uH, nH), (uL, n - nH)])
        row = dict(uH=uH, uL=uL, frac=frac, n=n, levels=[])
        for depth in (1, 2):
            t0 = time.time()
            S = cert.Search(uH, "wide")
            hom = min(lb.lCmax for lb in (S.top(n, cert.top_design(phi), LID, depth) for phi in PHIS) if lb is not None) / n
            vals = {bl: best(B, bl, depth) for bl in ("aligned", "mixed", "both")}
            both = vals["both"]
            row["levels"].append(dict(levels=depth + 1, homogeneous=hom, aligned=vals["aligned"].lCmax / n, mixed=vals["mixed"].lCmax / n,
                                      both=both.lCmax / n, both_top_is_mixed=both.design.comp is not None, seconds=time.time() - t0))
        out.append(row)
        print(f"u=({uH:g},{uL:g}) heavy {frac:g}: " + "; ".join(
            f"{x['levels']} levels: hom {x['homogeneous']:.4f} aligned {x['aligned']:.4f} mixed {x['mixed']:.4f} both {x['both']:.4f}" for x in row["levels"]), flush=True)
        (ROOT / "experiments" / "eng" / "twolevel" / "results" / "x014_mixed.json").write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
