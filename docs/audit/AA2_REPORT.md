# Assumption audit AA2 — theory report §§11.16–11.32

*Adversarial reader AA2, 2026-11-26.  Brief: `docs/workstreams/AA_brief.md`; directive:
`docs/collaboration/messages/theory/THY-MSG-0016.md` §1, item 2.  The reader did not write any of
the theorems audited.  Nothing outside `docs/audit/AA2_REPORT.md` and `experiments/audit/AA2/`
was created or changed; `lake` and `scripts/audit_all.sh` were not run; Lean files were read,
not compiled.*

## 0. How to read this report

**Sources.**  Line numbers `L…` refer to `docs/THEORY_REPORT.md` and `README:…` to `README.md`
as committed in `7e6eb4c` and unchanged through `87ffea8` and `b2cf817`, the head when this audit
closed (12 251 and 668 lines; the only change to the theory report during the audit was the
insertion of eleven lines after line 12 000 in `7e6eb4c`, so every line number below that was
stable throughout).  The quotations of §A.4 and §A.6 were checked against these lines once more
at the end.  `D…` are entries of `docs/DEAD_ENDS.md`; `XIII.1`, `DEAD.24`, … are tests of
`experiments/falsify_conjectures.py`, whose stored run is `docs/falsification_output.txt`;
"log" is `docs/RESEARCH_LOG.md`, section "Resume here" (line 2 621 ff. at the same commits; it
moved by 18 lines during the audit, so the log is cited by content), which is the source
for "refereed / not refereed".  `S1`–`S8` are the scripts of this audit (§A.5, with commands
and stored outputs).

**Labels of the report** are quoted as they stand: [V] machine-checked, [P] paper proof, [K]
cited, [N] numerical, [C] conjecture.

**Categories of this audit** — written in braces so that they cannot be confused with the
labels above; one tag per classified assumption (two tags where an assumption plays two
parts, e.g. false in its exact form and replaceable asymptotically):

| tag | meaning |
|---|---|
| `{E}` | mathematically essential: without it the statement is false or has no meaning |
| `{P}` | needed only by the present proof (the step is named) |
| `{C}` | convenience (computational or expository); can be dropped or is redundant |
| `{Q}` | replaceable by a weaker quantitative condition (stated) |
| `{X}` | removal changes the computational complexity (from what to what) |
| `{F}` | removal makes the claimed result false (counterexample named or constructed) |
| `{?}` | not known |

**Shape of an entry.**  *Statement* (label, referee status) — *Setting* — *Assumptions* —
*Generalises / not covered* — *Computational reading* — *Overstatement check*.  For Theorems
11.52, 11.54, 11.56, 11.58 the cube-specific ingredients are recorded briefly and the detailed
table is left to workstream N (`docs/workstreams/N_brief.md`, item N6), as instructed; the
rate of the recursion is workstream R's and is not audited as a result.

**What was checked independently by this reader** (details in §A.5):

* 216 numbers quoted in §§11.16–11.32 were recomputed from the formulas printed in the report
  with own code (`S4`): **216 of 216 agree** to the digits printed — the cube constants, the
  rate constants, both lower-bound columns of the finite-`n` separation table, `τ₂`, `T^{(2)}(0)`
  and `θ₂*` at four slopes, the field table of §11.20, the slice table of §11.25, the alphabet
  crossings of Proposition 11.103, the box-class counts, the chain constants, the norms and both
  polytopes of §11.22.  No numerical error was found; what is wrong in the report is in
  sentences (§A.4, §A.6).
* Assumptions were attacked numerically (`S1` twice, `S2`, `S3`, `S6` twice, `S7`, `S8`) and by three
  arguments written out in the entries.  Five of the constructions are new counterexamples, two
  confirm counterexamples that the repository has with independent code, and one conjecture was
  attacked and survived (`S5`).

**Rows of the summary table §0.3 that fall in this part** (L87–L100) and where they are
audited:

| row of §0.3 (line) | entries |
|---|---|
| second-order and correlated uncertainty — the §11.17 half (L87) | 5–9 |
| algorithms without a hint on the cube (L88) | 1–4, 10–18 |
| a known part: a field (L89) | 19–26 |
| the common structure (L90) | 27 |
| chains in the thermodynamic limit (L91) | 28–35 |
| a known part with interactions, function of the type (L92) | 36–42 |
| rounds of adaptivity (L93) | 43–46 |
| slices (L94) | 47–50 |
| heteropolymer product landscapes (L95) | 51–57 |
| evaluations with local ensemble-averaged data (L96) | 58 |
| observable free energies (L97) | 59–62 |
| a one-body marginal oracle with a field (L98) | 63–65 |
| sup-norm (box) classes (L99) | 66–71 |
| a known part with interactions along the chain (L100) | 73–74 |
| (no row) barriers and traps, §11.31 | 72 |

§0.2 has no row in this part.

---

## 1. §11.16 — without a hint: Monte Carlo and non-adaptive algorithms

### Entry 1 — Lemma 11.43 (tail lemmas)  [(a) V; (b), (c) P + K]  (L4112–4138)

*Statement.*  (a) An admissible residual neither falls nor rises faster than the envelope, hence
`Σw ≤ Σmin(w,t) + tΣ_{x∈D}(e^{β dist(Dᶜ,x)} − 1)`, `D = {w > t}`.  (b) On the cube, if `∅ ≠ D ≠ X` and
`|D| ≤ |B(r)|`, the last sum is at most that of a ball: `E(w−t)₊ ≤ t(e^{Δ_r} − 1)`.  (c) If
`|{w ≥ t}| ≥ |B(k)|` then `2ⁿE min(w,t) ≥ t·T_n(k)`.  Refereed (R5) for (a), (b); (c) is the referee's
appendix, re-derived, "not refereed a second time" (L4108–4110).
*Setting.*  (a): any finite space, any envelope, also asymmetric.  (b), (c): `{0,1}ⁿ`, uniform
measure, Hamming envelope with one slope `u`.

*Assumptions.*
- finite space in (a) — `{C}`: sums; the pointwise inequalities need nothing (`weight_le_of_outside`).
- `D ≠ X`, i.e. `r ≤ n−1`, in (b) — `{F}`: with `D = X` the bound is false; this was the closure gap
  of Theorem 11.52 (D45 item 4; XV.3 mutation M3; R7: 2 940 false brackets of 2 940 runs).
- uniform reference measure in (b), (c) — `{F}` for "balls are extremal", `{Q}` for the lemma:
  **new, `S1` test A** — on `Q_4` with `Bernoulli(p)^{⊗4}` and all 65 534 subsets, the maximum of
  `Σ_{x∈D}π(x)(e^{u·dist(x,Dᶜ)} − 1)` over `π(D) ≤ π(`ball`)` exceeds the best Hamming ball by the
  factor `2.08` at `(p,u) = (0.2, 2)` (`1.42` at `(0.3, 4)`; exactly `1` at `p = ½`, the control) and the
  best "ball with type-dependent radii" by `1.12` at `(0.2, 1)`.  The valid replacement is Lemma
  11.62 (the tail function `Ξ₀` as a maximum over subsets) and, for exponents, Theorem 11.63.
  The report says this for the reference `H` (L6461–6463: `2.08` on `Q_4` at `p = 0.2`, `u = 4`); for the
  reference `ψ₀ = 0` it was not computed.
- one common slope (identical sites) in (b), (c) — `{F}` for "balls are extremal": **new, `S1`
  test B** — with site-dependent slopes on `Q_4` the maximiser at the size of a weighted-metric ball
  is not such a ball for 17 of 20 slope vectors; a sub-cube spanned by the cheap coordinates beats
  the best ball by up to `2.36` (e.g. slopes `(1.921, 1.468, 2.291, 0.521)`, `|D| = 4`: `23.3` against
  `11.0`).  So the Harper step has no verbatim analogue for heterogeneous sites; only the
  asymptotic statement for finitely many site types exists (Theorem 11.97(c)).
- Harper's vertex-isoperimetric theorem — `{P}`: cited [K]; the reduction is on paper, checked by R5
  for all subsets, `n ≤ 5`, and by `S1` (control) for `n = 4`.  Any valid upper bound of the tail
  function serves the algorithms (this is how §11.20 uses `Ξ̄_H`).
- two letters — `{P}`: larger alphabets go through types, not through an exact theorem (§11.26).

*Generalises.*  Lemma 11.62 (any reference instance, any measure); Theorems 11.63, 11.78(b),
11.97(c) (asymptotic tail functions: field, exchangeable, several site types); abstract tail
function: workstream N.  *Not covered:* an exact (every-`n`) tail function for any measure other
than the uniform one, for unequal slopes, for more than two letters; continuous spaces.
*Computational reading.*  Useful as it stands: `E_r(n)`, `T_n(k)` are sums of `n` terms; the lemma is
the only place in §§11.16–11.19 where a finite-`n` constant is exact.
*Overstatement.*  None in the lemma.

### Entry 2 — Theorem 11.44 (plain Monte Carlo on the whole class)  [P]  (L4140–4182)

*Statement.*  With `M` uniform points, `Â = M⁻¹Σw(X_i)` satisfies `A ≤ (1+Γ′_n(r))E min(w,t*)` and
two-sided deviation bounds for every member of the class; `e^{nθ_na(ε₁)+o(n)}` samples suffice at
extensive accuracy and `e^{na+O(√n)}` at every fixed accuracy.  The first version was refereed (R5)
and found void below accuracy `≈ 6.7` (D43 item 1); **the present form is not refereed** (log: "Not
refereed: the revised Theorem 11.44").
*Setting.*  Uniform cube, zero known part, class `L_u`, independent uniform samples, target `ln A`.

*Assumptions.*
- the sampling law is the Gibbs law of the known part, and that law is uniform — `{F}` beyond the
  uniform cube: with a field plain Monte Carlo from `π` has the exponent `max_s KL(π_s‖π)/n`, up to
  `2.9a` (Theorem 11.61; `0.4621` against `0.2836` at `θ = 1`, `u = 2`, recomputed in `S4`); the right
  sample is type-stratified or `Bernoulli(r*)`.
- one slope, two letters, uniform measure for the constants `Γ′_n` — `{P}`: through Lemma 11.43(b), (c).
- independent samples — `{P}`: Chernoff and Markov; any design with the same two tail bounds would do.
- exact evaluations — `{Q}`: if every value carries an error of at most `η`, then
  `Â_noisy ∈ [e^{−η}Â, e^{η}Â]` and the accuracy degrades by `η` (two lines; not in the report).
- extensive accuracy below `ln cosh(u/2)` or a fixed accuracy — `{C}`: both regimes are treated;
  above the threshold `O(1)` samples.
- failure probability through Markov's inequality (`δ₂`, `δ₃`) — `{P}`: the accuracy carries
  `ln(1/δ₂)`; a median-of-means step would remove it at bounded accuracy (not written).

*Generalises.*  Theorem 11.61(b) (type-stratified sample, a field), Proposition 11.61a (a product
sampler at bounded accuracy), Theorem 11.76(a) (every exchangeable known part), Theorems 11.95,
11.98(d) (site types).  *Not covered:* chains as known part (the stratified construction fails,
Proposition 11.117(e)); any non-symmetric measure.
*Computational reading.*  An exponent.  At `u = 1` the cost is `e^{0.1109n}`: `6·10⁴` at `n = 100`,
`e^{33}` at `n = 300`.  The report's own finite-`n` numbers: upper and lower bound `e^{0.134n}` and
`e^{0.109n}` at `n = 4000`, `ε = 1` (L4204), `0.0307` against `0.0293` at `n = 6400` (L4278; the lower one
recomputed in `S4`: `0.02933`, `ln = 187.7`).  Nothing is certified by it at a size where the
sample could be drawn.
*Overstatement.*  **The section title** (L4092) "Without a hint: Monte Carlo is exponent-optimal
among non-adaptive algorithms" has no restriction to the uniform cube; four sections later
"plain Monte Carlo from the Gibbs measure of the known part is exponentially worse"
(L6233).

### Entry 3 — Theorem 11.45 (non-adaptive algorithms)  [(a) V; (b) V given two finite sums; (c)–(e) P]  (L4184–4217)

*Statement.*  (a) Pairs of class members with targets more than `ε` apart whose difference sets
cover every point with weight at most `B` force `(1−2δ)Σv_j/B` evaluations of every randomised
non-adaptive algorithm.  (b) On the cube: `(1−2δ)2ⁿ/|B(R−1)|` if `ε < D_R` (cone against flattened
cone).  (c) Exponents `θ_na(ε₁)`, and `a` at fixed accuracy.  (d) An adaptive class-correct algorithm
costs `n + 3` on every cone.  (e) Pre-drawn points with adaptive stopping: the same exponent on
cones.  Refereed (R5).
*Setting.*  (a): any class, any functional (Lean: any predicate and any `Φ`).  (b)–(e): cube.

*Assumptions.*
- non-adaptivity in (a) — `{F}`: R5's Lean example `adaptive_escapes_packing` (four points, three
  pairs, two evaluations; `reviews/R5_referee_report.md` L493) and part (d) itself.
- `δ < ½` — `{Q}` at bounded accuracy, `{F}` as `δ → 1`: see the lemma in Entry 16 (a `K`-level
  version holds for every `δ < 1` at accuracy `Kε`), and **`S6`(i)**: for
  `δ ≥ 1 − 1/⌈nu/ε⌉` one evaluation suffices on the whole class.
- both members of every pair in the class and separated by more than `ε` — `{E}`.
- uniform measure in (b) — `{Q}`: with a field the pairs are cones truncated at type-dependent
  radii (Theorem 11.61(c)); with any symmetry group the pairs are `(ψ∘σ, ψ^{tr}∘σ)` (`GroupSampling.lean` [V]).
- "randomised" means a finite mixture of deterministic algorithms — `{C}` (§8, L1165).

*Generalises.*  `symmetric_nonadaptive_queries_ge`, `group_nonadaptive_queries_ge` [V] (any
permutation-invariant or group-invariant class); Theorem 11.98(d).  (a) is already as general as
it can be stated.  *Not covered:* a non-adaptive bound for chains (Proposition 11.117(e)).
*Computational reading.*  The only statement of §11.16 that is an explicit finite-`n` bound with a
machine-checked core: e.g. `ln LB = 110.90` at `n = 1000`, `u = 1`, accuracy `0.8715` (recomputed, `S4`).
*Overstatement.*  (c) "plain Monte Carlo attains it" is about exponents (said in the next
sentence).  Part (d) contradicts a bold sentence of §11.17: Entry 9.

### Entry 4 — Proposition 11.46 (a certified bracket from two independent samples)  [P]  (L4242–4264)

*Statement.*  The `⌈K⌉`-th largest weight of one sample as threshold, the truncated mean over a
second, the tail by Lemma 11.43(b): `Â/(3/2) ≤ A ≤ 2Â + t̂(e^{Δ_r̂} − 1)` outside probability `δ`, on
every instance; with doubling it is correct for every `ε > ln 3` and has the hinted cost at the
zero residual for `ε > 2`.  Statement read by R5; it is the base family of every nested algorithm.
*Assumptions.*  `ε > ln 3` — `{Q}` (constants `1 ± η` reach every accuracy at a factor `ε⁻²`; this is
Proposition 11.57(a)); uniform cube and one slope — `{P}` (Lemma 11.43); `r̂ ≤ n − 1` — `{F}` (Entry 1).
*Computational reading.*  A procedure one can run at small `n` (harness XIII.5); at the zero
residual it is the benchmark every nested design is compared with and loses to it below
`n ≈ 500` (L5722–5725).
*Overstatement.*  None.

## 2. §11.17 — correlated uncertainty: linear classes and profiles

### Entry 5 — Theorem 11.47 (classes that are linear in features)  [V; exactness K]  (L4315–4358)

*Statement.*  For `g = θ·F` with coefficients in a box: the pairwise envelope is a pulled-back
weighted `ℓ¹` distance; every linear combination of evaluations brackets `g(y)` by the unexplained
part of `F(y)`; `rank F` evaluations determine `g` everywhere; with a first-order remainder a
transport term is added.  Refereed (R6).
*Setting.*  Any set `X`, known features, exact evaluations.

*Assumptions.*
- the residual is linear in *known* features — `{E}` for the rank statement and `{X}`: the
  first-order class of the same envelope costs `2^{n(1−o(1))}` deterministic evaluations where the
  linear class costs `n` (L4360–4366).
- coefficients in a box — `{C}` for (c) (the span argument needs no bound); `{Q}` for (a), (b): any
  convex coefficient set gives its support function in place of `Σw_α|r_α|`.
- no remainder — `{Q}` for a sup-norm remainder `η` (accuracy floor `η(1+‖λ‖₁)`, workstream P
  Theorem 13), `{X}` for a first-order remainder (first-order prices return, L4505–4512).
- `Σλ_i = 1` in (d) — `{E}` (the remainder is defined up to a constant).
- symmetric envelope in the lower end of (d) — `{F}` as stated with the upper term ("with the term
  of the upper end the statement is false for asymmetric envelopes", L4352–4353); the transposed
  term is machine-checked.

*Generalises.*  Theorem 11.48 (profiles), Propositions 11.50, 11.50a.  *Not covered:* randomised
algorithms for linear classes (§12 item 9(c)); features known only approximately.
*Computational reading.*  The one polynomial statement of this part that needs no hint and no
sampler — but it counts evaluations: "a certificate for the minimum … whatever the size of `X`"
(L4341–4342) still has to minimise `f + g` over `X`, and the report says so 180 lines later
(L4520–4523).
*Overstatement.*  L4339–4342 as just quoted (mild: true of evaluations, silent on computation).

### Entry 6 — Theorem 11.48 (pair-additive residuals; the profile envelope)  [inequalities V on a grid of distances and for one pair type; attainment, transport form P; (d) V]  (L4368–4436)

*Statement.*  `g = Σ_{p<q}φ_τ(s_pq)` with `L`-Lipschitz radial functions vanishing beyond a cutoff is
linear in the cumulative pair-count profiles; the envelope is `L` times the `L¹` distance of
profiles (Wasserstein-1 between truncated multisets of squared distances); span brackets as in
Theorem 11.47; Debye scattering curves of one conformation are members.  Refereed (R6, R_P;
SCI-REV-0006).
*Assumptions.*
- pair-additivity — `{E}` for linearity; `{C}` for (b) read as an envelope (the first-order class
  of `d_P` needs none).
- Lipschitz in the *squared* distance — `{C}`: any radial coordinate works with its own transport
  cost; but terms steep at short range have no useful `L` and must sit in the known part (L4374–4375).
- the cutoff `S_c` — `{C}` (it creates the truncation fibres; without it the profile is complete).
- one pair type and a grid of distances in the Lean statements — `{P}`: general distances and
  several types are on paper (label of the theorem).
- one conformation in (d) — `{E}`: for an ensemble the intensity is a Boltzmann average, a
  different statement (L4432–4434).

*Generalises.*  Proposition 11.49; §11.22.  *Not covered:* many-body terms (profiles on triangles,
not written), chirality, anything that is not a function of pair-distance statistics; whether a
physical residual has a useful `L` ("an empirical question that this report does not address",
L4524–4525).
*Computational reading.*  The envelope has large fibres (802 075 walks, 541 profiles, L4389–4390):
cheap to cover because it cannot tell much apart.
*Overstatement.*  None found in the theorem; the section says "not to chains" itself (L4513–4514).

### Entry 7 — Proposition 11.49 (what the profile format costs)  [P; (c) V]  (L4438–4525)

*Statement.*  (a) At extensive accuracy the first-order class of `d_P` has certificates of size
`ln N_cov ≤ ln 4·|𝒯|·⌈4zLS_c/ε₁⌉`, independent of `N`.  (b) With `G` distinct distances the
pair-additive class is learned exactly from `|𝒯|G` evaluations.  (c) Sharpness is stochastic
dominance [V].  (d) At fixed accuracy the first-order class is `exp(O(N/ε))`.  Refereed (R6, R_P).
*Assumptions.*
- excluded volume: at most `zN/2` pairs within the cutoff — `{E}` for independence of `N` (phantom
  product domains are excluded by it, L4439–4440).
- extensive accuracy `ε₁N` — `{X}`: at a fixed accuracy the count is `exp(Θ(N/ε))` on spaces whose
  profiles vary freely (the lower bound is the referee's, "not re-derived by us", L4483–4484) and
  polynomial on a lattice.
- a lattice (finitely many distances) in (b) — `{X}`: on the rational torus `G` grows with `N`
  (`1, 1, 1, 2, 5, 14, 36`), off-lattice the reduced-basis bound `(8(1+κ)|𝒯|zLS_c/ε₁)²` replaces it.
- the remainder outside the class is bounded in sup norm — `{X}`: bounded only in a per-torsion
  first-order envelope, the exponential cost of D42 returns "for every fixed `η > 0`" (L4509–4510).
- zero residual and a purely torsional known part in every measured table — `{C}` (instances, not
  hypotheses).

*Computational reading.*  **(a) is vacuous by the report's own words**: it "evaluates to
`10^{93}`–`10^{2697}` at accuracies at which 8 to 7000 evaluations suffice" (L4455–4456), and "there is
no saturation at extensive accuracy at any size that can be enumerated" (L4631–4632).  What is
useful is relative: 8 evaluations against at least 136 200 at 15 beads (L4641).
*Overstatement.*  §10 row G19 (L1512) still lists "at extensive accuracy certificates in this
format exist whose size does not depend on the chain length" without the word vacuous; the
section and the README (README:223–231) carry the caveat.  Mild.

### Entry 8 — Proposition 11.50 (a kernel for residuals linear in pairwise features)  [V; not refereed]  (L4527–4548)

*Statement.*  A subdivision of the coefficient box with multipliers and a pairwise certificate per
leaf bounds `E₀ + θ·F` for every coefficient vector of the box consistent with the anchors.
*Assumptions.*  Nonnegative feature tables — `{P}` ("the first term uses `F ≥ 0`"; a shift of the
features restores it); rational box and anchors — `{C}`; features pairwise in the rotamer variables
— `{E}` for the reduction to the pairwise kernel.  It is weak duality "and no more" (L4544–4545):
no completeness, no size bound.
*Computational reading.*  A checker, tested on one worked example (`contactTriangle_bound`).
*Overstatement.*  **§0.3, L87**: the status cell "inequalities and kernel machine-checked; refereed
(R6, R_P)" covers a kernel that the section itself calls "not refereed" (L4313, L4527).

### Entry 9 — Proposition 11.50a (residuals in a Hilbert ball)  [V; attainment N]  (L4550–4583)

*Statement.*  For a positive semidefinite kernel and `‖g‖ ≤ B`, `(g(x) − s(x))² ≤ (‖g‖² − ‖s‖²)P_λ(x)²`;
a certificate `(γ, λ, r)` is checked without square roots.
*Assumptions.*  The norm bound `B` is known a priori — `{E}` (it plays the part of the envelope
constant; nothing certifies it); a positive semidefinite kernel — `{E}`; finite configuration space —
`{C}`; the optimal rule for attainment — `{C}` ([N]).
*Generalises.*  A different class, "not a weaker one" (L4583).  The division's design bounds
"were not checked by us" (L4572).
*Overstatement — the worst of this part.*  L4579–4583: "**no procedure that is correct on a
first-order class can be cheap on any of its subclasses — a cheaper paradigm necessarily gives up
correctness on the first-order class** (a corollary of the instance-wise lower bounds of §11.10 …:
they hold at every instance, in particular at the instances of a benign subclass)".  As written
this is **false, by Theorem 11.45(d) of the same report** (L4205–4211): the algorithm there "is
correct on the whole class and costs `n + 3` on every cone" — the cones are a subclass on which a
class-correct procedure is cheap.  The instance-wise lower bounds "hold at every instance" only
in the sense that every instance has its own bound, and at a cone that bound is two evaluations
("a cone costs two evaluations", L5135–5136).  What is true: a procedure that is cheap *at an
instance whose own lower bound is large* — the zero residual below the threshold, say — cannot
be correct on the first-order class, whatever subclass that instance is placed in.  The false
form is repeated in README:148–151.

## 3. §11.18 — adaptivity replaces the hint (extensive accuracy)

### Entry 10 — Theorem 11.51 (radial instances)  [P; workstream H]  (L4737–4767)

*Statement.*  On the class `R_u` of radial functions with unknown centre, non-adaptive algorithms
have the exponent `θ_na`, adaptive ones `θ_hint`, with the explicit cost
`(n+1)⌈ln(2n/δ)2ⁿ/C(n,r_ε)⌉ + 2n + 1`.  Not refereed separately (R7 "ran the radial algorithm on full
cubes").
*Assumptions.*
- the promise of radiality — `{E}` for the algorithm ("trusts the promise … is not an algorithm for
  `L_u`", L4764), `{X}`: without it the same exponent needs the nested algorithm, whose `o(n)` at
  extensive accuracy is unquantified (Entry 13).
- `4|B(n, r_ε−2)|/2ⁿ ≤ δ` (fixed `δ`, extensive accuracy, `n` large) — `{P}`: the second branch of the proof.
- uniform cube — `{P}` (shell counts).
*Generalises.*  It is the two-round upper bound on radial instances (Proposition 11.88(c)).
*Computational reading.*  The one adaptive algorithm of the part with an explicit polynomial
overhead over the hinted lower bound — for a promise class.
*Overstatement.*  None; the limitation is stated in the theorem.

### Entry 11 — Theorem 11.52 (one more level)  [P; core algebra V]  (L4781–4925)

*Statement.*  A family of bracket procedures with exponent function `T` yields one with `R[T]`
(11.18.2), by a two-level layer-cake algorithm.  Refereed (R7: "proved with gaps", written in;
SCI-REV-0007: four bookkeeping gaps closed, D59 item 8).  The count of evaluations — "the content
of the theorem" — is not machine-checked (L4721–4723).
*Cube-specific ingredients* (brief; the full table is workstream N's, item N6):
- product structure of the reference measure over the two blocks, hence fact (F2), `−ln W` is
  `u`-Lipschitz on the outer block (`fibre_sum_le` [V]) — `{F}` without it: for an interacting known
  part the constant is `u + osc φ′` and depends on the instance (L8093–8101; D49 item 6).
  Confirmed in one screen, **`S8`**: for a Curie–Weiss known part the member `γ|b| ± u|a|` of `L_u` has
  a fibre average that changes by `u(1 + c)` per outer flip, with `c = 0.3`–`0.6` in one phase away
  from criticality and for antiferromagnets (stable in `n`: a weakening of the slope — `{Q}`, the
  "bounded influence" of `N_brief.md` §2(d)), and `c` up to `26` with two phases (`βJ = 3`, `u = 0.2`,
  `n = 400`, growing with `n`: no constant of the order of `u`).
- additivity of the Hamming distance over blocks (a block of `φn` sites carries the same problem
  at size `φn`) — `{E}` for the gain: on Gaussian space with Euclidean Lipschitz functions the
  construction "gains nothing as it stands" (L5121–5125; the coordinator's computation in
  `N_brief.md` §2(c) is a sketch).
- Lemma 11.43(b) on the outer cube with `r ≤ n_o − 1` — `{F}` at `r = n_o` (Entry 1); `{Q}`: any upper
  bound of the tail function keeps validity (Theorem 11.64).
- atoms of mass `2^{−n_o}` (termination, `M ≤ 4K·2^{n_o}`) — `{P}`; with a field `1/min μ_H` replaces
  `2^{n_o}` and the inner failure probability must shrink (repair (M2), L6349–6354).
- bounded oscillation (a trivial bracket from one evaluation) — `{E}` for a start.
- the abort test *before* every query — `{F}` without it for "the cost bound holds always"
  (R7; SCI-REV-0007; L4827–4836).
- extensive accuracy (the bracket has accuracy `gn + O(log n)`) — `{P}`: removed by Theorem 11.56.
*Computational reading.*  None at finite size: an earlier variant at `n = 32` closed in 12 of 32
runs and "needed far more evaluations than plain Monte Carlo for a wider bracket" (L5089–5092).
*Overstatement.*  L4924–4925 "No product structure of `ψ` is used" is true of `ψ` and easily read as
more: the product structure of the *measure* is used, and is what fails first (above).

### Entry 12 — Theorem 11.53 (the recursion converges to the hinted exponent) and the rate remark  [V]  (L4927–5039)

*Statement.*  For a pair `(θ_na, θ_hint)` with the identity `θ_na(e + θ_hint(e)) = θ_hint(e)` the hinted
exponent is a fixed point and a lower barrier of `R`, every nonincreasing bounded `T ≤ R[T]` lies
below it, and `T_{k+1} = min(T_k, R[T_k])` converges to it; `τ_k − h ≤ c₁/(k + c₂)`.  Machine-checked,
abstractly (`HintPair`), for the cube, and for the recursion as defined in Lean; the rate by the
Scientific Discovery Division (`RateFull.lean`).
*Assumptions* (the fields of `HintPair`).
- the pair identity — `{F}` without it: with `R_0` in place of `R^max` under a field the recursion
  "falls 3 % of `a` below the lower bound after ten levels" (L6192–6193; D47 item 1).
- `e + θ_hint(e)` nondecreasing, `θ_na` continuous and bounded, `θ_hint(e) ≥ h − Le` — `{P}` (each is
  used once in the three choices of parameters; Theorem 11.79(d) shows the slope condition needs
  no convexity; all hold for every game function, Theorem 11.66).
- `T` nonincreasing and bounded — `{E}` for the statement about super-solutions.
*Generalises.*  Already general: Lean statements about an arbitrary pair; Theorem 11.66 supplies
the pair from any game function.
*Computational reading.*  The proved rate needs `⌈A(g)/η⌉` levels for the exponent `θ_hint + η`
(`c₁ = 6.4a` at `u = 1`); observed `(τ_k − h)/a ≈ 0.65/k²` [N], conjectured `2π²h²θ_hint″(0)/k²`
(workstream R, in progress).  A statement about exponent functions; it says nothing at finite `n`.
*Overstatement / error.*  None in the statement.  L4967–4970 is stale: see §A.6, item 1.

### Entry 13 — Theorem 11.54 (the adaptive exponent without a hint, extensive accuracy)  [P: 11.25(a), 11.44, 11.52, 11.53]  (L5041–5084)

*Statement.*  For `0 < ε₁ < ε*`, `0 < δ < ½`, the least worst-case number of evaluations of an adaptive
randomised algorithm without a hint that is correct on `L_u(Q_n)` is `exp(nθ_hint(ε₁) + o(n))`.
Refereed (R7, SCI-REV-0007).
*Assumptions.*
- uniform cube, one slope, two letters — `{P}` for the upper bound: relaxed to a field (Theorem
  11.64) and to site types and alphabets (Theorem 11.101) by separate asymptotic isoperimetric
  theorems.
- product reference measure — `{?}` for the *statement*, `{F}` for the *proof* (Entry 11): whether
  "adaptive = hinted" holds for any interacting known part is open (O4 of Conjecture 11.83).
- extensive accuracy — `{P}`: removed on the cube by Theorem 11.58; beyond the cube it remains.
- worst case over the class — `{E}` for "= the hinted exponent": instance by instance the question
  is open (L5134–5138).
- `δ < ½` in the lower bound — `{Q}` (Entry 16).
- exact evaluations — `{?}`: no statement with noisy or bounded-error evaluations exists for any
  nested algorithm.
*Computational reading.*  "**Nothing here is an algorithm one would run**" (L5100).  The two-level
algorithm overtakes the two-sample bracket "between `n = 2000` and `n = 5000` — where either needs
more than `e^{70}` evaluations" (L5102–5103).  The `o(n)` at extensive accuracies is unquantified
(L5038–5039, L5650–5653).
*Overstatement.*  The section title (L4706) and the slogan L5049–5050, "*At the exponential scale a
hint is worth nothing to an adaptive algorithm*" (again L5972–5973, README:240–241), are true
for the worst case over `L_u` on the uniform cube.  With a field the natural hint — the known
part itself, `g = 0` — is worth an exponent: `R^max(ε₁) > R_0(ε₁)` (Proposition 11.65(a), L6376–6379).

## 4. §11.19 — every bounded accuracy

### Entry 14 — Lemma 11.55 (where a bounded ratio can be certified)  [P; exact tables]  (L5231–5273)

*Statement.*  Bounds for the one-sided ratio `Γ̃(r) = E_r/|B(r−1)|` and the two-sided `Γ″(r)`; (c) the
closing radius at a bounded threshold is `p_u m − O(√m)`; (d) at an extensive threshold the loss
is the factor `(m+1)e^{2u+e^u}e^{me}`.  (d) refereed (R12); (a)–(c) by R8 on exact tables, `m ≤ 4000`.
*Assumptions.*  Pure statements about binomial sums: uniform cube, one slope — `{P}` (they are the
quantitative form of Entry 1); `0 < η ≤ ½`, `θ ≤ 2e^{u(m₀+2)}`, `s ≤ p_u m/2 − 1` in (c) — `{P}` (two of them had
been dropped and were restored, D63 item 6).
*Computational reading.*  Explicit and sharp to a few nats ("a slack of 5 to 18 nats at
`m = 64 000`", L5266–5267).  This lemma, not a theorem, is where "`e^{O(ln m)}` against `e^{O(√m)}`" comes from.
*Overstatement.*  None.

### Entry 15 — Theorem 11.56 (Algorithm 2L⁺: one level at the price of an arbitrarily small constant)  [P, refereed (R8); algebra V]  (L5280–5341, remarks to L5424)

*Statement.*  Algorithm 2L⁺ is a bracket procedure with accuracy
`ln[(2p_u)ⁿ + e^b(e^λ(1+η)/(1−η) + η′ + θ)]` and cost `C_max = 1 + 2M̄ + Σ_l min{2M̄, (J+1)cnt(x_{l−1})}C_l`,
in every run.
*Cube-specific ingredients beyond Entry 11* (the rest is workstream N's):
- the *lower* isoperimetric bound, Lemma 11.43(c), inside the algorithm (the Harper term) — `{P}`
  on the cube, `{?}` elsewhere: no lower tail function is available for any other measure in the
  report, so **no bounded-accuracy adaptive statement exists beyond the uniform cube** (L6505–6507).
- the binomial median (Lemma 11.55(b)) — `{P}`.
- the abort test before *every* query, inner calls counted with their bounds — `{F}` without it:
  "the previous wording … proves `C_max + M̄`, not `C_max`" (L5310–5313; corrected three times: R7,
  R8, SCI-REV-0016).
- `0 < λ ≤ 1` — `{P}` (used once, in the lowered sample cap, L5372–5373).
*Computational reading.*  A finite-`n` theorem with every constant explicit — and astronomically
large: remark (1a), Entry 18.  Simulated only with simulated inner oracles at large size, with
real inner brackets on `Q_12`–`Q_14`, three levels on `Q_9`, `Q_10` (L6065–6067).
*Overstatement.*  None in the theorem.

### Entry 16 — Proposition 11.57 and Theorem 11.58 (the adaptive exponent at every bounded accuracy)  [P, refereed (R8)]  (L5426–5481)

*Statement.*  For every fixed `ε > 0` (and `ε_n = o(n)` with `ln(1/ε_n) = o(n)`), `0 < δ < ½`: the least
number of evaluations of an adaptive algorithm without a hint on `L_u(Q_n)` is `exp(nh + o(n))`.
*Assumptions.*
- uniform cube — `{P}` for the upper bound and `{?}` beyond it (Entry 15).
- `ln(1/ε_n) = o(n)` — `{?}`: at `ε = e^{−λn}` the hinted exponents (rows 4–6 of Theorem 11.25(d)) are
  not known to be attained without a hint (L5679; §12 item 2(d)(iv)).
- `δ < ½` in the lower bound — `{Q}` at bounded accuracy, `{F}` as `δ → 1`.  **New (argument written
  out here; `S6`(i) for the last clause).**  *A `K`-level version of Theorem 11.25(a).*  Let `K ≥ 1` and
  let the deepest dip on a ball of radius `k` raise `ln A` by more than `(1+η)Kε`.  For every centre
  `s` and `i = 1..K` the scaled dips `τ_iψ^{B(s,k)}` are members of `L_u`, agree with `0` off `B(s,k)`,
  and have `ln A = v_i := (1+η)iε` for suitable `τ_i ∈ (0,1]` (the class is convex, `ln A` is continuous
  in `τ`).  A run on `τ_iψ^{B(s,k)}` coincides with the run on `0` until `B(s,k)` is hit, so
  `P₀(`hit `B(s,k)) ≥ 1 − δ − P₀(`out `∈ I_i)`, `I_i = [v_i ± ε/2]`; the intervals `I_0, …, I_K` are
  disjoint and `P₀(I_0) ≥ 1 − δ`, so some `i` has `P₀(I_i) ≤ δ/K`, the same for all `s`.  Summing over
  the `2ⁿ` centres: `E₀|Q| ≥ (1 − δ(1 + 1/K))·2ⁿ/|B(n,k)|`.  With `K > δ/(1−δ)` this is positive for
  **every `δ < 1`**, at the accuracy `Kε` in place of `ε`: at bounded accuracy the exponent `h` of the
  lower bound does not need `δ < ½`; at extensive accuracy the bound is `θ_hint(Kε₁)`, weaker, and
  the truth for `½ ≤ δ < 1` is `{?}`.  (The same count with `K + 1` flattenings of one cone inside
  one ball, which share a difference set, extends the non-adaptive bound of Theorem 11.45 to every
  `δ < 1` at bounded accuracy.)  And the restriction cannot go altogether: after one
  evaluation `ln A + ψ(x₀)` lies in an interval of length `nu`, so a random point of an `ε`-grid is
  correct with probability `1/⌈nu/ε⌉` — **one evaluation suffices for `δ ≥ 1 − 1/⌈nu/ε⌉`** (`S6`(i),
  exact enumeration on `Q_8`).
- the two ways of counting (distinct points below, with multiplicity above) — `{C}` (L5464–5471).
*Generalises.*  Nothing beyond the uniform cube: "Bounded accuracies with a field: only the lower
bound `a` for non-adaptive algorithms" (L6505–6507; Proposition 11.61a added the non-adaptive
upper bound).
*Computational reading.*  "The algorithm of the proof has about `ln(a/h)·a/η` bounded levels on top
of an extensive family: nothing one would run" (L5688–5689).
*Overstatement.*  The title (L5185) and L5670–5671 ("*The picture for the cube class, complete at the
exponential scale*") are accurate for the worst case over the class on the uniform cube and say so.

### Entry 17 — Theorem 11.58a (`n·h + O(√(n ln n))`)  [P, refereed (R12); epoch arithmetic V]  (L5483–5668)

*Statement.*  `ln N(n; ε, δ) ≤ nB_M + 𝓔_M` for an explicit schedule of `k_M` nested levels;
`limsup (ln N − nh)/√(n ln n) ≤ C_*(u)`; and `ln N ≥ nh − max{1,(ε+ln 2)/u}ln((1−ρ_h)/ρ_h) − ln(1/(1−2δ))`.
*Assumptions.*
- Theorem 11.56 at thresholds `e^{Θ(n)}`, ladders of `Θ(n)` rungs, depth `√(n/ln n)` — `{P}` and
  untested: "the statement of Theorem 11.56 covers all this; no simulation does, and none can"
  (L5660–5661); the log lists it under "not checked by anyone".
- bounded accuracy — `{P}`: "extensive accuracies … are not treated" (L5650–5653, a conjecture).
- `δ < ½` and `k*(ε) ≤ n/2` in (c) — `{Q}` (Entry 16).
- the order `√(n ln n)` — `{?}`: "an upper bound for this method" (L5634); with a rate `C/k²` for an
  explicit schedule it would be `O(n^{1/3}(ln n)^{2/3})` (conjecture; workstreams R, Q2).  **No lower
  bound above the hinted one is known** (L5649–5650): between `nh + ½ln n` [N] and `nh + O(√(n ln n))`
  nothing.
*Computational reading.*  The report is explicit that the guarantee is not usable: the bound is
below the non-adaptive `n·a` "from `n ≈ 2.1·10⁴` on" (L5615); "the smallest slope step exists at
`n = 187` … its certified bound there is `e^{142}`" (L5661–5662); at `u = 4` the formula "beats
enumeration only from `n ≈ 5.6·10⁴`" (L5518–5519); "**Not a competitive design at any size where it
can be evaluated**" (L5628).  `C(u, ε, δ)` of "for all `n ≥ 2`" is not explicit.  The constants `C_*`
were recomputed (`S4`: `4.65, 8.64, 13.5`).
*Overstatement.*  §0.3 (L88) states the result with its two ends and no caveat on usability;
the caveats are in the section.  Acceptable.

### Entry 18 — Remarks (1a), (1b): certified statements at finite `n`  [P + N]  (L5759–5954)

*Statement.*  (1a) At `n = 1400` (`u = 1`), `540` (`u = 2`), `4700` (`u = ½`) the cost bound `C_max` of
Algorithm 2L⁺ is below the non-adaptive lower bound of Theorem 11.45(b).  (1b) With every rung
served by the procedure of least certified cost, a third level never raises the certified bound,
and from `n = 16 000` on it is below the exact two-level cost at the flat instance.  (1b) reviewed
and replicated (SCI-REV-0016).
*Assumptions.*  One design, one ladder, `u ∈ {½, 1, 2}` — `{C}` (instances); Theorem 11.56 — `{P}` (the
"certificate" is a paper theorem evaluated numerically); the monotonicity of `C_max` in the `C_l` —
`{E}` for (1b) and elementary.
*Check.*  Both lower-bound columns of the table L5774–5780 were recomputed from the definitions
(`S4`): `110.90/31.69`, `149.02/42.02`, `155.02/43.49`, `176.48/55.08`, `141.54/38.97`, and `1767.6` at
`n = 16 000` — all ten agree.  The `ln C_max` column was not recomputed.
*Computational reading.*  The separation is real and useless: `C_max = e^{154}` (L5795).
*Overstatement.*  L5782–5784: "**the adaptive algorithm is certified cheaper — in every run, at every
instance — than every non-adaptive algorithm is in expectation**".  One side of the comparison
(`LB`) is machine-checked given two sums; the other (`C_max`) is the count of Theorem 11.56, a paper
proof whose accounting was wrong five times before (D45) and whose abort rule was corrected three
times.  In a programme whose "certified" elsewhere means machine-checked, "is proved on paper to
be cheaper" is the accurate verb.

## 5. §11.20 — a field as known part

*Common setting of Entries 19–26.*  `Q_n` with the reference `π = Bernoulli(p)^{⊗n}` (known part
`θ|x|`), class `L_u` (one slope), target `ln E_πe^{−ψ}`, extensive accuracy `ε₁n`.  Refereed (R9): no
critical finding.  "Of the algorithmic part nothing has been simulated end to end with a field"
(L6131–6132).

### Entry 19 — Theorem 11.59 (hinted exponents with a field)  [(a) refereed earlier; (b)–(d) P, refereed R9]  (L6157–6179)

*Statement.*  (a) Every algorithm makes at least `(1−2δ)e^{−tε+nF(γ,t)}` evaluations at the additive
instance `γ|x|`, for every `n`.  (b) A closed form of `F(γ,t)`.  (c) Max–min forms.  (d) For `p ≠ ½`
the hardest instance with a hint is additive and not the zero residual: `R^max > R_0` on `[0, E)`.
*Assumptions.*
- product reference with identical two-state sites and one slope in (b)–(d) — `{C}` for the closed
  form (the general object is the game function of Theorem 11.27(c) / 11.98), `{P}` for (d).
- additive instances in (a) — `{E}` for the product form of the bound; the general form for any
  measure is Theorem 11.116(c) [V].
- `p ≠ ½` in (d) — `{E}` (at `p = ½` equality).
- extensive accuracy and `o(n)` in "with a hint `exp(nR_γ(ε₁)+o(n))` suffice" — `{P}`.
*Check.*  The closed form was evaluated independently (`S4`): all five columns of the table
L6432–6438 (`R_0`, `R^max`, `γ*`, `a`, plain Monte Carlo) and the site `bin` of §11.26 agree.
*Computational reading.*  (a) is an explicit every-`n` bound; the rest are exponents.
*Overstatement.*  None in the theorem.

### Entry 20 — Lemma 11.60 (the shift identity with a field)  [V for a two-letter `S` and interior profiles]  (L6181–6193)

*Assumptions.*  Two-letter centre and interior profiles in Lean — `{P}` (boundary cases "by
continuity, on paper"); a product reference — `{E}` for the single-letter form; the reference
instance must be `H`, not `0` — `{F}` otherwise (D47 item 1).
*Generalises.*  The shear law of Theorem 11.66; for several site types the pair comes from the
game function, not from an identity of this kind.  *Overstatement.*  None.

### Entry 21 — Theorem 11.61 (non-adaptive algorithms with a field)  [(a) V; (b) lower bound V; rest P]  (L6195–6250)

*Statement.*  Type-wise quantile truncation stays in the class; the truncation function `ε_n^{tr}(q)`
bounds the non-adaptive complexity from both sides for every `n`; the exponent is
`θ_na = R^max∘S^{−1}`, attained by sampling uniformly on every type class; plain Monte Carlo from `π`
is exponentially worse.
*Assumptions.*
- the reference is uniform on type classes (exchangeable) — `{E}` for (a), (b) and all they need
  ("this part does not involve the reference measure at all", L6204); `{F}` beyond symmetry: for a
  Markov reference "the class-wise quantile truncation of an admissible residual is not
  admissible" (L11527–11534: 188 of 300 and 464 of 600 cases).
- a product measure — `{P}` for (c), (d) only (types; Theorem 11.63).
- the density of states `π(T_κ)` is known and uniform sampling inside a type class is free — `{X}`:
  here both are trivial; for a general order parameter they are the hard part (L8132–8136).
- `Mq ≳ log n` and an `O(1)` loss of accuracy — `{Q}` (explicit in Theorem 11.76(a): `ln(4/δ)`).
- extensive accuracy for the strict separation of product samplers from the flat histogram — `{E}`:
  "at vanishing accuracy it is false: there the two are equal" (L6235–6236); that
  `min_r max(φ₀,φ₁) > θ_na` for every `p ≠ ½` "is not proved in general" — `{?}` ([N], three examples).
*Computational reading.*  The lower half is an every-`n` bound; the upper half costs the factor of
Entry 36.
*Overstatement.*  None; the section itself corrects the first guess ("`π` is the right sampler", D47).

### Entry 22 — Proposition 11.61a (a product sampler is exponent-optimal at bounded accuracy)  [P; (i), (ii) V]  (L6252–6285)

*Statement.*  `exp(na + O(u√(n ln(1/(δε)))))` samples from `Bernoulli(r*)^{⊗n}` are `(ε/2, δ)`-correct on
the whole class, for every `n`.  The Scientific Discovery Division's; steps re-derived; (iii), (iv) on paper.
*Assumptions.*  Every conditional one-site law of every member lies in the window `[a₀, a₁]` —
`{E}` for the chain rule, and it is where the product reference and the single slope are used —
`{Q}`: with site-dependent windows the bound is `Σ_i max_b KL(a_b^{(i)}‖r_i*)` by the same chain rule
(not written; the division's version for general site classes "is not adopted", L6259–6260);
bounded accuracy — `{E}` for optimality (at extensive accuracies product samplers lose, [N]).
*Check.*  `r*` and `a` at four fields recomputed (`S4`).
*Computational reading.*  The only upper bound with a field that holds for every `n` with an
explicit `O(√n)` term; still `e^{na}`.
*Overstatement.*  None.

### Entry 23 — Lemma 11.62 (tail lemma relative to a reference instance)  [P; elementary]  (L6287–6296)

*Assumptions.*  The reference `ψ₀` is a member of the class — `{F}` otherwise ("its slack becomes
negative and the closure bound picks up exits that the class forbids", D47, last paragraph);
`q < 1` — `{F}` at `q = 1` (Entry 1).  Nothing else: the lemma holds on any finite space with any
reference measure.
*Computational reading.*  `Ξ₀(q)` is "a finite maximum over subsets for which no closed form is
claimed" (L6295–6296): `{X}` — an algorithm that uses it is an algorithm in the query sense only.
`S1` test A computes it exhaustively on `Q_4` for `ψ₀ = 0`.

### Entry 24 — Theorem 11.63 (asymptotic isoperimetry for the flat-histogram reference)  [P; new; refereed R9: proved]  (L6298–6330)

*Statement.*  `Σ_{x∈D}μ_H(x)e^{s_H(x→Dᶜ)} ≥ e^{ne} ⟹ μ_H(D) ≥ exp(−n[R^max(e − ω_n) + ω_n])`, with `ω_n → 0`
depending on `(p, u)` only.
*Assumptions.*
- a fixed product measure with identical two-letter sites — `{P}` (method of types; relaxed to
  exchangeable references in Theorem 11.78(b) and to site types in Theorem 11.97(c)).
- the reference is `H` — `{E}`: with the reference `0` the isoperimetry of the fixed product measure
  "gives the worse exponents" (D47 item 4).
- the error term `ω_n` — `{Q}`, and this is the weak point: "a leading term `2n^{−1/8}`" beyond
  `n₀(p,u)`, "below it the trivial `ω_n = u`" (L6307–6309).
*Computational reading.*  **Vacuous as a finite-`n` statement.**  `2n^{−1/8}` is below the exponent it
perturbs only for `n ≥ (2/R)^8`: `n ≥ 10^{11}` for `R^max = 0.084` (`θ = 1`, `u = 2`) and
`n ≥ 1.7·10^{15}` for `R^max = 0.025` (`p = 0.3`, `u = 1`) (`S4`, block H, and the same arithmetic).
Numerically the least admissible `ω` is `≤ 0.5 ln n/n` on the families tried; "not tested by
anyone: … sets without any symmetry for `n > 6`" (L6553–6554).
*Overstatement.*  None in the theorem; see Entry 25.

### Entry 25 — Theorem 11.64 (adaptive algorithms without a hint, with a field)  [P; lower bound every `n`; upper bound after repairs (M1), (M2)]  (L6332–6371)

*Statement.*  The worst-case cost is `exp(nR^max(ε₁) + o(n))` for `0 < ε₁ < E`, `0 < δ < ½`.
*Assumptions.*
- a product reference — `{F}` for the proof (fibre averages relative to the reference; Entry 11),
  `{?}` for the statement with interactions (O4).
- extensive accuracy — `{?}`: no bounded-accuracy statement with a field (L6505–6507).
- the numbers `Ξ_H(q)` or an upper bound of them — `{X}`: "an algorithm in the query-complexity
  sense only … for which no formula is known"; the explicit bound has "the useless rate `n^{−1/8}`"
  (L6454–6458).
- inner failure probability `δe^{−c₁n}/(2⁶n⁴)` for strong fields — `{F}` without it (repair (M2)).
- left limits in the level induction — `{P}` (repair (M1)).
*Computational reading.*  Never simulated end to end; inherits Entry 24.
*Overstatement.*  (i) **L6105–6107**: "**Everything carries over with one change that matters**".
Not everything: no bounded-accuracy adaptive theorem (Theorem 11.58), no sub-exponential term
(Theorem 11.58a), no exact tail function (only Theorem 11.63 with `n^{−1/8}`), no statement on
rounds ("the same questions with a known part", open (4), L8542), no simulation.
(ii) **L6370–6371**: "'adaptive = hinted' persists with a known part" — with a *field*; for known
parts with interactions it is open (L7553–7556).

### Entry 26 — Proposition 11.65 (instance-optimality; a field always helps)  [P; refereed R9]  (L6373–6427)

*Statement.*  (a) `R^max > R_0` for `θ ≠ 0`.  (b) `θ ↦ F*(t;θ)` is even and strictly decreasing on
`[0, ∞)`: every exponent is nonincreasing in `|θ|`.  (c) The type-stratified two-sample bracket is
instance-optimal at symmetric instances up to a polynomial factor.
*Assumptions.*
- two letters in (b) — `{F}`: for three letters a field can make certification harder (Proposition
  11.103(d): `E = 0.120196` for `(0.05, 0.5, 0.45)` against `0.119499` uniform; DEAD.24; the uniform
  values recomputed in `S4`).
- "the uniform cube is the hardest case" as a statement about exponents — `{P}`: "conditional on
  Theorems 11.61 and 11.64" (L6375–6376).
- symmetric instances in (c) — `{?}` beyond ("instance-optimality at non-symmetric instances is open").
*Overstatement.*  README:291–292 "A field always helps: every exponent decreases with the strength
of the field" has no "two letters"; the restriction is made 150 lines later (README:443–444).  Mild.

## 6. §11.21 — the shear law and game functions

### Entry 27 — Theorem 11.66 (every game function yields a pair)  [V]  (L6604–6651)

*Statement.*  For a continuous `F` on `[0,1]` with `F(0) = F(1) = 0`, `F(t) ≤ L(1−t)`, `F(t) ≤ Et`,
`E = sup F(t)/t > 0`: `R(e) = max_t[F(t) − te]` and `θ_na = R∘S^{−1}` form a `HintPair`, `R` is a fixed
point and lower barrier of the level operator, and the exact recursion converges to `R`.
*Assumptions.*  All four are mild and the theorem is **already general** (Lean, arbitrary `F`; no
concavity — `GameFunction.pair` has none among its hypotheses, L9449–9450):
`F(1) = 0` and `F ≤ L(1−t)` — `{E}` for a finite non-adaptive exponent `a`; `E > 0` — `{E}` (otherwise
nothing to prove); continuity — `{P}`.
*What the theorem does not contain* — and the report says so (L6625–6631, L6640): that a given
problem has exponents of this form.  The paragraph "*What a problem must supply*" (L6640–6651)
ends "Then non-adaptive algorithms have the exponent `R∘S^{−1}` and adaptive ones `R`": an
implication from (I1)–(I3) that is proved in three models and **not in the abstract** (it is the
commission of workstream N).  `{?}` for the abstract form.
*Computational reading.*  Convex analysis; no finite-`n` content.
*Overstatement.*  **§0.3, L90**: the row "the shear law; every game function yields a pair, and the
level recursion converges" has the status "machine-checked".  Machine-checked is the theorem
about functions; the shear law as a statement about algorithms ("a non-adaptive algorithm
certifies an accuracy rate that is worse by exactly `θ`", L6582–6583, valid for budgets
`N ≤ e^{nh}` and in the worst case) is the paper Theorems 11.44, 11.45, 11.54, 11.61, 11.64.  §10
row G23 (L1516) has the distinction; the summary row and README:303–308 do not.

## 7. §11.22 — limit shapes of profile sets

*Common setting of Entries 28–35.*  One synthetic model: self-avoiding walks on the diamond
lattice, cutoff `S_c = 12` (three distances below it), the profile `(h₃, h₈, h₁₁)` and the gauche
count `g`; the covering problem is the *deterministic* certificate size for the *minimum* at the
*zero residual* with the made-up known part `e·g(x)`, `L = e = 1` (L6733–6736).  Reviewed
(SCI-REV-0002, -0009, -0011): "no statement labelled as proved was found false".  Machine-checked:
the two abstract theorems; "not machine-checked: everything about the lattice" (L6717–6718).

### Entry 28 — Lemmas 11.67, 11.68 (site-set reduction; concatenation of bridges)  [P; exhaustive checks]  (L6741–6792)

*Assumptions.*  The diamond lattice and the cutoff 12 — `{P}`: every constant (`β = 60`, `β′ = 28`,
the height argument "sites whose heights differ by 4 or more are farther apart than the
cutoff") is specific; another lattice or cutoff needs its own lemma — `{?}` whether one exists in
general.  Bridges (first bead strictly lowest, last highest) — `{E}` for concatenation without
interference; for walks see Entry 35.
*Check.*  The norms of the error vectors were recomputed (`S4`: `60`, `28`, `36`, `44`, `16`, `108`, `168`).
*Computational reading.*  Exact, finite, verified exhaustively up to 14 beads by three parties.

### Entry 29 — Theorem 11.69 (a limit shape for bridges)  [abstract part V; lattice part P]  (L6794–6851)

*Statement.*  The normalised sets `{(h, g)/N}` of bridges converge in the Hausdorff metric to a
compact convex `K^{br}`, and every point of the finite set is within `168/(N+3)` (later `108/(N+3)`)
of it.  Abstractly: (C) approximate super-additivity with error `β`, (E) extension by one with
error `β′`, (B) `|q| ≤ RM`.
*Assumptions.*
- (C) — `{E}`: it is the content.
- (B) — `{E}` for a compact limit.
- (E) — `{C}`, **redundant (new, an argument)**: if `Q_1 ≠ ∅`, then for `q ∈ Q_M` and any `q₂ ∈ Q_1`
  hypothesis (C) gives `q′ ∈ Q_{M+1}` with `|q′ − q − q₂| ≤ β`, and `|q₂| ≤ R` by (B); so (E) holds with
  `β′ := β + R`.  In `SetLimit.lean` the field `succ` of `SuperAdditive` is implied by `add`, `bound`
  and the non-emptiness that `hausdorff_limit` assumes anyway (`add` is quantified over all
  `M₁, M₂`, L184 of the file).  The separate `β′ = 28` only improves a constant.  In the lattice
  application the content of (E) reappears inside (C) for small `M₁` (the bookkeeping paragraph,
  L6821–6831).
- real error terms instead of an exact semigroup — `{C}` since Proposition 11.69b: bridges with
  clean ends form an exact semigroup, and the limit is a classical Newton–Okounkov body.
*Generalises.*  The abstract theorem is general (any normed space `W` in Lean).  *Not covered:*
unrestricted walks (Conjecture 11.75), rings ("a sketch"), any off-lattice chain ("Off-lattice
nothing of this is proved", L7442).
*Computational reading.*  The one-sided rate is explicit and small (`108/(N+3)`); how fast the
finite sets fill the body is another matter (Entries 30, 34).
*Overstatement.*  The section title (L6655) "Chains in the thermodynamic limit: a limit shape for
profile sets, and the limit of certificate sizes" — one lattice, bridges, the zero residual, and
a limit of certificate sizes that exists only off an unidentified countable set; the summary row
(L91) and the README (README:317–327) are careful, the title is not.

### Entry 30 — Propositions 11.69a, 11.69b (interior rate; the exact semigroup)  [P; 11.69b (f), (g) read only]  (L6852–7088)

*Assumptions.*  An interior point with `d + 1` points of one level around it — `{E}` for the rate
`M^{−1/2}`; `m₀(p)`, and `M₀` in 11.69b(f), "not effective" — `{?}` for any explicit threshold (the
elementary estimate has a constant `≥ 3 132`, recomputed in `S4`); clean ends — `{C}` (every bridge
is cleaned by a head of two and a tail of three beads, verified on `1.6·10⁸` pairs).
*Computational reading.*  Rates without thresholds; (g) "at 24 beads the count is a ninth of its
asymptote" (L6962–6963).

### Entry 31 — Lemma 11.70 (covering numbers are stable under Hausdorff convergence)  [(a), (b), example V; (c), (d) P]  (L7090–7115)

*Assumptions.*  The accuracy is not a jump of the limiting covering number — `{F}` at a jump: the
two-point example `F_N = {(0,0), (1+1/N, 0)}`, `ε = L`, machine-checked (`not_hasCover_shifted`).
Internal centres — `{C}` (they fix the constant `2L + e`; with free centres `L + e` would do).
Compactness and a finite-dimensional normed space — `{E}` for finiteness of `N(F, ε)`.
*Computational reading.*  Exact and elementary.

### Entry 32 — Theorem 11.71 (the limit of certificate sizes)  [(a) V in abstract form given Lemma 11.68; rest P, numbers computer-assisted]  (L7117–7196)

*Statement.*  For bridges the certificate sizes converge to `N_∞(ε₁)` off the jumps of `N_∞`; for all
walks every limit point at `(L, ε₁) = (1, ½)` lies between 116 and 3 627, and the size is at most
26 437 at every length.
*Assumptions.*
- bridges in (a) — `{?}` for walks (Conjecture 11.75).
- a non-exceptional accuracy — `{F}` at a jump (Entry 31), and "**no accuracy is known to be
  non-exceptional, in particular not `ε₁ = ½` or `¼`**" (L7127–7128): at the two accuracies of the
  table only the two-sided inequality is proved.
- the zero residual, the known part `e·g`, deterministic certificates of the minimum — `{C}`
  (the instance; nothing is said about `ln Z` or about randomised algorithms).
- the norm of *cumulative* profiles — `{E}` for the numbers (D48: 8 against 10 at 15 beads with
  the wrong norm).
*Check.*  Both polytopes of Proposition 11.72 were recomputed from their inequalities (`S4`):
`vol 𝒦₁ = 3.2269`, 12 vertices; `vol 𝒦₂ = 3.125`, the 12 listed vertices exactly.
*Computational reading.*  The proved bracket has a factor 31 between its ends; "the value at 27
beads (15) [is] a factor of more than 7 below every limit point" (L7188–7189); the limit is
approached at "`10³`–`10⁵` beads or more" [N], and "no theorem bounds that length from above or
from below" (L6680–6681).  For the question that was asked — when is the plateau reached —
the answer is: not at any size that can be enumerated, and not provably at any size.
*Overstatement.*  Corrected by SCI-REV-0002 (the "plateau … is real" sentence is withdrawn,
L7193–7196).  None left in the theorem.

### Entry 33 — Proposition 11.72 (outer bounds for every walk, inner points from bridges)  [P; exact certificates]  (L7198–7307)

*Assumptions.*  The eight-site cluster of the diamond lattice — `{P}` (cluster method); the routing
sketch for periodic systems — `{?}`: with it `vol 𝒦 ≈ 2.2`, without it `1.6313 ≤ vol 𝒦 ≤ 3.125`; "seven
vertices of `𝒦₂` are not attained by any chain system with at most 12 sites per cell" (L7303–7304).
*Computational reading.*  Proved volume known to a factor `1.9`.

### Entry 34 — Propositions 11.73, 11.74 (surface law; single-flip constants)  [P]  (L7309–7388)

*Assumptions.*  Loomis–Whitney on the lattice — `{P}`; Bezdek's theorem for the better constant —
[K], "not read by us" (L7327–7328); the scaling form `c_j ≈ nΦ(d_j/n)` — `{?}` ([C], "not visible at
these sizes", L7384).
*Check.*  The constants `17.6`, `24.1`, `29.4`, the thresholds `43 512`, `3.4·10⁵`, `1.1·10⁵` and the
fractions `47 / 730 / 5 800` beads were recomputed (`S4`).
*Computational reading.*  The useful negative statement of the section: for all chains shorter
than about `4·10⁴` beads the finite profile set misses part of the limit body by more than one
covering radius, so "**enumeration cannot see the limit**" (L7354–7355).

### Entry 35 — Conjecture 11.75 (walks have the same limit shape)  [C]  (L7390–7431)

Every statement of the section about *chains* — as opposed to bridges — beyond the bracket of
Entry 32 rests on it: `{?}`.  What is proved: `K^{br} ⊂ liminf 𝒟_N`; the equivalence with a
ground-state statement; and that local surgery cannot prove it (a double strand; D48 item 2).
"No counterexample is known"; the evidence at 11–23 beads "has little power against the
mechanism" (L7422–7423).

## 8. §11.23 — known parts that are functions of the type (mean-field)

*Common setting of Entries 36–42.*  `Q_n`, Hamming class `L_u`, an *exchangeable* reference
`π(x) = p_{|x|}/C(n,|x|)`, extensive accuracy; refereed (R10): no critical finding, two major
(Proposition 11.81(b) false as first stated; an interval with an unproved end).

### Entry 36 — Theorem 11.76 and the remark on an arbitrary symmetry group  [(a) lower bound and truncation V, upper P; (b) V; (c), (d) P]  (L7630–7707)

*Statement.*  (a) If `ε < ε_n^{tr}(q)`, every non-adaptive algorithm needs `(1−2δ)/q` evaluations; the
type-stratified sample with `⌈8ln(2(n+1)/δ)/q⌉` points per class is correct for
`ε ≥ ε_n^{tr}(q) + ln(4/δ)`.  (b) Every algorithm needs `(1−2δ)/maxdens(D)` at a symmetric instance.
(c) The flat-histogram instance is the hardest symmetric instance up to `n + 1`.  (d)
Instance-optimality at symmetric instances.  The same for any finite group acting by isometries
that preserve `π`.
*Assumptions.*
- invariance of `π` and of the envelope under a group with few orbits — `{E}`; `{F}` without
  symmetry (Markov classes, L11527–11534); and **empty when the orbits are exponentially many**
  (L7705–7707).  `S7` tabulates it: for 20 site types of three letters the factor
  `8N_orb ln(2N_orb/δ)/(1−2δ)` exceeds the cost `e^{0.25n}` it multiplies up to `n = 300`; for one
  type per site it is the cost of enumeration.
- the accuracy offset `ln(4/δ)` (`4.4` nats at `δ = 0.05`) — `{Q}`: below it (a) claims nothing; at
  bounded accuracy only Proposition 11.61a (a field) has an upper bound.
- `p_t > 0` known and free uniform sampling in every type class — `{X}` (computation; trivial for
  functions of the type, the whole difficulty for a general order parameter, L8132–8136).
- symmetric instances in (b)–(d) — `{?}`: that `H` is the hardest of *all* instances is O4.
- `randomised = finite mixture` — `{C}`.
*Generalises.*  `GroupSampling.lean` is already general (any finite group, asymmetric envelopes).
*Computational reading.*  For the cube at `u = 1` the factor exceeds the cost `e^{na}` it multiplies
for `n ≤ 50` and is still `e^{9.7} ≈ 1.6·10⁴` at `n = 200`, where the cost is `e^{22}` (`S7`).
*Overstatement.*  (i) L7531–7535: "**Symmetry alone settles the non-adaptive problem**" — it settles
the optimal *sample*, up to the factor above; the *exponent* is open without convexity (O3, O5;
`[0.00184, 0.00338]` at `u = 0.30`).  (ii) §0.3, L92 and L95: "flat-histogram sampling is optimal
non-adaptively", "joint-type-stratified sampling is optimal among fixed samples for every `n`" —
both without "up to a polynomial factor in the cost and `ln(4/δ)` in the accuracy", which §10
(G25, G28) and the theorem have.

### Entry 37 — Lemma 11.77 and Theorem 11.78 (the single-letter theorem for every rate function)  [P; (a) every `n`; (b) by types; refereed R10]  (L7709–7778)

*Statement.*  The cost of every algorithm at a symmetric instance has the exponent `R_λ(ε₁)`, a
supremum over block profiles of a finite-dimensional minimum; isoperimetry for the type-uniform
measure with `ω_n → 0`.
*Assumptions.*  Exchangeable reference — `{E}` (Step 2 uses that `Bernoulli(k/n)^{⊗n}` is uniform on
`T_k`, "as `π` is"); `φ` continuous — `{Q}` (Lipschitz gives `O(ln n/n)`, a modulus of continuity
`o(1)`); continuity points of `R_λ` for the hinted upper bound — `{P}`; two letters — `{P}` (Theorem 11.97
for alphabets); `ω_n` from the typical-subset lemma — `{Q}`, poor (as Entry 24).
*Computational reading.*  "Single-letter" means independent of `n`, **not computable**: the
supremum runs over all finite block structures, whether finitely many block types attain it is
open (O2), and with two phases its value is known only from searches (Entry 41).
*Overstatement.*  §12, L11689–11691: "§11.23 settles the non-adaptive problem and the hinted
exponent of symmetric instances for every rate function" — characterises, not settles: for a
non-convex rate function neither number is known (`0.0251012 ≤ R_H(0⁺) ≤ 0.0291391`).

### Entry 38 — Theorem 11.79 (non-adaptive algorithms: cones around shells)  [P]  (L7780–7831)

*Assumptions.*  Self-consistent shells — `{E}` for the lower bound to be good; strict monotonicity
of the shear and the witness condition — `{?}` without convexity ("neither is automatic", L7806);
the full supremum `R_H` in the upper bound — `{E}`: a lower bound of `R_H` gives no upper bound of
`θ_na` (D53 item 2).  No unimodality, no convexity for (a), (d).
*Computational reading.*  Brackets: at `u = 0.30` the non-adaptive exponent is in `[0.00184, 0.00338]`.

### Entry 39 — Theorem 11.80 (a convex rate function)  [P; (d) "=" numerical]  (L7833–7890)

*Statement.*  For convex `I`: `R_H = sup_γ R_γ`, binary centres suffice, there is a game function,
`θ_na = R̄_H∘S̄^{−1}`.
*Assumptions.*  Convexity of the rate function (one phase) — `{F}` without it, three times: binary
centres do not suffice (DEAD.19: `0.016155` against `0.015277` at `e = 0.02`); the hardest additive
instance has 35 % of the exponent of `H` (Proposition 11.82(d)); the cone formulas miss by a
factor of more than two (DEAD.20).  The equality in (d) — `{?}` ("`=`" numerical in 24 cases).
*What fails* (stated, L7876–7878): the closed form, the every-`n` product bound, and Theorem 11.64.
*Overstatement.*  None in the theorem.

### Entry 40 — Proposition 11.81 (ferromagnets)  [(a) P; (b) local P, global N in a range; (c) P given 11.64, completion not refereed]  (L7892–7981)

*Statement.*  (a) For concave `φ`, `R_H ≤ R_unif`, with equality for `B = 0`, `0 ≤ βJ ≤ 1`.  (b) The
junction with the uniform cube is beyond the critical coupling.  (c) For ferromagnetic
Curie–Weiss known parts an adaptive algorithm without a hint has exponent at most `R_unif`.
*Assumptions.*
- concavity of `φ` in (a) — `{P}`: Corollary 11.91 removes it for the hinted exponent of symmetric
  instances and for the non-adaptive one.
- the known part is a *function of the type* — `{F}` for "ferromagnets are never harder than the
  uniform cube": **`S3`** (independent code): for the nearest-neighbour ferromagnetic chain with
  flip probability `0.3` at `u = 1` every algorithm needs `e^{0.0346n − O(1)}` evaluations at every
  bounded accuracy (`0.0309n` at `p = 0.4`), against the cube's `e^{0.029139n + o(n)}`; the report's own
  §11.32 has `h_∞ ∈ [0.0401, 0.0450]` (L11401) and harness XXV.2 `0.0328`.
- `βJ ≥ 0` in (c) — `{P}`: the Hubbard–Stratonovich mixture of fields ("nothing for
  antiferromagnets: a negative coupling is not a positive mixture of fields", L7968–7969);
  `{?}` otherwise (Conjecture 11.94).
- the junction formula in (b) — `{F}` as a general statement (R10 M1; DEAD.25: at `u = 8`, `e = 0`,
  `βJ = 8.2632 < βJ* = 8.3366` a constant exit undercuts); `βJ*`, `E_unif = 3.307`, `I(½) = 3.438`
  recomputed by hand and consistent.
- Theorem 11.64 with failure probabilities `δ/(2Yn²)` — `{P}` (L7961–7966).
*Computational reading.*  Comparisons of exponents; nothing at finite `n`.
*Overstatement — among the worst.*  **README:358–359**: "A ferromagnetic interaction never makes
the problem harder than no interaction, and a shallow barrier is invisible to every exponent."
First half: true for mean-field ferromagnets, false for the ferromagnetic chain of the same
README's item (xviii) (README:547–551) — the sentence has no "of the mean-field kind".  Second
half: the proved statement is local; the global one is numerical, holds "only in a range of
slopes and accuracies" and "as first stated, for all `(e, u)`, it was false" (L7894–7895) — the
very correction that the same README paragraph reports at README:341–343; and for the adaptive
exponent it rests on the squeeze `[R_H, R_unif]`, numerical again.  The report's own heading has
"can be invisible" (L7547).

### Entry 41 — Proposition 11.82 (two phases: what the supremum looks like)  [N; every value a proved lower bound]  (L7983–8062)

One model (`βJ = 1.5`, `B = 0`, `u = 1`; side cases).  Every number is a lower bound for all
algorithms at `H` (Theorem 11.78(a)); none is known to be the value: `{?}`.  The free block beyond
`e₀ = 0.001804`, the seven-atom profile at `e = 0.05`, the failure of the pair identity for cones
around profile classes at `u = 0.30` are searches.  Not recomputed by this reader.

### Entry 42 — Conjecture 11.83 and the open items  [C]  (L8064–8120)

O4 — the adaptive exponent without a hint for any interacting known part — is the largest `{?}`
of this part: the nested algorithm fails at fact (F2), the repair by the type of the inner block
"leads to a recursion over rate functions that we could not close" (L9044–9045), and nothing but
the two-sided bound `R_H ≤ θ* ≤ θ_na` is proved outside ferromagnets and fields.

## 9. §11.24 — rounds of adaptivity

*Common setting of Entries 43–46.*  Uniform cube, no known part, class `L_u`, bounded accuracy;
`τ^{(r)}` is a `limsup`/`liminf` of `n⁻¹ln` of the least cost of `r`-round algorithms.  Refereed
(SCI-REV-0003): one major finding (the stopping rule), nine minor.

### Entry 43 — Theorem 11.84 (a ladder is as many rounds as it has rungs)  [P, given Theorem 11.56]  (L8269–8362)

*Statement.*  The batched schedule B2L⁺ has `r_1 + … + r_L` rounds, returns the bracket of Algorithm
2L⁺ with probability `1 − δ`, and — by a stopping rule — costs at most
`1 + M_max(1 + C_1) + Σ_{l≥2}3(J+1)cnt(x_{l−1})C_l` in every run.  Hence `τ^{(r)} → h`.
*Assumptions.*
- the stopping rule before each stage — `{F}` without it for the cost bound: `|C_2| = 393 216 = M_max`
  against `N_2 = 79 931` when rung 1 returns trivial brackets (L8296–8305; DEAD.27; XX.5).
- fixed levels and ladders (a fixed `η`) — `{E}` for "a number of rounds independent of `n`": the
  algorithms that reach `h + o(1)` have unboundedly many levels; whether `τ^{(r)} = h` for a finite
  `r` is open — `{?}`.
- Theorem 11.56 — `{P}` (Claims A, B use its steps 2, 6, 7).
*Check.*  `T^{(2)}(0)/a = 0.618, 0.620, 0.624, 0.641, 0.665` recomputed by direct minimisation (`S4`).
*Computational reading.*  "Independent of `n`" is not "small".  The recursion gives
`T^{(r)}(0)/a = 0.624 … 0.335` for `r = 2 … 64` against `h/a = 0.263`, "a gap of about
`0.37a/(log₂ r)^{0.8}`" (L8341–8342): if that fit held beyond its range, a gap of 5 % of `h` would need
`log₂ r ≈ 65`, i.e. `r ≈ 4·10^{19}` rounds (this reader's extrapolation).  And "the values for
`r ≥ 4` rest on one grid computation … and have no stored witness" (L8337–8339).
*Overstatement.*  L8208: "**The nested algorithms need a number of rounds that does not depend on
`n`**" — for a fixed `η`; the restriction follows in L8311–8320 (added after SCI-REV-0003).  Mild.

### Entry 44 — Lemma 11.85 and Theorem R4.1 (what `r` batches can see)  [two rounds V; general `r` P; R4.1 V]  (L8364–8403, L8467–8504)

*Assumptions.*  Block-radial twins with uniformly random hidden centres — `{E}` (the construction);
finite mixtures of deterministic algorithms in Lean — `{C}` ("for randomness without finite support
… that step is on paper", L8495–8497); a bound on batch sizes — `{C}` for two rounds (R4.1 needs
none), `{P}` for `r ≥ 3` (the virtual run is not a run on one function).
*Generalises.*  The Lean statements are abstract (arbitrary point sets and hidden parameters).

### Entry 45 — Theorem 11.86, Corollary R4.2, Corollary 11.87 (two rounds do not reach `h`)  [P; finite-`n` twins by exact computation]  (L8405–8512)

*Statement.*  `τ^{(2)} ≥ θ₂*(u) > h` for every slope, also for the expected cost at one instance (the
flat histogram of a block); hence `a = τ^{(1)} > T^{(2)}(0) ≥ τ^{(2)} ≥ θ₂* > h = lim τ^{(r)}`.
*Assumptions.*
- exactly two rounds — `{?}` for three: "the natural continuation of the two-round family hides
  nothing from a third batch" (L8229–8230; D50 item 5); "is `τ^{(3)} = h`? Either answer would be new".
- the whole class `L_u` (the twins are members) — `{E}`: on radial instances two rounds reach `h`
  (Proposition 11.88(c)).
- the uniform cube without a known part — `{?}` beyond (open (4), L8542).
- large `n` — `{P}`: the separation is asymptotic.
*Check.*  `θ₂*/a = 0.349, 0.359, 0.394, 0.440`, `θ₂*/h`, and the best `φ₁` at four slopes recomputed
from the definition of `Ξ` (`S4`): all agree.
*Computational reading.*  "These are two lower bounds; the separation from adaptive algorithms is
asymptotic, and none is shown at such a size" (L8220–8221): at `n = 3200` the two-round bound is
`e^{0.037n} = e^{118}`.  The matching upper bound at the hard instance is open.
*Overstatement.*  None left after SCI-REV-0003 (the statement at `n = 3200` was reworded, m5).

### Entry 46 — Proposition 11.88 (what a round can and cannot do)  [P unless marked]  (L8514–8534)

(a)–(c) proved; (d) upper half "[sketch]"; (e) "[sketch + numerical, an idealised game]", "not
examined" by the referee.  `{?}` for (d) upper and (e).  No recommendation rests on them.

## 10. §11.25 — slices

### Entry 47 — Lemma 11.89 (odds ratio)  [K: Hasenclever–Scholz 2013]  (L8619–8719)

*Assumptions.*  Binary variables — `{F}` for more letters: for Potts pairs "uniform marginals do
not maximise `I(s)`" (L8931–8934; XXI.5); positive cells — `{C}`.  The lemma is in print; "what is
ours in this section is therefore the application" (L8718–8719).

### Entry 48 — Theorem 11.90 (a slice is never harder than the cube)  [P; reviewed SCI-REV-0001]  (L8745–8839)

*Statement.*  On the type class of density `κ` binary centres suffice, the exponent functions have
closed forms, and `F*_{m,κ} ≤ F*_c` with equality only for `m = κ = ½`.
*Assumptions.*  Two letters — `{F}` beyond (Entry 47; at `u = 0.5` the two-letter values exceed the
three-letter ones, `0.007673` against `0.007425`, recomputed in `S4`); `e ≥ −h(κ)` — `{E}` (below it
no profile is feasible); the half-ray `ℓ ≥ 0` in the closed form — `{F}` over the whole ray
(`0.0202` against `0.1441`, L8759–8760) and harmless after the supremum over `m`.
*Check.*  All 24 numbers of the slice table at `u = 1` (values and centre types, L8772–8778)
recomputed from the closed forms (`S4`).
*Computational reading.*  Closed forms; exponents.

### Entry 49 — Corollary 11.91 (every function-of-type known part against the uniform cube)  [inequalities P; as exponents given Theorems 11.78, 11.79]  (L8855–8924)

*Statement.*  For every exchangeable `π` and every landscape: `R_λ ≤ R̂_c`, `N ≤ θ_na^{cube}`; equality
for symmetric convex rate functions.
*Assumptions.*
- two letters — `{F}` (L8926–8942: "a known part that pins the composition onto two of them … makes
  certification harder than no known part at small slopes").
- a function of the type — `{F}` beyond: the nearest-neighbour chain (`S3`; L11517–11526 explains
  why there is no contradiction).
- which exponent: the hinted one at *symmetric* instances and the non-adaptive one — `{E}` as a
  restriction of the claim; the adaptive exponent `θ*` is `{?}` ("an antiferromagnet without a
  field `θ* ∈ [0.029139, 0.110944]`", L8884–8885).
- exits inside the type class — `{Q}`: the slice bound is not the truth when exits change the type
  (`0.029139` against `R^max(0) = 0.025034` for a field `p = 0.3`, L8921–8922; the second number
  recomputed in `S4`).
- extensive accuracy — `{P}` ("nothing is said at bounded accuracy", L8885–8886).
*Overstatement.*  The headline was narrowed after SCI-REV-0001 (M1).  What remains: L9050–9053,
"the whole difficulty of certifying a free energy can be accounted for one value of the order
parameter at a time" — the accounting is an upper bound that the corollary's own "what the
corollary does not say" (L8920–8924) shows not to be tight.  Mild.

### Entry 50 — Theorem 11.92, Lemma 11.93, Conjecture 11.94 (reduction of algorithms to slices)  [P; deterministic core V; conjecture C]  (L8954–9045)

*Assumptions.*  Exchangeable `π` with known `p_t` — `{E}`; bracket procedures on every type class —
`{?}`: the only ones available are fixed samples, so "(c) yields today … nothing beyond Theorem
11.79(c)" (L8981–8986); accuracy `x_m + ln(n+1)` — `{P}`: extensive only; a uniformly random split
in Lemma 11.93 — `{F}` with a fixed partition ("with a fixed partition this is false", L9004–9006).
Conjecture 11.94(iii) — the adaptive exponent of a slice — is `{?}`; "none of it is written, so
whether an idea is missing as well is not known" (L9032–9033).
*Computational reading.*  A reduction, not a result about cost.

## 11. §11.26 — several site types, alphabets, asymmetric envelopes

*Common setting of Entries 51–57.*  A fixed sequence of `m` site types, alphabets `q_j ≥ 2`, a
*product* reference `⊗π_{τ(i)}` of full support, site envelopes with the triangle inequality, not
necessarily symmetric; extensive accuracy.  Reviewed (SCI-REV-0005): Theorems 11.99, 11.101 proved
after two gaps were closed.  "**Nothing of the nested algorithm has been simulated**" (L9096).

### Entry 51 — Theorem 11.95 (what the symmetry of the sequence gives)  [lower bounds V; rest P]  (L9141–9155)

*Assumptions.*  As Entry 36 with the group `ΠS_{n_j}`: few orbits — `{E}`; the factor
`8N_orb ln(2N_orb/δ)/(1−2δ)`, `N_orb = Π_jC(n_j+q_j−1, q_j−1)` — `{Q}` and often vacuous: `S7`, e.g.
`m = 20`, `q = 3`, `n = 300`: `ln(`factor`) = 105` against `na ≈ 75`; with every site its own type the
statement is empty.  "A fixed sequence of site types" is therefore a real restriction: finitely
many types, each repeated often.
*Overstatement.*  §0.3, L95 (see Entry 36).

### Entry 52 — Lemma 11.96 and Theorem 11.97 (single-letter theorem for functions of the joint type; isoperimetry for `μ_H`)  [P; (a) every `n`; (b), (c) by types]  (L9157–9250)

*Assumptions.*  (a), (b): the known part is a function of the joint type — `{E}` (orbit-uniform
measure).  (c): a product measure with `π_min > 0`, bounded `D_max`, `q_max`, `m` — `{Q}`: the error is
`ω_n ≤ q_max n^{−1/(2q_max+2)} + c·n^{−1/4}` uniformly in the composition.  Not refereed beyond the review
of 11.101: "a referee … for Theorem 11.97(c) together with Theorem 11.78(b)" is "not done"
(L9615–9618).
*Computational reading.*  **Vacuous as a finite-`n` statement**: `q_max n^{−1/(2q_max+2)} ≤ 0.05` needs
`n ≥ 4·10⁹` for two letters, `1.7·10^{14}` for three, `10^{19}` for four (`S4`, block H).  "The true size
of `ω_n` is not known: on the workstream's test families, `n ≤ 72`, the least admissible `ω` is at
most `0.42·ln n/n`" (L9249–9250).

### Entry 53 — Theorem 11.98 (product known parts: evaluation)  [P]  (L9252–9278)

*Assumptions.*  Product reference — `{E}` for separation over site types and "vertex labels
suffice" (open with interactions, L9474–9476); one common slope `t` for all types — `{E}`, it is the
result (exponents do not add; averaging at a common accuracy overestimates by up to `1365 %`,
L9366–9367); compositions tending to `λ` in (d) — `{P}`.  `F*` concave is **not** assumed for the pair.

### Entry 54 — Theorem 11.99 (the site function is a Rényi capacity)  [P; two steps V; reviewed: proved]  (L9280–9344)

*Statement.*  `F*_j(t) = (1−t)C_t` of the vertex channel; `θ_na = E_sp^{−1}`; "a fixed sample certifies
`E_sp(θ)`, for `0 < θ < a`; an adaptive algorithm, or one with a hint, certifies `E_sp(θ) − θ`, for
`0 < θ < h`".
*Assumptions.*  A finite site with a law of full support and an envelope closed under soft minima —
`{C}` (the identity holds for any finite space: §11.32 uses it for a whole chain as one site);
the ranges `θ < a`, `θ < h`, the worst case, the exponential scale — `{E}` for the operational
sentence (added after SCI-REV-0005 m1); `E_0` maximised per site type at a common `ρ` — `{E}`
(Sibson against Augustin, convention (2)).
*Check.*  `E_sp(θ) − θ = −0.008` at `θ = 0.3a` on the cube (`S4`).
*Computational reading.*  An identity between formulas: "no coding theorem is used" (L1306–1307).
*Overstatement.*  None left in the theorem.

### Entry 55 — Proposition 11.100 (exponents of site types do not add; `F*` need not be concave)  [P; N; C]  (L9346–9367)

*Assumptions.*  Three or more letters for non-concavity — the kink of the triangle site (DEAD.23).
Two letters: concavity of `F*` is a conjecture — `{?}`.  **Attacked here, `S5`:** 1 596 two-letter
channels including extreme ones (`logit` of both vertex laws in `[−14, 14]`, i.e. slopes and fields
up to 14, where the reviewers' 1 100 random sites did not go) on 399 slopes each, and a fine scan
of Z-like channels: no second difference above `2·10^{−10}`.  The conjecture survives; it remains
without proof.
*Computational reading.*  Not refereed (log).

### Entry 56 — Theorem 11.101 (adaptive algorithms without a hint, site types)  [lower bound P from V pieces, every `n`; upper bound P by transfer]  (L9369–9454)

*Statement.*  (a) At an additive instance at least `(1−2δ)exp(−tε + nΣ_jλ_jF_j(γ_j,t))` evaluations.
(b) Along compositions tending to `λ`, the adaptive cost without a hint is `exp(nR̂(ε₁) + o(n))`.
*Assumptions.*
- product reference — `{F}` for the proof ("fact (F2) uses the product structure of `π` (the step
  that fails with interactions)", L9389), `{?}` for the statement.
- finitely many site types with fractions tending to `λ` — `{P}` for (b) (uniformity (G1), (G2), (L)),
  `{?}` for genuinely site-dependent parameters: the lower bound (a) is a product over sites and
  does not care; no upper bound exists when the number of types grows with `n`.
- `λ_j > 0` — `{P}`, possibly `{C}`: "neither the reviewer nor we see where the argument uses it"
  (L9383–9385).
- extensive accuracy — `{P}`; bounded accuracy `{?}` ("Upper bounds at bounded accuracy" not done).
- the orientation of an asymmetric envelope — `{F}` if transposed ("2 582 violations of the tail
  lemma in 13 328 brute-force cases", L9135).
- the count of Theorem 11.52 — `{P}`, "inherited", not re-examined by the review.
*Computational reading.*  Lower bound usable at every `n` (on `mix` at `n = 480`: at least
`(1−2δ)·1.9·10⁶` evaluations, L9569–9570); the upper bound inherits Entry 52 and has never been run.
*Overstatement.*  L9077–9079: "The landscapes the certificate formats were built for have … more
than two states per site, single-site known parts and site envelopes that need not be
symmetric".  The certificate formats of §§1–6 were built for a *pairwise* known part
(`E₀ = Σh_i + ΣJ_ij`, L113); "single-site known parts" is the restriction of this section, presented
as the target setting.  Repeated in README:430–433.

### Entry 57 — Propositions 11.102, 11.103 (asymmetric envelopes; which site law is hardest)  [P; N]  (L9456–9543)

*Assumptions.*  "One must not symmetrise" — `{F}` (`max(d, dᵀ)` enlarges the class, `min` shrinks it,
L9464); two letters for "a field always helps" and for Corollary 11.91 — `{F}` (11.103(d), DEAD.24);
the ceiling `F*(t) ≤ t(1−t)D²/8` — general (any site, any envelope): record.  11.102 and
11.103(a)–(c) are "not refereed" (log).
*Check.*  The crossings `e^u = k(k−1)` (`h_2 = h_3`, `h_3 = h_4`, `h_4 = h_5` to `10^{−11}`), `a_2 = a_3` at
`u = 0.5194`, the four-letter groupings at `u = 1`, the three-letter values and their distance from
the ceiling (`11 %`, `5.0 %`, `1.9 %`, `5.8 %`) were recomputed (`S4`).
*Computational reading.*  The ceiling gives a usable universal bound: `h ≤ D²/32` per site.
*Overstatement.*  None found; the false first versions are recorded (D52).

## 12. §11.27 — evaluations together with local averaged data

### Entry 58 — Proposition 11.104 (a marginal oracle does not change the non-adaptive exponent on the cube)  [P; coordinator; not refereed]  (L9644–9681)

*Statement.*  With all exact marginals of order `≤ k` of the Gibbs measure for free, non-adaptive
algorithms still need `(1−2δ)2ⁿ/(|C|·|B(n,r−1)|)` evaluations; with BCH duals `|C| ≤ (2n)^{⌈k/2⌉}`, so
the exponent is unchanged for `k = o(n/ln n)`.
*Assumptions.*
- `k = o(n/ln n)` — `{X}`: **new, `S6`(ii)** — for `k = n` the oracle returns `μ_ψ` itself and *one*
  evaluation gives `ln A` exactly (`A = e^{−ψ(x₀)}/(2ⁿμ_ψ(x₀))`).  So between `k = o(n/ln n)` and `k = n`
  the complexity falls from exponential to one; where is `{?}`.  The proof itself survives for
  `k = κn` with small `κ` at a loss `ln 2·h₂(κ)` per site in the count *and in the accuracy* (codes
  from the Gilbert–Varshamov bound; `S6`(iii): positive exponent at `u = 1` up to `κ ≈ 0.02`).
- uniform cube, zero known part — `{P}` (translations by a code preserve the reference); with a
  field: one-body marginals only (Theorem 11.109a).
- exact marginals — `{?}` for noisy ones (the division's Proposition E "not checked by us", L10266).
- non-adaptive algorithms — the adaptive half is the other division's Theorem C, "not reviewed by
  us" (L1522).
*Computational reading.*  The loss `|C|` is polynomial and small against the bound it divides.
*Overstatement.*  README:453 calls exact marginals of the Gibbs measure of the residual on the
uniform cube "local experimental data"; the report's title has "local ensemble-averaged data"
and "an idealisation".  Mild.

## 13. §11.28 — observable free energies: the range of a ratio

*Common setting of Entries 59–62.*  A finite space with weights `w > 0`, an envelope with zero
diagonal and the triangle inequality (not necessarily symmetric), two disjoint non-empty
macrostates; only the *range* of `Z_g(A)/Z_g(B)` over the class, not the cost of narrowing it.
The coordinator's proofs, "not refereed", reviewed and replicated by the Scientific Discovery
Division (SCI-RES-0005).

### Entry 59 — Theorem 11.105 (duality for the robust ratio)  [(c) weak duality, (d) upper bound, (e), admissibility in (b): V; rest P]  (L9745–9815)

*Statement.*  Only the constraints from `B` to `A` matter; the maximum is attained at a closed pair;
`R⁺` is the value of a transport problem with gains, and every feasible plan is a certificate;
closed forms for one state; a max–min sandwich.
*Assumptions.*
- the triangle inequality of the envelope — `{F}` for (a) and (d) as stated, `{C}` in practice.
  **New, `S2`:** three states `a ∈ A`, `b ∈ B`, `c` outside, `d(b,a) = 10`, `d(b,c) = d(c,a) = 1`: the true
  `ln R⁺ = 2`, the bipartite programme of (a) and formula (d) give `10`; on 300 random raw tables the
  bipartite programme overestimates in 188 (never underestimates).  The shortest-path closure
  restores equality (300 of 300) and does not change the class (cf. D3).  The certificate half (c)
  is sound for raw tables too — it only becomes loose.
- finite space, positive weights — `{C}`.
- strong duality — `{P}` (linear programming, on paper).
- the programme has `|A|·|B|` variables — `{X}`: for macrostates of a product space it is
  exponentially large; "closed forms exist for one state, for thresholds of the order parameter on
  the cube, for one-coordinate macrostates with independent sites, and at the exponential scale"
  (§8, L1252–1254).
*Generalises.*  "As general as its hypotheses (a finite space, a quasi-metric envelope)" (L9975–9976)
— correct.  *Not covered:* the number of evaluations ("open", L9957–9958; settled only for box
classes, Entry 71); chains with geometric envelopes; soft or more than two macrostates.
*Computational reading.*  A certificate checked in `O(|A||B|)` additions; the sandwich (e) loses
exactly `ln|A| + ln|B|`.
*Overstatement.*  None.

### Entry 60 — Theorem 11.106 (symmetry; the two sides of a threshold)  [P]  (L9817–9846)

*Assumptions.*  A finite group preserving `w`, `d`, `A` and `B` — `{E}` for the reduction to orbits;
every type of `B` below every type of `A` — `{F}` otherwise for "the extremal residual is the maximal
field": "for a band between two parts of `B` no field is extremal" (L9837–9839); exchangeable
reference and macrostates that are unions of type classes — `{E}`.
*Computational reading.*  A closed form: `±n·ln cosh(u/2)(1+o(1))` for the two halves of the cube.

### Entry 61 — Theorem 11.106a (monotone macrostates: the two uniform fields are extremal)  [V; the division's]  (L9848–9899)

*Assumptions.*  Submodular known part — `{F}`: the field is "strictly suboptimal in 17 of 25
instances with a frustrated known part" (L9891; XXIII.6).  Monotone macrostates (a lower set
against an upper set) — `{F}`: "12 of 22 with a macrostate that is not monotone".  `β ≥ 0` — `{F}`
(`cube_sandwich_fails_negative_beta` [V]).  An envelope that two functions saturate (the cube
with site constants; ordered alphabets with envelopes additive along the order) — `{F}` for
attainment on three or more unordered states ("the fields give valid but not attained bounds",
L9895–9896).  `c_i^↑ + c_i^↓ ≥ 0` — `{E}` (otherwise the class is empty).
*Generalises.*  The Lean statement is on any finite distributive lattice: already general.  A
common generalisation with Theorem 11.106 "is known to neither division" — `{?}`.
*Computational reading.*  Two evaluations of a partition function of the known part in a field.

### Entry 62 — Theorems 11.107, 11.108 (one-coordinate macrostates; the exponential scale)  [P]  (L9901–9955)

*Assumptions.*  11.107: a site-additive envelope and a macrostate defined by one site — `{E}`;
an additive known part for exactness — `{Q}`: for a pairwise known part a two-sided bracket with a
site-local certificate, "both inequalities are strict in general" [N].  11.108: an exchangeable
reference, macrostates that are unions of type classes and closures of their interiors — `{E}` for
the limit formula; the every-`n` sandwich loses `ln` of the number of type classes.
*Computational reading.*  11.108 at `n = 144`: bracket `[0.4256, 0.4400]` against the limit `0.4142`
(L9949–9952) — the finite-size terms are `0.3`–`0.75·ln n/n`.

## 14. §11.29 — a one-body marginal oracle with a field

### Entry 63 — Proposition 11.109 (the criterion)  [P; (a), (b) V]  (L10017–10065)

*Assumptions.*  A product reference `Bernoulli(p)^{⊗n}`, one slope — `{P}` for the window `[p₋, p₊]`;
invariance under a transitive group of site permutations — `{E}` for "all one-body marginals equal
the mean type"; an exact oracle — `{?}` for noisy answers.  "At this size the symmetrised sets fill
whole type classes, so the illustration is about the oracle's answers, not about exponents"
(L10064–10065).

### Entry 64 — Theorem 11.109a (compensation: the class exponents are unchanged)  [(a)–(c) V; (d), (e) P; the division's]  (L10067–10193)

*Statement.*  For every `n`: at the instance `−ln(w̃_γ + b·w̃)` every algorithm with a free exact
one-body oracle makes at least `(1−2δ)/(n·H_{k,r})` evaluations; with the upper bounds of Theorems
11.64, 11.61 the class exponents are `R^max` and `θ_na`; at every bounded accuracy `h` and at least `a`.
*Assumptions.*
- one-body marginals — `{?}` for order `k ≥ 3` with a field ("its conjecture", L10270); for `k = 2`
  the division's construction is "not checked by us".
- a field (product reference, two letters) — `{P}`; the Lean statement is "for sites indexed by any
  finite group".
- the class is a convex cone in the weights (closed under sums and maxima) — `{E}` for the
  compensation by an admixture.
- `κ = ω_m − 1/(e^r − 1) > 0` — `{E}` (forces `u > 0`, `1 ≤ k ≤ n−1`).
- exact oracle — `{Q}`: "with all marginals … known only to an absolute precision `τ` the adaptive
  bound loses a factor polynomial in `1/τ`" (the division's, not checked, L10270–10271).
*Computational reading.*  The every-`n` bound carries the factors `n(n+1)C_m`: its exponent is
`0.00069`, `0.00889`, `0.01044` at `n = 400, 1600, 3200` against `R^max = 0.012210` (L10190–10192) — 6 %
of the limit at `n = 400`.
*Overstatement.*  §0.3, L98 "the adaptive exponent is `R^max` and the non-adaptive one `θ_na`, for
every `n`" — exponents are limits; "for every `n`" belongs to the lower bounds.  Mild.

### Entry 65 — Proposition 11.109b (at an instance the oracle helps)  [(a) P; (b) P given 11.78(b); (c) sketch; (d), numbers N]  (L10195–10261)

*Assumptions.*  A hint `γ`; Theorem 11.78(b) at the shifted field — `{P}`; the matched alternatives
of (c) — `{?}` ("a proof sketch of the division's … of it we re-derived the Laplace step only").
The truth lies in `[V_γ, U_γ]`, "which end is the truth is open".
*Overstatement.*  L10222: "**for `p ≠ ½` the oracle strictly lowers the exponent of the zero
residual**" — in bold, resting on "`∂_θR_γ ≠ 0` for `p ≠ ½` (**[N]**: in every case computed)" one line
above.  The label of the proposition gives (b) as [P].

## 15. §11.30 — sup-norm (box) classes around a sampleable known part

*Common setting of Entries 66–71.*  A finite space; a known function `f̂` whose partition function
`Z₀` is known and whose Gibbs measure `π` can be sampled exactly; a remainder known through
pointwise bounds `lo ≤ r ≤ hi`.  "Not refereed" as a section; parts reviewed (SCI-REV-0013, -0015).
"Every ingredient is in print" (L99).

### Entry 66 — Theorem 11.110 (box classes)  [(a) K; (f) K + V; (b), (e) P; (c), (d) V]  (L10328–10489)

*Statement.*  (c) The spot check of a hint with the dip- and bump-weighted sampler is correct on
every class inside the box with `N = ⌈ln(1/δ)·max(1, A + B)⌉` evaluations; (d) `k` disjoint heavy sets
force `(1−2δ)k` evaluations; (e) the cost is `Θ((Z(lo)/Z(r) − 1)/ε + (1 − Z(hi)/Z(r))/ε)`; (f) with a
certified floor and variance, `0 ≤ K ≤ W(b, σ²)`.
*Assumptions.*
- a *certified* floor `lo ≤ r` — `{E}`, and `{F}` without it: on `{E′ ≤ m₊}` no algorithm certifies an
  upper bound of `ln Z` with fewer than `(1−δ)|X|` evaluations (Proposition 11.113b(c)); "a variance
  estimated from the samples is not such a bound" (DEAD.28).  For a physical remainder none
  exists (§8, L1267–1269).
- exact independent samples of `π` and a known `Z₀` — `{X}`: product measures and bounded treewidth
  only; "a pairwise model on a general graph cannot be sampled exactly" (L10917–10918);
  approximately sampleable known parts are open (§12 item 13(d)).
- **a hint equal to the instance** — `{X}`: the display of (e) bounds `min_alg E|Q(r)|` over algorithms
  tailored to `r`; its upper bound is the spot check *of the hint `r`*.  Without a hint the worst
  case is `e^{w}/ε²` (L11014–11016) and instance-wise `max(σ², εμ′)/(εμ′)²` against the hinted
  `(1 − μ′)/(εμ′)` (L10546–10548): `1/ε²` instead of `1/ε`.
- computation is free — `{X}`: the spot check needs `Z(r)` *of the hint* (to know `N` and to state its
  answer) and samples of the dip/bump-weighted laws; both are available when the hint is the
  tractable model itself (`r ≡ 0`, sampler `π`), not for a general hint.
- no single state can change `ln Z` by `ε` — `{Q}`: a two-stage check covers the general case (the
  division's, "not re-derived here beyond the two lines", L10421–10427).
- `ε ≲ 1` for the `Θ` — `{Q}` (for large `ε` the two ends differ by `≈ 4(e^{ε/2}+1)ln(1/δ)/(1−2δ)`).
- finite space — `{C}`: (f) is machine-checked "on any probability space".
*Generalises.*  Lower models `m ≤ E` in place of a constant floor; Proposition 11.112 (Rényi
family); Propositions 11.113–11.113b (sandwiches).  *Not covered:* classes with geometry between
the box and the first-order class; minima ("minima do not share the benefit").
*Check.*  `544`, `1088`, `545`, the crossover `n ≈ 240`, `L(3.7) = 1.46`, `W(3.7, 0.036²) = 3.4·10^{−3}`
recomputed (`S4`).
*Computational reading.*  **Useful exactly when the floor is a few `k_BT` away, exponential in it
otherwise.**  `544` evaluations at `ρ₋ = 3`, `ε = 0.2`, `δ = 0.05`, whatever `n`.  On the division's
enumerated instances the distance `ln(Z(lo)/Z)` is `0.07–1.7` for valine but "`10–56` for serine and
`30–243` for two to four lysines", linear in the chain (L11045–11047): costs `e^{10}` to `e^{243}`; and
"these are the prices that a certificate would have to pay, not certificates" (L11043–11044).
*Overstatement — among the worst.*  **L10405–10411** ("**the cost of certifying a free energy in a
box class is …**"), **§0.3 L99** ("the cost of certifying `ln Z` is `Θ(…)` … with matching bounds for
all randomised algorithms") and **README:491–494** ("the number of evaluations that certifies the
free energy is the Boltzmann factor … divided by the accuracy") state the *hinted verification*
cost as "the cost".  The section knows the difference ("what the hint buys": "a hint buys the
variance term"), the headlines do not carry the three words "with a hint".

### Entry 67 — Corollary 11.111 (a sup-norm bound caps the cost of every class)  [P from V]  (L10520–10531)

*Assumptions.*  A hint in `𝒞 ∩ 𝓑` — `{X}` as in Entry 66 (without one the plain sample mean with
`e^{w}/ε²` samples serves every subclass of the box); the box bound certified — `{E}`.
*Computational reading.*  On the cube with `u = 1` and `|g| ≤ 3`: at most 1088 evaluations for every
`n`, against `e^{0.0291n}` — the smaller one from `n ≈ 240` (recomputed).  A real crossover at a
size where both numbers are feasible — the only one in this part.

### Entry 68 — Proposition 11.112 (the floor is the end `p = ∞` of a family)  [P; in print without a hint]  (L10920–11010)

*Assumptions.*  An a-priori bound on `‖e^{−r}‖_{L^p(π)}` or on a Rényi/Kullback–Leibler divergence of
the true ensemble from the model — `{E}`; an *exponential* moment — `{F}` for polynomial moments of
the remainder energy: "a root mean square of `0.1 k_BT` allows a dip of `100 k_BT` on a state of mass
`10^{−6}`, a change of `ln μ` by 86" (L10995–10996; recomputed); `B − B₀ ≥ B/2`, `ε ≤ 1` for the `Θ` —
`{Q}`; a product measure in (e) — `{P}`.  "Not checked by us": orders `1 < p < 2` without a hint and
the worst-case lower bound without a hint.
*Computational reading.*  (e) `e^{Σc_i²/4}/(δε²)`: polynomial only for square-summable constants; at
a fixed slope per site it is `e^{nu²/4}` — "exponential, and weaker than the samplers of §11.9".

### Entry 69 — Propositions 11.113, 11.113a (sandwiches; nested sandwiches)  [P]  (L10551–10767)

*Assumptions.*  Two models `m₋ ≤ E ≤ m₊` with known partition functions, the lower one sampleable —
`{X}` (as Entry 66); `[0,1]`-valued weights (Hoeffding) — `{Q}` (empirical Bernstein, (c′));
`N_f` fixed in advance in 11.113a — `{?}`: "the bound is not proved if proposals are drawn *until*
`N` have been accepted … nor for a stopping rule that looks at the running bracket"
(L10698–10700); a fine-grained sampler in the lower bound of (d) — `{P}` (two-point argument,
`Σq(x)² ≪ ε²/sinh²(Δ/2)`).
*Check.*  The factor `e^{−Δ}`, the widths `7.6·10^{−4}` and `5·10^{−3}`, `κ(δ)` and `0.316` recomputed (`S4`).
*Computational reading.*  The most usable statements of the part *given a sandwich*: a width of
`7.4·10^{−4}` nats from 50 000 accepted proposals (the division's run, "not re-run by us").  The
sandwich itself is an input.

### Entry 70 — Proposition 11.113b (one side at a time)  [(a) V; (b), (c) P, not refereed]  (L10769–10832)

*Assumptions.*  A floor with its sampler — `{E}` for a two-sided certificate, at the price `e^{2x}/ε²`
(`e^{x}/ε²` variance-sensitive), "the exponential cannot be avoided"; a ceiling alone — `{F}` for any
finite upper bound below `(1−δ)|X|` evaluations.  The division's data: the floor-only sampler would
need `6.9·10⁶ … 7·10⁹` evaluations where the nested sampler used `60 … 12 000` (L10825–10829;
arithmetic, "the floor-only sampler not run").

### Entry 71 — Corollary 11.114 (a ratio of two macrostate weights in a box class)  [(a)–(c) V; (d) P]  (L10834–10900)

*Assumptions.*  `π` can be sampled *conditionally* on each macrostate — `{X}` ("which is the
tractability assumption here", L10879–10880); a class without geometry — `{E}` for "nothing cancels";
`{?}` with geometry (§12 item 11(a)); a hint, `ε ≲ 1`, no heavy state — as Entry 66.  The constants
`6.9`, `10.7` are "its constants, not re-derived by us".
*Computational reading.*  "A macrostate of weight `10^{−6}` with a floor `8 k_BT` deep … has cost number
`e^{8} − 1 ≈ 2980` for the ratio and `0.11` for `ln Z`" (recomputed).

## 16. §11.31 — barriers and traps

### Entry 72 — Theorem 11.115 (barrier and trap certificates)  [V; not refereed; no harness test]  (L11192–11233)

*Statement.*  A cut whose wall is certified by the min kernel (or the residual kernel) bounds a
minimax barrier from below; box cuts; tree cuts with an exact adjacency test; site-graph
products; a trap bound `1 − T·U/Lo` for every stationary kernel.
*Assumptions.*  A finite configuration space with a move graph — `{C}` ((a) is for any move graph
in Lean: already general); single-site moves for box and tree cuts — `{P}` (the wall of a box is a
union of `n` boxes); non-empty boxes in the adjacency criterion — `{F}` without it
(`sep_card_le_one_not_sufficient` [V]); stationarity of the kernel, start from `w` restricted to the
basin — `{E}` for the trap bound (no reversibility needed: record); the barrier is relative to the
move set — `{E}` as a caveat ("a discrete rate is relative to the move set").
*Not covered* (stated, L11248–11258): completeness of the tree format, any size bound, exactness of
the robust interval of barrier heights, continuous surfaces; deciding a zero barrier is
PSPACE-complete (cited).
*Computational reading.*  Soundness only.  "Coordinate cuts certify nothing under unrestricted
single-site moves" — the format is not vacuous only on site-graph products.
*Overstatement.*  None.

## 17. §11.32 — a nearest-neighbour chain as known part

### Entry 73 — Theorem 11.116 (two reductions to blocks, a lower bound for every algorithm, a recursion, the limit)  [(c) V; (a), (b) V in two-block form; rest P]  (L11298–11389)

*Statement.*  (a) Cut couplings move into the residual at the price of slacks in the envelope.
(b) Blocks with gaps embed exactly.  (c) For any finite `(X, π, d)`, any law `M` on members and
`0 < t < 1`, every algorithm makes at least `(1−2δ)exp(G_t(M) − tε)` evaluations at the soft minimum
of the labels.  (d) A Markov recursion with a one-sided slack.  (e) Sub- and super-additive
brackets of the limit `F_∞`.  Refereed (R11; SCI-REV-0010).
*Assumptions.*
- none in (c) — **already general**: the Lean theorem `softMin_expected_queries_ge` takes an
  arbitrary `d : X → X → ℝ` (no triangle inequality, no symmetry), any known part, any finite `X`.
  It is the most general lower bound of this part.
- nearest-neighbour couplings in (a), (b) — `{Q}`: any finite range by blocking; in `ℤ^d` "both
  reductions lose a surface term", on trees "the sandwich does not close" (sketches, L11552–11554).
- a non-empty reduced class in (b): `u > κ_m` — `{E}`.
- the one-sided slack in (d) — `{F}` without it ("the left side is `0.667` and the product without
  slack `0.866`", L11357–11359; XXV.2).
- stationarity and homogeneity in (e) — `{P}` (exact sub-/super-additivity).
- for upper bounds on costs: Theorems 11.95, 11.98(d), 11.101(b) applied to blocks of `L` sites as
  super-sites of alphabet `q^L`, extensive accuracy, limits iterated — `{P}`, and `{?}` at bounded
  accuracy: "**at bounded accuracy no upper bound on the cost of any algorithm for the chain is
  proved**" (L11383–11384).
*Check.*  The embedding (b) was verified end to end on 8 sites and the bound (c) evaluated with
own code (`S3`).
*Computational reading.*  The lower bound is explicit at every `n` (loss `2t(u+K)` in the exponent,
not per site).
*Overstatement.*  None in the theorem; (f) is exemplary about what is and is not a statement on
algorithms.

### Entry 74 — Proposition 11.117 (the symmetric binary chain)  [P for the bounds, N for their evaluation]  (L11391–11535)

*Statement.*  At `u = 1` all three numbers `h_∞`, `a_∞`, `E_∞` are above the uniform cube's; to second
order in `u` the factor is `Var(Σs_i)/n`; the threshold rises at every slope; at large slopes the
proved upper bounds of `a_∞` and `h_∞` are below the cube's.
*Assumptions.*
- a symmetric envelope in the small-slope law (b) — `{F}`: on two points with `d₀(0,1) = 1`,
  `d₀(1,0) = 0` the coefficient is `V/4` (L11433–11439; XXV.3; D62 item 1).
- an associated (ferromagnetic) law for `V = ¼Var(Σs_i)` — `{F}`: for the antiferromagnetic chain
  the staggered field wins, `0.43` against `1.23` (recomputed in `S4`).
- a fixed length and second order in `u` — `{P}`: "nothing is uniform in `n`"; for the limit the
  lower side is "a sketch for `h` and `a`".
- one model: two states, one coupling, no field, one slope per statement — `{?}` for everything
  else ("a field, more states, site-dependent couplings", §12 item 14(f)); the direction of `a_∞`
  between `u ≈ 1.5` and `u = 3` is open.
- floating-point duality brackets, "no interval arithmetic" — `{P}` for the numbers.
*Check.*  `E_F` at four couplings, `u*` at four, the variance factors and all four ratios of the
table of (d) recomputed (`S4`); the direction at `u = 1` re-established with own code (`S3`:
`0.0346` at `p = 0.3`, `0.0309` at `p = 0.4`, against the cube's `0.029139`).
*Computational reading.*  Brackets, not values: `h_∞ ∈ [0.0401, 0.0450]` at `p = 0.3`.
*Overstatement.*  L11539–11543: the coupling "**raises** the cost of certification where the
envelope is weak … and **lowers** two of the three where it is strong".  "Raises" is
unconditional (a lower bound for every algorithm above the cube's exact exponent).  "Lowers" is
a statement about upper bounds of game-function numbers; as a statement about costs it is
conditional — "for non-adaptive algorithms both sides are conditional" (L11385) — and §8
(L1345–1346) writes "proved … at `u ≥ 3` for the non-adaptive exponent (downwards)" without the
condition.

---

## A. Synthesis

### A.1 The hierarchy (tractable model → broader classes → what fails)

The main line is the query complexity of `ln Z` over a first-order (Lipschitz) class.  Each level
lists what holds, with its label, and what was *lost* on the way down.

```
LEVEL 0   uniform cube, no known part, one slope, exact evaluations, worst case over L_u
          fixed samples: theta_na, a; plain Monte Carlo optimal            11.44 [P], 11.45 [V core]
          adaptive = hinted: theta_hint (extensive) 11.54 [P]; h (bounded) 11.58 [P];
                             n h - O(1) <= ln N <= n h + O(sqrt(n ln n))    11.58a [P]
          rounds: a > tau(2) > h = lim tau(r)                               11.84-11.87 [P; lemma V]
          k-body marginal oracle changes no exponent, k = o(n/ln n)         11.104 [P]
          the ONLY level with an exact tail function (Harper) and a bounded-accuracy adaptive theorem
   |
   |  lost: exact isoperimetry (S1); bounded-accuracy adaptive bound; sub-exponential term; rounds;
   |        "the zero residual is hardest"; "sample from the Gibbs law of the known part"
   v
LEVEL 1   a field: p-biased product measure, two letters                    11.59-11.65 [P], refereed
          exponents R^max, theta_na = R^max o S^-1; hardest instance gamma*|x|; sampler flat in the type
          isoperimetry only asymptotic, error 2 n^(-1/8)                    11.63 [P]
          bounded accuracy: non-adaptive only (11.61a); one-body oracle: 11.109a [V core]
   |
   |  lost: "a field always helps", "the uniform site law is hardest", concavity of F* (>= 3 letters);
   |        the error term worsens to n^(-1/(2q+2)); nothing simulated
   v
LEVEL 2   finitely many site types, any finite alphabets, asymmetric site envelopes,
          single-site (product) known part                                  11.95-11.103 [P by transfer]
          R^ = max_t [sum_j lambda_j F*_j(t) - t e], F*_j a Renyi capacity; one common slope
   |
   |  lost: the product measure, hence fact (F2) and every nested algorithm (S8)
   v
LEVEL 3   exchangeable known parts (functions of the type: mean-field), two letters
          every n, by symmetry: stratified sample optimal up to a polynomial factor;
                                H hardest among SYMMETRIC instances         11.76 [V lower / P upper]
          hinted exponent at symmetric instances: a supremum over block profiles   11.78 [P]
          convex rate function: game function, pair identity                11.80 [P]
          <= uniform cube for two of the three exponents                    11.91 [P]
          adaptive exponent: OPEN (ferromagnetic Curie-Weiss: <= cube, 11.81(c))
          two phases: values from searches only                             11.82 [N]
   3'     any finite symmetry group with few orbits                         GroupSampling.lean [V]
   |
   |  lost: symmetry, hence the stratified sample (truncation leaves the class), every upper bound
   |        that is not conditional, every formula; "ferromagnets are not harder" becomes false (S3)
   v
LEVEL 4   a nearest-neighbour chain as known part (one synthetic two-state model)
          lower bounds for every algorithm, every n, every accuracy         11.116(b),(c) [V core]
          game function in numerical brackets; direction of the effect turns with the slope   11.117 [P/N]
   |
   v
LEVEL 5   no structure: any finite space, any reference measure, any envelope
          what survives:  11.43(a) [V]   11.62 [P]   11.45(a) [V]   11.116(c) [V]   (lower bounds, tail lemma)
          what does not exist: any upper bound on the cost of any algorithm for a first-order class
```

Three side branches, each with its own ladder:

* **Other classes of ignorance** (not first-order): linear in known features — rank-many
  evaluations (11.47 [V], general) → a Hilbert ball — the spectrum (11.50a [V]) → a box with a
  certified floor and a sampleable known part — `e^{floor}/ε` with a hint (11.110 [V core]) → Rényi
  balls (11.112 [P]).  Each is a *different* assumption; none is implied by a first-order envelope.
* **Chain geometry**: linear classes (general) → the profile envelope of pair-additive residuals
  (any chain; 11.48) → cost bounds (excluded volume; a lattice; 11.49, vacuous at extensive
  accuracy) → the limit shape (diamond-lattice *bridges*, zero residual; 11.69–11.71) → walks
  (Conjecture 11.75) → off-lattice (nothing).
* **Observables**: the range of a ratio of macrostate weights (any finite space with a
  quasi-metric envelope; 11.105) → closed forms (thresholds with exchangeable references 11.106;
  monotone macrostates with submodular known parts 11.106a [V]; one coordinate 11.107; the
  exponential scale 11.108) → the *cost* of narrowing the range: box classes only (11.114).

**Not covered by any result of this part.**  Continuous configuration spaces (all statements are
for finite spaces; for Gaussian space the report claims nothing and the nested construction is
obstructed, L5120–5126); known parts with long-range or many-body interactions other than
mean-field ones; known parts without symmetry and without a chain structure (only Level 5);
genuinely site-dependent parameters (a number of site types that grows with `n`: lower bounds
only); noisy evaluations in any nested algorithm; adaptive algorithms at bounded accuracy
beyond Level 0; minima in box classes; any statement on computation as opposed to evaluations.

### A.2 The ten assumptions whose classification matters most outside the models of the report

1. **A product reference measure in every adaptive upper bound** (Entries 11, 13, 15, 25, 56): false
   for the proof without it (fact (F2); `S8`), unknown for the statement.  Consequence: for no known
   part with interactions is the adaptive cost known, except "at most the cube's" for mean-field
   ferromagnets.
2. **The model of ignorance itself — worst case over a first-order class, exact evaluations —
   and the hint** (Entries 9, 13, 66): essential for the exponential lower bounds, which are
   properties of the class; and every "cost" stated at an instance (§§11.20, 11.23, 11.26, 11.30)
   is a *verification* cost for an algorithm that was told the instance.  Removing the hint
   changes `1/ε` into `1/ε²` in box classes and is open elsewhere, instance by instance.
3. **Symmetry with few orbits** (Entries 21, 36, 51): essential for every every-`n` statement about
   fixed samples; false for Markov references (the truncation leaves the class); vacuous for
   sequences with many site types (`S7`).
4. **Uniform measure and equal slopes in the exact tail lemma** (Entry 1): false beyond them (`S1`,
   both tests).  Consequence: every upper bound below Level 0 is asymptotic with an error term
   that is useless at any size (`n^{−1/8}`, `n^{−1/(2q+2)}`; Entries 24, 52), and the Harper term of
   Algorithm 2L⁺ — hence every bounded-accuracy adaptive result — has no counterpart there.
5. **Two letters in the comparison theorems** (Entries 26, 47–49, 57): false for three ("a field
   always helps", "no function-of-type known part is harder than the cube", uniform marginals
   maximise the mutual information).
6. **A function of the type in "ferromagnets are never harder than the uniform cube"** (Entries 40,
   49): false for the nearest-neighbour ferromagnet (`S3`; §11.32).
7. **A convex rate function (one phase)** (Entry 39): false without it, three times over; with two
   phases every exponent is a searched lower bound and the extremal perturbations are not cones.
8. **Extensive accuracy** in every adaptive statement below Level 0 and in the slice and reduction
   results (Entries 25, 49, 50, 56, 73): required by the present proofs; whether the exponents
   survive at bounded accuracy is not known for any of them.
9. **Free computation: exact samples of the Gibbs measure of the known part, a known density of
   states, tables `Ξ_H(q)`, the partition function of the hint** (Entries 21, 23, 25, 36, 66): each
   changes the complexity if it has to be paid for; the theorems count evaluations.
10. **A certified a-priori constant** — the slope `u`, the floor `lo`, a variance, a norm bound, a
    per-pair `L` (Entries 6, 9, 66, 68): essential, and supplied by nothing in the report for any
    physical remainder; without the floor the cost of a box class is the number of states.

Next in line: bridges, one lattice and the zero residual in §11.22 (Entries 28–35); a symmetric
envelope and an associated law in the small-slope law (Entry 74); `δ < ½` (replaceable, Entry 16);
`k = o(n/ln n)` in the oracle result (Entry 58); the triangle inequality in the ratio duality
(free to restore, Entry 59).

### A.3 Where no classification was possible, ranked by how much hangs on it

1. **The adaptive exponent without a hint for any interacting known part** (O4 of Conjecture 11.83;
   Conjecture 11.94(iii)).  Whether "adaptive = hinted" is a property of product measures or of
   the problem.  Everything about adaptivity at Levels 3–5 hangs on it.
2. **A bounded-accuracy adaptive upper bound beyond the uniform cube** — needs a lower tail
   function for a non-uniform measure; without it Levels 1–2 say nothing at the accuracies one
   would use.
3. **A lower bound for adaptive algorithms without a hint above the hinted one** — at the
   sub-exponential scale (`nh + ½ln n` to `nh + O(√(n ln n))`), and instance by instance (is some
   algorithm cheap wherever a hint makes the instance cheap?).
4. **Whether the flat-histogram instance is the hardest of all instances**, not only of the
   symmetric ones (Entry 36).
5. **Upper bounds for genuinely heterogeneous sites** (the number of site types growing with `n`;
   Entry 56) — the case the word "heteropolymer" suggests.
6. **Whether the exponents of Level 4 are costs**: unconditional upper bounds for a chain, the
   crossover slope, the conjecture `E_n = ln[Z_n(u/2)/Z_n(0)]` (Entries 73, 74).
7. **Conjecture 11.75** (walks against bridges), whether `ε₁ = ½` is an exceptional accuracy, and
   anything off-lattice (Entries 32, 35).
8. **Two-phase values**: binary optimality at vanishing accuracy (C1), the supremum beyond `e₀`
   (O2), the witness condition (O3, O5), equality in Theorem 11.80(d) (Entries 38, 39, 41).
9. **`τ^{(3)} = h`?** and rounds with a known part (Entry 45).
10. **The abstract form of "what a problem must supply"** (Entry 27) — workstream N.
11. **The marginal oracle between `k = o(n/ln n)` and `k = n`**; order `k ≥ 3` with a field; noisy
    marginals; the instance-wise exponent in `[V_γ, U_γ]` (Entries 58, 64, 65).
12. **Exact evaluations** in the nested algorithms (Entry 13); `½ ≤ δ < 1` at extensive accuracy
    (Entry 16); proposals drawn until `N` are accepted in the nested sampler (Entry 69).
13. **Concavity of the two-letter site function** (Entry 55): survived `S5`; no proof.
14. A common generalisation of Theorems 11.106 and 11.106a (Entry 61); the routing lemma and the
    scaling form of single-flip constants (Entries 33, 34).

### A.4 Overstatements (25), with line numbers

*Major* — the sentence asserts something that a theorem of the report contradicts or does not
contain:

| # | where | sentence | what is proved |
|---|---|---|---|
| 1 | L4579–4583; README:148–151 | "no procedure that is correct on a first-order class can be cheap on any of its subclasses" | false as written: Theorem 11.45(d), L4205–4211, gives a class-correct procedure that costs `n + 3` on every cone (Entry 9) |
| 2 | README:358–359 | "A ferromagnetic interaction never makes the problem harder than no interaction, and a shallow barrier is invisible to every exponent." | first half: mean-field ferromagnets only — the ferromagnetic chain is harder (README:547–551; `S3`); second half: numerical, in a range of slopes, false as a general statement (L7894–7895) (Entry 40) |
| 3 | L10405–10411; L99; README:491–494 | "the cost of certifying a free energy in a box class is …" | the cost *with the instance as a hint*; without one `e^{w}/ε²` in the worst case (L11014–11016) (Entry 66) |
| 4 | L6105–6107 | "Everything carries over with one change that matters" | not Theorems 11.58, 11.58a, the exact tail lemma, the rounds, any simulation (Entry 25) |
| 5 | L9077–9079; README:430–433 | "The landscapes the certificate formats were built for have … single-site known parts" | the formats were built for pairwise known parts (L113); single-site is the restriction of §11.26 (Entry 56) |

*Moderate* — a restriction or a label is missing where the sentence stands:

| # | where | sentence | missing |
|---|---|---|---|
| 6 | L4092 (title) | "Monte Carlo is exponent-optimal among non-adaptive algorithms" | "on the uniform cube"; with a field it is "exponentially worse" (L6233) |
| 7 | L90; README:303–308 | status "machine-checked" for "the shear law; …" | the shear law about algorithms is Theorems 11.44–11.64, on paper (Entry 27) |
| 8 | L6370–6371 | "'adaptive = hinted' persists with a known part" | "that is a field"; open with interactions (L7553–7556) |
| 9 | L7531–7535; L11689–11691 | "Symmetry alone settles the non-adaptive problem"; "§11.23 settles … the hinted exponent of symmetric instances for every rate function" | settles the optimal sample; the exponents are unknown without convexity (Entries 36, 37) |
| 10 | L92; L95 | "flat-histogram sampling is optimal non-adaptively"; "joint-type-stratified sampling is optimal among fixed samples for every `n`" | "up to a polynomial factor in the cost and `ln(4/δ)` in the accuracy" — often larger than the cost (`S7`) |
| 11 | L5782–5784 | "the adaptive algorithm is certified cheaper — in every run, at every instance —" | "certified" by a paper count (Entry 18) |
| 12 | L10222 | "for `p ≠ ½` the oracle strictly lowers the exponent of the zero residual" | rests on "[N]: in every case computed" (Entry 65) |
| 13 | L11539–11543; L1345–1346 | the coupling "lowers two of the three"; "proved … for the non-adaptive exponent (downwards)" | conditional as a statement about costs (L11385) (Entry 74) |
| 14 | L4706 (title); L5049–5050; L5972–5973; README:240–241 | "a hint is worth nothing to an adaptive algorithm" | "in the worst case over the cube class"; with a field the hint `g = 0` is worth an exponent (L6376–6379) |
| 15 | L87 | status "inequalities and kernel machine-checked; refereed (R6, R_P)" | the kernel is "not refereed" (L4527) |
| 16 | L6640–6651 | "Then non-adaptive algorithms have the exponent `R∘S^{−1}` and adaptive ones `R`" | an abstract implication that is not proved (workstream N) |

*Mild*:

| # | where | sentence | remark |
|---|---|---|---|
| 17 | L9050–9053 | "the whole difficulty of certifying a free energy can be accounted for one value of the order parameter at a time" | an upper bound that is not tight (L8920–8924) |
| 18 | L6655 (title) | "Chains in the thermodynamic limit: … the limit of certificate sizes" | bridges of one lattice model at the zero residual; a limit only off an unidentified set |
| 19 | L8208 | "The nested algorithms need a number of rounds that does not depend on `n`" | for a fixed `η` (said at L8311–8320) |
| 20 | L4339–4342 | "a certificate for the minimum … whatever the size of `X`" | of evaluations; the minimisation is not counted (L4520–4523) |
| 21 | README:291–292 | "A field always helps: every exponent decreases with the strength of the field" | two letters (README:443–444) |
| 22 | README:453 | "local experimental data" | exact marginals of an idealised Gibbs measure |
| 23 | L98 | "the adaptive exponent is `R^max` and the non-adaptive one `θ_na`, for every `n`" | exponents are limits; "every `n`" belongs to the lower bounds |
| 24 | L1512 | "certificates in this format exist whose size does not depend on the chain length" | the bound is vacuous (L4455–4456) |
| 25 | L4924–4925 | "No product structure of `ψ` is used." | the product structure of the measure is |

Sections with no overstatement found: §11.28, §11.31 (and §11.24 after SCI-REV-0003).

### A.5 What was computed for this audit

All scripts are in `experiments/audit/AA2/`, deterministic or seeded (`20261126`), numpy/scipy only,
each below a minute except `S4` (two minutes), far below 1 GB.  Command for each:
`python3 experiments/audit/AA2/<script>.py > experiments/audit/AA2/<output>`.

| | script → output | what it shows |
|---|---|---|
| `S1` | `s1_tail_lemma_beyond_uniform.py` → `out_s1.txt` | all 65 534 subsets of `Q_4`.  Control: Lemma 11.43(b) holds with equality at balls (12 cases).  **A (new):** with a `p`-biased measure Hamming balls are not extremal for the tail functional relative to `ψ₀ = 0`: ratio up to `2.083` at `(p, u) = (0.2, 2)`; "type-dependent balls" up to `1.123`.  **B (new):** with site-dependent slopes weighted-metric balls are not extremal for 17 of 20 slope vectors, ratio up to `2.363` (sub-cubes over the cheap coordinates win) |
| `S2` | `s2_ratio_without_triangle.py` → `out_s2.txt` | **new:** without the triangle inequality Theorem 11.105(a), (d) overestimate `ln R⁺` (`10` against `2` on three states; 188 of 300 random raw tables); after the shortest-path closure equality in 300 of 300 |
| `S3` | `s3_ferromagnetic_chain_harder_than_cube.py` → `out_s3.txt` | own implementation of the block certificate of §11.32: embedding verified on 8 sites; lower bound for every algorithm `0.03462` per site at `p = 0.3` (`0.03086` at `p = 0.4`), `u = 1`, against the cube's `0.029139` — "ferromagnets are never harder than the cube" fails outside mean-field models |
| `S4` | `s4_recompute_quoted_numbers.py` → `out_s4.txt` | 216 quoted numbers of §§11.16–11.32 recomputed from the printed formulas: **216 PASS, 0 FAIL**; block H: the sizes at which the proved isoperimetric error terms fall below the exponents (`10^{11}`–`10^{19}`) |
| `S5` | `s5_two_letter_concavity_scan.py` → `out_s5.txt` | 1 596 two-letter channels (slopes and fields up to 14) × 399 slopes: no violation of the concavity conjecture of Proposition 11.100 (largest second difference `≤ 0`) |
| `S6` | `s6_degenerate_regimes.py` → `out_s6.txt` | **new:** (i) for `δ ≥ 1 − 1/⌈nu/ε⌉` one evaluation is `(ε/2, δ)`-correct on the whole class (`Q_8`, 400 members); (ii) with a marginal oracle of order `k = n` one evaluation gives `ln A` exactly; (iii) what the proof of Proposition 11.104 gives for `k = κn` |
| `S7` | `s7_polynomial_factors.py` → `out_s7.txt` | the factors of Theorems 11.76(a), 11.95 against the costs they multiply: vacuous for `n ≤ 50` on the cube, for 20 site types up to `n = 300`, and empty for one type per site |
| `S8` | `s8_fibre_averages_with_interactions.py` → `out_s8.txt` | fact (F2) with a Curie–Weiss known part: the fibre average of a member of `L_u` changes by `u(1 + c)` per outer flip, `c = 0.3`–`0.6` (one phase, antiferromagnets), up to `26` (two phases) |

Arguments written out in the entries (no script): the hypothesis (E) of the abstract limit
theorem is redundant (Entry 29); a `K`-level version of the lower bounds for every `δ < 1` at
accuracy `Kε` (Entry 16); bounded-error evaluations cost plain Monte Carlo an additive `η`
(Entry 2).

**New counterexamples constructed** (not in the repository before): `S1` A, `S1` B, `S2`, `S6`(i),
`S6`(ii); the contradiction between L4579–4583 and Theorem 11.45(d) (Entry 9).  **Independent
confirmations** of counterexamples the repository has: `S3` (harness XXV.2), `S8` (L8093–8101).

### A.6 Errors found in the report on the way

1. **A stale sentence about Lean** (L4967–4970): "What is **not** in Lean is the operator `R` itself
   … and that the iterates … satisfy the hypotheses of (d) … is not formalised."  Since
   `BoundedAccuracy.lean` the operator is defined (`Rstep`, an infimum over an admissible set,
   line 55 of the file) and the hypotheses are proved (`stepLE_exact`, `exactRec_props`); the
   header of the same theorem (L4927) and §11.19 (L5995–5998: "so Theorem 11.53 holds for the
   recursion as defined, with no hypothesis") say so.  The sentence contradicts both.
2. **L4579–4583 is false as written** (overstatement 1): contradicted by Theorem 11.45(d).
3. **README:358–359 contradicts its own paragraph** (overstatement 2): README:341–343 reports that
   the claim "a shallow barrier is invisible … for every slope was false at large slopes", and
   sixteen lines later states it without restriction.
4. **§8 against §11.32** (overstatement 13): L1345–1346 says the direction of the effect is "proved
   … for the non-adaptive exponent (downwards)"; Theorem 11.116(f) says that for non-adaptive
   algorithms "both sides are conditional" (L11385).
5. **Records out of date.**  The log ("Resume here", the sentence beginning "The coordinator's own
   proofs, checked numerically, no referee") still lists "the rate `O(1/k)` for the level
   recursion" as unrefereed, while the report gives it as machine-checked by the Scientific
   Discovery Division (L4990–4998) and the log itself records `RateFull.lean` elsewhere.
   README:21 lists "the independent referee reports on the theory report (nine so far)", R1–R9;
   R10, R11, R12 are in `docs/reviews/` and are cited by the README's own items (viii), (xviii),
   (xxii).  L79 has "(`reviews/R2` – `R9`)" likewise.
6. **A redundant hypothesis**, not an error: (E) in the abstract limit theorem behind Theorem
   11.69 follows from (C), (B) and `Q_1 ≠ ∅` (Entry 29).

No numerical error was found: 216 of 216 recomputed numbers agree (`S4`), and the three numbers
of §11.32 recomputed by another route (`S3`) are consistent with the brackets printed.

### A.7 Counts, and what this audit did not do

*Entries:* 74, covering 85 numbered statements — 40 Theorems (11.44–11.116 of this part, with
11.58a, 11.106a, 11.109a) and 45 Lemmas, Propositions, Corollaries and Conjectures — and the
adopted Theorem R4.1/Corollary R4.2.

*Classifications* — tags in §§1–17, counted with

    sed -n '/^## 1\. /,/^## A\. /p' docs/audit/AA2_REPORT.md | grep -o '`{[EPCQXF?]}`' | sort | uniq -c


| `{E}` essential | `{P}` proof only | `{C}` convenience | `{Q}` quantitative substitute | `{X}` changes complexity | `{F}` false without | `{?}` not known | total |
|---|---|---|---|---|---|---|---|
| 63 | 62 | 29 | 28 | 18 | 52 | 45 | 297 |

Of the classifications "false without", five rest on constructions of this audit (`S1` twice;
`S2`; `S6`(i), in Entries 3 and 16) and one "changes the complexity" on `S6`(ii); the others cite a
harness test, a dead end, a Lean witness or a later theorem of the report.

*Not done.*  No Lean file was compiled (declarations were read where a classification depended
on them: `SetLimit.lean`, `BoundedAccuracy.lean`, `SoftMinLowerBound.lean`, `NonAdaptive.lean`).
The proofs of Theorems 11.52, 11.56 and 11.58a were read for their use of the cube, not
re-derived (workstream N; referees R7, R8, R12).  The two-phase numbers of Proposition 11.82,
the numbers of Theorem 11.71(c) other than the polytopes, the `ln C_max` column of remark (1a)
and the tables of remark (1b) were not recomputed.  Prior-art statements were not checked.  The
harness was not re-run; its stored output `docs/falsification_output.txt` was read.
