"""R7: external control of the total conformation counts of the lattice class tables against the published number of
n-step self-avoiding walks on the diamond lattice (OEIS A001394; b-file https://oeis.org/A001394/b001394.txt, fetched
2026-11-25 through a page-reading tool, values typed below as returned).

A chain with n torsions has n+2 bonds; the enumerators fix the first two bonds (4 * 3 = 12 choices by lattice symmetry),
so   conformations(n) = c_{n+2} / 12.
"""
import own_lattice_cert as lc
A001394 = [1, 4, 12, 36, 108, 324, 948, 2796, 8196, 24060, 70188, 205284, 597996, 1744548, 5073900, 14774652, 42922452,
           124814484, 362267652, 1052271732, 3051900516, 8857050204, 25671988020, 74449697484, 215677847460,
           625096195404, 1810062340812, 5243388472212, 15177125874564, 43945760757084, 127158808850532,
           368051019383220, 1064650562078244]
ok = True
for n in range(1, 25):
    hist, count, gmin = lc.read_table(n)
    tot = sum(count)
    c = A001394[n + 2]
    same = (c % 12 == 0) and (c // 12 == tot)
    ok &= same
    print(f"n={n:2d}: class table total {tot:>15d}   A001394({n+2})/12 = {c // 12:>15d}   {'equal' if same else 'DIFFERENT'}")
print("all 24 totals equal the published series / 12:", ok)
