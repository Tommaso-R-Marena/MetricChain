import numpy as np
import scipy
from scipy.optimize import minimize
from mbar_certified import *
from itertools import combinations
import json, time
rng=np.random.default_rng(20261128)
report={}
print('Python float64 reference checks; seed 20261128; NumPy',np.__version__,'SciPy',scipy.__version__,flush=True)
# disconnection, tiny edge, invalid overlap
for O in [np.eye(2),np.array([[1-1e-15,1e-15],[1e-15,1-1e-15]])]:
    r=graph_diagnostic(O,[100,100]); assert r['status']=='FAIL_RANK' and r['graph_effective_overlap']==0 and np.isinf(r['R_max'])
try: graph_diagnostic([[.8,.2],[.1,.9]],[100,100]); raise AssertionError('expected invalid')
except ValueError: pass
assert graph_diagnostic([[.8,.2],[.2,.8]],[100,100])['status']=='DIAGNOSTIC_ONLY'
for U,labels in [(np.array([[0,np.inf],[np.inf,0]]),[0,1]),(np.array([[0,0],[np.inf,0]]),[0,1])]:
    try: solve(U,labels); raise AssertionError('expected no unique solution')
    except ValueError: pass
assert bridge_intervals(np.array([[0,np.inf],[np.inf,0]]),[0,1],[0,0])['status']=='PARTIAL_ABSTENTION'
print('PASS disconnected / tiny-rank / invalid-matrix / separated-solver / zero-bridge checks',flush=True)
# variance convexity / exact gradient / exact identity / perspective characterization numerical checks
max_grad=0.; max_jensen=0.; max_identity=0.; max_euler=0.
for _ in range(1500):
    K=int(rng.integers(2,9)); J=int(rng.integers(K,20)); P=rng.dirichlet(np.full(J,rng.uniform(.2,3)),size=K)
    c=rng.normal(size=K); c-=c.mean(); s=rng.dirichlet(np.ones(K))+0.03; t=rng.dirichlet(np.ones(K))+0.03; a=rng.random()
    V,g,R,L=variance_and_gradient(P,s,c); W=variance_and_gradient(P,t,c)[0]; M=variance_and_gradient(P,a*s+(1-a)*t,c)[0]
    max_jensen=max(max_jensen,M-a*V-(1-a)*W); max_identity=max(max_identity,abs(V-(R-np.sum(c*c/s)))); max_euler=max(max_euler,abs(V+s@g))
    h=rng.normal(size=K); h/=np.linalg.norm(h); eps=1e-6
    fd=(variance_and_gradient(P,s+eps*h,c)[0]-variance_and_gradient(P,s-eps*h,c)[0])/(2*eps)
    max_grad=max(max_grad,abs(fd-g@h)/(1+abs(fd)))
assert max_jensen<1e-8 and max_grad<1e-6 and max_identity<1e-8
report['variance_tests']={'trials':1500,'max_positive_jensen_gap':max_jensen,'max_relative_gradient_error':max_grad,'max_variance_identity_error':max_identity,'max_euler_error':max_euler}
print(report['variance_tests'],flush=True)
# fixed population allocation experiment, find objective difference on a reproducible collection
rows=[]
for j in range(60):
    K=4; J=12; P=rng.dirichlet(np.full(J,rng.uniform(.12,1.)),size=K); c=np.array([-1,0,0,1.]); u=np.ones(K)/K
    def obj(s,what):
        V,g,R,L=variance_and_gradient(P,s,c)
        return (V,g) if what=='variance' else (R,g-c*c/s**2)
    cons={'type':'eq','fun':lambda s:s.sum()-1,'jac':lambda s:np.ones(K)}; opts={'ftol':1e-11,'maxiter':300}
    rv=minimize(lambda s:obj(s,'variance'),u,jac=True,method='SLSQP',bounds=[(.02,1)]*K,constraints=cons,options=opts)
    rr=minimize(lambda s:obj(s,'resistance'),u,jac=True,method='SLSQP',bounds=[(.02,1)]*K,constraints=cons,options=opts)
    if not (rv.success and rr.success): continue
    base=variance_and_gradient(P,u,c)[0]; vv=variance_and_gradient(P,rv.x,c)[0]; vr=variance_and_gradient(P,rr.x,c)[0]
    assert vv<=min(base,vr)+1e-7
    rows.append((base,vv,vr,rv.x.tolist(),rr.x.tolist()))
report['allocation']={'attempted':60,'converged':len(rows),'median_reduction_vs_uniform':float(np.median([1-r[1]/r[0] for r in rows])),'median_reduction_vs_resistance_optimum':float(np.median([1-r[1]/r[2] for r in rows])),'max_reduction_vs_resistance_optimum':float(np.max([1-r[1]/r[2] for r in rows])),'rows':rows}
print({k:v for k,v in report['allocation'].items() if k!='rows'},flush=True)
# simultaneous heldout confidence + no-split certificate, using exactly known discrete free energies
cov=[]
for Nper in [100,1000,10000]:
    for overlap in [.05,.35]:
        K=4; P=np.full((K,K),overlap/(K-1)); np.fill_diagonal(P,1-overlap); fs=np.array([0,.7,-.2,1.1]); q=P*np.exp(-fs[:,None]); Utable=-np.log(q.T)
        bad=0; fully=0; widths=[]; cut_finite=0; cut_bad=0; cut_width=[]; solver_fallbacks=0
        for j in range(100):
            labels=np.repeat(np.arange(K),Nper); X=np.concatenate([rng.choice(K,size=Nper,p=P[k]) for k in range(K)])
            U=Utable[X]; pilot=fs+rng.normal(0,.5,K) # independent deliberately noisy reference, not fitted from holdout
            r=bridge_intervals(U,labels,pilot,.05); true=fs[None,:]-fs[:,None]
            bad+=int(np.any(true<r['lower']-1e-12) or np.any(true>r['upper']+1e-12)); fully+=int(np.all(np.isfinite(r['upper']))); widths.append(r['upper'][0,-1]-r['lower'][0,-1])
            try: center,O,res=solve(U,labels,tol=1e-7)
            except (ValueError,RuntimeError): center=pilot; solver_fallbacks+=1
            rad=observable_cut_radius(U,labels,center,.05); cut_finite+=int(np.isfinite(rad)); cut_bad+=int(np.ptp(center-fs)>rad+1e-12); cut_width.append(2*rad)
        row={'N_per_state':Nper,'overlap':overlap,'trials':100,'bridge_noncoverage':bad,'bridge_all_finite':fully,'bridge_median_endpoint_width':float(np.median(widths)),'cut_noncoverage':cut_bad,'solver_fallbacks':solver_fallbacks,'cut_finite':cut_finite,'cut_median_width':float(np.median(cut_width))}
        print(row,flush=True); cov.append(row)
report['coverage']=cov
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
from pathlib import Path
Path(__file__).resolve().parents[1].joinpath('results','benchmark_results.json').write_text(json.dumps(report,indent=2).replace('Infinity','null'))
print('ALL REFERENCE CHECKS PASSED',flush=True)
