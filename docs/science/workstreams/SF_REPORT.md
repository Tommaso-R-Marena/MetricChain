# SF — Workstream F (science division, second wave): a free, exact one-body marginal oracle on the biased cube

*Question (brief `F_brief.md`; SCI-REQ-0001 Q2; open problem A2): does a free, exact oracle for the one-body
marginals of the Gibbs measure lower the worst-case query-complexity exponents of certifying `ln Z` over the
Lipschitz class on the `p`-biased cube?  Everything of mine is in `experiments/science/ws_F/` (scripts, outputs `out/`,
running log `NOTES.md` with clock readings).  Nothing was changed outside that directory and this file; no
state-changing git command; no `lake build`.  Theory commits referred to: `5ed4072` (our branch point; §11.20), `89ac710`
(§11.26, read in `thy_ro`), and — read after my own results were logged, see §8 — `dcdfea6` (§11.29, Proposition 11.109).*

Labels: **[V]** machine-checked (by the theory division; Lean declaration named), **[P]** paper proof given here (with
what was checked numerically), **[K]** known and cited (reading level stated), **[N]** numerical only, **[C]** conjecture,
**[H]** heuristic.  "Black box" = a refereed paper proof of the theory division that I use and did not re-derive.

---

## 1. Verdicts

**The conjecture of the brief is true as a statement and false as an explanation.**  (i) *True:* for every `p ∈ (0,1)`
and `u > 0` a free exact one-body marginal oracle changes **neither** class exponent — adaptive (`R^max`, Theorem A,
Corollary A) nor non-adaptive (`θ_na`, Theorem B, Corollary B) — and the lower bounds hold **for every `n`**, with the
oracle costing at most a factor `C·n(n+1)` (adaptive) resp. `n` in the count and `O(1)` in the accuracy (non-adaptive);
for the adaptive bound this includes every fixed accuracy `ε > 0`.  (ii) *False:* the proposed reason — "the hardest
instance is self-consistent" by Augustin's fixed point — fails twice.  The excess mass of a sensitive dip is carried
by the **cone law** `π_φ` (the output law `MW` of the vertex channel), not by the tilted type `V_φ ∝ π_φ^t Q*^{1−t}`, which
is the type of the dip's *rim*; and `M*W ≠ Q*` whenever `p ≠ ½` (gap `0.006 … 0.21` in the 28 cases computed), so the
hardest *additive* instance is **not** self-consistent, and with the oracle its own instance-wise exponent drops
(Proposition C).  (iii) *The actual mechanism is compensation:* the class is a convex cone in the weights and contains
the tilted product measures, whose densities sweep the whole window of possible one-body marginals; adding
`b·(`an extreme additive instance`)` to **both** members of an indistinguishable pair moves their common one-body
marginal anywhere between that of the pair and the end of the window without changing the set on which they
differ — one exact linear equation, `b = A_w(c_Δ − c_w)/(p₂ − c_Δ)` (Lemma 3).  With the oracle the hardest instance is a
**two-component mixture**, not an additive instance.  (iv) *Instance-wise the oracle does help* (the coordinator's
second question): at the zero residual with a field the exponent with the oracle is strictly below `R_0`, and I
bracket it, `V(e) ≤ R_0^{orc}(e) ≤ U(e) < R_0(e)`, by explicit matched alternatives from below and by a new **tilt
inequality** plus the theory division's hinted theorem from above (e.g. `p = 0.1, u = 2, e = 0.2E_0`: `0.0154 ≤ · ≤ 0.0163`
against `0.0268`); in a window of accuracies the cost falls from exponential to sub-exponential (threshold ratio down
to `0.37`).  **"Restricted to the centre type forced by the matching equation" is a valid lower bound but not the
value**: dips around shells do much better (`0.0154` against `0` in the example).  (v) `k = 2`: exact two-body matching
is impossible with one centre type and any mixture of additive instances (the excess is *below* the parabola
`c₂ = c₁²`), and possible with two centre types `≳ √n` apart — an explicit two-component base again, verified exactly
at `n = 13` with `AGL(1,13)` (all 13 + 78 marginals equal to `10⁻¹⁴`).  (vi) *Tolerance:* with **all** marginals of every
order known to absolute precision `τ` the adaptive lower bound loses a factor polynomial in `1/τ` and logarithmic
in `n`, so the exponent is unchanged for every `τ ≥ e^{−o(n)}` (Theorem τ).  Against the theory division's §11.29
(commit `dcdfea6`, read afterwards): (a)–(d) agree; their
conjecture (f) is **proved** here by a different instance; their conjecture (e) is right in direction, their value
`ρ_e(p)` is (numerically, to six digits) my tilt **upper** bound, and the profiles that attain it do not have excess
mass of type `p` (§8).

*Status of each claim.*  **[P]** (complete proofs here; finite ingredients checked exhaustively, for Theorem A also in
exact rational arithmetic): Lemmas 0–3, Theorem A, Theorem B (on top of the machine-checked truncation lemma),
Proposition C(a), Proposition D(a), Proposition E(i)–(iii), Theorem τ.  **[P given a refereed paper proof of the theory
division that I did not re-derive]**: the upper bounds in Corollaries A(c) and B (Theorems 11.64, 11.61), the exponent
in Corollary B (Theorem 11.61(c)), Proposition C(b) (the hinted theorem at shifted fields).  **[P sketch + finite-`n`
certificates]**: `V` as a lower bound at the zero residual (Proposition D(b)); Proposition E(iv).  **[N]**: every
table, the strictness `U < R_0`, the failure of `M*W = Q*`.  **[C]**: Conjecture Z, exact `k`-body marginals for `k ≥ 3`.
Nothing is machine-checked by me.

---

## 2. Statements and proofs

### 2.0 Setting and notation

`X = {0,1}ⁿ`, `π = Bernoulli(p)^{⊗n}`, `q = 1 − p`; `L_u = {ψ : |ψ(x) − ψ(y)| ≤ u·d_H(x,y)}`; `A(ψ) = E_π e^{−ψ}`; target `ln A`;
`μ_ψ ∝ πe^{−ψ}`.  In the weights `w = e^{−ψ}` the class is the cone `𝒲_u = {w > 0 : e^{−u}w(x) ≤ w(x⁽ⁱ⁾) ≤ e^{u}w(x) for all x, i}`,
closed under sums, positive multiples, pointwise max and min.  `A(w) = Σ_x π(x)w(x)`.  For a finite non-negative
measure `ν` on `X` its **density** is `dens(ν) = Σ_x ν(x)|x| / (n·ν(X))`; `dens(w) := dens(πw)`.

*Additive instances.*  `ψ_γ = γ|x|`, `|γ| ≤ u`; site law `π_γ`, `p_γ := π_γ(1) = pe^{−γ}/(q + pe^{−γ})`; normalised weight
`w̃_γ := e^{−γ|x|}/(q + pe^{−γ})ⁿ`, so that `πw̃_γ = π_γ^{⊗n}` (mass 1, density `p_γ`).  **Window:** `p₋ := p_u < p₊ := p_{−u}`,
`ω := p₊ − p₋`.
*Cones.*  `π_0 := Bern(p₋)`, `π_1 := Bern(p₊)` (the two letters of the *vertex channel* `W` of theory report Theorem 11.99);
for `s ∈ X`: `π_s := ⊗_i π_{s_i}`, normalised cone weight `c̃_s := e^{−u·d(·,s)}/Z_s`, `πc̃_s = π_s`.  For `|s| = k = mn` the density of
`π_s` is `c₀(m) := (1−m)p₋ + m·p₊`, the output law `(MW)(1)` of the vertex channel at the input law `M = (1−m, m)`.
`T_k = {s : |s| = k}`; `σ` the cyclic shift of the coordinates.
*Single-letter quantities* (theory report §11.20, my implementation `sl.py`): game function
`F(γ,t) = −ln min_m ρ_t(m;γ)`, `ρ_t(m;γ) := max_{a∈{0,1}} [(1−m)(π_0(a)/π_γ(a))^t + m(π_1(a)/π_γ(a))^t]`; `F*(t) = max_γ F(γ,t)`;
`R_γ(e) = max_{0≤t≤1}[F(γ,t) − te]`, `R^max = max_γ R_γ`, `E`, `θ_na`, `a` as there; saddle `(t*, M*, Q*, γ*)` with `π_{γ*} = Q*`
the Rényi centre.  Constant-composition exponent of dips of centre type `m` at the base `γ`:
`Rcc(γ,m;e) := min{I(M,V) : D(V‖W|M) − D(V‖π_γ|M) ≤ e}` (`max_m Rcc = R_γ`; checked, §3.1).

*The oracle model.*  An **oracle algorithm** is a family of randomised query algorithms indexed by `o ∈ [0,1]ⁿ`; run on
`ψ` it uses the member with index `o(ψ) := (μ_ψ(x_i = 1))_{i≤n}`.  (This is the repair found by workstream L1 for the
theory division's `QueryAlgorithm`.)  It is *non-adaptive* if, for each `o`, the random set of evaluated points does
not depend on the values of `ψ`.  `(ε/2, δ)`-correct on `L_u`: for every `ψ ∈ L_u` the output is within `ε/2` of `ln A(ψ)`
with probability `≥ 1 − δ`.  Cost = number of evaluations.

### 2.1 Four lemmas

**Lemma 0 (window) [P; = theory Proposition 11.109(a) at `dcdfea6`, derived independently].**  For every `ψ ∈ L_u` and
every site, `μ_ψ(x_i = 1) ∈ [p₋, p₊]`; the densities of the additive instances fill `[p₋, p₊]`.  If all `n` marginals are
at ends of the window, with pattern `s` (`μ_ψ(x_i = 1) = p₊` iff `s_i = 1`), then `ψ = u·d(·,s) + const`: **at a cone the
oracle reveals the instance up to a constant, and one evaluation certifies `ln A` exactly.**
*Proof.*  Given `x_{−i}` the conditional odds of `x_i = 1` are `(p/q)e^{−[ψ(x^{i=1}) − ψ(x^{i=0})]} ∈ (p/q)[e^{−u}, e^{u}]`, and the
marginal is an average of conditional probabilities; equality at an end forces the increment `∓u` for every
`x_{−i}` (full support).  ∎

**Lemma 1 (indistinguishability with an oracle) [P; Theorem 11.22(c) **[V]** for the member of the family with a
fixed index].**  (a) Let `ψ₀, ψ_j ∈ L_u` (`j ∈ J`) with `o(ψ_j) = o(ψ₀)` and `|ln A(ψ_j) − ln A(ψ₀)| > ε`, `D_j := {ψ_j ≠ ψ₀}`.  Every
`(ε/2, δ)`-correct oracle algorithm makes on `ψ₀` at least `(1 − 2δ)·|J| / max_x #{j : x ∈ D_j}` evaluations in
expectation.  (b) Let `(ψ_j, ψ′_j)_{j∈J}` be pairs in `L_u`, **all `2|J|` instances with the same oracle answer**,
`|ln A(ψ_j) − ln A(ψ′_j)| > ε`, `D_j := {ψ_j ≠ ψ′_j}`.  Every non-adaptive `(ε/2, δ)`-correct oracle algorithm makes at least
`(1 − 2δ)·|J| / max_x #{j : x ∈ D_j}` evaluations in expectation.
*Proof.*  (a) The run on `ψ₀` and the run on `ψ_j` use the same member of the family; on the event that the queried
set `Q` misses `D_j` they coincide, and the common output cannot be within `ε/2` of both targets, so
`P(Q ∩ D_j ≠ ∅) ≥ 1 − 2δ`; sum over `j`.  (b) The law of `Q` is the same for all `2|J|` instances; conditionally on
`Q ∩ D_j = ∅` the outputs on `ψ_j` and `ψ′_j` have the same law; conclude as in (a).  ∎

**Lemma 2 (the excess of a dip is the cone law) [P; exact sums and enumeration §3.3, §3.4].**  Let `|γ| ≤ u`, `s ∈ T_k`,
`r > 0`, and `Δ_{s,r} := (e^r c̃_s − w̃_γ)₊`, so that `w̃_γ + Δ_{s,r} = max(w̃_γ, e^r c̃_s) ∈ 𝒲_u` is the dip of depth `r` at `s` on the
base `γ`; `D_{s,r} := {Δ_{s,r} > 0} = {x : π_γⁿ(x) < e^r π_s(x)}`.  Its mass `E_{k,r} := A(Δ_{s,r})` and density `c_{k,r} := dens(Δ_{s,r})`
depend on `(k, r)` only, and

    e^r − 1 ≤ E_{k,r} ≤ e^r ,        | c_{k,r} − c₀(k/n) | ≤ 1/(e^r − 1).

*Proof.*  `π·Δ_{s,r} = e^r π_s − min(e^r π_s, π_γⁿ)`; put `J := Σ_x min(e^r π_s, π_γⁿ) ∈ [0,1]` and let `c_J ∈ [0,1]` be the density
of that minimum.  Then `E = e^r − J` and `E·c = e^r c₀ − J c_J`, so `c − c₀ = J(c₀ − c_J)/(e^r − J)`.  Permutation
invariance of `π` and `w̃_γ` gives the dependence on `(k,r)` only.  ∎
So for `r` bounded away from `0` the one-body statistics of the excess are those of the *cone law* `π_s` — the output
of the vertex channel — up to `1/(e^r − 1)`; for extensive depths the error is exponentially small.  (`J` is in
fact exponentially small in `n` at fixed `r`, by a Chernoff bound; not needed.)

**Lemma 3 (compensation) [P; exact enumeration §3.3].**  Let `G` be a group of permutations of the coordinates that
is transitive on the sites.  Let `w ∈ 𝒲_u` and `Δ ≥ 0`, `Δ ≢ 0`, with `w + Δ ∈ 𝒲_u`, both `G`-invariant; `A_w, c_w` and
`A_Δ, c_Δ` their masses and densities.  Then:
(i) all one-body marginals of `μ_w` equal `c_w`, and all those of `μ_{w+Δ}` equal `(A_w c_w + A_Δ c_Δ)/(A_w + A_Δ)`: **the two
instances have the same oracle answer iff `c_Δ = c_w`** (the excess has the density of the base);
(ii) if `|γ₂| ≤ u` and `c_Δ` lies strictly between `c_w` and `p₂ := p_{γ₂}`, then with

    b := A_w (c_Δ − c_w) / (p₂ − c_Δ)  > 0

the weights `w₀ := w + b·w̃_{γ₂}` and `w₁ := w + Δ + b·w̃_{γ₂}` are in `𝒲_u`, are `G`-invariant, have **all one-body marginals
equal to `c_Δ`**, differ exactly on `{Δ > 0}`, and `A(w₁)/A(w₀) = 1 + (A_Δ/A_w)·(p₂ − c_Δ)/(p₂ − c_w)`.
*Proof.*  (i) `G` permutes the marginals of an invariant measure, so they all equal its density; `μ_{w+Δ}` is the
mixture of `μ_w` and `πΔ/A_Δ` with weights `A_w : A_Δ`.  (ii) The cone property gives membership.  The density of
`πw₀ = πw + b·π_{γ₂}ⁿ` is `(A_w c_w + b p₂)/(A_w + b)`, which equals `c_Δ` iff `b(p₂ − c_Δ) = A_w(c_Δ − c_w)`; then `μ_{w₁}` is a
mixture of two measures of density `c_Δ`.  `A(w₀) = A_w + b = A_w(p₂ − c_w)/(p₂ − c_Δ)`.  ∎
*Remarks.*  (1) By Lemma 0 no class member has a marginal outside the window, so compensation by class members is
possible **iff `c_Δ ∈ [p₋, p₊]`**; taking `γ₂ = ∓u` it is always possible when `c_Δ` is in the open window.  (2) The
excess `Δ` does not depend on `b`: the equation is linear and needs no intermediate-value argument.  This is the
difference from moving the base along the additive instances and taking its deepest dip each time, where the
mismatch vanishes at both ends without a sign change (the "trap" of theory report §11.29, `DEAD_ENDS` D54 item 3 at
`dcdfea6`).  (3) The general principle — one number, one continuous parameter of the adversary — is step (3) of
the coordinator's sketch and the theory division's remark in THY-RES-0005 §2 (Q4); what is added here is the
specific parameter and the decoupling that makes the matching exact and explicit.

### 2.2 The adaptive exponent is unchanged

**Theorem A (every `n`; adaptive algorithms with an exact one-body oracle) [P; every finite ingredient checked by
exhaustive enumeration for `n ≤ 16` (in exact rational arithmetic for `n ≤ 10`) and by type-class sums for `n ≤ 3200`].**  Let `0 < p < 1`, `u > 0`, `n ≥ 2`,
`|γ| ≤ u`, `1 ≤ k ≤ n − 1`, `m = k/n`, `m̲ := min(m, 1−m)`, `ω_m := ω·m̲`, and let `r > 0` satisfy `(e^r − 1)·ω_m > 1`.  Put
`κ := ω_m − 1/(e^r − 1)` and `β := ω/κ`.  There are `γ₂ ∈ {−u, +u}` and `b ∈ [0, β]` such that for the instance
`ψ₀ := −ln(w̃_γ + b·w̃_{γ₂}) ∈ L_u` the following holds: every randomised oracle algorithm (adaptive, with any hint) that
is `(ε/2, δ)`-correct for `ln A` on `L_u`, for some `ε < ln(1 + (e^r − 1)/(1 + β))`, makes on `ψ₀` in expectation at least

    (1 − 2δ) / ( n · H_{k,r} )   ≥   (1 − 2δ) · e^{−tr} · ρ_t(k/n; γ)^{−n} / ( n(n+1) )        for every t ≥ 0,

evaluations, where `H_{k,r} := max_x P_{s ∼ Unif(T_k)}[ x ∈ D_{s,r} ]`.  In particular, for every `ε > 0` and `0 ≤ t ≤ 1`,
choosing `r` suitably,

    E|Q(ψ₀)|  ≥  (1 − 2δ) · e^{−tε} · ρ_t(k/n; γ)^{−n} / ( C_m · n(n+1) ),        C_m := 1 + 2/m̲ + 2/ω_m ,

to be compared with `(1 − 2δ)e^{−tε}·(min_m ρ_t(m;γ))^{−n}` without the oracle (Theorem 11.59(a)).
*Proof.*  For `s ∈ T_k` let `Δ̄_s := n⁻¹Σ_{j<n} Δ_{σ^j s, r}`.  Then `w̃_γ + Δ̄_s` is an average of the `n` class members
`max(w̃_γ, e^r c̃_{σ^j s})`, hence in `𝒲_u`; it is invariant under the cyclic group; `A(Δ̄_s) = E_{k,r}`, `dens(Δ̄_s) = c_{k,r}`,
`{Δ̄_s > 0} = ∪_j D_{σ^j s, r}`.  By Lemma 2, `|c_{k,r} − c₀(m)| ≤ 1/(e^r − 1) < ω_m`, and `c₀(m)` is at distance `≥ ω_m` from both
ends of the window, so `c_{k,r} ∈ (p₋ + κ, p₊ − κ)`.  If `c_{k,r} > p_γ` take `γ₂ = −u` (`p₂ = p₊`), if `c_{k,r} < p_γ` take
`γ₂ = +u`, if `c_{k,r} = p_γ` take `b = 0`; Lemma 3 with `w = w̃_γ`, `Δ = Δ̄_s` gives `b = (c_{k,r} − p_γ)/(p₂ − c_{k,r}) ∈ [0, ω/κ]`,
**the same `b` for every `s ∈ T_k`**.  So `w₀ = w̃_γ + b w̃_{γ₂}` and the `|T_k|` alternatives `w₁^{(s)} = w₀ + Δ̄_s` are class
members with the common oracle answer `(c_{k,r}, …, c_{k,r})`, and
`ln A(w₁^{(s)}) − ln A(w₀) = ln(1 + E_{k,r}/(1+b)) ≥ ln(1 + (e^r − 1)/(1+β)) > ε`.  Lemma 1(a): a point `x` lies in
`{Δ̄_s > 0}` for at most `Σ_j #{s ∈ T_k : x ∈ D_{σ^j s,r}} = n·#{s ∈ T_k : x ∈ D_{s,r}}` centres (`σ^j` permutes `T_k`), which
gives `(1−2δ)/(n H_{k,r})`.  For the second form: `Unif(T_k)` is `Bern(m)^{⊗n}` conditioned on an event of probability
`≥ 1/(n+1)`, and for `s ∼ Bern(m)^{⊗n}`, with `Φ_s(x) := Σ_i ln(π_γ(x_i)/π_{s_i}(x_i))`, Markov's inequality gives
`P(Φ_s(x) < r) ≤ e^{tr} E e^{−tΦ_s(x)} = e^{tr} Π_i [(1−m)(π_0(x_i)/π_γ(x_i))^t + m(π_1(x_i)/π_γ(x_i))^t] ≤ e^{tr}ρ_t(m;γ)ⁿ`.
For the last display take `r := ln(1 + max{2/ω_m, (1 + 2/m̲)(e^ε − 1)}) + η`, `η ↓ 0`: then `κ ≥ ω_m/2`, `β ≤ 2/m̲`,
`ε < ln(1 + (e^r − 1)/(1+β))`, and `e^{tr} ≤ e^{tη}[(1 + 2/m̲)e^{ε} + 2/ω_m]^t ≤ e^{tη}·e^{tε}·C_m` for `t ≤ 1`.  ∎

**Corollary A (the class exponent) [P for the lower bound; the upper bound is Theorem 11.64, black box].**  For
every `p, u`, `δ < ½`:
(a) for `0 ≤ ε₁ < E` and all `n ≥ n₀(p,u,ε₁)`, the worst-case expected cost of `(ε₁n/2, δ)`-correct oracle algorithms is
at least `(1 − 2δ)·c·e^{n·R^max(ε₁)}/(n(n+1))`, with `c = c(p,u,ε₁) > 0` (take `γ = γ*`, `t = t*`, `k = round(m*n)` in Theorem A;
`ρ_{t*}(k/n;γ*)ⁿ ≤ e^{L}·e^{−nF*(t*)}`, `L` a Lipschitz constant of `ρ` in `m`; `0 < m* < 1` because `F*(t*) > 0`; `n₀` only
ensures `1 ≤ k ≤ n−1` and `min(k, n−k)/n ≥ ½·min(m*, 1−m*)`);
(b) for every fixed `ε > 0`: at least `(1 − 2δ)·c′·e^{nh}/(n(n+1))`, `h = R^max(0)`;
(c) hence for `0 < ε₁ < E` **the adaptive exponent with the oracle is `R^max(ε₁)`, the value without it**.
The hard instance is `ψ₀ = −ln(w̃_{γ*} + b·w̃_{∓u})`: its Gibbs measure is the mixture
`(π_{γ*}ⁿ + b·π_{∓u}ⁿ)/(1+b)` of two product measures, with `b ≈ (c₀(m*) − p_{γ*})/(p_± − c₀(m*))` (`0.11 … 0.62` in the examples
of §3) — a two-state ensemble whose one-body averages equal those of the same ensemble with a hidden dip added.

### 2.3 The non-adaptive exponent is unchanged

**Theorem B (every `n`; non-adaptive algorithms) [P; uses Theorem 11.61(a) **[V]** (`truncate_lipschitz_insert`,
`truncate_lipschitz_erase`, `truncate_ne_iff`); enumeration `n ≤ 14`, exact sums `n ≤ 1600`].**  Let `1 ≤ k ≤ n − 1`,
`m = k/n`, `0 < q < 1`, `s ∈ T_k`, and let `c̃_s^{tr}` be the truncation of the normalised cone at its type-wise upper
`q`-quantiles (Theorem 11.61(a): it is in `𝒲_u` and differs from `c̃_s` on a set `B_s` of density at most `q` in every type
class).  Put `A_t := A(c̃_s^{tr}) ≤ 1` (a function of `k, q`).  If `A_t < ω_m/2`, then for every
`ε < ln(1/A_t) − ln(2/ω_m)` every randomised non-adaptive oracle algorithm that is `(ε/2, δ)`-correct on `L_u` makes at
least `(1 − 2δ)/(n·q)` evaluations in expectation.
*Proof.*  Let `c̄_s`, `c̄_s^{tr}` be the averages over the `n` cyclic shifts of `s`; both are in `𝒲_u` and cyclically invariant.
Apply Lemma 3 with `w = c̄_s^{tr}` (mass `A_t`, density `c_t`) and `Δ = c̄_s − c̄_s^{tr} ≥ 0` (mass `1 − A_t`, density `c_Δ`).  Since
`c₀(m) = A_t c_t + (1 − A_t)c_Δ`, `|c_Δ − c₀(m)| ≤ A_t`, so `c_Δ` is in the open window at distance `κ′ := ω_m − A_t ≥ ω_m/2` from
its ends.  Take `p₂ = p₊` if `c_Δ > c_t`, `p₂ = p₋` if `c_Δ < c_t` (`b = 0` if equal): `b = A_t(c_Δ − c_t)/(p₂ − c_Δ) ≥ 0`, the same for
all `s ∈ T_k`.  The pairs `(c̄_s^{tr} + b w̃_{γ₂}, c̄_s + b w̃_{γ₂})`, `s ∈ T_k`, consist of class members which **all** have the
one-body marginals `(c_Δ, …, c_Δ)`; a pair differs on `∪_j B_{σ^j s}`; and
`A(w₁)/A(w₀) = 1 + ((1−A_t)/A_t)(p₂ − c_Δ)/(p₂ − c_t) ≥ 1 + κ′(1 − A_t)/A_t ≥ κ′/A_t`.  Lemma 1(b): the relation `x ∈ B_s` depends
on the joint type of `(x, s)` only, so for fixed `x` the fraction of `s ∈ T_k` with `x ∈ B_s` equals the density of `B_s` in
the type class of `x`, at most `q`; the union over shifts costs the factor `n`.  ∎

**Corollary B [P given Theorem 11.61(c), (d), black box].**  For `0 < ε₁ < E` the exponent of non-adaptive oracle
algorithms is `θ_na(ε₁)`, the value without the oracle; at every bounded accuracy it is at least `a` (the Shannon
capacity of the vertex channel).  *Proof.*  For `θ < θ_na(ε₁)` there is a centre type `m ∈ (0,1)` with
`min{D(V‖W|M) : I(M,V) ≤ θ′} ≥ ε₁ + 2η` for `θ′` near `θ`, and by Theorem 11.61(c)
`ln(1/A_t(k, e^{−nθ})) ≥ n(ε₁ + 2η) − O(ln n)`; Theorem B gives `(1−2δ)e^{nθ}/n`.  The upper bound ignores the
oracle.  A lower bound at accuracy `ε₁n` is one at every smaller accuracy; let `ε₁ ↓ 0`.  ∎

*Consistency with the uniform cube.*  At `p = ½`, `γ = 0`: `c_Δ = c_w = ½` by the symmetry `x ↦ 1 − x`, so `b = 0`, and
Theorems A, B are Theorem 4 and Theorem 4′ for `k = 1` with the cyclic group in place of a code.

### 2.4 What is wrong with the sketch of the brief

**Proposition S [(i) K, checked; (ii) P = Lemma 2; (iii), (iv) N].**
(i) Augustin's identity `Q* = Σ_φ M*(φ)V_φ`, `V_φ ∝ π_φ^{t*}Q*^{1−t*}`, holds at the saddle (to `10⁻⁹` in all cases; it is the
stationarity condition of `min_Q Σ_φ M*(φ)D_t(π_φ‖Q)`).
(ii) `V_φ` is **not** the type that carries the mass of a hidden dip.  It is the minimiser in
`min{I(M,V) : D(V‖W|M) − D(V‖π_γ|M) ≤ e}`, i.e. the joint type of the points of the dip's support that a sampler hits
most cheaply — the *rim*, where the dip weight barely exceeds the base.  The mass sits on the cone law `V = W`
(Lemma 2), exactly as on the uniform cube, where the excess sits on the shell `d ≈ n/(1 + e^u)` while the rim is at
`ρ₀n` (addendum A10).
(iii) The identity that the oracle argument needs is therefore `M*W = Q*` — the capacity-achieving output law
equals the centre — which is true at `t = 1` (Shannon) and at `p = ½` (symmetry) and **false otherwise**: the gap
`(M*W − Q*)(1)` is `+0.018, +0.024, +0.029, +0.035` at `(p,u) = (0.3, 1)`, `e/E = 0, 0.3, 0.6, 0.9`, and `+0.064 … +0.127` at
`(0.1, 2)` (§3.2).
(iv) So with **additive** bases the constraint binds: plain dips of the centre type `m(γ)` forced by
`c₀(m) = p_γ` have the exponent `Rcc(γ, m(γ); e)`, and `max_γ Rcc(γ, m(γ); e)` is `13 %` below `R^max` at `(0.3, 1, e = 0)`, `45 %`
below at `e = 0.3E`, and **zero** from `e = 0.6E` on (`(0.1, 2)`: `43 %` below at `e = 0`, zero from `0.3E`).  What rescues the
class exponent is not a property of the hardest additive instance but the freedom to leave the additive
instances (Lemma 3).

### 2.5 At an instance the oracle helps: the zero residual with a field (the coordinator's second question)

For an additive instance `ψ_γ` let `R_γ^{orc}(e)` denote the exponent of the least cost *at `ψ_γ`* of oracle algorithms
that are `(en/2, δ)`-correct on the whole class and are given `γ` as a hint (as in Theorem 11.59(a); at an additive
instance the hint costs `n + 1` evaluations).  Write `θ = ln(q/p)` for the field and `R_γ(e; θ)` for the hinted exponent
without oracle at the field `θ`.

**Proposition C (the tilt inequality, and an algorithm that uses the oracle) [(a) P, checked by enumeration §3.5;
(b) P given the hinted theorem of the theory division at shifted fields (black box); (c) N].**
(a) Let `ψ′ ∈ L_u`, `|γ| ≤ u`, and let `Δ := π(e^{−ψ′} − e^{−ψ_γ})/A(ψ_γ)` be the (signed) excess measure, of total mass
`Φ = A(ψ′)/A(ψ_γ) − 1`.  For real `λ` let `π^{(λ)} := Bern(p^{(λ)})^{⊗n}`, `logit p^{(λ)} = logit p + λ`, `A^{(λ)}` the same
functional with this reference, and `c_γ(λ) := ln(1 − p_γ + p_γe^{λ}) − λp_γ ≥ 0`.  Then

    A^{(λ)}(ψ′)/A^{(λ)}(ψ_γ) − 1  =  e^{−n c_γ(λ)} · Σ_x Δ(x) e^{λ(|x| − n p_γ)} ,

and **if `ψ′` has the one-body marginals of `ψ_γ`**, then for every real `λ`

    ln A^{(λ)}(ψ′) − ln A^{(λ)}(ψ_γ)  ≥  ln A(ψ′) − ln A(ψ_γ) − n·c_γ(λ) ;

if moreover `Δ ≥ 0`, the excess form `Φ^{(λ)} ≥ Φ·e^{−n c_γ(λ)}` holds.
*The same two functions, in the same class, are still far apart when the field is changed.*
(b) Consequently, for `e > 0` and every `λ` with `c_γ(λ) < e`: the set on which a matched alternative with
`ln A(ψ′) − ln A(ψ_γ) ≥ en` differs from `ψ_γ` is hit by the type-uniform sampler with probability at least
`exp(−n·R_γ(e − c_γ(λ); θ − λ) − o(n))`, and

    R_γ^{orc}(e)  ≤  U_γ(e) := inf{ R_γ(e − c_γ(λ); θ − λ) : c_γ(λ) < e } .

The algorithm: given the hint `γ`, **reject the hint if the oracle's answers are not `(p_γ, …, p_γ)`** (then evaluate
everything); otherwise run the hedged spot-check of Theorem 11.22(e) with `e^{nU_γ(e) + o(n)}` points from
`½π_γⁿ + ½·`(uniform on types, uniform inside each type class).  The oracle is used for one comparison only.
(c) The derivative of `λ ↦ R_γ(e − c_γ(λ); θ − λ)` at `λ = 0` is `−∂_θ R_γ(e; θ)` (because `c_γ′(0) = 0`); at `γ = 0` it vanishes
for `p = ½` (symmetry) and is non-zero in every case computed with `p ≠ ½` (`+0.0088` at `(0.3, 1)`, `+0.0277` at `(0.1, 2)`,
`e = 0.2E_0`): **for `p ≠ ½` the oracle strictly lowers the exponent of the zero residual**, and likewise that of the
hardest additive instance `γ*` (§3.5).  The threshold drops too: `E_0^{orc} ≤ min_λ[E_0(θ − λ) + c_0(λ)]`, which is `< E_0`
in every case computed with `p ≠ ½` (ratio `0.99 … 0.37`, §3.5); for accuracies in between, the cost at the zero
residual is `e^{o(n)}` with the oracle and `e^{nR_0}` without.
*Proof.*  (a) `Σ_x π^{(λ)}(x)w(x) = Z_λ^{−n}Σ_x π(x)e^{λ|x|}w(x)` for every weight `w`, with `Z_λ = q + pe^{λ}`; for `w = e^{−ψ_γ}` this
is `Z_λ^{−n}A(ψ_γ)(1 − p_γ + p_γe^{λ})ⁿ`; divide.  If the marginals agree, `E_{μ_{ψ′}}|x| = np_γ`, and by Jensen
`E_{μ_{ψ′}}e^{λ(|x| − np_γ)} ≥ 1`, i.e. `Σ_x π(x)e^{−ψ′(x)}e^{λ|x|} ≥ A(ψ′)e^{λnp_γ}`.  If `Δ ≥ 0`, Jensen for `Δ/Φ`, whose mean
type is `p_γ` by Lemma 3(i).  (b) `ψ′` and `ψ_γ` are members of `L_u` whatever the reference; by (a) they differ by
at least `n(e − c_γ(λ))` in `ln A^{(λ)}`; the hinted theorem for the additive instance `γ` at the field `θ − λ` (theory
report Theorem 11.27, "`R^gen` is the exponent" — workstream A's Theorem A, refereed — in the form of Theorem
11.59(a)) bounds from below the probability of their difference set under `½(π_γ^{(λ)})ⁿ + ½·`type-uniform, and the
type-uniform law dominates every product measure up to the factor `n + 1`.  Alternatives with a *smaller* `ln A`
differ on `π_γⁿ`-mass at least `1 − e^{−η}` (Theorem 11.28(c)).  ∎
*Caveat.*  For bounded accuracy (`e = 0`) the admissible range of `λ` is `{0}`; the values of `U` at `e = 0` quoted below
use the isoperimetric statement for negative `e` (stated for all real `e` in Theorem 11.63 for the flat-histogram
reference; for an additive reference I have not read it in that generality).

**Proposition D (lower bounds at an additive instance with the oracle) [(a) P; (b) P sketch, exact sums §3.6].**
(a) *Plain dips of two centre types.*  Let `k₁ < k₂`, `r > 0` with `c_{k₁,r} ≤ p_γ ≤ c_{k₂,r}` (Lemma 2: possible with
`k_i/n → m(γ)`, where `c₀(m(γ)) = p_γ`, as soon as `r → ∞`), `E_i := E_{k_i,r}`, and
`λ := E₂(c_{k₂,r} − p_γ)/[E₁(p_γ − c_{k₁,r}) + E₂(c_{k₂,r} − p_γ)]`.  The weights `w̃_γ + λΔ̄_{s₁,r} + (1−λ)Δ̄_{s₂,r}`,
`(s₁, s₂) ∈ T_{k₁} × T_{k₂}`, are class members with **all one-body marginals equal to `p_γ`** and `ln A` larger by at least
`r`; so for `ε < r` every oracle algorithm makes at `ψ_γ` at least `(1 − 2δ)/(n(H_{k₁,r} + H_{k₂,r}))` evaluations:
`R_γ^{orc}(e) ≥ Rcc(γ, m(γ); e)`.
(b) *Dips around shells do better.*  For `s ∈ T_k` and the shell `Sh_s(j₁, j₀) := {y : #(y ∧ s) = j₁, #(y ∧ ¬s) = j₀}` the
weight `e^{−u·d(·, Sh_s)}` is in `𝒲_u` (a distance to a set), and `max(w̃_γ, C·e^{−u·d(·,Sh_s)})` is an *annular dip*: the
smallest class member with a prescribed lift on the shell.  With `M = (1−m, m)`, `v₁ = j₁/k`, `v₀ = j₀/(n−k)`, the mass
of the excess sits **on the shell iff `v₀, v₁ ∈ [p₋, p₊]`** (otherwise on the nearest admissible shell — exact sums
§3.6), and then the hitting exponent is

    f(m, v₀, v₁; e) := min{ I(M, V′) : Σ_φ M(φ)[u|v′_φ − v_φ| + γ(v_φ − v′_φ)] ≤ e + D(V‖π_γ|M) } .

Mixing two shells whose excess densities bracket `p_γ` (one linear equation, as in (a)) gives

    R_γ^{orc}(e)  ≥  V_γ(e) := sup{ f(m, v₀, v₁; e) : v₀, v₁ ∈ [p₋, p₊], (1−m)v₀ + m v₁ = p_γ }  ≥  Rcc(γ, m(γ); e).

(The plain dip is the shell `(k, 0)`; its profile `(m, p₋, p₊)` has `f ≥ Rcc` with equality at the optimal `m`.)

**The bracket at the zero residual** (`p ≠ ½`; single-letter values [N], `t04`, `t11`):

| `(p, u)`, `e/E_0` | `R_0(e)` no oracle | plain dips, forced centre type `m_0` | `V_0(e)` (shells, two labels) | `U_0(e)` (tilt) |
|---|---|---|---|---|
| `(0.3, 1)`, `0.1` | `0.020056` | `0.015444` | `0.019311` | `0.019571` |
| `(0.3, 1)`, `0.3` | `0.012089` | `0.005667` | `0.011301` | `0.011558` |
| `(0.3, 1)`, `0.7` | `0.002211` | `0` | `0.001638` | `0.001826` |
| `(0.25, 1)`, `0.216` (`e = 0.02`) | `0.013669` | `0.005704` | `0.012630` | `0.012941` |
| `(0.1, 2)`, `0.2` | `0.026849` | `0` | `0.015441` | `0.016345` |
| `(0.1, 2)`, `0.5` | `0.010307` | `0` | `0.001226` | `0.001648` |
| `(0.1, 2)`, `0.7` | `0.003686` | `0` | `0` | `0` |
| `(0.05, 3)`, `0.1` | `0.043693` | `0` | `0.016939` | `0.017479` |
| `(0.05, 3)`, `0.5` | `0.012925` | `0` | `0` | `0` |
| `(0.5, 1)`, any | all four columns equal | | | |

So `V_0(e) ≤ R_0^{orc}(e) ≤ U_0(e) < R_0(e)`: **the answer to "is the instance-wise bound the hinted exponent restricted
to the centre types forced by the matching equation, and is it strictly below `R_0`?" is: strictly below — yes (and
by up to 100 %); restricted to the forced centre types — no: that is a valid lower bound (column 3) far below the
truth; the adversary's best matched alternatives are dips around shells whose *excess* has the type `p`
(column 4), and the gap that remains is between columns 4 and 5.**  The optimum of `V` always has `v₀ = p₋`: the
constraint "the excess mass sits on shells inside the window" is active, and the tilt bound does not see it
(`U_0` equals, to six digits, the supremum of `f` over profiles of type `p` with `v₀, v₁` *unrestricted*, attained at the
cone laws of the tilted reference, of which one lies outside the window — §3.6, §8).
**Conjecture Z [C].**  `R_γ^{orc}(e) = sup{f(P; e)}` over profiles `P` with finitely many labels, label-conditional laws
in the window and mean type `p_γ` — i.e. the left end of the bracket, possibly with more than two labels.  (What is
missing is an isoperimetric upper bound that knows the window: a type-resolved version of Theorem 11.63.)

### 2.6 `k = 2`: what changes, and an exact solution

**Proposition E [(i)–(iii) P, exact enumeration at `n = 11, 13` (§3.7); (iv) P sketch; (v) C].**
(i) *Reduction to two numbers.*  Let `G` be a permutation group on `[n]` that is transitive on sites and on
unordered pairs — e.g. `AGL(1, q)` on `F_q`, `n = q` a prime power, sharply 2-transitive of order `n(n−1)` **[K, standard;
from memory]**.  Every `G`-invariant finite measure `ν ≥ 0` has all one-body marginals equal to `c₁(ν) := E_ν|x|/n` and all
pair probabilities `ν(x_i = x_j = 1)/ν(X)` equal to `c₂(ν) := E_ν[|x|(|x| − 1)]/(n(n−1))`.  So two `G`-invariant instances have
the same one- **and two-body** marginals iff their `(c₁, c₂)` agree.  The same holds with the average of `Δ_{s,r}` over the
blocks `s` of a `2`-`(n, k, λ)` design in place of a `G`-orbit (the pair marginal of `Δ_{s,r}` at `(i, j)` depends on
`(s_i, s_j)` only), and such designs with polynomially many blocks exist for all `n` and `k` (**[K]**
Kuperberg–Lovett–Peled, Theorem 1.3, statement read in full: a `t`-`(v, k, λ)` design of size at most `(cv/t)^{ct}` for all
`v ≥ 1`, `1 ≤ t ≤ v`, `t ≤ k ≤ v`).
(ii) *The obstruction.*  A mixture `Σ_l a_l π_{γ_l}ⁿ` of product measures has `c₂ − c₁² = Var_a(p_γ) ≥ 0`.  The average of
the cone laws `π_s` over `s ∈ T_k` has `c₂ − c₁² = −m(1−m)ω²/(n−1) < 0` (the centre letters are sampled without
replacement).  So, with a base that is a mixture of additive instances, **dips of a single centre type can never be
matched in the two-body marginals** (their excess is within `O(1/(e^r − 1))` of the cone law): "one more number, one
more parameter" is not enough — the excess must first be moved above the parabola `c₂ = c₁²`.
(iii) *The solution is again a two-component base.*  Let `Δ ≥ 0` be `G`-invariant with `w̃_γ + Δ ∈ 𝒲_u`,
`(x, y) := (c₁, c₂)(Δ)`, `h := y − x²`, `g := x − p_γ`.  If `h > 0`, `g ≠ 0` and `p₂ := x + h/g ∈ [p₋, p₊]`, then with `b := g²/h` and
`p_{γ₂} = p₂` the instances `w₀ = w̃_γ + b·w̃_{γ₂}` and `w₀ + Δ` have **identical one- and two-body marginals**, and
`A(w₀ + Δ)/A(w₀) = 1 + A(Δ)·h/(h + g²)`.
*Proof.*  With `a = 1/(1+b) = h/(h + g²)` the base has `c₁ = p_γ + (1−a)(p₂ − p_γ) = p_γ + [g²/(h+g²)]·[(g² + h)/g] = x` and
`c₂ − c₁² = a(1−a)(p₂ − p_γ)² = h`; apply (i) to the mixture `μ_{w₀+Δ}` of `μ_{w₀}` and `πΔ/A(Δ)`.  ∎
(iv) *Getting above the parabola.*  For `Δ = θΔ̄₁ + (1−θ)Δ̄₂` (the `G`-averages of dips of centre types `k₁ < k₂`),
`h = θ′(1−θ′)(x₂ − x₁)² + θ′h₁ + (1−θ′)h₂` with `θ′ ∝ θE₁`, `x_i ≈ c₀(k_i/n)`, `h_i ≈ −m_i(1−m_i)ω²/(n−1)`: positive as soon as
`k₂ − k₁ ≳ 2√(n·m(1−m))`.  With `k_{1,2} = round(m*n ∓ √n)`, `r = ε + O(ln n)` (so that the excess moments are within
`o(1/n)` of the cone laws'), `h = Θ(1/n)`, `p₂ − x = h/g = O(1/n)`, `a = Θ(1/n)`: the bound of Theorem A is divided by a
further polynomial factor (`|G|`, `1/a`) and by `e^{O(√n)}` if one uses the Markov form (`ρ_t` has a kink at `m*`) — **the
exponent `R^max` is unchanged by an exact oracle for all one- and two-body marginals** (for `n` a prime power by the
group; for all `n` by KLP designs).  Not written out: the uniform estimate of the excess moments.
(v) **[C]** For every fixed `k`, exact `k`-body marginals change no exponent: `t`-designs (`t = k`) reduce the matching
to the first `k` factorial moments of `|x|` under the excess and under an exchangeable base (a mixture of product
measures has the moments `Σ_l a_l p_l^j`); mixing `> k/2` centre types brings the excess moments into the interior of
the moment space; an atom at `p_γ` of small positive mass can then be split off.  The theory division states the
same reduction (§11.29 at `dcdfea6`, last paragraph: "`k` matching conditions … open").

### 2.7 Tolerances: all marginals of every order, absolute precision `τ`

*Model* (as in addendum A10, for marginal probabilities): for the instance `ψ` the oracle returns numbers `m_{S,a}`
for every non-empty `S ⊆ [n]` and `a ∈ {0,1}^S`, subject only to `|m_{S,a} − μ_ψ(x_S = a)| ≤ τ`.

**Theorem τ [P; its ingredients checked by enumeration at `n = 12`, §3.9; not checked as a whole].**  Let `0 < τ ≤ 1`, `|γ| ≤ u`, `0 < m < 1`, `0 ≤ t ≤ 1`,
`ε > 0`, `n ≥ 2`; `θ₀ := max(p₊, 1 − p₋) < 1`, `k_τ := ⌈ln(1/τ)/ln(1/θ₀)⌉`, `N := ⌈(k_τ ln(2n) + ln 4)·2^{2k_τ+3}/τ²⌉`.  Let
`γ_c` be the additive instance with `p_{γ_c} = c₀(m)` and `ψ₀ := −ln(w̃_γ + (4/τ − 1)·w̃_{γ_c})`.  Every oracle algorithm with
the `τ`-tolerant oracle of all orders that is `(ε/2, δ)`-correct on `L_u` makes on `ψ₀` (with a legal answer of the
oracle) in expectation at least

    (1 − 2δ) · e^{−tε} · ρ_t(m; γ)^{−n} · τ^{t} / ( 2 · 9^{t} · N )

evaluations.  Hence with `γ = γ*`, `m = m*`, `t = t*`: **the adaptive lower bound `e^{nR^max(ε₁)}` survives, up to a factor
polynomial in `1/τ` and logarithmic in `n`, an oracle that gives every marginal of every order to absolute precision
`τ`; the exponent is unchanged for every `τ ≥ e^{−o(n)}`.**
*Proof.*  *Orders `≥ k_τ`.*  For every class member and every `S, a`: `μ(x_S = a) ≤ θ₀^{|S|}` (chain rule; every
conditional law of one site has `P(1) ∈ [p₋, p₊]`), so for `|S| ≥ k_τ` the answer `0` is legal for all instances.
*Alternatives.*  Let `e^r := (1 + max{8/τ, 4(e^{ε} − 1)/τ})·e^{η}`, `η ↓ 0`.  For a list `L = (s₁, …, s_N) ∈ X^N` put
`w_L := w₀ + N⁻¹Σ_l Δ_{s_l, r}` (a class member: an average of `max(w̃_γ, e^r c̃_{s_l}) + b w̃_{γ_c}`).  With `E_s := A(Δ_{s,r})`,
`ν_s := πΔ_{s,r}/E_s`: `‖ν_s − π_s‖_{TV} ≤ 1/(e^r − 1)` (proof of Lemma 2), `E_s ∈ [e^r − 1, e^r]`, and
`μ_{w_L} − μ_{w₀} = [Ē/(1 + b + Ē)]·(ν̄_L − μ_{w₀})`, `ν̄_L` the `E`-weighted average of the `ν_{s_l}`, which is within
`2/(e^r − 1) ≤ τ/4` in total variation of `N⁻¹Σ_l π_{s_l}`.  For `|S| < k_τ`,
`N⁻¹Σ_l π_{s_l}(x_S = a) = Σ_β f_S(β)Π_{i∈S}π_{β_i}(a_i)` with `f_S(β)` the frequency of the pattern `β` on `S` in the list.  Draw
the `s_l` independently from `Bern(m)^{⊗n}`: `E f_S(β) = M^{⊗S}(β)`, and `Σ_β M^{⊗S}(β)Ππ_{β_i}(a_i) = Bern(c₀(m))^{⊗S}(a)`.  By
Hoeffding and a union bound over the at most `(2n)^{k_τ}` pairs `(S, β)`, with probability at least `½` all
`|f_S(β) − M^{⊗S}(β)| ≤ τ·2^{−k_τ−2}` (*good* lists); then `|N⁻¹Σ_l π_{s_l}(x_S = a) − Bern(c₀)^{⊗S}(a)| ≤ τ/4`.  The base is
`μ_{w₀} = (τ/4)π_γⁿ + (1 − τ/4)Bern(c₀)ⁿ`, within `τ/4` of `Bern(c₀)ⁿ`.  So for good lists every marginal of order `< k_τ` of
`μ_{w_L}` is within `3τ/4` of that of `μ_{w₀}`: **the exact marginals of `ψ₀` (and `0` for orders `≥ k_τ`) are a legal answer
for `ψ₀` and for every good `w_L`.**  *Separation:* `A(w_L)/A(w₀) = 1 + Ē·τ/4 ≥ 1 + (e^r − 1)τ/4 > e^{ε}`.  *Packing*
(Theorem 11.22(c) with the weights of the product measure on lists, restricted to good lists, total weight `≥ ½`):
a point `x` lies in the difference set of `w_L` only if `x ∈ D_{s_l,r}` for some `l`, an event of probability at most
`N·e^{tr}ρ_t(m;γ)ⁿ` (Markov, as in Theorem A); and `e^{tr} ≤ e^{tη}(9e^{ε}/τ)^t`.  ∎
*Remarks.*  (1) No symmetrisation is needed: a list of `O(k_τ 4^{k_τ}ln n/τ²)` independent centres already makes every
low-order marginal of the averaged excess product-like, and the base is made product-like by giving the hard
component the small weight `τ/4`.  (2) For `p = ½` this is another proof of the marginal form of Theorem 4-τ, with
`ln n` in place of `(2n)^{⌈k_τ/2⌉}`, valid down to `τ = e^{−o(n)}`.  (3) The oracle of A10 returns *correlation functions*,
which is stronger at high orders (a correlation of order `j` is a signed sum of `2^j` marginal probabilities); for the
instances used here all components are within `1/(e^r − 1)` of mixtures of product measures, whose correlation of
order `j` is at most `max(|1 − 2p₋|, |1 − 2p₊|)^j`, so the argument of A10 should transfer — **[P sketch]**, not written.
(4) The non-adaptive analogue (cone against truncated cone, both plus `b·w̃_{γ_c}`, `b = 8A_t/τ`, lists of centres of one
type) is the same computation with a floor `τ ≳ k_τ²/n` from the hypergeometric defect — **[P sketch]**.

### 2.8 Reading (kept apart from the statements) **[H]**

*Model-relative.*  Everything above is about the Lipschitz class around an independent-site reference; no
experimental observable enters.  Within that model: (1) **Per-site averaged measurements do not certify a free
energy in the worst case even when the reference ensemble is asymmetric** — not because the hardest
homogeneous ensemble happens to reproduce the averages of its own hidden basins (it does not), but because the
adversary may take the ensemble to be a *population-weighted mixture of two sub-ensembles*.  An averaged
observable cannot tell a homogeneous ensemble from such a mixture, and the mixing weight is exactly the one free
number needed to absorb the signature of a hidden basin.  This is the ensemble-averaging ambiguity familiar from
the interpretation of averaged structural data, here with a price tag: a factor `C_m·n(n+1)` in the lower bound
(`C_m ≈ 15` at `p = 0.3`, `u = 1`).
(2) **The same data are informative once one commits to a homogeneous model.**  If the ensemble is believed to be
the reference itself (zero residual) and the measured per-site averages agree with it, hidden basins must be
"self-averaging" (their extra population must have the reference's composition, which forces shell-shaped rather
than ball-shaped basins), and the cost of certification drops: by a few percent of the exponent in a weak field
(at least `2–17 %` at `p = 0.3`, `u = 1`, growing towards the threshold), by a large part of it in a strong one (at least
`21–100 %` at `p = 0.1`, `u = 2`), and from exponential to sub-exponential in a window of accuracies.  (3) Pair data change nothing in the worst case either, but need a
mixture whose two components are tuned to the *spread* of the hidden basins' compositions; and error bars of
any fixed size make marginals of every order worthless against the worst case, at a polynomial price.  None of
this is a statement about a physical system: the class constant `u`, the reference and the oracle are idealisations.

---

## 3. Numerics (all scripts in `experiments/science/ws_F/`; outputs in `out/`; own code, nothing imported from the other divisions)

### 3.1 Single-letter formulas against the theory report (`sl.py`, `t01_single_letter.py`)

Independent implementation from the statements: closed form of Theorem 11.59(b) against the exact value of the
`2×2` game, `1.5·10⁻¹⁴` on 2000 random `(p, u, γ, t)`; Sibson form of `F*` against `max_γ F(γ,·)`, `3·10⁻¹⁶`; the table of
§11.20 (`u = 2`, `θ = 0, 0.5, 1, 2, 3`: `R_0`, `R^max`, `γ*`, `a`) to all printed digits; `R_0(0.3E) = 0.019497`,
`R^max(0.3E) = 0.023270` at `(0.1, 2)`; `θ_na = 0.1020, 0.0440, 0.0243`; the row `bin` of the table of §11.26 to six digits;
the pair identity `θ_na(e + R^max(e)) = R^max(e)` to `10⁻⁸`; `Rcc` dual against primal `5·10⁻¹⁵`, `max_m Rcc = R_γ`.

### 3.2 The fixed point, and the identity that fails (`t02_fixed_point.py`; 36 rows)

| `p, u` | `e/E` | `m*` | `Q*(1) = p_{γ*}` | `Σ_φ M*V_φ(1)` (Augustin) | `(M*W)(1)` | gap | `R^max` | forced type at `γ*` | best additive base, forced types | loss |
|---|---|---|---|---|---|---|---|---|---|---|
| `0.5, 1` | `0.3` | `0.5000` | `0.5000` | `0.5000` | `0.5000` | `0` | `0.014206` | `0.014206` | `0.014206` | `0` |
| `0.3, 1` | `0` | `0.5006` | `0.319398` | `0.319398` | `0.337382` | `+0.0180` | `0.025034` | `0.021574` | `0.021746` | `13 %` |
| `0.3, 1` | `0.3` | `0.5096` | `0.317452` | `0.317452` | `0.341011` | `+0.0236` | `0.012209` | `0.006272` | `0.006707` | `45 %` |
| `0.3, 1` | `0.6` | `0.5186` | `0.315537` | `0.315537` | `0.344620` | `+0.0291` | `0.003975` | `0` | `0` | `100 %` |
| `0.1, 2` | `0` | `0.5065` | `0.171335` | `0.171335` | `0.235677` | `+0.0643` | `0.048130` | `0.025043` | `0.027239` | `43 %` |
| `0.1, 2` | `0.3` | `0.5373` | `0.163304` | `0.163304` | `0.249100` | `+0.0858` | `0.023270` | `0` | `0` | `100 %` |
| `0.05, 3` | `0` | `0.5156` | `0.164455` | `0.164455` | `0.266243` | `+0.1018` | `0.072739` | `0.034519` | `0.039992` | `45 %` |
| `0.3, 4` | `0.3` | `0.5217` | `0.422870` | `0.422870` | `0.504075` | `+0.0812` | `0.107447` | `0.093322` | `0.101072` | `5.9 %` |

("forced type at `γ*`" = `Rcc(γ*, m(γ*); e)`; "best additive base" = `max_γ Rcc(γ, m(γ); e)`, 41-point scan with refinement.)
Augustin's identity: `2.9·10⁻⁹` over all rows.  The gap `M*W − Q*` is zero exactly at `p = ½` and positive in all 28 rows
with `p < ½`.  *The first run of this script (401-point scan) was stopped at its 30-minute limit; its partial output
is kept (`out/t02_fixed_point_partial_first_run.txt`) and agrees with the light version on the rows it reached.*

### 3.3 Exhaustive enumeration of the compensated adaptive construction (`t03_enum_adaptive.py`; `n = 8 … 16`)

Eight parameter sets (`p ∈ {0.1, 0.2, 0.3}`, `u ∈ {1, 1.5, 2}`, `γ = γ*` or `0`, centre a block of `k` ones, depth by bisection
so that the separation is `ε`).  On the whole cube: base and alternative in the class (largest single-flip
`|ln ratio| ≤ u`); **all `n` one-body marginals of base and alternative equal, largest difference `1.4·10⁻¹³`**; separation
`= ln(1 + E/(1+b))` to `10⁻⁹`; `b = 0.17 … 0.62`.  Controls: without compensation the marginals of base and alternative
differ by `1.4·10⁻² … 8.2·10⁻²`; a single unsymmetrised dip has marginals spread over e.g. `[0.105, 0.404]`.  At these
sizes the packing numbers are trivial (the exponents are `0.01 … 0.05`); for `n ≤ 12` the exact orbit-union count was
compared with the union bound of the proof.
**Exact rational arithmetic** (`t16_exact_rational.py`; Python fractions, no rounding at all; `n = 8, 8, 10`, with `p`, `e^{−u}`,
`e^{−γ}`, `e^r` rational, e.g. `p = 1/10`, `e^{−u} = 1/7`, `e^{−γ} = 3/2`, `e^r = 3`, `k = 5`): base and alternative are in the class, and
**their one-body marginals are identical as fractions at every site** (all equal to `c_{k,r}`); `A(w₁)/A(w₀) = 1 + E/(1+b)`
exactly; `b = 24607020265/142714081349` in the first case.  One of the three cases has `c_{k,r} < p_γ` (compensator `γ₂ = +u`).

### 3.4 Exact type-class sums for Theorem A (`ts.py`, `t05_typesums_adaptive.py`; `n = 100 … 3200`)

`ε = ε₁n`, `γ = γ*(ε₁)`, centre type scanned near `m*n`; `ln LB` = the exact bound of Theorem A without the factor `1 − 2δ`.
("Exact" here and below: finite sums over the `(n+1)(k+1)` joint-type classes, no asymptotics, evaluated in float64 in
the log domain — not rational arithmetic.)

| `(p, u, ε₁)` | `n` | with oracle `ln LB/n` | `b` | `c_{k,r}` | no oracle `ln LB₀/n` | `ln LB − ln LB₀` | `R^max − ln LB/n` | `× n/ln n` |
|---|---|---|---|---|---|---|---|---|
| `(0.3, 1, 0.3E)`, `R^max = 0.012209` | `400` | `0.001639` | `0.115` | `0.34016` | `0.016647` | `−6.00` | `0.010570` | `0.706` |
| | `800` | `0.006441` | `0.115` | `0.34016` | `0.014841` | `−6.72` | `0.005767` | `0.690` |
| | `1600` | `0.009097` | `0.122` | `0.34142` | `0.013732` | `−7.42` | `0.003112` | `0.675` |
| | `3200` | `0.010542` | `0.118` | `0.34079` | `0.013075` | `−8.10` | `0.001667` | `0.661` |
| `(0.1, 2, 0.3E)`, `R^max = 0.023270` | `400` | `0.012611` | `0.441` | `0.25137` | `0.027830` | `−6.09` | `0.010659` | `0.712` |
| | `800` | `0.017453` | `0.434` | `0.25028` | `0.025961` | `−6.81` | `0.005817` | `0.696` |
| | `1600` | `0.020144` | `0.426` | `0.24919` | `0.024811` | `−7.47` | `0.003127` | `0.678` |
| | `3200` | `0.021586` | `0.427` | `0.24932` | `0.024141` | `−8.18` | `0.001684` | `0.668` |

The bound with the oracle differs from the bound without it by `−ln n − O(0.1)` (the cyclic union; the deeper dip
costs almost nothing), and approaches `R^max` from below like `0.7·ln n/n`.  At `n = 3200`, `(0.3, 1, 0.3E)`: every algorithm
with the oracle needs `(1−2δ)·e^{33.7} ≈ 4·10^{14}` evaluations at the two-component instance.  `c_{k,r}` is the cone
density `c₀(k/n)` to all digits shown (Lemma 2), not `p_{γ*} = 0.317` resp. `0.163`.  (Rows for four further parameter
sets, `(0.1, 2, 0.05E)`, `(0.2, 1, 0.5E)`, `(0.5, 1, 0.3E)`, `(0.05, 3, 0.2E)`, as far as computed: `out/t05_run.log`; e.g.
`(0.1, 2, 0.05E)`, `R^max = 0.043316`: `0.037550`, `0.040221`, `0.041652` at `n = 800, 1600, 3200`.)

### 3.5 The tilt inequality and its consequences (`t09_tilt_check.py`, `t12_tilt_gammastar.py`, `t13_threshold.py`)

Proposition C(a) by enumeration (`n = 10 … 14`, five exactly matched alternatives, `λ ∈ [−3, 3]`): `min(LHS − RHS) = 0`
(at `λ = 0`), never negative beyond `2·10⁻¹⁶`; for an **unmatched** alternative the inequality fails
(`−4·10⁻³ … −6·10⁻²`), as it must.  The hardest *additive* instance with the oracle: `U_{γ*}(e)/R^max(e) = 0.984, 0.961, 0.893`
at `(0.3, 1)`, `e/E = 0, 0.3, 0.6`; `0.867, 0.654, 0.182` at `(0.1, 2)`; `0.799, 0.454, 0` at `(0.05, 3)`; `1` at `p = ½`.
Thresholds of the zero residual: `min_λ[E_0(θ−λ) + c_0(λ)]/E_0 = 1` (`p = ½`), `0.990` (`0.4, 1`), `0.963` (`0.3, 1`), `0.943` (`0.25, 1`),
`0.864` (`0.1, 1`), `0.631` (`0.1, 2`), `0.368` (`0.05, 3`).

### 3.6 The zero residual with the oracle (`prof.py`, `t04_instance.py`, `t10`, `t11`, `t14`, `t07b_annular_fast.py`)

Single-letter values: table in §2.5 (36 rows in `out/t04_instance.txt`).  Checks of the profile formula: `f` at the
plain-dip profile `≥ Rcc`, with equality at the optimal centre type; the unconstrained supremum over two-label
profiles equals `R_γ` to eight digits.  **The supremum over two-label profiles of type `p` with unrestricted
label-conditional laws equals the tilt bound to six digits** — `0.012941` (`(0.25, 1)`, `e = 0.02`), `0.016345`
(`(0.1, 2)`, `0.2E_0`), `0.024371` (`(0.3, 1)`, `e = 0`) — and is attained at the cone laws of the tilted reference
(`(0.0956, 0.4386)` in the first case, the first below the window `[0.1092, 0.4754]`); restricted to the window:
`0.012630`, `0.015443`, `0.024141`.  **Where the excess mass sits** (exact sums, `n = 400`, `p = 0.25`, `u = 1`, `k = 180`): the
dip around the shell `(j₁, j₀) = (76, 10)` — label-0 law `0.0455`, outside the window, shell type `0.2150` — has excess
density `0.2439`; around `(76, 24)` — label-0 law `0.1091`, at the end of the window, shell type `0.2500` — it has `0.2524`.
Certified finite-`n` bounds at the zero residual with the oracle (two shells with the same centre, excess
densities bracketing `p`, exact matching by the linear equation):

| `(p, u, e)` | `n` | shells: `ln LB/n` | `ln LB` | centre type, shells `(j₁, j₀)`, excess densities | plain dips of the forced centre type |
|---|---|---|---|---|---|
| `(0.1, 2, 0.2E_0)`; `V = 0.015441`, `U = 0.016345`, `R_0 = 0.026849` | `200` | `−0.006703` | `−1.34` | `k = 76`; `(18, 0)`, `(19, 0)`; `0.09678`, `0.10148` | no admissible pair (single-letter value `0`) |
| | `400` | `+0.002842` | `+1.14` | `k = 144`; `(36, 2)`, `(37, 2)`; `0.09891`, `0.10131` | no admissible pair |
| | `800` | `+0.008534` | `+6.83` | `k = 297`; `(72, 5)`, `(73, 5)`; `0.09939`, `0.10062` | — |
| | `1600` | `+0.011240` | `+17.98` | `k = 546`; `(143, 14)`, `(144, 14)`; `0.09991`, `0.10052` | — |

So at `n = 1600`, `ε = 0.0404·n`, every algorithm with the oracle needs `(1−2δ)·e^{17.98} ≈ 6·10⁷` evaluations **at the
zero residual**, where dips of the forced centre type certify nothing; `(V − ln LB/n)·n/ln n = 0.84, 0.83, 0.91` (the
scan over `(k, j₀)` is coarse — five centre types, six `j₀` — so these are lower bounds on what shells give).
Rows `n = 200, 400` of the first, slow script `t07_zero_residual_annular.py` (kept as
`out/t07_zero_residual_annular_partial.txt`) agree with `t07b_annular_fast.py`, which computes on a bounding box of the
supports (checked not to touch its boundary).  Further rows (`n = 3200`; `(0.3, 1)`, `(0.25, 1)`) were still running
when the report was closed: `out/t07b_run.log`.

### 3.7 Exact two-body matching (`t08_k2_exact.py`; `n = 11, 13`, `G = AGL(1, n)`, exhaustive)

`n = 13`, `p = 0.3`, `u = 1`, `γ = γ*`, centre types `4` and `9`, depth `1`: single types have `c₂ − c₁² = −0.0037, −0.0057`
(below the parabola); the mixed excess has `h = +0.00386`, `g = +0.0251`; base `a·π_γⁿ + (1−a)π_{γ₂}ⁿ` with `a = 0.8595`,
`p₂ = 0.4982`: **all 13 one-body marginals equal to `2.6·10⁻¹⁵` and all 78 pair marginals to `4·10⁻¹⁶`**, while the
three-body marginals differ by `3.8·10⁻⁴`.  Second case (`p = 0.1`, `u = 2`, types `4, 10`): `6.7·10⁻¹⁵`, `3.2·10⁻¹⁶`, three-body
`2.2·10⁻⁴`.  Two recorded failures show the conditions: `n = 11`, types `3, 8`: `p₂ = 0.602` outside the window;
`n = 13`, types `5, 9`, `θ = 0.4`: `h = −8·10⁻⁵ < 0` (types too close).

### 3.8 The non-adaptive pair (`t06_nonadaptive.py`)

(A) Enumeration, `n = 10 … 14`, six cases: the type-wise truncated cone is in the class (largest `|ln ratio| = u` —
the machine-checked statement of the theory division, re-checked by brute force); the compensated pair is in the
class with all one-body marginals equal to `1.6·10⁻¹⁵`; without compensation cone and truncated cone differ by
`10⁻³ … 2·10⁻²` in the marginals; `b = 0.05 … 15`.
(B) Exact sums, `(0.3, 1, ε₁ = 0.25E)`, `θ_na = 0.024324`: with the oracle `−ln(nq)/n = 0.010781, 0.016693, 0.019706, 0.021837,
0.023026` at `n = 100, 200, 400, 800, 1600` (deficit `≈ 0.29·ln n/n`); without the oracle the same pairs give
`0.0569, 0.0432, 0.0349, 0.0303, 0.0277` (from above).  `b/A_t = 0.07 … 0.09`: the compensator carries a tenth of the
mass of the *truncated* cone.  (Three further parameter sets were queued and not run; the enumeration part (A) and
this table are in `out/t06_run.log`.)

### 3.9 Ingredients of Theorem τ (`t15_tolerance_check.py`; `n = 12`, exhaustive)

Base `(τ/4)π_γⁿ + (1 − τ/4)Bern(c₀)ⁿ`, alternative = base + average of `N` dips at i.i.d. `Bern(m*)` centres, `e^r = 1 + 8/τ`:
both in the class; separation `ln 3`; largest deviation of all marginals of orders `1, 2, 3` between alternative
and base: `0.019, 0.018, 0.016` (`p = 0.3`, `u = 1`, `τ = 0.1`, `N = 400`), `0.014, 0.020, 0.020` (`p = 0.1`, `u = 2`, `τ = 0.1`, `N = 400`),
`0.0070, 0.0070, 0.0056` (`p = 0.3`, `u = 1`, `τ = 0.03`, `N = 2000`) — within `τ`, with lists far shorter than the theorem's `N`.

### How to re-run

`cd experiments/science/ws_F && export OMP_NUM_THREADS=1 && mkdir -p out`; then `python3 t01_single_letter.py` (1 min),
`t02_fixed_point.py` (20 min), `t03_enum_adaptive.py` (5 min), `t04_instance.py` (15 min), `t05_typesums_adaptive.py`
(60 min, 2 GB at `n = 3200`), `t06_nonadaptive.py` (60 min), `t07b_annular_fast.py` (30 min),
`t08_k2_exact.py` (1 min), `t09_tilt_check.py` (1 min), `t10_theory_e.py` (6 min), `t11_unrestricted_profiles.py` (10 min),
`t12_tilt_gammastar.py` (3 min), `t13_threshold.py` (seconds), `t14_theory_numbers.py` (2 min), `t15_tolerance_check.py`
(1 min), `t16_exact_rational.py` (1 min).  Each writes `out/<name>.txt` when it ends (running logs
`out/*_run.log`).  `t07_zero_residual_annular.py` is the first, slow version of `t07b`; it was stopped after `n = 400`,
and its header records a bug that would have affected it from `n = 800` on (the bisection range of the lift was too
short for annular dips); its two rows agree with `t07b`.  The times are with three jobs sharing the machine.

---

## 4. Prior art, with a search log

*Searches (2026-11-25, web search tool; four queries, three pages fetched).*
1. "Kuperberg Lovett Peled Probabilistic existence of regular combinatorial structures t-designs number of blocks"
   → arXiv:1302.4295 (GAFA 27 (2017) 919–972).  **[full text of the statement]** — the arXiv PDF was converted with
   `pdftotext` and the introduction read: *Theorem 1.3 (Existence of t-designs). For all integers `v ≥ 1`, `1 ≤ t ≤ v` and
   `t ≤ k ≤ v` there exists a `t`-`(v, k, λ)` design whose size is at most `(cv/t)^{ct}` for some universal constant `c > 0`.*
   (The displayed formula is garbled in the text layer; I read it as `(cv/t)^{ct}`, consistent with the lower bound
   `(v/t)^{⌊t/2⌋}` quoted two lines above it.)  The theorem on `t`-wise permutations: **[abstract]** only.
2. "Nakiboğlu Augustin capacity and center fixed point" → arXiv:1803.07937.  **[machine reading of the first
   100 000 characters of the ar5iv HTML: introduction and §2]**: the order-`α` tilted measure
   `w_α^q ∝ w^α q^{1−α}` (Definition 2); the Augustin mean `q_{α,p}` is the unique fixed point of the operator
   `T_{α,p}` (stated in the introduction, attributed for `α ∈ (0,1]` to Augustin's Lemma 34.2; the paper's Lemma 13);
   **for `α = 1` the Augustin mean is the output distribution `Σ_x p(x)W(x)`**.  This is exactly the distinction of
   Proposition S: the coordinator's identity is Augustin's fixed point (order `t`), the oracle needs the order-one
   statement.  The companion arXiv:1701.06610 (sphere packing with constant-composition codes via Augustin's
   method): **[search snippet]**.
3. "lower bound query complexity estimating partition function marginal oracle" → nothing that matches the
   two-oracle question (evaluations plus exact marginals of the Gibbs measure, over a Lipschitz class).  Found
   **[search snippets]**: `Ω(1/ε²)` classical / `Ω(1/ε)` quantum lower bounds for partition functions with
   Gibbs-sampling access (arXiv:2404.02414); normalising constants of log-concave densities (arXiv:2210.06539);
   partition ratios with black-box access to a family of Gibbs distributions (arXiv:2007.10824).  Different models
   (sampling access to the measure, no adversarial class).  "Not found" is not a claim of novelty.
4. The search for the Augustin fixed point in the constant-composition sphere-packing literature returned the two
   Nakiboğlu papers again; no statement comparing the Rényi centre with the channel output law at the optimal
   input was found at this depth (it is elementary; see §2.4).
*From memory, not checked:* `AGL(1, q)` is sharply 2-transitive and `PGL(2, q)` sharply 3-transitive (Zassenhaus);
Hoeffding's inequality; the mode of `Bin(n, k/n)` has probability at least `1/(n+1)`; Jerrum–Valiant–Vazirani.
*Internal prior art.*  Addendum A1 of `INFERENCE_LIMITS_ADDENDA.md` conjectured the opposite of Corollary A ("the
exponent with the oracle should be the hinted exponent restricted to that type — possibly strictly smaller than
`R^max`"): refuted for the class, and at an instance the restriction to centre *types* is the wrong formula (§2.5).
The theory division's §11.29 (`dcdfea6`) is treated in §8.

---

## 5. What I did not settle

1. **The exact instance-wise exponent with the oracle** at an additive instance (in particular the zero residual):
   it lies in `[V, U]` (§2.5), a gap of `1–8 %` in most rows, larger near the threshold (`0.001226` against `0.001648`).
   Conjecture Z says the lower end.  Missing: an isoperimetric *upper* bound for sets whose excess mass has a
   prescribed type, with the window built in.  I also did not test profiles with three labels.
2. **The finite-`n` certificates with shells** (§3.6) are for one parameter set and `n ≤ 1600`, with a coarse scan;
   the single-letter value `V` rests on a proof sketch (Proposition D(b)) plus those sums.  Rows for `n = 3200` and
   for two more parameter sets were still running when the report was closed (`out/t07b_run.log`) and are not
   quoted.  `t05` and `t06` were stopped by me when the report was closed, to free the shared machine, before
   their last rows (`t05`: three of six parameter sets complete to `n = 3200`, the fourth to `n = 800`; `t06`: the first
   of four parameter sets, to `n = 1600`): what was computed is in `out/t05_run.log`, `out/t06_run.log`; the files
   `out/t05_typesums_adaptive.txt`, `out/t06_nonadaptive.txt` therefore do not exist.
3. **`U` at bounded accuracy** (`e = 0`) needs the isoperimetric statement for an additive reference at negative `e`,
   which I did not read; at `e = 0` only the trivial `λ = 0` is covered by the black box as stated.
4. **`k = 2`** is a proposition with a proof sketch for the asymptotics (Proposition E(iv)): the uniform estimate of
   the excess moments, and the loss in the Markov form, are not written out.  `k ≥ 3`: conjecture.
5. **Upper bounds at bounded accuracy with a field** are not known even without an oracle (theory report §11.20,
   remark (4)); Corollaries A, B give lower bounds `h` and `a` there.
6. Theorem τ was not checked numerically as a whole (its ingredients were); the correlation-function form and the
   non-adaptive form are sketches.
7. Nothing here is machine-checked.  Lemma 3 and Theorem A are finite inequalities and would be easy targets
   (Theorem A needs only `expected_queries_ge_packing`, convexity of the weight cone and Lemma 2).
8. Larger alphabets, several site types, known parts with interactions: not touched.  The compensation lemma uses
   only that the class is a convex cone containing, for every target marginal in the window, a member with that
   marginal; what replaces "cyclic shift" and "additive instance" for a chain is open.

## 6. The three most promising next steps

1. **A type-resolved isoperimetric theorem** (the theorem behind Conjecture Z): for an additive reference, the least
   measure of a set whose excess mass `e^{ne}` sits at a prescribed type.  It would turn the bracket of §2.5 into the
   exact instance-wise value of a per-site measurement, and its `k`-body analogue would say how much each order of
   averaged data is worth *at a believed model* — the informative statement, since for the class the answer is
   "nothing" at every order tested.
2. **One theorem for all `k` with a field**: designs in the Johnson scheme (KLP) plus the moment problem of
   Proposition E(v); together with Theorem τ this would complete "oracle invariance of the complexity diagram"
   beyond the uniform cube.
3. **Formalise Lemma 3 and Theorem A** in Lean on top of `QueryLowerBound.lean` and workstream L1's oracle-indexed
   algorithms (the statement is short and every step is finite), so that the every-`n` bound with a field stands
   next to Theorems 4, 4′.

## 7. Requests

**To the theory division** (can be sent as they are).
T1. *Review Lemma 3 and Theorem A of `docs/science/workstreams/SF_REPORT.md`*: they prove conjecture (f) of
    Proposition 11.109 (`dcdfea6`) for every `n` and every `ε > 0`, with the instance `−ln(w̃_{γ*} + b·w̃_{∓u})` instead of the
    flat histogram with a well.  Is there an error?  If not, (f) can be relabelled, and Theorem B does the same for
    `θ_na` (not treated in §11.29).
T2. *Proposition 11.109(e)*: the quantity your script `oracle_zero_types.py` maximises admits block laws outside the
    window `[p₋, p₊]` (`x0` down to `0.005`; your reported maximiser at type `0.292` has `x1 = 0.497 > p₊ = 0.4754`); for such
    profiles the excess mass of the dip does not sit on the profile class (our exact sums: shell type `0.2150`,
    excess type `0.2439` at `n = 400`).  We reproduce your six numbers with block laws unrestricted (table in §8.3);
    at type `p` the supremum is `0.012941` and equals `min_λ R_0(e − c(λ); θ − λ)`, which we prove to be an *upper* bound
    for the exponent with the oracle (tilt inequality + your Theorem 11.59(a) at the field `θ − λ`); restricted to the
    window it is `0.012630`.  Please check both numbers, and say whether your Theorem 11.78 gives the type-resolved
    statement that would decide between them.
T3. *The hinted theorem at negative accuracy*: is the isoperimetric statement behind Theorem 11.59(a) proved for
    all real `e` for an additive reference (as Theorem 11.63 is for the flat histogram)?  We need it for `U` at
    bounded accuracy.
**To the engineering division.**
E1. *Exact sums for annular dips at the zero residual.*  Motivation: certified finite-`n` lower bounds with the
    one-body oracle at `ψ = 0` (Proposition D(b)).  Formulation: for `n ∈ {800, 1600, 3200, 6400}`, `(p, u) ∈ {(0.1, 2),
    (0.3, 1), (0.25, 1)}`, `ε = e·n` with `e ∈ {0.2, 0.5}·E_0`: maximise over `(k, j₀)` and adjacent `j₁` the bound
    `−ln n − ln max_κ Σ_{j ∈ D_A∪D_B} P_s(j | κ)` of `t07b_annular_fast.py` (class `Box`, function `pair`), with the common
    lift chosen minimal for separation `> ε`.  Inputs: the script.  Expected output: `ln LB/n` approaching `V` of §2.5
    from below like `c·ln n/n` (`c ≈ 0.83` in our rows).  Validation: reproduce our rows `n = 400, 800` (`+0.002842`,
    `+0.008534`) for `(0.1, 2, 0.2E_0)`; exact rational arithmetic at `n = 200`; a wider scan of `(k, j₀, j₁)` than ours (we
    scan five centre types and six `j₀`).  Stopping: `n = 6400` or 8 GB.  Resources: the bounding box of the supports
    has `O(n²)` cells with a small constant; a few minutes per `n` up to `1600`.

---

## 8. Against theory report §11.29 (Proposition 11.109, commit `dcdfea6`; THY-RES-0006 §3; `DEAD_ENDS` D54 item 3)

*Provenance.*  The theory division published its answer to the same question while this workstream was running.
Everything in §§2–3 above except the comparison rows marked "theirs" was derived and computed **before** I opened
THY-RES-0006, §11.29, D54 or the scripts `oracle_field_scan.py`, `oracle_zero_types.py` (`NOTES.md` records the order
with clock readings: first analysis H1–H5 before 20:23; compensated construction verified by enumeration by 20:45;
zero-residual bracket, non-adaptive pair and `k = 2` by 21:01; tilt check 21:02; their material read from 21:02 on).
Before that I had read only THY-RES-0005 §2 (their two-sentence
expectation "at the zero residual, restricted to that type; not for the class", and the parameter-counting
remark, which I attribute to them in Lemma 3, remark (3)).  All statements of theirs below are quoted from
`git show dcdfea6:docs/THEORY_REPORT.md`, lines 7080–7177, and are tagged **[T, `dcdfea6`]**.

### 8.1 Their (a)–(d): agreement, and an independent derivation of (c)

| theirs **[T, `dcdfea6`]** | mine | verdict |
|---|---|---|
| (a) every one-body marginal lies in `[p₋, p₊]`, `logit p_± = logit p ± u`; all sites at one end only for the field `∓u\|x\| + const` | Lemma 0 (same proof, found independently; plus: an arbitrary pattern of ends forces the cone `u·d(·,s) + const`) | **agree** |
| (b) an instance invariant under a transitive group shows the oracle one number, its mean type | Lemma 3(i), first half | **agree** |
| (c) `κ̄(ψ₁) − κ̄(ψ₀) = Φ/(1+Φ)·[type(ν) − κ̄(ψ₀)]` for a symmetric null and its deepest dip on a cyclically invariant set | Lemma 3(i): `μ_{w+Δ}` is the mixture of `μ_w` and `πΔ/A_Δ` with weights `A_w : A_Δ` | **agree; re-derived** |
| (d) if the criterion holds, `(1−2δ)/maxdens(D′)` evaluations at `ψ₀`; a factor `n` for the cyclic union | Lemma 1(a) + the count in Theorem A | **agree** |

*Re-derivation of (c).*  With `w_i = e^{−ψ_i}`, `Δ := w₁ − w₀`, `Φ = A(Δ)/A(w₀)`: `πw₁ = πw₀ + πΔ`, so
`μ_{ψ₁} = (μ_{ψ₀} + Φν)/(1 + Φ)` with `ν = πΔ/A(Δ)`, and for the linear functional "mean type":
`κ̄(ψ₁) = (κ̄(ψ₀) + Φ·type(ν))/(1 + Φ)`.  ∎  Checked on the whole cube in every run of `t03`, `t06`, `t09` (the matched pairs
have equal marginals to `10⁻¹³`; the unmatched controls differ by exactly `Φ/(1+Φ)·[type(ν) − κ̄]`).
*One remark on (c)/(d).*  Nothing in them uses that `ψ₁` is the **deepest** dip on `D′`: the identity and the bound
hold for every `ψ₁ ≤ ψ₀` that agrees with `ψ₀` outside `D′`.  This matters, because the hypothesis is what produces
their "trap": for the deepest dip the excess measure depends on the null, and along the additive instances it
degenerates at both ends.  My alternatives are *not* deepest dips of the compensated null — they are the null
plus a fixed excess — and that decoupling is what makes the matching equation linear (Lemma 3, remark (2)).
Likewise, for the cyclic union I use the **average** of the `n` shifted dips (a class member by convexity), whose
excess measure is exactly the average of the shifted excesses, rather than the deepest dip on the union, whose
excess type is not that of a single dip when the shifted sets overlap.

### 8.2 Their conjecture (f) — "for the class the oracle does not help": **proved, by a different instance, in a stronger form**

**[T, `dcdfea6`]** (f) **[C]**: "Take the flat-histogram instance with a logarithmic well at the type `t₀` of the
excess mass of its hardest dips … its Gibbs measure sits at `t₀`, its dips are as sensitive as those of `H` up to a
polynomial factor, and the criterion of (c) can be met.  So `R^max(ε₁)` is unchanged by a one-body oracle at every
accuracy `ε ≫ ln n`."  Missing, in their words: "a concentration statement: the excess mass of the sets of Theorem
11.78(a) sits on the classes of the optimal profile, i.e. the optimal profile is unique.  We have not proved that."

*Verdict: confirmed and proved* — Theorem A and Corollary A — and sharpened in four ways:
(1) **every `n`**, with an explicit loss `C_m·n(n+1)`; (2) **every accuracy `ε > 0`**, bounded ones included (their well
costs a polynomial factor in sensitivity, whence `ε ≫ ln n`; my compensator costs the factor `1 + b = O(1)`);
(3) **no concentration or uniqueness statement is needed**: the alternatives are explicit cone dips of one exact
centre type, whose excess type is `c₀(k/n)` up to `1/(e^r − 1)` by a two-line computation (Lemma 2), and the null is
adjusted by one explicit linear equation; (4) the **non-adaptive** exponent `θ_na` is covered as well (Theorem B;
not treated in §11.29).
*Is their mechanism the "self-consistency" of my brief?*  No, and neither is a proof as written.
- The brief (coordinator's sketch): the hardest **additive** instance `γ*` is self-consistent *automatically*, by
  Augustin's fixed point `Q* = Σ_φ M*V_φ`.  This is false: the excess of the hardest dips has the type of the cone
  law `M*W`, not of `Σ_φ M*V_φ` (which is the type of the rim), and `M*W ≠ Q*` for `p ≠ ½` (§2.4, §3.2).  At `γ*` the
  oracle does bind, and its instance exponent drops (`U_{γ*}/R^max = 0.65` at `(0.1, 2, 0.3E)`).
- The theory division: the adversary **builds** an instance whose mean type equals the excess type — the flat
  histogram plus a well.  That is the right idea, and the same in kind as Lemma 3 (move the mean type of the
  null); the differences are that their modification is a pointwise maximum of weights with the dip taken as
  the deepest dip of the modified null (so the excess moves with the tuning parameter and one needs a
  bracketing plus the unproved concentration), while mine is a **sum** of weights with the excess held fixed.
  Their sentence "the class contains an instance whose own averages already equal those of its hardest
  perturbations" is true — `−ln(w̃_{γ*} + b·w̃_{∓u})` is one — but by construction, not as a property of an extremal
  instance.  I did not try to complete their argument for the well; it is no longer needed.
*Their trap* (D54 item 3: along `γ ∈ [−u, u]` the mismatch of the deepest dip is zero at both ends and need not
change sign) is real and I confirm the mechanism (at `γ = ±u` the game function vanishes: `F(±u, t) = 0`).  It does
not touch Lemma 3: there the parameter is the weight `b` of an added extreme additive instance, the mismatch
`dens(null) − dens(excess)` runs monotonically from `p_γ − c_Δ` (at `b = 0`) to `p_± − c_Δ` (as `b → ∞`), of opposite signs
whenever `c_Δ` is in the open window, and the relative excess `E/(1+b)` stays bounded below because the root is at a
finite `b` (`0.11 … 0.62` in the examples).  *Lesson in their words, completed:* an extremal instance is useless as
the end of a homotopy of perturbations, but perfectly useful as an *admixture*.

### 8.3 Their conjecture (e) — "at a given instance the oracle helps": **direction proved; their formula over-counts; value bracketed**

**[T, `dcdfea6`]** (e) **[C]**: "At the zero residual the dips that survive are those whose excess mass has the type
`p` — for a dip around a centre of type `m` with its Gibbs shell inside, `m(1 − η₁) + (1 − m)η₀ = p` … — and the exponent
with the oracle is `ρ_e(p) := sup{r_μ(e) : μ̄ = p}` instead of `R_0(e) = sup_κ ρ_e(κ)` … (**[N]**, a coarse search over
two-block profiles at `p = ¼`, `u = 1`, `e = 0.02`: `ρ_e(κ)` is unimodal in the type, with `0.0134` at `κ ≈ 0.29` and `0.0129` at
`κ = p` — … about `3.5 %` …)"; and: "(e) needs an algorithm that uses the oracle, which we do not have."

1. **Direction: confirmed and proved** (given their own hinted theorem at shifted fields): Proposition C.  The
   algorithm they lack exists and is trivial — reject the hint if the oracle's answers differ from the hinted
   instance's, otherwise spot-check as without oracle; what was missing is the analysis, which is the tilt
   inequality.  The oracle strictly lowers the exponent of the zero residual for `p ≠ ½` in every case computed.
2. **Their numbers** (I did not run their code; I compared my profile formula `f` of §2.5 with their output file
   `out_oracle_zero_types.txt` at `dcdfea6`; `t10_theory_e.py`, `t14_theory_numbers.py`).  At `p = ¼`, `u = 1`, `e = 0.02`, for
   two-block profiles of type `κ`:

   | type `κ` | `0.184` | `0.238` | `0.250 = p` | `0.292` | `0.347` | `0.401` |
   |---|---|---|---|---|---|---|
   | theirs **[T, `dcdfea6`]** | `0.00485` | `0.01210` | `0.01294` | `0.01340` | `0.00942` | `0.00338` |
   | mine, block laws unrestricted | `0.00491` | `0.01210` | `0.01294` | `0.01341` | `0.00938` | `0.00338` |
   | mine, block laws in the window `[0.1092, 0.4754]` | `0.00217` | `0.01142` | `0.01263` | `0.01302` | `0.00482` | `0` |

   So their `r_μ` is my `f` with the block laws **unrestricted** (their script lets `x0` range over `(0.005, x1)`), and
   their reported maximiser at type `0.292`, `(m, x1, x0) = (0.46, 0.497, 0.118)`, has `x1 = 0.497 > p₊ = 0.4754`.  The exact
   `R_0(e)` is **`0.013669`** (two independent formulas), attained by cones of centre type `0.4555` whose excess type
   is `0.2760`; "`0.0134` at `κ ≈ 0.29`" is the value of their grid of seven types, not the maximum.  Their `0.01294` at
   `κ = p` equals my tilt bound `min_λ R_0(e − c(λ); θ − λ) = 0.012941` — the unrestricted supremum and the tilt bound
   coincide to six digits in the three cases tried, as Lagrangian duality suggests, and the maximiser is the pair
   of cone laws of the *tilted* reference, `(0.0956, 0.4386)`.  The decrease is `5.3 %` (or `7.6 %`, next item), not `3.5 %`.
3. **The formula over-counts.**  The maximising profile at type `p` has a block law (`0.0956`) *outside* the window
   `[p₋, p₊] = [0.1092, 0.4754]`.  For such a profile the excess mass of the dip does **not** sit on the profile class
   — it sits on the nearest shell inside the window (exact sums, §3.6: shell type `0.2150`, excess type `0.2439`) —
   so "`μ̄ = p`" is not "the excess mass has type `p`", and that dip is visible to the oracle.  The concentration
   statement they flag as unproved is false for these profiles.  Restricting to block laws in the window (shells
   that are Gibbs shells of soft cones) gives **`0.012630`** at their test point (two-label profiles; `ρ_e(κ)` so
   restricted is unimodal with maximum `0.01366` near `κ = 0.276`, `t10`); away from the centre the restriction
   matters much more (`0.00482` against `0.00942` at `κ = 0.347`; `0` against `0.00338` at `0.401`).
4. **Status of the value.**  `0.012630 ≤ R_0^{orc}(0.02) ≤ 0.012941`: the lower end from explicitly matched
   alternatives (Proposition D; certified at finite `n` in §3.6 for another parameter set), the upper end proved
   by the tilt inequality.  Their `ρ_e(p)` is therefore an **upper bound** for the true exponent, proved here, and
   — as far as constructions go — not attained.  Which end is the truth is open (Conjecture Z says the lower).
5. **"Restricted to that type — yes, at the zero residual"** (THY-RES-0006 §3) must be read as "restricted to
   alternatives whose excess mass has type `p`".  It must *not* be read as "restricted to cone-like dips whose
   centre type solves `m(1−η₁) + (1−m)η₀ = p`" (the condition of our addendum A1, which they cite as "the division's
   condition"): those give `0.005704` at their test point and `0` at `(0.1, 2, 0.2E_0)`, where shells give `0.0154`.

### 8.4 Other points of §11.29

* The paragraph "*For `k`-body marginals with a field* … `k` matching conditions … the first `k` factorial moments of the
  type under the excess measure and under the null; open" **[T, `dcdfea6`]** agrees with my reduction (Proposition
  E(i)), found independently.  Two additions: the citation they give from memory can be made precise — KLP
  Theorem 1.3 gives `t`-designs of size `(cv/t)^{ct}` for all `v, k, t` (read), which is what one needs for dips of a
  fixed centre type (a family of blocks, not of permutations); and counting parameters is not enough for `k = 2`:
  with nulls that are mixtures of additive instances a single family of dips can **never** be matched (its
  excess lies below the parabola `c₂ = c₁²`), and two centre types `≳ √n` apart are needed (Proposition E(ii)–(iv),
  verified exactly at `n = 13`).
* "At this size the symmetrised sets fill whole type classes, so the illustration is about the oracle's answers,
  not about exponents" **[T, `dcdfea6`]**: the same holds for my enumerations (`n ≤ 16`); my exponents come from exact
  type-class sums up to `n = 3200`.
* Nothing in (a)–(d) is wrong.  What says more than is shown: the bold sentence of (f) reads as a result while it
  is labelled **[C]** (now a theorem, so harmless); in (e) the identification of "excess mass of type `p`" with
  "profile of type `p`" (item 3 above), and the two coarse numbers (item 2).  The closing paragraph ("at an
  instance that the user believes in … the data do exclude most dips") is supported by Proposition C and the
  tables of §2.5; "most" is quantitatively right for strong fields (at least `21–100 %` of the exponent at `(0.1, 2)`)
  and an overstatement for weak ones (`2–17 %` at `(0.3, 1)`, the larger values near the threshold).
* Not treated by them and treated here: the non-adaptive exponent (Theorem B), tolerances (Theorem τ), an exact
  `k = 2` construction, the hardest additive instance with the oracle, thresholds.  Not treated here and treated
  by them: the brute-force scan along the additive instances on `Q_10` (I did not re-run it).
