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

