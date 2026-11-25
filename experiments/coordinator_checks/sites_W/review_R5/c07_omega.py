"""The error term of Theorem 11.97(c) as the proof gives it (my bookkeeping, NOTES section 1): evaluate
A = 2k + o1 + o2 (shift), B = [p_n ln q + eta + ln2/n]/(1 - p_n) + omega' + ln(N_orb)/n (additive, deep case),
C = (3k + o1 + o2 + ln(N_orb)/n)/2 (shallow case), and compare omega_n = max(A, B, C) with q n^(-1/(2q+2)) + c n^(-1/4)."""
import math
def terms(n, m, q, D, pimin):
    k = n ** -0.25
    D1 = max(D, 1.0)
    k1 = k / ((2 + m * q) * D1); k2 = k / (2 + m * q)
    M = math.ceil(n ** (1 / (2 * q + 2)))
    lnN = m * (q - 1) * math.log(n + 1)                      # ln N_orb <= m (q-1) ln(n+1)
    o1 = (1 + math.log(2 * n * D + 1) + lnN) / n
    o2 = m * q * (1 + (M + 1) ** q) * math.log(n + 1) / n
    pn = 2 * (1 + m * q) * math.exp(-2 * n * k1 * k1)
    eta = q / M + m * q * (M + 1) ** q * math.log(n + 1) / n
    omp = m * k2 * (q * math.exp(D) / pimin + math.log(1 / pimin))
    if pn >= 0.5:
        return None
    A = 2 * k + o1 + o2
    B = (pn * math.log(q) + eta + math.log(2) / n) / (1 - pn) + omp + lnN / n
    C = (3 * k + o1 + o2 + lnN / n) / 2
    return A, B, C, q / M, pn
for (m, q, D, pimin) in ((1, 2, 1.0, 0.3), (2, 3, 2.4, 0.2), (3, 4, 2.0, 0.05)):
    print("m = %d, q_max = %d, D_max = %.1f, pi_min = %.2f" % (m, q, D, pimin))
    for e in (4, 6, 8, 10, 12, 16, 20, 30):
        n = 10.0 ** e
        t = terms(n, m, q, D, pimin)
        if t is None:
            print("   n = 1e%d: p_n >= 1/2 (below n0: omega_n = D_max)" % e); continue
        A, B, C, lead, pn = t
        om = max(A, B, C)
        print("   n = 1e%d: A = %.3e  B = %.3e  C = %.3e  ->  omega_n = %.3e;  leading q/M = %.3e;  (omega_n - q n^(-1/(2q+2))) / n^(-1/4) = %.2f;  p_n = %.1e"
              % (e, A, B, C, om, lead, (om - q * n ** (-1 / (2 * q + 2))) / n ** -0.25, pn))
