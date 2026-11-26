#!/usr/bin/env python3
"""Assumption audit, Proposition AA.3 (the box limit): what the ball and the envelope allow, and how close the
certificate with a band and the recovery comes to it -- at every state of an enumerated instance.

Setting.  E = f + g; the certificate knows f, the values of g on the Hamming ball of radius m - 1 around the anchor
(hence I = I_{m-1} g everywhere) and an envelope env(x) = sum over the m-subsets T of the changed sites of
Theta_T(x_T) with |g - I|(x) <= env(x).  The class of energies compatible with that information is the BOX
        B = { E' : |E' - (f + I)|(x) <= env(x) for all x },
and both of its extreme members f + I - env and f + I + env are in it.  Hence (Proposition AA.3):
  (i)  no rule that uses only this information can certify ln Z in an interval narrower than
            W* = ln Z(f + I - env) - ln Z(f + I + env)                         ("the box limit"),
       because the interval must contain ln Z of both extreme members;
  (ii) the sandwich built from the exact models f + I -/+ env attains W*.
A band model cannot hold f + I -/+ env; the certificate reduces terms, pairs and penalties to windows, which widens the
sandwich to D >= W*, and Proposition A17.19 takes the known slack back out.  This script computes, by enumeration:
W* and the exact ln Z; the first-order size 2 beta <env> of W* under the Gibbs measure of f + I; and compares with the
sandwich D and the corrected bracket of the committed logs of first_order_recovery.py for the same instance.
Checks: |g - I| <= env at every state (workstream P9's Theorem R; control: every table divided by 1000 -- must be
violated; halving the tables is also printed and need not be violated: the envelope is loose by more than a factor ten);
the exact ln Z inside [ln Z(f + I + env), ln Z(f + I - env)].
Mine: this file.  Workstream P8's: the enumeration of g (ws_P8/out/m1_*.npz, not tracked).  Workstream P9's: the tables
(p9_verification/cache/theta2_*.npz through dump_theta2.py, not tracked).
Run: python3 -B aa02_box_limit.py K5 4 > aa02_box_limit_K5_m4.log
"""
import os, sys, re, math, time, glob, itertools, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "pi_inference"))
import nested_sampler as NS
L, pw = NS.L, NS.pw
BETA = L.BETA


def lz(e):
    e = np.asarray(e, dtype=float); m_ = e.min()
    return float(-BETA * m_ + math.log(np.exp(-BETA * (e - m_)).sum()))


def main():
    seq, m = sys.argv[1], int(sys.argv[2]); bb = "H"; M = m - 1; t0 = time.time()
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]; X0 = np.array(x0)
    Z = np.load(os.path.join(SCI, "ws_P8", "out", f"m1_{tag}.npz")); assert [int(v) for v in Z["anchor"]] == x0 and tuple(Z["shape"]) == tuple(k)
    X = np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, n)
    g = np.array(Z["g"], dtype=float).reshape(-1); assert len(g) == len(X)
    f = pw.f_energy(X, c0, h, J); E = f + g
    radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)

    def lookup(st):
        return g[np.atleast_2d(st).astype(np.int64) @ radix]
    d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None)
    I = np.full(len(X), float(d[()]))
    for U, arr in d.items():
        if len(U) >= 1: I += arr[tuple(X[:, u] for u in U)]
    off = (X != X0[None]); noff = off.sum(1)
    print(f"=== {seq} on {bb}, tau {tau}: {n} sites, states per site {k}, {len(X)} states, anchor {x0}; order m = {m}: the ball of radius {M} has {nb} states; "
          f"largest |g - I_{M} g| inside the ball {float(np.abs(g - I)[noff <= M].max()):.2e} kcal/mol", flush=True)
    # ---- the envelope from workstream P9's resolved tables
    subs = list(itertools.combinations(range(n), m)); non = [[b for b in range(k[i]) if b != x0[i]] for i in range(n)]
    files = sorted(glob.glob(os.path.join(SCI, "ws_P9", "cache", f"theta2_{tag}_m{m}*.npz"))) or sorted(glob.glob(os.path.join(SCI, "p9_verification", "cache", f"theta2_{tag}_m{m}*.npz")))
    tabs = [None] * len(subs)
    for fn in files:
        z = np.load(fn)
        for j in z["idx"]: tabs[int(j)] = np.array(z[f"t{int(j)}"], dtype=float)
    assert all(t is not None for t in tabs)
    env = np.zeros(len(X))
    for T, tab in zip(subs, tabs):
        full = np.zeros([k[i] for i in T]); full[np.ix_(*[non[i] for i in T])] = tab
        env += full[tuple(X[:, u] for u in T)]                                   # zero unless all sites of T are off the anchor
    r = g - I
    viol = int((np.abs(r) > env * (1 + 1e-9) + 1e-10).sum()); ctrl2 = int((np.abs(r) > 0.5 * env * (1 + 1e-9) + 1e-10).sum()); ctrl = int((np.abs(r) > 1e-3 * env * (1 + 1e-9) + 1e-10).sum())
    nz = np.abs(r) > 1e-9
    print(f"(1) |g - I| <= env at every state: {viol} violations; the remainder is non-zero at {int(nz.sum())} states, where env / |g - I| is at least {float((env[nz] / np.abs(r[nz])).min()):.2f} "
          f"(median {float(np.median(env[nz] / np.abs(r[nz]))):.0f}); control that must fail (every table divided by 1000): {ctrl} violations (with every table only halved: {ctrl2} -- the envelope is that loose)", flush=True)
    assert viol == 0 and ctrl > 0
    # ---- the box limit
    zE = lz(E); zlo = lz(f + I + env); zup = lz(f + I - env); Wstar = zup - zlo
    w0 = np.exp(-BETA * ((f + I) - (f + I).min())); w0 /= w0.sum(); first = 2 * BETA * float((w0 * env).sum())
    wE = np.exp(-BETA * (E - E.min())); wE /= wE.sum()
    print(f"(2) exact ln Z = {zE:.7f}; the box [ln Z(f + I + env), ln Z(f + I - env)] = [{zlo:.7f}, {zup:.7f}] contains it: {zlo <= zE <= zup}; "
          f"**the box limit W* = {Wstar:.4g} nats**; first-order size 2 beta <env> under f + I: {first:.4g} (ratio W* / first order {Wstar / first:.3f}); "
          f"mean number of sites off the anchor under E: {float((wE * noff).sum()):.3f}; Gibbs weight of the states with at least {m} sites off: {float(wE[noff >= m].sum()):.3g}", flush=True)
    assert zlo <= zE <= zup
    print(f"    where the exact value sits in the box: ln Z - lower end = {zE - zlo:.3g}, upper end - ln Z = {zup - zE:.3g} (the true remainder uses {100 * abs((zE - 0.5 * (zlo + zup)) / (0.5 * Wstar)):.1f} % of the half-width, on one side)")
    # ---- against the committed logs of the certificate with a band and the recovery
    print("(3) the certificate with a band, from the committed logs of pi_inference/first_order_recovery.py:")
    print("| band | sandwich D | D / W* | corrected bracket | its width | width / W* | corrected bracket contains the box [ln Z(f+I+env), ln Z(f+I-env)] |")
    print("|---|---|---|---|---|---|---|")
    for fn in sorted(glob.glob(os.path.join(SCI, "pi_inference", f"first_order_recovery_{tag.split('_')[0]}_m{m}_w*_enum.log"))):
        t = open(fn).read(); band = int(re.search(r"_w(\d+)_enum", fn).group(1))
        rows = [l for l in t.split("\n") if l.startswith("| ") and "[" in l and "**" in l]
        br = [tuple(float(v) for v in re.search(r"\[([0-9.]+), ([0-9.]+)\]", l).groups()) for l in rows]
        D = br[0][1] - br[0][0]; lo_, up_ = br[-1]
        print(f"| {band} | {D:.4g} | {D / Wstar:.1f} | [{lo_:.7f}, {up_:.7f}] | {up_ - lo_:.4g} | {(up_ - lo_) / Wstar:.2f} | {lo_ <= zlo and zup <= up_} |")
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
