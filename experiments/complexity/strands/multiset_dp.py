"""
Magnified partition function of the multi-stranded nearest-neighbour model, summed over ALL circular
orderings of the strands at once, with rotational symmetry, by dynamic programming over sub-multisets
of strand species.  Exact arithmetic (Fractions) for validation against ref_enum.py.

Model (weights instead of energies; W(loop) = exp(-g(loop)/kT)):
    hairpin with u unpaired bases                         : hp(u)
    two-pair loop (stack / bulge / interior), sides l1,l2 : il(l1, l2)      (must satisfy il(l1,l2) = il(l2,l1))
    multiloop with b pairs and u unpaired bases           : ma * mb**b * mc**u
    exterior loop (a loop with a nick)                    : 1
A physical structure S (strands with equal sequence indistinguishable) with rotational symmetry R(S) has
magnified weight  (prod of loop weights)**alpha * R(S)**(-alpha)   (association term omitted: it is the
constant factor exp(-alpha (c-1) dG_assoc / kT)).

Formula implemented (docs/complexity/STRANDS_ALGORITHM.md):
    Q_alpha = (1/c) * sum_{d | gcd(n_i)} J_{1-alpha}(d) * G_d(alpha)
    G_1  = sum over linear sequences Y of all strands of  Q_Y[1..N]            (magnification alpha)
    G_d  = sum over linear sequences y of one period, of the d-fold symmetric structures on y^d
           = sum over (designated nest, marked nick inside it, top segment)    (tables at magnification d*alpha)
    J_k(d) = sum_{e | d} mu(d/e) e^k      (Jordan totient, here with exponent k = 1 - alpha)
"""
from fractions import Fraction
from functools import lru_cache
from math import gcd

PAIR = {("A", "T"), ("T", "A"), ("C", "G"), ("G", "C")}


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def mobius(n):
    if n == 1:
        return 1
    r, p, m = 1, 2, n
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            r = -r
        p += 1
    if m > 1:
        r = -r
    return r


def jordan(k, d):
    """J_k(d) = sum_{e|d} mu(d/e) e^k, exact for integer k (possibly negative)."""
    return sum(mobius(d // e) * Fraction(e) ** k for e in divisors(d))


class Model:
    def __init__(self, hp, il, ma, mb, mc):
        self.hp, self.il, self.ma, self.mb, self.mc = hp, il, Fraction(ma), Fraction(mb), Fraction(mc)


class Tables:
    """DP tables for a list of species (sequences), at magnification exponent gamma (loop weights ** gamma).
    Indices inside strands are 1-based.  A multiset of species is a tuple of counts."""

    def __init__(self, species, model, gamma):
        self.sp = species
        self.k = len(species)
        self.m = model
        self.g = gamma
        self.len = [len(w) for w in species]
        self._qs = {}
        self._qbs = {}
        self._qms = {}
        self._q = {}
        self._qb = {}
        self._qm = {}

    # ---- helpers
    def can(self, s, i, t, j):
        return (self.sp[s][i - 1], self.sp[t][j - 1]) in PAIR

    def B(self):
        return self.m.mb ** self.g

    def C(self, u):
        return self.m.mc ** (self.g * u)

    def submultisets(self, A):
        """all (L, R) with L + R = A"""
        def rec(idx):
            if idx == self.k:
                yield ()
                return
            for x in range(A[idx] + 1):
                for rest in rec(idx + 1):
                    yield (x,) + rest
        for L in rec(0):
            yield L, tuple(a - l for a, l in zip(A, L))

    def minus(self, A, u):
        return tuple(a - (1 if x == u else 0) for x, a in enumerate(A))

    def size(self, A):
        return sum(A)

    # ---- single-strand tables: stretch s[i..j] (i <= j+1)
    def Qs(self, s, i, j):
        """nick-free top level trivially; any structure on s[i..j] (weights of enclosed loops)."""
        if j < i:
            return Fraction(1)
        key = (s, i, j)
        if key in self._qs:
            return self._qs[key]
        tot = Fraction(1)
        for e in range(i + 1, j + 1):
            for d in range(i, e):
                if self.can(s, d, s, e):
                    b = self.QBs(s, d, e)
                    if b:
                        tot += self.Qs(s, i, d - 1) * b
        self._qs[key] = tot
        return tot

    def QBs(self, s, i, j):
        """i and j (same strand, i<j) paired."""
        key = (s, i, j)
        if key in self._qbs:
            return self._qbs[key]
        tot = Fraction(0)
        if self.can(s, i, s, j):
            g = self.g
            tot += Fraction(self.m.hp(j - i - 1)) ** g
            for d in range(i + 1, j - 1):
                for e in range(d + 1, j):
                    if self.can(s, d, s, e):
                        tot += Fraction(self.m.il(d - i - 1, j - e - 1)) ** g * self.QBs(s, d, e)
            # multiloop: closing pair + >= 2 inner branches
            pre = self.m.ma ** g * self.B()
            for e in range(i + 2, j):
                for d in range(i + 2, e):
                    if self.can(s, d, s, e):
                        left = self.QMs(s, i + 1, d - 1)
                        if left:
                            tot += pre * left * self.B() * self.QBs(s, d, e) * self.C(j - 1 - e)
        self._qbs[key] = tot
        return tot

    def QMs(self, s, i, j):
        """multiloop segment on s[i..j] with >= 1 branch (weights mb per branch, mc per unpaired)."""
        if j <= i:
            return Fraction(0)
        key = (s, i, j)
        if key in self._qms:
            return self._qms[key]
        tot = Fraction(0)
        for e in range(i + 1, j + 1):
            for d in range(i, e):
                if self.can(s, d, s, e):
                    b = self.QBs(s, d, e)
                    if b:
                        tot += (self.C(d - i) + self.QMs(s, i, d - 1)) * self.B() * b * self.C(j - e)
        self._qms[key] = tot
        return tot

    # ---- split stretches: s[i..|s|], strands of A in any order, t[1..j]   (1 <= i <= |s|, 1 <= j <= |t|)
    def Q(self, s, i, t, j, A):
        """structures with nick-free top level (so at least one pair)."""
        key = (s, i, t, j, A)
        if key in self._q:
            return self._q[key]
        tot = Fraction(0)
        for e in range(1, j + 1):
            # rightmost top-level pair (d,e), e in t; tail t[e+1..j] unpaired
            # d in t
            for d in range(2, e):
                if self.can(t, d, t, e):
                    b = self.QBs(t, d, e)
                    if b:
                        tot += self.Q(s, i, t, d - 1, A) * b
            # d in s
            for d in range(i, self.len[s] + 1):
                if self.can(s, d, t, e):
                    b = self.QB(s, d, t, e, A)
                    if b:
                        tot += self.Qs(s, i, d - 1) * b
            # d in a strand u of A
            for u in range(self.k):
                if A[u] == 0:
                    continue
                Au = self.minus(A, u)
                for AL, AR in self.submultisets(Au):
                    for d in range(2, self.len[u] + 1):
                        if self.can(u, d, t, e):
                            b = self.QB(u, d, t, e, AR)
                            if b:
                                tot += self.Q(s, i, u, d - 1, AL) * b
        self._q[key] = tot
        return tot

    def QM(self, s, i, t, j, A):
        """as Q, with multiloop weights on the top level."""
        key = (s, i, t, j, A)
        if key in self._qm:
            return self._qm[key]
        tot = Fraction(0)
        for e in range(1, j + 1):
            tail = self.C(j - e)
            for d in range(2, e):
                if self.can(t, d, t, e):
                    b = self.QBs(t, d, e)
                    if b:
                        tot += self.QM(s, i, t, d - 1, A) * self.B() * b * tail
            for d in range(i, self.len[s] + 1):
                if self.can(s, d, t, e):
                    b = self.QB(s, d, t, e, A)
                    if b:
                        tot += (self.C(d - i) + self.QMs(s, i, d - 1)) * self.B() * b * tail
            for u in range(self.k):
                if A[u] == 0:
                    continue
                Au = self.minus(A, u)
                for AL, AR in self.submultisets(Au):
                    for d in range(2, self.len[u] + 1):
                        if self.can(u, d, t, e):
                            b = self.QB(u, d, t, e, AR)
                            if b:
                                tot += self.QM(s, i, u, d - 1, AL) * self.B() * b * tail
        self._qm[key] = tot
        return tot

    def Rstart(self, A, t, j):
        """stretch starting at a strand boundary: all strands of A (any order), then t[1..j]; nick-free top level.
        j may be 0 (then the stretch ends at the nick before t)."""
        if self.size(A) == 0:
            return self.Qs(t, 1, j)          # = 1 if j == 0
        if j == 0:
            return Fraction(0)               # a second nick would lie on the loop
        tot = Fraction(0)
        for u in range(self.k):
            if A[u]:
                tot += self.Q(u, 1, t, j, self.minus(A, u))
        return tot

    def QB(self, s, i, t, j, A):
        """(s,i) paired with (t,j); s and t are different strand copies; A strictly between."""
        key = (s, i, t, j, A)
        if key in self._qb:
            return self._qb[key]
        tot = Fraction(0)
        if self.can(s, i, t, j):
            g = self.g
            ls = self.len[s]
            # interior loops / stacks / bulges: inner pair (d in s, e in t)
            for d in range(i + 1, ls + 1):
                for e in range(1, j):
                    if self.can(s, d, t, e):
                        b = self.QB(s, d, t, e, A)
                        if b:
                            tot += Fraction(self.m.il(d - i - 1, j - e - 1)) ** g * b
            # multiloop: top level of the inside is nick-free with >= 2 branches
            pre = self.m.ma ** g * self.B()
            tot += pre * self._QM2_inside(s, i, t, j, A)
            # exterior loop: exactly one nick on the loop
            # (a) the nick right after strand s
            tot += self.Qs(s, i + 1, ls) * self.Rstart(A, t, j - 1)
            # (b) the nick after a strand u of A (then the nick after s must be covered: i < |s|)
            if i < ls:
                for u in range(self.k):
                    if A[u] == 0:
                        continue
                    Au = self.minus(A, u)
                    for A1, A2 in self.submultisets(Au):
                        left = self.Q(s, i + 1, u, self.len[u], A1)
                        if left:
                            tot += left * self.Rstart(A2, t, j - 1)
        self._qb[key] = tot
        return tot

    def _QM2_inside(self, s, i, t, j, A):
        """multiloop interior of the pair (s,i)-(t,j): stretch s[i+1..], A, t[..j-1], nick-free top level,
        >= 2 branches, weights mb per branch, mc per unpaired."""
        ls = self.len[s]
        if i == ls or j == 1:
            return Fraction(0)        # a nick would lie on the loop
        tot = Fraction(0)
        jj = j - 1
        for e in range(1, jj + 1):
            tail = self.C(jj - e)
            # rightmost branch (d,e); the rest must contain >= 1 branch
            for d in range(2, e):
                if self.can(t, d, t, e):
                    b = self.QBs(t, d, e)
                    if b:
                        tot += self.QM(s, i + 1, t, d - 1, A) * self.B() * b * tail
            for d in range(i + 1, ls + 1):
                if self.can(s, d, t, e):
                    b = self.QB(s, d, t, e, A)
                    if b:
                        tot += self.QMs(s, i + 1, d - 1) * self.B() * b * tail
            for u in range(self.k):
                if A[u] == 0:
                    continue
                Au = self.minus(A, u)
                for AL, AR in self.submultisets(Au):
                    for d in range(2, self.len[u] + 1):
                        if self.can(u, d, t, e):
                            b = self.QB(u, d, t, e, AR)
                            if b:
                                tot += self.QM(s, i + 1, u, d - 1, AL) * self.B() * b * tail
        return tot


def G1(species, counts, model, alpha):
    """sum over all linear sequences Y of all strands of the partition function over connected non-crossing
    structures of the circular arrangement Y (magnification alpha)."""
    T = Tables(species, model, alpha)
    c = sum(counts)
    k = len(species)
    if c == 1:
        s = [x for x in range(k) if counts[x]][0]
        return T.Qs(s, 1, len(species[s]))
    tot = Fraction(0)
    M = tuple(counts)
    for s in range(k):
        if M[s] == 0:
            continue
        Ms = T.minus(M, s)
        for t in range(k):
            if Ms[t] == 0:
                continue
            A = T.minus(Ms, t)
            tot += T.Q(s, 1, t, len(species[t]), A)
    return tot


def Gd(species, counts, model, alpha, d):
    """sum over linear sequences y of one period (counts/d) of the d-fold symmetric structures on y^d."""
    assert d >= 2 and all(n % d == 0 for n in counts)
    k = len(species)
    g = d * alpha
    T = Tables(species, model, g)
    M = tuple(n // d for n in counts)
    tot = Fraction(0)
    ma_a = model.ma ** alpha
    for s in range(k):
        if M[s] == 0:
            continue
        Ms = T.minus(M, s)
        ls = len(species[s])
        # Case II: the designated nest runs from (s,i) through all other strands of the period to (s,j) of the
        # next copy of the same strand, j < i; top segment s[j+1..i-1].
        A = Ms
        nicks = T.size(A) + 1
        for i in range(2, ls + 1):
            for j in range(1, i):
                nest = T.QB(s, i, s, j, A)
                if not nest:
                    continue
                u = i - 1 - j
                # k = 1 nest per period
                if d == 2:
                    central = Fraction(model.il(u, u)) ** alpha
                else:
                    central = ma_a * T.B() * T.C(u)
                tot += nicks * nest * central
                # k >= 2: further branches in the top segment
                tot += nicks * nest * ma_a * T.B() * T.QMs(s, j + 1, i - 1)
        # Case I: nest from (s,i) to (t,j), t another strand of the period; top segment t[j+1..], A3, s[..i-1]
        for t in range(k):
            if Ms[t] == 0:
                continue
            Mst = T.minus(Ms, t)
            lt = len(species[t])
            for A, A3 in T.submultisets(Mst):
                nicks = T.size(A) + 1
                for i in range(2, ls + 1):
                    for j in range(1, lt):
                        nest = T.QB(s, i, t, j, A)
                        if not nest:
                            continue
                        top = T.QM(t, j + 1, s, i - 1, A3)
                        if top:
                            tot += nicks * nest * ma_a * T.B() * top
    return tot


def magnified_pf(species, counts, model, alpha):
    """Q_alpha over the physical ensemble (association factor omitted)."""
    c = sum(counts)
    gg = 0
    for n in counts:
        if n:
            gg = gcd(gg, n)
    tot = Fraction(0)
    for d in divisors(gg):
        G = G1(species, counts, model, alpha) if d == 1 else Gd(species, counts, model, alpha, d)
        tot += jordan(1 - alpha, d) * G
    return tot / c
