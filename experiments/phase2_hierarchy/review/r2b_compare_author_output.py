"""Cross-check of the author's Lemma B table (out/h1_relaxation_lemma_check.txt, read as text, script not imported)
against the reviewer's exact extremal functions (shortest paths), for the same blocks, roles, slope and Theta = ratio n h.
The author's hypotheses have no parity; the reviewer's are computed without and with parity."""
import re
import sys
from r2_lemmaB import extremal
from rv_common import consts

path = '../out/h1_relaxation_lemma_check.txt'
pat = re.compile(r"u=([\d.]+) ns=\(([\d, ]+)\) roles=(\w+) theta/h=([\d.]+) .*viol=\s*([-+\d.]+) .*hidden max=\s*([-+\w.]+) vs")
rows = []
for line in open(path):
    mm = pat.search(line)
    if mm:
        rows.append((float(mm.group(1)), [int(x) for x in mm.group(2).split(',')], mm.group(3), float(mm.group(4)),
                     float(mm.group(5)), float(mm.group(6))))
print('author rows parsed:', len(rows))
maxdiff_v = 0.0
maxdiff_h = 0.0
max_par = 0.0
bigger = 0
for i, (u, ns, roles, ratio, viol, hid) in enumerate(rows):
    if i % 4 != 0 and not (u == 4.0 and ratio == 1.0):      # a quarter of the table plus the critical-budget rows at u = 4
        continue
    c = consts(u)
    n = sum(ns)
    Theta = ratio * n * c['h']
    o0 = extremal(ns, roles, u, Theta, parity=False)
    o1 = extremal(ns, roles, u, Theta, parity=True)
    myhid0 = o0['Xhidden'] - (Theta - n * c['h']) if o0['Xhidden'] == o0['Xhidden'] else float('-inf')
    dv = o0['X'] - viol
    dh = (myhid0 - hid) if (myhid0 > -1e300 and hid > -1e300) else 0.0
    if (myhid0 > -1e300) != (hid > -1e300):
        dh = float('nan')
    maxdiff_v = max(maxdiff_v, abs(dv))
    maxdiff_h = max(maxdiff_h, abs(dh)) if dh == dh else float('inf')
    max_par = max(max_par, o1['X'] - o0['X'])
    bigger += (dv > 2e-3)
    print('u=%g ns=%s %s theta/h=%.2f | author viol=%+8.3f hid=%+9.3f | reviewer (no parity) X=%+8.3f hid=%+9.3f | with parity X=%+8.3f'
          % (u, ns, roles, ratio, viol, hid, o0['X'], myhid0, o1['X']), flush=True)
print('max |reviewer X(no parity) - author viol| = %.4f ; max |difference of hidden maxima| = %.4f ; rows where the exact extremal value exceeds the author\'s by > 0.002: %d'
      % (maxdiff_v, maxdiff_h, bigger))
print('max increase of X due to parity-dependent profiles: %.4f' % max_par)
