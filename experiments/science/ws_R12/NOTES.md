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
