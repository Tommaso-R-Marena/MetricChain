"""N1: single-letter formulas against the printed numbers of theory report §11.20 and against each other."""
import numpy as np, sys
from sl import *
np.set_printoptions(precision=6, suppress=True)
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)

P("== (1) closed form of Thm 11.59(b) against the exact 2x2 game value ==")
rng = np.random.default_rng(1)
worst = 0
for _ in range(2000):
    p = rng.uniform(0.02, 0.98); u = rng.uniform(0.1, 4); g = rng.uniform(-u, u); t = rng.uniform(0.01, 0.99)
    worst = max(worst, abs(F_game(p,u,g,t) - F_closed(p,u,g,t)))
P("max |F_game - F_closed| over 2000 random (p,u,gamma,t):", worst)

P("\n== (2) F*(t): Sibson form (max over M) against max over gamma of the game; Renyi-centre check ==")
worst = 0; worstQ = 0
for _ in range(300):
    p = rng.uniform(0.03, 0.97); u = rng.uniform(0.2, 3.5); t = rng.uniform(0.02, 0.98)
    v1, m, Q, gs = Fstar(p,u,t,return_all=True)
    v2, g2 = Fstar_via_gamma(p,u,t)
    worst = max(worst, abs(v1-v2)); worstQ = max(worstQ, abs(gs-g2))
P("max |F*_Sibson - max_gamma F|:", worst, "  max |gamma*(centre) - argmax gamma|:", worstQ)

P("\n== (3) table of §11.20 (u = 2): theta, R_0(0+), R^max(0+), gamma*, a ==")
P("printed: theta  0: .0973 .0973 0 .3278 | 0.5: .0929 .0938 -.170 .3162 | 1: .0811 .0839 -.330 .2836 | 2: .0487 .0542 -.583 .1841 | 3: .0230 .0272 -.734 .0928")
u = 2.0
for theta in (0, 0.5, 1, 2, 3):
    p = 1/(1+np.exp(theta))
    r0 = R_gamma(p,u,0.0,0.0)
    r0c = R0_closed(p,u,0.0)
    rm, t, m, Q, g = Rmax(p,u,0.0,return_all=True)
    a, ma = a_capacity(p,u)
    P(f"theta={theta:4.1f} p={p:.5f}  R_0(0)={r0:.4f} (closed max_m: {r0c:.4f})  R^max(0)={rm:.4f}  gamma*={g:+.3f}  a={a:.4f}   [t*={t:.4f}, m*={m:.4f}]")

P("\n== (4) numbers quoted in §11.20: p=0.1,u=2,eps1=0.3E: R_0=0.019497, R^max=0.023270 ==")
p,u = 0.1,2.0
E = E_threshold(p,u)
P("E =", E, " R_0(0.3E) =", R_gamma(p,u,0.0,0.3*E), " R^max(0.3E) =", Rmax(p,u,0.3*E))
P("theta_na at (0.1,2,0.05E),(0.1,2,0.25E),(0.3,1,0.25E): printed 0.1020, 0.0440, 0.0243")
for (p,u,f) in ((0.1,2,0.05),(0.1,2,0.25),(0.3,1,0.25)):
    E = E_threshold(p,u)
    P("   ", p,u,f, "E=%.6f"%E, "theta_na = %.4f"%theta_na(p,u,f*E)[0])
P("§11.26 table, site 'bin' (pi=(0.7,0.3), u=1): printed E=0.103131 a=0.095301 h=0.025034 R(0.3E)=0.012209 theta_na(0.3E)=0.019941")
p,u = 0.3,1.0
E = E_threshold(p,u)
P("    E=%.6f a=%.6f h=%.6f R(0.3E)=%.6f theta_na(0.3E)=%.6f" % (E, a_capacity(p,u)[0], Rmax(p,u,0.0), Rmax(p,u,0.3*E), theta_na(p,u,0.3*E)[0]))

P("\n== (5) pair identity theta_na(e + R^max(e)) = R^max(e) ==")
for (p,u) in ((0.1,2.0),(0.3,1.0),(0.5,1.0)):
    E = E_threshold(p,u)
    for f in (0.1,0.3,0.6):
        e = f*E; r = Rmax(p,u,e)
        P(f"   p={p} u={u} e={f}E: R^max={r:.8f}  theta_na(e+R)={theta_na(p,u,e+r)[0]:.8f}")

P("\n== (6) constant-composition exponent: dual form vs primal; max over m equals R_gamma ==")
worst=0; worst2=0
for _ in range(40):
    p = rng.uniform(0.05,0.95); u = rng.uniform(0.3,3); g = rng.uniform(-0.8*u,0.8*u)
    E0 = F_game(p,u,g,1e-6)/1e-6
    e = rng.uniform(0,0.8)*E0
    m = rng.uniform(0.1,0.9)
    d1 = Rcc(p,u,g,m,e); d2 = Rcc_primal(p,u,g,m,e)
    worst = max(worst, abs(d1-d2))
    best,_ = max(((Rcc(p,u,g,mm,e),mm) for mm in np.linspace(0.01,0.99,99)))
    worst2 = max(worst2, R_gamma(p,u,g,e)-best)
P("max |Rcc_dual - Rcc_primal| (40 random):", worst)
P("max [R_gamma - max_m(grid 99) Rcc] (should be >= 0 and small):", worst2)
open('out/t01_single_letter.txt','w').write('\n'.join(out)+'\n')
