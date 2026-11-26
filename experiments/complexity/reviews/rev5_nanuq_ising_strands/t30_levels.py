# t30_levels.py -- compare the authors' dp_levels (Proposition 5; run in a separate process, read-only, no bytecode)
# with the reviewer's own enumeration (strands_mine.py).
import subprocess, sys, json, math, time
from strands_mine import levels

AUTH = '/home/user/MetricChain/experiments/complexity/strands'
def authors(species, counts):
    code = ("import sys, json; sys.path.insert(0, %r); sys.dont_write_bytecode = True\n"
            "from level_counts import dp_levels\n"
            "out, K, bits, naive = dp_levels(%r, %r)\n"
            "print(json.dumps({'phys': sorted([[R, m, v] for (R, m), v in out.items()]), 'K': K, 'bits': bits, 'naive': naive}))") % (AUTH, species, counts)
    r = subprocess.run([sys.executable, '-B', '-c', code], capture_output=True, text=True, cwd='/tmp')
    if r.returncode != 0:
        return {'error': r.stderr[-400:]}
    return json.loads(r.stdout.strip().splitlines()[-1])

cases = [
    (["GC"], [2]), (["GC"], [4]), (["GATC"], [2]), (["GATC"], [3]), (["AT", "GC"], [2, 2]), (["GC", "CG"], [2, 2]),
    (["GCA", "TGC"], [2, 2]), (["G", "C", "GC"], [2, 2, 2]), (["GGC", "GCC"], [2, 2]), (["ATGC"], [3]),
    (["GC", "GGCC"], [2, 1]), (["AT", "GC", "CG"], [2, 2, 2]), (["G", "C"], [4, 4]), (["GCGC"], [3]),
    (["A", "T", "GC"], [1, 1, 2]), (["GC"], [6]), (["AG", "CT"], [3, 3]), (["CATG"], [2]), (["GC", "AT"], [3, 3]),
    (["GGCC", "GC"], [2, 2]), (["GCGCGC"], [2]), (["ACGT", "GC"], [2, 2]),
]
allok = True; lower = 0; total_phys = 0; symset = set()
for species, counts in cases:
    t0 = time.time()
    phys, NR, w = levels(species, counts)
    mine = sorted([[R, m, v] for (R, m), v in phys.items()])
    a = authors(species, counts)
    N = sum(len(s) * n for s, n in zip(species, counts)); c = sum(counts)
    if 'error' in a:
        print(species, counts, "AUTHORS' PROGRAM FAILED:", a['error']); allok = False; continue
    ok = (mine == a['phys'])
    allok &= ok
    total_phys += sum(v for _, _, v in mine)
    symset |= {R for R, _, _ in mine}
    # bound of Proposition 5: |W| <= 24^N < 2^K
    K = math.ceil(N * math.log2(24)) + 1
    assert w <= 24 ** N < 2 ** K and K == a['K']
    mfe = min(m + math.log(R) for R, m, v in mine) if mine else None
    # symmetry-naive value: min_d (m_d + ln d), m_d = least energy among structures whose symmetry is a multiple of d
    g = 0
    for n in counts: g = math.gcd(g, n)
    naive = None
    for d in range(1, g + 1):
        if g % d: continue
        ms = [m for R, m, v in mine if R % d == 0]
        if ms:
            vv = min(ms) + math.log(d)
            naive = vv if naive is None else min(naive, vv)
    flag = ''
    if mine and naive < mfe - 1e-12:
        lower += 1; flag = ' naive (min,+) value %.3f < true MFE' % naive
        # claim of the note: this happens exactly when every loop-energy minimiser is symmetric
        mmin = min(m for R, m, v in mine)
        assert all(R > 1 for R, m, v in mine if m == mmin)
    elif mine:
        mmin = min(m for R, m, v in mine)
        assert any(R == 1 for R, m, v in mine if m == mmin), "naive = true although all minimisers are symmetric?"
    print("%-34s N=%2d c=%d |W|=%7d phys=%7d symmetries %s agree=%s bits=%d (c*N^2=%d) MFE=%s%s [%.1fs]" % (
        list(zip(species, counts)), N, c, w, sum(v for _, _, v in mine), sorted({R for R, _, _ in mine}), ok, a['bits'], c * N * N,
        'none' if mfe is None else '%.3f' % mfe, flag, time.time() - t0), flush=True)
print("ALL AGREE" if allok else "MISMATCH", "| systems:", len(cases), "| physical structures compared:", total_phys,
      "| symmetry degrees seen:", sorted(symset), "| naive value too low in", lower, "systems")
