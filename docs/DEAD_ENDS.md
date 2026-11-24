# MetricChain — Dead Ends, Falsified Conjectures and Repaired Statements

Every entry records a claim that was believed (or hoped) at some point, the exact reason it fails
or had to be weakened, and the lesson that survived.  Entries tagged **[harness]** are reproduced
by `experiments/falsify_conjectures.py` (tests named `DEAD.*` are *expected* to be refuted);
entries tagged **[Lean]** are refuted or repaired by a machine-checked statement in `proofs/`.

---

## D1. "Dual reparameterization can strictly improve dead-end elimination" — FALSE for pairwise models  **[harness: DEAD.1] [Lean]**

*Conjecture (charter Direction A, as seeded).* Optimizing an LP-dual / tree-reweighted gauge
(moving cost between unary and pair tables) should let Goldstein-type pruning eliminate more
states than classical DEE.

*Refutation.* For a pairwise energy over a product domain, the Goldstein value
`h_i(r) − h_i(t) + Σ_j min_s [J_ij(r,s) − J_ij(t,s)]` **is the exact dominance margin**
`min_{x_-i} [E(r,x_-i) − E(t,x_-i)]` (the difference is separable in the neighbours), and the
energy function is unchanged by reparameterization.  Hence the Goldstein value is a gauge
invariant: no message can change it.  In 2 000 random instances × 5 random gauges the value never
moved (max deviation 0).

*Lean.* `PairModel.goldstein_isLeast`, `PairModel.goldstein_gauge_invariant`,
`PairModel.exactMargin_reparam` (`proofs/Frontiers/Dominance.lean`).

*What survives.* (i) The older Desmet bounds criterion *is* gauge dependent and its supremum over
gauges equals Goldstein (`desmet_reparam_le`, `desmet_optimalGauge`), i.e. Goldstein is the
gauge-optimal Desmet criterion.  (ii) Gauges matter where dominance stops being separable: 3-body
terms, non-product (pair-pruned) domains, and bound-based (non-dominance) pruning.  (iii) Prior
art: the statement is folklore and a special case of Shekhovtsov's theorem that a term-wise
criterion optimized over reparameterizations equals the LP criterion — it is recorded as a
*formalized negative result*, not as a discovery.

---

## D2. "The classical margin `> hi − lo` is the tight criterion for a residual with global bounds" — ILL-POSED as first stated  **[Lean]**

*First formulation.* With only `lo ≤ Δ_res ≤ hi` known, the Goldstein margin must exceed
`hi − lo`, and an adversarial residual shows this is tight.

*Why it had to be repaired (prior-art review, L1 §C2).*
1. Tightness of a *dominance* test is not tightness of *safe pruning*.  The exact set of states
   that can be optimal for some admissible residual is the **energy window**
   `{x : E_0(x) ≤ min E_0 + (hi − lo)}`; the Goldstein-margin rule is only a polynomial-time
   shadow of it.
2. It silently assumed the residual is never evaluated.  One evaluation at a conformation `x̂`
   already replaces the margin `hi − lo` by the pruning interval `E(x̂) − min LB` (this is exactly
   iMinDEE, Gainza–Roberts–Donald 2012).

*Repaired statements (all machine-checked, `proofs/Frontiers/EnvelopeDuality.lean`).*
`energy_window_exact` (no evaluations: the window is exact), `robust_minimizer_iff` (general
envelope: contact set), and `robust_minimizer_with_anchors_iff` (**query model**: with evaluated
anchors the exact discardable set is the set violating "contact" or "optimistic value ≤ every
competitor's pessimistic value").  The repaired theory is strictly more informative than the
conjecture it replaced.

---

## D3. Differential envelopes must be transitively closed  **[Lean]**

*Naive formulation.* Any table `δ_i(r,t) ≤ Δ(r,x) − Δ(t,x)` gives a tight pruning criterion.

*Failure.* If `δ_i` violates the triangle inequality, the implied bound is its shortest-path
closure, and a criterion using the raw table is sound but not tight.

*Repair.* `IsEnvelope` requires `d x x = 0` and the triangle inequality (asymmetry is allowed);
all exactness theorems are stated for envelopes.  A raw differential table must be closed
(Floyd–Warshall per site, `O(k³)`) before use — this is part of the blueprint.

---

## D4. "A compression argument gives the rank-constrained spectral bound" — FALSE  **[harness: DEAD.2]**

*Attempted proof.* For `G ⪰ 0` of rank `≤ r` and symmetric `A`, drop the off-diagonal blocks of
`A − G` with respect to `range(G)` to get
`‖QAQ‖² + tr(QA)²/(r+1) ≥ Σ_{k>r} λ_k² + (Σ_{k>r} λ_k)²/(r+1)` for the complementary projector `Q`.

*Counterexample.* `λ = (5, −1, −1)`, `r = 1`: compressions can reach `1.33` while the right-hand
side is `4`.  The harness finds violations for generic mixed-sign spectra (first hit: lhs 9.16
vs rhs 21.99).

*Lesson.* The rank constraint cannot be handled by a single projector when the spectrum has mixed
signs; a genuine eigenvalue-pairing inequality is needed.  The final proof uses the
Hoffman–Wielandt inequality, formalized from Birkhoff's theorem and the rearrangement inequality
(`proofs/Frontiers/HoffmanWielandt.lean`), which is why that classical theorem had to be added to
the development.

---

## D5. "The classical-MDS strain bound is within a constant of the optimal s-stress" — FALSE  **[harness: DEAD.3]**

Under a uniform additive bias of the squared distances, the strain bound
`2 (Σ_{k>3} λ_k²)^{1/2}` is `Θ(√L)`, while the true optimum is `Θ(L)`.  The trace-enhanced bound
(`rank_psd_trace_obstruction`, `sstress_lower_bound`) recovers the right order; measured ratio
`trace / strain` is 1.41, 2.0, 2.83, 4.0 at `L = 8, 16, 32, 64` (≈ `√L / 2`).  For zero-mean
noise the two bounds coincide (tail trace ≈ 0): the gain is specific to *systematic* bias
(additive-constant and scale errors).

---

## D6. Leaf rule with per-orientation pair bounds was too weak  **[Lean, kernel design]**

*First kernel.* The dual leaf bounded each ordered pair table `J_ij − m_ij` separately.

*Failure.* Instances that store an unordered pair in one orientation (`J_ij` for `i < j`,
`J_ji = 0`) then lose the message from the other endpoint: the leaf could not certify even a
single edge exactly, and the frustrated-triangle example could not be closed with fewer than
`2³` leaves.

*Repair.* The leaf bounds the *joint* reparameterized interaction of the unordered pair,
`2 p_ij ≤ J_ij(a,b) + J_ji(b,a) − m_ij(a) − m_ji(b)`; soundness needs the index-swap lemma
`sum_erase_swap`.  The repaired leaf is as strong as the pairwise LP dual.

---

## D7. Plain `decide` cannot run the kernel  **[Lean, engineering]**

`decide` reduces with the elaborator's `whnf`, which does not unfold the (irreducible) rational
arithmetic of core Lean; evaluation got stuck at `Rat.add`.  `decide +kernel` evaluates in the
trusted kernel (GMP-accelerated naturals) and adds **no** axioms (`#print axioms` shows the three
standard ones); `native_decide` was rejected because it adds `Lean.ofReduceBool`.

---

## D8. "The extremal residual for bounded differences is additive" — true for the MGF, FALSE for tails

The supremum of `ln ⟨exp(−β(Δ − ⟨Δ⟩))⟩` over the bounded-difference class (product reference) is
attained by additive two-level residuals (harness III.3; exact value in Rio 2013, Lemma 4.1).
The analogous statement for *tail probabilities* is false: the optimal-uncertainty-quantification
solution of Owhadi et al. (2013, Thm 5.2) is not additive.  Consequence: the free-energy
sandwich is sharp as a statement about `ln Z`, but it must not be converted into claims about
extremal tail events.  Also: for general marginals the per-site quantity is a `sup` over subsets,
not a `max`.

---

## D9. Coaxial alignment is not the optimal superposition  **[harness: V.1]**

The closed form `2S − 2√(S² − 4 I_A I_B sin²(φ/2))` is the exact optimum over rotations *about the
torsion axis*; the true Kabsch optimum (free rotation and translation) can be smaller (observed
ratio true/bound down to ≈ 0.2, up to 0.98).  It is therefore stated as an upper bound
("`RigidWithin`"), not as an identity.  A first version of the harness also "refuted" the closed
form because of a too-coarse angular scan; the test now evaluates the analytic minimiser
`ψ* = arg(I_A + I_B e^{iφ})`.

---

## D10. Reduced-inertia chain bound is not tight for random errors

The chained bound accumulates in `ℓ¹` (triangle inequality of the Kabsch pseudo-metric), whereas
independent torsion errors accumulate in `ℓ²`.  Measured: bound/actual ≈ 3 at 8 torsions, ≈ 10 at
96 torsions (benchmark B7).  It is a *worst-case* certificate (coherent errors); a variance-aware
version would need a probabilistic statement and is left open.

---

## D13. Audit script: substring error detection and a lost exit code  **[engineering]**

The audit script flagged "errors in AxiomAudit output" whenever the output contained the substring
`error` — which the valid theorem names `boltzmannAvg_prune_error` and
`boltzmannAvg_dominance_error` do.  One commit was pushed while the script reported this failure,
because its output had been piped through a filter and the pipeline's exit status was that of the
filter.  The content of that commit was sound (build and axiom audit passed), but the incident
violated the "audit passes at every checkpoint" rule.  Repairs: the script now matches Lean's
diagnostic format (`path:line:col: error` / `error(...)`) instead of a substring, and commits are
gated on the script's own exit code.

---

## D12. "The trace-enhanced spectral bound is new" and "it is tight on vertex-transitive inputs" — both WRONG  **[harness: DEAD.4]**

*Novelty.*  The bound `min_X ‖D̂ − Δ(X)‖² ≥ 4 Σ_{k>r} λ_k² + (4/(r+1)) τ²` was derived here from
scratch and logged as a discovery.  The third literature check located it, constants included, in
Sonthalia, Van Buskirk, Raichel, Gilbert (NeurIPS 2021, Prop. 1 with their relaxation
inequality), and the K-identity in Tsang–Pereira (2016).  The claim was withdrawn; what remains is
a machine-checked proof (we know of no earlier formalization).

*Equality.*  It was also claimed that the bound is attained whenever `D̂` is invariant under a
transitive group ("vertex-transitive inputs").  The harness test supporting it used regular
polygons with `r = 2` only.  Counterexample: regular simplex, `L = 5`, `r = 3` — bound `1.25`,
optimum `≈ 1.3043`; circulants with `r = 3` are strict too.  The argument silently assumed that
the projector onto *the* top-`r` eigenspace has constant diagonal, which fails when the cut at
`r` splits a degenerate eigenspace.  Correct sufficient condition: the top-`r` spectral subspace
is a union of full eigenspaces invariant under the symmetry group, and the shifted eigenvalues
stay nonnegative.

*Lesson.*  A sharpness test must vary every parameter of the claim (here `r`), and an
"independently derived" inequality is not a new inequality until the literature check says so.

---

## D11. Claims that prior-art review showed to be known (no novelty claimed)

| Claim | Status after review | Reference |
|---|---|---|
| Tree-like LP-bounded branch-and-bound is exponential on disjoint frustrated triangles | KNOWN | Basu, Conforti, Di Summa, Jiang 2023 (Thm 2.2); Jeroslow 1974 |
| Hölder "temperature-rescaled" decomposition of `ln Z` | KNOWN (weighted mini-bucket) | Liu & Ihler 2011; Wainwright et al. 2005 |
| Free-energy sandwich from Jensen + bounded differences | KNOWN-IN-SPIRIT | Gourgoulias et al. 2020; Rio 2013; McDiarmid 1989 |
| Uniform sub-Gaussian free-energy bound ⇔ T₁ transport inequality | KNOWN | Bobkov & Götze 1999 |
| Goldstein exact for pairwise models, gauge invariance | FOLKLORE | Shekhovtsov 2014/2016; de Givry et al. 2013 |
| Verified interval branch-and-bound in Lean 4 | EXISTS | LeanCert (2026); girving/interval |
| Trace-enhanced s-stress lower bound and the K-identity | KNOWN | Sonthalia et al. 2021; Tsang & Pereira 2016 |
| Cycle-holonomy triangle bound | KNOWN | Lerman & Shi 2022 (Lemma 1) |
| TM-score lower bound from frame-aligned errors | KNOWN | Jumper et al. 2021 (SI 1.9.7) |

These remain in the development as machine-checked building blocks and are labelled as such in
`docs/THEORY_REPORT.md`.
