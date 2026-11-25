"""
T5 — finite temperature: variational rate bounds against exact linear algebra.

Dynamics: continuous-time single-site Metropolis, one proposal per neighbour per unit time,
  rate(x->y) = min(1, exp(-beta (E_y - E_x))),   c(x,y) = pi(x) rate(x->y) = exp(-beta max(E_x,E_y)) / Z.
(The discrete-time Metropolis sampler with uniform (site,state) proposals is P = I + Q/deg, deg = sum_i (k_i-1).)

For a metastable state a with exit target b, A = component of a in {E < B(a,b)}:

 (i)   lambda_A <= k_cut := Q(A,A^c)/pi(A)                       [Dirichlet eigenvalue vs indicator]
       identity  k_cut = sum_j w_j lambda_j  (spectral measure of 1_A)
       E_{pi_A}[tau] >= 1/k_cut,   P_{pi_A}(tau > t) >= exp(-k_cut t) for all t      [Jensen]
       k_cut <= k_cert := sum_{y in outer bdry} deg_A(y) e^{-beta E(y)} / Z(A)        [boundary partition fn]
 (ii)  gap <= Q(A,A^c)/(pi(A) pi(A^c))
 (iii) cap(a,b):  Dirichlet indicator (one cut)  >=  Nash-Williams over the levels of
       q = #{i in I : x_i != a_i}, I = sites where a and b differ  >=  exact
       >=  Thomson with K edge-disjoint minimax paths  >=  Thomson with one path.
       certified level form:  C_m <= min((m+1) Z_{m+1}, (sum_{i in I} (k_i-1) - ...) Z_m)/Z.
       mean hitting time identity  E_nu[tau_B] = sum_y pi(y) h_{A,B}(y) / cap(A,B).

Run:  python3 t5_rates.py
"""
import numpy as np
from kcore import (Space, barrier_from, random_pairwise, pairwise_energy, local_minima,
                   ising_chain_energy, curie_weiss_energy, component_below, outer_boundary,
                   generator, gibbs, conductances, spectral_gap, dirichlet_eig, mean_exit_time,
                   capacity, minimax_path)

rng = np.random.default_rng(3)


def exit_target(S, E, a):
    Ba = barrier_from(S, E, a)
    lower = np.nonzero(E < E[a])[0]
    if len(lower) == 0:
        return None
    best = Ba[lower].min()
    cands = lower[Ba[lower] <= best + 1e-12]
    return int(cands[np.argmin(E[cands])])


def edge_disjoint_paths(S, E, a, b, C, K):
    """Greedy: repeatedly take a minimax path avoiding used edges (by a large penalty on vertices is not
    possible for edges, so we search on a copy of the adjacency with used edges removed)."""
    import heapq
    used = set()
    paths = []
    for _ in range(K):
        Bv = np.full(S.N, np.inf)
        par = np.full(S.N, -1, dtype=np.int64)
        Bv[a] = E[a]
        heap = [(E[a], 0, a)]
        done = np.zeros(S.N, dtype=bool)
        while heap:
            bb, hops, u = heapq.heappop(heap)
            if done[u]:
                continue
            done[u] = True
            if u == b:
                break
            for v in S.nbrs[u]:
                v = int(v)
                if done[v] or (min(u, v), max(u, v)) in used:
                    continue
                nb = max(bb, E[v])
                if nb < Bv[v]:
                    Bv[v] = nb
                    par[v] = u
                    heapq.heappush(heap, (nb, hops + 1, v))
        if not np.isfinite(Bv[b]):
            break
        p = [b]
        while p[-1] != a:
            p.append(int(par[p[-1]]))
        p = p[::-1]
        for u, v in zip(p[:-1], p[1:]):
            used.add((min(u, v), max(u, v)))
        paths.append(p)
    return paths


def analyse(S, E, beta, a, b, label):
    N = S.N
    Q = generator(S, E, beta, "metropolis")
    pi = gibbs(E, beta)
    C = conductances(Q, pi)
    assert np.allclose(C, C.T, rtol=1e-9, atol=1e-300)
    gap, _ = spectral_gap(Q, pi)
    B = barrier_from(S, E, a)[b]
    A = component_below(S, E, a, B, strict=True)
    piA = pi[A].sum()
    Qflow = C[np.ix_(A, ~A)].sum()
    kcut = Qflow / piA
    lamA, qsd, evA, wts, idx = dirichlet_eig(Q, pi, A)
    ident = abs((wts * evA).sum() / kcut - 1)
    w = mean_exit_time(Q, A)
    Epi = (pi[A] * w[A]).sum() / piA
    Eqsd = (qsd * w[idx]).sum()
    ts = np.concatenate([[0.0], np.logspace(-3, 2.5, 60) / kcut])
    surv = (wts[None, :] * np.exp(-np.outer(ts, evA))).sum(axis=1)
    surv_ok = bool(np.all(surv >= np.exp(-ts * kcut) * (1 - 1e-9)))
    surv_min_ratio = float(np.min(surv / np.exp(-ts * kcut)))
    ob = outer_boundary(S, A)
    degA = np.array([A[S.nbrs[y]].sum() for y in range(N)])
    Emin = E.min()
    wgt = np.exp(-beta * (E - Emin))
    kcert = (degA[ob] * wgt[ob]).sum() / wgt[A].sum()
    gap_cut = Qflow / (piA * (1 - piA))
    # ---- capacities between the two states
    ma = np.zeros(N, dtype=bool); ma[a] = True
    mb = np.zeros(N, dtype=bool); mb[b] = True
    cap, h = capacity(Q, pi, ma, mb)
    cap_cut = Qflow
    I = S.cfg[a] != S.cfg[b]
    q = (S.cfg[:, I] != S.cfg[a][I][None, :]).sum(axis=1)
    R_nw = 0.0
    R_nwc = 0.0
    Z = wgt.sum()
    nI = int(I.sum())
    kI = np.array(S.ks)[I]
    for m in range(nI):
        lo = q == m
        hi = q == m + 1
        Cm = C[np.ix_(lo, hi)].sum()
        R_nw += 1.0 / Cm
        # certified from level partition functions: each y at level m+1 has exactly m+1 neighbours at level m;
        # each x at level m has sum_{i in I: x_i = a_i}(k_i-1) neighbours at level m+1 (<= max over x)
        up_deg = np.array([((S.cfg[x, I] == S.cfg[a][I]) * (kI - 1)).sum() for x in np.nonzero(lo)[0]]).max()
        Cm_cert = min((m + 1) * wgt[hi].sum(), up_deg * wgt[lo].sum()) / Z
        assert Cm <= Cm_cert * (1 + 1e-12)
        R_nwc += 1.0 / Cm_cert
    cap_nw = 1.0 / R_nw
    cap_nwc = 1.0 / R_nwc
    paths = edge_disjoint_paths(S, E, a, b, C, 8)
    Rs = [sum(1.0 / C[u, v] for u, v in zip(p[:-1], p[1:])) for p in paths]
    cap_1path = 1.0 / Rs[0]
    cap_kpath = sum(1.0 / r for r in Rs)
    # ---- mean hitting time a -> b and the potential-theoretic identity
    notb = ~mb
    idxn = np.nonzero(notb)[0]
    wb = np.linalg.solve(-Q[np.ix_(idxn, idxn)], np.ones(len(idxn)))
    Ea = wb[list(idxn).index(a)]
    ident2 = abs(Ea * cap / (pi * h).sum() - 1)
    # set version: nu_{A,B} with A the basin and B = {b}
    capAB, hAB = capacity(Q, pi, A, mb)
    e = -(Q @ hAB)
    nu = np.where(A, pi * e, 0.0) / capAB
    wfull = np.zeros(N); wfull[idxn] = wb
    Enu = (nu * wfull).sum()
    ident3 = abs(Enu * capAB / (pi * hAB).sum() - 1)
    lb_Enu = piA / capAB
    row = dict(label=label, beta=beta, H=B - E[a], sizeA=int(A.sum()), piA=piA,
               lam_over_kcut=lamA / kcut, Epi_kcut=Epi * kcut, Eqsd_lam=Eqsd * lamA, surv_ok=surv_ok,
               surv_min=surv_min_ratio, kcert_over_kcut=kcert / kcut, gap_over_gapcut=gap / gap_cut,
               cap_over_cut=cap / cap_cut, cap_over_nw=cap / cap_nw, cap_over_nwc=cap / cap_nwc,
               path1_over_cap=cap_1path / cap, pathK_over_cap=cap_kpath / cap, npaths=len(paths),
               ident=max(ident, ident2, ident3), ident_spec=ident, ident_hit=max(ident2, ident3),
               cond=pi[a] / pi.max(), Enu_over_lb=Enu / lb_Enu, Ea=Ea,
               arr=-np.log(lamA) / beta if beta > 0 else np.nan)
    return row


def show(rows):
    hdr = ("beta  H     |A|   pi(A)    lam/kcut Epi*kcut surv  kcert/kcut gap/gapcut "
           "cap/cut cap/NW cap/NWc 1path/cap Kpath/cap  Enu/lb   ident")
    print("   " + hdr)
    for r in rows:
        print(f"   {r['beta']:<4.2f} {r['H']:<5.2f} {r['sizeA']:<5d} {r['piA']:<8.2e} {r['lam_over_kcut']:<8.3f} "
              f"{r['Epi_kcut']:<8.3f} {str(r['surv_ok']):<5s} {r['kcert_over_kcut']:<10.2f} "
              f"{r['gap_over_gapcut']:<10.3f} {r['cap_over_cut']:<7.3f} {r['cap_over_nw']:<6.3f} "
              f"{r['cap_over_nwc']:<7.3f} {r['path1_over_cap']:<9.3f} {r['pathK_over_cap']:<9.3f} "
              f"{r['Enu_over_lb']:<8.3f} {r['ident']:.1e}")


def main():
    allrows = []
    S = Space([2] * 10)
    print("T5: Curie-Weiss n=10, J=1, h=0.05; a = all-down, b = all-up")
    E = curie_weiss_energy(S, 1.0, 0.05)
    rows = [analyse(S, E, beta, 0, S.N - 1, "CW") for beta in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0)]
    show(rows); allrows += rows
    print("T5: Ising chain n=10, J=1, h=0.3 (open); a = all-down, b = all-up")
    E = ising_chain_energy(S, 1.0, 0.3)
    rows = [analyse(S, E, beta, 0, S.N - 1, "Ising") for beta in (0.5, 1.0, 2.0, 3.0, 4.0)]
    show(rows); allrows += rows
    print("T5: random pairwise models (deepest non-global strict local minimum a, b = exit target)")
    for name, ks, graph in (("binary n=10 chain+", [2] * 10, "chain+"), ("3-state n=6 chain+", [3] * 6, "chain+"),
                            ("binary n=10 complete", [2] * 10, "complete")):
        S = Space(ks)
        for inst in range(3):
            h, J = random_pairwise(S, rng, graph=graph, scale_h=0.5, scale_J=1.0)
            E = pairwise_energy(S, h, J)
            best = None
            for a in local_minima(S, E, strict=True):
                b = exit_target(S, E, a)
                if b is None:
                    continue
                H = barrier_from(S, E, a)[b] - E[a]
                if best is None or H > best[0]:
                    best = (H, a, b)
            if best is None:
                continue
            H, a, b = best
            print(f"  {name} inst {inst}: a={a} b={b} d_H(a,b)={(S.cfg[a] != S.cfg[b]).sum()}")
            rows = [analyse(S, E, beta, a, b, name) for beta in (1.0, 2.0, 4.0, 8.0)]
            show(rows); allrows += rows
    # global sanity: all inequalities
    # The hitting-time identities involve h-values of order pi(a)/pi_max; float64 cannot resolve them when
    # that ratio is below ~1e-9.  Those cases are counted separately (see t5b_scaling_highprec.py, part A,
    # for a 60-digit recomputation of the identity in such a regime).
    illcond = [r for r in allrows if r["cond"] < 1e-9]
    bad = [r for r in allrows if not (r["lam_over_kcut"] <= 1 + 1e-9 and r["Epi_kcut"] >= 1 - 1e-9 and r["surv_ok"]
                                      and r["kcert_over_kcut"] >= 1 - 1e-9 and r["gap_over_gapcut"] <= 1 + 1e-9
                                      and r["cap_over_cut"] <= 1 + 1e-9 and r["cap_over_nw"] <= 1 + 1e-9
                                      and r["cap_over_nwc"] <= 1 + 1e-9 and r["path1_over_cap"] <= 1 + 1e-9
                                      and r["pathK_over_cap"] <= 1 + 1e-9 and r["Enu_over_lb"] >= 1 - 1e-9
                                      and r["ident_spec"] < 1e-6
                                      and (r["ident_hit"] < 1e-6 or r["cond"] < 1e-9))]
    print(f"T5 summary: {len(allrows)} (system, beta) cases; violations of any inequality or of a "
          f"well-conditioned identity: {len(bad)}")
    print(f"   hitting-time identity: {sum(1 for r in allrows if r['cond'] >= 1e-9)} well-conditioned cases, "
          f"max defect {max(r['ident_hit'] for r in allrows if r['cond'] >= 1e-9):.1e}; "
          f"{len(illcond)} ill-conditioned cases (pi(a)/pi_max < 1e-9), float64 defects "
          f"{[float('%.1e' % r['ident_hit']) for r in illcond]}")
    print(f"   ranges: lam/kcut [{min(r['lam_over_kcut'] for r in allrows):.3f}, {max(r['lam_over_kcut'] for r in allrows):.3f}]"
          f"  Epi*kcut [{min(r['Epi_kcut'] for r in allrows):.3f}, {max(r['Epi_kcut'] for r in allrows):.3f}]"
          f"  gap/gapcut [{min(r['gap_over_gapcut'] for r in allrows):.3f}, {max(r['gap_over_gapcut'] for r in allrows):.3f}]"
          f"  cap/cut [{min(r['cap_over_cut'] for r in allrows):.3f}, {max(r['cap_over_cut'] for r in allrows):.3f}]"
          f"  cap/NW [{min(r['cap_over_nw'] for r in allrows):.4f}, {max(r['cap_over_nw'] for r in allrows):.3f}]"
          f"  1path/cap [{min(r['path1_over_cap'] for r in allrows):.4f}, {max(r['path1_over_cap'] for r in allrows):.3f}]"
          f"  Kpath/cap [{min(r['pathK_over_cap'] for r in allrows):.4f}, {max(r['pathK_over_cap'] for r in allrows):.3f}]")
    for r in bad:
        print("   VIOLATION:", r)


if __name__ == "__main__":
    main()
