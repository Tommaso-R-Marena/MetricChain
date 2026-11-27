"""t04: the non-adaptive exponent theta_na(eps1) = max_m min{ I : Icone_m <= eps1 } and the identity
theta_na(e + theta_H(e)) = theta_H(e), theta_H = hinted exponent of the hardest instance."""
import math, numpy as np, time
from flib import *
t0 = time.time()

def theta_na_uniform(u, e1):
    pu = 1 / (1 + math.exp(u))
    if e1 >= kls(0.5, pu):
        return 0.0
    lo, hi = pu, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if kls(mid, pu) <= e1 else (lo, mid)
    return kls(lo, 0.5)

print("uniform case: max-min formula against min{KL(rho||1/2): KL(rho||p_u) <= eps1}")
for u in (0.5, 1.0, 2.0):
    st = Site(0.5, u)
    estar = math.log(math.cosh(u / 2))
    for frac in (0.01, 0.2, 0.5, 0.9):
        e = frac * estar
        v = maxmin_precise(st, "na", e)
        print(f"  u={u} eps1={e:.5f}: maxmin={v[0]:.8f} (m*={v[1]:.4f})  report={theta_na_uniform(u, e):.8f}")

print("biased case: identity theta_na(e + theta_H(e)) = theta_H(e); theta_na(e + R_0(e)) vs R_0(e)")
worst = 0.0
for p, u in ((0.3, 1.0), (0.1, 1.0), (0.1, 2.0), (0.05, 2.0), (0.2, 4.0), (0.02, 3.0)):
    st = Site(p, u)
    gs = np.linspace(-u, u, 401)
    E = max(thr_additive(p, u, g) for g in gs)
    # a = theta_na(0+) = max_m I(cone joint law)
    ms = np.linspace(1e-6, 1 - 1e-6, 200001)
    Ic = st.I(ms, st.eta1, st.eta0)
    a = float(Ic.max()); ma = float(ms[int(Ic.argmax())])
    print(f"p={p} u={u}: a = theta_na(0+) = max_m I_cone = {a:.6f} at m={ma:.4f};  class threshold E = {E:.6f}")
    for frac in (0.0, 0.1, 0.3, 0.6, 0.9):
        e = frac * E
        tH = maxmin_precise(st, "H", e)
        r0, _ = R_additive(p, u, 0.0, e)
        na_at = maxmin_precise(st, "na", e + tH[0])
        na_at0 = maxmin_precise(st, "na", e + r0)
        na_e = maxmin_precise(st, "na", max(e, 1e-9))
        worst = max(worst, abs(na_at[0] - tH[0]))
        print(f"   e={e:.5f}: theta_H={tH[0]:.8f}  theta_na(e+theta_H)={na_at[0]:.8f} (m*={na_at[1]:.4f}; H had m*={tH[1]:.4f})"
              f" | R_0={r0:.8f}  theta_na(e+R_0)={na_at0[0]:.8f} | theta_na(e)={na_e[0]:.6f} (m*={na_e[1]:.3f}, kappa*={na_e[4]:.3f})")
print("max |theta_na(e + theta_H(e)) - theta_H(e)| =", worst, " time", time.time() - t0)
