#!/usr/bin/env python3
"""R18: the inequalities behind "inside the range for every design used" (ENG-RES-0014 §1) and behind "its
classification shift c is the same" (§4), checked on EVERY cell of X-005 (jobs cost, claims, converge, converge2),
with the design rebuilt from the statement of ENG-RES-0008 §1 (my `x005_ladder`), not with their `design_params`.

Per cell: lo = n_i (u - Lambda_1), hi = n_i (2u - Lambda_1), x_0 = 2 u n_i, the ladder.
  R1  lo >= b                  ("top":    c = 0 at every feasible place)
  R2  x_0 - hi >= b            ("bottom": c = b at every feasible place, given R3)
  R3  x_1 >= b  (here: x_L = b)
  R4  x_1 <= lo and x_1 <= x_0 - hi   (then the windows of the rungs l >= 1 do not depend on the place: the union of §4
                                       changes the calls of the first inner procedure only)
and the exact shifts at the two ends of the range, from the closed rule.
The cell list (u, n, phi, n_o, n_i, L) is read from their stored results (data only).
usage: python3 -I -B r18_cells.py"""
import json, math, resource
from fractions import Fraction as Fr
from pathlib import Path
ENG = Path("/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/eng_ro_1cc4e1c")
RES = ENG / "experiments" / "eng" / "twolevel" / "results"


def x005_ladder(n, u, phi):
    n_o = max(1, min(n - 1, int(math.floor(phi * n))))
    n_i = n - n_o
    eps = math.log(math.cosh(u / 2))
    xs = [2 * u * n_i] + [eps * 0.85 ** i * n_i for i in range(40) if 0.5 < eps * 0.85 ** i * n_i < 2 * u * n_i] + [0.5]
    return n_o, n_i, xs


def shift(b, t0, x0, pos):
    A, B = [t0], [x0 - t0]
    for a, be in pos:
        A.append(min(A[-1], a)); B.append(min(B[-1], be))
    return max(min(b - a, be) for a, be in zip(A, B))


cells = {}
for job in ("cost", "claims", "converge", "converge2"):
    for line in (RES / f"x005_{job}.jsonl").read_text().splitlines():
        if line.strip():
            c = json.loads(line)
            assert c["design"] == dict(b=0.5, lam=0.2, eta=0.05, etap=0.05, theta=0.05, delta=0.05, ladder_ratio=0.85, ladder_len=40), c["design"]
            cells.setdefault((c["u"], c["n"], c["phi"]), []).append((job, c["n_o"], c["n_i"], c["constants"]["L"]))
b = 0.5
st = dict(cells=0, R1=0, R2=0, R3=0, R4=0, ladder_differs=0, shift_bad=0)
mins = dict(lo_minus_b=(1e99, None), x0hi_minus_b=(1e99, None), lo_minus_x1=(1e99, None), x0hi_minus_x1=(1e99, None))
for (u, n, phi), lst in sorted(cells.items()):
    n_o, n_i, xs = x005_ladder(n, u, phi)
    st["cells"] += 1
    st["ladder_differs"] += any((n_o, n_i, len(xs) - 1) != (a[1], a[2], a[3]) for a in lst)
    L1 = math.log(2 / (1 + math.exp(-u)))
    lo, hi, x0 = n_i * (u - L1), n_i * (2 * u - L1), 2 * u * n_i
    st["R1"] += lo >= b
    st["R2"] += x0 - hi >= b
    st["R3"] += (xs[1] >= b and xs[-1] == b)
    st["R4"] += (xs[1] <= lo and xs[1] <= x0 - hi) or len(xs) == 2
    for k, v in (("lo_minus_b", lo - b), ("x0hi_minus_b", x0 - hi - b), ("lo_minus_x1", lo - xs[1]), ("x0hi_minus_x1", x0 - hi - xs[1])):
        if v < mins[k][0]:
            mins[k] = (v, (u, n, phi, n_i))
    for t0 in (lo, hi, (lo + hi) / 2):
        cb = shift(b, t0, x0, [(0.0, x) for x in xs[1:]])
        ct = shift(b, t0, x0, [(x, 0.0) for x in xs[1:]])
        st["shift_bad"] += (abs(cb - b) > 1e-12 or abs(ct) > 1e-12)
print(f"cells (distinct (u, n, phi) over the four jobs): {st['cells']};  ladder of my reading differs from the stored (n_o, n_i, L): {st['ladder_differs']}")
print(f"R1 lo >= b: {st['R1']} of {st['cells']}   R2 x0 - hi >= b: {st['R2']}   R3 x_1 >= b and x_L = b: {st['R3']}   R4 x_1 <= min(lo, x0 - hi): {st['R4']}")
print(f"exact shift at t0 in {{lo, mid, hi}} different from b (bottom) or 0 (top): {st['shift_bad']} of {3 * st['cells']}")
for k, (v, at) in mins.items():
    print(f"  smallest {k}: {v:.4f} at (u, n, phi, n_i) = {at}")
print("smallest n_i over the cells:", min(a[2] for lst in cells.values() for a in lst))
print("peak RSS MB: %.1f" % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024))
