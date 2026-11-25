# Referee report on workstream P — envelopes for chain molecules from pair-distance profiles

Referee: independent (no part in the work).  Date: 2026-11-25.
Object: `scratch:ws/P/REPORT.md`,
version of 01:33:18 UTC (86 522 bytes, md5 `bbcf2cc2…`).  The file changed once while I was reading it
(01:21 → 01:33: a parenthesis in the proof of Lemma 11(c), `z = 24` instead of 28 in the remark after
Theorem 9, four more rows of numbers); the copy `docs/workstreams/P_REPORT.md` in the working tree is the
01:21 version.  No theorem differs between the two.
Everything below marked "mine" was computed with my own code in
`scratch:referee_P/`
(scripts `rp_*.py`, `c*.py`, outputs `out_c*.txt`); the author's scripts were read only to see what had been
computed.  Nothing in the repository was modified; no Lean was run.

---

## 0. Summary

**No statement labelled as a theorem, proposition, lemma or corollary in the report is false.**  I re-derived all
eighteen of them line by line (Propositions 1–3, Theorem 4, Corollary 5, Theorem 6, the entropy Lemma, Theorems
7–10, Lemma 11, Proposition 12, Theorems 13–14, Corollary 15, Propositions 16–17) and found the proofs correct;
the gaps are small and listed in §2.  The one external ingredient, Corollary 3.3(ii) of
DeVore–Petrova–Wojtaszczyk, I read in the source (arXiv:1204.2290v1, all 12 pages): it is quoted correctly, with
the right constant `2^{5α+1}γ^{−2}`, and its hypotheses hold in Theorem 8.

**Every measured number that the coordinator wants to quote was reproduced with independent code, at the
quoted sizes** (lattice `n ≤ 12`, 422 825 conformations; off-lattice `n ≤ 10`, 8 115 conformations; `ln Z` at
`n = 8`), with four corrections, all in the direction of *weak or slightly wrong numbers, not wrong
conclusions*:

1. The Hamming entries are valid but grossly weak lower bounds.  In every quoted instance the exact answer is
   **all conformations** (lattice `n = 12`: all 422 825, not "≥ 2.2·10⁵"; off-lattice `n = 10`: all 8 115, not
   "≥ 5 539"), by a one-line argument the report missed: the smallest valid constant exceeds the largest gap,
   so no conformation is covered by another one.  "×2.9–3.0 per torsion" is simply the growth of the number of
   self-avoiding conformations.
2. Off-lattice `n = 10`: the profile format needs **319**, not 318 (318 is the lower end of the author's own
   bracket; my MILP is solved to optimality).
3. `ln Z`, lattice `n = 8`, `ε = 0.01`: "P between 10 and 69" is true but the lower end is far from sharp; a
   rigorous knapsack bound gives **P between 65 and 69** (of 90 profile classes).
4. The one-evaluation threshold tabulated for the span format on the lattice is the threshold of the evaluation
   at the all-trans minimiser, which carries no information there (its profile is zero); the best single
   evaluation certifies up to an `L` that is 7 to 8.5 times larger (0.69 → 0.32 for `n = 5 → 12`), though it also
   decreases roughly like `4.8/N`.

**What is wrong is wording and scope** (the pattern of the earlier cycles):

* The numbers given for the sum class `P_L + Lip(η d_H)` ("needs 2, 2, 7, 20 evaluations"; "grows from 2 to
  20") are sizes of *greedy covers*, i.e. upper bounds, presented as requirements.  Pruning my own greedy covers
  gives 6 and 17 where the report has 7 and 20; no lower bound above 2 is proved, and Corollary 15 cannot give
  more than 4 in that instance.  (MAJOR M1.)
* The first negative finding is stated too strongly in two respects: chain-length independence is *not* confined
  to the "exactly pair-additive" class (Theorem 7 of the same report proves it for the whole first-order class
  of `d_P`, and Theorem 13 for sup-norm remainders up to a floor), and "reinstates the exponential cost in
  proportion to `η`" has no theorem behind it — by theory report Theorem 11.37 the exponential rate returns *in
  full* for every fixed `η > 0`; `η` enters a sub-leading term only.  (MAJOR M2.)
* The second negative finding ("no format has a chain-length-independent one-evaluation threshold") is a
  measurement for three formats and `n ≤ 12` plus a mechanism, not a theorem, and its span column needs the
  correction of item 4.  (MAJOR M3.)
* The summary (§1 of the report) is stronger than the theorems in eight places, listed in M4; the most
  misleading is "span cost ∝ features, first-order cost ∝ exp(features), and the chain length enters only
  through the number of features", which is contradicted for the first-order format by the report's own
  Theorem 6(b) and by its profile column (5 → 21 evaluations at three features).

Novelty: nothing here is deep, as the report says itself.  One thing it lists as "apparently new" is standard —
Lemma 11(c) is the Pietsch–Stesin width of a box in `ℓ¹` — and the closest precedent of Theorem 8 is not cited:
greedy evaluation points for worst-case recovery, analysed through Kolmogorov widths with the
DeVore–Petrova–Wojtaszczyk theorem, is the `P`-greedy algorithm of kernel interpolation (Santin–Haasdonk 2017).

Recommendation for the theory report.  *Can be stated as they are* (with the hypotheses of the report):
Proposition 2; Proposition 3 with the slack formulas and the correction to P3; Theorem 4 (with both "+1", and
without the equality `N_value = N_point` of the first-order theory); Corollary 5; Theorem 6(a), (b); the entropy
Lemma and Theorem 7; Theorem 8 (the cited corollary has now been read); Theorem 9; Theorem 10; Lemma 11 (with
the classical attribution for (c)); Theorems 13 and 14; Corollary 15; Proposition 16.  *Need qualifiers*:
Theorem 6(c) (product domain; on the measured self-avoiding instances the Hamming format needs every
conformation); Proposition 12 (`f ≡ 0`, zero residual, product domain — or the extensions of m8); Proposition 17
(the entropy statement is an upper bound for the first-order class); the two negative findings (M2, M3); the
measured table (four corrections above).

Three small additions of mine, offered for what they are worth (short proofs in §2, not checked by anyone
else): (a) on self-avoiding domains the Hamming format costs at least `|X_N|·exp(−4√((en+ε)/(Lc₀)))` whenever the
valid constants grow linearly with the lever arm — the correct replacement for "`3^{n−O(√n)}`", which cannot
hold on a domain with `2.9ⁿ` points; (b) Proposition 12 holds verbatim on the self-avoiding lattice chain for
`n ≤ 12` and on the hard-core generic chain for `n ≤ 10` (every trans/gauche pattern is realised), and it
extends to the torsional known part `e·#gauche` when `Lδ₁₄ > 2e`: `N^S_cov(ε) ≥ n − 2ε/(Lδ₁₄ − 2e)`; (c) the
entropy claim of Proposition 17 is correct, by a six-line quantisation argument that the report omits.

---

## 1. Verdict per statement

"Depth": S = short (a few lines once set up), M = moderate.  "Novelty": K = known mathematics, R = routine
application, N = not found in print but immediate.  Numbers of the coordinator's list in brackets.

| statement | correct? | how checked | depth | novelty | remark |
|---|---|---|---|---|---|
| Prop. 1 (P1: `g = −⟨φ′, N^x⟩`; class = image of an `L^∞` ball) | yes | re-derived; `c1`: random slopes, pair sums against profiles, 9 chain models, dev ≤ 6·10⁻¹⁴ | S | K (energy equation, integrated by parts) | — |
| [1] Prop. 2 (`d_P = L‖N^x−N^y‖₁ = L Σ_t‖sort−sort‖_{ℓ¹}`; pseudometric; invariances) | yes | re-derived (both multisets have `P_t` elements after truncation, so the profiles agree outside `[0,S_c)` and the quantile form of `W₁` applies); `c1`: LP over the radial functions themselves (Lipschitz constraints on the occurring distances) against both closed forms, 540 pairs, dev ≤ 3·10⁻¹⁴ | S | K (Kantorovich–Rubinstein on the line) | "vanishes exactly between conformations with equal profiles" is the definition of the fibres; fine |
| Prop. 3 (conditioning; `σ^±` as asymmetric weighted `L¹` gauges; `(1∓κ)L·dist₁ ≤ σ^± ≤ (1+κ)L·dist₁`; width `≤ 2L·dist₁`, equality at zero data) | yes | re-derived (substitute `v = −⟨ψ*,N^a⟩` in the dual); `c1`: 360 instances, primal in `φ`-form against dual in `λ`-form ≤ 7·10⁻¹⁴, slack formulas ≤ 6·10⁻¹⁴, all bounds hold | S | K (optimal recovery / LP duality) | — |
| [1] Correction to P3; instance with profile `(1,3,6,10)` | yes | `c1b`: profiles `(1,3,6,10)` and `(0,0,0,1)`, `‖N^{x₁}‖₁ = 46`, bracket `{1}`, `L·dist₁ = 1` (exact rationals by hand: `min_λ 36|λ|+|1−10λ| = 1`); ratio half-width/`L·dist₁` is 1 in all my instances at `κ = 0`, `< 1` in 43 of 110 at `κ = ½` and in 59 of 100 at `κ = 1`, down to 0 | S | K (global vs local radius of information) | at data `46κ` the half-width is 1, 1, 1, 0.575, 0.23, 0 for `κ = 0, ¼, ½, ¾, 0.9, 1` |
| [2] Theorem 4 (`N^S_cov ≤ N_value ≤ N_point ≤ N^S_cov + 1`; algorithmic reading) | yes | re-derived all four steps and the indistinguishability argument; `c2`, `c2b`: brute force over all evaluation sets of size ≤ 3 (≤ 2 on the 37-point domains) on 44 instances, the three implications checked for every set (0 failures), value certificates by an exact LP (max–min) | S | N | both inequalities on the right can be strict in the span format: I find `(N_cov, N_value, N_point) = (0,0,1), (1,1,2), (2,2,3)`; so `N_value ≠ N_point` here, unlike the first-order theory.  `N_value = N^S_cov` in all 31 resolved instances; whether that is a theorem is not addressed |
| [2] Corollary 5 (`N^S_cov ≤ N^P_cov ≤ N^H_cov`) | yes | re-derived (`u = N^a` in Prop. 3; `d_P` is the support function); consistent with all tables | S | N | — |
| [3] Theorem 6(a) `S ≤ rank ≤ DT` | yes | re-derived; ranks 3 (`S_c=12`), 7 (`S_c=28`), 4 (periodic two types), 9 (random two types), 14 (periodic four types) reproduced (`c3`, `c13`) | S | R | — |
| [3] Theorem 6(b) `N^P_cov ≤ #profiles ≤ C(M_N+DT, DT) ≤ (zN/2+1)^{DT}` | yes | re-derived (stars and bars; vectors of `DT` nonnegative integers with sum `≤ M_N`); profile counts 22, 37, 57, 90, 129, 190, 258, 356, 479 for `n = 5..13` reproduced | S | N | polynomial for fixed `D`, `T`; the degree is `DT` |
| [3] Theorem 6(c) (H: `c_i ≥ L c_i^{sf}`; exponential) | yes as stated (product domain by Thm 11.37; self-avoiding "measured") | `c3`, `c12`: `c^{sf}` reproduced exactly (`n = 12`: 52, 85, 92, 108, 114, 114, 114, 114, 108, 92, 85, 52); validity of `c^{sf}` on the non-product domain checked over all pairs (lattice `n ≤ 8`, generic `n ≤ 9`) | S | R | see §2 m1, m7: on the measured instances H is *all* conformations; `3^{n−O(√n)}` is a product-domain statement |
| [4] Entropy Lemma (§2.4): `4^{TG}` functions at distance `2SM/G` | yes | re-derived (rounding error `≤ TSq = SM/G`; at most `J = TG` unit jumps; moving them `≤ JqS/G = SM/G`; multisets of size `≤ J` from `TG` positions: `C(2TG,TG) ≤ 4^{TG}`); `c8`: 2 000 random monotone step functions incl. jumps on grid points, worst error 0.72·(2SM/G) | S | K (entropy of monotone functions) with an explicit constant | — |
| [4] Theorem 7 (`ln N^P_cov(ε₁N) ≤ T ln 4 ⌈4zLS_c/ε₁⌉`) | yes | re-derived: slack `≤ 2d_P`; maximal `ε/2L`-separated subset of `K_N` is an *internal* net of `d_P`-radius `ε/2`; its size is bounded by the *external* covering number at `ε/4L` (this is where 4 instead of 2 comes from); accuracy convention = theory report (interval of length `ε`) | S | R | `z` must be the `N`-independent packing constant; the "216 nats" uses the realised `z/2 = 3.25` at `N = 16` (with `z = 24` it would be 798 nats) |
| [5] Theorem 8 (`N^S_cov ≤ ⌈(8(1+κ)TzLS_cN/ε)²⌉`) | yes | re-derived the width estimate (`‖F−P_GF‖₂² ≤ hM²`, `d_n ≤ M√(2S_cT/n)` for *all* `n ≥ 1`, incl. `n < T`); cited corollary read in the source; constant `2^{7/2}·√2 = 16`; Cauchy–Schwarz on measure `S_cT`; greedy elements are profiles of conformations; `c8`: bound holds with 2–3 orders of magnitude to spare | S (given the citation) | R; the argument is that of `P`-greedy kernel interpolation | the `L²` width `≍ n^{−1/2}` of monotone functions is sharp, so exponent 2 cannot be improved by this route |
| [6] Theorem 9 (stretched exponential) | yes | re-derived both lines (`min(wA, B/w) ≤ √(AB)`, `B = 2 ln 4·TλN`; `√(2 ln 4) = 1.665`) | S | R (mechanism of Thm 11.38) | zero residual and `gap ≥ e·w` are hypotheses; vacuous below `N ≈ 10⁴` as the report says |
| [6] "Correction to the last sentence of P4" | (i), (ii) yes; (iii) is a conjecture and marked so; (iv) numbers reproduced except 318 → 319 | `c4`, `c13` | — | — | "refuted as stated" is fair: the universal claim fails on lattices |
| [7] Theorem 10 (i)–(iii) | yes | re-derived (zero-data argument; `(𝓛/V)* = V^⊥`; (iii) from Theorem 4 at `ψ* = 0`) | S | K (Bakhvalov; Traub–Woźniakowski) | deterministic schemes only, as stated |
| [7] Lemma 11 (a) Bernstein, (b) eigenvalue, (c) box | yes | re-derived; (c): the vertex argument is valid for arbitrary `V ⊂ 𝓛` because `ψ` is built on the supports of the `e_t`; `c7`: bounds `≤` brute-force inner widths; on the cube no subspace found below `(n−m)/2` | S | (a), (b) K; (c) **K** (Pietsch–Stesin), not new | — |
| [7] Proposition 12 (`d_m(K_N) ≥ δ₁₄(n−m)/2`; `m ≥ n − 2ε/(Lδ₁₄)`) | yes, for what it states: phantom chain, every pair its own type, zero residual, `f ≡ 0` | re-derived; `c7`: ranks 13, 21, 31 and greedy widths; `c9`: all `2ⁿ` trans/gauche patterns are realised by self-avoiding conformations (lattice `n ≤ 12`, generic `n ≤ 10`), so the bound also holds there | S | N (immediate from (c)) | linear in the number of *torsions*, not in the number of features (`∝ N²`); the last sentence ("on any sub-family…") needs "that realises all gauche counts independently" |
| [8] Theorem 13 (sup-norm remainder) | yes | re-derived; `c6`: 300 instances, primal (variables `ψ`, `r`) against dual ≤ 6·10⁻¹² | S | K | — |
| [8] Theorem 14 (first-order remainder; `Σλ_i = 1`; `d₀(y,A) ≤ KR ≤ Σ|λ_i|d₀(y,a_i)`) | yes | re-derived; `c6`: 300 instances, both ends, dual as one LP with a min-cost flow for the KR term ≤ 4·10⁻¹³; `Σλ = 1` at every optimum (forced by flow conservation); two-sided bound at optimal and at random `λ` with sum 1: 0 violations, hub/KR ratio up to 7.9 | S | R | `d₀` must be symmetric for the form stated; the theory report already has the asymmetric hub term |
| [8] Corollary 15 (`σ⁻_sum ≥ σ⁻_{S,aff} + s_{ηd₀}`; `N^{sum}_cov ≥ max(…)`) | yes | re-derived (minimum of a sum ≥ sum of minima; the second minimum is McShane's slack by the same duality with `L = 0`); `c6`: 0 violations in 300 instances, strict in 259 | S | N; the displayed maximum also follows from inclusion of classes alone | "the two slacks add" means super-additivity at each client; it does not make the *costs* add — see M1 |
| [9] Proposition 16 (`d_pair`; first-order format exponential) | yes | re-derived both bounds; `c7`: exact covers (MILP) on the phantom chain `n = 4, 5, 6` against `2ⁿ/V` and the partition bound, `d_pair ≥ Lδ₁₄ d_tg` on random pairs | S | R | exponential is proved for `f ≡ 0` (`ε < Lδ₁₄n/2`) and for `f = e·#gauche` only if `Lδ₁₄ > 2e`; product domain |
| [9] Proposition 17 (three-body; `KR_∂`) | dualities yes; entropy bound yes (proof supplied in §2 m9); "the complexity depends on the body order through the dimension" is an upper bound for the first-order class only | re-derived; triangle-type counts 4 and 21, 25, 27, 28, 28 reproduced (`c11`); the two LP dualities were not re-run | S | K (transport with a reservoir) | the statement for `b ≥ 4` bodies (dimension `3b−6`) is plausible, not proved |
| [10] lattice `n = 12`: H ≥ 2.2·10⁵ of 422 825; P 21; S 2 | true; H is in fact all 422 825 | `c3`: enumeration, `c^{sf}`, exact MILP for P (5, 6, 10, 10, 13, 16, 19, 21 for `n = 5..12`), brute force over singles and pairs for S (2 throughout); partition bound 219 098 | — | — | also reproduced at `ε = N/2` (P 8, S 2) and `L = 0.2` (P 4, S 1) |
| [10] off-lattice `n = 10`: H ≥ 5 539 of 8 115; P 318; S between 3 and 10 | H true (in fact all 8 115); **P is 319**; S bracket reproduced | `c4`: `c^{sf}` = 68.0, 108.8, 140.1, 176.7, 187.1,…; MILP optimal at 319 (dual bound 319); S: scaled eigenvalue bound 3, greedy cover 10 | — | — | P = 27, 48, 92, 137, 215 for `n = 5..9` reproduced exactly |
| [10] `ln Z`, lattice `n = 8`, `ε = 0.01`: H all 5 849; P 10–69; S exactly 3 | true; P bracket can be tightened to 65–69 | `c5`: H: an unevaluated state has half-width `≥ 35`; S: smallest range of `ln Z` over all pairs of evaluations is 0.2545 > 0.01, three evaluations determine everything; P: knapsack lower bound 65, my greedy + pruning 69 | — | — | — |
| [10] "216 nats against a measured 2.5" | true as a comparison of two entropies at scale `δ = 1` per bead | `c8`: bound `ln 4·⌈156⌉ = 216.3` at `n = 13`; farthest-point count 13 from my starting point (`ln = 2.56`; the author has 12) | — | — | it is not the size of a certificate of any instance; see row "Theorem 7" for `z` |
| [11] negative finding 1 (chain-length independence belongs to the exactly pair-additive class) | the theorem behind it (Cor. 15) is right; the sentence is too strong | see M2 | — | — | — |
| [11] negative finding 2 (no one-evaluation threshold independent of `N`) | numerically supported for H, P, S and `n ≤ 12`; not proved; S column needs correction | `c3`, `c13` (thresholds reproduced: lattice 0.0357/0.1034 at `n = 5`, 0.0088/0.0375 at `n = 12`; generic 0.0303/0.0536/0.0936 at `n = 5`, 0.0068/0.0234/0.0657 at `n = 9`) | — | — | see M3 |
| [12] prior art, §4 | accurate, with two omissions and one misclassification | §4 below | — | — | see m5, m6 |

---

## 2. Errors and gaps

### CRITICAL
None.

### MAJOR

**M1.  Sum class: upper bounds reported as requirements** (§2.7 after Corollary 15: "yet the sum class needs 2, 2,
7, 20 evaluations"; §1: "the certificate of a 683-state chain grows from 2 to 20"; §3.6, second table).
`e6b_sumclass.py` computes *greedy covers* (column header "sum class ub"; beyond 16 points the KR term is replaced
by the hub bound).  No lower bound is computed.  Mine (`c10b`, exact KR term throughout): greedy 2, 7, 21 at
`η = 0.5, 0.75, 1`; after backward pruning **6 and 17**.  So 7 and 20 are not minimal sizes, and what is
established is `2 ≤ N^{sum}_cov ≤ 6` at `η = 0.75` and `2 ≤ N^{sum}_cov ≤ 17` at `η = 1`.  Corollary 15 cannot do
better than 4 in this instance: the all-trans state together with three states of independent profiles makes
`σ⁻_{S,aff}` vanish and satisfies `η d_H(y,A) ≤ gap(y)` for `η ≤ 1`.  In the same passage "the pair-additive part
alone [needs] two" contradicts the report's own table of §3.3 (`S = 1` at `n = 6`, `L = 0.2`); 2 is the greedy
value from the minimiser (and the value with the constraint `Σλ = 1`).
*Fix:* "a greedy cover of the sum class has 2, 2, 7, 20 points (upper bounds; no matching lower bound)"; drop
"needs".  The qualitative statement that survives is Corollary 15 itself.

**M2.  First negative finding: two overstatements** (§1 "Most important negative finding…"; repeated in theory
report §11.17, Proposition 11.49(e), and in the research log).
(a) "The chain-length independence is a property of the *exactly* pair-additive, transferable class" contradicts
Theorem 7 of the same report (chain-length independence at extensive accuracy for the whole first-order class
`Lip(d_P)`; "pair-additivity is not used") and its Theorem 13 (a sup-norm remainder costs the floor
`η(1+‖λ‖₁)`, nothing more; with `λ = e_i` the floor is `2η` and the net of Theorem 7 serves unchanged).  What
Corollary 15 shows is narrower: independence is lost when the remainder is
only known to be first-order in an envelope whose own certificates grow with `N`.
(b) "…reinstates the exponential cost of D42 in proportion to `η`".  The only theorem available is
`N^{sum}_cov ≥ N^{ηd₀}_cov` combined with theory report Theorem 11.37 for constants `ηc_i ≥ ηc₀m_i^γ`:
`ln N ≥ n ln k − C((G+ε)/(ηc₀))^{1/(1+γ)}`.  For every fixed `η > 0` the leading term `n ln k` is unchanged; `η`
enters only the `o(n)` correction (equivalently, the number of sharp sites near the ends, `∝ (e/ηc₀)^{1/γ}`).
*Counter-statement:* "for every fixed `η > 0` the exponential cost returns in full at the zero instance; a
smaller `η` only enlarges the sub-exponential correction".  The measured growth "2 → 20" cannot be cited for
proportionality either (M1).

**M3.  Second negative finding is a measurement, and its span column is not the one-evaluation threshold**
(§1 last sentence; §3.7, table "One-evaluation thresholds").
(a) Scope: three formats, `n ≤ 12` (lattice) and `n ≤ 11` (generic), one known part; the mechanism (a hairpin with
3 gauche torsions and `‖N‖₁ = 29 → 80`, reproduced) is not turned into a proof.  "No format" should read "none of
the three formats (measured)".  What *is* provable in two lines: for every class containing `P_L`, the single
evaluation at the all-trans state certifies only if `L·dist₁(N^y, ℝN^{tt…t}) ≤ gap(y)` for the hairpin `y`.
(b) On the lattice the all-trans profile is zero, so every member of `P_L` vanishes there and the evaluation is
uninformative: the tabulated `L*_S = L*_P` is the threshold below which *no* evaluation is needed
(`(N_cov, N_value, N_point) = (0, 0, 1)` in my brute force at `L = 0.05`, `n = 5, 6`).  The largest `L` at which
some single evaluation is a cover is (`c3`)

| `n` | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|
| evaluation at all-trans (the report's `L*_S`, given there for `n = 5, 7, 9, 11, 12`; all values recomputed) | 0.103 | 0.088 | 0.063 | 0.058 | 0.053 | 0.048 | 0.040 | 0.038 |
| best single evaluation (mine) | 0.690 | 0.683 | 0.485 | 0.452 | 0.426 | 0.413 | 0.336 | 0.318 |
| the latter times `N` | 5.5 | 6.1 | 4.8 | 5.0 | 5.1 | 5.4 | 4.7 | 4.8 |

so the finding survives numerically (decay like `≈ 4.8/N`) with numbers 7 to 8.5 times larger.  Off-lattice the
all-trans profile is not zero and the evaluation must sit on the minimiser's profile at `ε = 0`; there the
report's column is the true threshold (`c13`: 0.0936, 0.0853, 0.0657 for `n = 5, 7, 9`).

**M4.  Statements of the summary (§1) that are stronger than the theorems.**
1. "span cost ∝ features, first-order cost ∝ exp(features), and the chain length enters only through the
   number of features."  Proved: span `≤ rank ≤ DT`; span `≥ n − 2ε/(Lδ₁₄)` for pair-specific classes with
   `f ≡ 0` on the product domain (`n` = number of 1–4 pairs, while the number of features is `∝ N²`);
   first-order `≤ C(M_N+DT, DT)`, which *depends on `N` at a fixed number of features* (the report's own profile
   column: 5 → 21 for `n = 5 → 12` with three features); first-order exponential only for pair-specific classes
   on the product domain.  The proportionalities are a heuristic; the last clause is false for the first-order
   format at fixed accuracy.
2. "lower bounds are linear in the number of features" (after P4(b)): only Proposition 12 (1–4 features of a
   pair-specific class); for typed classes the "feature-count law" 4 : 11 : 33 is one measurement at `N = 11`.
3. "P5 … cost between `n − 2ε/(Lδ₁₄)` (proved) and the rank `O(N²)`": proved for `f ≡ 0`, zero residual, phantom
   chain; the rank is `O(N²)` only on a lattice (off-lattice the pair-specific rank is bounded only by the
   number of distinct distance values, which can be exponential; the polynomial bound there is Theorem 8 with
   `T ∝ N²`).
4. "the last sentence of P4 is refuted … off-lattice it is at most stretched-exponential": only at the zero
   residual with `gap ≥ e·#excitations`; stated correctly in Theorem 9, compressed in the summary.
5. "the normalised entropy … saturates (`m(δ=1) = 10–12` for `N = 13…16`…)": a numerical observation in one
   model with three features (my traversal gives 12, 12, 13 at `n = 10, 12, 13`); not a theorem, and the bound of
   Theorem 7 says nothing at these sizes.
6. "H needs ≥ 2.2·10⁵ … (×2.9–3.0 per torsion, also at the extensive accuracy `N/2`)": true, but the factor is
   the growth of `|X_N|`; H is everything (m1).
7. §2.10, table of regimes: the H row (`3^{n−O(√n)}`, Theorem 11.37) is a product-domain statement, where the
   z-condition fails; the P and S rows assume the z-condition.  The three rows are simultaneously valid only for
   the lattice statements of Theorem 6 (with `M_N` in place of `zN/2`) — or with the replacement of m7.
8. "(measured: the certificate of a 683-state chain grows from 2 to 20…)": see M1.

### MINOR

**m1.  The Hamming entries are far from sharp; the exact value is "all".**  A conformation `y` is covered by
`a ≠ y` only if `L·min_i c_i ≤ gap(y) + ε`.  With `c ≥ L c^{sf}` and `min_i c_i^{sf} = 19, 23, 31, 35, 36, 40, 48, 52`
(lattice, `n = 5..12`) and `26.3, 33.5, 42.3, 50.8, 59.5, 68.0` (generic, `n = 5..10`) against `gap ≤ n`, every
conformation is covered only by itself at `L = 1`, `ε ≤ N/2`: `N^H_cov = |X_N|` exactly, for every valid constant
vector.  At `L = 0.2`: lattice `n = 12` at least 410 737 forced points (report: ≥ 44 180); generic chain all
conformations for `n ≤ 10` (report: ≥ 2 187 at `n = 10`).  The brackets `[1 027, 2 005]`, `[2 955, 5 849]`,
`[925, 1 393]`, `[2 272, 3 363]` of §3.3 all close at their upper ends.

**m2.  What a valid Hamming constant is on a self-avoiding domain** (asked by the coordinator).  `Σ_i c_i[x_i≠y_i]`
is valid for `P_L` on `X_N` iff `d_P(x,y) ≤ Σ_{i: x_i≠y_i} c_i` for all pairs of `X_N`, i.e. `Σ_{i∈S} c_i ≥ L·D_S` for
every nonempty set `S` of torsions, `D_S` the largest profile distance between two conformations of `X_N` that
differ exactly on `S`.  On a product domain the `n` single-flip conditions imply the rest (triangle inequality
along single flips); on `X_N` the intermediate states may be missing, so they do not, and the valid vectors form
a polyhedron without a least element in general.  The report handles this correctly: lower bounds use
`c^{sf}` (necessary for every valid vector; covering numbers are monotone in `c`), upper bounds the valid vector of
least sum.  I checked all pairs: `max_{x,y}[d_P − Σc^{sf}] = 0` on the lattice for `n ≤ 8` and on the generic chain
for `n ≤ 9`, so there `c^{sf}` is itself valid and is the least valid vector.  By m1 the choice does not matter in
any quoted instance.

**m3.**  Off-lattice `n = 10`, `L = 1`, `ε = 0`: `N^P_cov = 319` (MILP optimal, dual bound 319; the same with the
tolerance of the cover relation at `−10⁻⁵`, `10⁻⁷`, `+10⁻⁵`; LP relaxation 315.46; 122 classes are covered only by
themselves; `c15`).  The summary and §2.5(iv) quote 318, the lower end of the bracket `[318, 319]` in §3.3.

**m4.**  `ln Z` in the profile format: if `y` is not evaluated then `r_y ≥ δ_y` (distance to the nearest other
profile, `≥ L`), and the criterion implies `Σ_{y∉A} W_y(e^{δ_y} − e^{ε−δ_y}) ≤ (e^ε − 1)Z`; leaving out the cheapest
classes gives `N ≥ 65` at `L = 1`, `ε = 0.01` (33 at `ε = 0.1`, 41 at `L = 0.2`, `ε = 0.01`, 17 at `L = 0.05`), where
the report has 10, 10, 3, 2.  At `ε = 1` the report's bound (8) is better than mine (1).

**m5.  Lemma 11(c) is classical**, and is listed under "apparently new" in §4.1.  It is the lower bound in the
Pietsch–Stesin theorem `d_m(B_∞^n, ℓ_1^n) = n − m` (more generally widths of diagonal operators `ℓ_∞ → ℓ_1`: the
sum of the smallest diagonal entries), which the report's own search log (item 14) names.  Proposition 12 is its
application and is new only as an application.

**m6.  Prior art not cited.**  (i) Greedy selection of evaluation points for worst-case-optimal recovery, analysed
by comparing with Kolmogorov widths of the set of representers through the theorems of Binev et al. and
DeVore–Petrova–Wojtaszczyk, is the `P`-greedy algorithm of kernel interpolation (Santin–Haasdonk 2017; power
function = distance to the span = half-width of the bracket).  Theorem 8 is that argument with an `L²` detour
for an `L^∞` box.  (ii) The consistent set and the width of its bracket at a point are the version space and its
width in the eluder-dimension literature (Russo–Van Roy 2013), where "dependence on the evaluated points" for a
linear class is a distance to their span; cited from memory and a search summary only.

**m7.  `3^{n−O(√n)}` on a self-avoiding domain** (Theorem 6(c), §2.4 last paragraph, table of §2.10).  It cannot hold
there (`|X_N| ≈ 2.9ⁿ`).  The correct form follows from theory report Theorem 11.6(c), whose denominator may be
bounded by the product formula on any subdomain of the product: if the valid constants satisfy `c_i ≥ Lc₀m_i`
(`m_i` the distance to the nearer end), then for `f = e·#gauche` at the zero residual

    ln N^H_cov(ε) ≥ ln|X_N| − t(en+ε) − Σ_i ln(1+2e^{−tLc₀m_i}) ≥ ln|X_N| − 4√((en+ε)/(Lc₀))     (t = 2/√(Lc₀(en+ε))).

The growth `c_i^{sf} ≥ c₀m_i` on the self-avoiding domain is numerical (`c₀ ≈ 19` at `n = 12`).  (Referee's
derivation.)

**m8.  Proposition 12: scope and two extensions.**  (i) The remark after the proof ("on any sub-family of
conformations whose other pairs stay outside the cutoff") needs the condition that the sub-family realises all
gauche counts `0..n_t` independently for the type pairs.  (ii) The report says (§5.7) that Propositions 12 and 16(a) are proved on the product domain only.  For the
pair-specific class the proofs need nothing but that the projection on the 1–4 components contains the whole
cube, and every one of the `2ⁿ` trans/gauche patterns is realised by a self-avoiding conformation on the diamond
lattice for `n ≤ 12` and on the hard-core generic chain for `n ≤ 10` (`c9`).  So Proposition 12 and the first bound
of Proposition 16(a) (`2ⁿ/V`) hold verbatim on these domains; for larger `n` this is open.
(iii) With the known part `f = e·#gauche` the same projection sends the conformations of gap `≤ ke` onto the
points of the cube with at most `k` ones, whose absolutely convex hull contains `½{±1,0}`-vectors with `≤ 2k`
nonzero entries; the vertex argument gives `d_m ≥ (δ₁₄/2)·min(n−m, k)`, and Theorem 10(iii) at `G = (n−m)e`
gives `N^S_cov(ε) ≥ n − 2ε/(Lδ₁₄ − 2e)` whenever `Lδ₁₄ > 2e` — the threshold of Proposition 16(a).  (Referee's
derivation; `c14` is consistent with it but is not a sharp test.)

**m9.  Proposition 17, entropy.**  The claim is right; the omitted argument: measures on `Δ` with mass `≤ M`;
cut `Δ` into `n_c ≤ C(S_c/h)³` cells of `ℓ¹`-diameter `h` and move the mass to cell centres (cost `≤ Mh`); round
the mass of each cell down to a multiple of `q`, sending the remainder to the reservoir (cost `≤ n_c q S_c`);
with `h = δ/2M`, `q = δ/(2n_cS_c)` the error is `≤ δ` and the number of images is at most
`C(n_c + J, n_c) ≤ (e(1 + 2MS_c/δ))^{n_c}`, `J = M/q`; hence `ln N ≤ C(2MS_c/δ)³ ln(e(1 + 2MS_c/δ))`, and with
`M = z₃N`, `δ ∝ ε₁N/L` this is `O((z₃LS_c/ε₁)³ ln(·))`, independent of `N`.  The sentence in bold that follows
("the complexity depends on the body order through the dimension…") is an upper bound for the first-order class;
no lower bound is given, and for `b ≥ 4` bodies the covering of the `(3b−6)`-dimensional variety is asserted.

**m10.  The cited corollary.**  Corollary 3.3(ii) is quoted correctly.  Its printed proof (by contradiction from
`σ_{4s} ≤ √2γ^{−1}√(σ_{2s}d_s)`) covers indices `M ≥ 4` only and is silent on `M = 1, 2, 3`.  This does not affect
Theorem 8: there `σ_j ≤ σ₀ ≤ (zN/2)√S_c ≤ C₁j^{−1/2}` for all `j ≤ 256T` directly (`C₁ = 16(zN/2)√(S_cT)`).  Corollary 4.2(ii) (Banach:
`n^{−α+1/2+β}`) and the remark that the loss of `√n` cannot be removed in general (an example in `ℓ_∞`) are also
quoted correctly.  I read arXiv v1, not the journal version (Constr. Approx. 37, 455–466).

**m11.**  §3.3, "At `L = 0.05`: … S 1": for `n ≤ 9` the span format needs no evaluation at all (`L·‖N^y‖₁ ≤ gap(y)`
for every `y`; thresholds 0.103 … 0.053); from `n = 10` on it needs one.

**m12.**  Theorem 4 does not say that `N_value` and `N_point` can differ (they do, see §1) nor whether
`N_value = N^S_cov` always.  For the theory report: quote the theorem with both "+1" and do not write
`N_value = N_point` by analogy with Theorem 11.5.

**m13.**  §4.1, row P1: Henderson's theorem as "the statistical-mechanics shadow of the same linearity" is an
analogy (its proof is a convexity argument); harmless.

---

## 3. Independent numerical checks

All with my own code (`rp_chain.py`: diamond-lattice and generic rotamer chains, NeRF builder, enumeration with
excluded volume; `rp_lp.py`: LPs with HiGHS).  Geometry self-tests: self-avoiding counts 233, 683, 2 005, 5 849,
17 107, 49 833, 145 379, 422 825, 1 231 221 for `n = 5..13` (they agree with the report and, as far as I remember the
series 2 796, 8 196, 24 060, 70 188, …, with the diamond-lattice self-avoiding-walk counts `c_{n+2}/12`; not looked up);
generic chain 99, 239, 577, 1 393, 3 363, 8 115 for `n = 5..10`; squared distances 19/11 and 6.433/3.819.
`ulimit -v 2500000`, one thread, longest run 5 min.

| script → output | what | sizes | outcome |
|---|---|---|---|
| `c1_props123.py` → `out_c1.txt` | Prop. 1–3: definition of the class (LP over radial functions on the occurring distances) against the profile formulas | 9 models (dia/gen, phantom and self-avoiding, 1–3 types, `S_c` 10–28, `n` 4–7); 540 pairs, 360 conditioning instances with `κ ∈ {0, ½, 1}`, smooth and bang-bang slopes | all identities to ≤ 7·10⁻¹⁴; all bounds hold; half-width/`L·dist₁` = 1 at `κ = 0`, down to 0 at `κ = 1` |
| `c1b_instance.py` → `out_c1b.txt` | the instance of the correction to P3 | phantom lattice `n = 4` | reproduced exactly |
| `c2_theorem4.py`, `c2b_theorem4_strict.py` → `out_c2.txt`, `out_c2b.txt` | Theorem 4 by brute force (all sets of ≤ 3 evaluations; cover, value and point certificates by exact LPs) | 30 sub-domains of 14 conformations (5 models, random `f`, `L`, `κ`, `ε`) + 14 class-level lattice domains (22 and 37 points) | 0 failures of the three implications; resolved triples (1,1,1)×4, (2,2,2)×7, (3,3,3)×7, (1,1,2)×9, (2,2,3)×1, (0,0,1)×2, (2,2,>2)×1; 13 instances need more than 3 points |
| `c3_lattice_formats.py` → `out_c3_n9.txt`, `out_c3_n10_12.txt` | lattice, `S_c = 12`, homopolymer, `f = #gauche`, zero residual: `c^{sf}` and its validity, H, P (exact MILP), S (exact), thresholds | `n = 5..12`, up to 422 825 conformations, 356 profile classes | every number of the report's table reproduced (P: 5, 6, 10, 10, 13, 16, 19, 21; `ε = N/2`: 3, 5, 5, 5, 5, 7, 7, 8; `L = 0.2`: 2, 2, 2, 2, 3, 3, 4, 4; S: 2 / 1,1,1,1,1,1,2,2 / 1); H = all (m1); best single evaluation for S (M3) |
| `c4_gen_formats.py` → `out_c4_n5_7.txt`, `out_c4_n8_10.txt` | the same for the generic chain, `S_c = 16` | `n = 5..10`, up to 8 115 conformations, 1 360 classes, 150 features, rank 140 | P = 27, 48, 92, 137, 215, **319**; `L = 0.2`: 5, 5, 6, 9, 11, 13; S in [3,7], [3,7], [3,7], [3,8], [3,9], [3,10]; H = all (m1) |
| `c5_lnZ.py` → `out_c5_n8.txt` | `ln Z` certificates, lattice `n = 8` | 90 classes; all 4 005 pairs of evaluations | S = 3 at `ε = 0.01` and 0.1 (`L = 1`); ≤ 2 in the other four cases of the report's table; P bounds [65, 69] (m4) |
| `c6_robust.py` → `out_c6.txt` | Theorems 13, 14, Corollary 15 | 300 instances (5 models, `m ∈ {2,4,7}`, `η ∈ {0.05, 0.3, 1}`) | primal = dual; `Σλ = 1`; KR bounds; super-additivity (strict in 259/300); McShane in the sum envelope ≥ exact slack always |
| `c7_widths.py` → `out_c7.txt` | Lemma 11, Prop. 12, Prop. 16 | cube `n ≤ 6`; phantom lattice `n = 4, 5, 6` pair-specific (34, 93, 260 distinct truncated distance matrices; ranks 13, 21, 31); exact covers by MILP | all bounds hold; Bernstein and eigenvalue bounds ≤ brute-force inner widths |
| `c8_entropy_lemma.py` → `out_c8.txt` | rounding of the entropy Lemma; Theorems 7, 8 on real profile sets | 2 000 random step functions; lattice `n` up to 13, generic `n` up to 10 | error ≤ 0.72·(2SM/G); bounds hold (216 nats vs `ln 13`; Theorem 8 loose by 10²–10³) |
| `c9_patterns.py` → `out_c9.txt` | trans/gauche patterns realised with excluded volume | lattice `n ≤ 12`, generic `n ≤ 10` | all `2ⁿ` patterns realised (m8) |
| `c10b_sumclass_ub.py` → `out_c10b.txt` | sum class on the 683-state chain, exact KR term | `η = 0.5, 0.75, 1`, `L = 0.2` | greedy 2, 7, 21; pruned 2, 6, 17 (M1).  `c10_sumclass_lb.py`: an attempt at lower bounds by test functions — inconclusive |
| `c11_spot.py` → `out_c11.txt` | greedy `L¹` widths (generic `n = 8`); triangle types | 291 classes; lattice `n = 4..8` | `σ_m` = 3.67, 2.83, 0.96, 0.34 at `m = 1, 2, 4, 8` and `‖λ‖₁` 2.6/1.4 as reported; 4 and 21, 25, 27, 28, 28 triangle types as reported |
| `c12_valid_gen.py` → `out_c12.txt` | validity of `c^{sf}` on the generic chain | all pairs, `n = 5..9` | valid (m2) |
| `c13_misc.py` → `out_c13.txt` | generic-chain thresholds; lattice with seven distances; ranks with type sequences | `n = 5, 7, 9`; `n = 5, 6, 7`; `n = 8, 10` | thresholds as reported; P = 49, 102, 191 (and 12, 19, 23 at `L = 0.2`) as reported; ranks 3, 4, 9, 14 |
| `c15_p319.py` → `out_c15.txt` | robustness of `N^P_cov = 319` (generic chain, `n = 10`) | three tolerances of the cover relation; LP relaxation | 319 each time, MILP optimal (m3) |
| `c14_prop12_gapped.py` → `out_c14.txt` | referee's extension of Prop. 12 | phantom and self-avoiding lattice `n = 4`, all sets of ≤ 3 evaluations | consistent (no cover of size ≤ 3 where the bound requires 4); not a sharp test |

Adversarial rather than random elements: bang-bang true slopes (`κ = 1`) in `c1`; data at the vertex of the box
(`c1b`); jumps placed on grid points and mass at 0 in the rounding test; exhaustive search over evaluation sets in
`c2`, `c3`, `c5`; exact MILP instead of greedy covers wherever sizes allowed.

---

## 4. Literature (what I read, and how)

| item | read | finding |
|---|---|---|
| DeVore, Petrova, Wojtaszczyk, "Greedy algorithms for reduced bases in Banach spaces", arXiv:1204.2290v1 | **full text** (PDF, 12 pages, downloaded to `dl_dpw/dpw.pdf`) | Theorem 3.2, Corollary 3.3(i)–(iii), Theorem 4.1, Corollary 4.2(i)–(iii), §5 as quoted in the report.  Cor. 3.3(ii): weak greedy with constant `γ`, Hilbert space, compact `𝓕`: `d_n ≤ C₀n^{−α}` (`n ≥ 1`) ⟹ `σ_n ≤ 2^{5α+1}γ^{−2}C₀n^{−α}` (`n ≥ 1`); `σ_n = dist(f_n, span{f₀..f_{n−1}})`, greedy elements in `𝓕`.  Normalisation `‖f‖ ≤ 1` "for notational convenience only".  Proof gap for `n ≤ 3` (m10), irrelevant here.  Journal version not read |
| Podryabinkin, Shapeev, arXiv:1611.09346 | ar5iv HTML through the fetch tool (machine summary of the full text) | `C = b(x*)A^{−1}`, grade `γ = max_k|C_k|`, threshold `γ_th ≥ 1`, `E(x*) = Σ C_kE(x^{(k)})`: the report's description is accurate (square active set, zero misfit) |
| Santin, Haasdonk, "Convergence rate of the data-independent P-greedy algorithm…", arXiv:1612.02672 | ar5iv HTML through the fetch tool (machine summary) | applies Binev et al. and DeVore–Petrova–Wojtaszczyk to the set of kernel translates in the native space to bound the power function of greedily chosen points: the direct precedent of Theorem 8 (m6) |
| entropy of monotone functions (Birman–Solomyak 1967; van de Geer 1991/2000; van der Vaart–Wellner Thm 2.7.5; Gao–Wellner) | search summaries only | bracketing entropy `≤ C/ε` for uniformly bounded monotone functions; lineage as the report states; not verified in a primary source (the Lemma is proved in the report anyway) |
| Pietsch (1974), Stesin (1975): `d_n(B_p^N, ℓ_q^N) = (N−n)^{1/q−1/p}`, `q ≤ p` | search summaries (recent papers of Vasil'eva stating the theorem with this attribution) | confirms m5 |
| Maiorov–Crippen, J. Mol. Biol. 227 (1992) 876–888 | search summary (bibliographic data; described by later papers as the first use of linear inequalities over decoys) | attribution accurate |
| Milanese–Vicino, Automatica 27 (1991) 997–1009 | search summary (bibliographic data, abstract) | attribution accurate |
| Russo–Van Roy (2013), eluder dimension | search summary; definition from memory | context for m6 |
| Smolyak (1965), Micchelli–Rivlin (1977), Traub–Woźniakowski (1980), Bakhvalov, Gal–Micchelli; Soyster (1973); Henderson (1974); Figalli–Gigli (2010); Tobi et al. (2000); Tikhomirov's ball theorem; Ohlberger–Rave | **not read**; from memory the attributions are the standard ones (radius of information at zero information; adaption does not help for linear problems on balanced convex sets; column-wise box uncertainty; uniqueness of the pair potential; transport with a Dirichlet boundary) | no objection |

The "energy equation" (pair energy = pair potential integrated against the pair distribution) and the formula
`W₁ = ∫|F − G|` on the line are textbook; I did not search for them.  Assessment of §4.1 of the report: accurate
and candid, apart from m5 and m6.  The `L¹` width `≍ 1/m` and the `L²` width `≍ m^{−1/2}` of bounded monotone
functions, which the report calls its own two-line estimates, are right (lower bounds: `2m` disjoint intervals
give an octahedron in the absolutely convex hull; `d_m(B₁^{2m}, ℓ₁^{2m}) = 1`, `d_m(B₁^{2m}, ℓ₂^{2m}) = 2^{−1/2}`).

---

## 5. Faithfulness of the theory report (working tree), README, blueprint and research log

The working tree differs from commit `36ec238`; I compared the *working-tree* texts with the report.

* **Theory report §11.17, Proposition 11.49(a), last sentence** ("polynomial in `N` at every accuracy on a
  lattice") = Theorem 6(b).  Faithful.
* **11.49(b)** (`(8(1+κ)|𝒯|zLS_c/ε₁)²`, "we have not read the cited corollary ourselves") = Theorem 8.  Faithful; the
  corollary has now been read by this referee and is quoted correctly (`prior_art/L8_linear_classes.md` can be
  updated: "read in full, arXiv v1").
* **11.49(d)** ("at most stretched-exponential for a gapped site-additive known part at the zero residual") =
  Theorem 9.  Faithful.
* **11.49(e)**, "the span format needs a number of evaluations that grows at least linearly with the chain":
  Proposition 12 proves this for `f ≡ 0`, zero residual, uniform accuracy `ε < Lδ₁₄n/2`, on the product domain.
  Add these qualifiers (or use m8: self-avoiding domains with all patterns realised; gapped known part when
  `Lδ₁₄ > 2e`).  "the first-order format is exponential again (… on the product domain)": for `f ≡ 0`, or for
  `e·#gauche` if `Lδ₁₄ > 2e`.
* **11.49(e)**, "the exponential cost of D42 returns in proportion to `η` … the chain-length independence is a
  property of the exactly pair-additive, transferable class, not of chains": M2.  The second half contradicts
  part (a) of the same proposition ("pair-additivity is not used").  Suggested text: "…so a certificate is at
  least as large as the first-order certificate of the remainder alone, and with a per-torsion `d₀` whose
  constants grow with the lever arm the exponential cost of D42 returns for every fixed `η > 0` (`η` enters a
  sub-leading term) — the chain-length independence belongs to residuals that are Lipschitz functionals of the
  pair-distance statistics, up to a sup-norm remainder, not to chains."
* **11.49(e)**, "With a purely torsional known part no format has a one-evaluation threshold that is independent
  of `N`": M3 — "none of the three formats in the measurements (`n ≤ 12`)".
* **Table "Measured on the same instances"**: "≥ 2955 → ≥ 2.2·10⁵ of 422 825 (×3 per torsion)" → "all (5 849 →
  422 825)"; "all conformations for `n ≤ 7`; ≥ 5539 of 8115" → "all, for every `n ≤ 10`"; "27 → 318" → "27 → 319";
  "10–69" → "65–69"; the span entries are right (2 throughout; between 3 and 10 at `n = 10`, between 3 and 7 at
  `n = 5`; 3).  The caption "its Hamming entries are lower bounds valid for every valid vector of constants"
  stays true.
* **11.47(d)** ("workstream P, Theorem 14, with the minimum over `λ` exact"): faithful; checked numerically
  (§3, `c6`).
* **Research log, second checkpoint** ("the slacks … add, so the chain-length independence belongs to the exactly
  pair-additive class and not to chains"): same overstatement as M2(a).
* **README** ("a remainder outside the class paid at the old exponential price") and **blueprint** ("paid at
  first-order prices, i.e. exponentially for a per-torsion remainder envelope"): the blueprint wording is
  accurate; the README wording is accurate only for per-torsion first-order remainders (a sup-norm remainder
  costs an accuracy floor, Theorem 13).
* **`prior_art/L8_linear_classes.md`**, last paragraph: "the lower bound 'one evaluation per independent feature'
  for the span format (P, Proposition 12)" — per 1–4 pair (torsion), by a classical width (m5); and add
  Santin–Haasdonk for 11.49(b).
* The P report has no Lean and cites none; nothing to compare there.

---

## 6. Not checked

* Lean: none read (the report contains none; `LinearClass.lean` and `LinearKernel.lean`, cited by theory report
  §11.17, were outside this brief).
* The author's exact-rational runs (288 instances) and the 12 960 floating-point instances of §3.1 were not
  re-run as such; I ran 360 instances of my own in floating point.
* Sampled long chains (§3.2, `N` up to 960; §3.5, `N` up to 480); the `m_abs` columns behind conjecture (iii) of
  §2.5; the block-mixture heuristic `ln N ≳ cN/ln N`.
* The random-residual rows (`κ = ½`) of §3.3; the two-type rows of the certificate tables; lattice `S_c = 28`
  beyond the P column for `n ≤ 7`; `ln Z` for `n = 10` and for the generic chain; the "S pointwise (greedy)"
  column.
* Width tables of §3.5 beyond the spot check at `n = 8` (lower-bound rows, singular values, `n = 10, 12`).
* The LP dualities of Proposition 17 (`e7`); the statement for `b ≥ 4` bodies.
* The minimum certificate of the sum class (only upper bounds 6 and 17 and the trivial lower bound 2).
* Whether all trans/gauche patterns remain realisable for `n > 12` (m8), and whether `c_i^{sf}` grows linearly on
  self-avoiding domains for large `n` (m7).
* Theory report Theorems 11.4–11.6, 11.37, 11.38 were taken as given.
* Primary sources listed as "not read" in §4; the journal version of DeVore–Petrova–Wojtaszczyk.
