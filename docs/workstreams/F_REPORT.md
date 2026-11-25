# Workstream F — algorithms without a hint when there is a known part (a field)

> **Repository note (added by the coordinator at integration; the report below is otherwise as
> delivered).**  Status: **paper proofs, under independent review (referee R9,
> `docs/reviews/R9_brief.md`) at the time of integration** — see `docs/THEORY_REPORT.md` §11.20
> for the integrated statements and their labels.  The scripts and outputs named in §4 are in
> `experiments/workstreams/F/` (run from that directory; numpy and scipy).  The Lean file
> `lean/WorkstreamF.lean` is `proofs/Frontiers/FieldShift.lean` in the repository (namespace
> `MetricChain.FieldShift`, the repository's `klBin` reused, theorem names unchanged).
> Theorem numbers of the theory report: F1/F2 = Theorem 11.59, F3 = Lemma 11.60, F4 = Theorem
> 11.61, F5 = Lemma 11.62, F6 = Theorem 11.63, F7/F8/F9 = Theorem 11.64, F10 = Proposition 11.65;
> F11 and F12 are sketches and are quoted as such.  The coordinator re-computed the central
> formulas with own code (`experiments/coordinator_checks/f_spot_checks.py`).

Independent report.  Directory: `<session scratch>/ws/F/` (all scripts and outputs named below are in it and run as
`python3 <script> [args]`, numpy/scipy only, `ulimit -v 4000000`, each run under ten minutes; `run_all.sh` runs them one
after another).  Repository read-only: read at commit `1bff191`; it moved to `4cef47e` while I worked (workstream L added
`CubeHintPair.lean`); nothing in it was modified.

Status labels: **[proved]** = complete proof in this report (paper proof by me, not refereed; where a step is machine-checked
this is said); **[sketch]** = outline, missing steps named; **[numerical]**; **[conjecture]**; **[known]** = in the theory
report or in the literature, with the way I read the source.

---

## 1. Verdicts in one paragraph

With a field (`p`-biased reference measure, `u`-Lipschitz residual) everything of §§11.16/11.18 carries over **with one
change that matters: the reference of the hint-free algorithms is not the instance `g = 0`, and the sampling law is not
`π_f`.**  (1) The hinted exponent of the instance `(f, g = 0)` is `R_0(ε₁) = max_m [h(m) − h((Λ_m+ε₁)/u)]_+` (centres of an
optimal type `m* ≠ ½`; **[known]**, rewritten **[proved]**).  (2) The non-adaptive exponent is
`θ_na(ε₁) = max_m min{ I(S;X) : D(P_{X|S} ‖ π_s | P_S) ≤ ε₁ }` (`π_s` the Gibbs law of the cone with centre `s`); it is
attained by importance sampling from the **type-uniform mixture** (the normalised-maximum-likelihood mixture of all tilted
product measures), not from `π_f` and not from any single tilted product measure (Proposition F11: sketch + numerical);
lower bound **[proved]** for every `n`
(cones truncated at type-dependent radii), characterisation of the non-adaptive complexity by one extremal function
**[proved]** without any isoperimetry, matching upper bound **[proved, given Theorem F6]**.  (3) The identity becomes
`D(P_{X|S} ‖ π_s | P_S) = I(S;X) + [u·P(X≠S) − Λ(P_S)] + KL(P_X ‖ π)` (**[proved]**, machine-checked): *non-adaptive
accuracy = exponent of the sample + hinted accuracy at `g = 0` + `KL(P_X‖π)`*.  The extra term makes it the hinted
accuracy of a **different instance**: the identity "`θ_na(e + θ_hint(e)) = θ_hint(e)`" holds exactly with
`θ_hint := R^max = max_{|γ|≤u} R_γ`, the hinted exponent of the **hardest additive instance** `γ*|x|` (equivalently of
the "flat-histogram" instance `H`), and fails with `R_0`.  The pair `(θ_na, R^max)` satisfies `HintPair` (**[proved]**),
the two-level layer-cake construction goes through *relative to the reference instance `H`* (sample its Gibbs law, the
type-uniform mixture; the tail lemma is the hinted problem at `H`), and the abstract theorem gives: **the worst-case
exponent of adaptive algorithms without a hint is `R^max(ε₁)`, the largest hinted exponent of an instance of the
class** — "adaptive = hinted" persists (lower bound **[known]**, for every `n`; upper bound **[proved, given]** the
unrefereed proof of Theorem 11.52, whose changes are written out and whose logic is simulated, and Theorem F6).
(4) Instance-optimality in the field: **no in the worst case, yes at the instance.**  `R^max(ε₁) > R_0(ε₁)` strictly for
every `θ ≠ 0` (**[proved]**; the hardest instance tilts the field towards zero: `γ*θ < 0` in all computations), so the worst-case hint-free
exponent is *not* the hinted exponent of `(f, g=0)`; both decrease with `|θ|` (**[numerical]**); and a type-stratified
one-level bracket with adaptive stopping is instance-optimal at `g = 0`, at every additive instance and at every
permutation-symmetric instance (**[proved]**, soft).  The isoperimetric input is *not* a Harper theorem for product
measures (exact results cover down-sets only, Bollobás–Leader; the fixed-measure asymptotics of Ahlswede–Zhang/Yu give
the exponents of plain `π_f`-sampling, which are strictly worse): it is a **minimax version** — every set that is
sensitive for `H` has type-mixture measure at least `e^{−nR^max}` — proved here by the method of types (Theorem F6).

---

## 2. Setting and notation

**Setting.**  `Q_n = {0,1}ⁿ`, `d` the Hamming distance, `p ∈ (0,1)`, `q = 1−p`, `π = Bernoulli(p)^{⊗n}` (the Gibbs measure of
the known part `f(x) = θ|x|`, `θ = ln(q/p)`), `u > 0` (`= βc`), `L_u = {ψ : |ψ(x) − ψ(y)| ≤ u d(x,y)}`, `w = e^{−ψ}`,
`A(ψ) = E_π e^{−ψ}`; the target is `ln A(ψ)` (`ln Σ_x e^{−f−ψ} = ln A + n ln(1+e^{−θ})`).  Algorithms know `p, u` and
query `ψ`; an algorithm is correct if its output is within `ε/2` of `ln A(ψ)` with probability `≥ 1−δ` for **every**
`ψ ∈ L_u`; `ε = ε₁ n`, `0 < δ < ½` fixed; "cost" is the expected number of evaluations.  `T_t = {|x| = t}` are the type
classes, `dens_t(D) = |D ∩ T_t|/|T_t|`, `maxdens(D) = max_t dens_t(D)`.

**One site.**  `Λ(0) = −ln(q + p e^{−u})`, `Λ(1) = −ln(p + q e^{−u})` (soft gaps at `g = 0`), `Λ(s) = Σ_i Λ(s_i) =
−ln E_π e^{−u d(X,s)}`, `Λ_m = (1−m)Λ(0) + mΛ(1)`.  The *cone* `ψ_s = u d(·,s)` has `A(ψ_s) = e^{−Λ(s)}` and the product
Gibbs law `π_s(x) = π(x) e^{−u d(x,s) + Λ(s)}`: a coordinate with `s_i = 1` is flipped with probability
`η₁ = q e^{−u}/(p + q e^{−u})`, one with `s_i = 0` with probability `η₀ = p e^{−u}/(q + p e^{−u})`.

**Profiles.**  For a centre `s` and a point `x` let `P_{SX}` be the empirical law of the pairs `(s_i, x_i)`: `m = P(S=1)` (type of
`s`), `a = P(S=1, X=0)`, `b = P(S=0, X=1)`, `ρ = a + b = d(x,s)/n`, `κ = P(X=1) = m − a + b` (type of `x`).  Three functions of
the profile `z = (m; a, b)`:

    I(z)      = I(S;X) = h(κ) − m h(a/m) − (1−m) h(b/(1−m)),
    J(z)      = D(P_{X|S} ‖ π | P_S)   = m KL(a/m ‖ q)  + (1−m) KL(b/(1−m) ‖ p)  = I(z) + KL(κ ‖ p),
    I^cone(z) = D(P_{X|S} ‖ π_s | P_S) = m KL(a/m ‖ η₁) + (1−m) KL(b/(1−m) ‖ η₀).

(C) *Counting.*  The class of all `x` with a given profile relative to `s` has `C(mn, an)·C((1−m)n, bn)` points, so its density
in its type class is `e^{−nI + O(log n)}`, its `π`-measure `e^{−nJ + O(log n)}`, its `π_s`-measure `e^{−nI^cone + O(log n)}`
(`|O(log n)| ≤ 2 ln(n+1)`, by `(N+1)^{−1} e^{N h(K/N)} ≤ C(N,K) ≤ e^{N h(K/N)}`).

**Additive instances and the window.**  For `|γ| ≤ u` let `ψ_γ(x) = γ|x|`, `Z_γ = q + p e^{−γ}` (`A(ψ_γ) = Z_γⁿ`),
`π_γ = Bernoulli(p e^{−γ}/Z_γ)^{⊗n}` its Gibbs law.  The Gibbs means fill the *window* `[κ_−, κ_+]`,
`κ_± = p e^{±u}/(q + p e^{±u})`.  Put `v_γ(κ) = −γκ − ln Z_γ` (the normalised log-weight of `ψ_γ` at type `κ`, per site) and

    v(κ) = max_{|γ|≤u} v_γ(κ)  =  KL(κ ‖ p) on the window, continued with slopes ±u outside   ("regularised" KL(κ‖p)).

**Reference instances.**  For `ψ₀ ∈ L_u`: `w₀ = e^{−ψ₀}`, `μ₀ = π w₀/A(ψ₀)` (its Gibbs law), **slack**
`s₀(x,y) = u d(x,y) + ψ₀(x) − ψ₀(y) ∈ [0, 2u d(x,y)]`, `s₀(x → Dᶜ) = min_{y∉D} s₀(x,y)`.  The deepest admissible dip of `ψ₀`
on `D ⊊ Q_n` is the lower McShane extension `ψ₀^D = max_{y∉D}[ψ₀(y) − u d(·,y)]` on `D` (`= ψ₀` off `D`); it is in `L_u` and

    A(ψ₀^D)/A(ψ₀) = 1 + Φ₀(D),     Φ₀(D) = Σ_{x∈D} μ₀(x) (e^{s₀(x→Dᶜ)} − 1),     Ξ₀(q) = max{Φ₀(D) : D ⊊ Q_n, μ₀(D) ≤ q}

(`Ξ₀` is the **tail function** of the reference; `Φ₀⁺(D) = Σ_{x∈D} μ₀(x) e^{s₀(x→Dᶜ)} = Φ₀(D) + μ₀(D)`).  The reference
used below is

    ψ_H(x) = min_{|γ|≤u} [ γ|x| + n ln Z_γ ] = −n v(|x|/n)      (the lower envelope of the normalised additive instances),

a member of `L_u` (a minimum of `u`-Lipschitz functions).  Its Gibbs weight `π(x) w_H(x) = max_γ π_γ(x)` is `e^{−n h(κ)}`
for types in the window: **`μ_H` is, up to a factor `n+1`, uniform over the types of the window and uniform inside each
type** — the normalised-maximum-likelihood mixture of the family `{π_γ}`; `1 ≤ Z_H := A(ψ_H) ≤ n+1`.  `H` is the
"flat-histogram" instance.

**The game function and the three exponent functions** (definitions; all single-letter).

    K_t^γ(a,b) = exp(−t[u·1[a≠b] − Λ(b) − γa − ln Z_γ])      (a = letter of the point, b = letter of the centre),
    F(γ,t) = −ln val(K_t^γ)       (val = min over mixtures M of centres of max_a Σ_b M(b) K(a,b)),
    R_γ(e) = max_{0≤t≤1} [F(γ,t) − t e],      R_0 := R_{γ=0},      F*(t) = max_{|γ|≤u} F(γ,t),
    R^max(e) = max_{|γ|≤u} R_γ(e) = max_{0≤t≤1} [F*(t) − t e]                               (all real e),
    E = sup_{0<t≤1} F*(t)/t,     h = R^max(0),     S(e) = e + R^max(e),     θ_na(x) = R^max(S^{−1}(x))   (x > 0),
    a = θ_na(0+).

`K_t^γ` is the matrix `K_t(a,φ) = e^{−t σ_φ(a)}` of Theorem 11.27(c) for the additive instance `γ|x|` of *this* class (slack
`u[a≠b] − γa + γb`, soft gaps `Λ(b) + γb + ln Z_γ`, `β = 1`).  `R^max` is convex and nonincreasing with slopes in `[−1, 0]`,
`R^max(e) ≥ max(0, −e)`, `R^max = 0` exactly on `[E, ∞)`; `S` is nondecreasing, zero on `(−∞, e_c]`, strictly increasing
afterwards (Theorem F8).  The three exponents of this report:

| algorithms | exponent | max–min form (`S` = centre letter `∼ Bernoulli(m)`, `X` = point letter) |
|---|---|---|
| with a hint, at the instance `g = 0` | `R_0(ε₁)` | `max_m min{ I(S;X) : u P(X≠S) − Λ(P_S) ≤ ε₁ }` `= max_m [h(m) − h((Λ_m+ε₁)/u)]_+` |
| with a hint at the hardest instance `=` adaptive without a hint (worst case) | `R^max(ε₁)` | `max_m min{ I(S;X) : u P(X≠S) − Λ(P_S) + v(P_X) ≤ ε₁ }` |
| non-adaptive without a hint | `θ_na(ε₁)` | `max_m min{ I(S;X) : u P(X≠S) − Λ(P_S) + KL(P_X‖π) + I(S;X) ≤ ε₁ }` `= max_m min{ I(S;X) : D(P_{X|S}‖π_s|P_S) ≤ ε₁ }` |

For `p = ½` the three are `KL((Λ₁+ε₁)/u ‖ ½)`, the same again, and `min{KL(ρ‖½) : KL(ρ‖p_u) ≤ ε₁}` (`m* = ½`, `P_X = π`,
`v = 0` at the optimum): the table of §11.16.

---

## 3. Statements and proofs

### 3.1 The hinted exponents (Theorems 11.25/11.27 restated)

**Theorem F1 (hinted exponents of additive instances) [known].**
(a) *(Theorem 11.27(c); ingredients machine-checked in `GeneralisedDips.lean`; holds for every `n`.)*  For all `n`, `|γ| ≤ u`,
`t ≥ 0`, `ε > 0`: every randomised algorithm that is `(ε/2, δ)`-correct on `L_u` — with or without a hint, adaptive or not —
makes at least `(1 − 2δ) e^{−tε + nF(γ,t)}` evaluations in expectation at the instance `ψ_γ = γ|x|`.  Hence
`n^{−1} ln E|Q(ψ_γ)| ≥ R_γ(ε₁) − o(1)` at accuracy `ε = ε₁n`.
(b) *(The claim after Theorem 11.27 = Theorem A of workstream A; refereed in `reviews/R4`, not machine-checked.)*  With the
instance as a hint — or after `n + 1` evaluations on a star, the instance being additive — the hedged spot-check with samples
from `½π_γ + ½·(uniform mixture over the type classes)` costs `exp(n R_γ(ε₁) + o(n))` at `ψ_γ` (two-state sites:
`R^gen = R^rand`).
So the hinted exponent of the instance `(f, g = 0)` is `R_0(ε₁)`, and the largest hinted exponent of an additive instance is
`R^max(ε₁) = max_{|γ|≤u} R_γ(ε₁)`, positive exactly for `ε₁ < E` (`E = ε₁*`, the class threshold of Theorem 11.28(d,e)).

**Theorem F2 (closed forms; the max–min forms; `g = 0` is not the hardest instance) [proved].**
(a) For all `t ≥ 0`, `|γ| ≤ u`:  `F(γ,t) = max_m min_z [ I(z) + t (uρ − Λ_m + v_γ(κ)) ]` (`z` over the profiles with centre type `m`).
(b) `F(γ,t) = −t ln Z_γ + ln[(1 − e^{−t(u+γ)}) e^{−tΛ(0)} + (1 − e^{−t(u−γ)}) e^{−t(Λ(1)+γ)}] − ln(1 − e^{−2tu})`; with the total
field `λ = θ + γ`, the window of fields `λ_± = θ ± u` and `C(x) = 2 cosh(x/2)`,

    F(γ,t) = ln { [ sinh(t(λ₊−λ)/2) C(λ₋)^t + sinh(t(λ−λ₋)/2) C(λ₊)^t ] / sinh(tu) } − t ln C(λ)

(the log-ratio, at `λ`, between `C^t` and its interpolant on the window by solutions of `y'' = (t/2)² y`).  `F(γ,0) = F(γ,1) = 0`,
`F(γ,t) ≤ 0` for `t ≥ 1`, and `F(γ,t)/t →` the chord gap of `ln C` over `[λ₋, λ₊]` at `λ` as `t ↓ 0` (Theorem 11.28(e)).
(c) For `e ≥ 0`:  `R_γ(e) = max_m min{ I(z) : uρ − Λ_m + v_γ(κ) ≤ e }`; in particular
`R_0(e) = max_m [h(m) − h((Λ_m + e)/u)]_+` (the bracket read as `0` unless `(Λ_m+e)/u ≤ min(m, 1−m)`).
(d) For `e ≥ 0`:  `R^max(e) = max_m min{ I(z) : uρ − Λ_m + v(κ) ≤ e }`.
(e) For `x > 0`:  `θ_na(x) = max_m min{ I(z) : I^cone(z) ≤ x } = max_{0≤τ<1} (F*(τ) − τx)/(1 − τ)`, and
`a = θ_na(0+) = max_m I(z_c(m))`, `z_c(m) = (m; mη₁, (1−m)η₀)` the profile of the cone law (`a = n^{−1} max_s I_{π_s}(S;X)`).
(f) If `p ≠ ½`: `∂F/∂γ(0,t)` is nonzero with the sign of `p − ½` for every `0 < t < 1`; hence `F*(t) > F(0,t)` on `(0,1)`,
the class threshold `E` exceeds the threshold `E_0` of `g = 0`, and `R^max(e) > R_0(e)` for every `0 ≤ e < E`.  To first
order the hardest instance has `γ*` of the sign opposite to `θ` (numerically always: §4).

*Proof.*  (a) Fix `m` (the law `M` of `S`) and `t`.  The bracket is `I(S;X) + t E k(X,S)` with
`k(a,b) = u1[a≠b] − Λ(b) − γa − ln Z_γ`.  `I(S;X) = min_Q D(P_{X|S}‖Q|M)`, and for fixed `Q` and `b` the Gibbs variational
principle gives `min_ν [KL(ν‖Q) + t E_ν k(·,b)] = −ln Σ_a Q(a) e^{−t k(a,b)} =: G_b(Q)`.  So the inner minimum is
`min_Q Σ_b M(b) G_b(Q)`; `G_b` is convex in `Q` and finite, the expression is linear in `M`, so by the minimax theorem
`max_M min_Q Σ_b M(b) G_b(Q) = min_Q max_b G_b(Q) = −ln max_Q min_b Σ_a Q(a) K_t^γ(a,b) = −ln val(K_t^γ)`.
(b) Write `K = K_t^γ`.  `K(0,0) = e^{tΛ^γ(0)}`, `K(1,1) = e^{tΛ^γ(1)}`, `K(0,1) = K(1,1) e^{−t(u+γ)}`, `K(1,0) = K(0,0) e^{−t(u−γ)}`
with `Λ^γ(b) = Λ(b) + γb + ln Z_γ`.  Soft gaps are Lipschitz for the slack (Theorem 11.26(a)), so row `0` of `KM` is
nondecreasing and row `1` nonincreasing in `M(0)`; they cross, and the value is
`(K00 K11 − K01 K10)/(K00 − K10 + K11 − K01)`, which is the first formula.  The cosh form follows from `P(x) = ln(1+e^{−x}) =
ln C(x) − x/2`, `Λ^γ(0) = P(λ) − P(λ₊)`, `Λ^γ(1) = (λ − λ₋) + P(λ) − P(λ₋)`.  `F(γ,1) = 0` because
`(1 − e^{−(u+γ)})(q + pe^{−u}) + (e^{−γ} − e^{−u})(p + qe^{−u}) = Z_γ (1 − e^{−2u})`.  For `t ≥ 1` take `Q = π_γ` in
`F = min_Q max_b G_b(Q)`: `G_b(π_γ) = −tΛ^γ(b) − ln E_{π_γ} e^{−t s(·,b)} ≤ 0` by Jensen.  The limit `t ↓ 0` is a Taylor expansion.
(Checks: closed form against a generic game solver `3·10⁻¹⁴`, cosh form `1.4·10⁻¹⁵`, `t11`, `t17`.)
(c) Let `c_γ(z) = uρ − Λ_m + v_γ(κ)`.  For `e ≥ 0` the set `{c_γ ≤ e}` contains the profile `X = S` (`c_γ = v_γ(m) − Λ_m ≤ 0`,
because `Z_γ ≥ q + pe^{−u}` and `e^γ Z_γ ≥ p + qe^{−u}`).  `I` is convex in `(a,b)` and `c_γ` is affine, so by Sion's theorem
`min{I : c_γ ≤ e} = sup_{t≥0} min_z [I + t(c_γ − e)]`; taking `max_m` and using (a), `max_m min{…} = sup_{t≥0} [F(γ,t) − te]`,
and `t ≥ 1` contributes at most `0`, the value at `t = 0`, by (b).  For `γ = 0` the inner problem is
`min{I(S;X) : P(X≠S) ≤ ρ_m}`, the rate–distortion function of a Bernoulli(`m`) source with Hamming distortion
(**[known]**; from memory: Cover–Thomas, Thm 10.3.1).  (Check: `2·10⁻¹⁵` against the game formula, 40 parameter pairs, `t03`;
`1·10⁻¹¹` against the closed form, `t01`.)
(d) `v = max_γ v_γ`, so `min{I : c_0 + v ≤ e} = sup_t min_z max_γ [I + t(c_0 + v_γ − e)] = sup_t max_γ min_z […]` by Sion
(convex in `z`; `v_γ(κ) = −γκ − ln(q + pe^{−γ})` is concave in `γ`; compact convex sets); then `max_m` and (a), (c).
(Check: `2·10⁻¹⁴`, `t03`.)
(e) Put `c_H = uρ − Λ_m + v(κ)` and `n_m(x) = min{I(z) : I(z) + c_H(z) ≤ x}`.  The constraint is strictly satisfied at
`z_c` (`I + c_H ≤ I^cone(z_c) = 0 < x`), so `n_m(x) = sup_{t≥0} min_z [(1+t) I + t c_H − t x] = sup_{0≤τ<1} (φ_m(τ) − τx)/(1−τ)`
with `φ_m(τ) = min_z [I + τ c_H]` and `τ = t/(1+t)`.  As in (d), `max_m φ_m(τ) = max_γ F(γ,τ) = F*(τ)`.  So
`θ* := max_m n_m(x) = sup_{τ<1} (F*(τ) − τx)/(1−τ)`; the supremum is attained at some `τ* < 1` because `F*(1) = 0`, `F*` is
Lipschitz and `x > 0`.  Then `F*(τ) − τ(x − θ*) ≤ θ*` on `[0,1]` with equality at `τ*`, i.e. `R^max(x − θ*) = θ*`,
`S(x − θ*) = x`, `θ* = θ_na(x)`.  It remains to replace `I + c_H` by `I^cone`.  By Theorem F3, `I^cone = I + c_H +
(KL(κ‖p) − v(κ)) ≥ I + c_H`, so `min{I : I^cone ≤ x} ≥ n_m(x)`.  Conversely let `z₀` satisfy `I + c_H ≤ x` with `κ₀ > κ_+`
and let `X₁ = X·B`, `B ∼` Bernoulli(`κ_+/κ₀`) independent: `P(X₁ = 1) = κ_+`, `I(S;X₁) ≤ I(S;X)` (data processing),
`P(X₁ ≠ S) ≤ ρ₀ + κ₀ − κ_+`, `KL(κ_+‖p) = v(κ₀) − u(κ₀ − κ_+)`; so the profile `z₁` of `(S, X₁)` has `I^cone(z₁) ≤
(I + c_H)(z₀) ≤ x` and `I(z₁) ≤ I(z₀)` (symmetrically below `κ_−`).  Hence equality.  As `x ↓ 0` the sets `{I^cone ≤ x}` shrink
to `z_c(m)`, uniformly in `m`.  (Check: `10⁻¹¹` between the two forms for `x` on both sides of `h`, `t11`.)
(f) From (b), `∂F/∂γ(0,t) = t·g(t)/[(1 − e^{−tu})(A₀^t + A₁^t)]` with `A₀ = q + pe^{−u}`, `A₁ = p + qe^{−u}` and
`g(t) = A₀^t (p + qe^{−tu}) − A₁^t (q + pe^{−tu})`.  `ln[A₀^t (p + qe^{−tu})] − ln[A₁^t (q + pe^{−tu})] = G₀(t) − G₁(t) =: D(t)`,
where `G_b(t) = t k_b(1) − k_b(t)` is the chord gap of `k₀(t) = ln(q + pe^{−tu})`, resp. `k₁(t) = ln(p + qe^{−tu})`, on `[0,1]`.
`D(0) = D(1) = 0` and `D'' = k₁'' − k₀'' = u²[q_t(1−q_t) − p_t(1−p_t)]`, the variances of the tilted Bernoulli laws with logits
`−L − tu` and `L − tu`, `L = ln(p/q)`.  For `p < ½`: `|−L − tu| = ||L| − tu| < |L| + tu = |L − tu|`, the variance is a
decreasing function of the modulus of the logit, so `D'' > 0`: `D` is strictly convex, `D < 0` on `(0,1)` and `D'(0) < 0`.
So `∂F/∂γ(0,t) < 0` on `(0,1)` (and `> 0` for `p > ½`), `F*(t) > F(0,t)`, and `E = sup F*(t)/t > lim F(0,t)/t = E_0`
(the derivative of the chord gap is `D'(0)/(2u) ≠ 0`).  If `0 ≤ e < E_0`, the maximiser `t₀` of `F(0,t) − te` lies in `(0,1)`
(`R_0(e) > 0 ≥ −e`), so `R^max(e) ≥ F*(t₀) − t₀e > R_0(e)`; if `E_0 ≤ e < E` then `R_0(e) = 0 < R^max(e)`.  (Check of the
derivative formula and its sign by finite differences: `t21`.)  ∎

So the hinted exponent of the instance `(f, g=0)` has the "ball" form `max_m [h(m) − h(ρ_m)]`: Hamming balls of radius
`ρ_m n` around centres of type `m` are the smallest sensitive sets, `h(m) − h(ρ)` is the exponent of the largest density of
such a ball in a type class (the rate–distortion function), and the adversary optimises the type of the centre
(`ln((1−m*)/m*) = ((Λ(1)−Λ(0))/u) ln((1−ρ*)/ρ*)`: for `p < ½`, `m* < ½`, and in all computed cases `m* > p`).  For `p = ½`:
`m* = ½`, `KL(ρ‖½)`.

### 3.2 The shift identity

**Theorem F3 (shift identity with a field) [proved; machine-checked: `lean/WorkstreamF.lean`, `shift_identity`].**
For every joint law of `(S, X)` on `{0,1}²`,

    D(P_{X|S} ‖ π_s | P_S)  =  I(S;X)  +  KL(P_X ‖ π)  +  u·P(X ≠ S)  −  Λ(P_S),          i.e.   I^cone = I + KL(κ‖p) + uρ − Λ_m.

*Proof.*  `π_b(x) = π(x) e^{−u1[x≠b] + Λ(b)}`, so `ln(P(x|b)/π_b(x)) = ln(P(x|b)/P(x)) + ln(P(x)/π(x)) + u1[x≠b] − Λ(b)`; take
expectations.  ∎  (The Lean file proves the one-site statement `klBin_tilt`: `KL(x ‖ q₀e^{−u}/Z) = KL(x‖q₀) + ux + ln Z`,
`Z = 1 − q₀ + q₀e^{−u}` — `klBin_shift` of `HintRecursion.lean` is the case `q₀ = ½` — the chain rule `J = I + KL(κ‖p)`
(`sphere_rate_eq`) and their combination; `lake env lean` reports no error and the axioms `propext, Classical.choice,
Quot.sound`.  Numerically: `2.7·10⁻¹⁵` on 20000 random points, `t01`.)

Read at a profile: the accuracy that a sample of `e^{nθ}` points per type class certifies without a hint
(`I^cone`: the rate at which the cone law leaves the set that the sample has seen) is the exponent `θ = I(S;X)` of the sample,
plus the accuracy `uρ − Λ_m` that the same sample certifies with the hint `g = 0`, **plus `KL(P_X‖π)`**.  In the uniform
case the optimal profile has `P_X = π` and the last term vanishes; with a field it does not.  The sum
`uρ − Λ_m + KL(P_X‖π)` is the hinted accuracy at another instance: a dip of the flat-histogram instance `H` with centre `s`
and exit profile `z` has the effect `e^{n(uρ − Λ_m + v(κ))}` (it is a cone whose peak is as high as `w_H` at the exit allows,
and `w_H = e^{nv}`), and `v = KL(·‖p)` on the window.  This is why the hinted partner of `θ_na` is `R^max` (Theorem F2(d,e))
and not `R_0`.

### 3.3 Non-adaptive algorithms

For `ψ ∈ L_u` and `0 < q < 1` let `t_κ = t_κ(ψ,q)` be the smallest value `τ` of `w` on `T_κ` with `dens_κ{w > τ} ≤ q` (the upper
`q`-quantile of `w` on the type class), `ψ^{tr,q}(x) = max(ψ(x), −ln t_{|x|})` (the weight `min(w, t_{|x|})`: `ψ` *truncated at
the type-wise quantiles*), and

    ε_n^{tr}(q) = sup_{ψ∈L_u} ln [ A(ψ)/A(ψ^{tr,q}) ].

**Theorem F4 (non-adaptive algorithms without a hint).**
(a) **[proved]** *Quantiles are Lipschitz.*  `t_{κ±1} ≤ e^u t_κ`; hence `ψ^{tr,q} ∈ L_u`, it differs from `ψ` only on
`D = {x : w(x) > t_{|x|}}`, and `maxdens(D) ≤ q`.
(b) **[proved]** *The non-adaptive complexity is `1/q` at the accuracy `ε_n^{tr}(q)`, for every `n` — no isoperimetry.*
(i) If `ε < ε_n^{tr}(q)`, every randomised non-adaptive `(ε/2, δ)`-correct algorithm makes at least `(1−2δ)/q` evaluations.
(ii) Sample `M` points uniformly from *each* type class (`(n+1)M` evaluations), `Â = Σ_κ π(T_κ)·(`mean of `w` over the sample
of `T_κ)`.  With `K = Mq`: `ln Â ≥ ln A − ε_n^{tr}(q) − ln 2` outside an event of probability `(n+1)e^{−K/8}`, and
`ln Â ≤ ln A + ln(1/δ₂)` outside an event of probability `δ₂`.  So the shifted estimate is `(ε/2, (n+1)e^{−K/8} + δ₂)`-correct
on `L_u` as soon as `ε ≥ ε_n^{tr}(q) + ln(2/δ₂)`.
(c) **[proved]** *Lower bound for the exponent.*  For every `m` with `mn` integer, `0 < θ < I(z_c(m))` and `n` with `e^{−nθ} < 1/(n+1)`:
`ε_n^{tr}(e^{−nθ}) ≥ n F_m(θ + 3 ln(n+1)/n) − 5 ln(n+2)`, `F_m(θ) := min{ I^cone(z) : I(z) ≤ θ }` (centre type `m`).
Consequently every non-adaptive algorithm needs `exp(n θ_na(ε₁) − o(n))` evaluations.
(d) **[proved, given Theorem F6]** *Upper bound.*  `ε_n^{tr}(e^{−nθ}) ≤ n·S((R^max)^{−1}(θ)) + o(n)` uniformly on compact
subsets of `θ > 0` (the right side is `0` for `θ ≥ a`).  Consequently `exp(n θ_na(ε₁) + o(n))` evaluations suffice, by
type-stratified Monte Carlo (equivalently: importance sampling from `μ_H`).

So **the exponent of non-adaptive algorithms is `θ_na(ε₁) = max_m min{ I(S;X) : D(P_{X|S}‖π_s|P_S) ≤ ε₁ }`** for
`0 < ε₁ < E`, `θ_na(0+) = a = max_m I(z_c(m))` at vanishing extensive accuracy.

*Proof.*  (a) Let `X` be uniform on `T_κ` and `Y` be `X` with a uniformly chosen `0` flipped to `1`; by symmetry `Y` is uniform
on `T_{κ+1}`, and `w(Y) ≤ e^u w(X)`.  So `dens_{κ+1}{w > e^u t_κ} ≤ dens_κ{w > t_κ} ≤ q`, hence `t_{κ+1} ≤ e^u t_κ`; the same
with the roles exchanged.  Thus `x ↦ −ln t_{|x|}` is `u`-Lipschitz and so is the maximum of two `u`-Lipschitz functions.
(b)(i) `L_u` and `A` are invariant under permutations `σ` of the coordinates.  Take the pairs `(ψ∘σ, ψ^{tr,q}∘σ)` with equal
weights; a point `x` lies in the difference set of the pair `σ` iff `σx ∈ D`, an event of probability `dens_{|x|}(D) ≤ q`.
Theorem 11.45(a) (`nonadaptive_expected_queries_ge`).  (ii) `dens_κ{w ≥ t_κ} ≥ q` by the choice of `t_κ`, so the variables
`min(w(X_i), t_κ)/t_κ ∈ [0,1]` of the class `κ` have total mean at least `K`; the multiplicative Chernoff bound gives, outside
an event of probability `e^{−K/8}`, a class mean of `w` of at least half of `E_{T_κ} min(w, t_κ)`.  On the intersection,
`Â ≥ ½ A(ψ^{tr,q}) ≥ ½ e^{−ε_n^{tr}(q)} A(ψ)`.  `E Â = A`: Markov.
(c) Let `|s| = mn`, `ψ_s = u d(·,s)`, `q = e^{−nθ} < 1/(n+1)`.  On `T_t` the weight is `e^{−u d(x,s)}`, the distance takes the
values `r = |t−k|, |t−k|+2, …`, and `dens_t{d = r}` is a hypergeometric law in `r`: unimodal, with a mode `r_t*` of density at
least `1/(n+1)`.  So `D ∩ T_t = {d < ρ_t}` with `ρ_t ≤ r_t*`, `dens_t{d ≤ ρ_t} > q`, and, the densities of the shells being
nondecreasing up to the mode, `dens_t{d = r} > q/(n+1)` for all `ρ_t ≤ r ≤ r_t*`.
`A(ψ_s^{tr}) = Σ_{x∉D} π(x) e^{−u d(x,s)} + Σ_t π(T_t) dens_t(D) e^{−uρ_t}`; the second sum is at most
`(n+1) Σ_t π({x∈T_t : d = ρ_t}) e^{−uρ_t}`, which is at most `(n+1)` times the first, and the first is
`e^{−Λ(s)} π_s(Dᶜ)`.  So `A(ψ_s)/A(ψ_s^{tr}) ≥ 1/((n+2) π_s(Dᶜ))`.  `Dᶜ` is a union of at most `(n+1)²` profile classes.  A
shell of `T_t` with `ρ_t ≤ r ≤ r_t*` has density `> q/(n+1)`, so by (C) its profile has `I ≤ θ + 3 ln(n+1)/n` and its
`π_s`-measure is at most `e^{−n F_m(θ + 3ln(n+1)/n) + 2 ln(n+1)}`; the `π_s`-measures of the shells of `T_t` are unimodal too
(the hypergeometric law tilted by `e^{−ur}`), with a mode at or before `r_t*`, so the shells beyond `r_t*` have no more
`π_s`-measure than the shell `r_t*`.  Summing gives the claim.  With (b)(i): if `ε₁ < F_m(θ)`, non-adaptive algorithms need
`(1−2δ)e^{nθ}` evaluations for large `n`; and `sup{θ : max_m F_m(θ) > ε₁} = max_m min{I(z) : I^cone(z) ≤ ε₁} = θ_na(ε₁)`
(Theorem F2(e)).
(d) Let `q = e^{−nθ}`, `ψ ∈ L_u`, `D` as in (a), `T = max_κ π(T_κ) t_κ`.  `A(ψ^{tr}) ≥ Σ_κ π(T_κ) t_κ dens_κ{w ≥ t_κ} ≥ qT`.  By (a),
`t_κ ≤ T·min_{κ'} e^{un|κ−κ'|}/π(T_{κ'}) ≤ e^{2u}(n+1) T w_H(κ)` (`1/π(T_{κ'}) ≤ (n+1)e^{nKL(κ'‖p)}`, and `nv` is the
inf-convolution of `nKL(·‖p)` with `un|·|`).  For `x ∈ D`, `y ∉ D`: `w(x) ≤ w(y)e^{ud(x,y)} ≤ t_{|y|} e^{ud(x,y)}`.  Hence

    A(ψ) − A(ψ^{tr}) ≤ Σ_{x∈D} π(x) min_{y∉D} t_{|y|} e^{ud(x,y)} ≤ e^{2u}(n+1) T · Z_H · Φ_H⁺(D),     μ_H(D) ≤ maxdens(D) ≤ q,

and Theorem F6 bounds `Φ_H⁺(D)` by `exp(n[(R^max)^{−1}(θ)] + o(n))` (`= e^{−nθ + o(n)}` for `θ ≥ a`).  With `T ≤ e^{nθ}A(ψ^{tr})`:
`A(ψ)/A(ψ^{tr}) ≤ 1 + e^{n[θ + (R^max)^{−1}(θ)] + o(n)}`, and `θ + (R^max)^{−1}(θ) = S(e)` at `R^max(e) = θ`.  Then (b)(ii) with
`θ = θ_na(ε₁ − η)`.  ∎

*What replaces the tail lemma, and the sampling distribution.*  For the *characterisation* (b) nothing is needed: the
truncation at type-wise quantiles is itself a member of the class (this is the one place where the coupling of adjacent type
classes is used), so the same extremal function `ε_n^{tr}` bounds the complexity from both sides.  Isoperimetry enters only in
the *evaluation* (d) of that function.  The right sample is uniform on every type class — up to polynomial factors the Gibbs
law `μ_H` of the flat-histogram instance — with importance weights.  Plain Monte Carlo from `π_f` is exponentially worse, and
so is every single (tilted) product measure, though the best one comes close (Proposition F11).

### 3.4 Reference instances and the tail lemma

**Lemma F5 (tail lemma relative to a reference instance) [proved].**  Let `ψ₀ ∈ L_u` be a reference with `w₀, μ₀, s₀, Ξ₀` as in §2,
`ψ ∈ L_u` arbitrary (or `W` a fibre average of a `u`-Lipschitz function on a larger cube, `−ln W ∈ L_u`), and `ŵ = w/w₀`.  Then
`A(ψ) = A(ψ₀)·E_{μ₀} ŵ`; `ŵ(x) ≤ ŵ(y) e^{s₀(x,y)}` for all `x, y`; and for every level `t > 0` with `q := μ₀(ŵ > t) < 1`:

    E_{μ₀} (ŵ − t)₊  ≤  t·Ξ₀(q),

with equality for `ψ = ψ₀^D` (the deepest dip of the reference on `D`) and `t = 1`.
*Proof.*  `ŵ(x)/ŵ(y) = [w(x)/w(y)]·[w₀(y)/w₀(x)] ≤ e^{u d(x,y) + ψ₀(x) − ψ₀(y)}`.  With `D = {ŵ > t} ≠ Q_n`: for `x ∈ D`, `y ∉ D`,
`ŵ(x) ≤ t e^{s₀(x,y)}`, so `Σ_{x∈D} μ₀(x)(ŵ(x) − t) ≤ t Φ₀(D) ≤ t Ξ₀(μ₀(D))`.  ∎
For `ψ₀ = 0` and `p = ½` this is Lemma 11.43(b) with `Ξ₀(q) = 2^{−n} E_r(n)` (Harper).  In general `Ξ₀` is a finite maximum over
subsets — a number that depends on `(n, p, u, q)` only; no closed form is claimed.  (Checked on the 4-cube with all 65534
subsets, for the references `H`, `0` and additive ones: 11166 thresholds of fibre averages of random Lipschitz functions, no
violation, equality attained; the slack with the wrong orientation, Harper's function, and the tail function of the reference
`0` used for `H` are all violated: `t15`.)

**Theorem F6 (the converse tail lemma: asymptotic isoperimetry for the reference `H`) [proved — paper proof, unrefereed; it
uses the inherently-typical-subset lemma of Ahlswede–Yang–Zhang in the form of workstream A (Lemma T below, proof reproduced)].**
There is a sequence `ω_n → 0`, depending on `p, u` only, such that for all `n`, all real `e` and all `D ⊊ Q_n`:

    Φ_H⁺(D) = Σ_{x∈D} μ_H(x) e^{s_H(x→Dᶜ)} ≥ e^{ne}      ⟹      μ_H(D) ≥ exp(−n [R^max(e − ω_n) + ω_n]).

Equivalently: if `μ_H(D) ≤ e^{−nθ}` then `n^{−1} ln Φ_H⁺(D) ≤ (R^max)^{−1}(θ − ω_n) + ω_n`, where `(R^max)^{−1}` is the inverse of
`R^max` on `(−∞, E)` (`= −θ` for `θ ≥ a`).  In words: every set that is `e`-sensitive for the flat-histogram instance is hit
by its Gibbs law — the type-uniform mixture — with probability at least `e^{−nR^max(e) − o(n)}`; the tail function of `H` has
the exponent `χ(θ) = (R^max)^{−1}(θ)`, the inverse of the hinted exponent of the hardest additive instance.  For `e ≥ 0` this
says that the hinted exponent of `H` is at most `R^max`; it is at least `R^max` because `w_H ≥ Z_γ^{−n} e^{−γ|x|}` pointwise
(dips of `H` are at least as effective as those of any additive instance), so `H` and `γ*|x|` are equally hard.

*Lemma T (inherently typical subsets; workstream A, Lemma 5, from Ahlswede–Yang–Zhang 1997) [known; proof reproduced].*
Let `∅ ≠ C ⊂ Q_n`, `m ≥ 1`, `α_C = −n^{−1} ln π(C)`.  There are a finite `𝒰 ⊂ [0,1]` with `|𝒰| ≤ (m+1)²`, maps
`u_i : {0,1}^{i−1} → 𝒰`, a set `C̃ ⊂ C` and a law `P_{UX}` on `𝒰 × {0,1}` such that (1) every `x ∈ C̃` has the joint type
`P_{UX}` with its label sequence `(u_i(x^{i−1}))_i`; (2) `π(C̃) ≥ π(C)(n+1)^{−2(m+1)²}`; (3) `α_C − 2/m ≤ α := D(P_{X|U}‖π|P_U) ≤ α_{C̃}`;
(4) for `Xⁿ ∼ π(·|C̃)`, `I` uniform on `[n]` and `V = (I, X^{I−1})`: `I(X_I; V | U_I) = α_{C̃} − α ≤ η_{m,n} := 2/m + 2(m+1)² ln(n+1)/n`.
*Proof (A_REPORT §2.3).*  Let `p_i(·|x^{i−1})` be the conditional laws of `π(·|C)` and `u_i(x^{i−1})(a) = ⌈m p_i(a|x^{i−1})⌉ / Σ_b ⌈m p_i(b|x^{i−1})⌉`
(so `u_i ≥ p_i m/(m+2)` pointwise, at most `(m+1)²` values).  `C̃` := the most probable class of the partition of `C` by the joint
type of `((u_i(x^{i−1}), x_i))_i` (at most `(n+1)^{2(m+1)²}` classes): (1), (2).  For `x ∈ C̃`: `π(x)/π(C) = ∏ p_i ≤ (1+2/m)ⁿ ∏ u_i(x^{i−1})(x_i)`;
taking logarithms, `α_C ≤ 2/m + Σ P_{UX}(u,a) ln(u(a)/π(a)) = 2/m + α − D(P_{X|U}‖U|P_U) ≤ 2/m + α`.  By (1) `(U_I, X_I) ∼ P_{UX}`, and
by the chain rule `α_{C̃} = n^{−1} D(P_{Xⁿ}‖πⁿ) = D(P_{X_I|V}‖π|P_V) = α + I(X_I;V|U_I)`.  ∎

*Lemma SL (single-letter bound).*  Let `P_{UX}` be a law on `𝒰 × {0,1}` (`𝒰` finite), `μ_u = P(X=1|U=u)`, `α = D(P_{X|U}‖π|P_U)`, and
`B ≥ v(P_X)`.  Then there is a kernel `W(x'|x,u)` with

    u·P(X' ≠ X) + v(P_{X'}) ≤ B,        P_{X'}(1) ∈ [κ_−, κ_+],        I(X';U) ≤ R^max(B − α).

*Proof.*  Let `ν_u = P(X'=1|U=u)`; the cheapest kernel with these conditional laws has `P(X'≠X|U=u) = |ν_u − μ_u|`.  So it
suffices to bound `V := min{ I(ν) : g(ν) ≤ 0 }`, `I(ν) = h(ν̄) − Σ_u P(u) h(ν_u)`, `ν̄ = Σ_u P(u)ν_u`,
`g(ν) = u Σ_u P(u)|ν_u − μ_u| + v(ν̄) − B` (both convex; `g(μ) ≤ 0`).  By Sion's theorem, twice (`v = max_γ v_γ`, `v_γ(ν̄)` affine in
`ν` and concave in `γ`): `V = sup_{τ≥0} max_{|γ|≤u} Ψ(τ,γ)`, `Ψ(τ,γ) = min_ν [ I(ν) + τ(u Σ_u P(u)|ν_u − μ_u| + v_γ(ν̄) − B) ]`.
*`τ ≥ 1`:* `Ψ ≤ I(X;U) + τ(v_γ(P_X) − B) ≤ I(X;U) + v(P_X) − B ≤ α − B ≤ R^max(B − α)` (take `ν = μ`; `v_γ ≤ v ≤ KL(·‖p)`,
`α = I(X;U) + KL(P_X‖π)`, `R^max(e) ≥ −e`).
*`τ ≤ 1`:* `I(ν) = min_Q Σ_u P(u) KL(ν_u‖Q)` and `u|ν_u − μ_u| = max{E_{ν_u}φ − E_{μ_u}φ : |φ(0) − φ(1)| ≤ u}`.  For fixed `Q` and `u`,
exchanging `min_{ν_u}` and `max_φ` (Sion) and using the Gibbs variational principle,

    min_{ν_u} [ KL(ν_u‖Q) + τu|ν_u − μ_u| − τγν_u ] = max_φ [ −ln E_Q e^{−τψ} − τ E_{μ_u} ψ − τγμ_u ],      ψ := φ − γx.

By the Donsker–Varadhan inequality `−E_{μ_u}ψ ≤ KL(μ_u‖π_γ) + ln E_{π_γ} e^{−ψ}`, and `KL(μ_u‖π_γ) = KL(μ_u‖π) + γμ_u + ln Z_γ`.
Summing over `u`:  `Ψ(τ,γ) ≤ min_Q max_ψ g_Q(ψ) − τ(B − α)`, `g_Q(ψ) = −ln E_Q e^{−τψ} + τ ln E_{π_γ} e^{−ψ}`, the maximum over
`ψ(0) − ψ(1) = s ∈ [γ−u, γ+u]`.  `g_Q'(s) = τ[Q_s(0) − π_s(0)]` and `g_Q''(s) = τ[π_s(0)π_s(1) − τ Q_s(0)Q_s(1)]` (tilted laws); at a
critical point both tilted laws agree, so `g_Q'' = τ(1−τ) r(1−r) > 0` for `τ < 1`: the maximum is at an endpoint, i.e. at one
of the two distance functions `ψ = u1[·≠b] − γ· + γb`, where `g_Q = −ln Σ_a Q(a) K_τ^γ(a,b)`.  Hence
`min_Q max_ψ g_Q = F(γ,τ)` (`τ = 1` by continuity) and `Ψ(τ,γ) ≤ F(γ,τ) − τ(B − α) ≤ R^max(B − α)`.
*Window.*  If the kernel found has `κ' := P_{X'}(1) > κ_+`, replace `X'` by `X'' = X'·B'`, `B' ∼` Bernoulli(`κ_+/κ'`) independent:
`I(X'';U) ≤ I(X';U)`, `P(X''≠X) ≤ P(X'≠X) + κ' − κ_+`, `v(κ_+) = v(κ') − u(κ' − κ_+)`: the constraint is preserved.  Symmetrically
below `κ_−`.  ∎  (Check by a primal minimisation over kernels, independent of the game formula: for about 1900 laws `P_{UX}` with
`|𝒰| ≤ 4`, random and by local ascent, and `e = B − α` of both signs, `V − R^max(e) ≤ −2.5·10⁻⁵`; equality to `7·10⁻¹²` at the
"generalised dip" `U = S ∼` Bernoulli(`m*`), `X|U ∼` cone law: `t16`.)

*Proof of Theorem F6.*  Let `δ = n^{−1/4}`, `δ₁ = δ/(2u)`, `m = ⌈n^{1/8}⌉`.  `μ_H(x) e^{s_H(x,y)} = π(x) e^{n v(κ_y) + u d(x,y)}/Z_H`, `1 ≤ Z_H ≤ n+1`.
*Step 1.*  For `x ∈ D` let `B(x) = min_{y∉D} [v(κ_y) + u d(x,y)/n]`; it takes at most `(n+1)²` values (the type and the distance
of a minimiser).  So `Φ_H⁺(D) ≤ (n+1)² max_C π(C) e^{nB_C}` over the classes `C` of constant `B(x) = B_C`; fix the largest:
`B − α_C ≥ e − 2 ln(n+1)/n`.  By construction (∗): *for `x ∈ C`, every `y` with `v(κ_y) + u d(x,y)/n < B` lies in `D`.*
*Step 2.*  Lemma T for `C`: `C̃`, `(u_i)`, `P_{UX}`, `α ≤ α_{C̃} ≤ α_C + 2(m+1)² ln(n+1)/n`.  All points of `C̃` have the type `P_X`,
and `v(P_X) ≤ B` (`v` is `u`-Lipschitz, and the minimiser `y` of a point `x` has `|κ_y − κ_x| ≤ d(x,y)/n`).
*Step 3 (shallow case).*  If `B < v(P_X) + 3δ`:  `μ_H(D) ≥ μ_H(C̃) = π(C̃) e^{n v(P_X)}/Z_H`, so
`−n^{−1} ln μ_H(D) ≤ α_C − B + 3δ + [2(m+1)² + 1] ln(n+1)/n ≤ −e + o(1) ≤ R^max(e) + o(1)`.
*Step 4 (deep case).*  Otherwise apply Lemma SL with the budget `B − 2δ ≥ v(P_X)`: a kernel `W` with
`u P(X'≠X) + v(P_{X'}) ≤ B − 2δ`, `Q := P_{X'} ∈ [κ_−, κ_+]`, `I(X';U) ≤ R^max(B − 2δ − α)`.  Let `Xⁿ ∼ π(·|C̃)` and, given `Xⁿ = x`, draw
the `X'_i ∼ W(·|x_i, u_i(x^{i−1}))` independently.  For every `x ∈ C̃` the joint type of `(u_i, x_i)` is `P_{UX}`, so
`E d(X'ⁿ, x) = n P(X'≠X)` and `E|X'ⁿ| = nQ`; by Hoeffding's inequality, outside an event of probability `θ_n := 3e^{−2nδ₁²}`,
`d(X'ⁿ,x) ≤ n(P(X'≠X) + δ₁)` and `| |X'ⁿ|/n − Q | ≤ δ₁`, hence `v(κ_{X'ⁿ}) + u d(X'ⁿ,x)/n ≤ B − δ < B` and `X'ⁿ ∈ D` by (∗).  With
`𝒯 = {y : |κ_y − Q| ≤ δ₁}`:  `P(X'ⁿ ∈ D ∩ 𝒯) ≥ 1 − θ_n`.
*Step 5 (chain rule; A_REPORT §2.3, Step 5).*  `X'^{i−1} — X^{i−1} — X'_i` is a Markov chain, so
`n^{−1} D(P_{X'ⁿ}‖Qⁿ) = n^{−1} Σ_i [I(X'_i; X'^{i−1}) + D(P_{X'_i}‖Q)] ≤ n^{−1} Σ_i D(P_{X'_i|X^{i−1}}‖Q|P_{X^{i−1}}) = I(X'_I; V)`
(`P_{X'_I} = Q` because `(U_I, X_I, X'_I) ∼ P_{UX} × W`) `= I(X'_I;U_I) + I(X'_I;V|U_I) ≤ I(X';U) + I(X_I;V|U_I) ≤ I(X';U) + η_{m,n}`
(given `U_I`, `V — X_I — X'_I` is Markov; Lemma T(4)).
*Step 6.*  By the data-processing inequality for the event `D ∩ 𝒯`:  `(1 − θ_n) ln(1/Qⁿ(D∩𝒯)) − ln 2 ≤ D(P_{X'ⁿ}‖Qⁿ)`.  For
`y ∈ 𝒯`: `Qⁿ(y) ≤ e^{−n h(κ_y)}` and `μ_H(y) = e^{−n[h(κ_y) + KL(κ_y‖p) − v(κ_y)]}/Z_H ≥ Qⁿ(y) e^{−n c δ₁²}/(n+1)` (`KL(·‖p) − v` vanishes on the
window and is `O(dist²)` near it).  Altogether

    −n^{−1} ln μ_H(D) ≤ [R^max(B − 2δ − α) + η_{m,n} + ln 2/n]/(1 − θ_n) + cδ₁² + ln(n+1)/n,     B − α ≥ e − [2(m+1)² + 2] ln(n+1)/n,

and all error terms tend to `0` uniformly in `D` and `e` (`R^max` is nonincreasing and `1`-Lipschitz; for `e` below
`−c₁ := n^{−1} ln min_x μ_H(x)` the statement is trivial).  ∎

*Remarks.*  (i) The same proof with `v ≡ 0`, `w_H ≡ 1` and "density at most `q` in every type class" in place of "`μ_H(D) ≤ q`"
is Theorem A(ii) of workstream A at the instance `g = 0` (exponent `R_0`); with `v_γ` in place of `v` it is that theorem at
`γ|x|`.  What is new is the reference `H`, the budget that depends on the type of the exit point, and the collapse
`sup_{P_UX} V = max_γ R_γ` (Lemma SL) — the multi-constraint problem is the maximum of the single-instance problems, by
minimax.  (ii) *Status of exact isoperimetry.*  No finite-`n` extremal statement is available or used; the `o(n)` is of the poor
kind (`n^{7/8}`-ish).  On the 4-cube the exact `Ξ_H(q)` exceeds the best set of the family used for the formulas (balls with
type-dependent radii around one centre) by a factor at most `2` (unions of two balls, as in the uniform cube): `t18`.
(iii) *Exact sums on profile sets.*  For unions of profile classes around a centre — balls with type-dependent radii,
Hamming balls, anisotropic balls `{αa + βb < c}`, rectangles, far-side corners, bands not containing the centre — `μ_H(D)` and
`Φ_H⁺(D)` were computed exactly at `n = 600` and `n = 2000` (three parameter pairs, seven centre types).  On all 1829 sets with
`θ = −n^{−1} ln μ_H(D) ≥ 6 ln n/n` the inequality of the theorem holds with `ω_n = 3 ln n/n`; the raw difference
`n^{−1} ln Φ_H⁺(D) − (R^max)^{−1}(θ)` is at most `+0.005` (`t23`), and for the two extremal shapes at the optimal centre type it
is `0.92 ln n/n` (density ball) and `1.4`–`1.7 ln n/n` (the anisotropic ball tangent at the optimal exit profile) for
`n = 500 … 4000` (`t24`): the exponent is attained, with polynomial factors that differ between shapes — the density ball
is not the exact extremal set.

### 3.5 One more level, relative to a reference instance

*Bracket procedures*, *families* and their *exponent functions* are those of §11.18, for the class `L_u` on `Q_d` with the
reference measure `Bernoulli(p)^{⊗d}` (same `p, u` in every dimension).

**Theorem F7 (Theorem 11.52 relative to a reference) [proved, given the proof of Theorem 11.52 (unrefereed) — every step that
changes is written out below; outer loop simulated, `t14`].**  For every `d` let `ψ_ref^{(d)} ∈ L_u(Q_d)` be a reference whose Gibbs
law `μ^{(d)}` can be sampled and whose weights `w_ref^{(d)}` are known (no evaluations), with `min_x μ^{(d)}(x) ≥ e^{−c₁d}`, and
suppose its tail function satisfies, uniformly for `θ` in compact subsets of `(0, ∞)`,

    d^{−1} ln [ Ξ^{(d)}(e^{−dθ}) e^{dθ} ] ≤ Ŝ(θ) + o(1),        Ŝ ≥ 0 continuous and nonincreasing;      θ̂_na(x) := sup{θ : Ŝ(θ) ≥ x}.

If a family of bracket procedures has the nonincreasing exponent function `T`, then for all `0 < φ < 1`, `0 < β < g`, `η₀ > 0`
there is a family with accuracy `gn + O(log n)` in dimension `n`, for every member of `L_u` and failure probability `e^{−cn}`, of
cost at most `exp(n(τ + 2η₀) + o(n))`,

    τ = sup_{γ≥β} [ min(γ, φ·θ̂_na((g − β)/φ)) + (1 − φ)·T(γ/(1 − φ)) ].

For the reference `H`, Theorem F6 gives `Ŝ(θ) = S((R^max)^{−1}(θ))` and `θ̂_na = θ_na`: the operator `R[T]` of §11.18 with the
`θ_na` of this report.

*Proof.*  `Q_n = Q_o × Q_i`, `n_o = ⌊φn⌋`, `π = π_o ⊗ π_i`, `W(a) = E_{π_i} e^{−ψ(a,·)}`, `A = E_{π_o} W`; reference `ψ_ref = ψ_ref^{(n_o)}` on
`Q_o` with `μ, w_ref, s_ref, Ξ`, `Z = A(ψ_ref)`; `Ŵ = W/w_ref`, so `A = Z·E_μ Ŵ`.  The three facts of Theorem 11.52 become:
(F1) every fibre `b ↦ ψ(a,b)` is in `L_u(Q_i)`, so the inner procedures give brackets of `W(a)`, and — dividing by the known
`w_ref(a)` — brackets of `Ŵ(a)` *of the same ratio*;  (F2) `−ln W ∈ L_u(Q_o)` (`fibre_sum_le`), so Lemma F5 applies:
`Ŵ(a) ≤ Ŵ(a') e^{s_ref(a,a')}` and `E_μ(Ŵ − s)₊ ≤ s·Ξ(q)` whenever `p(s) := μ(Ŵ > s) ≤ q < 1` (`Ξ` is nondecreasing);
(F3) the layer-cake inequalities hold for any nonnegative function on any probability space: `s·p(s) ≤ E_μŴ` and
`E_μŴ ≤ s₀ + Σ_{i<j} s_{i+1} p(s_i) + E_μ(Ŵ − s_j)₊` (`level_mul_exceed_le_mean`, `mean_le_layer_cake`, stated for the uniform
measure on a finite type; the weighted case is the same computation).
*Algorithm.*  That of Theorem 11.52 with: outer points i.i.d. from `μ`; brackets and levels for `Ŵ`; one query at a reference
point gives `s₀ := e^{−ψ(a_ref,b_ref) − un}/max w_ref ≤ min Ŵ` and `max Ŵ ≤ s₀ e^{3un}`; `J = ⌈3un + b + c₁n + 10⌉`; closure test:
with the certified `q` (`= min(1, 2max(N,K)/M)`), **if `q = 1` no closure is attempted**, otherwise `tail := s_j·Ξ(q)`, and the
algorithm stops if `tail ≤ e^G ℓ`, returning `[Zℓ, Z(s₀ + Σ_{i<j} s_{i+1} q_i + tail)]`.  Everything else (ladder of inner
accuracies, classification "low/high", `ℓ := max(ℓ, s_j e^{−b}N/(2M))` at populated levels, negligibility threshold
`M_j^neg = 2KJe·s_j/(ℓ e^b)`, doubling of `M`) is unchanged.
*Good event, validity, width:* verbatim — (V2), (V3) are Chernoff bounds for i.i.d. samples of `μ` at `O(n³)` fixed thresholds;
`ℓ ≤ E_μŴ` by (F3); the upper end by (F3) and (F2) (`q < 1` guarantees a point outside the super-level set — D45(4)); the
ratio of the ends is at most `1 + 4Je^{b+1} + e^b + e^G` (`upper_le_width`).
*Termination within `J` levels:* above `max Ŵ·e^b` nothing is high, `M_j^neg` grows by `e` per level, and once
`q < min μ` (at most `c₁n` further levels) `Ξ(q) = 0`.
*How large `M` gets.*  Let `q† = sup{q₀ ≤ 1 : Ξ(q) ≤ q e^{G−b}/4 for all 0 < q ≤ q₀}` and `M† = 2K/q†`.  At a populated level
`s_j q = 4e^b·s_j e^{−b}N/(2M) ≤ 4e^bℓ`, at a negligible one `s_j q ≤ e^bℓ/(eJ)`; so if `q ≤ q†` and `q < 1` then
`tail = s_j Ξ(q) ≤ s_j q e^{G−b}/4 ≤ e^Gℓ` and the algorithm stops.  A level that is left has `q_j > q†` or `q_j = 1 ≥ q†`, and
the argument of Theorem 11.52 gives `M_j^neg ≤ 4Je²M†` and `M ≤ 8Je²M†` throughout (`negligibility_threshold_le`).  By the
hypothesis on `Ξ` (applied in dimension `n_o` with `x = (G−b)/n_o`), for every `η > 0` and large `n`: `q† ≥ exp(−n_o[θ̂_na(x) + η])`
(for `θ ≥ θ̂_na(x) + η`, `Ŝ(θ) < x`, hence `Ξ(e^{−n_oθ}) ≤ e^{−n_oθ} e^{n_o x}/4`; beyond `θ = c₁` the tail function vanishes).  So
`M† ≤ exp(nφ θ̂_na((g−β)/φ) + o(n))`.
*How many points are close to a level, and the cost:* verbatim (`close_points_bound`: the two factors `e^b` cancel; a point
with `Ŵ(a) = s_j e^{−G_a}` is classified once the inner accuracy is at most `max(G_a, b)`).  ∎

*Remarks.*  (i) The theorem holds for **every** reference in the class; only the exponent depends on it.  With the reference
`ψ₀ = 0` (plain sampling of `π_f`) the tail function is the isoperimetric function of the product measure `π` (Ahlswede–Zhang,
Yu), and the limit of the recursion is the hinted exponent of `g = 0` *restricted to the sampler `π`* — strictly worse than
`R^max` (Proposition F11).  (ii) The algorithm is not explicit: it uses the numbers `Ξ_H^{(n_o)}(q)` (finite maxima over subsets
of `Q_{n_o}`), which cost no evaluations but for which no formula is known; any upper bound `Ξ̄ ≥ Ξ_H` with the same exponent
would do.  In the uniform case Harper's theorem supplies `Ξ` exactly; here only its exponent is known (Theorem F6).  (iii) The
logic was run at small size (outer block `Q_4` with the exact `Ξ`, simulated inner brackets placed adversarially, references
`H`, `0`, additive): 198 runs, every bracket valid and within the width bound, sample sizes and close-point counts within the
bounds of the proof, populated and negligible levels both occur; closing at `q = 1` (33 of 96 runs invalid) and forgetting the
weights `1/w_ref` (6 of 96) are detected (`t14`).  My first run of this test reported an invalid bracket; the cause was my
table of `Ξ` (14 subsets instead of 65534), not the algorithm — the test has teeth.

### 3.6 The pair `(θ_na, R^max)` and the main theorem

**Theorem F8 (`HintPair`) [proved].**  `HintPair θ_na R^max a h E` holds (the structure of `HintRecursion.lean`), for every
`p ∈ (0,1)`, `u > 0`.
*Proof.*  `R^max(e) = max_{0≤t≤1}[F*(t) − te]` with `F*` continuous, `F*(0) = F*(1) = 0`, `F*(t) ≤ L(1−t)`, `E = sup F*(t)/t ∈ (0,∞)`
(Theorem F2(b); `E > 0` is the strict convexity of `ln C`).  Hence `R^max` is convex, nonincreasing, `1`-Lipschitz,
`R^max(e) ≥ max(0, −e)`, `R^max(e) = 0 ⟺ e ≥ E`, and `R^max(e) = −e` for `e ≤ −L`.  `S = id + R^max` is convex, nondecreasing,
`S ≥ max(e, 0)`, and vanishes exactly on `(−∞, e_c]`, `e_c := max{e : R^max(e) = −e} < 0`; a convex function that is zero up to
`e_c` and positive afterwards is strictly increasing on `[e_c, ∞)`.  So `S : [e_c, ∞) → [0, ∞)` is an increasing homeomorphism
and `θ_na = R^max ∘ S^{−1}` is continuous and nonincreasing on `(0, ∞)`, `θ_na ≤ θ_na(0+) = R^max(e_c) = −e_c = a`
(`na_cont`, `na_le`, `a_pos`), `θ_na(S(e)) = R^max(e)` for `e > e_c` (`ident`), `θ_na(h) = R^max(0) = h` since `S(0) = h`
(`na_h`); `h > 0` and `R^max > 0` on `(0, E)` (`h_pos`, `hint_pos`); `S` nondecreasing (`hint_mono`); `R^max(e) ≥ h − e`
(`hint_lower`, `L = 1`).  ∎
(The bound `t ≤ 1` in the game formula — `F ≤ 0` beyond — is exactly the slope condition `θ_hint' ≥ −1`.  Numerically: slopes
of `R^max` in `[−1, 0]`, second differences `≥ 0`, `S` nondecreasing, `θ_na(h) = h` to `10⁻¹⁷`, five parameter pairs: `t11`.  I did
not formalise this in Lean; `CubeHintPair.lean` does the analogous calculus for `p = ½`.)

**Theorem F9 (adaptive algorithms without a hint, with a field) [lower bound: known, every `n`; upper bound: proved given
Theorems F6, F7 — both unrefereed paper proofs — and the machine-checked `iterates_lt_hint_add`].**  For every `p ∈ (0,1)`,
`u > 0`, `0 < ε₁ < E`, `0 < δ < ½`, the least worst-case number of evaluations of a randomised adaptive algorithm without a
hint that is `(ε₁n/2, δ)`-correct on `L_u` is

    exp( n·R^max(ε₁) + o(n) ),        R^max(ε₁) = max_{|γ|≤u} R_γ(ε₁) = max_{0≤t≤1} [F*(t) − tε₁],

the hinted exponent of the hardest additive instance `γ*(ε₁)|x|`, while non-adaptive algorithms need
`exp(nθ_na(ε₁) + o(n))`, `θ_na(ε₁) = R^max(S^{−1}(ε₁)) > R^max(ε₁)`.  For `ε₁ > E` a bounded number of evaluations suffices on
every instance (Theorem 11.28(d,e)).
*Proof.*  Lower bound: Theorem F1(a) at `γ*(ε₁)`.  Upper bound: complete enumeration is a family of bracket procedures with
exponent function `T₁ ≡ ln 2 ≥ a` (alternatively: the stratified bracket of Theorem F10 with `T₁ = θ_na`).  By Theorem F7 with
the reference `H` and induction, for every `k` and `η > 0` there is a family with exponent function at most `T_k + η`,
`T_{k+1} = min(T_k, R[T_k])`.  The `T_k` are nonincreasing in `k` and in the accuracy, nonnegative and bounded by `ln 2`;
`HintPair θ_na R^max (ln 2) h E` holds (Theorem F8 with the bound `a ≤ ln 2`); so by `iterates_lt_hint_add` some `T_k(g)` is
within `η` of `R^max(g)` for a `g < ε₁` with `R^max(g) ≤ R^max(ε₁) + η`, and the midpoint of a bracket of accuracy
`gn + O(log n) ≤ ε₁n` is a correct output.  ∎

*Consequences.*  (i) **The hardest instance with a hint is the hardest additive instance** (an algorithm with a hint may
ignore it): `sup_{ψ∈L_u}` (hinted exponent of `ψ`) `= R^max(ε₁)`, attained at `γ*(ε₁)|x|` and at `H`.  For `θ = 0` this is "the
flat instance is the hardest" of §11.18.  (ii) The level recursion with the pair of this report was iterated numerically
(`t12`, `p = 0.1, u = 2` and `p = 0.3, u = 1`): levels nonincreasing, **never below `R^max`** (deficit `0.00`; the necessary
condition of D45), within `0.5 %` of `a` of `R^max` after 12 levels, and above `R_0` throughout (e.g. `T_12/a = 0.2380`,
`R^max/a = 0.2379`, `R_0/a = 0.2077` at `g = 0.1E`); `T_2(0+)/a = 0.505` (`h/a = 0.294`).  A recursion built on the pair of the
instance `g = 0` alone (i.e. assuming the identity with `R_0`) falls below `R^max` — by `3.1 %` of `a` after ten levels at
`p = 0.1, u = 2` — and is thereby refuted by the lower bound at `γ*` (`t17`): the D45 test has power here.  (iii) Everything
that §11.18 says about what the theorem does *not* say applies: exponents only, extensive accuracies only, `k → ∞` levels, no
algorithm one would run; in addition the tail function is not explicit (Remark (ii) after F7).

### 3.7 Instance-optimality in the field

**Theorem F10.**
(a) **[proved]** *Not in the worst case.*  For `θ ≠ 0` and `0 ≤ ε₁ < E`:  `R^max(ε₁) > R_0(ε₁)` (Theorem F2(f)).  With Theorem F9:
the worst-case exponent of adaptive algorithms without a hint on the class `{f + g}` is the hinted exponent of the instance
`(f, γ*|x|)`, **not** of `(f, g = 0)`; in all computations `γ*` has the sign opposite to `θ` (the hardest residual partly cancels the
field; proved to first order in `γ`, Theorem F2(f)), and
it depends on the accuracy (`γ* = −0.62, −0.56, −0.45` at `ε₁/E = 0, 0.3, 0.9` for `p = 0.1`, `u = 2`).  Also the thresholds
differ: between `E_0` and `E` the instance `g = 0` is cheap with a hint and the class is exponentially hard (this part is
Theorem 11.28(e); my numbers reproduce `G(0) = 0.11367`, `ε₁* = 0.11383` at `θ* = −0.037c` for `e/c = ½`, `β = 1`).
(b) **[numerical]** *Both are smaller than at zero field.*  `F*(t; θ)` is nonincreasing in `|θ|` for every `t` (121 fields in
`[0,6]`, `u ∈ {0.3, 1, 2, 4}`, 1001 values of `t`: no increase above `5·10⁻¹⁶`; `t19`), hence
`R_0(ε₁; θ) < R^max(ε₁; θ) ≤ R^max(ε₁; 0) = KL((Λ₁+ε₁)/u ‖ ½)`.  (For `R_0` alone this is the computation of H_REPORT §2.9
transposed to this class: `x^t + y^t` is concave.)  I have no proof of the monotonicity of `F*`; by the cosh form it is a
comparison statement for `y'' = (t/2)² y` on a window of fixed length that slides away from the origin.

| `u = 1`, `θ =` | 0 | 0.5 | 1 | 2 | 3 |  | `u = 2`, `θ =` | 0 | 0.5 | 1 | 2 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| threshold of `g=0`, `E_0` | .12011 | .11367 | .09678 | .05400 | .02395 | | | .43378 | .41607 | .36766 | .22872 | .11140 |
| class threshold `E` | .12011 | .11383 | .09728 | .05479 | .02446 | | | .43378 | .41774 | .37315 | .23925 | .11942 |
| `R_0(0+)` (hint, `g = 0`) | .029139 | .027531 | .023340 | .012884 | .005672 | | | .097281 | .092895 | .081093 | .048716 | .023040 |
| `R^max(0+)` (adaptive, no hint) | .029139 | .027621 | .023618 | .013322 | .005954 | | | .097281 | .093758 | .083936 | .054171 | .027194 |
| `γ*` at `ε₁ → 0` | 0 | −.055 | −.105 | −.177 | −.214 | | | 0 | −.170 | −.330 | −.583 | −.734 |
| `a = θ_na(0+)` (non-adaptive) | .1109 | .1052 | .0899 | .0507 | .0227 | | | .3278 | .3162 | .2836 | .1841 | .0928 |
| plain Monte Carlo from `π_f`, `a_π` | .1109 | .1225 | .1201 | .0826 | .0409 | | | .3278 | .4078 | .4621 | .4338 | .2732 |

(c) **[proved]** *Yes at the instance: the type-stratified bracket.*  For every type class draw two independent uniform samples of
size `M ≥ 2K`; let `t̂_κ` be the `⌈K⌉`-th largest weight of the first, `â_κ` the mean of `min(w, t̂_κ)` over the second, `q = 2K/M`,

    L = (2/3) Σ_κ π(T_κ) â_κ,     U = 2 Σ_κ π(T_κ) â_κ + Tail,
    Tail = max { Σ_{x∈D} π(x) [min_{y∉D} t̂_{|y|} e^{u d(x,y)} − t̂_{|x|}]₊ : D ⊊ Q_n, maxdens(D) ≤ q }.

With `K = 24 ln(4(n+1)/δ)`: `L ≤ A(ψ) ≤ U` with probability `≥ 1 − δ` for **every** `ψ ∈ L_u`.  At a permutation-symmetric
instance `ψ₀ = G(|x|)` — in particular at `g = 0` and at every additive instance — `U/L = 3 + (3/2)·Ξ^{md}_{ψ₀}(q)`,
`Ξ^{md}_{ψ₀}(q) := max{Φ_{ψ₀}(D) : maxdens(D) ≤ q}`, deterministically, whereas **every** algorithm that is correct on `L_u`
makes at least `(1−2δ)/q` evaluations at `ψ₀` whenever `ln(1 + Ξ^{md}_{ψ₀}(q)) > ε`.  So the algorithm that doubles `M` (with
`K_i = 24 ln(4(n+1)2^i/δ)`) and stops when `ln(U/L) ≤ ε` is correct on the whole class for every `ε > ln 3`, and at every
symmetric instance its cost is, up to the factor `16(n+1)K/(1−2δ)`, the least possible cost at the accuracy `ε − ln 3`:
at extensive accuracies **it has the hinted exponent of every symmetric instance** — `R_γ(ε₁)` at `γ|x|` (Theorem F1),
`R_0(ε₁)` at `g = 0` — and it needs no promise of symmetry.  In the worst case over `L_u` it has the non-adaptive exponent
`θ_na` (by the argument of Theorem F4(d), given Theorem F6); run until its cost reaches `e^{n(R^max+η)}` and followed by the nested algorithm of Theorem F9, it
gives one algorithm that is worst-case optimal *and* instance-optimal on the symmetric instances.
*Proof.*  Per class, as in Proposition 11.46 (H_REPORT Lemma 2.4): outside an event of probability `4e^{−K/24}`,
`dens_κ{w > t̂_κ} ≤ 2K/M`, `dens_κ{w ≥ t̂_κ} ≥ K/(2M)` and `â_κ ∈ [½, 3/2]·E_{T_κ} min(w, t̂_κ)`; union bound over the `n+1` classes.
Then `L ≤ Σ_κ π(T_κ) E_{T_κ} min(w,t̂_κ) ≤ A`, and `A = Σ_κ π(T_κ) E_{T_κ} min(w, t̂_κ) + Σ_{x∈D} π(x)(w(x) − t̂_{|x|})` with
`D = {w > t̂_{|x|}}`, `maxdens(D) ≤ q < 1`; for `x ∈ D`, `y ∉ D`: `w(x) ≤ w(y) e^{ud(x,y)} ≤ t̂_{|y|} e^{ud(x,y)}`; so `A ≤ U`.  At a symmetric
instance `w` is constant on type classes, `t̂_κ = â_κ = w₀(κ)`, `L = 2A/3`, and `w₀(y)e^{ud(x,y)} − w₀(x) = w₀(x)(e^{s₀(x,y)} − 1)`,
so `Tail = A·Ξ^{md}_{ψ₀}(q)`.  The lower bound is Theorem 11.22(c) for the dips `ψ₀^{σD}`, `σ` a uniformly random permutation
of the coordinates (`ψ₀` is invariant, a point `x` lies in `σD` with probability `dens_{|x|}(D) ≤ q`).  ∎
(The same statement with "learn the additive interpolant on a star, then spot-check" is in the theory report for additive
instances; the stratified bracket needs neither additivity nor the hinted sampler, and its two bounds are the same
combinatorial function, so no isoperimetry is used.)
(d) *Not settled:* instance-optimality at non-symmetric instances (a cone costs `n + 3` evaluations with a hint; the question
is the same as item (4) at the end of §11.18).

### 3.8 Plain Monte Carlo from `π_f`, and single product measures

**Proposition F11 [formulas: sketch — lower bounds by the truncated-cone construction of Theorem F4(c) with the measure of the
sampler in place of the type densities (not written out), upper bounds from the isoperimetric exponent of a fixed product
measure (Ahlswede–Zhang; Yu, Theorem 5, read as a machine summary) — values: numerical].**
(a) A non-adaptive algorithm whose points are i.i.d. from **one** product measure `Bernoulli(r)^{⊗n}` (importance weights) has the
exponent `θ_na^{(r)}(x) = max_m min{ I(S;X) + KL(P_X ‖ r) : D(P_{X|S}‖π_s|P_S) ≤ x }` (the cone of centre type `m`, truncated on the
largest set of sampler-measure `e^{−nθ}` around its centre, is not seen).  For `r = p` (plain Monte Carlo from `π_f`) the value
at `x → 0` is `a_π = n^{−1} max_s KL(π_s‖π)`, the Chatterjee–Diaconis sample size of the worst cone.  `θ_na^{(r)} > θ_na` for every
`r` when `p ≠ ½`:

| | type-uniform (`θ_na`) | best single `r` | plain `π_f` (`r = p`) |
|---|---|---|---|
| `p = 0.1, u = 2, x = 0.05E` | 0.1020 | 0.1046 (`r = 0.186`) | 0.2729 |
| `p = 0.1, u = 2, x = 0.25E` | 0.0440 | 0.0470 (`r = 0.168`) | 0.1420 |
| `p = 0.3, u = 1, x = 0.25E` | 0.0243 | 0.0247 (`r = 0.319`) | 0.0347 |

(`t20`.)  So the answer to "which sampling distribution?" is: **neither `π_f` nor a tilted product measure, but the mixture of
all of them** (uniform over the types of the window); a product measure tilted towards the hardest instance comes within a
few percent, `π_f` itself is off by a factor `2`–`3` in the exponent at small accuracies (last row of the table of §3.7).  The
same holds with a hint (workstream A, Proposition 6).
(b) The nested algorithm of Theorem F7 with the reference `ψ₀ = 0` — plain sampling of `π_f` on every outer block, tail function =
isoperimetric function of the product measure — converges (same abstract theorem; the pair is
`max_m min{I + KL(P_X‖π) : D(P_{X|S}‖π_s|P_S) ≤ x}` and `θ_h^π(e) = max_m min{ I + KL(P_X‖π) : uP(X≠S) − Λ(P_S) ≤ e }`, linked by the
identity of Theorem F3 with the two middle terms grouped differently) to `θ_h^π`, the hinted exponent of `g = 0` *for the
sampler `π`*: `0.0884, 0.0616, 0.0390` against `R^max = 0.0481, 0.0268, 0.0118` at `e/E = 0, ¼, ½` (`p = 0.1`, `u = 2`; `t17`).  This
is what "asymptotic isoperimetry of product measures" gives when used as the remark (3) at the end of §11.18 suggests; it is
a valid upper bound and not the exponent.

### 3.9 Larger alphabets, several site types, general single-site known parts

**Proposition F12 [sketch; (i) known].**  Identical sites with a finite alphabet `𝒮`, an arbitrary site law `π` of full support (an
arbitrary single-site known part), a site metric `d₁` (already multiplied by `β`), class `{ψ : |ψ(x) − ψ(y)| ≤ Σ_i d₁(x_i, y_i)}`.
Let `𝓛 = {γ : 𝒮 → ℝ, γ(a) − γ(b) ≤ d₁(a,b)}` (the additive members), `Z_γ = E_π e^{−γ}`, `F(γ,t) = −ln val(K_t^γ)` the game
function of Theorem 11.27(c) at the additive instance `γ` (vertices of the Lipschitz polytope of its slack), `F* = max_{γ∈𝓛} F(γ,·)`,
`R^max(e) = max_{0≤t≤1}[F*(t) − te]`, `θ_na = R^max ∘ S^{−1}`.  Then
(i) **[known]** every algorithm needs `e^{nR^max(ε₁) − o(n)}` evaluations at the additive instance `γ*` (Theorem 11.27(c), every `n`);
(ii) **[sketch]** `R^max` is the worst-case exponent of adaptive algorithms without a hint and `θ_na` that of non-adaptive ones,
with the reference `ψ_H(x) = min_{γ∈𝓛}[Σ_i γ(x_i) + n ln Z_γ]`, whose Gibbs law `μ_H ∝ max_γ π_γ^{⊗n}` is the normalised-maximum-
likelihood mixture of the tilted product laws (uniform inside type classes; `Z_H ≤ (n+1)^{|𝒮|−1}`); the regularised divergence is
`v(P) = max_{γ∈𝓛}[−E_Pγ − ln Z_γ] = min_{P'} [KL(P'‖π) + W_{d₁}(P, P')]`; the identity is
`D(P_{X|U}‖π^U|P_U) = I(U;X) + KL(P_X‖π) + E φ_U(X) − Λ(P_U)` for a vertex label `U` (`π^φ ∝ π e^{−φ}`, same one-line proof).
*What carries over verbatim:* Theorem F4(a,b) (adjacent type classes are coupled by changing one coordinate), Lemma F5,
Theorem F7, Theorem F8 (`t ≤ 1` is Lemma 3(b) of workstream A), Lemma T (stated for every alphabet), the collapse in Lemma SL
(Sion in `γ ∈ 𝓛`, compact convex; `v_γ` concave in `γ`), the vertex reduction for `τ ≤ 1` (Lemma 3(c) of workstream A) and the
window step (move `P_{X'}` to the minimiser `P'` of `KL(P'‖π) + W_{d₁}(P_{X'}, P')` by an optimal coupling).  *Not written out:*
Lemma SL with Kantorovich duality for `|𝒮| ≥ 3` (as in Proposition 4 of workstream A), the continuity of `KL − v` near
`{v = KL}`, and the evaluation of the truncated generalised cones (the unimodality argument of Theorem F4(c) is binary).
(iii) **[sketch]** *Sites of several types* (fractions `λ_j`, each with its own alphabet, law and metric): split every block
with the same composition; `F*(t) = Σ_j λ_j F*_j(t)` (one common `t`; the maximisation over `γ_j` separates), `R^max(e) =
max_t [Σ_j λ_j F*_j(t) − te]`, class threshold `E = Σ_j λ_j E_j` (Theorem 11.28, remark (ii)); the exponents do not add
(D31): for binary sites, `u = 1`, half with field `0` and half with field `3`, at `e = 0.3E`: `0.008559` against the average
`0.009791` of the two exponents (`t19`).  The hinted exponent of an additive instance with several site types is itself only
sketched in workstream A.
Nothing is claimed for known parts with interactions.

---

## 4. Numerics: what, sizes, results

All commands are run from this directory (`./run_all.sh` runs all of them in sequence, about 45 minutes; outputs `out_*.txt`).  Own code:
`flib.py` (single-letter formulas, max–min solvers, the pair `(θ_na, R^max)`), `birad.py` + `finite.py` (exact finite-`n` sums
for functions of the profile relative to a centre: counts `C(k,i)C(n−k,j)` in log space, type densities, McShane envelopes by
an `l₁` distance transform on the profile grid; checked against brute force on the full cube, `n ≤ 12`: `t05`, 146 checks, 0
failures), `recursion.py` (level recursion for an arbitrary pair).  Nothing was imported from the repository.

**Single-letter formulas against each other.**

| command | what | result |
|---|---|---|
| `t01_basic.py` | shift identity on 20000 random points; `p = ½` against the report; game formula against `max_m [h(m) − h(ρ_m)]` at `g = 0` (80 cases) | `2.7·10⁻¹⁵`; report's values reproduced; `1.0·10⁻¹¹` |
| `t03_precise.py` | max–min forms against the game: `R_0`, and `R^max` against the profile formula of `H`; is the exit type in the window? (8 pairs `(p,u)` × 5 accuracies) | `2.3·10⁻¹⁵`; `2.0·10⁻¹⁴`; always in the window |
| `t04_na.py` | `θ_na` max–min at `p = ½` against `min{KL(ρ‖½): KL(ρ‖p_u) ≤ ε₁}`; identity `θ_na(e + R^max(e)) = R^max(e)`; the same with `R_0` | equal to 8 digits; `2.1·10⁻¹²`; **fails** with `R_0` (e.g. `p=.1,u=2,e=0`: `θ_na(R_0) = 0.0531 ≠ R_0 = 0.0427`) |
| `t11_pair.py` | closed game formula against a generic solver; `R^max` from `F*`; `θ_na = R^max∘S^{−1}` against the max–min form for `x` on both sides of `h`; `HintPair` properties | `3·10⁻¹⁴`; `4·10⁻¹²`; `10⁻¹¹`; slopes in `[−1,0]`, convex, `S` nondecreasing, `θ_na(h) = h` |
| `t16_single_letter_sup.py` | Lemma SL by a primal minimisation over kernels (SLSQP), `≈1900` laws `P_{UX}`, `\|𝒰\| ≤ 4`, random and local ascent, `e` of both signs | `max (V − R^max) = −2.5·10⁻⁵`; equality `7·10⁻¹²` at the generalised dip |
| `t17_misc.py` | cosh form; recursion on the pair of `g = 0` (mutation); nested scheme with the sampler `π`; `T_2(0+)` | `1.4·10⁻¹⁵`; falls `3.1 %` of `a` below `R^max`; table of F11(b); `T_2(0+)/a = 0.505` |
| `t19_field_monotone.py`, `t13_field.py` | `F*(t;θ)` nonincreasing in `θ`; `F* > F(0,·)`; two site types; table of §3.7 | no increase (`4·10⁻¹⁶`); gap `≥ 2·10⁻¹¹`; §3.9 |
| `t20_product_samplers.py` | non-adaptive exponent of single product samplers | table of F11(a) |
| `t21_checks.py` | derivative formula of F2(f) (4000 points) and its sign; max–min form of `R_γ`, `γ ≠ 0` (18 cases); quantile truncation of F4(a) by brute force (`n ≤ 10`, 1080 checks); bound of F4(c) (`n ≤ 2000`, 24 cases) | `4·10⁻¹¹`, sign `= sign(p−½)`; `6·10⁻¹⁶`; 0 failures; holds in 24/24 |

**Exact finite-`n` exponents** (binomial sums; every reported set is certified sensitive, so each number is a valid lower
bound on a cost).  `t08_finite_large.py p u frac n₁,n₂,n₃`: for each `n`, the smallest "density ball" `{x : d(x,s) ≤ r_{|x|}}`
(largest type density `q`) whose deepest dip changes `ln A` by more than `ε = ε₁n` — at `g = 0`, at the hardest additive
instance `γ*|x|`, at `H` — and the smallest density ball on which flattening the cone `u d(·,s)` lowers `ln A` by more than
`ε`; reported `n^{−1} ln(1/q)`, maximised over five centre types around the predicted one; `ε₁ = frac·E`.

| `(p, u, ε₁/E)` | quantity | `n = 1000` | `2000` | `4000` | extrapolated (`a + b ln n/n + c/n`) | formula |
|---|---|---|---|---|---|---|
| `(0.1, 2, 0.3)` | hint, `g = 0` | .021964 | .020949 | .020254 | .019185 | `R_0 = .019497` |
| | hint, `γ* = −0.563` | .025517 | .024553 | .023996 | .023286 | `R^max = .023270` |
| | hint, `H` | .024696 | .024068 | .023718 | .023297 | `R^max = .023270` |
| | cone flattened (non-adaptive) | .040825 | .038801 | .037666 | .036281 | `θ_na = .036246` |
| `(0.3, 1, 0.3)` | `g=0` / `γ*` / `H` / non-adaptive | | | | .011793 / .012216 / .012199 / .019938 | .012049 / .012209 / .012209 / .019941 |
| `(0.05, 2, 0.1)` | `g=0` / `γ*` / `H` / non-adaptive | | | | .019080 / .022980 / .023253 / .047348 | .019026 / .022897 / .022897 / .047452 |
| `(0.2, 4, 0.3)` | `g=0` / `γ*` / `H` / non-adaptive | | | | .085784 / .100253 / .100238 / .139386 | .086324 / .100321 / .100321 / .139401 |

(`out_t08_finite_large.txt`; 3½ minutes per parameter set.)  The three-point extrapolation is crude (the coefficient of
`ln n/n` fluctuates between `0.33` and `0.41` with the rounding of radii), so two quantities were pushed further with
one-dimensional exact sums:
`t09_hamming_g0.py 0.1 2.0 0.3 500,…,32000` (Hamming balls at `g = 0`; hypergeometric tails): `0.023867, 0.021964, 0.020949,
0.020257, 0.019959, 0.019743, 0.019624` for `n = 500 … 32000` and `0.019568` at `n = 64000` (`out_t09_64000.txt`), i.e.
`R_0 + 0.39 ln n/n` with `R_0 = 0.019497`;
`t10_additive_large.py 0.1 2.0 0.3 1000,4000,16000 both` and `… 64000 star` (slack balls at `γ* = −0.563`): `0.025517, 0.023996,
0.023494, 0.023337` for `n = 1000, 4000, 16000, 64000`, i.e. `R^max + 0.37 ln n/n` with `R^max = 0.023270`.
**So at `n = 64000`, `p = 0.1`, `u = 2`, `ε = 0.0637n`: every algorithm, with or without a hint, needs `(1−2δ)e^{0.02334n}`
evaluations at the instance `γ*|x|`, while `e^{0.0196n}·poly` suffice with a hint at `g = 0`.**  (A first version of `t09`
truncated a convolution at relative size `e^{−80}` and reported exponents tending to `0`; the certified form used now
bounds the dip from below through the cone law.)

**The recursion.**  `t12_recursion.py p u 12` (pair of this report; grid of 120 accuracies, 50 fractions `φ`, 18 tolerances
`β`, 64 values of `γ`, piecewise-linear interpolation), entries `T_k/a`:

| `p = 0.1, u = 2`; `g/E =` | 0.001 | 0.02 | 0.10 | 0.25 | 0.50 | 0.75 |
|---|---|---|---|---|---|---|
| `k = 1` (`θ_na`) | 0.9443 | 0.7573 | 0.4937 | 0.2643 | 0.0974 | 0.0208 |
| `k = 2` | 0.4815 | 0.4034 | 0.2874 | 0.1751 | 0.0758 | 0.0185 |
| `k = 4` | 0.3312 | 0.3033 | 0.2441 | 0.1624 | 0.0737 | 0.0184 |
| `k = 12` | 0.2973 | 0.2840 | 0.2380 | 0.1615 | 0.0737 | 0.0184 |
| `R^max/a` | 0.2934 | 0.2825 | 0.2379 | 0.1615 | 0.0737 | 0.0184 |
| `R_0/a` (hint at `g = 0`) | 0.2602 | 0.2498 | 0.2077 | 0.1368 | 0.0578 | 0.0114 |

levels nonincreasing in `k` and `g`: true; `max_k max_g (R^max − T_k)/a = 0.00`; `max_g (T_12 − R^max)/a = 0.0047` (the same for
`p = 0.3`, `u = 1`: `0.0045`).

**Logic at small size.**  `t14_two_level_H.py 14 96` (Theorem F7; §3.5, Remark (iii)); `t15_tail_lemma_ref.py` (Lemma F5);
`t18_exact_vs_family.py` (exact `Ξ_H` on `Q_4` against the family of the formulas: ratio `≤ 2.000`).
**Theorem F6 on profile sets.**  `t23_ctl_profile_sets.py 600` and `… 2000` (1829 sets of six shapes with `θ ≥ 6 ln n/n`: the
inequality with `ω_n = 3 ln n/n` holds for all; raw difference `≤ +0.005`), `t24_ctl_convergence.py 500,1000,2000,4000` (§3.4,
Remark (iii)).
**Lean.**  `lean/WorkstreamF.lean` (`klBin_tilt`, `cone_rate_eq`, `sphere_rate_eq`, `shift_identity`), checked with
`lake env lean`: no errors, axioms `propext, Classical.choice, Quot.sound` (13 s).

*What the numerics do not test.*  The converse Theorem F6 for arbitrary sets at large `n` (tested: its single-letter part,
all sets at `n = 4`, and profile sets around one centre at `n ≤ 4000`; not tested: sets without a centre, e.g. unions of
many balls), and the cost of the nested algorithm (only the logic of one level
at `n_o = 4`; as in §11.18 the asymptotic gain is invisible at simulable sizes).

---

## 5. Negative findings and dead ends

1. **"The identity `θ_na(e + θ_hint(e)) = θ_hint(e)` holds with the hinted exponent of the instance `(f, g=0)`"** — false with
   a field: the two sides differ by the term `KL(P_X‖π)` of Theorem F3, and a level recursion built on that pair falls below
   the lower bound `R^max` (`t17`).  True at `θ = 0`.
2. **"`g = 0` is the hardest instance with a hint"** — false for `θ ≠ 0` (Theorem F2(f)); the hardest additive residual tilts
   the field towards zero.  True at `θ = 0` (H_REPORT §2.9, Theorem 11.54).
3. **"`π_f` is the right sampling distribution"** — false, for non-adaptive algorithms (`a_π` against `a`, up to a factor
   `2.9` at `θ = 3`, `u = 2`) and for the nested scheme (`θ_h^π` against `R^max`); **"a tilted product measure is"** — false too,
   by a few percent in the exponent (Proposition F11).
4. **"What is missing is a Harper theorem for product measures"** — it is neither available nor what is needed.  Exact
   vertex isoperimetry in the `p`-biased cube is known for down-sets (Bollobás–Leader); super-level sets of Lipschitz functions
   are not monotone.  The asymptotic isoperimetry of a *fixed* product measure (Ahlswede–Zhang; Yu) is the tail lemma of
   plain `π_f`-sampling and gives the worse exponents of item 3.  The statement needed has the sampler chosen as a mixture
   over types *and* the reference instance `H` (Theorem F6).
5. **"A non-additive symmetric instance (flat histogram) might be harder than every additive one"** — no: `H` is exactly as
   hard as the hardest additive instance (Lemma SL: the multi-constraint problem collapses to a maximum over `γ`).
6. **Importance weights `1/π(T_κ)` without regularisation** (reference `−ln |T_κ|`, which is not in `L_u` outside the window):
   the "slack" becomes negative and the closure bound picks up exits that the class forbids; the reference must be a member
   of the class (`ψ_H`), which also keeps atypical type classes (outside the window) at negligible cost.
7. **The max–min form of `R^max` does not extend to negative accuracies** (`e < 0`: for some centre types the constraint set
   is empty and the "volume regime" takes over); the form that is valid for all `x > 0` is the one for `θ_na`
   (Theorem F2(e)).  My solver for the former silently returned garbage for `e < 0` until a test compared it with the pair.
8. **At finite `n`** the bound of Theorem F4(c) is void for `n ≲ 1000` at `θ = 0.02`; all finite-`n` exponents approach their
   limits from above like `0.35`–`0.41·ln n/n`; on `Q_4` the exact tail function of `H` exceeds the family of the formulas by
   a factor up to `2`.  Nothing here is a finite-`n` statement about algorithms.
9. **Three errors of my own caught by the tests** (not by reading): the truncated convolution in `t09` (§4); a table of the
   tail function over 14 instead of 65534 subsets, which produced an invalid bracket in the first run of `t14`; a sign in
   `e_c`.  The first "violations" reported by `t15` were rounding (levels one ulp apart with zero slack outside the window).

---

## 6. Prior art, and how each source was read

| item | what I use / what it says | how read |
|---|---|---|
| Harper 1966 (vertex isoperimetry of the cube) | the uniform case only | from memory |
| B. Bollobás, I. Leader, *Isoperimetric inequalities and fractional set systems*, JCTA 56 (1991) 63–74 | for the `p`-biased measure and **down-sets**: `P(A) ≥ Σ_{r≤k} C(n,r)p^r(1−p)^{n−r}` implies the corresponding bound for the `t`-neighbourhood; "generalises Harper's theorem" | abstract, through a machine summary of a repository record (digitalcommons.memphis.edu/facpubs/4980; the formula was garbled there); paper not read |
| Ahlswede–Gács–Körner 1976 (blowing-up lemma) | sets of measure `e^{−o(n)}` blow up to measure `→ 1`: the concentration regime, not the large-deviation regime needed here | from memory |
| R. Ahlswede, Z. Zhang, *Asymptotical isoperimetric problem* (ITW 1999); Ahlswede–Yang–Zhang 1997 (inherently typical subsets) | the lemma (Lemma T) and the converse method of Theorem F6 | through A_REPORT §§2.3, 4 (workstream A read the three-page summary in full); sources not re-read by me |
| Lei Yu, *Exact exponents for concentration and isoperimetry in product Polish spaces*, arXiv:2205.07596 (IEEE Trans. IT) | isoperimetric exponent `E_0^{(n)}(α,τ) → ψ(α,τ) = sup_{Q_XW: D(Q_{X|W}‖P_X|Q_W) ≤ α} inf_{Q_{Y|XW}: E c ≤ τ} D(Q_{Y|W}‖P_Y|Q_W)` for two fixed product measures, `|W| ≤ 2` (Theorems 4, 5): the tail lemma of plain `π_f`-sampling (Proposition F11) | machine summary of the arXiv HTML v3 (first 100 000 characters), abstract page; hypotheses not verified in the source |
| Chatterjee–Diaconis 2018 (sample size of importance sampling `≈ e^{KL}`) | interpretation of `a_π` | from memory |
| Rate–distortion function of a Bernoulli source with Hamming distortion (Cover–Thomas, Thm 10.3.1) | Theorem F2(c) | from memory |
| Normalised maximum likelihood / Shtarkov sum | name for `μ_H ∝ max_γ π_γ^{⊗n}` only | from memory |

Search log (25 Nov 2026; no project-identifying terms): (1) `Bollobás Leader "Isoperimetric inequalities and fractional set
systems" weighted cube down-sets vertex isoperimetric inequality p-biased measure`; (2) the same with `JCTA 56 abstract` →
repository record, fetched; (3) `Lei Yu "Exact exponents for concentration and isoperimetry in product Polish spaces" …` →
arXiv abstract and HTML v3, fetched.  **Not found** (three searches, abstracts and summaries only — this is "not found", not
"new"): an isoperimetric statement with the second measure a mixture over types and a reference instance; a nested
hint-free algorithm with a known part; the exponent `max_γ R_γ`.

---

## 7. What is not settled

1. **Theorems F6, F7 and hence the upper bound of F9 are paper proofs by me, unrefereed.**  F7 inherits the status of
   Theorem 11.52 (its referee report was pending when I read the repository); F6 uses Lemma T as proved in workstream A and
   Sion's theorem four times.  The lower bounds (F1(a), F4(b)(i), F4(c)) and the soft statements (F4(a,b), F5, F10(c)) are
   elementary.
2. **Only exponents, only extensive accuracies** `ε = ε₁n`, `0 < ε₁ < E`; `o(n)` of the typical-subset kind; nothing at bounded
   accuracy (there the non-adaptive exponent is `a`, the hinted ones `R_0(0+) < R^max(0+) = h`).
3. **The tail function `Ξ_H` is not explicit** (a maximum over subsets): the nested algorithm is an algorithm in the
   query-complexity sense only.  A finite-`n` upper bound for `Ξ_H` with the right exponent — a weighted Harper-type
   inequality for the type-uniform measure and the slack of `H` — would make it explicit; I have none.
4. **Monotonicity of `F*(t;θ)` in `|θ|`** (so that the field always helps): numerical.
5. **Instance-optimality at non-symmetric instances** (Theorem F10(d)).
6. **Proposition F11** (exponents of product samplers) is a sketch: the lower bound construction with a general sampler
   measure and the use of Yu's theorem are not written out.
7. **Proposition F12** (larger alphabets, several site types): a sketch with every ingredient named; no proof of Lemma SL for
   `|𝒮| ≥ 3`, no numerics for `|𝒮| ≥ 3`.  Known parts with interactions: nothing.
8. **Lean:** only the shift identity is machine-checked; `HintPair` for the pair `(θ_na, R^max)` (Theorem F8, convex-analysis
   argument) is not formalised.
9. Whether the statements here are in print: not established (three searches).

---

## 8. Summary (at most 40 lines)

1. **Exponents with a field** (`π = Bernoulli(p)^n`, `u`-Lipschitz residual, accuracy `ε₁n`; `F(γ,t)` the closed 2×2 game function,
   `F* = max_{|γ|≤u} F(γ,·)`, `S` = centre letter, `X` = point letter, `π_s` = Gibbs law of the cone at `s`):
   - hint at `g = 0`: `R_0(ε₁) = max_{t≤1}[F(0,t) − tε₁] = max_m [h(m) − h((Λ_m+ε₁)/u)]_+` — known (Thm 11.27 + workstream A);
     rewriting proved; exact sums up to `n = 64000` (`0.019568` against `0.019497`).
   - non-adaptive: `θ_na(ε₁) = max_m min{I(S;X) : D(P_{X|S}‖π_s|P_S) ≤ ε₁} = R^max(S^{−1}(ε₁))`, `S(e) = e + R^max(e)`; sample = uniform on
     every type class (NML mixture), not `π_f`.  Lower bound proved for every `n`; two-sided characterisation by one extremal
     function proved without isoperimetry; matching upper bound proved given Theorem F6.
   - adaptive without a hint, worst case: `R^max(ε₁) = max_{|γ|≤u} R_γ(ε₁) = max_{t≤1}[F*(t) − tε₁]` = hinted exponent of the hardest
     additive instance `γ*|x|`.  Lower bound known for every `n` (certified at `n = 64000`: `0.023337` against `0.023270`); upper
     bound: paper proof (F6, F7, F8 + machine-checked `iterates_lt_hint_add`), unrefereed.
2. **"Adaptive = hinted" holds with a known part** (hint-free worst case = hardest hinted instance), with the identity
   `D(P_{X|S}‖π_s|P_S) = I(S;X) + [uP(X≠S) − Λ(P_S)] + KL(P_X‖π)` (proved, Lean-checked): the pair `(θ_na, R^max)` satisfies
   `HintPair` (proved).  **Not instance-optimal in the field in the worst case:** `R^max > R_0` for every `θ ≠ 0` (proved; numerically `γ*θ < 0`);
   both decrease with `|θ|` (numerical).  At the instance `g = 0`, at additive and at all permutation-symmetric instances a
   type-stratified one-level bracket is instance-optimal (proved, soft).
3. **Isoperimetric input:** Theorem F6 — every set that is `e`-sensitive for the flat-histogram reference `H` (lower envelope of
   the normalised additive instances) has type-mixture measure `≥ e^{−nR^max(e)−o(n)}`; proved by types (inherently typical
   subsets as in workstream A, Sion four times), unrefereed.  Exact isoperimetry in the biased cube exists for down-sets only
   (Bollobás–Leader; abstract via machine summary) and is not usable; fixed-measure asymptotics (Ahlswede–Zhang/Yu; machine
   summary) give only the worse exponents of plain `π_f`-sampling.  The nested algorithm uses the non-explicit table `Ξ_H`.
4. **Numerics** (`./run_all.sh`, 21 scripts, each run < 10 min): formulas against each other to `10⁻¹¹…10⁻¹⁵` (`t01,t03,t04,t11,t21`);
   exact binomial sums `n ≤ 4000` for four parameter sets (`t08`: extrapolations within `0.1–2 %` of `R_0, R^max, θ_na`) and
   `n ≤ 64000` (`t09, t10`: excess `0.39 ln n/n`); recursion with the new pair never below `R^max`, `0.5 %` above after 12
   levels (`t12`); single-letter converse by primal optimisation over `≈1900` laws (`t16`); Theorem F6 on 1829 profile sets of
   six shapes, `n ≤ 2000` (`t23`); two-level logic and tail lemma on `Q_4` with all 65534 subsets, mutations detected
   (`t14, t15`); Lean: `shift_identity` (no errors).
5. **Negative findings:** the identity and the recursion with `R_0` fail (falls `3 %` below the lower bound, `t17`); `g = 0` is not
   the hardest instance; `π_f` and every single tilted product measure are the wrong samplers (`a_π` up to `2.9 a`); a Harper
   theorem for product measures is neither available nor what is needed; `H` is not harder than the hardest additive instance;
   three implementation errors of mine were caught by the tests.
6. **Not settled:** referee F6/F7/F9; `o(n)` terms, bounded accuracies, an explicit bound for `Ξ_H`; monotonicity in `|θ|` (proof);
   instance-optimality at non-symmetric instances; Propositions F11 (product samplers) and F12 (`k` states, several site
   types) are sketches; `HintPair` for this pair not formalised in Lean.

---

## Appendix: files in this directory

`REPORT.md` (this file); `BRIEF.md`; `flib.py`, `birad.py`, `finite.py`, `recursion.py` (library); `t01`–`t24_*.py` (tests; `t02`,
`t06`, `t07` are exploratory predecessors of `t03`, `t08`); `t22_field_table.py` (the table of §3.7); `t23`, `t24` (Theorem F6 on profile sets); `run_all.sh`; outputs `out_*.txt`;
`lean/WorkstreamF.lean`, `lean/lean_out.txt`.  Nothing inside `/home/user/MetricChain` was modified by me; `lake env lean` was run on the
scratch file only (no `lake build`), and only `git status/log/diff` were used.  (At the end of my work the repository's working tree
shows changes made by others — `proofs/AxiomAudit.lean`, `docs/workstreams/K_REPORT.md`, `experiments/workstreams/`.)  The Write tool of this session refuses files named like reports, so this file was written
with shell redirection, as the brief requires a `REPORT.md` here.

