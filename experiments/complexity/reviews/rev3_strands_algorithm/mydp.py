#!/usr/bin/env python3
"""
Referee's own implementation of the algorithm described in STRANDS_ALGORITHM.md (sections 2-4), written from
the document, WITH letter-dependent hairpin and two-pair-loop weights (the document allows them; the author's
implementation does not have them).  Arithmetic modulo P = 2^61 - 1.

Model: bf.Model (hp(u,a,b), il(l1,a1,b1,l2,a2,b2) invariant under exchange of the two segments, ma, mb, mc).
"""
import sys
from functools import lru_cache
from math import gcd

sys.setrecursionlimit(100000)
P = (1 << 61) - 1
PAIRS = {('A', 'T'), ('T', 'A'), ('C', 'G'), ('G', 'C')}


def fmod(x):
    from fractions import Fraction
    x = Fraction(x)
    return x.numerator % P * pow(x.denominator % P, P - 2, P) % P


def mpow(x, e):
    """x^e mod P for integer e (negative allowed, x != 0 then); 0^0 = 1"""
    if e >= 0:
        return pow(x, e, P)
    return pow(pow(x, P - 2, P), -e, P)


def mobius(n):
    r, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            r = -r
        p += 1
    if n > 1:
        r = -r
    return r


def jordan(k, d):
    return sum(mobius(d // e) * mpow(e, k) for e in range(1, d + 1) if d % e == 0) % P


class Tab:
    def __init__(self, species, model, gamma):
        self.sp = species
        self.k = len(species)
        self.len = [len(w) for w in species]
        self.g = gamma
        m = model
        self.ma = mpow(fmod(m.ma), gamma)
        self.mb = mpow(fmod(m.mb), gamma)
        self.mcb = mpow(fmod(m.mc), gamma)
        self._hp = {}
        self._il = {}
        self.model = m
        for name in ('Qs', 'QBs', 'QMs', 'Q', 'QM', 'QB', 'QM2', 'Rst'):
            setattr(self, '_' + name, {})

    def mc(self, u):
        return pow(self.mcb, u, P)

    def hp(self, u, a, b):
        key = (u, a, b)
        if key not in self._hp:
            self._hp[key] = mpow(fmod(self.model.hp(u, a, b)), self.g)
        return self._hp[key]

    def il(self, l1, a1, b1, l2, a2, b2):
        key = (l1, a1, b1, l2, a2, b2)
        if key not in self._il:
            self._il[key] = mpow(fmod(self.model.il(l1, a1, b1, l2, a2, b2)), self.g)
        return self._il[key]

    def L(self, s, i):
        return self.sp[s][i - 1]

    def can(self, s, i, t, j):
        return (self.sp[s][i - 1], self.sp[t][j - 1]) in PAIRS

    # ------------------------------------------------------------ inside one strand
    def Qs(self, s, i, j):
        if j < i:
            return 1
        key = (s, i, j)
        v = self._Qs.get(key)
        if v is None:
            v = 1
            for e in range(i + 1, j + 1):
                for d in range(i, e):
                    if self.can(s, d, s, e):
                        v += self.Qs(s, i, d - 1) * self.QBs(s, d, e)
            v %= P
            self._Qs[key] = v
        return v

    def QBs(self, s, i, j):
        key = (s, i, j)
        v = self._QBs.get(key)
        if v is None:
            v = 0
            if self.can(s, i, s, j):
                a, b = self.L(s, i), self.L(s, j)
                v = self.hp(j - i - 1, a, b)
                for d in range(i + 1, j):
                    for e in range(d + 1, j):
                        if self.can(s, d, s, e):
                            v += self.il(d - i - 1, a, self.L(s, d), j - e - 1, self.L(s, e), b) * self.QBs(s, d, e)
                # multiloop: rightmost inner branch (d,e), at least one more branch to its left
                acc = 0
                for e in range(i + 2, j):
                    for d in range(i + 1, e):
                        if self.can(s, d, s, e):
                            acc += self.QMs(s, i + 1, d - 1) * self.QBs(s, d, e) % P * self.mc(j - 1 - e)
                v += self.ma * self.mb % P * self.mb % P * (acc % P)
                v %= P
            self._QBs[key] = v
        return v

    def QMs(self, s, i, j):
        if j <= i:
            return 0
        key = (s, i, j)
        v = self._QMs.get(key)
        if v is None:
            v = 0
            for e in range(i + 1, j + 1):
                for d in range(i, e):
                    if self.can(s, d, s, e):
                        v += (self.mc(d - i) + self.QMs(s, i, d - 1)) * self.mb % P * self.QBs(s, d, e) % P * self.mc(j - e)
            v %= P
            self._QMs[key] = v
        return v

    # ------------------------------------------------------------ multisets
    def subs(self, A):
        """all sub-multisets AL of A with complement"""
        res = [()]
        for x in A:
            res = [r + (y,) for r in res for y in range(x + 1)]
        return [(L, tuple(a - l for a, l in zip(A, L))) for L in res]

    def minus(self, A, u):
        return A[:u] + (A[u] - 1,) + A[u + 1:]

    # ------------------------------------------------------------ split stretches (s,i;A;t,j)
    def _top(self, s, i, t, j, A, multi, need2):
        """common recursion for Q (multi=False), QM (multi=True) and the '>= 2 branches' variant (need2=True,
        used for the inside of a multiloop).  Decomposition by the rightmost top-level pair (d,e), e in t."""
        tot = 0
        B = self.mb if multi else 1
        for e in range(1, j + 1):
            tail = self.mc(j - e) if multi else 1
            part = 0
            # d in t (d >= 2): everything else is to the left and must itself have nick-free top level
            for d in range(2, e):
                if self.can(t, d, t, e):
                    left = self.QM(s, i, t, d - 1, A) if multi else self.Q(s, i, t, d - 1, A)
                    part += left * self.QBs(t, d, e)
            # d in s: the left part is s[i..d-1], inside one strand
            for d in range(i, self.len[s] + 1):
                if self.can(s, d, t, e):
                    if multi:
                        left = self.QMs(s, i, d - 1) + (0 if need2 else self.mc(d - i))
                    else:
                        left = self.Qs(s, i, d - 1)
                    if left:
                        part += left * self.QB(s, d, t, e, A)
            # d in a strand u of A
            for u in range(self.k):
                if A[u]:
                    for AL, AR in self.subs(self.minus(A, u)):
                        for d in range(2, self.len[u] + 1):
                            if self.can(u, d, t, e):
                                left = self.QM(s, i, u, d - 1, AL) if multi else self.Q(s, i, u, d - 1, AL)
                                if left:
                                    part += left * self.QB(u, d, t, e, AR)
            tot += part % P * B % P * tail
        return tot % P

    def Q(self, s, i, t, j, A):
        key = (s, i, t, j, A)
        v = self._Q.get(key)
        if v is None:
            v = self._top(s, i, t, j, A, False, False) if j >= 1 and i <= self.len[s] else 0
            self._Q[key] = v
        return v

    def QM(self, s, i, t, j, A):
        key = (s, i, t, j, A)
        v = self._QM.get(key)
        if v is None:
            v = self._top(s, i, t, j, A, True, False) if j >= 1 and i <= self.len[s] else 0
            self._QM[key] = v
        return v

    def QM2(self, s, i, t, j, A):
        """as QM but with at least two top-level pairs"""
        key = (s, i, t, j, A)
        v = self._QM2.get(key)
        if v is None:
            v = self._top(s, i, t, j, A, True, True) if j >= 1 and i <= self.len[s] else 0
            self._QM2[key] = v
        return v

    def Rst(self, A, t, j):
        """all strands of A in any order, then t[1..j] (j may be 0); nick-free top level"""
        key = (A, t, j)
        v = self._Rst.get(key)
        if v is None:
            if sum(A) == 0:
                v = self.Qs(t, 1, j)
            elif j == 0:
                v = 0
            else:
                v = sum(self.Q(u, 1, t, j, self.minus(A, u)) for u in range(self.k) if A[u]) % P
            self._Rst[key] = v
        return v

    def QB(self, s, i, t, j, A):
        key = (s, i, t, j, A)
        v = self._QB.get(key)
        if v is None:
            v = 0
            if self.can(s, i, t, j):
                a, b = self.L(s, i), self.L(t, j)
                ls = self.len[s]
                # two-pair loop, inner pair (d in s, e in t)
                for d in range(i + 1, ls + 1):
                    for e in range(1, j):
                        if self.can(s, d, t, e):
                            v += self.il(d - i - 1, a, self.L(s, d), j - e - 1, self.L(t, e), b) * self.QB(s, d, t, e, A)
                # multiloop
                if i < ls and j > 1:
                    v += self.ma * self.mb % P * self.QM2(s, i + 1, t, j - 1, A)
                # exterior loop, the nick after s
                v += self.Qs(s, i + 1, ls) * self.Rst(A, t, j - 1)
                # exterior loop, the nick after a strand u of A
                if i < ls:
                    for u in range(self.k):
                        if A[u]:
                            for A1, A2 in self.subs(self.minus(A, u)):
                                left = self.Q(s, i + 1, u, self.len[u], A1)
                                if left:
                                    v += left * self.Rst(A2, t, j - 1)
                v %= P
            self._QB[key] = v
        return v


def F1(species, counts, model, alpha):
    T = Tab(species, model, alpha)
    M = tuple(counts)
    if sum(M) == 1:
        s = [x for x in range(len(species)) if M[x]][0]
        return T.Qs(s, 1, len(species[s]))
    tot = 0
    for s in range(T.k):
        if M[s]:
            Ms = T.minus(M, s)
            for t in range(T.k):
                if Ms[t]:
                    tot += T.Q(s, 1, t, T.len[t], T.minus(Ms, t))
    return tot % P


def Fd(species, counts, model, alpha, d):
    T = Tab(species, model, d * alpha)
    T1 = Tab(species, model, alpha)          # only for the weights of the central loop
    M = tuple(n // d for n in counts)
    tot = 0
    for s in range(T.k):
        if not M[s]:
            continue
        Ms = T.minus(M, s)
        ls = T.len[s]
        # (II) nest from (s,i) through all other strands of the period to (s,j) of the next copy, j < i
        nn = sum(Ms) + 1
        for i in range(2, ls + 1):
            for j in range(1, i):
                nest = T.QB(s, i, s, j, Ms)
                if not nest:
                    continue
                u = i - 1 - j
                if d == 2:
                    # central two-pair loop: segments (s,j) -> u unpaired -> (s,i), twice
                    central = T1.il(u, T.L(s, j), T.L(s, i), u, T.L(s, j), T.L(s, i))
                else:
                    central = T1.ma * T.mb % P * T.mc(u) % P
                tot += nn * nest % P * central
                tot += nn * nest % P * T1.ma % P * T.mb % P * T.QMs(s, j + 1, i - 1)
        # (I) nest from (s,i) to (t,j), t a different strand of the period
        for t in range(T.k):
            if not Ms[t]:
                continue
            Mst = T.minus(Ms, t)
            for A, A3 in T.subs(Mst):
                nn = sum(A) + 1
                for i in range(2, ls + 1):
                    for j in range(1, T.len[t]):
                        nest = T.QB(s, i, t, j, A)
                        if nest:
                            tot += nn * nest % P * T1.ma % P * T.mb % P * T.QM(t, j + 1, s, i - 1, A3)
    return tot % P


def magnified_pf(species, counts, model, alpha):
    c = sum(counts)
    g = 0
    for n in counts:
        g = gcd(g, n)
    tot = 0
    for d in range(1, g + 1):
        if g % d == 0:
            F = F1(species, counts, model, alpha) if d == 1 else Fd(species, counts, model, alpha, d)
            tot += jordan(1 - alpha, d) * F
    return tot % P * pow(c, P - 2, P) % P
