# Theorem-to-software register

Living register of the Structural & Computational Biology division (STRUCTBIO), branch
`research/structural-biology`. It records every result this division takes forward, plans, or
has considered and set aside, using the fifteen fields of the founding directive §4
(`OWNER_DIRECTIVES.md`). The synthesis behind it is `RESEARCH_INTAKE.md`. First version:
2026-11-26.

## Conventions

- **Source of each field.** Every field is copied from the intake reports in
  `docs/structural_biology/intake/` (cited as T1, T2, E, S1, S2, N, G, C, with a section) or from
  the coordinator's decisions. Fields the coordinator checked in person are marked
  **(coordinator)**; that list is in `RESEARCH_INTAKE.md` §0. Everything else is "per intake
  reviewer, not re-verified". "Not recorded in the intake reports" means what it says.
- **Status labels.** Labels are the originating repository's own ([V], [P], [K], [N], [C], [M],
  [X], P-exact, …). This register never upgrades them.
- **Reviews.** Every review named here is an **internal review by an AI session or subagent, not
  external academic peer review**.
- **Commits.**
  - Theory rows: field (2) is `eb88823c931953d6455f79c9d8089063abfb442b`, the head read by T1 and
    T2. The Lean sources and the reference checker are identical at the branch point `b2caab6`
    (`STRUCTBIO_UPSTREAM_SYNC.md`).
  - Theory abbreviations: `CA` = `proofs/CertificateAlgebra.lean`, `F/` = `proofs/Frontiers/`,
    BP = `docs/BLUEPRINT.md`, TR = `docs/THEORY_REPORT.md`, RC =
    `experiments/reference_checker.py`.
  - Other heads: ensemble `8d42f609…`, science `71bc661…`, geometry `288b2de…`, engineering
    `96c4fd2…`.
- **Modules.** Modules of this division live under `src/metricchain_sb/`. Modules described as
  "planned" do not exist yet.

---

## Part A — results taken forward or planned

### C1 — Certified GMEC on fixed-backbone rotamer models

**A1. Min-energy kernel K1: soundness and its real-model readings**
1. Division: theory.
2. Commit: `eb88823` (identical at `b2caab6`).
3. Identifier: TR §6.1 Master Soundness Theorem, row E1; Theorem 6.1 (T1 R1; T2 A1).
4. Lean, in `CA`: `Cert`, `verify`, `verify_sound` (CA:308), `certified_optimum` (CA:342),
   `verify_sound_real` (CA:960), `verify_sound_real_symm`.
5. Assumptions: a finite product domain `Dom n k`; rational pairwise tables (`PairInstance`). For
   a real model, the published instance must be ≤ the model entrywise, or bound it through
   symmetrised sums (T1 §2.1).
6. Proof status: [V].
7. Review: referee R1 read the statements ("I found no false theorem") and did not check the build
   or RC (T1 R1). Internal audits D15 and D19 (T2 A1). The coordinator built
   `proofs.CertificateAlgebra` at `b2caab6`. Building is not reviewing.
8. Numerical evidence: 4 `min` vectors; RC fuzz (n ≤ 4, k ≤ 3); kernel runs with n ≤ 6. Kernel
   evaluation exhausted 11.9 GB at 512 entries (T1 §3).
9. Counterexamples / dead ends: `triangle_no_leaf_certificate`, `sumFree_exponential` (T1 §2.1);
   D1, D6, D7, D15, D33; E2 is a known phenomenon (Basu et al. 2023) (T2 A1).
10. Physical interpretation: no assignment in the box has energy below `L` **for the published
    rational tables**; with a witness, the GMEC up to the gap (T1 R1). It is not a statement about
    a force field or about nature.
11. Prerequisites: a producer; exact dyadic or integer tables; a fast checker; an exactness
    convention, either an ε-gap or integrality (T1 §7.3).
12. Software: **C1**.
    - `model.py`: `PairModel`, the published instance.
    - `mincheck.py`: the independent integer checker, with the semantics of `verify` restricted to
      leaf/branch/prune (with `verify_sound_real_symm` for one-orientation pair tables).
    - `gmec.py`: the untrusted producer.
13. Competing methods:
    - toulbar2 and OSPREY emit no checkable proofs;
    - pseudo-Boolean proof logging (VeriPB/CakePB/PBLean; Koops et al. 2025, "within ×20, median
      1.43");
    - "Whether a native format is cheaper has not been measured" (T2 A1, E);
    - reviewers' own knowledge, not in the repository: Rosetta packer, SCWRL4, FASPR, MPLP/TRW-S,
      ILP (T1 R1; S2 G).
14. Useless or vacuous when: the box is empty; the box is not the intended rotamer set; the table
    does not bound the model; the LP gap is large with a huge search tree (T1 R1); the certificate
    tree is exponential (T2 A1).
15. Ready: **implemented (first checkpoint)** for small and medium instances. The producer is
    heuristic and untrusted; the checker is tested, not formally verified.

**A2. LP-dual leaf rule (`LeafOK`)**
1. Division: theory.
2. Commit: `eb88823`.
3. Identifier: leaf constructor of K1; "joint pair leaf" D6 (T2 A1).
4. Lean: `leaf u p m` / `LeafOK` (CA:127), inside `verify_sound`.
5. Assumptions: the messages `m_ij` are supplied. Unary `u_i ≤ h_i(a) + Σ_j m_ij(a)`; pair
   `2·p_ij ≤ J_ij + J_ji − m_ij − m_ji`; `L ≤ Σu + Σp` (T1 §2.1).
6. Proof status: [V].
7. Review: as A1.
8. Numerical evidence: science P7 [M] — "18 gaps in 1 732 models, all closed at depth ≤ 2"
   (S1 H5); "17 of 18 gap models at depth one" (T2 A1). The reports give these labels
   differently: see `RESEARCH_INTAKE.md` §4(b).
9. Counterexamples / dead ends: one leaf cannot certify the frustrated triangle
   (`triangle_no_leaf_certificate`); the pure dual certificate is incomplete (BP §9, T1 §6).
10. Physical interpretation: a reparametrisation (Lagrangian) lower bound per box. Not recorded in
    the intake reports beyond that.
11. Prerequisites: a dual solver emitting messages (T1 §7.1); exact recomputation of `u` and `p`.
    The "float proposes, exact certifies" pattern (E C.2; C D).
12. Software: **C1**, `gmec.py` (an MPLP dual bound from rounded messages). `mincert.py` stores
    only the messages and recomputes `u`, `p` as the largest admissible values.
13. Competing methods: soft-arc-consistency / LP-dual bounds in CFN solvers (E C.2); engineering
    X-012 `leafcert` checks the same rule on the P7 format (E C.2).
14. Useless when: the LP relaxation has a gap, so branching is needed; the dense size is about
    `2P·k` rationals per leaf (T1 §7.4).
15. Ready: **implemented**.

**A3. Goldstein dead-end elimination rule (`PruneOK`)**
1. Division: theory.
2. Commit: `eb88823`.
3. Identifier: prune constructor of K1.
4. Lean: `prune i r t ℓ rest` / `PruneOK` (CA:141, margin 0).
5. Assumptions: `t ∈ D_i`, `t ≠ r`; the per-neighbour bounds `ℓ_j`; continue on `D.remove i r`
   (T1 §2.1).
6. Proof status: [V].
7. Review: as A1.
8. Numerical evidence: not recorded in the intake reports beyond the RC fuzz. T1 notes that no
   stored partition-kind vector has a prune.
9. Counterexamples / dead ends:
    - D1: the Goldstein test is gauge invariant (T2 A1);
    - exact dominance on pruned domains is coNP-hard (T2 C9);
    - pruned non-product domains missed the clash-free minimum in 14 of 40 science analyses
      (SD45; S1 A.3);
    - RC rejects nesting deeper than 30 000 levels (T1 §7.6).
10. Physical interpretation: removal of a rotamer that cannot be in any optimum of the published
    tables.
11. Prerequisites: none beyond the tables.
12. Software: **C1**, `gmec.py` (DEE emits prune nodes); `mincert.py` stores
    `(site, remove, dominator)` only.
13. Competing methods: the DEE family (Desmet, Goldstein, split DEE, MinDEE, iMinDEE), all KNOWN
    (T2 E; S2 G).
14. Useless when: few states are dominated, or the nesting depth exceeds format limits.
15. Ready: **implemented**.

**A4. `sum` rule and split layer**
1. Division: theory; split requested by science (P7-T2).
2. Commit: `eb88823`.
3. Identifier: `sum` constructor; split is TR Prop 11.18b(e)(i) (T1 R2).
4. Lean: `SumOK` (CA:153); in `F/SplitRule.lean`, `SCert`, `verifyS`, `verifyS_sound`,
   `split_leaves_iff_branch`.
5. Assumptions: termwise decomposition of the instance; split only above kernel certificates
   (BP:209).
6. Proof status: [V].
7. Review: split was "written by a subagent under a brief, checked by the coordinator"
   (THY-RES-0014); T1 found no referee report.
8. Numerical evidence: no vector or fuzz case contains a `sum` node; T1's three-case probe behaved
   correctly. Split reduces checks by a factor of 3.8–6.7 (TR:2497) (T1 §3, R2).
9. Counterexamples / dead ends: without `sum`, `m` frustrated triangles need `2^m` leaves; `sum`
   "is *necessary*" (BP:199).
10. Physical interpretation: decomposition into independently certified parts.
11. Prerequisites: component detection. Split needs a schema and checker extension.
12. Software: **C1**, **planned**. `gmec.py` is "without the `sum` rule"; `mincheck.py` covers
    leaf/branch/prune only.
13. Competing methods: not recorded in the intake reports.
14. Useless when: split adds no proving power over `branch` (`split_leaves_iff_branch`).
15. Ready: `sum` partially (in RC, untested there); split no (Lean only).

**A5. Interchange format `metricchain-cert/1` and the reference checker**
1. Division: theory.
2. Commit: `eb88823`.
3. Identifier: BP §4.1; RC `validate` (RC:283).
4. Lean: none. RC is related to the kernels "by tests, not by proof" (T1 §3).
5. Assumptions: rationals ≤ 100 000 characters; uniform `k`; children only for states in the
   domain (T1 §2.11).
6. Proof status: RC "is *not* trusted; the Lean kernels are" (BP:1280).
7. Review: R1 did not check RC. Later internal checks found crashes and misreadings; "No unsound
   acceptance was found" (T1 §3). **(coordinator)** read RC's `min` and `partition` semantics in
   full.
8. Numerical evidence: 16 vectors, 53 hostile inputs, fuzz against brute force (T1 §3).
   **(coordinator)** our checker agrees with RC on 288 mutated certificates.
9. Counterexamples / dead ends: RC accepts `lower_bound = 10⁶` on an empty domain and ignores a
   witness outside the box (T1 §7.9); RC needed 6.0 s for one leaf at n = 60, k = 20 (T1 §7.5).
10. Physical interpretation: none.
11. Prerequisites: none.
12. Software: **C1**, `mincert.py` (exact conversion `to_metricchain_cert1`); RC is used as an
    external oracle in `tests/structbio/test_mincert.py`, unmodified (`STRUCTBIO_UPSTREAM_SYNC.md`
    "Imports").
13. Competing methods: VeriPB/CakePB proof formats (S2 A).
14. Useless when: instances are large, because RC loops over all `n(n−1)k²` entries (T1 §7.5).
15. Ready: **in use** as an oracle at small sizes.

### C1b — Certified per-residue stability of the GMEC (design)

**A6. Robust optimality / sharp minimum, and certified one-residue gaps**
1. Division: theory.
2. Commit: `eb88823`.
3. Identifier: TR A1–A4, Cor. 4.7 (T2 A2); BLUEPRINT §6.6 Step 1 (coordinator's decision; outside
   the BLUEPRINT sections the coordinator lists as read).
4. Lean, in `F/EnvelopeDuality.lean`: `robust_certified_iff`, `robust_minimizer_iff`,
   `robust_min_interval_exact` (T2 A2; N B for `robust_certified_iff`). `single_evaluation_certificate_iff`
   is in `F/CertificateComplexity.lean` by file search; it is named in no intake report. Gaps use
   `verify_sound` on boxes `D.fix i a`.
5. Assumptions: the perturbation satisfies `g(x) − g(y) ≤ d(x,y)` with per-site constants `c_i`
   (T2 A2); the incumbent passes the sharp-minimum test, i.e. one `min` certificate on
   `E₀ − Σ_i δ_i(x̂_i, ·)`.
6. Proof status: [V] for the declarations listed by T2. `single_evaluation_certificate_iff`: not
   recorded in the intake reports.
7. Review: R1; SCI-REV-0006 classes the envelope duality "known in substance" (D24) (T2 A2, E).
8. Numerical evidence: synthetic benchmarks B1 only (T2 A2).
9. Counterexamples / dead ends:
    - D2: iMinDEE is the one-anchor special case;
    - D28 / Thm 11.9: certificate count is exponential in non-sharp sites (T2 A2, C2);
    - RC has no `certified_gap` (T1 §7.9).
10. Physical interpretation: robustness of the minimum of the tables to a stated uniform
    perturbation, which addresses B5's "is the certified minimum meaningful" (S1 D, G.8). It is
    not a statement that the perturbation bounds the real model error.
11. Prerequisites: K1 only.
12. Software: **C1b**, **planned**: a stability module calling `gmec.py` and `mincheck.py`.
13. Competing methods: iMinDEE, MinDEE range terms, robust optimisation (T2 A2).
14. Useless when: the uniform margin is below any physically stated model uncertainty — science
    puts the relevant accuracy at "about `1.7 k_BT` on differences" (S1 C). Also useless when no
    site is sharp.
15. Ready: **design**.

### C2 — Certified partition functions, free energies, populations (in progress)

**A7. Partition kernel K3 (elementary rules)**
1. Division: theory.
2. Commit: `eb88823`.
3. Identifier: TR §3.1, §3.4, rows D1, D3 (T1 R4).
4. Lean, in `F/PartitionCertificate.lean`: `ZCert`, `zverify`, `zverifyTop_sound`, `zprune_sound`;
   `thermal_dee`.
5. Assumptions: nonnegative weights, checked at the top level (T1 §2.3).
6. Proof status: [V].
7. Review: R1, "sound but 'too weak for the stated application'" (T1 R4). Prior-art class (5) "new
   combination" (SCI-REV-0006; T2 A3). **(coordinator)** read RC's `partition` semantics.
8. Numerical evidence: 4 partition vectors; fuzz; harness I.5, I.6; B6 (n ≤ 6) (T1 R4).
9. Counterexamples / dead ends: D22, exponential on chains; `negativeW_unguarded` (T1 R4).
10. Physical interpretation: a two-sided bound on `Z` of the rotamer box of the published weights.
11. Prerequisites: weight tables (A9); a producer.
12. Software: **C2**, **planned**: Z-certificate module and checker.
13. Competing methods: toulbar2 `Z*_ε` (deterministic (1+ε)), K*/BBK*/MARK*/EWAK*, mini-bucket,
    TRW; verified counting checkers (CPOG, Tan et al. 2024, Cheng–Luo–Jiang 2024) (T2 A3; S2 G).
14. Useless when: the interaction graph is dense — leaves are loose and enumeration is exponential.
15. Ready: partially.

**A8. Extended partition kernel K3′ (cut, elimination)**
1. Division: theory.
2. Commit: `eb88823`.
3. Identifier: TR Theorems 11.19, 11.20, row G9 (T1 R5).
4. Lean, in `F/PartitionProduct.lean`: `ZCert2`, `zverify2`, `zverify2Top_sound`, `CutOK`,
   `Elim1OK`, `Elim2OK`, `WInstance.Z_cut`, `Z_elim1`, `Z_elim2`, `chainCert`,
   `zverify2Top_chainCert`, `chain_separation`. **(coordinator)** read the definitions and the
   soundness statement, and built the module.
5. Assumptions: nonnegative weights; an eliminated site has ≤ 2 neighbours on the box.
6. Proof status: [V] for soundness and for every chain; [P] for treewidth ≤ 2 in general (T1 R5).
7. Review: §§11.1–11.9 refereed by R2, with reservations M4 (D33) (T1 R5).
8. Numerical evidence: kernel runs on a 6-site chain, a tree and a ring; harness XI.12.
9. Counterexamples / dead ends:
    - D33: separations hold only for exact lower ends and are representation-dependent;
    - thermal prune exists only inside `base`, so it cannot precede cut or elimination (T1 §2.3;
      the coordinator read `ZCert2`);
    - no end-to-end theorem names `ZCert2` (T1 §4.6).
10. Physical interpretation: a transfer-matrix computation written as a certificate.
11. Prerequisites:
    - JSON nodes, absent from the schema and RC;
    - a tabulating checker ("In Lean the new instances are closures, not tables");
    - an elimination-order producer.
12. Software: **C2**, **planned**. The checker of this division's extension (A14) contains these
    rules.
13. Competing methods: bucket/variable elimination, weighted model counters (T1 R5); SCWRL4 / Xu–
    Berger tree decomposition (S2 G, from memory).
14. Useless when: treewidth > 2, the general protein case (T1 §7.7).
15. Ready: partially (Lean only).

**A9. Numeric layer and the interval → Z pipeline**
1. Division: theory.
2. Commit: `eb88823`.
3. Identifier: TR §5 (row B1), §3.4 (T1 R3).
4. Lean:
    - `proofs/Core/Rounding.lean`: `roundDown`, `roundUp`, `QInterval.*`, `expLo`, `expHi`,
      `exp_enclosure`, `contains_boltzmann`;
    - `F/PartitionCertificate.lean`: `Z_encloses_partitionFn`;
    - `F/IntervalInstance.lean`: `WInstance.lowerOfIntervals`, `upperOfIntervals`,
      `certified_partition_of_intervals`.
5. Assumptions: `N ≥ 1`, `|q| ≤ 2^K` for every entry, rational β; `expLo > 0` needs `N ≥ 4`.
6. Proof status: [V].
7. Review: R1 checked `Rounding.lean` only by "two spot checks" (T1 R3).
8. Numerical evidence:
    - `rounding_check_1…33`;
    - triangle `Z ∈ [2.3068, 2.3069]`;
    - T1's re-implementation measured numerators of ~5 400 to ~50 000 bits, and 10⁵–9·10⁵ with
      extra halvings (T1 §4).
9. Counterexamples / dead ends: a clash entry forces a large uniform `K`; RC rejects rationals over
   100 000 characters; the rounded variant is "an unwritten two-line lemma" (T1 §4).
10. Physical interpretation: rigorous Boltzmann-factor brackets.
11. Prerequisites: big-integer arithmetic; outward rounding after `exp`.
12. Software: **C2**, **planned**: weight-enclosure module, with outward-rounded weights (A14).
13. Competing methods: MPFI/Arb (reviewer); LeanCert, girving/interval (T1 R3).
14. Useless when: weights are unrounded (impractical sizes).
15. Ready: yes as a library; partially as a pipeline.

**A10. Thermal dominance and observables under pruning**
1. Division: theory.
2. Commit: `eb88823`.
3. Identifier: row D1, §3.1 (T2 A4).
4. Lean, in `F/Dominance.lean`: `boltzmannAvg_prune_error` (T1 §2.7), `thermal_dee`;
   `partition_transport`, `freeEnergy_prune_bracket`, `partition_prune_bracket_fibers`,
   `boltzmannAvg_dominance_error` (T2 A4).
5. Assumptions: a dominance margin `γ`; an injective or `m`-to-one map; or discarded weight ≤ a
   fraction `ρ` of the survivors.
6. Proof status: [V].
7. Review: R1; L1 C3 (T2 A4).
8. Numerical evidence: synthetic B-series.
9. Counterexamples / dead ends: D18 (the factor was asserted before it was proved).
10. Physical interpretation: pruning changes `ln Z` by ≤ `ln(1+m e^{−βγ})` and a bounded
    observable by ≤ `2Bρ`.
11. Prerequisites: exact dominance margins.
12. Software: **C2**, **planned**: the prune-before-elimination rule (A14) and observable error
    bars.
13. Competing methods: K*'s `p*` bound; pruning in `Z*_ε` (T2 A4).
14. Useless when: `γ ≲ kT` or `m` is large.
15. Ready: yes as a kernel rule. The bound is "inequality folklore"; as a certificate rule, "NO
    MATCH FOUND" (T2 A4).

**A11. Free-energy and partition-ratio sandwiches (weak pairs)**
1. Division: theory.
2. Commit: `eb88823`.
3. Identifier: Thm 3.1 (T2 B).
4. Lean: `free_energy_sandwich`, `partition_ratio_sandwich` in `F/FreeEnergySandwich.lean`.
   **(coordinator)** read the statements.
5. Assumptions: as stated in the Lean file, not reproduced by any intake report. T2: the width
   `β²Σc_i²/8` holds for a product reference (D14).
6. Proof status: [V] (T2 B).
7. Review: not recorded in the intake reports.
8. Numerical evidence: not recorded in the intake reports.
9. Counterexamples / dead ends:
    - D14;
    - "for any reference, vacuous once `βΣc_i>8`" (T2 B; AUD §5);
    - "Do not use the `Σ c_i²` width with a correlated reference: it is false there" (BP:460,
      T1 §6);
    - the width fails for every correlation ρ > 0 (T2 C14).
10. Physical interpretation: a second-order treatment of weak pairs relative to a reference.
11. Prerequisites: bounds on the weak-pair energies.
12. Software: **C2**, **planned**.  **Resolved by the coordinator, 2026-11-26:** only the
    *range form* is used — `partition_ratio_sandwich` (read at theory `b2caab6`,
    `proofs/Frontiers/FreeEnergySandwich.lean`): for any reference energy `E₀` and any `Δ` with
    `a ≤ Δ ≤ b` pointwise, `−β⟨Δ⟩₀ ≤ ln(Z/Z₀) ≤ −β⟨Δ⟩₀ + β²(b−a)²/8`.  The `Σc_i²` width is
    **not** used: it needs a product reference (D14), and our reference (the strong pairs) is
    correlated.
13. Competing methods: McDiarmid/Rio (known) (T2 B, E).
14. Useless when: `β(b−a)` exceeds about 3, where the width passes one nat and soon exceeds
    the first-order width `β(b−a)` itself (at 8).  Measured (RESULTS R-3): for the weak pairs of
    ubiquitin `β(b−a)` is 4 to 113 depending on the threshold — the rule is vacuous there; on
    crambin at the 0.03 kcal/mol threshold it gives 0.23 nats against 1.36 at first order.
15. Ready: **yes as a rule; of limited use** — it needs the reference mean `⟨Δ⟩₀` enclosed
    (pair marginals of the reference), and it is the subject of the open question Q-5 of
    STRUCTBIO-REQ-0003.

**A12. Population and marginal intervals**
1. Division: theory (inference) and science.
2. Commit: `eb88823`; science `71bc661` (A17 (13)).
3. Identifier: science addendum A17 (13) (S1 A.7; S2 B).
4. Lean: none. The only theorem of ratio type is `box_trap_certificate` in
   `F/KineticsCertificates.lean` (T1 §4.7).
5. Assumptions: per-state enclosures `[lo_a, hi_a]` from a root branch on site `i`; `lo` from `I⁻`,
   `hi` from `I⁺` (T1 §4.7).
6. Proof status: T1 calls it "my inference"; science labels it "[P, elementary]" (S2 B).
7. Review: science's populations are unrefereed (S2 B).
8. Numerical evidence: science gets all 60 rotamer populations of Val₂₀ within a relative 1.2 %,
   and 1 542 exact populations inside their intervals (S1 H4).
9. Counterexamples / dead ends: none recorded.
10. Physical interpretation: rotamer-model populations, "not of a molecule" (S2 F).
11. Prerequisites: a checker that exposes per-child intervals; `zverify` returns only the root
    interval (T1 §4.7).
12. Software: **C2**, **planned**.
13. Competing methods: "any two-sided Z bound gives this" (S2 H2); Kamisetty–Xing–Langmead 2008
    (S2 G, from memory).
14. Useless when: per-state intervals overlap widely.
15. Ready: partially (the formula only). A lemma has to be written.

**A13. Science's certified sandwich line (reference, not imported)**
1. Division: science, P3–P9 and A17.
2. Commits: `a841cb4…` (P3), `c1b710c…` (P6), `90abf0e…` (P9), `59e88bc…` (A17.23) (S1 H3–H7).
3. Identifier: P3 Prop 1, Theorem 3, Theorem 5; P6 Lemmas A, A′; A17.19; A17.23.
4. Lean: skeleton only.
    - Science: `ws_L4/RemainderIdentity.lean` (`remainder_identity`, `allocation_lemma`,
      `anchored_sandwich`);
    - theory: `AnchoredRemainder.lean`, `ShareLevels.lean`, `GibbsRecovery.lean`,
      `ResolvedPenalties.lean`.
5. Assumptions:
    - a fixed ideal backbone and the P2 grid;
    - a product or reset-closed domain;
    - the ball fully evaluated;
    - a band;
    - `ε_g = 10⁻⁷` kcal/mol, "not proved";
    - a double-precision transfer matrix.
6. Proof status: "[P] … not machine-checked" for the constants; [V] for the skeleton (S1 A.6).
7. Review: the coordinator re-derived statements; R19 reviewed A17 (19)–(20); much is unrefereed
   (S1 H3–H7).
8. Numerical evidence: Val₂₀ `[518.2332, 518.2937]`; 160 enumerated runs; 5 512 504 checks
   (S1 A.6).
9. Counterexamples / dead ends: the helix; (LKSE)₃ at order 3; pruned domains (SD45) (S1 A.8).
10. Physical interpretation: `ln Z` of a rotamer model, "not a hydration free energy" (S1 H3).
11. Prerequisites: G-3 (tree decompositions), "not written, not built" (S1 G.7).
12. Software: **C2** treats this as the chain/band, residual-class reference. C2 is the
    general-graph counterpart and **does not replace it**. Nothing is imported.
13. Competing methods: MARK*, K*, `Z*_ε`, mini-bucket (S2 H1).
14. Useless when: the interaction graph is not banded (S1 H3, reviewer's inference); the floor
    delocalises.
15. Ready: not for public structures (S2 H1).

**A14. STRUCTBIO extension: general elimination on factor tables (to be formulated)**
1. Division: STRUCTBIO, to be sent to theory.
2. Commit: not yet written.
3. Identifier: none yet.
4. Lean: none yet. The coordinator plans to machine-check it "where practical". The toolchain
   builds on our machine.
5. Assumptions, as designed:
    - nonnegative factor tables of any arity;
    - a product-form relaxation of weak pairs;
    - prune before elimination;
    - outward-rounded weights.
6. Proof status: none (design).
7. Review: none. To be requested from theory.
8. Numerical evidence: none.
9. Counterexamples / dead ends: the treewidth-2 limit of `WInstance` (A8); bit growth (A9).
10. Physical interpretation: as A7.
11. Prerequisites: an elimination-order heuristic (min-fill after DEE; C G2).
12. Software: **C2**, **planned**: the extension checker and producer.
13. Competing methods: junction-tree exact `Z`; toulbar2 BTD (S2 G).
14. Useless when: the factor tables are of size `q^{w+1}` with large treewidth (C G2).
15. Ready: **no**.

### C3 — Ensemble partial-identification certifier (priority 2)

**A15. Exposing certificates, stability and forward-model error (ensemble E1, E1.1, E2, E2.3)**
1. Division: ensemble. E2.2 (a) is attributed to science.
2. Commit: `8d42f609`; first stated at `a570520` / `1a067b5` (N B).
3. Identifier: E1, E1.1, E2, E2.3 (`ENSEMBLE_REPORT.md` §2.1–2.2).
4. Lean, in namespace `MetricChain.Ensemble`, `proofs/Ensemble/`:
    - `eq_of_exposing_certificate`, `mass_off_support_le`;
    - `transport_le_of_sharp`, `identification_of_robust_certificate`,
      `robust_certificate_of_sharp`, `residual_advantage_le`, which use theory's
      `robust_certified_iff`.
5. Assumptions: finite `X` (Lean); the library is exhaustive; forward-model error
   `sup_x‖Φ̃−Φ‖ ≤ η` adds to `τ` (E2.3).
6. Proof status:
    - E1: P, with the "if" direction V;
    - mass bound V, TV bound P;
    - E2 (c) V for finite `X`;
    - E2.3 P (N B).
7. Review: ER1 found E1 and E2 correct; E2.2 and E2.3 are "ER2-pending".
8. Numerical evidence: T1 (1 500 instances, 1500/1500 agreement); T2 (400 instances).
9. Counterexamples / dead ends: ED12 ("identified ⇔ exposed" false both ways); E1.2 is only
   Hölder-½ stable on a continuum.
10. Physical interpretation: a support is identified iff it is exactly the ground-state set of an
    energy in the span of the observables.
11. Prerequisites: an explicit `X` and feature matrix `Φ`; verifying `γ` is a minimisation over `X`
    (N C).
12. Software: **C3**, **planned**: an exact-rational LP certificate module (`exposedness_checks.py`
    as reference, read not copied).
13. Competing methods: the Donoho–Tanner face criterion; MaxOcc/maximum occurrence; BME, EROS,
    maximum entropy — not searched by ensemble (N F). Novelty is not established.
14. Useless when: the truth is not in `X`; `η` ≥ data accuracy; `|X|` is exponential (N G.1).
15. Ready: yes for finite libraries (N B). A forward-model error budget is needed before real data.

**A16. Partial identification with noise: flow certificate, minimax modulus, falsification (ensemble E13, E17; science Theorem 8, §8)**
1. Division: ensemble (E13, E17) and science (Theorem 8).
2. Commit: ensemble `8d42f609`; science `9d358cb` (S2 H5).
3. Identifier: E13, E17; `INFERENCE_LIMITS.md` §§8–9, Theorem 8.
4. Lean:
    - E13, E17: none;
    - science, in `ws_L1/IdentifiedSets.lean`: `modelFree_certificate_sound`,
      `divergenceBall_certificate_sound`, `envelope_flow_sound_gibbs`,
      `kl_lower_bound_certificate_sound`, `falsification_sound_gibbs`, `theorem8c_falsification`.
5. Assumptions: a convex compact class; Gaussian noise `σ`; a linear target (E17). Theorem 8 needs
   `D` closed. For kernel checking, `ψ, Φ` must be pairwise in the site variables (S2 B).
6. Proof status:
    - E13 P; E17 P (elementary), K (Donoho 1994);
    - Theorem 8 [P], with duality [K] and soundness [V] (S2 B, H5).
7. Review: E13 and E17 "ER2-pending"; Theorem 8 by R3.
8. Numerical evidence: F3, F5 (duality gap `5·10⁻¹⁵`); lattice chains of ≤ 10 to 27 beads (S2 H5).
9. Counterexamples / dead ends: E13's constants are "measured, not certified"; ED16.
10. Physical interpretation: the range of a property consistent with the data, and a lower bound
    on model error "independent of sampling".
11. Prerequisites: an LP or SOCP over `X`.
12. Software: **C3**, **planned**.
13. Competing methods: MaxOcc/maxOR, Christensen–Connault, OUQ (S2 H5); BME/EROS point estimates
    (N B).
14. Useless when: intervals are routinely trivial; `ω(2σ)` ≈ the range of `ψ`; noise is
    non-Gaussian.
15. Ready: E17 "yes for finite `X`" (N); the science model-free and KL-ball versions are "ready"
    (S2 H5); the envelope version is research.

### C4 — Geometric observability analyser (priority 3)

**A17. Local-data softness and identifiability ranks (geometry Theorems K, H)**
1. Division: geometry.
2. Commit: `288b2de`.
3. Identifier: Theorem K (G2.1–G2.4); Theorem H (G1.19, G1.20).
4. Lean: none.
5. Assumptions: K applies to any configuration, with sequence-local distances `|i−j| ≤ K`. H needs
   unit bonds and cos −5/13 or −1/3.
6. Proof status: K is P, with the exact helix scaling N; H is P-exact for K ≤ 8.
7. Review: K is "not reviewed"; SCI-REV-0023 found K(a) "a direct corollary of a printed
   statement". H was reviewed by REV-0001.
8. Numerical evidence: `local_data_bounds.py`; `exact_jacobian_rank.py 8` (G B8, B11).
9. Counterexamples / dead ends: DG-10 (local ≠ global); a length-independent constant needs
   `K ≳ n^{2/3}`.
10. Physical interpretation: backbone-local restraints cannot pin global shape; the softest modes
    are what the data cannot see.
11. Prerequisites: an SVD of the rigidity matrix; Jacobian rank mod p.
12. Software: **C4**, **planned**: `geomlib`-based (read, not copied); heterogeneous geometry and
    PDB input are needed (G D).
13. Competing methods: FIRST/KINARI, elastic-network normal modes, DMDGP — none mentioned by
    geometry (G F).
14. Useless when: analysis is only infinitesimal (s₇ is local) (G G-1).
15. Ready: "Yes" for s₇ / C_inf (G B11); H partially.

**A18. Handedness gaps, hinge mirror candidates, measurement-pattern connectivity (geometry Theorems L, M, J)**
1. Division: geometry. Theorem M is "Science division first".
2. Commit: `288b2de`.
3. Identifier: Theorem L (G2.5, G2.6); Theorem M / Prop M2 (G3.1–G3.5); Theorem J (G1.27).
4. Lean: none.
5. Assumptions:
    - L: τ > 0, `|η_jk| ≤ τ⁴/(73D²)`;
    - M: two states and conic-free segments;
    - J: generic ensembles and all `i,i+3` / `i,i+4` laws, relying on ensemble E5/E6, which are
      unrefereed.
6. Proof status: L is P; M is P, with counts P-exact; J is P given E5/E6.
7. Review:
    - L: "not reviewed"; SCI-REV-0023 is prior art and relevance only;
    - M: "two independent derivations agree";
    - J: REV-0001, "correct given E5/E6".
8. Numerical evidence: `local_data_upper.py` (360 pairs); the hinge scripts;
   `matroid_connectivity.py`.
9. Counterexamples / dead ends: the tail reflection (S) cannot be dropped; three states at two
   hinges can fail (N).
10. Physical interpretation: where handedness is resolvable at a stated error
    (`G = min 4|h⁻h⁺|`); mirror "ghosts" of hinge motions.
11. Prerequisites: O(n) evaluation; a small LP; modular rank.
12. Software: **C4**, **planned**, as diagnostics only.
13. Competing methods: Arias-Castro–Vishwanath; thin-rod rigidity; DMDGP reflection symmetry
    (G F).
14. Useless or vacuous: L at realistic geometry needs ≈ 1.3·10⁻⁴ Å errors (SCI-REV-0023 §5); with
    inexact or state-dependent bond geometry, "nothing is proved" (G §12).
15. Ready: partially; L only as a scaling statement.

---

## Part B — considered and not taken forward now

| result | precise reason (source) | what would change the verdict |
|---|---|---|
| **C5:** K2 residual kernel `verifyITop_sound`, `IProblem.consistent_iff_nonempty` ([V]) | "no first-order constant is certified for a concrete residual anywhere in the repository" (T2 A2; AA1 E14); D28, D42 | certified `c_i` for one real term, e.g. by interval evaluation of a force-field term |
| **C5:** share certificates and third-order models (`secondOrder_certified_of_state_shares` in `F/StateShares.lean`; `verify_sound_thirdOrder` in `F/ThirdOrderModel.lean`) | constants "exact maxima over enumerated domains, **not certified constants**" (T2 A6, A7); completeness fails on non-product domains (D59); Thm 11.18a "not refereed". With `c = 0`, shares certify a pairwise GMEC when the LP is tight (T1 R7, reviewer's inference) — a possible cheap C1 leaf, not yet assessed | certified `c_ij` / `c_T` (T2 F.1) |
| **C5:** science P-series constants (P3, P8, P9) | [P] by one workstream; "code not reviewed"; `ε_g` unproved (S1 A.5–A.7) | independent review and an outward-rounded evaluator (P3-E2) |
| query-complexity and exponent theory (Thms 11.6–11.9, 11.15, 11.33, 11.44–11.58a; §§11.20–11.26) | idealised classes (uniform cube, zero known part); asymptotic; "worse than plain Monte Carlo" at simulable sizes (T2 B, D) | finite-size constants on a rotamer class |
| voxel / continuous-rotamer enclosures (`voxel_boltzmann_bounds`, `pairwise_voxel_weight_bounds`, `certified_torsion_partition_top`) | interval evaluation of force-field terms "is not built"; `d^{d/2}` cost (T1 R8; T2 A5) | a verified interval evaluator for LJ/Coulomb over χ cells |
| barrier and macro-ratio certificates (`bverify_sound`, `macro_le_of_plan`) | no JSON/RC entry point; plans as large as the macrostates; "not refereed" (T1 R10; T2 A10, A11) | a schema plus a checker, and a size bound on realistic move graphs |
| linear/profile kernel (`verifyLTop_sound`) | profile class too small, constants vacuous (`10^{93}`–`10^{2697}`); kernel Lean-only and "not refereed" (T1 R9; T2 A12, B) | engineering THY-REQ-0004 delivered, and a real feature map with small coefficient boxes |
| STRANDS, NANUQ (complexity CX-T1–T14, T24, T30; T5–T9, T13, T26, T27) | nucleic acids and phylogenetics; "No protein application" (C B, C) | none expected. CX-T30 digit extraction is noted as a technique (C G1.5) |
| Ising ground-set theorems (CX-T16–T19, T28, T29) | ±1 spins on a complete graph; rotamers are q-ary on sparse graphs; T28/T29 unreviewed (C B7–B9, G3) | a q-ary local-polytope analogue. Until then they are design heuristics only (a posteriori tightness tests) |
| penalty-threshold bracket (CX-T21–T23) | product reference only; "void" on science's floors; unreviewed (C B11, B12) | review, and a band-reference version |
| ensemble positive theorems under exact idealised observables (E5–E8, E7′, E9–E12, E19, E20–E21) | exact laws, generic conformers; Part VI "read by nobody but its author"; no modulus under bands (O4) (N B, G) | a stability modulus under banded laws; review of Part VI. Negative diagnostics may enter C4 or C3 tests |
| geometry Theorems A–G, I (mixture identifiability from ⟨r²⟩) | exact, state-independent bond geometry; ⟨r²⟩ observable; κ uncertified (O-5) (G B1–B9) | certified κ and a perturbation theory for inexact geometry; meanwhile the witnesses serve as benchmark negatives (G G-3) |

---

## Part C — traceability for C1 (worked example)

| link | content |
|---|---|
| **theorem** | `verify_sound` (CA:308): `verify c I D L = true → ∀ x, InBox D x → L ≤ I.energy x`; with `verify_sound_real_symm` for one-orientation pair tables. Label [V]; not refereed beyond R1's reading of the statements (T1 R1) |
| **assumptions** | a finite product box of per-site rotamer lists; exact rational (dyadic) unary and pair tables; nodes leaf / branch / prune only; no `sum` and no `split` |
| **representation** | `model.py` `PairModel`: integer tables in units of `2**-scale_bits`, pair tables stored for `i < j`, ragged domains inside a common alphabet. `mincert.py`: compact format `structbio-mincert/1` (leaf = messages; prune = `(site, remove, dominator)`) with exact conversion to `metricchain-cert/1`; `u`, `p`, `ℓ` are recomputed as the largest admissible values, so both formats accept exactly the same claims |
| **implementation** | producer `gmec.py`: untrusted — Goldstein DEE, floating-point MPLP dual, ICM incumbents, depth-first branch and bound; claims `L = U − ε`. Checker `mincheck.py`: integer additions, minima and comparisons only; magnitudes ≤ `2**62` checked before arithmetic; never raises. Baseline `baselines/toulbar2.py`: same integer instance, no checkable certificate (label [H] for us) |
| **verification** | `tests/structbio/test_mincert.py`: (i) exact agreement with exhaustive enumeration on small instances; (ii) acceptance by the theory division's reference checker after conversion; (iii) agreement of both checkers on mutated certificates (288, coordinator), and no false bound accepted; (iv) rejection of out-of-range magnitudes. Also: rejection after raising `L` by one unit; serialisation round trip; checksum sensitivity. The checker implementation is **tested, not formally verified** |
| **benchmark** | Level 0–1 done locally. Levels 2–4 are to be specified in `docs/structural_biology/BENCHMARK_MASTER_PLAN.md` (not yet in the tree at this date) and requested from engineering (E-2, Q-14 / BM-2, science B2/B5), with toulbar2 and pseudo-Boolean proof logging as comparisons |
| **interpretation** | model-conditional: a certified minimum of the published rational tables — **not** of a force field and **not** of nature. The step from a force field to the tables is the producer's obligation (BP:48) and is not certified. A certified optimum is not a predicted structure (S1 C; science `PHYSICAL_APPLICABILITY.md` §6) |

---

## How this register is maintained

- Every new capability gets rows here **before** code is written.
- A status, a review entry or a readiness verdict changes only with a dated line: date, commit,
  source and what changed.
- Labels are copied from the originating repository and are never upgraded by this division. A
  computation never upgrades a mathematical status.
- Each synchronisation (`STRUCTBIO_UPSTREAM_SYNC.md`) re-checks the commits in field (2) and
  records any changed statement.
- Contradictions between sources stay visible (`RESEARCH_INTAKE.md` §4) until resolved by a dated
  entry.
