"""R28 — replication of the "necessary optimality" reduction of SCI-REV-0026 §4 and of its use in §0 point 2,
with my own code written from the statement (integers throughout; nothing imported from the script under
review).

Model: sites with finite state sets, an interaction graph, one-body entries U_i(a) and pair entries
P_ij(a, c) for the edges of the graph; a table b >= 0 of the same shape; scenario = any table within b,
entry by entry.  A configuration "uses" one one-body entry per site and one pair entry per edge.

 S1  (N) x* minimises every scenario        <=> x* minimises E~  (own entries +b, all others -b)
     (U) x* the only minimiser everywhere    <=> x* the only minimiser of E~
     truth: enumeration of ALL vertex scenarios (tiny models of several shapes, complete and sparse graphs).
     Controls: four mutilated criteria must disagree with the truth in some models.
 S2  possibly optimal: x minimises SOME scenario <=> x minimises E^x (own entries -b, all others +b).
 S3  per site / per well: W a set of states of site i containing x*_i.
     exact      : in every scenario every minimiser has x_i in W  <=> no x with x_i outside W is possibly optimal;
     sufficient : every x with x_i outside W has E~(x) > E~(x*)   ("compare against x* alone").
     Counted: sufficient => exact (must always hold); exact without sufficient (the sufficient
     condition is not necessary); and the smallest explicit example.
 S4  larger models: sampled scenarios (vertices and interior) where (N) holds; the scenario E~ where it fails.
 S5  uniform b on a complete graph: the exact radius b* = min_x gap(x) / (2 D(x)), D = number of entries x
     uses that x* does not; "x* necessarily optimal only if b <= gap/(2n)" (gap = second-best minus best);
     how often the bound is attained; sparse graphs, where 2n is the wrong count.
 S6  the five numbers of SCI-REV-0026 §0 point 2.
"""
import r28_common as rc
rc.cap()
import itertools
import sys
import time
from fractions import Fraction
import numpy as np

t0 = time.time()
print("R28 no_check.py  start", rc.utc())
rng = np.random.default_rng(2806)


class Model:
    def __init__(self, ks, edges, cen=None, rad=None, emax=12, bmax=3):
        self.ks = list(ks)
        self.n = len(ks)
        self.edges = list(edges)
        self.ent = [("u", i, a) for i in range(self.n) for a in range(ks[i])]
        self.ent += [("p", e, a, c) for e in range(len(self.edges)) for a in range(ks[self.edges[e][0]]) for c in range(ks[self.edges[e][1]])]
        self.m = len(self.ent)
        self.cf = list(itertools.product(*[range(k) for k in ks]))
        self.inc = np.zeros((len(self.cf), self.m), dtype=np.int64)
        col = {e: j for j, e in enumerate(self.ent)}
        for r, x in enumerate(self.cf):
            for i in range(self.n):
                self.inc[r, col[("u", i, x[i])]] = 1
            for e, (i, j) in enumerate(self.edges):
                self.inc[r, col[("p", e, x[i], x[j])]] = 1
        self.cen = rng.integers(-emax, emax + 1, size=self.m) if cen is None else np.asarray(cen, dtype=np.int64)
        self.rad = rng.integers(0, bmax + 1, size=self.m) if rad is None else np.asarray(rad, dtype=np.int64)

    def energies(self, table=None):
        return self.inc @ (self.cen if table is None else table)

    def tilde(self, r, own=1, other=-1, rad=None):
        """table with the entries configuration r uses moved by own*b and all other entries by other*b"""
        rad = self.rad if rad is None else rad
        used = self.inc[r].astype(bool)
        return self.cen + np.where(used, own, other) * rad

    def all_vertex_energies(self):
        m = self.m
        signs = ((np.arange(2 ** m, dtype=np.int64)[:, None] >> np.arange(m)) & 1) * 2 - 1
        return (self.cen[None, :] + signs * self.rad[None, :]) @ self.inc.T          # (vertices, configs)


def complete(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def path(n):
    return [(i, i + 1) for i in range(n - 1)]


# ------------------------------------------------------------------ S1, S2, S3 on tiny models, all vertices
shapes = [((2, 2, 2), complete(3), "3 sites x 2 states, complete (18 entries)"),
          ((3, 3), complete(2), "2 sites x 3 states (15 entries)"),
          ((2, 4), complete(2), "2 sites, 2 and 4 states (14 entries)"),
          ((2, 2, 2, 2), path(4), "4 sites x 2 states, path graph (20 entries)"),
          ((3, 2, 2), path(3), "3 sites (3,2,2), path graph (17 entries)")]
NPER = {0: 150, 1: 150, 2: 150, 3: 30, 4: 100}
tot = dict(models=0, N_agree=0, U_agree=0, N_true=0, U_true=0, m1=0, m2=0, m3=0, m4=0,
           po_checked=0, po_agree=0, site_cases=0, suff_and_exact=0, exact_only=0, suff_not_exact=0, neither=0,
           site_exact_agree=0, vertices=0)
for si, (ks, edges, label) in enumerate(shapes):
    for t in range(NPER[si]):
        M = Model(ks, edges)
        en0 = M.energies()
        r = int(np.argmin(en0))                       # x* = a nominal minimiser
        V = M.all_vertex_energies()
        mn = V.min(axis=1)
        ismin = V == mn[:, None]
        N_true = bool(ismin[:, r].all())
        U_true = bool((ismin[:, r] & (ismin.sum(axis=1) == 1)).all())
        et = M.energies(M.tilde(r))
        N_crit = bool(et[r] == et.min())
        U_crit = bool(et[r] == et.min() and (et == et.min()).sum() == 1)
        tot["models"] += 1
        tot["vertices"] += V.shape[0]
        tot["N_agree"] += N_true == N_crit
        tot["U_agree"] += U_true == U_crit
        tot["N_true"] += N_true
        tot["U_true"] += U_true
        # mutilated criteria (controls)
        e1 = M.energies(M.tilde(r, own=1, other=0))            # others not lowered
        e2 = M.energies(M.tilde(r, own=0, other=-1))           # own not raised
        e3 = en0                                               # no allowance at all
        rad1 = M.rad.copy()
        rad1[sum(ks):] = 0                                     # pair bounds ignored
        e4 = M.energies(M.tilde(r, rad=rad1))
        for key, e in (("m1", e1), ("m2", e2), ("m3", e3), ("m4", e4)):
            tot[key] += bool(e[r] == e.min()) != N_true
        # S2 possibly optimal, every configuration
        po_true = ismin.any(axis=0)
        po_crit = []
        for q in range(len(M.cf)):
            eb = M.energies(M.tilde(q, own=-1, other=+1))
            po_crit.append(bool(eb[q] == eb.min()))
            tot["po_checked"] += 1
            tot["po_agree"] += po_crit[q] == bool(po_true[q])
        # S3 per site, per well
        xs = M.cf[r]
        for i in range(M.n):
            wells = [frozenset([xs[i]])]
            if ks[i] >= 3:
                for extra in range(ks[i]):
                    if extra != xs[i]:
                        wells.append(frozenset([xs[i], extra]))
            for W in wells:
                outside = np.array([x[i] not in W for x in M.cf])
                truth = not bool(ismin[:, outside].any())                    # no minimiser outside W in any vertex scenario
                exact = not any(po_crit[q] for q in range(len(M.cf)) if outside[q])      # from the CRITERION, not from the enumeration
                suff = bool(et[outside].min() > et[r])
                tot["site_cases"] += 1
                tot["site_exact_agree"] += truth == exact
                if suff and truth:
                    tot["suff_and_exact"] += 1
                elif truth and not suff:
                    tot["exact_only"] += 1
                elif suff and not truth:
                    tot["suff_not_exact"] += 1
                else:
                    tot["neither"] += 1
print(f"S1 {tot['models']} tiny models of {len(shapes)} shapes, {tot['vertices']} vertex scenarios enumerated in all")
print(f"   (N) criterion equals enumeration in {tot['N_agree']}/{tot['models']}  (necessarily optimal in {tot['N_true']})")
print(f"   (U) criterion equals enumeration in {tot['U_agree']}/{tot['models']}  (necessarily the only minimiser in {tot['U_true']})")
print(f"   controls — mutilated criteria, disagreements with enumeration (each must be > 0): others not lowered {tot['m1']};"
      f" own entries not raised {tot['m2']}; no allowance {tot['m3']}; pair bounds ignored {tot['m4']}")
print(f"S2 possibly optimal: criterion (own entries lowered, others raised) equals enumeration for {tot['po_agree']}/{tot['po_checked']} configurations")
print(f"S3 per site and well ({tot['site_cases']} cases): the 'no possibly-optimal configuration outside W' form equals enumeration in {tot['site_exact_agree']};"
      f" sufficient and true {tot['suff_and_exact']}; TRUE WITHOUT the sufficient condition {tot['exact_only']};"
      f" sufficient but false {tot['suff_not_exact']} (must be 0); neither {tot['neither']}")

# the smallest explicit example for S3: 2 sites x 2 states, uniform b = 1
ex = Model((2, 2), complete(2), cen=[0, 0, 0, 0, 0, 1, 50, 50], rad=[10] * 8)
# entries: u(0,a) u(0,c) u(1,p) u(1,q) | p(a,p) p(a,q) p(c,p) p(c,q);  energies x10 so that b = 1 is 10 units
en = ex.energies()
V = ex.all_vertex_energies()
ismin = V == V.min(axis=1)[:, None]
r = int(np.argmin(en))
et = ex.energies(ex.tilde(r))
outside = np.array([x[0] != ex.cf[r][0] for x in ex.cf])
print("   explicit example (2 sites x 2 states; energies in tenths; every entry within b = 10):")
print(f"      configurations {ex.cf}: nominal energies {en.tolist()}; x* = {ex.cf[r]}")
print(f"      x* necessarily optimal: {bool(ismin[:, r].all())};  site 0 keeps its state in every one of the {V.shape[0]} vertex scenarios: {not bool(ismin[:, outside].any())};"
      f"  sufficient condition (E~ of every configuration with another state at site 0 above E~(x*)): {bool(et[outside].min() > et[r])}"
      f"  [E~ = {et.tolist()}]")

# ------------------------------------------------------------------ S4 larger models
hold = fail = viol = beats = scen = 0
for t in range(400):
    n = int(rng.integers(3, 7))
    ks = [int(rng.integers(2, 5)) for _ in range(n)]
    if np.prod(ks) > 1500:
        ks = ks[:4]
        n = 4
    edges = complete(n) if rng.random() < 0.6 else [e for e in complete(n) if rng.random() < 0.5]
    M = Model(ks, edges, emax=30, bmax=int(rng.integers(0, 4)))
    en = M.energies()
    r = int(np.argmin(en))
    et = M.energies(M.tilde(r))
    if et[r] == et.min():
        hold += 1
        for s in range(60):
            if s % 2 == 0:
                tab = 2 * (M.cen + M.rad * rng.choice([-1, 1], size=M.m))
            else:
                tab = 2 * M.cen + rng.integers(-2 * M.rad, 2 * M.rad + 1)
            e2 = M.energies(tab)
            scen += 1
            viol += e2[r] != e2.min()
    else:
        fail += 1
        beats += et.min() < et[r]
print(f"S4 400 larger models (3-6 sites, 2-4 states, complete and random sparse graphs): (N) holds in {hold}, fails in {fail};"
      f" where it holds: x* not a minimiser in {viol} of {scen} sampled scenarios (must be 0);"
      f" where it fails: E~ has a strictly better configuration in {beats}/{fail} (must be all)")

# ------------------------------------------------------------------ S5 uniform b, the radius, 'only if b <= gap/(2n)'
def radius(M, r):
    """largest uniform b with x* necessarily optimal: min over x != x* of (E(x)-E(x*)) / (number of entries in the symmetric difference)"""
    en = M.energies()
    D = np.abs(M.inc - M.inc[r][None, :]).sum(axis=1)            # symmetric difference = 2 * (entries x uses that x* does not)
    best = None
    arg = None
    for q in range(len(M.cf)):
        if q == r:
            continue
        v = Fraction(int(en[q] - en[r]), int(D[q]))
        if best is None or v < best:
            best, arg = v, q
    return best, arg, D


stat = dict(models=0, bound_ok=0, attained=0, strict=0, binder_multi=0, second_multi=0, radius_check=0, radius_ok=0)
for t in range(400):
    n = int(rng.integers(2, 6))
    ks = [int(rng.integers(2, 4)) for _ in range(n)]
    M = Model(ks, complete(n), emax=40, bmax=0)
    en = M.energies()
    order = np.argsort(en, kind="stable")
    if en[order[0]] == en[order[1]]:
        continue                                              # no unique minimiser: gap 0
    r = int(order[0])
    gap = int(en[order[1]] - en[r])
    bstar, arg, D = radius(M, r)
    stat["models"] += 1
    bound = Fraction(gap, 2 * n)
    stat["bound_ok"] += bstar <= bound
    stat["attained"] += bstar == bound
    stat["strict"] += bstar < bound
    nd = lambda q: sum(a != c for a, c in zip(M.cf[q], M.cf[r]))
    stat["binder_multi"] += nd(arg) > 1
    stat["second_multi"] += nd(int(order[1])) > 1
    # check the radius against enumeration-free truth: at b just below b* the criterion holds, just above it fails
    if bstar > 0:
        for num, expect in ((bstar * Fraction(99, 100), True), (bstar * Fraction(101, 100), False)):
            sc = num.denominator
            tab = M.cen * sc
            radv = np.full(M.m, num.numerator, dtype=np.int64)
            used = M.inc[r].astype(bool)
            e2 = M.inc @ (tab + np.where(used, 1, -1) * radv)
            stat["radius_check"] += 1
            stat["radius_ok"] += bool(e2[r] == e2.min()) == expect
print(f"S5 complete graphs, uniform b, {stat['models']} models with a unique minimiser: exact radius b* <= gap/(2n) in {stat['bound_ok']} (must be all);"
      f" b* = gap/(2n) in {stat['attained']}; b* < gap/(2n) in {stat['strict']} (the binding competitor differs at several sites in {stat['binder_multi']};"
      f" the second-best configuration differs at several sites in {stat['second_multi']});"
      f" radius confirmed by the criterion just below / just above in {stat['radius_ok']}/{stat['radius_check']}")
# the count D(d) = d (2n + 1 - d) / 2 for a complete graph
okD = True
for n in range(2, 7):
    M = Model([2] * n, complete(n), emax=1, bmax=0)
    for q in range(len(M.cf)):
        d = sum(M.cf[q])
        if np.abs(M.inc[q] - M.inc[0]).sum() != d * (2 * n + 1 - d):
            okD = False
print(f"   entries a configuration differing at d of n sites uses that x* does not (complete graph): d(2n+1-d)/2 — checked for n = 2..6: {okD};"
      f" d = 1 gives n, the smallest value")
# sparse graph: 2n is the wrong count
cnt = viol_sparse = 0
for t in range(300):
    n = int(rng.integers(3, 7))
    M = Model([2] * n, path(n), emax=40, bmax=0)
    en = M.energies()
    order = np.argsort(en, kind="stable")
    if en[order[0]] == en[order[1]]:
        continue
    r = int(order[0])
    bstar, arg, D = radius(M, r)
    cnt += 1
    viol_sparse += bstar > Fraction(int(en[order[1]] - en[r]), 2 * n)
print(f"   path graphs (each site in at most two pair tables): b* EXCEEDS gap/(2n) in {viol_sparse} of {cnt} models —"
      f" the count 2n holds for dense tables only; in general it is 2(1 + degree of the flipped site)")

# ------------------------------------------------------------------ S6 the five numbers
print("S6 gap/(2n) for the five published (sites, gap in kcal/mol):")
claimed = {"1CRN": (26, 0.0451, 8.7e-4), "5PTI": (36, 0.0243, 3.4e-4), "1BPI": (36, 0.1102, 1.5e-3), "1PGA": (46, 0.0068, 7.4e-5), "2IGD": (49, 0.0039, 4.0e-5)}
bad = 0
for nm, (n, gap, cl) in claimed.items():
    v = gap / (2 * n)
    lo, hi = (gap - 5e-5) / (2 * n), (gap + 5e-5) / (2 * n)
    ok = f"{v:.1e}" == f"{cl:.1e}"
    bad += not ok
    print(f"   {nm}: {gap} / (2 x {n}) = {v:.4e}  -> two significant digits {v:.1e}; claimed {cl:.1e}; equal: {ok};"
          f" with the gap known to +-5e-5: {lo:.3e} .. {hi:.3e}; one-site allowance 2bn at b = 2^-21: {2 * 2**-21 * n:.3e}")
print(f"   disagreements: {bad} of 5;  2^-21 = {2**-21:.4e} (the 'rounding unit 4.8e-7' of the text)")
print(f"   one-site allowance 2bn for n = 26 and n = 65: b = 2^-21: {2*2**-21*26:.2e}, {2*2**-21*65:.2e}; b = 0.01: {2*0.01*26:.2f}, {2*0.01*65:.2f}; b = 0.1: {2*0.1*26:.1f}, {2*0.1*65:.1f}")
rc.finish(t0)
