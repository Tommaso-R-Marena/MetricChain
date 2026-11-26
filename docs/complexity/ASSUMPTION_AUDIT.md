# Assumption audit of the complexity division's theorems

*2026-11-26 19:46 UTC.*  Written in the form asked for by the research owner's supplementary directive of 2026-11-26
("Mathematical Generality, Physical Relevance, and Foundational Breakthroughs", item 2), which reached this
division through the theory division's relay (THY-MSG-0016, read on the theory branch); our own mandate asks
for the "contribution and limitations" of every result, and this file is how we give them.

For every hypothesis of every registered theorem: its **class** —

* **E** essential: the statement is false without it (evidence named);
* **Q** replaceable by a weaker quantitative condition (the condition is given);
* **T** needed only by the present proof (no counterexample known without it);
* **V** a convenience of the model or of the exposition;
* **C** its removal changes the computational complexity;
* **?** not known —

and the evidence.  "Control" means a model or instance violating the hypothesis on which the statement was
observed to fail, in the exhaustive tests named.  The audit was made by the division itself, not by an
independent reader; two internal reviews are still running on parts of the material (the algorithm note,
the Ising note, the additions to the two reviewed notes), and this file will be revised when they report.

## 1. Hardness of multi-strand folding (`STRANDS_NN_HARDNESS.md`; CX-T1–T4, T14, T15, T20, T24)

| hypothesis | class | what happens without it; evidence |
|---|---|---|
| (H0) exterior loops have energy `0` | **Q** | may be replaced by: a reward `x` for flush nicked stacks with `|x| < |σ| + min(|σ|,γ)` (Thm 1c); dangles with `D_G + D_C < |σ|` (Thm 1d); both with `σ ≤ x ≤ 0`, `D_G + D_C < |σ| − |x|/B` (Thm 1e).  Beyond: the reduction fails at `x = σ, γ = 0`, at `|x| = |σ| + min(|σ|,γ)`, at `D_G + D_C = |σ|` (controls, `test_generalised_hypotheses.py`).  Not covered: dangle rules counting a base for two helices, terminal mismatches, any published table as implemented |
| (H1) the `GG/CC` stack is favourable, `σ < 0` | **E** (for this reduction) | with `σ = 0` all structures tie (science referee's control: wrong on 32 of 32 unsolvable instances).  Whether folding is hard in models without favourable stacks is a different question |
| (H2′) a bulge/interior loop costs more than `(u_C+1)σ` by a margin `δ > 0` | **E** for the reduction, in this quantitative form | `δ = 0` and `δ < 0`: fails on 21 of 31 instances (controls).  The first version's (H2) "`g ≥ 0`" was a **V** that excluded the Turner-2004 bulge rule |
| hypotheses on hairpins and multiloops | none needed | they do not occur in the instances (the chords are nested) |
| the pairing rule (Watson–Crick only) | **V** | only "`{C,G}` is the one complementary pair among `A`, `C`, `G`" is used |
| one complex containing all strands | **Q** | with unbound strands allowed the equivalence holds iff binding pays, `|σ|(a_i − 1) > ΔG_assoc`; counterexample otherwise (Remark 5) |
| the model with rotational symmetry and association terms | **V** | all structures of the instances have `R = 1`; the terms are constants |
| unboundedly many strand *species* | **C** | for a bounded number of species the partition function is computable in polynomial time (CX-T12, unreviewed), and bounded strand length implies bounded species; so hardness needs unboundedly many species **and** unbounded strand length — the instances use one strand of length `Θ(N)` |
| unary sizes / strong NP-hardness of the source problem | **E** for strings | the strands are written out; 3-PARTITION and 4-PARTITION are strongly NP-hard [K; 4-PARTITION re-proved, arithmetic machine-checked CX-V4] |
| `B ≥ 2` in Thm 1c (case `|x| ≥ |σ|`) and Thm 1e | **T** | used to pair every `G` from the loose-bond count; instances with `B = 1` are trivial |
| the term `|x|/B` in the hypothesis of Thm 1e | **T?** | the conclusion held without it in all tests and failed at `D_G + D_C = |σ|`; probably an artefact |
| Cor. 4(ii): the magnification (or temperature) is part of the input, of size `O(N log N)` | **?** — the open problem A3′ | at a fixed temperature for a fixed model nothing is proved; no approach found (`RESEARCH_LOG.md`) |
| Cor. 4: an exact real-number oracle | **V/T** | as in [DSW] Thm 22; a precision of `O(N log N)` bits suffices for the one-call reduction |
| Cor. 5: the Exponential Time Hypothesis, with the sparsification lemma | conditional | the chain 3-SAT → 3DM → 4-PARTITION → strands is linear and written out (Appendix A); the lemma is cited |
| NP membership | restricted | claimed only without the term `k_BT ln R` |

**Hierarchy.**  base-pair counting on these instances (trivial) ⊂ stack-only model ⊂ loop models with (H0), (H1), (H2′)
⊂ with a flush reward (1c) / dangles (1d) / both (1e) ⊂ [not covered] published parameter sets as implemented.
**Vacuity check.**  None of the hardness statements is vacuous, but each is a worst-case statement about one
synthetic family (a long template and many homopolymer strands) and says nothing about typical instances.

## 2. The partition function over all strand orderings (`STRANDS_ALGORITHM.md`; CX-T10–T12) — unreviewed

| hypothesis | class | remark |
|---|---|---|
| connected, unpseudoknotted structures; a loop with a nick is an exterior loop of weight 1 | **V** (the model of the cited papers) | pseudoknots change the problem class |
| multiloop weights of the form `m_a·m_b^b·m_c^u` | **C** | the usual condition for a polynomial recursion; general multiloop energies are not covered |
| general interior-loop weights | none | costs the factor `L_0^4`; a restricted form would give `L_0^3` (not done) |
| a bounded number of species for polynomial time | **C**, essential unless P = NP | by §1 the problem is NP-hard for unboundedly many species; `3^c`-type cost for distinct strands, optimal up to the base under ETH (CX-T14) |
| unit-cost arithmetic | **V**, hides a factor | with magnification `α = Θ(N)` the numbers have `Θ(N²)` bits |
| MFE and #SSEL from the partition function | cited, **not re-derived** | [SW26, §7] |

## 3. The NANUQ metric (`NANUQ_LOCAL_CRITERION.md`; CX-T5–T9, T13)

| hypothesis | class | what happens without it; evidence |
|---|---|---|
| Thm 4: the system is tree-generated | **V** | needed for the metric to be defined (every 4-set displays a quartet) |
| Thm 4: the six-point terms are non-negative and vanish for undisplayed splits | sufficient; **E among closed classes** for "Kalmanson with exact support" | each of the 23 six-point systems violating it fails itself or after doubling leaves (Thm 10); for "Kalmanson" alone sharpness is open (§7 of the note) |
| Thm 7: galled | **E** | `N*`: a level-2 outer-labeled planar bloblet on seven leaves, not galled, Kalmanson for none of the 360 orders; weights `2 − C(s+t,2)` in a family (Thm 9).  Most non-galled planar networks still satisfy the conclusion (referee's survey); they are not classified |
| Thm 7: outer-labeled planar | **V** for the formulation (it supplies the circular order); beyond it **?** | not studied; the third-party summary states that planarity cannot be dropped for exact support |
| Thm 7: binary | **?** | the setting of the source; not examined |
| Thm 7: bounded level, bloblet, number of blobs | none needed | any level, any number of blobs |
| the multiplicity-free averaging of [HABIMRW] Def. 4.1 | **E** for the failure outside "galled" | with multiplicities the metric is circular decomposable for every outer-labeled planar network ([HABIMRW] Cor. 3.4) |
| Thm 11: `ρ_o = ρ_s`, `ρ_c + ρ_s ≤ 2ρ_a < 2ρ_s` | **E**, exact domain | explicit witnesses for every violated inequality (blow-ups, sunlets, a level-1 network on eight leaves) — unreviewed |
| Thm 11: the reading of "4-cycle" above level 1 | **V**, ours | the family is defined in the source for level 1 only |
| the list of 108 six-leaf systems | computed | the six-point check is kernel-checked for the list; that the list is the closure is not (CX-V3) |

**Vacuity check.**  Thm 4 turns a statement about all `n` into a check on six-leaf restrictions — finitely
many for the network class, but for an arbitrary split system given explicitly it is a polynomial-time test
(`O(n⁶)` restrictions), not vacuous.

## 4. Ising ground sets (`ISING_GROUND_SETS.md`; CX-T16–T19, T25) — unreviewed

| hypothesis | class | remark |
|---|---|---|
| all pairs may be coupled | **T/C** | the twin reduction adds couplings between twins; with a restricted interaction graph twins must be twins in the graph |
| no fields | **V** | with fields the same argument works with columns not identified up to sign (not written) |
| global ground states (not single-flip stable states) | **C** | stability is a linear programme |
| `K` fixed | **C?** | the table has `2^{2^{K−1}}` entries; for `K` in the input: in co-NP, hardness unknown |
| Cor. 7: `1` and the products `t_kt_l` independent on the types | sufficient, **not necessary** | needs more than `K(K−1)/2` types; void in the regime `K ≈ n` |
| Prop. 10: a pair-separating sign symmetry | **T** | without it only "not exposed ⟹ another sign vector in the span" holds; the converse is false in general |
| Prop. 11: general position of the conformers | **T** | assumed for random conformers beyond `D_d'`, not cited |

## 5. Penalised models (`PENALTY_THRESHOLD.md`; CX-T21–T23) — unreviewed

| hypothesis | class | remark |
|---|---|---|
| product reference | **T**, and probably more | the factorisation over site-disjoint polymers fails for a Markov reference; only a product-reduced floor is covered |
| tables `γ_U ≥ 0` | **E** for the bracket `ln(1+W) ≤ gain ≤ W` | with signs only the absolute-value Kotecký–Preiss criterion would remain |
| tables vanish unless all their sites are off the anchor | not used in Thm 1; **Q** in Thm 2 | it gives the factor `q(supp Γ)`; any bound of the polymer weights by a product over sites would do |
| Thm 2: `eΔ·q_max^{1−λ/λ_0} < 1` | sufficient; **computationally vacuous when `q_max ≥ 1/(eΔ)`** | in that regime `W` itself is still sharp on the toy models; the explicit criterion says nothing |
| Prop. 5: general tables / at least two off states or a non-product known part | **C** | NP-hard; polynomial for two states with a product known part, for windowed tables, for product pair tables, and with a margin for exponentially decaying tables |

## 6. Statements that were presented more broadly than proved

Seven, all withdrawn or narrowed in COMPLEXITY-MSG-0003 §1 (`DEAD_ENDS.md` CX-D4): the "sign pattern of every
physical parameter set"; "coaxial stacking breaks the reduction"; #P-hardness of the partition function
without the qualifier "magnification in the input"; a citation behind the ETH bound; "all displayed trees of
a galled network are restrictions of one planar tree"; "direct tests" that presupposed the structure lemmas;
header times.  In addition the all-level NANUQ theorem is in all likelihood a rediscovery (CX-D5).
