# Coordinator's independent spot checks

Small scripts with which the Theoretical Research Division re-checked claims of others
before quoting them (the older ones need no numpy, the later ones need numpy and scipy; each
runs in seconds to a few minutes; not part of `scripts/audit_all.sh`).

| script | what it checks | quoted in |
|---|---|---|
| `k_spot_checks.py` | workstream K: the closed form of the first bounded-accuracy level `τ₂`; the necessary condition "never below `h`" at accuracy zero and for the two-rung bound; Lemma K.4(a),(b) (= Lemma 11.55) with exact binomial tables for `m ≤ 400`; the binomial-median fact | theory report §11.19 |
| `harper_fc_check.py` | Computational Research Division, ENG-RES-0006 §1: on the uniform cube the maximum of `W(C) = 2^{-n}Σ_y e^{u·dist(y,C)}` over all sets of a given size is attained by the initial segment of the simplicial order — brute force over all subsets, `n ≤ 4` | theory report §11.19 remark (2); THY-MSG-0005 |
| `siteset_check.py` | the pair-count profile of a diamond-lattice chain depends on its site set only (`h₃ = e₃ − (N−1)`, `h₈ = e₈ − (N−2)`, `h₁₁ = e₁₁`); profile-class counts `22, 37, 57, 90` for `n = 5 … 8` | THY-RES-0001 |
| `f_spot_checks.py` | workstream F: the closed form of the game function against a numerical game value; the hinted exponent at the zero residual in both forms; the uniform cube at `p = ½`; `R^max > R_0`; the max–min form of the non-adaptive exponent against the pair formula; type-wise quantiles are Lipschitz (brute force) | theory report §11.20 |
| `field_monotone_proof_check.py` | every step of the coordinator's proof that a field always helps (Proposition 11.65(b)) | theory report §11.20 |
| `r9_product_sampler_check.py` (output `out_r9_product_sampler_check.txt`) | referee R9, finding m4: the lower bound `max(φ₀, φ₁)` for samplers that are one product measure — the tilt identity behind it, the corrected table against `θ_na`, and the exact finite-`n` bound for plain Monte Carlo at `n = 2000` | theory report §11.20 (Theorem 11.61) |
| `s_lat.py` | own diamond-lattice helpers (walks, bridges, the profile from the definition, both norms) used by the checks of workstream S | — |
| `s_check1.py [NMAX] [DATA]` (`out_s_check1.txt`) | workstream S: the finite inequalities of Proposition 11.72(a), (b) and the surface bound of Proposition 11.73 on all profile classes — own enumeration up to 12 beads, the other division's tables up to 27 beads (identical where both exist) | theory report §11.22 |
| `s_check2.py` (`out_s_check2.txt`) | Lemma 11.68 with an own implementation: the copy of the second bridge is unique, the result is a bridge, the errors are in the proved intervals (48 058 concatenations) | §11.22 |
| `s_check3.py` (`out_s_check3.txt`) | the two cluster linear programmes re-formulated and re-solved: the values `b` of all rows, the polytopes `𝒦₁`, `𝒦₂` (vertices, volumes, support functions in 400 directions), the three gauche bounds, `γ_LP` at four points | §11.22 (Proposition 11.72) |
| `s_check4.py [DATA]` (`out_s_check4.txt`) | own lamella builder (valid bridges; densities → `(½,2,3/2;0)`, `(1,5,6;0)`); hairpins and the single-flip bound; the volume bounds of Theorem 11.71(c); own packings in `T₀` (52, 162, 7, 14); exact covering numbers at 15 and 21 beads with the cumulative and with the wrong weighted norm (8 against 10) | §11.22; D48 |
| `s_check5.py LP_EXACT_TXT` (`out_s_check5.txt`) | the eleven dual certificates of Proposition 11.72(b) in exact rational arithmetic with own code (multipliers read from `experiments/workstreams/S/out/lp_exact.txt`) | §11.22 |
| `s_check6.py S_CODE WITNESS W` (`out_s_check6.txt`) | the explicit bridge with 166 199 beads behind "`γ` is not identically zero": built by the workstream's builder, checked and counted with own code | §11.22 (Proposition 11.72(e)) |
| `s_check7.py` (`out_s_check7.txt`) | own exact dual certificates (integer multipliers) for the chain-marked cluster programme: the twelve rows of `𝒦₂` and the three lower bounds for the gauche density of Proposition 11.72(c) | §11.22 |
| `meanfield/` (own README) | exploration, not a result: type-level exponents for known parts that are functions of the type (Curie–Weiss), the pair identity with cone formulas, dip exponents from their definition, cones around shells | research log (entry after the seventh checkpoint of cycle 10); `docs/workstreams/T_brief.md` |
| `meanfield_T/` (own README) | workstream T (theory report §11.23): two independent inner solvers for the single-letter problem; the two-phase numbers (barrier shell, free blocks at four accuracies and three couplings), the junction with the uniform cube, the pair identity and its failure at `u = 0.30`, a one-phase case with a field, ferromagnets against the uniform cube, slices, the threshold `E` of the field case | theory report §11.23; `DEAD_ENDS.md` D49; THY-MSG-0009 |
| `rounds_U/` (own README) | workstream U (theory report §11.24): the two- and three-round upper bounds by direct minimisation; the asymptotic two-round lower bound `θ₂*`; the exact finite-`n` twins of Theorem 11.86 implemented from its statement | theory report §11.24; `DEAD_ENDS.md` D50 |

`DATA` is the directory of the other division's class tables
(`git archive origin/research/ubuntu-engineering experiments/eng/chain_cover/data | tar -x -C <dir>`,
then `<dir>/experiments/eng/chain_cover/data`); without it `s_check1.py` runs on the own
enumeration only and `s_check4.py` skips part (d).

Run: `python3 experiments/coordinator_checks/<script>` (the `s_check*.py` from inside the
directory, because they import `s_lat.py`)."
