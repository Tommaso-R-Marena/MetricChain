# R1 — Referee report on the mathematical content (git HEAD 477391f)

Independent referee; no part in the work. Scope: the mathematics as mathematics (definitions,
statements, paper proofs, cited results, novelty). Formal correctness of the Lean development was
taken as given; I read the Lean signature of every statement discussed. All numerical checks use my
own code (exact integer arithmetic for difference-constraint feasibility, LP cross-checks,
exhaustive enumeration); nothing from `experiments/` was reused. Statements of cited papers marked †
were checked against the paper text.

## 1. Summary of the submission

1. Setting: finite configuration space, energy `E₀ + Δ`; `E₀` explicit (pairwise); `Δ` known only
   through difference constraints `Δ(x) − Δ(y) ≤ d(x,y)` (`d` zero on the diagonal, triangle
   inequality, possibly asymmetric or negative) and through its values at evaluated points.
2. A-cluster: which `x` can / must minimise `E₀ + Δ` over that class (A1, A2; A3 with evaluations);
   the attainable values of `min(E₀+Δ)` and `Z_β` are exactly the interval spanned by the two
   McShane extensions (A4); a count of points that a certificate of a given form must evaluate (A5);
   bounded differences ⇒ site-additive envelope (A7); the single-site Goldstein test is exact and
   gauge invariant (A8).
3. D-cluster: the injection bound `Z(A) ≤ e^{−βγ} Z(S)` as a pruning rule (D1); the Jensen/McDiarmid
   sandwich for `ln(Z/Z₀)` under a product reference, its extremal residual, the Hoeffding fallback
   for arbitrary references (D2); Hölder (D5); monotone/Fubini bounds for voxel integrals (D4).
4. C-cluster: Lean proofs of Hoffman–Wielandt and of the s-stress lower bound of Sonthalia et al.
   (C1, C2); triangle-inequality holonomy bounds (C3); the optimal coaxial superposition after one
   torsion rotation and the resulting bounded-difference constants for an invariant Lipschitz
   residual (C4).
5. E-cluster: three Lean-verified checkers — (min,+) with LP-dual leaves, branch, DEE, `sum`; the
   same with a residual; (+,×) with a factorised leaf, branch, thermal prune (E1, D3) — and an
   exponential lower bound for sum-free certificates on disjoint frustrated triangles (E2).
6. The authors already label A8, D2(a–c,e), D5, C1–C3, E2 as known.
7. Every formal statement I read says what the report says it says. I found no false theorem and no
   degenerate definition that makes a headline statement vacuous.
8. Almost all of the mathematics is elementary (proofs of ≤ 5 lines) or a special case of classical
   duality. The A-cluster is the standard theory of systems of difference constraints / Lipschitz
   extension; its central "query-model" statement is in print for `E₀ ≡ 0`.
9. Several prose claims go beyond the theorems: the reading of the witness-size bound, the
   "negative answer" on dual reparameterisation, the novelty column for A1–A5, four [P]/[K] remarks.
10. The verified checkers are the substantive contribution. The (+,×) checker as specified is too
    weak for the stated application: exact `Z` of an `n`-site two-state chain needs `2ⁿ` leaves.

## 2. Verdict per result cluster

| # | verdict | justification |
|---|---|---|
| A1 | correct; trivial; known | Solvability of the difference-constraint system `{g_u − g_v ≤ d(u,v)} ∪ {g_x − g_y ≤ E₀(y) − E₀(x)}` ⇔ no negative cycle (Bellman–Ford; Rockafellar's feasible-differential theorem); `d` is its own shortest-path closure, so only the 2-cycles `x→y→x` matter. Same statement: the `c`-subdifferential of `E₀` at `x` is non-empty ⇔ `E₀(x) = E₀^{cc}(x)` for the cost `c = d` (abstract convexity: Dolecki–Kurcyusz, Pallaschke–Rolewicz, Rubinov; for a (quasi-)metric cost the `c`-concave functions are the `d`-Lipschitz ones). The witness `d(·,x)` is a column of the Kleene star, i.e. a tropical vertex of the polytrope `Adm(d)`. "Possibly optimal" in possibilistic optimisation (Inuiguchi–Sakawa). |
| A2 | correct; trivial; known | `sup_{g ∈ Adm(d)} [g(x) − g(y)] = d(x,y)` (tightness of the closed constraint matrix; the Kantorovich–Rubinstein extremal function `−d(x,·)`). Equivalent to the folklore "sharp minimum of modulus 1 ⇔ minimiser under every 1-Lipschitz perturbation" (Polyak 1979; Burke–Ferris 1993). "Necessarily optimal". |
| A3 | correct; corollary of A1; known for `E₀ ≡ 0` | Add a point `o` with `g(o) = 0` and put `d′(y,o) = U(y)`, `d′(o,y) = −L(y)`, `d′(y,z) = min(d(y,z), U(y) − L(z))`. `d′` is an envelope iff the data are consistent, the anchored class is the `d′`-admissible class normalised at `o`, and A1 for `d′` is exactly the two conditions of Theorem 2.6. For `E₀ ≡ 0`, symmetric `d`, this is Lemma 8 of Malherbe–Vayatis (ICML 2017)† ("potential maximizers": `x` is a maximiser of some consistent `k`-Lipschitz function ⇔ `min_i [f(X_i) + k‖x − X_i‖] ≥ max_i f(X_i)`). |
| A4 | correct; known + trivial | `L`, `U` are the McShane extensions (semi-Lipschitz extension for asymmetric `d`: Romaguera–Sanchis, Mustăţa) = the minimal-network intervals of a simple temporal network, with decomposability (Dechter–Meiri–Pearl 1991) = max-plus residuation. The bracket is monotonicity of `min` and `Z` (for `Z`: the density-bounded class of robust Bayes, DeRobertis–Hartigan). "Every intermediate value" = continuous image of a convex set; in optimal-recovery terms (Micchelli–Rivlin, Traub–Woźniakowski, Sukharev) the interval is the set of consistent values. Note: with several anchors `min(E₀+L)` is a min–max of pairwise models; the "lift at the cost of one modified instance per anchor" (§2.3) gives `max_a min_x`, which reaches the exact value only through branching. |
| A5 | Lean statement correct; elementary; gloss incorrectly stated (§3 item 1) | Three-line proof (the lower envelope can hide a dip of depth `(1−κ)σ` at an unevaluated point). Same looseness factor as Bachoc–Cesari–Gerchinovitz 2021, Thm 2† (`(1 − Lip f/L)^d` times a sum of packing numbers of near-optimal layers; their Prop. 3 shows failure at `κ = 1`), restricted to radii `< σ` where balls are singletons. No structure of the landscape is used; no upper bound. |
| A6 | correct; trivial | A1 for the discrete metric (interval uncertainty with common oscillation). |
| A7 | correct; standard | Bounded differences ⇔ Lipschitz for the site-additive quasi-metric (telescoping). |
| A8 | correct; known | As the authors say. The conclusion drawn from it is overstated (§3 item 3). |
| D1 | correct; trivial | Injection + positivity (Peierls). Plausibly new as an explicit pruning rule for `Z` in the K*/CFN literature; I did not search. The observable bound can be `2Bρ/(1+ρ)`. |
| D2 | correct; known | (a) Jensen, (b) Hoeffding, (c) McDiarmid's MGF bound, (e) sharpness of Hoeffding's lemma. (d) is the remark that the martingale proof bounds the MGF by the product of single-site suprema, attained by an additive function; the fixed-reference form is a corollary. The supremum formula of §3.2 is right (exhaustive vertex enumeration, §5). `(Σc_i)²` is Hoeffding with the range; the KL identity is the Gibbs variational identity. The Rio citation is accurate† (Lemma 4.1; `ℓ(t) = sup_r [ln(1 + r(e^t − 1)) − tr]`; `6ℓ(10) = 40.19`). |
| D3 | correct; weak rule set (§3 item 4) | Sound. Exact enclosure requires constant pair factors on every leaf box, i.e. enumeration. |
| D4 | correct; trivial | Monotonicity and additivity of the integral, Fubini. |
| D5 | correct; known | Hölder / weighted mini-bucket. |
| C1 | classical; formalisation | (The eigenvalue trace inequality for symmetric matrices is usually attributed to Ky Fan / Richter / Theobald; von Neumann's is for singular values.) |
| C2 | correct; known | Sonthalia et al. 2021: relaxation inequality + Prop. 1†; K-identity in Tsang–Pereira. Strictly weaker than Prop. 1 when `λ_r(Ĝ) < 0` (§3 item 9). |
| C3 | correct; known | Lerman–Shi 2022, Lemma 1†. The translation bound is the dead-reckoning triangle inequality. The abelian formula `hᵀ(CCᵀ)⁻¹h` is right. |
| C4 | correct; elementary | `min_ψ [2I_A(1−cos ψ) + 2I_B(1−cos(φ−ψ))] = 2S − 2|I_A + I_B e^{iφ}|`. It improves the trivial bound (superpose the heavier side exactly) by at most `√2` in RMSD. The chain rule is the triangle inequality of the Procrustes pseudo-metric; Cor. 4.7 is "invariant and Lipschitz ⇒ Lipschitz on the quotient". Probably not written down in this form; no depth. |
| B1 | infrastructure | Standard; only spot-checked (arctan brackets, circle atlas). |
| E1 | correct; engineering contribution | `consistent_iff_nonempty` is consistency of a simple temporal network (no negative cycle through the origin; the Hamming closure is already metric). `ResidualClass` / `ResidualIntervalClass` are the right classes (bounded differences are two-sided because quantified over all `x`). They constrain `Δ` on the whole product space, including states removed from the domains. |
| E2 | correct; known | Basu–Conforti–Di Summa–Jiang 2023, Thm 2.2† (`2^{m+1} − 2`); Jeroslow. Additions: DEE steps are covered; exact count `2^K`. Relative to pairwise-LP leaves, on a disconnected family (§3 item 12). |

Classification asked for by the editor. (a) Genuinely new mathematics: none with a non-trivial
proof; closest are the exact sum-free count including DEE steps (E2) and the closed form in C4.
(b) New formulations of known mathematics: A1–A7 (difference-constraint duality stated for a
white-box + black-box split), D1 (injection bound as a rule), D3/D4, C4, Cor. 4.7, E1.
(c) Rediscoveries: A3 (LIPO Lemma 8), A5 (BCG mechanism), A8, D2, D5, C1–C3, E2.

## 3. Errors and overstatements

No CRITICAL item: no machine-checked statement is false.

1. **MAJOR — §2.4 l.293–296, §7 item 1 (l.883–885), BLUEPRINT §6.2 (l.350) and §9 (l.550),
   RESEARCH_LOG ("any ε-certificate must evaluate…").** "The number of residual evaluations *any*
   certificate must contain is at least the number of states in the energy shell." False for
   certificates of an ε-optimal *configuration*. Counterexample: `X = {0,1}`, `d = 1`,
   `E₀ = (0, 5)`, `Δ ≡ 0`, `κ = 0`, `ε = 0`: the shell is `{0}`, yet Theorem 2.4 certifies `x = 0` for
   every admissible residual with zero evaluations. In 1 478 of 4 000 random instances some anchor
   set certifies a configuration while missing a shell state. What is proved (`anchor_necessary`)
   concerns one format: incumbent = best evaluated anchor, bound = McShane lower envelope.
   Fix — state what is true (both checked numerically, §5):
   (i) *value certificates*: if `min(E₀+U) − min(E₀+L) ≤ ε` then `A` contains every `y` with
   `(E₀+Δ)(y) − min(E₀+Δ) < (1−κ)σ − ε` (same three lines; no incumbent format needed);
   (ii) *configuration certificates* for `x̂`: `A` contains every `y ≠ x̂` with
   `E₀(y) − E₀(x̂) < d(x̂,y) − ε` **and** `(E₀+Δ)(y) − (E₀+Δ)(x̂) < (1−κ)σ − ε`; states separated by the
   white-box part alone cost nothing. The exact criterion is the anchored sharp-minimum condition
   `min(d(x̂,y), U(x̂) − L(y)) ≤ E₀(y) − E₀(x̂) + ε`, which the report never states.
   Also: the bound is only the first layer. The natural statement is a covering one —
   every `y` has an anchor with `(1−κ) d(a,y) ≤ gap(y) + ε` — and it has a converse (Q4, item 1).
2. **MAJOR — §0.2 novelty column A1–A5 (l.43–47), §2.3 prior-art paragraph (l.272–279),
   RESEARCH_LOG "No match found".** The search behind "not found in the literature" covered the
   DEE/CFN literature only (`prior_art/L1` §C2). A3 with `E₀ ≡ 0` is verbatim Malherbe–Vayatis 2017,
   Lemma 8†; A1, A2, A4 are the standard theory of difference constraints / McShane extension /
   `c`-conjugation / sharp minima / optimal recovery (table in Q3); A5 is the BCG21 mechanism†
   (cited by the authors, but as an analogy). Fix: cite these and reclassify A1–A5 as known in
   substance; "not found in the provable-design literature" is the defensible claim.
3. **MAJOR — §2.2 l.152–153, §0.2 row A8, DEAD_ENDS D1 title.** "Dual reparameterisation cannot
   improve dominance pruning for pairwise energies on product domains" and "negative answer to the
   seeded conjecture". Proved only for the single-site, context-independent (Goldstein) test.
   Multi-site improving maps verified through an LP dual (maximum persistency: Shekhovtsov 2014,
   which "subsumes simple Goldstein's DEE" — quoted in the authors' own `prior_art/L1` §C1 together
   with the caveat "the claim must not be read as 'the gauge does not help dominance-type
   pruning'") prune strictly more on pairwise product-domain models. Example: binary ferromagnetic
   chain, `n = 6`, `h_i = (0,1)`, `J = 3·[x_i ≠ x_{i+1}]`: no single-site test fires and the pair
   `(1,1)` is never pair-dominated, yet the map `x ↦ 0` is improving and is certified by one
   reparameterisation bound (LP value `0 = E(0…0)`); the term-wise test for this map fails in 200 of
   200 random gauges of the same energy function and holds in the right one. Fix: restrict the
   sentence to single-site fixed-substitution tests and list multi-site maps among the places
   where gauges matter.
4. **MAJOR (unstated limitation) — §0.1 item 3 (l.30), §3.4 "Kernel", §0.2 row D3, README status.**
   "Two semirings, parallel certificate rules." The tropical leaf carries a dual solution and is
   exact on trees; the (+,×) leaf replaces every pair factor by constants, and a thermal prune
   always widens the interval (`ρ > 0` for positive factors). Consequently an exact enclosure of
   `Z` for a two-state ferromagnetic chain needs every site fixed: `2ⁿ` leaves. Exhaustive search
   over all certificates with all three rules (`J = 1`): exact enclosure first at `8, 16, 32` leaves
   for `n = 3, 4, 5`; with half as many leaves the best ratio `hi/lo` is still `1.37, 1.22, 1.22`. The repository's own
   exact example uses an enumeration certificate (`enumZCert`). The pipeline "certified partition
   functions for chain molecules" therefore has no sub-exponential certificates in the verified
   kernel, while a transfer matrix computes `Z` in `O(nk²)`. Fix: say so in §3.4/§8; add a leaf with
   sum-product messages (exact on trees) or an elimination rule.
5. **MINOR — §2.3 l.239–240 and Lean docstring of `robust_minimizer_with_anchors_iff` ("no pruning
   rule using the same information can discard more").** Exact only for the notion "minimiser for
   no admissible residual". A value-preserving rule may discard more because of ties:
   `X = {x,y}`, `d = 1`, `E₀ = (0,1)`, with or without the anchor `Δ(x) = 0`: `y` satisfies both
   conditions (it ties for `g(y) − g(x) = −1`), yet `x` is a minimiser for every admissible `g`, so
   discarding `y` loses nothing. The kernel's own residual prune rule (margin
   `≥ c_i`, non-strict) removes such states. Fix: "up to ties" / "strictly".
6. **MINOR — §3.2 l.385–388 (T₁).** The Bobkov–Götze equivalence needs the bound for all `β`
   (`∀λ ∈ ℝ` in the Kontorovich–Raginsky statement of the theorem†, which is the authors' source).
   For a fixed `β` it is false: Bernoulli(0.02) with the discrete metric has T₁ constant `0.1233`,
   while the best constant at `β = 0.1, 1, 30` is `0.020, 0.028, 0.057`. For asymmetric envelopes
   the cost must be transposed (or both signs of `β` used); `W_{1,d}` is not symmetric then.
7. **MINOR — §3.4 l.494–497, BLUEPRINT §9 l.556.** "The exponent `d/2` cannot be improved in the
   Hessian-interval oracle model." The oracle model is not defined. The cited lower bounds
   (Bakhvalov; Holzmüller–Bach) are for point evaluations on `C²` balls; they give the exponent
   for the class "only `mI ⪯ ∇²E ⪯ MI` is known". An oracle returning Hessian enclosures on boxes
   is not a point oracle: for `C³` energies its widths shrink with the box and a third-order
   enclosure of the energy is available (`N ∼ ε^{−d/3}` voxels, at the price of non-separable
   Gaussian box integrals). In the proposed scheme second order is caused by the scalar
   sandwich / separable form (off-diagonal terms), not by information. Also "diagonal Hessian
   enclosure" is a scalar spectral enclosure, and the formula for `N` carries a factor `d^{d/2}`
   that the blueprint's `Θ(·)` drops. The Taylor step and the `N` formula themselves are right.
8. **MINOR — §3.6 l.514–518.** "Uniform racing stops once `2w(n) < gap`, i.e. within the factor
   `w⁻¹(g/2)/w⁻¹(g)` of the offline optimum." (i) "Offline optimum" is undefined. (ii) For two
   states, worst-case positions and convex `w`, separation requires `w(n₁)+w(n₂) ≤ g` and the
   cheapest allocation is the uniform one (Jensen): the ratio is 1, so `2^{d/2}` is an artefact of
   the lower bound `w⁻¹(g)`, not "the real obstacle". (iii) For `K > 2` states with unequal gaps,
   uniform refinement without elimination costs `K·w⁻¹(g_min/2)` against about `2·w⁻¹(g_min/2)`:
   ratio `≈ K/2`, unbounded. The stated factor is an upper bound for racing *with elimination*.
9. **MINOR — §8 l.931–932 and §4.1 attribution.** "Theorem 4.3 is … within `√((L+2)/2)` in general"
   needs the trace-shifted solution to be PSD (`λ_r + τ/(r+1) ≥ 0`). Counterexample (hollow,
   symmetric, as in the theorem's hypotheses): `D̂ = −2(11ᵀ − I)`, `L = 4`, `r = 3`: bound `5`, optimum
   `48`, ratio² `9.6 > 3`. For entrywise nonnegative `D̂` I found no violation (3 000 random
   instances) but there is no proof. When `λ_r(Ĝ) < 0` the report's bound is strictly weaker than
   Sonthalia et al., Prop. 1† (their `C₁`, `C₂` also count wrong-signed kept eigenvalues: `21`
   against `5` in the example), so "with the same constants" holds only for `λ_r(Ĝ) ≥ 0`. The Lean
   theorem can be strengthened by keeping `μ_k ≥ 0`.
10. **MINOR — BLUEPRINT §8.4 l.538.** `σ₃(X)` must be that of the *centred* coordinate matrix (the
    theory report says so, the blueprint does not). With an uncentred `X` the inequality fails
    (nearly planar molecule shifted along its normal: RMSD `0.0348` against a "bound" of `0.0076`).
    With centring the corollary is right (Tu et al., Lemma 5.4†; the composed constant is not
    attained, the Gram-step constant is).
11. **MINOR — §4.4 l.678–680, row C4.** The "naive lever-arm bound" used for the 2–2.5× comparison
    rotates the distal part regardless of weight. Against the obvious choice (superpose the heavier
    side) the exact coaxial cost gains at most `√2` in RMSD, since
    `C(φ) ≥ 4 I_red sin²(φ/2) ≥ 2 min(I_A,I_B) sin²(φ/2)`.
12. **MINOR — §6.3 title and §6.2.** "The decomposition rule is necessary" is relative to
    pairwise-LP leaves: a triplet-consistency leaf certifies `m` triangles in one leaf, and the hard
    family is disconnected. §6.2 l.820: the witness is `O(k)` messages per ordered pair (`n²k`
    rationals per leaf in the format used), not "`O(nk)` messages per neighbour pair".
13. **MINOR — small items.** Theorem 2.4 is stated without proof (two lines). §4.3 l.639 "open":
    the two-sided spectral bound of Bandeira–Singer–Spielman and SDP dual certificates should be
    named in the text, not only in `prior_art/L3`. Docstring of `robust_partition_interval_exact`
    says "any β"; for `β < 0` the hypothesis interval is degenerate and the true range is the
    reversed interval (the report's text is right). Row A5: "structured discrete landscapes" — no
    structure is used.

## 4. Answers to the editor's questions

**Q1. Is anything false, or stated more strongly than proved?** No machine-checked statement is
false, and the paper proofs of Theorems 2.3–2.7, 3.1, 4.2, 4.6, 6.1 are correct (2.4 lacks a proof;
the proof idea of 6.1(c) is complete, including the DEE and good-domain steps). False or overstated
as written: items 1–4 (major) and 5–13 (minor) above, each with a counterexample or the missing
hypothesis. Of the [P]/[K] statements the editor listed: supremum formula §3.2 — correct; Rio's
function — correct; T₁ equivalence — needs `∀β` (item 6); coNP-hardness §2.2 — correct (the decision
problem is coNP-complete; cf. Lecoutre et al. 2012 as quoted in `prior_art/L1`); second-order voxels — Taylor step and
count correct, optimality claim not established (item 7); racing — item 8; Sonthalia — accurate for
`λ_r ≥ 0` (item 9); Procrustes–Gram — correct with centring (item 10); Hodge — correct.

**Q2. What is publication-worthy?** As mathematics: none as it stands. Every new statement has a
proof of a few lines and sits inside a classical theory (Q3); the one result with the shape of a
theorem about certificates (A5) is a first-layer special case of a published bound, without a
converse. Possible routes:
- *Formalisation / verified-checker paper* (CPP, ITP, JAR; or a CP/SAT-style tool track): E1, E2,
  the Hoffman–Wielandt and s-stress formalisations. Needed: a certificate producer and experiments
  at realistic sizes; a compiled checker with a refinement proof (kernel evaluation by
  `decide +kernel` will not scale); a measured comparison with pseudo-Boolean encodings checked by
  VeriPB/CakePB; a (+,×) kernel complete on trees (item 4).
- *Computational protein-design methods paper* (RECOMB, JCTC, J. Comput. Biol.): the envelope
  interface, thermal DEE, voxel-integral enclosures. Needed: implementation against OSPREY or
  toulbar2 on real design instances; certified constants `c_i` for at least one real residual
  (truncated many-body remainder, rounding residual, or a small network); comparison with `p*` and
  `Z*_ε`. All experiments so far are synthetic and tiny.
- *Optimisation / learning-theory venue*: only with an actual theorem in the A-cluster — matching
  upper and lower bounds on certificate size (Q4, item 1) or a complexity classification of the
  exact criteria.
- D2 would support a short note only with sharp results for dependent references. C4: no.

**Q3. Is there a deeper known theory behind §2.3–2.4?** Yes: `Adm(d)` is the solution set of a
closed system of difference constraints (the Lipschitz polytope of a finite quasi-metric space, a
polytrope), and §2.3–2.4 are linear-programming duality on it.

| result | follows from |
|---|---|
| Thm 2.3 (A1) | no-negative-cycle criterion for difference constraints (Bellman–Ford; Rockafellar, feasible differential theorem); equivalently `∂^c E₀(x) ≠ ∅ ⇔ E₀(x) = E₀^{cc}(x)` with `c = d` |
| Thm 2.4 (A2) | tightness of the shortest-path closure, `max_{Adm(d)} (g(x) − g(y)) = d(x,y)` (Kantorovich–Rubinstein extremal function); sharp-minimum stability |
| Thm 2.5 (A4), bracket | McShane 1934 / semi-Lipschitz extension; minimal network of a simple temporal network and its decomposability (Dechter–Meiri–Pearl); max-plus residuation |
| Thm 2.5, exactness | convexity of the consistent set + continuity (optimal recovery: Micchelli–Rivlin, Traub–Woźniakowski; Sukharev and Piyavskii–Shubert for Lipschitz classes) |
| Thm 2.6 (A3) | Thm 2.3 on the one-point extension `(X ∪ {o}, d′)`; for `E₀ ≡ 0`: Malherbe–Vayatis 2017, Lemma 8 |
| energy window (A6) | Thm 2.3 for the discrete metric; possibly-optimal test under interval uncertainty |
| differential DEE, A7 | bounded differences ⇔ Lipschitz for the weighted Hamming quasi-metric |
| Thm 2.7 (A5) | Bachoc–Cesari–Gerchinovitz 2021, Thm 2 (the `(1 − Lip f/L)` adversary), finest scale only; the notion of minimal certificate goes back to Danilin 1971 and Hansen–Jaumard–Lu 1991 in dimension one; the layered packing sums are those of the zooming / near-optimality dimension (Kleinberg–Slivkins–Upfal; Munos) |
| `consistent_iff_nonempty` (E1) | consistency of a simple temporal network with interval domains |

What is left that does not follow: nothing mathematical. What remains is the formulation — a known
additive part `E₀` next to the Lipschitz class, which produces the contact condition and makes
white-box-sharp states free — and the machine-checked statements.

**Q4. Three most valuable directions.**
1. *Certificate complexity with matching bounds.* Replace Theorem 2.7 by the covering statement
   and its converse (both verified numerically, §5): for value certificates, necessary — every `y`
   has an anchor with `(1−κ) d(a,y) ≤ gap(y) + ε`; sufficient — `A` contains a minimiser and every
   `y` has an anchor with `κ d(y,a) + d(a,y) ≤ gap(y) + ε`; for `κ = 0`, `ε < σ` the two coincide, so
   minimal certificates are exactly minimum hitting sets of the balls `B(y, gap(y) + ε)`. Then
   (i) evaluate this hitting number for weighted Hamming envelopes in terms of the density of
   states (the discrete analogue of BCG's `S_C`); (ii) prove a competitive bound for the adaptive
   procedure of BLUEPRINT §6.2; (iii) treat configuration certificates, where white-box-sharp
   states are free; (iv) classify the criteria themselves for pairwise `E₀` and site-additive `d`:
   conformation-level membership is a pairwise minimisation (polynomial on chains), the
   rotamer-level question "is state `r` of site `i` possibly optimal" is `∃x∀y` — is it `Σ₂ᵖ`-hard,
   and is it polynomial on chains?
2. *Free energy beyond product references.* The natural reference for a chain is a Markov
   (transfer-matrix) measure, for which the report has only `(Σc_i)²`. Targets: the exact supremum
   of the Jensen gap over the bounded-difference class for a Markov reference (is the extremal
   residual still additive; what replaces Rio's `ℓ`); Wasserstein-matrix constants `‖Γc‖²` with `Γ`
   computed by dynamic programming, with a matching lower bound; a variance-sensitive sandwich
   (`β² Var₀(Δ)/2` plus an envelope-controlled remainder, variances computed exactly); cell-wise
   localisation against extensivity.
3. *Proof complexity where it is not known, and a (+,×) system that deserves the parallel.*
   Lower bounds for connected families (triangles coupled weakly along a chain) for sum-free
   certificates and for decomposition-aware (AND/OR, tree-decomposition) certificates, in terms of
   the frustration crossing separators; a partition kernel with a message-passing or elimination
   rule, with soundness and the separation from the present kernel (the `2ⁿ` chain bound of item 4
   is the easy half); comparison with the MICE/CPOG proof systems for model counting.

## 5. Independent numerical checks (own code, not in the repository)

- A1, A2: 20 662 (instance, `x`) pairs each, `|X| ≤ 6`; envelopes: asymmetric with negative entries,
  metrics, discrete, zero, potential type `d = h(x) − h(y)`, one-sided; ties; integer data; exact
  negative-cycle test plus LP cross-check. 0 mismatches (10 749 / 5 220 positive cases).
- A3: 16 599 pairs (7 604 positive), 0 mismatches. A4: 505 instances — pointwise extremes equal
  `L`, `U` (LP), `max_g min_S = min_S(E₀+U)`, intermediate values on the segment, `Z` bracket for
  `β ∈ {0, 0.3, 1, 2.5}` and its reversal for `β < 0`: 0 failures. A6: 3 000 instances; A7: 122 890
  pairs: 0 violations.
- A5: 96 316 anchor sets, 38 359 certificates in the Lean sense: 0 violations of
  `anchor_necessary` / `anchor_card_lower_bound`. Value-certificate variant: 39 146 certificates, 0
  violations. Configuration certificates missing a shell state: 1 478 of 4 000 instances; corrected
  statement of item 1(ii): 66 386 certificates (1 721 with no anchor), 0 violations. Covering
  characterisation of Q4.1: necessity 49 487, sufficiency 41 535, exact case 40 072 — 0 violations.
- Interval consistency (E1): 20 000 instances, `n ≤ 3`, `k ≤ 3`, with negative and zero constants,
  `k = 1`, duplicate anchors, missing upper values, no anchors: 0 mismatches (7 733 non-empty).
- D2: product reference, 33 990 cases (including `β ∈ {0, −1.5}`, `c = 0`, one-state sites, zero-mass
  states): no violation of `0 ≤ gap ≤ β²Σc_i²/8` nor of the supremum formula; exhaustive
  enumeration of all 24 552 vertices of small bounded-difference polytopes: maximum equals the
  formula to `4·10⁻¹⁴`. Arbitrary reference, 45 000 cases: `(Σc_i)²` never violated, `Σc_i²` violated
  1 681 times; the report's counterexample reproduced (`ln cosh 1 = 0.4338`).
- Coaxial cost: 20 000 parameter sets including `I = 0`, `I_A = I_B`, `φ ∈ {0, π, 2π}`: closed form
  equals the numerical minimum to `2·10⁻¹⁴`; two-sided bounds hold; 3 000 three-dimensional
  torsion moves: Kabsch cost ≤ coaxial cost (ratio 0–0.998).
- s-stress: Theorem 4.2 on 20 000 random pairs; Theorem 4.3 on 400 inputs (`L` from 1, `r` from 0,
  negative entries, random and optimised `Y`): no violation; simplex `L = 5`, `r = 3`: `1.25` against
  `1.3043`; bias ratios `1.414, 2, 2.828, 4`; singular values of `K`: `2, √(2L), 2√L` with
  multiplicities `L(L−3)/2, L−1, 1`.
- Certificate counts: exhaustive dynamic programme over all boxes; minimum number of leaves of a
  sum-free certificate for the bound `K` is `2^K` for all `K ≤ m ≤ 3` (and `m = K = 4`), with and
  without the prune rule; leaf values from the local-polytope LP, validated against the literal
  leaf rule; the peel certificate with `sum` visits `2m` leaves and passes every check.
- Partition kernel on a two-state ferromagnetic chain (item 4): Pareto-optimal enclosures per
  (box, leaf budget) with leaf, branch and thermal prune, `n ≤ 5`; leaf and branch only, `n ≤ 6`.
- Also: transport, `m`-to-one and observable bounds, Goldstein exactness / gauge invariance /
  Desmet at the optimal gauge, block separability, the 3-body reduction, Hölder, separable voxel
  bounds in 2-D, Tu et al. Lemma 5.4 (adversarial maximisation reaches ratio `1.0000`), the
  corollary of §4.2, dRMSD ≤ √2·RMSD, holonomy bounds, the abelian Hodge formula: no violation.
  The examples of items 3, 5, 6, 9, 10 were computed, not only argued.

## 6. Not checked

- The Lean build and the axiom audit (taken as given); `Core/Rounding.lean` and the chart-arc
  brackets of `VoxelBridge.lean` beyond two spot checks; the JSON reference checker and its
  conformance vectors; measurability side conditions in D4.
- Benchmark numbers B1, B2, B5–B7 and the `36.1` of B4 (the B3 ratios, the B4 values `40.2` and
  `75`, the simplex values and the `Z` of the triangle were reproduced).
- Cited results I did not read: Kontorovich–Ramanan / Kontorovich–Raginsky constants for dependent
  references, Holzmüller–Bach Thm 7, Tseng–Kirkpatrick, Shekhovtsov's theorems (I rely on the
  quotations in `prior_art/L1` and on classical roof duality), LuCore et al., iMinDEE, Gourgoulias
  et al., Popov–Grudinin; Deng et al. only by a text search.
- The "no match found" claims for D1, D3, D4, C4, E1: I did not search; my novelty judgement there
  rests on the statements being elementary.
- Untracked files that appeared in the working tree during the review (`docs/prior_art/L4_*.md`,
  `docs/prior_art/L5_*.md`, `proofs/Frontiers/CertificateComplexity.lean`,
  `proofs/Frontiers/CertificationGeometry.lean`) are not part of HEAD 477391f and were not read.

Sources checked online: [Malherbe & Vayatis, arXiv:1703.02628](https://ar5iv.labs.arxiv.org/html/1703.02628);
[Bachoc, Cesari & Gerchinovitz, arXiv:2102.01977](https://ar5iv.labs.arxiv.org/html/2102.01977).
