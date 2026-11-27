"""r10_14: RE-RUN of the theory division's own functions (ylib.py of workstream Y, from a scratch
copy; nothing of mine except this driver) at slopes they did not report, as a cross-check of
my large-slope finding: Markov-recursion bound with L = 3,
    h_inf <= h_bracket( P^(3)(.|+) with slopes (u,u,u*) ) / 3   (their certified bracket over all t),
    a_inf <= capacity / 3.
usage: python3 r10_14_rerun_their_functions.py <path to the copy of experiments/workstreams/Y/code>"""
import sys, time
sys.path.insert(0, sys.argv[1])
import ylib
t0 = time.time()
for u in (1.0, 3.0, 4.0):
    hc, ac, Ec = ylib.cube_numbers(u)
    print("u=%.1f  cube (their closed forms): h=%.6f a=%.6f E=%.6f" % (u, hc, ac, Ec))
    for p in (0.3, 0.2, 0.1):
        us = ylib.ustar(u, p)
        for L in (2, 3):
            V = ylib.lip_vertices([u] * (L - 1) + [us])
            P = ylib.gibbs_rows(ylib.bsc_block_law_cond(L, p, 0), V)
            hlo, hup, tst = ylib.h_bracket(P, scale=L)
            a = ylib.capacity(P)
            print("   p=%.1f L=%d (%d vertices, u*=%.4f): h in [%.6f, %.6f] (t*=%.3f)  ratio to cube %.4f | a <= %.6f  ratio %.4f   (%.0fs)"
                  % (p, L, len(V), us, hlo, hup, tst, hup / hc, a[1] / L, a[1] / L / ac, time.time() - t0), flush=True)
