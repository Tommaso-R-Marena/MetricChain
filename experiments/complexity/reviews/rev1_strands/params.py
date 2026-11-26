# params.py -- read a ViennaRNA "RNAfold parameter file v2.0" and evaluate the loops that occur in the
# systems I(a,m,B) (stack, bulge, interior loop, exterior-loop dangles) with the published numbers.
# Units: 0.01 kcal/mol (integers).  Written by the referee; the loop-energy conventions follow
# ViennaRNA's E_IntLoop / E_ExtLoop (reimplemented from memory of loop_energies.h; a symmetry
# self-test below guards against index mix-ups).
import re, math

BASE = {"N": 0, "A": 1, "C": 2, "G": 3, "U": 4, "T": 4}
PT = {("C", "G"): 1, ("G", "C"): 2, ("G", "U"): 3, ("U", "G"): 4, ("A", "U"): 5, ("U", "A"): 6,
      ("G", "T"): 3, ("T", "G"): 4, ("A", "T"): 5, ("T", "A"): 6}
RTYPE = [0, 2, 1, 4, 3, 6, 5, 7]
INF = 10 ** 7
MAXLOOP = 30


class Params:
    def __init__(self, path):
        txt = open(path).read()
        sec = {}
        cur = None
        for line in txt.splitlines():
            line = re.sub(r"/\*.*?\*/", " ", line)       # comments are single-line in these files
            if "/*" in line:                               # unterminated comment (present in the DNA files)
                line = line[:line.index("/*")]
            if line.startswith("##"):
                continue
            if line.startswith("#"):
                cur = line[1:].strip()
                sec[cur] = []
                continue
            if cur is None:
                continue
            for tok in line.split():
                if tok == "INF":
                    sec[cur].append(INF)
                elif tok == "DEF":
                    sec[cur].append(-50)
                else:
                    try:
                        sec[cur].append(int(tok))
                    except ValueError:
                        pass  # loop sequences in Tetraloops etc.
        self.sec = sec

        def arr(name, dims):
            v = sec[name]
            n = 1
            for d in dims:
                n *= d
            assert len(v) == n, (name, len(v), n)
            return v, dims

        self.stack_v = arr("stack", (7, 7))[0]
        self.mmI = arr("mismatch_internal", (7, 5, 5))[0]
        self.mm1n = arr("mismatch_internal_1n", (7, 5, 5))[0]
        self.mm23 = arr("mismatch_internal_23", (7, 5, 5))[0]
        self.mmE = arr("mismatch_exterior", (7, 5, 5))[0]
        self.d5 = arr("dangle5", (7, 5))[0]
        self.d3 = arr("dangle3", (7, 5))[0]
        self.i11 = arr("int11", (7, 7, 5, 5))[0]
        self.i21 = arr("int21", (7, 7, 5, 5, 5))[0]
        self.i22 = arr("int22", (6, 6, 4, 4, 4, 4))[0]
        self.bulge = sec["bulge"]
        self.internal = sec["internal"]
        assert len(self.bulge) == 31 and len(self.internal) == 31
        self.ninio, _, self.max_ninio = sec["NINIO"][:3]
        self.lxc = 107.856

    # --- accessors (pair types 1..7, bases 0..4)
    def stack(self, t, t2):
        return self.stack_v[(t - 1) * 7 + (t2 - 1)]

    def mismatch(self, tab, t, a, b):
        return tab[((t - 1) * 5 + a) * 5 + b]

    def int11(self, t, t2, a, b):
        return self.i11[(((t - 1) * 7 + (t2 - 1)) * 5 + a) * 5 + b]

    def int21(self, t, t2, a, b, c):
        return self.i21[((((t - 1) * 7 + (t2 - 1)) * 5 + a) * 5 + b) * 5 + c]

    def int22(self, t, t2, a, b, c, d):
        return self.i22[((((((t - 1) * 6 + (t2 - 1)) * 4 + (a - 1)) * 4 + (b - 1)) * 4 + (c - 1)) * 4 + (d - 1))]

    def dangle5(self, t, a):
        return self.d5[(t - 1) * 5 + a]

    def dangle3(self, t, a):
        return self.d3[(t - 1) * 5 + a]

    # --- degree-2 loop closed by (i,j) with inner pair (p,q), i<p<q<j
    def int_loop(self, n1, n2, t, t2, si1, sj1, sp1, sq1):
        nl, ns = (n1, n2) if n1 > n2 else (n2, n1)
        if nl == 0:
            return self.stack(t, t2)
        if ns == 0:
            e = self.bulge[nl] if nl <= MAXLOOP else self.bulge[30] + int(self.lxc * math.log(nl / 30.0))
            if nl == 1:
                e += self.stack(t, t2)
            return e  # (no terminal-AU term: all pairs here are G-C)
        if ns == 1:
            if nl == 1:
                return self.int11(t, t2, si1, sj1)
            if nl == 2:
                if n1 == 1:
                    return self.int21(t, t2, si1, sq1, sj1)
                return self.int21(t2, t, sq1, si1, sp1)
            e = self.internal[nl + 1] if nl + 1 <= MAXLOOP else self.internal[30] + int(self.lxc * math.log((nl + 1) / 30.0))
            e += min(self.max_ninio, (nl - ns) * self.ninio)
            e += self.mismatch(self.mm1n, t, si1, sj1) + self.mismatch(self.mm1n, t2, sq1, sp1)
            return e
        if ns == 2:
            if nl == 2:
                return self.int22(t, t2, si1, sp1, sq1, sj1)
            if nl == 3:
                e = self.internal[5] + self.ninio
                e += self.mismatch(self.mm23, t, si1, sj1) + self.mismatch(self.mm23, t2, sq1, sp1)
                return e
        u = nl + ns
        e = self.internal[u] if u <= MAXLOOP else self.internal[30] + int(self.lxc * math.log(u / 30.0))
        e += min(self.max_ninio, (nl - ns) * self.ninio)
        e += self.mismatch(self.mmI, t, si1, sj1) + self.mismatch(self.mmI, t2, sq1, sp1)
        return e


def nickfree_energy(P, f, rna=True, check=True):
    """energy of a nick-free two-chord face (Face object) of I(a,m,B)"""
    conv = (lambda ch: ch) if rna else (lambda ch: ch)
    segs = [s for s, _ in f.segs]
    if set(segs[0]) <= set("C"):
        iseg, tseg = segs[0], segs[1]
    else:
        tseg, iseg = segs[0], segs[1]
    # closing pair (i,j) = (tseg[0], iseg[-1]); inner pair (p,q) = (tseg[-1], iseg[0])
    t = PT[(tseg[0], iseg[-1])]
    t2 = RTYPE[PT[(tseg[-1], iseg[0])]]
    n1, n2 = len(tseg) - 2, len(iseg) - 2
    si1, sp1 = BASE[tseg[1]], BASE[tseg[-2]]
    sq1, sj1 = BASE[iseg[1]], BASE[iseg[-2]]
    e = P.int_loop(n1, n2, t, t2, si1, sj1, sp1, sq1)
    if check:
        e2 = P.int_loop(n2, n1, t2, t, sq1, sp1, sj1, si1)   # the same loop seen from the other helix
        assert e == e2, ("asymmetric loop energy", f.s, e, e2)
    return e


def exterior_stems(f):
    """for every chord of an exterior-loop face: (pair type, x, y, x_unpaired, y_unpaired) where x is the
    base covalently 5' of the pair's first base inside the loop (or None) and y the base covalently 3' of
    its second base inside the loop (or None)"""
    letters, seps = f.s[0::2], f.s[1::2]
    L = len(letters)
    paired = [seps[j] == "=" or seps[(j - 1) % L] == "=" for j in range(L)]
    out = []
    for j in range(L):
        if seps[j] == "=":
            u, v = j, (j + 1) % L
            t = PT[(letters[u], letters[v])]
            x = (j - 1) % L if seps[(j - 1) % L] == "-" else None
            y = (v + 1) % L if seps[v] == "-" else None
            out.append((t, None if x is None else letters[x], None if y is None else letters[y],
                        None if x is None else (not paired[x]), None if y is None else (not paired[y]), x, y))
    return out


def ext_d2(P, f):
    """ViennaRNA -d2 style: both neighbours of every stem contribute, paired or not"""
    e = 0
    for t, x, y, xu, yu, _, _ in exterior_stems(f):
        if x is not None and y is not None:
            e += P.mismatch(P.mmE, t, BASE[x], BASE[y])
        elif x is not None:
            e += P.dangle5(t, BASE[x])
        elif y is not None:
            e += P.dangle3(t, BASE[y])
    return e


def ext_some(P, f):
    """'some dangles' style: only unpaired neighbours dangle; a base flanked by two stems takes the better one"""
    best = {}
    for t, x, y, xu, yu, ix, iy in exterior_stems(f):
        if x is not None and xu:
            best[ix] = min(best.get(ix, 0), P.dangle5(t, BASE[x]))
        if y is not None and yu:
            best[iy] = min(best.get(iy, 0), P.dangle3(t, BASE[y]))
    return sum(best.values())


def states_bulge_correction(f):
    """NNDB Turner-2004 single-nucleotide bulge extras that ViennaRNA does not implement:
    special C bulge (-0.9 if the bulged C is adjacent to a paired C) and -RT ln(number of states)."""
    if f.kind != "bulge" or f.unp != 1:
        return 0
    segs = [s for s, _ in f.segs]
    seg = segs[0] if len(segs[0]) == 3 else segs[1]
    b = seg[1]
    states = 1 + (seg[0] == b) + (seg[2] == b)
    e = -int(round(61.6 * math.log(states)))
    if b == "C" and (seg[0] == "C" or seg[2] == "C"):
        e += -90
    return e
