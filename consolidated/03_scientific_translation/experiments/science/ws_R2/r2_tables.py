#!/usr/bin/env python3
"""R2 — finite inequalities of §11.22 tested on complete class tables.

Tables: mine (out/walk_N*.txt, N<=23, own enumerator) and the engineering division's
(n<=24, i.e. N<=27).  Everything here depends on a walk only through (N, h3, h8, h11, gmin).

 (A) my tables == engineering tables (N = 4..23)
 (B) Prop 11.72(a): h8 >= 4h3-2, h8 >= 6h3-N-4, h8 <= 2h3+3N+3
 (C) Prop 11.72(b), walk form: c.h <= bN + 4M + c3 + 2c8 for the eleven rows
 (D) Prop 11.72(c) rows (limit statements): max over classes of c.h - bN, and of the three
     gauche functionals minus gmin  -- reported, since no finite-N constant is claimed
 (E) Prop 11.73: 9h3+4h8+h11 <= 35N - 17.6 N^(2/3) + 17; e3 <= 2N - 2^(-2/3)N^(2/3);
     e8 <= 6N - 3N^(2/3); k_N = (1 - max||N^x||_1/(35N)) N^(1/3)
"""
import os, sys, math
from fractions import Fraction as Fr
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
from cmp_tables import load_mine, load_eng

ROWS_B=[((-1,0,0),0,Fr(1,2)),((4,-1,0),0,5),((6,-1,0),1,6),((-2,1,0),3,2),((-1,1,-1),0,3),((-1,2,-1),3,4),
        ((-4,2,-1),2,6),((3,4,-3),5,6),((6,-2,1),2,6),((0,-1,2),7,1),((-3,0,2),9,3)]
ROWS_C=[((-3,2,-1),2),((-3,4,-3),2)]
GAU=[("q>=2p11-5p3-8",lambda N,h:2*h[2]-5*h[0]-8*N),("q>=2p11-p8-7",lambda N,h:2*h[2]-h[1]-7*N),("q>=p11+p8-4p3-7",lambda N,h:h[2]+h[1]-4*h[0]-7*N)]

def tables():
    out={}
    for N in range(4,28):
        f=f"{HERE}/out/walk_N{N}.txt"
        mine=load_mine(N) if os.path.exists(f) else None
        try: eng,tot=load_eng(N-3)
        except FileNotFoundError: eng=None
        out[N]=(mine,eng)
    return out

if __name__=="__main__":
    T=tables()
    print("(A) own enumeration vs engineering class tables")
    for N,(mine,eng) in T.items():
        if mine is not None and eng is not None:
            print(f"  N={N:2d}: classes {len(mine):5d}  conformations {sum(v[0] for v in mine.values()):>14d}  identical={mine==eng}")
    print("\n(B) Prop 11.72(a) on every class (min slack over classes; must be >= 0)")
    okB=True
    for N,(mine,eng) in T.items():
        tab=eng if eng is not None else mine
        s1=min(h[1]-(4*h[0]-2) for h in tab); s2=min(h[1]-(6*h[0]-N-4) for h in tab); s3=min(2*h[0]+3*N+3-h[1] for h in tab)
        okB&=(s1>=0 and s2>=0 and s3>=0)
        print(f"  N={N:2d} ({'eng' if eng is not None else 'own'}): h8-(4h3-2)>={s1}   h8-(6h3-N-4)>={s2}   (2h3+3N+3)-h8>={s3}")
    print("  all hold:",okB)
    print("\n(C) Prop 11.72(b) walk form c.h <= bN + 4M + c3 + 2c8: max over classes of c.h - bN, against the constant")
    okC=True
    hdr="  N  "+" ".join(f"{str(c):>11s}" for c,b,M in ROWS_B)
    print(hdr); print("  const"+" ".join(f"{str(4*M+c[0]+2*c[1]):>11s}" for c,b,M in ROWS_B))
    for N,(mine,eng) in T.items():
        tab=eng if eng is not None else mine
        vals=[]
        for c,b,M in ROWS_B:
            m=max(c[0]*h[0]+c[1]*h[1]+c[2]*h[2]-b*N for h in tab)
            vals.append(m); okC&=(m<=4*M+c[0]+2*c[1])
        print(f"  {N:2d}   "+" ".join(f"{v:>11d}" for v in vals))
    print("  all hold:",okC)
    print("\n(D) rows of Prop 11.72(c) (limit statements): max over classes of c.h - bN; and max of (gauche functional - gmin)")
    for N,(mine,eng) in T.items():
        tab=eng if eng is not None else mine
        v=[max(c[0]*h[0]+c[1]*h[1]+c[2]*h[2]-b*N for h in tab) for c,b in ROWS_C]
        gv=[max(f(N,h)-tab[h][1] for h in tab) for name,f in GAU]
        print(f"  N={N:2d}: (-3,2,-1;2): {v[0]:4d}   (-3,4,-3;2): {v[1]:4d}   gauche bounds minus gmin: {gv}")
    print("\n(E) Prop 11.73")
    okE=True
    for N,(mine,eng) in T.items():
        tab=eng if eng is not None else mine
        mx=max(9*h[0]+4*h[1]+h[2] for h in tab)
        bound=35*N-17.6*N**(2/3)+17
        e3=max(h[0]+N-1 for h in tab); e8=max(h[1]+N-2 for h in tab)
        b3=2*N-2**(-2/3)*N**(2/3); b8=6*N-3*N**(2/3)
        okE&=(mx<=bound and e3<=b3 and e8<=b8)
        kN=(1-mx/(35*N))*N**(1/3)
        npairs=max(h[0]+h[1]+h[2] for h in tab)
        print(f"  N={N:2d}: max||N^x||_1={mx:4d} ({mx/N:6.3f}/bead = {100*mx/(35*N):4.1f}% of 35)  bound {bound:7.1f}  k_N={kN:.3f}   max pairs/bead={npairs/N:.2f}  max e3={e3} (<= {b3:.2f})  max e8={e8} (<= {b8:.2f})")
    print("  all hold:",okE)
