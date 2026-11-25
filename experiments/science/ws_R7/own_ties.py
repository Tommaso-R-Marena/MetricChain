"""R7 OWN: the "exact ties" of the generic chain's cover relation (ENG-RES-0007 section 3: five exact ties at n = 11,
L = 1, eps = N/2 = 7; "we did not pursue it").

For every n: all off-diagonal (centre a, point y) with |L*D(a,y) - (gmin(y)+eps)| < 1e-9 in any of the 12 cells.
Each such pair is re-evaluated with mpmath at 60 significant digits from the torsion words (own geometry code),
and the structure of the two profiles is printed, so that the reason for the tie can be read off.
"""
import json
import sys

import mpmath as mp
import numpy as np

import own_cover as oc
import own_gen as og

mp.mp.dps = 60
TH = mp.radians(111)
PH = [mp.pi, mp.pi / 3, -mp.pi / 3]
CT, ST = mp.cos(TH), mp.sin(TH)


def mp_coords(word):
    def sub(a, b): return [a[i] - b[i] for i in range(3)]
    def add(a, b): return [a[i] + b[i] for i in range(3)]
    def scal(c, a): return [c * a[i] for i in range(3)]
    def dot(a, b): return sum(a[i] * b[i] for i in range(3))
    def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    def unit(a):
        nrm = mp.sqrt(dot(a, a)); return [x / nrm for x in a]
    X = [[mp.mpf(0)] * 3, [mp.mpf(1), mp.mpf(0), mp.mpf(0)], [1 - CT, ST, mp.mpf(0)]]
    for k, st in enumerate(word):
        a, b, c = X[-3], X[-2], X[-1]
        bc = unit(sub(c, b))
        nrm = unit(cross(sub(b, a), bc))
        m = cross(nrm, bc)
        phi = PH[int(st)]
        d = add(add(scal(-CT, bc), scal(ST * mp.cos(phi), m)), scal(ST * mp.sin(phi), nrm))
        X.append(add(c, d))
    return X


def mp_sorted_trunc(word, sc=16):
    X = mp_coords(word)
    N = len(X)
    out = []
    for p in range(N):
        for q in range(p + 3, N):
            s = sum((X[p][i] - X[q][i]) ** 2 for i in range(3))
            out.append(min(s, mp.mpf(sc)))
    return sorted(out)


def mp_dist(wa, wy):
    A, Y = mp_sorted_trunc(wa), mp_sorted_trunc(wy)
    return sum(abs(x - y) for x, y in zip(A, Y))


def wordstr(w):
    return "".join("t+-"[int(k)] for k in w)


if __name__ == "__main__":
    n0, n1 = int(sys.argv[1]), int(sys.argv[2])
    allres = {}
    for n in range(n0, n1 + 1):
        cd = oc.class_data(n)
        D = oc.dist_matrix(cd["Srep"])
        N = n + 3
        ties = []
        nearest_non_tie = np.inf
        for L in (1.0, 0.2):
            for name, eps in (("0", 0.0), ("1", 1.0), ("N/20", N / 20), ("N/10", N / 10), ("N/4", N / 4), ("N/2", N / 2)):
                slack = (cd["mingap"] + eps)[None, :] - L * D
                off = np.abs(slack)
                np.fill_diagonal(off, np.inf)
                idx = np.argwhere(off < 1e-9)
                for a, y in idx:
                    ties.append((L, name, eps, int(a), int(y), float(slack[a, y])))
                off[off < 1e-9] = np.inf
                nearest_non_tie = min(nearest_non_tie, float(off.min()))
        print(f"n={n}: classes={cd['ncls']}  exact-tie candidates (|slack|<1e-9, off-diagonal): {len(ties)}  nearest non-tie: {nearest_non_tie:.4e}")
        recs = []
        for (L, name, eps, a, y, sl) in ties:
            wa, wy = cd["words"][cd["rep"][a]], cd["words"][cd["rep"][y]]
            dmp = mp_dist(wa, wy)
            target = (int(cd["mingap"][y]) + mp.mpf(eps)) / mp.mpf(L)
            dev = dmp - target
            rec = dict(L=L, eps=name, centre=wordstr(wa), point=wordstr(wy), gmin_point=int(cd["mingap"][y]),
                       float_slack=sl, D_float=float(D[a, y]), D_mp=mp.nstr(dmp, 40), deviation_mp=mp.nstr(dev, 5))
            recs.append(rec)
            print("   ", rec)
        allres[n] = dict(classes=int(cd["ncls"]), ties=recs, nearest_non_tie=nearest_non_tie)
        json.dump(allres, open(f"out_own_ties_{n0}_{n1}.json", "w"), indent=1)
