"""Which splits of N[kB, k1, k2] get a negative weight, or a wrong support, and with which value (exploration)."""
import sys
from level2_nongalled import *


def describe_split(n, names, i, j):
    U = [names[q] for q in range(i + 1, j + 1)]
    V = [names[q] for q in range(n) if not (i + 1 <= q <= j)]
    side = U if len(U) <= len(V) else V
    cnt = {}
    for s, _ in side:
        cnt[s] = cnt.get(s, 0) + 1
    return "{" + ",".join(f"{s}{k}" if s != "y" else "y" for s, k in side) + "}"


if __name__ == "__main__":
    maxtot = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    for tot in range(5, maxtot + 1):
        for kB in range(0, tot + 1):
            for k1 in range(0, tot - kB + 1):
                k2 = tot - kB - k1
                n, names, sigma, al, neg, wrong = status(kB, k1, k2)
                if not neg and not wrong:
                    continue
                items = []
                for (i, j), v in sorted(neg):
                    items.append(f"NEG {describe_split(n, names, i, j)}={v // 2 if v % 2 == 0 else v / 2}")
                for (i, j), v in sorted(wrong):
                    m = 0
                    for q in range(i + 1, j + 1):
                        m |= 1 << q
                    items.append(f"{'zero-on-displayed' if canon(n, m) in sigma else 'positive-on-undisplayed'} "
                                 f"{describe_split(n, names, i, j)}={v // 2 if v % 2 == 0 else v / 2}")
                print(f"[{kB},{k1},{k2}] n={n}: " + "; ".join(items))
