# Referee report on workstream D
("Free-energy estimation in statistical mechanics; other observables; continuous spaces; structured classes")

Reviewed: `<session scratch>/ws/D/REPORT.md`
(793 lines; identical to `docs/workstreams/D_REPORT.md` except for the directory line), scripts `s01`–`s12`
(read only to see what was computed), outputs `out/`, `lean/{ComparisonDip,SetDip,RefMeasure}.lean`.
Referee directory: `<session scratch>/referee_D/`
(own scripts `r*.py`, their outputs `out/*.out`, own Lean scratch `RefereeD_Relation.lean`, literature extracts
`txt/`).  Date: 2026-11-24.  I had no part in the work.  Nothing in the repository was modified.
Repository state: I first read the theory report at commit `973ad6e` plus uncommitted changes and re-read
Theorems 11.27–11.28 at commit `459319d` (where 11.28(d) is the hint-free class threshold for every alphabet and
11.28(e) is workstream B's Theorem B.12); all references below are to `459319d`.  All four Lean scratch files were
type-checked again at that commit.

Notation as in the report: class `𝒢 = {g : g(x) − g(y) ≤ d(x,y)}`, slack `s`, `π_g ∝ e^{−β(f+g)}`, `u = βc`,
`(ε/2, δ)`-correct = within `ε/2` with probability `≥ 1 − δ` on every member of the class.

---

## 0. Summary

**No critical error was found.**  All technical headline statements survived a line-by-line re-derivation and
independent numerics with my own code.  The weaknesses are of a different kind: one *false* statement in the list
of negative results, several statements in the summary that are stronger than what is proved, overlaps with
workstreams A, B and E that are larger than the report says, and small inaccuracies.

1. **Theorem 13 (second-order dichotomy at `w = βc₂n = 4`) is correct.**
   (b) (droplets, `w > 4`) is *completely proved*: membership of `−c₂T(r − d_H(x,y))` in `𝒢₂(c₂)` (the mixed second
   difference over a 2-face equals `±Δ²φ(k₀)` with `Δ²φ ∈ {0, c₂}`, also across the boundary of the support because
   `T(0) = T(−1) = 0`; brute force `n ≤ 10`, every radius), the support `B(r−1)`, the ratio
   `2^{−n}Σ_k C(n,k)e^{βc₂T(r−k)}`, the averaging bound `E|Q(0)| ≥ (1−2δ)2ⁿ/|B(r−1)|`, the limit `Ψ(w,ρ)`, the
   identity `Ψ(w,½) = max_m[wm²/8 − I(m)]` and its positivity iff `w > 4`.  Both rows of the `w`-table (ten
   numbers) and all fourteen entries of the `(u,w)` table were reproduced.
   (a) (`w ≤ 4`, star + annealed heat-bath Glauber) is a *correct proof sketch with standard tools*; I re-derived
   every step and supplied the parameter choices (Appendix A).  The Dobrushin (column-sum) condition
   `α = (n−1)tanh(βc₂/4) < 1` holds for every member of the class and for every point `λ ∈ [0,1]` of the annealing
   path (the path is in the coupling `λ`, not in `β`; `f` and `g_star` are additive and do not enter), because
   `|D_iD_jE_λ| = λ|D_iD_jg| ≤ c₂`; at `w = 4` one still has `1 − α > 1/n`, so mixing costs a factor `n` more
   (`T ≤ n² ln(n/τ)` steps); correctness on the *whole* class needs nothing more because correctness is required only
   on members and every member (with every unbounded additive part) satisfies the condition; the evaluation count
   `O(K³ε^{−2}ln(K/δ)·n ln(nK/ε)/(1−α))`, `K = ⌈wn⌉`, includes the `K` ratio estimates (it is `≈ n⁵ε^{−2}` up to
   logarithms at `w = 4`).  Checked numerically: exact influence matrices, spectral gaps and TV decay on 20 members
   (`n = 8`), an end-to-end run against exact enumeration (`n = 10`, errors `≤ 0.008`), and the complete failure on a
   planted droplet at `w = 8` (`n = 1000`: estimate `0.000`, truth `22.79`).
   Caveats: the dichotomy is asymptotic in `n` at fixed `w` (at `w = 5` the lower bound is only `e^{3.9}` at
   `n = 2000`); the droplet family coincides with the "second-order dips" of workstream E (Theorem A there,
   `c·C(r−d,2)₊`, radius shifted by one), which the author had not seen; the cost for `w > 4` above `n·f_CW(w)` is open
   (stated).
2. **Continuous spaces (Lemma 5, Theorem 6) are correct.**  The extremal 1-Lipschitz function on the circle for the
   Jensen gap (indeed for every convex functional) is the tent `|θ − θ₀|`, value `ln(sinh b/b)`, `b = βLπ/2`; the
   proof (isoperimetry ⇒ quantile function is `Lπ`-Lipschitz ⇒ convex domination by the uniform law) is complete.
   Tensorisation, the McDiarmid constant (`N = 8Σb_i² ln(2/δ)/(ε−J)²`), the cone-dip lower bound and its positivity
   iff `ε < J` (via `b − Λ₁(b) = ln(sinh b/b)`) were re-derived; all table entries reproduced.  In the continuum the
   dip is the same cone `−(C − Σ_iL_i|x_i − y_i|)₊` with a uniformly random centre, and the packing bound is a
   Chernoff bound on the volume of an `ℓ₁` ball.  "Exponential" means exponential in the number `n` of angles at
   extensive accuracy `ε = nε₁`, `ε₁` below the mean of `ln(sinh b_i/b_i)`; for fixed `n` the cost below `J` is only
   polynomial in `b`, and "threshold exactly `J`" is a statement about exponents.
3. **Boltzmann averages (Theorem 12) are correct**, including the negative headline.  `H = ½tanh(u/2)` is the exact
   half-range; the three rows of the table were reproduced in all 24 entries; `ε_set(u)/H` goes from `1/√2` (`u → 0`,
   derived analytically) to `0.8743` at `u = 8`.  Parts (a), (b) are sketches in the report; I completed (b) with
   explicit uniform bounds (Appendix B) and confirmed it with exact binomial type counts for `u = 1, 2, 8` and
   `n ≤ 25 600`, and by brute force at `n = 12`.  Single dips give only `(½ − ρ₀)tanh(u/2)`; type-class dips give
   `ε_set`: single dips are indeed not extremal for this observable.  The upper bound (c) is valid but is an
   instance-wise statement *with the zero residual as a hint*; the summary omits this.
4. **Lean.**  The three scratch files type-check (no errors, no `sorry`, axioms `propext, Classical.choice,
   Quot.sound`) and state what the prose says, with one nuance (closed, not open, dominance set).  They contain no
   mathematics beyond the repository: I machine-checked that the comparison dip is the repository's `genDip` with
   `Φ = g̃ − g`, that the author's randomised competitor theorem follows from repository lemmas alone, and that the
   key step of Theorem 2 is `mass_ge_of_twoMeasureBound` (`RefereeD_Relation.lean`).  All four files also
   type-check at commit `459319d`.
5. **Free-energy differences, ranking, staging.**  Proposition 10 is correct in the hinted, instance-wise model
   (threshold `V_A + V_B` for uncoupled product macrostates; ranking governed by the loser).  "Staging cannot help on
   the first-order class" is true only in the sense "staged protocols obey the same lower bounds"; as worded it is
   an overstatement (§2, M2).
6. **Literature.**  Verified in the primary sources: Holzmüller–Bach Proposition 9, Lemma 3, Theorem 8, Table 1 and
   the open problem (full text); Jarzynski (2006) Eq. (34) `N ∼ exp(β W̄_diss^{reverse})` (full text);
   Chatterjee–Diaconis (abstract).  The Zwanzig/Widom reading of `Λ(y)/β` is a correct identity.  I could **not**
   run web searches (the session's search budget was exhausted), so "no minimax or instance-wise threshold found"
   is not independently confirmed.
7. **What is wrong or overstated** (details in §2): (M1) "mean-based hint-free procedures cannot beat the passive
   width" and the open bracket `[0.1138, 0.1225]` are refuted by Theorem 11.28(d),(e) of the theory report (commit
   `459319d`; I agree with that correction and found no counterexample) and by my own computations; (M2) "staging cannot help"; (M3) the upper bound for averages is
   hinted; (M4) Theorem 2 is "new in this generality" only nominally; plus thirteen minor points.

---

## 1. Verdict per statement

"Depth": S = short argument with standard tools, M = moderate, the proof has one real idea.
"Novelty": relative to the theory report (commit `459319d`, Theorems 11.27–11.28), the other workstream reports and the
literature I know or read.

| # | statement | correct? | how checked | depth | novelty | remark |
|---|---|---|---|---|---|---|
| 1 | Lemma 1 (comparison dips; competitor form), Cor. 1′ | yes, in the closed-set form | Lean type-check of `ComparisonDip.lean`; re-derivation; own Lean proof from repository lemmas; 19 005 random numerical instances | S | none in content: it is Theorem 11.27(a,b) under `Φ = g̃ − g`; the dissipated-work reading is a new formulation | the displayed "`π_g̃ > e^{−ε}π_g`" should be "`≥`" (m1) |
| 2 | Set dips, set soft gap (`SetDip.lean`) | yes | Lean type-check; it is #1 with `g̃ = U_T` | S | special case of `genDip` (`Φ = s(·,T)`) | — |
| 3 | Theorem 2 (upper half at every finite instance) | yes | proof re-derived; 40 random non-product instances with arbitrary quasi-metrics, all polytope vertices, 39 881 alternatives, 0 violations; minimax equality checked by LP; own Lean `theorem2_key_step` | S | nominal: `mass_ge_of_twoMeasureBound` is already stated for arbitrary `X`; new is only the definition `V(g) = min_Q K_g(Q)` | on a general instance only an upper statement; "threshold" is meaningful on products (M4) |
| 4 | Theorem 3 (products: two-reference inequality, `V = ΣV_i`, exponent bound) | yes | (a) is `twoMeasureBound_prod` (repository, [V]); exact enumeration of all vertices on 12 random two-site products: game value `= V₁+V₂` to `2·10⁻¹⁵`; (c) re-derived | M | none (workstream A, Theorems 11.27(c), 11.28(a–c)); independent confirmation | — |
| 5 | Corollary 4 (homogeneous sites: threshold = Laplace functional, no hint) | yes | both halves re-derived; values for cube, `k`-point, cycle, circle recomputed | S–M | modest: Theorem 11.25 beyond the cube; follows from 11.28(c) + symmetry + passive sandwich | (b) needs site-dependent `φ_i` when the `c_i` differ (m7) |
| 6 | §2.3 table (single dips not extremal for `≥ 3` states) | yes | all five rows recomputed (closed forms and own game LP) | — | none (A) | "`≥ 3`-state sites" is too general: the flat 3-state site is not a counterexample (m2) |
| 7 | Lemma 5 (circle: tent is extremal in the convex order) | yes | proof re-derived; exhaustive over all extreme points for `m ≤ 22` (705 432 at `m = 22`), LP vertex ascent at `m = 120` (40/40 starts), 20 000 convex-order tests, 0 violations | M (classical) | classical in substance, as the report says | — |
| 8 | Theorem 6 (torus threshold `Σ ln(sinh b_i/b_i)`) | yes | re-derived (constants included); table reproduced; 2-D tensorisation by LP ascent; exact `ℓ₁`-ball volumes; simulation of the estimator | M | apparently new; an application of the pattern of Theorem 11.25 | "exactly" in the exponent sense (m6) |
| 9 | Proposition 7 (fixed `d`: order `(B/ln B)^d`) | lower bound yes; upper bound plausible | lower bound and the Brunn–Minkowski step in `ℝ^d` re-derived; order checked against Holzmüller–Bach (full text) | S | order known; instance-wise constants routine | upper bound is a sketch, with hint |
| 10 | Remark 8 (`ℓ₂` constant: dimension-free, `exp(Θ(B²))`) | numbers yes | `B²π²/24`, `B²π²/30` and the exponent `(J−ε)²/(4J)` recomputed | S | — | matching upper bound not written (m9) |
| 11 | Lemma 9 (`RefMeasure.lean`) | yes | Lean type-check; 145 272 random tests incl. weights with zeros, 0 violations, bound attained | S | restatement of `detection_weight_ge` | — |
| 12 | Proposition 10 (free-energy differences; `V_A+V_B`; ranking) | yes, hinted and asymptotic | (a)–(e) re-derived; (a) on 19 005 random instances | S | corollaries | (e): "exactly one evaluation more" → "at most one" (m3) |
| 13 | Proposition 11 (averages: linear-fractional identity, hinted sampler) | yes | re-derived; identity tested on 20 000 instances | S | new, simple | — |
| 14 | Theorem 12 (magnetisation) | yes; (a),(b) sketches completed by me | exact type counts `n ≤ 25 600` (`u = 1, 2, 8`); brute force `n = 12`; table (24 entries) reproduced; (c): 13 500 random tests of the inequality, 0 violations; design search | M | new; the most interesting negative result of the report | upper bound is hinted (M3); rates near `ε_set` are tiny |
| 15 | Theorem 13 (second-order dichotomy) | (b) yes, complete; (a) yes, sketch completed; (c) yes | see §0 item 1 and §3 | M | (b)'s family = workstream E, Theorem A; the thermal dichotomy and (a) are new | asymptotic in `n` (m5) |
| 16 | §2.6(i) "staging cannot help" | the argument proves less than the heading | logical check | S | — | M2 |
| 17 | §2.6(ii) few-body classes | yes | standard (anchored decomposition) | S | known | — |
| 18 | §2.7 item 6, §5 item 3 (mean-based hint-free procedures; open bracket) | **false / superseded** | LP ascent over the whole class (`n ≤ 4`); sandwich of Theorem 11.28(d) on 68 000 residuals of two-site products; exact LPs for a three-state site | — | — | M1; I agree with the correction made in Theorem 11.28(d) |
| 19 | Positioning (Holzmüller–Bach; Jarzynski; Chatterjee–Diaconis; Zwanzig/Widom) | yes, with small imprecisions | primary sources, see §4 | — | — | m4, m10 |

**Overlap with Theorems 11.27–11.28 of the theory report and with other workstreams** (the report is candid
about A; it understates B and E):

* Lemma 1 ≡ Theorem 11.27(a,b): `min(g, g̃ − C) = genDip g (g̃ − g) C`; `g̃ ∈ 𝒢 ⇔ g̃ − g` is slack-Lipschitz;
  `softGapOf(g̃ − g) = ln Z(g) − ln Z(g̃)`; conversely `genDip g Φ C = min(g, (g+Φ) − C)`.  All four facts and the
  derivation of `thermal_prob_hit_competitor` from `prob_query_ne_ge`, `genDip_admissible`, `genDip_sensitive`,
  `genDip_ne_imp_lt` alone are machine-checked in `RefereeD_Relation.lean`.  Corollary 1′ is
  `genDip_expected_queries_ge(_exp_weights)` for finite families.  `SetDip.lean` is the case `Φ = s(·,T)`.
* Theorem 2 ≡ `mass_ge_of_twoMeasureBound` (Theorem 11.28(b), already for arbitrary `X`) + Jensen's inequality for
  decreases + hedged spot-check; relative to 11.28(c) it differs by the symmetric hedge `V/2` and the explicit
  `N = 4βS ln(1/δ)/(ε − V)`.
* Theorem 3 ≡ 11.28(a), 11.28(c), 11.27(c); §2.3 ≡ consequences (i), (ii) of 11.27.
* The numbers `0.1137 / 0.1138 / 0.1225` of §2.2 are those of Theorem 11.28(e) (workstream B, Theorem B.12);
  Theorem 11.28(d) (one reference law, every alphabet) *closes* the question that §5 item 3 of the report calls
  open and refutes §2.7 item 6 (M1).
* Theorem 13(b): the droplet `c₂T(r − d)` is workstream E's second-order dip `c·C(r′ − d, 2)₊` with `r′ = r+1`
  (E, Theorem A, machine-checked there against `MixedDiffBound`).  E treats the minimum only; the thermal
  statement, the Curie–Weiss threshold and the Dobrushin half are D's.
* Not in 11.27–11.28 and, as far as I can tell, new: Corollary 4, Lemma 5/Theorem 6 (application), Propositions
  10–11 (corollaries), Theorem 12, Theorem 13 (thermal dichotomy).

---

## 2. Errors and gaps

### CRITICAL
None found.

### MAJOR

**M1. A false negative result, and a bracket that is already closed.**
*Location:* §2.7 item 6 ("Mean-based hint-free procedures cannot beat the passive width: adding a second
reference `Q` costs the transport term …, which cancels the gain"); §5 item 3 ("the minimax threshold … lies
between `sup_gV(g)` and the passive width (`0.1138` and `0.1225` per site in the two-state example) and needs a
multi-instance lower bound or an algorithm that is not mean-based"); last sentence of §2.2; §4.5.
*Counter-statement (two states).*  For identical two-state sites (`f = e·M`, all `c`-Hamming-Lipschitz residuals)
sample the *tilted* product reference `π_{θ*}` (Gibbs measure of the additive instance `θ*M`, where the tangent of the
pressure `P(θ) = ln(1+e^{−β(e+θ)})` is parallel to its chord over `[−c,c]`) and return
`ln Z(f+θ*M) − β·mean(g − θ*M) + nε₁*/2`.  This uses no hint, is mean-based, and is correct on **every** admissible
`g` up to `nε₁*/2` plus the sampling error, with `ε₁* = max_θ G(θ) = sup_θ V(θM)`; in the report's example
(`e/c = ½`, `β = 1`) `ε₁* = 0.11383 < 0.12246`.  This is Theorem 11.28(e) of the theory report (workstream B,
Theorem B.12).  *Independent check* (`r27_meanbased.py`): the maximum over **all** `c`-Lipschitz `g` on `{0,1}ⁿ` of
the Jensen gap `ln E_{π_θ}e^{−β(g−θM)} + βE_{π_θ}(g−θM)`, by LP vertex ascent from 60 starts, is `n·0.12246` at
`θ = 0` and `n·0.11383` at `θ = θ* = −0.0372c`, for `n = 2, 3, 4`.
*Counter-statement (every alphabet): Theorem 11.28(d) of the theory report, with which I agree.*  For one site
with known part `f₁` and class `𝓛`, and a law `Q`, put `F_Q(ψ) = ln Σ_a e^{−β(f₁+ψ)} + βE_Qψ`, `M(Q) = max_𝓛 F_Q`,
`m(Q) = min_𝓛 F_Q`.  Then every admissible `g` on `Sⁿ`, additive or not, satisfies
`n·m(Q) ≤ ln Z(f+g) + βE_{Qⁿ}g ≤ n·M(Q)`: both ends refer to the *same* law `Q`, so no transport term appears, and
sampling `Qⁿ` and averaging `g` is a mean-based hint-free procedure of width `n(M(Q) − m(Q))`.  I re-derived the
statement (the upper end is the two-measure bound for the weights `e^{−βf₁}` and `h = −g`; the lower end tensorises
by the same conditioning argument, in the opposite direction; `m(Q) = F_Q(γ)` when `Q` is the Gibbs law of `γ ∈ 𝓛`
by the Gibbs variational principle; `sup_γ ε₁^thr(γ) = min_Q[M(Q) − m(Q)]` by Sion's theorem, the payoff
`M(Q) − F_Q(γ)` being convex in `Q` and concave in `γ`), and checked it numerically (`r28d_hintfree.py`,
`r28e_hintfree_lp.py`): the sandwich holds on 68 000 admissible residuals of two-site products (McShane members,
additive vertices, single dips, set dips; the two-state site, the three-state site `(0,0,2)` and a random
asymmetric three-state site; five or six reference laws each), with both ends attained to `10⁻¹⁵`; for the site `(0,0,2)`,
`β = c = 1`, exact LPs give `ε₁^thr(0) = 0.11969 < ε₁* = sup_γ ε₁^thr(γ) = M(Q*) − m(Q*) = 0.11988 < W₁(0) = 0.12208`,
as the theory report states, with `Q* = (0.4707, 0.4707, 0.0586)` the Gibbs law of the additive instance
`γ* = (0, 0, 0.0836)`; for a random asymmetric three-state site `ε₁* = 0.1159 < W₁(0) = 0.1243`.  **I looked for a
counterexample to the correction and found none; the remark of the report is false, the correction is right.**
Hence the minimax hint-free threshold of a class of identical sites is exactly `ε₁* = min_Q[M(Q) − m(Q)]`, it is
strictly below the passive width of the known part in these examples, and it is reached by a mean-based procedure.
*What remains true:* pairing the Jensen bound under `π_f` with an upper bound under a *different* law `Q` does pay
the transport term `β(E_π − E_Q)g`; that is the only content of the remark.  What is still open (theory report,
"What is not proved") is the cost below the thresholds and known parts with interactions, not the threshold of
the class.
*Fix:* delete §2.7 item 6 or restrict it to the last sentence; rewrite §5 item 3, the end of §2.2 and §4.5
accordingly (the bracket `[0.1138, 0.1225]` is closed at `0.1138`).

**M2. "Staging cannot help on the first-order class."**
*Location:* §1 (iv); heading of §2.6(i); §2.6(iv), first row; §4.4 row 14.
*What is proved:* a staged protocol (annealing, thermodynamic integration, Jarzynski/AIS, replica exchange) is an
adaptive randomised query algorithm and therefore obeys Theorems 11.22–11.25, Lemma 1 and Theorem 3(c).  That is
all, and it is immediate.
*What is not proved, and is false in its natural reading:* that staging or adaptivity gives no advantage.
(i) The bounded-cost algorithms above an instance threshold are *hinted*; (ii) the hint-free exponent below the
threshold is open even on the cube (Theorem 11.25: between `≈ u²/32` and `ln cosh u`), and nothing excludes that a
staged scheme improves on plain Monte Carlo there; (iii) adaptivity provably helps without a hint on additive
instances: star + spot-check costs `n(k−1)+1+O(1)` evaluations (theory report, "Without a hint"), exponentially
fewer than non-adaptive sampling from the reference.  The companion phrase "the class is a lattice, which is
*exactly* what makes hidden perturbations possible" is also too strong: closure under minima is sufficient for the
splicing of Lemma 1, not necessary — `𝒢₂(c₂)` is not a lattice and has hidden perturbations for `w > 4` (the
report's own Theorem 13(b)).
*Fix:* "on a lattice class no protocol, staged or not, removes the exponential cost below the threshold; whether
staging improves hint-free exponents is open."

**M3. The upper bound for Boltzmann averages is hinted and instance-wise; the summary does not say so.**
*Location:* §1 (iii) ("a bounded number of samples suffices above a level that is within 1 % of that bound");
Theorem 12, third table row and the sentence "a threshold exists, it lies in the bracket of the last two rows".
Theorem 12(c) itself says "for the hint `g ≡ 0`".  So the bracket `[ε_set, η_up]` concerns the cost *at the zero
residual* of algorithms that are given that residual and evaluate everything once a difference is detected.  In
contrast with `ln Z` on homogeneous spaces (Theorem 11.25(b), Corollary 4(a), hint-free on every instance), no
hint-free algorithm with error below the trivial `H` (output `½`) is given, and nothing is proved at other
instances.  *Fix:* add "with the instance as a hint, at the zero residual" in §1 and in the table caption, and list
the hint-free question in §5.

**M4. Novelty labels (not mathematics).**
(a) Theorem 2, "[P; N in this generality]" and the title "the threshold of an instance is a game value": the
proof is correct, but its key step is the repository's `mass_ge_of_twoMeasureBound`, which is already stated for an
arbitrary finite space and an arbitrary slack; with `γ := K_g(Q)` the hypothesis `TwoMeasureBound` holds by the
definition of `K_g` (machine-checked: `theorem2_key_step`).  The new content is the definition of `V(g)` for
non-product instances.  Moreover on a general finite instance there is no lower half (below `V(g)` the cost need
not be large), so "threshold" is justified only on products with extensive accuracy, i.e. in workstream A's
Theorem B.  *Fix:* label Theorem 2 [R] and call `V(g)` an upper bound.
(b) Theorem 13(b): cite workstream E, Theorem A, for the membership of the parabolic profile (same function,
radius shifted by one) and claim novelty for the thermal statement only.
(c) Lemma 1 and the three Lean files: the report says correctly that §§2.1–2.3 are independent confirmations of
workstream A.  For the record, the coincidence is exact (machine-checked equivalence, §1), so the scratch files
contain no statement that is not a corollary of `GeneralisedDips.lean` / `SoftGapBounds.lean`; what is new in §2.1
is the dissipated-work formulation.

### MINOR

**m1. Open versus closed dominance set** (§2.1, displayed statement; §1).  The Lean theorem gives, for every `C`
with `βC > ln Z(g) − ln Z(g̃) + ε`, a queried point with `g̃ − g < C`; the intersection over all such `C` is
`{ℓ_g̃ ≤ ε} = {π_g̃ ≥ e^{−ε}π_g}`.  The displayed set `{π_g̃ > e^{−ε}π_g}` is smaller, and the statement with it is
false in degenerate cases (`ε = 0`, `g̃ = g + const`: the set is empty).  The strict form does hold whenever some
point has `ℓ_g̃ > ε`.  *Fix:* "`≥`", or "for every `ε′ > ε`".

**m2.** §1 "Negative" and §2.7 item 1: "single dips are not extremal on product spaces with `≥ 3`-state sites"
should read "need not be": for the flat 3-state site point dips are optimal for the threshold and for the exponent
at `ε₁ = 0` (my LP: `0.11950` and `0.03065` for both families at `u = 1`), as the report's own table says.

**m3.** Proposition 10(e): "costs exactly one evaluation more than `ln Z`" → "the two costs differ by at most one
evaluation" (`ln π(y) = −βE(y) − ln Z`, in both directions).

**m4.** §1 and Proposition 7: "Proposition 9 is *exactly* 'optimisation lower bound minus the soft gap
`d·ln(1+3B)`'".  In the source the subtracted term is the bound of their Lemma 3 on `|M_f − L_f|` (with
`|f|₁ ≤ √d·B`), valid for every member; it is an upper bound of the same order as the soft gap of the flat
instance (`≈ d ln B − ln(d!ω_d)` for an `ℓ₂`-Lipschitz class), not that soft gap.  Also their error criterion is the
expected absolute error, not `(ε,δ)`.  The substance of the comparison is right.

**m5.** Theorem 13: the dichotomy is a statement at fixed `w` as `n → ∞`.  Exact numbers (`ε = 1`): the lower
bound `(1−2δ)2ⁿ/|B(r−1)|` is `e^{1.5}, e^{3.9}, e^{22.8}, e^{204}` for `w = 5` at `n = 200, 2 000, 2·10⁴, 2·10⁵`, and
`e^{6.3}, e^{42}, e^{396}` for `w = 8` at `n = 200, 2 000, 2·10⁴`.  Conversely the proof of (a) works for
`w ≤ 4 + O(1/n)` (e.g. `w = 4 + 4/n` gives `1 − α ≈ n^{−2}`).  The provable cost at `w = 4` is `≈ n⁵ε^{−2}` up to
logarithms (at `n = 10` my run of the provable schedule used `10⁸` evaluations for `2^{10}` states).  This should
be said next to "sharp dichotomy" and "polynomial iff `w ≤ 4`".

**m6.** Theorem 6: "the threshold is exactly `Σ ln(sinh b_i/b_i)`" is a statement about exponents (`n → ∞`,
`ε = nε₁`); for fixed `n` and `ε < J` the bound is polynomial in `b` and may be trivial; for heterogeneous `b_i`
"exponential in `n`" needs `J − ε = Ω(n)`.  The report says this in the theorem, not in §1.

**m7.** Corollary 4(b) is written with one site function `φ` for all sites, whereas `J₁(βc_i)` may be attained by
different functions for different `c_i` (for the `k`-point site `j*` depends on `u`).  The proof works verbatim with
site-dependent `φ_i`; without them "the threshold is exactly `Σ_iJ₁(βc_i)`" does not follow for unequal `c_i`.

**m8.** Theorem 12.  (a) "iff `τ < 1 − ρ₀`" is for `τ ≥ ½`; in general the condition is `ρ₀ < min(τ, 1−τ)` (the
worst levels are the two corners, where the density is `1`).  (b) The limit of the shift is approached only at rate
`n^{−1/2}`, because the first group sits at the stationary type `1−q` (left derivative of the exponent zero): exact
value `0.5663H` at `n = 25 600` against the limit `0.5731H` (`u = 1`, design at 80 % of `a₀*`).  The exponential rates
are small: `−max_k ln density_k = 7.1, 22.2, 42.0` at `n = 3 200, 12 800, 25 600` for that design.  Neither affects the
theorem; both belong in the statement of what "exponential" means here.  A complete proof is in Appendix B.

**m9.** Remark 8: "`exp(Θ(β²L²))`" — only the lower half is argued.  The upper half is one line: plain Monte Carlo
with Chebyshev needs `e^{2B²}/(δ(1−e^{−ε/2})²)` samples since `E e^{−2β(g−Eg)} ≤ e^{2B²}` (Herbst) and
`E e^{−βg} ≥ e^{−βEg}`; the lower bound from the additive competitor is `exp((J−ε)²/(4J))`, `J = B²π²/24`.

**m10.** Attributions (§2.6 remarks, §4.3).  Levin–Luczak–Peres prove cut-off at `[2(1−β)]^{−1}n log n` for
`β < 1`, order `n^{3/2}` at `β = 1`, and `O(n log n)` for the dynamics restricted to one phase for `β > 1`; the
exponential slowdown for `β > 1` is older (Griffiths–Weng–Langer 1966, quoted there) [the latter from memory].
Eldan–Koehler–Zeitouni / Kunisky: the condition is on the spread `λ_max − λ_min` of the coupling matrix (`≤ 1 − ε`
fast, `≤ 1 + ε` hard under a low-degree conjecture), not on the spectral norm.  Harris–Kolmogorov claim optimality
up to logarithms for the estimation of the counts.  Adjacent prior art that should be cited next to Theorem 13:
Jain–Koehler–Mossel (COLT 2018, "The vertex sample complexity of free energy is polynomial") and Borgs et al. —
free energies of dense (mean-field-scaled) models from samples, in a different oracle model and for explicit
order-`r` interactions; and, for "uniqueness threshold = complexity threshold" in the white-box setting,
Weitz (2006) and Sly (2010) [from memory].

**m11.** Lemma 9, extension to weights with zeros "by continuity": one line is missing.  When the hypothesis is
tight, the perturbed weights `ν + t` satisfy it only with a slightly different `η_t`; one needs that the conclusion
is monotone in `η` (it reads `η·A ≥ B` with `B ≤ 0`, so it holds for all `0 ≤ η ≤ η′` if it holds at `η′`).  With
this the argument is complete; numerically 0 violations in 145 272 tests, 36 000 instances with zeros.

**m12.** §4.1: "formally a Widom insertion formula" is a loose analogy (Widom's formula is a particle insertion);
the precise name of `e^{−Λ(y)} = ⟨e^{−βs(·,y)}⟩_π` is the Zwanzig free-energy-perturbation identity with the slack as
perturbation.  The identities listed there (`Λ = min_Q[βE_Qs + KL(Q‖π)]`, `βE_{π_y}s ≤ Λ ≤ βE_πs`,
`βE_πs − Λ = KL(π‖π_y)`) are correct.

**m13.** Proposition 10(d) ("cheap iff `Δ > V_B`") holds in the hinted model, with `N = O(βS_B ln(1/δ)/(Δ − V_B))`
samples on the cheap side and with a product loser and an extensive margin on the exponential side; "iff" is in
this threshold sense.  The report says "hinted" at the end of (d), not in §1.

### Statements of the summary (§1) that are stronger than what is proved

1. "on the first-order class staging cannot help" (M2).
2. "a bounded number of samples suffices above a level …" for averages — hinted, at one instance (M3).
3. §2.7(6) "mean-based hint-free procedures cannot beat the passive width" — false (M1).
4. "the class is a lattice, which is exactly what makes hidden perturbations possible" (M2).
5. "single dips are not extremal on product spaces with `≥ 3`-state sites" (m2).
6. "must probe … a configuration where that switch dissipates less than `ε/β`" — at most `ε/β` (m1).
7. "their Proposition 9 is exactly … the soft gap `d·ln(1+3B)`" (m4).
8. "a sharp dichotomy at `w = 4`", "polynomial iff `w ≤ 4`" — asymptotic at fixed `w` (m5).
9. "the threshold is exactly `Σ_i ln(sinh b_i/b_i)`" — in the exponent sense (m6).
10. "everything is dimension-free, `exp(Θ(β²L²))`" — upper half not written (m9).
11. "certifying a ranking is cheap iff …" — hinted model (m13).
12. "The Gibbs probability of a single state costs exactly one evaluation more" (m3).

---

## 3. Independent numerical checks

All code is mine (plain Python, numpy/scipy/mpmath), in the referee directory; outputs in `out/`.  The author's
scripts were read only to see what had been computed.

| script | what was checked | sizes | result |
|---|---|---|---|
| `r13a_droplet.py` | Thm 13(b): `max_{x,i<j}|D_iD_jg_y|/c₂`, support `= B(r−1)`, closed form of `Z'/Z` | all `2ⁿ` points, all pairs, `n = 2..10`, every `r = 0..n+1`, random centres | max is `1.000000` (values of `|D_iD_j|/c₂` are exactly `{0,1}`), support and ratio exact; three other parabolic profiles (`m²/2`, `C(m,2)`, `(m+1)²/2`) are also members |
| `r13f_capped.py` | Thm 13(c): slope-capped droplets in `{|D_ig| ≤ c₁} ∩ {|D_iD_jg| ≤ c₂}` | `n = 6, 8, 10`, all `r`, 4 pairs `(c₁,c₂)`, 96 cases | all members |
| `r13b_tables.py` | `f_CW(w)`, `ρ*(w,0)`, exponent `ln 2 − h_b(ρ*)`, `ε₁^crit(u,w)`; exact finite-`n` radius and bound | grids of `2·10⁶` points; `n` up to `2·10⁵` | all entries of the three tables reproduced (`0.0359, 0.1152, 0.3265, 0.8094`; `0.0010, 0.0051, 0.0196, 0.0556`; 14 entries of `ε₁^crit`); `f_CW ≈ ¾((w−4)/4)²` near `4`; exact `r/n → ρ*`, exact exponents converge to the limits from above |
| `r13c_dobrushin.py` | Thm 13(a): exact influence matrix (max over all configurations), column and row sums, spectral gap of heat-bath Glauber, worst-start TV after 60 steps | `n = 8`; 10 members (Curie–Weiss ±, random ±c₂ pairwise, 3 droplets, 3 random many-body members with large additive parts, a radial member) × `w ∈ {4, 2}` × `λ ∈ {0, 0.3, 0.7, 1}` | column sum `≤ (n−1)tanh(βc₂/4)` (saturated by Curie–Weiss: `0.8703` vs `0.8705`), gap `≥ (1−α)/n` (smallest `0.067` vs `0.016`), TV `≤ n(1−(1−α)/n)^T`; 0 violations |
| `r13d_anneal.py` | Thm 13(a) end to end: star, `K = ⌈wn⌉` stages, cold-started chains of the provable length `T = n ln(8nK/ε)/(1−α)`, 3 000 chains per stage, against exact enumeration | `n = 10`, 4 members × `w ∈ {4, 2}` × 3 runs | all 24 errors `≤ 0.008` (target `ε/2 = 0.25`); `10⁸` evaluations at `w = 4` |
| `r13e_planted.py` | droplet above the threshold: exact `ln(Z'/Z)`, measure of the support, annealing from a typical start (lumped chain) | `n = 1000, 4000` | `22.793, 52.521, 43.476` and `e^{−19.5}, e^{−50.5}, e^{−19.0}` as in the report; my annealed estimate at `n = 1000`, `w = 8`: `0.0000` (truth `22.79`) |
| `r06a_circle.py` | Lemma 5: maximum of `ln E e^{−u(φ−Eφ)}` over all extreme points of the Lipschitz polytope of `ℤ_m`; convergence; LP vertex ascent | exhaustive `m = 8..22` (705 432 patterns at `m = 22`), `b ∈ {0.25, 1, 5}`; LP ascent `m = 120`, 40 starts, `b ∈ {0.5, 2, 8}` | the tent (one up-run, one down-run) is the maximiser in every case; values converge to `ln(sinh b/b)` (`0.161439` at `b = 1`, `m = 20 000`); 40/40 starts end at the tent |
| `r06b_convex_order.py` | Lemma 5, full convex-order statement against the discrete tent | `m = 4000`; 2 000 Lipschitz functions of 5 kinds × 10 convex `Ψ` | 0 violations (tolerance `10⁻¹⁰`) |
| `r06c_torus.py` | Thm 6: table; `b − Λ₁(b) = ln(sinh b/b)`; `E(ε₁;b) > 0` iff `ε₁ < J₁`; exact volume of the `ℓ₁` ball (Irwin–Hall, 80+ digits); maximum Jensen gap on `ℤ_m²` by LP ascent; the passive estimator | `n ≤ 160` for volumes; `m = 6, 8`, 3 parameter sets, 25 starts; 3-torus on a `48³` grid, 60 members × 30 runs | table reproduced (`0.0104 … 16.31`; `0.0026 … 1.384`); `−ln(vol)/n` decreases to `E(0;b)` from above; best 2-D value found = additive tent = sum of the site values to `10⁻⁸`; Jensen gaps in `[0.0009, 1.7165]` (grid value of `J = 1.7096` is slightly larger); 0 failures in 1 800 runs at `δ = 0.1`, `N = 1767` |
| `r12a_magnetisation.py` | Thm 12 table: single-dip ratio, `ε_set/H`, `η_up/H` | `u ∈ {0.01, 0.1, 0.5, 1, 2, 3, 4, 6, 8, 12}` | the 24 entries of the report reproduced; `ε_set/H → 0.70711` as `u → 0`; `0.8743` vs `0.8746` at `u = 8` |
| `r12b_exact.py` | Thm 12(a),(b) with exact binomial type counts: `ln`(mass), exact shift of `⟨O⟩`, `max_k ln density_k` | `u ∈ {1, 2, 8}`, designs at 80/90/97 % of `a₀*`, `n = 800..25 600`; single dips at `n = 3 200, 12 800` | e.g. `u = 1`, 80 %: mass `e^{371}`, shift `0.5663H` (limit `0.5731H`), `max_k ln density = −42.0` at `n = 25 600`; `u = 2`, 80 %: `e^{1267}`, `0.5889H` (limit `0.5919H`), `−119.0`; single dips: shift `(τ−½)tanh(u/2)` to 4 digits, density `e^{−107}` for `τ < 1−ρ₀` and `1` for `τ > 1−ρ₀`; above `a₀*` no admissible depth exists |
| `r12e_bruteforce.py` | validation of the type-level formulas and of the Lipschitz property of type-class dips | all 4 096 configurations, `n = 12`, 4 designs | exact agreement |
| `r12c_upper.py` | range `[q, 1−q]`; identity of Prop. 11; inequality of Thm 12(c); `η_up` vs unconstrained design; Prop. 10(a) and Lemma 1 | 20 000 Lipschitz functions (`n = 5`); 13 500 tests (`n = 3..6`, both signs of `t`); 7 values of `u`; 19 005 random instances with random quasi-metrics | 0 violations everywhere (minimal slack `0.058` in (c)); `η_up` equals the unconstrained two-group design value to 5 digits (the report's [num] remark) |
| `r12d_designs.py` | can unequal two-group or three-group designs beat `ε_set`? | grids `97×241²` and `121³`, `u ∈ {0.5, 1, 2, 4}` | no |
| `r23_table.py`, `r23b_vertices.py` | §2.3 table; two-state numbers of §2.2; point / set / all-vertex game values | closed forms; own LP for the site `(0,0,2)` and flat sites; 60 random sites with 3–5 states, all polytope vertices enumerated | every number reproduced (`0.02841/0.02914`, `0.0194/0.0309`, `0.0891/0.1195`, `0.0093/0.0309`, `0.0247/0.0290`, thresholds; `0.11367`, `0.11383` at `θ* = −0.0372c`, `0.12246`, `0.3137`); `V_all > V_set` in 55/60 of my sites (the report: 41/60 in its ensemble) |
| `r02_theorem2.py` | Thm 2: `V(g)` by LP over all vertices, minimax equality, both inequalities and the conclusion of the hedged spot-check | 40 random non-product instances (`|X| = 3..5`, random quasi-metric), 39 881 alternatives | 0 violations; `V < J` strictly in all 40 |
| `r03_tensor.py` | Thm 3(a): game value of a product by exact enumeration of the vertices of the product polytope | 12 two-site products (`2×2`, `2×3`, `3×2`) | `|V − (V₁+V₂)| ≤ 2·10⁻¹⁵`, and `K(Q₁*⊗Q₂*) = V₁+V₂` |
| `r09_refmeasure.py` | Lemma 9 including weights with zeros | 145 272 tests, 36 000 instances with zeros | 0 violations; bound attained (min ratio `1.000000`) |
| `r27_meanbased.py` | M1: maximum Jensen gap over the whole class with tilted and untilted reference | `n = 2, 3, 4`, LP ascent, 60 starts | `n·0.12246` (untilted), `n·0.11383` (tilted) |
| `r28d_hintfree.py` | M1 / Theorem 11.28(d): the one-reference sandwich `n·m(Q) ≤ ln Z(f+g) + βE_{Qⁿ}g ≤ n·M(Q)` for arbitrary admissible `g` | two-site products of a two-state site, the site `(0,0,2)` and a random asymmetric three-state site; 5–6 laws `Q` each; 68 000 residuals | 0 violations, both ends attained; two-state `ε₁* = 0.1138` at the Gibbs law of `θ*` |
| `r28e_hintfree_lp.py` | Theorem 11.28(d) for the site `(0,0,2)`, `β = c = 1`, with exact LPs; minimax identity | grid `81²` over additive instances + refinement | `ε₁^thr(0) = 0.11969`, `ε₁* = sup_γ ε₁^thr(γ) = M(Q*) − m(Q*) = 0.11988`, `W₁(0) = 0.12208` (the theory report's numbers) |

Lean (each `lake env lean <file>`, 6–25 s, exit code 0; run at the first reading and again at commit `459319d`):
`lean/ComparisonDip.lean`, `lean/SetDip.lean`, `lean/RefMeasure.lean` of the author — no errors, no `sorry`,
`#print axioms` gives `[propext, Classical.choice, Quot.sound]` for all six printed theorems;
`RefereeD_Relation.lean` (mine) — `cmpDip'_eq_genDip`, `genDip_is_cmpDip`, `admissible_iff_competitor_lipschitz`,
`softGapOf_competitor`, `prob_hit_competitor_from_repo`, `theorem2_key_step`, same axioms.

Comparison of the Lean statements with the prose.  `thermal_prob_hit_competitor`: hypotheses `0 ≤ β`, both
residuals admissible, correctness with probability `≥ 1−δ` on every admissible residual (finite mixture of
deterministic algorithms, as in the repository), `ln Z(g) − ln Z(g̃) + ε < βC`; conclusion: probability `≥ 1 − 2δ`
that a queried point has `g̃ − g < C` — as in Lemma 1 (direction of inequalities correct), except for m1.
`thermal_prob_cover_set`: needs `IsEnvelope d` (for the admissibility of `U_T`), `T` nonempty, `Λ(T) + ε < βc`;
conclusion `slackTo < c`, with `slackTo d g T x = min_{y∈T} s(x,y)` — as in the prose.  `detection_weight_ref`:
`ν > 0`, `β > 0`, `η ≥ 0`, `IsEnvelope d` — as in Lemma 9; the case of zeros is a paper argument (m11).

---

## 4. Literature

What I read (2026-11-24).  Web *search* was not available to me (the shared search budget of the session was
exhausted before my first query), so everything below was retrieved directly from primary sources with known
identifiers; I could not search for prior art of the new claims.

* **Holzmüller & Bach, "Convergence rates for non-log-concave sampling and log-partition estimation"**,
  arXiv:2303.03237v4, JMLR 26 (2025) 1–71 — **full text** of the abstract, §1 (Definitions 1–2, Lemma 3), §2.2
  (Theorems 7, 8, Proposition 9, Theorems 11–12, Table 1) and the proofs of Theorem 8 and Proposition 9 in
  Appendix B.2.  Confirmed: Lemma 3 `|M_f − εL_{f/ε}| ≤ εd log(1 + 3d^{−1/2}|f|₁/ε)`; Theorem 8
  `O(min{Bn^{−m/d}, exp(CBn^{−m/d})Bn^{−1/2−m/d}})`; Proposition 9 `≥ Ω(Bn^{−m/d}) − d log(1+3B)`, proved by
  reduction to optimisation plus Lemma 3; "optimization regime" `Bn^{−m/d} ≥ C log(1+B)` and "quadrature/sampling
  regime"; "We leave a lower bound outside of the optimization regime as an open problem"; the bump technique for
  the deterministic and sampling lower bounds.  The report's description is accurate (m4 for the word "exactly").
  The order `(B/ln B)^d` for `m = 1` at constant accuracy indeed follows from Theorem 8 and Proposition 9.
* **Jarzynski, "Rare events and the convergence of exponentially averaged work values"**, arXiv:cond-mat/0603185v1
  (Phys. Rev. E 73, 046105) — **full text** of the abstract, the introduction and Section III.  Confirmed:
  Eq. (34a) `N_c^F ∼ exp(β W̄_d^R)` (the number of forward realisations is governed by the mean dissipated work of
  the *reverse* process), dominant realisations = typical realisations of the reverse process, and "analogous
  results apply to the equilibrium perturbation method".  The report quotes it correctly.  Note that the report's
  dominance set `{ℓ_g̃ ≤ ε}` contains Jarzynski's dominant region (it has `π_g̃`-mass `≥ 1 − e^{−ε}`) but can be much
  larger; the analogy is a reading, not an identity.
* **Chatterjee & Diaconis, "The sample size required in importance sampling"**, arXiv:1511.01437v3 (Ann. Appl.
  Probab. 28, 2018) — abstract and first page: sample size `≈ exp(D(ν‖μ))` necessary and sufficient, cut-off.
  Correctly quoted.
* Abstract pages (tool summaries): **Ge–Lee–Lu** arXiv:1911.03043 (lower bound `d^{1−o(1)}/ε^{2−o(1)}`, as quoted);
  **Levin–Luczak–Peres** arXiv:0712.0790 (see m10); **Kunisky** arXiv:2307.12581 (see m10); **Harris–Kolmogorov**
  arXiv:2007.10824 (`Õ(q/ε²)` samples; optimality claimed for counts); **Štefankovič–Vempala–Vigoda**
  arXiv:cs/0612058 (schedule of length `O*(√ln A)`); **Jain–Koehler–Mossel** arXiv:1802.06129 (not cited by the
  report; adjacent to Theorem 13, see m10).
* Zwanzig (1954), Widom (1963): not accessed; the identities attributed to them are standard and the algebra
  `F[f+U_y] − F[f+g] = −β^{−1} ln⟨e^{−βs(·,y)}⟩_π = Λ(y)/β` is correct (`U_y − g = s(·,y)`).
* Not accessed: He–Zhang, Guo–Tao–Chen, Bobkov–Houdré–Tetali, Alon–Boppana–Spencer, Ahlswede–Zhang, Yu,
  Bollobás–Leader, Novak, Eldan–Koehler–Zeitouni, Wu–Kofke, Hahn–Then, Shenfeld et al., Weissler / Emery–Yukich
  (log-Sobolev constant `1` of the circle — correct to my knowledge), Griffiths–Weng–Langer.

*Novelty, as far as I can judge without a search.*  I know of no prior statement of (i) an accuracy threshold
between bounded and exponential query cost for `ln Z` over a Lipschitz class on a high-dimensional torus,
(ii) the hardness of Boltzmann averages relative to free energies in this black-box model, or (iii) a query
dichotomy at the Dobrushin/Curie–Weiss point for a class defined by mixed second differences.  (iii) has clear
white-box relatives (uniqueness thresholds as complexity thresholds; spectral conditions for Glauber dynamics) and
the vertex-sampling literature on dense free energies; these should be cited.  "No minimax or instance-wise
threshold found" is the author's search result; I confirm only that Holzmüller–Bach contains none beyond the
fixed-dimension regime boundary `Bn^{−m/d} ≍ log(1+B)`.

---

## 5. Not checked

* The author's exact LPs for general observables (`s02`: Charnes–Cooper programs, 44 instances), the optimal-support
  computations (`s04b`), the type-class-dip search for `ln Z` on biased binary sites (`s06`, `s06b`: 33 parameter
  sets), the large-`n` exact values and the `K₄×K₄` LP of §2.3 (`s07`, `s07b`), the Monte Carlo against tilted dips
  at `n = 400` (`s08b`) and the `n = 14` enumeration (`s08c`), the `e^{−0.2}` / `e^{−172}` example of §2.2, the `n = 4000`
  lumped-chain run at `w = 3.5`.  I reproduced the corresponding *statements* by other means where indicated in §3.
* The linear program "over all multi-group designs" of Theorem 12(b) (I only searched two-group designs with
  arbitrary split and three equal groups) and the conjecture that `ε_set` is the true threshold.
* Proposition 7 beyond the lower bound and the Brunn–Minkowski step in `ℝ^d` (the torus version "for supports that
  lift" and the hinted upper bound are plausible sketches); the estimate `(nb/ε)ⁿ` for deterministic certificates.
* The constants in Proposition 10(d) for `K` macrostates (the structure of the argument is right).
* Negative results 2, 3, 4, 8, 9 of §2.7 (computations of the author; nothing in my checks contradicts them).
* Whether the cone-dip exponent `E(ε₁;b)` of Theorem 6 is the true exponent (stated as open), and everything listed
  as open in §5 of the report.
* Constants in the evaluation count of Theorem 13(a) beyond the derivation in Appendix A; non-homogeneous `c_ij`.
* Literature: see the list at the end of §4; no search for prior art was possible.

---

## Appendix A.  Theorem 13(a): what is proved and what is a sketch

Proved in the report (and re-derived): (1) `|g − g_star| ≤ c₂·C(k,2)` at Hamming distance `k` from the anchor
(Theorem 11.16), hence `β|r| ≤ w(n−1)/2`; (2) `Z_{k+1}/Z_k = E_{π_k}e^{−βr/K}` with integrand in
`[e^{−1/2}, e^{1/2}]` for `K = ⌈wn⌉`, and `Z_0 = Z(f+g_star)` is a product; (3) for `E_λ = f + (1−λ)g_star + λg` the
log-odds of `x_i` given the rest change by `βλ|D_iD_jg| ≤ βc₂` when `x_j` is flipped, so the total-variation
influence of `j` on `i` is at most `tanh(βc₂/4)` for **every** `g ∈ 𝒢₂(c₂)`, every `λ ∈ [0,1]`, every additive `f`
(additive parts of any size drop out); (4) path coupling for single-site heat-bath updates: two configurations
differing at `j` coalesce with probability `1/n` and separate with probability at most
`n^{−1}Σ_{i≠j}tanh(βc₂/4)`, so the expected Hamming distance contracts by `1 − (1−α)/n`,
`α = (n−1)tanh(βc₂/4) ≤ (n−1)w/(4n) ≤ 1 − 1/n` for `w ≤ 4`, and `TV ≤ n(1−(1−α)/n)^T` from every start; each step
needs one new evaluation of `g`.

Left as a sketch ("Hoeffding and a union bound … give the stated count"); a complete choice is: let
`ρ₀ = e^{1/2} − e^{−1/2}`, `t = ε/(8√e·K)`, `τ = t/ρ₀`, `T = ⌈n ln(n/τ)/(1−α)⌉`, `M = ⌈ρ₀² ln(2K/δ)/(2t²)⌉`
independent chains per stage.  Then the law of each sample is within `τ` of `π_k`, its mean of `e^{−βr/K}` within
`t` of `Z_{k+1}/Z_k ≥ e^{−1/2}`, the `K` sample means are simultaneously within `t` of their expectations with
probability `≥ 1 − δ`, and each logarithm is off by at most `2t/(e^{−1/2} − 2t) ≤ 4√e·t = ε/(2K)` (for `ε ≤ 2K`).
Total: `n + 1 + KMT = O(K³ε^{−2}ln(K/δ)·n ln(nK/ε)/(1−α))` evaluations, i.e. `O(n⁵ε^{−2}·polylog)` at `w = 4` and
`O(n⁴ε^{−2}·polylog/(1−w/4))` for `w < 4`.  Nothing is missing; the theorem holds as stated.

(b) is complete in the report.  (c): the capped profile has first differences `min(c₁, c₂(r−k)) ≤ c₁` and second
differences in `[0, c₂]`; the formula for `ε₁^crit(u,w)` follows as in (b).

## Appendix B.  Theorem 12(b): completion of the sketch

Fix `u`, `q = 1/(1+e^u)`, `a₀ ∈ (q, a₀*(u))`, and `ρ ∈ (ρ_lo, ρ_hi)` with
`ρ_lo = [ln 2 − ½h_b(q) − ½h_b(a₀)]/u`, `ρ_hi = (1−q−a₀)/2` (the interval is nonempty iff `a₀ < a₀*`).  Let `n` be
even, `R = ⌊ρn⌋`, `T*` the type class `(K₁,K₂) ≈ ((1−q)n/2, a₀n/2)`, `g′ = −c(R − d_H(x,T*))₊`.
(i) `d_H(x,T*) = |k₁−K₁| + |k₂−K₂|` for `x` of type `(k₁,k₂)`; `g′` is `c`-Lipschitz (checked by brute force,
`n = 12`).
(ii) Mass: `Z′/Z − 1 ≥ 2^{−n}|T*|(e^{uR} − 1) ≥ c_u(n+1)^{−2}exp(n[½h_b(q) + ½h_b(a₀) − ln 2 + uρ]) → ∞`
exponentially (`c_u > 0` absorbs the rounding of `R`, `K₁`, `K₂`).
(iii) Excess measure: on the support the exponent
`½h_b(b₁) + ½h_b(b₂) − (u/2)(|b₁−(1−q)| + |b₂−a₀|)` is strictly concave in each variable on each side and is
maximal at `(1−q, a₀)` because both coordinates lie in `[q, 1−q]`; hence `⟨O⟩_ν → (1−q+a₀)/2` and, by the identity
of Proposition 11, the shift tends to `(a₀−q)/2` (rate `n^{−1/2}`, m8).
(iv) Support: types with `|b₁−(1−q)| + |b₂−a₀| < 2ρ`, hence `b₁ − b₂ ≥ δ := (1−q−a₀) − 2ρ > 0`.  Since
`h_b'' ≤ −4`, `h_b((b₁+b₂)/2) − ½h_b(b₁) − ½h_b(b₂) ≥ (b₁−b₂)²/2`, and with `C(n,k) ≥ e^{nh_b(k/n)}/(n+1)`:
`density_k(supp) ≤ (n+1)(n/2+1)e^{−nδ²/2}` for **every** level `k`.
(v) Pair version of the detection principle for `g′∘σ` and its mirror image, `σ` a uniform coordinate
permutation: a fixed point of level `k` lies in the two supports with probability
`≤ density_k + density_{n−k}`, so for every `η < (a₀−q)/2` and `n ≥ n₀`

    E|Q(0)|  ≥  (1 − 2δ_fail) · e^{nδ²/2} / (2(n+1)(n/2+1)).

Letting `a₀ ↑ a₀*` gives every `η < ε_set(u) = (a₀* − q)/2`.  My exact counts agree with (ii)–(iv)
(`r12b_exact.py`: e.g. `u = 2`, `a₀` at 80 %: `max_k ln density_k = −5.6, −16.9, −61.1, −119.0` at
`n = 800, 3 200, 12 800, 25 600`).

## Appendix C.  Files

Referee scripts and outputs: `r02_theorem2.py`, `r03_tensor.py`, `r06a_circle.py`, `r06b_convex_order.py`,
`r06c_torus.py`, `r09_refmeasure.py`, `r12a_magnetisation.py`, `r12b_exact.py`, `r12c_upper.py`, `r12d_designs.py`,
`r12e_bruteforce.py`, `r13a_droplet.py`, `r13b_tables.py`, `r13c_dobrushin.py`, `r13d_anneal.py`, `r13e_planted.py`,
`r13f_capped.py`, `r23_table.py`, `r23b_vertices.py`, `r27_meanbased.py`, `r28d_hintfree.py`, `r28e_hintfree_lp.py`;
`out/*.out`; `RefereeD_Relation.lean`;
`lean_*.log` (type-check logs of the author's files); `txt/hb.txt`, `txt/jar.txt`, `txt/cd.txt` (text of the three
papers read in full or in part; the PDFs are in `dl_*`).
