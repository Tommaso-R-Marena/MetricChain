# Coordinator's checks for theory report §§11.28 and 11.29 (thirteenth checkpoint of cycle 10)

Exploration scripts behind the answers to SCI-REQ-0001, Q1 (robust ratios of macrostate
weights) and Q2 (a one-body marginal oracle with a field).  Run from this directory:
`python3 <script> > out_<script>.txt` (numpy, scipy; each under two minutes).  The harness
(`experiments/falsify_conjectures.py`, block XXIII and DEAD.26) contains reduced versions
with mutations; these scripts are the larger runs whose numbers the theory report quotes.

| script | what it checks | outcome (stored in `out_*.txt`) |
|---|---|---|
| `ratio_lib.py` | the three linear programmes (all constraints; constraints from `B` to `A` only; transport with gains) and the two extensions | library |
| `ratio_check1.py` | Theorem 11.105 on 300 random finite spaces with asymmetric envelopes: the three programmes agree; the closure of an optimal residual is optimal, a fixed point and admissible in all directions; weak duality against random admissible residuals; one state in closed form | all to `10⁻¹⁵` |
| `ratio_check2.py` | Theorem 11.106 on the cube: the programme on `Q_n` (`n = 5, 6, 7`) against the programme on types; the maximal field for separated macrostates; band macrostates against the exponential-scale formula for `n ≤ 800` (the linear programme only while `u·n ≤ 50`) | `4·10⁻¹⁵`; band, uniform measure, `u = 1`: exact `0.276673` at `n = 50` = best cone around a type class; limit `0.282287` |
| `ratio_check3.py` | Theorem 11.107 on 120 random product spaces of three sites: additive known parts exact; pairwise ones strictly between the marginal and the largest conditional single-site value in all 120 cases; and a first version of the three-letter example with thresholds off the lattice of types (kept as run; see D54 item 5) | as stated |
| `ratio_check4.py` | Theorem 11.108, three letters, thresholds `1.25` and `0.5` on the lattice: transport cost by the six vertices of the Lipschitz polytope against the transport programme; the bracket by cone and plan and the max–min on types for `n ≤ 144`; the continuum value on a grid of mesh `1/240` | continuum `0.41422`; `M_n/n − 0.41422 ≈ −0.27/n`; bracket ends above the limit by `0.33·ln n/n` and `0.75·ln n/n` |
| `oracle_field_scan.py` | Proposition 11.109(c) on `Q_10`, `p = ¼`, `u = 1`: sensitivity, null type, mismatch and excess type along the additive instances `γ|x|` for two families of cyclically symmetrised balls | family (type 5, radius 1): no sign change — the mismatch is zero at both ends and positive between; family (type 3, radius 2): sign change near `γ = −0.02` |
| `oracle_zero_types.py` | Proposition 11.109(e): the dip exponent of the zero residual with a field restricted to two-block profiles of a given type, `ρ_e(κ)`, on a coarse grid with a Nelder–Mead polish (`p = ¼`, `u = 1`, `e = 0.02`; about 15 minutes; an earlier, finer version ran into its time limit) | `ρ_e = 0, 0.0049, 0.0121, 0.0129, 0.0134, 0.0094, 0.0034, 0` at the types `0.129, 0.184, 0.238, 0.250 = p, 0.292, 0.347, 0.401, 0.455`: unimodal, best type `≈ 0.29`, and `ρ_e(p)` is `0.965` of the maximum |
