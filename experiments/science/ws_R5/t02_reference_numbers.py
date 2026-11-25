"""
t02_reference_numbers.py -- replication of the reference numbers of THY-MSG-0011 section 1(c) and of the table
"A worked example" of theory report section 11.26, with r5lib (own implementation).

For every chain:  E, a (with duality brackets), h = R^(0), R^(0.3E), theta_na(0.3E) [two ways], zero residual R_0(0).
For the three-state sites: best two-state coarse-graining and best two-state deletion at e = 0.
"""
import time
import numpy as np
from r5lib import *
from t01_identity import sites_example

np.set_printoptions(precision=6, suppress=True, linewidth=150)

THEIRS = {  # chain: (E, a, h, R(0.3E), theta_na(0.3E), R_0(0), cut, pair)
    "bin":  (0.103131, 0.095301, 0.025034, 0.012209, 0.019941, None, None, None),
    "path": (0.400622, 0.294791, 0.089589, 0.043375, 0.066899, 0.080032, 0.048586, 0.115369),
    "tri":  (0.284907, 0.247541, 0.066729, 0.032077, 0.051124, 0.065233, 0.053168, 0.094950),
    "asym": (0.191059, 0.166046, 0.045407, 0.022108, 0.035544, 0.033856, 0.024685, 0.058646),
    "mix":  (0.251877, 0.195046, 0.057275, 0.027759, 0.043288, 0.052360, None, None),
    "mix2": (0.212197, 0.186645, 0.050050, 0.024122, 0.038641, 0.049065, None, None),
}


def F0_chain(chain, t):
    """sum_j lambda_j F_j(0, t): the game function of the ZERO residual, by linear programming."""
    if t <= 0:
        return 0.0
    return sum(l * F_game(s, np.zeros(s.q), t)[0] for l, s in chain.parts)


def h_binary(pi2, u12, u21):
    s = Site(pi2, [[0, u12], [u21, 0]])
    return Rhat(lambda t: Fstar_site(s, t), 0.0, ngrid=200)[0]


if __name__ == "__main__":
    t0 = time.time()
    S = sites_example()
    chains = {
        "bin": Chain([(1.0, S["bin"])], "bin"),
        "path": Chain([(1.0, S["path"])], "path"),
        "tri": Chain([(1.0, S["tri"])], "tri"),
        "asym": Chain([(1.0, S["asym"])], "asym"),
        "mix": Chain([(0.5, S["bin"]), (0.5, S["path"])], "mix"),
        "mix2": Chain([(0.4, S["bin"]), (0.6, S["tri"])], "mix2"),
    }
    print("chain | quantity | mine | theirs | diff")
    maxdiff = 0.0
    for nm, ch in chains.items():
        Elo = sum(l * threshold_E(s)[0] for l, s in ch.parts)
        Ehi = sum(l * threshold_E(s)[1] for l, s in ch.parts)
        alo = sum(l * capacity_a(s)[0] for l, s in ch.parts)
        ahi = sum(l * capacity_a(s)[1] for l, s in ch.parts)
        E = Elo
        h, th = Rhat(ch.Fstar, 0.0)
        R3, t3 = Rhat(ch.Fstar, 0.3 * E)
        na_d, tau = theta_na_direct(ch.Fstar, 0.3 * E)
        na_p, e_p = theta_na_pair(ch.Fstar, 0.3 * E)
        R0, t00 = _r0 = Rhat(lambda t: F0_chain(ch, t), 0.0, ngrid=200)
        gapmax = max(Fstar_gap(s, t) for l, s in ch.parts for t in (th, t3, tau))
        mine = [E, alo, h, R3, na_d, R0]
        names = ["E", "a", "h=R(0)", "R(0.3E)", "theta_na(0.3E)", "R_0(0)"]
        for k, (nme, val) in enumerate(zip(names, mine)):
            ref = THEIRS[nm][k]
            if ref is None:
                print(f"{nm:5s} {nme:15s} {val:.6f}   (no reference value)")
            else:
                maxdiff = max(maxdiff, abs(val - ref))
                print(f"{nm:5s} {nme:15s} {val:.6f}   {ref:.6f}   {val-ref:+.1e}")
        print(f"{nm:5s}   brackets: E in [{Elo:.9f}, {Ehi:.9f}], a in [{alo:.9f}, {ahi:.9f}], largest duality gap of F* at the "
              f"three optimal slopes {gapmax:.1e}")
        print(f"{nm:5s}   t*(0)={th:.4f}  t*(0.3E)={t3:.4f}  tau*(theta_na)={tau:.4f};  theta_na via R^(S^-1(x)) = {na_p:.9f} "
              f"(direct sup: {na_d:.9f}, diff {na_p-na_d:+.1e}), S^-1(0.3E) = {e_p:.6f}")
        # hardest instance at e -> 0
        for l, s in ch.parts:
            lo, M, hi = renyi_primal(s, th)
            Qc = centre_of(s, M, th)
            g = -np.log(Qc / s.pi)
            g -= g[0]
            print(f"{nm:5s}   site {s.name}: centre law {np.round(Qc, 4)}, gamma* {np.round(g, 4)}, M* {np.round(M, 4)} on vertices "
                  f"{[tuple(np.round(v, 2)) for v, m in zip(s.V, M) if m > 1e-6]}")
    print(f"largest |mine - theirs| over the table: {maxdiff:.1e}  (their table is rounded to 6 decimals)")
    print()
    print("== three-state sites: best two-state coarse-graining / best deletion at e = 0 ==")
    for nm in ("path", "tri", "asym"):
        s = S[nm]
        cut, pair = [], []
        for a in range(3):
            rest = [b for b in range(3) if b != a]
            u12 = min(s.d[a, b] for b in rest)
            u21 = min(s.d[b, a] for b in rest)
            cut.append(h_binary([s.pi[a], 1 - s.pi[a]], u12, u21))
        for a in range(3):
            for b in range(a + 1, 3):
                p = np.array([s.pi[a], s.pi[b]])
                p /= p.sum()
                pair.append(h_binary(p, s.d[a, b], s.d[b, a]))
        print(f"{nm:5s} cut: mine {max(cut):.6f} theirs {THEIRS[nm][6]:.6f} ({max(cut)-THEIRS[nm][6]:+.1e});  "
              f"pair: mine {max(pair):.6f} theirs {THEIRS[nm][7]:.6f} ({max(pair)-THEIRS[nm][7]:+.1e})")
    print()
    print("== 'the exponents do not add' (chain mix): average at a common accuracy against R^ ==")
    ch = chains["mix"]
    E = ch.E()
    for fr, ref in ((0.3, 8.5), (0.5, 47), (0.7, 172), (0.9, 1365)):
        R = Rhat(ch.Fstar, fr * E)[0]
        avg = sum(l * Rhat(lambda t, s=s: Fstar_site(s, t), fr * E)[0] for l, s in ch.parts)
        print(f"e/E={fr}: R^={R:.6f}  average={avg:.6f}  excess={100*(avg/R-1):.1f} %   (theirs: +{ref} %)")
    print(f"[{time.time()-t0:.1f} s]")
