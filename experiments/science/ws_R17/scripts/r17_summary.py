#!/usr/bin/env python3
"""R17: (1) a table of the simulation campaigns parsed from logs/sim_slope_*.log (my own logs);
(2) a few derived numbers quoted in the report that no other log prints."""
import glob, math, os, re, resource, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r17_formula as F
t0 = time.time()
LOGS = os.path.join(HERE, "..", "logs")
print("== (1) simulation campaigns, per level design ==")
print("log | u n n_o | xhat ln(theta) L K r_dag (floor(rho_h n_o)+1) ln(1/pi) [bound] | runs valid closed aborted G | "
      "violations every-run / good-event | width/xhat min..max (closed, valid) | max M/Mdag | max calls/bound | max used/cnt")
grand = dict(runs=0, valid=0, closed=0, abort=0, G=0, det=0, good=0, designs=0)
ALL = []
for path in sorted(glob.glob(os.path.join(LOGS, "sim_slope_*.log"))):
    name = os.path.basename(path)
    lines = open(path).read().split("\n")
    complete = any(l.startswith("LAST LINE") for l in lines)
    cur = None
    rows = []
    tiny = False
    for l in lines:
        if l.startswith("## delta"):
            tiny = True
        m = re.match(r"## level u=(\S+) n=(\d+) n_o=(\d+) n_i=(\d+) xhat=(\S+) ln\(theta\)=(\S+) L=(\d+) K=(\d+) J=(\d+) "
                     r"m_max=(\d+) r_dag=(\d+) \(r1=(\d+),.*?ln\(1/pi\)=(\S+) \(<= n_o h \+ ln\(n_o\+1\) = (\S+)\)", l)
        if m:
            cur = dict(u=m.group(1), n=int(m.group(2)), no=int(m.group(3)), xhat=float(m.group(5)), lth=float(m.group(6)),
                       L=int(m.group(7)), K=int(m.group(8)), rdag=int(m.group(11)), r1=int(m.group(12)),
                       lpi=float(m.group(13)), lpib=float(m.group(14)), runs=0, valid=0, closed=0, abort=0, G=0, det=0,
                       good=0, wmin=9.0, wmax=0.0, mdag=0.0, calls=0.0, used=0.0, tiny=tiny)
            tiny = False
            rows.append(cur)
            continue
        m = re.match(r"\S+ \d+ \d+ \| (\S+)\s+d0=\S+\s+s_in=\S+\s+(\S+)\s+\| (\S+)\s+G=(\d) det=(\d+) good=(-?\d+) \| (\S+) (\S+) "
                     r"(\S+) (\S+) (\S+) (\S+) (\S+)", l)
        if m and cur is not None:
            cur['runs'] += 1
            G = int(m.group(4))
            valid = m.group(2) in ("center", "top", "bottom", "adv_hi", "adv_lo", "exact", "random", "narrow", "mix")
            cur['valid'] += valid
            cur['closed'] += m.group(3) == "closed"
            cur['abort'] += m.group(3) == "abort"
            cur['G'] += G
            cur['det'] += int(m.group(5)) > 0
            cur['good'] += (int(m.group(6)) > 0)
            if m.group(3) == "closed" and valid:
                w = float(m.group(7))
                cur['wmin'] = min(cur['wmin'], w); cur['wmax'] = max(cur['wmax'], w)
            cur['mdag'] = max(cur['mdag'], float(m.group(9)))
            if m.group(10) != "-":
                cur['calls'] = max(cur['calls'], float(m.group(10)))
            if m.group(11) != "-":
                cur['used'] = max(cur['used'], float(m.group(11)))
    for r in rows:
        if r['runs'] == 0:
            continue
        r['log'] = name
        ALL.append(r)
        print("%s | %s %d %d%s | %.2f %.2f %d %d %d (%d) %.2f [%.2f] | %d %d %d %d %d | %d / %d | %.3f..%.4f | %.3f | %.4f | %.4f"
              % (name, r['u'], r['n'], r['no'], " delta=2^-n" if r['tiny'] else "", r['xhat'], r['lth'], r['L'], r['K'], r['rdag'],
                 r['r1'], r['lpi'], r['lpib'], r['runs'], r['valid'], r['closed'], r['abort'], r['G'], r['det'], r['good'],
                 r['wmin'], r['wmax'], r['mdag'], r['calls'], r['used']))
        for k in ('runs', 'valid', 'closed', 'abort', 'G', 'det', 'good'):
            grand[k] += r[k]
        grand['designs'] += 1
    print("   %s: %s" % (name, "reached its last line" if complete else "INCOMPLETE - not to be cited"))
print("ALL CAMPAIGNS: level designs %(designs)d, runs %(runs)d (valid oracle %(valid)d), closed %(closed)d, aborted %(abort)d, "
      "events (V1)-(V3) held in %(G)d, runs with a violation of an every-run claim %(det)d, of a good-event claim %(good)d" % grand)

print("\n== (1b) the same as a markdown table (sorted by u, n_o) ==")
print("| `u` | `n` | `n_o` | `x̂` | `ln θ` | rungs | `δ` | `K` | `r†` (`⌊ρ_h n_o⌋+1`) | runs: valid + invalid oracle | closed / aborted | violations | width`/x̂`, valid runs | largest sample`/M†` |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in sorted(ALL, key=lambda r: (float(r['u']), r['tiny'], r['no'], r['n'])):
    print("| %s | %d | %d | %.2f | %.2f | %d | %s | %d | %d (%d) | %d + %d | %d / %d | %d | %.4f – %.4f | %.2f |"
          % (r['u'], r['n'], r['no'], r['xhat'], r['lth'], r['L'], "`2^{-n}`" if r['tiny'] else "0.05", r['K'], r['rdag'], r['r1'],
             r['valid'], r['runs'] - r['valid'], r['closed'], r['abort'], r['det'] + r['good'],
             r['wmin'], r['wmax'], r['mdag']))
print("\n== (2) derived numbers ==")
for u in (0.5, 1.0, 2.0, 4.0):
    C = F.Cube(u)
    vals = []
    for n in (64000, 10 ** 6, 10 ** 8, 10 ** 10):
        L0 = math.log(20.0) + n * math.log(2)
        vals.append(F.c_S(C, n, 2 * L0, C.a) - (C.a / C.h + 4) * math.log(n))
    lim = ((C.a / C.h) * (1 + math.log(6) + 2 * u + math.exp(u) + C.h) + 1 + 2 * math.log(2 * u + math.log(2))
           + math.log(18 * math.e * (math.e - 1)) + math.log(36 * math.log(2)))
    print("u=%g: l_S - (a/h+4) ln n at n = 6.4e4, 1e6, 1e8, 1e10 (delta = 0.05): %s; limit formula %.2f; a/h = %.4f; "
          "(a/h)/(a/h+4) = %.3f; first term of the constant %.2f"
          % (u, ", ".join("%.2f" % v for v in vals), lim, C.a / C.h, (C.a / C.h) / (C.a / C.h + 4),
             (C.a / C.h) * (1 + math.log(6) + 2 * u + math.exp(u) + C.h)))
C = F.Cube(1.0)
print("X_0(n) at u=1: n=470: %.4f (h n = %.4f); u=2, n=202: %.4f (h n = %.4f)"
      % (1 + F.c_log(C, 470) + C.h, C.h * 470, 1 + F.c_log(F.Cube(2.0), 202) + F.Cube(2.0).h, F.Cube(2.0).h * 202))
print("shortfall (1 + c_log(n))/h of the outer block at u=1: n=470: %.1f sites; n=1e6: %.1f sites"
      % ((1 + F.c_log(C, 470)) / C.h, (1 + F.c_log(C, 10 ** 6)) / C.h))
# the closed form of Theorem Q9(b) at n = 1e10 in units of sqrt(n ln n)
n = 10 ** 10
Lam0 = math.log(20.0) + n * math.log(2)
lS = F.c_S(C, n, 2 * Lam0, C.a)
kd = math.sqrt((1 + C.rbar) * C.c1 * n / lS)
d, J, k, B, R, phi = C.epochs(80)
M = max(m for m in range(80) if k[m] <= kd)
eh, c, alpha = F.accuracies(1.0, M)
lD = max(F.c_D(C, n, 2 * Lam0, B[m], R[m], phi[m], c[m]) - F.c_D_sqrt_part(C, n, B[m], R[m], phi[m], c[m]) for m in range(M))
lB = F.E_base(C, n, alpha[0], 2 * Lam0) - C.u * math.sqrt(n * F.ell0_x(C, alpha[0]) / 2)
b, dr, a0 = F.C1_series(C, 1.0, M)
val = n * C.h + 2 * math.sqrt((1 + C.rbar) * C.c1 * n * lS) + (b + dr) * math.sqrt(n) + M * lD + lB
best, rows, ep = F.best_M(C, n, 1.0, math.log(20.0))
print("n=1e10: closed form of Thm Q9(b) (M=%d): (value - nh)/sqrt(n ln n) = %.2f; formula (5.2) at its best M: %.3f; C_* = %.3f"
      % (M, (val - n * C.h) / math.sqrt(n * math.log(n)), (best[1] - n * C.h) / math.sqrt(n * math.log(n)), C.Cstar))
for n in (64000, 10 ** 6, 10 ** 8, 10 ** 10):
    best, rows, ep = F.best_M(C, n, 1.0, math.log(20.0))
    det = F.E_total(C, n, 1.0, math.log(20.0), best[0], ep=ep, detail=True)
    print("n=%.3g: bound = %.1f nats = %.4f n a; E_M = %.1f = base %.1f + %d slope steps %.1f (mean %.1f) + drops %.1f "
          "(sqrt-terms %.1f, shift terms %.1f)" % (n, best[1], best[1] / (n * C.a), det['E'], det['base'], det['nslope'],
                                                 det['slope'], det['slope'] / det['nslope'], det['drop'], det['drop_sqrt'],
                                                 det['drop_shift']))
# Proposition Q9a: the closed form dominates (5.2) wherever its hypothesis T q* <= Lam_0 holds
print("\n== (3) Proposition Q9a: E_M <= C_1 sqrt(n) + (T - M) l_S + M l_D + l_B  where T q* <= Lam_0 ==")
ncase = nhyp = nviol = 0
worst = (1e300, None)
maxratio = 0.0
for u in (0.5, 1.0, 2.0):
    Cu = F.Cube(u)
    for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 8, 10 ** 10):
        for eps, lid in ((1.0, math.log(20.0)), (0.1, math.log(20.0)), (1.0, float(n))):
            Lam0 = lid + n * math.log(2)
            d, J, k, B, R, phi = Cu.epochs(30)
            for M in (0, 1, 2, 3, 5, 8, 12, 16, 20, 25):
                if k[M] > 20000:
                    continue
                ncase += 1
                eh, c, alpha = F.accuracies(eps, M)
                T = k[M] - 1
                qstar = max([F.q_S(Cu, n, 2 * Lam0)] + [F.q_D(Cu, n, 2 * Lam0, c[m]) for m in range(M)])
                if T * qstar > Lam0:
                    continue
                nhyp += 1
                det = F.E_total(Cu, n, eps, lid, M, ep=(d, J, k, B, R, phi), detail=True)
                lS = F.c_S(Cu, n, 2 * Lam0, Cu.a)
                lD = max([F.c_D(Cu, n, 2 * Lam0, B[m], R[m], phi[m], c[m]) - F.c_D_sqrt_part(Cu, n, B[m], R[m], phi[m], c[m])
                          for m in range(M)] or [0.0])
                lB = F.E_base(Cu, n, alpha[0], 2 * Lam0) - Cu.u * math.sqrt(n * F.ell0_x(Cu, alpha[0]) / 2)
                bb, dr, a0 = F.C1_series(Cu, eps, M)
                closed = (bb + dr) * math.sqrt(n) + (T - M) * lS + M * lD + lB
                maxratio = max(maxratio, det['LamT'] / det['Lam0'])
                if closed - det['E'] < worst[0]:
                    worst = (closed - det['E'], (u, n, eps, "e^-n" if lid > 10 else "0.05", M))
                if closed < det['E'] - 1e-9:
                    nviol += 1
print("cases %d; with the hypothesis %d; violations %d; least (closed form - E_M) = %.2f nats at (u, n, eps, delta, M) = %s; "
      "largest Lam_T/Lam_0 among them %.4f (claimed <= 2)" % (ncase, nhyp, nviol, worst[0], worst[1], maxratio))
# (4) beyond 1e12: the closed form of Proposition Q9a minimised over M (the referee R12's O2, quoted in TR 11.58a(b):
#     "beyond 1e12 the ratio keeps falling towards about 2 sqrt((a-h)(a/h+4))": 0.99, 1.92, 3.31 at n = 1e150 for u = 1/2, 1, 2).
#     r17_formula.py takes logarithms of products like 2 A_n m-bar (n+3), which overflow a float beyond n ~ 1e100; the
#     same formulas are therefore re-typed here with sums of logarithms ("_big") and validated against r17_formula at 1e12, 1e50.
def lKS_big(C, n, Lam):
    return math.log(18 * (Lam + math.log(2) + math.log(F.A_n(C, n)) + math.log(F.mbar_S(C, n)) + math.log(n + 3)) + 1)


def cS_big(C, n, Lam, Bv):
    return ((1 + F.c_log(C, n) + C.h) * Bv / C.h + 1 + 2 * math.log(F.A_n(C, n)) + math.log(18 * math.e * (math.e - 1))
            + lKS_big(C, n, Lam) + math.log(n + 3))


def qS_big(C, n, Lam):
    return math.log(4 * (n + 1)) + math.log(F.A_n(C, n)) + math.log(24 * math.e * (math.e - 1)) + lKS_big(C, n, Lam)


def lKD_big(C, n, Lam, c):
    return math.log(4 / c ** 2 * (Lam + math.log(2) + math.log(F.A_n(C, n) / c) + math.log(F.mbar_D(C, n, c))
                                  + math.log(n + 4)) + 1)


def cD_big(C, n, Lam, Bv, Rv, ph, c):
    cp = F.cpi_bar(C, math.floor(ph * n), F.ell_c(C, c))
    Pcnt = math.log(F.A_n(C, n) / c) + math.log(7.45) + math.log(F.nubar_D(C, n, c)) + lKD_big(C, n, Lam, c)
    return Bv * (1 + ph * F.nD_prime(C, c)) + Bv * cp / (C.a + Rv) + math.log(n + 4) + 1 + Pcnt


def qD_big(C, n, Lam, c):
    return math.log(4 * (n + 2)) + math.log(11.17) + math.log(F.nubar_D(C, n, c)) + lKD_big(C, n, Lam, c)


print("\n== (4) beyond 1e12: min over M of the closed form of Prop Q9a, in units of sqrt(n ln n) (hypothesis T q* <= Lam_0 required) ==")
C1v = F.Cube(1.0)
dv, Jv, kv, Bv_, Rv_, phv = C1v.epochs(20)
worstdiff = 0.0
for nn in (1e12, 1e50):
    L0 = math.log(20.0) + nn * math.log(2)
    for m in (0, 3, 12):
        cm = 1.0 / (13.0 * (m + 1) * (m + 2))
        worstdiff = max(worstdiff, abs(cS_big(C1v, nn, 2 * L0, Bv_[m]) - F.c_S(C1v, nn, 2 * L0, Bv_[m])),
                        abs(qS_big(C1v, nn, 2 * L0) - F.q_S(C1v, nn, 2 * L0)),
                        abs(cD_big(C1v, nn, 2 * L0, Bv_[m], Rv_[m], phv[m], cm) - F.c_D(C1v, nn, 2 * L0, Bv_[m], Rv_[m], phv[m], cm)),
                        abs(qD_big(C1v, nn, 2 * L0, cm) - F.q_D(C1v, nn, 2 * L0, cm)))
print("validation of the re-typed formulas against r17_formula.py at n = 1e12, 1e50 (u=1, m = 0, 3, 12): max |difference| = %.2e nats" % worstdiff)
for u in (0.5, 1.0, 2.0):
    Cu = F.Cube(u)
    Mx = 760
    d, J, k, B, R, phi = Cu.epochs(Mx)
    out = []
    for e10 in (12, 20, 50, 100, 150):
        n = 10.0 ** e10
        lid = math.log(20.0)
        Lam0 = lid + n * math.log(2)
        lS = cS_big(Cu, n, 2 * Lam0, Cu.a)
        qS = qS_big(Cu, n, 2 * Lam0)
        best = (float("inf"), -1)
        sumw = 0.0
        c1drops = 0.0
        lD = 0.0
        qD = 0.0
        for M in range(0, Mx):
            if M > 0:
                m = M - 1
                cm = 1.0 / (13.0 * (m + 1) * (m + 2))
                sumw += F.w_of_c(cm)
                c1drops += math.sqrt(phi[m] * F.ell_c(Cu, cm) / 2) * B[m + 1] / Cu.a
                lD = max(lD, cD_big(Cu, n, 2 * Lam0, B[m], R[m], phi[m], cm) - F.c_D_sqrt_part(Cu, n, B[m], R[m], phi[m], cm))
                qD = max(qD, qD_big(Cu, n, 2 * Lam0, cm))
            T = k[M] - 1
            if T * max(qS, qD) > Lam0:
                break
            a0 = 1.0 - sumw
            l0 = F.ell0_x(Cu, a0)
            lB = F.E_base(Cu, n, a0, 2 * Lam0) - Cu.u * math.sqrt(n * l0 / 2)
            C1 = Cu.u * (math.sqrt(l0 / 2) + c1drops)
            val = n * Cu.h / d[M] + C1 * math.sqrt(n) + (T - M) * lS + M * lD + lB      # n (B_M - h) = n h / d_M
            if val < best[0]:
                best = (val, M)
        out.append("1e%d: %.3f (M=%d)" % (e10, best[0] / math.sqrt(n * math.log(n)), best[1]))
    print("u=%g: %s;   2 sqrt((a-h)(a/h+4)) = %.3f;  C_* = %.3f"
          % (u, "; ".join(out), 2 * math.sqrt((Cu.a - Cu.h) * (Cu.a / Cu.h + 4)), Cu.Cstar))
print("LAST LINE r17_summary.py: completed; wall %.1f s; peak RSS %.1f MB"
      % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
