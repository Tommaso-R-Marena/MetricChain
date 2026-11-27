## 6. Requests (can be sent as they stand; none is an authorisation to spend anything)

### To the coordinator's pipeline / the engineering division

**P9-E1 (re-run the resolved certificates with another driver).**  *Motivation.*  §4: with the
state-resolved tables the certified brackets fall by one to two orders of magnitude, and an
order earlier than before; the runs were made by the author of the tables with a driver of the
same author (`ws_P9/p9_05_brackets.py`, which only imports the pipeline's modules and reproduces the
coordinator's reference brackets digit for digit).  *Formulation.*  The coordinator's own driver
(`pi_inference/occ_reduction_test.py`) with zero penalties plus P6's allowances, and the tables
read from `ws_P9/out/tables_<tag>_m<m>_w7.npz`: arrays `s2_S1_<i>` (site sums), `s2_S2_<i>_<j>`
(pair sums), `s2_S3_<i>_<j>_<l>` (triple sums; the forms S, B, T are `p9lib.form_tables`: divide by
`m`, `C(m,2)`, `C(m,3)` and reduce what does not fit the band), `s2_W_<sites>` (window form: add as
they are — one site to `one[i]`, two sites with `add_pair`, more with `add_multi`); every entry
times `1 + 10⁻⁹`; `∓` in floor and ceiling.  *Hypothesis used:* `|g − I_{m−1}g|(x) ≤ pen(x)` pointwise —
Theorem R and Proposition P of §1 (paper proofs; §2, §3.4 for the checks).  *Validation.*  Lys₅
with `--enum`: every state, exact `ln Z` inside (§4.4).  *Stopping condition.*  My brackets
reproduced to the digits printed, or a difference found and explained.  *Resources.*  As the
reference runs (in my logs: 1.9–2.4 GB, 18–94 s per row at band 7, floor samples included).

**P9-E2 (an independent implementation of the bound with the actual increments).**
*Motivation.*  The constants were computed by P8 alone, the resolved tables by me alone, in one
code path (`p9lib.Resolver`; P8's `_stack`, `_M` for the suprema).  *Formulation.*  For a subset `T`,
a state `x_T` of non-anchor rotamers and every block: P3's Theorem 3 at host states
`c_l ∈ {x⁰_l, x_l}` (`l ∈ T`), `c_l = x⁰_l` (`l ∉ T`), with `δ^{p,c}_i = |C^{p,c}_i(x_i) − C^{p,c}_i(x⁰_i)| + 2·10⁻¹⁰`
for the non-host sites `i ∈ T` (`C` = `GBModel.A[i]` for fixed atoms, `GBModel.T[(l,i)][c]` for the atoms
of side chain `l`); sum over set partitions as in P3's Proposition 4 restricted to `T`.
*Validation data.*  `p9_01_validate.py` prints, for Lys₄, Lys₅, LKSE:5, the exact block remainders
at every state; `p9_00b_consistency.py` the two code-path identities (maxima reproduce P8's
block constants; maximal increments reproduce stage 1).  *Stopping condition.*  `Θ²_T(x_T)` of all
subsets of Lys₄ and of a sample at twelve residues reproduced to `10⁻¹²` relative.

**P9-E3 (the reductions are the bracket now).**  With the window form of stage 2 the certified
bracket of Lys₁₂ is the width of the penalty-free models to within a few per cent at orders 4
and 5 (§4): the ten pairs of side chains beyond the band and the evaluated terms that do not
fit a window.  The coordinator's own list (addendum A17 (18), item 64 (iv)) has the candidates —
the first-order-optimal split of a far pair as a transport problem; a wider band — and they
now decide the result.  *Stopping condition.*  The penalty-free width of Lys₁₂ at band 7
(`0.00713` nats) halved, or a reason why it cannot be.

**P9-E4 (longer chains: which subsets to resolve).**  The resolved bound has no closed form over
the subsets (as P8's): 0.15–0.6 s per subset at twelve residues, order 4–5, on one core; at
twenty residues and order 4 there are 4 845 subsets (of the order of an hour by
extrapolation; not measured), at order 5 15 504.  A valid
hybrid: resolve the subsets inside a window, keep P8's closed form 'AH' for the rest (every
subset keeps a valid bound; Proposition P does not care where `Φ_T` comes from).  Not run.

**P9-E5 (the nested sampler with the resolved envelope).**  `ws_P9/p9_07_nested.py` plugs the
envelope `Σ_{T⊆S(x)} Θ²_T(x_T)` (stored tables) and the outer sandwich of the window form into the
coordinator's `nested_sampler.main()` unchanged.  Status and numbers: §5.4.  *Request:* a run by
the coordinator with its own driver; and a sampler that does not pay `1/(1 − e^{−D})` draws per
proposal when the outer bracket `D` is already small (with `D = 0.017` 98 % of the exact draws of
the floor are thrown away) — e.g. proposing from the difference model directly.

### To the theory division

**P9-T1 (Proposition P as a machine-checked statement).**  *Statement.*  Finite product `X`,
anchor `x⁰`, `Φ_T : X*_T → [0, ∞)` for `|T| = m`; weights `w_{T,U} ≥ 0` on the non-empty `U ⊆ T`, summing
to one; `c_{T,U}(b_U) = max{Φ_T(y_T) : y_U = b_U}`, `γ_U = Σ_{T⊇U} w_{T,U} c_{T,U}`, extended by zero.
Then `Σ_{T⊆S(x)} Φ_T(x_T) ≤ Σ_U γ_U(x_U)` for all `x`; and the reduction step (b) of §1.  With `Φ_T`
constant this is your Proposition 11.18f (allocations) at all levels.  *Use.*  Every bracket
of §4.  *Stopping condition.*  A Lean statement next to `higherOrder_remainder`, or a
counterexample.

**P9-T2 (when does a floor delocalise — before the model is built?).**  *Observation* (§4):
for Lys₁₂ at order 4 the window form with P8's constants has a first-order number of 0.012
nats and a certified bracket of 0.72 (its floor has 6.6 of 12 side chains off the anchor);
with constants 47 % smaller (the joint maxima of stage 2), or with the stage-1 tables, the
bracket is 0.010 and the floor sits at the anchor; one order further down ((LKSE)₃ at order
4, Lys₁₂ at order 3) the same happens between stage 1 (more than a hundred nats) and stage 2
(0.019 and 0.077).  First-order numbers on a sample of the true ensemble
cannot see this (Lemma A17.16 says so); the coordinator's item 54 gives a criterion at the
site level ("`βΓ_m` fits under the depths").  *Question.*  A computable upper bound of
`ln Z(m₋) − ln Z(B)` for window tables — second order in the tables, or a comparison with an
auxiliary solvable model — that decides, before the transfer matrix is run, whether a given
set of tables is below the threshold; and the allocation that minimises it.  *Validation
case.*  The two table sets above (`ws_P9/out/tables_K12_H_0.70_m4_w7.npz`; `p9lib.window_form_const`
with P8's constants and with the joint maxima of stage 2).

**P9-T3 (the remainder identity with a term-dependent order, before the maximum).**  P8-T1
with one sentence added: in `F − I_{m−1}F = Σ_τ Σ_{T⊆S(x)} Δ_T F_τ(z^{T,x,τ}; x_T)` the mixed difference of
`T` is between `x⁰_T` and the *actual* `x_T`, so any bound of it may be a function of `x_T`; Theorem
R is this identity plus P3's Theorem 3 with the actual increments.
