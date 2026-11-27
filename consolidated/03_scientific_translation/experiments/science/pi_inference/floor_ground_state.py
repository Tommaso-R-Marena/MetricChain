#!/usr/bin/env python3
"""Is the transition of a floor where ONE extremal state takes over?  (A test of a reading sent to the theory division in
SCI-RES-0031 section 1; prediction in the research log of 2026-11-26 before this script was written.)

Floor with every penalty table multiplied by lambda:  m_lambda = m_0 - lambda * pen.  With
    c(x) = ln Z(m_0) + beta m_0(x) >= 0   (minus the log-weight of the state x under m_0),      b(x) = beta pen(x) >= 0,
    G(lambda) = max_x [ lambda b(x) - c(x) ] = - beta min_x m_lambda(x) - ln Z(m_0)  <=  ln Z(m_lambda) - ln Z(m_0),
one state against the whole sum.  G is convex and piecewise linear, and needs one (min,+) pass of the band model per lambda
(workstream P3's BandModel.dp in mode "max"; the minimiser by backtracking, written here).  Reported per case:
  lambda_kink  the largest lambda at which the ground state of the floor is still the ground state of m_0
               (the displaced state's weight reaches the weight of that state);
  lambda_gs    where G = 0: the least ratio c(x) / b(x) over all states (one displaced state weighs as much as all of Z(m_0));
  the minimiser there: sites off the anchor, its penalty b* and its cost c* (and c*/b*, which must equal lambda_gs);
  the measured lambda_c of the committed scan (floor_transition_*.log), and G, ln Z - ln Z(m_0) at lambda_c and lambda_gs.
Checks: G <= ln Z(m_lambda) - ln Z(m_0) at every lambda evaluated (must hold); the ratio c/b of 2000 exact samples of the floor
at lambda_gs and at 2 lambda_gs is nowhere below the ratio c*/b* of the minimiser (must hold if that is the least ratio).
Control: the same ratio test against 1.05 c*/b* -- it must FAIL (the minimiser itself is sampled), and the (min,+) value at
lambda = 0 must equal the least energy among 2000 exact samples of m_0 or lie below it.
Last line (h): the two phases with their entropies -- S_a = -ln(weight of the ground state of m_0), S_d = ln(Z_d / largest
displaced term) -- and where they predict equal weights, against the measured lambda_c.
The construction of the floor is not copied: floor_transition.main() is run in-process on a two-point grid and its local
objects (model, lnz, pen) are taken from its frame; its lines (0)-(2) are printed here so that ln Z(m_0) can be compared with
the committed scan.
Run: python3 -B floor_ground_state.py K12 4 4 > floor_ground_state_K12_m4_w4.log
"""
import os, sys, io, re, time, math, contextlib, resource
import numpy as np
import floor_transition as FT
HERE = os.path.dirname(os.path.abspath(__file__))


def capture(argv):
    got = {}

    def prof(frame, event, arg):
        if event == "return" and frame.f_code is FT.main.__code__: got.update(frame.f_locals)
    old = sys.argv; sys.argv = ["floor_transition.py"] + argv; buf = io.StringIO(); sys.setprofile(prof)
    try:
        with contextlib.redirect_stdout(buf): FT.main()
    finally:
        sys.setprofile(None); sys.argv = old
    return got, buf.getvalue()


def argmin_state(mdl):
    """(minimum energy, a minimiser) of a band model: (min,+) forward pass, backtracking as in BandModel.sample."""
    val, As = mdl.dp(-1.0, "max", keep=True); n, w = mdl.n, mdl.w; st = np.zeros(n, dtype=int)
    for i in range(n - 1, -1, -1):
        hi = min(i + w, n - 1); st[i] = int(np.argmax(As[i][(slice(None),) + tuple(int(st[j]) for j in range(i + 1, hi + 1))]))
    return -val, st


def main():
    seq, m, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); t0 = time.time(); BETA, RND = FT.BETA, FT.RND
    got, text = capture([seq, str(m), str(w), "--grid", "0,0.01", "--N", "4"])
    for line in text.split("\n"):
        if line.startswith("=== ") or line.startswith("(0)") or line.startswith("(1)") or line.startswith("(2)"): print(line[:400], flush=True)
    model, lnz, pen, n, x0, z0 = got["model"], got["lnz"], got["pen"], got["n"], np.array(got["x0"]), got["z0"]
    m0 = model(0.0); L0 = z0
    tagf = f"floor_transition_{seq.replace(':', 'c')}_m{m}_w{w}.log"; lam_c = None
    if os.path.exists(os.path.join(HERE, tagf)):
        mm = re.search(r"\(4\) lambda_c in \[([0-9.]+), ([0-9.]+)\]", open(os.path.join(HERE, tagf)).read()); lam_c = 0.5 * (float(mm.group(1)) + float(mm.group(2)))
        zc = re.search(r"\(2\) ln Z\(m_0\) = ([0-9.]+)", open(os.path.join(HERE, tagf)).read()).group(1)
        print(f"(a) ln Z(m_0) here {L0:.7f}; in the committed scan {zc}; measured lambda_c there {lam_c:.5g} [{time.time() - t0:.0f}s]", flush=True)
    npass = [0]; viol = [0]; checked = [0]

    def gs(lam):
        npass[0] += 1; e, st = argmin_state(model(lam)); return e, st

    def G(e): return -BETA * e - L0
    e0, s0 = gs(0.0); off0 = int((s0 != x0).sum()); ea = float(m0.energy(x0)[0]); pa = float(pen(x0)[0])
    X0s = m0.sample(2000, np.random.default_rng(99)); emin_s = float(m0.energy(X0s).min())
    print(f"(b) ground state of m_0: {off0} sites off the anchor, log-weight G(0) = {G(e0):.4f}; the anchor: log-weight {-BETA * ea - L0:.4f}, penalty {pa:g} (must be 0); "
          f"control: least energy among 2000 exact samples of m_0 minus the (min,+) value = {emin_s - e0:.3e} (must be >= 0)", flush=True)
    assert pa == 0.0 and emin_s - e0 >= -1e-9
    hi = 2.0 * (lam_c if lam_c else 1.0)
    while G(gs(hi)[0]) <= 0: hi *= 2.0
    # lambda_kink: the ground-state energy starts to fall
    lo_k, hi_k = 0.0, hi
    for it in range(16):
        mid = 0.5 * (lo_k + hi_k)
        if e0 - gs(mid)[0] > 1e-9: hi_k = mid
        else: lo_k = mid
    ek, sk = gs(hi_k)
    # lambda_gs: G = 0
    lo_g, hi_g = lo_k, hi
    for it in range(16):
        mid = 0.5 * (lo_g + hi_g)
        if G(gs(mid)[0]) > 0: hi_g = mid
        else: lo_g = mid
    eg, sg = gs(hi_g); lam_gs = hi_g
    bstar = BETA * RND * float(pen(sg)[0]); cstar = L0 + BETA * float(m0.energy(sg)[0])
    bk = BETA * RND * float(pen(sk)[0]); ck = L0 + BETA * float(m0.energy(sk)[0])
    print(f"(c) lambda_kink in [{lo_k:.5g}, {hi_k:.5g}]: the ground state of the floor just above it has {int((sk != x0).sum())} sites off the anchor, penalty b = {bk:.4g} kT, cost c = {ck:.4g} "
          f"(c - c of the m_0 ground state) / b = {(ck + G(e0)) / bk:.5g}", flush=True)
    print(f"(d) lambda_gs in [{lo_g:.5g}, {hi_g:.5g}] (G = 0): minimiser with {int((sg != x0).sum())} of {n} sites off the anchor, penalty b* = {bstar:.5g} kT, cost c* = {cstar:.5g}; "
          f"c*/b* = {cstar / bstar:.5g} (must equal lambda_gs); the same state as just above lambda_kink: {bool((sg == sk).all())}", flush=True)
    rows = []
    for name, lam in (("lambda_kink", hi_k), ("measured lambda_c", lam_c), ("lambda_gs", lam_gs)):
        if lam is None: continue
        e, st = gs(lam); d = lnz(lam) - L0; checked[0] += 1; viol[0] += int(G(e) > d + 1e-9)
        rows.append((name, lam, G(e), d, int((st != x0).sum())))
    print("| at | lambda | G (one state) | ln Z(m_lambda) - ln Z(m_0) (exact) | difference (the entropy the one-state bound misses) | sites off in the ground state |")
    print("|---|---|---|---|---|---|")
    for name, lam, g, d, off in rows: print(f"| {name} | {lam:.5g} | {g:.4f} | {d:.4f} | {d - g:.4f} | {off} |")
    print(f"(e) G <= ln Z(m_lambda) - ln Z(m_0): {viol[0]} violations in {checked[0]} (must be 0)", flush=True)
    # the least-ratio claim on exact samples of the floor
    # (the reference is the ratio c*/b* of the minimiser itself, not the upper end of the bisection for lambda_gs, which lies above it by up to the
    #  resolution of the bisection -- a first version compared with that upper end at a tolerance finer than the resolution and counted the minimiser as a violation)
    rstar = cstar / bstar; bad = 0; badc = 0; tot = 0; least = math.inf
    for lam, seed in ((lam_gs, 7), (2.0 * lam_gs, 8)):
        X = model(lam).sample(2000, np.random.default_rng(seed)); b = BETA * RND * pen(X); c = L0 + BETA * m0.energy(X); ok = b > 0
        r = c[ok] / b[ok]; tot += int(ok.sum()); bad += int((r < rstar * (1 - 1e-9)).sum()); badc += int((r < 1.05 * rstar).sum()); least = min(least, float(r.min()) if ok.any() else math.inf)
    print(f"(f) the ratio c/b of {tot} exact samples of the floor at lambda_gs and at twice that (those with a positive penalty): least {least:.7g} against c*/b* = {rstar:.7g}; below c*/b*: {bad} (must be 0); "
          f"control, below 1.05 c*/b*: {badc} (must be positive: the minimiser has the ratio c*/b*)", flush=True)
    # the two phases with their entropies: S_a = -ln(weight of the ground state of m_0); S_d = ln(Z_d / largest displaced term), Z_d = Z(m_lambda) - Z of the reference
    # phase (continued to first order from lambda = 0); equal weights of the two phases at lambda_eq = lambda_gs - (S_d - growth of the reference phase) / b*
    if lam_c:
        s0 = float(got["s0"]); lines = []
        for name, lam, g, d, off in rows:
            ref = lam * s0; zd = math.exp(d) - math.exp(ref)
            if zd > 0: lines.append((name, lam, math.log(zd) - g, ref))
        Sd = [v for (nm, lam, v, ref) in lines if nm == "measured lambda_c"]
        if Sd:
            lam_eq = lam_gs - (Sd[0] - lam_c * s0) / bstar
            print("(h) two phases: entropy of the reference phase S_a = " + f"{-G(e0):.4f}; entropy of the displaced phase S_d = ln(Z_d / its largest term) at "
                  + ", ".join(f"{nm}: {v:.4f}" for (nm, lam, v, ref) in lines) + f"; equal weights predicted at lambda_gs - (S_d - reference growth) / b* = {lam_eq:.5g} "
                  f"(measured lambda_c, where the mean number of displaced sites is n/2: {lam_c:.5g}); lambda_kink + (S_a - S_d) / b* = {hi_k + (-G(e0) - Sd[0]) / bstar:.5g}", flush=True)
    if lam_c:
        print(f"(g) lambda_gs / measured lambda_c = {lam_gs / lam_c:.4f}; (lambda_gs - lambda_c) b* = {(lam_gs - lam_c) * bstar:.3f} nats (the entropy by which the displaced phase wins earlier); "
              f"lambda_kink / lambda_c = {hi_k / lam_c:.4f}")
    print(f"ALL DONE {time.time() - t0:.0f} s; {npass[0]} (min,+) passes; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
