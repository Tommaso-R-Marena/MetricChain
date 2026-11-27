"""Proposition T12: the Hubbard-Stratonovich representation of a ferromagnetic Curie-Weiss measure
as a mixture of fields, checked numerically (n = 10, 40); the tilt identity that absorbs a change
of the field into the residual; the grid of fields."""
import numpy as np
from scipy import integrate
from scipy.special import gammaln, logsumexp
rng = np.random.default_rng(3)
for (n, bJ, bB) in ((10, 1.5, 0.0), (10, 0.7, 0.3), (40, 1.5, 0.05)):
    t = np.arange(n + 1)
    Mg = 2 * t - n
    # Curie-Weiss weight of ONE configuration of type t: exp((bJ/2n) M^2 + bB M)
    lw = (bJ / (2 * n)) * Mg ** 2 + bB * Mg
    lbin = gammaln(n + 1) - gammaln(t + 1) - gammaln(n - t + 1)
    lZ = logsumexp(lw + lbin)
    pi_pt = np.exp(lw - lZ)                                   # pi(x) for |x| = t
    # mixture: nu(dy) prop. to exp(-n[y^2/(2bJ) - ln 2cosh(y+bB)]) dy,  Ber(p_y)^n(x) = exp((y+bB)M)/(2cosh(y+bB))^n
    g = lambda y: -n * (y * y / (2 * bJ) - np.log(2 * np.cosh(y + bB)))
    Y = 12.0
    norm = integrate.quad(lambda y: np.exp(g(y) - g(0)), -Y, Y, limit=400, epsabs=0, epsrel=1e-13)[0]
    mix = np.array([integrate.quad(lambda y: np.exp(g(y) - g(0)) * np.exp((y + bB) * m - n * np.log(2 * np.cosh(y + bB))), -Y, Y, limit=400, epsabs=0, epsrel=1e-13)[0] / norm for m in Mg])
    print(f"n={n} bJ={bJ} bB={bB}: max relative error of  pi(x) = int nu(dy) Ber(p_y)^n(x)  over the types: {np.max(np.abs(mix / pi_pt - 1)):.2e}")
# tilt identity on the full cube n = 10: A_y(psi) = C * A_{y0}(psi - 2(y - y0)|x|), psi - 2(y-y0)|x| in L_{u+2|y-y0|}
n = 10
N = 1 << n
wt = np.array([bin(x).count('1') for x in range(N)])
x = np.arange(N)
d = np.zeros((N, N), dtype=np.int8)
xx = x[:, None] ^ x[None, :]
for b in range(n):
    d += ((xx >> b) & 1).astype(np.int8)
u = 1.0
a = rng.normal(0, 2, size=N)
psi = np.min(a[None, :] + u * d, axis=1)                      # a member of L_u
bB = 0.1
def A(y, f):
    lp = (y + bB) * (2 * wt - n) - n * np.log(2 * np.cosh(y + bB))
    return np.sum(np.exp(lp - f))
y0, y = 0.3, 0.34
C = np.exp(-(y - y0) * n) * (np.cosh(y0 + bB) / np.cosh(y + bB)) ** n
lhs = A(y, psi)
rhs = C * A(y0, psi - 2 * (y - y0) * wt)
psi2 = psi - 2 * (y - y0) * wt
lipc = np.max(np.abs(psi2[:, None] - psi2[None, :]) / np.maximum(d, 1))
print(f"tilt identity: A_y(psi) / [C A_y0(psi - 2(y-y0)|x|)] - 1 = {lhs / rhs - 1:.2e};  Lipschitz constant of the tilted residual {lipc:.4f} <= u + 2|y-y0| = {u + 2*abs(y-y0):.4f}")
# |d/dy ln A_y| <= 2n
ys = np.linspace(-2, 2, 81)
der = np.gradient(np.log([A(yy, psi) for yy in ys]), ys)
print(f"max |d/dy ln A_y(psi)| on [-2,2] = {np.max(np.abs(der)):.3f} <= 2n = {2*n}")
