# lib.py -- referee's driver utilities (independent of the author's code).
import itertools, math, os, subprocess, hashlib, random
from fractions import Fraction
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ENUM = os.path.join(HERE, "enum")
CACHE = os.path.join(HERE, "cache")
os.makedirs(CACHE, exist_ok=True)


# ----------------------------------------------------------------- instances
def template(m, B):
    return "A".join(["G" * B] * m)


def system(a, m, B):
    return [template(m, B)] + ["C" * x for x in a]


def packable(a, m, B):
    """exact bin packing by brute force over all maps beta"""
    n = len(a)
    for beta in itertools.product(range(m), repeat=n):
        load = [0] * m
        for i, t in enumerate(beta):
            load[t] += a[i]
        if all(x == B for x in load):
            return True
    return False


def til_by_beta(a, m, B):
    """sum over solutions beta of prod_t |beta^-1(t)|!"""
    n = len(a)
    tot = 0
    for beta in itertools.product(range(m), repeat=n):
        load = [0] * m
        cnt = [0] * m
        for i, t in enumerate(beta):
            load[t] += a[i]
            cnt[t] += 1
        if all(x == B for x in load):
            p = 1
            for c in cnt:
                p *= math.factorial(c)
            tot += p
    return tot


def til_by_perm(a, m, B):
    """number of orderings of the labelled items whose prefix sums hit B,2B,...,(m-1)B"""
    n = len(a)
    need = set(B * t for t in range(1, m))
    tot = 0
    for perm in itertools.permutations(range(n)):
        s = 0
        hit = set()
        for i in perm:
            s += a[i]
            if s in need:
                hit.add(s)
        if hit == need:
            tot += 1
    return tot


def num_set_partitions(a, m, B):
    """L(a,m,B): partitions of the index set into m classes each of sum B (unordered classes)"""
    n = len(a)
    idx = list(range(n))

    def rec(remaining, k):
        if k == 0:
            return 1 if not remaining else 0
        if not remaining:
            return 0
        first = remaining[0]
        rest = remaining[1:]
        tot = 0
        for r in range(0, len(rest) + 1):
            for comb in itertools.combinations(rest, r):
                if a[first] + sum(a[i] for i in comb) == B:
                    rem2 = [i for i in rest if i not in comb]
                    tot += rec(rem2, k - 1)
        return tot

    return rec(idx, m)


def mu_fact(a):
    p = 1
    for s, c in Counter(a).items():
        p *= math.factorial(c)
    return p


# ----------------------------------------------------------------- enumeration
def run_enum(strands, prune=False, orbit=False, lean=False):
    key = "_".join(strands) + ("_P" if prune else "_F") + ("_O" if orbit else "") + ("_L" if lean else "")
    h = hashlib.sha1(key.encode()).hexdigest()[:16]
    path = os.path.join(CACHE, h + ".txt")
    if not os.path.exists(path):
        args = [ENUM] + (["--prune"] if prune else []) + (["--orbit"] if orbit else []) + (["--lean"] if lean else []) + list(strands)
        with open(path + ".tmp", "w") as f:
            subprocess.run(args, stdout=f, check=True)
        os.rename(path + ".tmp", path)
    return parse_enum(path)


def parse_enum(path):
    """returns dict with scalar counters, 'desc' (id -> string) and numpy arrays:
       lab, phys, til (per signature), ids (flat descriptor ids), sidx (signature index per id), ex (examples)"""
    import numpy as np
    from array import array
    res = {"desc": {}}
    lab, phys, til = array("q"), array("q"), array("q")
    ids, sidx = array("i"), array("i")
    ex = []
    k = 0
    with open(path) as f:
        for line in f:
            if line.startswith("SIG "):
                head, rest = line.rstrip("\n").split(" :", 1)
                idpart, e = rest.split(" ; ", 1)
                h = head.split()
                lab.append(int(h[2])); phys.append(int(h[3])); til.append(int(h[4]))
                v = [int(x) for x in idpart.split()]
                ids.extend(v); sidx.extend([k] * len(v))
                ex.append(e)
                k += 1
            elif line.startswith("DESC "):
                _, i, d = line.rstrip("\n").split(" ", 2)
                res["desc"][int(i)] = d
            else:
                kk, v = line.split()
                res[kk] = int(v)
    res["lab"] = np.frombuffer(lab, dtype=np.int64) if len(lab) else np.zeros(0, np.int64)
    res["phys"] = np.frombuffer(phys, dtype=np.int64) if len(phys) else np.zeros(0, np.int64)
    res["til"] = np.frombuffer(til, dtype=np.int64) if len(til) else np.zeros(0, np.int64)
    res["ids"] = np.frombuffer(ids, dtype=np.int32) if len(ids) else np.zeros(0, np.int32)
    res["sidx"] = np.frombuffer(sidx, dtype=np.int32) if len(sidx) else np.zeros(0, np.int32)
    res["ex"] = ex
    return res


# ----------------------------------------------------------------- face descriptors
class Face:
    """parsed cyclic boundary string, e.g. 'C-C=G-G=' (stack) or 'A-G=C|C=G-' (exterior)"""
    __slots__ = ("s", "nn", "k", "kind", "segs", "unp", "tside", "iside", "iota", "flush", "letters")

    def __init__(self, s):
        self.s = s
        letters = s[0::2]
        seps = s[1::2]
        assert len(letters) == len(seps)
        self.letters = letters
        self.nn = seps.count("|")
        self.k = seps.count("=")
        L = len(letters)
        # segments between chords: rotate so that we start just after a '='
        self.segs = []
        if self.k >= 1:
            st = (seps.index("=") + 1) % L
            cur_l, cur_s = [], []
            for t in range(L):
                j = (st + t) % L
                cur_l.append(letters[j])
                if seps[j] == "=":
                    self.segs.append(("".join(cur_l), "".join(cur_s)))
                    cur_l, cur_s = [], []
                else:
                    cur_s.append(seps[j])
        # number of unpaired bases
        self.unp = L - 2 * self.k
        # item covalent bonds on the boundary (a '-' between two C's)
        self.iota = sum(1 for j in range(L) if seps[j] == "-" and letters[j] == "C" and letters[(j + 1) % L] == "C")
        self.tside = None
        self.iside = None
        if self.nn >= 2:
            self.kind = "disconnected"
        elif self.nn == 1:
            self.kind = "exterior"
        elif self.k == 1:
            self.kind = "hairpin"
        elif self.k == 2:
            u = [len(sl) - 2 for sl, _ in self.segs]
            if u[0] == 0 and u[1] == 0:
                self.kind = "stack"
            elif u[0] == 0 or u[1] == 0:
                self.kind = "bulge"
            else:
                self.kind = "interior"
            for sl, _ in self.segs:
                if set(sl) <= set("C"):
                    self.iside = len(sl) - 2
                else:
                    self.tside = sl[1:-1]
        else:
            self.kind = "multi"
        # flush nicked stack: exterior loop with 2 chords and no unpaired base
        self.flush = (self.kind == "exterior" and self.k == 2 and self.unp == 0)


# ----------------------------------------------------------------- energy models
class Model:
    """loop-energy function on Face objects; integer (or Fraction) valued"""

    def __init__(self, name, sigma=-1, fn=None, ext=None, hyp=True):
        self.name, self.sigma, self.fn, self.ext, self.hyp = name, sigma, fn, ext, hyp

    def g(self, f):
        if f.kind == "exterior":
            return self.ext(f) if self.ext else 0
        if f.kind == "stack":
            return self.sigma
        if f.kind == "hairpin":
            return 12345  # cannot occur in the instances; arbitrary
        return self.fn(f) if self.fn else 0


def stable_rand(seed, s, lo, hi):
    h = hashlib.sha256(("%s|%s" % (seed, s)).encode()).digest()
    return lo + int.from_bytes(h[:8], "big") % (hi - lo + 1)


def models_H():
    """models satisfying (H0)-(H2)"""
    ms = [
        Model("stack-only s=-1", -1),
        Model("s=-7, bulge/int/multi=0", -7),
        Model("s=-1, bulge/int/multi=10^6", -1, lambda f: 10 ** 6),
        Model("s=-1000, bulge/int/multi=1", -1000, lambda f: 1),
        Model("s=-3, bulge(A only)=0 else 5", -3, lambda f: 0 if (f.kind == "bulge" and f.tside == "A") else 5),
        Model("s=-3, size-1 bulges 0, else 2*unp", -3, lambda f: 0 if (f.kind == "bulge" and f.unp == 1) else 2 * f.unp),
        Model("s=-2, item-side bulges 0, others 9", -2, lambda f: 0 if (f.kind == "bulge" and f.tside == "") else 9),
        Model("s=-2, interior 0, bulges 9", -2, lambda f: 0 if f.kind == "interior" else 9),
    ]
    for seed in range(6):
        sg = -stable_rand("sig%d" % seed, "", 1, 9)
        ms.append(Model("random>=0 seed %d s=%d" % (seed, sg), sg, (lambda sd: (lambda f: stable_rand(sd, f.s, 0, 12)))(seed)))
    return ms


def sig_energies(res, model, faces=None):
    """numpy int64 array: energy of every signature under the model (models are integer valued)"""
    import numpy as np
    if faces is None:
        faces = {i: Face(s) for i, s in res["desc"].items()}
    g = np.zeros(max(faces) + 1, dtype=np.int64)
    for i, f in faces.items():
        g[i] = model.g(f)
    nsig = len(res["lab"])
    E = np.zeros(nsig, dtype=np.int64)
    np.add.at(E, res["sidx"], g[res["ids"]])
    return E


def evaluate(res, model, faces=None):
    """returns dict energy -> [labelled count, physical count, tiling count]"""
    import numpy as np
    E = sig_energies(res, model, faces)
    u, inv = np.unique(E, return_inverse=True)
    hist = {}
    for name in ("lab", "phys", "til"):
        w = np.zeros(len(u), dtype=np.int64)
        np.add.at(w, inv, res[name])
        for e, c in zip(u.tolist(), w.tolist()):
            hist.setdefault(e, []).append(c)
    return hist
