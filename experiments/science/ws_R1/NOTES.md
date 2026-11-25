# Workstream R1 — notes (SCI-REV-0001, review of theory report §11.25 "slices")

Running log, appended after every step. Newest at the bottom.

## Step 0 (start)
- Read `docs/science/workstreams/COMMON.md` and `R1_brief.md`.
- Repository at theory head `5ed4072`; my writable locations: `experiments/science/ws_R1/`, `docs/science/workstreams/R1_REPORT.md`.
- Section under review: `docs/THEORY_REPORT.md` §11.25 starts at line 5792 (file is 569 kB).
- Plan: (1) read §11.25 statements only, restate; (2) attempt own proofs + own numerics BEFORE reading
  their proofs / their check scripts; (3) read their proofs and compare; (4) read Lean file; (5) headline audit
  (README vs Cor 11.91; dependence on 11.78/11.79); (6) originality search for Lemma 11.89; (7) report.

## Step 1 — read §11.25 (lines 5792–6103), statements listed
Numbered statements: Lemma 11.89 (odds ratio), Theorem 11.90 (a)(b)(c) + table of numbers, Remark (softly pinned type),
Corollary 11.91 (+ (i),(ii),(iii)) + "what the corollary does not say", Remark (q>=3 letters), Theorem 11.92 (a)(b)(c),
Lemma 11.93 (i)(ii), Conjecture 11.94 (i)-(iii).
(I saw the authors' proof of 11.89 while reading the section top; I then derived my own proof by a different route — below —
before studying theirs in detail.)

### Own proof of Lemma 11.89 (different route from the authors') — to be checked numerically
Ising coordinates: T(b,x) ∝ exp(J b x + h1 b + h2 x), b,x=±1, log odds ratio = 4J = 2s, J = s/2.
1. Fix the marginals (p,q) and move along the fibre of tables with these marginals, parametrised by J'∈[0,J].
   dI/dJ' = Σ Ṫ ln T (marginal terms vanish) = J'·dm/dJ', m := E[BX].  So I_{p,q}(J) = ∫_0^J J' m'(J') dJ'.
2. Tables with fixed marginals: T = T0 + c·(bx); m = m0 + 4c; d(4J)/dc = Σ 1/T  ⇒  dm/dJ = 16 / Σ_{bx} 1/T_{bx}.
3. Σ 1/T = Z(J,h)·Z(−J,h) = 4[A² + B² + 2cosh(2J)·AB], A = cosh(h1+h2) ≥ 1, B = cosh(h1−h2) ≥ 1
   ≥ 16 cosh²J, equality iff h1=h2=0.  (Equivalently AM–GM: (ΣT)(Σ1/T) ≥ 4(ψ^{1/4}+ψ^{-1/4})², ψ = odds ratio.)
   ⇒ dm/dJ' ≤ sech²J'.
4. I_{p,q}(J) ≤ ∫_0^J J' sech²J' dJ' = J tanh J − ln cosh J = K(J) = K(s/2).  Equality iff uniform marginals (or J=0). ∎
Reformulation: "among 2x2 tables with given odds ratio the harmonic mean of the four cells is largest for the
symmetric table" + the thermodynamic-integration identity dI = J dm at fixed marginals.
Generalisation: for P_s ∝ a_b c_x exp(s w(b,x)), I(s) = ∫_0^s s' ρ(s') ds' with ρ = residual variance of w after
projecting out additive functions a(b)+c(x) in L²(P_{s'}) (Schur complement of Fisher information) along the
fixed-marginal fibre.  For k≥3 the maximiser of ρ changes with s' ⇒ no single extremal table (consistent with the
authors' remark that the comparison fails for q≥3).  TODO: verify numerically; see if a clean k-letter bound follows.

## Step 2 — own numerics for Lemma 11.89 (`lemma_1189.py` → `out_lemma_1189.txt`; `lean_against.py`)
- A.grid: 9 938 940 tables ((p,q) on a 407×407 grid incl. 1e-9, 1e-6, 0.499, 0.5, 0.501; 60 values of s∈[1e-4,12]),
  float64: zero violations beyond rounding (max I/K = 1+1.4e-12 at the uniform table; min(K−I) = −1.1e-15).
  Grid maximiser is the uniform table for every s.  (First version had a cancellation bug in the Plackett
  discriminant for large odds ratios; rewritten as a sum of non-negative terms.)
- B.random (mpmath, 60 digits, Ising coordinates, 6 regimes × 3333 trials): max (I−K)/K: generic −2.9e-4;
  odds→1 −7.5e-3; odds→∞ −2.4e-3; marginals→0 −0.9997; near-uniform −1.5e-21; lines where cells coincide −4.4e-7.
  No violation.
- B.limits: s→0 ratio I/K → 16 p(1−p)q(1−q) (matches to 1e-8); s=200 at fixed marginals (700 digits): I → maximal-coupling MI ≤ ln2;
  marginals 1e-3…1e-30 at s = 0.5, 2, 8: all below K.
- C.channel: 2688 asymmetric binary channels at fixed odds ratio: capacity (golden section and textbook closed form agree
  to 4e-13) ≤ K(s/2); max (C−K)/K = 1.8e-11 (rounding, at the symmetric channel).
- P.proof-steps (referee's proof): dI/dJ = J dm/dJ (err 4e-62), dm/dJ = 16/Σ(1/T) (2e-60), Σ(1/T) − 16cosh²J ≥ 0.15 > 0 on
  300 random non-uniform tables, closed form Σ1/T = 4[A²+B²+2cosh(2J)AB] (3e-61), quadrature ∫J'm' = I (5e-61).  ⇒ my proof stands.
- E.equality: I(uniform)=K to 1e-55; Hessian of I in (h1,h2) at h=0 negative definite for J = .05…4 (strict local max).
- `lean_against.py`: the parenthesis "(the capacity-achieving input of an asymmetric channel leans against the channel's bias)":
  TRUE for the joint-law field (−h2 < h1* < 0 in all 30 cases, as the authors' step (5) says), but the INPUT MARGINAL leans
  the other way: for h2>0, E[B] > 0 in all 30 cases (the optimal input favours the more reliable symbol, as for the Z-channel).
  ⇒ minor finding (wording): "leans against" is true only in the Ising-field coordinate, not for P(B).
VERDICT so far: Lemma 11.89 TRUE; I have an independent 4-line proof (thermodynamic integration + AM–GM).

## Step 3 — read §11.23 (definitions, Thms 11.76–11.80, Prop 11.81–11.82, Conj 11.83) and README item (x)
Definitions: block profiles μ (fractions λ_j, densities μ_j), MI(μ)=h(μ̄)−Σλ_j h(μ_j), dist=Σλ_j|ν_j−μ_j|, α=MI+I(μ̄);
r_μ(e)=min{MI(ν): u·dist+λ(ν̄) ≤ e+α(μ)}, R_λ=sup_μ r_μ; n_μ(X)=min{MI(ν): MI(ν)+u·dist+v(ν̄)−α(μ) ≤ X}, N=sup_μ n_μ.
Paper re-derivation (mine) of Thm 11.90:
 (b) on a two-block ray everything is 1-dimensional: r = F((ℓ−(e+F(ℓ))/u)_+), maximised at F'(ℓ*)=u ⇒ F((Ψ(u)−e)_+/u);
     game form by Legendre duality with multiplier s=tu ≤ u; N: Lagrangian with τ=η/(1+η).  ✓ (my derivation agrees.)
     Edge: for e < −F(ℓ_max) no shell is feasible, "game form for all real e" then compares −e with sup over empty set.
 (c) the ray of a centre (m,κ) IS the fixed-marginal fibre of 2×2 tables (block marginal m, letter marginal κ), and
     Ψ''_{m,κ}(s) = dℓ/ds = 4/Σ(1/T) ≤ ¼ sech²(s/2) = Ψ_c''(s)  (my AM–GM step).  So D=Ψ_c−Ψ_{m,κ} is CONVEX with D(0)=D'(0)=0,
     which gives D(tu) ≤ tD(u) at once — stronger than, and independent of, Lemma 11.89 (curvature domination).
 (a) Lagrangian linear in the law ρ of block densities ✓ for e ≥ 0.  GAP for e<0: feasibility E_ρKL ≥ −e is a second linear
     constraint ⇒ extreme points have up to THREE atoms; the text's "mixture of two-point laws" ignores this.  Fix: three-atom
     vertices have zero budget ⇒ value −e, which two-block shells attain for −e ≤ h(κ).  So (a) survives; proof needs the patch.
 Strictness claim "strict inequality for κ≠½ wherever the right side is positive": false for e ≤ −K(u/2) in the game form
     (both sides = −e); fine for e > −K(u/2).
Corollary 11.91: inequalities r_μ(e) ≤ r^κ_μ(e+(I−λ)(κ)) ✓ (restriction of exits; feasibility same condition ✓).
 Reading as exponents: all three "never exceed the cube" readings need Thm 11.78(b) (isoperimetry, unrefereed) —
 hinted exponent of symmetric instances; non-adaptive exponent via 11.79(c) (which uses 11.78(b)).
 NOT covered: (1) adaptive algorithms without a hint over the class (cube: R_unif by §11.19; here only θ* ∈ [R_H, θ_na], θ_na ≤ θ_na^cube > R_unif);
              (2) hinted cost at NON-symmetric instances (O4 conjecture: H hardest among all instances).
 README (x) bold headline: "no known part that depends … only through one order parameter … makes certification harder than no
 known part at all, and an interaction without a field changes no exponent" — unqualified; the open items are listed afterwards
 but the bold sentence is broader than Cor 11.91.  "changes no exponent": the adaptive-no-hint exponent IS an exponent of the
 theory (R_unif on the cube) and is not known for any interacting known part.
 Unconditional direction: R_H ≥ R_unif for symmetric convex I (so at least as hard) via Thm 11.78(a) lower bound (every n).
 TODO: check GameFunction hypotheses for sup_m F*_{m,κ} (sup of concave functions need not be concave) — Conj 11.94(ii).

## Step 4 — own numerics for Theorem 11.90 (`thm_1190.py`; outputs `out_thm_1190.txt`, `out_thm_1190_closed.txt`)
(machine heavily loaded by other workstreams: load average 12–17 on 4 cores; one run killed at the 10-min limit; grids reduced.)
- defs: m=κ=½ reproduces the cube (Ψ=ln cosh(s/2), V=R_unif, N=θ_na^cube) to 1.4e-15; Ψ by table closed form vs the dual
  formula min{mΛ_κ(θ1)+(1−m)Λ_κ(θ2): θ1−θ2=2s}: 1e-15 on 300 random (m,κ,s).
- 11.90(b), 24 centres (m,κ,u), brute force = scan of shells with exits unrestricted on the ray, no duality:
  |V_brute − V_closed| ≤ 1.2e-16 (e ≥ 0); |V_brute − V_game| ≤ 2.8e-9 incl. 70 negative accuracies (down to e < −F(ℓ*), value −e);
  |N_brute − N_closed| ≤ 6.1e-8; |N_closed − N_game| ≤ 8e-7.   ⇒ (b) REPLICATED.
  Two bugs of MINE on the way (recorded honestly): (1) I first scanned the whole ray incl. ℓ<0 and got V_brute ≫ V_closed
  (0.1439 vs 0.0201 at m=.83, κ=.166, u=4): the half ℓ<0 belongs to the antipodal centre 1−m — checked: V_brute(ℓ≤0) = V_{1−m,κ}
  to 2e-16.  The statement "(b) for a centre of type m, the suprema over its shells" is correct only with "shells" = ℓ ≥ 0;
  the text's "the profiles of type κ form one ray" hides that the block structure (m,1−m) carries two centres. Harmless for sup_m.
  (2) for X=0 my root finder returned the shell itself as end of the feasible interval (φ(ℓ)=0) ⇒ N_brute = F(ℓ_hi); fixed by
  bracketing from a minimiser of φ.
- 11.90(c): 270 400 grid points (u ∈ {.25,1,3,8}, 52×52 (m,κ) incl. .499/.501, 25 t): min gap F*_c − F*_{m,κ} = 6.2e-10 > 0
  (at u=.25, m=.499, κ=.5, t=.02); exactly 0 (1e-13) at m=κ=½.  Near equality the gap is quadratic, positive definite:
  gap/(dm²+dκ²) → 0.1439 (direction m), 0.1439 (κ), 0.0774 (m=κ diagonal), 0.2104 (anti-diagonal) at u=1, t=.5.
- curvature domination (my strengthening): Ψ''_{m,κ}(s) ≤ Ψ_c''(s) on 4000 random (m,κ,s): max diff −1.4e-5 < 0; identity
  Ψ'' = dℓ/ds = 4/Σ(1/T) to 1e-7 (finite differences).
- TABLE (u=1, e=0): all six rows reproduced to the printed digits:
  κ=.5: .029139 (m=.500) .110944 | .45: .028856 (.477) .109898 | .4: .028005 (.454) .106755 | .3: .024588 (.408) .094080 |
  .2: .018842 (.362) .072574 | .1: .010688 (.316) .041588.   Best centre type strictly between κ and ½ ✓.
  Extra (not in the text): the best centre for N^κ(0+) differs from the one for R^κ(0): m_N = .471,.442,.383,.325,.266.
  u=2: R^κ(0) = .097281,.096389,.093707,.082861,.064328,.037269; N^κ(0+) = .327813,.325037,.316667,.282567,.223249,.133574.
- sup_m domination on a grid (u ∈ {.5,1,2}, 8 κ, 5 accuracies): R^κ ≤ R_unif, N^κ ≤ θ_na^cube, equality at κ=½ (1e-9), smallest
  strict gap 3.0e-7 (κ=.49).

## Step 5 — Lean file read (`proofs/Frontiers/SliceRefinement.lean`, 153 lines) — not yet compiled (waiting, other builds running)
Declarations: `sum_mem_bracket`, `bracket_width`, `argmax_deficit_le`, `deficit_ge`, `mean_le_of_biregular`. No `sorry`, no axioms in the text.
Match with Thm 11.92: (a) Lipschitz property of class means = `mean_le_of_biregular` + (NOT formalised) the biregular one-flip graph between
adjacent type classes; d_t ≥ J_t − V_n(t) = `deficit_ge` in multiplicative form (✓ I re-derived the log form).
(b) validity `sum_mem_bracket` — lower end in Lean is p_k L_k (k the arg max of p U), the paper returns max_t p_t L_t (tighter, also valid);
width `bracket_width` ✓; "refined only if d_t ≤ x_{l−1}" = `argmax_deficit_le` with hypothesis U_k ≤ c·A_k ✓.
NOT formalised (the file says so): the procedure itself (loop, termination, the invariant, intersection of brackets), the failure
probability (n+1)mδ′, the cost bound Σ_tΣ_l C_t(x_l), all of (c).  No vacuity: hypotheses are satisfiable, conclusions non-trivial but
each is a 3–4 line calc.  "Deterministic core" is a fair description; "(b) [V]" would not be.
GameFunction (GamePair.lean:515): cont on [0,1], F0=F1=0, F ≤ L(1−t), F ≤ E t, E sharp, E>0 — NO concavity needed ⇒ sup_m F*_{m,κ}
is a game function (checked the five fields by hand) ⇒ Conj 11.94(ii) parenthesis is right.  Pair identity also elementary:
N(X) = min{θ : R(X−θ) ≤ θ}.

## Step 6 — multi-block test of 11.90(a) (`thm_1190a_blocks.py`): quick run done, full run in background
Inner solver: KKT clipping root-finding; every value sandwiched dual ≤ min ≤ primal (gap ≤ 6e-17); independent SLSQP agrees to 7e-16
(40 random profiles, k = 2..5).  Quick outer search (4 starts, k=3,4,5): best k-block values = two-block sup to 9 digits for
(κ,u,e) = (.5,1,0): .029139139; (.3,1,0): .024587500; (.3,1,e=−0.03): .041619952 (two-block .041619950 from a coarse m-grid — fixed);
n at (.3,1,X=0): .094079843.  No k-block profile beats two blocks.

## Step 7 — three letters / Potts remark (`potts_three_letters.py` → `out_potts_three_letters.txt`): ALL REPLICATED
- thresholds: I_2=I_3 at s=0.519366, I_3=I_4 at s=1.335309 (claimed 0.5194, 1.3353); (extra) I_4=I_5 at 1.841601.
- second order I_k ≈ s²(k−1)/(2k²) ✓; third order (k−1)(k−2)/(3k³) (extra).
- max over BOTH marginals, q=3,4,5, 30–40 restarts, 11 slopes: always the uniform law on k*(s) letters; excess over max_k I_k ≤ 7e-16.
- integral identity tΨ(u)−Ψ(tu) = tu∫ I/s² for 12 random (a,c,u,t), q=3: 5e-16.
- R_k(0): u=.5: .007673, .007425, .006552; u=1: .029139, .030654, .028405 — game form = closed form = sup–min over shells ✓ (claimed digits).
  Crossings: R_2=R_3 at u = ln 2 (to 1e-12), R_3=R_4 at u = ln 6 (1e-12); mismatch fractions 2−log₂3, log₂3−1 ✓.
- (mine) second order: I(s) ≈ (s²/2)·Σ_{jk}Σ^a_{jk}Σ^c_{jk}; max over marginals = 1/4 (two letters) for q=3,4; uniform ternary 2/9.
- (mine) finite n, exact sums, u=.5, ε=1: ln(evals)/n certified by balls: ternary cube .008425/.007575/.007446/.007428 vs binary slice ½
  .008658/.007835/.007694/.007676 at n = 2e3/2e4/2e5/2e6.
LOGICAL STATUS of "a known part can make certification harder" (q≥3): both numbers are LOWER bounds from single-centre sets.
"Harder" needs an UPPER bound for the uniform ternary cube (its hinted exponent ≤ R_3) — the report itself calls larger alphabets
"a sketch" (§11.20 remark (4), §11.18 "not worked out").  So the remark compares lower-bound functions; fine as [N], but the bold
sentence is not established as a statement about complexity.  My small-u check: in the Gaussian regime the best direction for a
ternary block is (2,−1,−1) (ratio |v|₁²/|v|₂² = 8/3 < 4·... two-letter direction (1,−1,0) gives 2), coefficient 1/9 vs binary 1/8 ⇒
the ordering at small u is robust at second order under any single-letter structure.

## Step 8 — COORDINATOR MESSAGE received (about 18:45, after Step 7 was written)
Theory division published checkpoint 89ac710 (read-only at scratchpad/thy_ro): the remark "more than two letters" of §11.25 was
corrected (k=4 numbers were single dips on letters, not the uniform four-letter site; "hardest known part = uniformly weighted
sub-alphabet" false near the threshold; D52 item 7); three-letter statement now Prop 11.103(d) in new §11.26.  11.89–11.93 unchanged.
Asked: (i) review the remark as it now stands, say which version each finding refers to; (ii) say explicitly whether I had found the
corrected error; (iii) originality: A1 found Lemma 11.89 in Hasenclever–Scholz arXiv:1302.6161, Prop 8(a).
HONEST STATUS re (ii) at the time of the message: I had NOT found the k=4 error.  What I had (Step 7, written before the message):
 (1) replication of all numbers of the old remark AS VALUES OF THE SINGLE-CENTRE FORMULA (my script calls them "single-centre shells");
 (2) the logical objection that these are lower bounds only and that "harder than no known part" needs an upper bound for the
     uniform k-ary cube that the report does not have;
 (3) a second-order criterion (best direction v maximises |v|₁²/|v|₂² over zero-sum v) that I had applied to q=3 only.
 After the message: criterion (3) at q=4 gives v=(1,1,−1,−1), ratio 4 > 3 (single letter (3,−1,−1,−1)) ⇒ coefficient 1/8 = binary:
 the uniform four-letter site is a product of two uniform bits, so it contains the binary cube as a quotient and is at least as hard
 as the binary cube for every u.  So R_4(0)=0.006552 (u=.5) cannot be "the uniform 4-ary cube's exponent" (≥ 0.007673).  This is
 a confirmation obtained AFTER being told, from a tool I had built before; not an independent discovery.

## Step 9 — full multi-block run finished (`out_thm_1190a_blocks.txt`, 613 s) + X=0 check (`thm_1190a_x0_check.py`)
150 random profiles: duality gap ≤ 1.8e-16; KKT vs SLSQP ≤ 7e-14.  11 configurations (κ,u, r/n, accuracy), k=3,4,5, 12 starts each:
best k-block value = two-block supremum to all 9 printed digits, incl. negative accuracies e = −0.03, −0.05, −0.1
(values .041619952, .059049667, .121444088) and n at X = .02, .05.  Single flagged cell: n at X=0 exactly, excess 5e-9 —
shown to be the degenerate accuracy: at X = 1e-8, 1e-6, 1e-4 the excess is ≤ 1.5e-13, and the "offending" profile evaluated at
X = 1e-12 gives .094079262253 < two-block .094079262572.  (N^κ has a square-root cusp at X=0: N(1e-12) = N(0) − 5.8e-7.)
The best 3-block profile has two equal block densities (.143090, .143090, .552343; weights .1397+.4769, .3834) = a two-block
profile with m = .383 = my m_N for κ=.3.   ⇒ 11.90(a) REPLICATED numerically (R: e≥0 and e<0; N: X≥0).

## Step 10 — after the coordinator's message
- Read thy_ro (89ac710): diff of §11.25 old/new: only (1) status line ("11.78/11.79 refereed 'proved' by R10 as the checkpoint closed;
  report applied at the twelfth"), (2) a note in Cor 11.91(iii) (R10: the junction of Prop 11.81(b) comes earlier for u > 2 — global half
  false as a general statement), (3) the remark on more than two letters, rewritten with a "Correction" paragraph; harness XXI.1–5, 24 mutations.
  New §11.26 (workstream W): Thms 11.95–11.101, Prop 11.102–11.103; Prop 11.103(d),(e) carry the corrected statements.  D52 item 7.
- A1_REPORT §2.1: Lemma 11.89 = Hasenclever–Scholz (arXiv:1302.6161) Prop 8(a); A1's proof by two exponential tilts.
  MY READING: arXiv abstract page [abstract] and ar5iv full text through the fetch tool [full text, machine-summarised; Prop 8 quoted:
  "For all x∈ℝ∖{0}: a) sMutInf_x has exactly one maximum at the origin (y,z)=(0,0). b) lim sMutInf_x = 0"]; x = ln√(odds ratio).
  The fetch summary says the published proof is sketched ("after some calculations").  Journal reference (Open Stat. Probab. J. 2016)
  NOT verified by me (arXiv page lists none).
- My own short search (3 queries): no capacity-phrased version found; Ding–Song–Sun (arXiv:2107.09243, to appear PTRF) [abstract]:
  in ferromagnetic Ising models spin–spin correlations are maximal at zero field — the covariance analogue, any graph.
  One-line analogue for the phi coefficient (mine): φ = sinh2J / sqrt((cosh2h1+cosh2J)(cosh2h2+cosh2J)) ≤ tanh J = Yule's Y.
- `lemma_1189_authors_steps.py`: the authors' six steps verified numerically (40 digits): (1) 4e-40, (2) 2e-40, (3) max T = −5e-6 < 0,
  (4) closed form 3e-40, max(−T−δΔ) = −6e-5 < 0, (5) h1* = −k (1e-44), 0<k<h2, g(k)<δ(h2), dC/dh2 formula = finite difference of the
  directly maximised capacity, max dC/dh2 = −3.6e-4 < 0, (6) ✓.  I also re-derived (1)–(6) by hand: correct, incl. the envelope step
  (the existence of the root δ(h1) = T/Δ needs |T/Δ| < J, which is (4), cited one line later; non-degeneracy ∂²I/∂h1² < 0 gives
  differentiability of the maximiser).
- Lean: verbatim copy of SliceRefinement.lean + `#print axioms` compiles in 18 s (`out_lean_slice_refinement.txt`): all five theorems
  depend only on [propext, Classical.choice, Quot.sound].  Added: satisfiability example, `lower_end_any` (paper's lower end max_t p_t L_t).
- `remark_v2_sites.py` (new version of the remark, Prop 11.103(d),(e), via the vertex-channel formulas of Thm 11.99 taken as given):
  (S1) thresholds u=1: .119499 (uniform 3), .120196 ((.05,.5,.45)), .120115 (2 letters) ✓ brackets 1e-9.
  (S2) uniform q=3,4, u∈{.5,1,2,3}: E,a,h = best equal grouping in all 8 cases; q=4,u=1: E=E_2=.120115, a=a_4=.117993, h=h_2=.029139 ✓;
       q=4,u=.5: h=.007673=h_2 (the old remark's .006552 = h_4 is the single-letter-dip value) ✓ CONFIRMS THE CORRECTION.
  (S3) laws ((1−d)/2,(1−d)/2,d), u=.5: h = .007425 (d=1/3), .007610 (.1), .007673 (.01, .001, .0001) ✓; a_2(.3)=.011125, a_3(.3)=.010582 ✓.
  (S4) h_k = h_{k+1} at e^u = k(k−1), k=2..5 (1e-10) ✓.
  (S5) 171-law grid: uniform hardest for h at u=1 (.030654 vs .030572) and u=2 (.117699 vs .117413) ✓; u=.5 running.

## Step 11 — Corollary 11.91 with all exits (`corollary_1191_checks.py`), first run + a FALSE ALARM of mine
First run: (C2) field p=.3,u=1: sup over binary centres of r_mu(0) with exits of every type = .025034 at (m,a,b)=(.5006,.5381,.1362)
(type .3374); the vertex-channel formula of Thm 11.99 (W) gives h = .025034 as well (independent route — also a two-letter cross-check
of W's formula); slice bound .029139 ✓ = the numbers of "What the corollary does not say".
(C3) CW βJ=1.5 barrier shell x=.29803: r_mu(0) = .0251012 ✓ (neighbours .0249241, .0250572, [.0251012], .0250593, .0249352); I(½)=.1152 ✓.
(C4) equality (ii): antiferro βJ=−2 and ferro βJ=.8, B=0: |r_mu(e) − R_unif(e)| ≤ 1.3e-12 with exits of every type allowed ✓.
(C1) "FAIL": max[r_mu(e) − r^κ_mu(e+(I−λ)(κ))] = 1.9e-6, and a "sharper" solver gave 1.2e-4 in one case.  NOT a counterexample:
my inner solvers returned MI(μ) when no grid point was feasible (profiles with a ≈ b, budget ~1e-3 < grid spacing).  Shown in
`corollary_1191_c1_false_alarm.py`: thinning the slice exit to the contact type gives a feasible exit with MI .000798 < .000921,
and the corrected solver finds .000733.  Solver rewritten (quadrant-wise SLSQP from the profile itself + zooms); rerun in background,
with a new block (C5): the junction of Prop 11.81(b) at u = 1 and u = 3.
LESSON (same as the authors' D49/D51): an inner minimum that is too large makes the outer comparison lie; here it produced a
false refutation rather than a false confirmation.

## Step 12 — a new observation on three letters (after the correction notice; conditional on Thm 11.99's formulas)
`remark_v2_sites.py` (S5) at u=.5: grid maximum of h over 171 three-letter laws = .007675 at (.05,.45,.5) > h_2 = .007673.
`remark_v2_extra.py` (duality brackets 1e-9): h(.05,.45,.5) ∈ [.007675166, .007675167]; h(.02,.48,.5) = .007674567;
h(.1,.4,.5) = .007673370; h(.001,.4995,.4995) = .007672975 — all ABOVE the two-letter cube h_2 = .007672866; h(.02,.49,.49) = .007672224
and h(.05,.475,.475) = .007660173 below.  So at u = .5 (inside the range u ≤ .5194 where the 5ed4072 remark called
"the supremum … is attained on a sub-alphabet, uniformly weighted" true) some three-letter product laws are harder than the binary
cube also at VANISHING accuracy (the theory division's own counterexample, (.05,.5,.45) at u=1, is for the threshold E).
Excess 2.3e-6 (0.03 %) — small, but with a certified bracket.  Local search for the maximiser running.

## Step 13 — further checks (all own code)
- `ising_pair_generalisation.py`: generalisation candidate.  Ferromagnetic Ising models, n=3..6, 3000 random (J≥0, arbitrary fields):
  the log odds ratio of a pair marginal is maximal at zero field (0 violations, max excess 3e-15) ⇒ with Lemma 11.89 the pair mutual
  information is maximal at zero field (0 violations).  Mixed-sign couplings: 718 and 105 violations.  n=3 is elementary:
  ω = 4J_uv + ln[(cosh2h_w + cosh2(J_uw+J_vw))/(cosh2h_w + cosh2(J_uw−J_vw))].  Status [C]+[N]; related [K, abstract]: Ding–Song–Sun.
- `thm_1192_1193_enum.py`: Thm 11.92(a): ln A_t u-Lipschitz (slack 7e-16), d_t ≥ J_t − V_n(t) (−9e-16), equality at H (2e-15), n=6,8, 120 cases;
  (b): 3600 runs of optimistic refinement (n=8,12,20; random/low/high/alternating valid brackets): 0 violations of validity and of
  "refined only if d_t ≤ x_{l−1}"; width ≤ x_m + ln(n+1); #refinements ≤ Σ_t #{l: x_{l−1} ≥ d_t}.
  Lemma 11.93 (n=10,k=4,n_o=5, all 252 O): (i) 4e-16, (ii) 2e-16; Markov ✓; hypergeometric window mass ≤ δ''/2 in 9 cases ✓.
- `corollary_1191_checks.py` rerun: (C1) PASS: max[r_mu − r^κ_mu] = 1.6e-16, max[r^κ_mu − R^κ] = 1e-17, max[R^κ − R_unif] = −1.7e-7 (142 profiles).
- `remark_v2_extra.py`: local search at u=.5: π = (.04502, .45679, .49819), h ∈ [.007675293, .007675294] (h_2 = .007672866).
- final full rerun of `thm_1190.py` started (thresholds after bug fixes).

## Step 14 — results of the long runs
- `out_thm_1190.txt` (final): ALL PASS (defs; 11.90(b) 24 centres; (c) grid 270 400 pts; equality case; curvature domination; table; sup_m).
- `out_corollary_1191_checks.txt` (final): ALL PASS.  (C2) field: .025034 by direct sup–min at (m,a,b) = (.4994,.1362,.5381)/(mirror), and by the
  vertex-channel formula.  (C5) junction: u=1 equality below βJ*=1.125 and loss just above (βJ=1.1312: −1.2e-5); u=3: equality at
  βJ = 1.56, 1.89, 2.06 (< βJ* = 2.1158), loss at 2.17 (−3.0e-4).
- `junction_scan.py`/`junction_exits.py`: u ∈ {1,2,3,4,6}, e ∈ {0, 0.3Ψ_c(u)}, βJ = 1 + f(βJ*−1), f ∈ {.3,.6,.8,.9,.97}: r_mu(e) = R_unif(e)
  to 1e-15 in all 50 cases — NO early junction.  Exit tables (grid 2001², by exit type): below βJ* no feasible exit of any type has
  MI below R_unif (u=3, βJ=2.0; u=6, βJ=5.0; u=2.5, βJ=1.7); above βJ* (u=3, βJ=2.25) exits of type ≈ .33/.67 win (.171082 < .172831).
  ⇒ I do NOT reproduce the statement attributed to referee R10 in the 89ac710 text ("for larger slopes the junction comes earlier";
  R10's report is not in the checkout).  Unresolved; a concrete (u, e, βJ) from R10 is needed.
- `ceiling_check.py`: (U1) I ≤ s²/8 for 4000 random Potts pairs q=2..6 (max ratio .9958); (U2) F*(t) ≤ t(1−t)u²/8, E, a ≤ u²/8 for 60 random
  Hamming sites q=2..4 (max ratios .9966, .9971, .9920); h_2/(u²/32) = .9993, .9955, .9821, .9325, .7782 at u = .1,.25,.5,1,2;
  h_3/(u²/32) = .9033, .9230, .9504, .9809, .9416.  (U3) pair identity N^κ(e+R^κ(e)) = R^κ(e): 2e-16.
  [P] proof of the ceiling: Hoeffding's lemma (Λ'' ≤ u²/4) with Q = π in min_Q max_φ (1−t)D_t(π_φ‖Q).
- `remark_v2_extra.py` final: local maximiser at u=.5: π = (.04502,.45679,.49819), h ∈ [.007675293,.007675295]; excess over h_2: 2.4e-6.
Now writing R1_REPORT.md.

## Step 15 — report written: `docs/science/workstreams/R1_REPORT.md`
- One more search confirmed the journal reference of Hasenclever–Scholz at snippet level (Bentham Open TOSPJ-7-20, vol. 7 (2016) 20–35).
- Harness XXI.2 read (after my scripts): its multi-block test is for r at e ≥ 0 only (ef ∈ {0, 0.3}), like slice_check1.py → finding m12.
- Authors' numbers for u = 2 (out_slice_table.txt) agree with mine to all digits; their m for a^κ agree with my m_N.
- Findings: 0 critical; 4 major (M1 headline; M2 gap in 11.90(a) for e<0; M3 remark on ≥3 letters at 5ed4072 — not found by me before the
  correction notice; M4 Lemma 11.89 in print); 12 minor.  Unresolved U1: I do not reproduce the early junction attributed to R10.

## File index (all in this directory)
lemma_1189.py, lemma_1189_authors_steps.py, lean_against.py — Lemma 11.89 (statement, my proof's steps, the authors' steps, the parenthesis).
thm_1190.py — Theorem 11.90(b),(c), table; library (Ray, best_centre, R_unif …) used by the other scripts.
thm_1190a_blocks.py, thm_1190a_x0_check.py — Theorem 11.90(a) with 3–5 blocks (sandwiched inner problem), incl. e<0 and N.
corollary_1191_checks.py, corollary_1191_c1_false_alarm.py, junction_scan.py, junction_exits.py — Corollary 11.91 with exits of every type.
potts_three_letters.py — the remark at 5ed4072; remark_v2_sites.py, remark_v2_extra.py — the remark at 89ac710 / Prop 11.103(d),(e).
ceiling_check.py — universal ceiling t(1−t)u²/8; slice pair identity.   ising_pair_generalisation.py — many-spin conjecture.
thm_1192_1193_enum.py — Theorem 11.92(a),(b), Lemma 11.93.   SliceRefinement_copy_axioms.lean — Lean copy + axiom audit.
out_*.txt — outputs of the final runs.
