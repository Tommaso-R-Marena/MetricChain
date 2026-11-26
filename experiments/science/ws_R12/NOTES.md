# Workstream R12 — running notes

Independent review of what the theory division asked us to review in THY-RES-0010 §9.2
(theory branch at `9408e33`, read-only export
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_9408e33/`,
abbreviated `<EXP>` below).

All times UTC, 2026-11-26.

## Log

* 03:04 — started.  Read `COMMON.md` and `R12_brief.md`.  Created `experiments/science/ws_R12/`
  and `logs/`.  Our tree is at `d45ad56` (branch `research/scientific-translation`), untracked:
  P5/P6 reports and directories, the R12 brief.  Nothing of mine yet.
* 03:10–03:30 — read THY-RES-0010 in full; theory report (export) §11.30 lines 8888–9200
  (Theorem 11.110 (a)–(f), Corollary 11.111, "what the hint buys", Proposition 11.113,
  Corollary 11.114, "lower models"), §11.7 lines 2346–2422 (Theorem 11.18d, Proposition
  11.18e), §11.31 lines 9435–9517 (Theorem 11.115); `BoxClass.lean` (513 lines) in full;
  in `QueryLowerBound.lean` the structure `QueryAlgorithm`, `expected_queries_ge_packing`,
  `spotCheck`, `spotCheck_card_le`, `spotCheck_correct`.
  - `diff -q` export vs our tree: `proofs/Frontiers/QueryLowerBound.lean` IDENTICAL, so a
    copy of `BoxClass.lean` may be compiled here (brief, "Lean").
  - Old text of (e) (export of `24a3c27`, line 8881): the old *display* was a true pair of
    inequalities (its upper end contained `1/(1 − e^{−ε/2})`); what was false was the
    sentence after it ("the two bounds differ by a factor that depends on ε and δ only",
    "Θ((e^{ρ₋} − 1)/ε) … the ceiling ρ₊ … absent").
  - NOT yet opened: `experiments/falsify_conjectures.py` (their harness) — own code first.

### Item 1, re-derivation on paper (done before any code) — notation a = Z(lo)/Z − 1, b = 1 − Z(hi)/Z, z = Z(r)/Z₀
  - (d) greedy: if every point has dip weight ≤ t = (e^ε − 1)z, bins filled until the sum
    exceeds t have weight in (t, 2t]; with k complete bins U ≤ 2tk + t, so
    k ≥ ⌈U/(2t) − ½⌉ ≥ ⌊U/(2t)⌋ = ⌊a/(2(e^ε − 1))⌋.  Same for bumps with (1 − e^{−ε})z.  OK.
  - (e) upper end: N = ⌈ln(1/δ)·M⌉, M = max(1, 2a/(e^{ε/2} − 1), 2b/(1 − e^{−ε/2})).
    From k ≥ ⌊a/(2(e^ε − 1))⌋: a < 2(e^ε − 1)(k+1), so 2a/(e^{ε/2} − 1) < 4(e^{ε/2} + 1)(k+1);
    from k ≥ ⌊b/(2(1 − e^{−ε}))⌋: 2b/(1 − e^{−ε/2}) < 4(1 + e^{−ε/2})(k+1) ≤ 4(e^{ε/2}+1)(k+1).
    Hence N ≤ 4 ln(1/δ)(e^{ε/2}+1)(k+1) + 1.  OK — *needs* the single-state condition (for
    the greedy bound) and U, V > 0 (for the sampler to exist; at U = 0 or V = 0 drop that
    half — not covered by the Lean statement, which has `hU`, `hV`).
  - lower end: `expected_queries_ge_packing` with unit weights, B = 1.  OK.
  - Θ reading: for ε ≤ 1 uniform in ε (constants depend on δ only, additive constant);
    for large ε the factor is 4(e^{ε/2}+1)·ln(1/δ)/(1 − 2δ) — exponential in ε, so "/ε" is
    not the ε-dependence there (lower ~ a/(2(e^ε − 1)), upper ~ 2a/(e^{ε/2} − 1)).
  - Observation (mine): the mixture weights ½, ½ are not optimal; with weights
    λ ∝ a/(e^η − 1), 1 − λ ∝ b/(1 − e^{−η}) the detection probability is
    1/(a/(e^η − 1) + b/(1 − e^{−η})), i.e. N = ⌈ln(1/δ)·max(1, A + B)⌉ with A + B ≤ 2 max(A, B):
    the sum of the two terms, which is exactly the displayed quantity.  To be tested.
  - "what the hint buys" rule re-derived: wrong output at level v forces 1 − s > q(v)
    (up: (1 − s) > (e^η − 1)/(e^{ρ₋+v} − 1); down: (1 − s) > (1 − e^{−η})/(1 − e^{−(ρ₊−v)}) ≥ 1 − e^{−η});
    P(stop at v) = s_v^{N(v)}; so failure ≤ Σ s_v (1 − q(v))^{N(v)−1} ≤ δ.  OK.
    Arithmetic: (e³ − 1)/(e^{0.1} − 1)·ln 20 = 543.6 → 544; no hint 544 + 1 = 545; 2× → 1088.

**Correction of the clock (own error, harmless):** the times "03:10–03:30" above were guesses;
the machine clock read 03:12:53 when the reading was finished and 03:13:33 after the second
script.  From here on times are taken from `date -u`.

* 03:12 — `r12_01_box.py` written from the statements (harness not opened) and run:
  `logs/r12_01_box.log`, 15.6 s, last line `R12_01_DONE`.
  - Part A, 720 cases (random boxes n = 6, 8, 10; r interior / near floor / near ceiling /
    half-half; ε ∈ {0.02, 0.1, 0.2, 0.5, 1, 3}; δ = 0.05), packings exact by DP over subsets,
    fractional hitting numbers by LP: **0 violations** of: k_mix ≤ τ*; max(k_dip,k_bump) ≤ k_mix ≤ sum;
    greedy floors when no single state is heavy; `detect_ge` (exact detection probability ≥
    p(η), ratio min 1.0008, max 379); exact failure of the spot check ≤ δ (worst 0.0496);
    (e) upper end N ≤ 4 ln(1/δ)(e^{ε/2}+1)(k+1)+1 when no single state is heavy.
    In 387 cases where a single state IS heavy the one-stage N exceeds that bound.
    k_mix > max(k_dip, k_bump) in 108 cases.
  - Part B1: centre of [−3, 3], ε = 0.2, δ = 0.05, uniform π on 10³…10⁶ states: N_prop = 544,
    N_general = 1088 (their numbers), exact failure of 544 samples 0.0379…0.0495 ≤ δ;
    k = 83…86, (1 − 2δ)k = 74.7…77.4 ≤ cost ≤ 544 ≤ upper(e) = 2120…2196.
  - Part B2: at the floor of the constant box (a = 0): k_dip = 0, k_bump = 5, 20, 50, 100, 200 at
    ε = 0.2, 0.05, 0.02, 0.01, 0.005; the bump lower bound (45 at ε = 0.02) exceeds the upper end
    written with k_dip (25.1): the dips-only two-sided reading is refuted, as they say.
  - Part B3: Θ-reading in ε (centre, ρ₋ = 12): lower/((a+b)/ε) falls from 0.79 (ε = 0.1) to
    0.0024 (ε = 8); N_prop/lower grows from 7.4 to 187.  "Θ((a+b)/ε)" is uniform only for ε ≲ 1.
  - Part C: N(0) = 545, hinted 544, general 1088 — as reported.  Exact failure of the rule
    without a hint: sup over two-level members 0.9993·δ (v ≈ 2.998, second level at the floor,
    mass at the threshold); three-level random 0.9887·δ; all ≤ δ.  Their "0.994·δ" must be a
    grid value (to be compared when the harness is opened).
  - Part D: Monte Carlo of the spot check agrees with the exact miss probability.
* 03:13 — `r12_01b_twostage.py` (my own sharpening): `logs/r12_01b_twostage.log`, 2.4 s, last line
  `R12_01B_DONE`.  1425 cases, a single state heavy in 1238: the one-stage N exceeds
  C(k+1)+1 in 839; the two-stage count |H| + N_R exceeds it in **0** (largest ratio 0.49);
  worst exact miss probability of stage 2: 0.0287 ≤ δ.  So the hypothesis "no single state
  can change ln Z by ε" is not needed for the display of (e) — only for the closed form in a, b.

### Item 2, analysis before code (03:14–)
  - dimension N_ball: ANOVA decomposition, ⊕_{|U|<m} W_U, dim W_U = Π_{i∈U}(k_i − 1).  OK.
  - closure under adding order-<m functions: order-m mixed differences of such functions vanish. OK.
  - (a) deterministic adaptive: kernel of the evaluation map on Q(g) restricted to the space of
    order-<m functions has dimension ≥ N_ball − |Q| ≥ 1; g + th is indistinguishable; min → −∞,
    ln Z → +∞.  OK.  "any unisolvent set does": g = I_{m−1}g + R, |R| ≤ C; the values on a unisolvent
    Q determine I_{m−1}g up to ‖Λ_Q‖·C — a finite bound, of quality set by the Lebesgue constant
    of Q.  OK (finite; the ball has Λ explicit).
  - support lemma, proof by induction on the number of sites (slices f_s = f(·, s)): if no slice
    vanishes identically each has fraction ≥ bound; if one does, the others are differences of
    slices, of order < m − 1, and at least one is non-zero: fraction ≥ (1/k_n)·bound(m − 1).
    For unequal alphabets the same induction gives fraction ≥ 1/(product of the m − 1 largest
    k_i), attained by a cylinder on those sites.  To be brute-forced.
  - **(b) is false as written (if the task is that of (a) with failure probability δ).**
    Counter-algorithm (mine): g = h + R, h = I_{m−1}g of order < m, |R| ≤ C_m.  There is
    c = c(grid, m) > 0 with #{x : |h(x)| ≥ c‖h‖_∞} ≥ ρ|X| for every h of order < m (ρ the least
    support fraction; compactness of the unit sphere of the finite-dimensional space, the
    ⌈ρ|X|⌉-th largest |h(x)| is continuous and positive there).  Draw q uniform points,
    M = max|g(x^j)|; with probability ≥ 1 − (1 − ρ)^q, ‖g‖_∞ ≤ B := (M + C_m)/c + C_m, so
    min E₀ − B ≤ min(E₀ + g) and |ln Z(E₀ + g) − ln Z(E₀)| ≤ B: a valid finite bound for
    every g of the class, no hint, q = ⌈ln(1/δ)/ρ⌉ ≤ ⌈k^{m−1} ln(1/δ)⌉ evaluations whatever n.
    Explicit for the cube, m = 2: h = α + Σβ_i s_i (s = ±1), ‖h‖_∞ = |α| + Σ|β_i|; the largest
    of the n + 1 terms is ≥ ‖h‖_∞/(n+1); pairing s ↔ s with s_j flipped (or s ↔ −s for α) shows
    that at least half of the points have |h| ≥ that term: c = 1/(n+1), ρ = ½, q = ⌈log₂(1/δ)⌉
    (5 at δ = 0.05) against N_ball = n + 1.
    The sketch fails because the algorithm's bound may scale with the observed values;
    "the spread grows with the variance" does not prevent a valid finite bound.
    Under the other reading (accuracy fixed in advance) the count is plausible and unproved:
    conditionally on a transcript with fewer evaluations the target has atoms (the minimiser
    may lie where the unseen direction vanishes), so "probability of being right → 0" is not
    automatic.

* 03:22 — `r12_02_support.py` (brute force of the support lemma; dimension; unisolvence of the
  ball for every reference) started in the background, log `logs/r12_02_support.log`
  (budget: primal ≤ 2·10⁸ determinants, dual ≤ 6·10⁷ subsets per case; `timeout 1180`).
* 03:25 — `r12_03_randomised.py`: `logs/r12_03_randomised.log`, 20.7 s, last line `R12_03_DONE`.
  - Part 1 (cube, m = 2): n = 8, 12, 16 (N_ball = 9, 13, 17; claimed bound (1 − δ)N_ball = 8.55,
    12.35, 16.15): q = 5 random evaluations; largest exact fraction of bad points over 1080–1288
    test functions 0.5000 (attained), hill-climbing adversary ≤ 0.36; so exact failure ≤ 2⁻⁵ =
    0.03125 ≤ δ = 0.05.  End-to-end at n = 12 with a random known part and a remainder |R| ≤ 0.7:
    the output was an invalid bound in 2 of 20 000 runs (allowed 5 %).
    ⇒ **Proposition 11.18e(b) as written is false** (reading: the task of (a) with failure
    probability δ): 5 evaluations against a claimed 12.35 at n = 12.
  - Part 2 (cube, m = 3, 4): least fraction of points with |h| ≥ c‖h‖_∞ over 400 functions =
    2⁻ᵈ exactly (attained by cylinders), c = 0.6/(N_ball(3n)^d); q = 11 (d = 2), 23 (d = 3)
    against N_ball = 56, 79, 176.
    Proof of the explicit constant (cube, any d): U* maximising |ĥ(U)|·K^{|U|}, K = 3n; on every
    sub-cube over the coordinates of U* the top Walsh coefficient is ĥ(U*) + Σ_{V ⊋ U*} ±ĥ(V) with
    |Σ| ≤ |ĥ(U*)|((1 + 1/K)^n − 1) ≤ 0.4|ĥ(U*)|, and it is an average of ±h over the 2^{|U*|}
    points of the sub-cube, so one of them has |h| ≥ 0.6|ĥ(U*)| ≥ 0.6‖h‖_∞/(N_ball K^d).
  - Part 3 (c): N = ⌈k^{m−1} ln(1/δ)⌉ uniform samples miss a cylinder with probability
    0.0156–0.0452 ≤ 0.05 (exact and simulated, k = 2, 3, 4, m = 2, 3).
* 03:26 — item 5.  `diff` of our `experiments/science/ws_K/KineticsCertificates.lean` (639 lines,
  SHA-256 `fc9c7f28e5ad5fec806c8d80…`, the same at `25626db`, `a841cb4` and HEAD) against their
  `proofs/Frontiers/KineticsCertificates.lean` (612 lines): exactly two hunks — lines 32–33 (the
  sentence that the file is not part of the library, and the check command) replaced by a
  nine-line provenance paragraph; lines 606–639 (blank line, heading, 32 `#print axioms`) removed.
  Nothing else.  `proofs/CertificateAlgebra.lean` is identical in the two trees.
  Read `BarrierCertificate.lean` in full (1234 lines).
  - Our texts: SK_REPORT §2.5 ("two boxes D, D′ are adjacent iff #{i : D_i ∩ D′_i = ∅} ≤ 1"),
    §7 T1 ("two boxes contain a pair of configurations that differ in at most one site iff at
    most one coordinate has disjoint domains"), SCI-MSG-0005 §5 and §7 K-T1 (same).  The
    coordinator has already put a head note on SCI-MSG-0005 and a linked correction in
    SCI-RES-0011 §4, which says that "whether anything else of ours used the false direction is
    being checked by the review workstream" — this one.
  - Did anything of ours use the false direction?  Checked: (1) soundness of §2.5 and §2.8 —
    uses "neighbours ⇒ criterion" only; (2) "the format is complete (full tree)" — leaves of the
    full tree are single configurations, non-empty, where the criterion is exact; (3) the cost
    O(ℓ²nk) — unaffected; (4) T11 (`t11_cut_size.py`) — grows boxes around enumerated wall
    points, never uses the criterion (no occurrence of "adjacen"/"disjoint" in it); (5) our Lean
    file contains no adjacency lemma (the tree checker was "specified, not formalised").
    ⇒ nothing of ours depended on it.  The practical effect of the literal criterion is a false
    REJECTION of a valid certificate that has an empty leaf (their `ferroEmptyLeaf_literal_rejected`,
    reproduced below).
* 03:28 — `r12_05_barrier.py`: `logs/r12_05_barrier.log`, 0.6 s, last line `R12_05_DONE`.
  - adjacency, all pairs of boxes with empty domains allowed, (n,k) ∈ {(1,1),(1,2),(1,3),(2,1),
    (2,2),(2,3),(3,2),(2,4),(4,2)}: "neighbours ⇒ criterion" never fails; "criterion ⇒ neighbours"
    fails 3, 7, 15, 6, 98, 1110, 1029, 10850, 9604 times and NEVER with both boxes non-empty; with
    the non-emptiness clause the equivalence holds in every pair.
  - ferro: barrier 111 ↔ 000 = 7/2.  maze: energy = closed form; E(0000) = E(1111) = 0; barrier 1;
    basin {0000, 1000, 1100}; their `mazeCut` accepted by my own implementation of the three
    checks (adjacency by enumerating moves) and its region is that basin; 1 + 1/1000 is rejected;
    all 15 boxes around 0000 not containing 1111 (and the 15 around 1111): best box-cut bound 0 =
    the trivial bound.  scan: 5/2 with nearest-state moves, 0 with unrestricted moves; `scanCut`
    accepted on the product graph and rejected on the Hamming graph.  ferroResidual: g = −|x|/4
    is in the class and gives height exactly 13/4.  Empty-leaf example: accepted with the clause
    and with the move-enumeration test, rejected with the literal criterion.
  - Wording: `Dom.adjacent_iff` needs n > 0 (`hn : 0 < n`); the report's (d) does not say so
    (for n = 0 `SingleSite` is false, `Adjacent` true).  Trivial.
* 03:31 — `r12_02_support.py` finished: `logs/r12_02_support.log`, 8 min 41 s wall, last line `R12_02_DONE`.
  - Part 1: 101 grid × order cases (24 grids with 2–5 sites and 2–4 states): the span has dimension
    N_ball = size of the ball, and the Hamming ball of radius m − 1 around EVERY reference is
    unisolvent (0 failures).  Unisolvent N-subsets in tiny cases: 58 of 70 ((2,2,2), d = 1), 8 of 8
    ((2,2,2), d = 2), 81 of 126 ((3,3), d = 1), 504 of 792 ((2,2,3), d = 1) — the ball is one of many.
  - Part 2: **128 grid × order cases done exhaustively, 0 refutations**: the least support of a
    non-zero function of order ≤ d is exactly s* = product of the n − d smallest alphabet sizes
    (fraction 1/(product of the d largest)).  Equal alphabets: fraction k^{−(m−1)} exactly, as the
    report says.  Unequal alphabets: in 20 cases the least fraction is strictly above
    k_max^{−(m−1)} (e.g. (2,2,3), d = 2: 1/6 against 1/9) — the report's bound read with k = the
    largest alphabet is valid and not tight; the right constant is 1/Π(m − 1 largest k_i).
    Largest cases: (2,3,3,3) d = 1 (22 957 480 hyperplane candidates, 270 s), (2,2,3,4) d = 1
    (10 737 573, 127 s), (2,2,2,2,3) d = 2 (10 737 573 principal minors, 70 s).
  - 17 cases NOT done (too large for the budget): d = 1 on (3,4,4), (4,4,4), (2,2,4,4), (2,3,3,4),
    (2,3,4,4); d = 1 and d = 2 on (2,4,4,4), (3,3,3,3), (3,3,3,4), (3,3,4,4), (3,4,4,4), (4,4,4,4).
    For these only the induction proof (above) stands.
* 03:33 — `r12_04_sandwich.py`: first run CRASHED in Part 4 (formatting `None` when Δ < ε makes
  the deterministic bracket sufficient) — own error, fixed in the script, re-run; the log of the
  crashed run was overwritten and is not cited.  `logs/r12_04_sandwich.log`, 18.4 s, last line
  `R12_04_DONE`.
  - (a) identity: relative error ≤ 4.2·10⁻¹⁶ on 200 random sandwiches; (b) rate and law exact.
  - E d/max d: ≤ 1 always; median 0.012 when the bracket is wide only where the lower model is
    rare (gain factor ~80), 0.19–0.50 otherwise.
  - (c) coverage of the Hoeffding bracket 1.0000 in 400 000 simulated runs; exact for two-level W:
    least 0.99175; estimator unbiased (≤ 2.5 standard errors); point estimates never outside
    [Z(m₊), Z(m₋)], but the UNCLIPPED bracket sticks out in 47 % of runs at N = 20: "never leaves
    the deterministic one" is true of the estimate, and of the bracket only after clipping.
  - arithmetic of the illustration: 7.576·10⁻⁴ (N = 50 000), 4.89·10⁻³ (N = 1200) — as reported.
  - **(d) is wrong for large Δ.**  By Hoeffding's Theorem 1 in KL form (valid for every
    [0,1]-valued W of given mean) the plug-in estimate needs N_KL ≈ ln(2/δ)(e^Δ − 1)²/(2e^Δ ε²)
    samples on EVERY member: N_KL/N_H = 0.948, 0.61, 0.37, 0.136, 0.050, 0.0068 at Δ = 0.0605,
    0.5, 1, 2, 3, 5 (≈ e^{−Δ}); exact failure on two-level members with N_KL samples ≤ 0.007.
    Two-point lower bound ≈ N_KL/9.  So the order "(e^Δ − 1)²/ε² is necessary" is false in its
    Δ-dependence; the worst-case order without a hint is (e^Δ − 1)²/(e^Δ ε²), and the hint is
    worth (1 − e^{−Δ})/ε, not (e^Δ − 1)/ε.  At P3's Δ = 0.0605: factor 0.95, no consequence.
* 03:36 — read `BoxRatio.lean` in full (359 lines); `r12_06_ratio.py`: `logs/r12_06_ratio.log`, 8.6 s,
  last line `R12_06_DONE`.
  - `ratio_core`: 0 violations in 111 300 random instances; re-derived as a two-vertex LP.
  - 252 cases (n = 8, 10; partition into two macrostates; three placements; ε ∈ {0.05, 0.2, 1}):
    0 violations of `ratio_detect_ge` (exact/formula ≥ 1.25), spot-check failure ≤ 0.0228 ≤ δ,
    k_Z ≤ k_ratio and τ*_Z ≤ τ*_ratio always (claim (3)); greedy floor OK in the 87 cases without
    a heavy single state.  In 130 of 252 cases the packing of ALL ratio-far alternatives exceeds
    the packing of the Lean alternatives (dips inside one macrostate).
  - at the floor of both macrostates: the display of (d), max_M a_M/ε, is 0 while bumps inside
    the macrostates force (1 − 2δ)·10, 40, 200 evaluations at ε = 0.2, 0.05, 0.01 — the defect the
    theory division has just removed from Theorem 11.110(e); (d) mentions it in a parenthesis,
    and `BoxRatio.lean` has no bump alternative (`logRatio_bumpAlt…` does not exist).
  - example of (3): 2979.96 and 0.10815 — as reported (2980, 0.11).
  - Lean reading: `ratio_detect_ge`, `ratio_spotCheck_correct` do NOT assume A, B disjoint (more
    general than the report); they need U_A, V_A, U_B, V_B > 0 (not in the report); the
    docstring of the file says "Corollary 11.113" (the report numbers it 11.114).
* 03:38 — item 7, `r12_07_harness_rerun.sh` (their code, read-only export, `python3 -I -B … --only "<ID> "`,
  full mode, seed 20261124): `logs/r12_07_harness_rerun.log`, last line `R12_07_DONE`, each block ≤ 2.1 s.
  All seven blocks `survived`, "ALL TESTS BEHAVE AS EXPECTED", exit 0.  Printed statistics:
  - XI.19: identities=14444, worst=9.77e-15, strictly_smaller=85, equal_binary=154, sandwiches=2796
    (report: "for 85 of the sets T" — comes out; note: constants are computed only for the shapes
    (3,2), (3,3), (4,2), (4,3), so all 85 are three-state grids; THY-RES-0010 §2 says "85 sets with
    three or four").
  - XI.20: cases=106, largest=65, thinnest=1 (the support bound attained by cylinders).  Their
    support test: per (shape, m) one cylinder and four random sparse integer combinations, equal
    alphabets only — not exhaustive; nothing on part (b).
  - XXIV.6: laws=1599, attained=1599; XXIV.7: cube_sharp=0.9995, cube_largest=0.7484;
    XXIV.8: alternatives=1775, extremal=800, closest=1.002, packings=4, widest_factor=0.5149;
    XXIV.9: bump_sets=36, near_floor=4, widest_factor=0.5058, centre_closest=1, members=1200,
    worst_failure=0.9942 (report/THY-RES: "0.994·δ" — comes out; my own sup is 0.9993·δ: theirs is the
    maximum over 1200 random members, mine a threshold search; both below 1); 544/1088/545 are
    asserted inside the block;  XXIV.10: sandwiches=200, runs=8000, misses=1, gain=0.04442.
  - SHA-256 of their harness: b09937abcbb4e96d…
* 03:39 — `r12_08_lean_boxclass.sh`: a copy of their `BoxClass.lean` (first 513 lines identical to the
  export; 12 `#print axioms` lines appended) compiled against OUR tree with `lake env lean`:
  exit 0, 31.6 s, every one of the 12 statements depends on `propext, Classical.choice, Quot.sound`
  only.  `logs/r12_08_lean_boxclass.log`, last line `R12_08_DONE`.
* 03:40 — item 6: read `AnchoredRemainder.lean` in full, P3_REPORT §2.0, §2.1, §2.5, SCI-MSG-0023 §2,
  and the three other places where the theory report describes P3's certificate (lines 1262–1277,
  9343–9361, 9846–9861).  Numbers quoted from SCI-MSG-0020 (3.5·10⁹ states, 87 441 evaluations,
  [518.2332, 518.2937], 5·10⁻³ with 50 000 samples, 6.3 against 0.022, 33 to 1 400 times) are in
  SCI-MSG-0020 as quoted.  87 441 = Σ_{j<5} C(20,j)2^j ✓.
  Findings (all minor): (i) attribution line names parts (a) and (c) as ours; (b) is the
  "Consequently" of P3's Proposition 1 and (d) is the site-penalty form of P3's Theorem 5/§2.4 (the
  Lean docstring does attribute the anchored-base-point observation to us); (ii) "with equality
  for the set of all sites" is not a Lean statement (trivial; tested in XI.19) although the
  theorem is labelled [V]; (iii) "for two states per site the two kinds of constants coincide"
  is [N]/trivial, not [V]; (iv) the remark on "after the last site of T" follows from the Lean
  theorem for the reversed order — fine; (v) the file has 17 declarations, the report's index and
  THY-RES-0010 count 16 (`mem_sitesBefore` not listed).
* 03:41 — `r12_07b_mutations.sh` (their mutation driver, groups XXIV and XI, TMPDIR inside this
  directory) started in the background.
* 03:49 — `r12_07b_mutations.sh` finished: `logs/r12_07b_mutations.log`, last line `R12_07B_DONE`;
  group XXIV 38.7 s: 41 mutations, 41 caught, 11 baselines as expected (the report says "with 41
  mutations"; `XXIV.9 M2`, the old statement with the dips alone, is caught); group XI 3 min 2 s:
  56 mutations, 56 caught, 21 baselines as expected (XI.19 M1–M4, XI.20 M1–M4 among them).
  The scratch directory `tmp_mutants/` was inside this workstream's directory and has been
  removed by the script; the `/tmp/metricchain-mutants-*` directories on this machine are older
  than my run (latest 03:23:58) and are not mine.
* 03:45–03:50 — `docs/science/workstreams/R12_REPORT.md` written (the file-writing tool accepted
  it): verdict table, findings (2 major, 10 minor, 0 critical) with replacement texts,
  re-derivations, replication tables, the barrier comparison, consequences for SCI-MSG-0020,
  six requests, how to re-run, not checked, own errors.
  Nothing uses 11.18e(b) elsewhere in their tree: `BLUEPRINT.md` Step 3b and `RESEARCH_LOG.md`
  quote the deterministic statement only (grep of `11.18e` in the export).
* Next (optional): machine-check my own small additions (one-sided sampler at U = 0; weighted
  mixture; the bump alternative for one macrostate) in a file of my own whose only project
  import is `proofs.Frontiers.QueryLowerBound`.
* 03:51–03:55 — `lean/R12Additions.lean` (my own; 505 lines; imports Mathlib only; namespace
  `ScienceR12`; their definitions and five of their lemmas copied with their proofs) and
  `r12_09_lean_additions.sh`: `lake env lean` exit 0, 9 s, no warning, no `sorry`
  (`logs/r12_09_lean_additions.log`, last line `R12_09_DONE`).  Seven statements, each on
  `propext, Classical.choice, Quot.sound`:
  `detect_ge_at_floor`, `detect_ge_at_ceiling` (m1), `detect_ge_weighted`, `weighted_opt` (m3),
  `logRatio_bumpAlt_lt`, `logRatio_bumpAlt_gt` (m5), `affine_half_large` (core of M1 on the cube).
  First compile succeeded; the second (after adding the cube lemma) gave three deprecation
  warnings for `push_neg`, replaced by `push Not`; the log cited is of the final file.
* 03:56 — while checking THY-RES-0010's "the bump term is in … the blueprint": `<EXP>/docs/BLUEPRINT.md`
  Step 4 still has (i) "The ceiling and the number of states do not enter" (rule 1), (ii) the
  lower-bound display "no algorithm of any kind does better than (1 − 2δ)·max(⌊…⌋, ⌊…⌋) — verified"
  WITHOUT the hypothesis that no single state is heavy (grep "single state|single point|no single"
  in BLUEPRINT.md: nothing) — false without it: all dip weight on one state and no bumps, one
  evaluation suffices; (iii) rule (5) "ratios of macrostate weights are not covered", as do the
  theory report §8 (line 1276) and §11.30 (line 9381–9383), next to Corollary 11.114.
  Added to the report as m11 (minor; outside the list we were asked to review).
  The README does not display the Θ formula (my first draft of m4 said it did — corrected
  before anything left this directory).
* 03:58 — `r12_01b_twostage.py` made to test its own printed sentence (count of cases with no heavy
  single state in which the one-stage N exceeds the bound: 0) and re-run: 1.9 s, same numbers,
  last line `R12_01B_DONE`.  The log now cited is of this re-run.
* 03:59 — `git status`/`git log` (read-only): the coordinator has committed twice since I began
  (`8ad0a24` snapshot of the running workstreams — it contains an earlier state of this NOTES.md —
  and `8fb67d3`); head is now `8fb67d3`.  I ran no state-changing git command.  Only files of
  mine: `experiments/science/ws_R12/**` and `docs/science/workstreams/R12_REPORT.md`.
  Every log contains its `R12_…_DONE` line once (checked with grep); the Python logs end with the
  three lines of `time` after it.
* 04:00 — our tree searched for other uses of the adjacency lemma (`grep -rIl 'disjoint domains…'`
  in docs/science, docs/collaboration, experiments/science): SK_REPORT, SCI-MSG-0005, SCI-RES-0011,
  our DEAD_ENDS (SD46) only; no implementation of the tree checker exists on our side.
  Observation added to the report §4: in OUR format (branch nodes only, the kernel's convention of
  one child per state of the current domain, full root box) every leaf box is non-empty, so the
  literal test would have been exact on our trees; empty leaves need their `split` node or a root
  box with an empty domain.  The lemma as stated (arbitrary boxes) is false all the same.
  Library lemmas used by `BarrierCertificate.lean` (`verify_sound`, `verify_sound_real`,
  `verifyR_sound_lower`, `ResidualClass`, `ResidualLowerClass`, `RProblem.Consistent`) read in
  `proofs/CertificateAlgebra.lean` (identical in both trees).
* 04:03 — `r12_02b_support_search.py` (falsification attempt on the 17 cases too large for the
  exhaustive search): `logs/r12_02b_support_search.log`, 1 min 20 s, last line `R12_02B_DONE`:
  4 858 700 candidates (random sparse integer combinations, hill climbing, sums/differences of two
  cylinders), no support below s*, s* attained in all 17.  [N], not a proof.
* Report updated: table of the seven Lean statements of 11.115 against the wording (§2.5);
  §3.7 (my Lean additions); m11 (stale sentences in BLUEPRINT.md §6.4 and the theory report).

## Final state (04:06) — everything is in `docs/science/workstreams/R12_REPORT.md`

All seven items of the brief were reached.  No background job of mine is running.

| item | verdict | kind of checking |
|---|---|---|
| 1 Theorem 11.110(e) corrected | holds as stated; also without its hypothesis (two-stage check, m2); Θ reading right for ε ≲ 1 only (m4); text omits U, V > 0 (m1) | review + replication + re-run (XXIV.9, mutations) + a copy of BoxClass.lean compiled here |
| 2 Proposition 11.18e | (a), dimension, unisolvence for every anchor, "any unisolvent set": hold; **(b) false as written (M1)**; (c) true, proved, exact in 128 exhaustive cases, sharp constant for unequal alphabets 1/Π(m−1 largest k_i) | review + replication + re-run (XI.20); core of M1 machine-checked (`affine_half_large`) |
| 3 Proposition 11.113 | (a)–(c) hold (bracket needs clipping, m7); **(d) wrong by e^Δ (M2)** | review + replication + re-run (XXIV.10) |
| 4 Corollary 11.114 | (a)–(c) hold; (d) display has the dip term only (m5); Lean slightly more general (m6) | review + replication + re-run (XXIV.8); BoxRatio.lean read only; the missing bump lemma machine-checked by me |
| 5 BarrierCertificate / 11.115 | sound statements; instances reproduced; our lemma false for empty boxes only; nothing of ours used it; copy of our file = ours up to the two listed changes | Lean read only; replication; diff |
| 6 Theorem 11.18d text | says what is machine-checked with three small exceptions; attribution of (b), (d) incomplete (m9) | read only + re-run (XI.19) |
| 7 harness | seven blocks survive; quoted numbers come out; 41 + 56 mutations caught | re-run |

Findings: 0 critical, 2 major (M1, M2), 11 minor (m1–m11).
Scripts and logs (all logs contain their `R12_…_DONE` line):
r12_01_box (15.6 s), r12_01b_twostage (1.9 s), r12_02_support (8 min 41 s), r12_02b_support_search
(1 min 20 s), r12_03_randomised (20.7 s), r12_04_sandwich (18.4 s), r12_05_barrier (0.6 s),
r12_06_ratio (8.6 s), r12_07_harness_rerun (8 s), r12_07b_mutations (39 s + 3 min 2 s),
r12_08_lean_boxclass (31.6 s), r12_09_lean_additions (9 s).
Lean files: `lean/BoxClass_copy_9408e33.lean` (their file + 12 `#print axioms`),
`lean/R12Additions.lean` (mine; 7 statements).

Not checked (see report §8): BoxRatio.lean and BarrierCertificate.lean not compiled here; 17 large
cases of the support lemma not exhaustive; 11.18e(b) under the prescribed-width reading neither
proved nor refuted; lower bound of M2 is a two-point sketch; 11.110(b) entropy count; Hoeffding's
Theorem 1 (KL form) quoted from memory; the mutations themselves not reviewed; no prior-art search.
* 04:08 — `r12_10_arithmetic.py` (`logs/r12_10_arithmetic.log`, 0.02 s, last line `R12_10_DONE`): the
  arithmetic quoted in the report in one place — L(3.7) = 1.4604, W(3.7, 0.036²) = 3.378·10⁻³,
  543.64 → 544 / 1088 / 545, n = 240.3 for Corollary 11.111, the "0.3 %" of XXIV.7 (deficits 0.047,
  0.071, 0.217 % at u = 0.05 for p = 1.5, 2, 4 — comes out), our sandwich (cost numbers ≤ 0.0624,
  0.0587; hinted spot check 150 (75 one-sided); lower bound 5.4; 7.576·10⁻⁴ and 4.89·10⁻³; ball 87 441),
  the example of 11.114(3) (2979.96, 0.10815).  First run printed "%%" in one label (cosmetic);
  fixed and re-run.
* 04:10 — last pass over the report: tables checked for consistent column counts; the pipe inside a
  table cell of §3.5 removed; headline wording ("marked as a sketch or as quoted from memory");
  M1 "what remains" extended by the route a proof for prescribed width would take (probability of
  being right with j evaluations missing ≤ about 2^{−j} on the cube; one site: the packing bound
  (1 − 2δ)N_ball at a flat instance).  `git diff --stat d45ad56 HEAD` on the files I quote: only
  head notes were added to SCI-MSG-0005, SCI-MSG-0020, P3_REPORT (by the coordinator, 03:22 and
  earlier — before I read them); nothing under `proofs/` or `ws_K/` changed.
  Finished.  No process of mine is running.
