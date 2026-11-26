#!/usr/bin/env python3
"""Addendum A17 (10), note of 2026-11-26: ARE THE TWO SAMPLERS EXACT?  -- coordinator's script.

Reason.  For Ace-Val20-NMe on PPII two unbiased estimators of the same ln Z(E) (the energy functions agree to 4e-12 k_BT
on 400 states) give
    sandwich sampler (theory division's Proposition 11.113, run by workstream P6; two sandwiches, two seeds):
                                         518.262414 +- 0.000005   and   518.262417 +- 0.000006
    fitted chain model (coordinator; three seeds):   518.262443 +- 0.000024,  518.262457 +- 0.000025,  518.262573 +- 0.000075
-- all inside the certified bracket [518.262315, 518.262513] except the oldest and least precise, but the three of the
second kind are all above the first kind (combined: 2.3 standard errors).  A fluctuation of that size has probability
about 0.02; a sampling error of 0.5 per cent in either code would produce the same.  Neither sampler had been tested to
that precision: the earlier comparisons with enumeration had standard errors of 1e-4.

Test.  On Ace-Val12-NMe on PPII (531 441 assignments, energies enumerated by workstream P6 -- so a sample costs a table
look-up and millions can be drawn):
  A. the coordinator's chain model (beyond_enumeration_chain.Chain, window 2, tables refitted as in the production run):
     ln Z of the transfer matrix against the enumerated sum; site and nearest-neighbour pair frequencies of N samples
     against the exact marginals; the sampled mean of r = E - m against its exact mean; the estimate against exact ln Z(E).
  B. workstream P3's BandModel.sample on workstream P6's banded pair models (order 5, band 8 < n - 1 = 11, so the band is
     a real restriction, which the enumeration checks of P6 with bands 7 of 8 and 9 of 10 sites did not have):
     the same frequency tests for pi_(m_-); the acceptance rate against 1 - e^(-D); the mean of W over accepted points
     against the exact E_q W; the estimate against exact ln Z(E).
Run:  python3 -B sampler_precision_check.py > sampler_precision_check.log      (one core, a few minutes)
"""
import os, sys, math, json, time
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "ws_P6")))
import beyond_enumeration_chain as bec
import beyond_enumeration_fit as bef
import p6lib as L
pw = L.pw; BETA = L.BETA
assert abs(BETA - bec.BETA) < 1e-15


def log(s): print(s, flush=True)


def freq_test(x, p_exact, shape, label):
    """site and nearest-neighbour pair frequencies of the sample x (N, n) against exact marginals of p_exact (flat over the grid)."""
    N, n = x.shape; P = p_exact.reshape(shape); zs1 = []; zs2 = []
    for i in range(n):
        ex = P.sum(axis=tuple(a for a in range(n) if a != i)); f = np.bincount(x[:, i], minlength=shape[i]) / N
        zs1.extend(((f - ex) / np.sqrt(ex * (1 - ex) / N)).tolist())
    for i in range(n - 1):
        ex = P.sum(axis=tuple(a for a in range(n) if a not in (i, i + 1))).ravel()
        f = np.bincount(x[:, i] * shape[i + 1] + x[:, i + 1], minlength=ex.size) / N
        zs2.extend(((f - ex) / np.sqrt(ex * (1 - ex) / N)).tolist())
    zs1 = np.array(zs1); zs2 = np.array(zs2)
    log(f"     {label}: {N} samples; z-scores of the {len(zs1)} site frequencies: max |z| {np.abs(zs1).max():.2f}, rms {math.sqrt(float((zs1 ** 2).mean())):.2f}; "
        f"of the {len(zs2)} neighbour-pair frequencies: max |z| {np.abs(zs2).max():.2f}, rms {math.sqrt(float((zs2 ** 2).mean())):.2f}  (exact sampler: rms about 1)")
    return dict(z1_max=float(np.abs(zs1).max()), z1_rms=math.sqrt(float((zs1 ** 2).mean())), z2_max=float(np.abs(zs2).max()), z2_rms=math.sqrt(float((zs2 ** 2).mean())))


t0 = time.time(); out = {}
seq, bb, tau = "V12", "P2", 0.70
sd = L.setup(seq, bb, tau); G, c0, h, J, x0, E0 = sd
st, g, src = L.enumerate_g(G, seq, bb, tau, verbose=False)
shape = tuple(G.k); n = G.ns
assert np.array_equal(st, np.array(np.unravel_index(np.arange(len(st)), shape)).T), "enumeration is not in C order"
bE = BETA * (pw.f_energy(st, c0, h, J) + g)                                  # beta E at every state, C order
lnZE = float(logsumexp(-bE))
log(f"=== Ace-Val12-NMe on PPII: {len(st)} states ({src}); exact ln Z(E) = {lnZE:.9f}")

log("--- A. the coordinator's chain model (window 2), tables refitted on samples as in the production run")
rng = np.random.default_rng(20261126)
ch, g_of, dom = bec.build("V" * n, bb, 2, log)
assert all(list(map(int, a)) == list(map(int, b)) for a, b in zip(G.dom, dom)), "domains differ"
chk = rng.choice(len(st), 200, replace=False)
log(f"     the coordinator's energy function against the enumerated table at 200 states: largest difference {np.abs(g_of(st[chk]) - bE[chk]).max():.1e} k_BT")
g_tab = lambda x: bE[np.ravel_multi_index(tuple(x.T), shape)]
sds = [bef.refit(ch, g_tab, 30000, rng)[0] for _ in range(3)]
lnZm = ch.solve()
m_all = ch.energy(st); lnZm_enum = float(logsumexp(-m_all)); pm = np.exp(-m_all - lnZm_enum)
r_all = bE - m_all; Er = float(pm @ r_all); Vr = float(pm @ (r_all - Er) ** 2); K = float(np.log(pm @ np.exp(-(r_all - Er))))
log(f"     sd of r before each refit {', '.join(f'{s:.4f}' for s in sds)}; ln Z(m): transfer matrix {lnZm:.12f}, enumeration {lnZm_enum:.12f} (difference {lnZm - lnZm_enum:+.1e}); "
    f"exact E_m r = {Er:+.9f}, sd {math.sqrt(Vr):.5f}, K = {K:.3e}; identity ln Z(m) - E_m r + K - ln Z(E) = {lnZm_enum - Er + K - lnZE:+.1e}")
NA = 4_000_000; s1 = 0.0; s2 = 0.0; xs = []
for b in range(20):
    x = ch.sample(NA // 20, rng); r = g_tab(x) - ch.energy(x); s1 += float(r.sum()); s2 += float((r * r).sum())
    if b < 5: xs.append(x)
mean = s1 / NA; se = math.sqrt((s2 / NA - mean * mean) / NA)
fa = freq_test(np.concatenate(xs), pm, shape, "chain sampler")
log(f"     sampled mean of r over {NA} samples: {mean:+.9f} +- {se:.9f}; exact {Er:+.9f}; z = {(mean - Er) / se:+.2f};   "
    f"estimate ln Z(m) - mean + K = {lnZm - mean + K:.9f} against exact {lnZE:.9f}: difference {lnZm - mean + K - lnZE:+.2e} +- {se:.1e}")
out["A"] = dict(lnZm=lnZm, lnZm_enum=lnZm_enum, Er=Er, sd=math.sqrt(Vr), K=K, N=NA, mean=mean, se=se, z=(mean - Er) / se, **fa)

log("--- B. workstream P3's band sampler on workstream P6's banded pair models (order 5, band 8), and the rejection step")
lo, up, info = L.make_models(seq, bb, tau, 5, 8, "B", setup_data=sd)
ml, mu = BETA * lo.energy(st), BETA * up.energy(st)
assert (ml <= bE + 1e-9).all() and (bE <= mu + 1e-9).all(), "sandwich violated"
lzl, lzu = lo.lnZ(), up.lnZ(); D = lzl - lzu
p_lo = np.exp(-ml - logsumexp(-ml))
dq = np.exp(-ml) - np.exp(-mu); q = dq / dq.sum()
U = mu - ml; W_all = np.where(U > 0, np.expm1(-(bE - ml - U)) / np.where(U > 0, np.expm1(U), 1.0), 0.0)
EqW = float(q @ W_all); VqW = float(q @ (W_all - EqW) ** 2)
log(f"     ln Z(m_-): transfer matrix {lzl:.12f}, enumeration {float(logsumexp(-ml)):.12f}; ln Z(m_+): {lzu:.12f}, {float(logsumexp(-mu)):.12f}; D = {D:.6f}; "
    f"exact E_q W = {EqW:.9f} (sd {math.sqrt(VqW):.4f}); identity ln[Z+ + (Z- - Z+) E_q W] - ln Z(E) = {lzu + math.log1p(math.expm1(D) * EqW) - lnZE:+.1e}")
rng = np.random.default_rng(20261127)
NB = 6_000_000; nacc = 0; sW = 0.0; sW2 = 0.0; xs = []; xacc = []
for b in range(30):
    S = lo.sample(NB // 30, rng)
    idx = np.ravel_multi_index(tuple(S.T), shape)
    acc = rng.random(len(S)) < -np.expm1(-U[idx])
    w = W_all[idx[acc]]; nacc += int(acc.sum()); sW += float(w.sum()); sW2 += float((w * w).sum())
    if b < 5: xs.append(S)
    xacc.append(S[acc])
fb = freq_test(np.concatenate(xs), p_lo, shape, "band sampler, pi_(m_-)")
fq = freq_test(np.concatenate(xacc), q, shape, "accepted points, q")
rate = nacc / NB; rate_ex = -math.expm1(-D); se_rate = math.sqrt(rate_ex * (1 - rate_ex) / NB)
mW = sW / nacc; seW = math.sqrt((sW2 / nacc - mW * mW) / nacc)
est = lzu + math.log1p(math.expm1(D) * mW); se_est = math.expm1(D) * seW / (1 + math.expm1(D) * mW)
log(f"     {NB} proposals, {nacc} accepted: rate {rate:.6f} against 1 - e^(-D) = {rate_ex:.6f} (z = {(rate - rate_ex) / se_rate:+.2f}); "
    f"mean W = {mW:.6f} +- {seW:.6f} against exact {EqW:.6f} (z = {(mW - EqW) / seW:+.2f});   estimate {est:.9f} against exact {lnZE:.9f}: difference {est - lnZE:+.2e} +- {se_est:.1e}")
out["B"] = dict(D=D, EqW=EqW, N=NB, accepted=nacc, rate=rate, rate_exact=rate_ex, mean_W=mW, se_W=seW, z_W=(mW - EqW) / seW, est=est, se_est=se_est, lnZE=lnZE,
                band=fb, accepted_freq=fq)
json.dump(out, open(os.path.join(HERE, "sampler_precision_check.json"), "w"), indent=1)
log(f"ALL DONE {time.time() - t0:.0f} s")
