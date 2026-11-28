"""Reference implementation for proposed MBAR research theorems.
Float64, NOT interval-certified numerics. Statistical guarantees assume exact
arithmetic, independent equilibrium samples and the stated protocol.
"""
import numpy as np
from scipy.special import logsumexp, xlogy
from scipy.optimize import brentq, minimize
from scipy.linalg import null_space
from scipy.sparse.csgraph import connected_components


def graph_diagnostic(O, counts, *, tol=1e-9, rank_tol=1e-12):
    """Fail closed: never invert a disconnected or numerically unresolved Laplacian.
    This is an overlap diagnostic, not a statistical certificate.
    """
    O, counts = np.asarray(O, float), np.asarray(counts, float)
    K = len(counts)
    if K < 2 or O.shape != (K,K) or not np.all(np.isfinite(O)) or not np.all(np.isfinite(counts)) or np.any(counts <= 0):
        raise ValueError('invalid shape, nonfinite input or nonpositive count')
    s = counts / counts.sum()
    W = s[:,None]*O
    if np.any(O < -tol) or not np.allclose(O.sum(axis=1), 1, atol=tol, rtol=0) or not np.allclose(W, W.T, atol=tol, rtol=0):
        raise ValueError('overlap matrix fails nonnegativity, stochasticity or detailed balance')
    W = np.maximum((W+W.T)/2, 0)
    np.fill_diagonal(W,0)
    L = np.diag(W.sum(axis=1))-W
    Q = null_space(np.ones((1,K)))
    A = Q.T@L@Q
    eig = np.linalg.eigvalsh(A)
    if eig[0] <= rank_tol*max(1., eig[-1]):
        return dict(status='FAIL_RANK', R_max=np.inf, graph_effective_overlap=0., L=L)
    P = Q@np.linalg.solve(A,Q.T)
    R = np.diag(P)[:,None]+np.diag(P)[None,:]-2*P
    np.fill_diagonal(R,0.)
    return dict(status='DIAGNOSTIC_ONLY', R_max=float(R.max()), graph_effective_overlap=float(counts.sum()/R.max()), R=R, L=L, Lplus=P)


def solve(U, labels, *, tol=1e-9):
    """Only returns a solution for a strongly connected directed support graph
    and small numerical gradient. Numerical convergence is not a proof certificate.
    """
    U=np.asarray(U,float); labels=np.asarray(labels,int)
    if U.ndim != 2 or len(labels)!=len(U) or len(U)==0 or U.shape[1]<2: raise ValueError('shape')
    K=U.shape[1]
    if np.any(labels<0) or np.any(labels>=K) or np.any(np.isnan(U)) or np.any(np.isneginf(U)) or not np.all(np.isfinite(U[np.arange(len(U)),labels])): raise ValueError('invalid sampled state or energy')
    n=np.bincount(labels,minlength=K)
    if np.any(n==0): raise ValueError('unsampled state')
    support=np.array([np.any(np.isfinite(U[labels==k]),axis=0) for k in range(K)])
    if connected_components(support,directed=True,connection='strong')[0]!=1: raise ValueError('finite unique optimizer not identified')
    s=n/n.sum()
    def fun(g):
        f=np.r_[0.,g]; z=np.log(s)+f-U; l=logsumexp(z,axis=1); p=np.exp(z-l[:,None]); return l.mean()-s@f,(p.mean(axis=0)-s)[1:]
    res=minimize(fun,np.zeros(K-1),jac=True,method='BFGS',options={'gtol':tol/10})
    f=np.r_[0.,res.x]; z=np.log(s)+f-U; p=np.exp(z-logsumexp(z,axis=1)[:,None]); residual=np.max(np.abs(p.mean(axis=0)-s))
    if not np.isfinite(res.fun) or residual>tol: raise RuntimeError(f'optimizer residual {residual}')
    O=(p.T@p)/n[:,None]
    return f, O, residual


def kl_bernoulli(x,y):
    return float(xlogy(x,x)-xlogy(x,y)+xlogy(1-x,1-x)-xlogy(1-x,1-y))


def mean_interval(x,n,t):
    """KL-Chernoff inversion for a mean of independent [0,1] variables.
    Float64 reference calculation, outward one-ULP expansion (not rigorous interval arithmetic).
    """
    if not (0<=x<=1 and n>0 and t>0): raise ValueError('bad mean/count/threshold')
    z=t/n
    if x==0: return 0.,float(-np.expm1(-z))
    if x==1: return float(np.exp(-z)),1.
    # Bisection in mean space avoids singular endpoint evaluation.
    l,r=0.,x
    for _ in range(80):
        m=(l+r)/2
        if m==0 or kl_bernoulli(x,m)>z: l=m
        else: r=m
    lower=l
    l,r=x,1.
    for _ in range(80):
        m=(l+r)/2
        if m==1 or kl_bernoulli(x,m)>z: r=m
        else: l=m
    return float(max(0,np.nextafter(lower,-np.inf))),float(min(1,np.nextafter(r,np.inf)))


def bridge_intervals(U, labels, pilot, alpha=.05, edges=None):
    """Simultaneous confidence intervals for f_j-f_i using independent holdout.
    pilot and edge set must be fixed before validation. U = -log q, +inf allowed.
    Uses softmax(q*exp(pilot)); pilot includes arbitrary log weights.
    Returns shortest-path bounds and direct edges; infinite bounds mean abstention.
    """
    U=np.asarray(U,float); labels=np.asarray(labels,int); pilot=np.asarray(pilot,float)
    if U.ndim!=2 or len(U)==0 or len(labels)!=len(U): raise ValueError('shape')
    K=U.shape[1]
    if K<2 or pilot.shape!=(K,) or not np.all(np.isfinite(pilot)) or not 0<alpha<1: raise ValueError('pilot or alpha')
    if np.any(labels<0) or np.any(labels>=K) or np.any(np.isnan(U)) or np.any(np.isneginf(U)) or not np.all(np.isfinite(U[np.arange(len(U)),labels])): raise ValueError('energies or labels')
    n=np.bincount(labels,minlength=K)
    if np.any(n==0): raise ValueError('every validation state needs samples')
    edges=list((i,j) for i in range(K) for j in range(i+1,K)) if edges is None else list(edges)
    if not edges or len(set(edges))!=len(edges) or any(not 0<=i<j<K for i,j in edges): raise ValueError('edge list')
    logits=pilot-U; p=np.exp(logits-logsumexp(logits,axis=1)[:,None])
    t=np.log(4*len(edges)/alpha); D=np.full((K,K),np.inf); np.fill_diagonal(D,0.)
    direct=[]
    for i,j in edges:
        a=float(p[labels==i,j].mean()); b=float(p[labels==j,i].mean())
        al,au=mean_interval(np.clip(a,0,1),n[i],t); bl,bu=mean_interval(np.clip(b,0,1),n[j],t)
        # ratio a/b = exp(pilot_j-pilot_i) Z_j/Z_i.
        # f_j-f_i = pilot_j-pilot_i + log b - log a.
        offset=pilot[j]-pilot[i]
        lo=offset+np.log(bl)-np.log(au) if bl>0 and au>0 else -np.inf
        hi=offset+np.log(bu)-np.log(al) if al>0 and bu>0 else np.inf
        D[i,j]=min(D[i,j],hi); D[j,i]=min(D[j,i],-lo)
        direct.append((i,j,lo,hi,a,b))
    for k in range(K): D=np.minimum(D,D[:,k,None]+D[None,k,:])
    if np.any(np.diag(D)<-1e-10): return dict(status='FAIL_INCONSISTENT', lower=np.full((K,K),-np.inf), upper=np.full((K,K),np.inf),direct=direct)
    np.fill_diagonal(D,0)
    return dict(status='INTERVALS' if np.all(np.isfinite(D)) else 'PARTIAL_ABSTENTION', lower=-D.T, upper=D,direct=direct)


def cut_radius(O, counts, alpha=.05, *, residual_cut=0.):
    """No-split global oscillation radius at a candidate. O must be exact fitted
    overlap at stationarity; nonzero residual_cut must use the actual Hessian
    instead (not supported here)."""
    if not 0<alpha<1 or residual_cut!=0: raise ValueError('exact stationarity required')
    d=graph_diagnostic(O,counts)
    if d['status']!='DIAGNOSTIC_ONLY': return np.inf
    K=len(counts); N=sum(counts)
    # upper bound log(2*(2^(K-1)-1)/alpha) <= K log 2 - log alpha
    eps=np.sqrt((K*np.log(2)-np.log(alpha))/(2*N))
    q=d['R_max']*eps
    return float(-np.log1p(-q)) if q<1 else np.inf


def variance_and_gradient(P,s,c):
    """Exact discrete-model population objective V and ambient gradient.
    P[k,x] = normalized state probability mass; positive s need not sum to 1.
    """
    P,s,c=np.asarray(P,float),np.asarray(s,float),np.asarray(c,float)
    if P.ndim!=2 or len(s)!=len(P) or c.shape!=s.shape or np.any(P<0) or not np.allclose(P.sum(axis=1),1) or np.any(s<=0) or abs(c.sum())>1e-10: raise ValueError('bad input')
    m=s@P; active=m>0; P=P[:,active]; m=m[active]; pi=s[:,None]*P/m
    L=np.diag(s)-(pi*m)@pi.T
    Q=null_space(np.ones((1,len(s)))); A=Q.T@L@Q
    if np.linalg.eigvalsh(A)[0]<=1e-13*max(1,np.linalg.norm(A,2)): raise ValueError('disconnected/unresolved')
    v=Q@np.linalg.solve(A,Q.T@c); z=v@pi; means=P@z
    grad=-np.sum(P*(z[None,:]-means[:,None])**2,axis=1)
    V=float(-s@grad) # stable nonnegative variance decomposition
    return V,grad,float(c@v),L


def observable_cut_radius(U, labels, center, alpha=.05, rank_tol=1e-12):
    """No-split theorem: works for any data-dependent finite center; actual Hessian
    and actual score residual are used, not exact-stationarity assumption."""
    U=np.asarray(U,float); labels=np.asarray(labels,int); center=np.asarray(center,float)
    if U.ndim!=2 or len(U)==0 or len(labels)!=len(U): raise ValueError('shape')
    K=U.shape[1]
    if K<2 or center.shape!=(K,) or not np.all(np.isfinite(center)) or not 0<alpha<1: raise ValueError('center or alpha')
    if np.any(labels<0) or np.any(labels>=K) or np.any(np.isnan(U)) or np.any(np.isneginf(U)) or not np.all(np.isfinite(U[np.arange(len(U)),labels])): raise ValueError('energies or labels')
    n=np.bincount(labels,minlength=K)
    if np.any(n==0): raise ValueError('every state needs samples')
    s=n/n.sum(); z=np.log(s)+center-U; p=np.exp(z-logsumexp(z,axis=1)[:,None]); g=p.mean(axis=0)-s
    # build Hessian from offdiagonals to avoid subtractive loss on diagonals
    W=p.T@p/len(U); np.fill_diagonal(W,0); H=np.diag(W.sum(axis=1))-W
    Q=null_space(np.ones((1,K))); A=Q.T@H@Q; ev=np.linalg.eigvalsh(A)
    if ev[0]<=rank_tol*max(1,ev[-1]): return np.inf
    P=Q@np.linalg.solve(A,Q.T); R=np.diag(P)[:,None]+np.diag(P)[None,:]-2*P; Rmax=float(R.max())
    eps=np.sqrt((K*np.log(2)-np.log(alpha))/(2*len(U)))+.5*np.sum(np.abs(g))
    q=Rmax*eps
    return float(-np.log1p(-q)) if q<1 else np.inf
