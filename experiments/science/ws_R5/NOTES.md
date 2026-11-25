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
