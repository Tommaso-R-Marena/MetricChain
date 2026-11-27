#!/usr/bin/env python3
"""R24, item 1 (ii) on a floor that cannot be enumerated: lambda_gs and lambda_kink by DINKELBACH's ratio iteration
(not the script's bisection) with the referee's own (min,+) elimination over the tables of the model (r24_common.eliminate:
no windows, no BandModel), from three starting points; the closing pass G(c*/b*) = 0; the model's own pass at the same
lambdas.  Then, with the referee's own (+,x) elimination: F(lambda) = ln Z(m_lambda) - ln Z(m_0) exactly, the EXACT
occupancy (derivative of ln Z in a field on the number of sites off the anchor) and so the exact lambda_c of the scan's
definition; lambda_t (F = t); the Renyi upper bound and the bracket it certifies; the two-entropy estimate as a function of
the lambda at which its input is read.
Objects of the coordinator that are used, not rebuilt: lo0 (the floor without penalty), g1, g2, g3, RND, BETA, from the
frame of floor_transition.main().
Run: python3 -B r24_item1_band.py K12 4 4 > r24_item1_band_K12_m4_w4.log        (their run of this case: 130 s, 1031 MB)
"""
import os, sys, time, math, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PI = os.path.normpath(os.path.join(HERE, "..", "pi_inference"))
sys.path.insert(0, PI); sys.path.insert(0, HERE)
import r24_common as C


def main():
    seq, m, w = sys.argv[1], sys.argv[2], sys.argv[3]; t0 = time.time()
    import floor_transition as FT
    got, text = C.capture(FT, [seq, m, w, "--grid", "0,0.01", "--N", "4"], "floor_transition.py")
    for line in text.split("\n"):
        if line.startswith("=== ") or line.startswith("(1)") or line.startswith("(2)"): print("[theirs] " + line[:330], flush=True)
    BETA, RND = FT.BETA, FT.RND
    lo0, g1, g2, g3, k, x0, n = got["lo0"], got["g1"], got["g2"], got["g3"], list(got["k"]), np.array([int(v) for v in got["x0"]]), got["n"]
    model, pen, z0 = got["model"], got["pen"], got["z0"]
    c0, fac0 = C.factors_of(lo0)
    facp = [((i,), np.asarray(g1[i], float)) for i in range(n)] + [(tuple(K), np.asarray(v, float)) for K, v in g2.items()] + [(tuple(K), np.asarray(v, float)) for K, v in g3.items()]
    tmin = min(float(t.min()) for _, t in facp)
    L0 = C.eliminate(fac0, k, "sum", -BETA) - BETA * c0
    print(f"(0) ln Z(m_0): my elimination {L0:.9f}; their transfer matrix {z0:.9f} (difference {L0 - z0:.1e}); least entry of any penalty table {tmin:.3g} (>= 0: {tmin >= 0}); "
          f"{len(fac0)} tables of the floor without penalty, {len(facp)} penalty tables, largest scope {max(len(U) for U, _ in fac0 + facp)} sites [{time.time() - t0:.0f}s, peak RSS {C.rss():.0f} MB]", flush=True)

    def e0_of(X): X = np.atleast_2d(X); return c0 + sum(C.table_value(U, t, X) for U, t in fac0)

    def p_of(X): X = np.atleast_2d(X); return sum(C.table_value(U, t, X) for U, t in facp)
    rng = np.random.default_rng(24); XR = np.stack([rng.integers(0, kk, size=4000) for kk in k], axis=1)
    print(f"(1) my evaluation of their tables against their evaluators at 4000 uniformly random states: floor without penalty {float(np.abs(e0_of(XR) - lo0.energy(XR)).max()):.1e}, "
          f"penalty {float(np.abs(p_of(XR) - pen(XR)).max()):.1e} kcal/mol; penalty at the anchor {float(p_of(x0)[0]):.3g}; random states with a negative penalty: {int((p_of(XR) < 0).sum())}")

    def cb(x):
        return float(L0 + BETA * e0_of(x)[0]), float(BETA * RND * p_of(x)[0])
    npass = [0]

    def own_argmax(lam, shift=0.0):
        """max_x [lam b(x) - c(x)] + shift, and a maximiser (my elimination of -beta m_lambda)"""
        npass[0] += 1
        val, x = C.eliminate(fac0 + [(U, -lam * RND * t) for U, t in facp], k, "max", -BETA, want_arg=True)
        return val - BETA * c0 - L0 + shift, x
    g00, xg = own_argmax(0.0); c_a = -g00
    print(f"(2) ground state of m_0 by my (min,+): {int((xg != x0).sum())} sites off the anchor, c = -ln pi_0 = {c_a:.6f} (their S_a)")

    def dinkelbach(start, shift):
        """least (c(x) - shift) / b(x) over states with b > 0"""
        lam = start; hist = []
        while True:
            g, x = own_argmax(lam, shift)
            if g <= 1e-10: return lam, hist, g
            cc, bb = cb(x); lam = (cc - shift) / bb; hist.append((lam, int((x != x0).sum()), bb, cc, x.copy()))
    res = {}
    for start in (64.0, 1000.0, 20.0):
        p0 = npass[0]; lam, hist, g = dinkelbach(start, 0.0); res[start] = (lam, hist)
        print(f"(3) DINKELBACH for lambda_gs from lambda = {start:g}: iterates {', '.join(f'{h[0]:.8g}' for h in hist)}; {npass[0] - p0} passes; closing pass max_x [lambda b - c] = {g:.2e}; "
              f"minimiser: {hist[-1][1]} of {n} sites off, b* = {hist[-1][2]:.6g}, c* = {hist[-1][3]:.6g}, state {hist[-1][4].tolist()}", flush=True)
    lam_gs, hist = res[64.0]; xs = hist[-1][4]; bstar, cstar = hist[-1][2], hist[-1][3]
    same = all(abs(res[s][0] - lam_gs) < 1e-9 * lam_gs for s in res)
    p0 = npass[0]; lam_kink, hk, gk = dinkelbach(64.0, c_a)
    print(f"(4) **lambda_gs = {lam_gs:.9g}** (three starts agree to 1e-9: {same}); **lambda_kink = {lam_kink:.9g}** (Dinkelbach on (c - c_a)/b, {npass[0] - p0} passes, closing value {gk:.2e}); "
          f"same minimiser: {bool((hk[-1][4] == xs).all())}; lambda_gs - lambda_kink = {lam_gs - lam_kink:.6f} against c_a / b* = {c_a / bstar:.6f}")
    # the committed log of the coordinator
    fn = os.path.join(PI, f"floor_ground_state_{seq.replace(':', 'c')}_m{m}_w{w}.log")
    if os.path.exists(fn):
        txt = open(fn).read(); mm = re.search(r"least ([0-9.]+) against c\*/b\* = ([0-9.]+)", txt); mk = re.search(r"\(c\) lambda_kink in \[([0-9.]+), ([0-9.]+)\]", txt)
        print(f"(5) their committed log: c*/b* = {mm.group(2)}, lambda_kink in [{mk.group(1)}, {mk.group(2)}]; mine - theirs: lambda_gs {lam_gs - float(mm.group(2)):.2e}, lambda_kink within their bracket (4 digits): "
              f"{float(mk.group(1)) - 6e-4 <= lam_kink <= float(mk.group(2)) + 6e-4}")
    # the model's own (min,+) pass, value only
    dv = 0.0
    for lamv in (0.0, 1.0, lam_kink, lam_gs, 2 * lam_gs):
        dv = max(dv, abs((-BETA * model(lamv).minimum() - z0) - own_argmax(lamv)[0]))
    print(f"(6) the model's own (min,+) pass (BandModel.dp) against my elimination at 5 lambdas: largest difference of G {dv:.1e}")
    # control: a state that is NOT the minimiser must have a larger ratio; and a penalty table scaled by 1.01 must move lambda_gs
    worse = 0; tried = 0
    for i in range(n):
        for s in range(k[i]):
            if s != xs[i]:
                y = xs.copy(); y[i] = s; cc, bb = cb(y); tried += 1
                worse += int(bb <= 0 or cc / bb > lam_gs * (1 + 1e-12))
    print(f"(7) every single-site change of the minimiser has a larger ratio: {worse} of {tried} (must be all); control of the iteration: with ln Z(m_0) replaced by ln Z(m_0) + 0.01 the same state gives "
          f"{(cstar + 0.01) / bstar:.6f} (visible: {abs(0.01 / bstar) > 1e-6})")
    # ---------------------------------------------------------------- exact F, exact occupancy
    offp = [((i,), np.where(np.arange(k[i]) == x0[i], 0.0, 1.0)) for i in range(n)]

    def lnZ(lam, field=0.0):
        f = fac0 + [(U, -lam * RND * t) for U, t in facp]
        if field: f = f + [(U, -field / BETA * t) for U, t in offp]            # times the scale -BETA: weight e^{+field * (number of sites off)}
        return C.eliminate(f, k, "sum", -BETA) - BETA * c0

    def F(lam): return lnZ(lam) - L0

    def occ(lam, h=1e-4): return (lnZ(lam, h) - lnZ(lam, -h)) / (2 * h)       # d ln Z / d field = mean number of sites off the anchor
    dz = 0.0
    for lamv in (1.0, lam_kink, lam_gs):
        dz = max(dz, abs(F(lamv) - (got["lnz"](lamv) - z0)))
    s0 = (F(1e-3)) / 1e-3
    print(f"(8) F(lambda) = ln Z(m_lambda) - ln Z(m_0) by my (+,x) elimination against their transfer matrix at lambda = 1, lambda_kink, lambda_gs: largest difference {dz:.1e}; "
          f"F(1) = {F(1.0):.9g}; F(lambda_kink) = {F(lam_kink):.4f}; F(lambda_gs) = {F(lam_gs):.4f} (G = 0 there); slope at 0: {s0:.6g}; occupancy (mean sites off) at 0: {occ(0.0):.4f}, at lambda_gs: {occ(lam_gs):.3f} [{time.time() - t0:.0f}s]", flush=True)

    def cross(f, lo_, hi_, target, it=44):
        for _ in range(it):
            mid = 0.5 * (lo_ + hi_)
            if f(mid) < target: lo_ = mid
            else: hi_ = mid
        return 0.5 * (lo_ + hi_)
    lam_c = cross(occ, 0.5 * lam_gs, 1.5 * lam_gs, n / 2)
    lam_ln2 = cross(F, 0.5 * lam_gs, 1.5 * lam_gs, math.log(2.0)); fix = cross(lambda v: F(v) - v * s0, 0.5 * lam_gs, 1.5 * lam_gs, math.log(2.0))
    print(f"(9) EXACT lambda_c of the scan's definition (mean number of sites off the anchor = n/2; exact occupancy, no sampling): **{lam_c:.6f}** (the committed scan, 1000 samples per lambda: see its line (4)); "
          f"F = ln 2 at **{lam_ln2:.6f}**; F = ln 2 + lambda s0 at {fix:.6f}.  lambda_gs / lambda_c = {lam_gs / lam_c:.5f}; lambda_kink / lambda_c = {lam_kink / lam_c:.5f}; "
          f"(lambda_gs - lambda_c) b* = {(lam_gs - lam_c) * bstar:.4f} nats; F(lambda_c) = {F(lam_c):.4f}")

    def G(lam): return own_argmax(lam)[0]

    def lam_eq_of(lin):
        Fv = F(lin); zd = math.exp(Fv) - math.exp(lin * s0)
        return lam_gs - (math.log(zd) - G(lin) - lin * s0) / bstar
    print("(10) their two-entropy estimate lam_eq = lambda_gs - (S_d(lam_in) - lam_in s0) / b* as a function of the lambda at which S_d is read off the exact ln Z: "
          + "; ".join(f"lam_in = {nm} = {lin:.5g} -> {lam_eq_of(lin):.6g} ({100 * (lam_eq_of(lin) / lam_c - 1):+.3f} % from the exact lambda_c)" for nm, lin in
                      (("lambda_kink", lam_kink), ("0.99 lambda_c", 0.99 * lam_c), ("lambda_c", lam_c), ("1.01 lambda_c", 1.01 * lam_c), ("lambda_gs", lam_gs)))
          + f"; lambda_kink itself is {100 * (lam_kink / lam_c - 1):+.3f} %, the root of F = ln 2 is {100 * (lam_ln2 / lam_c - 1):+.3f} %, lambda_gs {100 * (lam_gs / lam_c - 1):+.3f} % from it")
    # ---------------------------------------------------------------- the Renyi bound and the bracket it certifies
    def renyi(theta): return C.eliminate(fac0, k, "sum", -theta * BETA) - theta * BETA * c0 - theta * L0     # ln sum_x pi_0(x)^theta
    bad = 0; cnt = 0; badc = 0; rows = []
    for q in (0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0):
        Fv = F(q * lam_gs); ub = renyi(1.0 - q); cnt += 1; bad += int(Fv > ub + 1e-9); badc += int(Fv > 1e-9); rows.append((q, Fv, ub))
    print(f"(11) F(lambda) <= ln sum_x pi_0(x)^(1 - lambda/lambda_gs) at {cnt} values: {bad} violations (must be 0); control, without the Renyi term (F <= 0): {badc} violations (must be positive)")
    print("      lambda/lambda_gs | exact F | Renyi upper bound")
    for q, Fv, ub in rows: print(f"        {q:.2f} | {Fv:.6g} | {ub:.6g}")
    print(f"      ln(number of states) = {sum(math.log(v) for v in k):.3f} = the bound at lambda = lambda_gs; Shannon-like slope: the bound at 0.05 lambda_gs is {rows[0][2]:.4f}")
    for t in (0.1, math.log(2.0), 1.0):
        lo_, hi_ = 0.0, 1.0
        for _ in range(50):
            mid = 0.5 * (lo_ + hi_)
            if renyi(mid) > t: lo_ = mid
            else: hi_ = mid
        lt = cross(F, 0.0, 1.5 * lam_gs, t)
        print(f"(12) F reaches t = {t:.3f} at lambda_t = {lt:.6f} (exact, my elimination); certified from lambda_gs and the model without penalty alone: [lambda_gs (1 - theta_t), lambda_gs + t/b*] = "
              f"[{lam_gs * (1 - hi_):.5f}, {lam_gs + t / bstar:.5f}] (theta_t = {hi_:.5f}); inside: {lam_gs * (1 - hi_) <= lt <= lam_gs + t / bstar}; lower end / lambda_t = {lam_gs * (1 - hi_) / lt:.3f}")
    print(f"ALL DONE {time.time() - t0:.0f} s; {npass[0]} (min,+) passes of mine; peak RSS {C.rss():.0f} MB")


if __name__ == "__main__":
    main()
