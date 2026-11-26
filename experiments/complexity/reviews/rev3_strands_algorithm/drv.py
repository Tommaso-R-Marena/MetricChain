#!/usr/bin/env python3
"""Driver for the C++ brute force bfmod (referee).  Everything modulo P = 2^61 - 1."""
import subprocess, os, sys, hashlib, pickle
from fractions import Fraction
P = (1 << 61) - 1
LET = 'ACGT'
HERE = os.path.dirname(os.path.abspath(__file__))

def fmod(x):
    x = Fraction(x)
    return x.numerator % P * pow(x.denominator % P, P - 2, P) % P

_tab_cache = {}
def tables(model, Nmax):
    key = (model.name, Nmax)
    if key in _tab_cache:
        return _tab_cache[key]
    hp = []
    for u in range(Nmax + 1):
        for a in LET:
            for b in LET:
                hp.append(fmod(model.hp(u, a, b)))
    il = []
    for l1 in range(Nmax + 1):
        for a1 in LET:
            for b1 in LET:
                for l2 in range(Nmax + 1):
                    for a2 in LET:
                        for b2 in LET:
                            il.append(fmod(model.il(l1, a1, b1, l2, a2, b2)))
    s = ' '.join(map(str, hp)) + '\n' + ' '.join(map(str, il)) + '\n' + '%d %d %d\n' % (fmod(model.ma), fmod(model.mb), fmod(model.mc))
    _tab_cache[key] = s
    return s

def brute_mod(species, counts, model, alphas, mode=1, timeout=3000):
    """returns (dict R -> (count, [T_R(alpha) mod P])), nwords, nstructs"""
    N = sum(len(s) * n for s, n in zip(species, counts))
    inp = '%d\n' % len(species) + ''.join('%s %d\n' % (s, n) for s, n in zip(species, counts))
    inp += '%d %s\n%d\n%d\n' % (len(alphas), ' '.join(map(str, alphas)), mode, N) + tables(model, N)
    out = subprocess.run([os.path.join(HERE, 'bfmod')], input=inp, capture_output=True, text=True, timeout=timeout).stdout
    res = {}
    nw = ns = None
    for line in out.splitlines():
        f = line.split()
        if f[0] == 'words':
            nw, ns = int(f[1]), int(f[3])
        elif f[0] == 'R':
            res[int(f[1])] = (int(f[3]), [int(x) for x in f[4:]])
    return res, nw, ns

def Q_from_T(res, c, alphas):
    """(1/c) sum_R R^(1-alpha) T_R(alpha)  mod P"""
    out = {}
    for t, a in enumerate(alphas):
        tot = 0
        for R, (cnt, T) in res.items():
            e = 1 - a
            Rp = pow(R, e, P) if e >= 0 else pow(pow(R, P - 2, P), -e, P)
            tot = (tot + Rp * T[t]) % P
        out[a] = tot * pow(c, P - 2, P) % P
    return out

def F_from_T(res, d, t):
    """F_d(alpha_t) = sum over pairs with d | R of w^alpha"""
    return sum(T[t] for R, (cnt, T) in res.items() if R % d == 0) % P
