"""R28 — a fact I quote from the literature (Kasperski & Zielinski's survey, passage read): under interval data the
optimum of the MIDPOINT scenario has at most twice the optimal maximum regret, hence "detects" a necessarily optimal
solution whenever one exists.  For SCI-REV-0026 §4 this means: testing the minimiser x* of the nominal table is
enough — if x* fails the criterion, NO configuration is necessarily optimal.

Check on random pair models (integers; criterion (N) for every configuration — the criterion itself was checked
against the enumeration of all vertex scenarios in no_check.py):
   exists q necessarily optimal  ==>  every minimiser of the nominal table is necessarily optimal.
Also the 2-approximation itself: max regret of a nominal minimiser <= 2 x the smallest max regret.
Control: the same implication with "nominal minimiser" replaced by "minimiser of the table with every entry at its
upper bound + a random integer tilt" must fail in some models.
"""
import r28_common as rc
rc.cap()
import itertools
import time
import numpy as np

t0 = time.time()
print("R28 no_midpoint.py  start", rc.utc())
rng = np.random.default_rng(2808)


def build(ks, edges):
    ent = [("u", i, a) for i in range(len(ks)) for a in range(ks[i])]
    ent += [("p", e, a, c) for e in range(len(edges)) for a in range(ks[edges[e][0]]) for c in range(ks[edges[e][1]])]
    col = {e: j for j, e in enumerate(ent)}
    cf = list(itertools.product(*[range(k) for k in ks]))
    inc = np.zeros((len(cf), len(ent)), dtype=np.int64)
    for r, x in enumerate(cf):
        for i in range(len(ks)):
            inc[r, col[("u", i, x[i])]] = 1
        for e, (i, j) in enumerate(edges):
            inc[r, col[("p", e, x[i], x[j])]] = 1
    return inc


n_models = n_exist = viol = viol2 = ctrl_fail = 0
for t in range(3000):
    n = int(rng.integers(2, 5))
    ks = [int(rng.integers(2, 4)) for _ in range(n)]
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.8]
    inc = build(ks, edges)
    m = inc.shape[1]
    cen = rng.integers(-12, 13, size=m)
    rad = rng.integers(0, int(rng.integers(1, 4)), size=m)
    en = inc @ cen
    # maximal regret of every configuration: attained at its own worst scenario (own entries up, others down)
    regret = np.empty(len(en), dtype=np.int64)
    for q in range(len(en)):
        tab = cen + np.where(inc[q].astype(bool), 1, -1) * rad
        e2 = inc @ tab
        regret[q] = e2[q] - e2.min()
    nec = regret == 0
    nominal_min = np.flatnonzero(en == en.min())
    n_models += 1
    if nec.any():
        n_exist += 1
        if not nec[nominal_min].all():
            viol += 1
    if not (regret[nominal_min] <= 2 * regret.min()).all():
        viol2 += 1
    # control: a different candidate
    other = inc @ (cen + rad + rng.integers(-6, 7, size=m))
    cand = int(np.argmin(other))
    if nec.any() and not nec[cand]:
        ctrl_fail += 1
print(f"{n_models} random pair models (2-4 sites, 2-3 states, random graphs); a necessarily optimal configuration exists in {n_exist}")
print(f"  'exists necessarily optimal' but some nominal minimiser is not: {viol} (must be 0)")
print(f"  max regret of a nominal minimiser above twice the smallest max regret: {viol2} (must be 0)")
print(f"  control (another candidate): the implication fails in {ctrl_fail} models (must be > 0)")
rc.finish(t0)
