#!/usr/bin/env python3
"""OPTIMAL SITE SHARES beyond enumeration -- coordinator's script (follows allocation_core_test.py, where everything
below is checked against exhaustive enumeration on Ace-Leu12-NMe).

Valid minimal site penalties are the core of the convex game Gamma(R) = sum_{T subset R} chat_T; its vertices are the
marginal vectors of orderings, gamma_i = Gamma(R_i) - Gamma(R_i minus i), each computable from n + 1 closed-form sums
on nested sets (workstream P6's sums with sites excluded) -- no subset is enumerated.  For a solvable site-penalty
sandwich  m_-/+ = [minorant / majorant of f + I_{m-1} g] -/+ sum_i gs_i [x_i != x0_i]:
  * ln Z(m_-) is CONVEX in the penalties: minimised over the core by Frank-Wolfe.  Gradient = beta x the off-anchor
    marginals of the floor model itself (exact, by transfer matrix: BandModel.moments); linear oracle = the marginal
    vector of the ordering by those marginals, most frozen first (Edmonds' greedy rule; the theory division's
    Proposition 11.18f(c) is its first step);  the duality gap certifies how far from the optimum the iterate is.
  * ln Z(m_+) is concave... i.e. -ln Z(m_+) is CONCAVE in the penalties: the best ceiling is a vertex = an ordering;
    start from "most frozen first" (marginals of the penalty-free majorant) and improve by adjacent swaps.
Floor and ceiling use DIFFERENT penalties (each covers, so the sandwich holds).
Allowances.  The floating-point error of the evaluated terms at a state with changed set S is at most
Phi(S) = EPS_G sum_{s=1}^{m-1} C(|S|, s) 2^s (workstream P3: every d_U is an alternating sum of 2^|U| evaluated values;
plus EPS_G for g(x0), kept as the models' constant).  Phi is a sum over subsets of S of non-negative weights -- THE SAME
STRUCTURE AS Gamma: a convex game -- so it is allocated by the same rule: the marginal vector of an ordering gives the
site at the head of a suffix of r sites  EPS_G sum_s C(r-1, s-1) 2^s.  P3's site allocation phi1 is its Shapley
value (equal split) and charges a mobile site as if every other site had changed; the vertex "most frozen first"
charges the mobile sites next to nothing.  Every vertex used below is the marginal vector of Gamma + Phi; a further
5e-9 Gamma per site covers the rounding of differences of rounded sums.  "Equal shares" is reported with P3's own
phi1, so that it reproduces workstream P3's site form.
Reported: the certified bracket with equal shares (workstream P3's site form: gamma_i = S_i / m), with the vertex
"most frozen first" at both ends (Proposition 11.18f(c) as stated), and with floor = Frank-Wolfe, ceiling = best
ordering; the sandwich is checked at Gibbs samples of the true ensemble and at exact samples of the floor.
Run:  python3 -B site_allocation_fw.py SEQ BB m w [models: reduced|window] [max FW steps] [max sweeps of the ordering search] [chains,sweeps,burn]
(at thirty residues one closed-form sum costs seconds: the two budgets decide the running time; the bracket printed is
certified at whatever iterate the budgets stop at, and the duality gap says how far the floor is from the best one)
What is whose: allocation problem and first-order rule -- theory division (Proposition 11.18f); constants, ball, band
models -- P3; closed-form sums -- P6; window models, convex-game reading, Frank-Wolfe, ordering search -- coordinator.
Model-relative; the certified constants are P3's paper proofs; allowances are allowances.
"""
import os, sys, math, json, time, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nested_sampler as NS
L, pw, BETA, EPS_G = NS.L, NS.pw, NS.BETA, NS.EPS_G
import serine_helix_reach as SR                    # the Gibbs sampler of the true ensemble


def log(s): print(s, flush=True)


def waterfill_bound(a, G):
    """A FLOOR NO SITE ALLOCATION CAN BEAT (coordinator; elementary).  Let m_-(gamma) = B - sum_i gamma_i [x_i != x0_i]
    for a base model B, and let a_i = exp(-beta B(x^i)) / Z(B) be the probability, under B, of the cheapest state x^i in
    which site i alone is changed.  Raising the weights of these n states only,
        Z(m_-(gamma)) >= Z(B) + sum_i exp(-beta B(x^i)) (e^{beta gamma_i} - 1),
    so  ln Z(m_-(gamma)) - ln Z(B) >= ln(1 + sum_i a_i (e^{g_i} - 1)),  g = beta gamma.  Every covering gamma has
    sum_i g_i >= G := beta Gamma(all sites) (the full set must be covered).  Minimising the convex function
    sum_i a_i (e^{g_i} - 1) over g >= 0, sum g_i >= G is water-filling: g_i = ln(lam / a_i)^+ with
    sum_i ln(lam / a_i)^+ = G, value sum_{active} (lam - a_i).  Returns (the bound ln(1 + value), g, lam).
    Needs only Gamma_m and the ball of radius one: an a-priori criterion for the site level.
    SHARPER, same function with other weights (found after the first runs): since e^{g.s} = prod_i (1 + s_i (e^{g_i} - 1))
    >= 1 + sum_i s_i (e^{g_i} - 1) for 0/1 indicators s_i,
        Z(m_-(gamma)) >= Z(B) (1 + sum_i p_i (e^{beta gamma_i} - 1)),   p_i = the off-anchor MARGINAL of site i under B,
    and p_i >= a_i.  Call the function with the marginals p in place of a: the bound is then exact to first order in
    the boosts, and its minimiser g_i = ln(lam / p_i)^+ is "each site is charged what its rarity can pay"."""
    a = np.asarray(a, dtype=float); la = np.log(a)
    f = lambda t: float(np.maximum(t - la, 0.0).sum()) - G            # t = ln lam; increasing in t
    lo_, hi_ = float(la.min()), float(la.max()) + G + 1.0
    for _ in range(200):
        mid = 0.5 * (lo_ + hi_)
        if f(mid) < 0: lo_ = mid
        else: hi_ = mid
    t = 0.5 * (lo_ + hi_); g = np.maximum(t - la, 0.0); val = float((np.exp(t) - a)[g > 0].sum())
    return math.log1p(val), g, math.exp(t)


class GammaOracle:
    """Gamma(R) = sum of chat_T over the m-subsets of R, by P6's closed form with the complement excluded; cached."""

    def __init__(self, GF, m, n):
        self.B = L.GFBatch(GF); self.m = m; self.n = n; self.cache = {0: 0.0}; self.calls = 0; self.seconds = 0.0

    def get(self, masks):
        todo = sorted({int(u) for u in masks if int(u) not in self.cache})
        small = [u for u in todo if bin(u).count("1") < self.m]
        for u in small: self.cache[u] = 0.0
        todo = [u for u in todo if bin(u).count("1") >= self.m]
        t1 = time.time()
        for s in range(0, len(todo), 128):
            chunk = todo[s:s + 128]
            se, cr = self.B.totals(self.m, [tuple(i for i in range(self.n) if not (u >> i) & 1) for u in chunk])
            for u, v in zip(chunk, se + cr): self.cache[u] = float(v)
        self.calls += len(todo); self.seconds += time.time() - t1
        return np.array([self.cache[int(u)] for u in masks])

    def vertex(self, order):
        """marginal vector of `order` (first = charged first)."""
        R = (1 << self.n) - 1; ms = [R]
        for i in order:
            R &= ~(1 << i); ms.append(R)
        v = self.get(ms); g = np.zeros(self.n)
        for j, i in enumerate(order): g[i] = v[j] - v[j + 1]
        return g

    def fp_vertex(self, order):
        """marginal vector of the floating-point game Phi for `order`: the site heading a suffix of r sites gets
        EPS_G sum_{s=1}^{M} C(r-1, s-1) 2^s  (= Phi(r) - Phi(r-1)),  M = m - 1."""
        M = self.m - 1; g = np.zeros(self.n)
        for j, i in enumerate(order):
            r = self.n - j; g[i] = EPS_G * sum(math.comb(r - 1, s_ - 1) * 2 ** s_ for s_ in range(1, M + 1))
        return g

    def total_vertex(self, order):
        """marginal vector of Gamma + Phi."""
        return self.vertex(order) + self.fp_vertex(order)


def main():
    a = sys.argv[1:]
    seq, bb, m, w = a[0], a[1], int(a[2]), int(a[3]); models = a[4] if len(a) > 4 else "reduced"; maxit = int(a[5]) if len(a) > 5 else 300
    maxsweeps = int(a[6]) if len(a) > 6 else 6                       # sweeps of the ordering search for the ceiling (each costs n - 1 closed-form sums)
    gib = [int(v) for v in a[7].split(",")] if len(a) > 7 else [16, 250, 50]   # Gibbs check of the true ensemble: chains, sweeps, burn-in
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    t0 = time.time(); M = m - 1; rng = np.random.default_rng(20261127)
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = np.array(x0)
    dom = float(np.prod([float(v) for v in k]))
    GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m); ORA = GammaOracle(GF, m, n)
    full = (1 << n) - 1
    Gam = float(ORA.get([full])[0]); S = Gam - ORA.get([full & ~(1 << i) for i in range(n)])            # S_i = sum of chat_T over T through i
    d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    zero = np.zeros(n); z2 = np.zeros((n, n))
    if models == "window":
        lo0, up0, info = NS.build_window_models(k, x0, c0, h, J, d, w, EPS_G, M, zero, z2, None)
    else:
        lo0, up0 = L.build_models(k, x0, c0, h, J, d, w, M, zero, z2); info = dict(exact=0)
    base_lo = [o.copy() for o in lo0.one]; base_up = [o.copy() for o in up0.one]
    assert all(v > 1 for v in k)                                      # every site can change (Phi counts all of them)
    allow = np.full(n, 5e-9 * Gam)                                    # rounding of differences of rounded sums; the fp game is inside the vertices
    PhiN = EPS_G * sum(math.comb(n, s_) * 2 ** s_ for s_ in range(1, M + 1))
    assert abs(ORA.fp_vertex(list(range(n))).sum() - PhiN) < 1e-12 * max(1.0, PhiN)

    def set_pen(mdl, base, gam, sense):
        for i in range(n):
            pen = np.full(k[i], sense * (gam[i] + allow[i])); pen[x0[i]] = 0.0
            mdl.one[i] = base[i] + pen

    def lnZ_floor(gam):
        set_pen(lo0, base_lo, gam, -1.0); return lo0.lnZ()

    def lnZ_ceil(gam):
        set_pen(up0, base_up, gam, +1.0); return up0.lnZ()

    ind = []
    for i in range(n):
        mdl = pw.BandModel(k, w); v = np.ones(k[i]); v[x0[i]] = 0.0; mdl.one[i] = v; ind.append(mdl)

    def marg(mdl):
        return np.array([mdl.moments(ind[i])[0] for i in range(n)])

    log(f"=== optimal site shares: {seq}/{bb}, order {m}, band {w}, models '{models}' ({info.get('exact', 0)} evaluated terms exact in the window): {n} sites, "
        f"{dom:.6g} assignments, ball {nball} evaluations; Gamma_{m} = {BETA * Gam:.4f} kT [{time.time() - t0:.0f}s]")
    # the true ensemble (uncertified), for the sandwich check and for the reader
    fr, XG = SR.gibbs(G, c0, h, J, x0, k, rng, nchain=gib[0], nsweep=gib[1], burn=gib[2]); pi = fr.mean(0)
    EG = pw.f_energy(XG, c0, h, J) + G.bulk_energy(XG)
    log(f"(0) Gibbs sampling of the true ensemble ({gib[0]} chains, {gib[1]} sweeps, {gib[2]} discarded; {len(XG)} states kept; uncertified, used only to check the "
        f"sandwich): off-anchor frequencies " + " ".join(f"{v:.2f}" for v in pi) + f" [{time.time() - t0:.0f}s]")
    res = dict(seq=seq, bb=bb, m=m, w=w, models=models, n=n, domain=dom, nball=int(nball), Gamma_kT=BETA * Gam, p_site=[float(v) for v in pi], rows={})

    def report(name, g_floor, g_ceil):
        b_ = lnZ_floor(g_floor); l1 = lo0.energy(XG); xs = lo0.sample(2000, rng); ml = lo0.energy(xs)
        a_ = lnZ_ceil(g_ceil); u1 = up0.energy(XG); mu = up0.energy(xs)
        Ex = pw.f_energy(xs, c0, h, J) + G.bulk_energy(xs)
        v = int((l1 > EG + 1e-9).sum() + (u1 < EG - 1e-9).sum()); vx = int((ml > Ex + 1e-9).sum() + (mu < Ex - 1e-9).sum())
        offx = float((xs != x0[None]).sum(1).mean())
        log(f"    {name}: CERTIFIED ln Z(E) in [{a_:.6f}, {b_:.6f}], width {b_ - a_:.6g} nats; sandwich violated at {v} of {len(XG)} Gibbs states and at {vx} of "
            f"2000 exact samples of the floor ({offx:.2f} sites off the anchor there); largest floor penalty {BETA * float(g_floor.max()):.2f} kT, "
            f"largest ceiling penalty {BETA * float(g_ceil.max()):.2f} kT")
        res["rows"][name] = dict(lo=a_, hi=b_, width=b_ - a_, viol_gibbs=v, viol_floor_samples=vx, floor_off=offx)
        return a_, b_

    g_eq = np.maximum(S, 0.0) / m * L.RND + phi1                       # P3's site form: equal shares of Gamma and of Phi
    a_eq, b_eq = report("equal shares (P3's site form)", g_eq, g_eq)
    # the a-priori bound for the site level: water-filling over the cheapest single-change states of the penalty-free floor model
    set_pen(lo0, base_lo, zero - allow, -1.0)                          # gs = 0: the minorant of f + I g alone (no penalty, no allowance)
    lnZ_base = lo0.lnZ(); a_i = np.zeros(n)
    for i in range(n):
        stt = np.tile(x0, (k[i], 1)); stt[:, i] = np.arange(k[i]); e = np.delete(lo0.energy(stt), x0[i])
        a_i[i] = math.exp(-BETA * float(e.min()) - lnZ_base)
    wf, g_wf, lam = waterfill_bound(a_i, BETA * (Gam + PhiN))
    log(f"    A-PRIORI BOUND for the site level (water-filling over the cheapest single-change states; needs Gamma_{m} and the ball of radius one): "
        f"every vector of site penalties that covers the constants and the floating-point allowance (together {BETA * (Gam + PhiN):.4f} kT on the full set) "
        f"has ln Z(m_-) >= {lnZ_base + wf:.6f}, i.e. at least {wf:.4g} nats above the penalty-free minorant "
        f"{lnZ_base:.6f}; probabilities of the single-change states, -ln a_i: " + " ".join(f"{-math.log(v):.1f}" for v in a_i)
        + "; water-filling penalties, kT: " + " ".join(f"{v:.2f}" for v in g_wf))
    res["waterfill"] = dict(bound=wf, lnZ_base=lnZ_base, minus_ln_a=[float(-math.log(v)) for v in a_i], g_kT=[float(v) for v in g_wf])
    # most frozen first: by the marginals of the penalty-free ceiling (a majorant of A: the best available solvable proxy), ties by the single-change cost
    set_pen(up0, base_up, zero, +1.0); p0 = marg(up0)
    single = np.zeros(n)                                  # cheapest single change at each site, kT, from the ball (exact values)
    for i in range(n):
        stt = np.tile(x0, (k[i], 1)); stt[:, i] = np.arange(k[i]); e = pw.f_energy(stt, c0, h, J) + pw.expansion_value(d, stt)
        single[i] = BETA * (np.delete(e, x0[i]).min() - e[x0[i]])
    order_f = sorted(range(n), key=lambda i: (round(float(p0[i]), 9), -single[i]))
    g_fro = ORA.total_vertex(order_f)
    log(f"(1) off-anchor marginals of the penalty-free majorant: " + " ".join(f"{v:.3f}" for v in p0) + f"; ordering most frozen first: {order_f} [{time.time() - t0:.0f}s]")
    a_fr, b_fr = report("vertex 'most frozen first' at both ends (Proposition 11.18f(c))", g_fro, g_fro)
    # ---- the ceiling: ordering search by adjacent swaps (maximise ln Z(m_+))
    order = list(order_f); best = lnZ_ceil(ORA.total_vertex(order)); improved = True; swaps = 0; sweeps = 0
    while improved and sweeps < maxsweeps:
        improved = False; sweeps += 1
        for q in range(n - 1):
            o2 = order[:]; o2[q], o2[q + 1] = o2[q + 1], o2[q]; v2 = lnZ_ceil(ORA.total_vertex(o2))
            if v2 > best + 1e-12: order, best, improved = o2, v2, True; swaps += 1
    g_ceil = ORA.total_vertex(order)
    log(f"(2) ceiling: ordering search, {swaps} improving swaps in {sweeps} sweeps: ln Z(m_+) = {best:.6f} (most frozen first: {a_fr:.6f}; equal shares: {a_eq:.6f}) "
        f"[{time.time() - t0:.0f}s; {ORA.calls} closed-form sums so far, {ORA.seconds:.0f}s]")
    # ---- the floor: Frank-Wolfe over the core
    cands = [("equal", g_eq), ("frozen", g_fro)]
    vals = [lnZ_floor(g) for _, g in cands]; gam = cands[int(np.argmin(vals))][1].copy(); cur = min(vals); gap = float("inf"); hist = []
    for it in range(1, maxit + 1):
        set_pen(lo0, base_lo, gam, -1.0); pt = marg(lo0)
        o = sorted(range(n), key=lambda i: (pt[i], -single[i])); v = ORA.total_vertex(o)
        gap = BETA * float(pt @ (gam - v)); hist.append((it, cur, gap))
        if it % 10 == 1: log(f"      Frank-Wolfe step {it}: ln Z(m_-) = {cur:.6f}, duality gap {gap:.3e} nats [{time.time() - t0:.0f}s; {ORA.calls} sums]")
        if gap < 1e-6: break
        lo_, hi_ = 0.0, 1.0
        for _ in range(40):
            a1 = lo_ + (hi_ - lo_) / 3; a2 = hi_ - (hi_ - lo_) / 3
            if lnZ_floor(gam + a1 * (v - gam)) < lnZ_floor(gam + a2 * (v - gam)): hi_ = a2
            else: lo_ = a1
        gam = gam + 0.5 * (lo_ + hi_) * (v - gam); cur = lnZ_floor(gam)
    log(f"(3) floor: Frank-Wolfe, {it} steps: ln Z(m_-) = {cur:.6f}, duality gap {gap:.3e} nats (so no core allocation gives a floor below {cur - gap:.6f}); "
        f"equal shares {b_eq:.6f}, most frozen first {b_fr:.6f} [{time.time() - t0:.0f}s; {ORA.calls} closed-form sums, {ORA.seconds:.0f}s]")
    log("    site penalties, kT: equal " + " ".join(f"{BETA * v:.2f}" for v in g_eq) + " | frozen first " + " ".join(f"{BETA * v:.2f}" for v in g_fro)
        + " | Frank-Wolfe (floor) " + " ".join(f"{BETA * v:.2f}" for v in gam) + " | ceiling " + " ".join(f"{BETA * v:.2f}" for v in g_ceil))
    a_, b_ = report("floor = Frank-Wolfe optimum, ceiling = best ordering", gam, g_ceil)
    res.update(order_frozen=order_f, order_ceiling=order, fw_steps=it, fw_gap=gap, closed_form_sums=ORA.calls, gamma_floor_kT=[float(BETA * v) for v in gam],
               gamma_ceiling_kT=[float(BETA * v) for v in g_ceil], seconds=time.time() - t0, peak_rss_mb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
    json.dump(res, open(os.path.join(HERE, f"site_allocation_fw_{seq.replace(':', 'c')}_{bb}_m{m}_w{w}_{models}.json"), "w"), indent=1)
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {res['peak_rss_mb']:.0f} MB")


if __name__ == "__main__":
    main()
