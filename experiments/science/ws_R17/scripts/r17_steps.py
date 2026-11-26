#!/usr/bin/env python3
"""R17: the two inductive steps (Propositions Q6 and Q7 of Q_REPORT) with SATURATING inner families, exact
constants of Theorem 11.56 from our r16lib (replication of the kind of check of Q_REPORT 7.2 and of the referee
R12, section 2.3-2.4, with our own code).

The inner family is given the certified cost  d B - sigma min(x, R d)  EXACTLY (error function 0): the worst that
the hypothesis H(B, sigma, R; 0) allows (C_max is nondecreasing in the inner costs).  The exact ln C_max of the level
as built is compared with the bound of the proposition:
   slope step:  n B - sigma' xhat + c_S(n, Lam; B),          sigma' = sigma + B/h - 1,  Lam = ln(1/delta) + n ln 2
   drop:        n B' + c_D(n, Lam)                (with shift);  the same with c_pi-bar in place of B*sigma(n) (no shift).
Also checked at every level (inside r17_nest): x_out, Lemma Q4 / Q3, (4.1) / (4.2), (2.1).
(B, sigma, R) run along the epoch schedule and through extreme values off it.
usage: python3 r17_steps.py <budget seconds>"""
import math, os, resource, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r17_nest as N
import r17_formula as F
import r16lib as R

INF = float("inf")


class Synth:
    """a family whose certified cost equals the majorant d B - sigma min(x, R d); error function 0"""

    def __init__(self, C, B, sigma, Rr):
        self.C, self.u, self.B, self.sigma, self.Rr = C, C.u, B, sigma, Rr
        self.name = "Synth(B=%.4g, sigma=%.3g, R=%.4g)" % (B, sigma, Rr)

    def E(self, d, x, Lam):
        return 0.0

    def cost(self, d, x, ld, variant):
        return d * self.B - self.sigma * (x if self.Rr == INF else min(x, self.Rr * d))


def main():
    t0 = time.time()
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 600.0
    tot = dict(S=0, Sviol=0, D=0, Dviol=0, Dn=0, Dnviol=0)
    worstS = (INF, None)
    worstD = (INF, None)
    worstDn = (INF, None)
    capped = 0
    stop = False
    for u in (1.0, 2.0, 0.5):
        C = F.Cube(u)
        d, J, k, B, Rm, phi = C.epochs(12)
        # ---- slope step: (B, sigma, R) along the schedule (the j-th step of epoch m has B_m, j/d_m, h/j; j = 0: R = inf)
        triples = []
        for m in range(0, 9):
            for j in range(0, J[m]):
                triples.append((B[m], j / d[m], INF if j == 0 else C.h / j, "epoch %d, step %d" % (m, j + 1)))
        # ---- off the schedule
        for Bx in (C.h, 1.01 * C.h, 2 * C.h, C.a, 11 * C.h):
            for sg, Rx in ((0.0, INF), (0.3, C.h), (1.0, C.h), (1.0, C.h / 3), (0.7, C.h / 50)):
                triples.append((Bx, sg, Rx, "off schedule"))
        for n in (1000, 4000, 16000, 40000 if u == 1.0 else 12000):
            X0 = 1 + F.c_log(C, n) + C.h
            for ld in (math.log(0.05), -float(n), -50.0 * n):
                Lam = -ld + n * math.log(2)
                for (Bx, sg, Rx, tag) in triples:
                    Rp = C.h if Rx == INF else Rx * C.h / (C.h + Rx)
                    if Rp * n < X0:
                        continue
                    fam = Synth(C, Bx, sg, Rx)
                    S = N.Slope(C, fam)
                    for frac in (0.0, 0.03, 0.2, 0.6, 1.0):
                        if time.time() - t0 > budget:
                            stop = True
                            break
                        xhat = X0 + 1e-9 + frac * (Rp * n - X0 - 1e-9)
                        lcm, lev = S.level(n, xhat, ld, 'proof')
                        bound = n * Bx - S.sigma * xhat + F.c_S(C, n, Lam, Bx)
                        tot['S'] += 1
                        capped += lev.xs[1] < math.ceil(xhat)
                        sl = bound - lcm
                        if sl < -1e-9:
                            tot['Sviol'] += 1
                        if sl < worstS[0]:
                            worstS = (sl, (u, n, "%.3g" % ld, tag, "B/h=%.3f sigma=%.3f R/h=%s" % (Bx / C.h, sg, "inf" if Rx == INF else "%.4f" % (Rx / C.h)),
                                           "xhat=%.2f n_o=%d" % (xhat, lev.n_o), "c_S=%.1f" % F.c_S(C, n, Lam, Bx)))
                    if stop:
                        break
                    R.clear_tabs()
                if stop:
                    break
            if stop:
                break
        # ---- drop: inner family H(B, 1, R); R, B along the schedule (R_m = h/J_m, B_m) and off it
        if not stop:
            eh, cs, alpha = F.accuracies(1.0, 9)
            dtr = [(B[m], Rm[m], cs[m], alpha[m + 1], alpha[m], "epoch %d" % m) for m in range(0, 9)]
            for Bx in (C.h, C.a, 3 * C.a):
                for Rx in (C.h, C.h / 7, C.h / 100):
                    # c = 1/3 has w(c) = 1.57 > 1, so no alpha <= 1 gives beta = alpha - w(c) > 0: Proposition Q7's own
                    # hypotheses (0 < alpha <= 1, beta >= x_min > 0) exclude it (the first version of this script tried
                    # it and stopped on the assertion beta >= x_min: not_cited/steps_saturating_failed_*.log)
                    for c in (1 / 8, 1 / 26, 1e-2, 1e-4):
                        al = min(1.0, 1.5 * F.w_of_c(c))
                        assert al - F.w_of_c(c) > 0
                        dtr.append((Bx, Rx, c, al, 0.0, "off schedule"))
            for n in (200, 1000, 10000, 40000):
                for ld in (math.log(0.05), -float(n)):
                    Lam = -ld + n * math.log(2)
                    for (Bx, Rx, c, al, xmin, tag) in dtr:
                        if time.time() - t0 > budget:
                            stop = True
                            break
                        fam = Synth(C, Bx, 1.0, Rx)
                        D = N.Drop(C, fam, c, al, xmin)
                        if n < F.nD_prime(C, c):
                            continue
                        sig = F.cpi_bar(C, math.floor(D.phi * n), F.ell_c(C, c)) / (C.a + Rx)
                        cD = F.c_D(C, n, Lam, Bx, Rx, D.phi, c)
                        cp = F.cpi_bar(C, math.floor(D.phi * n), F.ell_c(C, c))
                        no_s = math.floor(D.phi * n - sig)
                        no_n = math.floor(D.phi * n)
                        if no_s >= 1:
                            lcm, lev = D.level(n, no_s, ld, 'proof', True)
                            sl = n * D.B + cD - lcm
                            tot['D'] += 1
                            tot['Dviol'] += sl < -1e-9
                            if sl < worstD[0]:
                                worstD = (sl, (u, n, "%.3g" % ld, tag, "B/h=%.3f R/h=%.4f c=%.4g" % (Bx / C.h, Rx / C.h, c), "c_D=%.1f" % cD))
                        if no_n >= 1:
                            lcm, lev = D.level(n, no_n, ld, 'proof', False)
                            sl = n * D.B + cD - Bx * cp / (C.a + Rx) + cp - lcm
                            tot['Dn'] += 1
                            tot['Dnviol'] += sl < -1e-9
                            if sl < worstDn[0]:
                                worstDn = (sl, (u, n, "%.3g" % ld, tag, "B/h=%.3f R/h=%.4f c=%.4g" % (Bx / C.h, Rx / C.h, c)))
                    R.clear_tabs()
                    if stop:
                        break
                if stop:
                    break
        print("u=%g done so far: slope levels %d (violations %d), drops with shift %d (%d), without shift %d (%d)  [%.0f s]"
              % (u, tot['S'], tot['Sviol'], tot['D'], tot['Dviol'], tot['Dn'], tot['Dnviol'], time.time() - t0))
        sys.stdout.flush()
        if stop:
            print("# time budget reached")
            break
    print("\nSLOPE STEP (Proposition Q6), saturating inner family: %d levels (%d with a capped ladder); violations %d; "
          "least slack bound - exact = %.2f nats at %s" % (tot['S'], capped, tot['Sviol'], worstS[0], worstS[1]))
    print("DROP with shift (Proposition Q7): %d levels; violations %d; least slack %.2f at %s"
          % (tot['D'], tot['Dviol'], worstD[0], worstD[1]))
    print("DROP without shift: %d levels; violations %d; least slack %.2f at %s" % (tot['Dn'], tot['Dnviol'], worstDn[0], worstDn[1]))
    print("violations recorded by the level checks inside r17_nest (x_out, Lemma Q4/Q3, (4.1)/(4.2), (2.1), Q6/Q7 with E): %d %s"
          % (N.stats['viol'], N.viol_log[:3]))
    print("LAST LINE r17_steps.py: completed%s; wall %.1f s; peak RSS %.1f MB"
          % (" (budget reached)" if stop else "", time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))


if __name__ == "__main__":
    main()
