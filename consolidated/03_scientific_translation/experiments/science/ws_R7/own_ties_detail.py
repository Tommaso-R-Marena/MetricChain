"""R7 OWN: one exact tie of the generic chain in detail, and its dependence on the bond angle.
Usage: python3 own_ties_detail.py"""
import mpmath as mp
import own_ties as ot
import own_ties_structure as st

mp.mp.dps = 50

def poly_in_c(x, c, deg=6):
    rel = mp.pslq([x] + [c ** k for k in range(deg + 1)], maxcoeff=10 ** 5, maxsteps=10 ** 5)
    if rel is None: return "?"
    a0 = rel[0]
    terms = [f"{mp.mpf(-r) / a0}*c^{k}" for k, r in enumerate(rel[1:]) if r != 0]
    return " + ".join(f"({-r}/{a0})c^{k}" if k else f"({-r}/{a0})" for k, r in enumerate(rel[1:]) if r != 0)

def detail(wa, wy, theta_deg=111):
    # geometry with a chosen bond angle
    ot.TH = mp.radians(theta_deg); ot.CT, ot.ST = mp.cos(ot.TH), mp.sin(ot.TH)
    c = -ot.CT
    A, Y = st.labelled(st.word(wa)), st.labelled(st.word(wy))
    print(f"\n=== centre {wa}  point {wy}  bond angle {theta_deg} deg ===")
    tot = mp.mpf(0)
    for k, (a, y) in enumerate(zip(A, Y)):
        d = a[0] - y[0]
        if abs(d) > mp.mpf(10) ** -40:
            tot += abs(d)
            print(f"  rank {k:2d}: centre pair ({a[1]:2d},{a[2]:2d}) s~={mp.nstr(a[0], 12):>14s} = {poly_in_c(a[0], c)} | point pair ({y[1]:2d},{y[2]:2d}) s~={mp.nstr(y[0], 12):>14s} = {poly_in_c(y[0], c)} | diff {mp.nstr(d, 12)}")
    print("  profile distance:", mp.nstr(tot, 40))
    return tot

if __name__ == "__main__":
    wa, wy = st.PAIRS[1]
    detail(wa, wy, 111)
    print("\nDependence on the bond angle (same two torsion words):")
    for th in (109, 109.47, 110, 110.5, 111, 111.5, 112, 113, 115):
        ot.TH = mp.radians(th); ot.CT, ot.ST = mp.cos(ot.TH), mp.sin(ot.TH)
        for (a, y) in st.PAIRS:
            d = ot.mp_dist(st.word(a), st.word(y))
            print(f"  theta={th:7.2f}  {a} / {y}: D = {mp.nstr(d, 30)}")
    ot.TH = mp.radians(111); ot.CT, ot.ST = mp.cos(ot.TH), mp.sin(ot.TH)
