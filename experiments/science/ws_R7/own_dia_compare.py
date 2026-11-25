"""R7: compare the class tables of my own enumerator (own_dia) with the engineering class tables
(experiments/eng/chain_cover/data/dia_Sc12_n*.txt at a2f6dc7).  Compared per class: (h3,h8,h11) -> (count, gmin, gmax)."""
import subprocess, sys, time
from pathlib import Path
ENG = Path(__file__).resolve().parent / "eng_copy" / "experiments" / "eng" / "chain_cover" / "data"

def read_eng(n):
    d = {}
    for line in (ENG / f"dia_Sc12_n{n}.txt").read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        v = [int(t) for t in line.split()]
        d[tuple(v[:3])] = (v[3], v[4], v[6])       # count, gmin, gmax
    return d

def parse_own(text, d=None):
    d = {} if d is None else d
    for line in text.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        v = [int(t) for t in line.split()]
        k = tuple(v[:3])
        if k in d:
            c, a, b = d[k]
            d[k] = (c + v[3], min(a, v[4]), max(b, v[5]))
        else:
            d[k] = (v[3], v[4], v[5])
    return d

def run_own(n, extra=()):
    return subprocess.run(["./own_dia", "-n", str(n), *extra], check=True, capture_output=True, text=True).stdout

if __name__ == "__main__":
    n0, n1 = int(sys.argv[1]), int(sys.argv[2])
    extra = sys.argv[3:]
    for n in range(n0, n1 + 1):
        t0 = time.time()
        own = parse_own(run_own(n, extra))
        eng = read_eng(n)
        same = own == eng
        print(f"n={n} own: conformations={sum(v[0] for v in own.values())} classes={len(own)}; "
              f"engineering table: conformations={sum(v[0] for v in eng.values())} classes={len(eng)}; identical={same} "
              f"({time.time()-t0:.1f}s)", flush=True)
        if not same:
            diff = [(k, own.get(k), eng.get(k)) for k in sorted(set(own) | set(eng)) if own.get(k) != eng.get(k)]
            print("   first differences:", diff[:5])
