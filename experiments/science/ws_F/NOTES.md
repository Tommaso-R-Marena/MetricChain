# Workstream F (science division, second wave) — running notes

Question: does a free exact oracle for the one-body marginals of the Gibbs measure lower the
worst-case query-complexity exponents (adaptive / non-adaptive) of certifying `ln Z` over the
Lipschitz class on the p-biased Hamming cube?

Labels: [V] machine-checked, [P] paper proof here, [K] known+cited, [N] numerics only,
[C] conjecture, [H] heuristic.

## Log

* 2026-11-25 20:07 UTC — started.  Read COMMON.md and F_brief.md in full.  Created this file.
  Next: read INFERENCE_LIMITS.md §§0–4, 13, 14; ADDENDA A1, A8, A10; theory report §11.20,
  §11.26 (thy_ro checkout at 89ac710); R5_REPORT.md §4.1.

* (between 20:07 and 20:20; clock not read at the time) — Read: INFERENCE_LIMITS §§0–4, 13, 14; ADDENDA A1, A7–A10; THEORY_REPORT §11.20
  (lines 4197–4617), Thm 11.22, 11.27; thy_ro §11.26–11.27 (Thm 11.95–11.104); R5_REPORT §4.1.

### First analysis (before any numerics) — hypotheses to TEST

Notation: site laws `π=(q,p)`; vertex channel `W`: `π_0 ∝ (q, p e^{-u})`, `π_1 ∝ (q e^{-u}, p)`
(Gibbs laws of the cones at one site); additive instance `γ`: `π_γ ∝ (q, p e^{-γ})`,
`p_γ = π_γ(1)`; window of one-body marginals of the class `[π_0(1), π_1(1)] = [p_u, p_{-u}]`.

H1. **The excess mass of a dip is carried by the cone law, not by the rim.**  A dip of depth
    `r` at centre `s` on the additive base `γ` has Gibbs law `∝ max(π_γ^n, e^r π_s)`; the excess
    `(e^r π_s − π_γ^n)_+` equals `e^r π_s` up to an exponentially small part (for `r ≥ 0`), so
    its one-body density (after cyclic symmetrisation) is `c_0(m) = mπ_1(1) + (1−m)π_0(1)`
    = `(MW)(1)`, the OUTPUT LAW OF THE VERTEX CHANNEL at input `M=(1−m,m)`.  The type
    `V_φ ∝ π_φ^t Q^{1−t}` of the coordinator's sketch is the type of the RIM (where queries hit
    most cheaply), which carries an exponentially small part of the mass.  [to verify: exact
    type-class sums]
H2. So "self-consistency" would need `M* W = Q*` (Shannon-type identity), which for `t<1`
    is NOT Augustin's fixed point `Q* = Σ M* V_φ`.  Expect `M*W ≠ Q*` for `p≠½`.  [to verify]
H3. **Compensation instead of self-consistency.**  The class is a convex cone in the weights
    and contains the product measures `π_{γ2}`, whose densities sweep the whole window.  For a
    pair `(w, w+Δ)`, `Δ ≥ 0`, both invariant under a transitive group: the one-body marginals
    agree iff dens(Δ) = dens(w).  Adding `b·w̃_{γ2}` to both moves dens(w) to any value between
    dens(w) and `p_{γ2}` WITHOUT changing `Δ` or the set where the pair differs:
    `b = A_w (c_Δ − c_w)/(p_2 − c_Δ)`, exact, no IVT needed.  Then
    - adaptive: base `w̃_{γ*} + b w̃_{γ2}` (a two-component mixture, NOT additive), alternatives =
      base + cyclically symmetrised dip excess of centre type `m*`  ⇒ lower bound
      `(1−2δ) e^{−t r} ρ_t(M)^{−n} / (n(n+1))`, exponent `R^max` unchanged;
    - non-adaptive: pair (truncated cone + b w̃, cone + b w̃), `b ≍ A(truncated)` ⇒ `θ_na` unchanged.
    [to verify: exhaustive enumeration n ≤ 16; type sums; then write proofs]
H4. Instance-wise the oracle DOES help at additive instances that are not self-consistent:
    Jensen with a tilt (`E_{μ'}|x| = n p_γ` ⇒ `E_{π_γ} e^{h+λ(|x|−np_γ)} ≥ A'/A_γ` for all λ) plus the
    tensorised two-reference sandwich (Thm 11.28) should give a strictly lower accuracy
    threshold; derivative in λ at 0 is `(M*W)(1) − p_γ ≠ 0`.  [to verify numerically, then prove]
H5. k ≥ 2: k-transitive group ⇒ k-body matching ⇔ matching the first k factorial moments of
    `|x|` between excess and (exchangeable) base; needs spread of centre types and a
    mixture base; t-designs (Johnson scheme) instead of orthogonal arrays.  Tolerance version
    via random centre sets.  [later]

* (≈20:20, clock not read; the next clock reading is 20:23) — **Coordinator's note received** (after the entry above was written): the theory
  division's THY-RES-0005 (commit 40c5bd7; read by me now with `git show origin/...`, §2 Q2 and
  Q4) accepts SCI-REQ-0001 Q2 and expects "the answer to (a) to distinguish the *class*
  exponent from the exponent *at an instance* — your formulation 'restricted to centres of
  that type' is, we think, the right one at the zero residual and not for the class"; and its
  parameter-counting remark (Q4): "an adversary with as many continuous parameters as there
  are numbers can generically match them, so such oracles lower *worst-case* exponents only if
  the matching is impossible for a structural reason".
  **Provenance record.**  H1–H5 above were written BEFORE this note and before I read
  THY-RES-0005 (derived between 20:07 and ≈20:20 from the brief and the two theory sections alone).  In
  particular: (i) excess mass carried by the cone law `MW`, not by `V_φ` (H1, H2) — mine;
  (ii) the compensation lemma, `b = A_w(c_Δ − c_w)/(p_2 − c_Δ)`, base = two-component mixture (H3)
  — mine; it is an instance of the parameter-counting principle (one number, one continuous
  parameter `b`), which I note as the theory division's general remark and as step (3) of the
  coordinator's sketch; the specific parameter (admixture of a second additive instance to
  BOTH members of the pair) is not in either; (iii) H4 (oracle helps at additive instances,
  by Jensen-with-a-tilt) — mine.
  New task from the coordinator: treat BOTH the class exponent and the instance-wise exponent
  at the zero residual with a field.

* 20:23 (clock read) — **Derivation (mine, after the note): the tilt bound for instances.**  Let `ψ'∈L_u`
  have the same one-body marginals as the additive instance `ψ_γ`, `h = ψ_γ − ψ'`.  Jensen under
  `μ_{ψ'}`: for every real `λ`, `E_{π_γ} e^{h + λ(|x| − n p_γ)} ≥ A(ψ')/A(ψ_γ)`.  Read with the tilted
  reference `π^{(λ)} = Bern(p^{(λ)})^n`, `logit p^{(λ)} = logit p + λ`:
      `ln A_{π^{(λ)}}(ψ') − ln A_{π^{(λ)}}(ψ_γ) ≥ ln A_π(ψ') − ln A_π(ψ_γ) − n c_γ(λ)`,
  `c_γ(λ) = ln(1 − p_γ + p_γ e^λ) − λ p_γ ≥ 0`.  SAME two functions, SAME class, another field.  The
  universal sampler (uniform on types) does not depend on the field, so the hinted isoperimetry
  (theory Thm 11.27 "R^gen is the exponent" / 11.59(a)) at field `θ − λ` gives
      `R^orc_γ(e; θ) ≤ inf_λ R_γ(e − c_γ(λ); θ − λ, u)`,
  derivative at `λ=0` is `−∂_θ R_γ(e;θ)`: nonzero at the zero residual when `θ≠0` (table of §11.20:
  `R_0` strictly decreasing in `|θ|`).  ⇒ the oracle strictly lowers the instance exponent at
  the zero residual with a field; nothing at `θ=0` (consistent with Theorem 4).
  Dual side: profile `P_{UX}` (annular dips), budget shifts by `−λ(P_X(1) − p_γ)`; so
  `inf_λ sup_P ≥ sup_{P: P_X(1)=p_γ}`; time-sharing convexity suggests equality.  To test
  numerically: is the constrained sup attained by plain dips of the forced centre type `m_0`
  ("restricted to centres of that type"), or do annular/soft-label dips do better?

* (by 20:45, clock read 20:45 when these three entries were written) — **N1 done** (`t01_single_letter.py`, `out/t01_single_letter.txt`): my own implementation
  (`sl.py`) reproduces every printed number I tried: closed form of Thm 11.59(b) vs exact 2×2 game
  value `1.5e-14` (2000 random cases); Sibson form vs max over γ `3e-16`; table of §11.20 (u=2,
  θ=0,.5,1,2,3: R_0, R^max, γ*, a) to all printed digits; `R_0(0.3E)=0.019497`, `R^max(0.3E)=0.023270`
  at (0.1,2); `θ_na` = .1020,.0440,.0243; the "bin" row of §11.26 to 6 digits; pair identity;
  constant-composition exponent dual = primal (`5e-15`), `max_m Rcc = R_γ`.
* (by 20:45) — **N2 done** (`t02_fixed_point.py`, `out/t02_fixed_point.txt` once the slow job ends):
  Augustin's identity `Q* = Σ_φ M*(φ)V_φ` holds at the saddle (to 1e-9).  **But the identity that
  matters for the oracle is `M*W = Q*` and it FAILS for p ≠ ½**: gap `(M*W − Q*)(1)` = +0.018
  (p=.3,u=1,e=0) … +0.127 (p=.1,u=2,e=.9E); exactly 0 at p=½.  Plain dips at additive bases with
  the forced centre type lose 13 % (p=.3,u=1,e=0), 43 % (p=.1,u=2,e=0), and **100 %** (exponent 0)
  from e=0.6E (p=.3) resp. e=0.3E (p=.1) on.  ⇒ H1, H2 confirmed at the single-letter level; the
  coordinator's mechanism (self-consistency) is false; within additive bases + plain dips the
  constraint binds hard.
* (by 20:45) — **N5a done** (`t03_enum_adaptive.py`, `out/t03_enum_adaptive.txt`): exhaustive enumeration
  n = 8, 12, 14, 16, eight parameter sets.  Compensated base `w~_{γ1} + b w~_{γ2}` and cyclically
  symmetrised alternative: both in the class (max |ln ratio| ≤ u), **all n one-body marginals
  equal to ≤ 1.4e-13**, separation = ln(1+E/(1+b)) as predicted.  Without compensation the
  marginal gap is 1.4e-2 … 8.2e-2 (oracle separates); a single unsymmetrised dip has marginals
  spread over e.g. [0.105, 0.404] (oracle reveals the centre).  ⇒ H3 (construction) confirmed.
  At these n the packing numbers are trivial, as they must be (exponents 0.01–0.05).

* (between 20:49 and 21:01; clock read 21:01 when the next four entries were written) — **N3 (instance-wise, zero residual)** (`prof.py`, `t04_instance.py`, `out/t04_instance.txt`).
  Three single-letter quantities at the zero residual with the oracle:
  (a) plain dips of the centre type forced by one-body matching, `Rcc(0, m_0; e)`;
  (b) sup over binary-label *annular* profiles `(m, v0, v1)` (dips around a shell, cores in the
      window) with density constraint `(1−m)v0 + m v1 = p`;
  (c) my tilt upper bound `U(e) = min_λ R_0(e − c(λ); θ − λ)`.
  Results (p=.3,u=1): e=0: R_0=.024814 | (a) .021007 | (b) .024157 | (c) .024371;
  e=.3E_0: .012089 | .005667 | .011301 | .011558; e=.7E_0: .002211 | 0 | .001638 | .001826.
  (p=.1,u=2): e=.2E_0: .026849 | 0 | .015441 | .016345; e=.7E_0: .003686 | 0 | 0 | 0.
  (p=.05,u=3): e=0: .054854 | .013855 | .030820 | .031349; e ≥ .5E_0: with oracle 0 (R_0=.0129).
  p=½: all four equal.  ⇒ (i) the oracle strictly lowers the instance exponent at the zero
  residual with a field ((c) < R_0), up to making it ZERO in a window of accuracies;
  (ii) **"restricted to centre types forced by matching" (a) is a valid lower bound but NOT the
  value**: annular dips (b) do much better; the optimum of (b) always has `v0` at the lower end
  of the window (stability constraint active), which is why (b) < (c): the tilt bound does
  not know the window.  True instance exponent with oracle ∈ [(b), (c)] — gap 1–8 % typically.
  Sanity: f(plain profile) ≥ Rcc (annular around the cone-typical shell is smaller than the
  ball), equality at the optimal type; unconstrained sup over profiles = R_γ to 8 digits.
* (20:59) — **N5b** (`t06_nonadaptive.py` part A): exhaustive enumeration n = 10…14, six cases: the
  type-wise truncated cone is in the class (their [V] statement re-checked by brute force); the
  compensated pair (truncated + b·additive, cone + b·additive) is in the class and has ALL
  one-body marginals equal to ≤ 1.6e-15; uncompensated gap 1e-3…2e-2.  ⇒ H3 for the non-adaptive
  pair confirmed.  Part B and `t05` (type sums to n = 3200) running: with-oracle exponents
  approach R^max / θ_na from below like 0.7·ln n/n and 0.3·ln n/n (the price is the factor 1/n of
  the cyclic union bound: lnLB(oracle) − lnLB(no oracle) = −ln n − O(0.1)).
* 21:01 — **k = 2 exact** (`t08_k2_exact.py`, `out/t08_k2_exact.txt`): n = 13, G = AGL(1,13): base
  `a π_γ + (1−a) π_{γ2}` with `a = h/(h+g²)`, `p_2 = x + h/g` (h = height of the mixed excess above the
  parabola c2 = c1², g = self-consistency gap) and alternative = base + mixture of G-symmetrised
  dips of two centre types: ALL 13 one-body and ALL 78 two-body marginals equal to ≤ 7e-15;
  three-body differ by 2–4e-4.  A single centre type has h < 0 (below the parabola: sampling
  without replacement) — no mixture of product measures can match it; two types ≳ √n apart
  fix it.  Failures recorded: p_2 outside the window (n=11 case), h ≤ 0 (types too close).
* Literature: Kuperberg–Lovett–Peled, arXiv:1302.4295, Theorem 1.3 [full text of the statement
  read via pdftotext of the arXiv PDF]: "For all integers v ≥ 1, 1 ≤ t ≤ v and t ≤ k ≤ v there
  exists a t-(v,k,λ) design whose size is at most (cv/t)^{ct} for some universal constant c>0."
  ⇒ polynomial-size t-designs for ALL (n, block size, t): what the general k-body exact
  statement needs in place of the BCH codes of the uniform cube.

* 21:02 (clock read) — **N-tilt** (`t09_tilt_check.py`, `out/t09_tilt_check.txt`): the tilt inequality
  holds with min(LHS−RHS) = 0 (attained at λ=0) on 5 exactly matched alternatives (n = 10…14,
  λ ∈ [−3,3]); an unmatched alternative violates it (−4e-3 … −6e-2).  Derivative of the tilt bound
  at λ=0 at the zero residual: +0.0088 (p=.3,u=1), +0.0277 (p=.1,u=2), 0 (p=½).
* 21:02 — **Second coordinator note received**: the theory division published its own answer
  (THY-RES-0006 §3; theory report §11.29, Proposition 11.109, at commit dcdfea6; DEAD_ENDS D54
  item 3; scripts `oracle_field_scan.py`, `oracle_zero_types.py`).  I am asked for a separate
  report section "Against theory report §11.29".
  **Provenance record, before I open any of it:** everything logged above (H1–H5; the
  compensation lemma and the two-component base; Theorems A/B numerics N1–N6; the tilt bound;
  annular profiles; the k=2 construction with AGL(1,n); KLP designs) was derived and computed
  by me WITHOUT having seen THY-RES-0006, §11.29, D54 or their scripts.  I had read only
  THY-RES-0005 §2 (their two-sentence expectation and the parameter-counting remark).

* 21:02–21:15 (clock read 21:15 when written) — **Read the theory division's answer** (THY-RES-0006 §3; theory report §11.29,
  Proposition 11.109, lines 7080–7177 of the report at dcdfea6; DEAD_ENDS D54 item 3;
  `oracle_field_scan.py`, `oracle_zero_types.py`).  Their (a)–(d) [P]: window; one number;
  identity κ̄(ψ1) − κ̄(ψ0) = Φ/(1+Φ)[type(ν) − κ̄(ψ0)]; the lower bound (1−2δ)/maxdens survives with
  a factor n.  (e) [C]: at the zero residual the exponent with the oracle is
  ρ_e(p) = sup{r_μ(e): μ̄ = p}; coarse numbers 0.0129 vs 0.0134 at p=¼,u=1,e=0.02.  (f) [C]: for
  the class nothing changes at ε ≫ ln n — base = flat histogram with a logarithmic well at the
  excess type; missing: concentration of the excess mass / uniqueness of the optimal profile.
  Comparison with mine:
  - (a)–(d): agree; (c) is the mixture identity of my Lemma 3; my Theorem A is a pair that
    meets their criterion (c) EXACTLY by an explicit linear equation → their conjecture (f) is
    PROVED (different base: hardest additive instance + b × extreme additive instance; excess
    decoupled from the tuning parameter; no uniqueness/concentration needed; every n; every ε>0).
  - their trap (no sign change along the additive instances with the deepest dip) is real and
    does not touch my compensation (I do not move the base along additive instances; I ADD a
    second additive component to both members of the pair).
  - (e): `t10_theory_e.py`: exact R_0(0.02) = 0.013669 (centre type 0.4555, excess type 0.2760 —
    not "0.0134 at 0.29"); `t11_unrestricted_profiles.py`: **sup over two-block profiles of type
    p with block laws UNRESTRICTED = my tilt bound to 6 digits** (0.012941; 0.016345; 0.024371)
    and is attained at the cone laws of the TILTED reference, one of which lies OUTSIDE the
    window; restricted to block laws in the window (where the excess mass really sits — exact
    sums: an unstable-core dip with shell type 0.215 has true excess density 0.2439): 0.012630.
    So their number 0.0129 for ρ_e(p) is (numerically) my tilt upper bound; their search range
    (x0 down to 0.005 < p₋ = 0.109) includes profiles whose excess mass does NOT have the type
    of the profile — the concentration statement they flag as unproved is false there.
    Status of (e): direction proved here (tilt upper bound, given their hinted theorem at
    shifted fields); value in [0.012630, 0.012941] at their test point (decrease 5.3–7.6 %, not
    3.5 %).  They say "(e) needs an algorithm that uses the oracle (we have none)": mine is the
    hinted spot check + "reject the hint if the marginals differ", analysed by the tilt inequality.
* 21:13 — `t12`: at the hardest ADDITIVE instance γ* the oracle lowers the instance exponent too
  (tilt bound / R^max = 0.98, 0.96, 0.89 at p=.3,u=1, e = 0, .3E, .6E; 0.87, 0.65, 0.18 at p=.1,u=2;
  0 at p=.05,u=3,e=.6E).  With the oracle the hardest instance is no longer additive.
  `t13`: threshold of the zero residual with the oracle ≤ min_λ[E_0(θ−λ) + c(λ)]: ratio to E_0:
  0.990 (p=.4,u=1), 0.963 (.3,1), 0.864 (.1,1), 0.631 (.1,2), 0.368 (.05,3).
* The first run of `t02` was killed at its 30-minute limit (401-point γ-scan too slow); its
  partial output is kept as `out/t02_fixed_point_partial_first_run.txt`; a light version
  (41-point scan + refinement) is running and writes `out/t02_fixed_point.txt`.

* NOTE on the timestamps above (written 21:42): several entry headers were typed as estimates; I have corrected
  them here to the clock readings that the shell printed at the time (20:07, 20:23, 20:45, 20:49, 20:53, 20:59,
  21:01, 21:02, 21:15).  Order of events, which is what matters for provenance: H1-H5 (before 20:23) -> N1, N2,
  N5a (by 20:45) -> N3 zero-residual bracket, N5b, k=2 (by 21:01) -> tilt check (21:02) -> second coordinator note
  (21:02) -> theory material read and compared (21:02-21:15).
* 21:26-21:41 — report sections 1-8 written.  `t07` (slow annular scan) stopped; bug found in it by `t07b`
  debugging: the bisection range for the lift (eps + 60) is too short for annular dips at n >= 800 (their lift is
  n(e + D(core||pi)), not eps + O(1)); `t07b_annular_fast.py` (bounding box, lift range up to u*n) reproduces
  n = 400 (+0.002842) and gives n = 800: lnLB = +6.83 (lnLB/n = +0.008534) at p=.1,u=2,e=.2E_0.
* 21:41 — `t14_theory_numbers.py`: my profile formula with label laws UNRESTRICTED reproduces the theory
  division's own output file (dcdfea6, out_oracle_zero_types.txt) at all six types: 0.00491/0.00485,
  0.01210/0.01210, 0.01294/0.01294, 0.01341/0.01340, 0.00938/0.00942, 0.00338/0.00338; their reported maximiser
  (0.46, 0.497, 0.118) is mine (0.460, 0.1178, 0.4967), with 0.497 > p_+ = 0.4754.  Restricted to the window:
  0.00217, 0.01142, 0.01263, 0.01302, 0.00482, 0.  => their r_mu is my f; their rho_e(kappa) admits profiles
  whose excess mass does not have type kappa.

* 21:43 — `t15_tolerance_check.py`: ingredients of Theorem τ by enumeration at n = 12: all marginals of orders 1–3 of
  (base + average of N i.i.d.-centre dips) within 0.02 (τ = 0.1, N = 400) resp. 0.007 (τ = 0.03, N = 2000) of the base's.
* 21:45 — `t07b`: n = 1600: lnLB = +17.98 (lnLB/n = +0.011240) at the zero residual with the oracle, p=.1,u=2,e=.2E_0
  (V = 0.015441, U = 0.016345; forced-type plain dips: nothing).  `t05`: n = 3200 rows for (0.1,2,0.3E): 0.021586
  (R^max 0.023270) and (0.1,2,0.05E): 0.041652 (R^max 0.043316).
* 21:47 — report `docs/science/workstreams/SF_REPORT.md` complete (sections 1–8 + re-run instructions).

## State at close (resume here)

* Report: `docs/science/workstreams/SF_REPORT.md`.
* Still running when I closed (they write `out/<name>.txt` only when they end; the running logs are complete records
  of what was computed): `t05_typesums_adaptive.py` (`out/t05_run.log`), `t06_nonadaptive.py` (`out/t06_run.log`),
  `t07b_annular_fast.py` (`out/t07b_run.log`).  If they were killed with the session, the logs stand.
* Main results: Lemma 3 (compensation), Theorem A / Corollary A (adaptive exponent unchanged, every n), Theorem B /
  Corollary B (non-adaptive), Proposition S (the sketch's mechanism is false: M*W ≠ Q*), Proposition C (tilt
  inequality; oracle helps at additive instances), Proposition D (lower bounds at an instance; shells beat forced
  centre types), Conjecture Z, Proposition E (k = 2), Theorem τ (tolerances), §8 (against theory §11.29).
* Open: exact instance-wise exponent (bracket [V, U]); k ≥ 3; U at bounded accuracy; nothing machine-checked.
* Files: `sl.py` (single-letter library), `ts.py` (type-class sums), `prof.py` (profiles, tilt bound),
  `t01`…`t15` (tests; `t07` superseded by `t07b`), `out/` (outputs and logs).
