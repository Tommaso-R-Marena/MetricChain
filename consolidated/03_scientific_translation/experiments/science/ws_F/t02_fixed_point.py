"""N2 (light version after the first run hit the 30-minute limit: gamma-scan of 41 points + refinement): Augustin's fixed point at the saddle; is the hardest additive instance self-consistent?
   i.e. does the output law M*W of the vertex channel equal the Renyi centre Q* ?"""
import numpy as np
from sl import *
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)

P("columns: p u e/E | t* m* | Q*(1)=p_{gamma*} | Augustin sum_phi M* V_phi (1) [V_phi ∝ pi_phi^t Q*^(1-t)] | (M*W)(1) | gap (M*W - Q*)(1) | m_forced(gamma*) | R^max | Rcc(gamma*, m_forced) | max_gamma Rcc(gamma, m_forced(gamma)) | loss %")
rows = []
for (p,u) in ((0.5,1.0),(0.5,2.0),(0.3,1.0),(0.1,2.0),(0.1,1.0),(0.05,3.0),(0.2,0.5),(0.02,2.0),(0.3,4.0)):
    E = E_threshold(p,u)
    for f in (0.0, 0.3, 0.6, 0.9):
        e = f*E
        R, t, m, Q, g = Rmax(p,u,e,return_all=True)
        _, p0, p1 = site_laws(p,u,0.0)
        V0 = p0**t * Q**(1-t); V0 /= V0.sum()
        V1 = p1**t * Q**(1-t); V1 /= V1.sum()
        aug = (1-m)*V0[1] + m*V1[1]
        mw = (1-m)*p0[1] + m*p1[1]
        mf = m_forced(p,u,g)
        rc = Rcc(p,u,g,mf,e)
        # additive bases only: maximise over gamma the constrained exponent
        gs = np.linspace(-u*0.999,u*0.999,41)
        vals = [Rcc(p,u,gg,m_forced(p,u,gg),e) for gg in gs]
        i = int(np.argmax(vals)); radd = vals[i]
        from scipy.optimize import minimize_scalar
        res = minimize_scalar(lambda gg: -Rcc(p,u,gg,m_forced(p,u,gg),e), bounds=(gs[max(i-1,0)], gs[min(i+1,40)]), method='bounded', options={'xatol':1e-6})
        radd = max(radd, -res.fun)
        P(f"{p:5.2f} {u:4.1f} {f:3.1f} | {t:.4f} {m:.5f} | {Q[1]:.6f} | {aug:.6f} | {mw:.6f} | {mw-Q[1]:+.6f} | {mf:.5f} | {R:.6f} | {rc:.6f} | {radd:.6f} | {100*(1-radd/R) if R>0 else 0:.3f}")
        rows.append((p,u,f,t,m,Q[1],aug,mw,mf,R,rc,radd))
P("\nAugustin identity |sum M* V_phi - Q*| max:", max(abs(r[6]-r[5]) for r in rows))
P("self-consistency gap |M*W - Q*|: zero iff p = 1/2:")
for r in rows:
    if r[2]==0.0: P(f"   p={r[0]} u={r[1]}: gap at e=0: {r[7]-r[5]:+.6f}")
open('out/t02_fixed_point.txt','w').write('\n'.join(out)+'\n')
