"""
T6 — what does envelope uncertainty do to the rate bounds?  (brief, sketch 3(iv))

E_g = f + g, g admissible for the weighted Hamming envelope d(x,y) = sum_i c_i [x_i != y_i].
Dividing set A chosen from the KNOWN part f (component of a below the f-barrier to its exit target).
TST rate of the perturbed model (Metropolis, one proposal per neighbour per unit time):

    k(g) = sum_{x in A, y notin A, x~y} exp(-beta max(E_g(x), E_g(y))) / sum_{x in A} exp(-beta E_g(x)).

Quantities
  k_nom   = k(0)
  K_exact = sup_g k(g)                 exact, by a linear program (Charnes–Cooper) in the weights w = e^{-beta g}
  K_a     = pinned at the basin minimum a:   numerator with f - d(a,.),  denominator with f + d(.,a)
  K_gate  = sum over gateways y of deg_A(y) * sup_g pi_g(y)/pi_g(A)
          = sum_y deg_A(y) / sum_{x in A} exp(-beta (f(x) + d(x,y) - f(y)))      (each term exact: pinned at y)
  k(g_tilt), g_tilt = d(., A^c)        the "tilt towards the wall" candidate
Checks:  k(g) <= K_exact <= min(K_a, K_gate) for sampled admissible g;  the LP optimiser is admissible and
         attains K_exact;  lambda_A(g) <= k(g) (exact Dirichlet eigenvalue of the perturbed chain).
Reported: (1/beta) ln(K/k_nom) in energy units, against the envelope distance from a to the dominant gateway.

Run:  OMP_NUM_THREADS=1 python3 t6_robust_rates.py
"""
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
from kcore import (Space, barrier_from, random_pairwise, pairwise_energy, local_minima,
                   component_below, outer_boundary, generator, gibbs, dirichlet_eig,
                   random_admissible, is_admissible)

rng = np.random.default_rng(17)


def exit_target(S, E, a):
    Ba = barrier_from(S, E, a)
    lower = np.nonzero(E < E[a])[0]
    if len(lower) == 0:
        return None
    best = Ba[lower].min()
    cands = lower[Ba[lower] <= best + 1e-12]
    return int(cands[np.argmin(E[cands])])


def k_tst(S, E, beta, A, edges, ref):
    num = np.exp(-beta * (np.maximum(E[edges[:, 0]], E[edges[:, 1]]) - ref)).sum()
    den = np.exp(-beta * (E[A] - ref)).sum()
    return num / den


def crossing_edges(S, A):
    out = []
    for x in np.nonzero(A)[0]:
        for y in S.nbrs[x]:
            if not A[y]:
                out.append((int(x), int(y)))
    return np.array(out, dtype=np.int64)


def lp_sup(S, f, c, beta, A, edges, a):
    """sup over admissible g of k(g): maximise sum_e psi_e tau_e subject to
       psi_e tau_e <= phi_x w_x, psi_e tau_e <= phi_y w_y, sum_{x in A} phi_x w_x = 1,
       w_y <= exp(beta c_i) w_x for neighbours x~y differing at site i (both orientations).
       phi = exp(-beta (f - f(a)))."""
    N = S.N
    M = len(edges)
    phi = np.exp(-beta * (f - f[a]))
    psi = np.minimum(phi[edges[:, 0]], phi[edges[:, 1]]) * np.exp(beta * c.max())
    nv = N + M
    rows = []
    # cone constraints over neighbouring pairs
    ncone = sum(len(S.nbrs[x]) for x in range(N))
    Aub = lil_matrix((ncone + 2 * M, nv))
    bub = np.zeros(ncone + 2 * M)
    r = 0
    for x in range(N):
        for y, i in zip(S.nbrs[x], S.nbr_site[x]):
            Aub[r, y] = 1.0
            Aub[r, x] = -np.exp(beta * c[i])
            r += 1
    for e, (x, y) in enumerate(edges):
        Aub[r, N + e] = 1.0
        Aub[r, x] = -phi[x] / psi[e]
        r += 1
        Aub[r, N + e] = 1.0
        Aub[r, y] = -phi[y] / psi[e]
        r += 1
    Aeq = lil_matrix((1, nv))
    for x in np.nonzero(A)[0]:
        Aeq[0, x] = phi[x]
    cost = np.zeros(nv)
    scale = psi.max()
    cost[N:] = -psi / scale
    res = linprog(cost, A_ub=Aub.tocsr(), b_ub=bub, A_eq=Aeq.tocsr(), b_eq=[1.0],
                  bounds=[(0, None)] * nv, method="highs")
    assert res.status == 0, res.message
    w = res.x[:N]
    val = -res.fun * scale
    return val, w


def main():
    print("T6: robust TST bounds under a weighted Hamming envelope")
    print("    columns: beta | k_nom | (1/beta)ln(K/k_nom) for K = K_exact, K_gate, K_a, k(g_tilt) | "
          "d(a,y*) (envelope distance a -> dominant gateway) | max sampled ratio k(g)/K_exact | "
          "max lambda_A(g)/k(g)")
    nviol = 0
    ncheck = 0
    for name, ks, cval in (("binary n=8 chain+", [2] * 8, 0.15), ("binary n=8 chain+", [2] * 8, 0.4),
                           ("3-state n=5 chain+", [3] * 5, 0.15), ("3-state n=5 chain+", [3] * 5, 0.4)):
        S = Space(ks)
        for inst in range(3):
            h, J = random_pairwise(S, rng, graph="chain+", scale_h=0.5, scale_J=1.0)
            f = pairwise_energy(S, h, J)
            c = cval * rng.uniform(0.5, 1.5, S.n)
            D = S.hamming_env(c)
            best = None
            for a in local_minima(S, f, strict=True):
                b = exit_target(S, f, a)
                if b is None:
                    continue
                H = barrier_from(S, f, a)[b] - f[a]
                if best is None or H > best[0]:
                    best = (H, a, b)
            if best is None:
                continue
            H, a, b = best
            A = component_below(S, f, a, f[a] + H, strict=True)
            edges = crossing_edges(S, A)
            ob = outer_boundary(S, A)
            degA = np.array([A[S.nbrs[y]].sum() for y in range(S.N)])
            print(f"  {name}, c~{cval}, inst {inst}: H_f={H:.2f}, |A|={A.sum()}, |wall|={ob.sum()}, "
                  f"crossing edges={len(edges)}, sum c={c.sum():.2f}")
            for beta in (1.0, 2.0, 4.0):
                k_nom = k_tst(S, f, beta, A, edges, f[a])
                K_exact, w = lp_sup(S, f, c, beta, A, edges, a)
                g_opt = -np.log(np.maximum(w, 1e-300)) / beta
                adm = is_admissible(g_opt, D, tol=1e-6)
                k_at_opt = k_tst(S, f + g_opt, beta, A, edges, f[a] + g_opt[a])
                # pinned at a
                num = np.exp(-beta * (np.maximum((f - D[a, :])[edges[:, 0]], (f - D[a, :])[edges[:, 1]]) - f[a])).sum()
                den = np.exp(-beta * ((f + D[:, a])[A] - f[a])).sum()
                K_a = num / den
                # gateway bound
                K_gate = 0.0
                terms = []
                for y in np.nonzero(ob)[0]:
                    t = degA[y] / np.exp(-beta * (f[A] + D[A, y] - f[y])).sum()
                    terms.append((t, y))
                    K_gate += t
                ystar = max(terms)[1]
                # tilt candidate
                g_tilt = D[:, ~A].min(axis=1)
                assert is_admissible(g_tilt, D)
                k_tilt = k_tst(S, f + g_tilt, beta, A, edges, f[a])
                # sampling
                mx = 0.0
                mxlam = 0.0
                for s in range(25):
                    g = random_admissible(D, rng)
                    kg = k_tst(S, f + g, beta, A, edges, f[a])
                    mx = max(mx, kg / K_exact)
                    if s < 4:
                        Q = generator(S, f + g, beta)
                        pi = gibbs(f + g, beta)
                        lam = dirichlet_eig(Q, pi, A)[0]
                        mxlam = max(mxlam, lam / kg)
                for g in (g_tilt, -D[a, :], D[:, a], D[:, ystar], -D[ystar, :]):
                    mx = max(mx, k_tst(S, f + g, beta, A, edges, f[a]) / K_exact)
                ncheck += 1
                bad = (mx > 1 + 1e-6) or (K_exact > K_a * (1 + 1e-6)) or (K_exact > K_gate * (1 + 1e-6)) \
                    or (mxlam > 1 + 1e-9) or (not adm) or abs(k_at_opt / K_exact - 1) > 1e-5
                nviol += int(bad)
                print(f"    beta={beta:.0f} k_nom={k_nom:.3e} | exact {np.log(K_exact / k_nom) / beta:.3f}  "
                      f"gate {np.log(K_gate / k_nom) / beta:.3f}  pin-a {np.log(K_a / k_nom) / beta:.3f}  "
                      f"tilt {np.log(k_tilt / k_nom) / beta:.3f} | d(a,y*)={D[a, ystar]:.3f} | "
                      f"{mx:.4f} | {mxlam:.3f}"
                      f"{'' if adm and abs(k_at_opt / K_exact - 1) < 1e-5 else '   [LP optimiser check FAILED]'}")
    print(f"T6 summary: {ncheck} (instance, beta) cases, violations: {nviol}")


if __name__ == "__main__":
    main()
