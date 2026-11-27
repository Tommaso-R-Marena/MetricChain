"""R2 — common lattice helpers (own code)."""
import itertools
A=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
def is_A(s): return s[0]%2==0 and s[1]%2==0 and s[2]%2==0 and (s[0]+s[1]+s[2])%4==0
def is_B(s): return is_A((s[0]-1,s[1]-1,s[2]-1))
def lat(s): return is_A(s) or is_B(s)
def add(a,b): return (a[0]+b[0],a[1]+b[1],a[2]+b[2])
def sub(a,b): return (a[0]-b[0],a[1]-b[1],a[2]-b[2])
def d2(a,b): return (a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2
def sgn(s): return 1 if is_A(s) else -1
def nb(s,i):
    g=sgn(s); return (s[0]+g*A[i][0], s[1]+g*A[i][1], s[2]+g*A[i][2])
def nbrs(s): return [nb(s,i) for i in range(4)]

def measure(x):
    """(h3,h8,h11,g) of a sequence of sites by the O(N^2) definition; raises if not a self-avoiding lattice walk"""
    N=len(x); h={3:0,8:0,11:0}; g=0
    assert len(set(x))==N, "not injective"
    for i in range(N):
        assert lat(x[i]), "not a lattice site"
        if i+1<N: assert d2(x[i],x[i+1])==3, "not bonded"
    for p in range(N):
        for q in range(p+3,N):
            d=d2(x[p],x[q])
            if d in h: h[d]+=1
            if q-p==3:
                assert d in (11,19)
                g+=(d==11)
    return (h[3],h[8],h[11],g)

V3=[v for v in itertools.product(range(-3,4),repeat=3) if sum(c*c for c in v)==3]
V8=[v for v in itertools.product(range(-3,4),repeat=3) if sum(c*c for c in v)==8]
V11=[v for v in itertools.product(range(-3,4),repeat=3) if sum(c*c for c in v)==11]
def measure_fast(x):
    """same as measure() but by neighbour look-ups (for long walks); validated against measure() in r2_selftest"""
    N=len(x); idx={}
    for i,s in enumerate(x):
        assert s not in idx, "not injective"
        idx[s]=i
    h3=h8=h11=g=0
    for q,s in enumerate(x):
        if q+1<N: assert d2(s,x[q+1])==3
        for v in V3:
            p=idx.get((s[0]+v[0],s[1]+v[1],s[2]+v[2]))
            if p is not None and q-p>=3: h3+=1
        for v in V8:
            p=idx.get((s[0]+v[0],s[1]+v[1],s[2]+v[2]))
            if p is not None and q-p>=3: h8+=1
        for v in V11:
            p=idx.get((s[0]+v[0],s[1]+v[1],s[2]+v[2]))
            if p is not None and q-p>=3:
                h11+=1
                if q-p==3: g+=1
    return (h3,h8,h11,g)
def is_bridge(x):
    y0=x[0][1]; yl=x[-1][1]
    return all(s[1]>y0 for s in x[1:]) and all(s[1]<=yl for s in x)
def site_e(S):
    """(e3,e8,e11) of a finite site set by look-ups"""
    S=set(S); e3=e8=e11=0
    for s in S:
        for v in V3:
            if (s[0]+v[0],s[1]+v[1],s[2]+v[2]) in S: e3+=1
        for v in V8:
            if (s[0]+v[0],s[1]+v[1],s[2]+v[2]) in S: e8+=1
        for v in V11:
            if (s[0]+v[0],s[1]+v[1],s[2]+v[2]) in S: e11+=1
    return e3//2,e8//2,e11//2
def norm_c(d):
    return 5*abs(d[0])+3*abs(d[0]+d[1])+abs(d[0]+d[1]+d[2])
