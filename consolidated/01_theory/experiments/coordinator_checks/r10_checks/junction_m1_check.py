# Coordinator's own check of referee R10, finding M1 (junction with the uniform cube), using the harness helpers.
import sys, math, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location("fc", __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "..", "..", "falsify_conjectures.py"))
fc = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(fc)

def bstar(e, u):
    rho = (math.log(2 / (1 + math.exp(-u))) + e) / u
    c2 = 1 / (2 * rho * (1 - rho)) - 2
    L = math.log((1 - rho) / rho)
    return 1 + u * c2 / (2 * L), rho

def well(bJ):
    # magnetisation m = tanh(bJ m), kappa_w = (1 - m)/2
    m = 1.0
    for _ in range(2000):
        m = math.tanh(bJ * m)
    return (1 - m) / 2

def Ifun(bJ):
    kw = well(bJ)
    hb = lambda k: 0.0 if k <= 0 or k >= 1 else -(k * math.log(k) + (1 - k) * math.log(1 - k))
    raw = lambda k: -(bJ / 2) * (2 * k - 1) ** 2 - hb(k)
    c = raw(kw)
    return (lambda k: raw(k) - c), kw

for (u, efrac, f) in ((8.0, ("abs", 0.0), 0.99), (4.0, ("ec", 0.6), 0.99), (1.0, ("abs", 0.0), 0.99), (2.0, ("abs", 0.0), 0.99)):
    Lam1 = math.log(2 / (1 + math.exp(-u)))
    ec = -Lam1                      # accuracy at which rho = 0  (e_c = -Lambda_1)
    e = efrac[1] if efrac[0] == "abs" else efrac[1] * ec
    bs, rho = bstar(e, u)
    bJ = 1 + f * (bs - 1)
    I, kw = Ifun(bJ)
    pu = 1 / (1 + math.exp(u))
    KLu = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
    Eunif = math.log(math.cosh(u / 2))
    lhs = u * (0.5 - min(pu, kw)) + I(kw)
    rhs = e + KLu + I(0.5)
    Ru = fc.mf_R_unif(e, u)
    print(f"u={u} e={e:.5f} bJ*={bs:.4f} bJ={bJ:.4f} kappa_w={kw:.3e} p_u={pu:.3e} I(1/2)={I(0.5):.5f} E_unif-e={Eunif-e:.5f}")
    print(f"   constant exit at the well: u dist + I = {lhs:.5f}  vs  e + alpha = {rhs:.5f}  feasible={lhs <= rhs}   R_unif(e)={Ru:.7f}")
    M = fc.mf_model(bJ, 0.0, u, K=400001)
    half = np.array([0.5, 0.5]); mu = np.array([1 - pu, pu])
    val = fc.mf_r(M, half, mu, e, G=3000)
    print(f"   harness solver r_mu*(e) = {val:.7f}")
    # best symmetric binary shell (1/2; x, x): scan
    best = (0, None)
    for x in np.linspace(0.005, 0.2, 40):
        v = fc.mf_r(M, half, np.array([1 - x, x]), e, G=1200)
        if v > best[0]: best = (v, x)
    print(f"   best symmetric shell on a coarse scan: value {best[0]:.6f} at x = {best[1]}")
