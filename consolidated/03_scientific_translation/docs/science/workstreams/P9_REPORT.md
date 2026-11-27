# Workstream P9 (science division) — penalties resolved by rotamer state: what the resolution gains for the charged case

Report of an independent workstream of the Scientific Discovery, Translation & Independent
Validation Division.  Branch `research/scientific-translation`.  Everything is in
`experiments/science/ws_P9/` (running notes with the predictions, the dead ends and my own errors:
`NOTES.md`; logs: `logs/`; results: `out/`; logs that are not cited: `not_cited/`).  Written
2026-11-26.  **A draft of one workstream: nothing here has been refereed or machine-checked, no
run by anyone else is part of it, and it is not a statement of the division until the
coordinator has verified it.**  (The coordinator began a verification of its own in
`experiments/science/p9_verification/` while this was being written; I looked at four of its logs
at 12:17, read-only, and cite none of them.)

Labels: **[P]** proved here on paper (I say how it was checked); **[X]** exact enumeration of all
states of the named instance; **[M]** measured on the named model by the named script; **[K]** known
and cited with the reading level; **[H]** hypothesis or reading.  Units: kcal/mol;
`k_BT = 0.596161 kcal/mol` (300 K); brackets of `ln Z` in nats.  Every statement is
**model-relative**: it is about the finite function defined by OpenMM 8.6.1's GBn2 expression on
workstream P2's rigid synthetic peptides (Ace-X_n-NMe, ideal α-helix, three-state grid per
side-chain dihedral, P2's pruned product domain — for lysine and the patterned sequence a
greedily pruned sub-product of the clash-free domain), exactly as workstreams P3, P5, P6, P8 and
the coordinator's pipeline set it up.  No sequence was varied, designed or optimised; nothing
here bears on a real peptide in water.

*What is whose.*  The term-by-term bound and its ingredients: workstream P3.  The state-wise
evaluation per subset, the blocks, Theorem AH and the code that computes the per-host-state
block bounds: workstream P8 (`ws_P8/p8sr.py`; used unchanged, its arrays recorded before its
maximisation).  The share forms S, B, T with state-independent constants: P3 and P6.  The
window models, the occupancy-aware reductions, the split of the far pairs around the anchor,
the Gibbs sampler, the nested-sampler driver: the coordinator (`pi_inference/`).  The idea of
keeping the dependence on the state: P8's request P8-E4 and the coordinator's brief.  Charging
a subset to a sub-tuple of its sites: the theory division's Proposition 11.18f — as described
in P8_REPORT §4.1 and in addendum A17 (17), items 52–53; I did not read the theory division's
own text — estimated to first order by P8.  **Mine:** Theorem R and Proposition P as written out in §1 (both short),
the evaluation with the actual increments ("stage 2"), the tables, their validation, the
runs.

*What I read, and how much of it* (everything else is not relied on).  **[full text]**: the
brief; `COMMON.md`; `P8_REPORT.md` §0, the end of §3.2, §3.3, §3.4, §3.5, §4.1, §5, §7 and the
coordinator's note; `P3_REPORT.md` §2.1–§2.4 (Proposition 1, Lemma 2, Corollaries L1, L2, Remark
L3, Theorem 3, Proposition 4) and the start of §2.5; `INFERENCE_LIMITS_ADDENDA.md` part A17 (18)
(items 58–64) and part A17 (17), items 52–57.  **[code, read in full]**: `ws_P8/p8sr.py`, `p8lib.py`,
`p8_03c_blockcheck.py`, `p8_04b_gamma12_blocks.py`; `ws_P6/p6lib.py`; `ws_P3/pwmodel.py`, `gfbound.py`;
`pi_inference/window_model.py`, `window_model_occ.py`, `occ_reduction_test.py`,
`nested_sampler_ext.py`; `p8_verification/lys_enum_check.py`, `lys12_rerun.py`.  **[code, in part]**:
`pi_inference/nested_sampler.py` (docstring, `Envelope`, `inner_bounds`, `draw_q`, `main`);
`ws_P3/encl.py` (lines 195–300), `p3core.py` (header, `GBModel.__init__`, the evaluators),
`ws_P6/p6_09_triple.py` (first 100 lines).  **[one line]**: `ws_P5/s2_family.py`, `ws_P3/termwise.py`
(the lines found by a search for the increments).  **Literature outside the programme: not
searched.**

---

## 0. Verdict in ten lines

Certified width of the bracket of `ln Z` in nats, helix, band 7, the coordinator's models; "→" reads: P8's state-independent constants → host rotamers resolved (stage 1, the brief's first stage) → all sites of `T` resolved (stage 2).

1. **Lys₁₂, order 5**, triple form (the reference's own form): **0.05669 → 0.0452 → 0.016**; window form of stage 2: **0.007233**, `[517.125705, 517.132938]`.
2. **Lys₁₂, order 4**, triple form: **1.413 → 0.3493 → 0.1115**; window form: **0.007347**, `[517.125649, 517.132996]` — from 96 366 evaluations, tighter than the reference at order 5.
3. **(LKSE)₃, order 5**, triple form: **4.301 → 1.871 → 0.1946**; window form: **0.01699**, `[655.604050, 655.621038]` — deterministic, and inside the coordinator's sampled interval.
4. What is left is the band itself: the penalty-free widths are 0.007133, 0.007132, 0.0167; the window-form brackets are these plus one to three per cent.
5. The host rotamers alone are a weak dependence (site penalty 0.72–1.00 of the constant one at the visited rotamers); resolving the non-host sites too is the lever (typical subset bound 42–590 times below P8's constant).
6. One order earlier: (LKSE)₃ from its order-4 ball **0.0191**; Lys₁₂ from its order-3 ball **0.07686**; (LKSE)₃ at order 3: **no certificate** (658.9 nats, the floor delocalises).
7. Proved [P]: Theorem R (the remainder bound with all sites of `T` at their actual states), Corollary J (smaller state-independent constants), Proposition P (tables by maxima over the other sites), Corollary S (the sandwich).
8. Validated [X] at every state of Lys₄, Lys₅, LKSE:5: 18 181 488 block comparisons, 844 392 whole-function checks, 13 510 272 table checks, 87 enumerated sandwiches, no violation; the deliberately wrong tables fail.
9. Predictions written before the models: within 3–8 % in the first-order cases; about whether a floor delocalises, wrong five times of nine.
10. Stretch: the resolved envelope in the coordinator's nested sampler gives (LKSE)₃ within 0.00017 nats at probability 0.95 with 90 new evaluations.  **A draft: nothing refereed or machine-checked, stage 2 in one implementation, no run by anyone else cited.**

### 0.1 The same ten points, each with what stands behind it

1. **The first stage of the brief — the rotamers of the *host* side chains alone — is a weak
   dependence, and I can say why** [M, §3.1]: over the rotamers the ensemble visits, the resolved
   site penalty is 0.72–1.00 of the state-independent one; the anchor half of P3's host step,
   the blocks without a host in `T` and the *maximal* increments of the non-host sites do not
   move.  In certified nats (the reference's own form: triples, band 7, split around the
   anchor) it is still worth 0.05669 → 0.0452 for Lys₁₂ at order 5, and — because
   the reference floors were delocalised — 1.413 → 0.3493 at order 4 and
   4.301 → 1.871 for (LKSE)₃.
2. **The second stage is the lever** [P, §1; M]: with the non-host sites at their actual
   rotamers too — P3's theorem with the increments it is *stated* with; the maxima were only in
   the computable forms — the typical bound of a subset is 42–590 times below P8's constant
   in the three cases of the brief, and even its maximum over the states is 41–61 % of it
   (`βΓ = 18.2, 0.99, 26.1` where P8 has `34.0, 2.40, 42.8`: new *state-independent* constants).  The three brackets, like for like:
   **0.016** (was 0.0567), **0.1115** (was 1.4125), **0.1946** (was 4.30) nats.
3. **With every subset charged to one sub-tuple of its sites that fits a window** (an
   allocation in the sense of the theory division's Proposition 11.18f, here with
   state-resolved tables) the brackets are **0.007233, 0.007347, 0.01699 nats** —
   the penalty-free widths (0.007133, 0.007132, 0.0167) plus one to three per cent:
   factors 7.8, 192 and 253 against the three
   numbers of the brief.  The allocation alone, with P8's constants, gives 0.007286,
   0.7207 and 1.311: where the constants are large its floor delocalises.
4. **One order earlier.**  Lys₁₂ is certified from the order-4 ball (96 366 evaluations) within
   0.007347 nats, `[517.125649, 517.132996]` — 7.7 times tighter than the
   reference at order 5 (1 621 056 evaluations).  **(LKSE)₃ — "reachable by sampling and not
   deterministically" — is certified deterministically**: `[655.604050, 655.621038]` at order 5,
   inside the coordinator's sampled interval; and from its order-4 ball (181 268
   evaluations, where nobody had tried) within **0.0191 nats**, `[655.603013, 655.622116]`.
   At order 3: Lys₁₂ is still certified from its order-3 ball (3 841 evaluations) within 0.07686 nats, `[517.108870, 517.185731]`; (LKSE)₃ is not (658.9 nats: its floor delocalises completely).
5. **Statements** [P, §1]: Theorem R — `|g − I_{m−1}g|(x) ≤ Σ_{T⊆S(x)} Θ_T(x_T)`, block by block, with
   the hosts *and* the non-host sites of `T` at their actual states (P8's Theorem AH before its
   maximum; P3's Theorem 3 with actual increments); Proposition P — any allocation of
   `Θ_T(x_T)` to tables on sub-tuples by maxima over the *other* sites is a valid penalty, the
   state-dependent form of P3's site shares and P6's Lemmas A, A′.
6. **Validated by enumeration** [X, §2] on Lys₄, Lys₅, LKSE:5, every order, every state:
   18 181 488 block-level comparisons, 844 392 whole-function checks, 13 510 272 table checks,
   no violation; the resolved bound is attained within 0.3 %.  **Controls that fail as
   intended:** the minimum over the rotamers in place of the value, and the value at a wrong
   rotamer, fail at block level in every row and against every table form; against the
   whole function they fail only for stage 2 — for stage 1 that check has no power.
   Brackets on Lys₅ and LKSE:5: every sandwich at every state, exact `ln Z` inside.
7. **At twelve residues** [M, §3.4]: the resolved bound was checked at *every* state with
   exactly four side chains off the anchor (1 524 690 states of Lys₁₂, 3 290 515 of (LKSE)₃),
   at 20 000 random states with exactly five, and at 2 000–2 500 uniformly random states per
   case: no violation, both controls fail; my driver reproduces the coordinator's reference
   brackets digit for digit; the coordinator's sampled intervals are consistent with every
   bracket.
8. **Predictions** (written before the models, §4.1): within 3–8 % in the first-order cases
   (Lys₁₂ order 5, Ser₁₂), 20–40 % too high for the stage-2 rows in the equal-share forms elsewhere; about the floor
   itself wrong five times of nine — three times too pessimistic, twice too optimistic (by
   factors 36 and 9).
9. **Stretch** [M, §5.4]: with the resolved envelope and the window-form sandwich in the coordinator's nested sampler, the envelope's own bracket for (LKSE)₃ falls from 1.23 nats to 3.48e-06, and at probability 0.95 `ln Z` is known within **0.00017 nats as the theory division states the bound** (`[655.612610, 655.612778]`; 4.3e-05 in the two-end form with empirical Bernstein) from 400 000 proposals and 90 new evaluations — the coordinator's run with P8's constants: 0.188 and 0.041 in the same two forms, from 4 000 000 proposals and 12 000 evaluations.  From the order-4 ball alone: 0.00025 nats with 1200 evaluations.  One run per case, one seed; the Lys₁₂ run from the order-3 ball was not made (memory).
10. **Limits.**  A draft: no proof refereed or machine-checked, one implementation of the
    stage-2 evaluation, no run by anyone else is cited; P3's enclosures inherited; and the
    brackets are now the *reductions* of the band (ten far pairs), which I did not touch.

---

## 1. The statements, with proofs

**Setting (workstream P3's and P8's notation; nothing is changed).**  `X = ∏_i X_i`, anchor `x⁰`,
`S(x) = {i : x_i ≠ x⁰_i}`, `X*_U := ∏_{i∈U} (X_i ∖ {x⁰_i})` for a set `U` of sites.  `g = Σ_τ τ` is the sum
of the self terms `t_pp` and pair terms `t_pq` of the solvent energy; `𝓗(τ)` is the set of hosts
of `τ` (0, 1 or 2 sites); a *block* `𝔅` is a set of terms with a common host set `𝓗` (P8's
blocks: self terms of side chain `l`; pairs "fixed atom – `l`" and pairs inside `l`; pairs
between `l` and `l′`; and the two blocks without a host).  `I_{m−1}` is the anchored interpolant
of order `m − 1`.  For an atom `p` and a state `c` of its host, P3's per-state data
(`gfbound.GFBound.per_state`) are: the hull `[I⁻, I⁺]_{p,c}` of `I_p` over **all** states of the
other sites, the derivative suprema `Bd^{p,c}_k`, `L^{p,c}_k` over that hull, the range of `ℓ_p`,
and for two atoms in host states `c = (b, b′)` the kernel suprema `H^c_k` at the distance `r_pq`
of those states.  On `{x_{l(p)} = c}`, `I_p = const + Σ_{i≠l(p)} C^{p,c}_i(x_i)` (P3's structural
fact).  The **increment** of site `i` for atom `p` is

```
δ^{p,c}_i(y) := |C^{p,c}_i(y) − C^{p,c}_i(x⁰_i)|  (+ P3's table allowance),      δ̄^{p,c}_i := max_{y∈X_i} δ^{p,c}_i(y)   (P3's δ^{p,c}_i).
```

For a host-state assignment `c` on `𝓗(τ)`, a non-empty set `B` of sites with `B ∩ 𝓗(τ) = ∅`
and `y_B ∈ X_B`:

```
Θ_c(τ; B; y_B) := (κ/2) q_p² · Bd^{p,c}_{|B|} · ∏_{i∈B} δ^{p,c}_i(y_i)                                                            (τ = t_pp),
Θ_c(τ; B; y_B) := κ|q_p q_q| Σ_{π∈Part(B)} H^c_{|π|} ∏_{β∈π} ( L^{p,c}_{|β|} ∏_{i∈β} δ^{p,c}_i(y_i) + L^{q,c}_{|β|} ∏_{i∈β} δ^{q,c}_i(y_i) )     (τ = t_pq),
```

and `Θ̄_c(τ; B)` the same with every `δ(y_i)` replaced by `δ̄` — P8's `Θ_c(τ; B)`, which does not
depend on `y_B`.  `Θ_c ≤ Θ̄_c` (every ingredient is non-negative and `Θ` is non-decreasing in each).

### Lemma T′ [K: P3's Theorem 3 for one term, as P3's proof gives it — with the increments P3's Corollary L2 is stated with]

*Let `τ` be a term, `T ⊆ [n]` with `B := T ∖ 𝓗(τ) ≠ ∅`, `z ∈ X` with `z_T = x⁰_T`, `y_T ∈ X_T`, and
`𝒞(T; z, y)` the set of assignments `c` with `c_l = z_l` for `l ∈ 𝓗(τ) ∖ T` and `c_l ∈ {x⁰_l, y_l}` for
`l ∈ 𝓗(τ) ∩ T`.  Then*

```
|Δ_T τ(z; y_T)|  ≤  Σ_{c ∈ 𝒞(T; z, y)}  Θ_c(τ; B; y_B)   ≤   Σ_{c ∈ 𝒞(T; z, y)}  Θ̄_c(τ; B).
```

*Proof.*  P8's Lemma T, read with the increments that occur.  For a host `l ∈ T`,
`Δ_T F(z; y_T) = Δ_{T∖l} F|_{x_l=y_l} − Δ_{T∖l} F|_{x_l=x⁰_l}` (P3's Remark L3); applied to every host in
`T` this writes `Δ_T τ(z; y_T)` as a signed sum over `c ∈ 𝒞(T; z, y)` of `Δ_B τ_c(z; y_B)`, `τ_c` being
`τ` with its hosts held at `c`.  For fixed `c`, `r_pq` is constant and `I_p`, `I_q` are constants
plus sums of one-site functions `C^{p,c}_i`, `C^{q,c}_i` of the sites of `B`, with all values in the
hulls of the states `c` **whatever the other sites do**.  The mixed difference `Δ_B` from `z_B =
x⁰_B` to `y_B` involves each site `i ∈ B` in exactly two states, `x⁰_i` and `y_i`.  P3's Corollary L1
(`|Δ_B φ(u)| ≤ sup|φ^{(|B|)}| ∏_{i∈B} |a_i(y_i) − a_i(z_i)|` for `u = c + Σ_i a_i(x_i)`) gives the self
term with `a_i = C^{p,c}_i`; P3's Corollary L2 gives the pair term, and it is *stated* with
`δ^p_i := |C^p_i(y_i) − C^p_i(z_i)|` ("the change of the contribution of site `i` to `I_p`", P3_REPORT
§2.2): `D_β(ℓ_p) ≤ L^p_{|β|} ∏_{i∈β} δ^p_i` at every vertex, because the increment of an additive
function does not depend on the vertex.  The second inequality is monotonicity.  ∎

*What is whose.*  Nothing in Lemma T′ is new mathematics: P3's theorem is a statement with the
actual increments; P3's computable forms (`gfbound`, `termwise`) and P8's (`p8sr`) take `δ̄`.  I
re-derived L1, L2, L3 from P3_REPORT §2.2 (one page) and did not find an evaluation with the
actual increments in P3, P5, P6 or P8 (searched: `ws_P3/gfbound.py` line 110 and `termwise.py`
line 128 take `…max(axis=0)` over the states of the non-host site; `ws_P8/p8sr.py`, `p8lib.py` and
P6's `p6lib.py` use that array; P8's exploration `x01_ff_proto.py` likewise; P5's `s2_family.py`
uses single increments only for two-state sites, where they coincide).

### Theorem R (the remainder bound, resolved by state) [P; checked at every state, block by block, §2]

*For `|T| = m ≥ 3`, a block `𝔅` with host set `𝓗`, and `y_T ∈ X*_T` define*

```
Θ²_{𝔅,T}(y_T) := Σ_{c ∈ 𝒞_y(T)} Σ_{τ∈𝔅} Θ_c(τ; T∖𝓗; y_{T∖𝓗}),          Θ¹_{𝔅,T}(y_T) := Σ_{c ∈ 𝒞_y(T)} Σ_{τ∈𝔅} Θ̄_c(τ; T∖𝓗),
𝒞_y(T) := { c :  c_l = x⁰_l  (l ∈ 𝓗 ∖ T),   c_l ∈ {x⁰_l, y_l}  (l ∈ 𝓗 ∩ T) },          Θ^s_T := Σ_𝔅 Θ^s_{𝔅,T}     (s = 1, 2).
```

*(`Θ¹` depends on `y_T` through the states of the hosts of the block that lie in `T`; `Θ²` through all
of `y_T`.)  Then for every `x ∈ X`, every `m ≥ 3`, every block and `s = 1, 2`*

```
Σ_{τ∈𝔅} |τ(x) − I_{m−1}τ(x)|  ≤  Σ_{T ⊆ S(x), |T| = m} Θ²_{𝔅,T}(x_T)  ≤  Σ_{T ⊆ S(x), |T| = m} Θ¹_{𝔅,T}(x_T),
hence      |g(x) − I_{m−1}g(x)|  ≤  Σ_{T ⊆ S(x), |T| = m} Θ^s_T(x_T).                                                   (R)
```

*Proof.*  Steps (a) and (b) of P8's Theorem AH, word for word; step (c), the maximum, is not
taken.  (a) P3's remainder identity holds for every total order `≺` of the sites:
`F(x) − I_{m−1}F(x) = Σ_{T ⊆ S(x), |T| = m} Δ_T F(z^{T,x}; x_T)`, `z^{T,x}_i = x_i` if `i ≺ min_≺ T` and `x⁰_i`
otherwise; `I_{m−1}` does not depend on the order and is linear.  (b) For a term `τ` take an order
with the hosts of `τ` last.  For `T ⊆ S(x)` and a host `l ∉ T`: `T` has at least `m − 1 ≥ 2` elements
outside `𝓗(τ)`, all before `l`, so `z^{T,x}_l = x⁰_l`; and `z^{T,x}_i = x⁰_i` for `i ∈ T`.  Lemma T′ with
`z = z^{T,x}` and **`y_T = x_T`** gives `𝒞(T; z, y) = 𝒞_x(T)` and
`|Δ_T τ(z^{T,x}; x_T)| ≤ Σ_{c∈𝒞_x(T)} Θ_c(τ; T∖𝓗; x_{T∖𝓗})`.  Sum over `T ⊆ S(x)`, over the terms of the block
(same hosts, same order, same `𝒞_x(T)`), and over the blocks (`g = Σ τ`, `I_{m−1}g = Σ I_{m−1}τ`).  ∎

*Why the bound of `T` may depend on `x_T` at all.*  In the identity of step (a) the term of `T` is
a mixed difference **between `x⁰_T` and `x_T`**: each site of `T` occurs in its anchor state and in
its *actual* state, in no other.  The sites outside `T` occur only through the context `z^{T,x}`,
and every ingredient is a supremum over all contexts.  P8's constant is the maximum over `y_T` of
(a block-wise majorant of) `Θ¹_T(y_T)`; nothing forces that maximum.

**Corollary J (state-independent constants) [P].**  `ĉ^{J,s}_T := max_{y_T ∈ X*_T} Θ^s_T(y_T)` satisfies the
hypothesis of the pipeline, `|g − I_{m−1}g|(x) ≤ Σ_{T⊆S(x)} ĉ^{J,s}_T`, and
`ĉ^{J,2}_T ≤ ĉ^{J,1}_T ≤ ĉ^{SAb}_T` (P8's constant is the sum over the blocks of the block-wise maxima
of `Θ¹_{𝔅,T}`; a maximum of a sum is at most the sum of the maxima).

### Proposition P (tables) [P; elementary — the generalisation of P3's site form and P6's Lemmas A, A′ to state-dependent shares]

*Let `Φ_T : X*_T → [0, ∞)`, `|T| = m`, satisfy `|g − I_{m−1}g|(x) ≤ Σ_{T ⊆ S(x)} Φ_T(x_T)` for all `x`
(Theorem R: `Φ = Θ¹` or `Θ²`).*

*(a) Allocation.  For every `T` let `w_{T,U} ≥ 0`, `∅ ≠ U ⊆ T`, with `Σ_U w_{T,U} = 1`.  Put*

```
c_{T,U}(b_U) := max{ Φ_T(y_T) : y_T ∈ X*_T, y_U = b_U }      (b_U ∈ X*_U),
γ_U(b_U) := Σ_{T ⊇ U} w_{T,U} c_{T,U}(b_U)   for b_U ∈ X*_U,        γ_U(b_U) := 0   if some b_i = x⁰_i.
```

*Then `Σ_{T ⊆ S(x)} Φ_T(x_T) ≤ Σ_U γ_U(x_U)` for every `x`.*

*(b) Reduction.  Let `γ : X_U → [0, ∞)` vanish unless all sites of `U` are off the anchor, and
`λ_V ≥ 0`, `∅ ≠ V ⊊ U`, `Σ_V λ_V = 1`.  With `γ^{→V}(b_V) := max{ γ(b_V, y_{U∖V}) : y_{U∖V} ∈ X*_{U∖V} }` for
`b_V ∈ X*_V` and `0` otherwise:  `γ(x_U) ≤ Σ_V λ_V γ^{→V}(x_V)` for every `x`.*

*Proof.*  (a) Let `T ⊆ S(x)`.  Then `x_T ∈ X*_T`, **and for every `U ⊆ T` the actual `x_T` is one of
the points over which the maximum `c_{T,U}(x_U)` is taken, because the coordinates of `U` are held
at their actual values**; so `Φ_T(x_T) ≤ c_{T,U}(x_U)` for each `U`, and with the weights
`Φ_T(x_T) ≤ Σ_{U⊆T} w_{T,U} c_{T,U}(x_U)`.  Summing over `T ⊆ S(x)` and exchanging the sums,
`Σ_{U ⊆ S(x)} Σ_{T : U ⊆ T ⊆ S(x)} w_{T,U} c_{T,U}(x_U) ≤ Σ_{U ⊆ S(x)} γ_U(x_U) = Σ_U γ_U(x_U)`: the inequality
adds the non-negative terms of the `T ⊄ S(x)`, the equality uses `γ_U(x_U) = 0` for `U ⊄ S(x)`.
(b) If `U ⊄ S(x)` the left side is `0`.  Otherwise `x_{U∖V} ∈ X*_{U∖V}` is admissible in every maximum.  ∎

*The one line the brief asks for.*  A table `γ_i(x_i)` is a valid penalty for a set `T ∋ i`
because `c_{T,i}(x_i)` is a maximum over the states of the **other** sites of `T` at the actual
state of `i`, and the actual state `x_T` is among them; a state-independent constant is the
same maximum taken over `x_i` as well.

*What each table maximises over.*  `c_{T,U}(b_U)`: over the non-anchor states of the sites of
`T ∖ U`.  Inside `Φ_T` itself: stage 1 — the increments of every site of `T` *as a non-host site*
are maximal over all its states, including the sites of `U` (a site of `U` is resolved only as
a host); stage 2 — nothing; both stages — hosts outside `T` at the anchor (Theorem AH), all
derivative suprema and hulls over all contexts.

*The forms used below* (each is (a), followed by (b) where a tuple does not fit the band).
`w` is the band; "in band": `|i − j| ≤ w`; "in window": `max − min ≤ w`.

| form | (a): tuples and weights | (b): what does not fit |
|---|---|---|
| **S** site | `U = {i}`, `w_{T,i} = 1/m`: `γ_i(b) = (1/m) Σ_{T∋i} c_{T,i}(b)` | — |
| **B** banded pair | all pairs of `T`, weight `1/C(m,2)` | a pair beyond the band: one half of `max_{b_j} γ_ij(·, b_j)` to site `i`, one half of `max_{b_i} γ_ij(b_i, ·)` to site `j` |
| **T** banded triple | all triples of `T`, weight `1/C(m,3)` | a triple outside the window: one third of its maximum over each of its sites to the pair of the two others; then the pairs as in B |
| **W** window | one tuple per `T`, weight 1: `T` itself if it fits a window, else one maximal sub-tuple of `T` that fits | — |

With `Φ_T ≡ ĉ_T` forms S, B, T are P3's site form and P6's Lemmas A and A′ (their proofs are
the case of constant tables), and W is an allocation in the sense of the theory division's
Proposition 11.18f (any sub-tuple of `T` may be charged: `[T ⊆ S(x)] ≤ ∏_{i∈K}[x_i ≠ x⁰_i]`), which
workstream P8 estimated to first order ("least-occupied in-window sub-tuple", its §4.1) and
which, by the reports I read (P8 §4.1; addendum A17 (17)–(18)), had not been run as a bracket;
the choice of the sub-tuple is guided by an uncertified Gibbs sample and does not affect
validity.  In B and T the reduction (b) is applied to the *summed*
table `γ_U`, which is at least as tight as applying it subset by subset (a maximum of a sum is
at most the sum of the maxima); with constant tables the two coincide.

**Corollary S (the sandwich) [P].**  If `pen(x) := Σ_U γ_U(x_U)` is built by Proposition P from a `Φ`
of Theorem R, then `|g − I_{m−1}g|(x) ≤ pen(x)` pointwise, so the coordinator's window models with
`∓(pen + P6's floating-point allowances)` in place of `∓(state-independent penalties + allowances)`
satisfy `m₋ ≤ E ≤ m₊` on all of `X`: their validity argument (P3's Theorem 5; `window_model.py`,
docstring) uses the penalty only through that pointwise inequality.  Every table entry is
multiplied by P3's factor `1 + 10⁻⁹`: an entry is a sum of at most `C(n, m)` maxima of values of
`Φ_T`, each of them a sum of non-negative doubles that P8's code has already rounded up by the
same factor; the relative rounding error of such sums is orders of magnitude below `10⁻⁹`.

## 2. Validation by enumeration — before anything was computed at twelve residues

Script `p9_01_validate.py`; logs `logs/validate_K4_H_0.70.log`, `validate_K5_H_0.70.log`,
`validate_LKSEc5_H_0.60.log` (the runs cited are the re-runs with the final library; the first
runs, made with an earlier version of one routine, are in `not_cited/` and gave the same numbers
to the printed digits).  Instances: Lys₄ (16 464 states), Lys₅ (115 248), LKSE:5 (14 508) on the
helix, P2's pruned domain as P3 and P8 use it; every order `m = 3 … n`; **every state**.

**Left sides — my own code** (P3's evaluator supplies coordinates and Born radii only).
`g` at every state (P3's bulk evaluator); every term `t_pq`, `p ≤ q`, at every state from
coordinates and Born radii (the sum of the terms equals `g` to `1–2·10⁻¹²` kcal/mol);
`R_m(x) = |g − I_{m−1}g|(x)`; and, block by block, `L_m[𝔅](x) = Σ_{τ∈𝔅} |τ(x) − I_{m−1}τ(x)|` — absolute
values term by term, so that no cancellation inside a block can hide anything.  Three
independent confirmations of the left sides: P8's stored enumeration of `g` (`1.3–2.8·10⁻¹²`);
P8's stored block remainders, an enumeration pass of its own (`ws_P8/cache/bc_*_ckpt.npz`,
array `ACCR`; agreement `5·10⁻¹³`–`1.3·10⁻¹²` kcal/mol on all three instances after the blocks are
put in the same order — see my error 3 in §8); and the coordinator's three logs
`p8_verification/lys_enum_check_K4.log`, `_K5.log`, `_LKSEc5.log` (largest `R` of every order and its
Boltzmann mean, to the printed digits).  *The "self-test" printed in my
logs is not an independent check:* the two remainder routines it compares perform the same
subtractions in the same order (deviation exactly 0).

**Right sides.**  `E^s[𝔅](x) = Σ_{T ⊆ S(x)} Θ^s_{𝔅,T}(x_T)` for stage `s = 1` (P8's own arrays, recorded
in its code path before `_c1`/`_c2` maximise them) and `s = 2` (my evaluation with the actual
increments), and every table form built from them.  Two checks of the *code* precede the
checks of the statements (`p9_00b_consistency.py`, logs `logs/consistency_*.log`): the maximum
over the states of a stage-1 block table **is** P8's 'SAb' block constant (relative deviation
`0.0`), and stage 2 with every actual increment replaced by P3's maximum reproduces stage 1
(`4·10⁻¹⁶` on Lys₄, `9·10⁻¹⁶` on a sample of four subsets of Lys₁₂ at order 5).

**Checks** (tolerance `10⁻¹⁰` kcal/mol absolute, `10⁻¹²` relative):

* **V1** `L_m[𝔅](x) ≤ E^s[𝔅](x)` for every block, state and order — Theorem R itself, sharp.
* **V2** `R_m(x) ≤ E^s(x)` — the hypothesis of the pipeline, resolved.
* **V3** `E^s(x) ≤ pen(x)` and `R_m(x) ≤ pen(x)` for every table form: S; B and T with all tuples in
  band and with bands 1, 2 (the chains for what does not fit); W with window 2 and with
  everything in the window (then W *is* the envelope).  `E^s ≤ pen` is the sharp form of
  Proposition P: it is attained with equality.
* **V4** resolved `≤` the same form with the constants `ĉ^{J,s}` `≤` with P8's constants, pointwise.

**Controls that must fail** (`DEAD_ENDS.md` SD59: a check that cannot fail checks nothing).
**W1**: the *minimum* over the states in place of the value at the state (block tables; and
every site, pair, triple and window table).  **W2**: the value at a *wrong rotamer* (every
table rolled by one position along each state axis).  **W4**: shares that do not add up (the
banded forms without the parts moved from out-of-band tuples).

| instance (states; blocks) | order | subsets | stage | V1: block comparisons; violations; smallest bound/exact | V2: whole function, violations; smallest bound/remainder | V3, V4: violations over all table forms (envelope ≤ table; remainder ≤ table; chain) | Boltzmann mean of the envelope / of the remainder | control W1 (minimum over the states): violations at block level; whole function | control W2 (wrong rotamer): block level; whole function | controls on the tables, 'envelope ≤ table' violated: fewest over the forms (W1; W2) | control W4 (far parts dropped), 'envelope ≤ table' violated: fewest over the banded forms |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Lys₄ (16464; 16) | 3 | 4 | 1 | 263424; 0; **1.0374** | 0; 23.75 | 0; 0; 0 (8 forms) | 5190 | 10384; 0 | 3609; 0 | 117; 33 | 2677 |
| Lys₄ (16464; 16) | 3 | 4 | 2 | 263424; 0; **1.0086** | 0; 12.66 | 0; 0; 0 (8 forms) | 842 | 223481; 7762 | 50358; 13 | 4166; 69 | 22 |
| Lys₄ (16464; 16) | 4 | 1 | 1 | 263424; 0; **1.1641** | 0; 66.52 | 0; 0; 0 (8 forms) | 22692 | 1898; 0 | 621; 0 | 90; 17 | 3957 |
| Lys₄ (16464; 16) | 4 | 1 | 2 | 263424; 0; **1.0148** | 0; 11.19 | 0; 0; 0 (8 forms) | 880 | 162929; 8412 | 41243; 95 | 1744; 34 | 15 |
| Lys₅ (115248; 22) | 3 | 10 | 1 | 2535456; 0; **1.0211** | 0; 11.97 | 0; 0; 0 (8 forms) | 3902 | 140286; 0 | 52716; 0 | 640; 98 | 77113 |
| Lys₅ (115248; 22) | 3 | 10 | 2 | 2535456; 0; **1.0066** | 0; 8.46 | 0; 0; 0 (8 forms) | 593 | 2157553; 49983 | 469671; 414 | 22668; 378 | 15933 |
| Lys₅ (115248; 22) | 4 | 5 | 1 | 2535456; 0; **1.0732** | 0; 25.09 | 0; 0; 0 (8 forms) | 17616 | 41045; 0 | 15422; 0 | 581; 180 | 55128 |
| Lys₅ (115248; 22) | 4 | 5 | 2 | 2535456; 0; **1.0143** | 0; 10.75 | 0; 0; 0 (8 forms) | 661 | 2086029; 73096 | 496483; 1070 | 11091; 142 | 747 |
| Lys₅ (115248; 22) | 5 | 1 | 1 | 2535456; 0; **1.1208** | 0; 63.40 | 0; 0; 0 (8 forms) | 184323 | 9457; 0 | 3373; 0 | 180; 96 | 37858 |
| Lys₅ (115248; 22) | 5 | 1 | 2 | 2535456; 0; **1.0192** | 0; 12.49 | 0; 0; 0 (8 forms) | 640 | 1109737; 55006 | 286016; 1884 | 5495; 141 | 541 |
| LKSE:5 (14508; 22) | 3 | 10 | 1 | 319176; 0; **1.0092** | 0; 59.03 | 0; 0; 0 (8 forms) | 31420 | 18482; 0 | 6727; 0 | 30; 4 | 3618 |
| LKSE:5 (14508; 22) | 3 | 10 | 2 | 319176; 0; **1.0043** | 0; 30.16 | 0; 0; 0 (8 forms) | 697 | 221174; 931 | 50114; 6 | 247; 10 | 3579 |
| LKSE:5 (14508; 22) | 4 | 5 | 1 | 319176; 0; **1.0180** | 0; 47.79 | 0; 0; 0 (8 forms) | 289943 | 6977; 0 | 2624; 0 | 42; 19 | 3135 |
| LKSE:5 (14508; 22) | 4 | 5 | 2 | 319176; 0; **1.0034** | 0; 17.03 | 0; 0; 0 (8 forms) | 748 | 165110; 1716 | 41162; 1 | 106; 8 | 550 |
| LKSE:5 (14508; 22) | 5 | 1 | 1 | 319176; 0; **1.0352** | 0; 121.63 | 0; 0; 0 (8 forms) | 73753 | 1817; 0 | 667; 0 | 319; 190 | 2880 |
| LKSE:5 (14508; 22) | 5 | 1 | 2 | 319176; 0; **1.0100** | 0; 27.17 | 0; 0; 0 (8 forms) | 255 | 50417; 1146 | 13641; 1 | 80; 13 | 67 |

In all: 18181488 block-level comparisons (V1), 844392 whole-function checks (V2), 13510272 table checks (V3: two inequalities per form and state); **violations of V1–V4: 0**.

Ranges over the rows:

* stage 1: smallest block ratio 1.0092–1.1641; smallest whole-function ratio 12.0–121.6; Boltzmann mean of the envelope over that of the remainder 3902–289943; control W1 at block level 1817–140286 violations, against the whole function 0–0; control W2 at block level 621–52716, against the whole function 0–0; controls on the tables ('envelope ≤ table'): W1 at least 30, W2 at least 4, W4 at least 2677 violations in every form and row.
* stage 2: smallest block ratio 1.0034–1.0192; smallest whole-function ratio 8.5–30.2; Boltzmann mean of the envelope over that of the remainder 255–880; control W1 at block level 50417–2157553 violations, against the whole function 931–73096; control W2 at block level 13641–496483, against the whole function 1–1884; controls on the tables ('envelope ≤ table'): W1 at least 80, W2 at least 8, W4 at least 15 violations in every form and row.

**Reading.**  (i) *No violation of V1–V4 anywhere.*  At block level the resolved bound is
attained within 0.3–2 % in stage 2 (smallest ratios 1.0034–1.0192) and within 1–16 % in stage 1
(1.0092–1.1641): the statement is tight where it is tight, and never violated.  (ii) *Every
control fails at block level*, in both stages, in every row (`6·10²`–`2·10⁶` violations), and every
control on the tables fails in "envelope ≤ table" in every form and row.  (iii) **Against the
whole function the controls fail only in stage 2.**  In stage 1 the bound stays a factor
12–122 above the remainder at every state, so a table that is wrong by a factor two passes
`R ≤ pen` — the whole-function check, the one the brief names, has *no power* for stage 1 (0
violations of both controls in all eight rows); what validates stage 1 is V1 and "envelope ≤
table".  For stage 2 the whole-function check does detect W1 (931–73 096 violations) and W2
(1–1 884).  (iv) *How far the bound is from the truth where it matters:* in Boltzmann mean
under the true ensemble the stage-1 envelope is `4·10³`–`3·10⁵` times the remainder, the stage-2
envelope 255–880 times (the coordinator's logs give `9·10³`–`4·10⁵` for P8's constants on the same
instances).  (v) *What the enumeration cannot see:* interval enclosures, table allowances and
hulls are P3's and are inherited as in every certificate of the division; the check is of
the inequality chain built on them.

## 3. The tables: what they look like

Scripts: `p9_03_tables.py` (the bounds `Θ¹_T`, `Θ²_T` of all subsets of a twelve-residue peptide,
reduced on the fly to the sums the forms need), `p9_04_gain.py` (ratios on two Gibbs samples;
no model is built).  The Gibbs samples are the coordinator's sampler with its seeds (4242, 777;
`p9_02_gibbs.py`); they reproduce the off-anchor frequencies of the coordinator's logs digit
for digit and are uncertified.

### 3.1 The bound of a subset as a function of the states of its sites [M]

`Γ_m` and its resolved counterparts, in `k_BT` (sums over all subsets; P8's two columns are
re-computed here in P8's code path and equal P8's stored per-subset values exactly —
relative deviation `0.0` in every run):

| peptide, order | subsets | `βΓ_m`: P8's 'Sb' | P8's 'SAb' | joint maximum, stage 1 `Σ ĉ^{J,1}` | **joint maximum, stage 2 `Σ ĉ^{J,2}`** | sum of the medians over the states: stage 1; stage 2 | sum of the minima: stage 1; stage 2 | `ĉ^{J,2}/ĉ^{SAb}` per subset: min, median, max | seconds per subset; peak RSS (MB) |
|---|---|---|---|---|---|---|---|---|---|
| Lys₁₂, 3 | 220 | 408.11 | 375.11 | 372.74 | **272.11** | 138.3; 9.758 | 97.2; 0.3529 | 0.391, 0.673, 0.9403 | 0.08; 277 |
| Lys₁₂, 4 | 495 | 36.329 | 33.983 | 33.413 | **18.17** | 12.63; 0.2334 | 8.768; 0.001704 | 0.280, 0.553, 0.8612 | 0.15; 354 |
| Lys₁₂, 5 | 792 | 2.5403 | 2.4048 | 2.3367 | **0.98685** | 0.8822; 0.004074 | 0.5989; 6.054e-06 | 0.226, 0.434, 0.7636 | 0.46; 640 |
| (LKSE)₃, 3 | 220 | 1778.1 | 1660 | 1649.9 | **1234.8** | 1142; 266 | 1022; 86.54 | 0.346, 0.704, 1.0000 | 0.08; 225 |
| (LKSE)₃, 4 | 495 | 311.84 | 295.77 | 293.71 | **198.78** | 212.8; 20.92 | 190.9; 2.163 | 0.295, 0.617, 0.9747 | 0.16; 339 |
| (LKSE)₃, 5 | 792 | 44.543 | 42.836 | 42.624 | **26.093** | 31.21; 1.017 | 28.1; 0.02739 | 0.217, 0.542, 0.9449 | 0.58, 0.62; 1128 |
| Ser₁₂, 5 | 792 | 0.13846 | 0.13807 | 0.13796 | **0.092514** | 0.1197; 0.01071 | 0.1107; 0.001697 | 0.328, 0.687, 0.8648 | 0.25; 171 |

*Reading.*  **Stage 1 — the dependence on the host's rotamer is weak.**  Summed over the
subsets, the maximum and the minimum of `Θ¹_T` over the states of `T` differ by a factor 1.2–4:
the sum of the minima is 25–26 % of P8's constants for lysine, 62–66 % for the patterned sequence, 80 % for serine; the sum of its
medians 37 %, 69–73 %, 87 %; and its joint maximum is 97–99.9 % of 'SAb' (the block-wise
maxima nearly coincide).  The reason is in the formula: for a host `l ∈ T` the bound is
`W(x⁰_l) + W(x_l)` (P3's Remark L3) — the anchor half does not depend on `x`; the blocks without
a host in `T` do not either; and `W(b)` still carries the *maximal* increments of the non-host
sites, so it moves only through hulls and distances.  On Lys₄ the state-independent part is
36–43 % of the constant (`logs/probe_K4_H_0.70.log`).  This is the answer to the brief's
alternative stopping condition, *for the first stage as the brief defines it*.

**Stage 2 — the dependence on the rotamers of the non-host sites is strong, and grows with
the order.**  The typical (median) value of `Θ²_T` is 38, 146, 590 times below P8's constant
for Lys₁₂ at orders 3, 4, 5; 6, 14, 42 times for (LKSE)₃; 13 times for Ser₁₂; its minimum up
to five orders of magnitude below.  And **its maximum over the states — a state-independent
constant, `ĉ^{J,2}_T` of Corollary J — is 41–74 % of P8's**: `βΓ_m` falls from 34.0 to 18.2
(Lys₁₂, order 4), from 2.40 to 0.99 (order 5), from 42.8 to 26.1 ((LKSE)₃, order 5), without
any state dependence in the penalty.  The increments enter as products over the `m − 1` or
`m − 2` non-host sites of each term, and the rotamers the ensemble visits are mostly the ones
near the anchor, with small increments.

### 3.2 Site by site (question 3 of the brief) [M]

**Lys₁₂, order 4** — site form `γ_i(b) = (1/m) Σ_{T∋i} max{Θ_T : x_i = b}` against the state-independent `γ_i^SAb = (1/m) Σ_{T∋i} ĉ_T^SAb`.

| site | states | visits off the anchor (pooled Gibbs sample, 1 920 states) | `βγ_i^SAb` | stage 1: max over `b`, Boltzmann-typical, min over `b` (ratios to `γ_i^SAb`) | **stage 2**: max, typical, min |
|---|---|---|---|---|---|
| 0 | 14 | 776 | 2.487 | 0.923, 0.729, 0.725 | 0.351, 0.337, 0.078 |
| 1 | 14 | 447 | 3.322 | 0.928, 0.773, 0.770 | 0.390, 0.336, 0.072 |
| 2 | 12 | 433 | 3.085 | 0.957, 0.847, 0.844 | 0.450, 0.373, 0.079 |
| 3 | 7 | 56 | 3.09 | 0.906, 0.761, 0.719 | 0.423, 0.16, 0.113 |
| 4 | 7 | 43 | 4.231 | 0.840, 0.737, 0.722 | 0.368, 0.167, 0.132 |
| 5 | 7 | 39 | 3.621 | 0.850, 0.736, 0.728 | 0.379, 0.12, 0.097 |
| 6 | 7 | 35 | 3.154 | 0.845, 0.717, 0.709 | 0.399, 0.105, 0.091 |
| 7 | 7 | 49 | 3.518 | 0.850, 0.734, 0.720 | 0.376, 0.107, 0.080 |
| 8 | 7 | 77 | 2.715 | 0.950, 0.78, 0.773 | 0.361, 0.0757, 0.063 |
| 9 | 7 | 97 | 1.853 | 0.944, 0.868, 0.864 | 0.410, 0.0661, 0.048 |
| 10 | 7 | 129 | 1.629 | 0.948, 0.872, 0.869 | 0.438, 0.055, 0.044 |
| 11 | 7 | 124 | 1.281 | 0.966, 0.881, 0.880 | 0.455, 0.0474, 0.044 |

First-order numbers `2β⟨pen⟩` on the check sample (seed 777) [the estimate `ln⟨e^{β pen}⟩ − ln⟨e^{−β pen}⟩`; the largest `β·pen` on the sample] — uncertified estimates:

| form | P8's constants SAb | joint maxima of stage 2 as constants | resolved, stage 1 | **resolved, stage 2** | stage 2 / SAb |
|---|---|---|---|---|---|
| S | 6.37 [8.94; 13.4] | 3.29 [3.81; 6.95] | 4.96 [6.32; 10.1] | 1.81 [1.94; 3.54] | 0.284 |
| B | 0.948 [1.3; 5.09] | 0.491 [0.531; 2.57] | 0.652 [0.729; 3.14] | 0.192 [0.194; 0.807] | 0.203 |
| T | 0.489 [0.502; 1.76] | 0.267 [0.269; 0.898] | 0.358 [0.361; 1.09] | 0.111 [0.111; 0.311] | 0.228 |
| W | 0.00416 [0.00417; 0.254] | 0.00229 [0.00229; 0.125] | 0.00239 [0.00239; 0.11] | 0.000164 [0.000164; 0.00582] | 0.0395 |

Envelope `Σ_{T⊆S(x)}`, `2β⟨env⟩` on the two samples (777 / 4242): P8's constants 0.000794 / 0.00368; joint maxima of stage 2 0.000416 / 0.00174; resolved stage 1 0.000389 / 0.00176; **resolved stage 2 1.16e-05 / 0.000114**.


**Lys₁₂, order 5** — site form `γ_i(b) = (1/m) Σ_{T∋i} max{Θ_T : x_i = b}` against the state-independent `γ_i^SAb = (1/m) Σ_{T∋i} ĉ_T^SAb`.

| site | states | visits off the anchor (pooled Gibbs sample, 1 920 states) | `βγ_i^SAb` | stage 1: max over `b`, Boltzmann-typical, min over `b` (ratios to `γ_i^SAb`) | **stage 2**: max, typical, min |
|---|---|---|---|---|---|
| 0 | 14 | 776 | 0.1827 | 0.934, 0.774, 0.772 | 0.302, 0.288, 0.057 |
| 1 | 14 | 447 | 0.2368 | 0.939, 0.8, 0.798 | 0.321, 0.277, 0.052 |
| 2 | 12 | 433 | 0.2211 | 0.962, 0.876, 0.873 | 0.362, 0.303, 0.057 |
| 3 | 7 | 56 | 0.2194 | 0.907, 0.797, 0.763 | 0.318, 0.119, 0.083 |
| 4 | 7 | 43 | 0.2891 | 0.856, 0.773, 0.754 | 0.284, 0.127, 0.095 |
| 5 | 7 | 39 | 0.2541 | 0.870, 0.782, 0.771 | 0.307, 0.0911, 0.072 |
| 6 | 7 | 35 | 0.2231 | 0.857, 0.763, 0.755 | 0.320, 0.0812, 0.069 |
| 7 | 7 | 49 | 0.244 | 0.864, 0.766, 0.753 | 0.286, 0.0811, 0.059 |
| 8 | 7 | 77 | 0.1914 | 0.949, 0.804, 0.798 | 0.303, 0.0539, 0.043 |
| 9 | 7 | 97 | 0.1328 | 0.944, 0.891, 0.889 | 0.313, 0.0453, 0.031 |
| 10 | 7 | 129 | 0.1177 | 0.946, 0.896, 0.895 | 0.338, 0.0364, 0.028 |
| 11 | 7 | 124 | 0.09247 | 0.958, 0.902, 0.902 | 0.343, 0.0312, 0.028 |

First-order numbers `2β⟨pen⟩` on the check sample (seed 777) [the estimate `ln⟨e^{β pen}⟩ − ln⟨e^{−β pen}⟩`; the largest `β·pen` on the sample] — uncertified estimates:

| form | P8's constants SAb | joint maxima of stage 2 as constants | resolved, stage 1 | **resolved, stage 2** | stage 2 / SAb |
|---|---|---|---|---|---|
| S | 0.458 [0.46; 0.947] | 0.182 [0.183; 0.374] | 0.372 [0.373; 0.754] | 0.108 [0.108; 0.209] | 0.236 |
| B | 0.0821 [0.0822; 0.368] | 0.0343 [0.0343; 0.142] | 0.0616 [0.0617; 0.251] | 0.0145 [0.0145; 0.0551] | 0.176 |
| T | 0.0525 [0.0525; 0.162] | 0.0234 [0.0234; 0.0682] | 0.0402 [0.0402; 0.109] | 0.00935 [0.00935; 0.0243] | 0.178 |
| W | 4.41e-05 [4.41e-05; 0.00669] | 2.1e-05 [2.1e-05; 0.00261] | 2.25e-05 [2.25e-05; 0.00274] | 1.68e-07 [1.68e-07; 1.14e-05] | 0.00381 |

Envelope `Σ_{T⊆S(x)}`, `2β⟨env⟩` on the two samples (777 / 4242): P8's constants 0 / 1.18e-05; joint maxima of stage 2 0 / 4.67e-06; resolved stage 1 0 / 5.67e-06; **resolved stage 2 0 / 2.01e-09**.


**(LKSE)₃, order 5** — site form `γ_i(b) = (1/m) Σ_{T∋i} max{Θ_T : x_i = b}` against the state-independent `γ_i^SAb = (1/m) Σ_{T∋i} ĉ_T^SAb`.

| site | states | visits off the anchor (pooled Gibbs sample, 1 920 states) | `βγ_i^SAb` | stage 1: max over `b`, Boltzmann-typical, min over `b` (ratios to `γ_i^SAb`) | **stage 2**: max, typical, min |
|---|---|---|---|---|---|
| 0 | 2 | 234 | 2.412 | 0.997, 0.997, 0.997 | 0.661, 0.661, 0.661 |
| 1 | 29 | 665 | 3.581 | 0.982, 0.92, 0.919 | 0.440, 0.214, 0.048 |
| 2 | 9 | 1102 | 2.251 | 0.934, 0.851, 0.821 | 0.446, 0.146, 0.124 |
| 3 | 12 | 661 | 3.981 | 0.988, 0.955, 0.937 | 0.576, 0.122, 0.093 |
| 4 | 2 | 0 | 5.68 | 0.997, —, 0.997 | 0.662, —, 0.662 |
| 5 | 14 | 69 | 4.823 | 0.968, 0.915, 0.912 | 0.525, 0.0536, 0.046 |
| 6 | 9 | 508 | 3.944 | 0.982, 0.816, 0.813 | 0.502, 0.223, 0.179 |
| 7 | 12 | 642 | 5.078 | 0.976, 0.941, 0.940 | 0.608, 0.0855, 0.074 |
| 8 | 2 | 0 | 4.516 | 0.997, —, 0.997 | 0.667, —, 0.667 |
| 9 | 16 | 116 | 2.583 | 0.982, 0.958, 0.954 | 0.504, 0.0489, 0.033 |
| 10 | 9 | 669 | 1.937 | 0.967, 0.777, 0.774 | 0.512, 0.258, 0.201 |
| 11 | 13 | 838 | 2.05 | 0.992, 0.898, 0.890 | 0.631, 0.0617, 0.060 |

First-order numbers `2β⟨pen⟩` on the check sample (seed 777) [the estimate `ln⟨e^{β pen}⟩ − ln⟨e^{−β pen}⟩`; the largest `β·pen` on the sample] — uncertified estimates:

| form | P8's constants SAb | joint maxima of stage 2 as constants | resolved, stage 1 | **resolved, stage 2** | stage 2 / SAb |
|---|---|---|---|---|---|
| S | 17.4 [22.4; 25.8] | 10.3 [12.1; 15.2] | 15.6 [20; 23.4] | 2.79 [2.93; 5.05] | 0.16 |
| B | 4.06 [9.6; 15.2] | 2.34 [3.7; 8.67] | 3.31 [7; 12.6] | 0.287 [0.29; 1.18] | 0.0708 |
| T | 1.73 [3.48; 9.25] | 1.01 [1.2; 5.2] | 1.39 [1.99; 7.1] | 0.18 [0.181; 0.552] | 0.104 |
| W | 0.0546 [0.0631; 2.37] | 0.0284 [0.0293; 1.18] | 0.0294 [0.0303; 1.25] | 1.96e-05 [1.96e-05; 0.00164] | 0.000358 |

Envelope `Σ_{T⊆S(x)}`, `2β⟨env⟩` on the two samples (777 / 4242): P8's constants 0.0241 / 0.0272; joint maxima of stage 2 0.012 / 0.0136; resolved stage 1 0.0101 / 0.0114; **resolved stage 2 1.23e-06 / 1.64e-06**.

*Reading.*  (i) *Maximum over `b`:* at most 1 in every row, as it must be; for stage 1 it is
0.84–1.00, for stage 2 0.28–0.67.  **It is not 1 for the worst rotamer, as the brief
expected, for two reasons:** subset by subset the maximum over `b` of `c_{T,i}(b)` *is* the joint
maximum `ĉ^J_T` (by construction), but different subsets have different worst rotamers of the
same site, so the maximum of the sum is below the sum of the maxima; and P8's constant, the
reference of the ratio, takes its maxima block by block, the table jointly.  (ii) *Boltzmann-typical value:* stage 1 0.72–1.00 of the
state-independent penalty — nearly nothing; stage 2 0.03–0.37 for lysine and 0.05–0.26 for
the patterned sequence (0.66 at its two-state leucine sites, which have nothing to resolve
in themselves and gain only through the other sites of their subsets).  (iii) For Lys₁₂ the
three N-terminal sites, which carry most of the off-anchor weight (each is off the anchor 23–40 % of the time), sit in **one**
alternative rotamer whose penalty is near the maximum (0.28–0.37 of 'SAb'); the nine frozen
sites visit rotamers at 0.03–0.17.  (iv) The gain grows with the size of the tuple that is
resolved: first-order numbers of forms S, B, T fall to 0.16–0.28, 0.07–0.20, 0.10–0.23 of
the state-independent ones, the window form to `4·10⁻⁴`–`0.04`, the envelope to
`5·10⁻⁵`–`0.03` (both samples; `0.015` at most on the check sample).

### 3.3 By rotamer [M]

Lys₁₂, order 4: for every non-anchor rotamer `b` of a site, in the order of the domain: frequency in the pooled Gibbs sample / `γ_i(b)/γ_i^SAb` stage 1 / stage 2

```
site  0: 0.000/0.74/0.337  0.002/0.73/0.326  0.010/0.73/0.345  0.358/0.73/0.351  0.006/0.73/0.350  0.002/0.73/0.323  0.000/0.75/0.305  0.001/0.75/0.086  0.008/0.73/0.078  0.003/0.88/0.301  0.013/0.79/0.150  0.003/0.74/0.113  0.000/0.92/0.331
site  1: 0.000/0.79/0.387  0.000/0.77/0.348  0.003/0.79/0.386  0.207/0.77/0.356  0.000/0.78/0.390  0.003/0.77/0.333  0.000/0.80/0.338  0.000/0.80/0.101  0.005/0.78/0.072  0.001/0.88/0.230  0.009/0.82/0.130  0.004/0.78/0.090  0.000/0.93/0.267
site  2: 0.003/0.86/0.430  0.202/0.84/0.394  0.001/0.86/0.450  0.002/0.85/0.368  0.000/0.88/0.376  0.000/0.88/0.114  0.005/0.85/0.079  0.003/0.96/0.236  0.009/0.89/0.133  0.003/0.85/0.093  0.000/0.90/0.198
site  3: 0.000/0.76/0.154  0.006/0.72/0.113  0.002/0.87/0.296  0.019/0.76/0.156  0.002/0.75/0.200  0.000/0.91/0.423
site  4: 0.000/0.83/0.265  0.006/0.73/0.198  0.002/0.80/0.226  0.012/0.73/0.132  0.002/0.72/0.211  0.000/0.84/0.368
site  5: 0.000/0.85/0.293  0.002/0.75/0.218  0.002/0.79/0.168  0.016/0.73/0.097  0.001/0.73/0.213  0.000/0.85/0.379
site  6: 0.000/0.84/0.293  0.001/0.73/0.195  0.002/0.77/0.165  0.015/0.71/0.091  0.000/0.72/0.217  0.000/0.85/0.399
site  7: 0.000/0.85/0.295  0.001/0.76/0.233  0.005/0.77/0.141  0.018/0.72/0.080  0.001/0.74/0.279  0.000/0.85/0.376
site  8: 0.000/0.95/0.361  0.001/0.85/0.300  0.019/0.77/0.063  0.019/0.78/0.068  0.001/0.82/0.326  0.000/0.83/0.319
site  9: 0.000/0.94/0.289  0.001/0.94/0.336  0.016/0.87/0.052  0.032/0.86/0.048  0.002/0.93/0.410  0.000/0.93/0.379
site 10: 0.000/0.94/0.276  0.002/0.95/0.340  0.027/0.87/0.047  0.039/0.87/0.044  0.001/0.93/0.438  0.000/0.94/0.377
site 11: 0.000/0.95/0.313  0.001/0.97/0.405  0.030/0.88/0.044  0.034/0.88/0.045  0.000/0.94/0.455  0.000/0.93/0.314
```

(LKSE)₃, order 5: for every non-anchor rotamer `b` of a site, in the order of the domain: frequency in the pooled Gibbs sample / `γ_i(b)/γ_i^SAb` stage 1 / stage 2

```
site  0: 0.122/1.00/0.661
site  1: 0.000/0.93/0.309  0.000/0.94/0.351  0.000/0.94/0.370  0.000/0.93/0.335  0.000/0.93/0.323  0.000/0.92/0.248  0.001/0.92/0.224  0.008/0.92/0.229  0.306/0.92/0.225  0.005/0.92/0.236  0.003/0.92/0.212  0.000/0.93/0.213  0.000/0.93/0.059  0.007/0.92/0.048  0.012/0.94/0.068  0.004/0.92/0.054  0.000/0.96/0.127  0.000/0.95/0.340  0.000/0.98/0.440  0.000/0.94/0.339  0.000/0.93/0.289  0.000/0.96/0.270  0.000/0.92/0.242  0.000/0.93/0.293  0.000/0.92/0.264  0.000/0.93/0.311  0.000/0.92/0.257  0.000/0.93/0.282
site  2: 0.378/0.86/0.138  0.003/0.93/0.254  0.033/0.84/0.243  0.105/0.82/0.124  0.055/0.83/0.173  0.000/0.91/0.446  0.000/0.85/0.183  0.000/0.91/0.404
site  3: 0.000/0.94/0.508  0.000/0.95/0.477  0.000/0.95/0.500  0.000/0.94/0.576  0.000/0.94/0.549  0.000/0.94/0.550  0.097/0.95/0.093  0.198/0.95/0.097  0.000/0.99/0.308  0.000/0.97/0.256  0.049/0.98/0.280
site  4: 0.000/1.00/0.662
site  5: 0.000/0.94/0.503  0.000/0.94/0.525  0.000/0.92/0.347  0.000/0.92/0.359  0.000/0.92/0.085  0.004/0.91/0.066  0.028/0.92/0.046  0.004/0.92/0.100  0.000/0.97/0.211  0.000/0.93/0.227  0.000/0.94/0.255  0.000/0.92/0.293  0.000/0.92/0.267
site  6: 0.010/0.83/0.181  0.012/0.82/0.179  0.040/0.82/0.249  0.142/0.81/0.219  0.061/0.82/0.231  0.000/0.95/0.502  0.000/0.91/0.285  0.000/0.98/0.458
site  7: 0.000/0.94/0.492  0.000/0.94/0.472  0.000/0.95/0.485  0.000/0.96/0.608  0.000/0.96/0.561  0.000/0.98/0.591  0.089/0.94/0.074  0.193/0.94/0.076  0.000/0.95/0.152  0.000/0.94/0.135  0.053/0.94/0.139
site  8: 0.000/1.00/0.667
site  9: 0.000/0.98/0.445  0.000/0.98/0.430  0.000/0.98/0.504  0.000/0.98/0.498  0.000/0.97/0.114  0.001/0.97/0.121  0.023/0.96/0.038  0.030/0.96/0.033  0.005/0.97/0.172  0.000/0.98/0.224  0.000/0.96/0.069  0.001/0.95/0.073  0.000/0.96/0.079  0.000/0.96/0.105  0.000/0.97/0.111
site 10: 0.017/0.80/0.233  0.017/0.80/0.201  0.028/0.78/0.263  0.187/0.78/0.260  0.099/0.77/0.269  0.000/0.97/0.512  0.000/0.90/0.310  0.000/0.97/0.440
site 11: 0.000/0.92/0.464  0.000/0.92/0.452  0.000/0.92/0.454  0.000/0.97/0.597  0.000/0.96/0.558  0.000/0.99/0.631  0.000/0.89/0.068  0.085/0.90/0.065  0.182/0.90/0.060  0.000/0.89/0.064  0.000/0.89/0.064  0.169/0.89/0.062
```

### 3.4 The resolved bound at twelve residues, checked where it can be [M]

`p9_06_check12.py`.  (a) At a state with exactly `m` sites off the anchor the remainder **is**
the anchored term of order `m`, `g − I_{m−1}g = d_T(x_T)`, which the ball of radius `m` gives exactly;
so with P8's balls of radius 3 and 4 Theorem R can be tested at orders 3 and 4 at **every**
such state.  (c) At order 5 no ball of radius 5 exists; there 20 000 random states with
exactly five sites off the anchor were evaluated (one new evaluation each; the lower orders
from the ball of radius 4).  (b) Uniformly random states with `m … 12` sites off the anchor
(new evaluations of `g`; `I_{m−1}g` from the ball by my own formula, self-tested to `2.5·10⁻¹⁴`), as
the coordinator did for P8's constants.  Controls as in §2: W1 (the minimum of the table in
place of its value) and W2 (the table rolled by one rotamer along each axis).

| peptide, order | (a) EVERY state with exactly `m` sites off the anchor: states; violations; smallest and median bound / exact term | (a) controls: minimum over the states; wrong rotamer (violations) | (c) random states with exactly `m` sites off (where no ball of radius `m` exists): states; violations; smallest and median ratio; controls (minimum; wrong rotamer) | (b) uniformly random states, `m … 12` sites off: states; violations; smallest envelope / remainder | (b) control, wrong rotamer (violations) |
|---|---|---|---|---|---|
| Lys₁₂, 3 | 92525; 0; 9.02, 313 | 14334; 471 | — | 2500; 0; 11.3 | 7 |
| Lys₁₂, 4 | 1524690; 0; 8.25, 275 | 631363; 25012 | — | 2250; 0; 12.1 | 6 |
| Lys₁₂, 5 | — | — | 20000; 0; 9.96, 222; 9475; 550 | 2000; 0; 15.0 | 11 |
| (LKSE)₃, 3 | 175185; 0; 15.05, 399 | 42045; 302 | — | 2500; 0; 30.7 | 1 |
| (LKSE)₃, 4 | 3290515; 0; 8.26, 373 | 1855970; 24135 | — | 2250; 0; 17.1 | 2 |
| (LKSE)₃, 5 | — | — | 20000; 0; 13.14, 323; 9919; 140 | 2000; 0; 13.6 | 4 |
| Ser₁₂, 5 | — | — | — | 2000; 0; 10.3 | 3 |

No violation in any row.  Both controls fail in (a) and (c) in every row (`10²`–`2·10⁶`
violations), and fail weakly in (b) (1–11 violations): (a) and (c) are the checks with power.
The resolved bound is still 8–15 times the exact term at its tightest state and 200–400
times at the median state: the slack that is left is the sign-blind class and the suprema
over hulls, not the rotamers.

## 4. The certified brackets, with the predictions written before them

Script `p9_05_brackets.py`.  **Models.**  The coordinator's window models with exact in-window
evaluated terms, occupancy-aware reductions and the split of the far pairs around the anchor
(`window_model_occ.build_window_models_occ`, the rule "occ+" of `occ_reduction_test.py`, guided
by the Gibbs sample of seed 4242), built with **zero penalties plus workstream P6's
floating-point allowances** — `p6lib.fp_tables`, allocated exactly as in the state-independent
form of the same name: I call the coordinator's own functions (`site_form`,
`banded_pair_form`) with all constants set to zero, which returns the allowances alone (`φ₁` for
the site form; `ψ₁`, the in-band `ψ₂` and the halves of the out-of-band `ψ₂` for the pair, triple
and window forms).  Then my tables are added: site tables to `lo.one[i]`, `up.one[i]`, pair tables
with `add_pair`, tables on three or more sites with `add_multi`, with sign `∓`.  The ball is P8's
cached one, compared row by row with `pwmodel.ball_states`, 1 000 random values re-evaluated
(largest deviation `0.0`).  **Hypothesis used:** `|g − I_{m−1}g|(x) ≤ pen(x)` pointwise — Theorem R,
Proposition P, Corollary S.

**Rows.**  "P8's constants (the coordinator's recipe)": the reference, built by the
coordinator's code with P8's stored constants — it **reproduces the coordinator's brackets
digit for digit** in every case where one exists (Lys₁₂ order 5: S, B, T; Lys₁₂ order 4: T;
(LKSE)₃ order 5: T; Lys₅: T at bands 2 and 3), which is the check of my driver.  "Joint maxima
of stage 2 (constants)": the state-independent constants `ĉ^{J,2}_T` of Corollary J in the same
forms.  "Resolved": the tables of Proposition P.  Form W with constants is `p9lib.window_form_const`
(each subset charged to the maximal in-window sub-tuple with the least product of off-anchor
frequencies) — the allocation alone, without resolution.  *My chain against the coordinator's
recipe at twelve residues, as functions* [M; `p9_08_chaincheck.py`, `logs/chaincheck_*.log`]: the
rows with constants in forms S, B, T that are not the reference go through `p9lib.form_tables`
with constant tables; fed with P8's constants, that chain plus P6's allowances as my driver
allocates them equals the penalty function of the coordinator's `site_form`, `banded_pair_form`
and `triple_form_two_windows` at 5 000 uniformly random states to a relative `4·10⁻¹⁶` (S),
`2·10⁻¹¹` (B) and `2.5·10⁻¹⁰` (T) at worst over Lys₁₂ at orders 4 and 5 and (LKSE)₃ at order 5 —
the size of the recipe's own rounding allowances.  Two codes for one formula agree; it is
not a test of the formula.

**Checks.**  The sandwich `m₋ ≤ E ≤ m₊` at the 960 Gibbs states of the check sample (seed 777;
not the sample that guides the models) in every row; at 2 000 exact samples of the floor where
the last column says so; on Lys₅ and LKSE:5 at **every** state, with the exact `ln Z` inside
(§4.4).  *Against the coordinator's sampled values* (addendum A17 (18), items 62–63; theirs,
not mine; probability 0.95; the two-end intervals with empirical Bernstein of the order-5
runs, the narrowest the coordinator's driver prints — its logs
`pi_inference/nested_sampler_K12_H_m5_w7_T_window_SAb_occ.log` and
`nested_sampler_LKSEc12_H_m5_w7_T_window_SAb_occ.log`): Lys₁₂: sampled interval `[517.128526, 517.128559]` (width 3.3e-05); of my 32 certified brackets (all orders, all rows) 32 contain it and 32 overlap it.  (LKSE)₃: sampled interval `[655.592089, 655.632643]` (width 0.041); of my 16 certified brackets (all orders, all rows) 12 contain it and 16 overlap it; the narrowest, `[655.604050, 655.621038]` (order 5, s2:W), is inside it.

### 4.1 The predictions [written into `NOTES.md` before the models of each instance were built; the times are there]

| instance, order | what | predicted bracket (nats), written before the models | found | found / predicted | inside the range I gave? |
|---|---|---|---|---|---|
| Lys₁₂, 4 | reductions alone (all penalties zero) | 0.007 | **0.007132** | 1.02 | (no range given) |
| Lys₁₂, 4 | T, stage 1 | 0.75 (0.6–0.9) | **0.3493** | 0.47 | **no** |
| Lys₁₂, 4 | T, stage 2 | 0.15 (0.13–0.18; at worst 0.5) | **0.1115** | 0.74 | **no** |
| Lys₁₂, 4 | B, stage 2 | 0.25 | **0.1853** | 0.74 | (no range given) |
| Lys₁₂, 4 | S, stage 2 | 3 (2.5–4) | **1.874** | 0.62 | **no** |
| Lys₁₂, 4 | W, P8's constants | 0.02 (0.012–0.03) | **0.7207** | 36.04 | **no** |
| Lys₁₂, 4 | W, stage 2 | 0.0075 (0.0073–0.0080) | **0.007347** | 0.98 | yes |
| Lys₁₂, 5 | T, stage 1 | 0.045 (0.043–0.048) | **0.0452** | 1.00 | yes |
| Lys₁₂, 5 | T, stage 2 | 0.0165 (0.016–0.0175) | **0.016** | 0.97 | **no** |
| Lys₁₂, 5 | B, stage 2 | 0.021 | **0.02058** | 0.98 | (no range given) |
| Lys₁₂, 5 | S, stage 2 | 0.11 | **0.1119** | 1.02 | (no range given) |
| Lys₁₂, 5 | W, P8's constants | 0.0072 | **0.007286** | 1.01 | (no range given) |
| Lys₁₂, 5 | W, stage 2 | 0.00713 | **0.007233** | 1.01 | (no range given) |
| (LKSE)₃, 5 | T, stage 1 | 3.3 (2.8–3.8) | **1.871** | 0.57 | **no** |
| (LKSE)₃, 5 | T, stage 2 | 0.25 (0.22–0.35) | **0.1946** | 0.78 | **no** |
| (LKSE)₃, 5 | B, stage 2 | 0.4 (0.33–0.5) | **0.3009** | 0.75 | **no** |
| (LKSE)₃, 5 | S, stage 2 | 4 (3.5–6) | **2.918** | 0.73 | **no** |
| (LKSE)₃, 5 | W, P8's constants | 0.15 (0.1–0.4) | **1.311** | 8.74 | **no** |
| (LKSE)₃, 5 | W, stage 2 | 0.0168 (0.0167–0.0175) | **0.01699** | 1.01 | yes |
| (LKSE)₃, 4 | reductions alone (all penalties zero) | 0.017 | **0.01669** | 0.98 | (no range given) |
| (LKSE)₃, 4 | W, stage 2 | 0.02 (0.018–0.03), with a 40 % risk of more than 1 | **0.0191** | 0.96 | yes |
| (LKSE)₃, 4 | T, stage 2 | 3 (1.2–8) | **1.147** | 0.38 | **no** |
| (LKSE)₃, 4 | W, stage 1 | more than 5 | **166.5** | — | yes |
| Lys₁₂, 3 | W, stage 2 | 0.12 (0.08–0.3), with a 50 % risk of more than 1 | **0.07686** | 0.64 | **no** |
| Lys₁₂, 3 | T, stage 2 | more than 2 | **0.832** | — | **no** |
| (LKSE)₃, 3 | W, stage 2 | more than 2 | **658.9** | — | yes |

(The line "Lys₁₂, 5: T, stage 2" reads 0.016 at four digits; the width is 0.0159968
(`out/brackets_K12_H_0.70_m5_w7_B.json`), below the lower end 0.016 of the range I had given
by `3·10⁻⁶`: "no".)

Basis of every prediction: the first-order numbers of §3.2 plus the penalty-free width, and a
guess about the floor.  **What was wrong, and why** — §4.5.

### 4.2 Lys₁₂ on the helix [M; validity P]

**Lys₁₂, order 4, band 7 (ball 96 366)** — the models with all penalties zero (what the reductions cost; not a sandwich): 0.007132 nats.

| penalty | form | certified bracket of `ln Z` | width (nats) | `β ×` mean of `m₊ − m₋` on the check sample | sandwich violated at the 960 Gibbs states | exact samples of the floor: sites off the anchor (mean); violations |
|---|---|---|---|---|---|---|
| P8's constants 'SAb' (the coordinator's recipe) | S | `[515.931855, 526.493103]` | **10.56** | 6.38 | 0 | — |
| resolved, stage 1 | S | `[516.013141, 522.892300]` | **6.879** | 4.969 | 0 | — |
| **resolved, stage 2** | S | `[516.511117, 518.385324]` | **1.874** | 1.82 | 0 | — |
| P8's constants 'SAb' (the coordinator's recipe) | B | `[516.824121, 519.920439]` | **3.096** | 0.9553 | 0 | — |
| resolved, stage 1 | B | `[516.887590, 517.612872]` | **0.7253** | 0.6597 | 0 | — |
| **resolved, stage 2** | B | `[517.045207, 517.230503]` | **0.1853** | 0.1994 | 0 | — |
| P8's constants 'SAb' (the coordinator's recipe) | T | `[516.924368, 518.336878]` | **1.413** | 0.4964 | 0 | 2000 samples: 7.18; 0 |
| joint maxima of stage 2 (constants) | T | `[517.008878, 517.270943]` | **0.2621** | 0.2747 | 0 | — |
| resolved, stage 1 | T | `[516.971032, 517.320289]` | **0.3493** | 0.3658 | 0 | 2000 samples: 1.34; 0 |
| **resolved, stage 2** | T | `[517.075039, 517.186576]` | **0.1115** | 0.1187 | 0 | 2000 samples: 1.20; 0 |
| P8's constants 'SAb', my chains | W | `[517.123316, 517.844029]` | **0.7207** | 0.0115 | 0 | 2000 samples: 6.58; 0 |
| joint maxima of stage 2 (constants) | W | `[517.124375, 517.134614]` | **0.01024** | 0.009624 | 0 | — |
| resolved, stage 1 | W | `[517.124286, 517.134627]` | **0.01034** | 0.00973 | 0 | — |
| **resolved, stage 2** | W | `[517.125649, 517.132996]` | **0.007347** | 0.0075 | 0 | 2000 samples: 1.15; 0 |

**Lys₁₂, order 5, band 7 (ball 1 621 056)** — the models with all penalties zero (what the reductions cost; not a sandwich): 0.007133 nats.

| penalty | form | certified bracket of `ln Z` | width (nats) | `β ×` mean of `m₊ − m₋` on the check sample | sandwich violated at the 960 Gibbs states | exact samples of the floor: sites off the anchor (mean); violations |
|---|---|---|---|---|---|---|
| P8's constants 'SAb' (the coordinator's recipe) | S | `[516.918315, 517.376967]` | **0.4587** | 0.4661 | 0 | — |
| resolved, stage 1 | S | `[516.954491, 517.328608]` | **0.3741** | 0.3801 | 0 | — |
| **resolved, stage 2** | S | `[517.074547, 517.186432]` | **0.1119** | 0.1157 | 0 | — |
| P8's constants 'SAb' (the coordinator's recipe) | B | `[517.088342, 517.173208]` | **0.08487** | 0.08953 | 0 | — |
| resolved, stage 1 | B | `[517.097272, 517.162891]` | **0.06562** | 0.06906 | 0 | — |
| **resolved, stage 2** | B | `[517.119079, 517.139654]` | **0.02058** | 0.02189 | 0 | — |
| P8's constants 'SAb' (the coordinator's recipe) | T | `[517.101364, 517.158058]` | **0.05669** | 0.05991 | 0 | 2000 samples: 1.18; 0 |
| joint maxima of stage 2 (constants) | T | `[517.114741, 517.144086]` | **0.02934** | 0.03084 | 0 | — |
| resolved, stage 1 | T | `[517.106951, 517.152147]` | **0.0452** | 0.0476 | 0 | 2000 samples: 1.17; 0 |
| **resolved, stage 2** | T | `[517.121336, 517.137333]` | **0.016** | 0.01677 | 0 | 2000 samples: 1.16; 0 |
| P8's constants 'SAb', my chains | W | `[517.125679, 517.132965]` | **0.007286** | 0.007464 | 0 | 2000 samples: 1.15; 0 |
| joint maxima of stage 2 (constants) | W | `[517.125692, 517.132951]` | **0.007259** | 0.007441 | 0 | — |
| resolved, stage 1 | W | `[517.125691, 517.132952]` | **0.007261** | 0.007442 | 0 | — |
| **resolved, stage 2** | W | `[517.125705, 517.132938]` | **0.007233** | 0.00742 | 0 | 2000 samples: 1.15; 0 |

### 4.3 (LKSE)₃ on the helix [M; validity P]

**(LKSE)₃, order 5, band 7 (ball 3 471 783)** — the models with all penalties zero (what the reductions cost; not a sandwich): 0.0167 nats.

| penalty | form | certified bracket of `ln Z` | width (nats) | `β ×` mean of `m₊ − m₋` on the check sample | sandwich violated at the 960 Gibbs states | exact samples of the floor: sites off the anchor (mean); violations |
|---|---|---|---|---|---|---|
| **resolved, stage 2** | S | `[654.528369, 657.446737]` | **2.918** | 2.811 | 0 | — |
| **resolved, stage 2** | B | `[655.475250, 655.776117]` | **0.3009** | 0.3046 | 0 | — |
| P8's constants 'SAb' (the coordinator's recipe) | T | `[654.981476, 659.282763]` | **4.301** | 1.744 | 0 | 2000 samples: 9.02; 0 |
| joint maxima of stage 2 (constants) | T | `[655.198838, 656.327471]` | **1.129** | 1.024 | 0 | — |
| resolved, stage 1 | T | `[655.070627, 656.941958]` | **1.871** | 1.406 | 0 | — |
| **resolved, stage 2** | T | `[655.520038, 655.714657]` | **0.1946** | 0.1977 | 0 | 2000 samples: 2.90; 0 |
| P8's constants 'SAb', my chains | W | `[655.586885, 656.898185]` | **1.311** | 0.0721 | 0 | 2000 samples: 9.40; 0 |
| joint maxima of stage 2 (constants) | W | `[655.594170, 655.633502]` | **0.03933** | 0.04594 | 0 | — |
| resolved, stage 1 | W | `[655.593546, 655.634115]` | **0.04057** | 0.0469 | 0 | — |
| **resolved, stage 2** | W | `[655.604050, 655.621038]` | **0.01699** | 0.01753 | 0 | 2000 samples: 2.82; 0 |

### 4.4 Every state: Lys₅ and LKSE:5 [X]

On the enumerated instances the same driver checks every sandwich at every state and
whether the exact `ln Z` (`251.348445` for Lys₅, `276.467293` for LKSE:5) is inside.  Result:
**no violation at any state and the exact value inside, in every row** (87 sandwiches in all: Lys₅, order 4, band 2: 19 rows, no violation at any state, exact value inside every bracket; Lys₅, order 4, band 3: 19 rows, no violation at any state, exact value inside every bracket; Lys₅, order 5, band 3: 19 rows, no violation at any state, exact value inside every bracket; LKSE:5, order 4, band 2: 15 rows, no violation at any state, exact value inside every bracket; LKSE:5, order 5, band 2: 15 rows, no violation at any state, exact value inside every bracket).  Logs: `logs/brackets_K5_H_0.70_m4_w2.log`, `_m4_w3.log`, `_m5_w3.log`,
`logs/brackets_LKSEc5_H_0.60_m4_w2.log`, `_m5_w2.log`.  My chains with P8's constants (rows "my
chains") equal the coordinator's forms to every printed digit.  Two of the five tables:

**Lys₅ (115 248 states, enumerated), order 4, band 2** — the models with all penalties zero (what the reductions cost; not a sandwich): 0.0459 nats.

| penalty | form | certified bracket of `ln Z` | width (nats) | `β ×` mean of `m₊ − m₋` on the check sample | sandwich violated at the 960 Gibbs states | violated at any state; exact `ln Z` inside | exact samples of the floor: sites off the anchor (mean); violations |
|---|---|---|---|---|---|---|---|
| P8's constants 'SAb' (the coordinator's recipe) | S | `[251.003734, 251.852770]` | **0.849** | 0.8276 | 0 | 0; yes | — |
| P8's constants 'SAb', my chains | S | `[251.003734, 251.852770]` | **0.849** | 0.8276 | 0 | 0; yes | — |
| joint maxima of stage 2 (constants) | S | `[251.155986, 251.596634]` | **0.4406** | 0.4385 | 0 | 0; yes | — |
| resolved, stage 1 | S | `[251.060427, 251.749517]` | **0.6891** | 0.6813 | 0 | 0; yes | — |
| **resolved, stage 2** | S | `[251.230773, 251.495235]` | **0.2645** | 0.2668 | 0 | 0; yes | — |
| P8's constants 'SAb' (the coordinator's recipe) | B | `[251.185565, 251.597280]` | **0.4117** | 0.3932 | 0 | 0; yes | — |
| P8's constants 'SAb', my chains | B | `[251.185565, 251.597280]` | **0.4117** | 0.3932 | 0 | 0; yes | — |
| joint maxima of stage 2 (constants) | B | `[251.253207, 251.479408]` | **0.2262** | 0.2252 | 0 | 0; yes | — |
| resolved, stage 1 | B | `[251.224753, 251.525426]` | **0.3007** | 0.2957 | 0 | 0; yes | — |
| **resolved, stage 2** | B | `[251.295663, 251.420920]` | **0.1253** | 0.1297 | 0 | 0; yes | — |
| P8's constants 'SAb' (the coordinator's recipe) | T | `[251.198528, 251.572785]` | **0.3743** | 0.3581 | 0 | 0; yes | — |
| P8's constants 'SAb', my chains | T | `[251.198528, 251.572785]` | **0.3743** | 0.3581 | 0 | 0; yes | — |
| joint maxima of stage 2 (constants) | T | `[251.260399, 251.469356]` | **0.209** | 0.2085 | 0 | 0; yes | — |
| resolved, stage 1 | T | `[251.236300, 251.506641]` | **0.2703** | 0.2671 | 0 | 0; yes | — |
| **resolved, stage 2** | T | `[251.298958, 251.416914]` | **0.118** | 0.1224 | 0 | 0; yes | — |
| P8's constants 'SAb', my chains | W | `[251.323891, 251.410287]` | **0.0864** | 0.09346 | 0 | 0; yes | — |
| joint maxima of stage 2 (constants) | W | `[251.327967, 251.390713]` | **0.06275** | 0.07331 | 0 | 0; yes | — |
| resolved, stage 1 | W | `[251.326825, 251.390431]` | **0.06361** | 0.06975 | 0 | 0; yes | — |
| **resolved, stage 2** | W | `[251.332486, 251.380139]` | **0.04765** | 0.05678 | 0 | 0; yes | — |

**LKSE:5 (14 508 states, enumerated), order 4, band 2** — the models with all penalties zero (what the reductions cost; not a sandwich): 0.2042 nats.

| penalty | form | certified bracket of `ln Z` | width (nats) | `β ×` mean of `m₊ − m₋` on the check sample | sandwich violated at the 960 Gibbs states | violated at any state; exact `ln Z` inside | exact samples of the floor: sites off the anchor (mean); violations |
|---|---|---|---|---|---|---|---|
| P8's constants 'SAb' (the coordinator's recipe) | S | `[274.611132, 287.220745]` | **12.61** | 10.58 | 0 | 0; yes | — |
| joint maxima of stage 2 (constants) | S | `[274.776508, 283.027063]` | **8.251** | 7.265 | 0 | 0; yes | — |
| resolved, stage 1 | S | `[274.674935, 286.149441]` | **11.47** | 9.425 | 0 | 0; yes | — |
| **resolved, stage 2** | S | `[275.695202, 278.665290]` | **2.97** | 2.276 | 0 | 0; yes | — |
| P8's constants 'SAb' (the coordinator's recipe) | B | `[275.635403, 285.160333]` | **9.525** | 4.453 | 0 | 0; yes | — |
| joint maxima of stage 2 (constants) | B | `[275.742666, 281.264464]` | **5.522** | 3.095 | 0 | 0; yes | — |
| resolved, stage 1 | B | `[275.668766, 283.636913]` | **7.968** | 3.89 | 0 | 0; yes | — |
| **resolved, stage 2** | B | `[276.171745, 277.327682]` | **1.156** | 0.8765 | 0 | 0; yes | — |
| P8's constants 'SAb' (the coordinator's recipe) | T | `[275.702267, 284.675420]` | **8.973** | 3.693 | 0 | 0; yes | — |
| joint maxima of stage 2 (constants) | T | `[275.815861, 280.891182]` | **5.075** | 2.612 | 0 | 0; yes | — |
| resolved, stage 1 | T | `[275.735996, 282.978722]` | **7.243** | 3.267 | 0 | 0; yes | — |
| **resolved, stage 2** | T | `[276.180423, 277.269018]` | **1.089** | 0.8414 | 0 | 0; yes | — |
| joint maxima of stage 2 (constants) | W | `[276.403216, 278.011726]` | **1.609** | 0.2334 | 0 | 0; yes | — |
| resolved, stage 1 | W | `[276.402458, 279.939531]` | **3.537** | 0.243 | 0 | 0; yes | — |
| **resolved, stage 2** | W | `[276.417293, 276.622683]` | **0.2054** | 0.1705 | 0 | 0; yes | — |

### 4.5 Reading

**(i) Like for like — the form of the reference (T: equal shares on triples, band 7).**
Lys₁₂, order 5: 0.05669 (reference) → 0.0452 (stage 1) → **0.016** (stage 2), a
factor 3.5.  Lys₁₂, order 4: 1.413 → 0.3493 → **0.1115**, a
factor 13.  (LKSE)₃, order 5: 4.301 → 1.871 →
**0.1946**, a factor 22.  In the site and pair forms of stage 2:
0.1119 and 0.02058 (Lys₁₂, order 5; the reference has 0.4587 and 0.08487),
1.874 and 0.1853 (order 4; 10.56 and 3.096), 2.918 and
0.3009 ((LKSE)₃; the coordinator's log `occ_reduction_test_LKSEc12_H_m5_w7_SAb.log` has 22.58 and 10.83
for the reference; I did not re-run those two).  The three stopping
numbers of the brief — 0.0567, the order-4 number 1.4125, 4.30 — are beaten in the reference's
own form by factors 3.5, 13 and
22.

**(ii) The brief's first stage alone** (hosts resolved) is worth a factor 1.3 at
Lys₁₂ order 5 — the first-order regime, where the bracket follows the mean penalty and the
mean penalty moves by 23 % (§3.2) — and factors 4 at order 4 and
2.3 for (LKSE)₃, where the reference floor was delocalised (7.2 and
9.0 side chains off the anchor in its samples) and the stage-1 floor is not (1.3 for Lys₁₂).
**The dependence on the host's rotamer is weak, as §3.1 says; what stage 1 buys is the
threshold, not the slope.**

**(iii) With one sub-tuple per subset (form W)** the brackets are the penalty-free widths to
within a few per cent: Lys₁₂ order 5 **0.007233** `[517.125705, 517.132938]`
(reductions alone 0.007133); order 4 **0.007347** `[517.125649, 517.132996]`
(0.007132); (LKSE)₃ order 5 **0.01699** `[655.604050, 655.621038]`
(0.0167).  Against the three stopping numbers: factors 7.8,
192, 253.  The allocation alone — W with P8's
constants — gives 0.007286 at Lys₁₂ order 5 (constants small: enough), 0.7207 at
order 4 (floor delocalised: not enough) and 1.311 for (LKSE)₃; with the joint maxima
of stage 2 as *constants* 0.01024 at order 4 and 0.03933 for (LKSE)₃.
**Lys₁₂ is certified at order 4 — from 96 366 evaluations — 7.7 times
more tightly than the reference at order 5 with 1 621 056**; for comparison, the coordinator's
nested sampler on the order-4 reference sandwich reaches 0.0060 nats at probability 0.95 with
12 000 further evaluations (`[517.125561, 517.131531]`: its two-end form with empirical Bernstein;
0.032 as the theory division states the bound; addendum A17 (18) item 62) — the
deterministic bracket is 0.007347 with none, and the two intervals overlap.  **(LKSE)₃, the sequence that was "reachable by sampling and not
deterministically", is certified deterministically within 0.01699 nats**; the
coordinator's sampled interval (`[655.592089, 655.632643]`, 0.041 nats at probability 0.95, two-end
form with empirical Bernstein) contains my bracket.

**(iv) Where the predictions were wrong** (§4.1).  Wherever the floor stays at the anchor,
"penalty-free width + `2β⟨pen⟩` on the Gibbs sample" predicted the certified bracket within a
few per cent (every line of Lys₁₂ at order 5 within 3 %, of Ser₁₂ within 8 %; the stage-2 lines of
Lys₁₂ at order 4 and of (LKSE)₃ within a factor 1.6 — the equal-share forms 22–38 % below my guess, the window form within 2 % of it).  The two errors that matter are about
the floor: (a) I assumed that a delocalised reference floor stays delocalised under stage-1
tables (predicted 0.75 and 3.3 nats; found 0.3493 and 1.871); (b) I assumed that the
window form with P8's constants would be "first order plus a little" (Lys₁₂ order 4: predicted
0.02, found 0.7207, its floor at 6.6 side chains off the anchor; (LKSE)₃: predicted 0.15,
found 1.311, floor at 9.4).  In both cases the
number on the Gibbs sample was right about the sample and silent about the floor, as Lemma
A17.16 says it must be; I have no rule that says on which side of the threshold a set of
tables lies before the model is built (request P9-T2).

**(v) What the brackets now consist of.**  At the window form of stage 2 the penalties
contribute 0.007233 − 0.007133 and 0.007347 − 0.007132 nats for Lys₁₂ and
0.01699 − 0.0167 for (LKSE)₃: one to three per cent of the bracket.  The rest is
the reductions — the ten pairs of side chains beyond the band and the evaluated terms that
do not fit a window — which this workstream did not touch.

## 5. Second stage and stretch

The brief's item 5 has two parts — resolve the non-host sites too; unequal weights — and both
are in §1–§4: "stage 2" is the first, the window form W the second.  This section says what
each contributes alone, and reports what lies beyond the three brackets the brief asked for.

### 5.1 What each lever contributes alone [M]

| instance, order (ball) | penalty | S | B | T (equal shares: the form of the reference) | W (one in-window sub-tuple per subset) | reductions alone |
|---|---|---|---|---|---|---|
| Lys₁₂, 5 (1 621 056) | P8's constants | 0.4587 | 0.08487 | 0.05669 (floor: 1.2 sites off) | 0.007286 (floor: 1.2 sites off) | 0.007133 |
| Lys₁₂, 5 (1 621 056) | joint maxima of stage 2 (constants) | not run | not run | 0.02934 | 0.007259 | 0.007133 |
| Lys₁₂, 5 (1 621 056) | resolved, stage 1 | 0.3741 | 0.06562 | 0.0452 (floor: 1.2 sites off) | 0.007261 | 0.007133 |
| Lys₁₂, 5 (1 621 056) | **resolved, stage 2** | **0.1119** | **0.02058** | **0.016** (floor: 1.2 sites off) | **0.007233** (floor: 1.2 sites off) | 0.007133 |
| Lys₁₂, 4 (96 366) | P8's constants | 10.56 | 3.096 | 1.413 (floor: 7.2 sites off) | 0.7207 (floor: 6.6 sites off) | 0.007132 |
| Lys₁₂, 4 (96 366) | joint maxima of stage 2 (constants) | not run | not run | 0.2621 | 0.01024 | 0.007132 |
| Lys₁₂, 4 (96 366) | resolved, stage 1 | 6.879 | 0.7253 | 0.3493 (floor: 1.3 sites off) | 0.01034 | 0.007132 |
| Lys₁₂, 4 (96 366) | **resolved, stage 2** | **1.874** | **0.1853** | **0.1115** (floor: 1.2 sites off) | **0.007347** (floor: 1.2 sites off) | 0.007132 |
| Lys₁₂, 3 (3 841) | joint maxima of stage 2 (constants) | not run | not run | not run | 238 | 0.007104 |
| Lys₁₂, 3 (3 841) | resolved, stage 1 | not run | not run | not run | 117.8 | 0.007104 |
| Lys₁₂, 3 (3 841) | **resolved, stage 2** | not run | not run | **0.832** | **0.07686** (floor: 1.3 sites off) | 0.007104 |
| (LKSE)₃, 5 (3 471 783) | P8's constants | not run | not run | 4.301 (floor: 9.0 sites off) | 1.311 (floor: 9.4 sites off) | 0.0167 |
| (LKSE)₃, 5 (3 471 783) | joint maxima of stage 2 (constants) | not run | not run | 1.129 | 0.03933 | 0.0167 |
| (LKSE)₃, 5 (3 471 783) | resolved, stage 1 | not run | not run | 1.871 | 0.04057 | 0.0167 |
| (LKSE)₃, 5 (3 471 783) | **resolved, stage 2** | **2.918** | **0.3009** | **0.1946** (floor: 2.9 sites off) | **0.01699** (floor: 2.8 sites off) | 0.0167 |
| (LKSE)₃, 4 (181 268) | joint maxima of stage 2 (constants) | not run | not run | not run | 157 | 0.01669 |
| (LKSE)₃, 4 (181 268) | resolved, stage 1 | not run | not run | not run | 166.5 | 0.01669 |
| (LKSE)₃, 4 (181 268) | **resolved, stage 2** | not run | not run | **1.147** (floor: 3.4 sites off) | **0.0191** (floor: 2.8 sites off) | 0.01669 |
| (LKSE)₃, 3 (6 083) | **resolved, stage 2** | not run | not run | **660** | **658.9** (floor: 12.0 sites off) | 0.01623 |
| Ser₁₂, 5 (481 506) | P8's constants | not run | not run | 0.05469 | 0.02259 | 0.009096 |
| Ser₁₂, 5 (481 506) | joint maxima of stage 2 (constants) | not run | not run | 0.03979 | not run | 0.009096 |
| Ser₁₂, 5 (481 506) | resolved, stage 1 | not run | not run | 0.05064 | not run | 0.009096 |
| Ser₁₂, 5 (481 506) | **resolved, stage 2** | not run | not run | **0.02256** (floor: 6.3 sites off) | **0.01169** (floor: 6.3 sites off) | 0.009096 |

*Reading.*  (i) **The allocation alone is not enough where the constants are large.**  The
window form with P8's constants leaves Lys₁₂ at order 4 at 0.72 nats: its floor delocalises
(6.6 of 12 side chains off the anchor in its samples).  (ii) **Constants below the threshold,
and it works — even state-independent ones:** the joint maxima of stage 2 (`βΓ₄ = 18.2`
instead of 34.0), still constants, give 0.0102 in the same form.  (iii) **Resolution by state
then takes the bracket to the reductions**, and takes the equal-share forms down by the
first-order ratio of §3.2.  (iv) Stage 1 — the brief's first stage — is worth 20 % of the
T bracket in the first-order regime (Lys₁₂ order 5: 0.0567 → 0.0452) and a factor four where
the reference floor was delocalised (order 4: 1.41 → 0.35): the reference at order 4 was
beyond a threshold, not on a slope.  (v) **One order further down only the fully resolved
tables keep the floor at the anchor** (§5.2): (LKSE)₃ at order 4 and Lys₁₂ at order 3 have
window-form brackets of 0.019 and 0.077 nats with stage 2 and of more than a hundred nats
with stage-1 tables or with constants.

### 5.2 One order earlier — and two [M; validity P; predictions 3 and 4 of §4.1]

**(LKSE)₃, ORDER 4, band 7 (ball 181 268) — an order at which no certificate had been attempted** — the models with all penalties zero (what the reductions cost; not a sandwich): 0.01669 nats.

| penalty | form | certified bracket of `ln Z` | width (nats) | `β ×` mean of `m₊ − m₋` on the check sample | sandwich violated at the 960 Gibbs states | exact samples of the floor: sites off the anchor (mean); violations |
|---|---|---|---|---|---|---|
| **resolved, stage 2** | T | `[655.203848, 656.350724]` | **1.147** | 1.054 | 0 | 2000 samples: 3.45; 0 |
| joint maxima of stage 2 (constants) | W | `[655.449624, 812.459249]` | **157** | 0.7997 | 0 | — |
| resolved, stage 1 | W | `[655.452259, 821.956407]` | **166.5** | 0.7382 | 0 | — |
| **resolved, stage 2** | W | `[655.603013, 655.622116]` | **0.0191** | 0.01976 | 0 | 2000 samples: 2.82; 0 |

**Lys₁₂, ORDER 3, band 7 (ball 3 841)** — the models with all penalties zero (what the reductions cost; not a sandwich): 0.007104 nats.

| penalty | form | certified bracket of `ln Z` | width (nats) | `β ×` mean of `m₊ − m₋` on the check sample | sandwich violated at the 960 Gibbs states | exact samples of the floor: sites off the anchor (mean); violations |
|---|---|---|---|---|---|---|
| **resolved, stage 2** | T | `[516.827371, 517.659419]` | **0.832** | 0.7827 | 0 | — |
| joint maxima of stage 2 (constants) | W | `[517.064798, 755.046155]` | **238** | 0.4908 | 0 | — |
| resolved, stage 1 | W | `[517.058972, 634.904208]` | **117.8** | 0.389 | 0 | — |
| **resolved, stage 2** | W | `[517.108870, 517.185731]` | **0.07686** | 0.06935 | 0 | 2000 samples: 1.30; 0 |

**(LKSE)₃, ORDER 3, band 7 (ball 6 083)** — the models with all penalties zero (what the reductions cost; not a sandwich): 0.01623 nats.

| penalty | form | certified bracket of `ln Z` | width (nats) | `β ×` mean of `m₊ − m₋` on the check sample | sandwich violated at the 960 Gibbs states | exact samples of the floor: sites off the anchor (mean); violations |
|---|---|---|---|---|---|---|
| **resolved, stage 2** | T | `[654.530095, 1314.530025]` | **660** | 4.254 | 0 | — |
| **resolved, stage 2** | W | `[655.483269, 1314.417980]` | **658.9** | 0.4026 | 0 | 2000 samples: 12.00; 0 |

*Reading.*  None of these orders had a certificate: P8's constants are `βΓ₄ = 296` for
(LKSE)₃ and `βΓ₃ = 375`, `1 660` for the two peptides (P8's code path, run here; P8 stored
constants from order 4 on), and with them the equal-share triple form has first-order
numbers of 2.7–52 nats and exponential estimates of 16–360 nats on the Gibbs sample
(`logs/gain_LKSEc12_H_0.60_m4_w7.log`, `gain_K12_H_0.70_m3_w7.log`, `gain_LKSEc12_H_0.60_m3_w7.log`; not
run as models).

**(LKSE)₃ at order 4 — 181 268 evaluations instead of 3 471 783 — is certified within
0.0191 nats**, `[655.603013, 655.622116]` (reductions alone 0.01669; floor at
2.8 side chains off the anchor, the ensemble's own value).  The order-5 bracket lies
inside it, and both inside the coordinator's sampled interval.  **Here the second stage is
not an improvement but the difference between a certificate and none**: the same window form
gives 166.5 nats with stage-1 tables and 157 with the joint maxima of stage 2 as
constants — both floors delocalise — and the equal-share triple form of stage 2 gives
1.147.

**Lys₁₂ at order 3 — 3 841 evaluations — is certified within 0.07686 nats**,
`[517.108870, 517.185731]` (reductions alone 0.007104; floor at 1.3 side chains
off the anchor); the triple form of stage 2 gives 0.832, the window form 117.8 with
stage-1 tables and 238 with constants.  For comparison (the coordinator's numbers):
the reference certificate of this peptide is 1.41 nats at order 4 (96 366 evaluations) and
0.0567 at order 5 (1 621 056).  Workstream P8's first-order *estimates* for this order with **exact** state-independent
constants were 0.54 nats in the banded triple form and 0.024 with all triples charged in a
window (its §4.1, row "exact3", band 6, reductions not included); the resolved **bounds** are
certified at 0.832 and 0.07686 in the corresponding forms — within a factor 1.5–3.5 of what
exact constants were estimated to give.

**(LKSE)₃ at order 3 — 6 083 evaluations —** there the method stops: the window form of stage 2 gives 658.9 nats and the triple form 660 — its floor has all twelve side chains off the anchor (12.0 on average in its samples) — although the first-order number on the Gibbs sample is 0.39 nats.  The patterned sequence is certified from order 4 on, not from order 3.

*Against the predictions* (3 and 4 of §4.1).  The two window-form brackets I hoped for came
out as predicted or better ((LKSE)₃ order 4: 0.02 predicted, 0.0191 found; Lys₁₂ order 3:
0.12 predicted with an even chance of failure, 0.07686 found); the equal-share triple form
at order 3 of Lys₁₂, which I had written off ("more than 2"), gives 0.832.  Of the nine
predictions of this workstream that were about a floor I was too pessimistic three times
(T with stage-1 tables at Lys₁₂ order 4 and (LKSE)₃ order 5; T with stage-2 tables at Lys₁₂
order 3), too optimistic twice (the window form with P8's constants, twice), and right four
times, two of them with a stated risk of 40–50 % — I cannot predict it.

### 5.3 A look at the neutral, mobile case: Ser₁₂ [M; outside the brief; why: to know whether the lever is specific to charged, mostly frozen side chains]

Ser₁₂ is the opposite ensemble: every side chain is off the anchor about half of the time
(6.4 of 12 on average), nothing is frozen, and P8's state-wise constants gain only a factor
1.6–1.8 there (P8_REPORT §3.5).  Tables: `p9_03_tables.py S12 5` (197 s); first-order numbers: `p9_04_gain.py S12 5`;
random-state check: `p9_06_check12.py S12 5 --noa` (2 000 states, no violation, smallest ratio
10.3, control 3 violations); brackets: `p9_05_brackets.py S12 5 7 --pairs … --label X` (26 s,
0.36 GB).  `βΓ₅`: P8's 'SAb' 0.1381 (re-computed, equal to P8's stored values); joint maxima of
stage 2: 0.0925; sum of the medians over the states: 0.0107.

**Ser₁₂, order 5, band 7 (ball 481 506)** — the models with all penalties zero (what the reductions cost; not a sandwich): 0.009096 nats.

| penalty | form | certified bracket of `ln Z` | width (nats) | `β ×` mean of `m₊ − m₋` on the check sample | sandwich violated at the 960 Gibbs states | exact samples of the floor: sites off the anchor (mean); violations |
|---|---|---|---|---|---|---|
| P8's constants 'SAb' (the coordinator's recipe) | T | `[227.341786, 227.396479]` | **0.05469** | 0.05474 | 0 | — |
| joint maxima of stage 2 (constants) | T | `[227.349132, 227.388924]` | **0.03979** | 0.03972 | 0 | — |
| resolved, stage 1 | T | `[227.343781, 227.394418]` | **0.05064** | 0.05062 | 0 | — |
| **resolved, stage 2** | T | `[227.357675, 227.380236]` | **0.02256** | 0.02237 | 0 | 2000 samples: 6.34; 0 |
| P8's constants 'SAb', my chains | W | `[227.357722, 227.380312]` | **0.02259** | 0.02291 | 0 | — |
| **resolved, stage 2** | W | `[227.363089, 227.374782]` | **0.01169** | 0.01154 | 0 | 2000 samples: 6.33; 0 |

*Reading.*  The lever is not specific to charged, mostly frozen side chains: the equal-share
triple form falls from 0.0547 (P8's constants) to 0.0226 nats, the window form from 0.0226
to 0.0117, of which 0.0091 are the reductions.  The coordinator's published bracket for this
peptide, with workstream P3's closed-form constants, is 0.0872 nats
(`[227.325848, 227.413092]`, addendum A17 (18), item 61); every bracket of the table lies inside
it.  The gain is smaller than for lysine because a mobile ensemble visits many rotamers, not
the ones near the anchor only; all five predictions for this peptide (prediction 5 in
`NOTES.md`: 0.0091, 0.054, 0.021, 0.022, 0.011) were within 8 % — a first-order regime
throughout.

### 5.4 Stretch: the nested sampler with the resolved envelope [M; the algorithm is the theory division's Proposition 11.113a, the driver the coordinator's]

The brief: for (LKSE)₃ the sampler's cost is the envelope's own bracket, 1.23 nats with P8's
constants; the fully resolved `Σ_{T⊆S(x)} Θ²_T(x_T)` is a valid envelope (Theorem R); estimate
its cost per proposal first.

**Cost, estimated before anything was built** (`NOTES.md`, 11:26; a scratch timing, not a cited
log).  The envelope is a sum of 792 table look-ups: 36 microseconds per state at uniformly
random states — 14 s for 400 000 proposals.  What costs is the proposals themselves: with an
outer bracket `D` the rejection step keeps a fraction `1 − e^{−D}` of the exact draws of the
floor, so the tighter the outer sandwich, the more draws a proposal costs (24 million draws
for 400 000 proposals at `D = 0.017`).

**Driver.**  `p9_07_nested.py` calls the coordinator's `nested_sampler.main()` unchanged, with the
outer sandwich of the window form of stage 2 and an envelope object that reads the stored
tables `Θ²_T` (`p9_03_tables.py --keeptabs`); the inner sandwich, its clipping and its
allowances are the coordinator's.  The envelope object reproduces the envelope accumulated
by the table run at the 960 Gibbs states to `3·10⁻²⁰` kcal/mol (from the same scratch run as
the timing: recorded in `NOTES.md`, not a cited log).

**(A) (LKSE)₃, order 5** (`logs/nested_LKSEc12_H_m5_w7.log`; 471 s, peak RSS 2736 MB).
Outer sandwich `[655.604050, 655.621038]`, `D = 0.01699` — the bracket of §4.3 rebuilt by this
driver.  400 000 proposals from 23 718 047 exact draws of the floor
(45 685 distinct states).  **The resolved envelope's own bracket, estimated from the
proposals: 3.48e-06 nats** (P8's constants: 1.23); mean `ρ = 0.000205`:
90 proposals accepted for evaluation, 90 evaluated; evaluated energy outside
the inner sandwich at 0, outside the outer at 0; clipping active at
0 proposals, inconsistent at 0.  With probability at least 0.95, given the two
sandwiches:

| bound | interval for `ln Z` | width (nats) |
|---|---|---|
| as stated by the theory division (Hoeffding) | `[655.612610, 655.612778]` | 0.00017 |
| two-end form (Hoeffding) | `[655.612652, 655.612736]` | 8.5e-05 |
| as stated, empirical Bernstein | `[655.612672, 655.612716]` | 4.4e-05 |
| **two-end form, empirical Bernstein** | `[655.612673, 655.612715]` | **4.3e-05** |

*Against what I had written before the run* (`NOTES.md`, 11:26): width about `1.7·10⁻⁴` "as stated"
— found 0.00017; "fewer than ten evaluations" — found 90.  That guess was wrong twice
over: my own rule `ρ ≈ (envelope bracket)/D` with my own input (`10⁻⁶/0.017`) gives 24 of 400 000,
not "fewer than ten" (a slip of arithmetic); and the envelope's bracket under the proposals is
3.48e-06, two to three times its first-order numbers on the two Gibbs samples of the true
ensemble (`1.2·10⁻⁶` and `1.6·10⁻⁶`, §3.2) — the rule itself holds (mean `ρ = 0.000205` is
3.48e-06`/D`).  How much of that factor is the inner sandwich's own allowances and how much
the different distribution of the proposals I did not separate.  *Against the coordinator's run for this `ln Z`* with
P8's constants (`pi_inference/nested_sampler_LKSEc12_H_m5_w7_T_window_SAb_occ.log`; theirs: 4 000 000
proposals, 12 000 evaluations): 0.188 nats as stated (Hoeffding) and 0.041 in the two-end form
with empirical Bernstein (`[655.592089, 655.632643]`, the interval quoted in addendum A17 (18)) —
here 0.00017 and 4.3e-05 in the same two forms, from a tenth of the proposals and
90 evaluations; their two-end interval contains 6 of the 6 intervals the
driver prints for my run (four of them are in the table).  The plain sampler with the same
90 evaluations (printed by the coordinator's driver) is 29–151 times wider.  What limits the result
now is the number of proposals, and each proposal costs `1/(1 − e^{−D})` = 59 exact draws of the
floor: 363 of the 471 seconds (request P9-E5).

**(B) (LKSE)₃ from the ORDER-4 ball** (181 268 evaluations; `logs/nested_LKSEc12_H_m4_w7.log`;
323 s, peak RSS 1512 MB).  Outer sandwich `[655.603013, 655.622116]`,
`D = 0.0191` (the bracket of §5.2); 400 000 proposals from 21 195 687 draws;
envelope bracket estimated from the proposals: 0.000727 nats; mean `ρ = 0.0381`:
15158 proposals accepted for evaluation, 1200 evaluated; evaluated energy
outside the inner sandwich at 0, outside the outer at 0; clipping
active at 0, inconsistent at 0.  With probability at least 0.95: as stated
(Hoeffding) `[655.612562, 655.612814]`, width **0.00025**; two-end, empirical
Bernstein `[655.612657, 655.612719]`, width 6.2e-05.  *Reading.*  What I had written before the run (`NOTES.md`, 11:47): "2–3·10⁻⁴ as stated, up to 1 200
evaluations" — found 0.00025 with 1200 (the cap I had set: 15158 proposals were
accepted for evaluation and the driver evaluates the first 1200; 1072 distinct states).
*The two runs against each other:* the interval from the order-4 ball contains the interval of the
same kind from the order-5 ball in 6 of the 6 forms the driver prints; 6 of the
6 order-4 intervals lie inside the deterministic bracket of order 5, and 6
inside the coordinator's two-end interval.  At this order the envelope is no longer negligible
(its own bracket 0.000727 nats; mean `ρ = 0.0381`): the evaluations carry 26 % of the
half-width "as stated", and the plain sampler with the same 1200 evaluations is
5.9–17 times wider (order 5: 29–151 times).  In evaluations of the
model function: 181 268 + 1200 here, 3 471 783 + 90 in run (A), 3 471 783 + 12 000 in the
coordinator's run.

**(C) Lys₁₂ from the order-3 ball: not run.**  The deterministic bracket there is 0.077 nats
(§5.2) and the resolved envelope is not small (first-order number 0.053 on the Gibbs sample),
so a sampler would have something to do: with 12 000 evaluations I expect about `2·10⁻³` nats
"as stated" from 3 841 + 12 000 evaluations in all (written at 11:47, before any sampler run).
I did not run it because the band-7 model of Lys₁₂ together with the sampler's stored
messages peaks near 2.9 GB (the coordinator's own Lys₁₂ sampler log: 2 877 MB), too close to
the 3 GB limit of this workstream.  It is one command (`p9_07_nested.py K12 H 3 7 W window --N 12000
--Nf 400000`) for whoever may use the memory.

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

## 7. How to re-run (one command per number)

Everything is in `experiments/science/ws_P9/`; run from that directory with
`export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1` and `python3 -B`.  Nothing
is written outside `ws_P9/` (the library `p9lib.py` guards the imports of the other
workstreams' modules; every log ends with the number of foreign writes attempted — 0 in
every run — and with its peak resident memory, printed as `ru_maxrss/1024` and called "MB"
there: mebibytes; where this section says GB it is a thousand of those).  Read-only inputs: P8's cached balls
`ws_P8/cache/ball_*`, P8's stored constants `ws_P8/out/g12b_*.npz`, `bc_*.json`, P8's stored
enumerations (comparison only).  `.npz`/`.npy` files are regenerable and may be ignored by git —
`cache/` is 0.52 GB (redirected caches of P3's evaluator, enumerations, Gibbs samples, the
stored tables `Θ²_T` that the sampler driver reads) and `out/*.npz` 0.64 GB (the tables the
bracket driver reads); `out/*.json`, `logs/*.log`, the scripts, `NOTES.md` and `report_parts/` are
the record (about 1.5 MB).

| what | command | log | time, peak RSS |
|---|---|---|---|
| probe: P8's constants reproduced, first look | `p9_00_probe.py K4` | `logs/probe_K4_H_0.70.log` | 2 s, 0.15 GB |
| consistency of the two-stage resolver with P8's code | `p9_00b_consistency.py K4`; `p9_00b_consistency.py K12 --m 5 --sample 4` | `logs/consistency_K4_H_0.70.log`, `consistency_K12_H_0.70_m5.log` | 2 s; 23 s, 0.46 GB |
| **validation by enumeration** (§2) | `p9_01_validate.py K4`; `… LKSE:5`; `… K5` | `logs/validate_K4_H_0.70.log`, `validate_LKSEc5_H_0.60.log`, `validate_K5_H_0.70.log` | 12 s; 16 s; 229 s, 1.6 GB |
| Gibbs samples (seeds 4242, 777) | `p9_02_gibbs.py K12`; `… LKSE:12`; `… K5` | `logs/gibbs_*.log` | 3–4 min; 2.5 min; 26 s |
| **tables**, both stages (§3) | `p9_03_tables.py K12 4 --keeptabs`; `p9_03_tables.py K12 5 --keeptabs`; `p9_03_tables.py LKSE:12 5 --part 0 2 --keeptabs`, `… --part 1 2 --keeptabs`, `… --merge 2`; `p9_03_tables.py LKSE:12 4 --keeptabs`; `p9_03_tables.py K12 3 --keeptabs`; `p9_03_tables.py LKSE:12 3 --keeptabs`; `p9_03_tables.py K5 4 --w 2`, `K5 4 --w 3`, `K5 5 --w 3` | `logs/tables_*.log` | 87 s; 378 s; 231 s + 249 s (+ 1 s for the merge); 81 s; 29 s; 19 s; 3 s each; at most 1.1 GB |
| gain on the Gibbs samples (§3.2) | `p9_04_gain.py K12 4`; `K12 5`; `LKSE:12 5`; `LKSE:12 4`; `K12 3`; `LKSE:12 3` | `logs/gain_*.log` | 1–2 s |
| **certified brackets** (§4) | `p9_05_brackets.py K12 4 7 --sources ref,s1 --forms S,B,T,W --floor ref:T,s1:T --label A`; `p9_05_brackets.py K12 4 7 --pairs s2:S,s2:B,s2:T,s2:W,sab:W,cJ2:T,cJ2:W --floor s2:T,s2:W,sab:W --label B`; `p9_05_brackets.py K12 5 7 --pairs ref:S,ref:B,ref:T,s1:S,s1:B,s1:T,s1:W --floor ref:T,s1:T --label A` and the same `--label B` line with `K12 5 7`; `p9_05_brackets.py LKSE:12 5 7 --pairs ref:T,s1:T,s1:W,s2:S,s2:B,s2:T,s2:W,sab:W,cJ2:T,cJ2:W --floor ref:T,s2:T,s2:W,sab:W --label A` | `logs/brackets_<tag>_m<m>_w7_A.log`, `…_B.log` | see the list below |
| the extra orders and Ser₁₂ (§5.2, §5.3) | `p9_05_brackets.py LKSE:12 4 7 --pairs s2:W,s2:T,s1:W,cJ2:W --floor s2:W,s2:T --label X`; `p9_05_brackets.py K12 3 7 --pairs s2:W,s2:T,s1:W,cJ2:W --floor s2:W --label X`; `p9_05_brackets.py LKSE:12 3 7 --pairs s2:W,s2:T --floor s2:W --label X`; `p9_02_gibbs.py S12`, `p9_03_tables.py S12 5 --keeptabs`, `p9_05_brackets.py S12 5 7 --pairs ref:T,s2:T,sab:W,s2:W,cJ2:T,s1:T --floor s2:W,s2:T --label X` | `logs/brackets_<tag>_m<m>_w7_X.log` | see the list below |
| brackets on Lys₅ with **every state** checked | `p9_05_brackets.py K5 4 2 --enum --sources ref,sab,cJ2,s1,s2 --forms S,B,T,W`; `… K5 4 3 --enum …`; `… K5 5 3 --enum …` | `logs/brackets_K5_H_0.70_m4_w2.log`, `_m4_w3.log`, `_m5_w3.log` | 6–7 s, 0.25 GB |
| checks at twelve residues (§3.4) | `p9_06_check12.py K12 4`; `K12 3`; `K12 5 --noa`; `LKSE:12 4`; `LKSE:12 3`; `LKSE:12 5 --noa`; `S12 5 --noa`; and at order 5 `p9_06_check12.py K12 5 --noa --nob --shell 20000`, `LKSE:12 5 --noa --nob --shell 20000` | `logs/check12_*.log`, `check12_*_shell.log` | 4–53 s, at most 1.4 GB |
| my chains with constants against the coordinator's forms, as functions (§4) | `p9_08_chaincheck.py K12 4`; `K12 5`; `LKSE:12 5` | `logs/chaincheck_K12_H_0.70_m4.log`, `_m5.log`, `chaincheck_LKSEc12_H_0.60_m5.log` | under 1 s each |
| enumerated brackets for LKSE:5 (§4.4) | `p9_02_gibbs.py LKSE:5`; `p9_03_tables.py LKSE:5 4 --w 2`, `LKSE:5 5 --w 2`; `p9_05_brackets.py LKSE:5 4 2 --enum --sources ref,cJ2,s1,s2 --forms S,B,T,W`, `… LKSE:5 5 2 --enum …` | `logs/brackets_LKSEc5_H_0.60_m4_w2.log`, `_m5_w2.log` | seconds |
| stretch: the nested sampler (§5.4) | `p9_07_nested.py LKSE:12 H 5 7 W window --N 1200 --Nf 400000 > logs/nested_LKSEc12_H_m5_w7.log`; `p9_07_nested.py LKSE:12 H 4 7 W window --N 1200 --Nf 400000 > logs/nested_LKSEc12_H_m4_w7.log` (both need the tables stored by `p9_03_tables.py … --keeptabs`) | `logs/nested_*.log` | see §5.4 |
| the tables of this report | `mk_tables.py`, then `mk_report.py` | — | 1 s |

Times and peak resident memory of the twelve-residue bracket runs (last lines of their logs):
`K12_H_0.70_m3_w7_X`: 146 s, 1899 MB; `K12_H_0.70_m4_w7_A`: 235 s, 1938 MB; `K12_H_0.70_m4_w7_B`: 316 s, 1939 MB; `K12_H_0.70_m5_w7_A`: 411 s, 2384 MB; `K12_H_0.70_m5_w7_B`: 511 s, 2405 MB; `LKSEc12_H_0.60_m3_w7_X`: 60 s, 958 MB; `LKSEc12_H_0.60_m4_w7_X`: 184 s, 1043 MB; `LKSEc12_H_0.60_m5_w7_A`: 572 s, 1958 MB; `S12_H_0.70_m5_w7_X`: 26 s, 359 MB.

Logs of stopped, failed or superseded runs — none is cited — are in `not_cited/`:
`not_cited/brackets_K12_H_0.70_m3_w7_X_failed_no_stored_constants.log`,
`not_cited/brackets_LKSEc12_H_0.60_m3_w7_X_failed_no_stored_constants.log`,
`not_cited/chain_orders_screen_output_with_the_two_failed_order3_runs.stdout`,
`not_cited/consistency_K12_H_0.70_m5_first_cross_version.log`,
`not_cited/consistency_K12_m5_first_cross_version.stdout`,
`not_cited/consistency_K4_H_0.70_first_cross_version.log`,
`not_cited/gain_K12_H_0.70_m4_w7_first_version.log`,
`not_cited/probe_K4_H_0.70_first_library_version.log`,
`not_cited/validate_K4_H_0.70_first_cross_version.log`,
`not_cited/validate_K4_H_0.70_run1_block_order_bug.log`,
`not_cited/validate_K5_H_0.70_first_cross_version.log`,
`not_cited/validate_K5_first_cross_version.stdout`,
`not_cited/validate_LKSEc5_H_0.60_first_cross_version.log`.

Files named `logs/*.stdout` are the captured screen output of chained runs (the same lines
as the `.log` files of the scripts they ran); they are not cited.

## 8. Not settled; not checked; my own errors

### Not settled

1. **Nothing here is refereed or machine-checked, and no run by anyone else is part of it.**  Theorem R
   is P8's Theorem AH with its last step left out and P3's Theorem 3 with the increments it is
   stated with; Proposition P is elementary.  The brackets are outputs of the pipeline's modules
   fed with tables of mine through a driver of mine (requests P9-E1, P9-E2, P9-T1).
2. **The reductions are the bracket.**  With the window form of stage 2 the bracket of Lys₁₂ is
   the penalty-free width (0.0071 nats) plus 1–3 % at orders 4 and 5; for (LKSE)₃ likewise at
   order 5 (0.0167), and plus 14 % at order 4 (§4, §5.2).  What the band gives up — ten far pairs, the evaluated terms that do not fit a window —
   is now the whole certificate (request P9-E3).  I did not touch the reductions.
3. **When a floor delocalises** is not predicted by anything I have: first-order numbers on a
   sample of the true ensemble are right within 10 % wherever the floor stays at the anchor,
   and wrong by any factor where it does not (0.012 against 0.72; 0.07 against 1.31; 0.4
   against 659 for (LKSE)₃ at order 3).  The outcome of a model run is the only test I can
   offer (request P9-T2).  **(LKSE)₃ at order 3 is not certified** (§5.2).
4. **The slack that is left** in the resolved bound: at twelve residues it is still 8–15 times
   the exact term at its tightest state and several hundred times at the median state with
   four side chains off the anchor (§3.4); on the enumerated instances its Boltzmann mean is
   255–880 times the true remainder's (stage 1: `4·10³`–`3·10⁵`; P8's constants, by the
   coordinator's logs: `9·10³`–`4·10⁵`).  What remains is the sign-blind class (P5) and the suprema over hulls taken
   over all contexts — a context-resolved hull (the hull of `I_p` given the states of the sites
   of `T`, not over everything) is the next resolution of the same kind; not tried.
5. **Longer chains.**  No closed form over the subsets; 0.15–0.6 s per subset; the hybrid of
   request P9-E4 is not run; nothing beyond twelve residues was computed.
6. **Unequal weights beyond "one sub-tuple per subset".**  The window form puts the whole
   weight of a subset on one sub-tuple chosen by a product-of-marginals estimate from an
   uncertified sample.  The convex optimum over allocations (the coordinator's Frank–Wolfe
   at the site level, addendum A17 (17)) at the level of windows with state-dependent tables
   was not attempted.
7. **Other sequences.**  Serine (mobile, neutral): one order, six rows (§5.3); leucine not
   at all (two states per site: stage 1 has nothing to resolve there, stage 2 has).
8. **The sampler** (§5.4): one run per case, one seed; the Lys₁₂ order-3 run was not made
   (memory); a proposal costs 59 exact draws of the floor at `D = 0.017`.

### Not checked

* **No proof was machine-checked.**  I re-derived P3's Corollaries L1, L2 and Remark L3 from
  P3_REPORT §2.2 and P8's Theorem AH from P8_REPORT §3.3; I did not re-derive P3's Lemma 2
  (the multilinear interpolation argument) beyond reading it.
* **P3's interval enclosures, hulls, the table allowance `PAD_TAB` and the factor `1 + 10⁻⁹`** are
  inherited unexamined, as in every certificate of the division.  My only additions to the
  arithmetic: per-state increments (`PAD_TAB` added wherever P3's maximal increment is non-zero,
  so that the maximum over the states *is* P3's value — asserted bit for bit in the code), sums,
  products and maxima of non-negative doubles, and one more factor `1 + 10⁻⁹` on every table
  entry.  The rounding argument for that last factor is a sentence in §1, not a proof.
* **The stage-2 evaluation exists in one implementation.**  It is tied to P8's code by two
  identities (maxima of stage 1 = P8's block constants; stage 2 with maximal increments =
  stage 1, to `9·10⁻¹⁶`), validated block by block at every state of three enumerated instances
  (smallest ratio 1.0034), and at twelve residues by necessary conditions only (§3.4): every
  state with exactly three or four side chains off the anchor (orders 3, 4), 20 000 random
  states with exactly five (order 5, where no ball of radius 5 exists), and 2 000–2 500
  uniformly random states per peptide and order.
* **The sandwiches at twelve residues** were checked at 960 Gibbs states of the true ensemble
  and, for the forms named in the tables of §4, at 2 000 exact samples of the floor — not at
  every state.  On Lys₅ and LKSE:5 every sandwich was checked at every state, with the exact
  `ln Z` inside (87 sandwiches).  The probability statements of §5.4 are "given the two
  sandwiches", as in the coordinator's runs; the sampler's code is the coordinator's and I
  read only its docstring, `Envelope`, `inner_bounds`, `draw_q` and `main`.
* **The whole-function check has no power for stage 1** (§2): a stage-1 table wrong by a
  factor two would pass it.  Stage 1 rests on the block-level check and on "envelope ≤ table".
* **The "self-test" of my remainder routine is not independent** (§2).
* **The Gibbs samples are uncertified**; they guide the reductions of the models (as in the
  coordinator's runs, same seeds) and my choice of sub-tuples in the window form.  Validity
  does not depend on them; the numbers do.  16 chains in all, 120 sweeps each.
* **My chains with state-independent constants equal the coordinator's forms** to every printed
  digit of the brackets on Lys₅ (three runs).  At twelve residues only the coordinator's recipe
  itself was run as a model for P8's constants (rows "ref"); my chain was compared with it
  there as a penalty *function* at 5 000 random states per case (§4, agreement to `2.5·10⁻¹⁰`
  relative), not through a model, and the brackets of the rows "joint maxima of stage 2" have
  no second driver behind them.
* **One anchor per instance, the helix, P2's pruned domain, band 7, two twelve-residue
  peptides** (plus Ser₁₂ at order 5).  No other band, backbone or sequence.
* **At order 3 "P8's constants" are P8's code path run by me**; P8 stored no per-subset
  constants at that order for twelve residues, so there is nothing of P8's to compare with.
* **Scripts were extended between runs** (options added to `p9_05_brackets.py` — an explicit list
  of pairs, a fallback when P8 stored no constants — and a third check to `p9_06_check12.py`).
  The runs made before those edits were not repeated with the final scripts; the code they
  exercised did not change.  The library `p9lib.py`: its bound and table code was last changed
  at 10:54 (session record), before every table run; at 11:00 two functions were appended
  (`off_frequencies`, `window_form_const`: the window form with constants, used by the gain and
  bracket scripts only) — the table runs of Lys₁₂ at orders 4 and 5 and of (LKSE)₃ at order 5
  were started before that append and were not repeated after it; every bracket run was made
  after it; the validations and consistency runs were repeated with the final file.
* **Timings and memory** are single runs on a shared machine.
* **Prior art outside our own reports was not searched.**  Searched: P3 (`gfbound.py` line 110,
  `termwise.py` line 128), P5, P6, P8 (`p8sr.py`, `p8lib.py`, `x01_ff_proto.py`) for an evaluation
  with the actual increments — all take the maximum over the states of the non-host site; and
  addendum A17 (17), (18) for the allocation.  I claim nothing as new beyond "not in those".
* **Physical meaning.**  Everything is relative to the GBn2 model function on P2's rigid
  synthetic peptides; nothing here bears on water or on a real peptide.

### My own errors

1. **A wrong expectation at the start, recorded before the number:** that the bound would
   depend strongly on the rotamer of the *host* side chain (the brief's first stage).  It does
   not (§3.1); the dependence is in the non-host increments.  Found in the first probe; the
   plan was changed then (`NOTES.md`, 10:41).
2. **Predictions about the floor: five wrong out of nine** (§4.1, §4.5, §5.2).  Too pessimistic
   three times (the triple form with stage-1 tables at Lys₁₂ order 4: 0.75 predicted, 0.35
   found; at (LKSE)₃ order 5: 3.3 predicted, 1.87 found; the triple form of stage 2 at Lys₁₂
   order 3: "more than 2" predicted, 0.83 found); too optimistic twice, by factors 36 and 9
   (the window form with P8's constants: 0.02 predicted, 0.72 found; 0.15 predicted, 1.31
   found) — the second of these after I had seen the first, because the prediction had
   already been written.  In the first-order cases the predictions were within 3–8 %; the
   stage-2 rows in the equal-share forms elsewhere came out 20–40 % below my guesses.
3. **A comparison in the wrong order.**  My first Lys₄ validation compared my exact block
   remainders with P8's stored ones assuming P8 orders its blocks as I do; it does not, and
   the "deviation" was 0.3 kcal/mol.  I had not read P8's list.  Fixed; with the blocks
   re-ordered the two enumerations agree to `5·10⁻¹³`
   (`not_cited/validate_K4_H_0.70_run1_block_order_bug.log`).
4. **Two runs that failed at once.**  The order-3 bracket runs stopped with an error because
   my driver insisted on P8's stored per-subset constants, and P8 stored none at order 3 for
   the twelve-residue peptides.  I had not looked.  Fixed (the driver then uses the constants
   it re-computes in P8's code path, and says so); the failed logs are in `not_cited/`.
5. **Logs produced with code that changed afterwards.**  The first validation runs and the
   first consistency runs used the first version of one routine (`Resolver._cross`, rewritten
   at 10:51 for memory; same arithmetic up to rounding).  All were re-run with the final
   library before being cited; the first runs are in `not_cited/` and agree with the cited
   ones to the printed digits (the consistency figure at twelve residues moved from
   `6.9·10⁻¹⁶` to `8.7·10⁻¹⁶`).  The first version of `p9_04_gain.py` chose the sub-tuples of its
   constant window column differently from the bracket driver; re-run, old log in `not_cited/`.
   And one script of the re-run list (`p9_00_probe.py`) still used the first version's call
   and would have failed; found on re-reading, fixed and re-run (same numbers).
6. **Run times over-estimated by a factor 2–4** in the announcements the rules require before
   long runs (tables of (LKSE)₃: announced 10–13 minutes per part, took 4; bracket runs at
   order 4: announced 9–11 minutes, took 4–5).  The announcements are in `NOTES.md` with the
   measured times next to them.  And one memory mark of my own passed: I had written that I
   would stop the sampler run above 2.9 GB; its peak was 2 801 972 kB (2.87 GB decimal, 2 736
   in the "MB" of the logs); it was below the 3 GB limit and I let it run.  Three run times in
   the table of §7 had been typed from memory and were off by a few seconds; corrected from
   the last lines of the logs in the final read.
7. **A guessed time stamp** (10:33 written, the clock said 10:27), once, corrected with the
   correction visible; since then every time in `NOTES.md` is pasted from `date -u`.
8. **A foreground `sleep`** of 45 s (and two of 1–2 s to stagger starts), against the rule;
   from then on the long jobs ran in the harness's background mode.
9. **A careless `sed`** with an unescaped dot replaced one line of this report's draft by "XX";
   seen at once and repaired by hand.
10. **A self-test that tests nothing** (§2): the two remainder routines it compares do the
    same subtractions in the same order.  Left in the logs, labelled here.
11. **A comparison that did not name its form.**  Until the last hour my draft set my sampler
    width "as stated" (Hoeffding) next to "the coordinator's 0.041 with 12 000 evaluations"
    without saying that 0.041 is the coordinator's *two-end, empirical-Bernstein* interval from
    4 000 000 proposals (as stated: 0.188).  I had copied the number from the addendum's table
    and not opened the log.  It understated the gain and compared unlike things; §5.4 now
    names both forms and both numbers of proposals.
12. **A note that claimed too much:** I wrote in `NOTES.md` that prediction 2 "held in every
    line" for Lys₁₂ at order 5; one line (0.015997) was `3·10⁻⁶` below the range I had given.
    Corrected in the notes two minutes later; the table of §4.1 says "no" for that line.
13. **An expectation that contradicted its own formula, and an untested explanation.**  Before
    the sampler run I wrote "fewer than ten evaluations" next to a rule that gives 24 with the
    numbers I had put into it; 90 were needed (§5.4).  And my draft then explained the
    difference by "the allowances of the inner sandwich", which I had not tested; the sentence
    is removed and §5.4 says what is known (the envelope's bracket under the proposals is two
    to three times its first-order numbers on the Gibbs samples) and what is not.

## Coordinator's note (2026-11-26, after the hand-back; everything above is the workstream's text, unchanged)

*Who writes here.*  The report above is workstream P9's.  I am the coordinator of the division.
Before publishing it (SCI-MSG-0028) I read it in full, went through §1 on paper, and checked
what is listed below with code that is not P9's (`experiments/science/p9_verification/`, every
log there ends with `ALL DONE`).  "Checked" never means refereed: **nothing in this report has
been read by an independent referee, and nothing in it is machine-checked.**

**N1.  The statements (§1) — re-derived, no gap found.**  Lemma T′ is P3's theorem with the
increments it is stated with; Theorem R is P8's Theorem AH with its last step left out — the
one point to verify is that a host `l ∉ T` sits at the anchor in the context `z^{T,x}`, and it
does: with the hosts last in the order, `T` (at least three sites, at most two hosts) has a
non-host element, which precedes `l`.  Proposition P stands on the two sentences its proof
prints in bold: the actual `x_T` is among the points of the maximum that defines `c_{T,U}(x_U)`,
and a table that is charged although `T ⊄ S(x)` only adds a non-negative term.

**N2.  The raw tables `Θ²_T` against exact remainders (my left sides, my states, my controls).**

| instance, order | what was compared | states | violations | smallest bound / exact | controls that must fail (violations) |
|---|---|---|---|---|---|
| Lys₄, Lys₅, LKSE:5, every order 3…n | `R ≤ B₂ ≤ B₁ ≤ B_SAb` at every state (`resolved_enum_check.py`) | 15 743 – 114 263 per row | 0 in all eight rows | 8.46 – 30.2 (Boltzmann mean of `B₂/R`: 255 – 880) | minimum in place of the value: 877 – 68 427; table reversed: 2 – 2 703 |
| Lys₁₂, 3 | every state with exactly 3 side chains off: exact anchored term against `Θ²_T(x_T)` (`resolved_check12.py`) | 92 525 | 0 | 9.02 | 14 334; 438 |
| Lys₁₂, 4 | the same with 4 | 1 524 690 | 0 | 8.25 | 630 395; 18 972 |
| (LKSE)₃, 3 | the same with 3 | 175 185 | 0 | 15.05 | 42 045; 2 819 |
| (LKSE)₃, 4 | the same with 4 | 3 290 515 | 0 | 8.26 | 1 853 296; 170 176 |
| Lys₁₂, (LKSE)₃, Ser₁₂, 5 | no ball of radius 5 exists: 2 000 uniformly random states each, and the Gibbs states with five or more side chains off | 2 000 + 0, 116, 812 | 0 | 17.7, 23.3, 8.9 | table reversed: 15, 20, 3 (weak) |

At order 5 the check is a necessary condition at states far from the ensemble; the per-entry
check that exists at orders 3 and 4 does not exist there.

**N3.  From the raw tables to the brackets, with a driver of mine (P9's request P9-E1, done:
`resolved_brackets.py`).**  The window-form tables and the triple sums, re-built from the raw
tables with my code, equal P9's stored ones entry for entry (largest deviation `0.0`) in all six
cases; "envelope ≤ tables" holds at 32 000 – 40 000 random states per case with **equality**
where the envelope is a single entry (window form), and fails with the minimum in place of the
maximum (15 393 – 27 020 violations) and with every twentieth table removed (119 – 10 560).
The brackets, digit for digit those of §4 and §5:

| instance, order (ball) | window form W | equal shares on triples T |
|---|---|---|
| Lys₁₂, 3 (3 841) | `[517.108870, 517.185731]` 0.07686 | `[516.827371, 517.659419]` 0.832 |
| Lys₁₂, 4 (96 366) | `[517.125649, 517.132996]` 0.007347 | `[517.075039, 517.186576]` 0.1115 |
| Lys₁₂, 5 (1 621 056) | `[517.125705, 517.132938]` 0.007233 | `[517.121336, 517.137333]` 0.016 |
| (LKSE)₃, 4 (181 268) | `[655.603013, 655.622116]` 0.0191 | `[655.203848, 656.350724]` 1.147 |
| (LKSE)₃, 5 (3 471 783) | `[655.604050, 655.621038]` 0.01699 | `[655.520038, 655.714657]` 0.1946 |
| Ser₁₂, 5 (481 506) | `[227.363089, 227.374782]` 0.01169 | `[227.357675, 227.380236]` 0.02256 |

The sandwich `m₋ ≤ E ≤ m₊` at 6 980 states of mine per case and form (Gibbs states of my seed,
exact samples of the floor **and of the ceiling**, uniformly random states, states with exactly
`m` and `m + 1` side chains off; new evaluations of the energy): no violation.  **How much that
last check can see** — the same states with the tables left out: 829 and 929 violations (Lys₁₂,
order 3), 18 (order 4), 92 ((LKSE)₃, order 4), and **none** for Lys₁₂ and (LKSE)₃ at order 5 and
for Ser₁₂; with tables a hundred times smaller 207, 4, 3 (window form) and never with tables ten
times smaller.  A table too small by a factor ten would pass the sandwich check at my states;
it would not pass N2.

**N4.  Not checked by me.**  The stage-1 tables (only stage 2 was compared with exact terms and
re-built); the forms S and B; the rows "joint maxima of stage 2 as constants" and "P8's
constants, my chains"; (LKSE)₃ at order 3 (no certificate there anyway); the gain tables of §3;
P3's interval enclosures and hulls, inherited by every certificate of the division.
*The sampler (§5.4).*  Run (B) — (LKSE)₃ from the order-4 ball — was repeated with a driver of
mine and another seed (`p9_verification/nested_resolved.py`, seed 2026113740 where the workstream
had 2026112740): as the theory division states the bound `[655.612563, 655.612815]` (above:
`[655.612562, 655.612814]`); two-end form with empirical Bernstein `[655.612658, 655.612720]`
(above: `[655.612657, 655.612719]`); 15 392 of 400 000 proposals accepted, 1 200 evaluated, none
outside either sandwich.  Run (A) was not repeated.  Run (C), which the workstream could not
make for memory, is in addendum A17 (19).

**N5.  What "certified" means in this report.**  A bracket of §4–§5 is the output of exact
transfer matrices on two models whose validity rests on a chain of paper proofs: P3's theorem
(workstream P3; its corollaries re-derived by workstreams P8 and P9, its bound tested on every
triple and four-body term that was enumerated; no independent referee), P8's Theorem AH
(re-derived and tested by me, not refereed), Theorem R and Proposition P above (N1; not
refereed), and on one implementation
of the stage-2 evaluation, tied to exact four-body and three-body terms by N2.  It is relative
to the GBn2 model function on rigid synthetic peptides.

**N6.  What is in the repository.**  Scripts, `NOTES.md`, the report parts, 60 logs (each ends
with `ALL DONE`) and 22 screen captures of chained runs (`logs/*.stdout`, not cited), the JSON
records, and `not_cited/` — 13 logs of failed or superseded runs,
kept under that name as the brief prescribed and named in §7; none of them is evidence.  **Not**
in the repository: `cache/` (0.52 GB) and `out/*.npz` (0.64 GB), regenerable arrays; the commands
are in §7 (`p9_03_tables.py … --keeptabs` writes the raw tables that my verification scripts
and the sampler driver read: 87 s and 378 s for Lys₁₂ at orders 4 and 5, twice four minutes
for (LKSE)₃ at order 5).

**N7.  What followed.**  The report's last line — the brackets are now the reductions of the
band, untouched — is where the coordinator went next: the slack of a reduction is a known
table, and a Gibbs–Bogoliubov argument with exact marginals of the ceiling model takes it
out of the bracket.  That is addendum A17 (19) of `docs/science/INFERENCE_LIMITS_ADDENDA.md`
(`pi_inference/slack_recovery.py`, `first_order_recovery.py`), not part of this workstream.
