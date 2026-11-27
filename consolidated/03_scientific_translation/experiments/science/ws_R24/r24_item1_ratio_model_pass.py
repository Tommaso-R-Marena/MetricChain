#!/usr/bin/env python3
"""R24, item 1 (ii), the cases whose band is too wide for the referee's own elimination within the memory limit: lambda_gs and
lambda_kink by DINKELBACH's ratio iteration (not the script's bisection) with the MODEL'S OWN (min,+) pass (BandModel.dp and
the back-tracking of floor_ground_state.argmin_state), the ratio c/b of every state returned being evaluated by the referee
from the tables (r24_common), and the closing test max_x [lambda b - c] = 0 at lambda = c*/b* -- the pass that the
coordinator's script does not make.  Weaker than r24_item1_band.py (the pass is theirs); stated so in the report.
Run: python3 -B r24_item1_ratio_model_pass.py LKSE:12 3 7 > r24_item1_ratio_model_pass_LKSEc12_m3_w7.log
"""
import os, sys, time, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PI = os.path.normpath(os.path.join(HERE, "..", "pi_inference"))
sys.path.insert(0, PI); sys.path.insert(0, HERE)
import r24_common as C


def main():
    seq, m, w = sys.argv[1], sys.argv[2], sys.argv[3]; t0 = time.time()
    import floor_transition as FT
    import floor_ground_state as FG
    got, text = C.capture(FT, [seq, m, w, "--grid", "0,0.01", "--N", "4"], "floor_transition.py")
    for line in text.split("\n"):
        if line.startswith("=== ") or line.startswith("(2)"): print("[theirs] " + line[:300], flush=True)
    BETA, RND = FT.BETA, FT.RND
    lo0, g1, g2, g3, k, x0, n = got["lo0"], got["g1"], got["g2"], got["g3"], list(got["k"]), np.array([int(v) for v in got["x0"]]), got["n"]
    model, pen, z0 = got["model"], got["pen"], got["z0"]
    c0, fac0 = C.factors_of(lo0)
    facp = [((i,), np.asarray(g1[i], float)) for i in range(n)] + [(tuple(K), np.asarray(v, float)) for K, v in g2.items()] + [(tuple(K), np.asarray(v, float)) for K, v in g3.items()]
    tmin = min(float(t.min()) for _, t in facp)

    def cb(x):
        X = np.atleast_2d(x); e = c0 + sum(C.table_value(U, t, X) for U, t in fac0); p = sum(C.table_value(U, t, X) for U, t in facp)
        return float(z0 + BETA * e[0]), float(BETA * RND * p[0])
    rng = np.random.default_rng(7); XR = np.stack([rng.integers(0, kk, size=2000) for kk in k], axis=1)
    e_mine = c0 + sum(C.table_value(U, t, XR) for U, t in fac0); p_mine = sum(C.table_value(U, t, XR) for U, t in facp)
    print(f"(0) ln Z(m_0) (theirs) = {z0:.7f}; my evaluation of their tables against their evaluators at 2000 random states: {float(np.abs(e_mine - lo0.energy(XR)).max()):.1e}, {float(np.abs(p_mine - pen(XR)).max()):.1e} kcal/mol; "
          f"least entry of any penalty table {tmin:.3g}; penalty at the anchor {cb(x0)[1]:.3g} [{time.time() - t0:.0f}s, peak RSS {C.rss():.0f} MB]", flush=True)
    npass = [0]

    def gmax(lam, shift=0.0):
        npass[0] += 1; e, x = FG.argmin_state(model(lam)); return -BETA * e - z0 + shift, x
    g00, xg = gmax(0.0); c_a = -g00

    def dinkelbach(start, shift):
        lam = start; hist = []
        while True:
            g, x = gmax(lam, shift)
            if g <= 1e-9: return lam, hist, g
            cc, bb = cb(x); lam = (cc - shift) / bb; hist.append((lam, int((x != x0).sum()), bb, cc, x.copy()))
            print(f"    iterate {lam:.9g} ({hist[-1][1]} sites off, b = {bb:.6g}, c = {cc:.6g}) [{time.time() - t0:.0f}s]", flush=True)
    fn = os.path.join(PI, f"floor_ground_state_{seq.replace(':', 'c')}_m{m}_w{w}.log"); txt = open(fn).read()
    their = float(re.search(r"least ([0-9.]+) against c\*/b\* = ([0-9.]+)", txt).group(2)); mk = re.search(r"\(c\) lambda_kink in \[([0-9.]+), ([0-9.]+)\]", txt)
    lam_gs, hist, g = dinkelbach(4.0 * their, 0.0)
    print(f"(1) DINKELBACH for lambda_gs from 4 x (their value): {len(hist)} iterates; **lambda_gs = {lam_gs:.9g}**; closing pass max_x [lambda b - c] = {g:.2e} (must be 0 to rounding); minimiser {hist[-1][1]} of {n} sites off, "
          f"b* = {hist[-1][2]:.6g}, c* = {hist[-1][3]:.6g}; their committed c*/b* = {their}: difference {lam_gs - their:.1e}")
    xs = hist[-1][4]; bstar = hist[-1][2]
    lam_k, hk, gk = dinkelbach(4.0 * their, c_a)
    print(f"(2) lambda_kink by the same iteration on (c - c_a)/b: **{lam_k:.9g}** (closing value {gk:.2e}); their bracket [{mk.group(1)}, {mk.group(2)}]; same minimiser: {bool((hk[-1][4] == xs).all())}; "
          f"lambda_gs - lambda_kink = {lam_gs - lam_k:.6g} against c_a / b* = {c_a / bstar:.6g} (c_a = {c_a:.4f})")
    # control: every single-site change of the minimiser has a larger ratio; a wrong ln Z(m_0) is visible
    worse = 0; tried = 0
    for i in range(n):
        for s in range(k[i]):
            if s != xs[i]:
                y = xs.copy(); y[i] = s; cc, bb = cb(y); tried += 1; worse += int(bb <= 0 or cc / bb > lam_gs * (1 + 1e-12))
    print(f"(3) every single-site change of the minimiser has a larger ratio: {worse} of {tried} (must be all); control: at lambda = 0.999 lambda_gs the same pass gives max_x [lambda b - c] = {gmax(0.999 * lam_gs)[0]:.4f} "
          f"(must be negative) and at 1.001 lambda_gs {gmax(1.001 * lam_gs)[0]:.4f} (must be positive)")
    print(f"ALL DONE {time.time() - t0:.0f} s; {npass[0]} (min,+) passes; peak RSS {C.rss():.0f} MB")


if __name__ == "__main__":
    main()
