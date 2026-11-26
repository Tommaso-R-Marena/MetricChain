# AA1 — Assumption audit of `docs/THEORY_REPORT.md`, §§2–6 and §§11.1–11.15

*Reader AA1 of the assumption audit (brief: `docs/workstreams/AA_brief.md`; mandate: item 2 of the
research owner's directive, `docs/collaboration/messages/theory/THY-MSG-0016.md` §1).  Written
adversarially by a reader who wrote none of the theorems.  Date: 2026-11-26.*

**Object.**  `docs/THEORY_REPORT.md` as last changed by commit `7e6eb4c` (12 251 lines), sections
2–6 (Directions A–E) and 11.1–11.15; the rows of §0.2 (A1–E2), of §0.3 (the first three rows) and
of §10 (G1–G17) that summarise them; the sentences of §7 and of `README.md` (668 lines, last
changed by `dd067f1`) that restate them.  Repository HEAD when this was written: `b2cf817`.
**All line numbers below are line numbers of those two files in that state.**  (The report was
edited once while the audit ran — 11 lines inserted near line 12 000; nothing cited here moved.
`docs/RESEARCH_LOG.md` moved as well and is therefore cited by section name.)

**What was done.**  Every statement and label of the two parts was read in full; proofs were read
where a classification depends on them; the Lean signatures of the statements whose generality is
at issue were read in `proofs/` (not compiled — `lake` was not run); `docs/DEAD_ENDS.md` D1–D42
and the entries after it that touch §11.7, the referee reports R1–R4 and the workstream reviews
R_B, R_C, R_D, R_E, R_G were used as evidence; the statements of the workstream reports behind
§§11.11–11.15 were compared with the statements of the theory report.  Seven scripts were written
(`experiments/audit/AA1/`, with stored outputs; §9 of this document lists them and the commands);
they contain the new counterexamples, an independent recomputation of 48 numbers of the two
parts (all 48 reproduced) and a cross-check of the 405 Lean names cited there (all declared).

**Conventions.**
* The report's labels are kept in square brackets: **[V]** machine-checked, **[P]** paper proof,
  **[K]** known and cited, **[N]** numerical.
* The seven categories of the brief are written in braces, so that they cannot be confused with
  the labels: **{E}** mathematically essential; **{P}** needed only by the present proof;
  **{C}** convenience (computational or expository; includes "without loss of generality");
  **{Q}** replaceable by a weaker quantitative condition (stated); **{X}** removal changes the
  computational complexity (from what to what); **{F}** removal makes the stated result false
  (counterexample cited); **{?}** not known.  An assumption can carry two tags (for instance
  {F}{Q}: false if simply dropped, true with a stated quantitative substitute).
* Evidence pointers: `Dnn` = entry of `docs/DEAD_ENDS.md`; `XI.3`, `DEAD.5`, … = test ids of
  `experiments/falsify_conjectures.py`; `S1`–`S7` = the scripts of this audit (part ids as printed
  in their outputs); Lean names in backticks.
* "Refereed" follows `docs/RESEARCH_LOG.md` (section "Resume here") and the scope sections of the
  referee reports themselves; where the report's own status cells say more, this is recorded
  (§8, Err-10).

**Counts.**  50 entries cover 71 numbered statements.  In §§2–6 (the 20 rows of §0.2): Theorems
2.1–2.7 with the two corollaries of §2.3, Theorem 3.1, the kernel, voxel and Hölder statements of
§§3.4–3.5, Lemma 4.1, Theorems 4.2–4.6, Corollary 4.7, §5, the Master Soundness Theorems and
Theorem 6.1 — 23 statements.  In §§11.1–11.15: Theorems and Propositions 11.1–11.42 with 11.18a–f
— 48 statements.  The classifications are counted in §10.

---

## 0. The result of the audit in one page

1. **No machine-checked statement was found false, and the Lean statements are as general as the
   prose says or more so** (Theorems 2.3, 2.4, 2.6, 2.7 and 11.22 are stated for an arbitrary
   type — no finiteness, hence continuous spaces included; the one-shot lower bounds 11.6, 11.13,
   11.24, 11.27(a,b) hold for every finite instance with no product, symmetry or homogeneity
   assumption).
2. **One paper theorem is false as stated in the theory report: Theorem 11.33(a)** (second-order
   classes below the Curie–Weiss coupling cost polynomially many evaluations).  Its source,
   `docs/workstreams/D_REPORT.md` Theorem 13, assumes an *additive* known part; the theory report
   states (a) with no hypothesis on the known part, in a chapter whose setting gives every
   instance a known part (line 1739–1740).  Without it the statement fails: for a
   pairwise known part made of ferromagnetic blocks every algorithm needs at least `e^{c·n^{1/3}}`
   evaluations at the boundary coupling `w = 4`, and for a known part that is a code landscape
   `(1 − 2δ)·e^{R(w)n}` evaluations at every coupling `w > 0`, `R(4) = 0.056` (S4; §8, Err-1).
3. **Seven passages are stale** — they contradict later sections of the same report (§8,
   Err-2 to Err-8), among them "whether additivity survives for binary Markov trees is open" (line 502,
   refuted at line 4083) and "where between, for adaptive algorithms, is open" (line 3413,
   settled in §§11.18–11.19).
4. **Twenty-two items present a result more generally than it is proved** (§7).  The three
   worst: `README.md` 148–150 ("no procedure that is correct on a first-order class can be cheap
   on any of its subclasses" — false at the instances the report itself names at lines
   3400–3403); the unqualified dichotomy "one evaluation or exponentially many" (`README.md`
   117–119; report 1082–1084, 1496, 1966–1969, 2998–3001), which needs an additive residual with
   `κ < 1` and site types that stay fixed as `n` grows — with margins `c_i/e_i − 1 < 1/n` all
   `n` sites are non-sharp and the smallest certificate has exactly `n + 1` points (S3); and
   row G15, line 1507 with 3898–3900 ("second-order classes have a transition at the
   Curie–Weiss coupling"), which summarises the theorem of item 2 without the hypothesis that
   makes it true.  A fourth of the same kind as D14: line 2171–2174 states the `Σc_i²` width and
   its sampling version without the product reference (S2: the width fails for *every*
   positive correlation).
5. **What carries the theory outside its models is a short list.**  The exact statements about
   the envelope class (§2, §11.1–11.3, 11.12–11.14, 11.22–11.24, 11.26, 11.29) need nothing but a
   finite or arbitrary set and a difference-constraint class.  Every *exponent* and every
   *threshold* needs independent sites (a product measure, an additive known part, a
   site-additive envelope), almost always identical sites, an additive instance, and an accuracy
   window; every "bounded cost" statement is at an extensive accuracy.  The second-order and
   chain results are for one reference configuration, a product domain and constants that are
   inputs — certified, so far, for no residual in this repository (the one exception the report
   names is another division's paper certificate for one twenty-residue instance, line
   1272–1279).  §4 is the hierarchy, §5 the ten assumptions that matter most.
6. **Quantitatively**, most positive guarantees are at extensive accuracy or exponential cost, and
   several lower bounds are small at the sizes one would compute (the machine-checked cube bound at
   `u = 1`, `ε = 1` is `e^{4.6}` evaluations at `n = 100` and `e^{16.9}` at `n = 500`; S6(d)).
   Each entry says which.

---

## 1. Entries, part I — sections 2–6 (the first phase; rows A1–E2 of §0.2)

Status of the whole part: machine-checked statements; refereed by R1 (`docs/reviews/R1_referee_report.md`,
which read the Lean signature of every statement it discusses) and audited twice by an internal
reviewer (D14–D20).  After R1 the report itself classifies the mathematics as elementary or
classical (lines 66–79); that classification is not disputed here.

### E1. Theorem 2.1 and §3.1 — dominance transport, thermal dead-end elimination (row D1)

1. **Statement.**  `T : A → S` injective with `E(Tx) + γ ≤ E(x)` on `A`, `β ≥ 0` ⟹
   `Z_β(A) ≤ e^{−βγ} Z_β(S)`; pruning with margin `γ` changes `ln Z` by at most `ln(1 + e^{−βγ})`
   (`ln(1 + m e^{−βγ})` for an `m`-to-one map); Boltzmann averages of `|O| ≤ B` move by at most
   `2B e^{−βγ}`.  **[V]** (`partition_transport`, `partition_prune_bracket_fibers`, `thermal_dee`,
   `boltzmannAvg_dominance_error`); refereed (R1).
2. **Setting.**  Any type, finite sets `A, S`, any real energy function; in §3.1 a product box and
   the map `x ↦ x[i ↦ t]`.  Nothing about pairwise structure is used.
3. **Assumptions.**
   * **{F}{Q}** `T` injective.  Dropped: `A = {a₁, a₂}`, `S = {s}`, `E(a) = E(s) + γ`:
     `Z(A) = 2e^{−βγ}Z(S)` (S1(c1)).  Quantitative substitute: at most `m`-to-one ⟹ factor `m` **[V]**
     (harness I.6); attained by the same example.
   * **{F}** `β ≥ 0`.  For `β < 0` the inequality reverses (S1(c2)).
   * **{E}** the pointwise margin `E(Tx) + γ ≤ E(x)` on all of `A` — it is the content; the
     producer must certify it (Goldstein value for pairwise `E`, Theorem 2.2; margin `≥ γ + δ_i`
     for an envelope class, by `differential_dee_sound` at zero temperature — the thermal rule
     with a residual is not stated in the report but follows from Theorem 2.1 applied to `E₀ + Δ`).
   * **{C}** finite sets.  For a measure `μ` the same proof gives `Z(A) ≤ J·e^{−βγ}Z(S)` whenever
     `T` is injective, measurable and `T_#(μ|_A) ≤ J·μ|_S` (one line: change of variables); the
     report uses the finite form only, after voxelisation, where `T` maps a voxel to a voxel and
     `J` is the ratio of their volumes — that ratio is absent from `PruneZOK` because the weights
     `w_i` already contain the volumes (§3.4).
   * **{C}** `A ∩ S = ∅`, `t ≠ r`, product box (§3.1) — bookkeeping for the two-sided bracket.
4. **Generalises.**  To `m`-to-one maps, to observables, to the weight domain (`zprune_sound`);
   split and multi-site maps are instances (line 154–156).  Not covered: how to *find* a map with a
   certified margin beyond single-site ones (Theorem 2.2 says single-site ones gain nothing from
   the gauge; multi-site ones are a search problem, line 189–196).
5. **Computational reading.**  Useful.  The error is `Σ_k ln(1 + m_k e^{−βγ_k})` over pruning rounds
   (line 415–417): linear in the number of *rounds*, independent of the number of conformations
   each round removes.  At 298 K a margin of 3 kcal/mol gives `e^{−βγ} = 6·10⁻³` per round, so a
   thousand rounds certify `ln Z` only to about 6 nats; a total of 0.1 nat needs
   `βγ ≥ ln(10⁴)`, i.e. margins above 5.5 kcal/mol.  Benchmark B6 (line 161): `4·10⁻⁴` to `1`.
6. **Overstatement check.**  Line 159–160, "this bound does not grow with the *number* of pruned
   conformations": true per injective round, and the next section gives the sum over rounds;
   read alone it suggests a size-independent error.  Minor.

### E2. Theorem 2.2 — Goldstein's criterion is exact and gauge invariant (row A8)

1. **Statement.**  For a pairwise energy on a product domain the Goldstein value is the least
   element of the set of energy differences `E(x[i↦r]) − E(x[i↦t])`, invariant under every
   reparameterisation, and equal to the best Desmet bound over gauges.  **[V]**; refereed (R1,
   item 3: scope narrowed).  Known (Shekhovtsov; de Givry et al.).
2. **Setting.**  Pairwise model, product (box) domain, one site, a dominator `t` that does not
   depend on the context.
3. **Assumptions.**
   * **{X}** pairwise energy.  With 3-body terms the difference energy is a pairwise model on the
     link graph of `i`; exact dominance is then coNP-hard in general (**[P]**, line 209–211: `t`
     dominates `r` iff `min g ≥ 0` for an arbitrary pairwise `g`), and the term-wise rule is no
     longer exact (S1(d2): exact margin `1`, nested sum of minima `−1`).  **{Q}**: if the
     difference energy is block-separable the exact margin is the sum of block minima (**[V]**
     `exact_margin_of_block_separable`, harness I.4) — cost exponential in the treewidth of the
     link graph only; that a 3-body model has this form is **[P]** (no 3-body model exists in
     Lean, D18).
   * **{X}** product domain.  On a domain with excluded pairs exact dominance "contains
     constraint satisfaction" (line 214–215) — asserted in one line.  The reduction, written
     out: take `J ≡ 0`, `h_i(t) = 1`, `h_i(r) = 0`; then no configuration with `x_i = r` is
     improved by `r ↦ t`, so "`t` dominates `r` on the domain" holds iff the domain contains no
     configuration with `x_i = r` — unsatisfiability of a binary constraint network.  Exact
     single-site dominance is therefore coNP-hard on domains with pairwise exclusions, against
     `O(Σ_j|D_j|)` operations on a product domain.
   * **{F}** single site, context-independent dominator — as a hypothesis of the *negative*
     conclusion "the gauge cannot help".  Binary ferromagnetic chain, `n = 6`, `h = (0,1)`,
     `J = 3[x_i ≠ x_{i+1}]`: the largest single-site margin is `−2`, the pair `(1,1)` is never
     dominated (largest margin `−1`), and `x ↦ 0…0` is improving and certified by one LP-dual
     bound (R1 item 3; re-computed in S1(d1)).
   * **{C}** finite alphabets.
4. **Generalises.**  Block-separable difference energies (abstract, **[V]**).  Not covered: any
   exactness statement for multi-site improving maps (their term-wise test depends on the gauge,
   **[K]**), non-product domains.
5. **Computational reading.**  The test costs `O(Σ_j |D_j|)` per pair `(r, t)`.  The theorem is a
   negative result: it removes a hope, it does not add pruning power.  Benchmark B1 (line
   315–327): single-site rules discard 13–16 % of the states where the exact criterion discards
   63–65 %.
6. **Overstatement check.**  None found: lines 184–187 and row A8 carry "for that class of tests
   only" (D1, D23).

### E3. Theorems 2.3, 2.4 and their corollaries — contact set, sharp minimum, energy window, differential DEE (rows A1, A2, A6, A7)

1. **Statement.**  `x` minimises `f + g` for *some* admissible `g` ⇔ `f(x) ≤ f(y) + d(y,x) ∀y`;
   for *every* admissible `g` ⇔ `d(x,y) ≤ f(y) − f(x) ∀y`.  With global bounds only the
   possibly-optimal set is the energy window; differential DEE is sound.  **[V]**
   (`robust_minimizer_iff`, `robust_certified_iff`, `energy_window_exact`,
   `differential_dee_sound`); refereed (R1).  Known in substance (difference constraints, sharp
   minima; lines 329–352).
2. **Setting.**  **More general than the prose**: the Lean statements are for an arbitrary type
   `X` (`variable {X : Type*}`, no `Fintype`), any `f : X → ℝ`, any `d` with zero diagonal and the
   triangle inequality — asymmetric and negative values allowed.  "Minimises" means that the
   minimum is attained at `x`.  The class is *all* `g` with `g(x) − g(y) ≤ d(x,y)`.
3. **Assumptions.**
   * **{C}{F}** triangle inequality.  Without loss of generality — the class of a table and of
     its shortest-path closure coincide — but the *criteria* are false for a table that is not
     closed: `d(y,x) = 10`, `d(y,z) = d(z,x) = 1`, `f = (5, 0, 100)` on `(x, y, z)` satisfies the
     raw contact condition while no admissible `g` makes `x` optimal; and a raw sharp-minimum
     condition can fail although `x` is optimal for every admissible `g` (S1(a1)–(a3), by linear
     programming; D3).
   * **{C}** zero diagonal (a positive diagonal entry is a vacuous constraint).
   * **{E}** the class is the *whole* difference-constraint class.  Both proofs use an extremal
     member (`d(·,x)`, `−d(x,·)`).  For a subclass (a structured residual) one half of each
     theorem survives — contact stays necessary for possible optimality, the sharp-minimum
     condition stays sufficient for certified optimality — and the other half fails.  The exact
     criteria of other classes are different theorems (second order: Theorem 11.17; linear
     classes: §11.17).
   * Not assumed: finiteness, symmetry, nonnegativity of `d`, product structure, pairwise `f`.
4. **Generalises.**  With evaluations: Theorems 2.6, 11.1, 11.2 (worst-case regret).  At finite
   temperature: Theorem 11.12 (range of a Gibbs probability; the two theorems are its limits).
   Ratios of macrostate weights: §11.28 (reader AA2).  Not covered: nothing is missing at this
   level of generality; what is missing is tractability.
5. **Computational reading.**  The criteria are optimisation problems — `min_y [f(y) + d(y,x)]`
   and `min_y [f(y) − f(x) − d(x,y)]` — pairwise minimisations for pairwise `f` and site-additive
   `d`, NP-hard in general, polynomial on chains and trees; "is state `r` of site `i` possibly
   optimal" is an `∃∀` question whose complexity is open (§8 line 1132–1134; §12 item 3).  As a
   *specification* of what a sound rule may discard the theorems are sharp; they are not
   algorithms.
6. **Overstatement check.**  None found.  "Every sound rule must keep the whole window" (line
   308–309) is exact for the information stated (global bounds, no evaluation).

### E4. Theorem 2.5 and §3.3 — McShane brackets; the exact robust interval (row A4)

1. **Statement.**  For consistent values on a finite anchor set the two McShane envelopes bracket
   every admissible residual; `min_S(f+g)` and `Z_β(f+g; S)` range *exactly* over the interval
   between the envelope values.  **[V]** (`robust_min_bracket`, `robust_partition_bracket`,
   `robust_min_interval_exact`, `robust_partition_interval_exact`); refereed (R1).  Known
   (McShane; optimal recovery).
2. **Setting.**  Arbitrary `X`, finite anchor set `A`, finite `S`; the bracket of `Z` for `β ≥ 0`.
3. **Assumptions.**
   * **{E}** consistency of the anchor values (`v(a) − v(b) ≤ d(a,b)`): otherwise the class is
     empty (`IProblem.consistent_iff_nonempty` **[V]**), and a soundness statement about it is
     vacuous (D15: the unguarded kernel accepted `41/4` on a problem whose minimum is `1`).
   * **{Q}** exact anchor values.  Interval data `lo_p ≤ Δ(x_p) ≤ hi_p` give the same theory on
     the one-point extension (§11.1; `IntervalInstance.lean` **[V]**); the bracket widens by the
     interval widths.
   * **{E}** convexity of the class — for "every value in between is attained" (intermediate
     value theorem along `(1−λ)L + λU`).  For a non-convex class the set of attainable values
     need not be an interval.
   * **{P}** finite `S`.  Monotonicity holds for integrals verbatim; attainment of intermediate
     values then needs continuity in `λ` (dominated convergence), not written.
4. **Generalises.**  The conditional envelope `D_A` (Theorem 11.1) is the same information as an
   envelope; `Z(f+L_A)/Z = E_π e^{βs(A,Y)}` (Theorem 11.13) quantifies the width.  Not covered:
   classes that are not convex.
5. **Computational reading.**  Exact, and by itself **vacuous**: with one anchor on the uniform
   cube (`f ≡ 0`, `d = c·`Hamming) the exact interval of `ln Z` has width `n·βc` — the a-priori
   width (S6(b)).  The interval is narrow only when the anchors form a cover (Theorems 11.4,
   11.13), whose size is the subject of §11.  Computing the lower end with several anchors is a
   minimum of a maximum of pairwise models (line 275–278); `Z(f + L_A)` with several anchors is
   not a pairwise partition function.
6. **Overstatement check.**  "No certificate using the same information can report a tighter
   one" (line 266–267) is exactly what is proved.  None found.

### E5. Theorem 2.6 — the query model (row A3)

1. **Statement.**  With evaluated anchors, `x` is a minimiser for some consistent admissible
   residual ⇔ contact ∧ `f(x) + L(x) ≤ f(y) + U(y) ∀y`.  **[V]**
   (`robust_minimizer_with_anchors_iff`); refereed (R1).  For `f ≡ 0`, symmetric `d`: Lemma 8 of
   Malherbe–Vayatis.
2. **Setting.**  As E3, with a finite non-empty anchor set and consistent values.
3. **Assumptions.**  Those of E3 and E4, and
   * **{E}** "up to ties": the criterion is exact for "minimiser for no consistent residual"; a
     rule that preserves only the minimum *value* may discard more (the report's two-point
     example, line 293–296; D23).
4. **Generalises.**  Theorem 11.2 is the "for every consistent residual" version (the exact
   criterion R1 asked for).
5. **Computational reading.**  As E3: a `min_y` of a pairwise model per candidate; iMinDEE is the
   one-anchor, one-sided special case.
6. **Overstatement check.**  None found (line 303–304 has "(up to ties) in the query model").

### E6. Theorem 2.7 — anchors are necessary (row A5)

1. **Statement.**  For a certificate whose incumbent is an evaluated anchor and whose bound is the
   McShane lower envelope, every state with gap `< (1−κ)σ − ε` that is `σ`-separated from the
   other anchors must be an anchor.  **[V]** (`anchor_necessary`, `anchor_card_lower_bound`);
   refereed (R1 item 1: the gloss "any certificate" was false, D21).  A rediscovery
   (Bachoc–Cesari–Gerchinovitz 2021).
2. **Setting.**  Arbitrary `X`; `d` need not even be an envelope in the Lean statement; the true
   residual `κ`-Lipschitz for `d`.
3. **Assumptions.**
   * **{F}** the certificate format (point or value certificate).  For a *configuration*
     certificate the conclusion fails: `X = {0,1}`, `d = 1`, `E₀ = (0,5)`: no evaluation at all
     (line 376–379; D21; `config_certificate_skips_forced_point` **[V]**; `DEAD.7`).
   * **{Q}** `κ ≤ 1`.  The bound scales with `1 − κ` and is empty at `κ = 1` or as soon as
     `ε ≥ (1−κ)σ`.
   * **{F}** the direction of the separation, `d(a, y) ≥ σ` (from the anchors to `y`).  With the
     transposed reading: `X = {a, y}`, `d(a,y) = 0`, `d(y,a) = 1`, `g ≡ 0`, `f = (0, 1/10)`:
     `{a}` is an exact certificate and the transposed hypothesis would force `y` (S1(b); R2, m9).
   * **{Q}** uniform separation, for the counting form — replaced by the weights of Theorem 11.6.
4. **Generalises.**  Theorems 11.4–11.6 (covering characterisation with a converse; LP duality),
   11.23 (every algorithm).  The theorem is "the first layer" of those (line 389–395).
5. **Computational reading.**  Benchmark B2: at `κ = 0.9`, `ε = 0.2` it forces nothing while the
   optimum is `2.2` (line 371–372).  Superseded; of historical interest.
6. **Overstatement check.**  Corrected in place (line 374–388).  None remaining.

### E7. Theorem 3.1 — the free-energy sandwich (row D2)

1. **Statement.**  (a) `ln(Z/Z₀) ≥ −β⟨Δ⟩₀`; (b) `≤ −β⟨Δ⟩₀ + β²(b−a)²/8` for `a ≤ Δ ≤ b`;
   (c) `≤ −β⟨Δ⟩₀ + β²Σc_i²/8` for a **product** reference and bounded differences `c_i`; (d) the
   worst residual of the bounded-difference class is additive and two-level; (e) `1/8` is optimal.
   **[V]** (`FreeEnergySandwich.lean`); refereed (R1).  Known (Jensen, Hoeffding, McDiarmid; (d)
   in Alon–Boppana–Spencer and Bobkov–Houdré–Tetali).
2. **Setting.**  Finite product spaces in Lean; `μ₀` any reference for (a), (b); `⊗_i μ_i` for
   (c)–(e); one inverse temperature.
3. **Assumptions.**
   * (a) none — holds for every reference (general).
   * **{E}{Q}** (b) bounded range.  Some control of the upper tail of `−Δ` is essential (moments
     alone certify nothing: Proposition 11.112, reader AA2); the range can be replaced by a
     one-sided floor with a variance (Bennett form, Theorem 11.110(f)) or by Rio's function
     `ℓ(βc)` (**[K]**, line 475–478).
   * **{F}{Q}** (c) product reference.  False for a perfectly correlated reference (**[V]**
     `correlated_reference_counterexample`; D14; `DEAD.5`).  *New here:* it is false for **every**
     positive correlation — for two binary sites with `P(x₁ = x₂) = (1+ρ)/2` the exact supremum
     of the gap over the class is `(1 + ρ)` times the product width as `β → 0` (S2(A1), (A3);
     `ρ = 0.01` already violates it at `β = 0.1`), and for a chain of 16 sites with `ρ = 0.6` the
     additive residual exceeds it by the factor `3.4`, approaching the structure factor
     `(1+ρ)/(1−ρ) = 4` (S2(B)).  There is no threshold of weak dependence.  Quantitative
     substitutes, in increasing generality: (i) a **mixture of `K` product measures** (a
     multimodal reference): `ln Σ_k w_k e^{−βm_k} ≤ ln(Z/Z₀) ≤ ln Σ_k w_k e^{−βm_k} + β²Σc_i²/8`
     with the `K` component averages `m_k` — the same width, `K` linear functionals instead of
     one (apply (a), (c) to each component; S2(D); not in the report); (ii) Markov or Dobrushin
     references: `‖Γc‖²` with a Wasserstein matrix (**[K]**, line 479–481; not formalised; an
     upper bound in the two-site family, S2(A)); (iii) any reference: `(Σc_i)²` (**[V]**
     `bounded_differences_sandwich_any_reference`).
   * **{F}** (d) product reference.  For dependent references the extremal residual need not be
     additive: two ternary sites (D25, `DEAD.9`); binary pairwise models and binary Markov trees
     (D41).  **{F}** "moment generating function, not tails" (D8, **[K]**).
   * **{F}** one fixed `β` — for the equivalence with a transport inequality, which needs all
     `β ∈ ℝ` (D27, `DEAD.8`); Theorem 11.14 is the fixed-`β` statement.
   * **{C}** finite alphabets and finitely many sites (McDiarmid's argument is measure-theoretic).
   * **{Q}** exact knowledge of `⟨Δ⟩₀` — replaced by a sample mean in Theorem 11.21.
4. **Generalises.**  Theorem 11.14 (every reference, transport form), 11.21 (sampled), 11.25(b)
   and 11.28 (exact constants; two references; one reference for a whole class), §11.30 (box
   classes; reader AA2).  Not covered: sharp constants for dependent references (§12 item 5);
   open chains without tilt remain **{?}** (D41: no counterexample).
5. **Computational reading.**  The width is extensive.  The report's own number (line 505–508):
   `c_i = 0.5` kcal/mol on 100 torsions at 298 K gives ≈ 5 kcal/mol (`8.9 k_BT`; trivial width
   `84 k_BT`).  For an arbitrary reference the machine-checked width `β²(Σc_i)²/8` is `888 k_BT`
   in the same example — **worse than the trivial bound whenever `βΣc_i > 8`**.  The sandwich
   certifies free energies only for `βc_i ≪ n^{−1/2}` or cell by cell.
6. **Overstatement check.**  Rows and §3.2 carry the product hypothesis.  It is **dropped at line
   2171–2174** (§11.6: "One reference average … pins `ln Z` to within `β²Σc_i²/8` (Theorem 3.1),
   and `N` random evaluations estimate it … independently of the size of the state space") —
   neither the width nor the concentration holds for a dependent reference (S2(A), (C)); this is
   the slip that D14 records.  Stale: line 501–503 (§8, Err-2).

### E8. §3.4 — the partition-function kernel and the voxel enclosure (rows D3, D4)

1. **Statement.**  `zverify` returns a rational interval that contains `Z` over a box
   (`zverify_sound`, `zverifyTop_sound`); rational brackets of the Boltzmann factors and of the
   cell volumes give a two-sided bound on the continuous Boltzmann integral for pairwise torsion
   energies on product voxels (`certified_torsion_partition`); separable envelopes factor a voxel
   integral (`separable_voxel_bounds`).  **[V]**; the Taylor step that produces separable
   envelopes from a Hessian sandwich is **[P]**; refereed (R1 items 4, 7; D18, D22).
2. **Setting.**  Rational pairwise weight instances on `n` sites with `k` states; boxes; for the
   voxel bridge a product measure `⊗ν_i` on the torsion coordinates, measurable cells of finite
   measure, a pairwise energy, and real tables that enclose the energy terms on the cells.
3. **Assumptions.**
   * **{F}** nonnegative factors.  `negativeW_unguarded`: the bare checker returns an interval
     that misses `Z`.  Checked by `zverifyTop`, so not an assumption of the top-level theorem.
   * **{X}** the rule set leaf / branch / thermal prune.  With it an exact enclosure of a
     two-state chain needs `2ⁿ` leaves where a transfer matrix needs `O(nk²)` operations (line
     538–546; D22); repaired by the cut and elimination rules (E32).
   * **{P}** pairwise energy, in the voxel bridge.  `voxel_boltzmann_bounds` holds for any
     measurable energy with bounds on a voxel; the end-to-end theorem is written for pairwise
     tables.
   * **{E}** product reference measure and product voxels — for the factorisation (Fubini).  A
     non-product base measure (a Jacobian that couples coordinates) is not covered.
   * **{E}** table enclosures of the energy terms on the cells — an *input* (interval
     evaluation is outside the development, line 587–588); cells on which the energy is
     unbounded must be removed from the domain.
   * **{C}** the scalar Hessian sandwich `m·I ⪯ ∇²E ⪯ M·I` (it discards off-diagonal terms to
     keep the envelopes separable; a third-order enclosure would need `ε^{−d/3}` voxels, line
     621–626).  **{C}** only the base chart of the circle atlas is formalised.
4. **Generalises.**  §11.8 (cut, elimination).  Not covered: non-pairwise energies end to end,
   non-product base measures, the enclosures of the tables themselves.
5. **Computational reading.**  The report's count (line 616–617): accuracy `1+ε` needs
   `N ≈ vol·(β(M−m)d/(8 ln(1+ε)))^{d/2}` voxels.  For `d = 10` coupled torsions, `β(M−m) = 10`,
   `ε = 0.1` this is `4·10¹⁰` voxels per unit volume, `4·10¹⁸` on the full torus: **vacuous beyond
   a handful of coupled continuous coordinates**, as the factor `d^{d/2}` announces.  The
   zeroth-order bound is worse.
6. **Overstatement check.**  Row D4 (line 56) lists "separable (second-order) envelopes" with
   **[V]** only; the step from a Hessian bound to separable envelopes is **[P]** (line 602, 612).
   Minor label.  §3.4 itself states its limits.

### E9. §3.5 — Hölder decomposition (row D5)

1. **Statement.**  `Z_β(E₁+E₂) ≤ Z_{β/ρ}(E₁)^ρ Z_{β/(1−ρ)}(E₂)^{1−ρ}`.  **[V]**; known (weighted
   mini-bucket).
2. **Setting.**  Any finite set, any two functions, `ρ ∈ (0,1)`.
3. **Assumptions.**  None beyond the setting (general).  **{E}** one-sidedness: Hölder gives an
   upper bound on `Z` only; there is no two-sided rule of this kind (D17), which is why the
   kernel uses cut bounds instead.
4. **Generalises.**  The tropical `sum` rule is its limit `β → ∞`.
5. **Computational reading.**  A bound, not a kernel rule; the parts are evaluated at colder
   temperatures.  Looseness not quantified in the report.
6. **Overstatement check.**  None (D17 applied: §0.1 item 3 says "one-sided").

### E10. Lemma 4.1, Theorems 4.2, 4.3 — the trace-enhanced spectral obstruction (rows C1, C2)

1. **Statement.**  `‖D̂ − Δ(Y)‖_F² ≥ 4Σ_{k>r}λ_k² + (4/(r+1))(Σ_{k>r}λ_k)²` for every `Y ∈ ℝ^{L×r}`.
   **[V]** down to Hoffman–Wielandt; refereed (R1 item 9).  Known with these constants
   (Sonthalia et al. 2021).
2. **Setting.**  A complete hollow symmetric matrix of *squared* distances between `L` points;
   unweighted Frobenius norm; target dimension `r`.
3. **Assumptions.**
   * **{E}** complete, unweighted data.  The K-identity is an identity for the full operator;
     certificates for weighted or incomplete data with bond-length constraints "were not found
     … and are not provided here" (line 729–732).
   * **{E}** squared distances (the Gram matrix is linear in them).
   * **{Q}** `λ_r(Ĝ) ≥ 0`.  Otherwise the bound holds and is strictly weaker than the cited one:
     `D̂ = −2(11ᵀ − I)`, `L = 4`, `r = 3`: `5` here, `21` there, optimum `48` (line 689–691;
     arithmetic re-checked by hand).
   * **{F}** for equality: "vertex-transitive input" is not enough (regular simplex `L = 5`,
     `r = 3`: bound `1.25`, minimum `1.304`; D12, `DEAD.4`); and the two-sided `O(√L)` statement
     needs the trace-shifted solution to be positive semidefinite (line 724–728: ratio² `9.6 > 3`).
   * **{C}** exact eigenvalues (certified enclosures are outside Lean, §8).
4. **Generalises.**  Nothing later in the report.  Chirality is invisible to distances (line
   745–746) — inherent, not an assumption.
5. **Computational reading.**  One `O(L³)` eigen-decomposition.  Gain over the strain bound
   `√L/2` under a uniform bias, none for zero-mean noise (D5).
6. **Overstatement check.**  None found (the section title says "known; formalized").

### E11. Theorems 4.4, 4.5 — holonomy obstructions (row C3)

1. **Statement.**  The holonomy of measured edge transforms bounds the total edge error of any
   frame assignment; for SE(3) a translation holonomy with lever arms.  **[V]**; the triangle
   bound is known (Lerman–Shi).
2. **Setting.**  A group with a conjugation-invariant norm; a closed cycle.
3. **Assumptions.**  **{E}** conjugation invariance of the norm (SE(3) has no bi-invariant
   metric, whence Theorem 4.5).  **{E}** a closed cycle.  **{Q}** the `ℓ¹` accumulation
   (`‖hol‖² ≤ mΣ‖err_k‖²`): sharp for coherent errors, loose by `√m` for independent ones.
4. **Generalises.**  A sharp non-abelian Hodge-type bound is open (line 779).
5. **Computational reading.**  A cheap necessary condition; no completeness.
6. **Overstatement check.**  None.

### E12. Theorem 4.6 and Corollary 4.7 — torsion moves and superposition; the envelope of an invariant residual (row C4)

1. **Statement.**  A torsion move by `δ` changes the superposed configuration by at most
   `2√(min(I_A, I_B))|sin(δ/2)|`; moves chain additively; a `G`-invariant, `Λ`-Lipschitz residual
   therefore has bounded differences `c_i = Λ·2√(2Ī_i)` and belongs to the kernel's residual
   class.  **[V]** for any group `G` containing the axis rotations; the identification with
   `SE(3)` is **[P]** (the group is not defined in Lean; D16, D19).  Refereed (R1 item 11).
2. **Setting.**  Point configurations with unit masses; rigid arms on both sides of the axis; a
   uniform bound `Ī_i` on the inertia over the conformations considered.
3. **Assumptions.**
   * **{E}** rigid arms (ideal geometry during a move) and `G ∋` axis rotations.
   * **{E}** invariance and a Cartesian Lipschitz constant `Λ` of the residual, and the bound
     `Ī_i` — all three are inputs ("a modelling input", line 843–844).
   * **{P}** the `ℓ¹` chain rule and the coaxial superposition: the coaxial optimum is not the
     Kabsch optimum (ratio down to `0.2`, D9) and independent errors accumulate like `√m`, not
     `m` (D10).  A sharper metric (Eckart frame) is open (line 864–865).
   * **{C}** unit masses.
   * **{Q}** — with a consequence for everything downstream: the constants are not bounded.
     `Ī_i` grows like `m³` on domains with extended arms (Theorem 11.36) and at least like `m` on
     *every* torsion domain (new, S6(c): among three consecutive atoms one is at distance
     `≥ ½b cos(θ/2)` from any line, so `I ≥ 0.0267·m b²` and `c_i ≥ 0.33·Λ b m_i^{1/2}`).
4. **Generalises.**  §11.14 draws the consequences; §11.17 (reader AA2) leaves the format.
5. **Computational reading.**  As a displacement bound: within `√2` of the obvious baseline (line
   822–825).  As a source of envelope constants for chains: **vacuous for long chains** — at
   fixed `Λ` only `O(N^{1/3})` torsions near the ends are sharp and certification in this format
   costs `k^{n−o(n)}` (Theorem 11.37; §8 line 1178–1184).
6. **Overstatement check.**  Row C4 (line 61) carries **[V]** for a sentence that names `SE(3)`;
   and neither the row nor §4.4 says that the envelope it "turns … into" (line 841–843) is
   useless beyond short chains — that is said only in §8 and §11.14.  Minor.

### E13. §5 — outward rounding, certified exponential, rational atlas (row B1)

1. **Statement.**  Rational interval arithmetic with containment theorems; `expLo ≤ exp ≤ expHi`;
   every unit vector is a quarter turn of a rational point with `|t| ≤ 1/2`.  **[V]**.
2. **Setting.**  Rational arithmetic; `|q| ≤ 2^k` for the exponential; `0 < lo` for inverses.
3. **Assumptions.**  **{C}** rational chart endpoints and bond geometries (irrational ones need
   enclosures, line 892–895).  **{E}** a certified positive lower bound on `r²` for
   Lennard-Jones poles.
4. **Generalises / not covered.**  Infrastructure; verified interval evaluation of the energy
   terms over cells is not built (§6.4, last paragraph).
5. **Computational reading.**  Sound; the growth of rational bit sizes along a certificate is not
   measured anywhere in the report.
6. **Overstatement check.**  None ("every ingredient is standard", line 895).

### E14. §6.1 — Master Soundness Theorems (row E1)

1. **Statement.**  An accepted certificate bounds the energy on the box (`verify_sound`); for the
   residual kernel, for **every** residual of the class consistent with interval anchor data,
   and the kernel decides that the class is non-empty (`verifyITop_sound`,
   `IProblem.consistent_iff_nonempty`); for partition functions `zverifyTop_sound`.  **[V]**;
   refereed (R1; internal audit D15, D19).
2. **Setting.**  Rational pairwise instances, box domains, certificate trees
   (leaf / branch / prune / sum); residual class = bounded differences `c_i` plus anchors.
3. **Assumptions.**
   * **{F}** consistency of the published data, if it is not checked: the bound `41/4` is
     accepted on a problem whose minimum is `1` (`inconsistentResidual_unguarded`; D15).  The
     top-level kernel checks it.
   * **{C}** pairwise instances and box domains (no 3-body rule; non-product domains only by
     branching).  **{C}** the weighted-Hamming residual class (the second-order and third-order
     reductions feed the same kernel, `verify_sound_secondOrder`, `verify_sound_thirdOrder`;
     linear classes have their own kernel, §11.17).
   * **{Q}** exact tables: real energies are handled by termwise lower instances
     (`verify_sound_real`; `verify_sound_real_symm` for instances that store each pair once).
   * **{E}** the constants `c_i` are inputs (§8 line 1143–1145): no first-order constant is
     certified for a concrete residual anywhere in the repository.
4. **Generalises / not covered.**  No kernel for probabilistic certificates (§11.9, §12 item 8);
   no certificate producer; evaluation inside the Lean kernel does not scale (512 table entries
   exhausted 11.9 GB, line 2476–2478; a purpose-built integer leaf check runs on 147 456 entries
   but its refinement theorem is not written, line 2484–2486).
5. **Computational reading.**  Checking is linear in the certificate; the certificate is
   exponential in general (E15, E19).  At present an accepted certificate of realistic size is
   the output of a compiled checker with `verify_sound` as specification, not a kernel theorem —
   the report says so (line 2484–2486).
6. **Overstatement check.**  None found; the novelty column was rewritten after SCI-REV-0006.

### E15. Theorem 6.1 — the decomposition rule is necessary relative to pairwise-LP leaves (row E2)

1. **Statement.**  On `m` disjoint frustrated triangles every accepted certificate without `sum`
   visits `≥ 2^m` leaves for the bound `m` (`2^{m−d}` for `m − d`); with `sum`, `2m` leaves;
   also for node count and description length.  **[V]**; refereed (R1 item 12).  Known
   phenomenon (Jeroslow; Basu et al.).
2. **Setting.**  The tropical kernel with LP-dual leaves, branch and DEE; tree-like certificates.
3. **Assumptions.**
   * **{F}** the leaf rule is the pairwise (local-polytope) LP.  A leaf with triplet consistency
     certifies `m` triangles at once (line 982–984), so "necessary" is relative to the rule set.
   * **{P}{?}** a disconnected family.  For connected families the report has no exponential
     lower bound: a ring family needs linear depth (the Scientific Discovery Division's
     Proposition P7.5, not re-derived), and "a connected family with a unique minimiser whose
     `sum`-free certificates need exponentially many leaves" is open (§12 item 6).
   * **{E}** tree-like certificates (no sharing of sub-certificates).
4. **Generalises.**  `chain_separation` (E32) is the finite-temperature counterpart on a
   connected family, for exact lower endpoints.
5. **Computational reading.**  The separation is real and cheap to realise (`4m − 1` nodes
   against `2^m`).
6. **Overstatement check.**  Row E2 (line 64) says "on `m` frustrated triangles" without
   "disjoint" and without "relative to pairwise-LP leaves"; the section title (line 979) has
   both.  Minor.

## 2. Entries, part II — §§11.1–11.9 (certification geometry; rows G1–G10)

Status of the part: machine-checked cores; refereed by R2 at commit `ee2053f`, i.e. Theorems
11.1–11.21 as they then stood (one paper theorem false as stated, four overstatements, all
corrected: D29–D33).  Theorem 11.18a and Propositions 11.18b–f were added later and reviewed by the
Scientific Discovery Division (SCI-REV-0012, -0013, -0015), in part not at all (see E28, E31).
Setting of the part (line 1739–1743): `X` finite, `d` an envelope, `f` known, `g` an unknown
admissible residual; a procedure evaluates `g` exactly at points of its choice; **the cost is the
number of evaluations** — computation, and everything that is known about `f`, is free.

### E16. Theorems 11.1, 11.2 — conditional envelope; anchored sharp minimum; worst-case regret (row G2)

1. **Statement.**  After evaluations on `A` the largest value of `g(x) − g(y)` over consistent
   residuals is `D_A(x,y) = min(d(x,y), U(x) − L(y))`; `x` is optimal for every consistent
   residual iff `D_A(x,y) ≤ f(y) − f(x) ∀y`; the worst regret is `max_y[f(x) − f(y) + D_A(x,y)]`.
   **[V]**; refereed (R2).  Known (minimal simple temporal network).
2. **Setting.**  Arbitrary `X` (`ConditionalEnvelope.lean` has no finiteness), finite `A`,
   consistent exact values.
3. **Assumptions.**  **{E}** consistent values (E4).  **{Q}** exact values (intervals: the
   ground-node construction of §11.1).  **{C}** the triangle inequality (E3).  Nothing else.
4. **Generalises.**  It *is* the general statement for first-order classes.  Finite temperature:
   `gibbsProb_range_with_anchors_eq`.
5. **Computational reading.**  The regret is a maximum over `y` of a function that contains
   `min_a` and `max_a` over the anchors: a `max–min` problem over pairwise models, hard in
   general (§8 line 1170–1173).
6. **Overstatement check.**  None ("known mathematics" is in the section title).

### E17. Theorems 11.3–11.5 — slack geometry; certificates are coverings; three notions, one number (row G1)

1. **Statement.**  `s(a,y) = d(a,y) − g(a) + g(y)` is an envelope; `A` is a point
   `ε`-certificate iff every `y` has an evaluated point within slack `E(y) − UB(A) + ε`;
   `N_cov ≤ N_value = N_point ≤ N_cov + 1`, `N_point = max(1, N_config)`.  **[V]**
   (`isCertificate_iff_cover`, `value_exchange`, `config_exchange`); refereed (R2, whose exchange
   lemmas sharpened 11.5).  A reformulation of a known notion.
2. **Setting.**  Any finite `X`, any envelope (asymmetric allowed), any known part, any admissible
   residual.  No product structure.
3. **Assumptions.**
   * **{E}** the class is the first-order (difference-constraint) class: "the uncertainty … does
     not combine across evaluations — it is their minimum" (line 1806–1807) is a property of that
     class.  **{F}** in other classes: in a second-order class one star determines the additive
     part (Theorem 11.16); in a linear class rank-many evaluations determine everything (§11.17);
     in a Hilbert ball evaluations combine linearly (Proposition 11.50a).
   * **{Q}** exact evaluations.  With an evaluation error bounded by `τ` the envelopes become
     `L_A − τ`, `U_A + τ`; every radius shrinks by `2τ` and nothing is certified below `ε = 2τ`
     (immediate from Theorem 11.3; not stated in the report, which assumes exactness throughout
     and says so at lines 3077–3078 and 3693 only).
   * **{P}** finite `X` (minima are attained).  On a compact metric space the covering picture is
     the known one (Bachoc et al., for `f ≡ 0`).
   * `κ` enters only through `s ≥ (1−κ)d`.
4. **Generalises.**  Theorem 11.23(a): the same number is the instance-wise deterministic query
   complexity.  Normal form: Theorem 11.29.
5. **Computational reading.**  A characterisation, exact for every instance.  Its value is
   decided by the size of `N_cov` (E19, E25) and by the fact that finding or even checking a small
   cover is hard (E20; §8 line 1167–1173).
6. **Overstatement check.**  None.

### E18. Theorem 11.6 — dual lower bounds (row G3)

1. **Statement.**  Weak LP duality for the covering: weights, forced points, fooling sets, volume,
   exponential weights `e^{−tε}Σ_y v(y) ≤ |A|·max_a Σ_y v(y)e^{−t(s(a,y) − gap(y))}`, and the
   partition-function form.  **[V]**; refereed (R2).  Tools known (Csiszár's dual bound).
2. **Setting.**  Any finite instance.
3. **Assumptions.**  None beyond E17 — general.  The Hamming form `partition_bound_hamming` uses
   a weighted Hamming envelope and a `κ`-Lipschitz residual (**{C}**).
4. **Generalises.**  Tensorises (Theorem 11.8); thermal version Theorem 11.13(c); for every
   algorithm Theorem 11.23(b).
5. **Computational reading.**  All bounds are at most `N_frac`, and
   `N_frac ≤ N_cov ≤ (1 + ln max|S|)N_frac` (**[K]**): tight to a logarithm in general, exponentially tight on
   products.  Evaluating them needs sums over `X` — a transfer matrix for chain known parts, an
   intractable sum in general.
6. **Overstatement check.**  None.

### E19. Theorems 11.7, 11.8, 11.9 — product landscapes: one evaluation, an exponential lower bound, the exact exponent (row G4)

1. **Statement.**  On a product space with additive `f`, weighted Hamming envelope and additive
   residual: the single evaluation at `x₀` is an exact certificate iff every site is sharp
   (`c_i ≤ φ_i(s) − φ_i(x₀_i)`); `ln|A| ≥ Σ_i r_i(t; v_i) − tε` for every certificate and every
   common `t`; for finitely many site types and `ε = o(n)`,
   `ln N_cov = max_t Σ_i max_v r_i(t;v) + o(n)`, and `R* = 0` iff the site is sharp.  11.7, 11.8 **[V]** for every `n` and arbitrary
   sites (`product_single_certificate_iff`, `product_exp_weights`); the qualitative dichotomy
   **[V]** only for identical sites, zero residual, `ε = 0`
   (`homogeneous_certificate_dichotomy`); the upper bound of 11.9 **[P + K]** (type covering; the
   heterogeneous case by an argument of the second referee).  Refereed (R2); R3 did not check
   the type-covering step (its §6).
2. **Setting.**  `X = ∏σ_i`, `f = Σφ_i`, `d = Σc_i[x_i ≠ y_i]`, `g = Σγ_i` with
   `|γ_i(a) − γ_i(b)| ≤ κc_i`, `κ < 1`, `c_i > 0`; point certificates of the minimum.
3. **Assumptions.**
   * 11.7 itself needs none of this: `d(x₀,y) ≤ f(y) − f(x₀) + ε ∀y` characterises the single
     evaluation "for every residual and every envelope" (`single_evaluation_certificate_iff`
     **[V]**, line 1897–1899) — general.
   * **{E}{X}** independent sites (product space, additive known part, site-additive envelope) —
     for the single-letter exponent.  With a nearest-neighbour known part the exponent is
     `sup_ν R_ν(e(ν))` over stationary processes and the Boltzmann-weight formula vanishes on a
     window where the true cost is exponential (Theorem 11.40, Proposition 11.41).  With the
     RMSD envelope of a chain in place of its weighted-Hamming relaxation the cost at the same
     instance drops from `exp(Θ(N))` to `exp(Θ̃(√N))` (Theorem 11.38).  So the exponential law is
     a property of this geometry, not of first-order envelopes as such.
   * **{F}** `κ < 1`, for "`R* = 0` iff sharp".  The report's example (line 1953–1954):
     `φ = (0,0)`, `γ = (0,c)`: not sharp, `N_cov = 1` (S3(D)).
   * **{Q}{F}** finitely many site types, *fixed as `n` grows*.  The lower bound
     `exp(Σ_i r_i − tε)` is valid for every `n`; it is exponential in the number of non-sharp
     sites only if the `r_i` stay bounded away from zero.  **New:** `n` two-state sites,
     excitation energy `e`, constants `c = e(1+δ)`, zero residual, `ε = 0`: every site is
     non-sharp, and for `δ < 1/n` the smallest certificate has **exactly `n + 1` points** (the
     ground state and the `n` single excitations, each covered only by itself, cover everything;
     exhaustive for `n ≤ 12`, S3(A)).  In general the exponent of a two-state site is
     `R*(δ) = (0.2785 + o(1))·δ` as `δ → 0` (S3(B)): super-polynomial growth needs
     `nδ ≫ ln n`.  The substitute for "non-sharp ⟹ exponential" is therefore the quantitative
     bound itself, with the margins `c_i/e_i − 1` in it.
   * **{F}** a *common* slope `t`: maximising site by site overshoots (`0.3765` against `0.2329`,
     D31, `DEAD.12`; re-computed in S5).  **{F}** Boltzmann weights beyond two-state sites with
     zero residual (D31; S5).
   * **{?}** an additive residual.  For a non-additive residual the one-shot bound (Theorem
     11.6) holds and no exponent is known (§12 item 2(a)).
   * **{Q}** `ε = o(n)`; `ε = 0` is allowed.  At extensive accuracy the lower bound keeps its
     term `−tε₁`; a matching upper bound is not stated (the zero-temperature sandwich of Theorem
     11.28(iii) gives the accuracy `(c² − e²)₊/(2c)` per site above which a bounded number of
     random evaluations suffices).
4. **Generalises.**  To every algorithm, deterministic or randomised (Theorem 11.23); to chain
   known parts (Theorems 11.39–11.40); for `ln Z` to several site types and alphabets (§11.26,
   reader AA2).  Not covered: non-additive instances, known parts with interactions beyond
   nearest-neighbour chains and functions of the type, non-product domains (excluded pairs),
   continuous sites.
5. **Computational reading.**  At `e/c = 1/2` the exponent is `0.188` per site: `1.5·10⁸`
   evaluations at `n = 100`.  For nearly sharp sites it is small: with a margin of 1 % a
   thousand-fold certificate needs about 2 500 sites (S3(B)).  The theorem is a no-go result with
   an explicit rate; the rate, not the word "exponential", is the information.
6. **Overstatement check.**  The unqualified dichotomy is stated five times without the
   hypotheses that make it true (additive residual with `κ < 1`; site types fixed as `n` grows):
   `README.md` 117–119 ("on product landscapes one evaluation suffices iff every site is sharp;
   otherwise the number is exponential in the number of non-sharp sites"); report 1082–1084
   ("one evaluation if every site is sharp and exponentially many otherwise"); row G4, line
   1496; line 1966–1969 ("in general by the paper proof above" — the paper proof is for
   finitely many types); line 2998–3001 (see E26).  Inside Theorem 11.9 the bold sentence (line
   1921–1923) is covered by the theorem's hypotheses.

### E20. Theorem 11.10 — minimal certificates contain dominating sets (row G5)

1. **Statement.**  On a 0/1/2-distance gadget the exact certificates are `{o} ∪` a dominating
   set; computing a minimal certificate is NP-hard and hard to approximate within
   `(1−o(1))ln|X|`.  Gadget **[V]**; complexity reading **[K]**; no instance-optimal algorithm
   **[P]** (hub family).  Refereed (R2).  Known for metric search (Hetland 2020).
2. **Setting.**  An explicitly tabulated finite metric space; `g ≡ 0`.
3. **Assumptions.**  **{C}** explicit input (on succinct product spaces even *checking* a
   certificate is coNP-hard, §12 item 3).  **{P}** the adversary argument is for deterministic
   procedures; the randomised version is the bound `((1−2δ)²/8)min(M,N)` of Theorem 11.23(iii),
   **[P]** (R3, Appendix B).
4. **Generalises.**  —
5. **Computational reading.**  Says that the certificate size `N_cov` is not a cost any single
   algorithm attains: on the hub family `N_cov = 2` and every algorithm pays `Ω(min(M, N))`.
6. **Overstatement check.**  None.

### E21. Theorem 11.11 — best-first search with resource augmentation (row G6)

1. **Statement.**  For symmetric `d` and a `κ`-Lipschitz residual, `κ < 1`, best-first search
   stops after at most `|C| + 1` evaluations for every cover `C` at the shrunk radii
   `θ(gap + ε/6)`, `θ = (1−κ)/(4(1+κ))`.  **[V]** (`bestFirst_card_le`); refereed (R2).
2. **Setting.**  Any finite instance; the comparison is with covers at radii shrunk by `θ ≤ 1/4`.
3. **Assumptions.**
   * **{Q}** symmetric `d` — a `ρ`-quasi-symmetric slack with `θρ ≤ 1/4` suffices
     (`bestFirst_card_le_of_quasiSymm`).
   * **{Q}** `κ < 1` — at `κ = 1` the radius is zero and the theorem is empty; Proposition 11.30
     covers `κ = 1` under another hypothesis.
   * **{F}** the shrunk radii.  Against `N_cov` itself the statement is false: hub family, 17
     evaluations against a certificate of 2 (D26, `DEAD.6`, XI.4).
   * **{P}** the constants `θ`, `ε/6` (not tight; the referee found no violation at `2θ`).
   * **{F}** for the conversion "shrunk cover ≈ constant × `N_cov`": false with a known part,
     even on the line (`N_cov = 1`, shrunk covers `m + 1`; D30, `DEAD.11`).  **{?}** for
     `f ≡ 0` (a conjecture, §12 item 2).
4. **Generalises.**  Proposition 11.30 (centre form, `κ = 1`).
5. **Computational reading.**  With a known part the comparison class can be unboundedly larger
   than `N_cov`, so as a competitive guarantee the theorem is **vacuous with respect to the
   certificate size**; on random instances the shrunk covers have 8–10 points against a smallest
   cover of 2–2.4 (line 2031–2035).
6. **Overstatement check.**  None remaining (D30).

### E22. Theorem 11.12 — thermal contact

1. **Statement.**  Over the class the Gibbs probability of a state ranges exactly over an interval
   whose ends are attained by `−d(x,·)` and `d(·,x)`.  **[V]**; refereed (R2).
2. **Setting.**  Any finite instance, `β ≥ 0`.
3. **Assumptions.**  None beyond the envelope class.  **{E}** a single state: for other
   observables the robust average is a linear-fractional programme with no closed form (line
   2052–2054); ratios of macrostate weights are §11.28 (reader AA2).
4.–6. Exact; cheap for one state (`2` partition sums of modified landscapes); no overstatement.

### E23. Theorem 11.13 — free-energy certificates are quantizers

1. **Statement.**  `Z(f+L_A)/Z = E_π e^{βs(A,Y)}`; if this is at most `e^ε` then the mean slack
   is `≤ ε/β`, `H(π) ≤ ln|A| + ln max_a Σ_y e^{−ts(a,y)} + tε/β`, and a Hölder converse holds.
   **[V]** (`card_ge_entropy`, `thermal_exp_weights`); refereed (R2).
2. **Setting.**  Any finite instance, `β > 0`; no product structure.
3. **Assumptions.**  **{C}** the hypothesis is one-sided and involves the true `Z` (line
   2113–2116) — weaker than a two-sided certificate, which strengthens the lower bound.
   **{E}** deterministic certificates built from pointwise evaluations: randomised algorithms
   pay less (Theorems 11.24–11.26; E33).
4. **Generalises.**  Tensorises (`thermal_product_exp_weights`); every deterministic algorithm
   (Theorem 11.24(c)).
5. **Computational reading.**  At least `exp(entropy)` evaluations up to a slack-ball factor: at
   any temperature at which the ensemble has entropy, deterministic pointwise certification of
   `ln Z` to sub-extensive accuracy is out of reach.
6. **Overstatement check.**  None.

### E24. Theorem 11.14 — transport–entropy duality at fixed `β`

1. **Statement.**  `ln E_μ e^{β(g − E_μ g)} = β(E_ν g − E_μ g) − KL(ν‖μ) ≤ βΣγd − KL(ν‖μ)` for
   every coupling.  **[V]**; the converse (Donsker–Varadhan) **[K]**.  Refereed (R2).
2. **Setting.**  Any finite instance, any reference, `β ≥ 0`.
3. **Assumptions.**  **{F}** `β ≥ 0` and the orientation of the coupling for asymmetric
   envelopes ("every `β`" was wrong, R2).  **{F}** one `β` does not give the transport
   inequality (D27).
4.–6. General; the "unification" paragraph (line 2092–2095) is accurate; no overstatement.

### E25. Theorem 11.15 — the exact exponent at finite temperature (row G7)

1. **Statement.**  For `n` identical independent sites and accuracies with `ε_n = o(n)` **and**
   `ln(1/ε_n) = o(n)`: `n⁻¹ ln N_Z → R_β = max_Q R(Q; s, KL(Q‖π)/β) ≥ H(π)`.  Lower bound **[V]**
   for every `n`; upper bound **[P]**, a corollary of an example in Merhav 2011.  Refereed (R2:
   false as first stated, D29; R3 checked the corrected proof "for internal consistency only").
2. **Setting.**  As E19 with identical sites; two-sided certificates of `ln Z` by pointwise
   evaluations; slack positive off the diagonal.
3. **Assumptions.**
   * **{F}** `ln(1/ε_n) = o(n)`.  For `ε = 0` the certificate is the whole space
     (`exact_free_energy_certificate_eq_univ` **[V]**), and `R_β < ln k` (D29).  For
     `ε = e^{−λn}` only a bracket is known — **{?}** (§12 item 1(c′)).
   * **{Q}** `ε_n = o(n)`: at extensive accuracy the entropy bound of Theorem 11.13(b) applies
     with its term `−tε₁/β` (line 2174–2177).
   * **{P}{?}** identical sites.  The lower bound tensorises for arbitrary sites; an upper bound
     for several site types is not stated here (for `ln Z` and randomised algorithms it is
     §11.26, reader AA2).  Interacting known parts: "the finite-temperature exponents of a
     chain" are open (§12 item 1).
   * **{E}** slack positive off the diagonal (`κ < 1`, `c > 0`): type classes at distortion zero
     are evaluated entirely.
   * **{?}** an additive instance.
   * **{X}** deterministic.  Randomised algorithms have a strictly smaller exponent at the same
     instance (machine-checked on the cube: about `(2/(1+e^{−βc}))ⁿ` against almost `2ⁿ`;
     Theorem 11.26).
4. **Generalises.**  Theorem 11.24(c) (every deterministic algorithm); the table at line
   3288–3292 (three budgets).
5. **Computational reading.**  A no-go result: for the report's sharp site (`e/c = 2`,
   `β = ln 2`) the exponent is `0.514` per site (re-computed, S5): `10¹¹` evaluations at
   `n = 50`.
6. **Overstatement check.**  Row G7 (line 1499) states the exponent "for accuracies that are not
   exponentially small" without "identical independent sites" and "an additive instance".
   Minor.

### E26. Theorems 11.16, 11.17 — the star sandwich and its exactness (row G8)

1. **Statement.**  If all mixed second differences of `g` are bounded by symmetric `c_ij`, then
   `|g − g_star| ≤ Σ_{i<j changed} c_ij`, `g_star` the additive interpolant of the `n(k−1)+1`
   star values; the two bounds are members of the class, so the robust problem is exactly a
   pairwise problem and `x₀` is certified iff it minimises its lower pairwise model.  **[V]**
   (`secondOrder_remainder`, `secondOrder_envelope_exact`,
   `secondOrder_certified_minimizer_iff`); refereed (R2: "the way out" overstated, D32).
2. **Setting.**  A full product domain, one reference configuration, constants valid at all base
   points, exact star values, **no bound on the first-order terms** (the class is closed under
   adding additive functions).
3. **Assumptions.**
   * **{F}{Q}** a product domain.  On `D = {00, 01, 11}` the class with any constants contains
     every function (Proposition 11.18c(c)); the bounds survive on *reset-closed* domains
     (11.18c(a), **[P]**; the Lean statements are for full products).
   * **{E}** one reference and its star.  **{F}** "several stars combine": a union of stars
     gives exactly the best single-star bound (`stars_do_not_combine` **[V]**).  An ensemble
     that is not concentrated near one reference therefore pays a covering number again
     (Theorem 11.32).
   * **{Q}{X}** weak coupling — not a hypothesis of the theorems but of their usefulness.  The
     star certifies iff no set of sites is over-dense (Proposition 11.18b); for dense constants
     `c_ij = c` the remainder is quadratic in the Hamming distance and the cost is
     `2^{n − Θ(√n log n)}` (Theorem 11.32(i)).
   * **{Q}** constants at all base points — constants at base points that agree with the
     reference on the pair suffice and can be strictly smaller for three or more states
     (Theorem 11.18d(b)).
   * **{C}** symmetric `c`; exact star values (interval values widen the one-body tables).
   * **{E}** the constants `c_ij` are inputs.  None is certified in this repository: "an
     interface without an instance" (§8 line 1174–1177); the measured ones are maxima over
     enumerated domains (line 2306–2313).  The one exception the report names is the Scientific
     Discovery Division's certificate for a twenty-residue instance, whose order-`m` constants
     are bounded on paper with interval arithmetic, "its code … unreviewed" (line 1272–1279;
     line 2702–2705: "not machine-checked and not checked by us").
4. **Generalises.**  Order `m` (Theorem 11.18), third order to pairwise models (11.18a), exact
   identities and anchored constants (11.18d), exclusions (11.18c); dense classes (§11.12);
   free energies (Theorem 11.33).
5. **Computational reading.**  `n(k−1)+1` evaluations, then a pairwise problem for the kernel.
   Useful under weak coupling only; with dense constants of order one the star certifies only
   when `e ≥ c(n−1)/2`.
6. **Overstatement check.**  Line 2998–3001 ("The resulting picture.  First-order envelope: …
   the price is exponential unless the known part is sharp (Theorems 11.4, 11.9, 11.15) — for
   every algorithm"): true on product landscapes with independent sites of fixed types and
   `κ < 1` (E19); at finite temperature the price is exponential *also* when the known part is
   sharp (Theorem 11.15, line 2108–2110), and for other envelope geometries it is not
   exponential (Theorem 11.38).  §7 line 1097 ("The kind of envelope matters more than its
   size") is conditional on weak coupling, as the next sentences say.

### E27. Theorems 11.18, 11.18a, 11.18d — order `m`; third order to pairwise models; the remainder as an identity

1. **Statement.**  If the mixed differences of order `m` are bounded by `c_T`, the anchored
   interpolant of order `m−1` (the Hamming ball of radius `m−1`) satisfies
   `|g − I_{m−1}g| ≤ Σ_{T ⊆ changed, |T| = m} c_T`; for `m = 3` every covering of the triples by
   site and pair penalties gives a pairwise lower model for the kernel; the remainder is an
   explicit sum of mixed differences at base points that agree with the reference on `T`
   (identity), also for down-closed families, for a separate order of the sites per term, and
   with shares of every level.  **[V]** (`higherOrder_remainder`, `thirdOrder_pairwise_lower`,
   `anchored_remainder_identity`, …); attainment for `m ≥ 3` with arbitrary ball data **[P]**
   (confirmed by linear programming for `m = 3`).  11.18 refereed (R2); 11.18a, 11.18d reviewed
   by the Scientific Discovery Division (SCI-REV-0012, -0013).
2. **Setting.**  Full product domains; one reference; the function evaluated exactly on a Hamming
   ball; constants as inputs.
3. **Assumptions.**
   * **{Q}** product domain → reset-closed domain (**[P]**, Proposition 11.18c).
   * **{Q}** uniform constants → anchored constants (11.18d(b)); equal for two states per site.
   * **{F}** "a term with `m + 1` hosts" in 11.18d(a″): for the triple coupling on three binary
     sites with `m = 2` the host-anchored constants are `0` and the remainder is `1`
     (`term_orders_sharp` **[V]**, XI.24).
   * **{E}** the penalties *cover* the triples (11.18a(b)); coverings that do not come from
     shares must be checked on all sets of sites (line 2285–2289).
   * **{E}** constants are inputs, as in E26.
4. **Generalises.**  11.18d is the general form (any function, any order).  Not covered: an
   a-priori bound on `c_T` without enumerating the domain (line 2311–2313; §12 item 10(a)).
5. **Computational reading.**  The ball has `Σ_{|U|<m}∏_{i∈U}(k_i − 1)` points — degree `m−1` in
   `n`: the Scientific Discovery Division's certificate at twenty residues used 9 921
   evaluations at order 4 (line 2669–2670).  Whether the bound is useful depends entirely on
   constants that are measured, not certified.
6. **Overstatement check.**  None found; "**The cost of the star depends on how the energy is
   split; that of the ball does not**" (line 2301–2302) is an identity (`I₂(g + p) = I₂g + p`).

### E28. Proposition 11.18b — share certificates

1. **Statement.**  (a) shares `c_ij ≤ s_ij + s_ji`, `Σ_j s_ij ≤ Δ_i` certify `x₀` (**[V]**);
   (b) for an additive known part on a product domain shares exist iff no set of sites is
   over-dense — one maximum flow (**[P]** from max-flow min-cut, cited from memory); (d) deficits
   for a pairwise known part (**[V]**, sufficient only); (e) state-dependent shares exist iff
   `x₀` solves the pairwise linear relaxation (soundness **[V]**, the duality **[P]**).
   Reviewed by the Scientific Discovery Division (SCI-REV-0012); **the duality statement of (e)
   is unrefereed** (research log, "Resume here": "no referee").
2. **Setting.**  That of E26 with measured single-site excitation energies `Δ_i`.
3. **Assumptions.**
   * **{F}** (b) a product domain: on a product minus one pair of states the criterion holds
     and no shares exist (11.18c(a); XI.21; D59).
   * **{F}** (b) an additive known part: for a pairwise known part shares of the deficits are
     not necessary (three reasons, line 2372–2377; XI.21).
   * **{F}** (e) completeness beyond the relaxation: with an integrality gap `x₀` minimises the
     model and no shares exist (three binary sites, line 2402–2406; XI.21).
4. **Generalises.**  Triples (11.18b(c)), every level (11.18d(c′)).
5. **Computational reading.**  Useful: `O(n²k²)` additions to check, one max-flow or one linear
   programme to find.  On the division's instances it certifies 106 of 110 (line 2434–2435) —
   with measured constants.
6. **Overstatement check.**  The bold sentence at line 2351–2353 is inside part (b), whose first
   words are "For an additive known part"; `README.md` 156–161 says "for independent known
   parts".  None.

### E29. Proposition 11.18c — domains with pairwise exclusions

1. **Statement.**  On a reset-closed domain the remainder bounds and the sufficient directions
   survive, completeness of shares does not; the largest reset-closed part of a domain with
   pairwise exclusions is explicit; connectivity is not the right condition.  **[P; N]** (XI.18);
   reviewed (SCI-REV-0012, which found the first version's completeness claim false, D59).
2.–3. **{E}** reset-closedness (the proofs evaluate `g` only at resets of `x`); **{F}**
   connectivity as a substitute (`D = {00, 01, 11}`).  Outside the reset-closed part the class is
   unbounded below at every point, for every order and all constants (line 2522–2526).
4. **Not covered.**  How many references a cover by reset-closed pieces needs (§12 item 10(e)).
5. **Computational reading.**  A warning with numbers: in 14 of the division's 40 non-product
   analyses the minimum of the clash-free domain is not in the pruned product that was
   certified (line 2546–2547).
6. **Overstatement check.**  None (corrected twice in place).

### E30. Proposition 11.18e — the Hamming ball is necessary for a deterministic certificate

1. **Statement.**  For a class closed under adding functions of order below `m`, every
   deterministic algorithm that returns a finite bound evaluates at least `N_ball` points on
   every input; for randomised algorithms and an unspecified width this is false; with a hint a
   wrong residual of order below `m` is refuted by `⌈k^{m−1}ln(1/δ)⌉` random evaluations.
   **[P]**; the core of the counter-algorithm **[V]** (`affine_half_large`); (b′)(ii) a
   conjecture.  Reviewed (SCI-REV-0013, -0015).
2. **Setting.**  Product domains; no a-priori bound on the terms of order below `m`.
3. **Assumptions.**
   * **{X}** no a-priori bound on the lower orders.  With such bounds "fewer evaluations may do,
     at the price of the exponents of §§11.9–11.20" (line 2844–2846) — not quantified.
   * **{F}** deterministic.  Five random evaluations at `δ = 0.05` return a valid (useless)
     bound where a deterministic algorithm needs `n + 1` (D60; XI.22).
   * **{?}** randomised algorithms with a bracket of *prescribed* width: conjectured
     `(1 − δ)N_ball − o(1)`; an outline exists for binary sites at order two (line 2802–2827).
4.–6. The count is a statement about deterministic certificates and the report says so (line
   2749–2751).  No overstatement.

### E31. Proposition 11.18f — the allocation of shares for a law

1. **Statement.**  The two ends of the bracket of `ln Z` are convex and concave in the
   allocation; to first order every constant should be charged to its least probable
   sub-pattern; the site allocations form the core of a convex game and the greedy vertex is
   first-order optimal (**[V]** `greedy_optimal`, the division's file).  **[P]**; reviewed in
   part (SCI-REV-0015); (c″) "beyond the parts the science division stated" is unrefereed
   (research log, "Resume here").
2.–3. **{E}** the law of the changed set under the evaluated model is known.  **{Q}** independent
   sites, for the closed forms; for other laws the best order is a search that contains a
   minimum-weight hitting-set problem (line 2886–2888, "not re-derived by us") — **{?}** as a
   complexity statement.
4.–6. Elementary convexity, nothing claimed new (line 2849–2850); the summary "in evaluations
   neither matters" (line 2976–2977) is the honest reading.  No overstatement.

### E32. Theorems 11.19, 11.20 — cut and elimination rules; separations (row G9)

1. **Statement.**  `Λ·Z_S·Z_{Sᶜ} ≤ Z ≤ Υ·Z_S·Z_{Sᶜ}` from bounds on the cut factors; a site with
   at most two neighbours is summed out exactly; for every chain with nonnegative factors `m`
   eliminations and one leaf give the exact partition sum; elementary certificates with an exact
   lower end need `k^{m+1}` leaves on positive rigid chains.  **[V]** (`zverify2_sound`,
   `zverify2Top_chainCert`, `chain_separation`); "exact on treewidth at most two" **[P]**.
   Refereed (R2: scope narrowed, D33).
2. **Setting.**  Rational pairwise weight instances.
3. **Assumptions.**
   * **{F}** nonnegative factors (E8).
   * **{X}** degree at most two for elimination.  Eliminating a site with three neighbours
     creates a three-body factor, outside the kernel; on general interaction graphs exact
     partition functions are #P-hard (**[K]**), and the report has no lower bound for
     certificates that *use* the decomposition rules (line 3049–3052) — **{?}**.
   * **{?}** "exact lower endpoint" in the separation: a certificate whose lower end is
     `(1 − 10⁻⁹)Z` is outside the theorem; a robust version is open (D33).
   * **{F}** `Rigid` as a property of the model: it is a property of the representation
     (`gauge_trivial_separation` **[V]**: two independent uniform sites satisfy it).
4. **Generalises.**  The finite-temperature counterpart of E15, on a connected family.
5. **Computational reading.**  Useful: a transfer-matrix certificate of a chain costs `O(mk²)`
   rational operations and is checked by the kernel.  These (chains, trees, rings; treewidth at
   most two on paper) are the only exact partition-function certificates of polynomial size in
   this part of the report.
6. **Overstatement check.**  None remaining.

### E33. Theorem 11.21 — the sampled free-energy sandwich (row G10)

1. **Statement.**  `N` independent samples of a product reference give
   `−βm̂ − |β|η ≤ ln(Z/Z₀) ≤ −βm̂ + |β|η + β²C/8` outside an event of probability
   `2e^{−2Nη²/C}`, `C = Σc_i²`.  **[V]** (`sampled_free_energy_sandwich`); refereed (R2).
   Standard concentration.
2. **Setting.**  Finite product space; exact independent samples; exact evaluations; `Z₀` known.
3. **Assumptions.**
   * **{F}{Q}** product reference.  The concentration bound with `C = Σc_i²` fails for a
     dependent reference: perfectly correlated sites, `n = 4`, one sample:
     `P(|Δ − mean| ≥ 2) = 1 > 0.27`; a Markov chain with `ρ = 0.6`, `n = 12`: probability
     `0.086` against the bound `0.005` (S2(C)).  Substitutes: `(Σc_i)²` for any reference
     (Hoeffding); per-component sampling for a mixture of products (E7).
   * **{Q}** exact sampling.  If the samples come from `μ'` with total variation `τ` from `μ₀`
     the mean shifts by at most `τ·Σc_i`, so the bracket widens by `|β|τΣc_i` (immediate; not in
     the report).
   * **{E}** `Z₀` known — otherwise only the ratio is certified.
   * **{E}** the floor `β²C/8`: more samples do not reduce it (line 3078–3079).
4. **Generalises.**  Theorem 11.25(b) (exact constant `n ln cosh(u/2)` on the cube), 11.28(d)
   (one reference law for a class), §11.30 (box classes; reader AA2).
5. **Computational reading.**  `N = C ln(2/δ)/(2η²)`: for 100 torsions with `c_i = 0.5` kcal/mol,
   `η = 0.1` kcal/mol, `δ = 0.05`: about 4 600 samples — and a floor of 5.3 kcal/mol that they do
   not touch.  Polynomial, at an extensive accuracy.
6. **Overstatement check.**  Row G10 (line 1501): "polynomially many random evaluations where
   deterministic certification needs exponentially many" — true at the accuracy of the floor and
   for ensembles with entropy; "for a cold sharp site … the single evaluation of the ground state
   already reaches that accuracy" (line 2178–2179).  §7 item 4(d), line 1122–1124 ("exponentially
   more informative"), has the same omission.

## 3. Entries, part III — §§11.10–11.15 (query complexity with a hint; normal form; dense second order; free energies beyond first order; chains; rows G11–G17)

Status: §11.10 was refereed by R3 at commit `f1a6015` (Theorems 11.22–11.25 as they then stood;
one statement false, D35; a converse not tight, D36; scope too wide, D37).  **R3 did not referee
Theorem 11.26 or Theorem 11.23(c)** (its §6, §7); R4 refereed workstream A's upper bound of the
exponent (the claim after Theorem 11.27) and states that Theorems 11.27–11.28 as written in the
theory report were "outside my brief" (R4, line 343).  Theorem 11.28(d), (e) were checked
numerically by the reviewers of workstreams D and B.  §§11.11–11.15 are workstream results, each
re-derived by one independent reviewer (R_C, R_E, R_D, R_G, R_B); paper proofs except where a Lean
name is given.

### E34. Theorem 11.22 — sensitive alternatives must be detected; the hedged spot-check

1. **Statement.**  A deterministic algorithm that is `ε/2`-correct on a class queries, on every
   instance `g`, a point where `g'` differs from `g`, for every member `g'` with
   `|Φ(g') − Φ(g)| > ε`; a randomised one detects it with probability `≥ 1 − 2δ`; packing forms;
   conversely a hedged spot-check of a hint is correct.  **[V]** (`exists_query_ne`,
   `prob_query_ne_ge`, `expected_queries_ge_packing`, `hedgedSpotCheck_correct`); refereed (R3).
   Method known (radius of information; fractional block sensitivity).
2. **Setting.**  **Fully general**: any type `X` (no finiteness for (a)–(d)), any class, any
   functional.  An algorithm is any map from residuals to a finite queried set and an output that
   is consistent on residuals agreeing on the queried set — a class strictly larger than decision
   trees.
3. **Assumptions.**
   * **{E}** the only access to the residual is exact evaluation at points.  Other oracles
     change the theory: free marginals of the Gibbs measure are §§11.27, 11.29 (reader AA2);
     gradients or averaged data are not treated.
   * **{Q}** exactness of the evaluations — for the *converse* (the spot-check compares values
     for equality).  With errors bounded by `τ` the check must tolerate `τ`, and alternatives
     within `2τ` of the hint are indistinguishable: an accuracy floor (`2βτ` for `ln Z`), no
     change of the counting.  Stochastic noise is not treated — **{?}**.
   * **{E}** correctness on every member with probability `1 − δ` (not on average over a prior);
     an average-case theory is not in the report.
   * **{P}** finite mixtures of deterministic algorithms ("the arguments are pointwise in the
     random seed", line 3112–3114; continuum mixtures are not formalised, D37).
   * **{C}** the fallback "evaluate everything" of the spot-check (finite `X`; only the cost on
     the hint is claimed).
4. **Generalises.**  It is the general principle; everything in §11.10 instantiates it.
5. **Computational reading.**  The bracket between the two fractional hitting numbers is tight up
   to `(1 − 2δ)` and `ln(1/δ)` when the hedged converse applies; whether it is small is decided
   instance by instance.
6. **Overstatement check.**  None.  ("Every randomised algorithm" is qualified at line 1165–1166
   and 3112–3114.)

### E35. Theorem 11.23 — the minimum: every algorithm pays the covering price

1. **Statement.**  (a) On an instance `g` there is an algorithm, correct on every admissible
   residual, that makes exactly `k` evaluations on `g`, iff `g` has a value certificate with `k`
   points; (b) every randomised algorithm pays `(1 − 2δ)` times each exponential-weights bound;
   (c) a hedged spot-check attains `⌈ln(1/δ)(N_frac(ε⁻) + 1)⌉`.  **[V]**; (a), (b) refereed
   (R3); (c) appeared during the review and was not formally refereed (R3 commented on a draft
   and supplied the hedge; machine-checked: `min_hedgedSpotCheck_correct`).  The hub-family bound for randomised algorithms **[P]** (R3,
   Appendix B).
2. **Setting.**  Any finite instance of the admissible class; the functional is the minimum.
3. **Assumptions.**
   * **{E}{X}** the class is the first-order class (it contains every dip and both McShane
     envelopes).  In a class without dips the argument has no analogue ("a generic evaluation
     sees every perturbation", §12 item 9(c)): linear classes cost rank-many evaluations.
   * **{F}** "tailored to the instance", if read as "one algorithm": on the hub family
     `N_cov = 2` at every instance with a good hub and every randomised decision tree pays
     `((1−2δ)²/8)min(M, N)` on some instance (line 3239–3247; D37).
   * **{E}** correctness on the *whole* class: an algorithm that is only required to be correct
     on a subclass pays that subclass's price.
   * (ii) learn-then-cover (**[P]**): **{E}** an additive instance on a product space with a
     site-additive envelope (the additive interpolant must be admissible and equal to `g`);
     **{C}** computation is free (a type-covering code or a greedy cover must be *computed*).
4. **Generalises.**  Theorem 11.24 at finite temperature (as `β → ∞` the randomised theory
   becomes the covering theory, line 3279–3282).
5. **Computational reading.**  Randomisation gains the integrality gap of a covering problem and
   no more, so the exponents of E19 are query complexities at additive instances.  The costs
   are instance-wise: they are attained by algorithms that are handed the instance.
6. **Overstatement check.**  `README.md` 148–150: "the lower bounds hold at every instance, so
   **no procedure that is correct on a first-order class can be cheap on any of its
   subclasses**".  The lower bound at an instance is that instance's own covering number, which
   is small at many instances: at a sharp instance one evaluation; at the residual `c|x|` on
   the cube two evaluations "at every accuracy and temperature" (line 3400–3403); at the
   nearly sharp family of S3, `n + 1`.  On those subclasses a correct procedure *is* cheap.
   What is proved is narrower: at an instance whose covering number is large, membership in a
   benign subclass does not help.  (The same sentence is in D28.)  Also line 3236–3239, "The
   pattern is general: query complexity ≤ cost of learning … + cost of verifying …" — a
   heuristic, shown on additive instances only.

### E36. Theorem 11.24 — the free energy: soft gaps

1. **Statement.**  A dip of depth `c` at `y` multiplies `Z` by at least `e^{βc − Λ(y)}`, so every
   algorithm that is correct for `ln Z` reaches within slack `c` of every `y` with
   `βc > Λ(y) + ε`; packing forms; the queries of a deterministic algorithm form a free-energy
   certificate; the exact dip criterion (d).  **[V]**; refereed (R3).
2. **Setting.**  Any finite instance, `β ≥ 0`.
3. **Assumptions.**  **{E}** the first-order class (dips).  **{Q}** the soft gap is a relaxation
   (`(c − s)₊ ≥ c − s`); the exact criterion (d) replaces it and is necessary for small `ε`
   (**{F}** for "the soft-gap bound is attained for every `ε = o(n)`": D35, `DEAD.15`).  For the
   single-letter forms: **{E}** a product landscape with site-additive slack
   (`softGap_hamEnv_additive`).
4. **Generalises.**  Generalised dips (Theorem 11.27): single dips are not the extremal
   perturbations (D34, D38).
5. **Computational reading.**  A valid lower bound at every instance; exact only on the cube and
   for two-state sites.
6. **Overstatement check.**  None in the theorem.  The table cell at line 3292 ("the exponent
   itself is known only on the cube at the zero residual") is stale — it understates what the
   same section claims 240 lines later (§8, Err-5).

### E37. Theorem 11.25 — the cube: a sharp threshold and the accuracy diagram at the zero residual (row G11)

1. **Statement.**  On `{0,1}ⁿ`, `f ≡ 0`, `d = c·`Hamming, `u = βc`: (a) at the zero residual
   `E|Q(0)| ≥ (1−2δ)2ⁿ/|B(k)|` whenever `ε < Δ_k` (**[V]**, `cube_exact_dip_randomized`); (b)
   for `ε₁ > ln cosh(u/2)` a bounded number of uniform random evaluations suffices on every
   instance (**[P]**); (c), (d) matching upper bounds at the zero residual by Harper's theorem
   and the hedged spot-check, and the exponent in every accuracy regime (**[P + K]**).  Refereed
   (R3 found the first version false for exponentially small accuracies, D35, and supplied the
   hedge).
2. **Setting.**  The uniform two-state cube with equal constants; the *class-wide* statement is
   the threshold; the exponents are at one instance, the zero residual, **with the instance as
   a hint**.
3. **Assumptions.**
   * **{F}** the zero residual, if read as "every instance": `c|x|` costs two evaluations (line
     3400–3403; D37).
   * **{F}{Q}** no known part (`f ≡ 0`).  With an excitation energy `e ≠ 0` the hardest instance
     is not the zero residual and the threshold is the largest chord gap of the pressure
     (`0.11383` against `0.11367` at `e/c = ½`, `β = 1`; Theorem 11.28(e); S5); with a field the
     exponents and the optimal sampler change (§11.20, reader AA2).
   * **{F}** two states per site — for "single dips are extremal": false from three states on
     (D38, `DEAD.16`; Theorem 11.27).
   * **{Q}** equal constants `c_i = c`: the threshold of a product of site types is the average
     of the site thresholds (Theorem 11.28, remark (ii), **[P]**); the exponents do not add
     (D31).
   * **{P}** Harper's theorem (**[K]**; "the step that uses it is checked exhaustively for
     `n ≤ 4`", line 1360–1361).  Beyond the cube the upper bound has another proof (inherently
     typical subsets; R4).
   * **{X}** the hint.  Without it non-adaptive algorithms have the larger exponent `θ_na`
     (§11.16) and adaptive ones recover the hinted exponent with `o(n)` terms that are
     enormous at any computable size (§§11.18–11.19; reader AA2).
4. **Generalises.**  Theorems 11.27–11.28 (alphabets, additive instances, the class threshold);
   11.34 (the torus); §§11.16–11.26 (reader AA2).
5. **Computational reading.**  Two things.  (i) "Bounded cost above the threshold" is a statement
   about the accuracy `n·ln cosh(u/2) ≈ nu²/8` — *extensive*; at `u = 1` and `n = 100` it is
   `12 k_BT`.  (ii) Below the threshold the exponent is `≈ u²/32` for small `u`, and the
   machine-checked bound is modest at computable sizes: at `ε = 1`, `u = 1` it is `e^{4.6}`
   evaluations at `n = 100`, `e^{16.9}` at `n = 500`; at `u = 0.5` it is `e^{9.7}` at `n = 1000`
   (S6(d)).  The hardness is asymptotic; for weak envelopes on a few hundred sites it forbids
   little.
6. **Overstatement check.**  The theorem and `README.md` 130–135 are scoped ("for the worst case
   over instances", "on the zero residual").  Stale: line 3413–3414 (§8, Err-4).

### E38. Theorem 11.26 — soft-gap sampling: an upper bound in the same quantity

1. **Statement.**  The spot-check with the sampler `½π + ½w/W` is correct for `ln Z` on the whole
   class with `N = ⌈2 ln(1/δ)E_π[e^Λ]/(1 − e^{−ε/2})⌉` samples.  **[V]** (`detection_weight_ge`,
   `thermal_spotCheck_correct`); **not refereed** (R3, §7).
2. **Setting.**  Any finite instance, `β ≥ 0`; the instance is given as a hint.
3. **Assumptions.**  **{E}** the hint (on additive instances of product landscapes it can be
   learned from a star, **[P]**, line 3462–3469).  **{C}** unhedged.  **{E}** sampling from the
   Gibbs measure of the hinted landscape and from the dip weights — free in this model.
4. **Generalises.**  The hedged, isoperimetric upper bounds of Theorems 11.25(c), 11.27.
5. **Computational reading.**  **Uninformative as an exponent**: on the cube it gives
   `ln(2/(1+e^{−u})) = 0.380` per site against the true `0.029` at `u = 1` (line 3454–3457); for
   the site `e/c = ½` it "says nothing" at `β = 4` (`0.630 > 0.482`).  Its content is the
   machine-checked separation from deterministic cost on the cube.
6. **Overstatement check.**  "There **randomisation provably lowers the exponent**" (line 3447)
   is at one site, three temperatures, with a hint — and the sentence says where.  None.

### E39. Theorem 11.27 — generalised dips (row G12)

1. **Statement.**  (a), (b) For every `Φ` that is Lipschitz for the slack, `g − (r − Φ)₊` is
   admissible and raises `ln Z` by at least `βr − Λ(Φ)`; packing bounds follow (**[V]**,
   `GeneralisedDips.lean`).  (c) On identical sites at an additive instance
   `n⁻¹ ln E|Q| ≥ R^gen_β(ε₁)`, a matrix game over the vertices of the Lipschitz polytope of a
   site (**[P]**, ingredients **[V]**).  "`R^gen_β` is the exponent" (**[P]**; the upper bound
   refereed by R4 as workstream A's Theorem A).
2. **Setting.**  (a), (b): any finite instance.  (c) and the exponent: `Sⁿ`, identical sites,
   additive instance, `ε_n/n → ε₁`, `ln(1/ε_n) = o(n)`, fixed `δ`, the instance as a hint or
   learned from a star.
3. **Assumptions** (of the exponent statement).
   * **{F}** accuracy not exponentially small (D35).
   * **{F}** the hedge in the upper-bound algorithm (the unhedged spot-check loses `e^{Θ(ε)}`,
     D36).
   * **{P}** identical sites: for several site types the class-level exponents are established
     in §11.26 (reader AA2) with a common slope.
   * **{?}** an additive instance (non-additive instances are open, line 3679–3680).
   * **{Q}** a fixed error probability (`ln(1/δ)` enters the cost linearly).
   * **{E}** independent sites: for a nearest-neighbour known part the exponents move in either
     direction (§11.32, reader AA2).
4. **Generalises.**  §11.26 (heteropolymer landscapes), §11.20 (field).
5. **Computational reading.**  The exponents are small numbers per site (`0.029` for the flat
   four-state site at `u = 1`; S5), so the remark of E37(5) applies.
6. **Overstatement check.**  Line 3549–3551: "The statement **needs** every one of its
   hypotheses: identical sites, an additive instance, an accuracy that is not exponentially
   small, a fixed error probability, and the hedge."  Necessity is shown for two of the five
   (accuracy: D35; hedge: D36); the other three are *used* — and "identical sites" is relaxed by
   the report's own §11.26.  Stale: line 3675–3677 calls the upper bound "the unrefereed claim
   above" although line 3528 and §8 (line 1162–1163) say it was checked by a referee (§8, Err-3).

### E40. Theorem 11.28 — the two-reference sandwich; thresholds beyond the cube (row G12)

1. **Statement.**  (a), (b) a two-measure exponential-moment inequality tensorises, and a set that
   supports a sensitive profile has `Qⁿ`-mass bounded below (**[V]**); (c) every additive
   instance of identical sites has a sharp accuracy threshold `ε₁^thr = min_Q γ(Q)` (**[P]**);
   (d) for every admissible residual `n·m(Q) ≤ ln Z(f+g) + βE_{Qⁿ}g ≤ n·M(Q)` (**[V]**
   `product_sandwich`), hence the worst-case threshold of the class without a hint is
   `ε₁* = min_Q[M(Q) − m(Q)]` (**[P]**, minimax); (e) two-state sites: the largest chord gap of
   the pressure (**[P]**).  Not refereed by R3 or R4; (d) re-derived and tested by the reviewer
   of workstream D, (e) by the reviewer of workstream B; harness XII.10–XII.13.
2. **Setting.**  `Sⁿ`, identical sites, any alphabet, extensive accuracy `ε = nε₁`.
3. **Assumptions.**
   * **{E}** independent sites — for a width that is `n` times a single-site quantity and for
     the exponential cost below it.  The sandwich and the minimax identity themselves "use
     nothing of the product structure" (remark (i), line 3630–3636, **[P]**): on any finite
     class the threshold is `min_Q[max F_Q − min F_Q]`, with `O(β²D²ln(1/δ)/Δ²)` samples above
     it.  For a chain the threshold of the class is **{?}** (the additive candidate is not
     extremal, D41; line 4086–4090).
   * **{Q}** identical sites: finitely many types by averaging (remark (ii), **[P]**).
   * **{E}** extensive accuracy.  The thresholds say nothing about `ε = o(n)`.
   * **{E}** exact samples of the reference `Q*ⁿ` and exact knowledge of the known part.
4. **Generalises.**  §11.26 (site types), §11.20 (field); for sup-norm classes the threshold
   picture is replaced by a cost formula (§11.30) — reader AA2.
5. **Computational reading.**  The positive half ("a bounded number of evaluations above the
   threshold, without a hint") is at an accuracy of `0.114` nats *per site* for the report's
   example (`e/c = ½`, `β = 1`; S5) — `11 k_BT` on 100 sites.  Every accuracy below it is
   exponential asymptotically.  So the theorem certifies free energies only to a precision
   that grows with the system.
6. **Overstatement check.**  Line 3665 ("So the picture of Theorem 11.25 extends beyond the
   cube, to every product landscape of identical sites"): the thresholds extend; the accuracy
   diagram below them does not (exponentially small accuracies are treated only on the cube,
   §8 line 1153–1155).  The next sentences say what is meant.  Minor.  Stale: line 3672–3673
   and 3679–3680 (§8, Err-8).

### E41. Theorem 11.29 and Proposition 11.30 — the normal form; best-first search in centre form (row G13)

1. **Statement.**  With `f^d` the Pasch–Hausdorff envelope of the known part and `σ` the reduced
   cost of `d`, the value certificates of `(d, f, g)` are exactly the point certificates of
   `(σ, 0, f^d + g)` (**[V]**, `isValueCertificate_iff_normalForm`).  If `σ` is
   `ρ`-quasi-symmetric, best-first search makes at most `|C|` evaluations for every cover with
   centre radii `(gap^d(c) + ε)/(2ρ+3)`, for every admissible residual (**[P]**; separation
   lemma **[V]**).  Workstream C, re-derived by its reviewer (R_C).
2. **Setting.**  Any finite instance; asymmetric envelopes must be allowed.
3. **Assumptions.**
   * **{F}** "minima and certificates of minima".  For free energies the reduction is false:
     `X = {0,1}`, `d = [x ≠ y]`, `f = (0, 5)`: `f^d = (0, 1)`, every minimum is unchanged and
     `ln Z` changes by up to `0.675` over the class at `β = 1` (S6(a)).  The report says so
     (line 3742–3743).
   * **{E}** asymmetric envelopes in the framework (the reduced envelope of a symmetric one is
     a weightable quasi-metric).
   * Proposition 11.30: **{E}** quasi-symmetry of the reduced envelope, which "fails as soon as
     one state is dominated in the known part — one sharp site of a product, one
     dead-end-elimination pair" (line 3769–3771).  **{F}** without it: best-first search is
     unboundedly worse than the smallest certificate on the line (`212` evaluations against `3`;
     D39, `DEAD.17` — growth laws computed, not proved).
4. **Generalises.**  —
5. **Computational reading.**  The normal form is a clean reduction.  Proposition 11.30 excludes
   exactly the instances a design problem has (dominated states), so as a search guarantee it
   is **vacuous there**; only Theorem 11.11 remains, whose comparison class is itself
   unboundedly weak (E21).
6. **Overstatement check.**  `README.md` 143–144: "A known part turns out to be nothing but the
   gradient part of an asymmetric envelope (normal form, machine-checked)"; report line
   1550–1551: "the normal form (G13), which shows that the known part was never a separate
   ingredient".  Both omit "for minima": for every free-energy statement of §§11.6, 11.10 the
   known part *is* a separate ingredient (it is the reference measure).

### E42. Theorems 11.31, 11.32 — dense second-order classes (row G14)

1. **Statement.**  The dip `c·C(r − d_H(x,y), 2)₊` belongs to the dense second-order class, so
   after any evaluations the uncertainty at `y` is at least `c·C(d_H(y,A)+1, 2)`; a union of
   stars gives exactly the best single-star bound (**[V]**, `SecondOrderDip.lean`, for arbitrary
   site alphabets).  Hence `K₋ ≤ N₂ ≤ (n+1)K₊ + 1` with covering codes at radii
   `≈ (2·gap/c)^{1/2}`; full exponent for constants of order one; a rate–distortion exponent for
   mean-field constants, positive iff `e/γ < 1/4` (**[P]**, counts verified numerically).
   Workstream E, re-derived by its reviewer (R_E).
2. **Setting.**  The cube (the theorems hold for `k` states: Lean for 11.31, workstream E §2.9 for
   11.32), one constant `c` for all pairs, an additive true residual, no first-order bound.
3. **Assumptions.**
   * **{Q}** dense, equal constants.  For sparse constants the class is finite-dimensional and
     the cost lies between an exponential in the clique number and the number of cliques
     (11.32(v), **[P]**).
   * **{P}** an additive true residual (the star then reproduces it).
   * **{C}** `f = e|x|`, zero residual, in (i)–(iv).
   * **{?}** the best `n + 1` evaluations (the spider is conjecturally optimal; §12 item 4).
4. **Generalises.**  Order `m` (threshold `2^{1−m}/m!`); free energies: Theorem 11.33.
5. **Computational reading.**  For constants of order one the saving over full enumeration is a
   factor `2^{Θ(√n log n)}`: nothing.  For mean-field constants `c = γ/n` two opposite stars
   (`2n+2` evaluations) certify iff `e ≥ c(⌊n/2⌋ − 1)/2`; the numbers `0.295, 0.078, 0.007` are
   reproduced (S5).  (The remark at line 2985–2987, "two stars at opposite corners do not once
   `n ≥ 6e/c + 6`", is true and weaker than this exact threshold `n > 4e/c + 2`.)
6. **Overstatement check.**  None in the section.  Stale: line 2995–2996 and 3866–3868 (§8,
   Err-6, Err-7).

### E43. Theorem 11.33 — second-order classes at finite temperature: a transition at the Curie–Weiss coupling (row G15)

1. **Statement.**  For the class `𝒢₂(c₂)` on the cube, `w = βc₂n`: (a) for `w ≤ 4` polynomially
   many evaluations at every accuracy (Dobrushin uniqueness along an annealing path); (b) for
   `w > 4`, `f ≡ 0`, at the zero residual, exponentially many for every algorithm below the
   accuracy `n·f_CW(w)`.  **[P]** (the droplet is **[V]**); workstream D, Theorem 13;
   re-derived by its reviewer (R_D), who completed the bookkeeping of (a).
2. **Setting.**  Binary cube; one dense constant; no first-order bound; heat-bath Glauber
   dynamics with one evaluation per update.
3. **Assumptions.**
   * **{F}{X}** **an additive known part in (a) — a hypothesis that the theory report's
     statement does not contain.**  The source has it ("`f` additive", `D_REPORT.md` line
     489–491, and the proof: "`f` and `g_star` are additive and drop out"); the report states
     (a) for the class with no word about `f` and (b) "for `f ≡ 0`".  Without it (a) is false,
     for every `w > 0`.  *Counterexample (new, S4).*  Let `C` be a binary code of minimum
     distance `d_min`, `f = M·[x ∉ C]` with `M` large, instance `g ≡ 0`.  For `y ∈ C` the droplet
     `−c₂·C(r + 1 − d_H(x,y), 2)₊` is in the class (Theorem 11.31(a); re-checked exhaustively at
     `n = 10`), differs from `0` only on `B(y, r−1)`, and multiplies the weight of `y` by
     `e^{βc₂ r(r+1)/2}`.  If `2(r−1) < d_min` the supports are disjoint, so by Theorem 11.22(c)
     `E|Q(0)| ≥ (1−2δ)|C|` as soon as one droplet is sensitive.  Explicit instance: the extended
     Golay code, `n = 24`, `w = 4`, `r = 4`: each of the 4 096 droplets changes `ln Z` by
     `1.05·10⁻³`, so every algorithm with `ε < 10⁻³` makes `(1−2δ)·4096` evaluations.
     Asymptotically, with Gilbert–Varshamov codes of relative distance `δ*`,
     `E|Q(0)| ≥ (1−2δ)e^{R(w)n}` at every bounded accuracy, `R(w) = ln 2 − h(δ*) = wδ*²/8`:
     `R = 0.006, 0.020, 0.034, 0.056` at `w = ¼, 1, 2, 4`.  The complexity changes from
     polynomial to exponential.  *The same with a pairwise known part* (S4(D)): ferromagnetic
     blocks of size `b` with no coupling between blocks; for a strong coupling the Gibbs measure
     of `f` is uniform on the `2^{n/b}` block-constant configurations, which are at mutual
     distance `≥ b`; a droplet of radius `≈ b/2` at one of them multiplies its weight by
     `e^{wb²/(8n)}`, and with `b ≈ 1.5·n^{2/3}` every one of the `2^{n/b}` disjoint droplets is
     sensitive at `w = 4`, `ε = 1` (closed form checked by enumeration at `n = 12`; `2^{21}`
     droplets at `n = 32 256`, `2^{85}` at `n = 2·10⁶`): at least `exp(Θ(n^{1/3}))` evaluations —
     super-polynomial — for a known part of exactly the kind §1 of the report considers.  (In
     block variables the class has the effective coupling `w·b`.)  **{Q}**: what the proof of
     (a) needs is Dobrushin's condition for `f + g` along the path, i.e. the influence of `f`
     plus `(n−1)tanh(βc₂/4)` below one.
   * **{P}** two states per site, equal constants (non-homogeneous constants give a row-sum
     condition; `k` states open: §12 item 10).
   * **{C}** no first-order bound (part (c) adds one).
4. **Generalises.**  Not to interacting known parts (above).  The continuous analogue is open
   (§12 item 10).
5. **Computational reading.**  (a) is polynomial and far from practical: the workstream's count
   is `O(K³ε⁻²·n·…/(1−α))` with `K = ⌈wn⌉` and `1 − α ≥ 1/n`, "about `n⁵ε⁻²`" (line 3886) —
   `10¹⁰/ε²` evaluations at `n = 100`; taken literally it exceeds `2ⁿ` up to `n = 22`, with the
   constants and logarithms of the workstream's count up to `n ≈ 40`.  (b) is
   asymptotic: "at `w = 5` the bound is only `e^{3.9}` for `n = 2000`" (line 3902).
6. **Overstatement check.**  Row G15 (line 1507): "second-order classes have a transition at the
   Curie–Weiss coupling `βc₂n = 4` (polynomial below …, exponential above …)"; line 3898–3900:
   "for free energies second-order structure does rescue certification, but only in the
   high-temperature phase of the *class*".  Both are for an additive known part, a binary cube
   and one dense constant; with a known part that has structure — a pairwise one suffices —
   the "rescue" fails (S4).

### E44. Theorem 11.34 — a continuous space: the torus of torsion angles (row G15)

1. **Statement.**  On `(ℝ/2πℤ)ⁿ` with the uniform reference, `f ≡ 0` and per-coordinate
   Lipschitz constants `L_i`: for `ε > J = Σ_i ln(sinh b_i/b_i)` a number of uniform random
   evaluations independent of `n` suffices on the whole class; for `ε < J` every algorithm pays
   an exponential lower bound at every constant residual.  **[P]** (workstream D, Lemma 5 and
   Theorem 6; re-derived by R_D).
2. **Setting.**  The only continuous configuration space of the two parts.  Exact point
   evaluations; uniform random points (a continuum mixture, outside the formal model of
   randomness, which covers finite mixtures).
3. **Assumptions.**
   * **{?}** no known part (uniform reference).  The class threshold with a known part is
     Theorem 11.28(d) on finite alphabets; its continuous version is not written.
   * **{X}** per-coordinate (`ℓ¹`) constants.  With one global `ℓ²` Lipschitz constant the cost
     is dimension-free, `exp(Θ(β²L²))` (line 3917–3918; `D_REPORT.md`, Remark 8); in fixed
     dimension it is `(βL/ln βL)^d` (**[K]**).
   * **{C}** heterogeneous `b_i` are allowed.
   * **{P}** the isoperimetric step on the circle (Lemma 5 of the workstream, "probably
     classical").
4. **Generalises.**  Theorem 11.25 from the two-point site to the circle.  Not covered: hybrid
   (basin, angle) sites, a known part, constraints between angles.
5. **Computational reading.**  As E37: the positive statement is at the extensive accuracy `J`
   (`0.16` nats per angle at `b = 1`); a deterministic mesh needs `(nb/ε)ⁿ` points.
6. **Overstatement check.**  Line 3914–3916: "it is the form of the threshold that applies to
   torsion-angle coordinates" — for a flat landscape (no known part) and angles that are
   independent in the envelope.  No chain has either.

### E45. Theorem 11.35 — Boltzmann averages are harder than free energies (row G15)

1. **Statement.**  On the cube with `f ≡ 0`, for the mean magnetisation at the zero residual:
   every algorithm needs exponentially many evaluations for an accuracy `η < ε_set(u)`, with
   `ε_set/H` between `1/√2` and `0.87`; with a hint a bounded number of samples suffices above a
   level within one per cent of `ε_set` for `u ≥ 6`.  **[P]** (workstream D, Theorem 12, a
   "proof sketch" there; re-derived by R_D).
2. **Setting.**  One observable, one model, one instance.
3. **Assumptions.**  **{E}** the observable is the mean magnetisation of the uniform cube;
   **{E}** the instance is the zero residual; **{?}** the interval between `H/√2` and `H` at weak
   coupling (line 3931–3932).  Nothing is proved for another observable or another known part.
4. **Generalises.**  Proposition 11 of the workstream (any observable in `[0,1]`: a dip that
   changes `ln Z` by less than `Δ` moves every average by less than `1 − e^{−Δ}`) is not in the
   theory report.
5. **Computational reading.**  A lower bound of the asymptotic kind (E37).
6. **Overstatement check.**  The title (line 3920), "Boltzmann averages are harder than free
   energies", and row G15, "Boltzmann averages are uncertifiable on most of their a-priori
   range" (line 1507), state a result about one observable at one instance of one model as a
   general fact; "almost the whole a-priori range" (line 3925) is 71–87 %.

### E46. Theorem 11.36 — the lever-arm law (row G16)

1. **Statement.**  The verified constants of Theorem 4.6, uniform over the rotamer domain, are
   `c_i^ver = 2Λ sin(δ/2)√(Ī(m_i))` with `Ī(m) = ⅓ sin²(θ/2) b² m³(1 + O(1/m))`; the smallest
   valid constants are at least `0.186·Λ b m_i^{3/2}` (computed for `m ≤ 10⁵`, **[N]**).
   **[P]** for the bound; workstream G, checked by R_G with own geometry code; wording corrected
   by SCI-REV-0006, -0009.
2. **Setting.**  A chain with fixed bond length and bond angle, torsions as the only degrees of
   freedom, a product rotamer domain that contains extended arms; excluded volume ignored.
3. **Assumptions.**
   * **{Q}** a domain that contains extended arms — for the power `3/2`.  **New (S6(c)):** on
     *every* torsion domain the inertia of an arm of `m` atoms about any line is at least
     `(m/3)(½b cos(θ/2))² = 0.0267·m b²` at `θ = 111°` (three consecutive atoms span a triangle of
     width `b cos(θ/2)`), so the verified constants grow at least like `m^{1/2}`:
     `c_i^ver ≥ 0.33·sin(δ/2)·Λ b m_i^{1/2}`.  The hypothesis "`γ > 0`" of Theorem 11.37 therefore holds
     for the verified constants with no assumption on the domain; excluded volume does not
     rescue the route.
   * **{C}** ideal geometry (rigid bond lengths and angles).  Flexible geometry is not treated —
     **{?}**.
   * **{?}** the proved lower constant for the smallest valid constants (only the numerical one
     is given; §12 item 9).
4. **Generalises.**  —
5. **Computational reading.**  This is the theorem that makes the weighted-Hamming route of §4.4
   quantitatively empty for chains (E47).
6. **Overstatement check.**  None (the name "law" is disclaimed at line 3978–3984).

### E47. Theorems 11.37, 11.38 — growing constants; the RMSD envelope used directly (row G16)

1. **Statement.**  If `c_i ≥ c₀m_i^γ`, `γ > 0`, then at an additive known part with total
   excitation energy `G` and zero residual `ln N_cov(ε) ≥ n ln k − C((G+ε)/c₀)^{1/(1+γ)}`, also
   for randomised algorithms and for `ln Z` at extensive accuracy (**[P]** from **[V]**
   bounds).  With the RMSD envelope itself,
   `c√(λN) ≤ ln N_cov(0) ≤ 4.91√(λN ln(e(k−1)n)) + ln(81(n+1))` (**[P]**; the lower constant
   numerical).  Workstream G, checked by R_G.
2. **Setting.**  Product rotamer domain without excluded volume; additive known part; zero
   residual; fixed `L`.
3. **Assumptions.**
   * **{E}** the weighted-Hamming *format* (11.37).  **{X}**: with the RMSD envelope itself the
     cost at the same instance is a stretched exponential (11.38).
   * **{P}** additive known part, zero residual (the one-shot bounds of Theorem 11.6 hold for
     any known part; the count is written for additive ones).
   * **{?}** excluded volume: the domain is then not a product and the counting of 11.37 does
     not apply as written (the growth of the constants does, E46).
   * **{Q}** `Lb/e = o(N)` in 11.38; for an extensive `L` both formats are exponential (R_G,
     item 2).
4. **Generalises.**  §11.17 (reader AA2) leaves the format: classes linear in pair features.
5. **Computational reading.**  11.37 is a clean no-go for the format.  11.38 is "one instance and
   a wide bracket" (line 4013).
6. **Overstatement check.**  Line 3994–3995 and §10 line 1555–1556: "**the verified chain-rule
   route of §4.4 cannot certify long chains**" — proved at the zero residual of an additive
   known part on a product domain, in one format, at fixed `L`; the sentence is the natural
   reading of the theorem but it is stated without them.  Numbers: §8, Err-9.

### E48. Theorem 11.39 — chains as known parts: the droplet criterion (row G17)

1. **Statement.**  For a nearest-neighbour chain known part and the envelope `c·`Hamming, one
   evaluation at a minimiser certifies the minimum for every residual iff every contiguous
   droplet is sharp, `c ≤ τ = min_y gap(y)/d_H(x̂,y)`; otherwise the certificate size grows
   exponentially (for randomised algorithms: proved at the zero residual).  For the
   ferromagnetic Ising chain `τ = 2h`.  **[P]**; workstream B, re-derived by R_B; no Lean.
2. **Setting.**  A chain (inhomogeneous allowed in the criterion), one constant `c`.
3. **Assumptions.**  **{E}** nearest-neighbour interactions (the criterion is a min-plus
   transfer-matrix computation); for longer range or two dimensions the sharp-minimum condition
   of Theorem 2.4 still characterises one evaluation, but no droplet reduction is stated —
   **{?}**.  **{Q}** a uniform constant `c` (site-dependent constants give a weighted ratio; not
   stated).  **{C}** the Hamming envelope.
4. **Generalises.**  Theorem 11.7 from independent sites to chains; functions of the type are
   §11.23, a chain at finite temperature §11.32 (reader AA2).
5. **Computational reading.**  Useful as a test (`O(nk²)`), and sobering: at zero field no chain
   is sharp for any `c > 0`, however large the coupling.
6. **Overstatement check.**  None; line 4027–4028 states the scope of everything before it
   exactly.

### E49. Theorem 11.40 and Proposition 11.41 — the exponent of homogeneous chains; the Boltzmann bound is vacuous on a window (row G17)

1. **Statement.**  For a homogeneous nearest-neighbour chain, an additive residual with `κ < 1`
   and `ε_n = o(n)`: `n⁻¹ ln N_cov → sup_ν R_ν(e(ν))` over stationary processes; the
   transfer-matrix (Shannon) lower bound is positive iff `c > 2(J+h)` although certification is
   exponential for `c > 2h`.  **[P]**, "checked by a reviewer, no gap found"; no Lean.
2. **Setting.**  As E48, homogeneous.
3. **Assumptions.**  **{P}** homogeneity (block coding); inhomogeneous chains are open (§12 item
   1).  **{F}** `κ < 1`, as in E19.  **{?}** an additive residual.  **{Q}** `ε = o(n)`.
4. **Generalises.**  Theorem 11.9.  Finite-temperature exponents of a chain are open.
5. **Computational reading.**  The exponent is a supremum over processes with **no computable
   form** below the critical distortion; a free block of length 12 gives `0.215 ≤ R* ≤ 0.242`
   at `c = 4J`, `h = 0` (line 4065–4066).  The blueprint's planning formula is zero on the whole
   window `2h < c ≤ 2(J+h)`.
6. **Overstatement check.**  Line 4051, "This settles the conjecture of §12 item 1(c)": by a
   paper proof read by one reviewer.  Minor.

### E50. Proposition 11.42 — finite temperature on a chain (row G17)

1. **Statement.**  For a site-additive slack the soft gap of a chain is a hidden-Markov
   log-likelihood (a pinned free energy); the dip threshold at an additive instance is a chord
   gap of the chain's pressure.  **[P]**; workstream B.
2.–3. **{E}** nearest-neighbour chain; **{F}** "the worst-case Jensen gap of a pairwise binary
   reference is attained by an additive residual" (the workstream's conjecture; refuted, D41:
   antiferromagnetic `K₄`, a star, a tilted chain of three sites) — so the dip threshold is a
   lower bound and the threshold of the class is **{?}**.
4.–6. A lower bound and a formula; the section says what turned out false (line 4077–4090).
   No overstatement.

## 4. (a) The hierarchy for this part

From the tractable models outwards.  "→" = relaxed by; "✗" = fails, with the evidence; "open" =
no result.

```
L0  ANY SET / ANY FINITE INSTANCE, the first-order (difference-constraint) class     [V], general
    exact characterisations:  Thm 2.3, 2.4, 2.6, 2.7 (arbitrary type X)  ·  2.1, 2.5  ·  11.1–11.6
    11.12–11.14  ·  11.22–11.24, 11.26, 11.27(a,b)  ·  11.29  ·  kernel soundness (§6.1, §11.8)
    – nothing assumed: no product, symmetry, homogeneity; asymmetric envelopes allowed
    – cost of using them: a covering number / a max–min over pairwise models (NP-hard, 11.10)
    ✗ a table that is not transitively closed (D3, S1)   ✗ other certificate notions for 2.7 (D21)
    ✗ one algorithm for all instances (hub family, D26, D37)   ✗ search vs N_cov (D30, D39)

L1  INDEPENDENT SITES, arbitrary site types, every n                          [V] one-shot bounds
    11.7, 11.8 (minimum)  ·  thermal product bounds (ln Z)  ·  3.1(c), 11.21 (product reference)
    11.28(a,b), sandwich of 11.28(d)
    ✗ dependent reference for the Σc_i² width: every correlation ρ > 0 (D14; S2)
      → mixture of K products: same width with K averages (S2(D))
      → Markov / Dobrushin: ‖Γc‖² [K]        → any reference: (Σc_i)² [V] (vacuous if βΣc_i > 8)
    ✗ additive extremal residual for dependent references (D25, D41)

L2  IDENTICAL SITES (or finitely many FIXED types), ADDITIVE INSTANCE, ACCURACY WINDOW   [P] upper bounds
    11.9  exponent R*  (ε = o(n))            ✗ κ = 1; ✗ margins → 0 with n: N_cov = n+1 (S3)
    11.15 exponent R_β (ε = o(n), ln 1/ε = o(n))   ✗ exponentially small ε (D29)
    11.25 the cube, f ≡ 0, zero residual, with a hint: every accuracy regime
    11.27 exponent R^gen (identical sites, additive instance)   ✗ single dips, ≥ 3 states (D38)
    11.28 thresholds: additive instance; whole class without a hint (extensive accuracy only)
    → several site types, alphabets, field, no hint, rounds: §§11.16–11.26 (reader AA2)
    open: non-additive instances; exponentially small ε beyond the cube

L3  KNOWN PARTS WITH INTERACTIONS                                              [P], no Lean
    11.39 one evaluation ⇔ droplets sharp (nearest-neighbour chain)
    11.40 exponent = sup over stationary processes (no computable form; brackets)
    ✗ transfer-matrix (Boltzmann) formula: zero on a window (11.41)
    11.42 soft gap = pinned free energy;  class threshold open (✗ additive extremality, D41)
    → functions of the type §11.23, chain at finite temperature §11.32 (reader AA2)
    open: longer range, many-body, two dimensions, inhomogeneous chains

L4  OTHER UNCERTAINTY CLASSES (evaluations combine)
    second order, ONE reference, PRODUCT domain, WEAK coupling: 11.16–11.18f   [V] bounds
    ✗ non-product domain (11.18c)   ✗ several stars (11.31(b))   ✗ dense constants: 11.31–11.32
    free energies: 11.33  (binary cube, dense constant, ADDITIVE known part)
    ✗ a known part with structure: ≥ exp(c·n^{1/3}) for pairwise blocks, ≥ exp(Rn) for a code (S4)
    → linear classes §11.17, Hilbert ball 11.50a, box classes §11.30 (reader AA2)
    open: certified constants (one paper certificate elsewhere); several references; k states for 11.33

L5  CONTINUOUS VARIABLES
    voxel enclosures (§3.4): product measure, pairwise energy; cost ∝ (β(M−m)d)^{d/2}
    11.34 the torus: f ≡ 0, per-angle constants   ✗→ one ℓ² constant: dimension-free
    open: a known part on a continuous space; hybrid (basin, angle) sites; noise

L6  CHAIN GEOMETRY
    4.6, 4.7 torsion → RMSD → bounded-difference constants (inputs: Λ, inertia bound)
    11.36 constants ≥ 0.82·Λ b m^{3/2} (extended arms); ≥ 0.33 sin(δ/2)·Λ b m^{1/2} on every domain (S6)
    11.37 ⇒ weighted-Hamming format exponential with almost full exponent
    11.38 RMSD envelope itself: exp(Θ̃(√N)) at one instance (bracket e^{1.4} … e^{235} at n = 1000)
    open: excluded volume, flexible geometry; → pair-distance profiles §11.17 (reader AA2)
```

What no result of this part covers: exponents or thresholds at non-additive instances; known
parts with long-range or many-body interactions; residual classes on non-product domains beyond
the remainder bounds of 11.18c; continuous spaces with a known part; evaluations with noise;
average-case correctness; and — for every class — constants certified for a concrete residual
(one paper certificate of another division excepted, line 1272–1279).

## 5. (b) The ten assumptions whose classification matters most outside the report's models

1. **The residual lies in the full first-order class, and nothing more is known about it**
   ({E} for every lower bound: the dips must be members; {X} when it changes).  The exponential
   price is the price of *this class*: a linear class costs rank-many evaluations, a weakly
   coupled second-order class `n(k−1)+1`, a box class the Boltzmann factor of a free-energy
   distance.  Whoever applies the theory must first decide which class the residual is in — and
   the constants of every class are inputs (assumption 7).
2. **Independent sites** — a product reference measure, an additive known part, a site-additive
   envelope ({E}/{F}/{X}).  Every exponent and every threshold of §§11.4–11.10 needs it (the
   report says so at line 4027).  Outside it: the `Σc_i²` width fails for every positive
   correlation (S2); additive extremality fails (D25, D41); the Boltzmann-weight formula is zero
   where the truth is exponential (11.41); the class threshold of a chain is open.
3. **The accuracy scale** ({E}/{F}).  Every "bounded number of evaluations" statement (11.21,
   11.25(b), 11.28, 11.34) is at an *extensive* accuracy — `0.11`–`0.16` nats per site in the
   report's examples; every exponent needs `ε = o(n)` **and** `ln(1/ε) = o(n)` (D29, D35).
   Nothing positive is proved at a fixed (chemical) accuracy for a growing system.
4. **Exact and free side information** ({Q}, partly {?}): exact evaluations, exact independent
   samples of the reference, a known `Z₀`, a fully known known part, computation not counted.
   Bounded errors become accuracy floors (`2τ`, `2βτ`, `βτΣc_i`); stochastic noise and the cost
   of *computing* a cover, a sample or a check (coNP-hard in general) are outside the model.
5. **A hint** ({X}): the costs of §11.10 are those of an algorithm that is handed the instance
   and only has to verify it.  Without it the non-adaptive exponent is larger and the adaptive
   one is reached only with `o(n)` terms that are impractical (§§11.16–11.19, reader AA2); and no
   single algorithm attains the instance-wise costs (hub family).
6. **One reference configuration on a product domain, and weak coupling**, for the second- and
   higher-order reductions ({F}/{X}): on domains with exclusions the class may contain every
   function (11.18c); stars at several references do not combine (11.31(b)); with dense
   constants the cost is `2^{n − o(n)}` (11.32).
7. **Envelope constants are inputs** ({E}): `c_i`, `c_ij`, `c_T`, `Λ`, the inertia bounds.  None
   is certified for a concrete residual in this repository (§8 line 1143–1145, 1174–1177; the
   exception the report names is another division's paper certificate of order-`m` constants
   for one twenty-residue instance, line 1272–1279); the one verified route
   to first-order constants for chains produces constants that grow with the position along
   the chain on every domain (11.36; S6(c)), which empties the format (11.37).
8. **The known part has no structure of its own** in the positive free-energy theorems: `f ≡ 0`
   in 11.25, 11.33(b), 11.34, 11.35, and an additive `f` — unstated in the report — in 11.33(a)
   ({F}: S4, already for a pairwise block ferromagnet).  With a structured known part the hardest instance, the right sampler and even the
   polynomial/exponential boundary change.
9. **Site types fixed as `n` grows, and `κ < 1`**, for "one evaluation or exponentially many"
   ({F}/{Q}: S3; line 1953).  The correct statement is quantitative: the exponent of a
   two-state site is `≈ 0.28·(c/e − 1)` for small margins.
10. **Additive instances and identical sites** ({?}/{P}): every exponent is computed at an
    additive (usually the zero) residual of a homogeneous system.  The lower bounds hold at every
    instance in one-shot form; whether the single-letter formulas describe a non-additive
    instance is not known.

## 6. (c) What could not be classified — the "?"s, ranked by what hangs on them

1. **Exponents and thresholds at non-additive instances** (E19, E25, E39, E40, E49).  All
   single-letter results are at additive instances; the only general statements are the
   one-shot bounds.  Everything the theory says about a *real* residual hangs on this.
2. **The class threshold and the finite-temperature exponents when the known part has
   interactions** (E40, E49, E50; §12 items 1, 2(c), 5): open for chains; the additive candidate
   is refuted (D41).
3. **A known part on a continuous space; hybrid sites** (E44): the torus theorem has `f ≡ 0`.
4. **Evaluations with stochastic noise; average-case correctness** (E34): not treated; bounded
   errors give floors by a one-line argument, variance does not.
5. **Lower bounds for certificates that use the decomposition rules; an approximate version of
   the partition-kernel separation; exponential lower bounds on connected families** (E15, E32;
   §12 item 6).  Until then "the decomposition rules are needed" is proved, "they are enough"
   is not even formulated.
6. **Excluded volume and flexible geometry in the chain no-go** (E46, E47): the growth of the
   verified constants is settled on every domain (S6(c)); the counting of Theorem 11.37 is for
   product domains.
7. **Randomised algorithms and the Hamming ball at prescribed width** (E30(b′)(ii)): a
   conjecture with an outline.
8. **Exponentially small accuracies beyond the cube**, and the bracket of Theorem 11.15 there
   (E25; §12 item 1(c′)).
9. **The complexity of the exact criteria** — "is state `r` of site `i` possibly optimal" (E3;
   §12 item 3) — and the hitting-set claim of 11.18f (E31).
10. Smaller ones: the doubling conversion for `f ≡ 0` (E21); the best `n+1` evaluations in a
    dense second-order class (E42); the interval `[H/√2, H]` for averages (E45); additive
    extremality for open chains without tilt (E7); the droplet criterion beyond nearest
    neighbours (E48); the proved lower constant of the lever-arm law (E46).

## 7. Overstatements — the consolidated list

Sentences that present a result more generally than it is proved.  Severity: **A** = false as
written (a counterexample exists, in the report or here); **B** = a hypothesis that carries the
result is omitted in a summary; **C** = wording.

| # | where | sentence (abridged) | what is proved | sev. |
|---|---|---|---|---|
| O-1 | `README.md` 148–150 | "the lower bounds hold at every instance, so no procedure that is correct on a first-order class can be cheap on any of its subclasses" | at each instance the bound is that instance's covering number; it is 1 at sharp instances, 2 at `c\|x\|` (report 3400–3403), `n+1` on the family of S3 | A |
| O-2 | `README.md` 117–119 | "on product landscapes one evaluation suffices iff every site is sharp; otherwise the number is exponential in the number of non-sharp sites" | additive residual with `κ < 1`, site types fixed as `n` grows; counterexamples: report 1953–1954 (`κ = 1`), S3 (`N_cov = n+1`) | A |
| O-3 | report 1082–1084 (§7) | "one evaluation if every site is sharp and exponentially many otherwise" | as O-2 | A |
| O-4 | report 1496 (row G4) | "one evaluation suffices iff every site is sharp; otherwise the minimal certificate grows like `exp(nR*)`" | as O-2 | A |
| O-5 | report 1966–1969 | "exponentially many in the number of non-sharp sites … in general by the paper proof above" | the paper proof is for finitely many site types | B |
| O-6 | report 2998–3001 | "First-order envelope: … the price is exponential unless the known part is sharp … for every algorithm" | product landscapes of E19 only; at finite temperature exponential also when sharp (2108–2110); not exponential for the RMSD envelope (11.38) | A |
| O-7 | report 2171–2174 | "One reference average … pins `ln Z` to within `β²Σc_i²/8` (Theorem 3.1), and `N` random evaluations estimate it … independently of the size of the state space" | product reference only (D14 [V]; S2: fails for every `ρ > 0`); the paragraph's context is independent sites, the sentence does not say so | B |
| O-8 | `README.md` 143–144 | "A known part turns out to be nothing but the gradient part of an asymmetric envelope" | for minima and their certificates; false for `ln Z` (report 3742–3743; S6(a)) | A |
| O-9 | report 1550–1551 | "the normal form (G13), which shows that the known part was never a separate ingredient" | as O-8 | B |
| O-10 | report 1507 (row G15), 3880–3887, 3898–3900 | "second-order classes have a transition at the Curie–Weiss coupling (polynomial below …)" | additive known part (hypothesis lost, Err-1), binary cube, one dense constant; S4 | A |
| O-11 | report 3920 (title), 1507, 3925 | "Boltzmann averages are harder than free energies"; "uncertifiable on most of their a-priori range"; "almost the whole" | the mean magnetisation, uniform cube, zero residual; 71–87 % | B |
| O-12 | report 1122–1124 (§7) | "A reference average of the residual is exponentially more informative for free energies than the same number of pointwise evaluations" | at the extensive accuracy of the sandwich, product reference, ensembles with entropy (2178–2179 gives the exception) | B |
| O-13 | report 1501 (row G10) | "polynomially many random evaluations where deterministic certification needs exponentially many" | as O-12 | B |
| O-14 | report 3994–3995, 1555–1556 | "the verified chain-rule route of §4.4 cannot certify long chains" | zero residual, additive known part, product domain, fixed `L`, this format | B |
| O-15 | report 3914–3916 | "it is the form of the threshold that applies to torsion-angle coordinates" | `f ≡ 0` and per-angle constants | B |
| O-16 | report 1078, 1091–1092 (§7) | "An architecture is certifiable only through the envelope it exports"; "unbounded Lipschitz constants are incompatible with certification" | true of first-order classes; the second-order classes of §11.7 have no first-order bound at all and are certified by a star | A |
| O-17 | report 3549–3551 | "The statement needs every one of its hypotheses" | necessity shown for two of five (D35, D36); "identical sites" is relaxed in §11.26 | B |
| O-18 | report 3–4 (subtitle) | "… for fixed-sequence articulated SE(3) heteropolymer chains" | `SE(3)` is not defined in the development (819–820); every exponent and threshold of §§11.4–11.10 is for independent sites (4027–4028); chains enter in §4.4, §§11.14–11.15 and §§11.17, 11.22, 11.32 | C |
| O-19 | report 85–87 (§0.3) | "refereed (R2)", "refereed (R3, R4)", "refereed (R6, R_P)" | Err-10 | B |
| O-20 | report 159–160 | "this bound does not grow with the number of pruned conformations" | per round; the total is a sum over rounds (415–417) | C |
| O-21 | report 56, 61, 64 (rows D4, C4, E2) | "[V]" for "(second-order)" and for "`SE(3)`"; "on `m` frustrated triangles" | the Taylor step and `SE(3)` are [P]; disjoint triangles, relative to pairwise-LP leaves | C |
| O-22 | report 1499 (row G7), 3665, 4051, 1100 | exponent "for accuracies that are not exponentially small"; "the picture … extends … to every product landscape of identical sites"; "This settles the conjecture"; "no first-order constant, however small, avoids the exponential price at a non-sharp site" | identical independent sites and an additive instance; thresholds only; a paper proof read by one reviewer; a small enough constant makes the site sharp, and the exponent vanishes linearly in the margin (S3) | C |

Twenty-two items: eight of severity A, ten of B, four of C.  Sections 2–6 contain almost none
(they were rewritten after R1); the summaries (§0.3, §7, §10, `README.md`) contain most.

## 8. (d) Errors found in the report

* **Err-1 (substantive).  Theorem 11.33(a) is false as stated.**  Lines 3877–3887 state the
  polynomial bound for the class `𝒢₂(c₂)` without a hypothesis on the known part — which in
  the setting of §11 (line 1739–1740) is an arbitrary known function `f`; part (b) names its own
  ("for `f ≡ 0`"), part (a) names none.  The source
  (`docs/workstreams/D_REPORT.md`, line 489–493, 516–519) assumes "`f` additive".  For a pairwise
  known part of ferromagnetic blocks every algorithm needs at least `e^{c·n^{1/3}}` evaluations
  at `w = 4`, and for a code landscape exponentially many at every `w > 0` (S4; entry E43).
  Repair: restore the hypothesis, or state Dobrushin's condition for `f + g`.
  (The same failure mode — a hypothesis lost on adoption — is recorded once before, D62.)
* **Err-2 (stale).**  Line 501–503: "Whether additivity survives for *binary* Markov trees is
  open."  Refuted in the same report: line 4081–4083 ("a star (so additivity already fails for
  binary Markov *trees* …)"), §12 item 5 (line 11770–11772), D41.
* **Err-3 (stale).**  Line 3675–3677: the upper bound of the exponent is "the unrefereed claim
  above".  Line 3528–3529 labels it "[P; proof checked by an independent referee]" (R4), and §8
  (line 1162–1163) and `README.md` 141–143 say the same.
* **Err-4 (stale).**  Line 3413–3414: "where between, for adaptive algorithms, is open (§12)".
  §12 item 2(d) (line 11626–11631) and §0.3 (line 88) say it is settled at the level of
  exponents (§§11.18–11.19).
* **Err-5 (stale).**  Line 3292 (table) and 3297–3298: "the exponent itself is known only on the
  cube at the zero residual"; "exact where Theorem 11.25 says so".  Line 3528–3549 claims the
  exponent `R^gen_β` at additive instances of identical sites and concludes that "the values of
  `R^rand_β` quoted after Theorem 11.24 are exact exponents".
* **Err-6 (stale).**  Line 2995–2996: "whether other evaluation sets do better is open".
  Answered twelve lines later (3006–3008) and by Theorem 11.31(a) (line 3837–3838: "no choice of
  evaluation set … escapes the quadratic law").
* **Err-7 (stale).**  Line 3866–3868: workstream D "is under review"; line 3872–3874 reports
  the review.
* **Err-8 (stale).**  Line 3672–3673 and 3679–3680: "nothing is said here about sites of
  several types"; remark (ii) at line 3636–3640 gives the class threshold for finitely many
  site types, and §12 item 2(c) counts it as settled.
* **Err-9 (numbers).**  Theorem 11.38, line 4004–4014.  The display has the lower constant
  "`c ≈ 0.043`" and the upper bound `4.91√(λN ln(e(k−1)n)) + ln(81(n+1))`; the sentence "at
  `n = 1000`, `λ = 1`: between `e^{1.6}` and `e^{235}`" is not their value.  With `c = 0.043` the
  lower end is `e^{1.36}` (`e^{1.60}` belongs to the workstream's constant `0.0506`, which its
  reviewer found not to be delivered by the proof on the stated range: R_G, m1); the displayed
  upper bound is `e^{467}` at `k = 3`, and `e^{235}`
  is the value of the workstream's sharper sum formula, which the report does not display
  (S5, last block: `215.8`, `234.7`, `247.4` for `k = 2, 3, 4`).
* **Err-10 (status cells).**  §0.3, lines 85–87.  "§§11.1–11.9 … refereed (R2)": R2 reviewed the
  section as of `ee2053f`; Theorem 11.18a and Propositions 11.18b–f are later, reviewed by the
  Scientific Discovery Division in part (the duality of 11.18b(e) and parts of 11.18f(c″) by
  nobody).  "§11.10 … the rest paper proofs, refereed (R3, R4)": R3 did not referee Theorems
  11.26 and 11.23(c) (its §6, §7) nor the type-covering step; R4 refereed workstream A's report
  and calls Theorems 11.27–11.28 "outside my brief".  "§§11.7, 11.12, 11.17 … refereed (R6,
  R_P)": those two reports concern §11.17; §11.12 was reviewed by R_E.
* Not errors, recorded for completeness: line 2985–2987 ("two stars at opposite corners do not
  once `n ≥ 6e/c + 6`") is true and weaker than the exact threshold `n > 4e/c + 2` that follows
  from Theorem 11.31(b); `docs/DEAD_ENDS.md` D25 (line 512) and D32 (line 653–654) end with
  "open" items that D41 and D40 close.

No machine-checked statement was found false; the 405 Lean names cited in the two parts exist as
declarations in `proofs/` (S7: a text cross-check, not a compilation); 48 numbers of §§11.4–11.14
were recomputed with independent code and all agree to the digits printed (S5).

## 9. New material of this audit, scripts and commands

All scripts are deterministic (S2 part D is seeded), run in seconds, and print `PASS`/`FAIL`
lines (S5: `OK`/`MISMATCH`); outputs are stored next to them.

| id | script (`experiments/audit/AA1/`) | output | what it establishes |
|---|---|---|---|
| S1 | `aa1_01_envelope_checks.py` | `out_01_envelope_checks.txt` | (a) Theorems 2.3/2.4 fail on a table that is not transitively closed; (b) Theorem 2.7 fails with the separation transposed; (c) Theorem 2.1 fails for a two-to-one map and for `β < 0`; (d) the referee's chain (no single-site or pair dominance, an improving map) and a 3-body example where the term-wise rule is not exact |
| S2 | `aa1_02_sandwich_dependence.py` | `out_02_sandwich_dependence.txt` | the `Σc_i²` width fails for every correlation `ρ > 0` (factor `1+ρ` as `β → 0`; exact, by vertex enumeration of the class); structure-factor growth on chains; the concentration bound of Theorem 11.21 fails for dependent references; **a mixture of `K` product measures keeps the product width with `K` averages** |
| S3 | `aa1_03_near_sharp_sites.py` | `out_03_near_sharp_sites.txt` | **`N_cov = n + 1` exactly with all `n` sites non-sharp** (`δ < 1/n`, `n ≤ 12`, exhaustive); `R*(δ)/δ → 0.2785`; fractional covers at `n = 8`; the `κ = 1` example |
| S4 | `aa1_04_second_order_known_part.py` | `out_04_second_order_known_part.txt` | **Theorem 11.33(a) without an additive known part**: droplets are in the class; Golay-code instance (`n = 24`, 4 096 disjoint sensitive droplets at `w = 4`); Gilbert–Varshamov exponents `R(w) > 0` for every `w`; a *pairwise* known part (ferromagnetic blocks): `2^{n/b}` disjoint sensitive droplets, `exp(Θ(n^{1/3}))` |
| S5 | `aa1_05_numbers.py` | `out_05_numbers.txt` | 48 numbers of Theorems 11.9, 11.15, 11.24–11.28, 11.32, 11.36 reproduced; the bracket of Theorem 11.38 (Err-9) |
| S6 | `aa1_06_misc.py` | `out_06_misc.txt` | (a) the normal form changes `ln Z`; (b) the exact one-anchor interval of `ln Z` on the cube has the a-priori width `nβc`; (c) **inertia of any arm about any line `≥ 0.0267·m b²`**, so verified constants grow at least like `m^{1/2}` on every domain; (d) the cube lower bound of Theorem 11.25(a) at finite sizes |
| S7 | `aa1_07_lean_names.py` | `out_07_lean_names.txt` | the 405 back-ticked Lean names of §0.2, §§2–6 and §§11.1–11.15 are declared in `proofs/` (text cross-check; nothing compiled) |

```
cd /home/user/MetricChain
for k in 01_envelope_checks 02_sandwich_dependence 03_near_sharp_sites \
         04_second_order_known_part 05_numbers 06_misc 07_lean_names; do
  python3 experiments/audit/AA1/aa1_$k.py > experiments/audit/AA1/out_$k.txt
done
```

(One process at a time; the largest, S5, takes about 15 s and well under 200 MB.)

Arguments written out in the entries and not scripted: the measure-theoretic form of Theorem 2.1
(E1); coNP-hardness of exact single-site dominance on domains with pairwise exclusions (E2); the
halves of Theorems 2.3/2.4 that survive on a subclass (E3); bounded evaluation and
sampling errors as accuracy floors (E17, E33, E34); the exact threshold of two opposite stars
from Theorem 11.31(b) (E42); Dobrushin's condition for `f + g` as the hypothesis Theorem 11.33(a)
actually uses (E43).

**Not done.**  `lake` was not run (rule of the brief); the type-covering and Merhav steps behind
Theorems 11.9 and 11.15, Harper's theorem, and the paper proofs of §§11.12–11.15 were not
re-derived — their status is quoted from the referees; the full harness was not re-run (its
stored output was used); §9 of the report was checked only by the name cross-check; nothing of
§§11.16–11.32 was audited (reader AA2), and where those sections are cited as the place where an
assumption is relaxed the citation rests on §0.3 and §10 of the report.

## 10. Counts

Classifications in the 50 entries (an assumption with two tags is counted under both):

| part | entries | {E} | {P} | {C} | {Q} | {X} | {F} | {?} |
|---|---|---|---|---|---|---|---|---|
| I — §§2–6 | 15 | 18 | 4 | 13 | 12 | 3 | 14 | 2 |
| II — §§11.1–11.9 | 18 | 14 | 4 | 5 | 15 | 5 | 21 | 9 |
| III — §§11.10–11.15 | 17 | 20 | 8 | 8 | 12 | 5 | 12 | 12 |
| **total** | **50** | **52** | **16** | **26** | **39** | **13** | **47** | **23** |

202 classified assumptions, 216 tags.  Ten of the {F} classifications rest on examples constructed
and checked here (S1–S4, S6); the others on evidence already in the repository (a Lean
counterexample, a dead-end entry, a harness test, or a later theorem).  Three of the new examples
are facts the repository did not have: the nearly sharp product family with `N_cov = n + 1`
(S3), the failure of the `Σc_i²` width at every positive correlation (S2), and the known parts
(a code landscape; pairwise ferromagnetic blocks) that make second-order classes
super-polynomial at and below the Curie–Weiss coupling (S4).  Two
positive statements are new as well: the `K`-component sandwich for multimodal references
(S2(D)) and the lower bound `0.0267·m b²` on the inertia of any arm (S6(c)).
