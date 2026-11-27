# Coordinator's check of the site-set reduction on the diamond-lattice chain (own enumeration).
# Beads 0..N-1, N = n+3; bond m is +a_i (m even) or -a_i (m odd), consecutive indices differ.
import itertools, sys
A = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
def walks(nbonds):
    def rec(pos, last, m, path, occ):
        if m == nbonds:
            yield path; return
        for i in range(4):
            if i == last: continue
            s = 1 if m % 2 == 0 else -1
            q = (pos[0]+s*A[i][0], pos[1]+s*A[i][1], pos[2]+s*A[i][2])
            if q in occ: continue
            occ.add(q); path.append(q)
            yield from rec(q, i, m+1, path, occ)
            path.pop(); occ.remove(q)
    start = (0,0,0)
    # fix the first bond to +a_0 (symmetry): multiplies counts by 4
    q = A[0]
    yield from rec(q, 0, 1, [start, q], {start, q})
def d2(p,q): return (p[0]-q[0])**2+(p[1]-q[1])**2+(p[2]-q[2])**2
for n in range(1, 9):
    N = n + 3
    classes = {}; cnt = 0; bad = 0
    for path in walks(N-1):
        cnt += 1
        h = {3:0, 8:0, 11:0}
        for p in range(N):
            for q in range(p+3, N):
                d = d2(path[p], path[q])
                if d in h: h[d] += 1
        # from the site set alone
        e = {3:0, 8:0, 11:0}
        for p in range(N):
            for q in range(p+1, N):
                d = d2(path[p], path[q])
                if d in e: e[d] += 1
        if (h[3], h[8], h[11]) != (e[3]-(N-1), e[8]-(N-2), e[11]): bad += 1
        g = sum(1 for i in range(N-3) if d2(path[i], path[i+3]) == 11)
        # gauche by the index rule: torsion j trans iff i_{j+2} = i_j  <=> |x_{j+3}-x_j|^2 = 19
        key = (h[3], h[8], h[11])
        classes[key] = min(classes.get(key, 10**9), g)
    print(f"n={n} N={N} conformations={cnt*4} (12 x the published count: 233, 683, 2005, 5849 for n = 5..8) classes={len(classes)} site-set identity violations={bad}")
