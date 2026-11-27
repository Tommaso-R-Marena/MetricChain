# R6 — referee report on theory report §11.17

**Object.** `docs/THEORY_REPORT.md` §11.17 at commit `36ec238` (lines 2973–3086): Theorem 11.47, Theorem 11.48,
Proposition 11.49, the comparison paragraphs and the prior-art paragraph; `proofs/Frontiers/LinearClass.lean`;
the witnesses `linRes_span_witness`, `pairRes_envelope_tight_witness`; harness XIV.1–XIV.2; blueprint §7
("A format that does not grow", lines 691–717); README lines 163–178; research log lines 776–784.

**Referee.** Independent; no part in the work. All scripts, outputs and the Lean scratch file are in
`<session scratch>/referee6/`
(`scripts/`, `out/`, `lean/`, `snapshot/`).

**Note on the object.** While I worked, the working tree of the repository was being changed by another process
(a Proposition 11.50, `LinearKernel.lean`, `pairRes_le_of_dominates`, `pairRes_sharp`, harness XIV.3, edits to the
blueprint and the log, and finally an uncommitted `docs/workstreams/P_REPORT.md`). I reviewed the committed
state `36ec238`, from a snapshot taken with `git show` (`snapshot/`). The uncommitted additions are not
reviewed, and I did not read the workstream P report, so that this report stays independent of it.

---

## 0. Summary

No statement marked as a theorem is false as an inequality, and everything marked **[V]** is what the Lean file
proves. The defects are of the kinds found in earlier cycles: an exactness claim that is stronger than what is
true, a comparison that is not like with like, a bound that is not tight presented as the order of the truth,
and scope that is too wide in two places.

Verified (re-derived, and checked with my own code):

* Theorem 11.47 (a), (c), the inequality of (b) for every `λ`, the upper end of (d) with its orientation.
* Theorem 11.48 (a), (b) including attainment, the transport description (also when the two configurations have
  different numbers of pairs within the cutoff, and with pairs exactly at the cutoff), the invariances, the
  inequality of (c).
* Proposition 11.49 (a) with its constant `8 ln 2 · |𝒯|² z L S_c / ε₁`, and (b).
* The planning constant `5.6` of the blueprint (`8 ln 2 = 5.545`).

Wrong, overstated or misleading (details in §2):

1. **M1.** "Minimised over `λ` … the exact range" (11.47(b)) and "exact after minimising over `λ`: the bracket at
   `y` is the `L¹` distance … to the span" (11.48(c); also README and research log). The exact range is
   `[max_λ (lower end), min_λ (upper end)]` with **two different** multipliers. Its half-width equals the
   weighted `ℓ¹` distance to the span only for central data (the worst case over data, which is what Smolyak's
   lemma is about). Counterexample with two features: exact range `{1}`, distance to the span `1`.
2. **M2.** The comparison of the three formats is not a comparison of like with like. Theorem 11.38 is a statement
   at `ε = 0`. At an extensive accuracy and the same `L`, the RMSD envelope has uniform nets of size independent
   of `N` as well (this already follows from the proof of Theorem G8(a) of workstream G; I re-derived it). The
   three numbers belong to three residual classes with Lipschitz constants in different units.
3. **M3.** The transport term of 11.47(d) is the cost of one particular transport plan (everything through `y`),
   not the transport cost. For the star with a remainder of envelope `η·`Hamming it gives `2k(k−1)η`, but the
   exact value is `2(k−1)η` — linear in `k`, not quadratic. The remark "the order of the second-order bound of
   §11.7" compares a loose bound for one class with a sharp bound for a larger class.
4. **M4.** Proposition 11.49(b) and the blueprint name "chains on the rational torus … with bounded denominators"
   as a case with finitely many distances. With rational torsion charts of bounded denominator the number `G` of
   distinct squared distances below the cutoff grows with `N` (1, 1, 1, 2, 5, 14, 36 for `N = 4…10`, exhaustive;
   at least 474 at `N = 14`).
5. **M5.** The bound of 11.49(a) is correct but numerically vacuous for plausible parameters (`10^{100}` to
   `10^{2700}` in my examples, against actual nets of `10` to `10⁴` points). The blueprint calls it a planning
   number.
6. **M6.** "Does not grow" holds for the number of residual evaluations, at an extensive accuracy, for the
   class of functionals of pair-distance statistics. At a fixed absolute accuracy the same argument gives
   `exp(O(N/ε))`, and that order is attained for the first-order class on rich conformation spaces.

Improvements the authors can take over (§2, "Improvements"; appendices B–D):

* `|𝒯|²` can be replaced by `|𝒯|` in 11.49(a) (use that the *total* count over all types is at most `zN/2`).
* For the pair-additive class itself (not the first-order class of `d_P`), `256 (|𝒯| z L S_c/ε₁)²` evaluations
  suffice for every `N` — polynomial instead of exponential in `1/ε₁`, and polynomial in `N` at a fixed absolute
  accuracy. This follows from a published theorem on greedy reduced bases (DeVore–Petrova–Wojtaszczyk 2013,
  Cor. 3.3) and answers, for the class without a remainder, the question left open in 11.49(c). Not
  machine-checked; my derivation; the decay is confirmed numerically on synthetic chains.
* 11.47(d) should be stated with the Kantorovich–Rubinstein cost (exact by duality; verified numerically), and
  the lower end with the transposed term (proved in my Lean scratch file).

Novelty: every individual statement is known or routine; the envelope `d_P` is, as a structural metric, the
`ℓ¹` distance between sorted pair distances per type (Bag of Bonds, 2015; shape distributions, 2002). What I did
not find elsewhere is its use as an envelope of a residual class with certificates counted in evaluations.

---

## 1. Verdict per statement

Depth: E = elementary, R = routine application of a known theorem. "LP" = my own linear programs (HiGHS).

| # | statement | correct? | how checked | depth | novelty | remark |
|---|---|---|---|---|---|---|
| 1 | 11.47(a) `sup_θ [g(x) − g(y)] = θ⁰·ΔF + Σ w∣ΔF∣` | yes | Lean signatures re-read with `#check` (`linRes_sub_le`, `linRes_sub_attained`); LP | E | known (dual norm of a box; robust LP with interval coefficients) | — |
| 2 | 11.47(a) class ⊂ first-order class of `d_F` around the centre, pairwise as wide | yes | Lean (`linRes_dev_admissible`, `featEnv_isEnvelope`) | E | routine | — |
| 3 | 11.47(b) bracket for every `λ`, centred at `λ·v + θ⁰·r` | yes | Lean (`linRes_span_upper/lower`); LP: 35 534 brackets × 3 random `λ` | E (weak duality) | known | centre term confirmed (harness mutation M1 also tests it) |
| 4 | 11.47(b) "minimised over `λ` it is the exact range" | **only end by end**; false as "half-width = `min_λ Σ w∣r∣`" | LP primal = dual at both ends: 35 534 feasible cases (zero weights, boundary data, dependent rows), 6 374 infeasible; exact rational arithmetic, 622 440 cases; Lean scratch `single_multiplier_not_exact` | LP duality | known | M1 |
| 5 | 11.47(c) span ⇒ exact; `rank F` evaluations determine `g` | yes | Lean (`linRes_span_exact`); LP (26 357 in-span cases, width 0) | trivial | known (it is Eq. `E(x*) = Σ C_k E(x^(k))` of Podryabinkin–Shapeev) | counts evaluations only |
| 6 | 11.47(d) upper end with `Σ λ = 1` | yes, orientation right | Lean (`sumClass_span_upper`); LP on 1 500 random asymmetric envelopes | E | routine (Lebesgue-constant bound) | not sharp: M3 |
| 7 | 11.47(d) read as a two-sided bracket | **no** for asymmetric `d` | LP: lower end with the same term violated in 489/1 500; Lean scratch `lower_same_orientation_fails`, `sumClass_span_lower` | E | — | m1 |
| 8 | `Σ λ = 1` necessary | yes (pure first-order remainder) | LP unbounded in 1 500/1 500 cases with `Σ λ ≠ 1` | E | — | avoidable only with pointwise bounds on the remainder |
| 9 | star remark: (d) gives `2k(k−1)η`; §11.7 gives `k(k−1)η` | arithmetic yes; **message no** | exact LP on cubes `n = 4, 5, 6`, all `k`: sup `= 2(k−1)η` | E | — | M3 |
| 10 | cube comparison: first-order class exponential, linear class `n + 1` | yes, with qualifiers | re-derived from 11.25/11.26 | trivial | "specific here" | rank is `n`, not `n+1`; functional and accuracy regime left implicit (§1A.2) |
| 11 | 11.48(a) summation by parts | yes | exact (Fractions) on 420 chains with non-grid breakpoints; Lean `pairRes_eq_cum` | E | textbook (energy as a linear functional of the pair distribution) | boundary term needs `φ(S_c) = 0`: fine |
| 12 | 11.48(b) `sup = d_P`, attained | yes | exact on 2 520 ordered pairs (attained by evaluating the extremal radial functions on the pair distances); Lean scratch `pairRes_sub_attained` | E | KR duality with a Dirichlet boundary | repo has only a one-cell witness and a tautological harness check (m8) |
| 13 | `L¹` of cumulative counts = `W₁` with the cutoff as free boundary | yes | exact: sorted clamped multisets (7 560 type pairs); optimal partial matching with a reservoir (7 366; 4 884 with different numbers of pairs inside the cutoff; 148 pairs exactly at the cutoff) | E | known (Figalli–Gigli-type boundary; Osada et al. 2002: `L¹` of cdf = EMD) | it is `W₁` of *squared* distances (m4) |
| 14 | invariance under rigid motions, reflections, permutations of beads of one type | yes | exact (60 mirror images, 56 permutations: `d_P = 0`) | E | — | reflection invariance = blindness to chirality (m10); "beads of one type" presupposes pair types given by bead types (m5) |
| 15 | 11.48(c) inequality for every `λ` | yes | Lean grid (`pairRes_span_upper/lower`); LP on the merged grid, 420 brackets, primal = dual at both ends | E | instance of 11.47(b) | "the bracket is the distance to the span": M1 (strictly smaller in 224/420) |
| 16 | Lean statement as formalisation of 11.48 | adequate for the inequalities | instantiation (grid = occurring squared distances) reproduces `g` and `d_P` exactly, 180 cases | — | — | not formalised: instantiation, several types, attainment, duality, `W₁`, invariance (§1A.3) |
| 17 | 11.49(a) `ln N_cov ≤ 8 ln 2 ∣𝒯∣² z L S_c/ε₁` | yes | re-derived incl. integer rounding of `B`; rounding error and count checked (20 000 functions); lattice enumeration; off-lattice samples | R (entropy of monotone functions) | application apparently new | improvable to `∣𝒯∣` (App. B); vacuous in numbers (M5) |
| 18 | 11.49(a) "independent of `N`", "of the known part", "pair-additivity not used" | yes | proof inspection | — | — | at `N ≤ 16` actual nets still grow with `N` when `G = 6`: saturation is asymptotic |
| 19 | 11.49(b) `∣𝒯∣ G` features; contact energies | yes given `G` | rank of the profile matrix over all square-lattice chains: 3 (`S_c = 5`), 6 (`S_c = 10`), `N = 8…16` | trivial | Maiorov–Crippen 1992; Tobi et al. 2000 | rational-torus example wrong: M4 |
| 20 | 11.49(c) "what is not covered" | incomplete | — | — | — | m10; the polynomial question has a positive answer for the pure class (App. C) |
| 21 | three formats: `exp(Θ(N))`, `exp(Θ̃(√N))`, `exp(O(1))` "at an extensive accuracy" | **not like with like** | re-derived; workstream G, Theorem G8(a); my block-net lemma (App. A) with a numerical sanity check | — | — | M2 |
| 22 | prior-art paragraph | citations correct in substance | §4 | — | — | Smolyak imprecise (m2); closer prior art missing (m11) |
| 23 | witnesses `linRes_span_witness`, `pairRes_envelope_tight_witness` | genuine | read; copied verbatim into `lean/R6Witnesses.lean` and type-checked | — | — | minimal (three points; one cell) |
| 24 | harness XIV.1–XIV.2 | test the grid/LP statements; can fail | read; run from my snapshot (both survive: 507 and 439 brackets) | — | — | gaps: m9 |
| 25 | blueprint paragraph | mostly backed | §1A Q7 | — | — | voxel rule unbacked (m13); M4; M5; m1 |

---

## 1A. Answers to the exact questions

### Q1. Theorem 11.47

**(a), (b) against Lean.** `linRes_sub_le` needs only `|θ − θ₀| ≤ w`; `linRes_sub_attained` needs `w ≥ 0`; together
they are (a). `linRes_span_upper` and `linRes_span_lower` are exactly the displayed inequality of (b), with
`g(a k)` in place of `v_k`. The prose matches the Lean statements, including the centre term `θ⁰·r`.

**Exactness.** LP duality holds here in the following form, which I verified (script `r6_lp_duality.py`):

    { g(y) : θ in the box, g(x_i) = v_i }  =  [ max_λ (λ·v + θ⁰·r − w·|r|),  min_λ (λ·v + θ⁰·r + w·|r|) ],   r = F(y) − Σ λ_i F(x_i).

* *Feasible data* (35 534 cases, including weights equal to zero, data on the boundary of the feasible set,
  linearly dependent evaluated feature vectors): primal = dual at both ends, gap below `3·10⁻¹³`.
* *Infeasible data* (6 374 cases): the primal is infeasible and both dual problems are unbounded, so the
  "range" is empty. The dual is always feasible (`λ` is free), so there is no other case.
* *Zero weights* are harmless: an LP needs no Slater condition; the corresponding `|r_α|` is not penalised.
* *Unbounded `λ`*: the minimum is attained (LP), but the set of minimisers is unbounded when the evaluated
  feature vectors are dependent. This costs nothing without a remainder.
* *Exact arithmetic*: for one evaluation and up to three features I enumerated vertices and breakpoints with
  rational numbers (622 440 cases, 191 952 infeasible): equality at both ends in every case.

What is **not** true is the reading "the exact range is the bracket of the multiplier that minimises
`Σ w|r|`", i.e. "the half-width is the weighted `ℓ¹` distance of `F(y)` to the span". The two ends are attained
at different multipliers (in 3 787 of 35 534 cases the minimiser of the upper end is not optimal for the lower
end), and the width is strictly below twice the distance in 3 741 of the non-central cases. Equality holds
for central data `v = F_A θ⁰` (8 385 cases, all equal). Example (also in `lean/R6Scratch.lean`,
`single_multiplier_not_exact`): features `(1,1)` at `x₁` and `(1,0)` at `y`, `θ⁰ = 0`, `w = (1,1)`, `v₁ = 2`.
Then `θ = (1,1)` is forced and `g(y) = 1` exactly, while `|1−λ| + |λ| ≥ 1` for every `λ`; the upper end is
attained at `λ = 0`, the lower at `λ = 1`.

**Attribution.** Smolyak's result (candidate dissertation, Moscow 1965; a proof is in Novak–Woźniakowski,
Thm 4.7, according to Foucart; also attributed to Bakhvalov) says: for a linear functional, linear information
and a *symmetric convex* class,
some **linear** algorithm is optimal for the worst-case error *over the class*. In the notation here (centre
`0`): `min_λ Σ w|r(λ)| = sup{ g(y) : data = 0 }`. That is the zero-data instance of the duality — the radius
of information — with one `λ` for all data. The exact range for given data is ordinary LP duality with
data-dependent multipliers; it is not Smolyak's lemma. For a box around `θ⁰ ≠ 0` the optimal rule is affine
(`λ*·v + θ⁰·r*`), which is Sukharev's extension to convex non-symmetric classes. I did not read
Micchelli–Rivlin 1977 itself (§4). From memory, not re-read: the survey sets up optimal recovery with the
intrinsic error `sup{|Ux| : x ∈ K, Ix = 0}` at zero information, shows that it is within a factor 2 of the best
possible error for balanced convex `K`, and presents the linear optimal algorithm for linear functionals with
the attribution to Smolyak — again the worst-case statement. "Robust linear programming with interval
coefficients" is Soyster's setting (also from memory); (a) is its one-line worst case.

**(c)** Correct, and it holds for coefficients outside the box as well (the Lean statement has no box
hypothesis). "A certificate for every functional at every accuracy" is right in the sense of §11 (a set of
evaluations after which the consistent values have width 0). It is a statement about the number of residual
evaluations; the minimisation over `X` that turns the determined residual into a value of `min` or `ln Z` is
not part of it.

**(d)** Orientation: for the **upper** end the term `Σ_i (λ_i⁺ d(y,x_i) + λ_i⁻ d(x_i,y))` is right with the
convention `ρ(a) − ρ(b) ≤ d(a,b)` (valid on 1 500/1 500 random asymmetric envelopes; the transposed term is the
one for the lower end, and with the same term the lower end fails in 489/1 500). `Σ λ_i = 1` is necessary for
a remainder constrained only through differences: adding a constant `C` to `ρ` changes
`ρ(y) − Σ λ_i ρ(x_i)` by `C(1 − Σ λ_i)` (LP unbounded in 1 500/1 500 cases). With pointwise bounds on the
remainder (the ground node of §11.1) the missing mass can be sent to the ground node.

The term is **not sharp**. The exact value of `sup_ρ [ρ(y) − Σ λ_i ρ(x_i)]` is the Kantorovich–Rubinstein cost
of moving the positive part `δ_y + Σ λ_i⁻ δ_{x_i}` of the signed measure onto its negative part `Σ λ_i⁺ δ_{x_i}`
(min-cost flow = LP in 1 500/1 500 cases); the term of (d) is the cost of the plan that routes everything
through `y`. It exceeds the exact value in 759/1 500 cases, by a factor up to 12.6.

*The star.* The arithmetic is right: `λ = 1` on the `k` neighbours, `1 − k` on the centre, so (d) gives
`k·(k−1)η + (k−1)·kη = 2k(k−1)η`; and §11.7 with `c_ij = 2η` gives `k(k−1)η`. But the exact value is

    sup_ρ [ ρ(y) + (k−1) ρ(x⁰) − Σ_{i∈S} ρ(x⁰⊕e_i) ]  =  2(k−1)η

(plan: `y →` one neighbour at cost `(k−1)η`, `x⁰ →` the other `k−1` neighbours at cost `η` each; attained by
`ρ(x) = η·| |x|_S − 1 |`; LP on the cubes `n = 4, 5, 6`, every `k`). The exact bracket of the class "additive
(slopes in `[−c,c]`, free constant) + `η`-Lipschitz remainder", given the values of the zero residual on the
star, is `±(k−1)(η + min(c,η))` (LP over coefficients and remainder, four parameter sets). So an additive
residual with a first-order remainder is determined by a star up to
an error **linear** in the Hamming distance; the quadratic law of §11.7 belongs to the larger second-order
class. The sentence in the report suggests the opposite.

### Q2. The comparison on the cube

Fair in the narrow sense: same envelope (`c·`Hamming is the feature envelope of `F_i = x_i`, `w_i = c`), same
instance (the zero residual lies in both classes), and the cost compared is that of an algorithm correct on
the respective class. Three qualifiers are missing.

* The linear class has `n` parameters and the first-order class `2ⁿ − 1`; the statement is "knowing that the
  residual is additive is worth an exponential factor", not "a better format for the same uncertainty".
* "`2^{n(1−o(1))}`" is for `ε = o(n)` (minimum: covering by Hamming balls; `ln Z`:
  `cube_deterministic_lower_bound`). At an extensive accuracy the deterministic exponent is
  `ln 2 − h(ε₁/u)`, and above the threshold `ε₁ > ln cosh(u/2)` a randomised algorithm on the first-order
  class needs `O(1)` evaluations (Theorem 11.25(b)) — fewer than `n + 1`. The parenthesis "below the
  threshold" covers this, but the headline sentence does not.
* With the features `x_i` alone the rank is `n` (`g(0) = 0`); `n + 1` is right with a free constant.

The sentence about Theorems 11.23–11.28 is accurate: those theorems give costs *at* additive instances for
algorithms correct on the first-order class, and the verification against non-additive members of the class
is what costs (learn-then-cover, "without a hint"); with the class restricted to additive residuals the star
alone suffices.

### Q3. Theorem 11.48

* **Summation by parts.** `g(x) = Σ_τ ∫ φ_τ dN^x_τ = φ_τ(S_c) N^x_τ(S_c⁻) − Σ_τ ∫_0^{S_c} φ_τ′ N^x_τ ds`; the boundary term
  vanishes because `φ_τ(S_c) = 0`. A pair exactly at the cutoff is not counted in `N^x(s)`, `s < S_c`, and
  contributes `φ(S_c) = 0`: consistent. Lean: `sum_mul_eq_sum_diff_mul_cum` is Abel summation with boundary
  term `φ m · Σ_{j<m} c_j`, removed by `φ m = 0` in `pairRes_eq_cum`. Checked exactly on 420 chains with radial
  functions whose breakpoints are not grid points.
* **Cutoff condition.** It is needed. A square-well contact term is discontinuous at the cutoff and is not in
  the class for continuous distances; it adds the feature `N^x(S_c⁻)` with coefficient `φ(S_c⁻)`. On a lattice
  it is in the class with `L = u₀/(`gap to the next distance`)`, as 11.49(b) uses it.
* **Envelope.** `L^∞`–`L¹` duality; the extremal slope `−L·sign(N^x − N^y)` is a legitimate member. Exact on 2 520
  ordered pairs, evaluated on the pair distances directly.
* **Transport description.** Correct. Clamp every squared distance at `S_c`; the two clamped multisets of one
  type have the same number of elements (the number of pairs of that type is fixed by the sequence), and the
  `L¹` distance of the cumulative counts on `[0, S_c]` is their `W₁` distance. Equivalently it is the optimal
  partial matching in which an unmatched pair is moved to `S_c` at cost `S_c − s`: this is what "free boundary"
  means, and it covers the case of different numbers of pairs within the cutoff (4 884 such cases among the
  7 366 I solved as assignment problems; all equal to the `L¹` distance). Two remarks: it is the transport
  distance of *squared* distances (`∫|ΔN| ds = ∫|ΔN| 2r dr`), and the mass is counts, not probabilities.
* **Invariances.** Correct. Reflection invariance means the class cannot contain a term that distinguishes
  mirror images. "Permutations of beads of one type" requires `τ(p,q)` to be a function of the two bead types;
  with pair types that depend on the sequence separation it is false.
* **Span bracket.** The inequality is right; "exact after minimising over `λ`" is M1.
* **Lean statement.** `pairRes φ cnt m x = Σ_{k<m} φ k · cnt x k`, `cumCount`, `profEnv L Δ cnt m`, hypotheses
  `φ m = 0` and `|φ k − φ (k+1)| ≤ L Δ k`. For any *finite* set of configurations with real distances, take as
  grid the occurring squared distances below the cutoff and `S_c` as the point `m`, `cnt x k` the number of
  pairs at the `k`-th value, `Δ k` the gaps; then `pairRes = g`, `cumCount = N^x(s_k)` and
  `profEnv = L ∫|N^x − N^y|` (checked exactly, 180 instances). Every instance of the inequalities involves
  finitely many configurations, so nothing is lost for them. What is not formalised: this instantiation
  (no real-valued distances, no Lipschitz function of a real variable, no chain); several types (a sum of
  instances — not a concatenation, which would add a spurious term at the block boundary); attainment (one-cell
  witness only; a 25-line proof for every grid is in `lean/R6Scratch.lean`, `pairRes_sub_attained`);
  exactness of the span bracket; the transport interpretation; the invariances; all of Proposition 11.49.
  The tag "[V on a grid of distances]" is accurate.

### Q4. Proposition 11.49

**(a) Re-derivation.** Per type, `N^x_τ(s) ≤` (number of pairs within the cutoff) `≤ zN/2`. For nondecreasing
`h : [0,S_c] → [0, M]`, `M = z/2`: the step function with value `(M/B)⌊h(s_j) B/M⌋` on `[s_j, s_{j+1})` satisfies
`0 ≤ h − h̃ ≤ [h(s_{j+1}⁻) − h(s_j)] + M/B` on the cell, hence `‖h − h̃‖₁ ≤ (S_c/B) M + S_c M/B = z S_c/B`.
The rounded functions are nondecreasing sequences of length `B` over `B + 1` levels: `C(2B, B) ≤ 4^B`. With
`|𝒯|` types: external radius `L|𝒯| z S_c N/B` in `d_P`, at most `4^{B|𝒯|}` cells; one representative per
non-empty cell gives an internal net of twice the radius (a certificate consists of evaluated conformations,
so the net must be internal). `B = 4 z S_c L|𝒯|/ε₁` gives radius `ε₁N/2` and `4^{B|𝒯|} = exp(8 ln 2 |𝒯|² z L S_c/ε₁)`.
The constant is right.

* *Integer `B`.* With `m = ⌈B⌉` cells: `C(2m,m) ≤ 4^m/√(πm) ≤ 4^{m−1} < 4^B` for `m ≥ 6`; `C(10,5) = 252 ≤ 4^4 < 4^B`
  for `m = 5`; and for `m ≤ 4` we have `ε₁ ≥ |𝒯| z L S_c`, which is at least twice the diameter of `d_P/N`, so
  one evaluation is a net. The bound holds for all parameters.
* *Accuracy.* `ε` is a width. A net of `d_P`-radius `ρ` gives `U_A − L_A ≤ 2ρ` pointwise, hence
  `min(f+U_A) − min(f+L_A) ≤ 2ρ` and `Z(f+L_A)/Z(f+U_A) ≤ e^{2βρ}`; with `ρ = ε/2` the net itself is a value
  certificate of width `ε` for the minimum and for `β⁻¹ ln Z` (no extra evaluation at a minimiser is needed
  for a value certificate). It is also a cover in the sense of `N_cov(ε)`: `s(a,y) ≤ 2 d(a,y) ≤ ε`.
* *Independence of `N` and of `f`.* Yes: a uniform net of the profile set, the same for every `f` and `g`.
  "Pair-additivity is not used": right; only `|g(x) − g(y)| ≤ d_P(x,y)` is used.
* *Checks.* Rounding error and count on 20 000 random and adversarial monotone functions (worst error
  `4.22` against the bound `4.5` at `B = 8`; counts below `C(2B,B)`).

**Vacuous or meaningful?** Numerically vacuous; meaningful only as the statement "independent of `N`".

* *Contact energy on the square lattice* (analytic): contacts at `s = 1`, next distance `s = 2`, `S_c = 2`,
  `z = 4`, `L = u₀`. At `ε₁ = 0.1 u₀` per bead the bound is `exp(444) ≈ 10^{193}`. The truth: the profile is one
  integer in `[N−1, 2N]`, a net of radius `ε₁N/2` has about `L/ε₁ = 10` points, and in the linear class one
  evaluation determines the contact strength.
* *Square-lattice chains, exhaustive* (`r6_lattice_cover.py`; all self-avoiding walks up to symmetry;
  `L = 1`). Net sizes are bracketed by a separated set (below) and a farthest-first net (above).

  | `N` | walks | `S_c` (`z`, `G`) | profiles | diam `d_P/N` (a priori `zS_c/2`) | `ε₁ = 1`: net | `ε₁ = 0.25`: net | bound at `ε₁ = 1` / `0.25` |
  |---|---|---|---|---|---|---|---|
  | 12 | 15 037 | 5 (12, 3) | 168 | 5.00 (30) | 5–12 | 33–82 | `10^{144}` / `10^{578}` |
  | 16 | 802 075 | 5 (12, 3) | 541 | 5.75 (30) | 6–16 | 46–124 | `10^{144}` / `10^{578}` |
  | 12 | 15 037 | 10 (28, 6) | 2 247 | 19.0 (140) | 41–173 | 547–1 328 | `10^{674}` / `10^{2697}` |
  | 16 | 802 075 | 10 (28, 6) | 29 860 | 23.25 (140) | 74–464 | 2 297–6 780 | `10^{674}` / `10^{2697}` |

  For `G = 6` the nets still grow with `N` at `N = 16`; they must saturate below `(1 + 2|𝒯| z L S_c/ε₁)^{|𝒯|G}`
  (volume bound, m7), but the saturation is not visible at sizes that can be enumerated.
* *Off-lattice chains, sampled* (`r6_offlattice.py`; unit bonds, hard core 0.85, `S_c = 4`, `L = 1`; coils,
  stiff coils, globules of several densities, helices, zigzags, mixed; 180–240 conformations per `N`):

  | `N` | `z` | diam `d_P/N` (a priori) | nearest-profile radius after 8 / 32 / 64 evaluations | bound of 11.49(a) at those accuracies |
  |---|---|---|---|---|
  | 32 | 31 | 8.67 (62) | 1.30 / 0.53 / 0.35 | `10^{115}` / `10^{280}` / `10^{426}` |
  | 64 | 31 | 11.18 (62) | 1.61 / 0.46 / 0.31 | `10^{93}` / `10^{323}` / `10^{483}` |
  | 128 | 33 | 11.77 (66) | 1.52 / 0.46 / 0.25 | `10^{104}` / `10^{346}` / `10^{648}` |

  (sample-based: a lower bound on what the full conformation space needs, but the gap is hundreds of orders
  of magnitude). Two reasons for the gap: the a-priori diameter `zLS_c/2` overestimates the real one by a
  factor 5–7, and that factor sits in the exponent; and realistic profile sets are far from "all monotone
  functions".
* The bound beats plain enumeration (`μ^N` conformations, `ln μ ≈ 0.97` on the square lattice) only for
  `N > 5.7 |𝒯|² z L S_c/ε₁`: `N > 460` in the contact example, `N > 4 100` with three pair types.

**Lower bound.** For the first-order class the order `1/ε₁` cannot be improved in general. If every bead has one
partner at a distance that can be set freely in an interval of squared length `ℓ` (for instance 1–3 distances
with flexible bond angles, the other pairs outside the cutoff), the normalised profiles contain all
distributions of mass `m₁ ≈ 1` on that interval, and at `f = 0`, `g = 0`

    ln N_cov(ε₁N)  ≥  0.0082 · L m₁ ℓ/ε₁ − 0.13

(staircases with one atom per cell at the left end or the middle, Gilbert–Varshamov; App. D). Same form as the
upper bound; the constants differ by two to three orders of magnitude. On my "rich" synthetic family (unit
mass on 48 distances) the nearest-profile radius after 64, 128, 256, 512 evaluations is `0.108, 0.090, 0.076,
0.064` — logarithmic decay, as the entropy predicts.

**Improvements.** (i) `|𝒯|² → |𝒯|` (App. B; checked numerically). (ii) Discrete distances:
`ln N_cov ≤ |𝒯| G ln(1 + 2|𝒯| z L S_c/ε₁)`. (iii) For the pair-additive class: `256 (|𝒯| z L S_c/ε₁)²` evaluations
(App. C). On the rich family the span of 48 profiles is exact where 512 nearest-profile evaluations leave
`0.064`; on the off-lattice samples 32 span evaluations leave `0.7–1.3 %` of the diameter against `4–6 %`.

**(b)** Correct as a conditional statement, and the rank is attained on the lattice (3 and 6). The Lipschitz
hypothesis is not needed there. The example "chains on the rational torus of §5 with bounded denominators"
is wrong unless the denominators of the *squared distances* are bounded: the squared distance of two beads at
sequence separation `m` is a product of `m` rational rotations, its denominator grows like `5^{2m}` in my model,
and `G` grows with `N` (M4).

**(c) What is missing.**

* Chirality: `d_P(x, mirror image of x) = 0`, so every member of the class takes the same value on a
  conformation and its mirror image. Handedness preferences must be in the known part.
* `d_P` is a pseudometric with very large fibres: on the square lattice at `N = 16`, 802 075 chains (up to
  lattice symmetry) have 541 distinct profiles (`S_c = 5`). The first-order class of `d_P` is the class of functionals of the profile.
  That is reasonable for a homogeneous pair-additive error and for nothing else; it is far smaller than an
  RMSD-Lipschitz class (a member is RMSD-Lipschitz with a constant of order `4 z L R_c N`, not conversely).
* The accuracy: at a fixed absolute accuracy the bound is `exp(O(N/ε))` (M6).
* The Lipschitz condition is in `s = r²`: a term with bounded `dφ/dr` has `dφ/ds = φ′(r)/2r`, large at short
  range. Steep short-range terms and long-range terms (`z ∝ S_c^{3/2}`, so the exponent grows like `S_c^{5/2}`)
  are outside.
* Sequence-specific residuals are covered by "every pair its own type"; the intermediate case (types that
  depend on the sequence separation) multiplies `|𝒯|`.
* The count is of residual evaluations. Checking a certificate requires a lower bound of `f + L_A` over all
  conformations, and `L_A` is a function of global pair counts; over voxels of torsions the enclosure of a
  pair distance widens with the lever arm, so the difficulty of §11.14 returns in the checker even though it
  has left the constants.
* The hypothesis "at most `z` beads within the cutoff" excludes the phantom (product) domains on which
  Theorems 11.37–11.38 are stated.

### Q5. The three formats

Not like with like, in three respects.

1. *Accuracy.* Theorem 11.38 is `c√(λN) ≤ ln N_cov(0) ≤ …`: exact certification at the zero residual. At an
   extensive accuracy the RMSD envelope with the same `L` has covers of size independent of `N`. Theorem
   G8(a) of workstream G, read at `ε = ε₁N`, has `s_w ≥ s_0 = ⌊ε₁N/((1+√3)Lb)⌋` for every `w`, so it gives
   `N_cov(ε₁N) ≤ 1 + n·81^{⌈(N−1)/s_0⌉}`, and its proof (code cells of RMSD diameter `(1+√3) s b`) gives the
   single layer `N_cov(ε₁N) ≤ 81^{⌈(N−1)/s_0⌉}` without the factor `n`: for large `N`,
   `ln N_cov ≤ 4.4·(2.73 Lb/ε₁ + 1)`. I re-derived this independently (App. A: uniform nets for every `f` and
   `g`, `ln N ≤ 42.5 Lb/ε₁`; sanity check `r6_rmsd_net.py`). Also `RMSD² ≤ R_g(X)² + R_g(Y)²` (quoted in
   `reviews/R_G_review.md`), so `RMSD ≤ 0.41 bN` and for `ε₁ ≥ 0.82 Lb` one evaluation suffices. The entry
   `exp(Θ̃(√N))` is therefore not the cost of the RMSD format "at an extensive accuracy"; at an extensive
   accuracy and fixed `L` it is `exp(O(1))`, like the profile envelope.
2. *Constants.* `L` in Theorems 11.36–11.38 is a Lipschitz constant in RMSD; `L` in 11.48–11.49 is per pair and
   per unit of squared distance. A pair-additive residual with fixed per-pair `L` is extensive and has
   `L_RMSD` of order `N` (§11.14 says so for extensive local residuals). For such `L` the RMSD format is
   exponential in `N` (G8(c); the workstream's reviewer: "for extensive `L` both formats are exponential").
3. *Classes and domains.* The weighted-Hamming class contains the RMSD class with the same `L`; the `d_P` class
   is contained in an RMSD class with `L_RMSD ∝ N` and is far smaller than it. Theorems 11.37–11.38 are on
   phantom product domains; 11.49 needs excluded volume.

A like-for-like table would read:

| residual | accuracy | per-torsion Hamming | RMSD directly | profile `d_P` |
|---|---|---|---|---|
| RMSD-Lipschitz, `L` fixed | `ε = 0`, zero residual | `exp(Θ(N))` | `exp(Θ̃(√N))` (11.38) | not applicable (other class) |
| RMSD-Lipschitz, `L` fixed | `ε₁N` | `exp(Θ(N))` (11.37) | `exp(O(1))` (G8(a); App. A) | not applicable |
| functional of pair statistics, per-pair `L` fixed (so `L_RMSD ∝ N`) | `ε₁N` | `exp(Θ(N))` | `exp(O(N))`, presumably `exp(Θ(N))` (lower bound not proved here) | `exp(O(1))` (11.49(a)) |
| same | fixed `ε`, or `ε = 0` | exponential | exponential | `exp(O(N/ε))` by the same argument; `exp(Ω(N/ε))` on rich spaces (first-order class); pair-additive class: polynomial (App. C) |

*A reader may conclude:* (i) a residual that is admissible for `d_P` — in particular pair-additive with
`L`-Lipschitz radial functions vanishing at the cutoff, on a conformation space with bounded coordination — has
value certificates of width `ε₁N` whose number of evaluations is bounded independently of `N`, for every known
part; (ii) with finitely many distances `|𝒯|G` evaluations determine a pair-additive residual exactly.

*A reader may not conclude:* (i) that the profile format beats the RMSD format on a common class at a common
accuracy — at extensive accuracy and fixed `L` the RMSD format does not grow either, and the `√N` law is a law
at `ε = 0`; (ii) that certificates in the profile format stay bounded at a fixed absolute accuracy or at
`ε = 0`; (iii) anything about residuals that are not functionals of pair-distance statistics (RMSD-Lipschitz,
chirality-sensitive, sequence-specific, many-body); (iv) that `exp(5.6…)` is a number one can plan with;
(v) that the certificate can be checked at bounded cost.

### Q6. Prior art

* **Smolyak; Micchelli–Rivlin 1977.** Correct for the worst-case statement (linear optimal algorithm for a
  linear functional on a symmetric convex class). The report attaches the name to the exact range at given
  data, which is plain LP duality (m2). Sukharev should be cited for the affine case.
* **Maiorov–Crippen 1992.** I could not open the paper (HTTP 403). Tobi–Shafran–Linial–Elber (Proteins 40, 2000;
  I read pp. 71–73) say on p. 72: "We are not the first investigators to use inequalities to design folding
  potentials. The first pioneering work was of Maiorov and Crippen". The attribution is supported by this
  secondary source. The closer reference for the report's features is Tobi et al. themselves: `U = Σ_l p_l S_l(X)`,
  "`n_α^i` is the number of contacts of type `α` in structure `i`" (210 types), and step potentials with seven
  distance segments per type (1 470 parameters) — pair counts per type and distance bin as linear features,
  with linear inequalities over decoys.
* **Podryabinkin–Shapeev 2017.** Verified (arXiv 1611.09346, full text through the fetch tool):
  `E(x*) = Σ_k C_k E(x^(k))`,
  `C = b(x*) A⁻¹`, `γ(x*) = max_k |C_k|`, "we call `γ(x*)` the *extrapolation grade*", "if all `|C_k| ≤ 1` then we
  are interpolating"; selection by D-optimality (maxvol). The report's sentence is accurate; the grade is the
  `ℓ^∞` size of the multipliers, the transport term of (d) their weighted `ℓ¹` size.
* **Closer prior art not cited.**
  - `L¹` distance of the cdf of pair distances as an earth mover's distance between shapes: Osada, Funkhouser,
    Chazelle, Dobkin, ACM TOG 21 (2002), p. 815, footnote 1 (read): "The cdf `L₁` and the cdf `L_∞` norms are the
    `L₁` earth mover's … and the Kolmogorov–Smirnov distances".
  - Bag of Bonds (Hansen et al., J. Phys. Chem. Lett. 6, 2015; full text via summary): entries grouped by
    pair type, **sorted** within each bag, zero-padded, compared in `ℓ¹`. The `ℓ¹` distance of sorted padded
    vectors is the `W₁` distance of the per-type distributions with a reservoir at the padding value: `d_P`
    is this distance with `min(r², S_c)` in place of `Z_iZ_j/r`.
  - Wasserstein-1 distances between radial distribution functions as similarity measures in crystal-structure
    work, and earth mover's distances between pointwise distance distributions with Lipschitz continuity
    (Widdowson–Kurlin): search summaries only.
  - Transport with the boundary as a reservoir: Figalli–Gigli 2010 (search summary only).
  - Entropy of bounded monotone functions `≍ 1/ε` (Birman–Solomjak 1967; van de Geer 1991; van der Vaart–Wellner
    Thm 2.7.5): the content of 11.49(a) (secondary sources only).
  - Greedy reduced bases (Binev et al. 2011; DeVore–Petrova–Wojtaszczyk 2013): gives App. C.
  - The energy of a pair-additive system as a linear functional of the pair distribution is the textbook
    energy equation (from memory; not re-read).
  - Decision making with a utility linear in unknown parameters constrained by queries, minimax regret
    (Boutilier et al. 2006; abstract level): the general setting of 11.47 in another field.
* **Known, routine, new.** 11.47(a)–(c): known. 11.47(d): routine and not sharp. 11.48(a): textbook. 11.48(b):
  KR duality; the metric is known as a descriptor distance. 11.48(c): instance of 11.47(b). 11.49(a): the
  classical entropy bound plus McShane. 11.49(b): trivial. Apparently new: the use of the profile distance as
  an envelope of a residual class next to a known part, and the count of evaluations that follows. I found
  nothing that states this, but my search was a few queries (§4).
* **Title.** "An envelope for chains that does not grow" is too short for what is proved. What does not grow
  is (i) the constant `L` per pair, in contrast with the per-torsion constants, and (ii) the number of
  evaluations of a certificate at an extensive accuracy for the class of pair-statistics functionals. The
  envelope itself is extensive, and at a fixed absolute accuracy the certificates of the first-order class
  grow exponentially (M6).

### Q7. Blueprint paragraph

| rule in the blueprint | backing | hypotheses right? |
|---|---|---|
| envelope `d_P = L Σ ∫∣N^x − N^y∣` | `pairRes_sub_le`, `profEnv_isEnvelope` (grid, one type) | yes; several types and real distances by an instantiation that is not formalised |
| exact computation with rational breakpoints | squared distances of rational coordinates are rational; integral of a step function | yes, "when the geometry is rational" (§5 notes that bond-angle sines are irrational in general; then only enclosures) |
| nearest profile `∣g(y) − g(x_i)∣ ≤ d_P(y,x_i)` | `pairRes_sub_le` in both orders | yes |
| span, any rational `λ` | `pairRes_span_upper/lower` | yes; no condition on `Σ λ` is needed for the pure class, and none is stated |
| planning number `exp(5.6 · types² · z L S_c/ε₁)` | Proposition 11.49(a) **[P]**; `8 ln 2 = 5.545` | constant right; first-order class of `d_P`, width `ε₁N`; it is an upper bound, not a planning figure (M5); "have at most" should be "need at most" |
| `types · G` evaluations for `G` distances "(lattice or rational-torus geometries)" | `linRes_span_exact` | lattice yes; rational torus no (M4) |
| remainder: extra term, `Σ λ = 1` | `sumClass_span_upper` — upper end only, stated for `linRes` | for an asymmetric `d` the lower end needs the transposed term (m1); the link `pairRes` = `linRes` with cumulative counts is not in Lean |
| voxel: "replace `N^y` by its interval enclosure" | **none** (not in §11.17, not in Lean) | the rule must read: replace the integrand by `max(∣N_lo − c∣, ∣N_hi − c∣)`, `c = Σ λ_i N^{x_i}`, pointwise in `s`; elementary, but unstated (m13) |

---

## 2. Errors and gaps

### CRITICAL

None. No inequality stated as a theorem is false, and no **[V]** tag is wrong.

### MAJOR

**M1. Exactness of the span bracket is overstated** (report lines 2997–2999 and 3039–3041; README lines 171–174;
research log lines 777–779).
*Claim.* "Minimised over `λ` it is the exact range"; "exact after minimising over `λ`: the bracket at `y` is the
`L¹` distance from the profile of `y` to the span of the evaluated profiles".
*Counter-statement.* The set of consistent values is `[max_λ (λ·v + θ⁰·r − w·|r|), min_λ (λ·v + θ⁰·r + w·|r|)]`, the
two ends at different multipliers in general. Its width is at most `2·min_λ Σ w|r|`, with equality for central
data and strict inequality otherwise in general (two features: range `{1}`, distance `1`; 3 741 of 27 149
non-central random cases; 224 of 420 chain cases).
*Fix.* State the two ends separately; say that the weighted `ℓ¹` distance to the span is the **worst case over
the data** (the radius of information) and is attained by the affine rule `λ*·v + θ⁰·r*`; attach Smolyak's
name to that statement. The same qualifier applies to "a first-order class has the distance to the nearest
one". Soundness is not affected.

**M2. The comparison of the three formats** (lines 3073–3076). See Q5. *Fix:* replace the sentence by the table
of Q5, or say: "at `ε = 0` and fixed RMSD-Lipschitz constant …; for an extensive pair-additive residual …".
The claim "at an extensive accuracy: RMSD used directly `exp(Θ̃(√N))`" is not compatible with Theorem G8(a)
read at `ε = ε₁N`.

**M3. Theorem 11.47(d) is not sharp, and the star remark draws a conclusion from the loss** (lines 3005–3009,
3017–3019; blueprint lines 714–716).
*Counter-statement.* `sup_ρ [ρ(y) − Σ λ_i ρ(x_i)] = W_d(δ_y + Σ λ_i⁻ δ_{x_i}, Σ λ_i⁺ δ_{x_i})`; the term of (d) is an upper
bound for it, loose by a factor `k` on the star (`2k(k−1)η` against `2(k−1)η`).
*Fix.* State (d) with the transport cost (a transport plan is a certificate that a checker verifies by one
sum; the plan through `y` is the default); correct the star remark: additive + first-order remainder is
determined by a star up to `2(k−1)η`, the quadratic law belongs to the second-order class.

**M4. "Rational torus with bounded denominators" is not a case of finitely many distances** (line 3057;
blueprint line 711).
*Evidence.* `r6_rational_torus.py`: unit bonds, bend `(3/5, 4/5)`, torsions `(−1,0), (3/5, ±4/5)`, exact arithmetic,
`S_c = 4`: `G = 1, 1, 1, 2, 5, 14, 36` for `N = 4…10` (all conformations), at least `84, 161, 289, 474` for
`N = 11…14` (3 000 random conformations each); denominators up to `5^{24}`.
*Fix.* Keep "lattice chains"; for the rational torus say that `G` is finite for every `N` but grows with `N`
(here by a factor of about 2.6 per bead), so the count `|𝒯|G` is not independent of `N`.

**M5. The planning number** (blueprint lines 707–710; Proposition 11.49(a)). The bound is valid and of no use
as a number: `10^{93}` to `10^{2700}` at accuracies where 8 to 7 000 evaluations suffice in my examples (Q4).
*Fix.* Call it an existence bound. Give the alternatives: `|𝒯|` instead of `|𝒯|²`; the volume bound for
discrete distances; the polynomial bound for the pair-additive class; and the advice to compute the profile
diameter instead of using `zLS_c/2`.

**M6. Scope of "does not grow"** (section title; title of Proposition 11.49; blueprint heading).
*Counter-statement.* At a fixed absolute accuracy `ε` the argument of 11.49(a) gives
`ln N_cov ≤ 8 ln 2 |𝒯|² z L S_c N/ε`, and on rich conformation spaces `ln N_cov(ε) ≥ 0.008 L m₁ ℓ N/ε` at
`f = g = 0` (App. D): the certificates of the first-order class grow exponentially with `N` exactly in the
regime in which a ground state can be told from its competitors. The brief of workstream P says this
("at fixed absolute accuracy the first-order class is exponential in `N`"); §11.17 does not.
*Fix.* Say it in 11.49, and say that the count is of evaluations (Q4(c), last-but-one item).

### MINOR

* **m1** (lines 3005–3007; blueprint 714–716)**.** (d), lower end: for an asymmetric envelope the term is
  `Σ_i (λ_i⁺ d(x_i,y) + λ_i⁻ d(y,x_i))`. Proved (`sumClass_span_lower`) and the same-orientation version refuted
  (`lower_same_orientation_fails`: `d(y,a) = 0`, `d(a,y) = 1`, `ρ(y) = ρ(a) − 1`) in `lean/R6Scratch.lean`. The
  report says "the bracket … gains the transport term", the blueprint states a two-sided rule.
* **m2** (lines 2998–2999, 3079–3080)**.** Attribution to Smolyak: see Q1. Add Sukharev (convex, non-symmetric: affine rules).
* **m3** (line 3016)**.** "`n + 1` evaluations": `n` with the features `x_i` alone.
* **m4** (lines 3032–3034)**.** "Wasserstein-1 distance between the pair-distance distributions": of the *squared* distances. Say that
  `L` is a Lipschitz constant in `s`.
* **m5** (line 3035)**.** "Permutations of beads of one type": only if pair types are functions of bead types.
* **m6** (line 3049)**.** `|𝒯|²` → `|𝒯|` (App. B).
* **m7** (lines 3056–3059)**.** Discrete distances: `ln N_cov ≤ |𝒯|G ln(1 + 2|𝒯| z L S_c/ε₁)` for the first-order class.
* **m8** (line 3032)**.** Attainment of `d_P` is machine-checked on one cell only and "harness-checked" by an identity that
  cannot fail (m9). A general proof is 25 lines (scratch file).
* **m9** (`falsify_conjectures.py` lines 4546–4663)**.** Harness. XIV.1 and XIV.2 do test the Lean/LP statements and are not vacuous (mutations M1–M4, M1–M3
  exist; I read them, did not run them). Gaps: (i) the two "attained" checks compare `w·|ΔF|` with itself
  under a sign choice — they cannot fail; (ii) data are always feasible and interior (no infeasible, no
  boundary data); (iii) the lower end is compared with the truth but not with its own dual; (iv) (d): upper
  end only; (v) XIV.2 uses random counts on a random grid — no chain, no real distances, no pair at the
  cutoff, one type, nothing about transport or invariance; (vi) nothing tests Proposition 11.49.
* **m10** (lines 3062–3071)**.** 11.49(c) omits chirality, the size of the fibres of `d_P`, the accuracy regime, the `s`-Lipschitz
  condition and the cost of checking (Q4(c)).
* **m11** (lines 3078–3085)**.** Prior art: add Osada et al. 2002, Bag of Bonds 2015, Tobi et al. 2000, the entropy of monotone
  functions, greedy reduced bases, transport with a boundary (Q6).
* **m12** (lines 3062–3063)**.** "If every pair is its own type, `d_P` is the weighted `ℓ¹` distance of distance matrices": of the
  squared distance matrices clamped at `S_c`.
* **m13** (blueprint lines 716–717)**.** Blueprint, voxel rule: no statement behind it; give the precise form (Q7).
* **m14** (§13; `prior_art/`)**.** The four new citations have no entry in §13 or in `prior_art/` with a verification status.
* **m15** (lines 3066–3070)**.** 11.49(c): "whether polynomially many evaluations … suffice depends on … bounded coefficients".
  Without a remainder the size of the coefficients plays no role, and the answer is yes (App. C). The
  sentence is right only with a remainder.

### Improvements (not errors)

* App. B: `ln N_cov ≤ 8 ln 2 |𝒯| z L S_c/ε₁`.
* App. C: `256 (|𝒯| z L S_c/ε₁)²` evaluations for the pair-additive class, for every `N`.
* App. D: a lower bound of the same form for the first-order class.
* M3: the transport form of (d).

---

## 3. Independent numerical checks

All code is mine (`scripts/`); outputs in `out/`. One core, `ulimit -v 2500000`, longest run 7.5 minutes.

| script | what | sizes | outcome |
|---|---|---|---|
| `r6_lp_duality.py` | 11.47(a)–(c): primal and dual LP at both ends; infeasible, boundary and central data; zero weights; dependent rows; random `λ`; width against `2·`distance to the span; exact rational check for one evaluation | 6 000 instances, 41 908 (instance, `y`) pairs: 35 534 feasible, 6 374 infeasible; 622 440 exact cases (`p ≤ 3`) | duality holds end by end, max gap `2.8·10⁻¹³`; infeasible ⇔ dual unbounded; width `= 2·`distance for central data (8 385), strictly smaller in 3 741 cases; one multiplier not optimal for both ends in 3 787 cases; exact check: equality in all cases |
| `r6_remainder_transport.py` | 11.47(d): hub term on random asymmetric envelopes; lower end; KR cost; `Σ λ ≠ 1`; star on the cube; exact bracket of "additive + remainder" | 1 500 envelopes on 4–8 points; cubes `n = 4, 5, 6`, all `k`; 4 parameter sets | upper end valid 1 500/1 500; same term on the lower end fails 489; transposed valid 1 500; KR = LP 1 500/1 500; hub loose in 759 (factor ≤ 12.6); unbounded when `Σ λ ≠ 1`: 1 500; star: exact `2(k−1)η` against `2k(k−1)η` and `k(k−1)η`; bracket `±(k−1)(η + min(c,η))` |
| `r6_pair_profiles.py` | 11.48 with exact rational arithmetic on chains with non-grid distances, 1–3 bead types, cutoff equal to an occurring squared distance | 60 instances × 7 chains of 5–10 beads | (a) exact on 420 chains; (b) bound and attainment exact on 2 520 ordered pairs; `W₁` identity 7 560; partial matching 7 366 (4 884 with different pair numbers; 148 pairs at the cutoff); mirror 60, permutation 56; Lean form 180; (c) primal = dual 420, better than McShane in 249, width below `2·`distance in 224 |
| `r6_lattice_cover.py` | 11.49(a),(b): all square-lattice self-avoiding walks, profiles, nets, ranks | `N = 8…16` (802 075 walks up to symmetry at `N = 16`); `S_c = 5` and `10` | table in Q4; ranks 3 and 6; bound never violated and `10^{140}`–`10^{2690}` times too large |
| `r6_offlattice.py` | 11.49 on sampled off-lattice chains: nets against spans | `N = 32, 64, 128`; 180–240 conformations; 160 cells | table in Q4; span radius after 32 evaluations `0.7–1.3 %` of the diameter, nearest profile `4–6 %`; `ℓ¹` size of the multipliers ≤ 3.5 |
| `r6_rounding_and_widths.py` | rounding lemma and count of 11.49(a); `∣𝒯∣` version; rich family | 20 000 + 9 000 functions; 4 048 profiles on 48 distances | error ≤ `zS_c/B` (worst 4.22 against 4.5); counts ≤ `C(2B,B)`; total error with `∣𝒯∣` types ≤ `zS_c/B`; nets logarithmic, span exact at 48 |
| `r6_rational_torus.py` | 11.49(b): number of distinct squared distances | exhaustive `N ≤ 10` (6 561 conformations), 3 000 samples for `N = 11…14`; exact | `G` = 1, 1, 1, 2, 5, 14, 36, ≥84, ≥161, ≥289, ≥474 |
| `r6_rmsd_net.py` | block-net lemma for the RMSD envelope | `N = 40…320`, `K = 2, 4, 8`, 6 000 chains each | deviation within a cell ≤ `(2+√3) bN/K` in all cases; number of cells below the cap, independent of `N` |
| `lean/R6Scratch.lean` | signatures and axioms of the cited theorems; `sumClass_span_lower`; `lower_same_orientation_fails`; `pairRes_sub_attained`; `single_multiplier_not_exact` | type-checked with `lake env lean` against the compiled library, exit 0, no warnings | axioms `propext`, `Classical.choice`, `Quot.sound` only |
| `snapshot/proofs/Frontiers/LinearClass.lean`; `lean/R6Witnesses.lean` | the committed file itself; the two committed witnesses copied verbatim | type-checked with `lake env lean`, exit 0, no warnings | standard axioms only |
| committed harness, `--only XIV` (from my snapshot copy, to see what it computes) | XIV.1, XIV.2 | default seed | both survive (507 brackets, 283 exact; 439 brackets, 251 open) |

The research log's counts are right: 43 Lean files, 89 registered tests (17 expected refutations), 132
mutations (counted in the snapshot).

---

## 4. Literature (search log)

Searches (web search tool, 25 November 2026) and what I read. "Summary" means the answer of the fetch tool on
the full text; "search summary" means the result page only.

| query / source | read | finding |
|---|---|---|
| "Smolyak lemma optimal recovery linear functional convex balanced set" | Foucart, arXiv 2004.00195 (summary of full text); arXiv 2311.15767 (summary) | "there is a linear functional among the optimal recovery maps as soon as the set is symmetric and convex" (Smolyak 1965, candidate dissertation; proof in Novak–Woźniakowski, Thm 4.7); global worst-case error, distinct from the local error at given data; "goes back to Smolyak and Bakhvalov"; convex non-symmetric: Sukharev (search summary) |
| Micchelli–Rivlin, "A survey of optimal recovery", 1977 | bibliographic record only | exists (Plenum 1977, pp. 1–54); content **not read** |
| Maiorov–Crippen, J. Mol. Biol. 227 (1992) 876–888 | not accessible (403); search summary; Tobi et al. p. 72 | supported by secondary sources |
| Tobi, Shafran, Linial, Elber, Proteins 40 (2000) 71–85 | pp. 71–73 in full | Eqs. 2–6 quoted in Q6 |
| Tobi–Elber, Proteins 41 (2000) 40–46 | search summary | distance-dependent pair potential by linear optimisation |
| Podryabinkin–Shapeev, arXiv 1611.09346 | summary of full text | Eqs. 8–9, "extrapolation grade", D-optimality, maxvol |
| "Wasserstein distance radial distribution functions structural similarity" | search summary | 1D Wasserstein-1 between normalised pair-distance histograms used as RDF similarity in recent crystal-structure papers; Wasserstein on Coulomb-matrix representations |
| Osada et al., ACM TOG 21 (2002) | pp. 814–815 in full | cdf `L₁` = earth mover's distance (footnote 1) |
| Hansen et al., J. Phys. Chem. Lett. 6 (2015) (Bag of Bonds) | summary of full text (PMC) | bags by pair type, sorted, zero-padded, `ℓ₁` distance |
| Widdowson–Kurlin, pointwise distance distributions | search summary | EMD between distance distributions; Lipschitz continuity |
| Binev et al., SIAM J. Math. Anal. 43 (2011) | abstract (search summary) | `d_n ≤ M n^{−α}` ⇒ `σ_n ≤ C_α M n^{−α}` (Hilbert space) |
| DeVore–Petrova–Wojtaszczyk, arXiv 1204.2290 | summary of full text | Cor. 3.3(ii): `σ_n ≤ 2^{5α+1} γ^{−2} C_0 n^{−α}` (Hilbert); Cor. 4.2(ii): `n^{−α+1/2+β}` (Banach) |
| "metric entropy monotone functions L1" | search summary | order `1/ε`: Birman–Solomjak 1967, van de Geer 1991, van der Vaart–Wellner Thm 2.7.5; originals not read |
| Figalli–Gigli 2010 | search summary | transport distance with the boundary as a reservoir |
| Boutilier et al., AIJ 170 (2006) | search summary | minimax regret under linear utility uncertainty with queries |

Not searched: Kolmogorov or Gelfand widths of sets of radial distribution functions; kernel methods on
pair-distance histograms beyond Bag of Bonds; robust-optimisation literature on force-field parameters. The
novelty statement in Q6 rests on this limited search.

---

## 5. Faithfulness of README, blueprint and research log

* **README (lines 163–178).** Faithful except for M1: "its bracket after evaluations is a weighted `ℓ¹` distance to
  the *span* … (machine-checked; exactness is linear-programming duality)". Machine-checked is the bound for
  every `λ`; the width is *at most* twice that distance. "Certificates in that format do not grow with the
  chain length at extensive accuracy — … for a smaller class of residuals" is accurate; it omits the
  hypothesis of bounded coordination and that the count is of evaluations.
* **Research log (lines 776–784).** Same remark (M1). "Its first-order class has certificates whose size does not
  depend on the chain length at extensive accuracy" is accurate. The factual counts of the "Verified state"
  paragraph are right.
* **Blueprint (lines 691–717).** See Q7: the envelope, nearest-profile and span rules are backed; M4 (rational
  torus), M5 (planning number), m1 (remainder, lower end), m13 (voxel rule) are not.
* **Lean header of `LinearClass.lean`.** Accurate; it says that exactness is not formalised.
* **Theory report §9 index.** The committed table row for `LinearClass.lean` omits `sumClass_span_upper` and
  `sumClass_sub_le` (present in the file); the working tree has already added them.

---

## 6. Not checked

* `lake build`, `scripts/audit_all.sh` and the mutation tests were not run (rules). I type-checked my scratch
  files and a snapshot copy of the committed `LinearClass.lean` against the existing compiled library; the
  library's `LinearClass.olean` was rebuilt by another process during the review, and the signatures printed
  by `#check` agree with the committed text. The full axiom audit of the commit was not repeated.
* The uncommitted additions (Proposition 11.50, `LinearKernel.lean`, `pairRes_le_of_dominates`, `pairRes_sharp`,
  harness XIV.3) and the uncommitted workstream P report (not read).
* Theorems 11.36–11.38 and workstream G themselves; I used the statement of G8(a) and my own lemma.
* The lower bound `exp(Ω(N))` for the RMSD format at extensive `L` and extensive accuracy (row 3 of the table
  in Q5) — I state it as presumed.
* Appendix C rests on a corollary I read through the fetch tool's summary of arXiv 1204.2290, not line by
  line; the numerical decay I observed is consistent with it but does not prove it. The constant 256 is crude.
* Appendix D's richness assumption for a concrete chain model (I argued it for flexible bond angles; not
  computed).
* Saturation of the lattice nets with `N` (not reachable by enumeration at `G = 6`).
* The originals of Smolyak, Micchelli–Rivlin, Maiorov–Crippen, Birman–Solomjak, van de Geer, Figalli–Gigli.
* Three-body profiles; the claim of §11.14 that `L_RMSD ∝ N` for extensive local residuals (I gave a one-line
  bound in the other direction only).

---

## Appendix A. The RMSD envelope at an extensive accuracy

Chains with `N` beads and bond length `b`, first bead at the origin. Cut into blocks of `⌈N/K⌉` beads and snap
the first bead of each block to the grid `hℤ³`, `h = bN/K`. A bead is within `bN/K` of the first bead of its
block, and snapping moves a point by at most `h√3/2`. So two chains with the same snapped sequence differ by
at most `2bN/K + h√3 = (2+√3) bN/K` at every bead, hence in RMSD, without superposition. Consecutive snapped
points differ by at most `b(N/K + 1) + h√3`, so there are at most `(2(1 + K/N + √3) + 1)^{3(K−1)} ≤ 296^{K−1}`
sequences (`K ≤ N/10`). One representative per non-empty cell is an internal net of RMSD-radius
`(2+√3) bN/K`. For `d = L·RMSD` and radius `ε₁N/2`: `K = ⌈2(2+√3) Lb/ε₁⌉` and

    ln N_net ≤ 5.7 (K − 1) ≤ 42.5 · Lb/ε₁,   for every N, every known part and every residual of the class.

Theorem G8(a) has the same code with better constants (`81` per block, radius `(1+√3) s b`).

## Appendix B. `|𝒯|` instead of `|𝒯|²`

Let `m_τ = N^x_τ(S_c⁻)/N`; the hypothesis gives `Σ_τ m_τ ≤ z/2 =: M`. Round on `B` cells down to multiples of
`q = M/(|𝒯|B)`. Error of type `τ`: `(S_c/B) m_τ + S_c q`; total: `(S_c/B) M + |𝒯| S_c q = z S_c/B`. The rounded
tuples are `|𝒯|` nondecreasing sequences of length `B` whose last entries sum to at most `|𝒯|B`; shifting each
block by the last entry of the previous one maps them injectively to nondecreasing sequences of length `|𝒯|B`
over `|𝒯|B + 1` levels: at most `C(2|𝒯|B, |𝒯|B) ≤ 4^{|𝒯|B}`. Internal radius `2 L z S_c N/B = ε₁N/2` for
`B = 4 z L S_c/ε₁`:

    ln N_cov ≤ 8 ln 2 · |𝒯| z L S_c/ε₁.

Checked numerically (`r6_rounding_and_widths.py`, part 2).

## Appendix C. Polynomially many evaluations for the pair-additive class

Let `K_N` be the set of tuples `(N^x_τ/N)_τ` in `H = ⊕_τ L²[0,S_c]`. Piecewise constants on `q = ⌊n/|𝒯|⌋` cells per
type approximate a tuple within `(S_c/q) Σ_τ m_τ² ≤ (S_c/q) M²` in squared norm, so the Kolmogorov widths satisfy
`d_n(K_N) ≤ C₀ n^{−1/2}`, `C₀ = M √(2|𝒯|S_c)`, for all `n ≥ 1` and all `N`. By DeVore–Petrova–Wojtaszczyk (2013),
Cor. 3.3(ii), the greedy choice of `n` elements **of `K_N`** has `sup_{h ∈ K_N} dist_H(h, span) ≤ 2^{3.5} C₀ n^{−1/2}`.
With `‖u‖_{L¹} ≤ √(|𝒯|S_c) ‖u‖_H`, every profile is within `8 z |𝒯| S_c/√n` of the span in `L¹`, and by
`pairRes_span_upper/lower` the bracket at every `y` has half-width at most `L N · 8 z|𝒯|S_c/√n`. Hence

    n = 256 (|𝒯| z L S_c/ε₁)²  evaluations determine g(y) within ± ε₁N/2 for every conformation y,

for every `N` and every pair-additive `g`; at an absolute accuracy `ε` the number is `256 (|𝒯| z L S_c N/ε)²`.
The size of the multipliers is not controlled, so this is for the class without a remainder. From below,
`n` is at least the first index with `d_n(K_N)_{L¹} ≤ ε₁/2L` (a span of `n` profiles is an `n`-dimensional space),
which is of order `L m₁ ℓ/ε₁` on rich spaces. Observed decay on the off-lattice samples: `18.7, 15.5, 8.5, 5.3,
2.4, 1.3 %` of the diameter at `n = 1, 2, 4, 8, 16, 32` (`N = 32`).

## Appendix D. A lower bound for nets of the first-order class

Let the normalised profiles contain `c₀ + m₁ F` for every distribution function `F` of a probability measure
with atoms of mass `1/J` on an interval of squared length `ℓ`. Put one atom per cell of length `ℓ/J`, at the left
end or at the middle: `2^J` functions; two that differ in `h` cells are at `L¹` distance `h m₁ ℓ/(2J²)`. By
Gilbert–Varshamov `2^{0.1887 J}` of them are pairwise at distance at least `m₁ℓ/(8J)`, so every cover of radius
below `m₁ℓ/(16J)` has that many centres. At `f = 0`, `g = 0` the radius of `N_cov(ε₁N)` is `ε₁/L` in normalised
`L¹`: `ln N_cov(ε₁N) ≥ 0.1887 ln 2 · (L m₁ ℓ/(16 ε₁) − 1)`. The construction needs `J ≤ m₁N` adjustable pairs, i.e.
`ε₁ ≥ Lℓ/(16N)`; below that accuracy the packing stops at `J = m₁N` and the bound is `0.13 m₁N`.

## Appendix E. The star with a first-order remainder

`y = x⁰ ⊕ e_S`, `|S| = k`. Signed measure `δ_y + (k−1) δ_{x⁰} − Σ_{i∈S} δ_{x⁰⊕e_i}`. Upper bound:
`ρ(y) − ρ(x⁰⊕e_1) ≤ (k−1)η` and `ρ(x⁰) − ρ(x⁰⊕e_i) ≤ η` for the other `k−1` neighbours: `2(k−1)η`. Attained by
`ρ(x) = η | |x ⊕ x⁰|_S − 1 |`, which is `η`-Lipschitz for the Hamming distance: `ρ(y) = (k−1)η`, `ρ(x⁰) = η`,
`ρ(x⁰⊕e_i) = 0`.
