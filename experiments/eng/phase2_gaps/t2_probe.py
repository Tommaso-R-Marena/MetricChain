"""T2 (c): a small probe of the repaired partition-function checker (SB commit 0e934eb, run at a5cc106) around F1.

    <their python> experiments/eng/phase2_gaps/t2_probe.py <sb-worktree> > results/t2_probe_<commit>.jsonl

Not a campaign: a few dozen calls.  Every accepted interval is compared with the exact value of ln Z computed here in
60-digit decimal arithmetic (ln of a sum of exponentials of integers; independent of their code); an accepted interval
that does not contain it is printed with "UNSOUND".

Probes
 P1  the F1 instance (energies 677, 678; beta 1; no steps) at the boundaries of the range the repair enforces
     (float 15/16/17, 511/512/513; exact 15/16/1023/1024/1025) and a few settings nearby (64, 256, 990);
 P2  the same kind of instance with the two energies moved across the double-range edge (E0 in 600..760, E1 = E0 + 1,
     plus E1 = E0 + 40), float tier at exp_bits 16, 64, 512 and exact tier at 1024;
 P3  the root cause of F1 directly: FloatTables._ldexp_up / from_me_bounds on mantissas of about 1000 bits whose value
     is far above 1e-300, where the old code returned 1e-300 (an upper bound below the value).
"""
from __future__ import annotations

import json
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 60
SB = Path(sys.argv[1])
sys.path.insert(0, str(SB / "src"))
import numpy as np  # noqa: E402
from metricchain_sb import mincert, zcert  # noqa: E402
from metricchain_sb.model import PairModel  # noqa: E402
from metricchain_sb.zcheck import check_partition_certificate  # noqa: E402
from metricchain_sb.itables import FloatTables  # noqa: E402


def instance(e0: int, e1: int):
    """Two configurations of energies e0 (x0 = 0) and e1 (x0 = 1): unary [[0, e1 - e0 + ...]] as in F1's construction."""
    m = PairModel(unary=[np.array([0, e1]), np.array([0])], pair={(0, 1): np.array([[e0], [0]])}, scale_bits=0)
    sha = mincert.model_sha256(m)
    text = ('{"format":"structbio-zcert/1","model_sha256":"%s","beta":"1/1","domains":[[0,1],[0]],"keep":null,"claim":{},'
            '"root":{"steps":[],"order":[1,0]},"meta":"{}"}' % sha)
    assert m.energy_int((0, 0)) == e0 and m.energy_int((1, 0)) == e1
    return m, zcert.loads(text, model=m)


def ln_z(e0: int, e1: int) -> Decimal:
    return ((-Decimal(e0)).exp() + (-Decimal(e1)).exp()).ln()


def frac_to_dec(q: Fraction) -> Decimal:
    return Decimal(q.numerator) / Decimal(q.denominator)


def call(cert, truth: Decimal, tier: str, bits: int) -> dict:
    try:
        r = check_partition_certificate(cert, arithmetic=tier, exp_bits=bits)
    except Exception as exc:  # noqa: BLE001
        return dict(tier=tier, exp_bits=bits, raised=f"{type(exc).__name__}: {str(exc)[:80]}")
    out = dict(tier=tier, exp_bits=bits, accepted=bool(r.accepted), reason=r.reason[:100])
    if r.accepted:
        lo, hi = r.ln_z_lo, r.ln_z_hi
        # exact comparison: Fraction(Decimal) is exact, the Decimal truth has 60 digits (error ~1e-57, far below widths)
        tq = Fraction(truth)
        out.update(lo=float(lo), hi=float(hi), contains_truth=bool(lo <= tq <= hi), width=float(hi - lo))
        if not out["contains_truth"]:
            out["UNSOUND"] = True
            out["miss_nats"] = float(min(abs(lo - tq), abs(hi - tq)))
    return out


def main() -> int:
    rows = []
    m, cert = instance(677, 678)
    t = ln_z(677, 678)
    for tier, bits in [("float", b) for b in (15, 16, 17, 64, 256, 511, 512, 513, 990)] + \
                      [("exact", b) for b in (15, 16, 64, 990, 1023, 1024, 1025)]:
        rows.append(dict(probe="P1", e0=677, e1=678, truth=str(t)[:25], **call(cert, t, tier, bits)))
    for e0 in (600, 650, 690, 700, 708, 709, 710, 720, 745, 746, 760):
        for e1 in (e0 + 1, e0 + 40):
            m, cert = instance(e0, e1)
            t = ln_z(e0, e1)
            for tier, bits in (("float", 16), ("float", 64), ("float", 512), ("exact", 1024)):
                rows.append(dict(probe="P2", e0=e0, e1=e1, truth=str(t)[:25], **call(cert, t, tier, bits)))
    # P3: the conversion itself.  value = m * 2**e with m of ~1000 bits and e = -(mbits + 990): the value is about
    # 2**-990 > 1e-300 (= 2**-996.6), while e < -2000 as soon as mbits > 1010 -- the case where the old code returned 1e-300
    ft = FloatTables()
    for mbits in (900, 1000, 1011, 1016, 1020):
        mant = (1 << mbits) - 12345
        e = -(mbits + 990)
        val = Fraction(mant) * Fraction(2) ** e
        try:
            up = FloatTables._ldexp_up(FloatTables._up(mant), e)
            dn = FloatTables._ldexp_down(FloatTables._down(mant), e)
            rows.append(dict(probe="P3", mantissa_bits=mbits, exponent=e, value=float(val), ldexp_up=up, ldexp_down=dn,
                             up_is_upper_bound=bool(Fraction(up) >= val), down_is_lower_bound=bool(Fraction(dn) <= val)))
        except Exception as exc:  # noqa: BLE001
            rows.append(dict(probe="P3", mantissa_bits=mbits, exponent=e, raised=f"{type(exc).__name__}: {str(exc)[:80]}"))
        try:
            tab = ft.from_me_bounds((0,), [(mant, e)], [(mant, e)], (1,))
            rows.append(dict(probe="P3-table", mantissa_bits=mbits, shift=tab.shift if hasattr(tab, "shift") else None,
                             lo=float(tab.lo[0]), hi=float(tab.hi[0])))
        except Exception as exc:  # noqa: BLE001
            rows.append(dict(probe="P3-table", mantissa_bits=mbits, raised=f"{type(exc).__name__}: {str(exc)[:80]}"))
    for r in rows:
        print(json.dumps(r), flush=True)
    acc = [r for r in rows if r.get("accepted")]
    print(json.dumps(dict(summary=True, calls=sum(1 for r in rows if r["probe"] in ("P1", "P2")), accepted=len(acc),
                          unsound=sum(1 for r in acc if r.get("UNSOUND")),
                          p3_bad=sum(1 for r in rows if r["probe"] == "P3" and not (r.get("up_is_upper_bound") and r.get("down_is_lower_bound"))))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
