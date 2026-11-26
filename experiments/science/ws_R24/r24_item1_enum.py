#!/usr/bin/env python3
"""R24, item 1 (ii)-(iv) on an ENUMERABLE floor: lambda_gs = min_x c(x)/b(x) by brute force over every state against
(1) Dinkelbach's ratio iteration with the referee's own (min,+) elimination, (2) the same iteration with the model's own
(min,+) pass, (3) the coordinator's bisection (floor_ground_state.py, re-run as a subprocess into this directory).
Then, exactly by enumeration: F(lambda) = ln Z(m_lambda) - ln Z(m_0), the occupancy, lambda_c by its three definitions,
and the two-sided statement the referee proposes (report, section 2):
     G(lambda) <= F(lambda) <= (lambda/lambda') G(lambda') + ln sum_x pi_0(x)^(1 - lambda/lambda')      (0 <= lambda <= lambda').
Objects of the coordinator that are USED (not rebuilt): the floor without penalty (band model lo0), the penalty tables
g1, g2, g3 in the window form, RND, BETA -- taken from the frame of floor_transition.main().  Everything computed from
them here is the referee's code (r24_common.py).
Run: python3 -B r24_item1_enum.py K5 4 2 > r24_item1_enum_K5_m4_w2.log
"""
import os, sys, time, math, subprocess, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PI = os.path.normpath(os.path.join(HERE, "..", "pi_inference"))
sys.path.insert(0, PI); sys.path.insert(0, HERE)
import r24_common as C


def lse(a):
    m = a.max(); return float(m + math.log(np.exp(a - m).sum()))


def main():
    seq, m, w = sys.argv[1], sys.argv[2], sys.argv[3]; t0 = time.time()
    import floor_transition as FT
    got, text = C.capture(FT, [seq, m, w, "--grid", "0,0.01", "--N", "4"], "floor_transition.py")
    for line in text.split("\n"):
        if line.startswith("=== ") or line.startswith("(1)") or line.startswith("(2)"): print("[theirs] " + line[:330], flush=True)
    BETA, RND = FT.BETA, FT.RND
    lo0, g1, g2, g3, k, x0, n = got["lo0"], got["g1"], got["g2"], got["g3"], list(got["k"]), [int(v) for v in got["x0"]], got["n"]
    model, pen, z0 = got["model"], got["pen"], got["z0"]
    # ---------------------------------------------------------------- own objects from their tables
    c0, fac0 = C.factors_of(lo0)
    facp = [((i,), np.asarray(g1[i], float)) for i in range(n)] + [(tuple(K), np.asarray(v, float)) for K, v in g2.items()] + [(tuple(K), np.asarray(v, float)) for K, v in g3.items()]
    E0 = C.energy_all(c0, fac0, k).ravel(); P = C.energy_all(0.0, facp, k).ravel()                  # kcal/mol, every state
    st = np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, n); N = len(st)
    dev_e = float(np.abs(E0 - lo0.energy(st)).max()); dev_p = float(np.abs(P - pen(st)).max())
    # control of the comparison itself: one table entry changed by 1e-6 kcal/mol must be seen
    facx = [(U, t.copy()) for U, t in fac0]; facx[n][1].flat[0] += 1e-6; ctrl_e = float(np.abs(C.energy_all(c0, facx, k).ravel() - lo0.energy(st)).max())
    print(f"(0) {N} states; my evaluation of their tables against their own evaluators at every state: floor without penalty {dev_e:.1e} kcal/mol, penalty {dev_p:.1e} "
          f"(control: one table entry moved by 1e-6 is seen as {ctrl_e:.1e}) [{time.time() - t0:.0f}s]", flush=True)
    tmin = min(float(t.min()) for _, t in facp); ia = int(np.ravel_multi_index(x0, k))
    print(f"(1) signs: least entry of any penalty table {tmin:.3g} kcal/mol (>= 0: {tmin >= 0}); penalty at the anchor {P[ia]:.3g}; states with a positive penalty: {int((P > 0).sum())} of {N}; "
          f"states with a NEGATIVE penalty: {int((P < 0).sum())}; RND - 1 = {RND - 1:.1e} (the model subtracts lambda*RND*pen: b = beta*RND*pen)")
    L0 = lse(-BETA * E0); c = L0 + BETA * E0; b = BETA * RND * P
    L0_el = C.eliminate(fac0, k, "sum", -BETA) - BETA * c0
    print(f"(2) ln Z(m_0): by enumeration {L0:.10f}; by my elimination {L0_el:.10f}; their transfer matrix {z0:.10f}; least c(x) = {c.min():.3e} at state {st[int(np.argmin(c))].tolist()} "
          f"(anchor {x0}: c = {c[ia]:.6f}); rounding of c: an error eps in ln Z(m_0) moves every ratio c/b by eps/b, here |L0 - z0| = {abs(L0 - z0):.1e}")
    pos = b > 0
    r = np.full(N, np.inf); r[pos] = c[pos] / b[pos]; j = int(np.argmin(r)); lam_gs = float(r[j])
    cmin = float(c.min()); rk = np.full(N, np.inf); rk[pos] = (c[pos] - cmin) / b[pos]; jk = int(np.argmin(rk)); lam_kink = float(rk[jk])
    print(f"(3) BRUTE FORCE over every state: lambda_gs = min c/b = {lam_gs:.10g} at state {st[j].tolist()} ({int((st[j] != np.array(x0)).sum())} of {n} sites off; b* = {b[j]:.6g}, c* = {c[j]:.6g}); "
          f"lambda_kink = min (c - c_min)/b = {lam_kink:.10g} at state {st[jk].tolist()}; same state: {j == jk}; second smallest ratio c/b: {float(np.partition(r, 1)[1]):.10g}")

    # ---------------------------------------------------------------- Dinkelbach, own (min,+)
    def fac_lam(lam):
        return fac0 + [(U, -lam * RND * t) for U, t in facp]

    def own_argmax(lam):
        """max_x [lam b(x) - c(x)] and a maximiser, by my elimination of -beta * m_lambda"""
        val, x = C.eliminate(fac_lam(lam), k, "max", -BETA, want_arg=True)
        return val - BETA * c0 - L0, x

    def ratio_of(x):
        i = int(np.ravel_multi_index(x, k)); return c[i] / b[i], b[i], c[i]
    lam = float(c[int(np.argmax(b))] / b.max()); passes = 0; hist = [lam]
    while True:
        g, x = own_argmax(lam); passes += 1
        if g <= 1e-10: break
        lam = ratio_of(x)[0]; hist.append(lam)
    g_close, x_close = own_argmax(lam); lam_d = lam
    print(f"(4) DINKELBACH with my own (min,+) elimination: start {hist[0]:.6g} (the state of largest penalty), iterates {', '.join(f'{v:.8g}' for v in hist[1:])}; "
          f"{passes} passes; lambda_gs = {lam_d:.10g}; closing pass at that lambda: max_x [lambda b - c] = {g_close:.2e} (must be 0 to rounding); "
          f"brute force - Dinkelbach = {lam_gs - lam_d:.2e}")
    # the model's own (min,+) pass, value only, at the same lambdas; and their back-tracking
    import floor_ground_state as FG
    devv = 0.0
    for lamv in hist + [0.0, 0.5 * lam_d, 2 * lam_d]:
        v_their = -BETA * model(lamv).minimum() - z0; devv = max(devv, abs(v_their - own_argmax(lamv)[0]))
    lam2 = hist[0]; p2 = 0
    while True:
        e, x = FG.argmin_state(model(lam2)); p2 += 1; g = -BETA * e - z0
        if g <= 1e-10: break
        lam2 = ratio_of(x)[0]
    print(f"(5) the MODEL'S OWN (min,+) pass (BandModel.dp, their back-tracking): value against mine at {len(hist) + 3} lambdas: largest difference {devv:.1e}; Dinkelbach with it: {p2} passes, lambda_gs = {lam2:.10g} "
          f"(brute force - this = {lam_gs - lam2:.2e})")
    # control: a ratio iteration on a WRONG objective (b without RND, c with ln Z shifted by 1e-3) must not reproduce the brute-force number to 1e-9
    bw = BETA * P; cw = c + 1e-3; rw = np.full(N, np.inf); rw[pos] = cw[pos] / bw[pos]
    print(f"(6) controls: the least ratio with ln Z(m_0) wrong by 1e-3: {float(rw.min()):.10g} (differs from lambda_gs by {float(rw.min()) - lam_gs:.2e}; must be visible); "
          f"without the factor RND in b: differs by {float((c[pos] / (BETA * P[pos])).min()) - lam_gs:.2e} (relative {RND - 1:.0e}: NOT visible at the printed digits)")
    assert abs(lam_gs - lam_d) < 1e-9 * lam_gs and abs(lam_gs - lam2) < 1e-9 * lam_gs and abs(g_close) < 1e-8
    # ---------------------------------------------------------------- the coordinator's bisection, re-run into this directory
    tag = f"{seq.replace(':', 'c')}_m{m}_w{w}"; out = os.path.join(HERE, f"rerun_floor_ground_state_{tag}.log")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
    rc = subprocess.run([sys.executable, "-B", os.path.join(PI, "floor_ground_state.py"), seq, m, w], cwd=PI, env=env, stdout=open(out, "w"), stderr=subprocess.PIPE)
    txt = open(out).read(); done = "ALL DONE" in txt
    mk = re.search(r"\(c\) lambda_kink in \[([0-9.e+-]+), ([0-9.e+-]+)\]", txt); mg = re.search(r"\(d\) lambda_gs in \[([0-9.e+-]+), ([0-9.e+-]+)\].*?c\*/b\* = ([0-9.e+-]+)", txt)
    if done and mk and mg:
        print(f"(7) THEIR script re-run (output in {os.path.basename(out)}, reached ALL DONE: {done}): lambda_kink in [{mk.group(1)}, {mk.group(2)}], lambda_gs in [{mg.group(1)}, {mg.group(2)}], c*/b* = {mg.group(3)}; "
              f"brute force inside their bracket for lambda_gs: {float(mg.group(1)) * (1 - 1e-4) <= lam_gs <= float(mg.group(2)) * (1 + 1e-4)}; for lambda_kink: {float(mk.group(1)) * (1 - 1e-4) <= lam_kink <= float(mk.group(2)) * (1 + 1e-4)}")
    else:
        print(f"(7) THEIR script re-run did not reach its last line (return code {rc.returncode}); stderr tail: {rc.stderr.decode()[-300:]!r}")
    # ---------------------------------------------------------------- exact F(lambda), occupancy, the three "lambda_c", by enumeration
    off = (st != np.array(x0)[None]).sum(axis=1).astype(float)

    def exact(lamv):
        a = lamv * b - c; F = lse(a); p = np.exp(a - F); return F, float((p * off).sum()), float(p[j]), float(p[ia])

    def G(lamv): return float((lamv * b - c).max())
    grid = sorted(set([0.0] + list(np.linspace(0.02, 3.0, 150) * lam_gs)))
    Fv = np.array([exact(v)[0] for v in grid]); Gv = np.array([G(v) for v in grid])
    viol = int((Gv > Fv + 1e-12).sum()); ctrl = int((1.05 * np.maximum(Gv, 0) + 1e-3 > Fv + 1e-12).sum())
    print(f"(8) G(lambda) <= F(lambda) = ln Z(m_lambda) - ln Z(m_0) on {len(grid)} values of lambda up to 3 lambda_gs, exact by enumeration: {viol} violations (must be 0); "
          f"control, 1.05 max(G, 0) + 0.001 <= F: {ctrl} violations (must be positive)")

    def cross(f, lo_, hi_, target):
        for _ in range(200):
            mid = 0.5 * (lo_ + hi_)
            if f(mid) < target: lo_ = mid
            else: hi_ = mid
        return 0.5 * (lo_ + hi_)
    hi_l = 4 * lam_gs
    occ_end = exact(hi_l)[1]
    lam_half = cross(lambda v: exact(v)[1], 0.0, hi_l, n / 2) if occ_end >= n / 2 else float("nan")
    # equal weights of "reference" (states with zero penalty) and "displaced" (states with positive penalty): exact two-set definition
    def frac_disp(v):
        a = v * b - c; F = lse(a); return float(np.exp(a[pos] - F).sum())
    lam_eq = cross(frac_disp, 0.0, hi_l, 0.5)
    lam_ln2 = cross(lambda v: exact(v)[0], 0.0, hi_l, math.log(2.0))
    print(f"(9) exact 'transition' of this floor by three definitions: mean number of sites off the anchor = n/2 at lambda = {lam_half:.6g} (the scan's definition; occupancy at 4 lambda_gs: {occ_end:.3f}); "
          f"states with a positive penalty carry half the weight at {lam_eq:.6g}; F = ln 2 at {lam_ln2:.6g}.  lambda_gs / these: {lam_gs / lam_half:.4f}, {lam_gs / lam_eq:.4f}, {lam_gs / lam_ln2:.4f}; "
          f"lambda_kink / these: {lam_kink / lam_half:.4f}, {lam_kink / lam_eq:.4f}, {lam_kink / lam_ln2:.4f}")
    F1, o1, pj1, pa1 = exact(lam_gs)
    print(f"    at lambda_gs: F = {F1:.4f} (G = 0), weight of the minimiser {pj1:.4f}, of the anchor {pa1:.4f}, mean sites off {o1:.3f}; at lambda = 1 (the certificate): F = {exact(1.0)[0]:.6g}, mean sites off {exact(1.0)[1]:.4f}")
    # ---------------------------------------------------------------- the two-sided statement
    lp0 = -c                                                                  # ln pi_0(x)

    def renyi(theta): return lse(theta * lp0)                                # ln sum_x pi_0(x)^theta
    bad = 0; cnt = 0; badc = 0; badh = 0; worst = -1e9; tight = []
    for lp_ in (lam_gs, 0.7 * lam_gs, 1.5 * lam_gs, 2.5 * lam_gs):
        Gp = G(lp_)
        for v in np.linspace(0.0, lp_, 41):
            F = exact(v)[0]; ub = (v / lp_) * Gp + renyi(1.0 - v / lp_); cnt += 1; bad += int(F > ub + 1e-10); worst = max(worst, F - ub)
            badc += int(F > (v / lp_) * Gp + 1e-10)                         # control: the bound WITHOUT the Renyi term (one state against the sum, reversed)
            badh += int(F > (v / lp_) * max(Gp, 0.0) + 0.5 * renyi(1.0 - v / lp_) + 1e-10)
            if lp_ == lam_gs and abs(v / lp_ - round(v / lp_ * 10) / 10) < 1e-9: tight.append((v / lp_, F, ub))
    print(f"(10) TWO-SIDED: F(lambda) <= (lambda/lambda') G(lambda') + ln sum_x pi_0(x)^(1 - lambda/lambda') for 0 <= lambda <= lambda', {cnt} pairs (lambda' = 0.7, 1, 1.5, 2.5 lambda_gs): "
          f"{bad} violations (must be 0; largest F - bound = {worst:.2e}); control, the same without the Renyi term: {badc} violations (must be positive); "
          f"for information, with HALF the Renyi term: {badh} violations (0 means the bound is loose by more than a factor two in the exponent -- the first version of this script used this as its control, and it could not fail)")
    print("     with lambda' = lambda_gs (G = 0):  lambda/lambda_gs | exact F | upper bound ln sum pi_0^(1 - lambda/lambda_gs)")
    for q, F, ub in tight: print(f"       {q:.1f} | {F:.6g} | {ub:.6g}")
    # rigorous brackets for the lambda at which F reaches t: lambda_gs (1 - theta_t) <= lambda_t <= lambda_gs + t / b*, theta_t: ln sum pi_0^theta = t
    for t in (0.1, math.log(2.0), 1.0):
        lo_, hi_ = 0.0, 1.0
        for _ in range(200):
            mid = 0.5 * (lo_ + hi_)
            if renyi(mid) > t: lo_ = mid
            else: hi_ = mid
        th = hi_; lt = cross(lambda v: exact(v)[0], 0.0, hi_l, t)
        print(f"(11) F reaches t = {t:.3f} at lambda_t = {lt:.6g} (exact); certified bracket [lambda_gs (1 - theta_t), lambda_gs + t/b*] = [{lam_gs * (1 - th):.6g}, {lam_gs + t / b[j]:.6g}] "
              f"(theta_t = {th:.5f}); inside: {lam_gs * (1 - th) <= lt * (1 + 1e-12) and lt <= (lam_gs + t / b[j]) * (1 + 1e-12)}; lower end / lambda_t = {lam_gs * (1 - th) / lt:.3f}")
    # ---------------------------------------------------------------- the coordinator's "two phases with their entropies", on exact numbers
    # theirs (floor_ground_state.py, line (h)):  Z_ref(lam) = Z(m_0) e^{lam s0},  Z_d = Z(m_lam) - Z_ref,  S_d(lam) = ln Z_d - G(lam),
    #   lam_eq = lambda_gs - (S_d(lam_in) - lam_in s0) / b*   with lam_in = the measured lambda_c.
    # identity (where the minimiser is the ground state at lam_in):  lam_eq - lam_in = - ln( Z_d / Z_ref )(lam_in) / b*,
    # and the fixed point lam_eq = lam_in is the solution of  F(lam) = ln 2 + lam s0.
    s0 = float((np.exp(-c) * b).sum())                                       # beta <pen>_0, exactly
    def lam_eq_of(lin):
        F = exact(lin)[0]; zd = math.exp(F) - math.exp(lin * s0)
        return (lam_gs - (math.log(zd) - G(lin) - lin * s0) / b[j]) if zd > 0 else float("nan")
    fix = cross(lambda v: exact(v)[0] - v * s0, 0.0, hi_l, math.log(2.0))
    rows = [(nm, lin, lam_eq_of(lin)) for nm, lin in (("lambda_kink", lam_kink), ("0.95 lambda_c", 0.95 * lam_half), ("lambda_c (occupancy n/2, exact)", lam_half), ("1.05 lambda_c", 1.05 * lam_half), ("lambda_gs", lam_gs))]
    print(f"(12) their two-entropy estimate lam_eq = lambda_gs - (S_d(lam_in) - lam_in s0)/b*, with S_d read off the exact ln Z at lam_in (s0 = beta <pen>_0 = {s0:.6g} exactly): "
          + "; ".join(f"lam_in = {nm} = {lin:.5g} -> {le:.5g} ({100 * (le / lam_half - 1):+.2f} % from lambda_c)" for nm, lin, le in rows)
          + f".  Its fixed point is the root of F = ln 2 + lambda s0: {fix:.6g} ({100 * (fix / lam_half - 1):+.2f} % from lambda_c); for comparison lambda_kink is {100 * (lam_kink / lam_half - 1):+.2f} % and lambda_gs {100 * (lam_gs / lam_half - 1):+.2f} % from lambda_c; "
          f"(lambda_gs - lambda_c) b* = {(lam_gs - lam_half) * b[j]:.3f} nats, c* = {c[j]:.2f}, so 1 nat is {100 / c[j]:.1f} % of lambda_gs here")
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {C.rss():.0f} MB")


if __name__ == "__main__":
    main()
