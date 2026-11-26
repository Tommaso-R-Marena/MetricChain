# Assumption audit of the complexity division's theorems

*2026-11-26 19:46 UTC; revised 2026-11-26 21:23 UTC after the internal reviews COMPLEXITY-REV-0003 and -0004.*  Written in the form asked for by the research owner's supplementary directive of 2026-11-26
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
independent reader.  The two internal reviews that were running when it was first written have reported
(COMPLEXITY-REV-0003, -0004); the rows they changed are marked, and §6 lists what they found to be
overstated.  §§3a and 4 contain statements written after those reviews, which no referee has seen.

## 1. Hardness of multi-strand folding (`STRANDS_NN_HARDNESS.md`; CX-T1–T4, T14, T15, T20, T24)

| hypothesis | class | what happens without it; evidence |
|---|---|---|
| (H0) exterior loops have energy `0` | **Q** | may be replaced by: a reward `x` for flush nicked stacks with `|x| < |σ| + min(|σ|,γ)` (Thm 1c); dangles with `D_G + D_C < |σ|` (Thm 1d); both with `σ ≤ x ≤ 0`, `D_C + max(D_G, |x|/B) < |σ|` (Thm 1e).  Beyond: the reduction fails at `x = σ, γ = 0`, at `|x| = |σ| + min(|σ|,γ)`, at `D_G + D_C = |σ|` (controls, `test_generalised_hypotheses.py`).  Not covered: dangle rules counting a base for two helices, terminal mismatches, any published table as implemented |
| (H1) the `GG/CC` stack is favourable, `σ < 0` | **E** (for this reduction) | with `σ = 0` all structures tie (science referee's control: wrong on 32 of 32 unsolvable instances).  Whether folding is hard in models without favourable stacks is a different question |
| (H2′) a bulge/interior loop costs more than `(u_C+1)σ` by a margin `δ > 0` | **E** for the reduction, in this quantitative form | `δ = 0` and `δ < 0`: fails on 21 of 31 instances (controls).  The first version's (H2) "`g ≥ 0`" was a **V** that excluded the Turner-2004 bulge rule |
| hypotheses on hairpins and multiloops | none needed | they do not occur in the instances (the chords are nested) |
| the pairing rule (Watson–Crick only) | **V** | only "`{C,G}` is the one complementary pair among `A`, `C`, `G`" is used |
| one complex containing all strands | **Q** | with unbound strands allowed the equivalence holds iff binding pays, `|σ|(a_i − 1) > ΔG_assoc`; counterexample otherwise (Remark 5) |
| the model with rotational symmetry and association terms | **V** | all structures of the instances have `R = 1`; the terms are constants |
| unboundedly many strand *species* | **C** | for a bounded number of species the partition function is computable in polynomial time (CX-T12, unreviewed), and bounded strand length implies bounded species; so hardness needs unboundedly many species **and** unbounded strand length — the instances use one strand of length `Θ(N)` |
| unary sizes / strong NP-hardness of the source problem | **E** for strings | the strands are written out; 3-PARTITION and 4-PARTITION are strongly NP-hard [K; 4-PARTITION re-proved, arithmetic machine-checked CX-V4] |
| `B ≥ 2` in Thm 1c (case `|x| ≥ |σ|`) and Thm 1e | **T** | used to pair every `G` from the loose-bond count; instances with `B = 1` are trivial |
| the block-length term in the hypothesis of Thm 1e, `D_C + max(D_G, |x|/B) < |σ|` | **E** in this form when `D_G` is small | with `x = σ`, `D_G = 0`, `D_C = ⅔|σ|` the conclusion fails for `B = 2` (control); a first guess that the term was an artefact was wrong.  For the hardness corollary it is harmless: `B` may be taken large |
| Cor. 4(ii): the magnification (or temperature) is part of the input, of size `O(N)` (sharpened from `O(N log N)` after REV-0003) | **?** — the open problem A3′ | at a fixed temperature for a fixed model nothing is proved; no approach found (`RESEARCH_LOG.md`) |
| Cor. 4: an exact real-number oracle | **V/T** | as in [DSW] Thm 22; a precision of `O(N log N)` bits suffices for the one-call reduction |
| Cor. 5: the Exponential Time Hypothesis, with the sparsification lemma | conditional | the chain 3-SAT → 3DM → 4-PARTITION → strands is linear and written out (Appendix A); the lemma is cited |
| NP membership | restricted | claimed only without the term `k_BT ln R` |

**Hierarchy.**  base-pair counting on these instances (trivial) ⊂ stack-only model ⊂ loop models with (H0), (H1), (H2′)
⊂ with a flush reward (1c) / dangles (1d) / both (1e) ⊂ [not covered] published parameter sets as implemented.
**Vacuity check.**  None of the hardness statements is vacuous, but each is a worst-case statement about one
synthetic family (a long template and many homopolymer strands) and says nothing about typical instances.

## 2. The partition function over all strand orderings (`STRANDS_ALGORITHM.md`; CX-T10–T12, CX-T30) — reviewed by COMPLEXITY-REV-0003

| hypothesis | class | remark |
|---|---|---|
| connected, unpseudoknotted structures; a loop with a nick is an exterior loop of weight 1 | **V** (the model of the cited papers) | pseudoknots change the problem class |
| multiloop weights of the form `m_a·m_b^b·m_c^u` | **C** | the usual condition for a polynomial recursion; general multiloop energies are not covered |
| general interior-loop weights | none | **corrected after REV-0003:** the factor `L_0^4` does not come from the interior loops alone — the tables are decomposed by the rightmost top-level pair with both ends free, `Θ(ℓ L_0)` per entry in any loop model; last-base recursions *and* the usual interior-loop treatment would give `L_0^3` (not done) |
| a bounded number of species for polynomial time | **C**, essential unless P = NP | by §1 the problem is NP-hard for unboundedly many species; `3^c`-type cost for distinct strands, optimal up to the base under ETH (CX-T14) |
| unit-cost arithmetic | **V**, hides a factor | for the decoding of Proposition 5 the numbers have `O(cGN²)` bits (`α = (N log₂ 24 + O(1))·k_BT ln 2/ε`) |
| loop energies integer multiples of a unit `ε` (Proposition 5) | **Q** | needed to separate levels by digits; the free energy contains `k_BT ln R`, which is why the decoding is done per symmetry class |
| weights depending on loop sizes only | **T** of our implementation, not of the theorem | the referee's implementation has letter-dependent weights and agrees with brute force |
| MFE and level counts from the fixed-point sums | **proved after REV-0003** (Proposition 5, the referee's argument) | the first version cited [SW26, §7], whose decoding is per ordering and does not apply |

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
| Thm 11: `ρ_o = ρ_s`, `ρ_c + ρ_s ≤ 2ρ_a < 2ρ_s` | **E**, exact domain | explicit witnesses for every violated inequality (blow-ups, sunlets, a level-1 network on seven leaves) — reviewed by REV-0004 (correct as far as checked; the witness of (c) restated) |
| Lemma 0 (restriction commutes with display) | used everywhere | its proof had a gap (single source of the union of up-down paths), closed after REV-0004 with the referee's argument |
| Thm 11: the reading of "4-cycle" above level 1 | **V**, ours | the family is defined in the source for level 1 only |
| the list of 108 six-leaf systems | computed | the six-point check is kernel-checked for the list; that the list is the closure is not (CX-V3) |

### 3a. Added after the reviews: the sharp class for "Kalmanson" alone and level 2 (CX-T26, CX-T27) — unreviewed

| hypothesis | class | what happens without it; evidence |
|---|---|---|
| Thm 10′: closure under restriction **and** under replacing leaves by cherries | **E** for the "only if" direction | a single system outside `𝒦′` need not fail: 14 of the 17 excluded six-point systems have a Kalmanson metric themselves; the argument blows up a six-point restriction |
| Thm 10′(a): only the six-leaf terms non-negative (no condition on undisplayed splits) | exactly what "Kalmanson" needs among closed classes | the six systems of `𝒦′ ∖ 𝒦` are Kalmanson with a weight on an undisplayed split |
| Thm 12: level at most 2 | **T/C?** | the list of blobs that are not galled (Lemma C) is for two hybrid nodes; for three and more it has not been made.  The reduction to six positions of one blob (Step 1) holds for every level |
| Thm 12: outer-labeled planar | **E** for the list of positions | planarity empties one of the three paths of a nested blob; without it the family has more parameters and Lemma 1 has no circular order to offer |
| Thm 12(b): `k_1 ≥ 1`, `k_B ≥ 2` | **V** | otherwise there is no critical split: for `k_1 = 0` it is a cut-edge split, for `k_B ≤ 1` the blob displays the trees of a level-1 blob |
| Thm 12: sizes of pendant subnetworks enter only through their numbers of leaves | proved | pairs of leaves in one pendant subnetwork contribute `0`; no other term sees more than two leaves of one pendant subnetwork |
| Cor. 13: "Kalmanson for no circular order" when the critical weight is negative | **[X] only**, bloblets with at most nine leaves | Theorem 12 itself is about the planar order (and, for exact support, about every order) |
| Cor. 14: replacing leaves by clades | **E** for monotonicity | without it the criterion is not monotone: `N[4,1,1]` fails, `N[4,1,2]` has weight 0, `N[4,1,3]` satisfies the conclusion |

**Vacuity check.**  Thm 4 turns a statement about all `n` into a check on six-leaf restrictions — finitely
many for the network class, but for an arbitrary split system given explicitly it is a polynomial-time test
(`O(n⁶)` restrictions), not vacuous.

## 4. Ising ground sets (`ISING_GROUND_SETS.md`; CX-T16–T19, T25, T28, T29) — reviewed by COMPLEXITY-REV-0004; CX-T28, T29 added afterwards

| hypothesis | class | remark |
|---|---|---|
| all pairs may be coupled | **T/C** | the twin reduction adds couplings between twins; with a restricted interaction graph twins must be twins in the graph |
| no fields | **V** (corrected after REV-0004) | a field is one more site of constant spin; everything applies verbatim |
| global ground states (not single-flip stable states) | **C** | stability is a linear programme |
| `K` fixed | **C** — weakened after REV-0004 | not needed for polynomial time: `K = O(log n)` suffices (`2^K·poly(n)`, Corollary 5a).  For larger `K`: in co-NP, hardness unknown |
| Cor. 7: `1` and the products `t_kt_l` independent on the types | sufficient, **not necessary**; **known** (Laurent–Poljak) | needs more than `K(K−1)/2` types; void in the regime `K ≈ n` |
| Prop. 10: a pair-separating sign symmetry | **T** | without it only "not exposed ⟹ another sign vector in the span" holds; the converse is false in general — and the gap is exactly "degree 2 versus higher degree" (Prop. 13) |
| Prop. 13: the certificate has degree 2 | **E/C** | with it, "exposed" becomes "no other sign vector in the span", which is co-NP-complete to decide (Thm 14); without it the complexity is open and the hard instances of Thm 14 are all exposed |
| Prop. 13′: independent uniform states, `K ≤ n/20` | **Q** | the union bound; the true threshold is not determined; for small `n` the event "another sign vector" is common (`≈ 4C(K,3)(3/4)^n`) |
| Thm 14(b): the exponential time hypothesis with sparsification | conditional | cited, not re-derived |
| the earlier reformulation "exposed ⇔ unique decomposition of the Hamming metric" | **false** beyond simplicial faces | corrected after REV-0004, finding 1 |
| Prop. 11: general position of the conformers | **T** | assumed for random conformers beyond `D_d'`, not cited |

## 5. Penalised models (`PENALTY_THRESHOLD.md`; CX-T21–T23) — unreviewed (not covered by REV-0003 or -0004)

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

Found by the reviews COMPLEXITY-REV-0003 and -0004 (2026-11-26) and corrected in the notes:

* **algorithm note:** "we found no statement of this in print" — false as worded: for the base-pair model
  the partition function over all orderings with rotational symmetries is in the journal version of
  Boehmer et al. (2025), which we had not read; "MFE and #SSEL within the same bounds via [SW26, §7]" —
  the citation does not apply (per ordering); the statement is now proved (Proposition 5); "the same
  recursion over (min,+)" for the minimum free energy — wrong; "the interior-loop term is the source of
  `N⁴`" — wrong;
* **Ising note:** "exposed ⇔ the Hamming metric decomposes in exactly one way" — false for non-simplicial
  faces; the structural section presented as ours what is Laurent–Poljak's (Corollary 7, Proposition 5);
  "the table does not help when `K` grows" overlooked a `2^K` algorithm; "with fields the twin argument
  changes" — inaccurate; "a sporadic orbit" — a member of a family;
* **NANUQ note:** a proof step of Lemma 0 was missing; the witness of Theorem 11(c) was described
  ambiguously.
