# MetricChain — Dead Ends, Falsified Conjectures and Repaired Statements

Every entry records a claim that was believed (or hoped) at some point, the exact reason it fails
or had to be weakened, and the lesson that survived.  Entries tagged **[harness]** are reproduced
by `experiments/falsify_conjectures.py` (tests named `DEAD.*` are *expected* to be refuted);
entries tagged **[Lean]** are refuted or repaired by a machine-checked statement in `proofs/`.

---

## D1. "Dual reparameterization can strictly improve dead-end elimination" — FALSE for single-site (Goldstein-type) tests on pairwise models  **[harness: DEAD.1] [Lean]**

*Scope (added after the referee report, `reviews/R1` item 3).*  The refutation below concerns
single-site tests with a context-independent dominator.  It must not be read as "the gauge does
not help dominance-type pruning": multi-site improving maps (maximum persistency) and bound-based
pruning are gauge dependent, and on a binary ferromagnetic chain no single-site test fires
although one reparameterisation bound certifies the improving map `x ↦ 0…0`.

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

---

# Findings of the independent adversarial audit (session 1, after the second formalization batch)

An independent reviewer compared every documented claim with the Lean statement behind it and
looked for vacuous or circular theorems.  No forbidden construct and no vacuous headline theorem
was found, but the following claims were wrong or stronger than what had been proved.  Each entry
states what was claimed, what was actually true, and the repair.

## D14. "The bounded-difference free-energy sandwich holds for a pairwise / tree-structured reference" — FALSE  **[Lean] [harness: DEAD.5, III.6]**

*Claim (theory report §0.2/§3.2/§7 and blueprint §6.4, as first written).*  For the reference
ensemble `μ₀ ∝ e^{−βE₀}` and a residual with bounded differences `c`,
`ln(Z/Z₀) + β⟨Δ⟩₀ ≤ β² Σ_i c_i²/8`, and `KL(reference ‖ target)` obeys the same bound for any
sampler of the reference.

*What was proved.*  `bounded_differences_sandwich` and
`kl_reference_target_le_bounded_differences` assume a **product** reference `∏_i p_i(x_i)`; the
documentation dropped the hypothesis.

*Counterexample.*  Two binary sites, `μ₀` uniform on `{00, 11}` (perfectly correlated),
`Δ = x₁ + x₂`, `c = (1, 1)`, `β = 1`: the gap is `ln cosh 1 ≈ 0.434 > 0.25 = β² Σ c_i²/8`.
Correlation lets single-site variations add coherently.

*Repair.*  Product reference stated wherever the `Σ c_i²` width is used; the counterexample is
now a Lean theorem (`correlated_reference_counterexample`); for an arbitrary reference the
verified statement is the Hoeffding width `β²(Σ_i c_i)²/8`
(`bounded_differences_sandwich_any_reference`, harness III.6); widths for weakly dependent
references are quoted as known results and are not formalized.

*Lesson.*  A documented theorem must be read back against its Lean hypotheses line by line; the
phrase "the reference ensemble" silently generalised a statement about independent sites.

## D15. Kernel soundness theorems that were vacuous on bad inputs  **[Lean]**

*Residual kernel.*  `verifyR_sound` quantifies over the residual class of the published data.  The
kernel checked neither `c ≥ 0` nor compatibility of the anchor values, so for unsatisfiable data
the theorem was vacuously true and the kernel accepted absurd bounds: anchors `(0,1,0) ↦ 0` and
`(1,1,0) ↦ 10` with `c = 1/4` certify `L = 41/4` on a problem whose pairwise minimum is `1`
(`inconsistentResidual_unguarded`).

*Partition kernel.*  `zverify_sound` assumed nonnegative factors, which `zverify` did not check;
with a negative one-body factor the returned "interval" `(−1, −9)` misses `Z = −4`
(`negativeW_unguarded`).

*Repair.*  `RProblem.Consistent` is decidable and is *exactly* non-emptiness of the residual
class (`RProblem.consistent_iff_nonempty`); the top-level kernels `verifyRTop`, `zverifyTop` check
the side conditions, and `verifyRTop_sound`, `zverifyTop_sound` have no hypothesis left for the
caller.  The Python reference checker and the conformance vectors were extended accordingly.

*A second-order correction found while repairing — itself corrected by the re-audit (D19).*
Soundness of lower bounds needs only `value ≤ Δ(anchor)` (`ResidualLowerClass`), which is what a
producer with floating-point evaluations can guarantee, and for rounded-down values the exact
pairwise check would be wrong (rounding can violate it for a legitimate producer).  The first
repair therefore introduced a second entry point that checked only `c ≥ 0`.  That design could
never refute an envelope; the final design uses interval anchor data, see D19.

*Lesson.*  "Sound for every member of the class" must come with "the class is non-empty", and
every hypothesis of a soundness theorem must be either checked by the kernel or discharged by
another theorem.

## D16. "SE(3)-invariant residual" was formalized as E(3)-invariance  **[Lean]**

`RigidInvariant` quantifies over all isometries, reflections included, although the blueprint
recommends chirality-sensitive (pseudoscalar) features, which are not reflection-invariant; and
the uniform constant promised by the docstring ("exactly the constants required by
`ResidualClass`") did not exist as a theorem.  Repair: invariance is parametrised by a submonoid
`G` of motions (`RigidInvariantIn`); the torsion bounds hold whenever `G` contains the rotations
about the torsion axis, which is true for the proper motions (`residual_torsion_move_in`,
`residual_torsion_move_min_in`); `residual_torsion_move_uniform`,
`residualLowerClass_of_rigidWithinIn` and `verifyR_sound_invariant` carry the statement down to
the kernel's residual class, with a concrete non-degenerate witness in `AxiomAudit.lean`.
Remaining gap, stated in the documents: the group `SE(3)` is not defined in Lean; the verified
statements are for an arbitrary group containing the axis rotations, instantiated for the group
generated by the rotations about one axis and a residual that is not reflection-invariant
(`signed_offset_residual_torsion_bound`, `Δz_not_rigidInvariant`).

## D17. "Two semirings, one certificate algebra — the same rules" — OVERSTATED

The partition kernel has leaf, branch and thermal-prune rules but no decomposition rule: the
tropical `sum` rule (`min(E₁+E₂) ≥ min E₁ + min E₂`) has only a one-sided finite-temperature
analogue (Hölder), which is proved as a theorem but is not a rule of `zverify`.  The claim was
reworded; a two-sided product rule for independent sub-instances (tree elimination) is listed as
a natural extension.  *(Cycle 7: the extension now exists — cut and elimination rules, with
separation theorems; see D22.)*

## D18. The voxel pipeline assumed its key hypothesis; smaller overstatements  **[Lean]**

* `certified_voxel_partition` took as a hypothesis that the rational weights bracket each voxel
  integral, and nothing derived it.  Closed by `VoxelBridge.lean`
  (`pairwise_voxel_weight_bounds`, `certified_torsion_partition`) for pairwise energies on
  product voxels.
* "Exactly the interval" for the robust optimum / partition function was proved only as a
  bracket plus attainment of the endpoints.  Now a theorem: every intermediate value is attained
  (`robust_min_interval_exact`, `robust_partition_interval_exact`).
* The separation "with `sum` strictly smaller than every sum-free certificate" was measured in
  visited leaves, ignoring that a `sum` node stores two sub-instances.  Now also proved for the
  node count and for the full description length (`sum_rule_separation_size`,
  `sum_rule_separation_dataSize`).
* The many-to-one pruning factor `1 + m e^{−βγ}` was asserted in the report but only the
  injective case was proved; now `partition_prune_bracket_fibers`.
* The exact-dominance factorisation "over the components of the link graph" is verified in its
  abstract block-separable form only; the 3-body model itself is not defined in Lean.  The
  documents now say so.
* A non-vacuity witness for the witness-size bound concluded `|filter| ≤ |univ|`; replaced by one
  that forces both states into every exact certificate.
* Three harness tests could not fail (same quadrature on both sides of X.1; a dead membership
  check in II.4; `m ≤ 2` without the prune rule in VII.1); rewritten with independent
  computations and built-in power checks.
* Novelty wording: "no verified checker for this problem class" now carries the reviewer's
  caveat (pseudo-Boolean encodings with existing verified checkers), and the voxel claim is
  scoped to "inside a provable design algorithm".

---

# Findings of the re-audit (the same reviewer, checking the repairs)

Ten of the eleven original findings and the three weak tests were confirmed resolved; nothing
false, vacuous or circular was found.  The re-audit added one major and five minor points.

## D19. What the first round of repairs still got wrong

* **The audit could be passed with an incomplete proof (major, tooling).**  The script looked for
  the compiler warning with the quoting style of an older Lean version, the token scan skipped
  `AxiomAudit.lean`, and the automatic axiom walk does not see anonymous `example`s — so a
  `sorry` inside a non-vacuity witness would have passed.  No such proof existed, but the claim
  "the audit fails if any module contains `sorry`" was false for that file.  Repair: the warning
  pattern is version-independent, the token scan covers every file and forbids the substring
  (which also covers the placeholder axiom itself) and the debugging tactic `stop`, the witnesses
  are named theorems covered by the axiom walk, and the audit begins with a self-test in which
  planted violations must be detected.
* **Lower-only anchor semantics could never refute an envelope.**  With values `0` and `10` at
  Hamming distance one and `c = 1/4`, the lower-bound kernel accepts `L = 41/4`; every residual
  of that class has `g ≥ 39/4` at the anchor published as `0`.  Rounding justifies a tolerance,
  not dropping the check.  Repair: **interval anchor data** `lo ≤ Δ(x) ≤ hi` (upper value
  optional) with the check `lo_p − hi_q ≤ d(x_p, x_q)`, which is exactly non-emptiness of the
  class (`IProblem.consistent_iff_nonempty`), is always satisfied by a legitimate producer, and
  rejects incompatible evaluations even after rounding (`inconsistentInterval_rejected`).  The
  two earlier entry points are the special cases `[v, v]` and `[v, ∞)`
  (`verifyITop_ofExact`, `verifyITop_ofLower`).  The file format no longer has a default reading
  of a bare anchor value.
* **The reference checker accepted files that cannot be written in Lean.**  A domain containing
  the state `−1` (silently indexing from the end of a table) or an anchor configuration outside
  the state range were accepted.  Repair: explicit well-formedness validation, two more reject
  vectors, and the rule stated in the blueprint.
* **"Kabsch RMSD" was claimed from theorems that allow improper motions**, and "chirality-
  sensitive residuals are covered" was prose under a verified heading.  Repair: the chain rule is
  proved for superposition restricted to any group containing the axis rotations
  (`rigidWithinIn_torsion_chain_min`); the identification with `SE(3)` is marked as a paper
  step; a verified instance uses a residual that is not reflection-invariant.
* **The executable volume bound for chart arcs did not converge under subdivision** although the
  blueprint suggested subdividing.  Repair: `chartArc_onebody_brackets_pos` / `_neg` with the
  convergent bound.
* **Wording.**  "`< 147 m³`" where the theorem says "≤" and needs `m ≥ 21`; "sharp" for the
  arbitrary-reference width without a theorem; "removed cells require nothing"; and a statement
  about mutation testing with no artifact behind it — now `experiments/mutation_tests.py` and
  `docs/mutation_output.txt`, run by the audit.

*Lesson.*  A repair is a new claim and needs the same adversarial reading as the original; and
the audit tooling is part of the trusted base of the *process* and has to be tested by planting
violations.

## D20. Residue found by the final focused check (all minor)

* **The axiom walk was by name.**  It audited constants whose name starts with `MetricChain`, so
  an axiom declared outside that namespace (or a private declaration, or an anonymous `example`
  using it, or native evaluation spelt `decide +native`) could have passed — demonstrated by the
  reviewer on a scratch copy; the repository itself contained nothing of the kind.  Repair: the
  walk (`proofs/AuditCommand.lean`) now covers every constant *defined in a project module*,
  whatever its name or visibility; anonymous `example`s are forbidden in `proofs/` (the 49
  remaining ones were named); the token list covers the other spellings; nothing may follow the
  walk in the audit file; and the audit's self-test plants an axiom outside the namespace, used
  by a public and by a private theorem, and requires the walk to name both.
* **The reference checker could be confused or crashed.**  Alias keys (`" 0,1"`, `"00,1"`),
  duplicate JSON keys, non-canonical numbers (`"0.5"`, `"1e0"`, booleans), unknown fields (a
  leftover `anchor_semantics` would have been silently ignored), tables given with the wrong JSON
  type, very deep nesting and very long numbers were accepted, misread, or raised exceptions; the
  command-line status was zero for rejected files.  No unsound acceptance was found.  Repair: a
  strict format with one reading per file, every failure turned into a rejection, a meaningful
  exit status, and 53 hostile inputs in the self-test.
* **Nits.**  The doc-reference check accepted `Anything.existing_name`; it now tracks namespaces
  and also checks lowerCamelCase and Greek-initial names.  A witness was named as if it concerned
  a chirality pseudoscalar; it concerns a signed offset along the axis and is now called
  `signed_offset_residual_torsion_bound`.  `verifyITop_sound_invariant` had no instance in the
  repository; it has one now (`interval_invariant_instance`).

---

# Cycle 7 — findings of the independent referee report and of the second research phase

The entries below come from the referee report on checkpoint 477391f (`reviews/R1_referee_report.md`),
from three further literature checks (`prior_art/L4`–`L6`), and from the work on certification
geometry (theory report §11).  No machine-checked statement was found false; the entries concern
prose that went beyond the theorems, novelty claims, a weakness of one kernel, and conjectures of
the new phase that were refuted before formalization.

## D21. "Any ε-certificate must evaluate every state of the energy shell" — FALSE for configuration certificates  **[harness: DEAD.7, XI.6] [Lean]**

*Claim (theory report §2.4, blueprint §6.2 and §9, research log, up to 477391f).*  The witness-size
theorem `anchor_necessary` was glossed as a lower bound on the number of residual evaluations of
*any* certificate.

*Refutation (referee, item 1).*  The theorem is about one format — incumbent = best evaluated
point, bound = McShane lower envelope.  A certificate that a *configuration* is ε-optimal for
every consistent residual need not evaluate anything where the white-box part alone separates
the candidate: `X = {0,1}`, `d = 1`, `E₀ = (0,5)`, `Δ ≡ 0`: the shell is `{0}` and the sharp-minimum
theorem certifies `x = 0` with no evaluation.  The harness finds such certificates in the third
random instance (`DEAD.7`); its mutation that restricts the candidate to evaluated points
survives, as it must.

*What is true (machine-checked, `proofs/Frontiers/CertificateNotions.lean`).*  Three notions —
point, value and configuration certificates — are characterised exactly; a value certificate is
a covering of every state within slack radius `gap + ε` (`cover_of_isValueCertificate`), a point
certificate is a configuration certificate (`isConfigCertificate_of_isCertificate`), and a
configuration certificate becomes a point certificate after evaluating the candidate
(`isCertificate_insert_of_isConfigCertificate`).  So the minimal sizes differ by at most one, and
the shell bound holds for configuration certificates up to the candidate and the states it
covers itself.

*Sharpening (second referee, m2; `RefereeLemmas.lean`).*  The sizes do not differ at all once an
evaluation is made: exchanging one anchor turns a value certificate, and a configuration
certificate with at least one evaluation, into a point certificate of at most the same size
(`value_exchange`, `config_exchange`), so `N_value = N_point` and `N_point = max(1, N_config)`.
A configuration certificate may still consist of *different* points and skip a state that every
point certificate contains (`config_certificate_skips_forced_point`) — the refutation above
stands; what it saves in number is at most the one evaluation needed when none is necessary.

## D22. The partition-function kernel had no sub-exponential exact certificates on chains — LIMITATION, repaired  **[Lean]**

*Finding (referee, item 4).*  With the rules leaf / branch / thermal prune, an exact enclosure of
`Z` needs constant pair factors on every leaf box, i.e. full enumeration (`2ⁿ` leaves for a
two-state chain), although a transfer matrix computes `Z` in `O(nk²)`.  "Two semirings, parallel
certificate rules" (already weakened in D17) therefore overstated what the (+,×) kernel could do
for the stated application to chain molecules.

*Repair.*  A *cut* rule (bracket `Λ·Z_S·Z_{Sᶜ} ≤ Z ≤ Υ·Z_S·Z_{Sᶜ}` from bounds on the cut factors,
exact for independent subsystems; `zverify2_sound`) with a machine-checked separation from
cut-free certificates (`cut_rule_separation`), and an *elimination* rule that sums out a site
with at most two neighbours (theory report §11.8).  For certificates built from the elementary
rules whose lower end is exact, a lower bound on a connected family is proved
(`chain_separation`; see D33 for its scope); lower bounds for certificates that use
decomposition rules, for approximate enclosures, and a comparison with proof systems for model
counting remain open.

## D23. Withdrawn sentences (referee, items 5–13)

* *"No pruning rule using the same information can discard more"* (query-model theorem): true for
  the notion "minimiser for no admissible residual"; a rule that only preserves the minimum
  value may discard more because of ties.  Wording corrected ("up to ties").
* *"The exponent `d/2` cannot be improved in the Hessian-interval oracle model"*: not
  established — the cited lower bounds are for point evaluations on `C²` balls; a box-enclosure
  oracle on smoother energies would do better.  Replaced by the correct, weaker statement.
* *"Uniform racing is within `w⁻¹(g/2)/w⁻¹(g)` of the offline optimum"*: the benchmark was
  undefined, the factor is an artefact for two states and wrong (unbounded ratio `≈ K/2`) for
  `K > 2` states without elimination.  Withdrawn.
* *"Classical scaling with the trace shift is within `√((L+2)/2)` in general"*: needs the
  trace-shifted solution to be PSD; *"with the same constants as Sonthalia et al."*: only for
  `λ_r(Ĝ) ≥ 0` (otherwise their Proposition 1 is strictly stronger).
* *Blueprint §8.4*: `σ₃` must be that of the centred coordinate matrix.
* *"2–2.5× tighter than the lever-arm bound"*: the baseline was weak; against superposing the
  heavier side the gain is at most `√2`.
* *"The decomposition rule is necessary"*: relative to pairwise-LP leaves, on a disconnected
  family.
* *"Dual reparameterisation cannot improve dominance pruning"*: see the scope note added to D1.

## D24. Novelty claims withdrawn after the referee report and the checks L4–L6

* **A1–A5 (envelope duality).**  "Not found in the literature" was a statement about the
  dead-end-elimination literature only.  As mathematics A1, A2, A4 are the theory of difference
  constraints / McShane extension / `c`-conjugation / sharp minima / optimal recovery; A3 for
  `E₀ ≡ 0` is Lemma 8 of Malherbe–Vayatis (2017); A5 is the `(1 − Lip f/L)` adversary of
  Bachoc–Cesari–Gerchinovitz (2021) at the finest scale.  Reclassified as known in substance.
* **D2(d) (the worst residual is additive two-level, fixed product reference).**  In print:
  Alon–Boppana–Spencer (1998), Bobkov–Houdré–Tetali (2006).
* **Identifications of §11.1** (polytrope, simple temporal network, conditional envelope as
  minimal network, Kantorovich–Rubinstein and transport–entropy duality, thermal contact):
  textbook or known in spirit; stated as such.
* **Tools of §11.3–11.6** (LP duality for coverings, the exponential-weights bound as Csiszár's
  dual lower bound, type covering, one-shot converses): known; what was *not* found is their use
  to determine certificate complexity (verdicts and search logs in `prior_art/L4` C4–C9,
  `prior_art/L6` T6–T8).

## D25. "For dependent references the worst residual is still additive" — FALSE  **[harness: DEAD.9]**

*Conjecture (natural extension of Theorem 3.1(d), and the first step of a planned "transfer-matrix
formula for the exact worst-case free-energy gap of a chain reference").*

*Refutation (found by the literature check L6, re-verified here).*  Two ternary sites with the
correlated law `((0.0112, 0.4674, 0.0278), (0.0782, 0.0002, 0.0909), (0.1403, 0.0296, 0.1544))`,
`c = (1,1)`, `β = 2`: the non-additive admissible residual with table
`((1,0,1), (1,1,2), (2,1,2))` has gap `1.2818`, every additive residual at most `1.2767`.  Every
two-site law is a Markov chain.  On the even-weight strings of the 3-cube, `β = 1/2`: `0.1201`
against `0.1074`.

*What survives.*  The fixed-`β` duality `sup_g ln E e^{β(g − E g)} = sup_ν [β·W − KL]`
(`logMGF_le_transport_entropy` and Theorem 11.14) holds for every reference; additive two-level
residuals give a computable lower bound, Wasserstein-matrix constants `‖Γc‖²` an upper bound.
Open: binary Markov trees (no counterexample in 21 000 random binary 3-chains).

## D26. "Best-first search is within one evaluation of the smallest certificate" — FALSE without radius augmentation  **[harness: DEAD.6, XI.4] [Lean]**

*Conjecture.*  Optimistic (Piyavskii–Shubert) search needs at most `N_cov(ε) + 1` evaluations.

*Refutation.*  A far minimiser, one hub of huge energy at distance 1 from `N` shallow states at
mutual distance 2: the two evaluations {minimiser, hub} certify, best-first search evaluates all
`N` states because the hub is never a minimiser of the lower bound.  Random instances violate
the claim too (16th trial).  In dimension `d ≥ 2` the same phenomenon is Baran's theorem
(`OPT = 2` against `Ω(ε^{1−d})`, `prior_art/L4` C7).  More generally no algorithm can be
instance-optimal with respect to the certificate size: finding the good hub among `M` candidates
is a search problem although the certificate has two points.

*What is true (machine-checked, `bestFirst_card_le`).*  For a symmetric envelope and a
`κ`-Lipschitz residual, the search stops after at most `|C| + 1` evaluations for *every* cover
`C` with radii shrunk to `θ·(gap + ε/6)`, `θ = (1−κ)/(4(1+κ))`.

## D27. "The Bobkov–Götze equivalence holds at a fixed inverse temperature" — FALSE  **[harness: DEAD.8]**

*Claim (theory report §3.2 up to 477391f).*  A uniform bound `ln⟨e^{−β(Δ−⟨Δ⟩)}⟩₀ ≤ β²C/2` over the
envelope class is equivalent to the transport inequality `T₁(C)`.

*Refutation (referee, item 6).*  The equivalence needs the bound for all `β ∈ ℝ`.  For
Bernoulli(0.02) with the discrete metric the `T₁` constant is `0.1233` while the best constant at
`β = 0.1, 1, 30` is `0.0202, 0.0276, 0.0566`.  The correct fixed-`β` statement is the conjugate
duality of Theorem 11.14 (known: Gozlan–Léonard 2007).

## D28. Point evaluations under a first-order envelope: a paradigm with an exponential price  **[Lean] [harness: XI.3, XI.8]**

This is a theorem rather than a refuted conjecture, recorded here because it closes a direction
that the blueprint (§6.2, up to 477391f) presented as the main loop for non-decomposable
residuals.

* *Zero temperature.*  On product landscapes one evaluation certifies the minimum iff every site
  is sharp (`product_single_certificate_iff`); otherwise the number of evaluations grows
  exponentially in the number of non-sharp sites, with an exact exponent (theory report
  Theorems 11.8–11.9; `binary_certificate_exponential`: at least `(6/5)ⁿ` although the residual
  vanishes identically).
* *Finite temperature.*  Every certificate of `ln Z` to within `ε` needs at least
  `exp(H(π) − tε/β) / max_a Σ_y e^{−t·slack}` evaluations (`card_ge_entropy`): exponentially many
  in the entropy of the Gibbs ensemble, even for sharp landscapes.
* *Ways out, and their limits.*  Higher-order structure of the residual (bounded mixed
  differences: `n(k−1)+1` evaluations give an exact pairwise reduction, `secondOrder_remainder`,
  `verify_sound_secondOrder`) — but only under weak second-order coupling (D32); linear
  information (one reference average pins `ln Z` to `β²Σc_i²/8`, Theorem 3.1) and random
  evaluations (Theorem 11.21) — but not at every accuracy: on the uniform cube class, below
  `n ln cosh(βc/2)` (which is smaller than the width `β²Σc_i²/8` of the sandwich), every
  randomised algorithm is exponential as well in the worst case, namely at the zero residual
  (Theorem 11.25; D37 for what this does not say); extensive accuracy.
* *Not a property of one certificate format.*  The bounds hold for every algorithm that
  evaluates the residual, deterministic or randomised (theory report §11.10;
  `instance_query_complexity`, `expected_queries_ge_exp_weights_min`,
  `binary_randomized_exponential`).
* *The converse reading* (added at the sixteenth checkpoint of cycle 10 at the request of
  the Scientific Discovery Division, SCI-MSG-0007 X-T4).  The lower bounds are
  *instance-wise*: an algorithm that is correct on a first-order class pays that class's
  price at every instance — in particular at the instances of any benign subclass.  So
  "assume the benign class and fall back if the data contradict it" is not available (the
  contradiction costs exponentially many evaluations to see), and **a cheaper paradigm
  necessarily gives up correctness on the first-order class and should say which members
  it gives up**.  The exponential price is the geometry of the class — evaluations
  combine by a minimum — not the worst-case quantifier: in a Hilbert ball they combine
  linearly (theory report Proposition 11.50a), in a box around a sampleable known part
  they combine through a mean (§11.30); both are different assumptions, not weaker ones.

## D29. "The finite-temperature exponent holds for every accuracy `ε = o(n)`" — FALSE for exponentially small accuracies  **[Lean]**

*Claim (theory report Theorem 11.15 up to ee2053f).*  For `n` identical sites and accuracy
`ε = o(n)`, the least number of evaluations in a certificate of `ln Z` grows like `exp(n R_β)`,
`R_β = max_Q R(Q; s, KL(Q‖π)/β)`.

*Refutation (second referee, C1).*  For `ε = 0` every certificate of `ln Z` is the whole space:
if the optimistic and the pessimistic partition functions coincide then the two McShane
envelopes coincide pointwise, so every point has slack distance zero from the evaluated set
(`exact_free_energy_certificate_eq_univ`; witness `exact_free_energy_certificate_witness`).
Hence `N_Z(0) = kⁿ`, while `R_β < ln k` unless `π` is uniform (`0.666, 0.482, 0.216 < ln 2` in
the report's own example).  For `ε_n = e^{−λn}` the exponent is at least
`max{H(Q) : KL(Q‖π) < λ}`.  The proof given in the report only reached accuracy about `2/n`.

*Correct statement.*  The theorem holds for accuracies that are neither extensive nor
exponentially small: `ε_n = o(n)` and `ln(1/ε_n) = o(n)` (the covering level in the proof is
lowered by `a_n = [(k+1) ln(n+1) + ln(4/ε_n)]/(nβ)`).  For exponentially small accuracies the
construction gives the upper bound `max_Q R(Q; s, (KL(Q‖π) − λ)₊/β)`; a matching lower bound
is open.  The zero-temperature theorem (11.9) is not affected.

## D30. "In a doubling space the shrunk covers of the best-first bound are within a constant factor of the smallest certificate" — FALSE with a known part  **[harness: DEAD.11]**

*Claim (theory report, remark after Theorem 11.11, up to ee2053f).*  "In a doubling space the
shrinkage converts into a constant factor."

*Refutation (second referee, M1; re-computed independently).*  `X = {0} ∪ {2^{−i} : 1 ≤ i ≤ m}` on
the line, `d(x,y) = |x − y|`, `f(x) = x`, `g ≡ 0`, `ε = 2^{−m−3}`.  The point `0` covers every `y`
at radius `gap(y) + ε` (`N_cov = N_point = 1`); at the shrunk radius `¼(gap(y) + ε/6) < y/2` every
point is covered only by itself, so every shrunk cover has `m + 1` points (`m = 4, 8, 12`:
ratio `5, 9, 13`).  Best-first search itself uses at most two evaluations here: the theorem is
not violated, its comparison class is just unboundedly weaker than `N_cov`.

*What remains.*  For `f ≡ 0` (gaps are then Lipschitz for the envelope) the conversion is a
conjecture (theory report §12, item 2(e)).

## D31. "The exponent of the product-landscape theorem is obtained with Boltzmann weights, site by site" — FALSE  **[harness: DEAD.12]**

*Claim (blueprint §6.6 Step 2, up to ee2053f; theory report, "Reading" after Theorem 11.9 and
§12 item 1).*  "The count is … about `exp(Σ_i r_i)` with
`r_i = max_t [ln Z_i^{gap}(t) − ln Z_i^{slack}(t)]`"; "Boltzmann weights … (two-state sites:
always)".

*Refutation (second referee, M2; re-computed independently).*  Three separate errors.
(1) *One slope for all sites.*  Two-state types `(e, c) = (0.5, 1)` and `(5, 10)`, zero residual:
the per-site maxima add up to `0.3765` per pair, the common-slope value — the true exponent — is
`0.2329`.  The blueprint's number was not even a lower bound.
(2) *Boltzmann weights are not optimal for three states.*  Gaps `(0, 0.5, 3)`, `c = 1`:
`R* = 0.1882` (optimal weights put nothing on the third state), Boltzmann weights give `0.1066`.
(3) *Nor for two states with a residual.*  `φ = (0, 0.677)`, `γ = (0, 0.644)`, `c = 1`:
`R* = 0.0252`, the Boltzmann bound is `≤ 0` for every `t`.

*Correct statement.*  The exponent is `max_t Σ_i max_v r_i(t; v)` — one linear program per site
and slope; the Boltzmann form is a valid lower bound, tight for two-state sites with zero
residual.

## D32. "Second-order envelopes are the way out" — OVERSTATED: the remainder is quadratic in the distance  **[harness: DEAD.13]**

*Claim (theory report §11.7 title and "resulting picture", README, D28, up to ee2053f).*  With
bounded mixed second differences `n(k−1)+1` evaluations reduce certification to the pairwise
kernel — presented as the general way out of the exponential price.

*What was omitted (second referee, M3; re-computed independently).*  Theorems 11.16–11.17 are
correct, but the half-width of the star envelope is `Σ_{i<j changed} c_ij`, quadratic in the
Hamming distance, and more evaluations of the same kind do not remove it.  For `n` two-state
sites with `c_ij = c`: the function `−c·C(|x| − 1, 2)` is in the class (all mixed differences in
`{0, −c}`), vanishes on the whole Hamming ball of radius 2 and equals `−c(n−1)(n−2)/2` at the
far corner; and for a set `S` of `w ≤ (n+2)/3` sites the function
`−c·C(a,2)·C(n−w−b,2)/C(n−w,2)` (`a`, `b` the numbers of changed sites inside and outside `S`)
is in the class, vanishes on the stars of both corners and equals `−c·C(w,2)` at the indicator
of `S`.  So with `f(x) = e|x|` neither the radius-2 ball (`n ≥ 2e/c + 3`) nor two opposite stars
(`n ≥ 6e/c + 6`) certify the minimiser.  The loop `STARCERT` of the blueprint could run forever
on such an instance; it now has a fallback.

*Correct statement.*  A way out *under weak coupling*: a star certifies iff the second-order
sharp-minimum condition holds; sufficient is the row-sum condition
`½ Σ_{j≠i} c_ij ≤` measured single-site excitation energies.  Lower bounds for dense constants
are open.

## D33. "Exponential separation of the partition kernel on every chain" — NARROWER than described  **[Lean]**

*Claim (theory report §10 row G9, §11.8; blueprint §9, up to ee2053f).*  Certificates without
decomposition rules need `k^{m+1}` leaves on positive rigid chains, against one leaf with
elimination.

*Scope (second referee, M4).*  The theorems are true, with two reservations.  (1) *Exact lower
endpoint only*: a certificate whose lower end is `(1 − 10⁻⁹)Z` is outside them, and approximate
enclosures are the normal case at finite temperature.  (2) *`WInstance.Rigid` is a property of
the representation*: it asks that one of the two **ordered** factors of a pair distinguishes the
states of a site.  The instance `W₀₁(a,b) = 2^{a+2b}`, `W₁₀(b,a) = 2^{−(a+2b)}`, `w ≡ 1` on two
two-state sites is positive and rigid, every configuration has weight one (two independent
uniform sites), and the theorem demands four leaves for it (`gauge_trivial_separation`).  What
is measured there is that the leaf rule bounds the two orientations of a pair separately.

*What remains.*  For the ferromagnetic chain the interaction is genuine and the statement is as
intended (`ferroChain_separation`).  A representation-independent notion of rigidity (through
the symmetrised factor `W_ij(a,b)·W_ji(b,a)`, after absorbing rank-one parts) and an approximate
version of the separation are open.

## D34. "At finite temperature single dips are the extremal perturbations on every instance" — FALSE  **[harness: DEAD.14]**

*Conjecture (own, cycle 8, while looking for a matching upper bound to Theorem 11.24).*  The
fractional hitting number of the supports of all perturbations that change `ln Z` by more than
`ε` equals that of the single-dip balls; so the dip bound would be the exact randomised query
complexity at every instance.

*Refutation.*  Uniform metric on `n = 8` points, `f = g = 0`, `β = 1`, `ε = 0.3`.  A set `D`
supports an admissible perturbation of effect `ln(1 + |D|(e^β − 1)/n)`, which exceeds `ε` iff
`|D| ≥ 2`: two shallow dips at different points add up.  Every correct randomised algorithm
must therefore hit every pair, i.e. needs about `n/2 = 4` evaluations (fractional hitting
number `4`), whereas no single dip supported on one point is sensitive, and the dip bound gives
`1`.  On random small instances the ratio between the two numbers was up to `2.7`.

*What survives.*  The dip bound is a valid lower bound (Theorems 11.22–11.24).  On the uniform
cube Hamming balls *are* extremal (Harper's theorem; harness XII.5), which gives the matching
upper bound of Theorem 11.25(c).  For product spaces extremality at the exponential scale was
conjectured; it fails for sites with three or more states (D38).

## D35. "On the cube the soft-gap bound is attained up to a polynomial factor for every accuracy `ε = o(n)`" — FALSE for exponentially small accuracies  **[Lean] [harness: DEAD.15, XII.8]**

*Claim (theory report at f1a6015, Theorem 11.25(c) and the sentence "with exponent
`ln 2 − h(ρ(ε₁))` … for `ε₁ = 0`").*  For `ε = o(n)` the lower bound
`(1−2δ) exp(n(ln 2 − h(ρ₀)))`, `ρ₀ = ln(2/(1+e^{−u}))/u`, is attained at the zero residual up to a
polynomial factor.

*Refutation (third referee, C1).*  For `ε = 0` — and for every `ε` below
`ln(1 + 2^{−n}(e^u − 1))`, the effect of a dip supported on one point — every randomised algorithm
makes at least `(1 − 2δ) 2ⁿ` evaluations on the zero residual (`cube_small_accuracy_randomized`,
`cube_exact_randomized`).  The claimed bound is smaller by `e^{n h(ρ₀)}`.  The text's own count
`2ⁿ/|B(r*)|` was right; its identification with the soft-gap exponent was not: the soft gap
replaces `(c − s)₊` by `c − s`, a relaxation that is far from the exact dip criterion when
`e^ε − 1` is small.

*This is the second occurrence of the same error* (D29: Theorem 11.15 claimed for all
`ε = o(n)`).  An asymptotic exponent statement of this theory needs two conditions on the
accuracy, `ε_n = o(n)` **and** `ln(1/ε_n) = o(n)`, or an explicit treatment of the exponentially
small regime.

*What is true.*  The exponent at the zero residual in every accuracy regime (theory report
Theorem 11.25(d)): `ln 2 − h((Λ₁ + ε₁)/u)` at accuracy `nε₁`; `ln 2 − h(Λ₁/u)` for accuracies that are
neither extensive nor exponentially small; `ln 2 − h((Λ₁ − λ)/u)` for `ε = e^{−λn}`, `λ ≤ λ_c`; `λ` for
`λ_c ≤ λ ≤ ln 2` (cost of order `1/ε`); `ln 2` beyond.  Lower bounds from the exact effect of a dip
on a Hamming ball (`cube_exact_dip_randomized`), upper bounds from the hedged spot-check and
Harper's theorem; benchmark B10 compares exact ball counts with the formulas at `n = 3200`.

## D36. "The spot-check determines the randomised complexity up to constants; randomisation gains exactly the integrality gap" — NOT with the unhedged spot-check  **[Lean] [harness: XII.7] [benchmark B10]**

*Claims (theory report at f1a6015 and the following uncommitted draft).*  (i) The randomised
query complexity at an instance is the fractional hitting number of the distinguishable
alternatives "up to the factors `1 − 2δ`, `ln(1/δ)` and the change from `ε` to `ε/2`".  (ii) At zero
temperature the spot-check with a fractional cover shows that randomisation gains exactly the
integrality gap of the covering problem.

*What is wrong (third referee, M1).*  The spot-check that returns the hint's value has to
detect alternatives at level `ε/2`; the lower bound counts alternatives at level `ε`.  The
change of level is not a constant: on the cube it costs `e^{Θ(ε)}` (measured `e^{13}` at `ε = √n`,
`e^{30}` at `ε = 0.06n`, `n = 3200`; reproduced in benchmark B10), and at zero temperature
`N_frac(ε/2)` can exceed even the integral covering number at level `ε` without bound (uniform
metric, `ε = 1.5 d`: `1` against `|X|`).

*Repair.*  Hedge the output (`hedgedSpotCheck_correct`): returning `Φ(g) + ε/2 − η` instead of
`Φ(g)`, only alternatives that raise `Φ` by more than `ε − η` or lower it by more than `η` have
to be detected.  For the minimum (`min_hedgedSpotCheck_correct`) this gives the bracket
`(1−2δ) N_frac(ε) ≤ E|Q| ≤ ⌈ln(1/δ)(N_frac(ε⁻) + 1)⌉`, and (ii) becomes true; on the cube the two
sides of Theorem 11.25(c) then agree within a constant for `ε ≥ 2`.  The general lower bound of
the right shape is the pair version (`prob_query_ne_pair`), the fractional relaxation of a value
certificate.

## D37. Statements of scope that were too wide: "the best algorithm", "the cube class", "below the accuracy of the sandwich"  **[harness: XII.3 (factor), XII.8]**

Recorded together because they are the same kind of slip (third referee, M2–M4).

* *"The size of the smallest certificate is exactly the number of evaluations of the best
  algorithm that is correct on the whole class"* (README at f1a6015).  The theorem
  (`instance_query_complexity`) is instance by instance: for each residual there is an
  algorithm, built from that residual, that is correct everywhere and cheap there.  No single
  algorithm achieves this on all instances: on the hub family every randomised decision tree
  pays `((1−2δ)²/8) min(M, N)` on some instance whose certificate has two points (theory report
  Theorem 11.23(iii)).
* *"Randomisation gains at most `1 − 2δ` against each covering bound."*  Proved against the
  fractional (LP-dual) covering bounds, not against the integral covering number.
* *"On the cube class … exponentially many for every sampling distribution" / "a sharp
  threshold on the cube class".*  The lower bound is at the zero residual.  The residual `c|x|`
  of the same class is determined by its values at `0…0` and `1…1`, so with that hint two
  evaluations suffice at every accuracy.  The threshold is a worst-case statement.
* *"Below the accuracy of the sandwich every randomised algorithm is exponential."*  The
  theorem concerns the uniform cube and the accuracy `n ln cosh(βc/2)`, which is strictly below
  the width `β²Σc_i²/8` of Theorem 11.21 (`0.120` against `0.125` per site at `u = 1`); in between a
  bounded number of evaluations suffices.  For other product references the exponential
  regime was proved below `ε₁^crit` only.
* *"Every randomised algorithm."*  The formal statements cover finite mixtures of
  `QueryAlgorithm`s — a class strictly larger than decision trees (`Referee3.pathoAlg_not_a_tree`),
  which strengthens lower bounds; continuum mixtures follow by the same pointwise argument but
  are not formalised.

## D38. "On product landscapes single dips are extremal at the exponential scale" — FALSE in general for sites with three or more states  **[harness: DEAD.16]**

*Conjecture (theory report at 6344bf9, "What is not proved", and §12 item 2(b)).*  At an
additive instance of a product landscape the randomised exponent of `ln Z` is the dip exponent
`R^rand_β(ε₁)`, and its vanishing point `ε₁^crit` is the boundary between polynomial and
exponential cost.

*Refutation (independent workstream A, `workstreams/A_REPORT.md`; the example re-derived by
hand and recomputed in the harness).*  For any `Φ` with `Φ(x) − Φ(y) ≤ s(x,y)` the *generalised
dip* `(r − Φ)₊` is admissible and raises `ln Z` by at least `βr − Λ(Φ)`, `Λ(Φ) = −ln E_π e^{−βΦ}`.
With `Φ` additive over the sites and each site function the indicator-type vertex
`c·1[a ∉ B_i]`, this is a dip centred at the box `∏ B_i` — a union of equally deep single dips,
the mechanism of D34.  Flat four-state site, `u = βc = 1`, `ε = o(n)`: the boxes of pairs give the
exponent `D(ρ₂‖½) = 0.02914`, `ρ₂ = −ln(½ + ½e^{−1})`, the single dips `D(ρ₁‖¾) = 0.02841`,
`ρ₁ = −ln(¼ + ¾e^{−1})` (the uniform sampler is optimal by symmetry; exact binomial tails at
`n = 20000`: a factor `e^{14.8}`).  Flat eight-state site: `0.0309` against `0.0194`.  Three states
suffice (energies `(0,0,2)`, `β = c = 1`: `0.0290` against `0.0247`), and there the threshold of the
lower bound is `0.1197`, not `ε₁^crit = 0.0947` (both recomputed for this revision): between the
two values the cost is exponential, where the conjecture predicted polynomial.

*What survives.*  The conjecture holds on the uniform cube (Harper) and, by a paper proof of
the same workstream that has not yet been refereed, for every two-state site (the Lipschitz
polytope of a two-point space is a segment whose endpoints are the two distance functions).
The gap closes as `β → ∞`: at zero temperature a sensitive perturbation contains a sensitive
single dip, which is why the zero-temperature theory is a covering theory.

*What replaces it* (theory report Theorems 11.27–11.28; `GeneralisedDips.lean`; harness
XII.9–XII.12).  The lower bound with all slack-Lipschitz centre functions, machine-checked on
every instance; on product landscapes the single-letter bound `R^gen_β`, a game over the vertices
of the Lipschitz polytope of a site; and the threshold `min_Q max_Φ[βE_QΦ − Λ(Φ)]`, which is
sharp at every additive instance.  That `R^gen_β` is the exact exponent at additive instances
of identical sites is a paper proof of the workstream that an independent referee checked
without finding a gap (`reviews/R4_referee_report.md`); the conjecture therefore holds for all
two-state sites, and it also holds on some sites with more states (the flat three-state site).

## D39. "Best-first search is within a constant factor of the smallest certificate on the line, also with a known part" — FALSE  **[harness: DEAD.17]**

*Claim (implicit in theory report §11.5 at 6344bf9, which left open whether the one-dimensional
theorem of Hansen–Jaumard–Lu, `n_PY ≤ 4n_B + 1`, survives a known part; D30 had shown only that
the comparison class of Theorem 11.11 degenerates).*

*Refutation (workstream C, Proposition C5; family B′ of its reviewer; recomputed in the
harness).*  Points `x* = −D`, a hub `c = 0`, a grid to the right of the hub, known part
`f(0) = G`, `f(t) = G + (1−η)t`.  With zero residual and `f(x*) = 0`, `{x*, c}` is a certificate and
best-first search makes `4, 5, 6, 6, 7, 8` evaluations for `η = 0.2, …, 0.00625` (`11` at
`η = 1/1280`); with the extremal residual `g = −|x|` and one further point it makes
`9, 16, 29, 55, 107, 212` against a certificate of three.  In normal form the half-line right of
the hub has cost density `η` in one direction and `2 − η` in the other: the hub almost
dominates everything to its right, but the lower bound is lowest at the far end.

*What survives.*  Theorem 11.11 and Proposition 11.30 (both consistent with the families).  The
growth laws `log₂(1/η)` and `1.3/η` are computed, not proved.  One overstatement of the
workstream report was corrected by its reviewer: without the extra point, the second family is
solved in two evaluations by a search that starts at a centre of the reduced envelope.

## D40. Three hopes for dense second-order classes — FALSE  **[Lean] [harness: XI.15]**

Recorded together; all three were live in theory report §12 item 4 and blueprint §6.6 before
workstream E (theory report §11.12).

* *"A cleverer evaluation set than stars (covering arrays, codes, random sets) determines the
  residual up to `O(c)`."*  For every evaluated set the uncertainty at Hamming distance `d` is at
  least `c·C(d+1, 2)` (`SecondOrderDip.dip_witness`).  With polynomially many evaluations it is
  `(1 − o(1))·c·n²/8` somewhere.
* *"Several stars combine."*  A union of stars gives exactly the best single-star bound
  (`SecondOrderDip.stars_do_not_combine`): the information is combined by a minimum, as in the
  first-order class.
* *"The star is the right `n+1` evaluations."*  A balanced three-legged spider certifies for
  `e ≥ c·n/3`, the star only for `e ≥ c(n−1)/2`.

Also corrected by the reviewer in the workstream's own report: "all but a `2^{−Θ(√n log n)}`
fraction of the cube must be evaluated" (that is the fraction that *is* evaluated; the exponent
is full), and "`N₂` is the algorithmic cost" (true up to `+1` only).

## D41. "For pairwise binary references the worst-case Jensen gap is attained by an additive residual" — FALSE  **[recomputed for the theory report]**

*Conjecture (workstream B, Conjecture B.13; it would have given the worst-case free-energy gap
of a chain reference and the upper half of the accuracy threshold for chains).*  For every
measure `π ∝ exp(Σ J_ij s_i s_j + Σ h_i s_i)` on `{0,1}ⁿ` and every tilt `θ`, the maximum of
`ln E_π exp(−β(g − θM − E_π[g − θM]))` over the `c`-Hamming-Lipschitz `g` is attained at an
additive `g = c Σ_i (±1) y_i`.  Evidence offered: no violation in about 6 100 exactly enumerated
models and under adversarial search.

*Refutation (the reviewer of workstream B, with 50–60-digit arithmetic; first instance recomputed
here).*  (1) No tilt, antiferromagnetic complete graph on four sites with fields, `βc = 1.5`:
the best additive residual gives `0.99202`, a non-additive vertex of the Lipschitz polytope
`1.00985`.  (2) No tilt, a star with three leaves: margin `4.4·10⁻⁵` — so additivity fails for
binary Markov trees, which D25 had left open; by a gauge transformation the same instance is a
ferromagnetic star with non-uniform fields.  (3) Tilt `0.95c`, homogeneous antiferromagnetic
open chain of three sites: `7.513` against `7.964`.  The mechanism is that of D34 (a union of
dips on a slice where the measure is nearly degenerate).

*Why the evidence had no power.*  Violations occupy tuned regimes of relative volume below
`10⁻⁴`; random couplings of order one and local search from random starts miss them.  A count
of instances without violations is not evidence when the violating set is thin.

*What survives.*  No counterexample for all laws on two sites, for open chains without tilt
(`n ≤ 5`), or for homogeneous ferromagnetic chains.  The statement for product measures is the
classical tensorisation.

## D42. "The verified per-torsion constants make long chains certifiable in weighted-Hamming format" — FALSE  **[theory report §11.14]**

*Assumption (theory report §4.4, §7 and blueprint §7 up to d8d3777, implicitly).*  The verified
torsion-to-RMSD chain rule turns an RMSD-Lipschitz residual into a weighted-Hamming envelope to
which the kernels and the complexity theory of §11 apply; small constants then give small
certificates.

*What is wrong (workstream G, checked by its reviewer).*  The constants are not small: the
verified ones satisfy `c_i ≥ 0.824·Λ b m_i^{3/2}`, `m_i` the distance to the nearer chain end, and
no valid constants are below about `0.186·Λ b m_i^{3/2}` (lever arm).  With constants growing like
any positive power the certificate size is `k^{n − o(n)}`; only `O(N^{1/3})` sites near the ends are
sharp.  For contact-type residuals every torsion-Hamming envelope has constants growing
linearly in `m_i`, whatever the metric.

*What survives.*  The kernels are sound for whatever constants are supplied.  The RMSD envelope
used directly (not through the chain rule) costs only a stretched exponential at the zero
residual; residual classes that are local along the sequence, expressed in windowed local
frames, or linear in pair features have bounded constants or few degrees of freedom.  Also
recorded: the workstream's own summary sentence "the whole exponential price is the `ℓ¹` chain
rule" was found too strong by its reviewer (one instance, `Lb/e = o(N)`, a bracket of two orders
of magnitude in the exponent's constant).

## D43. Six statements of the first version of theory report §§11.16–11.17 that said more than was proved (cycle 10; fifth and sixth referees, workstream P)

No theorem of the two sections was found false; these sentences were.

1. **"Their sample size is now a theorem on the class and replaces the Chebyshev bound"**
   (Theorem 11.44, first version).  The bound used `E min(w,t*) ≥ t* K/M` only; the resulting
   quantity `Γ_n(r)` stays near or above `4eᵘ(eᵘ−1)` (the limit of its minimum over `r`), so the theorem certified nothing below an
   accuracy of about `ln(2(1+4eᵘ(eᵘ−1))) + ln(1/δ₂)` (`6.7` for `u = 1`, `δ₂ = 0.05`), and just above
   it gave an exponent larger than `KL(p_u‖½)`.  *Repair*: the two-sided tail lemma of the
   referee (Lemma 11.43(c); `Γ′_n` with `T_n(r−1)` in the denominator), which gives the exponent
   `KL(p_u‖½)` at every fixed accuracy.  Harness XIII.2 checks both facts; benchmark B12 shows
   "void" for the first bound at `ε = 1`.
2. **"The matching non-adaptive lower bound was not found"** (table row G18).  The method —
   hidden cone centres, pairs that differ on a ball at the centre, Bakhvalov averaging, the
   remark that adaption defeats it — is in Mathé–Novak (2007) for log-concave densities with a
   Lipschitz logarithm.  What was not found is the exponent on the cube for `ln Z` and the
   class-wide upper bound.
3. **"[V]" on Theorem 11.45 as a whole, "machine-checked up to Harper's theorem"** (README).
   Machine-checked are part (a) of the tail lemma, the abstract non-adaptive bound, and the
   cube bound *given* two finite sums; the reduction to Harper, the closed forms and every
   exponent are paper computations.
4. **"Exact after minimising over `λ`: the bracket is the `L¹` distance to the span"** (Theorems
   11.47(b), 11.48(c)).  Each end of the consistent range is attained by its own `λ`; the width
   is at most twice the distance to the span, with equality at the central data only (the
   radius of information is attained at the zero information).  Two features suffice for a
   range that is a single point at distance one.  Harness XIV.1 now requires such cases.
5. **The comparison "per-torsion Hamming `exp(Θ(N))`, RMSD `exp(Θ̃(√N))`, profile `exp(O(1))` at an
   extensive accuracy".**  Not like with like: the `√N` law is a statement at `ε = 0`; at an
   extensive accuracy and a fixed RMSD-Lipschitz constant the RMSD envelope has nets of size
   `exp(O(Lb/ε₁))`, independent of `N` (blocks of beads snapped to a grid); the constant of
   §11.17 is per pair, so an extensive pair-additive residual has an RMSD constant of order
   `N`; and the classes differ.  The section now has a like-for-like table.  Likewise "does not
   grow" holds at extensive accuracy and for counts of evaluations only: at a fixed accuracy
   the first-order class of the profile envelope is `exp(Θ(N/ε))` on rich conformation spaces,
   and the existence bound of Proposition 11.49(a) is numerically vacuous (`10^{93}`–`10^{2697}`
   where 8–7000 evaluations suffice).
6. **Three smaller ones.**  "Chains on the rational torus with bounded denominators" as a
   case of finitely many distances (the number of distinct squared distances grows with the
   chain: `1, 1, 1, 2, 5, 14, 36` for 4–10 beads); the remark that the star with a first-order
   remainder shows "the order of the second-order bound" (it came from a wasteful transport
   plan: the exact term is `2(k−1)η`, linear in the distance); and, in the brief of workstream
   P, "at fixed absolute accuracy the first-order class is exponential in `N`" as a general
   statement (on lattices it is polynomial, because there are polynomially many profiles).

*Lesson.*  The pattern of cycles 8 and 9 repeated: every proof survived, and the sentences
around the proofs did not — a comparison across theorems with different hypotheses, a label
wider than the formalisation, a "not found" after too little search.  The one statement that
would have been useful to a reader as a number (the planning bound) was the vacuous one.

## D44. Four numbers and four sentences about the profile format that were weaker or stronger than the facts (cycle 10; review of workstream P)

The reviewer of workstream P re-derived its eighteen statements and found none false
(`reviews/R_P_review.md`).  What did not survive, in the workstream's summary and in the
sentences of theory report §11.17 and of the research log that repeated it:

1. **"The chain-length independence is a property of the exactly pair-additive class, not of
   chains."**  Contradicted by the workstream's own Theorem 7 (independence at extensive
   accuracy for the whole first-order class of the profile envelope — pair-additivity is not
   used) and Theorem 13 (a sup-norm remainder costs an accuracy floor and nothing else).
   What is lost with a remainder that is only first-order in a per-torsion envelope is the
   subject of Corollary 15, and nothing wider.
2. **"With a per-torsion remainder the exponential cost returns in proportion to `η`."**  No
   theorem says so.  By Theorem 11.37 the leading term of the exponent is the same for every
   fixed `η > 0`; `η` enters a sub-leading correction.  The measured growth "2 → 20
   evaluations" could not support a proportionality either: these were sizes of greedy
   covers, i.e. upper bounds reported as requirements (they prune to 6 and 17; no lower
   bound above 2 is proved).
3. **"No format has a one-evaluation threshold that is independent of `N`."**  A measurement
   for three formats and `n ≤ 12`, not a theorem; and the span column on the lattice was the
   threshold of an evaluation at the all-trans state, whose profile is zero there, so that
   it carries no information — the best single evaluation certifies up to an `L` that is
   seven to eight times larger (and still decays like `4.8/N`).
4. **"Span cost ∝ features, first-order cost ∝ exp(features); the chain length enters only
   through the number of features."**  The proved statements are: span at most the rank;
   span at least one evaluation per *torsion* for pair-specific classes at a vanishing known
   part on the product domain (a classical width of a box in `ℓ¹`, Pietsch–Stesin — listed
   as new, it is not); first-order at most the number of profiles, which depends on `N` at a
   fixed number of features.
5. **Four numbers.**  The Hamming entries "≥ 2.2·10⁵ of 422 825" and "≥ 5539 of 8115" were valid
   and grossly weak: the smallest valid constant exceeds the largest gap, so every
   conformation must be evaluated.  Off-lattice `n = 10` in the profile format: 319, not 318
   (318 was the lower end of a bracket).  `ln Z` in the profile format: between 65 and 69, not
   between 10 and 69.  "`3^{n−O(√n)}`" cannot hold on a self-avoiding domain with `2.9ⁿ` points
   (the reviewer gives the replacement `|X_N|·exp(−4√((en+ε)/(Lc₀)))`).

*Also at this checkpoint, a defect of the harness, not of a claim.*  XIV.3 required that
multipliers bounded by 50 gain one unit on every coefficient box that contradicts the
anchors.  The claim is that the data term is unbounded there, which is true (Farkas plus
positive homogeneity); the gain at bounded multipliers is proportional to the margin of the
contradiction and was `0.035` in one instance of the full run.  The quick mode, which the
audit runs, had never met such an instance.  The check is now positivity plus exact
homogeneity, with a mutation of its own.

*Lesson.*  A summary written by the author of the theorems is not safer than one written by
a reader: three of the four sentences were contradicted by statements a few pages below
them.  And weak numbers are errors too — "at least half" where the truth is "all" hid the
one-line reason.

## D45. Adaptive algorithms without a hint: five wrong accountings, one gap in the algorithm, and the lower bounds that are not there (cycle 10; workstream H, harness XV.3)

The result of theory report §11.18 — adaptive algorithms without a hint reach the hinted
exponent — came out of more wrong arguments than any other in this project.  All of them
concern the same step: *how many sampled points need which inner accuracy*.

1. **The coordinator's multilevel scheme with a single threshold** (brief of workstream H, step
   3): "an outer sample whose fibre average is `t e^{−G}` needs only a one-sided inner bound at
   gap `G`", from which the recursion `T_{k+1} = a·T_k/(a − h + T_k)` was derived.  **False as an
   accounting.**  One-sided certificates "`Z_a ≤ t`" bound `Σ_a min(Z_a, t)` only by `M·t`, whereas
   the main term can be as small as `K·t`; what a single-threshold bracket needs are gaps
   measured from a tolerance on the *estimate*, and then Markov's inequality gives no bound
   on the number of samples at small gap.  Counterexample ("trap", found independently by the
   coordinator and by the workstream): a flat bulk with a bump of radius just above the
   critical one in the outer coordinates, with flattened cones as inner landscapes whose
   plateaus are tuned to the required gap; the single-threshold scheme pays
   `φ θ_na(ε₁/φ) + (1 − φ) θ_na(≈ 2ε₁/(1 − φ))`, which tends to `a` as `ε₁ → 0`: no gain.  The repair is a
   *ladder* of levels with exceedance probabilities in place of strata (the layer cake).
2. **Three recursions of the workstream before the right one** (its report, §2.8; outputs kept
   in its directory).  v1 counted the samples within gap `γ` of a level as `e^{n(γ − g₁)}` — the
   negligibility tolerance does not reduce that count.  v2 and v4 forgot that the first
   negligible level above a bulk already needs `e^{nβ}` samples.  v2 and v4 produce levels
   *below* the hinted exponent and are thereby refuted by the lower bound of Theorem 11.25(a);
   v1 passes that test by luck.  The same mistake as v1 is mutation XV.2 M4 of the harness.
   **The test "no level of a recursion may lie below `θ_hint`" is a necessary condition that
   every accounting must pass**; for the correct recursion it is a theorem (`R[θ_hint] = θ_hint`,
   Theorem 11.53(b)).
3. **The coordinator's accounting with the tail lemma at every level** ("CLOSE"): evaluated by
   the workstream (`0.58`–`0.60 θ_na` at two levels), **not proved**; it would need two-sided inner
   accuracy on the samples that carry each stratum.  Instance by instance it is incomparable
   with the layer-cake scheme.  Not used.
4. **The closure test as first written** (workstream report §2.6 and the first draft of
   Theorem 11.52): the radius `r` is the least one with `|B(n_o, r)| ≥ 2^{n_o} q`, and the tail
   lemma was applied at that radius also when it is `n_o`.  But the tail lemma needs a point
   outside the super-level set; while every sampled fibre lies above the level (`q = 1`) the
   "ball" is the whole cube and the bound is false.  With a small outer block and a large
   accuracy the algorithm then closes at the lowest level with an upper end below the mean
   (first instance of harness XV.3 in its first run; mutation XV.3 M3; found independently by
   the referee, who shows that the algorithm as drafted returns a false bracket with
   probability one whenever `φ(u − Λ₁) ≲ g`: 2 940 of 2 940 simulated runs).  Fix: no closure at
   `r = n_o`.  Two of the three parameter choices of the convergence proof lie outside the
   affected range; the third (a fixed outer fraction and *every* accuracy) does not, so the
   convergence proof needs the corrected theorem — the coordinator's first note to the
   referee said otherwise and was wrong.
5. **Lower bounds above the hinted exponent — none.**  Seven families tried by the workstream
   (decoy cones; a rough background from a random code; a low plateau with a hidden dip;
   populations of flattened cones with rare exceptions; graph-type non-product instances;
   long thin valleys; stability versions of Harper's theorem as an algorithmic tool) all cost
   at most `e^{nθ_hint}` to resolve, and now a theorem says that nothing else is possible.
   Long valleys of the Aldous type carry no mass under the constraint that the oscillation
   is at most `un`; known stability theorems for Harper's inequality (Keevash–Long;
   Przykucki–Roberts) need a slack `1 + O(1/n)` where this problem has `e^{Θ(n)}`.
6. **A numerical trap.**  The recursion iterated on a grid with a conservative (one-sided)
   interpolation stalls 0.5–2 % above `θ_hint` at every accuracy, which reads like a limit
   strictly above the hinted exponent.  With piecewise-linear interpolation the residual
   falls to `0.35 %` of `a` after 14 levels and keeps falling; the limit is `θ_hint` by Theorem
   11.53(d).

*Lesson.*  For a nested randomised algorithm the validity of the output was never in doubt
after the first day; its cost was wrong five times.  Three things helped, in this order: a
necessary condition from an independent lower bound; writing the count as one inequality
with explicit constants, in which a cancellation becomes visible (`close_points_bound`); and
running the logic at small size with a simulated inner oracle, which found the one gap that
all readers had missed.


## D46. Bounded accuracy and chain length: a sketch that was wrong in its mechanism, a reason that was wrong, and a saturation that is not there (cycle 10; workstream K, Computational Research Division)

Four corrections, none of which invalidates a theorem, all of which changed sentences.

1. **The "closure window" (coordinator's sketch for bounded accuracy; refuted by workstream
   K).**  The sketch handed to workstream K proposed to keep the closure test of Theorem 11.52
   — tail against the mass certified at the level itself, ratio `Γ̃(r) = E_r/|B(r−1)|` — and
   argued that, as the sample doubles, the closing radius moves through a window of radii in
   which `Γ̃(r) ≤ e^{G−b}/4` with `G − b = O(1)`.  Wrong as a mechanism, for three reasons.
   (a) `Γ̃` is never small: `Γ̃(r) ≥ 4e^u(e^u−1)(1−o(1))` for every `r`, so the window is empty unless
   `G − b ≥ ln(16e^u(e^u−1))` (`2.84, 4.31, 6.63` for `u = ½, 1, 2`).  (b) Where it is not empty its upper
   end is `ρ₊n_o` with `ρ₊ < p_u`: the outer sample would have the exponent `φ·KL(ρ₊‖½) > φa`, which
   gives at best a weak form of the result.  (c) Populated levels never sit in the window:
   their closing radius lies within `O(√(n log n))` of `p_un_o`, where `Γ̃ ≈ c√n` (a level whose
   super-level set is a ball well inside radius `p_un_o` carries a negligible share of the
   mass of the cone above it and is declared negligible before it is populated).  The repair
   puts the *two-sided* tail lemma into the algorithm (the Harper term of Theorem 11.56) and
   raises the negligibility factor; the same sketch's "each level adds `O(1)` to the accuracy"
   then turned out to be too pessimistic — a level adds an arbitrarily small constant, which
   is why the strong form (every fixed accuracy) holds.
2. **"Ratio `≤ 3 + 12Γ(r)`, bounded up to `p_un`" (reason given for the exponent `a` of the base
   bracket at fixed accuracy).**  The conclusion is right, the reason is not: that ratio is
   never below `3 + 48e^u(e^u−1)` and grows like `√n` at `p_un`.  The bounded ratio at exponent `a`
   comes from the two-sided lemma 11.43(c) (Proposition 11.57(a)).
3. **A saturation read off from an estimator.**  Workstream P's table of traversal numbers
   `m(δ)` (its §3.2) — `m(1) = 11, 11, 10, 12` — was read as "the entropy of the profile set
   saturates near `N ≈ 13`".  The Computational Research Division could not reproduce `m(δ)` as
   defined (a farthest-point traversal depends on the starting point and on tie-breaking,
   neither of which is stated; its values differ by up to 2 at `δ ≥ 1` and by a factor 1.4 at
   `δ = ¼`), and the *exact* internal covering numbers at the same radii keep increasing
   through 27 beads (`δ = 1`: 4, 5, 6, 7, 8, 8, 9, 10, 11, 11 for `n = 8, …, 24`).  A traversal
   length is an upper estimate of a covering number, not a covering number; report
   covering numbers with certified brackets.
4. **"Certificates whose size does not depend on the chain length" (blueprint §7, theory
   report §11.17, G19, THY-MSG-0002 principle 3).**  True as a bound (Proposition 11.49(a)),
   and the theory division asked at which size the plateau sets in, expecting an answer
   within reach of enumeration (THY-REQ-0002: "where does chain-length independence set
   in?").  It does not
   set in at any size that can be enumerated: on the diamond-lattice chain the smallest
   certificate at accuracy `N/2` grows by about one evaluation per two torsions through 27
   beads, because the profile set per bead has reached only about 38 % of its bulk extent;
   off-lattice it grows geometrically (a factor 1.3–1.7 per torsion through 15 beads),
   because the number of distinct distances below the cutoff grows with the chain and the
   plateau is of the order `exp(c·zLS_c/ε₁)`.  The format is cheap in absolute terms when the
   per-pair constant is small and orders of magnitude cheaper than the per-torsion format
   always; "independent of the chain length" describes a regime nobody will reach by
   enumeration.  All four places were reworded.

5. **Two false side remarks in the workstream's report, found by the referee (R8, m5, m6).**
   "`Γ̃` is never below `4e^u(e^u−1)`" — repeated in item 1(a) above — is false at `r = 0`
   (`Γ̃(0) = e^u − 1`) and, by a fraction of a per cent, at finite `n` (`18.672 < 18.683` at
   `n = 12 800`, `u = 1`); the true statement is `min_{r≥1} Γ̃(r) = 4e^u(e^u−1)(1 − o(1))`, and at
   `r = 0` the test of the sketch holds from `G − b ≥ ln(4(e^u−1))` on, for a useless sample of
   `2^{n_o}K` points — "empty window" should read "no useful window".  And "numpy's binomial
   sampler returns 0 for `p < 10^{-16}` whatever `n`" is false for the current generator
   interface (only the legacy sampler fails, and only for means below 30); the statement
   about the multinomial sampler is true.  The second remark had been passed on to the
   other division in THY-MSG-0005 and is corrected in THY-MSG-0007.  (*Later:* the
   referee's correction is itself true for means of at most 30 only; for larger means
   and counts above about `10¹⁵` the generator's binomial sampler is wrong in another way
   — Scientific Discovery Division, SCI-REV-0007 §4; D57 item 4; THY-MSG-0015.)
6. **An over-narrow claim of the coordinator's, refuted by its own harness test.**  A first
   version of harness test XVI.2 asserted that the first level at accuracy zero is below
   `0.52a`; it is `0.58a` at `u = 4.5` (the value `0.5006a` quoted everywhere is for `u = 1`).  The
   test now states `[max(h, a/2), a]`, and `0.51a` for `u ≤ 2.5`.  The claim was never in the
   theory report.

*Lesson.*  (1) and (2): a mechanism that is plausible at the level of exponents can fail at
the level of constants in a way that changes the exponent — tabulate the ratio before
building on it.  (3) and (4): an existence bound and a heuristic estimator together
produced an expectation ("saturation near 16 beads") that exact computation by an
independent party removed in one day.

## D47. With a field, four natural guesses about "what carries over" are false (cycle 10; workstream F)

The results of §§11.16–11.18 for the uniform cube suggest four statements for a known part
`f = θ|x|` (the `p`-biased cube).  All four are false for `θ ≠ 0`; the fourth was the
coordinator's own, written into §12 item 2(d) of two checkpoints.

1. **"The identity `θ_na(e + θ_hint(e)) = θ_hint(e)` holds with the hinted exponent of the
   instance `(f, g = 0)`."**  False.  The shift identity with a field has an extra term,
   `D(P_{X|S}‖π_s|P_S) = I(S;X) + KL(P_X‖π) + u·P(X≠S) − Λ(P_S)` (`shift_identity`), and `KL(P_X‖π)` does
   not vanish at the optimum.  A level recursion built on the pair `(θ_na, R_0)` falls below
   the lower bound — by 3.1 % of `a` after ten levels at `p = 0.1`, `u = 2` — which is the
   necessary condition of D45 doing its work again.  The identity holds with the hinted
   exponent `R^max` of the hardest additive instance.
2. **"The zero residual is the hardest instance with a hint."**  False: `R^max(e) > R_0(e)` for
   every `0 ≤ e < E` when `p ≠ ½` (Theorem 11.59(d)); the hardest residual is additive and
   partly cancels the field (`γ* = −0.62` at `p = 0.1`, `u = 2`, `e → 0`).  True at `θ = 0` (remark (4)
   of §11.18).
3. **"The Gibbs measure of the known part is the right sampling distribution."**  False for
   non-adaptive algorithms: plain Monte Carlo from `π` needs at least `e^{n·max(φ₀,φ₁)}` points
   (an elementary lower bound from the cone around a constant centre and its truncation,
   written out in Theorem 11.61 after the referee asked for it), which is up to 2.9 times
   the non-adaptive exponent `a` at vanishing accuracy.  A single tilted product measure is
   not right either in the examples computed (0.5–3 % worse; that this holds for every
   `p ≠ ½` is not proved).  For the nested scheme the corresponding statement — with the
   reference `ψ₀ = 0` the recursion converges to a strictly larger limit, `0.0884` against
   `0.0481` at `p = 0.1`, `u = 2`, `e → 0` — is a **sketch** (it rests on Yu's theorem read as a
   machine summary, and on numerics; the referee did not check it).  The right sample is
   uniform on every type class: the Gibbs law of the flat-histogram instance, a mixture of
   all tilted product measures.
4. **"What is missing for product measures is a Harper-type theorem — the asymptotic
   isoperimetry of a fixed product measure (Ahlswede–Zhang) should do"** (theory report §12
   item 2(d), checkpoints three and four; research log, "Resume here", item 2).  Neither
   available in the exact form nor what is needed.  Exact vertex isoperimetry in the biased
   cube is known for down-sets only, and super-level sets of Lipschitz functions are not
   monotone; the asymptotic isoperimetry of a *fixed* product measure is the tail lemma of
   plain `π`-sampling and yields the worse exponents of item 3.  The statement that is needed
   has the measure chosen as a mixture over types *and* a reference instance `H` in the
   slack (Theorem 11.63), and it is proved by types, not by compression.

5. **Found by referee R9 in the workstream's report** (none affects a theorem).  (i) A
   finite-`n` side remark was false as a general statement: "on the 4-cube the exact tail
   function `Ξ_H` exceeds the best ball with type-dependent radii by a factor at most 2" —
   `2.080` at `p = 0.2`, `u = 4`; it was true in the nine cases the workstream computed (`u ≤ 2`), and
   the coordinator passed "at most 2.000" on to the other division as a validation target
   (THY-REQ-0007; corrected in THY-MSG-0008).  (ii) The table for single product samplers
   was inaccurate by up to 4 %: the script maximised over centre types on a grid
   `[0.005, 0.995]`, and the maximum is at the constant centres `m ∈ {0, 1}` — objective and
   constraint are linear in `m`, so the maximum of the formula is at an end point, in closed
   form.  The margin by which the best single tilted product measure loses shrank from
   "a few per cent" to `0.0244` against `0.0243` in one row.  (iii) Conclusions of a proposition
   labelled "sketch" were used as facts in three other places of the report, and the
   coordinator copied two of them into this entry and into THY-MSG-0006 without the label.
   (iv) Two gaps in the written proof of the upper bound (theory report, Theorem 11.64,
   (M1), (M2)): a compressed induction that an earlier referee (R7) had already objected to
   in the uniform case was repeated, and "verbatim" hid a union bound that fails for strong
   fields; the workstream's simulation used simulated inner brackets and could not see it.
   *Lessons.*  A maximum over a parameter on an open grid must be checked at the end points
   — here a two-line argument (linearity) decides where it is.  "At most 2 in all cases
   computed" is not "at most 2".  A sketch stays a sketch wherever it is quoted.  "Verbatim"
   in a proof that transposes an algorithm to a new measure is a claim about every constant
   that depended on the old measure — here `2^{n_o}` as the number of points.

Also recorded by the workstream: importance weights `1/π(T_κ)` without regularisation
correspond to a reference that is not in the class outside the window (its "slack" becomes
negative and the closure bound picks up exits that the class forbids) — the reference must
be a member of the class; and the max–min form of `R^max` does not extend to negative
accuracies, where a solver returned garbage silently until a test compared it with the
pair.

*Lesson.*  The uniform cube hides three coincidences — the hardest instance is the zero
residual, the Gibbs measure of the known part is uniform on type classes up to the
binomial weights that the optimal profile respects, and Harper's theorem is both exact and
about the right measure.  A statement that is true on the uniform cube "for the obvious
reason" should be re-derived with a field before it is believed in general.

## D48. Limit shape of profile sets: a wrong norm in the coordinator's brief, a plan that cannot work, and a rate that was mis-stated (cycle 10; workstream S, ENG-REQ-0001)

1. **"The profile distance on the lattice is `9|Δh₃| + 4|Δh₈| + |Δh₁₁|`, equivalently the `L¹`
   distance of cumulative profiles"** (the coordinator's brief for workstream S).  The two
   are not equivalent.  The envelope of Theorem 11.48(b) is `L` times the `L¹` distance of the
   *cumulative* counts, `5|Δh₃| + 3|Δh₃ + Δh₈| + |Δh₃ + Δh₈ + Δh₁₁|`; the weighted form is what one gets by
   applying the triangle inequality to it, agrees with it for a single profile (`9h₃ + 4h₈ + h₁₁`)
   and whenever no two of the three differences have opposite signs, and is strictly larger
   otherwise.  It matters for numbers: the exact covering number at 15 beads (`L = 1`,
   `ε = N/2`) is 8 with the right norm — the value the other division had published — and 10
   with the wrong one (20–23 instead of 15 at 27 beads).  The workstream found it on its
   first comparison with published numbers; the theorems of §11.22 hold for every norm.
   *Lesson:* a brief should define a distance by reference to the theorem and to code that
   reproduces a published number, not by a formula re-derived from memory; and "equivalently"
   deserves a check on one example with mixed signs.
2. **"A buried chain end can be exposed by changing `o(N)` sites"** (the natural route from
   bridges to all walks; the coordinator's outline in THY-RES-0001 had a version of it for
   compact conformations).  False as a general statement (Conjecture 11.75(iv)): a site set
   that contains a double strand — two adjacent parallel rods and nothing else over `2ℓ`
   levels — is not within `(ℓ − 3)/2` sites of the site set of any bridge that starts below it,
   by parity of level crossings.  The conformation still has the `(h, g)` of two bridges up to
   `O(1)`: the statement that can be true, and is open, changes `(N, h, g)` by `o(N)` and uses the
   convexity of the limit set non-locally.
3. **"`N_∞(ε₁) − N^P_cov(ε₁N) = Θ(N^{-1/3})`"** (the form of the rate question in ENG-REQ-0001, and of
   the coordinator's first answer).  Covering numbers are integers; for a non-exceptional
   accuracy the difference is eventually zero.  What has a surface correction of order
   `N^{-1/3}` is the *shape*, and the covering number at length `N` is the limiting one at an
   accuracy shifted by `(2L + e)·d_H` (Theorem 11.71(a)).
4. **"Enumeration will eventually show the plateau."**  At 27 beads the profile set has
   39 % of its bulk extent and about a tenth of its limiting volume; by the surface law
   `35(1 − 1.8N^{-1/3})` half of the extent needs about 47 beads (`≈ 10²⁰` conformations), 90 %
   about 5 800.  The plateau is a statement about `10³`–`10⁵` beads and has to be approached
   through the limit shape and through constructed conformations.
5. **"The convexity of the lower boundary should be visible in the data."**  It is not: the
   largest gap between the least gauche count and its convex envelope is a constant
   `0.25…0.30` per bead for `N = 12 … 27` — at these sizes a fold costs as much as a stem.
   Convexity of `γ` is a statement about `N ≫ 27`.
6. *Not a dead end, but a correction of scale:* the "numerically vacuous" bound of
   Proposition 11.49(a) (`10^{1387}`) and the volume bound with three discrete distances
   (`1.5·10⁹`) overestimate the lattice plateau by `1380` and by 5 to 7 orders of magnitude; the
   reason is the same in both — the a-priori box of profile densities is ten times larger
   than the body that chains can reach, and the gauche credit and the internal-centre
   factor `2³` are ignored.


## D49. Known parts that are functions of the type: four guesses that fail with two phases, one about antiferromagnets, a repair that does not work, and what a max–min computation does to its inner solver (cycle 10; workstream T)

1. **"The dip exponent of the flat-histogram instance, computed from sets around one centre, is
   its exponent at phase coexistence (`≈ 0.026`)"** (the coordinator's brief for workstream T).
   Wrong twice.  The value is `0.0251012` (`βJ = 1.5`, `B = 0`, `u = 1`); the coordinator's
   `0.0255`–`0.0261` were the same quantity on grids of `241²` and `161²` points.  And for
   accuracy rates above `e₀ ≈ 0.0018` the statement itself fails: profiles with a **free
   block** — a shell on about 86 % of the coordinates, nothing on the rest — give strictly
   larger exponents than every binary centre (`0.016155` against `0.015277` at `e = 0.02`;
   Proposition 11.82(c); harness DEAD.19).  "Binary centres suffice" is a theorem for convex
   rate functions (Theorem 11.80(b)) and false in general.  Three searches with three
   blocks at `e = 0` had found nothing — nothing is there at `e = 0`; the gain was found by
   the fourth, at `e = 0.02`.
2. **"The cone formulas of §11.20 hold with the rate function in place of the divergence."**
   True for convex `I`, false with two phases: `0.01070` against `0.025101` at `e = 0`, and the
   truncated cone around a point misses the pair identity by a factor 12 (harness DEAD.20).
   The cone's own Gibbs shell sits in a well; the hard dips sit on the barrier.  The right
   functions are cones around shells that are their own Gibbs shell (Theorem 11.79(b)).
3. **"With the zero residual's exponent the pair identity holds."**  False whenever `H ≠ 0`
   (D47, item 1, again): one phase with a field `0.02529` against `0.02266`; two phases
   `R_0(0) = 0.00875`.
4. **"The flat-histogram ensemble is the normalised-maximum-likelihood mixture of the
   field-tilted Gibbs measures, also with interactions"** (theory report §11.20, remark (3),
   offered as the route beyond independent sites).  The ensemble is right, the derivation
   is right only for convex `I`: the tilted measures of a two-phase known part never sit on
   the barrier, `max_γ λ_γ` is the convex envelope of the landscape, and the hardest additive
   instance has 35 % of the exponent of `H`.
5. **"An antiferromagnetic interaction — in the limit, the uniform measure on one slice —
   should be harder than the uniform cube, because exits that change the type are more
   expensive."**  The workstream's guess, and the coordinator's own reasoning while reading
   its report.  The premise is right and the conclusion is not: at the uniform cube's
   optimal profile the cheapest exit does not change the type anyway, and no other profile
   does better.  Every antiferromagnet without a field (`βJ` down to `−40`), and the slice of
   type `½` itself, have the uniform cube's exponents to all digits computed; slices of type
   `0.4`, `0.3`, `0.2` have less (`0.028005`, `0.024588`, `0.018842` against `0.029139`; the values
   `0.0281`, `0.0247`, `0.0189` printed here until the tenth checkpoint came from
   `experiments/coordinator_checks/meanfield_T/slice_check.py`, whose inner minimum on a grid
   is biased upward: D51, item 7).  *Since the tenth checkpoint both statements are
   theorems* (theory report §11.25: equality for every symmetric convex rate function,
   strict inequality for every slice other than `½`; unrefereed).
6. **"The nested algorithm transfers once the fibres stay in the class."**  They do (the
   conditional law of a block is again a function of its type), but fibre averages are not
   Lipschitz relative to a reference: the constant is `u + osc φ′` and the excess depends on
   the instance.  Three repairs were examined by the workstream and fail, among them
   working slice by slice at fixed *total* type (the outer function is then `2u`-Lipschitz
   across outer type classes).  Not examined there, and open: conditioning on the type of
   the *inner* block, under which the two blocks are independent (theory report §11.23,
   "a possible repair").
7. **Numerics: in a max–min computation every inaccuracy of the inner minimum is found by
   the outer maximiser.**  The workstream lists six errors of its own that tests caught and
   reading did not; the coordinator's independent solver made two of the same kind within
   an hour.  (a) Local minima of a scan were ranked by value; a plateau of equal values (no
   clipping from below) filled all the slots, the other exit was never refined, and
   Nelder–Mead climbed to `0.0251100` at an asymmetric centre whose true value is
   `0.0250913`.  (b) The repair compared neighbours with a tolerance of `10⁻¹⁵`; next to
   exact zeros the scan has values of `5·10⁻¹⁷`, the zero region was dropped, and the
   maximiser reported `0.0521` at a profile whose value is `0`.  *Rule adopted:* an optimum
   is re-evaluated with an inner solver that shares no approximation with the one used in
   the search (here: clippings with the minorant `v`, against a generic convex programme per
   exit type with `I`), and a search result is not quoted before that.
8. **"Small cubes will test the isoperimetric statement."**  On `Q_3` and `Q_4` every subset
   satisfies it without any error term, because `Φ⁺(D) < 1` puts all of them in the volume
   regime; the tests say nothing about exponents.  Families of sets at `n = 96, 144` did not
   see the free-block gain either (it is below the finite-size terms there); the
   single-letter search found it, and exact sums at fixed profiles confirm it from
   `n = 300` on.
9. **A harness test that "refuted" Theorem 11.79(b)** for a few minutes: the coordinator's
   first version compared a truncated cone with the truncated cone around its Gibbs shell
   at an accuracy relaxed on the wrong side.  Both statements of the theorem are
   consequences of the triangle inequality and hold *exactly* on a grid; the test now
   checks them without tolerance, and they hold with equality whenever the truncation
   shell lies beyond the Gibbs shell.
10. **A documented refutation that would have "refuted" a true statement.**  The first
   version of harness test DEAD.22 (cones around shells fall short at `u = 0.30`) scanned the
   accuracies `e ≥ R − 0.003` only; at `u = 0.35`, where the statement is true, the feasible
   accuracies are `e ≤ 0` and lie outside that range, so the test reported the same
   "refutation".  Its mutation — the same test at `u = 0.35`, where the refutation must
   disappear — was the one mutation of 246 that was not caught, which is how the flaw was
   found.  A test of a negative result needs a control on which the positive result holds.
11. **A threshold quoted from a finite difference.**  The threshold `E` of the field case was
   given as `0.21227` (`p = 0.1`, `u = 2`) in the brief for workstream T and in THY-REQ-0007;
   that is `F*(t)/t` at `t = 10⁻⁴`.  The threshold is the limit, the largest chord gap of
   `ln 2cosh(x/2)` over the window of fields: `0.212295` (and `0.103131`, not `0.10312`, at
   `p = 0.3`, `u = 1`); `R^max(0.3E) = 0.023270` as in the theory report (`0.023273` belongs to
   `0.3·0.21227`).  Found by the workstream's control computation.

## D50. Rounds of adaptivity: the mechanism the coordinator expected is not the one that works, an estimate that bounds nothing, and three numerical traps (cycle 10; workstream U)

1. **"A separation, if there is one, needs instances in which finding one level of
   structure does not reveal the location of the next — nested basins with hidden
   centres"** (the coordinator's observation (iii) in the brief for workstream U).  It points the wrong way.  In every nested family that could be analysed —
   balls inside plateaus, concentric balls in growing sets of blocks, max–min nests of
   cones with independent centres — two rounds cost exactly `e^{nh}`: a structure that
   matters is wide, a blind batch of `e^{nh}` points lands on every level that is cheap, and
   what remains hidden costs at most `e^{nh}` again from where the batch stands (the erosion
   inequality, workstream U §3.3; a proof in one case, random search over up to four levels
   otherwise).  Moreover a dip that sticks out of a plateau is read off from the antipode
   of the plateau's centre (Proposition 11.88(b)).  **The separation that exists comes from
   dilution**: a structure in one block that is *not* localised — a flat histogram, every
   shell equally heavy — forces a blind batch to spread over the shells, and on each shell
   it sees too little of a second block to notice a dip there (Theorem 11.86).  Twice in the
   workstream hand computations with nested families produced instances that seemed to
   cost a fully adaptive algorithm more than `e^{nh}`; the necessary conditions "`r = ∞` gives
   at most `h`, `r = 1` at most `a`" caught both.
2. **"`r` rounds of local descent cost about `e^{na/r}`, so two rounds cost about `a/2`"** (a
   scratch computation of the coordinator while the workstream was running: the cost of
   descending a cone in `r` batches).  It bounds nothing.  A cone is an easy instance (its
   centre is found from `n + 1` evaluations), so a descent on it is not an algorithm for the
   class, and its cost is not a lower bound either.  What is proved: `τ^{(2)} ∈ [0.359a, 0.624a]`
   at `u = 1`; and the two-level value `τ₂ = 0.5006a` of §11.19 is reached only by a ladder
   with unboundedly many rungs, i.e. rounds (four rounds give `0.481a`).  Harness XX.3,
   mutation M1.
3. **The twins without the cap.**  The first version of the pair of Theorem 11.86 — the lower
   McShane envelope of the flat histogram from what a blind batch sees, without the cap
   `g₁ + g₂` — plateaued at `1.18h` in exact computations where the analysis predicted
   `1.37h`.  Below the range that the first batch sees, the first-block profile continued as
   a full cone, whose bulk is *visible* to the second batch and heavier than the typical
   type: the visible maximum was not zero.  The analysis had assumed a flat histogram on
   all shells.  *Lesson (again, D45):* compute the visible maximum, do not assume it.
4. **The product formula for the measure of an intersection of balls with independent
   centres**, used outside its range: at `u = 4` it gave a one-round value `1.087a > a`.  Two
   balls of radius below `n/4` around centres at distance `n/2` are disjoint; the formula
   holds on average over the centres only.  Caught by the one-round necessary condition.
5. **A three-round lower bound by iterating the two-round construction** (three blocks:
   flat histogram, a structure the first batch cannot see, a dip the second cannot
   follow): the hidden gain at the budget `e^{nh}` is negative for every split tried,
   `≈ −φ₁/2` for a small first block.  The second batch knows the first centre and has the
   full budget on a smaller cube, whose own hinted exponent is smaller.  Whether three
   rounds reach `h` on the whole class is open in both directions.
6. **Three arithmetic traps.**  (a) `p₁ = 1 − Σ_{W₁}P` in floating point is zero or negative
   from `n ≈ 1600` on; tail probabilities must be summed in log space over the complement
   (workstream).  (b) The coordinator's first helper for the lower bound of all algorithms
   computed `ln(e^x − 1)` through `expm1`, which overflows from `n ≈ 3000` on and returned a
   radius of 710 instead of 1217 (an "exponent" `0.165` instead of `0.0301`); now `x + ln(1 − e^{−x})`.
   (c) The coordinator's first harness test for the conditional covering exponent ran at
   `n ≤ 240` with tolerance `4 ln n/n ≈ 0.1`, larger than the term `KL(σ‖½)` it was meant to
   see; two mutations survived until the test was moved to `n = 300, 600` with tolerances
   calibrated on the exact counts.

## D51. The adaptive question for function-of-type known parts: a workstream that produced nothing, and six wrong turns on the way to the reduction to type classes (cycle 10; coordinator)

Theory report §11.25 is what remained of an attempt to find the exponent of adaptive
algorithms without a hint for a known part that is a function of the type (Conjecture
11.83).  It does not answer that question; it reduces it.  What failed on the way:

1. **Workstream V produced nothing.**  It was commissioned with an open brief
   (`workstreams/V_brief.md`: "nesting by the type of the inner block"; find the exponent or
   say what obstructs it).  The agent read the sources and then spent four maximal
   responses without writing a file, a script or a note, and was stopped by the output
   limit; nothing was recoverable.  *Lesson:* a brief for a problem whose answer may not
   exist must demand written intermediate artefacts — a notes file after every step,
   numerics before theory — and must be cut into steps that can be checked separately;
   the earlier workstreams succeeded where the brief named the first three computations.
   The coordinator then took the question in small steps, one script each.
2. **"Nesting by the type of the inner block gives the adaptive exponent"** (the repair
   proposed in §11.23 and in the brief).  The two facts it rests on are true — given the
   type of the inner block the blocks are independent and the fibre means are exactly
   `u`-Lipschitz — but the outer block then carries a *different* exchangeable law for
   every inner type, all levels below the first are type classes, and the recursion does
   not close on one family of functions.  Resolving the outer block by type as well gives
   products of type classes and discards everything across type classes: the bound of
   Theorem 11.92, which is not tight when exits change the type (a field `p = 0.3` at
   `u = 1`: `0.0291` against the true `0.0250`).
3. **"A fixed split of the coordinates will do on a type class."**  The centre of the hard
   instance can have any outer type, so a window of pairs of block densities would
   matter and the recursion would run over densities.  A uniformly random split removes
   this (Lemma 11.93) — at the price of failures, one-sided and with probability `1/poly`,
   for each fibre separately.
4. **"A synchronous ladder over the type classes refines each class down to its deficit."**
   It refines to half of it: the class and the current maximum are both known only up to
   the common width.  Refining the class with the largest weighted upper end gives
   `max(ε, d_t)`; the additive form `ε + d_t`, which the lower bound suggests, would need the
   leading class at a finer width than the others and is not reached by the simple rule
   (immaterial when the supremum over classes is attained in the contact set).
5. **Two proofs of the odds-ratio lemma that do not work.**  (i) Write the table as a
   diagonal scaling of the symmetric one and drop the two divergence terms: the bound
   that remains is `KL(tilted w ‖ w)`, which exceeds the symmetric value for small `w`.
   (ii) Degradation: an asymmetric channel is *not* a degraded version of the symmetric
   channel with the same odds ratio (one of its two likelihood ratios exceeds `e^{2J}`), and
   conditioning on a product event only gives `I ≤ I_sym/P(accept)`.  The proof that works
   differentiates the capacity along the field of the channel.
6. **Two embeddings of a type class into a cube** (to use Theorem 11.56 as a black box).
   (i) Retractions of the cube onto a type class — greedy or random — send two adjacent
   points to the same point or to points at distance two: the Lipschitz constant
   doubles, and a penalty that concentrates the product measure on the class costs half
   of the slope again.  (ii) The "domino" subcubes of the class `½` (a perfect matching of
   the coordinates, one letter of each kind per pair) are isometric copies of `Q_{n/2}` with
   slope `2u` and average to the class, but a random matching is aligned with a given
   centre with probability `2^{−n/2}`.
7. **A number, and D49 item 7 a second time.**  The slices `0.4`, `0.3`, `0.2` at `u = 1` were
   quoted as `0.0281`, `0.0247`, `0.0189`; the values are `0.028005`, `0.024588`, `0.018842`.  The
   first computation took the inner minimum over a grid of exits — biased upward — and
   the outer maximum selected the bias (`10⁻⁴`, on a grid of 4001 points).  The closed
   form, a solver by clipping and a direct evaluation agree on the second set.

## D52. More than two letters and several site types: six two-letter intuitions that fail, a conjecture and a remark that refuted each other, and a slip in a brief (cycle 10; workstream W and the coordinator)

Theory report §11.26.  The sketch for larger alphabets (workstream F, Proposition F12)
turned out right; these did not.

1. **"The exponents of the site types add"** (D31 again), now quantified: the average of
   the types' exponents at a common accuracy overestimates the chain's by `8.5 %`, `47 %`,
   `172 %`, `1365 %` at `e/E = 0.3, 0.5, 0.7, 0.9` (half binary, half three-state sites).  What
   adds: the game functions at a common slope, the thresholds, the capacities.
2. **"After the best split of the accuracy they add."**  True when the site functions are
   concave; false in general (a chain with a triangle site: by `8·10⁻⁷`, small but not
   zero).
3. **"The site function `F*` is concave, `R^max` is smooth."**  False for three letters: for a
   triangle envelope `(1, 1.5, 2)` the optimal labels switch at `t = 0.378` and `F*` has a convex
   kink; for the uniform four-letter Hamming site the same happens at `t = 0.65`, where the
   best grouping of its letters changes from pairs to singletons.  Concave in 100 two-letter
   cases, unproved.  Harness DEAD.23.
4. **"The labels are distance functions (single dips); binary centres suffice."**  The labels
   are vertices of the site's Lipschitz polytope; beyond the label switch of the triangle
   site an "anti-dip" carries almost half the weight, and the dip theory underestimates by
   a factor up to four near the threshold (D38, now for the worst-case exponents).
5. **"A three-state site is its worst two-state reduction."**  Coarse-graining two states (a
   subclass, hence a lower bound) gives `54 %`–`80 %` of the exponent and too small a
   threshold; deleting a state (not a bound) gives `129 %`–`142 %`.
6. **"A field always helps; the uniform site law is the hardest"** (Proposition 11.65(b), a
   theorem for two letters).  False for three letters with the Hamming envelope: near the
   threshold at `u = 1` (`0.120196` for `(0.05, 0.5, 0.45)` against `0.119499`; workstream), and at
   vanishing accuracy for every `u < ln 2`, where laws near `(½, ½, 0)` are harder
   (coordinator).  Harness DEAD.24.
7. **A conjecture and a remark that refuted each other.**  The workstream scanned site laws
   at `u = 1, 2`, found the uniform law hardest for `h` and `a`, and listed it as a conjecture.
   The coordinator had, the day before, written into §11.25 that at small slopes two
   letters beat three — and, in the same remark, quoted "uniform `k`-ary cubes" for `k = 4`
   with the values of single dips on letters and proposed "a uniformly weighted
   sub-alphabet" as the hardest known part.  Each was right where it had looked and wrong
   where the other had: the uniform law is the hardest for `h` at `u = 1, 2` and not for
   `u < ln 2`; a uniform four-letter site groups its letters in pairs at small slopes
   (indicator functions of sets are vertices of its Lipschitz polytope) and has the
   two-letter values, not the single-dip ones; and near the threshold neither a uniform
   law nor a sub-alphabet is the hardest.  *Lesson:* a scan confirms a statement on its
   grid; the slope is a parameter of the statement, and item 4 applies to the
   coordinator's own closed forms.
8. **A reference value quoted at a finite difference — the third time.**  The brief gave
   `0.008559` / `0.009791` for a two-type control; they belong to the threshold computed as
   `F*(t)/t` at `t = 1/4000` (`0.072271`), not to the threshold (`0.072290`): `0.008557` / `0.009790`.
   The same slip as D49 item 11 and THY-MSG-0009 §3.1; thresholds are limits and are now
   computed as the convex programme `max_M −ln Σ_aΠ_φπ_φ(a)^{M(φ)}`.
9. **Errors of the workstream, caught by its own tests** (kept because the first one led to
   the closed form): a grid-and-zoom maximiser over the Lipschitz polytope returned values
   too small by `10⁻⁶`–`10⁻⁵` — the maximum is a kink, at which all letters are active, which
   is the equalisation behind the Rényi centre; a blind outer search in a max–min returned
   zero where the value is `3.5·10⁻⁴`; exact finite-`n` bounds at the flat-histogram instance
   approach the formula from *below* (a polynomial normalisation), so a table at that
   instance alone would have suggested that the formula is too large by `5`–`12 %` at
   `n ≈ 450`; isoperimetric test families at `n ≤ 72` have no power against a wrong exponent
   function and are recorded as such.


## D53. What the referee of the mean-field section found: a numerical statement made at one slope and stated for all, an interval whose "upper end" was a lower bound, and two numbers nobody had recomputed (cycle 10; referee R10 on workstream T and theory report §11.23)

Referee R10 (`docs/reviews/R10_referee_report.md`) found no critical error in §11.23 and
confirmed its core (the isoperimetric theorem for every rate function, the convex case,
the every-`n` statements).  What it did find is recorded here because each item is a
*kind* of error that the coordinator's own check — re-derivation of the proofs and
re-computation of "every headline number" with independent solvers — had passed.

1. **"For `1 < βJ ≤ βJ*(e, u)` the barrier is invisible" — false for large slopes.**  The
   workstream proved a local statement (the symmetric exit of the uniform cube's optimal
   profile is a strict local minimum iff `βJ < βJ* = 1 + u·c₂/(2L)`), observed at `u = 1` and
   three accuracies that the local minimum is the global one, and wrote the conclusion
   `R_H = R_unif` for `1 < βJ ≤ βJ*` with the label "numerical" but without the range.  The
   coordinator re-computed it at six couplings — at `u = 1` — and copied the sentence into
   Proposition 11.81(b), into finding 4 of the section head, into Corollary 11.91(iii) and
   into a message (THY-MSG-0009).  At `u = 8`, `e = 0` the statement fails: at
   `βJ = 8.2632 < βJ* = 8.3366` the barrier `I(½) = 3.438` exceeds the uniform cube's threshold
   `E_unif = ln cosh(u/2) = 3.307`, the *constant* exit at a well (`MI = 0`) is feasible for the
   uniform cube's profile, and its value is `0`; the best profile found has `0.3674` against
   `R_unif = 0.3985`.  A local analysis around one exit cannot see a far exit.  On the
   referee's grid the junction is `min{βJ*, βJ_w}`, `βJ_w` the coupling at which a constant
   exit becomes feasible; at `u = 1` the second number is far away.  Harness DEAD.25.
   *Lessons:* (a) a statement with a free parameter that was computed at one value of the
   parameter must carry that value — the same lesson as D52 item 7, one day later;
   (b) "local minimum, numerically global" needs the competing far exits named, and the
   cheapest of them (a constant profile) has a closed form that would have shown the
   failure in one line; (c) a coordinator who re-computes at the workstream's own
   parameters confirms the workstream's arithmetic, not its statement.
2. **An interval whose upper end was a lower bound.**  At `u = 0.30` the best cone around a
   shell certifies `0.00184` at the accuracy `S(0)` while the best binary centre has
   `R^{(2)}(0) = 0.00226`; both documents wrote "the exponent of non-adaptive algorithms is
   known only to lie in `[0.00184, 0.00226]`".  The upper bound of Theorem 11.79(c) is in
   terms of the *full* supremum `R_H`, of which `R^{(2)}` is a lower bound; what is proved is
   `[0.00184, 0.00338]` (from `R_H ≤ R_unif`).  The same care had been taken at `u = 1` (where
   the text says "if binary centres are optimal") and was dropped here.  *Lesson:* in a
   sandwich, write next to every number whether it bounds the quantity from above or
   from below; a supremum that has only been searched is a lower bound everywhere it is
   used.
3. **Two numbers wrong in the third digit, both outside every re-computation.**
   `e₀ = 0.00181` was a linear interpolation between `e = 0.001` and `0.002` (the crossing of
   the two branches is at `0.001804`); `a_cone = 0.0446` is the mutual information of the
   *metastable* Gibbs shell of a cone at centre type `≈ 0.5025` — the global shell has
   `0.04435` at type `½`, where the two wells tie (re-computed by the coordinator after the
   report: `0.044351`; `0.044596` on the metastable branch).  No output file of the
   workstream contains `0.0446`.  Neither number enters any conclusion.  *Lesson:* the
   coordinator's "every headline number" was a list chosen by the coordinator; numbers
   quoted in passing were not on it.  A local minimiser started on the wrong side of a
   tie returns the metastable branch; the global shell needs all local minima.
4. **A certified exponent rounded up.**  "`(1 − 2δ)e^{0.02509n}`" for the certified `0.025087`.
   A lower bound is rounded down.
5. **A loosely worded step that happened to have a true conclusion**: "every constant `ν` is
   at distance `≥ η`" as the argument for a positive threshold in the convex case (the
   minimiser of the Lagrangian is not constant; the repair is two inequalities), and
   "`R_λ` is nonincreasing" where only `R̄_λ` is (admissibility at negative accuracies) — the
   coordinator had "read, not re-derived" exactly these two proofs.
6. **What the theory report said beyond the workstream's report** (the referee compared
   the two statement by statement): `R_H = max_t[F* − te]` without the restriction `e ≥ 0`
   (true for `R̄_H`, with an argument that was missing and is now in Theorem 11.80(c));
   "the best cone around *any* shell" for three families of shells; "every coupling
   `−40 ≤ βJ ≤ 1`" for eight couplings; and an interpretation that dropped the caveat that
   the optimal fixed sample is stratified over *all* level sets.  Each is the
   coordinator's summary going one step past its source.
7. **For the record: the coordinator read the referee's draft.**  The eleventh checkpoint
   cites finding M1 (in Corollary 11.91(iii)) before the referee had handed in the report —
   the coordinator had read the draft in the referee's scratch directory.  The finding
   did not change, and the referee gives two precisions (the failure needs large slopes
   *and* small or negative accuracies; that `R_H` itself leaves `R_unif` rests on searches
   in two cells).  Reading a draft is not a breach of the referee's independence — nothing
   was sent to the referee — but a citation of an unfinished report should say that it is
   one; it did not.

## D54. Ratios of macrostates and local data with a field: four wrong first guesses of the coordinator (cycle 10, thirteenth checkpoint; theory report §§11.28, 11.29, and the remark after Theorem 11.56)

1. **"The extremal residual of a ratio is constant on each macrostate"** — the first guess
   for the uncertainty of a free-energy difference: shift the two states against each
   other by their distance, `R⁺ = e^{d(B,A)}·w(A)/w(B)`.  False already for three states (the
   Scientific Discovery Division's example: `e + e^{10}` against `2e`), and false for the two
   halves of the cube, where the extremal residual is the maximal field (`2.8` times the
   constant shift on `Q_6`).  Harness DEAD.26.
2. **"The signed distance to the interface is the extremal residual."**  The natural
   second guess for a threshold macrostate — `−d(B, x)` on `A` and `+d(x, A)` on `B` — is not
   admissible: across the interface it jumps by twice the envelope.  The closure
   equations of Theorem 11.105(b) have the maximal field as their only symmetric solution;
   the "distance from the other side" enters *alternately* (lowest extension to `A`,
   highest to `B`), not symmetrically.
3. **A sign change that was not one** (Proposition 11.109).  To match the oracle's answers
   at a null and at its dips, the first argument swept the additive instances `γ|x|` from
   `γ = +u` to `γ = −u`: at the two ends no instance of the class has a smaller or a larger
   one-body marginal, so the mismatch "must" have opposite signs there.  It is exactly
   zero at both ends — an instance with no slack in one direction has no dips — and for
   some families of dips (small balls around centres of type `½`) it has one sign in
   between.  The brute-force scan on `Q_10` showed it before anything was written.  What
   survives is a criterion, and the two consequences are labelled conjectures.
   *Lesson:* an extremal instance is extremal because nothing can be done to it; do not
   use it as the end of a homotopy of perturbations.
4. **"Every sample of Algorithm 2L⁺ is below `2e^λM†`."**  The coordinator's first answer to
   the engineering division's question, derived from the constants of Theorem 11.52 and
   transferred to Algorithm 2L⁺ without re-reading its closure test.  In 2L⁺ the closing
   radius `r†` is defined through the two-sided ratio, and after a populated level the
   closure of an unpopulated pass needs the radius to drop by `⌈λ/u⌉` — the cap is
   `2·max{e^λM†, M‡}`.  The simulation found a sample of `3.69·M†` at `λ = ½`, above `2e^{1/2} = 3.30`
   (harness XVI.4, mutation M1).  *Lesson:* D52 item 7 and D53 item 1 a third time — a
   constant was carried from the setting in which it was derived to a neighbouring one.
5. **Two convergence tests that tested the lattice.**  The first check of the
   exponential-scale formula used thresholds off the lattice of types (`1.1`, `0.6`): the
   lattice sets then differ from the continuum sets by `O(1/n)` in a way that is not
   monotone in `n`, and a test "the gap decreases" failed on a true statement.  With
   thresholds on the lattice the gap is `−0.27/n`.  And the exploration of the
   type-restricted dip exponent at the zero residual (for Proposition 11.109(e)) was
   launched as a nested grid with an inner solver in the loop and ran into its time limit;
   a version reduced by a factor of twenty needed fifteen minutes for one row of eight
   numbers — the coarse numbers quoted in Proposition 11.109(e).

## D55. What five reviews by another division found in sections that our own checks had passed: a bound "in every run" that held on the good event, a headline for three exponents with a corollary for two, a duality step tested only where it was true, a "plateau" that was a bracket, and classical objects under new names (cycle 10, fourteenth checkpoint; Scientific Discovery Division, SCI-REV-0001, -0002, -0003, -0005, -0006 on theory report §§11.25, 11.22, 11.24, 11.26 and on the prior-art columns)

No exponent, no inequality between exponents and no machine-checked statement was found
false; one clause of the statement of a theorem was — Theorem 11.84(ii), item 1 below.  (The
first wording of this paragraph, "No theorem was found false", was itself too strong:
Scientific Discovery Division, SCI-REV-0009.  The same sentence stands in our published
message THY-MSG-0013, which is not edited.)  What was found is listed here as lessons,
because each item had passed the coordinator's own check and, in three cases, an earlier
referee's.

1. **"In every run" for a bound proved on the good event — for the third time**
   (Theorem 11.84(ii)).  The candidate sets of the batched schedule were claimed to have at
   most `N_l` members "in every run (deterministic)".  The count uses
   `L_i ≥ U_ie^{−x_{l−1}}`, which holds only if the inner procedure of the previous rung returned
   a bracket of the promised ratio; a bracket procedure may return its trivial bracket
   with probability `δ′`, and then every outer point is a candidate (`2.2·10¹²` against
   `N_2 = 4.4·10⁹` with the constants of the theorem).  The same gap had been found by referee
   R7 in Theorem 11.52 and by referee R8 in Theorem 11.56; the coordinator's check of Theorem
   11.84 "line by line against the proof of Theorem 11.56" followed both claims on the good
   event and never asked what an inner procedure may return off it.  *Repair:* a stopping
   rule checked before any evaluation of the stage.  *Lesson:* a cost bound of a randomised
   procedure is a statement about every run; for each sub-procedure ask what it may return
   when it fails, and put the test that protects the budget before the spending.  Harness
   XX.5, DEAD.27.
2. **A headline about "exponents" where the corollary lists two of three** (§11.25).  "No
   known part that is a function of the type is harder than the uniform cube … an
   interaction without a field changes no exponent."  Corollary 11.91 covers the hinted
   exponent of symmetric instances and the non-adaptive exponent; the exponent of adaptive
   algorithms without a hint — the one that is small on the cube — is covered for
   ferromagnets and fields only, and is otherwise Conjecture 11.94.  The sentence was
   repeated in the title, in §0, §8, §10, §12, the README and three messages.  *Lesson:* this
   report has three exponents; a headline must say which, for which algorithms, at which
   instances.
3. **A duality step tested numerically only where it was true** (Theorem 11.90(a)).  "Every
   law with mean `κ` is a mixture of two-point laws with mean `κ`, so two blocks suffice."
   At negative accuracies feasibility is a *second* linear constraint on the law, the
   two-point components of a feasible law can be infeasible, and the chain of equalities,
   read literally, gives `+∞`.  The statement is true (vertices of the feasible polytope
   have at most three atoms, and three atoms mean zero budget), but our scripts and the
   harness tested profiles with more than two blocks at `e ≥ 0` only — while the
   non-adaptive half of Corollary 11.91 uses the function near `e = −K(u/2) < 0` — and the
   status line said "every step checked numerically".  *Lesson:* test a formula on the
   whole range on which it is used; "every step checked" must name the ranges.  Harness
   XXI.6.
4. **"The plateau is real, it is in the hundreds"** (§11.22).  One sentence joined a theorem
   (every limit point of the certificate sizes lies in a bracket), a conjecture
   (convergence: proved for bridges off a countable set of accuracies that nobody has
   identified, conjectured for walks) and an estimate (the value; the chain length at
   which it is approached).  The same paragraph counted a sketch as a proof ("five
   vertices settled", "`2.2 ≲ vol 𝒦`").  And the lower end of the bracket, 50, used one
   triangle of the body although the section's own tools — explicit bridges, the one-sided
   rate, convexity — give 116: the reviewer raised our bound with our lemmas.  *Lessons:*
   three labels, three sentences; and before a bound is published, ask what the tools
   already in the section give.
5. **A negative remark is a claim too.**  "Nothing in this argument says how fast they fill
   it" (after Theorem 11.69) is true at the boundary and false in the interior, where the
   same three hypotheses give the rate `M^{-1/2}` (now Proposition 11.69a).
6. **Sentences about the state of a field age.**  "Verified checkers exist for exact model
   counting only" was false from 2024 on; "the 43-times figure is the number to beat" was
   obsolete from 2025 on; both stood in the summary table and in `prior_art/L1`.  *Lesson:*
   date such sentences, say who read what, and prefer "not found in these searches on
   this date" to "does not exist".
7. **Classical objects under new names.**  The reduced envelope of the normal form is a
   weightable quasi-metric; the profile distance is the Wasserstein distance between global
   distance distributions, a lower bound of the Gromov–Wasserstein distance, whose zero
   set is homometry; the limit of a super-additive family of sets is, for exact semigroups,
   a Newton–Okounkov body; the lever-arm "law" is the growth of a moment of inertia and its
   weighted-`ℓ¹` bound a published certificate in robot motion planning; the
   finite-temperature formula is an example in Merhav's paper, not a theorem.  None of
   these names was in our eight prior-art files.  *Lesson:* a reformulation is recognised
   by someone who knows the neighbouring field; an independent prior-art review belongs at
   the start of a write-up, not after thirteen checkpoints.
8. **Stated too modestly, twice.**  The property that distinguishes the residual kernel — one
   certificate for a whole class of residuals — was listed as one kernel among three.  And
   the sharp lever-arm constant was in workstream G all along, but Theorem 11.36 said
   "`c_i ≥ 0.824…`" and "lower constant numerical", so that the reviewer derived the same
   formula again and reported it as an improvement.  A tag that does not say which constant
   is numerical hides the theorem next to it.
9. **A pair-distance profile does not identify a conformation** — and the theorem usually
   quoted for the opposite (generic reconstructibility from the distribution of distances)
   excludes chains by its own genericity condition, because bond lengths coincide.  We had
   written "large fibres" and quoted a count; the reviewer separated three sources (labels,
   homometry, truncation) and found non-congruent lattice chains with identical complete
   distance multisets from 6 beads on (harness XIV.5).
10. **"Re-computed" without a script.**  When the corrections were applied, a dozen new
    sentences cited computations that existed only in scratch directories.  They are now
    in the repository (`experiments/coordinator_checks/rounds_U/`, `slices/`,
    `limit_shape_review/`), re-run by the coordinator with identical output.
11. **In the heteropolymer section (§11.26; SCI-REV-0005 and SCI-REV-0001 §5).**  (i) The
    isoperimetric statement that the nested algorithm needs — for the measure `μ_H`, with
    an error term uniform over compositions — was stated and proved in the workstream's
    report only; our text referred to "Theorem 11.97 in the form for `μ_H`", which did not
    exist in it (now Theorem 11.97(c)).  (ii) "Families of procedures are indexed by
    compositions" was the whole of our account of a level induction whose inner blocks
    have a different composition at every level; the workstream's argument for the
    uniformity cited the continuity of the wrong function (now written out, with a
    Lipschitz bound, in Theorem 11.101).  (iii) "Site laws close to `(½, ½, 0)` have the
    two-letter values": false in both directions — at `u = 0.5` the law `(0.05, 0.5, 0.45)`
    is above the two-letter cube by `0.03 %` and `(0.02, 0.49, 0.49)` below it; what is a
    theorem is the comparison for laws with weight exactly `½` on a set of letters, and the
    ceiling `u²/32`.  (iv) "Machine-checked: the every-`n` lower bounds" — machine-checked are
    the general inequalities behind them; the product step for several site types is on
    paper.  (v) A number (`+0.0052`) taken from a second difference on a grid of step
    `5·10⁻⁴` and reported as a slope jump (it is `+0.0056`).  (vi) A Lean theorem cited for a
    recursion with another start (`exactRec_tendsto` starts at `θ_na`; the level induction
    starts from complete enumeration, which is `iterates_lt_hint_add`).  (vii) The
    dictionary sentence "a fixed sample of `e^{nθ}` points certifies `E_sp(θ)`; adaptivity gains
    exactly `θ`" without its ranges (`θ < a`; `θ < h`), its mode (asymptotic, worst case) and
    the convention for `E_0` (maximised per site type).  Harness XXII.5.
12. **A mutation "caught" for the wrong reason, and a test that failed only in the mode
    the audit runs** (found when this checkpoint's own audit failed).  The new test XXI.6
    carried a coverage guard ("at least 60 cases") that the full run met (93) and the
    quick run of the audit did not (56): the test *misbehaved in quick mode without any
    mutation*.  The mutation runner ran every mutant in quick mode and counted exit
    code 1 as "caught" — so all four mutations of XXI.6 were reported as caught, and one
    of them (**the bound `MI ≤ h(κ)` weakened to `0.9·h(κ)`**) was in fact not caught by
    anything: no sampled profile came near the bound.  Three repairs: the guard now
    counts what the quick run delivers; the test checks the bound where it is attained
    (the pure profile, blocks of density 1 and 0, has `MI = h(κ)` exactly); and the
    mutation runner now runs the **unmutated** harness on the same selection, in the same
    mode, before the first mutant of a selection, and fails if that baseline misbehaves.
    *Lesson:* "the mutant fails" is evidence only relative to "the original passes *under
    the same conditions*"; and a new test must be run in every mode in which it will be
    run later, before its mutations are written.

## D56. Two conjectures that another division settled within hours, and a "certificate" that is not one (theory report §§11.29, 11.30; fifteenth checkpoint of cycle 10)

1. **A conjecture offered with a formula and two numbers from a grid of seven points**
   (first version of Proposition 11.109(e)).  We wrote that with a one-body marginal
   oracle the exponent of the zero residual is `sup{r_μ(e) : μ̄ = p}`, "`0.0129` against `0.0134`,
   about `3.5 %`".  The Scientific Discovery Division's workstream F (SCI-RES-0006) showed:
   the exact value without the oracle is `0.013669` — our `0.0134` was the best of seven
   grid points, reported as a maximum; our `0.0129` is an *upper* bound (it equals a tilt
   bound that the division proved), not the value; and the decrease is between `5.3 %` and
   `7.6 %`.  The formula over-counts for a structural reason we had not looked at: **"a
   profile of mean type `p`" is not "a dip whose excess mass has type `p`"**.  The excess
   mass of a dip around a shell sits on that shell only if the shell's block laws lie in
   the window `[p₋, p₊]` of one-body marginals; otherwise it sits on the nearest shell
   inside the window, the dip's mean type is another one, and the oracle sees it.  The
   maximiser of our formula has a block law outside the window.  *Lesson:* a coarse
   search may support the *direction* of a statement; a number quoted from it is a
   claim about a maximum and needs the maximiser to be examined — here one look at the
   maximising profile against Proposition 11.109(a), which we had proved two paragraphs
   earlier, would have shown that it is not admissible.  Harness XXIII.7 (mutations M7,
   M8 are the two claims of the first version).
2. **A true conjecture with an argument that could not be completed** (first version of
   Proposition 11.109(f)).  To make the class exponent survive the oracle we modified
   the flat-histogram instance by a logarithmic well — a pointwise *maximum* of weights —
   and took its deepest dips.  Then the excess measure moves with the tuning parameter,
   the matching equation needs an intermediate-value argument, and that needs a
   concentration statement we could not prove (and which, for the profiles of item 1, is
   false).  The division's proof adds a *sum*: a fixed excess, and a null moved by an
   admixture of an extreme additive instance.  The matching equation is then linear in
   one weight, holds exactly, for every `n`, and costs a factor `(1 + b)·n`.  *Lesson, in
   the division's words:* an extremal instance is useless as the end of a homotopy of
   perturbations and perfectly useful as an admixture.  More generally: in a class that
   is a convex cone in the weights, look for constructions that are *linear* in the
   weights before tuning nonlinear ones.  The trap of D54 item 3 remains a trap.
3. **The naive interval is not a certificate** (harness DEAD.28).  "The sample mean of the
   Boltzmann factors of the remainder plus two standard errors is an upper confidence
   bound for `E_π e^{−r}`": false for every sample size at members of a box class with a
   rare deep dip — with a dip of probability `1/m` the sample contains no dip point with
   probability about `e^{−1} ≈ 0.37`, the sample variance is then zero and the interval a
   point below the truth (frequency `0.3705` in the test).  This is the precise sense of
   "a typical-norm estimate is not a certificate" (§11.30): the number of samples below
   which *nothing* is certified is set by the floor of the class, `e^{ρ₋}/ε`, and no
   statistic of the sample can replace an a-priori floor.  The science division's pilot
   had met the same fact empirically (sup-norm remainders estimated on samples were
   exceeded on held-out conformations by factors up to ten).
4. **A "tightness" check that no instance exercised** (found by the mutation of harness
   XXIV.2).  The test asserted that the least detection probability of a far member in
   the linear relaxation is at most `2p`.  True, and trivially so — but in all random
   instances it was below `1.2p`, so that weakening the constant changed nothing: the
   check tested no boundary.  The factor 2 is attained exactly at the centre of a
   constant box; that instance is now part of the test.  The same pattern as D55 item
   12: an inequality is tested only where it is nearly an equality.
5. **A citation to a file that does not contain it.**  The draft of §11.30 cited the
   empirical Bernstein inequality "in the form recalled in `prior_art/L7`"; that file
   does not mention it.  The reference was from memory.  It is now in
   `docs/prior_art/L10_box_classes.md` with its reading level (a search summary), and
   its use is tested by simulation.

## D57. A second way for a mutation to be "caught" for the wrong reason, a condition that was vacuous at the sizes tested, and a statement written before its model was looked at (sixteenth checkpoint of cycle 10)

1. **A mutant that crashes is not a mutant that is caught.**  The harness reports a test
   that raises an exception as "ERROR" and exits with code 1, and the mutation runner
   counted every exit code 1 as "caught".  One of the oldest mutations (VII.1 M2b, a
   mis-modelled leaf rule) made a linear programme unbounded, the test then negated
   `None`, and the crash was recorded as a detection — for eleven checkpoints.  Found when
   the mutants of a new test were inspected one by one for *why* they fail.  Now: the
   runner rejects a mutant if any test of it ends with an exception, or if it does not
   reach the harness's own verdict line; the leaf-bound function returns `+∞` for an
   unsolved programme, and the test treats a non-finite bound as a failed comparison.
   With D55 item 12 this makes three conditions for "caught": the unmutated test passes
   in the same mode, the mutant runs to its end, and the harness itself reports the
   failure.  All 380 mutations existing at that time were re-run under the new rule:
   one crash, no other change.
2. **A condition that was vacuous at the sizes tested** (harness XVIII.7, mutation M1).
   The exact semigroup of Proposition 11.69b needs three conditions on a bridge: the bond
   before the last is an up-bond, and no pair between a linker and the bridge at either
   end.  Up to 7 beads the second and third hold automatically whenever the first does,
   so a test restricted to 7 beads (the quick mode) could not distinguish the proposition
   from the false statement without them.  From 8 beads on they can fail (8 of 264).  The
   test now always includes 8 beads and requires that such bridges exist.  *The same
   pattern for the third time in two checkpoints* (D55 item 12, D56 item 4): a clause of
   a statement is tested only if the test set contains a case in which that clause, and
   nothing else, decides.
3. **A statement written before its model was looked at** (first draft of Proposition
   11.18b(c), corrected before it was committed).  "With third-order constants and an
   additive known part the exact criterion is: no set of sites is over-dense with respect
   to the triples."  False as stated: the lower model of third order contains the
   *measured* second mixed differences of the residual on the ball, which have no sign,
   so the criterion is a pairwise minimisation with those terms, and the triple-density
   condition is exact only when they (and the known pair terms) vanish.  The
   combinatorial equivalence that the harness tests (shares exist iff no over-dense set)
   was true all along; the sentence connecting it to the model was not.  *Lesson:* a
   harness test of a combinatorial lemma does not test the sentence that applies it.
4. **A sampler called "stable" that is not, at the sizes it was written for** (found by the
   Scientific Discovery Division, SCI-REV-0007 §4; confirmed here).  numpy's
   `Generator.binomial(n, p)` is biased low for `n ≳ 10¹⁷` with mean between about 60 and
   `10⁴` (mean `91.26` instead of `92` at `n = 2⁶¹`, `z = −49` in `4·10⁵` draws; `−0.21 %` at `n = 10¹⁸`,
   `np = 500`; nothing detected at `n ≤ 10¹⁶`, at `np = 20`, or for the Poisson sampler).
   Workstream K's `stable_multinomial.py` sends exactly those nodes to it.  The harness
   itself draws binomials only at cube dimensions and is not affected; which published
   numbers of §11.19 are, and the corrected sampler, are the subject of the next
   checkpoint (the review is being applied).
   *Completed at the eighteenth checkpoint, and this item's own description corrected*
   (`experiments/coordinator_checks/nested_review_R6/`): the defect is wider than "biased low
   for `n ≳ 10¹⁷`, means 60 to `10⁴`".  It begins near `n = 10¹⁵`; the window of means begins
   sharply at `np = 44` (nothing at `43.9`, a wrong mean and variance at `44.1`) and is
   detectable up to `10⁵`; the mean is too *high* at `n = 2⁵³`, `np = 500`; and at `n = 10¹⁷`,
   `np = 92` the mean is right and the variance `6 %` too small.  "Nothing detected at
   `n ≤ 10¹⁶`" was a statement of too few draws.  No published number is affected: of the
   `93 402` binomial draws of the published run with a count of at least `10¹⁴` none had a
   count above `10¹⁵` together with a mean below `10⁸`.  The sampler is replaced by an exact
   reduction to at most `2³¹` trials by order statistics; the first version and its outputs
   are kept under `first_version/` there.  *Lesson, twice:* a referee's "correct down to
   `p = 10⁻²⁰`" (R8, m6) had been measured at means below 30 and was passed on by us to the
   other division as a recipe (THY-MSG-0007 §2: "a tail-safe sampler can be built from
   sequential `Generator.binomial` draws" — withdrawn by THY-MSG-0015); and our own first
   confirmation of the division's finding repeated its window instead of scanning for
   the window's ends.
5. **A headline that was true of a constant box and misleading for everything else, and
   an illustration with the wrong number** (theory report §11.30 as published at the
   fifteenth checkpoint; found by the Scientific Discovery Division, SCI-RES-0007 §3(1)
   and SCI-MSG-0017).  The section said that the cost of a box class "does not depend on
   the size of the system", and illustrated it with floors of `3.7` and `15.6 k_BT` "whatever
   the chain length".  The theorem is right and both sentences mislead.  The cost is the
   Boltzmann factor of the free-energy distance to the floor; for a remainder that is a
   sum over a growing system that distance grows with the system, so the exponential is
   renamed, not removed — and the two numbers were two-sided sup norms of *one* remainder
   at two chain lengths, taken from the division's own pilot, where the theorem charges a
   one-sided distance.  The division then measured that distance on 74 enumerated
   instances: between `0.07` and `243`, linear in the chain length in every family, and
   unrelated to the width.  *Lessons:* a class whose defining constant depends on the size
   must not be headlined as size-free; and a theorem should be illustrated with the
   quantity it charges for, computed for the example, not with the nearest number at
   hand.
6. **"Without a floor a single hidden state defeats every sampler" — true of polynomial
   moments, false of exponential ones** (theory report §12 item 13(b) and the first
   "reading" of §11.30 as published at the fifteenth checkpoint; corrected by the
   division's Rényi family, SCI-RES-0007 §3(3)).  We had dismissed moment constraints
   under the known measure in one sentence, with the example `E_π e^{−2(r − r̄)} ≤ κ`.  That
   example is an *exponential* moment, i.e. a ball in `L²(π)` for the Boltzmann factor of
   the remainder, and there a hidden state of mass `q` can raise the partition sum by at
   most `B√q` (Hölder): the cost is `e^{κ}/ε²`, not the number of states.  What a single
   hidden state defeats is every bound on *polynomial* moments of the remainder energy
   (mean, root mean square).  The sentence was written without the two-line computation
   that decides it.  Now Proposition 11.112, tested in harness XXIV.7.

## D58. A two-sided bound that was one-sided near the floor, a hint that was credited with what it does not do, a section written before the literature was read, and a mutant that was not false (seventeenth checkpoint of cycle 10)

1. **"The two bounds differ by a factor that depends on `ε` and `δ` only" — false near the
   floor** (theory report Theorem 11.110(e) as published at the fifteenth and sixteenth
   checkpoints; found by the Scientific Discovery Division, SCI-RES-0009 §2 item 4).  The
   upper bound had two terms, from dips and from bumps; the lower bound came from dips
   alone.  At an instance near the floor of the box there are no heavy dips, the lower
   bound was zero, and the upper bound was of order `1/ε`: not a matching pair.  The
   missing half is true and easy — a set with bump weight above `(1 − e^{−ε})Z`, raised to
   the ceiling, changes `ln Z` by more than `ε` — and is now machine-checked
   (`logZ_bumpAlt_gt`, `box_expected_queries_ge_mixed`); the cost is
   `Θ((Z(lo)/Z − 1)/ε + (1 − Z(hi)/Z)/ε)`.  *Lesson:* a claim "matching up to constants" has
   to be checked at the instances where one of the two bounds degenerates; the harness
   test of the bracket (XXIV.3) used instances at the centre only.  Now XXIV.9, with a
   mutation that restores the old statement and is caught.
2. **A count attributed to the hint that a rule without a hint beats** (the same theorem;
   SCI-RES-0009 §2 item 3).  We quoted `1088` evaluations "with a hint" at the centre of a
   constant box.  The division's rule — stop when the first `N(v)` values of the remainder
   under `π` agree — needs `545` with no hint.  Two things were wrong: the general bound
   loses a factor two there (at the centre the dip and bump samplers coincide with `π`;
   now `detect_ge_of_proportional`, `544`), and the sentence credited the hint with a
   saving that it does not make at flat instances.  A hint removes a variance term.
   *Lesson:* before attributing a cost to a resource, compare with the best procedure
   without it at the same instance.
3. **A section written before the literature was read.**  Our prior-art note for §11.30
   was three queries at the level of search summaries; the section said "no novelty
   claimed beyond the placement".  The division's full-text search (47 sources) found
   every ingredient in print — Hoeffding's two inequalities of 1963 for parts (a) and
   (f), the stopping criterion of provable partition-function algorithms for (b),
   importance sampling against an upper-bounding model for the cost quantity, a 2026 paper
   for the divergence table that the division had itself sent us as new — and did not
   find the hinted two-sided statement.  The hedge was honest and the order of work was
   wrong: two checkpoints of text, harness and Lean were spent before anyone knew what
   was known.  The division made the same mistake with its addendum and says so.
4. **A constant that was not sharp** (Proposition 11.112(e) at the sixteenth checkpoint):
   `D_2 ≤ Σc_i²/2` is true; `D_2 ≤ Σc_i²/4` holds and is attained in the limit of small
   constants (the division's, SCI-RES-0009 §3; re-derived, harness XXIV.7).
5. **A mutation that was not a false statement** (harness XI.19, first version of M1).
   To test the remainder identity of Theorem 11.18d we mutated "the base point is switched
   at the changed sites *before* the first site of `T`" into "*after* the last site of
   `T`".  The mutant survived — correctly: the identity holds for every linear order of
   the sites, and reversing the order turns one statement into the other.  Found because
   the failure of every new mutant is inspected, in both modes, before it is counted
   (D55 item 12, D57 item 1).  *Lesson:* a mutant must be shown to be false, not merely
   different; an uncaught mutant is evidence about the test or about the mutant, and one
   has to find out which.


## D59. A headline that was true at the one slope computed, a completeness claim that needed a product, a remark "not proved" that was false, and a recipe passed on from a check made in the wrong regime (eighteenth checkpoint of cycle 10; reviews SCI-REV-0007, -0009, -0010, -0011, -0012 of the Scientific Discovery Division and our referee R11)

Five reviews were applied at this checkpoint.  No machine-checked statement was touched.
What was false or misleading in our own texts:

1. **"A nearest-neighbour interaction raises the exponents."**  The summary line of our
   workstream Y, carried into the research log and the status file as its headline (marked
   unverified, and never into the theory report).  It is proved where the workstream
   computed it — slope `u = 1`, four couplings — and it is **not** the answer to the
   question that was asked: with the workstream's own Markov recursion and blocks of three
   sites the non-adaptive exponent of the chain is *below* the uniform cube's at
   `u = 3, 4, 6`, and the hinted one at `u = 4, 6` for strong couplings (the division's finding
   M1, SCI-REV-0010; re-computed here with the workstream's functions and with independent
   code in the harness).  The workstream had seen the sign of its own lower bound change
   at `u ≥ 2` and wrote "the direction is not decided there"; our referee R11 checked every
   proof and every number at `u = 1` and did not vary the slope either.  The upper-bound
   tool that decides it was in the report; nobody had evaluated it away from `u = 1`.
   *Lesson:* a qualitative headline ("raises", "never helps", "independent of") drawn
   from a table at one value of a parameter is a statement about that value.  Before a
   direction is written down, the proved bound of the *opposite* sign has to be evaluated
   over the range the sentence covers — here it took one second per cell.
2. **The same headline, by its mechanism.**  The workstream explained the factor at small
   slopes by "the susceptibility".  For this chain that is right; in general the quantity
   is the largest variance per site of a Lipschitz function, and for an antiferromagnetic
   chain it is the staggered susceptibility (the division's Propositions R10.1, R10.2 and
   counter-examples; harness XXV.3).  *Lesson:* a mechanism named after the one example
   in which it was observed is a guess about the others.
3. **Completeness of share certificates on domains with exclusions** (Proposition 11.18c(a)
   as written at the sixteenth checkpoint: "Theorems 11.16, 11.18, 11.18a and Proposition
   11.18b hold").  The bounds and the sufficient directions do; "shares exist whenever the
   exact criterion holds" does not — two sites, three states, the pair of cheapest states
   excluded (SCI-REV-0012 §3).  The proof of completeness on products has one sentence that
   uses the product — "the worst state of a site is its cheapest one" — and the extension
   was written by inspecting which *evaluations* the proofs use, which is the right test
   for the bounds and the wrong one for a statement about minimisers.  Our harness test of
   the domain statement (XI.18) tested the remainder bounds only.  *Lesson:* when a
   proposition is extended "because its proof uses only …", every part of it has to be
   named and checked against that reason; an equivalence has two directions.
4. **"What the pruning discards is the set that (c) is about"** — our description of the
   division's pruned clash-free products.  The division measured it: the pruned product
   is strictly smaller than the largest reset-closed part in 34 of 40 analyses, and in 14
   the minimum of the clash-free domain is not in it at all.  We had described another
   group's data by what our proposition would have liked them to be.  (The division
   corrected its own message in the same review.)
5. **A remark labelled "(not proved)" that was false.**  Proposition 11.69b, sixteenth
   checkpoint: "a head and a tail of two beads already suffice for every bridge with at
   most 10 beads (not proved)".  True as scoped, true at 11 beads, false from 12 — a tail
   of two fails for 16 of the 17 400 pairs (SCI-REV-0011).  Our script tried equal lengths
   only and stopped at 10 beads.  And the proposition itself said less than was true in
   three places (three beads for two and three; a cost of at most 168 for exactly the two
   end terms of the error, at most 60; a threshold `M₀(p)` where every `M` works), because
   it was written for clean bridges only: the division's theorem is the same computation
   for *all* bridges, and the decomposition of the error that makes it a coboundary was
   already in our own remark after Lemma 11.68.  *Lesson:* "not proved" is not a licence;
   a conjecture printed in a theorem's *Numbers* paragraph should have been tested one
   size beyond the sizes that suggested it, and in the asymmetric variants.
6. **"For `d = 1`, where the limit is a point, a super-additive sequence can converge
   arbitrarily slowly"** (the sentence before Proposition 11.69a; unchanged through two
   revisions although the division had flagged it).  Under the two-sided hypothesis (C) a
   point limit has the rate `β/M`; the true example is an interval (SCI-REV-0009, C1;
   SCI-REV-0011, R9b-T2).  Seven further text defects of the same review are listed in the
   research log (a table cell contradicting its sentence; harness counts in an index row;
   "adopted unchanged" for files with a changed header; a bound called "the largest moment
   of inertia"; "No theorem was found false" in D55 above, itself too strong; a docstring
   promising an instance that was not there).
7. **A recipe passed on from a check made in the wrong regime.**  Referee R8 tested the
   binomial sampler at means below 30 and wrote "correct down to `p = 10⁻²⁰`"; we passed
   on "a tail-safe sampler can be built from sequential binomial draws" to another division
   (THY-MSG-0007 §2).  At counts above `10¹⁵` and means above 44 it is wrong (D57 item 4, as
   completed; withdrawn by THY-MSG-0015).  No published number was affected — by the
   structure of the one run that used it, not by design.
8. **Two conditions in the proof of the lowered sample cap** (§11.19): the unpopulated
   pass at the boundary size was covered by a sentence that does not cover it, and an
   erratum of ours called a hypothesis unused that this very proof needs (SCI-REV-0007;
   closed by the division's argument).  Four gaps of bookkeeping in §11.18 with it (an
   abort test after the call; a cost display with an undefined index and two missing
   terms; a missing case; an assembly over a dense set without a one-sided limit).  No
   exponent changes.

9. **A coverage requirement that depended on luck, and a pre-check that skipped the
   baseline** (this checkpoint's own new test XI.21).  The test demanded that among its
   random instances at least one has state-dependent shares and no constant shares.  In
   full mode there are eighteen; in quick mode, with the harness's seed, none — so the
   *unmutated* test failed in quick mode with "cases not exercised".  The coordinator's
   script for inspecting new mutants judged "caught" by the exit code and by the printed
   reason, and had run the baseline only with a seed of its own; all six mutants looked
   caught, for the right reasons.  The real runner checks the unmutated baseline in the
   same mode with the same seed (D55 item 12) and refused all eight mutations of the two
   selections concerned — the hole it was repaired for at the fourteenth checkpoint,
   re-opened in a private script.  Repaired: the decisive cases of the test are now its
   explicit instances (the two-site witness, the two-site counter-example), random ones
   are extra; the inspection script runs the baseline in both modes with the harness's
   seed first.  *Lesson:* a requirement "some random case exercises this clause" must be
   met by a constructed case; and a private copy of a check inherits none of the repairs
   of the original.

*What worked.*  Every one of these was found by a reader who re-derived or re-computed
with independent code *and varied something the author had held fixed* — the slope, the
domain, the bead count, the mean of the binomial.  Reviews that confirm every printed
number can still miss the sentence drawn from them (item 1 was missed by a referee who
replicated every digit).  From this checkpoint on a new section is not given a
qualitative headline until the bound of the opposite sign has been evaluated over the
stated range, and an extension "by inspection of the proof" lists the parts it extends.

## D60. A sketch stated as a theorem for randomised algorithms, a "necessary order" inherited from a sufficient count, and a correction that stopped one corollary short (nineteenth checkpoint of cycle 10; review SCI-REV-0013 of the Scientific Discovery Division; the Computational Research Division's checkpoint 4)

The review was requested by us (THY-RES-0010 §9.2) for the statements of the seventeenth
checkpoint.  It found two sentences false or wrong, both in parts we had labelled as a
sketch or as quoted from memory, and eleven smaller defects.  Each finding was verified
here before it was applied — by a derivation of our own and by new harness tests
(XI.22, XXIV.11) whose numbers agree with the reviewer's.

1. **Proposition 11.18e(b): "randomised algorithms without a hint need the Hamming ball
   as well" — false as written.**  The statement was `sup_g E|Q(g)| ≥ (1 − δ)N_ball − o(1)`
   for the task "a finite lower bound for the minimum, or a bracket of finite width for
   `ln Z`", justified by one sentence: under a Gaussian prior of large variance the target
   keeps a spread that grows with the variance.  *Counter-example (the division's):* a
   function of order below `m` is at least a fixed fraction `c` of its maximum on a fixed
   fraction `ρ` of the configurations, so `⌈ln(1/δ)/−ln(1 − ρ)⌉` uniformly random
   evaluations bound its maximum by `(largest observed value + C)/c + C` with probability
   `1 − δ` on every member — five evaluations at `δ = 0.05` on the cube at order two,
   whatever the number of sites, where the claim demanded `0.95(n + 1)`.  The core is
   machine-checked (`affine_half_large`, the division's, adopted).  *Why the sketch
   failed:* a spread that grows does not prevent a valid bound that scales with the
   observed values; validity is asked with probability `1 − δ` per instance, not a width.
   *What is true:* the count for deterministic algorithms (part (a), unchanged); for
   randomised ones on one site, instance by instance (a needle at an unevaluated state:
   new part (b′)(i)); for a prescribed width it is a conjecture.  *What we added while
   checking:* a Gaussian prior cannot prove the conjecture either — on one site with two
   states the average count under that prior is `2 − √(2δ)`, below `2(1 − δ)` — and a prior
   with widely separated coefficient scales, with a pairing of instances that share a
   transcript, gives an outline for `(1 − 2δ)N_ball` on the cube at order two (stated as an
   outline, not as a proof: this entry is the reason).
   *Lesson:* a lower bound "for randomised algorithms" is tested against the laziest
   randomised algorithm — uniformly random evaluations and an output that scales with
   what is seen — before it is written down; "the posterior stays spread" is not an
   impossibility argument unless the task asks for a width; and a statement about all
   algorithms that rests on a sketch carries **[C]**, not **[P-sketch]**.

2. **Proposition 11.113(d): "this order is necessary" — wrong by `e^Δ`.**  The count
   `ln(2/δ)(e^Δ − 1)²/(2ε²)` of part (c) is sufficient.  We called its order necessary
   "in the worst case over the box", citing from memory the classical lower bound for
   the mean of a bounded function.  That bound is in terms of the variance, and here
   the target is a *relative* accuracy of `1/(e^Δ − 1) + E W`: the worst mean is
   `1/(e^Δ + 1)`, not `½`, and there the variance is small.  The right order is
   `sinh²(Δ/2)/ε²`, and worst case against worst case a hint is worth `(1 − e^{−Δ})/ε`,
   not `(e^Δ − 1)/ε`.  No consequence at the width `0.06` of the instance for which the
   proposition was written; a factor 20 at width 3.  The necessity of the corrected
   order is now written out (a two-point argument with independent inclusion bits and
   Pinsker's inequality) and cross-checked against the exact number of bits at which
   the two binomial laws separate.  *Lesson:* a lower bound quoted for
   "the mean of a `[0, 1]`-valued function" concerns an absolute error at the worst mean;
   when the target is another function of the mean, the optimisation over the mean is
   redone before a count is called necessary.

3. **Corollary 11.114(d) kept the defect that had just been removed from its theorem.**
   One checkpoint earlier the lower bound of Theorem 11.110(e) had been completed by
   bumps (D58 item 1).  The corollary for ratios, derived from that theorem, still
   displayed the dip term alone, with the bumps in a parenthesis and no bump alternative
   in `BoxRatio.lean`; and three sentences elsewhere (report §8, §11.30, blueprint §6.4)
   still said that ratios are not covered, or that "the ceiling does not enter".  The
   division supplied the two missing lemmas machine-checked; the mixed lower bound is
   now `ratio_expected_queries_ge_mixed`.  *Lesson:* a correction is propagated by
   searching for the corrected formula and its consequences, not for the theorem's
   number; the list of places a correction "has reached" is made by grep, not from
   memory.

4. **Hypotheses lost between the Lean statement and the text; an attribution too
   short.**  Theorem 11.110(c) omitted `U, V > 0` — the case excluded is the floor
   itself, the subject of the correction; Corollary 11.114 stated a disjointness that
   two of its Lean statements do not use and omitted the positivity they do; Theorem
   11.115(d) needs at least one site; the bracket of Proposition 11.113(c) "never
   leaves the deterministic one" only after intersection; Theorem 11.18d credited the
   division with parts (a), (c) where (b) and (d) are its as well; "85 sets with three
   or four states" were all three-state sets; the `Θ` of the summary row lacked "for
   `ε ≲ 1`, where no single state is heavy, up to an additive constant".

5. **A threshold read off a grid chosen for other reasons** (the defect of the library's
   binomial sampler; THY-MSG-0015).  We had written "the defect begins near `n = 10¹⁵`".
   Our scan went from `10¹²` to `2⁵⁰` — a power of two, and powers of two up to `2⁵²` are
   clean — and then to `10¹⁵`.  Both other divisions found it lower; our second scan
   (`nested_review_R6/t5b_onset.py`, generic numbers of trials, three seeds) puts the
   onset between `2·10¹⁴` (clean) and `2.5·10¹⁴` (variance `0.2 %` too small at mean 92, `z`
   between `−6` and `−8`).  Our replacement sampler never hands the library more than
   `2³¹` trials and is not affected.  *Lesson:* a threshold is located by bisection on
   generic values; powers of two are not generic for a floating-point defect.

*What worked.*  The review we had asked for found what our own harness could not: the
tests of the seventeenth checkpoint checked the statements as written, and a false
"necessary" has no instance to fail on.  The reviewer wrote its code from the statements
before opening ours, and machine-checked the core of its counter-example.  From this
checkpoint on, a sentence of the form "no algorithm does better" is stated only with a
machine-checked or written-out proof, or with the label **[C]** or **[K]** and the source.

## D61. Three nested levels with servers chosen at the flat fibre: no certified gain — a design tuned on the benign instance (twentieth checkpoint of cycle 10; the Computational Research Division's ENG-RES-0014; the coordinator's follow-up)

*What was tried.*  Our referee R8 built three nested levels of Algorithm 2L⁺ by serving
every rung of the outer ladder with the cheaper of the base bracket (Proposition K0) and
a two-level run on the fibre — cheaper **at the flat fibre**, where both costs are exact.
The flat-instance figures (`ln(cost)/(na) = 0.453, 0.389` at `n = 4 000, 16 000`, `u = 1`, against
`0.552, 0.513` for two levels) went out in THY-MSG-0007 §3 as "the first evidence at large
`n` that a further level lowers the cost at a bounded accuracy".

*What the Computational Research Division found* (ENG-RES-0014; its evaluator first
reproduces the referee's 48 flat-instance numbers to the digit).  The flat instance is the
cheapest case twice over — for the outer loop and for every level above a base bracket.
On cone fibres the third level keeps `0.92–0.96` of the two-level cost, and **charged its
certified bound this design is not below two levels at any of the three sizes**
(`1.155, 0.726, 0.590` against a two-level bound `1.138, 0.726, 0.590`; at `n = 1 000` it is
*above* it).

*Why.*  A server that is cheap at the flat fibre can be certified far above the base
bracket it replaces.  At `n = 4 000`, outer fraction `0.40`, the rung of accuracy `9.8` is
served by a two-level run that costs `e^{0.223na}` at the flat fibre and is certified at
`e^{0.704na}`; the base bracket costs `e^{0.512na}` on every fibre.  Eleven such rungs (accuracies
`10` to `97`, the "extensive" middle design `λ = 1`, `η = ½`, `b = x/4`) are each certified above
the base bracket they replace, and the finest of them carry the certified bound of that
design.  The flat-instance advantage lives exactly in these rungs.

*What repaired it.*  Theorem 11.56's bound is nondecreasing in the cost bounds of the
inner procedures, so choosing every server **by certified cost** makes the certified
bound of three levels at most that of two — and it is then strictly below the two-level
*worst case found* from `n = 4 000` on (theory report §11.19, remark (1b);
`experiments/coordinator_checks/three_levels_certified/`).  (*Added at the twenty-second
checkpoint, after the Scientific Discovery Division's review SCI-REV-0016:* the rule was
re-derived and all 159 certified numbers were replicated; but five of the two-level worst
cases in that comparison were for another ladder — two designs that our texts describe
by the same words, "a geometric ladder of 40 rungs", had been treated as one — and the
two-level side is a mean-run model.  The comparison that
needs neither is with the exact cost of two levels at the flat instance, and there the
certified three-level bound is lower from `n = 16 000` on, not from `4 000`.)  The certified gain comes from
other rungs (the finest ones) and another middle design (the bounded-accuracy one) than
the flat-instance gain.

*The coordinator's own detour.*  The first draft of this checkpoint took the division's
certified column as a property of a third level, wrote "no size at which a certified third
level pays has been exhibited", extrapolated the gap (`0.109, 0.032, 0.015`) to a crossing
beyond `n = 16 000`, and drafted a request to the division to look for it at sizes up to
`10⁶`.  None of that was published: while the audit of the draft ran, the referee's own
routines — in this repository since the sixth checkpoint — answered the question in
minutes, and the crossing is between `n = 2 000` and `4 000`.

*Lessons.*  (1) A design is tuned for the quantity it will be charged: a server chosen on
the benign instance is not a server chosen for the certificate, and a table of costs at
the benign instance says nothing about which design has the better bound.  (2) "This
design gains nothing" is a statement about the design until the design space has been
looked at; before extrapolating a gap or asking another division for a computation, try
the obvious variation with the tools at hand.  (3) The flat-instance figures of
THY-MSG-0007 remain exact and remain best cases; the linked correction is in
THY-RES-0013 §2.

## D62. A hypothesis lost on adoption, numbers quoted from a draft, and summaries wider than their cells (twenty-first checkpoint of cycle 10; the Scientific Discovery Division's review SCI-REV-0014)

The review we had asked for (THY-RES-0011 §9(a): the rate of the level recursion) found the
rate right — and machine-checked it — and, reading how five of its earlier reviews had
been applied, one false proposition and twelve errors of record in our texts.

1. **A hypothesis lost on adoption (major).**  Proposition 11.117(b) — the small-slope
   law `F*(t) = (t(1−t)/2)u²V + O(u³)` — is the division's Proposition R10.1, which reads "`d₀`
   symmetric".  Our text adopted it "for every finite `(X, π)` and envelope `u·d₀`", in a
   section whose Setting allows envelopes that are not symmetric.  There it is false: on
   two points with `d₀(0,1) = 1`, `d₀(1,0) = 0` the class is a segment, and the coefficient is
   `V/4`.  The proof we repeated uses the two labels `±uf*`; `−f*` is a member only if the
   envelope is symmetric.  Harness XXV.3 could not see it: every instance it tested had a
   Hamming envelope.  *Lesson:* a statement adopted from another text is copied with its
   hypotheses and checked against the setting of the section it lands in; and a test of a
   statement "for every …" contains an instance outside each hypothesis the statement
   does not make (XXV.3 now carries the counter-example, with two mutations).
2. **An inequality stated for `p ≠ ½` that holds for `p < ½`** (11.117(c): `E_F > ln cosh(u/2)`;
   `E_F(0.7, 1) = 0.0540 < 0.1201`).  The conclusion survives by a gauge transformation; the
   proposition itself uses `p = 0.7` elsewhere.
3. **Numbers of a test quoted from a draft of the test** (harness XI.21: "153 … 135 … 154,
   one integrality gap", "8 of 100"; the stored output has `146 / 138 / 148`, two gaps, `10 of
   100`).  The stored output was regenerated when the test changed; the prose and a message
   (THY-RES-0011 §2) were not.  *Lesson:* a number of the harness in the prose is copied
   from the stored output of the audit that closes the checkpoint, after it.
4. **Grid values quoted as values** (`τ₂/a = 0.5006`, `h/a = 0.2627` at `u = 1`; the closed form
   gives `0.5004`, and `h/a = 0.262647`).  Our own later script printed `0.5004`; the workstream
   report had both.
5. **Summaries wider than their cells.**  "Two of the three exponents fall below the cube
   at `u ≥ 3`" — proved: `a_∞` for `p ≤ 0.3` from `u = 3`, `h_∞` for `p ≤ 0.2` at `u = 4, 6`; and "by the
   structure factor `(1−p)/p` to second order" — proved at a fixed length with the factor
   `Var(Σs_i)/n`, whose limit is the structure factor, proved for the limit from above and
   for the threshold exactly.  The proposition had the cells right; four summary
   sentences and one message (THY-RES-0011 §8) did not.
6. **A remark that used more than it listed.**  The rate remark said "it uses only the
   three inequalities"; it also uses monotonicity in the level and in the accuracy,
   `T₁ ≤ a`, `a > h` and two properties of `θ_hint` (all true and machine-checked on the cube);
   and "the gain per level increases with `d`" is true of its lower bound, the gain itself
   being a sawtooth.
7. Two of the errors were the division's own, inherited by us word for word (Theorem
   11.18a(c): "with one or two of them changed neither does"); it found them itself.

*What worked.*  Asking for the review; the division machine-checking what it reviewed
(`RateFull.lean`, adopted); checking its counter-example with a few lines of our own
before accepting it (both rows of its table to the digit).  *What did not:* our own
adoption checks in the eighteenth checkpoint compared numbers and attributions and did
not compare hypotheses.

## D63. A heuristic that counted the wrong levels, two designs under one name, and a lower bound quoted from a theorem that does not state it (twenty-second checkpoint of cycle 10; workstream Q and its referee R12; the Scientific Discovery Division's reviews SCI-REV-0015 and SCI-REV-0016)

1. **"Heuristically not better than `n^{3/4}`" — wrong.**  Theory report §11.19, remark (2),
   the last sentence of the rate remark after Theorem 11.53 ("the sub-exponential factors
   of a family with `k` nested levels would have to be bounded uniformly in `k`, and they
   are not"), §12, `K_REPORT.md` §7 and the brief of workstream Q all said that the `o(n)` of
   the adaptive cost at a bounded accuracy cannot be better than `n^{3/4}` by this method:
   `≈ 1/η` levels, each losing `e^{O(√n)}`.  The count of levels was right and the loss per
   level was not.  In the recursion whose rate is proved only one level per epoch is a
   bounded level (`O(ln(1/η))` of them, with summable `√`-losses); the others are run at an
   accuracy `x ≫ ln n` with a closure threshold `e^{x − O(1)}`, where the closing radius is
   `ρ_h·n_o` and the outer sample costs `e^{n_o h}` up to a polynomial factor (Lemma 11.55(d)).
   The result is `exp(n·h + O(√(n ln n)))` (Theorem 11.58a).  *How the heuristic survived
   four checkpoints:* nobody had written the finite-`n` form of one level at an extensive
   threshold; "each level loses `e^{O(√n)}`" was true of the one kind of level that had
   been computed (the bounded one of Proposition 11.57(b)) and was extended to all.
   *Lesson:* a heuristic about what "each level" loses is a statement about every kind of
   level in the schedule; before publishing a limit of a method, compute one instance of
   each kind.  The brief asked for `n^{3/4}` "or the precise step at which the proof
   fails"; the workstream answered a better question than it was asked.
2. **Two designs under one name** (SCI-REV-0016, M1).  Remark (1b) compared the certified
   three-level bound with "the worst instance found for the two-level algorithm of the
   same outer design" at five sizes.  At three of them the two-level numbers were the
   Computational Research Division's for the ladder of inner rates `ε*·0.85^i`
   (ENG-RES-0008), while the bound was for the referee's ladder `x₀(b/x₀)^{l/40}`
   (ENG-RES-0014): our texts call both "a geometric ladder of 40 rungs".  No number was
   wrong; the attribution was, and the margins `e^{82}, e^{377}, e^{702}` were differences
   between quantities of two designs.  It could have been caught from our own report:
   remark (1a) gives `ln C_max = 153.96` at `n = 1 400` for one ladder and the table of (1b)
   `0.9933·na = 154.28` for the other.  *Lesson:* a design is its parameters, not its
   description; a table that takes numbers from two messages states both designs in full
   and compares one common number first.
3. **A theorem set against a model.**  The same comparison set a certified bound (true in
   every run on every instance) against costs of *mean runs* on searched instances, and
   called the latter "at the level of expectations".  The Scientific Discovery Division
   supplied the comparison that needs neither: the exact, deterministic cost of two levels
   at the flat instance.  By that measure three levels are certified below two from
   `n = 16 000` on, not from `4 000` as we wrote.  The earlier claim is not refuted — at
   `4 000` and `8 000` it rests on the model — but it was stated as more than it was.
4. **The abort rule as worded proved `C_max + M̄`** (SCI-REV-0016, m1; R12, m2).  Theorem 11.56
   said "before every inner call"; the queries of new outer points were untested.  It
   had been corrected once already (referee R8, m1: before, not after, an inner call) —
   and corrected one step short.  It matters exactly where a run is charged its bound as
   an inner procedure, which is where remark (1b) and Theorem 11.58a use it.
5. **A lower bound quoted from a theorem that does not state it** (R12, m1).  The
   workstream's Theorem Q(c), and the first draft of Theorem 11.58a, had
   "`n·h − O(ln n) ≤ ln N` for `0 < δ < 1`, by Theorem 11.25(a),(d)".  Theorem 11.25(a) is a
   finite inequality that is void for `δ ≥ ½`; (d) gives an exponent.  The truth is better
   — `n·h − O(1)` for `δ < ½`, three lines from (a) — and was found by the referee, not by
   the coordinator's own reading of the report.
6. **Lemma 11.55(c) had dropped two hypotheses of the workstream lemma it quotes**
   (`θ ≤ 2e^{u(m₀+2)}`; the radius at least `p_u m/2` for the size of the ball), and carried
   "`O(√m)`" where an explicit bound with the leading constant `u` holds.  Harmless for
   exponents, which is why it went unnoticed; not harmless for an explicit error term.
7. **The first-order allocation rule published without its range** (SCI-REV-0015, m4, m5;
   SCI-RES-0017).  Proposition 11.18f(c) said "charge every constant to its least probable
   sub-pattern" and gave a formula that, read with ties, charges a shared constant to
   every tied site.  On the division's leucine helix the rule raised one end of the
   bracket from 3.2 to 8.6 nats.  The statement was labelled first order and was true as
   such; what was missing is where first order ends (a penalty above the free-energy cost
   of its site is paid nat for nat).  And the sampler bound of Proposition 11.113a had a
   factor two that the affine dependence on the inner mean removes.

*What worked.*  Commissioning the question that the heuristic was about, with the request
to find the step at which it fails; an independent referee told to break the answer, and
not to import its code (220 million checks, and the two findings — the lower bound, the
abort rule — that the coordinator's own line-by-line reading had passed over); asking the
other division to attack the certified third level rather than its arithmetic.  *What did
not:* the coordinator's reading of the workstream report accepted its quotation of the
lower bound without opening Theorem 11.25; and the coordinator integrated the referee's
report from a draft that lay in the repository while its last runs were going — the
final version corrected one condition (the lower bound is proved with the constant
`max{1, (ε + ln 2)/u}`, not `(ε + ln 2)/u`, at small sizes) and two numbers that had been
copied from it.  *Lesson:* a referee's report is integrated when the referee hands it
back, not when its file appears.

## D64. Lines of a majorant propagated one by one, single-line epochs with the best rates, and a tolerance guessed before it was computed (after the twenty-second checkpoint of cycle 10; the coordinator's analysis of the rate of the level recursion)

*Context.*  Theorem 11.53a: under one level of the recursion a line `B − σx` below `T`
stays below `T′` with the new slope `Σ_B(σ) = sup_e [B − (1−σ)θ_na(e)]/e` (Lemma L), and the
slope map has a saddle-node at `B = h`.  Three things that looked like consequences and
are not:

1. **"The same map propagates the lines of a convex majorant, so
   `τ′ ≤ sup_lines min(B, (1−s)a)`."**  False as soon as a line's new slope jumps over the
   window `[1 − B/a, 1]` in which a line can be dropped at accuracy zero.  Gaussian pair:
   `T_1 = θ_na ≤ (1 − x)_+`, lines `(B, s) = (s, s)`, first level `τ₂ = ½`; the map sends `(s, s)`
   to the slope `s(1−s)/(1−2s)`, the formula gives `τ₃ ≤ ⅓` — but `τ₃ ≥ 1/(2√2) = 0.3536`
   (from `T_2 ≥ θ_hint` and `T_2(0+) = ½`), and `τ₃ = 0.3559` on the grid.  What is true: for a
   *convex* majorant with slopes in `[−1, 0]` the level operator commutes with taking
   minorant lines (Sion's minimax theorem: the bracket is affine in the line and
   quasi-convex in the outer rate), but the supremum is over the **convex hull** of the
   lines, the new slopes have to be capped at one, and the concave hull of the new dual
   curve has to be taken: the lines with `s ∈ (0.382, ½)` jump beyond slope `1`, are capped,
   and the chord from the capped point to the regular lines crosses the dropping window
   at `0.357`.  Harness XVI.7 (a documented refutation); mutation XVI.6 M7 is the same
   error inside the duality check (31 of 120 random families need a genuine mixture of
   two lines).  The coordinator made this error in its first numerical comparison and
   found it because the "upper bound" came out below the grid value at `k = 3`.
2. **"With the outer rate of every slope step chosen freely, the epoch schedule of
   Theorem 11.58a has the rate `C/k²`."**  It has `C/k` (`experiments/coordinator_checks/level_rate/epochs.py`:
   `k²(B_k − h)` grows linearly in `k`, for the Gaussian pair and the cube at `u = ½, 1, 2`).
   A single line that starts flat after a drop does pass the bottleneck in
   `π√(2θ_hint″(0)h²/δ)` levels instead of `h/δ`, but the range on which it is a majorant is
   only `O(√δ)` at the bottleneck (before it, the range tends to the fixed point
   `e − θ_na(e) → 0` of `R ↦ Re/(θ_na(e) + R)` as the rate `e` tends to `h`), `O(δ^{3/2})` at the
   end, and the drop is proportional to the range: `δ^{3/2}` per epoch of `δ^{−1/2}` levels,
   again `dδ/dk ≈ −δ²`.  The `1/k²` law of the exact recursion comes from the lines with
   *all* intercepts in `(h, τ]` passing the bottleneck in parallel; a schedule needs
   several lines at once (a type that is a maximum of lines), not better rates for one.
3. **A tolerance written into a statement before the number was computed.**  The first
   version of harness XVI.6 claimed the Gaussian lower bound to be "within 1 per cent of
   `¼ + (π²/16)/(k + ½)²` from `k = 10` on"; it is `1.5` per cent above at `k = 10` (within `2`
   per cent from `10`, `0.5` per cent from `20`).  The harness refused the claim on its first
   run, which is what it is for.

*Process.*  The brief of the Lean task for these lemmas was first written to the path of
an existing brief of an earlier workstream with the same letter; the earlier file was
restored from the repository at once and the new brief renamed (`LD_brief.md`).  Before
naming a workstream, list the directory.

*What worked.*  Deriving the continuum limit first (a Hopf–Lax step, a similarity
solution through a folded saddle, a Kepler problem — three independent routes to the
same `2π²`) and only then looking for the discrete statement that can be proved; and
comparing every candidate bound with the grid recursion at small `k`, where an error of
this kind is large.

## D65. A hypothesis lost on adoption, again: "second-order classes below the Curie–Weiss coupling cost polynomially many evaluations" — FALSE unless the known part is additive  **[audit AA1: `experiments/audit/AA1/aa1_04_second_order_known_part.py`]**

Theorem 11.33(a) of the theory report was adopted from workstream D without its hypothesis
"`f` additive" — the failure mode of D62, item 1; found by the assumption audit
(`audit/AA1_REPORT.md`, Err-1).  Without it (a) is false: a known part that confines the ensemble
to a code (extended Golay code, `n = 24`, `w = 4`: `(1 − 2δ)·4096` evaluations at `ε < 10⁻³`;
Gilbert–Varshamov codes: exponentially many at every `w > 0`) or a pairwise one of ferromagnetic
blocks (`exp(Θ(n^{1/3}))` at `w = 4`) makes disjoint droplets sensitive.  Restored, with a remark
after the theorem.  *Lesson:* that of D62; statements adopted before it need the same check.
