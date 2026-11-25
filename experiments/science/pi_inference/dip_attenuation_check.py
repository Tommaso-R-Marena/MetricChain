"""Check of the attenuation lemma behind Theorem 4-tau (INFERENCE_LIMITS_ADDENDA.md A10).

kappa_j(d) = K_j(d)/C(n,j)  (normalised Krawtchouk polynomial).
(L1) exact identity:  sum_d C(n,d) z^d kappa_j(d) = (1-z)^j (1+z)^(n-j)          (all z)
     hence for the full cone (z = e^-u):  ratio = tanh(u/2)^j  exactly.
(L2) dip of radius r:  S_j = sum_{d<r} C(n,d) (e^{u(r-d)} - 1) kappa_j(d).  Claim:
         | S_j / S_0 - tanh(u/2)^j |  <=  2 (eta + V/A) / (1 - eta - V/A),
     eta = P(Bin(n, p_u) >= r),  V = sum_{d<r} C(n,d),  A = e^{ur} (1+e^-u)^n,
     uniformly in j >= 1.  Exact rational arithmetic for kappa; high-precision floats for the sums.
"""
import math
from fractions import Fraction
from mpmath import mp, mpf, exp, tanh, binomial, log
mp.dps = 60

def kappa_table(n, jmax):
    """kappa_j(d) for j <= jmax, d = 0..n, exact, via the recurrence in j:
       (j+1) K_{j+1}(d) = (n - 2d) K_j(d) - (n - j + 1) K_{j-1}(d)."""
    K = [[1]*(n+1), [n - 2*d for d in range(n+1)]]
    for j in range(1, jmax):
        K.append([((n - 2*d)*K[j][d] - (n - j + 1)*K[j-1][d])//(j+1) for d in range(n+1)])
    return [[Fraction(K[j][d], math.comb(n, j)) for d in range(n+1)] for j in range(jmax+1)]

def run(n, u, jmax=14):
    kap = kappa_table(n, jmax)
    z = exp(-mpf(u)); pu = 1/(1+exp(mpf(u)))
    # (L1)
    worst1 = mpf(0)
    for j in range(1, jmax+1):
        lhs = sum(binomial(n, d)*z**d*mpf(kap[j][d].numerator)/kap[j][d].denominator for d in range(n+1))
        rhs = (1-z)**j*(1+z)**(n-j)
        worst1 = max(worst1, abs(lhs/rhs - 1))
    # sensitive radius: least r with 2^-n S_0 >= 1  (ln Z changes by ln 2)
    r = None
    for rr in range(1, n):
        S0 = sum(binomial(n, d)*(exp(u*(rr-d)) - 1) for d in range(rr))
        if S0 >= mpf(2)**n: r = rr; break
    S0 = sum(binomial(n, d)*(exp(u*(r-d)) - 1) for d in range(r))
    eta = sum(binomial(n, d)*pu**d*(1-pu)**(n-d) for d in range(r, n+1))
    V = sum(binomial(n, d) for d in range(r)); A = exp(mpf(u)*r)*(1+z)**n
    bound = 2*(eta + V/A)/(1 - eta - V/A)
    worst2 = mpf(0)
    for j in range(1, jmax+1):
        Sj = sum(binomial(n, d)*(exp(u*(r-d)) - 1)*mpf(kap[j][d].numerator)/kap[j][d].denominator for d in range(r))
        dev = abs(Sj/S0 - tanh(mpf(u)/2)**j)
        worst2 = max(worst2, dev)
        assert dev <= bound, (n, u, j, dev, bound)
    print(f"n={n:4d} u={u}: (L1) max relative defect {float(worst1):.1e}; sensitive radius r={r} (rho={r/n:.4f}, p_u={float(pu):.4f}); "
          f"(L2) max_j |S_j/S_0 - tanh^j| = {float(worst2):.2e} <= bound {float(bound):.2e}  [eta={float(eta):.1e}, V/A={float(V/A):.1e}]")

for n in (100, 200, 400, 800):
    for u in (1.0, 2.0):
        run(n, u)
