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
