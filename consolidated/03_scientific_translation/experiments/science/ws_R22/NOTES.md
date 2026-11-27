# R22 — working notes (adversarial review of Geometry division Theorems B, B′, G)

All times read from the clock (`date -u`).

## 2026-11-26 17:16 UTC — start

* Read `docs/science/workstreams/COMMON.md` and `R22_brief.md`.
* Created `experiments/science/ws_R22/` (did not exist).
* Object: `<GEO>` = `/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/geo_ro_d84a43b/`
  (30 files; read-only for me).
* Plan: (1) read GEOMETRY-REQ-0003, GEOMETRY-MSG-0002, ENSEMBLE_RIGIDITY.md (all 729 lines), Lean file;
  (2) read coordinator's hinge_pair.py/.log; (3) own code from the definitions BEFORE opening their code;
  (4) line-by-line re-derivation; (5) re-run their checks from a scratch copy; (6) prior art; (7) report.

## Tool actions declined

(none so far)

## Log

### 17:16–17:25 UTC — reading (read only)
* Read in full: GEOMETRY-REQ-0003.md, GEOMETRY-MSG-0002.md, ENSEMBLE_RIGIDITY.md (all 729 lines),
  proofs/Geometry/EnsembleRigidity.lean (397 lines), coordinator's hinge_pair.py + hinge_pair.log.
* NOT yet opened: their experiments/geometry/*.py (will open only after my own code exists).
* First-pass marks while reading (to be re-derived, not yet findings):
  - Lemma 2.2: `A` is said "measurable A: C → R^{d×m}" but x_1 normalised to 0; "A^T A ∈ P(z)" a.e. requires
    a version; fine. Check: the datum includes E0 pairs? yes (M(ν)=D(z) on all pairs).
  - Thm B proof: "(CC) ⇒ z spans affinely: else vv^T ∈ N(z), but a block-scalar matrix has rank 0 or ≥ d ≥ 2" —
    rank 0 or a multiple of d; vv^T rank 1; OK for d ≥ 2. (T ⊂ block-scalar.)
  - Thm B: "class of X_k has ν-probability w_k" — if two X_k are congruent (X_k ≅ X_l), z does not span? Check:
    if X_1 = R X_2 then stacked z has rank ≤ ... (blocks proportional up to rotation) → not spanning → (CC) fails. OK.
  - Thm B′ (⇒): Tchakaloff — P(z) is closed; compact? I + N(z), P ⪰ 0, rank ≤ d. e^T P e = |e|^2 for edges.
    If edges of z span R^m (z spans affinely and E0 connected ⇒ edge vectors span), then PSD P with e^T P e bounded
    on a spanning set is bounded (tr P ≤ ...). Need check. Tchakaloff for a Borel prob. measure on a compact set with
    finitely many (continuous) moment functions: fine. Restricting to ball B and complement — fine.
    BUT: "ρ'' (B) > 0 ⇒ [ν'] ≠ [μ]" — needs points of B to be ≠ E_k/w_k: yes B disjoint. OK.
    But is ρ' a measure on P(z) with barycentre I *any* such measure — fine.
    Also the (⇐) direction: needs ρ = (A^T A)_* ν be the unique one — fine.
  - Thm G(b): "smooth manifold near X_k" and n−1 > dK. Compactness: inf over X ∈ C not in ∪[X_k] of φ/d_P^2;
    away from the states φ > 0 continuous on compact → positive min. Near the states: sequence argument.
    Flex V in limit: V orthogonal to infinitesimal isometries AND a flex with Π^⊥ V = 0. Need: the algebra.
    NOTE the flex condition uses only first order; no smoothness needed for "limit of secants is a flex"?
    (constraints 2 e·V_e + ρ|V_e|^2 = 0 → e·V_e = 0: yes no smoothness needed.) So where is smoothness used in (b)? Not.
    In (d): "Δ = τ + O(|Δ|^2) with τ tangent" — needs smooth manifold AND flex space = tangent space (regular point).
  - Thm G(b) algebra: V = z B^T + 1 t^T; edge of V is Be; edge of X_k is Π_k e/√w_k; flex: (Π_k e)·(Be) = 0
    ⇒ e^T Π_k^T B e = 0 ⇒ sym(Π_k^T B) ∈ N(z) = T.  Π_k^T B is dK×dK with nonzero rows only in block k.
    sym = block-scalar Σ s_l E_l. Off-diagonal blocks (k,l) of Π_k^T B: B_l (the l-th d×d block of B) at position (k,l);
    symmetrisation has (k,l) block = B_l/2 and (l,k) block = B_l^T/2 → must vanish → B_l = 0 for l≠k.
    (l,l) block for l≠k is 0 → s_l = 0. Then Σ w_l s_l = 0 → w_k s_k = 0 → s_k = 0 → sym(B_k) = 0 → B_k skew.
    Then V = X_k-edge... V = z B^T + 1 t^T = √w_k X_k B_k^T + 1 t^T: infinitesimal isometry. OK at first sight.
  - Thm G(c): ‖Π^⊥‖_F = √(n−1−dK): rank of Π^⊥ = n − 1 − dK if z spans affinely. OK. Needs n−1>dK for Π^⊥≠0
    (else φ ≡ 0 and κ = 0 → (b) false!). Actually if n − 1 = dK, φ ≡ 0, so (a) "vanishes exactly on classes" false.
    With (CC) and K≥1: 2n−3 ≥ D_K ... n−1 > dK automatically? For K=1: n ≥ 5 > 4 = dK+1 OK n−1 ≥ 4 > 3. yes.
  - Thm G(d): bracketed proof — to redo in full.
  - Thm G(e): fine if ∂_v X ≠ 0 mod isometries.

### 17:25–17:50 UTC — read the rest of <GEO>/docs (PRIOR_ART, PROOF_OBLIGATIONS, DEAD_ENDS, RESEARCH_LOG, THEOREM_REGISTER,
HANDOFF) and the coordinator's SCI-RES-0029.  Their code still unopened.  Paper re-derivation (before numerics):

**Lemma 2.2** — holds.  Simpler proof that removes the measurability worry (i): with Π^⊥ = projector off span(1, cols z),
φ(x)=tr(x^T Π^⊥ x) = −½<Π^⊥,D(x)> ≥ 0 and ∫φ dν = −½<Π^⊥,M(ν)> = −½<Π^⊥,D(z)> = φ(z) = 0 ⇒ φ=0 on supp ν (φ continuous) ⇒
x = 1 t^T + z A^T with A(x) = (Z0^+ X0)^T a LINEAR (continuous) function of x.  ∫A^T A dν = I from M(ν)=D(z) and
"a quadratic form vanishing on all differences of an affinely spanning set is 0".  No L² representatives needed.

**Theorem B** — holds as stated (needs Σw=1, w>0, complete data).  Pairwise non-congruence of X_k follows from (CC)
(⇒ z spans).  Lean `block_rigidity` = TWO-block statement (U1 ⟂ U2, finrank d, A into finrank ≤ d, ‖A(u+u')‖² =
c1‖u‖²+c2‖u'‖² ⇒ c1=0 ∨ c2=0); the K-block step of the paper = apply to every pair + Σ w_k c_k = 1 ("exactly one") —
not in Lean (§10 says so; §4.2 l.242–244 says "Σ_k c_k|E_k v|²", loose).

**Theorem B′** — holds.  Unstated but true: P(z) compact when z spans affinely & E0 connected (edge vectors span R^m;
tr P ≤ Σ|e|²/λ_min(Σ e e^T)).  "Tchakaloff" = barycentre of a prob. measure on a compact set lies in its convex hull
+ Carathéodory; ball/complement split keeps barycentre exactly.  Fine.

**Theorem G(b)** algebra redone in full: sym(Π_k^T B) block structure ⇒ B_l=0 (l≠k), s_l=0 (l≠k), w_k s_k=0 ⇒ B_k skew ⇒
V infinitesimal isometry.  OK.  "V_j ⊥ infinitesimal isometries at X_k": first-order optimality gives ⊥ to isometries at
X_j; but <V_j, V_j Ξ^T> = tr(V_j^T V_j Ξ^T) = 0 (sym × skew) so also at X_k exactly.  OK.
Smoothness of C is NOT used in (b) (limit of secants is a flex needs only the constraint equations); used only in
(d) (Δ = τ + O(|Δ|²)) and (e).  n−1 > dK only makes Π^⊥ ≠ 0; for chains in R^3 it follows from (CC)
(2n−3 ≥ D_K ⇒ n ≥ (9K²+K+8)/4 > 3K+1).
**(d)** bracketed proof redone: ż = zΞ^T + 1t^T (complete framework on a spanning set is inf. rigid);
flex of state k on stacked edges: e^T[E_k Ξ − (a_k/2w_k)E_k]e = 0 ⇒ sym(E_kΞ) − (a_k/2w_k)E_k ∈ T;
sym(E_kΞ) has zero diagonal blocks, off-diag (k,m) = ½Ξ_km ⇒ Ξ block-diagonal; (k,k): −(a_k/2w_k)I = s_k I, s_l=0 (l≠k),
Σw s=0 ⇒ a_k = 0.  OK.  Slip: "‖D(Δ)‖ ≤ 4‖Δ‖²" is false in Frobenius norm for n>10 (Δ_1=u, Δ_2=−u: ‖D(Δ)‖_F =
√(4n+24) vs 8); true constant ≤ min(2n, 4√n).  Harmless (constant not tracked).
Transport: W2² ≤ 2Q + 2·diam²·TV = 2Q + diam² Σ|ν_k−w_k|: matches.

**Weaker natural hypotheses for G(a)–(c)** (to test): (H1) P(z) = {E_k/w_k}; (H2) no flex of (E0,X_k) of the form
z B^T + 1 t^T other than infinitesimal isometries.  (CC) ⇒ H1, H2; the compactness proof of (b) uses only H1, H2.

**Finitely many states is essential (Carathéodory):** M(μ) ∈ conv D(C), dim aff ≤ (n−2)(n−3)/2, so there is a ν with
≤ (n−2)(n−3)/2+1 atoms and M(ν)=M(μ): an ensemble with more shapes than that (in particular any continuous part)
is never identifiable.

**Shared rigid segments (K=2), analysis by Lemma 2.2 / Theorem B′ (my derivation; to be checked numerically):**
segments S_j, state 2 = Q_j·state 1 on S_j (Q_1 = I), competitor x = A z, A=[A1 A2], F=√w1 A1, G=√w2 A2,
B_j = F + G Q_j must be in O(3) on every segment whose edge directions lie on no conic (≥5 atoms generic).
Normalise B_1 = I: B_j = I + G(Q_j − I).  Competitor conformations = re-hingings INCLUDING reflections of segments
(B_j ∈ O(3), not SO(3)): component (det ρ_1, det ρ_2, …) with ρ_j = B_j^{-1}B_{j+1} ∈ O(2) about hinge j.
* s=2 (one torsion): z spans only 5 dims; P = two circles (rotations and reflections about the hinge). Not identifiable.
* s=3 (two torsions θ1, θ2; hinge directions b1, b2 in the frame of S_2, e = unit(b1×b2), σ = reflection with normal e,
  Rot_j = rotation about b_j by θ_j): solving G on b1^⊥ and on Q_2 b2^⊥ with consistency on their common line gives
  EXACTLY 8 linear images, (ρ1, ρ2) =
    (I,I)=X1, (Rot1,Rot2)=X2, (Rot1,σ), (I,σRot2), (σ,Rot2), (Rot1σ,I), (Rot1σ,σRot2), (σ,σ)
  i.e. 6 spurious conformations with mirrored segments, at EVERY chain length (so φ has 6 extra zeros; G(a) fails).
  Data equations (E[ρ1], E[ρ2], E[ρ1ρ2]): the third forces c_(Rot1,σ)+c_(Rot1σ,I)=0 and c_(I,σRot2)+c_(σ,Rot2)=0
  (I, Q3, Rot1σ, σRot2 lin. indep.), the first gives (c_vi I + c_v Rot1)e = 0 ⇒ c_v=c_vi=0 unless Rot1 e = −e.
  ⇒ **two differing torsions: identifiable (generic), although (CC) fails and P(z) has 8 points;**
  **exception θ1 = θ2 = π (two half-turn flips): D(X1)+D(X2) = D(Y_v)+D(Y_vi) exactly ⇒ NOT identifiable**
  (Y_vi = middle segment mirrored in the plane of the two hinge directions, Y_v = the same on state 2).
* s=4 (three torsions): compatibility of the 8-point lists of the two overlapping triples leaves only X1, X2 (generic)
  ⇒ P(z) = 2 points ⇒ identifiable by Theorem B′ with dim N = 3 > 1.
* The coordinator's moment-matrix sketch covers only the proper (rot,rot) component; the mirrored components must be
  included (a grid LP over two torsions only would miss them).

### 17:30 UTC — coordinator's note received (mid-task), recorded here
* Geometry published a 2nd checkpoint 7c2a3d1 (17:18 UTC); my object stays d84a43b; line numbers of that export stay valid.
* New there: §5.5 Theorem I (generic two-state ensemble identifiable from n = 10 by an exact Gröbner computation:
  linear images of z that are chains = the two states; not at n = 7, 8; n = 9 numerical).  NOT part of my review;
  at most a one-paragraph remark.  Second read-only export: .../scratchpad/geo_ro_7c2a3d1/ (never write into it).
* For Item 3(c): the route "which linear images of z are chains, then an LP over those" is legitimate besides the grid LP;
  use whichever decides and say which.  (I had planned exactly that route; see the derivation above.)
* Report must say: review is of the text at d84a43b; §§2, 4.2, 7.2 unchanged at 7c2a3d1.
* My own check (read-only): sha256 of the text of §2, §4.2, §7.2 (heading to next heading) is identical in both exports
  (c679…f1da, 14da…e373, 414b…9475).  File grew 729 → 801 lines.

### 17:32 UTC — own library `r22lib.py` (transfer-frame chain, exact rational chain, conic system, Bareiss rank, Procrustes
with reflections, analytic torsion tangents).  Self-test v1: 1 "violation" = MY ERROR (threshold 1e-20 on a
floating-point Procrustes residual 7e-15); log moved to not_cited/; threshold set to 1e-12; v2: 0 violations
(`r22lib_selftest_v2.log`).

### 17:33 UTC — Item 3(a) `t3a_cc_thresholds.py` → `t3a_cc_thresholds.log` (12 s, reached last line; 0 violations)
* Exact (Q, cos = −5/13, Bareiss): rank = min(2n−3, D_K) in all 22 cases: K=1 n=4,5,6; K=2 n=10..13; K=3 n=21..24
  (two random rational tuples each).  (CC) holds exactly from n = 5, 12, 23; fails below.  Confirms Theorem C(b) at
  K = 1, 2, 3 for that geometry (replication, own code).
* Float: 20 random tuples per cell, 3 bond angles: dim N = dim Sym(3K) − min(2n−3, D_K) always; note the smallest
  kept singular value at threshold is small (1e-5 … 7e-6 relative) — conditioning at the threshold is poor.
* Controls: trivial quadrics in N(z) (8e-16); congruent pair dim N = 15; planar chain dim N = 3; weight-independent.

### 17:36–17:40 UTC — Item 3(c) route A: `t3c_linear_images.py` → `t3c_linear_images_run1.log` (25 s, reached last line)
Outcome (K = 2, weights 0.37/0.63, cos −1/3, own code; LM enumeration of the linear images of z that are chains + LP):
* control generic pair n=12: only the two states found (dim N = 1). OK.
* control ONE torsion: z has affine rank 5; 300/300 starts give 300 distinct images (continuum); LP min mass on true
  states = 0 → competitor exists (as it must).
* TWO torsions (segments ≥ 5 atoms), 8 instances n = 14…26: dim N = 6; all images found are among the 8 PREDICTED ones;
  the 8 predicted conformations are chains (edge error ≤ 4e-15) and linear images (φ ≤ 4e-28); alternating affine
  dependency P1−P2+Pi−Pii+Piii−Piv+Pv−Pvi = 0 holds to ≤ 5e-14; **LP minimum of the mass on the true states = 1.000000000
  in all 8 → identifiable although (CC) fails and φ has 6 further zero classes.**
  One instance (n=16, hinges [3,8]) LM found 7 of the 8 (a basin miss: `probe_7of8.log`, 1500 starts: hits per predicted
  point as low as 0–2 in some instances; never an image outside the predicted list) — reported as such, not hidden.
* TWO torsions, both half-turns: D(X1)+D(X2) = D(Yv)+D(Yvi) to 3e-14 (3 instances), Yv, Yvi far from the true shapes
  (d_P² ≥ 7); LP minimum = 0.26 = 1 − 2·min(w) → **NOT identifiable** (prediction confirmed).  At π−0.01 the LP minimum
  is 1 again (the exception is exactly the half-turn pair).
* THREE torsions (long segments), 6 instances n = 18…32: dim N = 3; only the two states are linear images → P(z) = 2
  points → identifiable by Theorem B′ (given the enumeration is complete; 180–400 of 400 starts converged, all to the 2).
  All half-turns with three torsions: still only two images (2 instances).
* SHORT segments (information): hinges two apart (j, j+2; middle segment of 4 atoms): continuum of images, dim N = 7,
  LP minimum 0 → NOT identifiable (to be verified directly); adjacent hinges (j, j+1): 4 images, LP minimum 1.

### 17:41 UTC — `t3c_short_segments.py` → `t3c_short_segments.log` (55 s, reached last line; control passes)
Arrangement study (2 instances each, 500 LM starts; every LP competitor verified: |Σc D − M| ≤ 3e-13, E0 errors ≤ 5e-15):
* one torsion: competitor (LP 0).  * (j, j+1): 4 images, LP 1.  * (j, j+3), (j, j+4): the 8 images, LP 1.
* (j, j+2) [4-atom middle segment]: CONTINUUM of images (dim N = 7); LP 1 in 5 of 6 instances, LP 0 in 1 of 6
  (a verified 8-state competitor, states at d_P² ≥ 3.09 from the true ones) → instance-dependent.
* (j, j+1, j+2): continuum (dim N = 7); LP 0 in 3 of 4 instances (verified competitors), 1 in 1 of 4.
* (j,j+1,j+3): 4 images, LP 1.  (j,j+2,j+4), (j,j+2,j+5), (j,j+3,j+6): only the two states.  Four torsions: two states.
So "long segments" is a real hypothesis: with a 4-atom segment or three consecutive torsions the set of linear images
is a curve and identifiability depends on the instance [N].
Next: route B grid LP (`t3c_grid_lp.py`), est. cost < 5 min, < 1 GB (largest LP 552 x 13824 dense).

### 17:45 UTC — route B `t3c_grid_lp.py` → `t3c_grid_lp_run1.log` (169 s, reached last line; 0 control violations)
Grid LP over ALL re-hingings (mirrored components included), true states on the grid:
* one torsion (control): LP1 = 0 (competitors), data-map rank 5 (= 1 + 2 rot + 2 refl).
* two torsions (4 instances, n = 20, 26, grid 24², 4 components, 2304 columns, data-map rank 13 = 1+4+4+4):
  LP1 = 1.000000 (only μ has exactly M); LP2 (|ΔM| ≤ ε entrywise): mass within one grid step of the true states
  ≥ 0.887…0.942 at ε=1e-2, ≥ 0.9887 at 1e-3, ≥ 0.9989 at 1e-4 (loss ∝ ε).
* two half-turns: LP1 = 0.26 = 1 − 2 min w with support (−,−)(12,12) and (−,−)(0,0), weights 0.37 each = Yv, Yvi;
  the SAME programme restricted to the proper component (a grid over the two torsions only, as in the brief's wording)
  returns 1.000000 — it would have missed the competitor.
* three torsions (2 instances, n = 26, grid 12³, 8 components, 13824 columns, rank 25 = 1+12+8+4): LP1 = 1; LP2 0.978 at 1e-2.
Both routes agree.  Route A decides (Theorem B′ + enumeration); route B is the brief's test and its control.
Prediction from my count of what M sees with h hinges and long segments: proper component rank 2h²+1 (9, 19, 33),
all components 1 + 4h + 4·C(h,2)… (5, 13, 25 observed) — to verify for h = 3, 4 on the proper component.

### 17:46 UTC — `t3c_fourier_rank.py` → `t3c_fourier_rank.log` (1 s): what M sees of h differing torsions (long segments):
rank of the map (3^h product functions → M) = 2h²+1 = 3, 9, 9, 19, 19, 33, 33 for h = 1, 2, 2, 3, 3, 4, 4 (0 violations).
So for h ≥ 3 M does NOT see all Fourier coefficients with indices in {−1,0,1}: 19 of 27, 33 of 81 (refines the
coordinator's item (5): "linear image of" is right; "sees every coefficient" holds only for h ≤ 2).

### 17:53 UTC — Item 3(b) `t3b_theorem_G.py` → `t3b_theorem_G_run1.log` (311 s, reached last line; 0 violations)
* (a) φ(X_k) ~ 1e-28; φ = −½<Π^⊥,D> to 1e-13; φ > 0 on 200 random chains.
* (b) local values (softest eigenvalue of Π^⊥ on flexes ⊖ isometries; reproduced by the ratio along the direction):
  n=12: 1.3e-2/2.2e-2 and 6.2e-3/6.3e-3; n=13: 8.0e-3/1.7e-2; n=14: 1.9e-2/2.9e-2 and 3.1e-2/1.9e-2; n=16: 8.2e-3; n=20: 1.5e-2.
  GLOBAL search (20000 random chains + 48 L-BFGS starts) finds SMALLER ratios FAR from the states:
  n=12: 1.15e-2 and 9.3e-4 (d_P² = 2.4, 8.0); n=13: 7.2e-3; n=14: 3.8e-3, 3.4e-3; n=16: 2.7e-3; n=20: 5.9e-3.
  ⇒ κ is not the local value (up to 7x smaller here); κ ≲ 1e-3 … 1e-2 in these instances.
* (c) constant √(n−7)/(2κ̂) = 97 … 1199; the bound beats the trivial bound only for ‖ΔM‖_F ≤ 0.02 … 0.64,
  i.e. 2.5e-4 … 4.1e-3 of ‖M(μ)‖_F; slack LHS/RHS on random ensembles 5e-5 … 5e-3; on symmetric broadenings ≤ 0.008.
* (d) infinitesimal identifiability: smallest s.v. of the column-normalised map 0.026 … 0.052 > 0.
* (e) exponents 2.000 (‖ΔM‖), 2.000 (W2²), one-sided control 0.997; W2²/‖ΔM‖ → 0.3116.
* (w) (CC) fails: two torsions: local values 2.7e-2, 1.6e-2 > 0 but global min ratio 9e-14 at d_P² = 20 (the mirrored
  linear images): κ = 0, G(a) fails, yet the mixture is identifiable; three torsions: local 3.6e-3 … 1.8e-2,
  global 8.5e-4, 1.9e-3 > 0: G(a)–(c) hold numerically without (CC).

### 17:54–17:56 UTC — Item 3(d) re-runs (THEIR code, scratch copy `rerun_copy/`, 13 files, sha256 identical to the export)
`python3 -I -B rerun_copy/run_checks.py` FAILS with ModuleNotFoundError (isolated mode does not put the script directory
on sys.path) — not a defect of their code; I used `rerun_launcher.py` (adds exactly the copy directory, runs as __main__),
still with `-I -B`.  mutation_checks.py spawns `sys.executable run_checks.py` itself (children not isolated;
PYTHONDONTWRITEBYTECODE=1 inherited; no __pycache__ appeared in the copy).
* run_checks.py: 23 of 23 PASS in 8 s (`rerun_run_checks.log`).  Report §11 says "about one minute", HANDOFF "about 10 s".
  quadratic_growth_local: local growth constants [0.03952, 0.05314] (n=14, 111°) — same order as mine (0.019…0.031 at
  cos −1/3); NO test of the global infimum exists in their harness.
* mutation_checks.py: 11 of 11 caught (`rerun_mutation_checks.log`, 13 s).
* hierarchy_example.py: OK, deviation on F 1.8e-15 (`rerun_hierarchy_example.log`).
* exact_conic_rank.py 12: ALL OK in 32 s, 48 lines (2 geometries × {bond+angle, bonds only} × K = 1..12), all at seed 0;
  n0(K) = 5, 12, 23, 39, 60, 85, 114, 148, 187, 230, 277, 329 as in Theorem C(b) (`rerun_exact_conic_rank_12.log`).
  THEOREM_REGISTER "96 witnesses for K ≤ 12" ≠ 48 printed [minor, outside my object].
* exact_jacobian_rank.py 8: ALL OK, 30 witnesses (2 s).  exact_4d_extreme.py: OK.  demix.py: state RMSD ≤ 7.7e-8,
  weights 2e-15 … 5.8e-12 (report: "weights to 1e-13" — not met at K=4: 5.8e-12), s* = 6.9e-3 (n=12), 7.8e-2 (n=16;
  report says 9e-2) [minor, outside my object].

### 17:57–18:12 UTC — Item 5 literature (generic queries only; nothing of this project in any query; nothing uploaded)
Search log (WebSearch, standard mode) and what was OPENED (WebFetch / PDF read with the Read tool):
 S1 "universal rigidity dimensional rigidity affine motions "conic at infinity" Alfakih theorem equivalent frameworks affine image"
    → opened ar5iv 1605.07911 (Connelly–Gortler–Theran, Affine rigidity and conics at infinity) [full text through the fetch
      tool's summary+quotes]: Def 1.1 conic at infinity; Prop 1.4 (conic ⇔ non-trivial affine flex, citing Connelly 1993/2005);
      Alfakih 2014: dimensionally rigid but not universally rigid ⇔ conic at infinity; Thm 4.2 super stability ⇒ universal rigidity.
    → opened arXiv abs 1401.7029 (Connelly–Gortler, Iterative universal rigidity) [abstract]; abs 1001.0172 (Gortler–Thurston) [abstract].
 S2 "identifiability mixture of conformations from ensemble-averaged squared distances Euclidean distance matrix decomposition
    unique mixture bond constraints" → nothing on the question [search summary].
 S3 "super-resolution dual certificate quadratic growth support stability bound weighted squared distance to true spikes noise
    level Fernandez-Granda "support detection"" → opened arXiv 1302.3921v2 (Fernandez-Granda, Support detection in
    super-resolution) [FULL TEXT, 4 pages read as PDF]: Thm 1.2 (ii) Σ|â_l|(t̂_l − t_j)² ≤ C2 λc² δ, (iii) Σ_far |â_l| ≤ C3 δ;
    Lemma 2.1 Σ|â_k| min{Ca, Cb d(t̂_k,T)/λc²} ≤ 2δ, d = squared distance to the support; Lemma 2.3 dual polynomial with
    |q| ≤ 1 − Cb (t−t_j)²/λc² near the support; proof = certificate linear in the data + Cauchy–Schwarz on the data misfit.
    ⇒ the mechanism AND the form of Theorem G(b)–(c) (quadratic-growth dual certificate ⇒ ∫dist² dν ≤ C·data error).
 S4 "unique decomposition of a Euclidean distance matrix as convex combination of low-dimensional distance matrices "faces" EDM
    cone mixture of point configurations identifiability stress" → nothing on the question [search summary]; opened ar5iv
    1405.2037 (Drusvyatskiy–Pataki–Wolkowicz, Coordinate shadows…) [through fetch summary]: Thm 4.1 singularity degree one ⇔
    minimal face exposed; Cor 4.3 Hölder-1/2 bound; Thm 3.2 projected EDM set closed.
 S5 "diploid genome 3D reconstruction identifiability Euclidean distance geometry homologous chromosomes distance constraints
    neighboring loci Belyaeva Kubjas Sun Uhler" → opened ar5iv 2101.05336 [through fetch summary]: two homologous copies in ONE
    frame, data = sum over the four copy pairs of SQUARED distances; Thm 1 infinitely many solutions; with neighbouring-bead
    distances unique in 2D, still infinitely many in 3D; with 3-way contacts unique in 3D.  Different model (not a mixture of
    separately observed conformations).  Opened abs 2301.11764 (Cifuentes et al., Bull. Math. Biol. 86:33, 2024) [abstract].
 S6 "convex hull of rotation matrices SO(3) spectrahedron faces orbitope "convex hull of SO(n)" Saunderson Parrilo Willsky free
    spectrahedron 4x4 positive semidefinite trace one" → opened ar5iv 0911.5436 (Sanyal–Sottile–Sturmfels, Orbitopes)
    [first 100k chars through fetch summary]: Prop 4.1 conv SO(3) affinely isomorphic to the free spectrahedron n=4;
    all proper faces are free spectrahedra of dimensions 0, 2, 5 (no edges); Example 1.1: the 4-dim Carathéodory orbitope is
    2-neighborly.  Opened ar5iv 0712.3777 (Longinetti–Sgheri–Sottile, Convex hulls of orbits and orientations of a moving
    protein domain) [through fetch summary]: mean susceptibility tensors (RDC), convex hull of an SO(3)-orbit, p_max(R) =
    maximal fraction of time in an orientation compatible with the averaged data; "ill-posed"; Carathéodory numbers.
    Not opened: 1403.4914 (Saunderson–Parrilo–Willsky).
 S7 ""maximum occurrence" OR "maximum allowed probability" conformation ensemble averaged data convex largest weight …" →
    [search summary only]: MaxOcc method (Andrałojć, Luchinat, Parigi, Ravera, Sgheri …): the maximum weight a conformer can have
    in ANY ensemble reproducing population-averaged data.  Nothing opened.
 S8 "identifiability finite mixture from low-order marginals bounded range "sequence separation" OR "banded" moments …" →
    [search summary only]: thresholds 2K−1 for mixtures of products/grouped samples (Tahmasebi et al. 1807.05444;
    Vandermeulen–Scott 2207.11164).  Nothing on banded distance moments.  Nothing opened.
 S9 "simplicial faces of the set of correlation matrices Tropp …" → opened arXiv 1801.00749v1 (Tropp, Simplicial faces of the set
    of correlation matrices, DCG 2018) [FULL TEXT pages 1–8 read as PDF]: Fact 2.6 faces generated by vertices are simplicial
    (Laurent–Poljak); Fact 2.7 simplicial face of dim k iff k(k+1) ≤ 2(n−1); **Fact 3.1 (= LP96 Thm 4.2): c_1..c_r ∈ {±1}^n,
    W = [c_1 … c_r], Z = [1 | c_i ⊙ c_j (i<j)]; if W and Z have full column rank then conv{c_i c_i^T} is a simplicial face of
    the elliptope.**  For d = 1 and star constraints, (CC) ⇔ "Z has full column rank" (my algebra) ⇒ Theorem B/Cor 4.2 at
    (d = 1, unit-diagonal constraints) IS this 1996 theorem; (CC) is its rank-d, general-E0 analogue.  LP96 itself not opened.
    Opened abs 1204.1220 (Saunderson–Chandrasekaran–Parrilo–Willsky, SIMAX 2012) [abstract].
 S10 "Li Tam "A note on extreme correlation matrices" …" → [search summary only]: criterion "rank-r correlation matrix extreme
    ⇔ span{z_i z_i^T} has dim r(r+1)/2" quoted from Gribling–de Laat–Laurent (arXiv 1605.00988, Thm 3.5, their ref [20]).
 S11 "truncated trigonometric moment problem on the torus unique representing measure flat extension …" → [search summary only].
 S12 "faces of the convex hull of rank-constrained elliptope "rank at most k" correlation matrices simplicial faces …" →
    nothing beyond Tropp, Saunderson et al., E.-Nagy–Laurent–Varvitsiotis [search summary]; opened abs 1205.2040 [abstract]:
    egd(G) = smallest r such that every G-partial matrix completable to a correlation matrix has a completion in the convex
    hull of correlation matrices of rank ≤ r (a statement about PROJECTIONS, unit-diagonal constraints).

### 18:04 UTC — coordinator's second note received, recorded
* Geometry's third checkpoint f7eed26 (17:55 UTC); object unchanged; keep citing line numbers of geo_ro_d84a43b.
* Their "ensemble rigidity" is renamed "second-moment rigidity" (the Ensemble division's use has priority): in the report use
  the new term once with the old one in brackets.
* New, NOT part of the review: Theorem J (§5.6), a numerical claim that second-moment rigidity is strictly weaker than
  universal rigidity (§8.2).  They have not read SCI-RES-0029; Item 3(c) stands as briefed.
* My own read-only check of the third export: see the hashes/diff printed at 18:04 (recorded below).
  Result: sha256 of §2 and §4.2 identical in geo_ro_d84a43b and geo_ro_f7eed26 (c679…, 14da…); §7.2 differs in exactly one
  line, the title of Theorem G ("global quantitative ensemble rigidity" → "global quantitative rigidity of ensembles").

### 18:05 UTC — `t4_fourth_moment.py` → `t4_fourth_moment_v2.log` (9 s; v1 with a 2° window moved to not_cited/: its LP2 column
measured broadening beyond 2°, not competitors — MY choice of window was uninformative)
One differing torsion, grid 360 on each of the two circles (rotations, reflections), true states on the grid:
data <d²> only (control): LP1 = 0 (3/3), data-map rank 5; data <d²> and <d⁴>: LP1 = 1.000000 (3/3), rank 9;
LP2 (15° window): 0.77–0.98 at relative ε = 1e-3 … 0.98–0.998 at 1e-5.  So the one-torsion pair, never identified by M,
is identified (on the grid, within the re-hinging family to which Lemma 2.2 still confines competitors because <d²> is
part of the data) once the fourth powers are added — the second harmonic enters (Carathéodory 2-neighbourliness).

### 18:08 UTC — `t3a_below_threshold_images.py` → `t3a_below_threshold_images.log` (68 s): generic pairs below n0(2) = 12
(cos −5/13; 3 instances per n; 600 LM starts): n = 8: continuum of images, LP 0 with 9-atom competitors (verified to 3e-12);
n = 9: 6, 6, 8 further images, none carries mass (LP 1); n = 10, 11, 12: only the two states.  Agrees with the Geometry
division's §5.2 and with their Theorem I at 7c2a3d1 (exact at n = 10) — and validates my enumeration against their exact
result.  (They report "4–6 further" at n = 9; I find 6–8: instance-dependent count.)

### 18:10 UTC — paper proof of the two-torsion statement completed (all four components, see report §3.3):
(C): (ρ1 − I)α1 = ρ1(ρ2 − I)β2 with α1 = 1/(1 − e^{−iθ1}) (Re = ½) in b1^⊥ and β2 = 1/(e^{iθ2} − 1) (Re = −½) in b2^⊥;
exactly 8 solutions when θ1, θ2 ∉ 2πZ, b1 ∦ b2 and each segment's edge directions lie on no conic.
D is affine in (ρ1, ρ2, ρ1ρ2) ⇒ alternating sum of the eight D's vanishes identically.
Uniqueness: E[ρ1ρ2] equation ⇒ b(Q3 − Q3^T) = 0 ⇒ (Q3 not symmetric) c_i = c_ii = c_iii = c_iv = 0; E[ρ1] ⇒ (c_vi + c_v R1)e = 0
⇒ c_v = c_vi = 0 unless θ1 = π; then E[ρ2] ⇒ θ2 = π.  So: identifiable if (R1R2)² ≠ I and (θ1,θ2) ≠ (π,π); NOT if θ1 = θ2 = π.

### 18:10 UTC — `t3c_three_torsion_candidates.py` → `t3c_three_torsion_candidates.log` (0.0 s; 0 violations)
Three torsions: each of the 6 spurious candidates of the first triple (G from (ρ1,ρ2)) fails orthogonality on the 4th segment:
smallest defect ‖B4ᵀB4 − I‖_F = 4.62, 0.63, 0.75, 0.64, 1.48 (generic), 0.74 (all half-turns); the two states: ≤ 3e-15.
Facts used in the two-torsion uniqueness proof: rank{I, Q3, R1σ, σR2} = 4, ‖Q3 − Q3ᵀ‖ ≥ 1.6 (generic instances).

### 18:11 UTC — start writing R22_REPORT.md.  Findings list fixed:
critical: none.  major: F1 scope of (CC) / states sharing rigid segments; F2 Theorem G(c)–(d) qualitative, κ ≠ local value;
F3 prior art (Laurent–Poljak 1996 Thm 4.2 via Tropp 2018 Fact 3.1 = Theorem B at d = 1; Fernandez-Granda 2013 = mechanism of
G(b)–(c)).  minor: F4 Lemma 2.2 proof; F5 Theorem B implicit hypotheses + Lean two-block; F6 Theorem B′ compactness/
Tchakaloff/non-spanning; F7 Cor 4.2 converse + K bound; F8 Theorem G slips and weaker hypotheses H1+H2; F9 §8.1 egd
sentence; F10 re-run discrepancies (96 vs 48 witnesses; 1e-13 vs 5.8e-12; 9e-2 vs 7.8e-2; one minute vs 8 s).

### 18:17 UTC — `t2_rigidity_rank.py` → `t2_rigidity_rank.log` (0.0 s; 0 violations): the rigidity matrix of E0 (bonds + 1–3) has
full row rank 2n−3 on random, planar (zigzag, 0/π), helical and all-cis chains, n = 6, 14, 30, cosines −1/3, −0.95, 0.5;
control with bond angle π − 1e-9: smallest singular value 2e-33.  ⇒ no singular states for chains; C smooth everywhere.

### 18:12–18:25 UTC — report written (`docs/science/workstreams/R22_REPORT.md`), then every number in it checked against
the logs; corrections made: "7 times" → 6.6; φ ≤ 5e-28; defect ≤ 4e-15; LP2 values of the three-torsion rows; d_P² ≥ 1.3;
residual ≤ 3e-13; demix weights 1e-15…5.8e-12; reading level of the Alfakih sentence ([summary]); no journal/year invented
for Longinetti–Sgheri–Sottile (arXiv id only); constant 4√n; proof of R22-1(c) restated with γ, δ.

### 18:20 UTC — `t3c_dual_certificate.py` → `t3c_dual_certificate.log` (10 s; 0 violations)
Dual LP on the grid of all re-hingings: maximise t s.t. f = c0 + <Λ,D>, f(X1)=f(X2)=0, f(x_g) ≥ t·min_k d_P², |Λ_ij| ≤ 1.
two torsions: t* = 0.311, 0.635, 1.133 (‖Λ‖₁/t* = 482, 236, 242) while φ (same normalisation) has growth −2e-14…−4e-14 (= 0);
three torsions: t* = 0.753 (φ: 0.055); controls one torsion and two half-turns: t* = 0.  ⇒ a linear certificate beyond φ
exists numerically for two torsions (on the re-hinging family); request 5 refined (Σ_j φ_{S_j} for the segments + this).

### 18:21–18:30 UTC — second pass over the report: F1 table (rows "four consecutive", "(z has affine rank 5)" for (j, j+1),
"four or more with long enough segments"); replacement texts added for F5, F8 (hypotheses), F9; [H] label; the dual-side
paragraph in §3.3.

### 18:23 UTC — `t6_d1_dictionary.py` → `t6_d1_dictionary.log`: for d = 1 with star constraints dim N(z) = r(r+1)/2 − rank Z and
(CC) ⇔ Z full column rank in 20 of 20 random families of sign vectors (r = 2…6): the dictionary behind finding F3 holds.

### 18:24 UTC — report final (docs/science/workstreams/R22_REPORT.md).  Hand-back follows.  Tool actions declined: none.
State for a successor: everything is in this file and in the report; all scripts re-run in < 6 min each with
`OMP_NUM_THREADS=1 python3 -B <script> > <log>`; `rerun_copy/` and `not_cited/` are not to be committed.
