# Coordinator's independent spot checks

Small scripts with which the Theoretical Research Division re-checked claims of others
before quoting them (numpy not needed; each runs in seconds to a few minutes; not part of
`scripts/audit_all.sh`).

| script | what it checks | quoted in |
|---|---|---|
| `k_spot_checks.py` | workstream K: the closed form of the first bounded-accuracy level `τ₂`; the necessary condition "never below `h`" at accuracy zero and for the two-rung bound; Lemma K.4(a),(b) (= Lemma 11.55) with exact binomial tables for `m ≤ 400`; the binomial-median fact | theory report §11.19 |
| `harper_fc_check.py` | Computational Research Division, ENG-RES-0006 §1: on the uniform cube the maximum of `W(C) = 2^{-n}Σ_y e^{u·dist(y,C)}` over all sets of a given size is attained by the initial segment of the simplicial order — brute force over all subsets, `n ≤ 4` | theory report §11.19 remark (2); THY-MSG-0005 |
| `siteset_check.py` | the pair-count profile of a diamond-lattice chain depends on its site set only (`h₃ = e₃ − (N−1)`, `h₈ = e₈ − (N−2)`, `h₁₁ = e₁₁`); profile-class counts `22, 37, 57, 90` for `n = 5 … 8` | THY-RES-0001 |

Run: `python3 experiments/coordinator_checks/<script>`.
