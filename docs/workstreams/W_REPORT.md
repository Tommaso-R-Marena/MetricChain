# Workstream W — the heteropolymer product landscape: several site types, larger alphabets, general single-site known parts and site envelopes; exponents without a hint

> **Repository note (added by the coordinator at integration; the report below is otherwise as
> delivered).**  Status: **paper proofs by one author; reviewed after integration by the
> Scientific Discovery Division (SCI-REV-0005: Theorem W3(c) with Remark W3.1 and Proposition
> W4.0 proved; Theorem W4 proved with two gaps in the written proof, both closed — see the
> errata below); checked and re-computed in part by the coordinator.**  *Re-computed with
> an own implementation written from the
> statements* (`experiments/coordinator_checks/sites_W/`): the vertices of the four Lipschitz
> polytopes; Theorem W3(c) — the Rényi form against the linear-programming value of the game
> at the Rényi centre and against a blind search over `γ`, with the dual bound (12 cases);
> every number of the first table of §6.2 and `R^max(0.3E)`, `θ_na(0.3E)` for the six chains
> (largest deviation `5·10⁻⁷`, the rounding of the table); "the exponents do not add" at three
> accuracies; the pair identity (`10⁻¹³`); the two negative results (the convex kink of `F*` of the
> triangle site at `t = 0.378`; `E = 0.119499 < 0.120196` for three states).  *Re-derived:* Theorem
> W3(c) (the step `min_a ln(P(a)/m(a)) ≤ −ln Σm` and the closure of `L_j` under soft minima), the
> dictionary of Remark W3.1, Lemma W1.0, Proposition W3.2(a), Proposition W4.0.  *Read, not
> re-derived line by line:* Lemma T′, Theorem W2(b), (c), Theorem W3(b), Theorem W4 (a proof by
> transfer of Theorems 11.52, 11.54, 11.64).  *Not re-run:* the exact sums over joint types (§6.3),
> the brute-force runs (§6.4), the isoperimetric families.
> **One conjecture of the report is refuted by the coordinator's checks** (§8, Proposition
> W7.3(b), and §11 item 8: "the uniform site law maximises `h` and `a` for the Hamming envelope"
> — scanned by the workstream at `u = 1, 2` only): for three letters it fails at small slopes,
> for `h` exactly when `u < ln 2` and for `a` when `u < 0.5194`, where site laws close to
> `(½, ½, 0)` are harder (theory report §11.26, Proposition 11.103).  The upper bounds of
> Theorems W2, W4 inherit the status of Theorem 11.78(b) (refereed "proved" by R10 as this
> report was integrated).
> The integrated statements and their labels are in `docs/THEORY_REPORT.md` §11.26: Theorem W1
> = Theorem 11.95; Lemma T′, Theorem W2 = Lemma 11.96, Theorem 11.97; Theorem W3(a), (b), (d),
> (e) = Theorem 11.98; Theorem W3(c), Remark W3.1 = Theorem 11.99; Proposition W3.2 =
> Proposition 11.100; Proposition W4.0, Theorem W4 = Theorem 11.101; Theorem W6, Proposition
> W6.1 = Proposition 11.102; Propositions W7.1–W7.3 = Proposition 11.103.  Scripts and outputs:
> `experiments/workstreams/W/` (the report's `code/`, `out/`; "`scratchpad/ws/W/`" in the text is
> the session directory in which the report was written).
>
> **Errata after the independent review SCI-REV-0005** (Scientific Discovery Division,
> workstream R5; its report is `docs/science/workstreams/R5_REPORT.md` on the branch
> `research/scientific-translation`; no critical finding; every reference number replicated,
> largest deviation `5·10⁻⁷`).  The text below is unchanged; read it with these.  The
> integrated corrections, with what was re-derived and re-computed for each, are in the
> theory report §11.26.  Line numbers in the review refer to this file before this block
> was inserted.
> *Major (gaps in what is written; closed; no exponent changes).*
> (M1) Theorem W2(c) — the isoperimetric statement in the form the nested algorithm needs,
> uniform in the composition — was stated and proved in this report only.  It is now
> Theorem 11.97(c) of the theory report, with the dependence of `ω_n` on
> `(m, q_max, D_max, π_min)` explicit.  In its proof here the modulus `ω′(δ₂)` of `I − v` comes from
> uniform continuity and has no rate; the bound
> `(I − v)(P) = Σ_jλ_j·min_{γ∈L_j}KL(P_j‖π_γ) ≤ Σ_jλ_j·χ²(P_j‖Q_j)` for `Q` in the window gives one.
> (M2) Theorem W4, proof, (i) "the exponent of `M†`" and (iii): "exponent function … defined
> along sequences of compositions tending to `λ`" is not defined, and the bound on `M†` is
> claimed "uniformly over the compositions of the outer block" because `R̂` is continuous in
> `λ`, while the quantity that enters is `θ_na`; the restriction to compact sets of `θ` is not
> needed.  The definition, a direct argument and the bound
> `|θ_na^{λ′}(x) − θ_na^λ(x)| ≤ ‖λ′ − λ‖₁·max_ja_j` are in the theory report, Theorem 11.101 (the
> reviewer's closure, re-derived).
> *Minor.*  (m1) Remark W3.1: "a fixed sample certifies `E_sp(θ)`" is for `0 < θ < a`; "an adaptive
> algorithm, or one with a hint, certifies `E_sp(θ) − θ`" only for `0 < θ < h` (beyond, the
> expression is `≤ 0`), asymptotically, in the worst case over the class and, with a hint,
> at the hardest instance; `max_{ρ≥0}` in the formula for `R^max` is a supremum.  (m5) Proof of
> Theorem W2(b), Step 4: "all of them are within `nδ₁·max(D_max,1)` of their means" does not
> give the next inequality when `D_max > 1`; read: the cost within `nδ₁D_max` and every letter
> count within `nδ₁` — which is what Hoeffding's inequality gives with the stated
> probability.  (m6) Lemma T′ is stated for `ρ_j` of full support and applied with
> `ρ = ⊗_iP_{τ(i)}`, `P` a joint type that may miss letters: restrict the alphabets to the
> supports.  (m7) Theorem W4, (ii)–(iii): with the base family "complete enumeration" the
> recursion does not start at `θ_na`; the machine-checked statement that applies is
> `iterates_lt_hint_add` (any bounded start) with the `HintPair` of `GameFunction.pair`, not the
> convergence statement of Theorem 11.66(c) (`GameFunction.exactRec_tendsto`).
> (m8) Proposition W3.2(c): the slope jump of `F*` at the label switch of the triangle site
> is **`+0.0056`** (the slopes of the two branches at `t_c = 0.377987` are `0.054049` and `0.059631`),
> not `+0.0052`; the printed number is a second difference on a grid of step `5·10⁻⁴`
> (`w08_misc.py`), lowered by the curvature of the branches.  `t_c`, the weights, the corner
> `0.1996·E` and the slopes `−0.383 → −0.373` of `R^max` are right.  (m9) Theorem W4: the `o(n)` is
> uniform over chains with compositions near `λ` (this is what the closure of (M2) gives);
> `λ_j > 0` is assumed and does not seem to be used.  (m11) Theorem W3(c), "the labels that
> carry weight are exactly at Rényi distance `C_t` from it": one direction only — labels in
> the support of `M*` are at distance `C_t` from the centre; a vertex at that distance need
> not carry weight, and `M*` need not be unique (`s*` and the centre are).  (m12) Numerical
> hygiene: game values from a linear programme solved with default tolerances bias a
> blind maximisation over `γ` upwards by `1–3.5·10⁻⁹`; not an error of a statement (the
> checks are at `5·10⁻⁷`).  (m2, m3, m4, m10 concern the theory report's rendering only.)
> *Additions of the reviews* (theory report, Proposition 11.103(d), (f)), to be read with
> §8, Proposition W7.3 and §11, item 8: at `u = 0.5` the three-letter law `(0.05, 0.5, 0.45)` is
> harder than the two-letter cube in `h`, `a` and `E`; every site law that gives some set of
> letters the weight `½` is at least as hard as the cube (Hamming envelope); and
> `F*(t) ≤ t(1−t)u²/8` for every site whose envelope is at most `u`.

Independent report (25 Nov 2026).  Directory: `scratchpad/ws/W/` (`W_report.md`, scripts `code/`, outputs `out/`).
The repository was read at commit `e4351b9` with the working tree as found (modified files of others); nothing in it
was changed, no state-changing git command, no subagent, no Lean, no `lake build`.  Numerics: own Python (numpy/scipy
only; nothing imported from the repository), fixed seeds, `ulimit -v 4000000`, every run under ten minutes (`timeout
590`), one heavy process at a time; commands, sizes and run times in §12.

Labels on every statement: **[proved]** = complete proof in this report (a paper proof by one author, **not
refereed**; what is taken from the theory report or from a machine-checked file is named), **[sketch]** (missing steps
named), **[numerical]**, **[conjecture]**, **[known]** (source, and how it was read).

---

## 0. Verdicts

| goal | verdict |
|---|---|
| **W1** symmetry alone | **Carries over completely, [proved] for every `n`** (Theorem W1).  Group `Γ = Π_j S_{n_j}`, orbits = joint-type classes, `N_orb = Π_j C(n_j+q_j−1, q_j−1)`.  The quotient envelope **is** the transport cost, `δ(P, P′) = n Σ_j λ_j W_{d_j}(P_j, P′_j)`, exactly (oriented, for asymmetric `d_j`).  The joint-type-stratified sample is optimal among non-adaptive algorithms up to `8 N_orb ln(2N_orb/δ)/(1−2δ)` in the cost and `ln(4/δ)` in the accuracy; every algorithm needs `(1−2δ)/maxdens(D)` at an invariant instance; the flat-histogram instance is the hardest invariant instance up to the factor `N_orb + 1`.  Brute force on a two-type chain with two asymmetric envelopes: no violation (`w06`, Part B). |
| **W2** single-letter theorem | **[proved]** (Theorem W2): the exponent of every algorithm at an invariant instance is a supremum over *labelled profiles* — laws of (label, site type, letter) — of a minimum over exit profiles with the transport cost `E d_T(X′, X)`; lower bound for every `n`, upper bound by types.  Three steps of the proof of Theorem 11.78 change (Lemma T with the site type in the label; a transport cost in the kernel and in the Hoeffding step; `N_orb` for `n+1`); nothing in it uses a product measure, so it is stated for **every known part that is a function of the joint type** (this is most of W7). |
| **W3** evaluation | **(a) yes [proved]**: the flat-histogram instance is exactly as hard as the hardest additive instance (Sion).  **(b) yes [proved]**: labels that are vertices of the Lipschitz polytopes `L_j` suffice, with the Gibbs law of the vertex as letter law, at most `q_j` of them per site type.  **(c) yes [proved]**: `F* = max_γ F(γ,·)` is a game function, with `E = Σλ_jE_j` and the sharp constant `L = a = Σλ_ja_j`; Theorem 11.66 gives the pair.  **New closed form [proved]:** `F*_j(t) = (1−t)·C_t(𝒲_j)`, the Rényi capacity of order `t` of the channel "vertex `φ` ↦ Gibbs law `π_φ`", and **the hardest additive instance is the Rényi centre of the window**; consequently `a_j` is a Shannon capacity, `E_j` a reverse-divergence radius, and `θ_na` is the inverse of a sphere-packing exponent.  **(d) yes [proved]**: `F*(t) = Σ_j λ_j F*_j(t)` with one common `t` (F12(iii) is right).  The exponents do not add: `R^max(e) ≤ min_{Σλ_je_j=e} Σλ_jR_j(e_j) ≤ Σλ_jR_j(e)`; the second gap is `+8.5 %`, `+47 %`, `+1365 %` at `e = 0.3E, 0.5E, 0.9E` in the worked example, the first is zero iff the `F*_j` are concave where it matters.  **Negative, new:** for three states `F*_j` **need not be concave** — the optimal label structure can switch discontinuously (a corner of `R^max`), and then even the best split of the accuracy is not exact. |
| **W4** adaptive, no hint | **Transfers [proved by transfer of the refereed binary proofs; every changed step written out; not refereed]** (Theorem W4): the worst-case exponent of adaptive algorithms without a hint is `R^max(ε₁) = max_t[Σ_jλ_jF*_j(t) − tε₁]`, the hinted exponent of the hardest additive instance.  Neither candidate obstacle is one: the tail lemma relative to a reference holds verbatim in the orientation `s(y→x)`, and the isoperimetric input is Theorem W2(c).  What needed more than the binary proof: Lemma T′, the evaluation lemma with Kantorovich duality, the window step by an optimal coupling, uniform continuity of `I − v` in place of a quadratic bound, families indexed by compositions, and the constant in the union bound (M2).  Nothing of the algorithm was simulated. |
| **W5** worked example | Done (§6): a path `0–1–2` with steps `0.8, 1.6`, a triangle with sides `1, 1.5, 2`, an asymmetric three-state envelope, and two chains with a binary and a ternary site type.  Every optimum is certified by a duality bracket (`≤ 2·10⁻⁹`) and re-evaluated by a primal solver that shares nothing with the search (agreement `≤ 5·10⁻¹⁴`).  Exact sums over joint types up to `n = 480` (hinted) and `n = 240` (non-adaptive) approach the formulas with `|θ_n − R| ≤ 0.4·ln n/n`, resp. an excess `0.4…0.7·ln n/n`; brute force on full product spaces (`3⁸`, `2⁴3⁴`, `3⁷` points) agrees to `10⁻¹⁴`.  The binary theory applied to a "worst binary reduction" is off by factors `0.54`–`0.80` (coarse-graining two states: a proved lower bound) and `1.29`–`1.42` (deleting a state: not a bound) at vanishing accuracy, and by any factor near the threshold. |
| **W6** asymmetric envelopes | **Everything survives, [proved]**, once the orientation is fixed (§1.2): the every-`n` statements, the single-letter theorem, the evaluation, the shear law, the nested algorithm.  For two states an asymmetric envelope is a symmetric one plus a field (checked to `3·10⁻¹⁶`); for three states it is a new case, and in it the zero residual is far from the hardest instance (`R_0/R^max = 0.75` at `e = 0`, `0.15` at `0.7E`; its own threshold is `0.1555` against `E = 0.1911`). |
| **W7** (optional) | Theorem W1, Theorem W2, "`v` or `I`", shell-cones and the regularity statement transfer verbatim to every known part that is a function of the joint type (**[proved]**, same proofs); for a convex rate function also the collapse to additive instances and the game function.  What does not: the closed (Rényi) form, the clean every-`n` product bound, the nested algorithm (the obstruction of §11.23).  Mean-field Potts (`q = 3`, convex regime): the exponent at the colour-symmetric profile equals the flat product site's, for every coupling (**[proved]** by symmetry; numerically `10⁻¹⁴`).  **Negative:** "a field always helps" (Proposition 11.65(b)) is **false for three states near the threshold** (`E = 0.119499` for the uniform law against `0.120196` for `π = (0.05, 0.5, 0.45)`, Hamming envelope, `u = 1`). |

**The three things to take away.**
(1) *The sketch F12 is right, and it is now a chain of theorems:* for a fixed sequence of site types, any alphabets,
any single-site known parts and any site envelopes (symmetric or not), the three exponents are

    hinted at the hardest instance = adaptive without a hint:   R^max(e) = max_{0≤t≤1} [ Σ_j λ_j F*_j(t) − t e ],
    non-adaptive without a hint:                                 θ_na = R^max ∘ S^{-1},   S(e) = e + R^max(e),
    thresholds:   E = Σ_j λ_j E_j   (bounded cost above),        a = θ_na(0+) = Σ_j λ_j a_j .

(2) *The single-site ingredient has a closed variational form:* `F*_j(t) = (1−t)·C_t`, with `C_t` the Rényi capacity of
the family of Gibbs laws of the vertices of the site's Lipschitz polytope — a smooth convex programme; the hardest
additive instance is the one whose Gibbs law is the Rényi centre.  The class threshold is `E_sp(0)`, the non-adaptive
exponent at vanishing accuracy is the Shannon capacity, and the accuracy that a fixed sample of `e^{nθ}` points
certifies is the sphere-packing exponent `E_sp(θ)` of that channel.
(3) *What is genuinely different from two states:* the hardest perturbations are labelled by vertices that need not be
distance functions; the label structure can switch discontinuously with the accuracy; exponents of site types combine
through a common slope `t`, not at a common accuracy; and the uniform site law is not always the hardest.

---

## 1. Setting, notation, and the orientation convention

### 1.1 Setting

Sites `i = 1..n` with types `τ(i) ∈ {1..m}` (a fixed sequence), `n_j = #{i : τ(i) = j} ≥ 1`, `λ_j = n_j/n` (the
*composition*).  Site type `j`: alphabet `𝒮_j`, `q_j = |𝒮_j| ≥ 2`; site law `π_j` of full support, `π_min = min π_j(a)`;
site envelope `d_j : 𝒮_j × 𝒮_j → [0, ∞)` with `d_j(a,a) = 0` and the triangle inequality, **not necessarily symmetric**;
`D_max = max_j max_{a,b} d_j(a,b)`, `q_max = max_j q_j`.  `X = Π_i 𝒮_{τ(i)}`, `π = ⊗_i π_{τ(i)}`,
`d(x,y) = Σ_i d_{τ(i)}(x_i, y_i)`,

    𝒞 = { ψ : X → ℝ :  ψ(x) − ψ(y) ≤ d(x,y)  for all x, y },     w = e^{−ψ},     A(ψ) = E_π e^{−ψ} .

Target `ln A(ψ)`, accuracy `ε = ε₁n`; an algorithm is `(ε/2, δ)`-correct if its output is within `ε/2` of `ln A(ψ)`
with probability `≥ 1 − δ` for **every** `ψ ∈ 𝒞`; cost = expected number of evaluations of `ψ`; model of algorithms
as in theory report §11.10.

### 1.2 Orientation (used everywhere; this is the whole content of W6 as far as bookkeeping goes)

**(O) In `d(x, y)` the first argument is the point at which `ψ` may be larger:** `ψ(x) ≤ ψ(y) + d(x,y)`, i.e.
`w(y) ≤ w(x) e^{d(x,y)}`.  Consequences, each a one-line check:

* *Dips.*  For `ψ₀ ∈ 𝒞` and `D ⊊ X` the smallest member of `𝒞` that agrees with `ψ₀` off `D` is
  `ψ₀^D(x) = max_{y∉D} [ψ₀(y) − d(y, x)]` (`x ∈ D`).  (The function `E(x) = max_{y∉D}[ψ₀(y) − d(y,x)]` satisfies
  `E(x) − E(x′) ≤ d(y*, x′) − d(y*, x) ≤ d(x, x′)` and equals `ψ₀` off `D`.)  With the **slack**
  `s₀(y, x) = d(y, x) − ψ₀(y) + ψ₀(x) ≥ 0` (`y` the outside point, `x` the inside point — the first argument is the
  evaluated point, the second the centre, as in §11.10), the Gibbs law `μ₀ ∝ π e^{−ψ₀}` and
  `s₀(Dᶜ→x) = min_{y∉D} s₀(y,x)`:

      A(ψ₀^D)/A(ψ₀) = 1 + Φ₀(D),     Φ₀(D) = Σ_{x∈D} μ₀(x) (e^{s₀(Dᶜ→x)} − 1),     Φ₀⁺(D) = Φ₀(D) + μ₀(D).

* *Additive members.*  `γ = (γ_j)`, `γ_j ∈ L_j := {γ : γ(a) − γ(b) ≤ d_j(a,b)}` (the Lipschitz polytope of the site;
  compact modulo constants), `ψ_γ(x) = Σ_i γ_{τ(i)}(x_i)`, `Z_γ = E_{π_j} e^{−γ}`, `γ̃ = γ + ln Z_γ`,
  `π_γ = π_j e^{−γ̃}` (Gibbs law), `𝒱_j` = the vertices of `L_j/ℝ`.
* *Transport.*  `W_j(P′, P) := min { Σ κ(a,b) d_j(a,b) : κ a coupling with first marginal P′, second marginal P }
  = max_{φ∈L_j} [E_{P′}φ − E_Pφ] = max_{φ∈𝒱_j} [E_{P′}φ − E_Pφ]` (Kantorovich duality for a cost with zero diagonal
  and the triangle inequality: for a dual pair `f(a) + g(b) ≤ d_j(a,b)` put `φ(a) = min_b[d_j(a,b) − g(b)]`; then
  `φ ∈ L_j`, `φ ≥ f`, `−φ ≥ g`).  `W_j` satisfies the triangle inequality and is not symmetric.
* *Joint types.*  `P_x = (P_{x,j})_j`, `P_{x,j}` the empirical law of `x` on the sites of type `j`;
  `𝒫 = Π_j Δ(𝒮_j)`; `W(P′, P) = Σ_j λ_j W_j(P′_j, P_j)`; `H(P) = Σ_jλ_jH(P_j)`; for the product measure
  `I(P) = Σ_j λ_j KL(P_j‖π_j)`.
* *Flat histogram.*  `v_γ(P) = Σ_j λ_j [−E_{P_j}γ_j − ln Z_{γ_j}]` (the normalised log-weight of `ψ_γ` per site),

      v(P) = max_{γ ∈ ΠL_j} v_γ(P) = min_{P′} [ I(P′) + W(P′, P) ]        (Gibbs principle, then Kantorovich),
      ψ_H(x) = −n v(P_x) = min_γ [ ψ_γ(x) + Σ_j n_j ln Z_{γ_j} ]  ∈ 𝒞,     μ_H ∝ max_γ π_γ^{⊗},     1 ≤ Z_H := A(ψ_H) ≤ N_orb .

  `v` is convex, `v ≤ I`, and `v(P) ≤ v(P″) + W(P″, P)`.  The **window** is `𝒲 = {v = I} = {(π_{γ_j})_j : γ ∈ ΠL_j}`
  (`v(P) = I(P)` iff `−ln(P_j/π_j) ∈ L_j` for all `j`); every member has all letters `≥ π_min e^{−D_max}`.

Brute force (`w06`, Parts A, B) checks the dip formula, the orientation of the slack (the transposed slack violates
the tail lemma in 2 582 of 13 328 cases) and the identity of the quotient envelope with the transport cost.

### 1.3 The game of a site, and the exponent functions

For a site type `j`, `γ ∈ L_j` and `t ≥ 0` (Theorem 11.27(c) for this class: the slack of `ψ_γ` is
`d_j(a,b) − γ(a) + γ(b)`, its Lipschitz polytope is `L_j − γ`, and `σ_φ = φ̃ − γ̃` is the normalised centre):

    K_t^γ(a, φ) = e^{−t(φ̃(a) − γ̃(a))} = (π_φ(a)/π_γ(a))^t   (a ∈ 𝒮_j, φ ∈ 𝒱_j),      F_j(γ, t) = −ln val(K_t^γ),
    F*_j(t) = max_{γ∈L_j} F_j(γ, t),     F*(t) = Σ_j λ_j F*_j(t),     R̂(e) = max_{0≤t≤1} [F*(t) − t e]   (all real e),
    E = sup_{0<t≤1} F*(t)/t,    a = sup_{0≤t<1} F*(t)/(1−t),    h = R̂(0),    S(e) = e + R̂(e),    θ_na = R̂ ∘ S^{-1}  on (0, ∞).

(`val` = value of the matrix game in which the sampler mixes letters and the adversary mixes vertices.)  `R̂` is what
the brief and §11.20 call `R^max`; I write `R^max` in the summary tables and `R̂` in proofs.

---

## 2. W1 — what symmetry alone gives (every `n`)

`Γ = Π_j S_{n_j}` acts on `X` by permuting sites of the same type.  The hypotheses of the remark after Theorem 11.76
hold: `d(σx, σy) = d(x,y)` (sites of one type carry the same `d_j`), `π(σx) = π(x)`, hence `𝒞` and `A` are invariant.
The orbits are the joint-type classes `T_P = {x : P_x = P}`; their number is

    N_orb = Π_j C(n_j + q_j − 1, q_j − 1)  ≤  Π_j (n_j + 1)^{q_j − 1}        (polynomial in n).

`dens_P(S) = |S ∩ T_P|/|T_P|`, `maxdens(S) = max_P dens_P(S)`; `J_P = −ln π(T_P)`.  An *invariant instance* is
`ψ_g(x) = g(P_x)`.

**Lemma W1.0 (the quotient envelope is a transport cost) [proved].**
`δ(P, P′) := min{d(x,y) : x ∈ T_P, y ∈ T_{P′}} = n·W(P, P′) = Σ_j n_j W_j(P_j, P′_j)`, exactly, for every `n`; it has
zero diagonal, satisfies the triangle inequality and is asymmetric when the `d_j` are.  An invariant function `g(P_x)`
is in `𝒞` iff `g(P) − g(P′) ≤ δ(P, P′)` for all joint types.
*Proof.*  For fixed `x ∈ T_P` the sites of type `j` can be re-arranged freely in `y`; choosing `y` is choosing, for
every type, a nonnegative integer matrix `(N_{ab})` with row sums `n_jP_j` and column sums `n_jP′_j`
(`N_{ab}` = number of sites with `x_i = a`, `y_i = b`), at cost `Σ N_{ab} d_j(a,b)`.  The transportation polytope with
integer marginals has integer vertices, so the integer minimum is the linear-programming minimum `n_jW_j(P_j,P′_j)`.
The last claim: "only if" by taking minimising pairs, "if" because `δ(P_x,P_y) ≤ d(x,y)`.  ∎  (Brute force, both
envelopes asymmetric: `1.8·10⁻¹⁵`, `w06` B1.)

**Theorem W1 (what the symmetry of the sequence of site types gives; every `n`, every composition, symmetric or
asymmetric envelopes).**  [(a): truncation and lower bound **[proved]** from machine-checked statements
(`GroupSampling.lean`: `lowDens_shift`, `truncate_admissible`, `group_nonadaptive_queries_ge`), upper bound
**[proved]**; (b): **[known]**, machine-checked (`group_queries_ge`); (c), (d): **[proved]**.]

(a) *Non-adaptive algorithms.*  For `ψ ∈ 𝒞` and `0 < q < 1` let `t_P` be the smallest value `τ` of `w` on `T_P` with
`dens_P{w > τ} ≤ q` (the upper `q`-quantile on the orbit), `ψ^{tr,q}(x) := max(ψ(x), −ln t_{P_x})`, and
`ε_n^{tr}(q) := sup_{ψ∈𝒞} ln[A(ψ)/A(ψ^{tr,q})]`.  Then
 (i) `t_{P_y} ≤ t_{P_x} e^{d(x,y)}` for all `x, y`; hence `ψ^{tr,q} ∈ 𝒞`, it differs from `ψ` only on
 `D = {w > t_{P_x}}`, `maxdens(D) ≤ q`, and `dens_P{w ≥ t_P} ≥ q` for every `P`;
 (ii) if `ε < ε_n^{tr}(q)`, every randomised non-adaptive `(ε/2, δ)`-correct algorithm makes at least `(1 − 2δ)/q`
 evaluations;
 (iii) the **joint-type-stratified sample** — `M = ⌈8 ln(2N_orb/δ)/q⌉` uniform points from each joint-type class,
 `Â = Σ_P π(T_P)·(`sample mean of `w` over `T_P)`, output `ln Â + ½[ε_n^{tr}(q) + ln 2 − ln(2/δ)]` — is `(ε/2, δ)`-correct
 on `𝒞` for every `ε ≥ ε_n^{tr}(q) + ln(4/δ)`.
 So it is optimal among non-adaptive algorithms up to the factor `N_orb·⌈8 ln(2N_orb/δ)/q⌉·q/(1−2δ)` in the cost and
 the additive `ln(4/δ)` in the accuracy, with the one extremal function `ε_n^{tr}`; no isoperimetry is used.

(b) *All algorithms at an invariant instance.*  If `ψ′ ∈ 𝒞` differs from the invariant instance `ψ_g` on a set of
orbit density at most `q` and `|ln A(ψ′) − ln A(ψ_g)| > ε`, every randomised `(ε/2, δ)`-correct algorithm — adaptive
or not, with any hint — makes at least `(1 − 2δ)/q` evaluations in expectation at `ψ_g`.  In particular
`(1 − 2δ)/maxdens(D)` whenever `ε < ln(1 + Φ_g(D))`, `D ⊊ X`.

(c) *The flat-histogram instance is the hardest invariant instance.*  For an invariant instance put
`Λ_g(P) := −g(P) + min_{P′}[J_{P′} + g(P′)]` (its landscape) and `Z_g := Σ_P e^{−(J_P − Λ_g(P))} ∈ [1, N_orb]`.  Then

    Φ_g⁺(D) = Z_g^{-1} Σ_{x∈D} π(x) exp( min_{y∉D} [ d(y,x) + Λ_g(P_y) ] ),        Λ_g(P) ≤ V_n(P) := min_{P′} [ J_{P′} + δ(P′, P) ],

with equality for `ψ_H^{lat}(x) := −V_n(P_x) ∈ 𝒞`.  Hence `Z_gΦ_g⁺(D) ≤ Z_HΦ_H⁺(D)`, `Φ_g⁺(D) ≤ N_orb·Φ_H⁺(D)`, and
`ln(1 + Φ_g(D)) > ε ⟹ ln(1 + Φ_H(D)) > ε − ln(N_orb + 1)` for every `D`: every lower bound that (b) gives at an invariant
instance holds at the flat-histogram instance at the accuracy `ε − ln(N_orb + 1)`.  (`V_n` is the largest minorant of
`J` that is admissible for the *transposed* quotient envelope, `V_n(P) − V_n(P′) ≤ δ(P′, P)`: the orientation matters
when the `d_j` are asymmetric.  For the product measure `nv ≤ V_n ≤ nv + O(log n)`, so `ψ_H` of §1.2 and `ψ_H^{lat}` are
the same instance at the exponential scale.)

(d) *Instance-optimality at invariant instances without a hint.*  Per joint-type class draw two independent uniform
samples of size `M ≥ 2K`; `t̂_P` := the `⌈K⌉`-th largest weight of the first, `â_P` := the mean of `min(w, t̂_P)` over the
second, `q = 2K/M`, `L = (2/3)Σ_Pπ(T_P)â_P`, `U = 2Σ_Pπ(T_P)â_P + Tail`,
`Tail = max{Σ_{x∈D}π(x)[min_{y∉D} t̂_{P_y}e^{d(y,x)} − t̂_{P_x}]₊ : D ⊊ X, maxdens(D) ≤ q}`.  With `K = 24 ln(4N_orb/δ)`:
`L ≤ A(ψ) ≤ U` with probability `≥ 1 − δ` for every `ψ ∈ 𝒞`; with doubling (`K_i = 24 ln(4N_orb2^i/δ)`) and stopping at
`ln(U/L) ≤ ε` the cost at every invariant instance is within `16N_orbK/(1−2δ)` of the least cost of any correct algorithm
at that instance at the accuracy `ε − ln 3`.

*Proof.*  (a)(i) `lowDens_shift` **[V]**: for an admissible `ψ`, points `x, y` and a level `c`, the orbit density of
`{ψ < c − d(x,y)}` at `y` is at most that of `{ψ < c}` at `x` (if `ψ(σy)` is that low, admissibility between `σx` and
`σy` forces `ψ(σx) < c`; no coupling of adjacent orbits has to be constructed).  In weights:
`dens_{P_y}{w > τe^{d(x,y)}} ≤ dens_{P_x}{w > τ}`.  With `τ = t_{P_x}` the right side is `≤ q < 1`, so some value of `w`
on `T_{P_y}` is `≤ t_{P_x}e^{d(x,y)}`, and the largest such value `τ′` has `dens{w > τ′} ≤ q`: `t_{P_y} ≤ τ′`.  So
`c(x) := −ln t_{P_x}` is in `𝒞`, and so is the maximum of two members (`truncate_admissible` **[V]**).  (The Lean file
regularises arbitrary invariant levels; the exact quantiles need no regularisation.)  `dens_P{w ≥ t_P} ≥ q`: if `t_P`
is not the least value on the orbit, the next smaller value `τ⁻` has `dens{w > τ⁻} > q` and `{w > τ⁻} = {w ≥ t_P}`.
(ii) `group_nonadaptive_queries_ge` **[V]** for the pair `(ψ, ψ^{tr,q})`.  (iii) `A(ψ) = Σ_Pπ(T_P)E_{T_P}w` by
invariance of `π`; `E Â = A` and Markov give `Â ≤ 2A/δ` outside probability `δ/2`; the variables `min(w(X_i), t_P)/t_P ∈ [0,1]`
of class `P` have total mean `≥ Mq ≥ 8ln(2N_orb/δ)`, so by the multiplicative Chernoff bound every class mean is at
least `½E_{T_P}min(w,t_P)` outside probability `δ/(2N_orb)` each; then `Â ≥ ½A(ψ^{tr,q}) ≥ ½e^{−ε_n^{tr}(q)}A(ψ)`.
(b) is `group_queries_ge` **[V]** (Theorem 11.22(c) for the alternatives `ψ′∘σ`, `σ` uniform in `Γ`).
(c) By (O), `Σ_{x∈D}π(x)e^{−g(P_x)}e^{s_g(Dᶜ→x)} = Σ_{x∈D}π(x)exp(min_{y∉D}[d(y,x) − g(P_y)])`; divide by
`A(ψ_g) = Z_g e^{−min[J+g]}`.  `ψ_g ∈ 𝒞` gives `g(P′) − g(P) ≤ δ(P′,P)`, hence `Λ_g(P) ≤ J_{P′} + δ(P′,P)` for all `P′`.
`V_n(P_y) ≤ V_n(P_x) + δ(P_x,P_y)` by the triangle inequality of `δ`, so `ψ_H^{lat} ∈ 𝒞`, and its landscape is `V_n`.
Then `1 + Φ_g ≤ 1 + Φ_g⁺ ≤ 1 + N_orb(Φ_H + μ_H(D)) ≤ (N_orb+1)(1+Φ_H)`.  (`nv ≤ V_n ≤ nv + O(log n)`: `nI(P) ≤ J_P ≤ nI(P) + Σ_jq_j ln(n_j+1)` by `(N+1)^{-q}e^{NH} ≤` multinomial `≤ e^{NH}`; the continuous minimiser `P′` of `I(P′) + W(P′,P)` lies in the window, where `I` is Lipschitz, and rounding it to the lattice costs `O(1)` per site type.)
(d) is the proof of Proposition 11.65(c) with `N_orb` classes: per class, outside probability `4e^{−K/24}`,
`dens_P{w > t̂_P} ≤ 2K/M`, `dens_P{w ≥ t̂_P} ≥ K/(2M)`, `â_P ∈ [½, 3/2]·E_{T_P}min(w,t̂_P)`; then `L ≤ A`, and
`A = Σ_Pπ(T_P)E_{T_P}min(w,t̂_P) + Σ_{x∈D}π(x)(w(x) − t̂_{P_x})` with `D = {w > t̂}`, where for `x ∈ D`, `y ∉ D`:
`w(x) ≤ w(y)e^{d(y,x)} ≤ t̂_{P_y}e^{d(y,x)}` (orientation (O)).  At an invariant instance `t̂_P = â_P = w_g(P)`, `L = 2A/3`,
`Tail = A·max{Φ_g(D) : maxdens(D) ≤ q}`, and the comparison with (b) is as in the binary case (if the bracket is still
too wide at `2q`, then `ln(1 + Φ_g(D)) > ε − ln 3` for some `D` of density `≤ 2q`).  ∎

*What is new here against Theorem 11.76:* nothing in substance — the remark after it already names "larger alphabets,
sites of several types".  Written out: the constants with `N_orb`; the identification of the quotient envelope
(Lemma W1.0); that the exact orbit-wise quantiles are admissible without regularisation; and the orientation of `V_n`.
*Checked by brute force* (`w06` B, 216 points, two site types, both envelopes asymmetric): 300 random members —
quantile levels admissible, truncation in the class, density `≤ q`: no violation; 200 random invariant instances and
sets — the dip formula to `7·10⁻¹⁶`, `Λ_g ≤ V_n`, `Z_gΦ_g⁺ ≤ Z_HΦ_H⁺`: no violation; `Z_H = 32.6 ≤ N_orb = 40`.

---

## 3. W2 — the single-letter theorem

### 3.1 Objects

*Known part.*  The theorem does not use that `π` is a product measure; it is stated for `f(x) = n·φ(P_x)` with `φ`
continuous on `𝒫` (a function of the joint type), `π ∝ e^{−f}`, which is `Γ`-invariant.  Rate function
`I := φ − H − min_𝒫(φ − H)`; `|J_P − nI(P)| ≤ c_n := Σ_jq_j ln(n_j+1) + n·osc_φ(1/min_jn_j)` uniformly (`o(n)`).  **Product
measure:** `φ(P) = −Σ_jλ_jE_{P_j} ln π_j`, `I(P) = Σ_jλ_jKL(P_j‖π_j)`, `0 ≤ J_P − nI(P) ≤ Σ_jq_j ln(n_j+1)`.  `v` := the largest
function with `v ≤ I` and `v(P) ≤ v(P″) + W(P″,P)`, i.e. `v(P) = min_{P′}[I(P′) + W(P′,P)]`.

*Landscapes.*  A landscape is a continuous `λ : 𝒫 → ℝ` with `λ(P) ≤ λ(P″) + W(P″, P)`, `λ ≤ I`, `min(I − λ) = 0`; its
instance is `ψ_n(x) = −nλ(P_x)` (`∈ 𝒞` by Lemma W1.0).  `λ = v`: the flat-histogram instance `H`; `λ ≡ 0`: the zero
residual; `λ = v_γ` (product measure): the additive instance `γ`.

*Labelled profiles.*  A **labelled profile** `μ` is a joint law of `(T, U, X)`: `T` the site type, `P(T = j) = λ_j`; `U` a
label in a finite set `𝒰_j`, `P(U = u | T = j) = P_j(u)`; `X ∈ 𝒮_T` with `P(X = · | T = j, U = u) = μ_{ju}`.  It describes the
class `C_μ` of all `x` such that, in a fixed partition of the sites of every type `j` into blocks `(j,u)` of sizes
`n_jP_j(u)`, the empirical law of `x` on block `(j,u)` is `μ_{ju}`.  An *exit profile* `ν` has the same labels; kernels
`X → X′` given `(T,U)` realise it.

    MI(μ)      = I(X; U | T) = Σ_j λ_j Σ_u P_j(u) KL(μ_ju ‖ μ̄_j)              (−n⁻¹ ln of the density of C_μ in its joint-type class),
    dist(ν→μ)  = Σ_j λ_j Σ_u P_j(u) W_j(ν_ju, μ_ju)                           (n⁻¹ min{d(y,x) : y ∈ C_ν, x ∈ C_μ}; = min E d_T(X′, X)),
    α(μ)       = MI(μ) + I(μ̄)                                                (−n⁻¹ ln π(C_μ); product measure: Σ_jλ_jΣ_uP_j(u)KL(μ_ju‖π_j)),
    V(μ, B; λ) = min{ MI(ν) : dist(ν→μ) + λ(ν̄) ≤ B },      r_μ(e) = V(μ, e + α(μ); λ)   (for e + α(μ) ≥ λ(μ̄)),
    R_λ(e)     = sup_μ r_μ(e)   (all finite label sets),      R̄_λ(e) = max(R_λ(e), −e),      R_H := R_v .

In words: `R_λ(e) = sup_{P_TUX} min{ I(X′;U|T) : E d_T(X′, X) + λ(P_{X′|T}) ≤ e + I(X;U|T) + I(P_{X|T}) }` — Theorem 11.78
with the label `(U, T)`, the conditional mutual information, and the oriented transport cost `E d_T(X′, X)` (exit
letter first) in place of `u|ν − μ|`.

### 3.2 The theorem

**Theorem W2 (single-letter theorem for joint-type-invariant instances) [proved; (a) for every `n`; (b), (c) by the
method of types; the every-`n` lower bound rests on `group_queries_ge` (machine-checked)].**
Let `λ` be a landscape and `ψ_n = −nλ(P_x)`.

(a) *Lower bound, every `n`.*  Let `μ` be a labelled profile on the lattice of the chain (all `n_jP_j(u)` and all
`n_jP_j(u)μ_{ju}(a)` integers), `c_μ := Σ_j q_j(|𝒰_j| + 1)`, `B > λ(μ̄) + ln 2/n`, and `D` the union of the classes `C_ν`
(same blocks) with `dist(ν→μ) + λ(ν̄) < B`.  Then

    ln(1 + Φ(D)) ≥ n(B − α_n(μ)) − ln 2 − ln N_orb,        maxdens(D) ≤ (n+1)^{c_μ} · exp(−n·V(μ, B; λ)),

(`α_n(μ) := −n⁻¹ ln π(C_μ) = α(μ) + o(1)`; the constants are for the product measure — for a general `φ` subtract `c_n`
from the first bound), so every algorithm makes at least `(1 − 2δ)(n+1)^{−c_μ}e^{nV(μ,B;λ)}`
evaluations at `ψ_n` whenever `ε < n(B − α_n(μ)) − ln(2N_orb)`: the exponent of the instance is at least `R_λ(ε₁⁺)`.

(b) *Upper bound: isoperimetry for the orbit-uniform measure.*  There is `ω_n → 0`, depending on `(m, q_max, D_max)`
and on the modulus `c_n/n` only — not on the composition, the landscape or the set — such that for all `n`, all real
`e` and all `D ⊊ X`:

    Φ⁺(D) ≥ e^{ne}      ⟹      maxdens(D) ≥ exp( −n [ R̄_λ(e − ω_n) + ω_n ] ).

Hence the hedged spot-check of Theorem 11.22(e) with samples from `½μ_n + ½·(`uniform over joint types, uniform inside
each class`)` costs `e^{nR_λ(ε₁)+o(n)}` at `ψ_n` (at continuity points of `R_λ`): **the hinted exponent of every invariant
instance is `R_λ(ε₁)`**; by Theorem W1(c), (d) the largest is `R_H`, it is attained at `H`, and at invariant instances it
is attained without a hint.

(c) *Product measure, reference `H`, in the form the nested algorithm needs.*  With `R̂` of §1.3:

    Φ_H⁺(D) ≥ e^{ne}      ⟹      μ_H(D) ≥ exp( −n [ R̂(e − ω_n) + ω_n ] )        (ω_n → 0, depending on the site types only — not on the composition),

equivalently, for `θ > ω_n`: `μ_H(D) ≤ e^{−nθ} ⟹ n⁻¹ ln Φ_H⁺(D) ≤ R̂^{-1}(θ − ω_n) + ω_n` — the tail function of `H` has
the exponent `R̂^{-1}` (`R̂^{-1}(θ) = −θ` for `θ ≥ a`).  (Uses Theorem W3(b): `V(μ, B; v) ≤ R̂(B − α(μ))` with the exit type
in the window.)

### 3.3 Lemma T′ and the proofs

**Lemma T′ (inherently typical subsets for a fixed sequence of site types) [proved; the proof of Lemma 5 of workstream A
(= Lemma T of §11.20) with the site type adjoined to the label].**  Let `ρ = ⊗_i ρ_{τ(i)}` be a product measure on `X`
(`ρ_j` of full support on `𝒮_j`), `∅ ≠ A ⊂ X`, `M ≥ 1` an integer, `α_B := −n⁻¹ ln ρ(B)`.  There are finite sets
`𝒰_j ⊂ Δ(𝒮_j)` with `|𝒰_j| ≤ (M+1)^{q_j}`, maps `u_i : Π_{i′<i}𝒮_{τ(i′)} → 𝒰_{τ(i)}`, a subset `Ã ⊂ A` and a labelled profile
`P_{TUX}` such that
 (1) every `x ∈ Ã` has the joint type `P_{TUX}` with its label sequence, i.e. the empirical law of
 `(τ(i), u_i(x^{i−1}), x_i)_{i≤n}` is `P_{TUX}`;
 (2) `ρ(Ã) ≥ ρ(A)·Π_j (n_j+1)^{−q_j(M+1)^{q_j}}`;
 (3) `α_A − q_max/M ≤ α := D(P_{X|UT} ‖ ρ_T | P_{UT}) ≤ α_Ã`;
 (4) for `Xⁿ ∼ ρ(·|Ã)`, `I` uniform on `[n]` and `V = (I, X^{I−1})`:
 `I(X_I; V | U_I, T_I) = α_Ã − α ≤ η_{M,n} := q_max/M + Σ_j q_j(M+1)^{q_j} ln(n+1)/n`.
*Proof.*  Let `p_i(·|x^{i−1})` be the conditional laws of `ρ(·|A)` and
`u_i(x^{i−1})(a) := ⌈M p_i(a|x^{i−1})⌉ / Σ_b⌈M p_i(b|x^{i−1})⌉` — a law on `𝒮_{τ(i)}` with at most `(M+1)^{q_{τ(i)}}` values and
`p_i ≤ (1 + q_{τ(i)}/M)·u_i` pointwise.  Partition `A` by the joint type of `((τ(i), u_i(x^{i−1}), x_i))_i` (at most
`Π_j(n_j+1)^{q_j(M+1)^{q_j}}` classes) and let `Ã` be the most `ρ`-probable class: (1), (2).  For `x ∈ Ã`:
`ρ(x)/ρ(A) = Π_ip_i(x_i|x^{i−1}) ≤ (1 + q_max/M)ⁿ Π_iu_i(x^{i−1})(x_i)`; taking logarithms and using (1),
`α_A ≤ q_max/M + Σ P_{TUX}(j,u,a) ln(u(a)/ρ_j(a)) = q_max/M + α − D(P_{X|UT}‖U|P_{UT}) ≤ q_max/M + α`.  Under `ρ(·|Ã)`,
`(T_I, U_I, X_I) ∼ P_{TUX}` by (1), `(T_I, U_I)` is a function of `V`, and by the chain rule
`α_Ã = n⁻¹D(P_{Xⁿ}‖ρ) = D(P_{X_I|V}‖ρ_{T_I}|P_V) = α + I(X_I; V | U_I, T_I)`.  ∎
(Brute force, `w08`(i): 3 ternary + 3 binary sites, 120 sets of four kinds, `M = 1, 2, 3, 5`: (2), (3), (4) hold in all
480 cases.)

*Proof of Theorem W2(a).*  The normalised landscape of `ψ_n` is `Λ = nλ + c`, `c = min_P[J_P − nλ(P)] ≥ 0`, and
`Z ≤ N_orb` (Theorem W1(c)).  For `x ∈ C_μ` and `y ∉ D`, with `ν` the block profile of `y`:
`d(y,x) ≥ n·dist(ν→μ)` (block by block the cost is at least the transport cost), so `d(y,x)/n + λ(P_y) ≥ B`; by the
formula of Theorem W1(c), `Φ⁺(D) ≥ π(C_μ)e^{nB}/N_orb`, and the points of `C_μ` have slack at least
`n(B − λ(μ̄)) > ln 2`, so `Φ(D) ≥ ½π(C_μ)e^{nB}/N_orb`.  A class `C_ν ⊂ D` satisfies the closed constraint of `V`, so
`MI(ν) ≥ V(μ,B;λ)`; its density in its joint-type class is at most `Π_j(n_j+1)^{q_j}e^{−nMI(ν)}` (multinomial bounds), and
a joint-type class contains at most `Π_{j,u}(n_jP_j(u)+1)^{q_j−1}` classes.  Now Theorem W1(b).  ∎

*Proof of Theorem W2(b)* — the six steps of the proof of Theorem 11.63/11.78(b); **what changes is marked ▶.**
Put `δ = n^{−1/4}`, `δ₁ = δ/((2 + mq_max)·max(D_max, 1))`, `M = ⌈n^{1/(2q_max+2)}⌉` (so `η_{M,n} → 0`).
*Step 1 (one piece).*  `Φ⁺(D) = Z⁻¹Σ_{x∈D}π(x)e^{nB(x)+c}`, `B(x) := min_{y∉D}[λ(P_y) + d(y,x)/n]`.  ▶ Round `B(x)` down to a
multiple of `1/n` (at most `n(D_max + osc λ) + 1` values, a factor `e` lost) and split `D` by this value **and by the joint
type of `x`**; fix the piece `C ⊂ T_P` with the largest `π(C)e^{nB}`.  With `α_C := −n⁻¹ln(|C|/|T_P|)` (the density exponent of `C`):
`e ≤ B − I(P) − α_C + o(1)`, and (∗): every `y` with `λ(P_y) + d(y,x)/n < B` for some `x ∈ C` lies in `D`.  `λ(P) ≤ B`, because
`λ(P_x) ≤ λ(P_y) + W(P_y,P_x) ≤ λ(P_y) + d(y,x)/n` — the orientation of the landscape condition is the one needed here.
*Step 2.*  ▶ Lemma T′ for `C` with the product measure `ρ = ⊗_iP_{τ(i)}`, **which is uniform on `T_P`, as `π` is** (this is
where §11.20 used that `π` is a product measure; §11.23 used `Bernoulli(k/n)ⁿ`): `C̃ ⊂ C`, labels `u_i`, a labelled profile
`μ := P_{TUX}` with `μ̄ = P` exactly, so `α = I(X;U|T) = MI(μ)`, and `α_C − q_max/M ≤ MI(μ) ≤ α_{C̃} + o(1) ≤ α_C + o(1)`
(the `ρ`-exponents of the lemma are the density exponents plus `−n⁻¹ln ρ(T_P) ∈ [0, Σ_jq_j ln(n_j+1)/n]`).
*Step 3 (shallow piece, `B < λ(P) + 3δ`).*  `maxdens(D) ≥ dens_P(C̃) = e^{−nα_{C̃}}` and
`α_{C̃} ≤ B − I(P) − e + o(1) ≤ (λ − I)(P) + 3δ − e + o(1) ≤ −e + o(1)`: the term `−e` of `R̄`.
*Step 4 (deep piece).*  By the definition of `V` there are kernels `W_j(x′|x,u)` with ▶ `E d_T(X′,X) + λ(P_{X′|T}) ≤ B − 2δ`
(an optimal coupling of `ν_{ju}` and `μ_{ju}` for every label) and `I(X′;U|T) = V(μ, B−2δ; λ) ≤ R_λ(B − 2δ − α(μ))`.  Draw `Xⁿ`
uniformly from `C̃` and `X′_i ∼ W_{τ(i)}(·|x_i, u_i(x^{i−1}))` independently.  ▶ Given `x ∈ C̃`, `d(X′ⁿ, x) = Σ_id_{τ(i)}(X′_i,x_i)`
is a sum of independent variables in `[0, D_max]` with mean `n·E d_T(X′,X)` (the joint type of `(τ(i),u_i,x_i)` is `μ` for
every `x ∈ C̃`), and for every `(j,b)` the number of sites of type `j` with `X′_i = b` is a sum of independent indicators
with mean `nλ_jP_{X′|T=j}(b)`; by Hoeffding, outside probability `θ_n := 2(1 + mq_max)e^{−2nδ₁²}`, all of them are within
`nδ₁·max(D_max,1)` of their means, hence `d(X′ⁿ,x)/n + λ(P_{X′ⁿ}) ≤ B − 2δ + δ₁D_max(1 + mq_max/2) ≤ B − δ < B`
(`λ(P′) ≤ λ(Q) + W(Q,P′)`, and `W` is at most `D_max` times the weighted total-variation distance) and `X′ⁿ ∈ D` by (∗).
*Step 5 (chain rule).*  With `Q_j := P_{X′|T=j}` and `Q^⊗ := ⊗_iQ_{τ(i)}`: since `X′^{i−1} — X^{i−1} — X′_i` is a Markov chain,
`n⁻¹D(P_{X′ⁿ}‖Q^⊗) ≤ n⁻¹Σ_iD(P_{X′_i|X^{i−1}}‖Q_{τ(i)}|P_{X^{i−1}}) = I(X′_I; V | T_I) = I(X′_I;U_I|T_I) + I(X′_I;V|U_I,T_I)
≤ I(X′;U|T) + I(X_I;V|U_I,T_I) ≤ I(X′;U|T) + η_{M,n}` (▶ everything conditional on the site type `T_I`, which is a function of
`V`; given `(U_I,T_I)`, `V — X_I — X′_I` is Markov; Lemma T′(4)).
*Step 6.*  Data processing for the event `D`: `(1 − θ_n) ln(1/Q^⊗(D)) − ln 2 ≤ D(P_{X′ⁿ}‖Q^⊗)`.  ▶ For every `y` and every
product measure of this form, `Q^⊗(y) ≤ Π_je^{−n_jH(P_{y,j})} ≤ 1/|T_{P_y}|`, so `Q^⊗(D) ≤ Σ_P dens_P(D) ≤ N_orb·maxdens(D)`: the
orbit-uniform measure dominates every such product measure up to the number of joint types.  Altogether
`−n⁻¹ ln maxdens(D) ≤ [R_λ(B − 2δ − α(μ)) + η_{M,n} + ln 2/n]/(1 − θ_n) + n⁻¹ln N_orb` with `B − α(μ) ≥ e − o(1)`; `R_λ` is
nonincreasing and bounded by `Σ_jλ_j ln q_j`, and all error terms depend on `(n, m, q_max, D_max, c_n/n)` only.  ∎

*Proof of Theorem W2(c).*  Steps 1–5 with `λ = v` and `I = Σλ_jKL(·‖π_j)`; in Step 4 use Theorem W3(b) instead of the
definition: kernels with `E d_T(X′,X) + v(P_{X′|T}) ≤ B − 2δ`, `I(X′;U|T) ≤ R̂(B − 2δ − α(μ))` **and `Q = P_{X′|T}` in the
window**.  Step 6 is that of Theorem 11.63: let `𝒯` be the set of `y` whose letter counts are within `nδ₂` of those of
`Q`, `δ₂ := δ₁·max(D_max,1)` (probability `≥ 1 − θ_n` by Step 4).  For every `y`, `π(y) = e^{−n[H(P_y) + I(P_y)]}`, so
`μ_H(y) = π(y)e^{nv(P_y)}/Z_H ≥ Q^⊗(y)·e^{−n(I − v)(P_y)}/N_orb`.  ▶ `I − v ≥ 0` is continuous on the compact `𝒫` and vanishes on
the window; on `𝒯`, `λ_j‖P_{y,j} − Q_j‖₁ ≤ q_jδ₂`, so `(I − v)(P_y) ≤ ω′(δ₂) := max_jω_j(q_max√δ₂) + m√δ₂ ln(1/π_min) → 0`
(`ω_j` the modulus of `KL(·‖π_j) − v_j` at the window; site types with `λ_j < √δ₂` contribute at most `λ_j ln(1/π_min)`) —
uniform continuity replaces the quadratic bound of the binary proof, and the estimate is uniform in the composition.
Then `μ_H(D) ≥ Q^⊗(D∩𝒯)e^{−nω′}/N_orb`.  In the shallow case `μ_H(D) ≥ μ_H(C̃) = π(C̃)e^{nv(P)}/Z_H` gives `−e + o(1) ≤ R̂(e) + o(1)`.
The inverse form follows because `R̂` is nonincreasing with slopes in `[−1,0]` (Theorem W3(d)).  ∎

**Which steps of Theorem 11.78 change — summary.**  (1) Types → joint types, `n+1 → N_orb` (Steps 1, 6).  (2) Lemma T →
Lemma T′: the site type is part of the label, the alphabet is general, and the lemma is applied with the product
measure `⊗_iP_{τ(i)}` that is uniform on the joint-type class (Step 2).  (3) The Hamming distance of block counts →
the oriented transport cost: kernels are optimal couplings, the Hoeffding step is for `Σ_id_{τ(i)}(X′_i,x_i)` and for all
letter counts (Step 4).  (4) Mutual informations are conditional on the site type (Step 5).  (5) For the `μ_H`-form:
the window step and the continuity of `I − v` (Theorem W3(b), Step 6).  Unchanged: the architecture, the shallow/deep
dichotomy, the chain rule, data processing.  *What the theorem does not give:* the value of the supremum `R_λ` — §4 for
product measures.

---

## 4. W3 — evaluation: product known parts are the convex case

Throughout this section `π` is the product measure, `I = Σ_jλ_jKL(·‖π_j)`, and the notation of §1.3 is used.  For a
labelled profile `μ`, an additive instance `γ` and `τ ≥ 0` put
`φ_{μ,γ}(τ) := min_ν [ MI(ν) + τ( dist(ν→μ) + v_γ(ν̄) − α(μ) ) ]` (the Lagrangian of `r_μ` at the instance `γ`).

**Theorem W3 (evaluation of the single-letter supremum) [proved].**

(a) *Collapse to additive instances.*  For every labelled profile `μ` and `B ≥ v(μ̄)`:
`V(μ, B; v) = max_{γ∈ΠL_j} V(μ, B; v_γ)`.  Hence `R_H = max_γ R_{v_γ}`: **the flat-histogram instance is exactly as hard as
the hardest additive instance.**

(b) *Evaluation lemma; vertex labels suffice.*  For `0 ≤ τ ≤ 1` and every `γ`:

    sup_μ φ_{μ,γ}(τ) = Σ_j λ_j F_j(γ_j, τ),

attained by the **generalised-dip profile**: labels `𝒰_j = 𝒱_j` (vertices of the Lipschitz polytope of the site),
`P_j = M_j*` an optimal strategy of the adversary in the game `K_τ^{γ_j}`, letter laws `μ_{jφ} = π_φ` (the Gibbs law of the
vertex); at most `q_j` labels of type `j` carry weight.  Consequently, for every labelled profile `μ` and `B ≥ v(μ̄)`
there are kernels with `E d_T(X′,X) + v(P_{X′|T}) ≤ B`, `P_{X′|T}` in the window, and `I(X′;U|T) ≤ R̂(B − α(μ))`; and

    R_H(e) = R̂(e) = max_{0≤t≤1} [ Σ_j λ_j F*_j(t) − t e ]   for e ≥ 0,        R̄_H ≤ R̂ on ℝ,
    R_{v_γ}(e) = max_{0≤t≤1} [ Σ_j λ_j F_j(γ_j, t) − t e ]   for e ≥ 0          (every additive instance).

In particular **`F*(t) = Σ_jλ_jF*_j(t)` with one common `t`**: Proposition F12(iii) is correct.  (With Theorem W2 and the
every-`n` bound of §5 this also proves, for several site types, the hinted exponent of every additive instance —
Theorem A of workstream A, which was a sketch for more than one site type.)

(c) *Closed variational form (new).*  For a site `(π_j, d_j)` and `0 < t < 1`:

    F*_j(t) = max_{M ∈ Δ(𝒱_j)}  −t · ln Σ_a ( Σ_φ M(φ) π_φ(a)^t )^{1/t}  =  min_Q max_{φ∈𝒱_j} (1 − t)·D_t(π_φ ‖ Q)  =  (1 − t)·C_t(𝒲_j),

where `D_t` is the Rényi divergence of order `t` and `C_t(𝒲_j)` the Rényi capacity (= Rényi radius) of order `t` of the
channel "vertex `φ` ↦ Gibbs law `π_φ`" — equivalently of the whole window `𝒲_j = {π_γ : γ ∈ L_j}`.  The maximising
instance is unique: **the hardest additive instance at slope `t` is the one whose Gibbs law is the Rényi centre,**
`π_{γ*(t)}(a) ∝ (Σ_φ M*(φ) π_φ(a)^t)^{1/t}`, and the labels that carry weight are exactly at Rényi distance `C_t` from it.
The first expression is a smooth convex programme in `M`.  Limits:

    E_j := lim_{t↓0} F*_j(t)/t = max_M −ln Σ_a Π_φ π_φ(a)^{M(φ)} = min_Q max_φ KL(Q ‖ π_φ),
    a_j := lim_{t↑1} F*_j(t)/(1−t) = max_M I(M; π_·) = min_Q max_φ KL(π_φ ‖ Q)      (the Shannon capacity of the vertex channel);

`F*_j(t)/t` is nonincreasing and `F*_j(t)/(1−t)` nondecreasing in `t`.

(d) *Game function.*  `F*` is continuous on `[0,1]`, `F*(0) = F*(1) = 0`, `F*(t) ≤ a(1−t)`, `F*(t) ≤ E·t`, with the sharp
constants `E = Σ_jλ_jE_j > 0` (unless every `d_j ≡ 0`) and `a = Σ_jλ_ja_j`: the hypotheses of `GameFunction F* E a`
(`GamePair.lean`).  So Theorem 11.66 **[V]** applies: `R̂` is convex, nonincreasing, with slopes in `[−1,0]`, vanishes
exactly on `[E, ∞)`, `R̂(e) = −e` for `e ≤ −a`; `S` is strictly increasing on `[−a, ∞)`; `(θ_na, R̂)` with
`θ_na := R̂∘S^{-1}` is a `HintPair` with constants `a`, `h = R̂(0)`, `E`; `θ_na(x) = max_{0≤τ<1}(F*(τ) − τx)/(1−τ)`; and the
level recursion built on `θ_na` converges to `R̂`.  **`F*` need not be concave** (Proposition W3.2).

(e) *Non-adaptive algorithms.*  The exponent of non-adaptive algorithms without a hint is `θ_na(ε₁) = R̂(S^{-1}(ε₁))`
for `0 < ε₁ < E`, attained by the joint-type-stratified sample (equivalently, importance sampling from `μ_H`); the
lower bound holds for every `n` (generalised cones with vertex labels, truncated at the orbit-wise quantiles).  In
max–min form, with `𝒟(ν) := Σ_jλ_jΣ_φM_j(φ)KL(ν_{jφ}‖π_φ)` (the divergence from the Gibbs law of the generalised cone):

    θ_na(x) = max_{M} min{ MI(ν) : 𝒟(ν) ≤ x },      x_na(θ) = max_M min{ 𝒟(ν) : MI(ν) ≤ θ } = S(R̂^{-1}(θ)) .

*Proof.*
(a) `g(ν) := dist(ν→μ) + v(ν̄) − B` and `MI` are convex and continuous on the compact convex set of exit profiles
(`W_j(·, μ_{ju})` is the value of a linear programme, `v` is convex), and `g(μ) ≤ 0`.  By Sion's theorem
`V = sup_{τ≥0} min_ν[MI + τg]` (compactness on the minimising side; linear in `τ`), and for fixed `τ`,
`min_ν max_γ[MI(ν) + τ(dist + v_γ(ν̄) − B)] = max_γ min_ν[…]` (convex in `ν`; concave in `γ`, because `ln Z_γ` is convex;
`γ` normalised by `γ_j(a₀) = 0` ranges over a compact convex set).  The inner problem is the Lagrangian of `V(μ,B;v_γ)`,
and `V(μ,B;v_γ) ≤ V(μ,B;v)` trivially (`v_γ ≤ v`).
(b) *Upper bound.*  Fix `γ`, `τ ∈ [0,1]`, `μ`.  `MI(ν) = min_Q Σ_jλ_jΣ_uP_j(u)KL(ν_{ju}‖Q_j)`, so for every `Q` of full support

    φ_{μ,γ}(τ) ≤ Σ_j λ_j Σ_u P_j(u) [ min_ν { KL(ν‖Q_j) + τW_j(ν, μ_ju) − τE_νγ_j } − τ ln Z_{γ_j} − τKL(μ_ju‖π_j) ] :

**the problem separates over the site types** (this is the whole content of "one common `t`").  For one label, by
Kantorovich duality (§1.2), Sion (convex in `ν`, linear in `φ ∈ L_j`, both compact) and the Gibbs variational principle,
`min_ν{…} = max_{φ∈L_j}[−ln E_{Q_j}e^{−τ(φ−γ_j)} − τE_{μ_{ju}}φ]`; by Donsker–Varadhan, `−E_μφ ≤ KL(μ‖π_j) + ln Z_φ`.  The
terms `τKL(μ_{ju}‖π_j)` cancel and

    φ_{μ,γ}(τ) ≤ Σ_j λ_j max_{φ∈L_j} g^{(j)}_{Q_j}(φ),      g_Q(φ) := −ln Σ_a Q(a) (π_φ(a)/π_γ(a))^τ .

For `τ ≤ 1` the maximum of `g_Q` over the polytope `L_j` is attained at a vertex (Lemma 3(c) of workstream A, re-derived:
in the relative interior of a face of positive dimension take a direction `1_C`; at a critical point the two tilted
laws give `C` the same mass `p ∈ (0,1)` and the second derivative is `τ(1−τ)p(1−p) > 0`; `τ = 1` by continuity).
Minimising over `Q_j`: `φ_{μ,γ}(τ) ≤ Σ_jλ_j min_Q max_{φ∈𝒱_j} g_Q(φ) = Σ_jλ_jF_j(γ_j,τ)`.
*Attained.*  For the generalised-dip profile, `W_j(ν_φ, π_φ) ≥ E_{ν_φ}φ − E_{π_φ}φ` and
`α(μ) = Σ_jλ_jΣ_φM_j(φ)[−E_{π_φ}φ − ln Z_φ]`, so `dist(ν→μ) + v_γ(ν̄) − α(μ) ≥ Σ_jλ_jΣ_φM_j(φ)E_{ν_{jφ}}[φ̃ − γ̃_j]` and
`φ_{μ,γ}(τ) ≥ Σ_jλ_j min_Q Σ_φM_j(φ)[−ln Σ_aQ(a)K_τ^{γ_j}(a,φ)] ≥ Σ_jλ_j[−ln max_a (K_τ^{γ_j}M_j)(a)] = Σ_jλ_jF_j(γ_j,τ)`
(Jensen for `−ln`; `M_j` optimal).  An optimal strategy in a game with `q_j` rows can be taken with at most `q_j`
columns in its support (a basic optimal solution; by (c) also: a point of the boundary of a convex hull in `ℝ^{q_j}`).
*Consequences.*  By (a) and Sion, `V(μ,B;v) = sup_τ max_γ[φ_{μ,γ}(τ) − τ(B − α(μ))]`.  For `τ ≤ 1` the bracket is at most
`F*(τ) − τ(B−α) ≤ R̂(B−α)`.  For `τ ≥ 1` take `ν = μ`: the bracket is at most
`MI(μ) + τ(v_γ(μ̄) − B) ≤ MI(μ) + v(μ̄) − B ≤ α(μ) − B ≤ R̂(B−α)` (`v_γ(μ̄) − B ≤ 0`, `v ≤ I`, `R̂(e) ≥ F*(1) − e`).  Hence
`V(μ,B;v) ≤ R̂(B − α(μ))`, `R_H ≤ R̂`, `R̄_H ≤ R̂`; and `R_H(e) ≥ r_{μ*}(e) ≥ φ_{μ*,γ*}(t*) − t*e = R̂(e)` for `e ≥ 0` at the
generalised-dip profile of the maximising `(t*, γ*)`.  The same with a fixed `γ`.
*Window step.*  If the kernel found has exit type `P′ := P_{X′|T}` outside the window, let `P″` minimise
`I(P″) + W(P″, P′)` and pass `X′` through an optimal coupling kernel `X′ → X″` (depending on the site type and on the
letter only).  Then `P″` is in the window (`v(P′) ≤ v(P″) + W(P″,P′)` and `v(P′) = I(P″) + W(P″,P′)` give `I(P″) ≤ v(P″)`),
`I(X″;U|T) ≤ I(X′;U|T)` (data processing), `E d_T(X″,X) ≤ E d_T(X″,X′) + E d_T(X′,X)` (triangle inequality, in this
order) and `v(P″) = v(P′) − W(P″,P′)`: the constraint is preserved.  (For two states this is the thinning of §11.20.)
(c) By the minimax theorem for matrix games,
`F_j(γ,t) = −ln min_M max_a Σ_φM(φ)K_t^γ(a,φ) = max_M min_a t·ln(π_γ(a)/m_M(a))`, `m_M(a) := (Σ_φM(φ)π_φ(a)^t)^{1/t}`.  For
any probability vector `P`, `min_a ln(P(a)/m(a)) ≤ −ln Σ_am(a)`, with equality iff `P = m/Σm` (if `P ≥ c·m` then
`1 ≥ cΣm`).  So `F_j(γ,t) ≤ max_M[−t ln Σ_am_M(a)] =: max_MG_t(M)` for every `γ`, with equality iff `π_γ ∝ m_{M*}`.  That
instance is in the class: `γ* := −ln(m_{M*}/π_j)` has
`γ*(a) − γ*(b) = t⁻¹ ln[Σ_φM(φ)e^{−tφ̃(b)} / Σ_φM(φ)e^{−tφ̃(a)}] ≤ d_j(a,b)`, because `e^{−tφ̃(b)} ≤ e^{−tφ̃(a)+td_j(a,b)}` for
every `φ ∈ L_j` — `L_j` is closed under soft minima.  `N_t(M) = Σ_a(Σ_φM(φ)π_φ(a)^t)^{1/t}` is convex in `M` (`x ↦ x^{1/t}`
is convex and increasing) and depends on `M` only through `s = Σ_φM(φ)π_φ^t ∈ ℝ^{q_j}`, in which it is strictly convex:
`s*`, the centre `Q* = m/Σm` and `γ*` are unique.  The Karush–Kuhn–Tucker conditions of `min_MN_t` read
`(1−t)D_t(π_φ‖Q*) ≤ −t ln N_t(M*)` for every vertex, with equality on the support of `M*`; and for every `γ`, `Q`,
substituting `Q′ ∝ Q^{1−t}π_γ^t` in `F_j(γ,t) = min_{Q′}max_φ g_{Q′}(φ)` gives
`F_j(γ,t) ≤ max_φ(1−t)[D_t(π_φ‖Q) − D_t(π_γ‖Q)] ≤ max_φ(1−t)D_t(π_φ‖Q)`.  Together: the second expression.  `G_t(M)` is
`(1−t)` times Sibson's information of order `t`; that `max_M` of it is the Rényi radius is Csiszár's theorem
(**[known]**; here proved directly).  Limits: `G_t(M) = min_Q −ln Σ_φM(φ)Σ_aπ_φ(a)^tQ(a)^{1−t}` is concave in `t` and
vanishes at `0`, so `G_t(M)/t` is nonincreasing and its supremum is the limit `t ↓ 0`, where the power mean becomes the
geometric mean; the dual form by the same Karush–Kuhn–Tucker argument.  `D_t` is nondecreasing in the order and tends
to `KL` as `t ↑ 1` (**[known]**, elementary), hence `C_t ↑ C_1`.
(d) Continuity on `(0,1)` from the min–max form (`(1−t)D_t(P‖Q) = −ln ΣP^tQ^{1−t}` is jointly continuous for `P` of full
support); `F*_j(t) ≤ E_jt` and `≤ a_j(1−t)` by the monotonicity in (c), which also gives the two sharp constants for the
sum (`F*(t)/t = Σλ_jF*_j(t)/t` is nonincreasing, `F*(t)/(1−t)` nondecreasing).  `E_j = 0` iff all `π_φ` coincide iff
`L_j/ℝ` is a point.
(e) *Lower bound, every `n`.*  Let `μ` be a lattice profile with site functions `φ_{ju} ∈ L_j` as labels and
`ψ(x) = Σ_iφ_i(x_i)` the **generalised cone** (`φ_i = φ_{ju}` on block `(j,u)`): an additive, non-invariant member of `𝒞`
whose weight is constant on the classes `C_ν`, with `π(C_ν)w(C_ν) = exp(−n[𝒟(ν) − Σ_jλ_jΣ_uP_j(u)ln Z_{φ_{ju}}] + O(c_μ ln n))`.
For `q = e^{−nθ}` and a joint type `P`: the classes with `w ≥ t_P` have total density `≥ q` (Theorem W1(a)(i)), so one of
them has density `≥ q/N_c` (`N_c ≤ (n+1)^{c_μ}` classes per joint type) and therefore `MI ≤ θ + c_μ ln(n+1)/n ≤ θ″ := θ + 2c_μ ln(n+1)/n`
("seen"); a class with `MI > θ″` has density `≤ q/N_c` and contributes at most `(q/N_c)t_P` to `E_{T_P}min(w,t_P)`.  Hence
`A(ψ^{tr,q}) ≤ 2N_cN_orb·max_{ν seen}π(C_ν)w(C_ν)`, `A(ψ) ≥ max_νπ(C_ν)w(C_ν)`, and

    ln[A(ψ)/A(ψ^{tr,q})] ≥ n·min{ 𝒟(ν) : MI(ν) ≤ θ + 2c_μ ln(n+1)/n } − c ln(n+1) − c′

(no unimodality is needed: this is the argument of Theorem 11.79(a), which replaces the binary log-concavity argument
of Theorem 11.61(c)).  With Theorem W1(a)(ii): non-adaptive algorithms need `(1−2δ)e^{nθ}` evaluations whenever
`ε₁ < min{𝒟 : MI ≤ θ} − o(1)`.  *Single-letter value.*  For `x > 0` the programme `n_M(x) = min{MI(ν) : 𝒟(ν) ≤ x}` is strictly
feasible at the cone law, so `n_M(x) = max_{s≥0}min_ν[MI + s(𝒟 − x)]`; with `τ = s/(1+s)` and
`min_ν[KL(ν‖Q) + sKL(ν‖P)] = D_τ(P‖Q)`:
`n_M(x) = max_{0≤τ<1}[(1−τ)A_τ(M) − τx]/(1−τ)`, `A_τ(M) := Σ_jλ_j min_QΣ_φM_j(φ)D_τ(π_φ‖Q)`.  `max_M(1−τ)A_τ(M) = F*(τ)`
(linear in `M`, convex in `Q`: Sion, then (c)).  So `max_Mn_M(x) = max_{τ<1}(F*(τ) − τx)/(1−τ) = R̂(S^{-1}(x))` (the argument
of Theorem F2(e): at the maximiser `τ*`, `F*(τ) − τ(x − θ*) ≤ θ*` with equality at `τ*`).
*Upper bound* (the proof of Theorem 11.61(d) in the orientation (O)): let `q = e^{−nθ}`, `D = {w > t_{P_x}}`,
`T := max_Pπ(T_P)t_P`.  `A(ψ^{tr}) ≥ Σ_Pπ(T_P)t_Pdens_P{w ≥ t_P} ≥ qT`.  By Theorem W1(a)(i),
`t_P ≤ t_{P′}e^{δ(P′,P)} ≤ T·e^{J_{P′} + δ(P′,P)}` for all `P′`, i.e. `t_P ≤ Te^{V_n(P)} ≤ T·poly(n)·e^{nv(P)}`; for `x ∈ D`, `y ∉ D`:
`w(x) ≤ w(y)e^{d(y,x)} ≤ t_{P_y}e^{d(y,x)}`.  Hence `A(ψ) − A(ψ^{tr}) ≤ poly(n)·T·Z_H·Φ_H⁺(D)` with `μ_H(D) ≤ maxdens(D)·poly ≤ q·poly`,
and Theorem W2(c) bounds `Φ_H⁺(D)` by `exp(n[R̂^{-1}(θ)] + o(n))`: `ε_n^{tr}(e^{−nθ}) ≤ n[θ + R̂^{-1}(θ)] + o(n) = nS(R̂^{-1}(θ)) + o(n)`.
With Theorem W1(a)(iii) and the continuity of `θ_na`.  ∎

**Remark W3.1 (a dictionary with channel coding) [the identities proved in (c), (e); the names known].**  For the
"vertex channel" `W_j(a|φ) = π_φ(a)` of every site type, with Gallager's function
`E_0(ρ) = Σ_jλ_j max_M −ln Σ_a(Σ_φM(φ)π_φ(a)^{1/(1+ρ)})^{1+ρ} = ρ·Σ_jλ_jC_{1/(1+ρ)}(𝒲_j)` and the sphere-packing exponent
`E_sp(θ) = sup_{ρ≥0}[E_0(ρ) − ρθ]`:

    F*(t) = t·E_0((1−t)/t),      R^max(e) = max_{ρ≥0} (E_0(ρ) − e)/(1+ρ),      θ_na(x) = max_{ρ>0} (E_0(ρ) − x)/ρ = E_sp^{-1}(x),
    x_na(θ) = E_sp(θ),      e_hint(θ) = E_sp(θ) − θ   (the shear law),      E = E_sp(0⁺),      a = capacity   (E_sp(a) = 0),

and `h = R^max(0)` is the fixed point of the sphere-packing exponent, `E_sp(h) = h`.  *With a budget of `e^{nθ}` evaluations a
fixed sample certifies the accuracy rate `E_sp(θ)`; an adaptive algorithm, or one with a hint, certifies `E_sp(θ) − θ`.*
The max–min form of (e) is the Csiszár–Körner form `E_sp(θ) = max_M min{D(V‖W|M) : I(M,V) ≤ θ}` of that exponent:
the Gibbs law of a generalised cone is the output law of the channel for the "codeword" `φ⃗`, a sample of `e^{nθ}` points
per joint type sees exactly the outputs whose empirical mutual information with `φ⃗` is at most `θ`, and truncating the
cone removes the rest.  On the uniform cube the channel is the binary symmetric channel with crossover
`p_u = 1/(1+e^u)`: `a = ln 2 − h(p_u)`, `E = −ln(2√(p_u(1−p_u))) = ln cosh(u/2)`, `E_sp(θ) = KL(ρ‖p_u)` at `KL(ρ‖½) = θ` — the
formulas of §11.16.  (Numerical check of the dictionary on the path site: `w08`(vi).)  I did not find this
identification in the theory report; whether it is useful beyond naming things — for instance known bounds on `E_0`,
or Arimoto's algorithm for `C_t` — is open.

**Proposition W3.2 (the exponents of site types do not add; `F*` need not be concave)
[inequalities proved; numbers numerical, certified].**
(a) Let `R_j(e) := max_t[F*_j(t) − te]` be the exponent of a chain of sites of type `j` alone.  Then for every `e`

    R^max(e)  ≤  R^split(e) := min_{Σ_jλ_je_j = e} Σ_j λ_j R_j(e_j)  ≤  Σ_j λ_j R_j(e) ,

`R^split(e) = max_t[Σ_jλ_j conc(F*_j)(t) − te]` (`conc` = concave envelope on `[0,1]`).  The first inequality is an equality
iff the maximiser `t*` of the middle expression has `conc(F*_j)(t*) = F*_j(t*)` for all `j` — in particular whenever all
`F*_j` are concave; the second iff all `R_j` have a common slope at `e`.  The thresholds and the non-adaptive exponents at
vanishing accuracy **do** add (`E = Σλ_jE_j`, `a = Σλ_ja_j`); in between the site types share one slope `t*`, and each type
`j` works at its own accuracy `e_j = e_j(t*) < E_j`.
(b) *For two states `F*_j` is concave in all cases computed* (100 sites: `u ∈ {0.3, 1, 2, 4}`, 25 fields in `[0, 6]`,
201 values of `t`: largest second difference `−5·10⁻⁹`) **[numerical]**; I have no proof.
(c) *For three states it need not be* **[numerical, certified brackets]**: for the triangle site of §6 the optimal mix
`M*(t)` jumps at `t_c = 0.378` from {dip at 2, anti-dip at 2, dip at 0} with weights `(0.506, 0.431, 0.063)` to the three
dips with weights `(0.466, 0.389, 0.145)`; `F*` has a convex kink there (slope jump `+0.0052`), `R^max` has a corner at
`e_c = 0.1996·E` (slope `−0.383 → −0.373`), and the hardest instance `γ*` is continuous through it.  For the chain `mix2`
the first inequality of (a) is strict near the switch (by `8·10⁻⁷`, relative `2.5·10⁻⁵`: small, but not zero).
*Why:* `F*_j(t) = −t ln min_{s∈conv{π_φ^t}}Σ_as_a^{1/t}` — the minimiser `s*(t)` is unique and moves continuously, but the
face of the hull that carries it can flip when four vertex points become coplanar (possible from `q_j = 3` on, when
`|𝒱_j| > q_j`); for fixed `M`, `t ↦ G_t(M)` is concave, and `F*_j` is an upper envelope of such functions.
*Proof of (a).*  `Σ_jλ_jR_j(e_j) = Σ_jλ_j max_{t_j}[F*_j(t_j) − t_je_j] ≥ max_tΣ_jλ_j[F*_j(t) − te_j] = R^max(e)`; the minimum over
splits is the infimal convolution, whose conjugate is the sum of the conjugates; `R_j` is the conjugate transform of
`conc(F*_j)` as well.  ∎

*Checks of this section.*  (i) Controls of the brief, all reproduced by the general code (`w01`): `p = 0.1`, `u = 2`:
`E = 0.212295`, `R^max(0) = 0.048130`, `R^max(0.3E) = 0.023270`, `θ_na(0.3E) = 0.036246`; `p = ½`, `u = 1`: `0.029139`;
two binary types, fields `0` and `3`: `0.008557` against the average `0.009790` at `0.3E` with the threshold
`E = 0.072290` — the brief's `0.008559`/`0.009791` are at `E = 0.072271`, the finite difference `F*(t)/t` at `t = 1/4000` of the
reference script, and are reproduced exactly with that value (`w01`; the same slip as DEAD_ENDS D49, item 11); and from Theorems 11.27/11.28: flat four-state site `0.02914`/`0.02841`, site `(0,0,2)`:
`0.02903`/`0.02467`, thresholds `0.11969`, `0.0947`, `0.11988`.  (ii) (c) against the game: the bracket
`[G_t(M), (1−t)max_φD_t(π_φ‖Q_M)]` closes to `≤ 6·10⁻¹⁰`, the linear-programming value of the game at `γ*` agrees to
`3·10⁻¹⁶`, and a blind grid-and-zoom search over `γ` never exceeds it (42 points, six sites; `w01`).  (iii) (a), (b), (e)
with the **primal** solver (`w02`; minimisation over couplings by SLSQP — no duality, no vertices, no `t`): at the
generalised-dip profile `r_{μ*}(e)` equals `R^max(e)` to `≤ 5·10⁻¹⁴` with the landscape `v` (second-stage coupling), with
`I` itself, and with `v_{γ*}`, for six chains at `e/E = 0, 0.3, 0.6`; 30 random profiles (1–3 labels per type) and 30
perturbations of `μ*` per case never exceed it (the perturbations come within `2·10⁻⁵`); at a negative accuracy the
admissible random profiles stay below `R̂`; the collapse (a) holds to `≤ 8·10⁻¹⁴` on 36 profiles with positive value; the
cone formula of (e) at `M*` equals `R̂(S^{-1}(x))` to `10⁻⁹` (this is the pair identity `θ_na(e + R(e)) = R(e)` with the two
sides computed by different programmes), and random label laws stay below.  (iv) Pair and recursion (`w03`): `F*/t`
nonincreasing, `F*/(1−t)` nondecreasing, slopes of `R̂` in `[−0.94, 0]`, pair identity on 400 accuracies of both signs
(`≤ 9·10⁻⁷`, grid); the level recursion built on `θ_na` never falls below `R^max` (the **lower-barrier property** of DEAD_ENDS D45, item 2:
`min_{k,g}(T_k − R^max)/a = −0.00000` on 59 accuracies and 10 levels, three chains) and is within `0.6 %` of `a` after ten
levels; built on the pair of a wrong game function it **falls below the proved lower bound**: zero residual `−2.3 %` of
`a` (chain `mix`), single dips only `−0.2 %` (triangle), worst binary cut `−4 %` to `−10 %` — the necessary condition of
D45 has power here too.  (v) All 60 optima of the tables of §6.2 re-evaluated with the primal solver (`w12`):
`|r_{μ*}(e) − R^max(e)| ≤ 5·10⁻¹⁴`, and the primal cone formula at `x = e + R^max(e)` returns `R^max(e)` to `3·10⁻¹³`.

---

## 5. W4 — adaptive algorithms without a hint

**Proposition W4.0 (every algorithm, every `n`, at an additive instance) [proved: Theorem 11.27(a), (b) and Theorem
11.22(c) are machine-checked; the product step is the computation of Theorem 11.27(c) with one factor per site
type].**  For all `n`, all compositions, all `γ ∈ ΠL_j`, `t ≥ 0`, `ε > 0`: every randomised algorithm that is
`(ε/2, δ)`-correct on `𝒞` — with or without a hint, adaptive or not — makes at least

    (1 − 2δ) · exp( −tε + n Σ_j λ_j F_j(γ_j, t) )

evaluations in expectation at `ψ_γ`.  Hence, at `γ*`, the exponent of every algorithm is at least `R̂(ε₁)`.
*Proof.*  For `φ ∈ 𝒱_j` the site function `σ_{j,φ} := φ̃ − γ̃_j` is Lipschitz for the slack of `γ_j` and
`E_{π_{γ_j}}e^{−σ_{j,φ}} = 1`.  Draw `φ_i ∼ M_{τ(i)}` independently and put `Φ(x) = Σ_iσ_{τ(i),φ_i}(x_i)`: Lipschitz for the slack
of `ψ_γ`, `E_{μ_γ}e^{−Φ} = 1`, so the generalised dip `ψ_γ − (r − Φ)₊` is in `𝒞` and raises `ln A` by at least `r` (Theorem
11.27(a)).  A fixed `x` lies in the support `{Φ < r}` with probability at most
`e^{tr}Π_iΣ_φM_{τ(i)}(φ)e^{−tσ_φ(x_i)} ≤ e^{tr}Π_jρ_t(M_j)^{n_j}` (Markov), `ρ_t(M_j) = max_aΣ_φM_j(φ)K_t^{γ_j}(a,φ)`.  Theorem
11.22(c) with these alternatives, the best `M_j`, and `r ↓ ε`.  ∎

**Theorem W4 (the adaptive exponent without a hint) [proved by transfer: the proofs of Theorems 11.52, 11.54 and
11.64 (refereed for two states: R7, R9, with the repairs M1, M2), every step re-read in the present setting and the
changed steps written out below; inputs: Proposition W4.0, Theorem W2(c), Theorem W3(d), Theorem 11.66 (machine-
checked).  Not refereed; nothing simulated.]**
Fix `m`, the site types `(𝒮_j, π_j, d_j)`, fractions `λ_j > 0`, `0 < ε₁ < E` and `0 < δ < ½`.  Along every sequence of
chains with `n → ∞` and compositions `n_j/n → λ_j`, the least worst-case number of evaluations of a randomised adaptive
algorithm without a hint that is `(ε₁n/2, δ)`-correct on `𝒞` is

    exp( n·R^max(ε₁) + o(n) ),        R^max(ε₁) = max_{0≤t≤1} [ Σ_j λ_j F*_j(t) − t ε₁ ] ,

**the hinted exponent of the hardest additive instance** `γ*(ε₁)` (Gibbs laws = the Rényi centres of order `t*(ε₁)` of
the windows), while non-adaptive algorithms need `exp(nθ_na(ε₁) + o(n))`, `θ_na(ε₁) = R^max(S^{-1}(ε₁)) > R^max(ε₁)`.  For
`ε₁ > E` a bounded number of evaluations suffices on every instance (Theorem 11.28(d), remark (ii): the sandwich
tensorises site by site).  Consequently the hardest instance with a hint is the hardest additive instance, equally
hard as the flat-histogram instance `H`.

*Proof.*  Lower bound: Proposition W4.0.  Upper bound, in the three steps of Theorem 11.64.

(i) *One more level, relative to the reference `H` of the outer block.*  Split the sites: the outer block takes
`⌊φn_j⌋` sites of **every** type `j`, the inner block the rest; both are chains of the same kind whose compositions tend
to `λ` (this is the only use of the "fixed sequence of site types": any subset of the sites with the right composition
will do).  `X = X_o × X_i`, `π = π_o ⊗ π_i`, `d = d_o + d_i`, `W(a) := E_{π_i}e^{−ψ(a,·)}`, `A = E_{π_o}W`.  The three facts of
Theorem 11.52:
 (F1) every fibre `b ↦ ψ(a,b)` is in `𝒞(X_i)` — additivity of `d` over the sites;
 (F2) `−ln W ∈ 𝒞(X_o)`: `ψ(a,b) − ψ(a′,b) ≤ d_o(a,a′)` for all `b` gives `W(a′) ≤ W(a)e^{d_o(a,a′)}` (term by term; **the
 product structure of `π` is used here and only here** — for a known part with interactions this is the step that fails,
 §11.23);
 (F3) the layer-cake inequalities, which are measure-free.
 *Tail lemma relative to a reference (Lemma 11.62) in the orientation (O):* with `ψ_ref ∈ 𝒞(X_o)`, `μ ∝ π_oe^{−ψ_ref}`,
 `Ŵ = W/w_ref`: `Ŵ(x) ≤ Ŵ(y)e^{s_ref(y,x)}`, `s_ref(y,x) = d_o(y,x) − ψ_ref(y) + ψ_ref(x)`, hence for every level `s` with
 `D = {Ŵ > s} ≠ X_o`: `E_μ(Ŵ − s)₊ ≤ s·Φ_ref(D) ≤ s·Ξ_ref(μ(D))`, `Ξ_ref(q) := max{Φ_ref(D) : μ(D) ≤ q}`.  (One line, as in the
 binary case; checked by brute force with two asymmetric envelopes, 13 328 levels, and violated by the transposed
 slack: `w06` B4.)
 *The algorithm* is that of Theorems 11.52/F7 with: `ψ_ref = ψ_H` of the outer block (weights known, Gibbs law `μ_H`
 sampled by choosing a joint type and then a uniform point of its class; no evaluations); brackets and levels for `Ŵ`;
 one query at a reference point gives `s₀ ≤ min Ŵ` with `max Ŵ ≤ s₀e^{3nD_max}` (the oscillation of a member of `𝒞` is at
 most `nD_max` in either direction); `J = ⌈3nD_max + b + c₁n + 10⌉`, `c₁ := ln(1/π_min) + 1 ≥ −n_o⁻¹ln min μ_H` for large `n`
 (`μ_H(a) ≥ π_o(a)/N_orb`); closure test with an upper bound `Ξ̄ ≥ Ξ_H` that vanishes below `min μ_H` and **never at
 `q = 1`**; everything else unchanged.
 *What changes in the proof* — every place where the cube entered: (1) the number of points `2^{n_o}` becomes
 `1/min μ_H ≤ e^{c₁n_o}`, so the number of potential inner calls is at most `4Ke^{c₁n_o}` and the inner failure probability
 handed down is `δe^{−c₁n}/(2⁶n⁴)` with `K = ⌈24 ln(2⁶n³/δ)⌉` (**this is repair (M2), needed here for every site law**;
 the definition of an exponent function allows failure probabilities `e^{−cd}`); (2) Harper's function `2^{−n_o}E_r(n_o)`
 becomes `Ξ̄(q)`, and "a ball `B(n_o,r)` with `r ≤ n_o − 1`" becomes "`q < 1`"; (3) the constant `2un` becomes `3nD_max`.
 Good event, validity (Markov under `μ_H`; layer cake; tail lemma), width (algebra), termination, the bound
 `M ≤ 8Je²M†` with `M† = 2K/q†`, `q† := sup{q₀ : Ξ̄(q) ≤ qe^{G−b}/4 for all q ≤ q₀}`, the count of points close to a
 level (the two factors `e^b` cancel) and the cost sum are measure-free and hold verbatim.
 *The exponent of `M†`.*  By Theorem W2(c), for `θ` in compact subsets of `(0,∞)`:
 `n_o⁻¹ ln[Ξ_H(e^{−n_oθ})e^{n_oθ}] ≤ θ + R̂^{-1}(θ) + o(1) =: Ŝ(θ) + o(1)`, uniformly over the compositions of the outer
 block (the `ω_n` of Theorem W2(c) does not depend on the composition, and `R̂` is continuous in `λ`: a supremum of
 functions that are linear in `λ`).  `Ŝ` is continuous and nonincreasing (`R̂` has slopes in `[−1,0]`) and
 `sup{θ : Ŝ(θ) ≥ x} = θ_na(x)`.  Hence `q† ≥ exp(−n_o[θ_na((G−b)/n_o) + η])` and `M† ≤ exp(nφθ_na((g−β)/φ) + o(n))`.
 *Conclusion of (i):* if a family of bracket procedures — one for every chain of the given site types, accuracy and
 failure probability — has the nonincreasing exponent function `T` (defined along sequences of compositions tending to
 `λ`), then for all `0 < φ < 1`, `0 < β < g`, `η₀ > 0` there are procedures of accuracy `gn + O(log n)` and cost at most
 `exp(n(τ + 2η₀) + o(n))`, `τ = sup_{γ≥β}[min(γ, φθ_na((g−β)/φ)) + (1−φ)T(γ/(1−φ))]` — the operator `R[T]` of §11.18 with the
 present `θ_na`.

(ii) *The pair.*  `F*` is a game function (Theorem W3(d)), so `(θ_na, R̂)` is a `HintPair` and the exact level recursion
`T_{k+1} = min(T_k, R[T_k])` converges to `R̂` at every `g > 0` (Theorem 11.66 **[V]**; concavity of `F*` is not among its
hypotheses).

(iii) *The levels.*  Base family: complete enumeration, `T₁ ≡ Σ_jλ_j ln q_j`.  The induction of Theorem 11.54 (assembly of
the one-level procedures into a family — exponent function `min(T, R[T])(·⁻) + η₀`, with a left limit; the shift
inequality; induction) uses of (i) only its accuracy, its cost exponent for a finite ladder of rates and the
monotonicity of `θ_na` and `T` (repair (M1)); it applies verbatim with "dimension `d`" read as "chain with composition
tending to `λ`".  For every `k`, `η′ > 0` and `g < ε₁` this gives a family whose exponent at `ε₁` is at most `T_k(g) + kη′`;
let `k → ∞`, `g ↑ ε₁` and use the continuity of `R̂`.  ∎

**Verdict on the two candidate obstacles of the brief.**  *The tail lemma relative to a reference:* no obstacle — it
never used two states or symmetry, only the orientation has to be written down.  *The isoperimetric input:* no
obstacle either, but this is where all the work is: Lemma T′ (site types in the label), the evaluation lemma with
Kantorovich duality and the vertex reduction (Theorem W3(b)), the window step by an optimal coupling, and uniform
continuity of `I − v` near the window (Theorem W2(c)).  Two further points needed care and are not in the binary
proofs: families of procedures must be indexed by compositions (the outer and the inner block have compositions that
are only asymptotically `λ`), and the union bound over inner calls needs the constant `c₁ = ln(1/π_min) + 1`.

*What this does and does not say* — as in §§11.18, 11.20: exponents only; extensive accuracies `0 < ε₁ < E` only (at a
bounded accuracy only the lower bounds `h` and `a` are proved here); worst case over the class; `k → ∞` nested levels;
the `o(n)` is of the typical-subset kind (`η_{M,n}` with `M ≈ n^{1/(2q_max+2)}`: worse than the binary `n^{−1/8}`); the tail
function `Ξ_H` is not explicit (a finite maximum over subsets; the algorithm needs only the upper bound that the
proof of Theorem W2(c) provides) — **nothing here is an algorithm one would run**, and none of it was simulated.
Instance-optimality at non-invariant instances is as open as before.

---

## 6. W5 — a worked example with numbers

### 6.1 The sites and chains (`code/wsites.py`)

| name | alphabet, site law `π` | envelope `d` (rows = first argument) | vertices of `L/ℝ` (normalised `φ(0) = 0`); `*` = distance function |
|---|---|---|---|
| `bin` | 2 states, `(0.7, 0.3)` | `u = 1` | `*(0,−1)`, `*(0,1)` |
| `path` | 3 states on a path `0–1–2`, `(0.5, 0.3, 0.2)` | steps `0.8`, `1.6` (so `d(0,2) = 2.4`) | `*(0,−0.8,−2.4)` dip at 2; `*(0,−0.8,0.8)` dip at 1; `(0,0.8,−0.8)` (lowest at both ends); `*(0,0.8,2.4)` dip at 0 — a rectangle |
| `tri` | 3 states, `(0.2, 0.5, 0.3)` | triangle `d₀₁ = 1`, `d₁₂ = 1.5`, `d₀₂ = 2` (strict) | the three dips `d(·,b)` and the three "anti-dips" `−d(·,b)` — a hexagon |
| `asym` | 3 states, `(0.5, 0.3, 0.2)` | asymmetric: `d = [[0,1,2],[0.5,0,1.5],[1,0.5,0]]` (not "metric + gradient") | 5 vertices, three of them distance functions `d(·,b)` |
| `mix` | half `bin`, half `path` | | |
| `mix2` | `0.4` `bin`, `0.6` `tri` | | |

"Dip at `b`" is the vertex `d(·,b) − d(0,b)`: its generalised dip is a single dip centred at letter `b`; a non-distance
vertex is a union of dips with different depths (for the Hamming envelope: a box).

### 6.2 Single-letter numbers (`w04`; every `R^max` certified by the bracket of Theorem W3(c), gap `≤ 2·10⁻⁹`)

| chain | `E` | `a = θ_na(0⁺)` | `h = R^max(0)` | `h/a` | `t*(0)` | hardest additive instance at `e → 0`: `γ*` (Gibbs law) | labels and weights `M*` at `e → 0` |
|---|---|---|---|---|---|---|---|
| `bin` | `0.103131` | `0.095301` | `0.025034` | `0.263` | `0.490` | `γ* = −0.0908` | the two cones, `(0.501, 0.499)` |
| `path` | `0.400622` | `0.294791` | `0.089589` | `0.304` | `0.460` | `(0, 0.1454, −0.3946)`; law `(0.473, 0.246, 0.281)` | dip at 2: `0.504`, dip at 0: `0.496` |
| `tri` | `0.284907` | `0.247541` | `0.066729` | `0.270` | `0.486` | `(0, 0.1558, −0.0888)`; law `(0.209, 0.448, 0.343)` | dips at 2, 0, 1: `0.458, 0.377, 0.165` |
| `asym` | `0.191059` | `0.166046` | `0.045407` | `0.273` | `0.482` | `(0, 0.0806, −0.6115)` | `d(·,2)`: `0.501`, `d(·,0)`: `0.499` |
| `mix` | `0.251877` | `0.195046` | `0.057275` | `0.294` | `0.467` | `bin`: `−0.0894`; `path`: `(0, 0.1483, −0.3961)` | as for the two types, `(0.502, 0.498)`, `(0.503, 0.497)` |
| `mix2` | `0.212197` | `0.186645` | `0.050050` | `0.268` | `0.487` | `bin`: `−0.0905`; `tri`: `(0, 0.1558, −0.0888)` | as for the two types |

`R^max(e)` (adaptive without a hint = hinted at the hardest additive instance) and `θ_na(e)` (non-adaptive), against
four things one might compute instead: `R_0` (hint at the zero residual), `R^dip` (single dips only, hardest additive
instance), and the binary theory applied to the **worst binary reduction** of every ternary site in two readings —
`R^cut` (coarse-graining `{a} | rest`: a binary site with law `(π(a), 1 − π(a))` and envelope
`(min_b d(a,b), min_b d(b,a))`; the residuals that depend on the coarse letter are a **subclass**, so `R^cut ≤ R^max` is a
theorem: the binary game is the ternary game restricted to coarse vertices) and `R^pair` (deleting a state: the binary
site on `{a,b}` with the renormalised law and envelope `(d(a,b), d(b,a))`; **not** a subclass, no inequality).  In both
readings the maximum over the three reductions is taken.

| chain | `e/E` | **`R^max`** | **`θ_na`** | `R_0` | `R^dip` | `R^cut` | `R^pair` |
|---|---|---|---|---|---|---|---|
| `path` | `0` | **`0.089589`** | **`0.294791`** | `0.080032` | `0.089589` | `0.048586` | `0.115369` |
| | `0.1` | `0.072194` | `0.146318` | `0.063275` | `0.072194` | `0.031465` | `0.098039` |
| | `0.3` | `0.043375` | `0.066899` | `0.036441` | `0.043375` | `0.008558` | `0.068019` |
| | `0.5` | `0.022073` | `0.028920` | `0.017602` | `0.022073` | `0.000070` | `0.043820` |
| | `0.7` | `0.007958` | `0.009223` | `0.005868` | `0.007958` | `0` | `0.025117` |
| | `0.9` | `0.000889` | `0.000931` | `0.000506` | `0.000889` | `0` | `0.011679` |
| `tri` | `0` | **`0.066729`** | **`0.247541`** | `0.065233` | `0.066729` | `0.053168` | `0.094950` |
| | `0.1` | `0.053634` | `0.117164` | `0.052190` | `0.053634` | `0.040446` | `0.082219` |
| | `0.3` | `0.032077` | `0.051124` | `0.030871` | `0.031821` | `0.020377` | `0.059714` |
| | `0.5` | `0.016311` | `0.021673` | `0.015467` | `0.015726` | `0.007211` | `0.040995` |
| | `0.7` | `0.005869` | `0.006846` | `0.005430` | `0.005260` | `0.000750` | `0.025907` |
| | `0.9` | `0.000653` | `0.000685` | `0.000556` | `0.000385` | `0` | `0.014335` |
| `asym` | `0` | **`0.045407`** | **`0.166046`** | `0.033856` | `0.045407` | `0.024685` | `0.058646` |
| | `0.3` | `0.022108` | `0.035544` | `0.012814` | `0.022108` | `0.004666` | `0.034560` |
| | `0.5` | `0.011257` | `0.015108` | `0.004626` | `0.011257` | `0.000090` | `0.022127` |
| | `0.7` | `0.004051` | `0.004750` | `0.000591` | `0.004051` | `0` | `0.012503` |
| | `0.9` | `0.000451` | `0.000473` | `0` | `0.000451` | `0` | `0.005630` |
| `mix` | `0` | **`0.057275`** | **`0.195046`** | `0.052360` | `0.057275` | `0.036803` | `0.070142` |
| | `0.3` | `0.027759` | `0.043288` | `0.024122` | `0.027759` | `0.009634` | `0.040113` |
| | `0.5` | `0.014126` | `0.018622` | `0.011745` | `0.014126` | `0.001326` | `0.024989` |
| | `0.9` | `0.000568` | `0.000595` | `0.000355` | `0.000568` | `0` | `0.005614` |
| `mix2` | `0` | **`0.050050`** | **`0.186645`** | `0.049065` | `0.050050` | `0.041910` | `0.066961` |
| | `0.3` | `0.024122` | `0.038641` | `0.023331` | `0.023974` | `0.017032` | `0.040696` |
| | `0.5` | `0.012268` | `0.016358` | `0.011712` | `0.011919` | `0.006654` | `0.026974` |
| | `0.9` | `0.000491` | `0.000515` | `0.000424` | `0.000325` | `0` | `0.008122` |

(`θ_na` at `e/E = 0` is `a`.)  Thresholds of the variants: `path`: zero residual `0.394664`, dips `0.400622` (= `E`), best cut
`0.208294`, best pair `0.533502`; `tri`: `0.283427`, **dips `0.277528 < E = 0.284907`**, cut `0.226591`, pair `0.423162`;
`asym`: zero residual **`0.155521`** against `E = 0.191059`, cut `0.101690`, pair `0.250182`.

*Reading.*
(1) **The worst binary reduction is not the ternary site, in either reading.**  Coarse-graining two states — the only
reduction that is a theorem — gives `54 %` (`path`, `asym`) to `80 %` (`tri`) of the exponent at vanishing accuracy and
nothing at all beyond its own threshold (`0.52E` for `path`, `0.53E` for `asym`, `0.80E` for `tri`): between `0.21` and `0.40` (`path`) the coarse-grained
binary theory predicts bounded cost where the cost is exponential.  Deleting a state overestimates by `29 %`–`42 %` at
vanishing accuracy and by an unbounded factor near `E` (its threshold is `1.3`–`1.5` times `E`): it is the exponent of
a different class (the middle state of the path is not forbidden, and through it a residual can be lowered more
cheaply).  The ternary structure enters through the *depth profile* of the vertices: the optimal labels of `path` are
the two dips at the **ends** of the path, each with the full three-level profile `(0, 0.8, 2.4)`; no two-state site
has such a label.
(2) **Single dips suffice for `path` and `asym`, not for `tri`.**  For the triangle the optimal labels are the three
dips only below `e_c = 0.1996·E`; above it the anti-dip `2 − d(·,2)` carries `43 %`–`48 %` of the weight (with the dip
at 2 and a small weight on the dip at 0), `R^max/R^dip = 1.04, 1.70, 4.0` at `e/E = 0.5, 0.9, 0.95`, and between the
dip threshold `0.2775` and `E = 0.2849` the dip theory predicts bounded cost.  At `e_c` the label structure switches
discontinuously and `R^max` has a corner (Proposition W3.2).
(3) **The hardest instance is not the zero residual**, as in §11.20 — mildly for the metric sites (`R_0/R^max = 0.89`
for `path`, `0.98` for `tri` at `e = 0`) and strongly for the asymmetric envelope (`0.75` at `e = 0`, `0.15` at `0.7E`,
`0` at `0.9E`), where the zero residual sits near the boundary of the Lipschitz polytope.  The hardest instance moves
the site law towards the Rényi centre of the window: for `path`, `π = (0.5, 0.3, 0.2) → π_{γ*} = (0.473, 0.246, 0.281)`.
(4) **Several site types** (`mix`: half `bin`, half `path`; `mix2`):

| `mix`, `e/E` | `R^max` | `Σ_jλ_jR_j(e)` (average at a common accuracy) | best split `min Σλ_jR_j(e_j)` | split `(e_bin, e_path)`; thresholds `(0.1031, 0.4006)` | common `t*` | `t*_j` at the common accuracy |
|---|---|---|---|---|---|---|
| `0` | `0.057275` | `0.057311` (`+0.06 %`) | `0.057275` | `(+0.0048, −0.0048)` | `0.467` | `(0.490, 0.460)` |
| `0.1` | `0.046179` | `0.046327` (`+0.3 %`) | `0.046179` | `(0.0153, 0.0350)` | `0.415` | `(0.367, 0.428)` |
| `0.3` | `0.027759` | `0.030121` (`+8.5 %`) | `0.027759` | `(0.0356, 0.1155)` | `0.317` | `(0.129, 0.365)` |
| `0.5` | `0.014126` | `0.020800` (`+47 %`) | `0.014126` | `(0.0552, 0.1967)` | `0.225` | `(0, 0.305)` |
| `0.7` | `0.005090` | `0.013844` (`+172 %`) | `0.005090` | `(0.0744, 0.2783)` | `0.134` | `(0, 0.248)` |
| `0.9` | `0.000568` | `0.008322` (`+1365 %`) | `0.000568` | `(0.0935, 0.3599)` | `0.045` | `(0, 0.191)` |

  The average at a common accuracy is an upper bound that becomes useless towards the threshold (the binary type is
  beyond its own threshold `0.103` from `e = 0.41E` on and contributes nothing to the average, while in the chain it
  works at `e_bin < 0.103` and keeps contributing).  The best split of the accuracy is exact here (both `F*_j` are
  concave); for `mix2` it is exact at the tabulated accuracies and off by `8·10⁻⁷` near the label switch.  The binary
  control of the brief (fields `0` and `3`): `R^max(0.3E) = 0.008557`, average `0.009790`, best split `0.008557` at
  `(e₁, e₂) = (0.0360, 0.0074)`.  *The hardest instance and the optimal labels of one site type depend on the other
  types in the chain only through the common slope `t*`.*

### 6.3 Exact finite-`n` sums over joint types (`w05`, `w07`; method in `wfin.py`)

*Hinted / adaptive lower bound.*  For the lattice version of the generalised-dip profile `μ*` (label blocks of sizes
`round(n_jM*_j)`, block types `round(n_{ju}π_φ)`) and an invariant instance `ψ_g` (the hardest additive instance `γ*`, or
`H`), `Φ(y) := min_{x∈C}[d(y,x) − ψ_g(y) + ψ_g(x)]` depends on `y` only through its joint type and its block-wise transport
cost to `C`, so the table `N[P, c] = #{y ∈ T_P : cost = c}` (built exactly by combining the blocks) gives **exactly** the
effect `E(r) = ln E_{μ_g}e^{(r−Φ)₊}` of the generalised dip `(r − Φ)₊` and the density of its support in every joint-type
class.  `r*` := the least `r` with `E(r) > ε = ε₁n + 1`; then **every** `(ε/2, δ)`-correct algorithm makes at least
`(1−2δ)/maxdens` evaluations at the instance (`group_queries_ge`).  `θ_n := −n⁻¹ ln maxdens`:

| chain, accuracy | instance | `n = 60` | `120` | `240` | `480` | `R^max` |
|---|---|---|---|---|---|---|
| `path`, `ε = 1` | `γ*` | `0.099655` | `0.095924` | `0.094458` | `0.092450` | `0.089589` |
| | `H` | `0.084196` | `0.085934` | `0.087871` | `0.088443` | |
| `path`, `ε = 0.3En + 1` | `γ*` | `0.050831` | `0.050265` | `0.048539` | `0.046618` | `0.043375` |
| | `H` | `0.041877` | `0.043514` | `0.044067` | `0.043907` | |
| `asym`, `ε = 1` | `γ*` | `0.051745` | `0.050522` | `0.048884` | `0.047788` | `0.045407` |
| | `H` | `0.039199` | `0.041819` | `0.043041` | `0.044093` | |
| `asym`, `ε = 0.3En + 1` | `γ*` | `0.028123` | `0.026990` | `0.025506` | `0.024929` (`n = 360`) | `0.022108` |
| | `H` | `0.020427` | `0.021110` | `0.021606` | `0.021871` (`n = 360`) | |
| `tri`, `ε = 1` | `γ*` | `0.073943` | `0.072556` | `0.069153` | | `0.066729` |
| | `H` | `0.056357` | `0.060978` | `0.061928` | | |
| `tri`, `ε = 0.3En + 1` | `γ*` | `0.041385` | `0.037870` | `0.035320` | | `0.032077` |
| | `H` | `0.029654` | `0.030208` | `0.030626` | | |
| `mix`, `ε = 1` | `γ*` | `0.065509` | `0.061400` | `0.059680` | `0.059374` | `0.057275` |
| | `H` | `0.047815` | `0.048888` | `0.051516` | `0.054290` | |
| `mix`, `ε = 0.3En + 1` | `γ*` | `0.035796` | `0.031425` | `0.030892` | `0.030094` | `0.027759` |
| | `H` | `0.024449` | `0.023744` | `0.025528` | `0.026692` | |
| `mix2`, `ε = 1` (`n = 50, 100, 200, 400`) | `γ*` | `0.056107` | `0.051196` | `0.052051` | `0.050330` | `0.050050` |
| | `H` | `0.034062` | `0.036410` | `0.042118` | `0.044160` | |
| `mix2`, `ε = 0.3En + 1` (`n = 50, 100, 200, 400`) | `γ*` | `0.028477` | `0.027679` | `0.026435` | `0.025300` | `0.024122` |
| | `H` | `0.015116` | `0.017814` | `0.020008` | `0.021220` | |

So, for example, **at `n = 480` on the chain `mix`, at accuracy `ε = 37.3`, every algorithm — adaptive, with any hint —
needs `(1 − 2δ)·e^{0.0301·480} ≈ (1−2δ)·1.9·10⁶` evaluations at the additive instance `γ*`** (`maxdens = 5.3·10⁻⁷`).  In all
runs `(θ_n − R^max)·n/ln n` lies in `[+0.02, +0.25]` at `γ*` and in `[−0.39, +0.04]` at `H`: the values approach the formula
like `c·ln n/n`, from above at `γ*`, mostly from below at `H` (the set family is the same; the normalisation
`Z_H ≈ poly(n)` of the flat-histogram instance costs a polynomial factor in the effect).  Three-point extrapolations
`a + b ln n/n + c/n` (`w11`) are within `1.2 %`–`6 %` of `R^max` for the profiles with two labels per site type (and for the three-label profiles at
`0.3E`), and `10 %`–`12 %` off for the three-label profiles at `ε = 1` (`tri`, `mix2`), whose smallest block has `10`–`66`
sites and whose series are not monotone — the extrapolations are not a test at that precision; the raw values are.

*Non-adaptive lower bound.*  For the generalised cone with the label blocks of `μ*` the weight is constant on cells, so
the truncation at the orbit-wise `q`-quantiles and `x_n(q) = ln[A(ψ)/A(ψ^{tr,q})]` are exact; `θ_n := −n⁻¹ ln q_min`, `q_min` the
least `q` with `x_n(q) > ε = xn + 1` (then every non-adaptive algorithm needs `(1−2δ)/q_min` evaluations):

| site, accuracy rate `x = e + R(e)` | `n = 30` | `60` | `120` | `240` | 3-point extrapolation | `θ_na(x)` |
|---|---|---|---|---|---|---|
| `path`, `e = 0`: `x = 0.089589` | `0.153143` | `0.131022` | `0.115246` | `0.104936` | `0.089782` | `0.089589` |
| `path`, `e = 0.3E`: `x = 0.163562` | `0.096943` | `0.077217` | `0.063893` | `0.055661` | `0.044289` | `0.043375` |
| `tri`, `e = 0`: `x = 0.066729` | `0.128518` | `0.107129` | `0.091892` | `0.081893` | `0.067133` | `0.066729` |
| `tri`, `e = 0.3E`: `x = 0.117549` | `0.082918` | `0.064092` | `0.051611` | `0.043706` | `0.032472` | `0.032077` |
| `asym`, `e = 0`: `x = 0.045407` | `0.096134` | `0.079848` | `0.067498` | `0.058979` | `0.045772` | `0.045407` |
| `asym`, `e = 0.3E`: `x = 0.079426` | `0.065845` | `0.050483` | `0.039782` | `0.032767` | `0.022423` | `0.022108` |

The excess `(θ_n − θ_na)n/ln n` is `0.39`–`0.67`; the three-point extrapolations agree with `θ_na = R̂∘S^{-1}` to
`0.2 %`–`2.1 %`.  (These rows test the pair identity at finite `n`: `x = e + R(e)` on the left, `R(e)` on the right.)

*The isoperimetric side* (`w10`; Theorem W2(b), (c) on sets that are **not** the optimal ones).  For unions of cells of
a two-block-per-type structure, exits are computed exactly by a multi-source Dijkstra search on the graph of cells,
so `Φ_H⁺(D)`, `μ_H(D)` and `maxdens(D)` are exact.  Six families — neighbourhoods of the optimal and of random centre
classes, unions of two neighbourhoods, half-spaces of the cell lattice, sub-level sets of random admissible functions,
neighbourhoods restricted to one joint type — about 110 sets per run, for `path` (`n = 24, 48, 72`), `tri` (`24, 48`),
`asym` (`48`), `mix` (`24, 36`): the least `ω` with `θ_D ≤ R̂(e_D − ω) + ω` is **at most `0.11·ln n/n`** in the `maxdens` form
(`0.0146, 0.0069, 0.0056` for `path` at `n = 24, 48, 72`) and **at most `0.42·ln n/n`** in the `μ_H` form
(`0.051, 0.031, 0.025`), always largest for neighbourhoods of the optimal classes at accuracies near the threshold; no
counterexample.  At these sizes most sets are in the volume regime (`e_D < 0`), and the test has no power against a
wrong exponent function (the finite-size `ω` is as large as the differences); power comes from the exact sums above:
with `R_0` in place of `R̂` the sets of the `path`/`H` row would need `ω ≈ 0.0065` at every `n` from 60 to 480.

### 6.4 Brute force on full product spaces (`w06`)

*Part A (the tables of `wfin.py`).*  `path`, `n = 8` (`3⁸ = 6561` points); `mix`, `n = 4 + 4` (`1296` points, four label
blocks); `asym`, `n = 7` (`2187` points): the table `N[P,c]` against a direct count (`≤ 2·10⁻¹⁴`); for the instances
`γ*` and `H` and nine values of `r`: `Φ` by `min_{x∈C}` over the full space, the generalised dip is in `𝒞` (all pairs
checked), its effect and the largest orbit density of its support against the table (`≤ 2·10⁻¹⁵`), and the deepest
dip on the same support is at least as effective (`+10⁻³ … +3.6` in `ln A`).  *Part C (truncated cones):* `path` (`n = 8`),
`tri` (`n = 7`), `asym` (`n = 8`): `ln[A/A^{tr,q}]` at seven values of `q` against the table (`≤ 7·10⁻¹⁵`), truncations in
the class.  *Part B (Theorem W1 with two asymmetric envelopes):* §2.

---

## 7. W6 — asymmetric envelopes

**Theorem W6 [proved — every statement of §§2–5 is stated and proved for envelopes that need not be symmetric].**
With the orientation conventions of §1.2:
(a) *the every-`n` statements* (Theorem W1) hold verbatim (`GroupSampling.lean` is stated for asymmetric envelopes); the
quotient envelope is the oriented transport cost `nW(P,P′)`, and the flat-histogram landscape is
`V_n(P) = min_{P′}[J_{P′} + δ(P′,P)]` — admissible for the transposed quotient envelope;
(b) *the single-letter theorem* (Theorem W2) holds with `E d_T(X′, X)`, the exit letter in the first argument;
(c) *the evaluation* (Theorem W3) holds: Kantorovich duality needs only the triangle inequality and a zero diagonal;
the vertex reduction, the Rényi form and the game-function properties never use symmetry — indeed the slack
`d_j(a,b) − γ(a) + γ(b)` of an additive instance is asymmetric even when `d_j` is a metric, so the hinted theory of
workstream A was already a theory of quasi-metrics;
(d) *the shear law and the adaptive exponent* (Theorem W3(d), (e), Theorem W4) hold verbatim.

**Proposition W6.1 (two states: nothing new; three states: a new case) [proved / numerical].**
(a) For a two-state site with `γ(0) − γ(1) ≤ u₁`, `γ(1) − γ(0) ≤ u₂`: `ψ ∈ 𝒞` iff `ψ − κ|x|` is `u`-Lipschitz, with
`u = (u₁+u₂)/2`, `κ = (u₂−u₁)/2`, and `A(ψ) = Z_κⁿ·E_{π_κ}e^{−(ψ−κ|x|)}`: the asymmetric binary site is the symmetric one with the
site law tilted by `κ` — the normal form of §11.11 — and every exponent function coincides (`w08`(ii): `3·10⁻¹⁶` on four
sites, including a one-sided one with `u₂ = 0`).
(b) For three states the antisymmetric part of `d` need not be a gradient (`asym`: it is not), so the envelope is not
"metric + field".  Numbers in §6: `E = 0.191059`, `a = 0.166046`, `h = 0.045407`; the optimal labels are the two distance
functions `d(·,2)`, `d(·,0)`; the zero residual is far from the hardest instance (its threshold `0.1555` is `81 %` of
`E`).  Validation: primal re-evaluation (`2·10⁻¹⁴`), exact sums to `n = 480`, brute force on `3⁷` points, the every-`n`
statements on a chain with two asymmetric envelopes (`w06` A3, B, C), and the isoperimetric families at `n = 48`.

*What one must not do:* symmetrise.  Replacing `d` by `max(d, dᵀ)` enlarges the class, replacing it by `min(d, dᵀ)` (after
closure) shrinks it; and transposing the slack in the tail lemma is wrong (`w06` B4: 2 582 violations).  One-sided
information with `d_j(a,b) = 0` for some `a ≠ b` is allowed everywhere (`L_j` stays compact modulo constants).

---

## 8. W7 (optional) — a known part that is a function of the joint type

`f(x) = nφ(P_x)` with `φ` continuous on `𝒫` (mean-field heteropolymer; one site type: mean-field Potts,
`φ(P) = −(βJ/2)Σ_aP(a)²`); `I = φ − H − min`; `v(P) = min_{P′}[I(P′) + W(P′,P)]`.

**Proposition W7.1 (what of §11.23 transfers) [proved — the proofs of §§2–3 do not use a product measure].**
(a) Theorem 11.76 (a)–(d) = Theorem W1, verbatim (`π` enters only through `π∘σ = π`).
(b) Theorem 11.78 = Theorem W2(a), (b): the exponent of every algorithm at an invariant instance is `R_λ(ε₁)`, the
supremum over labelled profiles.  (Lemma T′ is applied with the product measure `⊗_iP_{τ(i)}`, uniform on the orbit.)
(c) Lemma 11.77(b) ("`v` or `I`"; exits in the contact set): `min{MI(ν) : dist(ν→μ) + v(ν̄) ≤ B} = min{MI(ν) : dist(ν→μ) + I(ν̄) ≤ B}`,
by the optimal-coupling step of Theorem W3(b) — no convexity.  Lemma 11.77(a) (clipping) is binary; for larger
alphabets the inner problem is a transport problem without a closed form (a convex programme when `I` is convex).
(d) Theorem 11.79: truncated shell-cones `ψ = d(·, C_μ)` (the argument of Theorem W3(e) is the argument of 11.79(a));
shell-cones against dips and self-consistent shells (the triangle inequality of the oriented transport cost);
the shear upper bound; and the regularity statement (`R̄_H` is 1-Lipschitz: unions of permuted copies) — all verbatim.
(e) Theorem 11.80 for a **convex** `I`: (a) the collapse `V(μ,B;v) = max_γV(μ,B;λ_γ)`, `λ_γ(P) = −Σ_jλ_jE_{P_j}γ_j − I*(−γ)`
(`v` is convex and admissible, so it is the upper envelope of its affine minorants, whose gradients lie in `−ΠL_j`),
and (c) the game function `F*(t) = max_γ sup_μ φ_{μ,γ}(t)` with its pair — by the proofs of Theorem 11.80.
*Not transferred:* (b) "binary centres suffice" — for a product measure it becomes "at most `q_j` vertex labels"
(Theorem W3(b)); for an interacting convex `I` the number of labels needed is open (**[sketch]**: for fixed `γ`, `τ`
the Lagrangian is linear in the law of the block types, so by a support lemma finitely many labels suffice).
*What fails:* the Rényi form and the every-`n` product bound (they are the product structure), and the nested
algorithm — fibre averages are not admissible for the outer envelope when the conditional law of the inner block
depends on the outer joint type (§11.23; step (F2) of Theorem W4).  The adaptive exponent stays open.

**Proposition W7.2 (a colour-symmetric interaction does not change the value at the symmetric profile) [proved].**
One site type with `q` states, an envelope and a convex rate function `I` that are invariant under a group `G` of
permutations of the letters acting transitively, `min I = I(`uniform`)`.  Let `μ*` be a `G`-invariant optimal labelled
profile of the flat product site (it exists: the set of optimal `M` is convex and `G`-invariant).  Then
`r_{μ*}(e)` for the known part `I` equals `r_{μ*}(e)` for the flat product site; hence `R_H(e) ≥ R_flat(e)`.
*Proof.*  The feasible set `{ν : dist(ν→μ*) + I(ν̄) ≤ e + MI(μ*) + I(μ̄*)}` is convex and `G`-invariant and `MI` is convex and
`G`-invariant, so there is a `G`-invariant minimiser; its type is uniform, where both rate functions vanish.  ∎
(The argument of Theorem 11.80(e) with the colour group in place of the reflection.)  *Numerically* (`w09`): three-state
mean-field Potts, Hamming envelope `u = 1`, `βJ ∈ {0.5, 1, 1.5, 1.9, −2}` (convex regime: `βJ ≤ 2` for every `q`):
`r_{μ*}(e) = 0.03065363` at `e = 0` and `0.01519609` at `e = 0.3E`, equal to the flat product site to `3·10⁻¹⁴` for every
coupling; 40 random or perturbed profiles per coupling stay below (`e = 0`).

**Proposition W7.3 (ferromagnets against product sites; "a field always helps" fails for three states)
[(a) proved; (b) numerical, certified].**
(a) If `φ` is concave (ferromagnetic mean-field interaction of any strength), then
`R_H(e) ≤ sup_p R̂_{product site with law p}(e)`, the supremum over the effective site laws `p₀(P) ∝ e^{−∇φ(P)}`: `I` is the lower
envelope of `KL(·‖p_θ) + c(θ)`, so the feasible set of `r_μ(e)` contains that of the product site with the law `p₀(μ̄)`
(the proof of Proposition 11.81(a) with (c) above in place of Lemma 11.77(b)).
(b) For two states the supremum is at the uniform law (Proposition 11.65(b)).  **For three states it is not, near the
threshold:** Hamming envelope, `u = 1`: `E = 0.119499` for the uniform law, `0.120196` for `π = (0.05, 0.5, 0.45)` (three
evaluations: the dual certificate, the linear programme at `γ*`, a blind search over `γ`), and `F*(t; π) > F*(t; `uniform`)`
for `t ≤ 0.05`; for `h` and for `a` the uniform law is the hardest on a grid of 171 laws (`h = 0.030654`, `a = 0.123284`),
and pointwise at `t ∈ {0.1, 0.3, 0.5, 0.7, 0.9}` on 57 of them; for `u = 2` the uniform law is the hardest in all three
(`E = 0.474266`).  The two-state cube with `u = 1` has
`E = ln cosh ½ = 0.120115`: a rare third state makes the class slightly *harder* near the threshold than either the
two-state or the flat three-state site.  So Proposition 11.81(a)/(b) ("never harder than the uniform cube") does not
extend to three states as it stands; with (a) and Proposition W7.2 one gets `R_H(0⁺) = h_flat` for a colour-symmetric
ferromagnet with convex `I` only **given** that the uniform law maximises `h` (numerical).

*Not done for W7:* a non-convex rate function (the first-order transition of the Potts model: by the reasoning of
§11.23 the extremal labels should be shells in barrier joint types) — no number; two order parameters — only what
(a)–(d) say.

---

## 9. Statement of §11.20 / §11.23 → what it uses → carries over / changes / fails

| statement | what it uses | here |
|---|---|---|
| 11.59(a) every-`n` bound `(1−2δ)e^{−tε+nF(γ,t)}` | Theorem 11.27(c): product of site games | **carries over**, one factor per site type (Prop. W4.0) |
| 11.59(a) hinted cost `e^{nR_γ+o(n)}` at an additive instance | Theorem A of workstream A (identical sites) | **carries over** to several site types (Thm W2(b) + W3(b)); was a sketch |
| 11.59(b) closed (cosh) form of `F(γ,t)` | 2×2 game | **changes**: no closed form for `F(γ,t)`, but `F*_j(t) = (1−t)C_t` (Thm W3(c)), a convex programme; for two states the same numbers (`10⁻¹⁵`) |
| 11.59(c) max–min forms | minimax in the centre law | **carry over** with labels = vertices (Thm W3(b), (e)) |
| 11.59(d) `R^max > R_0` unless `p = ½` | derivative of the closed form | **changes**: `R^max ≥ R_0` always; equality iff `π_j` is the Rényi centre of its window for the relevant `t` (not re-proved as a strict statement; strict in every example) |
| Lemma 11.60 (shift identity) | `π_s` product | **carries over**: `𝒟(ν) = MI(ν) + I(ν̄) + Eφ_U(X′) + E ln Z_{φ_U}` (one line); used only through Thm W3(e) |
| 11.61(a) quantiles are Lipschitz | coupling of adjacent type classes | **changes** (simpler): invariance alone (`lowDens_shift`), no coupling (Thm W1(a)) |
| 11.61(b) one extremal function, both sides | permutation symmetry | **carries over** with `N_orb` (Thm W1(a)) |
| 11.61(c) truncated cones | log-concavity of hypergeometric shells | **changes**: the binary argument is replaced by that of 11.79(a) (densest class above the quantile); generalised cones with vertex labels |
| 11.61(d) upper bound | 11.63; `nv` = inf-convolution | **carries over** in the orientation (O) |
| 11.61 product samplers are worse | constant centres | **not examined** |
| Lemma 11.62 tail lemma relative to a reference | nothing about `π` or two states | **carries over verbatim**, slack `s(y→x)` |
| 11.63 Lemma T | i.i.d. product measure | **changes**: Lemma T′ (site type in the label; any alphabets) |
| 11.63 Lemma SL | Sion; Donsker–Varadhan; endpoints of a segment; thinning | **changes**: Kantorovich duality, vertices of `L_j` (Lemma 3(c) of workstream A), separation over site types, optimal coupling for the window step (Thm W3(b)) |
| 11.63 Steps 1–6 | counting; Hoeffding; `KL − v = O(dist²)` | **carry over**; uniform continuity instead of the quadratic bound (Thm W2(c)) |
| 11.64 lower bound | 11.59(a) | **carries over** |
| 11.64 (i) one more level relative to `H` | product `π`; fibres; (M2) | **carries over**; (M2) needed for every site law; families indexed by compositions (Thm W4) |
| 11.64 (ii) the pair | game function | **carries over**: `F*` is a game function, **not necessarily concave** (Thm W3(d), Prop. W3.2) |
| 11.64 (iii) levels | abstract | **carries over** |
| 11.65(a) not instance-optimal in the worst case | closed form | **carries over** as `R^max ≥ R_0`, numerically strict |
| 11.65(b) a field always helps | ODE for the 2×2 game | **fails for three states near the threshold** (Prop. W7.3(b)); holds numerically for `h` and `a` (Hamming, `u = 1, 2`) |
| 11.65(c) stratified bracket | symmetry | **carries over** with `N_orb` (Thm W1(d)) |
| §11.20 remark (3): `μ_H` is the NML mixture | product family | **carries over**: `μ_H ∝ max_γπ_γ^⊗`, `Z_H ≤ N_orb`; `μ_H(D) ≥ π_γ^⊗(D)/N_orb` |
| §11.20 remark (4) / F12 | — | **confirmed** (i)–(iii); new: the Rényi form, non-concavity |
| 11.76 and the remark after it | invariance | **carries over** (Thm W1) |
| 11.77(a) clipping | binary | **fails** (a transport problem) |
| 11.77(b) `v` or `I` | thinning | **carries over** by an optimal coupling |
| 11.78 | types; Lemma T inside a type class | **carries over** (Thm W2); three steps change (§3.3) |
| 11.79 shell-cones, shear bound, regularity | triangle inequality; permuted copies | **carry over** (Prop. W7.1(d)) |
| 11.80(a), (c) convex `I` | Sion; game function | **carry over**; (b) binary centres → at most `q_j` vertex labels for product measures, open with interactions |
| 11.81 ferromagnets | 11.65(b) | (a) **changes** (`≤ sup_p`, not `≤` uniform); (b), (c) not examined |
| 11.82, 11.83 two phases | — | **not examined** for larger alphabets |

---

## 10. Negative results, refuted guesses, and errors of my own that the tests caught

1. **"The exponents of the site types add"** — false (DEAD_ENDS D31 again), now quantified: the average at a common
   accuracy overestimates by `+8.5 %`, `+47 %`, `+172 %`, `+1365 %` at `e/E = 0.3, 0.5, 0.7, 0.9` (`mix`).  What adds: the game
   functions at a common slope; the thresholds; the non-adaptive exponents at vanishing accuracy.
2. **"After the best split of the accuracy they add"** — true when the `F*_j` are concave, **false in general**: `mix2`
   near the label switch (by `8·10⁻⁷`; Proposition W3.2).  I had written "`R^max = R^split`" into my notes before the
   second-difference test of `w03` reported a positive second derivative of `F*_tri`.
3. **"`F*` is concave / `R^max` is smooth"** — false for three states (label switch of the triangle site, a corner of
   `R^max` at `0.1996·E`); true in all 100 binary cases computed, unproved.
4. **"Single dips (distance functions) are the labels" / "binary centres suffice"** — the labels are vertices of the
   Lipschitz polytope; for `path` and `asym` they happen to be distance functions at all accuracies, for `tri` only
   below the switch; beyond it the dip theory underestimates by up to a factor `4` at `0.95E` and has the wrong
   threshold (`0.2775` against `0.2849`).  This is DEAD_ENDS D38 for the worst-case (hint-free) exponents.
5. **"The worst binary reduction captures a ternary site"** — false in both readings (§6.2): `0.54`–`0.80` of the
   exponent by coarse-graining, `1.29`–`1.42` by deleting a state, and wrong thresholds by factors `0.5`–`0.8` and
   `1.3`–`1.5`.
6. **"A field always helps: the uniform site law is the hardest"** (Proposition 11.65(b)) — false for three states near
   the threshold (Proposition W7.3(b)).  Found by a grid scan that I expected to confirm the binary statement.
7. **"The zero residual is nearly the hardest instance"** — false already with a field (D47); for an asymmetric
   envelope it is badly false (`R_0/R^max = 0.75 → 0`), because `γ = 0` is not a distinguished point of an asymmetric
   Lipschitz polytope.
8. **The upper bound has a worse error term than in the binary case:** `η_{M,n}` needs `(M+1)^{q_max} ln n/n → 0`, so
   `ω_n` is of order `n^{−1/(2q_max+2)}` in the proof (`n^{−1/8}` for two states); the exact sums suggest `c·ln n/n` as before.
9. **At `H` the finite-`n` bounds from sets around one labelled class approach the formula from below**, at `γ*` from
   above (§6.3): a polynomial factor (`Z_H`), not a discrepancy — but a table at `H` alone would have looked like a
   formula that is too large by `5`–`12 %` at `n = 400`–`480`.
10. **A value of the brief quoted at a finite difference** (item (i) of the checks in §4): `0.008559`/`0.009791` belong to
    `E = 0.072271 = F*(t)/t` at `t = 1/4000` (reproduced exactly); with the threshold `0.072290` they are `0.008557`/`0.009790`.
11. **Errors of mine caught by tests, not by reading.**
    (i) *The maximum over `γ` is a kink.*  My first maximiser of `F_j(γ,t)` over `L_j` (grid and zoom) returned values that
    were too small by `10⁻⁶`–`10⁻⁵` and depended on the zoom parameters; `F` decreases linearly, not quadratically, away
    from `γ*`, and the table of `F*` was noisy at `10⁻⁵`.  Found by the rule of the brief: the primal re-evaluation at the
    reported optimum came out *larger* than the "optimum" by `7·10⁻⁸` (`path`) and `9·10⁻⁸` (`mix`) — small, but above the
    solver tolerance.  The repair was the closed form of Theorem W3(c), which the bug led to: at the optimum all
    letters are active, which is the equalisation behind the Rényi centre.
    (ii) *A blind outer search in a max–min* (the collapse test, `w02` T3): Nelder–Mead over `γ` returned `0` where the
    value is `3.5·10⁻⁴` (the positive region in `γ` is small); it looked like a violation of Sion's theorem in the
    harmless direction.  Replaced by the certificate "`V(v) ≥ V(γ)` trivially, and equality at the `γ` read off the exit
    type"; the blind search is still run and printed for chains with one site type (for two site types it is optional —
    third argument `blind` — and the stored outputs print `nan` in its place).
    (iii) *Zoom parameter:* the first zoom shrank to `1.25` grid spacings (a factor-two slip; caught on reading, before
    any run).  (iv) *A coverage check that was too strict* rejected complete cost tables (`w06` A2 failed with an
    assertion; the tables were right).  (v) *Memory:* the first version of the tables kept four copies and failed at
    `n = 480`; one run (`asym`, `0.3E`, `H`, `n = 480`) still does and is reported at `n = 360`.  (vi) The first
    label-switch detector in `w04` reports the same `t*` on both sides of the switch for `mix2` (a bisection on the
    wrong side); the numbers of Proposition W3.2 are from `w08`(iv), which brackets the two branches separately.
12. **A test without power, recorded as such:** the isoperimetric families of `w10` at `n ≤ 72` cannot distinguish `R̂`
    from the wrong exponent functions (zero residual, dips only); see the end of §6.3.

*Looked for and not found — places where the sketch F12 could have failed:* the window step for alphabets with more
than two letters (works by an optimal coupling); the unimodality argument for truncated cones (not needed); Lemma T
for a non-i.i.d. product measure (the site type goes into the label); the vertex reduction for asymmetric envelopes
(unchanged); the union bound of the nested algorithm (needs (M2) always); block compositions that are only
asymptotically `λ` (families indexed by compositions).  None is an obstruction.

---

## 11. What I did not check

1. **Nothing here is refereed.**  The proofs of Theorems W1–W4 and W6 are mine; Theorem W4 is a proof by transfer —
   I re-read every step of the proofs of Theorems 11.52, 11.54, 11.64 (theory report) in the new setting and wrote out
   what changes, but I did not rewrite the algorithm, and **nothing of the nested algorithm was simulated**, with or
   without real inner brackets.  The uniformity of the `o(n)` terms through the levels is on paper only.
2. Theorems 11.22, 11.27(a), (b), 11.66 and `GroupSampling.lean` were used as stated (read, not re-derived; no Lean was
   run).  Lemma 3(c) of workstream A (vertex reduction) was re-derived; Theorem A of workstream A is not used.
3. Alphabets with more than three letters: only the flat four-state control; the finite-`n` code and `v_types` are for
   `q ≤ 3`.  More than two site types: no number.  Site types with very different sizes of `n_j`: only on paper
   (uniformity in the composition).
4. Bounded accuracies (`ε = O(1)`): only the lower bounds (`h` for all algorithms, `a` for non-adaptive ones) — the
   exact sums at `ε = 1` are lower bounds; no upper bound at bounded accuracy is claimed (as in §11.20).
5. Product samplers / plain Monte Carlo from `π` for larger alphabets: not examined.
6. Concavity of `F*` for two states: numerical (100 sites).  Where exactly label switches occur for three states, and
   whether there can be several: one example.
7. The finite-`n` sums use one centre class per `n` (the rounded single-letter optimum), not an optimisation over
   classes; the isoperimetric families are unions of cells of one block structure at `n ≤ 72`.
8. W7: no non-convex rate function; no number for a mean-field heteropolymer with two site types; the number of labels
   needed with interactions.  Whether the uniform site law maximises `h` and `a` for the Hamming envelope: grid scans at
   `u = 1, 2` only.
9. Prior art: two generic searches (§13); the identification of `F*` with a Rényi capacity is elementary once seen and
   may well be known in another language — "not found in the theory report", not "new".

---

## 12. Scripts: commands, sizes, run times

All in `code/`, run from that directory as `ulimit -v 4000000; timeout 590 python3 <script> <args>`, one at a time;
outputs in `out/` under the names given.  Libraries: `wlib.py` (sites, vertices of the Lipschitz polytope, matrix games
by enumeration and by linear programming, `Site.renyi` = Theorem W3(c) with its dual certificate, `Estar`, `capacity`,
chains, `R`, `θ_na`), `wprimal.py` (primal solver: SLSQP on couplings with analytic gradients; cone formula),
`wsites.py` (the example sites), `wfin.py` (exact tables over joint types, `DipTable`, `v` on all types).

| script → output | what | sizes | run time |
|---|---|---|---|
| `w01_controls.py` → `w01_controls.txt` | controls of the brief; closed binary form; larger-alphabet controls; Theorem W3(c) against zoom and LP | 2000 random games; 575 + 42 points | 7 s |
| `w02_single_letter.py <chain> 30` → `w02_<chain>.txt` | primal re-evaluation; random and perturbed profiles; collapse; cone formula and pair identity | 6 chains × 3 accuracies × 60 profiles; 36 collapse profiles | 3–222 s |
| `w03_recursion.py <chain> 10` → `w03_<chain>.txt` | game-function and pair properties; level recursion; three mutations | 801 values of `t`; 59 accuracies × 49 × 15 × 41, 10 levels | 12–15 s |
| `w04_example.py` → `w04_example.txt` | tables of §6.2 | 6 chains, 10 accuracies, variants on 401 values of `t` | 122 s |
| `w05_finite.py <chain> <e/E> <n,…> 1` → `w05_<chain>_e<…>.txt` | exact hinted lower bounds at `γ*` and `H` | `n ≤ 480` (`path`, `asym`, `mix`), `≤ 400` (`mix2`), `≤ 240` (`tri`); tables up to `231 361 × 242` | 11–42 s |
| `w06_bruteforce.py` → `w06_bruteforce.txt` | brute force, Parts A, B, C | `6561`, `1296`, `2187`, `216` points | 33 s |
| `w07_nonadaptive_finite.py <chain> <e/E> 30,60,120,240 1` → `w07_<chain>_e<…>.txt` | exact truncated generalised cones | `n ≤ 240`, tables up to `58 081 × 961` | 8–69 s |
| `w08_misc.py all` → `w08_misc.txt` | Lemma T′; asymmetric binary; concavity; label switch; hardest site law; coding dictionary | 480 + 76 + 100 + … cases | 226 s |
| `w09_potts.py` → `w09_potts.txt` | mean-field Potts, convex regime | 6 couplings × 2 accuracies | 4 s |
| `w10_isoperimetry.py <chain> <n>` → `w10_<chain>_n<n>.txt` | isoperimetric statement on six families of cell sets (Dijkstra) | up to `494 209` cells, `5.6·10⁶` moves | 10–60 s |
| `w11_extrapolate.py` → `w11_extrapolate.txt` | three-point extrapolations of the series of `w05`, `w07` | — | < 1 s |
| `w12_reeval.py` → `w12_reeval.txt` | every optimum of §6.2 re-evaluated by the primal solver; primal cone formula at `e + R` | 6 chains × 10 accuracies | 41 s |

Accuracy of the single-letter numbers: `F*_j(t)` is bracketed by `[G_t(M), (1−t)max_φD_t(π_φ‖Q_M)]` with gap `≤ 2·10⁻⁹`;
`R^max(e)` is a maximum over `t` (grid of 201, then bounded Brent, `10⁻¹⁰` in `t`); the primal solver reproduces it to
`5·10⁻¹⁴`; the variant columns of §6.2 (`R_0`, `R^dip`, `R^cut`, `R^pair`) are maxima over a grid of 401 values of `t`
(accurate to about `10⁻⁶`).  The finite-`n` sums are exact up to floating-point rounding of sums of positive terms.

---

## 13. Prior art and search log

Two generic searches (25 Nov 2026; no project names, paths or personal data), read as search summaries only:
(1) "Sibson alpha mutual information Gallager E_0(rho) = rho I_{1/(1+rho)} Rényi capacity equals Rényi radius Csiszár
generalized cutoff rates" — summaries of B. Nakiboğlu, *The Rényi capacity and center* (arXiv:1608.02424: `E_0(ρ,W) =
ρC_{1/(1+ρ),W}`; Csiszár: the three definitions of the order-`α` Rényi capacity coincide with the Rényi radius; a unique
Rényi centre exists) and of surveys of `α`-mutual information; (2) "sphere packing exponent E_sp(R) = sup_rho [E_0(rho) −
rho R] Haroutunian form min D(V||W|P) subject to I(P,V) <= R" — summary of *The sphere packing bound via Augustin's method*
(arXiv:1611.06924); it warns that "Haroutunian's exponent" is the name of a *different* (feedback) exponent, so the
constant-composition form `max_M min{D(V‖W|M) : I(M,V) ≤ θ}` is called the Csiszár–Körner form here (from memory).
Nothing in the proofs of this report depends on these sources: Theorem W3(c), (e) prove what is used.  From memory,
not read: Kantorovich duality for quasi-metric costs; integrality of transportation polytopes; Sion's minimax theorem;
Hoeffding's inequality; monotonicity of Rényi divergence in the order; the support size of optimal strategies of
matrix games.  The typical-subset method (Ahlswede–Yang–Zhang; Ahlswede–Zhang; Yu) was taken through
`A_REPORT.md`, `F_REPORT.md` and `R9_referee_report.md`, not from the sources.
*Not found in the theory report or in the workstream reports I read:* the identification of `F*` with a Rényi capacity
and of `θ_na` with the inverse sphere-packing exponent; the non-concavity of `F*`.  "Not found there", not "new".

---

## 14. Summary (at most 40 lines)

1. **W1 [proved, every `n`]**: symmetry group `Π_jS_{n_j}`, orbits = joint types (`N_orb = Π_jC(n_j+q_j−1, q_j−1)`); quotient
   envelope = oriented transport cost `nΣ_jλ_jW_{d_j}`; the joint-type-stratified sample is optimal among fixed samples up to
   `8N_orb ln(2N_orb/δ)/(1−2δ)`; every algorithm needs `(1−2δ)/maxdens(D)` at an invariant instance; the flat-histogram
   instance is the hardest invariant one up to `N_orb + 1`.  Lower halves machine-checked (`GroupSampling.lean`).
2. **W2 [proved]**: single-letter theorem `R_λ(e) = sup_{P_TUX} min{I(X′;U|T) : E d_T(X′,X) + λ(P_{X′|T}) ≤ e + I(X;U|T) + I(P_{X|T})}`
   for every invariant instance of every known part that is a function of the joint type; lower bound every `n`, upper
   bound by types with Lemma T′ (site type in the label); three steps of Theorem 11.78 change.
3. **W3 [proved]**: (a) `H` = hardest additive instance (Sion); (b) vertex labels suffice (`≤ q_j` per type);
   (c) `F*` is a game function, `E = Σλ_jE_j`, `L = a = Σλ_ja_j`; (d) `F*(t) = Σ_jλ_jF*_j(t)`, one common `t`.  **New closed form:**
   `F*_j(t) = (1−t)·C_t` (Rényi capacity of the vertex channel), hardest instance = Rényi centre; `θ_na = E_sp^{-1}`,
   `a` = Shannon capacity, `E = E_sp(0)`.  Exponents do not add: average at a common accuracy `+8.5 % … +1365 %`;
   best split exact iff `F*_j` concave.  **Negative:** `F*_j` not concave for a three-state site (label switch, corner of
   `R^max` at `0.1996E`); concave in 100 binary cases (numerical).
4. **W4 [proved by transfer of the refereed binary proofs; not refereed, not simulated]**: adaptive exponent without a
   hint `= R^max(ε₁) = max_t[Σλ_jF*_j(t) − tε₁]`; non-adaptive `θ_na = R^max∘S^{-1}` (lower bound every `n`).  Tail lemma and
   isoperimetric input are no obstacles; (M2) is needed for every site law; families indexed by compositions.
5. **W5**: `path` (steps 0.8, 1.6; `π = (.5,.3,.2)`): `E = 0.400622`, `a = 0.294791`, `h = 0.089589`, `R^max(0.3E) = 0.043375`,
   `θ_na(0.3E) = 0.066899`, `γ* = (0, 0.145, −0.395)`, labels = dips at the two ends; worst binary cut `0.0486` (54 %),
   pair `0.1154` (129 %).  `tri` (sides 1, 1.5, 2): `0.284907`, `0.247541`, `0.066729`; dips-only threshold `0.2775`.  `asym`:
   `0.191059`, `0.166046`, `0.045407` (`R_0 = 0.0339`).  `mix` (half binary): `0.251877`, `0.195046`, `0.057275`,
   `R^max(0.3E) = 0.027759` against the average `0.030121`.  Exact sums: `n = 480`, `path`: `0.09245` (`γ*`), `0.08844` (`H`)
   against `0.08959`; non-adaptive `n = 240`: `0.1049`, extrapolated `0.08978` against `0.08959`.  Brute force (`3⁸`, `2⁴3⁴`, `3⁷`
   points): `10⁻¹⁴`.  Controls of the brief reproduced (two-type control: `0.008557`/`0.009790` at the true threshold).
6. **W6 [proved]**: everything survives with the orientation `s(y→x)`; binary asymmetric = symmetric + field; ternary
   asymmetric is new and validated like the rest.
7. **W7**: W1, W2, "`v` or `I`", shell-cones, regularity transfer **[proved]**; convex `I`: collapse and game function;
   Potts at the symmetric profile = flat product site (**[proved]**, `10⁻¹⁴`); **"a field always helps" fails for three
   states near the threshold** (`0.119499 < 0.120196`); nested algorithm does not transfer; non-convex `I` not examined.
8. **Conjectural / numerical:** concavity of `F*` for two states; the uniform law maximises `h`, `a` for the Hamming
   envelope; `ω_n = O(ln n/n)`.  **Not checked:** a referee; the nested algorithm end to end; `q ≥ 4` and `m ≥ 3`
   numerically; bounded accuracies (upper bounds); product samplers; prior art beyond two searches.
