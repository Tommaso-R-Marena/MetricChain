"""Driver for h5_cells_small_slope.py: the three-round game with a code of cells at level 1
(small-slope limit, box Lipschitz body, exact min-plus envelopes on a grid of step d).
gain > 0 would be a three-round lower bound above h; the plain dip gives 1 - 2 sqrt(theta)."""
import numpy as np, sys
from h5_cells_small_slope import solve
d = 0.01
for theta in (0.25, 0.26, 0.28):
    res = []
    for phi1 in (0.03, 0.05, 0.1, 0.2, 0.3, 0.45, 0.6):
        for phi2 in (0.05, 0.1, 0.2, 0.3, 0.45, 0.6):
            if 1 - phi1 - phi2 < 0.15: continue
            for R1 in (0.0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2):
                r = solve((np.sqrt(phi1), np.sqrt(phi2), np.sqrt(1 - phi1 - phi2)), R1, 0.0, theta, d=d, lim=1.1)
                res.append((r['gain'], phi1, phi2, R1, r['at']))
    res.sort(key=lambda t: -t[0])
    print("theta = %.2f: plain dip value 1 - 2 sqrt(theta) = %+.4f; grid step %.2f (envelopes exact on the grid; region boundaries rounded to it)" % (theta, 1 - 2*np.sqrt(theta), d))
    for t in res[:4]:
        print("   largest gain %+.4f at phi1 %.2f phi2 %.2f R1 %.3f, hidden type (%.2f, %.2f, %.2f)" % (t[0], t[1], t[2], t[3], *t[4]))
    print("   smallest gain %+.4f; %d parameter sets" % (res[-1][0], len(res)))
    sys.stdout.flush()
