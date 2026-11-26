# STRUCTBIO intake C: Mathematical Biology and Computational Complexity division

Reviewer: STRUCTBIO research-intake (read-only). Source: worktree `wt/cx`, branch `research/biological-complexity`, head commit **`25bcd61d362ee860bf02845f062b150314aa916b`** ("Lean: Corollary 5' on six points kernel-checked (CX-V5); companion note on higher levels (draft)"). Worktree clean (`git status` empty), and I changed nothing in it. I ran no Lean and no Python. Every claim below comes from the files named. Text marked **[my inference]** or **[standard, from memory]** is mine, not the repository's.

Repository labels (from `docs/complexity/README.md`): **[V]** Lean-kernel-checked · **[P]** paper proof · **[K]** known, cited · **[N]** numerical · **[X]** exact finite computation (integer/rational) · **[C]** conjecture. Every "review" is an **internal AI adversarial review** (COMPLEXITY-REV-0001…0004, subagents the division commissioned itself), plus one cross-division review (SCI-REV-0019, science division). The repository says explicitly that none of these is academic peer review.

---

## A. Problems worked on, and the published open problems they address

Mandate (README): open problems in theoretical computational biology, statistical mechanics and complexity; "abstract combinatorial models … synthetic instances only." All work dates from one session, 2026-11-26.

| # | Problem (precise) | Published source / requester | Repository status label | Reviews |
|---|---|---|---|---|
| A1 | **STRANDS hardness.** Decide MFE ≤ k for a multiset of DNA/RNA strands in the multi-strand **unpseudoknotted nearest-neighbour (NN)** model (connected structures, association + rotational-symmetry terms). Also #SSEL (count of structures at a given energy) and the partition function (PF). | Ducloz–Shalaby–Woods, DNA 31 (2025), "Future work" 1 (`OPEN_PROBLEMS.md` A1) | "OPEN, partly ILL-POSED" in the literature; ours **OURS-[P], internally reviewed twice, not peer reviewed**; "apparently unpublished" | REV-0001 "correct with gaps"; SCI-REV-0019 correct; REV-0003 additions correct |
| A6 | **STRANDS algorithm.** Magnified NN partition function summed over **all circular strand orderings**, with symmetry, avoiding the (c−1)! factor. Also whether c can grow past O(1). | Shalaby–Woods arXiv:2611.27945v2 (preprint, 23 Nov 2026), Future work 3, 4 | **OURS-[P], validated [X], reviewed (REV-0003: correct)**. For the base-pair model this is **already Boehmer et al., AMB 2025, Thm 4**; only the NN version is theirs | REV-0003 |
| A2 | Is the NN model PF-polynomially magnifiable? | DSW Future work 2 | **SOLVED-ELSEWHERE** (Shalaby–Woods 2026), dead end CX-D1 | — |
| A3′, A4, A5, A7 | PF hardness at fixed temperature; log-precision; returning MFE structures; pathway encoding | DSW / SW26 | OPEN (A3′ active, no approach; A4/A5 queued; A7 ill-posed) | — |
| B1–B3 | **NANUQ.** Is the NANUQ inter-taxon quartet metric of outer-labeled planar galled semi-directed phylogenetic networks circular decomposable with support = displayed splits, for all level-2 networks (B1), level-3 bloblets (B2), and a parametric family (B3)? | Holtgrefe et al., Bull. Math. Biol. 2025, §6 conjectures | **CLAIMED-ELSEWHERE** (unreviewed third-party "vibemathed" entry B-II, 30 Sep 2026); ours: **OURS-[P]+[X], finite inputs [V], probably a rediscovery** (CX-D5) | REV-0002, REV-0004 |
| D1 / E-C1 | **Ising ground sets.** Given K sign vectors in {±1}ⁿ, is there a pair energy E_J (all pairs, optionally fields) whose ground-state set is *exactly* these vectors, i.e. do they form a face of the cut polytope ("exposed")? Is this co-NP-hard? | Ensemble division (ENSEMBLE-MSG-0003 §4), not a published problem | fixed K: linear time; K=O(log n): polynomial; **general K: hardness OPEN**; degree-2-SOS variant **co-NP-complete (unreviewed)** | REV-0004 |
| E-C2 | Lower bound on the SOS degree needed to certify exact ground-state sets | Ensemble (MSG-0004 §4) | "Completed in part" (CX-T25, unreviewed) | — |
| Penalty | **Penalty thresholds.** For a product reference P₀ tilted by non-negative tables γ_U, bound gain(λ)=ln⟨e^{λΣγ}⟩₀ and locate the localisation transition λ_c. Also: is "has the floor left its reference?" (max_x[b(x)+ln π₀(x)] ≥ 0) NP-hard? | Theory THY-MSG-0017 §5 item 3; Science SCI-RES-0027 Q-CX3, SCI-MSG-0031 §2 | **Unreviewed**; "no new mathematics claimed" | none |
| Q-CX1 | W[1]-hardness in r of Z=Σexp(−f(x)−φ(u(x))) with r additive integer statistics | Science SCI-RES-0027 | answered (COMPLEXITY-RES-0001), not registered in THEOREMS | none |
| GEOM C1 | Complexity of max Σc_ij‖x_i−x_j‖² over freely jointed chains | Geometry GEOMETRY-REQ-0004 | answered in part (RES-0002); C2 declined | none |

**Inconsistencies in the repository's own records that I found:**
1. `HANDOFF.md`'s "State in a few lines" still calls the strand algorithm and the Ising note "Unreviewed". `THEOREMS.md`, `status/complexity.md` and MSG-0004 all record them as reviewed (REV-0003, REV-0004). THEOREMS.md is the authoritative register.
2. `NANUQ_HIGHER_LEVELS.md` (the draft in the head commit) cites "THEOREMS.md CX-T31, CX-X3", but neither appears in THEOREMS.md. Its §2.1 results are still a placeholder.

---

## B. Theorem register (15 fields)

Fields: (1) division · (2) commit · (3) id · (4) Lean · (5) assumptions · (6) status (verbatim label) · (7) review · (8) numerics · (9) counterexamples/dead ends · (10) physical meaning · (11) computational prerequisites · (12) software use · (13) competing methods · (14) when useless · (15) ready?

Unless stated otherwise, (1) is the Complexity division and (2) is `25bcd61` (the head commit; no row of the register gives its own commit; reviewed versions: REV-0001 at `22cf1a6`, REV-0002 at `9a35d2f`, REV-0003/0004 at `36d86cc`→`89114ea`).

### B1. CX-T1 / CX-T2 (+ CX-T15, CX-T20, CX-T24): strong NP-hardness of multi-strand NN MFE
(3) `STRANDS_NN_HARDNESS.md` Thm 1, Cor 2; Thms 1c, 1d, 1e. (4) **CX-V1** `Complexity.StackPacking.packing_of_all_stacked`, `exact_packing_of_all_stacked`: only the counting step (d). The structure/loop model is *not* formalised. (5) Exterior loops 0 (H0), or a flush coaxial reward with |x|<|σ|+min(|σ|,γ), or dangles with D_G+D_C<|σ|. GG/CC stack σ<0 (H1). Bulge/interior loops satisfy g(f) ≥ (u_C+1)σ+δ with δ>0 (H2′). Watson–Crick pairing. One complex. Instances: one template strand G^B(AG^B)^{m−1} plus homopolymer strands C^{a_i}, reduction from 3-/4-PARTITION. (6) **[P]**. (7) REV-0001 + SCI-REV-0019: correct; REV-0003: (H2′), 1c and 1e correct. (8) [X] `test_partition_reduction*.py` (18 instances), `test_generalised_hypotheses.py` (36), referee 134+867; T24: 12 329 instance–model pairs. (9) CX-D4(i): the original (H2) "g ≥ 0" excluded the Turner-2004 bulge rule. The reduction fails at δ ≤ 0, at x=σ with γ=0, and at D_G+D_C=|σ|. (10) Nucleic acids only: binding many short strands to a template is as hard as bin packing. (11) none. (12) none for proteins. (13) Condon–Hajiaghayi–Thachuk 2021 (BPM), Lyngsø 2004 gadget. (14) It is a worst-case result for one synthetic family; it says nothing about typical instances or published parameter tables as implemented (R20-CX-G not answered). (15) N/A (a hardness result).

### B2. CX-T4: #SSEL #P-hard; magnified PF #P-hard (magnification as input)
(3) Cor 4. (4) none. (5) As B1. The magnification j=O(N), or the temperature, is part of the input. Exact real oracle. (6) [P]. (7) REV-0001 (i) correct; REV-0003 (ii) correct on 154 pairs. (8) no dedicated program. (9) CX-D4(iv): "#P-hard as soon as species unbounded" was withdrawn. **Fixed-temperature hardness is open (A3′).** (10) Nucleic acids. (12)–(13) none. (14) Says nothing about a fixed temperature. (15) N/A.

### B3. CX-T14: ETH lower bound 2^{o(c)}·poly(N) excluded
(3) Cor 5, Appendix A (Lemmas A1, A2). (4) **CX-V4** `Complexity.FourPartition.four_sum`, `sum_good`, `size_bounds` (the arithmetic of Lemma A2 only). (5) ETH plus the sparsification lemma (cited from memory). (6) "[P], conditional on ETH". (7) REV-0001 rejected the first citation chain; REV-0003: Appendix A correct (9 390 formulas, 1 160 instances). (8) [X] `test_eth_chain.py`. (9) CX-D4(iii). (10) Nucleic acids. (14) Only a statement about the parameter c. (15) N/A.

### B4. CX-T10 / T11 / T12: orbit formula and sub-multiset DP over all strand orderings
(3) `STRANDS_ALGORITHM.md` Lemma 2, Lemma 3/Prop 4, Thm 1. (4) **CX-V2** `Complexity.JordanOrbit.weighted_fixed_point_formula` (with `sum_jordan`, `fix_iff_dvd_stab`, `stab_eq`): Σ_x R(x)^k g(x) = Σ_{d|c} J_k(d) Σ_{ρ^{c/d}x=x} g(x) for a permutation with ρ^c=1, g: X→ℚ, k∈ℤ. Lean does not cover the identification of physical structures with orbits. (5) Connected, unpseudoknotted. Affine multiloop m_a m_b^b m_c^u. Exterior loop weight 1. Species pairwise different. Unit-cost arithmetic. No dangles or coaxial stacking. (6) [P]; T11 "[P] / [K]". (7) REV-0003: correct; the L₀⁴ remark was wrong and is now corrected. (8) [X] exact `Fraction` agreement with `ref_enum.py` on 280 systems; referee ≈740 runs / 17 800 comparisons, letter-dependent weights 5 600. (9) An early version silently returned wrong values for duplicated species; that is now refused. Novelty for the base-pair model was overstated (REV-0003 F1). (10) Nucleic-acid complexes. (11) O(L₀⁴ Σ_d Π_i C(n_i/d+2,2)) operations: O(N⁴3^c) for distinct strands, polynomial for a bounded number of species. (12) **Reusable as technique**: Burnside/Möbius with Jordan totients for symmetric ensembles, sub-multiset tables, and exact rational validation against brute force. No direct protein use. (13) Boehmer et al. 2025 (BPM); Shalaby–Woods 2025/26 (NN, (c−1)!). (14) Exponential in the number of distinct species. (15) Partially: a tested Python reference exists, but only for nucleic acids.

### B5. CX-T30: MFE and level counts per symmetry class
(3) Prop 5. (5) Loop energies in εℤ, weights 2^{−Kg/ε} with K=⌈N log₂24⌉+1, Möbius inversion, base-2^K digit extraction. Numbers have O(cGN²) bits. (6) "[P] (the argument is the referee's)". (7) Proposed in REV-0003 F2. **The write-up and implementation are unreviewed.** (8) [X] `level_counts.py`, 17 systems; the naive (min,+) value is too low in 11 of them. (9) **A symmetry-naive (min,+) recursion is wrong** when the minimiser is symmetric. (12) **Transferable idea [my inference]**: exact density of states and the integer energy spectrum from one exact big-integer PF evaluation at a "magnified" weight. This is directly relevant to certified level-counting over rotamer energies discretised to εℤ. (14) Bit cost grows like Θ(N) × the energy range. (15) Partially (the idea and a Python reference; this model only).

### B6. NANUQ group: CX-T5, T6, T7, T8, T9, T13, T26, T27 (+ X1, X2)
(3) `NANUQ_LOCAL_CRITERION.md` Prop 2/Lemma 4/Thm 4 (local criterion, ≤6-leaf terms); Thm 7 (all galled outer-labeled planar networks); Thm 9 (7-leaf non-galled counterexample, weight 2−C(s+t,2)); Thm 10 (sharpness, 150/141/127/108); Thm 11 (parametric domain ρ_o=ρ_s, ρ_c+ρ_s ≤ 2ρ_a < 2ρ_s); Cor 5′/Thm 10′ (forbidden six-leaf pattern, 133/150); Thm 12 (level 2: critical split weight α(S*) = β₁G+ξ₁R−Σβ_jβ_l). (4) **CX-V3** `Complexity.NanuqFinite.five_point_facts`, `decomposition_five`, `decomposition_six`, `tg6_length`, `tg6_globally_good`, `tg6_locally_good`, `locally_good_imp_globally_good_six`, `doubled_five_point_systems`, `C6_spec`, `closure_locally_good` (by `decide +kernel`; the list C6 is imported from Python). **CX-V5** `Complexity.NanuqPattern.phi6_neg_iff_pattern`, `kprime_six`, `seventeen` (axiom `propext` only). (6) T5 "[P]+[X]+[V]"; T6 "[P]+[X]"; T7 "[X]+[P]"; T8 "[X]+[P]", partly [V]; T13 "[P]+[X]"; T26, T27 "[P]+[X]". (7) T5–T9: REV-0002 correct; the Lemma 0 gap was closed after REV-0004. T13: REV-0004 "correct as far as checked". **T26, T27: unreviewed.** (9) CX-D2 (arbitrary circular split systems fail); CX-D5 (rediscovery). (10) **Phylogenetics. No protein application.** (12)–(15) None for STRUCTBIO; not ready, not relevant.

### B7. CX-T16 (+ Cor 5a): twin reduction; fixed K linear; 2^K·poly(n) decision
(3) `ISING_GROUND_SETS.md` Thm 1 (exposed ⇔ aff P(V) ∩ conv P(V^c) = ∅; in co-NP), Thm 2 (only the set of column types matters), Cor 5a. (4) none. (5) Pair energy on **all pairs**; fields allowed (one constant site). Exact global ground states. (6) [P]. (7) REV-0004: correct; the 2^K algorithm was the referee's addition. (8) [X] `test_theory.py`; `span_algorithm.py` agrees with the full LP on all 255 type sets (K=4) and 900 random sets (K=5–7); "K=12, n=80: 6 seconds". Referee 885+1 301+3 895. (9) CX-D6(i)–(iii). The first version wrongly said "does not help when K grows". (10) Can a set of K configurations be made *exactly* the ground states of some pairwise model? In protein terms [my inference]: the inverse problem of designing pairwise energies so that a prescribed set of K rotamer assignments, and nothing else, is degenerate-optimal. (11) Gaussian elimination, listing ≤2^{K−1} span vectors, an LP, exact rational verification. Python + numpy + scipy. (12) Inverse design and validation of pairwise energy tables; certificate-producing feasibility checks. (13) Generic LP with constraint generation, where separation is itself a MAP problem. (14) **Binary spins and complete interaction graph only.** A restricted interaction graph breaks the twin argument. Rotamer variables are q-ary, not ±1. (15) Partially: the code is exact and certifying, but the model (binary, complete graph) does not match rotamer graphs.

### B8. CX-T17 / CX-T18 / CX-T19: tables and structure (mostly KNOWN)
(3) Thm 3 (K=4: not exposed iff the site-wise product is constant and four types occur); K=5 table (6 of 130 orbits non-exposed); Prop 12 (singleton states); Prop 5; Thm 6; Cor 7; Lemmas 8, 9; Prop 10 (Sidon criterion). (6) T17 "[X]+[P]"; T18 "[P] / [K]"; T19 "[P]". (7) REV-0004: correct. (8) [X] `table_k4.py` (2 s), `table_k5.py` (17 s); external anchor f₃ = 1780 of the cut polytope on 5 nodes. (9) "Exposed ⇔ unique cut decomposition" is false (REV-0004 F1). (13) **Known**: Laurent–Poljak 1995/96 Thm 4.2 = Cor 7; Deza–Laurent; Deza–Deza; Tropp 2018. (12) The polynomial sufficient conditions (Cor 7, isometric condition) and obstruction (Lemma 8, O(K⁴n)) are cheap screening tests. (14) Cor 7 is void for K ≈ n. (15) Partially.

### B9. CX-T28 / CX-T29: degree-2 SOS certificates ⇔ no other sign vector in the span; co-NP-complete
(3) Prop 13, 13′, Thm 14. (5) As B7. The certificate is a sum of squares of affine forms, equivalently the SDP relaxation over the elliptope is exact for E_J. Positive 1-in-3-SAT (cited from memory). (6) "[P]"; the ETH part depends on [K]. (7) **Unreviewed**, except that the reduction is the referee's (REV-0004 F5). (8) [X] `degree2_certificates.py` (94 sets); `span_algorithm.py reduction` (60 instances). (9) Every hard instance of the reduction **is exposed**, so this says nothing about the hardness of "exposed?". (10) **Directly relevant to "when is the SDP / degree-2 relaxation of a ±1 pairwise model tight with a unique (up to listed) ground set"**: tightness holds iff the span of the optimal set contains no other ±1 vector. The certifying energy is E(x) = xᵀ(I−Π_L)x (the projection rule of associative memories). (12) An exact, cheap, sufficient test for SDP-tightness on a candidate optimal set. It also shows that SDP tightness can fail even when a pair energy exposing the set exists. (13) Lasserre/SOS hierarchy theory (Laurent 2003; Fawzi–Saunderson–Parrilo; cited from snippets). (14) Prop 13′ only bites for n in the hundreds. At enumeration sizes (n ≈ 12–16) "another sign vector in span" is common (12–85 %). (15) Partially: unreviewed, binary only.

### B10. CX-T25: SOS interpolation bound
(3) Prop 11: if E ≥ 0 on the cube is an SOS of degree-d′ polynomials vanishing on V, then V lies in a degree-≤d′ variety. For K points in general position, K < Σ_{j≤d′}C(n,j). (6) "[P] (elementary)". (7) **unreviewed**. (8) none. (14) Not a statement about four-body energies specifically. (15) No (a theoretical bound).

### B11. CX-T21 / CX-T22: cluster bracket, Kotecký–Preiss-type criterion, threshold as max-flow
(3) `PENALTY_THRESHOLD.md` Thm 1: max(λ⟨G⟩, ln(1+W)) ≤ gain ≤ W, with W = Σ_{connected Γ} ⟨Π(e^{λγ_U}−1)⟩. Thm 2: tail bound n·ε^{s′}/(eΔ s′(1−ε)), ε = eΔ q_max^{1−λ/λ₀}, valid for λ < λ* = λ₀(1 − ln(eΔ)/ln(1/q_max)). Prop 3: λ₀ = min_S Σ_{i∈S} ln(1/q_i) / Σ_{U⊆S} max γ_U is a project-selection min-cut. Prop 4: gain ≥ (λ/λ₁ − 1) ln(1/P₀(x*)), λ₁ = min_x ln(1/P₀(x))/G(x), and λ₀ ≤ λ₁. (5) **Product reference**, tables γ_U ≥ 0 that vanish unless all sites are off-anchor. (6) "[P] (standard polymer-gas inequalities, applied)"; T22 "[P]". (7) **unreviewed**. (8) [N] `price_bound.py` (8 sites, 3 states, two seeds, exact enumeration). In the low-q case W matches the exact gain to 3–4 digits up to λ₀, where first order is off ×1000 and Finner ×100. (9) **On the science division's four floors (SCI-RES-0034) the explicit criterion is void** (q_max is 8–17× above 1/(eΔ)), and λ₀ is only 0.10–0.16 of the measured transition. **λ₁ comes within 1.1–3.3 %.** The science division found λ₁ independently ("λ_gs"). (10) Free-energy cost of switching on non-negative penalties over a reference ensemble, and where the ensemble "leaves" its reference. (11) Max-flow (networkx), bisection or Dinkelbach. (12) **Certified upper/lower bracket for ln Z ratios** in the low-excitation regime, with a polynomial-time computable threshold. Possible use as a cluster-expansion certificate for free-energy *differences* relative to a factorised reference [my inference]. (13) Kotecký–Preiss; Helmuth–Perkins–Regts 2019 (cited from memory). (14) Void when q_max ≥ 1/(eΔ). Not valid for Markov/band references. W has exponentially many terms. (15) Partially: the bounds and a toy implementation exist, but there is no review and only a product reference is covered.

### B12. CX-T23: "has the floor left its reference?" NP-hard; polynomial cases
(3) Prop 5. For fixed m ≥ 2, deciding max_x[b(x) + ln π₀(x)] ≥ 0 is NP-hard: (i) three states and a product known part, (ii) two states and a nearest-neighbour-pair known part, both by MAX-CUT. It is polynomial for: two states with a product known part (project selection); windowed tables ((max,+) pass); product pair tables (one-parameter separable family, O(nq²) breakpoints; band: ≤ n^{1+log₂Q}); and, with a margin ε, exponentially decaying tables (window O(ln(n/ε)/κ)). (6) "[P]". (7) **unreviewed**; "no search made". (8) [X] `hardness_maxcut.py` (40 graphs). (10) Whether a penalised pairwise model's MAP leaves the reference state: a MAP problem with fields and non-negative couplings on "off" states. (12) **A ready-made decision boundary**: binary (on/off) + product reference ⇒ min-cut exact; ≥ 3 states or non-product reference ⇒ NP-hard in general; banded/windowed ⇒ DP. (14) Worst-case only. The science division's actual instances are windowed, hence DP-exact. (15) Partially.

### B13. Unregistered answers (COMPLEXITY-RES-0001, -0002)
- **Q-CX1** [P, two lines + K]: Z with r additive unary statistics and a threshold φ is W[1]-hard in r (from Unary Bin Packing, Jansen–Kratsch–Marx–Schlotter 2013, "cited from memory"). No g(r)·(nR)^{o(r/log r)} algorithm under ETH, even for a factor-2 approximation. Alphabet k = r. **Unreviewed.** Relevance: constrained ensembles (fixed composition / count constraints) cost n^{Θ(r)} in general.
- **GEOM C1** [P, elementary]: max Σc_ij‖x_i−x_j‖² over freely jointed chains is *exactly* a rank-3 Heisenberg/Grothendieck problem with arbitrary couplings, because the chain order gives no structure. The hardness consequences are "conditional on sources we have not read".
- **Q-CX2**: a list of sources on #P-hardness of pairwise PFs and treewidth tractability, explicitly "from memory … leads, not verified citations".

---

## C. Relevance filter for protein side-chain computation

**No direct protein application:** all STRANDS work (CX-T1–T4, T10–T12, T14, T15, T20, T24, T30, V1, V2, V4) concerns nucleic-acid secondary structure. All NANUQ work (CX-T5–T9, T13, T26, T27, X1, X2, V3, V5, NANUQ_HIGHER_LEVELS) concerns phylogenetic networks. The GEOM C1 result concerns geometric chain inverse problems.

| Axis | Bearing results | Verdict for STRUCTBIO |
|---|---|---|
| (i) MAP / ground states | CX-T16–T19, T28, T29 (exact ground-*set* structure of ±1 pairwise models, cut-polytope faces, uniqueness/degeneracy design); CX-T23 (MAP with non-negative "off" couplings: NP-hard for ≥3 states, min-cut for binary + product). The division proves **no new NP-hardness of MAP itself**; that is standard (Barahona 1982, cited from memory in RES-0001). | Relevant conceptually. Binary/complete-graph restrictions limit direct use. CX-T23's binary ⇒ min-cut / ternary ⇒ NP-hard dichotomy maps onto the known submodular vs non-submodular split [my inference]. |
| (ii) counting / log Z | CX-T21, T22 (cluster bracket, KP criterion); Q-CX1 (W[1]); PENALTY §3(iii) quotes, from memory and marked "[K?]", Jerrum–Sinclair FPRAS (ferromagnetic, consistent fields), #BIS-hardness for mixed fields (Goldberg–Jerrum), HPR cluster algorithms. CX-T4 is nucleic-acid specific. | The bracket is usable only as a low-temperature, sparse-excitation certificate relative to a product reference. No treewidth/transfer-matrix algorithm for Potts models is proved here. |
| (iii) certificate size vs algorithm | Thm 1 (non-exposedness has a poly-size certificate, so co-NP); Cor 5a (certificates live in a 2^K-size span); CX-T28/T29 (degree-2 SOS certificates exist iff the span condition holds, which is co-NP-complete to check); CX-T25 (SOS degree must grow with K). | **Most decision-relevant theory in this division.** It shows concretely that *checking* or *existence* of a cheap (SDP/degree-2) optimality certificate for a prescribed optimal set is a different and harder question than computing MAP on easy instances. |
| (iv) penalty / relaxation exactness | CX-T22 (λ₀ via min-cut is the exact threshold of the binary relaxation; λ₁ the true extremal ratio, NP-hard with state-dependent tables, DP on bands); CX-T28 (exactness of the SDP relaxation for E_J ⇔ the span condition). | **Directly informs dual-decomposition / LP/SDP bound design**: relaxation tightness has a combinatorial characterisation in the binary case. Nothing is proved for q-ary LP (local polytope) tightness. |
| (v) reusable proven DP | CX-T12 sub-multiset DP (with uniqueness proof and orbit formula, V2); CX-T30 digit-extraction for exact level counts; PENALTY Prop 5 product-table parametric (max,+) trick. | Techniques transfer. The code does not (nucleic-acid model). |

---

## D. Rigorous algorithms with proof and implementation

| Algorithm | Input → output | Complexity | Exact? | Proof / review | Reuse potential |
|---|---|---|---|---|---|
| `strands/multiset_dp.py` (CX-T12) | strand species, multiplicities, loop-weight model (hp, il, m_a/m_b/m_c), α → Q_α as a `Fraction` | O(L₀⁴ Σ_d Π C(n_i/d+2,2)) | yes (`fractions.Fraction`) | [P], REV-0003 correct, 280 + ~740 exact cross-checks | technique (Burnside/Jordan, sub-multiset tables, brute-force oracle `ref_enum.py`); not the code |
| `strands/level_counts.py` (CX-T30) | same, integer energies → table (R, m) ↦ physical structure counts, MFE | same ops; O(cGN²)-bit integers | yes | [P], write-up unreviewed | **Pattern for exact density of states from one big-integer PF** |
| `ising_faces/span_algorithm.py` + `faces.py` (Cor 5a, Thm 1) | K sign vectors → exposed? with a certificate (rational J, or rational (μ, α)) | 2^K·poly(n); 6 s at K=12, n=80 | **certified in exact rationals** (LP proposals from scipy are floating point, then rationalised and verified) | [P], REV-0004 | **Certifying-LP pattern** (float proposal → exact rational verification) is exactly what STRUCTBIO needs for GMEC certificates |
| `ising_faces/degree2_certificates.py` (Prop 13) | V → projection energy xᵀ(I−Π_L)x and its exact zero set | enumerates all 2ⁿ states (small n) | yes | unreviewed | test harness only |
| `penalty_threshold/price_bound.py` (Props 3–4) | product reference, tables → λ₀ (max-flow), λ₁ (brute force), bracket | λ₀ polynomial; λ₁ and W exponential | **floating point** (`math`, networkx) | unreviewed, [N] | Prop 3 min-cut threshold is reusable as a cheap bound |
| `penalty_threshold/hardness_maxcut.py` | graph → checks of reductions | brute force | float | unreviewed | none |

Dependencies (HANDOFF): Python 3, `networkx`, `numpy`, `scipy`; `g++` for the referee's C++ code; Lean 4.31.0 + Mathlib v4.31.0. Lean files are checked file by file with `lake env lean experiments/complexity/lean/<File>.lean`. There is no `sorry`, `admit`, `native_decide` or new axiom (my grep confirms no occurrence). `NanuqFinite.lean` needs about 11 GB and 3.5 min. **Lean covers only finite or arithmetic cores; no complexity statement is formalised** (lean/README).

---

## E. Dead ends, open problems, limitations, inter-division traffic

**Dead ends** (`DEAD_ENDS.md`):
- CX-D1: A2 was already solved by Shalaby–Woods.
- CX-D2: NANUQ fails for general circular split systems.
- CX-D3: both flagship problems had moved before work began.
- CX-D4: seven overstatements (physical parameter sign pattern, coaxial-stacking failure, ETH citation, #P-hardness without the magnification qualifier, planar-tree claim, non-independent tests, header times).
- CX-D5: the NANUQ all-level theorem is a probable rediscovery.
- CX-D6: Ising ("exposed ⇔ span condition" is false; "four constant-product states" is not exhaustive from K=5; no co-NP-hardness reduction found).
- CX-D7: Lean traps (a hand-typed tree list was wrong; a kernel evaluation exhausted 16 GB).

**Open** (RESEARCH_LOG "Resume here"; OPEN_PROBLEMS):
- E-C1 for K ≫ log n.
- A3′, fixed-temperature #P-hardness (no approach).
- C1: FPRAS/inapproximability of these PFs (not started).
- C2: W[1]-hardness in the number of species.
- NANUQ level 3.
- Defining the C6 closure in Lean.
- 2^c by fast subset convolution (remark only).
- L₀³ recursion (not implemented).
- The PENALTY band-reference case.
- Unanswered: SCI-RES-0031 §1, THY-MSG-0017 §5 item 1, R20-CX-G.

**Review traffic:**
- COMPLEXITY-REV-0001 (hardness): "correct with gaps", 4 major / 8 minor findings, all processed.
- REV-0002 (NANUQ): no claim broken, 2 major findings.
- REV-0003 (algorithm + hardness additions): no theorem broken; 2 major findings (the novelty paragraph was wrong; the MFE clause was unproved). Processed by 21:24 UTC.
- REV-0004 (Ising + NANUQ additions): no false numbered theorem; majors were the ℓ1-rigidity reformulation and the Laurent–Poljak attribution. Processed by 21:09 UTC.
- The referees' code is in `experiments/complexity/reviews/rev{1..4}_*` and is "written without access to … the division's own programs".
- SCI-REV-0019 (science division, independent) is answered in COMPLEXITY-RES-0004, "Completed, except R20-CX-A second half (Lyngsø's paper not read) and R20-CX-G (no published table checked)".
- **Engineering: no request or response either way** ("For Engineering: no request yet", MSG-0001). The division sent no requests ("requests open: none of ours"; `requests/complexity/` does not exist).

**Still unreviewed** (MSG-0004 §3): CX-T26, T27, T28, T29(a,b), T30 write-up, all of `PENALTY_THRESHOLD.md` (T21–T23), and T25.

**"Threshold on four floors" / SCI-RES-0034** (recorded in `PENALTY_THRESHOLD.md` §2 "Correction", §6 and MSG-0004 §1(e)):
- The division had claimed that the science instances lie in the regime ln(1/q) ≫ ln Δ. That was wrong: 8–9 kT is the cost of the extremal state, while ln(1/q_i) is only 1.0–3.8 on the "lysine chain".
- On the four floors the KP criterion is void and λ₀ is 0.10–0.16 of the transition. λ₁ is within 1.1–3.3 % of it and was found independently by science as λ_gs.
- Science's reference is a band model, which is outside the theorem's product hypothesis. Its instances are windowed tables, so one (min,+) pass is exact for them.
- The division concludes that "the lower side as we proved it certifies nothing there" and does not request the tables.

---

## F. Prior art and novelty verdicts (`PRIOR_ART.md`)

- **STRANDS hardness**: "apparently unpublished". The gadget is Lyngsø 2004, which they did not read and know only via DSW App. B.3. Four searches of their own plus ten by the referee. A 2026 PhD thesis (Shalaby, A-XIII) could not be inspected and is listed as a novelty risk.
- **STRANDS algorithm**: for BPM the result is Boehmer–Berkemer–Will–Ponty, AMB 21:4 (2025), Thm 4 O(3^m n³ m²). The central loop is Shalaby–Woods ICALP 2025 Lemma 18. The only new parts are the NN version, arbitrary α (J_{1−α} closed form), the operation count and the implementation.
- **NANUQ**: CX-T6 is "in all likelihood a rediscovery" of the unreviewed B-II. They could not read its repo: the attach request was denied. No prior art was found for T7, T8, T13, T26 or T27.
- **Ising**: the object is the face lattice of the cut polytope. Cor 7 = Laurent–Poljak Thm 4.2 (pp. 13–14 read). Prop 5 follows from Laurent–Poljak. The K=4 obstruction and the ≤5-type tables are in Deza–Laurent / Deza–Deza (read by the referee only). Tropp 2018: ≤ √(cn) random states give a simplicial face. No source was found for Thm 6, Lemma 9, Prop 10/Sidon, Prop 13 or Thm 14, which is "not evidence of novelty". The projection rule is "classical", cited from memory.
- **Penalty**: "Nothing here is new mathematics". Kotecký–Preiss, Picard, Dinkelbach, Jerrum–Sinclair, Goldberg–Jerrum and HPR are all cited from memory, unread.

---

## G. Intake assessment and design guidance for STRUCTBIO (mine)

**G1. What this division gives STRUCTBIO (from the repository).**
1. **A certification pattern that works.** In `faces.py`/`span_algorithm.py`, a floating-point LP proposes a primal (J) or dual (Farkas μ, α) object, which is then rationalised and verified in exact arithmetic. "Yes" and "no" both carry independently checkable certificates. This is the template for a GMEC optimality certificate: an LP/ILP or dual-decomposition bound proposed in floats, then checked exactly. **Recommend adopting it as the STRUCTBIO certificate architecture.**
2. **Relaxation tightness can be characterised and is itself hard to decide** (CX-T28/T29, binary case). The degree-2 SDP is exact for some energy with ground set V iff span(V) has no extra ±1 vector, and checking that is co-NP-complete but costs only 2^K·poly(n) in the number K of co-optimal states. Design consequence: test tightness *a posteriori* on the found solution set; a dual gap of zero is the certificate. Do not attempt to predict tightness a priori.
3. **Penalty/threshold dichotomy** (CX-T22, T23). Binary on/off with a product reference ⇒ min-cut is exact. ≥3 states, or a non-product reference ⇒ NP-hard in general. Banded/windowed ⇒ exact DP. Product pair tables ⇒ a one-parameter separable reduction. In the binary product case the threshold λ₀ is computable by max-flow. The empirical lesson from SCI-RES-0034: **the extremal-state ratio λ₁ predicted the transition to within 3 %, whereas the polynomial relaxation λ₀ was off by ×6–10.** Cheap relaxations can be badly loose in exactly the regime that matters.
4. **Cluster-expansion bracket** (CX-T21) for log-partition *ratios* versus a factorised reference: tight while W is small, provably convergent only when q_max < 1/(eΔ). For rotamers [my inference], q is the probability that a residue is off its dominant rotamer, and the criterion holds only for very rigid, low-degree interaction graphs. Treat it as an optional certified bound, not as the main log Z engine.
5. **Exact spectrum by digit extraction** (CX-T30): integerised energies (εℤ) plus one exact big-integer PF at weight 2^{−K} give every level count. This is a cheap route to certified low-energy state counts once an exact (treewidth) PF exists [my inference].
6. **Process lessons** (CX-D4, REV-0003 F1). Read journal versions before claiming novelty. Symmetry-naive (min,+) recursions can be silently wrong (CX-T30). Exhaustive brute-force cross-checks with exact rationals caught real implementation bugs (duplicated species).

**G2. Standard complexity facts to build in** (standard, from memory; not from this repository unless noted).
- MAP/GMEC on pairwise Potts models is NP-hard in general (even planar with fields; APX-hard; Pierce–Winfree 2002 for side-chain placement). The polynomial cases are bounded treewidth (DP / junction tree, O(n·q^{w+1})), submodular binary energies (min-cut), and planar zero-field Ising MAP (matching). Ternary or general submodular-like extensions need care (α-expansion is approximate).
- log Z is #P-hard in general. An FPRAS exists for ferromagnetic Ising with consistent fields (Jerrum–Sinclair; the repository cites this from memory as "[K?]"). Mixed fields are #BIS-hard to approximate; antiferromagnetic/general cases are NP-hard to approximate beyond uniqueness thresholds. Exact log Z is O(n·q^{w+1}) by treewidth, or by transfer matrices for banded systems.
- Residue-interaction graphs under typical distance cutoffs (≈ 8–10 Å side-chain contacts) have small treewidth only for small or sparse systems after dead-end elimination pruning. Whole-protein graphs often have treewidth in the tens, so q^{w+1} with q ≈ 10–100 rotamers is infeasible without pruning. **Design: compute a treewidth upper bound (min-fill) after DEE/pruning and dispatch exact DP vs branch-and-bound vs bound-only per instance.**
- A branch-and-bound or DEE certificate can be checked in time linear in its size, but its size can be exponential. A dual (LP/SDP) certificate has polynomial size but exists only when the relaxation is tight. Report which kind of certificate was produced.
- The division's lower bounds (NP-hardness, ETH, W[1]) are **worst-case statements about synthetic families**. Its own ASSUMPTION_AUDIT stresses that they "say nothing about typical instances". STRUCTBIO must not read them as obstructions to real-protein performance. Likewise the polynomial bounds (O(N⁴3^c), n^{1+log₂Q}, 2^K·poly(n)) are worst-case counts. The division itself calls the n^{1+log₂Q} exponent "of theoretical interest only". None of them is a practical runtime guarantee.

**G3. What does *not* transfer.** The Ising-ground-set theorems assume **±1 spins and a complete interaction graph**. Rotamer models are q-ary on sparse graphs, and the repository says the twin argument changes on restricted graphs. A q-ary analogue (faces of the marginal/local polytope) is not addressed. All STRANDS and NANUQ code is domain-specific. None of the protein-relevant theorems (T21–T23, T25, T28, T29) has been reviewed even internally, so STRUCTBIO should rely on them only as design heuristics until reviewed.

**Readiness summary:** the one item worth porting now is the certify-in-exact-arithmetic LP pattern (D). The degree-2/span tightness test, the min-cut threshold and the digit-extraction spectrum are partially ready (ideas proved, code toy-scale or domain-specific, mostly unreviewed). Everything else is not relevant to protein side chains.
