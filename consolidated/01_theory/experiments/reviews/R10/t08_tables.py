"""spot checks of the tables of Sections 5.3, 6.5, 6.7 (two rows each) with own code."""
import time, sys
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
from r10tab import *
t0 = time.time()
which = sys.argv[1] if len(sys.argv) > 1 else "all"
if which in ("all", "53"):
    print("# Section 5.3 (u = 1): rows (bJ, bB) = (0.5, 0.3) and (1.0, 0.1)")
    for (bJ, bB, ref) in ((0.5, 0.3, dict(RH=0.023983, gam=0.2147, R0=0.022659, EH=0.099123, E0=0.095345, a=0.091019)),
                          (1.0, 0.1, dict(RH=0.027964, gam=0.2000, R0=0.020271, EH=0.115250, E0=0.090246, a=0.106465))):
        M = Model(bJ=bJ, bB=bB, u=1.0)
        RH, lH, mH = R_binary(M, 0.0)
        zero = lambda k: 0.0 * np.asarray(k, float)
        R0, l0, m0 = R_binary(M, 0.0, land=zero)
        fg = lambda g: -R_binary(M, 0.0, land=landscape_gamma(M, g), starts=[(lH[0], 1 - mH[0], mH[1])])[0]
        gs = np.linspace(-0.3, 0.9, 13)
        vals = [fg(g) for g in gs]
        i = int(np.argmin(vals))
        rg = optimize.minimize_scalar(fg, bounds=(gs[max(i - 1, 0)], gs[min(i + 1, 12)]), method='bounded', options={'xatol': 1e-5})
        EH, _ = E_threshold(M)
        E0, _ = E_threshold(M, land=zero)
        a, ma = a_cone(M, convex=True)
        Rc, mc = R_cone(M, 0.0, convex=True)
        print(f"  bJ={bJ} bB={bB}: R_H(0) {RH:.6f} [{fmt(lH, mH)}] (report {ref['RH']})   max_gamma R_gamma(0) {-rg.fun:.6f} at gamma* {rg.x:+.4f} (report {ref['gam']:+.4f})")
        print(f"       cone formula R_cone(0) {Rc:.6f} (m={mc:.4f})   R_0(0) {R0:.6f} (report {ref['R0']})   E_H {EH:.6f} (report {ref['EH']})   E_0 {E0:.6f} (report {ref['E0']})   a(cones) {a:.6f} at m={ma:.4f} (report {ref['a']})   t={time.time()-t0:.0f}", flush=True)
if which in ("all", "65"):
    print("# Section 6.5 (bJ = 1.5, B = 0, e = 0): rows u = 0.60, 0.30, 0.25")
    for (u, ref, starts) in ((0.60, dict(RH=0.00907144, x=0.3780, cone=0.00321748), None),
                             (0.30, dict(RH=0.00226457, x=0.4409, cone=0.00075446), [(0.5, 0.441, 0.441), (0.5, 0.445, 0.445), (0.5, 0.45, 0.45), (0.53, 0.91, 0.06)]),
                             (0.25, dict(RH=0.00052346, x=None, cone=0.00052067), [(0.537, 0.9085, 0.0576), (0.5, 0.9, 0.06), (0.5, 0.45, 0.45), (0.45, 0.93, 0.05)])):
        M = Model(bJ=1.5, bB=0.0, u=u)
        RH, lH, mH = R_binary(M, 0.0, starts=starts)
        # symmetric shells on a fine scan (the range of shells with a positive value can be narrow)
        xs = np.linspace(0.30, 0.499, 400)
        vs = np.array([r_mu(M, *binary(0.5, x, x), 0.0) for x in xs])
        j = int(np.argmax(vs))
        Rc, mc = R_cone(M, 0.0)
        s2 = inner_dual(M, lH, mH, alpha(M, lH, mH), nk=1601, refine=5)[0]
        print(f"  u={u}: contact {[(round(a,4), round(b,4)) for a,b in M.contact()]}  R2(0) {RH:.8f} [{fmt(lH, mH)}] S2 {s2:.8f} (report {ref['RH']}, x={ref['x']})   best symmetric shell on scan: x={xs[j]:.4f} {vs[j]:.8f}   cone formula {Rc:.8f} at m={mc:.4f} (report {ref['cone']})   R_unif {R_unif(0.0,u):.8f}  t={time.time()-t0:.0f}", flush=True)
if which in ("all", "67"):
    print("# Section 6.7 (u = 1, B = 0, e = 0.02): rows bJ = 1.2, 1.3; and the field at coexistence bB = 0.05, e = 0")
    def s3(lf, x):
        return np.array([(1 - lf) / 2, lf, (1 - lf) / 2]), np.array([1 - x, 0.5, x])
    for (bJ, ref) in ((1.2, dict(b=0.0189503, x=0.2769, cone=0.0176913, f=0.0192108, lf=0.034)), (1.3, dict(b=0.0175999, x=0.2875, cone=0.0108824, f=0.0181202, lf=0.072))):
        M = Model(bJ=bJ, bB=0.0, u=1.0)
        e = 0.02
        RH, lH, mH = R_binary(M, e)
        Rc, mc = R_cone(M, e)
        f = lambda z: -(r_mu(M, *s3(min(max(z[0], 1e-5), 0.9), min(max(z[1], 0.01), 0.49)), e))
        res = optimize.minimize(f, [ref['lf'], 0.27], method='Nelder-Mead', options={'xatol': 1e-9, 'fatol': 1e-14, 'maxiter': 800})
        l3, m3 = s3(*res.x)
        s2 = inner_dual(M, l3, m3, e + alpha(M, l3, m3), nk=1601, refine=5)[0]
        print(f"  bJ={bJ}: binary {RH:.8f} [{fmt(lH, mH)}] (report {ref['b']}, x={ref['x']})  cone formula {Rc:.8f} (report {ref['cone']})  free block {-res.fun:.8f} lf={res.x[0]:.4f} x={res.x[1]:.4f} S2 {s2:.8f} (report {ref['f']}, lf={ref['lf']})  R_unif {R_unif(e,1.0):.8f}  t={time.time()-t0:.0f}", flush=True)
    M = Model(bJ=1.5, bB=0.05, u=1.0)
    RH, lH, mH = R_binary(M, 0.0, starts=[(0.4761, 0.3260, 0.2707), (0.5, 0.3, 0.3), (0.45, 0.3, 0.3), (0.52, 0.28, 0.32)])
    zero = lambda k: 0.0 * np.asarray(k, float)
    R0, l0, m0 = R_binary(M, 0.0, land=zero, starts=[(0.5, 0.3, 0.3), (0.3, 0.2, 0.2), (0.8, 0.1, 0.5), (0.9, 0.05, 0.6), (0.7, 0.2, 0.4)])
    Rc, mc = R_cone(M, 0.0)
    s2 = inner_dual(M, lH, mH, alpha(M, lH, mH), nk=1601, refine=5)[0]
    print(f"  bJ=1.5 bB=0.05 e=0: contact {[(round(a,4), round(b,4)) for a,b in M.contact()]} binary {RH:.8f} (m; a, b) = ({lH[0]:.4f}; {1-mH[0]:.4f}, {mH[1]:.4f}) S2 {s2:.8f} (report 0.0250232 at (0.4761; 0.3260, 0.2707))  cone formula {Rc:.8f} (report 0.0115296)  zero residual {R0:.8f} [{fmt(l0, m0)}] (report 0.0075630)  t={time.time()-t0:.0f}", flush=True)
print("time", time.time() - t0)
