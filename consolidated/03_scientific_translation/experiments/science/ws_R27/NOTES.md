# Workstream R27 — notes (kept from the first minute)

Internal review by an AI agent (not external peer review).  Object: Geometry division's Theorem L
(threshold-free form), Lemmas P and Q, Corollaries L.1–L.3, Theorem L⁺; read-only copies in
`/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/geo_ro_9f164f9/`.

Times are read from the clock (`date -u`) at the moment of writing.

## Log

* 2026-11-26T22:46:24Z — started.  Read COMMON.md and R27_brief.md in full.  Created this directory.
  Read-only copies present: GEOMETRY-RES-0007.md (10015 B), LOCAL_DATA_STABILITY.md (41812 B),
  PRIOR_ART.md (24741 B).  Machine: 4 cores, 15 GB, Python 3.13.18.
* 2026-11-26T22:52Z (clock read below when appended) — read in full: LOCAL_DATA_STABILITY.md (562 lines, all of it), GEOMETRY-RES-0007.md,
  SCI-REV-0023.md §5–§6 (l.126–225), experiments/science/geometry_checks/theorem_l_threshold.py.  PRIOR_ART.md not yet read.

## Review by hand (first pass, before any code) — kind of checking: REVIEW (re-derived)

**Lemma P.**  Re-derived line by line.  (a) optimal R = polar factor of XᵀU ⇒ after X ← XR, XᵀU sym. PSD ✓.
(b) expansion: with M = XΔᵀ+ΔXᵀ+ΔΔᵀ, tr M² has nine terms: 2 tr(XᵀX A) + 2 tr B² + 4 tr(AB) + tr A² ✓ (uses B symmetric).
(c) tr(A+√2B)² ≥ 0 ⇒ bracket ≥ (4−2√2) tr(AB); tr(A(B+XᵀX)) = tr(A·XᵀU) ≥ 0 ⇒ tr(AB) ≥ −tr(A XᵀX) ✓.
(d) total ≥ (2√2−2) tr(XᵀX A) ≥ 2(√2−1) σ_r² ‖Δ‖² ✓.  No hypothesis on U; X of full column rank is needed only for σ_r > 0.
Equality cases (mine): p = bottom right singular vector of X, U = X − Xppᵀ + w⊥pᵀ with w⊥ ⟂ col(X), |w⊥|² = (√2−1)σ_r².
For r = 1: u ⟂ x, |u|² = (√2−1)|x|² gives equality ⇒ the constant 2(√2−1) is sharp (needs m ≥ r+1).  To be confirmed by code.

**Lemma Q.**  ‖E‖_F = √2 e (each pair twice), ‖−½JEJ‖_F ≤ ½‖E‖_F = e/√2 ✓; Lemma P with U = JY_S, X = JX_S (m×3, σ_3 = s) gives
‖JY_S − JX_S R‖ ≤ (e/√2)/√(2(√2−1)) /s = e/(2√(√2−1) s); κ = 0.776887… < 0.777 ✓.  t = c_Y − c_X R.  R ∈ O(3): improper allowed, needed
(mirror image has e = 0).  Lemma Q cannot be *exactly* sharp through the equality case of P: ‖JEJ‖=‖E‖ needs diag(G_Y)=diag(G_X), which
forces (Xp)_i² = (w⊥)_i² for all i, impossible since the norms are σ² and (√2−1)σ².  (To measure the sup numerically.)
Their sharpness sentence: "window moves by 2 min(h⁻,h⁺) up to a rigid motion" is an UPPER bound for d_P of the window; "s ≤ √2 max(h⁻,h⁺)"
gives bound ≥ 2.2 min(h) — that is consistency, not sharpness.  Sharpness up to a constant needs s ≳ max(h⁻,h⁺) (false if the middle
triangle is thin) and d_P ≳ min(h⁻,h⁺).  To test (Item 1 (iii)).

**Theorem L, Step 1** ✓ (s_i ≥ max(τ_i, τ_{i+1}): monotonicity of σ_3² in S re-derived: centroid minimises the sum of squares).
**Step 2** ✓: on the four shared rows the two representations of Y_W are equal exactly; centring: (X_W − 1c_W)(R_j − R_{j+1}) = J(ε_{j+1} − ε_j)|_W;
‖MN‖_F ≥ σ_min(M)‖N‖_F for M of full column rank; τ_{j+1} = σ_3 of the centred FOUR-point window {j+1..j+4} (the shared one) ✓.  No use
of determinants: correct as linear algebra for every τ_{j+1} > 0 (if det differ then ‖R_j − R_{j+1}‖_F ≥ 2 and the inequality says the data
errors are at least 2τ_{j+1}).  m_j = mean_W ε_j − mean_W ε_{j+1}, |mean of 4 vectors| ≤ ½ Frobenius ✓.
**Step 3** ✓ (telescoping identity re-derived; i(k) = min(k, n−4) ⇒ k ∈ F_{i(k)}).  NOTE: (local) uses only τ_2 … τ_{n−4} (the interior
four-point windows) and s_1 … s_{n−4}: the end windows W_1, W_{n−3} need not be non-degenerate.
**Step 4** ✓: |x_k − c_{j+1}| ≤ b(k−j+½) (equality possible only for k = j+1; for k ≥ j+4 the true value is ≤ b(k−j−5/2));
pair of separation s lies in 5−s ≤ 4 windows ✓; Σ(δ_j+δ_{j+1})² ≤ 4Σδ_j² ≤ 16κ²‖η‖²/s_*² ✓; Σ_{u<k}(u+½)² ≤ (k+½)³/3 ✓;
Σ_k (k+½)³ ≤ (n+3/2)⁴/4 ✓; (2√k+1)² ≤ 9k ✓; τ_* ≤ √(5/3) b = 1.291 b ✓.  Minkowski: κ[(2/√3) + (3/√2)(n+½)·1.291/(n+3/2)²] ≤ κ(1.1547+0.3566)
at n = 5 → 1.174 ≤ 1.18 ✓; 1.18(n+3/2)² ≤ 1.2(n+2)² ✓.
**Cor. L.1** ✓ (η(Ŷ) = r + ε, ‖η‖ ≤ 2‖ε‖).  **Cor. L.2** ✓ as a deduction (roles swapped; d_P symmetric); needs ν = bound on the ℓ² norm of
the errors of the SQUARED distances, complete data of separation ≤ 4, an X in ℝ³ that exists; nothing circular.  "only because no smallness
condition" is an overstatement (a threshold in terms of the reference = the estimate could be verified from r and a sup bound on the noise).
**Cor. L.3** (a) ✓ given Theorem K(c) (K(c) re-derived too: test field, 8-dim space, Courant–Fischer; 14π² = 138.2 ≤ 139);
(b) ✓: for V ⟂ trivial motions, d_P(X, X+tV) = t‖V‖ + O(t²), ‖η‖ = 2t‖AV‖ + O(t²) ⇒ ‖V‖ ≤ 2C_L‖AV‖ ⇒ ker A = trivial motions and μ ≥ 1/(2C_L).
**Thm L⁺** ✓: η = 2A_{X′}V + Q(V) exact; ‖Q‖₂ ≤ ‖Q‖₁ = Vᵀ(L⊗I)V ≤ Λv²; φ(v) = 2μv − Λv² increasing on [0, μ/Λ], φ ≥ μv there; Theorem L puts v
in [0, μ/Λ].  Λ: symbol 8 − 2Σcos sθ, max near θ ≈ 57.5°, ≈ 11.039 by hand (to compute).  The "if ‖η‖ ≤ μ²/Λ" clause is needed because a valid
C_L may lie in [1/(2μ), 1/μ).
**Observation (mine, to test):** at an X with an interior four-point window exactly coplanar the framework is still infinitesimally rigid
(μ > 0: two rigid bodies sharing 4 coplanar non-collinear points have no relative infinitesimal motion) but not globally rigid (reflection of
one side in that plane keeps all data).  So near such X: 1/(2μ) stays bounded while sup_Y d_P/‖η‖ ≥ d_P(reflection)/(4h⁻h⁺) → ∞ like 1/τ.
Consequences: (i) the factor 1/τ of Theorem L is necessary in kind; (ii) a Y with ‖η‖ ≤ μ²/Λ and d_P ≫ ‖η‖/μ exists there: the range of
Theorem L⁺ cannot be replaced by ‖η‖ ≤ μ²/Λ — a control "just outside the hypotheses".
**Observation (mine):** the theorem needs Y in ℝ³.  For Y in ℝ⁴ (e.g. an SDP/MDS output before projection) the linear bound is false:
5 points, y_i = (x_i, εw_i), w the affine dependency: η = O(ε²), d_P ~ ε.

## Code and runs (REPLICATION: own code written from the statements; their scripts not available)

Files: `r27lib.py` (definitions), `thmL_steps.py` (every inequality of Steps 1–4 for one pair), `item2_battery.py`, `item1_lemmas.py`,
`item2_adv_fixedX.py`, `item2_adv_joint.py`, `diag_ptratio.py`.

* 22:58–22:59Z `item2_battery_run1.log` (complete, last line ALL DONE): 12 427 pairs (X, Y), 0 violations of any claimed inequality; identities
  of Steps 2–3 hold to 3·10⁻¹⁵; max ratios: Lemma Q 0.736; Step 2b 0.540; (local) per point 0.535; d_P/‖local‖₂ 0.279; d_P/uniform 0.00546.
  Controls: C1 (sep-4 errors left out) violated by 2004 pairs (reflections) ✓; uniform/1000: 468 ✓, /100 and /10: 0 (so the control
  "constant divided by a large factor" fails from 1000 on); C3 κ→½: 5; C4 proper rotations only: 2954; C5 s_j in place of τ_{j+1}: 240;
  C6 "three windows": 81; C7 no lever arm: 2092; C8 local/10: 1704.  (The last summary line of that log says "False" because /10 and /100
  did not fail; to be reworded in a later run.)
* 23:01–23:06Z `item1_lemmas_run1.log` (complete): Lemma P 22 000 pairs, 0 violations, max ratio 1.000000; equality family (mine) attains
  the constant to 5·10⁻¹³ for every X with m ≥ r+1 ⇒ Lemma P is sharp; for m = r the sup is 0.8284 = 2(√2−1).  Control (factor √2−1 dropped):
  violated by 4472 pairs ✓.  Lemma Q: 12 000 windows, 0 violations; sup over (X_S, Y_S): |S|=4: 0.808, |S|=5: 0.971, |S|=6: 0.971 ⇒ κ cannot
  be improved by more than 3 % for five-point windows.  Controls: κ→½ 635 ✓; proper only 1332 ✓; σ₂ for σ₃ 987 ✓.
  Reflection example (Item 1 (iii)): exactly one squared distance changes by 4h⁻h⁺ ✓ (asserted); d_P(window) = 0.26–0.89 × 2min|h| (their
  "moves by 2 min(h⁻,h⁺)" is an upper bound); d_P/bound: helix-like 0.55; strand-like 0.21–0.24; double tetrahedron 0.50; random five-point
  chains 0.02–0.63 (median 0.22); thin middle triangle 0.034, 0.0034, 0.0003 (→ 0).  So the reflection attains the lemma up to a factor 2–5 on
  helix/strand windows and NOT uniformly; but sup_Y of the ratio on a fixed window is ≥ 0.73 on every window tried (collapse of the thin
  direction) — Lemma Q is sharp up to a constant on every window, through a different example.
* 23:08Z `item2_adv_fixedX_run1.log`, `item2_adv_joint_run1.log`: STOPPED BY ME (not complete; not to be cited).  **Own error**: the
  per-point ratio dist_k/local_k was formed with no noise floor; for a reflected tail the points before the reflection have local_k = 0
  exactly and dist_k ~ 1e-15, which printed ratios 1.9, 23, 2e15 and "violations".  `diag_ptratio.py` (23:10Z) shows dist ≤ 4.5e-15 against
  local = 0.0 at exactly those points, and the checker with the floor has 0 violations there.  Fixed (floor 1e-7·diam; a point farther than
  1e-9·diam with a bound below the floor is still counted as a violation); rerun as `_run2` started 23:11:30Z.

## Web log (network used only for Lemma P's source so far; nothing of this project in any query)

| # | time (UTC) | address / query | what it gave | reading level |
|---|---|---|---|---|
| W1 | 23:12 | https://arxiv.org/abs/1507.03566 (WebFetch) | record: Tu, Boczar, Simchowitz, Soltanolkotabi, Recht, "Low-rank Solutions of Linear Matrix Equations via Procrustes Flow"; v1 13 Jul 2015, v2 5 Feb 2016; no journal reference on the page | record only |
| W2 | 23:12 | https://arxiv.org/pdf/1507.03566v2 (curl; PDF 23 pages, saved outside the repository in the session scratch directory `…/scratchpad/r27_dl/tu_procrustes_flow_v2/`; text by pdftotext; pages 9, 20, 21 rendered and read as images) | **Lemma 5.4** (p. 9): "For any U, X ∈ ℝ^{n×r}, we have dist²(U, X) ≤ 1/(2(√2−1)σ_r²(X)) ‖UUᵀ − XXᵀ‖_F²", dist defined in (3.1) as min over R with RᵀR = I_r of ‖U − XR‖_F; followed by "We would like to point out that the dependence on σ_r²(X) in the lemma above is unavoidable."  Proof: Appendix A (pp. 20–21): H = U − XR, wlog R = I, UᵀX ⪰ 0, HᵀX symmetric; completes the square Tr((HᵀH + √2HᵀX)²) — the same argument as the note's.  A slip in the source's proof: it says "(A.1) holds with η = 1/(2(√2−1)σ_r²(X))"; for (A.1) and for its last line (XᵀX ⪰ η/(2(√2−1)) I_r "trivially holds") η must be 2(√2−1)σ_r²(X).  The lemma is unaffected. | the passage (statement and its proof read; the rest of the paper not read) |
| W3 | 23:13 | https://proceedings.mlr.press/v48/tu16.pdf (curl; 10 pages; text by pdftotext) | the ICML 2016 version ("Proceedings of the 33rd International Conference on Machine Learning, New York, NY, USA, 2016. JMLR: W&CP volume 48"): the same **Lemma 5.4**, same statement, same sentence after it; proof not in the 10 pages | the passage (statement only) |

**Verdict on the attribution of Lemma P:** correct — authors, year, number (5.4 in both the arXiv v2 and the ICML 2016 proceedings version) and statement match.
The source states it for ANY U, X ∈ ℝ^{n×r} (no rank hypothesis; for rank X < r the right side is +∞).  "cited from memory" can be replaced by the checked citation.
* 23:11–23:16Z `item2_adv_fixedX_run2.log` (complete): 19 reference chains [corrected at 23:50Z: an earlier version of this line said 26 — a miscount of mine] (helix-like n=6..20, strand-like 160/175, random, angle-constrained, thin
  interior window h=0.1/0.01/0.001, double tetrahedron), 66–84 starts each, L-BFGS with analytic gradients (self-check 6e-8; control: gradient
  scaled by 1.3 → error 0.13).  0 violations.  Largest: d_P/(C_L‖η‖) = 0.00742 (double tetrahedron n=5); d_P/‖local‖₂ = 0.355; per-point 0.647.
  **Finding to follow up:** for helix-like chains the best d_P/‖η‖ is far ABOVE the first-order constant 1/(2μ): n=20: 1.92 against 0.447
  (a distant maximiser, d_P/diam = 2.95, ‖η‖ = 22.1 Å²); n=12: 0.93 against 0.23; n=8: 0.62 against 0.16.  For thin-window chains
  116 and 1066 against 3.3 and 15.  So sup_Y d_P/‖η‖ (the true global constant) is not the first-order one.
* 23:19Z `item3_Lplus_run1.log` (complete): symbol max 11.039115763 at 57.4533° ✓ (< 11.04); Λ_n increasing, Λ_1000 = 11.038914 ✓.
  1346 pairs inside the certified ranges: 6 "violations" with d_P/bound ≤ 1.0000055, all at the smallest amplitude (‖η‖ = 1e-4 × range, displacement
  ~1e-9): **suspected rounding** (Y = X + V formed in double loses V's low bits: relative noise ~1e-6 in ‖η‖).  NOT to be cited as it stands; to be
  redone with η computed from V exactly (2d·w + |w|²) and d_P by a perturbative Procrustes (run2).  Part (3) of that log is fine: thin-window chain
  n=10, reflection of the tail: μ → 0.164 (1/(2μ) → 3.05) as h → 0 while d_P/‖η‖ = 4.9, 46, 456, 4560 for h = 0.1, 0.01, 0.001, 0.0001; at h = 1e-4,
  ‖η‖ = 3.3e-4 ≤ μ²/Λ = 2.9e-3 and d_P = 1.51 ≫ ‖η‖/μ = 2.0e-3: the conclusion of L⁺ fails for a Y inside the "first-order range" μ²/Λ — the
  restriction to μ/(ΛC_L) is doing real work.
* 23:20Z `item2_adv_joint_run2.log` (complete): joint search over (X, Y), numerical gradients: uniform ratio sup 0.00767 (n=5), 0.00789 (6), 0.00897 (7),
  0.00922 (8); local Frobenius 0.434 (n=5), 0.310 (6), 0.295 (7), 0.256 (8); per point 0.841 (n=5), 0.836 (n=6); 0 violations.
* 23:21Z `item4_tables_run1.log` (complete): their §6 table replicated (C_L 184.5/455.7/9795/1784/4406/94710/65130; 1/(2μ) 0.2313/0.4471/9.502/3.246/
  7.311/167.9/41.61; first-order worst case 4.208/8.96/206.8/57.82/140.1/3463/753 — all agree with theirs to the digits they give; certified range
  agrees within the conversion (they appear to use Λ_n, I used 11.04 in that table)).  Thresholds for "error bar < radius of gyration":
  helix-like 3.8e-3 Å (n=5), 8.5e-4 (20), 1.8e-4 (100); strand 160: 2.8e-4, 8.7e-5, 1.9e-5; strand 175: 1.9e-5, 5.9e-6, 1.3e-6.
  With C_loc (= 2‖M‖₂ from the local form): 0.17 Å (n=5: this is just Lemma Q), 4.3e-3 (20), 6.8e-4 (100).
* 23:23Z `item2_adv_jointU.py` (analytic gradients, smooth surrogate ≤ exact): trial run to the terminal (not a log): 0.0141 at n = 10.
  Full runs `item2_adv_jointU_run1_seed27116.log`, `…27117.log` started 23:23:36Z.
* 23:31Z **Tool action declined:** a foreground `sleep 100 ; …` (to wait for the two running searches) was blocked by the shell tool ("use Monitor
  with an until-loop / run_in_background; do not chain shorter sleeps").  Not worked around: no further sleeps; I continue with other work and read
  the logs when they are complete.

## Web log (continued; Item 5; generic queries only)

| # | time | address / query | what it gave | reading level |
|---|---|---|---|---|
| W4 | 23:24 | https://arxiv.org/abs/2207.07218 (WebFetch) | Arias-Castro & Chau, "On the Selection of Tuning Parameters for Patch-Stitching Embedding Methods", v1 14 Jul 2022, v2 18 Oct 2023; comment on the page: "Theory was removed to spin off another paper" (arXiv:2310.10900).  So the current version has no stitching error bound. | record only (abstract page, through a summarising fetch) |
| W5 | 23:24 | https://arxiv.org/abs/2310.10900 (WebFetch) | record: Arias-Castro & Vishwanath, v1 17 Oct 2023, v2 26 Mar 2024, v3 8 Dec 2024 | record only |
| W6 | 23:25 | https://arxiv.org/pdf/2310.10900v3 (curl, 591 kB; pdftotext) | Theorem 2.1: "there are σ > 0 and A > 0 … such that, if Σε² ≤ σ², sequential lateration outputs an embedding satisfying min_g Σ‖y_i − g(x_i)‖² ≤ A Σ ε²"; (2.6) A_n ≤ (1+C₂α)^{n−p−1}/((p+1)ω²)·max{C₁α, C₂/(1+C₂α)}; (2.7) the admissible η⁴ decreases like (1+C₂α)^{−(n−p−2)}; "worst case scenario where … each node v_k is connected to precisely the preceding p+1 nodes"; Theorem 3.1 the same form for stress minimisers ("if Σε² ≤ σ²"); Prop. 3.2 lower bound; noise model d²_ij = ‖x_i−x_j‖² + ε_ij (1.2).  **Both theorems have a smallness condition and an exponential constant in the worst case** — as the note says. | the passages (statements of Thm 2.1, 3.1, Prop 3.2, (1.1), (1.2), (2.6), (2.7) and the remarks around them; proofs not read) |
| W7 | 23:25 | search: "stability bound network localization lateration graph noise "polynomial" accumulation of error Procrustes stitching overlapping cliques global bound without small noise assumption" | only the arXiv 2310.10900 pages and Moore et al. 2004; nothing threshold-free | search summary |
| W8 | 23:25 | search: "patch stitching embedding error bound Procrustes alignment overlapping patches error accumulation number of patches theorem rigid alignment noise" | arXiv 2207.07218; arXiv 2303.11620 (Kohli, Mishne, Cloninger, rigid alignment of patches); arXiv 2604.21094 (Lemma 17); arXiv 2510.13406 (Maystre et al., Procrustes bounds from dot products) | search summary |
| W9 | 23:26 | search: "noisy Euclidean distance matrix completion overlapping cliques facial reduction error bound chordal graph singularity degree Hölder error bound square root" | arXiv 1410.6852 (Drusvyatskiy, Krislock, Voronin, Wolkowicz); arXiv 1405.2037 (coordinate shadows); Waterloo reports | search summary |
| W10 | 23:26 | search: "quantitative global rigidity estimate point configuration from distances "for all" configurations no smallness assumption chain of simplices sequence local distances stability constant length squared" | generic global rigidity papers (qualitative); Singer PNAS 2008; Javanmard–Montanari FoCM; nothing matching | search summary |
| W11 | 23:26 | https://arxiv.org/pdf/1410.6852 (curl, 646 kB; pdftotext) | Drusvyatskiy, Krislock, Voronin, Wolkowicz, "Noisy Euclidean distance realization: robust facial reduction and the Pareto frontier", arXiv v2 26 Aug 2015.  A clique-based (= windows with complete data) method "provably robust to noise … output error is linearly proportional to the noise level".  Theorem C.5 (Robustness): under three conditions "there exist constants ε > 0 and κ > 0 so that ‖P∘K(Alg(d̂)) − d‖ ≤ κ‖d̂ − d‖ whenever ‖d̂ − d‖ < ε" — local, constants not explicit, a statement about the data fit of the algorithm's output. | the passages (abstract, p. 3 paragraph, Appendix C statement and proof of Thm C.5) |
| W12 | 23:27 | https://arxiv.org/abs/2510.13406 (WebFetch) | record: Maystre et al., "When Embedding Models Meet: Procrustes Bounds and Applications", 15 Oct 2025; abstract: a tight bound on the alignment error when pairwise dot products are approximately preserved (the bound itself not on the page) | record only |
| W13 | 23:27 | search: "Procrustes" "Gram" inequality dist(U,X)² ≤ … classical scaling perturbation bound global | Arias-Castro, Javanmard, Pelletier (JMLR 21, 2020): Procrustes bound in terms of Gram matrices; a 2026 arXiv paper (2605.30687) uses its Frobenius branch under the condition ‖X†‖ε ≤ 1/√2 (i.e. a smallness condition) | search summary (ACJP not opened by me) |
| W14 | 23:27 | https://arxiv.org/pdf/2604.21094 (curl, 858 kB; pdftotext) | Nguyen-Cong, Hy, Dinh, "Spectral Embeddings Leak Graph Topology: Theory, Benchmark, and Adaptive Reconstruction".  Lemma 17: Procrustes alignment residual of two overlapping eigenvector patches ≤ O(√m η/δ_v); Lemma 18: "‖X_u − Z_u‖_F ≤ O(depth(u)·E_align) + O(E_local)" — errors accumulate linearly with depth for sequentially stitched patches.  O(·) constants; data are local spectral embeddings, not distances; no lever arm, no explicit conditioning constant. | the passages (statements of Lemmas 17, 18 and the two paragraphs around them; proofs not read) |

## Runs (continued)

* 23:23–23:33Z `item2_adv_jointU_run1_seed27116.log`, `…_seed27117.log` (both complete): joint search for the UNIFORM bound with analytic
  gradients (self-check 1e-8; surrogate ≤ exact).  Largest d_P/(uniform bound): n=5 0.00765, 6 0.00848, 7 0.0103, 8 0.0113, 9 0.0120, 10 0.0145,
  11 0.0141, 12 0.0167, 14 0.0174, 16 **0.0180** (seed 27116), 0.0175 (seed 27117).  0 violations.  Structure of the maximisers (inspected by hand,
  n=12 and 16): two nearly straight arms of long bonds (≈ b) joined by a "hinge" of short bonds (0.2–0.26 b); the windows that are thin are all
  equally thin (τ ≈ 0.063 b, s ≈ 0.077 b); the error η sits on the two central windows (e_j/‖η‖ ≈ 1 there), on pairs of separation 1 and 2 (92 %),
  NOT on the separation-4 pair; one change of determinant between consecutive frames; d_P comes from the lever arms.  At the n=16 maximiser:
  d_P/‖local‖₂ = 0.248, Lemma Q ratio 0.759, Step 2b 0.683, the passage local → uniform loses the rest (Cauchy–Schwarz over windows that carry no
  error).
* 23:33Z `item3_Lplus_v2_run1.log` (complete): everything computed from V (no cancellation; perturbative Procrustes cross-checked: agrees with the
  ordinary one within its rounding; control: a first-order-only routine differs by 8.5e-5).  1322 pairs inside the certified ranges, **0 violations**
  (tolerance 1e-10), max d_P/bound = 0.99999995 (softest mode, smallest amplitude): the bound is attained in the limit.  Controls: first-order
  constant alone violated by 52 pairs (none on the helix n=20: its softest mode has no cubic term, by symmetry I believe — not checked); 1.01 μ
  violated by 187.  The six "violations" of v1 were rounding, as suspected (own error, v1 not to be cited for part (2)).
  Part (3): thin-window chain n=10: μ → 0.2066 while d_P/‖η‖ = 2.3, 24, 242, 2420 for h = 0.1, 0.01, 0.001, 0.0001; for h ≤ 1e-3 the reflected
  configuration has ‖η‖ ≤ μ²/Λ and violates both conclusions; d_P/(C_L‖η‖) stays at 1.6e-4 as h → 0: the 1/τ of Theorem L is the right order.
* 23:34Z `item4_examples_run1.log`: INCOMPLETE (an assert of mine — an instance filter "interior τ > 1e-3" — stopped it; not a theorem check);
  `item4_examples_run2.log` (complete): (A1) interior coplanar window: η = 0 to 1e-15, d_P = 0.02–3.6 → false; (A2) both END windows coplanar:
  3600 pairs, 0 violations (max per-point 0.286; uniform with interior τ*: 0.0022); control 48/48; (B1), (B2) missing pairs: false (examples);
  (B3) an interior pair of separation 1–3 removed: μ stays positive (0.28–0.30 vs 0.30); (C) Y in ℝ⁴: d_P/‖η‖ = 0.489/ε; (D) (d,K) = (2,3), (3,4),
  (3,5), (3,6), (3,7), (4,5): 1000 pairs each, 0 violations; control (no lever arm) violated 4–60 times.
* 23:35Z `item2_cor_L3_run1.log` (complete): helices n = 20…320, K = 4, 6: lower bound ≤ 1/s_7 ≤ upper bound in all 30 cases; exponents 1.98–2.00
  (helix-like, strand 160), 1.89 for strand 175 over n = 40…320 (pre-asymptotic: (1/s_7)/n² → 0.730).  Helix-like, K=4: 1/s_7 = 0.0104 n², lower
  bound 2.3e-4 n², upper bound 28.9 (n+2)²: the two explicit constants are 1.3·10⁵ apart.  μ/(s*τ*/(2.4 b (n+2)²)) ≈ 1010–1050 (helix), 550–600
  (strand 160), 1500–1800 (strand 175), ≥ 351 on 200 random chains.  Controls fail as they should (20, 25, 64).
* 23:35Z `item4_worstcase.py` running (worst RMSD at a given rms DISTANCE error, by constrained search).  First lines: helix n=20: σ = 0.1 Å →
  0.91 Å (= first order); σ = 0.3 Å → **9.95 Å, above the radius of gyration 8.95 Å**; helix n=12: σ = 0.5 Å → 6.35 Å (R_g 5.66).  To verify.
* 23:33–23:43Z `item2_adv_jointU_run2_large_seed27121.log` (complete, 596.9 s): continuation from the n=16 maximiser to n = 18…40: 0.0155 (18),
  0.0158 (20), 0.0129 (24), 0.0141 (28), 0.0126 (32), 0.0098 (40).  So the largest ratio d_P/(uniform bound) reached anywhere is **0.0180 (n = 16)**;
  beyond n ≈ 16 the single-hinge design loses (expected: its bound grows like n² and its distance like n^{3/2}).
* 23:35–23:36Z `item4_worstcase_run1.log` (complete; 81.7 s): max d_P subject to rms DISTANCE error ≤ σ (SLSQP).  One row "no feasible end point"
  (helix n=20, σ=0.2).  Stored configurations re-evaluated in `item4_worstcase_verify_run3.log` Part 1 with a different code path: all 27
  satisfy their constraint; RMSD values confirmed; the distant ones have about half of their four-point windows with the opposite chirality.
* 23:38Z `item2_corollaries_run1.log` (complete): L.1: 330 estimates (stress minimisers with stress ≤ Σε²), 0 violations, max ratio 1.2e-3, control
  (/1000) violated once; L.2: 864 pairs, bound computed from the estimate only, 0 violations, max 1.6e-3; control (ν left out) 30/30.
  σ_min(edge matrix)/σ_3(centred) ∈ [1.0000, 1.9997] on 20 000 windows ✓; σ_3 monotone 20 000/20 000 ✓.
* 23:39–23:41Z `item4_worstcase_verify_run1.log`, `_run2.log`: Part 2 (scan by SLSQP) FLAWED — most rows "none" (SLSQP ends slightly infeasible),
  and in run1 the control line printed the wrong row.  **Own error; Part 2 of those two logs is not to be cited.**  Replaced by a penalty
  formulation (minimise the rms distance error subject to RMSD ≥ r): `item4_worstcase_verify_run3.log` (complete).  Results (every row an explicit
  configuration, re-evaluated; an upper bound for the true minimum):
    helix-like n=20 (R_g 8.95 Å, first-order 8.96σ): RMSD 0.5 Å needs 0.0556 Å (first order 0.0558 ✓ control); 1 Å: 0.110; 2 Å: 0.210;
      **RMSD 6.97 Å at rms 0.237 Å** (max error 1.39 Å on one pair; one window of opposite chirality); 9.0 Å at 0.271 Å; 10 Å at 0.308 Å.
    helix-like n=12 (R_g 5.66): 1 Å: 0.220; RMSD 4.28 Å at 0.320 Å; 5.76 Å (> R_g) at 0.367 Å.
    strand-like 160 n=20 (R_g 19.05, first-order 140σ): 1 Å: 0.0071; 4 Å: 0.026; 10 Å: 0.068 Å.  (From run1: 18.6 Å at 0.2 Å, 21.2 Å at 0.3 Å.)
  Reading: on these idealised traces, local distances with errors of a few tenths of an ångström (helix) or a few hundredths (strand) admit, in the
  worst case, configurations farther than half the radius of gyration.  The first-order factor (9σ, 140σ) is valid only up to σ ≈ 0.2 Å (helix).
* 23:41–23:43Z `item2_battery_run2.log` (complete; 116 s): as run1 plus roles swapped (Corollary L.2 situation): 10 933 pairs, 0 violations.
* 23:44Z helix n=20: ⟨AV, Q(V)⟩ = 3e-16 for the softest mode (cubic term vanishes); helix n=12: 0.069; strand 160 n=12: 2.5e-5 (terminal check,
  not a log).  So "1/(2μ) alone is not a bound at finite amplitude" is generic, not universal.
* 23:44Z `item2_adv_step2.py` started (Step 2 attacked on its own, six points).
* 23:44–23:47Z `item2_adv_step2_run1.log` (complete): Step 2 on its own (six points, 120 starts): sup of ‖R₁−R₂‖_F τ/(δ₁+δ₂) = 0.830 and of
  ‖R₁−R₂‖_F τ/(‖ε₁|W‖+‖ε₂|W‖) = **1.000000** — both at maximisers with det R₁·det R₂ = −1 and ‖R₁−R₂‖_F = 2.0000.  So the linear-algebra line of
  Step 2 is attained exactly, in the opposite-determinant case; no violation.  Control (s₁ for τ): violated (5·10⁵).
* 23:46–23:47Z `item4_extras_run1.log` (complete): (1) Lemma Q for ONE helix-like five-point window: RMSD ≤ 0.32 Å at |errors| ≤ 0.1 Å (worst found
  0.147), 0.99 at 0.3 (0.48); strand 160: 2.1 (0.67); strand 175: 8.0 (0.61).  (2) (local) with the earliest window containing k, i⁻(k) = max(1,k−4):
  71 688 point-wise checks, 0 violations, largest ratio 0.527; control (one more term dropped) violated 1742 times.
* 23:47Z `diag_ptratio_run1.log` (complete): the diagnostic of the per-point noise-floor error, now in a log.
* Side remark (terminal reasoning, from P3 of item1): for m = r the numerical sup of LHS/RHS in Lemma P is 2(√2−1) (collapse of the weakest
  direction), i.e. there the inequality holds with 1/σ_r²; irrelevant for five-point windows (centred rank 4 > 3).

## Status at 23:48Z: all computations done; writing docs/science/workstreams/R27_REPORT.md.
Logs NOT to be cited (incomplete or flawed): item2_adv_fixedX_run1.log, item2_adv_joint_run1.log (stopped: noise-floor error), item4_examples_run1.log
(stopped by an assert of mine), item3_Lplus_run1.log part (2) (rounding), item4_worstcase_verify_run1.log / _run2.log Part 2 (SLSQP infeasible).
The scripts on disk are the versions of the LAST run of each (battery: run2; adv_fixedX, adv_joint: run2; adv_jointU: run2_large, same computation
as run1 plus two optional arguments; worstcase_verify: run3; examples: run2).  Files `…_seed1.npy` come from a 50-second trial of
item2_adv_jointU.py printed to the terminal (no log).

| W15 | 23:51 | https://arxiv.org/pdf/1810.09569 (curl, 1.9 MB; pdftotext) | Arias-Castro, Javanmard, Pelletier, "Perturbation Bounds for Procrustes, Classical Scaling, and Trilateration, with Applications to Manifold Learning", arXiv v2 24 Oct 2019.  Theorem 1: X, Y tall of the same size, X of full rank, ε² = ‖YYᵀ − XXᵀ‖_p; then min_Q ‖Y − XQ‖_p ≤ ‖X‡‖ε² + (1 − ‖X‡‖²ε²)^{−1/2}‖X‡‖ε² ∧ (d^{1/2p}ε) if ‖X‡‖ε < 1, and ≤ ‖X‡‖ε² + d^{1/2p}ε otherwise; "Consequently, if ‖X‡‖ε ≤ 1/√2, then min_Q ‖Y − XQ‖_p ≤ (1+√2)‖X‡‖ε²" (5).  So the linear bound (5) has a smallness condition, but the theorem itself is stated for all Y; and since ε ≤ √2‖X‡‖ε² when ‖X‡‖ε ≥ 1/√2, its two branches together give a threshold-free linear bound with constant 1 + √2·d^{1/2p} (my one-line combination, not a statement of theirs) — for p = 2, d = 3: 2.86‖X‡‖‖ΔG‖_F, against 1.10 from Lemma P. | the passage (statement of Theorem 1 and the lines after it; proof not read) |

(the row above belongs to the second web table)

## 23:58:02Z — report written
`/home/user/MetricChain/docs/science/workstreams/R27_REPORT.md` (sections 0–6) is complete.  Verdicts: Lemma P, Lemma Q, Theorem L (local and
uniform), Corollaries L.1–L.3, Theorem L⁺: all proved as stated; 0 critical, 1 major (F1: the first-order constant is not the global one; explicit
distant configurations at 0.24–0.37 Å rms on helix-like traces, 0.07 Å on a strand-like one), 11 minor (F2–F12).  Largest ratios reached: 0.84
(local, per point), 0.43 (local, Frobenius), 0.018 (uniform, n = 16).  Read-only `git status --short` at 23:57Z shows as mine only
`docs/science/workstreams/R27_REPORT.md` and `experiments/science/ws_R27/` (the other entries belong to other workstreams).
Tool actions declined: one (a foreground `sleep 100`), not worked around.
Disclosures: text-editing snippets were run as `python3 -` without -B and without the cap (no computation, no cache directory); short commands
(curl, pdftotext, grep) ran beside two running computations.
