# R5 notes — review SCI-REV-0005 of theory report §11.26 (Theorems 11.99, 11.101)

(Running log; newest entries at the bottom.  Object under review: `thy_ro` = read-only theory checkout at 89ac710.)

## Step 0 (start)
* Read COMMON.md and R5_brief.md.  Created this directory.
* Plan: (1) read §11.26, THY-MSG-0011, THY-REQ-0011, W_REPORT §5, D52; (2) write OWN numerics for the site
  function / Rényi capacity / E_0 / sphere packing BEFORE reading wv_lib.py; (3) re-derive identity;
  (4) go through the transfer against §11.16–11.20; (5) read RenyiCentre.lean; (6) report.

## Step 1 — first reading (statements only; authors' code NOT read yet)
Read: THEORY_REPORT §11.26 (l. 6138–6417), THY-MSG-0011, THY-REQ-0011, W_REPORT §0–§5 (l. 1–700).
Definitions I extracted (to implement from scratch):
* site (π, d): L = {γ : γ(a) − γ(b) ≤ d(a,b)} ("first argument = point where ψ may be larger"), V = vertices of L/ℝ,
  π_φ ∝ π e^{−φ}.
* game K(a,φ) = (π_φ(a)/π_γ(a))^t; val = min_M max_a (KM)(a) = max_Q min_φ (QK)(φ); F(γ,t) = −ln val; F*(t) = max_{γ∈L} F(γ,t).
* claim 11.99: F*(t) = max_M −t ln Σ_a(Σ_φ M π_φ(a)^t)^{1/t} = min_Q max_φ (1−t) D_t(π_φ‖Q) = (1−t) C_t.
* R̂(e) = max_{0≤t≤1}[F*(t) − te]; S(e) = e + R̂(e); θ_na = R̂∘S⁻¹ = max_{τ<1}(F*(τ) − τx)/(1−τ).
* E = sup F*(t)/t, a = sup F*(t)/(1−t), h = R̂(0).  Several types: F* = Σ λ_j F*_j at a common t.

Hand re-derivation of the identity (done before any code; details go to the report):
* For any M: max_a Σ_φ M(φ)(π_φ(a)/π_γ(a))^t = max_a (m_M(a)/π_γ(a))^t ≥ (Σ_a m_M(a))^t because π_γ is a probability vector
  (weighted mean ≤ max).  Hence val ≥ min_M (Σ m_M)^t and F(γ,t) ≤ max_M −t ln Σ m_M for EVERY γ (even outside L).
* Equality at π_γ* = m_{M*}/Σ m_{M*}; γ*(a) = −(1/t) ln Σ_φ M*(φ) e^{−tφ̃(a)} ∈ L because each φ̃ ∈ L (soft-min closure):
  Σ_φ M e^{−tφ̃(b)} ≤ e^{t d(a,b)} Σ_φ M e^{−tφ̃(a)}.  ✓.
* −t ln Σ_a(Σ_φ M π_φ^t)^{1/t} = (1−t)·I_t^{Sibson}(M; W), W(a|φ) = π_φ(a), D_t(P‖Q) = (t−1)^{-1} ln Σ P^t Q^{1−t}, natural logs.
  max_M I_t^{Sibson} = min_Q max_φ D_t(W_φ‖Q) (Sion; Σ_φ M Σ_a W^t Q^{1−t} linear in M, concave in Q).  ✓
  (At the level of capacities Sibson = Augustin = Arimoto [Csiszár 1995, from memory]; at fixed M they differ.)
* E_0(ρ, M) := −ln Σ_a(Σ_φ M W^{1/(1+ρ)})^{1+ρ} = ρ I^{Sibson}_{1/(1+ρ)}(M;W); so F*(t) = t·max_M E_0(ρ,M), ρ = (1−t)/t.  ✓ (algebra)
* θ_na(x) = sup_{ρ>0}(E_0(ρ) − x)/ρ = inf{θ : E_sp(θ) ≤ x}, E_sp(θ) = sup_{ρ≥0}[E_0(ρ) − ρθ]: algebra, needs no concavity.  ✓
  R̂(e) ≤ θ ⟺ e ≥ E_sp(θ) − θ.  ✓ (shear law is algebra once R̂ and θ_na are what the theorems say.)
* Crossing e^u = k(k−1): with c_k = ln((e^u+k−1)/k)/u (the optimal match fraction), h_k = ln k − H_b(c_k) − (1−c_k) ln(k−1);
  at e^u = k(k−1): c_k + c_{k+1} = 1 and h_k − h_{k+1} = 0 exactly (hand computation).  ✓ [P, mine]
  To check numerically: uniqueness of the crossing, t* ∈ [0,1].
Next: own code r5lib.py (vertex enumeration, LP game value, Rényi capacity by three routes, E, a, R̂, θ_na).

## Step 2 — own implementation (r5lib.py), written before reading wv_lib.py; first results
* r5lib.py: brute-force vertex enumeration of L/ℝ; LP game value (HiGHS, tolerances 1e-10, value re-evaluated from the
  returned strategy); primal Rényi programme (SLSQP + analytic gradient, gradient derived by hand:
  ∂G/∂M(φ) = −exp(G − (1−t)D_t(π_φ‖Q_M))); dual epigraph programme min_Q max_φ (1−t)D_t; E by the geometric-mean
  programme with KL(Q‖π_φ) certificate; a by Blahut–Arimoto with max_φ KL(π_φ‖Q) certificate; R̂, θ_na by grid+Brent.
* NUMERICAL TRAP (mine, caught): first version — blind Nelder–Mead over γ of the LP value EXCEEDED the Rényi value by
  2–3.5e-9 on path/asym.  Cause: HiGHS default feasibility tolerance (1e-7) → LP optimum noisy at 1e-9 and a maximiser over γ
  picks the positive noise; also my SLSQP had no analytic gradient (duality gap 2e-8).  After tightening both:
  blind − primal ≤ 6e-16 everywhere.  NOT a counterexample.
* t01_identity.py (out/t01_identity.txt, 309 s): 20 cases on bin/path/tri/asym at t = .1,.3,.5,.7,.9:
  blind LP search = primal = dual = LP at the Rényi centre to 4e-14; centre always in L; 36 random asymmetric sites
  (q = 2,3,4): 9e-13, centre in L always, blind never above.  F(γ,t) ≤ F*(t) also for 1600 random γ outside L (largest
  difference −3e-7 < 0).  Gallager's raw E_0(ρ,M) = G_t(M)/t to 5e-16.
  Vertices: bin 2, path 4, tri 6, asym 5 — as in W_REPORT §6.1.
* t02_reference_numbers.py (out/t02_reference_numbers.txt): all 6 chains × (E, a, h, R̂(0.3E), θ_na(0.3E), R_0(0)):
  largest |mine − theirs| = 5.0e-7 = rounding of their 6-decimal table.  path: E=0.400622034, a=0.294791205,
  h=0.089589 (t*=0.4601), R̂(0.3E)=0.043375, θ_na(0.3E)=0.066899057 (both by sup formula and by R̂∘S⁻¹, diff 1e-15),
  R_0(0)=0.080032; centre law (0.4734,0.2456,0.2810), γ*=(0,0.1454,−0.3946), M*=(0.5039,0.4961) on the two end dips. ✓.
  cut/pair for path: 0.048586 / 0.115369 ✓.

## Step 3 — read the two-letter proofs and the transfer; Lean; more numerics
* Read THEORY_REPORT §11.16 (non-adaptive, cube), §11.18 (Thm 11.52 one more level; 11.53 recursion; 11.54), §11.19 (11.56–11.58,
  bounded accuracy), §11.20 (11.59–11.65, Lemma 11.62, Thm 11.63, 11.64 with repairs M1/M2), §11.21 (Thm 11.66, GamePair),
  §11.23 (11.76–11.80), Thm 11.22, 11.27, 11.28; F_REPORT §3.4–3.6 (Lemma T, Lemma SL, six steps of F6, F7, F8, F9);
  W_REPORT whole; D52; RenyiCentre.lean; GamePair.lean (structure GameFunction, pair, exactRec_*), HintRecursion.lean
  (HintPair, StepLE, iterates_lt_hint_add).
* Step-by-step re-derivation of W2(a), Lemma T′, W2(b) Steps 1–6, W2(c), W3(a), W3(b) (upper bound, vertex reduction, attained,
  consequences τ ≤ 1 / τ ≥ 1, window step), W3(c)–(e), W4.0, W4 (i)–(iii): all steps check out on paper (details → report §2).
  Things I found on the way (to be classified in the report):
   - Hoeffding step of W2(b) Step 4: "all within nδ₁·max(D_max,1)" is sloppy; with counts within nδ₁ and the cost within
     nδ₁D_max the stated bound B − δ follows (constant fine).  minor.
   - Lemma T′ needs ρ_j of full support; applied with ρ_j = P_j (joint type of the piece) which may miss letters → restrict
     alphabet.  minor.
   - 11.99 "why sphere packing" sentence: "truncating the cone removes the rest, whose Gibbs mass is exp(−n min{D: I ≤ θ})" —
     garbled: exp(−n·min{D(V‖W|M): I(M,V) ≤ θ}) is the Gibbs mass of the SEEN outputs (what remains), not of the rest.  minor.
   - dictionary "adaptive certifies E_sp(θ) − θ": only for 0 < θ < h (fixed point); for θ ∈ [h, a) the expression is ≤ 0.
   - recursion start: with enumeration base T₁ ≡ Σλ_j ln q_j the Lean theorem that applies is `iterates_lt_hint_add` (hbdd: any
     bound C) + `GameFunction.pair`; `GameFunction.exactRec_tendsto` is for T₁ = θ_na.  citation imprecise, harmless.
   - GameFunction (Lean) has NO concavity hypothesis: cont, F0=F1=0, F ≤ L(1−t), F ≤ Et, E sharp, E>0.  ✓
   - 11.27(c)/W4.0 product step with several site types is a paper step (Lean: identical sites as nested pairs).  Label
     "P from machine-checked pieces" is accurate.  Re-derived by hand: OK.
* RenyiCentre.lean (read; not compiled): scale_le_inv_sum, exists_ratio_le, eq_of_forall_ratio_ge, softmin_admissible.
  Free-standing elementary inequalities about real vectors; no sorry; hypotheses satisfiable.  They cover exactly the two
  steps named.  NOT covered: minimax, game ↔ min_a (P/m)^t, Sibson/Csiszár radius, limits, dictionary, any site definitions.
* t03_dictionary.py (running): cube = BSC(p_u): a, E, F*, h, E_sp(θ)=KL(ρ‖p_u) at KL(ρ‖½)=θ, shear — all to 1e-9.
  path: sup_ρ[E_0(ρ) − ρθ] (raw Gallager) = S(R̂⁻¹(θ)) to 2e-15.
* t04 (running): tri F* not concave (largest second difference +4.9e-6 at t=0.378 on a 0.001 grid; switch
  {dip2, dip0, anti-dip2} → {dip1, dip2, dip0} at t_c=0.37799); three letters Hamming u=1: E = 0.119499 (uniform) <
  0.120115 (cube) < 0.120196 (0.05,0.5,0.45) ✓.
* t06_bruteforce_orientation.py (36 points, two site types, both envelopes asymmetric; 400 random members):
  quotient envelope = transport cost (4e-16); dip formula (4e-16), minimality; fibre averages admissible; tail lemma
  relative to H: 0 violations in 11 485 levels, 8 602 violations with the transposed slack; quantile truncation admissible;
  Z_gΦ_g⁺ ≤ Z_HΦ_H⁺; generalised dips with independent vertex labels (Prop. W4.0): admissible, effect ≥ r, hit probability
  ≤ e^{tr}Πρ^{n_j} (largest ratio 0.91).  ψ_H built with the transposed quotient envelope is NOT in the class (as they say).
  MY BUG, caught: first version counted w = t_P points as "changed" (−ln(exp(−ψ)) ≠ ψ by one ulp) → 330 spurious violations
  of the quantile truncation; fixed with a tolerance.

## Step 4 — results of t03, t04, t04b, t04c, t05, Lean compile
* t03_dictionary.py (out/t03_dictionary.txt, 676 s):
  (A) cube u = 0.5, 1, 2: vertex channel = BSC(p_u = 1/(1+e^u)); a = ln2 − h(p_u), E = ln cosh(u/2), F* = Λ(tu) − tΛ(u),
      h = KL(Λ₁/u‖½), E_sp(θ) = KL(ρ‖p_u) at KL(ρ‖½) = θ, E_sp − θ = uρ − Λ₁ — all to ≤ 1e-9.  NOTE: E_sp(θ) − θ < 0 for θ > h
      (e.g. θ = 0.3a) → the "adaptive certifies E_sp(θ) − θ" statement only makes sense for 0 < θ < h.
  (B) path, asym, mix, mix2 (two site types, common ρ): sup_ρ[E_0(ρ) − ρθ] with raw Gallager E_0 maximised per type
      = S(R̂⁻¹(θ)) to 2.3e-14; θ_na(E_sp(θ)) = θ to 5e-15; E_0(ρ) → E (ρ → ∞), E_0(ρ)/ρ → a (ρ → 0); E_sp(h) = h.
  (C) fixed label law M: Gallager(M) := sup_ρ[E_0(ρ,M) − ρθ] ≤ CK(M) := min{D(V‖W|M): I(M,V) ≤ θ} (primal SLSQP) ≤ E_sp,
      0 violations in 48 random M; strict gap Gallager < CK up to 3.5e-3; equality of all three at M* (1e-15).
      ⇒ convention: for a GIVEN cone label law the exponent is the Csiszár–Körner/Augustin form, not Gallager's fixed-input
      form; they agree only after maximising over M.  The report's statement uses the maximised E_0 — correct.
* t04_beyond_two_letters.py (out/t04_beyond_two_letters.txt, 324 s), t04b_kink.py, t04c_split.py:
  (a) tri: t_c = 0.377987, slope jump +0.005582 (THEIRS: +0.0052 — small discrepancy, 7 %), corner of R̂ at 0.1996E,
      slopes −0.383 → −0.373 ✓; concave envelope − F* up to 6.8e-6; 16 two-letter sites concave (second diff ≤ −6e-8).
      mix2: R^split − R̂ = 7.95e-7 (rel. 2.5e-5) at e = 0.043306 ✓ (theirs 8e-7).
  (b) Hamming q=3, u=1: E = 0.119499 (uniform), 0.120196 ((0.05,0.5,0.45)), 0.120115 (cube) ✓.  F*(tilt) > F*(uniform) for
      t ≤ 0.05 ✓ (their statement), < for t ≥ 0.1.  h, a uniform: 0.030654, 0.123284 ✓.
  (c) u=0.5: h₃ = 0.007425 < h₂ = 0.007673 ✓; u=0.3: a₃ = 0.010582 < a₂ = 0.011125 ✓; laws ((1−η)/2,(1−η)/2,η) → two-letter
      values; crossing of h₂,h₃ at u = 0.693147181 = ln 2 ✓; of a₂,a₃ at 0.519366 ✓; sign of h(near (½,½,0)) − h(uniform)
      flips between u = ln2 ∓ 0.02 ✓.
  (d) uniform Hamming q = 3, 4, u ∈ {.5,1,2,3}: E, a, h each equal to the best equal grouping to ≤ 1e-13; q=4,u=1:
      h = h₂ = 0.029139, a = a₄ = 0.117993, E = E₂ = 0.120115 ✓.  F*(q=4,u=1) = max(F₂,F₄) to 4e-15, switch at t = 0.6458 ✓.
  (e) e^u = k(k−1): h_k − h_{k+1} = 0 to 40 digits for k = 2..8, c_k + c_{k+1} = 1, t*_k + t*_{k+1} = 1, sign + below / − above;
      argmax_k h_k obeys (k−1)(k−2) ≤ e^u ≤ k(k−1) for u = .5,1,2,3,4,6 ✓.
* t05_evaluation_lemma.py 14 (out/t05_evaluation_lemma.txt, 336 s): PRIMAL convex programme for V(μ,B;v) (no games, no t):
  at the generalised-dip profile V = R̂(e) to ≤ 4e-14 for e = 0, .3E, .6E on asym, tri, mix (bin+path) and asym+tri (two
  asymmetric/triangle types, fractions .3/.7) — "one common slope" confirmed by a solver that does not know t;
  191 random (profile, budget) pairs incl. negative e: V − R̂ ≤ −1.8e-3 < 0; perturbed optimal profiles: ≤ −5.5e-4.
* Lean: verbatim copy of RenyiCentre.lean + four `#print axioms` lines, `lake env lean` (no lake build): exit 0, no errors,
  axioms [propext, Classical.choice, Quot.sound] for all four theorems (out/lean_check.txt).
