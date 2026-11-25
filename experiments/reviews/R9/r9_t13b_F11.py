# R9 test 13b: Proposition F11(a).  For a product sampler Bernoulli(r)^n the formula of the proposition,
#   theta_na^(r)(x) = max_m min{ D(P_X|S || r | P_S) : D(P_X|S || pi_s | P_S) <= x },
# is maximised at a CONSTANT centre (m = 0 or m = 1): objective and constraint are both linear in m for fixed
# conditional laws, so inner(m) <= m phi_1(x) + (1-m) phi_0(x) <= max(phi_0, phi_1), where
#   phi_0 = min{KL(y||r) : KL(y||eta_0) <= x},  phi_1 = min{KL(z||1-r) : KL(z||eta_1) <= x}.
# The report's table was computed with m restricted to [0.005, 0.995] and is slightly too small.
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from r9lib import Par, kl
def phi(x, eta, r):
    """min{KL(y||r) : KL(y||eta) <= x}"""
    if float(kl(r, eta)) <= x: return 0.0
    if r > eta: y = brentq(lambda y: float(kl(y, eta)) - x, eta, 1 - 1e-15)
    else: y = brentq(lambda y: float(kl(y, eta)) - x, 1e-15, eta)
    return float(kl(y, r))
for (p, u, f, rep) in [(0.1, 2.0, 0.05, (.1020, .1046, .186, .2729)), (0.1, 2.0, 0.25, (.0440, .0470, .168, .1420)), (0.3, 1.0, 0.25, (.0243, .0247, .319, .0347))]:
    P = Par(p, u); x = f * P.E()[0]
    val = lambda r: max(phi(x, P.eta0, r), phi(x, P.eta1, 1 - r))
    rs = np.linspace(0.005, 0.995, 1981); v = np.array([val(r) for r in rs]); i = int(np.argmin(v))
    rr = minimize_scalar(val, bounds=(rs[i - 1], rs[i + 1]), method='bounded', options={'xatol': 1e-10})
    print(f"p={p} u={u} x={f}E: type-uniform theta_na = {P.theta_na(x):.4f};  best single r: {min(rr.fun, v[i]):.4f} at r = {rr.x:.3f} (report: {rep[1]} at r = {rep[2]});  plain pi (r = p): {val(p):.4f} (report: {rep[3]})")
