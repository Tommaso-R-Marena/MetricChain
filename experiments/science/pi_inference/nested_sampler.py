#!/usr/bin/env python3
"""The theory division's NESTED SAMPLER (their Proposition 11.113a; read in THY-RES-0012 section 2.3 at theory commit
f7df44f, not in their report) on our certified sandwiches -- coordinator's script, written at their request
(THY-RES-0012, request 2).

Their statement, in our units.  Let m_- <= e_- <= E <= e_+ <= m_+ pointwise, m_-/+ exactly solvable, e_-/+ computable
at a state WITHOUT an evaluation of E.  With q ~ exp(-beta m_-) - exp(-beta m_+), A = Z(m_-) - Z(m_+) and, at a state,
U = beta (m_+ - m_-), u_- = beta (e_- - m_-), u_+ = beta (e_+ - m_-), r = beta (E - m_-):
    b    = (e^{-u_+} - e^{-U}) / (1 - e^{-U}),            [their "beta"; renamed, beta is 1/kT here]
    rho  = (e^{-u_-} - e^{-u_+}) / (1 - e^{-U}),
    W_in = (e^{-r} - e^{-u_+}) / (e^{-u_-} - e^{-u_+}),
    W = b + rho W_in,   Z(e_+) = Z(m_+) + A E_q b,   Z(e_-) - Z(e_+) = A E_q rho,   Z(E) = Z(m_+) + A E_q W.
Algorithm: propose from q (a draw of pi_{m_-} accepted with probability 1 - e^{-U}); compute b and rho at the proposal;
evaluate E only with probability rho.  With N_f proposals (N_f FIXED IN ADVANCE) and N evaluations (the first N accepted:
a rule that looks at the acceptance indicators only -- the scheme under which the bound is proved, as our review
workstream R15 spells out; "propose until N are accepted" is not covered), with probability
>= 1 - delta:   |E_q W - (mean b + mean rho x mean W_in)| <= 2 t_f + mean rho x t,
t_f = sqrt(ln(6/delta)/(2 N_f)),  t = sqrt(ln(6/delta)/(2 N))   (three two-sided Hoeffding bounds, delta/3 each).

The inner sandwich used here: the envelope of the anchored expansion, the pointwise smallest penalty that workstream
P3's certified constants allow (addendum A17 (15)),
    e_-/+ (x) = f(x) + I~_{m-1} g (x)  -/+  [ env(x) + a(t) + EPS_G ],    clipped into [m_-(x), m_+(x)],
    env(x) = sum of chat_T over the m-subsets T of the changed set S(x)       (closed form: workstream P6's sum with the
             complement of S(x) excluded -- no subset is enumerated; rounded up by P3's factor),
    a(t)   = EPS_G x (sum of the absolute coefficients with which evaluated ball values enter I~_{m-1} g at a state
             with t changed sites) = EPS_G x sum_{v=0}^{m-1} C(t, v) C(t-v-1, m-1-v)  for t >= m   [derived below],
and, at a state INSIDE the ball (t < m), e_- = e_+ = the cached evaluated energy: rho = 0, never evaluated.
Clipping makes the nesting m_- <= e_- <= e_+ <= m_+ hold by construction, whatever the bookkeeping of allowances in
the outer models; it is counted and reported (it should never be active).
Target of the estimator: Z(E^) with E^ = the evaluated energy clipped into [m_-, m_+]; |E^ - E| <= EPS_G, so
|ln Z(E^) - ln Z(E)| <= beta EPS_G, which is added to both ends (the theory division's sharper form of the rounding
remark, THY-RES-0012 section 2.2: the allowance enters once and unamplified).

Coefficients of the ball values in the interpolant.  I_M g (x) = sum_{U subset S, |U| <= M} d_U(x_U), d_U = the
alternating sum over V subset U of g(x_V; x0 elsewhere).  So the coefficient of g(x_V) is
sum_{j=0}^{M-|V|} (-1)^j C(t-|V|, j) = (-1)^{M-|V|} C(t-|V|-1, M-|V|) for t > |V| (and 1 for t = |V|, where every other
coefficient vanishes if t <= M).  `coeff_abs_sum` checks the closed form against brute force.

Modes
  python3 -B nested_sampler.py SEQ BB m w FORM MODELS --enum [--reps R] [--N n] [--Nf nf]
        enumerable instance: every identity by enumeration; coverage over R repetitions of the algorithm; the plain
        sandwich sampler (Proposition 11.113) with the same number of evaluations, for comparison.
  python3 -B nested_sampler.py SEQ BB m w FORM MODELS [--N n] [--Nf nf] [--w3 w3] [--seed s]
        one run: N_f proposals, N evaluations of the solvent term; and the plain sampler with N evaluations.
FORM: S (site shares, P3), B (banded pair shares, P6), T (banded triple shares, P6).
MODELS: reduced (the workstreams' models: P3's reduction of evaluated terms to pair tables) or window (exact in-window
evaluated terms, window_model.py).
What is whose: the algorithm and its error bound -- the theory division; the certified constants, the ball, the
evaluator and the band models -- workstream P3; the closed-form sums and the share forms -- workstream P6; the window
models, the inner sandwich as built here (clipping, allowances, ball states), this driver -- the coordinator.
Model-relative; the certified constants are P3's paper proofs; EPS_G is an allowance.  Nothing is written into a
workstream directory.
"""
import os, sys, math, json, time, glob, shutil, importlib, itertools, resource
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "ws_P6"))
import p6lib as L
T9 = importlib.import_module("p6_09_triple")
sys.path.insert(0, HERE)
import window_model
pw = L.pw; BETA = L.BETA; EPS_G = L.EPS_G
WindowModel, build_window_models, diff_window = window_model.make(pw)
CACHE = os.path.join(HERE, "serine_helix_reach_cache"); os.makedirs(CACHE, exist_ok=True)
for src in ("ws_P5", "ws_P6", "ws_P3"):
    for pat in ("atom_*.npz", "zeta_*.npz", "enum_*.npy"):
        for fn in glob.glob(os.path.join(SCI, src, "cache", pat)):
            dst = os.path.join(CACHE, os.path.basename(fn))
            if not os.path.exists(dst): shutil.copy(fn, dst)
L.encl.CACHE = CACHE; L.MYCACHE = CACHE


def log(s): print(s, flush=True)


def opt(a, key, default, cast=str):
    return cast(a[a.index(key) + 1]) if key in a else default


def coeff_abs_sum(t, M):
    """sum over V subset S (|S| = t), |V| <= M, of |coefficient of g(x_V) in I_M g(x)|."""
    if t <= M: return 1.0
    return float(sum(math.comb(t, v) * math.comb(t - v - 1, M - v) for v in range(M + 1)))


def _coeff_abs_sum_brute(t, M):
    tot = 0.0
    for v in range(min(t, M) + 1):
        c = sum((-1) ** j * math.comb(t - v, j) for j in range(0, M - v + 1) if j <= t - v)
        tot += math.comb(t, v) * abs(c)
    return tot


for _t in range(0, 14):
    for _M in range(1, 7):
        assert abs(coeff_abs_sum(_t, _M) - _coeff_abs_sum_brute(_t, _M)) < 1e-9, (_t, _M)


class Envelope:
    """env(x) = sum of chat_T over the m-subsets of the changed set.  Two ways, which agree (checked in --enum mode):
    'table' (when C(n, m) <= 6000): every chat_T once, by workstream P6's closed form with the complement of T
    excluded (cached on disk), then subset sums;  otherwise one closed-form sum per distinct changed set (the
    complement of the changed set excluded -- no subset is enumerated), cached by the bitmask of the changed set."""

    def __init__(self, GF, m, n, x0, tag=None):
        self.B = L.GFBatch(GF); self.m = m; self.n = n; self.x0 = np.asarray(x0); self.cache = {}; self.seconds = 0.0
        self.pow = (1 << np.arange(n)).astype(np.int64); self.table = math.comb(n, m) <= 6000; self.nsets = 0
        if self.table:
            subs = list(itertools.combinations(range(n), m)); self.Tmask = np.array([sum(1 << i for i in T) for T in subs], dtype=np.int64)
            fn = os.path.join(CACHE, f"chat_{tag}_m{m}.npz") if tag else None
            if fn and os.path.exists(fn) and list(np.load(fn)["anchor"]) == [int(v) for v in x0] and len(np.load(fn)["chat"]) == len(subs):
                self.chat = np.load(fn)["chat"]
            else:
                t1 = time.time(); full = (1 << n) - 1; out = []
                for s_ in range(0, len(subs), 256):
                    ex = [tuple(i for i in range(n) if i not in T) for T in subs[s_:s_ + 256]]
                    se, cr = self.B.totals(m, ex); out.append(se + cr)
                self.chat = np.concatenate(out); self.seconds += time.time() - t1
                if fn: np.savez(fn, chat=self.chat, anchor=np.array(x0))

    def masks(self, st):
        return ((np.atleast_2d(st) != self.x0[None]) * self.pow[None]).sum(1)

    def value(self, st):
        mk = self.masks(st); uniq = np.unique(mk)
        if self.table:
            lut = np.empty(len(uniq))
            for s_ in range(0, len(uniq), 2000):
                u = uniq[s_:s_ + 2000]; lut[s_:s_ + 2000] = ((self.Tmask[None, :] & ~u[:, None]) == 0) @ self.chat
            self.nsets = max(self.nsets, len(uniq))
            return lut[np.searchsorted(uniq, mk)]
        todo = [int(u) for u in uniq if int(u) not in self.cache]
        for u in todo:
            if bin(u).count("1") < self.m: self.cache[u] = 0.0
        todo = [u for u in todo if bin(u).count("1") >= self.m]
        t1 = time.time()
        for s_ in range(0, len(todo), 256):
            chunk = todo[s_:s_ + 256]
            ex = [tuple(i for i in range(self.n) if not (u >> i) & 1) for u in chunk]
            se, cr = self.B.totals(self.m, ex)
            for u, v in zip(chunk, se + cr): self.cache[u] = float(v)
        self.seconds += time.time() - t1; self.nsets = len(self.cache)
        lut = np.array([self.cache[int(u)] for u in uniq])
        return lut[np.searchsorted(uniq, mk)]

    def value_closed_form(self, st):
        """the closed form with the complement of the changed set excluded, for a check of the table."""
        mk = self.masks(st); uniq = np.unique(mk)
        ex = [tuple(i for i in range(self.n) if not (int(u) >> i) & 1) for u in uniq]
        se, cr = self.B.totals(self.m, ex); lut = np.where(np.array([bin(int(u)).count("1") for u in uniq]) < self.m, 0.0, se + cr)
        return lut[np.searchsorted(uniq, mk)]


def build(seq, bb, m, w, form, models, w3=None):
    """everything the sampler needs for one instance; mirrors steps (1)-(4) of serine_helix_reach.py."""
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    w3 = w if w3 is None else w3; M = m - 1
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k)
    GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m)
    excl = L.exclusion_sets(n, None)
    fps = os.path.join(CACHE, f"pairsums_{seq.replace(':', 'c')}_{bb}_m{m}.npz")
    fp6 = os.path.join(SCI, "ws_P6", "out", f"pairsums_{L.tagname(seq, bb, tau)}_m{m}.npz")
    if os.path.exists(fps) and list(np.load(fps)["anchor"]) == [int(v) for v in x0]:
        tot_ex = np.load(fps)["tot"]; srcp = "this script's cache"
    elif os.path.exists(fp6) and list(np.load(fp6)["anchor"]) == [int(v) for v in x0] and len(np.load(fp6)["tot"]) == len(excl):
        z = np.load(fp6); val6 = {tuple(int(v) for v in e if v >= 0): float(t) for e, t in zip(z["excl"], z["tot"])}
        tot_ex = np.array([val6[tuple(e)] for e in excl]); srcp = "workstream P6's file " + os.path.basename(fp6)
    else:
        t1 = time.time(); se, cr = L.GFBatch(GF).totals(m, excl); tot_ex = se + cr
        np.savez(fps, tot=tot_ex, anchor=np.array(x0)); srcp = f"computed, {time.time() - t1:.0f}s"
    Gam, S, Gp = L.assemble_pair_sums(n, m, excl, tot_ex)
    val = {tuple(e): float(t) for e, t in zip(excl, tot_ex)}
    d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    if form == "S":
        tabs = (L.site_form(n, m, S, phi1), np.zeros((n, n)), None)
    elif form == "B":
        tabs = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, 5e-9 * Gam) + (None,)
    else:
        tris = T9.window_triples(n, w3)
        fpt = os.path.join(CACHE, f"triplesums_{seq.replace(':', 'c')}_{bb}_m{m}_w{w3}.npz")
        if os.path.exists(fpt) and list(np.load(fpt)["anchor"]) == [int(v) for v in x0]:
            t3 = np.load(fpt)["tot"]
        else:
            se, cr = L.GFBatch(GF).totals(m, tris); t3 = se + cr; np.savez(fpt, tot=t3, anchor=np.array(x0))
        H = {tr: (val[()] - val[(tr[0],)] - val[(tr[1],)] - val[(tr[2],)] + val[(tr[0], tr[1])] + val[(tr[0], tr[2])] + val[(tr[1], tr[2])]) - float(v)
             for tr, v in zip(tris, t3)}
        tabs = window_model.triple_form_two_windows(T9.window_triples, L.RND, n, m, w, w3, Gp, H, psi1, psi2, 5e-9 * Gam, 1e-8 * Gam)
    if models == "window":
        lo, up, info = build_window_models(k, x0, c0, h, J, d, w, L.EPS_G, M, *tabs); diff = diff_window(lo, up)
    else:
        if form == "T":
            lo, up = T9.build_triple_models(k, x0, c0, h, J, d, w, M, *tabs); diff = T9.diff_triple(lo, up)
        else:
            lo, up = L.build_models(k, x0, c0, h, J, d, w, M, tabs[0], tabs[1]); diff = L.diff_model(lo, up)
        info = dict(exact=0)
    return dict(seq=seq, bb=bb, tau=tau, m=m, M=M, w=w, w3=w3, form=form, models=models, G=G, c0=c0, h=h, J=J, x0=np.array(x0), E0=E0, n=n, k=k,
                GF=GF, Gam=Gam, d=d, nball=int(nball), srcb=srcb, srcp=srcp, lo=lo, up=up, diff=diff, info=info,
                env=Envelope(GF, m, n, x0, tag=f"{seq.replace(':', 'c')}_{bb}"))


def inner_bounds(I, st, ml, mu):
    """(e_-, e_+, number of states at which clipping was active, env) at the states st; no evaluation of E."""
    st = np.atleast_2d(st); x0 = I["x0"]; M = I["M"]
    t = (st != x0[None]).sum(1)
    base = pw.f_energy(st, I["c0"], I["h"], I["J"]) + pw.expansion_value(I["d"], st)
    env = I["env"].value(st)
    a = EPS_G * np.array([coeff_abs_sum(int(v), M) for v in t])
    half = np.where(t <= M, 0.0, env + a + EPS_G)
    el, eh = base - half, base + half
    clip = int(((el < ml - 1e-12) | (eh > mu + 1e-12)).sum())
    bad = int(((el > mu + 1e-9) | (eh < ml - 1e-9)).sum())                # would mean one of the two sandwiches is invalid
    return np.clip(el, ml, mu), np.clip(eh, ml, mu), clip, bad, env, base


def b_rho(ml, mu, el, eh):
    U = BETA * (mu - ml); um = BETA * (el - ml); up_ = BETA * (eh - ml)
    den = -np.expm1(-U)
    with np.errstate(divide="ignore", invalid="ignore"):
        b = np.where(den > 0, (np.exp(-up_) - np.exp(-U)) / den, 0.0)
        rho = np.where(den > 0, (np.exp(-um) - np.exp(-up_)) / den, 0.0)
    return np.clip(b, 0.0, 1.0), np.clip(rho, 0.0, 1.0)


def w_in(E, ml, el, eh):
    r = BETA * (E - ml); um = BETA * (el - ml); up_ = BETA * (eh - ml)
    return (np.exp(-r) - np.exp(-up_)) / (np.exp(-um) - np.exp(-up_))


def lnz_of(lnZup, D, v):
    return lnZup + math.log1p(math.expm1(D) * min(max(v, 0.0), 1.0))


def hoeff(nn, dl):
    """two-sided Hoeffding half-width for the mean of nn independent variables in an interval of length 1, level dl."""
    return math.sqrt(math.log(2 / dl) / (2 * nn)) if nn > 0 else 1.0


def eb(x, dl):
    """two-sided EMPIRICAL BERNSTEIN half-width for i.i.d. variables in [0, 1], level dl: the one-sided bound of Maurer and
    Pontil (2009), Theorem 4,   E Z - mean <= sqrt(2 V_n ln(2/d)/n) + 7 ln(2/d)/(3(n-1)),   V_n the unbiased sample
    variance, applied to x and to 1 - x at level d = dl/2 each.  (Statement read in the ar5iv rendering of
    arXiv:0907.3740v1 by a fetch subagent on 2026-11-26, and quoted in the same form by the theory division,
    THY-RES-0012 section 2.2; the proceedings version was not consulted.)"""
    nn = len(x)
    if nn < 2: return 1.0
    Lg = math.log(4 / dl)
    return min(1.0, math.sqrt(2 * float(np.var(x, ddof=1)) * Lg / nn) + 7 * Lg / (3 * (nn - 1)))


W0 = 0.5          # the fixed centre of the "one known mean" variant; fixed before any run, not tuned
KEYS = ("thy_H", "two_H", "one_H", "thy_EB", "two_EB", "one_EB")


def nested_brackets(bq, rq, win, lnZup, D, delta):
    """brackets of ln Z(E) from b and rho at the N_f proposals and W_in at the N evaluated states.
    'thy': the theory division's bound: |E_q W - (mean b + mean rho x mean W_in)| <= h_b + h_rho + mean rho x h_w
           (their 2 t_f + rho t when the three half-widths are Hoeffding's at level delta/3);
    'two': the TWO-END form found by our review workstream R15 (its addition A2): the error of the free part,
           (E_q b - mean b) + (E_q rho - mean rho) mu, is affine in mu = E_in W_in in [0, 1], hence at most the larger of
           its values at mu = 0 and mu = 1 -- the errors of the means of b and of b + rho (the two ends Z(e_+), Z(e_-)):
           |E_q W - (mean b + mean rho x mean W_in)| <= max(h_b, h_{b+rho}) + mean rho x h_w   (t_f + rho t with Hoeffding);
    'one': the coordinator's variant with ONE known mean.  c = b + rho W0 is computable without an evaluation and
           E_q W = E_q c + E_q rho x (E_in W_in - W0), so
           |E_q W - (mean c + mean rho x (mean W_in - W0))| <= h_c + h_rho (|mean W_in - W0| + h_w) + mean rho x h_w.
           (With Hoeffding half-widths 'two' is never wider than 'one'; with variance-sensitive half-widths 'one' can be
           much narrower, because c varies far less than b or b + rho.)
    Each with Hoeffding half-widths ('H') and with empirical Bernstein half-widths ('EB'); three two-sided events at
    level delta/3 in every case."""
    Nf, N = len(bq), len(win); bbar, rbar = float(bq.mean()), float(rq.mean()); wbar = float(win.mean()) if N else W0
    cq = bq + rq * W0; cbar = float(cq.mean()); eq = np.clip(bq + rq, 0.0, 1.0); out = {}
    for kind in ("H", "EB"):
        if kind == "H":
            hb = hr = hc = he = hoeff(Nf, delta / 3); hw = hoeff(N, delta / 3)
        else:
            hb, hr, hc, he = eb(bq, delta / 3), eb(rq, delta / 3), eb(np.clip(cq, 0.0, 1.0), delta / 3), eb(eq, delta / 3); hw = eb(win, delta / 3)
        hw = min(hw, 1.0)
        c1 = bbar + rbar * wbar; h1 = hb + hr + rbar * hw
        h3 = max(hb, he) + rbar * hw
        c2 = cbar + rbar * (wbar - W0); h2 = hc + hr * (abs(wbar - W0) + hw) + rbar * hw
        for name, c, hh in (("thy", c1, h1), ("two", c1, h3), ("one", c2, h2)):
            out[name + "_" + kind] = dict(lo=lnz_of(lnZup, D, c - hh) - BETA * EPS_G, hi=lnz_of(lnZup, D, c + hh) + BETA * EPS_G, point=lnz_of(lnZup, D, c),
                                          half_W=hh, prop_part=hh - rbar * hw, eval_part=rbar * hw)
    return out


def plain_brackets(W, lnZup, D, delta):
    W = np.clip(W, 0, 1); c = float(W.mean()); out = {}
    for kind, hh in (("H", hoeff(len(W), delta)), ("EB", eb(W, delta))):
        out[kind] = dict(lo=lnz_of(lnZup, D, c - hh) - BETA * EPS_G, hi=lnz_of(lnZup, D, c + hh) + BETA * EPS_G, point=lnz_of(lnZup, D, c), half_W=hh)
    return out


def draw_q(lo, diff, Nq, rng, batch):
    """Nq draws of q by rejection from pi_{m_-}; returns states, U, number of draws of pi_{m_-} used."""
    out = []; outU = []; got = 0; nlo = 0
    while got < Nq:
        P = lo.sample(batch, rng); U = BETA * diff.energy(P); ok = np.flatnonzero(rng.random(batch) < -np.expm1(-U))
        if got + len(ok) >= Nq:
            ok = ok[:Nq - got]; nlo += int(ok[-1]) + 1
        else:
            nlo += batch
        out.append(P[ok]); outU.append(U[ok]); got += len(ok)
    return np.concatenate(out), np.concatenate(outU), nlo


def main():
    a = sys.argv[1:]
    seq, bb, m, w, form, models = a[0], a[1], int(a[2]), int(a[3]), a[4], a[5]
    N = opt(a, "--N", 1200, int); Nf = opt(a, "--Nf", 0, int); reps = opt(a, "--reps", 200, int); delta = 0.05
    seed = opt(a, "--seed", 2026112700 + 10 * m, int); w3 = opt(a, "--w3", w, int)
    t0 = time.time(); rng = np.random.default_rng(seed)
    I = build(seq, bb, m, w, form, models, w3); lo, up, diff = I["lo"], I["up"], I["diff"]; n, k, x0 = I["n"], I["k"], I["x0"]
    lnZlo, lnZup = lo.lnZ(), up.lnZ(); D = lnZlo - lnZup; acc_q = -math.expm1(-D)
    dom = float(np.prod([float(v) for v in k]))
    log(f"=== nested sampler (theory division, Proposition 11.113a) on {seq}/{bb}, order {m}, band {w}"
        + (f", triples within {w3}" if form == "T" and w3 != w else "") + f", form {form}, models '{models}' "
        f"({I['info'].get('exact', 0)} evaluated terms exact in the window): {n} sites, {dom:.6g} assignments, ball {I['nball']} evaluations; "
        f"Gamma_{m} = {BETA * I['Gam']:.4f} kT; outer sandwich ln Z in [{lnZup:.6f}, {lnZlo:.6f}], D = {D:.6f} nats; "
        f"acceptance of the q-rejection 1 - e^-D = {acc_q:.5f}; seed {seed}; delta {delta} [{time.time() - t0:.0f}s]")
    res = dict(seq=seq, bb=bb, m=m, w=w, w3=w3, form=form, models=models, n=n, domain=dom, nball=I["nball"], Gamma_kT=BETA * I["Gam"],
               lnZ_up=lnZup, lnZ_lo=lnZlo, D=D, seed=seed, delta=delta)
    batch = int(min(200000, max(20000, 4000 / max(acc_q, 1e-6))))
    if "--enum" in a:
        st, g, src = L.enumerate_g(I["G"], seq, bb, I["tau"], verbose=False)
        E = pw.f_energy(st, I["c0"], I["h"], I["J"]) + g
        ml, mu = lo.energy(st), up.energy(st)
        v_out = int((ml > E + 1e-9).sum() + (mu < E - 1e-9).sum())
        el, eh, nclip, nbad, env, base = inner_bounds(I, st, ml, mu)
        Eh = np.clip(E, ml, mu)
        v_in = int((el > Eh + 1e-9).sum() + (eh < Eh - 1e-9).sum())
        tch = (st != x0[None]).sum(1)
        # the envelope closed form against the per-subset constants (where the number of subsets allows)
        dev_env = float("nan")
        if len(st) <= 20000 and math.comb(n, m) <= 800:                      # P3's per-subset evaluation, an independent code path
            chat = L.enum_chat(I["GF"], m); dev_env = float(np.abs(L.envelope_value(st, x0, chat) - env).max())
        pick = np.random.default_rng(5).choice(len(st), min(len(st), 400), replace=False)
        dev_cf = float(np.abs(I["env"].value_closed_form(st[pick]) - env[pick]).max())      # one closed form per changed set against the table
        lz = lambda e: float(logsumexp(-BETA * e))
        lnZE, lnZEh, lnZel, lnZeh = lz(E), lz(Eh), lz(el), lz(eh)
        Zs = lnZup                                                           # all partition functions relative to Z(m_+)
        A = math.expm1(D)                                                    # (Z(m_-) - Z(m_+)) / Z(m_+)
        b, rho = b_rho(ml, mu, el, eh)
        qw = np.exp(-BETA * ml - lnZlo) * (-np.expm1(-BETA * (mu - ml))); q = qw / qw.sum()
        Eqb, Eqr = float(q @ b), float(q @ rho)
        pos = rho > 0
        Win = np.zeros(len(st)); Win[pos] = np.clip(w_in(np.clip(Eh[pos], el[pos], eh[pos]), ml[pos], el[pos], eh[pos]), 0.0, 1.0)   # v_in = 0: clipping removes rounding only
        EqW = float(q @ (b + rho * Win))
        id1 = abs(math.log1p(A * Eqb) + Zs - lnZeh); id2 = abs(A * Eqr - (math.exp(lnZel - Zs) - math.exp(lnZeh - Zs))); id3 = abs(math.log1p(A * EqW) + Zs - lnZEh)
        qin = q * rho; qin = qin / qin.sum(); mWin = float(qin @ Win); sdWin = float(math.sqrt(qin @ (Win - mWin) ** 2))
        mc = float(q @ (b + rho * W0)); sdc = float(math.sqrt(q @ (b + rho * W0 - mc) ** 2)); sdb = float(math.sqrt(q @ (b - Eqb) ** 2)); sdr = float(math.sqrt(q @ (rho - Eqr) ** 2))
        Wtot = b + rho * Win; sdW = float(math.sqrt(q @ (Wtot - EqW) ** 2))
        log(f"(E) enumeration, {len(st)} states ({src if isinstance(src, str) else 'cache'}): outer sandwich violated at {v_out} states, inner at {v_in}; "
            f"clipping active at {nclip} states, inconsistent at {nbad}; envelope: table against P3's per-subset constants, max deviation "
            + (f"{dev_env:.2e}" if dev_env == dev_env else "not computed (more than 20 000 states)") + f", against one closed "
            f"form per changed set (400 states) {dev_cf:.2e} kcal/mol; "
            f"largest envelope {BETA * env.max():.4f} kT, largest |g - I g| {BETA * np.abs(E - base).max():.3e} kT")
        log(f"    exact: ln Z(E) = {lnZE:.9f} (clipped evaluated energy: {lnZEh:.9f}); ln Z(e_+) = {lnZeh:.9f}, ln Z(e_-) = {lnZel:.9f}: "
            f"ENVELOPE BRACKET {lnZel - lnZeh:.6f} nats inside the outer {D:.6f}")
        log(f"    identities: ln[Z(m_+) + A E_q b] - ln Z(e_+) = {id1:.1e};  A E_q rho - (Z(e_-) - Z(e_+)) = {id2:.1e} (in units of Z(m_+));  "
            f"ln[Z(m_+) + A E_q W] - ln Z(E^) = {id3:.1e};  E_q b = {Eqb:.6f}, E_q rho = {Eqr:.6f}, E_q W = {EqW:.6f}; "
            f"W_in in [{Win[pos].min():.4f}, {Win[pos].max():.4f}] on the {int(pos.sum())} states with rho > 0; rho = 0 at all {int((tch < m).sum())} ball states: "
            f"{bool((rho[tch < m] == 0).all())}")
        sde = float(math.sqrt(q @ (b + rho - Eqb - Eqr) ** 2))
        log(f"    exact standard deviations under q: b {sdb:.4f}, b + rho {sde:.4f}, rho {sdr:.4f}, c = b + rho/2 {sdc:.4f}, W {sdW:.4f}; under the inner law: W_in {sdWin:.4f} "
            f"(mean {mWin:.4f})")
        res["enum"] = dict(states=int(len(st)), viol_outer=v_out, viol_inner=v_in, clip=nclip, bad=nbad, dev_env=dev_env, dev_closed_form=dev_cf, lnZ_E=lnZE, lnZ_Eh=lnZEh, lnZ_e_plus=lnZeh,
                           lnZ_e_minus=lnZel, envelope_bracket=lnZel - lnZeh, Eq_b=Eqb, Eq_rho=Eqr, Eq_W=EqW, id1=id1, id2=id2, id3=id3,
                           sd_b=sdb, sd_rho=sdr, sd_c=sdc, sd_W=sdW, sd_Win=sdWin, mean_Win=mWin)
        idx_of = lambda S: np.ravel_multi_index(tuple(S.T), k)
        chk = idx_of(st[:1000]); assert (chk == np.arange(min(1000, len(st)))).all()      # the enumeration is in C order
        Wpl = np.zeros(len(st)); pp = mu > ml
        Wpl[pp] = np.exp(-BETA * (Eh[pp] - ml[pp])) * np.expm1(-BETA * (mu[pp] - Eh[pp])) / np.expm1(-BETA * (mu[pp] - ml[pp]))
        bal = int(round(4 * N / max(Eqr, 1e-3) ** 2))
        for Nf_r in ([Nf] if Nf else [bal, 4 * bal, 16 * bal]):
            ins = {kk: 0 for kk in KEYS}; wid = {kk: [] for kk in KEYS}; err = []; insp = dict(H=0, EB=0); widp = dict(H=[], EB=[]); errp = []
            nev = []; nlos = []; bb_ = []; rr_ = []; t1 = time.time()
            for rep in range(reps):
                S, U, nlo = draw_q(lo, diff, Nf_r, rng, batch); ii = idx_of(S)
                acc = np.flatnonzero(rng.random(Nf_r) < rho[ii]); ev = acc[:N]
                br = nested_brackets(b[ii], rho[ii], Win[ii[ev]], lnZup, D, delta)
                for kk in KEYS:
                    ins[kk] += int(br[kk]["lo"] <= lnZE <= br[kk]["hi"]); wid[kk].append(br[kk]["hi"] - br[kk]["lo"])
                err.append(br["thy_H"]["point"] - lnZE); nev.append(len(ev)); nlos.append(nlo); bb_.append(float(b[ii].mean())); rr_.append(float(rho[ii].mean()))
                # the plain sampler with the same number of evaluations: the first len(ev) proposals, all evaluated
                Np = max(len(ev), 2); pb = plain_brackets(Wpl[ii[:Np]], lnZup, D, delta)
                for kk in ("H", "EB"):
                    insp[kk] += int(pb[kk]["lo"] <= lnZE <= pb[kk]["hi"]); widp[kk].append(pb[kk]["hi"] - pb[kk]["lo"])
                errp.append(pb["H"]["point"] - lnZE)
            err = np.array(err); errp = np.array(errp); rms, rmsp = float(np.sqrt((err ** 2).mean())), float(np.sqrt((errp ** 2).mean()))
            log(f"(R) {reps} repetitions, N_f = {Nf_r} proposals ({Nf_r / bal:.0f} x 4N/rho^2), at most N = {N} evaluations (used on average {np.mean(nev):.0f}; draws of the "
                f"floor per repetition {np.mean(nlos):.0f}) [{time.time() - t1:.0f}s]; mean b {np.mean(bb_):.6f}, mean rho {np.mean(rr_):.6f}")
            log(f"    NESTED, mean width in nats (truth inside, of {reps}): " + "; ".join(f"{kk} {np.mean(wid[kk]):.5f} ({ins[kk]})" for kk in KEYS)
                + f"; point estimate rms error {rms:.2e}")
            log(f"    PLAIN (Proposition 11.113, same number of evaluations): Hoeffding {np.mean(widp['H']):.5f} ({insp['H']}); empirical Bernstein "
                f"{np.mean(widp['EB']):.5f} ({insp['EB']}); rms error {rmsp:.2e}.   plain/nested: Hoeffding {np.mean(widp['H']) / np.mean(wid['thy_H']):.2f} (thy), "
                f"{np.mean(widp['H']) / np.mean(wid['two_H']):.2f} (two), {np.mean(widp['H']) / np.mean(wid['one_H']):.2f} (one); EB "
                f"{np.mean(widp['EB']) / np.mean(wid['thy_EB']):.2f} (thy), {np.mean(widp['EB']) / np.mean(wid['two_EB']):.2f} (two), "
                f"{np.mean(widp['EB']) / np.mean(wid['one_EB']):.2f} (one); rms errors {rmsp / max(rms, 1e-300):.2f}")
            res.setdefault("reps", []).append(dict(Nf=Nf_r, N=N, reps=reps, mean_evals=float(np.mean(nev)), inside=ins, mean_width={kk: float(np.mean(wid[kk])) for kk in KEYS},
                                                   rms_err=rms, plain_inside=insp, plain_mean_width={kk: float(np.mean(widp[kk])) for kk in widp}, plain_rms_err=rmsp,
                                                   mean_floor_draws=float(np.mean(nlos))))
    else:
        if not Nf: Nf = 100000
        t1 = time.time(); S, U, nlo = draw_q(lo, diff, Nf, rng, batch)
        ml = lo.energy(S); mu = ml + U / BETA
        log(f"(1) {Nf} proposals from q ({nlo} draws of the floor, observed acceptance {Nf / nlo:.5f}) [{time.time() - t1:.0f}s]; "
            f"{len(np.unique(S, axis=0))} distinct states; changed sites among proposals: mean {float((S != x0[None]).sum(1).mean()):.2f}")
        t1 = time.time(); el, eh, nclip, nbad, env, base = inner_bounds(I, S, ml, mu)
        b, rho = b_rho(ml, mu, el, eh)
        log(f"(2) inner bounds at the proposals, no evaluation: {I['env'].nsets} distinct changed sets, closed-form sums for the envelope {I['env'].seconds:.0f}s "
            f"[{time.time() - t1:.0f}s]; clipping active at {nclip} proposals, inconsistent at {nbad}; mean b = {b.mean():.6f} (sd {b.std():.4f}), "
            f"mean rho = {rho.mean():.6f} (sd {rho.std():.4f}), sd of c = b + rho/2: {(b + rho * W0).std():.4f}; proposals with rho = 0: {int((rho == 0).sum())}")
        acc = np.flatnonzero(rng.random(Nf) < rho); ev = acc[:N]
        t1 = time.time()
        uniq, inv = np.unique(S[ev], axis=0, return_inverse=True); inv = np.asarray(inv).reshape(-1)
        gU = np.concatenate([I["G"].bulk_energy(uniq[s:s + 4096]) for s in range(0, len(uniq), 4096)]) if len(uniq) else np.zeros(0)
        Eev = (pw.f_energy(uniq, I["c0"], I["h"], I["J"]) + gU)[inv]
        v_in = int((Eev < el[ev] - 1e-9).sum() + (Eev > eh[ev] + 1e-9).sum()); v_out = int((Eev < ml[ev] - 1e-9).sum() + (Eev > mu[ev] + 1e-9).sum())
        Eh = np.clip(Eev, ml[ev], mu[ev])                                   # the target E^; inside [e_-, e_+] if the inner sandwich is valid
        Wraw = w_in(Eh, ml[ev], el[ev], eh[ev]); w_out = int(((Wraw < -1e-6) | (Wraw > 1 + 1e-6)).sum())
        Win = np.clip(Wraw, 0.0, 1.0)
        log(f"(3) {len(acc)} of the {Nf} proposals accepted with probability rho; the first {len(ev)} evaluated ({len(uniq)} distinct states) [{time.time() - t1:.0f}s]: "
            f"evaluated energy outside the inner sandwich at {v_in}, outside the outer at {v_out}; W_in in [{Win.min():.4f}, {Win.max():.4f}], mean {Win.mean():.4f} "
            f"(sd {Win.std(ddof=1):.4f}); largest |E - (f + I g)| among evaluated {BETA * float(np.abs(Eev - base[ev]).max()):.2e} kT against largest envelope "
            f"{BETA * float(env[ev].max()):.2e} kT (mean ratio |remainder| / envelope: {float((np.abs(Eev - base[ev]) / np.maximum(env[ev], 1e-300)).mean()):.4f})")
        if v_in or w_out:
            log(f"    !!! INNER SANDWICH VIOLATED at {v_in} evaluated states (W_in outside [0, 1] at {w_out}): the brackets below are NOT valid")
        br = nested_brackets(b, rho, Win, lnZup, D, delta)
        for kk, name in (("thy_H", "NESTED as stated by the theory division (Hoeffding)"), ("two_H", "NESTED, two-end form of workstream R15 (Hoeffding)"),
                         ("one_H", "NESTED, one known mean (Hoeffding)"), ("thy_EB", "NESTED as stated, empirical Bernstein"),
                         ("two_EB", "NESTED, two-end form, empirical Bernstein"), ("one_EB", "NESTED, one known mean, empirical Bernstein")):
            v = br[kk]
            log(f"    {name}, with probability >= {1 - delta}: ln Z(E) in [{v['lo']:.6f}, {v['hi']:.6f}], width {v['hi'] - v['lo']:.6f} nats; point {v['point']:.6f}; "
                f"half-width in W {v['half_W']:.5f} = {v['prop_part']:.5f} (proposals) + {v['eval_part']:.5f} (evaluations)")
        # what the envelope alone gives, estimated (not certified): Z(e_+) and Z(e_-) from the proposals
        env_est = lnz_of(lnZup, D, b.mean() + rho.mean()) - lnz_of(lnZup, D, b.mean())
        log(f"    estimated from the proposals alone (no evaluation): ln Z(e_+) ~ {lnz_of(lnZup, D, b.mean()):.6f}, ln Z(e_-) ~ {lnz_of(lnZup, D, b.mean() + rho.mean()):.6f}: "
            f"envelope bracket ~ {env_est:.6f} nats against the outer {D:.6f}")
        # the plain sampler with the same number of evaluations (other states: the first N proposals)
        t1 = time.time(); Np = len(ev)
        uq, iv = np.unique(S[:Np], axis=0, return_inverse=True); iv = np.asarray(iv).reshape(-1)
        gq = np.concatenate([I["G"].bulk_energy(uq[s:s + 4096]) for s in range(0, len(uq), 4096)])
        Ep = np.clip((pw.f_energy(uq, I["c0"], I["h"], I["J"]) + gq)[iv], ml[:Np], mu[:Np])
        Wp = np.exp(-BETA * (Ep - ml[:Np])) * np.expm1(-(U[:Np] - BETA * (Ep - ml[:Np]))) / np.expm1(-U[:Np])
        pb = plain_brackets(Wp, lnZup, D, delta); wH = pb["H"]["hi"] - pb["H"]["lo"]; wE = pb["EB"]["hi"] - pb["EB"]["lo"]
        wd = {kk: br[kk]["hi"] - br[kk]["lo"] for kk in KEYS}
        log(f"    PLAIN sampler (Proposition 11.113) with the same {Np} evaluations at the first {Np} proposals ({len(uq)} distinct) [{time.time() - t1:.0f}s]: "
            f"Hoeffding [{pb['H']['lo']:.6f}, {pb['H']['hi']:.6f}], width {wH:.6f}; empirical Bernstein [{pb['EB']['lo']:.6f}, {pb['EB']['hi']:.6f}], width {wE:.6f}; "
            f"point {pb['H']['point']:.6f}; mean W {Wp.mean():.4f} (sd {Wp.std(ddof=1):.4f}).  plain/nested widths: Hoeffding {wH / wd['thy_H']:.2f} (thy), "
            f"{wH / wd['two_H']:.2f} (two), {wH / wd['one_H']:.2f} (one); EB {wE / wd['thy_EB']:.2f} (thy), {wE / wd['two_EB']:.2f} (two), {wE / wd['one_EB']:.2f} (one)")
        res["run"] = dict(Nf=Nf, floor_draws=int(nlo), distinct_proposals=int(len(np.unique(S, axis=0))), distinct_changed_sets=int(I["env"].nsets), clip=nclip, bad=nbad,
                          mean_b=float(b.mean()), mean_rho=float(rho.mean()), sd_b=float(b.std()), sd_rho=float(rho.std()), sd_c=float((b + rho * W0).std()),
                          accepted=int(len(acc)), N=int(len(ev)), distinct_evaluated=int(len(uniq)), viol_inner=v_in, viol_outer=v_out, W_in_outside=w_out,
                          mean_Win=float(Win.mean()), sd_Win=float(Win.std(ddof=1)), brackets=br, plain=pb, mean_W_plain=float(Wp.mean()), sd_W_plain=float(Wp.std(ddof=1)),
                          envelope_bracket_est=env_est, env_seconds=I["env"].seconds)
    res["seconds"] = time.time() - t0; res["peak_rss_mb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    tag = f"{seq.replace(':', 'c')}_{bb}_m{m}_w{w}_{form}_{models}" + ("_enum" if "--enum" in a else "")
    json.dump(res, open(os.path.join(HERE, f"nested_sampler_{tag}.json"), "w"), indent=1)
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {res['peak_rss_mb']:.0f} MB")


if __name__ == "__main__":
    main()
