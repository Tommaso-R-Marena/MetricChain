"""R7: numbers of ENG-RES-0002 that are stated in prose or in derived tables, recomputed with my own code from the
class tables (experiments/eng/chain_cover/data/dia_Sc12_n*.txt at a2f6dc7) and from results/lattice_Sc12_flip.json."""
import json
import numpy as np
import own_lattice_cert as lc

print("finite-size table (section 3): n | N | max pairs in cutoff / N | max ||N||_1 / N | gmin of that class")
for n in (8, 12, 16, 18, 20, 22, 24):
    hist, count, gmin = lc.read_table(n)
    N = n + 3
    C = np.cumsum(hist, axis=1)
    norm = 5 * C[:, 0] + 3 * C[:, 1] + 1 * C[:, 2]            # ||N||_1 = 9 h3 + 4 h8 + 1 h11
    assert (norm == 9 * hist[:, 0] + 4 * hist[:, 1] + hist[:, 2]).all()
    i = int(norm.argmax())
    print(f"  {n:2d} | {N} | {hist.sum(axis=1).max() / N:.2f} | {norm.max() / N:.2f} | {gmin[i]}/{n}")
hist, count, gmin = lc.read_table(24)
norm = 9 * hist[:, 0] + 4 * hist[:, 1] + hist[:, 2]
for g in (3, 4, 5):
    print(f"n=24: largest ||N||_1 among classes with gmin <= {g}: {norm[gmin <= g].max()} ({norm[gmin <= g].max() / 27:.2f} per bead)")
print("sequence (section 2): n: conformations / classes")
for n in range(13, 25):
    hist, count, gmin = lc.read_table(n)
    print(f"  {n}: {sum(count)} / {len(hist)}")
print("N^P_cov(eps=0)/N^2 at N = 10, 15, 21, 27 (text: 0.100, 0.093, 0.109, 0.110-0.126):")
res = json.loads((lc.ENG / "results" / "lattice_Sc12.json").read_text()); rows = {r["n_torsions"]: r for r in res["rows"]}
for n in (7, 12, 18, 24):
    c = rows[n]["cover"]["L=1,eps=0"]; N = n + 3
    lo = c["N_cov"] if c["proved_optimal"] else max(c["lower_certified"], c["lower_solver"])
    print(f"  N={N}: [{lo / N**2:.3f}, {c['N_cov'] / N**2:.3f}]")
cl = {n: len(lc.read_table(n)[0]) for n in (12, 24)}
import math
print("effective exponent of the number of classes between N=15 and N=27 (text: 4.3):", round(math.log(cl[24] / cl[12]) / math.log(27 / 15), 2))
print("eps=N/2 sequence n=5..24:", [rows[n]["cover"]["L=1,eps=1/2*N"]["N_cov"] for n in range(5, 25)])
print("largest entry at L=1/5 over all n and eps (text: 'at most 8'):", max(v["N_cov"] for n in rows for k, v in rows[n]["cover"].items() if k.startswith("L=1/5")))
# single-flip constants against Proposition 11.74 (ENG-RES-0009 section 1)
flip = json.loads((lc.ENG / "results" / "lattice_Sc12_flip.json").read_text())["rows"]
tot = bad = 0
for r in sorted(flip, key=lambda r: r["n_torsions"]):
    n, c = r["n_torsions"], r["c_sf"]
    js = [j for j in range(1, n + 1) if min(j, n + 1 - j) >= 5]
    if not js: continue
    d = lambda j: min(j, n + 1 - j)
    lo = min(c[j - 1] - (14 * d(j) - 15) for j in js); hi = max(c[j - 1] / (70 * (d(j) + 3)) for j in js)
    v = sum(not (14 * d(j) - 15 <= c[j - 1] <= 70 * (d(j) + 3)) for j in js)
    tot += len(js); bad += v
    print(f"  flip bounds n={n}: {len(js)} torsions with d_j>=5, least c_j-(14d_j-15) = {lo}, largest c_j/(70(d_j+3)) = {hi:.3f}, violated {v}")
print("  all:", tot, "violated:", bad)
print("min_j c_j/d_j per n (text: between 14 and 22 from n=8):", {r["n_torsions"]: round(min(r["c_sf"][j] / min(j + 1, r["n_torsions"] - j) for j in range(r["n_torsions"])), 1) for r in flip if r["n_torsions"] >= 8})
