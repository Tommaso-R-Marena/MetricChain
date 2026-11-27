#!/usr/bin/env python3
"""The tables of SCI-RES-0034 and of addendum item 92, generated from the four JSON exports of product_threshold.py and the
committed scans floor_transition_<case>.log -- no number of those tables is typed by hand.

Adds one split that product_threshold.py does not print: the factor B2 (one state against all states with its displaced
set) = B2a x B2b, with
    B2a = [ln(1/P_0(all of S* off)) + sum_{i in S*} ln k_i] / ln(1/P_0(all of S* off))     (k_i = number of off states of site i:
          what B2 would be if the off states of each displaced site were equally likely -- mere counting),
    B2b = c* / [ln(1/P_0(all of S* off)) + sum_{i in S*} ln k_i]                           (the off states the extremal state uses
          are rarer than that).
Checks: A x B1 x B2a x B2b x C must equal lambda_gs / lambda_0 (1e-9); the exported lambda_0 must equal the ratio at the
exported minimising set recomputed from the exported q and table maxima (1e-9) -- a check of the export itself.
Run: python3 -B product_threshold_tables.py > product_threshold_tables.log
"""
import json, math, os, re
D = os.path.dirname(os.path.abspath(__file__))
CASES = [("K12_m4_w4", "Lys₁₂, order 4, band 4"), ("K12_m4_w7", "Lys₁₂, order 4, band 7"), ("K12_m3_w7", "Lys₁₂, order 3, band 7"), ("LKSEc12_m3_w7", "(LKSE)₃, order 3, band 7")]


def load():
    return {c: json.load(open(os.path.join(D, f"product_threshold_{c}.json"))) for c, _ in CASES}


def b2_split(j):
    S = j["displaced_sites"]; cS = j["ln_inv_P_all_of_Sstar_off"]; cnt = sum(math.log(j["states_per_site"][i] - 1) for i in S)
    return (cS + cnt) / cS, j["cost_kT"] / (cS + cnt), cS / len(S), cnt / len(S), j["cost_kT"] / len(S)


def tables():
    J = load()
    t1 = ["| case | tables (site sets of sizes) | sum of their maxima, kT | `Δ` | `1/(eΔ)` | sites with `q_i ≥ 1/(eΔ)` | `q_max` | **`λ₀`** | measured `λ_c` | **`λ₀/λ_c`** | `λ_gs/λ₀` | minimising set | explicit criterion |", "|" + "---|" * 13]
    t2 = ["| case | `λ_gs/λ₀` | `A`: `S*` is not the binary minimiser | `B1`: the band against a product, at `S*` | `B2`: one state against all states with that displaced set | of it `B2a`: the number of off states | `B2b`: the state's off states are rarer than average | `C`: table maxima against the penalty paid | sites displaced in `x*` | per displaced site, kT: being off / + the count of off states / the state | at the full set: `ln(1/P₀(all off))` against `Σ ln(1/q_i)` |", "|" + "---|" * 11]
    t3 = ["| case | `λ₀` | grid value nearest to `λ₀` | exact gain there | first order | ratio | largest grid value below `0.9 λ_c` (as a fraction of `λ_c`) | exact gain there | first order | ratio |", "|" + "---|" * 10]
    for c, name in CASES:
        j = J[c]; q = j["q"]; tm = j["table_maxima_kT"]; sizes = sorted(set(len(k.split(",")) for k in tm)); tot = sum(tm.values()); thr = 1 / (math.e * j["Delta"])
        # check of the export: lambda_0 at the exported minimising set
        S0 = set(j["minimising_set"]); g = sum(v for k, v in tm.items() if set(int(u) for u in k.split(",")) <= S0); r0 = sum(math.log(1 / q[i]) for i in S0) / g
        assert abs(r0 - j["lambda_0"]) <= 1e-9 * r0 and j["entropy_factor"] <= 0, c
        b2a, b2b, per_set, per_cnt, per_state = b2_split(j); whole = j["cost_kT"] / j["penalty_kT"] / j["lambda_0"]
        assert abs(j["factor_A"] * j["factor_B1"] * b2a * b2b * j["factor_C"] - whole) <= 1e-9 * whole and abs(b2a * b2b - j["factor_B2"]) <= 1e-9 * j["factor_B2"], c
        t1.append(f"| {name} | {len(tm)} ({', '.join(str(s) for s in sizes)}) | {tot:.5g} | {j['Delta']} | {thr:.4f} | {sum(1 for v in q if v >= thr)} of {j['sites']} | {j['q_max']:.3f} | **{j['lambda_0']:.4g}** | {j['measured_lambda_c']:.5g} | "
                  f"**{j['lambda_0'] / j['measured_lambda_c']:.3f}** | {j['lambda_gs'] / j['lambda_0']:.2f} | {len(j['minimising_set'])} of {j['sites']} sites | void |")
        lq = sum(math.log(1 / v) for v in q)
        t2.append(f"| {name} | {whole:.2f} | {j['factor_A']:.3f} | {j['factor_B1']:.3f} | {j['factor_B2']:.2f} | {b2a:.2f} | {b2b:.2f} | {j['factor_C']:.2f} | {len(j['displaced_sites'])} of {j['sites']} | "
                  f"{per_set:.1f} / {per_set + per_cnt:.1f} / {per_state:.1f} | {j['ln_inv_P_all_sites_off']:.2f} against {lq:.2f} |")
        rows = []
        for line in open(os.path.join(D, f"floor_transition_{c}.log")):
            m = re.match(r"\| ([0-9.]+) \| [0-9.]+ \| ([0-9.e+-]+) \| ([0-9.e+-]+) \|", line)
            if m and float(m.group(1)) > 0: rows.append((float(m.group(1)), float(m.group(2)), float(m.group(3))))
        near = min(rows, key=lambda r: abs(math.log(r[0] / j["lambda_0"]))); far = max((r for r in rows if r[0] < 0.9 * j["measured_lambda_c"]), key=lambda r: r[0])
        t3.append(f"| {name} | {j['lambda_0']:.4g} | {near[0]:g} | {near[1]:.4g} | {near[2]:.4g} | {near[1] / near[2]:.3f} | {far[0]:g} ({far[0] / j['measured_lambda_c']:.2f}) | {far[1]:.4g} | {far[2]:.4g} | {far[1] / far[2]:.2f} |")
    return "\n".join(t1), "\n".join(t2), "\n".join(t3), J


if __name__ == "__main__":
    a, b, c, J = tables()
    print("(1) the Complexity division's zero-temperature threshold on four floors\n" + a + "\n")
    print("(2) the exact split of lambda_gs / lambda_0 at the extremal state (A x B1 x B2a x B2b x C; asserted to 1e-9)\n" + b + "\n")
    print("(3) the exact gain against its first-order term, from the committed scans\n" + c + "\n")
    for cs, name in CASES:
        j = J[cs]; print(f"{name}: off states per site {[k - 1 for k in j['states_per_site']]}; q: {', '.join(f'{v:.3g}' for v in j['q'])}; extremal state {j['extremal_state']}, displaced sites {j['displaced_sites']}")
    print("checks passed: the exported lambda_0 equals the ratio at the exported minimising set recomputed from the exported q and maxima; the five factors multiply to lambda_gs / lambda_0")
    print("ALL DONE")
