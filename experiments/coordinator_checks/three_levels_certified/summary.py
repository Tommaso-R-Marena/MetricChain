#!/usr/bin/env python3
"""Collect the output files of cert3.py in this directory into one table (best outer fraction per column).

usage:  python3 summary.py            (reads out_*.txt next to this file, except out_terms_*, out_flat_* and
                                       out_summary.txt)

The last columns are NOT computed here: they are the worst instances found for TWO levels by the Computational
Research Division, copied from its messages (branch research/ubuntu-engineering): ENG-RES-0014, table
"three_worst_best" (n = 1000, 4000, 16000; reading (B), the algorithm as built, and reading (A), base brackets'
answers placed adversarially) and ENG-RES-0008, table "main_u1", column "best phi against the worst instance"
(reading (A); the other sizes).  All numbers are ln(.)/(n a) at u = 1.

The two messages are about two outer designs (the Scientific Discovery Division's review SCI-REV-0016, finding M1):
ENG-RES-0014 uses the design of this directory (the referee's ladder x_l = x_0 (b/x_0)^(l/40)); ENG-RES-0008 uses the
same constants with the ladder of inner rates eps* 0.85^i (the ladder of the report's remark (1a) and of K_REPORT.md
section 6.4).  Its entries are marked with a dagger below.  Both ladders were searched at n = 1000, 4000, 16000, where
the two worst cases (reading (A)) are 1.040 / 1.0461, 0.694 / 0.6940, 0.576 / 0.5753.
"""
import glob
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TWO_LEVEL_WORST = {            # n: (reading (B) or None, reading (A)), source
    1000: (1.0114, 1.0461, 'ENG-RES-0014'),
    1400: (None, 0.924, 'ENG-RES-0008'),
    2000: (None, 0.822, 'ENG-RES-0008'),
    4000: (0.6829, 0.6940, 'ENG-RES-0014'),
    8000: (None, 0.619, 'ENG-RES-0008'),
    16000: (0.5749, 0.5753, 'ENG-RES-0014'),
    32000: (None, 0.550, 'ENG-RES-0008'),
    64000: (None, 0.537, 'ENG-RES-0008'),
}
ENG_THREE_WORST = {      # (n, phi_1): (two levels flat, two levels (B), two levels (A), three levels flat, certified C_max of three levels)
    (1000, 0.25): (1.2529, 1.3090, 1.3367, 1.0102, 1.4012),
    (1000, 0.30): (1.2054, 1.2547, 1.2840, 0.9842, 1.3506),
    (1000, 0.35): (1.1523, 1.1931, 1.2208, 0.9727, 1.2645),
    (1000, 0.40): (1.0901, 1.1269, 1.1683, 0.9360, 1.2233),
    (1000, 0.45): (1.0370, 1.0692, 1.1042, 0.9049, 1.1895),
    (1000, 0.50): (0.9839, 1.0114, 1.0461, 0.8645, 1.1554),
    (1000, 0.55): (0.9205, 1.0536, 1.0536, 0.8277, 1.1854),
    (1000, 0.60): (0.8675, 1.1033, 1.1033, 0.8113, 1.2497),
    (1000, 0.65): (0.8147, 1.1655, 1.1655, 0.7828, 1.3139),
    (1000, 0.70): (0.7510, 1.2131, 1.2338, 0.7323, 1.3781),
    (1000, 0.75): (0.6937, 1.2832, 1.2832, 0.6937, 1.4308),
    (1000, 0.80): (0.7123, 1.3444, 1.3451, 0.7123, 1.4948),
    (4000, 0.25): (0.9299, 0.9475, 0.9639, 0.5502, 0.9689),
    (4000, 0.30): (0.8800, 0.8972, 0.9115, 0.5279, 0.9095),
    (4000, 0.35): (0.8262, 0.8437, 0.8564, 0.5029, 0.8687),
    (4000, 0.40): (0.7724, 0.7885, 0.8014, 0.4780, 0.8094),
    (4000, 0.45): (0.7209, 0.7347, 0.7477, 0.4530, 0.7609),
    (4000, 0.50): (0.6670, 0.6829, 0.6940, 0.4602, 0.7261),
    (4000, 0.55): (0.6133, 0.7374, 0.7374, 0.4756, 0.7829),
    (4000, 0.60): (0.5592, 0.7936, 0.7936, 0.5116, 0.8369),
    (4000, 0.65): (0.5519, 0.8466, 0.8466, 0.5519, 0.8934),
    (4000, 0.70): (0.5973, 0.9027, 0.9027, 0.5973, 0.9500),
    (4000, 0.75): (0.6378, 0.9573, 0.9573, 0.6378, 1.0040),
    (4000, 0.80): (0.6841, 1.0074, 1.0118, 0.6841, 1.0604),
    (16000, 0.25): (0.8226, 0.8274, 0.8355, 0.4094, 0.8152),
    (16000, 0.30): (0.7718, 0.7759, 0.7834, 0.3893, 0.7669),
    (16000, 0.35): (0.7201, 0.7242, 0.7318, 0.4053, 0.7185),
    (16000, 0.40): (0.6684, 0.6724, 0.6795, 0.4155, 0.6621),
    (16000, 0.45): (0.6167, 0.6207, 0.6272, 0.4345, 0.6210),
    (16000, 0.50): (0.5650, 0.5749, 0.5753, 0.4527, 0.5899),
    (16000, 0.55): (0.5126, 0.6275, 0.6274, 0.4959, 0.6428),
    (16000, 0.60): (0.5338, 0.6805, 0.6805, 0.5338, 0.6957),
    (16000, 0.65): (0.5797, 0.7316, 0.7328, 0.5797, 0.7486),
    (16000, 0.70): (0.6267, 0.7851, 0.7851, 0.6267, 0.8016),
    (16000, 0.75): (0.6739, 0.8374, 0.8375, 0.6739, 0.8540),
    (16000, 0.80): (0.7184, 0.8887, 0.8897, 0.7184, 0.9062),
}
PAT = re.compile(r"n=(\d+) phi_1=([0-9.]+): two levels: flat ([0-9.na]+), C_max ([0-9.na]+) \| three levels, servers chosen "
                 r"at the flat fibre: flat ([0-9.na]+), C_max with flat middle costs ([0-9.na]+), certified C_max ([0-9.na]+)"
                 r" \| servers chosen by certified cost: flat ([0-9.na]+), certified C_max ([0-9.na]+) \| the same with more "
                 r"middle designs: flat ([0-9.na]+), certified C_max ([0-9.na]+)")
KEYS = ('two_flat', 'two_cmax', 'ref_flat', 'ref_cmax_flat', 'cert', 'tuned_flat', 'tuned', 'searched_flat', 'searched')


def main():
    rows = {}
    files = sorted(f for f in glob.glob(os.path.join(HERE, 'out_*.txt'))
                   if not os.path.basename(f).startswith(('out_terms', 'out_summary', 'out_flat')))
    for f in files:
        for line in open(f):
            m = PAT.match(line)
            if not m:
                continue
            n, phi = int(m.group(1)), float(m.group(2))
            vals = [float(v) for v in m.groups()[2:]]
            rows.setdefault(n, {}).setdefault(phi, {})
            for k, v in zip(KEYS, vals):
                if v == v:                                    # not nan
                    old = rows[n][phi].get(k)
                    assert old is None or abs(old - v) < 5e-5, (f, n, phi, k, old, v)      # files agree where they overlap
                    rows[n][phi][k] = v

    def best(n, key):
        c = [(d[key], phi) for phi, d in rows[n].items() if key in d]
        return min(c) if c else (None, None)

    def fmt(v, phi=None):
        if v is None:
            return '-'
        return ('%.4f' % v) if phi is None else ('%.4f (%.3g)' % (v, phi))

    print("files read: " + ", ".join(os.path.basename(f) for f in files))
    # cross-check with the Computational Research Division's table "three_worst" (ENG-RES-0014), where the grids overlap
    agree = total = 0
    for (n, phi), (e_two_flat, e_two_b, e_two_a, e_three_flat, e_cert) in sorted(ENG_THREE_WORST.items()):
        d = rows.get(n, {}).get(phi)
        if d is None:
            continue
        for key, val in (('two_flat', e_two_flat), ('ref_flat', e_three_flat), ('cert', e_cert)):
            if key in d:
                total += 1
                if abs(d[key] - val) < 5.1e-5:
                    agree += 1
                else:
                    print("DIFFERENT from ENG-RES-0014 at n=%d phi_1=%.2f, %s: here %.4f, there %.4f" % (n, phi, key, d[key], val))
    print("cross-check with ENG-RES-0014, table three_worst (two levels flat; three levels flat; certified C_max of three "
          "levels, servers chosen at the flat fibre): %d of %d numbers agree to the four digits given" % (agree, total))
    # the two-level worst case per outer fraction: its minimum over the division's grid, readings (B) and (A)
    for n in (1000, 4000, 16000):
        mb = min((v[1], phi) for (m, phi), v in ENG_THREE_WORST.items() if m == n)
        ma = min((v[2], phi) for (m, phi), v in ENG_THREE_WORST.items() if m == n)
        assert abs(mb[0] - TWO_LEVEL_WORST[n][0]) < 5.1e-5 and abs(ma[0] - TWO_LEVEL_WORST[n][1]) < 5.1e-5
    print("ln(cost or bound)/(n a), u = 1; in brackets the outer fraction phi_1 of the grid at which the minimum is taken")
    print("| n | outer fractions computed | two levels: certified bound | three levels, servers chosen at the flat fibre: "
          "certified bound | three levels, servers by certified cost (referee's middle designs): certified bound | the same "
          "with more middle designs: certified bound | cost of that design at the flat instance (same fraction) | two "
          "levels: worst instance found by the Computational Research Division, reading (B) / (A); a dagger: for the "
          "other ladder (ENG-RES-0008) | margin: two-level worst found (smaller reading) minus the certified three-level "
          "bound, in units of n a; in nats (with a dagger: a difference between two outer designs) |")
    print("|---|---|---|---|---|---|---|---|---|")
    pu = 1 / (1 + math.e)                            # a = ln 2 - H(1/(1+e)) = 0.11094
    compact = []
    a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
    for n in sorted(rows):
        two, two_phi = best(n, 'two_cmax')
        cert, cert_phi = best(n, 'cert')
        tun, tun_phi = best(n, 'tuned')
        sea, sea_phi = best(n, 'searched')
        sflat = rows[n][sea_phi].get('searched_flat') if sea is not None else None
        wb, wa, src = TWO_LEVEL_WORST.get(n, (None, None, ''))
        three = sea if sea is not None else tun
        w = min(v for v in (wb, wa) if v is not None)
        margin = w - three
        print(("| %d | %s | %s | %s | %s | %s | %s | %s / %s (%s) | %+.3f; %+.0f" + ('†' if src == 'ENG-RES-0008' else '') + " |")
              % (n, ", ".join('%.3g' % p for p in sorted(rows[n])), fmt(two, two_phi), fmt(cert, cert_phi), fmt(tun, tun_phi),
                 fmt(sea, sea_phi), fmt(sflat), fmt(wb), ('%.3f†' % wa) if src == 'ENG-RES-0008' else fmt(wa), src, margin,
                 margin * n * a))
        compact.append("| `%s` | `%.4f` | %s / `%s` | `%.4f` | `%.4f` | %s | %s |"
                       % (format(n, ',').replace(',', ' '), two, ('`%.4f`' % wb) if wb is not None else '—',
                          ('%.3f†' % wa) if src == 'ENG-RES-0008' else '%.4f' % wa, cert, tun,
                          ('**`%.4f`** (`%.3g`)' % (sea, sea_phi)) if sea is not None else 'not computed',
                          ('`%.4f`' % sflat) if sflat is not None else 'not computed'))
    print()
    print("the same, as in theory report section 11.19, remark (1b) (the division's numbers with the digits it gives):")
    print("| `n` | two levels: certified | two levels: worst instance found by the division (algorithm as built / inner answers "
          "placed adversarially) | three levels, certified: servers chosen at the flat fibre | servers by certified cost, the "
          "referee's two middle designs | the same with more middle designs (outer fraction) | cost of that last design at the "
          "flat instance |")
    print("|---|---|---|---|---|---|---|")
    for line in compact:
        print(line)
    print()
    print("† ENG-RES-0008: the same constants with the ladder of inner rates eps* 0.85^i, not the ladder "
          "x_l = x_0 (b/x_0)^(l/40) of this table (SCI-REV-0016, M1).  The certified two-level bound of that design at "
          "the outer fraction 0.50 is 0.9913, 0.8700, 0.7228, 0.6387, 0.5887, 0.5596, 0.5419 at n = 1400, ..., 64000 (the "
          "Scientific Discovery Division's computation; ENG-RES-0008 prints 0.991, 0.870, 0.723, 0.639, 0.589, 0.560, "
          "0.542; our remark (1a) has ln C_max = 153.96 at n = 1400 and 1045.1 at n = 16000, i.e. 0.9912 and 0.5888), where "
          "this table has 0.9933, ..., 0.5407.")


if __name__ == '__main__':
    main()
