"""Check of the tilt inequality (Proposition C) by exhaustive enumeration, and of the derivative formula.

If psi' in L_u has the same one-body marginals as the additive instance psi_gamma, then for every real lambda
    ln A^(lam)(psi') - ln A^(lam)(psi_gamma) >= ln A(psi') - ln A(psi_gamma) - n c_gamma(lam),
where A^(lam) uses the reference Bern(p^(lam))^n, logit p^(lam) = logit p + lam, c_gamma(lam) = ln(1-p_g+p_g e^lam) - lam p_g.
Matched alternatives: additive base + mixture of cyclically symmetrised dips of two centre types whose excess
densities bracket p_gamma (exact linear equation).  Control: an unmatched alternative (one centre type) violates it.
"""
import numpy as np, sys
from sl import *
from prof import c_tilt
from t03_enum_adaptive import cube, popcount, in_class, marginals, rot
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()

def run(n, p, u, g, r):
    q = 1 - p
    X, bits, wt = cube(n)
    pi = p ** wt * q ** (n - wt)
    w = np.exp(-g * wt)                      # the additive instance itself (not normalised)
    wn = w / (pi * w).sum()
    pg = pgam(p, g)
    def symexc(k):
        s0 = (1 << k) - 1
        exc = np.zeros(2 ** n)
        orb = sorted(set(rot(s0, j, n) for j in range(n)))
        for s in orb:
            c = np.exp(-u * popcount(X ^ s)); c /= (pi * c).sum()
            exc += np.maximum(np.exp(r) * c - wn, 0.0) / len(orb)
        E = (pi * exc).sum(); return exc, E, (pi * exc * wt).sum() / (n * E)
    stats = [symexc(k) for k in range(1, n)]
    pair = None
    for i in range(len(stats) - 1):
        if stats[i][2] <= pg <= stats[i + 1][2]:
            pair = (i, i + 1)
    if pair is None:
        P(f"n={n} p={p} u={u} gamma={g}: no bracketing pair at depth {r}"); return
    (eA, EA, cA), (eB, EB, cB) = stats[pair[0]], stats[pair[1]]
    lam_mix = EB * (cB - pg) / (EA * (pg - cA) + EB * (cB - pg))
    alt = wn + lam_mix * eA + (1 - lam_mix) * eB
    m0, A0 = marginals(pi, wn, bits); m1, A1 = marginals(pi, alt, bits)
    ok, _ = in_class(alt, n, u)
    P(f"--- n={n} p={p} u={u} gamma={g} depth r={r}: centre types {pair[0]+1},{pair[1]+1} (excess densities {cA:.5f} <= p_gamma={pg:.5f} <= {cB:.5f}), mixing weight {lam_mix:.4f}")
    P(f"    matched alternative in class: {ok}; max |marginal(alt) - p_gamma| = {np.abs(m1-pg).max():.2e}; ln A(alt)/A(base) = {np.log(A1/A0):.6f}")
    # unmatched control: single type A
    altU = wn + eB
    worst = np.inf; worstU = np.inf
    for lam in np.linspace(-3, 3, 121):
        pl = 1 / (1 + np.exp(-(np.log(p / q) + lam)))
        pil = pl ** wt * (1 - pl) ** (n - wt)
        lhs = np.log((pil * alt).sum() / (pil * wn).sum())
        rhs = np.log(A1 / A0) - n * c_tilt(p, g, lam)
        worst = min(worst, lhs - rhs)
        lhsU = np.log((pil * altU).sum() / (pil * wn).sum())
        rhsU = np.log((pi * altU).sum() / A0) - n * c_tilt(p, g, lam)
        worstU = min(worstU, lhsU - rhsU)
    P(f"    min over lambda in [-3,3] of (LHS - RHS): matched {worst:+.3e} (>= 0 required);  unmatched control {worstU:+.3e} (negative = violated)")

for (n, p, u, g, r) in ((12, 0.2, 1.0, 0.0, 1.0), (12, 0.1, 2.0, 0.0, 1.5), (14, 0.3, 1.0, 0.0, 0.8), (12, 0.3, 1.5, 0.4, 1.0), (10, 0.5, 1.0, 0.0, 1.0)):
    run(n, p, u, g, r)

P("\nderivative of the tilt bound at lambda=0 (zero residual): d/dlam R_0(e - c(lam); theta - lam) = -dR_0/dtheta; finite differences")
for (p, u, fr) in ((0.3, 1.0, 0.2), (0.1, 2.0, 0.2), (0.5, 1.0, 0.2)):
    E0 = F_game(p, u, 0.0, 1e-6) / 1e-6; e = fr * E0
    def val(lam):
        pl = 1 / (1 + np.exp(-(np.log(p / (1 - p)) + lam)))
        return R_gamma(pl, u, 0.0, e - c_tilt(p, 0.0, lam))
    d = (val(1e-4) - val(-1e-4)) / 2e-4
    P(f"   p={p} u={u} e={fr}E_0: R_0={val(0):.6f}, derivative in lambda at 0 = {d:+.6f}")
open('out/t09_tilt_check.txt', 'w').write('\n'.join(out) + '\n')
