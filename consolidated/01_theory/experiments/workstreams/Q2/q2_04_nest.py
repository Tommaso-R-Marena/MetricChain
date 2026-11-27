#!/usr/bin/env python3
"""Workstream Q2, check 4: the nested design of Theorem A evaluated EXACTLY for a small number of epochs.

G_0 = T[base at accuracy X_B(n)];  for m < M:  G_{m,j} = S[G_{m,j-1}] (the slope step of Q_REPORT, class SLevel of
experiments/workstreams/Q/qscheme.py, unchanged),  G'_{m+1} = D'[G_{m,J_m}; phi_m, X_D(n; phi_m)],
G_{m+1} = T[G'_{m+1}];  the top chain delivers eps^, the others the accuracy 1.  The blocks of the chains are those
of the design (the same as in the formula (A.1), q2lib.E_new).

Every level is evaluated with the exact constants of Theorem 11.56; at every node the inequality of the induction,
   certified cost <= d B - sigma min(x, R d) + E(d, x; ln(1/delta) + d ln 2),
is checked with the error functions of the report (slope steps: the sharper term of Lemma U), and at every level
built the lemma that bounds its outer sample.

"proof": every family is the construction of its proposition and nothing else (pass-through only where the proof
uses it).  "min": at every node the cheaper, by certified cost, of the construction and the inner procedure.

usage: python3 q2_04_nest.py A B > out_q2_04_nest.txt          (stages A: M <= 1, B: M = 2; about 6 minutes)
       python3 q2_04_nest.py C > out_q2_04_nest_C.txt            (M = 2 at u = 1, n = 16 000, "proof" variant; 24 minutes)
       python3 q2_04_nest.py S > out_q2_04_nest_S.txt            (every n from 2 to 200; a few minutes)
       python3 q2_04_nest.py quick                                (10 seconds)
"""
import math
import os
import sys
import time

import numpy as np

import q2lib as L

sys.path.insert(0, os.path.join(L.HERE, '..', 'Q'))
import qscheme as S          # noqa: E402

Q = L.Q
LN2 = L.LN2
INF = L.INF
t0 = time.time()
quick = len(sys.argv) > 1 and sys.argv[1] == 'quick'


class SLevelSharp(S.SLevel):
    """the slope step of Q_REPORT (level and family unchanged) with the error term of Lemma U:
    sigma'(1 + c_log(n) + h) + ell_0(n, Lam)  in place of  c_S(n, Lam; B)"""

    def Ebound(self, d, x, Lam):
        cu = self.cube
        return self.inner.Ebound(d, min(x, 1.0), Lam + Q.qS(cu, d, Lam)) + L.cSe(cu, d, Lam, self.sigma, cu.h)


class SlopeOne:
    """a family with slope >= 1 on (0, R] read as slope one"""

    def __init__(self, inner):
        self.inner = inner
        assert inner.sigma >= 1 - 1e-12
        self.B, self.sigma, self.R = inner.B, 1.0, inner.R

    def Ebound(self, d, x, Lam):
        return self.inner.Ebound(d, x, Lam)

    def costs(self, d, xs, ld):
        return self.inner.costs(d, xs, ld)


def build(ev, n, eps, dl, M, seq, mode, st):
    """the family G_M with horizon n; returns (family, the detail of the formula (A.1), list of the parts)"""
    cu = ev.cu
    pr = L.E_new(cu, n, eps, dl, M, seq, detail=True)
    blocks = {c['e']: c['m'] for c in pr['chains']}
    eh = min(eps, 1.0)
    base = L.HiBase(cu, n, st)
    fam = L.ChainFam(ev, base, eh if M == 0 else 1.0, n, st, None, m=blocks[0])
    parts = dict(chains=[fam], slopes=[], drops=[])
    for m in range(M):
        for j in range(seq['J'][m]):
            fam = SLevelSharp(cu, fam, seq['B'][m], minrule=(mode == 'min'))
            parts['slopes'].append(fam)
        fam = L.DprimeFam(ev, SlopeOne(fam), seq['phi'][m], n, st, mode=mode)
        parts['drops'].append(fam)
        assert abs(fam.B - seq['B'][m + 1]) < 1e-12
        fam = L.ChainFam(ev, fam, eh if m + 1 == M else 1.0, n, st, None, m=blocks[m + 1])
        parts['chains'].append(fam)
    return fam, pr, parts


print("# Workstream Q2, check 4: the nested design of Theorem A, exact certified cost, node-by-node check of the induction")
print("# eps = 0.8715 (as in section 7.3 of Q_REPORT), delta = 0.05; costs and bounds in units of n a")
print("#  u    n     M  levels on a path  mode  | exact   bound of Theorem A   (n B_M)/(n a)  | chain levels evaluated; slope levels built; D' levels / passed through"
      " | node checks  viol  least slack: induction (chains, D', slope steps); D' as built; S as built; ball of the chains | time")
EPS = 0.8715
dl = math.log(20.0)
STAGES = {
    'A': ((1.0, (1000, 1400, 2000, 4000, 8000, 16000), (0, 1)), (2.0, (1000, 2000, 4000, 8000), (0, 1)), (0.5, (4000, 16000, 64000), (0, 1))),
    'B': ((1.0, (1000, 2000, 4000, 8000), (2,)), (2.0, (1000, 2000), (2,)), (0.5, (16000,), (2,))),
    'C': ((1.0, (16000,), (2,)),),          # "proof" variant only (24 minutes; 8.9 million node checks)
}
stages = [a for a in sys.argv[1:] if a in STAGES] or ([] if 'S' in sys.argv[1:] else ['A', 'B'])
plan = []
for st_ in stages:
    for u, ns, Ms in STAGES[st_]:
        for M in Ms:
            for n in ns:
                for mode in (('proof',) if st_ == 'C' else ('proof', 'min')):
                    plan.append((u, n, M, mode))
if quick:
    plan = [p for p in plan if p[1] <= 4000 and p[2] <= 1]
print("# stages: %s" % ", ".join(stages))
evs = {}
for (u, n, M, mode) in plan:
    if u not in evs:
        evs[u] = L.Ev(u, both=False)          # the nest uses qlib's evaluator (as qscheme's slope steps do); see checks 1, 2, 5 for both
    ev = evs[u]
    cu = ev.cu
    seq = Q.epoch_seq(cu, max(M, 1) + 1)
    st = L.Stat()
    S.reset_check()
    t1 = time.time()
    fam, pr, parts = build(ev, n, EPS, dl, M, seq, mode, st)
    v = float(fam.costs(n, np.array([min(EPS, 1.0)]), -dl)[0])
    na = n * cu.a
    bound = n * seq['B'][M] + pr['E']
    own = n * fam.B + fam.Ebound(n, min(EPS, 1.0), dl + n * LN2)
    kpath = 1 + sum(seq['J'][m] + 1 for m in range(M))
    nchain = sum(c.nlev for c in parts['chains'])
    nS = sum(s.nconstruct for s in parts['slopes'])
    nD = sum(d.wins['level'] for d in parts['drops'])
    nDp = sum(d.wins['passthrough'] for d in parts['drops'])
    C = S.CHECK
    viol = len(st.viol) + C.viol + (1 if v > bound + 1e-9 or v > own + 1e-9 else 0)
    ms = st.minslack

    def g(name):
        return ms[name][0] if name in ms else float('nan')

    sS = C.by.get('S', [0, float('nan'), 0])[1]
    sSb = C.by.get('S as built', [0, float('nan'), 0])[1]
    print("  %.1f %6d  %d  %2d + chains  %-5s | %.4f  %.4f  %.4f | %d; %d; %d / %d | %d  %d  %.1f, %.1f, %.1f; %.1f; %.1f; %.1f | %.0f s"
          % (u, n, M, kpath, mode, v / na, bound / na, seq['B'][M] / cu.a, nchain, nS, nD, nDp, st.total() + C.n, viol,
             g('induction T'), g("induction D'"), sS, g("D' as built"), sSb, g('T: ln(1/pi_dagger) <= varpi'), time.time() - t1))
    for vv in st.viol[:5]:
        print("     VIOLATION:", vv)
    if C.viol:
        print("     VIOLATION (qscheme check):", C.worst)
    sys.stdout.flush()
# ------------------------------------------------------------------------------------------------ small sizes
if 'S' in sys.argv[1:]:
    print("\n# stage S: awkward small sizes -- every n from 2 to 200, M = 0, 1, 2, eps in {0.8715, 0.01}, delta in {0.05, e^{-n}}, both variants")
    print("#  u   M   designs   node checks   violations   least slack of the induction   chain levels / slope levels / D' levels built   largest exact cost / (n ln 2)")
    for u in (0.5, 1.0, 2.0):
        ev = L.Ev(u, both=True)
        cu = ev.cu
        for M in (0, 1, 2):
            seq = Q.epoch_seq(cu, max(M, 1) + 1)
            nd = nchk = nv = 0
            minsl = INF
            built = [0, 0, 0]
            worst = 0.0
            for n in range(2, 201):
                for eps in (0.8715, 0.01):
                    for dl_ in (math.log(20.0), float(n)):
                        for mode in ('proof', 'min'):
                            st = L.Stat()
                            S.reset_check()
                            fam, pr, parts = build(ev, n, eps, dl_, M, seq, mode, st)
                            v = float(fam.costs(n, np.array([min(eps, 1.0)]), -dl_)[0])
                            bound = n * seq['B'][M] + pr['E']
                            # at these sizes the top chain has no level (its block is longer than n), so the families
                            # below it are also called directly, in the dimension n: every D' and every slope family
                            for D_ in parts['drops']:
                                D_.costs(n, np.array([D_.calX]), -dl_)
                            for S_ in parts['slopes']:
                                S_.costs(n, np.array([1.0, 3.0, max(1.0, S_.R * n)]), -dl_)
                            nd += 1
                            nchk += st.total() + S.CHECK.n
                            nv += len(st.viol) + S.CHECK.viol + (1 if v > bound + 1e-9 else 0)
                            for k_, (sl_, _) in st.minslack.items():
                                if k_.startswith('induction'):
                                    minsl = min(minsl, sl_)
                            minsl = min(minsl, S.CHECK.minslack, bound - v)
                            built[0] += sum(c.nlev for c in parts['chains'])
                            built[1] += sum(s_.nconstruct for s_ in parts['slopes'])
                            built[2] += sum(d.wins['level'] for d in parts['drops'])
                            worst = max(worst, v / (n * LN2))
            print("  %.1f  %d  %5d  %7d  %3d   %8.2f   %d / %d / %d   %.4f   [%.0f s]" % (u, M, nd, nchk, nv, minsl, built[0], built[1], built[2], worst, time.time() - t0))
            sys.stdout.flush()

print("\n# done in %.0f s" % (time.time() - t0))
