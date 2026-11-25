import math, numpy as np
from scipy.optimize import minimize_scalar
p,u,e=0.25,1.0,0.02
q=1-p
L0=-math.log(q+p*math.exp(-u)); L1=-math.log(p+q*math.exp(-u))
h=lambda x: 0.0 if x<=0 or x>=1 else -x*math.log(x)-(1-x)*math.log(1-x)
def val(m):
    Lm=(1-m)*L0+m*L1
    x=(Lm+e)/u
    return h(m)-h(x) if x<0.5 else -1.0   # the min over profiles: distance below the typical one
# closed form max_m [h(m)-h((Lam_m+e)/u)]_+
ms=np.linspace(1e-6,1-1e-6,2000001)
Lm=(1-ms)*L0+ms*L1
x=(Lm+e)/u
hh=lambda z: -z*np.log(z)-(1-z)*np.log(1-z)
v=hh(ms)-hh(x)
i=int(np.argmax(v)); print("closed form R_0(e) =",v[i],"at m =",ms[i], " x=",x[i])
# game form: max_t F(0,t) - t e
def F(g,t):
    return (-t*math.log(q+p*math.exp(-g))+math.log((1-math.exp(-t*(u+g)))*math.exp(-t*L0)+(1-math.exp(-t*(u-g)))*math.exp(-t*(L1+g)))-math.log(1-math.exp(-2*t*u)))
r=minimize_scalar(lambda t: -(F(0.0,t)-t*e),bounds=(1e-6,1),method='bounded',options=dict(xatol=1e-12))
print("game form   R_0(e) =",-r.fun,"at t =",r.x)
