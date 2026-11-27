Message ID:                  COMPLEXITY-REV-0006
Message type:                Internal adversarial review of what the fifth review did not cover: docs/complexity/NANUQ_LOCAL_CRITERION.md §7.2 (Theorem 12′, Corollary 14(v), "History of (v)"), docs/complexity/CHAIN_GEOMETRY_HARDNESS.md (all of it), docs/complexity/NANUQ_HIGHER_LEVELS.md with the six-leaf survey, docs/complexity/PENALTY_THRESHOLD.md
From:                        Mathematical Biology and Computational Complexity Division (branch research/biological-complexity)
To:                          All divisions (for the record); Geometry division (the accuracy clause of the realizability statement in COMPLEXITY-RES-0009 changes); the division itself (findings to process)
Date and time (UTC):         2026-11-27 01:18 (read from the clock when this file was written)
Priority:                    High
Status:                      Review received 2026-11-27 about 01:00 UTC; **every finding has a disposition** (table at the end of this file); two remedies are deliberately not carried out and are recorded as open (findings 1 and 4)
Relevant source commit:      307654f (the referee notes that the four documents and the programs it ran are byte-identical at d920323 and 05865bb, which appeared during the review)
Related theorem or experiment: docs/complexity/THEOREMS.md CX-T34 (Theorem 12′), CX-T27 (Corollary 14), CX-T31, CX-X3 (higher levels, survey), CX-T32, CX-T33 (chains), CX-T21–CX-T23 (penalised product reference)
Related message/request IDs: COMPLEXITY-MSG-0006 (fifth checkpoint, where these statements were announced as unreviewed), COMPLEXITY-RES-0009 (to Geometry), COMPLEXITY-REV-0005 (finding 1, which Theorem 12′ answers); linked corrections are sent in COMPLEXITY-MSG-0007

Scientific context:
Sixth and last internal adversarial review of this research cycle.  It was commissioned at 23:36 UTC on 26 November,
before the research owner's consolidation directive (received about 00:58 UTC on 27 November); under that directive
the referee was asked to wrap up, delivered this report, and was stopped.  No further review was started.
Verdict of the referee: **no theorem of Theorem 12′, the chain note or the penalty note was found false; two
statements of the higher-levels note were wrong or unproved as written; one corollary of the chain note cited a
theorem that does not give the accuracy it claimed.**
(2) Corollary C of the higher-levels note had lost the qualifier `k_1 ≥ 1` and was false as written;
(3) the summary "the conclusion holds robustly iff every bloblet is in `𝒦`" was proved in one direction only for
networks obtained from subnetworks; (1) Corollary 5 of the chain note (realizability is NP-hard in the weak sense)
claimed an accuracy of `1/poly` on a citation, made from memory, that gives only an accuracy written in binary — the
claim is rescued by a theorem that nobody here has read; (4) the six-leaf survey identifies networks by an invariant
that is not complete from three hybrid nodes on; (7) the literature on fixed-angle chains was missing.
Theorem 12′ survived the referee's own code: an exact search over all circular orders on 25 620 explicit networks
with a negative critical weight.

What this review is and is not:
The referee was a separate AI agent instantiated by this division with an adversarial brief (re-derive, recompute
with code written from the definitions, search for prior art, state the strongest hostile objection).  It had no
access to our reasoning, only to the files of this branch.  **This is an internal AI review.  It is not independent
academic peer review**, and the results it covers remain unrefereed in the sense of the collaboration README.
Everything the referee reports about the literature was read through a page-fetching tool that returns a
model-written summary, not the text; we have opened none of the sources it names.  The report is reproduced verbatim
below (the referee could not save a report file itself; the text is its hand-back message).  A container restart at
about 00:24 UTC interrupted the referee; it was resumed, and according to its report nothing it had computed was
lost.  Paths in the report that point to a session scratch directory refer to the referee's working directory; its
programs and logs are preserved in `experiments/complexity/reviews/rev6_thm12prime_chain_levels/` (not stored:
pickled intermediate data, and the referee's copies of our own programs — where a script refers to `authors_copy/`,
use `experiments/complexity/nanuq/`, `chain_geometry/` or `penalty_threshold/` instead).

---------------------------------------------------------------------------------------------------------------
REPORT (verbatim)
---------------------------------------------------------------------------------------------------------------

# COMPLEXITY review 6 — Theorem 12′, chain-geometry note, higher-levels note, penalty note

**This is an internal AI review, not academic peer review. I did not modify the repository: nothing was created, changed or deleted in `/home/user/MetricChain`, and only read-only git commands were used (`log`, `status`, `diff`, `show`, `ls-tree`, `rev-parse`). All my files are in the scratch directory `…/scratchpad/review6/`.**

Two notes on delivery:
- **`report.md` was not saved.** The harness refused the write ("Subagents should return findings as text, not write report files"), and I did not work around it. This hand-back text is the report; please save it yourself.
- The container restart during Part C lost nothing I had computed (all logs survived). I repeated the two re-runs of the authors' programs that were interrupted.

## 2. Bottom line

**No theorem of Part A, B or D was found false. Two statements of Part C are wrong or unproved as written, and one corollary of Part B cites a theorem that does not give the accuracy it claims.**

- **Part A (Theorem 12′): correct, as far as I can determine.**
  - *Proved by me:* I re-derived every step of the proof and found no gap. The result is conditional on Theorem 12(a),(b), which I used as given.
  - *Computed by me:* own code from the definitions, exact integers, exact search over all circular orders. In 25 620 explicit networks with a negative critical weight (7–14 leaves) there is no Kalmanson order.
  - Corollary 14(v) and the paragraph "History of (v)" are right. The defects are in how the note describes its own evidence (findings 5, 6).
- **Part B (chain note): all derivations check.** This covers Theorem 1, the blow-up lemma, the triangle, Proposition 1a, the Consequence, the Remark, the Lemma of §3, Theorem 3, Proposition 4 and the ETH remark.
  - **One real gap (finding 1):** Corollary 5 claims hardness for `δ⁻¹` polynomial in `n` but cites the Grötschel–Lovász–Schrijver equivalence, which by Gharibian's account gives hardness only for exponentially small accuracy. The statement is rescued by a different citation (Liu's Proposition 2.8, as used by Gharibian 2010).
  - The attributions to Kallaugher et al. and to Piddock are accurate.
  - The literature on fixed-angle chains is not cited (finding 7). None of it contains Theorem 3.
  - I found neither the lifting identity nor the 3-4-5 triangle in the literature (searches only; this proves nothing).
- **Part C (higher-levels note): Theorem A(a)–(e) is correct, two surrounding statements are not.**
  - **Corollary C is false as written** (finding 2): the qualifier `k_1 ≥ 1` of Corollary 14(i) was dropped.
  - **The displayed "robustly … if and only if" is unproved in one direction** (finding 3): the "only if" is shown only for networks obtained from subnetworks of `N`.
  - The survey's counts are reproduced. But the survey identifies networks by an invariant that is not complete (finding 4): at three hybrid nodes at least 2 106 labelled networks are merged with non-isomorphic ones. The conclusions about split systems are unaffected as far as I checked.
  - Four of the 36 never-found systems cannot be displayed by any network at all (finding 13). For the other 32, a random search of mine up to 12 hybrid nodes found nothing.
- **Part D (penalty note): correct.** One inequality chain in Theorem 2 is misprinted (finding 14).

## 3. Commit reviewed

`307654f` on branch `research/biological-complexity` ("NANUQ beyond level 2: six-leaf survey up to four hybrid nodes …").

HEAD moved during the review (to `d920323`, then `05865bb`). The four documents and the programs under review are byte-identical between `307654f` and `05865bb` (`git diff --stat`, empty). The authors' programs were run from copies taken with `git show 307654f:…`, with `python3 -B`.

## 4. Verdicts

### Part A — `NANUQ_LOCAL_CRITERION.md` §7.2, Theorem 12′, Corollary 14(v), "History of (v)"

| claim | verdict | justification |
|---|---|---|
| Identity (∗); a strictly largest pair sum must be the crossing one | correct | Re-derived: a `C`-circular split inducing `ps|qr` or a trivial split on the four leaves contributes 0. The Kalmanson condition is "crossing sum ≥ the other two". |
| Five leaves; only `S*` with non-zero weight separates `{Y,X_1}` from `{B_1,C_c}` | correct | Re-derived for intervals through the pendant subnetworks at `y` and `x_1`, for critical splits of other blobs, and for every kind of entry. Computed: 35 002 other separating splits, all of weight exactly 0. |
| The three displayed splits (of `T_3`, `T_1`, the `b`-arm of `T_2`/`T_4`), `k_2 ≥ 1` and `k_2 = 0`, not critical | correct | By hand in both cases. Computed: displayed and of positive weight in 5 134 cases on explicit networks; the four trees equal the switchings for 30 triples `(k_B,k_1,k_2)`. |
| Final contradiction | correct | (2), (3) put `Y` and `X_1` on the same side of `{B_1,C_c}`; (1) separates them. |
| Parts (a), (b), including "support `Split(T(N))`" for other orders | correct | (b) uses the uniqueness of the representation by `C`-circular splits; no other order enters. |
| A suitable `Z` exists whenever the weight is negative | correct | `α(S*) < 0` forces `|M| ≥ 2`. The proviso "`j < k_B` if `k_2 = 0`" is automatic (finding 6). |
| Theorem 12′ as a whole | correct, given Theorem 12 | Theorem 12(a),(b) used as given; re-confirmed as a by-product on every circular split of 25 638 explicit networks. |
| Corollary 14(v) restored, proof of (v) ⇒ (i) | correct | The clade blow-up keeps `β_1, G, ξ_1, R`; then Theorem 12′. |
| "History of (v)" | accurate | Compared with REV-0005, finding 1 (120 + 150 instances) and the addendum. |
| Numbers in the evidence parenthetical | reproduced | `level2_all_orders.py 13 10` re-run in full; `level2_all_orders_explicit.py 500 6 12 8` re-run; the other two logged runs matched on their counts of negative weights (111, 76). |
| Description of what the two programs cover | overstated | Findings 5, 6. |

### Part B — `CHAIN_GEOMETRY_HARDNESS.md`

| claim | verdict | justification |
|---|---|---|
| §1 identity (1), inverse, range `w` | correct | Algebra; 200 random chains. |
| Gadget inequality `h(t) ≤ 10 − t²` | correct | Squared twice; both sides positive; polynomial `76t² + 125t⁴ − 10t⁶ + t⁸/4`. |
| Theorem 1 | correct | Both cases re-derived: `|p_v|² ≤ τ_v/(1−|s|) ≤ 2τ_v`; the edge inequality with `x² + y² − xy ≤ 1`; `Λ = 4|E| ≥ 3d_max`. 11 new graphs, never exceeded. |
| Corollary 2 | correct | `5|V| + 5` atoms, integer data. |
| Blow-up lemma | correct | Equal fields for the copies; sequential replacement. |
| Right-angle triangle `g(t) ≤ 25 − t²` | correct | `t²(94 − 24t + t²) ≥ 0`. |
| Proposition 1a | correct | The multi-affine step is valid (no loops; a linear function on a ball is maximal on the sphere). `λ_1 ≥ L/(k+1)`. `4.5(k+1)Δ` suffices. The lower bound uses `3u + 4z + 5r = 0`. |
| Consequence | correct | Polynomial for each fixed `k` (degree grows with `k`, finding 11). Thresholds differ by `2·9^{k−1}`. |
| Remark (approximation) | correct, given Piddock's preprint | Data including the diagonal `Q̃_kk = deg(k)/2` verified. |
| Corollary 5 | correct with gap | Bijection, body, inscribed ball, direction of the reduction and integrality are all fine. The clause "`δ⁻¹` polynomial in `n`" does not follow from the cited theorem (finding 1). |
| Lemma of §3 | correct | All cases; the parity rule is superfluous (finding 8). |
| Theorem 3 | correct | Designated bonds range over `(S²)^N`; `Q̃` vanishes elsewhere, diagonal included. |
| Proposition 4(a),(b) | correct | A rotation by `δ` moves a unit vector by `2 sin(δ/2) ≤ δ`. There are `l − k − 1 ≤ w − 2` torsions between coupled bonds. State and cost as stated. |
| ETH remark | correct, given the standard bound for Max-Cut | Chain length is `O(|V|)`; the bound itself was not re-derived. |
| Attribution to Kallaugher et al. and Piddock | accurate | Checked on the arXiv abstract and HTML pages (finding 9 for details). |
| Prior-art coverage | incomplete | Finding 7. |

### Part C — `NANUQ_HIGHER_LEVELS.md`

| claim | verdict | justification |
|---|---|---|
| Theorem A(a) | correct | Step 1 uses the level only to classify the sink blob. The finite fact was recomputed (74 substitution systems, all 6-locally good). Own check on 12 000 networks of levels 2–8. |
| Theorem A(b) | correct | Closure under restriction, plus (a). |
| Theorem A(c) | correct as worded | The converse is for networks obtained from *subnetworks*. |
| Theorem A(d) | correct | If the end leaves sit at four positions of `𝔅`, at least three of them lie in one pendant subnetwork of any other blob. |
| Theorem A(e) | correct | Every position lies on one side of a split that cuts the blob; Step 4 needs only Lemma D. Not checked numerically. |
| Displayed "robustly … iff"; Remark "(b)–(c) decide the robust question" | unproved ("only if") | Finding 3. |
| Corollary B | correct | Lemma B0 ⇒ every hybrid node is a position ⇒ Lemma A. |
| Corollary C | **false as written** | Finding 2. |
| §2.1 description against the code | accurate, with one false claim in the code | Insertions, acyclicity, wheel test and `sym` are as described. The unfolding is not a complete invariant (finding 4). |
| §2.2 counts | reproduced for 0–3 hybrid nodes | 126 / 2 988 / 59 706 labelled; 12 / 253 / 5 000 / 96 095 classes; 1 151 442 labelled at `k = 3`; 14 / 71 / 113 / 114 systems. `k = 4` not re-run. |
| Table of the 36 missing systems | reproduced | Eight classes, sizes, splits and status agree. |
| §2.3 items 1–3 | justified as hedged | Item 2 is conditional and says so. |
| A network displaying one of the 36 | none found | 4 are impossible for every network; random search to 12 hybrid nodes. |

### Part D — `PENALTY_THRESHOLD.md`

| claim | verdict | justification |
|---|---|---|
| Theorem 1 | correct (for `λ ≥ 0`) | Component factorisation; Jensen. |
| Theorem 2 | correct with a misprint | The middle term of the chain is wrong when `s + 1 < k_min` (finding 14). |
| Proposition 3 | correct | Project selection; the maximum is 0 iff `λ ≤ λ_0`. |
| Proposition 4 | correct | `G(x) ≤ γ^max(S)`, `ln(1/P_0(x)) ≥ Σ_S ln(1/q_i)`. |
| Proposition 5(i),(ii) | correct | Read through; the brute-force program was re-run. |
| Toy programs | reproduce | `price_bound.py 3` reproduces `toy_run_seed3.log` exactly. |

## 5. Findings

1. **MAJOR (gap in the cited justification; the statement is true). `CHAIN_GEOMETRY_HARDNESS.md` §2b, Corollary 5; also §0 item 2 and `THEOREMS.md` CX-T32.**
   - *What is right.* The map `m ↔ G(m)` is a linear bijection. `conv E_3` is a centred well-bounded body in the `C(n−1,2)` off-diagonal coordinates, with `r = C(n−1,2)^{−1/2}` and `R = C(n−1,2)^{1/2}`. The direction is the right one (optimisation reduces to membership). The Theorem 1 instances have integer optimum and polynomial `‖Q‖`, so weak optimisation with accuracy `1/poly` decides the threshold. The note's one-sided promise problem is at least as hard as the two-sided weak membership problem.
   - *What is wrong.* The cited equivalence is oracle-polynomial in the *encoding length* of the accuracy. According to Gharibian (QIC 10 (2010) 343–360, arXiv:0810.4507), the Yudin–Nemirovskii link through the shallow-cut ellipsoid method "results in exponential scaling" of the membership accuracy.
   - *What rescues it.* Gharibian uses Liu's Proposition 2.8 (Y.-K. Liu, thesis, 2007): for `B(p,r) ⊆ K ⊆ B(0,R) ⊂ ℝ^m`, weak optimisation with error `ε` reduces to weak membership with error `β = r³ε³ / (2¹³·3³·m⁵·R⁴·(R+r))`. With `m = C(n−1,2)`, `R = 1/r = √m` and `ε = 1/poly` this gives `β = 1/poly`.
   - *Basis.* Gharibian's paper read through the fetch tool's summary of its HTML. I did not open the Grötschel–Lovász–Schrijver book or Liu's thesis.
   - *Fix.* Cite Liu's Proposition 2.8 and Gharibian. Or weaken to "`δ` given in binary".

2. **MAJOR (a stated corollary is false as written; one-phrase fix). `NANUQ_HIGHER_LEVELS.md` §1, Corollary C.**
   - It says a blob with two hybrid nodes has `Σ(𝔅) ∈ 𝒦` "iff it is galled, or nested with at most one middle position".
   - Corollary 14(i) of the main note is about nested blobs **with `k_1 ≥ 1`**. A nested blob with `k_1 = 0` and any number of middle positions is in `𝒦`: the bad six-tuples of Step 1 need an `x`-position.
   - *Computed.* For `N[k_B,0,k_2]`, `k_B = 3..6`, `k_2 = 0..2`: no six-leaf restriction has the pattern. With clades of sizes 1–4 at the positions (47 networks, up to 15 leaves) all weights are `≥ 0` and positive exactly on the displayed splits.
   - *Fix.* "…nested with `k_1 = 0` or with at most one middle position".

3. **MAJOR (unproved "only if" in a summary statement; Theorem A itself is worded correctly). `NANUQ_HIGHER_LEVELS.md` §1, the displayed sentence after Theorem A, and the first sentence of the Remark.**
   - The sentence before defines the question for `N` and its clade replacements. Theorem A(c) proves the converse only for "some network obtained from a *subnetwork* of `N`".
   - For `N` itself the six-leaf term that goes wrong need not be a term of a split of `N`: the four end leaves need not be adjacent in `N`. The main note records this obstacle itself (§7.1, Remark 2: "For a single network only the 'if' direction holds").
   - For level 2 the "only if" is true (Corollary 14, through the explicit formula and Theorem 12′). For level ≥ 3 it is unproved.
   - *Fix.* Define "robustly" as "for `N`, its subnetworks `N|_Y`, and all networks obtained from these by replacing leaves by clades". Or state the "only if" for `N` as open.

4. **MINOR. `six_leaf_survey.py`, docstring ("a complete invariant for binary networks with distinct leaf labels"); `NANUQ_HIGHER_LEVELS.md` §2.1, §2.2; `THEOREMS.md` CX-X3.** The marked unfolding is not a complete invariant.
   - *Example.* Three hybrid nodes, both outer-labeled planar for `(0,…,5)`, both produced by the insertion rule. Children lists, root 6, leaves 0–5:
     ```
     N1: 6→15,14  15→13,16  13→11,14  11→7,16   7→8,3  8→9,2  9→10,1  10→0,5  14→12  16→12  12→4
     N2: 6→13,14  13→11,14  11→15,16  15→7,16   7→8,3  8→9,2  9→10,1  10→0,5  14→12  16→12  12→4
     ```
     The authors' own `unfolding_key` gives both the key `((((((((L0,L5),L1),L2),L3),[[L4]]),[[L4]]),[[L4]]),[[L4]])`. They are not isomorphic (networkx, leaf labels fixed). The four spine nodes point to the hybrid nodes 14, 16, 14, 16 in `N1` and 14, 14, 16, 16 in `N2`.
   - *Mechanism.* Two hybrid nodes with a common hybrid child have equal unfoldings, so their parents can be paired differently. This needs three hybrid nodes.
   - *Size of the effect.* For `k ≤ 2` the key classes equal the classes of my finer invariant (59 706 = 59 706). At `k = 3` there are 96 095 keys but at least 96 271 classes up to rotation and reflection: 106 keys hold 2 or 3 pairwise different networks. Labelled: at least 1 153 548 instead of 1 151 442.
   - *Consequences.* In all 106 collisions the networks display the same set of trees, so the systems at `k ≤ 3` are unaffected. But the survey extends only one network per key, so at `k = 4` the extensions of the dropped networks were never generated. I did not test whether a system is lost there.
   - *Fix.* Identify by a finer canonical form (bottom-up key plus top-down context, isomorphism test inside ties), or keep all networks of a key. Restate the counts as "unfolding classes". Correct the docstring.

5. **MINOR. `NANUQ_LOCAL_CRITERION.md`, parenthetical after the proof of Theorem 12′, and §10, row `level2_all_orders_explicit.py`.** The explicit test hardly exercises the cases the proof is about.
   - Instrumented re-run of the three logged runs: of 287 negative critical weights, 262 are in blobs with the root on `A`. Of the 25 entered through a cut edge: middle `b` 15, `b_{k_B}` 7, `b_1` 2, `c_1` 1, `c_e` with `e ≥ 2` none.
   - Position `y` carries more than one leaf in 6 of the 287, `x_1` in 11. Step (1) of the proof is about exactly these intervals.
   - `level2_all_orders.py` does put clades of up to three leaves at `y` and `x_1`, but takes the four trees by formula and uses caterpillars of one orientation.
   - *Fix.* Report this breakdown and add a targeted generator. My runs supply the missing evidence: 2 024 / 2 001 / 1 828 / 2 328 / 3 440 negative blobs entered at `b_1` / `c_1` / `c_e` / `b_{k_B}` / a middle `b`, with compound pendant subnetworks at `y` and `x_1`.

6. **MINOR. Same parenthetical ("the five leaves taken from the circular order alone"), and the statement of Theorem 12′.**
   - In `level2_all_orders_explicit.py` only `B_1` and `C_c` are read off the order. `Z`, `Y`, `X_1` come from the generator's record of the positions (lines 79–86), as in `level2_all_orders.py`. This is right for checking the proof's inequalities, but it is not independent of the proof.
   - The independent evidence is the search over all orders: 423 formula-tree instances with at most ten leaves and 53 explicit networks with at most eight or nine.
   - Wording of the theorem: "binary semi-directed, `n ≥ 4`" is omitted. "and `j < k_B` if `k_2 = 0`" is redundant. "By Theorem 12(b), `M` contains at least two positions" also needs `k_1 ≥ 1`, `k_B ≥ 2`, which follow from Theorem 12(a). The label should read "[P, given Theorem 12] + [X]".
   - *Fix.* Correct the sentence and the wording.

7. **MINOR (prior art not cited). `CHAIN_GEOMETRY_HARDNESS.md` §7 and the sentence "Whether the statement of Theorem 3 is in the literature … we have not searched".** There is a literature on fixed-angle chains:
   - M. Soss, G. Toussaint, *Geometric and computational aspects of polymer reconfiguration*, J. Math. Chem. 27 (2000) 303–318: flattening and minimum/maximum flat span of fixed-angle chains are NP-hard (weakly, from Partition, according to later papers).
   - E. Demaine, S. Eisenstat, *Flattening fixed-angle chains is strongly NP-hard*, WADS 2011 (LNCS 6844): strong NP-hardness, also for equal lengths.
   - E. Demaine, H. Ito, J. Lynch, R. Uehara, arXiv:2212.12450 (CCCG 2022): equilateral chains with angles 90°/180°.
   - N. Benbernou, J. O'Rourke, *On the maximum span of fixed-angle chains*, CCCG 2006, arXiv:0801.0258: the maximum 3D span is polynomial for equal angles.
   - C. Borcea, I. Streinu, *Extremal reaches in polynomial time*, SoCG 2011, 472–480: the global maximum and minimum of the end-to-end distance of a 3D chain with fixed lengths and angles, in polynomial time.

   None contains Theorem 3: they treat planar non-crossing configurations with variable angles, or a single pair. But Borcea–Streinu is CHAIN(θ) with the single data point `c_{1n} = ±1`, and it is polynomial. So the hardness of Theorem 3 comes from many pairs with both signs, not from the fixed angle. The model also has a standard name (freely rotating chain). All of this is from search summaries and one abstract page; full texts were not opened.
   - *Fix.* Cite these and state the contrast.

8. **MINOR. `CHAIN_GEOMETRY_HARDNESS.md` §3, Lemma.** Correct in all cases, with three remarks.
   - The parity rule is not needed. Stepping towards `q` whenever more than two steps remain keeps `d ≤ rψ`, since the new distance is `|d − ψ| ≤ (r−1)ψ` for `r ≥ 3`. My simpler construction passed 6 420 cases, including `d = 0`, `d = π`, `d = 2ψ` and `θ` near 0, `π/2`, `π`.
   - The lemma is a special case of the classical closing condition for spherical polygons (`m` sides `ψ ≤ π/2` and one side `d`; only `d ≤ mψ` binds). I know this criterion from memory and from a search summary of arXiv:2305.07160; I could not open a primary source.
   - `m` is best possible: `m − 1` steps stay within distance `(m−1)ψ < π`.
   - *Fix.* Drop the parity rule or keep it as optional; cite the criterion as known.

9. **MINOR (attribution details). `CHAIN_GEOMETRY_HARDNESS.md` §7, table.**
   - *E.-Nagy, Laurent, Varvitsiotis.* The abstract also says that deciding membership in the convex hull of `E_k(G)` is NP-hard for every fixed `k ≥ 2`. §2b says so; the table lists only membership in `E_k(G)`. This is the closest prior art for the realizability question (partial data). For complete data I found no statement.
   - *Kallaugher et al.* Theorem 1.5 is for a promise version: completeness value `m(11 + 2√3)`, soundness gap `Θ(m⁻²)`. "This contains Theorem 1" is right after scaling the couplings; say so. Their footnote credits an earlier unpublished proof for product-state Quantum Max-Cut to J. Wright (2022); the note does not mention it.
   - *Piddock.* Verified: Theorem 3 verbatim, triangles plus a bipartite expander, inequalities only (no exact identity), one arXiv version, no journal reference.

10. **MINOR. `heisenberg_reduction.py` part (5) against §3 and §6 of the note.** The program uses `Q̃ = Q/2` (it prints "data 2c integral") and the threshold 841 for `F`. The note says integer data from `Q̃ = Q`, for which the objective is `2F` and the threshold 1682. Part (5) also evaluates only the explicit optimum. Harmless; align the two. My check with integer data: the paw graph gives a 71-atom chain whose objective equals `2F` on random configurations and `2·1442` at the optimum.

11. **MINOR. §2a, "Consequence".** The reduction is polynomial for each fixed `k`, but the degree grows with `k`: `Δ(H′) = max(3Δ + 9L, 8n) ≥ 8n` and `|V(H′)| ≈ 22.5(k+1)nΔ`, so the exponents grow like Fibonacci numbers. Say so.

12. **MINOR. `NANUQ_HIGHER_LEVELS.md`, proof of Theorem A(a).** "the 624 such systems on six points" repeats a wording corrected in the main note after REV-0005 finding 4. They are 624 quadruples giving 74 systems (my count: 74).

13. **MINOR (an addition, not an error). `NANUQ_HIGHER_LEVELS.md` §2.2, §2.3 item 3.** Two of the eight never-found classes, 4 systems, are displayed by no network at all, planar or not.
    - The classes are "all six 2-splits, no 3-split" (1 system) and "`12 23 45 56 | 234 345`" (3 systems).
    - In each, the only binary planar trees inside the system are two trees, both needed, with no common non-trivial split and different restrictions after deleting any single leaf.
    - Two switchings that differ at one hybrid node give trees that differ by moving one pendant subtree, so the displayed trees of a network are connected under such moves.
    - For the other six classes a connected covering family of trees exists, so this argument does not apply.
    - The authors' research log at `05865bb` (after the reviewed commit) records the same count "4 of the 36". I found it independently before reading that entry. It is not in the note.

14. **MINOR. `PENALTY_THRESHOLD.md` Theorem 2, displayed chain.** The middle term `Σ_{S connected, |S| > s} q(S) e^{λγ^max(S)}` includes sets with fewer than `k_min` sites, which contain no table and contribute `q(S)`. The right-hand side starts at `s′ = max(s+1, k_min)`.
    - As printed, "middle ≤ right" fails in 70 of 480 toy cases of mine, all with `s + 1 < k_min`.
    - With the middle sum over `|S| ≥ s′` (or over sets containing a table) the chain holds in all 480. `price_bound.py` checks such a correct variant, not the printed one.
    - *Fix.* Restrict the middle sum.

15. **MINOR. `PENALTY_THRESHOLD.md` Theorem 1 and Theorem 2.** `λ ≥ 0` is used (`f_U ≥ 0`) and not stated. `λ < λ_0` is used in Theorem 2 and follows from `ε < 1` only because `q_max < 1`.

16. **MINOR. `NANUQ_HIGHER_LEVELS.md` §2.1, the caveat on networks not generated.** Accurate as far as it goes, but incomplete.
    - It should mention finding 4.
    - Six positions of a blob in a larger network give a subnetwork `N|_Y` which, after suppression, can have parallel edges. So the hypothesis of §2.3 item 2 concerns more than the generated networks. The hedge there covers it.

## 6. What I computed

All Part A and Part C computations use exact integer arithmetic. Part B uses floating-point optimisation and is evidence only.

**Part A (own library `partA/rn.py`: rooted network → switchings → displayed quartets → 6·d as integers → split weights → exact backtracking search over all circular orders).**
- *Anchor.* The network `N*` reproduces the matrix printed in §6 of the note; weight `−1`; no order among the 360.
- *Search validation.* 400/400 scrambled circular-decomposable metrics recognised (5–12 points). 300/300 agreement with brute force on perturbed matrices (175 with an order, 125 without).
- *`t1_thm12prime.py`, eight runs.* 24 000 explicit networks of level ≤ 2 with 7–14 leaves (trees, cycles, galled and nested level-2 blobs as pendant subnetworks).
  - 15 000 have a negative critical weight (15 003 negative critical splits). All 15 000 searched over all orders: none.
  - Theorem 12(a),(b) holds on every circular split of all 24 000.
  - 207 718 quintuples `(B_1, Z, C_c, Y, X_1)` satisfy the three strict inequalities and the identity for the first difference.
  - 34 272 other splits separating `{Y,X_1}` from `{B_1,C_c}` have weight exactly 0.
- *Two-blob tests.* 1 368 + 270 networks, 1 032 + 250 with a negative weight, 340 + 132 with two negative critical weights. The lower blob hangs at `b_1`, a middle `b`, `b_{k_B}`, `c_1`, `x_1` and `y` of the upper one. No order.
- *`t3_mutation.py`, four runs (no use of blobs or positions).* 30 000 planar networks of level ≤ 2 from random trees or mutated bloblets, order read from the embedding. 9 338 have a negative weight (9 273 / 56 / 9 with 2 / 3 / 4 hybrid nodes, 7–13 leaves). None is Kalmanson for any order.
- *Totals.* 25 620 networks with a negative weight searched; 224 739 quintuples; 35 002 zero-weight splits.
- *Named splits.* Displayed and positive in 5 134 cases.
- *Authors' programs.* `level2_all_orders.py 13 10` (2 min 34 s) and `level2_all_orders_explicit.py 500 6 12 8` reproduce their logs.

**Part B.**
- *`b1_thm1.py`.* Theorem 1 on 11 graphs not used by the authors (claw, paw, bull, `K_{2,3}`, `K_5`, `C_7`, prism, `K_3 + K_2`, edge plus isolated vertex, wheel, Petersen).
  - Reduced and full objective; 11 adversarial starts each (equal or antipodal poles, `s = ½`, vector optimum of `G` in general position, flattened into the plane of the poles, tilted optimum) plus random starts.
  - The formula is attained and never exceeded.
  - With `Λ = 0.05` the same test finds violations for the paw, `K_5` and `C_7`.
- *`b2_prop1a.py`.* 14 liftings, `k = 1→2` up to `4→5`, on graphs with closed-form `OPT_k`; 21 starts each, 7 adversarial. Attained, never exceeded. Too few poles: violations for `K_5` (`L = 1`) and `C_7` (`L = 2`). Explicit `H′` for `C_4` (444 vertices; only a local optimum 1800 < 1836 was reached) and `K_5` (1 059 vertices; 4518 reached).
- *`b3_fixed_angle.py`, `b4_identities.py`.* The Lemma (6 420 cases); Theorem 3 end to end with integer data; the identities of §1, §2a, §2b; the two elementary bounds of Theorem 1; the torsion bound of Proposition 4 (largest ratio 0.9926).
- *Authors' programs.* Both re-run: "ALL OK".

**Part C.**
- *Counts (own code).* Labelled networks 126 / 2 988 / 59 706 for 0–2 hybrid nodes. Classes 12 / 253 / 5 000 / 96 095 for 0–3. Labelled at `k = 3` by key: 1 151 442. Systems 14 / 71 / 113 / 114.
- *Collisions.* The explicit pair of finding 4; all 106 colliding keys; labelled count by the finer invariant.
- *Random search (`c5_random_search.py`).* Six-leaf planar networks with coinciding edges allowed (parallel edges): 151 159 samples with four hybrid nodes and 374 402 with 5–12. No system outside the 114.
- *Tables.* 150 / 127 / 17 recounted; the 36 missing systems and their status; tree-connectivity for each class.
- *Theorem A(a).* 12 000 networks of levels 2–8 (7–10 leaves), 890 043 six-subsets: 16 759 restrictions are not 6-locally good, and all of them sit at six positions of one blob.

**Part D.**
- *`d1_check.py`.* 32 random instances × 10 values of `λ`: Theorem 1, Propositions 3, 4, the connected-set count, Theorem 2 in the corrected reading (480 cases), and the failure of the printed chain (70 cases).
- *Authors' programs.* `price_bound.py 3` reproduces its log exactly; `hardness_maxcut.py` runs.

## 7. What I searched and read

Everything below was read through the fetch tool, which returns a model-written summary of the page, not the raw text.

| source | URL | what I read |
|---|---|---|
| Holtgrefe et al. | arxiv.org/abs/2507.17308, arxiv.org/html/2507.17308v2 | Abstract page; Def. 4.1 and Eq. (10) (sum of `2ρ` plus `2n−4`, unweighted average); Theorem 4.7; the conjecture. Table 1 could not be retrieved. |
| Kallaugher, Parekh, Thompson, Wang, Yirka | arxiv.org/abs/2401.06725, arxiv.org/html/2401.06725v2 | Abstract; v1 12 Jan 2024, v2 6 Jan 2025; ITCS 2025, LIPIcs 325, 63:1–63:32. Theorem 1.5; definition of `MC_k`; the Lovász sentence; the Wright footnote; the proof part (3-Coloring, thresholds, bibliography). |
| Piddock | arxiv.org/abs/2510.07995, arxiv.org/html/2510.07995v1 | Abstract; single version of 9 Oct 2025. Theorem 3; gadgets; prior work; no exact identity. |
| E.-Nagy, Laurent, Varvitsiotis | arxiv.org/abs/1203.6602 | Abstract. |
| Gharibian | arxiv.org/abs/0810.4507, ar5iv.labs.arxiv.org/html/0810.4507 | Abstract; Liu's Proposition 2.8 with the formula for `β`; the remark on the Yudin–Nemirovskii link. |
| Demaine, Ito, Lynch, Uehara | arxiv.org/abs/2212.12450 | Abstract. |
| Kapovich, Millson | cambridge.org (Canad. Math. Bull. 42, 1999) | Abstract only; the inequalities are not on the page. |

Search queries (results read as summaries):
- Bachas 1984, "Computer-intractability of the frustration model of a spin glass". Result: three-dimensional Ising only; no older hardness result for vector spins found.
- NP-hardness of the classical Heisenberg spin glass / rank-constrained Grothendieck problem. Nothing relevant.
- Soss–Toussaint; Benbernou–O'Rourke; Borcea–Streinu; fixed-angle chain reachability. Results as in finding 7.
- Kapovich–Millson spherical polygonal linkage; spherical polygon inequalities.
- Vector Max-Cut reduction `k → k+1`, right angle, 3-4-5, blow-up identity. Nothing found.
- Membership in the convex hull of the rank-constrained elliptope. Only E.-Nagy–Laurent–Varvitsiotis.

Not accessible or not opened: the Grötschel–Lovász–Schrijver book; Liu's thesis; Lovász, *Graphs and Geometry*, p. 236; full texts of Soss–Toussaint, Demaine–Eisenstat, Benbernou–O'Rourke, Borcea–Streinu, Kapovich–Millson.

## 8. Strongest hostile objection

- **Part A.** "Theorem 12′ is a ten-line corollary. All its content is in Theorem 12(a), in particular in the claim that undisplayed non-critical splits have weight exactly zero, and that rests on computed tables that no kernel checks. The networks concerned lie outside the class of the published conjecture. The five-leaf obstruction gives no handle on level 3. The note's numerical confirmation mostly re-checks inequalities the proof already implies, on leaves chosen by the proof."
- **Part B.** "Everything hard here is known. The translation to chains is a change of variables. Theorem 3 shows only that the model is unphysical: a phantom chain with couplings of both signs and of size `|E|` between every `m`-th bond, the fixed angle being bought off with `m − 1` idle bonds per spin. For one pair the fixed-angle problem is polynomial (Borcea–Streinu), and that literature is not cited. The one statement that answers the question asked, Corollary 5, rests on a theorem cited from memory that does not give the accuracy claimed."
- **Part C.** "Theorem A is a re-reading of two steps of an existing proof. Its one new use, the robust criterion, is overstated, and its level-2 corollary is misquoted. The survey is not a classification, identifies networks by an invariant that is not one, and four levels of it say nothing about arbitrary level. The open question is untouched except for four systems that fall to a two-line argument."
- **Part D.** "Standard polymer-gas inequalities. By the note's own correction the explicit criterion is void on the instances that motivated it. The one displayed chain of inequalities is misprinted."

## 9. Not checked

- Theorem 12(a),(b), Lemmas C and D, and Theorems 10 and 10′ of the main note were used as given. They were re-confirmed only as by-products of my runs.
- Networks with parallel edges in Part A.
- Theorem A(e) (the weight polynomial) numerically. The claim "at most one blob" in A(d) beyond its proof.
- The `k = 4` level of the survey was not re-run. Whether the unfolding collisions lose a system at `k = 4` was not tested.
- Whether my finer invariant is complete (the corrected counts are lower bounds).
- `six_leaf_examples.py`, the Lean files, `six_leaf_treesets.py` and everything committed after `307654f`.
- The primary sources listed as not opened in section 7.
- The ETH lower bound for Max-Cut (standard; not re-derived).
- The dynamic programme of Proposition 4 was not implemented.
- In the penalty note: the list "What is polynomial" of §6 beyond a read-through (including the bound `n^{1+log₂Q}`), the complexity remarks of §3 (iii) that the note itself marks as from memory, and `price_bound.py` with seed 7.
- The global optimality of the numerical maxima in Part B (multi-start local optimisation can only fail to find a violation).
- Lost through the restart: nothing.

## 10. Files

Scratch directory `/tmp/claude-0/-home-user-MetricChain/70d1e32f-7f3d-51c2-b433-c26de14bc582/scratchpad/review6/` (no `report.md`, see the top of this report):

- `partA/`
  - Library and generators: `rn.py`, `gen_l2.py`, `chk.py`.
  - Tests: `t0_anchor.py`, `t_search_validation.py`, `t1_thm12prime.py`, `t2_twoblobs.py`, `t2b_twoblobs_big.py`, `t3_mutation.py`, `t4_named_splits.py`, `t5_k1zero.py`; runners `run_t1.sh`, `run_t3.sh`.
  - Logs: `log_t0_anchor.txt`, `log_search_validation.txt`, `log_t1_random_s1..4.txt`, `log_t1_targeted_s21..24.txt`, `log_t2.txt`, `log_t2b.txt`, `log_t3_s1..4.txt`, `log_t4.txt`, `log_t5.txt`, `log_authors_coverage.txt`.
  - `authors_copy/` — the authors' `nanuq/*.py` at `307654f`, my `instr_explicit.py`, `run_authors.sh`, and the re-run logs `rerun_all_orders_13_10.log`, `rerun_explicit_500_6_12_8.log`.
- `partB/`
  - `b1_thm1.py`, `b2_prop1a.py`, `b3_fixed_angle.py`, `b4_identities.py`; logs `log_b1.txt` … `log_b4.txt`.
  - `authors_copy/` — the two author programs and `rerun_heisenberg.log`, `rerun_lifting.log`.
- `partC/`
  - `c1_survey.py`, `c2_survey_sym.py`, `c3_collision.py`, `c4_collisions_all.py`, `c5_random_search.py`, `c6_missing36.py`, `c7_step1_fact.py`, `c8_labelled_inv.py`, `c9_theoremA.py`, `run_c5.sh`.
  - Data: `level_0.pkl` … `level_3.pkl`, `systems_k2.pkl`, `systems_level_1..3.pkl`.
  - Logs: `log_c1_k2.txt`, `log_c2_k3.txt`, `log_c3_collision.txt`, `log_c4_collisions.txt`, `log_c5_s11..13.txt`, `log_c6_missing36.txt`, `log_c7.txt`, `log_c8.txt`, `log_c9_s2.txt`, `log_c9_s3.txt`.
- `partD/`
  - `d1_check.py`, `log_d1.txt`, `rerun_clean.txt`.
  - `authors_copy/` — the two author programs, their two logs, and `rerun_price_seed3.log`.

---------------------------------------------------------------------------------------------------------------
END OF REPORT
---------------------------------------------------------------------------------------------------------------

Disposition of the findings (by the division; completed 2026-11-27 01:18 UTC):

| # | finding (short) | disposition |
|---|---|---|
| 1 | MAJOR: Corollary 5 of the chain note claims accuracy `1/poly` on a citation that gives accuracy in binary only | **Accepted; the statement is split, and one half is conditional.**  Corollary 5 now states hardness for an accuracy written in binary (Grötschel–Lovász–Schrijver, from memory) and, for `δ^{-1}` polynomial, "provided the sharper reduction is as reported" (Liu, thesis 2007, Proposition 2.8, through Gharibian 2010 — **read by nobody here**; the referee read a summary).  §0 item 2; `THEOREMS.md` CX-T32; `PRIOR_ART.md` D-VI, D-VIa; `OPEN_PROBLEMS.md` D2 ("to do before any external use: read the two sources").  **Linked correction** of COMPLEXITY-RES-0009 (row "C1 itself", which said "reject at distance ≥ 1/poly" without qualification) in COMPLEXITY-MSG-0007.  We did not open the sources ourselves: the consolidation directive of 27 November excludes new literature work |
| 2 | MAJOR: Corollary C of the higher-levels note is false as written (the qualifier `k_1 ≥ 1` was dropped) | **Accepted.**  Corrected ("galled, or nested with `k_1 = 0`, or nested with at most one middle position"), with the referee's check of 47 networks; the same qualifier added to `THEOREMS.md` CX-T27 (the row's summary of Corollary 14 had lost it too; the corollary itself in the main note was right).  The misquoted form was not sent to any division |
| 3 | MAJOR: "robustly … iff" is unproved in the "only if" direction for `N` and its clade replacements alone | **Accepted, first remedy.**  "Robustly" is now defined to include every subnetwork `N\|_Y` and its clade replacements; the note says that for `N` and its clade replacements alone the "only if" is proved for level ≤ 2 and open beyond; Remark reworded; `THEOREMS.md` CX-T31; `OPEN_PROBLEMS.md` B (beyond level 2, item 3) |
| 4 | MINOR: the marked unfolding is not a complete invariant; counts are counts of unfolding classes; at four hybrid nodes the extensions of merged networks were not generated | **Accepted in the text; the remedy is not carried out.**  Docstring of `six_leaf_survey.py`; §2.1 (new paragraph with the referee's numbers: at least 1 153 548 labelled networks and 96 271 classes at three hybrid nodes against 1 151 442 and 96 095 keys; 106 colliding keys, all with equal tree sets); §2.2 table header; `THEOREMS.md` CX-X3.  A re-run of the four-hybrid level with a complete canonical form (a code change and about 90 minutes) was **not** done — it is not near completion and the survey is not a classification either way; recorded as open (`OPEN_PROBLEMS.md` B, beyond level 2, item 2; note §3).  The referee's random search (151 159 samples with four hybrid nodes, parallel edges allowed) found no further system |
| 5 | MINOR: the explicit test of Theorem 12′ hardly exercises the cases step (1) is about | **Accepted.**  The breakdown (262 of 287 root-entered; 15 / 7 / 2 / 1 by entry position; `y` compound in 6, `x_1` in 11) and the referee's own runs are reported after the proof and in the table of §10; `THEOREMS.md` CX-T34.  We wrote no targeted generator of our own; the referee's is stored |
| 6 | MINOR: "the five leaves taken from the circular order alone"; wording of Theorem 12′ | **Accepted**, all four points: only `B_1`, `C_c` are read off the order (said, with the remark that only the searches over all orders are independent of the proof); "binary semi-directed, `n ≥ 4`"; the redundant proviso turned into a parenthesis; `k_1 ≥ 1`, `k_B ≥ 2` from Theorem 12(a); label "[P, given Theorem 12] + [X]" |
| 7 | MINOR, prior art: the literature on fixed-angle chains is not cited | **Accepted.**  New row in §7 of the chain note with the five papers and the contrast (Borcea–Streinu: the extremal end-to-end distance of a fixed-angle chain is polynomial, so the hardness comes from many pairs with both signs); `PRIOR_ART.md` D-VIII; `THEOREMS.md` CX-T33; `OPEN_PROBLEMS.md` D2.  All from the referee's search summaries; full texts opened by nobody.  Our own search had used the wrong vocabulary — recorded in `PRIOR_ART.md` §D and `ASSUMPTION_AUDIT.md` §6 |
| 8 | MINOR: the lemma of §3 — parity rule unnecessary, classical closing condition, `m` best possible | **Accepted** as a remark after the lemma (the proof is kept as written; the classical criterion is quoted at second hand, as the referee quotes it from memory) |
| 9 | MINOR: attribution details (E.-Nagy–Laurent–Varvitsiotis; Kallaugher et al.; Piddock) | **Accepted**: the convex-hull statement of the first, the promise version and the Wright footnote of the second added to §7 and to `PRIOR_ART.md` §D |
| 10 | MINOR: `heisenberg_reduction.py` part (5) uses `Q̃ = Q/2` (threshold 841), the note integer data (1682) | **Accepted**: the note states the program's convention and both thresholds; the program is unchanged |
| 11 | MINOR: the degree of the reduction grows with `k` | **Accepted**, said in the "Consequence" |
| 12 | MINOR: "the 624 such systems" | **Accepted**: 624 substitutions, 74 systems |
| 13 | MINOR (addition): four of the 36 missing systems are displayed by no network | **Accepted**, added to §2.2 with the argument (the displayed trees of a network are connected under moves of one pendant subtree) and the referee's random search.  Found independently by the referee and in our log of 27 November |
| 14 | MINOR: Theorem 2 of the penalty note, misprinted chain | **Accepted**: the middle sum starts at `s' = max(s+1, k_min)`; the misprint is recorded in the note.  Our program had checked a correct variant, which is why it did not catch the printed one |
| 15 | MINOR: `λ ≥ 0` unstated; `λ < λ_0` | **Accepted**, both said |
| 16 | MINOR: the caveat of §2.1 is incomplete | **Accepted**: finding 4 and the parallel edges of suppressed subnetworks added |

Not covered by this review (the referee says so): Theorem 12(a),(b), Lemmas C, D and Theorems 10, 10′ of the main
note (used as given; covered by REV-0005); Theorem A(e) numerically; the four-hybrid level of the survey; the Lean
files; `six_leaf_examples.py`, `six_leaf_treesets.py` and everything committed after 307654f; the primary sources
it lists as not opened; the global optimality of the numerical maxima in the chain note; the dynamic programme of
Proposition 4 of the chain note (not implemented).  **Not reviewed by anyone:** `CERTIFIED_BRACKETS.md` (CX-T35,
CX-T36), written after the review began, and the correspondence between the Lean files and the notes.

The referee's four "strongest hostile objections" are quoted in the four notes (main NANUQ note §9; chain note §7;
higher-levels note §3; penalty note §8).  We accept them as fair, with the two errors named in the third now
corrected: (A) Theorem 12′ is a short corollary whose content is in Theorem 12(a), which rests on a computed table
that no kernel checks, and it gives no handle on level 3; (B) everything hard in the chain note is known, the
translation to chains is a change of variables, and the instances of Theorem 3 are unphysical; (C) Theorem A
re-reads two steps of an existing proof, and the survey is not a classification; (D) the penalty note contains
standard inequalities whose explicit criterion is void on the instances that motivated it.

State of review after six reviews: every note of this division except `CERTIFIED_BRACKETS.md` has been through at
least one internal adversarial review; none has been seen by a human expert; none is peer reviewed.
