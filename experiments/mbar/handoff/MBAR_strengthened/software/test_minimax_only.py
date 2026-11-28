import numpy as np
import scipy
from scipy.optimize import minimize
from mbar_certified import *
from itertools import combinations
import json, time
rng=np.random.default_rng(20261128)
report={}
print('Python float64 reference checks; seed 20261128; NumPy',np.__version__,'SciPy',scipy.__version__,flush=True)
# graph hard-instance numerical divergence tests: exact category distributions (not simulated observations)
maxratio=0.; minvar=1.; maxcomp=0.
for j in range(1000):
    K=int(rng.integers(2,12)); s=rng.dirichlet(np.ones(K)); edges=list((i,i+1) for i in range(K-1)); edges+= [(i,j) for i,j in combinations(range(K),2) if j>i+1 and rng.random()<.25]
    w=rng.uniform(.01,1,len(edges)); W=np.zeros(K)
    for (i,k),z in zip(edges,w): W[i]+=z; W[k]+=z
    w*=.125/W.max(); P=np.zeros((K,K+len(edges))); P1=P.copy()
    for m,((i,k),z) in enumerate(zip(edges,w)): P[i,K+m]=P[k,K+m]=z
    P[np.arange(K),np.arange(K)]=1-P.sum(axis=1)
    c=np.zeros(K); c[0]=-1;c[-1]=1; V,g,R,L=variance_and_gradient(P,s,c); Q=null_space(np.ones((1,K))); v=Q@np.linalg.solve(Q.T@L@Q,Q.T@c); d=.5; theta=d*v/R
    for m,((i,k),z) in enumerate(zip(edges,w)):
        a=(s[i]*theta[i]+s[k]*theta[k])/(s[i]+s[k]); P1[i,K+m]=z*np.exp(a-theta[i]); P1[k,K+m]=z*np.exp(a-theta[k])
    P1[np.arange(K),np.arange(K)]=1-P1.sum(axis=1)
    mask=P>0; kl=np.sum(s[:,None]*np.where(mask,P1*np.log(np.divide(P1,P,out=np.ones_like(P),where=mask)),0)); bound=4*d*d/R
    maxratio=max(maxratio,kl/bound); minvar=min(minvar,V/R)
    assert kl<=bound+1e-10 and np.ptp(theta)<=d+1e-8 and V/R>=.75-1e-9
    _,_,R1,_=variance_and_gradient(P1,s,c); maxcomp=max(maxcomp,R1/R,R/R1); assert max(R1/R,R/R1)<=np.exp(d)+1e-8
report['minimax_construction']={'trials':1000,'max_KL_to_bound_ratio':maxratio,'min_corrected_variance_to_resistance':minvar,'max_resistance_ratio':maxcomp}
print(report['minimax_construction'],flush=True)
